// Unit tests for the pure parts of the Circulation Desk. Run: npm test
import test from 'node:test';
import assert from 'node:assert/strict';

import { addDays, dayBounds, dayOf, startOfDay, wallClock } from '../src/time.js';
import { isBot, parseUA } from '../src/ua.js';
import { channelOf, normalizeHost, normalizeSource, referrerHost } from '../src/sources.js';
import { normalizePath, readHit } from '../src/ingest.js';
import { span } from '../src/stats.js';

const NY = 'America/New_York';
const IPHONE_IG = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 390.0.0.0';
const MAC_SAFARI = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15';
const WIN_EDGE = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0';
const ANDROID_TABLET = 'Mozilla/5.0 (Linux; Android 14; SM-X710) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36';

test('days follow New York time, not UTC', () => {
  // 01:30 UTC on 26 September is still 25 September in New York.
  const ms = Date.UTC(2026, 8, 26, 1, 30);
  assert.equal(dayOf(ms, NY), '2026-09-25');
  assert.equal(wallClock(ms, NY).h, 21);
  assert.equal(dayOf(ms, 'UTC'), '2026-09-26');
});

test('day bounds survive daylight-saving changes', () => {
  // Spring forward: 8 March 2026 lasts 23 hours in New York; fall back: 1 November lasts 25.
  const [a, b] = dayBounds('2026-03-08', NY);
  assert.equal(b - a, 23 * 3600);
  const [c, d] = dayBounds('2026-11-01', NY);
  assert.equal(d - c, 25 * 3600);
  assert.equal(new Date(startOfDay('2026-07-04', NY)).toISOString(), '2026-07-04T04:00:00.000Z');
  assert.equal(new Date(startOfDay('2026-12-25', NY)).toISOString(), '2026-12-25T05:00:00.000Z');
});

test('calendar arithmetic crosses months and years', () => {
  assert.equal(addDays('2026-09-30', 1), '2026-10-01');
  assert.equal(addDays('2026-01-01', -1), '2025-12-31');
  assert.equal(addDays('2028-02-28', 1), '2028-02-29');
});

test('crawlers and scripts are not readers; phones named Cubot are', () => {
  for (const ua of [
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/140.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome-Lighthouse',
    'curl/8.5.0', 'python-requests/2.32', 'facebookexternalhit/1.1', 'GPTBot/1.2', '',
  ]) assert.equal(isBot(ua), true, ua);
  for (const ua of [IPHONE_IG, MAC_SAFARI, WIN_EDGE, 'Mozilla/5.0 (Linux; Android 11; CUBOT X30) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36']) {
    assert.equal(isBot(ua), false, ua);
  }
});

test('devices, browsers and systems', () => {
  assert.deepEqual(parseUA(IPHONE_IG), { device: 'Mobile', os: 'iOS', browser: 'Instagram app' });
  assert.deepEqual(parseUA(MAC_SAFARI), { device: 'Desktop', os: 'macOS', browser: 'Safari' });
  assert.deepEqual(parseUA(MAC_SAFARI, 5), { device: 'Tablet', os: 'iPadOS', browser: 'Safari' }); // iPad in desktop mode
  assert.deepEqual(parseUA(WIN_EDGE), { device: 'Desktop', os: 'Windows', browser: 'Edge' });
  assert.deepEqual(parseUA(ANDROID_TABLET), { device: 'Tablet', os: 'Android', browser: 'Chrome' });
});

test('one name per network', () => {
  assert.equal(normalizeHost('www.google.co.uk'), 'google.com');
  assert.equal(normalizeHost('news.google.com'), 'news.google.com');
  assert.equal(normalizeHost('l.instagram.com'), 'instagram.com');
  assert.equal(normalizeHost('lm.facebook.com'), 'facebook.com');
  assert.equal(normalizeHost('t.co'), 'x.com');
  assert.equal(normalizeHost('lnkd.in'), 'linkedin.com');
  assert.equal(normalizeHost('chat.openai.com'), 'chatgpt.com');
  assert.equal(normalizeSource('IG'), 'instagram.com');
  assert.equal(normalizeSource('chatgpt.com'), 'chatgpt.com');
  assert.equal(normalizeSource('morning-brief'), 'morning-brief');
  assert.equal(referrerHost('android-app://com.google.android.googlequicksearchbox/'), 'discover.google.com');
  assert.equal(referrerHost('https://www.rapaport.com/news/x'), 'www.rapaport.com');
  assert.equal(referrerHost('javascript:alert(1)'), '');
});

test('channels', () => {
  const c = (o) => channelOf({ host: '', internal: false, ...o });
  assert.equal(c({ host: 'google.com' }), 'Search');
  assert.equal(c({ host: 'instagram.com' }), 'Social');
  assert.equal(c({ host: 'chatgpt.com' }), 'AI');
  assert.equal(c({ source: 'chatgpt.com' }), 'AI'); // ChatGPT tags links with utm_source=chatgpt.com
  assert.equal(c({ host: 'mail.google.com' }), 'Email');
  assert.equal(c({ medium: 'email' }), 'Email');
  assert.equal(c({ source: 'newsletter' }), 'Email');
  assert.equal(c({ medium: 'social' }), 'Social');
  assert.equal(c({ medium: 'cpc', host: 'google.com' }), 'Paid');
  assert.equal(c({ host: 'www.rapaport.com' }), 'Referral');
  assert.equal(c({}), 'Direct');
  assert.equal(c({ internal: true }), 'Internal');
});

test('paths: .html, trailing slashes and index all fold together', () => {
  assert.equal(normalizePath('/a-gold-sheds.html'), '/a-gold-sheds');
  assert.equal(normalizePath('/a-gold-sheds/'), '/a-gold-sheds');
  assert.equal(normalizePath('/index.html'), '/');
  assert.equal(normalizePath('//diamonds'), '/diamonds');
  assert.equal(normalizePath(''), '/');
});

const hosts = new Set(['caratcapital.org', 'www.caratcapital.org']);
const beacon = (over = {}) => ({
  t: 'v', id: 4242, n: 'navigate',
  u: 'https://caratcapital.org/a-sixty-one-sixty-off-gold?utm_source=ig&utm_medium=social&utm_campaign=sept|carousel',
  r: 'https://l.instagram.com/', ti: 'Gold sheds $61.60 — Carat Capital', se: 'Gold & Metals',
  pu: '2026-09-24T06:30:00-04:00', tp: 5, ...over,
});

test('a pageview beacon becomes a row', () => {
  const now = Date.UTC(2026, 8, 26, 1, 30);
  const hit = readHit(beacon(), { ua: IPHONE_IG, cf: { country: 'BE', city: 'Antwerp' }, hosts, tz: NY, now });
  assert.equal(hit.path, '/a-sixty-one-sixty-off-gold');
  assert.equal(hit.title, 'Gold sheds $61.60');
  assert.equal(hit.desk, 'gold-metals');
  assert.equal(hit.published, '2026-09-24');
  assert.equal(hit.channel, 'Social');
  assert.equal(hit.ref, 'instagram.com');
  assert.equal(hit.utm_campaign, 'sept/carousel'); // '|' is the roll-up key separator
  assert.equal(hit.entry, 1);
  assert.equal(hit.day, '2026-09-25');
  assert.equal(hit.hour, 21);
  assert.equal(hit.country, 'BE');
  assert.equal(hit.city, 'Antwerp');
  assert.equal(hit.device, 'Mobile');
});

test('clicks between our pages, reloads and back steps are not new visits', () => {
  const opts = { ua: MAC_SAFARI, hosts, tz: NY };
  const inside = readHit(beacon({ r: 'https://caratcapital.org/', u: 'https://caratcapital.org/diamonds' }), opts);
  assert.equal(inside.channel, 'Internal');
  assert.equal(inside.entry, 0);
  assert.equal(inside.ref, null);
  assert.equal(readHit(beacon({ n: 'reload' }), opts).entry, 0);
  assert.equal(readHit(beacon({ n: 'back_forward' }), opts).entry, 0);
  const direct = readHit(beacon({ r: '', u: 'https://caratcapital.org/' }), opts);
  assert.equal(direct.channel, 'Direct');
  assert.equal(direct.entry, 1);
});

test('beacons from other sites or without an id are ignored', () => {
  const opts = { ua: MAC_SAFARI, hosts, tz: NY };
  assert.equal(readHit(beacon({ u: 'https://copycat.example/a-story' }), opts), null);
  assert.equal(readHit(beacon({ id: 'x' }), opts), null);
  assert.equal(readHit(beacon({ id: -3 }), opts), null);
  assert.equal(readHit(beacon({ u: 'not a url' }), opts), null);
  // A desk only belongs to a dated story.
  assert.equal(readHit(beacon({ pu: '' }), opts).desk, null);
});

test('ranges: whole days ending yesterday, compared with the same length before', () => {
  const now = Date.UTC(2026, 8, 26, 14); // 10:00 in New York on 26 September
  assert.deepEqual(span('7d', NY, now), { range: '7d', today: '2026-09-26', from: '2026-09-19', to: '2026-09-25', prevFrom: '2026-09-12', prevTo: '2026-09-18' });
  const today = span('today', NY, now);
  assert.equal(today.from, '2026-09-26');
  assert.equal(today.prevFrom, '2026-09-25');
  const year = span('12m', NY, now);
  assert.equal(year.from, '2025-09-26');
  assert.equal(year.to, '2026-09-25');
});
