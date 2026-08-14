import Link from 'next/link';
import { requireAdmin } from '@/lib/auth';
import { callWindow, maxConcurrentCalls } from '@/lib/env';
import { isInsideCallWindow, localTimeInZone, nextWindowOpenLabel } from '@/lib/call-window';
import { usd } from '@/lib/money';
import { estimatedRecoveredCents, reachRate } from '@/lib/revenue';
import { supabaseAdmin } from '@/lib/supabase/admin';
import type { CallOutcome } from '@/lib/types';
import { CallsTable, type CallRowView } from '@/components/admin/CallsTable';
import { ClientCard, type ClientCardData } from '@/components/admin/ClientCard';
import { QueueMeter } from '@/components/admin/QueueMeter';

export const dynamic = 'force-dynamic';

/** A human answered. Voicemail and busy are dials, not conversations. */
const REACHED_OUTCOMES: CallOutcome[] = ['answered', 'booked', 'declined', 'opted_out'];

const n = (r: { count: number | null }): number => r.count ?? 0;

export default async function DashboardPage() {
  await requireAdmin(); // gate: defence in depth — the layout checks too
  const db = supabaseAdmin();
  const since = new Date(Date.now() - 7 * 86_400_000).toISOString();
  const { start, end } = callWindow();
  const cap = maxConcurrentCalls();

  const [pending, dialed, reached, booked, optOuts, inFlight, clientsRes, callsRes] = await Promise.all([
    db.from('contacts').select('*', { count: 'exact', head: true }).eq('status', 'pending'),
    db.from('calls').select('*', { count: 'exact', head: true }).gte('created_at', since),
    db
      .from('calls')
      .select('*', { count: 'exact', head: true })
      .gte('created_at', since)
      .in('outcome', REACHED_OUTCOMES),
    db.from('bookings').select('*', { count: 'exact', head: true }).gte('created_at', since),
    db.from('suppression').select('*', { count: 'exact', head: true }).eq('reason', 'opt_out'),
    db.from('calls').select('*', { count: 'exact', head: true }).eq('outcome', 'dialing'),
    db
      .from('clients')
      .select('id, name, vertical, timezone, stripe_status, active, avg_ticket_cents')
      .order('created_at', { ascending: true }),
    db
      .from('calls')
      .select(
        'id, client_id, contact_id, outcome, duration_seconds, cost_usd, transcript_url, recording_url, summary, started_at, created_at',
      )
      .order('created_at', { ascending: false })
      .limit(8),
  ]);

  const clients = clientsRes.data ?? [];
  const calls = callsRes.data ?? [];
  const contactIds = calls.map((c) => c.contact_id).filter((id): id is string => Boolean(id));

  const [contactsRes, perClient] = await Promise.all([
    contactIds.length > 0
      ? db.from('contacts').select('id, name, first_name, phone').in('id', contactIds)
      : null,
    // Two count queries per client — PostgREST cannot group, and counts stay cheap.
    Promise.all(
      clients.flatMap((client) => [
        db
          .from('contacts')
          .select('*', { count: 'exact', head: true })
          .eq('client_id', client.id)
          .eq('status', 'pending'),
        db
          .from('bookings')
          .select('*', { count: 'exact', head: true })
          .eq('client_id', client.id)
          .gte('created_at', since),
      ]),
    ),
  ]);

  const cards: ClientCardData[] = clients.map((client, i) => {
    const booked7d = n(perClient[i * 2 + 1]);
    return {
      id: client.id,
      name: client.name,
      vertical: client.vertical,
      timezone: client.timezone,
      stripeStatus: client.stripe_status,
      active: client.active,
      localTime: localTimeInZone(client.timezone),
      // Window state and paused state are separate facts — the card shows both.
      windowOpen: isInsideCallWindow(client.timezone, start, end),
      windowHint: nextWindowOpenLabel(client.timezone, start, end),
      pending: n(perClient[i * 2]),
      booked7d,
      recovered7dCents: estimatedRecoveredCents(booked7d, client.avg_ticket_cents),
    };
  });

  const contacts = new Map((contactsRes?.data ?? []).map((c) => [c.id, c]));
  const clientsById = new Map(clients.map((c) => [c.id, c]));
  const recovered7dCents = cards.reduce((sum, card) => sum + card.recovered7dCents, 0);
  const rate = reachRate(n(reached), n(dialed));

  const recent: CallRowView[] = calls.map((call) => {
    const client = call.client_id ? clientsById.get(call.client_id) : undefined;
    const contact = call.contact_id ? contacts.get(call.contact_id) : undefined;
    return {
      id: call.id,
      clientName: client?.name ?? '—',
      timeZone: client?.timezone ?? 'UTC',
      contactName: contact?.name ?? contact?.first_name ?? null,
      phone: contact?.phone ?? null,
      outcome: call.outcome,
      durationSeconds: call.duration_seconds,
      costUsd: call.cost_usd,
      transcriptUrl: call.transcript_url,
      recordingUrl: call.recording_url,
      summary: call.summary,
      at: call.started_at ?? call.created_at,
    };
  });

  return (
    <div className="flex flex-col gap-10">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="eyebrow">Dashboard</p>
          <h1 className="h-display">The state of the floor</h1>
        </div>
        <p className="text-sm text-ink-mute tabular-nums">
          Rolling 7 days · call window {start}–{end}, each client&rsquo;s local time
        </p>
      </header>

      {clientsRes.error && (
        <p className="error-text">Could not load clients: {clientsRes.error.message}</p>
      )}

      <section className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
        <div className="stat">
          <p className="stat-num tabular-nums">{n(pending).toLocaleString('en-US')}</p>
          <p className="stat-label">Contacts queued</p>
        </div>
        <div className="stat">
          <p className="stat-num tabular-nums">{n(dialed).toLocaleString('en-US')}</p>
          <p className="stat-label">Dialed · 7d</p>
        </div>
        <div className="stat">
          <p className="stat-num tabular-nums">{n(reached).toLocaleString('en-US')}</p>
          <p className="stat-label">Reached · {Math.round(rate * 100)}%</p>
        </div>
        <div className="stat">
          <p className="stat-num tabular-nums">{n(booked).toLocaleString('en-US')}</p>
          <p className="stat-label">Booked · 7d</p>
        </div>
        <div className="stat">
          <p className="stat-num tabular-nums text-brass-deep">{usd(recovered7dCents)}</p>
          <p className="stat-label">Est. recovered · 7d</p>
        </div>
        <div className="stat">
          <p className="stat-num tabular-nums">{n(optOuts).toLocaleString('en-US')}</p>
          <p className="stat-label">Opt-outs · total</p>
        </div>
      </section>

      <QueueMeter
        inFlight={n(inFlight)}
        cap={cap}
        pending={n(pending)}
        windowLabel={`${start}–${end}`}
      />

      <section className="flex flex-col gap-4">
        <div className="flex items-baseline justify-between gap-4">
          <h2 className="h-display text-xl">Clients</h2>
          <Link className="btn btn-ghost btn-sm" href="/admin/clients">
            All clients
          </Link>
        </div>
        {cards.length === 0 ? (
          <div className="card card-pad">
            <p className="prose-tight">
              No clients yet. Add the salon first — the offer text and timezone you enter there are what
              Malone actually says and obeys.
            </p>
            <Link className="btn btn-primary mt-4 inline-flex" href="/admin/clients">
              Add the first client
            </Link>
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {cards.map((card) => (
              <ClientCard key={card.id} client={card} />
            ))}
          </div>
        )}
      </section>

      <section className="flex flex-col gap-4">
        <div className="flex items-baseline justify-between gap-4">
          <h2 className="h-display text-xl">Latest calls</h2>
          <Link className="btn btn-ghost btn-sm" href="/admin/calls">
            All calls
          </Link>
        </div>
        <div className="card">
          <CallsTable rows={recent} />
        </div>
      </section>
    </div>
  );
}
