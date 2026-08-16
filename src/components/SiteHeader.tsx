import Link from "next/link";
import { CTA, SITE, bookingCallUrl } from "@/lib/site";

/**
 * Site-wide marketing header.
 *
 * The anchors are absolute (`/#how`, not `#how`) so the same header works on /start,
 * /terms and /privacy: from the home page the browser treats them as an in-page jump,
 * from anywhere else they navigate home and land on the section.
 */
const NAV: { href: string; label: string }[] = [
  { href: "/#how", label: "How it runs" },
  { href: "/#call", label: "The call" },
  { href: "/#pricing", label: "Pricing" },
  { href: "/#faq", label: "Questions" },
];

export function SiteHeader({ showNav = true }: { showNav?: boolean }) {
  const callUrl = bookingCallUrl();

  return (
    <header className="nav-sticky">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-3.5">
        <Link
          href="/"
          className="font-display text-lg tracking-tight transition-opacity duration-150 hover:opacity-70"
        >
          {SITE.name}
          <span className="text-brass">.</span>
        </Link>

        {showNav ? (
          <nav
            aria-label="Sections"
            className="hidden items-center gap-7 text-[0.8125rem] text-ink-soft md:flex"
          >
            {NAV.map((item) => (
              <a
                key={item.href}
                className="transition-opacity duration-150 hover:opacity-60"
                href={item.href}
              >
                {item.label}
              </a>
            ))}
          </nav>
        ) : null}

        <div className="flex items-center gap-2">
          <a className="btn btn-ghost btn-sm hidden sm:inline-flex" href={callUrl}>
            {CTA.callLabelShort}
          </a>
          <Link className="btn btn-primary btn-sm" href={CTA.startHref}>
            {CTA.startLabelShort}
          </Link>
        </div>
      </div>
    </header>
  );
}

export default SiteHeader;
