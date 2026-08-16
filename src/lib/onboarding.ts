/**
 * The self-serve onboarding funnel — pure module.
 *
 * Types, the zod schema the server action validates with, the plan-recommendation rule, and the
 * option lists both the form and the confirmation render from. No I/O, no `process.env`, no
 * database, no React: safe to import from a `'use client'` component and testable on its own.
 *
 * The server action in src/app/start/actions.ts is the authority. Everything here is shared shape.
 */

import { z } from 'zod';
import { COMPANY, COMPANY_ADDRESS_LINE, PLANS, type Plan } from '@/lib/site';

/* ------------------------------------------------------------------ constants */

/**
 * Contact details are derived from src/lib/site.ts rather than retyped here. A support address
 * that drifts between the marketing page and the confirmation email is the kind of small lie
 * nobody notices until a prospect writes to an inbox no one reads.
 */

/**
 * The booking calendar, resolved through the one accessor that also repairs a stale env value.
 * Re-exported rather than re-derived so every funnel surface — form, confirmation panel, page,
 * confirmation email — links to the same calendar as the marketing site.
 */
export { bookingCallUrl } from '@/lib/site';

/** The only support address. Every funnel surface shows this one. */
export const SUPPORT_EMAIL = COMPANY.supportEmail;

/** The number Malone dials out from, so a prospect recognises it in their call log. */
export const OUTBOUND_NUMBER = COMPANY.outboundPhone;

export const OPERATOR = {
  legalName: COMPANY.legalName,
  address: COMPANY_ADDRESS_LINE,
} as const;

export const DEFAULT_TIMEZONE = 'America/New_York';

/** Caps for every free-text field. A public endpoint accepts nothing unbounded. */
export const LIMITS = {
  salonName: 120,
  contactName: 120,
  email: 160,
  phone: 40,
  timezone: 64,
  offerMin: 12,
  offerMax: 400,
  ticketMinDollars: 5,
  ticketMaxDollars: 5000,
} as const;

/* ------------------------------------------------------------------ options */

export const BUSINESS_TYPES = ['salon', 'medspa', 'multi-location'] as const;
export type BusinessType = (typeof BUSINESS_TYPES)[number];

export const BUSINESS_TYPE_OPTIONS: { value: BusinessType; label: string }[] = [
  { value: 'salon', label: 'Salon — hair, nails, barbering' },
  { value: 'medspa', label: 'Med spa — injectables, laser, skin' },
  { value: 'multi-location', label: 'Multi-location group' },
];

/** Ranges, not a number: nobody knows their lapsed count to the digit, and a guess would be noise. */
export const LIST_SIZES = ['under_250', '250_1000', '1000_5000', '5000_plus'] as const;
export type ListSize = (typeof LIST_SIZES)[number];

/** The entry range. Picking it recommends the one-time pilot, whatever the vertical. */
export const SMALLEST_LIST_SIZE: ListSize = 'under_250';

export const LIST_SIZE_OPTIONS: { value: ListSize; label: string }[] = [
  { value: 'under_250', label: 'Under 250 lapsed clients' },
  { value: '250_1000', label: '250 to 1,000' },
  { value: '1000_5000', label: '1,000 to 5,000' },
  { value: '5000_plus', label: 'More than 5,000' },
];

export const LIST_SIZE_LABELS: Record<ListSize, string> = {
  under_250: 'Under 250',
  '250_1000': '250 to 1,000',
  '1000_5000': '1,000 to 5,000',
  '5000_plus': 'More than 5,000',
};

export const BUSINESS_TYPE_LABELS: Record<BusinessType, string> = {
  salon: 'Salon',
  medspa: 'Med spa',
  'multi-location': 'Multi-location group',
};

/**
 * Real IANA zone ids. The dialer compares `now() at time zone cl.timezone` against the calling
 * window, so a made-up string here would fail closed and never dial — the list is deliberately
 * short and real rather than long and guessed.
 */
export const TIMEZONE_GROUPS: { group: string; zones: [string, string][] }[] = [
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
      ['America/Regina', 'Regina — Central, no DST'],
      ['America/Edmonton', 'Edmonton — Mountain'],
      ['America/Vancouver', 'Vancouver — Pacific'],
      ['America/Halifax', 'Halifax — Atlantic'],
      ['America/St_Johns', 'St John’s — Newfoundland'],
    ],
  },
  {
    group: 'Elsewhere',
    zones: [
      ['Europe/London', 'London'],
      ['Europe/Dublin', 'Dublin'],
      ['Europe/Madrid', 'Madrid'],
      ['Europe/Berlin', 'Berlin'],
      ['Australia/Sydney', 'Sydney'],
      ['Pacific/Auckland', 'Auckland'],
    ],
  },
];

/** Written to be read out loud, because that is what happens to it. */
export const OFFER_PLACEHOLDER =
  '20% off your next colour, or a free deep-conditioning add-on — whichever they’d rather have.';

/**
 * What actually happens after the form is submitted. Every line is something the code does:
 * the row is written with `active = false`, the claim query requires `active = true`, the scrub
 * runs server-side on upload, and the booking alert and Friday report are shipped templates.
 */
export const NEXT_STEPS: { n: string; title: string; body: string }[] = [
  {
    n: '01',
    title: 'Nothing dials until we have looked',
    body: 'Your account is created switched off, and a switched-off account is not eligible to dial anyone. It stays that way until we have been through your answers and your list with you. That is a gate in the code, not a promise in a document.',
  },
  {
    n: '02',
    title: 'You send the export, we scrub it',
    body: 'Whatever your booking software produces, CSV or XLSX. Rows without consent are dropped, unusable numbers are dropped, anyone on the global do-not-call list is dropped — and you see the count for every reason before one call goes out.',
  },
  {
    n: '03',
    title: 'Malone calls inside your hours, you get the email',
    body: 'One attempt per person, ever, in your salon’s local time. A booking email lands the second someone says yes, and Friday brings the arithmetic: dialled, reached, booked, opted out, recovered revenue at your ticket.',
  },
];

/* ------------------------------------------------------------------ plans */

export type PlanId = 'pilot' | 'salon' | 'medspa' | 'group';

/**
 * Total by construction: PLANS is a module-level literal that contains all four ids, so the
 * fallback exists only so callers never have to handle `undefined`.
 */
export function planById(id: PlanId): Plan {
  return PLANS.find((p) => p.id === id) ?? PLANS[0];
}

/**
 * The recommendation. Multi-location → the group plan, med spa → med spa, salon → salon —
 * except that the smallest list size always wins and gets the $299 one-time pilot instead,
 * whatever the vertical. Under 250 names is a week of calling, not a subscription, and asking
 * someone to start a monthly plan for it is a worse deal for them and a worse conversion for us.
 *
 * It is a suggestion only. Every caller renders the other three plans alongside it, priced and
 * clickable — the cheaper option is never hidden.
 */
export function recommendPlan(a: { businessType: BusinessType; listSize: ListSize }): PlanId {
  if (a.listSize === SMALLEST_LIST_SIZE) return 'pilot';
  if (a.businessType === 'multi-location') return 'group';
  if (a.businessType === 'medspa') return 'medspa';
  return 'salon';
}

/** One honest sentence for why that plan, shown next to the recommendation. */
export function recommendationReason(a: { businessType: BusinessType; listSize: ListSize }): string {
  if (a.listSize === SMALLEST_LIST_SIZE) {
    return 'Under 250 names is one week of calling, not a subscription. The pilot runs the whole list once and tells you what it was worth — then you decide whether a monthly plan is worth anything to you.';
  }
  if (a.businessType === 'multi-location') {
    return 'A group needs its own offer, its own calling hours and its own booking inbox per location, rolled into one Friday report.';
  }
  if (a.businessType === 'medspa') {
    return 'Med spa recall is higher ticket and longer memory — lapsed membership and treatment cycles, priced for a list that size.';
  }
  return 'One location, one rolling win-back campaign, up to 1,500 contacts a month. This is the plan most single salons want.';
}

/**
 * The database has exactly two verticals (`salon | medspa` in supabase/migrations/0001_init.sql).
 * A multi-location group is a group of salons, so it stores as `salon`; the real answer travels in
 * the operator email, and the operator reviews every signup before it can dial anything.
 */
export function verticalFor(businessType: BusinessType): 'salon' | 'medspa' {
  return businessType === 'medspa' ? 'medspa' : 'salon';
}

/* ------------------------------------------------------------------ validation */

/** Deliberately loose on the local part, strict on shape: the confirmation email is the real test. */
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[A-Za-z]{2,}$/;

/** Pure: `Intl` is a language primitive, not I/O. An unknown zone throws and is rejected. */
export function isSupportedTimeZone(tz: string): boolean {
  try {
    new Intl.DateTimeFormat('en-US', { timeZone: tz });
    return true;
  } catch {
    return false;
  }
}

/**
 * The schema. Server-side is the authority — the browser's `required` attributes are a courtesy,
 * and the form is submitted with `noValidate` so these messages are the only voice the user hears.
 */
export const StartSchema = z.object({
  salon_name: z
    .string()
    .min(2, 'Use the name Malone should say out loud on the phone.')
    .max(LIMITS.salonName, 'That is longer than any salon name — shorten it.'),
  contact_name: z
    .string()
    .min(2, 'Who should we reply to?')
    .max(LIMITS.contactName, 'Shorten that to a name we can use.'),
  contact_email: z
    .string()
    .max(LIMITS.email, 'That address is too long to be real.')
    .regex(EMAIL_RE, 'A working email — booking alerts and the Friday report go here.'),
  contact_phone: z
    .string()
    .min(7, 'We need a number we can actually reach you on.')
    .max(LIMITS.phone, 'That is too long to be a phone number.'),
  business_type: z.enum(BUSINESS_TYPES, { error: 'Pick the one that fits best.' }),
  timezone: z
    .string()
    .max(LIMITS.timezone, 'Choose a timezone from the list.')
    .refine(isSupportedTimeZone, 'Choose a timezone from the list.'),
  list_size: z.enum(LIST_SIZES, { error: 'A rough range is enough.' }),
  avg_ticket_dollars: z
    .number('Average ticket in whole dollars, digits only.')
    .int('Whole dollars — no cents.')
    .min(LIMITS.ticketMinDollars, `That is below $${LIMITS.ticketMinDollars}. Check the figure.`)
    .max(
      LIMITS.ticketMaxDollars,
      `That is above $${LIMITS.ticketMaxDollars.toLocaleString('en-US')} — check the figure.`,
    ),
  offer_text: z
    .string()
    .min(LIMITS.offerMin, 'Write the offer the way you would say it, not the way it looks on a flyer.')
    .max(LIMITS.offerMax, 'Keep it to something that can be said in one breath.'),
});

export type StartInput = z.infer<typeof StartSchema>;

/** The keys the form posts, in order. Used to echo values back after a rejected submit. */
export const START_FIELDS = [
  'salon_name',
  'contact_name',
  'contact_email',
  'contact_phone',
  'business_type',
  'timezone',
  'list_size',
  'avg_ticket_dollars',
  'offer_text',
] as const;

export type StartField = (typeof START_FIELDS)[number];

/**
 * Hidden field name. Bots fill every input they can see in the DOM; a human never touches this one,
 * so a non-empty value is the single cheapest bot signal available without a third-party service.
 */
export const HONEYPOT_FIELD = 'company_website';

/** What the server action hands back on success, for the confirmation panel to render. */
export type StartSuccess = {
  /** First name only — the confirmation greets them, it does not file them. */
  greeting: string;
  salonName: string;
  contactEmail: string;
  recommendedPlanId: PlanId;
  recommendationReason: string;
  /** The recommended plan's Stripe payment link, or null when it is not configured. */
  checkoutUrl: string | null;
  /**
   * Whether the confirmation email actually left. A failed send never fails the signup — but the
   * confirmation screen must not promise an inbox copy that is not coming.
   */
  confirmationEmailed: boolean;
};

export type StartState = {
  status: 'idle' | 'error' | 'success';
  /** One generic sentence. Database detail goes to the server log, never to the browser. */
  error?: string;
  fieldErrors?: Partial<Record<StartField, string>>;
  /** React 19 resets an uncontrolled form once an action settles, so failures echo the input back. */
  values?: Partial<Record<StartField, string>>;
  success?: StartSuccess;
};

export const INITIAL_START_STATE: StartState = { status: 'idle' };

/** "Renée Alvarez" → "Renée". Falls back to the whole string, then to a neutral greeting. */
export function firstNameOf(fullName: string): string {
  const first = fullName.trim().split(/\s+/)[0];
  return first || 'there';
}
