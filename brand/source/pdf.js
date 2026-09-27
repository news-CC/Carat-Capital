// Prints the brand book to PDF (one 1600×1000 page per spread) and saves page previews.
const { chromium } = require('playwright'); const { useFonts } = require('./fontroute'); const fs = require('fs');
(async () => {
  const path = require('path');
  const [,, src = path.join(__dirname, '..', 'brand-book.html'), out = path.join(__dirname, '..', 'Carat-Capital-Brand-Book.pdf'), prev = ''] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1600, height: 1000 } }); await useFonts(p);
  await p.goto('file://' + src, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
  await p.emulateMedia({ media: 'print' });
  await p.pdf({ path: out, width: '1600px', height: '1000px', printBackground: true, preferCSSPageSize: true });
  if (prev) { fs.mkdirSync(prev, { recursive: true }); const els = await p.$$('.sp'); let i = 1; for (const e of els) await e.screenshot({ path: `${prev}/p${String(i++).padStart(2, '0')}.png` }); }
  await b.close(); console.log('pdf', (fs.statSync(out).size / 1024 / 1024).toFixed(2) + 'MB');
})();
