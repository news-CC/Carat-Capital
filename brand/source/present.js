// Builds the identity presentation page: brand/index.html.
const R = require('./routes'); const { C } = require('./lib'); const fs = require('fs');
const P = C.paper, I = C.ink, S = C.seal;
const plate = (svg, cls, cap = '', max = '72%', style = '') => `<figure class="plate ${cls}"${style ? ` style="${style}"` : ''}><div class="art" style="max-width:${max}">${svg}</div>${cap ? `<figcaption>${cap}</figcaption>` : ''}</figure>`;
const ladder = (fn, cls = 'paper') => `<figure class="plate ${cls}"><div class="ladder">${[96, 48, 32, 16].map((s) => `<div><span style="width:${s}px;height:${s}px">${fn(s)}</span><small>${s} px</small></div>`).join('')}</div><figcaption>Scale</figcaption></figure>`;
const spec = (rows) => `<dl class="spec">${rows.map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`).join('')}</dl>`;

const hero = [
  plate(R.pointSymbol({}), 'paper sq', '01 The Point', '66%'),
  plate(R.hallmarkSymbol({ foil: true }), 'ink sq', '02 The Hallmark', '80%'),
  plate(R.stepCutSymbol({ gold: true }), 'ink sq', '03 The Step Cut', '62%'),
  plate(R.solidusSeal({ detail: 'simple' }), 'paper sq', '04 The Solidus', '78%'),
  plate(R.insertionMonogram({ fg: P, stone: I }), 'seal sq', '05 The Insertion', '62%'),
].join('');

const finds = [
  ['The point', '1 pt = 0.01 ct', 'Printers measure type in points. Dealers weigh diamonds in points too: one point is a hundredth of a carat.'],
  ['Keration', 'κεράτιον · carob seed', 'Carat comes from the Greek word for the carob seed, which merchants used as a counterweight on their scales.'],
  ['The solidus', '24 seeds = 1 coin', 'Constantine’s gold coin weighed 24 carob seeds, which is why pure gold is 24 karat. Its name survives in the slash, once the sign for shillings.'],
  ['The maker’s mark', 'sponsor · fineness · office · date', 'Before jewelers had logos they had punches: initials struck into the metal beside the assay office’s marks for fineness, office and year.'],
  ['The caret', '‸ insert here', 'The proofreader’s mark for an insertion. The current nameplate already sets one between CARAT and CAPITAL.'],
  ['The briefke', 'Antwerp · little letter', 'In Antwerp the folded paper that holds loose stones is called a briefke, a little letter. The Morning Brief could arrive folded the same way.'],
].map(([t, u, d]) => `<article class="find"><h3>${t}</h3><p class="unit">${u}</p><p>${d}</p></article>`).join('');

const browser = (fav) => `<div class="browser"><div class="tab"><span class="fav">${fav}</span><span class="tt">Carat Capital</span><span class="x">×</span></div><div class="url">caratcapital.org</div></div>`;
const routes = [
  {
    id: 'point', n: '01', kind: 'Editorial', name: 'The Point', thesis: 'A diamond in profile that is also a pen nib.',
    lockup: plate(R.pointLockup({}), 'paper wide', 'Primary lockup', '820px'),
    copy: `<p>The crown uses the 34.5° angle from Marcel Tolkowsky’s <i>Diamond Design</i> (1919) on a 56% table. The pavilion runs to 45°, just deep enough for the stone to read as a nib as well. The slit follows the pavilion’s centre facet, and the breather hole holds a red point: the unit that printers and diamond dealers share.</p><p>The same red point closes the wordmark, so the symbol and the name end on one mark.</p>`,
    spec: [['Wordmark', 'Bodoni Moda 500, tracked −8'], ['Tagline', 'IBM Plex Mono 500, tracked +262'], ['Small sizes', 'A separate cut for 16–48 px drops the facets and opens the knockouts'], ['Best for', 'Primary symbol, app icon, favicon, social avatar']],
    plates: plate(R.pointSymbol({ fg: P }), 'ink', 'Reverse', '64%') + plate(R.pointConstruction({}), 'lo', 'Construction', '94%') +
      ladder((s) => R.pointSymbol({ size: s <= 48 ? 'small' : 'large' })) +
      `<figure class="plate paper"><div class="apps"><div class="app">${R.pointSymbol({ fg: P, size: 'small' })}</div><div class="avatar">${R.pointSymbol({})}</div>${browser(R.pointSymbol({ size: 'small' }))}</div><figcaption>App icon, avatar, favicon</figcaption></figure>`,
  },
  {
    id: 'hallmark', n: '02', kind: 'Heritage', name: 'The Hallmark', thesis: 'A maker’s mark for the paper, and a masthead struck like a hallmark.',
    lockup: plate(R.hallmarkLockup({}), 'paper wide', 'Primary lockup', '820px'),
    copy: `<p>C◆C sits in a canted punch with a struck inner border, the way a workshop marks its silver. The pellet between the initials is a lozenge in the seal red.</p><p>The strip turns the idea into a system for the masthead: the sponsor’s mark, the edition number struck like a fineness figure (072 sits where 750 or 925 would), the office mark, and a date letter for the volume.</p>`,
    spec: [['Punch letters', 'Bodoni Moda 700'], ['Name', 'Castoro Titling, tracked +150'], ['Finishes', 'Ink, reverse, gold foil'], ['Best for', 'Masthead device, stationery, packaging, the mark on corrections and price lists']],
    plates: plate(R.hallmarkSymbol({ foil: true }), 'ink', 'Gold foil', '78%') + plate(R.hallmarkStrip({}), 'lo', 'The hallmark strip: sponsor, edition, office, date letter', '92%') +
      ladder((s) => R.hallmarkSymbol({})) +
      `<figure class="plate paper"><div class="bcard"><div class="bmark">${R.hallmarkSymbol({ foil: true })}</div><div class="bline"><b>The Mines Desk</b><span>caratcapital.org</span></div></div><figcaption>Card, foil on black stock</figcaption></figure>`,
  },
  {
    id: 'step-cut', n: '03', kind: 'Art Deco', name: 'The Step Cut', thesis: 'An emerald cut with a slot in its side is a C.',
    lockup: plate(R.stepCutLockup({}), 'paper wide', 'Primary lockup', '700px'),
    copy: `<p>Seen from above, an emerald cut is a set of nested octagons with a 45° keel at each corner. Cut a slot into the right-hand side and it becomes a C, with the table as its counter.</p><p>The name is set in a titling alphabet drawn for the seven letters it needs (C, A, R, T, P, I and L) with the same clipped corners, so the symbol and the type come from one geometry.</p>`,
    spec: [['Outline', '1 : 1.23, three steps, four keels'], ['Name', 'Bespoke octagonal titling, monoline'], ['Finishes', 'Ink, reverse, gold foil'], ['Best for', 'The luxury register: foil on black, signage, events, the annual']],
    plates: plate(R.stepCutLockup({ stacked: true, gold: true, fg: C.foilB }), 'ink', 'Gold foil on black stock', '88%') + plate(R.stepCutConstruction({}), 'lo', 'Construction', '76%') +
      ladder((s) => R.stepCutSymbol({ kw: s <= 32 ? 0 : 9 })) + plate(R.stepCutSymbol({ fg: P }), 'seal', 'Reverse on seal red', '52%'),
  },
  {
    id: 'solidus', n: '04', kind: 'Seal', name: 'The Solidus', thesis: 'Twenty-four seeds, one stone.',
    lockup: plate(R.solidusSeal({}), 'paper wide tall', 'The seal, full engraving', '560px'),
    copy: `<p>Twenty-four carob seeds ring a round brilliant engraved facet by facet. Each facet is hatched at its own angle and density, so the stone sparkles in pure line. The culet shows through the table as a red point.</p><p>The legend reads <span class="sc">PONDERE · ET · FIDE</span>, by weight and by good faith. The diamond bourses still close deals on a handshake, and a newspaper trades on the same terms.</p>`,
    spec: [['Legend', 'Castoro Titling'], ['Rim', '144 denticles'], ['Detail', 'Full engraving above 200 px, a simplified cut below'], ['Best for', 'The paper’s seal: editorial standards, price lists, the Almanac, certificates']],
    plates: plate(R.solidusSeal({ fg: P, detail: 'simple' }), 'ink', 'Reverse, simplified cut', '70%') +
      `<figure class="plate paper"><div class="doc"><p class="eyebrow">Editorial standards</p><p class="doc-h">Every price is dated. Every source is named and linked.</p><div class="doc-lines"><i></i><i></i><i></i><i></i><i style="width:62%"></i></div><div class="stamp">${R.solidusSeal({ fg: S, red: S, detail: 'simple' })}</div></div><figcaption>Stamped in seal red</figcaption></figure>` +
      ladder((s) => R.solidusSeal({ detail: 'simple' })) + plate(R.solidusSeal({ fg: C.foilB, red: S, detail: 'simple' }), 'ink', 'Gold on black', '64%'),
  },
  {
    id: 'insertion', n: '05', kind: 'Nameplate', name: 'The Insertion', thesis: 'The caret is a stone laid table-down.',
    lockup: plate(R.insertionNameplate({}), 'paper wide', 'The nameplate', '980px'),
    copy: `<p>Graders set a loose diamond table-down on white to judge its colour. Seen side-on, a stone lying that way rises to its culet in the shape of the proofreader’s caret.</p><p>The nameplate inserts one stone between its two words, which gives the caret already on the site a reason to be there. The monogram sets the same stone inside a C.</p>`,
    spec: [['Nameplate', 'Gloock, tracked +10'], ['Stone', 'Cut to the proportions of route 01, turned over'], ['Best for', 'Front-page nameplate, newsletter header, avatar']],
    plates: plate(R.insertionMonogram({}), 'paper', 'Monogram', '56%') + plate(R.insertionMonogram({ fg: P }), 'ink', 'Monogram, reverse', '56%') +
      `<figure class="plate paper span2"><div class="front"><div class="folio"><span>Friday 25 September 2026</span><span>Edition No. 072</span></div>${R.insertionNameplate({})}<p class="front-kicker">Diamonds desk · London</p><p class="front-h">De Beers digs 88% more, banks 44% less</p></div><figcaption>Front page</figcaption></figure>`,
  },
];

const routeHTML = routes.map((r) => `
<section class="route" id="${r.id}">
  <header class="route-head"><p class="eyebrow">Route ${r.n} · ${r.kind}</p><h2>${r.name}</h2><p class="thesis">${r.thesis}</p></header>
  ${r.lockup}
  <div class="route-body"><div class="copy">${r.copy}${spec(r.spec)}</div><div class="plates">${r.plates}</div></div>
</section>`).join('');

const masthead = `<figure class="plate paper mast-plate"><div class="mast">
  <div class="folio"><span>Friday 25 September 2026</span><span>Vol. 1 · Edition No. 072</span><span>Free to read</span></div>
  <div class="mast-row"><div class="ear">${R.hallmarkStrip({})}</div><div class="mast-name">${R.pointLockup({})}</div><div class="ear ear-r">${R.solidusSeal({ detail: 'simple' })}</div></div>
</div><figcaption>The recommended system in the masthead</figcaption></figure>`;

const tree = Object.entries(require('./build').files).map(([d, set]) => `<div class="tree-dir"><b>brand/logos/${d}/</b>${Object.keys(set).map((f) => `<span>${f}</span>`).join('')}</div>`).join('');

const css = `
:root{--paper:#F2EDE3;--paper-hi:#F8F4EB;--paper-lo:#E8E1D1;--ink:#16130E;--ink-2:#3B362C;--ink-3:#6F6758;--seal:#BE3319;--gilt:#96762E;--rule:rgba(22,19,14,.14);--on-ink:#F2EDE3;--on-ink-dim:rgba(242,237,227,.56);color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.62 'Lora',Georgia,serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:1240px;margin:0 auto;padding-inline:clamp(16px,4vw,48px);padding-block:clamp(28px,5vw,64px) 48px}
.eyebrow{margin:0;font:500 11.5px/1.4 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}
h1,h2,h3{font-family:'Instrument Sans',Arial,sans-serif;text-wrap:balance;margin:0}
h1{font-weight:600;font-size:clamp(40px,6.4vw,86px);line-height:.98;letter-spacing:-.032em;max-width:15ch}
h2{font-weight:600;font-size:clamp(36px,5vw,64px);line-height:1;letter-spacing:-.028em}
h3{font-weight:600;font-size:21px;letter-spacing:-.01em}
p{margin:0}
.hero{display:grid;gap:22px;padding-bottom:clamp(28px,4vw,48px);border-bottom:1px solid var(--ink)}
.lede{max-width:62ch;font-size:clamp(17px,1.6vw,19px);color:var(--ink-2)}
.hero-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-top:10px}
@media (max-width:860px){.hero-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.hero-grid>:first-child{grid-column:span 2}}
.plate{margin:0;position:relative;display:flex;align-items:center;justify-content:center;padding:clamp(22px,5%,56px) clamp(18px,4%,48px) clamp(34px,6%,60px);border:1px solid var(--rule);min-height:200px;min-width:0}
.plate.sq{aspect-ratio:1;min-height:0;padding:12% 10% 16%}
.plate.paper{background:var(--paper-hi)}.plate.lo{background:var(--paper-lo)}
.plate.ink{background:var(--ink);border-color:var(--ink)}.plate.seal{background:var(--seal);border-color:var(--seal)}
.plate figcaption{position:absolute;left:14px;right:14px;bottom:11px;font:500 10.5px/1.3 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.plate.ink figcaption,.plate.seal figcaption{color:var(--on-ink-dim)}
.art{width:100%}.art svg{display:block;width:100%;height:auto}
.plate.wide{min-height:clamp(220px,30vw,380px)}
.plate.tall{min-height:clamp(320px,52vw,640px)}
.finds{padding-block:clamp(36px,5vw,64px);display:grid;gap:26px;border-bottom:1px solid var(--ink)}
.finds-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border-top:1px solid var(--rule)}
@media (max-width:900px){.finds-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.finds-grid{grid-template-columns:1fr}}
.find{padding:20px 22px 24px 0;border-bottom:1px solid var(--rule);display:grid;gap:6px;align-content:start}
.find p{font-size:15.5px;color:var(--ink-2);max-width:40ch}
.find .unit{font:500 12px/1.4 'IBM Plex Mono',ui-monospace,monospace;color:var(--seal);letter-spacing:.04em}
.route{padding-block:clamp(44px,6vw,84px);display:grid;gap:clamp(18px,2.4vw,28px);border-bottom:1px solid var(--ink)}
.route-head{display:grid;gap:10px}
.thesis{font-style:italic;font-size:clamp(19px,2vw,24px);color:var(--ink-2);max-width:40ch}
.route-body{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(20px,3vw,40px);align-items:start}
@media (max-width:900px){.route-body{grid-template-columns:1fr}}
.copy{display:grid;gap:14px;max-width:60ch}
.spec{margin:8px 0 0;display:grid;gap:0;border-top:1px solid var(--rule)}
.spec div{display:grid;grid-template-columns:120px 1fr;gap:12px;padding:9px 0;border-bottom:1px solid var(--rule)}
.spec dt{font:500 11px/1.6 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}
.spec dd{margin:0;font-size:15px;line-height:1.5}
.plates{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
@media (max-width:560px){.plates{grid-template-columns:1fr}}
.plates .span2{grid-column:1/-1}
.sc{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:.82em;letter-spacing:.08em}
.ladder{display:flex;align-items:flex-end;gap:clamp(8px,1.8vw,18px);justify-content:center}
.ladder div{display:grid;justify-items:center;gap:8px}
.ladder span{display:block}.ladder span svg{width:100%;height:100%;display:block}
.ladder small{font:500 10.5px 'IBM Plex Mono',ui-monospace,monospace;color:var(--ink-3);letter-spacing:.06em}
.apps{display:flex;flex-wrap:wrap;gap:18px;align-items:center;justify-content:center;width:100%}
.app{width:84px;height:84px;border-radius:20px;background:var(--ink);display:grid;place-items:center}.app svg{width:72%;height:72%}
.avatar{width:84px;height:84px;border-radius:50%;background:var(--paper);border:1px solid var(--rule);display:grid;place-items:center}.avatar svg{width:70%;height:70%}
.browser{width:100%;max-width:300px;background:#DAD4C6;border-radius:10px 10px 0 0;padding:7px 8px 0}
.tab{display:flex;align-items:center;gap:8px;background:var(--paper-hi);border-radius:8px 8px 0 0;padding:7px 11px;font:500 13px 'Instrument Sans',Arial,sans-serif;max-width:210px}
.fav{width:16px;height:16px;flex:none}.fav svg{width:16px;height:16px;display:block}
.tt{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.x{color:var(--ink-3)}
.url{background:var(--paper-hi);margin:0 -8px;padding:6px 14px;font:12px 'IBM Plex Mono',ui-monospace,monospace;color:var(--ink-2);border-top:1px solid var(--rule)}
.bcard{width:100%;max-width:320px;aspect-ratio:1.75;background:var(--ink);border-radius:5px;padding:20px 22px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 14px 30px -12px rgba(22,19,14,.45)}
.bmark{width:42%}.bmark svg{width:100%;height:auto;display:block}
.bline{display:flex;justify-content:space-between;align-items:baseline;gap:10px;color:var(--on-ink);font:500 10.5px 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase}
.bline b{font:600 14px 'Instrument Sans',Arial,sans-serif;letter-spacing:0;text-transform:none}
.doc{position:relative;width:100%;max-width:330px;background:#FBF8F1;padding:24px 24px 30px;box-shadow:0 12px 28px -14px rgba(22,19,14,.4);display:grid;gap:12px}
.doc-h{font:600 19px/1.2 'Instrument Sans',Arial,sans-serif;letter-spacing:-.01em;max-width:18ch}
.doc-lines{display:grid;gap:9px;margin-top:4px}.doc-lines i{display:block;height:6px;background:rgba(22,19,14,.1);width:100%}
.stamp{position:absolute;right:-14px;bottom:-18px;width:132px;transform:rotate(-11deg);mix-blend-mode:multiply;opacity:.9}.stamp svg{width:100%;height:auto;display:block}
.front{width:100%;display:grid;gap:10px}
.folio{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font:500 10.5px 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-2);border-bottom:1px solid var(--ink);padding-bottom:7px}
.front svg{width:100%;height:auto;display:block}
.front-kicker{font:500 10.5px 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--seal);border-top:3px double var(--ink);padding-top:12px}
.front-h{font:700 clamp(22px,3vw,34px)/1.02 'Instrument Sans',Arial,sans-serif;letter-spacing:-.025em;max-width:22ch}
.rec{padding-block:clamp(44px,6vw,84px);display:grid;gap:24px;border-bottom:1px solid var(--ink)}
.rec-body{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(20px,3vw,44px)}
@media (max-width:900px){.rec-body{grid-template-columns:1fr}}
.rec-body p{max-width:60ch}
.mast{width:100%;display:grid;gap:16px}
.mast-row{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,2.6fr) minmax(0,.62fr);gap:clamp(12px,2.4vw,32px);align-items:center}
@media (max-width:700px){.mast-row{grid-template-columns:1fr}.ear{max-width:260px}.ear-r{display:none}}
.mast svg{width:100%;height:auto;display:block}
.ear-r{justify-self:end;width:100%;max-width:120px}
.palette{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
@media (max-width:640px){.palette{grid-template-columns:repeat(2,minmax(0,1fr))}}
.chip{border:1px solid var(--rule);display:grid;align-content:end;min-height:120px;padding:12px;font:500 11px/1.5 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.06em;text-transform:uppercase}
.chip b{font:600 15px 'Instrument Sans',Arial,sans-serif;letter-spacing:0;text-transform:none}
.files{padding-block:clamp(40px,5vw,72px);display:grid;gap:18px}
.tree{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px 26px}
.tree-dir{display:grid;gap:2px;align-content:start;font:12.5px/1.6 'IBM Plex Mono',ui-monospace,monospace;color:var(--ink-2)}
.tree-dir b{font-weight:500;color:var(--ink);margin-bottom:4px}
.tree-dir span::before{content:'· ';color:var(--ink-3)}
footer{padding-top:22px;border-top:1px solid var(--ink);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
`;

const body = `
<main class="wrap">
  <header class="hero">
    <p class="eyebrow">Carat Capital · Identity routes · Round one · 26 September 2026</p>
    <h1>Five marks for the trade paper of the jewelry world</h1>
    <p class="lede">Each route starts from a fact of the trade that belongs to Carat Capital: a unit of weight, a punch, a cut, a coin, a proof mark. The stones are drawn to real cutting proportions and every letter is outlined, so the files are ready to use.</p>
    <div class="hero-grid">${hero}</div>
  </header>
  <section class="finds">
    <p class="eyebrow">What the routes are built on</p>
    <h2>Six facts from the trade</h2>
    <div class="finds-grid">${finds}</div>
  </section>
  ${routeHTML}
  <section class="rec" id="recommendation">
    <p class="eyebrow">Recommendation</p>
    <h2>Lead with The Point</h2>
    <div class="rec-body">
      <p>The Point is the only route that stays clear as a 16-pixel favicon and still carries a full story at poster size. It also grows out of the nib-and-diamond mark the paper uses today, so readers keep what they already recognise.</p>
      <p>Keep The Solidus as the paper’s seal for anything that certifies: the editorial standards, the price lists and the Almanac. Run The Hallmark strip in the masthead ear, where the edition number changes every morning. The Step Cut and The Insertion stay in reserve for a luxury sub-brand and for print.</p>
    </div>
    ${masthead}
    <div class="palette">
      <div class="chip" style="background:#F2EDE3"><b>Paper</b>#F2EDE3</div>
      <div class="chip" style="background:#16130E;color:#F2EDE3;border-color:#16130E"><b>Ink</b>#16130E</div>
      <div class="chip" style="background:#BE3319;color:#F2EDE3;border-color:#BE3319"><b>Seal</b>#BE3319</div>
      <div class="chip" style="background:linear-gradient(135deg,#7A5E1F,#D9B45E 38%,#F1DFA4 55%,#D9B45E 72%,#8A6C28);color:#16130E;border-color:#96762E"><b>Gilt foil</b>#7A5E1F → #F1DFA4</div>
    </div>
    <p class="eyebrow">Every route keeps the paper’s existing colours</p>
  </section>
  <section class="files">
    <p class="eyebrow">Files</p>
    <h2>33 SVGs, ready to use</h2>
    <p class="lede">Type is converted to outlines and knockouts are transparent masks, so every file renders the same everywhere and sits on any background.</p>
    <div class="tree">${tree}</div>
  </section>
  <footer><p class="eyebrow">Carat Capital · caratcapital.org</p><p class="eyebrow">Round one · for review</p></footer>
</main>`;

const fontLink = `<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,500;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">`;
const artifact = `<title>Carat Capital Identity</title>\n${fontLink}\n<style>${css}</style>\n${body}\n`;
const repoDoc = `<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Carat Capital Identity</title>\n${fontLink}\n<style>${css}</style></head><body>${body}</body></html>\n`;


fs.writeFileSync(require('path').join(__dirname, '..', 'index.html'), repoDoc);
console.log('artifact', (artifact.length / 1024).toFixed(0) + 'KB');
