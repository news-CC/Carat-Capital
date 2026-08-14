import Link from 'next/link';
import { usd } from '@/lib/money';
import { StatusPill, WindowPill } from '@/components/admin/StatusPill';

export type ClientCardData = {
  id: string;
  name: string;
  vertical: string;
  timezone: string;
  stripeStatus: string;
  active: boolean;
  localTime: string;
  windowOpen: boolean;
  /** From nextWindowOpenLabel() — rendered verbatim, only when the window is shut. */
  windowHint: string;
  pending: number;
  booked7d: number;
  recovered7dCents: number;
};

export function ClientCard({ client }: { client: ClientCardData }) {
  return (
    <article className="card card-pad flex flex-col gap-4">
      <div className="flex items-start justify-between gap-4">
        <div>
          <Link
            href={`/admin/clients/${client.id}`}
            className="font-display text-xl leading-tight text-ink transition-opacity duration-150 hover:opacity-70"
          >
            {client.name}
          </Link>
          <p className="mt-1 text-xs text-ink-mute">
            {client.vertical} · {client.timezone.replace('_', ' ')}
          </p>
        </div>
        <div className="text-right">
          <p className="font-display text-2xl leading-none text-ink tabular-nums">{client.localTime}</p>
          <p className="eyebrow mt-1">local time</p>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <WindowPill open={client.windowOpen} />
        <StatusPill value={client.stripeStatus} />
        {!client.active && <span className="badge badge-mute">paused</span>}
      </div>

      {!client.windowOpen && <p className="text-sm text-ink-soft">{client.windowHint}</p>}

      <div className="rule" />

      <dl className="grid grid-cols-3 gap-4">
        <div>
          <dd className="font-display text-lg text-ink tabular-nums">
            {client.pending.toLocaleString('en-US')}
          </dd>
          <dt className="stat-label">queued</dt>
        </div>
        <div>
          <dd className="font-display text-lg text-ink tabular-nums">{client.booked7d}</dd>
          <dt className="stat-label">booked 7d</dt>
        </div>
        <div>
          <dd className="font-display text-lg text-brass-deep tabular-nums">
            {usd(client.recovered7dCents)}
          </dd>
          <dt className="stat-label">recovered 7d</dt>
        </div>
      </dl>
    </article>
  );
}
