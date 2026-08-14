#!/usr/bin/env node
/**
 * Prints supabase/migrations/0002_dial_scheduler.sql with __CRON_SECRET__ substituted,
 * ready to paste into the Supabase SQL Editor.
 *
 * The committed .sql keeps the placeholder on purpose — the real CRON_SECRET authorizes
 * outbound calls and must never land in git.
 *
 *   node --env-file=.env.local scripts/setup-scheduler.mjs            # print to stdout
 *   node --env-file=.env.local scripts/setup-scheduler.mjs --out FILE # write to a file
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const sqlPath = path.join(root, 'supabase/migrations/0002_dial_scheduler.sql');

const secret = process.env.CRON_SECRET;
if (!secret) {
  console.error('CRON_SECRET is not set. Run with: node --env-file=.env.local scripts/setup-scheduler.mjs');
  process.exit(1);
}

const appUrl = (process.env.NEXT_PUBLIC_APP_URL || 'https://www.startup25.com').replace(/\/+$/, '');

let sql = fs.readFileSync(sqlPath, 'utf8').replaceAll('__CRON_SECRET__', secret);

// Keep the endpoint in step with wherever the app actually lives.
sql = sql.replace(
  /url\s*:=\s*'[^']*\/api\/cron\/dial'/,
  `url     := '${appUrl}/api/cron/dial'`,
);

const outIdx = process.argv.indexOf('--out');
if (outIdx !== -1 && process.argv[outIdx + 1]) {
  const out = process.argv[outIdx + 1];
  fs.writeFileSync(out, sql, { mode: 0o600 });
  console.error(`Wrote ${out} (contains a live secret — do not commit it).`);
  console.error(`Paste it into the Supabase SQL Editor, then verify with:`);
  console.error(`  select jobname, schedule, active from cron.job;`);
} else {
  process.stdout.write(sql);
}
