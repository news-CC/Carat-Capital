# WIN-BACK PIPELINE — BUILD BRIEF (v1)

Goal: a boring, working app that runs paid win-back campaigns for salons/med spas.
Success = first real campaign for a paying client. Nothing else counts.

## PRIME DIRECTIVE: KEEP IT STUPID
- One Next.js app (App Router) on Vercel. Server Actions > API route sprawl.
- Supabase = the only database. No Redis, no queues, no workers. Vercel Cron + a
  `call_queue` table IS the queue.
- No component library beyond minimal Tailwind. No dark mode. No settings pages.
- Single admin login (env-based credentials). No user auth system. No signup.
- NO SMS in v1. NO Twilio. Voice (Vapi) + email (Resend) only.
- NO multi-tenancy abstractions. A `clients` table is enough.
- If a feature is not in this file, do not build it. Ask first.

## STACK (already provisioned — keys in .env.local)
Next.js / Vercel · Supabase · Vapi (voice + free number) · Resend · Stripe payment links.

## DATA MODEL (5 tables, that's all)
- `clients` — the salon/med spa: name, contact, offer_text, timezone, stripe_status
- `contacts` — uploaded list rows: client_id, name, phone, email, consent (bool),
  last_visit, status (pending/called/booked/declined/suppressed)
- `calls` — one row per attempt: contact_id, vapi_call_id, outcome, duration,
  transcript_url, cost
- `suppression` — global do-not-contact: phone, reason (opt_out/dnc/complaint)
- `bookings` — contact_id, slot_text, confirmed (bool)

## FLOWS (build in this order, one slice at a time)
1. **Upload:** admin uploads CSV/XLSX → parse client-side → insert to `contacts`.
2. **Scrub (HARD GATE, server-side, before anything dials):**
   drop rows where consent != true; drop matches in `suppression`;
   drop malformed phones; dedupe. Log counts.
3. **Queue & dial:** cron picks pending contacts inside CALL_WINDOW (client's
   local time), calls Vapi outbound `/call` with assistantId + per-customer
   variable overrides (first_name, salon_name, offer). Max 1 attempt per contact
   per campaign. Ever.
4. **Webhook:** Vapi call-status webhook → update `calls` + `contacts.status`;
   "remove me" → insert to `suppression` immediately.
5. **Booking:** agent captures a slot verbally → webhook writes `bookings` →
   Resend email to salon owner instantly with the details.
6. **Friday report:** cron → Resend email per client: reached / booked /
   estimated recovered revenue. This email is the retention product. Make it clean.

## COMPLIANCE GATES (code, not comments)
- Never dial without consent=true. Never dial suppressed. Never dial outside
  CALL_WINDOW local time. One attempt max. Opt-out honored instantly and globally.
- Agent always discloses it's a virtual assistant. No exceptions.

## MARKETING SITE (startup25.com)
One page. Headline: "Your dead client list is buried money."
Sub: pay-per-show offer. One CTA: book-a-call link + Stripe payment links.
No blog, no pricing matrix, no chatbot. Ship it ugly-fast; SEO comes later.

## VOICE PERSONA — "SALON MALONE" (Vapi system prompt)
You are Salon Malone — {salon_name}'s virtual concierge. Smooth, warm, quick.
Pizazz, not pressure. You sound like the coolest front-desk person alive.

Rules of flow:
- Open honest + slick: "Hey {first_name} — Salon Malone here, {salon_name}'s
  virtual concierge. Ninety seconds, I promise. We miss you."
- ONE goal: book a specific slot using {offer_text}. Offer two concrete times.
- Short lines. No belaboring. Never repeat a pitch twice. Never argue.
- Warm no? "All love — the chair's here when you're ready." End call.
- "Stop calling"? "Done — you're off the list. Be good." End call, flag opt-out.
- Voicemail? One breezy 15-second message with the offer + salon's real number.
- Never claim to be human. Never discuss anything but the visit. 90s target,
  3 min hard max.

## DEFINITION OF DONE (v1)
- I upload a CSV, scrub runs, Salon Malone calls MY phone, books me, the
  booking email arrives, the Friday report renders. Deployed on Vercel.
- Timebox: one week. When done → repo freezes, selling starts.
