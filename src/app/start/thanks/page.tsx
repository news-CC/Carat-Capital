import type { Metadata } from 'next';
import Link from 'next/link';
import { SiteFooter } from '@/components/SiteFooter';
import { SiteHeader } from '@/components/SiteHeader';
import { NEXT_STEPS, OUTBOUND_NUMBER, SUPPORT_EMAIL } from '@/lib/onboarding';
import { bookingCallUrl } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Your win-back campaign is queued for review',
  description:
    'What happens after you sign up: your account is created switched off, we scrub your list before anything dials, and you get an email the second a booking lands.',
  // A confirmation page is for one person who just submitted, not for search results.
  robots: { index: false, follow: false },
};

export default function StartThanksPage() {
  const callUrl = bookingCallUrl();

  return (
    <div className="font-sans">
      <SiteHeader showNav={false} />

      <main className="bg-[linear-gradient(180deg,var(--color-cream)_0%,var(--color-shell)_100%)]">
        <div className="mx-auto max-w-3xl px-6 pt-16 pb-20 sm:pt-20">
          <p className="eyebrow">Received</p>
          <h1 className="h-display mt-4 text-[clamp(2rem,6vw,3.25rem)]">
            Your details are with us.
          </h1>
          <p className="prose-tight mt-5 text-[1.0625rem]">
            A copy of what you sent should be in your inbox — check spam if it is not there in a
            couple of minutes, and add our address to your contacts so the booking alerts never land
            there either. If it never turns up, write to {SUPPORT_EMAIL} and we will resend it. Here
            is exactly what happens from here, in order.
          </p>

          <ol className="mt-12 grid gap-8">
            {NEXT_STEPS.map((step) => (
              <li key={step.n} className="border-t border-line pt-5">
                <span className="font-display text-2xl text-brass">{step.n}</span>
                <h2 className="mt-2 font-display text-xl">{step.title}</h2>
                <p className="prose-tight mt-2 text-[0.9375rem]">{step.body}</p>
              </li>
            ))}
          </ol>

          <div className="card card-pad mt-12">
            <p className="eyebrow">If you would rather talk it through</p>
            <h2 className="mt-3 font-display text-xl">Fifteen minutes, your export, a straight read.</h2>
            <p className="prose-tight mt-2 text-[0.9375rem]">
              Bring the list you were thinking of, or nothing at all. We will tell you whether a
              win-back campaign is worth running for your chairs before you pay for one.
            </p>
            <div className="mt-5 flex flex-wrap items-center gap-3">
              <a className="btn btn-primary" href={callUrl}>
                Book 15 minutes
              </a>
              <a className="btn btn-ghost" href={`mailto:${SUPPORT_EMAIL}`}>
                Email {SUPPORT_EMAIL}
              </a>
            </div>
            <p className="help mt-4">
              {SUPPORT_EMAIL} is the support address for everything — billing, your list, or asking
              us to delete what you just sent. When calling starts, Malone dials from{' '}
              {OUTBOUND_NUMBER}.
            </p>
          </div>

          <p className="help mt-10">
            Ready to pick a plan instead?{' '}
            <Link className="link" href="/#pricing">
              The four plans and their prices
            </Link>{' '}
            are on the main page — the $299 pilot included.
          </p>
        </div>
      </main>

      <SiteFooter />
    </div>
  );
}
