import { NextResponse } from 'next/server';

import { isInsideCallWindow } from '@/lib/call-window';
import { countLiveCalls, STUCK_CALL_MINUTES } from '@/lib/calls';
import { authorizeCron } from '@/lib/cron-auth';
import { callWindow, dialFictionalNumbers, maxConcurrentCalls, serverEnv } from '@/lib/env';
import { maloneVariables } from '@/lib/malone';
import { isFictionalPhone } from '@/lib/phone';
import { supabaseAdmin } from '@/lib/supabase/admin';
import type { Contact } from '@/lib/types';
import { listActiveCallCount, startOutboundCall } from '@/lib/vapi';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 60;

type Outcome = 'dialed' | 'failed' | 'skipped';

export async function GET(req: Request) {
  if (!authorizeCron(req)) {
    return NextResponse.json({ ok: false, error: 'unauthorized' }, { status: 401 });
  }

  try {
    const db = supabaseAdmin();
    const window = callWindow();

    // Read the Vapi ids BEFORE anything is claimed. serverEnv throws on a missing or blank
    // value — a deploy state setup-vapi.mjs prints on purpose — and a throw after the claim
    // would leave the batch at status='calling' with its single attempt already spent, for
    // expire_stuck_calling to burn to 'failed' without a call ever being placed.
    const assistantId = serverEnv('VAPI_ASSISTANT_ID');
    const phoneNumberId = serverEnv('VAPI_PHONE_NUMBER_ID');

    // One attempt per contact ever, so rows abandoned mid-dial are burned, not retried.
    await db.rpc('expire_stuck_calling', { p_older_than_minutes: STUCK_CALL_MINUTES });

    // In-flight means "has not ended", not outcome='dialing' — see countLiveCalls, which the
    // dashboard's in-flight tile shares so the two surfaces cannot disagree. Vapi's own count is
    // the other half: whichever is higher wins, because over-counting lines is the fail-closed
    // direction for a concurrency cap.
    const inFlight = Math.max(await countLiveCalls(db), await listActiveCallCount());
    const slots = Math.max(0, maxConcurrentCalls() - inFlight);
    if (slots === 0) {
      return NextResponse.json({
        ok: true,
        claimed: 0,
        dialed: 0,
        failed: 0,
        skipped: 0,
        inFlight,
        reason: 'at_capacity',
      });
    }

    const { data, error } = await db.rpc('claim_contacts_for_dialing', {
      p_limit: slots,
      p_window_start: window.start,
      p_window_end: window.end,
    });
    if (error) {
      return NextResponse.json({ ok: false, error: error.message }, { status: 500 });
    }

    const claimed = (Array.isArray(data) ? data : []) as Contact[];
    if (claimed.length === 0) {
      return NextResponse.json({
        ok: true,
        claimed: 0,
        dialed: 0,
        failed: 0,
        skipped: 0,
        inFlight,
        reason: 'nothing_to_dial',
      });
    }

    const batch = await loadBatchContext(db, claimed);

    // The batch is already capped at the free concurrency slots, so dialing it in
    // parallel cannot exceed MAX_CONCURRENT_CALLS.
    const results = await Promise.all(
      claimed.map((contact) =>
        dialOne({
          db,
          contact,
          client: batch.clients.get(contact.client_id),
          suppressed: batch.suppressed,
          window,
          assistantId,
          phoneNumberId,
        }),
      ),
    );

    return NextResponse.json({
      ok: true,
      claimed: claimed.length,
      dialed: results.filter((r) => r === 'dialed').length,
      failed: results.filter((r) => r === 'failed').length,
      skipped: results.filter((r) => r === 'skipped').length,
      inFlight,
      window,
    });
  } catch (e) {
    return NextResponse.json(
      { ok: false, error: e instanceof Error ? e.message : 'dial run failed' },
      { status: 500 },
    );
  }
}

type Db = ReturnType<typeof supabaseAdmin>;
type ClientRow = {
  id: string;
  name: string;
  timezone: string;
  offer_text: string;
  booking_phone: string | null;
  active: boolean;
  stripe_status: string;
};

const BILLABLE: ReadonlySet<string> = new Set(['active', 'trialing']);

/**
 * The client rows and suppression hits the batch needs before it can dial.
 *
 * This is the whole window between the claim and the first dial, and it is a function so it
 * stays that way. The claim RPC has already spent every claimed contact's one and only
 * attempt, so a throw in here must hand those attempts back: left at status='calling' the
 * rows get burned to 'failed' by expire_stuck_calling without a call ever being placed, and
 * nothing in the codebase returns a 'failed' contact to 'pending'. These two queries do not
 * reject today (postgrest reports errors as values, and a null data lands in dialOne's
 * !client branch, which releases), so the release is the guarantee for whatever gets added
 * here next. Only the pre-dial window gets it — once a number has been handed to Vapi the
 * attempt is genuinely spent, and releasing it would risk dialing a consumer twice.
 */
async function loadBatchContext(
  db: Db,
  claimed: Contact[],
): Promise<{ clients: Map<string, ClientRow>; suppressed: Set<string> }> {
  try {
    const clientIds = [...new Set(claimed.map((c) => c.client_id))];
    const phones = claimed.map((c) => c.phone).filter((p): p is string => Boolean(p));

    const [clientsRes, suppressionRes] = await Promise.all([
      db.from('clients').select('*').in('id', clientIds),
      phones.length > 0
        ? db.from('suppression').select('phone').in('phone', phones)
        : Promise.resolve({ data: [] as { phone: string }[] }),
    ]);

    return {
      clients: new Map((clientsRes.data ?? []).map((c) => [c.id, c])),
      suppressed: new Set((suppressionRes.data ?? []).map((s) => s.phone)),
    };
  } catch (e) {
    await releaseBatchToPending(db, claimed);
    throw e;
  }
}

async function dialOne(a: {
  db: Db;
  contact: Contact;
  client: ClientRow | undefined;
  suppressed: Set<string>;
  window: { start: string; end: string };
  assistantId: string;
  phoneNumberId: string;
}): Promise<Outcome> {
  const { db, contact, client } = a;

  // One bad contact must never fail the batch.
  try {
    if (!client) {
      await releaseToPending(db, contact);
      return 'skipped';
    }

    // Paused or lapsed client: not a compliance failure, so the attempt is given back.
    if (!client.active || !BILLABLE.has(client.stripe_status)) {
      await releaseToPending(db, contact);
      return 'skipped';
    }

    if (!contact.phone) {
      await db
        .from('contacts')
        .update({ status: 'invalid', scrub_reason: 'missing_phone', claimed_at: null })
        .eq('id', contact.id);
      return 'skipped';
    }

    // Gate 1 (re-check): consent. The claim SQL already filtered; we do not trust it alone.
    // Unconditional, with no REQUIRE_CONSENT_FLAG in it: contacts.consent now records what the
    // uploaded sheet actually said (see scrub.ts GATE 1), so `false` here means this row's source
    // never claimed consent. The flag decides whether such a row may be STORED, never whether it
    // may be DIALED — and the SQL gate is `c2.consent = true` either way, so reading the flag here
    // could only ever weaken a gate SQL already enforces.
    if (contact.consent !== true) {
      await db
        .from('contacts')
        .update({ status: 'suppressed', scrub_reason: 'no_consent', claimed_at: null })
        .eq('id', contact.id);
      return 'skipped';
    }

    // Gate 2 (re-check): global suppression list.
    if (a.suppressed.has(contact.phone)) {
      await db
        .from('contacts')
        .update({ status: 'suppressed', scrub_reason: 'suppressed', claimed_at: null })
        .eq('id', contact.id);
      return 'skipped';
    }

    // Gate 3 (re-check): call window in the CLIENT's timezone. Fails closed on a bad tz.
    // A window miss is not an attempt — give the contact its single try back.
    if (!isInsideCallWindow(client.timezone, a.window.start, a.window.end)) {
      await releaseToPending(db, contact);
      return 'skipped';
    }

    // Gate 4: 555-01XX is the reserved-for-fiction range — the demo list is built entirely from
    // it. Those numbers do not route, so dialing them is 250 billed failures that also burn 250
    // contacts' single attempt. scrub.ts keeps them on purpose; this is where they stop.
    if (!dialFictionalNumbers() && isFictionalPhone(contact.phone)) {
      await db
        .from('contacts')
        .update({ status: 'invalid', scrub_reason: 'fiction_range_demo_number', claimed_at: null })
        .eq('id', contact.id);
      return 'skipped';
    }

    const started = await startOutboundCall({
      phone: contact.phone,
      assistantId: a.assistantId,
      phoneNumberId: a.phoneNumberId,
      variables: maloneVariables({
        first_name: contact.first_name ?? contact.name ?? '',
        salon_name: client.name,
        offer_text: client.offer_text,
        booking_phone: client.booking_phone ?? '',
      }),
      metadata: { contact_id: contact.id, client_id: client.id, campaign: contact.campaign },
    });

    // Every dial attempt writes a calls row — success or failure. Unlogged calls are bugs,
    // so a failed insert is shouted about rather than swallowed.
    if (!started.ok) {
      const logged = await db.from('calls').insert({
        contact_id: contact.id,
        client_id: client.id,
        outcome: 'failed',
        ended_reason: started.error.slice(0, 500),
        started_at: new Date().toISOString(),
        ended_at: new Date().toISOString(),
      });
      if (logged.error) {
        console.error('[cron-dial] failed dial went unlogged', contact.id, logged.error.message);
      }
      await db.from('contacts').update({ status: 'failed' }).eq('id', contact.id);
      return 'failed';
    }

    const logged = await db.from('calls').insert({
      contact_id: contact.id,
      client_id: client.id,
      vapi_call_id: started.data.vapiCallId,
      outcome: 'dialing',
      started_at: new Date().toISOString(),
    });
    if (logged.error) {
      // The call is live at Vapi but we have no row for it. The webhook will upsert one on
      // vapi_call_id, so this is recoverable — but it has to be visible in the logs.
      console.error(
        '[cron-dial] live call went unlogged',
        started.data.vapiCallId,
        logged.error.message,
      );
    }
    return 'dialed';
  } catch (e) {
    await db
      .from('contacts')
      .update({ status: 'failed', scrub_reason: e instanceof Error ? e.message.slice(0, 200) : 'dial_error' })
      .eq('id', contact.id);
    return 'failed';
  }
}

/**
 * Batch form of releaseToPending, for a failure that hit the whole claimed batch before the
 * first dial. Deliberately swallows its own errors: the failure that triggered the release is
 * the one worth surfacing, and a row we could not release is left for the stuck sweeper.
 */
async function releaseBatchToPending(db: Db, contacts: Contact[]): Promise<void> {
  const settled = await Promise.allSettled(contacts.map((c) => releaseToPending(db, c)));
  for (const [i, result] of settled.entries()) {
    if (result.status === 'rejected') {
      console.error('[cron-dial] claimed contact left in calling', contacts[i].id, result.reason);
    }
  }
}

/** Hand the contact its single attempt back — used only when we never touched the phone. */
async function releaseToPending(db: Db, contact: Contact): Promise<void> {
  await db
    .from('contacts')
    .update({
      status: 'pending',
      claimed_at: null,
      attempts: Math.max(0, contact.attempts - 1),
    })
    .eq('id', contact.id);
}
