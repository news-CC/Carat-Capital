#!/usr/bin/env python3
# Carat Capital — static site builder (Third Edition, content-driven)
# Content lives in content/articles.json + content/wire.json — edit those, re-run this.
import html as H
import json, pathlib

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content"
ARTICLES = json.loads((CONTENT / "articles.json").read_text()) if (CONTENT / "articles.json").exists() else []
ARTICLES.sort(key=lambda a: a.get("date", ""), reverse=True)
WIRE = json.loads((CONTENT / "wire.json").read_text()) if (CONTENT / "wire.json").exists() else {}
RECORD = json.loads((CONTENT / "record.json").read_text()) if (CONTENT / "record.json").exists() else {}

def lead_article():
    for a in ARTICLES:
        if a.get("lead"):
            return a
    return ARTICLES[0] if ARTICLES else None

def desk_articles(slug, n=6):
    return [a for a in ARTICLES if a.get("desk") == slug][:n]

FONTS = "https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400..700;1,400..700&family=Lora:ital,wght@0,400..700;1,400..700&family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&display=swap"

DEFS = """
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<defs>
  <linearGradient id="foilFill" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#8A6C28"/><stop offset=".3" stop-color="#D9B45E"/>
    <stop offset=".48" stop-color="#F1DFA4"/><stop offset=".62" stop-color="#B08F3F"/>
    <stop offset=".85" stop-color="#D9B45E"/><stop offset="1" stop-color="#7A5E1F"/>
  </linearGradient>
  <pattern id="engrave" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(-42)">
    <rect width="4" height="4" fill="none"/><line x1="0" y1="0" x2="0" y2="4" stroke="#16130E" stroke-width="1.1"/>
  </pattern>
  <g id="hm-maker">
    <path d="M16 1 L31 10 L16 19 L1 10 Z" fill="url(#foilFill)" stroke="currentColor" stroke-width="1.2"/>
    <text x="16" y="13.6" text-anchor="middle" font-family="'IBM Plex Mono',monospace" font-size="8.5" font-weight="600" letter-spacing="1" fill="currentColor">CC</text>
  </g>
  <g id="hm-fine">
    <path d="M6 1 h14 l5 5 v8 l-5 5 H6 l-5-5 V6 Z" fill="url(#foilFill)" stroke="currentColor" stroke-width="1.2"/>
    <text x="13" y="13.8" text-anchor="middle" font-family="'IBM Plex Mono',monospace" font-size="8" font-weight="600" letter-spacing=".5" fill="currentColor">750</text>
  </g>
  <g id="hm-assay">
    <ellipse cx="13" cy="10" rx="12" ry="9" fill="url(#foilFill)" stroke="currentColor" stroke-width="1.2"/>
    <path d="M8.5 13 L13 6.5 L17.5 13" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <g id="hm-date">
    <rect x="1" y="1" width="18" height="18" rx="4" fill="url(#foilFill)" stroke="currentColor" stroke-width="1.2"/>
    <text x="10" y="14.6" text-anchor="middle" font-family="'Lora',serif" font-style="italic" font-size="11.5" fill="currentColor">a</text>
  </g>
</defs>
</svg>"""

HALLROW = """<div class="hall" aria-label="Carat Capital hallmark" style="color:var(--ink)">
  <svg width="34" height="21" viewBox="0 0 32 20"><use href="#hm-maker"/></svg>
  <svg width="28" height="21" viewBox="0 0 26 20"><use href="#hm-fine"/></svg>
  <svg width="28" height="21" viewBox="0 0 26 20"><use href="#hm-assay"/></svg>
  <svg width="21" height="21" viewBox="0 0 20 20"><use href="#hm-date"/></svg>
</div>"""

DESKS = [
 dict(no="01", slug="diamonds", nav="Diamonds", title="Diamonds",
   tag="the stone that runs on trust",
   dek="Rough and polished, natural and mined, priced sight by sight. The diamond desk follows the pipeline end to end — producer sales in Gaborone, tenders in Antwerp and Dubai, manufacturing in Surat, memo programs in New York — and publishes the prices the trade actually deals at.",
   stats=[("$5,240","1ct RBC · D/IF, today"),("−22%","Rough supply vs 2020"),("6","Borders per stone, avg.")],
   motif="diamond",
   briefing=[
     ("B-01","Producers hold the line on rough","De Beers-style supply discipline is back: allocations trimmed, prices defended. Polished has stabilized after two brutal years — the question is whether midstream margins recover before credit patience runs out.","Supply · Gaborone"),
     ("B-02","The 86% gap becomes the strategy","With lab-grown 1ct goods under $750, natural sellers have stopped competing on price and started competing on account of provenance, rarity and resale. Watch the marketing budgets, not the price lists.","Positioning · Global"),
     ("B-03","Traceability goes from virtue to invoice","Origin platforms are no longer CSR decoration — G7 rules and retailer mandates are making sourcing paperwork a condition of sale. Compliant goods are starting to command a measurable premium.","Regulation · Antwerp"),
   ],
   glossary=[
     ("The Sight","Term","De Beers' ten-times-a-year allocation sale, where approved buyers — sightholders — purchase rough in pre-assembled boxes at prices set by the producer. Refusing a box has consequences; so does needing one."),
     ("Four Cs vs. the fifth","Concept","Carat, color, clarity, cut set the grade — but the trade increasingly prices a fifth C: certainty of origin. Two identical stones can part ways on price over a paper trail."),
     ("Midstream squeeze","Dynamic","Miners set rough prices, retailers set polished prices, and the cutters and traders in between absorb the difference. When both ends tighten at once, Surat and Antwerp bleed first — the industry's recurring crisis."),
     ("Memo","Practice","Goods consigned to retailers on memorandum — sold before they're paid for. Memo keeps counters full and balance sheets fragile; its terms are one of the best barometers of trade confidence."),
   ],
   stories=[
     ("Gold at $4,100 is quietly redrawing the entire map of the jewelry trade","Lighter mountings, re-cut margins — and a diamond demand ripple nobody has priced yet.","Lead · 8 min"),
     ("Inside the sight: what the boxes said this month","Allocations read like a mood ring for the whole pipeline. This month's mood: cautious defiance.","Gaborone · 6 min"),
     ("The 86% question nobody in Surat will answer aloud","Lab-grown slipped again. The polishing capital's answer is a pivot two years in the making.","Surat · 7 min"),
     ("Antwerp's tender season opens hot on fancy color","Pinks and vivid yellows clear well above reserve while white melee stays soft.","Antwerp · 4 min"),
     ("Provenance premiums are now measurable — we measured them","Certified-origin goods are clearing 3–5% over identical uncertified stones. The paper is the product.","Data · 5 min"),
   ]),
 dict(no="02", slug="gold-metals", nav="Gold", title="Gold & Metals",
   tag="the metal beneath every margin",
   dek="Bullion is the jewelry industry's weather. The metals desk files the morning note on gold, silver, platinum and palladium — then follows the price into the workshop: hallmarking policy, recycling flows, hollow-chain engineering and what $4,000-plus gold does to every counter in the world.",
   stats=[("$4,115","Gold/oz · this morning"),("+31%","Gold, trailing 12 months"),("~50%","Of demand is jewelry")],
   motif="ingot",
   briefing=[
     ("B-01","$4,135 at the open — the new normal hardens","Another higher open Friday. Central-bank buying and haven flows keep the floor rising, and manufacturers have stopped waiting for a retreat: product architecture is being redesigned around the price.","Bullion · New York"),
     ("B-02","The lightweighting revolution","Hollow forms, electroforming, 9k and 10k revivals, silver-gilt hybrids — the craft of making less metal look like more is the decade's quiet growth industry. Vicenza and Shenzhen lead.","Manufacturing · Vicenza"),
     ("B-03","Recycling becomes a supply line","At these prices, the scrap drawer is a mine. Old-gold buybacks are now a strategic sourcing channel for refiners and brands alike — with its own pricing, logistics and fraud problems.","Supply · Global"),
   ],
   glossary=[
     ("Hallmark","Term","The assay office's stamped guarantee of fineness — 750 for 18k, 916 for 22k. The oldest consumer-protection system in the world, and the inspiration for this paper's own mark."),
     ("Making charge","Practice","The labor and design fee added over the metal's melt value — the jeweler's actual margin. When gold spikes, making charges get squeezed first; watch them to see who holds pricing power."),
     ("Fineness ladder","Concept","24k is pure; 22k, 18k, 14k, 10k and 9k trade purity for durability and price. Bull markets in bullion push whole countries down a rung — India's 18k boom is this cycle's signature."),
     ("Melt value","Metric","What a piece is worth as raw metal, ignoring craft entirely. The gap between melt and retail is where brand, design and trust live — and it's the number every buyback desk starts from."),
   ],
   stories=[
     ("Morning bullion note: gold opens 1.2% higher at $4,135","Futures firm overnight on haven flows; silver and platinum follow.","Bullion · 3 min"),
     ("How Vicenza learned to make more jewelry with less gold","Inside the hollow-chain engineering arms race remaking Italian manufacturing.","Vicenza · 7 min"),
     ("India shrugs at $4,000 gold — wedding season doesn't wait","Volumes dip, values soar. The world's largest gold-jewelry market adapts in real time.","Mumbai · 5 min"),
     ("The scrap-gold gold rush","Buyback desks, melt logistics and the fraud fight inside recycling's boom.","Supply · 6 min"),
     ("Platinum's stealth rally is finally reaching the counter","At a widening discount to gold, the once-premium metal becomes the value play.","Metals · 4 min"),
   ]),
 dict(no="03", slug="gemstones", nav="Gems", title="Colored Gemstones",
   tag="supply lines drawn in emerald, ruby and sapphire",
   dek="The most opaque corner of the trade — and the most alive. The gemstone desk tracks auction results from Zambian emerald and Mozambican ruby tenders, the cutting rooms of Bangkok and Jaipur, treatment disclosure fights, and the collector demand pushing top stones past diamonds.",
   stats=[("+12%","Fine sapphire, YoY"),("80%+","Of rubies transit Bangkok"),("3","Stones rule: E · R · S")],
   motif="gem",
   briefing=[
     ("B-01","The big three outrun diamonds again","Untreated Burmese rubies, Kashmir-quality sapphire and vivid Colombian emerald keep setting per-carat records. Scarcity is structural: the great mines are old and the new finds are small.","Market · Global"),
     ("B-02","Origin is the price","A ruby's passport matters as much as its color. Lab reports naming Mogok or Kashmir multiply value — which makes origin science, and origin fraud, the desk's permanent beat.","Certification · Lucerne"),
     ("B-03","Tender economics tighten midstream","Producer tenders in Zambia and Mozambique now set benchmark rough prices with auction transparency — squeezing the traditional dealer margin and professionalizing a famously handshake market.","Supply · Lusaka"),
   ],
   glossary=[
     ("The Big Three","Term","Emerald, ruby, sapphire — the trio that anchors colored-stone value. Everything else, however beautiful, trades as 'semi-precious' economics with rare exceptions like paraíba and spinel."),
     ("Treatment disclosure","Practice","Most gems are heated, oiled or filled to improve appearance; the sin isn't treatment, it's silence. 'No indications of heating' on a lab report can multiply a stone's price tenfold."),
     ("Origin determination","Science","Labs read a stone's chemistry and inclusions like a birth certificate — Mogok ruby, Panjshir emerald, Ceylon sapphire. It's expert judgment, not barcode certainty, and labs occasionally disagree."),
     ("Pigeon's blood","Grade","The trade's most contested color term: the pure vivid red, historically Burmese, that marks the summit of the ruby market. Whose lab gets to say it is a running commercial war."),
   ],
   stories=[
     ("Zambian emerald tender clears 14% above expectations","Auction transparency keeps repricing the whole green supply chain.","Lusaka · 5 min"),
     ("The Odyssey effect — ancient-world jewelry is about to have its moment","Nolan's epic has buyers hunting intaglios, granulation and antique cuts.","Trends · 6 min"),
     ("Bangkok's cutting rooms bet big on sapphire","The world's colored-stone capital retools for the blue decade.","Bangkok · 6 min"),
     ("When labs disagree: inside a $2m origin dispute","Two reports, two origins, one very expensive ruby. A case study in gem science's limits.","Certification · 8 min"),
     ("Spinel completes its climb from consolation prize to headline","The connoisseur's secret is now on maison counters at maison prices.","Market · 4 min"),
   ]),
 dict(no="04", slug="watches", nav="Watches", title="Watches",
   tag="haute horlogerie, priced by the second",
   dek="Where jewelry meets machinery and the secondary market never sleeps. The watch desk reads Swiss export data, brand strategy and auction results — and tracks the collector indices that turned wristwatches into an asset class with a service manual.",
   stats=[("CHF 26B","Swiss exports, annualized"),("−8%","Secondary index vs peak"),("70%","Of value: top 4 brands")],
   motif="watch",
   briefing=[
     ("B-01","World Cup summer becomes a watch story","Diamond-set footballs, athlete ambassadors, limited editions timed to the tournament — the industry is spending the summer converting football fever into waiting lists.","Marketing · Geneva"),
     ("B-02","The secondary market finds its floor","After the 2022–24 correction, blue-chip references have stabilized. Dealers report clean two-way trade again — the speculative froth is gone, the collector base isn't.","Secondary · Global"),
     ("B-03","Steel sports scarcity is policy, not accident","Waiting lists for steel icons persist because supply discipline works. The desks reads allocation strategy the way the diamond desk reads the sight.","Strategy · Biel"),
   ],
   glossary=[
     ("Grey market","Term","Unauthorized but legal dealers trading new watches outside official channels. Grey premiums and discounts are the truest real-time price signal in the industry — we quote them daily."),
     ("Manufacture","Concept","A maison that builds its own movements rather than buying them. The word carries a price premium and a century of Swiss industrial politics."),
     ("Reference","Practice","A watch's model number — collectors trade references the way equity desks trade tickers. One digit can double a price at auction."),
     ("Complication","Term","Any function beyond telling the time: chronograph, perpetual calendar, minute repeater. Complexity is the currency of horological prestige — and of service costs."),
   ],
   stories=[
     ("World Cup gold rush: watchmakers bet the summer on football","Inside the tournament marketing offensive from Geneva to Miami.","Geneva · 4 min"),
     ("Swiss exports hold as America buys the dip","The US overtakes on volume while Asia consolidates on value.","Data · 5 min"),
     ("The steel waiting list, decoded","Allocation strategy is the industry's most effective pricing machine. Here's how it works.","Strategy · 7 min"),
     ("Independents keep outrunning the majors at auction","Small-series watchmaking is the collector story of the decade.","Auctions · 5 min"),
     ("America 250 editions land on the wrist","Heritage dials and anniversary references join the patriotic product wave.","Market · 3 min"),
   ]),
 dict(no="05", slug="auctions", nav="Auctions", title="Auctions & Estates",
   tag="where the trade marks itself to market",
   dek="Every hammer price is a data point the whole industry reprices against. The auction desk previews and reports the jewelry sales at Christie's, Sotheby's, Phillips and Bonhams, tracks private treaty and estate flows, and reads provenance the way analysts read balance sheets.",
   stats=[("$1.1B","Annual jewelry hammer, est."),("×3.2","Provenance premium, avg."),("2","Capitals: GVA · HKG")],
   motif="gavel",
   briefing=[
     ("B-01","Signed period jewels carry the season","Cartier Art Deco, JAR, early Bulgari — signed and dated material clears high estimates while generic goods labor. The market is paying for authorship, not just material.","Results · Geneva"),
     ("B-02","Estate supply is the decade's quiet flood","Generational wealth transfer is bringing decades of collections to market. The houses are building entire departments to catch it — and the trade buys its future inventory there.","Supply · New York"),
     ("B-03","Private sales eat the middle","Six-figure stones increasingly trade by private treaty instead of the room — faster, quieter, fee-flexible. The public sale is becoming the shop window; the deal happens after.","Structure · Global"),
   ],
   glossary=[
     ("Hammer vs. premium","Term","The hammer price is what the gavel confirms; the buyer's premium (20–27%) goes to the house on top. Read carefully: reports mix the two, and the difference is the house's entire business."),
     ("Provenance","Concept","A jewel's chain of ownership. A documented duchess multiplies value like a lab report multiplies a ruby's — history is the one gem that can't be mined."),
     ("Reserve","Practice","The confidential minimum below which a lot won't sell. 'Bought in' means the reserve wasn't met — auction-speak for a price the market refused."),
     ("Fresh to market","Signal","A piece unseen for decades. Freshness is the auction world's scarcity premium; a jewel flipped twice in five years trades tired."),
   ],
   stories=[
     ("Geneva magnificent jewels: signed Deco clears the century mark","Cartier and Van Cleef period pieces triple estimates in a selective room.","Geneva · 6 min"),
     ("The estate flood is here — and the trade is the buyer","How dealers restock from the greatest wealth transfer in history.","New York · 7 min"),
     ("Private treaty: the auction you never see","More top stones now trade behind the room than in it. Inside the quiet market.","Structure · 6 min"),
     ("A duchess's clip and the mathematics of provenance","Case study: same stones, 3.2× the price. History priced per carat.","Analysis · 5 min"),
     ("Hong Kong preview: jadeite tests the ceiling again","Imperial green returns to the block with an eight-figure ambition.","Hong Kong · 4 min"),
   ]),
 dict(no="06", slug="retail-tech", nav="Retail", title="Retail & Technology",
   tag="the counter, rebuilt for the next generation",
   dek="Where the industry meets its customer — and its future. The retail desk covers lab-grown economics, e-commerce and live-selling, traceability tech, AI in the showroom, and the store formats winning buyers who are 24, online at midnight, and allergic to velvet ropes.",
   stats=[("$720","Lab-grown 1ct, retail"),("~20%","Of sales now online"),("24","Median first-buyer age")],
   motif="store",
   briefing=[
     ("B-01","Lab-grown settles into its true business model","At an 86% discount to natural, LGD is no longer a diamond substitute — it's a fashion-jewelry category with diamond optics. Margins migrate from the stone to the brand and the volume.","Economics · Global"),
     ("B-02","Live selling jumps the Pacific","The livestream counter that built China's jewelry e-commerce is landing in the West — TikTok gem sales, WhatsApp private clienteling, and jewelers becoming broadcasters.","Channels · Shenzhen"),
     ("B-03","Traceability tech grows teeth","Blockchain provenance, ledgers, and assay-office digital passports move from pilot to mandate as regulation and retailer policy converge. The tech stack becomes a condition of shelf space.","Technology · London"),
   ],
   glossary=[
     ("Lab-grown (LGD)","Term","Diamonds grown in weeks by HPHT or CVD — chemically identical to mined, economically a different universe. Their price curve is a technology curve, which is the whole story."),
     ("Clienteling","Practice","One-to-one retail relationship management — the private-client WhatsApp thread, remembered anniversaries, first calls on new goods. The oldest luxury skill, now run on software."),
     ("Omnichannel","Concept","The customer researches at midnight, tries on Saturday, buys by DM on Tuesday. Winning retailers price, stock and staff as one continuous counter across all of it."),
     ("Digital product passport","Regulation","An EU-led ID standard giving each piece a scannable record of origin, materials and custody. Coming for jewelry the way nutrition labels came for food."),
   ],
   stories=[
     ("Lab-grown slips again — the 86% question nobody will answer aloud","The discount widened. The business model finally makes sense. Both are true.","Economics · 7 min"),
     ("The midnight counter: how 24-year-olds actually buy emeralds","Live streams, DMs and the death of the appointment. A field study.","Channels · 8 min"),
     ("America 250: heritage houses mint an anniversary economy","The patriotic product wave is a retail calendar event now.","New York · 4 min"),
     ("The digital product passport is coming for your inventory","What the EU standard means for every stockroom, explained.","Regulation · 6 min"),
     ("Store of the decade: the jeweler as broadcaster","Shenzhen's livestream studios are the new flagship format.","Shenzhen · 5 min"),
   ]),
]

MOTIFS = dict(
 diamond="""<g stroke="#16130E" fill="none"><path d="M210 40 L300 96 L210 186 L120 96 Z" stroke-width="1.6" stroke-linejoin="round"/><path d="M120 96 H300 M210 40 L168 96 L210 186 L252 96 Z" stroke-width=".8"/><g stroke-width=".4" opacity=".6"><path d="M135 86 L168 52 M147 92 L186 46 M192 44 L150 96"/><path d="M285 86 L252 52 M273 92 L234 46 M228 44 L270 96"/></g><circle cx="210" cy="96" r="3" fill="#BE3319" stroke="none"/></g>""",
 ingot="""<g stroke="#16130E" fill="none"><path d="M140 128 h84 l22 40 H118 Z" stroke-width="1.6" stroke-linejoin="round"/><path d="M172 68 h84 l22 40 h-128 Z" stroke-width="1.6" stroke-linejoin="round"/><g stroke-width=".4" opacity=".6"><path d="M130 150 h110 M126 158 h118 M182 84 h86 M178 92 h94"/></g><text x="210" y="152" text-anchor="middle" font-family="'IBM Plex Mono',monospace" font-size="12" letter-spacing="2" fill="#16130E" stroke="none">999.9</text></g>""",
 gem="""<g stroke="#16130E" fill="none"><path d="M160 60 h100 l34 34 v50 l-34 34 h-100 l-34 -34 v-50 Z" stroke-width="1.6" stroke-linejoin="round"/><path d="M182 84 h56 l22 22 v26 l-22 22 h-56 l-22 -22 v-26 Z" stroke-width=".8"/><g stroke-width=".4" opacity=".6"><path d="M160 60 L182 84 M260 60 L238 84 M294 94 L260 132 M126 94 L160 132 M160 178 L182 154 M260 178 L238 154"/></g><circle cx="210" cy="119" r="3" fill="#BE3319" stroke="none"/></g>""",
 watch="""<g stroke="#16130E" fill="none"><circle cx="210" cy="118" r="62" stroke-width="1.6"/><circle cx="210" cy="118" r="52" stroke-width=".7"/><path d="M210 82 V118 L238 138" stroke-width="1.4" stroke-linecap="round"/><g stroke-width=".5" opacity=".7"><path d="M210 66 v8 M210 162 v8 M158 118 h8 M254 118 h8"/></g><path d="M186 50 L192 30 h36 l6 20 M186 186 L192 206 h36 l6 -20" stroke-width="1.1"/><circle cx="210" cy="118" r="2.6" fill="#BE3319" stroke="none"/></g>""",
 gavel="""<g stroke="#16130E" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M172 92 l52 52 M198 64 l64 64 M186 76 l-22 -22 M240 130 l22 22" stroke-width="1.6"/><path d="M130 196 h108 M152 196 l44 -58" stroke-width="1.4"/><g stroke-width=".4" opacity=".6"><path d="M196 70 l54 54 M190 82 l50 50"/></g><circle cx="198" cy="118" r="3" fill="#BE3319" stroke="none"/></g>""",
 store="""<g stroke="#16130E" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M138 108 L152 62 h116 l14 46" stroke-width="1.6"/><path d="M138 108 a15 15 0 0 0 30.6 0 a15 15 0 0 0 30.6 0 a15 15 0 0 0 30.6 0 a15 15 0 0 0 30.6 0 a15 15 0 0 0 30.6 0" stroke-width="1.3"/><path d="M152 126 v66 h116 v-66 M186 192 v-40 h30 v40" stroke-width="1.4"/><g stroke-width=".4" opacity=".6"><path d="M160 70 h100 M156 82 h108 M152 94 h116"/></g><circle cx="238" cy="166" r="3" fill="#BE3319" stroke="none"/></g>""",
)

def plate(motif, label, code):
    waves_top = "".join(f'<path d="M0 {y} Q105 {y-8} 210 {y} T420 {y}"/>' for y in range(20, 120, 16))
    waves_bot = "".join(f'<path d="M0 {y} Q105 {y+8} 210 {y} T420 {y}"/>' for y in range(190, 240, 16))
    return f"""<svg class="plate" viewBox="0 0 420 240" role="img" aria-label="{label}">
<rect width="420" height="240" fill="#F8F4EB"/>
<g stroke="#16130E" stroke-width=".45" fill="none" opacity=".3">{waves_top}</g>
<g stroke="#16130E" stroke-width=".45" fill="none" opacity=".2">{waves_bot}</g>
{MOTIFS[motif]}
<text x="14" y="228" font-family="'IBM Plex Mono',monospace" font-size="8" letter-spacing="2" fill="#7A7263">{label.upper()}</text>
<text x="406" y="228" text-anchor="end" font-family="'IBM Plex Mono',monospace" font-size="8" letter-spacing="2" fill="#7A7263">{code}</text>
</svg>"""

BASE_URL = "https://caratcapital.org"  # swap when the real domain is connected

def head(title, desc, path="", extra=""):
    canonical = f"{BASE_URL}/{path}" if path else BASE_URL
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="Carat Capital">
<meta property="og:title" content="{H.escape(title)}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE_URL}/assets/og-card.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="Carat Capital — all desks" href="{BASE_URL}/feed.xml">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
{extra}
</head>
<body>
<div class="grain" aria-hidden="true"></div>
{DEFS}"""

def folio(right):
    edition = WIRE.get("edition", "Vol. I — No. 001 · Third Edition")
    return f"""<div class="wrap"><div class="folio">
  <div class="ed">{edition}</div>
  <div class="clocks">
    <span class="clock">NYC <b data-tz="America/New_York">--:--</b></span>
    <span class="clock">ANR <b data-tz="Europe/Brussels">--:--</b></span>
    <span class="clock">BOM <b data-tz="Asia/Kolkata">--:--</b></span>
    <span class="clock">HKG <b data-tz="Asia/Hong_Kong">--:--</b></span>
    <span class="clock">GVA <b data-tz="Europe/Zurich">--:--</b></span>
  </div>
  <div>{right}</div>
</div></div>"""

def navbar(active=""):
    here = ' class="here"'
    links = "".join(
        f'<a href="{d["slug"]}.html"{here if active==d["slug"] else ""}><i>D—{d["no"]}</i>{d["nav"]}</a>'
        for d in DESKS)
    return f"""<div class="navbar" id="navbar">
  <div class="wrap"><div class="nav-inner">
    <button class="menu-btn" onclick="ccMenu(true)" aria-label="Open menu"><span class="bars"><i></i><i></i><i></i></span>Menu</button>
    <a class="nav-brand" href="index.html"><img class="nav-mark" src="assets/logo-mark.svg" alt="Carat Capital medal">Carat<span class="caret">^</span>Capital</a>
    <div class="nav-links">{links}</div>
    <a class="nav-sub" href="index.html#rates"><span>Subscribe — $12/mo</span></a>
  </div></div>
</div>"""

def omenu():
    rows = "".join(f"""<a class="o-desk" href="{d['slug']}.html">
      <span class="n">D—{d['no']}</span><span class="t">{d['title']}</span><span class="d">{d['tag']}</span></a>""" for d in DESKS)
    return f"""<div class="omenu" id="omenu">
  <div class="wrap">
    <div class="o-head">
      <div class="o-brand">Carat<span class="caret">^</span>Capital</div>
      <button class="o-close" onclick="ccMenu(false)">Close ×</button>
    </div>
    <div class="o-grid">
      <div>
        <div class="o-label">The Six Desks</div>
        {rows}
      </div>
      <div class="o-side">
        <div class="o-label">The Paper</div>
        <a href="index.html">Front Page</a>
        <a href="field-guide.html">The Field Guide — Learn the Trade</a>
        <a href="the-record.html">The Record — Eight Weeks of the Trade</a>
        <a href="almanac.html">The Almanac — The Quarter in Numbers</a>
        <a href="index.html#tape-a">The Price Tape</a>
        <a href="index.html#voices">Voices — Interviews</a>
        <a href="index.html#coupon">The Morning Brief — Free</a>
        <a href="index.html#rates">Rate Card — Subscribe</a>
        <a href="about.html">About the Paper</a>
        <a href="about.html#standards">Editorial Standards</a>
        <a href="about.html#contact">Write to the Desk</a>
      </div>
    </div>
    <div class="o-foot">Carat Capital · The trade paper of the jewelry world · Read in 120+ countries</div>
  </div>
</div>"""

def colophon():
    desk_links = "".join(f'<a class="fl" href="{d["slug"]}.html">{d["title"]}</a>' for d in DESKS)
    return f"""<footer class="colophon">
  <div class="wrap">
    <div class="top">
      <div>
        <div class="cbrand">Carat<span class="caret">^</span>Capital</div>
        <div class="cbrand-sub">The Trade Paper of the Jewelry World</div>
        <div class="hallrow" style="color:var(--gilt)">
          <svg width="32" height="20" viewBox="0 0 32 20"><use href="#hm-maker"/></svg>
          <svg width="26" height="20" viewBox="0 0 26 20"><use href="#hm-fine"/></svg>
          <svg width="26" height="20" viewBox="0 0 26 20"><use href="#hm-assay"/></svg>
          <svg width="20" height="20" viewBox="0 0 20 20"><use href="#hm-date"/></svg>
        </div>
      </div>
      <div><h4>Desks</h4>{desk_links}</div>
      <div><h4>Masthead</h4>
        <a class="fl" href="about.html">About the paper</a><a class="fl" href="about.html#standards">Editorial standards</a>
        <a class="fl" href="field-guide.html">The Field Guide</a><a class="fl" href="the-record.html">The Record</a><a class="fl" href="almanac.html">The Almanac</a><a class="fl" href="about.html#contact">Write to the desk</a>
      </div>
      <div><h4>Subscribe</h4>
        <a class="fl" href="index.html#coupon">Morning Brief — free</a>
        <a class="fl" href="index.html#rates">Desk — $12/mo</a>
        <a class="fl" href="index.html#rates">House — $49/mo</a>
        <a class="fl" href="#">Gift a subscription</a>
      </div>
    </div>
    <div class="base">
      <div>© MMXXVI Carat Capital · Printed daily on the internet</div>
      <div>ISSN pending · caratcapital.com</div>
    </div>
  </div>
</footer>"""

SCRIPT = """<script>
function tick(){document.querySelectorAll('[data-tz]').forEach(el=>{el.textContent=new Intl.DateTimeFormat('en-GB',{hour:'2-digit',minute:'2-digit',timeZone:el.dataset.tz}).format(new Date())})}
tick();setInterval(tick,30000);
const nb=document.getElementById('navbar');
addEventListener('scroll',()=>nb.classList.toggle('scrolled',scrollY>60),{passive:true});
function ccMenu(open){document.getElementById('omenu').classList.toggle('open',open);document.body.classList.toggle('menu-open',open)}
document.addEventListener('keydown',e=>{if(e.key==='Escape')ccMenu(false)});
const belt=document.getElementById('belt');if(belt)belt.innerHTML+=belt.innerHTML;
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.1});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));
requestAnimationFrame(()=>document.querySelectorAll('.rv').forEach(el=>{const r=el.getBoundingClientRect();if(r.top<innerHeight&&r.bottom>0)el.classList.add('in')}));
const sio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('go');sio.unobserve(e.target)}}),{threshold:.4});
document.querySelectorAll('.spark').forEach(el=>sio.observe(el));
function ccJoin(e){e.preventDefault();window.open('https://caratcapital.beehiiv.com/subscribe?email='+encodeURIComponent(e.target.querySelector('input').value),'_blank');const f=document.getElementById('cp-fine');e.target.querySelector('input').value='';if(f){f.textContent='/// RECEIVED — your first Morning Brief prints tomorrow, 06:30 ET ///';f.style.color='var(--seal)'}return false}
</script>
</body>
</html>"""

# ---------------- FEED + LLMS ----------------
def rss_feed():
    import datetime as _dt
    items = ""
    for a in ARTICLES[:30]:
        d = _dt.datetime.strptime(a["date"], "%Y-%m-%d").strftime("%a, %d %b %Y 06:30:00 GMT")
        items += f"""<item>
<title>{H.escape(a["title"])}</title>
<link>{BASE_URL}/a-{a["slug"]}.html</link>
<guid isPermaLink="true">{BASE_URL}/a-{a["slug"]}.html</guid>
<pubDate>{d}</pubDate>
<category>{H.escape(DESK_NAMES.get(a["desk"], a["desk"]))}</category>
<description>{H.escape(a["dek"])}</description>
</item>"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>Carat Capital — The Trade Paper of the Jewelry World</title>
<link>{BASE_URL}</link>
<description>Prices, intelligence and analysis from every desk of the stone trade: diamonds, gold and metals, gemstones, watches, auctions, retail and technology.</description>
<language>en</language>
{items}
</channel></rss>"""

def llms_txt():
    desks = "\n".join(f"- [{d['title']}]({BASE_URL}/{d['slug']}.html): {d['tag']}" for d in DESKS)
    arts = "\n".join(f"- [{a['title']}]({BASE_URL}/a-{a['slug']}.html): {a['dek'][:140]}" for a in ARTICLES[:15])
    return f"""# Carat Capital

> The trade paper of the jewelry world — original, sourced daily reporting on diamonds, gold and precious metals, colored gemstones, watches, jewelry auctions, and jewelry retail and technology. Published at {BASE_URL}. All articles are original writing with named, linked sources; prices are dated and indicative.

## The paper
- [Front page]({BASE_URL}/): today's edition, the wire, and the live price tape
- [The Record]({BASE_URL}/the-record.html): a dated, sourced week-by-week chronicle of the industry
- [The Almanac]({BASE_URL}/almanac.html): the quarter's key numbers in sourced tables (metals, exports, prices, auctions, retail)
- [The Field Guide]({BASE_URL}/field-guide.html): plain-language introduction to how the jewelry trade works
- [About & editorial standards]({BASE_URL}/about.html)
- [RSS feed]({BASE_URL}/feed.xml)
- [Morning Brief newsletter](https://caratcapital.beehiiv.com): free daily email, 06:30 ET

## The six desks
{desks}

## Recent articles
{arts}
"""

# ---------------- THE RECORD + ALMANAC ----------------
DESK_CHIP = {"diamonds":"Diamonds","gold-metals":"Gold & Metals","gemstones":"Gemstones","watches":"Watches","auctions":"Auctions","retail-tech":"Retail & Tech"}

def record_entry(e, week=""):
    chip = DESK_CHIP.get(e.get("d",""), "The Paper")
    wk = f'<span style="color:var(--ink-3)">{week}</span>' if week else ""
    return f"""<div class="rec-e rv" style="padding:22px 0;border-bottom:1px solid rgba(22,19,14,.14)">
      <div style="font-family:var(--mono);font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:var(--seal);display:flex;gap:14px;align-items:baseline">{chip} {wk}</div>
      <h3 style="font-family:var(--disp);font-weight:700;font-size:clamp(19px,2vw,25px);letter-spacing:-.02em;margin:8px 0 7px">{e["h"]}</h3>
      <p style="max-width:820px;font-size:15.5px;line-height:1.65;color:var(--ink-2)">{e["t"]}</p>
      <div style="font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--gilt);margin-top:9px">Source — {e["s"]}</div>
    </div>"""

def record_page():
    weeks = ""
    for w in RECORD.get("weeks", []):
        entries = "".join(record_entry(e) for e in w["entries"])
        weeks += f"""<section style="padding:34px 0 8px">
          <div class="sec-mast rv"><h2>{w["label"]}</h2><div class="mono-note">the week's ledger</div></div>
          {entries}</section>"""
    return f"""{head("The Record — eight weeks of the trade — Carat Capital", "A dated, sourced chronicle of the jewelry trade, week by week.")}
{folio("The Record · A running chronicle")}
{navbar()}
{omenu()}
<section class="deskhero"><div class="wrap">
  <div class="dh-no">The Paper · Updated {RECORD.get("updated","")}</div>
  <h1 class="art-h" style="font-size:clamp(40px,6vw,86px);text-transform:uppercase">The Record<em style="font-family:var(--text);font-style:italic;font-weight:400;color:var(--seal);text-transform:none;font-size:.5em;display:block;margin-top:12px">eight weeks of the trade, kept properly</em></h1>
  <p class="dh-dek" style="max-width:760px">{RECORD.get("intro","")}</p>
</div></section>
<section class="burin"><div class="wrap">{weeks}
  <div style="padding:40px 0"><a class="big" href="almanac.html" style="font-family:var(--mono);font-size:12px;letter-spacing:.22em;text-transform:uppercase;border-bottom:2px solid var(--seal);padding-bottom:4px">The Almanac — the quarter in numbers →</a></div>
</div></section>
<section class="ctastrip"><div class="wrap"><div class="inner">
  <h2>The Record, delivered — <em>every morning at 06:30.</em></h2>
  <a class="big" href="index.html#coupon">Get the Morning Brief →</a>
</div></div></section>
{colophon()}
{SCRIPT}"""

def almanac_table(t):
    headr = "".join(f'<th style="text-align:left;font-family:var(--mono);font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--ink-3);padding:0 14px 10px 0;border-bottom:2px solid var(--ink)">{c}</th>' for c in t["cols"])
    rows = ""
    for r in t["rows"]:
        tds = f'<td style="font-family:var(--text);font-size:14.5px;padding:9px 14px 9px 0;border-bottom:1px solid rgba(22,19,14,.12)">{r[0]}</td>'
        tds += "".join(f'<td style="font-family:var(--mono);font-size:13px;padding:9px 14px 9px 0;border-bottom:1px solid rgba(22,19,14,.12);white-space:nowrap">{c}</td>' for c in r[1:])
        rows += f"<tr>{tds}</tr>"
    return f"""<div class="rv" style="break-inside:avoid;margin:0 0 44px">
      <h3 style="font-family:var(--disp);font-weight:700;font-size:21px;letter-spacing:-.02em">{t["title"]}</h3>
      <div style="font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--seal);margin:5px 0 14px">{t.get("note","")}</div>
      <table style="width:100%;border-collapse:collapse"><thead><tr>{headr}</tr></thead><tbody>{rows}</tbody></table>
      <div style="font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--gilt);margin-top:10px">Source — {t.get("src","")}</div>
    </div>"""

def almanac_page():
    tables = "".join(almanac_table(t) for t in RECORD.get("tables", []))
    return f"""{head("The Almanac — the quarter in numbers — Carat Capital", "The jewelry trade's key numbers, tabled: metals, exports, prices, salerooms, retail.")}
{folio("The Almanac · The quarter in numbers")}
{navbar()}
{omenu()}
<section class="deskhero"><div class="wrap">
  <div class="dh-no">The Paper · Updated {RECORD.get("updated","")}</div>
  <h1 class="art-h" style="font-size:clamp(40px,6vw,86px);text-transform:uppercase">The Almanac<em style="font-family:var(--text);font-style:italic;font-weight:400;color:var(--seal);text-transform:none;font-size:.5em;display:block;margin-top:12px">the quarter, in numbers a desk can use</em></h1>
  <p class="dh-dek" style="max-width:760px">Every figure below is sourced and dated. Read it with The Record for the narrative; bring it to your Monday meeting for the argument.</p>
</div></section>
<section class="burin"><div class="wrap" style="columns:2;column-gap:64px;padding-top:30px">{tables}</div></section>
<section class="ctastrip"><div class="wrap"><div class="inner">
  <h2>Numbers, every morning — <em>before the market opens.</em></h2>
  <a class="big" href="index.html#coupon">Get the Morning Brief →</a>
</div></div></section>
{colophon()}
{SCRIPT}"""

# ---------------- DESK PAGES ----------------
def desk_page(d):
    briefs = "".join(f"""<div class="brf rv">
      <div class="bn">{b[0]}</div><h3>{b[1]}</h3><p>{b[2]}</p><div class="tagm">{b[3]}</div></div>""" for b in d["briefing"])
    glos = "".join(f"""<div class="glo rv">
      <div class="term">{g[0]}<i>{g[1]}</i></div><p>{g[2]}</p></div>""" for g in d["glossary"])
    # published articles for this desk first, then house stubs to fill the list
    rows = [(f"a-{a['slug']}.html", a["title"], a["dek"], f"{a['date']} · {a['minutes']} min") for a in desk_articles(d["slug"])]
    rows += [("#", s[0], s[1], s[2]) for s in d["stories"] if s[0] not in {r[1] for r in rows}]
    stories = "".join(f"""<a class="dstory rv" href="{href}">
      <div class="n">S—{i+1:02d}</div><h3>{t}</h3><div class="d">{dk}</div><div class="m">{m}</div></a>""" for i,(href,t,dk,m) in enumerate(rows[:6]))
    stats = "".join(f"<div><b>{v}</b><span>{l}</span></div>" for v,l in d["stats"])
    recs = [(w["label"], e) for w in RECORD.get("weeks", []) for e in w.get("entries", []) if e.get("d") == d["slug"]][:5]
    recsec = ""
    if recs:
        rec_html = "".join(record_entry(e, wl) for wl, e in recs)
        recsec = f"""<section class="burin"><div class="wrap">
    <div class="sec-mast rv"><h2>This desk, on the record — <em>the last eight weeks</em></h2><div class="mono-note"><a href="the-record.html">Full chronicle →</a></div></div>
    {rec_html}
  </div></section>"""
    body = f"""{head(f"{d['title']} — Carat Capital", d['dek'][:150])}
{folio(f"Desk D—{d['no']} · {d['title']}")}
{navbar(d['slug'])}
{omenu()}
<section class="deskhero">
  <div class="wrap"><div class="dh-grid">
    <div>
      <div class="dh-no">Desk D—{d['no']} · Filed Daily</div>
      <h1>{d['title']}<em>{d['tag']}</em></h1>
      <p class="dh-dek">{d['dek']}</p>
      <div class="dh-stats">{stats}</div>
    </div>
    <figure class="dh-plate">
      {plate(d['motif'], f"Plate D-{d['no']} — the {d['title'].lower()} desk", f"CC/2026/D{d['no']}")}
      <div class="cap"><span>Engraving — CC graphics desk</span><span>D—{d['no']}</span></div>
    </figure>
  </div></div>
</section>
<section class="briefing">
  <div class="wrap">
    <div class="sec-mast rv"><h2>The briefing — <em>what's moving now</em></h2><div class="mono-note">Updated each edition</div></div>
    <div class="brf-grid">{briefs}</div>
  </div>
</section>
<section class="glossary burin">
  <div class="wrap">
    <div class="sec-mast rv"><h2>Understand the segment — <em>the working vocabulary</em></h2><div class="mono-note">The trade's terms, plainly told</div></div>
    <div class="glo-grid">{glos}</div>
  </div>
</section>
<section class="deskstories">
  <div class="wrap">
    <div class="sec-mast rv"><h2>Latest from this desk</h2><div class="mono-note">Filed by correspondents</div></div>
    <div>{stories}</div>
  </div>
</section>
{recsec}
<section class="ctastrip">
  <div class="wrap"><div class="inner">
    <h2>Never miss this desk — <em>it's in the Morning Brief.</em></h2>
    <a class="big" href="index.html#coupon">Get it free →</a>
  </div></div>
</section>
{colophon()}
{SCRIPT}"""
    return body

def spark(pts, color):
    n = max(len(pts) - 1, 1)
    coords = [(round(i * 120 / n), p) for i, p in enumerate(pts)]
    line = "M" + " L".join(f"{x} {y}" for x, y in coords)
    area = line + " V26 H0 Z"
    return f"""<svg class="spark" width="100%" height="26" viewBox="0 0 120 26" preserveAspectRatio="none"><path class="a" d="{area}" fill="{color}"/><path class="l" d="{line}" stroke="{color}"/></svg>"""

def tape_block():
    cells = ""
    for t in WIRE.get("tape", []):
        color = "#69D08A" if t["dir"] == "up" else "#E8705F"
        cells += f"""<div class="cell"><div class="sym"><span>{t['name']}</span><span class="code">{t['code']}</span></div><div class="px">{t['px']}</div><div class="d {t['dir']}">{t['chg']}</div>{spark(t['pts'], color)}</div>"""
    ts = WIRE.get("tape_ts", "")
    return f"""<div class="tape" id="tape-a">
  <div class="wrap">
    <div class="head"><span>Carat Capital Price Desk</span><span class="live">● Live — {ts}</span><span>USD · Indicative</span></div>
    <div class="row">{cells}</div>
  </div>
</div>"""

def wire_block():
    items = "".join(f'<span class="item"><b>{i["b"]}</b>{i["t"]}</span>' for i in WIRE.get("items", []))
    return f"""<div class="wire">
  <div class="tag"><span class="blink"></span>The Wire</div>
  <div class="belt"><div class="belt-track" id="belt">{items}</div></div>
</div>"""

DEX_STUBS = [
    ("gemstones.html", "Boucheron rewrites its own icon — and resets the bar for Place Vendôme", "High Jewelry · Paris · 5 min"),
    ("gemstones.html", "The Odyssey effect — ancient-world jewelry is about to have its moment", "Trends · London · 6 min"),
    ("retail-tech.html", "America 250: heritage houses mint an anniversary economy", "Retail · New York · 4 min"),
]

DESK_NAMES = {d["slug"]: d["title"] for d in DESKS}

# ---------------- ARTICLE PAGE ----------------
def article_page(a):
    paras = "".join(f"<p>{p}</p>" for p in a["body"])
    srcs = "".join(f'<a href="{s["url"]}" target="_blank" rel="noopener">{s["title"]} ↗</a>' for s in a.get("sources", []))
    desk_name = DESK_NAMES.get(a["desk"], a["desk"])
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "NewsArticle",
        "headline": a["title"], "description": a["dek"], "datePublished": a["date"],
        "author": {"@type": "Organization", "name": f"Carat Capital — {a['byline']}"},
        "publisher": {"@type": "Organization", "name": "Carat Capital", "url": BASE_URL},
        "articleSection": desk_name, "mainEntityOfPage": f"{BASE_URL}/a-{a['slug']}.html"
    })
    extra = f'<scr' + f'ipt type="application/ld+json">{jsonld}</scr' + f'ipt>'
    return f"""{head(f"{a['title']} — Carat Capital", a['dek'][:150], f"a-{a['slug']}.html", extra)}
{folio(f"{a['date']} · {desk_name}")}
{navbar(a['desk'])}
{omenu()}
<article class="artpage">
  <div class="wrap">
    <div class="art-head rv in">
      <div class="kick">{a['kicker']}</div>
      <h1 class="art-h">{a['title']}</h1>
      <p class="lead-dek">{a['dek']}</p>
      <div class="byline">By <b>{a['byline']}</b> · {a['date']} · {a['minutes']} min read</div>
    </div>
    <div class="art-body rv in">{paras}</div>
    <div class="art-sources rv in">
      <div class="kick">Sources &amp; further reading</div>
      {srcs}
    </div>
  </div>
</article>
<section class="ctastrip">
  <div class="wrap"><div class="inner">
    <h2>More from the {desk_name} desk — <em>every morning, free.</em></h2>
    <a class="big" href="index.html#coupon">Get the Morning Brief →</a>
  </div></div>
</section>
{colophon()}
{SCRIPT}"""

# ---------------- INDEX ----------------
def index_page():
    LEAD = lead_article()
    lead_href = f"a-{LEAD['slug']}.html" if LEAD else "#"
    dex_rows = [(f"a-{a['slug']}.html", a["title"], f"{DESK_NAMES.get(a['desk'],'')} · {a['minutes']} min") for a in ARTICLES if not a.get("lead")]
    dex_rows += [s for s in DEX_STUBS if s[1] not in {r[1] for r in dex_rows}]
    dex = "".join(f"""<a class="story" href="{href}"><div class="n">{i+2:02d}</div><div><h3>{t}</h3><div class="m">{m}</div></div></a>""" for i,(href,t,m) in enumerate(dex_rows[:5]))
    ledger = "".join(f"""<a class="rowd" href="{d['slug']}.html">
      <div class="no">D—{d['no']}</div><h3>{d['title']}</h3>
      <div class="desc">{d['glossary'][0][2][:0]}{d['dek'].split('. ')[1][:140] if '. ' in d['dek'] else d['dek'][:140]}…</div>
      <div class="freq">{d['tag']}</div><div class="go">-&gt;</div></a>""" for d in DESKS)
    return f"""{head("CARAT CAPITAL — The Trade Paper of the Jewelry World",
      "Carat Capital is the trade paper of the global jewelry industry. Prices, intelligence and reporting from every desk of the stone trade.")}
<style>
.mast2{{background:linear-gradient(180deg,var(--paper-hi,#F8F4EB),var(--bone,#F2EDE3));border-bottom:1px solid rgba(22,19,14,.28)}}
.mast2 .m2-grid{{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:28px;padding:26px 0 22px}}
.mast2 .m2-side{{font-family:var(--mono);font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink-2);display:flex;flex-direction:column;gap:7px}}
.mast2 .m2-side b{{color:var(--seal);font-weight:600}}
.mast2 .m2-right{{text-align:right;align-items:flex-end}}
.mast2 .m2-center{{display:flex;align-items:center;gap:22px}}
.mast2 .m2-rule{{display:block;width:min(11vw,150px);height:1px;background:linear-gradient(90deg,transparent,rgba(22,19,14,.5));position:relative}}
.mast2 .m2-rule.r{{background:linear-gradient(90deg,rgba(22,19,14,.5),transparent)}}
.mast2 .m2-rule::after{{content:"";position:absolute;top:-2.5px;width:6px;height:6px;transform:rotate(45deg);background:var(--seal)}}
.mast2 .m2-rule.l::after{{right:0}}
.mast2 .m2-rule.r::after{{left:0}}
.mast2 .m2-medal{{width:104px;height:104px;display:block;transition:transform 1.2s cubic-bezier(.19,1,.22,1)}}
.mast2 a:hover .m2-medal{{transform:rotate(8deg)}}
.mast2 .m2-halls{{display:flex;gap:9px;align-items:center;color:var(--gilt)}}
.mast2 .m2-clock b{{font-weight:600;color:var(--ink)}}
@media(max-width:860px){{.mast2 .m2-side{{display:none}}.mast2 .m2-grid{{grid-template-columns:1fr;justify-items:center;padding:20px 0 16px}}.mast2 .m2-rule{{width:18vw}}}}
</style>
<div class="mast2"><div class="wrap"><div class="m2-grid">
  <div class="m2-side">
    <span>{WIRE.get("edition","")}</span>
    <span>{WIRE.get("date_line","")}</span>
    <span><b>Est. MMXXVI</b> · Read in 120+ countries</span>
  </div>
  <div class="m2-center">
    <span class="m2-rule l"></span>
    <div class="m2-halls">
      <svg width="30" height="19" viewBox="0 0 32 20"><use href="#hm-maker"/></svg>
      <svg width="25" height="19" viewBox="0 0 26 20"><use href="#hm-fine"/></svg>
    </div>
    <a href="index.html" aria-label="Carat Capital"><img class="m2-medal" src="assets/logo-mark.svg" alt="Carat Capital — the minted mark"></a>
    <div class="m2-halls">
      <svg width="25" height="19" viewBox="0 0 26 20"><use href="#hm-assay"/></svg>
      <svg width="19" height="19" viewBox="0 0 20 20"><use href="#hm-date"/></svg>
    </div>
    <span class="m2-rule r"></span>
  </div>
  <div class="m2-side m2-right">
    <span class="m2-clock">NYC <b data-tz="America/New_York">--:--</b> · ANR <b data-tz="Europe/Brussels">--:--</b></span>
    <span class="m2-clock">BOM <b data-tz="Asia/Kolkata">--:--</b> · HKG <b data-tz="Asia/Hong_Kong">--:--</b></span>
    <span>The trade paper of the jewelry world</span>
  </div>
</div></div></div>
{navbar()}
{omenu()}
{wire_block()}
{tape_block()}
<section class="front" id="front">
  <div class="wrap"><div class="front-grid">
    <article class="rv">
      <div class="kick">{LEAD['kicker'] if LEAD else 'Lead Story'}</div>
      <h2 class="lead-h"><a href="{lead_href}">{LEAD['title'] if LEAD else ''}</a></h2>
      <p class="lead-dek">{LEAD['dek'] if LEAD else ''}</p>
      <div class="byline">By <b>{LEAD['byline'] if LEAD else ''}</b> · Fig. plate I · {LEAD['minutes'] if LEAD else 0} min read</div>
      <figure class="lead-fig">
        <svg class="plate" viewBox="0 0 900 430" role="img" aria-label="Engraved plate of a brilliant-cut stone">
          <rect width="900" height="430" fill="#F8F4EB"/>
          <g stroke="#16130E" stroke-width=".5" fill="none" opacity=".33">
            <path d="M0 26 Q225 16 450 26 T900 26"/><path d="M0 44 Q225 34 450 44 T900 44"/><path d="M0 62 Q225 52 450 62 T900 62"/><path d="M0 80 Q225 70 450 80 T900 80"/><path d="M0 98 Q225 88 450 98 T900 98"/><path d="M0 116 Q225 106 450 116 T900 116"/><path d="M0 134 Q225 124 450 134 T900 134"/><path d="M0 152 Q225 142 450 152 T900 152"/>
          </g>
          <g stroke="#16130E" stroke-width=".5" fill="none" opacity=".22">
            <path d="M0 300 Q225 310 450 300 T900 300"/><path d="M0 318 Q225 328 450 318 T900 318"/><path d="M0 336 Q225 346 450 336 T900 336"/><path d="M0 354 Q225 364 450 354 T900 354"/><path d="M0 372 Q225 382 450 372 T900 372"/><path d="M0 390 Q225 400 450 390 T900 390"/><path d="M0 408 Q225 418 450 408 T900 408"/>
          </g>
          <line x1="60" y1="282" x2="840" y2="282" stroke="#16130E" stroke-width="1"/>
          <g stroke="#16130E" fill="none">
            <path d="M450 60 L590 148 L450 282 L310 148 Z" stroke-width="1.8" stroke-linejoin="round" fill="#F8F4EB"/>
            <path d="M310 148 H590" stroke-width="1.1"/>
            <path d="M450 60 L385 148 L450 282 L515 148 Z" stroke-width=".9"/>
            <path d="M450 60 L340 122 M450 60 L560 122 M310 148 L385 148 M590 148 L515 148" stroke-width=".7"/>
            <g stroke-width=".45" opacity=".65"><path d="M334 132 L368 92 M346 140 L392 86 M420 70 L364 140"/><path d="M566 132 L532 92 M554 140 L508 86 M480 70 L536 140"/></g>
            <g stroke-width=".45" opacity=".5"><path d="M330 162 L438 262 M348 178 L430 254 M366 194 L422 246"/><path d="M570 162 L462 262 M552 178 L470 254 M534 194 L478 246"/></g>
            <path d="M450 60 L450 10" stroke-width=".8" stroke-dasharray="1 4"/>
            <circle cx="450" cy="148" r="3.4" fill="#BE3319" stroke="none"/>
          </g>
          <g font-family="'IBM Plex Mono',monospace" fill="#16130E">
            <text x="618" y="152" font-size="11" letter-spacing="1.5">GIRDLE — $4,135/OZ</text>
            <line x1="594" y1="148" x2="612" y2="148" stroke="#BE3319" stroke-width="1"/>
            <text x="240" y="70" font-size="11" letter-spacing="1.5" text-anchor="end">CROWN</text>
            <line x1="248" y1="66" x2="330" y2="90" stroke="#16130E" stroke-width=".6"/>
            <text x="240" y="240" font-size="11" letter-spacing="1.5" text-anchor="end">PAVILION</text>
            <line x1="248" y1="236" x2="360" y2="210" stroke="#16130E" stroke-width=".6"/>
            <text x="60" y="316" font-size="10" letter-spacing="2" fill="#7A7263">FIG. I — THE STONE, RE-CUT BY THE METAL BENEATH IT</text>
          </g>
        </svg>
        <figcaption class="cap"><span>Plate I — Engraving by the Carat Capital graphics desk</span><span>CC/2026/001</span></figcaption>
      </figure>
    </article>
    <div class="dex rv rv-d1">
      <div class="kick">The Index</div>
      {dex}
    </div>
    <aside class="dispatch rv rv-d2">
      <svg class="stamp" width="30" height="19" viewBox="0 0 32 20" style="color:var(--gilt)"><use href="#hm-maker"/></svg>
      <div class="kick">The Dispatch · Opinion</div>
      <h3>A price list you can believe is worth more than a high one.</h3>
      <p>De Beers spent two years defending a book that traded thirty percent above reality, and the market simply routed around it. This week it moves to close the gap. The lesson prices in everywhere: in rough, in retail tickets, in lab-grown tags — the trade pays a premium for honest numbers and discounts everything else.</p>
      <div class="sig">— The Editor's Desk, No. 002</div>
    </aside>
  </div></div>
</section>
<section class="desks" id="desks">
  <div class="wrap">
    <div class="sec-mast rv"><h2>Six desks. <em>The whole trade.</em></h2><div class="mono-note">Open a desk to learn its segment</div></div>
    <div class="ledger rv">{ledger}</div>
  </div>
</section>
<section class="burin"><div class="wrap" style="padding:64px 0 58px">
  <div class="sec-mast rv"><h2>The paper keeps a ledger. <em>Two of them.</em></h2><div class="mono-note">Updated weekly</div></div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:26px;margin-top:26px">
    <a class="rv" href="the-record.html" style="border:1.5px solid var(--ink);padding:30px 28px;display:block">
      <div style="font-family:var(--mono);font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:var(--seal)">The Record</div>
      <div style="font-family:var(--disp);font-weight:700;font-size:clamp(22px,2.4vw,32px);letter-spacing:-.02em;margin:10px 0 8px">Eight weeks of the trade, kept properly</div>
      <p style="color:var(--ink-2);font-size:14.5px;line-height:1.6">Every story that moved the industry since mid-May — dated, sourced, one page. The fastest way to catch up on the quarter.</p>
      <div style="font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;margin-top:14px;border-bottom:2px solid var(--seal);display:inline-block;padding-bottom:3px">Read the chronicle →</div>
    </a>
    <a class="rv rv-d1" href="almanac.html" style="border:1.5px solid var(--ink);padding:30px 28px;display:block">
      <div style="font-family:var(--mono);font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:var(--seal)">The Almanac</div>
      <div style="font-family:var(--disp);font-weight:700;font-size:clamp(22px,2.4vw,32px);letter-spacing:-.02em;margin:10px 0 8px">The quarter in numbers a desk can use</div>
      <p style="color:var(--ink-2);font-size:14.5px;line-height:1.6">Metals prints, Swiss exports by market, lab-grown price curves, the saleroom league table, the retail scorecard — tabled and sourced.</p>
      <div style="font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;margin-top:14px;border-bottom:2px solid var(--seal);display:inline-block;padding-bottom:3px">Open the tables →</div>
    </a>
  </div>
</div></section>
<section class="plateband">
  <div class="rosette">
    <svg width="640" height="640" viewBox="0 0 640 640" fill="none" stroke="#96762E" stroke-width=".6">
      <g transform="translate(320 320)">
        {"".join(f'<ellipse rx="300" ry="104" transform="rotate({a})"/>' for a in range(0,180,15))}
        {"".join(f'<ellipse rx="190" ry="60" transform="rotate({a})"/>' for a in range(0,180,22))}
        <circle r="300" opacity=".5"/><circle r="104" opacity=".5"/>
      </g>
    </svg>
  </div>
  <div class="wrap">
    <blockquote class="rv">A diamond crosses <b>six borders</b> before it reaches a ring finger. We file from every one of them.</blockquote>
    <div class="attr rv rv-d1">Carat Capital · Correspondents in 120 countries</div>
  </div>
</section>
<section class="voices" id="voices">
  <div class="wrap">
    <div class="sec-mast rv"><h2>Voices <em>of the trade</em></h2><div class="mono-note">Interview series · Wednesdays</div></div>
    <div class="vcols">
      <div class="vcol rv"><div class="series">The Maison Interview</div>
        <blockquote>The houses that survive the next decade will be the ones that treat traceability as romance, not compliance.</blockquote>
        <div class="who"><svg width="26" height="16" viewBox="0 0 32 20" style="color:var(--seal)"><use href="#hm-maker"/></svg>Creative directors on craft &amp; provenance</div></div>
      <div class="vcol rv rv-d1"><div class="series">The Dealmaker Series</div>
        <blockquote>Lab-grown didn't kill the diamond dream. It made the natural stone tell a better story — or lose.</blockquote>
        <div class="who"><svg width="22" height="17" viewBox="0 0 26 20" style="color:var(--seal)"><use href="#hm-assay"/></svg>Traders, sightholders &amp; financiers</div></div>
      <div class="vcol rv rv-d2"><div class="series">The New Retail Diaries</div>
        <blockquote>My customers are 24 and buying emeralds on their phones at midnight. Meet them there, or meet nobody.</blockquote>
        <div class="who"><svg width="22" height="17" viewBox="0 0 26 20" style="color:var(--seal)"><use href="#hm-fine"/></svg>Founders building tomorrow's counters</div></div>
    </div>
  </div>
</section>
<section class="couponband burin" id="coupon">
  <div class="wrap"><div class="coupon rv">
    <div class="scissors"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="6" cy="6" r="2.6"/><circle cx="6" cy="18" r="2.6"/><path d="M8.2 7.6 L20 18 M8.2 16.4 L20 6" stroke-linecap="round"/></svg></div>
    <div class="nocharge">No Charge · Ever</div>
    <h2>The Morning Brief — read it <em>before the market opens.</em></h2>
    <p>One five-minute dispatch every trading day: overnight prices, the three stories that matter, and one line sharp enough to repeat in your first meeting. Filed 06:30 ET / before Antwerp lunch.</p>
    <form class="cp-form" onsubmit="return ccJoin(event)">
      <input type="email" required placeholder="you@yourhouse.com" aria-label="Email">
      <button type="submit"><span>File Me In</span></button>
    </form>
    <div class="cp-fine" id="cp-fine">/// Read in 120+ countries · Unsubscribe anytime ///</div>
  </div></div>
</section>
<section class="rates" id="rates">
  <div class="wrap">
    <div class="sec-mast rv"><h2>The <em>rate card</em></h2><div class="mono-note">Tariff of subscription · 2026</div></div>
    <div class="ratetable rv">
      <div class="rt-head">
        <div>Entitlement</div>
        <div class="tier"><span>Reader</span><span class="p">$0</span></div>
        <div class="tier mark"><span style="color:var(--gilt)">Desk — most taken</span><span class="p"><sup>$</sup>12<em>/mo</em></span></div>
        <div class="tier"><span>House · ×5 seats</span><span class="p"><sup>$</sup>49<span style="font-size:13px">/mo</span></span></div>
      </div>
      <div class="rt-row"><div>The Morning Brief, daily</div><div class="y">✓</div><div class="y mk">✓</div><div class="y">✓</div></div>
      <div class="rt-row"><div>Stories per month</div><div>3</div><div class="mk y">∞</div><div class="y">∞</div></div>
      <div class="rt-row"><div>Price desk — gold, polished, lab-grown</div><div>Weekly</div><div class="mk y">Daily</div><div class="y">Daily + history</div></div>
      <div class="rt-row"><div>Auction previews &amp; results wire</div><div class="n">—</div><div class="mk y">✓</div><div class="y">✓</div></div>
      <div class="rt-row"><div>Voices interview archive</div><div class="n">—</div><div class="mk y">✓</div><div class="y">✓</div></div>
      <div class="rt-row"><div>Quarterly State of the Trade report</div><div class="n">—</div><div class="n mk">—</div><div class="y">✓</div></div>
      <div class="rt-row"><div>Data downloads &amp; survey early access</div><div class="n">—</div><div class="n mk">—</div><div class="y">✓</div></div>
      <div class="rt-cta">
        <div style="text-align:left;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);display:flex;align-items:center">Billed annually · cancel anytime</div>
        <div><a href="#coupon">Start Free</a></div>
        <div class="mk"><a class="sealed" href="#">Take a Desk</a></div>
        <div><a href="#">Equip a House</a></div>
      </div>
    </div>
  </div>
</section>
{colophon()}
{SCRIPT}"""

# ---------------- FIELD GUIDE (education hub) ----------------
def field_guide():
    sections = ""
    for d in DESKS:
        cards = "".join(f"""<div class="glo rv"><div class="term">{g[0]}<i>{g[1]}</i></div><p>{g[2]}</p></div>""" for g in d["glossary"])
        sections += f"""<section class="glossary" style="background:transparent;border-bottom:1px solid var(--rule-soft)">
  <div class="wrap">
    <div class="sec-mast rv"><h2><a href="{d['slug']}.html" style="border-bottom:2px solid var(--seal)">{d['title']}</a> — <em>{d['tag']}</em></h2><div class="mono-note">Desk D—{d['no']}</div></div>
    <div class="glo-grid">{cards}</div>
  </div>
</section>"""
    borders = "".join(f"""<div class="brf rv"><div class="bn">{n}</div><h3>{t}</h3><p>{p}</p></div>""" for n, t, p in [
        ("B-01","The mine","A stone starts in Botswana, Russia, Canada or Australia — or increasingly, in a reactor in Surat or Singapore. Producer sales and tenders set the first price it will ever carry."),
        ("B-02","The trading floor","Rough crosses into Antwerp, Dubai or Ramat Gan, where bourses, sightholders and dealers move it toward the cutters — and where most of the trade's credit lives."),
        ("B-03","The cutting room","Surat polishes roughly nine of every ten stones on earth; Bangkok and Jaipur rule colored gems. Yield decisions made here — what shape, what grade to chase — decide the stone's fate."),
        ("B-04","The laboratory","GIA, SSEF, Gübelin and their peers grade, certify and determine origin. A sentence on a report can multiply a price tenfold; the paper is part of the product."),
        ("B-05","The maison","Design, brand and setting happen in Paris, Milan, New York and ten thousand independent workshops. This is where melt value becomes meaning — and margin."),
        ("B-06","The counter","A boutique, a department store, a livestream, a DM thread. The final border, where the trade meets a person with an occasion — and the whole pipeline gets paid."),
    ])
    return f"""{head("The Field Guide — Learn the Jewelry Trade — Carat Capital",
      "The working vocabulary of the global jewelry trade, desk by desk: diamonds, gold, gemstones, watches, auctions and retail — explained plainly by Carat Capital.", "field-guide.html")}
{folio("The Field Guide · Free Forever")}
{navbar()}
{omenu()}
<section class="deskhero">
  <div class="wrap">
    <div class="dh-no">The Field Guide · Education Desk</div>
    <h1 class="art-h" style="font-size:clamp(40px,6.4vw,92px);text-transform:uppercase">Learn the trade<em style="font-family:var(--text);font-style:italic;font-weight:400;color:var(--seal);text-transform:none;font-size:.55em;display:block;margin-top:14px">the working vocabulary, desk by desk</em></h1>
    <p class="dh-dek" style="max-width:66ch">Every industry has a language, and jewelry's is older than most. This guide collects the terms the trade actually uses — the sight and the memo, hallmarks and making charges, pigeon's blood and provenance — written plainly enough for a newcomer and precisely enough for a dealer. It is free, it always will be, and it grows with every edition we publish.</p>
  </div>
</section>
<section class="briefing">
  <div class="wrap">
    <div class="sec-mast rv"><h2>First, the map — <em>six borders, one stone</em></h2><div class="mono-note">The pipeline, end to end</div></div>
    <div class="brf-grid" style="grid-template-columns:repeat(3,1fr)">{borders}</div>
  </div>
</section>
{sections}
<section class="ctastrip">
  <div class="wrap"><div class="inner">
    <h2>Fluent yet? — <em>the Morning Brief keeps you that way.</em></h2>
    <a class="big" href="index.html#coupon">Get it free →</a>
  </div></div>
</section>
{colophon()}
{SCRIPT}"""

# ---------------- ABOUT ----------------
def about_page():
    return f"""{head("About Carat Capital — The Trade Paper of the Jewelry World",
      "What Carat Capital is, how we report, and how to reach the desk.", "about.html")}
{folio("About the Paper")}
{navbar()}
{omenu()}
<article class="artpage">
  <div class="wrap">
    <div class="art-head rv in">
      <div class="kick">The Masthead</div>
      <h1 class="art-h">A trade paper, in the oldest sense — built for the fastest market</h1>
      <p class="lead-dek">Carat Capital is the daily intelligence desk of the global jewelry industry: prices, reporting and analysis for the people who make, move and sell the world's most beautiful objects.</p>
    </div>
    <div class="art-body rv in">
      <p>The jewelry trade runs from the mines of Botswana to the ateliers of Place Vendôme, through the bourses of Antwerp, the polishing wheels of Surat, the auction rooms of Geneva and the livestream studios of Shenzhen. It employs millions, turns over hundreds of billions of dollars, and until now has had no single, modern, daily paper of record. That is the job we hired ourselves to do.</p>
      <p>We publish six desks — Diamonds, Gold &amp; Metals, Colored Gemstones, Watches, Auctions &amp; Estates, and Retail &amp; Technology — plus a daily price tape and the Morning Brief, a five-minute email filed before the market opens. Reading is free at the counter; depth is for members.</p>
      <h2 id="standards" style="font-family:var(--disp);font-weight:700;font-size:28px;letter-spacing:-.02em;margin:34px 0 16px;scroll-margin-top:90px">Editorial standards</h2>
      <p>Everything we publish is original writing. We research widely and credit sources by name and link at the foot of every article. We never reproduce another publication's text or images. Prices are verified the morning of publication or marked unchanged. We do not accept payment for coverage; sponsored content, when it exists, will say so in the headline. When we are wrong, we correct in place and note it. Every claim is priced, sourced, or cut.</p>
      <h2 id="contact" style="font-family:var(--disp);font-weight:700;font-size:28px;letter-spacing:-.02em;margin:34px 0 16px;scroll-margin-top:90px">Write to the desk</h2>
      <p>Tips, corrections, interview subjects and partnership inquiries: <b>connect@roomysjewelery.store</b>. We read everything; the good tips make the wire.</p>
    </div>
  </div>
</article>
<section class="ctastrip">
  <div class="wrap"><div class="inner">
    <h2>Judge us by the work — <em>it's free every morning.</em></h2>
    <a class="big" href="index.html#coupon">Get the Morning Brief →</a>
  </div></div>
</section>
{colophon()}
{SCRIPT}"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><circle cx="16" cy="16" r="15.2" fill="#F2EDE3" stroke="#16130E" stroke-width="1.3"/><circle cx="16" cy="16" r="12.9" fill="none" stroke="#16130E" stroke-width=".7"/><path d="M9.4 14.6 L16 8.6 L22.6 14.6" fill="none" stroke="#BE3319" stroke-width="3.4"/><path d="M10.2 19.1 L16 13.9 L21.8 19.1 M10.2 24.2 L16 19 L21.8 24.2" fill="none" stroke="#16130E" stroke-width="1.4"/></svg>"""

# ---- the minted mark, nav-scale (engine-turned medal, reduced density) ----
import math as _m
def _ring(base, amp, k, ph, steps=200):
    pts = []
    for s_ in range(steps + 1):
        th = 2 * _m.pi * s_ / steps
        r = base + amp * _m.sin(k * th + ph)
        pts.append(f"{500 + r*_m.cos(th):.0f} {500 + r*_m.sin(th):.0f}")
    return "M " + " L ".join(pts) + " Z"

def _chev(apex, half=188, drop=148):
    return f"M {500-half} {apex+drop} L 500 {apex} L {500+half} {apex+drop}"

def logo_mark_svg():
    rings = []
    n = 26
    for i in range(n):
        base = 118 + (382 - 118) * i / (n - 1)
        amp = 10.0 * min(1.0, (base - 66) / 170.0)
        ph = 2 * _m.pi * 2 * i / n
        rings.append(f'<path d="{_ring(base, amp, 12, ph)}" stroke="#16130E" stroke-width="1.9" fill="none" opacity=".85"/>')
    ticks = []
    a = 0.0
    while a < 360:
        th = _m.radians(a)
        ticks.append(f"M {500+458*_m.cos(th):.0f} {500+458*_m.sin(th):.0f} L {500+479*_m.cos(th):.0f} {500+479*_m.sin(th):.0f}")
        a += 3.6
    CH, CW = [330, 466, 602], 56
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">
<defs><mask id="cm"><rect width="1000" height="1000" fill="white"/>
<g stroke="black" stroke-width="{CW+30}" fill="none"><path d="{_chev(CH[0])}"/><path d="{_chev(CH[1])}"/><path d="{_chev(CH[2])}"/></g></mask></defs>
<circle cx="500" cy="500" r="480" stroke="#16130E" stroke-width="7" fill="none"/>
<path d="{" ".join(ticks)}" stroke="#16130E" stroke-width="3" fill="none" opacity=".9"/>
<circle cx="500" cy="500" r="446" stroke="#16130E" stroke-width="4" fill="none"/>
<g transform="translate(500,500) scale(1.06) translate(-500,-500)">
<g mask="url(#cm)">{"".join(rings)}</g>
<path d="{_chev(CH[0])}" stroke="#BE3319" stroke-width="{CW}" fill="none"/>
<g stroke="#16130E" stroke-width="5" fill="none" opacity=".9">
<path d="{_chev(CH[1]-CW/2)}"/><path d="{_chev(CH[1]+CW/2)}"/>
<path d="{_chev(CH[2]-CW/2)}"/><path d="{_chev(CH[2]+CW/2)}"/></g></g></svg>'''

def sitemap(pages):
    urls = "".join(f"<url><loc>{BASE_URL}/{p}</loc></url>" for p in pages)
    return f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'

out = ROOT
(out/"index.html").write_text(index_page())
for d in DESKS:
    (out/f"{d['slug']}.html").write_text(desk_page(d))
for a in ARTICLES:
    (out/f"a-{a['slug']}.html").write_text(article_page(a))
(out/"field-guide.html").write_text(field_guide())
(out/"the-record.html").write_text(record_page())
(out/"almanac.html").write_text(almanac_page())
(out/"about.html").write_text(about_page())
(out/"assets"/"favicon.svg").write_text(FAVICON)
(out/"assets"/"logo-mark.svg").write_text(logo_mark_svg())
(out/"feed.xml").write_text(rss_feed())
(out/"llms.txt").write_text(llms_txt())
pages = ["index.html", "field-guide.html", "about.html", "the-record.html", "almanac.html"] + [f"{d['slug']}.html" for d in DESKS] + [f"a-{a['slug']}.html" for a in ARTICLES]
(out/"sitemap.xml").write_text(sitemap(pages))
(out/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
print("built:", ", ".join(pages), "+ sitemap, robots, favicon")
