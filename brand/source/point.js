// The Point, v2 — the Carat Capital identity. A brilliant in profile whose pavilion is a pen nib;
// the breather hole holds the red point. Three optical cuts, an engraved cut, two wordmark cuts.
const L = require('./lib');
const { C, r2, deg, setText, inkBox, poly, line, hatch, svg, foilGrad } = L;

let idn = 0; const uid = (p) => `${p}${(idn++).toString(36)}`;
const bgRect = (bg) => (bg && bg !== 'none' ? `<rect width="100%" height="100%" fill="${bg}"/>` : '');
function knockout(body, cuts, box) {
  const id = uid('k'), [x, y, w, h] = [box[0] - 60, box[1] - 60, box[2] + 120, box[3] + 120];
  return { defs: `<mask id="${id}" maskUnits="userSpaceOnUse" x="${r2(x)}" y="${r2(y)}" width="${r2(w)}" height="${r2(h)}"><rect x="${r2(x)}" y="${r2(y)}" width="${r2(w)}" height="${r2(h)}" fill="#fff"/>${cuts}</mask>`, body: `<g mask="url(#${id})">${body}</g>` };
}

// Geometry: half-girdle 400. Crown 34.5° on a 56% table (Tolkowsky's crown angle, a modern ideal
// table); pavilion 45° so the stone doubles as a nib. The point sits a third of the way down the
// pavilion; the facet break on the girdle at 36% of the half-width.
const G = (() => { const half = 400, tw = half * 0.56, ch = (half - tw) * Math.tan(deg(34.5)), pd = half * Math.tan(deg(45));
  return { half, tw, ch, pd, H: ch + pd, fx: 0.36 * half, hy: ch + pd / 3 }; })();
// Optical cuts. k = knockout weight, hr = hole radius, dr = point radius (units of the 800-wide stone).
const CUTS = {
  L: { k: 11, hr: 44, dr: 31, crown: true, pav: true, use: '96 px and up · 25 mm and up' },
  M: { k: 20, hr: 54, dr: 34, crown: false, pav: true, use: '32–96 px · 9–25 mm' },
  S: { k: 34, hr: 76, dr: 44, crown: false, pav: false, use: '16–32 px · under 9 mm' },
};
const pts = (cx, top) => { const P = (x, y) => [cx + x, top + y];
  return { P, TL: P(-G.tw, 0), TR: P(G.tw, 0), GL: P(-G.half, G.ch), GR: P(G.half, G.ch), FL: P(-G.fx, G.ch), FR: P(G.fx, G.ch), M0: P(0, G.ch), CU: P(0, G.H), HO: P(0, G.hy) }; };

// Symbol markup at (cx, top) in stone units. fg = body, dot = the point, cut = L|M|S.
function mark({ fg = C.ink, dot = C.seal, cut = 'L', cx = 0, top = 0, fill = null } = {}) {
  const c = CUTS[cut], p = pts(cx, top);
  let cuts = line([p.GL[0] - 24, p.GL[1]], [p.GR[0] + 24, p.GR[1]]);
  if (c.crown) cuts += line(p.TL, p.FL) + line(p.TR, p.FR);
  if (c.pav) cuts += line(p.FL, p.CU) + line(p.FR, p.CU);
  cuts += line([p.HO[0], p.HO[1] + c.hr - 4], [p.CU[0], p.CU[1] + 40]);
  const ko = knockout(`<path d="${poly([p.TL, p.TR, p.GR, p.CU, p.GL])}" fill="${fill || fg}"/>`,
    `<path d="${cuts}" stroke="#000" stroke-width="${c.k}"/><circle cx="${r2(p.HO[0])}" cy="${r2(p.HO[1])}" r="${c.hr}" fill="#000"/>`, [cx - 450, top - 40, 900, G.H + 80]);
  return { defs: ko.defs, body: ko.body + `<circle cx="${r2(p.HO[0])}" cy="${r2(p.HO[1])}" r="${c.dr}" fill="${dot}"/>` };
}
// The engraved cut: line art for print, foil and certificates. Each facet is hatched at its own
// angle and density, lit from the upper left, so the stone reads in pure line.
function engraved({ fg = C.ink, dot = C.seal, cx = 0, top = 0, w = 3.4 } = {}) {
  const p = pts(cx, top), ang = (a, b) => (Math.atan2(b[1] - a[1], b[0] - a[0]) * 180) / Math.PI;
  const F = [ // [polygon, hatch angle, spacing]
    [[p.TL, p.FL, p.GL], ang(p.GL, p.TL), 13], [[p.TL, p.TR, p.FR, p.FL], 0, 8.5], [[p.TR, p.GR, p.FR], ang(p.TR, p.GR), 5.2],
    [[p.GL, p.FL, p.CU], ang(p.GL, p.CU), 6.2], [[p.FL, p.M0, p.CU], ang(p.FL, p.CU), 4.6], [[p.M0, p.FR, p.CU], ang(p.FR, p.CU), 11], [[p.FR, p.GR, p.CU], ang(p.GR, p.CU), 4.8],
  ];
  let defs = '', hs = '';
  F.forEach(([pl, a, s]) => { const h = hatch(pl, a, s, w * 0.62, fg); defs += h.defs; hs += h.body; });
  const ko = knockout(hs, `<circle cx="${r2(p.HO[0])}" cy="${r2(p.HO[1])}" r="52" fill="#000"/><path d="${line([p.HO[0], p.HO[1]], p.CU)}" stroke="#000" stroke-width="14"/>`, [cx - 450, top - 40, 900, G.H + 80]);
  const edges = line(p.GL, p.GR) + line(p.TL, p.FL) + line(p.TR, p.FR) + line(p.FL, p.CU) + line(p.FR, p.CU) + line([p.HO[0], p.HO[1] + 42], p.CU);
  return { defs: defs + ko.defs, body: ko.body + `<path d="${poly([p.TL, p.TR, p.GR, p.CU, p.GL])}" fill="none" stroke="${fg}" stroke-width="${w * 2.4}" stroke-linejoin="miter"/><path d="${edges}" fill="none" stroke="${fg}" stroke-width="${w * 1.3}"/><circle cx="${r2(p.HO[0])}" cy="${r2(p.HO[1])}" r="42" fill="none" stroke="${fg}" stroke-width="${w * 1.3}"/><circle cx="${r2(p.HO[0])}" cy="${r2(p.HO[1])}" r="28" fill="${dot}"/>` };
}
// Standalone symbol files: square 1000 canvas, or tight (bounds + margin) for UI use.
function symbol({ cut = 'L', fg = C.ink, dot = C.seal, bg = 'none', tight = false, style = 'solid', gold = false } = {}) {
  const gid = uid('g'), top = tight ? 30 : (1000 - G.H) / 2 - 8, cx = tight ? 440 : 500;
  const m = style === 'engraved' ? engraved({ fg: gold ? `url(#${gid})` : fg, dot, cx, top }) : mark({ fg, dot, cut, cx, top, fill: gold ? `url(#${gid})` : null });
  const vb = tight ? `0 0 880 ${r2(G.H + 60)}` : '0 0 1000 1000';
  return svg(vb, bgRect(bg) + m.body, (gold ? foilGrad(gid, 0, 0, 1, 1) : '') + m.defs);
}

// Wordmark: Bodoni Moda 500. Display cut = optical size 28 (lockups); text cut = optical size 11
// (small sizes, live web text). The point is 0.16 em, on the baseline, 0.05 em after the l.
const WM = { display: { f: 'bodoni500o28', tr: -22 }, text: { f: 'bodoni500', tr: -8 } };
function wordmark({ cut = 'display', size = 200, fg = C.ink, dot = C.seal, x = 0, base = 0 } = {}) {
  const { f, tr } = WM[cut], b = inkBox(f, 'Carat Capital', size, tr), cap = inkBox(f, 'C', size);
  const t = setText(f, 'Carat Capital', x - b.x1, base, size, tr);
  const r = size * 0.08, px = x + b.w + size * 0.05 + r;
  return { w: px + r - x, cap: -cap.y1, desc: size * 0.25, body: `<path fill="${fg}" d="${t.d}"/><circle cx="${r2(px)}" cy="${r2(base - r)}" r="${r2(r)}" fill="${dot}"/>` };
}
const TAG = 'THE TRADE PAPER OF THE JEWELRY WORLD';
// Tagline justified to a given measure (tracking solved so ink width = measure).
function tagline(measure, size, { fg = C.ink, x = 0, base = 0, op = 0.8 } = {}) {
  const f = 'plexmono500', b0 = inkBox(f, TAG, size, 0), n = TAG.length - 1, tr = ((measure - b0.w) / n / size) * 1000;
  const b = inkBox(f, TAG, size, tr);
  return `<path fill="${fg}" opacity="${op}" d="${setText(f, TAG, x - b.x1, base, size, tr).d}"/>`;
}

// Lockups. Measurements in wordmark units (size 200).
function lockup({ layout = 'horizontal', tag = true, fg = C.ink, dot = C.seal, bg = 'none', cut = 'display', gold = false, pad = null } = {}) {
  const size = 200, W = wordmark({ cut, size, fg, dot }), cap = W.cap, gid = uid('g');
  const P = pad ?? cap * 0.5; let body = '', defs = '', vw, vh;
  const symFill = gold ? `url(#${gid})` : null; if (gold) defs += foilGrad(gid, 0, 0, 1, 1);
  const tagSize = size * 0.16, tagGap = size * 0.56; // tagline baseline below the wordmark baseline
  if (layout === 'horizontal') {
    const symH = tag ? cap + tagGap : cap + W.desc, sc = symH / G.H, symW = G.half * 2 * sc, gap = size * 0.34;
    const tx = P + symW + gap, base = P + cap;
    const m = mark({ fg, dot, cut: 'L', cx: 0, top: 0, fill: symFill }); defs += m.defs;
    body += `<g transform="translate(${r2(P + symW / 2)} ${r2(P)}) scale(${r2(sc * 10000) / 10000})">${m.body}</g>`;
    const Wm = wordmark({ cut, size, fg, dot, x: tx, base }); body += Wm.body;
    if (tag) body += tagline(Wm.w, tagSize, { fg, x: tx, base: base + tagGap });
    vw = tx + Wm.w + P; vh = P + symH + P;
  } else if (layout === 'stacked') {
    const symW = 0.36 * W.w, sc = symW / (G.half * 2), symH = G.H * sc, gap = cap * 0.62;
    const vwIn = W.w; vw = vwIn + 2 * P; const base = P + symH + gap + cap;
    const m = mark({ fg, dot, cut: 'L', cx: 0, top: 0, fill: symFill }); defs += m.defs;
    body += `<g transform="translate(${r2(vw / 2)} ${r2(P)}) scale(${r2(sc * 10000) / 10000})">${m.body}</g>`;
    body += wordmark({ cut, size, fg, dot, x: P, base }).body;
    if (tag) body += tagline(W.w, tagSize, { fg, x: P, base: base + tagGap });
    vh = base + (tag ? tagGap + P * 0.6 : W.desc * 0.2 + P);
  } else { // wordmark only
    const base = P + cap; body += wordmark({ cut, size, fg, dot, x: P, base }).body;
    if (tag) body += tagline(W.w, tagSize, { fg, x: P, base: base + tagGap });
    vw = W.w + 2 * P; vh = base + (tag ? tagGap + P * 0.6 : W.desc + P * 0.4);
  }
  return svg(`0 0 ${r2(vw)} ${r2(vh)}`, bgRect(bg) + body, defs);
}

// Favicon: small cut in a 32 box; the stone turns paper-coloured when the browser is dark.
function favicon() {
  const sc = 30 / 800, m = mark({ fg: C.ink, dot: C.seal, cut: 'S', cx: 0, top: 0 });
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><style>@media (prefers-color-scheme:dark){.b{fill:${C.paper}}}</style><defs>${m.defs}</defs><g class="s" transform="translate(16 ${r2((32 - G.H * sc) / 2)}) scale(${r2(sc * 100000) / 100000})">${m.body.replace(`fill="${C.ink}"`, `class="b" fill="${C.ink}"`)}</g></svg>`;
}

module.exports = { G, CUTS, mark, engraved, symbol, wordmark, tagline, lockup, favicon, knockout, TAG };
