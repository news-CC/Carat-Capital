import { timingSafeEqual } from 'node:crypto';

import { optionalEnv } from '@/lib/env';

/**
 * One authorizer for both cron routes. It lived twice — once in /api/cron/dial and once in
 * /api/cron/report — and two copies of an auth check drift.
 *
 * The shared secret is the ONLY credential. `x-vercel-cron` is deliberately not trusted: any
 * header is attacker-controlled on a public deployment, and /api/cron/dial places real phone
 * calls to real consumers. Treating that header as proof of origin would let anyone who knows
 * the URL burn every contact's single dial attempt.
 *
 * Vercel injects `Authorization: Bearer $CRON_SECRET` into scheduled invocations whenever the
 * CRON_SECRET env var is set, so requiring it costs nothing operationally.
 * https://vercel.com/docs/cron-jobs/manage-cron-jobs#securing-cron-jobs
 *
 * Fails closed: no secret configured means no cron run, rather than an open endpoint.
 * Node runtime only (node:crypto), which both cron routes already are.
 */
export function authorizeCron(req: Request): boolean {
  const secret = optionalEnv('CRON_SECRET');
  if (!secret) return false;

  const presented = Buffer.from(req.headers.get('authorization') ?? '', 'utf8');
  const expected = Buffer.from(`Bearer ${secret}`, 'utf8');
  return presented.length === expected.length && timingSafeEqual(presented, expected);
}
