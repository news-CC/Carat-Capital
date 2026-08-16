import Link from "next/link";
import { COMPANY, CTA, SITE, bookingCallUrl } from "@/lib/site";

/**
 * Site-wide marketing footer. Every public page ends in this: who legally sells the product,
 * where to write to it, the number Malone dials out from, and the two legal documents.
 *
 * Rendered explicitly by each public page rather than from the root layout. The operator app
 * (/admin, /login) is deliberately unbranded and simply does not render it, which is why the
 * root layout stays chrome-free — a layout-level footer would need to know the pathname, and
 * the only way to read that in a layout is a client component. This is a server component and
 * ships no JavaScript.
 */
export function SiteFooter() {
  const callUrl = bookingCallUrl();

  return (
    <footer className="border-t border-line bg-cream">
      <div className="mx-auto max-w-6xl px-6 py-14">
        <div className="grid gap-10 md:grid-cols-[1.4fr_1fr_1fr]">
          <div>
            <Link href="/" className="font-display text-base tracking-tight">
              {SITE.name}
              <span className="text-brass">.</span>
            </Link>
            <p className="help mt-3 max-w-xs">
              {SITE.name} is a product of <strong className="text-ink">{COMPANY.legalName}</strong>
            </p>
            <address className="help mt-3 max-w-xs not-italic">
              {COMPANY.addressStreet}
              <br />
              {COMPANY.addressLocality}, {COMPANY.addressRegion} {COMPANY.postalCode}
              <br />
              {COMPANY.addressCountry}
            </address>
          </div>

          <div>
            <p className="stat-label">Contact</p>
            <ul className="mt-4 grid gap-2.5 text-[0.8125rem] text-ink-soft">
              <li>
                <a className="link" href={`mailto:${COMPANY.supportEmail}`}>
                  {COMPANY.supportEmail}
                </a>
              </li>
              <li>
                <a className="link" href={callUrl}>
                  {CTA.callLabel}
                </a>
              </li>
              <li className="help">
                Malone calls from{" "}
                <a className="link" href={COMPANY.outboundPhoneHref}>
                  {COMPANY.outboundPhone}
                </a>
              </li>
            </ul>
          </div>

          <div>
            <p className="stat-label">Site</p>
            <ul className="mt-4 grid gap-2.5 text-[0.8125rem] text-ink-soft">
              <li>
                <Link className="link" href={CTA.startHref}>
                  {CTA.startLabel}
                </Link>
              </li>
              <li>
                <Link className="link" href="/#pricing">
                  Pricing
                </Link>
              </li>
              <li>
                <Link className="link" href="/terms">
                  Terms of service
                </Link>
              </li>
              <li>
                <Link className="link" href="/privacy">
                  Privacy notice
                </Link>
              </li>
              <li>
                <Link className="link" href="/login">
                  Operator login
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <hr className="rule my-9" />

        <p className="help max-w-3xl">{SITE.complianceLine}</p>
        <p className="help mt-4">
          {SITE.domain} · © {new Date().getFullYear()} {COMPANY.legalName} · All figures on this
          site are illustrative arithmetic, not customer results.
        </p>
      </div>
    </footer>
  );
}

export default SiteFooter;
