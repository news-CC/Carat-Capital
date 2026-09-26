// One shared staff password (the DASHBOARD_PASSWORD secret) opens the desk.
// A signed, HttpOnly session cookie keeps it open for thirty days. Changing
// the password signs everyone out, because the signing key is derived from it.

import { hex, json } from './http.js';

const COOKIE = 'cc_session';
const TTL = 30 * 24 * 3600;
const enc = new TextEncoder();

const b64url = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf)))
  .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

const unb64url = (s) => {
  const bin = atob(s.replace(/-/g, '+').replace(/_/g, '/'));
  return Uint8Array.from(bin, (c) => c.charCodeAt(0));
};

let cachedKey = { secret: '', key: null };

async function signingKey(env) {
  if (cachedKey.secret === env.DASHBOARD_PASSWORD && cachedKey.key) return cachedKey.key;
  const read = () => env.DB.prepare("SELECT v FROM meta WHERE k = 'session_salt'").first('v');
  let salt = await read();
  if (!salt) {
    await env.DB.prepare("INSERT OR IGNORE INTO meta (k, v) VALUES ('session_salt', ?1)")
      .bind(hex(crypto.getRandomValues(new Uint8Array(32)))).run();
    salt = await read();
  }
  const material = await crypto.subtle.digest('SHA-256', enc.encode(`${salt}|${env.DASHBOARD_PASSWORD}`));
  const key = await crypto.subtle.importKey('raw', material, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign', 'verify']);
  cachedKey = { secret: env.DASHBOARD_PASSWORD, key };
  return key;
}

async function samePassword(given, expected) {
  const [a, b] = await Promise.all([
    crypto.subtle.digest('SHA-256', enc.encode(given)),
    crypto.subtle.digest('SHA-256', enc.encode(expected)),
  ]);
  return crypto.subtle.timingSafeEqual(a, b);
}

function cookieOf(request, name) {
  for (const part of (request.headers.get('Cookie') || '').split(';')) {
    const [k, ...v] = part.trim().split('=');
    if (k === name) return v.join('=');
  }
  return '';
}

const sameOrigin = (request) => {
  const origin = request.headers.get('Origin');
  return !origin || origin === new URL(request.url).origin;
};

export async function hasSession(request, env) {
  if (!env.DASHBOARD_PASSWORD) return false;
  const [exp, sig] = cookieOf(request, COOKIE).split('.');
  if (!exp || !sig || !(Number(exp) > Date.now() / 1000)) return false;
  try {
    return await crypto.subtle.verify('HMAC', await signingKey(env), unb64url(sig), enc.encode(`v1:${exp}`));
  } catch {
    return false;
  }
}

export async function login(request, env) {
  if (!env.DASHBOARD_PASSWORD) return json({ error: 'not-configured' }, 503);
  if (!sameOrigin(request)) return json({ error: 'forbidden' }, 403);
  if (env.LOGINS) {
    const { success } = await env.LOGINS.limit({ key: request.headers.get('CF-Connecting-IP') || 'unknown' });
    if (!success) return json({ error: 'slow-down' }, 429);
  }
  let password = '';
  try { password = String((await request.json()).password ?? ''); } catch { /* treated as empty */ }
  if (!(await samePassword(password, env.DASHBOARD_PASSWORD))) {
    await new Promise((r) => setTimeout(r, 600));
    return json({ error: 'wrong-password' }, 401);
  }
  const exp = Math.floor(Date.now() / 1000) + TTL;
  const sig = await crypto.subtle.sign('HMAC', await signingKey(env), enc.encode(`v1:${exp}`));
  return json({ ok: true }, 200, {
    'Set-Cookie': `${COOKIE}=${exp}.${b64url(sig)}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=${TTL}`,
  });
}

export function logout(request) {
  if (!sameOrigin(request)) return json({ error: 'forbidden' }, 403);
  return json({ ok: true }, 200, {
    'Set-Cookie': `${COOKIE}=; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=0`,
  });
}
