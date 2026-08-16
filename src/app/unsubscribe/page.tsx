import type { Metadata } from "next";
import Link from "next/link";

import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { LEGAL } from "@/components/LegalLayout";
import { unsubscribeByToken, type UnsubscribeOutcome } from "@/lib/outreach";
import { SITE } from "@/lib/site";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Unsubscribe",
  description: "Remove your address from Salon Malone marketing email.",
  robots: { index: false, follow: false },
};

type Props = { searchParams: Promise<{ token?: string }> };

const COPY: Record<UnsubscribeOutcome | "error", { title: string; body: string }> = {
  done: {
    title: "Done — you're off the list.",
    body: "You won't get marketing email from us again. Anything already queued to you has been cancelled.",
  },
  invalid: {
    title: "That link has already been used.",
    body: "Which almost certainly means you're already unsubscribed. If you get another email from us anyway, reply to it and we'll fix it by hand.",
  },
  missing: {
    title: "That link is missing its code.",
    body: "Use the unsubscribe link in the email itself, or email us and we'll take care of it.",
  },
  unavailable: {
    title: "We couldn't reach the list right now.",
    body: "This is our fault, not yours. Email us and we'll remove you manually today.",
  },
  error: {
    title: "Something went wrong on our end.",
    body: "Your request didn't record. Email us and we'll remove you manually today.",
  },
};

export default async function UnsubscribePage({ searchParams }: Props) {
  const { token } = await searchParams;
  const result = await unsubscribeByToken(token);
  const state = result.ok ? result.data : "error";
  const { title, body } = COPY[state];

  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader showNav={false} />
      <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col justify-center px-6 py-24">
        <p className="eyebrow">Marketing email</p>
        <h1 className="h-display mt-5 text-[clamp(2rem,5vw,3rem)]">{title}</h1>
        <p className="prose-tight mt-5 text-lg">{body}</p>

        <div className="rule my-10" />

        <p className="help">
          This only covers marketing email from {LEGAL.entity} about {SITE.name}. It has nothing to
          do with calls to your own clients — if you are a salon owner running a campaign, your list
          is untouched.
        </p>
        <p className="help mt-3">
          Questions, or want to be removed some other way?{" "}
          <a className="underline" href={`mailto:${SITE.contactEmail}`}>
            {SITE.contactEmail}
          </a>
        </p>

        <div className="mt-10">
          <Link className="btn btn-ghost" href="/">
            Back to {SITE.name}
          </Link>
        </div>
      </main>
      <SiteFooter />
    </div>
  );
}
