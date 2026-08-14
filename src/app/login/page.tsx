import type { Metadata } from "next";
import Link from "next/link";
import { LoginForm } from "@/components/ui/LoginForm";
import { safeNextPath } from "@/lib/next-path";
import { SITE } from "@/lib/site";

export const metadata: Metadata = {
  title: "Operator login",
  robots: { index: false, follow: false },
};

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string }>;
}) {
  const { next } = await searchParams;
  // The same gate the server action applies to the field this seeds — one helper, so a `/\evil.com`
  // that the action would reject can never be planted in the markup either.
  const target = safeNextPath(next);

  return (
    <main className="flex min-h-dvh flex-col items-center justify-center bg-[linear-gradient(180deg,var(--color-cream)_0%,var(--color-shell)_100%)] px-6 py-16">
      <div className="w-full max-w-sm">
        <div className="card card-pad">
          <p className="eyebrow">{SITE.domain}</p>
          <h1 className="h-display mt-3 text-3xl">
            {SITE.name}
            <span className="text-brass">.</span>
          </h1>
          <p className="help mt-2">Operator access only.</p>

          <hr className="rule my-6" />

          <LoginForm next={target} />
        </div>

        <p className="help mt-6 text-center">
          <Link className="underline decoration-line underline-offset-4" href="/">
            Back to {SITE.domain}
          </Link>
        </p>
      </div>
    </main>
  );
}
