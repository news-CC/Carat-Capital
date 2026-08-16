# Salon Malone — cold outreach campaign (DRAFT, nothing sent yet)

Runs on the existing engine at `~/ai-workspace/job-postings-app/scrapers/vc/`
(`personalize.js` → queues, `send.js` → sends). That engine already does the things that keep a
cold campaign alive: pre-send address verification, hard-bounce suppression, `List-Unsubscribe`
one-click, a warm-up ramp, and per-account daily caps.

**Status: nothing is queued and nothing is sent.** Two things are missing — a prospect list, and
your go-ahead on the copy below.

---

## Sender identity

| | |
|---|---|
| From | `vijayravi1998@gmail.com` (already connected, `gmail.send`, last used 14 Aug) |
| Reply-to | `salon925malon@proton.me` |
| Postal line (CAN-SPAM) | Easecase, Inc., 1111b South Governors Avenue, Dover, DE 19904 |
| Unsubscribe | `https://www.startup25.com/unsubscribe?token=…` |
| Sent-by line | "Sent by Easecase, Inc. about Salon Malone. You're receiving this at a published business address." |

These are set per-campaign via `outreach_campaigns.profile`, so JobTheHunt's five live campaigns
keep their own Frisco TX address and jobthehunt.com unsubscribe links untouched.

## Pacing

Warm-up ramp is 10 → 15 → 20 → 25 → 30/day, then `daily_cap`. Proposed `daily_cap: 30`,
`monthly_cap: 600`.

The account-wide cap is 400/day **shared with the JobTheHunt campaigns already running on
`vijayravi1998@gmail.com`**. A salon campaign competes with those for the same budget and the same
sending reputation.

## Contact policy

Role inboxes only — `info@`, `hello@`, `bookings@`, `frontdesk@`. Never a named stylist or owner's
personal address. One address per business. This is the same policy the employer campaign already
follows, and it is the reason that campaign is on simple footing: a published business inbox whose
purpose is receiving business enquiries, no individual's personal data processed to find it.

---

## Variant A — "the ones who stopped"

**Subject:** `the clients who stopped coming in`

```
I built something for salons and I'd rather show you than pitch you.

Most salons have a few hundred clients who just stopped. Moved, got busy,
tried somewhere else. They're not angry — nobody ever called them.

Salon Malone is a virtual concierge that phones that list for you. It says
up front that it's a virtual assistant, makes whatever offer you choose,
books a specific time, and emails you the moment someone says yes. Friday
you get one email: who picked up, who booked, what it's worth.

It only calls people who consented, only inside your local business hours,
once each — never twice. "Stop calling" removes them permanently, mid-call.

$299 runs a 350-call pilot on your own list. If it works, it's $399/month
after. If it doesn't, you're out $299 and you know.

Want me to run one on {{firm}}'s list this week?

— Vijay
   startup25.com
```

## Variant B — "empty chair" (shorter, more direct)

**Subject:** `{{firm}} — the chair nobody booked yesterday`

```
Quick one.

Every salon has a list of clients who quietly stopped coming in. Most never
get called, because calling three hundred people is nobody's favourite
afternoon.

Salon Malone does it. A virtual concierge — it says so on the call — phones
your lapsed list, offers what you tell it to offer, books a time, and emails
you the second it lands. Consent-gated, business hours only, one attempt per
person, instant opt-out.

$299 for a 350-call pilot on your own list, then $399/month if you keep it.

Worth ten minutes? startup25.com — or just reply and I'll set it up.

— Vijay
```

---

## What is deliberately NOT in this copy

- **No testimonials, no logos, no "trusted by 200 salons", no case-study numbers.** There are zero
  customers. Every one of those would be fabricated, and a salon owner who checks would be right
  to never reply again.
- **No revenue promise.** No "recover $8,000/month". The site's worked example is labelled
  illustrative and the email makes no claim at all.
- **No fake urgency.** No expiring discount, no "3 pilot slots left".
- **No claim that anyone has used it yet.** "I built something" is true. "Salons are seeing…" is not.

## Compliance notes

- CAN-SPAM: accurate `From`, real subject, working one-click unsubscribe, physical postal address,
  opt-outs honoured. The engine enforces the mechanics; the postal address and unsubscribe host are
  now correct for Easecase, Inc.
- This is B2B to published business addresses. Some jurisdictions (notably Canada's CASL and the EU)
  are stricter than CAN-SPAM about implied consent — worth a look before sending outside the US.
- **Kinective's Legal team should review this copy and the terms it references before it goes out.**

## To launch, once a list exists

```bash
cd ~/ai-workspace/job-postings-app
node scrapers/vc/personalize.js --campaign <id>   # renders + queues, sends nothing
node scrapers/vc/send.js --campaign <id> --dry-run
node scrapers/vc/send.js --campaign <id>          # respects warm-up + caps
```
