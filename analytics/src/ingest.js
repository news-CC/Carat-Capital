// POST /c: the tracker on caratcapital.org reports here. Two kinds of beacon:
//   {t:'v', ...}          a pageview
//   {t:'e', id, s, d}     reading time (seconds) and depth (percent) for that pageview
// Beacons are text/plain so the browser sends them without a CORS preflight.

import { dayOf, addDays, wallClock } from './time.js';
import { isBot, parseUA } from './ua.js';
import { channelOf, normalizeHost, normalizeSource, referrerHost } from './sources.js';
import { hex, siteHosts, timezone } from './http.js';

// article:section on the page, as the site prints it → desk slug.
const DESKS = {
  'diamonds': 'diamonds',
  'gold & metals': 'gold-metals',
  'colored gemstones': 'gemstones',
  'gemstones': 'gemstones',
  'watches': 'watches',
  'auctions & estates': 'auctions',
  'auctions': 'auctions',
  'retail & technology': 'retail-tech',
  'retail & tech': 'retail-tech',
};

const clip = (s, n) => String(s ?? '').replace(/\s+/g, ' ').trim().slice(0, n);

const intIn = (v, lo, hi) => {
  const n = Math.round(Number(v));
  return Number.isFinite(n) ? Math.min(hi, Math.max(lo, n)) : lo;
};

const pageviewId = (v) => {
  const n = Number(v);
  return Number.isSafeInteger(n) && n > 0 ? n : 0;
};

/** /a-story.html, /a-story/ and /a-story are one page; so are / and /index.html. */
export function normalizePath(pathname) {
  let p = String(pathname || '/').replace(/\/{2,}/g, '/');
  p = p.replace(/\/index\.html?$/i, '/').replace(/\.html?$/i, '');
  if (p.length > 1) p = p.replace(/\/+$/, '');
  return p.slice(0, 200) || '/';
}

const cleanTitle = (t) => clip(String(t || '').replace(/\s+[—|–-]\s+Carat\s*Capital\s*$/i, ''), 200) || null;

/**
 * Turn a pageview beacon into a row for `hits`, or null if it is not ours.
 * Pure apart from the clock, so the tests can drive it directly.
 */
export function readHit(body, { ua, cf = {}, hosts, tz, now = Date.now() }) {
  const id = pageviewId(body.id);
  if (!id) return null;
  let page;
  try { page = new URL(String(body.u || '')); } catch { return null; }
  if (!hosts.has(page.hostname.toLowerCase())) return null;

  const params = page.searchParams;
  const source = normalizeSource(params.get('utm_source') || params.get('ref'));
  const medium = clip(params.get('utm_medium'), 40).toLowerCase();
  const campaign = clip(params.get('utm_campaign'), 80).replace(/\|/g, '/') || null;

  const rawRef = referrerHost(body.r);
  const internal = !!rawRef && hosts.has(rawRef.toLowerCase());
  const host = internal ? '' : normalizeHost(rawRef);
  const channel = channelOf({ host, internal, medium, source });

  // A visit starts with anything but a reload, a back/forward step or a click
  // from another page of the paper.
  const nav = String(body.n || 'navigate');
  const entry = !internal && nav !== 'reload' && nav !== 'back_forward' ? 1 : 0;

  const published = /^(\d{4}-\d{2}-\d{2})/.exec(String(body.pu || ''))?.[1] || null;
  const desk = published ? DESKS[clip(body.se, 40).toLowerCase()] || null : null;
  const { device, browser, os } = parseUA(ua, intIn(body.tp, 0, 20));
  const clock = wallClock(now, tz);

  return {
    id,
    ts: Math.floor(now / 1000),
    day: dayOf(now, tz),
    hour: clock.h,
    path: normalizePath(page.pathname),
    title: cleanTitle(body.ti),
    desk,
    published,
    entry,
    channel,
    ref: host || source || null,
    utm_campaign: campaign,
    country: /^[A-Z0-9]{2}$/.test(cf.country || '') ? cf.country : null,
    city: clip(cf.city, 60) || null,
    device,
    browser,
    os,
  };
}

// One salt per day, cached per isolate. Old salts are deleted as new ones
// arrive, which is what makes yesterday's visitor hashes unrecoverable.
let salted = { day: '', salt: '' };

async function saltFor(env, day) {
  if (salted.day === day) return salted.salt;
  const read = () => env.DB.prepare('SELECT salt FROM salts WHERE day = ?1').bind(day).first('salt');
  let salt = await read();
  if (!salt) {
    await env.DB.batch([
      env.DB.prepare('INSERT OR IGNORE INTO salts (day, salt) VALUES (?1, ?2)')
        .bind(day, hex(crypto.getRandomValues(new Uint8Array(16)))),
      env.DB.prepare('DELETE FROM salts WHERE day < ?1').bind(addDays(day, -1)),
    ]);
    salt = await read(); // another isolate may have won the race; everyone uses its salt
  }
  salted = { day, salt };
  return salt;
}

async function visitorOf(salt, ip, ua) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(`${salt}|${ip}|${ua}`));
  return hex(new Uint8Array(digest).slice(0, 8));
}

async function record(env, hit, ip, ua) {
  hit.visitor = await visitorOf(await saltFor(env, hit.day), ip, ua);
  await env.DB.prepare(
    `INSERT OR IGNORE INTO hits (id, ts, day, hour, path, title, desk, published, visitor, entry,
       channel, ref, utm_campaign, country, city, device, browser, os)
     VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16, ?17, ?18)`,
  ).bind(hit.id, hit.ts, hit.day, hit.hour, hit.path, hit.title, hit.desk, hit.published,
    hit.visitor, hit.entry, hit.channel, hit.ref, hit.utm_campaign, hit.country, hit.city,
    hit.device, hit.browser, hit.os).run();
}

async function engage(env, body, now = Date.now()) {
  const id = pageviewId(body.id);
  const seconds = intIn(body.s, 0, 3600);
  const depth = intIn(body.d, 0, 100);
  if (!id || (!seconds && !depth)) return;
  // Only recent pageviews, and only when something grew: a no-op is not a write.
  await env.DB.prepare(
    `UPDATE hits SET engaged = MAX(engaged, ?1), depth = MAX(depth, ?2)
     WHERE id = ?3 AND ts > ?4 AND (engaged < ?1 OR depth < ?2)`,
  ).bind(seconds, depth, id, Math.floor(now / 1000) - 6 * 3600).run();
}

function corsHeaders(origin, hosts) {
  const h = {
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
    Vary: 'Origin',
  };
  try {
    if (origin && hosts.has(new URL(origin).hostname.toLowerCase())) h['Access-Control-Allow-Origin'] = origin;
  } catch { /* a malformed Origin gets no CORS grant */ }
  return h;
}

export async function collect(request, env, ctx) {
  const hosts = siteHosts(env);
  const origin = request.headers.get('Origin') || '';
  const headers = corsHeaders(origin, hosts);
  const done = (status = 204) => new Response(null, { status, headers });

  if (request.method === 'OPTIONS') return done();
  if (request.method !== 'POST') return done(405);
  if (!headers['Access-Control-Allow-Origin'] && origin) return done(); // not our pages: quietly ignore

  const ip = request.headers.get('CF-Connecting-IP') || '';
  if (env.HITS) {
    const { success } = await env.HITS.limit({ key: ip || 'unknown' });
    if (!success) return done(429);
  }

  let body;
  try {
    const text = await request.text();
    if (text.length > 4096) return done(413);
    body = JSON.parse(text);
  } catch {
    return done(400);
  }
  const ua = request.headers.get('User-Agent') || '';
  if (!body || typeof body !== 'object' || isBot(ua)) return done();

  const safely = (p) => ctx.waitUntil(p.catch((e) => console.error('circulation write failed:', e.message)));
  if (body.t === 'e') {
    safely(engage(env, body));
    return done();
  }
  if (body.t !== 'v') return done(400);
  const hit = readHit(body, { ua, cf: request.cf || {}, hosts, tz: timezone(env) });
  if (hit) safely(record(env, hit, ip, ua));
  return done();
}
