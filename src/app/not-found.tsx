import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { CTA, SITE } from "@/lib/site";

export const metadata: Metadata = {
  title: "Page not found",
  robots: { index: false, follow: false },
};

export default function NotFound() {
  return (
    <div className="flex min-h-dvh flex-col font-sans">
      <SiteHeader />
      <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col items-center px-6 py-24 text-center sm:py-32">
        <p className="eyebrow">404</p>
        <h1 className="h-display mt-5 max-w-lg text-[clamp(2rem,6vw,3.25rem)]">
          This page went the way of a lapsed client.
        </h1>
        <p className="help mt-4 max-w-sm">
          The link is wrong or the page has moved. Nothing is lost — the front page has the whole
          story, and the campaign form is two minutes.
        </p>
        <hr className="rule mt-8 w-16" />
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link className="btn btn-primary" href={CTA.startHref}>
            {CTA.startLabel}
          </Link>
          <Link className="btn btn-ghost" href="/">
            Back to {SITE.domain}
          </Link>
        </div>
      </main>
      <SiteFooter />
    </div>
  );
}
