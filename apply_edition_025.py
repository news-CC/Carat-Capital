#!/usr/bin/env python3
# Edition No. 025 - 2026-08-04. Prepends 7 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-04"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - the-one-carat-stops-falling ==========
art("the-one-carat-stops-falling","diamonds",True,"Lead Story · Diamonds Desk",5,"The Diamonds Desk",
["NUM","RECORD","VS"],
"The 1-carat stops falling: polished's best month since the tariffs",
"July ended a thirteen-month slide in the 1-carat index at flat, while 0.30-carat rose 1.6%, 0.50-carat rose 1.8% and 3-carat rose 0.2%. The first month since March 2025 with nothing falling.",
[
"Thirteen months of decline ended in July, and it ended level. The RapNet Diamond Index for 1-carat polished was unchanged across the month, closing a fall that had run without a single positive print since June 2025, on figures Rapaport published on Tuesday. The three other headline sizes moved up: 0.30-carat gained 1.6%, 0.50-carat gained 1.8% and 3-carat gained 0.2%. It is the first month since March 2025 in which none of the four fell, which makes July the best month for polished prices since the April 2025 tariff schedule began rearranging where a stone can profitably be cut.",
"The 0.50-carat print is the one to mark, because 1.8% is that size's largest monthly gain since March 2025 and because it belongs to the band the American engagement counter actually clears. This desk has now filed the same shape four times: smalls turning first on 14 July, smalls again on 24 July, and the thirties outrunning the ones on 27 July. What has changed is that the largest size in the set has stopped subtracting. A recovery led by 0.30-carat goods with the 1-carat still falling is a mix shift. A recovery in which the 1-carat holds is a floor.",
"Geography did some of the work, and the trade should be honest about which part. The tariff schedule in force since late July keeps 10% on polished goods finished in India while loose natural diamonds cut in Belgium, Botswana and Namibia clear at zero, a split this desk reported on 2 August. A price index measured on a network priced in dollars will reflect that gap before it reflects any change in consumer appetite. Some of July's gain is demand and some of it is a duty line, and nobody currently publishes a series that separates the two.",
"What has not been repaired is still the larger part of the picture. Lab-grown goods continue to take the entry price point, Chinese demand remains weak on the tonnage series, and Angolan rough is still clearing at volumes the polished market did not ask for. Rapaport reports American buying concentrated in 2-carat rounds in G to J colour and VS1 to SI2 clarity, plus fancy shapes, which is a narrow lane rather than a broad bid. Our own tape carries NAT1 at 5,232.00 unchanged for a sixth session, and for the first time this week that is a sourced flat rather than an absent print.",
"The desk's view: a flat month is not a recovery, it is the end of a decline, and the two are worth different amounts of inventory. Four categories that stopped falling in the same month have told you the sellers ran out of reasons to cut, not that the buyers arrived. The test is September, when the Vicenzaoro and Hong Kong calendars put real parcels in front of real budgets and the tariff-sorted origins get priced against each other in the same hall. Until then, treat July as the first month in more than a year that did not cost you money to hold goods."
],
[
 {"title":"Diamond Prices See Best Month Since Before Tariffs — Rapaport (4 August 2026)","url":"https://rapaport.com/news/diamond-prices-see-best-month-since-before-tariffs/"},
 {"title":"Latest News — Rapaport","url":"https://rapaport.com/all-news/"},
 {"title":"Rapaport Research Report: A Recovery in the Diamond Industry? — Rapaport","url":"https://rapaport.com/analysis/rapaport-research-report-a-recovery-in-the-diamond-industry/"},
])

# ========== 2. minus-point-one-for-color ==========
art("minus-point-one-for-color","gemstones",False,"Gemstones Desk · Fancy color",4,"The Gemstones Desk",
["NUM","VS"],
"Minus 0.1% for color: pinks rise, blues and yellows slip",
"The Fancy Color Research Foundation's second-quarter index moved one tenth of one percent. Pink gained 0.1%, blue lost 0.4%, yellow lost 0.3%. The widest single move in the set was a 1.3% fall in 2-carat blues.",
[
"The most illiquid corner of the diamond trade has just reported a quarter in which almost nothing happened, and that is the finding. The Fancy Color Research Foundation's index of pink, blue and yellow diamonds moved 0.1% lower across the second quarter of 2026. Pink rose 0.1%, blue fell 0.4%, yellow fell 0.3%, and the index moved one tenth of one percent. The foundation described a market that remained broadly stable. Against a natural colourless market that spent thirteen months falling and a lab-grown market that has lost most of its wholesale value since 2018, a flat quarter in colour is a competitive result rather than a dull one.",
"Pink is the only one of the three that turned, and it turned by size rather than by intensity. One and 1.5-carat pinks each added 0.4% while 2 and 3-carat pinks added 0.6%, which is the opposite of the pattern in colourless goods, where the small sizes have led every recent turn. On intensity, fancy-vivid pinks gained 0.5% and fancy-intense pinks lost 0.1%. The previous quarter had pink down 0.3%, so this is a reversal rather than a continuation, and it is the largest category in the index by traded value.",
"Blue is where the dispersion sits. The blue index fell 0.4% on a spread that runs from 1-carat stones up 0.7% to 2-carat stones down 1.3%, with 3-carat down 0.7% and 5-carat flat. Inside that, 1-carat fancy-vivid blues gained 1.5% while fancy and fancy-intense blues each lost 0.6%. A 2.8 point gap between the best and worst blue sub-categories in a single quarter, in a market where a handful of stones can constitute a quarter's evidence, is the honest measure of how thin this tape is. Yellow was the quietest of the three, down 0.3% for a second consecutive quarter, with 3-carat yellows up 0.7% against fancy-intense yellows down 1.3%.",
"For the counter, the useful comparison is not quarter on quarter but category against category. Coloured stones proper have been running at two speeds since the spring, with a 6.59-carat Kashmir sapphire clearing $906,250 at Heritage in May while members of the International Colored Gemstone Association reported demand roughly 30% below 2022. Fancy colour diamonds have done neither. They have not printed a trophy result this quarter and they have not repriced downward. The index has been embedded in cutting-and-planning software since July, which means a cutter can now see the same number the trader sees before the wheel touches the rough.",
"The desk's view: stability at this level is a statement about liquidity, not about value. An index that moves a tenth of a percent across three months is describing a market where very little changed hands, and the sub-category spreads confirm it, because 1-carat fancy-vivid blues up 1.5% alongside 2-carat blues down 1.3% is not a trend, it is a sample size. Read the direction, ignore the decimal, and price the individual stone. Fancy colour has always been a market of specific goods rather than of averages, and this quarter it did the trade the courtesy of not pretending otherwise."
],
[
 {"title":"Fancy-Color Price Index Holds Steady in Second Quarter — Rapaport (3 August 2026)","url":"https://rapaport.com/news/fancy-color-price-index-holds-steady-in-second-quarter/"},
 {"title":"Fancy Color Research Foundation","url":"https://www.fcresearch.org/"},
 {"title":"An Incongruous Moment for the Gemstone Industry — Rapaport Magazine","url":"https://rapaport.com/magazine-article/an-incongruous-moment-for-the-gemstone-industry/"},
])

# ========== 3. independents-pass-lvmh ==========
art("independents-pass-lvmh","watches",False,"Watches Desk · Secondary market",5,"The Watches Desk",
["NUM","VS","STAKES"],
"$633.8 million for the independents, more than LVMH's watches",
"EveryWatch puts the first-half secondary market at $10.5 billion, up 37.2%. Independent makers took $633.8 million of it, up 89%, with F.P. Journe alone at $201.6 million on a median sale price of $215,000.",
[
"The pre-owned watch market has spent three years as the industry's cold room, and the first half of 2026 says the door is open. EveryWatch, which compiles sold prices from about 650 dealers and roughly 470 auction houses, put global secondary transactions at $10.5 billion for the six months, up 37.2% year on year, in a report published on 30 July and taken up by the trade press this week. The median watch sold for $5,900, up 19%, and took 43 days to sell against 39 a year ago. Value grew faster than volume, which means the money moved up the price ladder rather than across more wrists.",
"The line that reorders the table sits below the giants. Independent watchmakers sold $633.8 million on the secondary market in the first half, up 89%, and that is more than the entire LVMH watch portfolio, which transacted about $617 million over the same period. A group of workshops that between them build a few thousand watches a year now clears more second-hand value than the owner of Tag Heuer, Hublot, Zenith and Bulgari. Nothing about that says LVMH is shrinking. It says the resale market has stopped treating brand scale as the thing it pays for.",
"Almost all of the independent growth has one name on it. F.P. Journe transacted $201.6 million, close to triple the prior year at a reported 196.9% increase, which places the 27-year-old Geneva house seventh among all watch brands by secondary value. Its median sale price rose 82% to $215,000 and its turnover rate ran above 57%, meaning more than half the Journe watches offered found a buyer while the price was climbing. Behind it the field is much smaller: H. Moser and Cie. at $26 million, up 64%, Parmigiani Fleurier at $21 million, up 60%, and De Bethune at $19 million, up 2%.",
"The scale of the market still belongs where it always has. Rolex accounted for $4.29 billion, about 41% of all secondary value, with Patek Philippe at $1.51 billion and Audemars Piguet at $983 million. Rolex certified pre-owned alone did $385 million, more than double the prior year, which is the manufacturer taking margin out of the grey market by joining it. Geography split as sharply as brand did: the United States and Canada transacted $4.5 billion, up 70%, while Asia fell 2.6%. EveryWatch cofounder Giovanni Prigigallo credits \"a new wave of collectors, many from tech\".",
"The desk's view: scarcity that was never manufactured is the only kind the secondary market still pays for. A house that cannot increase output without changing what it is has a supply constraint no marketing department invented, and buyers are now paying an 82% higher median for exactly that quality. The instructive number is not Journe's total but its 57% turnover, because a rising price with a falling clearance rate is speculation and a rising price with a rising clearance rate is demand. Retailers reading this should note where the American 70% went, and that it did not go to the middle of the catalogue."
],
[
 {"title":"Secondary Watch Market Surges: Independents Outpace Luxury Giants — JCK (3 August 2026)","url":"https://www.jckonline.com/editorial-article/secondary-watch-market-growth/"},
 {"title":"The secondary market is back on the rise, at least $1M+ lots are — Time+Tide","url":"https://timeandtidewatches.com/the-secondary-market-is-back-on-the-rise-at-least-1m-lots-are"},
 {"title":"Analytics — Reports — EveryWatch","url":"https://everywatch.com/analytics/reports"},
])

# ========== 4. one-point-two-million-apply ==========
art("one-point-two-million-apply","watches",False,"Watches Desk · Distribution",4,"The Watches Desk",
["NUM","GAP","HOWTO"],
"1.2 million apply for 1,969 watches, and nobody queued",
"Swatch put its MoonSwatch 1969 behind a 32-question online form. More than 1.2 million people completed it for 1,969 pieces at $570, roughly 600 applicants per watch, three months after crowds forced 15 US stores shut.",
[
"Swatch has replaced the queue with a questionnaire, and the arithmetic is worth writing down. To buy one of 1,969 MoonSwatch Mission to the Moon 1969 pieces, a customer had to complete the Electronic Swatch Timepiece Application, a 32-question online form. More than 1.2 million people finished it. About six hundred people applied for every watch available. The retail price is $570, a figure Swatch derived from the gold price on 21 July 1969, and JCK reports the watch carries 11 grams of 18-karat gold across the dial, hands, crown and pushers.",
"That metal claim deserves a bench check, because it inverts the usual accounting. Eleven grams of 18-karat is 8.25 grams of fine gold. At Tuesday's Kitco spot of $4,048.80 an ounce, or $130.17 a gram, the fine content alone is worth about $1,074, which is close to twice the ticket. Swatch is not selling a watch at a margin on materials. It is selling a date, and pricing the object at what the metal cost on the morning of the moon landing rather than at what it costs now. The scarcity is the edition size and the price is the storytelling.",
"The contrast is three months old and still bruising. The Royal Pop collaboration with Audemars Piguet in May drew crowds that required police outside stores in New York, Paris and London, closed 15 American shops on a Saturday, and produced trading at four to five times retail within days. JCK reports that same watch changing hands below $400 by August. Swatch Group stock rose about 15% in the two weeks after the launch, so the event worked as a market signal and failed as a customer experience, and the resale collapse suggests most of the queue was there for the flip rather than the watch.",
"What the form actually collects is the point most of the coverage missed. A 32-question application completed 1.2 million times is a verified, self-selected, freely given database of watch buyers, their tastes and their intent, delivered at no acquisition cost against 1,969 units of inventory. Eugene Tutunikov of SwissWatchExpo, quoted by JCK, put it plainly: \"nobody slept on a sidewalk.\" The allocation problem every hot-product retailer faces was solved with a web form, and the byproduct is worth more than the run.",
"The desk's view: the quiz is not a lottery, it is a customer database with a watch attached, and any jeweller with a waiting list should be reading it that way. The mechanic is portable to a single-door independent with a limited drop and no security budget, and it converts the two things a queue destroys, which are staff safety and customer goodwill, into two things a shop can use, which are data and a reason to email. The failure mode is equally clear. Six hundred to one means 599 disappointed applicants per sale, and none of them are strangers any more."
],
[
 {"title":"Experts Share What Swatch Is Doing Right (and Wrong) — JCK (3 August 2026)","url":"https://www.jckonline.com/editorial-article/swatch-moonswatch-quiz/"},
 {"title":"A \"Failed Launch\"? Swatch Encounters Chaos on Royal Pop Release Day — JCK","url":"https://www.jckonline.com/editorial-article/royal-pop-debut-deemed-a-fail/"},
 {"title":"Precious Metals Spot Prices — Kitco (4 August 2026, 5:59am New York)","url":"https://www.kitco.com/price/precious-metals"},
])

# ========== 5. seventy-three-lots-over-a-million ==========
art("seventy-three-lots-over-a-million","auctions",False,"Auctions Desk · Watches",4,"The Auctions Desk",
["NUM","RECORD"],
"73 lots over a million: the watch auction room reflates",
"EveryWatch puts first-half watch auction sales at $680 million, up 45%. Seventy-three lots cleared $1 million against roughly 25 a year earlier, three passed $10 million, and the median watch sold for $5,900.",
[
"The watch auction room has had its best six months since the boom, and it has had them at the top of the book. EveryWatch's first-half report puts auction sales at $680 million, up 45% year on year, inside a total secondary market of $10.5 billion. Seventy-three lots cleared a million dollars in six months, close to three times last year's count. Three lots passed $10 million. Against a dealer market that grew 37.2%, the salerooms grew faster, which reverses the pattern of the past two years when auction was the segment shedding value while dealers held the floor.",
"The record at the top of that column is one this desk filed on 9 July. An F.P. Journe Chronometre a Resonance Souscription, number 007, made $13,922,000 at Phillips New York on 14 June, the highest price ever paid at auction for a watch by an independent maker. It is not an isolated result: Phillips also placed a Resonance Souscription number 18 at $6.3 million and a Resonance Pisa at $3 million across the spring season. One workshop supplied a meaningful share of the seven-figure lots in a half that had 73 of them.",
"Underneath the trophies the market is behaving normally, which is the more useful signal. The median watch across all channels sold for $5,900, up 19%, and took 43 days to move against 39 a year earlier. A rising median with a slightly slower clock describes a market absorbing higher prices rather than chasing them, and it sits consistently with the dealer-side picture of value growing faster than unit volume. EveryWatch compiles from sold results rather than asking prices, drawing on about 650 dealers and roughly 470 auction houses, which is why the figures are worth more than the usual index snapshot.",
"For consignors the practical read is about where the estimate should sit. Heritage booked a record half in jewellery, Phillips took $235 million across the spring watch season, and the million-dollar count has tripled, but none of that has repriced the middle of the catalogue, where the median is still under six thousand dollars and the clock has slowed by four days. The lot that benefits from this market is the one with a name, a serial number and a story that can be checked. The lot that does not is the good watch with no argument attached to it.",
"The desk's view: the auction room is not recovering broadly, it is recovering at the top, and a 45% headline hides a market that has become two markets. Seventy-three seven-figure lots is a statement about a few hundred buyers, not about the trade. If you are placing goods, place the extraordinary piece at auction and sell the ordinary one across the counter, because the salerooms are currently paying a premium for provenance and charging a discount for everything else. That spread will close, and it will close from the top."
],
[
 {"title":"Secondary Watch Market Surges: Independents Outpace Luxury Giants — JCK (3 August 2026)","url":"https://www.jckonline.com/editorial-article/secondary-watch-market-growth/"},
 {"title":"The secondary market is back on the rise, at least $1M+ lots are — Time+Tide","url":"https://timeandtidewatches.com/the-secondary-market-is-back-on-the-rise-at-least-1m-lots-are"},
 {"title":"An F.P. Journe Chronometre a Resonance Sells for $13.9 Million at Phillips — Robb Report","url":"https://robbreport.com/style/watch-collector/f-p-journe-chronometre-a-resonance-13-9-million-1238353415/"},
])

# ========== 6. platinum-adds-one-seven ==========
art("platinum-adds-one-seven","gold-metals",False,"Gold & Metals Desk · The tape",4,"The Bullion Desk",
["NUM","VS"],
"Platinum adds 1.7%, gold slips: the white metals lead again",
"At 5:59am New York, gold bid $4,048.80, down 0.14%. Platinum is $1,655.00, up 1.72%, palladium $1,266.00, up 1.77%, and silver $58.63, up 0.97%. ADP lands Wednesday, payrolls Friday.",
[
"Three of the four precious metals are higher and the one that matters most to a jewellery counter is not. At 5:59am New York time on Tuesday, Kitco's spot page had gold bid at $4,048.80 an ounce, down $5.70 or 0.14% against Monday's close. Platinum bid $1,655.00, up $28.00 or 1.72%. Palladium bid $1,266.00, up $22.00 or 1.77%. Silver bid $58.63, up 56.3 cents or 0.97%. Gold is the only one of the four that is lower, and it is lower by fourteen hundredths of a percent, which is the market saying nothing rather than saying down.",
"The ratios are where the movement shows. Gold to silver has tightened to about 69.0 ounces from 69.8 on Monday, and platinum now sits at 40.9% of the gold price, its firmest reading in this run. Trading Economics, quoting a different print time on the same session, has platinum up 2.56% and silver up 1.83%, both larger than Kitco's figures, while agreeing with Kitco on gold to the basis point at minus 0.14%. Two sources agree on gold to the basis point and disagree on silver by nearly a full percent, which is the ordinary condition of a fragmented spot market and a reason to name your source every time you quote a level.",
"The week is built around American labour data. The ADP national employment report lands on Wednesday and the Bureau of Labor Statistics releases non-farm payrolls on Friday, the first full read on hiring since the Federal Reserve held rates on 29 July with three dissents. Gold has now spent six sessions inside a range it entered after that decision. On the longer view Trading Economics has gold down about 2.8% over the past month but up 19.8% on the year, silver down 5.3% on the month and up 55.3% on the year, and platinum up 26.8% on the year.",
"At the bench, gold at $4,048.80 an ounce is $130.17 a gram of fine metal before refining, alloy, loss and making charge, against $130.32 on Monday morning. The white metals are the ones changing a costing sheet this week. Silver approaching $59 puts real money on the raw material of a sterling line in a way it never does on a gold chain, and platinum through $1,650 narrows the discount that has made platinum bridal an easy substitution argument for two years. A ring quoted on last month's platinum figure is now quoted wrong.",
"The desk's view: this tape prints Kitco's 5:59am New York spot rather than a settlement, and it says so on the line, because Monday's close is not published to this desk as a discrete figure and deriving one by arithmetic from a change field would be inventing a number. That is the third consecutive edition carrying a live quotation rather than a close, and it is a standing weakness in the process rather than a judgement call. NAT1 and LGD1 both carry unchanged, NAT1 for the sourced reason that the RapNet 1-carat index was flat across July. Friday's payroll print is the number worth waiting for."
],
[
 {"title":"Precious Metals Spot Prices — Kitco (4 August 2026, 5:59am New York)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Gold — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/gold"},
 {"title":"Platinum — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/platinum"},
 {"title":"Silver — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/silver"},
])

# ========== 7. thirteen-hundred-brands-and-a-centenary ==========
art("thirteen-hundred-brands-and-a-centenary","retail-tech",False,"Retail & Tech Desk · The calendar",4,"The Retail Desk",
["NUM","ACTOR"],
"1,300 brands and a centenary: Vicenzaoro opens Hall 2",
"Vicenzaoro September runs 4 to 8 September with about 1,300 brands from 38 countries, buyers from more than 130, the new Hall 2 in full use and T.Gold moved on site. CIBJO's centenary congress sits inside it.",
[
"The next real test of the trade's summer numbers has a date and a floor plan. Vicenzaoro September runs from 4 to 8 September at Fiera di Vicenza, with roughly 1,300 exhibiting brands from 38 countries and buyers expected from more than 130, on figures the Italian Exhibition Group gave JCK on 13 July. The show was reported close to sold out in late May, more than three months ahead. Two structural changes land at once: the new Hall 2, a two-storey central hub connected by covered walkways, is fully operational for the first time, and T.Gold has moved inside the expo centre grounds.",
"The T.Gold move is the one manufacturers should read. The machinery and technology section for precious-metal production has run as a separate proposition and now sits in Hall 4 alongside the finished goods, which puts casting, laser and setting equipment in the same building as the brands that buy the output. Jewellery Outlook reported both the integration and the Hall 2 timetable on 31 July, confirming through interviews that neither has slipped. For a show that has spent three years arguing it represents the whole supply chain rather than a display of Italian goldsmithing, this is the edition where the claim gets tested against a floor plan.",
"Sharing the site is a hundredth birthday with a rulebook attached. CIBJO, the World Jewellery Confederation, holds its centenary congress in Vicenza from 4 to 7 September, a century after its founding in 1926. The congress that writes the Blue Books turns one hundred in the hall next door. Its Assembly of Delegates and sectoral commissions meet there, and amendments to the Blue Books, the international standards covering diamonds, coloured stones and pearls, are introduced at exactly these sessions. The scheduled agenda covers the state of the diamond industry, lab-grown diamonds, the supply chain, pearls and coloured gemstones.",
"That agenda is not ceremonial this year. Russia's Resolution 657 comes into force on 1 September, three days before the congress opens, banning the word diamond and its derivatives for synthetics sold there and requiring weight in grams. CIBJO's own president has been arguing publicly for synthetic over lab-grown as the correct term. A standards body meets to debate nomenclature in the same week a G20 economy stops waiting for it, which changes what the room is deciding. Delegates are no longer choosing between a rule and no rule. They are choosing between a global rule and a set of national ones.",
"The desk's view: a standards congress is where the lab-grown naming fight gets settled, and Russia has already moved, which means Vicenzaoro in September is the most consequential week on the calendar between now and Hong Kong. Buyers should go for the price discovery, because September is the first hall since the July tariff schedule where Belgian, Botswanan and Indian goods sit within walking distance of each other and get quoted against the same budget. Manufacturers should go for Hall 4. Everyone else should watch what the commissions write down, because that language will be on labels for a decade."
],
[
 {"title":"Vicenzaoro Organizers Eager for New Hall, CIBJO in September — JCK (13 July 2026)","url":"https://www.jckonline.com/editorial-article/vicenzaoro-september-2026/"},
 {"title":"CIBJO's Centenary Congress to be held in Vicenza, Italy, from September 4 to 7, 2026 — CIBJO","url":"https://cibjo.org/cibjos-centenary-congress-to-be-held-in-vicenza-italy-from-september-4-to-7-2026/"},
 {"title":"INTERVIEW: Machinery area T.Gold integrated into main Vicenzaoro site from September 2026 edition — Jewellery Outlook (31 July 2026)","url":"https://jewelleryoutlook.com/interview-machinery-area-t-gold-integrated-into-main-vicenzaoro-site-from-september-2026-edition/"},
 {"title":"CIBJO: the centenary congress at Vicenzaoro September — Vicenzaoro","url":"https://www.vicenzaoro.com/en/news-detail/cibjo-the-centenary-congress-at-vicenzaoro-september?newsId=7057497"},
])

# ---------------- EDITORIAL SPECS ----------------
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

specs["the-one-carat-stops-falling"] = {
 **strip("By the numbers · RapNet Diamond Index, July 2026",[
   {"fig":"0.0%","lab":"1-carat, ends 13 months down"},
   {"fig":"+1.8%","dir":"up","lab":"0.50-carat, best since Mar 2025"},
   {"fig":"+1.6%","dir":"up","lab":"0.30-carat"},
   {"fig":"+0.2%","dir":"up","lab":"3-carat"},
   {"fig":"Mar 2025","lab":"last month none fell"}]),
 "figs":[bars("Plate I","RAPI monthly change, by size",[
   {"l":"0.50 CARAT","v":1.8,"d":"+1.8%","hi":True},
   {"l":"0.30 CARAT","v":1.6,"d":"+1.6%"},
   {"l":"3 CARAT","v":0.2,"d":"+0.2%"},
   {"l":"1 CARAT","v":0.0,"d":"flat"}],
   "July 2026, per cent. Rapaport, published 4 August 2026.",178)],
 "flow":flow5("Thirteen months, ended level.","Some of it is a duty line.","What is still not repaired.",
   "It is the first month since March 2025 in which none of the four fell","The Diamonds Desk",
   "Small stones lead again","a-small-stones-lead-again.html"),
 "desk":{"split":"a flat month is not a recovery, it is the end of a decline"},
 "next":nxt("thirties-outrun-the-ones","Polished","The 0.30-carat band turned first, and turned hardest.",
   "zero-for-antwerp","Tariffs","lab-grown-finds-its-floor","Lab-grown")}

specs["minus-point-one-for-color"] = {
 **strip("By the numbers · FCRF index, Q2 2026",[
   {"fig":"−0.1%","dir":"down","lab":"overall index"},
   {"fig":"+0.1%","dir":"up","lab":"pink, from −0.3%"},
   {"fig":"−0.4%","dir":"down","lab":"blue"},
   {"fig":"−0.3%","dir":"down","lab":"yellow, second quarter running"},
   {"fig":"−1.3%","dir":"down","lab":"2-carat blue, widest move"}]),
 "figs":[bars("Plate I","Second-quarter change, by colour",[
   {"l":"PINK","v":0.1,"d":"+0.1%","hi":True},
   {"l":"OVERALL","v":-0.1,"d":"−0.1%"},
   {"l":"YELLOW","v":-0.3,"d":"−0.3%"},
   {"l":"BLUE","v":-0.4,"d":"−0.4%"}],
   "Per cent, Q2 2026. Fancy Color Research Foundation via Rapaport, 3 August 2026.",179)],
 "flow":flow5("A quarter in which nothing happened.","Blue is where the dispersion sits.","Category against category.",
   "Pink rose 0.1%, blue fell 0.4%, yellow fell 0.3%, and the index moved one tenth of one percent.","The Gemstones Desk",
   "Two speeds in colour","a-color-runs-two-speeds.html"),
 "desk":{"split":"stability at this level is a statement about liquidity, not about value"},
 "next":nxt("fancy-color-gets-a-tape","Pricing","FCRF prices now sit inside the planning software.",
   "color-runs-two-speeds","Colour","twelve-point-five-for-color","Demand")}

specs["independents-pass-lvmh"] = {
 **strip("By the numbers · secondary market, H1 2026",[
   {"fig":"$10.5B","dir":"up","lab":"total, +37.2%"},
   {"fig":"$633.8M","dir":"up","lab":"independents, +89%"},
   {"fig":"$617M","lab":"LVMH watch portfolio"},
   {"fig":"$201.6M","dir":"up","lab":"F.P. Journe, 7th overall"},
   {"fig":"$215,000","dir":"up","lab":"Journe median, +82%"}]),
 "figs":[bars("Plate I","Secondary-market value, H1 2026",[
   {"l":"ROLEX","v":4290,"d":"$4.29B, 41%","hi":True},
   {"l":"PATEK PHILIPPE","v":1510,"d":"$1.51B"},
   {"l":"AUDEMARS PIGUET","v":983,"d":"$983M"},
   {"l":"INDEPENDENTS","v":634,"d":"$633.8M, +89%"},
   {"l":"LVMH WATCHES","v":617,"d":"$617M"}],
   "US dollars, millions. EveryWatch H1 2026 report via JCK.",180)],
 "flow":flow5("The door is open.","One name, almost all the growth.","Scale still belongs where it was.",
   "Independent watchmakers sold $633.8 million on the secondary market in the first half, up 89%, and that is more than the entire LVMH watch portfolio","The Watches Desk",
   "List up, resale down","a-list-up-resale-down.html"),
 "desk":{"split":"scarcity that was never manufactured is the only kind the secondary market still pays for"},
 "next":nxt("cartier-secondhand-heat","Pre-owned","Cartier's heat built 3.5 times faster than any rival.",
   "list-up-resale-down","Prices","crown-premium-shrinks","Rolex")}

specs["one-point-two-million-apply"] = {
 **strip("By the numbers · MoonSwatch 1969",[
   {"fig":"1.2M+","dir":"up","lab":"completed applications"},
   {"fig":"1,969","lab":"pieces worldwide"},
   {"fig":"600:1","lab":"applicants per watch"},
   {"fig":"$570","lab":"retail, priced off July 1969"},
   {"fig":"~$1,074","dir":"up","lab":"fine gold content at spot"}]),
 "figs":[bars("Plate I","The 1969 ticket against its metal",[
   {"l":"FINE GOLD CONTENT","v":1074,"d":"~$1,074","hi":True},
   {"l":"RETAIL PRICE","v":570,"d":"$570"}],
   "8.25g fine from 11g of 18-karat, at Kitco spot $4,048.80/oz, 4 August 2026.",181)],
 "flow":flow5("A questionnaire instead of a queue.","Three months ago, the sidewalk.","What the form actually collects.",
   "About six hundred people applied for every watch available.","The Watches Desk",
   "Swatch's split screen","a-swatch-nine-up-six-down.html"),
 "desk":{"split":"the quiz is not a lottery, it is a customer database with a watch attached"},
 "next":nxt("swatch-nine-up-six-down","Results","Nine percent growth, sixteen million of profit.",
   "ap-105-million-paradox","Audemars","guess-lets-the-machine-draw","Retail")}

specs["seventy-three-lots-over-a-million"] = {
 **strip("By the numbers · watch auctions, H1 2026",[
   {"fig":"$680M","dir":"up","lab":"auction sales, +45%"},
   {"fig":"73","dir":"up","lab":"lots over $1 million"},
   {"fig":"3","dir":"up","lab":"lots over $10 million"},
   {"fig":"$5,900","dir":"up","lab":"median watch, +19%"},
   {"fig":"43 days","dir":"up","lab":"average time to sell, from 39"}]),
 "figs":[bars("Plate I","Where the top of the book cleared",[
   {"l":"JOURNE RESONANCE 007","v":13.92,"d":"$13.92M","hi":True},
   {"l":"RESONANCE No. 18","v":6.3,"d":"$6.3M"},
   {"l":"RESONANCE PISA","v":3.0,"d":"$3.0M"}],
   "US dollars, millions. Phillips spring season 2026, via Robb Report.",182)],
 "flow":flow5("Best six months since the boom.","Underneath the trophies.","Where the estimate should sit.",
   "Seventy-three lots cleared a million dollars in six months, close to three times last year's count.","The Auctions Desk",
   "Phillips takes $235 million","a-phillips-235-million-spring.html"),
 "desk":{"split":"the auction room is not recovering broadly, it is recovering at the top"},
 "next":nxt("phillips-235-million-spring","Season","A $235 million spring, and the record that came with it.",
   "heritage-books-a-record-half","Heritage","trophy-lots-carry-the-half","Trophies")}

specs["platinum-adds-one-seven"] = {
 **strip("The tape · 4 August, 5:59am New York",[
   {"fig":"$4,048.80","dir":"down","lab":"gold, −0.14%"},
   {"fig":"$1,655.00","dir":"up","lab":"platinum, +1.72%"},
   {"fig":"$1,266.00","dir":"up","lab":"palladium, +1.77%"},
   {"fig":"$58.63","dir":"up","lab":"silver, +0.97%"},
   {"fig":"69.0","dir":"down","lab":"gold to silver ratio"}]),
 "figs":[bars("Plate I","Day change, 4 August",[
   {"l":"PALLADIUM","v":1.77,"d":"+1.77%","hi":True},
   {"l":"PLATINUM","v":1.72,"d":"+1.72%"},
   {"l":"SILVER","v":0.97,"d":"+0.97%"},
   {"l":"GOLD","v":-0.14,"d":"−0.14%"}],
   "Per cent against Monday's close. Kitco spot, 5:59am New York, 4 August 2026.",183)],
 "flow":flow5("Three up, and not the one that matters.","The week is labour data.","What it costs at the bench.",
   "Gold is the only one of the four that is lower, and it is lower by fourteen hundredths of a percent","The Bullion Desk",
   "Silver leads the reopen","a-silver-leads-the-reopen.html"),
 "desk":{"split":"deriving one by arithmetic from a change field would be inventing a number"},
 "next":nxt("silver-leads-the-reopen","The tape","Monday's reopen, with silver in front.",
   "gold-waits-on-payrolls","Payrolls","white-metals-close-the-month","White metals")}

specs["thirteen-hundred-brands-and-a-centenary"] = {
 **strip("By the numbers · Vicenzaoro September",[
   {"fig":"4-8 Sept","lab":"Fiera di Vicenza"},
   {"fig":"~1,300","lab":"brands, 38 countries"},
   {"fig":"130+","lab":"buyer countries expected"},
   {"fig":"Hall 2","lab":"in full use for the first time"},
   {"fig":"100","lab":"years of CIBJO, founded 1926"}]),
 "figs":[bars("Plate I","The September floor",[
   {"l":"BRANDS EXHIBITING","v":1300,"d":"~1,300","hi":True},
   {"l":"BUYER COUNTRIES","v":130,"d":"130+"},
   {"l":"EXHIBITOR COUNTRIES","v":38,"d":"38"}],
   "Italian Exhibition Group figures via JCK, 13 July 2026.",184)],
 "flow":flow5("A date and a floor plan.","A hundredth birthday with a rulebook.","Not ceremonial this year.",
   "The congress that writes the Blue Books turns one hundred in the hall next door.","The Retail Desk",
   "Say synthetic, not lab-grown","a-say-synthetic-not-lab-grown.html"),
 "desk":{"split":"a standards congress is where the lab-grown naming fight gets settled, and Russia has already moved"},
 "next":nxt("russia-bans-the-word","Nomenclature","Moscow strikes the word diamond from synthetic labels.",
   "say-synthetic-not-lab-grown","CIBJO","dubai-diamond-week-returns","Calendar")}

# ---------------- VALIDATE specs ----------------
allslugs = set(a["slug"] for a in articles) | set(a["slug"] for a in NEW)
errs=[]
for d in NEW:
    s=d["slug"]; sp=specs[s]; body=d["body"]; n=len(body)
    ps=[f["p"] for f in sp["flow"] if "p" in f]
    if sorted(ps)!=list(range(n-1)): errs.append(f"{s}: flow paras {sorted(ps)} != {list(range(n-1))}")
    pq=[f["pull"]["q"] for f in sp["flow"] if "pull" in f][0]
    if not any(pq in body[i] for i in range(n-1)): errs.append(f"{s}: pull not verbatim")
    if sp["desk"]["split"] not in body[-1]: errs.append(f"{s}: desk split not in last para")
    if not body[-1].startswith("The desk's view:"): errs.append(f"{s}: last para not desk's view")
    _href=[f["also"]["href"] for f in sp["flow"] if "also" in f][0]
    also=_href[2:-5] if _href.startswith("a-") and _href.endswith(".html") else _href
    if also not in allslugs: errs.append(f"{s}: also slug {also} missing")
    for m in [sp["next"]["lead"]["slug"]]+[x["slug"] for x in sp["next"]["minis"]]:
        if m not in allslugs: errs.append(f"{s}: next slug {m} missing")
        if m==s: errs.append(f"{s}: next points to self")
    # house style checks
    joined=" ".join(body)+" "+d["title"]+" "+d["dek"]
    if "!" in joined: errs.append(f"{s}: exclamation mark")
    if joined.count("—") > 1: errs.append(f"{s}: {joined.count(chr(8212))} em-dashes (max 1)")
    for w in ["insane","stunning","shocking","incredible","unbelievable"]:
        if w in joined.lower(): errs.append(f"{s}: hype word '{w}'")
    if len(d["dek"].split()) > 40: errs.append(f"{s}: dek {len(d['dek'].split())} words > 40")
    wc=len(" ".join(body).split())
    if not (330 <= wc <= 620): errs.append(f"{s}: body {wc} words outside 330-620")
    if len(d["title"].split()) > 11: errs.append(f"{s}: title {len(d['title'].split())} words > 11")
if errs:
    print("SPEC ERRORS:"); [print(" -",e) for e in errs]; sys.exit(1)

# ---------------- PREPEND + write ----------------
articles = NEW + articles
leads=[a["slug"] for a in articles if a.get("lead")]
assert leads==["the-one-carat-stops-falling"], f"lead set wrong: {leads}"
for s in specs: editorial[s]=specs[s]

(C/"articles.json").write_text(json.dumps(articles,ensure_ascii=False,indent=1))
(C/"editorial.json").write_text(json.dumps(editorial,ensure_ascii=False,indent=1))
print("articles now:",len(articles)," specs now:",len(editorial)," lead:",leads)
for d in NEW: print("  ",d["desk"].ljust(12), str(len(" ".join(d["body"]).split())).rjust(4),"w  ",d["slug"])
print("OK")
