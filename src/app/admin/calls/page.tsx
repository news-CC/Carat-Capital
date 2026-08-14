import Link from 'next/link';
import { requireAdmin } from '@/lib/auth';
import { supabaseAdmin } from '@/lib/supabase/admin';
import type { CallOutcome } from '@/lib/types';
import { CallsTable, type CallRowView } from '@/components/admin/CallsTable';

export const dynamic = 'force-dynamic';

const PAGE_SIZE = 200;

const OUTCOMES: CallOutcome[] = [
  'dialing',
  'answered',
  'booked',
  'declined',
  'no_answer',
  'voicemail',
  'busy',
  'failed',
  'opted_out',
];

export default async function CallsPage({
  searchParams,
}: {
  searchParams: Promise<{ client?: string; outcome?: string }>;
}) {
  await requireAdmin(); // gate
  const { client: clientParam, outcome: outcomeParam } = await searchParams;
  const db = supabaseAdmin();

  const { data: clientRows } = await db.from('clients').select('id, name, timezone').order('name');
  const clients = clientRows ?? [];

  // Narrow both filters against known values so a hand-edited URL can't reach the database.
  const clientId = clients.find((c) => c.id === clientParam)?.id;
  const outcome = OUTCOMES.find((o) => o === outcomeParam);

  let query = db
    .from('calls')
    .select(
      'id, client_id, contact_id, outcome, duration_seconds, cost_usd, transcript_url, recording_url, summary, started_at, created_at',
      { count: 'exact' },
    )
    .order('created_at', { ascending: false })
    .limit(PAGE_SIZE);

  if (clientId) query = query.eq('client_id', clientId);
  if (outcome) query = query.eq('outcome', outcome);

  const { data, count, error } = await query;
  const calls = data ?? [];

  const contactIds = calls.map((c) => c.contact_id).filter((id): id is string => Boolean(id));
  const contactsRes =
    contactIds.length > 0
      ? await db.from('contacts').select('id, name, first_name, phone').in('id', contactIds)
      : null;
  const contacts = new Map((contactsRes?.data ?? []).map((c) => [c.id, c]));
  const clientsById = new Map(clients.map((c) => [c.id, c]));

  const rows: CallRowView[] = calls.map((call) => {
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

  const total = count ?? rows.length;

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="eyebrow">Calls</p>
          <h1 className="h-display">Every attempt, logged</h1>
        </div>
        <p className="text-sm text-ink-mute tabular-nums">
          {total === 0
            ? 'no calls match'
            : `showing ${rows.length.toLocaleString('en-US')} of ${total.toLocaleString('en-US')}`}
        </p>
      </header>

      <form method="get" className="card card-pad flex flex-wrap items-end gap-5">
        <div className="field">
          <label className="label" htmlFor="filter-client">
            Client
          </label>
          <select id="filter-client" name="client" className="select" defaultValue={clientId ?? ''}>
            <option value="">All clients</option>
            {clients.map((client) => (
              <option key={client.id} value={client.id}>
                {client.name}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label className="label" htmlFor="filter-outcome">
            Outcome
          </label>
          <select id="filter-outcome" name="outcome" className="select" defaultValue={outcome ?? ''}>
            <option value="">Any outcome</option>
            {OUTCOMES.map((value) => (
              <option key={value} value={value}>
                {value.replace(/_/g, ' ')}
              </option>
            ))}
          </select>
        </div>
        <button className="btn btn-primary" type="submit">
          Filter
        </button>
        {(clientId || outcome) && (
          <Link className="btn btn-ghost" href="/admin/calls">
            Clear
          </Link>
        )}
      </form>

      {error && <p className="error-text">Could not load calls: {error.message}</p>}

      <div className="card">
        <CallsTable rows={rows} />
      </div>

      <p className="help">
        Times are shown in the client&rsquo;s own timezone. Cost is what Vapi billed for the call.
      </p>
    </div>
  );
}
