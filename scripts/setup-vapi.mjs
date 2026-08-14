#!/usr/bin/env node
/**
 * Creates or updates the "Salon Malone" Vapi assistant, and provisions a free Vapi phone number
 * if the account has none yet.
 *
 * Idempotent. The assistant is looked up by name before anything is created, so re-running updates
 * in place rather than filling the dashboard with copies of Malone.
 *
 * ─────────────────────────────────────────────────────────────────────────────────────────────────
 * src/lib/malone.ts IS THE SOURCE OF TRUTH for the prompt, the voice config and the analysis plan.
 * The payload below is a hand-kept mirror of maloneAssistantPayload() from that file, duplicated
 * here only because this is a plain .mjs script and cannot import TypeScript.
 * If you edit src/lib/malone.ts, re-sync the block below and re-run `npm run setup:vapi`.
 * The script reports when the deployed prompt no longer matches this file, so drift is at least loud.
 * ─────────────────────────────────────────────────────────────────────────────────────────────────
 *
 * Usage:
 *   npm run setup:vapi                          # node --env-file=.env.local scripts/setup-vapi.mjs
 *   npm run setup:vapi -- --dry-run             # report only, write nothing
 *   npm run setup:vapi -- --url=https://x.com   # override the webhook base URL
 */
import { randomBytes } from 'node:crypto';

const DRY_RUN = process.argv.includes('--dry-run');
const urlFlag = process.argv.find((a) => a.startsWith('--url='))?.slice('--url='.length);

const API = 'https://api.vapi.ai';
const ASSISTANT_NAME = 'Salon Malone';
const NUMBER_NAME = 'Salon Malone outbound';

const apiKey = process.env.VAPI_API_KEY;
if (!apiKey) {
  console.error('VAPI_API_KEY is not set.');
  console.error('Run through npm so the env file is loaded:  npm run setup:vapi');
  process.exit(1);
}

const appUrl = (urlFlag ?? process.env.NEXT_PUBLIC_APP_URL ?? '').replace(/\/+$/, '');
if (!appUrl) {
  console.error('No app URL. Set NEXT_PUBLIC_APP_URL in .env.local, or pass --url=https://your-domain.');
  process.exit(1);
}
const serverUrl = `${appUrl}/api/vapi/webhook`;

// A webhook secret that only exists in this process is useless — if we mint one, the operator must
// save it, so that is called out loudly at the end.
const existingSecret = process.env.VAPI_WEBHOOK_SECRET;
const serverSecret = existingSecret || randomBytes(32).toString('hex');
const secretWasGenerated = !existingSecret;

// ── mirror of maloneAssistantPayload() — see the sync note above ──────────────
const MALONE_SYSTEM_PROMPT = `You are Salon Malone, {{salon_name}}'s virtual concierge, calling a client who hasn't been in for a while. Smooth, warm, quick. Pizazz, not pressure. The coolest front-desk person alive.

DISCLOSURE (mandatory): say you are {{salon_name}}'s virtual concierge in your opening line. If asked whether you're a real person, a bot, or a recording, answer at once: "I'm a virtual assistant for {{salon_name}} — a real human takes care of you in the chair." Never claim to be human. Never dodge it.

ONE GOAL: book a specific time using this offer — {{offer_text}}.
Offer exactly two concrete times: "Thursday at two, or Saturday morning at ten — which is easier?" If neither works, ask which day does. When they pick, repeat the day and time back in full, then close.

FLOW
- Short lines. One idea per turn. Never pitch twice. Never argue. Never oversell.
- One beat of small talk, max. Only the visit and the offer.
- You can't see the calendar or take payment. You note the time down; the salon confirms.
- Off-topic, prices, or anything medical: "Best person for that is the front desk — {{booking_phone}}." Then back to the time, or close.

EXITS
- Warm no: "All love — the chair's here when you're ready." End the call.
- Stop calling / take me off the list / do not call: "Done — you're off the list. Be good." End the call at once. Never pitch again.
- Wrong person, wrong number, or an upset caller: apologise once, end the call.

PACE: 90 seconds is the target, 3 minutes the hard ceiling. Near it, close or exit.`;

const MALONE_FIRST_MESSAGE =
  "Hey {{first_name}} — Salon Malone here, {{salon_name}}'s virtual concierge. Ninety seconds, I promise. We miss you.";

const MALONE_VOICEMAIL_MESSAGE =
  "Hey {{first_name}}, Salon Malone here — {{salon_name}}'s virtual concierge. We miss you, and we saved you something: {{offer_text}}. Call {{booking_phone}} and we'll get you back in the chair. Take care.";

const STRUCTURED_DATA_INSTRUCTIONS = `You are reading a transcript of an outbound win-back call made by a salon's virtual concierge. Extract only what was actually said.
- outcome: "booked" only if the client agreed to a specific day/time. "declined" if they said no or not now. "opted_out" if they asked not to be called again. "voicemail" if only a machine was reached. "no_answer" if nobody spoke. Otherwise "answered".
- slot_text: the agreed day and time in the client's own words, e.g. "Thursday at 2pm". Empty string if nothing was agreed.
- opt_out: true only if the client asked to be removed, to stop calls, or said do not call.
- notes: one short sentence a salon owner would care about. No speculation.`;

const MALONE_ANALYSIS_PLAN = {
  minMessagesThreshold: 1,
  summaryPlan: {
    enabled: true,
    timeoutSeconds: 20,
    messages: [
      {
        role: 'system',
        content:
          'Summarise this win-back call for the salon owner in two sentences: what the client said, and what happens next. Plain language, no preamble.',
      },
      { role: 'user', content: 'Transcript:\n\n{{transcript}}' },
    ],
  },
  structuredDataPlan: {
    enabled: true,
    timeoutSeconds: 20,
    messages: [
      { role: 'system', content: STRUCTURED_DATA_INSTRUCTIONS },
      { role: 'user', content: 'Transcript:\n\n{{transcript}}' },
    ],
    schema: {
      type: 'object',
      properties: {
        outcome: {
          type: 'string',
          enum: ['booked', 'declined', 'opted_out', 'voicemail', 'no_answer', 'answered'],
          description: 'How the call resolved.',
        },
        slot_text: { type: 'string', description: "Agreed day and time in the client's words, or an empty string." },
        opt_out: { type: 'boolean', description: 'True only if the client asked never to be called again.' },
        notes: { type: 'string', description: 'One short sentence for the salon owner.' },
      },
      required: ['outcome', 'opt_out'],
    },
  },
  successEvaluationPlan: { enabled: false },
};

function maloneAssistantPayload() {
  return {
    name: ASSISTANT_NAME,
    firstMessage: MALONE_FIRST_MESSAGE,
    firstMessageMode: 'assistant-speaks-first',
    model: {
      provider: 'openai',
      model: 'gpt-4o-mini',
      temperature: 0.4,
      maxTokens: 120,
      messages: [{ role: 'system', content: MALONE_SYSTEM_PROMPT }],
    },
    transcriber: { provider: 'deepgram', model: 'nova-2-phonecall', language: 'en', smartFormat: true },
    voice: {
      provider: '11labs',
      voiceId: 'rachel',
      model: 'eleven_turbo_v2_5',
      optimizeStreamingLatency: 3,
      stability: 0.5,
      similarityBoost: 0.75,
      useSpeakerBoost: true,
    },
    backchannelingEnabled: true,
    fillerInjectionEnabled: true,
    backgroundDenoisingEnabled: true,
    startSpeakingPlan: { waitSeconds: 0.4, smartEndpointingEnabled: true },
    stopSpeakingPlan: { numWords: 2, voiceSeconds: 0.2, backoffSeconds: 1 },
    endCallFunctionEnabled: true,
    endCallMessage: "All love — the chair's here when you're ready. Take care.",
    endCallPhrases: ['goodbye', 'good bye', 'be good', 'see you then'],
    silenceTimeoutSeconds: 20,
    maxDurationSeconds: 180,
    voicemailDetection: { provider: 'vapi' },
    voicemailMessage: MALONE_VOICEMAIL_MESSAGE,
    serverUrl,
    serverUrlSecret: serverSecret,
    serverMessages: ['status-update', 'end-of-call-report'],
    artifactPlan: { recordingEnabled: true, transcriptPlan: { enabled: true } },
    analysisPlan: MALONE_ANALYSIS_PLAN,
    metadata: { app: 'salon-malone' },
  };
}

// ── API helper ────────────────────────────────────────────────────────────────
async function vapi(path, init = {}) {
  const res = await fetch(`${API}${path}`, {
    ...init,
    headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json', ...(init.headers ?? {}) },
    signal: AbortSignal.timeout(30_000),
  });
  const text = await res.text();
  let body = null;
  try {
    body = text ? JSON.parse(text) : null;
  } catch {
    body = text;
  }
  if (!res.ok) {
    const raw = body && typeof body === 'object' ? (body.message ?? body.error ?? body) : body;
    const message = Array.isArray(raw) ? raw.join('; ') : typeof raw === 'string' ? raw : JSON.stringify(raw);
    const error = new Error(`${res.status} ${message}`);
    error.status = res.status;
    error.body = body;
    throw error;
  }
  return body;
}

const asList = (body) => (Array.isArray(body) ? body : (body?.results ?? []));

/** Vapi refuses free numbers once the plan's allowance is used up. The wording varies; the fix does not. */
function isFreeNumberExhausted(e) {
  const text = JSON.stringify(e.body ?? e.message ?? '').toLowerCase();
  return (
    [400, 402, 403].includes(e.status) &&
    /free|limit|quota|allowance|upgrade|subscription|payment|card|billing/.test(text)
  );
}

// ── steps ─────────────────────────────────────────────────────────────────────
async function upsertAssistant() {
  const existing = asList(await vapi('/assistant?limit=100')).find((a) => a.name === ASSISTANT_NAME);
  const payload = maloneAssistantPayload();

  if (!existing) {
    if (DRY_RUN) {
      console.log(`assistant   would CREATE "${ASSISTANT_NAME}"`);
      return null;
    }
    const created = await vapi('/assistant', { method: 'POST', body: JSON.stringify(payload) });
    console.log(`assistant   CREATED ${created.id}`);
    return created.id;
  }

  const deployedPrompt = existing.model?.messages?.[0]?.content ?? '';
  const promptInSync = deployedPrompt === MALONE_SYSTEM_PROMPT;
  const webhookInSync = existing.serverUrl === serverUrl;
  console.log(
    `assistant   exists ${existing.id} · prompt ${promptInSync ? 'in sync' : 'DIFFERS from src/lib/malone.ts'} · webhook ${webhookInSync ? 'in sync' : `-> ${serverUrl}`}`,
  );

  if (DRY_RUN) {
    console.log('            would PATCH it with the payload in this script');
    return existing.id;
  }
  await vapi(`/assistant/${existing.id}`, { method: 'PATCH', body: JSON.stringify(payload) });
  console.log(`            UPDATED ${existing.id}`);
  return existing.id;
}

async function ensurePhoneNumber() {
  const numbers = asList(await vapi('/phone-number?limit=100'));
  if (numbers.length > 0) {
    const n = numbers.find((x) => x.name === NUMBER_NAME) ?? numbers[0];
    console.log(`number      exists ${n.id} · ${n.number ?? '(pending)'} · provider ${n.provider ?? 'unknown'}`);
    return { id: n.id, number: n.number };
  }

  if (DRY_RUN) {
    console.log("number      would CREATE a free Vapi number (provider 'vapi')");
    return null;
  }

  try {
    // Deliberately created without an assistantId: v1 places outbound calls only, and Malone reads
    // the salon's own number on voicemail. Nothing is meant to answer inbound here.
    const created = await vapi('/phone-number', {
      method: 'POST',
      body: JSON.stringify({ provider: 'vapi', name: NUMBER_NAME }),
    });
    console.log(`number      CREATED ${created.id} · ${created.number ?? '(provisioning)'}`);
    return { id: created.id, number: created.number };
  } catch (e) {
    if (isFreeNumberExhausted(e)) {
      console.log('number      NOT CREATED — this Vapi plan has no free numbers left.');
      console.log('');
      console.log('            Vapi grants a limited number of free numbers per account. Options:');
      console.log('              · Dashboard → Phone Numbers → buy a Vapi number (a few dollars a month).');
      console.log('              · Import a Twilio number you already own:');
      console.log('                  POST /phone-number { provider: "twilio", number, twilioAccountSid, twilioAuthToken }');
      console.log('              · Reuse an existing number on the account — re-running this script picks it up.');
      console.log(`            Vapi said: ${e.message}`);
      console.log('');
      return null;
    }
    throw e;
  }
}

// ── main ──────────────────────────────────────────────────────────────────────
async function main() {
  console.log('');
  console.log(`SALON MALONE — Vapi setup${DRY_RUN ? '   (dry run — nothing will be written)' : ''}`);
  console.log(`webhook     ${serverUrl}`);
  console.log(`secret      ${secretWasGenerated ? 'GENERATED (save it — see below)' : 'from VAPI_WEBHOOK_SECRET'}`);
  console.log('');

  const assistantId = await upsertAssistant();
  const number = await ensurePhoneNumber();

  console.log('');
  console.log('─'.repeat(78));
  console.log('Paste into .env.local, and into Vercel → Settings → Environment Variables.');
  console.log('─'.repeat(78));
  console.log('');
  if (assistantId) console.log(`VAPI_ASSISTANT_ID=${assistantId}`);
  if (number?.id) console.log(`VAPI_PHONE_NUMBER_ID=${number.id}`);
  if (secretWasGenerated) {
    console.log(`VAPI_WEBHOOK_SECRET=${serverSecret}`);
  } else {
    // Already in your env. Echoing it again would only spread it into shell history and CI logs.
    console.log('# VAPI_WEBHOOK_SECRET is already set — unchanged, not reprinted.');
  }
  console.log('');

  if (secretWasGenerated && !DRY_RUN) {
    console.log('!! VAPI_WEBHOOK_SECRET was generated just now and the assistant was configured with it.');
    console.log('   It is not stored anywhere else. Save it before this terminal scrolls away, or every');
    console.log('   webhook delivery will be rejected with a 401 and no call will ever be recorded.');
    console.log('');
  }
  if (!number) {
    console.log('No phone number id yet. /api/cron/dial cannot place calls without VAPI_PHONE_NUMBER_ID.');
    console.log('');
  }
  if (appUrl.includes('localhost') || appUrl.includes('127.0.0.1')) {
    console.log('Note: the webhook URL points at localhost, which Vapi cannot reach. Re-run with');
    console.log('--url=https://<your-vercel-domain> once deployed, or tunnel it for local testing.');
    console.log('');
  }
}

main().catch((e) => {
  console.error('setup:vapi failed:', e instanceof Error ? e.message : e);
  process.exit(1);
});
