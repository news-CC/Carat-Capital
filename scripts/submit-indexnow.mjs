#!/usr/bin/env node
/**
 * Push the public URLs to IndexNow — Bing, Yandex, Seznam and Naver share one endpoint.
 *
 *   npm run seo:submit
 *
 * Google does NOT participate in IndexNow, and it retired its sitemap ping endpoint in 2023.
 * The only way to nudge Google is Search Console (verify the property, then Sitemaps → submit
 * /sitemap.xml, or URL Inspection → Request Indexing per page). No API key can do it for you
 * without an OAuth-authorised service account attached to a verified property, so this script
 * deliberately does not pretend to.
 *
 * Ownership proof is the key file at /<key>.txt containing the key and nothing else. If that file
 * 404s the submission is accepted (202) and then silently ignored, so this checks it first.
 */
const KEY = process.env.INDEXNOW_KEY;
const APP = (process.env.NEXT_PUBLIC_APP_URL || 'https://www.startup25.com').replace(/\/+$/, '');

if (!KEY) {
  console.error('INDEXNOW_KEY missing. Run with: node --env-file=.env.local scripts/submit-indexnow.mjs');
  process.exit(1);
}

const host = new URL(APP).host;
const keyLocation = `${APP}/${KEY}.txt`;
const urlList = ['/', '/start', '/terms', '/privacy'].map((p) => `${APP}${p}`);

// Verify the key file is actually reachable before claiming the submission worked.
const probe = await fetch(keyLocation, { redirect: 'follow' }).catch(() => null);
const probeBody = probe && probe.ok ? (await probe.text()).trim() : null;
if (!probe?.ok || probeBody !== KEY) {
  console.error(`Key file check FAILED at ${keyLocation}`);
  console.error(`  status: ${probe?.status ?? 'unreachable'}`);
  if (probeBody !== null) console.error(`  body:   ${JSON.stringify(probeBody).slice(0, 80)} (expected ${KEY})`);
  console.error('\nDeploy first — IndexNow accepts the request and then drops it if it cannot verify ownership.');
  process.exit(1);
}
console.log(`key file verified at ${keyLocation}`);

const res = await fetch('https://api.indexnow.org/indexnow', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json; charset=utf-8' },
  body: JSON.stringify({ host, key: KEY, keyLocation, urlList }),
});

const body = await res.text();
console.log(`\nIndexNow -> HTTP ${res.status} ${body || '(empty body, which is normal)'}`);
console.log(`submitted ${urlList.length} urls:`);
for (const u of urlList) console.log(`  ${u}`);

// 200 = accepted, 202 = accepted pending key validation. Anything else is a real failure.
if (res.status !== 200 && res.status !== 202) {
  console.error('\nSubmission rejected.');
  process.exit(1);
}
console.log('\nBing/Yandex accepted. For Google, use Search Console — see README.');
