/**
 * Marketing copy + pricing config for startup25.com.
 * Pure data — safe to import from client components.
 */

/** The legal entity behind the product. Rendered in the footer and in page metadata. */
export const COMPANY = {
  legalName: "Easecase, Inc.",
  addressStreet: "1111b South Governors Avenue",
  addressLocality: "Dover",
  addressRegion: "DE",
  postalCode: "19904",
  addressCountry: "United States",
  supportEmail: "salon925malon@proton.me",
  /** The number Salon Malone calls from — printed so anyone who gets a call can check it. */
  outboundPhone: "+1 (863) 496-6101",
  outboundPhoneHref: "tel:+18634966101",
} as const;

/** One street line for compact footer rendering. */
export const COMPANY_ADDRESS_LINE = `${COMPANY.addressStreet}, ${COMPANY.addressLocality}, ${COMPANY.addressRegion} ${COMPANY.postalCode}, ${COMPANY.addressCountry}`;

/**
 * The booking calendar. This exact URL and no other — the deeper /salon-malone path
 * that used to be configured does not exist and returns a 404.
 */
export const BOOKING_CALL_URL = "https://cal.com/startup25";

/** The conversion path, in one place so every CTA on the site says the same thing. */
export const CTA = {
  startHref: "/start",
  startLabel: "Start my win-back campaign",
  startLabelShort: "Start my campaign",
  callLabel: "Book a 15-minute call",
  callLabelShort: "Book a call",
} as const;

export const SITE = {
  name: "Salon Malone",
  domain: "startup25.com",
  tagline: "Win back the clients who stopped coming.",
  headline: "Your dead client list is buried money.",
  // Every claim here has to be one the shipped product delivers: the Friday email counts booked
  // visits at the average ticket and says so, and the money is a $299 one-time pilot plus flat
  // monthly tiers. No pay-per-show claim — nothing in the product records a show.
  subhead:
    "Salon Malone is the virtual concierge that phones the clients who quietly stopped booking, offers them a specific time, and emails you the moment one says yes. You write the offer, we go through it and your list with you before anything dials — then a $299 pilot or a flat monthly plan. No per-minute billing, no per-lead invoices.",
  description:
    "Salon Malone calls your lapsed salon or med spa clients as your virtual concierge, books them back into empty chairs, emails you the instant a booking lands, and sends a Friday report with estimated recovered revenue from the visits it booked. Consent-gated, opt-out instant. Voice and email only.",
  contactEmail: COMPANY.supportEmail,
  complianceLine:
    "We only call contacts you have marked as consented, one attempt each, inside local business hours. Malone says it is a virtual assistant on every call. Anyone who asks to be removed is added to a global do-not-call list before the call ends.",
} as const;

export type Plan = {
  id: string;
  name: string;
  priceLabel: string;
  cadence: string;
  blurb: string;
  features: string[];
  linkEnv: string;
  highlight?: boolean;
};

export const PLANS: Plan[] = [
  {
    id: "pilot",
    name: "Win-Back Pilot",
    priceLabel: "$299",
    cadence: "one time",
    blurb:
      "One list, one campaign, one week. The cheapest honest way to find out what your lapsed clients are actually worth.",
    features: [
      "Up to 400 consented contacts dialled",
      "Offer written with you before we call",
      "Booking emails as they land",
      "One closing report with the real numbers",
      "No subscription, no auto-renew",
    ],
    linkEnv: "NEXT_PUBLIC_STRIPE_LINK_PILOT_299",
  },
  {
    id: "salon",
    name: "Salon",
    priceLabel: "$399",
    cadence: "per month",
    blurb: "One location, one chair-filling campaign running quietly in the background.",
    features: [
      "Up to 1,500 contacts dialled per month",
      "Rolling win-back campaign",
      "Instant booking emails",
      "Friday recovered-revenue report",
      "Global opt-out list managed for you",
    ],
    linkEnv: "NEXT_PUBLIC_STRIPE_LINK_SALON_399",
    highlight: true,
  },
  {
    id: "medspa",
    name: "Med Spa",
    priceLabel: "$999",
    cadence: "per month",
    blurb: "Higher ticket, longer memory. Built for injectables, laser and membership recall.",
    features: [
      "Up to 5,000 contacts dialled per month",
      "Treatment-aware offer scripting",
      "Lapsed-membership recall passes",
      "Instant booking emails",
      "Friday recovered-revenue report",
    ],
    linkEnv: "NEXT_PUBLIC_STRIPE_LINK_MEDSPA_999",
  },
  {
    id: "group",
    name: "Multi-Location",
    priceLabel: "$2,499",
    cadence: "per month",
    blurb: "Up to ten locations, each with its own offer, own hours and own inbox.",
    features: [
      "Up to 25,000 contacts dialled per month",
      "Per-location offers and calling hours",
      "Per-location booking alerts",
      "One rolled-up Friday report",
      "Shared suppression list across the group",
    ],
    linkEnv: "NEXT_PUBLIC_STRIPE_LINK_GROUP_2499",
  },
];

/**
 * Stripe payment links must reach the browser, so they are NEXT_PUBLIC_ and read
 * through a static map — Next.js only inlines literal `process.env.NEXT_PUBLIC_X`
 * references, never computed keys.
 */
const PAYMENT_LINKS: Record<string, string | undefined> = {
  NEXT_PUBLIC_STRIPE_LINK_PILOT_299: process.env.NEXT_PUBLIC_STRIPE_LINK_PILOT_299,
  NEXT_PUBLIC_STRIPE_LINK_SALON_399: process.env.NEXT_PUBLIC_STRIPE_LINK_SALON_399,
  NEXT_PUBLIC_STRIPE_LINK_MEDSPA_999: process.env.NEXT_PUBLIC_STRIPE_LINK_MEDSPA_999,
  NEXT_PUBLIC_STRIPE_LINK_GROUP_2499: process.env.NEXT_PUBLIC_STRIPE_LINK_GROUP_2499,
};

/** Real https link, or '#' when the payment link is not live yet. */
export function planLink(p: Plan): string {
  const link = PAYMENT_LINKS[p.linkEnv]?.trim();
  return link && /^https:\/\//i.test(link) ? link : "#";
}

/**
 * The book-a-call link.
 *
 * `BOOKING_CALL_URL` is the answer unless the environment supplies a different https URL,
 * and a cal.com URL under our own handle is collapsed back to the booking page itself:
 * the deployed value spent a while pointing at `cal.com/startup25/salon-malone`, an event
 * type that does not exist, so every "book a call" on the site landed on a 404. Env can
 * still point the CTA at a completely different scheduler; it can no longer point it at a
 * dead sub-path of ours.
 */
export function bookingCallUrl(): string {
  const raw = process.env.NEXT_PUBLIC_BOOKING_CALL_URL?.trim();
  if (!raw || !/^https:\/\//i.test(raw)) return BOOKING_CALL_URL;

  try {
    const url = new URL(raw);
    const isCalCom = /^(www\.)?cal\.com$/i.test(url.hostname);
    const isOurHandle = /^\/startup25(\/|$)/i.test(url.pathname);
    return isCalCom && isOurHandle ? BOOKING_CALL_URL : raw;
  } catch {
    return BOOKING_CALL_URL;
  }
}

/** 'HH:MM' 24h → '9:00 AM'. Used to print the real calling window in the copy. */
export function formatClock(hhmm: string): string {
  const m = /^(\d{1,2}):(\d{2})$/.exec(hhmm.trim());
  if (!m) return hhmm;
  const hour24 = Number(m[1]);
  const minute = m[2];
  const suffix = hour24 < 12 ? "AM" : "PM";
  const hour12 = hour24 % 12 === 0 ? 12 : hour24 % 12;
  return `${hour12}:${minute} ${suffix}`;
}

export const STEPS: { n: string; title: string; body: string }[] = [
  {
    n: "01",
    title: "Tell us about the salon",
    body: "Two minutes on the start form: the salon, your timezone, your average ticket, roughly how many clients have drifted, and the offer you want Malone to make. The form tells you which plan fits before you pay for anything.",
  },
  {
    n: "02",
    title: "Send the list",
    body: "Export the clients who have not booked in six months. CSV or XLSX, whatever your software spits out. We map the columns for you — name, phone, last visit, and the consent column.",
  },
  {
    n: "03",
    title: "We scrub it before anyone rings",
    body: "Rows without consent are dropped. Bad numbers are dropped. Anyone on the do-not-call list is dropped. You see the counts for every reason before a single call goes out.",
  },
  {
    n: "04",
    title: "Malone calls, inside your hours",
    body: "One attempt per person, ever, in your salon’s local time. Malone opens by saying it is a virtual concierge, offers two concrete times, and takes the first yes.",
  },
  {
    n: "05",
    title: "You get the email immediately",
    body: "Name, phone, the slot they asked for, and what was said. It lands while the chair is still open, so your front desk can confirm it the same hour.",
  },
  {
    n: "06",
    title: "Friday, the arithmetic",
    body: "One email: dialled, reached, booked, opted out, and recovered revenue at your average ticket. If the number is bad, you will see it on Friday, not in six months.",
  },
];

/**
 * A sample exchange, written from the prompt Malone actually runs. It is an example, not a
 * transcript: the salon, the client and the offer are all invented for the page.
 */
export const SAMPLE_CALL = {
  salon: "Ridgeline Hair",
  client: "Dana",
  offer: "a complimentary gloss with your next cut",
  disclaimer:
    "An example script, not a recording. The lines are the ones Malone is built to say — the salon, the client and the offer are invented for this page. Nothing here is a real call, and no client of ours appears on this site.",
  lines: [
    {
      who: "Malone",
      agent: true,
      text: "Hey Dana — Salon Malone here, Ridgeline Hair’s virtual concierge. Ninety seconds, I promise. We miss you.",
    },
    { who: "Dana", agent: false, text: "Oh — hi. Hang on, is this a real person?" },
    {
      who: "Malone",
      agent: true,
      text: "I’m a virtual assistant for Ridgeline Hair — a real human takes care of you in the chair.",
    },
    { who: "Dana", agent: false, text: "Ha. Okay. What’s up?" },
    {
      who: "Malone",
      agent: true,
      text: "It’s been a while, so we saved you something: a complimentary gloss with your next cut. Thursday at two, or Saturday morning at ten — which is easier?",
    },
    { who: "Dana", agent: false, text: "Saturday could work, I think." },
    {
      who: "Malone",
      agent: true,
      text: "Saturday at ten it is. I’ll note it down and the desk will confirm with you. Take care, Dana.",
    },
  ],
  branches: [
    {
      when: "If it is a no",
      line: "All love — the chair’s here when you’re ready.",
      then: "Call ends there. No rebuttal, no second attempt, not next month either.",
    },
    {
      when: "If they say stop calling",
      line: "Done — you’re off the list. Be good.",
      then: "The number is written to a global do-not-call list before the call report is accepted, and pulled out of every queue we run.",
    },
    {
      when: "If a machine picks up",
      line: "We saved you something… call the salon and we’ll get you back in the chair.",
      then: "One fifteen-second message with your real front-desk number. Malone does not call back.",
    },
  ],
} as const;

/** Illustrative arithmetic only — labelled as such everywhere it renders. */
export const MATH_EXAMPLE = {
  premise:
    "A two-chair salon, $120 average ticket, eighteen months of clients who drifted off. Every number below is an assumption we picked to show the shape of the arithmetic.",
  rows: [
    { label: "Names exported from the booking system", value: "1,200", note: "your list" },
    { label: "Survive the scrub (consent + valid phone)", value: "740", note: "we drop the rest" },
    { label: "Answer the phone", value: "260", note: "35% of dials" },
    { label: "Book a specific time", value: "31", note: "12% of conversations" },
    { label: "Actually sit in the chair", value: "25", note: "80% show rate" },
    { label: "Recovered revenue, month one", value: "$3,000", note: "25 shows × $120" },
  ],
  // The shipped Friday email reports booked × ticket (31 × $120 = $3,720), so the page names that
  // number too instead of showing only the smaller show-based one the buyer would never be sent.
  footnote:
    "Against $399 for the month. Two numbers on purpose: our Friday email counts booked visits at your ticket — 31 × $120 is $3,720 — and the $3,000 above is that same month if only 25 of them show. No-shows count in ours, so your book is the last word. Your list, your offer and your show rate will move every line — up or down. We report the real ones every Friday.",
} as const;

/** The compliance posture, stated as what the code does. Each line is enforced, not intended. */
export const SAFEGUARDS: { title: string; body: string }[] = [
  {
    title: "No consent, no call",
    body: "Consent is a gate at import, not a policy in a document. A row that is not marked consented is dropped before it can enter the dial queue, and you see the dropped count with a reason for every row.",
  },
  {
    title: "Opt-out is instant and global",
    body: "“Take me off the list” writes to a do-not-call list shared across every salon we run, before the call report is even accepted. That number is never dialled again, by us, for anyone.",
  },
  {
    title: "One attempt per person, ever",
    body: "Not a retry policy — a condition in the query that picks who to call. There is no second pass, no drip, no next-month list. If the window closes before we reach them, the attempt is given back, not spent.",
  },
  {
    title: "Your hours, not ours",
    body: "The calling window is evaluated in each salon’s own timezone. A timezone we cannot read fails closed: no call goes out at all rather than one going out at the wrong hour.",
  },
  {
    title: "Malone says what it is",
    body: "The disclosure is in the opening line and repeated whenever anyone asks. It never claims to be a person, never argues, and hands anything off-topic back to your front desk number.",
  },
  {
    title: "Voice and email only",
    body: "No SMS, no chatbot, no app for your clients to install. The only two things that ever happen are a phone call to them and an email to you.",
  },
];

export const COUNSEL_NOTE =
  "We are engineers, not your lawyers. Outbound calling is regulated — TCPA in the US and its state analogues, with rules on consent, calling hours, disclosure and do-not-call handling — and what counts as valid consent for a voice call is not obvious from a spreadsheet column named “consent”. The gates above are how we built the system; they are not legal advice and they are not a compliance programme. Have your own counsel review the consent language your clients agreed to before the first list is dialled.";

export const FAQ: { q: string; a: string }[] = [
  {
    q: "Will this annoy my clients?",
    a: "It is built so it cannot become a nuisance. One call per person, ever — no retry queue, no drip, no second pass next month. Ninety seconds is the target and three minutes is a hard stop. A warm no ends the call immediately, with no rebuttal. It only dials inside the calling window, read in your salon’s own timezone — never at 7am, never late. The part that decides whether it is welcome is the offer, and we write that with you before anything dials.",
  },
  {
    q: "Do I need their consent?",
    a: "Yes, and we enforce it rather than trusting it. Your export needs a consent column; rows that do not say yes are dropped at import and never enter the dial queue, and you get the dropped counts with a reason per row. We cannot manufacture consent for you — it has to be consent your clients actually gave your salon. Have your counsel look at the language they agreed to before the first campaign.",
  },
  {
    q: "What if someone asks to be removed?",
    a: "Malone says “done — you’re off the list, be good” and ends the call. That number is written to a global do-not-call list before the call report is accepted, and pulled out of every pending queue we run. If the write ever failed, the report is rejected so it is delivered again — the one thing we will not risk losing is an opt-out. It can never be dialled again, by us, for anyone.",
  },
  {
    q: "Can I hear it before it calls anyone?",
    a: "Yes, and that is how every account starts. The first campaign we run for you is a one-row list: your own mobile, your salon name, your offer. You pick up, you hear exactly what your clients would hear, and the booking email lands in your inbox. Nothing else is dialled until you say go.",
  },
  {
    q: "What if nobody books?",
    a: "You will know by Friday, in writing, with the dial and answer counts behind it. Usually the offer is the problem rather than the list, so we rewrite it and run the remainder. The pilot is $299 once with no auto-renew, and the monthly plans are month to month — cancel and the calling stops that day. We would rather lose a subscription than defend a bad number.",
  },
  {
    q: "Will they know it is not a person?",
    a: "Yes. Malone says it is the salon’s virtual concierge in its opening line, and answers straight away if anyone asks whether it is a bot or a recording. It never claims to be human and it never dodges the question. Anything it cannot handle — prices, anything medical, anything off-topic — goes to your front desk number.",
  },
  {
    q: "How many times will you call one person?",
    a: "Once. Ever. A win-back campaign that pesters people costs you more goodwill than it recovers, so there is no mechanism in the product to call anyone twice.",
  },
  {
    q: "What happens to my client list?",
    a: "It is used to run your campaigns and nothing else. We never sell it, share it, or dial it for another salon. Recordings and transcripts stay with our telephony provider — we store the link, not a copy. Ask us and we delete your list. The full detail is in the privacy notice.",
  },
  {
    q: "Is there texting?",
    a: "No. Voice calls and email only. No SMS, no chatbot, no app for your clients to install.",
  },
];
