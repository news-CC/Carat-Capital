/**
 * Marketing copy + pricing config for startup25.com.
 * Pure data — safe to import from client components.
 */

export const SITE = {
  name: "Salon Malone",
  domain: "startup25.com",
  tagline: "Win back the clients who stopped coming.",
  headline: "Your dead client list is buried money.",
  // Every claim here has to be one the shipped product delivers: the Friday email counts booked
  // visits at the average ticket and says so, and the money is a $299 one-time pilot plus flat
  // monthly tiers. No pay-per-show claim — nothing in the product records a show.
  subhead:
    "Salon Malone is the virtual concierge that phones the clients who quietly stopped booking, offers them a specific time, and emails you the moment one says yes. Start on a $299 pilot or a flat monthly plan — no per-minute billing, no per-lead invoices. Friday's number is the visits Malone booked at your average ticket, no-shows included, so your own book has the last word.",
  description:
    "Salon Malone calls your lapsed salon or med spa clients as your virtual concierge, books them back into empty chairs, emails you the instant a booking lands, and sends a Friday report with estimated recovered revenue from the visits it booked. Consent-gated, opt-out instant. Voice and email only.",
  contactEmail: "hello@startup25.com",
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

/** Book-a-call link, falling back to email so the CTA is never dead. */
export function bookingCallUrl(): string {
  const url = process.env.NEXT_PUBLIC_BOOKING_CALL_URL?.trim();
  return url && /^https:\/\//i.test(url)
    ? url
    : `mailto:${SITE.contactEmail}?subject=${encodeURIComponent("Win-back call — Salon Malone")}`;
}

export const STEPS: { n: string; title: string; body: string }[] = [
  {
    n: "01",
    title: "Send us the list",
    body: "Export the clients who have not booked in six months. CSV or XLSX, whatever your software spits out. We map the columns for you.",
  },
  {
    n: "02",
    title: "We scrub it before anyone rings",
    body: "Rows without consent are dropped. Bad numbers are dropped. Anyone on the do-not-call list is dropped. You see the counts for every reason before a single call goes out.",
  },
  {
    n: "03",
    title: "Malone calls, inside your hours",
    body: "One attempt per person, ever, in your salon's local time. Malone opens by saying it is a virtual concierge, offers two concrete times, and takes the first yes.",
  },
  {
    n: "04",
    title: "You get the email immediately",
    body: "Name, phone, the slot they asked for, and what was said. It lands while the chair is still open, so your front desk can confirm it the same hour.",
  },
  {
    n: "05",
    title: "Friday, the arithmetic",
    body: "One email: dialled, reached, booked, opted out, and recovered revenue at your average ticket. If the number is bad, you will see it on Friday, not in six months.",
  },
];

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

export const FAQ: { q: string; a: string }[] = [
  {
    q: "Do you call people who never agreed to be contacted?",
    a: "No. Consent is a hard gate in the code, not a policy in a document. If a row is not marked consented in the list you upload, it is dropped at import and never enters the dial queue. You can see the dropped count for every campaign.",
  },
  {
    q: "What happens when someone says stop?",
    a: "Malone says 'done, you're off the list' and ends the call. Before the webhook finishes, that number is written to a global do-not-call list shared across every client we run. It can never be dialled again, by us, for anyone.",
  },
  {
    q: "What does the call actually sound like?",
    a: "Warm, quick, and honest about what it is. A sample opening — the names are placeholders, the salon name and offer are yours: \"Hey Dana — Salon Malone here, Ridgeline Hair's virtual concierge. Ninety seconds, I promise. We miss you.\" Then one offer, two concrete times, and it takes the answer. Ninety seconds is the target, three minutes is the hard stop. It never claims to be a person and it never argues.",
  },
  {
    q: "How many times will you call one person?",
    a: "Once. Ever. There is no retry queue, no drip, no second pass next month. A win-back campaign that pesters people costs you more goodwill than it recovers.",
  },
  {
    q: "What if nobody books?",
    a: "You will know by Friday, in writing, with the dial and answer counts behind it. Usually the offer is the problem, not the list, so we rewrite it and run the remainder. The monthly plans are month to month — cancel and the calling stops that day. We would rather lose a subscription than defend a bad number.",
  },
  {
    q: "Is there texting?",
    a: "No. Voice calls and email only. No SMS, no chatbot, no app for your clients to install.",
  },
];
