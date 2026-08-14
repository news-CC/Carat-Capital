import type { Metadata } from "next";
import { Fraunces, Inter } from "next/font/google";
import { publicEnv } from "@/lib/env";
import { SITE } from "@/lib/site";
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
      <body className="min-h-dvh bg-cream text-ink antialiased">{children}</body>
    </html>
  );
}
