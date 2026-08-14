#!/usr/bin/env node
/**
 * Applies supabase/migrations/0001_init.sql — or rather, hands it to you to apply.
 *
 * There is deliberately no automation here. Supabase's REST endpoint (PostgREST) cannot execute DDL:
 * it exposes tables and RPCs, not `create table`. Every "run SQL over the API" trick needs a
 * pre-existing exec-sql function, which itself needs DDL to create. So the two real paths are the SQL
 * Editor in the dashboard, or psql against the pooler.
 *
 * The migration is written to be idempotent, so re-running it is safe.
 *
 * Usage:
 *   node scripts/apply-migration.mjs              # print the SQL + instructions
 *   node scripts/apply-migration.mjs --quiet      # print only the SQL (pipe it: | pbcopy, | xclip)
 *   node --env-file=.env.local scripts/apply-migration.mjs   # also resolves SUPABASE_DB_URL
 */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const MIGRATION = join(ROOT, 'supabase/migrations/0001_init.sql');
const quiet = process.argv.includes('--quiet');

let sql;
try {
  sql = readFileSync(MIGRATION, 'utf8');
} catch {
  console.error(`Could not read ${MIGRATION}`);
  console.error('Expected the migration to exist. Nothing to apply.');
  process.exit(1);
}

if (quiet) {
  process.stdout.write(sql);
  process.exit(0);
}

const dbUrl = process.env.SUPABASE_DB_URL;
const projectUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const projectRef = projectUrl ? /https:\/\/([a-z0-9]+)\.supabase\.co/i.exec(projectUrl)?.[1] : undefined;
const lines = sql.split('\n').length;

console.log('');
console.log('SALON MALONE — schema migration (0001_init.sql)');
console.log(`${lines} lines · 5 tables · idempotent, safe to re-run`);
console.log('');
console.log('─'.repeat(78));
console.log('OPTION A — SQL Editor (what you want the first time)');
console.log('─'.repeat(78));
console.log('  1. Open the SQL Editor:');
console.log(
  projectRef
    ? `       https://supabase.com/dashboard/project/${projectRef}/sql/new`
    : '       https://supabase.com/dashboard → your project → SQL Editor → New query',
);
console.log('  2. Paste the SQL printed below, or pipe it straight to your clipboard:');
console.log('       node scripts/apply-migration.mjs --quiet | pbcopy      # macOS');
console.log('       node scripts/apply-migration.mjs --quiet | xclip -sel c # Linux');
console.log('  3. Run it. Expect "Success. No rows returned."');
console.log('  4. Verify: Table Editor should list clients, contacts, calls, suppression, bookings —');
console.log('     each showing "RLS enabled" with zero policies. That is correct and intentional:');
console.log('     the service role bypasses RLS, and the anon key must therefore see nothing.');
console.log('');
console.log('─'.repeat(78));
console.log('OPTION B — psql');
console.log('─'.repeat(78));
if (dbUrl) {
  console.log('  SUPABASE_DB_URL is set. Run:');
  console.log('');
  console.log('       psql "$SUPABASE_DB_URL" -v ON_ERROR_STOP=1 -f supabase/migrations/0001_init.sql');
  console.log('');
  console.log('  (Load the env first: node --env-file=.env.local, or export it in your shell.)');
} else {
  console.log('  SUPABASE_DB_URL is not set. Grab it from');
  console.log('       Supabase dashboard → Project Settings → Database → Connection string → URI');
  console.log('  add it to .env.local as SUPABASE_DB_URL=postgresql://..., then:');
  console.log('');
  console.log('       psql "$SUPABASE_DB_URL" -v ON_ERROR_STOP=1 -f supabase/migrations/0001_init.sql');
}
console.log('');
console.log('─'.repeat(78));
console.log('NOT AN OPTION — the REST API');
console.log('─'.repeat(78));
console.log('  PostgREST executes queries against existing tables and functions. It cannot run DDL,');
console.log('  so there is no way to create this schema with SUPABASE_SERVICE_ROLE_KEY over HTTP.');
console.log('  Do not add a generic exec_sql RPC to work around this — an arbitrary-SQL function');
console.log('  reachable from the app is a much bigger problem than pasting SQL once.');
console.log('');
console.log('─'.repeat(78));
console.log('SQL follows');
console.log('─'.repeat(78));
console.log('');
process.stdout.write(sql);
console.log('');
