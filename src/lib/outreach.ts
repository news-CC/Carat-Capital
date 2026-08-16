import { createClient, type SupabaseClient } from '@supabase/supabase-js';

import { optionalEnv } from '@/lib/env';
import { err, ok, type Result } from '@/lib/result';

/**
 * Marketing-unsubscribe support.
 *
 * Salon Malone's own database holds salons and the people they asked us to call. Our COLD outreach
 * to salon owners is queued by a separate engine with its own Supabase project, so the unsubscribe
 * token lives over there. The link still has to resolve on startup25.com — a salon owner clicking
 * "unsubscribe" in an email about Salon Malone must not land on an unrelated job board — hence this
 * one narrow cross-database reader.
 *
 * Nothing else in the app touches this. It is deliberately not wired into supabaseAdmin().
 */
function outreachDb(): SupabaseClient | null {
  const url = optionalEnv('OUTREACH_SUPABASE_URL');
  const key = optionalEnv('OUTREACH_SUPABASE_SERVICE_ROLE_KEY');
  if (!url || !key) return null;
  return createClient(url, key, { auth: { persistSession: false } });
}

export type UnsubscribeOutcome = 'done' | 'invalid' | 'missing' | 'unavailable';

/**
 * Idempotent by construction: the suppression upsert and the queued-message cancellation both
 * converge on the same state, so a mail client that prefetches the link and a human who then clicks
 * it produce one result, not an error the second time.
 */
export async function unsubscribeByToken(token: string | undefined | null): Promise<Result<UnsubscribeOutcome>> {
  const clean = (token ?? '').trim();
  if (!clean) return ok('missing');

  const db = outreachDb();
  if (!db) {
    console.error('[unsubscribe] OUTREACH_SUPABASE_* not configured — cannot honour an opt-out');
    return err('unavailable');
  }

  const { data: message, error } = await db
    .from('outreach_messages')
    .select('id, campaign_id, contact_id, vc_contacts(email)')
    .eq('unsubscribe_token', clean)
    .maybeSingle();

  if (error) {
    console.error('[unsubscribe] lookup failed', { detail: error.message });
    return err('lookup_failed');
  }
  if (!message) return ok('invalid');

  const contact = message.vc_contacts as { email?: string } | null;

  // The suppression row is the durable record — it is what stops every future send. Write it first
  // and treat a failure here as a hard failure, because losing it means we mail them again.
  if (contact?.email) {
    const suppressed = await db
      .from('outreach_suppressions')
      .upsert(
        { email: contact.email, reason: 'unsubscribe', source_campaign: message.campaign_id },
        { onConflict: 'email' },
      );
    if (suppressed.error) {
      console.error('[unsubscribe] SUPPRESSION WRITE FAILED', { detail: suppressed.error.message });
      return err('suppression_failed');
    }
  }

  // Best-effort from here. The person is already suppressed; an audit-log miss or a stale queued
  // row must not turn into an error page that invites them to click again.
  const events = await db
    .from('outreach_events')
    .insert({ message_id: message.id, event_type: 'unsubscribed', payload: { via: 'startup25' } });
  if (events.error) console.error('[unsubscribe] event log failed', { detail: events.error.message });

  const cancelled = await db
    .from('outreach_messages')
    .update({ status: 'suppressed', error: 'unsubscribed by recipient' })
    .eq('contact_id', message.contact_id)
    .eq('status', 'queued');
  if (cancelled.error) console.error('[unsubscribe] queue cancel failed', { detail: cancelled.error.message });

  return ok('done');
}
