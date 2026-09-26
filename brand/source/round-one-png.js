const { chromium } = require('playwright');
const R = require('./routes'); const { C } = require('./lib'); const fs = require('fs');
const out = require('path').join(__dirname, '..', 'round-one', 'png'); fs.mkdirSync(out, { recursive: true });
const jobs = [
  ['01-the-point-avatar.png', R.pointSymbol({}), C.paper, 0.70],
  ['01-the-point-app-icon.png', R.pointSymbol({ fg: C.paper, size: 'small' }), C.ink, 0.74],
  ['02-the-hallmark-foil.png', R.hallmarkSymbol({ foil: true }), C.ink, 0.78],
  ['03-the-step-cut-gold.png', R.stepCutSymbol({ gold: true }), C.ink, 0.64],
  ['04-the-solidus-seal.png', R.solidusSeal({}), C.paper, 0.84],
  ['05-the-insertion-monogram.png', R.insertionMonogram({ fg: C.paper, stone: C.ink }), C.seal, 0.66],
];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1024, height: 1024 } });
  for (const [name, svg, bg, frac] of jobs) {
    await p.setContent(`<body style="margin:0;width:1024px;height:1024px;background:${bg};display:grid;place-items:center"><div style="width:${frac * 1024}px">${svg.replace('<svg', '<svg style="display:block;width:100%;height:auto"')}</div></body>`);
    await p.screenshot({ path: `${out}/${name}` });
  }
  await b.close(); console.log('png', jobs.length);
})();
