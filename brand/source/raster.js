// Renders SVG/HTML to PNG or JPEG with Chromium. jobs: [out, html, w, h, type]
const { chromium } = require('playwright');
async function raster(jobs) {
  const b = await chromium.launch();
  for (const [out, html, w, h, type = 'png', transparent = false] of jobs) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(`<!doctype html><html><head><style>html,body{margin:0;width:${w}px;height:${h}px;overflow:hidden${transparent ? ';background:transparent' : ''}}</style></head><body>${html}</body></html>`, { waitUntil: 'networkidle' });
    await p.screenshot({ path: out, type, ...(type === 'jpeg' ? { quality: 93 } : {}), omitBackground: transparent });
    await p.close();
  }
  await b.close();
}
module.exports = { raster };
