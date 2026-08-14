import type { SupabaseClient } from '@supabase/supabase-js';

import type { CallOutcome, Database } from '@/lib/types';

type Db = SupabaseClient<Database>;

/**
 * A human answered. Voicemail and busy are dials, not conversations.
 *
 * Defined once because two surfaces publish it: the admin dashboard's reach rate and the Friday
 * report the client reads. If they ever disagreed, the salon's own email would contradict the
 * number we quote them.
 */
export const REACHED_OUTCOMES: CallOutcome[] = ['answered', 'booked', 'declined', 'opted_out'];

/**
 * How long a call may sit unfinished before we treat it as gone. One constant for the stuck-call
 * sweeper (`expire_stuck_calling`), the dialer's concurrency headroom, and the dashboard's in-flight
 * tile, so the three can never disagree about which calls are still up. 15 minutes is 5x Malone's
 * 3 minute hard ceiling.
 */
export const STUCK_CALL_MINUTES = 15;

/**
 * Calls that are still live, counted the only way this schema can answer the question.
 *
 * NOT `outcome = 'dialing'`: the webhook's status-update handler rewrites a live call's outcome to
 * 'answered', which is also what a finished conversation gets, so `outcome` cannot separate live from
 * done and a count built on it undercounts the lines actually in use. `ended_at` can: every writer
 * that terminates a call stamps it (the end-of-call report, dialOne's failed-dial insert,
 * expire_stuck_calling) and the two live-call writers both leave it NULL.
 *
 * The age bound is the sweeper's own cutoff. Without it a call whose end-of-call report never arrived
 * would hold one of the eight lines forever. A bare not-ended predicate over-counts rather than
 * under-counts, which is the fail-closed direction for a line cap.
 */
export async function countLiveCalls(db: Db): Promise<number> {
  const liveSince = new Date(Date.now() - STUCK_CALL_MINUTES * 60_000).toISOString();
  const { count } = await db
    .from('calls')
    .select('*', { count: 'exact', head: true })
    .is('ended_at', null)
    .gte('created_at', liveSince);
  return count ?? 0;
}
