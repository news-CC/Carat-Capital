#!/usr/bin/env node
/**
 * Place one real end-to-end test call to your own phone.
 *
 *   node --env-file=.env.local scripts/test-call.mjs +15105550142
 *   node --env-file=.env.local scripts/test-call.mjs +15105550142 --name Vijay
 *
 * Creates (or reuses) a test client, adds YOUR number as a consented contact under a fresh
 * campaign, then triggers the real dial route — the same code path a paying salon's list goes
 * through. Nothing is stubbed.
 *
 * WHY A FRESH CAMPAIGN EVERY RUN: one dial attempt per contact, ever, is a compliance rule
 * enforced by `attempts = 0` in claim_contacts_for_dialing. A contact that has been tried is
 * finished — permanently. Re-running therefore inserts a NEW contact row under a new campaign
 * name rather than resetting the old one, because resetting it would quietly break the guarantee
 * the whole product rests on. The failed rows stay as the audit trail.
 */
import { createClient } from '@supabase/supabase-js';

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
const cronSecret = process.env.CRON_SECRET;
const appUrl = (process.env.NEXT_PUBLIC_APP_URL || 'https://www.startup25.com').replace(/\/+$/, '');
if (!url || !key || !cronSecret) {
  console.error('Missing env. Run with: node --env-file=.env.local scripts/test-call.mjs +1XXXXXXXXXX');
  process.exit(1);
}

const raw = process.argv[2];
if (!raw) {
  console.error('Usage: node --env-file=.env.local scripts/test-call.mjs +1XXXXXXXXXX [--name Vijay]');
  process.exit(1);
}
const nameIdx = process.argv.indexOf('--name');
const firstName = nameIdx !== -1 ? process.argv[nameIdx + 1] : 'Vijay';

// Same normalization the scrub and dialer use: a '+' prefix means a written country code, so a
// 10-digit '+..' value is ambiguous and rejected rather than guessed into a NANP number.
const digits = String(raw).replace(/\D/g, '');
const hadPlus = String(raw).trim().startsWith('+');
const ten = digits.length === 11 && digits.startsWith('1') ? digits.slice(1) : digits;
if (!(digits.length === 10 && !hadPlus) && !(digits.length === 11 && digits.startsWith('1'))) {
  console.error(`"${raw}" is not a US/Canada number this script can place a test call to.`);
  process.exit(1);
}
if (!/^[2-9]\d{2}[2-9]\d{2}\d{4}$/.test(ten)) {
  console.error(`"${raw}" is not a valid NANP number.`);
  process.exit(1);
}
const phone = `+1${ten}`;
if (/^\+1\d{3}55501\d{2}$/.test(phone)) {
  console.error(`${phone} is in the 555-01XX fiction range — the dialer skips those by design.`);
  process.exit(1);
}

const db = createClient(url, key, { auth: { persistSession: false } });

const TEST_CLIENT = 'Salon Malone — test line';
let { data: client } = await db.from('clients').select('*').eq('name', TEST_CLIENT).maybeSingle();

if (!client) {
  const { data, error } = await db
    .from('clients')
    .insert({
      name: TEST_CLIENT,
      contact_name: firstName,
      contact_email: process.env.EMAIL_FROM?.match(/[^<>\s]+@[^<>\s]+/)?.[0] ?? 'ops@startup25.com',
      contact_phone: phone,
      booking_phone: process.env.SALON_MALONE_PHONE || '+18634966101',
      offer_text: 'twenty percent off your next cut and colour, any day this week',
      timezone: 'America/Los_Angeles',
      vertical: 'salon',
      avg_ticket_cents: 12000,
      stripe_status: 'trialing',
      active: true,
    })
    .select()
    .single();
  if (error) { console.error('could not create the test client:', error.message); process.exit(1); }
  client = data;
  console.log(`+ created test client ${client.id}`);
} else {
  console.log(`= reusing test client ${client.id}`);
  if (!client.active || !['active', 'trialing'].includes(client.stripe_status)) {
    await db.from('clients').update({ active: true, stripe_status: 'trialing' }).eq('id', client.id);
    console.log('  re-activated it so the claim query can see it');
  }
}

// Is it inside the calling window in THIS client's timezone? The dialer will refuse otherwise —
// correctly — so say so up front rather than letting it look like a failure.
const nowLocal = new Intl.DateTimeFormat('en-GB', {
  timeZone: client.timezone, hour12: false, hour: '2-digit', minute: '2-digit',
}).format(new Date());
const start = process.env.CALL_WINDOW_START || '09:00';
const end = process.env.CALL_WINDOW_END || '19:00';
const inside = nowLocal >= start && nowLocal <= end;
console.log(`  local time in ${client.timezone}: ${nowLocal}  window ${start}-${end}  ${inside ? 'OPEN' : 'CLOSED'}`);
if (!inside) {
  console.error(`\nThe calling window is closed. The dialer will claim nothing — that is the gate working.`);
  console.error(`Either wait, or temporarily widen CALL_WINDOW_END for the test.`);
  process.exit(2);
}

const campaign = `test-${new Date().toISOString().replace(/[-:T.]/g, '').slice(0, 14)}`;
const { data: contact, error: cErr } = await db
  .from('contacts')
  .insert({
    client_id: client.id,
    campaign,
    name: firstName,
    first_name: firstName,
    phone,
    phone_raw: raw,
    consent: true,          // you are consenting to be called by your own test
    status: 'pending',
    attempts: 0,
  })
  .select()
  .single();
if (cErr) { console.error('could not create the contact:', cErr.message); process.exit(1); }
console.log(`+ contact ${contact.id} — ${phone}, campaign ${campaign}, consent true`);

console.log('\ntriggering the dialer…');
const res = await fetch(`${appUrl}/api/cron/dial`, {
  headers: { Authorization: `Bearer ${cronSecret}` },
});
const body = await res.json().catch(() => ({}));
console.log(`  HTTP ${res.status} ${JSON.stringify(body)}`);

await new Promise((r) => setTimeout(r, 3000));
const { data: calls } = await db
  .from('calls')
  .select('outcome, ended_reason, vapi_call_id, created_at')
  .eq('contact_id', contact.id)
  .order('created_at', { ascending: false });

if (!calls?.length) {
  console.log('\nNo calls row yet. If claimed=0 above, a gate stopped it — check consent/window/suppression.');
  process.exit(0);
}
for (const c of calls) {
  console.log(`\n  outcome: ${c.outcome}`);
  if (c.vapi_call_id) console.log(`  vapi call: ${c.vapi_call_id}`);
  if (c.ended_reason) console.log(`  reason: ${c.ended_reason}`);
}
if (calls[0].outcome === 'dialing') {
  console.log('\nYour phone should ring in a few seconds. Answer it — Salon Malone is on the line.');
  console.log(`Watch the result land: ${appUrl}/admin/calls`);
}
