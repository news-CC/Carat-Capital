// Carat Capital — five identity routes. Every mark is pure geometry + outlined type, so files are
// self-contained. Knockouts are true masks (transparent), so marks sit on any background.
const L = require('./lib');
const { C, r2, deg, setText, inkBox, arcText, poly, line, polar, brilliantTop, hatch, svg, foilGrad } = L;

let idn = 0;
const uid = (p) => `${p}${(idn++).toString(36)}`;
const bgRect = (bg, w = '100%', h = '100%') => (bg && bg !== 'none' ? `<rect width="${w}" height="${h}" fill="${bg}"/>` : '');
// Knockout: black shapes in `cuts` remove paint from `body`.
function knockout(body, cuts, box = [0, 0, 1000, 1000]) {
  const id = uid('k'), x = box[0] - 50, y = box[1] - 50, w = box[2] + 100, h = box[3] + 100;
  return { defs: `<mask id="${id}" maskUnits="userSpaceOnUse" x="${x}" y="${y}" width="${w}" height="${h}"><rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#fff"/>${cuts}</mask>`,
    body: `<g mask="url(#${id})">${body}</g>` };
}
const TAG = 'THE TRADE PAPER OF THE JEWELRY WORLD';
const label = (s, x, y, fg, size = 22, a = 'start') => { const bb = inkBox('plexmono500', s, size, 60); const ox = a === 'end' ? -bb.w : a === 'middle' ? -bb.w / 2 : 0; return `<path fill="${fg}" d="${setText('plexmono500', s, x + ox - bb.x1, y, size, 60).d}"/>`; };

/* ─────────────── 01 · THE POINT — a brilliant in profile that is also a pen nib ─────────────── */
// Crown to Tolkowsky's 1919 ideal (table 56%, crown 34.5°); pavilion at 45° so the silhouette
// doubles as a nib. The slit is the pavilion's centre line; the breather hole holds the red point:
// printers measure type in points, dealers weigh stones in points (1 pt = 0.01 ct).
function pointGeom({ pav = 45, table = 0.56, crown = 34.5, half = 400 } = {}) {
  const tw = half * table, ch = (half - tw) * Math.tan(deg(crown)), pd = half * Math.tan(deg(pav));
  return { half, tw, ch, pd, H: ch + pd };
}
function pointMarkup({ fg = C.ink, dot = C.seal, size = 'large', cx = 500, top = null } = {}) {
  const g = pointGeom(); top = top ?? (1000 - g.H) / 2 - 8;
  const P = (x, y) => [cx + x, top + y], small = size === 'small';
  const outline = poly([P(-g.tw, 0), P(g.tw, 0), P(g.half, g.ch), P(0, g.H), P(-g.half, g.ch)]);
  const k = small ? 30 : 11, hy = g.ch + g.pd * 0.33, hr = small ? 76 : 44, dr = small ? 48 : 27, fx = 0.36;
  let cuts = line(P(-g.half - 20, g.ch), P(g.half + 20, g.ch));
  if (!small) cuts += line(P(-g.tw, 0), P(-g.half * fx, g.ch)) + line(P(g.tw, 0), P(g.half * fx, g.ch)) + line(P(-g.half * fx, g.ch), P(0, g.H)) + line(P(g.half * fx, g.ch), P(0, g.H));
  cuts += line(P(0, hy + hr - 4), P(0, g.H + 30));
  const ko = knockout(`<path d="${outline}" fill="${fg}"/>`, `<path d="${cuts}" stroke="#000" stroke-width="${k}"/><circle cx="${r2(cx)}" cy="${r2(top + hy)}" r="${hr}" fill="#000"/>`, [cx - 500, top - 100, 1000, g.H + 200]);
  return { defs: ko.defs, body: ko.body + `<circle cx="${r2(cx)}" cy="${r2(top + hy)}" r="${dr}" fill="${dot}"/>`, g, top };
}
function pointSymbol(o = {}) { const m = pointMarkup(o); return svg('0 0 1000 1000', bgRect(o.bg) + m.body, m.defs); }
function pointLockup({ fg = C.ink, dot = C.seal, bg = 'none', tag = true } = {}) {
  const size = 200, f = 'bodoni500', tr = -8, b = inkBox(f, 'Carat Capital', size, tr), cap = inkBox(f, 'C', size).h;
  const symH = tag ? cap + 118 : cap * 1.3, g = pointGeom(), sc = symH / g.H, symW = g.half * 2 * sc, gap = size * 0.34;
  const x0 = 24, y0 = 24, tx = x0 + symW + gap, base = y0 + cap, W = tx + b.w + 26 + 17 + 30, H = y0 + symH + 24;
  const m = pointMarkup({ fg, dot, cx: 0, top: 0 });
  let body = bgRect(bg) + `<g transform="translate(${r2(x0 + symW / 2)} ${r2(y0)}) scale(${r2(sc * 10000) / 10000})">${m.body}</g>`;
  body += `<path fill="${fg}" d="${setText(f, 'Carat Capital', tx - b.x1, base, size, tr).d}"/><circle cx="${r2(tx + b.w + 26)}" cy="${r2(base - 17)}" r="17" fill="${dot}"/>`;
  if (tag) body += `<path fill="${fg}" opacity=".8" d="${setText('plexmono500', TAG, tx + 4, base + 118, 33, 262).d}"/>`;
  return svg(`0 0 ${r2(W)} ${r2(H)}`, body, m.defs);
}
function pointConstruction({ fg = C.ink, red = C.seal, faint = 'rgba(22,19,14,.3)' } = {}) {
  // a line drawing: guides, facet lines, angles and labels kept outside the stone
  const g = pointGeom(), cx = 500, top = 250, P = (x, y) => [cx + x, top + y], fx = 0.36, hy = g.ch + g.pd * 0.33, hr = 44;
  const TL = P(-g.tw, 0), TR = P(g.tw, 0), GR = P(g.half, g.ch), GL = P(-g.half, g.ch), CU = P(0, g.H);
  const arc = (p, r, a1, a2) => { const p1 = polar(p[0], p[1], r, deg(a1)), p2 = polar(p[0], p[1], r, deg(a2)); return `M${r2(p1[0])} ${r2(p1[1])}A${r} ${r} 0 0 ${a2 > a1 ? 1 : 0} ${r2(p2[0])} ${r2(p2[1])}`; };
  const guides = line([40, top], [960, top]) + line([40, top + g.ch], [960, top + g.ch]) + line([40, top + g.H], [960, top + g.H]) + line([40, top + hy], [960, top + hy]) + line([cx, top - 150], [cx, top + g.H + 40]);
  let o = `<path d="${guides}" stroke="${faint}" stroke-width="1.6" stroke-dasharray="5 7" fill="none"/>`;
  o += `<path d="${poly([TL, TR, GR, CU, GL])}" fill="none" stroke="${fg}" stroke-width="3.2" stroke-linejoin="miter"/>`;
  o += `<path d="${line(GL, GR) + line(TL, P(-g.half * fx, g.ch)) + line(TR, P(g.half * fx, g.ch)) + line(P(-g.half * fx, g.ch), CU) + line(P(g.half * fx, g.ch), CU) + line(P(0, hy + hr), CU)}" fill="none" stroke="${fg}" stroke-width="1.8"/>`;
  o += `<circle cx="${cx}" cy="${r2(top + hy)}" r="${hr}" fill="none" stroke="${fg}" stroke-width="1.8"/><circle cx="${cx}" cy="${r2(top + hy)}" r="27" fill="${red}"/>`;
  o += `<path d="${arc(GL, 120, -34.5, 0) + arc(GL, 165, 0, 45)}" stroke="${red}" stroke-width="2.6" fill="none"/>`;
  const tick = (x, y) => line([x, y - 12], [x, y + 12]);
  o += `<path d="${line([TL[0], top - 56], [TR[0], top - 56]) + tick(TL[0], top - 56) + tick(TR[0], top - 56) + line([GL[0], top - 112], [GR[0], top - 112]) + tick(GL[0], top - 112) + tick(GR[0], top - 112)}" stroke="${fg}" stroke-width="2"/>`;
  o += label('TABLE 56%', cx, top - 70, fg, 24, 'middle') + label('GIRDLE 100%', cx, top - 126, fg, 24, 'middle');
  o += label('CROWN 34.5°', GL[0] + 10, GL[1] - 150, red, 24) + label('PAVILION 45°', GL[0] - 60, GL[1] + 200, red, 24);
  o += label('THE POINT', 790, top + hy - 6, fg, 24) + label('1/3 DEPTH', 790, top + hy + 26, fg, 24) + label('THE SLIT', cx + 36, top + g.H - 8, fg, 24);
  return svg('0 0 1000 850', o, '');
}

/* ─────────────── 02 · THE HALLMARK — the maker's mark C◆C ─────────────── */
// Before there were logos there were makers' marks: initials struck into metal inside a shaped punch.
function cartouche(x, y, w, h, k) { return poly([[x + k, y], [x + w - k, y], [x + w, y + k], [x + w, y + h - k], [x + w - k, y + h], [x + k, y + h], [x, y + h - k], [x, y + k]]); }
function hallmarkMarkup({ field = C.ink, pellet = C.seal, foil = false } = {}) {
  const f = 'bodoni700', size = 520, b = inkBox(f, 'C', size), base = 310 - b.h / 2 - b.y1;
  const cL = setText(f, 'C', 210 - b.x1, base, size).d, cR = setText(f, 'C', 990 - b.w - b.x1, base, size).d;
  const px = 600, py = 318, pr = 62, pel = poly([[px, py - pr * 1.18], [px + pr * 0.82, py], [px, py + pr * 1.18], [px - pr * 0.82, py]]);
  const gid = uid('f');
  const ko = knockout(`<path d="${cartouche(20, 20, 1160, 580, 92)}" fill="${foil ? `url(#${gid})` : field}"/>`,
    `<path d="${cartouche(52, 52, 1096, 516, 79)}" fill="none" stroke="#000" stroke-width="7"/><path d="${cL}${cR}${pel}" fill="#000"/>`, [0, 0, 1200, 620]);
  return { defs: (foil ? foilGrad(gid, 0, 0, 1, 1) : '') + ko.defs, body: ko.body + `<path d="${pel}" fill="${pellet}"/>` };
}
function hallmarkSymbol(o = {}) { const m = hallmarkMarkup(o); return svg('0 0 1200 620', bgRect(o.bg) + m.body, m.defs); }
function hallmarkLockup({ fg = C.ink, bg = 'none', pellet = C.seal, foil = false } = {}) {
  const m = hallmarkMarkup({ field: fg, pellet, foil });
  const f = 'castorotitling', size = 150, tr = 150, wm = inkBox(f, 'CARAT CAPITAL', size, tr), tb = inkBox('plexmono500', TAG, 29.5, 322);
  const s = 0.42, symW = 1200 * s, symH = 620 * s, gap = 72, H = symH + 48, tx = 24 + symW + gap;
  const base = 24 + (symH - (wm.h + 66)) / 2 + wm.h, W = tx + Math.max(wm.w, tb.w) + 24;
  return svg(`0 0 ${r2(W)} ${r2(H)}`, bgRect(bg) + `<g transform="translate(24 24) scale(${s})">${m.body}</g>` +
    `<path fill="${fg}" d="${setText(f, 'CARAT CAPITAL', tx - wm.x1, base, size, tr).d}"/>` +
    `<path fill="${fg}" opacity=".8" d="${setText('plexmono500', TAG, tx - tb.x1 + 2, base + 66, 29.5, 322).d}"/>`, m.defs);
}
// The strip: sponsor (C◆C) · "fineness" = edition number · office = the point · date letter.
function hallmarkStrip({ fg = C.ink, red = C.seal, edition = '072', letter = 'a' } = {}) {
  const h = 200; let x = 0, out = '', defs = '';
  const sp = hallmarkMarkup({ field: fg, pellet: red }); defs += sp.defs; out += `<g transform="scale(${r2((h / 620) * 10000) / 10000})">${sp.body}</g>`; x += 1200 * (h / 620) + 24;
  const fw = 300, eb = inkBox('bodoni700', edition, 118, 20);
  let ko = knockout(`<ellipse cx="${x + fw / 2}" cy="${h / 2}" rx="${fw / 2 - 6}" ry="${h / 2 - 6}" fill="${fg}"/>`,
    `<ellipse cx="${x + fw / 2}" cy="${h / 2}" rx="${fw / 2 - 19}" ry="${h / 2 - 19}" fill="none" stroke="#000" stroke-width="3.5"/><path fill="#000" d="${setText('bodoni700', edition, x + fw / 2 - eb.x1 - eb.w / 2, h / 2 + eb.h / 2 - eb.y2, 118, 20).d}"/>`, [0, 0, 2000, h]);
  defs += ko.defs; out += ko.body; x += fw + 24;
  const sw = 186, shield = `M${x} 6H${x + sw}V${h * 0.55}Q${x + sw} ${h - 10} ${x + sw / 2} ${h - 5}Q${x} ${h - 10} ${x} ${h * 0.55}Z`, pg = pointGeom(), sc = 0.16;
  const sy = h / 2 - (pg.H * sc) / 2 - 8;
  ko = knockout(`<path d="${shield}" fill="${fg}"/>`, `<g transform="translate(${x + sw / 2} ${r2(sy)}) scale(${sc})"><path d="${poly([[-pg.tw, 0], [pg.tw, 0], [pg.half, pg.ch], [0, pg.H], [-pg.half, pg.ch]])}" fill="#000"/></g>`, [0, 0, 2000, h]);
  defs += ko.defs; out += ko.body + `<circle cx="${r2(x + sw / 2)}" cy="${r2(sy + (pg.ch + pg.pd * 0.33) * sc)}" r="8" fill="${red}"/>`; x += sw + 24;
  const lw = 186, lb = inkBox('bodoni700', letter, 150);
  ko = knockout(`<path d="${cartouche(x, 6, lw, h - 12, 34)}" fill="${fg}"/>`, `<path fill="#000" d="${setText('bodoni700', letter, x + lw / 2 - lb.x1 - lb.w / 2, h / 2 + lb.h / 2 - lb.y2, 150).d}"/>`, [0, 0, 2000, h]);
  defs += ko.defs; out += ko.body; x += lw;
  return svg(`0 0 ${r2(x)} ${h}`, out, defs);
}

/* ─────────────── 03 · THE STEP CUT — an emerald cut with a slot in its side: a C ─────────────── */
function stepCutMarkup({ fg = C.ink, gold = false, lines = 3, kw = 9 } = {}) {
  const x0 = 170, x1 = 830, y0 = 95, y1 = 905, k = 205, T = 172, s2 = Math.SQRT2 - 1;
  const ring = (t) => ({ a: x0 + t, b: x1 - t, c: y0 + t, d: y1 - t, kk: k - t * s2 });
  const n = ring(T), termTop = n.c + n.kk, termBot = n.d - n.kk;
  const outer = poly([[x1, termTop], [x1, y0 + k], [x1 - k, y0], [x0 + k, y0], [x0, y0 + k], [x0, y1 - k], [x0 + k, y1], [x1 - k, y1], [x1, y1 - k], [x1, termBot],
    [n.b, termBot], [n.b - n.kk, n.d], [n.a + n.kk, n.d], [n.a, n.d - n.kk], [n.a, n.c + n.kk], [n.a + n.kk, n.c], [n.b - n.kk, n.c], [n.b, termTop]]);
  let cuts = '';
  for (let i = 1; i < lines; i++) {
    const r = ring((T * i) / lines);
    cuts += `M${r2(r.b)} ${r2(termTop + 40)}L${r2(r.b)} ${r2(r.c + r.kk)}L${r2(r.b - r.kk)} ${r2(r.c)}L${r2(r.a + r.kk)} ${r2(r.c)}L${r2(r.a)} ${r2(r.c + r.kk)}L${r2(r.a)} ${r2(r.d - r.kk)}L${r2(r.a + r.kk)} ${r2(r.d)}L${r2(r.b - r.kk)} ${r2(r.d)}L${r2(r.b)} ${r2(r.d - r.kk)}L${r2(r.b)} ${r2(termBot - 40)}`;
  }
  const O = [[x1 - k, y0], [x0 + k, y0], [x0, y0 + k], [x0, y1 - k], [x0 + k, y1], [x1 - k, y1], [x1, y0 + k], [x1, y1 - k]];
  const I = [[n.b - n.kk, n.c], [n.a + n.kk, n.c], [n.a, n.c + n.kk], [n.a, n.d - n.kk], [n.a + n.kk, n.d], [n.b - n.kk, n.d], [n.b, n.c + n.kk], [n.b, n.d - n.kk]];
  O.forEach((o, i) => { cuts += line(o, I[i]); });
  const gid = uid('g');
  const ko = knockout(`<path d="${outer}" fill="${gold ? `url(#${gid})` : fg}"/>`, kw > 0 ? `<path d="${cuts}" fill="none" stroke="#000" stroke-width="${kw}" stroke-linecap="square"/>` : '');
  return { defs: (gold ? foilGrad(gid, 0, 0, 1, 1) : '') + ko.defs, body: ko.body, outer, cuts };
}
function stepCutSymbol(o = {}) { const m = stepCutMarkup(o); return svg('0 0 1000 1000', bgRect(o.bg) + m.body, m.defs); }
// Bespoke titling for the seven letters of the name (C A R T P I L): octagonal, step-cut corners.
function decoGlyphs(Hc = 200, w = 22) {
  const h = w / 2, c = Hc * 0.23, c2 = Hc * 0.17, ov = 40, G = {}, U = Hc / 200;
  const Wc = 150 * U; G.C = { w: Wc, p: [[[Wc - h, h + c + 14 * U], [Wc - h, h + c], [Wc - h - c, h], [h + c, h], [h, h + c], [h, Hc - h - c], [h + c, Hc - h], [Wc - h - c, Hc - h], [Wc - h, Hc - h - c], [Wc - h, Hc - h - c - 14 * U]]] };
  const Wa = 170 * U, ah = 13 * U, cb = Hc * 0.66, lx = (y) => h + 2 + ((Wa / 2 - ah - h - 2) * (Hc + ov - y)) / (Hc + ov - h);
  G.A = { w: Wa, p: [[[h + 2, Hc + ov], [Wa / 2 - ah, h], [Wa / 2 + ah, h], [Wa - h - 2, Hc + ov]], [[lx(cb), cb], [Wa - lx(cb), cb]]] };
  const yb = Hc * 0.56, bowl = (W) => [[h, Hc + ov], [h, h], [W - h - c2, h], [W - h, h + c2], [W - h, yb - c2], [W - h - c2, yb], [h, yb]];
  G.P = { w: 140 * U, p: [bowl(140 * U)] };
  G.R = { w: 146 * U, p: [bowl(146 * U), [[146 * U * 0.5, yb], [146 * U - h, Hc + ov]]] };
  G.T = { w: 150 * U, p: [[[0, h], [150 * U, h]], [[75 * U, h], [75 * U, Hc + ov]]] };
  G.I = { w: w, p: [[[h, -ov], [h, Hc + ov]]] };
  G.L = { w: 122 * U, p: [[[h, -ov], [h, Hc - h], [122 * U, Hc - h]]] };
  G[' '] = { w: 110 * U, p: [] };
  return G;
}
function decoWord(str, { Hc = 200, w = 22, gap = 70, fg = C.ink, x = 0, y = 0 } = {}) {
  const G = decoGlyphs(Hc, w); let cx = x, d = '';
  [...str].forEach((ch, i) => {
    const g = G[ch], nx = str[i + 1];
    g.p.forEach((pl) => { d += 'M' + pl.map((q) => `${r2(cx + q[0])} ${r2(y + q[1])}`).join('L'); });
    let adv = g.w + (ch === ' ' ? 0 : gap);
    if ((ch === 'A' && nx === 'T') || (ch === 'T' && nx === 'A')) adv -= 26 * (Hc / 200);
    cx += adv;
  });
  const width = cx - x - gap, id = uid('c');
  return { width, defs: `<clipPath id="${id}"><rect x="${r2(x - 50)}" y="${r2(y)}" width="${r2(width + 100)}" height="${Hc}"/></clipPath>`,
    body: `<path clip-path="url(#${id})" d="${d}" fill="none" stroke="${fg}" stroke-width="${w}" stroke-linejoin="miter" stroke-miterlimit="8"/>` };
}
function stepCutLockup({ fg = C.ink, bg = 'none', gold = false, stacked = false } = {}) {
  const m = stepCutMarkup({ fg, gold });
  if (!stacked) { // the stone spans both lines of the name
    const Hc = 150, lg = 64, blockH = Hc * 2 + lg, s = blockH / 810, pad = 24, tx = pad + 660 * s + 66;
    const A = decoWord('CARAT', { fg, x: tx, y: pad, Hc, w: 17, gap: 52 }), B = decoWord('CAPITAL', { fg, x: tx, y: pad + Hc + lg, Hc, w: 17, gap: 52 });
    const W = tx + Math.max(A.width, B.width) + pad, H = blockH + pad * 2;
    return svg(`0 0 ${r2(W)} ${r2(H)}`, bgRect(bg) + `<g transform="translate(${r2(pad - 170 * s)} ${r2(pad - 95 * s)}) scale(${r2(s * 10000) / 10000})">${m.body}</g>${A.body}${B.body}`, m.defs + A.defs + B.defs);
  }
  const Hc = 120, D0 = decoWord('CARAT CAPITAL', { Hc, w: 14, gap: 46 }), W = D0.width + 60, s = 0.5, symH = 810 * s;
  const D = decoWord('CARAT CAPITAL', { fg, x: 30, y: 30 + symH + 70, Hc, w: 14, gap: 46 });
  return svg(`0 0 ${r2(W)} ${r2(30 + symH + 70 + Hc + 30)}`, bgRect(bg) + `<g transform="translate(${r2(W / 2 - 500 * s)} ${r2(30 - 95 * s)}) scale(${s})">${m.body}</g>${D.body}`, m.defs + D.defs);
}
function stepCutConstruction({ fg = C.ink, red = C.seal, faint = 'rgba(22,19,14,.3)' } = {}) {
  const m = stepCutMarkup({ fg, kw: 0 });
  let o = `<path d="M170 95H830V905H170Z M500 30V970 M60 500H940" fill="none" stroke="${faint}" stroke-width="1.6" stroke-dasharray="5 7"/>`;
  o += `<path d="${m.outer}" fill="none" stroke="${fg}" stroke-width="3"/><path d="${m.cuts}" fill="none" stroke="${red}" stroke-width="2.2"/>`;
  o += label('EMERALD CUT 1 : 1.23', 170, 64, fg, 28) + label('3 STEPS', 846, 548, red, 24) + label('45° KEELS', 846, 584, red, 24) + label('TABLE = COUNTER', 470, 510, fg, 28, 'middle');
  return svg('0 0 1000 1000', o, '');
}

/* ─────────────── 04 · THE SOLIDUS — twenty-four seeds, one stone ─────────────── */
function seed(cx, cy, len, wid, rot) { const a = len / 2, b = wid / 2;
  return `<path transform="translate(${r2(cx)} ${r2(cy)}) rotate(${r2(rot)})" d="M${-a} 0C${-a} ${r2(-b * 1.05)} ${r2(a * 0.2)} ${r2(-b * 1.12)} ${r2(a * 0.72)} ${r2(-b * 0.62)}C${r2(a * 1.02)} ${r2(-b * 0.32)} ${r2(a * 1.02)} ${r2(b * 0.32)} ${r2(a * 0.72)} ${r2(b * 0.62)}C${r2(a * 0.2)} ${r2(b * 1.12)} ${-a} ${r2(b * 1.05)} ${-a} 0Z"/>`; }
function solidusSeal({ fg = C.ink, red = C.seal, bg = 'none', detail = 'full', legendTop = 'CARAT  CAPITAL', legendBot = 'PONDERE · ET · FIDE' } = {}) {
  const cx = 500, cy = 500, full = detail === 'full'; let body = bgRect(bg), defs = '';
  body += `<circle cx="${cx}" cy="${cy}" r="490" fill="none" stroke="${fg}" stroke-width="12"/>`;
  let ticks = ''; const N = full ? 144 : 96;
  for (let i = 0; i < N; i++) { const a = (i / N) * Math.PI * 2; ticks += line(polar(cx, cy, 462, a), polar(cx, cy, 480, a)); }
  body += `<path d="${ticks}" stroke="${fg}" stroke-width="${full ? 5.2 : 7}"/><circle cx="${cx}" cy="${cy}" r="453" fill="none" stroke="${fg}" stroke-width="${full ? 3 : 5}"/>`;
  body += `<g fill="${fg}">${arcText('castorotitling', legendTop, cx, cy, 374, 84, 190, 'top')}${arcText('castorotitling', legendBot, cx, cy, 432, 58, 260, 'bottom')}</g>`;
  [90, 270].forEach((a) => { const [x, y] = polar(cx, cy, 404, deg(a - 90)); body += `<path fill="${red}" d="${poly([[x, y - 17], [x + 10, y], [x, y + 17], [x - 10, y]])}"/>`; });
  body += `<circle cx="${cx}" cy="${cy}" r="356" fill="none" stroke="${fg}" stroke-width="${full ? 3 : 5}"/>`;
  let seeds = '';
  for (let i = 0; i < 24; i++) { const a = (i / 24) * Math.PI * 2 - Math.PI / 2, [x, y] = polar(cx, cy, 328, a); seeds += seed(x, y, 40, 25, (a * 180) / Math.PI + 90); }
  body += `<g fill="${fg}">${seeds}</g><circle cx="${cx}" cy="${cy}" r="300" fill="none" stroke="${fg}" stroke-width="${full ? 3 : 5}"/>`;
  const R = 272, B = brilliantTop(cx, cy, R);
  if (full) { // each facet hatched at its own angle and density: the stone scintillates in pure line
    const F = B.facets, add = (h) => { defs += h.defs; body += h.body; };
    add(hatch(F.table[0], 0, 11, 1.5, fg));
    F.stars.forEach((p, k) => add(hatch(p, k * 45 + 22.5, 6.5, 1.6, fg)));
    F.kites.forEach((p, k) => add(hatch(p, k * 45 + (k % 2 ? 90 : 0), k % 2 ? 4.2 : 9, k % 2 ? 2.2 : 1.4, fg)));
    F.ugirdle.forEach((p, k) => add(hatch(p, Math.floor(k / 2) * 45 + (k % 2 ? 60 : -60), k % 2 === Math.floor(k / 2) % 2 ? 4.2 : 8, 1.7, fg)));
  }
  body += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="${fg}" stroke-width="${full ? 5 : 7}"/><path d="${B.lines.join('')}" fill="none" stroke="${fg}" stroke-width="${full ? 3.4 : 6.5}" stroke-linejoin="round"/>`;
  body += `<circle cx="${cx}" cy="${cy}" r="${full ? 13 : 20}" fill="${red}"/>`;
  return svg('0 0 1000 1000', body, defs);
}

/* ─────────────── 05 · THE INSERTION — the caret is a stone laid table-down ─────────────── */
// Dealers lay loose stones on the paper table-down; seen side-on, the pavilion rises to the culet —
// the proofreader's caret. The nameplate inserts one stone between its two words.
function tableDown(x, base, h, color, kw = 0.035) {
  const half = h * 0.56, tw = half * 0.56, crH = (half - tw) * Math.tan(deg(34.5)), fx = half * 0.36;
  const P = [[x - tw, base], [x + tw, base], [x + half, base - crH], [x, base - h], [x - half, base - crH]];
  const cuts = line([x - half - 5, base - crH], [x + half + 5, base - crH]) + line([x - tw, base], [x - fx, base - crH]) + line([x + tw, base], [x + fx, base - crH]) + line([x - fx, base - crH], [x, base - h]) + line([x + fx, base - crH], [x, base - h]);
  return knockout(`<path d="${poly(P)}" fill="${color}"/>`, `<path d="${cuts}" stroke="#000" stroke-width="${r2(h * kw)}" fill="none"/>`, [x - h, base - h * 1.2, h * 2, h * 1.4]);
}
function insertionNameplate({ fg = C.ink, red = C.seal, bg = 'none', rule = true } = {}) {
  const f = 'gloock', size = 300, tr = 10, a = inkBox(f, 'CARAT', size, tr), b = inkBox(f, 'CAPITAL', size, tr);
  const capH = a.h, gap = capH * 0.52, x0 = 30, caretX = x0 + a.w + gap, Bx = caretX + gap - b.x1, W = Bx + b.x2 + 30, top = capH + 40;
  const st = tableDown(caretX, 0, capH * 0.6, red);
  let body = bgRect(bg) + `<g transform="translate(0 ${r2(top)})"><path fill="${fg}" d="${setText(f, 'CARAT', x0 - a.x1, 0, size, tr).d}${setText(f, 'CAPITAL', Bx, 0, size, tr).d}"/>${st.body}`;
  if (rule) {
    const ty = 88, tb = inkBox('plexmono500', TAG, 30, 420);
    body += `<path d="M30 ${ty - 11}H${r2(W / 2 - tb.w / 2 - 34)}M${r2(W / 2 + tb.w / 2 + 34)} ${ty - 11}H${r2(W - 30)}" stroke="${fg}" stroke-width="2.4"/>`;
    body += `<path fill="${fg}" d="${setText('plexmono500', TAG, W / 2 - tb.x1 - tb.w / 2, ty, 30, 420).d}"/>`;
  }
  return svg(`0 0 ${r2(W)} ${r2(top + (rule ? 120 : 40))}`, body + `</g>`, st.defs);
}
function insertionMonogram({ fg = C.ink, red = C.seal, bg = 'none', stone = null } = {}) {
  const f = 'gloock', size = 1000, b = inkBox(f, 'C', size), base = 500 + b.h / 2 - 14, x = 500 - b.w / 2 - b.x1 - 24;
  const st = tableDown(x + b.x1 + b.w * 0.6, base - b.h * 0.035, b.h * 0.33, stone || red, 0.045);
  return svg('0 0 1000 1000', bgRect(bg) + `<path fill="${fg}" d="${setText(f, 'C', x, base, size).d}"/>` + st.body, st.defs);
}

module.exports = { pointSymbol, pointLockup, pointConstruction, pointGeom, hallmarkSymbol, hallmarkLockup, hallmarkStrip, stepCutSymbol, stepCutLockup, stepCutConstruction, decoWord, solidusSeal, insertionNameplate, insertionMonogram, tableDown, TAG };
