import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import SalonPlate from "@/components/SalonPlate";
import { SiteHeader } from "@/components/SiteHeader";
import { callWindow, publicEnv } from "@/lib/env";
import {
  COMPANY,
  COUNSEL_NOTE,
  CTA,
  FAQ,
  MATH_EXAMPLE,
  PLANS,
  SAFEGUARDS,
  SAMPLE_CALL,
  SITE,
  STEPS,
  bookingCallUrl,
  formatClock,
  planLink,
  type Plan,
} from "@/lib/site";

export const metadata: Metadata = {
  // absolute: the root layout's "%s · Salon Malone" template must not double the name
  title: { absolute: `${SITE.name} — ${SITE.tagline}` },
  description: SITE.description,
  alternates: { canonical: "/" },
};

const callUrl = bookingCallUrl();
const pilot = PLANS[0];
const monthly = PLANS.slice(1);

/** The real configured window, printed rather than claimed. */
const CALL_HOURS = callWindow();
const WINDOW_LABEL = `${formatClock(CALL_HOURS.start)} to ${formatClock(CALL_HOURS.end)}`;

const ORG_JSONLD = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: COMPANY.legalName,
  url: publicEnv.appUrl || `https://${SITE.domain}`,
  email: COMPANY.supportEmail,
  telephone: COMPANY.outboundPhone,
  brand: { "@type": "Brand", name: SITE.name, slogan: SITE.tagline },
  address: {
    "@type": "PostalAddress",
    streetAddress: COMPANY.addressStreet,
    addressLocality: COMPANY.addressLocality,
    addressRegion: COMPANY.addressRegion,
    postalCode: COMPANY.postalCode,
    addressCountry: "US",
  },
  contactPoint: [
    {
      "@type": "ContactPoint",
      contactType: "customer support",
      email: COMPANY.supportEmail,
      url: callUrl,
    },
  ],
};

export default function HomePage() {
  return (
    <div className="font-sans">
      <script
        type="application/ld+json"
        // Static, hand-written object — no user input reaches this string.
        dangerouslySetInnerHTML={{ __html: JSON.stringify(ORG_JSONLD) }}
      />

      <SiteHeader />

      {/* the one gradient in the product: cream settling into shell */}
      <section className="bg-[linear-gradient(180deg,var(--color-cream)_0%,var(--color-shell)_100%)]">
        <div className="mx-auto max-w-6xl px-6 pt-16 pb-24 sm:pt-24">
          <div className="grid items-center gap-12 lg:grid-cols-[minmax(0,1.15fr)_minmax(0,0.85fr)] lg:gap-16">
            <div>
              <p className="eyebrow">Win-back campaigns for salons &amp; med spas</p>
              <h1 className="h-display mt-6 text-[clamp(2.6rem,6.5vw,4.75rem)]">{SITE.headline}</h1>
              <p className="prose-tight mt-8 text-[1.0625rem] sm:text-lg">{SITE.subhead}</p>

              <div className="mt-10 flex flex-wrap items-center gap-3">
                <Link className="btn btn-primary" href={CTA.startHref}>
                  {CTA.startLabel}
                </Link>
                <a className="btn btn-ghost" href={callUrl}>
                  {CTA.callLabel}
                </a>
              </div>
              <p className="help mt-4">
                Two minutes, no card.{" "}
                <a className="link" href="#pricing">
                  Already know what you want? Prices and checkout are below.
                </a>
              </p>
            </div>

            {/* Decorative: the headline already says this, so it carries no information a
                screen-reader user would miss. Hidden below lg — on a phone it would push the
                offer and the button below the fold, which is the one thing that must not happen. */}
            <SalonPlate className="hidden lg:block" />
          </div>

          <ul className="mt-14 grid gap-px border-y border-line bg-line sm:grid-cols-3">
            {[
              ["Consent-gated", "No consent flag on the row, no call. Enforced in code at import."],
              ["One attempt, ever", "No retry queue, no drip, no second pass next month."],
              [
                "Opt-out is instant",
                "“Stop calling” writes to a global do-not-call list before the call ends.",
              ],
            ].map(([title, body]) => (
              <li key={title} className="bg-cream px-5 py-6">
                <h2 className="font-display text-base">{title}</h2>
                <p className="help mt-1.5">{body}</p>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* ---------- what it is ---------- */}
      <Section id="what" eyebrow="What this is" title="A concierge for the chairs nobody booked.">
        <div className="mt-8 grid gap-10 md:grid-cols-[1.15fr_1fr] md:items-start">
          <div className="prose-tight">
            <p>
              Every salon has the same quiet asset: a few hundred people who used to come in and
              then, with no argument and no goodbye, stopped. They are not leads. They know your
              name, they liked the work, and life simply got in the way. Nobody calls them, because
              calling them is a day of somebody&rsquo;s life.
            </p>
            <p>
              <strong>Salon Malone makes those calls.</strong> It rings as your salon&rsquo;s virtual
              concierge, says so out loud, makes the one offer you chose, and puts a specific day and
              time on it. You get an email the second someone says yes, and a report every Friday
              with what the week actually recovered.
            </p>
            <p>
              It is one job done properly. There is no dashboard to learn, no chatbot on your
              website, no texting product, and nothing for your clients to install.
            </p>
          </div>

          <div className="card card-pad">
            <p className="eyebrow">What you actually get</p>
            <ul className="mt-4 grid gap-2.5">
              <FeatureItem>A written offer, agreed with you before anything dials</FeatureItem>
              <FeatureItem>A scrub report: who was dropped, and why, per row</FeatureItem>
              <FeatureItem>Calls inside your hours, in your salon&rsquo;s local time</FeatureItem>
              <FeatureItem>A booking email the moment a slot is agreed</FeatureItem>
              <FeatureItem>A Friday report: dialled, reached, booked, opted out</FeatureItem>
              <FeatureItem>A global do-not-call list, managed for you</FeatureItem>
            </ul>
            <hr className="rule my-5" />
            <p className="help">
              Zero customers so far — this is a new product from {COMPANY.legalName}, and you would
              be early. Everything on this page is either what the software does or arithmetic
              labelled as an example.
            </p>
          </div>
        </div>
      </Section>

      {/* ---------- how it works ---------- */}
      <Section id="how" eyebrow="How it runs" title="Six steps, then it is quiet.">
        <ol className="mt-12 grid gap-x-12 gap-y-10 sm:grid-cols-2">
          {STEPS.map((s) => (
            <li key={s.n} className="border-t border-line pt-5">
              <span className="font-display text-2xl text-brass">{s.n}</span>
              <h3 className="mt-2 text-xl">{s.title}</h3>
              <p className="prose-tight mt-2 text-[0.9375rem]">{s.body}</p>
            </li>
          ))}
        </ol>

        <div className="mt-12 flex flex-wrap items-center gap-3">
          <Link className="btn btn-primary" href={CTA.startHref}>
            {CTA.startLabel}
          </Link>
          <a className="btn btn-ghost" href="#call">
            First, hear what it says
          </a>
        </div>
      </Section>

      {/* ---------- what the call sounds like ---------- */}
      <Section
        id="call"
        eyebrow="The call"
        title="What Malone actually says."
        lead="Ninety seconds is the target and three minutes is a hard ceiling. It opens honest, makes one offer, names two concrete times, and takes the first yes."
      >
        <div className="mt-10 grid gap-8 lg:grid-cols-[1.25fr_1fr] lg:items-start">
          <div className="card overflow-hidden">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-line px-6 py-4">
              <h3 className="text-lg">Example script</h3>
              <span className="badge badge-mute">Example — not a recording</span>
            </div>

            <div className="px-6 py-7">
              {SAMPLE_CALL.lines.map((line, i) => (
                <div key={i} className={line.agent ? "say say-agent" : "say"}>
                  <p className="say-who">{line.who}</p>
                  <p className="say-line">{line.text}</p>
                </div>
              ))}
            </div>

            <p className="help border-t border-line bg-cream px-6 py-4">{SAMPLE_CALL.disclaimer}</p>
          </div>

          <div className="grid gap-4">
            {SAMPLE_CALL.branches.map((b) => (
              <div key={b.when} className="card card-pad">
                <p className="eyebrow">{b.when}</p>
                <p className="mt-3 font-display text-[1.0625rem] leading-snug text-ink">
                  &ldquo;{b.line}&rdquo;
                </p>
                <p className="help mt-2.5">{b.then}</p>
              </div>
            ))}
          </div>
        </div>
      </Section>

      {/* ---------- mid-page conversion band ---------- */}
      <section className="border-t border-line bg-shell">
        <div className="mx-auto flex max-w-6xl flex-col gap-8 px-6 py-16 md:flex-row md:items-center md:justify-between">
          <div className="max-w-xl">
            <p className="eyebrow">Before your clients hear it</p>
            <h2 className="h-display mt-4 text-[clamp(1.7rem,4vw,2.5rem)]">
              The first call any account makes is to you.
            </h2>
            <p className="prose-tight mt-4 text-[0.9375rem]">
              One row, your own mobile, your salon name, your offer. Pick up and hear exactly what
              your clients would hear, then read the booking email it sends you. Nothing else is
              dialled until you say go.
            </p>
          </div>
          <div className="flex shrink-0 flex-wrap gap-3">
            <Link className="btn btn-primary" href={CTA.startHref}>
              {CTA.startLabel}
            </Link>
            <a className="btn btn-ghost" href={callUrl}>
              {CTA.callLabel}
            </a>
          </div>
        </div>
      </section>

      {/* ---------- the arithmetic ---------- */}
      <Section
        id="math"
        eyebrow="The arithmetic"
        title="Empty chairs, priced honestly."
        lead={MATH_EXAMPLE.premise}
      >
        <div className="card mt-10 overflow-hidden">
          <div className="flex items-center justify-between gap-4 border-b border-line px-6 py-4">
            <h3 className="text-lg">Worked example</h3>
            <span className="badge badge-mute">Illustrative — not a customer result</span>
          </div>
          <div className="overflow-x-auto px-3 py-4 sm:px-6">
            <table className="table">
              <thead>
                <tr>
                  <th>Step</th>
                  <th className="text-right">Count</th>
                  <th>Assumption</th>
                </tr>
              </thead>
              <tbody>
                {MATH_EXAMPLE.rows.map((r, i) => {
                  const last = i === MATH_EXAMPLE.rows.length - 1;
                  return (
                    <tr key={r.label}>
                      <td className={last ? "text-ink" : undefined}>{r.label}</td>
                      <td
                        className={`text-right font-display text-lg tabular-nums ${
                          last ? "text-brass-deep" : "text-ink"
                        }`}
                      >
                        {r.value}
                      </td>
                      <td className="text-ink-mute">{r.note}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          <p className="help border-t border-line bg-cream px-6 py-4">{MATH_EXAMPLE.footnote}</p>
        </div>

        <div className="mt-10 grid gap-6 sm:grid-cols-2">
          <div className="card card-pad">
            <p className="eyebrow">The moment it happens</p>
            <h3 className="mt-3 text-xl">A booking email</h3>
            <p className="prose-tight mt-2 text-[0.9375rem]">
              Name, number, the exact slot they asked for, and a two-line summary of the call. Sent
              the second the booking is captured, so the front desk can confirm it while the chair is
              still open.
            </p>
          </div>
          <div className="card card-pad">
            <p className="eyebrow">Every Friday</p>
            <h3 className="mt-3 text-xl">The recovered-revenue report</h3>
            <p className="prose-tight mt-2 text-[0.9375rem]">
              Dialled, reached, booked, declined, opted out, and recovered revenue at your average
              ticket. One page. No dashboard to log into, no chart to interpret.
            </p>
          </div>
        </div>
      </Section>

      {/* ---------- pricing ---------- */}
      <Section id="pricing" eyebrow="Pricing" title="Start small. The list will tell you the rest.">
        <div className="callout callout-tint mt-8 max-w-3xl">
          <span className="callout-title">Not sure which one yet?</span>
          <p>
            You do not have to guess.{" "}
            <Link className="link" href={CTA.startHref}>
              Start your campaign
            </Link>{" "}
            and the form reads your list size and your ticket back to you with the plan that fits
            and why it fits — no card, and the other three stay one click away. Checkout below is
            the shortcut for people who already know.
          </p>
        </div>

        <div className="card mt-8 flex flex-col gap-8 border-brass/40 p-6 sm:p-8 md:flex-row md:items-center">
          <div className="md:flex-1">
            <div className="flex flex-wrap items-baseline gap-3">
              <h3 className="font-display text-2xl">{pilot.name}</h3>
              <span className="badge badge-warn">Start here</span>
            </div>
            <p className="prose-tight mt-3 text-[0.9375rem]">{pilot.blurb}</p>
            <ul className="mt-4 grid gap-1.5 sm:grid-cols-2">
              {pilot.features.map((f) => (
                <FeatureItem key={f}>{f}</FeatureItem>
              ))}
            </ul>
          </div>
          <div className="shrink-0 md:w-56 md:border-l md:border-line md:pl-8">
            <p className="font-display text-4xl leading-none">{pilot.priceLabel}</p>
            <p className="stat-label mt-2">{pilot.cadence}</p>
            <div className="mt-5">
              <PlanCta plan={pilot} />
            </div>
          </div>
        </div>

        <div className="mt-6 grid gap-6 md:grid-cols-3">
          {monthly.map((p) => (
            <div
              key={p.id}
              className={`card card-pad flex flex-col ${p.highlight ? "border-brass/50" : ""}`}
            >
              <div className="flex items-baseline justify-between gap-3">
                <h3 className="font-display text-xl">{p.name}</h3>
                {/* honest recommendation, not a popularity statistic — no invented social proof */}
                {p.highlight ? <span className="badge badge-ok">Our default</span> : null}
              </div>
              <p className="mt-4 font-display text-3xl leading-none">{p.priceLabel}</p>
              <p className="stat-label mt-2">{p.cadence}</p>
              <p className="help mt-4">{p.blurb}</p>
              <ul className="mt-5 grid flex-1 gap-1.5">
                {p.features.map((f) => (
                  <FeatureItem key={f}>{f}</FeatureItem>
                ))}
              </ul>
              <div className="mt-6">
                <PlanCta plan={p} />
              </div>
            </div>
          ))}
        </div>

        <p className="help mt-6 max-w-3xl">
          Monthly plans are month to month — cancel and the calling stops that day. The pilot is one
          payment with no auto-renew. Voice and email only; there is no SMS product to buy. Prefer to
          talk it through first?{" "}
          <a className="link" href={callUrl}>
            Book a 15-minute call
          </a>
          .
        </p>
      </Section>

      {/* ---------- legal / safe ---------- */}
      <Section
        id="safe"
        eyebrow={"Legal & safe"}
        title="The rules are in the code, not in a policy document."
        lead={`Six things the system will not do, each enforced where the call is actually placed. The calling window running today is ${WINDOW_LABEL}, read in your salon’s own timezone — and it is yours to narrow.`}
      >
        <ul className="mt-10 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {SAFEGUARDS.map((s) => (
            <li key={s.title} className="card card-pad">
              <h3 className="text-lg">{s.title}</h3>
              <p className="help mt-2.5">{s.body}</p>
            </li>
          ))}
        </ul>

        <div className="callout mt-8 max-w-3xl">
          <span className="callout-title">Read this part twice</span>
          <p>{COUNSEL_NOTE}</p>
          <p>
            <Link className="link" href="/terms">
              Terms of service
            </Link>{" "}
            ·{" "}
            <Link className="link" href="/privacy">
              What we do with your list
            </Link>
          </p>
        </div>
      </Section>

      {/* ---------- objections ---------- */}
      <Section id="faq" eyebrow="Straight answers" title="The questions that actually decide it.">
        <dl className="mt-10 max-w-3xl">
          {FAQ.map((item) => (
            <div key={item.q} className="border-t border-line py-6">
              <dt className="font-display text-xl">{item.q}</dt>
              <dd className="prose-tight mt-2 text-[0.9375rem]">{item.a}</dd>
            </div>
          ))}
        </dl>
        <p className="help mt-8 max-w-3xl">
          Something not answered here? Write to{" "}
          <a className="link" href={`mailto:${COMPANY.supportEmail}`}>
            {COMPANY.supportEmail}
          </a>{" "}
          and a person replies.
        </p>
      </Section>

      {/* ---------- closing band ---------- */}
      <section className="border-t border-line bg-shell">
        <div className="mx-auto flex max-w-6xl flex-col gap-8 px-6 py-20 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="eyebrow">What happens next</p>
            <h2 className="h-display mt-4 max-w-xl text-[clamp(1.9rem,4.5vw,3rem)]">
              Bring the list. We&rsquo;ll tell you what is in it.
            </h2>
            <p className="prose-tight mt-4 max-w-md text-[0.9375rem]">
              Answer a few questions about your salon, the clients who drifted, and the offer you
              want Malone to make. The plan that fits comes back straight away; we come back on the
              offer itself, and on whether a win-back campaign is worth running for your chairs.
            </p>
          </div>
          <div className="flex shrink-0 flex-col items-start gap-3">
            <Link className="btn btn-primary" href={CTA.startHref}>
              {CTA.startLabel}
            </Link>
            <a className="btn btn-ghost" href={callUrl}>
              {CTA.callLabel}
            </a>
            <a className="help link" href={`mailto:${COMPANY.supportEmail}`}>
              Or just email us: {COMPANY.supportEmail}
            </a>
          </div>
        </div>
      </section>

      <SiteFooter />
    </div>
  );
}

function Section({
  id,
  eyebrow,
  title,
  lead,
  children,
}: {
  id: string;
  eyebrow: string;
  title: string;
  lead?: string;
  children: React.ReactNode;
}) {
  return (
    <section id={id} className="anchor-target border-t border-line">
      <div className="mx-auto max-w-6xl px-6 py-20 sm:py-24">
        <p className="eyebrow">{eyebrow}</p>
        <h2 className="h-display mt-4 max-w-2xl text-[clamp(1.9rem,4.5vw,3rem)]">{title}</h2>
        {lead ? <p className="prose-tight mt-5">{lead}</p> : null}
        {children}
      </div>
    </section>
  );
}

function FeatureItem({ children }: { children: React.ReactNode }) {
  return (
    <li className="flex gap-2.5 text-[0.875rem] leading-relaxed text-ink-soft">
      <span aria-hidden className="mt-2 h-px w-3 shrink-0 bg-brass" />
      <span>{children}</span>
    </li>
  );
}

/**
 * Checkout is the express lane, so it is the button. A plan whose payment link is not live
 * falls back to /start rather than a dead '#': the conversion path must never end in nothing.
 */
function PlanCta({ plan }: { plan: Plan }) {
  const href = planLink(plan);

  if (href === "#") {
    return (
      <div className="grid gap-2">
        <Link className="btn btn-primary w-full" href={CTA.startHref}>
          {CTA.startLabelShort}
        </Link>
        <span className="help">Checkout for this plan opens shortly — we send the link.</span>
      </div>
    );
  }

  const label = plan.id === "pilot" ? `Start the ${plan.priceLabel} pilot` : `Choose ${plan.name}`;

  return (
    <div className="grid gap-2">
      <a className="btn btn-primary w-full" href={href}>
        {label}
      </a>
      <Link className="help link text-center" href={CTA.startHref}>
        or start with the questions
      </Link>
    </div>
  );
}
