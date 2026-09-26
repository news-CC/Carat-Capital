// Response helpers shared by the API and the dashboard shell.

const PRIVATE = {
  'Cache-Control': 'no-store',
  'X-Content-Type-Options': 'nosniff',
  'X-Robots-Tag': 'noindex, nofollow',
  'Referrer-Policy': 'no-referrer',
};

export function json(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', ...PRIVATE, ...extra },
  });
}

const CSP = [
  "default-src 'none'",
  "script-src 'self'",
  "style-src 'self' https://fonts.googleapis.com",
  'font-src https://fonts.gstatic.com',
  "img-src 'self' data:",
  "connect-src 'self'",
  "base-uri 'none'",
  "form-action 'self'",
  "frame-ancestors 'none'",
].join('; ');

/** The dashboard's static files, with the headers a private back office wants. */
export function secure(response) {
  const r = new Response(response.body, response);
  r.headers.set('Content-Security-Policy', CSP);
  r.headers.set('X-Frame-Options', 'DENY');
  for (const [k, v] of Object.entries(PRIVATE)) if (k !== 'Cache-Control') r.headers.set(k, v);
  if ((r.headers.get('Content-Type') || '').includes('text/html')) r.headers.set('Cache-Control', 'no-cache');
  return r;
}

export const timezone = (env) => env.TIMEZONE || 'America/New_York';

export function siteHosts(env) {
  return new Set(String(env.SITE_HOSTS || 'caratcapital.org,www.caratcapital.org')
    .split(',').map((h) => h.trim().toLowerCase()).filter(Boolean));
}

export const hex = (bytes) => Array.from(bytes, (b) => b.toString(16).padStart(2, '0')).join('');
