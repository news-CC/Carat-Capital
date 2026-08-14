import { createHmac, randomBytes, scryptSync, timingSafeEqual } from 'node:crypto';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { optionalEnv } from '@/lib/env';

/**
 * One operator, one password, one signed cookie. No user table, no signup.
 * Node runtime only — middleware must not import this (it does a presence check
 * and lets the admin layout call requireAdmin()).
 */

export const SESSION_COOKIE = 'sm_session';

const SESSION_TTL_MS = 7 * 24 * 60 * 60 * 1000;
const SCRYPT_KEYLEN = 64;

/** The documented way to produce ADMIN_PASSWORD_HASH (see scripts/hash-password.mjs). */
export function hashPassword(password: string): string {
  const salt = randomBytes(16);
  const key = scryptSync(password, salt, SCRYPT_KEYLEN);
  return `scrypt$${salt.toString('hex')}$${key.toString('hex')}`;
}

/** Constant-time only once lengths match; length itself is not a secret here. */
function equal(a: Buffer, b: Buffer): boolean {
  return a.length === b.length && timingSafeEqual(a, b);
}

export function verifyPassword(password: string, stored: string): boolean {
  if (typeof password !== 'string' || typeof stored !== 'string' || stored === '') return false;

  // Escape hatch so the operator can boot before hashing anything. hashPassword
  // is the documented path; 'plain$' is for day one only.
  if (stored.startsWith('plain$')) {
    return equal(Buffer.from(password, 'utf8'), Buffer.from(stored.slice(6), 'utf8'));
  }

  const [scheme, saltHex, keyHex] = stored.split('$');
  if (scheme !== 'scrypt' || !saltHex || !keyHex) return false;

  const expected = Buffer.from(keyHex, 'hex');
  if (expected.length === 0) return false;
  try {
    return equal(scryptSync(password, Buffer.from(saltHex, 'hex'), expected.length), expected);
  } catch {
    return false;
  }
}

export function verifyAdminCredentials(email: string, password: string): boolean {
  const adminEmail = optionalEnv('ADMIN_EMAIL');
  const stored = optionalEnv('ADMIN_PASSWORD_HASH');
  if (!adminEmail || !stored) return false;

  const emailMatches = equal(
    Buffer.from(email.trim().toLowerCase(), 'utf8'),
    Buffer.from(adminEmail.toLowerCase(), 'utf8'),
  );
  // Always run the password check so a wrong email is not faster than a wrong password.
  const passwordMatches = verifyPassword(password, stored);
  return emailMatches && passwordMatches;
}

function sessionKey(): string {
  const key = optionalEnv('ADMIN_PASSWORD_HASH') ?? optionalEnv('SUPABASE_SERVICE_ROLE_KEY');
  if (!key) throw new Error('Cannot sign sessions: set ADMIN_PASSWORD_HASH');
  return key;
}

const b64url = (input: Buffer | string): string =>
  (typeof input === 'string' ? Buffer.from(input, 'utf8') : input).toString('base64url');

function sign(payload: string): string {
  return b64url(createHmac('sha256', sessionKey()).update(payload).digest());
}

export function signSession(email: string, issuedAt: number = Date.now()): string {
  const payload = b64url(JSON.stringify({ email: email.trim().toLowerCase(), iat: issuedAt }));
  return `${payload}.${sign(payload)}`;
}

export function verifySessionToken(token: string | undefined | null): { email: string } | null {
  if (!token) return null;
  const [payload, signature] = token.split('.');
  if (!payload || !signature) return null;

  let expected: string;
  try {
    expected = sign(payload);
  } catch {
    return null; // no key configured -> nobody is authenticated
  }
  if (!equal(Buffer.from(signature, 'utf8'), Buffer.from(expected, 'utf8'))) return null;

  try {
    const decoded: unknown = JSON.parse(Buffer.from(payload, 'base64url').toString('utf8'));
    if (typeof decoded !== 'object' || decoded === null) return null;
    const { email, iat } = decoded as { email?: unknown; iat?: unknown };
    if (typeof email !== 'string' || email === '' || typeof iat !== 'number') return null;

    const age = Date.now() - iat;
    if (age < -60_000 || age > SESSION_TTL_MS) return null; // future-dated or expired
    return { email };
  } catch {
    return null;
  }
}

export async function getSession(): Promise<{ email: string } | null> {
  const jar = await cookies();
  return verifySessionToken(jar.get(SESSION_COOKIE)?.value);
}

export async function requireAdmin(): Promise<{ email: string }> {
  const session = await getSession();
  if (!session) redirect('/login');
  return session;
}

/** Shared by the login action and logout so the cookie shape stays in one place. */
export const sessionCookieOptions = {
  httpOnly: true,
  sameSite: 'lax',
  secure: optionalEnv('NODE_ENV') === 'production',
  path: '/',
  maxAge: SESSION_TTL_MS / 1000,
} as const;
