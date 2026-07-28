#!/usr/bin/env python3
import json, pathlib
C = pathlib.Path("content")
wire = json.loads((C/"wire.json").read_text())
record = json.loads((C/"record.json").read_text())

wire["date_line"] = "Tuesday, July 28, 2026"
wire["edition"] = "Vol. I — No. 018"
wire["tape_ts"] = "28 Jul 2026, into the New York open · Fed decides Wed. (July 29)"
wire["items"] = [
 {"b":"GOLD IDLES BEFORE THE FED","t":" — Spot held near $4,046 an ounce in a tight $4,021–$4,080 triangle on the eve of the decision; CME FedWatch shows a 62% chance of a hold at 3.50–3.75% and 38% of a hike, with GDP and core PCE (near 3.3%) due Thursday"},
 {"b":"TITAN MAKES IT THREE","t":" — Titan Company's June quarter revenue rose about 41%, a third straight quarter above 40%; the Tanishq-led jewellery arm gained 39%, watches 23%, eyewear 23% and the small international business 128%"},
 {"b":"WATCH TRADE SUES OVER TARIFFS","t":" — California retailer Collective Horology, with Burlap & Barrel and the Liberty Justice Center, challenged the Section 301 duties at the US Court of International Trade; Swiss watches have run at least 12.5% dearer since April 2025 and it is owed $164,000 in vacated IEEPA refunds"},
 {"b":"QATAR OPENS A DIAMOND EXCHANGE","t":" — The Qatar Free Zones Authority launched the Qatar Diamond Exchange at Ras Bufontas, a Kimberley-compliant hub offering sorting, independent valuation, vaulting and rough and polished tenders, and a Gulf rival to Dubai"},
 {"b":"THREE FANCIES, NO RESERVE","t":" — Bonhams' 300-lot California sale on July 28 offers unmounted fancy pink-purple, deep-pink and blue diamonds estimated near $35,000–$50,000, and a 70-carat diamond necklace with no reserve; Van Cleef & Arpels, Graff and Boucheron feature"},
 {"b":"THE BOOK BENDS TO RUBY","t":" — GemGuide raised Mozambique ruby prices sharply on demand for untreated goods and scrapped its 1–10 scale for Burma stones, pricing only four grades as fine Mogok material grows too scarce to chart"},
 {"b":"IIJS FILLS EARLY","t":" — GJEPC's IIJS Premiere returns to Mumbai on August 6–10 with pre-registration past 25,000 and the first deadline extended, landing as June gems-and-jewellery exports jumped 26.5% to about $2.21 billion"},
 {"b":"WHITE METALS RUN","t":" — Palladium jumped about 3.3% to roughly $1,268 and platinum 1.7% to about $1,612 on Monday, while silver held near $58.50 with $60 back in view after an intraday $60.11 earlier in the month"},
 {"b":"SMALL STONES STILL FIRM","t":" — The recovery in 0.30–0.69ct rounds continued in Rapaport's latest market comment, with steady US demand and trimmed inventories supporting prices into IIJS and the wedding season"},
]
wire["tape"] = [
 {"name":"Gold / oz","code":"XAU","px":"4,046.00","chg":"— easing before the Fed","dir":"flat",
  "pts":[16,16,15,15,16,15,15,14,14,14]},
 {"name":"Natural 1ct (RAPI proxy)","code":"NAT1","px":"5,232.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Lab-grown 1ct wholesale","code":"LGD1","px":"727.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Platinum / oz","code":"XPT","px":"1,610.00","chg":"▲ +1.70%","dir":"up",
  "pts":[13,13,14,14,15,15,16,16,17,17]},
 {"name":"Silver / oz","code":"XAG","px":"58.40","chg":"— $60 in view","dir":"flat",
  "pts":[17,17,17,18,18,18,17,18,18,18]},
]
(C/"wire.json").write_text(json.dumps(wire,ensure_ascii=False,indent=1))

# ---- record: prepend 5 entries into the current top week ----
wk = record["weeks"][0]
assert "July 27" in wk["label"], wk["label"]
newent = [
 {"d":"gold-metals","h":"Gold idles near $4,046 on the eve of the Fed decision",
  "t":"Spot gold traded in a tight $4,021–$4,080 range into the July 28–29 FOMC, with CME FedWatch pricing a 62% chance of a hold at 3.50–3.75% and 38% of a quarter-point hike, and roughly 81% odds of a September move. Second-quarter GDP, personal income and spending, and core PCE near 3.3% follow on Thursday. Palladium jumped ~3.3% and platinum ~1.7% on Monday; silver held near $58.50 with $60 in view.",
  "s":"FX Leaders / Kitco"},
 {"d":"retail-tech","h":"Titan's June quarter revenue rises about 41% — a third straight 40%-plus",
  "t":"Titan Company reported roughly 41% revenue growth for the quarter to June 2026, its third consecutive quarter above 40%. The jewellery division (Tanishq, Mia, CaratLane) grew about 39% with plain and studded each up in the mid-thirties and strong coin demand; watches rose 23% (analogue high-twenties, smart watches down low-teens), eyewear 23%, emerging businesses 19% and the international business 128%. Buyer growth was in the early double digits while average ticket sizes rose in the high double digits amid stable gold prices.",
  "s":"Goodreturns / Indian Retailer"},
 {"d":"watches","h":"Collective Horology takes the US tariffs to the Court of International Trade",
  "t":"The California watch retailer, joined by spice importer Burlap & Barrel and backed by the Liberty Justice Center, sued to challenge the Section 301 duties, arguing the US Trade Representative applied a near-uniform tariff across dozens of countries without the country-by-country analysis the 1974 Trade Act requires. Swiss watch imports have run at least 12.5% more expensive since April 2025; Collective says it is owed more than $164,000 in refunds from the vacated IEEPA tariffs, on top of Section 122 and 301 duties paid.",
  "s":"WatchPro"},
 {"d":"diamonds","h":"Qatar launches its first diamond exchange at Ras Bufontas",
  "t":"The Qatar Free Zones Authority launched the Qatar Diamond Exchange, a Kimberley Process-compliant hub near Doha offering trading licences, on-site sorting and independent valuation, secure vaulting, specialist insurance and participation in rough and polished tenders. Qatar became a full KP member in 2021 and in 2025 named the free-zone authority the sole authorized entry and exit point for rough. CEO Sheikh Mohammed Bin Hamad Bin Faisal Al-Thani framed it as bringing the full value chain into one regulated ecosystem — a Gulf rival to Dubai's record $41.7 billion 2025 trade.",
  "s":"Rapaport / Euronews"},
 {"d":"gemstones","h":"GemGuide lifts Mozambique ruby prices and regrades Burma stones",
  "t":"The colored-stone pricing service raised Mozambique ruby prices sharply on strong demand for unenhanced, untreated material sold by tender, and abandoned its traditional one-to-ten scale for unenhanced Burmese ruby, pricing only four grades — Middle Commercial, Lower Good, Upper Fine and Upper Extra Fine. Research director Stuart Robertson said fine Mogok material is now so scarce that availability matters more than price. The revisions are live in the app and appear in the July–August issue.",
  "s":"National Jeweler"},
]
wk["entries"] = newent + wk["entries"]
record["updated"] = "28 Jul 2026"
(C/"record.json").write_text(json.dumps(record,ensure_ascii=False,indent=1))
print("wire No.018 written; record top week now", len(wk["entries"]), "entries")
