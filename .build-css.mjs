import postcss from 'postcss';
import tw from '@tailwindcss/postcss';
import fs from 'node:fs';
const css = fs.readFileSync('/home/msd/ai-workspace/salon-man/src/app/globals.css', 'utf8');
const out = await postcss([tw({ optimize: false })]).process(css, {
  from: '/home/msd/ai-workspace/salon-man/src/app/globals.css',
});
fs.writeFileSync('/tmp/claude-1000/-home-msd-ai-workspace-salon-man/e719906e-4515-4ce7-ae8f-69b098289863/scratchpad/out.css', out.css);
console.log('bytes', out.css.length);
