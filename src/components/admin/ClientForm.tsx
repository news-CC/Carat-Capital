'use client';

import { useActionState } from 'react';
import {
  createClientAction,
  updateClientAction,
  type ClientFormState,
} from '@/app/admin/clients/actions';

const TIMEZONES: { group: string; zones: [string, string][] }[] = [
  {
    group: 'United States',
    zones: [
      ['America/New_York', 'New York — Eastern'],
      ['America/Detroit', 'Detroit — Eastern'],
      ['America/Indiana/Indianapolis', 'Indianapolis — Eastern'],
      ['America/Chicago', 'Chicago — Central'],
      ['America/Denver', 'Denver — Mountain'],
      ['America/Phoenix', 'Phoenix — Mountain, no DST'],
      ['America/Los_Angeles', 'Los Angeles — Pacific'],
      ['America/Anchorage', 'Anchorage — Alaska'],
      ['Pacific/Honolulu', 'Honolulu — Hawaii'],
      ['America/Puerto_Rico', 'San Juan — Atlantic'],
    ],
  },
  {
    group: 'Canada',
    zones: [
      ['America/Toronto', 'Toronto — Eastern'],
      ['America/Winnipeg', 'Winnipeg — Central'],
      ['America/Edmonton', 'Edmonton — Mountain'],
      ['America/Vancouver', 'Vancouver — Pacific'],
      ['America/Halifax', 'Halifax — Atlantic'],
    ],
  },
  {
    group: 'Elsewhere',
    zones: [
      ['Europe/London', 'London'],
      ['Europe/Dublin', 'Dublin'],
      ['Europe/Madrid', 'Madrid'],
      ['Australia/Sydney', 'Sydney'],
    ],
  },
];

const OFFER_PLACEHOLDER =
  "20% off your next colour with Renée, plus a complimentary gloss — I've got Tuesday at 2 or Thursday at 5.";

export type ClientFormDefaults = {
  id?: string;
  name?: string;
  contact_name?: string | null;
  contact_email?: string;
  contact_phone?: string | null;
  booking_phone?: string | null;
  offer_text?: string;
  timezone?: string;
  vertical?: string;
  avg_ticket_cents?: number;
};

const INITIAL: ClientFormState = { ok: false };

export function ClientForm({
  mode,
  defaults = {},
}: {
  mode: 'create' | 'edit';
  defaults?: ClientFormDefaults;
}) {
  const [state, formAction, pending] = useActionState(
    mode === 'create' ? createClientAction : updateClientAction,
    INITIAL,
  );

  // On a rejected submit the action echoes the typed values back, because React resets
  // uncontrolled forms once an action settles.
  const value = (key: string, fallback: string | null | undefined): string =>
    state.values?.[key] ?? fallback ?? '';

  const err = (key: string) => state.fieldErrors?.[key];
  const ticketDollars = defaults.avg_ticket_cents ? String(Math.round(defaults.avg_ticket_cents / 100)) : '120';

  return (
    <form action={formAction} className="grid gap-5 sm:grid-cols-2">
      {mode === 'edit' && <input type="hidden" name="id" value={defaults.id ?? ''} />}

      <div className="field sm:col-span-2">
        <label className="label" htmlFor="cf-name">
          Salon name
        </label>
        <input
          id="cf-name"
          className="input"
          name="name"
          required
          maxLength={120}
          placeholder="Maison Verde Hair Studio"
          defaultValue={value('name', defaults.name)}
          aria-invalid={err('name') ? true : undefined}
        />
        {err('name') && <p className="error-text">{err('name')}</p>}
        <p className="help">Exactly how Malone should say it on the phone.</p>
      </div>

      <div className="field">
        <label className="label" htmlFor="cf-contact-name">
          Owner / manager
        </label>
        <input
          id="cf-contact-name"
          className="input"
          name="contact_name"
          maxLength={120}
          placeholder="Renée Alvarez"
          defaultValue={value('contact_name', defaults.contact_name)}
        />
        {err('contact_name') && <p className="error-text">{err('contact_name')}</p>}
      </div>

      <div className="field">
        <label className="label" htmlFor="cf-contact-email">
          Owner email
        </label>
        <input
          id="cf-contact-email"
          className="input"
          name="contact_email"
          type="email"
          required
          placeholder="renee@maisonverde.com"
          defaultValue={value('contact_email', defaults.contact_email)}
          aria-invalid={err('contact_email') ? true : undefined}
        />
        {err('contact_email') && <p className="error-text">{err('contact_email')}</p>}
        <p className="help">Booking alerts land here within seconds. The Friday report too.</p>
      </div>

      <div className="field">
        <label className="label" htmlFor="cf-contact-phone">
          Owner phone
        </label>
        <input
          id="cf-contact-phone"
          className="input"
          name="contact_phone"
          type="tel"
          placeholder="(415) 555-0142"
          defaultValue={value('contact_phone', defaults.contact_phone)}
          aria-invalid={err('contact_phone') ? true : undefined}
        />
        {err('contact_phone') && <p className="error-text">{err('contact_phone')}</p>}
      </div>

      <div className="field">
        <label className="label" htmlFor="cf-booking-phone">
          Booking phone
        </label>
        <input
          id="cf-booking-phone"
          className="input"
          name="booking_phone"
          type="tel"
          placeholder="(415) 555-0188"
          defaultValue={value('booking_phone', defaults.booking_phone)}
          aria-invalid={err('booking_phone') ? true : undefined}
        />
        {err('booking_phone') && <p className="error-text">{err('booking_phone')}</p>}
        <p className="help">The salon&rsquo;s real front-desk line. Malone reads it out on voicemail.</p>
      </div>

      <div className="field sm:col-span-2">
        <label className="label" htmlFor="cf-offer">
          Offer text
        </label>
        <textarea
          id="cf-offer"
          className="textarea"
          name="offer_text"
          required
          rows={3}
          maxLength={400}
          placeholder={OFFER_PLACEHOLDER}
          defaultValue={value('offer_text', defaults.offer_text)}
          aria-invalid={err('offer_text') ? true : undefined}
        />
        {err('offer_text') && <p className="error-text">{err('offer_text')}</p>}
        <p className="help">
          Spoken aloud, one sentence, with two concrete times. Write it the way a person talks.
        </p>
      </div>

      <div className="field">
        <label className="label" htmlFor="cf-timezone">
          Timezone
        </label>
        <select
          id="cf-timezone"
          className="select"
          name="timezone"
          defaultValue={value('timezone', defaults.timezone) || 'America/New_York'}
        >
          {TIMEZONES.map((group) => (
            <optgroup key={group.group} label={group.group}>
              {group.zones.map(([zone, label]) => (
                <option key={zone} value={zone}>
                  {label}
                </option>
              ))}
            </optgroup>
          ))}
        </select>
        {err('timezone') && <p className="error-text">{err('timezone')}</p>}
        <p className="help">The call window is enforced in this zone. Never dialed outside it.</p>
      </div>

      <div className="field">
        <label className="label" htmlFor="cf-vertical">
          Vertical
        </label>
        <select
          id="cf-vertical"
          className="select"
          name="vertical"
          defaultValue={value('vertical', defaults.vertical) || 'salon'}
        >
          <option value="salon">Salon</option>
          <option value="medspa">Med spa</option>
        </select>
        {err('vertical') && <p className="error-text">{err('vertical')}</p>}
      </div>

      <div className="field">
        <label className="label" htmlFor="cf-ticket">
          Average ticket
        </label>
        <input
          id="cf-ticket"
          className="input tabular-nums"
          name="avg_ticket_dollars"
          type="number"
          min={1}
          max={5000}
          step={1}
          required
          defaultValue={value('avg_ticket_dollars', ticketDollars)}
          aria-invalid={err('avg_ticket_dollars') ? true : undefined}
        />
        {err('avg_ticket_dollars') && <p className="error-text">{err('avg_ticket_dollars')}</p>}
        <p className="help">US dollars per visit. Recovered-revenue figures are booked visits × this.</p>
      </div>

      <div className="sm:col-span-2">
        <div className="rule mb-5" />
        <div className="flex flex-wrap items-center gap-4">
          <button className="btn btn-primary" type="submit" disabled={pending}>
            {pending ? 'Saving…' : mode === 'create' ? 'Create client' : 'Save changes'}
          </button>
          {state.error && <p className="error-text">{state.error}</p>}
          {state.ok && state.message && <p className="text-sm text-sage">{state.message}</p>}
        </div>
      </div>
    </form>
  );
}
