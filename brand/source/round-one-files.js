// Writes the logo files into the repo (brand/logos/**) and the presentation page.
const R = require('./routes'); const { C } = require('./lib'); const fs = require('fs'); const path = require('path');
const REPO = path.join(__dirname, '..', 'round-one');
const P = C.paper, I = C.ink, S = C.seal;
const files = {
  '01-the-point': {
    'symbol.svg': R.pointSymbol({}), 'symbol-reverse.svg': R.pointSymbol({ fg: P }), 'symbol-small.svg': R.pointSymbol({ size: 'small' }),
    'symbol-small-reverse.svg': R.pointSymbol({ size: 'small', fg: P }), 'lockup.svg': R.pointLockup({}), 'lockup-reverse.svg': R.pointLockup({ fg: P }),
    'lockup-no-tagline.svg': R.pointLockup({ tag: false }), 'construction.svg': R.pointConstruction({}),
  },
  '02-the-hallmark': {
    'mark.svg': R.hallmarkSymbol({}), 'mark-reverse.svg': R.hallmarkSymbol({ field: P }), 'mark-foil.svg': R.hallmarkSymbol({ foil: true }),
    'lockup.svg': R.hallmarkLockup({}), 'lockup-reverse.svg': R.hallmarkLockup({ fg: P }), 'hallmark-strip.svg': R.hallmarkStrip({}), 'hallmark-strip-reverse.svg': R.hallmarkStrip({ fg: P }),
  },
  '03-the-step-cut': {
    'symbol.svg': R.stepCutSymbol({}), 'symbol-reverse.svg': R.stepCutSymbol({ fg: P }), 'symbol-gold.svg': R.stepCutSymbol({ gold: true }), 'symbol-solid.svg': R.stepCutSymbol({ kw: 0 }),
    'lockup.svg': R.stepCutLockup({}), 'lockup-reverse.svg': R.stepCutLockup({ fg: P }), 'lockup-stacked.svg': R.stepCutLockup({ stacked: true }),
    'lockup-stacked-gold.svg': R.stepCutLockup({ stacked: true, gold: true, fg: C.foilB }), 'construction.svg': R.stepCutConstruction({}),
  },
  '04-the-solidus': { 'seal.svg': R.solidusSeal({}), 'seal-reverse.svg': R.solidusSeal({ fg: P }), 'seal-simple.svg': R.solidusSeal({ detail: 'simple' }), 'seal-simple-reverse.svg': R.solidusSeal({ detail: 'simple', fg: P }) },
  '05-the-insertion': {
    'nameplate.svg': R.insertionNameplate({}), 'nameplate-reverse.svg': R.insertionNameplate({ fg: P }), 'nameplate-no-tagline.svg': R.insertionNameplate({ rule: false }),
    'monogram.svg': R.insertionMonogram({}), 'monogram-reverse.svg': R.insertionMonogram({ fg: P }),
  },
};
const header = '<?xml version="1.0" encoding="UTF-8"?>\n<!-- Carat Capital identity, round one. Outlined type; knockouts are transparent masks. -->\n';
let total = 0;
for (const [dir, set] of Object.entries(files)) {
  fs.mkdirSync(path.join(REPO, 'logos', dir), { recursive: true });
  for (const [name, svgStr] of Object.entries(set)) { fs.writeFileSync(path.join(REPO, 'logos', dir, name), header + svgStr + '\n'); total++; }
}
console.log('svg files', total);
module.exports = { files };
