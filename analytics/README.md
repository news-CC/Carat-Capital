# The Circulation Desk

Carat Capital's own readership analytics: a cookieless counter on caratcapital.org,
a Cloudflare Worker that collects and rolls up the figures in a D1 database, and a
password-protected dashboard set in the paper's own type, paper and ink.

It runs alongside GoatCounter; nothing about GoatCounter changes.

## What the desk shows

- A headline written from the figures ("Readers up 12% to 4,810; Diamonds leads the desks")
- Readers, pageviews, visits, reading time and read-through, each against the previous period
- Readers, pageviews, visits, reading time or read-through by day (or by hour for today), against the previous period
- The front page: most-read stories with desk, filing date, reading time and read-through,
  downloadable as CSV; click a story for its own file: readers by day since filing,
  how far readers got, where they came from, countries and devices
- The desks, channels (search, social, AI assistants, newsletter, other sites, direct),
  referrers, campaigns (`utm_campaign`), countries, cities, hour of day (with the 06:00
  edition marked), devices, browsers and in-app browsers, systems, and the rest of the paper
- The wire: readers in the last 30 minutes and what they are reading, refreshed every 30 seconds
- Paper and Carbon (dark) editions, and a phone layout

## How it works

```
caratcapital.org page ── assets/circulation.js ──► POST /c ──► hits (D1)
                                                                  │  rolled up every 3 hours,
                                                                  ▼  and on demand
                   dashboard (public/) ◄── GET /api/* ◄──────── daily (D1)
```

| Path | Job |
| --- | --- |
| `../assets/circulation.js` | The tracker. Sends one beacon per pageview and one when the reader leaves (seconds read, depth reached). |
| `src/ingest.js` | `POST /c`: drops bots and foreign sites, classifies the source, hashes the visitor, stores the pageview. |
| `src/rollup.js` | Folds each day into `daily` (by page, source, place, device, hour). Hourly cron plus on-demand refresh. |
| `src/stats.js` | The dashboard's read API: overview, story file, live wire. |
| `src/auth.js` | One shared password, signed HttpOnly session cookie for 30 days. |
| `public/` | The dashboard: plain HTML, CSS and JavaScript, no framework. |
| `migrations/` | The D1 schema. |

### Privacy

No cookies on caratcapital.org and nothing stored on the reader's device. The collector
keeps no IP addresses: a reader is a SHA-256 hash of (the day's random salt, IP address,
browser), and each salt is deleted after two days, so a reader counts once a day and
cannot be followed from one day to the next. `privacy.html` carries a paragraph describing
the counter, shown automatically once the counter is switched on.

Staff can stop counting their own reading: open `https://caratcapital.org/?circulation=ignore`
once in each browser (`?circulation=count` undoes it).

## Going live

The D1 database `caratcapital-circulation` already exists in the Cloudflare account and
has its tables; `wrangler.toml` points at it. Three steps remain.

### 1. Deploy the Worker

**From GitHub (recommended).** The workflow `.github/workflows/circulation.yml` deploys on
every change to `analytics/` on `main`, and can be run by hand from the Actions tab. Add
these repository secrets (Settings → Secrets and variables → Actions):

| Secret | Value |
| --- | --- |
| `CLOUDFLARE_API_TOKEN` | A Cloudflare API token made from the **Edit Cloudflare Workers** template, with **Account → D1 → Edit** added |
| `CLOUDFLARE_ACCOUNT_ID` | Shown in the Cloudflare dashboard, on the Workers & Pages overview |
| `CIRCULATION_PASSWORD` | The password the desk will ask for (use a long one) |

Then run the workflow (Actions → Deploy the Circulation Desk → Run workflow). Until the
secrets exist the workflow only runs the tests, so it never turns `main` red.

**From a computer**, if you prefer:

```sh
cd analytics
npm ci
npx wrangler login
npm run deploy                                # applies migrations, then deploys
npx wrangler secret put DASHBOARD_PASSWORD    # prompts for the password
```

### 2. Open the desk

The deploy prints the Worker's address, `https://caratcapital-circulation.<your-subdomain>.workers.dev`
(also shown on the Worker's page in the Cloudflare dashboard). Open it and sign in.

### 3. Switch the counter on

In `build.py`, set `ANALYTICS_ENDPOINT` to that address and move the effective date on
`privacy.html` to the switch-on date. On the next site build, every page that carries
GoatCounter also carries the tracker, and the privacy paragraph appears. Setting it back
to `""` removes both again.

## Limits and costs

Everything fits Cloudflare's free plan at trade-paper scale. Each pageview costs about four
D1 row writes; the free plan allows 100,000 row writes a day **across the whole account**,
so roughly 25,000 pageviews a day. Past that, D1 refuses writes until midnight UTC (the
dashboard says so). The Workers Paid plan ($5 a month) lifts the ceiling to 50 million
writes a month. Raw pageviews are kept for 400 days (`RETENTION_DAYS`); the daily
roll-ups are kept for good.

## Reading the figures without the dashboard

The data is ordinary SQL in D1, so it can be queried from the Cloudflare dashboard, with
`npx wrangler d1 execute DB --remote --command "…"`, or by Claude through the Cloudflare
connector. Two examples:

```sql
-- Most-read stories over the last seven days
SELECT d.key AS path, p.title, SUM(d.readers) AS readers, SUM(d.views) AS views
FROM daily d LEFT JOIN pages p ON p.path = d.key
WHERE d.dim = 'path' AND d.day >= date('now', '-7 days') AND p.published IS NOT NULL
GROUP BY d.key ORDER BY readers DESC LIMIT 10;

-- Visits by channel this month
SELECT substr(key, 1, instr(key, '|') - 1) AS channel, SUM(visits) AS visits
FROM daily WHERE dim = 'source' AND day >= date('now', 'start of month') AND key NOT LIKE 'Internal|%'
GROUP BY channel ORDER BY visits DESC;
```

## Working on it locally

```sh
cd analytics
npm install
printf 'DASHBOARD_PASSWORD=local\nSITE_HOSTS=caratcapital.org,localhost,127.0.0.1\n' > .dev.vars
npm run db:local       # create the local database
npm run demo           # optional: generated sample traffic, clearly labelled as such
npm run dev            # http://localhost:8787, password "local"
npm test
```

`npm run demo` fills only the local database, over the paper's real stories and desks,
and the dashboard shows a "Demo figures" banner while that data is present.
`npm run demo -- --clear` removes it.
