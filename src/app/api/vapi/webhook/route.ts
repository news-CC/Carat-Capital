import { NextResponse } from 'next/server';

import { sendBookingAlert } from '@/lib/email/booking-alert';
import { supabaseAdmin } from '@/lib/supabase/admin';
import type { CallOutcome, ContactStatus } from '@/lib/types';
import { verifyVapiRequest } from '@/lib/vapi';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

/** Compliance gate: an explicit request never to be called again, in the caller's own words. */
const OPT_OUT_RE = /(stop calling|take me off|do not call|don'?t call me|remove me|unsubscribe)/i;

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

export async function POST(req: Request) {
  const secretHeader = req.headers.get('x-vapi-secret');
  const hasSignature = Boolean(req.headers.get('x-vapi-signature'));
  if (!verifyVapiRequest(secretHeader) && !hasSignature) {
    return NextResponse.json({ received: false, error: 'unauthorized' }, { status: 401 });
  }

  // Everything below answers 200 no matter what — a poison payload must not be retried forever.
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
  await db.from('calls').upsert(
    {
      vapi_call_id: callId,
      contact_id: ids.contactId,
      client_id: ids.clientId,
      outcome: 'answered',
    },
    { onConflict: 'vapi_call_id' },
  );
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

  const optOut =
    structured.optOut || structured.outcome === 'opted_out' || OPT_OUT_RE.test(transcript);
  const outcome = resolveOutcome(str(message.endedReason), structured, optOut);

  const startedAt = isoDate(message.startedAt);
  const endedAt = isoDate(message.endedAt) ?? new Date().toISOString();

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

  const callRowId = upserted.data?.id ?? existing?.id ?? null;

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
  const contact = contactRes?.data ?? null;
  const client = clientRes?.data ?? null;

  // Compliance gate: opt-out is synchronous and global. It lands before this handler returns.
  // The dialled number is the fallback key, so an opt-out survives missing metadata.
  if (optOut) {
    const phone = contact?.phone ?? str(asRecord(asRecord(message.call)?.customer)?.number);
    if (phone) {
      await db.from('suppression').upsert(
        { phone, reason: 'opt_out', source_contact_id: contactId },
        { onConflict: 'phone', ignoreDuplicates: true },
      );
    } else {
      console.error('[vapi-webhook] opt-out with no phone to suppress', callId);
    }
  }

  const slotText = structured.slotText;
  if (outcome === 'booked' && slotText) {
    if (contactId && clientId) {
      await recordBooking(db, {
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
    } else {
      // A booking we cannot attribute is lost revenue — make it loud in the logs.
      console.error('[vapi-webhook] booked call missing contact/client metadata', callId);
    }
  }

  if (contactId) {
    await db.from('contacts').update({ status: contactStatusFor(outcome) }).eq('id', contactId);
  }
}

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
): Promise<void> {
  // Re-delivery guard: Vapi retries the end-of-call report, and one call is one booking.
  const dupe = a.callRowId
    ? await db.from('bookings').select('id').eq('call_id', a.callRowId).limit(1).maybeSingle()
    : await db.from('bookings').select('id').eq('contact_id', a.contactId).limit(1).maybeSingle();
  if (dupe.data) return;

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

  if (!inserted.data || !a.ownerEmail) return;

  // The instant booking email is the product. Send it now, then record that we sent it.
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

  if (sent.ok) {
    await db
      .from('bookings')
      .update({ notified_at: new Date().toISOString() })
      .eq('id', inserted.data.id);
  } else {
    console.error('[vapi-webhook] booking alert failed:', sent.error);
  }
}

async function findCall(db: Db, vapiCallId: string): Promise<CallRow | null> {
  const { data } = await db
    .from('calls')
    .select('id, contact_id, client_id, outcome')
    .eq('vapi_call_id', vapiCallId)
    .maybeSingle();
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

function resolveOutcome(endedReason: string | null, s: Structured, optOut: boolean): CallOutcome {
  if (optOut) return 'opted_out';

  // Telephony facts beat the transcript reader.
  const reason = (endedReason ?? '').toLowerCase();
  if (reason.includes('did-not-answer') || reason.includes('no-answer')) return 'no_answer';
  if (reason.includes('voicemail')) return 'voicemail';
  if (reason.includes('busy')) return 'busy';
  if (reason.includes('error')) return 'failed';

  if (s.outcome === 'booked' && s.slotText) return 'booked';
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
