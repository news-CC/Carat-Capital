#!/usr/bin/env python3
# Carat Capital — static site builder (Third Edition, content-driven)
# Content lives in content/articles.json + content/wire.json — edit those, re-run this.
import html as H
import datetime
import json, pathlib

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content"
ARTICLES = json.loads((CONTENT / "articles.json").read_text()) if (CONTENT / "articles.json").exists() else []
ARTICLES.sort(key=lambda a: a.get("date", ""), reverse=True)
WIRE = json.loads((CONTENT / "wire.json").read_text()) if (CONTENT / "wire.json").exists() else {}
RECORD = json.loads((CONTENT / "record.json").read_text()) if (CONTENT / "record.json").exists() else {}
PRICES = json.loads((CONTENT / "prices.json").read_text()) if (CONTENT / "prices.json").exists() else {}
LAB = json.loads((CONTENT / "lab-prices.json").read_text()) if (CONTENT / "lab-prices.json").exists() else {}

# The natural 1ct tape mark is the RAPI level published on the price list.
# Overridden here so the chip and the page it opens can never drift apart,
# whatever the daily wire writes.
if PRICES.get("headline"):
    for _t in WIRE.get("tape", []):
        if _t.get("code") == "NAT1":
            _t["px"] = f'{PRICES["headline"]["rapi_ct"]:,.2f}'
            _t["chg"] = "\u22126.4% YTD"
            _t["dir"] = "down"

# The lab-grown mark is the midpoint of the published CVD wholesale band for a
# one-carat D-F/VS stone. Same lock, same reason: the chip and the list it opens
# must never quote two different numbers.
if LAB.get("headline"):
    for _t in WIRE.get("tape", []):
        if _t.get("code") == "LGD1":
            _t["px"] = f'{LAB["headline"]["trade_mid"]:,.2f}'
            _t["chg"] = "\u221213% YoY"
            _t["dir"] = "down"

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
   stats=[("$5,232","1ct RBC · natural, this week"),("+4.2%","RAPI 0.30ct, June"),("6","Borders per stone, avg.")],
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
   stats=[("$3,997","Gold/oz · Jul 13 close"),("−10.9%","Silver, on the month"),("~50%","Of gold demand is jewelry")],
   motif="ingot",
   briefing=[
     ("B-01","$4,000 is the floor — tested three times, held three times","Gold stabbed below $4,000 on war nerves and snapped back within a day. Manufacturers have stopped waiting for a retreat: product architecture is being redesigned around a $4,000-plus planning price.","Bullion · New York"),
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
   stats=[("$475","Lab-grown 1ct, wholesale midpoint"),("~20%","Of sales now online"),("24","Median first-buyer age")],
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
import re as _re2
def cu(u):
    # clean an emitted URL string: drop a trailing .html (before end, # or ?)
    return _re2.sub(r'\.html(?=$|#|\?)', '', u)
def _clean_links(html):
    # rewrite in-page links to extensionless; index -> site root
    html = _re2.sub(r'href="index\.html(#[\w-]+)?"', lambda m: 'href="/' + (m.group(1) or '') + '"', html)
    html = _re2.sub(r'href="([a-z0-9][a-z0-9-]*)\.html(#[\w-]+)?"', r'href="\1\2"', html)
    return html

import hashlib as _hl
CSS_V = _hl.md5((ROOT / "assets" / "styles.css").read_bytes()).hexdigest()[:8] if (ROOT / "assets" / "styles.css").exists() else "0"

# ---------------- REDESIGN v3: photo plates, glyphs, accents ----------------
import re as _re
PH = json.loads((ROOT / "assets" / "ph" / "manifest.json").read_text()) if (ROOT / "assets" / "ph" / "manifest.json").exists() else {}

DESK_ACCENTS = {"diamonds":"#BE3319","gold-metals":"#96762E","gemstones":"#2E6E5E","watches":"#16130E","auctions":"#8A5A2E","retail-tech":"#4A5A6E"}

# A representative openly-licensed photo per desk (from assets/ph), used so photoless
# stories still get a real, tinted image instead of a bare engraving glyph.
DESK_HERO = {"diamonds":"diamonds-hero","gold-metals":"gold-hero","gemstones":"gemstones-hero","watches":"watches-hero","auctions":"auctions-hero","retail-tech":"retail-hero"}

def best_img(slug, desk):
    """Article's own photo if it has one, else its desk's representative photo."""
    if slug in PH:
        return ("assets/ph/%s.jpg" % slug, True)
    h = DESK_HERO.get(desk)
    return ("assets/ph/%s.jpg" % h, False) if (h and h in PH) else ("", False)

def desk_hero_plate(desk, label="Plate I"):
    """Hero figure fallback: the desk's representative photo (tinted) instead of a glyph."""
    h = DESK_HERO.get(desk)
    if h and h in PH:
        return photo_plate(h, cls="plate-hero", eager=True, label=label)
    return motif_plate(desk, label)

_GLYPHS = {
 "diamonds": '<path d="M16 7 H32 L41 17 L24 42 L7 17 Z"/><path d="M7 17 H41 M16 7 L24 17 L32 7 M24 17 V42 M16 7 L12 17 M32 7 L36 17"/>',
 "gold-metals": '<path d="M5 37 L11 27 H26 L32 37 Z"/><path d="M18 26 L24 16 H39 L45 26 Z"/><path d="M11 27 L15 20 M32 37 L36 30"/>',
 "gemstones": '<path d="M15 7 H33 L42 16 V32 L33 41 H15 L6 32 V16 Z"/><path d="M18 12 H30 L37 18 V30 L30 36 H18 L11 30 V18 Z"/>',
 "watches": '<circle cx="24" cy="25" r="13.5"/><path d="M24 25 V16 M24 25 L30.5 28.5 M17 13 L20 7 H28 L31 13 M17 37 L20 43 H28 L31 37"/><circle cx="24" cy="25" r="1.6" fill="currentColor"/>',
 "auctions": '<path d="M10 16 L20 6 L30 16 L20 26 Z"/><path d="M25 21 L42 38 M40 36 L36 40 M6 42 H26"/>',
 "retail-tech": '<path d="M8 8 H24 L42 26 L26 42 L8 24 Z"/><circle cx="16.5" cy="16.5" r="3.2"/>',
}
def desk_glyph(slug, size=54):
    return (f'<svg class="dglyph" width="{size}" height="{size}" viewBox="0 0 48 48" fill="none" '
            f'stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" aria-hidden="true">{_GLYPHS.get(slug, _GLYPHS["diamonds"])}</svg>')

def photo_plate(slug, cls="", eager=False, label="Plate"):
    m = PH.get(slug)
    if not m:
        return ""
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    _cred = m["credit"] if "Carat Capital" in m.get("credit","") else f'{m["credit"]} · Wikimedia Commons'
    return (f'<figure class="lead-fig pfig{(" " + cls) if cls else ""}"><div class="plate-img">'
            f'<img src="assets/ph/{slug}.jpg" alt="" width="{m["w"]}" height="{m["h"]}" {load}></div>'
            f'<div class="cap"><span>{label} — {_cred}</span><span>CC</span></div></figure>')

def motif_plate(desk_slug, code=""):
    return (f'<figure class="lead-fig pfig mfig"><div class="mplate">{desk_glyph(desk_slug, 130)}</div>'
            f'<div class="cap"><span>Engraving — CC graphics desk</span><span>{code or desk_slug.upper()}</span></div></figure>')

_FIG_RE = _re.compile(r'^((?:Plus |Minus |Up |Down )?[$\u00a3\u20ac]?\d[\d,.]*(?:%| percent| million| billion| carats)?)')
def figwrap(title):
    return _FIG_RE.sub(r'<span class="fign">\1</span>', title, count=1)


def metadesc(text, limit=155):
    """Cut a dek for the search-result summary without breaking a word.

    Every dek on this site is longer than the meta-description slot (271 of 271,
    median 216 characters), so every page is cut. Slicing at a fixed 150 cut 160
    of them mid-word -- 'platinum and pa' -- which is what a reader saw in Google
    for seventeen days. Cut on a space instead and mark the cut.

    Applied to .site-repo/build.py on 2026-08-21. The same repair was made on
    2026-08-20 to website/build.py, which is a MIRROR: the publish run rsyncs this
    file over it, so that edit was erased and never reached a page. This copy is
    the one that ships.
    """
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    sp = cut.rfind(" ")
    if sp > limit * 0.6:
        cut = cut[:sp]
    return cut.rstrip(" ,;:.\u2014-") + "\u2026"


def head(title, desc, path="", extra=""):
    canonical = cu(f"{BASE_URL}/{path}") if path else BASE_URL
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
<script data-goatcounter="https://caratcapital.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css?v={CSS_V}">
{extra}
</head>
<body>
<div class="grain" aria-hidden="true"></div>
{DEFS}"""

def folio(right):
    return ""


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
    <a class="nav-sub" href="the-record.html"><span>The Record — catch up fast</span></a>
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
        <a href="natural-diamond-prices.html">The Natural Diamond Price List — Every Shape, Every Weight</a>
        <a href="lab-grown-diamond-prices.html">The Lab-Grown Diamond Price List — What a Made Diamond Costs</a>
        <a href="indices.html">The Carat Indices — The Trade, Marked to Market</a>
        <a href="magazine.html">The Folio — The Week, Bound</a>
        <a href="index.html#tape-a">The Price Tape</a>
        <a href="about.html">About the Paper</a>
        <a href="about.html#standards">Editorial Standards</a>
        <a href="about.html#contact">Write to the Desk</a>
      </div>
    </div>
    <div class="o-foot">Carat Capital · The trade paper of the jewelry world · Est. MMXXVI · Free to read</div>
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
        <a class="fl" href="field-guide.html">The Field Guide</a><a class="fl" href="the-record.html">The Record</a><a class="fl" href="almanac.html">The Almanac</a><a class="fl" href="natural-diamond-prices.html">Natural diamond prices</a><a class="fl" href="lab-grown-diamond-prices.html">Lab-grown diamond prices</a><a class="fl" href="about.html#contact">Write to the desk</a>
      </div>
      <div><h4>The Paper</h4>
        <a class="fl" href="index.html">Front page</a>
        <a class="fl" href="index.html#tape-a">The price tape</a>
        <a class="fl" href="natural-diamond-prices.html">The natural diamond price list</a>
        <a class="fl" href="lab-grown-diamond-prices.html">The lab-grown diamond price list</a>
        <a class="fl" href="feed.xml">RSS feed</a>
        <a class="fl" href="https://caratcapital.beehiiv.com">The Morning Brief — free</a>
      </div>
    </div>
    <div class="base">
      <div>© MMXXVI Carat Capital · Printed daily on the internet</div>
      <div>Free to read, cover to cover · caratcapital.org</div>
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
if(innerWidth>860)document.querySelectorAll('details.mob-collapse').forEach(d=>d.open=true);
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
<link>{BASE_URL}/a-{a["slug"]}</link>
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
    desks = "\n".join(f"- [{d['title']}]({BASE_URL}/{d['slug']}): {d['tag']}" for d in DESKS)
    arts = "\n".join(f"- [{a['title']}]({BASE_URL}/a-{a['slug']}): {a['dek'][:140]}" for a in ARTICLES[:15])
    return f"""# Carat Capital

> The trade paper of the jewelry world — original, sourced daily reporting on diamonds, gold and precious metals, colored gemstones, watches, jewelry auctions, and jewelry retail and technology. Published at {BASE_URL}. All articles are original writing with named, linked sources; prices are dated and indicative.

## The paper
- [Front page]({BASE_URL}/): today's edition, the wire, and the live price tape
- [The Record]({BASE_URL}/the-record): a dated, sourced week-by-week chronicle of the industry
- [The Almanac]({BASE_URL}/almanac): the quarter's key numbers in sourced tables (metals, exports, prices, auctions, retail)
- [The Natural Diamond Price List]({BASE_URL}/natural-diamond-prices): natural diamond prices by shape, weight, colour and clarity — wholesale trade benchmark and retail asking price side by side, with stated method and named sources
- [The Lab-Grown Diamond Price List]({BASE_URL}/lab-grown-diamond-prices): lab-grown diamond prices by shape and weight — retail asking prices against the published CVD and HPHT wholesale bands, the wholesale index, resale, and what was deliberately left out
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
  <h1 class="art-h" style="font-size:clamp(40px,6vw,86px);text-transform:uppercase">The Record<em style="font-family:var(--disp);font-style:normal;font-weight:400;color:var(--seal);text-transform:none;font-size:.5em;display:block;margin-top:12px;letter-spacing:-.01em">Eight weeks of the trade, kept properly</em></h1>
  <p class="dh-dek" style="max-width:760px">{RECORD.get("intro","")}</p>
</div></section>
<section class="burin"><div class="wrap">{weeks}
  <div style="padding:40px 0"><a class="big" href="almanac.html" style="font-family:var(--mono);font-size:12px;letter-spacing:.22em;text-transform:uppercase;border-bottom:2px solid var(--seal);padding-bottom:4px">The Almanac — the quarter in numbers →</a></div>
</div></section>
<section class="ctastrip"><div class="wrap"><div class="inner">
  <h2>Prefer the numbers? — <em>the Almanac tables the quarter.</em></h2>
  <a class="big" href="almanac.html">Open the Almanac →</a>
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
  <h1 class="art-h" style="font-size:clamp(40px,6vw,86px);text-transform:uppercase">The Almanac<em style="font-family:var(--disp);font-style:normal;font-weight:400;color:var(--seal);text-transform:none;font-size:.5em;display:block;margin-top:12px;letter-spacing:-.01em">The quarter, in numbers a desk can use</em></h1>
  <p class="dh-dek" style="max-width:760px">Every figure below is sourced and dated. Read it with The Record for the narrative; bring it to your Monday meeting for the argument.</p>
</div></section>
<section class="burin"><div class="wrap" style="columns:2;column-gap:64px;padding-top:30px">{tables}</div></section>
<section class="ctastrip"><div class="wrap"><div class="inner">
  <h2>Want the stories behind these numbers? — <em>read the Record.</em></h2>
  <a class="big" href="the-record.html">Open the Record →</a>
</div></div></section>
{colophon()}
{SCRIPT}"""

# ---------------- THE PRICE LIST (natural diamonds) ----------------
import math as _pm

PX_INK, PX_SEAL, PX_GILT, PX_DIM = "#16130E", "#BE3319", "#96762E", "#7A7263"
PX_SOFT, PX_HAIR = "rgba(22,19,14,.16)", "rgba(22,19,14,.07)"


def _usd(n, dp=0):
    return "$" + f"{n:,.{dp}f}"


def px_fig(svg, plate_no, caption, sub=""):
    """House figure wrapper — plate number, rule, caption."""
    return f"""<figure class="rv" style="margin:0 0 52px;break-inside:avoid">
  <figcaption style="display:flex;justify-content:space-between;align-items:baseline;gap:18px;border-bottom:2px solid var(--ink);padding-bottom:9px;margin-bottom:20px">
    <span style="font-family:var(--disp);font-weight:700;font-size:clamp(17px,2vw,22px);letter-spacing:-.02em">{caption}</span>
    <span style="font-family:var(--mono);font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--gilt);white-space:nowrap">CC/2026/{plate_no}</span>
  </figcaption>
  {f'<div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--seal);margin:-10px 0 18px">{sub}</div>' if sub else ''}
  <div style="width:100%;overflow:hidden">{svg}</div>
</figure>"""


def px_table(cols, rows, note="", src="", numeric_from=1):
    headr = ""
    for i, c in enumerate(cols):
        ta = "left" if i < numeric_from else "right"
        headr += (f'<th style="text-align:{ta};font-family:var(--mono);font-size:9px;letter-spacing:.18em;'
                  f'text-transform:uppercase;color:var(--ink-3);padding:0 0 10px 14px;border-bottom:2px solid var(--ink);'
                  f'white-space:nowrap">{c}</th>')
    body = ""
    for r in rows:
        muted = r[0].startswith("\x00")
        cells = ""
        for i, c in enumerate(r):
            c = c.lstrip("\x00")
            ta = "left" if i < numeric_from else "right"
            fam = "var(--text)" if i < numeric_from else "var(--mono)"
            fs = "14.5px" if i < numeric_from else "13px"
            op = ";opacity:.55" if muted else ""
            cells += (f'<td style="text-align:{ta};font-family:{fam};font-size:{fs};padding:9px 0 9px 14px;'
                      f'border-bottom:1px solid {PX_SOFT};white-space:nowrap{op}">{c}</td>')
        body += f"<tr>{cells}</tr>"
    out = (f'<div style="width:100%;overflow-x:auto"><table style="width:100%;min-width:520px;border-collapse:collapse">'
           f"<thead><tr>{headr}</tr></thead><tbody>{body}</tbody></table></div>")
    if note:
        out += (f'<p style="font-family:var(--text);font-size:14.5px;line-height:1.62;color:var(--ink-2);'
                f'margin:16px 0 0;max-width:70ch">{note}</p>')
    if src:
        out += (f'<div style="font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;'
                f'color:var(--gilt);margin-top:12px">Source — {src}</div>')
    return out


# ---- chart primitives -------------------------------------------------------

def px_curve(rows):
    """Log-scale per-carat curve: trade against retail, across the weight ladder."""
    W, Hh = 1040, 452
    L, R, T, B = 84, 96, 30, 62
    pw, ph = W - L - R, Hh - T - B
    lo, hi = _pm.log10(800), _pm.log10(45000)

    def y(v):
        return T + ph - (_pm.log10(v) - lo) / (hi - lo) * ph

    n = len(rows) - 1
    xs = [L + i * pw / n for i in range(len(rows))]

    grid, ylab = "", ""
    for g in (1000, 2000, 5000, 10000, 20000, 40000):
        gy = y(g)
        grid += f'<line x1="{L}" y1="{gy:.1f}" x2="{L+pw}" y2="{gy:.1f}" stroke="{PX_SOFT}" stroke-width="1"/>'
        lab = f"{g//1000}k" if g >= 1000 else str(g)
        ylab += (f'<text x="{L-12}" y="{gy+3.6:.1f}" text-anchor="end" font-family="IBM Plex Mono,monospace" '
                 f'font-size="10.5" fill="{PX_DIM}">${lab}</text>')

    xlab = ""
    for i, r in enumerate(rows):
        col = PX_SEAL if r["basis"] == "withheld" else PX_DIM
        xlab += (f'<text x="{xs[i]:.1f}" y="{T+ph+24}" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
                 f'font-size="10.5" fill="{col}">{r["wt"]:g}</text>')
    xlab += (f'<text x="{L+pw/2:.1f}" y="{T+ph+46}" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
             f'font-size="9" letter-spacing="2.4" fill="{PX_DIM}">CARATS</text>')

    def series(key, colour, dash):
        # kept = the weights this series actually prices. A break caused only by a
        # withheld band is bridged with a hairline so the eye follows the curve; a
        # break caused by a figure nobody publishes is left open on purpose.
        kept = [(i, xs[i], y(r[key])) for i, r in enumerate(rows) if r[key]]
        out, seg = "", []
        for i, px, py in kept:
            if seg and i - seg[-1][0] > 1:
                skipped = rows[seg[-1][0] + 1:i]
                if len(seg) > 1:
                    out += _poly([(a, b) for _, a, b in seg], colour, dash)
                if all(s["basis"] == "withheld" for s in skipped):
                    out += (f'<path d="M{seg[-1][1]:.1f} {seg[-1][2]:.1f} L{px:.1f} {py:.1f}" fill="none" '
                            f'stroke="{colour}" stroke-width="1.2" stroke-dasharray="1 4" opacity=".5"/>')
                seg = []
            seg.append((i, px, py))
        if len(seg) > 1:
            out += _poly([(a, b) for _, a, b in seg], colour, dash)
        for _, px, py in kept:
            out += (f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.6" fill="var(--paper)" stroke="{colour}" '
                    f'stroke-width="2.2"/>')
        return out

    def _poly(seg, colour, dash):
        d = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in seg)
        return f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="2.4" stroke-linejoin="round" {dash}/>'

    body = series("retail_ct", PX_SEAL, "") + series("trade_ct", PX_GILT, 'stroke-dasharray="7 4"')

    # gap marker over the withheld band
    gap = ""
    for i, r in enumerate(rows):
        if r["basis"] == "withheld":
            gap = (f'<line x1="{xs[i]:.1f}" y1="{T}" x2="{xs[i]:.1f}" y2="{T+ph}" stroke="{PX_SEAL}" '
                   f'stroke-width="1" stroke-dasharray="2 5" opacity=".65"/>'
                   f'<text x="{xs[i]:.1f}" y="{T-10}" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
                   f'font-size="9" letter-spacing="1.6" fill="{PX_SEAL}">WITHHELD</text>')

    # keyed top-left: the curves rise to the right, so this corner is always empty
    key = (f'<g transform="translate({L+18},{T+26})">'
           f'<line x1="0" y1="0" x2="28" y2="0" stroke="{PX_SEAL}" stroke-width="2.4"/>'
           f'<text x="37" y="3.6" font-family="IBM Plex Mono,monospace" font-size="10" fill="{PX_INK}">Retail asking</text>'
           f'<line x1="0" y1="19" x2="28" y2="19" stroke="{PX_GILT}" stroke-width="2.4" stroke-dasharray="7 4"/>'
           f'<text x="37" y="22.6" font-family="IBM Plex Mono,monospace" font-size="10" fill="{PX_INK}">Trade benchmark</text>'
           f'<text x="0" y="41" font-family="IBM Plex Mono,monospace" font-size="8.5" letter-spacing="1.1" '
           f'fill="{PX_DIM}">DOTTED BRIDGE = WITHHELD BAND</text></g>')

    return (f'<svg viewBox="0 0 {W} {Hh}" width="100%" role="img" aria-label="Per-carat price by weight, '
            f'trade against retail" style="display:block">'
            f'{grid}{ylab}'
            f'<line x1="{L}" y1="{T+ph}" x2="{L+pw}" y2="{T+ph}" stroke="{PX_INK}" stroke-width="1.6"/>'
            f'{gap}{body}{xlab}{key}</svg>')


def px_bars(rows, colour=PX_SEAL, unit="$", show=None, tint=None):
    """Horizontal bars. rows = [{label, value, right, flag}]"""
    rowh, gap, lw, vw = 30, 8, 176, 108
    W = 1040
    bw = W - lw - vw - 26
    Hh = len(rows) * (rowh + gap) + 16
    out = ""
    mx = max(r["value"] for r in rows) or 1
    for i, r in enumerate(rows):
        yy = i * (rowh + gap) + 6
        w = max(r["value"] / mx * bw, 2)
        col = tint(r) if tint else colour
        flag = r.get("flag")
        out += (f'<text x="{lw-14}" y="{yy+rowh/2+4.6:.1f}" text-anchor="end" font-family="Instrument Sans,sans-serif" '
                f'font-size="13.5" fill="{PX_INK}">{r["label"]}</text>')
        out += f'<rect x="{lw}" y="{yy}" width="{bw}" height="{rowh}" fill="{PX_HAIR}"/>'
        out += f'<rect x="{lw}" y="{yy}" width="{w:.1f}" height="{rowh}" fill="{col}"/>'
        if flag:
            out += (f'<rect x="{lw}" y="{yy}" width="{w:.1f}" height="{rowh}" fill="url(#pxHatch)" opacity=".5"/>')
        out += (f'<text x="{W-26}" y="{yy+rowh/2+4.6:.1f}" text-anchor="end" font-family="IBM Plex Mono,monospace" '
                f'font-size="12.5" fill="{PX_INK}">{r["right"]}</text>')
    hatch = ('<defs><pattern id="pxHatch" width="6" height="6" patternUnits="userSpaceOnUse" '
             'patternTransform="rotate(45)"><rect width="6" height="6" fill="none"/>'
             '<line x1="0" y1="0" x2="0" y2="6" stroke="#F2EDE3" stroke-width="2"/></pattern></defs>')
    return (f'<svg viewBox="0 0 {W} {Hh}" width="100%" role="img" style="display:block">{hatch}{out}</svg>')


def px_spread(rows):
    """Markup-decay curve."""
    W, Hh = 1040, 300
    L, R, T, B = 74, 30, 26, 56
    pw, ph = W - L - R, Hh - T - B
    n = len(rows) - 1
    mx = 120
    xs = [L + i * pw / n for i in range(len(rows))]
    ys = [T + ph - r["pct"] / mx * ph for r in rows]
    grid, ylab = "", ""
    for g in (0, 30, 60, 90, 120):
        gy = T + ph - g / mx * ph
        grid += f'<line x1="{L}" y1="{gy:.1f}" x2="{L+pw}" y2="{gy:.1f}" stroke="{PX_SOFT}" stroke-width="1"/>'
        ylab += (f'<text x="{L-12}" y="{gy+3.6:.1f}" text-anchor="end" font-family="IBM Plex Mono,monospace" '
                 f'font-size="10.5" fill="{PX_DIM}">+{g}%</text>')
    line = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in zip(xs, ys))
    area = line + f" L{xs[-1]:.1f} {T+ph:.1f} L{xs[0]:.1f} {T+ph:.1f} Z"
    dots, xlab = "", ""
    for i, r in enumerate(rows):
        dots += (f'<circle cx="{xs[i]:.1f}" cy="{ys[i]:.1f}" r="3.6" fill="var(--paper)" stroke="{PX_SEAL}" '
                 f'stroke-width="2.2"/>')
        dots += (f'<text x="{xs[i]:.1f}" y="{ys[i]-13:.1f}" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
                 f'font-size="10.5" fill="{PX_SEAL}">{r["pct"]}</text>')
        xlab += (f'<text x="{xs[i]:.1f}" y="{T+ph+24}" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
                 f'font-size="10.5" fill="{PX_DIM}">{r["w"].split()[0]}</text>')
    xlab += (f'<text x="{L+pw/2:.1f}" y="{T+ph+44}" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
             f'font-size="9" letter-spacing="2.4" fill="{PX_DIM}">CARATS</text>')
    return (f'<svg viewBox="0 0 {W} {Hh}" width="100%" role="img" aria-label="Retail markup over the trade '
            f'benchmark, by weight" style="display:block">{grid}{ylab}'
            f'<path d="{area}" fill="{PX_SEAL}" opacity=".10"/>'
            f'<path d="{line}" fill="none" stroke="{PX_SEAL}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<line x1="{L}" y1="{T+ph}" x2="{L+pw}" y2="{T+ph}" stroke="{PX_INK}" stroke-width="1.6"/>'
            f'{dots}{xlab}</svg>')


# ---- page section helpers ---------------------------------------------------

def px_sec(title, em, note=""):
    return (f'<div class="sec-mast rv"><h2>{title} — <em>{em}</em></h2>'
            f'<div class="mono-note">{note}</div></div>')


def px_lede(text):
    return (f'<p class="rv" style="font-family:var(--text);font-size:clamp(16px,1.5vw,18.5px);line-height:1.66;'
            f'color:var(--ink-2);max-width:74ch;margin:0 0 30px">{text}</p>')


def px_flag(text):
    return (f'<div class="rv" style="border-left:3px solid var(--seal);padding:2px 0 2px 18px;margin:26px 0 0;'
            f'max-width:74ch"><div style="font-family:var(--mono);font-size:9px;letter-spacing:.22em;'
            f'text-transform:uppercase;color:var(--seal);margin-bottom:7px">A note on this figure</div>'
            f'<p style="font-family:var(--text);font-size:14.5px;line-height:1.62;color:var(--ink-2)">{text}</p></div>')


def prices_page():
    P = PRICES
    hd = P["headline"]

    # -- headline block
    stat = lambda v, l, c: (
        f'<div><b style="display:block;font-family:var(--mono);font-size:clamp(26px,4vw,44px);font-weight:500;'
        f'letter-spacing:-.03em;color:{c};line-height:1">{v}</b>'
        f'<span style="display:block;font-family:var(--mono);font-size:9px;letter-spacing:.2em;text-transform:uppercase;'
        f'color:var(--ink-3);margin-top:10px">{l}</span></div>')
    headline = f"""<div class="rv" style="border-top:3px solid var(--ink);border-bottom:1px solid {PX_SOFT};padding:26px 0 28px;margin:0 0 12px">
  <div style="font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--seal);margin-bottom:20px">The benchmark stone — {hd['spec']}</div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:30px 26px">
    {stat(_usd(hd['trade_ct']), 'Trade / ct', 'var(--gilt)')}
    {stat(_usd(hd['retail_ct']), 'Retail asking / ct', 'var(--seal)')}
    {stat('+' + str(hd['spread_pct']) + '%', 'The spread', 'var(--ink)')}
    {stat(str(hd['vs_list_pct']) + '%', 'vs Rapaport list', 'var(--ink-3)')}
  </div>
  <p style="font-family:var(--text);font-size:15.5px;line-height:1.64;color:var(--ink-2);max-width:70ch;margin:26px 0 0">{hd['note']}</p>
</div>"""

    # -- weight table + curve
    wt = P["weights"]
    wrows = []
    for r in wt["rows"]:
        if r["basis"] == "withheld":
            wrows.append(["\x00" + r["w"], "—", "—", "—", "—", "—", "Withheld"])
        else:
            b = {"observed": "Observed", "modelled": "Modelled", "retail-only": "Retail only"}[r["basis"]]
            wrows.append([
                r["w"],
                _usd(r["trade_ct"]) if r["trade_ct"] else "—",
                _usd(r["trade_stone"]) if r["trade_stone"] else "—",
                _usd(r["retail_ct"]),
                _usd(r["retail_stone"]),
                f"+{r['spread']}%" if r["spread"] else "—",
                b])
    weight_tbl = px_table(
        ["Weight", "Trade / ct", "Trade, stone", "Retail / ct", "Retail, stone", "Spread", "Basis"],
        wrows,
        src="IDEX price drivers 30 July 2026 · RAPI 1 July 2026 · six-retailer median 30 July 2026")

    dual = P["dual_basis"]
    dual_tbl = px_table(
        ["Weight", "RAPI · D–H / IF–VS2", "IDEX · market average", "Gap"],
        [[r["w"], _usd(r["rapi"]), _usd(r["idex"]) if r["idex"] else "no driver", r["gap"] or "—"] for r in dual["rows"]],
        note=dual["note"])

    # -- shapes
    sh = P["shapes"]
    sh_bars = px_bars(
        [{"label": r["s"], "value": r["usd"], "right": _usd(r["usd"]) + ("  ·  " + (f"{r['d']:+.1f}%" if r["d"] else "base")),
          "flag": r["conf"] == "conflicted"} for r in sh["rows"]],
        tint=lambda r: PX_GILT if r["flag"] else PX_SEAL)
    sh_tbl = px_table(
        ["Shape", "Asking / ct", "Against round", "Cross-source range", "Family"],
        [[r["s"], _usd(r["usd"]), (f"{r['d']:+.1f}%" if r["d"] else "baseline"), r["band"],
          {"brilliant": "Round", "elongated": "Elongated brilliant", "step": "Step / square"}[r["tier"]]]
         for r in sh["rows"]],
        src="StoneAlgo live asking-price sample, n=169,324, 30 July 2026")
    tiers = "".join(
        f"""<div class="glo rv"><div class="term">{t['name']}<i>{t['range']}</i></div><p>{t['why']}</p></div>"""
        for t in sh["tiers"])

    # -- colour + clarity
    col, cla = P["colour"], P["clarity"]
    col_bars = px_bars([{"label": r["g"], "value": r["usd"], "right": f'{_usd(r["usd"])}  ·  {r["idx"]}'} for r in col["rows"]])
    cla_bars = px_bars([{"label": r["g"], "value": r["usd"], "right": f'{_usd(r["usd"])}  ·  {r["idx"]}'} for r in cla["rows"]],
                       colour=PX_GILT)
    col_tbl = px_table(["Colour", "Index", "Applied / ct", ""],
                       [[r["g"], str(r["idx"]), _usd(r["usd"]), r["note"]] for r in col["rows"]], numeric_from=1)
    cla_tbl = px_table(["Clarity", "Index", "Applied / ct", ""],
                       [[r["g"], str(r["idx"]), _usd(r["usd"]), r["note"]] for r in cla["rows"]], numeric_from=1)

    # -- retailers, magic, lab
    rt = P["retailers"]
    rt_tbl = px_table(["Counter", "Asking / ct", "Tier"],
                      [[r["n"], _usd(r["usd"]), r["t"]] for r in rt["rows"]], note=rt["note"])
    mg_tbl = px_table(["Step", "Per carat", "Reading"],
                      [[r["step"], r["pct"], r["note"]] for r in P["magic"]["rows"]])
    lb = P["lab"]
    lb_tbl = px_table(["Measure", "Figure"], [[r["k"], r["v"]] for r in lb["rows"]])

    ctx = "".join(f"""<div class="brf rv"><div class="bn">M—{i+1:02d}</div><h3>{c['h']}</h3><p>{c['b']}</p></div>"""
                  for i, c in enumerate(P["context"]["rows"]))
    meth = "".join(f"""<div class="glo rv"><div class="term">{m['h']}</div><p>{m['b']}</p></div>"""
                   for m in P["method"]["rows"])
    srcs = "".join(
        f'<tr><td style="font-family:var(--text);font-size:14px;padding:8px 14px 8px 0;border-bottom:1px solid {PX_HAIR}">{s["n"]}</td>'
        f'<td style="font-family:var(--mono);font-size:11.5px;padding:8px 14px 8px 0;border-bottom:1px solid {PX_HAIR};'
        f'white-space:nowrap;color:var(--ink-3)">{s["d"]}</td>'
        f'<td style="font-family:var(--mono);font-size:11.5px;padding:8px 0;border-bottom:1px solid {PX_HAIR};'
        f'color:var(--gilt)">{s["u"]}</td></tr>' for s in P["sources"])
    excl = "".join(f'<li style="margin-bottom:9px"><b style="font-family:var(--mono);font-size:12.5px">{e["n"]}</b> — {e["why"]}</li>'
                   for e in P["excluded"])

    return f"""{head("The Natural Diamond Price List — every shape, every weight — Carat Capital",
                     "Natural diamond prices for 2026: wholesale trade benchmark and retail asking price side by side, across ten shapes and eleven weight bands, with colour and clarity ladders, sources and method.",
                     "natural-diamond-prices.html")}
{folio("The Price Desk · Natural diamonds")}
{navbar()}
{omenu()}

<section class="deskhero"><div class="wrap">
  <div class="dh-no">The Price Desk · Natural · Updated {P['as_of']}</div>
  <h1 class="art-h" style="font-size:clamp(38px,5.6vw,80px);text-transform:uppercase;max-width:16ch">The Natural Diamond Price List<em style="font-family:var(--disp);font-style:normal;font-weight:400;color:var(--seal);text-transform:none;font-size:.34em;display:block;margin-top:16px;letter-spacing:-.01em">{P['kicker']}</em></h1>
  <p class="dh-dek" style="max-width:78ch">{P['standfirst']}</p>
</div></section>

<section class="burin"><div class="wrap" style="padding-top:34px">
  {headline}
</div></section>

<section class="burin"><div class="wrap">
  {px_sec("Weight", "what a carat costs, all the way up", "Figure CC/2026/149")}
  {px_lede(wt['sub'])}
  {px_fig(px_curve(wt['rows']), '149', 'Per carat, by weight', 'Log scale · trade against retail asking · USD')}
  {weight_tbl}
  {px_flag(wt['withheld_note'])}
  {px_flag(wt['ten_note'])}
</div></section>

<section class="burin"><div class="wrap">
  {px_sec("The spread", "how much the counter adds", "Figure CC/2026/150")}
  {px_lede(P['spread']['note'])}
  {px_fig(px_spread(P['spread']['rows']), '150', 'Retail markup over the trade benchmark', 'Percentage added, by weight')}
  {px_table(["Evidence", "Reading"], [[e["k"], e["v"]] for e in P['spread']['evidence']])}
</div></section>

<section class="burin"><div class="wrap">
  {px_sec("Two benchmarks", "why the trade quotes two numbers")}
  {dual_tbl}
</div></section>

<section class="burin"><div class="wrap">
  {px_sec("Shape", "ten cuts, one carat, one grading standard", "Figure CC/2026/151")}
  {px_lede(sh['sub'])}
  {px_fig(sh_bars, '151', 'Asking price per carat, by shape', 'Hatched bars carry conflicting sources')}
  {sh_tbl}
  {px_flag(sh['conflict_note'])}
  <div class="glo-grid" style="margin-top:38px">{tiers}</div>
</div></section>

<section class="burin"><div class="wrap">
  {px_sec("Colour and clarity", "the two ladders that set the price", "Figures CC/2026/152–153")}
  {px_lede("Weight tells you how big. Shape tells you what it looks like. Colour and clarity tell you what it costs — and between them they move the price of a one-carat round by more than a factor of two in each direction.")}
  {px_fig(col_bars, '152', col['caption'] + ' — ' + col['sub'], 'H = 100 · applied to the observed one-carat retail median')}
  {col_tbl}
  {px_flag(col['note'])}
  <div style="height:56px"></div>
  {px_fig(cla_bars, '153', cla['caption'] + ' — ' + cla['sub'], 'VS2 = 100 · applied to the observed one-carat retail median')}
  {cla_tbl}
  {px_flag(cla['note'])}
  {px_flag(P['matrix_note'])}
</div></section>

<section class="burin"><div class="wrap">
  {px_sec("Six counters", "the same certificate, six prices")}
  {rt_tbl}
</div></section>

<section class="burin"><div class="wrap">
  {px_sec("The magic weights", "what crossing a round number costs")}
  {mg_tbl}
  {px_flag(P['magic']['band_caveat'])}
  {px_lede(P['magic']['note'])}
</div></section>

<section class="burin"><div class="wrap">
  {px_sec("Against lab-grown", "where the two markets now sit")}
  {lb_tbl}
  {px_flag(lb['inversion'])}
</div></section>

<section class="briefing"><div class="wrap">
  {px_sec("What moved the numbers", "the market behind the table")}
  <div class="brf-grid">{ctx}</div>
</div></section>

<section class="glossary burin"><div class="wrap">
  {px_sec("Method", "observed, modelled, withheld")}
  <div class="glo-grid">{meth}</div>
  <div class="rv" style="margin-top:52px">
    <h3 style="font-family:var(--disp);font-weight:700;font-size:21px;letter-spacing:-.02em;border-bottom:2px solid var(--ink);padding-bottom:9px;margin-bottom:6px">Sources</h3>
    <table style="width:100%;border-collapse:collapse"><tbody>{srcs}</tbody></table>
  </div>
  <div class="rv" style="margin-top:38px;max-width:74ch">
    <h3 style="font-family:var(--disp);font-weight:700;font-size:17px;letter-spacing:-.02em;margin-bottom:12px">What we left out, and why</h3>
    <ul style="font-family:var(--text);font-size:14.5px;line-height:1.6;color:var(--ink-2);padding-left:20px">{excl}</ul>
  </div>
</div></section>

<section class="ctastrip"><div class="wrap"><div class="inner">
  <h2>The quarter's other numbers — <em>metals, exports, salerooms, retail.</em></h2>
  <a class="big" href="almanac.html">Open the Almanac →</a>
</div></div></section>
{colophon()}
{SCRIPT}"""



# ---------------- THE LAB-GROWN PRICE LIST ----------------
# Same reporting as the natural list, half the height. Everything that runs
# down the page there runs across it here: paired columns, dumbbells instead
# of two bar charts, one apparatus row instead of three stacked blocks.

def lx_table(cols, rows, numeric_from=1, min_w=320):
    """Tighter cousin of px_table, sized to sit inside a half-width column."""
    headr = ""
    for i, c in enumerate(cols):
        ta = "left" if i < numeric_from else "right"
        headr += (f'<th style="text-align:{ta};font-family:var(--mono);font-size:8.5px;letter-spacing:.15em;'
                  f'text-transform:uppercase;color:var(--ink-3);padding:0 0 8px 10px;border-bottom:2px solid var(--ink);'
                  f'white-space:nowrap">{c}</th>')
    body = ""
    for r in rows:
        mark = r[0][:1]
        muted, strong = mark == "\x00", mark == "\x01"
        cells = ""
        for i, c in enumerate(r):
            c = c.lstrip("\x00\x01")
            ta = "left" if i < numeric_from else "right"
            fam = "var(--text)" if i < numeric_from else "var(--mono)"
            fs = "13.4px" if i < numeric_from else "12px"
            sty = ";opacity:.5" if muted else (";color:var(--seal)" if strong else "")
            cells += (f'<td style="text-align:{ta};font-family:{fam};font-size:{fs};padding:7px 0 7px 10px;'
                      f'border-bottom:1px solid {PX_HAIR};white-space:nowrap{sty}">{c}</td>')
        body += f"<tr>{cells}</tr>"
    return (f'<div style="width:100%;overflow-x:auto"><table style="width:100%;min-width:{min_w}px;'
            f'border-collapse:collapse"><thead><tr>{headr}</tr></thead>'
            f"<tbody>{body}</tbody></table></div>")


def lx_head(n, title, em, plate=""):
    pl = f'<div class="pl">{plate}</div>' if plate else ""
    return (f'<div class="lx-h rv"><div class="lx-n">{n}</div>'
            f"<h2>{title} <em>{em}</em></h2>{pl}</div>")


def lx_lede(t):
    return f'<p class="lx-lede rv">{t}</p>'


def lx_note(t, label="A note on this figure", gilt=False):
    cls = "lx-note lx-note--gilt" if gilt else "lx-note"
    return f'<div class="{cls} rv"><span class="lb">{label}</span><p>{t}</p></div>'


def lx_src(t):
    return f'<div class="lx-src">Source — {t}</div>'


def _lxpoly(pts, colour, dash="", w=2.2):
    d = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
    return f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{w}" stroke-linejoin="round" {dash}/>'


def lx_flat(rows):
    """The whole page in one figure: lab per-carat flat, natural per-carat climbing."""
    W, Hh = 640, 396
    L, R, T, B = 54, 72, 30, 52
    pw, ph = W - L - R, Hh - T - B
    lo, hi = _pm.log10(400), _pm.log10(40000)

    def y(v):
        return T + ph - (_pm.log10(v) - lo) / (hi - lo) * ph

    n = len(rows) - 1
    xs = [L + i * pw / n for i in range(len(rows))]

    grid = ylab = ""
    for g, lb in ((500, "$500"), (1000, "$1k"), (2500, "$2.5k"), (5000, "$5k"),
                  (10000, "$10k"), (25000, "$25k")):
        gy = y(g)
        grid += f'<line x1="{L}" y1="{gy:.1f}" x2="{L+pw}" y2="{gy:.1f}" stroke="{PX_SOFT}" stroke-width="1"/>'
        ylab += (f'<text x="{L-10}" y="{gy+3.4:.1f}" text-anchor="end" font-family="IBM Plex Mono,monospace" '
                 f'font-size="9.5" fill="{PX_DIM}">{lb}</text>')

    # the widening gap, tinted. the 4 ct step has no natural mark, so the band
    # cuts straight across it and the natural line is dashed there.
    kept = [i for i, r in enumerate(rows) if r["nat_ct"]]
    top = " L".join(f'{xs[i]:.1f} {y(rows[i]["nat_ct"]):.1f}' for i in kept)
    bot = " L".join(f'{xs[i]:.1f} {y(rows[i]["lab_ct"]):.1f}' for i in reversed(kept))
    band = f'<path d="M{top} L{bot} Z" fill="{PX_GILT}" opacity=".11"/>'

    natp, brid, run = "", "", []
    for i, r in enumerate(rows):
        if not r["nat_ct"]:
            continue
        if run and i - run[-1] > 1:
            brid += (f'<path d="M{xs[run[-1]]:.1f} {y(rows[run[-1]]["nat_ct"]):.1f} '
                     f'L{xs[i]:.1f} {y(r["nat_ct"]):.1f}" fill="none" stroke="{PX_GILT}" '
                     f'stroke-width="1.4" stroke-dasharray="2 4" opacity=".8"/>')
            if len(run) > 1:
                natp += _lxpoly([(xs[k], y(rows[k]["nat_ct"])) for k in run], PX_GILT)
            run = []
        run.append(i)
    if len(run) > 1:
        natp += _lxpoly([(xs[k], y(rows[k]["nat_ct"])) for k in run], PX_GILT)

    labp = _lxpoly([(xs[i], y(r["lab_ct"])) for i, r in enumerate(rows)], PX_SEAL, w=2.6)

    dots = ratios = xlab = ""
    for i, r in enumerate(rows):
        dots += (f'<circle cx="{xs[i]:.1f}" cy="{y(r["lab_ct"]):.1f}" r="3.4" fill="var(--paper)" '
                 f'stroke="{PX_SEAL}" stroke-width="2.2"/>')
        if r["nat_ct"]:
            dots += (f'<circle cx="{xs[i]:.1f}" cy="{y(r["nat_ct"]):.1f}" r="3.4" fill="var(--paper)" '
                     f'stroke="{PX_GILT}" stroke-width="2.2"/>')
            my = (y(r["nat_ct"]) + y(r["lab_ct"])) / 2
            ratios += (f'<text x="{xs[i]:.1f}" y="{my+3.6:.1f}" text-anchor="middle" paint-order="stroke" '
                       f'stroke="#F2EDE3" stroke-width="3.4" font-family="IBM Plex Mono,monospace" '
                       f'font-size="11" fill="{PX_GILT}">{r["ratio"]:g}×</text>')
        col = PX_SEAL if not r["nat_ct"] else PX_DIM
        xlab += (f'<text x="{xs[i]:.1f}" y="{T+ph+22}" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
                 f'font-size="10" fill="{col}">{r["wt"]:g}</text>')
    xlab += (f'<text x="{L+pw/2:.1f}" y="{T+ph+42}" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
             f'font-size="8.5" letter-spacing="2.2" fill="{PX_DIM}">CARATS</text>')

    tags = (f'<text x="{L+pw+9}" y="{y(rows[-1]["nat_ct"])+3.4:.1f}" font-family="IBM Plex Mono,monospace" '
            f'font-size="8.5" letter-spacing="1.1" fill="{PX_GILT}">NATURAL</text>'
            f'<text x="{L+pw+9}" y="{y(rows[-1]["lab_ct"])+3.4:.1f}" font-family="IBM Plex Mono,monospace" '
            f'font-size="8.5" letter-spacing="1.1" fill="{PX_SEAL}">LAB</text>')

    return (f'<svg viewBox="0 0 {W} {Hh}" width="100%" role="img" aria-label="Price per carat by weight, '
            f'lab-grown against natural, log scale" style="display:block">{grid}{ylab}{band}{brid}{natp}'
            f'{labp}<line x1="{L}" y1="{T+ph}" x2="{L+pw}" y2="{T+ph}" stroke="{PX_INK}" stroke-width="1.5"/>'
            f"{ratios}{dots}{xlab}{tags}</svg>")


def lx_swing(rows):
    """Dumbbell: where each shape sits against a round, natural and lab, on one axis."""
    W = 640
    L, R, T = 84, 78, 62
    rowh, gapy = 26, 6
    pw = W - L - R
    Hh = T + len(rows) * (rowh + gapy) + 12
    lo, hi = -48.0, 30.0

    def x(v):
        return L + (v - lo) / (hi - lo) * pw

    grid = glab = ""
    for g in (-40, -20, 0, 20):
        gx = x(g)
        wid = "1.6" if g == 0 else "1"
        colr = PX_INK if g == 0 else PX_SOFT
        gl = "0" if g == 0 else f"{g:+g}".replace("-", "\u2212")
        grid += f'<line x1="{gx:.1f}" y1="{T-10}" x2="{gx:.1f}" y2="{Hh-8}" stroke="{colr}" stroke-width="{wid}"/>'
        glab += (f'<text x="{gx:.1f}" y="{T-16}" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
                 f'font-size="9.5" fill="{PX_DIM}">{gl}%</text>')
    glab += (f'<text x="{x(0):.1f}" y="{T-32}" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
             f'font-size="8.5" letter-spacing="1.4" fill="{PX_INK}">THE ROUND</text>')

    body = ""
    for i, r in enumerate(rows):
        yy = T + i * (rowh + gapy) + rowh / 2
        xa, xb = x(r["nat_d"]), x(r["d"])
        body += (f'<text x="{L-14}" y="{yy+4.4:.1f}" text-anchor="end" font-family="Instrument Sans,sans-serif" '
                 f'font-size="12.5" fill="{PX_INK}">{r["s"]}</text>')
        if abs(xb - xa) > 1:
            body += (f'<line x1="{xa:.1f}" y1="{yy:.1f}" x2="{xb:.1f}" y2="{yy:.1f}" stroke="{PX_SOFT}" '
                     f'stroke-width="5" stroke-linecap="round"/>')
        body += (f'<circle cx="{xa:.1f}" cy="{yy:.1f}" r="4.4" fill="var(--paper)" stroke="{PX_GILT}" '
                 f'stroke-width="2.2"/>')
        fill = PX_SEAL if r["inv"] else "var(--paper)"
        body += (f'<circle cx="{xb:.1f}" cy="{yy:.1f}" r="4.4" fill="{fill}" stroke="{PX_SEAL}" '
                 f'stroke-width="2.2"/>')
        sw = "—" if not r["swing"] else f'{r["swing"]:+.1f}'
        body += (f'<text x="{W-8}" y="{yy+4.2:.1f}" text-anchor="end" font-family="IBM Plex Mono,monospace" '
                 f'font-size="11" fill="{PX_DIM}">{sw}</text>')

    key = (f'<text x="{W-8}" y="{T-16}" text-anchor="end" font-family="IBM Plex Mono,monospace" '
           f'font-size="8.5" letter-spacing="1.1" fill="{PX_DIM}">SWING, PTS</text>'
           f'<circle cx="{L+4}" cy="{T-52}" r="4.4" fill="var(--paper)" stroke="{PX_GILT}" stroke-width="2.2"/>'
           f'<text x="{L+15}" y="{T-48.4}" font-family="IBM Plex Mono,monospace" font-size="9" '
           f'fill="{PX_INK}">Natural</text>'
           f'<circle cx="{L+78}" cy="{T-52}" r="4.4" fill="{PX_SEAL}" stroke="{PX_SEAL}" stroke-width="2.2"/>'
           f'<text x="{L+89}" y="{T-48.4}" font-family="IBM Plex Mono,monospace" font-size="9" '
           f'fill="{PX_INK}">Lab · filled = dearer than round</text>')

    return (f'<svg viewBox="0 0 {W} {Hh}" width="100%" role="img" aria-label="Each shape against a round '
            f'brilliant, natural and lab-grown" style="display:block">{grid}{glab}{key}{body}</svg>')


def lx_range(rows):
    """Four counters, one specification, three weights — the asking-price range."""
    W = 640
    L, R, T = 62, 58, 44
    rowh, gapy = 50, 16
    pw = W - L - R
    Hh = T + len(rows) * (rowh + gapy) + 6
    mx = 3400.0
    keys = [("ritani", "Ritani"), ("clean", "Clean Origin"), ("clarity", "Clarity"), ("be", "Brilliant Earth")]

    def x(v):
        return L + v / mx * pw

    grid = glab = ""
    for g in (0, 1000, 2000, 3000):
        gx = x(g)
        grid += f'<line x1="{gx:.1f}" y1="{T-14}" x2="{gx:.1f}" y2="{Hh-14}" stroke="{PX_SOFT}" stroke-width="1"/>'
        lbl = "$0" if not g else f"${g//1000}k"
        glab += (f'<text x="{gx:.1f}" y="{T-22}" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
                 f'font-size="9.5" fill="{PX_DIM}">{lbl}</text>')
    glab += (f'<text x="{L}" y="{T-38}" font-family="IBM Plex Mono,monospace" font-size="8.5" '
             f'letter-spacing="1.4" fill="{PX_INK}">ASKING PRICE PER CARAT</text>')

    body = ""
    for i, r in enumerate(rows):
        yy = T + i * (rowh + gapy) + 20
        vals = [r[k] for k, _ in keys]
        a, b = min(vals), max(vals)
        body += (f'<text x="{L-12}" y="{yy+4.2:.1f}" text-anchor="end" font-family="Instrument Sans,sans-serif" '
                 f'font-size="12.5" fill="{PX_INK}">{r["w"].split()[0]}</text>')
        body += (f'<line x1="{x(a):.1f}" y1="{yy:.1f}" x2="{x(b):.1f}" y2="{yy:.1f}" stroke="{PX_SEAL}" '
                 f'stroke-width="5" opacity=".22" stroke-linecap="round"/>')
        for k, _ in keys:
            body += (f'<circle cx="{x(r[k]):.1f}" cy="{yy:.1f}" r="3.6" fill="var(--paper)" stroke="{PX_SEAL}" '
                     f'stroke-width="2"/>')
        body += (f'<text x="{x(a):.1f}" y="{yy-11:.1f}" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
                 f'font-size="10" fill="{PX_DIM}">${a:,}</text>')
        body += (f'<text x="{x(b):.1f}" y="{yy-11:.1f}" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
                 f'font-size="10" fill="{PX_SEAL}">${b:,}</text>')
        body += (f'<text x="{L}" y="{yy+21:.1f}" font-family="IBM Plex Mono,monospace" font-size="9.5" '
                 f'fill="{PX_DIM}">{r["x"]:g}× cheapest to dearest</text>')

    return (f'<svg viewBox="0 0 {W} {Hh}" width="100%" role="img" aria-label="Retail asking price range '
            f'across four counters, by weight" style="display:block">{grid}{glab}{body}</svg>')


def lab_prices_page():
    P = LAB
    hd = P["headline"]
    wt, sh, ld = P["weights"], P["shapes"], P["ladder"]
    ms, dp, ix = P["method_split"], P["dispersion"], P["divergence"]

    # -- headline band: six figures, one rail
    def bstat(v, l, c="var(--ink)"):
        return (f'<div><b style="color:{c}">{v}</b><span>{l}</span></div>')
    vsn = f"{hd['vs_nat_pct']:g}".replace("-", "\u2212") + "%"
    band = f"""<div class="lx-band rv">
  <div class="spec">The benchmark stone — {hd['spec']}</div>
  <div class="row">
    {bstat(_usd(hd['retail_ct']), 'Retail asking / ct', 'var(--seal)')}
    {bstat('$' + str(hd['trade_lo']) + '–' + str(hd['trade_hi']), 'Wholesale band, CVD', 'var(--gilt)')}
    {bstat(vsn, 'Against natural')}
    {bstat(hd['spread_x'], 'Cheapest to dearest')}
    {bstat(P['index']['rows'][0]['v'], 'Wholesale, year on year')}
    {bstat(P['index']['rows'][1]['v'], 'Since July 2018', 'var(--ink-3)')}
  </div>
  <p>{hd['note']}</p>
</div>"""

    # -- 01 weight
    wrows = []
    for r in wt["rows"]:
        has = bool(r["nat_ct"])
        wrows.append([
            r["w"],
            _usd(r["stone"]),
            _usd(r["lab_ct"]),
            _usd(r["nat_ct"]) if has else "—",
            f'{r["ratio"]:g}×' if has else "—",
            f'−{r["disc"]:g}%' if has else "no natural mark"])
    wtbl = lx_table(["Weight", "Lab, stone", "Lab / ct", "Natural / ct", "Multiple", "Discount"], wrows, min_w=400)

    # -- 02 shape
    chips = "".join(
        f'<div class="{"up" if r["d"] > 0 else "dn"}"><i>{r["s"]}</i><b>{_usd(r["usd"])}</b></div>'
        for r in sh["rows"])
    stab = lx_table(
        ["Shape", "1.00 ct", "2.00 ct", "3.00 ct"],
        [[("\x01" if r["all3"] else "") + r["s"], r["one"].replace("-", "−"),
          r["two"].replace("-", "−"), r["three"].replace("-", "−")] for r in sh["stability"]],
        min_w=300)

    # -- 03 the ladder we will not model
    ldtbl = lx_table(["Measure", "Figure", "Basis"],
                     [[r["k"], r["v"], r["b"].title()] for r in ld["rows"]], min_w=330)

    # -- 04 how it was grown
    mstbl = lx_table(["Band", "CVD / ct", "HPHT / ct", "HPHT"],
                     [[r["band"], r["cvd"], r["hpht"], r["prem"]] for r in ms["rows"]], min_w=340)

    # -- 06 the wholesale index
    ixtbl = lx_table(["Measure", "Change", "Period"],
                     [[("\x01" if r["v"].startswith("+") else "") + r["k"], r["v"], r["d"]]
                      for r in P["index"]["rows"]], min_w=330)

    # -- 07 divergence
    dvtbl = lx_table(["Measure"] + ix["cols"],
                     [[r["k"], r["a"], r["b"], r["c"]] for r in ix["rows"]], min_w=380)

    # -- 08 resale
    rs = P["resale"]
    rstbl = lx_table(["Measure", "Figure"], [[r["k"], r["v"]] for r in rs["rows"]], min_w=260)

    tiles = "".join(
        f"""<div class="rv"><div class="n">M—{i+1:02d}</div><h3>{c['h']}</h3><p>{c['b']}</p></div>"""
        for i, c in enumerate(P["context"]["rows"]))
    meth = "".join(f"""<div class="m"><b>{m['h']}</b><p>{m['b']}</p></div>""" for m in P["method"]["rows"])
    srcs = "".join(
        f'<tr><td class="s-n">{s["n"]}</td><td class="s-d">{s["d"]}</td><td class="s-u">{s["u"]}</td></tr>'
        for s in P["sources"])
    excl = "".join(f'<li><b>{e["n"]}</b>{e["why"]}</li>' for e in P["excluded"])

    return f"""{head("The Lab-Grown Diamond Price List — every shape, every weight — Carat Capital",
                     "Lab-grown diamond prices for 2026: retail asking prices and the published wholesale band side by side, across seven shapes and six weights, with the CVD-against-HPHT split, the wholesale index, resale, sources and method.",
                     "lab-grown-diamond-prices.html")}
{folio("The Price Desk · Lab-grown")}
{navbar()}
{omenu()}

<section class="deskhero"><div class="wrap">
  <div class="dh-no">The Price Desk · Lab-grown · Updated {P['as_of']}</div>
  <h1 class="art-h" style="font-size:clamp(36px,5.2vw,74px);text-transform:uppercase;max-width:17ch">The Lab-Grown Diamond Price List<em style="font-family:var(--disp);font-style:normal;font-weight:400;color:var(--seal);text-transform:none;font-size:.32em;display:block;margin-top:14px;letter-spacing:-.01em">{P['kicker']}</em></h1>
  <p class="dh-dek" style="max-width:82ch">{P['standfirst']}</p>
</div></section>

<section class="lgd burin"><div class="wrap" style="padding-top:30px">
  {band}
</div></section>

<section class="lgd burin"><div class="wrap">
  {lx_head("01", "Weight —", "the line that does not rise", "Figure CC/2026/154")}
  {lx_lede(wt['sub'])}
  <div class="lx-split">
    <figure class="rv">{lx_flat(wt['rows'])}
      <figcaption style="font-family:var(--mono);font-size:9px;letter-spacing:.15em;text-transform:uppercase;color:var(--ink-3);margin-top:12px;border-top:1px solid {PX_SOFT};padding-top:9px">Per carat, by weight · log scale · tinted band = the gap · 4 ct carries no natural mark</figcaption>
    </figure>
    <div class="rv">{wtbl}{lx_src(wt['src'])}
      {lx_note(wt['flat_note'], "Why the line is flat")}
      {lx_note(wt['floor_note'], "The blank row", gilt=True)}
    </div>
  </div>
</div></section>

<section class="lgd burin"><div class="wrap">
  {lx_head("02", "Shape —", "the ranking flips", "Figure CC/2026/155")}
  {lx_lede(sh['inversion'])}
  <div class="lx-split">
    <div class="rv">
      <figure>{lx_swing(sh['rows'])}</figure>
      <div class="lx-chips">{chips}</div>
      <div class="lx-src">Asking price per carat, one carat · StoneAlgo, n={sh['n']}, {sh['date']}</div>
    </div>
    <div class="rv">{stab}
      <div class="lx-src">Percentage against a round of the same weight · vermillion = premium at all three</div>
      {lx_note(sh['unstable'], "Read this before quoting a premium")}
      {lx_note(sh['guides'], "Conflict on the record", gilt=True)}
    </div>
  </div>
</div></section>

<section class="lgd burin"><div class="wrap">
  <div class="lx-duo">
    <div>
      {lx_head("03", "Colour and clarity —", "the ladder nobody publishes")}
      {lx_lede(ld['withheld'])}
      {ldtbl}
      {lx_src(ld['src'])}
      {lx_note(ld['modal'], "What the gap still tells you")}
    </div>
    <div>
      {lx_head("04", "How it was grown —", "CVD against HPHT")}
      {lx_lede(ms['note'])}
      {mstbl}
      {lx_src(ms['src'])}
      {lx_note(ms['melee'], "Below the table", gilt=True)}
    </div>
  </div>
</div></section>

<section class="lgd burin"><div class="wrap">
  <div class="lx-duo">
    <div>
      {lx_head("05", "The counters —", "same stone, four prices", "Fig. CC/2026/156")}
      {lx_lede(dp['note'])}
      <figure class="rv">{lx_range(dp['rows'])}</figure>
      <div class="lx-src">Held constant — {dp['spec']}</div>
      {lx_note(dp['floor'], "The floor is below wholesale")}
      {lx_src(dp['src'])}
    </div>
    <div>
      {lx_head("06", "The wholesale index —", "ninety-six per cent off")}
      {lx_lede(P['index']['note'])}
      {ixtbl}
      {lx_src(P['index']['src'])}
      {lx_note(P['index']['rough'], "Rough turns first", gilt=True)}
    </div>
  </div>
</div></section>

<section class="lgd burin"><div class="wrap">
  <div class="lx-duo">
    <div>
      {lx_head("07", "The divergence —", "2019, 2025, now")}
      {dvtbl}
      {lx_note(ix['note'], "Where the saving went")}
      {lx_src(ix['src'])}
    </div>
    <div>
      {lx_head("08", "Resale —", "the number that started at zero")}
      {rstbl}
      {lx_note(rs['note'], "What a jeweller will pay you")}
      {lx_note(rs['conflict'], "Excluded", gilt=True)}
      {lx_src(rs['src'])}
    </div>
  </div>
</div></section>

<section class="lgd briefing"><div class="wrap">
  {lx_head("09", "What moved the numbers —", "the market behind the table")}
  <div class="lx-tiles">{tiles}</div>
</div></section>

<section class="lgd glossary"><div class="wrap">
  {lx_head("10", "The apparatus —", "method, sources, exclusions")}
  <div class="lx-app rv">
    <div><h3>Method</h3>{meth}</div>
    <div><h3>Sources</h3><table><tbody>{srcs}</tbody></table></div>
    <div><h3>What we left out</h3><ul>{excl}</ul></div>
  </div>
</div></section>

<section class="ctastrip"><div class="wrap"><div class="inner">
  <h2>The other half of the market — <em>natural, every shape and weight.</em></h2>
  <a class="big" href="natural-diamond-prices.html">Open the natural list →</a>
</div></div></section>
{colophon()}
{SCRIPT}"""


# ---------------- THE CARAT INDICES ----------------
IDX = json.loads((CONTENT / "indices.json").read_text()) if (CONTENT / "indices.json").exists() else {}

# index hues chosen for ink-on-paper legibility, echoing the desk hues
IDX_HUE = {"CC20": "#96762E", "CC-M": "#7C5CD6", "CC-C": "#0E7C7B",
           "CC-P": "#2563A8", "CC-W": "#1E7D46"}
SEG_NAME = {"M": "Maison", "C": "Counter", "P": "Pit", "W": "Movement"}


def _idx_chart(lines, W=960, Hh=420, pad_l=46, pad_r=118, pad_t=18, pad_b=30,
               baseline=100.0):
    """A build-time SVG line chart of real [date, value] series.

    lines: list of (label, hue, series, dash) — series is [[iso_date, v], ...].
    Every path is drawn from the data; nothing decorative, nothing seeded."""
    allv = [v for _, _, s, _ in lines for _, v in s]
    lo, hi = min(allv + [baseline]), max(allv + [baseline])
    sp = (hi - lo) * 0.08 or 1
    lo, hi = lo - sp, hi + sp
    days = sorted({d for _, _, s, _ in lines for d, _ in s})
    X = {d: pad_l + (W - pad_l - pad_r) * i / max(1, len(days) - 1)
         for i, d in enumerate(days)}
    Y = lambda v: pad_t + (Hh - pad_t - pad_b) * (hi - v) / (hi - lo)
    out = [f'<svg viewBox="0 0 {W} {Hh}" width="100%" role="img" '
           f'aria-label="The Carat indices, rebased to 100 at the start of the year" '
           f'style="display:block;font-family:var(--mono)">']
    # horizontal grid at round steps
    step = max(5, round((hi - lo) / 5 / 5) * 5)
    g = (int(lo) // step) * step + step
    while g < hi:
        y = Y(g)
        em = abs(g - baseline) < 1e-9
        out.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{W-pad_r}" y2="{y:.1f}" '
                   f'stroke="{"#3B362C" if em else "#3B362C22"}" stroke-width="{1.2 if em else 1}"/>')
        out.append(f'<text x="{pad_l-8}" y="{y+3:.1f}" text-anchor="end" font-size="10" '
                   f'fill="#3B362C88">{g}</text>')
        g += step
    # month ticks
    seen = set()
    for d in days:
        mo = d[:7]
        if mo in seen: continue
        seen.add(mo)
        if d == days[0]: continue
        x = X[d]
        out.append(f'<line x1="{x:.1f}" y1="{pad_t}" x2="{x:.1f}" y2="{Hh-pad_b}" stroke="#3B362C14"/>')
        lab = datetime.date.fromisoformat(d).strftime("%b").upper()
        out.append(f'<text x="{x:.1f}" y="{Hh-10}" text-anchor="middle" font-size="9" '
                   f'letter-spacing="1" fill="#3B362C88">{lab}</text>')
    # the lines
    ends = []
    for lab, hue, s, dash in lines:
        pts = " ".join(f"{X[d]:.1f},{Y(v):.1f}" for d, v in s)
        da = ' stroke-dasharray="5 4"' if dash else ""
        out.append(f'<polyline points="{pts}" fill="none" stroke="{hue}" '
                   f'stroke-width="{1.6 if dash else 2.2}"{da} stroke-linejoin="round"/>')
        d_end, v_end = s[-1]
        ends.append((Y(v_end), lab, hue, v_end, X[d_end]))
    # end labels, nudged apart so they never overlap
    ends.sort()
    prev = -1e9
    for y, lab, hue, v, x in ends:
        y = max(y, prev + 13)
        prev = y
        out.append(f'<circle cx="{x:.1f}" cy="{Y(v):.1f}" r="3" fill="{hue}"/>')
        out.append(f'<text x="{x+8:.1f}" y="{y+3:.1f}" font-size="10.5" font-weight="600" '
                   f'fill="{hue}">{lab} {v:,.1f}</text>')
    out.append("</svg>")
    return "".join(out)


def _spread_chart(a, b, W=960, Hh=230, pad_l=46, pad_r=20, pad_t=14, pad_b=28):
    """Area of (a − b) around zero — who is winning, by how much, since January."""
    A, B = dict(a), dict(b)
    days = [d for d in sorted(A) if d in B]
    sp = [(d, A[d] - B[d]) for d in days]
    vals = [v for _, v in sp]
    lo, hi = min(vals + [0]), max(vals + [0])
    m = (hi - lo) * 0.1 or 1
    lo, hi = lo - m, hi + m
    X = {d: pad_l + (W - pad_l - pad_r) * i / max(1, len(days) - 1) for i, d in enumerate(days)}
    Y = lambda v: pad_t + (Hh - pad_t - pad_b) * (hi - v) / (hi - lo)
    z = Y(0)
    pts = " ".join(f"{X[d]:.1f},{Y(v):.1f}" for d, v in sp)
    area = f"{pad_l},{z:.1f} " + pts + f" {X[days[-1]]:.1f},{z:.1f}"
    out = [f'<svg viewBox="0 0 {W} {Hh}" width="100%" role="img" aria-label="Spread" '
           f'style="display:block;font-family:var(--mono)">',
           f'<line x1="{pad_l}" y1="{z:.1f}" x2="{W-pad_r}" y2="{z:.1f}" stroke="#3B362C" stroke-width="1.2"/>',
           f'<polygon points="{area}" fill="#96762E1E"/>',
           f'<polyline points="{pts}" fill="none" stroke="#96762E" stroke-width="2"/>']
    for gv in (lo + (hi - lo) * .25, hi - (hi - lo) * .25):
        out.append(f'<text x="{pad_l-8}" y="{Y(gv)+3:.1f}" text-anchor="end" font-size="10" '
                   f'fill="#3B362C88">{gv:+.0f}</text>')
    d_end, v_end = sp[-1]
    out.append(f'<circle cx="{X[d_end]:.1f}" cy="{Y(v_end):.1f}" r="3" fill="#96762E"/>')
    out.append(f'<text x="{X[d_end]-8:.1f}" y="{Y(v_end)-8:.1f}" text-anchor="end" font-size="11" '
               f'font-weight="600" fill="#96762E">{v_end:+.1f} pts</text>')
    out.append("</svg>")
    return "".join(out)


def indices_page():
    if not IDX:
        return f"""{head("The Carat Indices — Carat Capital",
        "Five indices of the listed jewelry world, computed daily by Carat Capital.", "indices.html")}
{navbar()}{omenu()}
<section class="deskhero"><div class="wrap">
  <div class="dh-no">The Index Desk</div>
  <h1 class="art-h" style="text-transform:uppercase">The Carat Indices</h1>
  <p class="dh-dek">The index desk has not filed today. The indices print with the next edition.</p>
</div></section>{colophon()}{SCRIPT}"""

    ix = IDX["indices"]
    hue = IDX_HUE
    ser = {k: v["series"] for k, v in ix.items()}
    hero = _idx_chart(
        [(k, hue[k], ser[k], False) for k in ("CC20", "CC-M", "CC-C", "CC-P", "CC-W")] +
        [("GOLD", "#B8860B", IDX["gold"]["series"], True)])
    chain = _spread_chart(ser["CC-C"], ser["CC-P"])
    maison = _spread_chart(ser["CC-M"], ser["CC-C"])

    pill = lambda v: (f'<span style="color:#1E7D46">▲ {v:+.2f}%</span>' if v > 0 else
                      (f'<span style="color:#A33B25">▼ {v:+.2f}%</span>' if v < 0 else
                       f'<span style="color:var(--ink-3)">— {v:+.2f}%</span>'))

    # ── the five index cards ──
    cards = []
    cons_by = {c["sym"]: c for c in IDX["constituents"]}
    for code in ("CC20", "CC-M", "CC-C", "CC-P", "CC-W"):
        x = ix[code]
        mem = [cons_by[m] for m in x["members"] if m in cons_by]
        best = max(mem, key=lambda c: c["ytdp"])
        worst = min(mem, key=lambda c: c["ytdp"])
        mini = _idx_chart([(code, hue[code], x["series"], False)],
                          W=430, Hh=150, pad_l=38, pad_r=16, pad_t=10, pad_b=22)
        cards.append(f"""<div class="rv" style="border:1px solid {PX_SOFT};background:var(--paper-2,#fff0);padding:22px 22px 18px">
  <div style="display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap">
    <div><span style="font-family:var(--mono);font-size:10px;letter-spacing:.22em;color:{hue[code]};font-weight:600">{code}</span>
      <span style="font-family:var(--disp);font-weight:700;font-size:21px;letter-spacing:-.02em;margin-left:9px">{x['name']}</span></div>
    <div style="font-family:var(--mono);font-size:22px;font-weight:500;letter-spacing:-.02em">{x['level']:,.2f}</div>
  </div>
  <div style="font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;color:var(--ink-2);margin:7px 0 12px;display:flex;gap:18px;flex-wrap:wrap">
    <span>1D {pill(x['d1p'])}</span><span>1W {pill(x['w1p'])}</span>
    <span>1M {pill(x['m1p'])}</span><span>YTD {pill(x['ytdp'])}</span>
  </div>
  {mini}
  <div style="font-family:var(--mono);font-size:9.5px;letter-spacing:.08em;color:var(--ink-3);margin-top:12px;line-height:1.8">
    {len(mem)} names · {x['dek']}<br>
    best {best['name']} {best['ytdp']:+.1f}% · worst {worst['name']} {worst['ytdp']:+.1f}% ·
    range {x['lo']:,.1f}–{x['hi']:,.1f} · max drawdown {x['mddp']:.1f}%
  </div>
</div>""")

    # ── constituents table ──
    seg_chip = lambda s: (f'<span style="font-family:var(--mono);font-size:8.5px;letter-spacing:.14em;'
                          f'text-transform:uppercase;padding:3px 8px;border:1px solid {PX_SOFT};'
                          f'color:var(--ink-2)">{SEG_NAME[s]}</span>')
    rows = []
    for c in sorted(IDX["constituents"], key=lambda c: -(c["ytdp"] if c["ytdp"] is not None else -999)):
        rows.append(f"""<tr>
  <td style="padding:11px 14px;border-top:1px solid {PX_SOFT}"><b style="font-family:var(--disp);font-weight:600">{c['name']}</b>
    <span style="font-family:var(--mono);font-size:9.5px;color:var(--ink-3);margin-left:8px">{c['sym']}</span></td>
  <td style="padding:11px 14px;border-top:1px solid {PX_SOFT};font-family:var(--mono);font-size:11px;color:var(--ink-2)">{c['ex']}</td>
  <td style="padding:11px 14px;border-top:1px solid {PX_SOFT}">{seg_chip(c['seg'])}</td>
  <td style="padding:11px 14px;border-top:1px solid {PX_SOFT};font-family:var(--mono);font-size:12px;text-align:right">{c['last']:,} {c['cur']}</td>
  <td style="padding:11px 14px;border-top:1px solid {PX_SOFT};font-family:var(--mono);font-size:11.5px;text-align:right">{pill(c['m1p'])}</td>
  <td style="padding:11px 14px;border-top:1px solid {PX_SOFT};font-family:var(--mono);font-size:11.5px;text-align:right">{pill(c['ytdp'])}</td>
  <td style="padding:11px 14px;border-top:1px solid {PX_SOFT};text-align:center;font-family:var(--mono);font-size:11px;color:{'#1E7D46' if c['above50'] else '#A33B25'}">{'●' if c['above50'] else '○'}</td>
</tr>""")

    g = IDX["gold"]
    mg = IDX["metal_gap"]
    cc20 = ix["CC20"]
    mg_line = (f"the makers lead the metal by {abs(mg):.1f} points" if mg < 0 else
               f"the metal leads the makers by {abs(mg):.1f} points")

    tile = lambda v, l, c="var(--ink)": (
        f'<div><b style="display:block;font-family:var(--mono);font-size:clamp(24px,3.6vw,40px);font-weight:500;'
        f'letter-spacing:-.03em;color:{c};line-height:1">{v}</b>'
        f'<span style="display:block;font-family:var(--mono);font-size:9px;letter-spacing:.2em;text-transform:uppercase;'
        f'color:var(--ink-3);margin-top:10px;line-height:1.7">{l}</span></div>')

    return f"""{head("The Carat Indices — the listed jewelry world, marked to market — Carat Capital",
      "Five proprietary indices computed daily from exchange closes: the Jewelry Twenty, the Maisons, the Counter, the Pit and the Movement.",
      "indices.html")}
{navbar()}{omenu()}

<section class="deskhero"><div class="wrap">
  <div class="dh-no">The Index Desk · computed {IDX['as_of']} · base {IDX['base_day']}</div>
  <h1 class="art-h" style="font-size:clamp(38px,5.6vw,80px);text-transform:uppercase;max-width:16ch">The Carat Indices<em style="font-family:var(--disp);font-style:normal;font-weight:400;color:var(--seal);text-transform:none;font-size:.34em;display:block;margin-top:16px;letter-spacing:-.01em">The listed jewelry world, marked to market. Computed by this desk, quoted from no one.</em></h1>
  <p class="dh-dek" style="max-width:78ch">Twenty listed companies across nine exchanges — the maisons, the jewelers' counters, the diamond pits and the watchmakers — folded into five equal-weight indices and rebased to 100 at the first trading day of the year. Every close is an exchange print. Nothing here is estimated, and nothing is anyone else's number.</p>
</div></section>

<section class="burin"><div class="wrap" style="padding-top:34px">
  <div class="rv" style="border-top:3px solid var(--ink);border-bottom:1px solid {PX_SOFT};padding:26px 0 28px;margin-bottom:12px">
    <div style="font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--seal);margin-bottom:20px">The state of the trade — {IDX['as_of']}</div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:30px 26px">
      {tile(f"{cc20['level']:,.1f}", "CC20 · the Jewelry Twenty", "var(--gilt)")}
      {tile(f"{mg:+.1f} pts", f"The metal gap · gold {g['ytdp']:+.1f}% YTD vs CC20 {cc20['ytdp']:+.1f}%", "var(--seal)")}
      {tile(f"{IDX['breadth50']}%", "Breadth · CC20 names above their 50-day mean")}
      {tile(f"{IDX['corr63']:+.2f}", "63-day correlation · CC20 daily moves vs gold", "var(--ink-3)")}
    </div>
    <p style="font-family:var(--text);font-size:15.5px;line-height:1.64;color:var(--ink-2);max-width:74ch;margin:26px 0 0">
      Gold is having a historic year and the old rule says jewelry equities should suffer for it —
      the metal is their input cost. The tape says otherwise: {mg_line}. The divergence is not the
      houses; it is the watchmakers, and the table below names them.</p>
  </div>
</div></section>

<section class="burin"><div class="wrap">
  <h2 class="rv" style="font-family:var(--disp);font-weight:700;font-size:clamp(24px,3vw,34px);letter-spacing:-.02em;margin:26px 0 6px">Five lines, one trade</h2>
  <p class="rv" style="font-family:var(--text);font-size:14.5px;color:var(--ink-2);max-width:72ch;margin:0 0 20px">Every index rebased to 100 at {IDX['base_day']}. Gold, dashed, on the same footing — {g['label']}.</p>
  <div class="rv" style="border:1px solid {PX_SOFT};padding:18px 14px 8px;overflow-x:auto">{hero}</div>
</div></section>

<section class="burin"><div class="wrap">
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(430px,100%),1fr));gap:18px;margin-top:26px">
    {''.join(cards)}
  </div>
</div></section>

<section class="burin"><div class="wrap">
  <h2 class="rv" style="font-family:var(--disp);font-weight:700;font-size:clamp(24px,3vw,34px);letter-spacing:-.02em;margin:40px 0 6px">The spreads</h2>
  <p class="rv" style="font-family:var(--text);font-size:14.5px;color:var(--ink-2);max-width:74ch;margin:0 0 20px">Two numbers this desk watches that nobody else prints: who in the chain is capturing the year, and what the market pays for a name over a counter.</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(440px,100%),1fr));gap:18px">
    <div class="rv" style="border:1px solid {PX_SOFT};padding:18px">
      <div style="font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--gilt);margin-bottom:6px">The chain spread · Counter − Pit</div>
      <p style="font-family:var(--text);font-size:13.5px;color:var(--ink-2);margin:0 0 12px;line-height:1.6">Above zero, the shops are beating the mines for the year; below it, the rough end of the chain is winning.</p>
      {chain}
    </div>
    <div class="rv" style="border:1px solid {PX_SOFT};padding:18px">
      <div style="font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--gilt);margin-bottom:6px">The maison premium · Maisons − Counter</div>
      <p style="font-family:var(--text);font-size:13.5px;color:var(--ink-2);margin:0 0 12px;line-height:1.6">What the market pays for a house over a counter. Negative all year: luxury's crown has slipped to the trade.</p>
      {maison}
    </div>
  </div>
</div></section>

<section class="burin"><div class="wrap">
  <h2 class="rv" style="font-family:var(--disp);font-weight:700;font-size:clamp(24px,3vw,34px);letter-spacing:-.02em;margin:40px 0 6px">The twenty</h2>
  <p class="rv" style="font-family:var(--text);font-size:14.5px;color:var(--ink-2);max-width:74ch;margin:0 0 18px">Sorted by the year. Prices in each stock's home currency; the dot is its own 50-day mean, held or lost.</p>
  <div class="rv" style="border:1px solid {PX_SOFT};overflow-x:auto">
  <table style="width:100%;border-collapse:collapse;min-width:720px">
    <thead><tr style="font-family:var(--mono);font-size:8.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-3);text-align:left">
      <th style="padding:12px 14px">Company</th><th style="padding:12px 14px">Market</th>
      <th style="padding:12px 14px">Book</th><th style="padding:12px 14px;text-align:right">Last close</th>
      <th style="padding:12px 14px;text-align:right">1M</th><th style="padding:12px 14px;text-align:right">YTD</th>
      <th style="padding:12px 14px;text-align:center">50D</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table></div>
</div></section>

<section class="burin"><div class="wrap">
  <div class="rv" style="border-top:1px solid {PX_SOFT};margin-top:44px;padding:26px 0 10px;max-width:78ch">
    <div style="font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--seal);margin-bottom:14px">Methodology — read before quoting</div>
    <p style="font-family:var(--text);font-size:14px;line-height:1.7;color:var(--ink-2)">
      Each constituent is measured in its home currency and rebased to 100 at its last close on or
      before {IDX['base_day']}; an index is the equal-weight mean of those relatives, so no exchange
      rate and no giant market cap can speak for the group. Constituents were chosen for listed,
      liquid exposure to jewelry, diamonds or watches; conglomerates carry their whole business
      (Anglo American is in for De Beers, and carries the rest of Anglo with it). The Pit holds
      only three names because that is how many investable diamond miners remain — that fact is
      itself a finding of this desk. Closes are exchange prints retrieved from Yahoo Finance's
      public chart interface at computation time and spot-checked against independent sources;
      gold is {g['label']}. Exchanges close at different hours, so the latest session differs by
      market; each series carries its own last print. The indices are computed with each edition,
      not live. They are editorial instruments of Carat Capital, not investment advice and not a
      tradeable benchmark — quote them with attribution: “Carat Capital indices, {IDX['as_of']}.”</p>
    <p style="font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;color:var(--ink-3);margin-top:14px">
      {IDX['base_note']} · computed {IDX['built'][:16].replace('T',' ')} · CC20 twenty names ·
      Maisons five · Counter eight · Pit three · Movement seven</p>
  </div>
</div></section>

<section class="ctastrip"><div class="wrap"><div class="inner">
  <h2>The stones themselves are priced too — <em>every shape, every weight.</em></h2>
  <a class="big" href="natural-diamond-prices.html">Open the price lists →</a>
</div></div></section>
{colophon()}
{SCRIPT}"""


# ---------------- THE FOLIO — the week, bound ----------------
def _folio_issue():
    """Compose this week's leaves from the real archive. Returns (meta, pages) —
    each page is a full HTML string designed for a 5:7 leaf."""
    import datetime as _dt
    today = max((a.get("date", "") for a in ARTICLES), default="")
    t = _dt.date.fromisoformat(today)
    wk_start = t - _dt.timedelta(days=6)
    week = [a for a in ARTICLES if a.get("date", "") >= wk_start.isoformat()]
    lead = next((a for a in week if a.get("lead")), week[0] if week else None)
    rng = f"{wk_start.day} {wk_start.strftime('%b')} – {t.day} {t.strftime('%b %Y')}"
    issue_no = "I"
    edition = WIRE.get("edition", "")

    def ph_of(a):
        s = a["slug"] if a["slug"] in PH else DESK_HERO.get(a.get("desk", ""), "")
        return (s, PH.get(s, {}).get("credit", "")) if s in PH else ("", "")

    def folio(n, head_r):
        return (f'<div class="folio"><span>{head_r}</span><span>{n:02d}</span></div>')

    def plate(img, credit, h="46%"):
        if not img: return ""
        cr = f'<span class="pcr">{credit}</span>' if credit else ""
        return (f'<div class="plate" style="height:{h}">'
                f'<img src="assets/ph/{img}.jpg" alt="" loading="lazy">{cr}</div>')

    P = []

    # 00 · cover — the plate runs the full leaf, the masthead prints over it
    ci, ccr = ph_of(lead) if lead else ("", "")
    others = [a for a in week if a is not lead][:2]
    covlines = "".join(f'<div class="cvl"><i></i>{H.escape(a["title"])}</div>' for a in others)
    P.append(f"""<div class="pg pg-cover">
  <div class="cov-bleed">{f'<img src="assets/ph/{ci}.jpg" alt="">' if ci else ''}</div>
  <div class="cov-scrim"></div>
  <div class="cov-in">
    <div class="cov-top"><svg viewBox="0 0 100 100" class="cmedal"><use href="#medal"/></svg>
      <div class="cbrand">Carat<span>^</span>Capital</div>
      <div class="cov-iss">Issue {issue_no}</div></div>
    <div class="cov-mast">The<br>Folio</div>
    <div class="cov-sub">{rng} &middot; the week, bound</div>
    <div class="cov-line">{H.escape(lead['title']) if lead else ''}</div>
    {covlines}
    <div class="cov-foot">The trade paper of the jewelry world &middot; caratcapital.org{f' &middot; plate: {ccr}' if ccr else ''}</div>
  </div>
</div>""")

    # 01 · masthead + contents
    desks_live = [(d, [a for a in week if a.get("desk") == d["slug"]]) for d in DESKS]
    toc = "".join(
        f'<div class="toc"><span class="tn">{7+i:02d}</span><b>{d["title"]}</b>'
        f'<i></i><em>{(str(len(arts)) + " filed") if arts else "dark this week"}</em></div>'
        for i, (d, arts) in enumerate(desks_live))
    P.append(f"""<div class="pg">
  <div class="mk">The Folio &middot; Issue {issue_no}</div>
  <h2 class="ph2">In this issue</h2>
  <div class="toc"><span class="tn">03</span><b>The week's lead</b><i></i><em>{H.escape((lead or {}).get('kicker',''))[:34]}</em></div>
  <div class="toc"><span class="tn">05</span><b>The tape</b><i></i><em>the Carat indices</em></div>
  {toc}
  <div class="toc"><span class="tn">13</span><b>The wire, distilled</b><i></i><em>the week in one page</em></div>
  <div class="toc"><span class="tn">14</span><b>By the numbers</b><i></i><em>the week's marks</em></div>
  <div class="mast-note">Bound weekly from the daily editions of Carat Capital.
    Every claim in these pages was priced, sourced, or cut before it ran.
    {edition and 'This issue closes with ' + H.escape(edition) + '.'}</div>
  {folio(1, 'The Folio')}
</div>""")

    # 02 · house plate — the Morning Brief
    P.append(f"""<div class="pg pg-ad">
  <div class="adk">A word from the house</div>
  <div class="adbig">Six desks read the trade press in nine languages<br>
    <em>so you can read one page.</em></div>
  <div class="adcta">The Morning Brief &middot; free &middot;
    <a href="/#brief">sign on at caratcapital.org</a></div>
  <div class="adfoot">No hype words &middot; no exclamation marks &middot; unsubscribe in one click</div>
  {folio(2, 'The house')}
</div>""")

    # 03-04 · the lead spread: plate at full bleed, story facing it
    li, lcr = ph_of(lead) if lead else ("", "")
    P.append(f"""<div class="pg pg-plate">{plate(li, lcr, "100%")}</div>""")
    body0 = ((lead or {}).get('body') or [''])[0]
    pull = (lead or {}).get('dek', '')
    P.append(f"""<div class="pg">
  <div class="mk">{H.escape((lead or {}).get('kicker', 'The lead'))}</div>
  <h2 class="ph1">{H.escape((lead or {}).get('title', ''))}</h2>
  <div class="pull">{H.escape(pull[:160])}</div>
  <p class="pbody drop">{H.escape(body0[:520])}&hellip;</p>
  <div class="pby">{H.escape((lead or {}).get('byline', 'The desk'))} &middot; {(lead or {}).get('minutes', 5)} min &middot;
    <a href="a-{(lead or {}).get('slug', '')}.html">read the story in full &rarr;</a></div>
  {folio(4, 'The lead')}
</div>""")

    # 05-06 · the tape spread
    if IDX:
        chart = _idx_chart(
            [(k, IDX_HUE[k], IDX["indices"][k]["series"], False) for k in
             ("CC20", "CC-M", "CC-C", "CC-P", "CC-W")],
            W=560, Hh=560, pad_l=40, pad_r=86, pad_t=14, pad_b=26)
        P.append(f"""<div class="pg">
  <div class="mk">The tape</div>
  <h2 class="ph2">The Carat indices</h2>
  <p class="pdek" style="margin-bottom:12px">Five indices this paper computes itself —
    the listed jewelry world rebased to 100 at the year's first trading day.</p>
  <div style="border:1px solid var(--pline);padding:8px 4px">{chart}</div>
  {folio(5, 'The tape')}
</div>""")
        rows = "".join(
            f'<div class="ixr"><span class="c" style="color:{IDX_HUE[k]}">{k}</span>'
            f'<b>{IDX["indices"][k]["name"]}</b>'
            f'<span class="v">{IDX["indices"][k]["level"]:,.1f}</span>'
            f'<span class="y {"up" if IDX["indices"][k]["ytdp"]>0 else "dn"}">{IDX["indices"][k]["ytdp"]:+.1f}%</span></div>'
            for k in ("CC20", "CC-M", "CC-C", "CC-P", "CC-W"))
        cons = sorted(IDX["constituents"], key=lambda c: -(c["ytdp"] or -999))
        hi, lo = cons[0], cons[-1]
        P.append(f"""<div class="pg">
  <div class="mk">Marked to market &middot; {IDX['as_of']}</div>
  <h2 class="ph2">The year so far</h2>
  {rows}
  <div class="bignum"><b>{IDX['metal_gap']:+.1f} pts</b><span>the metal gap — gold against the makers, YTD</span></div>
  <div class="pnote">Best name of the year: {H.escape(hi['name'])} {hi['ytdp']:+.1f}%.
    Hardest fall: {H.escape(lo['name'])} {lo['ytdp']:+.1f}%. Breadth: {IDX['breadth50']}% of the
    Twenty above their 50-day mean. Full charts, spreads and method at
    <a href="indices.html">the Index Desk</a>.</div>
  {folio(6, 'The tape')}
</div>""")

    # 07-12 · six desk leaves
    for i, (d, arts) in enumerate(desks_live):
        img = DESK_HERO.get(d["slug"], "")
        cr = PH.get(img, {}).get("credit", "") if img in PH else ""
        if arts:
            top = arts[:3]
            items = "".join(
                f'<div class="dst"><h3><a href="a-{a["slug"]}.html">{H.escape(a["title"])}</a></h3>'
                f'<p>{H.escape((a.get("dek") or "")[:150])}</p></div>' for a in top)
            body = items + (f'<div class="pnote">{len(arts)} stories filed this week &middot; '
                            f'<a href="{d["slug"]}.html">open the desk &rarr;</a></div>')
        else:
            body = ('<div class="dark-desk">The desk filed nothing this week. Its sources '
                    'went quiet, and this paper does not fill quiet weeks — '
                    'the next print carries the desk&rsquo;s return.</div>')
        P.append(f"""<div class="pg">
  <div class="mk">D&mdash;{d['no']} &middot; {H.escape(d['tag'])}</div>
  <h2 class="ph2">{H.escape(d['title'])}</h2>
  {plate(img, cr, "24%")}
  {body}
  {folio(7+i, d['title'])}
</div>""")

    # 13 · the wire, distilled
    wire_items = [a for a in week if a is not lead][:8]
    wl = "".join(
        f'<div class="wl"><span class="wk">{H.escape((a.get("kicker") or DESK_NAMES.get(a.get("desk"),"Desk"))[:26])}</span>'
        f'<a href="a-{a["slug"]}.html">{H.escape(a["title"])}</a></div>' for a in wire_items)
    P.append(f"""<div class="pg">
  <div class="mk">The wire, distilled</div>
  <h2 class="ph2">The week in one page</h2>
  {wl}
  {folio(13, 'The wire')}
</div>""")

    # 14 · by the numbers
    nums = []
    for d in DESKS:
        st = (d.get("stats") or [])
        if st: nums.append((st[0][0], f"{d['title']} — {st[0][1]}"))
    nums = "".join(f'<div class="bn"><b>{H.escape(v)}</b><span>{H.escape(k)}</span></div>'
                   for v, k in nums[:6])
    P.append(f"""<div class="pg">
  <div class="mk">The week's marks</div>
  <h2 class="ph2">By the numbers</h2>
  <div class="bngrid">{nums}</div>
  <div class="pnote">Each figure carries its desk's sourcing on the site — nothing here
    is estimated, and what could not be verified was carried &ldquo;unch.&rdquo;</div>
  {folio(14, 'The marks')}
</div>""")

    # 15 · a full-bleed plate to breathe
    pimg = "gemstones-hero" if "gemstones-hero" in PH else next(iter(PH), "")
    pcr = PH.get(pimg, {}).get("credit", "")
    P.append(f"""<div class="pg pg-plate">{plate(pimg, pcr, "100%")}
  <div class="plate-cap">Plate II &middot; the colour the week went without</div>
</div>""")

    # 16 · the open seat
    P.append(f"""<div class="pg pg-ad">
  <div class="adk">The open seat</div>
  <div class="adbig">Your maison,<br>on this page.</div>
  <div class="adcta" style="max-width:30ch">The Folio binds the week for the people who
    price it. One plate an issue is kept for a house the desk would stand behind.</div>
  <div class="adfoot"><a href="about.html#contact">Write to the desk &rarr;</a></div>
  {folio(16, 'The open seat')}
</div>""")

    # 17 · back cover
    P.append(f"""<div class="pg pg-cover pg-back">
  <div class="cov-scrim" style="background:linear-gradient(165deg,#191612,#0E0C09)"></div>
  <div class="cov-in" style="text-align:center;justify-content:center">
  <svg viewBox="0 0 100 100" class="cmedal big"><use href="#medal"/></svg>
  <div class="cov-mast" style="font-size:34px">Clarity, daily.</div>
  <div class="cov-foot" style="margin-top:22px">Carat Capital &middot; est. MMXXVI &middot; free to read &middot; caratcapital.org</div>
  </div>
</div>""")

    return dict(no=issue_no, rng=rng, pages=len(P)), P


def magazine_page():
    meta, pages = _folio_issue()
    leaves = "".join(f'<div class="pg-slot">{p}</div>' for p in pages)
    npages = len(pages)
    # the table of contents drawer: section → sheet index (page n lives on sheet ceil(n/2))
    toc_items = [("Cover", 0), ("In this issue", 1), ("The week's lead", 2),
                 ("The tape — the Carat indices", 3)] + \
                [(d["title"], (7 + k + 1) // 2) for k, d in enumerate(DESKS)] + \
                [("The wire, distilled", 7), ("By the numbers", 7),
                 ("The open seat", 8), ("Back cover", 9)]
    toc_html = "".join(f'<button data-s="{sh}">{H.escape(t)}</button>' for t, sh in toc_items)
    return f"""{head("The Folio — the week, bound — Carat Capital",
      "Carat Capital's weekly digital magazine: the week's editions bound into a page-turning issue.",
      "magazine.html")}
<style>
:root{{--pink:#16130E;--pink2:#3B362C;--pink3:#8A8272;--pgilt:#96762E;--pseal:#BE3319;
  --paper:#F6F1E6;--paper2:#EFE8D8;--pline:rgba(59,54,44,.22);
  --pd:'Instrument Sans',sans-serif;--pt:'Lora',Georgia,serif;--pm:'IBM Plex Mono',monospace}}
html,body{{background:#100E0B;overflow-x:clip;overscroll-behavior:none}}
body{{margin:0;color:var(--pink);font-family:var(--pt);
  background:
    radial-gradient(120% 90% at 50% -20%,rgba(198,162,74,.10),transparent 55%),
    radial-gradient(90% 70% at 50% 118%,rgba(120,86,30,.12),transparent 60%),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3CfeColorMatrix values='0 0 0 0 0.07 0 0 0 0 0.06 0 0 0 0 0.045 0 0 0 .5 0'/%3E%3C/filter%3E%3Crect width='240' height='240' filter='url(%23n)'/%3E%3C/svg%3E"),
    linear-gradient(180deg,#14110D,#0C0A07);
  min-height:100dvh}}
body::after{{content:"";position:fixed;inset:0;pointer-events:none;z-index:1;
  background:radial-gradient(130% 100% at 50% 45%,transparent 55%,rgba(0,0,0,.5) 100%)}}
.stage,.mgbar,.mgnav,.drawer{{position:relative;z-index:2}}
.mgbar,.mgnav{{position:fixed}}
.mgbar{{position:fixed;left:0;right:0;top:0;z-index:40;display:flex;justify-content:space-between;
  align-items:center;gap:14px;padding:calc(env(safe-area-inset-top,0px) + 12px) 18px 12px;
  font-family:var(--pm);font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:#B9AE96;
  background:linear-gradient(180deg,#141310 60%,transparent)}}
.mgbar a{{color:#B9AE96;text-decoration:none}}
.mgbar a:hover{{color:#F6F1E6}}
.mgbar .t{{color:#E8CB7C;letter-spacing:.3em}}
.stage{{min-height:100dvh;display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:calc(env(safe-area-inset-top,0px) + 56px) 16px 100px;overflow:hidden}}
#bookwrap{{position:relative;transition:transform .85s cubic-bezier(.16,.9,.24,1)}}
#zoomer{{transition:transform .55s cubic-bezier(.16,.9,.24,1);transform-origin:center center}}
body.zoomed #zoomer{{cursor:grab}}
body.zoomed.panning #zoomer{{cursor:grabbing;transition:none}}
#book{{position:relative;touch-action:none;-webkit-user-select:none;user-select:none;
  -webkit-touch-callout:none;cursor:grab}}
/* the book lies on the desk: one wide soft shadow, one tight contact line */
#book::before{{content:"";position:absolute;left:2%;right:2%;bottom:-4.5%;height:9%;z-index:0;
  background:radial-gradient(50% 100% at 50% 0%,rgba(0,0,0,.65),transparent 75%);
  filter:blur(6px)}}
/* the block of pages at the fore-edges */
.edge{{position:absolute;top:1.2%;height:97.6%;width:0;z-index:0;
  background:repeating-linear-gradient(90deg,#E9E2D2 0 1px,#CFC5AC 1px 2px);
  transition:width .5s}}
.edge.l{{right:100%;border-radius:2px 0 0 2px}}
.edge.r{{left:100%;border-radius:0 2px 2px 0}}
/* the two lying pages */
.lp{{position:absolute;top:0;bottom:0;width:50%;overflow:hidden;background:var(--paper);z-index:2}}
#pgL{{left:0}} #pgR{{left:50%}}
#pgL{{border-radius:3px 0 0 3px;box-shadow:0 2px 10px rgba(0,0,0,.35)}}
#pgR{{border-radius:0 3px 3px 0;box-shadow:0 2px 10px rgba(0,0,0,.35)}}
#pgL::after{{content:"";position:absolute;inset:0;z-index:6;pointer-events:none;
  background:linear-gradient(-90deg,rgba(30,24,14,.34) 0%,rgba(30,24,14,.10) 3.5%,transparent 9%),
             linear-gradient(-90deg,transparent 88%,rgba(255,252,244,.16) 96%,transparent 100%)}}
#pgR::after{{content:"";position:absolute;inset:0;z-index:6;pointer-events:none;
  background:linear-gradient(90deg,rgba(30,24,14,.34) 0%,rgba(30,24,14,.10) 3.5%,transparent 9%),
             linear-gradient(90deg,transparent 88%,rgba(255,252,244,.16) 96%,transparent 100%)}}
/* the fold machinery: the page being peeled + what it reveals */
#under{{position:absolute;top:0;bottom:0;width:50%;overflow:hidden;background:var(--paper);
  display:none;z-index:1}}
#peelC{{position:absolute;top:0;bottom:0;overflow:hidden;display:none;z-index:10}}
#peel{{position:absolute;top:0;bottom:0;width:0;overflow:hidden;background:var(--paper);
  box-shadow:0 0 34px rgba(10,8,4,.42)}}
#peel .inner{{position:absolute;top:0;bottom:0}}
#peel .curl{{position:absolute;inset:0;pointer-events:none}}
#foldsh{{position:absolute;top:0;bottom:0;width:70px;display:none;z-index:9;pointer-events:none}}
#cornhint{{position:absolute;right:0;bottom:0;width:46px;height:46px;z-index:12;pointer-events:none;
  background:linear-gradient(315deg,rgba(59,54,44,.20) 6%,rgba(255,252,244,.4) 12%,transparent 46%);
  opacity:0;transition:opacity .4s;border-radius:0 0 2px 0}}
#book:hover #cornhint{{opacity:1;animation:breathe 2.6s ease-in-out infinite}}
@keyframes breathe{{50%{{transform:scale(1.22);opacity:.75}}}}
/* leaves */
/* container units: type scales with the page like ink, not like a website */
.lp,#under,#peel .inner,.pg-slot,.th{{container-type:size}}
.pg{{position:absolute;inset:0;padding:7.2% 8%;display:flex;flex-direction:column;
  font-size:3.4cqw;line-height:1.55}}
.pg-slot{{display:contents}}
.mk{{font-family:var(--pm);font-size:2.05cqw;letter-spacing:.26em;text-transform:uppercase;
  color:var(--pgilt);margin-bottom:10px}}
.ph1{{font-family:var(--pd);font-weight:700;font-size:6.1cqw;line-height:1.1;letter-spacing:-.02em;margin:0 0 10px}}
.ph2{{font-family:var(--pd);font-weight:700;font-size:5.5cqw;line-height:1.1;letter-spacing:-.02em;margin:0 0 12px}}
.pdek{{font-size:3.5cqw;color:var(--pink2);margin:0 0 10px}}
.pull{{font-family:var(--pt);font-style:italic;font-size:3.9cqw;line-height:1.5;color:var(--pink2);
  border-left:2px solid var(--pgilt);padding:2px 0 2px 12px;margin:0 0 12px}}
.pbody{{font-size:3.25cqw;color:var(--pink2);margin:0;text-align:justify;hyphens:auto;-webkit-hyphens:auto}}
.pbody.drop::first-letter{{font-family:var(--pd);font-weight:700;font-size:10.4cqw;line-height:.82;
  float:left;padding:4px 7px 0 0;color:var(--pink)}}
.pby{{font-family:var(--pm);font-size:2.2cqw;letter-spacing:.14em;text-transform:uppercase;
  color:var(--pink3);margin-top:auto;padding-top:12px}}
.pby a,.pnote a{{color:var(--pseal);text-decoration:none}}
.plate{{position:relative;margin:0 0 12px;overflow:hidden;background:var(--paper2)}}
.plate img{{width:100%;height:100%;object-fit:cover;display:block;filter:saturate(.8)}}
.pcr{{position:absolute;right:1.5cqw;bottom:1.2cqw;font-family:var(--pm);font-size:1.45cqw;
  letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.75);
  text-shadow:0 1px 3px rgba(0,0,0,.6)}}
.pg-plate{{padding:0}}
.pg-plate .plate{{margin:0;height:100%!important}}
.plate-cap{{position:absolute;left:8%;bottom:6%;z-index:3;font-family:var(--pm);font-size:1.8cqw;
  letter-spacing:.24em;text-transform:uppercase;color:rgba(255,252,240,.85);
  text-shadow:0 1px 6px rgba(0,0,0,.7)}}
.folio{{margin-top:auto;padding-top:2.6cqw;display:flex;justify-content:space-between;
  font-family:var(--pm);font-size:1.95cqw;letter-spacing:.22em;text-transform:uppercase;color:var(--pink3)}}
.toc{{display:flex;align-items:baseline;gap:9px;padding:7px 0;border-bottom:1px solid var(--pline)}}
.toc .tn{{font-family:var(--pm);font-size:2.2cqw;color:var(--pgilt)}}
.toc b{{font-family:var(--pd);font-weight:600;font-size:3.25cqw}}
.toc i{{flex:1;border-bottom:1px dotted var(--pline)}}
.toc em{{font-style:normal;font-family:var(--pm);font-size:1.8cqw;letter-spacing:.1em;
  text-transform:uppercase;color:var(--pink3)}}
.mast-note{{margin-top:3.6cqw;font-size:2.7cqw;color:var(--pink3);line-height:1.6}}
.ixr{{display:flex;align-items:baseline;gap:9px;padding:8px 0;border-bottom:1px solid var(--pline);
  font-family:var(--pm)}}
.ixr .c{{font-size:2.2cqw;letter-spacing:.16em}}
.ixr b{{font-family:var(--pd);font-size:3.4cqw;flex:1}}
.ixr .v{{font-size:3.1cqw}}
.ixr .y{{font-size:2.6cqw;width:14.5cqw;text-align:right}}
.ixr .up{{color:#1E7D46}}.ixr .dn{{color:#A33B25}}
.bignum{{margin:16px 0 10px}}
.bignum b{{display:block;font-family:var(--pm);font-size:7.8cqw;font-weight:500;letter-spacing:-.02em;color:var(--pseal)}}
.bignum span{{font-family:var(--pm);font-size:1.95cqw;letter-spacing:.2em;text-transform:uppercase;color:var(--pink3)}}
.pnote{{font-size:2.85cqw;color:var(--pink3);line-height:1.6;margin-top:10px}}
.dst{{padding:9px 0;border-bottom:1px solid var(--pline)}}
.dst h3{{font-family:var(--pd);font-weight:700;font-size:3.5cqw;line-height:1.2;margin:0 0 4px}}
.dst h3 a{{color:var(--pink);text-decoration:none}}
.dst p{{font-size:2.85cqw;color:var(--pink2);margin:0}}
.dark-desk{{margin:auto 0;font-size:3.4cqw;color:var(--pink3);font-style:italic;line-height:1.7;
  border-left:2px solid var(--pline);padding-left:14px}}
.wl{{padding:8px 0;border-bottom:1px solid var(--pline)}}
.wl .wk{{display:block;font-family:var(--pm);font-size:1.7cqw;letter-spacing:.2em;
  text-transform:uppercase;color:var(--pgilt);margin-bottom:3px}}
.wl a{{font-family:var(--pd);font-weight:600;font-size:3.25cqw;line-height:1.3;
  color:var(--pink);text-decoration:none;display:block;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis}}
.wl{{padding:1.9cqw 0}}
.bngrid{{display:grid;grid-template-columns:1fr 1fr;gap:14px 12px;margin-top:6px}}
.bn b{{display:block;font-family:var(--pm);font-size:4.7cqw;font-weight:500;letter-spacing:-.02em}}
.bn span{{font-family:var(--pm);font-size:1.7cqw;letter-spacing:.14em;text-transform:uppercase;
  color:var(--pink3);line-height:1.6;display:block;margin-top:3px}}
.pg-cover{{padding:0;color:#F0E8D6}}
.cov-bleed{{position:absolute;inset:0}}
.cov-bleed img{{width:100%;height:100%;object-fit:cover;filter:saturate(.7) brightness(.9)}}
.cov-scrim{{position:absolute;inset:0;background:linear-gradient(178deg,rgba(10,8,5,.72) 0%,rgba(10,8,5,.35) 38%,rgba(10,8,5,.82) 78%,rgba(10,8,5,.94) 100%)}}
.cov-in{{position:relative;z-index:2;display:flex;flex-direction:column;height:100%;padding:7.2% 8%;
  outline:1px solid rgba(198,162,74,.34);outline-offset:-11px}}
.cov-top{{display:flex;align-items:center;gap:9px}}
.cov-top .cov-iss{{margin-left:auto;font-family:var(--pm);font-size:1.8cqw;letter-spacing:.26em;
  text-transform:uppercase;color:#C6A24A}}
.cmedal{{width:6.8cqw;height:6.8cqw;color:#C6A24A;flex:none}}
.cmedal.big{{width:16.6cqw;height:16.6cqw;margin:0 auto 18px}}
.cbrand{{font-family:var(--pd);font-weight:700;font-size:2.7cqw;letter-spacing:.24em;text-transform:uppercase}}
.cbrand span{{color:#BE3319}}
.cov-mast{{font-family:var(--pd);font-weight:700;font-size:16.6cqw;line-height:.92;letter-spacing:-.03em;margin:6.2cqw 0 2cqw}}
.cov-sub{{font-family:var(--pm);font-size:1.95cqw;letter-spacing:.26em;text-transform:uppercase;color:#C6A24A}}
.cov-line{{font-family:var(--pd);font-weight:700;font-size:4.4cqw;line-height:1.25;letter-spacing:-.01em;margin-top:auto}}
.cvl{{display:flex;gap:2cqw;align-items:baseline;font-family:var(--pd);font-weight:600;font-size:2.85cqw;
  line-height:1.35;margin-top:9px;color:rgba(240,232,214,.86)}}
.cvl i{{flex:none;width:14px;border-top:1px solid #6E7278;transform:translateY(-3px)}}
.cov-foot{{margin-top:3.6cqw;font-family:var(--pm);font-size:1.7cqw;letter-spacing:.2em;
  text-transform:uppercase;color:rgba(240,232,214,.55)}}
.pg-ad{{background:var(--paper2);justify-content:center;text-align:center}}
.adk{{font-family:var(--pm);font-size:1.95cqw;letter-spacing:.3em;text-transform:uppercase;color:var(--pgilt);margin-bottom:18px}}
.adbig{{font-family:var(--pd);font-weight:700;font-size:6cqw;line-height:1.2;letter-spacing:-.02em}}
.adbig em{{font-style:italic;font-family:var(--pt);font-weight:400}}
.adcta{{margin:4.7cqw auto 0;font-size:3.25cqw;color:var(--pink2)}}
.adcta a,.adfoot a{{color:var(--pseal);text-decoration:none}}
.adfoot{{margin-top:3.6cqw;font-family:var(--pm);font-size:1.8cqw;letter-spacing:.18em;
  text-transform:uppercase;color:var(--pink3)}}
/* ── the desk under the book ── */
.mgnav{{position:fixed;left:0;right:0;bottom:0;z-index:40;display:flex;flex-direction:column;gap:8px;
  padding:10px 18px calc(env(safe-area-inset-bottom,0px) + 12px);
  background:linear-gradient(0deg,#141310 62%,transparent)}}
.mgrow{{display:flex;justify-content:center;align-items:center;gap:12px;
  font-family:var(--pm);font-size:9px;letter-spacing:.18em;text-transform:uppercase;color:#B9AE96}}
.mgrow.icons{{gap:8px}}
.mgrow.icons button{{width:40px;height:40px;display:grid;place-items:center;color:#CDB878;
  background:rgba(20,17,12,.55);border:1px solid rgba(198,162,74,.3);border-radius:12px;
  cursor:pointer;transition:color .25s,border-color .25s,background .25s}}
.mgrow.icons button svg{{width:19px;height:19px}}
.mgrow.icons button:hover{{color:#F2E3B6;border-color:rgba(198,162,74,.65);background:rgba(198,162,74,.14)}}
.isep{{width:1px;height:22px;background:rgba(198,162,74,.25);margin:0 4px}}
.chev{{position:fixed;top:50%;transform:translateY(-50%);z-index:40;width:52px;height:78px;
  display:grid;place-items:center;color:#CDB878;background:none;border:0;cursor:pointer;
  opacity:.75;transition:opacity .25s,color .25s,transform .2s}}
.chev svg{{width:34px;height:34px;filter:drop-shadow(0 2px 6px rgba(0,0,0,.6))}}
.chev.l{{left:max(8px,calc(50vw - min(1180px,100vw - 36px)/2 - 62px))}}
.chev.r{{right:max(8px,calc(50vw - min(1180px,100vw - 36px)/2 - 62px))}}
.chev:hover{{opacity:1;color:#F2E3B6;transform:translateY(-50%) scale(1.12)}}
.chev[disabled]{{opacity:.14;cursor:default;transform:translateY(-50%)}}
.pgbox{{display:flex;align-items:baseline;gap:6px}}
.pgbox input{{width:58px;text-align:center;font:inherit;color:#E8CB7C;background:rgba(20,17,12,.6);
  border:1px solid rgba(198,162,74,.35);border-radius:8px;padding:5px 4px;letter-spacing:.14em}}
.pgbox em{{font-style:normal;color:#8A8272}}
#scrub{{-webkit-appearance:none;appearance:none;width:min(520px,64vw);height:2px;border-radius:2px;
  background:rgba(198,162,74,.28);outline:none}}
#scrub::-webkit-slider-thumb{{-webkit-appearance:none;width:13px;height:13px;border-radius:50%;
  background:#E8CB7C;border:1px solid #3F3F3F;cursor:pointer}}
#scrub::-moz-range-thumb{{width:13px;height:13px;border-radius:50%;background:#E8CB7C;
  border:1px solid #3F3F3F;cursor:pointer}}
.drawer{{position:fixed;left:0;right:0;bottom:0;z-index:50;transform:translateY(102%);
  transition:transform .5s cubic-bezier(.16,.9,.24,1);background:#0F0E0B;
  border-top:1px solid rgba(198,162,74,.3);padding:14px 16px calc(env(safe-area-inset-bottom,0px) + 14px)}}
.drawer.open{{transform:none}}
#thumbs{{display:flex;gap:10px;overflow-x:auto}}
.th{{flex:none;width:76px;height:106px;position:relative;overflow:hidden;background:var(--paper);
  border:1px solid rgba(198,162,74,.25);cursor:pointer}}
.th:hover{{border-color:#6E7278}}
.th .pg{{transform:scale(.19);transform-origin:top left;width:400px;height:560px;position:absolute}}
.th b{{position:absolute;right:3px;bottom:2px;z-index:9;font-family:var(--pm);font-weight:500;
  font-size:7px;color:#96762E;background:rgba(246,241,230,.85);padding:1px 4px;border-radius:3px}}
#tocp{{display:flex;flex-direction:column;gap:2px;max-height:44vh;overflow-y:auto}}
#tocp button{{font-family:var(--pm);font-size:10px;letter-spacing:.14em;text-transform:uppercase;
  text-align:left;color:#CFC5AC;background:none;border:0;border-bottom:1px solid rgba(198,162,74,.14);
  padding:10px 6px;cursor:pointer}}
#tocp button:hover{{color:#E8CB7C;background:rgba(198,162,74,.07)}}
/* the paper back of a single-mode turning page */
#peel .pback{{position:absolute;inset:0;display:none;background:
  linear-gradient(90deg,#EFE8D8,#F6F1E6 40%,#EFE8D8);}}
#book.single #peel .pback{{display:block}}
@media(prefers-reduced-motion:reduce){{#bookwrap,#zoomer,.edge{{transition:none!important}}}}
html:not(.js) #book{{display:flex;flex-direction:column;gap:16px;width:min(92vw,480px);background:none}}
html:not(.js) .pg-slot{{display:block;position:relative;aspect-ratio:5/7;background:var(--paper)}}
html:not(.js) .lp,html:not(.js) #under,html:not(.js) #peelC,html:not(.js) #foldsh{{display:none}}
</style>
<script>document.documentElement.classList.add('js')</script>

<div class="mgbar">
  <a href="index.html">&larr; The paper</a>
  <span class="t">The Folio &middot; Issue {meta['no']}</span>
  <span class="pgbox"><input id="pgin" inputmode="numeric" aria-label="Go to page" value="1">
    <em id="pgof">/ {npages}</em></span>
</div>

<div class="stage"><div id="bookwrap"><div id="zoomer"><div id="book">{leaves}
  <div class="lp" id="pgL"></div><div class="lp" id="pgR"></div>
  <div id="under"></div>
  <div id="foldsh"></div>
  <div id="peelC"><div id="peel"><div class="inner"></div><div class="pback"></div><div class="curl"></div></div></div>
  <div id="cornhint"></div>
  <div class="edge l"></div><div class="edge r"></div>
</div></div></div></div>

<button class="chev l" id="mprev" aria-label="Previous page"><svg viewBox="0 0 24 24"><path d="M15 4 7 12l8 8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
<button class="chev r" id="mnext" aria-label="Next page"><svg viewBox="0 0 24 24"><path d="m9 4 8 8-8 8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>

<div class="mgnav">
  <div class="mgrow"><input id="scrub" type="range" min="0" max="1" value="0" step="1"
    aria-label="Scrub through the issue"></div>
  <div class="mgrow icons">
    <button id="mtoc" aria-label="Contents" title="Contents"><svg viewBox="0 0 24 24"><path d="M4 6h16M4 12h10M4 18h13" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <button id="mthumbs" aria-label="Pages" title="Pages"><svg viewBox="0 0 24 24"><rect x="3.5" y="5" width="7.5" height="14" rx="1" fill="none" stroke="currentColor" stroke-width="1.4"/><rect x="13.5" y="5" width="7.5" height="14" rx="1" fill="none" stroke="currentColor" stroke-width="1.4"/></svg></button>
    <span class="isep"></span>
    <button id="mzoom" aria-label="Zoom" title="Zoom"><svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="m15.5 15.5 4.5 4.5M8 10.5h5M10.5 8v5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    <button id="mfull" aria-label="Fullscreen" title="Fullscreen"><svg viewBox="0 0 24 24"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
  </div>
</div>
<div id="thumbsD" class="drawer"><div id="thumbs" aria-label="Page thumbnails"></div></div>
<div id="tocD" class="drawer"><div id="tocp" aria-label="Contents">{toc_html}</div></div>

<script>
(function(){{
  const book=document.getElementById('book'), wrap=document.getElementById('bookwrap'),
        zoomer=document.getElementById('zoomer');
  const slots=[...book.querySelectorAll('.pg-slot')];
  const pgL=document.getElementById('pgL'), pgR=document.getElementById('pgR');
  const under=document.getElementById('under'), peelC=document.getElementById('peelC'),
        peel=document.getElementById('peel'), peelIn=peel.querySelector('.inner'),
        curl=peel.querySelector('.curl'), foldsh=document.getElementById('foldsh');
  const pgno=document.getElementById('pgin'), scrub=document.getElementById('scrub');
  const bp=document.getElementById('mprev'), bn=document.getElementById('mnext');
  const isPhone=matchMedia('(max-width:700px)');
  const NP={npages}, NSpread=Math.ceil({npages}/2);
  let mode='', cur=0, BW=0, BH=0, anim=null, NS=NSpread;

  const leaf=i=>slots[i]?slots[i].firstElementChild:null;
  function put(el,i){{ el.innerHTML=''; const l=leaf(i); if(l) el.appendChild(l.cloneNode(true)); }}

  function sizeBook(){{
    const single=mode==='single';
    const vw=Math.min(innerWidth-(single?20:36),1180), vh=innerHeight-(single?150:186);
    let pw=single?Math.min(vw,vh/1.4):Math.min(vw/2,vh/1.4);
    BH=pw*1.4; BW=single?pw:pw*2;
    book.style.width=BW+'px'; book.style.height=BH+'px';
    book.classList.toggle('single',single);
  }}
  function settle(){{
    under.style.display=peelC.style.display=foldsh.style.display='none';
    if(mode==='single'){{
      /* one leaf fills the book, bound at its left edge */
      pgL.style.visibility='hidden';
      pgR.style.left='0'; pgR.style.width='100%';
      put(pgR, cur); pgR.style.visibility='';
      pgR.style.clipPath='';
      wrap.style.transform='';
      document.querySelector('.edge.l').style.width=Math.min(9,cur*0.9)+'px';
      document.querySelector('.edge.r').style.width=Math.min(9,(NP-1-cur)*0.9)+'px';
      pgno.value=cur===0?'cover':(cur===NP-1?'back':cur+1);
      bp.disabled=cur===0; bn.disabled=cur===NP-1;
      scrub.max=NP-1; scrub.value=cur;
      if(history.replaceState) history.replaceState(null,'','#p'+cur);
      return;
    }}
    pgR.style.left='50%'; pgR.style.width='50%';
    put(pgL, 2*cur-1); put(pgR, 2*cur);
    pgL.style.visibility=cur===0?'hidden':'';
    pgR.style.visibility=cur===NS?'hidden':'';
    wrap.style.transform=cur===0?'translateX(-'+(BW/4)+'px)':
                         cur===NS?'translateX('+(BW/4)+'px)':'';
    document.querySelector('.edge.l').style.width=Math.min(12,cur*1.4)+'px';
    document.querySelector('.edge.r').style.width=Math.min(12,(NS-cur)*1.4)+'px';
    pgno.value=cur===0?'cover':(cur===NS?'back':(2*cur)+'\\u2013'+(2*cur+1));
    bp.disabled=cur===0; bn.disabled=cur===NS;
    scrub.max=NS; scrub.value=cur;
    if(history.replaceState) history.replaceState(null,'','#s'+cur);
  }}
  /* ── the fold, laid out at progress p ∈ (0,1) ──
     Forward peels sheet `cur` right-to-left; backward peels sheet `cur-1` back.
     The paper does not stretch: with the free edge at e, the fold sits midway
     between e and the page's resting edge, and the strip beyond the fold shows
     the sheet's other face, free edge leading. */
  function fold(dir,p){{
    p=Math.max(0.001,Math.min(0.999,p));
    const W=BW, P=W/2;
    if(mode==='single'){{
      /* the leaf is bound at the left edge; its free edge travels from the
         right edge across and out. The fold chases it at half speed, so at
         the end the page lies flat against the binding, gone. */
      const idx=dir>0?cur:cur-1;
      const e=W*(1-2*p), l=W*(1-p);
      if(dir>0) put(under, cur+1); else put(under, cur);
      under.style.display='block'; under.style.left='0'; under.style.width='100%';
      if(dir>0) put(pgR, cur); else put(pgR, cur-1);
      pgR.style.visibility='';
      pgR.style.clipPath='inset(0 '+(W-l)+'px 0 0)';
      peelC.style.display='block'; peelC.style.left='0'; peelC.style.width=W+'px';
      const x0=Math.max(0,e);
      peel.style.left=x0+'px'; peel.style.width=Math.max(0,l-x0)+'px';
      const pb1=peel.querySelector('.pback'); if(pb1) pb1.style.display='block';
      peelIn.style.display='none';
      curl.style.background='linear-gradient(90deg,transparent 55%,rgba(59,54,44,.16) 88%,rgba(20,16,8,.32) 99%),'+
        'linear-gradient(90deg,rgba(255,252,240,.5) 0%,transparent 10%)';
      foldsh.style.display='block'; foldsh.style.left=l+'px';
      foldsh.style.background='linear-gradient(90deg,rgba(10,8,4,'+(0.34*Math.sin(Math.min(1,p*1.2)*Math.PI)).toFixed(3)+'),transparent)';
      return;
    }}
    peelIn.style.display=''; const pb=peel.querySelector('.pback'); if(pb) pb.style.display='none';
    if(dir>0){{
      const e=W*(1-p), l=(e+W)/2;
      put(under, 2*(cur+1)); under.style.display='block';
      under.style.left=P+'px'; under.style.width=P+'px';
      under.style.visibility=(cur+1===NS)?'hidden':'';
      pgR.style.visibility='';
      pgR.style.clipPath='inset(0 '+(W-l)+'px 0 0)';
      peelC.style.display='block'; peelC.style.left='0'; peelC.style.width=W+'px';
      peel.style.left=e+'px'; peel.style.width=Math.max(0,l-e)+'px';
      peelIn.style.left='0'; peelIn.style.width=P+'px';
      if(!peel.dataset.face||peel.dataset.face!=='b'+(2*cur+1)){{
        peelIn.innerHTML=''; const lf=leaf(2*cur+1);
        if(lf) peelIn.appendChild(lf.cloneNode(true));
        peel.dataset.face='b'+(2*cur+1);
      }}
      curl.style.background='linear-gradient(90deg,transparent 55%,rgba(59,54,44,.14) 88%,rgba(20,16,8,.30) 99%),'+
        'linear-gradient(90deg,rgba(255,252,240,.5) 0%,transparent 8%)';
      foldsh.style.display='block';
      foldsh.style.left=l+'px';
      foldsh.style.background='linear-gradient(90deg,rgba(10,8,4,'+(0.36*Math.sin(p*Math.PI)).toFixed(3)+'),transparent)';
    }} else {{
      const e=W*p, l=e/2;
      put(under, 2*(cur-1)-1); under.style.display='block';
      under.style.left='0'; under.style.width=P+'px';
      under.style.visibility=(cur-1===0)?'hidden':'';
      pgL.style.visibility='';
      pgL.style.clipPath='inset(0 0 0 '+l+'px)';
      peelC.style.display='block'; peelC.style.left='0'; peelC.style.width=W+'px';
      peel.style.left=l+'px'; peel.style.width=Math.max(0,e-l)+'px';
      peelIn.style.width=P+'px';
      peelIn.style.left=(Math.max(0,e-l)-P)+'px';
      if(!peel.dataset.face||peel.dataset.face!=='f'+(2*(cur-1))){{
        peelIn.innerHTML=''; const lf=leaf(2*(cur-1));
        if(lf) peelIn.appendChild(lf.cloneNode(true));
        peel.dataset.face='f'+(2*(cur-1));
      }}
      curl.style.background='linear-gradient(-90deg,transparent 55%,rgba(59,54,44,.14) 88%,rgba(20,16,8,.30) 99%),'+
        'linear-gradient(-90deg,rgba(255,252,240,.5) 0%,transparent 8%)';
      foldsh.style.display='block';
      foldsh.style.left=(l-70)+'px';
      foldsh.style.background='linear-gradient(-90deg,rgba(10,8,4,'+(0.36*Math.sin(p*Math.PI)).toFixed(3)+'),transparent)';
    }}
  }}
  function unfoldStatics(dir){{
    pgR.style.clipPath=''; pgL.style.clipPath=''; peel.dataset.face='';
  }}
  function snapAnim(){{
    /* finish the running turn instantly so the next gesture is never eaten */
    if(!anim) return;
    cancelAnimationFrame(anim.raf);
    const a=anim; anim=null;
    fold(a.dir,a.toP); a.done&&a.done();
  }}
  function spring(dir,fromP,toP,done){{
    snapAnim();
    const dur=matchMedia('(prefers-reduced-motion: reduce)').matches?1:480;
    const t0=performance.now();
    const tick=now=>{{
      let t=Math.min(1,(now-t0)/dur);
      const ease=1-Math.pow(1-t,2.6);
      fold(dir, fromP+(toP-fromP)*ease);
      if(t<1) anim={{raf:requestAnimationFrame(tick),dir,toP,done}};
      else {{ anim=null; done&&done(); }}
    }};
    anim={{raf:requestAnimationFrame(tick),dir,toP,done}};
  }}
  function turn(dir){{
    if(mode==='') return;
    snapAnim();
    const top=mode==='single'?NP-1:NS;
    if(dir>0&&cur>=top||dir<0&&cur<=0) return;
    wrap.style.transform='';
    if(mode==='single'&&dir<0){{
      /* the previous leaf folds back in from the left */
      spring(-1,1,0,()=>{{ cur-=1; unfoldStatics(-1); settle(); }});
      return;
    }}
    spring(dir,0.02,1,()=>{{ cur+=dir; unfoldStatics(dir); settle(); }});
  }}
  function go(n){{
    if(anim){{cancelAnimationFrame(anim.raf);anim=null;unfoldStatics(1);}}
    cur=Math.max(0,Math.min(mode==='single'?NP-1:NS,n)); settle();
  }}
  const next=()=>turn(1);
  const prev=()=>turn(-1);

  /* the drag: the fold follows the finger, in both modes */
  let D=null;
  book.addEventListener('pointerdown',e=>{{
    if(mode===''||document.body.classList.contains('zoomed')) return;
    if(e.target.closest('a')) return;
    snapAnim();
    if(book.setPointerCapture&&e.pointerId!=null)
      try{{book.setPointerCapture(e.pointerId)}}catch(_){{}}
    const r=book.getBoundingClientRect();
    const x=e.clientX-r.left;
    if(mode==='single'){{
      D={{dir:1,r,x0:e.clientX,t0:performance.now(),moved:false,p:0.02,single:true,
          canFwd:cur<NP-1,canBack:cur>0}};
      if(D.canFwd) fold(1,D.p);
      e.preventDefault(); return;
    }}
    const fwd=x>r.width/2?1:-1;
    if(fwd>0&&cur>=NS||fwd<0&&cur<=0) return;
    D={{dir:fwd,r,x0:e.clientX,t0:performance.now(),moved:false,p:0.02}};
    wrap.style.transform='';
    fold(D.dir,D.p);
    e.preventDefault();
  }});
  addEventListener('pointermove',e=>{{
    if(!D) return;
    const x=e.clientX-D.r.left;
    if(D.single){{
      /* the finger holds the free edge; the crease trails it at half pace */
      if(!D.canFwd) return;
      let p=(1-(x/D.r.width))/2;
      p=Math.max(0,Math.min(1,p*1.06));
      if(Math.abs(e.clientX-D.x0)>4) D.moved=true;
      D.p=p; fold(1,p); return;
    }}
    let p=D.dir>0? 1-(x/D.r.width) : (x/D.r.width);
    p=Math.max(0,Math.min(1,p*1.04));
    if(Math.abs(e.clientX-D.x0)>4) D.moved=true;
    D.p=p; fold(D.dir,p);
  }});
  addEventListener('pointercancel',()=>{{
    if(!D) return;
    const {{dir,p,single}}=D; D=null;
    /* Safari took the gesture back: lay the page where it was going */
    const d=single?1:dir;
    if(p>0.5) spring(d,p,1,()=>{{cur+=d;unfoldStatics(d);settle();}});
    else spring(d,p,0,()=>{{unfoldStatics(d);settle();}});
  }});
  addEventListener('pointerup',e=>{{
    if(!D) return;
    const {{dir,moved,p,t0,x0,single,canFwd,canBack}}=D; D=null;
    const dx=e.clientX-x0, dt=Math.max(1,performance.now()-t0), v=dx/dt;
    if(single){{
      if(!moved){{
        /* a tap: the right third turns forward, the left third turns back */
        const r=book.getBoundingClientRect(), x=e.clientX-r.left;
        unfoldStatics(1); settle();
        if(x<r.width*0.33&&canBack) turn(-1);
        else if(canFwd) turn(1);
        return;
      }}
      if(dx>60&&v>0.35&&canBack){{ unfoldStatics(1); settle(); turn(-1); return; }}
      if(canFwd&&(p>0.28||(v<-0.4&&dx<-50)))
        spring(1,p,1,()=>{{cur+=1;unfoldStatics(1);settle();}});
      else spring(1,p,0,()=>{{unfoldStatics(1);settle();}});
      return;
    }}
    let turnIt;
    if(!moved) turnIt=true;
    else if(dir>0) turnIt=p>0.5||(v<-0.45&&dx<-60);
    else turnIt=p>0.5||(v>0.45&&dx>60);
    if(turnIt) spring(dir,p,1,()=>{{cur+=dir;unfoldStatics(dir);settle();}});
    else spring(dir,p,0,()=>{{unfoldStatics(dir);settle();}});
  }});

  /* zoom: double-click or the button; drag to pan while zoomed */
  let Z=false, pan=null, px=0, py=0;
  function setZoom(on,cx,cy){{
    Z=on; document.body.classList.toggle('zoomed',Z);
    if(Z){{ px=0;py=0;
      zoomer.style.transformOrigin=(cx||50)+'% '+(cy||50)+'%';
      zoomer.style.transform='scale(1.8)'; }}
    else zoomer.style.transform='';
  }}
  document.getElementById('mzoom').addEventListener('click',()=>setZoom(!Z));
  book.addEventListener('dblclick',e=>{{
    const r=book.getBoundingClientRect();
    setZoom(!Z, (e.clientX-r.left)/r.width*100, (e.clientY-r.top)/r.height*100);
  }});
  zoomer.addEventListener('pointerdown',e=>{{ if(!Z)return;
    pan={{x:e.clientX-px,y:e.clientY-py}}; document.body.classList.add('panning'); e.preventDefault(); }});
  addEventListener('pointermove',e=>{{ if(!pan)return;
    px=e.clientX-pan.x; py=e.clientY-pan.y;
    zoomer.style.transform='scale(1.8) translate('+(px/1.8)+'px,'+(py/1.8)+'px)'; }});
  addEventListener('pointerup',()=>{{pan=null;document.body.classList.remove('panning');}});

  /* drawers */
  const thumbsD=document.getElementById('thumbsD'), tocD=document.getElementById('tocD');
  function buildThumbs(){{
    const t=document.getElementById('thumbs'); t.innerHTML='';
    slots.forEach((s,i)=>{{
      const d=document.createElement('div'); d.className='th';
      d.appendChild(s.firstElementChild.cloneNode(true));
      const b=document.createElement('b'); b.textContent=i===0?'cover':i; d.appendChild(b);
      d.addEventListener('click',()=>{{thumbsD.classList.remove('open');
        go(mode==='single'?i:Math.ceil(i/2));}});
      t.appendChild(d);
    }});
  }}
  document.getElementById('mthumbs').addEventListener('click',()=>{{
    tocD.classList.remove('open'); thumbsD.classList.toggle('open');}});
  document.getElementById('mtoc').addEventListener('click',()=>{{
    thumbsD.classList.remove('open'); tocD.classList.toggle('open');}});
  document.getElementById('tocp').addEventListener('click',e=>{{
    const b=e.target.closest('button'); if(!b) return;
    tocD.classList.remove('open');
    go(mode==='single'?Math.max(0,2*(+b.dataset.s)-1):+b.dataset.s);}});
  document.addEventListener('click',e=>{{
    if(!e.target.closest('.drawer')&&!e.target.closest('#mthumbs')&&!e.target.closest('#mtoc')){{
      thumbsD.classList.remove('open'); tocD.classList.remove('open');}}}});
  document.getElementById('mfull').addEventListener('click',()=>{{
    const el=document.documentElement;
    if(document.fullscreenElement) (document.exitFullscreen||document.webkitExitFullscreen).call(document);
    else (el.requestFullscreen||el.webkitRequestFullscreen||function(){{}}).call(el);
  }});
  scrub.addEventListener('input',()=>go(+scrub.value));
  pgno.addEventListener('change',()=>{{
    const n=parseInt(pgno.value,10);
    if(isNaN(n)) return settle&&settle();
    const li=Math.max(0,Math.min(NP-1,n-1));
    go(mode==='single'?li:Math.ceil(li/2));
  }});
  pgno.addEventListener('keydown',e=>{{if(e.key==='Enter')pgno.blur();e.stopPropagation();}});

  function setMode(){{
    const want=isPhone.matches?'single':'book';
    if(want===mode) return;
    const wasLeaf=mode==='single'?cur:cur*2;   /* keep the reader's place */
    const had=mode!=='';
    mode=want;
    slots.forEach(s=>{{s.style.display='none';}});
    if(had) cur=want==='single'?Math.min(NP-1,wasLeaf):Math.ceil(wasLeaf/2);
    sizeBook(); settle();
  }}
  const h=location.hash.match(/^#([sp])(\\d+)$/);
  const wantSingle=isPhone.matches;
  if(h){{
    const n=+h[2], leaf=h[1]==='p'?n:n*2;
    cur=wantSingle?Math.max(0,Math.min(NP-1,leaf)):Math.max(0,Math.min(NSpread,Math.ceil(leaf/2)));
  }}
  setMode(); buildThumbs();
  isPhone.addEventListener?isPhone.addEventListener('change',setMode):isPhone.addListener(setMode);
  addEventListener('resize',()=>{{if(mode==='book'){{sizeBook();settle();}}}});
  bp.addEventListener('click',prev); bn.addEventListener('click',next);
  addEventListener('keydown',e=>{{
    if(e.key==='ArrowRight'||e.key==='PageDown')next();
    if(e.key==='ArrowLeft'||e.key==='PageUp')prev();}});

}})();
</script>
</body></html>"""


# ---------------- DESK PAGES ----------------
def desk_page(d):
    briefs = "".join(f"""<div class="brf rv">
      <div class="bn">{b[0]}</div><h3>{b[1]}</h3><p>{b[2]}</p><div class="tagm">{b[3]}</div></div>""" for b in d["briefing"])
    glos = "".join(f"""<div class="glo rv">
      <div class="term">{g[0]}<i>{g[1]}</i></div><p>{g[2]}</p></div>""" for g in d["glossary"])
    # published articles for this desk first, then house stubs to fill the list
    rows = [(f"a-{a['slug']}.html", a["title"], a["dek"], f"{a['date']} · {a['minutes']} min") for a in desk_articles(d["slug"])]
    stories = ""
    for i,(href,t,dk,m) in enumerate(rows[:6]):
        lead_cls = " dstory--lead" if i == 0 else ""
        stories += f"""<a class="dstory{lead_cls} rv" href="{href}">
      <div class="n">S—{i+1:02d}</div><h3>{figwrap(t) if i==0 else t}</h3><div class="d">{dk}</div><div class="m">{m}</div></a>"""
    stats = "".join(f"<div><b>{v}</b><span>{l}</span></div>" for v,l in d["stats"])
    _dphoto = ""
    for _a2 in desk_articles(d["slug"], 8):
        if _a2["slug"] in PH:
            _dphoto = photo_plate(_a2["slug"], cls="dh-photo", eager=True, label=f"Plate D-{d['no']}"); break
    dh_fig = _dphoto or f"""<figure class="dh-plate">
      {plate(d['motif'], f"Plate D-{d['no']} — the {d['title'].lower()} desk", f"CC/2026/D{d['no']}")}
      <div class="cap"><span>Engraving — CC graphics desk</span><span>D—{d['no']}</span></div>
    </figure>"""
    recs = [(w["label"], e) for w in RECORD.get("weeks", []) for e in w.get("entries", []) if e.get("d") == d["slug"]][:5]
    recsec = ""
    if recs:
        rec_html = "".join(record_entry(e, wl) for wl, e in recs)
        recsec = f"""<section class="burin"><div class="wrap">
    <div class="sec-mast rv"><h2>This desk, on the record — <em>the last eight weeks</em></h2><div class="mono-note"><a href="the-record.html">Full chronicle →</a></div></div>
    <details class="mob-collapse"><summary>Show the chronicle</summary>{rec_html}</details>
  </div></section>"""
    body = f"""{head(f"{d['title']} — Carat Capital", metadesc(d['dek']))}
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
    {dh_fig}
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
    <div class="sec-mast rv"><h2>Talk like the trade — <em>the working vocabulary</em></h2><div class="mono-note">The trade's terms, plainly told</div></div>
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
    <h2>Go deeper — <em>eight weeks of this trade, on one page.</em></h2>
    <a class="big" href="the-record.html">Open the Record →</a>
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
        inner = f"""<div class="sym"><span>{t['name']}</span><span class="code">{t['code']}</span></div><div class="px">{t['px']}</div><div class="d {t['dir']}">{t['chg']}</div>{spark(t['pts'], color)}"""
        if t["code"] == "NAT1":
            cells += f"""<a class="cell cell--cta" href="natural-diamond-prices.html">{inner}<span class="cell-cta">See all natural prices →</span></a>"""
        elif t["code"] == "LGD1":
            cells += f"""<a class="cell cell--cta" href="lab-grown-diamond-prices.html">{inner}<span class="cell-cta">See all lab-grown prices →</span></a>"""
        else:
            cells += f"""<div class="cell">{inner}</div>"""
    ts = WIRE.get("tape_ts", "")
    return f"""<div class="tape" id="tape-a">
  <div class="wrap">
    <div class="head"><span>Carat Capital Price Desk</span><span class="live">● Live — {ts}</span><span>USD · Indicative</span></div>
    <div class="row">{cells}</div>
  </div>
</div>"""

def wire_block():
    def _wire_href(it):
        blob = ((it.get("b") or "") + " " + (it.get("t") or "")).lower()
        for a in ARTICLES[:24]:
            words = [w for w in _re.findall(r"[a-z]{5,}", a["title"].lower())[:4]]
            if words and sum(1 for w in words if w in blob) >= 2:
                return f"a-{a['slug']}.html"
        return None
    items = ""
    for i in WIRE.get("items", []):
        h = _wire_href(i)
        inner = f'<b>{i["b"]}</b>{i["t"]}'
        items += (f'<a class="item" href="{h}">{inner}</a>' if h else f'<span class="item">{inner}</span>')
    return f"""<div class="wire">
  <div class="tag"><span class="blink"></span>The Wire</div>
  <div class="belt"><div class="belt-track" id="belt">{items}</div></div>
</div>"""

DESK_NAMES = {d["slug"]: d["title"] for d in DESKS}

# ---------------- ARTICLE PAGE ----------------
# ---------------- ARTICLE EDITORIAL v2 ----------------
EDITORIAL = json.loads((CONTENT / "editorial.json").read_text()) if (CONTENT / "editorial.json").exists() else {}
for _a in ARTICLES:
    if _a["slug"] in EDITORIAL and "ed" not in _a:
        _a["ed"] = EDITORIAL[_a["slug"]]

def _fig_bars(f):
    rows = f["rows"]; W, LX, RX = 620, 150, 596
    bh, gap, top = 34, 22, 44
    H = top + len(rows) * (bh + gap) + 34
    mx = max(r["v"] for r in rows) or 1
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{f.get("title","")}">',
           f'<text x="20" y="24" font-family="\'IBM Plex Mono\',monospace" font-size="11" letter-spacing="1" fill="#7A7263">{f.get("title","").upper()}</text>']
    y = top
    for r in rows:
        w = max(10, int((RX - LX - 76) * r["v"] / mx))
        col = "#BE3319" if r.get("hi") else "#16130E"
        fw = ' font-weight="600"' if r.get("hi") else ""
        lfs = 11.5 if len(r["l"]) <= 19 else (9.5 if len(r["l"]) <= 24 else 8)
        out.append(f'<text x="{LX-8}" y="{y+bh-12}" font-family="\'IBM Plex Mono\',monospace" font-size="{lfs}" text-anchor="end" fill="{col}"{fw}>{r["l"]}</text>')
        if r.get("hi"):
            out.append(f'<rect x="{LX}" y="{y}" width="{w}" height="{bh}" fill="#BE3319" opacity=".08"/>')
        out.append(f'<rect x="{LX}" y="{y}" width="{w}" height="{bh}" fill="none" stroke="{col}" stroke-width="{1.5 if r.get("hi") else 1.2}"/>')
        for i, ly in enumerate(range(y + 9, y + bh - 5, 9)):
            out.append(f'<line x1="{LX+7}" y1="{ly}" x2="{LX+w-7}" y2="{ly}" stroke="{col}" stroke-width=".45" opacity=".55"/>')
        out.append(f'<text x="{LX+w+10}" y="{y+bh-12}" font-family="\'IBM Plex Mono\',monospace" font-size="12" font-weight="600" fill="{col}">{r["d"]}</text>')
        y += bh + gap
    if f.get("note"):
        nfs = 10 if len(f["note"]) <= 80 else (9 if len(f["note"]) <= 100 else 8)
        nls = 1 if len(f["note"]) <= 80 else 0
        out.append(f'<text x="20" y="{H-8}" font-family="\'IBM Plex Mono\',monospace" font-size="{nfs}" letter-spacing="{nls}" fill="#7A7263">{f["note"].upper()}</text>')
    out.append('</svg>')
    return "".join(out)

def _fig_svg(f):
    return f["svg"] if "svg" in f else _fig_bars(f)

def _amap():
    return {x["slug"]: x for x in ARTICLES}

def _p_split(p, at):
    i = p.find(at) if at else -1
    if i > 0:
        return [p[:i].rstrip(), p[i:]]
    return [p]

def _v2_strip(s):
    cells = ""
    for c in s["cells"]:
        d = f'<span class="{c.get("dir","up")}">{c.get("delta","")}</span> · ' if c.get("delta") else ""
        cells += f'<div class="cell"><div class="fig">{c["fig"]}</div><div class="lab">{d}{c["lab"]}</div></div>'
    return f'<div class="art-strip rv in"><div class="cap">{s["cap"]}</div><div class="grid">{cells}</div></div>'

def _v2_spec(s):
    rows = "".join(f'<div class="row"><div class="l">{r["l"]}</div><div class="v">{r["v"]}</div></div>' for r in s["rows"])
    return f'<div class="art-spec rv in"><div class="cap">{s["cap"]}</div>{rows}</div>'

def _v2_fig(f, num):
    no = f.get("no", ["Plate I", "Fig. II", "Fig. III"][num])
    return f'<figure class="art-fig rv in"><div class="frame">{_fig_svg(f)}</div><figcaption><b>{no}</b> — {f["cap"]}</figcaption></figure>'

def _v2_next(nx, desk, desk_name):
    am = _amap()
    la = am[nx["lead"]["slug"]]
    lead = (f'<a class="leadcard" href="a-{la["slug"]}.html"><div class="t">{nx["lead"]["tag"]} · {la["minutes"]} min</div>'
            f'<h4>{la["title"]}</h4><p>{nx["lead"]["blurb"]}</p></a>')
    minis = ""
    for m in nx["minis"]:
        ma = am[m["slug"]]
        minis += f'<a href="a-{ma["slug"]}.html"><div class="t">{m["tag"]} · {ma["minutes"]} min</div><h5>{ma["title"]}</h5></a>'
    return (f'<div class="art-next rv in"><div class="k"><span>Keep reading · The {desk_name} Desk</span>'
            f'<a href="{desk}.html">Open the desk →</a></div>{lead}<div class="minis">{minis}</div></div>')

def _v2_body(a, ed):
    body = a["body"]
    desk_para = body[-1] if body[-1].startswith("The desk's view:") else None
    out, first = "", True
    for it in ed["flow"]:
        if "sub" in it:
            out += f'<h2 class="art-sub"><span class="n">{it["n"]}</span>{it["sub"]}</h2>'
        elif "p" in it:
            for seg in _p_split(body[it["p"]], it.get("split")):
                cls = ' class="drop"' if first else ""
                out += f"<p{cls}>{seg}</p>"
                first = False
        elif "fig" in it:
            if it["fig"] > 0:
                out += _v2_fig(ed["figs"][it["fig"]], it["fig"])
        elif "pull" in it:
            out += f'<div class="art-pull"><p class="pq">{it["pull"]["q"]}</p><div class="attr">{it["pull"]["attr"]}</div></div>'
        elif "also" in it:
            out += f'<div class="art-also"><span class="k">See also</span><a href="{it["also"]["href"]}">{it["also"]["t"]} →</a></div>'
    if desk_para:
        txt = desk_para[len("The desk's view:"):].strip()
        txt = txt[0].upper() + txt[1:]
        segs = _p_split(txt, ed.get("desk", {}).get("split"))
        dv = f"<p>{segs[0]}</p>"
        if len(segs) > 1:
            dv += f'<p class="kick2">{segs[1]}</p>'
        desk_name = DESK_NAMES.get(a["desk"], a["desk"])
        out += (f'<div class="art-desk rv in"><div class="lab"><span>The Desk&rsquo;s View</span><span>{desk_name}</span></div>'
                f'<div class="in">{dv}</div></div>')
    return out

def article_page_v2(a):
    ed = a["ed"]
    srcs = "".join(f'<a href="{s["url"]}" target="_blank" rel="noopener">{s["title"]} ↗</a>' for s in a.get("sources", []))
    desk_name = DESK_NAMES.get(a["desk"], a["desk"])
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "NewsArticle",
        "headline": a["title"], "description": a["dek"], "datePublished": a["date"],
        "author": {"@type": "Organization", "name": f"Carat Capital — {a['byline']}"},
        "publisher": {"@type": "Organization", "name": "Carat Capital", "url": BASE_URL},
        "articleSection": desk_name, "mainEntityOfPage": f"{BASE_URL}/a-{a['slug']}"
    })
    extra = f'<scr' + f'ipt type="application/ld+json">{jsonld}</scr' + f'ipt>'
    opener = _v2_strip(ed["strip"]) if "strip" in ed else _v2_spec(ed["spec"])
    lead_fig = _v2_fig(ed["figs"][0], 0) if ed.get("figs") else ""
    art_photo = photo_plate(a["slug"], cls="art-photo", eager=True, label="Plate") or motif_plate(a.get("desk","diamonds"), f"CC/{a['date'][-5:]}")
    prog = ('<div id="artprog"></div><scr' + 'ipt>addEventListener("scroll",function(){var h=document.documentElement;'
            'document.getElementById("artprog").style.width=h.scrollTop/(h.scrollHeight-h.clientHeight)*100+"%"})</scr' + 'ipt>')
    return f"""{head(f"{a['title']} — Carat Capital", metadesc(a['dek']), f"a-{a['slug']}.html", extra)}
{prog}
{folio(f"{a['date']} · {desk_name}")}
{navbar(a['desk'])}
{omenu()}
<article class="artpage">
  <div class="wrap">
    <div class="art-head rv in">
      <div class="kick">{a['kicker']}</div>
      <h1 class="art-h">{figwrap(a['title'])}</h1>
      <p class="lead-dek">{a['dek']}</p>
      <div class="byline meta-serif">By <b>{a['byline']}</b> · {a['date']} · {a['minutes']} min read</div>
    </div>
    {art_photo}
    {opener}
    {lead_fig}
    <div class="art-body rv in">{_v2_body(a, ed)}</div>
    <div class="art-sources rv in">
      <div class="kick">Sources &amp; further reading</div>
      {srcs}
    </div>
    <div class="art-brief rv in">
      <div class="k">The Morning Brief · free</div>
      <h3>The trade, filed to your inbox before the New York open.</h3>
      <p>Prices, tenders and the one story that moved the industry overnight — read in ninety seconds.</p>
      <a class="btn" href="https://caratcapital.beehiiv.com" target="_blank" rel="noopener">Subscribe free →</a>
    </div>
    {_v2_next(ed["next"], a["desk"], desk_name)}
  </div>
</article>
{colophon()}
{SCRIPT}"""

def article_page(a):
    if a.get("ed"):
        return article_page_v2(a)
    paras = "".join(f"<p>{p}</p>" for p in a["body"])
    srcs = "".join(f'<a href="{s["url"]}" target="_blank" rel="noopener">{s["title"]} ↗</a>' for s in a.get("sources", []))
    desk_name = DESK_NAMES.get(a["desk"], a["desk"])
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "NewsArticle",
        "headline": a["title"], "description": a["dek"], "datePublished": a["date"],
        "author": {"@type": "Organization", "name": f"Carat Capital — {a['byline']}"},
        "publisher": {"@type": "Organization", "name": "Carat Capital", "url": BASE_URL},
        "articleSection": desk_name, "mainEntityOfPage": f"{BASE_URL}/a-{a['slug']}"
    })
    extra = f'<scr' + f'ipt type="application/ld+json">{jsonld}</scr' + f'ipt>'
    return f"""{head(f"{a['title']} — Carat Capital", metadesc(a['dek']), f"a-{a['slug']}.html", extra)}
{folio(f"{a['date']} · {desk_name}")}
{navbar(a['desk'])}
{omenu()}
<article class="artpage">
  <div class="wrap">
    <div class="art-head rv in">
      <div class="kick">{a['kicker']}</div>
      <h1 class="art-h">{figwrap(a['title'])}</h1>
      <p class="lead-dek">{a['dek']}</p>
      <div class="byline meta-serif">By <b>{a['byline']}</b> · {a['date']} · {a['minutes']} min read</div>
    </div>
    {photo_plate(a["slug"], cls="art-photo", label="Plate") or motif_plate(a.get("desk","diamonds"), f"CC/{a['date'][-5:]}")}
    <div class="art-body rv in">{paras}</div>
    <div class="art-sources rv in">
      <div class="kick">Sources &amp; further reading</div>
      {srcs}
    </div>
  </div>
</article>
<section class="ctastrip">
  <div class="wrap"><div class="inner">
    <h2>More from the {desk_name} desk — <em>the story so far.</em></h2>
    <a class="big" href="{a['desk']}.html">Open the desk →</a>
  </div></div>
</section>
{colophon()}
{SCRIPT}"""

# ---------------- INDEX ----------------
# ---------------- FRONT PAGE (the Dawn Edition homepage) ----------------
# The design lives in home_template.html; everything dated or priced is
# injected here so the page re-dresses itself on every build.
HOME_TPL = (ROOT / "home_template.html")

def _num(px):
    """'4,341.40' -> 4341.40 ; returns None if it is not a number."""
    try: return float(str(px).replace(",", "").replace("$", "").strip())
    except Exception: return None

def _tape_code(code):
    for t in WIRE.get("tape", []):
        if t.get("code") == code: return t
    return None

def _short_date(dl):
    """'Monday, August 10, 2026' -> '10 Aug'"""
    import re as _re
    m = _re.search(r"([A-Z][a-z]+)\s+(\d{1,2})", dl or "")
    return "%s %s" % (m.group(2), m.group(1)[:3]) if m else (dl or "")

def _iso_date(s):
    """'2026-07-01' -> '1 Jul 2026'. Anything else is passed through."""
    import datetime as _dt
    try:
        d = _dt.date.fromisoformat((s or "").strip())
    except ValueError:
        return s or ""
    return "%d %s %d" % (d.day, d.strftime("%b"), d.year)

def _dircls(d):
    return {"up":"up","down":"dn","flat":"fl"}.get(d, "fl")

def index_page():
    import json as _json
    LEAD = lead_article()
    tape = WIRE.get("tape", [])
    xau, nat, lgd = _tape_code("XAU"), _tape_code("NAT1"), _tape_code("LGD1")
    xag = _tape_code("XAG")
    spot_ag = _num((xag or {}).get("px")) or 63.99
    spot_ag_txt = (xag or {}).get("px", "63.99")
    spot = _num(xau["px"]) if xau else 4341.30
    spot_txt = (xau or {}).get("px", "4,341.30")
    asof = WIRE.get("tape_ts") or WIRE.get("date_line") or ""
    # The Bench carries a stamp, not the Editor's whole audit note: keep the
    # date and the source, drop the prose that follows the first clause.
    asof_short = _re.split(r"[,.;]| \u00b7 ", asof.strip(), 1)[0].strip() if asof else ""
    if len(asof_short) > 44:
        asof_short = asof_short[:44].rstrip()
    dateline = WIRE.get("date_line", "")
    edition = WIRE.get("edition", "")
    ed_short = edition.split("—")[-1].strip() if "—" in edition else edition

    # ── the running tape ──
    tape_rows = [[t["name"].upper(), t["px"], _dircls(t.get("dir")), t.get("chg","")] for t in tape[:6]]
    tape_rows.append(["EDITION", ed_short or "—", "up", "● PRINTED 06:00 ET"])
    tape_rows.append(["SPECIMEN TAPE", "illustrative", "fl", "not quoted"])

    # ── the price desk tabs: the Carat indices, drawn from their real series ──
    # The metals live on the running tape and the bench; this desk charts the
    # paper's own five indices. Every curve is the actual daily series from
    # content/indices.json — the first real chart on the page, and footnoted
    # as such. If the index desk has not filed, the metals return as specimen
    # tabs with the old honest disclaimer.
    px_rows = []
    px_dates = []
    if IDX:
        _cons = {c["sym"]: c for c in IDX["constituents"]}
        px_dates = [d for d, _ in IDX["indices"]["CC20"]["series"]]
        for code in ("CC20", "CC-M", "CC-C", "CC-P", "CC-W"):
            x = IDX["indices"][code]
            d1 = x["d1p"]
            arrow = "▲" if d1 > 0 else ("▼" if d1 < 0 else "—")
            px_rows.append({
                "k": f"{code} · {x['name']}", "v": f"{x['level']:,.2f}",
                "d": f"{arrow} {d1:+.2f}%",
                "cls": "up" if d1 > 0 else ("dn" if d1 < 0 else "fl"),
                "ser": [round(v, 2) for _, v in x["series"]],
                # the analyst's row: enough to read the index without leaving
                "st": {"w1": x["w1p"], "m1": x["m1p"], "ytd": x["ytdp"],
                       "hi": x["hi"], "lo": x["lo"], "dd": x["mddp"]},
                "dek": x["dek"],
                "ft": ("Drawn from exchange closes · equal weight, base 100 = "
                       "first trading day of the year · as of %s" % IDX["as_of"])})
    else:
        _ph, _lh = PRICES.get("headline", {}), LAB.get("headline", {})
        _px_src = {}
        if _lh:
            _px_src["LGD1"] = "CVD wholesale band midpoint · %s" % (LAB.get("as_of") or "published list")
        if _ph:
            _px_src["NAT1"] = "%s · %s price list" % (
                _ph.get("rapi_label", "RAPI"), _iso_date(_ph.get("rapi_date", "")))
        for i, t in enumerate(tape[:5]):
            px_rows.append({"k": t["name"], "v": t["px"], "d": t.get("chg",""),
                            "cls": _dircls(t.get("dir")), "seed": 3 + i*7,
                            "trend": 1 if t.get("dir")=="up" else (-1 if t.get("dir")=="down" else 1),
                            "ft": "Series shape illustrative, not quoted · Mark: "
                                  + _px_src.get(t.get("code"), "as carried on the tape")})
    if not px_rows:
        px_rows = [{"k":"Gold / oz","v":spot_txt,"d":"— unch.","cls":"fl","seed":9,"trend":1,"ft":"Kitco spot basis"}]

    # ── the counter sheet: arithmetic on the tape, never invented ──
    perg = spot / 31.1035
    natv, lgdv = _num((nat or {}).get("px")), _num((lgd or {}).get("px"))
    ledger = [{
      "num": "$%s" % f"{perg:,.2f}", "lab": "per gram, fine", "dk": "#E8C06A", "desk": "D—02 Gold",
      "move": "Gold sits at %s the ounce%s." % (spot_txt, (", " + xau["chg"].replace("—","").strip()) if xau and xau.get("chg") else ""),
      "ctr": "A 5&nbsp;g 18ct band carries about $%s of metal before you have made a thing on it." % f"{perg*0.75*5:,.0f}",
      "viz": {"t":"spark","seed":9,"trend":1,"lo":"the tape","hi":spot_txt},
      "work": ["%s &divide; 31.1035 g = %s per gram fine" % (spot_txt, f"{perg:,.2f}"),
               "%s &times; 0.750 (18ct) = %s per gram at 18ct" % (f"{perg:,.2f}", f"{perg*0.75:,.2f}"),
               "%s &times; 5 g = %s" % (f"{perg*0.75:,.2f}", f"{perg*0.75*5:,.2f}")],
      "src": ["Full tape &amp; tables", "almanac.html"]}]
    if natv and lgdv:
        ledger.append({
          "num": "%.1f&times;" % (natv/lgdv), "lab": "natural : lab", "dk": "#8CC5FF", "desk": "D—01 Diamonds",
          "move": "Natural one-carat at %s against lab-grown at %s." % (nat["px"], lgd["px"]),
          "ctr": "The same look at a fraction of the ticket. Your case has to answer for the difference, out loud.",
          "viz": {"t":"ratio","a":["Natural",natv,"#8CC5FF"],"b":["Lab",lgdv,"rgba(220,234,245,.30)"]},
          "work": ["%s &divide; %s = %.2f&times;" % (nat["px"], lgd["px"], natv/lgdv),
                   "both figures as carried on this morning&rsquo;s tape"],
          "src": ["The lab-grown price list", "lab-grown-diamond-prices.html"]})
    # two editorial lines, taken from whatever the desks actually filed
    _seen = {LEAD["slug"]} if LEAD else set()
    for a in ARTICLES:
        if len(ledger) >= 4: break
        if a.get("lead") or a["slug"] in _seen: continue
        _seen.add(a["slug"])
        ledger.append({
          "num": "&rarr;", "lab": DESK_NAMES.get(a.get("desk"), "the desks"),
          "dk": "#6FE3E3", "desk": "D—%s" % next((d["no"] for d in DESKS if d["slug"]==a.get("desk")), "06"),
          "move": a["title"],
          "ctr": (a.get("dek") or "")[:150],
          "viz": {"t":"split","a":["Filed today",100,"#6FE3E3"],"b":["",0,"rgba(220,234,245,.22)"]},
          "work": ["filed by %s" % a.get("byline","the desk"), "%s minutes" % a.get("minutes",5)],
          "src": [a["title"], "a-%s.html" % a["slug"]]})

    # ── today's paper: what this edition actually filed behind the lead ──
    # A fixed slice of six silently borrowed from yesterday and then printed
    # a hardcoded count over it. The section now shows this morning's own
    # stories and says how many there are; a thin day prints a short grid.
    _WORDS = {0:"No", 1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six"}
    _today = (LEAD or {}).get("date")
    _todays = [x for x in ARTICLES if not x.get("lead") and x.get("date") == _today]
    if len(_todays) >= 2:
        _pick = _todays[:6]
        _hook = "%s more this morning" % _WORDS.get(len(_pick), len(_pick))
    else:
        _pick = [x for x in ARTICLES if not x.get("lead")][:6]
        _hook = "%s more, recently filed" % _WORDS.get(len(_pick), len(_pick))
    arts = []
    for a in _pick:
        # the story's own photograph if it has one, its desk's hero if not —
        # every card carries a plate, and every plate carries its credit
        img = a["slug"] if a["slug"] in PH else DESK_HERO.get(a.get("desk", ""), "")
        if img not in PH:
            img = ""
        arts.append({"h": a["title"], "p": (a.get("dek") or "")[:120],
                     "img": img, "cr": PH.get(img, {}).get("credit", ""),
                     "s": DESK_NAMES.get(a.get("desk"), "Desk"),
                     "t": "%s min" % a.get("minutes", 5),
                     "href": "a-%s.html" % a["slug"]})

    # ── the desk board: what each desk actually filed ──
    HUE = {"diamonds":"#8CC5FF","gold-metals":"#E8C06A","gemstones":"#4FD08A",
           "watches":"#B79BFF","auctions":"#FF8FA8","retail-tech":"#6FE3E3"}
    board = []
    for d in DESKS:
        da = desk_articles(d["slug"], 3)
        if not da: continue
        st = (d.get("stats") or [("—","")])[0]
        _hero = DESK_HERO.get(d["slug"], "")
        board.append({"n": "D—%s" % d["no"], "t": d["title"], "c": HUE.get(d["slug"], "#C6A24A"),
                      "img": _hero if _hero in PH else "",
                      "seed": 3 + int(d["no"])*6, "trend": 1, "href": "%s.html" % d["slug"],
                      "st": {"k": st[1], "v": st[0], "d": d.get("tag",""), "cls": "fl"},
                      "a": [[x["title"], "a-%s.html" % x["slug"], "%s min" % x.get("minutes",5)] for x in da]})

    lead_href = "a-%s.html" % LEAD["slug"] if LEAD else "#"
    lead_img = "assets/ph/%s.jpg" % LEAD["slug"] if LEAD and LEAD["slug"] in PH else \
               ("assets/ph/%s.jpg" % DESK_HERO.get((LEAD or {}).get("desk",""), "diamonds-hero"))
    lead_plate = "Plate I — %s" % DESK_NAMES.get((LEAD or {}).get("desk"), "Carat Capital")

    html = HOME_TPL.read_text()
    # ── the menu's six desks, straight from DESKS so they cannot drift ──
    menu_desks = "".join(
        f'<a class="omx-desk" style="--i:{i}" href="{d["slug"]}.html">'
        f'<span class="n">D&mdash;{d["no"]}</span>'
        f'<span class="t">{d["title"]}</span>'
        f'<span class="d">{d["tag"]}</span></a>'
        for i, d in enumerate(DESKS))

    # ── one line under the charts: the door to the full Index Desk ──
    # (the five indices themselves are the tabs above, so no chip row here)
    idx_strip = ""
    if IDX:
        idx_strip = f"""<div class="ixstrip rv rv-3">
  <div class="ixhead"><span>Computed by this desk, quoted from no one &mdash; the spreads, the twenty and the method</span>
    <a href="indices.html">Open the Index Desk &rarr;</a></div>
</div>"""

    for k, v in {
      "__IDX_STRIP__": idx_strip,
      "__MENU_DESKS__": menu_desks,
      "__TAPE_JSON__": _json.dumps(tape_rows),
      "__PX_JSON__": _json.dumps(px_rows),
      "__PX0_K__": px_rows[0]["k"], "__PX0_V__": px_rows[0]["v"], "__PX0_D__": px_rows[0]["d"],
      "__PX0_FT__": px_rows[0]["ft"],
      "__PXD_JSON__": _json.dumps(px_dates),
      "__LEDGER_JSON__": _json.dumps(ledger),
      "__ARTS_JSON__": _json.dumps(arts),
      "__BOARD_JSON__": _json.dumps(board),
      "__SPOT__": "%.2f" % spot, "__SPOT_TXT__": spot_txt,
      "__SPOT_AG__": "%.2f" % spot_ag, "__SPOT_AG_TXT__": spot_ag_txt,
      "__SPOT_AG_LINE__": "SILVER %s / OZ &middot; %s" % (spot_ag_txt, str((xag or {}).get("chg","")).upper()),
      "__SPOT_LINE__": "GOLD %s / OZ &middot; %s" % (spot_txt, str((xau or {}).get("chg","")).upper()),
      # the price desk's stamp: the tape's own as-of, never a frozen date
      "__PX_ASOF__": (("The Carat indices · computed %s · exchange closes" % IDX["as_of"]) if IDX
                      else "Metals " + (" · ".join((asof or "").split(" · ")[:2]) or dateline)),
      "__ALSO_HOOK__": _hook, "__ALSO_LINE__": _hook[:1].lower() + _hook[1:],
      "__ASOF__": asof, "__ASOF_SHORT__": asof_short,
      "__DATELINE__": dateline, "__EDITION__": edition,
      "__EDITION_SHORT__": ed_short, "__DATE_SHORT__": _short_date(dateline),
      "__LEAD_KICKER__": (LEAD or {}).get("kicker","Lead story"),
      "__LEAD_TITLE__": (LEAD or {}).get("title",""),
      "__LEAD_DEK__": (LEAD or {}).get("dek",""),
      "__LEAD_BY__": "%s · %s min read" % ((LEAD or {}).get("byline","The desk"), (LEAD or {}).get("minutes",5)),
      "__LEAD_HREF__": lead_href, "__LEAD_IMG__": lead_img, "__LEAD_PLATE__": lead_plate,
    }.items():
        html = html.replace(k, str(v))
    return html

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
    <h1 class="art-h" style="font-size:clamp(40px,6.4vw,92px);text-transform:uppercase">Learn the trade<em style="font-family:var(--disp);font-style:normal;font-weight:400;color:var(--seal);text-transform:none;font-size:.55em;display:block;margin-top:14px;letter-spacing:-.01em">The working vocabulary, desk by desk</em></h1>
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
    <h2>Fluent yet? — <em>test it on today's front page.</em></h2>
    <a class="big" href="index.html">Read today's edition →</a>
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
      <p>We publish six desks — Diamonds, Gold &amp; Metals, Colored Gemstones, Watches, Auctions &amp; Estates, and Retail &amp; Technology — plus a daily price tape and the Morning Brief, a five-minute email filed before the market opens. Everything on this site is free to read, cover to cover.</p>
      <h2 id="standards" style="font-family:var(--disp);font-weight:700;font-size:28px;letter-spacing:-.02em;margin:34px 0 16px;scroll-margin-top:90px">Editorial standards</h2>
      <p>Everything we publish is original writing. We research widely and credit sources by name and link at the foot of every article. We never reproduce another publication's text or images. Prices are verified the morning of publication or marked unchanged. We do not accept payment for coverage; sponsored content, when it exists, will say so in the headline. When we are wrong, we correct in place and note it. Every claim is priced, sourced, or cut.</p>
      <h2 id="contact" style="font-family:var(--disp);font-weight:700;font-size:28px;letter-spacing:-.02em;margin:34px 0 16px;scroll-margin-top:90px">Write to the desk</h2>
      <p>Tips, corrections, interview subjects and partnership inquiries: <b>connect@roomysjewelery.store</b>. We read everything; the good tips make the wire.</p>
    </div>
  </div>
</article>
<section class="ctastrip">
  <div class="wrap"><div class="inner">
    <h2>Judge us by the work — <em>start with today's front page.</em></h2>
    <a class="big" href="index.html">Read the paper →</a>
  </div></div>
</section>
{colophon()}
{SCRIPT}"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><circle cx="16" cy="16" r="15.2" fill="#F2EDE3" stroke="#16130E" stroke-width="1.3"/><circle cx="16" cy="16" r="12.9" fill="none" stroke="#16130E" stroke-width=".7"/><path d="M 16 26.4 L 11.7 18.3 C 10.4 14.4 10.6 11 12.6 8.6 C 13.7 7.2 14.7 6.6 16 6.4 C 17.3 6.6 18.3 7.2 19.4 8.6 C 21.4 11 21.6 14.4 20.3 18.3 Z" fill="none" stroke="#16130E" stroke-width="1.5" stroke-linejoin="miter"/><path d="M 16 25.2 L 16 16.6" stroke="#16130E" stroke-width=".9"/><path d="M 16 10.2 L 18.7 13.6 L 16 17 L 13.3 13.6 Z" fill="#BE3319"/></svg>"""

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
    NIB = "M 500 722 L 413 556 C 386 478 390 408 430 358 C 452 330 474 318 500 314 C 526 318 548 330 570 358 C 610 408 614 478 587 556 Z"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">
<defs><mask id="cm"><rect width="1000" height="1000" fill="white"/>
<path d="{NIB}" fill="black" stroke="black" stroke-width="54" stroke-linejoin="miter"/></mask></defs>
<circle cx="500" cy="500" r="480" stroke="#16130E" stroke-width="7" fill="none"/>
<path d="{" ".join(ticks)}" stroke="#16130E" stroke-width="3" fill="none" opacity=".9"/>
<circle cx="500" cy="500" r="446" stroke="#16130E" stroke-width="4" fill="none"/>
<g transform="translate(500,500) scale(1.06) translate(-500,-500)">
<g mask="url(#cm)">{"".join(rings)}</g>
<path d="{NIB}" stroke="#16130E" stroke-width="11" fill="none" stroke-linejoin="miter"/>
<path d="M 500 700 L 500 512" stroke="#16130E" stroke-width="7"/>
<path d="M 443 574 C 424 500 430 432 462 386 M 557 574 C 576 500 570 432 538 386" stroke="#16130E" stroke-width="4.5" fill="none" opacity=".85"/>
<path d="M 500 396 L 552 462 L 500 528 L 448 462 Z" fill="#BE3319"/></g></svg>'''

def sitemap(pages):
    def _loc(p): return BASE_URL if p == "index.html" else cu(f"{BASE_URL}/{p}")
    urls = "".join(f"<url><loc>{_loc(p)}</loc></url>" for p in pages)
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
(out/"natural-diamond-prices.html").write_text(prices_page())
(out/"lab-grown-diamond-prices.html").write_text(lab_prices_page())
(out/"indices.html").write_text(indices_page())
(out/"magazine.html").write_text(magazine_page())
for _f in out.glob("*.html"):
    _f.write_text(_clean_links(_f.read_text()))
(out/"assets"/"favicon.svg").write_text(FAVICON)
(out/"assets"/"logo-mark.svg").write_text(logo_mark_svg())
(out/"feed.xml").write_text(rss_feed())
(out/"llms.txt").write_text(llms_txt())
pages = ["index.html", "field-guide.html", "about.html", "the-record.html", "almanac.html", "natural-diamond-prices.html", "lab-grown-diamond-prices.html", "indices.html", "magazine.html"] + [f"{d['slug']}.html" for d in DESKS] + [f"a-{a['slug']}.html" for a in ARTICLES]
(out/"sitemap.xml").write_text(sitemap(pages))
(out/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
print("built:", ", ".join(pages), "+ sitemap, robots, favicon")
