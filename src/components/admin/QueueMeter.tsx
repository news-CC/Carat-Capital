export function QueueMeter({
  inFlight,
  cap,
  pending,
  windowLabel,
}: {
  inFlight: number;
  cap: number;
  pending: number;
  windowLabel: string;
}) {
  const lines = Array.from({ length: Math.max(cap, 1) }, (_, i) => i < inFlight);
  const atCapacity = inFlight >= cap;
  const overflow = Math.max(0, inFlight - cap);

  return (
    <section className="card card-pad">
      <div className="flex flex-wrap items-baseline justify-between gap-3">
        <div>
          <h2 className="stat-label">Lines in flight</h2>
          <p className="stat-num tabular-nums">
            {inFlight}
            <span className="text-ink-mute"> / {cap}</span>
          </p>
        </div>
        {atCapacity ? (
          <span className="badge badge-warn">at capacity — cron will wait</span>
        ) : (
          <span className="badge badge-mute">{cap - inFlight} free</span>
        )}
      </div>

      <div className="mt-4 flex items-end gap-1.5" aria-hidden="true">
        {lines.map((busy, i) => (
          <span
            key={i}
            className={`h-8 flex-1 rounded-sm ${busy ? 'bg-brass' : 'bg-shell'}`}
          />
        ))}
      </div>

      <p className="mt-4 text-sm text-ink-soft tabular-nums">
        {pending.toLocaleString('en-US')} contact{pending === 1 ? '' : 's'} waiting behind the gates.
        <span className="text-ink-mute"> Call window {windowLabel}, each client&rsquo;s local time.</span>
      </p>
      {overflow > 0 && (
        <p className="error-text mt-2">
          {overflow} call{overflow === 1 ? '' : 's'} above the cap — check for stuck{' '}
          <span className="font-mono">dialing</span> rows.
        </p>
      )}
    </section>
  );
}
