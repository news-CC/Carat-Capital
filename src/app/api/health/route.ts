import { NextResponse } from 'next/server';

import { getSession } from '@/lib/auth';
import { authorizeCron } from '@/lib/cron-auth';
import { optionalEnv } from '@/lib/env';
import { supabaseAdmin } from '@/lib/supabase/admin';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

/** Presence only — a health endpoint must never echo a secret's value. */
const ENV_KEYS = [
  'VAPI_API_KEY',
  'VAPI_PHONE_NUMBER_ID',
  'VAPI_ASSISTANT_ID',
  'VAPI_WEBHOOK_SECRET',
  'SUPABASE_SERVICE_ROLE_KEY',
  'RESEND_API_KEY',
  'EMAIL_FROM',
  'STRIPE_SECRET_KEY',
  'STRIPE_WEBHOOK_SECRET',
  'ADMIN_EMAIL',
  'ADMIN_PASSWORD_HASH',
  'CRON_SECRET',
  'NEXT_PUBLIC_SUPABASE_URL',
  'NEXT_PUBLIC_SUPABASE_ANON_KEY',
] as const;

/** Without these the dialer cannot run at all. */
const CRITICAL: readonly string[] = [
  'VAPI_API_KEY',
  'VAPI_PHONE_NUMBER_ID',
  'VAPI_ASSISTANT_ID',
  'SUPABASE_SERVICE_ROLE_KEY',
  'NEXT_PUBLIC_SUPABASE_URL',
];

export async function GET(req: Request) {
  const env: Record<string, boolean> = {};
  for (const key of ENV_KEYS) env[key] = Boolean(optionalEnv(key));

  const database = await checkDatabase();
  const missing = CRITICAL.filter((key) => !env[key]);
  const ok = database.reachable && missing.length === 0;

  // Anonymous callers get liveness only. Which-secret-is-set is a map of the deployment's
  // attack surface, and the raw database error is free fingerprinting — an uptime check needs
  // neither. The detail view is for the operator: the cron bearer, or an admin session.
  if (!authorizeCron(req) && !(await getSession())) {
    return NextResponse.json(
      { ok, service: 'salon-malone', time: new Date().toISOString() },
      { status: ok ? 200 : 503 },
    );
  }

  return NextResponse.json(
    { ok, service: 'salon-malone', time: new Date().toISOString(), env, missing, database },
    { status: ok ? 200 : 503 },
  );
}

async function checkDatabase(): Promise<{ reachable: boolean; error: string | null }> {
  try {
    const { error } = await supabaseAdmin()
      .from('clients')
      .select('id', { head: true, count: 'exact' })
      .abortSignal(AbortSignal.timeout(5_000));
    // Logged, not returned to an unauthenticated caller: the message is only useful to us.
    if (error) console.error('[health] database unreachable', error.message);
    return { reachable: !error, error: error?.message ?? null };
  } catch (e) {
    const message = e instanceof Error ? e.message : 'supabase unreachable';
    console.error('[health] database unreachable', message);
    return { reachable: false, error: message };
  }
}
