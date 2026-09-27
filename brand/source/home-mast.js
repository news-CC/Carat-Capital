// The front-page masthead: the no-tagline lockup as layered artwork for home_template.html.
// Layers: symbol L cut (≥96 px) and M cut, the construction strokes (pathLength=1), the transient
// cutter's labels, the outlined name (the "impression" animates its fill), and the two points.
const Pn = require('./point'); const { C, r2, poly, line } = require('./lib'); const fs = require('fs'); const path = require('path');
const { G } = Pn, size = 200, W = Pn.wordmark({ cut: 'display', size }), cap = W.cap, desc = W.desc;
const symH = cap + desc, sc = symH / G.H, symW = G.half * 2 * sc, gap = size * 0.34, tx = symW + gap;
const Wm = Pn.wordmark({ cut: 'display', size, x: tx, base: cap, fg: 'currentColor', dot: C.seal });
const VW = tx + Wm.w, VH = symH;
const name = Wm.body.replace(/<circle[^>]*\/>/, ''), dot = Wm.body.match(/<circle[^>]*\/>/)[0].replace('<circle', '<circle class="pt pt-a"');
const cut = (c, id) => { const m = Pn.mark({ cut: c, cx: 0, top: 0, fg: 'currentColor' }); return m.defs.replace(/id="k[0-9a-z]+"/, `id="${id}"`) + `<g class="sym sym-${c}">${m.body.replace(/url\(#k[0-9a-z]+\)/, `url(#${id})`).replace('<circle', '<circle class="pt pt-b"')}</g>`; };
// construction: the facet edges in the order a cutter lays them out
const P = (x, y) => [x, y], TL = P(-G.tw, 0), TR = P(G.tw, 0), GL = P(-G.half, G.ch), GR = P(G.half, G.ch), FL = P(-G.fx, G.ch), FR = P(G.fx, G.ch), CU = P(0, G.H), HO = P(0, G.hy);
const edges = [[GL, GR], [TL, GL], [TR, GR], [TL, TR], [TL, FL], [TR, FR], [GL, CU], [GR, CU], [FL, CU], [FR, CU], [[0, G.hy + 44], CU]];
const con = edges.map((e, i) => `<path class="cs" style="--i:${i}" pathLength="1" d="${line(e[0], e[1])}"/>`).join('') + `<circle class="cs cs-o" style="--i:11" pathLength="1" cx="0" cy="${r2(G.hy)}" r="44"/>`;
const X = (x) => r2(symW / 2 + x * sc), Y = (y) => r2(y * sc);
const lab = (t, x, y, a = 'middle') => `<text x="${x}" y="${y}" text-anchor="${a}">${t}</text>`;
const labels = lab('0.56', X(0), -16) + lab('34.5°', X(-G.half) - 10, Y(G.ch * 0.5) + 4, 'end') + lab('45°', X(-G.half * 0.62) - 12, Y(G.ch + G.pd * 0.42), 'end') + lab('1 pt = 0.01 ct', X(0), VH + 26);
const svg = `<svg class="mast-art" viewBox="0 0 ${r2(VW)} ${r2(VH)}" overflow="visible" aria-hidden="true" focusable="false"><defs>${''}</defs>`
  + `<g class="symw" transform="translate(${r2(symW / 2)} 0) scale(${r2(sc * 10000) / 10000})">${cut('L', 'mastL')}${cut('M', 'mastM')}<g class="con">${con}</g></g>`
  + `<g class="lbl">${labels}</g><g class="nm">${name}</g>${dot}</svg>`;
const out = path.join(__dirname, 'build', 'snippets'); fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, 'masthead.svg'), svg);
console.log('masthead', r2(VW), 'x', r2(VH), 'W_em', r2(VW / size), (svg.length / 1024).toFixed(1) + 'KB');

// The mark the Brief's turning stone settles into: the brand's engraved cut in gilt, served as assets/stone-mark.svg.
// Its tight viewBox puts the girdle at x 40–840, so the canvas stone (radius s) overlays it at width 2.2 s.
const eng = Pn.symbol({ style: 'engraved', tight: true, gold: true }).replace(/id="([a-z]+\d*[a-z0-9]*)"/g, 'id="eg-$1"').replace(/url\(#([a-z]+\d*[a-z0-9]*)\)/g, 'url(#eg-$1)');
fs.writeFileSync(path.join(__dirname, '..', '..', 'assets', 'stone-mark.svg'), eng);
console.log('stone-mark', (eng.length / 1024).toFixed(1) + 'KB', eng.match(/viewBox="[^"]+"/)[0]);
