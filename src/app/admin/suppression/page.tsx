import Link from 'next/link';
import { requireAdmin } from '@/lib/auth';
import { formatPhone } from '@/lib/phone';
import { supabaseAdmin } from '@/lib/supabase/admin';
import { StatusPill } from '@/components/admin/StatusPill';
import { addSuppressionAction, removeSuppressionAction } from '@/app/admin/suppression/actions';

export const dynamic = 'force-dynamic';

const PAGE_SIZE = 200;

const REASON_OPTIONS: [string, string][] = [
  ['opt_out', 'Opt-out — asked us to stop'],
  ['dnc', 'DNC — registry or legal request'],
  ['complaint', 'Complaint'],
  ['invalid', 'Invalid number'],
  ['manual', 'Manual — operator judgement'],
];

const ERRORS: Record<string, string> = {
  phone: 'That is not a dialable number, so nothing was added. Suppression matches on E.164 exactly.',
  save: 'Could not write to the suppression list. Try again, then check the logs.',
};

function when(iso: string): string {
  return new Date(iso).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    timeZone: 'UTC',
  });
}

export default async function SuppressionPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; error?: string }>;
}) {
  await requireAdmin(); // gate
  const { q, error: errorKey } = await searchParams;
  const db = supabaseAdmin();

  const search = (q ?? '').trim();
  const digits = search.replace(/\D/g, '');

  let query = db
    .from('suppression')
    .select('id, phone, reason, created_at', { count: 'exact' })
    .order('created_at', { ascending: false })
    .limit(PAGE_SIZE);

  if (digits.length >= 3) query = query.ilike('phone', `%${digits}%`);
  else if (search) query = query.ilike('reason', `%${search}%`);

  const { data, count, error } = await query;
  const rows = data ?? [];
  const total = count ?? rows.length;

  return (
    <div className="flex flex-col gap-8">
      <header className="max-w-prose">
        <p className="eyebrow">Suppression</p>
        <h1 className="h-display">The do-not-call list</h1>
        <p className="prose-tight mt-2 text-ink-soft">
          One global list across every client. A number here is checked twice before any dial — once in
          the claim query, once in application code — so adding a number takes effect on the next
          five-minute cron with no other action needed.
        </p>
      </header>

      <section className="card card-pad">
        <h2 className="h-display text-xl">Add a number</h2>
        <form action={addSuppressionAction} className="mt-5 flex flex-wrap items-end gap-5">
          <div className="field">
            <label className="label" htmlFor="sup-phone">
              Phone
            </label>
            <input
              id="sup-phone"
              className="input tabular-nums"
              name="phone"
              type="tel"
              required
              placeholder="(415) 555-0142"
            />
          </div>
          <div className="field">
            <label className="label" htmlFor="sup-reason">
              Reason
            </label>
            <select id="sup-reason" className="select" name="reason" defaultValue="manual">
              {REASON_OPTIONS.map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </div>
          <button className="btn btn-primary" type="submit">
            Suppress
          </button>
        </form>
        {errorKey && ERRORS[errorKey] && <p className="error-text mt-4">{ERRORS[errorKey]}</p>}
        <p className="help mt-4">
          Any queued contact on this number is marked suppressed at the same moment. Calls already
          connected are not cut off.
        </p>
      </section>

      <section className="flex flex-col gap-4">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <form method="get" className="flex flex-wrap items-end gap-3">
            <div className="field">
              <label className="label" htmlFor="sup-q">
                Search
              </label>
              <input
                id="sup-q"
                className="input"
                name="q"
                defaultValue={search}
                placeholder="415 555 or complaint"
              />
            </div>
            <button className="btn btn-ghost" type="submit">
              Search
            </button>
            {search && (
              <Link className="btn btn-ghost btn-sm" href="/admin/suppression">
                Clear
              </Link>
            )}
          </form>
          <p className="text-sm text-ink-mute tabular-nums">
            {total.toLocaleString('en-US')} number{total === 1 ? '' : 's'} suppressed
            {search ? ' matching' : ''}
          </p>
        </div>

        {error && <p className="error-text">Could not load the list: {error.message}</p>}

        <div className="card">
          {rows.length === 0 ? (
            <p className="card-pad help">
              {search
                ? 'No match — the number is not suppressed, so it is still dialable.'
                : 'Empty list. Opt-outs land here automatically the moment a caller asks to be removed.'}
            </p>
          ) : (
            <div className="overflow-x-auto py-4">
              <table className="table">
                <thead>
                  <tr>
                    <th>Phone</th>
                    <th>Reason</th>
                    <th>Added</th>
                    <th className="text-right">Remove</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row) => (
                    <tr key={row.id}>
                      <td className="whitespace-nowrap tabular-nums text-ink">
                        {formatPhone(row.phone)}
                        <span className="ml-2 text-xs text-ink-mute">{row.phone}</span>
                      </td>
                      <td>
                        <StatusPill value={row.reason} />
                      </td>
                      <td className="whitespace-nowrap tabular-nums text-ink-mute">
                        {when(row.created_at)}
                      </td>
                      <td className="text-right">
                        <form action={removeSuppressionAction}>
                          <input type="hidden" name="id" value={row.id} />
                          <button className="btn btn-danger btn-sm" type="submit">
                            Remove
                          </button>
                        </form>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
        <p className="help">
          Removing a number makes it dialable again. Only do it for a typo — never because a client asked
          you to call someone back.
        </p>
      </section>
    </div>
  );
}
