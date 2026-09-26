// Shared helpers: palette, outlined type (opentype.js), arc legends, gem geometry.
const opentype = require('opentype.js');
const path = require('path');

const C = {
  paper: '#F2EDE3', paperHi: '#F8F4EB', ink: '#16130E', ink2: '#3B362C', ink3: '#7A7263',
  seal: '#BE3319', sealDeep: '#93250F', gilt: '#96762E',
  foilA: '#7A5E1F', foilB: '#D9B45E', foilC: '#F1DFA4', foilD: '#8A6C28',
};

const fontCache = {};
function font(name) {
  if (!fontCache[name]) fontCache[name] = opentype.loadSync(path.join(__dirname, 'fonts', name + '.ttf'));
  return fontCache[name];
}

const r2 = (n) => Math.round(n * 100) / 100;
const deg = (a) => (a * Math.PI) / 180;

// Lay out a string with kerning + tracking (tracking in em/1000). Returns {d, width}.
function setText(fontName, str, x, y, size, tracking = 0) {
  const f = font(fontName);
  const glyphs = f.stringToGlyphs(str);
  const scale = size / f.unitsPerEm;
  let cx = x, d = '';
  glyphs.forEach((g, i) => {
    d += g.getPath(cx, y, size).toPathData(2);
    cx += g.advanceWidth * scale;
    if (i < glyphs.length - 1) cx += f.getKerningValue(g, glyphs[i + 1]) * scale + (tracking / 1000) * size;
  });
  return { d, width: cx - x };
}
function textWidth(fontName, str, size, tracking = 0) { return setText(fontName, str, 0, 0, size, tracking).width; }
// Optical bounding box of a string (ink extents), useful for centring.
function inkBox(fontName, str, size, tracking = 0) {
  const f = font(fontName); const glyphs = f.stringToGlyphs(str); const scale = size / f.unitsPerEm;
  let cx = 0, x1 = Infinity, x2 = -Infinity, y1 = Infinity, y2 = -Infinity;
  glyphs.forEach((g, i) => {
    const bb = g.getPath(cx, 0, size).getBoundingBox();
    if (bb.x1 !== bb.x2) { x1 = Math.min(x1, bb.x1); x2 = Math.max(x2, bb.x2); y1 = Math.min(y1, bb.y1); y2 = Math.max(y2, bb.y2); }
    cx += g.advanceWidth * scale;
    if (i < glyphs.length - 1) cx += f.getKerningValue(g, glyphs[i + 1]) * scale + (tracking / 1000) * size;
  });
  return { x1, x2, y1, y2, w: x2 - x1, h: y2 - y1, adv: cx };
}
// Centre a string horizontally on cx by its ink box.
function centeredText(fontName, str, cx, y, size, tracking = 0) {
  const b = inkBox(fontName, str, size, tracking);
  return setText(fontName, str, cx - (b.x1 + b.w / 2), y, size, tracking).d;
}

// Legend on a circle. where='top': reads clockwise, letters stand outward from baseline radius r.
// where='bottom': reads left→right along the bottom, letters hang inward from baseline radius r.
function arcText(fontName, str, cx, cy, r, size, tracking = 0, where = 'top', centerDeg = null) {
  const f = font(fontName); const glyphs = f.stringToGlyphs(str); const scale = size / f.unitsPerEm;
  const advs = glyphs.map((g, i) => g.advanceWidth * scale +
    (i < glyphs.length - 1 ? f.getKerningValue(g, glyphs[i + 1]) * scale + (tracking / 1000) * size : 0));
  const total = advs.reduce((a, b) => a + b, 0);
  const span = total / r; // radians
  let out = '', s = 0;
  glyphs.forEach((g, i) => {
    const w = g.advanceWidth * scale;
    const mid = (s + w / 2) / r - span / 2; // radians from centre of legend
    s += advs[i];
    if (where === 'top') {
      const th = mid + deg(centerDeg ?? 0);
      const px = cx + r * Math.sin(th), py = cy - r * Math.cos(th);
      out += `<path transform="translate(${r2(px)} ${r2(py)}) rotate(${r2((th * 180) / Math.PI)})" d="${g.getPath(-w / 2, 0, size).toPathData(2)}"/>`;
    } else {
      const ps = mid + deg(centerDeg ?? 0);
      const px = cx + r * Math.sin(ps), py = cy + r * Math.cos(ps);
      out += `<path transform="translate(${r2(px)} ${r2(py)}) rotate(${r2((-ps * 180) / Math.PI)})" d="${g.getPath(-w / 2, 0, size).toPathData(2)}"/>`;
    }
  });
  return out;
}

const pts = (arr) => arr.map((p) => `${r2(p[0])},${r2(p[1])}`).join(' ');
const poly = (arr) => 'M' + arr.map((p) => `${r2(p[0])} ${r2(p[1])}`).join('L') + 'Z';
const line = (a, b) => `M${r2(a[0])} ${r2(a[1])}L${r2(b[0])} ${r2(b[1])}`;
const polar = (cx, cy, r, a) => [cx + r * Math.cos(a), cy + r * Math.sin(a)];

// Round brilliant, top view. Angles in radians, 0 = east, y down. Table has a vertex pointing north.
function brilliantTop(cx, cy, R, { table = 0.56, star = 0.5 } = {}) {
  const off = -Math.PI / 2; // vertex at north
  const tv = [], st = [], gk = [], gs = [];
  const rt = R * table; // table circumradius
  const rEdge = rt * Math.cos(Math.PI / 8);
  const rs = rEdge + (R - rEdge) * star;
  for (let k = 0; k < 8; k++) {
    const a = off + (k * Math.PI) / 4, b = a + Math.PI / 8;
    tv.push(polar(cx, cy, rt, a)); gk.push(polar(cx, cy, R, a));
    st.push(polar(cx, cy, rs, b)); gs.push(polar(cx, cy, R, b));
  }
  const facets = { table: [tv], stars: [], kites: [], ugirdle: [] };
  for (let k = 0; k < 8; k++) {
    const n = (k + 1) % 8, p = (k + 7) % 8;
    facets.stars.push([tv[k], st[k], tv[n]]);
    facets.kites.push([tv[k], st[k], gk[k], st[p]]);
    // two upper-girdle facets between kite k and kite n, split at gs[k]
    facets.ugirdle.push([st[k], gk[k], gs[k]]);
    facets.ugirdle.push([st[k], gs[k], gk[n]]);
  }
  const lines = [];
  for (let k = 0; k < 8; k++) {
    const n = (k + 1) % 8;
    lines.push(line(tv[k], tv[n]), line(tv[k], st[k]), line(st[k], tv[n]), line(st[k], gk[k]), line(st[k], gk[n]), line(st[k], gs[k]));
  }
  return { tv, st, gk, gs, facets, lines };
}

// Hatch a polygon with parallel lines (engraving). Returns <g> using a clipPath with a unique id.
let clipN = 0;
function hatch(polyPts, angleDeg, spacing, width, color, extra = '') {
  const id = 'h' + clipN++;
  const xs = polyPts.map((p) => p[0]), ys = polyPts.map((p) => p[1]);
  const cx = (Math.min(...xs) + Math.max(...xs)) / 2, cy = (Math.min(...ys) + Math.max(...ys)) / 2;
  const L = Math.hypot(Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys)) / 2 + spacing;
  const a = deg(angleDeg), ux = Math.cos(a), uy = Math.sin(a), nx = -uy, ny = ux;
  let d = '';
  for (let t = -L; t <= L; t += spacing) {
    const px = cx + nx * t, py = cy + ny * t;
    d += line([px - ux * L, py - uy * L], [px + ux * L, py + uy * L]);
  }
  return { defs: `<clipPath id="${id}"><path d="${poly(polyPts)}"/></clipPath>`,
    body: `<path clip-path="url(#${id})" d="${d}" stroke="${color}" stroke-width="${width}" fill="none" ${extra}/>` };
}

const svg = (vb, body, defs = '', extra = '') =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}" ${extra}>${defs ? `<defs>${defs}</defs>` : ''}${body}</svg>`;

const foilGrad = (id, x1 = 0, y1 = 0, x2 = 1, y2 = 1) =>
  `<linearGradient id="${id}" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}"><stop offset="0" stop-color="${C.foilA}"/><stop offset=".38" stop-color="${C.foilB}"/><stop offset=".55" stop-color="${C.foilC}"/><stop offset=".72" stop-color="${C.foilB}"/><stop offset="1" stop-color="${C.foilD}"/></linearGradient>`;

module.exports = { C, font, r2, deg, setText, textWidth, inkBox, centeredText, arcText, pts, poly, line, polar, brilliantTop, hatch, svg, foilGrad };
