// The Carat Capital Brand Book (The Point, edition 1.0): HTML for the repo + artifact, and a PDF.
const path = require('path'); const BUILD = path.join(__dirname, 'build'); const BRAND = path.join(__dirname, '..');
const Pn = require('./point'); const R = require('./routes'); const L = require('./lib'); const fs = require('fs');
const { C, r2, line, poly } = L; const { G } = Pn;
const P = C.paper, I = C.ink, RED = C.seal, GOLD = C.foilB;
const inl = (s, cls = '') => s.replace('<svg', `<svg class="${cls}" aria-hidden="true"`);
const b64 = (f, t) => `data:${t};base64,${fs.readFileSync(f).toString('base64')}`;
const inner = (s) => s.replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '');
const vbOf = (s) => s.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
const nest = (s, x, y, w) => { const [, , vw, vh] = vbOf(s); return `<svg x="${r2(x)}" y="${r2(y)}" width="${r2(w)}" height="${r2((w * vh) / vw)}" viewBox="0 0 ${vw} ${vh}">${inner(s)}</svg>`; };
const T = (s, x, y, o = {}) => `<text x="${r2(x)}" y="${r2(y)}" font-family="IBM Plex Mono, monospace" font-size="${o.size || 17}" font-weight="500" letter-spacing="${o.ls || 1.6}" fill="${o.fill || I}" text-anchor="${o.a || 'start'}">${s}</text>`;
const halo = (d, col = I) => `<path d="${d}" stroke="${P}" stroke-width="5" fill="none" stroke-linecap="round"/><path d="${d}" stroke="${col}" stroke-width="1.5" fill="none"/>`;

// ── diagrams ──
function anatomy() {
  const s = 0.78, ox = 70, oy = 120, X = (x) => ox + (400 + x) * s, Y = (y) => oy + y * s;
  const m = Pn.mark({ cut: 'L', cx: 400, top: 0 });
  let o = `<g transform="translate(${ox} ${oy}) scale(${s})">${m.body}</g>`;
  const R_ = [['TABLE', X(120), Y(0), Y(0)], ['CROWN', X(300), Y(G.ch * 0.55), Y(G.ch * 0.55)], ['GIRDLE', X(G.half), Y(G.ch), Y(G.ch) + 14], ['PAVILION', X(250), Y(G.ch + 150), Y(G.ch + 150)]];
  R_.forEach(([t, x, y, ly]) => { o += halo(`M${r2(x)} ${r2(y)}L${r2(x + 30)} ${r2(ly)}L770 ${r2(ly)}`) + `<circle cx="${r2(x)}" cy="${r2(y)}" r="4" fill="${I}" stroke="${P}" stroke-width="2"/>` + T(t, 782, ly + 6); });
  const Lf = [['THE POINT', X(0), Y(G.hy), Y(G.hy), RED], ['THE SLIT', X(0), Y(G.H - 70), Y(G.H - 70), I]];
  Lf.forEach(([t, x, y, ly, col]) => { o += halo(`M${r2(x)} ${r2(y)}L${r2(x - 40)} ${r2(ly)}L118 ${r2(ly)}`, col) + `<circle cx="${r2(x)}" cy="${r2(y)}" r="4" fill="${col}" stroke="${P}" stroke-width="2"/>` + T(t, 106, ly + 6, { a: 'end', fill: col }); });
  return `<svg viewBox="-40 60 1040 520" aria-hidden="true"><defs>${m.defs}</defs>${o}</svg>`;
}
function reading(kind) { // three small line drawings: stone, pen, point
  const s = 0.34, ox = 150, oy = 60, X = (x) => ox + x * s, Y = (y) => oy + y * s;
  const out = poly([[X(-G.tw), Y(0)], [X(G.tw), Y(0)], [X(G.half), Y(G.ch)], [X(0), Y(G.H)], [X(-G.half), Y(G.ch)]]);
  const fac = line([X(-G.half), Y(G.ch)], [X(G.half), Y(G.ch)]) + line([X(-G.tw), Y(0)], [X(-G.fx), Y(G.ch)]) + line([X(G.tw), Y(0)], [X(G.fx), Y(G.ch)]) + line([X(-G.fx), Y(G.ch)], [X(0), Y(G.H)]) + line([X(G.fx), Y(G.ch)], [X(0), Y(G.H)]);
  const slit = line([X(0), Y(G.hy + 16)], [X(0), Y(G.H)]);
  let o = '';
  if (kind === 'stone') o = `<path d="${out}" fill="none" stroke="${I}" stroke-width="2.2"/><path d="${fac}" fill="none" stroke="${I}" stroke-width="1.2"/>`;
  if (kind === 'pen') o = `<path d="${out}" fill="none" stroke="${I}" stroke-width="1.2" opacity=".35"/><path d="${fac}" fill="none" stroke="${I}" stroke-width="1" opacity=".25"/><path d="${slit}" stroke="${I}" stroke-width="2.4"/><circle cx="${X(0)}" cy="${Y(G.hy)}" r="15" fill="none" stroke="${I}" stroke-width="2.4"/><path d="${line([X(-G.fx), Y(G.ch)], [X(0), Y(G.H)]) + line([X(G.fx), Y(G.ch)], [X(0), Y(G.H)])}" stroke="${I}" stroke-width="2.2"/>`;
  if (kind === 'point') o = `<path d="${out}" fill="none" stroke="${I}" stroke-width="1.2" opacity=".25"/><circle cx="${X(0)}" cy="${Y(G.hy)}" r="19" fill="${RED}"/>`;
  return `<svg viewBox="0 30 300 240" aria-hidden="true">${o}</svg>`;
}
function wordmarkSpec() {
  const W = Pn.wordmark({ cut: 'display', size: 200, x: 200, base: 250 }), cap = W.cap, px = 200 + W.w - 16;
  let o = `<path d="M20 250H${r2(W.w + 230)}M20 ${r2(250 - cap)}H${r2(W.w + 230)}M20 ${r2(250 + W.desc)}H${r2(W.w + 230)}" stroke="${I}" stroke-opacity=".28" stroke-width="1.4" stroke-dasharray="5 6"/>` + W.body;
  o += `<circle cx="${r2(px)}" cy="234" r="30" fill="none" stroke="${RED}" stroke-width="1.6"/>` + halo(`M${r2(px + 22)} 214L${r2(px + 60)} 150L${r2(px + 80)} 150`, RED);
  o += T('BASELINE', 20, 243, { size: 14, fill: C.ink3 }) + T('CAP HEIGHT', 20, r2(250 - cap - 8), { size: 14, fill: C.ink3 }) + T('DESCENDER', 20, r2(250 + W.desc - 8), { size: 14, fill: C.ink3 });
  o += T('THE POINT', px + 88, 146, { size: 15, fill: RED }) + T('0.16 EM · ON THE BASELINE', px + 88, 168, { size: 12, fill: RED });
  return `<svg viewBox="0 30 ${r2(W.w + 580)} 290" aria-hidden="true">${o}</svg>`;
}
function clearSpace() {
  const s = Pn.lockup({}), [, , vw, vh] = vbOf(s), cap = Pn.wordmark({ size: 200 }).cap, pad = cap * 0.5, x = cap;
  const bx = pad - x, by = pad - x, bw = vw - 2 * pad + 2 * x, bh = vh - 2 * pad + 2 * x;
  let o = `<rect x="${r2(bx)}" y="${r2(by)}" width="${r2(bw)}" height="${r2(bh)}" fill="${C.paperHi}" stroke="${RED}" stroke-width="2.4" stroke-dasharray="10 8"/>`;
  o += `<rect x="${r2(pad)}" y="${r2(pad)}" width="${r2(vw - 2 * pad)}" height="${r2(vh - 2 * pad)}" fill="none" stroke="${I}" stroke-opacity=".25" stroke-width="1.6"/>` + nest(s, 0, 0, vw);
  const sq = (qx, qy) => `<rect x="${r2(qx)}" y="${r2(qy)}" width="${r2(x)}" height="${r2(x)}" fill="${RED}" fill-opacity=".12" stroke="${RED}" stroke-width="1.6"/><text x="${r2(qx + x / 2)}" y="${r2(qy + x / 2 + 14)}" font-family="IBM Plex Mono, monospace" font-size="40" fill="${RED}" text-anchor="middle">x</text>`;
  o += sq(bx, by) + sq(vw - pad, vh - pad);
  return `<svg viewBox="${r2(bx - 20)} ${r2(by - 20)} ${r2(bw + 40)} ${r2(bh + 40)}" aria-hidden="true">${o}</svg>`;
}
// ── colour ──
const cmyk = (hex) => { const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255), k = 1 - Math.max(r, g, b); const f = (v) => Math.round(((1 - v - k) / (1 - k || 1)) * 100); return `${f(r)} ${f(g)} ${f(b)} ${Math.round(k * 100)}`; };
const rgb = (hex) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16)).join(' ');
const chip = (name, hex, role, fg, big = true, bg = null) => `<div class="chip${big ? ' big' : ''}" style="background:${bg || hex};color:${fg}"><b>${name}</b><span>${role}</span><dl><div><dt>HEX</dt><dd>${hex}</dd></div><div><dt>RGB</dt><dd>${rgb(hex)}</dd></div><div><dt>CMYK*</dt><dd>${cmyk(hex)}</dd></div></dl></div>`;
const FOIL = `linear-gradient(135deg,${C.foilA},${C.foilB} 38%,${C.foilC} 55%,${C.foilB} 72%,${C.foilD})`;

// ── misuse ──
const lk = Pn.lockup({ tag: false });
const misuse = [
  ['Stretch or squash it', `<div style="transform:scaleX(1.32)">${inl(lk)}</div>`],
  ['Recolour the point', inl(Pn.lockup({ tag: false, dot: '#2F6DB5' }))],
  ['Rotate it', `<div style="transform:rotate(-11deg)">${inl(lk)}</div>`],
  ['Outline it', inl(lk.replace(/fill="#16130E"/g, `fill="none" stroke="${I}" stroke-width="4"`))],
  ['Add shadows or glows', `<div style="filter:drop-shadow(6px 8px 5px rgba(0,0,0,.45)) drop-shadow(0 0 14px rgba(190,51,25,.6))">${inl(lk)}</div>`],
  ['Rearrange the lockup', `<div class="swap">${inl(Pn.lockup({ layout: 'wordmark', tag: false }))}${inl(Pn.symbol({ cut: 'L', tight: true }), 'sm')}</div>`],
  ['Set it on a busy image without a plate', `<div class="busy">${inl(lk)}</div>`],
  ['Bring back the caret', `<div class="oldcaret">CARAT<span>^</span>CAPITAL</div>`],
].map(([t, h]) => `<figure class="mis"><div class="mis-art">${h}</div><figcaption><i>×</i>Don’t ${t.charAt(0).toLowerCase() + t.slice(1)}</figcaption></figure>`).join('');

// ── pages ──
const SEC = ['The idea', 'The symbol', 'Construction', 'Optical sizes', 'The engraved cut', 'The wordmark', 'Lockups', 'Clear space and minimum size', 'Colour', 'Colour in use', 'Typography', 'Misuse', 'On the site', 'On screens', 'In print', 'Files'];
const pages = [];
const page = (title, body, cls = '') => { const n = String(pages.length + 1).padStart(2, '0'); pages.push(`<section class="sp ${cls}" id="p${n}" aria-label="${title}"><header class="rh"><span>Carat Capital · Brand Book</span><span>${n} · ${title}</span></header><div class="pc">${body}</div><footer class="rf"><span>The Point · Edition 1.0</span><span>${n}</span></footer></section>`); };
pages.push(`<section class="sp ink cover" id="p01" aria-label="Cover"><div class="cv-top"><span>Brand Book</span><span>Edition 1.0 · September 2026</span></div><div class="cv-mark">${inl(Pn.symbol({ style: 'engraved', tight: true, gold: true }))}</div><div class="cv-name">${inl(Pn.lockup({ layout: 'wordmark', fg: P }))}</div><div class="cv-bot"><span>The Point</span><span>caratcapital.org</span></div></section>`);
page('Contents', `<div class="two" style="--c:5fr 6fr"><div class="stack"><p class="kick">How to use this book</p><h2>Contents</h2><p class="lede">This book sets out how the Carat Capital mark is drawn and how to use it. Every file it refers to is in <code>brand/logo</code>.</p><p>When a case isn’t covered here, choose the simpler option and keep the point red.</p></div><ol class="toc">${SEC.map((s, i) => `<li><span>${s}</span><b>${String(i + 3).padStart(2, '0')}</b></li>`).join('')}</ol></div>`);
page('The idea', `<div class="stack gap-l"><div class="two" style="--c:7fr 5fr;align-items:end"><div class="stack"><p class="kick">The idea</p><h2>A diamond that is also a pen</h2></div><p class="lede">Printers set type in points. Dealers weigh diamonds in points: one point is a hundredth of a carat. The mark sits where the two trades meet.</p></div>
<div class="three">${[['stone', 'The stone', 'A round brilliant seen from the side. The crown is cut at 34.5°, the angle Marcel Tolkowsky published in <i>Diamond Design</i> in 1919.'], ['pen', 'The pen', 'Its pavilion is a nib. The slit runs down the centre facet, and the two pavilion mains become the tines.'], ['point', 'The point', 'The nib’s breather hole holds a red point. The same point closes the name, so the symbol and the wordmark end on one mark.']].map(([k, t, d]) => `<div class="read"><div class="read-art">${reading(k)}</div><h3>${t}</h3><p>${d}</p></div>`).join('')}</div></div>`);
page('The symbol', `<div class="two" style="--c:7fr 4fr"><div class="anat">${anatomy()}</div><div class="stack"><p class="kick">The symbol</p><h2>Six parts, all from the stone</h2><p>Every line in the mark is a facet edge or the slit of a nib. Nothing is there for decoration, which is why it holds together at every size.</p><p class="note">The symbol is always drawn with the table up and the point red. It never sits in a circle, badge or frame.</p></div></div>`);
page('Construction', `<div class="two" style="--c:6fr 5fr"><div class="plate lo">${inl(R.pointConstruction({}))}</div><div class="stack"><p class="kick">Construction</p><h2>Drawn to a cutter’s figures</h2><table class="spec"><tbody>${[['Girdle', '1.000 (the unit)'], ['Table', '0.56 of the girdle'], ['Crown angle', '34.5°'], ['Crown height', '0.151'], ['Pavilion angle', '45°'], ['Pavilion depth', '0.500'], ['Overall height', '0.651'], ['Facet break', '0.36 of the half-girdle'], ['The point', 'a third of the way down the pavilion'], ['Knockout, L cut', '1.4% of the width']].map(([k, v]) => `<tr><th>${k}</th><td>${v}</td></tr>`).join('')}</tbody></table><p class="note">The pavilion runs deeper than an ideal cut (45° against 40.75°). That extra depth is what lets the stone read as a nib.</p></div></div>`);
page('Optical sizes', `<div class="stack gap-l"><div class="two" style="--c:6fr 5fr;align-items:end"><div class="stack"><p class="kick">Optical sizes</p><h2>Three cuts for three distances</h2></div><p class="lede">Fine knockouts disappear on small screens, so the mark comes in three cuts. Each keeps the silhouette and the point and drops detail as it shrinks.</p></div>
<div class="three">${['L', 'M', 'S'].map((c) => `<div class="cut"><div class="plate paper sq">${inl(Pn.symbol({ cut: c, tight: true }))}</div><h3>${c} cut</h3><p class="mono">${Pn.CUTS[c].use}</p><p>${{ L: 'All facets. The master drawing.', M: 'Crown facets removed, knockouts doubled.', S: 'Girdle, slit and point only. Favicons and app bars.' }[c]}</p><div class="ladder">${(c === 'L' ? [128, 96] : c === 'M' ? [64, 32] : [24, 16]).map((s) => `<span style="width:${s}px">${inl(Pn.symbol({ cut: c, tight: true }))}</span>`).join('')}</div></div>`).join('')}</div></div>`);
page('The engraved cut', `<div class="two" style="--c:5fr 7fr"><div class="stack"><p class="kick">The engraved cut</p><h2>For print that invites a closer look</h2><p>Each facet is hatched at its own angle and density, lit from the upper left, so the stone reads in pure line. Use it on certificates, the Almanac cover, foil and blind stamping, and letterpress.</p><p class="note">Use it at 40 mm or 400 px and larger. Below that, use the L cut.</p></div><div class="pair"><div class="plate paper">${inl(Pn.symbol({ style: 'engraved', tight: true }))}</div><div class="plate ink">${inl(Pn.symbol({ style: 'engraved', tight: true, gold: true }))}</div></div></div>`);
page('The wordmark', `<div class="stack gap-l"><div class="two" style="--c:6fr 5fr;align-items:end"><div class="stack"><p class="kick">The wordmark</p><h2>Bodoni Moda, and one red point</h2></div><p class="lede">The name is set in Bodoni Moda 500. Its hairlines echo the facet edges, and the full stop is drawn as the point.</p></div><div class="wmspec">${wordmarkSpec()}</div>
<div class="three small"><div><h3>Display cut</h3><p>Optical size 28, tracking −22. For every lockup and any wordmark with a cap height of 24 px or 6 mm and up.</p></div><div><h3>Text cut</h3><p>Optical size 11, tracking −8. Sturdier hairlines for small sizes, navigation bars and live web text. <span class="tcut">Carat Capital<i class="pt"></i></span></p></div><div><h3>Artwork, not type</h3><p>Use the files; don’t retype the name. The website is the one exception: it sets the name live in Bodoni Moda and draws the point in CSS to the same measurements.</p></div></div></div>`);
page('Lockups', `<div class="lockgrid"><div class="lk-head stack"><p class="kick">Lockups</p><h2>Five arrangements</h2><p>The horizontal lockup is the default. Choose another only when the space asks for it.</p></div>
${[['Primary · horizontal with tagline', 'Mastheads, covers, the share card, anything with room.', Pn.lockup({}), 'wide'], ['Horizontal, no tagline', 'Headers and bars under 300 px wide.', Pn.lockup({ tag: false }), ''], ['Stacked', 'Square and portrait formats, social cards, posters.', Pn.lockup({ layout: 'stacked' }), 'tall'], ['Wordmark', 'Where the symbol already appears nearby.', Pn.lockup({ layout: 'wordmark', tag: false }), ''], ['Symbol', 'Favicons, avatars, app icons, stamps.', Pn.symbol({ cut: 'L', tight: true }), 'sym']].map(([t, u, s, cls]) => `<figure class="lk ${cls}"><div class="plate paper">${inl(s)}</div><figcaption><b>${t}</b>${u}</figcaption></figure>`).join('')}</div>`);
page('Clear space and minimum size', `<div class="two" style="--c:7fr 4fr"><div class="plate paper">${clearSpace()}</div><div class="stack"><p class="kick">Clear space and minimum size</p><h2>Give it one cap height</h2><p>Keep everything else at least <b>x</b> away from the lockup on every side, where <b>x</b> is the cap height of the C.</p><table class="spec"><tbody>${[['Lockup with tagline', '180 px · 45 mm wide'], ['Lockup, no tagline', '120 px · 30 mm'], ['Stacked lockup', '100 px · 25 mm'], ['Wordmark', '90 px · 22 mm'], ['Symbol, S cut', '16 px · 5 mm']].map(([k, v]) => `<tr><th>${k}</th><td>${v}</td></tr>`).join('')}</tbody></table><p class="note">Below 180 px the tagline stops being legible, so drop it rather than shrink it.</p></div></div>`);
page('Colour', `<div class="stack gap-m"><div class="two" style="--c:6fr 5fr;align-items:end"><div class="stack"><p class="kick">Colour</p><h2>Ink, paper, and the point</h2></div><p class="lede">The palette is the paper’s own. Point Red is kept for the point and the paper’s red accents; it never becomes a background for long text.</p></div>
<div class="chips">${chip('Ink', C.ink, 'The mark, text', P)}${chip('Paper', C.paper, 'The ground', I)}${chip('Point Red', C.seal, 'The point only', P)}${chip('Gilt', C.gilt, 'Foil, hallmarks', I, true, FOIL)}${chip('Ink 2', C.ink2, 'Secondary text', P, false)}${chip('Ink 3', C.ink3, 'Captions, rules', P, false)}${chip('Paper Low', '#E8E1D1', 'Plates, panels', I, false)}</div><p class="fine">* CMYK values are converted from RGB as a starting point. Ask the printer for a proof, and match it to the swatches in this book.</p></div>`);
const tile = (bg, s, t, style = '') => `<figure class="use"><div class="plate" style="background:${bg};${style}">${inl(s)}</div><figcaption>${t}</figcaption></figure>`;
page('Colour in use', `<div class="stack gap-m"><div class="two" style="--c:6fr 5fr;align-items:end"><div class="stack"><p class="kick">Colour in use</p><h2>Six approved pairings</h2></div><p class="lede">The point stays red in every pairing but one: one-colour work, where it takes the colour of the mark.</p></div>
<div class="uses">${tile(P, Pn.lockup({ tag: false }), '<b>Primary.</b> Ink and Point Red on Paper')}${tile(I, Pn.lockup({ tag: false, fg: P }), '<b>Reverse.</b> Paper and Point Red on Ink')}${tile(I, Pn.lockup({ tag: false, fg: GOLD, gold: true }), '<b>Foil.</b> Gilt on Ink, the point in red foil')}${tile(RED, Pn.lockup({ tag: false, fg: P, dot: I }), '<b>On Point Red.</b> Paper, with the point in Ink')}${tile('#FFFFFF', Pn.lockup({ tag: false, dot: I }), '<b>One colour.</b> Ink only, for faxes, engraving, embossing')}${tile(I, Pn.lockup({ tag: false, fg: P, dot: P }), '<b>One colour, reversed.</b> Paper only, on dark images with a plate', `background-image:url(${b64(path.join(BUILD, 'cap-folio.jpg'), 'image/jpeg')});background-size:cover;background-position:center;box-shadow:inset 0 0 0 999px rgba(22,19,14,.62)`)}</div></div>`);
page('Typography', `<div class="two" style="--c:4fr 7fr;align-items:start"><div class="stack"><p class="kick">Typography</p><h2>One face for the name, three for the paper</h2><p>Bodoni Moda belongs to the name. The paper keeps the faces it already reads in, so the new mark arrives without a redesign.</p></div><div class="types">
<div class="ty"><p class="mono">Bodoni Moda 500 · the name, the masthead</p><p class="ty-bod">Carat Capital<i class="pt"></i></p></div>
<div class="ty"><p class="mono">Instrument Sans 600–700 · headlines</p><p class="ty-ins">De Beers digs 88% more, banks 44% less</p></div>
<div class="ty"><p class="mono">Lora 400 · text</p><p class="ty-lor">Second-quarter rough output jumped 88% to 7.8 million carats even as the average price fell 32% to $105 a carat.</p></div>
<div class="ty"><p class="mono">IBM Plex Mono 500 · data, labels, the tape</p><p class="ty-mono"><span>NATURAL 1CT (RAPI PROXY)</span> <b>3,915.00</b> <em>−5.1% YTD</em></p></div></div></div>`);
page('Misuse', `<div class="stack gap-m"><div class="two" style="--c:6fr 5fr;align-items:end"><div class="stack"><p class="kick">Misuse</p><h2>Eight things not to do</h2></div><p class="lede">Each of these breaks either the geometry of the stone or the single red point.</p></div><div class="mises">${misuse}</div></div>`);
page('On the site', `<div class="site"><div class="stack"><p class="kick">On the site</p><h2>Live on caratcapital.org</h2><p>The homepage sets the name in the display cut under the rotating brilliant. Every other page carries the S-cut symbol and the name in the text cut in its navigation bar.</p><p class="note">Rendered from the site’s own templates.</p></div>
<figure class="shot big"><img src="${b64(path.join(BUILD, 'cap-home.jpg'), 'image/jpeg')}" alt="The Carat Capital homepage with the new wordmark"><figcaption>Front page</figcaption></figure><figure class="shot"><img src="${b64(path.join(BUILD, 'cap-article.jpg'), 'image/jpeg')}" alt="An article page with the new navigation bar"><figcaption>Article page</figcaption></figure><figure class="shot phone"><img src="${b64(path.join(BUILD, 'cap-phone.jpg'), 'image/jpeg')}" alt="The homepage on a phone"><figcaption>Phone</figcaption></figure></div>`);
page('On screens', `<div class="screens"><div class="stack"><p class="kick">On screens</p><h2>Small, and still the stone</h2><p>The S cut carries the favicon and app bars. Avatars and app icons use the L and M cuts on Ink or Paper, with the stone at about 62% of the width so circular crops never touch it.</p></div>
<figure class="scr tabs"><div class="browser"><div class="tab">${inl(Pn.symbol({ cut: 'S', tight: true }), 'fav')}<span>Carat Capital</span><i>×</i></div><div class="url">caratcapital.org</div></div><div class="browser dark"><div class="tab">${inl(Pn.symbol({ cut: 'S', tight: true, fg: P }), 'fav')}<span>Carat Capital</span><i>×</i></div><div class="url">caratcapital.org</div></div><figcaption>Favicon, light and dark browsers</figcaption></figure>
<figure class="scr"><div class="icons"><span class="app">${inl(Pn.symbol({ cut: 'M', tight: true, fg: P }))}</span><span class="av">${inl(Pn.symbol({ cut: 'L', tight: true }))}</span><span class="av ink">${inl(Pn.symbol({ cut: 'L', tight: true, fg: P }))}</span></div><figcaption>App icon and avatars</figcaption></figure>
<figure class="scr card"><img src="${b64(path.join(BRAND, '..', 'assets', 'share-card.png'), 'image/png')}" alt="The share card"><figcaption>Share card, 1200 × 630</figcaption></figure></div>`);
page('In print', `<div class="print"><div class="stack"><p class="kick">In print</p><h2>Cards, letters and the brief</h2><p>Stationery uses the engraved cut in gilt foil on Ink stock, and the lockup in Ink on Paper stock. The Morning Brief opens with the lockup and a date line in Plex Mono.</p></div>
<figure class="pr"><div class="bc front">${inl(Pn.symbol({ style: 'engraved', tight: true, gold: true }))}</div><div class="bc back">${inl(Pn.lockup({ tag: false }))}<p><b>The Mines Desk</b><br>caratcapital.org</p></div><figcaption>Business card, front and back</figcaption></figure>
<figure class="pr"><div class="letter">${inl(Pn.lockup({}))}<i></i><i></i><i></i><i style="width:70%"></i><i></i><i style="width:55%"></i><p>caratcapital.org · The trade paper of the jewelry world</p></div><figcaption>Letterhead</figcaption></figure>
<figure class="pr"><div class="mail"><div class="mail-top">${inl(Pn.lockup({ tag: false }))}<span>The Morning Brief · Friday 25 September 2026</span></div><p class="mail-h">The trade, filed before the New York open.</p><i></i><i></i><i style="width:72%"></i></div><figcaption>The Morning Brief</figcaption></figure></div>`);
page('Files', `<div class="two" style="--c:4fr 7fr;align-items:start"><div class="stack"><p class="kick">Files</p><h2>Everything in brand/logo</h2><p>SVG for anything that scales, PNG where a platform asks for pixels. Type is outlined and knockouts are transparent, so every file sits on any background.</p><p class="note">The drawings are generated from <code>brand/source/point.js</code>. Change a proportion there and every file, and this book, rebuilds to match.</p></div><div class="files">${[['svg/', 'Lockups (horizontal, stacked, wordmark) in ink, reverse, gold and one-colour; the symbol in L, M and S cuts, gold and engraved.'], ['png/', 'Transparent PNGs of the lockups at 2400 px, the symbol at 1024 px, the engraved cut at 2048 px.'], ['favicon/', 'favicon.svg (switches to paper in dark browsers), favicon.ico (16, 32, 48), apple-touch-icon, 192 and 512 px icons.'], ['social/', 'Avatars on Paper and on Ink at 1024 px, and the 1200 × 630 share card.'], ['Brand book', 'This book as a PDF: Carat-Capital-Brand-Book.pdf.']].map(([k, v]) => `<div class="file"><b>${k}</b><p>${v}</p></div>`).join('')}</div></div>`);

const css = `
:root{--paper:#F2EDE3;--paper-hi:#F8F4EB;--paper-lo:#E8E1D1;--desk:#D9D1BF;--ink:#16130E;--ink-2:#3B362C;--ink-3:#6F6758;--red:#BE3319;--rule:rgba(22,19,14,.16);color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:var(--desk);color:var(--ink);font-family:'Lora',Georgia,serif;-webkit-font-smoothing:antialiased}
.book{container-type:inline-size;max-width:1600px;margin:0 auto;padding-inline:clamp(16px,3vw,40px);padding-block:clamp(16px,3vw,40px);display:grid;gap:clamp(16px,2.2vw,30px)}
.sp{position:relative;aspect-ratio:16/10;font-size:1cqw;background:var(--paper);display:grid;grid-template-rows:auto minmax(0,1fr) auto;gap:1.6em;padding:2.2em 3.2em 1.8em;overflow:hidden;box-shadow:0 .15em 1.2em rgba(22,19,14,.14)}
.sp.ink{background:var(--ink);color:var(--paper)}
.rh,.rf{display:flex;justify-content:space-between;font:500 .66em/1 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3)}
.rh{border-bottom:1px solid var(--rule);padding-bottom:1em}
.pc{min-height:0;display:grid}.pc>*{align-self:center}
.stack{display:grid;gap:1.1em;align-content:start}.gap-l{gap:2.4em}.gap-m{gap:1.6em}
.two{display:grid;grid-template-columns:var(--c,1fr 1fr);gap:3.2em;align-items:center;min-height:0}
.three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2.6em}
h2,h3{font-family:'Instrument Sans',Arial,sans-serif;margin:0;text-wrap:balance}
h2{font-weight:600;font-size:3.3em;line-height:.98;letter-spacing:-.03em}
h3{font-weight:600;font-size:1.3em;letter-spacing:-.01em}
p{margin:0;font-size:1.02em;line-height:1.55;max-width:34em}
.lede{font-size:1.28em;line-height:1.45;color:var(--ink-2)}
.kick{font:500 .74em/1 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.18em;text-transform:uppercase;color:var(--red)}
.note{font-size:.92em;color:var(--ink-2);border-left:2px solid var(--red);padding-left:1em}
.mono{font:500 .72em/1.4 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.fine{font-size:.78em;color:var(--ink-3);max-width:none}
code{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:.88em}
.plate{display:flex;align-items:center;justify-content:center;padding:6%;min-height:0;min-width:0}
.plate.paper{background:var(--paper-hi)}.plate.lo{background:var(--paper-lo)}.plate.ink{background:var(--ink)}
.plate>svg,.plate>img{display:block;width:100%;height:auto;max-height:100%}
.plate.sq{aspect-ratio:1.45}
.pt{display:inline-block;width:.16em;height:.16em;border-radius:50%;background:var(--red);margin-left:.02em;vertical-align:baseline}
/* cover */
.cover{grid-template-rows:auto minmax(0,1fr) auto auto;gap:0;padding:2.6em 3.4em 2.4em}
.cv-top,.cv-bot{display:flex;justify-content:space-between;font:500 .72em/1 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.2em;text-transform:uppercase;color:rgba(242,237,227,.6)}
.cv-mark{display:flex;align-items:center;justify-content:center;min-height:0;padding-top:2em}.cv-mark svg{height:100%;max-height:25em;width:auto}
.cv-name{width:42%;margin:1.6em auto 3.2em}.cv-name svg{width:100%;height:auto;display:block}
.cv-bot span:first-child{color:#D9B45E}
/* contents */
.toc{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;column-gap:2.4em;align-self:center}
.toc li{display:flex;justify-content:space-between;gap:1em;padding:.62em 0;border-bottom:1px solid var(--rule);font-size:1.05em}
.toc b{font:500 .8em 'IBM Plex Mono',monospace;color:var(--red)}
/* idea */
.read{display:grid;gap:.7em;align-content:start;border-top:1px solid var(--ink);padding-top:1.2em}.read-art svg{width:80%;height:auto;display:block}
.anat svg{width:100%;height:auto;display:block}
/* construction */
.spec{border-collapse:collapse;width:100%;font-size:.95em}.spec th,.spec td{text-align:left;padding:.5em 0;border-bottom:1px solid var(--rule);font-weight:400}.spec th{font:500 .78em 'IBM Plex Mono',monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);width:44%}
.plate.lo svg{max-height:32em}
/* optical */
.cut{display:grid;gap:.6em;align-content:start}.cut .plate{padding:10% 14%}
.ladder{display:flex;align-items:flex-end;gap:14px;margin-top:.4em}.ladder span{display:block}.ladder svg{width:100%;height:auto;display:block}
/* engraved */
.pair{display:grid;grid-template-columns:1fr 1fr;gap:1.2em}.pair .plate{aspect-ratio:.9;padding:10%}
/* wordmark */
.wmspec svg{width:100%;height:auto;display:block;max-height:17em}
.three.small p{font-size:.95em}
.tcut{display:inline-block;margin-top:.5em;font-family:'Bodoni Moda',Didot,Georgia,serif;font-weight:500;font-variation-settings:'opsz' 11;letter-spacing:-.008em;font-size:18px}
/* lockups */
.lockgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-template-rows:auto auto;gap:1.2em 1.4em;align-content:center}
.lk-head{grid-column:1/2}.lk.wide{grid-column:2/5}
.lk{margin:0;display:grid;gap:.6em;align-content:start}.lk .plate{aspect-ratio:1.6;padding:9%}.lk.wide .plate{aspect-ratio:auto;height:100%;padding:3% 8%}
.lk.tall .plate{padding:6% 16%}.lk.sym .plate{padding:10% 26%}
.lk figcaption{font-size:.84em;color:var(--ink-2);display:grid;gap:.2em}.lk figcaption b{font:500 .82em 'IBM Plex Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--ink)}
/* colour */
.chips{display:grid;grid-template-columns:repeat(4,minmax(0,1fr)) ;gap:1em}
.chip{display:grid;gap:.4em;align-content:end;padding:1.2em;min-height:9.4em;border:1px solid var(--rule)}.chip.big{min-height:14em}
.chip b{font:600 1.3em 'Instrument Sans',Arial,sans-serif}.chip span{font-size:.86em;opacity:.8}
.chip dl{margin:.4em 0 0;display:grid;gap:.15em;font:500 .7em 'IBM Plex Mono',monospace;letter-spacing:.06em}.chip dl div{display:flex;gap:.8em}.chip dt{opacity:.65;width:4.2em}.chip dd{margin:0}
.uses{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.1em}
.use{margin:0;display:grid;gap:.55em}.use .plate{aspect-ratio:2.6;padding:6% 12%;border:1px solid var(--rule)}.use figcaption{font-size:.84em;color:var(--ink-2)}
/* typography */
.types{display:grid;gap:1.4em}.ty{display:grid;gap:.5em;border-top:1px solid var(--ink);padding-top:.9em}
.ty-bod{font-family:'Bodoni Moda',Didot,Georgia,serif;font-weight:500;font-variation-settings:'opsz' 28;letter-spacing:-.022em;font-size:5.6em;line-height:1;max-width:none}
.ty-ins{font:700 3em/1 'Instrument Sans',Arial,sans-serif;letter-spacing:-.03em;max-width:none}
.ty-lor{font-size:1.4em;max-width:34em}
.ty-mono{font:500 1.25em 'IBM Plex Mono',monospace;letter-spacing:.06em;max-width:none}.ty-mono span{color:#96762E}.ty-mono em{font-style:normal;color:var(--red)}
/* misuse */
.mises{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.1em}
.mis{margin:0;display:grid;gap:.55em}.mis-art{aspect-ratio:1.9;background:var(--paper-hi);border:1px solid var(--rule);display:flex;align-items:center;justify-content:center;padding:6% 12%;overflow:hidden}
.mis-art>svg,.mis-art>div{width:100%}.mis-art svg{display:block;width:100%;height:auto}
.mis figcaption{font-size:.86em;display:flex;gap:.5em;align-items:baseline}.mis figcaption i{font-style:normal;color:var(--red);font-weight:700}
.swap{display:flex;align-items:center;gap:4%}.swap svg:first-child{width:70%}.swap .sm{width:22%}
.busy{background:repeating-conic-gradient(from 20deg,#c9b98f 0 12deg,#6f6758 0 24deg,#e8e1d1 0 36deg);padding:6%;margin:-6% -12%;width:calc(100% + 24%)!important}
.oldcaret{font:700 1.9em 'Instrument Sans',Arial,sans-serif;letter-spacing:-.02em;text-align:center}.oldcaret span{color:var(--red)}
/* site */
.site{display:grid;grid-template-columns:4fr 7fr 2.1fr;grid-template-rows:auto auto;gap:1.2em 1.6em;align-items:start}
.site>.stack{grid-row:1/3}
.shot{margin:0;display:grid;gap:.45em}.shot img{width:100%;height:auto;display:block;box-shadow:0 .2em 1em rgba(22,19,14,.2)}.shot figcaption{font:500 .7em 'IBM Plex Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.shot.big{grid-column:2/3}.shot.phone{grid-column:3/4;grid-row:1/3}.site .shot:not(.big):not(.phone){grid-column:2/3}
/* screens */
.screens{display:grid;grid-template-columns:4fr 4fr 4fr;grid-template-rows:auto auto;gap:1.6em 2em;align-items:start}
.screens>.stack{grid-row:1/3}
.scr{margin:0;display:grid;gap:.6em}.scr figcaption{font:500 .7em 'IBM Plex Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.scr.card{grid-column:2/4}.scr.card img{width:100%;height:auto;display:block;box-shadow:0 .2em 1em rgba(22,19,14,.2)}
.browser{background:#DAD4C6;border-radius:.7em .7em 0 0;padding:.5em .6em 0}.browser.dark{background:#2A2825;margin-top:.8em}
.tab{display:flex;align-items:center;gap:.6em;background:var(--paper-hi);border-radius:.55em .55em 0 0;padding:.55em .8em;font:500 .9em 'Instrument Sans',Arial,sans-serif;max-width:15em}.browser.dark .tab{background:#3B3833;color:#EDE7DB}
.tab .fav{width:16px;height:auto;flex:none}.tab span{flex:1}.tab i{font-style:normal;opacity:.5}
.url{background:var(--paper-hi);margin:0 -.6em;padding:.45em 1em;font:.78em 'IBM Plex Mono',monospace;border-top:1px solid var(--rule)}.browser.dark .url{background:#3B3833;color:#CFC8BA;border-color:rgba(255,255,255,.08)}
.icons{display:flex;gap:1.4em;align-items:center}.icons svg{width:62%;height:auto;display:block}
.app{width:6.4em;height:6.4em;border-radius:1.5em;background:var(--ink);display:grid;place-items:center}
.av{width:6.4em;height:6.4em;border-radius:50%;background:var(--paper-hi);border:1px solid var(--rule);display:grid;place-items:center}.av.ink{background:var(--ink)}
/* print */
.print{display:grid;grid-template-columns:4fr 4fr 4fr;grid-template-rows:auto auto;gap:1.6em 2em;align-items:start}
.print>.stack{grid-row:1/3}
.pr{margin:0;display:grid;gap:.6em;align-content:start}.pr figcaption{font:500 .7em 'IBM Plex Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.bc{aspect-ratio:1.75;display:flex;align-items:center;justify-content:center;box-shadow:0 .3em 1.2em rgba(22,19,14,.22)}.bc.front{background:var(--ink)}.bc.front svg{width:34%;height:auto}
.bc.back{background:#FBF8F1;flex-direction:column;align-items:flex-start;justify-content:space-between;padding:1.2em 1.4em}.bc.back svg{width:62%;height:auto}.bc.back p{font:500 .74em/1.5 'IBM Plex Mono',monospace;letter-spacing:.06em}
.letter{aspect-ratio:.71;background:#FBF8F1;box-shadow:0 .3em 1.2em rgba(22,19,14,.22);padding:1.6em 1.5em;display:grid;gap:.55em;align-content:start}.letter svg{width:56%;height:auto;display:block;margin-bottom:1.4em}
.letter i,.mail i{display:block;height:.42em;background:rgba(22,19,14,.12)}.letter p{font:.6em 'IBM Plex Mono',monospace;color:var(--ink-3);margin-top:auto}
.mail{background:#FBF8F1;box-shadow:0 .3em 1.2em rgba(22,19,14,.22);padding:1.3em;display:grid;gap:.6em}.mail-top{display:grid;gap:.6em;border-bottom:3px double var(--ink);padding-bottom:.8em}.mail-top svg{width:58%;height:auto}
.mail-top span{font:500 .62em 'IBM Plex Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--red)}.mail-h{font:700 1.2em/1.1 'Instrument Sans',Arial,sans-serif;letter-spacing:-.02em}
.print .pr:nth-of-type(1){grid-column:2/3}.print .pr:nth-of-type(2){grid-column:3/4;grid-row:1/3}.print .pr:nth-of-type(3){grid-column:2/3}
/* files */
.files{display:grid;gap:0;border-top:1px solid var(--ink)}.file{display:grid;grid-template-columns:9em 1fr;gap:1.4em;padding:1em 0;border-bottom:1px solid var(--rule)}.file b{font:500 .9em 'IBM Plex Mono',monospace}.file p{font-size:.98em}
@media (max-width:760px){
  .sp{aspect-ratio:auto;font-size:13px;padding:20px 18px 18px;gap:18px}
  .cover{min-height:520px}.cv-name{width:78%}.cv-mark svg{max-height:210px}
  .two,.three,.pair,.chips,.uses,.mises,.site,.screens,.print,.lockgrid,.toc{grid-template-columns:1fr!important}
  .lk-head,.lk.wide,.site>*,.screens>*,.print>*,.print .pr:nth-of-type(n){grid-column:auto!important;grid-row:auto!important}
  h2{font-size:30px}.ty-bod{font-size:44px}.chip.big,.chip{min-height:8em}.lk .plate{aspect-ratio:1.8}
}
@page{size:1600px 1000px;margin:0}
@media print{body{background:none}.book{max-width:none;padding:0;gap:0}.sp{width:1600px;height:1000px;aspect-ratio:auto;box-shadow:none;break-after:page;font-size:16px}}
`;
const FONTS = `<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400..700&family=Instrument+Sans:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,500;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">`;
const body = `<main class="book">${pages.join('\n')}</main>`;
fs.mkdirSync(BUILD, { recursive: true });
fs.writeFileSync(path.join(BUILD, 'carat-capital-brand-book.artifact.html'), `<title>Carat Capital Brand Book</title>\n${FONTS}\n<style>${css}</style>\n${body}\n`);
fs.writeFileSync(path.join(BRAND, 'brand-book.html'), `<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Carat Capital Brand Book</title>\n${FONTS}\n<style>${css}</style></head><body>${body}</body></html>\n`);
console.log('pages', pages.length, 'html', Math.round(fs.statSync(path.join(BRAND, 'brand-book.html')).size / 1024) + 'KB');
