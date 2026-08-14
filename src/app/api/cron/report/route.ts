import { NextResponse } from 'next/server';

import { REACHED_OUTCOMES } from '@/lib/calls';
import { authorizeCron } from '@/lib/cron-auth';
import { sendWeeklyReport } from '@/lib/email/weekly-report';
import { estimatedRecoveredCents } from '@/lib/revenue';
import { supabaseAdmin } from '@/lib/supabase/admin';
import type { CallOutcome } from '@/lib/types';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 60;

const PERIOD_DAYS = 7;

/**
 * Billing state, not `clients.active`: `active` is the campaign on/off switch that pauseCampaign
 * flips, and a salon we dialed Monday to Wednesday still earned Friday's wrap-up if the operator
 * paused it on Thursday. Wider than the dialer's BILLABLE set on purpose — a past_due salon is
 * exactly who needs to see the revenue we recovered — because this email spends nothing on their
 * behalf. Canceled means the relationship is over, so no email. Dormant clients need no filter:
 * the `dialed === 0` skip below already keeps them out of the send.
 */
const REPORTABLE_STATUSES: ReadonlySet<string> = new Set(['trialing', 'active', 'past_due']);

type ClientRow = {
  id: string;
  name: string;
  contact_email: string;
  timezone: string;
  avg_ticket_cents: number;
  stripe_status: string;
};

type ReportResult = {
  clientId: string;
  salonName: string;
  sent: boolean;
  reason?: string;
  dialed: number;
  booked: number;
};

export async function GET(req: Request) {
  if (!authorizeCron(req)) {
    return NextResponse.json({ ok: false, error: 'unauthorized' }, { status: 401 });
  }

  try {
    const db = supabaseAdmin();
    // Optional single-client send, so the admin "send report now" button can reuse this route.
    const only = new URL(req.url).searchParams.get('client_id');

    let query = db
      .from('clients')
      .select('id, name, contact_email, timezone, avg_ticket_cents, stripe_status');
    // A single-client send skips the SQL filter so the operator gets a real reason back instead of
    // an empty result set. The same gate still runs in the loop below, so it cannot email anyone
    // the Friday run would not.
    if (only) query = query.eq('id', only);
    else query = query.in('stripe_status', [...REPORTABLE_STATUSES]);

    const { data: clients, error } = await query;
    if (error) return NextResponse.json({ ok: false, error: error.message }, { status: 500 });

    const since = new Date(Date.now() - PERIOD_DAYS * 86_400_000);
    const results: ReportResult[] = [];

    for (const client of clients ?? []) {
      // GATE: the billing check the Friday query applies in SQL, re-run here so a single-client
      // send names the reason instead of quietly emailing a client the cron would skip.
      if (!REPORTABLE_STATUSES.has(client.stripe_status)) {
        results.push({
          clientId: client.id,
          salonName: client.name,
          sent: false,
          reason: `not_reportable: billing is ${client.stripe_status}`,
          dialed: 0,
          booked: 0,
        });
        continue;
      }
      results.push(await reportFor(db, client, since));
    }

    return NextResponse.json({
      ok: true,
      period: { since: since.toISOString(), days: PERIOD_DAYS },
      sent: results.filter((r) => r.sent).length,
      skipped: results.filter((r) => !r.sent).length,
      results,
    });
  } catch (e) {
    return NextResponse.json(
      { ok: false, error: e instanceof Error ? e.message : 'report run failed' },
      { status: 500 },
    );
  }
}

type Db = ReturnType<typeof supabaseAdmin>;
type Count = { value: number; error: string | null };

async function reportFor(db: Db, client: ClientRow, since: Date): Promise<ReportResult> {
  const base = { clientId: client.id, salonName: client.name };

  // One broken client must not stop the rest of the Friday send.
  try {
    const [dialedCount, reached, booked, declined, optedOut] = await Promise.all([
      countCalls(db, client.id, since),
      countCalls(db, client.id, since, REACHED_OUTCOMES),
      // Booked comes from the bookings TABLE, not from calls.outcome — the same source
      // /admin/bookings and the dashboard tile read. A call can both book a slot and opt out (the
      // webhook writes the booking and stores outcome='opted_out', because the opt-out is the
      // compliance fact), so counting outcome='booked' would leave an appointment that is sitting
      // in the owner's inbox and in /admin/bookings missing from the Friday tally, and understate
      // the recovered-revenue figure computed from it.
      countBookings(db, client.id, since),
      countCalls(db, client.id, since, ['declined']),
      countCalls(db, client.id, since, ['opted_out']),
    ]);

    // A failed count must never read as a quiet week: 'no_activity' drops the retention email and
    // tells the operator there was nothing to send, which a broken query would make a lie.
    const failed = [dialedCount, reached, booked, declined, optedOut].find((c) => c.error !== null);
    if (failed?.error) {
      return {
        ...base,
        sent: false,
        reason: `counts_query_failed: ${failed.error}`,
        dialed: 0,
        booked: 0,
      };
    }

    const dialed = dialedCount.value;
    if (dialed === 0) return { ...base, sent: false, reason: 'no_activity', dialed: 0, booked: 0 };

    const stats = {
      dialed,
      reached: reached.value,
      booked: booked.value,
      declined: declined.value,
      optedOut: optedOut.value,
    };

    const { data: bookings, error: bookingsError } = await db
      .from('bookings')
      .select('slot_text, contact_id')
      .eq('client_id', client.id)
      .gte('created_at', since.toISOString())
      .order('created_at', { ascending: false })
      .limit(5);

    if (bookingsError) {
      // The counts above are the numbers the client reads; the highlights are a nicety. Send the
      // report without them rather than not at all, but say so in the log.
      console.error('[cron-report] booking highlights unavailable', client.id, bookingsError.message);
    }

    const sent = await sendWeeklyReport({
      to: client.contact_email,
      salonName: client.name,
      periodLabel: periodLabel(since, client.timezone),
      ...stats,
      estimatedRecoveredCents: estimatedRecoveredCents(stats.booked, client.avg_ticket_cents),
      avgTicketCents: client.avg_ticket_cents,
      topBookings: await namedBookings(db, bookings ?? []),
    });

    return sent.ok
      ? { ...base, sent: true, dialed, booked: stats.booked }
      : { ...base, sent: false, reason: sent.error, dialed, booked: stats.booked };
  } catch (e) {
    return {
      ...base,
      sent: false,
      reason: e instanceof Error ? e.message : 'report failed',
      dialed: 0,
      booked: 0,
    };
  }
}

/**
 * Counted in the database, never tallied from fetched rows: PostgREST caps a response at 1000 rows,
 * so `rows.length` would silently understate dialed, booked and recovered revenue for exactly the
 * busy clients the Friday email has to keep.
 */
async function countCalls(
  db: Db,
  clientId: string,
  since: Date,
  outcomes?: CallOutcome[],
): Promise<Count> {
  let query = db
    .from('calls')
    .select('*', { count: 'exact', head: true })
    .eq('client_id', clientId)
    .gte('created_at', since.toISOString());
  if (outcomes) query = query.in('outcome', outcomes);

  const { count, error } = await query;
  return { value: count ?? 0, error: error?.message ?? null };
}

/** Bookings written in the period. One row per appointment, whatever the call's outcome was. */
async function countBookings(db: Db, clientId: string, since: Date): Promise<Count> {
  const { count, error } = await db
    .from('bookings')
    .select('*', { count: 'exact', head: true })
    .eq('client_id', clientId)
    .gte('created_at', since.toISOString());
  return { value: count ?? 0, error: error?.message ?? null };
}

/** Two small queries instead of a join — keeps us off relational typing. */
async function namedBookings(
  db: Db,
  bookings: { slot_text: string; contact_id: string | null }[],
): Promise<{ firstName: string; slotText: string }[]> {
  const ids = bookings.map((b) => b.contact_id).filter((id): id is string => Boolean(id));
  if (ids.length === 0) return bookings.map((b) => ({ firstName: 'A client', slotText: b.slot_text }));

  const { data: contacts } = await db.from('contacts').select('id, first_name, name').in('id', ids);
  const names = new Map((contacts ?? []).map((c) => [c.id, c.first_name ?? c.name ?? 'A client']));

  return bookings.map((b) => ({
    firstName: (b.contact_id ? names.get(b.contact_id) : null) ?? 'A client',
    slotText: b.slot_text,
  }));
}

function periodLabel(since: Date, timeZone: string): string {
  const day = (d: Date, tz: string) =>
    new Intl.DateTimeFormat('en-US', { timeZone: tz, month: 'short', day: 'numeric' }).format(d);
  try {
    return `${day(since, timeZone)} – ${day(new Date(), timeZone)}`;
  } catch {
    return `${day(since, 'UTC')} – ${day(new Date(), 'UTC')}`;
  }
}
