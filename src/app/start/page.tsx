import type { Metadata } from 'next';
import { SiteFooter } from '@/components/SiteFooter';
import { SiteHeader } from '@/components/SiteHeader';
import { StartForm } from '@/components/StartForm';
import { NEXT_STEPS, OUTBOUND_NUMBER, SUPPORT_EMAIL } from '@/lib/onboarding';
import { SITE, bookingCallUrl } from '@/lib/site';

export const metadata: Metadata = {
  title: 'Start a win-back campaign',
  description:
    'Tell us about your salon or med spa, the lapsed clients you want called, and the offer Malone should make. Nothing is dialled until we have been through your list with you.',
  alternates: { canonical: '/start' },
  robots: { index: true, follow: true },
};

export default function StartPage() {
  const callUrl = bookingCallUrl();

  return (
    <div className="font-sans">
      <SiteHeader showNav={false} />

      <main className="bg-[linear-gradient(180deg,var(--color-cream)_0%,var(--color-shell)_100%)]">
        <div className="mx-auto max-w-5xl px-6 pt-12 pb-20 sm:pt-16">
          <p className="eyebrow">Set up in one screen</p>
          <h1 className="h-display mt-4 max-w-3xl text-[clamp(2rem,6vw,3.5rem)]">
            Tell us which chairs you want filled.
          </h1>
          <p className="prose-tight mt-5 text-[1.0625rem]">
            Nine answers. They become the account, the calling window and the exact words Malone says
            to the clients who stopped booking. You pick a plan on the next screen — no card on this
            one.
          </p>

          <div className="mt-10 grid gap-8 lg:grid-cols-[minmax(0,1fr)_19rem] lg:items-start">
            <div className="card card-pad">
              <StartForm />
            </div>

            <aside className="grid gap-6 lg:sticky lg:top-8">
              <div className="card card-pad">
                <p className="eyebrow">After you submit</p>
                <ol className="mt-4 grid gap-5">
                  {NEXT_STEPS.map((step) => (
                    <li key={step.n}>
                      <div className="flex items-baseline gap-2.5">
                        <span className="font-display text-base text-brass">{step.n}</span>
                        <h2 className="font-display text-[1.0625rem] leading-snug">{step.title}</h2>
                      </div>
                      <p className="help mt-1.5">{step.body}</p>
                    </li>
                  ))}
                </ol>
              </div>

              <div className="card card-pad">
                <p className="eyebrow">The rules we call under</p>
                <p className="help mt-3">{SITE.complianceLine}</p>
                <hr className="rule my-4" />
                <p className="help">
                  Malone dials from {OUTBOUND_NUMBER}. Voice and email only — there is no SMS product
                  here to opt into.
                </p>
              </div>

              <div className="card card-pad">
                <p className="eyebrow">Rather talk first</p>
                <p className="help mt-3">
                  Fifteen minutes, your export, and an honest read on whether a win-back campaign is
                  worth running for your chairs.
                </p>
                <a className="btn btn-ghost btn-sm mt-4" href={callUrl}>
                  Book 15 minutes
                </a>
                <p className="help mt-4">
                  Or email{' '}
                  <a className="link" href={`mailto:${SUPPORT_EMAIL}`}>
                    {SUPPORT_EMAIL}
                  </a>
                  .
                </p>
              </div>
            </aside>
          </div>
        </div>
      </main>

      <SiteFooter />
    </div>
  );
}
