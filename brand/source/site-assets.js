const Pn = require('./point'); const { C } = require('./lib'); const { raster } = require('./raster');
const A = require('path').join(__dirname, '..', '..', 'assets');
const center = (bg, svg, wpct) => `<div style="width:100%;height:100%;background:${bg};display:grid;place-items:center"><div style="width:${wpct}%">${svg.replace('<svg', '<svg style="display:block;width:100%;height:auto"')}</div></div>`;
const card = `<div style="width:1200px;height:630px;background:${C.paper};position:relative;display:grid;place-items:center">
  <div style="position:absolute;inset:34px;border:2px solid ${C.ink}"></div><div style="position:absolute;inset:42px;border:1px solid rgba(22,19,14,.35)"></div>
  <div style="width:800px">${Pn.lockup({ pad: 0 }).replace('<svg', '<svg style="display:block;width:100%;height:auto"')}</div>
  <div style="position:absolute;bottom:62px;left:0;right:0;text-align:center;font:500 15px/1 'DejaVu Sans Mono',monospace;letter-spacing:.3em;color:${C.ink2}">CARATCAPITAL.ORG</div></div>`;
raster([
  [`${A}/share-card.png`, card, 1200, 630],
  [`${A}/apple-touch-icon.png`, center(C.ink, Pn.symbol({ cut: 'M', fg: C.paper, tight: true }), 68), 180, 180],
  [`${A}/cc-icon-1024.jpg`, center(C.paper, Pn.symbol({ cut: 'L', tight: true }), 70), 1024, 1024, 'jpeg'],
]).then(() => console.log('site assets written'));
