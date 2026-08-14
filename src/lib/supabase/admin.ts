import { createClient, type SupabaseClient } from '@supabase/supabase-js';
import { publicEnv, serverEnv } from '@/lib/env';
import type { Database } from '@/lib/types';

/**
 * Service-role client. Bypasses RLS, so this module must never be imported by
 * a "use client" component. Every table has RLS on with zero policies, which
 * means this is the only key that can read or write anything.
 */
export function supabaseAdmin(): SupabaseClient<Database> {
  const url = publicEnv.supabaseUrl;
  if (!url) throw new Error('Missing required environment variable: NEXT_PUBLIC_SUPABASE_URL');

  return createClient<Database>(url, serverEnv('SUPABASE_SERVICE_ROLE_KEY'), {
    auth: { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false },
    global: { headers: { 'x-application-name': 'salon-malone' } },
  });
}
