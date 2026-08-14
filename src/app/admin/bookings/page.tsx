import Link from 'next/link';
import { requireAdmin } from '@/lib/auth';
import { usd } from '@/lib/money';
import { supabaseAdmin } from '@/lib/supabase/admin';
import { BookingsTable, type BookingRowView } from '@/components/admin/BookingsTable';

export const dynamic = 'force-dynamic';

const PAGE_SIZE = 200;
/** PostgREST's own response cap, so a full page means "there is probably more". */
const VALUE_PAGE = 1_000;
const VALUE_SCAN_CAP = 100_000;

const n = (r: { count: number | null }): number => r.count ?? 0;

type Db = ReturnType<typeof supabaseAdmin>;

export default async function BookingsPage({
  searchParams,
}: {
  searchParams: Promise<{ client?: string }>;
}) {
  await requireAdmin(); // gate
  const { client: clientParam } = await searchParams;
  const db = supabaseAdmin();
  const since = new Date(Date.now() - 7 * 86_400_000).toISOString();

  const { data: clientRows } = await db.from('clients').select('id, name, timezone').order('name');
  const clients = clientRows ?? [];
  const clientId = clients.find((c) => c.id === clientParam)?.id;

  let query = db
    .from('bookings')
    .select('id, client_id, contact_id, slot_text, confirmed, notified_at, estimated_value_cents, created_at', {
      count: 'exact',
    })
    .order('created_at', { ascending: false })
    .limit(PAGE_SIZE);
  if (clientId) query = query.eq('client_id', clientId);

  const [bookingsRes, confirmedRes, weekValue] = await Promise.all([
    query,
    db.from('bookings').select('*', { count: 'exact', head: true }).eq('confirmed', true),
    weekValueCents(db, since),
  ]);

  const bookings = bookingsRes.data ?? [];

  const contactIds = bookings.map((b) => b.contact_id).filter((id): id is string => Boolean(id));
  const contactsRes =
    contactIds.length > 0
      ? await db.from('contacts').select('id, name, first_name, phone').in('id', contactIds)
      : null;
  const contacts = new Map((contactsRes?.data ?? []).map((c) => [c.id, c]));
  const clientsById = new Map(clients.map((c) => [c.id, c]));

  const rows: BookingRowView[] = bookings.map((booking) => {
    const client = booking.client_id ? clientsById.get(booking.client_id) : undefined;
    const contact = booking.contact_id ? contacts.get(booking.contact_id) : undefined;
    return {
      id: booking.id,
      clientName: client?.name ?? '—',
      timeZone: client?.timezone ?? 'UTC',
      contactName: contact?.name ?? contact?.first_name ?? null,
      phone: contact?.phone ?? null,
      slotText: booking.slot_text,
      confirmed: booking.confirmed,
      notifiedAt: booking.notified_at,
      estimatedValueCents: booking.estimated_value_cents,
      createdAt: booking.created_at,
    };
  });

  const total = bookingsRes.count ?? rows.length;

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="eyebrow">Bookings</p>
          <h1 className="h-display">Chairs filled</h1>
        </div>
        <p className="text-sm text-ink-mute tabular-nums">
          {total === 0
            ? 'no bookings match'
            : `showing ${rows.length.toLocaleString('en-US')} of ${total.toLocaleString('en-US')}`}
        </p>
      </header>

      <section className="grid grid-cols-2 gap-4 md:grid-cols-3">
        <div className="stat">
          <p className="stat-num tabular-nums">{total.toLocaleString('en-US')}</p>
          <p className="stat-label">{clientId ? 'Bookings · this client' : 'Bookings · all time'}</p>
        </div>
        <div className="stat">
          <p className="stat-num tabular-nums">{n(confirmedRes).toLocaleString('en-US')}</p>
          <p className="stat-label">Confirmed by the salon</p>
        </div>
        <div className="stat">
          <p className="stat-num tabular-nums text-brass-deep">
            {weekValue.cents === null ? '—' : usd(weekValue.cents)}
          </p>
          <p className="stat-label">Est. value · 7d, all clients</p>
        </div>
      </section>

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
        <button className="btn btn-primary" type="submit">
          Filter
        </button>
        {clientId && (
          <Link className="btn btn-ghost" href="/admin/bookings">
            Clear
          </Link>
        )}
      </form>

      {bookingsRes.error && (
        <p className="error-text">Could not load bookings: {bookingsRes.error.message}</p>
      )}

      {weekValue.error && (
        <p className="error-text">Could not total this week&rsquo;s value: {weekValue.error}</p>
      )}

      <div className="card">
        <BookingsTable rows={rows} />
      </div>

      <p className="help">
        The owner alert goes out the moment the webhook lands. A missing alert means the Resend call
        failed — check the logs before the salon notices.
      </p>
    </div>
  );
}

/**
 * The week's booked value, summed page by page. One plain select would be capped at 1000 rows by
 * PostgREST, so the tile would quietly stop growing while the count tiles beside it kept rising.
 * Ascending created_at is what makes the paging safe: a booking written mid-scan lands on the last
 * page, never shifting a page already read into counting a row twice.
 */
async function weekValueCents(
  db: Db,
  since: string,
): Promise<{ cents: number | null; error: string | null }> {
  let cents = 0;
  for (let from = 0; from < VALUE_SCAN_CAP; from += VALUE_PAGE) {
    const { data, error } = await db
      .from('bookings')
      .select('estimated_value_cents')
      .gte('created_at', since)
      .order('created_at', { ascending: true })
      .order('id', { ascending: true })
      .range(from, from + VALUE_PAGE - 1);
    // A partial sum shown as a dollar figure is a wrong number, so the tile shows nothing instead.
    if (error) return { cents: null, error: error.message };

    const rows = data ?? [];
    for (const row of rows) cents += row.estimated_value_cents ?? 0;
    if (rows.length < VALUE_PAGE) return { cents, error: null };
  }

  // Out of scan budget, so the real total is higher than what we summed — and a money tile that
  // reads low is worse than one that reads nothing.
  return {
    cents: null,
    error: `over ${VALUE_SCAN_CAP.toLocaleString('en-US')} bookings in the window — total not shown`,
  };
}
