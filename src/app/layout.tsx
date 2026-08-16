import type { Metadata } from "next";
import { Fraunces, Inter } from "next/font/google";
import { publicEnv } from "@/lib/env";
import { COMPANY, SITE } from "@/lib/site";
import "./globals.css";

const fraunces = Fraunces({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-fraunces",
});

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

/** metadataBase must never throw the build — fall back to the canonical domain. */
function baseUrl(): URL {
  try {
    return new URL(publicEnv.appUrl);
  } catch {
    return new URL(`https://${SITE.domain}`);
  }
}

const title = `${SITE.name} — ${SITE.tagline}`;

export const metadata: Metadata = {
  metadataBase: baseUrl(),
  title: { default: title, template: `%s · ${SITE.name}` },
  description: SITE.description,
  applicationName: SITE.name,
  // The product is Salon Malone; the company that sells it is Easecase, Inc.
  authors: [{ name: COMPANY.legalName }],
  creator: COMPANY.legalName,
  publisher: COMPANY.legalName,
  keywords: [
    "salon win-back campaign",
    "med spa client reactivation",
    "lapsed client calls",
    "AI voice concierge for salons",
    "salon rebooking",
  ],
  alternates: { canonical: "/" },
  icons: { icon: "/favicon.svg" },
  openGraph: {
    type: "website",
    siteName: SITE.name,
    url: "/",
    title,
    description: SITE.description,
    images: [{ url: "/og.svg", width: 1200, height: 630, alt: SITE.headline }],
  },
  twitter: {
    card: "summary_large_image",
    title,
    description: SITE.description,
    images: ["/og.svg"],
  },
  robots: { index: true, follow: true },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${fraunces.variable} ${inter.variable}`}>
      {/*
        Deliberately chrome-free. The marketing pages render <SiteHeader /> and <SiteFooter />
        themselves; the operator app (/admin, /login) renders neither. Putting the footer here
        instead would mean the layout had to know the pathname to hide it from /admin, and the
        only way a layout can read that is by becoming a client component — which would ship
        the whole footer as JavaScript on every route, operator screens included.
      */}
      <body className="min-h-dvh bg-cream text-ink antialiased">{children}</body>
    </html>
  );
}
