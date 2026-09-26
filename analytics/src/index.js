// The Circulation Desk: collector, API and dashboard for caratcapital.org.
//
//   POST /c              beacons from the site tracker (public)
//   POST /api/login      staff password → session cookie
//   POST /api/logout
//   GET  /api/session    is this browser signed in? (always 200)
//   GET  /api/overview   ?range=today|7d|30d|90d|12m
//   GET  /api/story      ?path=/a-some-story&range=…
//   GET  /api/live       the last thirty minutes
//   everything else      the dashboard's static files (./public)

import { collect } from './ingest.js';
import { hasSession, login, logout } from './auth.js';
import { live, overview, story } from './stats.js';
import { cron } from './rollup.js';
import { json, secure, timezone } from './http.js';

async function api(request, env, url) {
  const path = url.pathname;
  if (path === '/api/login' && request.method === 'POST') return login(request, env);
  if (path === '/api/logout' && request.method === 'POST') return logout(request);
  const signedIn = await hasSession(request, env);
  // The dashboard asks this on every load, so a signed-out answer is not an error.
  if (path === '/api/session') {
    return json({ signedIn, configured: !!env.DASHBOARD_PASSWORD, tz: timezone(env) });
  }
  if (!signedIn) return json({ error: env.DASHBOARD_PASSWORD ? 'signed-out' : 'not-configured' }, 401);
  if (request.method !== 'GET') return json({ error: 'method-not-allowed' }, 405);
  if (path === '/api/overview') return json(await overview(env, url));
  if (path === '/api/story') return json(await story(env, url));
  if (path === '/api/live') return json(await live(env));
  return json({ error: 'not-found' }, 404);
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === '/c') return collect(request, env, ctx);
    if (url.pathname.startsWith('/api/')) {
      try {
        return await api(request, env, url);
      } catch (e) {
        console.error('circulation api error:', e?.stack || e);
        // D1's free tier refuses queries past its daily row limits until midnight UTC.
        const capped = /daily row (read|write) limit/i.test(String(e?.message));
        return json({ error: capped ? 'daily-limit' : 'server-error' }, capped ? 503 : 500);
      }
    }
    return secure(await env.ASSETS.fetch(request));
  },

  async scheduled(controller, env, ctx) {
    ctx.waitUntil(cron(env).catch((e) => console.error('circulation roll-up failed:', e?.stack || e)));
  },
};
