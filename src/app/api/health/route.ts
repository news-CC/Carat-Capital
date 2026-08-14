import { NextResponse } from 'next/server';

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

export async function GET() {
  const env: Record<string, boolean> = {};
  for (const key of ENV_KEYS) env[key] = Boolean(optionalEnv(key));

  const database = await checkDatabase();
  const missing = CRITICAL.filter((key) => !env[key]);
  const ok = database.reachable && missing.length === 0;

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
    return { reachable: !error, error: error?.message ?? null };
  } catch (e) {
    return { reachable: false, error: e instanceof Error ? e.message : 'supabase unreachable' };
  }
}
