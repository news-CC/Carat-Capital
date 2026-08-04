#!/usr/bin/env python3
import json, pathlib
C = pathlib.Path("content")
wire = json.loads((C/"wire.json").read_text())
record = json.loads((C/"record.json").read_text())

wire["date_line"] = "Tuesday, August 4, 2026"
wire["edition"] = "Vol. I — No. 025"
wire["tape_ts"] = "4 Aug 2026, 5:59am New York · Kitco spot · change against Monday's close"
wire["items"] = [
 {"b":"THE ONE-CARAT STOPS FALLING","t":" — The RapNet Diamond Index for 1-carat polished was unchanged across July, ending a decline that had run without a positive print since June 2025; 0.30-carat rose 1.6%, 0.50-carat 1.8% and 3-carat 0.2%, the first month since March 2025 in which none of the four fell"},
 {"b":"THE BEST MONTH SINCE THE TARIFFS","t":" — The 0.50-carat gain is that size's largest since March 2025; Rapaport reports American buying concentrated in 2-carat rounds, G to J colour, VS1 to SI2, plus fancy shapes, while the July schedule keeps 10% on India-finished polished and clears Belgian, Botswanan and Namibian cutting at zero"},
 {"b":"MINUS ONE TENTH FOR COLOR","t":" — The Fancy Color Research Foundation's second-quarter index fell 0.1%, with pink up 0.1% after a 0.3% fall, blue down 0.4% and yellow down 0.3% for a second quarter running; 1-carat fancy-vivid blues gained 1.5% while 2-carat blues lost 1.3%"},
 {"b":"SIX HUNDRED AND THIRTY-THREE FOR THE INDEPENDENTS","t":" — EveryWatch puts first-half secondary transactions at $10.5 billion, up 37.2%, with independent makers taking $633.8 million, up 89%, ahead of the LVMH watch portfolio at about $617 million; F.P. Journe alone did $201.6 million on a median sale price of $215,000, up 82%"},
 {"b":"ROLEX STILL FORTY-ONE PERCENT","t":" — Rolex accounted for $4.29 billion of secondary value, Patek Philippe $1.51 billion and Audemars Piguet $983 million; Rolex certified pre-owned did $385 million, more than double, while the United States and Canada transacted $4.5 billion, up 70%, against Asia down 2.6%"},
 {"b":"SEVENTY-THREE LOTS OVER A MILLION","t":" — Watch auction sales reached $680 million in the first half, up 45%, with 73 lots clearing $1 million against roughly 25 a year earlier and three passing $10 million; the median watch across all channels sold for $5,900, up 19%, in 43 days against 39"},
 {"b":"ONE POINT TWO MILLION APPLY","t":" — More than 1.2 million people completed Swatch's 32-question online application for 1,969 MoonSwatch 1969 pieces at $570, about 600 applicants per watch; JCK puts the fine gold content at 8.25 grams, worth roughly $1,074 at Tuesday's spot, and reports the May Royal Pop trading below $400"},
 {"b":"PLATINUM ADDS ONE POINT SEVEN","t":" — At 5:59am New York, gold bid $4,048.80, down 0.14%, platinum $1,655.00, up 1.72%, palladium $1,266.00, up 1.77%, and silver $58.63, up 0.97%; the gold to silver ratio tightened to about 69.0 and ADP lands Wednesday with non-farm payrolls on Friday"},
 {"b":"THIRTEEN HUNDRED BRANDS AND A CENTENARY","t":" — Vicenzaoro September runs 4 to 8 September at Fiera di Vicenza with about 1,300 brands from 38 countries and buyers from more than 130, the new Hall 2 in full use and T.Gold moved on site; CIBJO's centenary congress sits inside it from 4 to 7 September"},
]
wire["tape"] = [
 {"name":"Gold / oz","code":"XAU","px":"4,048.80","chg":"▼ −0.14%","dir":"down",
  "pts":[16,15,15,15,14,15,16,15,16,15]},
 {"name":"Natural 1ct (RAPI proxy)","code":"NAT1","px":"5,232.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Lab-grown 1ct wholesale","code":"LGD1","px":"727.00","chg":"— unch.","dir":"flat",
  "pts":[13,13,13,13,13,13,13,13,13,13]},
 {"name":"Platinum / oz","code":"XPT","px":"1,655.00","chg":"▲ +1.72%","dir":"up",
  "pts":[17,16,16,16,15,15,17,16,17,18]},
 {"name":"Silver / oz","code":"XAG","px":"58.63","chg":"▲ +0.97%","dir":"up",
  "pts":[18,18,17,17,17,16,16,15,16,17]},
]
(C/"wire.json").write_text(json.dumps(wire,ensure_ascii=False,indent=1))

# ---- record: prepend into the current week ----
wk = record["weeks"][0]
assert wk["label"] == "This week — August 3", wk["label"]

newent = [
 {"d":"diamonds","h":"The 1-carat polished index stops falling after thirteen months, and July prints the best month since the tariffs",
  "t":"Rapaport published July 2026 RapNet Diamond Index figures on 4 August. The 1-carat index was unchanged across the month, ending a decline that had run without a positive print since June 2025. The 0.30-carat index rose 1.6%, the 0.50-carat index rose 1.8%, its largest monthly gain since March 2025, and the 3-carat index rose 0.2%. It is the first month since March 2025 in which none of the four headline categories fell, making July the best month for polished prices since the April 2025 tariff schedule. Rapaport reports American demand concentrated in 2-carat rounds in G to J colour and VS1 to SI2 clarity, plus fancy shapes. The tariff schedule in force from late July keeps 10% on polished finished in India while loose natural diamonds cut in Belgium, Botswana and Namibia clear at zero. Lab-grown competition at the entry price point, weak Chinese demand and Angolan rough surplus are unresolved. Carat Capital's NAT1 line carries 5,232.00 unchanged, now for the sourced reason that the 1-carat index was flat rather than for the absence of a print.",
  "s":"Rapaport"},
 {"d":"gemstones","h":"Fancy colour diamond prices move one tenth of one percent in the second quarter",
  "t":"The Fancy Color Research Foundation's index of pink, blue and yellow diamonds fell 0.1% across the second quarter of 2026, reported by Rapaport on 3 August. Pink rose 0.1% after falling 0.3% in the prior quarter, with 1 and 1.5-carat pinks each up 0.4%, 2 and 3-carat pinks each up 0.6%, fancy-vivid pinks up 0.5% and fancy-intense pinks down 0.1%. Blue fell 0.4% after falling 0.3%, with 1-carat blues up 0.7%, 1.5-carat down 0.2%, 2-carat down 1.3%, 3-carat down 0.7% and 5-carat flat; 1-carat fancy-vivid blues rose 1.5% while fancy and fancy-intense blues each fell 0.6%. Yellow fell 0.3% for a second consecutive quarter, with 3-carat yellows up 0.7% against fancy-intense yellows down 1.3%. The foundation described a market that remained broadly stable.",
  "s":"Fancy Color Research Foundation via Rapaport"},
 {"d":"watches","h":"Independent watchmakers clear more secondary value than LVMH's watch brands in the first half",
  "t":"EveryWatch's first-half 2026 report, published 30 July and taken up by the trade press on 3 August, put global secondary watch transactions at $10.5 billion, up 37.2% year on year, compiled from sold prices at about 650 dealers and roughly 470 auction houses. Independent makers transacted $633.8 million collectively, up 89%, ahead of the LVMH watch portfolio at about $617 million. F.P. Journe accounted for $201.6 million of that, an increase of 196.9%, ranking seventh among all watch brands, on a median sale price of $215,000, up 82%, and a turnover rate above 57%. H. Moser and Cie. did $26 million, up 64%, Parmigiani Fleurier $21 million, up 60%, and De Bethune $19 million, up 2%. Rolex remained the largest single brand at $4.29 billion, about 41% of all value, with Patek Philippe at $1.51 billion and Audemars Piguet at $983 million. Rolex certified pre-owned reached $385 million, more than double the prior year. The United States and Canada transacted $4.5 billion, up 70%, while Asia fell 2.6%. The median watch sold for $5,900, up 19%, in an average of 43 days against 39.",
  "s":"EveryWatch via JCK and Time+Tide"},
 {"d":"watches","h":"Swatch replaces the release-day queue with a 32-question form and takes 1.2 million applications",
  "t":"Swatch allocated 1,969 MoonSwatch Mission to the Moon 1969 pieces through the Electronic Swatch Timepiece Application, a 32-question online form, and more than 1.2 million people completed it, about 600 applicants per available watch. The retail price is $570, derived from the gold price on 21 July 1969. JCK reports the watch carries 11 grams of 18-karat gold across dial, hands, crown and pushers, which is 8.25 grams of fine gold, worth about $1,074 at Kitco spot of $4,048.80 an ounce on 4 August. The mechanic followed the May Royal Pop collaboration with Audemars Piguet, which required police outside stores in New York, Paris and London, closed 15 American stores on a Saturday and traded at four to five times retail before falling below $400 by August. Swatch Group stock rose about 15% in the two weeks after the Royal Pop launch.",
  "s":"JCK / Kitco"},
 {"d":"auctions","h":"Watch auction sales rise 45% to $680 million with 73 lots above a million dollars",
  "t":"EveryWatch's first-half 2026 report put watch auction sales at $680 million, up 45% year on year, inside a total secondary market of $10.5 billion. Seventy-three lots cleared $1 million, close to three times the same period a year earlier, and three lots passed $10 million. The highest was an F.P. Journe Chronometre a Resonance Souscription number 007, which made $13,922,000 at Phillips New York on 14 June 2026, the highest auction price for a watch by an independent maker. Phillips also placed a Resonance Souscription number 18 at $6.3 million and a Resonance Pisa at $3 million across the spring season. The median watch across all channels sold for $5,900, up 19%, and took an average of 43 days to sell against 39 a year earlier.",
  "s":"EveryWatch via JCK / Robb Report"},
 {"d":"gold-metals","h":"The white metals lead again as gold slips 0.14% ahead of Friday's payrolls",
  "t":"At 5:59am New York time on 4 August, Kitco's spot page had gold bid at $4,048.80 an ounce, down $5.70 or 0.14% against Monday's close; platinum $1,655.00, up $28.00 or 1.72%; palladium $1,266.00, up $22.00 or 1.77%; and silver $58.63, up 56.3 cents or 0.97%. The gold to silver ratio tightened to about 69.0 from 69.8 the previous session and platinum stood at 40.9% of the gold price. Trading Economics, quoting a different print time on the same session, showed platinum up 2.56% and silver up 1.83% while agreeing with Kitco on gold at minus 0.14%; it put gold down about 2.8% over the past month and up 19.8% on the year, silver down 5.3% on the month and up 55.3% on the year, and platinum up 26.8% on the year. The ADP national employment report is due Wednesday and non-farm payrolls Friday, the first full read on American hiring since the Federal Reserve held rates on 29 July with three dissents. Gold at $4,048.80 an ounce is $130.17 a gram of fine metal.",
  "s":"Kitco / Trading Economics"},
 {"d":"retail-tech","h":"Vicenzaoro September opens Hall 2 and hosts CIBJO's centenary congress",
  "t":"Vicenzaoro September runs from 4 to 8 September 2026 at Fiera di Vicenza, organised by Italian Exhibition Group, with roughly 1,300 exhibiting brands from 38 countries and buyers expected from more than 130 countries, on figures IEG gave JCK on 13 July. The show was reported close to sold out in late May. The new Hall 2, a two-storey central hub connected by covered walkways, is fully operational for the first time, and T.Gold, the machinery and technology section for precious-metal production, has moved inside the expo centre grounds into Hall 4; Jewellery Outlook confirmed both through interviews published 31 July. CIBJO, the World Jewellery Confederation, holds its centenary congress in Vicenza from 4 to 7 September, one hundred years after its founding in 1926, with its Assembly of Delegates and sectoral commissions meeting and amendments to the Blue Books introduced. The scheduled agenda covers the state of the diamond industry, lab-grown diamonds, the supply chain, pearls and coloured gemstones. Russia's Resolution 657, which bans the word diamond for synthetics sold there, comes into force on 1 September, three days before the congress opens.",
  "s":"JCK / CIBJO / Jewellery Outlook / Vicenzaoro"},
]
wk["entries"] = newent + wk["entries"]
record["updated"] = "4 Aug 2026"
(C/"record.json").write_text(json.dumps(record,ensure_ascii=False,indent=1))
print("wire No.025 written;", len(newent), "record entries prepended into", wk["label"], "- week now", len(wk["entries"]))
