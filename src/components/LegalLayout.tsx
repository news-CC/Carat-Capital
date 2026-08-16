import Link from "next/link";
import type { ReactNode } from "react";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { COMPANY, COMPANY_ADDRESS_LINE } from "@/lib/site";

/**
 * Shared shell for /terms and /privacy.
 *
 * Server component on purpose: the section nav is plain anchor links, so the whole page
 * works with no JavaScript at all.
 */

/**
 * Who the company legally is, for the two documents that have to name it precisely.
 *
 * Everything except the revision date is derived from COMPANY in src/lib/site.ts. These are
 * contract terms — an address that says one thing in the footer and another in the notices
 * clause is the kind of drift that makes a contract arguable, so there is exactly one place
 * to change it and this is not that place.
 */
export const LEGAL = {
  entity: COMPANY.legalName,
  entityLong: `${COMPANY.legalName}, a Delaware corporation`,
  address: COMPANY_ADDRESS_LINE,
  addressLine1: COMPANY.addressStreet,
  addressLine2: `${COMPANY.addressLocality}, ${COMPANY.addressRegion} ${COMPANY.postalCode}, ${COMPANY.addressCountry}`,
  email: COMPANY.supportEmail,
  outboundNumber: COMPANY.outboundPhone,
  /** Displayed date and its machine-readable twin. Change both together. */
  updated: "16 August 2026",
  updatedISO: "2026-08-16",
} as const;

export type LegalSection = {
  /** Anchor id, also the target of the sticky nav. */
  id: string;
  title: string;
  /** The plain-English one-liner shown in the tinted callout. */
  short: ReactNode;
  body: ReactNode;
};

export type LegalLayoutProps = {
  eyebrow: string;
  title: string;
  lede: ReactNode;
  /** Optional straight-faced banner above the sections (the Terms uses it for the counsel note). */
  notice?: { label: string; body: ReactNode };
  sections: LegalSection[];
  /** The other legal page, linked from the footer so the pair is always one click apart. */
  sibling: { href: string; label: string; blurb: string };
};

const num = (i: number): string => String(i + 1).padStart(2, "0");

export default function LegalLayout({
  eyebrow,
  title,
  lede,
  notice,
  sections,
  sibling,
}: LegalLayoutProps) {
  return (
    <div className="font-sans">
      <SiteHeader />

      <main>
        <section className="border-b border-line bg-[linear-gradient(180deg,var(--color-cream)_0%,var(--color-shell)_100%)]">
          <div className="mx-auto max-w-6xl px-6 pt-16 pb-14 sm:pt-20">
            <p className="eyebrow">{eyebrow}</p>
            <h1 className="h-display mt-5 max-w-3xl text-[clamp(2.4rem,6vw,4rem)]">{title}</h1>
            <div className="prose-tight mt-7 text-[1.0625rem]">{lede}</div>
            <p className="mt-8 flex flex-wrap items-center gap-x-3 gap-y-2">
              <span className="badge badge-mute">
                Last updated <time dateTime={LEGAL.updatedISO}>{LEGAL.updated}</time>
              </span>
              <span className="help">
                {LEGAL.entity} · {LEGAL.address}
              </span>
            </p>
          </div>
        </section>

        <div className="mx-auto max-w-6xl gap-x-16 px-6 py-16 lg:grid lg:grid-cols-[14rem_minmax(0,1fr)] lg:py-20">
          <aside className="hidden lg:block">
            {/* Clears the sticky site header, which is ~3.5rem tall. */}
            <nav aria-label="On this page" className="sticky top-24">
              <p className="stat-label">On this page</p>
              <ol className="mt-4 grid gap-3 border-l border-line pl-4">
                {sections.map((s, i) => (
                  <li key={s.id}>
                    <a
                      href={`#${s.id}`}
                      className="flex gap-2.5 text-[0.8125rem] leading-snug text-ink-soft transition-opacity duration-150 hover:opacity-60"
                    >
                      <span className="font-display tabular-nums text-brass">{num(i)}</span>
                      <span>{s.title}</span>
                    </a>
                  </li>
                ))}
              </ol>
              <hr className="rule my-6" />
              <p className="help">
                Anything unclear, write to{" "}
                <a
                  className="underline decoration-line underline-offset-4 transition-opacity duration-150 hover:opacity-60"
                  href={`mailto:${LEGAL.email}`}
                >
                  {LEGAL.email}
                </a>
                . A human answers.
              </p>
            </nav>
          </aside>

          <div className="min-w-0">
            {notice ? (
              <div className="card card-pad mb-12 border-brass/40">
                <p className="eyebrow">{notice.label}</p>
                <div className="prose-tight mt-3 text-[0.9375rem]">{notice.body}</div>
              </div>
            ) : null}

            <details className="card card-pad mb-10 lg:hidden">
              <summary className="cursor-pointer text-[0.9375rem] font-medium text-ink">
                Jump to a section
              </summary>
              <ol className="mt-4 grid gap-3">
                {sections.map((s, i) => (
                  <li key={s.id}>
                    <a href={`#${s.id}`} className="flex gap-2.5 text-[0.875rem] text-ink-soft">
                      <span className="font-display tabular-nums text-brass">{num(i)}</span>
                      <span>{s.title}</span>
                    </a>
                  </li>
                ))}
              </ol>
            </details>

            {sections.map((s, i) => (
              <section key={s.id} id={s.id} className="anchor-target">
                {i > 0 ? <hr className="rule my-14" /> : null}
                <p className="font-display text-2xl leading-none text-brass tabular-nums">
                  {num(i)}
                </p>
                <h2 className="h-display mt-3 max-w-2xl text-[clamp(1.5rem,3.2vw,2.125rem)]">
                  {s.title}
                </h2>

                {/* Slightly wider than the 62ch prose measure below it, so the summary reads as a
                    step up from the body rather than a different column. */}
                <div className="mt-6 max-w-[38rem] rounded-[14px] border border-brass/25 bg-brass-wash px-5 py-4 sm:px-6">
                  <p className="eyebrow">The short version</p>
                  <p className="mt-2 text-[0.9375rem] leading-relaxed text-ink">{s.short}</p>
                </div>

                <div className="prose-tight mt-7 text-[0.9375rem]">{s.body}</div>
              </section>
            ))}
          </div>
        </div>
      </main>

      {/* The pair is always one click apart: whichever document you are in, the other one is here. */}
      <section className="border-t border-line bg-shell">
        <div className="mx-auto flex max-w-6xl flex-col gap-8 px-6 py-14 md:flex-row md:items-start md:justify-between">
          <div className="max-w-md">
            <p className="eyebrow">Keep reading</p>
            <h2 className="mt-3 text-xl">
              <Link className="link" href={sibling.href}>
                {sibling.label}
              </Link>
            </h2>
            <p className="help mt-2">{sibling.blurb}</p>
          </div>
          <address className="not-italic">
            <p className="stat-label">Written notices go to</p>
            <p className="help mt-3 leading-relaxed">
              {LEGAL.entity}
              <br />
              {LEGAL.addressLine1}
              <br />
              {LEGAL.addressLine2}
              <br />
              <a className="link" href={`mailto:${LEGAL.email}`}>
                {LEGAL.email}
              </a>
            </p>
          </address>
        </div>
      </section>

      <SiteFooter />
    </div>
  );
}

/** Brass-dash list. The one list style used inside legal prose. */
export function LegalList({ items }: { items: ReactNode[] }) {
  return (
    <ul className="mt-4 grid gap-2.5">
      {items.map((item, i) => (
        <li key={i} className="flex gap-3">
          <span aria-hidden className="mt-[0.7em] h-px w-3 shrink-0 bg-brass" />
          <span className="min-w-0">{item}</span>
        </li>
      ))}
    </ul>
  );
}

/** Sub-heading inside a section. Spaced so it never collides with the paragraph above it. */
export function LegalHeading({ children }: { children: ReactNode }) {
  return <h3 className="mt-9 mb-3 text-[1.0625rem]">{children}</h3>;
}

/** A quiet aside — used for the bits people skim past and then email us about. */
export function LegalNote({ children }: { children: ReactNode }) {
  return (
    <div className="mt-6 rounded-[14px] border border-line bg-shell px-5 py-4 text-[0.875rem] leading-relaxed text-ink-soft">
      {children}
    </div>
  );
}
