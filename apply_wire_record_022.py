#!/usr/bin/env python3
import json, pathlib
C = pathlib.Path("content")
wire = json.loads((C/"wire.json").read_text())
record = json.loads((C/"record.json").read_text())

wire["date_line"] = "Saturday, August 1, 2026"
wire["edition"] = "Vol. I — No. 022"
wire["tape_ts"] = "31 Jul 2026, 5pm New York close · Kitco · markets shut for the weekend"
wire["items"] = [
 {"b":"RUSSIA BANS THE WORD","t":" — Government Resolution No. 657, signed May 30 and in force September 1, prohibits the word diamond and its derivatives for synthetic stones sold in Russia; tags must read synthetic or Synth., and weight must be shown in grams because carat weight is banned outright"},
 {"b":"NATURAL, REAL, ECO-FRIENDLY STRUCK","t":" — The same resolution removes precious, real, genuine, natural, mined, mineral and eco-friendly from all consumer-facing description of man-made stones, in store and online, along with the colour and clarity descriptors borrowed from natural grading"},
 {"b":"GOLD CLOSES JULY HIGHER","t":" — Kitco's 5pm close put spot at $4,041.70, down $60.90 or 1.48% on the session, but July finished about 0.5% up, gold's first monthly gain since February and the end of a four-month losing run; the metal is 20.22% higher year on year"},
 {"b":"PALLADIUM DOWN 3.38%","t":" — The white metals fell harder than gold on the last session of July: palladium $1,256.00, silver $57.44 and platinum $1,644.00, putting the gold-silver ratio near 70.4 and platinum at roughly 41% of the gold price"},
 {"b":"DUBAI BOOKS OCTOBER 26","t":" — DMCC will hold the second Dubai Diamond Week from October 26 to 29 with the Italian Exhibition Group co-hosting a sourcing show, after the emirate traded a record $41.7 billion and 359.5 million carats in 2025, 95.8% of the value in natural stones"},
 {"b":"HERMÈS HOLDS WATCHES FLAT","t":" — First-half watch revenue was €269 million, down 4.2% as published but up 0.2% at constant rates, with the second quarter up 4.4%; jewellery and home took €1.065 billion, up 5.4%, on group revenue of €8.2 billion and a 41.0% operating margin"},
 {"b":"BUCHERER GETS FIFTH AVENUE","t":" — Rolex's own retailer confirmed it will operate the Manhattan flagship, reported by WatchPro at 43,000 square feet over four floors in a David Chipperfield building, more than four times the size of the current largest Rolex showroom in Dubai"},
 {"b":"SIXTY DOORS FOR FRIENDSHIP DAY","t":" — De Beers India is running the second edition of Love, from Bestie today and tomorrow across 60 retail partner stores in nine cities, built on four paired natural diamond bracelets, against Indian jewellery demand that fell 15% by weight in the second quarter"},
 {"b":"A DOLLAR IN, FIFTEEN OUT","t":" — Sy Kessler launched a watch battery starter kit listing from $235 on the arithmetic that the average cell costs about $1 and the job sells for more than $15, one of the few counter lines priced on skill rather than on spot"},
]
wire["tape"] = [
 {"name":"Gold / oz","code":"XAU","px":"4,041.70","chg":"▼ −1.48%","dir":"down",
  "pts":[16,16,15,15,15,14,15,16,15,14]},
 {"name":"Natural 1ct (RAPI proxy)","code":"NAT1","px":"5,232.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Lab-grown 1ct wholesale","code":"LGD1","px":"727.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Platinum / oz","code":"XPT","px":"1,644.00","chg":"▼ −0.60%","dir":"down",
  "pts":[17,17,16,16,16,15,15,17,16,16]},
 {"name":"Silver / oz","code":"XAG","px":"57.44","chg":"▼ −2.45%","dir":"down",
  "pts":[18,18,18,17,17,17,16,16,15,14]},
]
(C/"wire.json").write_text(json.dumps(wire,ensure_ascii=False,indent=1))

# ---- record: prepend 5 entries into the current top week ----
wk = record["weeks"][0]
assert "July 27" in wk["label"], wk["label"]
newent = [
 {"d":"diamonds","h":"Russia bans the word diamond for synthetic stones from September 1",
  "t":"Russian Government Resolution No. 657, signed on May 30 and taking effect on September 1, 2026, prohibits the word diamond and all its derivatives in consumer-facing descriptions of synthetic stones sold in Russia. Tags must carry the word synthetic or the abbreviation Synth., and the approved term is cut synthetic diamond. The words precious, real, genuine, natural, mined, mineral and eco-friendly are struck from all consumer information, along with colour and clarity descriptors borrowed from natural grading. Weight must be given in grams; carat weight is prohibited for synthetics, making a one-carat stone a 0.2 gram stone. Tags must also carry product name, maker or importer, country of origin, model number, total weight, metal and fineness, stone particulars and a unique identification number matching a two-dimensional barcode. Deputy finance minister Alexey Moiseev said the aim is to improve transparency and protect consumers. CIBJO is expected to mandate the same single term at its September 4 congress.",
  "s":"Alrosa / Rapaport / Solitaire GJEPC / The Retail Jeweller India"},
 {"d":"gold-metals","h":"Gold closes July at $4,041.70, its first monthly gain since February",
  "t":"Kitco's 5pm New York close on July 31 put spot gold at $4,041.70 an ounce, down $60.90 or 1.48% on the session, the weakest day of the week, as the dollar rebounded from a six-week low and traders unwound the rally that followed the Federal Reserve's hold. Across July the metal still finished about 0.5% higher, its first monthly gain since February and the end of a four-month losing run. Trading Economics puts gold 20.22% above a year earlier. The white metals fell harder: silver $57.44, down 2.45%, platinum $1,644.00, down 0.60%, and palladium $1,256.00, down 3.38%, putting the gold-silver ratio near 70.4 and platinum at roughly 41% of the gold price. From this edition the tape carries the Kitco 5pm close as its single reference point, replacing mixed intraday prints.",
  "s":"Kitco / Kitco News / CNBC / Trading Economics"},
 {"d":"diamonds","h":"DMCC sets the second Dubai Diamond Week for October 26 to 29",
  "t":"DMCC will hold the second edition of Dubai Diamond Week from October 26 to 29, 2026, four days of conference sessions alongside a sourcing exhibition co-hosted with the Italian Exhibition Group, with governments, producers, manufacturers, retailers, traders, investors and technology firms invited. Dubai's diamond trade reached a record $41.7 billion and 359.5 million carats in 2025, with natural stones accounting for 95.8% of traded value, and the Dubai Diamond Exchange now anchors an ecosystem of close to 1,400 companies and the largest tender facility in the business. The event follows a year in which the 41st World Diamond Congress met in Dubai, Okavango Diamond Company signed a tender arrangement with the exchange, and Qatar's new bourse joined the World Federation of Diamond Bourses.",
  "s":"DMCC / Solitaire GJEPC / Arabian Business / InStore"},
 {"d":"watches","h":"Hermès holds watches flat at €269 million while jewellery and home grow 5.4%",
  "t":"Hermès reported first-half 2026 watch revenue of €269 million, down 4.2% as published but up 0.2% at constant exchange rates, with second-quarter watch sales of €134 million up 3.0% published and 4.4% at constant rates. Other Hermès sectors, the segment carrying jewellery and home, took €1.065 billion in the half, up 0.8% published and 5.4% at constant rates, with the second quarter up 4.0%. Group revenue was €8.2 billion, up 6.1% at constant rates, with recurring operating income of €3.4 billion, an operating margin of 41.0% and net profit of €2.2 billion. The Americas grew 15.3% at constant rates and Japan 11.0%, while the Middle East fell 4.2%. Separately, Bucherer confirmed it will operate Rolex's Fifth Avenue flagship in Manhattan, reported by WatchPro at 43,000 square feet over four floors.",
  "s":"Hermès / Retail Insight Network / WatchPro / JCK"},
 {"d":"retail-tech","h":"De Beers India runs Friendship Day across 60 stores as tonnage falls 15%",
  "t":"De Beers India launched the second edition of its Love, from Bestie campaign for Friendship Day, running August 1 and 2 across 60 retail partner stores including Forevermark outlets in Mumbai, Delhi, Bengaluru, Chennai, Pune, Kanpur, Kochi, Coimbatore and Nagpur. The collection is four natural diamond bracelet designs made to be worn in pairs, including a signature piece spelling BFF in Morse code with baguette and round stones, supported by a three-station in-store experience. The backdrop is Indian jewellery demand down 15% by weight in the second quarter, to 75.1 tonnes from 88.8 tonnes, with the value of that demand up about 50% on record gold prices. Separately, supplier Sy Kessler launched a watch battery starter kit from $235 on the arithmetic that a cell costs about $1 and the job sells for more than $15.",
  "s":"The Retail Jeweller India / Medianews4u / Business Standard / JCK"},
]
wk["entries"] = newent + wk["entries"]
record["updated"] = "1 Aug 2026"
(C/"record.json").write_text(json.dumps(record,ensure_ascii=False,indent=1))
print("wire No.022 written; record top week now", len(wk["entries"]), "entries")
