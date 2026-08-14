import { formatPhone } from '@/lib/phone';
import { usdExact } from '@/lib/money';
import { StatusPill } from '@/components/admin/StatusPill';

export type CallRowView = {
  id: string;
  clientName: string;
  /** IANA zone of the owning client — timestamps are shown where the call happened. */
  timeZone: string;
  contactName: string | null;
  phone: string | null;
  outcome: string;
  durationSeconds: number | null;
  /** numeric(10,4) arrives as a JSON number, but tolerate a string from PostgREST. */
  costUsd: number | string | null;
  transcriptUrl: string | null;
  recordingUrl: string | null;
  summary: string | null;
  at: string | null;
};

function localWhen(iso: string | null, timeZone: string): string {
  if (!iso) return '—';
  const opts: Intl.DateTimeFormatOptions = {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  };
  try {
    return new Date(iso).toLocaleString('en-US', { ...opts, timeZone });
  } catch {
    // Junk timezone on the client row — fall back rather than crash the page.
    return new Date(iso).toLocaleString('en-US', { ...opts, timeZone: 'UTC' });
  }
}

function duration(seconds: number | null): string {
  if (seconds == null) return '—';
  const m = Math.floor(seconds / 60);
  return `${m}:${String(seconds % 60).padStart(2, '0')}`;
}

function cost(value: number | string | null): string {
  if (value == null) return '—';
  const dollars = Number(value);
  return Number.isFinite(dollars) ? usdExact(Math.round(dollars * 100)) : '—';
}

export function CallsTable({
  rows,
  showClient = true,
}: {
  rows: CallRowView[];
  showClient?: boolean;
}) {
  if (rows.length === 0) {
    return (
      <p className="help">
        No calls yet — the cron dials only inside the call window, so an empty table before 9am local is
        normal.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="table">
        <thead>
          <tr>
            <th>When</th>
            {showClient && <th>Client</th>}
            <th>Contact</th>
            <th>Outcome</th>
            <th className="text-right">Length</th>
            <th className="text-right">Cost</th>
            <th>Notes</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              <td className="whitespace-nowrap tabular-nums text-ink-soft">
                {localWhen(row.at, row.timeZone)}
              </td>
              {showClient && <td className="whitespace-nowrap">{row.clientName}</td>}
              <td className="whitespace-nowrap">
                <span className="text-ink">{row.contactName ?? 'Unknown'}</span>
                {row.phone && (
                  <span className="block text-xs text-ink-mute tabular-nums">
                    {formatPhone(row.phone)}
                  </span>
                )}
              </td>
              <td>
                <StatusPill value={row.outcome} />
              </td>
              <td className="text-right tabular-nums text-ink-soft">{duration(row.durationSeconds)}</td>
              <td className="text-right tabular-nums text-ink-mute">{cost(row.costUsd)}</td>
              <td className="max-w-sm">
                {row.summary && <span className="text-sm text-ink-soft">{row.summary}</span>}
                <span className="mt-0.5 flex gap-3 text-xs">
                  {row.transcriptUrl && (
                    <a
                      className="text-brass-deep underline decoration-line underline-offset-2"
                      href={row.transcriptUrl}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Transcript
                    </a>
                  )}
                  {row.recordingUrl && (
                    <a
                      className="text-brass-deep underline decoration-line underline-offset-2"
                      href={row.recordingUrl}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Recording
                    </a>
                  )}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
