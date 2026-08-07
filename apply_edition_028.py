#!/usr/bin/env python3
# Edition No. 028 - 2026-08-07. Prepends 6 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-07"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - fifteen-years-no-tax ==========
art("fifteen-years-no-tax","diamonds",True,"Lead Story · Diamonds Desk",5,"The Diamonds Desk",
["GAP","NUM","STAKES"],
"Fifteen years, no tax: what Mumbai just offered to take from Dubai",
"India's lower house passed a Bill on 6 August exempting qualifying foreign rough sellers from income tax between 1 October 2026 and 31 March 2041. It replaces a safe harbour that presumes profit at 1.25% of gross revenue, against corporate rates reaching about 33%.",
[
"India has put a fifteen-year tax holiday on the table for the foreign companies that sell rough diamonds into its bourses. The Taxation and Other Laws (Amendment) Bill, 2026 passed the Lok Sabha on 6 August and proposes exempting qualifying non-resident sellers of rough from Indian income tax between 1 October 2026 and 31 March 2041. The exemption is conditional on the sale taking place inside a Special Notified Zone, of which two matter: the zone inside the Bharat Diamond Bourse in Mumbai and the one at the Surat Diamond Bourse. Miners, brokers, aggregators, auction operators and sightholders all fall within the class of seller the Bill describes, and a qualifying company must furnish information when asked.",
"What the Bill removes is a piece of arithmetic that has kept rough auctions out of India for a decade. A foreign miner selling rough in an Indian zone today can elect a safe harbour that presumes taxable profit at 1.25% of gross revenue, or else face Indian corporate tax at rates reaching about 33% of profit. Neither figure is punitive on its own. The obstacle is that both require a foreign seller to take an Indian tax filing position on goods it intends to sell and move out within days, and that is a cost Dubai and Antwerp do not impose on the same parcel. Zero for fifteen years removes the calculation rather than lowering it.",
"The target is not disguised. India cuts and polishes the large majority of the world's rough but buys very little of it on Indian soil, which means the stone crosses a border twice before a Surat wheel touches it, and the intermediary trading centre collects the margin, the storage and the paperwork on the way through. This paper reported on 2 August that a single tender cleared at 100% in Dubai against 75% in Johannesburg, and on 15 July that Dubai's diamond trade was worth $41.7 billion in a year. The Gem and Jewellery Export Promotion Council, which has lobbied for this change for years, welcomed the introduction as a step for India's rough trading ecosystem. Antwerp, whose position this desk covered on 2 August, has the same exposure with less growth behind it.",
"None of this is law. The Bill has cleared the lower house only. It requires passage through the Rajya Sabha and presidential assent before any exemption exists, and no date has been set for a hearing in the upper house, though the trade bodies quoted expect it to pass. That leaves the 1 October start date as an intention rather than a commitment, roughly eight weeks out, with two procedural steps and no calendar between here and there. A miner building a 2027 tender schedule around a Mumbai or Surat sale is currently building it on a Bill, and the sensible position is to plan the logistics and withhold the commitment until assent.",
"The desk's view: the cheapest thing a government can give a diamond trade is certainty about where the paperwork happens, and India has just offered fifteen years of it. Price is not what has kept rough tenders in Dubai and Antwerp; predictability is, and a fifteen-year window is long enough to survive three Indian governments and to justify a producer moving a permanent sales function rather than flying in for a week. The read for a cutter is that landed rough cost could fall by the intermediary's cut rather than by any change in the mine price, which is the only kind of cost relief available in a year when both major producers are shrinking output on purpose. The read for Dubai is that its 100% clearance rates were earned in the absence of a competitor with a hundred thousand polishers behind it."
],
[
 {"title":"India Proposes Tax Exemption for Overseas Rough Sellers — Rapaport (6 August 2026)","url":"https://rapaport.com/news/india-proposes-tax-exemption-for-overseas-rough-sellers/"},
 {"title":"India set to Challenge Dubai, Antwerp with Foreign Tax Exemption — IDEX Online","url":"https://www.idexonline.com/FullArticle?Id=51324"},
 {"title":"GJEPC Welcomes Introduction of Taxation and Other Laws (Amendment) Bill 2026 — Mines to Market","url":"https://minestomarket.news/gjepc-welcomes-introduction-of-taxation-and-other-laws-amendment-bill-2026-a-landmark-step-for-indias-rough-diamond-trading-ecosystem/"},
 {"title":"Taxation and Other Laws (Amendment) Bill, 2026 — Explained","url":"https://vajiramandravi.com/current-affairs/taxation-amendment-bill-2026/"},
])

# ========== 2. every-metal-runs-before-payrolls ==========
art("every-metal-runs-before-payrolls","gold-metals",False,"Gold & Metals Desk · The Tape",5,"The Gold & Metals Desk",
["NUM","STAKES"],
"$4,314.50 and silver up 4.71%: every metal runs before payrolls",
"At 5:58am New York gold bid $4,314.50, up $75.20 or 1.77%. Silver added $2.89 or 4.71% to $64.29, platinum 3.14% to $1,772.00 and palladium 2.14% to $1,382.00. The ratio tightened to 67.1 from 69.3. Payrolls land at 8:30am.",
[
"Every metal on the board ran on Friday morning, and the fastest one ran hardest. At 5:58am New York time Kitco had gold bid at $4,314.50 an ounce, up $75.20 or 1.77% against Thursday's close, a fifth consecutive advance and above the seven-week high this paper carried yesterday. Silver was bid at $64.29, up $2.89 or 4.71%, the largest single-session move of the four. Platinum was bid at $1,772.00, up $54.00 or 3.14%, and palladium at $1,382.00, up $29.00 or 2.14%. Against the 6:03am mark carried here on Thursday, gold has added $43.60 an ounce or 1.02% and silver $2.62 or 4.25% in twenty-four hours.",
"Thursday's warning did not hold. This desk wrote yesterday that silver turning red beneath a gold high was the clearest internal warning the tape had printed all week, on the reasoning that the high-beta metal leads in both directions. Silver has now taken that back in a single session with a 4.71% advance, and the gold to silver ratio has tightened to 67.1 from 69.3, more than reversing Thursday's widening. The honest reading is that one red session in silver was noise rather than a turn. This desk records the call it made against the print that followed it rather than quietly moving on.",
"What the trade is pricing is a route and a jobs number. Iran said this week it had reached an understanding with Oman on a proposed shipping lane through the Strait of Hormuz, with a joint statement described as in final drafting, and Iran has been explicit that this is a temporary route and not a full reopening. Lower oil lowers inflation expectations, and the CME FedWatch tool has September's move at a 56.9% probability against 63.4% a week earlier. The labour data has run the same way: ADP put July private hiring at 44,000 against about 50,000 expected, JOLTS came in softer and initial claims rose to 199,000. The Bureau of Labor Statistics releases July non-farm payrolls at 8:30am this morning, after this edition closes.",
"Two marks belong on the record. This paper's own overnight tape read gold at $4,304.40 at 4:58am, $10.10 below the 5:58am bid carried here, with silver at $64.16 and platinum at $1,763.00; palladium was identical at $1,382.00 and every previous close matched, so this is a rally continuing between two reads rather than two desks disagreeing. Retail quotes are wider apart than that. Khaleej Times had Dubai 24-carat at AED 517.50 a gram this morning while this paper's own metals desk read AED 510.25 the same day and the overnight desk AED 514.00 on Thursday, a spread of AED 7.25 a gram between two readings of the same Friday. Fine gold at $4,314.50 an ounce is $138.72 a gram, against $137.31 yesterday.",
"The desk's view: a rally where the leader comes back after one down session is a rally with money still arriving, and it has about two hours left before something can break it. Silver at $64.29 has now moved more than 4% on three of the last five sessions, which is not the behaviour of a hedge and is the behaviour of a position. For the bench the working number is $138.72 a gram, $1.41 above yesterday and $8.55 above Tuesday, and a quotation written before 8:30am this morning is a quotation written before the only scheduled event of the week that can reprice it. NAT1 and LGD1 are both carried unchanged; the lab-grown reference held at $709 on CaratRadar for a third straight day while a second tracker stood at $536, a spread of roughly 24% that this desk continues to carry rather than average."
],
[
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (7 August 2026, 5:58am EST)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Gold steadies near seven-week high as markets await Strait of Hormuz deal — FXStreet (6 August 2026)","url":"https://www.fxstreet.com/news/gold-steadies-near-seven-week-high-as-markets-await-strait-of-hormuz-deal-202608061118"},
 {"title":"Today's Gold Rate in Dubai, Live Gold Price — Khaleej Times (7 August 2026)","url":"https://www.khaleejtimes.com/gold-forex"},
 {"title":"US Employment Situation (Non-Farm Payrolls), release 7 August 2026 — Bureau of Labor Statistics","url":"https://www.bls.gov/news.release/empsit.nr0.htm"},
])

# ========== 3. one-thirty-two-against-three-thirty-nine ==========
art("one-thirty-two-against-three-thirty-nine","gold-metals",False,"Gold & Metals Desk · China",5,"The Gold & Metals Desk",
["NUM","VS"],
"132 tonnes of jewellery, 339 tonnes of bars: China picks a side",
"China Gold Association figures put first-half gold jewellery consumption at 132.13 tonnes, down 33.88%, against bar and coin demand of 339.34 tonnes, up 28.42%. Total consumption still rose 1.23% to 511.41 tonnes. The jewellery counter is now the smaller half by a distance.",
[
"China bought more gold in the first half of 2026 than in the first half of 2025 and bought far less jewellery. The China Gold Association's half-year figures put national gold consumption at 511.41 tonnes, up 1.23% year on year, with gold jewellery at 132.13 tonnes, down 33.88%, and bars and coins at 339.34 tonnes, up 28.42%. Investment metal is now two and a half times the jewellery figure in the world's largest jewellery market. The association attributes the split to elevated and volatile prices and to the rollout of new domestic gold tax policies, with temporary price corrections pulling buyers into bank-sold bars.",
"That is a second authority on the same market, and it does not agree with the first. This paper reported on 3 August, from the World Gold Council's Q2 report, that Chinese jewellery demand fell about 30% across the half to roughly 136 tonnes and hit its weakest second quarter since 2004. The China Gold Association now puts the same half at 132.13 tonnes and the same decline at 33.88%. The gap is about four tonnes and nearly four percentage points, on definitions that differ between a consumption series and a demand series. Both bodies describe the same collapse and neither should be quoted to the decimal against the other.",
"The bar and coin line is where the number changes what a retailer should do. A Chinese consumer who once bought a chain as a store of value now buys the bar directly, and 339.34 tonnes says that substitution has already happened at scale rather than being a forecast. The jewellery counter is not losing customers to another jeweller; it is losing them to a product with no making charge, no design risk and a resale spread the buyer can calculate. That is the same structure this desk described on 5 August in Luk Fook's fixed-price mix, where the profitable answer was to sell design rather than grams.",
"The value line will keep hiding this. At the prices that have run all year, 132 tonnes of jewellery is worth more in yuan than a much larger tonnage was worth in 2024, which means Chinese jewellery revenue can be reported as healthy while the metal moving across the counter falls by a third. This paper has made the same point about India, where 75.1 tonnes in the second quarter was a 15% volume fall and roughly a 50% value rise. Any 2026 comparison built on revenue rather than weight is measuring the gold price and calling it demand.",
"The desk's view: the tonnage series says the Chinese jewellery counter has lost a third of its volume in a year and the total consumption figure says the country's appetite for gold is intact, which are not contradictory statements but one statement about form. Gold is winning and jewellery is losing, in the same market, at the same time. For a fabricator planning Chinese orders into the fourth quarter the useful figure is 132.13 tonnes and not 511.41, and the useful question is whether a piece justifies its making charge against a bar sitting in the same window. Two authorities now put the decline between 30% and 34%, which is close enough to plan against and far enough apart to quote carefully."
],
[
 {"title":"China's gold consumption patterns diverge amid volatile prices — China.org.cn (7 August 2026)","url":"http://www.china.org.cn/2026-08/07/content_118637711.shtml"},
 {"title":"China's gold consumption patterns diverge amid volatile prices — China Daily (6 August 2026)","url":"http://usa.chinadaily.com.cn/a/202608/06/WS6a747b61a310986e2b469663.html"},
 {"title":"Gold Demand Trends: Q2 2026 — World Gold Council","url":"https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q2-2026"},
 {"title":"China gold market update: June concludes a divided H1 — World Gold Council","url":"https://www.gold.org/goldhub/gold-focus/2026/07/china-gold-market-update-june-concludes-divided-h1"},
])

# ========== 4. twenty-two-thirty-eight-an-order ==========
art("twenty-two-thirty-eight-an-order","retail-tech",False,"Retail & Technology Desk · Earnings",5,"The Retail Desk",
["NUM","ACTOR"],
"$2,238 an order: Brilliant Earth buys its profit back",
"Second-quarter revenue rose 6% to $115.1 million on 2.1% fewer orders, with average order value up 8% to $2,238. Gross margin reached 57.9% and the company posted $0.8 million of net income against a $1.1 million loss. Full-year guidance goes to $459-462 million.",
[
"Brilliant Earth sold fewer things for more money and that was enough to turn the quarter. Second-quarter revenue rose 6% year on year to $115.1 million on a 2.1% decline in total orders, with average order value up 8% to $2,238. Net income was $0.8 million against a $1.1 million loss in the same quarter last year. Gross margin reached 57.9%, a 360 basis point improvement on the previous quarter. The company raised full-year revenue guidance to $459 million to $462 million and guided the third quarter to roughly flat sales with adjusted EBITDA between $3 million and $5 million.",
"The mix is doing the work rather than the traffic. Fine jewellery bookings grew 32% year on year, which is the line that matters most in a business built on bridal, because it is the part of the assortment a customer can buy more than once. An eight percent rise in ticket against a two percent fall in orders is a business trading down its unit count deliberately and being paid for it. A 57.9% gross margin says the pricing held while it did so. This is the second consecutive quarter in which the story is composition rather than volume.",
"A negative order count in a growing revenue line is worth sitting with. It means the customer base did not expand, and the additional $6.5 million or so of quarterly revenue came from existing demand spending more per transaction. That works while the higher-income buyer holds and stops working the moment that cohort trims, because there is no volume growth underneath to absorb it. The company has effectively concentrated its result in the top of its own customer file, which is a real strategy and a narrow one.",
"Set against the wider counter, the direction is consistent. This paper reported on 3 August that American jewellery revenue rose while tonnage fell across the largest markets, and on 5 August that Luk Fook's record profit came from fixed-price design rather than gram weight. Brilliant Earth's version is the same trade made online: fewer transactions, higher tickets, margin defended. The difference is that Brilliant Earth prices a category where lab-grown has removed the floor from the centre stone, which makes the fine jewellery line's 32% growth the more durable of its two numbers.",
"The desk's view: raising annual guidance on a quarter with fewer orders is a bet that the high-ticket customer stays, and the third-quarter guide of flat sales says the company is not pretending otherwise. For an independent competing against this, the transferable lesson is the 360 basis point margin recovery, which came from what was sold rather than from discounting less, and that is available to any shop willing to edit its case toward the pieces that carry a making charge. The number to watch in the fourth quarter is not revenue but orders, because a second consecutive decline with the ticket flat would mean the ticket has finished doing the work."
],
[
 {"title":"Brilliant Earth Returns to Profit as Sales Value Rises — Rapaport (August 2026)","url":"https://rapaport.com/news/brilliant-earth-returns-to-profit-as-sales-value-rises/"},
 {"title":"Brilliant Earth Reports Second Quarter Results and Raises Annual Profitability Guidance — GlobeNewswire (6 August 2026)","url":"https://www.manilatimes.net/2026/08/06/tmt-newswire/globenewswire/brilliant-earth-reports-second-quarter-results-and-raises-annual-profitability-guidance/2399851"},
 {"title":"Brilliant Earth Raises Profit Outlook After Margins Rebound — JCK","url":"https://www.jckonline.com/editorial-article/brilliant-earth-raises-profit/"},
])

# ========== 5. the-fourteen-percent-that-isnt ==========
art("the-fourteen-percent-that-isnt","gold-metals",False,"Gold & Metals Desk · Platinum",4,"The Gold & Metals Desk",
["GAP","HOWTO"],
"The 14% that isn't a decline: platinum's China forecast, read properly",
"The World Platinum Investment Council projects Chinese platinum jewellery down 14% in 2026 and global platinum jewellery down 6%. Strip out an unrepeated 2025 stock build and Chinese fabrication shows a small increase. Spot platinum added 3.14% to $1,772.00 the same week.",
[
"The most quotable platinum number of the week is a 14% fall in Chinese jewellery demand for 2026, and it is not a fall in demand. The World Platinum Investment Council's projection compares 2026 against a 2025 that carried an extraordinary inventory build in the second quarter, when Chinese fabricators bought platinum ahead of a gold price that had made their usual metal unaffordable. Strip that unrepeated stock build out of the base and Chinese platinum jewellery fabrication shows a small year-on-year increase rather than a double-digit contraction. The underlying trend in China is growth. The published headline is a base effect.",
"That distinction decides what a buyer does with the number. A fabricator reading 14% as a demand signal cuts its 2026 order book into a market that is quietly growing. A fabricator reading it as an inventory comparison holds the order book and watches the offtake instead. The same trap sits in the global figure: WPIC has worldwide platinum jewellery demand contracting about 6% in 2026, with North American and European growth consolidating after strong years and Indian demand facing tariff headwinds, and the largest single contributor to that global contraction is the Chinese comparison that is not what it appears.",
"The price is moving the other way while the forecast falls. Platinum was bid at $1,772.00 an ounce at 5:58am New York on Friday, up $54.00 or 3.14% on the session and the second-strongest performer of the four metals, and WPIC has forecast a fourth consecutive annual market deficit for 2026 at 297,000 ounces. A metal in structural deficit with a headline jewellery forecast in decline is a metal whose jewellery number is being read by nobody who trades it, and the deficit is the reason the price does not care.",
"For the bench the practical figure is the ratio rather than either forecast. Platinum at $1,772.00 stands at 41.1% of gold at $4,314.50, essentially unchanged from the 41.0% this desk marked on Thursday, which means platinum has kept pace with a gold rally rather than closed any of the gap. A platinum band still costs well under half the metal cost of the equivalent gold band, and that arithmetic, not a Chinese inventory comparison, is what puts the metal into a case.",
"The desk's view: read WPIC's own footnote before quoting WPIC's own headline, because the 14% is an artefact of an exceptional 2025 quarter and the council says so plainly. The rule generalises past platinum. Any 2026 comparison against 2025 in this trade is a comparison against a year in which buyers front-ran a gold price, and a great many of this year's declines are last year's stockpiling being unwound. The number that survives the caveat is the deficit, now heading into a fourth consecutive year, and a fabricator planning 2027 should price the metal off that rather than off a jewellery forecast."
],
[
 {"title":"Platinum Jewelry Demand Update — CME Group (2026)","url":"https://www.cmegroup.com/articles/2026/platinum-jewelry-demand-update.html"},
 {"title":"Fourth consecutive platinum market deficit forecast for 2026 — World Platinum Investment Council","url":"https://www.prnewswire.com/news-releases/fourth-consecutive-platinum-market-deficit-forecast-for-2026---supply-to-fall-short-of-demand-by-297-koz-302774250.html"},
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (7 August 2026, 5:58am EST)","url":"https://www.kitco.com/price/precious-metals"},
])

# ========== 6. twenty-nine-ninety-nine-at-the-counter ==========
art("twenty-nine-ninety-nine-at-the-counter","retail-tech",False,"Retail & Technology Desk · Mass Market",4,"The Retail Desk",
["NUM","STAKES"],
"$29.99 at the piercing counter: lab-grown finds the mass market",
"Claire's is rebuilding its in-store piercing service across the United States and Canada from August, its second overhaul in three years, and adding lab-grown diamond studs to the starter assortment. Kits begin at $29.99 with the piercing free.",
[
"The cheapest place a lab-grown diamond now sits is a mall piercing chair. Claire's is relaunching its in-store piercing experience across the United States and Canada from August 2026, the second revamp of that service in three years, and the expanded stud assortment adds lab-grown diamonds and coloured gemstones alongside its existing gold and steel starters. Piercing kits begin at $29.99 with the piercing itself free, and the lab-grown range includes 14-carat white gold studs at 0.10 carats total weight sold as a complete kit with aftercare solution.",
"That price point is the story rather than the stone. A tenth of a carat of grown material in a 14-carat gold setting, sold as a service bundle to a first-time piercing customer, is lab-grown functioning as a finish specification rather than as a gemstone purchase. Nobody buying at $29.99 is comparing certificates. They are buying a stud that will not react to a healing lobe, and the material happens to be diamond because grown material has fallen far enough to make that the practical choice at that price.",
"This is the tier-down this desk has been tracking from the other end. Carat Capital reported on the collapse of grown wholesale prices through the year and on retailers separating their floors, with lab-grown taking the everyday and bridal-adjacent business while natural is positioned as rarity. Claire's sits well below the level at which that positioning debate happens, and its arrival is the clearest evidence yet that grown material has reached the price at which it displaces cubic zirconia and steel rather than natural diamond. The competitive damage lands on the synthetics below it, not the stones above it.",
"There is a demand argument in the service itself. Piercing brings a customer into a fixed appointment with a staff member and a decision to make about metal and stone, which is the transaction structure a jeweller spends money to create and a chain like this gets for the price of a chair. Claire's has now rebuilt that service twice in three years, which reads as a company that has identified piercing as the reason for the store rather than an add-on to the merchandise.",
"The desk's view: the trade should stop treating each new lab-grown price floor as a natural diamond story, because this one is not. A $29.99 piercing kit competes with cubic zirconia, surgical steel and a twelve-dollar sleeper, and it wins on hypoallergenic setting quality as much as on the stone. What it does to the independent jeweller is subtler and slower: a generation whose first diamond is a free-with-purchase stud at fourteen arrives at an engagement counter with a different idea of what the word costs. That is a twenty-year problem being created at $29.99 a time, and no amount of certification argument reaches it."
],
[
 {"title":"Claire's Revamps Piercing Services for Second Time in Three Years — National Jeweler","url":"https://nationaljeweler.com/articles/15201-claire-s-revamps-piercing-services-for-second-time-in-three-years"},
 {"title":"Claire's Intensifies Focus On Piercing As Part Of Store Overhaul — Forbes (6 August 2026)","url":"https://www.forbes.com/sites/sharonedelson/2026/08/06/claires-intensifies-focus-on--piercing-as-part-of-store-overhaul/"},
 {"title":"Claire's revamps iconic piercing experience — Retail Dive","url":"https://www.retaildive.com/news/claires-revamps-in-store-piercing-experience/826321/"},
 {"title":"14kt White Gold 0.1 ct tw Laboratory Grown Diamond Studs Ear Piercing Kit — Claire's","url":"https://www.claires.com/us/14kt-white-gold-0.1-ct-tw-laboratory-grown-diamond-studs-baby-ear-piercing-kit-with-ear-care-solution-67004P.html"},
])

# ---------------- specs ----------------
def strip(cap, cells): return {"strip":{"cap":cap,"cells":cells}}
def bars(no,title,rows,note,cc): return {"no":no,"title":title,"rows":rows,"note":note,
    "cap":"Carat Capital graphics desk. &nbsp;CC/2026/%d"%cc}
def flow5(sub1,sub2,sub3,pull_q,pull_attr,also_t,also_href):
    return [{"sub":sub1,"n":"§1"},{"p":0},{"p":1},
            {"sub":sub2,"n":"§2"},{"p":2},{"pull":{"q":pull_q,"attr":pull_attr}},
            {"sub":sub3,"n":"§3"},{"p":3},{"also":{"t":also_t,"href":also_href}}]
def nxt(lslug,ltag,lblurb,m1,mt1,m2,mt2):
    return {"lead":{"slug":lslug,"tag":ltag,"blurb":lblurb},
            "minis":[{"slug":m1,"tag":mt1},{"slug":m2,"tag":mt2}]}

specs = {}

specs["fifteen-years-no-tax"] = {
 **strip("By the numbers · Taxation and Other Laws (Amendment) Bill, 2026",[
   {"fig":"15 yrs","lab":"proposed income-tax exemption"},
   {"fig":"1 Oct 2026","lab":"start, to 31 Mar 2041"},
   {"fig":"1.25%","lab":"current safe harbour, of gross revenue"},
   {"fig":"~33%","lab":"corporate rate if safe harbour not elected"},
   {"fig":"2","lab":"Special Notified Zones: Mumbai, Surat"}]),
 "figs":[bars("Plate I","What a foreign rough seller pays in an Indian notified zone",[
   {"l":"CORPORATE RATE, ON PROFIT","v":33,"d":"up to ~33%"},
   {"l":"SAFE HARBOUR, ON REVENUE","v":1.25,"d":"1.25%"},
   {"l":"PROPOSED, FROM 1 OCT 2026","v":0,"d":"nil","hi":True}],
   "Per cent. Existing regime against the exemption proposed in the Bill passed by the Lok Sabha, 6 August 2026.",188)],
 "flow":flow5("Fifteen years, two bourses.","The arithmetic it removes.","Cleared one house of two.",
   "Zero for fifteen years removes the calculation rather than lowering it.","The Diamonds Desk",
   "Zero for Antwerp: the tariff line that moved","a-zero-for-antwerp.html"),
 "desk":{"split":"the cheapest thing a government can give a diamond trade is certainty about where the paperwork happens"},
 "next":nxt("every-metal-runs-before-payrolls","Metals","Gold $4,314.50 and silver up 4.71% into an 8:30am payrolls print.",
   "the-tender-ladder","Rough","dubai-41-billion-year","Dubai")}

specs["every-metal-runs-before-payrolls"] = {
 **strip("By the numbers · Kitco spot, 5:58am New York",[
   {"fig":"$4,314.50","delta":"▲ +1.77%","dir":"up","lab":"gold, fifth session up"},
   {"fig":"$64.29","delta":"▲ +4.71%","dir":"up","lab":"silver, largest move"},
   {"fig":"$1,772.00","delta":"▲ +3.14%","dir":"up","lab":"platinum"},
   {"fig":"$1,382.00","delta":"▲ +2.14%","dir":"up","lab":"palladium"},
   {"fig":"67.1","lab":"gold to silver ratio, from 69.3"}]),
 "figs":[bars("Plate I","Session change by metal · 7 August 2026",[
   {"l":"SILVER","v":4.71,"d":"+4.71%","hi":True},
   {"l":"PLATINUM","v":3.14,"d":"+3.14%"},
   {"l":"PALLADIUM","v":2.14,"d":"+2.14%"},
   {"l":"GOLD","v":1.77,"d":"+1.77%"}],
   "Per cent against Thursday's close. Kitco spot, 5:58am New York, 7 August 2026.",189)],
 "flow":flow5("Five sessions up, and the leader returns.","A route and a jobs number.","Two marks, and a retail spread.",
   "The honest reading is that one red session in silver was noise rather than a turn.","The Gold & Metals Desk",
   "$4,270.90, a seven-week high, and silver alone in the red","a-silver-alone-in-the-red.html"),
 "desk":{"split":"a rally where the leader comes back after one down session is a rally with money still arriving"},
 "next":nxt("fifteen-years-no-tax","Diamonds","India offers foreign rough sellers fifteen years without income tax.",
   "silver-alone-in-the-red","Metals","the-fourteen-percent-that-isnt","Platinum")}

specs["one-thirty-two-against-three-thirty-nine"] = {
 **strip("By the numbers · China Gold Association, first half 2026",[
   {"fig":"132.13t","delta":"▼ −33.88%","dir":"down","lab":"gold jewellery"},
   {"fig":"339.34t","delta":"▲ +28.42%","dir":"up","lab":"bars and coins"},
   {"fig":"511.41t","delta":"▲ +1.23%","dir":"up","lab":"total consumption"},
   {"fig":"~136t","lab":"same half, World Gold Council"},
   {"fig":"2.6×","lab":"bars and coins over jewellery"}]),
 "figs":[bars("Plate I","China, first half 2026 · year-on-year change",[
   {"l":"BARS AND COINS","v":28.42,"d":"+28.42%"},
   {"l":"TOTAL CONSUMPTION","v":1.23,"d":"+1.23%"},
   {"l":"GOLD JEWELLERY","v":-33.88,"d":"−33.88%","hi":True}],
   "Per cent year on year. China Gold Association half-year figures, published 6-7 August 2026.",190)],
 "flow":flow5("More gold, far less jewellery.","Two authorities, four tonnes apart.","Why the value line hides it.",
   "Investment metal is now two and a half times the jewellery figure in the world's largest jewellery market.","The Gold & Metals Desk",
   "China's gold counter falls to its lowest since 2004","a-china-lowest-since-2004.html"),
 "desk":{"split":"Gold is winning and jewellery is losing, in the same market, at the same time"},
 "next":nxt("every-metal-runs-before-payrolls","Metals","Gold $4,314.50 and silver up 4.71% into an 8:30am payrolls print.",
   "china-lowest-since-2004","China","india-buys-fifteen-percent-less","India")}

specs["twenty-two-thirty-eight-an-order"] = {
 **strip("By the numbers · Brilliant Earth, second quarter 2026",[
   {"fig":"$115.1M","delta":"▲ +6%","dir":"up","lab":"revenue"},
   {"fig":"$2,238","delta":"▲ +8%","dir":"up","lab":"average order value"},
   {"fig":"−2.1%","dir":"down","lab":"total orders"},
   {"fig":"57.9%","delta":"▲ +360bps","dir":"up","lab":"gross margin, sequential"},
   {"fig":"$459–462M","lab":"full-year guidance, raised"}]),
 "figs":[bars("Plate I","Brilliant Earth Q2 2026 · year-on-year change",[
   {"l":"FINE JEWELLERY BOOKINGS","v":32,"d":"+32%","hi":True},
   {"l":"AVERAGE ORDER VALUE","v":8,"d":"+8%"},
   {"l":"REVENUE","v":6,"d":"+6%"},
   {"l":"TOTAL ORDERS","v":-2.1,"d":"−2.1%"}],
   "Per cent year on year. Company results, 6 August 2026.",191)],
 "flow":flow5("Fewer orders, higher tickets.","A negative order count, examined.","The same trade, made online.",
   "An eight percent rise in ticket against a two percent fall in orders is a business trading down its unit count deliberately and being paid for it.","The Retail Desk",
   "100 watches for 20 years: Brilliant Earth walks into horology","a-brilliant-earth-100-watches.html"),
 "desk":{"split":"raising annual guidance on a quarter with fewer orders is a bet that the high-ticket customer stays"},
 "next":nxt("twenty-nine-ninety-nine-at-the-counter","Retail","Lab-grown studs arrive at a $29.99 mall piercing counter.",
   "tiffany-goes-to-blue-nile","People","eighty-percent-to-the-consumer","Marketing")}

specs["the-fourteen-percent-that-isnt"] = {
 **strip("By the numbers · WPIC platinum jewellery outlook",[
   {"fig":"−14%","dir":"down","lab":"China 2026, as published"},
   {"fig":"−6%","dir":"down","lab":"global platinum jewellery 2026"},
   {"fig":"297koz","lab":"forecast 2026 market deficit"},
   {"fig":"$1,772.00","delta":"▲ +3.14%","dir":"up","lab":"platinum spot, 7 August"},
   {"fig":"41.1%","lab":"platinum as share of gold"}]),
 "figs":[bars("Plate I","Platinum jewellery 2026 forecast against the spot session",[
   {"l":"SPOT, 7 AUGUST SESSION","v":3.14,"d":"+3.14%"},
   {"l":"GLOBAL JEWELLERY, 2026","v":-6,"d":"−6%"},
   {"l":"CHINA JEWELLERY, 2026","v":-14,"d":"−14%","hi":True}],
   "Per cent. WPIC forecasts against Kitco spot change, 5:58am New York, 7 August 2026.",192)],
 "flow":flow5("A base effect, not a fall.","What the distinction decides.","A deficit the price is watching.",
   "The underlying trend in China is growth. The published headline is a base effect.","The Gold & Metals Desk",
   "Platinum adds 1.7%, gold slips: the white metals lead again","a-platinum-adds-one-seven.html"),
 "desk":{"split":"read WPIC's own footnote before quoting WPIC's own headline"},
 "next":nxt("every-metal-runs-before-payrolls","Metals","Gold $4,314.50 and silver up 4.71% into an 8:30am payrolls print.",
   "platinum-loses-its-teacher","Platinum","one-thirty-two-against-three-thirty-nine","China")}

specs["twenty-nine-ninety-nine-at-the-counter"] = {
 **strip("By the numbers · Claire's piercing relaunch",[
   {"fig":"$29.99","lab":"kits start, piercing free"},
   {"fig":"0.10ct","lab":"total weight, lab-grown studs"},
   {"fig":"14kt","lab":"white gold setting"},
   {"fig":"2nd","lab":"piercing overhaul in three years"},
   {"fig":"US + CA","lab":"rollout from August 2026"}]),
 "figs":[bars("Plate I","Where the starter stud sits",[
   {"l":"CLAIRE'S LAB-GROWN KIT","v":29.99,"d":"$29.99 with piercing","hi":True}],
   "Advertised entry price for a piercing kit, Claire's United States, August 2026.",193)],
 "flow":flow5("A mall chair, and a grown stone.","Why the price point is the story.","The tier-down, from the other end.",
   "Nobody buying at $29.99 is comparing certificates.","The Retail Desk",
   "Lab-grown finds its floor","a-lab-grown-finds-its-floor.html"),
 "desk":{"split":"the trade should stop treating each new lab-grown price floor as a natural diamond story"},
 "next":nxt("twenty-two-thirty-eight-an-order","Retail","Brilliant Earth turns a profit on fewer orders and a bigger ticket.",
   "sixty-one-percent-said-lab","Lab-grown","seventy-three-percent-cheaper","Price")}

# ---------------- validation ----------------
existing = {a["slug"] for a in articles} | {a["slug"] for a in NEW}
errs = []
for a in NEW:
    s = a["slug"]
    if len(a["body"]) != 5: errs.append("%s: body has %d paragraphs, need 5" % (s, len(a["body"])))
    if not a["body"][4].startswith("The desk's view:"): errs.append("%s: para 5 does not open 'The desk's view:'" % s)
    sp = specs.get(s)
    if not sp: errs.append("%s: no spec" % s); continue
    if sp["desk"]["split"] not in a["body"][4]: errs.append("%s: desk.split not verbatim in final paragraph" % s)
    pull = [b for b in sp["flow"] if "pull" in b][0]["pull"]["q"]
    if not any(pull in p for p in a["body"][:4]): errs.append("%s: pull quote not verbatim in paras 0-3" % s)
    for ref in [sp["next"]["lead"]["slug"]] + [m["slug"] for m in sp["next"]["minis"]]:
        if ref not in existing: errs.append("%s: next slug '%s' does not exist" % (s, ref))
        if ref == s: errs.append("%s: next slug self-references" % s)
if sum(1 for a in NEW if a.get("lead")) != 1: errs.append("lead count is not exactly 1 among new articles")
if sum(1 for a in NEW + articles if a.get("lead")) != 1: errs.append("lead count across articles.json is not exactly 1")
if errs:
    print("VALIDATION FAILED"); [print(" -", e) for e in errs]; sys.exit(1)

articles = NEW + articles
for s in specs: editorial[s] = specs[s]
(C/"articles.json").write_text(json.dumps(articles, ensure_ascii=False, indent=1))
(C/"editorial.json").write_text(json.dumps(editorial, ensure_ascii=False, indent=1))
print("OK: %d articles prepended, %d specs written, total %d" % (len(NEW), len(specs), len(articles)))
