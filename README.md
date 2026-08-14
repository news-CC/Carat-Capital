# Salon Malone

Runs paid win-back campaigns for salons and med spas. You upload a salon's lapsed client list, a scrub
drops every row that must not be called, a cron claims what survives and dials it, a voice agent
("Salon Malone") books a specific slot out loud, and the salon owner gets an email the moment a booking
lands plus a report every Friday.

One Next.js app on Vercel. Supabase is the only datastore. Vapi for voice, Resend for email, Stripe
payment links for billing. No queues, no Redis, no workers — Vercel Cron plus a `status` column on
`contacts` is the queue.

This is a runbook. If you are trying to get this deployed and working, read it top to bottom.

---

## The five tables

Defined in `supabase/migrations/0001_init.sql`. There are five and there is no sixth.

| Table | Holds |
|---|---|
| `clients` | The salon or med spa: contact email, `offer_text` that Malone reads aloud, `timezone`, `avg_ticket_cents`, `stripe_status`, `booking_phone`, `active`. |
| `contacts` | Uploaded list rows: `phone` (E.164, `NULL` when unusable), `phone_raw`, `consent`, `last_visit`, `status`, `scrub_reason`, `attempts`. Unique on `(client_id, campaign, phone)`. |
| `calls` | One row per dial attempt, always. `vapi_call_id` is unique, which is what makes the webhook idempotent. Outcome, duration, cost, transcript and recording URLs. |
| `suppression` | Global do-not-contact, keyed on `phone`. Not scoped to a client — an opt-out from one salon suppresses that number everywhere. |
| `bookings` | `slot_text` in the client's own words, `estimated_value_cents`, `notified_at`. |

RLS is enabled on all five tables with **zero policies**. That is deliberate and it is the whole access
model: the service role bypasses RLS, so every server-side query works, and the anon key can see
nothing at all. Do not add policies to "fix" it.

---

## Compliance gates

These are code, not conventions. Each one is enforced in at least two places, because the interesting
failure is not "the gate was missing", it is "the gate was bypassed by a code path nobody thought about".

| Gate | Where it is enforced |
|---|---|
| **Consent must be `true`** | `src/lib/scrub.ts` at upload (first gate, before anything else) · `claim_contacts_for_dialing` in `0001_init.sql` (`c2.consent = true`) · re-checked unconditionally in app code in `src/app/api/cron/dial/route.ts`. `contacts.consent` stores what the uploaded sheet said and nothing else — a row kept under `REQUIRE_CONSENT_FLAG=false` is stored `consent = false`, so it can never be claimed. A cell that says **no** out loud (`no`, `false`, `opt_out`, `dnc`, …) is dropped whatever the flag says: the flag may cover a blank cell, never a written refusal |
| **Never dial a suppressed number** | `src/lib/scrub.ts` against the live `suppression` table · `not exists` clause in the claim SQL · re-checked again in `dial/route.ts` before the call is placed. One implementation of the write in `src/lib/suppression.ts`, shared by the webhook and both admin paths |
| **Never dial outside the calling window** | `src/lib/call-window.ts` · the claim SQL compares `now() at time zone cl.timezone` against the window · re-checked in `dial/route.ts`. The window is in the **client's** timezone, not yours or the server's. An unparseable timezone returns `false` — it fails closed and does not dial |
| **One attempt per contact, ever** | `c2.attempts = 0` in the claim SQL. Not application memory, not a retry counter. A window miss is reverted rather than counted, so it is not spent as an attempt |
| **Opt-out is instant and global** | `src/app/api/vapi/webhook/route.ts`: writes `suppression`, pulls the number out of every client's pending queue, sets the contact to `opted_out` and the call to `opted_out` before returning — and answers **500** if the suppression row could not be written, so Vapi re-delivers rather than the opt-out being lost. Detected from the end-of-call structured data and, as a backstop, the phrase list in `src/lib/opt-out.ts` (`tests/opt-out.test.ts`), matched against the **caller's** turns only |
| **Malone always discloses it is not human** | `MALONE_SYSTEM_PROMPT` in `src/lib/malone.ts`. Mandatory in the opening line and again whenever asked. Mirrored in `scripts/setup-vapi.mjs`, which is what actually configures the assistant |

The browser-side scrub preview in the upload wizard is advisory only. The server action re-runs
`scrubRows` against the live suppression table, and the server is the gate.

> **Have counsel review this before you run a real campaign.** The gates above are an engineering
> implementation of a compliance posture; they are not legal advice and they are not a compliance
> program. Outbound calling is regulated (TCPA and state analogues in the US, with rules on consent,
> calling hours, disclosure, do-not-call handling and record keeping), the rules change, and what
> counts as valid consent for a *voice* call is not obvious from a spreadsheet column named `consent`.
> Have a qualified lawyer review the consent language your clients collect, your retention of that
> evidence, and this design, before the first real list is dialled.

---

## Setup, in order

The order matters. Each step needs the output of the one before it.

### 1. Install

```bash
npm install
cp .env.example .env.local
```

Fill in Supabase and Resend now; the rest is generated by later steps.

### 2. Apply the migration

```bash
node scripts/apply-migration.mjs
```

Prints the SQL with instructions. Paste it into the Supabase SQL Editor, or pipe it to your clipboard
with `node scripts/apply-migration.mjs --quiet | pbcopy`. If `SUPABASE_DB_URL` is set it also prints a
`psql` command that applies it directly.

The migration is idempotent, so re-running it is safe. There is no way to apply it over the REST API —
PostgREST cannot execute DDL. Do not add a generic `exec_sql` RPC to work around that.

Verify: the Table Editor lists all five tables, each marked RLS enabled with no policies.

### 3. Hash your admin password

```bash
printf %s 'a long passphrase you will remember' | node scripts/hash-password.mjs
```

Put the printed `ADMIN_PASSWORD_HASH=` line in `.env.local`, and set `ADMIN_EMAIL`. This pair is the
entire auth system — there is no user table and no signup. The hash also keys the session cookie HMAC,
so changing it signs you out.

### 4. Stripe

```bash
npm run setup:stripe -- --dry-run   # look first
npm run setup:stripe
```

Creates four products with prices and payment links: `sm_salon_399` ($399/mo), `sm_medspa_999`
($999/mo), `sm_group_2499` ($2,499/mo) and `sm_pilot_299` ($299 one-time). Idempotent — every object is
looked up by its `sm_sku` metadata before anything is created, so re-running never duplicates.

Paste the printed env lines. Each plan needs **both** forms: the server copy and the `NEXT_PUBLIC_`
copy, because the pricing buttons are rendered in the browser and Next.js only inlines `NEXT_PUBLIC_`
variables.

Then add the webhook: Stripe dashboard → Developers → Webhooks → Add endpoint, pointed at
`https://<your-domain>/api/stripe/webhook`, subscribed to `checkout.session.completed`,
`customer.subscription.updated`, `customer.subscription.deleted` and `invoice.payment_failed`. Copy the
signing secret into `STRIPE_WEBHOOK_SECRET`.

### 5. Vapi

```bash
npm run setup:vapi -- --dry-run
npm run setup:vapi
```

Creates or updates the "Salon Malone" assistant (looked up by name, so it updates in place) and
provisions a free Vapi phone number if the account has none. Prints `VAPI_ASSISTANT_ID`,
`VAPI_PHONE_NUMBER_ID`, and a generated `VAPI_WEBHOOK_SECRET` if you had not set one.

The prompt, voice config and analysis plan are **not** duplicated in the script — it imports
`maloneAssistantPayload()` from `src/lib/malone.ts`, which is the only place the persona is defined.
Edit `malone.ts`, re-run this, done. That import needs a Node that strips TypeScript types: **Node
≥ 22.18** (no flag). On Node 22.6–22.17 add `--experimental-strip-types`; the script says so if the
import fails. The dry run also reports when the *deployed* assistant's prompt or webhook URL has
drifted from the repo, which is the state to check before any demo call.

If it generated the secret, **save it immediately** — the assistant was configured with it and it is
stored nowhere else. Lose it and every webhook delivery is rejected with a 401, which looks exactly like
"calls happen but nothing is ever recorded".

If Vapi reports no free numbers left, the script says so and lists the options (buy a Vapi number,
import a Twilio number, or reuse an existing one — a re-run picks up any number already on the account).

`src/lib/malone.ts` is the source of truth for the prompt. `scripts/setup-vapi.mjs` keeps a hand-synced
copy because it is a plain `.mjs` script and cannot import TypeScript. The script reports when the
deployed prompt no longer matches, so edit `malone.ts`, re-sync the block, and re-run.

### 6. Vercel environment

Put every variable from `.env.example` into Vercel → Settings → Environment Variables, for all
environments. Set `NEXT_PUBLIC_APP_URL` to the real deployed origin with no trailing slash.
`CRON_SECRET` should be a long random string (`openssl rand -hex 32`).

### 7. Deploy

```bash
npm run typecheck && npm test && npm run build
```

Then deploy. `vercel.json` registers the two cron jobs.

### 8. Point the Vapi webhook at the deployed URL

The assistant's `serverUrl` was set from `NEXT_PUBLIC_APP_URL` when you ran `setup:vapi`. If that was
still `localhost`, or the domain has changed since, re-run against the real origin:

```bash
npm run setup:vapi -- --url=https://your-domain.com
```

This patches the existing assistant in place. You can confirm it in the Vapi dashboard: the assistant's
server URL must be `https://your-domain.com/api/vapi/webhook` and its secret must equal
`VAPI_WEBHOOK_SECRET` in Vercel. Those two facts are the single most common reason a demo "works" while
no call, booking or opt-out is ever written.

### 9. Smoke test

```bash
curl -s https://your-domain.com/api/health | jq
```

Returns 200 with `ok: true` when the database is reachable and no required variable is missing, 503
otherwise. Anonymous callers get liveness only (`ok`, `service`, `time`) — which secrets are set is a
map of the deployment, so the detail is for the operator. Add the cron bearer (or call it with an
admin session in the browser) to see the `env` map, the `missing` array and the database error:

```bash
curl -s -H "Authorization: Bearer $CRON_SECRET" https://your-domain.com/api/health | jq
```

Then log in at `/login` and confirm `/admin` renders.

Trigger a cron by hand:

```bash
curl -s -H "Authorization: Bearer $CRON_SECRET" https://your-domain.com/api/cron/dial
```

With nothing queued this returns a claimed count of zero, which is a successful smoke test.

---

## Environment variables

| Variable | Required | Notes |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | yes | Project URL. |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | yes | Sees nothing — RLS has no policies. |
| `SUPABASE_SERVICE_ROLE_KEY` | yes | Bypasses RLS. Server only, never shipped to the browser. |
| `NEXT_PUBLIC_APP_URL` | yes | Public origin, no trailing slash. |
| `NEXT_PUBLIC_BOOKING_CALL_URL` / `BOOKING_CALL_URL` | yes | The one CTA on the marketing page. |
| `ADMIN_EMAIL` | yes | The only account. |
| `ADMIN_PASSWORD_HASH` | yes | `scrypt$<saltHex>$<keyHex>` from `scripts/hash-password.mjs`. Also keys the session HMAC. |
| `VAPI_API_KEY` | yes | Private key. |
| `VAPI_ASSISTANT_ID` | yes | From `setup:vapi`. |
| `VAPI_PHONE_NUMBER_ID` | yes | From `setup:vapi`. No dialling without it. |
| `VAPI_WEBHOOK_SECRET` | yes | Must match the assistant's configured secret, or every webhook 401s. |
| `RESEND_API_KEY` | yes | Booking alerts and the Friday report. |
| `EMAIL_FROM` | yes | Use a verified domain. `"Salon Malone <malone@yourdomain.com>"`. |
| `STRIPE_SECRET_KEY` | yes | `setup:stripe` reads it and never prints it. |
| `STRIPE_WEBHOOK_SECRET` | yes | Signing secret for `/api/stripe/webhook`. |
| `STRIPE_LINK_SALON_399` · `_MEDSPA_999` · `_GROUP_2499` · `_PILOT_299` | yes | Server copies. |
| `NEXT_PUBLIC_STRIPE_LINK_SALON_399` · `_MEDSPA_999` · `_GROUP_2499` · `_PILOT_299` | yes | Same URLs. The pricing buttons read these in the browser. |
| `CRON_SECRET` | yes | Bearer token for the cron routes. Vercel's own `x-vercel-cron` header is also accepted. |
| `CALL_WINDOW_START` / `CALL_WINDOW_END` | no | `HH:MM`, 24h, in each client's local time. Defaults `09:00` / `19:00`. |
| `REQUIRE_CONSENT_FLAG` | no | Only the exact string `false` relaxes the upload gate, and only for a **blank** consent cell — a cell that says no is still dropped, and rows kept this way are stored `consent = false`, which the dialer's hard gate never claims. Do not set it. |
| `MAX_CONCURRENT_CALLS` | no | Default 8. The standard plan has 10 lines; leave headroom. |
| `DIAL_FICTIONAL_NUMBERS` | no | Only the exact string `true` lets the dialer place calls to the 555-01XX reserved-for-fiction range. Off by default; the demo list is built entirely from that range, so turning it on buys billed failures and burns those contacts' one attempt. |
| `SUPABASE_DB_URL` | no | Scripts only, never read by the app. Lets `apply-migration.mjs` offer a `psql` command. |

`src/lib/env.ts` is the only module permitted to read `process.env`. Add new variables to its
`ServerEnvKey` union.

---

## Cron, and the Vercel plan caveat

`vercel.json` registers two jobs:

| Path | Schedule | Does |
|---|---|---|
| `/api/cron/dial` | `*/5 * * * *` | Expires rows stuck in `calling`, claims pending contacts inside their window, dials up to the concurrency cap. |
| `/api/cron/report` | `0 20 * * 5` | Friday, the weekly report per **billable** client (`trialing`, `active`, `past_due`). Deliberately not `clients.active`: that is the campaign on/off switch, and a salon dialled Monday to Wednesday still earned its wrap-up if you paused it on Thursday. `canceled` gets nothing, and a client with no calls in the period is skipped. |

**A five-minute schedule needs a Vercel Pro plan.** Hobby projects are limited to a small number of
cron jobs that run at most once a day, and Vercel will either reject the schedule or quietly run it
daily. On Hobby, `*/5 * * * *` is not a working dialer. Either upgrade to Pro, or drive the endpoint
from an external scheduler with the `CRON_SECRET` bearer token:

```bash
curl -s -H "Authorization: Bearer $CRON_SECRET" https://your-domain.com/api/cron/dial
```

Cron schedules are UTC. `0 20 * * 5` is 4pm Eastern in summer and 3pm Eastern in winter — if the Friday
report must land at a specific local hour year-round, adjust it at the daylight-saving boundary.

---

## Running the demo

```bash
npm run demo:clientele
```

Writes `demo/salon-malone-demo-clientele.xlsx` — 250 synthetic rows, all phones in the `555-01NN`
range reserved for fiction, all emails `@example.com`. Upload it to a demo client and the scrub should
drop 44 of 250 rows and tell you why for each. To actually hear Malone, use a *separate* client whose
list is one row: your own mobile, consent `TRUE`.

Full walkthrough, expected numbers, and why you should not start a campaign on the 250-row list:
[`demo/README.md`](demo/README.md).

---

## Operating notes

- **Review calls by hand for the first two weeks.** Five a day, from `/admin/calls`. Prompt fixes beat
  code fixes; the transcript tells you what to change in `offer_text` or in `malone.ts`.
- Recordings and transcripts are not copied anywhere. Only Vapi's URLs are stored.
- Every dial attempt writes a `calls` row, including failures. A call that happened without a row is a
  bug worth chasing.
- The Vapi webhook answers 200 for anything it cannot use — malformed JSON, an unexpected shape, an
  event type we ignore — so a poison payload is never retried forever. It answers **500** only when a
  write a re-delivery could repair was lost (above all the suppression row, but also the `calls` row,
  the booking and the contact status), because Vapi re-delivering the report is the only second chance
  those writes get. A bad secret is a 401. Everything else goes to the Vercel logs; the line worth
  alerting on is `[vapi-webhook] SUPPRESSION WRITE FAILED`, which after Vapi exhausts its retries is
  the only trace that someone asked to be left alone and was not recorded.
- v1 observability is the Supabase tables plus Vercel logs. That is the whole plan.

---

## What v1 deliberately does not do

Not oversights. If you want one of these, it is a decision to make on purpose, with a reason.

- **No SMS.** No Twilio. Voice and email only.
- **No second attempt.** One dial per contact, ever. No retry queue, no drip.
- **No mid-call tool calls.** Malone cannot see a calendar or take payment. The slot is spoken and then
  extracted from the transcript afterwards, because a mid-call tool round trip breaks the sub-second
  voice turn that makes the agent feel human.
- **No in-app checkout.** Billing is Stripe payment links, out of band.
- **No user accounts.** One env-based admin credential. No signup, no roles, no password reset.
- **No multi-tenancy abstractions.** A `clients` table is enough.
- **No queues, Redis, workers or microservices.** Cron plus a status column.
- **No realtime dashboards, feature flags, observability platform or multi-region.**
- **No component library and no dark mode.** No settings pages.
- **No blog, no pricing matrix, no chatbot** on the marketing page. One headline, one CTA.

---

## Layout

```
src/lib/            env, types, phone, scrub, opt-out, suppression, calls, call-window,
                    next-path, money, revenue, auth, result
src/lib/email/      Resend wrapper + the booking alert and Friday report templates
src/lib/malone.ts   the voice persona — source of truth for the prompt
src/app/api/        cron/dial, cron/report, vapi/webhook, stripe/webhook, health
src/app/admin/      the admin app (server components + server actions)
scripts/            setup-stripe, setup-vapi, apply-migration, hash-password, demo clientele
supabase/migrations 0001_init.sql — five tables, indexes, RLS, the claim RPC
demo/               synthetic clientele and the demo walkthrough
tests/              the scrub, phone, call-window, opt-out and next-path gates
```

```bash
npm run dev         # local
npm run typecheck   # tsc --noEmit
npm test            # vitest — the compliance gates
npm run build       # must pass before deploying
```

Tests cover the scrub, phone normalisation and the calling window. Those are the gates; the rest of v1
is deliberately untested.
