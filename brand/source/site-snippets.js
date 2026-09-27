// Prints the three drawings the site templates embed, into build/snippets/. Paste them into:
//   favicon.svg     -> FAVICON in build.py
//   logo-mark.svg   -> LOGO_MARK in build.py
//   medal.svgfrag   -> the <mask id="medal-k"> + <symbol id="medal"> in build.py DEFS and home_template.html
const Pn = require('./point'); const { C } = require('./lib'); const fs = require('fs'); const path = require('path');
const out = path.join(__dirname, 'build', 'snippets'); fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, 'favicon.svg'), Pn.favicon());
fs.writeFileSync(path.join(out, 'logo-mark.svg'), Pn.symbol({ cut: 'S', tight: true }).replace(/id="k/g, 'id="lm').replace(/url\(#k/g, 'url(#lm'));
const m = Pn.mark({ fg: 'currentColor', dot: C.seal, cut: 'M', cx: 500, top: (1000 - Pn.G.H) / 2 - 8 });
fs.writeFileSync(path.join(out, 'medal.svgfrag'), m.defs.replace(/id="k[0-9a-z]+"/, 'id="medal-k"') + '<symbol id="medal" viewBox="0 0 1000 1000">' + m.body.replace(/url\(#k[0-9a-z]+\)/, 'url(#medal-k)') + '</symbol>');
console.log('snippets in', out);
