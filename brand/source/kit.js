// Exports the final The Point logo kit into brand/logo/{svg,png,favicon,social}.
const Pn = require('./point'); const { C } = require('./lib'); const { raster } = require('./raster');
const fs = require('fs'); const path = require('path');
const OUT = process.argv[2] || path.join(__dirname, '..', 'logo');
const P = C.paper, I = C.ink, S = C.seal, GOLD = C.foilB;
const HDR = '<?xml version="1.0" encoding="UTF-8"?>\n<!-- Carat Capital · The Point · brand/README.md. Outlined type; knockouts are transparent. -->\n';
const svgs = {
  'carat-capital-lockup.svg': Pn.lockup({}), 'carat-capital-lockup-reverse.svg': Pn.lockup({ fg: P }), 'carat-capital-lockup-gold.svg': Pn.lockup({ fg: GOLD, gold: true }),
  'carat-capital-lockup-no-tagline.svg': Pn.lockup({ tag: false }), 'carat-capital-lockup-no-tagline-reverse.svg': Pn.lockup({ tag: false, fg: P }),
  'carat-capital-lockup-stacked.svg': Pn.lockup({ layout: 'stacked' }), 'carat-capital-lockup-stacked-reverse.svg': Pn.lockup({ layout: 'stacked', fg: P }),
  'carat-capital-lockup-mono-ink.svg': Pn.lockup({ dot: I }), 'carat-capital-lockup-mono-paper.svg': Pn.lockup({ fg: P, dot: P }),
  'carat-capital-wordmark.svg': Pn.lockup({ layout: 'wordmark', tag: false }), 'carat-capital-wordmark-reverse.svg': Pn.lockup({ layout: 'wordmark', tag: false, fg: P }),
  'carat-capital-wordmark-tagline.svg': Pn.lockup({ layout: 'wordmark' }), 'carat-capital-wordmark-text-cut.svg': Pn.lockup({ layout: 'wordmark', tag: false, cut: 'text' }),
  'carat-capital-symbol-L.svg': Pn.symbol({ cut: 'L', tight: true }), 'carat-capital-symbol-L-reverse.svg': Pn.symbol({ cut: 'L', tight: true, fg: P }),
  'carat-capital-symbol-M.svg': Pn.symbol({ cut: 'M', tight: true }), 'carat-capital-symbol-M-reverse.svg': Pn.symbol({ cut: 'M', tight: true, fg: P }),
  'carat-capital-symbol-S.svg': Pn.symbol({ cut: 'S', tight: true }), 'carat-capital-symbol-S-reverse.svg': Pn.symbol({ cut: 'S', tight: true, fg: P }),
  'carat-capital-symbol-mono-ink.svg': Pn.symbol({ cut: 'L', tight: true, dot: I }), 'carat-capital-symbol-gold.svg': Pn.symbol({ cut: 'L', tight: true, gold: true }),
  'carat-capital-symbol-engraved.svg': Pn.symbol({ style: 'engraved', tight: true }), 'carat-capital-symbol-engraved-gold.svg': Pn.symbol({ style: 'engraved', tight: true, gold: true }),
};
const vb = (s) => s.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
const fit = (s, w) => { const [, , vw, vh] = vb(s); return [w, Math.round((w * vh) / vw)]; };
const img = (s) => s.replace('<svg', '<svg style="display:block;width:100%;height:100%"');
const centered = (bg, s, frac) => `<div style="width:100%;height:100%;background:${bg};display:grid;place-items:center"><div style="width:${frac * 100}%">${s.replace('<svg', '<svg style="display:block;width:100%;height:auto"')}</div></div>`;
function ico(pngs) { // PNG-in-ICO container
  const head = Buffer.alloc(6 + 16 * pngs.length); head.writeUInt16LE(0, 0); head.writeUInt16LE(1, 2); head.writeUInt16LE(pngs.length, 4);
  let off = head.length; pngs.forEach(([sz, buf], i) => { const e = 6 + 16 * i; head.writeUInt8(sz >= 256 ? 0 : sz, e); head.writeUInt8(sz >= 256 ? 0 : sz, e + 1); head.writeUInt16LE(1, e + 4); head.writeUInt16LE(32, e + 6); head.writeUInt32LE(buf.length, e + 8); head.writeUInt32LE(off, e + 12); off += buf.length; });
  return Buffer.concat([head, ...pngs.map((p) => p[1])]);
}
(async () => {
  for (const d of ['svg', 'png', 'favicon', 'social']) fs.mkdirSync(path.join(OUT, d), { recursive: true });
  for (const [n, s] of Object.entries(svgs)) fs.writeFileSync(path.join(OUT, 'svg', n), HDR + s + '\n');
  fs.writeFileSync(path.join(OUT, 'favicon', 'favicon.svg'), Pn.favicon() + '\n');
  const pngs = [['carat-capital-lockup.svg', 2400], ['carat-capital-lockup-reverse.svg', 2400], ['carat-capital-lockup-gold.svg', 2400], ['carat-capital-lockup-no-tagline.svg', 2400],
    ['carat-capital-lockup-stacked.svg', 1600], ['carat-capital-lockup-stacked-reverse.svg', 1600], ['carat-capital-wordmark.svg', 2400],
    ['carat-capital-symbol-L.svg', 1024], ['carat-capital-symbol-L-reverse.svg', 1024], ['carat-capital-symbol-engraved.svg', 2048], ['carat-capital-symbol-engraved-gold.svg', 2048]];
  const jobs = pngs.map(([n, w]) => { const [W, H] = fit(svgs[n], w); return [path.join(OUT, 'png', n.replace('.svg', `-${w}.png`)), img(svgs[n]), W, H, 'png', true]; });
  const tmp = path.join(__dirname, 'build', 'ico'); fs.mkdirSync(tmp, { recursive: true });
  const fav = Pn.symbol({ cut: 'S', tight: true });
  [16, 32, 48].forEach((s) => jobs.push([path.join(tmp, `f${s}.png`), centered('transparent', fav, 0.94), s, s, 'png', true]));
  jobs.push([path.join(OUT, 'favicon', 'apple-touch-icon.png'), centered(I, Pn.symbol({ cut: 'M', fg: P, tight: true }), 0.68), 180, 180]);
  jobs.push([path.join(OUT, 'favicon', 'icon-192.png'), centered(I, Pn.symbol({ cut: 'M', fg: P, tight: true }), 0.62), 192, 192]);
  jobs.push([path.join(OUT, 'favicon', 'icon-512.png'), centered(I, Pn.symbol({ cut: 'L', fg: P, tight: true }), 0.62), 512, 512]);
  jobs.push([path.join(OUT, 'social', 'avatar-paper-1024.png'), centered(P, Pn.symbol({ cut: 'L', tight: true }), 0.62), 1024, 1024]);
  jobs.push([path.join(OUT, 'social', 'avatar-ink-1024.png'), centered(I, Pn.symbol({ cut: 'L', fg: P, tight: true }), 0.62), 1024, 1024]);
  await raster(jobs);
  fs.writeFileSync(path.join(OUT, 'favicon', 'favicon.ico'), ico([16, 32, 48].map((s) => [s, fs.readFileSync(path.join(tmp, `f${s}.png`))])));
  fs.copyFileSync(path.join(__dirname, '..', '..', 'assets', 'share-card.png'), path.join(OUT, 'social', 'share-card-1200x630.png'));
  console.log('kit:', Object.keys(svgs).length, 'svg,', pngs.length, 'png + favicon + social');
})();
