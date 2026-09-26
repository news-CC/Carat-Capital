// Captures renders of the built site for the brand book (JPEG). Run python3 build.py first.
const path = require('path'); const ROOT = path.join(__dirname, '..', '..'); const OUTD = path.join(__dirname, 'build'); require('fs').mkdirSync(OUTD, { recursive: true });
const { chromium } = require('playwright'); const { useFonts } = require('./fontroute');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl'] });
  const shot = async (file, out, w, h, scroll = 0) => { const p = await b.newPage({ viewport: { width: w, height: h } }); await useFonts(p);
    await p.goto('file://' + file, { waitUntil: 'networkidle' }); await p.waitForTimeout(3800); if (scroll) { await p.mouse.wheel(0, scroll); await p.waitForTimeout(1500); }
    await p.screenshot({ path: out, type: 'jpeg', quality: 80 }); await p.close(); };
  await shot(path.join(ROOT, 'index.html'), path.join(OUTD, 'cap-home.jpg'), 1440, 810);
  await shot(path.join(ROOT, 'a-the-bar-and-the-token.html'), path.join(OUTD, 'cap-article.jpg'), 1440, 640);
  await shot(path.join(ROOT, 'magazine.html'), path.join(OUTD, 'cap-folio.jpg'), 1440, 800);
  await shot(path.join(ROOT, 'index.html'), path.join(OUTD, 'cap-phone.jpg'), 390, 760);
  await b.close(); console.log('captured');
})();
