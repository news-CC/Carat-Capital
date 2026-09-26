# Carat Capital brand

The identity is **The Point**: a round brilliant seen from the side whose pavilion is also a pen nib. The nib's breather hole holds a red point, because printers set type in points and diamond dealers weigh stones in points (1 pt = 0.01 ct). The same point closes the wordmark, *Carat Capital.*, set in Bodoni Moda 500.

- **Brand book:** [`brand-book.html`](brand-book.html) (web, `noindex`) and [`Carat-Capital-Brand-Book.pdf`](Carat-Capital-Brand-Book.pdf), 18 pages: idea, anatomy, construction, optical sizes, the engraved cut, wordmark, lockups, clear space, colour, typography, misuse and applications.
- **Logo kit:** [`logo/`](logo)
  - `svg/` lockups (horizontal, stacked, wordmark) in ink, reverse, gold and one-colour; the symbol in L, M and S cuts, gold and engraved
  - `png/` transparent PNGs of the lockups and symbols
  - `favicon/` favicon.svg (turns paper-coloured in dark browsers), favicon.ico (16/32/48), apple-touch-icon, 192/512 icons
  - `social/` avatars on Paper and Ink, and the 1200 × 630 share card
- **Round one:** [`round-one/`](round-one) holds the five routes this identity was chosen from.

## On the site

The site builds every page from `build.py` and `home_template.html`, so the mark is set there:

| Where | What changed |
| --- | --- |
| `build.py` | Nav bar, menu and footer wordmark; the Folio cover; `FAVICON`; `LOGO_MARK` (the nav symbol); the `#medal` symbol; the assay hallmark; Bodoni Moda in `FONTS`; share image and apple-touch-icon in `head()` |
| `home_template.html` | Front-page masthead, top bar, menu, loader and footer; `#medal`; the assay hallmark; share image |
| `assets/styles.css` | Wordmark styles and the drawn point (`.pt`: 0.16 em, on the baseline) |
| `seo.py` | Default share image |
| `assets/` | `share-card.png`, `apple-touch-icon.png`, and `cc-icon-1024.jpg` (the schema.org logo) redrawn |

The deploy workflow still generates the old text-only `assets/og-card.png`. Nothing references it any more, so that step can be deleted from `.github/workflows/build.yml` whenever convenient.

## Source

Every drawing is computed from the geometry in [`source/point.js`](source/point.js). Change a proportion there and rebuild:

```sh
cd brand/source
./fonts.sh && npm install --no-save opentype.js@1.3.4   # the OFL typefaces + outlining
node kit.js            # logo/ (SVG, PNG, favicon, social)
node site-assets.js    # assets/share-card.png, apple-touch-icon.png, cc-icon-1024.jpg
node site-snippets.js  # build/snippets: paste into FAVICON, LOGO_MARK and #medal (see file header)
cd ../.. && python3 build.py && cd brand/source
node site-caps.js      # screenshots of the built site for the book
node book.js && node pdf.js   # brand-book.html and the PDF
```

The scripts render with Playwright and Chromium. Typefaces (SIL Open Font License): Bodoni Moda, IBM Plex Mono; round one also uses Castoro Titling and Gloock.
