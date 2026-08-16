import type { Metadata } from "next";
import Link from "next/link";
import LegalLayout, {
  LEGAL,
  LegalHeading,
  LegalList,
  LegalNote,
  type LegalSection,
} from "@/components/LegalLayout";
import { SITE } from "@/lib/site";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description:
    "How Salon Malone handles data: your account details, the lapsed-client lists salons upload, " +
    "call records and recordings, our named sub-processors, how long we keep things, and how anyone " +
    "gets themselves off a calling list permanently.",
  alternates: { canonical: "/privacy" },
};

type Processor = {
  name: string;
  role: string;
  sees: string;
};

const PROCESSORS: Processor[] = [
  {
    name: "Vapi",
    role: "Places the calls and runs the voice agent — telephony, speech-to-text, the language model and the synthesised voice.",
    sees: "Contact first name and phone number, the salon name and offer read aloud, the audio of the call, and the transcript. Recordings and transcripts are stored by Vapi.",
  },
  {
    name: "Supabase",
    role: "The database. Every table described above lives here.",
    sees: "Account records, uploaded contact rows, call records, bookings and the suppression list.",
  },
  {
    name: "Resend",
    role: "Sends the booking alert and the Friday report to you.",
    sees: "Your email address and the contents of those emails, which include the contact name, phone number and the slot they agreed to.",
  },
  {
    name: "Stripe",
    role: "Takes the payments.",
    sees: "Your billing details and card data, which Stripe holds and we never see or store. We keep your Stripe customer reference and subscription status.",
  },
  {
    name: "Vercel",
    role: "Hosts and serves the application.",
    sees: "Request and server logs — IP address, timing and errors — in the ordinary course of serving the app.",
  },
];

const sections: LegalSection[] = [
  {
    id: "two-hats",
    title: "We wear two hats, and this is the whole policy in one idea",
    short: (
      <>
        Your business&rsquo;s own account data is ours to be responsible for. Your clients&rsquo;
        contact data is <em>yours</em> — we only ever handle it on your instructions, which makes us
        the hired hands, not the owner.
      </>
    ),
    body: (
      <>
        <p>
          Almost every question about this policy is answered by working out which hat applies.
        </p>
        <LegalHeading>Hat one: your account. We decide, so we are responsible.</LegalHeading>
        <p>
          When you sign up we hold information about your business — your salon name, who to contact,
          the email and phone number, your timezone, your average ticket, the offer text Malone reads
          out, and your billing status. We decide what to do with that, so for it we are the{" "}
          <strong>controller</strong> (or, if your local law prefers, the <strong>business</strong>).
        </p>
        <LegalHeading>Hat two: your list. You decide, so we only follow instructions.</LegalHeading>
        <p>
          When you upload a list of lapsed clients, that is your data about your customers. We store
          it, scrub it, dial it and report on it because you told us to, for that purpose and no
          other. For that data we are a <strong>processor</strong> (a <strong>service provider</strong>
          , in the American phrasing) acting on your documented instructions — which is a technical
          way of saying: it is your list, we are just the ones holding the phone.
        </p>
        <p>Concretely, and without any wriggle room:</p>
        <LegalList
          items={[
            <>
              We do not sell it. We are not that kind of establishment, and there is no version of
              this business where that changes.
            </>,
            <>We do not use it to market anything to anyone, including to you.</>,
            <>
              We do not use it to train models. The model that runs the call reads the transcript in
              the moment and that is the end of its involvement.
            </>,
            <>
              We never mix one salon&rsquo;s list into another&rsquo;s. Every row is tied to the client
              that uploaded it.
            </>,
            <>
              We delete it when you tell us to, subject only to the one exception below.
            </>,
          ]}
        />
        <LegalHeading>The one exception, and why it exists</LegalHeading>
        <p>
          If someone tells us to stop calling, their phone number goes onto a{" "}
          <strong>global suppression list</strong> shared across every campaign we run for every
          client. We keep that number — just the number, the reason and the date — precisely so that
          nobody ever calls it again, including you, including a different salon, including us in two
          years when everyone involved has forgotten. That is not us making use of your data. It is
          the only way <em>never call me again</em> can actually mean never.
        </p>
        <p>
          This policy covers {SITE.name} and {SITE.domain}, both products of {LEGAL.entityLong}, at{" "}
          {LEGAL.address}.
        </p>
      </>
    ),
  },
  {
    id: "what-we-collect",
    title: "What we actually collect",
    short: (
      <>
        Account details, the rows in the list you upload, one record per call attempt, and the
        suppression list. There is no fifth thing we are quietly hoovering up.
      </>
    ),
    body: (
      <>
        <LegalHeading>From you, when you become a client</LegalHeading>
        <p>
          Salon or med spa name, contact name, contact email, contact phone, timezone, whether you are
          a salon or a med spa, your average ticket, the offer text Malone reads, the front-desk phone
          number Malone gives out on voicemail, your billing status and your Stripe customer
          reference. Not your card number — that never touches our systems.
        </p>

        <LegalHeading>From the list you upload</LegalHeading>
        <p>Per contact row, whatever your export contains from among:</p>
        <LegalList
          items={[
            <>Name and first name.</>,
            <>Phone number, both as you sent it and normalised to a standard format.</>,
            <>Email address, if your export has one. We do not email your clients.</>,
            <>The consent flag on that row.</>,
            <>Last visit date, and lifetime value if you include it.</>,
            <>
              What our scrub decided: whether the row was kept or dropped, and the reason — no
              consent, suppressed, invalid number, missing number, duplicate.
            </>,
          ]}
        />

        <LegalHeading>From the calls</LegalHeading>
        <p>
          Every dial attempt writes one record, including the ones that fail: the outcome (booked,
          declined, opted out, voicemail, no answer, answered, failed), how long it lasted, when it
          started and ended, why it ended, what it cost us, a two-sentence summary written for you,
          and the structured result — the agreed time in the client&rsquo;s own words, and whether they
          asked to be removed.
        </p>
        <p>
          <strong>Calls are recorded and transcribed</strong> by our voice provider, so that the
          booking can be extracted afterwards and so that we can review calls for quality. The audio
          and the transcript are stored by that provider; what our database holds is the link to each
          of them, not a second copy. Where you are calling into a jurisdiction that requires notice
          or all-party consent for recording, meeting that requirement is your obligation as the
          sender of the calls — see section 3 of the{" "}
          <Link className="underline decoration-line underline-offset-4" href="/terms">
            Terms
          </Link>
          .
        </p>

        <LegalHeading>Bookings</LegalHeading>
        <p>
          The slot in the client&rsquo;s own words, the estimated value at your average ticket, and
          when we emailed it to you.
        </p>

        <LegalHeading>The global suppression list</LegalHeading>
        <p>
          Phone number, the reason it is there (opted out, do-not-call, complaint, invalid, added by
          hand) and the date. Deliberately the bare minimum needed to keep a promise.
        </p>

        <LegalHeading>The website itself</LegalHeading>
        <p>
          {SITE.domain} is a marketing page and an operator login. There are no advertising trackers,
          no third-party analytics, no session recorders and no marketing pixels on it. The one cookie
          we set is a signed, HTTP-only session cookie for the operator login, and it exists solely to
          keep whoever is running campaigns logged in. Our host keeps ordinary server logs.
        </p>
      </>
    ),
  },
  {
    id: "why",
    title: "Why we hold each thing",
    short: (
      <>
        Every field is there because a call, an email, an invoice or a promise to leave someone alone
        needs it. If a field stopped being needed, it would stop being collected.
      </>
    ),
    body: (
      <>
        <div className="card mt-2 overflow-hidden">
          <div className="overflow-x-auto px-3 py-4 sm:px-6">
            <table className="table">
              <thead>
                <tr>
                  <th>What</th>
                  <th>Why it is there</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="text-ink">Account details</td>
                  <td>To run your campaigns, send your reports, and invoice you.</td>
                </tr>
                <tr>
                  <td className="text-ink">Phone number and first name</td>
                  <td>To place the call and to greet the person by name.</td>
                </tr>
                <tr>
                  <td className="text-ink">Consent flag</td>
                  <td>
                    To decide whether the row may be dialled at all. Without it, the row never enters
                    the queue.
                  </td>
                </tr>
                <tr>
                  <td className="text-ink">Last visit, lifetime value</td>
                  <td>To prioritise who is worth calling first and to estimate recovered revenue.</td>
                </tr>
                <tr>
                  <td className="text-ink">Call records</td>
                  <td>
                    To enforce one attempt per person, to produce your Friday report, and to review
                    calls for quality.
                  </td>
                </tr>
                <tr>
                  <td className="text-ink">Recording and transcript</td>
                  <td>
                    To extract the agreed appointment after the call and to check the agent behaved.
                  </td>
                </tr>
                <tr>
                  <td className="text-ink">Suppression list</td>
                  <td>
                    To make sure someone who asked not to be called again is never called again, by
                    anyone we work with.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <p className="mt-6">
          For your account data, our lawful basis is performing our contract with you and our
          legitimate interest in running and defending the business. For contact data, the lawful
          basis is whatever you relied on when you collected the consent you warranted to us — you
          are the one who decided to call these people, and we act on your instruction.
        </p>
      </>
    ),
  },
  {
    id: "sub-processors",
    title: "Who else touches it",
    short: (
      <>
        Five suppliers, named. Nobody else, no data brokers, no advertisers, and no list of
        &ldquo;trusted partners&rdquo; doing something unspecified.
      </>
    ),
    body: (
      <>
        <p>
          Running a voice agent takes suppliers. These are ours, what each one does, and what each one
          can see:
        </p>
        <div className="card mt-6 overflow-hidden">
          <div className="overflow-x-auto px-3 py-4 sm:px-6">
            <table className="table">
              <thead>
                <tr>
                  <th>Sub-processor</th>
                  <th>What it does</th>
                  <th>What it can see</th>
                </tr>
              </thead>
              <tbody>
                {PROCESSORS.map((p) => (
                  <tr key={p.name}>
                    <td className="text-ink">{p.name}</td>
                    <td>{p.role}</td>
                    <td className="text-ink-mute">{p.sees}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        <p className="mt-6">
          Each of them is bound by its own terms and processes data on our instructions. If we add or
          change a sub-processor in a way that materially affects your data, we will update this page
          and, for a material change, email you.
        </p>
        <LegalHeading>Everyone else: no</LegalHeading>
        <LegalList
          items={[
            <>
              <strong>We do not sell personal information</strong>, and we do not share it for
              cross-context behavioural advertising. There is no advertising in this product to sell
              it to.
            </>,
            <>
              We would disclose data if we were legally compelled to — a valid court order, subpoena
              or equivalent. We would tell you first unless we were forbidden from doing so.
            </>,
            <>
              If the business is ever sold or merged, the data moves with it and this policy follows
              it. If a new owner wanted to change it materially, you would get notice and a way out
              before it applied.
            </>,
          ]}
        />
      </>
    ),
  },
  {
    id: "retention",
    title: "How long we keep it",
    short: (
      <>
        As long as your campaigns and our accounts need it — and forever for opt-outs, which is
        entirely the point of them.
      </>
    ),
    body: (
      <>
        <LegalList
          items={[
            <>
              <strong>Account data:</strong> while you have an account, and afterwards for as long as
              we need it for tax, accounting and legal records — generally up to seven years for
              billing records.
            </>,
            <>
              <strong>Contact rows and call records:</strong> for the life of your account, because
              the never-call-anyone-twice rule and your reports both depend on remembering what
              already happened. Deleted sooner on request.
            </>,
            <>
              <strong>Recordings and transcripts:</strong> held by our voice provider under its
              retention settings; we hold only the links. Ask us and we will delete the links and ask
              the provider to delete the artifacts.
            </>,
            <>
              <strong>Suppression entries:</strong> kept permanently, and this one is not negotiable
              for anybody. A do-not-call record that expires is not a do-not-call record. It is a
              phone number, a reason and a date — nothing that identifies the person beyond the number
              itself.
            </>,
            <>
              <strong>Server and email logs:</strong> kept for the short periods our host and email
              provider retain them, for security and debugging.
            </>,
          ]}
        />
      </>
    ),
  },
  {
    id: "your-rights",
    title: "Getting your data out, or getting yourself off the list",
    short: (
      <>
        Ask and we will do it. The one thing we will never delete is a record that says somebody does
        not want to be called.
      </>
    ),
    body: (
      <>
        <LegalHeading>If you are the salon</LegalHeading>
        <p>
          Email{" "}
          <a className="underline decoration-line underline-offset-4" href={`mailto:${LEGAL.email}`}>
            {LEGAL.email}
          </a>{" "}
          and we will export or delete your list, your call records, or your entire account. We will
          do it within 30 days and confirm in writing when it is done. Deleting your account deletes
          your client record, your contacts, your calls and your bookings. It does not delete
          suppression entries, for the reason given above.
        </p>

        <LegalHeading>If we called you and you want it to stop</LegalHeading>
        <p>Two routes. Both work, and neither of them involves finding this page again.</p>
        <LegalList
          items={[
            <>
              <strong>Say it on the call.</strong> &ldquo;Stop calling&rdquo;, &ldquo;take me off the
              list&rdquo;, &ldquo;do not call me&rdquo; — Malone answers{" "}
              <em>done, you&rsquo;re off the list</em> and ends the call, and your number is written to
              the global do-not-call list before the call report has finished processing. It is
              immediate, it is permanent, and it applies to every salon and med spa we work with, not
              only the one that rang you. You do not need to repeat it to anyone.
            </>,
            <>
              <strong>Email us.</strong> Write to{" "}
              <a className="underline decoration-line underline-offset-4" href={`mailto:${LEGAL.email}`}>
                {LEGAL.email}
              </a>{" "}
              with the number, and we will suppress it and confirm. We will also pass a deletion
              request to the business whose list it came from, because they collected the record and
              they hold the original.
            </>,
          ]}
        />

        <LegalHeading>Asking what we hold</LegalHeading>
        <p>
          Email us and we will answer within 30 days. We may ask you to confirm the number is yours
          before we hand over call records — otherwise anyone could ask for the record of anyone
          else&rsquo;s phone call, which would be a worse privacy policy than this one.
        </p>
        <p>
          Depending on where you live you may have rights to access, correct, delete, port, or object
          to the processing of your personal information, and to be free from discrimination for
          asking. Exercise any of them by email. We do not charge for it. Where the data was uploaded
          by a salon, we will usually route the request to that salon, since it is their record and
          their relationship — but a request to <strong>stop calling</strong> we act on ourselves,
          immediately, without asking anyone&rsquo;s permission.
        </p>
        <p>
          If you think we have got something wrong, tell us first — we would rather fix it than read
          about it. You can also complain to your data protection authority, and we will not hold it
          against you.
        </p>
      </>
    ),
  },
  {
    id: "security",
    title: "How it is kept",
    short: (
      <>
        Small system, few doors. Everything encrypted in transit, a database whose public key can read
        nothing at all, and one admin login rather than a directory of accounts to phish.
      </>
    ),
    body: (
      <>
        <LegalList
          items={[
            <>All traffic to and from the application runs over TLS.</>,
            <>
              The database has row-level security enabled with no public policies at all: the key that
              could reach the browser can read nothing, and only the server, holding a private service
              key, can read or write. That key never leaves the server.
            </>,
            <>
              There is one operator credential and no user accounts, no signup, and no password-reset
              flow — so there is very little to phish. The session cookie is signed and HTTP-only.
            </>,
            <>
              Access to the database and to call recordings is limited to the people who run the
              service, and call reviews are done for quality, not curiosity.
            </>,
          ]}
        />
        <LegalNote>
          Honest bit: we are a small company. We do not hold SOC 2, ISO 27001, or any other audited
          certification, and we are not going to imply otherwise on a page about honesty. If your
          procurement process needs a security review before you upload a list, ask us and we will
          answer every question truthfully, including the ones where the answer is{" "}
          <em>we do not have that</em>.
        </LegalNote>
        <p>
          If a breach affects your data, we will tell you promptly with what we know, what we have
          done about it, and what you should do — rather than a carefully worded paragraph three weeks
          later.
        </p>
      </>
    ),
  },
  {
    id: "elsewhere",
    title: "Children, and people outside the United States",
    short: (
      <>
        This is a tool for adults booking haircuts and treatments. We are hosted in the US, and
        sending us a list from elsewhere is a decision you need a lawful basis for.
      </>
    ),
    body: (
      <>
        <p>
          The service is sold to businesses and is not directed at children. We do not knowingly
          collect information about anyone under 16. If a list contains a minor&rsquo;s number, tell us
          and we will remove and suppress it.
        </p>
        <p>
          {LEGAL.entity} is based in the United States and our suppliers process data there. If you or
          the people on your list are outside the United States, uploading that list means transferring
          personal data to the US, and having a lawful basis for that transfer is your responsibility
          as the controller of it. If you need a data processing addendum or standard contractual
          clauses to make that work, ask us — we will sign a reasonable one.
        </p>
      </>
    ),
  },
  {
    id: "changes-contact",
    title: "Changes, and how to reach a human",
    short: (
      <>
        The date at the top is always the truth. Material changes come with an email, not a silent
        edit.
      </>
    ),
    body: (
      <>
        <p>
          We may update this policy as the product changes or a supplier changes. The{" "}
          <strong>Last updated</strong> date at the top of the page always reflects the current
          version, and for material changes we will email the address on your account before it takes
          effect.
        </p>
        <p>Questions, requests, deletions, or a complaint about a call:</p>
        <LegalList
          items={[
            <>
              <strong>Email:</strong>{" "}
              <a className="underline decoration-line underline-offset-4" href={`mailto:${LEGAL.email}`}>
                {LEGAL.email}
              </a>{" "}
              — this is the fastest route and a person reads it.
            </>,
            <>
              <strong>Post:</strong> {LEGAL.entity}, {LEGAL.address}
            </>,
            <>
              <strong>The number our calls come from:</strong> {LEGAL.outboundNumber}.
            </>,
          ]}
        />
        <p>
          The companion document is the{" "}
          <Link className="underline decoration-line underline-offset-4" href="/terms">
            Terms of Service
          </Link>
          , which covers who is responsible for the list in the first place. The two are meant to be
          read together.
        </p>
      </>
    ),
  },
];

export default function PrivacyPage() {
  return (
    <LegalLayout
      eyebrow="How we handle data"
      title="Privacy Policy"
      lede={
        <>
          <p>
            Salon Malone makes phone calls to real people about their haircuts, so a privacy policy
            here is not a formality. This one is short, specific, and names every supplier that
            touches anything.
          </p>
          <p>
            If you are one of the people we called and you want off the list forever, skip to{" "}
            <a className="underline decoration-line underline-offset-4" href="#your-rights">
              section 6
            </a>
            . It takes one sentence, and saying it on the call itself is enough.
          </p>
        </>
      }
      sections={sections}
      sibling={{
        href: "/terms",
        label: "Terms of Service",
        blurb:
          "The agreement itself: what the service does, who is responsible for the consent behind a list, how billing works, and what we will not promise.",
      }}
    />
  );
}
