/**
 * The ONLY module allowed to read process.env.
 * Server keys are read lazily so a missing key fails at the call site (with a
 * useful message) instead of at import time, which would break `next build`.
 */

export type ServerEnvKey =
  | 'VAPI_API_KEY'
  | 'VAPI_PHONE_NUMBER_ID'
  | 'VAPI_ASSISTANT_ID'
  | 'VAPI_WEBHOOK_SECRET'
  | 'SUPABASE_SERVICE_ROLE_KEY'
  | 'RESEND_API_KEY'
  | 'EMAIL_FROM'
  | 'STRIPE_SECRET_KEY'
  | 'STRIPE_WEBHOOK_SECRET'
  | 'STRIPE_LINK_SALON_399'
  | 'STRIPE_LINK_MEDSPA_999'
  | 'STRIPE_LINK_GROUP_2499'
  | 'STRIPE_LINK_PILOT_299'
  | 'ADMIN_EMAIL'
  | 'ADMIN_PASSWORD_HASH'
  | 'CRON_SECRET'
  | 'CALL_WINDOW_START'
  | 'CALL_WINDOW_END'
  | 'REQUIRE_CONSENT_FLAG'
  | 'MAX_CONCURRENT_CALLS'
  | 'BOOKING_CALL_URL';

const DEFAULT_WINDOW_START = '09:00';
const DEFAULT_WINDOW_END = '19:00';
const DEFAULT_MAX_CONCURRENT_CALLS = 8;

/** Throws when the variable is missing or blank. Use for anything we cannot fake. */
export function serverEnv(key: ServerEnvKey): string {
  const value = process.env[key];
  if (value === undefined || value.trim() === '') {
    throw new Error(`Missing required environment variable: ${key}`);
  }
  return value.trim();
}

export function optionalEnv(key: string, fallback?: string): string | undefined {
  const value = process.env[key];
  if (value === undefined || value.trim() === '') return fallback;
  return value.trim();
}

/** 'HH:MM' 24h, zero-padded. Anything unparseable falls back to the default. */
function normalizeClock(value: string | undefined, fallback: string): string {
  if (!value) return fallback;
  const m = /^(\d{1,2}):(\d{2})$/.exec(value.trim());
  if (!m) return fallback;
  const hour = Number(m[1]);
  const minute = Number(m[2]);
  if (hour > 23 || minute > 59) return fallback;
  return `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`;
}

export function callWindow(): { start: string; end: string } {
  return {
    start: normalizeClock(optionalEnv('CALL_WINDOW_START'), DEFAULT_WINDOW_START),
    end: normalizeClock(optionalEnv('CALL_WINDOW_END'), DEFAULT_WINDOW_END),
  };
}

/**
 * Compliance gate: consent is required unless the operator explicitly opts out
 * by setting REQUIRE_CONSENT_FLAG=false. Anything else (unset, typo) means ON.
 */
export function requireConsent(): boolean {
  return optionalEnv('REQUIRE_CONSENT_FLAG')?.toLowerCase() !== 'false';
}

export function maxConcurrentCalls(): number {
  const parsed = Number.parseInt(optionalEnv('MAX_CONCURRENT_CALLS') ?? '', 10);
  if (!Number.isFinite(parsed) || parsed < 1) return DEFAULT_MAX_CONCURRENT_CALLS;
  return parsed;
}

/**
 * Read with literal keys — Next.js only inlines NEXT_PUBLIC_* for the browser
 * bundle when the access is statically analysable.
 */
export const publicEnv: { supabaseUrl: string; supabaseAnonKey: string; appUrl: string } = {
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL ?? '',
  supabaseAnonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? '',
  appUrl: process.env.NEXT_PUBLIC_APP_URL ?? 'http://localhost:3000',
};
