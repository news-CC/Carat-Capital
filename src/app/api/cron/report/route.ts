import { timingSafeEqual } from 'node:crypto';

import { NextResponse } from 'next/server';

import { sendWeeklyReport } from '@/lib/email/weekly-report';
import { optionalEnv } from '@/lib/env';
import { estimatedRecoveredCents } from '@/lib/revenue';
import { supabaseAdmin } from '@/lib/supabase/admin';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 60;

const REACHED: ReadonlySet<string> = new Set(['answered', 'booked', 'declined', 'opted_out']);
const PERIOD_DAYS = 7;

type ClientRow = {
  id: string;
  name: string;
  contact_email: string;
  timezone: string;
  avg_ticket_cents: number;
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
      .select('id, name, contact_email, timezone, avg_ticket_cents')
      .eq('active', true);
    if (only) query = query.eq('id', only);

    const { data: clients, error } = await query;
    if (error) return NextResponse.json({ ok: false, error: error.message }, { status: 500 });

    const since = new Date(Date.now() - PERIOD_DAYS * 86_400_000);
    const results: ReportResult[] = [];

    for (const client of clients ?? []) {
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

async function reportFor(db: Db, client: ClientRow, since: Date): Promise<ReportResult> {
  const base = { clientId: client.id, salonName: client.name };

  // One broken client must not stop the rest of the Friday send.
  try {
    const { data: calls } = await db
      .from('calls')
      .select('outcome')
      .eq('client_id', client.id)
      .gte('created_at', since.toISOString());

    const rows = calls ?? [];
    const dialed = rows.length;
    if (dialed === 0) return { ...base, sent: false, reason: 'no_activity', dialed: 0, booked: 0 };

    const tally = (o: string) => rows.filter((r) => r.outcome === o).length;
    const booked = tally('booked');
    const stats = {
      dialed,
      reached: rows.filter((r) => REACHED.has(r.outcome)).length,
      booked,
      declined: tally('declined'),
      optedOut: tally('opted_out'),
    };

    const { data: bookings } = await db
      .from('bookings')
      .select('slot_text, contact_id')
      .eq('client_id', client.id)
      .gte('created_at', since.toISOString())
      .order('created_at', { ascending: false })
      .limit(5);

    const sent = await sendWeeklyReport({
      to: client.contact_email,
      salonName: client.name,
      periodLabel: periodLabel(since, client.timezone),
      ...stats,
      estimatedRecoveredCents: estimatedRecoveredCents(booked, client.avg_ticket_cents),
      avgTicketCents: client.avg_ticket_cents,
      topBookings: await namedBookings(db, bookings ?? []),
    });

    return sent.ok
      ? { ...base, sent: true, dialed, booked }
      : { ...base, sent: false, reason: sent.error, dialed, booked };
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
