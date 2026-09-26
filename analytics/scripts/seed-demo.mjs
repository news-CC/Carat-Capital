// Fill the LOCAL development database with generated sample traffic, so the
// dashboard can be previewed before the tracker has collected real figures.
//
//   npm run db:local && npm run demo         seed (resets local data first)
//   npm run demo -- --clear                  remove the sample data again
//
// It only ever touches the local database that `wrangler dev` uses, and it
// sets a flag that makes the dashboard label every figure as sample data.
// The traffic is invented; the story titles, desks and dates are the paper's
// real ones, taken from content/articles.json.

import { readFileSync } from 'node:fs';
import { getPlatformProxy } from 'wrangler';
import { rollupDay } from '../src/rollup.js';
import { addDays, dayOf, startOfDay } from '../src/time.js';

const TZ = 'America/New_York';
const clear = process.argv.includes('--clear');

// A seeded generator, so every preview shows the same sample.
let seed = 20260926;
const rand = () => {
  seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
const between = (a, b) => a + rand() * (b - a);
const normal = () => Math.sqrt(-2 * Math.log(rand() || 1e-9)) * Math.cos(2 * Math.PI * rand());
const pick = (weighted) => {
  const total = weighted.reduce((a, [, w]) => a + w, 0);
  let r = rand() * total;
  for (const [v, w] of weighted) if ((r -= w) <= 0) return v;
  return weighted[weighted.length - 1][0];
};
const hex = (n) => Array.from({ length: n }, () => Math.floor(rand() * 16).toString(16)).join('');

const { env, dispose } = await getPlatformProxy();
const db = env.DB;

await db.batch([
  db.prepare('DELETE FROM hits'), db.prepare('DELETE FROM daily'), db.prepare('DELETE FROM pages'),
  db.prepare('DELETE FROM salts'), db.prepare("DELETE FROM meta WHERE k != 'session_salt'"),
]);
if (clear) {
  console.log('Local sample data cleared.');
  await dispose();
  process.exit(0);
}

const articles = JSON.parse(readFileSync(new URL('../../content/articles.json', import.meta.url), 'utf8'));
const DESK_PULL = { diamonds: 1.25, 'gold-metals': 1.1, 'retail-tech': 0.9, watches: 1, auctions: 1, gemstones: 0.9 };
for (const a of articles) a.pull = Math.exp(normal() * 0.8) * (a.lead ? 2.4 : 1) * (DESK_PULL[a.desk] || 1);

const EVERGREEN = [
  ['/', 'Carat Capital — The Trade Paper of the Jewelry World', 16],
  ['/diamonds', 'Diamonds', 1.6], ['/gold-metals', 'Gold & Metals', 1.3], ['/gemstones', 'Colored Gemstones', 0.7],
  ['/watches', 'Watches', 0.8], ['/auctions', 'Auctions & Estates', 0.7], ['/retail-tech', 'Retail & Technology', 0.8],
  ['/natural-diamond-prices', 'Natural diamond prices', 2.6], ['/lab-grown-diamond-prices', 'Lab-grown diamond prices', 1.9],
  ['/indices', 'The Carat indices', 1.4], ['/the-record', 'The Record', 1.2], ['/field-guide', 'The Field Guide', 0.5],
  ['/about', 'About the paper', 0.4],
];

const CHANNELS = [
  ['Search', 33], ['Social', 21], ['Direct', 19], ['Email', 8], ['AI', 5.5], ['Referral', 5],
];
const REFS = {
  Search: [['google.com', 80], ['bing.com', 7], ['duckduckgo.com', 5], ['news.google.com', 6], ['discover.google.com', 2]],
  Social: [['instagram.com', 48], ['linkedin.com', 27], ['facebook.com', 10], ['x.com', 8], ['tiktok.com', 4], ['reddit.com', 3]],
  AI: [['chatgpt.com', 60], ['perplexity.ai', 24], ['gemini.google.com', 11], ['claude.ai', 5]],
  Email: [['newsletter', 62], ['mail.google.com', 38]],
  Referral: [['feedly.com', 50], ['flipboard.com', 30], ['inoreader.com', 20]],
};
const CAMPAIGNS = { 'instagram.com': [['ig-carousel', 55], ['ig-reel', 25], [null, 20]], 'linkedin.com': [['linkedin-post', 60], [null, 40]], newsletter: [['morning-brief', 100]] };

// [country, share, hours ahead of New York, cities]
const PLACES = [
  ['US', 36, 0, [['New York', 45], ['Los Angeles', 10], ['Miami', 7], ['Chicago', 6], ['Dallas', 5], ['Houston', 4], ['San Francisco', 4], ['Boston', 4]]],
  ['IN', 11, 9.5, [['Mumbai', 45], ['Surat', 30], ['Jaipur', 10], ['Delhi', 15]]],
  ['GB', 7, 5, [['London', 82], ['Birmingham', 18]]],
  ['AE', 6, 8, [['Dubai', 90], ['Abu Dhabi', 10]]],
  ['BE', 5, 6, [['Antwerp', 86], ['Brussels', 14]]],
  ['HK', 5, 12, [['Hong Kong', 100]]],
  ['IL', 3, 7, [['Ramat Gan', 62], ['Tel Aviv', 38]]],
  ['CH', 3, 6, [['Geneva', 60], ['Zurich', 40]]],
  ['CA', 3, 0, [['Toronto', 62], ['Vancouver', 38]]],
  ['IT', 2.5, 6, [['Milan', 50], ['Vicenza', 30], ['Arezzo', 20]]],
  ['DE', 2, 6, [['Berlin', 40], ['Munich', 30], ['Pforzheim', 30]]],
  ['FR', 2, 6, [['Paris', 100]]],
  ['TH', 2, 11, [['Bangkok', 100]]],
  ['SG', 2, 12, [['Singapore', 100]]],
  ['AU', 2, 14, [['Sydney', 60], ['Melbourne', 40]]],
  ['JP', 2, 13, [['Tokyo', 100]]],
  ['CN', 2, 12, [['Shenzhen', 50], ['Shanghai', 50]]],
  ['BW', 1, 6, [['Gaborone', 100]]],
  ['ZA', 1, 6, [['Johannesburg', 100]]],
  ['NL', 1, 6, [['Amsterdam', 100]]],
];
// When people read, in their own time: the morning read, lunch, the evening.
const LOCAL_HOURS = [0.3, 0.2, 0.1, 0.1, 0.1, 0.3, 1.2, 2.6, 3.2, 2.9, 2.3, 2, 2.2, 2.1, 1.9, 1.8, 1.7, 1.6, 1.4, 1.6, 1.9, 1.6, 1.1, 0.6];

function kit(channel, ref) {
  const social = channel === 'Social';
  const device = pick([['Mobile', social ? 82 : channel === 'Email' ? 44 : 55], ['Desktop', social ? 14 : channel === 'Email' ? 52 : 41], ['Tablet', 4]]);
  if (device === 'Tablet') return { device, os: 'iPadOS', browser: 'Safari' };
  if (device === 'Mobile') {
    const os = pick([['iOS', 58], ['Android', 42]]);
    if (ref === 'instagram.com' && rand() < 0.62) return { device, os, browser: 'Instagram app' };
    if (ref === 'linkedin.com' && rand() < 0.45) return { device, os, browser: 'LinkedIn app' };
    if (ref === 'facebook.com' && rand() < 0.55) return { device, os, browser: 'Facebook app' };
    if (ref === 'tiktok.com' && rand() < 0.8) return { device, os, browser: 'TikTok app' };
    if (os === 'iOS') return { device, os, browser: pick([['Safari', 78], ['Chrome', 14], ['Google app', 8]]) };
    return { device, os, browser: pick([['Chrome', 80], ['Samsung Internet', 16], ['Firefox', 4]]) };
  }
  const os = pick([['Windows', 52], ['macOS', 44], ['Linux', 2], ['ChromeOS', 2]]);
  if (os === 'macOS') return { device, os, browser: pick([['Safari', 44], ['Chrome', 50], ['Firefox', 6]]) };
  return { device, os, browser: pick([['Chrome', 66], ['Edge', 27], ['Firefox', 7]]) };
}

const now = Date.now();
const today = dayOf(now, TZ);
const first = articles.reduce((a, x) => (x.date < a ? x.date : a), today);
const lastDays = [];
for (let d = first; d <= today; d = addDays(d, 1)) lastDays.push(d);
const rows = [];

lastDays.forEach((day, index) => {
  const t = index / Math.max(1, lastDays.length - 1);
  const weekday = new Date(`${day}T12:00:00Z`).getUTCDay();
  const views = Math.round(950 * (2300 / 950) ** t * [0.58, 1.0, 1.08, 1.06, 1.02, 0.97, 0.62][weekday] * between(0.9, 1.1));
  const dayStart = startOfDay(day, TZ) / 1000;
  const cutoff = day === today ? Math.floor(now / 1000) : Infinity;

  const live = articles.filter((a) => a.date <= day);
  const weights = live.map((a) => {
    const age = (Date.parse(`${day}T00:00:00Z`) - Date.parse(`${a.date.slice(0, 10)}T00:00:00Z`)) / 86400000;
    return [a, a.pull * (0.5 ** (age / 1.3) + 0.018)];
  });
  const pages = [...weights.map(([a, w]) => [a, (w / weights.reduce((s, [, x]) => s + x, 0)) * 70]),
    ...EVERGREEN.map(([path, title, w]) => [{ path, title }, w])];

  let made = 0;
  const regulars = []; // readers who come back later the same day keep their device and place
  while (made < views) {
    const channel = pick(CHANNELS);
    const ref = REFS[channel] ? pick(REFS[channel]) : null;
    const campaign = CAMPAIGNS[ref] ? pick(CAMPAIGNS[ref]) : null;
    let reader;
    if (regulars.length > 20 && rand() < 0.2) {
      reader = regulars[Math.floor(rand() * regulars.length)];
    } else {
      const [country, , ahead, cities] = pick(PLACES.map((p) => [p, p[1]]));
      reader = { visitor: hex(16), country, ahead, city: pick(cities), ...kit(channel, ref) };
      regulars.push(reader);
    }
    const { visitor, country, ahead, city, device, browser, os } = reader;
    const local = pick(LOCAL_HOURS.map((w, h) => [h, w]));
    let ts = dayStart + ((((local - ahead) % 24) + 24) % 24) * 3600 + Math.floor(rand() * 3600);
    const length = 1 + Math.floor(-Math.log(rand() || 1e-9) * 0.9);
    for (let i = 0; i < length && made < views; i++) {
      if (ts >= cutoff || ts >= dayStart + 86400) break;
      const page = pick(pages);
      const story = page.slug ? page : null;
      const minutes = story?.minutes || 1;
      const reported = rand() < 0.92;
      const bounce = rand() < 0.12;
      const engaged = !reported ? 0 : Math.min(3600, Math.round(bounce ? between(3, 14) : minutes * 60 * Math.exp(normal() * 0.5) * 0.62));
      const depth = !reported ? 0 : story
        ? Math.min(100, Math.round(bounce ? between(8, 30) : (engaged / (minutes * 60)) * between(80, 125)))
        : Math.round(between(30, 100));
      rows.push({
        id: rows.length + 1, ts, day, hour: Math.floor((ts - dayStart) / 3600) % 24,
        path: story ? `/a-${story.slug}` : page.path, title: story ? story.title : page.title,
        desk: story?.desk || null, published: story ? story.date.slice(0, 10) : null, visitor,
        entry: i === 0 ? 1 : 0, channel: i === 0 ? channel : 'Internal',
        ref: i === 0 && ref ? ref : null, utm_campaign: i === 0 ? campaign : null,
        country, city, device, browser, os, engaged, depth,
      });
      made++;
      ts += Math.max(20, engaged) + Math.floor(between(5, 60));
    }
  }
});

const COLS = ['id', 'ts', 'day', 'hour', 'path', 'title', 'desk', 'published', 'visitor', 'entry', 'channel', 'ref', 'utm_campaign', 'country', 'city', 'device', 'browser', 'os', 'engaged', 'depth'];
const lit = (v) => (v == null ? 'NULL' : typeof v === 'number' ? String(v) : `'${String(v).replace(/'/g, "''")}'`);
const statements = [];
for (let i = 0; i < rows.length; i += 150) {
  const values = rows.slice(i, i + 150).map((r) => `(${COLS.map((c) => lit(r[c])).join(',')})`).join(',');
  statements.push(db.prepare(`INSERT INTO hits (${COLS.join(',')}) VALUES ${values}`));
}
for (let i = 0; i < statements.length; i += 40) await db.batch(statements.slice(i, i + 40));

for (const day of lastDays) await rollupDay(env, day, { final: day < today, now });
await db.prepare("INSERT OR REPLACE INTO meta (k, v) VALUES ('demo', '1')").run();

console.log(`Seeded ${rows.length.toLocaleString()} sample pageviews across ${lastDays.length} days (${first} to ${today}) in the LOCAL database.`);
console.log('The dashboard will label them as sample data. Run `npm run demo -- --clear` to remove them.');
await dispose();
