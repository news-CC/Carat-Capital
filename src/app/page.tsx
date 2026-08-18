import type { Metadata } from "next";
import Link from "next/link";
import localFont from "next/font/local";
import LandingEngine from "@/components/landing/LandingEngine";
import { callWindow, publicEnv } from "@/lib/env";
import {
  COMPANY,
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
import "./landing.css";

/* Self-hosted so the build never depends on a font CDN. */
const archivo = localFont({
  src: [
    { path: "../fonts/Archivo-400-normal.woff2", weight: "400", style: "normal" },
    { path: "../fonts/Archivo-500-normal.woff2", weight: "500", style: "normal" },
    { path: "../fonts/Archivo-600-normal.woff2", weight: "600", style: "normal" },
  ],
  variable: "--font-archivo",
  display: "swap",
});
const instrument = localFont({
  src: [{ path: "../fonts/InstrumentSerif-400-italic.woff2", weight: "400", style: "italic" }],
  variable: "--font-instrument",
  display: "swap",
});

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
/** "9:00 AM" → "9AM" for the hero stat cell. */
const shortClock = (hhmm: string) => formatClock(hhmm).replace(":00", "").replace(" ", "");

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

/** Enforcement point for each safeguard, in SAFEGUARDS order. */
const SAFE_TAGS = ["Gate at import", "Mid-call write", "In the claim query", "Fails closed", "Opening line", "Nothing else exists"];

/** Funnel rows: the count rows of the worked example, widths relative to the first. */
const FUNNEL_ROWS = MATH_EXAMPLE.rows.slice(0, 5).map((r, i, all) => {
  const count = parseInt(r.value.replace(/[^0-9]/g, ""), 10);
  const first = parseInt(all[0].value.replace(/[^0-9]/g, ""), 10);
  return { label: `${r.label} — ${r.note}`, value: r.value, count, width: Math.max((count / first) * 100, 1.8), delay: i * 0.12 };
});

export default function HomePage() {
  return (
    <div className={`landing-root ${archivo.variable} ${instrument.variable}`}>
      <script
        type="application/ld+json"
        // Static, hand-written object — no user input reaches this string.
        dangerouslySetInnerHTML={{ __html: JSON.stringify(ORG_JSONLD) }}
      />

      <LandingEngine />

      <nav className="lnav" aria-label="Main">
        <div className="lnav-l">
          <a className="lnav-link" href="#call">The call</a>
          <a className="lnav-link" href="#how">How it runs</a>
          <a className="lnav-link" href="#math">The math</a>
        </div>
        <a className="lbrand" href="#top">{SITE.name}</a>
        <div className="lnav-r">
          <a className="lnav-link" href="#pricing">Pricing</a>
          <a className="lnav-link" href="#faq">FAQ</a>
          <Link className="lnav-cta" href={CTA.startHref}>Start a campaign</Link>
        </div>
      </nav>

      <main id="top">
        {/* ================= HERO ================= */}
        <section className="scene" id="hero" data-scene="hero">
          <div className="scene-inner">
            <div className="hero-stage lon">
              <div className="hero-tl">
                <h1 className="lcaps h-mega">
                  <span className="rise"><span style={{ ["--d" as string]: ".15s" }}>Your dead</span></span>
                  <span className="rise"><span style={{ ["--d" as string]: ".27s" }}>client list</span></span>
                </h1>
              </div>
              <div className="hero-br">
                <p className="lcaps h-mega">
                  <span className="rise"><span style={{ ["--d" as string]: ".42s" }}>is buried</span></span>
                  <span className="rise"><span style={{ ["--d" as string]: ".54s" }}>money.</span></span>
                </p>
                <Link className="hero-cta lfade" style={{ ["--d" as string]: ".9s" }} href={CTA.startHref}>
                  {CTA.startLabel} &nbsp;&rarr;
                </Link>
              </div>
              <div className="hero-bl">
                <p className="lmicro lfade" style={{ ["--d" as string]: ".75s" }}>
                  A virtual concierge that phones the clients who quietly stopped booking — and says so out
                  loud. You approve the offer before anything dials.
                </p>
                <div className="stats-strip lfade" style={{ ["--d" as string]: ".9s" }}>
                  <div className="cell"><p className="num">90 sec</p><p className="lbl">Target call</p></div>
                  <div className="cell"><p className="num">1</p><p className="lbl">Attempt, ever</p></div>
                  <div className="cell">
                    <p className="num">{shortClock(CALL_HOURS.start)}–{shortClock(CALL_HOURS.end)}</p>
                    <p className="lbl">Local hours</p>
                  </div>
                </div>
              </div>
              <div className="scroll-cue lfade" style={{ ["--d" as string]: "1.3s" }}>
                <span className="lmicro" style={{ letterSpacing: ".28em" }}>Scroll</span>
                <span className="stem" />
              </div>
            </div>
          </div>
        </section>

        {/* ================= THE CALL ================= */}
        <section className="scene" id="call" data-scene="call">
          <div className="scene-inner">
            <div className="sec-right" data-reveal>
              <p className="lmicro kick lfade"><span>The call</span><span className="tick" /></p>
              <h2 className="lcaps h-big">
                <span className="rise"><span>What Malone</span></span>
                <span className="rise"><span style={{ ["--d" as string]: ".12s" }}>actually says</span></span>
              </h2>
              <p className="body-s sec-para lfade" style={{ ["--d" as string]: ".25s" }}>
                It opens honest, makes one offer, names two concrete times, and takes the first yes. Ninety
                seconds is the target — a warm no ends the call with no rebuttal.
              </p>
            </div>

            <div className="call-grid">
              <div className="transcript lglass" id="transcript" data-reveal>
                <div className="tr-top">
                  <div className="tr-id">
                    <span className="tr-avatar lglass">m</span>
                    <div>
                      <p className="tr-name">{SITE.name}</p>
                      <p className="tr-sub"><span className="live-dot" /> calling for {SAMPLE_CALL.salon}</p>
                    </div>
                  </div>
                  <span className="tr-timer" id="call-timer">0:00</span>
                </div>
                <div className="chat" id="chat" aria-label="Example call script" />
                <div className="tr-note">
                  <span>Example script — not a recording. Salon, client and offer invented for this page.</span>
                  <button className="replay lglass" id="replay" type="button" aria-label="Replay the example call">
                    Replay
                  </button>
                </div>
              </div>

              <div className="branches" data-reveal>
                {SAMPLE_CALL.branches.map((b, i) => (
                  <div className="branch" key={b.when}>
                    <p className="bw lfade">{b.when}</p>
                    <p className="bq lfade" style={{ ["--d" as string]: ".1s" }}>&ldquo;{b.line}&rdquo;</p>
                    <p className="body-s bt lfade" style={{ ["--d" as string]: ".18s" }}>{b.then}</p>
                    <div className="ltags lfade" style={{ ["--d" as string]: ".26s" }}>
                      {i === 0 && (<><span className="ltag lglass">No rebuttal</span><span className="ltag lglass">Never re-dialled</span></>)}
                      {i === 1 && (<><span className="ltag lglass">Global do-not-call</span><span className="ltag lglass">Before the call ends</span></>)}
                      {i === 2 && (<><span className="ltag lglass">15 seconds</span><span className="ltag lglass">No call back</span></>)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* ================= INTERLUDE ================= */}
        <section className="scene inter" id="vow" data-scene="vow">
          <div className="scene-inner">
            <div className="inter-stage" data-reveal>
              <div className="inter-word wl"><p className="lcaps h-mega"><span className="rise"><span>Lapsed</span></span></p></div>
              <div className="inter-word wr"><p className="lcaps h-mega"><span className="rise"><span style={{ ["--d" as string]: ".15s" }}>Rebooked</span></span></p></div>
              <div className="inter-chips lfade" style={{ ["--d" as string]: ".3s" }}>
                <span className="ltag lglass">Consent-gated</span>
                <span className="ltag lglass">One attempt, ever</span>
                <span className="ltag lglass">Local hours only</span>
                <span className="ltag lglass">Opt-out instant</span>
              </div>
              <p className="lmicro inter-note lfade" style={{ ["--d" as string]: ".45s" }}>
                Built so it cannot become a nuisance — the part that decides whether it is welcome is the
                offer, and you write that with us.
              </p>
            </div>
          </div>
        </section>

        {/* ================= HOW IT RUNS ================= */}
        <section className="scene" id="how" data-scene="how">
          <div className="scene-inner">
            <div className="sec-right" data-reveal>
              <p className="lmicro kick lfade"><span>How it runs</span><span className="tick" /></p>
              <h2 className="lcaps h-big">
                <span className="rise"><span>Six steps,</span></span>
                <span className="rise"><span style={{ ["--d" as string]: ".12s" }}>then it is quiet</span></span>
              </h2>
              <p className="body-s sec-para lfade" style={{ ["--d" as string]: ".25s" }}>
                Upload, scrub, dial, book, report. There is no dashboard to learn and nothing for your
                clients to install.
              </p>
            </div>

            <div className="lsteps" data-reveal>
              {STEPS.map((s, i) => (
                <div className="lstep lfade" style={{ ["--d" as string]: `${i * 0.08}s` }} key={s.n}>
                  <p className="n">{s.n}</p>
                  <h3>{s.title}</h3>
                  <p>{s.body}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ================= THE MATH ================= */}
        <section className="scene" id="math" data-scene="math">
          <div className="scene-inner">
            <div className="sec-left" data-reveal>
              <p className="lmicro kick lfade"><span>The arithmetic</span><span className="tick" /></p>
              <h2 className="lcaps h-big">
                <span className="rise"><span>Empty chairs,</span></span>
                <span className="rise"><span style={{ ["--d" as string]: ".12s" }}>priced honestly</span></span>
              </h2>
              <p className="body-s sec-para lfade" style={{ ["--d" as string]: ".25s" }}>{MATH_EXAMPLE.premise}</p>
            </div>

            <div className="funnel" id="funnel" data-reveal>
              {FUNNEL_ROWS.map((r) => (
                <div className="frow" key={r.label}>
                  <p className="fl">{r.label}</p>
                  <div className="track">
                    <div className="bar" data-w={r.width.toFixed(1)} style={{ ["--d" as string]: `${r.delay}s` }} />
                  </div>
                  <p className="fn" data-count={r.count}>{r.value}</p>
                </div>
              ))}
            </div>

            <div className="math-results" data-reveal>
              <div className="result lglass lfade">
                <p className="rn">$3,720</p>
                <p className="body-s rl">
                  Booked visits at your ticket — 31&nbsp;&times;&nbsp;$120. This is the number our Friday
                  email reports; $3,000 is the same month if only 25 of them show.
                </p>
              </div>
              <div className="result lglass lfade" style={{ ["--d" as string]: ".12s" }}>
                <p className="rn">$399</p>
                <p className="body-s rl">
                  The month of the Salon plan that made the calls. Your list, your offer and your show rate
                  move every line — up or down.
                </p>
              </div>
            </div>

            <div data-reveal>
              <span className="ltag lglass badge-line lfade">Illustrative — not a customer result</span>
              <p className="lfootnote lfade" style={{ ["--d" as string]: ".1s" }}>
                Two numbers on purpose: no-shows count in ours, so your book is the last word. We report the
                real figures every Friday — dialled, reached, booked, opted out — not this example.
              </p>
            </div>

            <div className="after" data-reveal>
              <div className="after-item lfade">
                <p className="aw">The moment it happens</p>
                <h3 className="lcaps">A booking email</h3>
                <p className="body-s">
                  Name, number, the exact slot they asked for, and a two-line summary of the call — sent the
                  second the booking is captured.
                </p>
              </div>
              <div className="after-item lfade" style={{ ["--d" as string]: ".12s" }}>
                <p className="aw">Every Friday</p>
                <h3 className="lcaps">The recovered-revenue report</h3>
                <p className="body-s">
                  One page: dialled, reached, booked, declined, opted out, and recovered revenue at your
                  average ticket. No dashboard to log into.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* ================= SAFEGUARDS ================= */}
        <section className="scene" id="safe" data-scene="safe">
          <div className="scene-inner">
            <div className="sec-left" data-reveal>
              <p className="lmicro kick lfade"><span>Legal &amp; safe</span><span className="tick" /></p>
              <h2 className="lcaps h-big">
                <span className="rise"><span>The rules are</span></span>
                <span className="rise"><span style={{ ["--d" as string]: ".12s" }}>in the code</span></span>
              </h2>
              <p className="body-s sec-para lfade" style={{ ["--d" as string]: ".25s" }}>
                Six things the system will not do — each one enforced where the call is actually placed. The
                calling window running today is {WINDOW_LABEL}, read in your salon&rsquo;s own timezone — and
                it is yours to narrow.
              </p>
            </div>

            <div className="safes" data-reveal>
              {SAFEGUARDS.map((s, i) => (
                <div className="safe lfade" style={{ ["--d" as string]: `${i * 0.08}s` }} key={s.title}>
                  <div className="s-top">
                    <h3>{s.title}</h3>
                    <span className="ltag lglass">{SAFE_TAGS[i]}</span>
                  </div>
                  <p className="body-s">{s.body}</p>
                </div>
              ))}
            </div>

            <div className="counsel lglass" data-reveal>
              <p className="ct lfade">Read this part twice</p>
              <p className="body-s lfade" style={{ ["--d" as string]: ".1s" }}>
                We are engineers, not your lawyers. Outbound calling is regulated — TCPA in the US and its
                state analogues — and what counts as valid consent for a voice call is not obvious from a
                spreadsheet column named &ldquo;consent&rdquo;. The gates above are how we built the system;
                they are not legal advice. Have your own counsel review the consent language your clients
                agreed to before the first list is dialled.
              </p>
              <p className="body-s lfade" style={{ ["--d" as string]: ".18s" }}>
                <Link href="/terms">Terms of service</Link> &nbsp;&middot;&nbsp;{" "}
                <Link href="/privacy">What we do with your list</Link>
              </p>
            </div>
          </div>
        </section>

        {/* ================= PRICING ================= */}
        <section className="scene" id="pricing" data-scene="pricing">
          <div className="scene-inner">
            <div className="sec-right" data-reveal>
              <p className="lmicro kick lfade"><span>Pricing</span><span className="tick" /></p>
              <h2 className="lcaps h-big">
                <span className="rise"><span>Start small.</span></span>
                <span className="rise"><span style={{ ["--d" as string]: ".12s" }}>The list decides</span></span>
              </h2>
              <p className="body-s sec-para lfade" style={{ ["--d" as string]: ".25s" }}>
                Flat prices, no per-minute billing, no per-lead invoices. Monthly plans are month to month —
                cancel and the calling stops that day.
              </p>
            </div>

            <div className="pilot" data-reveal>
              <div className="pilot-main lfade">
                <p className="pk">Start here — {pilot.cadence}</p>
                <h3>{pilot.name}</h3>
                <p className="pb">{pilot.blurb}</p>
                <ul>
                  {pilot.features.map((f) => (
                    <li key={f}>{f}</li>
                  ))}
                </ul>
              </div>
              <div className="pilot-side lfade" style={{ ["--d" as string]: ".12s" }}>
                <p className="price">{pilot.priceLabel}</p>
                <p className="cad">{pilot.cadence}</p>
                <PilotCta plan={pilot} />
              </div>
            </div>

            <div className="lplans" data-reveal>
              {monthly.map((p, i) => (
                <div className="lplan lglass lfade" style={{ ["--d" as string]: `${i * 0.1}s` }} key={p.id}>
                  <div className="p-top">
                    <h3 className="lcaps">{p.name}</h3>
                    {p.highlight ? <span className="chip-flag lglass">Our default</span> : null}
                  </div>
                  <p className="price">{p.priceLabel}</p>
                  <p className="cad">{p.cadence}</p>
                  <p className="body-s pb">{p.blurb}</p>
                  <ul>
                    {p.features.map((f) => (
                      <li key={f}>{f}</li>
                    ))}
                  </ul>
                  <PlanCta plan={p} />
                </div>
              ))}
            </div>

            <p className="body-s pricing-note" data-reveal>
              <span className="lfade">
                Not sure which one? <Link href={CTA.startHref}>Start with the questions</Link> — the form
                reads your list size and your ticket back to you with the plan that fits, no card required.
                Or <a href={callUrl}>book a 15-minute call</a> and talk it through first.
              </span>
            </p>
          </div>
        </section>

        {/* ================= FAQ ================= */}
        <section className="scene" id="faq" data-scene="faq">
          <div className="scene-inner">
            <div className="sec-left" data-reveal>
              <p className="lmicro kick lfade"><span>Straight answers</span><span className="tick" /></p>
              <h2 className="lcaps h-big">
                <span className="rise"><span>The questions that</span></span>
                <span className="rise"><span style={{ ["--d" as string]: ".12s" }}>actually decide it</span></span>
              </h2>
            </div>

            <div className="lfaq" data-reveal>
              {FAQ.map((item, i) => (
                <details className="lfade" style={{ ["--d" as string]: `${i * 0.05}s` }} key={item.q}>
                  <summary>
                    {item.q} <span className="plus">+</span>
                  </summary>
                  <p className="ans body-s">{item.a}</p>
                </details>
              ))}
            </div>
            <p className="body-s faq-more" data-reveal>
              <span className="lfade">
                Something not answered here? Write to{" "}
                <a href={`mailto:${SITE.contactEmail}`}>{SITE.contactEmail}</a> and a person replies.
              </span>
            </p>
          </div>
        </section>

        {/* ================= CLOSING ================= */}
        <section className="scene lclosing" id="start" data-scene="closing">
          <div className="scene-inner">
            <div className="closing-stage" data-reveal>
              <p className="lmicro lfade">What happens next</p>
              <h2 className="lcaps h-mega blurcaps" id="closing-title" style={{ marginTop: "1.1rem" }}>
                Bring the list
              </h2>
              <div className="closing-cols">
                <p className="body-s lfade" style={{ ["--d" as string]: ".35s" }}>
                  Answer a few questions about your salon, the clients who drifted, and the offer you want
                  Malone to make. The plan that fits comes back straight away.
                </p>
                <p className="body-s col-r lfade" style={{ ["--d" as string]: ".45s" }}>
                  We come back on the offer itself — and on whether a win-back campaign is worth running for
                  your chairs at all.
                </p>
              </div>
              <form className="contact lglass lfade" style={{ ["--d" as string]: ".6s" }} id="contact-form" aria-label="Start a campaign">
                <input type="text" name="name" id="cf-name" placeholder="Name" autoComplete="name" aria-label="Your name" />
                <span className="divider" />
                <input type="email" name="email" id="cf-email" placeholder="Email" autoComplete="email" aria-label="Your email" />
                <button className="btn-white" type="submit">Start a campaign &nbsp;&rarr;</button>
              </form>
              <p className="body-s closing-alt lfade" style={{ ["--d" as string]: ".75s" }}>
                Prefer to talk first? <a href={callUrl}>Book a 15-minute call</a> &nbsp;&middot;&nbsp;{" "}
                <a href={`mailto:${SITE.contactEmail}`}>Or just email us</a>
              </p>
            </div>
          </div>
        </section>
      </main>

      <footer className="lfooter">
        <div className="foot-wrap">
          <div>
            <p className="foot-brand">{SITE.name}</p>
            <p style={{ marginTop: ".7rem", maxWidth: "36ch" }}>
              Win-back campaigns for salons and med spas. A new product from {COMPANY.legalName} — zero
              customers so far, and you would be early. Everything on this page is what the software does,
              or arithmetic labelled as an example.
            </p>
          </div>
          <div>
            <p className="foot-h">The promise</p>
            <p style={{ maxWidth: "38ch" }}>{SITE.complianceLine}</p>
          </div>
          <div>
            <p className="foot-h">{COMPANY.legalName}</p>
            <p>
              {COMPANY.addressStreet}
              <br />
              {COMPANY.addressLocality}, {COMPANY.addressRegion} {COMPANY.postalCode}, {COMPANY.addressCountry}
            </p>
            <p style={{ marginTop: ".55rem" }}>
              Malone calls from <a href={COMPANY.outboundPhoneHref}>{COMPANY.outboundPhone}</a> — printed
              here so anyone who gets a call can check it.
            </p>
          </div>
        </div>
        <div className="foot-legal">
          <span>
            &copy; {new Date().getFullYear()} {COMPANY.legalName} &middot; {SITE.domain}
          </span>
          <span>
            <Link href="/terms">Terms</Link> &nbsp;&middot;&nbsp; <Link href="/privacy">Privacy</Link>
          </span>
        </div>
      </footer>
    </div>
  );
}

/**
 * Checkout is the express lane. A plan whose payment link is not live falls back
 * to /start rather than a dead '#': the conversion path must never end in nothing.
 */
function PlanCta({ plan }: { plan: Plan }) {
  const href = planLink(plan);
  if (href === "#") {
    return (
      <Link className="choose" href={CTA.startHref}>
        Choose {plan.name} &rarr;
      </Link>
    );
  }
  return (
    <a className="choose" href={href}>
      Choose {plan.name} &rarr;
    </a>
  );
}

function PilotCta({ plan }: { plan: Plan }) {
  const href = planLink(plan);
  if (href === "#") {
    return (
      <Link className="btn-ink" href={CTA.startHref}>
        Start the pilot &nbsp;&rarr;
      </Link>
    );
  }
  return (
    <a className="btn-ink" href={href}>
      Start the {plan.priceLabel} pilot &nbsp;&rarr;
    </a>
  );
}
