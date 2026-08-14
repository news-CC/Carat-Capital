import { NextResponse } from 'next/server';

import { sendBookingAlert } from '@/lib/email/booking-alert';
import { containsOptOutRequest } from '@/lib/opt-out';
import { supabaseAdmin } from '@/lib/supabase/admin';
import { suppressPhoneGlobally } from '@/lib/suppression';
import type { CallOutcome, ContactStatus } from '@/lib/types';
import { verifyVapiRequest } from '@/lib/vapi';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

/** Once a call has resolved, a later delivery must not walk the outcome backwards. */
const TERMINAL: ReadonlySet<string> = new Set([
  'booked',
  'declined',
  'no_answer',
  'voicemail',
  'busy',
  'failed',
  'opted_out',
]);

const received = () => NextResponse.json({ received: true });

/**
 * A write this delivery lost that a re-delivery could repair — above all the suppression row.
 * Thrown at the end of the handler so it becomes a 500, which is the only signal Vapi has to
 * send the report again.
 */
class RetriableWebhookError extends Error {
  constructor(callId: string, failures: readonly string[]) {
    super(`${callId} — ${failures.join('; ')}`);
    this.name = 'RetriableWebhookError';
  }
}

export async function POST(req: Request) {
  // Vapi sends the configured server secret as x-vapi-secret; some accounts send it as
  // x-vapi-signature instead. Either header is accepted, but BOTH are verified against
  // VAPI_WEBHOOK_SECRET — presence alone is not authorisation. This endpoint writes to the
  // suppression list and creates bookings, so an unverified caller could forge opt-outs.
  const authorized =
    verifyVapiRequest(req.headers.get('x-vapi-secret')) ||
    verifyVapiRequest(req.headers.get('x-vapi-signature'));
  if (!authorized) {
    return NextResponse.json({ received: false, error: 'unauthorized' }, { status: 401 });
  }

  // A poison payload answers 200 no matter what — it must not be retried forever. A lost write is
  // the one exception: RetriableWebhookError answers 500 so Vapi re-delivers, because dropping an
  // opt-out means dialing someone who asked us to stop. Replay is safe: both handlers are keyed on
  // vapi_call_id, the suppression upsert ignores duplicates, and the booking de-dupes on contact.
  try {
    const parsed: unknown = JSON.parse(await req.text());
    const message = asRecord(asRecord(parsed)?.message);
    if (!message) return received();

    // 'hang', 'speech-update', 'transcript' and friends are deliberately ignored.
    const type = str(message.type);
    if (type === 'status-update') await handleStatusUpdate(message);
    else if (type === 'end-of-call-report') await handleEndOfCall(message);

    return received();
  } catch (e) {
    console.error('[vapi-webhook]', e instanceof Error ? e.message : e);
    if (e instanceof RetriableWebhookError) {
      return NextResponse.json({ received: false, error: 'retry' }, { status: 500 });
    }
    return received();
  }
}

type Db = ReturnType<typeof supabaseAdmin>;
type CallRow = { id: string; contact_id: string | null; client_id: string | null; outcome: string };

async function handleStatusUpdate(message: Record<string, unknown>): Promise<void> {
  const callId = vapiCallId(message);
  if (!callId) return;
  if (str(message.status) !== 'in-progress') return; // 'ended' is only authoritative in the report

  const db = supabaseAdmin();
  const existing = await findCall(db, callId);
  if (existing && TERMINAL.has(existing.outcome)) return;

  const ids = resolveIds(message, existing);
  const { error } = await db.from('calls').upsert(
    {
      vapi_call_id: callId,
      contact_id: ids.contactId,
      client_id: ids.clientId,
      outcome: 'answered',
    },
    { onConflict: 'vapi_call_id' },
  );
  // Not worth a re-delivery: the end-of-call report rewrites this row from scratch, and
  // expire_stuck_calling frees the concurrency slot if it never arrives. Unlogged calls are still
  // bugs (ARCHITECTURE §4), so the failure is shouted about rather than swallowed.
  if (error) console.error('[vapi-webhook] status-update upsert failed', callId, error.message);
}

async function handleEndOfCall(message: Record<string, unknown>): Promise<void> {
  const callId = vapiCallId(message);
  if (!callId) return;

  const db = supabaseAdmin();
  const existing = await findCall(db, callId);
  const { contactId, clientId } = resolveIds(message, existing);

  const artifact = asRecord(message.artifact);
  const analysis = asRecord(message.analysis);
  const transcript = str(artifact?.transcript) ?? str(message.transcript) ?? '';
  const structured = readStructuredData(analysis?.structuredData);
  const summary = str(analysis?.summary) ?? str(message.summary);
  const transcriptUrl = str(artifact?.transcriptUrl);

  const optOut = detectOptOut(structured, transcript);
  const { outcome, booked } = resolveCall(str(message.endedReason), structured, optOut);

  const startedAt = isoDate(message.startedAt);
  const endedAt = isoDate(message.endedAt) ?? new Date().toISOString();

  // Failures a re-delivery could repair are collected rather than thrown on the spot: one bad
  // write must not skip the writes after it. The list becomes a single 500 at the end.
  const retriable: string[] = [];

  const [contactRes, clientRes] = await Promise.all([
    contactId
      ? db.from('contacts').select('id, phone, first_name, name').eq('id', contactId).maybeSingle()
      : null,
    clientId
      ? db
          .from('clients')
          .select('id, name, contact_email, avg_ticket_cents')
          .eq('id', clientId)
          .maybeSingle()
      : null,
  ]);
  // The contact row carries the phone the opt-out is written against, and the client row carries
  // the address the booking alert goes to. Losing either is repairable by a re-delivery.
  if (contactRes?.error) retriable.push(`contact read failed: ${contactRes.error.message}`);
  if (clientRes?.error) retriable.push(`client read failed: ${clientRes.error.message}`);
  const contact = contactRes?.data ?? null;
  const client = clientRes?.data ?? null;

  // Compliance gate: opt-out is synchronous and global, and it lands before anything else in this
  // handler. If it cannot land, the request answers 500 so Vapi re-delivers the report — a lost
  // opt-out is a person who asked to be left alone and would be dialed again by the next client's
  // list. The dialled number is the fallback key, so an opt-out survives missing metadata.
  if (optOut) {
    const phone = contact?.phone ?? str(asRecord(asRecord(message.call)?.customer)?.number);
    if (phone) {
      if (!contact?.phone) {
        // The payload number is all we have. If it is not the E.164 we stored, the row we write
        // will not match the claim query's exact-match gate, so this needs a human eye.
        console.error('[vapi-webhook] opt-out suppressed on the payload number', callId, phone);
      }
      // One implementation of "suppress this number everywhere", shared with both admin paths
      // (src/lib/suppression.ts): the durable global row, then the fan-out that pulls the number
      // out of every other client's pending queue now rather than trusting the claim query to skip
      // it later. Only a failure of the durable row comes back — a failed fan-out is logged there,
      // because the suppression row is the gate and both the claim query and the dial route
      // re-check it before every dial.
      const suppressed = await suppressPhoneGlobally(db, {
        phone,
        reason: 'opt_out',
        sourceContactId: contactId,
        tag: '[vapi-webhook]',
        context: callId,
      });
      if (suppressed.error) retriable.push(suppressed.error);
    } else {
      // An opt-out we cannot record must not answer 200: there is no number in the payload and no
      // contact row to read one from, so the only honest move is to make Vapi send it again.
      console.error('[vapi-webhook] opt-out with no phone to suppress', callId);
      retriable.push('opt-out with no phone to suppress');
    }
  }

  // Idempotent by vapi_call_id: a re-delivered report rewrites the same row.
  const upserted = await db
    .from('calls')
    .upsert(
      {
        vapi_call_id: callId,
        contact_id: contactId,
        client_id: clientId,
        outcome,
        ended_reason: str(message.endedReason),
        duration_seconds: durationSeconds(message, startedAt, endedAt),
        cost_usd: num(message.cost),
        summary,
        transcript_url: transcriptUrl,
        recording_url:
          str(artifact?.recordingUrl) ??
          str(artifact?.stereoRecordingUrl) ??
          str(message.recordingUrl),
        ended_at: endedAt,
        ...(startedAt ? { started_at: startedAt } : {}),
      },
      { onConflict: 'vapi_call_id' },
    )
    .select('id')
    .maybeSingle();
  if (upserted.error) {
    // Every attempt keeps its calls row (ARCHITECTURE §4), and the row is the only record of what
    // was said, so this one is worth a re-delivery.
    console.error('[vapi-webhook] call upsert failed', callId, upserted.error.message);
    retriable.push(`call upsert failed: ${upserted.error.message}`);
  }

  const callRowId = upserted.data?.id ?? existing?.id ?? null;

  // str() trims, so a whitespace-only slot_text is already null here and can never be booked.
  const slotText = structured.slotText;
  if (booked && slotText) {
    if (contactId && clientId) {
      if (optOut) {
        // A captured slot and an opt-out on the same call: the salon still gets the appointment
        // the client asked for, and we still never dial this number again. Loud, because a human
        // should read the transcript and decide whether the opt-out was meant as one.
        console.error('[vapi-webhook] booked call also opted out — suppressed and booked', callId);
      }
      const failure = await recordBooking(db, {
        callRowId,
        contactId,
        clientId,
        slotText,
        summary: summary ?? structured.notes,
        transcriptUrl,
        firstName: contact?.first_name ?? contact?.name ?? 'A client',
        phone: contact?.phone ?? '',
        salonName: client?.name ?? 'your salon',
        ownerEmail: client?.contact_email ?? null,
        avgTicketCents: client?.avg_ticket_cents ?? null,
      });
      if (failure) {
        console.error('[vapi-webhook]', failure, callId);
        retriable.push(failure);
      }
    } else {
      // A booking we cannot attribute is lost revenue — make it loud in the logs.
      console.error('[vapi-webhook] booked call missing contact/client metadata', callId);
    }
  }

  if (contactId) {
    const marked = await db
      .from('contacts')
      .update({ status: contactStatusFor(outcome) })
      .eq('id', contactId);
    if (marked.error) {
      console.error('[vapi-webhook] contact status update failed', callId, marked.error.message);
      retriable.push(`contact status update failed: ${marked.error.message}`);
    }
  }

  if (retriable.length > 0) throw new RetriableWebhookError(callId, retriable);
}

/**
 * Writes the booking row and fires the owner alert. Returns a description of a failure a
 * re-delivery could repair, or null when everything that could be written was written.
 *
 * De-duped on contact_id: one attempt per contact ever means one booking per contact, and unlike
 * call_id it is the same on every delivery of the report. Three layers, in order of authority:
 * the `bookings_contact_id_key` partial unique index in 0001_init.sql (Postgres settles the race),
 * the lookup below (so the common re-delivery costs no failed insert), and `droppedAsDuplicate`
 * (for a database where the index could not be created). The owner alert is claimed separately via
 * notified_at, so exactly one delivery ever emails a given booking.
 */
async function recordBooking(
  db: Db,
  a: {
    callRowId: string | null;
    contactId: string;
    clientId: string;
    slotText: string;
    summary: string | null;
    transcriptUrl: string | null;
    firstName: string;
    phone: string;
    salonName: string;
    ownerEmail: string | null;
    avgTicketCents: number | null;
  },
): Promise<string | null> {
  // Re-delivery guard: Vapi retries the end-of-call report, and one call is one booking.
  const existing = await db
    .from('bookings')
    .select('id, call_id')
    .eq('contact_id', a.contactId)
    .order('created_at')
    .limit(1)
    .maybeSingle();
  if (existing.error) return `bookings lookup failed: ${existing.error.message}`;

  let bookingId = existing.data?.id ?? null;
  if (bookingId && !existing.data?.call_id && a.callRowId) {
    // An earlier delivery wrote the booking before its calls row existed. Link it now so the
    // booking is still traceable to the call it came from.
    const linked = await db
      .from('bookings')
      .update({ call_id: a.callRowId })
      .eq('id', bookingId)
      .is('call_id', null);
    if (linked.error) {
      console.error('[vapi-webhook] booking left unlinked', bookingId, linked.error.message);
    }
  }
  if (!bookingId) {
    const inserted = await db
      .from('bookings')
      .insert({
        contact_id: a.contactId,
        client_id: a.clientId,
        call_id: a.callRowId,
        slot_text: a.slotText,
        confirmed: false,
        estimated_value_cents: a.avgTicketCents,
      })
      .select('id')
      .maybeSingle();
    if (inserted.error || !inserted.data) {
      // A unique violation on bookings_contact_id_key is not a failure: it means a concurrent
      // delivery inserted this contact's booking between our select and our insert, and Postgres
      // settled the race for us. The winner sends the alert (it claims notified_at), so this
      // delivery is done — retrying it would only lose the same race again.
      if (isUniqueViolation(inserted.error)) {
        console.warn('[vapi-webhook] concurrent delivery already booked this contact', a.contactId);
        return null;
      }
      // Lost revenue if it stays lost, and the guard above makes a replay safe: ask for one.
      return `booking insert failed: ${inserted.error?.message ?? 'no row returned'}`;
    }
    bookingId = inserted.data.id;

    // Belt and braces for a database where bookings_contact_id_key could not be created (see
    // 0001_init.sql: it is skipped when duplicates already exist). Without the index two overlapping
    // deliveries can both pass the select-then-insert above, so settle it after the fact: the oldest
    // row for this contact is the real one, and the loser removes the row it just wrote and leaves
    // the alert to the winner. With the index in place this never finds anything.
    if (await droppedAsDuplicate(db, a.contactId, bookingId)) return null;
  }

  if (!a.ownerEmail) return null; // no address to send it to; the row is the durable part

  // The instant booking email is the product, and notified_at is what stops it being sent twice.
  // Claim it BEFORE the send with one conditional update — `where id = … and notified_at is null`
  // returns a row to exactly one delivery — so a re-delivery cannot double-book the owner's chair.
  const claimed = await db
    .from('bookings')
    .update({ notified_at: new Date().toISOString() })
    .eq('id', bookingId)
    .is('notified_at', null)
    .select('id')
    .maybeSingle();
  if (claimed.error) return `booking alert claim failed: ${claimed.error.message}`;
  if (!claimed.data) return null; // an earlier delivery already emailed the owner

  const sent = await sendBookingAlert({
    to: a.ownerEmail,
    salonName: a.salonName,
    firstName: a.firstName,
    phone: a.phone,
    slotText: a.slotText,
    summary: a.summary,
    transcriptUrl: a.transcriptUrl,
    estimatedValueCents: a.avgTicketCents,
  });

  if (!sent.ok) {
    // Not a reason to fail the delivery: Vapi re-delivering a report is not a mail retry, and a
    // 500 here would replay every write above for a send that failed at Resend. Log it and hand
    // the claim back, so notified_at keeps meaning "the owner was emailed".
    console.error('[vapi-webhook] booking alert failed:', sent.error);
    const cleared = await db.from('bookings').update({ notified_at: null }).eq('id', bookingId);
    if (cleared.error) {
      console.error('[vapi-webhook] booking alert claim stuck', bookingId, cleared.error.message);
    }
  }
  return null;
}

/** Postgres 23505 — the row this delivery tried to write already exists. */
function isUniqueViolation(error: { code?: string } | null): boolean {
  return error?.code === '23505';
}

/**
 * Post-insert reconciliation for the select-then-insert window: if a concurrent delivery already
 * wrote a booking for this contact, the older row is the real one and the row we just wrote goes.
 * Returns true when ours was the duplicate. Dead code once bookings_contact_id_key exists, and kept
 * for the database where it could not be created.
 */
async function droppedAsDuplicate(
  db: Db,
  contactId: string,
  bookingId: string,
): Promise<boolean> {
  const { data, error } = await db
    .from('bookings')
    .select('id')
    .eq('contact_id', contactId)
    .order('created_at')
    .order('id');
  if (error) {
    console.error('[vapi-webhook] duplicate booking check failed', bookingId, error.message);
    return false;
  }
  if (!data || data.length < 2 || data[0].id === bookingId) return false;

  const removed = await db.from('bookings').delete().eq('id', bookingId);
  if (removed.error) {
    // A duplicate row in /admin/bookings is cosmetic; the half that matters is skipping the alert
    // below, so a failed delete is logged rather than escalated.
    console.error('[vapi-webhook] duplicate booking left behind', bookingId, removed.error.message);
  }
  return true;
}

async function findCall(db: Db, vapiCallId: string): Promise<CallRow | null> {
  const { data, error } = await db
    .from('calls')
    .select('id, contact_id, client_id, outcome')
    .eq('vapi_call_id', vapiCallId)
    .maybeSingle();
  // Not fatal — resolveIds falls back to the payload metadata — but it costs us the TERMINAL
  // guard, so it never happens quietly.
  if (error) console.error('[vapi-webhook] call lookup failed', vapiCallId, error.message);
  return data ?? null;
}

function resolveIds(
  message: Record<string, unknown>,
  existing: CallRow | null,
): { contactId: string | null; clientId: string | null } {
  const metadata = asRecord(asRecord(message.call)?.metadata);
  return {
    contactId: existing?.contact_id ?? str(metadata?.contact_id),
    clientId: existing?.client_id ?? str(metadata?.client_id),
  };
}

function vapiCallId(message: Record<string, unknown>): string | null {
  return str(asRecord(message.call)?.id) ?? str(message.callId);
}

type Structured = {
  outcome: string | null;
  slotText: string | null;
  optOut: boolean;
  notes: string | null;
};

/** Vapi may hand back structuredData as an object, as a JSON string, or not at all. */
function readStructuredData(raw: unknown): Structured {
  let value: unknown = raw;
  if (typeof raw === 'string') {
    try {
      value = JSON.parse(raw);
    } catch {
      value = null;
    }
  }
  const rec = asRecord(value);
  const optOut = rec?.opt_out;
  return {
    outcome: str(rec?.outcome),
    slotText: str(rec?.slot_text),
    optOut: optOut === true || (typeof optOut === 'string' && /^(true|yes|1)$/i.test(optOut)),
    notes: str(rec?.notes),
  };
}

/**
 * Compliance gate: opt-out detection, fail-closed. The extractor is the primary signal — it read
 * the whole conversation — and the transcript match is the backstop for when the analysis plan
 * times out or is skipped entirely. Either one alone is enough: a caller who asked in plain words
 * to be removed is removed even when the extractor says otherwise.
 *
 * The phrase list and the caller-only scoping live in src/lib/opt-out.ts, where they are unit
 * tested (tests/opt-out.test.ts).
 */
function detectOptOut(s: Structured, transcript: string): boolean {
  if (s.optOut || s.outcome === 'opted_out') return true;
  return containsOptOutRequest(transcript);
}

/**
 * The stored outcome and the booking decision, resolved together.
 *
 * `booked` is deliberately independent of `outcome`: an opt-out has to be the recorded outcome —
 * it is the compliance fact, and it is what contacts.status must become — but the salon still
 * gets a slot the client actually agreed to. A slot only counts if a conversation happened: an
 * unanswered ring or a voicemail agreed to nothing, whatever the extractor read into it.
 */
function resolveCall(
  endedReason: string | null,
  s: Structured,
  optOut: boolean,
): { outcome: CallOutcome; booked: boolean } {
  // Telephony facts beat the transcript reader.
  const reason = (endedReason ?? '').toLowerCase();
  const silent =
    reason.includes('did-not-answer') ||
    reason.includes('no-answer') ||
    reason.includes('voicemail') ||
    reason.includes('busy');

  const booked = !silent && s.outcome === 'booked' && s.slotText !== null;

  return { outcome: outcomeFor(reason, s, booked, optOut), booked };
}

function outcomeFor(reason: string, s: Structured, booked: boolean, optOut: boolean): CallOutcome {
  if (optOut) return 'opted_out';

  if (reason.includes('did-not-answer') || reason.includes('no-answer')) return 'no_answer';
  if (reason.includes('voicemail')) return 'voicemail';
  if (reason.includes('busy')) return 'busy';

  // A captured slot outranks an error-ish endedReason: the voice pipeline can die seconds after
  // the client agreed to a time, and the analysis plan reads the transcript either way. Booked is
  // the outcome this business exists to record — losing it to a late TTS failure is lost revenue.
  if (booked) return 'booked';
  if (reason.includes('error')) return 'failed';

  if (s.outcome === 'declined') return 'declined';
  if (s.outcome === 'voicemail') return 'voicemail';
  if (s.outcome === 'no_answer') return 'no_answer';
  return 'answered';
}

function contactStatusFor(outcome: CallOutcome): ContactStatus {
  switch (outcome) {
    case 'booked':
      return 'booked';
    case 'declined':
      return 'declined';
    case 'opted_out':
      return 'opted_out';
    case 'no_answer':
      return 'no_answer';
    case 'failed':
      return 'failed';
    default:
      return 'called';
  }
}

function durationSeconds(
  message: Record<string, unknown>,
  startedAt: string | null,
  endedAt: string,
): number | null {
  const direct = num(message.durationSeconds);
  if (direct !== null) return Math.round(direct);

  const ms = num(message.durationMs);
  if (ms !== null) return Math.round(ms / 1000);

  if (!startedAt) return null;
  const span = Date.parse(endedAt) - Date.parse(startedAt);
  return Number.isFinite(span) && span >= 0 ? Math.round(span / 1000) : null;
}

/** Vapi timestamps arrive as ISO strings or epoch millis; Postgres wants ISO. */
function isoDate(v: unknown): string | null {
  if (typeof v === 'number' && Number.isFinite(v)) return new Date(v).toISOString();
  if (typeof v === 'string' && v.trim().length > 0) {
    const t = Date.parse(v);
    return Number.isFinite(t) ? new Date(t).toISOString() : null;
  }
  return null;
}

function asRecord(v: unknown): Record<string, unknown> | null {
  return typeof v === 'object' && v !== null && !Array.isArray(v)
    ? (v as Record<string, unknown>)
    : null;
}

function str(v: unknown): string | null {
  if (typeof v === 'string') return v.trim().length > 0 ? v.trim() : null;
  if (typeof v === 'number' && Number.isFinite(v)) return String(v);
  return null;
}

function num(v: unknown): number | null {
  if (typeof v === 'number' && Number.isFinite(v)) return v;
  if (typeof v === 'string' && v.trim().length > 0) {
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
  }
  return null;
}
