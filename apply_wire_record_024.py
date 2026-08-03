#!/usr/bin/env python3
import json, pathlib
C = pathlib.Path("content")
wire = json.loads((C/"wire.json").read_text())
record = json.loads((C/"record.json").read_text())

wire["date_line"] = "Monday, August 3, 2026"
wire["edition"] = "Vol. I — No. 024"
wire["tape_ts"] = "3 Aug 2026, 6:01am New York · Kitco spot · change against Friday's 5pm close"
wire["items"] = [
 {"b":"SEVENTY-THREE MILLION IN SHOES","t":" — Vietnamese police have re-scaled the diamond-smuggling case to $73 million of stones moved into the country, about $57 million of them identified, with more than 30 people arrested or detained; the stone count is unchanged at 28,000-plus across 141 trips since 2024, against the $10.65 million in the July charge sheet"},
 {"b":"A SERIAL NUMBER TO COLLECT IT","t":" — Couriers carried stones in luggage, shoes and clothing on commercial flights from Hong Kong, arranged prices over WhatsApp, and released goods only to a recipient holding a US dollar bill whose eleven-character serial number matched one agreed in advance; state-owned Saigon Jewelry Company bought more than 3,400 stones for about $19 million"},
 {"b":"CHINA'S LOWEST SINCE 2004","t":" — Mainland Chinese gold jewellery demand fell 28% to 50.0 tonnes in the second quarter, the weakest second quarter since 2004, and 30% across the half to 136 tonnes, while the value of that half-year demand rose 11% to about $21 billion"},
 {"b":"THE UNITED STATES DOWN TWENTY-FIVE","t":" — American gold jewellery fabrication fell 25% to 22.2 tonnes in the second quarter, the sharpest percentage decline among the major markets, with India down 15% to 75.1 tonnes and the Middle East down 19% to 32.2 tonnes on a global figure of 278.2 tonnes"},
 {"b":"SILVER LEADS THE REOPEN","t":" — At 6:01am New York, gold bid $4,053.30, up $11.60 or 0.29% against Friday's close, silver $58.05, up 1.06%, platinum $1,647.00 and palladium $1,259.00; the ADP employment report lands midweek and non-farm payrolls on Friday"},
 {"b":"MICHAEL HILL ADDS TWO PERCENT","t":" — Group revenue rose 2% to A$654.7 million in the year to June 28, with same-store sales up 3% overall, Canada a record 7%, Australia 4.8% and New Zealand 3.6%; the chain closed eight stores and opened two, ending with 281"},
 {"b":"SHOPLIFTING DOWN, FRAUD UP","t":" — The National Retail Federation's 2026 study has shoplifting incidents down 12.4% and merchandise theft down 8.1%, while 69% of retailers report rising phone scams, 42% gift-card fraud and 40% organised retail crime; jewellery, gold and watches rank among the highest dollar-loss categories"},
 {"b":"FEWER CRIMES, COSTLIER ONES","t":" — The Jewelers' Security Alliance counted 1,233 crimes against US jewellery firms in 2025, down 13%, on losses that rose to $144.7 million; robberies involving guns, mace or vehicles went from 17% to 27% of the total and vehicle ram-raids from none reported to 13"},
]
wire["tape"] = [
 {"name":"Gold / oz","code":"XAU","px":"4,053.30","chg":"▲ +0.29%","dir":"up",
  "pts":[16,16,15,15,15,14,15,16,15,16]},
 {"name":"Natural 1ct (RAPI proxy)","code":"NAT1","px":"5,232.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Lab-grown 1ct wholesale","code":"LGD1","px":"727.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Platinum / oz","code":"XPT","px":"1,647.00","chg":"▲ +0.18%","dir":"up",
  "pts":[17,17,16,16,16,15,15,17,16,17]},
 {"name":"Silver / oz","code":"XAG","px":"58.05","chg":"▲ +1.06%","dir":"up",
  "pts":[18,18,18,17,17,17,16,16,15,16]},
]
(C/"wire.json").write_text(json.dumps(wire,ensure_ascii=False,indent=1))

# ---- record: new week at the top ----
old = record["weeks"][0]
assert old["label"] == "This week — July 27", old["label"]
old["label"] = "Week of July 27"

newent = [
 {"d":"diamonds","h":"Vietnam's smuggling case re-scaled to $73 million, with dollar-bill serial numbers as the release code",
  "t":"Vietnamese investigators now put the transnational diamond-smuggling network at $73 million of stones moved into the country, of which about $57 million have been identified, with more than 30 people arrested or detained. The stone count is unchanged from earlier reporting at more than 28,000 diamonds carried on 141 separate occasions since 2024. The figure in the charge sheet reported on 16 July was 280 billion dong, about $10.65 million, against 22 people charged. Couriers carried stones in luggage, shoes and clothing on commercial flights from Hong Kong into Vietnamese airports, with orders and prices arranged over WhatsApp, and released goods only to a recipient holding a US dollar bill whose eleven-character serial number matched one agreed in advance. Goods typically moved at about a third below market. State-owned Saigon Jewelry Company, which sets Vietnam's benchmark gold price, bought more than 3,400 of the stones for about $19 million. Police believe the operation was directed by an Indian national living in Hong Kong, sourcing in India and consolidating in Hong Kong. The former director of P-Lab, the grading subsidiary wholly owned by Phu Nhuan Jewelry that handles about 70% of Vietnamese certification, is among those charged.",
  "s":"IDEX Online / South China Morning Post / Bloomberg / Nikkei Asia"},
 {"d":"gold-metals","h":"Chinese gold jewellery demand falls to its lowest second quarter since 2004",
  "t":"The World Gold Council's Gold Demand Trends for the second quarter of 2026, published 30 July, put mainland Chinese gold jewellery demand at 50.0 tonnes, down 28% from 69.2 tonnes a year earlier and the lowest second-quarter figure since 2004. First-half Chinese demand was 136 tonnes, down 30%, while the value of that demand rose 11% to about $21 billion. India took 75.1 tonnes in the quarter, down 15% and its lowest second quarter since the pandemic, on first-half demand of 141 tonnes worth about $21 billion, up 26% by value. The Middle East fell 19% to 32.2 tonnes and the United States fell 25% to 22.2 tonnes, the sharpest percentage decline among the major markets. Global jewellery fabrication was 278.2 tonnes against 335.3 tonnes a year earlier, which the council described as one of the weakest second quarters in its data series. First-half global jewellery value reached about $86 billion, up 22% from $71 billion.",
  "s":"World Gold Council"},
 {"d":"gold-metals","h":"Metals reopen higher after the weekend, with silver leading at $58.05",
  "t":"The first session since Friday's close opened higher across the precious complex. At 6:01am New York time on 3 August, Kitco's spot page had gold bid at $4,053.30 an ounce, up $11.60 or 0.29% against the 31 July 5pm close of $4,041.70, on a range of $4,045.80 to $4,083.50. Silver bid $58.05, up 61.1 cents or 1.06%, on a range of $57.68 to $58.76, the largest percentage gain of the four metals and a gold to silver ratio of about 69.8. Platinum bid $1,647.00, up $3.00 or 0.18%, on a range of $1,641.00 to $1,676.00. Palladium bid $1,259.00, up $3.00 or 0.24%, on a wide range of $1,257.00 to $1,322.00. The week holds the ADP employment report midweek and non-farm payrolls on Friday, the first complete read on American hiring since the Federal Reserve held rates on 29 July with three dissents. This tape prints the live quotation rather than the settlement because Friday's close had already been carried through two editions.",
  "s":"Kitco"},
 {"d":"retail-tech","h":"Michael Hill lifts revenue 2% and same-store sales 3% while closing eight stores",
  "t":"Michael Hill reported group revenue of A$654.7 million, about $459.5 million, for the financial year to 28 June 2026, an increase of 2%. Same-store sales rose 3% across the group: 7% in Canada, described by the company as a record, on segment revenue of C$169.3 million; 4.8% in Australia on A$364.6 million; and 3.6% in New Zealand on NZ$108.9 million. The chain closed eight stores over the year, four in Australia and two each in Canada and New Zealand, and opened two, one in Australia and one in Canada, ending with 281 stores: 157 in Australia, 81 in Canada and 43 in New Zealand. Chief executive Jonathan Waecker said growth was significantly accelerating in Canada and New Zealand in the second half. Earnings were not disclosed alongside the sales figures.",
  "s":"Rapaport / Michael Hill"},
 {"d":"retail-tech","h":"Shoplifting falls while fraud, organised crime and violence against jewellers rise",
  "t":"The National Retail Federation's Impact of Retail Theft and Violence study, published in late July 2026, found shoplifting incidents down 12.4% in 2025 and merchandise theft down 8.1% against 2024, while 69% of retailers reported an increase in phone scams, 42% in gift-card theft and fraud, 40% in organised retail crime driving shoplifting, 36% in cargo and supply-chain theft, and 50% in repeat offenders. Jewellery, gold and watches rank among the categories generating the highest dollar losses to organised retail crime groups. The Jewelers' Security Alliance annual crime report, published 13 May 2026, counted 1,233 crimes against United States jewellery firms in 2025, down 13% from 1,420, on total dollar losses of $144.7 million against $142.5 million. On-premises burglaries fell 14% to 262 and robberies were flat at 218. Robberies involving guns, mace or vehicles rose to 27% of the total from 17%; mace or pepper-spray incidents went from 3 to 14; vehicles driven into stores went from none reported in 2024 to 13; crimes at jewellers' homes rose from 4 to 11; and two people in the industry died in 2025 against four the year before.",
  "s":"JCK / National Jeweler / National Retail Federation / Jewelers' Security Alliance"},
]
record["weeks"].insert(0, {"label":"This week — August 3","entries":newent})
record["updated"] = "3 Aug 2026"
(C/"record.json").write_text(json.dumps(record,ensure_ascii=False,indent=1))
print("wire No.024 written; new record week with", len(newent), "entries; weeks now", len(record["weeks"]))
