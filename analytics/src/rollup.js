// Fold a day's pageviews into `daily`, one row per (dimension, key). Each
// dimension is one GROUP BY over the day's slice of `hits`, done inside D1,
// and a row is only rewritten when its numbers moved, so re-rolling a quiet
// day costs reads but almost no writes.

import { addDays, dayBounds, dayOf, startOfDay } from './time.js';
import { timezone } from './http.js';

const DIMS = [
  ['total', "''"],
  ['hour', "printf('%02d', hour)"],
  ['path', 'path'],
  ['source', "channel || '|' || COALESCE(ref, '') || '|' || COALESCE(utm_campaign, '')"],
  ['geo', "COALESCE(country, '') || '|' || COALESCE(city, '')"],
  ['tech', "COALESCE(device, '') || '|' || COALESCE(browser, '') || '|' || COALESCE(os, '')"],
];

const COLUMNS = ['views', 'readers', 'visits', 'engaged', 'engaged_n', 'reads', 'articles'];

// `articles` counts article pageviews that reported how far they got, which is
// the fair denominator for read-through: a beacon that never arrived is not a
// reader who gave up.
const AGGREGATES = `COUNT(*), COUNT(DISTINCT visitor), SUM(entry), SUM(engaged), SUM(engaged > 0),
  SUM(published IS NOT NULL AND depth >= 90),
  SUM(published IS NOT NULL AND (engaged > 0 OR depth > 0))`;

const UPSERT = `ON CONFLICT (dim, day, key) DO UPDATE SET
  ${COLUMNS.map((c) => `${c} = excluded.${c}`).join(', ')}
  WHERE ${COLUMNS.map((c) => `daily.${c} != excluded.${c}`).join(' OR ')}`;

const stamp = (db, k, now) => db.prepare(
  'INSERT INTO meta (k, v) VALUES (?1, ?2) ON CONFLICT (k) DO UPDATE SET v = excluded.v',
).bind(k, String(Math.floor(now / 1000)));

export async function rollupDay(env, day, { final = false, now = Date.now() } = {}) {
  const db = env.DB;
  const [start, end] = dayBounds(day, timezone(env));
  const statements = DIMS.map(([dim, key]) => db.prepare(
    `INSERT INTO daily (dim, day, key, ${COLUMNS.join(', ')})
     SELECT ?1, ?2, ${key}, ${AGGREGATES} FROM hits WHERE ts >= ?3 AND ts < ?4 GROUP BY 3
     ${UPSERT}`,
  ).bind(dim, day, start, end));
  // The newest title, desk and date for each page (SQLite takes the bare
  // columns from the row that supplied MAX(ts)).
  statements.push(db.prepare(
    `INSERT INTO pages (path, title, desk, published, last_seen)
     SELECT path, title, desk, published, MAX(ts) FROM hits WHERE ts >= ?1 AND ts < ?2 GROUP BY path
     ON CONFLICT (path) DO UPDATE SET
       title = COALESCE(excluded.title, pages.title), desk = COALESCE(excluded.desk, pages.desk),
       published = COALESCE(excluded.published, pages.published), last_seen = excluded.last_seen
     WHERE excluded.last_seen > pages.last_seen`,
  ).bind(start, end));
  statements.push(stamp(db, `rolled:${day}`, now));
  if (final) statements.push(stamp(db, `final:${day}`, now));
  await db.batch(statements);
}

/** Re-roll `day` unless it is final or was rolled within `maxAge` seconds. */
export async function freshen(env, day, { final = false, now = Date.now(), maxAge = 600 } = {}) {
  const { results } = await env.DB.prepare('SELECT k, v FROM meta WHERE k IN (?1, ?2)')
    .bind(`rolled:${day}`, `final:${day}`).all();
  const seen = Object.fromEntries(results.map((r) => [r.k.split(':')[0], Number(r.v)]));
  if (seen.final) return false;
  if (!final && seen.rolled && now / 1000 - seen.rolled < maxAge) return false;
  await rollupDay(env, day, { final, now });
  return true;
}

/** A day is settled two hours after it ends, once late reading-time beacons are in. */
export function settled(day, tz, now = Date.now()) {
  return now >= startOfDay(addDays(day, 1), tz) + 2 * 3600 * 1000;
}

export async function prune(env, now = Date.now()) {
  const tz = timezone(env);
  const keep = Number(env.RETENTION_DAYS ?? 400);
  const old = dayOf(now - 40 * 86400 * 1000, tz);
  const statements = [
    env.DB.prepare("DELETE FROM meta WHERE k >= 'final:' AND k < ?1").bind(`final:${old}`),
    env.DB.prepare("DELETE FROM meta WHERE k >= 'rolled:' AND k < ?1").bind(`rolled:${old}`),
  ];
  // Raw pageviews go after RETENTION_DAYS (0 keeps them); the daily totals stay.
  if (keep > 0) statements.push(env.DB.prepare('DELETE FROM hits WHERE ts < ?1').bind(Math.floor(now / 1000) - keep * 86400));
  await env.DB.batch(statements);
}

/** The scheduled job: today, the three days before it, then housekeeping. */
export async function cron(env, now = Date.now()) {
  const tz = timezone(env);
  const today = dayOf(now, tz);
  await rollupDay(env, today, { now });
  for (let i = 3; i >= 1; i--) {
    const day = addDays(today, -i);
    await freshen(env, day, { final: settled(day, tz, now), now, maxAge: 0 });
  }
  await prune(env, now);
}
