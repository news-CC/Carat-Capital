// The dashboard's read API. Everything answers from the `daily` roll-ups
// except the story view and the live panel, which read recent raw pageviews
// through the (path, ts) and (ts) indexes.

import { addDays, dayBounds, dayOf, startOfDay } from './time.js';
import { freshen, settled } from './rollup.js';
import { timezone } from './http.js';

export const RANGES = { today: 1, '7d': 7, '30d': 30, '90d': 90, '12m': 365 };

const METRICS = ['views', 'readers', 'visits', 'engaged', 'engaged_n', 'reads', 'articles'];
const SUMS = METRICS.map((m) => `SUM(${m}) AS ${m}`).join(', ');
const RAW = `COUNT(*) AS views, COUNT(DISTINCT visitor) AS readers, SUM(entry) AS visits,
  SUM(engaged) AS engaged, SUM(engaged > 0) AS engaged_n,
  SUM(published IS NOT NULL AND depth >= 90) AS reads,
  SUM(published IS NOT NULL AND (engaged > 0 OR depth > 0)) AS articles`;

export function numbers(row) {
  const out = {};
  for (const m of METRICS) out[m] = Number(row?.[m]) || 0;
  return out;
}

const add = (a, b) => { for (const m of METRICS) a[m] += Number(b[m]) || 0; return a; };

/** The days a range covers. Multi-day ranges are whole days ending yesterday. */
export function span(range, tz, now = Date.now()) {
  const today = dayOf(now, tz);
  if (range === 'today') {
    const yesterday = addDays(today, -1);
    return { range, today, from: today, to: today, prevFrom: yesterday, prevTo: yesterday };
  }
  const n = RANGES[range];
  const to = addDays(today, -1);
  const from = addDays(to, -(n - 1));
  return { range, today, from, to, prevFrom: addDays(from, -n), prevTo: addDays(from, -1) };
}

function daysBetween(from, to) {
  const out = [];
  for (let d = from; d <= to; d = addDays(d, 1)) out.push(d);
  return out;
}

const HOURS = Array.from({ length: 24 }, (_, h) => String(h).padStart(2, '0'));

/** Rows keyed by `key`, laid over the full list of keys with zeros for gaps. */
function fill(keys, rows, keyOf = (r) => r.key) {
  const byKey = new Map(rows.map((r) => [keyOf(r), r]));
  return keys.map((key) => ({ key, ...numbers(byKey.get(key)) }));
}

function split(rows, parts) {
  return rows.map((r) => {
    const bits = String(r.key).split('|');
    const o = numbers(r);
    parts.forEach((p, i) => { o[p] = bits[i] || ''; });
    return o;
  });
}

/** Sum rows by `field`, largest first by `sortBy`. */
function group(rows, field, sortBy = 'views', extra = () => ({})) {
  const map = new Map();
  for (const r of rows) {
    const k = r[field];
    if (!k) continue;
    if (!map.has(k)) map.set(k, { name: k, ...numbers(), ...extra(r) });
    add(map.get(k), r);
  }
  return [...map.values()].sort((a, b) => b[sortBy] - a[sortBy] || a.name.localeCompare(b.name));
}

// A small per-isolate cache: the dashboard refreshes often, the figures don't.
const cache = new Map();

function remember(key, ttl, now, make) {
  const hit = cache.get(key);
  if (hit && hit.until > now) return hit.value;
  const value = make();
  cache.set(key, { until: now + ttl * 1000, value });
  value.catch(() => cache.delete(key));
  if (cache.size > 64) cache.delete(cache.keys().next().value);
  return value;
}

export function overview(env, url, now = Date.now()) {
  const range = RANGES[url.searchParams.get('range')] ? url.searchParams.get('range') : '30d';
  const s = span(range, timezone(env), now);
  return remember(`overview:${range}:${s.to}`, range === 'today' ? 60 : 600, now, () => buildOverview(env, s, now));
}

async function buildOverview(env, s, now) {
  const tz = timezone(env);
  const db = env.DB;
  const q = (sql, ...args) => db.prepare(sql).bind(...args);

  // Today is always refreshed, even for ranges that end yesterday, so the
  // dashboard knows counting has begun on a site's very first day.
  await freshen(env, s.today, { now });
  if (s.range !== 'today') await freshen(env, s.to, { final: settled(s.to, tz, now), now });

  const today = s.range === 'today';
  const [start] = dayBounds(s.today, tz);
  const yStart = startOfDay(s.prevFrom, tz) / 1000;
  const elapsed = Math.floor(now / 1000) - start;

  const [cur, prev, series, prevSeries, hours, paths, sources, geo, tech, first, demo] = await db.batch([
    q(`SELECT ${SUMS} FROM daily WHERE dim = 'total' AND day BETWEEN ?1 AND ?2`, s.from, s.to),
    today
      // Today so far against yesterday up to the same minute: a fair race.
      ? q(`SELECT ${RAW} FROM hits WHERE ts >= ?1 AND ts < ?2`, yStart, yStart + elapsed)
      : q(`SELECT ${SUMS} FROM daily WHERE dim = 'total' AND day BETWEEN ?1 AND ?2`, s.prevFrom, s.prevTo),
    today
      ? q(`SELECT key, ${SUMS} FROM daily WHERE dim = 'hour' AND day = ?1 GROUP BY key`, s.today)
      : q(`SELECT day AS key, ${SUMS} FROM daily WHERE dim = 'total' AND day BETWEEN ?1 AND ?2 GROUP BY day`, s.from, s.to),
    today
      ? q(`SELECT key, ${SUMS} FROM daily WHERE dim = 'hour' AND day = ?1 GROUP BY key`, s.prevFrom)
      : q(`SELECT day AS key, ${SUMS} FROM daily WHERE dim = 'total' AND day BETWEEN ?1 AND ?2 GROUP BY day`, s.prevFrom, s.prevTo),
    q(`SELECT key, ${SUMS} FROM daily WHERE dim = 'hour' AND day BETWEEN ?1 AND ?2 GROUP BY key`, s.from, s.to),
    q(`SELECT a.*, p.title, p.desk, p.published FROM
         (SELECT key, ${SUMS} FROM daily WHERE dim = 'path' AND day BETWEEN ?1 AND ?2 GROUP BY key) a
       LEFT JOIN pages p ON p.path = a.key ORDER BY a.views DESC LIMIT 1500`, s.from, s.to),
    q(`SELECT key, ${SUMS} FROM daily WHERE dim = 'source' AND day BETWEEN ?1 AND ?2 GROUP BY key`, s.from, s.to),
    q(`SELECT key, ${SUMS} FROM daily WHERE dim = 'geo' AND day BETWEEN ?1 AND ?2 GROUP BY key`, s.from, s.to),
    q(`SELECT key, ${SUMS} FROM daily WHERE dim = 'tech' AND day BETWEEN ?1 AND ?2 GROUP BY key`, s.from, s.to),
    q(`SELECT MIN(day) AS day FROM daily WHERE dim = 'total'`),
    // Set only by scripts/seed-demo.mjs in a local database; the dashboard then
    // labels every figure as sample data.
    q(`SELECT v FROM meta WHERE k = 'demo'`),
  ]);

  const keys = today ? HOURS : daysBetween(s.from, s.to);
  const prevKeys = today ? HOURS : daysBetween(s.prevFrom, s.prevTo);

  const pages = paths.results.map((r) => ({
    path: r.key, title: r.title || null, desk: r.desk || null, published: r.published || null, ...numbers(r),
  }));
  const stories = pages.filter((p) => p.published);
  const desks = group(stories, 'desk', 'views', () => ({ stories: 0 }));
  for (const d of desks) d.stories = stories.filter((p) => p.desk === d.name).length;

  const src = split(sources.results, ['channel', 'ref', 'campaign']).filter((r) => r.channel !== 'Internal');
  const place = split(geo.results, ['country', 'city']);
  const kit = split(tech.results, ['device', 'browser', 'os']);
  const refChannel = new Map(src.map((r) => [r.ref, r.channel]));

  return {
    range: s.range, tz, from: s.from, to: s.to, prevFrom: s.prevFrom, prevTo: s.prevTo,
    today: s.today, generated: now, since: first.results[0]?.day || null, demo: demo.results.length > 0,
    totals: numbers(cur.results[0]),
    previous: numbers(prev.results[0]),
    series: fill(keys, series.results),
    previousSeries: fill(prevKeys, prevSeries.results),
    hours: fill(HOURS, hours.results),
    stories: stories.slice(0, 60),
    pages: pages.filter((p) => !p.published).slice(0, 20),
    desks,
    channels: group(src, 'channel', 'visits'),
    refs: group(src, 'ref', 'visits', (r) => ({ channel: refChannel.get(r.ref) })).slice(0, 25),
    campaigns: group(src, 'campaign', 'visits').slice(0, 15),
    countries: group(place, 'country').slice(0, 40),
    cities: group(place.map((r) => ({ ...r, place: r.city ? `${r.city}|${r.country}` : '' })), 'place')
      .slice(0, 25).map(({ name, ...r }) => ({ ...r, name: name.split('|')[0], country: name.split('|')[1] })),
    devices: group(kit, 'device'),
    browsers: group(kit, 'browser').slice(0, 12),
    os: group(kit, 'os').slice(0, 10),
  };
}

export async function story(env, url, now = Date.now()) {
  const path = String(url.searchParams.get('path') || '').slice(0, 200);
  const range = RANGES[url.searchParams.get('range')] ? url.searchParams.get('range') : '30d';
  const tz = timezone(env);
  const s = span(range, tz, now);
  const [start] = dayBounds(s.from, tz);
  const end = range === 'today' ? Math.floor(now / 1000) + 60 : dayBounds(s.to, tz)[1];
  const db = env.DB;
  const q = (sql, ...args) => db.prepare(sql).bind(path, start, end, ...args);
  const where = 'path = ?1 AND ts >= ?2 AND ts < ?3';
  const bucket = range === 'today' ? "printf('%02d', hour)" : 'day';

  const [page, totals, series, sources, internal, countries, devices] = await db.batch([
    db.prepare('SELECT title, desk, published FROM pages WHERE path = ?1').bind(path),
    q(`SELECT ${RAW}, SUM(engaged > 0 OR depth > 0) AS reported,
         SUM(depth >= 25) AS d25, SUM(depth >= 50) AS d50, SUM(depth >= 75) AS d75, SUM(depth >= 90) AS d90
       FROM hits WHERE ${where}`),
    q(`SELECT ${bucket} AS key, ${RAW} FROM hits WHERE ${where} GROUP BY 1`),
    q(`SELECT channel, COALESCE(ref, '') AS ref, COUNT(*) AS views, SUM(entry) AS visits
       FROM hits WHERE ${where} AND channel != 'Internal' GROUP BY channel, ref ORDER BY visits DESC, views DESC LIMIT 20`),
    q(`SELECT COUNT(*) AS views FROM hits WHERE ${where} AND channel = 'Internal'`),
    q(`SELECT country AS name, COUNT(*) AS views FROM hits WHERE ${where} AND country IS NOT NULL
       GROUP BY country ORDER BY views DESC LIMIT 10`),
    q(`SELECT device AS name, COUNT(*) AS views FROM hits WHERE ${where} GROUP BY device ORDER BY views DESC`),
  ]);

  const t = totals.results[0] || {};
  return {
    path, range, from: s.from, to: s.to, ...(page.results[0] || {}),
    totals: numbers(t),
    depth: {
      reported: Number(t.reported) || 0,
      steps: [25, 50, 75, 90].map((p) => ({ at: p, views: Number(t[`d${p}`]) || 0 })),
    },
    series: fill(range === 'today' ? HOURS : daysBetween(s.from, s.to), series.results),
    channels: group(sources.results.map((r) => ({ ...r, ...numbers(r) })), 'channel', 'visits'),
    refs: sources.results.filter((r) => r.ref).slice(0, 8)
      .map((r) => ({ name: r.ref, channel: r.channel, visits: Number(r.visits) || 0, views: Number(r.views) || 0 })),
    fromOtherPages: Number(internal.results[0]?.views) || 0,
    countries: countries.results.map((r) => ({ name: r.name, views: Number(r.views) || 0 })),
    devices: devices.results.map((r) => ({ name: r.name, views: Number(r.views) || 0 })),
  };
}

export async function live(env, now = Date.now()) {
  const t = Math.floor(now / 1000);
  const q = (sql, ...args) => env.DB.prepare(sql).bind(...args);
  const [recent, pages, minutes] = await env.DB.batch([
    q('SELECT COUNT(DISTINCT visitor) AS readers, COUNT(*) AS views FROM hits WHERE ts > ?1', t - 1800),
    q(`SELECT path, MAX(title) AS title, COUNT(DISTINCT visitor) AS readers FROM hits WHERE ts > ?1
       GROUP BY path ORDER BY readers DESC, path LIMIT 6`, t - 1800),
    // D1 binds JavaScript numbers as REAL, so make the minute an integer in SQL.
    q('SELECT CAST((?2 - ts) / 60 AS INTEGER) AS ago, COUNT(*) AS views FROM hits WHERE ts > ?1 GROUP BY ago', t - 1800, t),
  ]);
  const perMinute = Array(30).fill(0);
  for (const r of minutes.results) {
    const ago = Number(r.ago);
    if (ago >= 0 && ago < 30) perMinute[29 - ago] = Number(r.views) || 0;
  }
  return {
    now,
    readers: Number(recent.results[0]?.readers) || 0,
    views: Number(recent.results[0]?.views) || 0,
    pages: pages.results.map((r) => ({ path: r.path, title: r.title, readers: Number(r.readers) || 0 })),
    perMinute,
  };
}
