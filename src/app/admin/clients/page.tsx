import Link from 'next/link';
import { requireAdmin } from '@/lib/auth';
import { isInsideCallWindow, localTimeInZone } from '@/lib/call-window';
import { callWindow } from '@/lib/env';
import { usd } from '@/lib/money';
import { estimatedRecoveredCents } from '@/lib/revenue';
import { supabaseAdmin } from '@/lib/supabase/admin';
import { ClientForm } from '@/components/admin/ClientForm';
import { StatusPill, WindowPill } from '@/components/admin/StatusPill';

export const dynamic = 'force-dynamic';

const n = (r: { count: number | null }): number => r.count ?? 0;

export default async function ClientsPage({
  searchParams,
}: {
  searchParams: Promise<{ notice?: string; error?: string }>;
}) {
  await requireAdmin(); // gate
  const { notice, error: flash } = await searchParams;
  const db = supabaseAdmin();
  const { start, end } = callWindow();

  const { data, error } = await db
    .from('clients')
    .select('id, name, vertical, timezone, stripe_status, active, avg_ticket_cents, contact_email')
    .order('active', { ascending: false })
    .order('name', { ascending: true });

  const clients = data ?? [];
  const counts = await Promise.all(
    clients.flatMap((client) => [
      db
        .from('contacts')
        .select('*', { count: 'exact', head: true })
        .eq('client_id', client.id)
        .eq('status', 'pending'),
      db.from('bookings').select('*', { count: 'exact', head: true }).eq('client_id', client.id),
    ]),
  );

  return (
    <div className="flex flex-col gap-10">
      <header>
        <p className="eyebrow">Clients</p>
        <h1 className="h-display">Who we call for</h1>
        <p className="prose-tight mt-2 max-w-prose text-ink-soft">
          Each row is a paying salon. The offer text and timezone here are the two settings that change
          what Malone says and when he is allowed to say it.
        </p>
      </header>

      {notice && (
        <p role="status" className="card card-pad bg-brass-wash text-sm text-ink">
          {notice}
        </p>
      )}
      {flash && (
        <p role="alert" className="card card-pad text-sm text-rose">
          {flash}
        </p>
      )}
      {error && <p className="error-text">Could not load clients: {error.message}</p>}

      <section className="card">
        {clients.length === 0 ? (
          <p className="card-pad help">
            No clients yet — fill in the form below and you can upload a list a minute later.
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Client</th>
                  <th>Local time</th>
                  <th>Billing</th>
                  <th className="text-right">Queued</th>
                  <th className="text-right">Booked</th>
                  <th className="text-right">Est. recovered</th>
                  <th className="text-right">Avg ticket</th>
                </tr>
              </thead>
              <tbody>
                {clients.map((client, i) => {
                  const pending = n(counts[i * 2]);
                  const booked = n(counts[i * 2 + 1]);
                  return (
                    <tr key={client.id}>
                      <td>
                        <Link
                          href={`/admin/clients/${client.id}`}
                          className="text-ink underline decoration-line underline-offset-2"
                        >
                          {client.name}
                        </Link>
                        <span className="block text-xs text-ink-mute">
                          {client.vertical} · {client.contact_email}
                        </span>
                      </td>
                      <td className="whitespace-nowrap">
                        <span className="tabular-nums text-ink">
                          {localTimeInZone(client.timezone)}
                        </span>
                        <span className="mt-1 block">
                          <WindowPill open={isInsideCallWindow(client.timezone, start, end)} />
                        </span>
                      </td>
                      <td className="whitespace-nowrap">
                        <StatusPill value={client.stripe_status} />
                        {!client.active && <span className="badge badge-mute ml-1">paused</span>}
                      </td>
                      <td className="text-right tabular-nums">{pending.toLocaleString('en-US')}</td>
                      <td className="text-right tabular-nums">{booked.toLocaleString('en-US')}</td>
                      <td className="text-right tabular-nums text-brass-deep">
                        {usd(estimatedRecoveredCents(booked, client.avg_ticket_cents))}
                      </td>
                      <td className="text-right tabular-nums text-ink-mute">
                        {usd(client.avg_ticket_cents)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="card card-pad">
        <h2 className="h-display text-xl">Add a client</h2>
        <p className="help mt-1 mb-6">
          Nothing dials until you upload a list, so it is safe to create the record now and tune the offer
          later.
        </p>
        <ClientForm mode="create" />
      </section>
    </div>
  );
}
