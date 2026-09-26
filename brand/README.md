# Carat Capital identity, round one

Five logo routes for Carat Capital, each built on a fact from the trade. Open `index.html` for the full presentation: rationale, construction drawings, scale tests and applications. The page is marked `noindex`.

| Route | Idea | Primary files |
| --- | --- | --- |
| 01 The Point | A brilliant in profile (34.5° crown, 56% table) whose pavilion is also a pen nib. The breather hole holds a red point: printers set type in points, dealers weigh stones in points (1 pt = 0.01 ct). | `logos/01-the-point/lockup.svg`, `symbol.svg`, `symbol-small.svg` |
| 02 The Hallmark | C◆C struck in a punch like a maker's mark, plus a masthead strip: sponsor's mark, edition number as the fineness figure, office mark, date letter. | `logos/02-the-hallmark/lockup.svg`, `mark-foil.svg`, `hallmark-strip.svg` |
| 03 The Step Cut | An emerald cut with a slot in its side is a C. The name is set in bespoke octagonal titling drawn for its seven letters. | `logos/03-the-step-cut/lockup.svg`, `symbol-gold.svg` |
| 04 The Solidus | A coin seal: 24 carob seeds (the origin of carat and of 24 karat) around an engraved round brilliant. Legend: PONDERE · ET · FIDE, by weight and by good faith. | `logos/04-the-solidus/seal.svg`, `seal-simple.svg` |
| 05 The Insertion | The proofreader's caret is a stone laid table-down. The nameplate inserts one between CARAT and CAPITAL. | `logos/05-the-insertion/nameplate.svg`, `monogram.svg` |

**Recommendation:** lead with The Point, use The Solidus as the seal for anything that certifies (standards, price lists, the Almanac), and run The Hallmark strip in the masthead ear.

## Files

- `logos/` — 33 SVGs. Type is outlined and knockouts are transparent masks, so each file works on any background. `-reverse` files are for dark grounds; `-small` and `-simple` files are cut for 16–48 px.
- `png/` — 1024 px avatars and icons for social profiles and app stores.
- `source/` — the generator. Every mark is computed from geometry, so proportions can be changed in `routes.js` and rebuilt:

```sh
cd brand/source
npm install && ./fonts.sh     # opentype.js + the five OFL typefaces used
node present.js               # writes logos/**/*.svg and index.html
node export.js                # writes png/ (needs Playwright + Chromium)
```

Typefaces (all SIL Open Font License): Bodoni Moda, Castoro Titling, Gloock, IBM Plex Mono. The Step Cut titling is drawn from scratch.
