# Startup25 — Investor Strategy & Business Plan

**Working draft · 20 August 2026 · Confidential — do not merge to `main` (this repo deploys to the public site)**

This document does three things the founding team asked for:

1. Audits, step by step, how plausible the stated idea is — *"Salon Malone renamed to Startup25: a marketing company gathering a lot of data on clients and using that data to help businesses tailor-sell their products, funded by VC."*
2. Reshapes it into the version that is actually fundable in 2026, without throwing away what has already been built.
3. Lays out the full plan: market, moat, model, go-to-market, financial path, the raise, the pitch, and a 90-day action list.

It is written to be honest, not encouraging. Where a number is an assumption, it says so — the same discipline the Salon Malone landing page already practices.

---

## 1. Where we stand today (the honest baseline)

What exists, as of this week:

| Asset | State |
|---|---|
| **Salon Malone** — AI voice win-back concierge for salons & med spas | Landing page live at `/salon-malone/`. Consent-gated, one-attempt-ever, local-hours-only, discloses it's AI on every call. Pricing published: $299 pilot · $399/mo Salon · $999/mo Med Spa · $2,499/mo Multi-Location. **Zero customers.** |
| **Compliance posture** | Unusually strong for a student project: consent gate at import, global do-not-call written mid-call, fails-closed timezone logic, no-rebuttal script, AI disclosure in the opening line. This is a real asset — most competitors bolt this on later, badly. |
| **Easecase, Inc.** | Delaware entity, Dover registered agent. `startup25.com` in the footer. |
| **Team** | NYU students. Credibility with student-founder capital; a "who goes full-time?" question with everyone else. |
| **Carat Capital** | A daily jewelry-trade publication with a working content machine (editions, social carousels, a podcast). Separate business — but a distribution weapon and a door into a future vertical (jewelry retail). |
| **Roomy's** | An operating jewelry store in the family. A captive design partner for a jewelry-vertical pilot: zero sales cycle, real data. |

The single most important fact in this table is **zero customers**. Every strategic decision below is downstream of it.

---

## 2. The idea as stated — a step-by-step plausibility audit

The stated idea: *rename to Startup25, become a marketing company that gathers a lot of data on clients, and use that data to help many businesses tailor-sell products; raise VC to do it.*

### Step 1 — Is the underlying problem real?

**Yes, emphatically.** Appointment businesses bleed revenue through client lapse and have no capacity to fight it:

- ~70% of first-time salon visitors never rebook a second appointment ([Phorest](https://www.phorest.com/us/blog/fully-booked-salon-client-retention/)); industry-average first-visit retention runs roughly 30–45%, with only the best salons reaching 60–75% ([Callpad](https://www.callpad.ai/post/salon-client-retention-rate-benchmarks-improve)).
- Only ~14% of that churn is about price — most is lack of follow-up and friction ([Jeri Commerce](https://blog.jericommerce.com/resources/spas-salons-medspas-retention-statistics)). Nobody calls the lapsed client. That is the gap Malone fills.
- Targeted win-back campaigns recover on the order of 22–28% of lapsed clients when done well ([Jeri Commerce](https://blog.jericommerce.com/resources/spas-salons-medspas-retention-statistics)) — and almost no salon runs them, because the front desk has no time and email gets ignored.

**Verdict: strong.** The problem is real, measurable in dollars, and chronically unsolved.

### Step 2 — Is "a marketing company" fundable by VC?

**Not as a company type.** VCs fund *software* (80%+ gross margins, revenue that compounds without headcount), not *services* (agencies are valued at 1–3× revenue and scale linearly with people). The phrase "marketing company" in a pitch reads as "agency" and ends the meeting.

The fix is framing, not substance: what has been built **is already software**. Startup25 must pitch as a **product company with a service-grade onboarding layer** ("we write the offer with you" is concierge onboarding, not an agency).

**Verdict: fundable only if positioned as a platform, never as a marketing company.**

### Step 3 — Is "gathering a lot of data on clients" viable as the core strategy?

This is the step that needs the most surgery. Three problems with the literal version:

1. **Cold start.** Data is an *outcome* of scale, not a starting strategy. With zero customers there is zero data; you cannot raise on an asset you don't have yet.
2. **Regulatory gravity.** Cross-business use of consumers' personal data walks into CCPA/CPRA and ~20 state privacy laws, data-broker registration regimes, and FTC attention. Meanwhile the FCC ruled in Feb 2024 that AI-generated voices fall under the TCPA's "artificial or prerecorded voice" rules ([FCC](https://www.fcc.gov/document/fcc-makes-ai-generated-voices-robocalls-illegal)) — the consent bar for the calling channel is already high (§8 covers this in detail).
3. **Self-contradiction.** The Salon Malone page promises, verbatim: *"It runs your campaigns and nothing else. We never sell it, share it, or dial it for another salon."* That promise is why a salon will hand over its client list at all. A pivot to cross-client data monetization breaks the exact trust the product depends on.

But the *instinct* behind the idea — data compounds, and tailored selling beats generic marketing — is correct and is precisely what makes this venture-scale. It just has to attach to the **right layer of data** (see §7: monetize *intelligence*, never *identities*).

**Verdict: as stated, weak (a data-broker play a 2026 VC will not touch). Reframed as an outcome-data flywheel, it becomes the moat slide.**

### Step 4 — Does the market want this product right now?

**The timing evidence is unusually strong:**

- Voice AI is a funded, validated category: roughly **$4.5B went into 68 voice-AI companies between Oct 2024 and Mar 2026** ([AgentVoice market map](https://agentvoice.com/blog/ai-voice-agents-funding-market-map/)).
- SMB front-desk voice agents specifically are raising: Newo.ai took a **$25M Series A** for SMB front-desk voice ([Tech Funding News](https://techfundingnews.com/newo-ai-raises-25m-series-a-voice-infrastructure/)); Beside raised **$32M** for an AI receptionist ([Fortune](https://www.fortune.com/2025/11/11/beside-ai-voice-startup-raises-32-million-ai-receptionist-for-small-business/)); at the stage that matters to us, **Linda AI ($3.1M pre-seed, Feb 2026), Voicebit ($2.7M pre-seed, Mar 2026), and Certus AI ($500K pre-seed)** all got funded as *vertical* phone agents ([Synaptic](https://synaptic.com/resources/tip-offs/ai-voice-agent-startups-and-founders)).
- The strongest single signal: **GlossGenius — salon software — just raised $44M at a $1.15B valuation (July 2026) and rebranded to "Genius AI" to build "AI operations for all service businesses"** ([Fortune](https://fortune.com/2026/07/21/glossgenius-rebrand-genius-ai-small-businesses-beauty-unicorn-series-d/)). A billion-dollar company is repositioning onto this exact thesis. That validates the prize and starts a clock (§6 addresses the threat honestly).

**Verdict: timing is a tailwind, and it is citable.**

### Step 5 — Can this team raise VC *today*?

**No — and trying now would waste the best introductions.** With zero customers, the pitch is a landing page and a plan; pre-seed investors in this category are funding *live agents with early revenue*. The good news: the distance from here to "raisable" is short — roughly ten paying pilots and three written case studies (§12). The team's student status is an asset on this path, not a liability: NYU's Entrepreneurial Institute / Leslie eLab, the Innovation Venture Fund, student-founder funds, and YC all pattern-match "students who shipped a vertical AI agent with real revenue."

**Verdict: raisable in months, not now. Traction first, then the round prices itself.**

### Step 6 — Is the rename to "Startup25" right?

Split decision. **As the company umbrella: fine** — the domain exists and a neutral parent name leaves room for many verticals. **As the customer-facing brand: weak** — it's generic, it will age (the "25" dates it immediately), and it means nothing to a salon owner. Meanwhile "Malone" — the concierge with a name, a voice, and manners — is genuinely distinctive and already carries the product's personality.

**Recommendation:** Startup25, Inc. (or keep Easecase legally, d/b/a Startup25) as the company; **Malone** as the agent brand across every vertical: *Salon Malone, Med Spa Malone, Jeweler Malone* — or simply "Malone by Startup25." Customers buy Malone; investors buy Startup25.

### Step 7 — Net plausibility score

| Version | Fundability | Why |
|---|---|---|
| As stated ("marketing company gathering lots of client data") | **3/10** | Agency framing + data-broker framing + cold start + contradicts own trust promise |
| Reframed (§3: vertical AI revenue agent with an outcome-data flywheel) | **7–8/10**, gated on pilot traction | Real problem, proven willingness to fund the category at pre-seed, working compliance moat, unfair distribution assets |

The rest of this document is the 7–8/10 version.

---

## 3. The reframe — what Startup25 actually is

**One-liner:**

> **Startup25 builds Malone, an AI revenue agent for appointment businesses. Malone turns the client list every local business already owns into booked revenue — starting with win-back calls — and every call teaches the system which offer, timing, and script fills chairs in each vertical.**

Three sentences of investor logic underneath it:

1. **System of action, not a dashboard.** Malone doesn't report on lapsed clients; it phones them, books them, and emails the front desk the yes. SMBs pay for outcomes, and outcomes are measurable here to the dollar (the Friday report already does this).
2. **The data story, done legally.** Client lists stay sacred and siloed per business — that promise is permanent. What compounds across the network is *anonymized outcome data*: which offer converts a 9-month-lapsed color client, what answer rates look like at 11am Tuesday for med spas, which scripts get a yes in 90 seconds. At 1,000 businesses, Startup25 knows more about what wins back a lapsed service client than anyone alive — and no competitor can shortcut that corpus. This is "gathering a lot of data and tailoring selling" in the only form that survives 2026 privacy law *and* the company's own promises.
3. **Wedge → platform.** Win-back is the beachhead because it has the cleanest ROI math in SMB software ($399 in, ~$3,000–4,000 of illustrated bookings out). The same phone + list + consent infrastructure then carries no-show rescue, waitlist fill, reminder confirmations, and inbound overflow — and the same playbook carries into med spa, dental, veterinary, auto service, and jewelry retail.

---

## 4. Market — bottom-up, no hand-waving

| Segment | Count (US) | Notes for our ICP |
|---|---|---|
| Hair & nail salons | ~1.42M businesses ([IBISWorld](https://www.ibisworld.com/united-states/number-of-businesses/hair-nail-salons/1718/)) | Majority are solo operators/booth renters. Serviceable slice: multi-chair salons on booking software — est. 100–150K. |
| Barbershops | ~155K ([IBISWorld](https://www.ibisworld.com/united-states/number-of-businesses/barber-shops/5806/)) | Lower ticket; good for volume plans. |
| Med spas | ~11.5K (AmSpa 2025 forecast, [via](https://www.bookpinch.com/blog/expansion-us-medical-spa-industry)) | The premium ICP: ~$17B industry, average location revenue ~$1.4–2M/yr ([AmSpa / Boulevard benchmarks](https://leadresponse.co/blog/med-spa-industry-statistics)). High ticket → one recovered client can pay for a year of Malone. |
| Adjacent verticals (later) | Dental ~130K practices, veterinary ~30K clinics, auto repair ~230K shops, independent jewelers ~20K (estimates) | Same lapse mechanics, same phone channel, higher tickets in several. |

**SAM math (deliberately conservative):** 20,000 businesses at a $500/mo blended plan ≈ **$120M ARR**. That is <2% of the professionalized salon/med-spa universe and ignores every later vertical. The hair & nail *services* market alone is ~$90B/yr ([IBISWorld](https://www.ibisworld.com/united-states/number-of-businesses/hair-nail-salons/1718/)); Malone monetizes a sliver of the revenue it recovers into that market. A venture-scale outcome does not require heroic penetration — it requires surviving SMB churn (§15).

---

## 5. Why now (the slide investors actually check)

1. **Voice AI crossed the uncanny floor.** Sub-second, natural, interruptible conversation became commodity infrastructure (Vapi/Retell/Bland et al.) — the differentiation moved up-stack to workflow, compliance, and data. Startup25 is built exactly up-stack.
2. **Capital validated the category** — $4.5B across 68 voice-AI companies in ~18 months ([AgentVoice](https://agentvoice.com/blog/ai-voice-agents-funding-market-map/)), with pre-seed checks going to vertical phone agents monthly ([Synaptic](https://synaptic.com/resources/tip-offs/ai-voice-agent-startups-and-founders)).
3. **The incumbent proved the prize.** GlossGenius → Genius AI at $1.15B to chase "AI operations for service businesses" ([Fortune](https://fortune.com/2026/07/21/glossgenius-rebrand-genius-ai-small-businesses-beauty-unicorn-series-d/)).
4. **Owned-audience economics.** Paid acquisition costs keep climbing; the cheapest revenue any salon can buy is a client it already served. The channel shift favors first-party-list activation — exactly Malone's job.
5. **Regulatory clarity rewards the compliant.** The FCC's 2024 ruling put AI voices squarely under TCPA ([FCC](https://www.fcc.gov/document/fcc-confirms-tcpa-applies-ai-technologies-generate-human-voices)); the one-to-one consent rule was vacated in 2025; the Fifth Circuit's *Bradford* decision (Feb 2026) softened the written-consent standard in three states only ([Henson Legal](https://www.henson-legal.com/ai-voice-compliance)). Net: the rules are now knowable, and Malone was *designed to the strict reading before it had a single customer*. Cowboys will get sued out of this market; that is a moat.

---

## 6. Competition — and the honest answer to "why won't Genius AI kill you"

| Bucket | Who | What they do | Why Malone wins the job |
|---|---|---|---|
| Vertical booking/CRM suites | Genius AI (ex-GlossGenius), Boulevard, Vagaro, Mindbody, Zenoti, Mangomint, Square Appointments | Own the calendar; send SMS/email reminders | Passive channels. Nobody *calls* the lapsed client with a specific offer and takes the yes. We integrate with all of them rather than replacing any — the Switzerland position. |
| AI receptionists (inbound) | Newo.ai, Beside, Slang.ai, Goodcall, Smith.ai | Answer missed inbound calls | Different job. Inbound answering saves leads; outbound win-back *creates* revenue from a dormant asset, with per-call attribution. Outbound is also harder (consent, DNC, timing law) — which is why fewer do it, which is why it's defensible. |
| Win-back status quo | Email/SMS drips, postcard agencies, "we'll get to it" | Low-cost, low-conversion | A 90-second conversation with two concrete times beats an ignored email. The Friday arithmetic email makes the comparison unignorable. |
| Voice infrastructure | Vapi, Retell, Bland, Synthflow | Sell the pipes | Suppliers, not competitors — but they make "an AI that calls" table stakes. Our defense is never the calling; it's consent infrastructure + offer intelligence + integrations + vertical trust. |

**The Genius AI question, answered straight:** a $1.15B incumbent pivoting to "AI operations" will eventually ship an outbound agent. Three honest defenses: (1) **speed and focus** — win-back is our whole company, their feature #40; (2) **cross-platform neutrality** — we work with the ~85% of the market *not* on their calendar, including their competitors, who will not feed data to Genius AI; (3) **the outbound compliance stack** (consent gating, global DNC, state-by-state calling law) is unglamorous work an incumbent's roadmap defers — and it's already our core. And if the wedge works, being acquired by exactly such an incumbent is a respectable outcome, which investors know.

---

## 7. The data strategy done right (keeping the founder's instinct, losing the liability)

Three layers, with a bright legal line between them:

1. **Tenant layer — sacred.** Each business's client list, recordings, transcripts. Never sold, never shared, never dialed for another business, deleted on request. This is already promised on the landing page; it stays promised forever. Architecturally isolated per tenant, not just policy-isolated.
2. **Learning layer — the moat.** Aggregated, de-identified campaign outcomes: answer rates by daypart and vertical, offer-type conversion by lapse age and ticket size, script variants, voicemail response rates. This is what compounds. **Action item: the Terms of Service must be updated to grant Startup25 explicit rights to use de-identified, aggregated data for product improvement and benchmarks — reviewed by counsel — before pilot #1.** Getting this into the first contract costs nothing; retrofitting it across a customer base later is painful.
3. **Intelligence layer — future revenue and marketing.** "State of Win-Back" benchmark reports per vertical (also the best content marketing this company could produce), and eventually **Malone Brain**: per-business recommendations — who to contact, when, with which offer, on which channel — computed from that business's own data plus network-level patterns. This is the founder's "tailored selling" vision, delivered per-tenant and consent-clean.

**Pitch line:** *"We are the anti-data-broker. Businesses keep their client data; the network keeps the lessons. We monetize intelligence, not identities."*

**Compliance roadmap (this is a feature list, not a tax):**
- Consent standard: design to **prior express written consent** nationally, even though *Bradford* relaxed it in TX/LA/MS ([Henson Legal](https://www.henson-legal.com/ai-voice-compliance)) — one standard, the strict one, everywhere.
- **Consent-capture toolkit**: a QR/checkout widget and one-tap re-permission flow salons run at the front desk to (re)permission their lists. This solves our biggest funnel leak — rows dropped at scrub — *and* deepens the moat *and* gives partners (booking platforms) a reason to integrate.
- Call-recording two-party-consent states handled explicitly; STIR/SHAKEN attestation and branded caller ID so Malone doesn't show up as "Scam Likely"; written DNC/consent audit trail per dial (mostly already designed).
- Retain a TCPA attorney on advisory equity now; SOC 2 after the seed round.

---

## 8. Product roadmap — wedge to platform

| Phase | When | What ships | Why it's the next brick |
|---|---|---|---|
| **1. Win-back** (now) | M0–M6 | Exactly what the landing page promises, hardened by 10 pilots. Plus: the **"Malone calls YOU" self-serve demo** on the site, and the consent-capture toolkit. | Cleanest ROI story in SMB software; every pilot generates the case studies the raise needs. |
| **2. Revenue desk** | M6–M12 | No-show rescue (a cancellation triggers Malone to fill the slot from the lapsed/waitlist queue within minutes), appointment confirmations, waitlist fill, inbound missed-call pickup. | Same infrastructure, daily (not monthly) usage → habit → retention. Converts Malone from a campaign into a utility. |
| **3. Verticals** | M9–M18 | Med spa deepening (treatment-aware recall is already on the pricing page), then dental, veterinary, auto service — and **jewelry retail via the unfair advantage**: Roomy's as design partner #1 (disclosed as founder-affiliated), Carat Capital as the trade-media channel to reach every independent jeweler. Anniversary recall + repair/inspection callbacks at a $704 average ticket is Malone's best arithmetic yet. | Each vertical reuses 90% of the stack and adds a benchmark corpus competitors don't have. |
| **4. Malone Brain** | M18+ | Per-tenant mini-CDP (booking + POS + call outcomes unified) driving recommendations across channels: call, SMS, email — whoever should be contacted, whenever, with whatever offer. | This is the full "data-driven tailored marketing" end-state — reached with earned data and standing consent, not asserted on day one. |

---

## 9. Business model & unit economics

**Pricing (keep, with two additions):** $299 pilot · $399 Salon · $999 Med Spa · $2,499 Multi-Location — already sane. Add:
1. **A performance-flavored on-ramp** for skeptics: e.g., pilot fee credited back if Malone books less than 3× the fee in visits ("If the arithmetic doesn't work, the pilot's on us"). SMBs distrust software promises; they trust dares.
2. **Annual prepay at 2 months off** once trust exists — SMB churn insurance.

**Illustrative unit economics (assumptions labeled, per the house style):**

| Line | Estimate | Basis |
|---|---|---|
| COGS per 90-sec completed call | ~$0.10–0.25 | Telephony ~$0.014/min + STT/TTS/LLM; assume platform-priced infra at the high end |
| COGS, Salon plan month (1,500 dials, ~35% answer) | ~$60–130 | Dials that hit voicemail cost less than conversations |
| Gross margin on $399 | **~70–85%** | Software-grade; improves with self-hosted stack |
| Target CAC (blended, founder-led + partner channel) | <$600 | ≈1.5 months of Salon revenue |
| Payback | <2 months | The number pre-seed investors will anchor on |
| LTV @ 3%/mo churn (~28-mo avg life) | ~$9K Salon · ~$22K Med Spa | Churn assumption is the whole ballgame — see §15 |

**The customer's arithmetic is the sales deck:** the landing page's own worked example — 1,200 exported names → 740 survive scrub → 260 conversations → 31 bookings → 25 in the chair → **$3,000–3,720 recovered against a $399 month** — needs to stop being illustrative and start being three real customers' Friday reports. That is the entire content of the traction slide.

---

## 10. Go-to-market

**Phase 0 — ten design partners (weeks 1–6).** Nothing else matters until this is done.
- Recruit: NYC salons within walking distance of NYU (founder walk-ins carrying the one-row demo), the med spa tier via booking-consultant intros, Roomy's for jewelry, salon-owner Facebook groups and r/Hairstylist, and the Carat Capital list for jewelers.
- Offer: five founding-member pilots free (in exchange for case-study rights + a named testimonial + a reference call), five at the $299 pilot price to prove willingness to pay. Both cohorts must sign the updated ToS (aggregated-learning rights, §7).
- **The demo is the whole sales motion:** "Type your number. Malone calls you in 60 seconds with your own salon's name and offer." Every account already starts with the one-row list per the FAQ — move that moment to the top of the funnel, self-serve, on the site. It converts skeptics in ninety seconds and costs cents.

**Repeatable channels (in order of expected efficiency):**
1. **Booking-platform integrations & marketplaces** (Vagaro, Boulevard, Mangomint, Square Appointments): one-click list sync kills the CSV friction *and* is distribution. Start integration conversations at 25 customers, not before.
2. **Trade partners:** salon business coaches, med spa MSO operators, POS resellers — people paid to grow their clients' revenue, who can resell or refer Malone with a rev-share.
3. **Content that only this team can make:** the Carat Capital machine (editions, carousels, podcast) proves the team can run a daily content operation. Point a fraction of that muscle at "the win-back ledger" — public benchmark data from the learning layer, weekly. Own the category's arithmetic the way Carat Capital owns the jewelry tape.
4. **Events:** beauty & med spa trade shows with a live "Malone calls your phone at the booth" station.

**Sales motion:** self-serve pilot start → concierge offer-writing (high-touch by design, productized later into offer templates from the learning layer) → Friday report → monthly plan conversion → multi-location expansion.

---

## 11. Financial path (milestones, not hockey sticks)

| Period | Customers (paying) | MRR | Proof produced | Team |
|---|---|---|---|---|
| M0–M2 | 10 pilots (5 paid) | ~$1.5K one-time | 3 written case studies with real Friday reports; pilot→paid conversion rate | Founders only |
| M3–M6 | 30 | ~$13–16K | Churn & answer-rate baselines; consent toolkit live; ToS v2 signed by all | Founders (≥1 full-time) |
| M7–M12 | 100 | ~$45–60K | 1 booking-platform integration; med spa cohort ≥20; **pre-seed closed** | +1 GTM, +1 eng |
| M13–M24 | 300–400 | ~$150–220K ($1.8–2.6M ARR run-rate) | No-show rescue shipped; jewelry/dental beta; **seed raise window** | ~6–8 people |

Burn discipline: pilots cost almost nothing to run (the software exists; COGS is cents per call). Pre-pre-seed burn should be near zero; post-pre-seed, $25–40K/mo covering 2–3 modest founder salaries, infra, and legal.

---

## 12. The raise

**Sequence, not event:**

1. **Now → pilot proof (0–3 months): raise nothing.** Use NYU's free machinery instead — Entrepreneurial Institute / Leslie eLab coaching, Entrepreneurs Challenge, Innovation Venture Fund track — plus, if timing fits, a YC application: "students, live vertical AI agent, paying customers, 80% margins" is a canonical YC profile, and the category is being funded there monthly.
2. **Pre-seed ($600K–$1M) once the deck's traction slide is real:** 10–25 paying, three case studies, >30% pilot→paid conversion, one recognizable logo (a known local chain counts). Comparables say this is achievable: Linda AI raised $3.1M and Voicebit $2.7M at pre-seed as vertical phone agents this year ([Synaptic](https://synaptic.com/resources/tip-offs/ai-voice-agent-startups-and-founders)). Target investors: student-founder and pre-seed funds (Contrary, Neo, Pear, Afore, Hustle Fund, Antler NYC), plus **operator angels from the industry** — salon chain owners and med spa MSO executives whose checks come with pilot pipelines attached.
3. **Seed ($2.5–4M) at ~$50K+ MRR** with retention data and an integration live — priced by the momentum, not negotiated from weakness.

**Use of pre-seed funds:** ~60% GTM experiments + making ≥2 founders full-time · ~25% product (integrations, consent toolkit, no-show rescue) · ~15% legal/compliance (TCPA counsel, ToS/DPA suite, recording-consent matrix).

**What kills the raise (avoid saying or being):** "We're a marketing agency." "We collect and sell client data." "Everyone is part-time." "The cap table / entity naming is complicated." Clean up Easecase→Startup25 (name, equity splits, IP assignment from all contributors) **before** the first partner meeting.

---

## 13. The pitch itself (12 slides + the moment)

1. **Cold open** — the landing page already wrote it: *"Your dead client list is buried money."* 1,200 names, $120 ticket, zero calls made.
2. **Problem** — 70% of first-timers never return; nobody calls them; email is ignored. Sourced numbers from §2.
3. **Product / THE DEMO** — do not describe Malone. **Have Malone call the lead partner's phone, live, in the meeting, with the fund's name in the script.** The consent architecture (one attempt, instant opt-out, discloses AI) narrates itself on the call. This is the highest-variance asset the company owns; rehearse it to death.
4. **Why now** — §5's five forces, with the Genius AI valuation as the flag.
5. **Traction** — three real Friday reports; recovered-revenue vs. plan-price bar chart.
6. **Market** — §4's bottom-up table; "$120M SAM at 2% of one vertical, before dental, vet, auto, jewelry."
7. **Business model** — plans, ~80% GM, <2-month payback.
8. **Moat** — compliance-in-code + the offer-intelligence flywheel ("every call makes every next call smarter") + Switzerland integrations.
9. **Competition** — the 2×2: passive↔active × horizontal↔vertical; the honest Genius AI answer from §6.
10. **Roadmap** — win-back → revenue desk → verticals → Malone Brain.
11. **Team** — builders who shipped a compliant voice agent as students; advisory board: TCPA counsel + a salon-chain operator + a med spa MSO exec (recruit these *now*; they close credibility gaps a student team can't close alone).
12. **Ask** — $750K pre-seed → the M12 milestones in §11, named and dated.

---

## 14. What to add and improve — ranked

1. **Run the ten pilots.** Everything else is decoration until real Friday reports exist. Include Roomy's as jewelry design partner #1, disclosed as founder-affiliated.
2. **Ship the self-serve "Malone calls YOU" demo** on the landing page. It is the funnel, the pitch-meeting moment, and the trade-show booth in one feature.
3. **Update the ToS before pilot #1** to secure de-identified aggregated-learning rights (with counsel). The data moat legally begins at the first signed pilot.
4. **Build the consent-capture toolkit** — fixes the scrub-loss funnel leak, hardens compliance, and creates the integration hook.
5. **Add the ROI dare** ("books less than 3× the pilot fee → next campaign free") to collapse SMB skepticism.
6. **Fast-follow with no-show rescue** — daily-pain product on the same infrastructure; converts Malone from campaign to utility and guards retention.
7. **Fix the brand architecture:** Startup25 = company, Malone = the agent customers meet. Retire "Easecase" publicly.
8. **Instrument the flywheel from call #1** — outcome schema (offer type, lapse age, daypart, script variant, result) designed before the pilots, not discovered after.
9. **Recruit the three advisors** (TCPA attorney, salon operator, med spa operator) on small equity now.
10. **Point the Carat Capital content machine at the category** one day a week — public win-back benchmarks until Startup25 owns the arithmetic of this market the way Carat Capital owns the jewelry tape.

---

## 15. Risks, stated plainly (and the answers)

| Risk | Reality check | Mitigation |
|---|---|---|
| **SMB churn** | The #1 killer of SMB SaaS; 3%/mo assumed, could be worse | The Friday report ritual (value made visible weekly), no-show rescue (daily utility), annual prepay, multi-location expansion revenue |
| **Consent reality** | Many salons' "consent column" won't meet the written-consent standard; scrub will gut list sizes | Consent-capture toolkit as step 0 of onboarding; email/SMS re-permission pass before dialing; sell it as list *rehabilitation*, a product in itself |
| **Answer rates decline** | Unknown numbers get screened | Branded caller ID + STIR/SHAKEN attestation, local presence numbers, published callback number (already on the page), disciplined voicemail play |
| **Voice AI commoditization** | "An AI that calls" is a weekend project on Vapi | The moat was never the call: consent infrastructure, outcome corpus, integrations, vertical trust |
| **Incumbent attack (Genius AI, Boulevard)** | Real, on an 18–24 month fuse | Speed, cross-platform neutrality, outbound-compliance depth; acquisition by an incumbent is an acceptable secondary outcome |
| **Regulatory shift** | FCC's AI-disclosure rule is still a proposal ([status mid-2026](https://www.henson-legal.com/ai-voice-compliance)); states keep adding mini-TCPAs | Malone already discloses AI voluntarily and fails closed; track state laws quarterly with counsel; compliance is marketed, not hidden |
| **Team focus** | Founder also runs Carat Capital + a jewelry store; VCs will probe | Decide and say it: Startup25 is the company; Carat Capital is a channel asset; ≥2 founders full-time at pre-seed close |
| **Raising too early** | A no from a good fund is expensive to reverse | Don't pitch until the traction slide is real (§12) |

---

## 16. The next 90 days

| Weeks | Do |
|---|---|
| 1–2 | ToS v2 with counsel (learning-layer rights, consent standard, recording-consent matrix) · outcome-data schema · entity/naming cleanup begins · advisor outreach list |
| 2–4 | "Malone calls YOU" demo live on the site · pilot recruiting sprint (walk-ins, groups, Roomy's, Carat Capital list) — target 10 signed |
| 4–8 | Run pilots · weekly Friday reports · fix everything the calls surface · first "win-back ledger" content post |
| 8–10 | Convert pilots to monthly plans (target ≥3 of 10 first pass) · write the three case studies with real numbers · consent toolkit v1 |
| 10–13 | NYU eLab / Innovation Venture Fund engagement · YC application if window open · assemble the 12-slide deck with real traction · begin operator-angel conversations |

---

## 17. Open questions for the founding team

Answers to these will sharpen the next revision:

1. **Build status:** Has Malone completed real calls end-to-end (which telephony/voice stack — Twilio + Vapi/Retell, or self-built), or is the landing page currently ahead of the software?
2. **Team & cap table:** Who are the founders, what does the Easecase cap table look like, and who can commit full-time at a pre-seed close?
3. **Runway & appetite:** Current cash runway, target raise size/timing, and is an accelerator (YC / Antler / NYU summer program) on the table?
4. **Lead vertical:** Committed to salons first, or open to leading with med spas (11.5K professionalized, high-ticket buyers) — or jewelry, where distribution is already owned?
5. **Carat Capital's role:** Separate company, channel asset of Startup25, or same entity? Investors will ask; the answer should be one sentence.
6. **The data ambition:** Did "gathering a lot of data" mean cross-business monetization (the version §2/§7 argues against), or does the outcome-intelligence flywheel capture the intent?
7. **Geography:** US-first is implied by the TCPA-shaped design — confirmed?
8. **Naming:** Is "Startup25" intended as the permanent public brand, or a working title the team would trade for something better before the raise?

---

## Appendix — sources

- Salon retention: [Phorest — client retention](https://www.phorest.com/us/blog/fully-booked-salon-client-retention/) · [Callpad — retention benchmarks](https://www.callpad.ai/post/salon-client-retention-rate-benchmarks-improve) · [Jeri Commerce — spa/salon retention statistics](https://blog.jericommerce.com/resources/spas-salons-medspas-retention-statistics)
- Market counts: [IBISWorld — hair & nail salons](https://www.ibisworld.com/united-states/number-of-businesses/hair-nail-salons/1718/) · [IBISWorld — barbershops](https://www.ibisworld.com/united-states/number-of-businesses/barber-shops/5806/) · [Pinch — AmSpa med spa expansion](https://www.bookpinch.com/blog/expansion-us-medical-spa-industry) · [LeadResponse — med spa statistics](https://leadresponse.co/blog/med-spa-industry-statistics)
- Funding climate: [AgentVoice — voice AI funding market map](https://agentvoice.com/blog/ai-voice-agents-funding-market-map/) · [Tech Funding News — Newo.ai $25M](https://techfundingnews.com/newo-ai-raises-25m-series-a-voice-infrastructure/) · [Fortune — Beside $32M](https://www.fortune.com/2025/11/11/beside-ai-voice-startup-raises-32-million-ai-receptionist-for-small-business/) · [Synaptic — voice agent startups tip-offs](https://synaptic.com/resources/tip-offs/ai-voice-agent-startups-and-founders) · [Fortune — GlossGenius → Genius AI, $44M at $1.15B](https://fortune.com/2026/07/21/glossgenius-rebrand-genius-ai-small-businesses-beauty-unicorn-series-d/)
- Regulatory: [FCC — AI-generated voices under TCPA](https://www.fcc.gov/document/fcc-makes-ai-generated-voices-robocalls-illegal) · [FCC — TCPA applies to AI voices](https://www.fcc.gov/document/fcc-confirms-tcpa-applies-ai-technologies-generate-human-voices) · [Henson Legal — AI voice compliance 2026](https://www.henson-legal.com/ai-voice-compliance) · [Retell — TCPA playbook 2026](https://www.retellai.com/blog/tcpa-compliance-playbook-voice-ai-outbound)

*Figures from third-party sources are as reported by those sources; internal projections are assumptions and labeled as such.*
