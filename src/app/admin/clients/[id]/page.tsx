import Link from 'next/link';
import { notFound } from 'next/navigation';
import { requireAdmin } from '@/lib/auth';
import { isInsideCallWindow, localTimeInZone, nextWindowOpenLabel } from '@/lib/call-window';
import { callWindow } from '@/lib/env';
import { usd } from '@/lib/money';
import { formatPhone } from '@/lib/phone';
import { estimatedRecoveredCents } from '@/lib/revenue';
import { supabaseAdmin } from '@/lib/supabase/admin';
import type { ContactStatus } from '@/lib/types';
import { BookingsTable, type BookingRowView } from '@/components/admin/BookingsTable';
import { CallsTable, type CallRowView } from '@/components/admin/CallsTable';
import { ClientForm } from '@/components/admin/ClientForm';
import { StatusPill, WindowPill } from '@/components/admin/StatusPill';
import { sendWeeklyReportNowAction } from '@/app/admin/clients/actions';
import { pauseCampaign, startCampaign } from '@/app/admin/clients/[id]/campaign-actions';

export const dynamic = 'force-dynamic';

const CONTACTS_SHOWN = 50;

/** Audit order: still ours → in motion → outcomes → the ones the gates removed. */
const AUDIT_STATUSES: ContactStatus[] = [
  'pending',
  'calling',
  'called',
  'no_answer',
  'booked',
  'declined',
  'opted_out',
  'suppressed',
  'invalid',
  'failed',
];

const n = (r: { count: number | null }): number => r.count ?? 0;

export default async function ClientDetailPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ notice?: string; error?: string }>;
}) {
  await requireAdmin(); // gate
  const [{ id }, { notice, error }] = await Promise.all([params, searchParams]);
  const db = supabaseAdmin();
  const { start, end } = callWindow();

  const { data: client } = await db.from('clients').select('*').eq('id', id).maybeSingle();
  if (!client) notFound();

  const [statusCounts, contactsRes, contactTotal, callsRes, bookingsRes] = await Promise.all([
    Promise.all(
      AUDIT_STATUSES.map((status) =>
        db
          .from('contacts')
          .select('*', { count: 'exact', head: true })
          .eq('client_id', id)
          .eq('status', status),
      ),
    ),
    db
      .from('contacts')
      .select(
        'id, name, first_name, phone, email, campaign, consent, last_visit, lifetime_value_cents, status, scrub_reason, attempts',
      )
      .eq('client_id', id)
      .order('created_at', { ascending: false })
      .limit(CONTACTS_SHOWN),
    db.from('contacts').select('*', { count: 'exact', head: true }).eq('client_id', id),
    db
      .from('calls')
      .select(
        'id, contact_id, outcome, duration_seconds, cost_usd, transcript_url, recording_url, summary, started_at, created_at',
      )
      .eq('client_id', id)
      .order('created_at', { ascending: false })
      .limit(25),
    db
      .from('bookings')
      .select('id, contact_id, slot_text, confirmed, notified_at, estimated_value_cents, created_at')
      .eq('client_id', id)
      .order('created_at', { ascending: false })
      .limit(25),
  ]);

  const contacts = contactsRes.data ?? [];
  const calls = callsRes.data ?? [];
  const bookings = bookingsRes.data ?? [];

  const relatedIds = [...calls, ...bookings]
    .map((row) => row.contact_id)
    .filter((cid): cid is string => Boolean(cid));
  const relatedRes =
    relatedIds.length > 0
      ? await db.from('contacts').select('id, name, first_name, phone').in('id', relatedIds)
      : null;
  const related = new Map((relatedRes?.data ?? []).map((c) => [c.id, c]));

  const audit = AUDIT_STATUSES.map((status, i) => ({ status, count: n(statusCounts[i]) }));
  const bookedCount = audit.find((a) => a.status === 'booked')?.count ?? 0;
  // Two independent facts: is the window open, and is the campaign live. Both are shown.
  const windowOpen = isInsideCallWindow(client.timezone, start, end);

  const callRows: CallRowView[] = calls.map((call) => {
    const contact = call.contact_id ? related.get(call.contact_id) : undefined;
    return {
      id: call.id,
      clientName: client.name,
      timeZone: client.timezone,
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

  const bookingRows: BookingRowView[] = bookings.map((booking) => {
    const contact = booking.contact_id ? related.get(booking.contact_id) : undefined;
    return {
      id: booking.id,
      clientName: client.name,
      timeZone: client.timezone,
      contactName: contact?.name ?? contact?.first_name ?? null,
      phone: contact?.phone ?? null,
      slotText: booking.slot_text,
      confirmed: booking.confirmed,
      notifiedAt: booking.notified_at,
      estimatedValueCents: booking.estimated_value_cents,
      createdAt: booking.created_at,
    };
  });

  return (
    <div className="flex flex-col gap-10">
      <header className="flex flex-col gap-5">
        <Link href="/admin/clients" className="eyebrow hover:opacity-70">
          ← All clients
        </Link>
        <div className="flex flex-wrap items-end justify-between gap-6">
          <div>
            <h1 className="h-display">{client.name}</h1>
            <p className="mt-2 text-sm text-ink-soft">
              {client.contact_name ? `${client.contact_name} · ` : ''}
              {client.contact_email}
              {client.booking_phone && (
                <span className="text-ink-mute"> · desk {formatPhone(client.booking_phone)}</span>
              )}
            </p>
          </div>
          <div className="text-right">
            <p className="font-display text-3xl leading-none text-ink tabular-nums">
              {localTimeInZone(client.timezone)}
            </p>
            <p className="eyebrow mt-1">{client.timezone.replace('_', ' ')}</p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <WindowPill open={windowOpen} />
          <StatusPill value={client.stripe_status} />
          <span className={`badge ${client.active ? 'badge-ok' : 'badge-mute'}`}>
            {client.active ? 'campaign live' : 'campaign paused'}
          </span>
          {!windowOpen && (
            <span className="text-sm text-ink-soft">
              {nextWindowOpenLabel(client.timezone, start, end)}
            </span>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <Link className="btn btn-primary" href={`/admin/clients/${client.id}/upload`}>
            Upload a list
          </Link>
          <form action={client.active ? pauseCampaign : startCampaign}>
            <input type="hidden" name="clientId" value={client.id} />
            <button className={client.active ? 'btn btn-danger' : 'btn btn-ghost'} type="submit">
              {client.active ? 'Pause campaign' : 'Start campaign'}
            </button>
          </form>
          <form action={sendWeeklyReportNowAction}>
            <input type="hidden" name="id" value={client.id} />
            <button className="btn btn-ghost" type="submit">
              Send this week&rsquo;s report now
            </button>
          </form>
        </div>

        {notice && (
          <p role="status" className="card card-pad bg-brass-wash text-sm text-ink">
            {notice}
          </p>
        )}
        {error && (
          <p role="alert" className="card card-pad text-sm text-rose">
            {error}
          </p>
        )}
      </header>

      <section className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <div className="stat">
          <p className="stat-num tabular-nums">{n(contactTotal).toLocaleString('en-US')}</p>
          <p className="stat-label">Contacts on file</p>
        </div>
        <div className="stat">
          <p className="stat-num tabular-nums">{bookedCount.toLocaleString('en-US')}</p>
          <p className="stat-label">Booked · all time</p>
        </div>
        <div className="stat">
          <p className="stat-num tabular-nums text-brass-deep">
            {usd(estimatedRecoveredCents(bookedCount, client.avg_ticket_cents))}
          </p>
          <p className="stat-label">Est. recovered</p>
        </div>
        <div className="stat">
          <p className="stat-num tabular-nums">{usd(client.avg_ticket_cents)}</p>
          <p className="stat-label">Average ticket</p>
        </div>
      </section>

      <section className="card card-pad">
        <h2 className="h-display text-xl">Scrub audit</h2>
        <p className="help mt-1">
          Every contact this client has, by what the gates decided. Anything but{' '}
          <span className="font-mono">pending</span> or <span className="font-mono">calling</span> will
          never be dialed again — one attempt per contact, ever.
        </p>
        <dl className="mt-6 grid grid-cols-3 gap-x-6 gap-y-5 sm:grid-cols-5">
          {audit.map(({ status, count }) => (
            <div key={status}>
              <dd
                className={`font-display text-xl tabular-nums ${count === 0 ? 'text-ink-mute' : 'text-ink'}`}
              >
                {count.toLocaleString('en-US')}
              </dd>
              <dt className="stat-label">{status.replace(/_/g, ' ')}</dt>
            </div>
          ))}
        </dl>
      </section>

      <section className="card card-pad">
        <h2 className="h-display text-xl">Offer &amp; settings</h2>
        <p className="help mt-1 mb-6">
          Saved changes apply to the next dial — calls already in flight keep the old script.
        </p>
        <ClientForm
          mode="edit"
          defaults={{
            id: client.id,
            name: client.name,
            contact_name: client.contact_name,
            contact_email: client.contact_email,
            contact_phone: client.contact_phone,
            booking_phone: client.booking_phone,
            offer_text: client.offer_text,
            timezone: client.timezone,
            vertical: client.vertical,
            avg_ticket_cents: client.avg_ticket_cents,
          }}
        />
      </section>

      <section className="flex flex-col gap-4">
        <div className="flex flex-wrap items-baseline justify-between gap-3">
          <h2 className="h-display text-xl">Contacts</h2>
          <p className="text-sm text-ink-mute tabular-nums">
            {contacts.length === 0
              ? 'none yet'
              : `showing ${contacts.length} newest of ${n(contactTotal).toLocaleString('en-US')}`}
          </p>
        </div>
        <div className="card">
          {contacts.length === 0 ? (
            <p className="card-pad help">
              Nothing uploaded yet — a CSV or XLSX with a phone column and a consent column is all it
              takes.
            </p>
          ) : (
            <div className="overflow-x-auto">
              <table className="table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Campaign</th>
                    <th>Phone</th>
                    <th>Consent</th>
                    <th>Status</th>
                    <th>Last visit</th>
                    <th className="text-right">Lifetime</th>
                    <th className="text-right">Attempts</th>
                  </tr>
                </thead>
                <tbody>
                  {contacts.map((contact) => (
                    <tr key={contact.id}>
                      <td className="whitespace-nowrap">
                        {contact.name ?? contact.first_name ?? '—'}
                        {contact.email && (
                          <span className="block text-xs text-ink-mute">{contact.email}</span>
                        )}
                      </td>
                      <td className="whitespace-nowrap text-ink-mute">{contact.campaign}</td>
                      <td className="whitespace-nowrap tabular-nums text-ink-soft">
                        {contact.phone ? formatPhone(contact.phone) : '—'}
                      </td>
                      <td>
                        <span className={`badge ${contact.consent ? 'badge-ok' : 'badge-bad'}`}>
                          {contact.consent ? 'yes' : 'no'}
                        </span>
                      </td>
                      <td>
                        <StatusPill value={contact.status} />
                        {contact.scrub_reason && (
                          <span className="block text-xs text-ink-mute">{contact.scrub_reason}</span>
                        )}
                      </td>
                      <td className="whitespace-nowrap tabular-nums text-ink-mute">
                        {contact.last_visit ?? '—'}
                      </td>
                      <td className="text-right tabular-nums text-ink-mute">
                        {contact.lifetime_value_cents == null ? '—' : usd(contact.lifetime_value_cents)}
                      </td>
                      <td className="text-right tabular-nums text-ink-mute">{contact.attempts}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </section>

      <section className="flex flex-col gap-4">
        <h2 className="h-display text-xl">Calls</h2>
        <div className="card">
          <CallsTable rows={callRows} showClient={false} />
        </div>
      </section>

      <section className="flex flex-col gap-4">
        <h2 className="h-display text-xl">Bookings</h2>
        <div className="card">
          <BookingsTable rows={bookingRows} showClient={false} />
        </div>
      </section>
    </div>
  );
}
