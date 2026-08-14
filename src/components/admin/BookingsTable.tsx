import { formatPhone } from '@/lib/phone';
import { usd } from '@/lib/money';

export type BookingRowView = {
  id: string;
  clientName: string;
  /** IANA zone of the owning client — timestamps are shown where the booking landed. */
  timeZone: string;
  contactName: string | null;
  phone: string | null;
  slotText: string;
  confirmed: boolean;
  notifiedAt: string | null;
  estimatedValueCents: number | null;
  createdAt: string;
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

export function BookingsTable({
  rows,
  showClient = true,
}: {
  rows: BookingRowView[];
  showClient?: boolean;
}) {
  if (rows.length === 0) {
    return (
      <p className="help">
        No bookings yet — Malone writes one the moment a caller commits to a specific time.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="table">
        <thead>
          <tr>
            <th>Booked</th>
            {showClient && <th>Client</th>}
            <th>Guest</th>
            <th>Slot</th>
            <th>Owner alert</th>
            <th className="text-right">Est. value</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              <td className="whitespace-nowrap tabular-nums text-ink-soft">
                {localWhen(row.createdAt, row.timeZone)}
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
              <td className="max-w-xs text-ink">
                {row.slotText}
                {row.confirmed && <span className="badge badge-ok ml-2">confirmed</span>}
              </td>
              <td className="whitespace-nowrap text-xs">
                {row.notifiedAt ? (
                  <span className="text-ink-mute tabular-nums">
                    sent {localWhen(row.notifiedAt, row.timeZone)}
                  </span>
                ) : (
                  <span className="badge badge-warn">not sent</span>
                )}
              </td>
              <td className="text-right tabular-nums text-brass-deep">
                {row.estimatedValueCents == null ? '—' : usd(row.estimatedValueCents)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
