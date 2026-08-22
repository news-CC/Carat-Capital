#!/usr/bin/env python3
# Edition No. 041 - 2026-08-22. Prepends 6 articles.
import json, pathlib
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())

DATE = "2026-08-22"
for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    assert len(body) == 5, slug
    assert body[-1].startswith("The desk's view:"), slug
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

KIT = {"title":"Gold, Silver, Platinum & Palladium spot prices - Kitco (read 22 August 2026; source timestamp 21 August 17:00 UTC)","url":"https://www.kitco.com/price/precious-metals"}

# ========== 1. LEAD - four-five-five-four-in-beijing ==========
art("four-five-five-four-in-beijing","gold-metals",True,"Lead Story · Gold & Metals Desk",5,"The Gold & Metals Desk",
["NUM","VS"],
"Gold breaks $4,550 in Beijing and adds $47.96 more by New York",
"Eastmoney timestamped spot gold at $4,554.44 on Friday's Beijing afternoon. This paper's tape carries Friday's last New York print at $4,602.40, up $20.80. Same session, ten hours apart, and both are printed.",
[
"Spot gold broke through $4,550 an ounce during Friday's Beijing afternoon and kept going after China went home. Eastmoney, timestamped 14:51 on 21 August, put the metal at $4,554.441 an ounce, up 0.8%, with COMEX futures at $4,598.4, up 0.59%. The drivers it names are the US Treasury's expansion of its liquidity-support repurchase operations from $20 billion to $40 billion, falling long-end Treasury yields, a weaker dollar, a repricing of fiscal risk, and visible policy disagreement inside the Federal Reserve, with US federal debt passing $40 trillion sitting underneath all of it. This paper's own mark of record for the same session, taken from Kitco's board and re-read at press time this morning, is $4,602.40. Saturday is not a trading day and there is no fresher number in existence.",
"The two figures are the same rally at different hours, and the distance between them is the story. Beijing's 14:51 is 02:51 in New York, roughly ten hours before Friday's last print. Gold was at $4,554.44 when the Chinese wire wrote it up and $4,602.40 when the New York board stopped moving: $47.96 higher, a further 1.05%, this desk's arithmetic on the two published readings. Against this paper's 21 August mark of record, Friday's close is up $20.80 or 0.45%. Silver went the other way, down $0.45 or 0.65% to $68.86, which widens the gold-to-silver ratio to 66.84 from 66.10, this desk's division of its own two marks. Platinum and palladium are held at $1,881.00 and $1,336.00 because Kitco and TradingEconomics sit $18.70 and $19.50 apart on them, gaps of 1.00% and 1.47%, and a mark no second page corroborates is not written.",
"The Chinese retail counter is where the rally is landing hardest. Eastmoney carries Chow Sang Sang's pure gold jewellery at 1,365 yuan a gram, up 6 yuan after a 46-yuan jump the day before, 52 yuan across two sessions. This paper reported the same counter at 1,285 yuan a gram on 8 August, alongside Chow Tai Fook at 1,286 and four other brands within five yuan of both. That is 80 yuan a gram, or 6.23%, added in thirteen days, on this desk's comparison of its own published record against Friday's quotation. What was described here two weeks ago as a collectively held floor moving on its own schedule has moved again, and it has moved with the metal rather than lagging it, which is not what these counters did through most of the past year.",
"The Gulf leg of the same session is thinner evidence and is labelled as such. Ghorba News, dated in its own text to Friday 21 August, carries UAE retail gold at 538.46 dirhams a gram for 24 karat, 493.59 for 22, 471.15 for 21 and 403.84 for 18, all four above Thursday's close. No second dated Gulf source was found for those figures, so they are single-source and are not promoted past that. One thing can be said about them without a second source: the four numbers are one rate and three multiplications. Divide each by the 24-karat figure and the results are 0.9167, 0.8750 and 0.7500 to four decimals, the exact fineness ratios, so this is a single struck rate stepped down by purity rather than four independently quoted markets. At the dirham's pegged 3.6725 to the dollar the 24-karat rate converts to $146.62 a gram, against $147.97 a gram derived from this paper's own mark of record, a difference of $1.35 explained by the hours between them.",
"The desk's view: the number worth carrying out of Friday is not the one that broke a round figure. A wire writing up $4,550 at three in the morning New York time was reporting a level the market left behind before lunch, and the trade that prices its stock off a headline rather than off a timestamp will be repricing twice. What the session actually says is narrower and more useful. The metal is being bought against a fiscal story rather than a jewellery one, the Chinese counter is now passing that through at 6.23% in thirteen days instead of absorbing it, and a Dubai window is publishing one rate stepped down by fineness rather than four prices. A bench costing work this week should take the gram figure, note the hour it was struck, and assume the counter it competes with has already moved."
],
[
 KIT,
 {"title":"Spot gold breaks $4,550/oz (21 August 2026, 14:51 Beijing) - Eastmoney","url":"https://finance.eastmoney.com/a/202608213849220877.html"},
 {"title":"Gold - price, chart, historical data (read 22 August 2026) - TradingEconomics","url":"https://tradingeconomics.com/commodity/gold"},
 {"title":"Platinum - price, chart, historical data (read 22 August 2026) - TradingEconomics","url":"https://tradingeconomics.com/commodity/platinum"},
 {"title":"Palladium - price, chart, historical data (read 22 August 2026) - TradingEconomics","url":"https://tradingeconomics.com/commodity/palladium"},
 {"title":"UAE gold prices, Friday 21 August 2026 (Arabic) - Ghorba News","url":"https://ghorbanews.com/%D8%A3%D8%B3%D8%B9%D8%A7%D8%B1-%D8%A7%D9%84%D8%B0%D9%87%D8%A8-%D8%A7%D9%84%D8%A5%D9%85%D8%A7%D8%B1%D8%A7%D8%AA%D9%8A%D8%A9-3"},
 {"title":"938 at the exchange, 1,286 at the counter - Carat Capital (9 August 2026)","url":"https://caratcapital.org/a-nine-thirty-eight-and-twelve-eighty-six.html"},
])

# ========== 2. four-point-one-six-billion-in-july ==========
art("four-point-one-six-billion-in-july","gold-metals",False,"Gold & Metals Desk · Demand",5,"The Gold & Metals Desk",
["NUM","ACTOR"],
"India's July gold imports more than double to $4.16 billion",
"The World Gold Council puts July imports at $4.16 billion against $1.97 billion in June, with volumes at 40 to 45 tonnes against 20. The ETF leg went the other way, down 55% on the month.",
[
"India bought the correction. The World Gold Council's India market update, published 19 August 2026, puts July gold imports at $4.16 billion against $1.97 billion in June, a rise of 111% on this desk's arithmetic and more than a doubling on the council's own description. In tonnage the report estimates July volumes at 40 to 45 tonnes, up from 20 tonnes in June. The mechanism it describes is the ordinary one: June's price correction brought consumers back to the jewellery counter, and retailers restocked behind them ahead of the festival season that runs from September into October. MCX futures turned over an average 14.9 tonnes a day across the month, which is the hedging and speculative leg of the same rebound.",
"The window that produced those imports has already closed at a higher price. The council marks the international benchmark up 9% in the first two weeks of August to $4,391 an ounce, with Indian domestic prices up nearly 7% to 151,744 rupees per 10 grams over the same stretch. This paper's own mark of record for gold, Friday's last New York print, is $4,602.40, which is a further $211.40 or 4.81% above the level the council was writing about, this desk's arithmetic on the two figures. An importer who restocked in July at June's prices is holding metal that has appreciated. An importer who waited is buying a festival season at close to $4,600.",
"The investment leg contradicts the demand leg and the report says so. Net inflows into Indian gold ETFs totalled 15.6 billion rupees, about $163 million, in July, which the council states plainly was 55% lower month on month, citing Association of Mutual Funds of India data. Holdings rose by one tonne to 120 tonnes and the accounts kept opening, 57,000 new folios taking the total to 12.53 million. The first two weeks of August added a further 11.79 billion rupees, about $124 million. So the household buying metal to wear came back hard while the household buying metal as a financial position slowed by more than half, in the same month, in the same country.",
"That split is the part worth carrying. Import value and import tonnage are jewellery-and-restock signals; ETF flow is a price expectation. When they diverge this far in one month the honest reading is that Indian buyers treated June's dip as a chance to own the thing rather than a chance to own the trade. The folio count supports it: accounts are still being opened, so this is not investors leaving, it is investors adding less per head into a rising price. Anyone modelling Indian demand into the fourth quarter should note that the restock has already happened, at prices roughly 5% below where the metal now sits.",
"The desk's view: the $4.16 billion is a real number and it is a backward-looking one. It prices a window that existed in July and does not exist now, and the trade reading it as evidence that Indian demand is elastic should finish the sentence — elastic to a lower price, in a month when the lower price was available. What the same report shows about August is thinner and more cautionary: the benchmark up 9% in a fortnight, the domestic price up almost 7%, and the investment flow already halving before either of those had finished. The festival season will be bought at a level no part of this dataset covers. A jeweller planning October inventory off a July import figure is planning against the wrong price."
],
[
 {"title":"India gold market update: recovery taking shape (19 August 2026) - World Gold Council","url":"https://www.gold.org/goldhub/gold-focus/2026/08/india-gold-market-update-recovery-taking-shape"},
 KIT,
 {"title":"India buys fifteen percent less gold - Carat Capital (31 July 2026)","url":"https://caratcapital.org/a-india-buys-fifteen-percent-less.html"},
])

# ========== 3. one-in-two-out-at-the-lbma ==========
art("one-in-two-out-at-the-lbma","gold-metals",False,"Gold & Metals Desk · Refining",4,"The Gold & Metals Desk",
["NUM","VS"],
"One Chinese refiner in, two out: the LBMA's seventeen days",
"Shenzhen Zhonghenglong joined the gold Good Delivery List on 17 August. Shandong Gold Smelting came off both lists on 5 August, and Hunan Shuikoushan off the silver list on 21 August. All three are Chinese.",
[
"Three changes to the London Bullion Market Association's Good Delivery Lists inside seventeen days all concern Chinese refiners, and they run in both directions. Shandong Gold Smelting was suspended from the gold and silver lists with effect from 5 August 2026, after the association invoked its incident review process. Shenzhen Zhonghenglong Industrial was added to the gold list with effect from 17 August. Hunan Shuikoushan Nonferrous Metals Group, known as SKS, was suspended from the silver list with effect from 21 August, announced the day before. The association's current lists, read on 22 August, show 67 accredited gold refiners and 86 silver refiners.",
"The two suspensions have nothing in common except the country. Shandong Gold Smelting was suspended as an interim measure after its addition to the United States Uyghur Forced Labor Prevention Act entity list, with the association's investigation still to conclude. SKS was suspended following a modified assurance opinion issued by SLR Consulting for its 2025 Responsible Silver compliance reporting. One is a refiner caught by another jurisdiction's sanctions machinery. The other is a refiner whose own auditor declined to sign a clean opinion on its responsible-sourcing report. A buyer treating the two as the same event would be misreading both.",
"Good Delivery status is the gate to London settlement, which is what makes an administrative notice a commercial fact. Bars from an accredited refiner are deliverable against the contracts that clear the world's largest over-the-counter bullion market; bars from a suspended one are not, for as long as the suspension holds. Zhonghenglong reached that gate on the usual tests, covering ownership, history, production capability and financial standing, plus independent assay of its bars and of its own assaying capability. The company was founded in March 1997, refines gold, silver, platinum and palladium from recovery and purification streams, and in 2007 became the first private enterprise approved as a Good Delivery gold refiner by the Shanghai Gold Exchange.",
"The net position for Chinese refining is worse than the arithmetic of one in and two out suggests, because the two that left were already inside and the one that arrived starts at the bottom of a customer list. It is also the second time this month that a Chinese refiner's London standing has turned on a document rather than on metal. Neither suspension alleges a bar that failed assay. One turns on a foreign entity listing and one on an audit opinion, which is where accreditation risk now sits for anyone sourcing refined metal out of China.",
"The desk's view: this trade tends to read refinery accreditation as plumbing, and it is not plumbing this month. A jeweller or a bank buying kilobars cares about one thing at settlement, which is whether the bar is deliverable, and three notices in seventeen days have changed that answer for two Chinese suppliers and created it for a third. The transferable lesson is in the failure modes rather than the names. Sanctions exposure and a qualified audit opinion are both now sufficient to remove a refiner from the London gate, and neither is visible in the metal. Anyone whose supply chain runs through a single accredited Chinese refiner should know today what the second door is, because the notice arrives with a next-day effective date and no consultation."
],
[
 {"title":"Hunan Shuikoushan Nonferrous Metals Group Co Ltd (SKS) Suspended from the GDL List - LBMA","url":"https://www.lbma.org.uk/articles/hunan-shuikoushan-nonferrous-metals-group-co-ltd-sks-suspended-from-the-gdl-list"},
 {"title":"Shandong Gold Smelting Co. Ltd. - Incident Review Process Invoked - LBMA","url":"https://www.lbma.org.uk/articles/shandong-gold-smelting-co-ltd-incident-review-process-invoked"},
 {"title":"Good Delivery Current List - Gold (read 22 August 2026) - LBMA","url":"https://www.lbma.org.uk/good-delivery/gold-current-list"},
 {"title":"Good Delivery Current List - Silver (read 22 August 2026) - LBMA","url":"https://www.lbma.org.uk/good-delivery/silver-current-list"},
 {"title":"LBMA adds China's Shenzhen Zhonghenglong to Gold Good Delivery List - GJEPC Solitaire","url":"https://gjepc.org/solitaire/lbma-adds-chinas-shenzhen-zhonghenglong-to-gold-good-delivery-list/"},
])

# ========== 4. dvash-takes-the-odc-chair ==========
art("dvash-takes-the-odc-chair","diamonds",False,"Diamonds Desk · Governance",4,"The Diamonds Desk",
["ACTOR","NUM"],
"Yoram Dvash takes the chair at the company that sells 30% of Debswana",
"Botswana's state rough trader has named the former World Federation of Diamond Bourses president as board chairman, two months after his term there ended. The seat he replaced had been empty since November.",
[
"Okavango Diamond Company has appointed Yoram Dvash chairman of its board, reported 20 August 2026. He succeeds Gape Kaboyakgosi, who left in November after five years, meaning Botswana's state-owned rough trading arm has run without a permanent board chairman for most of a year. Dvash stepped down as president of the World Federation of Diamond Bourses two months ago, having held the office since 2020, and he remains chairman of both the Israel Diamond Institute and the Israel Diamond Exchange. He said he looks forward to \"working with the board, management and the government of Botswana.\"",
"The seat carries more rough than the announcement suggests. Under the sales agreement signed with De Beers in February 2025, Okavango receives 30% of Debswana's production for the first five years of the ten-year term, rising to 40% for the second five, with a possible further extension moving the split to 50-50. Debswana is the joint venture between De Beers and the government of Botswana that mines the country's diamonds, and Botswana is the largest producer of rough by value in the world. The chairman of Okavango's board therefore sits above the disposal of nearly a third of that output, sold outside the De Beers channel.",
"This paper has covered Dvash twice before in different chairs. On 15 July it reported his succession at the World Federation of Diamond Bourses by Mehul Shah, after Dvash completed the maximum two consecutive three-year terms. On 1 August it reported that Okavango had signed a tender arrangement with the Dubai Diamond Exchange, part of that centre's year of buying the pieces it lacked. The appointment joins those two threads: the man who ran the bourse federation now chairs the state seller that has just opened a Dubai tender window.",
"What the appointment does not come with is a number, and that is worth saying plainly. Okavango published no revenue figure, no tender calendar and no strategic target alongside the announcement, and the company does not report publicly on the cadence a listed miner would. The verifiable content of the news is the name, the date, the vacancy it fills and the tonnage the seat governs. Everything else being written about it this weekend is inference.",
"The desk's view: the interesting part is who Botswana hired rather than what he was hired to do. Okavango's problem is not that it lacks rough, it is that it has a rising share of a shrinking market and has to sell into it without De Beers' book. Appointing a chairman whose career is bourse politics, in Ramat Gan and then at the federation, is a decision to solve that through the trading centres rather than through the mining side. Watch where the tenders go next. A Dubai arrangement already exists, Israel is the chairman's own ground, and the 40% step in this contract arrives well before anyone expects the natural rough market to have recovered."
],
[
 {"title":"Yoram Dvash to head up Okavango Diamond Company board (20 August 2026) - Rapaport","url":"https://rapaport.com/news/yoram-dvash-to-head-up-okavango-diamond-company-board/"},
 {"title":"De Beers, Botswana Make New Diamond Sales Deal Official (26 February 2025) - National Jeweler","url":"https://nationaljeweler.com/articles/13684-de-beers-botswana-make-new-diamond-sales-deal-official"},
 {"title":"Mehul Shah takes the gavel - Carat Capital (15 July 2026)","url":"https://caratcapital.org/a-mehul-shah-takes-the-gavel.html"},
 {"title":"Dubai Diamond Week returns - Carat Capital (1 August 2026)","url":"https://caratcapital.org/a-dubai-diamond-week-returns.html"},
])

# ========== 5. vasant-mehta-dies-at-81 ==========
art("vasant-mehta-dies-at-81","diamonds",False,"Diamonds Desk · Obituary",4,"The Diamonds Desk",
["ACTOR","STAKES"],
"Vasant Mehta, who chaired GJEPC through the crash years, dies at 81",
"He was the council's vice chairman in 1991-92 and again in 2006-08, chairman from 2008 to 2010, and convenor of its banking, insurance and taxation committee for years after that.",
[
"Vasant Mehta, a former chairman of India's Gem and Jewellery Export Promotion Council, has died at 81, reported 18 August 2026. He ran M/s V. Rameshchandra & Co in Mumbai and spent four decades inside the institutions of the Indian diamond trade rather than only in his own business. He was the council's vice chairman in 1991-92, vice chairman again in 2006-08, and chairman from 2008 to 2010. Gaetano Cavalieri, president of the World Jewellery Confederation, described him as \"first and foremost a servant of the industry.\"",
"The chairmanship dates matter more than an obituary usually allows. Mehta held the council's top seat from 2008 to 2010, which is precisely the window in which the global financial crisis emptied the order books of the world's cutting floor and the credit lines behind them. India polishes the large majority of the world's diamonds by piece, and it does so on bank finance. Running the export council through those two years was a job about liquidity rather than about promotion.",
"That is the thread through the rest of his service. He convened the council's banking, insurance and taxation committee for years, and advised the legal committee of the Bharat Diamond Bourse. Those are the unglamorous seats where the Indian trade's actual constraint sits, and he kept them long after the ceremonial one ended. Internationally he represented Indian interests at the World Diamond Council, the World Federation of Diamond Bourses, the International Diamond Manufacturers Association, the World Jewellery Confederation and the Kimberley Process, and he served the Mumbai Diamond Merchants Association.",
"This paper carries no independent verification of the date or circumstances of the death beyond the trade report, and does not have a statement from the family or the council. What is on the record is the report, dated 18 August, the age, the firm and the roles with their years, all of which are consistent across the council's own published history of its office holders.",
"The desk's view: the obituaries of this trade tend to count carats, and this one should count committees. A man who was vice chairman twice, fifteen years apart, and who then spent his post-chairmanship years on banking and taxation rather than on the podium, was doing the part of the work that decides whether Surat's floors have credit in a bad year. That is the work the Indian industry has always been short of and it is the seat nobody campaigns for. The people now running GJEPC through a genuine downturn in natural stones inherited a machinery he helped build for the last one."
],
[
 {"title":"Former GJEPC chairman Vasant Mehta dies at 81 (18 August 2026) - Rapaport","url":"https://rapaport.com/news/former-gjepc-chairman-vasant-mehta-dies-at-81/"},
])

# ========== 6. fifty-three-percent-at-the-top ==========
art("fifty-three-percent-at-the-top","retail-tech",False,"Retail & Technology Desk · Consumer",4,"The Retail & Technology Desk",
["NUM","ACTOR"],
"Miniso grows 53% and takes the top of NRF's Hot 25",
"Kantar ranks the fastest-growing US retailers on domestic sales growth from 2024 to 2025. Dick's Sporting Goods is second at 49% after buying Foot Locker, and every name in the top five is a value format.",
[
"The National Retail Federation's Hot 25 list for 2026, compiled by Kantar and published 21 August, ranks Miniso first on 53% growth in US sales. Dick's Sporting Goods is second at 49%, lifted by its acquisition of Foot Locker. Daiso Sangyo is third at 26%, Primark fourth at 24% and Five Below fifth at 23%. The metric is the increase in domestic sales between 2024 and 2025, which makes this a ranking of momentum rather than of size. Rachel Dalton, Kantar's head of retail insights for the Americas, said \"value is a huge story in this year's list.\"",
"None of these are jewellers and that is the reason to read it. Miniso sells blind-box toys, plush, stationery and skincare at entry prices, built on licensed collaborations and fast inventory turnover. Daiso and Five Below are discount formats. Primark is fast fashion that does not sell online at scale. What the top of the list has in common is a low ticket, a high visit frequency and a store designed to be walked rather than searched, and Kantar's own reading is that value-seeking now reaches into higher-income households too.",
"The read-through for a jewellery counter is about the customer's calibration rather than about competition. Nobody chooses between a Miniso haul and a diamond stud. But the retailers growing fastest are the ones teaching a shopper what a good value looks like and what a discovery-led store feels like, and that shopper walks into a fine jewellery showroom with those two expectations already set. This paper reported on 21 August that Zales, a Signet banner, puts 67% of purchases among its core shoppers as self-purchases, which is the same customer at a different price point: buying frequently, for herself, without an occasion.",
"The honest limits of the list should be stated. It measures growth off a base, so a chain expanding from a small US footprint outranks a larger one growing steadily, and Dick's second place is an acquisition rather than organic demand. It is a US ranking. And it covers 2024 to 2025, so it describes the year before the current gold price, not this one. It is a directional read on where traffic concentrated, not a forecast.",
"The desk's view: an independent jeweller has nothing to learn from Miniso's assortment and something to learn from its cadence. The formats winning American footfall right now give a customer a reason to come in without a purchase in mind and a price at which trying something costs nothing, and most fine jewellery stores are built to do the opposite. That is defensible when the customer arrives already committed, which is what the gift calendar used to guarantee. It is a problem when two thirds of the counter is self-purchase, because a self-purchase is a visit that has to be earned before it can be sold to. The lesson is the entry price and the permission to browse, not the merchandise."
],
[
 {"title":"These are 2026's hottest retailers, says NRF (21 August 2026) - National Jeweler","url":"https://www.nationaljeweler.com/articles/15249-these-are-2026-s-hottest-retailers-says-nrf"},
 {"title":"Zales says 67% of its core shoppers now buy for themselves - Carat Capital (21 August 2026)","url":"https://caratcapital.org/a-sixty-seven-percent-buy-it-for-themselves.html"},
])

articles = NEW + articles
(C/"articles.json").write_text(json.dumps(articles, indent=1, ensure_ascii=False))
leads = [a["slug"] for a in articles if a.get("lead")]
print("articles.json: %d new, %d total, lead=%s" % (len(NEW), len(articles), leads))
assert len(leads) == 1, leads
