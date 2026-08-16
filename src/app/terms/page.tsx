import type { Metadata } from "next";
import Link from "next/link";
import LegalLayout, {
  LEGAL,
  LegalHeading,
  LegalList,
  LegalNote,
  type LegalSection,
} from "@/components/LegalLayout";
import { SITE, bookingCallUrl } from "@/lib/site";

export const metadata: Metadata = {
  title: "Terms of Service",
  description:
    `The agreement between you and ${LEGAL.entity} for Salon Malone: what the service does, ` +
    "who is responsible for the list, how billing works, and what we do and do not promise. " +
    "Written in plain language.",
  alternates: { canonical: "/terms" },
};

const sections: LegalSection[] = [
  {
    id: "who-we-are",
    title: "Who you are dealing with",
    short: (
      <>
        Salon Malone is a product of <strong>{LEGAL.entity}</strong>, a Delaware company. When this
        page says <em>we</em>, that is who is on the hook.
      </>
    ),
    body: (
      <>
        <p>
          {SITE.name} and {SITE.domain} are products of {LEGAL.entityLong}, with its registered
          office at {LEGAL.address}. In this agreement, <strong>we</strong>, <strong>us</strong> and{" "}
          <strong>our</strong> mean {LEGAL.entity} — the company that bills you, answers your email
          and is on the other end of any argument. <strong>You</strong> means the business buying
          the service — the salon, med spa, or group of locations — and anyone you let use your
          account.
        </p>
        <p>
          These terms become the agreement between us on the earlier of two moments: you pay for a
          plan, or we run a campaign for you. There is no separate paperwork to sign and no
          negotiation ritual. This is the paperwork.
        </p>
        <p>
          The service is sold to businesses. It is not a consumer product, and nothing here is meant
          to create rights for the people we call on your behalf — although the{" "}
          <Link className="underline decoration-line underline-offset-4" href="/privacy">
            Privacy Policy
          </Link>{" "}
          describes exactly what they can ask us for, and we honour it whether or not they read a
          word of this.
        </p>
      </>
    ),
  },
  {
    id: "the-service",
    title: "What the service actually is",
    short: (
      <>
        We phone the lapsed clients on <em>your</em> list, ask for a specific time, and email you
        the moment someone says yes. That is the whole product.
      </>
    ),
    body: (
      <>
        <p>
          Salon Malone is an outbound voice agent. You give us a list of your own past customers who
          have stopped booking. Malone calls them as your virtual concierge, reads the offer you
          wrote, proposes two concrete times, and writes down the one they pick.
        </p>
        <p>What you get with it:</p>
        <LegalList
          items={[
            <>
              <strong>A booking email, immediately.</strong> Name, number, the slot in the client&rsquo;s
              own words, and a short summary of the call — sent as soon as the call report lands, so
              your front desk can confirm it while the chair is still open.
            </>,
            <>
              <strong>A Friday report.</strong> Dialled, reached, booked, declined, opted out, and
              estimated recovered revenue calculated as booked visits × the average ticket you gave
              us.
            </>,
            <>
              <strong>A scrub report on every upload.</strong> How many rows were kept, how many were
              dropped, and the reason for each one.
            </>,
          ]}
        />
        <LegalHeading>What it is not, so nobody is surprised in week two</LegalHeading>
        <LegalList
          items={[
            <>
              <strong>It is not a calendar integration.</strong> Malone cannot see your book and
              cannot write to it. The time is agreed out loud and your front desk confirms it. A
              booking email is a captured intention, not a confirmed appointment.
            </>,
            <>
              <strong>It cannot take payment</strong> and it will not discuss prices, medical
              questions, or anything other than getting someone back in the chair. It refers those to
              your front desk number.
            </>,
            <>
              <strong>There is no SMS and no chatbot.</strong> Voice calls and email. That is
              deliberate and it is not on a roadmap we are asking you to believe in.
            </>,
            <>
              <strong>Nobody gets called twice.</strong> One attempt per contact, per campaign, ever.
              No retry queue, no drip, no second pass next month.
            </>,
          ]}
        />
        <p>
          We may improve the service, change how it works under the hood, or swap a supplier, as long
          as we do not materially reduce what you are paying for. If we ever do reduce it, that is a
          material change and section 10 applies.
        </p>
      </>
    ),
  },
  {
    id: "your-list",
    title: "Your list and your consent",
    short: (
      <>
        This is the clause that matters most, so it is written straight. You own the list, you are
        the one calling, and by uploading a contact you are stating that this person gave you
        permission to phone them.
      </>
    ),
    body: (
      <>
        <p>
          Every campaign runs on contacts you supply. You are the sender of record for those calls.
          We place them for you, on your instruction, in your salon&rsquo;s name, with your offer. That
          makes the consent behind each number your responsibility, and it is not one we can take off
          your hands.
        </p>

        <LegalHeading>What you are warranting, for every row</LegalHeading>
        <p>By uploading a list, you represent and warrant that, for each contact on it:</p>
        <LegalList
          items={[
            <>
              You collected the contact directly, in the ordinary course of your own relationship
              with that person — they were your customer, or they asked you to contact them.
            </>,
            <>
              You have their <strong>prior express consent</strong> to contact them at that number
              for the purpose of offering appointments, and that consent has not been withdrawn.
            </>,
            <>
              You hold a record of that consent — what they agreed to, when, and how — and you can
              produce it if we or anyone else asks.
            </>,
            <>
              The number is theirs and is current as far as you know, and they have not told you to
              stop contacting them.
            </>,
          ]}
        />

        <LegalHeading>What you must not upload</LegalHeading>
        <p>
          You will not upload purchased, rented, scraped, appended, harvested, or otherwise
          third-party lists, or any number you cannot connect to a consent record of your own.
          Uploading one is a material breach of this agreement and grounds for immediate suspension or
          termination, without refund. This is not a fine-print trap: it is the single thing that
          would end this service for every other customer on it, so we treat it as a bright line
          rather than a conversation.
        </p>

        <LegalHeading>Our scrubbing is belt-and-braces, not a transfer of responsibility</LegalHeading>
        <p>
          Before anything dials, we drop rows that are not marked consented, drop numbers on our
          global do-not-call list, drop malformed numbers, de-duplicate, and hold everything outside
          local calling hours. Those gates exist to catch mistakes, and they catch a lot of them.
        </p>
        <p>
          They cannot, and do not, verify that consent genuinely exists. A spreadsheet column
          containing the word <em>yes</em> is a claim you are making, not a fact we can check. Our
          gates do not make us the sender, do not make us responsible for the lawfulness of your
          list, and do not reduce anything you warranted above.
        </p>

        <LegalHeading>Your own compliance obligations</LegalHeading>
        <p>
          You are responsible for complying with the laws that apply to calls made on your behalf.
          In the United States that includes the Telephone Consumer Protection Act and its state
          equivalents, state telemarketing registration where your state requires it, and the rules
          on recording calls where you and the person you are calling are located. Calls placed
          through the service are recorded and transcribed by our voice provider — see the{" "}
          <Link className="underline decoration-line underline-offset-4" href="/privacy">
            Privacy Policy
          </Link>{" "}
          — and where notice or all-party consent to recording is required, meeting that requirement
          is yours.
        </p>
        <p>
          You will tell us promptly if you learn that a row should not have been called, or that
          someone has complained, so we can suppress the number and stop.
        </p>

        <LegalHeading>Cover for us if this goes wrong</LegalHeading>
        <p>
          You will defend and indemnify {LEGAL.entity} against third-party claims, demands, fines and
          reasonable legal costs arising from contacts you supplied without the consent you warranted,
          from offer text you gave us, or from your other breach of this section. We will tell you
          promptly about any such claim, let you control the defence of it, and cooperate with you at
          your expense — we will not settle anything in your name behind your back.
        </p>

        <LegalNote>
          If your obligations are more specific than the average salon&rsquo;s — a franchise agreement,
          a med spa handling protected health information, an existing do-not-call policy, customers
          outside the United States — have your own counsel read this section before your first
          upload. We can tell you what our code does. We cannot tell you what your consent records
          are worth.
        </LegalNote>
      </>
    ),
  },
  {
    id: "our-side",
    title: "What we do on our side",
    short: (
      <>
        Five gates, written into the code rather than into a policy binder: consent, suppression,
        calling hours, one attempt, and Malone saying out loud that it is not a person.
      </>
    ),
    body: (
      <>
        <p>These are commitments about how we run the service, and they are how it is built:</p>
        <LegalList
          items={[
            <>
              <strong>Consent gate.</strong> A contact that is not marked consented in your upload
              never enters the dial queue. It is enforced when the list is imported and again in the
              query that picks up contacts to call.
            </>,
            <>
              <strong>Global do-not-call suppression, honoured instantly.</strong> When someone asks
              not to be called again, Malone ends the call and the number is written to a suppression
              list before the call report finishes processing. That list is global, not per-client:
              once a number is on it, it is never dialled again by us, for anyone, including you. It
              cannot be removed on request from a paying customer, and we will not do it as a favour.
            </>,
            <>
              <strong>Calling hours in the client&rsquo;s local time.</strong> We dial only inside the
              window configured for the location running the campaign, evaluated in that
              location&rsquo;s own timezone rather than ours or yours. The default window is 09:00 to
              19:00. If a timezone cannot be read, nothing dials.
            </>,
            <>
              <strong>One attempt per contact, per campaign. Ever.</strong> Enforced by the database
              query that claims contacts, not by anyone remembering to be careful.
            </>,
            <>
              <strong>Disclosure on every call.</strong> Malone identifies itself as your virtual
              concierge in its opening line, and if anyone asks whether it is a real person, a bot, or
              a recording, it answers immediately that it is a virtual assistant. It never claims to
              be human. There is no version of this that we will switch off for you.
            </>,
          ]}
        />
        <p>
          These are commitments about our design and our operation. They are not a warranty that
          software, telephone networks and third-party suppliers will never fail — see section 9 for
          what we do and do not stand behind.
        </p>
      </>
    ),
  },
  {
    id: "acceptable-use",
    title: "Acceptable use, or: behave like a salon",
    short: (
      <>
        This is an appointment-booking tool for your own past customers. It is not a boiler room, and
        we would like to keep it that way.
      </>
    ),
    body: (
      <>
        <p>
          You are responsible for everything done under your account, for keeping your credentials to
          yourself, and for the accuracy of what you tell us — including your average ticket, your
          timezone, and the phone number Malone reads out on voicemail.
        </p>
        <p>You will not use the service:</p>
        <LegalList
          items={[
            <>To call anyone who has not given you the consent described in section 3.</>,
            <>
              For debt collection, political calling, charitable solicitation, surveys, market
              research, or lead generation. It books appointments for your own lapsed clients. That
              is the entire permitted use.
            </>,
            <>
              To make an offer you cannot honour at the price and on the terms Malone reads out.
              People will arrive expecting it.
            </>,
            <>
              To make claims that are unlawful or that require a licence, qualification or approval
              you do not hold — medical or therapeutic claims, prescription products, financing
              offers, and anything a regulator would want to read twice.
            </>,
            <>
              To impersonate another business, or to run calls on behalf of a business that is not
              yours, without our written agreement.
            </>,
            <>
              To harass, mislead, threaten or pressure anyone, or to ask us to widen the calling
              window past what the law allows.
            </>,
            <>
              To resell the service, resell calls, or expose it to third parties as if it were your
              own product, without our written agreement.
            </>,
            <>
              To probe, scrape, overload or reverse-engineer the service, or to work around any of the
              gates in section 4.
            </>,
          ]}
        />
        <p>
          You write the offer text, or we write it with you and you approve it. Either way it goes out
          in your name and you are responsible for it being true.
        </p>
      </>
    ),
  },
  {
    id: "money",
    title: "Money",
    short: (
      <>
        Monthly plans bill in advance and keep going until you cancel. The $299 pilot is a one-off and
        renews into nothing. Cancel whenever you like; it stops at the end of the period you already
        paid for.
      </>
    ),
    body: (
      <>
        <LegalHeading>The plans</LegalHeading>
        <LegalList
          items={[
            <>
              <strong>Win-Back Pilot — $299, one time.</strong> One list, one campaign, one closing
              report. Not a subscription. Nothing renews and nothing is charged again.
            </>,
            <>
              <strong>Salon — $399 per month.</strong> One location, a rolling win-back campaign.
            </>,
            <>
              <strong>Med Spa — $999 per month.</strong>
            </>,
            <>
              <strong>Multi-Location — $2,499 per month.</strong> Up to ten locations.
            </>,
          ]}
        />
        <p>
          Prices are in US dollars and exclude any sales or other tax we are required to collect. Each
          plan states a monthly contact-dialling allowance on the{" "}
          <Link className="underline decoration-line underline-offset-4" href="/#pricing">
            pricing section
          </Link>
          . There is no per-minute billing, no per-lead invoice and no overage charge — the plan price
          is the plan price. If a list is far larger than your allowance, we will talk to you about it
          before dialling rather than quietly working through it.
        </p>

        <LegalHeading>How it is charged</LegalHeading>
        <p>
          Payments run through Stripe. We never see or store your card number. Subscriptions are
          billed monthly in advance, on the day of the month you started, and{" "}
          <strong>renew automatically until you cancel</strong>. You authorise those recurring charges
          when you subscribe.
        </p>
        <p>
          If a payment fails we may pause your campaigns until it clears. Nothing is deleted when that
          happens; the calls simply stop.
        </p>

        <LegalHeading>Cancelling</LegalHeading>
        <p>
          Email <a className="underline decoration-line underline-offset-4" href={`mailto:${LEGAL.email}`}>{LEGAL.email}</a>{" "}
          — one line is enough, and if your Stripe receipt carries a manage-subscription link that
          works too. Cancellation stops future renewals.
          You keep the service until the end of the period you have already paid for, and if you would
          rather we stopped calling immediately, say so and we will stop that day. No retention call,
          no exit survey, no three-step flow designed to wear you down.
        </p>

        <LegalHeading>Refunds, honestly</LegalHeading>
        <p>
          We do not offer an automatic or pro-rata refund for a period that has already started, and
          we do not offer a money-back guarantee. We would rather say that plainly here than imply a
          promise we have not made.
        </p>
        <p>
          What we do commit to: if something went wrong on our side — we billed you twice, we billed
          after you cancelled, we never ran the campaign you paid for — write to us and we will make
          it right, up to and including a full refund. Outside those cases, refunds are at our
          discretion, and you will get a straight answer either way, in writing, within five business
          days.
        </p>

        <LegalHeading>Price changes</LegalHeading>
        <p>
          If we change the price of a plan you are on, we will email you at least 30 days beforehand
          and the new price takes effect at your next renewal. Cancel before then and you never pay
          it.
        </p>
      </>
    ),
  },
  {
    id: "no-guarantee",
    title: "We do not guarantee bookings or revenue",
    short: (
      <>
        Nobody honest can promise you bookings. Every number on our website is illustrative
        arithmetic, labelled as such, and we have no customer results to show you yet.
      </>
    ),
    body: (
      <>
        <p>
          How a campaign performs depends on your list, your offer, your prices, your area, the time
          of year, and whether people enjoyed their last visit. We control none of those. We do not
          guarantee any number of answered calls, bookings, attended appointments, or dollars
          recovered, and nothing anyone at {LEGAL.entity} says in an email or on a call creates such a
          guarantee unless it is written into this agreement.
        </p>
        <p>
          <strong>The figures on {SITE.domain} are illustrative.</strong> The worked example on the
          front page is arithmetic we made up to show the shape of the maths, using assumptions we
          picked and labelled. It is not a customer result, a projection, or a promise. We have no
          customer results to publish. When we do, they will be labelled as what they are, with the
          business named only if that business agreed to it.
        </p>
        <p>
          <strong>The Friday report counts bookings, not attendance.</strong> Estimated recovered
          revenue is booked visits multiplied by the average ticket you gave us. We have no way of
          knowing who actually sat in the chair, so no-shows are included in our number and excluded
          from yours. Your own book is the last word. Please do not file our figure as revenue.
        </p>
      </>
    ),
  },
  {
    id: "suspension",
    title: "Suspension and termination",
    short: (
      <>
        You can leave any time. We can suspend immediately for a consent breach. Opt-outs survive
        everything — they are not yours to take with you.
      </>
    ),
    body: (
      <>
        <p>
          <strong>You.</strong> Cancel whenever you like, as described in section 6.
        </p>
        <p>
          <strong>Us, immediately.</strong> We may suspend or terminate your account without notice
          if you upload a list you do not have consent for, if you use the service for something in
          section 5, if your payment fails and stays failed, or if continuing would expose us or the
          people being called to legal risk. Where the breach is fixable and nobody is being harmed
          in the meantime, we will tell you what is wrong and give you a fair chance to fix it first.
        </p>
        <p>
          <strong>Us, ordinarily.</strong> We may end a subscription for any other reason on 30
          days&rsquo; notice by email, and we will refund anything you have paid for time you will not
          get.
        </p>
        <p>
          Termination for a consent breach is not refunded. Termination for our own convenience is.
        </p>
        <LegalHeading>What happens after</LegalHeading>
        <LegalList
          items={[
            <>We stop calling immediately.</>,
            <>
              We will export your campaign data — contacts, calls, bookings — in a normal file format
              if you ask within 30 days.
            </>,
            <>
              We delete or retain the rest as described in the{" "}
              <Link className="underline decoration-line underline-offset-4" href="/privacy">
                Privacy Policy
              </Link>
              .
            </>,
            <>
              <strong>The suppression list survives.</strong> Numbers that asked never to be called
              again stay suppressed permanently, across every account, including after yours closes.
              Those entries are not part of your data and you cannot take them, delete them, or ask
              for them back. That is what makes the promise to those people real.
            </>,
          ]}
        />
        <p>
          Sections 3, 6 (for amounts already owed), 7, 9 and 11 survive termination, because they are
          the ones that matter after the calling stops.
        </p>
      </>
    ),
  },
  {
    id: "limits",
    title: "Warranties, and the limits of our liability",
    short: (
      <>
        We run this carefully. We do not promise perfection, telephone networks, or that software will
        never mishear a Tuesday. What you can recover from us is capped at what you paid us in the
        last three months.
      </>
    ),
    body: (
      <>
        <p>
          Except for what is expressly promised in this agreement, the service is provided{" "}
          <strong>as is</strong> and <strong>as available</strong>, and to the fullest extent
          permitted by law we disclaim all implied warranties, including merchantability, fitness for
          a particular purpose, and non-infringement.
        </p>
        <p>
          We depend on third parties for telephony, speech recognition, language models, database,
          email and hosting. Outages, dropped calls, delayed emails and degraded audio happen. We do
          not offer an uptime commitment or a service-level guarantee, and we are not liable for
          failures of the public telephone network or of a supplier acting outside our control.
        </p>
        <p>
          <strong>The agent is software and it can be wrong.</strong> It can mishear a name, note a
          time incorrectly, or record an outcome that does not match what a human would have written
          down. Your front desk confirming every booking is a designed part of this process, not a
          workaround for a bug, and you should not treat a booking email as a confirmed appointment
          until you have confirmed it.
        </p>
        <p>
          Neither of us is liable to the other for indirect, incidental, special, consequential or
          punitive damages, or for lost profits, lost revenue, lost goodwill or lost data, even if
          warned they were possible.
        </p>
        <p>
          <strong>
            Our total aggregate liability under this agreement is capped at the amount you paid us in
            the three months before the event giving rise to the claim.
          </strong>{" "}
          On the $299 pilot, that is $299.
        </p>
        <p>
          Two carve-outs, in both directions. That cap does not apply to your indemnity in section 3,
          or to amounts you owe us. And nothing here limits liability that cannot lawfully be limited
          — including fraud, wilful misconduct, or death or personal injury caused by negligence.
        </p>
      </>
    ),
  },
  {
    id: "changes",
    title: "Changes to these terms",
    short: (
      <>
        We can update this page. If a change actually matters to you, you get 30 days&rsquo; notice by
        email and a chance to leave before it applies.
      </>
    ),
    body: (
      <>
        <p>
          We may revise this agreement — for a new feature, a new supplier, or a lawyer&rsquo;s
          sensible correction. The <strong>Last updated</strong> date at the top always reflects the
          current version.
        </p>
        <p>
          For material changes — anything that reduces what you get, increases what you pay, or adds
          an obligation — we will email the address on your account at least 30 days before it takes
          effect. Continuing to use the service after that date means you accept the new version. If
          you would rather not, cancel before it takes effect and the current version governs until
          your paid period ends.
        </p>
        <p>
          We will keep it in plain language. If a future revision reads like it was drafted by
          something that resents you, reply to the notice email and say so.
        </p>
      </>
    ),
  },
  {
    id: "legal-bits",
    title: "The legal odds and ends",
    short: (
      <>
        Delaware law, Delaware courts, the usual housekeeping. Nothing hidden in here, but read it
        anyway — that is rather the point of a contract.
      </>
    ),
    body: (
      <>
        <LegalList
          items={[
            <>
              <strong>Governing law.</strong> The laws of the State of Delaware, without regard to its
              conflict-of-law rules.
            </>,
            <>
              <strong>Where disputes go.</strong> The state and federal courts located in Delaware.
              Both of us consent to their jurisdiction and to venue there. Before filing anything,
              please email us — most of what looks like a dispute is a misunderstanding that survives
              about four minutes of conversation.
            </>,
            <>
              <strong>Entire agreement.</strong> This page, together with the Privacy Policy and the
              plan you bought, is the whole agreement between us about the service, and it replaces
              anything said beforehand.
            </>,
            <>
              <strong>Severability.</strong> If a court finds one clause unenforceable, that clause is
              trimmed to the minimum that works and the rest of the agreement stands.
            </>,
            <>
              <strong>No waiver.</strong> If we do not enforce something once, we have not given it
              up for good.
            </>,
            <>
              <strong>Assignment.</strong> You may not assign this agreement without our written
              consent. We may assign it to a successor in a merger, acquisition or sale of the
              business, and the obligations here follow it.
            </>,
            <>
              <strong>Independent parties.</strong> Nothing here creates a partnership, joint venture,
              franchise, agency or employment relationship. We are your supplier, not your staff.
            </>,
            <>
              <strong>Force majeure.</strong> Neither of us is liable for a failure caused by
              something genuinely outside our control — carrier outages, natural disasters,
              government action. Payment obligations are not excused by this.
            </>,
            <>
              <strong>Notices.</strong> To you, at the email address on your account. To us, at{" "}
              <a className="underline decoration-line underline-offset-4" href={`mailto:${LEGAL.email}`}>
                {LEGAL.email}
              </a>{" "}
              or by post to {LEGAL.entity}, {LEGAL.address}.
            </>,
          ]}
        />
      </>
    ),
  },
  {
    id: "contact",
    title: "Talking to an actual person",
    short: (
      <>
        One email address, one calendar link, and a phone number so you know which one shows up on
        your clients&rsquo; screens.
      </>
    ),
    body: (
      <>
        <p>
          Questions about this agreement, a refund, a strange invoice, or a call that did not go the
          way it should have:
        </p>
        <LegalList
          items={[
            <>
              <strong>Email:</strong>{" "}
              <a className="underline decoration-line underline-offset-4" href={`mailto:${LEGAL.email}`}>
                {LEGAL.email}
              </a>
            </>,
            <>
              <strong>Book fifteen minutes:</strong>{" "}
              <a className="underline decoration-line underline-offset-4" href={bookingCallUrl()}>
                {bookingCallUrl().replace(/^https:\/\//, "")}
              </a>
            </>,
            <>
              <strong>Post:</strong> {LEGAL.entity}, {LEGAL.address}
            </>,
            <>
              <strong>Our outbound number:</strong> {LEGAL.outboundNumber}. That is the number
              campaigns are dialled from, so if a client asks you who rang them, that is the answer.
            </>,
          ]}
        />
        <p>
          If you are one of the people Malone called and you want off the list, you do not need this
          page or an email — say <em>stop calling</em> on the call and it is done, immediately and
          everywhere. The{" "}
          <Link className="underline decoration-line underline-offset-4" href="/privacy">
            Privacy Policy
          </Link>{" "}
          explains the other ways to reach us.
        </p>
      </>
    ),
  },
];

export default function TermsPage() {
  return (
    <LegalLayout
      eyebrow="The agreement"
      title="Terms of Service"
      lede={
        <>
          <p>
            Most terms of service are written to be survived rather than read. This one is written to
            be read: same obligations, fewer Latin abbreviations, and a plain-English summary above
            every section so you can find the bit you came for.
          </p>
          <p>
            The summaries are there to help you navigate. The paragraphs underneath them are the
            actual agreement.
          </p>
        </>
      }
      notice={{
        label: "Before you read this",
        body: (
          <p>
            This is a plain-language agreement, and it is still a binding contract between your
            business and {LEGAL.entity} — not legal advice, and we are not your lawyers. If you
            operate under specific compliance obligations — state telemarketing registration,
            protected health information, a franchise agreement, an existing do-not-call policy, or
            customers outside the United States — have your own counsel review these terms, and
            particularly section 3, before you upload a list.
          </p>
        ),
      }}
      sections={sections}
      sibling={{
        href: "/privacy",
        label: "Privacy Policy",
        blurb:
          "Who holds what, which suppliers touch it, how long we keep it, and how anyone gets themselves off a list forever.",
      }}
    />
  );
}
