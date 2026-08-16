'use client';

import Link from 'next/link';
import { useActionState, useEffect, useRef } from 'react';
import { startAction } from '@/app/start/actions';
import {
  BUSINESS_TYPE_OPTIONS,
  DEFAULT_TIMEZONE,
  HONEYPOT_FIELD,
  INITIAL_START_STATE,
  LIMITS,
  LIST_SIZE_OPTIONS,
  OFFER_PLACEHOLDER,
  SUPPORT_EMAIL,
  TIMEZONE_GROUPS,
  bookingCallUrl,
  planById,
  type StartField,
  type StartSuccess,
} from '@/lib/onboarding';
import { PLANS, planLink, type Plan } from '@/lib/site';

export function StartForm() {
  const [state, formAction, pending] = useActionState(startAction, INITIAL_START_STATE);

  const alertRef = useRef<HTMLParagraphElement>(null);
  const doneRef = useRef<HTMLHeadingElement>(null);

  // Move focus to whatever just changed, so a screen reader and a thumb both land in the same place.
  useEffect(() => {
    if (state.status === 'success') doneRef.current?.focus();
    if (state.status === 'error') alertRef.current?.focus();
  }, [state]);

  if (state.status === 'success' && state.success) {
    return <Confirmation ref={doneRef} success={state.success} />;
  }

  // React 19 resets an uncontrolled form once the action settles, so a rejected submit re-seeds
  // every field from the values the action echoed back. Nobody retypes their offer.
  const value = (key: StartField, fallback = ''): string => state.values?.[key] ?? fallback;
  const fieldError = (key: StartField): string | undefined => state.fieldErrors?.[key];

  return (
    <form action={formAction} noValidate className="grid gap-5 sm:grid-cols-2">
      {/* Bots fill every input in the DOM. Humans never see this one; a value here is discarded
          server-side and the bot is shown the ordinary success screen. */}
      <div aria-hidden="true" className="pointer-events-none absolute left-[-9999px] h-px w-px overflow-hidden">
        <label htmlFor="sf-company-website">Company website</label>
        <input
          id="sf-company-website"
          name={HONEYPOT_FIELD}
          type="text"
          tabIndex={-1}
          autoComplete="off"
          defaultValue=""
        />
      </div>

      {state.error ? (
        <p ref={alertRef} tabIndex={-1} role="alert" className="error-text sm:col-span-2">
          {state.error}
        </p>
      ) : null}

      <FormField
        id="sf-salon-name"
        label="Salon or med spa name"
        help="Exactly how Malone should say it out loud."
        error={fieldError('salon_name')}
        wide
      >
        <input
          id="sf-salon-name"
          name="salon_name"
          className="input"
          type="text"
          required
          autoComplete="organization"
          maxLength={LIMITS.salonName}
          placeholder="Maison Verde Hair Studio"
          defaultValue={value('salon_name')}
          {...describe('sf-salon-name', fieldError('salon_name'))}
        />
      </FormField>

      <FormField id="sf-contact-name" label="Your name" error={fieldError('contact_name')}>
        <input
          id="sf-contact-name"
          name="contact_name"
          className="input"
          type="text"
          required
          autoComplete="name"
          maxLength={LIMITS.contactName}
          placeholder="Renée Alvarez"
          defaultValue={value('contact_name')}
          {...describe('sf-contact-name', fieldError('contact_name'))}
        />
      </FormField>

      <FormField
        id="sf-email"
        label="Work email"
        help="Booking alerts land here in seconds. The Friday report too."
        error={fieldError('contact_email')}
      >
        <input
          id="sf-email"
          name="contact_email"
          className="input"
          type="email"
          inputMode="email"
          required
          autoComplete="email"
          maxLength={LIMITS.email}
          placeholder="renee@maisonverde.com"
          defaultValue={value('contact_email')}
          {...describe('sf-email', fieldError('contact_email'))}
        />
      </FormField>

      <FormField
        id="sf-phone"
        label="Best phone"
        help="How we reach you — and the number Malone reads out if it leaves a voicemail. You can split those later."
        error={fieldError('contact_phone')}
        wide
      >
        <input
          id="sf-phone"
          name="contact_phone"
          className="input"
          type="tel"
          inputMode="tel"
          required
          autoComplete="tel"
          maxLength={LIMITS.phone}
          placeholder="(415) 555-0142"
          defaultValue={value('contact_phone')}
          {...describe('sf-phone', fieldError('contact_phone'))}
        />
      </FormField>

      <FormField id="sf-business-type" label="Business type" error={fieldError('business_type')}>
        <select
          id="sf-business-type"
          name="business_type"
          className="select"
          required
          defaultValue={value('business_type', 'salon')}
          {...describe('sf-business-type', fieldError('business_type'))}
        >
          {BUSINESS_TYPE_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      </FormField>

      <FormField
        id="sf-timezone"
        label="Timezone"
        help="Calls only ever go out inside business hours in this zone."
        error={fieldError('timezone')}
      >
        <select
          id="sf-timezone"
          name="timezone"
          className="select"
          required
          defaultValue={value('timezone', DEFAULT_TIMEZONE)}
          {...describe('sf-timezone', fieldError('timezone'))}
        >
          {TIMEZONE_GROUPS.map((group) => (
            <optgroup key={group.group} label={group.group}>
              {group.zones.map(([zone, label]) => (
                <option key={zone} value={zone}>
                  {label}
                </option>
              ))}
            </optgroup>
          ))}
        </select>
      </FormField>

      <FormField
        id="sf-list-size"
        label="Lapsed clients, roughly"
        help="People who have not booked in six months or more. A range is fine."
        error={fieldError('list_size')}
      >
        <select
          id="sf-list-size"
          name="list_size"
          className="select"
          required
          defaultValue={value('list_size', '250_1000')}
          {...describe('sf-list-size', fieldError('list_size'))}
        >
          {LIST_SIZE_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      </FormField>

      <FormField
        id="sf-ticket"
        label="Average ticket"
        help="US dollars per visit. Every recovered-revenue figure is booked visits × this number."
        error={fieldError('avg_ticket_dollars')}
      >
        <div className="relative">
          <span
            aria-hidden="true"
            className="pointer-events-none absolute top-1/2 left-3 -translate-y-1/2 text-sm text-ink-mute"
          >
            $
          </span>
          <input
            id="sf-ticket"
            name="avg_ticket_dollars"
            className="input pl-7 tabular-nums"
            type="number"
            inputMode="numeric"
            required
            min={LIMITS.ticketMinDollars}
            max={LIMITS.ticketMaxDollars}
            step={1}
            placeholder="120"
            defaultValue={value('avg_ticket_dollars')}
            {...describe('sf-ticket', fieldError('avg_ticket_dollars'))}
          />
        </div>
      </FormField>

      <FormField
        id="sf-offer"
        label="The win-back offer Malone should make"
        help="One sentence, spoken not printed. Malone reads this to every person it reaches, then offers two concrete times."
        error={fieldError('offer_text')}
        wide
      >
        <textarea
          id="sf-offer"
          name="offer_text"
          className="textarea"
          rows={3}
          required
          maxLength={LIMITS.offerMax}
          placeholder={OFFER_PLACEHOLDER}
          defaultValue={value('offer_text')}
          {...describe('sf-offer', fieldError('offer_text'))}
        />
      </FormField>

      <div className="sm:col-span-2">
        <hr className="rule mb-5" />
        <button type="submit" className="btn btn-primary w-full sm:w-auto" disabled={pending}>
          {pending ? 'Sending…' : 'Start my win-back campaign'}
        </button>
        <p className="help mt-3">
          No card yet — you choose a plan on the next screen. Your account is created switched off,
          so nothing can be dialled until we have been through your list with you.
        </p>
      </div>
    </form>
  );
}

/* ------------------------------------------------------------------ pieces */

/** `aria-describedby` only when there is an error to point at, so the hint is never announced twice. */
function describe(id: string, error: string | undefined) {
  return error ? { 'aria-invalid': true as const, 'aria-describedby': `${id}-error` } : {};
}

function FormField({
  id,
  label,
  help,
  error,
  wide,
  children,
}: {
  id: string;
  label: string;
  help?: string;
  error?: string;
  wide?: boolean;
  children: React.ReactNode;
}) {
  return (
    <div className={`field ${wide ? 'sm:col-span-2' : ''}`}>
      <label className="label" htmlFor={id}>
        {label}
      </label>
      {children}
      {error ? (
        <p className="error-text" id={`${id}-error`}>
          {error}
        </p>
      ) : null}
      {help ? <p className="help">{help}</p> : null}
    </div>
  );
}

/**
 * The money moment. The recommendation is a suggestion in plain sight: the other three plans are
 * listed underneath at their real prices and every one of them is clickable, including the cheapest.
 */
function Confirmation({
  ref,
  success,
}: {
  ref: React.Ref<HTMLHeadingElement>;
  success: StartSuccess;
}) {
  const plan = planById(success.recommendedPlanId);
  const others = PLANS.filter((p) => p.id !== success.recommendedPlanId);

  return (
    <div>
      <p className="eyebrow">Request received</p>
      <h2 ref={ref} tabIndex={-1} className="h-display mt-3 text-[clamp(1.75rem,5vw,2.5rem)]">
        Thanks, {success.greeting}. We have everything for {success.salonName}.
      </h2>
      <p className="prose-tight mt-4 text-[0.9375rem]">
        {success.confirmationEmailed ? (
          <>
            A copy of everything you wrote is on its way to <strong>{success.contactEmail}</strong>.
          </>
        ) : (
          <>
            Our confirmation email to <strong>{success.contactEmail}</strong> did not go through —
            your details are with us regardless. Write to {SUPPORT_EMAIL} if you want the copy.
          </>
        )}{' '}
        Nothing is dialled yet, and nothing can be until we have been through your answers and your
        list with you.
      </p>

      <hr className="rule my-8" />

      <p className="eyebrow">What we would put you on</p>
      <div className="card mt-4 border-brass/50 p-6">
        <div className="flex flex-wrap items-baseline justify-between gap-3">
          <h3 className="font-display text-2xl">{plan.name}</h3>
          <p className="font-display text-3xl leading-none">
            {plan.priceLabel}
            <span className="stat-label ml-2 align-middle">{plan.cadence}</span>
          </p>
        </div>
        <p className="prose-tight mt-3 text-[0.9375rem]">{success.recommendationReason}</p>
        <ul className="mt-4 grid gap-1.5 sm:grid-cols-2">
          {plan.features.map((f) => (
            <li key={f} className="flex gap-2.5 text-[0.875rem] leading-relaxed text-ink-soft">
              <span aria-hidden className="mt-2 h-px w-3 shrink-0 bg-brass" />
              <span>{f}</span>
            </li>
          ))}
        </ul>
        <div className="mt-6">
          {success.checkoutUrl ? (
            <a className="btn btn-primary w-full sm:w-auto" href={success.checkoutUrl}>
              Start the {plan.name} — {plan.priceLabel} {plan.cadence}
            </a>
          ) : (
            <div className="grid gap-2">
              <span className="btn btn-primary w-full sm:w-auto" aria-disabled="true">
                Checkout opening shortly
              </span>
              <a className="help underline decoration-line underline-offset-4" href={bookingCallUrl()}>
                Book 15 minutes and we will send the payment link
              </a>
            </div>
          )}
        </div>
      </div>

      <p className="help mt-6">
        A suggestion, not a gate. Any of these works with what you told us:
      </p>
      <ul className="mt-3 grid gap-2">
        {others.map((p) => (
          <PlanChoice key={p.id} plan={p} />
        ))}
      </ul>

      <hr className="rule my-8" />

      <div className="grid gap-2">
        <p className="help">
          Not paying today?{' '}
          <Link className="underline decoration-line underline-offset-4" href="/start/thanks">
            See exactly what happens next
          </Link>
          .
        </p>
        <p className="help">
          Rather talk it through first?{' '}
          <a className="underline decoration-line underline-offset-4" href={bookingCallUrl()}>
            Book 15 minutes
          </a>{' '}
          — or email{' '}
          <a className="underline decoration-line underline-offset-4" href={`mailto:${SUPPORT_EMAIL}`}>
            {SUPPORT_EMAIL}
          </a>
          .
        </p>
      </div>
    </div>
  );
}

function PlanChoice({ plan }: { plan: Plan }) {
  const href = planLink(plan);

  return (
    <li className="card flex flex-wrap items-center justify-between gap-3 px-5 py-4">
      <div>
        <p className="font-display text-lg leading-tight">{plan.name}</p>
        <p className="stat-label mt-1">
          {plan.priceLabel} · {plan.cadence}
        </p>
      </div>
      {href === '#' ? (
        <span className="btn btn-ghost btn-sm" aria-disabled="true">
          Link coming
        </span>
      ) : (
        <a className="btn btn-ghost btn-sm" href={href}>
          Choose {plan.name}
        </a>
      )}
    </li>
  );
}
