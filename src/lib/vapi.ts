import { timingSafeEqual } from 'node:crypto';

import { optionalEnv, serverEnv } from '@/lib/env';
import { err, ok, type Result } from '@/lib/result';

const VAPI_BASE = 'https://api.vapi.ai';
const DIAL_TIMEOUT_MS = 15_000;
const LIST_TIMEOUT_MS = 8_000;

/** Vapi call states that still occupy one of our concurrent telephony lines. */
const LIVE_STATUSES = new Set(['queued', 'scheduled', 'ringing', 'in-progress', 'forwarding']);

export type StartCallArgs = {
  phone: string;
  assistantId: string;
  phoneNumberId: string;
  variables: Record<string, string>;
  metadata: Record<string, string>;
  /**
   * Per-call prompt override. Demo calls only — see src/lib/demo.ts.
   *
   * Campaign dials must NOT pass this: overriding the model block costs Vapi's warm prompt cache
   * and pushes time-to-first-token out of the sub-second budget in ARCHITECTURE.md §2. One demo
   * call to a salon owner who is expecting it can afford the extra latency; three hundred calls to
   * lapsed clients cannot.
   */
  systemPrompt?: string;
  firstMessage?: string;
  /** A Vapi first-party voiceId. Demo calls only, same latency caveat as systemPrompt. */
  voiceId?: string;
};

export async function startOutboundCall(a: StartCallArgs): Promise<Result<{ vapiCallId: string }>> {
  let apiKey: string;
  try {
    apiKey = serverEnv('VAPI_API_KEY');
  } catch {
    return err('VAPI_API_KEY is not configured');
  }

  try {
    const res = await fetch(`${VAPI_BASE}/call`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phoneNumberId: a.phoneNumberId,
        assistantId: a.assistantId,
        // Per-customer personalisation only — no assistant/model overrides, so Vapi keeps
        // the warm prompt cache and time-to-first-token stays inside the latency budget.
        // The prompt override below is the one exception, and only demo calls set it.
        assistantOverrides: {
          variableValues: a.variables,
          ...(a.systemPrompt
            ? { model: { messages: [{ role: 'system', content: a.systemPrompt }] } }
            : {}),
          ...(a.firstMessage ? { firstMessage: a.firstMessage } : {}),
          ...(a.voiceId ? { voice: { provider: 'vapi', voiceId: a.voiceId } } : {}),
        },
        customer: { number: a.phone },
        metadata: a.metadata,
      }),
      signal: AbortSignal.timeout(DIAL_TIMEOUT_MS),
      cache: 'no-store',
    });

    const body = await res.text();
    if (!res.ok) return err(`vapi ${res.status}: ${body.slice(0, 300)}`);

    const id = readCallId(body);
    return id ? ok({ vapiCallId: id }) : err(`vapi 200 without call id: ${body.slice(0, 200)}`);
  } catch (e) {
    return err(e instanceof Error ? e.message : 'vapi request failed');
  }
}

/** Compliance gate: an unauthenticated webhook could forge opt-outs and bookings. */
export function verifyVapiRequest(secretHeader: string | null): boolean {
  if (!secretHeader) return false;
  const expected = optionalEnv('VAPI_WEBHOOK_SECRET');
  if (!expected) return false; // fail closed when unconfigured
  return timingSafeEqualString(secretHeader, expected);
}

/** Belt-and-braces line count straight from the provider. Returns 0 on any error. */
export async function listActiveCallCount(): Promise<number> {
  const apiKey = optionalEnv('VAPI_API_KEY');
  if (!apiKey) return 0;

  try {
    const res = await fetch(`${VAPI_BASE}/call?limit=100`, {
      headers: { Authorization: `Bearer ${apiKey}` },
      signal: AbortSignal.timeout(LIST_TIMEOUT_MS),
      cache: 'no-store',
    });
    if (!res.ok) return 0;

    const parsed: unknown = JSON.parse(await res.text());
    const rows = Array.isArray(parsed) ? parsed : [];
    return rows.filter((row) => {
      const status = isRecord(row) ? row.status : undefined;
      return typeof status === 'string' && LIVE_STATUSES.has(status);
    }).length;
  } catch {
    return 0;
  }
}

function readCallId(body: string): string | null {
  try {
    const parsed: unknown = JSON.parse(body);
    if (!isRecord(parsed)) return null;
    const id = parsed.id;
    return typeof id === 'string' && id.length > 0 ? id : null;
  } catch {
    return null;
  }
}

function timingSafeEqualString(a: string, b: string): boolean {
  const left = Buffer.from(a, 'utf8');
  const right = Buffer.from(b, 'utf8');
  if (left.length !== right.length) return false;
  return timingSafeEqual(left, right);
}

function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === 'object' && v !== null;
}
