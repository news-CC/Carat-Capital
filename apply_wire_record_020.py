#!/usr/bin/env python3
import json, pathlib
C = pathlib.Path("content")
wire = json.loads((C/"wire.json").read_text())
record = json.loads((C/"record.json").read_text())

wire["date_line"] = "Thursday, July 30, 2026"
wire["edition"] = "Vol. I — No. 020"
wire["tape_ts"] = "30 Jul 2026, European session · gold recovers the Fed"
wire["items"] = [
 {"b":"ONE BILLION FOR DE BEERS","t":" — Bloomberg puts the Gareth Penny consortium's price for Anglo American's 85% stake at about $1 billion: roughly $750 million on closing and $250 million deferred, with some $500 million of working capital going in behind it, against a book value of about $2.3 billion earlier this year"},
 {"b":"GOLD TAKES BACK $4,075","t":" — Spot recovered to about $4,074.98 an ounce, up 0.22% on the day and 23.84% on the year, erasing Wednesday's post-FOMC slip to $4,029; the market unwound a hawkish hold with three dissents in a single session"},
 {"b":"PLATINUM JUMPS 1.62%","t":" — Platinum rose to $1,628.20 an ounce and palladium 2.51% to $1,284.00, reversing Wednesday's cooling; platinum is 26.13% higher year on year with a fourth straight annual supply deficit still forecast"},
 {"b":"NINETY-FIVE PERCENT IN LUANDA","t":" — TAGS cleared 95% of a Luanda tender of rough above 10.8 carats and called it a return to near normal trading, while Sodiam's seventeenth auction took about $21.7 million net from 6,586.89 carats, 23.46% above expected value"},
 {"b":"HERITAGE BOOKS $1.41 BILLION","t":" — First-half sales rose 47% to more than $1.41 billion, the highest midyear total in the firm's fifty years; its May 4 jewelry auction made $9,713,640, led by a 6.59-carat Kashmir sapphire at $906,250"},
 {"b":"FOUR SWISS GROUPS IN THE BLACK","t":" — Morgan Stanley's second-quarter secondary index rose 1.5% and all four groups it tracks are positive year on year for the first time since early 2022, Swatch Group up 5.4% and Richemont 4.2%"},
 {"b":"PLATINUM LOSES ITS TEACHER","t":" — Platinum Guild International USA announced that senior vice president Kevin Reilly retired at the end of June after twenty years there and thirty-nine in the trade; global platinum jewellery demand is forecast to contract 6% in 2026"},
 {"b":"THE SHOP THAT WAS NEVER THERE","t":" — AI-built jewellery storefronts are running fabricated closing-down and bereavement sales at 80% to 90% off with scraped product photography and synthetic voiceovers; buyers report receiving resin, plastic and plated metal, or nothing"},
 {"b":"COLOR RUNS TWO SPEEDS","t":" — ICA members report colored-stone demand roughly 30% below 2022 even as Mahenge spinel holds a 150% post-pandemic gain and Mozambican Paraiba trades at $10,000 to $12,000 a carat; tsavorite has given back 15% to 20% in a year"},
]
wire["tape"] = [
 {"name":"Gold / oz","code":"XAU","px":"4,074.98","chg":"▲ +0.22%","dir":"up",
  "pts":[16,16,15,15,15,14,14,15,16,16]},
 {"name":"Natural 1ct (RAPI proxy)","code":"NAT1","px":"5,232.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Lab-grown 1ct wholesale","code":"LGD1","px":"727.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Platinum / oz","code":"XPT","px":"1,628.20","chg":"▲ +1.62%","dir":"up",
  "pts":[17,17,16,16,16,15,15,15,16,17]},
 {"name":"Silver / oz","code":"XAG","px":"57.79","chg":"▼ −0.25%","dir":"down",
  "pts":[18,18,18,17,17,17,17,16,16,16]},
]
(C/"wire.json").write_text(json.dumps(wire,ensure_ascii=False,indent=1))

# ---- record: prepend 5 entries into the current top week ----
wk = record["weeks"][0]
assert "July 27" in wk["label"], wk["label"]
newent = [
 {"d":"diamonds","h":"Anglo's price for De Beers comes in at about $1 billion",
  "t":"Bloomberg reported on July 29 that the Global Diamond Consortium, led by former De Beers chief executive Gareth Penny and including the governments of Namibia and Angola, would pay about $1 billion for Anglo American's 85% stake: roughly $750 million on closing and $250 million deferred, plus some $500 million of working capital injected into the business. De Beers carried a book value of about $2.3 billion earlier this year after $3.5 billion of write-downs, against a $17.6 billion valuation at the 2001 take-private. Botswana holds the remaining 15%. Terms are not final; Anglo still expects to close by the end of 2026.",
  "s":"Bloomberg / Rapaport / JCK"},
 {"d":"gold-metals","h":"Gold recovers to $4,074.98 the day after the Fed's hawkish hold",
  "t":"Spot gold rose about 0.22% to $4,074.98 an ounce on July 30, roughly $46 above Wednesday's post-FOMC level of $4,029 and back inside its pre-meeting range; the metal is 23.84% higher year on year. Silver eased 0.25% to $57.79 from $57.94 and the gold-silver ratio widened to 70.37 from 70.22. Central-bank buying of 244 tonnes in the first quarter and 41 tonnes in May continues to underpin the dips.",
  "s":"Trading Economics / FXStreet"},
 {"d":"gold-metals","h":"Platinum jumps 1.62% to $1,628.20 as Kevin Reilly retires from PGI USA",
  "t":"Platinum rose 1.62% to $1,628.20 an ounce, up 1.77% on the month and 26.13% year on year, with palladium 2.51% higher at $1,284.00 — a reversal of Wednesday's cooling in the white metals. Analysts still forecast a fourth consecutive annual supply deficit; January's all-time high was $2,923.70. Against that, global platinum jewellery demand is expected to contract about 6% in 2026, led by China, with India facing tariff headwinds. Platinum Guild International USA announced on July 28 that senior vice president Kevin Reilly had retired at the end of June after twenty years there and a thirty-nine-year career, having established platinum programmes at GIA, Pratt, SCAD, RISD, the 92Y Jewelry Center and the Miami Jewelry School.",
  "s":"Trading Economics / National Jeweler / JCK"},
 {"d":"auctions","h":"Heritage books a record $1.41 billion half and its largest jewelry sale ever",
  "t":"Heritage Auctions took more than $1.41 billion in the first six months of 2026, up 47% year on year and the highest midyear total in its fifty-year history. Its Spring Fine Jewelry Signature auction on May 4 realised $9,713,640, the highest-grossing jewelry auction in the firm's history, beating the $9.2 million set in September 2025. The top lot was a platinum ring set with a 6.59-carat octagonal Kashmir sapphire at $906,250, more than $300,000 above its high estimate. Across the majors, first-half global sales at Christie's, Sotheby's and Phillips rose 70% to $6.8 billion with fees, with Sotheby's alone at a record $4.4 billion.",
  "s":"ARTnews / Intelligent Collector / National Jeweler / The Art Newspaper"},
 {"d":"watches","h":"All four Swiss groups turn positive year on year for the first time since early 2022",
  "t":"Morgan Stanley's second-quarter index of Swiss watch secondary-market prices rose 1.5%, and all four groups it tracks are now positive year on year for the first time since early 2022: Swatch Group up 5.4% and Richemont up 4.2%. Sequentially in the quarter, Richemont gained 1.3% and Swatch 1.0%. April had been the market's best single month since March 2022 at plus 2.5% on the WatchCharts overall index, ahead of Watches and Wonders, before dealer supply reached record levels and demand lagged through May and June.",
  "s":"Morgan Stanley via ScrewDownCrown / WatchCharts"},
]
wk["entries"] = newent + wk["entries"]
record["updated"] = "30 Jul 2026"
(C/"record.json").write_text(json.dumps(record,ensure_ascii=False,indent=1))
print("wire No.020 written; record top week now", len(wk["entries"]), "entries")
