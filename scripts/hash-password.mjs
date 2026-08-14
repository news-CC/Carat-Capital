#!/usr/bin/env node
/**
 * Prints the ADMIN_PASSWORD_HASH line for .env.local / Vercel.
 *
 * MUST STAY IN SYNC with hashPassword()/verifyPassword() in src/lib/auth.ts:
 *   salt = 16 random bytes
 *   key  = scrypt(password, salt AS RAW BYTES, 64)   // Node's default N=16384, r=8, p=1
 *   line = `scrypt$${salt.toString('hex')}$${key.toString('hex')}`
 * If you change the KDF there, change it here — a mismatch locks you out of /login with no error
 * message beyond "wrong password".
 *
 * Usage:
 *   node scripts/hash-password.mjs 'my long passphrase'
 *   printf %s 'my long passphrase' | node scripts/hash-password.mjs
 */
import { randomBytes, scryptSync } from 'node:crypto';

const KEY_LENGTH = 64;
const SALT_LENGTH = 16;

function hashPassword(password) {
  const salt = randomBytes(SALT_LENGTH);
  const key = scryptSync(password, salt, KEY_LENGTH);
  return `scrypt$${salt.toString('hex')}$${key.toString('hex')}`;
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString('utf8');
}

async function main() {
  const fromArgv = process.argv.slice(2).filter((a) => !a.startsWith('--'));
  let password;

  if (fromArgv.length > 0) {
    password = fromArgv.join(' ');
    console.error('note: the password is now in your shell history. Clear it, or pipe it via stdin next time.');
  } else if (!process.stdin.isTTY) {
    password = (await readStdin()).replace(/\r?\n$/, '');
  } else {
    console.error('Pass the password as an argument or pipe it in:');
    console.error("  node scripts/hash-password.mjs 'my long passphrase'");
    console.error("  printf %s 'my long passphrase' | node scripts/hash-password.mjs");
    process.exit(1);
  }

  if (password.length === 0) {
    console.error('error: empty password.');
    process.exit(1);
  }
  if (password.length < 12) {
    console.error(`warning: ${password.length} characters. This is the only lock on /admin — use 16+.`);
  }

  const hash = hashPassword(password);

  console.log('');
  console.log('Add this to .env.local and to your Vercel project env (all environments):');
  console.log('');
  console.log(`ADMIN_PASSWORD_HASH=${hash}`);
  console.log('');
  console.log('Notes:');
  console.log('  · This value also keys the session cookie HMAC. Rotating it signs everyone out. Good.');
  console.log('  · Re-running this script on the same password gives a different (equally valid) line —');
  console.log('    the salt is random. Store one, not both.');
  console.log('');
}

main().catch((e) => {
  console.error('failed:', e instanceof Error ? e.message : e);
  process.exit(1);
});
