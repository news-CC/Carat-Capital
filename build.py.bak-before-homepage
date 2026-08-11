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
   stats=[("$727","Lab-grown 1ct, wholesale"),("~20%","Of sales now online"),("24","Median first-buyer age")],
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
            out += f'<div class="art-pull"><q>{it["pull"]["q"]}</q><div class="attr">— {it["pull"]["attr"]}</div></div>'
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
    return f"""{head(f"{a['title']} — Carat Capital", a['dek'][:150], f"a-{a['slug']}.html", extra)}
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
    return f"""{head(f"{a['title']} — Carat Capital", a['dek'][:150], f"a-{a['slug']}.html", extra)}
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
def index_page():
    LEAD = lead_article()
    lead_href = f"a-{LEAD['slug']}.html" if LEAD else "#"
    latest_date = max(a["date"] for a in ARTICLES)
    lead_photo = photo_plate(LEAD["slug"], cls="plate-hero", eager=True, label="Plate I") if LEAD else ""
    if not lead_photo and LEAD:
        lead_photo = desk_hero_plate(LEAD.get("desk","diamonds"), "PLATE I")
    # stat band from the lead's editorial numbers strip
    statband = ""
    ed = (LEAD or {}).get("ed") or {}
    cells = (ed.get("strip") or {}).get("cells", [])[:3]
    if cells:
        tiles = "".join(f'<a class="sb-tile" href="{lead_href}"><div class="v">{c["fig"]}</div><div class="l">{c["lab"]}</div></a>' for c in cells)
        statband = (f'<section class="statband sec--tint"><div class="wrap"><div class="sb-grid rv">{tiles}'
                    f'<a class="sb-tile sb-more" href="almanac.html"><div class="v">→</div><div class="l">The quarter in numbers</div></a></div></div></section>')
    # pull-quote band from the lead's flow
    quote, attr = "", ""
    for it in ed.get("flow", []):
        if "pull" in it:
            quote, attr = it["pull"]["q"], it["pull"].get("attr",""); break
    if not quote:
        quote, attr = "Every stone has a price. The story is who pays it.", "The masthead"
    plateband = (f'<section class="plateband"><div class="wrap"><blockquote class="rv">&ldquo;{quote}&rdquo;</blockquote>'
                 f'<div class="attr rv">— {attr}</div></div></section>')
    railmini = '<div class="rm-k">Also filed today</div>' + "".join(
        f'<a href="a-{x["slug"]}.html"><span class="rm-d">{DESK_NAMES.get(x.get("desk"),"")[:14]}</span>{x["title"]}</a>'
        for x in [a for a in ARTICLES if not a.get("lead")][:3])
    # price rail (compact tape)
    chips = ""
    for t in WIRE.get("tape", [])[:5]:
        if t["code"] == "NAT1":
            chips += f"""<a class="chip chip--cta" href="natural-diamond-prices.html"><span class="nm">{t['name']}</span><span class="px">{t['px']}</span><span class="d {t['dir']}">{t['chg']}</span><span class="cta">See all natural prices →</span></a>"""
        elif t["code"] == "LGD1":
            chips += f"""<a class="chip chip--cta" href="lab-grown-diamond-prices.html"><span class="nm">{t['name']}</span><span class="px">{t['px']}</span><span class="d {t['dir']}">{t['chg']}</span><span class="cta">See all lab-grown prices →</span></a>"""
        else:
            chips += f"""<a class="chip" href="almanac.html"><span class="nm">{t['name']}</span><span class="px">{t['px']}</span><span class="d {t['dir']}">{t['chg']}</span></a>"""
    # desk navigator: latest story per desk + count
    # desk of the day = most stories filed today; runner-up gets the second wide card
    fresh_counts = {d["slug"]: sum(1 for a in ARTICLES if a.get("desk") == d["slug"] and a["date"] == latest_date) for d in DESKS}
    ranked = sorted(DESKS, key=lambda d: (-fresh_counts[d["slug"]], int(d["no"])))
    lead_desk = ranked[0]["slug"]
    wide_desk = ranked[1]["slug"] if len(ranked) > 1 else None
    cards = ""
    for d in DESKS:
        da = [a for a in ARTICLES if a.get("desk") == d["slug"]]
        top = da[0] if da else None
        if top and LEAD and top["slug"] == LEAD["slug"] and len(da) > 1:
            top = da[1]
        fresh = '<span class="new">NEW TODAY</span>' if top and top["date"] == latest_date else (f'<span class="dt">{top["date"]}</span>' if top else "")
        acc = DESK_ACCENTS.get(d["slug"], "#96762E")
        _hero = DESK_HERO.get(d["slug"])
        bg = f'<div class="dc-bg"><img src="assets/ph/{_hero}.jpg" alt="" loading="lazy" decoding="async"></div>' if (_hero and _hero in PH) else ""
        if d["slug"] == lead_desk and top:
            xcls, badge = "dcard--lead", '<span class="deskled">Desk of the day</span>'
        elif d["slug"] == wide_desk and top:
            xcls, badge = "dcard--wide", f'<span class="glyph">{desk_glyph(d["slug"], 34)}</span>'
        else:
            xcls, badge = "", f'<span class="glyph">{desk_glyph(d["slug"], 34)}</span>'
        cards += f"""<a class="dcard {xcls} rv" href="{d['slug']}.html" style="--da:{acc}">{bg}
      <div class="row1"><span class="no">D—{d['no']}</span>{badge}<span class="ct">{len(da)} stories</span></div>
      <h3>{d['title']}</h3>
      <div class="tagl">{d['tag']}</div>
      <div class="latest">{fresh}<span class="lt">{top['title'] if top else ''}</span></div>
      <div class="go">Open the desk →</div>
    </a>"""
    # today's edition: 4 newest non-lead headlines
    rows = ""
    others = [a for a in ARTICLES if not a.get("lead")][:5]
    _used_imgs = set()
    for i, a in enumerate(others, 2):
        _img, _own = best_img(a["slug"], a.get("desk"))
        if _img and not _own and _img in _used_imgs:
            _img = ""  # don't repeat the same category photo twice; fall back to a glyph
        if _img:
            _used_imgs.add(_img)
        if _img:
            cell = f'<span class="th{"" if _own else " th--desk"}" style="--da:{DESK_ACCENTS.get(a.get("desk"),"#96762E")}"><img src="{_img}" alt="" loading="lazy" decoding="async"></span>'
        else:
            cell = f'<span class="th thg" style="--da:{DESK_ACCENTS.get(a.get("desk"),"#96762E")}">{desk_glyph(a.get("desk","diamonds"), 34)}</span>'
        if i == 2:
            rows += f"""<a class="trow trow--lead" href="a-{a['slug']}.html">{cell}<span class="tx"><span class="t">{figwrap(a['title'])}</span><span class="dk">{(a['dek'] if len(a['dek'])<=150 else a['dek'][:150].rsplit(' ',1)[0].rstrip(',;— ') + ' …')}</span><span class="m meta-serif">{DESK_NAMES.get(a['desk'],'')} · {a['minutes']} min</span></span></a>"""
        else:
            rows += f"""<a class="trow" href="a-{a['slug']}.html"><span class="n">{i:02d}</span>{cell}<span class="t">{a['title']}</span><span class="m">{DESK_NAMES.get(a['desk'],'')} · {a['minutes']} min</span></a>"""
    return f"""{head("CARAT CAPITAL — The Trade Paper of the Jewelry World",
      "Carat Capital is the trade paper of the global jewelry industry. Prices, intelligence and reporting from every desk of the stone trade.")}
{navbar()}
{omenu()}
{wire_block()}
<header class="nameplate home-plate rv in">
  {HALLROW}
  <div class="h1">CARAT<span class="caret">^</span>CAPITAL</div>
  <div class="plate-sub">The Trade Paper of the Jewelry World</div>
</header>
<section class="heroF" id="front">
  <div class="wrap"><div class="hf-grid">
    <article class="rv">
      <div class="kick">{LEAD['kicker'] if LEAD else 'Lead Story'}</div>
      <h2 class="lead-h"><a href="{lead_href}">{figwrap(LEAD['title']) if LEAD else ''}</a></h2>
      <p class="lead-dek">{LEAD['dek'] if LEAD else ''}</p>
      <div class="byline meta-serif">By <b>{LEAD['byline'] if LEAD else ''}</b> · {LEAD['minutes'] if LEAD else 0} min read</div>
      {lead_photo}
      <a class="hf-cta" href="{lead_href}">Read this morning&rsquo;s lead →</a>
    </article>
    <aside class="pricerail rv rv-d1">
      <div class="pr-head"><span>The Price Desk</span><span class="live">● {WIRE.get("tape_ts","")}</span></div>
      <div class="chips">{chips}</div>
      <a class="pr-more" href="almanac.html">Full tape &amp; tables →</a>
      <div class="rail-foot">
        <div class="ed-line">{WIRE.get('date_line','')} · {WIRE.get('edition','')}</div>
        <div class="rail-sub">
          <div class="k">The Morning Brief · free</div>
          <div class="row"><input id="rs-em" type="email" placeholder="you@thetrade.com" aria-label="Email">
          <a class="go" href="https://caratcapital.beehiiv.com" target="_blank" rel="noopener" onclick="var v=document.getElementById('rs-em').value;if(v)this.href='https://caratcapital.beehiiv.com/subscribe?email='+encodeURIComponent(v)">Join →</a></div>
          <div class="n">The trade, before the New York open.</div>
        </div>
        <div class="rail-mini">{railmini}</div>
        <a class="fg-card" href="field-guide.html"><span class="fk">New here?</span><span>Start with the Field Guide →</span></a>
      </div>
    </aside>
  </div></div>
</section>
<section class="desknav" id="desks">
  <div class="wrap">
    <div class="sec-mast rv"><h2>Find <em>your</em> desk.</h2><div class="mono-note">Six industries · one paper · updated daily</div></div>
    <div class="dn-grid">{cards}</div>
  </div>
</section>
{statband}
<section class="todayed sec--rule-gilt">
  <div class="wrap">
    <div class="sec-mast rv"><h2>Also in today&rsquo;s paper<em>.</em></h2><div class="mono-note">{WIRE.get("edition","")}</div></div>
    <div class="te-list rv">{rows}</div>
    <div class="te-links rv"><a href="the-record.html">Eight weeks of the trade → The Record</a><a href="almanac.html">The quarter in numbers → The Almanac</a><a href="field-guide.html">New to the trade? → The Field Guide</a></div>
  </div>
</section>
{plateband}
<section class="homebrief">
  <div class="wrap"><div class="hb-in rv">
    <div class="k">The Morning Brief · free</div>
    <h3>The trade, filed to your inbox before the New York open.</h3>
    <p>Prices, tenders and the one story that moved the industry overnight — read in ninety seconds.</p>
    <a class="btn" href="https://caratcapital.beehiiv.com" target="_blank" rel="noopener">Subscribe free →</a>
  </div></div>
</section>
<div class="subbar"><span>The Morning Brief — free, before the NY open</span><a href="https://caratcapital.beehiiv.com" target="_blank" rel="noopener">Subscribe →</a></div>
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
for _f in out.glob("*.html"):
    _f.write_text(_clean_links(_f.read_text()))
(out/"assets"/"favicon.svg").write_text(FAVICON)
(out/"assets"/"logo-mark.svg").write_text(logo_mark_svg())
(out/"feed.xml").write_text(rss_feed())
(out/"llms.txt").write_text(llms_txt())
pages = ["index.html", "field-guide.html", "about.html", "the-record.html", "almanac.html", "natural-diamond-prices.html", "lab-grown-diamond-prices.html"] + [f"{d['slug']}.html" for d in DESKS] + [f"a-{a['slug']}.html" for a in ARTICLES]
(out/"sitemap.xml").write_text(sitemap(pages))
(out/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
print("built:", ", ".join(pages), "+ sitemap, robots, favicon")
