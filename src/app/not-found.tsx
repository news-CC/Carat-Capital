import type { Metadata } from "next";
import Link from "next/link";
import { SITE } from "@/lib/site";

export const metadata: Metadata = {
  title: "Page not found",
  robots: { index: false, follow: false },
};

export default function NotFound() {
  return (
    <main className="flex min-h-dvh flex-col items-center justify-center px-6 py-20 text-center">
      <p className="eyebrow">404</p>
      <h1 className="h-display mt-5 max-w-lg text-[clamp(2rem,6vw,3.25rem)]">
        This page went the way of a lapsed client.
      </h1>
      <p className="help mt-4 max-w-sm">
        The link is wrong or the page has moved. Everything worth reading is on the front page.
      </p>
      <hr className="rule mt-8 w-16" />
      <Link className="btn btn-ghost mt-8" href="/">
        Back to {SITE.domain}
      </Link>
    </main>
  );
}
