// Serve Google Fonts to headless Chromium via curl (which trusts the proxy CA bundle); TLS stays verified.
const { execFileSync } = require('child_process');
const cache = {};
async function useFonts(page) {
  await page.route(/https:\/\/fonts\.(googleapis|gstatic)\.com\/.*/, async (route) => {
    const url = route.request().url();
    try {
      if (!cache[url]) cache[url] = execFileSync('curl', ['-sS', '-A', route.request().headers()['user-agent'] || 'Mozilla/5.0', url], { maxBuffer: 1 << 26 });
      const css = url.includes('googleapis');
      await route.fulfill({ status: 200, body: cache[url], contentType: css ? 'text/css' : (url.endsWith('.woff2') ? 'font/woff2' : 'application/octet-stream'), headers: { 'access-control-allow-origin': '*' } });
    } catch (e) { await route.abort(); }
  });
  await page.route(/gc\.zgo\.at/, (r) => r.abort());
}
module.exports = { useFonts };
