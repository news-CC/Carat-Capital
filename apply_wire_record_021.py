#!/usr/bin/env python3
import json, pathlib
C = pathlib.Path("content")
wire = json.loads((C/"wire.json").read_text())
record = json.loads((C/"record.json").read_text())

wire["date_line"] = "Friday, July 31, 2026"
wire["edition"] = "Vol. I — No. 021"
wire["tape_ts"] = "31 Jul 2026, late session · the complex closes July lower"
wire["items"] = [
 {"b":"DE BEERS NARROWS THE LOSS","t":" — Anglo American's half-year accounts put De Beers revenue at $1.58 billion, down 19%, with an underlying loss of $188 million, 23% narrower, and an underlying EBITDA loss of $113 million; the realised price fell 32% to $105 a carat while unit costs fell 26% to $64"},
 {"b":"THE INDEX HOLDS AT 68 AND 69","t":" — De Beers' rough price index sat 16% below last year but moved barely at all inside the half, 68 in the first quarter and 69 in the second, the first quantitative support for the argument that rough has found its level"},
 {"b":"GOLD GIVES BACK $4,086","t":" — Spot fell 1.19% to $4,054.68 an ounce on the last trading day of July as the dollar rebounded from a six-week trough and traders booked Thursday's post-Fed rally; gold is still 20.57% higher on the year and about 1.4% up on the month"},
 {"b":"WHITE METALS ALL LOWER","t":" — Silver fell 1.72% to $57.99, platinum 1.46% to $1,636 and palladium 1.53% to $1,288.50, putting the gold-silver ratio near 69.9; on the year silver is up 56.44%, platinum 24.28% and palladium 6.80%"},
 {"b":"278 TONNES OF JEWELLERY","t":" — World Gold Council data put second-quarter jewellery demand at 278 tonnes, down 17% and the lowest quarterly volume since the pandemic, though its value rose 14% to $40 billion against a quarterly average price of $4,506.29"},
 {"b":"INDIA BUYS 15% LESS","t":" — Indian jewellery demand fell to 75.1 tonnes in the second quarter from 88.8 tonnes, with total Indian gold demand down 6% and the value of that demand up about 50% as prices set records"},
 {"b":"CONFIDENCE SLIPS TO 90.8","t":" — The Conference Board's index fell 1.4 points in July against a 92.3 consensus; the present situation index dropped 3.6 points to 114.9, a third consecutive decline, while expectations held at 74.7"},
 {"b":"THE ASK IS EXCLUSION","t":" — Jewelers of America met administration officials as a 10% to 12.5% duty round covering roughly sixty countries took effect, seeking to remove diamonds, gemstones and pearls from the schedule; seven African producers and EU-polished goods are exempt, India stays at 10%"},
 {"b":"GEMFIELDS TAKES $102.9 MILLION","t":" — First-half auction revenue rose 72%, carried by emerald, while premium-grade ruby recovery at Montepuez ran at 0.025 carats a tonne; net debt stood at $44.2 million on June 30 before $33.3 million of auction receivables"},
]
wire["tape"] = [
 {"name":"Gold / oz","code":"XAU","px":"4,054.68","chg":"▼ −1.19%","dir":"down",
  "pts":[16,16,15,15,15,14,14,15,16,15]},
 {"name":"Natural 1ct (RAPI proxy)","code":"NAT1","px":"5,232.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Lab-grown 1ct wholesale","code":"LGD1","px":"727.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Platinum / oz","code":"XPT","px":"1,636.00","chg":"▼ −1.46%","dir":"down",
  "pts":[17,17,16,16,16,15,15,15,17,16]},
 {"name":"Silver / oz","code":"XAG","px":"57.99","chg":"▼ −1.72%","dir":"down",
  "pts":[18,18,18,17,17,17,17,16,16,15]},
]
(C/"wire.json").write_text(json.dumps(wire,ensure_ascii=False,indent=1))

# ---- record: prepend 5 entries into the current top week ----
wk = record["weeks"][0]
assert "July 27" in wk["label"], wk["label"]
newent = [
 {"d":"diamonds","h":"De Beers narrows its half-year loss to $188 million as the rough index holds flat",
  "t":"Anglo American's interim results put De Beers revenue at $1.58 billion for the first half of 2026, down 19% year on year, with an underlying loss of $188 million, 23% narrower than a year earlier, and an underlying EBITDA loss of $113 million, 40% smaller. Sales volumes fell 20%. The consolidated average realised price fell 32% to $105 a carat on a lower-value sales mix and a rough price index 16% below last year, but the index barely moved within the half at 68 in the first quarter and 69 in the second. Unit costs fell 26% to $64 a carat, capital expenditure fell 33% to $115 million, and annual overheads are more than $100 million lighter than in 2024. The trading division swung to $30 million of underlying EBITDA from a $260 million loss. Anglo's chief executive said the sale process is in its final and most challenging phase and declined to name a buyer.",
  "s":"Rapaport / National Jeweler / JCK / Anglo American"},
 {"d":"gold-metals","h":"Gold ends July at $4,054.68, giving back the post-Fed rally on a dollar bounce",
  "t":"Spot gold fell about 1.19% to $4,054.68 an ounce on July 31 after prints earlier in the session held above $4,086, as the dollar rebounded from a six-week trough and traders booked the previous day's gains. Thursday had seen the metal crest $4,100 following the Federal Reserve's hold. Gold finished the month roughly 1.4% higher and is 20.57% up year on year. Silver fell 1.72% to $57.99, platinum 1.46% to $1,636 and palladium 1.53% to $1,288.50, putting the gold-silver ratio near 69.9. Fine gold at that level costs about $130 a gram before making charges.",
  "s":"Trading Economics / FXStreet / Yahoo Finance"},
 {"d":"gold-metals","h":"Second-quarter jewellery demand falls to 278 tonnes, the lightest since the pandemic",
  "t":"World Gold Council figures published on July 30 put global gold jewellery demand at 278 tonnes in the second quarter, down 17% year on year and the lowest quarterly volume since the pandemic, while the value of that demand rose 14% to $40 billion. Total demand was flat at 1,269 tonnes: bar and coin steady at 307 tonnes, central banks buying 289 tonnes in a sharp recovery from the first quarter, and exchange-traded funds shedding 45 tonnes. The quarter's average London price was $4,506.29 an ounce, roughly 10% above where gold traded at the end of July, and the first half set a record for the value of gold demand at $380 billion.",
  "s":"World Gold Council / Gulf News"},
 {"d":"retail-tech","h":"India's jewellery demand falls 15% to 75.1 tonnes as the value of the bill rises 50%",
  "t":"Indian gold jewellery demand fell to 75.1 tonnes in the second quarter from 88.8 tonnes a year earlier, a 15% decline by weight, while total Indian gold demand fell 6% and the value of that demand rose about 50% on record prices. Investment demand held up as jewellery gave way, the same split visible in the global figures. The context is a counter running on recycled metal and price-led revenue: Indian gold fell about 10% in June to a six-month low near 141,000 rupees per 10 grams, listed jewellers reported 30% to 60% revenue growth, old-gold trade-ins now fund up to 55% of counter sales, and June gem and jewellery exports rose 26.5% to $2.21 billion with gold jewellery up 54.5%.",
  "s":"World Gold Council / IBTimes India / KNN India"},
 {"d":"gemstones","h":"Gemfields lifts first-half auction revenue 72% to $102.9 million on emerald",
  "t":"Gemfields reported auction revenue of $102.9 million for the first half of 2026, up 72% year on year. Kagem in Zambia held premium emerald output, and its higher-quality rough auction in May took $26.8 million, selling 36 of 37 lots and 183,385 of 185,135 carats offered at an average $146.08 a carat. A mixed-quality ruby sale in February added $53 million from 121 of 135 lots. At Montepuez in Mozambique, premium-grade ruby recovery ran at 0.025 carats per tonne; the company is redirecting mining to higher-potential areas and has commissioned a new processing plant expected to reach full capacity later in 2026. Net debt stood at $44.2 million on June 30, before $33.3 million of auction receivables. Full results are due on September 25.",
  "s":"Rapaport / TipRanks / National Jeweler / Gemfields Group"},
]
wk["entries"] = newent + wk["entries"]
record["updated"] = "31 Jul 2026"
(C/"record.json").write_text(json.dumps(record,ensure_ascii=False,indent=1))
print("wire No.021 written; record top week now", len(wk["entries"]), "entries")
