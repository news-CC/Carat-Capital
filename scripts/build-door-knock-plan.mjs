/**
 * Build the door-knock plan: 621 named salons/spas in Hoboken + Manhattan, grouped into walkable
 * clusters and sequenced across Aug 19-27.
 *
 * Optimised for signups, which in a foot campaign means minimising walking between conversations
 * and maximising the number of doors where you already have a warm opener. So:
 *  - clustered by neighbourhood, then ordered south-to-north within a cluster
 *  - anyone already emailed is flagged FIRST in their cluster, because "I sent you a note Monday"
 *    outperforms a cold open by a wide margin
 *  - a phone number on the row means you can demo on the spot without asking for theirs
 */
import fs from 'node:fs';

const SP = '/tmp/claude-1000/-home-msd-ai-workspace-salon-man/e719906e-4515-4ce7-ae8f-69b098289863/scratchpad';
const els = JSON.parse(fs.readFileSync(`${SP}/walk.json`, 'utf8')).elements;

// Who already has an email from us, straight from the campaign table — authoritative about what
// actually SENT, rather than what we merely intended to send. 'sent' is a warm door today;
// 'queued' becomes one over the next few days, so it is worth distinguishing.
const emailed = new Map();
const queued = new Map();
for (const r of JSON.parse(fs.readFileSync(`${SP}/emailed.json`, 'utf8'))) {
  const key = (r.name || '').toLowerCase().trim();
  if (!key) continue;
  (r.status === 'sent' ? emailed : queued).set(key, r.email);
}

const CLUSTERS = [
  { key: 'Hoboken', lat: [40.735, 40.760], lon: [-74.045, -74.020] },
  { key: 'Lower Manhattan / FiDi & Tribeca', lat: [40.700, 40.722], lon: [-74.020, -73.995] },
  { key: 'SoHo / NoLita / LES', lat: [40.715, 40.729], lon: [-74.010, -73.980] },
  { key: 'West Village / Chelsea', lat: [40.729, 40.752], lon: [-74.014, -73.992] },
  { key: 'East Village / Gramercy', lat: [40.722, 40.742], lon: [-73.995, -73.972] },
  { key: 'Midtown', lat: [40.742, 40.765], lon: [-74.000, -73.968] },
  { key: 'Upper East Side', lat: [40.760, 40.790], lon: [-73.975, -73.940] },
  { key: 'Upper West Side', lat: [40.765, 40.800], lon: [-74.000, -73.960] },
];

const clusterFor = (lat, lon) =>
  CLUSTERS.find((c) => lat >= c.lat[0] && lat <= c.lat[1] && lon >= c.lon[0] && lon <= c.lon[1])?.key ??
  'Other';

const fmtPhone = (p) => {
  const d = String(p || '').replace(/\D/g, '');
  const ten = d.length === 11 && d[0] === '1' ? d.slice(1) : d;
  return ten.length === 10 ? `(${ten.slice(0, 3)}) ${ten.slice(3, 6)}-${ten.slice(6)}` : (p || '');
};

const rows = [];
for (const e of els) {
  const t = e.tags || {};
  const name = (t.name || '').trim();
  if (!name) continue;
  const lat = e.lat ?? e.center?.lat;
  const lon = e.lon ?? e.center?.lon;
  if (lat == null || lon == null) continue;

  const kind =
    t.amenity === 'spa' || t.leisure === 'spa' ? 'spa'
    : t.shop === 'beauty' ? 'beauty'
    : 'hair';

  const street = [t['addr:housenumber'], t['addr:street']].filter(Boolean).join(' ');
  rows.push({
    name,
    kind,
    cluster: clusterFor(lat, lon),
    street,
    phone: fmtPhone(t.phone || t['contact:phone']),
    website: (t.website || t['contact:website'] || '').replace(/^https?:\/\//, '').replace(/\/$/, ''),
    emailedAt: emailed.get(name.toLowerCase().trim()) || '',
    queuedAt: queued.get(name.toLowerCase().trim()) || '',
    lat,
    lon,
  });
}

// De-dupe by name WITHIN a cluster, keeping the richest row.
//
// Keying on name+street let the same salon appear twice — once with an address and once without,
// because OSM often carries both a node and a building way for one business. On a walking list a
// duplicate is a wasted trip.
const richness = (r) => (r.street ? 2 : 0) + (r.phone ? 1 : 0) + (r.website ? 1 : 0);
const best = new Map();
for (const r of rows) {
  const k = `${r.cluster}|${r.name.toLowerCase()}`;
  const cur = best.get(k);
  if (!cur || richness(r) > richness(cur)) best.set(k, r);
}
const unique = [...best.values()];

/**
 * Ranking, in the order that actually matters on foot:
 *  1. An ADDRESS. Without one there is no door to knock on, however warm the lead — these sink to
 *     the bottom and are worth a phone call instead.
 *  2. Already emailed, then queued. "I sent you a note Monday" is the best opener available.
 *  3. A phone number, so a demo can be placed without asking for theirs.
 */
const score = (r) =>
  (r.street ? 0 : 1000) + (r.emailedAt ? 0 : r.queuedAt ? 10 : 20) + (r.phone ? 0 : 1);

const byCluster = new Map();
for (const r of unique) {
  if (!byCluster.has(r.cluster)) byCluster.set(r.cluster, []);
  byCluster.get(r.cluster).push(r);
}
for (const list of byCluster.values()) {
  list.sort((a, b) => score(a) - score(b) || a.lat - b.lat || a.name.localeCompare(b.name));
}

// Wed 19 Aug 2026 .. Thu 27 Aug 2026. Hoboken first (home turf, walkable, least travel).
const DAYS = [
  ['Wed 19 Aug', ['Hoboken']],
  ['Thu 20 Aug', ['SoHo / NoLita / LES']],
  ['Fri 21 Aug', ['West Village / Chelsea']],
  ['Sat 22 Aug', ['Upper East Side']],
  ['Sun 23 Aug', ['Upper West Side']],
  ['Mon 24 Aug', ['Midtown']],
  ['Tue 25 Aug', ['East Village / Gramercy']],
  ['Wed 26 Aug', ['Lower Manhattan / FiDi & Tribeca']],
  ['Thu 27 Aug', ['Other']],
];

const CAP = 18; // realistic doors per day when each stop can turn into a 15-minute demo

let md = `# Salon Malone — door-knock plan, 19–27 Aug 2026

**${unique.length} salons, spas and barbershops** across Hoboken and Manhattan, clustered so each day
is walkable and sequenced south-to-north within a cluster.

## How to use a stop

1. Ask who books the appointments. Only that person can say yes.
2. One sentence: *"You've got a few hundred clients who quietly stopped coming in. I've got something that phones them and books them back. Want to hear it call you right now?"*
3. Open **startup25.com/admin/demo** on your phone. Their salon name, their offer, their number. **Call now.**
4. Hand them the phone.
5. Close on the **$299 pilot** — 350 calls on their own list. Card at [startup25.com](https://www.startup25.com/#pricing) or send them to /start.

**⚑ = already has your email** (sent 17 Aug). **◷ = email queued**, going out over the next few days. Open with that: *"I sent you a note Monday about your lapsed clients."* Warmest doors on the list — do them first.
**☎ = phone on file**, so you can demo without asking for their number.

Rows without an address are listed last in each day and are **phone-first** — OSM has the business
but not its street number. Ring those instead of hunting for the door.

Cost to you per demo call: about **8 cents**.

---

`;

let dayNo = 0;
for (const [label, keys] of DAYS) {
  const pool = keys.flatMap((k) => byCluster.get(k) ?? []);
  if (!pool.length) continue;
  dayNo += 1;
  const list = pool.slice(0, CAP);
  const warm = list.filter((r) => r.emailedAt).length;

  md += `## Day ${dayNo} — ${label} · ${keys.join(', ')}\n\n`;
  md += `${pool.length} in this cluster, top ${list.length} below. **${warm} already emailed.**\n\n`;
  md += `| | Salon | Type | Address | Phone | Site |\n|---|---|---|---|---|---|\n`;
  for (const r of list) {
    const flags = [r.emailedAt ? '⚑' : r.queuedAt ? '◷' : '', r.phone ? '☎' : ''].filter(Boolean).join(' ') || '·';
    md += `| ${flags} | ${r.name} | ${r.kind} | ${r.street || '—'} | ${r.phone || '—'} | ${r.website || '—'} |\n`;
  }
  if (pool.length > CAP) {
    md += `\n<details><summary>${pool.length - CAP} more in ${keys.join(', ')}</summary>\n\n`;
    for (const r of pool.slice(CAP)) {
      md += `- ${r.emailedAt ? '⚑ ' : ''}**${r.name}** · ${r.street || 'no address'} · ${r.phone || 'no phone'}\n`;
    }
    md += `\n</details>\n`;
  }
  md += `\n`;
}

const totalWarm = unique.filter((r) => r.emailedAt).length;
md += `---

## Totals

| | |
|---|---|
| Salons on the plan | ${unique.length} |
| Already emailed (⚑) | ${totalWarm} |\n| Email queued (◷) | ${unique.filter((r) => r.queuedAt).length} |
| Phone on file (☎) | ${unique.filter((r) => r.phone).length} |
| Days | ${dayNo} (19–27 Aug) |
| Doors/day cap | ${CAP} |

## Honest expectations

At ${CAP} doors a day you will speak to the decision-maker at maybe a third of them — the rest the
owner is out, or you get a stylist mid-colour. Of those conversations, a live demo is the thing that
converts; a leaflet is not. Six good demos a day is a strong day.

Cheapest close is the **$299 pilot**, not the $399/month. It is one decision, it is reversible in
their head, and it is credited against month one.

## Before you walk out

- [ ] Log in to startup25.com/admin on your phone and leave the tab open
- [ ] Test one demo call to yourself so the first one in front of an owner is not the first of the day
- [ ] Have the $299 checkout link open in a second tab
- [ ] Bring a charger

Data: OpenStreetMap (ODbL). Addresses and phones are as published there and can be stale — the
salon in front of you is the source of truth.
`;

fs.writeFileSync(`${SP}/DOOR-KNOCK-PLAN.md`, md);
console.log(`wrote DOOR-KNOCK-PLAN.md — ${unique.length} salons, ${totalWarm} already emailed, ${dayNo} days`);
for (const [k, v] of byCluster) console.log(`  ${k.padEnd(36)} ${v.length}`);
