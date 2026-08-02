#!/usr/bin/env python3
import json, pathlib
C = pathlib.Path("content")
wire = json.loads((C/"wire.json").read_text())
record = json.loads((C/"record.json").read_text())

wire["date_line"] = "Sunday, August 2, 2026"
wire["edition"] = "Vol. I — No. 023"
wire["tape_ts"] = "31 Jul 2026, 5pm New York close · Kitco · no session since; New York reopens Monday"
wire["items"] = [
 {"b":"NOBODY HAS DE BEERS YET","t":" — Anglo American chief executive Duncan Wanblad said the sale is in its final and most challenging phase, that the group is not exclusive with any consortium and still holds multiple active bidders, and that completion is targeted for the second half with regulatory approval about a year after signature"},
 {"b":"NO LISTING FOR DE BEERS","t":" — Wanblad ruled out a flotation on the view that the market lacks the capacity to absorb one, confirming a private sale; De Beers turned over $1.6 billion in the first half, down 19%, with an underlying EBITDA loss of $113 million narrowed from $189 million"},
 {"b":"ZERO PERCENT FOR ANTWERP","t":" — The Section 301 schedule in force since July 24 exempts loose natural diamonds cut in the European Union at 0%, along with rough and polished coloured stones and natural pearls, while lab-grown diamonds received no exemption from any of the roughly 60 countries listed"},
 {"b":"CENTRAL BANKS TAKE 289 TONNES","t":" — Official sector buying rose 62% year on year to 289 tonnes in the second quarter, a record for any second quarter, led by Poland at 51 tonnes and China at 33; the first half still totalled only 345 tonnes, the smallest since 2022, after a first quarter revised to 57"},
 {"b":"A $380 BILLION HALF-YEAR","t":" — Total gold demand was flat at 1,269 tonnes in the second quarter and up 2% at 2,522 tonnes across the half, but measured by value the first half set a record near $380 billion, with jewellery fabrication at a post-pandemic low of 278 tonnes"},
 {"b":"THE TENDER LADDER SPLITS","t":" — TAGS cleared 100% of a Zimbabwean parcel in Dubai and 95% of an Angolan sale worth $21.7 million, but only about 75% per tender on South African run-of-mine goods in Johannesburg, where participant attendance set a record; its latest Dubai sale of large South African stones took $15.2 million above 80%"},
 {"b":"NY NOW OPENS AT THE JAVITS","t":" — The summer market runs today to August 4, the first edition since Rockview Management Group bought the show from Emerald, with more than 70 new or returning exhibitors and over 90 brands from 19 countries across the Luxury Lifestyle and Curated sections"},
 {"b":"JEWELLERY TOPS A FLAT MARKET","t":" — Bain and Altagamma put personal luxury goods at €358 billion in 2025, down from €364 billion, and forecast €365 billion to €373 billion this year, growth of 2% to 4%, with jewellery named the strongest category in a total luxury market growing between nothing and 2%"},
 {"b":"GOLD WAITS ON PAYROLLS","t":" — No session since Friday's $4,041.70 close, so the tape carries unchanged into a week holding the ADP employment report midweek and non-farm payrolls on Friday; analysts mark the metal six weeks into a range, with near support at $4,020 and resistance at $4,070"},
]
wire["tape"] = [
 {"name":"Gold / oz","code":"XAU","px":"4,041.70","chg":"— unch.","dir":"flat",
  "pts":[16,16,15,15,15,14,15,16,15,14]},
 {"name":"Natural 1ct (RAPI proxy)","code":"NAT1","px":"5,232.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Lab-grown 1ct wholesale","code":"LGD1","px":"727.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Platinum / oz","code":"XPT","px":"1,644.00","chg":"— unch.","dir":"flat",
  "pts":[17,17,16,16,16,15,15,17,16,16]},
 {"name":"Silver / oz","code":"XAG","px":"57.44","chg":"— unch.","dir":"flat",
  "pts":[18,18,18,17,17,17,16,16,15,14]},
]
(C/"wire.json").write_text(json.dumps(wire,ensure_ascii=False,indent=1))

# ---- record: prepend entries into the current top week ----
wk = record["weeks"][0]
assert "July 27" in wk["label"], wk["label"]
newent = [
 {"d":"diamonds","h":"Anglo says no bidder holds exclusivity on De Beers, and rules out a listing",
  "t":"Duncan Wanblad, chief executive of Anglo American, said the De Beers disposal is in the final phases of its process and that this is also the most challenging phase because several parties must move together. He put completion in the second half of 2026, with regulatory approval taking roughly a year after signature. Wanblad said Anglo is not exclusive with any consortium and retains multiple active bidders, contradicting reports that the group assembled by former De Beers chief executive Gareth Penny had been selected as front-runner. He also ruled out a public listing, saying the market lacks the capacity to absorb a De Beers flotation, confirming that the exit will be a private sale with no continuing disclosure obligation. De Beers reported first-half revenue of $1.6 billion, down 19% year on year, and an underlying EBITDA loss of $113 million, narrowed from $189 million in the first half of 2025 on cost reductions rather than recovered demand. Reports in late July put a prospective sale near $1 billion with about $750 million payable up front.",
  "s":"National Jeweler / Rapaport / JCK"},
 {"d":"diamonds","h":"EU natural diamonds enter the US at zero percent while lab-grown pays everywhere",
  "t":"The Section 301 tariff schedule that took effect at midnight on July 24, 2026 applies duties of 10% to 12.5% to roughly 60 countries on forced-labour grounds, but exempts loose natural diamonds cut in the European Union at 0%, along with rough and polished coloured gemstones and natural pearls from the bloc. Lab-grown diamonds received no exemption from any listed country. Raw and semi-manufactured gold, silver, platinum and palladium are exempt from all 60. Karen Rentmeesters, chief executive of the Antwerp World Diamond Centre, said the exemption follows from there being no US mining or cutting industry to protect. Belgium exported $2.1 billion of polished diamonds to the United States in 2024. The Belgian flow has been repriced three times in eleven months: a 10% reciprocal duty from September 2025 until it was ruled unlawful in February, a 10% Section 122 surcharge from February to July 24, and the Section 301 schedule since. India, Canada, Mexico, Pakistan, Sri Lanka and the United Kingdom pay 10%; Angola, Australia, China, Colombia, Hong Kong, Israel, South Africa, Thailand, Turkey and the UAE pay 12.5%; Brazil carries 37.5%; Canadian polished diamonds face 50% separately from August 19.",
  "s":"Rapaport / National Jeweler"},
 {"d":"gold-metals","h":"Central banks buy 289 tonnes in a record second quarter, but the half is the weakest since 2022",
  "t":"The World Gold Council's Gold Demand Trends, published on 30 July 2026, put central bank net purchases at 289 tonnes in the second quarter, up 62% on the 177.9 tonnes bought a year earlier and a record for any second quarter. That was a fivefold increase on a first quarter revised down to 57 tonnes, leaving the first half at 345 tonnes, the smallest first half since 2022's 241 tonnes. The National Bank of Poland was the largest buyer at 51 tonnes, taking its half-year total to 82 tonnes against a self-set reserve target of about 700 tonnes. The People's Bank of China added 33 tonnes, its largest quarterly addition since the fourth quarter of 2023, lifting reported holdings to 2,346 tonnes. Uzbekistan took 16 tonnes, Kazakhstan 15, and Jordan and the Czech Republic 6 each. The Bank of Russia was the largest seller at 22 tonnes, attributed to a federal budget deficit, with Turkey selling 4 tonnes and reducing swaps from more than 80 to around 60, and the Bundesbank 1 tonne. The council's survey has 89% of reserve managers expecting official holdings to rise over the next twelve months.",
  "s":"World Gold Council"},
 {"d":"gold-metals","h":"Gold demand flat at 1,269 tonnes while the half-year sets a record $380 billion by value",
  "t":"Total gold demand in the second quarter of 2026 was unchanged year on year at 1,269 tonnes, and the first half reached 2,522 tonnes, up 2% on the same period of 2025. Measured by value rather than weight, the first half set a record of roughly $380 billion, the gap between the two measures being entirely the price. The composition was a substitution: central banks took 289 tonnes, up 62%, while jewellery fabrication fell to 278 tonnes, the weakest quarter since the pandemic, with Indian jewellery demand down 15% by weight to 75.1 tonnes even as the value of that demand rose about 50%. Gold closed July at $4,041.70 on the Kitco 5pm New York close, its first monthly gain since February, so the second half opens with a cost base above the average that produced the record first-half figure. No session has traded since; the tape carries unchanged into a week holding the ADP employment report midweek and non-farm payrolls on Friday.",
  "s":"World Gold Council / Kitco / City Index / FX Leaders"},
 {"d":"diamonds","h":"TAGS tenders clear between 75% and 100% depending on stone size",
  "t":"TAGS reported four summer tender outcomes that describe two different rough markets. A Zimbabwean parcel offered in Dubai in early June cleared 100%, with prices firm in higher qualities and slightly lower in the bottom ranges. An Angolan sale of stones 10.8 carats and above, drawing material from ten deposits plus the full run-of-mine output of one further seller, cleared 95% and realised $21.7 million. South African run-of-mine goods sold through June and July in Johannesburg cleared about 75% per tender despite record participant attendance. The most recent Dubai sale, of large South African production, cleared better than 80% and realised $15.2 million on extremely high attendance. The house said prices again exceeded the participating mines' expectations. The pattern places large sorted stones sold internationally at or near full clearance and smaller variable parcels, the segment most exposed to lab-grown competition, a quarter unsold.",
  "s":"Rapaport / TAGS"},
 {"d":"retail-tech","h":"NY Now opens under Rockview ownership as Bain names jewellery luxury's strongest category",
  "t":"NY Now's summer market opened at the Javits Center on August 2 and runs to August 4, the first edition since Rockview Management Group acquired the show from Emerald, with chief executive Dorothy Belshaw leading. More than 70 exhibitors are new or returning after a hiatus, and over 90 brands and makers from 19 countries are exhibiting. Fine jewellery sits in the Luxury Lifestyle section, carrying Brooke Gregson, Heather B. Moore, Bondeye Jewelry, Eden Presley, Carolina Neves, Dana Kellin and Annette Ferdinandsen, and in Curated for emerging designers; exhibitors include Dilamani, Hine Fine Jewelry, J Fields Jewelry, Jacob Keleher Jewelry, Lauren Newton Jewelry, Tacit Fine Jewelry, Jewels by Sanjam, Jessica Liu Designs and Yael Sonia. Attendance figures were not published. Separately, the spring Bain and Altagamma Luxury Goods Worldwide Market Study put personal luxury goods at €358 billion in 2025, down from €364 billion, and forecast €365 billion to €373 billion in 2026, growth of 2% to 4%, within a total luxury market of €1.44 trillion to €1.47 trillion growing between nothing and 2% at constant rates. Jewellery was named the strongest category, with US luxury brands up 10% to 15% year on year in the first quarter, Europe the weak link on tourism, China recovering slowly and Japan slowing.",
  "s":"National Jeweler / InStore / Gifts & Decorative Accessories / Bain & Company / GJEPC Solitaire / WWD"},
]
wk["entries"] = newent + wk["entries"]
record["updated"] = "2 Aug 2026"
(C/"record.json").write_text(json.dumps(record,ensure_ascii=False,indent=1))
print("wire No.023 written; record top week now", len(wk["entries"]), "entries")
