import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

/**
 * The /start server action is the only public write path into the production database, so the
 * two properties that matter most are pinned here rather than left to a code comment:
 *
 *   1. the client row is inserted with `active = false` — `claim_contacts_for_dialing` requires
 *      `cl.active = true`, so this is the gate that stops a 3am signup from the open internet
 *      dialling anybody before an operator has looked at it; and
 *   2. a failed confirmation email never fails the signup — the lead is worth more than the
 *      receipt — but the confirmation screen must not then promise an email that is not coming.
 *
 * Supabase and Resend are stubbed. Nothing here touches a network or a database.
 */

/* ------------------------------------------------------------------ supabase stub */

type InsertCall = Record<string, unknown>;

const inserted: InsertCall[] = [];
const updated: InsertCall[] = [];
/** Rows the duplicate-lookup select pretends to find. */
let existingRows: { id: string; created_at: string }[] = [];
let insertFails = false;

/**
 * The narrow slice of the supabase-js builder the action actually uses. Every method returns
 * `this`, and the object is thenable so an un-terminated chain (`.eq(...)`) resolves like the
 * real builder does.
 */
function builder(table: string) {
  const state: { op: 'select' | 'insert' | 'update' | null; payload?: InsertCall } = { op: null };

  const result = () => {
    if (state.op === 'select') return { data: existingRows, error: null };
    if (state.op === 'insert') {
      if (insertFails) return { data: null, error: { message: 'connection reset by peer' } };
      return { data: { id: 'client-uuid-1' }, error: null };
    }
    return { data: null, error: null };
  };

  const chain = {
    select() {
      if (state.op === null) state.op = 'select';
      return chain;
    },
    insert(payload: InsertCall) {
      state.op = 'insert';
      state.payload = payload;
      inserted.push({ table, ...payload });
      return chain;
    },
    update(payload: InsertCall) {
      state.op = 'update';
      updated.push({ table, ...payload });
      return chain;
    },
    eq: () => chain,
    order: () => chain,
    limit: () => chain,
    single: async () => result(),
    maybeSingle: async () => result(),
    then: (resolve: (v: ReturnType<typeof result>) => unknown) => Promise.resolve(result()).then(resolve),
  };

  return chain;
}

vi.mock('@/lib/supabase/admin', () => ({
  supabaseAdmin: () => ({ from: (table: string) => builder(table) }),
}));

/* ------------------------------------------------------------------ resend stub */

const sent: { to: string; subject: string }[] = [];
/** Recipients whose sends should fail, matched by substring. */
let failSendTo: string[] = [];
/** Resend is down entirely — neither the operator nor the prospect is reachable. */
let failAllSends = false;

vi.mock('@/lib/email/client', () => ({
  sendEmail: async (a: { to: string; subject: string }) => {
    sent.push({ to: a.to, subject: a.subject });
    if (failAllSends || failSendTo.some((needle) => a.to.includes(needle))) {
      return { ok: false as const, error: 'resend rejected the message' };
    }
    return { ok: true as const, data: { id: 'msg_1' } };
  },
}));

/* ------------------------------------------------------------------ helpers */

import { startAction } from '@/app/start/actions';
import { HONEYPOT_FIELD, INITIAL_START_STATE } from '@/lib/onboarding';

const GOOD = {
  salon_name: 'Ridgeline Hair',
  contact_name: 'Renée Alvarez',
  contact_email: 'Renee@Ridgeline.example',
  contact_phone: '(415) 555-0142',
  business_type: 'salon',
  timezone: 'America/Los_Angeles',
  list_size: '250_1000',
  avg_ticket_dollars: '120',
  offer_text: 'A complimentary gloss with your next cut.',
};

function form(overrides: Record<string, string> = {}): FormData {
  const fd = new FormData();
  for (const [k, v] of Object.entries({ ...GOOD, ...overrides })) fd.set(k, v);
  return fd;
}

const submit = (fd: FormData) => startAction(INITIAL_START_STATE, fd);

beforeEach(() => {
  inserted.length = 0;
  updated.length = 0;
  sent.length = 0;
  existingRows = [];
  insertFails = false;
  failSendTo = [];
  failAllSends = false;
  vi.spyOn(console, 'error').mockImplementation(() => {});
  vi.spyOn(console, 'warn').mockImplementation(() => {});
});

afterEach(() => {
  vi.restoreAllMocks();
});

/* ------------------------------------------------------------------ 1. active = false */

describe('the insert is switched off', () => {
  it('writes active = false so the new client cannot be claimed for dialing', async () => {
    const state = await submit(form());

    expect(state.status).toBe('success');
    expect(inserted).toHaveLength(1);
    expect(inserted[0].active).toBe(false);
  });

  it('never writes active = true, whatever the business type or list size', async () => {
    for (const business_type of ['salon', 'medspa', 'multi-location']) {
      for (const list_size of ['under_250', '250_1000', '1000_5000', '5000_plus']) {
        inserted.length = 0;
        await submit(form({ business_type, list_size }));
        expect(inserted[0].active).toBe(false);
      }
    }
  });

  it('stores the normalized phone and the stated vertical alongside it', async () => {
    await submit(form({ business_type: 'multi-location' }));

    expect(inserted[0].contact_phone).toBe('+14155550142');
    // The schema has two verticals; a group is a group of salons.
    expect(inserted[0].vertical).toBe('salon');
    expect(inserted[0].avg_ticket_cents).toBe(12_000);
    expect(inserted[0].stripe_status).toBe('trialing');
    // Lower-cased so the Stripe webhook's email match is not case-sensitive by accident.
    expect(inserted[0].contact_email).toBe('renee@ridgeline.example');
  });

  it('does not touch active when it updates a row inside the de-dupe window', async () => {
    existingRows = [{ id: 'existing-1', created_at: new Date().toISOString() }];

    const state = await submit(form());

    expect(state.status).toBe('success');
    expect(inserted).toHaveLength(0);
    expect(updated).toHaveLength(1);
    // A resubmit must never flip the dialing switch in either direction, nor un-pay someone who
    // clicked the payment link between the two submits.
    expect(updated[0]).not.toHaveProperty('active');
    expect(updated[0]).not.toHaveProperty('stripe_status');
  });
});

/* ------------------------------------------------------------------ 2. email failure */

describe('a failed confirmation email does not fail the signup', () => {
  it('still succeeds, still saves, and still tells the operator', async () => {
    failSendTo = ['ridgeline.example'];

    const state = await submit(form());

    expect(state.status).toBe('success');
    expect(state.error).toBeUndefined();
    expect(inserted).toHaveLength(1);
    expect(inserted[0].active).toBe(false);
    // Both emails were attempted; only the prospect's failed.
    expect(sent).toHaveLength(2);
  });

  it('does not promise an inbox copy that is not coming', async () => {
    failSendTo = ['ridgeline.example'];
    const failed = await submit(form());
    expect(failed.success?.confirmationEmailed).toBe(false);

    failSendTo = [];
    const delivered = await submit(form());
    expect(delivered.success?.confirmationEmailed).toBe(true);
  });

  it('survives the database write failing, as long as the operator was emailed', async () => {
    insertFails = true;

    const state = await submit(form());

    // The lead lives in the operator email instead — the prospect is not shown a broken screen.
    expect(state.status).toBe('success');
    expect(sent.some((e) => e.subject.startsWith('SIGNUP NOT SAVED'))).toBe(true);
  });

  it('only errors when the row did not save AND the operator was not told', async () => {
    insertFails = true;
    failAllSends = true;

    const state = await submit(form());

    expect(state.status).toBe('error');
    expect(state.error).toContain('@');
    // Everything typed is echoed back so nobody retypes their offer.
    expect(state.values?.offer_text).toBe(GOOD.offer_text);
  });

  it('leaks no database detail to the browser', async () => {
    insertFails = true;
    failAllSends = true;

    const state = await submit(form());

    expect(state.error).not.toContain('connection reset');
  });
});

/* ------------------------------------------------------------------ gates */

describe('the public endpoint gates', () => {
  it('discards a honeypot submission without writing or sending anything', async () => {
    const state = await submit(form({ [HONEYPOT_FIELD]: 'http://spam.example' }));

    expect(state.status).toBe('success'); // a bot is told nothing
    expect(inserted).toHaveLength(0);
    expect(updated).toHaveLength(0);
    expect(sent).toHaveLength(0);
  });

  it('rejects an invalid submission before it reaches the database', async () => {
    const state = await submit(form({ contact_email: 'not-an-email' }));

    expect(state.status).toBe('error');
    expect(state.fieldErrors?.contact_email).toBeTruthy();
    expect(inserted).toHaveLength(0);
    expect(sent).toHaveLength(0);
  });

  it('rejects a phone number it could not dial', async () => {
    const state = await submit(form({ contact_phone: '12345' }));

    expect(state.status).toBe('error');
    expect(state.fieldErrors?.contact_phone).toBeTruthy();
    expect(inserted).toHaveLength(0);
  });
});
