#!/usr/bin/env python3
# Edition No. 036 - 2026-08-17. Prepends 6 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-17"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - no-total-for-the-gem-drop ==========
art("no-total-for-the-gem-drop","auctions",True,"Lead Story · Auctions Desk",5,"The Auctions Desk",
["REVERSAL","ACTOR"],
"Two Sotheby's jewel sales closed. Neither has published a number",
"The Gem Drop August closed in New York on 13 August and the Arcade Sale in Hong Kong on 6 August. Sotheby's own results index carries no total for either, and the July edition still carries none after 32 days.",
[
"The Gem Drop August closed online in New York on 13 August after four days of bidding. Four days later Sotheby's own results index lists the sale as past and shows no total, no sell-through rate and no top lot against it. The Arcade Sale in Hong Kong, which ran from 31 July to 6 August, is listed the same way and has been for eleven days. Neither absence is particular to this month. This desk checked the previous edition of the same series, the Gem Drop July, which closed on 16 July and which this paper covered on 17 July: thirty-two days on, its page carries no result either. Three closed jewellery sales, no published number on any of them.",
"The series page is the clearest evidence of the pattern. Sotheby's maintains a landing page for the Gem Drop, describing it as a monthly release of jewels through its Sealed platform, and that page carries a heading for past auctions with nothing underneath it. The lot pages survive, so a reader can still see what was offered and what it was estimated at. What does not survive is what anything sold for, or whether it sold at all. For a format the house has now run at least seven times on a stated monthly cadence, the accumulated public record of how it has performed is a set of empty listings and an empty heading. One limit belongs on that finding and is stated rather than buried: Sotheby's builds parts of these pages with scripts this desk's fetch does not execute, so what is reported here is what the public page gives a reader, not proof that no figure exists anywhere inside the house.",
"The contrast sits inside the same building. Sotheby's New York High Jewelry sale on 13 June made $31.4 million with 95% of lots sold, led by a $3.2 million Graff ring set with a 35-carat D-colour diamond, and this paper printed those figures on 24 July. The house reported a $4.4 billion first half for 2026 with private sales at a record $826 million. An auction house that publishes a total for a trophy night, and a half-year figure for its owners, is not a house that cannot count an eleven-lot online sale. Where the number serves the brand it is published within days. Where it would answer a question about a new format, it has not been published at all, across three sales and five weeks.",
"What is lost is a figure the trade has no other route to. The Gem Drop's distinguishing feature is that it charges no buyer's premium, which this desk described on 17 July as the auction house competing with the jewellery store on the store's own terms. Whether that competition is working is an empirical question with a real answer inside it: hammer against estimate, sell-through, whether the same bidders return each month. Seven editions of that data exist somewhere in Sotheby's and none of it is public. A dealer weighing a consignment into a no-premium online format, and a retailer wondering whether the format is quietly taking a customer, are both reasoning from the house's own description of itself.",
"The desk's view: an auction is a price discovery mechanism, and a price discovery mechanism that does not publish its prices is a shop. That is not a complaint about secrecy; auction houses withhold plenty and are entitled to. It is a note about what this particular format is being sold as. The premium-free monthly drop is pitched to buyers as the transparent, retail-legible end of the auction business, and it has so far been the least legible thing either house runs, because a retailer at least prints the price on the tag. This paper's recommendation on 14 August was to retire the Gem Drop result as a story after four days of waiting for it. That was the wrong call and this is the correction to it: the waiting was never the story. The silence is, and it now has three sales and five weeks behind it."
],
[
 {"title":"Past auction results index, read 17 August 2026 — Sotheby's","url":"https://www.sothebys.com/en/results"},
 {"title":"The Gem Drop July, sale page read 17 August 2026 — Sotheby's","url":"https://www.sothebys.com/en/buy/auction/2026/the-gem-drop-july"},
 {"title":"Sotheby's Sealed: The Gem Drop, series page read 17 August 2026 — Sotheby's","url":"https://www.sothebys.com/en/series/sothebys-sealed-the-gem-drop"},
 {"title":"Eleven lots, zero premium: Sotheby's quiet monthly experiment — Carat Capital (17 July 2026)","url":"https://caratcapital.org/a-eleven-lots-no-premium.html"},
 {"title":"Trophies carry Sotheby's to $31.4 million; a pink walks — Carat Capital (24 July 2026)","url":"https://caratcapital.org/a-sothebys-thirty-one-million.html"},
])

# ========== 2. four-metals-four-write-backs ==========
art("four-metals-four-write-backs","gold-metals",False,"Gold & Metals Desk · The Tape",5,"The Gold & Metals Desk",
["NUM","STAKES"],
"Four metals up, and a palladium mark three sessions old retired",
"Kitco's board read gold $4,394.60, silver $65.38, platinum $1,749.00 and palladium $1,311.00 at 05:59 New York time. All four are written back. The palladium mark being replaced was set on 14 August and sat below every live reading taken today.",
[
"Kitco's live board at 05:59 New York time read gold at $4,394.60 an ounce, silver at $65.38, platinum at $1,749.00 and palladium at $1,311.00. All four are written back over the 04:59 marks and are now this paper's marks of record, with the source named and the timestamp new. Two comparisons are printed here rather than one, because no edition published on 15 or 16 August and the two bases answer different questions. Against Kitco's own previous close the moves are a single session: gold up $19.00, silver up $0.80, platinum up $4.00, palladium up $13.00. Against this paper's last printed marks of 14 August the moves are three days deep: gold up $38.40 or 0.88%, silver up $0.61 or 0.94%, platinum up $24.00 or 1.39%, palladium up $14.00 or 1.08%. All four metals are higher on both bases.",
"The mark being retired is palladium's $1,297.00, set on 14 August and carried unchanged since. The tape desk declined to write it back at 04:59 this morning, having found Kitco at $1,311.00 against FXEmpire at $1,320.55, a gap of $9.55 or 0.73%, and held the older figure under the two-page rule. At 05:59 this desk read two further pages: TradingEconomics at $1,331.00 and JM Bullion at $1,351.00. Four live readings, spanning $40.00 or 3.05% from low to high, and every one of them above the held mark. Palladium is a thin metal quoted on wide spreads and the disagreement between those four pages is real and is disclosed here rather than reconciled. What the disagreement does not support is $1,297.00, which is not one of the four numbers and is below all of them.",
"That is the argument that ended the platinum hold on 14 August, applied to the other white metal. Platinum today shows the same basis this paper has now recorded for a fourth consecutive session: Kitco at $1,749.00 against TradingEconomics at $1,760.40, $11.40 or 0.65% low, the same sign and roughly the same size as the gaps of 12, 13 and 14 August. A difference that recurs in one direction across four sessions describes how two pages are quoting, not a market nobody can read, and this paper prints Kitco because Kitco is the board carrying the other three marks. Gold and silver each cleared their second page cleanly, at $4,394.79 and $65.484 on TradingEconomics, 0.004% and 0.16% from the marks printed here.",
"At 31.1035 grams to the troy ounce the four marks work out at $141.29 a gram of fine gold, $2.10 a gram of fine silver, $56.23 a gram of fine platinum and $42.15 a gram of fine palladium, all this desk's arithmetic. The gold-to-silver ratio, this desk's division of its own gold mark by its own silver mark on the same board at the same minute, reads 67.22 against 67.26 on 14 August: four hundredths of a point across three days in which both metals rose about nine-tenths of a per cent. Silver has not outrun gold and gold has not outrun silver. For a workshop repricing stock this morning, the practical figure is palladium, where the shelf price moves 1.08% in one step because the previous step never happened.",
"The desk's view: the three-day gap in this tape is the paper's, not the market's, and the distinction matters more than it sounds. Nothing stopped trading between Friday and this morning; only the printing stopped, and a reader who takes the change column at face value would think gold moved $19.00 since this paper last spoke to them when it moved $38.40. That is why both bases are on the page. The second lesson is the one palladium keeps teaching: a rule written to stop a paper printing a number it cannot defend will, if followed mechanically, end up defending a number nobody is quoting. Two sessions of holding is caution. Three sessions of holding, while four separate pages print higher figures, is just an old number with a procedure wrapped around it."
],
[
 {"title":"Gold, Silver, Platinum & Palladium spot prices — Kitco (17 August 2026, 05:59 EST live board)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Commodity prices, precious metals table — TradingEconomics (read 17 August 2026)","url":"https://tradingeconomics.com/commodities"},
 {"title":"Palladium prices today per ounce — JM Bullion (17 August 2026, 06:01 EDT)","url":"https://www.jmbullion.com/charts/palladium-price/"},
 {"title":"The platinum hold ends at $1,725 after three mornings — Carat Capital (14 August 2026)","url":"https://caratcapital.org/a-the-platinum-hold-ends.html"},
])

# ========== 3. thirty-nine-point-six ==========
art("thirty-nine-point-six","gold-metals",False,"Gold & Metals Desk · China",5,"The Gold & Metals Desk",
["NUM","VS"],
"China's counter held its 39.6% margin through a 1.4% move",
"Shanghai gold reads 954.01 yuan a gram today and Chow Tai Fook's counter 1,332. Three days ago this paper printed 940.72 and 1,312. Both legs rose about 1.5% and the markup moved fifteen hundredths of a point.",
[
"The Shanghai Gold Exchange's Au99.99 contract opened at 946.00 yuan a gram today and last traded at 954.01, a rise of 1.41% on the session, on the market report carried by the Chinese finance aggregator cngold. Chow Tai Fook's 24-carat counter reads 1,332 yuan a gram, a figure carried identically today by two independent Chinese price aggregators, jinjia.com.cn and cngold, which is the strongest agreement available on a counter price. Dividing one by the other, this desk's arithmetic, puts the shop window 39.62% above the exchange, a gap of 377.99 yuan on every gram sold.",
"Three days ago this paper printed the same pair at 940.72 and 1,312, a markup of 39.47% and a gap of 371.28 yuan. Since then the exchange has risen 13.29 yuan, or 1.41%, and the counter has risen 20 yuan, or 1.52%. The markup went from 39.47% to 39.62%. The margin held to within fifteen hundredths of a point. That is the test this desk set for itself on 14 August, when it argued that the Chinese counter price is a merchant setting a margin rather than a market clearing, and the three sessions since have returned the answer the argument predicted: the shop moved the same percentage the metal did, not the same number of yuan.",
"Two divergences between outside sources belong on the page. On the exchange leg, the Bureau's gold desk read today's Shanghai sessions at 951.80 and 952.98 yuan against the 954.01 used here, and on 952.98 the markup would read 39.77% and the gap 379.02 yuan; this desk cannot establish which minute of the board each page is reading and does not resolve it, so the figures on both bases are printed. On the counter leg, the aggregator series runs 1,312 on 14 August, 1,325 on 15 August, no reading published for 16 August and 1,332 today, so the 20-yuan rise is three calendar days containing two counter revisions rather than a single jump. The counter still moves in whole yuan and the exchange in hundredths, which is the shape this paper has recorded all month.",
"One cross-check and one limit. Gold at $4,394.60 an ounce, this paper's own mark of record this morning, is $141.29 a gram, and 954.01 yuan against $141.29 implies 6.752 yuan to the dollar, which is this desk's arithmetic and is not an official rate; it is printed as a sanity test on the Shanghai figure rather than as a currency quotation, and it lands where a plausible rate would. The limit is the one this desk prints every time: a listed counter price is an asking price, not a transacted one, and workmanship charges, store discounts and buy-back terms sit outside both numbers. What a Chinese buyer actually pays is above 1,332 and what she can sell back at is well below 954.01.",
"The desk's view: the counter is priced as a percentage, not as a price, and three sessions of live data now say so rather than one desk's inference. That is a more useful fact than either number on its own. It means a Chinese retail gold price can be forecast from the exchange with a multiplier, that a fall in Shanghai will show up in the shop window within a day or two at roughly forty per cent on top, and that the widening this paper reported between 9 and 14 August, from 37.10% to 39.47%, was a repricing of the margin itself rather than a lag in the shop catching up. The number to watch is still the 39.6%, not the 1,332. A margin that survives a 1.4% move in the underlying is a decision somebody is defending."
],
[
 {"title":"2026年8月17日上海黄金交易所市场行情 — Shanghai Gold Exchange market report, 17 August 2026 — 金投网","url":"https://m.cngold.org/home/xw10694457.html"},
 {"title":"周大福今日金价 — Chow Tai Fook daily counter price series, read 17 August 2026 — 金价网","url":"https://www.jinjia.com.cn/chowtaifook/"},
 {"title":"周大福黄金价格查询 — Chow Tai Fook quotation page, read 17 August 2026 — 金投网","url":"https://m.cngold.org/quote/gjs/swhj_zdf.html"},
 {"title":"China's jewellery counter charges 39.5% over the exchange price — Carat Capital (14 August 2026)","url":"https://caratcapital.org/a-nine-forty-and-thirteen-twelve.html"},
])

# ========== 4. eight-oh-six-out-six-sixty-five-in ==========
art("eight-oh-six-out-six-sixty-five-in","retail-tech",False,"Retail & Technology Desk · Ownership",5,"The Retail & Technology Desk",
["NUM","VS"],
"One fund cut 806,676 Signet shares. An index fund bought 665,182",
"Four institutions filed amended 13G statements on Signet Jewelers for the June quarter. Between them they hold 10,767,453 shares, 27.38% of the company. The two that moved went in opposite directions by almost the same amount.",
[
"Four institutions filed amended Schedule 13G statements with the Securities and Exchange Commission on Signet Jewelers between 8 July and 14 August, each reporting a position as at 30 June. Vanguard Portfolio Management reported 3,577,704 shares, or 9.09%. Dimensional Fund Advisors reported 2,584,443, or 6.6%. Select Equity Group reported 2,436,873, or 6.2%. FMR, the parent of Fidelity, reported 2,168,433, or 5.5%. Together they hold 10,767,453 shares against the 39,329,783 shares Signet disclosed as outstanding on 29 May in its own quarterly report, which is 27.38% of the largest specialty jewellery retailer in the United States held by four filers, this desk's arithmetic on the filings.",
"Two of those positions moved enough to be worth reading. Select Equity Group filed its first 13G on Signet on 3 April at 3,243,549 shares, or 8.1%, as at 1 April. By 30 June it held 2,436,873, or 6.2%: a cut of 806,676 shares, 24.87% of the stake and 1.9 points of the company. Vanguard Portfolio Management filed at 2,912,522, or 7.26%, as at 31 March, and reported 3,577,704, or 9.09%, at 30 June: an addition of 665,182 shares, 22.84% of its own holding. Active money sold a quarter of its stake; index money bought. The net of the two is 141,494 shares leaving the pair, which is a rotation between kinds of shareholder rather than an exit from the company.",
"The longer arc is FMR's. Fidelity's parent reported 4,792,767 shares, or 11.6%, as at 29 August 2025. Its 30 June filing puts it at 2,168,433, or 5.5%, a reduction of 54.76% over ten months on a holder that is one more amendment from dropping below the 5% disclosure threshold and out of this record entirely. BlackRock last filed at 5,893,515 shares, or 14.4%, as at 30 September 2025 and has not filed on Signet since. One filing needs care rather than a headline: The Vanguard Group lodged a fifteenth amendment on 27 March reporting zero shares, and two Vanguard entities filed fresh 13Gs at the end of April. This desk reads that as the same money re-registering under new filing entities rather than a sale, and states it as a reading rather than a fact.",
"Three limits belong on all of it. A Schedule 13G is a passive declaration, filed by holders who state they are not seeking to influence control, so none of this is an activist arriving. Every figure above describes 30 June and was disclosed weeks later, so the register may already have moved. And the 27.38% total is four filers measured against a share count from 29 May, which is the most recent Signet has published; it is not a complete register, because holders below 5% never appear and BlackRock's last disclosed 14.4% is eleven months old and unrefreshed. What the filings do establish is the direction of the two holders who did report a change, and the size of the float they are moving inside.",
"The desk's view: a 13G is a photograph of a quarter that ended seven weeks ago, and photographs are still worth looking at when the company in them reports in three weeks. Signet's share count has come down far enough that a single active manager selling 806,676 shares moves almost two points of the company, and the buyer on the other side was an index fund that will hold the stock regardless of what the second quarter says. That is what a shrinking float does: it makes the register twitchier and the remaining active opinion louder. The trade tends to read Signet through same-store sales and the bridal cycle. The ownership page is the other half of the story, it is free, it is filed at a public address, and almost nobody in this industry reads it."
],
[
 {"title":"Schedule 13G/A, Select Equity Group L.P. on Signet Jewelers, filed 14 August 2026 — SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/832988/000110465926097176/primary_doc.xml"},
 {"title":"Schedule 13G/A, Vanguard Portfolio Management on Signet Jewelers, filed 31 July 2026 — SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/832988/000210012126000997/primary_doc.xml"},
 {"title":"Schedule 13G/A, Dimensional Fund Advisors on Signet Jewelers, filed 14 July 2026 — SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/832988/000035420426000774/primary_doc.xml"},
 {"title":"Schedule 13G/A, FMR LLC on Signet Jewelers, filed 8 July 2026 — SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/832988/000031506626001464/primary_doc.xml"},
 {"title":"Signet Jewelers Ltd, complete filing history — SEC EDGAR","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000832988&type=SC+13&dateb=&owner=include&count=40"},
])

# ========== 5. four-eighty-six-thousand-ounces ==========
art("four-eighty-six-thousand-ounces","gold-metals",False,"Gold & Metals Desk · Physical Demand",5,"The Gold & Metals Desk",
["ACTOR","NUM"],
"The Perth Mint sold 486,043 ounces of silver in July",
"Silver sales rose 65% on the month and platinum 59%. Gold rose 4% to 30,871 ounces. The mint published the figures on 10 August, and gold has risen 8.51% since the month those figures describe.",
[
"The Perth Mint sold 30,871 troy ounces of gold, 486,043 ounces of silver and 1,915 ounces of platinum in minted product during July, in figures the mint published on 10 August. Gold rose 4% on the month and 41% on the year. Silver rose 65% on the month and 8% on the year. Platinum rose 59% on the month and 46% on the year. Those figures are seven days old as they print here and describe a month that closed more than a fortnight ago, which is stated rather than smoothed over: this is new to this paper's archive, not new to the world, and it is reported because nothing else this desk found this morning shows the small physical buyer as directly.",
"Silver is the number that carries the release. Fifteen point seven ounces of silver for every ounce of gold left the mint in July, on this desk's division of the two counts. Turned into money at this morning's marks of $4,394.60 and $65.38 an ounce, that is roughly $135.7 million of gold against $31.8 million of silver, so gold outsold silver by 4.27 to one by value while silver outsold gold by 15.7 to one by weight. A 65% monthly jump in silver ounces against a 4% jump in gold ounces is a buyer trading down the periodic table, which is the behaviour a retail counter shows when the headline metal has run away from the wallet rather than when confidence has left the sector.",
"The price context is the part the release cannot state, because it was written before it happened. The mint's own note records gold trading near $4,050 an ounce at the end of July, a modest monthly gain of about 1% after touching the year's low during the month. This paper's mark of record this morning is $4,394.60, which is 8.51% above that end-July level, this desk's arithmetic. So July's demand was recorded at a price the buyer would now be delighted to pay, and every ounce of that 30,871 has appreciated since the ledger closed. It also means the July figures cannot be read forward: a 4% rise in gold ounces at $4,050 says nothing about what August looks like $344 higher.",
"The mint's exchange-traded product moved almost not at all in the same month. Holdings in PMGOLD rose 1,011 ounces, or 0.26%, to 382,735 ounces, which is 11.90 tonnes at 31.1035 grams to the ounce. A 65% surge at the coin counter beside a quarter of a per cent at the fund is two different customers in one release. Two limits: these are one mint's minted-product sales, not Australian demand and certainly not global demand, and the Perth Mint is a refiner whose retail channel skews to Australian and Asian buyers. The series is worth carrying because it is monthly, unrevised and published by the seller, which is more than most physical demand data offers.",
"The desk's view: the coin counter and the fund moved in different directions in July, and the gap between them is the most honest reading of who is still buying metal at these levels. The fund buyer adds a quarter of a per cent and waits. The counter buyer, priced out of gold, takes fifteen ounces of silver for every ounce of gold and takes 65% more of it than the month before. This paper reported on 14 August that global gold ETF flows in July were a European story with North America contributing $71 million; the Perth Mint's July says the same market from the other end, where the ticket is a coin rather than a fund unit. Both describe a buyer who wants the metal and is increasingly choosing the cheaper one."
],
[
 {"title":"Perth Mint July sales resilient, July 2026 sales update (10 August 2026) — The Perth Mint","url":"https://www.perthmint.com/news/investor/market-research-and-analysis/july-2026-sales-update/"},
 {"title":"Gold, Silver, Platinum & Palladium spot prices — Kitco (17 August 2026, 05:59 EST live board)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"$71 million from America in a $3 billion gold month — Carat Capital (14 August 2026)","url":"https://caratcapital.org/a-seventy-one-million-from-america.html"},
])

# ========== 6. seven-oh-five-across-seventeen-times ==========
art("seven-oh-five-across-seventeen-times","diamonds",False,"Diamonds Desk · Lab-Grown",5,"The Diamonds Desk",
["NUM","GAP"],
"$705 for a one-carat lab-grown, on asking prices spanning 17.6 times",
"The reference price this paper's tape carries for a one-carat lab-grown diamond is $705 today. The same page shows one-carat rounds offered between $185 and $3,247, and a second source read $550 three weeks ago.",
[
"The lab-grown reference on this paper's tape reads $705 a carat this morning, taken from CaratRadar's one-carat round average and confirmed at source, where the page is dated 17 August and states that it refreshes daily. The series this paper has printed runs $727 earlier in the month, $711 on 11 August, $707 on the 14th and $705 today: down 0.84% in six days and 3.03% from $727. That is a slow, orderly decline rather than the collapse the category is usually described with, and it is the fourth consecutive reading this paper has published in the same direction.",
"The number underneath the number is the one worth printing. The same page that averages a one-carat round at $705 shows the offers it is averaging running from $185 to $3,247 for the same nominal weight and shape, a spread of 17.6 times, this desk's division. At two carats the cushion range runs $345 to $6,984 and at three carats $449 to $12,050. An average sitting inside a seventeen-fold range is doing an enormous amount of work, and a jeweller quoting $705 to a customer is quoting the midpoint of a market in which the same specification is being offered at a quarter of it and at four and a half times it.",
"A second source disagrees, and this paper carries both. Its own natural and lab-grown price lists, compiled on 25 July from a live retail sample, put the one-carat lab-grown round at $550 a carat against a natural one-carat round at $4,581, a multiple of 8.3. CaratRadar's $705 is 28.2% above that $550, this desk's arithmetic, on a gap of three weeks and two different samples of the same market. Neither figure is wrong and the divergence is disclosed rather than resolved: one is a live retail asking average from one aggregator, the other a six-retailer median from another, and there is no clearing exchange behind either to settle the question. In a market with no scarcity and no benchmark, the price is whatever the sample says.",
"Against that, the category's own trade body spent last week arguing the problem lies elsewhere. Marty Hurwitz, executive director of the Grown Diamond Trade Organization, told JCK on 14 August that lab-grown diamonds are a help and not a hindrance to the jewelry industry, and put the real challenge at getting Gen Z into jewellery stores to buy anything at all. He also noted that consumers keep walking in to buy the category with no macro marketing behind it. Both of those can be true while the price series above keeps sliding, because they measure different things: he is describing footfall and this desk is describing what happens to a manufactured product's price once footfall arrives and supply is unconstrained.",
"The desk's view: a single average across a seventeen-fold range is not a price, it is a summary statistic wearing a price's clothes, and the trade should stop quoting one. Natural diamonds have Rapaport and RAPI, which this paper has spent a fortnight failing to read behind a paywall but which at least exist. Lab-grown has aggregator averages that disagree by 28% and ranges that disagree by 1,700%, and the gap between the cheapest and dearest one-carat is not error, it is cut quality, growth method and brand pretending to be the same product. The useful number for a retailer is not $705. It is the range, and the fact that nobody publishing an average is being paid to tell you how wide it is."
],
[
 {"title":"Lab-grown diamond prices, one-carat reference, read 17 August 2026 — CaratRadar","url":"https://caratradar.com/diamond-prices/lab-grown-diamonds/"},
 {"title":"The Natural Diamond Price List (as of 30 July 2026) — Carat Capital","url":"https://caratcapital.org/natural-diamond-prices.html"},
 {"title":"GDTO's Hurwitz: the real industry challenge is Gen Z, not defeating lab-grown — JCK (14 August 2026)","url":"https://www.jckonline.com/editorial-article/gdto-hurwitz-lab-grown/"},
 {"title":"The one-carat stops falling — Carat Capital (4 August 2026)","url":"https://caratcapital.org/a-the-one-carat-stops-falling.html"},
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

specs["no-total-for-the-gem-drop"] = {
 **strip("By the numbers · Sotheby's unreported jewel sales",[
   {"fig":"4","lab":"days since the Gem Drop August closed"},
   {"fig":"11","lab":"days since the Arcade Sale closed"},
   {"fig":"32","lab":"days since the Gem Drop July closed"},
   {"fig":"0","lab":"totals published for any of the three"},
   {"fig":"$31.4m","lab":"published within weeks for the June trophy night"}]),
 "figs":[bars("Plate I","Days closed without a published result · Sotheby's jewel sales, at 17 August",[
   {"l":"GEM DROP JULY, CLOSED 16 JUL","v":32,"d":"32 days","hi":True},
   {"l":"ARCADE SALE HK, CLOSED 6 AUG","v":11,"d":"11 days"},
   {"l":"GEM DROP AUGUST, CLOSED 13 AUG","v":4,"d":"4 days"},
   {"l":"HIGH JEWELRY NY, 13 JUN","v":0,"d":"total published"}],
   "Counted by this desk from each sale's closing date to 17 August 2026 against Sotheby's own results index, read the same day. The High Jewelry row is shown at zero because its total, $31.4m at 95% sold, was public and in the trade press well before this paper printed it on 24 July.",225)],
 "flow":flow5("Three sales, no numbers.","The same house, counting elsewhere.","What the silence costs the trade.",
   "Three closed jewellery sales, no published number on any of them","The Auctions Desk",
   "Eleven lots, zero premium: Sotheby's quiet monthly experiment","a-eleven-lots-no-premium.html"),
 "desk":{"split":"an auction is a price discovery mechanism, and a price discovery mechanism that does not publish its prices is a shop"},
 "next":nxt("four-metals-four-write-backs","Metals","All four metals higher, and the palladium mark comes off after three sessions.",
   "eleven-lots-no-premium","Auctions","sothebys-thirty-one-million","Auctions")}

specs["four-metals-four-write-backs"] = {
 **strip("By the numbers · The tape, 17 August",[
   {"fig":"$4,394.60","delta":"▲ +0.88%","dir":"up","lab":"gold, vs this paper's 14 Aug mark"},
   {"fig":"$65.38","delta":"▲ +0.94%","dir":"up","lab":"silver, same basis"},
   {"fig":"$1,749.00","delta":"▲ +1.39%","dir":"up","lab":"platinum, same basis"},
   {"fig":"$1,311.00","delta":"▲ +1.08%","dir":"up","lab":"palladium, a three-session hold ends"},
   {"fig":"67.22","delta":"▼ −0.04","dir":"down","lab":"gold-to-silver ratio, derived"}]),
 "figs":[bars("Plate I","Palladium on four pages, 17 August · dollars an ounce",[
   {"l":"JM BULLION, 06:01 EDT","v":1351.00,"d":"$1,351.00"},
   {"l":"TRADINGECONOMICS","v":1331.00,"d":"$1,331.00"},
   {"l":"FXEMPIRE, PER THE TAPE DESK","v":1320.55,"d":"$1,320.55"},
   {"l":"KITCO, 05:59 EDT","v":1311.00,"d":"$1,311.00","hi":True},
   {"l":"THE HELD MARK, 14 AUG","v":1297.00,"d":"$1,297.00"}],
   "Four live readings taken this morning span $40.00, or 3.05%, and disagree about palladium in a way this desk discloses rather than resolves. The mark being retired is not one of the four and sits below all of them. Kitco is taken because it carries the other three marks on this tape.",226)],
 "flow":flow5("Four marks, one board, two bases.","The mark that sat below everybody.","What it works out to at the bench.",
   "Four live readings, spanning $40.00 or 3.05% from low to high","The Gold & Metals Desk",
   "The platinum hold ends at $1,725 after three mornings","a-the-platinum-hold-ends.html"),
 "desk":{"split":"the three-day gap in this tape is the paper's, not the market's"},
 "next":nxt("thirty-nine-point-six","Metals","Shanghai rose 1.41% and Chow Tai Fook's counter kept its markup to within fifteen hundredths of a point.",
   "the-platinum-hold-ends","Metals","nine-forty-and-thirteen-twelve","Metals")}

specs["thirty-nine-point-six"] = {
 **strip("By the numbers · China's gold counter, 17 August",[
   {"fig":"954.01","delta":"▲ +1.41%","dir":"up","lab":"Au99.99, yuan a gram"},
   {"fig":"1,332","delta":"▲ +1.52%","dir":"up","lab":"Chow Tai Fook counter, same day"},
   {"fig":"377.99","lab":"the gap in yuan, derived here"},
   {"fig":"39.62%","lab":"the markup, derived here"},
   {"fig":"+0.15","lab":"points added to the markup since 14 August"}]),
 "figs":[bars("Plate I","Three sessions of the Chinese pair · yuan a gram",[
   {"l":"COUNTER, 17 AUGUST","v":1332,"d":"1,332","hi":True},
   {"l":"COUNTER, 14 AUGUST","v":1312,"d":"1,312"},
   {"l":"EXCHANGE, 17 AUGUST","v":954.01,"d":"954.01"},
   {"l":"EXCHANGE, 14 AUGUST","v":940.72,"d":"940.72"}],
   "The 14 August pair is as this paper published it that morning from the exchange's own quotations. Over three days the exchange rose 1.41% and the counter 1.52%, moving the markup from 39.47% to 39.62%, this desk's arithmetic. The Bureau's gold desk read the same session at 952.98, on which the markup would be 39.77%.",227)],
 "flow":flow5("Two prices for the same gram.","The margin, not the price.","One cross-check and one limit.",
   "The margin held to within fifteen hundredths of a point","The Gold & Metals Desk",
   "China's jewellery counter charges 39.5% over the exchange price","a-nine-forty-and-thirteen-twelve.html"),
 "desk":{"split":"the counter is priced as a percentage, not as a price"},
 "next":nxt("eight-oh-six-out-six-sixty-five-in","Retail","Four filers hold 27.38% of Signet, and the two that moved went opposite ways.",
   "nine-forty-and-thirteen-twelve","Metals","china-lowest-since-2004","Metals")}

specs["eight-oh-six-out-six-sixty-five-in"] = {
 **strip("By the numbers · Signet's register at 30 June",[
   {"fig":"27.38%","lab":"held by four 13G filers, derived here"},
   {"fig":"−806,676","delta":"▼ −24.87%","dir":"down","lab":"Select Equity, shares cut"},
   {"fig":"+665,182","delta":"▲ +22.84%","dir":"up","lab":"Vanguard Portfolio Management, added"},
   {"fig":"9.09%","lab":"the largest disclosed holding"},
   {"fig":"39.3m","lab":"shares outstanding, 29 May"}]),
 "figs":[bars("Plate I","Signet: disclosed 13G holdings at 30 June 2026 · shares",[
   {"l":"VANGUARD PORTFOLIO MGMT","v":3577704,"d":"3,577,704 · 9.09%","hi":True},
   {"l":"DIMENSIONAL FUND ADVISORS","v":2584443,"d":"2,584,443 · 6.6%"},
   {"l":"SELECT EQUITY GROUP","v":2436873,"d":"2,436,873 · 6.2%"},
   {"l":"FMR LLC","v":2168433,"d":"2,168,433 · 5.5%"}],
   "Read directly from each filer's Schedule 13G/A on SEC EDGAR. Percentages are the filers' own; the 27.38% total is this desk's sum against the 39,329,783 shares Signet disclosed outstanding on 29 May 2026. Holders below the 5% threshold never appear, so this is not a complete register.",228)],
 "flow":flow5("Four filers, one quarter.","The two that moved.","What a 13G does not tell you.",
   "Active money sold a quarter of its stake; index money bought","The Retail & Technology Desk",
   "Zales goes to Mattel","a-zales-goes-to-mattel.html"),
 "desk":{"split":"a 13G is a photograph of a quarter that ended seven weeks ago"},
 "next":nxt("four-eighty-six-thousand-ounces","Metals","The Perth Mint's silver sales rose 65% in a month; its gold fund rose 0.26%.",
   "zales-goes-to-mattel","Retail","the-loss-that-wasnt-revenue","Retail")}

specs["four-eighty-six-thousand-ounces"] = {
 **strip("By the numbers · Perth Mint, July 2026",[
   {"fig":"486,043","delta":"▲ +65%","dir":"up","lab":"ounces of silver, month on month"},
   {"fig":"30,871","delta":"▲ +4%","dir":"up","lab":"ounces of gold"},
   {"fig":"1,915","delta":"▲ +59%","dir":"up","lab":"ounces of platinum"},
   {"fig":"15.7","lab":"ounces of silver per ounce of gold, derived"},
   {"fig":"+0.26%","lab":"PMGOLD holdings, the same month"}]),
 "figs":[bars("Plate I","Perth Mint July sales, month-on-month change · per cent",[
   {"l":"SILVER","v":65,"d":"+65%","hi":True},
   {"l":"PLATINUM","v":59,"d":"+59%"},
   {"l":"GOLD","v":4,"d":"+4%"},
   {"l":"PMGOLD ETF HOLDINGS","v":0.26,"d":"+0.26%"}],
   "Published by the Perth Mint on 10 August 2026 and seven days old as this prints. Year-on-year the same three metals read +41%, +46% and +8% for gold, platinum and silver. PMGOLD holdings rose 1,011 ounces to 382,735, or 11.90 tonnes, this desk's conversion at 31.1035 grams to the troy ounce.",229)],
 "flow":flow5("A month at the coin counter.","Silver carries the release.","The price the ledger was written at.",
   "Fifteen point seven ounces of silver for every ounce of gold","The Gold & Metals Desk",
   "$71 million from America in a $3 billion gold month","a-seventy-one-million-from-america.html"),
 "desk":{"split":"the coin counter and the fund moved in different directions"},
 "next":nxt("seven-oh-five-across-seventeen-times","Diamonds","The lab-grown one-carat reference reads $705, inside a range that runs 17.6 times.",
   "seventy-one-million-from-america","Metals","four-metals-four-write-backs","Metals")}

specs["seven-oh-five-across-seventeen-times"] = {
 **strip("By the numbers · Lab-grown, 17 August",[
   {"fig":"$705","delta":"▼ −0.84%","dir":"down","lab":"one-carat round average, six days"},
   {"fig":"$185","lab":"cheapest one-carat offered on the same page"},
   {"fig":"$3,247","lab":"dearest one-carat on the same page"},
   {"fig":"17.6×","lab":"the spread, derived here"},
   {"fig":"$550","lab":"a second source, three weeks ago"}]),
 "figs":[bars("Plate I","One nominal carat, lab-grown · dollars per carat, asking",[
   {"l":"DEAREST OFFER ON THE PAGE","v":3247,"d":"$3,247"},
   {"l":"THE AVERAGE QUOTED","v":705,"d":"$705","hi":True},
   {"l":"CARAT CAPITAL LIST, 25 JULY","v":550,"d":"$550"},
   {"l":"CHEAPEST OFFER ON THE PAGE","v":185,"d":"$185"}],
   "All four describe a one-carat round lab-grown diamond. The top and bottom are the ends of the range the $705 average is drawn from, read 17 August 2026. The $550 is this paper's own price list of 25 July from a six-retailer sample; CaratRadar's average is 28.2% above it, this desk's arithmetic, and the divergence is disclosed rather than resolved.",230)],
 "flow":flow5("Four readings in a fortnight.","The range under the average.","What the trade body says instead.",
   "An average sitting inside a seventeen-fold range is doing an enormous amount of work","The Diamonds Desk",
   "The one-carat stops falling","a-the-one-carat-stops-falling.html"),
 "desk":{"split":"a single average across a seventeen-fold range is not a price"},
 "next":nxt("no-total-for-the-gem-drop","Auctions","Three closed Sotheby's jewel sales, and not one published result between them.",
   "the-one-carat-stops-falling","Diamonds","lab-grown-finds-its-floor","Diamonds")}

# ---------------- validation ----------------
existing = {a["slug"] for a in articles} | {a["slug"] for a in NEW}
errs = []
for a in NEW:
    s = a["slug"]
    if len(a["body"]) != 5: errs.append("%s: body has %d paragraphs, need 5" % (s, len(a["body"])))
    if not a["body"][4].startswith("The desk's view:"): errs.append("%s: para 5 does not open 'The desk's view:'" % s)
    if "!" in " ".join(a["body"]): errs.append("%s: exclamation mark in body" % s)
    em = " ".join(a["body"]).count("—")
    if em > 1: errs.append("%s: %d em-dashes in body" % (s, em))
    if len(a["dek"].split()) > 40: errs.append("%s: dek is %d words" % (s, len(a["dek"].split())))
    sp = specs.get(s)
    if not sp: errs.append("%s: no spec" % s); continue
    if sp["desk"]["split"] not in a["body"][4]: errs.append("%s: desk.split not verbatim in final paragraph" % s)
    pull = [b for b in sp["flow"] if "pull" in b][0]["pull"]["q"]
    if not any(pull in p for p in a["body"][:4]): errs.append("%s: pull quote not verbatim in paras 0-3" % s)
    wc = len(pull.split())
    if wc > 15: errs.append("%s: PULL QUOTE OVER THE CAP - %d words" % (s, wc))
    for ref in [sp["next"]["lead"]["slug"]] + [m["slug"] for m in sp["next"]["minis"]]:
        if ref not in existing: errs.append("%s: next slug '%s' does not exist" % (s, ref))
        if ref == s: errs.append("%s: next slug self-references" % s)
if sum(1 for a in NEW if a.get("lead")) != 1: errs.append("lead count is not exactly 1 among new articles")
if sum(1 for a in NEW + articles if a.get("lead")) != 1: errs.append("lead count across articles.json is not exactly 1")
if errs:
    print("VALIDATION FAILED"); [print(" -", e) for e in errs]; sys.exit(1)

print("PULL QUOTE WORD COUNTS (cap 15):")
for a in NEW:
    pull = [b for b in specs[a["slug"]]["flow"] if "pull" in b][0]["pull"]["q"]
    print("  %-38s %2d words" % (a["slug"], len(pull.split())))
print("HEADLINE WORD COUNTS:")
for a in NEW:
    print("  %-38s %2d words headline, %2d words dek" % (a["slug"], len(a["title"].split()), len(a["dek"].split())))

articles = NEW + articles
for s in specs: editorial[s] = specs[s]
(C/"articles.json").write_text(json.dumps(articles, ensure_ascii=False, indent=1))
(C/"editorial.json").write_text(json.dumps(editorial, ensure_ascii=False, indent=1))
print("OK: %d articles prepended, %d specs written, total %d" % (len(NEW), len(specs), len(articles)))
