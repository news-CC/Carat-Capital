#!/usr/bin/env node
/**
 * Creates or updates the "Salon Malone" Vapi assistant, and provisions a free Vapi phone number
 * if the account has none yet.
 *
 * Idempotent. The assistant is looked up by name before anything is created, so re-running updates
 * in place rather than filling the dashboard with copies of Malone.
 *
 * ─────────────────────────────────────────────────────────────────────────────────────────────────
 * src/lib/malone.ts IS THE SOURCE OF TRUTH for the prompt, the voice config and the analysis plan,
 * and this script imports it directly rather than mirroring it. The persona used to be duplicated
 * here as literals; it drifted, which is exactly why it is imported now. Edit malone.ts, re-run
 * this script, done — there is nothing here to keep in sync.
 *
 * That import needs a Node that strips TypeScript types on the fly (>= 22.18, or >= 22.6 with
 * --experimental-strip-types). Checked below with a message that says what to do.
 * ─────────────────────────────────────────────────────────────────────────────────────────────────
 *
 * Usage:
 *   npm run setup:vapi                          # node --env-file=.env.local scripts/setup-vapi.mjs
 *   npm run setup:vapi -- --dry-run             # report only, write nothing
 *   npm run setup:vapi -- --url=https://x.com   # override the webhook base URL
 */
import { randomBytes } from 'node:crypto';
import { fileURLToPath } from 'node:url';
// Not named `path`: the vapi() helper below takes a `path` argument.
import nodePath from 'node:path';

const DRY_RUN = process.argv.includes('--dry-run');
const urlFlag = process.argv.find((a) => a.startsWith('--url='))?.slice('--url='.length);

const API = 'https://api.vapi.ai';
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

// ── the persona, imported from the one place it is defined ───────────────────
const MALONE = await importMalone();
const { MALONE_SYSTEM_PROMPT, maloneAssistantPayload } = MALONE;

// The lookup key for the idempotent upsert. Taken from the payload so the name cannot drift either.
const ASSISTANT_NAME = maloneAssistantPayload('', '').name;

/**
 * src/lib/malone.ts is TypeScript. Node >= 22.18 strips the types on import with no flag; older
 * runtimes throw ERR_UNKNOWN_FILE_EXTENSION (or a syntax error) and get told what to do instead of
 * a stack trace.
 */
async function importMalone() {
  const here = nodePath.dirname(fileURLToPath(import.meta.url));
  const target = nodePath.join(here, '..', 'src', 'lib', 'malone.ts');
  try {
    return await import(`file://${target}`);
  } catch (e) {
    console.error('');
    console.error('Could not load src/lib/malone.ts — the assistant persona lives there.');
    console.error(`  ${e instanceof Error ? e.message : e}`);
    console.error('');
    console.error(`This script needs a Node that can strip TypeScript types. You are on ${process.version}.`);
    console.error('  · Node >= 22.18: works with no flag.');
    console.error('  · Node 22.6-22.17: node --experimental-strip-types --env-file=.env.local scripts/setup-vapi.mjs');
    console.error('  · Node 20: upgrade, or run the setup from the Vapi dashboard by hand.');
    console.error('');
    process.exit(1);
  }
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
  const payload = maloneAssistantPayload(serverUrl, serverSecret);

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
    console.log('            would PATCH it with the payload from src/lib/malone.ts');
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
