import { timingSafeEqual } from 'node:crypto';

import { NextResponse } from 'next/server';

import { isInsideCallWindow } from '@/lib/call-window';
import { callWindow, maxConcurrentCalls, optionalEnv, requireConsent, serverEnv } from '@/lib/env';
import { maloneVariables } from '@/lib/malone';
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

    // One attempt per contact ever, so rows abandoned mid-dial are burned, not retried.
    await db.rpc('expire_stuck_calling', { p_older_than_minutes: 15 });

    const { count } = await db
      .from('calls')
      .select('id', { count: 'exact', head: true })
      .eq('outcome', 'dialing');

    const inFlight = Math.max(count ?? 0, await listActiveCallCount());
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

    const clientIds = [...new Set(claimed.map((c) => c.client_id))];
    const phones = claimed.map((c) => c.phone).filter((p): p is string => Boolean(p));

    const [clientsRes, suppressionRes] = await Promise.all([
      db.from('clients').select('*').in('id', clientIds),
      phones.length > 0
        ? db.from('suppression').select('phone').in('phone', phones)
        : Promise.resolve({ data: [] as { phone: string }[] }),
    ]);

    const clients = new Map((clientsRes.data ?? []).map((c) => [c.id, c]));
    const suppressed = new Set((suppressionRes.data ?? []).map((s) => s.phone));

    const assistantId = serverEnv('VAPI_ASSISTANT_ID');
    const phoneNumberId = serverEnv('VAPI_PHONE_NUMBER_ID');

    // The batch is already capped at the free concurrency slots, so dialing it in
    // parallel cannot exceed MAX_CONCURRENT_CALLS.
    const results = await Promise.all(
      claimed.map((contact) =>
        dialOne({
          db,
          contact,
          client: clients.get(contact.client_id),
          suppressed,
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
    if (requireConsent() && contact.consent !== true) {
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

    // Every dial attempt writes a calls row — success or failure. Unlogged calls are bugs.
    if (!started.ok) {
      await db.from('calls').insert({
        contact_id: contact.id,
        client_id: client.id,
        outcome: 'failed',
        ended_reason: started.error.slice(0, 500),
        started_at: new Date().toISOString(),
        ended_at: new Date().toISOString(),
      });
      await db.from('contacts').update({ status: 'failed' }).eq('id', contact.id);
      return 'failed';
    }

    await db.from('calls').insert({
      contact_id: contact.id,
      client_id: client.id,
      vapi_call_id: started.data.vapiCallId,
      outcome: 'dialing',
      started_at: new Date().toISOString(),
    });
    return 'dialed';
  } catch (e) {
    await db
      .from('contacts')
      .update({ status: 'failed', scrub_reason: e instanceof Error ? e.message.slice(0, 200) : 'dial_error' })
      .eq('id', contact.id);
    return 'failed';
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

function authorizeCron(req: Request): boolean {
  if (req.headers.get('x-vercel-cron')) return true;
  const secret = optionalEnv('CRON_SECRET');
  if (!secret) return false;
  const header = req.headers.get('authorization') ?? '';
  const expected = `Bearer ${secret}`;
  const a = Buffer.from(header, 'utf8');
  const b = Buffer.from(expected, 'utf8');
  return a.length === b.length && timingSafeEqual(a, b);
}
