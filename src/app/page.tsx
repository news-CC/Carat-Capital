import type { Metadata } from "next";
import Link from "next/link";
import { FAQ, MATH_EXAMPLE, PLANS, SITE, STEPS, bookingCallUrl, planLink, type Plan } from "@/lib/site";

export const metadata: Metadata = {
  // absolute: the root layout's "%s · Salon Malone" template must not double the name
  title: { absolute: `${SITE.name} — ${SITE.tagline}` },
  description: SITE.description,
  alternates: { canonical: "/" },
};

const callUrl = bookingCallUrl();
const pilot = PLANS[0];
const monthly = PLANS.slice(1);

export default function HomePage() {
  const pilotLink = planLink(pilot);
  const heroHref = pilotLink === "#" ? callUrl : pilotLink;
  const heroLabel = pilotLink === "#" ? "Book a 15-minute call" : `Start the ${pilot.priceLabel} pilot`;

  return (
    <div className="font-sans">
      <SiteHeader />

      {/* the one gradient in the product: cream settling into shell */}
      <section className="bg-[linear-gradient(180deg,var(--color-cream)_0%,var(--color-shell)_100%)]">
        <div className="mx-auto max-w-6xl px-6 pt-20 pb-24 sm:pt-28">
          <p className="eyebrow">Win-back campaigns for salons &amp; med spas</p>
          <h1 className="h-display mt-6 max-w-4xl text-[clamp(2.6rem,7.5vw,5.25rem)]">
            {SITE.headline}
          </h1>
          <p className="prose-tight mt-8 text-[1.0625rem] sm:text-lg">{SITE.subhead}</p>

          <div className="mt-10 flex flex-wrap items-center gap-3">
            <a className="btn btn-primary" href={heroHref}>
              {heroLabel}
            </a>
            <a className="btn btn-ghost" href="#math">
              See the arithmetic
            </a>
          </div>

          <ul className="mt-14 grid gap-px border-y border-line bg-line sm:grid-cols-3">
            {[
              ["Consent-gated", "No consent flag on the row, no call. Enforced in code at import."],
              ["One attempt, ever", "No retry queue, no drip, no second pass next month."],
              ["Opt-out is instant", "“Stop calling” writes to a global do-not-call list before the call ends."],
            ].map(([title, body]) => (
              <li key={title} className="bg-cream px-5 py-6">
                <h2 className="font-display text-base">{title}</h2>
                <p className="help mt-1.5">{body}</p>
              </li>
            ))}
          </ul>
        </div>
      </section>

      <Section id="how" eyebrow="How it runs" title="Five steps, then it is quiet.">
        <ol className="mt-12 grid gap-x-12 gap-y-10 sm:grid-cols-2">
          {STEPS.map((s) => (
            <li key={s.n} className="border-t border-line pt-5">
              <span className="font-display text-2xl text-brass">{s.n}</span>
              <h3 className="mt-2 text-xl">{s.title}</h3>
              <p className="prose-tight mt-2 text-[0.9375rem]">{s.body}</p>
            </li>
          ))}
        </ol>
      </Section>

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
              Name, number, the exact slot they asked for, and a two-line summary of the call. Sent the
              second the booking is captured, so the front desk can confirm it while the chair is still
              open.
            </p>
          </div>
          <div className="card card-pad">
            <p className="eyebrow">Every Friday, 4pm</p>
            <h3 className="mt-3 text-xl">The recovered-revenue report</h3>
            <p className="prose-tight mt-2 text-[0.9375rem]">
              Dialled, reached, booked, declined, opted out, and recovered revenue at your average
              ticket. One page. No dashboard to log into, no chart to interpret.
            </p>
          </div>
        </div>
      </Section>

      <Section id="pricing" eyebrow="Pricing" title="Start small. The list will tell you the rest.">
        <div className="card mt-10 flex flex-col gap-8 border-brass/40 p-6 sm:p-8 md:flex-row md:items-center">
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

        <p className="help mt-6">
          Monthly plans are month to month — cancel and the calling stops that day. Voice and email
          only; there is no SMS product to buy.
        </p>
      </Section>

      <Section id="faq" eyebrow="Straight answers" title="The questions that actually decide it.">
        <dl className="mt-10 max-w-3xl">
          {FAQ.map((item) => (
            <div key={item.q} className="border-t border-line py-6">
              <dt className="font-display text-xl">{item.q}</dt>
              <dd className="prose-tight mt-2 text-[0.9375rem]">{item.a}</dd>
            </div>
          ))}
        </dl>
      </Section>

      <section className="bg-shell">
        <div className="mx-auto flex max-w-6xl flex-col gap-6 px-6 py-20 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="eyebrow">One conversation</p>
            <h2 className="h-display mt-4 max-w-xl text-[clamp(1.9rem,4.5vw,3rem)]">
              Bring the list. We&rsquo;ll tell you what is in it.
            </h2>
            <p className="help mt-4 max-w-md">
              Fifteen minutes, your export, and an honest read on whether a win-back campaign is worth
              running for your chairs.
            </p>
          </div>
          <a className="btn btn-primary self-start md:self-auto" href={callUrl}>
            Book a 15-minute call
          </a>
        </div>
      </section>

      <SiteFooter />
    </div>
  );
}

function SiteHeader() {
  return (
    <header className="border-b border-line bg-cream">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-6 px-6 py-4">
        <span className="font-display text-lg tracking-tight">
          {SITE.name}
          <span className="text-brass">.</span>
        </span>
        <nav className="hidden items-center gap-7 text-[0.8125rem] text-ink-soft sm:flex">
          <a className="transition-opacity duration-150 hover:opacity-60" href="#how">
            How it runs
          </a>
          <a className="transition-opacity duration-150 hover:opacity-60" href="#math">
            Arithmetic
          </a>
          <a className="transition-opacity duration-150 hover:opacity-60" href="#pricing">
            Pricing
          </a>
          <a className="transition-opacity duration-150 hover:opacity-60" href="#faq">
            FAQ
          </a>
        </nav>
        <a className="btn btn-ghost btn-sm" href={callUrl}>
          Book a call
        </a>
      </div>
    </header>
  );
}

function SiteFooter() {
  return (
    <footer className="border-t border-line bg-cream">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <div className="flex flex-wrap items-baseline justify-between gap-4">
          <span className="font-display text-base">
            {SITE.name}
            <span className="text-brass">.</span>
          </span>
          <div className="flex items-center gap-6 text-[0.8125rem] text-ink-soft">
            <a className="transition-opacity duration-150 hover:opacity-60" href={callUrl}>
              Book a call
            </a>
            <Link className="transition-opacity duration-150 hover:opacity-60" href="/login">
              Operator login
            </Link>
          </div>
        </div>
        <hr className="rule my-8" />
        <p className="help max-w-3xl">{SITE.complianceLine}</p>
        <p className="help mt-4">
          {SITE.domain} · © {new Date().getFullYear()} · All figures on this page are illustrative
          arithmetic, not customer results.
        </p>
      </div>
    </footer>
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
    <section id={id} className="scroll-mt-16 border-t border-line">
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

/** A missing payment link is softened, never shipped as a live-looking dead '#'. */
function PlanCta({ plan }: { plan: Plan }) {
  const href = planLink(plan);

  if (href === "#") {
    return (
      <div className="grid gap-2">
        <span className="btn btn-primary w-full" aria-disabled="true">
          Checkout opening shortly
        </span>
        <a className="help underline decoration-line underline-offset-4" href={callUrl}>
          Book a call and we&rsquo;ll send the link
        </a>
      </div>
    );
  }

  return (
    <a className="btn btn-primary w-full" href={href}>
      Choose {plan.name}
    </a>
  );
}
