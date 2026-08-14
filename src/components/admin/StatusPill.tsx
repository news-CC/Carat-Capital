type Tone = 'ok' | 'warn' | 'bad' | 'mute';

// Contact statuses and call outcomes share one visual vocabulary: green = money or a
// live human, amber = in motion, red = a door closed on us, grey = nothing happened yet.
const TONES: Record<string, Tone> = {
  // contacts.status
  pending: 'mute',
  calling: 'warn',
  called: 'mute',
  booked: 'ok',
  declined: 'bad',
  opted_out: 'bad',
  suppressed: 'bad',
  invalid: 'bad',
  no_answer: 'mute',
  failed: 'bad',
  // calls.outcome
  dialing: 'warn',
  answered: 'ok',
  voicemail: 'mute',
  busy: 'mute',
  // clients.stripe_status
  trialing: 'warn',
  active: 'ok',
  past_due: 'bad',
  canceled: 'bad',
  // suppression.reason
  opt_out: 'bad',
  dnc: 'bad',
  complaint: 'bad',
  manual: 'mute',
};

const LABELS: Record<string, string> = {
  no_answer: 'no answer',
  opted_out: 'opted out',
  opt_out: 'opt-out',
  past_due: 'past due',
  dnc: 'DNC',
};

export function StatusPill({ value }: { value: string }) {
  const tone = TONES[value] ?? 'mute';
  return <span className={`badge badge-${tone}`}>{LABELS[value] ?? value.replace(/_/g, ' ')}</span>;
}

export function WindowPill({ open }: { open: boolean }) {
  return (
    <span className={`badge ${open ? 'badge-ok' : 'badge-mute'}`}>
      {open ? 'window open' : 'window closed'}
    </span>
  );
}
