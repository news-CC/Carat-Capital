#!/usr/bin/env python3
# Edition No. 041 - 2026-08-22. Wire tape + wire items + record entries.
import json, pathlib
C = pathlib.Path("content")
wire = json.loads((C/"wire.json").read_text())
record = json.loads((C/"record.json").read_text())

wire["date_line"] = "Saturday, August 22, 2026"
wire["edition"] = "Vol. I — No. 041"
wire["tape_ts"] = ("Friday 21 Aug 2026, last print · Kitco, corroborated on TradingEconomics · "
                   "Editor re-read at press time 22 August and confirmed unchanged; no weekend session exists")

# Press-time re-read on 22 August returned Kitco's Friday last print unchanged from the 05:00 tape
# (gold $4,602.40, silver $68.86), so nothing is written back. Platinum and palladium stay held.
TAPE = {
 "XAU": ("4,602.40", "▲ +0.45%", "up",   [26,24,22,26,25,23,22,26,28,29]),
 "XAG": ("68.86",    "▼ −0.65%", "down", [23,25,22,23,26,25,19,26,28,27]),
 "XPT": ("1,881.00", "— unch.",  "flat", [22,21,18,20,23,22,19,24,27,27]),
}
for t in wire["tape"]:
    if t["code"] in TAPE:
        px, chg, d, pts = TAPE[t["code"]]
        t["px"], t["chg"], t["dir"], t["pts"] = px, chg, d, pts
# NAT1 and LGD1 are locked by build.py to prices.json / lab-prices.json and are left alone.

wire["items"] = [
 {"b":"GOLD BREAKS $4,550 IN BEIJING AND ADDS $47.96 MORE BY NEW YORK",
  "t":"Eastmoney timestamped spot gold at $4,554.441 at 14:51 Beijing on 21 August, up 0.8%. Friday's last New York print, this paper's mark of record, is $4,602.40. Same session, ten hours apart. Drivers named: a repo expansion from $20bn to $40bn, falling long-end yields and US debt past $40 trillion."},
 {"b":"THE EDITOR RE-READ THE TAPE AT PRESS TIME AND WROTE NOTHING BACK",
  "t":"Saturday has no spot session. Kitco returned Friday's last print unchanged at gold $4,602.40 and silver $68.86, so the 05:00 marks stand. Gold is up $20.80 or 0.45% on this paper's 21 August mark; silver is down $0.45 or 0.65%, the only metal lower."},
 {"b":"PLATINUM AND PALLADIUM STAY HELD ON A TWO-PAGE GAP OF 1.00% AND 1.47%",
  "t":"Kitco read $1,877.00 and $1,331.00 at press time, TradingEconomics $1,895.70 and $1,350.50. Both gaps are outside the band gold and silver cleared at 0.11%, so the last agreed marks of $1,881.00 and $1,336.00 carry unch. Both held marks sit inside today's live range."},
 {"b":"CHOW SANG SANG'S COUNTER HAS ADDED 80 YUAN A GRAM IN THIRTEEN DAYS",
  "t":"Eastmoney carries the brand's pure gold jewellery at 1,365 yuan a gram, up 6 after 46 the day before. This paper recorded the same counter at 1,285 yuan on 8 August. That is 6.23% passed through to the Chinese shopper in under a fortnight."},
 {"b":"INDIA'S JULY GOLD IMPORTS MORE THAN DOUBLE TO $4.16 BILLION",
  "t":"The World Gold Council puts July at $4.16bn against June's $1.97bn, with volumes at 40 to 45 tonnes against 20 and MCX turning over 14.9 tonnes a day. The ETF leg went the other way: net inflows of INR15.6bn, 55% lower month on month."},
 {"b":"THREE GOOD DELIVERY NOTICES IN SEVENTEEN DAYS, ALL OF THEM CHINESE",
  "t":"Shandong Gold Smelting came off both LBMA lists on 5 August after a US forced-labour entity listing. Shenzhen Zhonghenglong joined the gold list on 17 August. Hunan Shuikoushan came off the silver list on 21 August after a modified assurance opinion. Neither suspension concerns a failed assay."},
 {"b":"YORAM DVASH TAKES THE CHAIR AT THE COMPANY THAT SELLS 30% OF DEBSWANA",
  "t":"Okavango Diamond Company named the former WFDB president board chairman, reported 20 August, filling a seat empty since November. Under the February 2025 sales agreement ODC takes 30% of Debswana's rough for five years and 40% for the next five. No figures accompanied the announcement."},
 {"b":"VASANT MEHTA, GJEPC CHAIRMAN FROM 2008 TO 2010, HAS DIED AT 81",
  "t":"He was the council's vice chairman in 1991-92 and again in 2006-08, and convened its banking, insurance and taxation committee for years afterwards. He represented India at the World Diamond Council, WFDB, IDMA, CIBJO and the Kimberley Process."},
 {"b":"MINISO GROWS 53% AND TAKES THE TOP OF NRF'S HOT 25",
  "t":"Kantar's ranking of US domestic sales growth from 2024 to 2025 puts Miniso first, Dick's Sporting Goods second at 49% after buying Foot Locker, then Daiso at 26%, Primark at 24% and Five Below at 23%. Every name in the top five is a value format."},
]
(C/"wire.json").write_text(json.dumps(wire, indent=1, ensure_ascii=False))

ENTRIES = [
 {"d":"gold-metals",
  "h":"Gold's mark of record holds at $4,602.40 as the Editor's press-time re-read returns Friday's print unchanged",
  "t":"22 August 2026 is a Saturday and no spot session exists. Under the one-price rule the Editor re-read the metals at press time on Kitco, the board carrying this tape, and returned Friday 21 August's last print unchanged: gold $4,602.40 an ounce and silver $68.86. Nothing was written back and the 05:00 marks stand. Against this paper's 21 August marks of record, gold is up $20.80 or 0.45% and silver is down $0.45 or 0.65%, the only metal lower on the session. Second page, TradingEconomics, read gold at $4,607.35, a gap of $4.95 or 0.11%, inside the band this tape treats as agreement. Platinum and palladium remain held at $1,881.00 and $1,336.00: Kitco read $1,877.00 and $1,331.00 at press time against TradingEconomics at $1,895.70 and $1,350.50, gaps of $18.70 or 1.00% and $19.50 or 1.47%, both outside the agreement band, and both held marks sit inside the live range rather than outside it. This desk's arithmetic: the gold-to-silver ratio reads 66.84 against 66.10 on 21 August marks, 0.74 points wider, because silver fell while gold rose; at 31.1035 grams to the troy ounce the four marks work out at $147.97, $2.21, $60.48 and $42.95 a gram."},
 {"d":"gold-metals",
  "h":"Spot gold broke $4,550 on the Beijing afternoon and closed New York $47.96 higher still",
  "t":"Eastmoney, timestamped 14:51 Beijing on 21 August 2026, reported international spot gold breaking through $4,550 an ounce and trading at $4,554.441, up 0.8%, with COMEX futures at $4,598.4, up 0.59%. The drivers it names are the US Treasury's expansion of its liquidity-support repurchase operations from $20 billion to $40 billion, falling long-end Treasury yields, a weaker dollar, a repricing of fiscal risk, visible policy disagreement inside the Federal Reserve, and US federal debt passing $40 trillion. The Beijing timestamp is 02:51 in New York, roughly ten hours before Friday's last print, and this paper's own mark of record for the same session is $4,602.40, which is $47.96 or 1.05% higher, this desk's arithmetic on the two published readings. The two figures are the same rally at different hours and not a source disagreement. Eastmoney also carried Chow Sang Sang's pure gold jewellery at 1,365 yuan a gram, up 6 yuan after a 46-yuan rise the previous day; this paper reported the same counter at 1,285 yuan on 8 August 2026, so 80 yuan a gram or 6.23% has been passed to the Chinese shopper in thirteen days. A single-source Gulf leg is carried and labelled: Ghorba News, dated in its own text to Friday 21 August, put UAE retail gold at 538.46 dirhams a gram for 24 karat, 493.59 for 22, 471.15 for 21 and 403.84 for 18. Divided by the 24-karat rate those give 0.9167, 0.8750 and 0.7500 to four decimals, the exact fineness ratios, so the four figures are one struck rate stepped down by purity rather than four quoted markets; at the dirham's pegged 3.6725 the 24-karat rate is $146.62 a gram against $147.97 derived from this paper's own mark."},
 {"d":"gold-metals",
  "h":"India's July gold imports more than doubled to $4.16 billion while ETF inflows fell 55%",
  "t":"The World Gold Council's India gold market update, published 19 August 2026, puts July gold imports at $4.16 billion against $1.97 billion in June, a rise of 111% on this desk's arithmetic, with volumes estimated at 40 to 45 tonnes against 20 tonnes in June. The council attributes the rebound to June's price correction bringing consumers back to the counter and retailers restocking ahead of the September-October festival season. MCX futures averaged 14.9 tonnes of daily turnover in July. The investment leg moved the other way: net inflows into Indian gold ETFs were INR15.6 billion, about $163 million, which the council states was 55% lower month on month on Association of Mutual Funds of India data, while holdings rose one tonne to 120 tonnes and 57,000 new folios took total accounts to 12.53 million. The first two weeks of August added INR11.79 billion, about $124 million. The council marks the international benchmark up 9% in the first two weeks of August to $4,391 an ounce and Indian domestic prices up nearly 7% to INR151,744 per 10 grams; this paper's own mark of record on 22 August is $4,602.40, a further $211.40 or 4.81% above the level the report describes, so the restock window it documents has already closed at a higher price."},
 {"d":"gold-metals",
  "h":"Three LBMA Good Delivery notices in seventeen days, every one of them a Chinese refiner",
  "t":"Three changes to the London Bullion Market Association's Good Delivery Lists between 5 and 21 August 2026 all concern Chinese refiners and run in both directions. Shandong Gold Smelting was suspended from both the gold and silver lists with effect from 5 August, as an interim measure after the association invoked its incident review process following the company's addition to the United States Uyghur Forced Labor Prevention Act entity list, with the investigation still to conclude. Shenzhen Zhonghenglong Industrial was added to the gold list with effect from 17 August, having met the association's tests on ownership, history, production capability and financial standing plus independent assay of its bars and its own assaying capability; the company was founded in March 1997, refines gold, silver, platinum and palladium from recovery and purification streams, and in 2007 became the first private enterprise approved as a Good Delivery gold refiner by the Shanghai Gold Exchange. Hunan Shuikoushan Nonferrous Metals Group, known as SKS, was suspended from the silver list with effect from 21 August, announced 20 August, following a modified assurance opinion issued by SLR Consulting for its FY2025 Responsible Silver compliance reporting. The association's current lists, read on 22 August 2026, show 67 accredited gold refiners and 86 silver refiners. Neither suspension alleges a bar that failed assay; one turns on a foreign entity listing and one on an audit opinion."},
 {"d":"diamonds",
  "h":"Okavango Diamond Company names Yoram Dvash board chairman",
  "t":"Okavango Diamond Company, Botswana's state-owned rough trading arm, has appointed Yoram Dvash chairman of its board, reported 20 August 2026. He succeeds Gape Kaboyakgosi, who left in November after five years, so the seat had been vacant for most of a year. Dvash stepped down as president of the World Federation of Diamond Bourses two months earlier, having held that office since 2020 and completed the maximum two consecutive three-year terms, and he remains chairman of both the Israel Diamond Institute and the Israel Diamond Exchange. He said he looks forward to working with the board, management and the government of Botswana. Under the ten-year sales agreement signed with De Beers in February 2025, Okavango receives 30% of Debswana's production for the first five years and 40% for the second five, with a conditional five-year extension that would move the split to 50-50; the agreement in principle announced in July 2023 had projected ODC reaching 50% within the base term and the signed document does not. No revenue figure, tender calendar or strategic target was published with the announcement. This paper reported Dvash's succession at the WFDB by Mehul Shah on 15 July 2026 and Okavango's tender arrangement with the Dubai Diamond Exchange on 1 August 2026."},
 {"d":"diamonds",
  "h":"Vasant Mehta, GJEPC chairman from 2008 to 2010, has died at 81",
  "t":"Vasant Mehta, a former chairman of India's Gem and Jewellery Export Promotion Council, has died at 81, reported 18 August 2026. He ran M/s V. Rameshchandra & Co in Mumbai. He was the council's vice chairman in 1991-92, vice chairman again in 2006-08 and chairman from 2008 to 2010, a term that spans the global financial crisis and the credit contraction it produced across India's cutting and polishing sector. He convened the council's banking, insurance and taxation committee for years afterwards and advised the legal committee of the Bharat Diamond Bourse. Internationally he represented Indian interests at the World Diamond Council, the World Federation of Diamond Bourses, the International Diamond Manufacturers Association, the World Jewellery Confederation and the Kimberley Process, and he served the Mumbai Diamond Merchants Association. Gaetano Cavalieri, president of the World Jewellery Confederation, described him as first and foremost a servant of the industry. This paper carries no independent verification of the date or circumstances of the death beyond the trade report and stated so in print."},
 {"d":"retail-tech",
  "h":"Miniso tops NRF's Hot 25 on 53% US sales growth",
  "t":"The National Retail Federation's Hot 25 list for 2026, compiled by Kantar and published 21 August 2026, ranks Miniso first on 53% growth in US sales, Dick's Sporting Goods second at 49% following its acquisition of Foot Locker, Daiso Sangyo third at 26%, Primark fourth at 24% and Five Below fifth at 23%. The metric is the increase in domestic sales between 2024 and 2025, which makes the ranking a measure of momentum off each chain's own base rather than of size, and Dick's placing reflects an acquisition rather than organic demand. Rachel Dalton, Kantar's head of retail insights for the Americas, said value is a huge story in this year's list. No jewellery specialist appears in the top five and the list is a US ranking covering the year before the current gold price. This paper ran it against its own 21 August 2026 report that Zales, a Signet banner, puts 67% of purchases among its core shoppers as self-purchases."},
]

wk = record["weeks"][0]
assert wk["label"] == "This week — August 17", wk["label"]
wk["entries"] = ENTRIES + wk["entries"]
record["updated"] = "22 Aug 2026"
(C/"record.json").write_text(json.dumps(record, indent=1, ensure_ascii=False))
print("wire.json: edition %s, %d items" % (wire["edition"], len(wire["items"])))
print("record.json: %d entries prepended, week now %d" % (len(ENTRIES), len(wk["entries"])))
