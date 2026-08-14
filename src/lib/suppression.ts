import type { SupabaseClient } from '@supabase/supabase-js';

import { err, ok, type Result } from '@/lib/result';
import type { Database } from '@/lib/types';

/**
 * THE GLOBAL DO-NOT-CONTACT GATE, in one place.
 *
 * Four call sites write or read this list — the Vapi webhook (a caller said stop), the admin
 * suppression form, the per-contact suppress button, and both scrub paths — and they used to carry
 * three slightly different versions of the same two operations, which is how a compliance gate drifts:
 * one wrote `scrub_reason = 'opt_out'` and another `'suppression:opt_out'`, one paged the list and
 * another threw instead of returning. There is exactly one implementation of each here.
 *
 * Not a `"use server"` module on purpose: every export of one becomes a callable endpoint, which is
 * why the two upload paths could not share their copies. Plain server-side library code can be
 * shared by a server action and a route handler alike.
 */

type Db = SupabaseClient<Database>;

/** Mirrors the suppression_reason_chk CHECK in 0001_init.sql. */
export const SUPPRESSION_REASONS = ['opt_out', 'dnc', 'complaint', 'invalid', 'manual'] as const;
export type SuppressionReason = (typeof SUPPRESSION_REASONS)[number];

/** Anything unrecognised is 'manual': a reason we cannot read must never drop the suppression. */
export function asSuppressionReason(value: unknown): SuppressionReason {
  return SUPPRESSION_REASONS.find((reason) => reason === value) ?? 'manual';
}

/** PostgREST caps a response at 1000 rows, so the list is read a page at a time. */
const SUPPRESSION_PAGE = 1_000;
const SUPPRESSION_CAP = 200_000;

/**
 * The whole suppression list as E.164 strings. Small table by design: one row per person who ever
 * said no. Errors come back as a Result — a scrub that silently ran against half the list would
 * dial people who asked us not to, so every caller has to decide out loud what to do with a failure.
 */
export async function loadSuppressionPhones(db: Db): Promise<Result<Set<string>>> {
  const phones = new Set<string>();
  for (let from = 0; from < SUPPRESSION_CAP; from += SUPPRESSION_PAGE) {
    const { data, error } = await db
      .from('suppression')
      .select('phone')
      .order('phone')
      .range(from, from + SUPPRESSION_PAGE - 1);
    if (error) return err(`the do-not-contact list could not be read (${error.message})`);
    if (!data || data.length === 0) break;
    for (const row of data) if (row.phone) phones.add(row.phone);
    if (data.length < SUPPRESSION_PAGE) break;
  }
  return ok(phones);
}

/**
 * Suppresses a number everywhere, synchronously: the durable global row first, then the fan-out that
 * pulls the number out of every client's pending queue immediately rather than waiting for the claim
 * query to skip it.
 *
 * The return value is deliberately narrow — it reports ONLY a failure of the durable row, because
 * that is the half a caller may need to retry (the Vapi webhook answers 500 so the report is
 * re-delivered). A failed fan-out is logged and swallowed on purpose: the suppression row is the
 * gate, and both `claim_contacts_for_dialing` and the dial route re-check it before every dial, so a
 * pending row that kept its status still never gets called.
 *
 * `tag` is the log prefix of the calling path, e.g. '[vapi-webhook]'. It stays at the very start of
 * the line, ahead of any per-call `context`, because '[vapi-webhook] SUPPRESSION WRITE FAILED' is the
 * exact string a log alert matches on — after Vapi exhausts its retries that line is the only trace
 * that someone asked to be left alone and was not recorded.
 */
export async function suppressPhoneGlobally(
  db: Db,
  a: {
    phone: string;
    reason: SuppressionReason;
    sourceContactId?: string | null;
    tag: string;
    context?: string;
  },
): Promise<{ error: string | null }> {
  // Idempotent: replaying the same opt-out is a no-op, never a duplicate-key failure.
  const wrote = await db.from('suppression').upsert(
    { phone: a.phone, reason: a.reason, source_contact_id: a.sourceContactId ?? null },
    { onConflict: 'phone', ignoreDuplicates: true },
  );
  if (wrote.error) {
    // The number is in this line because it is the only trace left of a person we failed to
    // suppress — without it nobody can go and add the row by hand.
    console.error(`${a.tag} SUPPRESSION WRITE FAILED`, a.context ?? '-', a.phone, wrote.error.message);
    return { error: `suppression write failed: ${wrote.error.message}` };
  }

  const fanout = await db
    .from('contacts')
    .update({ status: 'suppressed', scrub_reason: `suppression:${a.reason}` })
    .eq('phone', a.phone)
    .eq('status', 'pending');
  if (fanout.error) {
    console.error(`${a.tag} suppression fan-out failed`, a.context ?? '-', a.phone, fanout.error.message);
  }

  return { error: null };
}
