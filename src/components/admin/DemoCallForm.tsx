'use client';

import { useActionState } from 'react';
import { useFormStatus } from 'react-dom';

import { placeDemoCall } from '@/app/admin/demo/actions';
import type { DemoState } from '@/lib/demo';

/**
 * Eastern first and labelled as the default: the whole prospect list is NYC-metro, so anything
 * else is the exception. The bare IANA id ("New York") does not read as a timezone at a glance,
 * which is how an operator ends up demoing against the wrong calling window.
 */
const TIMEZONES: [string, string][] = [
  ['America/New_York', 'New York — Eastern (default)'],
  ['America/Chicago', 'Chicago — Central'],
  ['America/Denver', 'Denver — Mountain'],
  ['America/Phoenix', 'Phoenix — Arizona, no DST'],
  ['America/Los_Angeles', 'Los Angeles — Pacific'],
  ['America/Anchorage', 'Anchorage — Alaska'],
  ['Pacific/Honolulu', 'Honolulu — Hawaii'],
  ['America/Toronto', 'Toronto — Eastern'],
  ['America/Vancouver', 'Vancouver — Pacific'],
];

const PRESETS = [
  {
    label: 'Standard win-back',
    offer: '20% off your next cut and colour, any day this week',
    instructions: '',
  },
  {
    label: 'Med spa recall',
    offer: 'a complimentary skin consult with any treatment booked this month',
    instructions:
      'This is a med spa. Do not give medical advice or discuss results. If they ask anything clinical, say the provider will cover it at the consult.',
  },
  {
    label: 'Quiet-Tuesday filler',
    offer: '30% off any Tuesday or Wednesday appointment',
    instructions:
      'Only offer Tuesday and Wednesday times. If they push for a weekend, say those are booked and offer the midweek slots again once.',
  },
  {
    label: 'Code hand-out',
    offer: 'a free deep-conditioning treatment on your next visit',
    instructions: 'Make sure they write the code down before you end the call.',
    promo: 'MALONE20',
  },
] as const;

function Submit() {
  const { pending } = useFormStatus();
  return (
    <button className="btn btn-primary" type="submit" disabled={pending}>
      {pending ? 'Dialling…' : 'Call now'}
    </button>
  );
}

function FieldError({ errors, name }: { errors: Record<string, string> | undefined; name: string }) {
  const message = errors?.[name];
  if (!message) return null;
  return (
    <p className="error-text" id={`${name}-error`}>
      {message}
    </p>
  );
}

export default function DemoCallForm({ defaultTimezone }: { defaultTimezone: string }) {
  const [state, action] = useActionState<DemoState, FormData>(placeDemoCall, { status: 'idle' });
  const errors = state.status === 'error' ? state.fieldErrors : undefined;

  function applyPreset(preset: (typeof PRESETS)[number]) {
    const form = document.getElementById('demo-form') as HTMLFormElement | null;
    if (!form) return;
    (form.elements.namedItem('offer_text') as HTMLTextAreaElement).value = preset.offer;
    (form.elements.namedItem('instructions') as HTMLTextAreaElement).value = preset.instructions;
    (form.elements.namedItem('promo_code') as HTMLInputElement).value =
      'promo' in preset ? preset.promo : '';
  }

  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_20rem]">
      <form id="demo-form" action={action} className="card card-pad">
        <div className="grid gap-5 sm:grid-cols-2">
          <div className="field">
            <label className="label" htmlFor="phone">
              Number to call
            </label>
            <input
              className="input"
              id="phone"
              name="phone"
              type="tel"
              required
              autoComplete="off"
              placeholder="(510) 375-5890"
              aria-describedby={errors?.phone ? 'phone-error' : undefined}
            />
            <FieldError errors={errors} name="phone" />
            <p className="help">Theirs, not their clients&apos;. Malone rings this in a few seconds.</p>
          </div>

          <div className="field">
            <label className="label" htmlFor="first_name">
              Their first name <span className="text-ink-mute">(optional)</span>
            </label>
            <input className="input" id="first_name" name="first_name" autoComplete="off" placeholder="Dana" />
            <p className="help">Left blank, Malone opens with &ldquo;Hey there&rdquo;.</p>
          </div>

          <div className="field sm:col-span-2">
            <label className="label" htmlFor="salon_name">
              Salon name Malone says it is calling for
            </label>
            <input
              className="input"
              id="salon_name"
              name="salon_name"
              required
              placeholder="Butterfly Studio Salon"
              aria-describedby={errors?.salon_name ? 'salon_name-error' : undefined}
            />
            <FieldError errors={errors} name="salon_name" />
          </div>

          <div className="field sm:col-span-2">
            <label className="label" htmlFor="offer_text">
              The offer
            </label>
            <textarea
              className="textarea"
              id="offer_text"
              name="offer_text"
              rows={2}
              required
              placeholder="20% off your next cut and colour, any day this week"
              aria-describedby={errors?.offer_text ? 'offer_text-error' : undefined}
            />
            <FieldError errors={errors} name="offer_text" />
            <p className="help">Said aloud, so write it the way you would say it.</p>
          </div>

          <div className="field sm:col-span-2">
            <label className="label" htmlFor="instructions">
              How should this conversation run? <span className="text-ink-mute">(optional)</span>
            </label>
            <textarea
              className="textarea"
              id="instructions"
              name="instructions"
              rows={5}
              placeholder={
                'Only offer Tuesday and Wednesday slots.\nMention the new colourist by name.\nIf they mention the old pricing, say it has not changed.'
              }
              aria-describedby={errors?.instructions ? 'instructions-error' : undefined}
            />
            <FieldError errors={errors} name="instructions" />
            <p className="help">
              Added on top of Malone&apos;s script, not instead of it. It always says it is a virtual
              assistant, always takes the first no, always stops when asked, always under three minutes
              — nothing typed here changes that.
            </p>
          </div>

          <div className="field">
            <label className="label" htmlFor="promo_code">
              Code to give out <span className="text-ink-mute">(optional)</span>
            </label>
            <input
              className="input"
              id="promo_code"
              name="promo_code"
              autoComplete="off"
              placeholder="MALONE20"
              aria-describedby={errors?.promo_code ? 'promo_code-error' : undefined}
            />
            <FieldError errors={errors} name="promo_code" />
            <p className="help">Given once, after they agree to a time, spelled out slowly.</p>
          </div>

          <div className="field">
            <label className="label" htmlFor="booking_phone">
              Front desk number <span className="text-ink-mute">(optional)</span>
            </label>
            <input className="input" id="booking_phone" name="booking_phone" type="tel" placeholder="(201) 555-0143" />
            <p className="help">Read out on voicemail.</p>
          </div>

          <div className="field sm:col-span-2">
            <label className="label" htmlFor="timezone">
              Their timezone
            </label>
            <select className="select" id="timezone" name="timezone" defaultValue={defaultTimezone}>
              {TIMEZONES.map(([zone, label]) => (
                <option key={zone} value={zone}>
                  {label}
                </option>
              ))}
            </select>
            <p className="help">
              Used for the calling-hours check. Leave it on Eastern for anyone in the NYC metro.
            </p>
          </div>
        </div>

        <div className="rule my-6" />

        <label className="flex items-start gap-3 text-sm" htmlFor="consent_attested">
          <input
            className="mt-0.5"
            id="consent_attested"
            name="consent_attested"
            type="checkbox"
            required
            aria-describedby={errors?.consent_attested ? 'consent_attested-error' : undefined}
          />
          <span>
            <span className="text-ink">This person asked me to call them.</span>
            <span className="help mt-1 block">
              Recorded against the call. A demo is a call to someone expecting it — not a cold dial.
            </span>
          </span>
        </label>
        <FieldError errors={errors} name="consent_attested" />

        <label className="mt-4 flex items-start gap-3 text-sm" htmlFor="window_override">
          <input className="mt-0.5" id="window_override" name="window_override" type="checkbox" />
          <span>
            <span className="text-ink">Call outside 9am–7pm their time.</span>
            <span className="help mt-1 block">
              Only needed off-hours, and only because they asked you to call now. Logged on the contact.
            </span>
          </span>
        </label>
        <FieldError errors={errors} name="window_override" />

        <div className="mt-7 flex flex-wrap items-center gap-3">
          <Submit />
          {state.status === 'error' && <p className="error-text">{state.error}</p>}
        </div>

        {state.status === 'success' && (
          <div className="card card-pad mt-6 bg-brass-wash">
            <p className="eyebrow">Dialling now</p>
            <p className="mt-2 text-lg">
              Malone is calling <span className="font-display">{state.phone}</span> as {state.salonName}.
            </p>
            {state.promoCode && (
              <p className="help mt-2">
                It will hand out <span className="text-ink">{state.promoCode}</span> once a time is agreed.
              </p>
            )}
            {state.outsideWindow && (
              <p className="help mt-2">Placed outside normal calling hours using the override.</p>
            )}
            <p className="help mt-3">
              The transcript, outcome and any booking land in{' '}
              <a className="underline" href="/admin/calls">
                Calls
              </a>{' '}
              when the call ends — same handling as a live campaign.
            </p>
          </div>
        )}
      </form>

      <aside className="grid content-start gap-4">
        <div className="card card-pad">
          <p className="eyebrow">Start from</p>
          <div className="mt-3 grid gap-2">
            {PRESETS.map((preset) => (
              <button
                key={preset.label}
                type="button"
                className="btn btn-ghost btn-sm justify-start"
                onClick={() => applyPreset(preset)}
              >
                {preset.label}
              </button>
            ))}
          </div>
          <p className="help mt-3">Fills the offer, notes and code. Edit before calling.</p>
        </div>

        <div className="card card-pad">
          <p className="eyebrow">What still holds</p>
          <ul className="help mt-3 grid gap-2">
            <li>Suppressed numbers are refused, override or not.</li>
            <li>Malone discloses it is a virtual assistant.</li>
            <li>&ldquo;Stop calling&rdquo; suppresses them globally, mid-call.</li>
            <li>Three minutes maximum.</li>
            <li>A booking emails the salon immediately.</li>
          </ul>
        </div>
      </aside>
    </div>
  );
}
