'use client';

import { useActionState, useState } from 'react';
import { useFormStatus } from 'react-dom';

import { placeDemoCall } from '@/app/admin/demo/actions';
import type { DemoState } from '@/lib/demo';

/**
 * Built for one situation: standing inside a salon, on a phone, with the owner watching.
 *
 * Everything follows from that. Single column so it never needs a zoom or a sideways scroll. The
 * three fields that must be typed are first and always visible; everything else is behind one
 * "More" toggle. Presets fill the slow fields in a tap. The submit button is sticky, because on a
 * phone the natural thing to do after typing an offer is reach for the button, not hunt for it.
 */

const TIMEZONES: [string, string][] = [
  ['America/New_York', 'Eastern (default)'],
  ['America/Chicago', 'Central'],
  ['America/Denver', 'Mountain'],
  ['America/Phoenix', 'Arizona'],
  ['America/Los_Angeles', 'Pacific'],
  ['America/Anchorage', 'Alaska'],
  ['Pacific/Honolulu', 'Hawaii'],
];

type Preset = { label: string; offer: string; instructions: string; promo?: string };

/** Written for what a salon owner actually says when handed the phone. */
const PRESETS: Preset[] = [
  {
    label: 'Cut & colour',
    offer: '20% off your next cut and colour, any day this week',
    instructions: '',
  },
  {
    label: 'Quiet midweek',
    offer: '30% off any Tuesday or Wednesday appointment',
    instructions:
      'Only offer Tuesday and Wednesday times. If they push for a weekend, say those are booked and offer the midweek slots again once.',
  },
  {
    label: 'Med spa recall',
    offer: 'a complimentary skin consult with any treatment booked this month',
    instructions:
      'This is a med spa. Do not give medical advice or discuss results. Anything clinical: say the provider covers it at the consult.',
  },
  {
    label: 'Barbershop',
    offer: 'a free hot-towel finish with any cut this month',
    instructions: 'Keep it brief and easy. No colour talk.',
  },
  {
    label: 'With a code',
    offer: 'a free deep-conditioning treatment on your next visit',
    instructions: 'Make sure they have the code written down before you end the call.',
    promo: 'MALONE20',
  },
];

function Submit() {
  const { pending } = useFormStatus();
  return (
    <button className="btn btn-primary w-full text-base sm:w-auto" type="submit" disabled={pending}>
      {pending ? 'Dialling…' : 'Call now'}
    </button>
  );
}

function FieldError({ errors, name }: { errors?: Record<string, string>; name: string }) {
  const message = errors?.[name];
  if (!message) return null;
  return (
    <p className="error-text" id={`${name}-error`}>
      {message}
    </p>
  );
}

export default function DemoCallForm({
  defaultTimezone,
  voices,
  defaultVoice,
}: {
  defaultTimezone: string;
  voices: readonly { id: string; label: string; hint: string }[];
  defaultVoice: string;
}) {
  const [state, action] = useActionState<DemoState, FormData>(placeDemoCall, { status: 'idle' });
  const [showMore, setShowMore] = useState(false);
  const errors = state.status === 'error' ? state.fieldErrors : undefined;

  // Controlled, so a preset tap visibly fills them rather than silently poking the DOM.
  const [offer, setOffer] = useState('');
  const [instructions, setInstructions] = useState('');
  const [promo, setPromo] = useState('');

  function applyPreset(p: Preset) {
    setOffer(p.offer);
    setInstructions(p.instructions);
    setPromo(p.promo ?? '');
    if (p.promo || p.instructions) setShowMore(true);
  }

  return (
    <form action={action} className="mx-auto w-full max-w-2xl">
      {/* Presets first: on a doorstep this is the difference between ten seconds and ninety. */}
      <p className="eyebrow">Start from</p>
      <div className="mt-3 flex flex-wrap gap-2">
        {PRESETS.map((p) => (
          <button key={p.label} type="button" className="btn btn-ghost btn-sm" onClick={() => applyPreset(p)}>
            {p.label}
          </button>
        ))}
      </div>

      <div className="rule my-6" />

      <div className="grid gap-5">
        <div className="field">
          <label className="label" htmlFor="phone">
            Their number
          </label>
          <input
            className="input text-base"
            id="phone"
            name="phone"
            type="tel"
            inputMode="tel"
            autoComplete="off"
            required
            placeholder="(201) 555-0143"
            aria-describedby={errors?.phone ? 'phone-error' : undefined}
          />
          <FieldError errors={errors} name="phone" />
        </div>

        <div className="field">
          <label className="label" htmlFor="salon_name">
            Salon name
          </label>
          <input
            className="input text-base"
            id="salon_name"
            name="salon_name"
            required
            autoComplete="off"
            placeholder="Butterfly Studio Salon"
            aria-describedby={errors?.salon_name ? 'salon_name-error' : undefined}
          />
          <FieldError errors={errors} name="salon_name" />
          <p className="help">Malone says it is calling from here.</p>
        </div>

        <div className="field">
          <label className="label" htmlFor="offer_text">
            The offer
          </label>
          <textarea
            className="textarea text-base"
            id="offer_text"
            name="offer_text"
            rows={2}
            required
            value={offer}
            onChange={(e) => setOffer(e.target.value)}
            placeholder="20% off your next cut and colour, any day this week"
            aria-describedby={errors?.offer_text ? 'offer_text-error' : undefined}
          />
          <FieldError errors={errors} name="offer_text" />
        </div>

        <div className="field">
          <span className="label">Voice</span>
          <div className="grid gap-2">
            {voices.map((v) => (
              <label
                key={v.id}
                className="flex cursor-pointer items-start gap-3 rounded-[10px] border border-line px-3 py-2.5 text-sm transition-opacity duration-150 hover:opacity-80"
                htmlFor={`voice-${v.id}`}
              >
                <input
                  className="mt-1"
                  type="radio"
                  id={`voice-${v.id}`}
                  name="voice"
                  value={v.id}
                  defaultChecked={v.id === defaultVoice}
                />
                <span>
                  <span className="text-ink">{v.label}</span>
                  <span className="help mt-0.5 block">{v.hint}</span>
                </span>
              </label>
            ))}
          </div>
        </div>
      </div>

      <button
        type="button"
        className="btn btn-ghost btn-sm mt-5"
        onClick={() => setShowMore((v) => !v)}
        aria-expanded={showMore}
      >
        {showMore ? 'Fewer options' : 'More: code, notes, front desk, timezone'}
      </button>

      {showMore && (
        <div className="mt-5 grid gap-5">
          <div className="field">
            <label className="label" htmlFor="promo_code">
              Code to give out
            </label>
            <input
              className="input text-base"
              id="promo_code"
              name="promo_code"
              autoComplete="off"
              value={promo}
              onChange={(e) => setPromo(e.target.value)}
              placeholder="MALONE20"
              aria-describedby={errors?.promo_code ? 'promo_code-error' : undefined}
            />
            <FieldError errors={errors} name="promo_code" />
            <p className="help">Given once, after they agree to a time, spelled out slowly.</p>
          </div>

          <div className="field">
            <label className="label" htmlFor="instructions">
              How should this conversation run?
            </label>
            <textarea
              className="textarea text-base"
              id="instructions"
              name="instructions"
              rows={4}
              value={instructions}
              onChange={(e) => setInstructions(e.target.value)}
              placeholder={'Only offer Tuesday and Wednesday.\nMention the new colourist.\nDo not discuss pricing.'}
              aria-describedby={errors?.instructions ? 'instructions-error' : undefined}
            />
            <FieldError errors={errors} name="instructions" />
            <p className="help">
              Added on top of Malone&apos;s script, never instead of it. It still says it is a virtual
              assistant, still takes the first no, still stops when asked, still under three minutes.
            </p>
          </div>

          <div className="grid gap-5 sm:grid-cols-2">
            <div className="field">
              <label className="label" htmlFor="first_name">
                Their first name
              </label>
              <input className="input text-base" id="first_name" name="first_name" autoComplete="off" placeholder="Dana" />
              <p className="help">Blank opens with &ldquo;Hi there&rdquo;.</p>
            </div>

            <div className="field">
              <label className="label" htmlFor="booking_phone">
                Front desk number
              </label>
              <input
                className="input text-base"
                id="booking_phone"
                name="booking_phone"
                type="tel"
                inputMode="tel"
                placeholder="(201) 555-0199"
              />
              <p className="help">Read out on voicemail.</p>
            </div>
          </div>

          <div className="field">
            <label className="label" htmlFor="timezone">
              Their timezone
            </label>
            <select className="select text-base" id="timezone" name="timezone" defaultValue={defaultTimezone}>
              {TIMEZONES.map(([zone, label]) => (
                <option key={zone} value={zone}>
                  {label}
                </option>
              ))}
            </select>
          </div>

          <label className="flex items-start gap-3 text-sm" htmlFor="window_override">
            <input className="mt-0.5" id="window_override" name="window_override" type="checkbox" />
            <span>
              <span className="text-ink">Call outside 9am–7pm their time.</span>
              <span className="help mt-1 block">Only off-hours, only because they asked. Logged.</span>
            </span>
          </label>
          <FieldError errors={errors} name="window_override" />
        </div>
      )}

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
          <span className="text-ink">They asked me to call them.</span>
          <span className="help mt-1 block">Recorded against the call.</span>
        </span>
      </label>
      <FieldError errors={errors} name="consent_attested" />

      {/* Sticky on phones: after typing the offer your thumb is already at the bottom. */}
      <div className="sticky bottom-0 z-10 mt-6 -mx-6 border-t border-line bg-cream/95 px-6 py-4 backdrop-blur sm:static sm:mx-0 sm:border-0 sm:bg-transparent sm:px-0 sm:backdrop-blur-none">
        <div className="flex flex-wrap items-center gap-3">
          <Submit />
          {state.status === 'error' && <p className="error-text">{state.error}</p>}
        </div>
      </div>

      {state.status === 'success' && (
        <div className="card card-pad mt-6 bg-brass-wash">
          <p className="eyebrow">Ringing now</p>
          <p className="mt-2 text-lg">
            Calling <span className="font-display">{state.phone}</span> as {state.salonName}, in{' '}
            {state.voice}&rsquo;s voice.
          </p>
          {state.promoCode && (
            <p className="help mt-2">
              It hands out <span className="text-ink">{state.promoCode}</span> once a time is agreed.
            </p>
          )}
          {state.outsideWindow && <p className="help mt-2">Placed off-hours using the override.</p>}
          <p className="help mt-3">
            Hand them the phone. The transcript and any booking land in{' '}
            <a className="link" href="/admin/calls">
              Calls
            </a>{' '}
            when it ends.
          </p>
        </div>
      )}
    </form>
  );
}
