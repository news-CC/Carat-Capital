#!/usr/bin/env python3
# Edition No. 026 - 2026-08-05. Prepends 7 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-05"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - four-metals-third-session ==========
art("four-metals-third-session","gold-metals",True,"Lead Story · Gold & Metals Desk",5,"The Gold & Metals Desk",
["NUM","VS","STAKES"],
"Four metals, third session: gold $4,157.80, silver up 3.27%",
"At 5:58am New York gold bid $4,157.80, up 1.99%, silver $61.35, up 3.27%, platinum $1,747.00, up 1.10% and palladium $1,355.00, up 1.96%. The gold to silver ratio tightened to 67.8.",
[
"Every precious metal on the Kitco board rose for a third consecutive session on Wednesday. At 5:58am New York time gold was bid at $4,157.80 an ounce, up $81.20 or 1.99%; silver at $61.35, up $1.94 or 3.27%; platinum at $1,747.00, up $19.00 or 1.10%; and palladium at $1,355.00, up $26.00 or 1.96%. Set against the print this paper carried in yesterday's tape, gold at $4,048.80 and down 0.14%, the metal has added about $109 an ounce in twenty-four hours. That is the largest single-session move in gold since this desk began carrying a daily 5:58am mark.",
"The reason is a shipping lane rather than a mine. Reuters and the currency desks report the United States, Iran and Oman closing on an interim agreement to reopen the Strait of Hormuz, with an announcement targeted for Wednesday, and oil has fallen on the expectation. Lower oil lowers the inflation path, a lower inflation path lowers the odds of another Federal Reserve increase, and traders have trimmed the probability of a September hike to about 57% from about 67% a day earlier. Gold rose because the war premium is coming out, not because it is going in. This desk filed the same inversion on 19 July, when gold lost 3.4% in a week of airstrikes.",
"Silver did the heavy lifting, as it has all week. A 3.27% session against gold's 1.99% pulls the gold to silver ratio to 67.8 from about 69.0 at yesterday's mark, a second consecutive tightening. Platinum now stands at 42.0% of the gold price. For the bench, the number that matters is not the ounce but the gram: fine gold at $4,157.80 an ounce is $133.68 a gram, against $130.17 yesterday, which is $3.51 a gram added to the metal cost of every piece in a case overnight.",
"Two cautions belong on the record. The intraday spread was wide, with this paper's own overnight print at $4,170.90 at 3:08am and an independent check at $4,174.70 at 2:44am, both above the 5:58am bid carried here, so a reader working from a headline number rather than a timestamp is working from the wrong number. And the second sources disagree: Trading Economics printed platinum at $1,760.10 and palladium at $1,372.00 against Kitco's $1,747.00 and $1,355.00, spreads of $13.10 and $17.00. Kitco is this paper's designated mark and is what the tape carries. On the diamond lines, NAT1 and LGD1 are both carried unchanged, the lab-grown reference because two trackers stood 28% apart today at $709 and $552 and neither can be printed as a market.",
"The desk's view: a metals rally built on peace talk is a rate trade wearing a geopolitics costume, and it can be unwound by the same headline that made it. If the Hormuz announcement lands on Wednesday as briefed, the news is already in the price; if it slips, the $109 comes back out faster than it went in. Friday's non-farm payrolls is the real test, the first full read on American hiring since the Fed held on 29 July with three dissents. Anyone quoting a gold-content price to a customer this week should quote the timestamp with it."
],
[
 {"title":"Gold Spot Prices, Silver, Platinum & Palladium — Kitco (5 August 2026, 5:58am EST)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Gold rallies to two-week high as USD softens on Iran deal hopes, receding Fed hike bets — FXStreet (5 August 2026)","url":"https://www.fxstreet.com/news/gold-rallies-to-two-week-high-as-usd-softens-on-iran-deal-hopes-receding-fed-hike-bets-202608050354"},
 {"title":"Gold Jumps on Iran Deal Hopes. The Real Driver Is the Fed — GoldSilver (5 August 2026)","url":"https://goldsilver.com/industry-news/goldsilver-news/gold-jumps-on-iran-deal-hopes-the-real-driver-is-the-fed/"},
 {"title":"Asia-Pacific market news 5 August 2026: Gold jumped above US$4,130 — investingLive","url":"https://investinglive.com/news/investinglive-asia-pacific-market-news-5-august-2026-gold-jumped-above-us-4130/"},
])

# ========== 2. india-confirms-the-turn ==========
art("india-confirms-the-turn","gold-metals",False,"Gold & Metals Desk · India",4,"The Gold & Metals Desk",
["NUM","VS"],
"₹1,45,359 and rising: India confirms the metals turn at home",
"October gold on the MCX rose 0.73% to ₹1,45,359 per 10 grams and September silver 1.13% to ₹2,24,109 a kilo. Indian jewellery demand fell 19% in the first quarter and 15% in the second.",
[
"The global bid reached the world's largest jewellery counter on Wednesday. October 2026 gold futures on India's Multi Commodity Exchange traded at ₹1,45,359 per 10 grams, up ₹1,060 or 0.73%, and September 2026 silver at ₹2,24,109 a kilogram, up ₹2,494 or 1.13%. On Tuesday the same gold contract was holding above ₹1,43,500. A domestic contract that rises with global spot rather than lagging it is telling you the rupee is not absorbing the move for the buyer.",
"The context is a market coming off two bad quarters. Indian jewellery demand fell 19% in the first quarter and then to 75.1 tonnes in the second, down 15% from 88.8 tonnes, on World Gold Council figures this desk filed on 31 July. The council's own read was that demand began recovering in late June after a month-long lull, once buyers stopped waiting for a price that was not coming back. A rising futures curve at the start of August is consistent with that read, and it is the opposite of what China is doing: Chinese gold jewellery demand fell 28% in the second quarter to 50 tonnes, the weakest since 2004, as this desk reported on 3 August.",
"The arithmetic on the counter is straightforward. ₹1,45,359 per 10 grams is ₹14,536 a gram of futures-grade metal, a duty-inclusive domestic number that carries India's import levy inside it, which is why it cannot be compared directly with the $133.68 a gram of fine gold on the international spot mark. What a retailer can compare is week to week, and the direction there has been up for three sessions in both markets at once.",
"The caution is that a futures print is not an offtake number. Exchange contracts are traded by hedgers and speculators, not by families buying a chain, and India's real test arrives with the wedding and festival season from September, when the physical demand data catches up with the screen. Third-quarter tonnage will not be published for months. What the futures do confirm is that the domestic and global markets are moving together this week rather than against each other, which is not always true when the rupee is under pressure.",
"The desk's view: India is now carrying Asian demand on its own, and that is a thin plank to stand a recovery on. With China's counter at a twenty-two-year low, an Indian futures market up 0.73% on the day is the only positive tonnage signal in the region, and it is a signal about price expectations rather than about purchases made. Watch the September import numbers, not the screen. If Indian buyers step in at ₹14,536 a gram, the price has found a level the world's largest jewellery market can live with."
],
[
 {"title":"Gold, Silver Prices Today (August 5, 2026) — NewsX","url":"https://www.newsx.com/business/gold-silver-prices-today-august-5-2026-check-city-wise-18k-22k-24k-gold-and-silver-rates-in-delhi-mumbai-chennai-and-more-256851/"},
 {"title":"Gold, silver prices today (August 5) — Business Today","url":"https://www.businesstoday.in/personal-finance/investment/story/gold-silver-prices-today-august-5-check-latest-rates-in-delhi-mumbai-kolkata-other-cities-547247-2026-08-05"},
 {"title":"Gold Rates & Silver Rates Today (04/08/2026): MCX Gold Holds Above Rs 1,43,500 — Goodreturns","url":"https://www.goodreturns.in/news/gold-rates-silver-rates-today-04-08-2026-live-mcx-gold-silver-price-comex-24k-22k-18k-gold-prices-1526065.html"},
])

# ========== 3. hong-kong-fourteen-months ==========
art("hong-kong-fourteen-months","retail-tech",False,"Retail & Technology Desk · Hong Kong",4,"The Retail Desk",
["NUM","RECORD"],
"Twenty percent in June: Hong Kong's fourteenth month up",
"Jewellery, watches and clocks took HK$5.49 billion in June, up 20% year on year, inside overall retail of HK$31.49 billion, up 5%. First-half hard luxury rose 25% to HK$31.07 billion.",
[
"Hong Kong's hard-luxury counter grew four times faster than the shops around it in June. Sales of jewellery, watches, clocks and valuable gifts reached HK$5.49 billion, about $699.9 million, a 20% increase on June 2025, on Census and Statistics Department figures published Tuesday. Total retail sales across every category were HK$31.49 billion, about $4.02 billion, up 5%. That makes hard luxury 17.4% of everything the city sold at retail last month, and the fourteenth consecutive month of overall retail growth.",
"The half-year figures are the stronger evidence. Jewellery, watches and clocks took HK$31.07 billion, about $3.96 billion, in the first six months, up 25%, while all retail categories together took HK$203 billion, about $25.88 billion, up 10%. A category growing at two and a half times the pace of the whole market for six months is not a seasonal effect. The government attributed the run to continued economic expansion, rising local incomes and a steady increase in inbound visitors.",
"One qualification belongs on every reading of these numbers, and it is the gold price. Hong Kong's counters sell a great deal of gold by weight, and gold spent the half at or near record levels, so a shop selling the same grams to the same number of customers prints a larger number. This desk reported Luk Fook's June quarter on 21 July with retail value up 32% and gold same-store sales up 50%, while diamond same-store sales fell 17% and 58% on the mainland. Value is up. Volume is a separate question, and the Census figures do not answer it.",
"The read-through for the trade is about location rather than sentiment. Hong Kong has been the weak point in Greater China luxury for three years, and it is now the strong one while mainland demand falls: Chinese gold jewellery demand hit its lowest second quarter since 2004 in the same period. Any brand deciding where to place Asian inventory for the autumn is looking at a city where hard luxury has outgrown general retail every month since the spring of 2025, and a mainland where the tonnage keeps falling.",
"The desk's view: Hong Kong's recovery is real and it is narrow. Twenty percent growth in a category that is 17.4% of the city's retail spend, in a market where the gold price is doing part of the arithmetic, is a strong signal about the tourist and the local buyer in that one city. It is not a signal about China. Read it as a Hong Kong number, plan inventory for a Hong Kong customer, and wait for the September quarter before extending the line across the border."
],
[
 {"title":"Hong Kong Luxury Sales Strengthen in June — Rapaport (4 August 2026)","url":"https://rapaport.com/news/hong-kong-luxury-sales-strengthen-in-june/"},
 {"title":"Hong Kong June retail sales notch 14th month of growth — Xinhua (4 August 2026)","url":"https://english.news.cn/20260804/1421771e5038465ca18892918c46044d/c.html"},
 {"title":"Hong Kong retail sales rise 4.6% in June as growth streak extends to 14 months — South China Morning Post","url":"https://www.scmp.com/news/hong-kong/hong-kong-economy/article/3362917/hong-kong-retail-sales-rise-46-june-growth-streak-extends-14-months"},
])

# ========== 4. pandora-fills-the-seat ==========
art("pandora-fills-the-seat","retail-tech",False,"Retail & Technology Desk · People",4,"The Retail Desk",
["ACTOR","GAP"],
"Six months empty: Pandora hands North America to a beauty CEO",
"André Branch becomes president of Pandora's North America cluster on 15 August, a seat vacant since Luciano Rodembusch left in February. He arrives from R.E.M. Beauty, with two decades in consumer brands and none in jewellery.",
[
"Pandora has filled the biggest open job in mass-market jewellery. André Branch joins on 15 August as president of the company's North America cluster, succeeding Luciano Rodembusch, who left in February. The seat has therefore been empty for roughly six months, across the period in which American tariff schedules were rewritten twice and the lab-grown share of the engagement counter kept climbing. Pandora describes North America as one of its largest and most important growth markets.",
"The choice is the story. Branch arrives from the chief executive's office at R.E.M. Beauty, and before that spent two decades in senior roles at Estée Lauder, L'Oréal, Diageo and Kraft Heinz. That is a consumer-marketing career, not a jewellery career, and it is a deliberate signal from a company that sells an affordable charm bracelet in the same shopping centre as a cosmetics counter. Pandora's competition for a $70 gift is not a diamond house; it is a fragrance, a handbag and a concert ticket.",
"The vacancy itself is worth marking. Six months without a regional president in a company's largest growth market is a long time to run on an interim structure, and it followed a wider set of executive changes at Pandora North America reported earlier in the year. Whatever the internal reason, the practical effect is that the region's next holiday season will be planned by someone who starts in the middle of August, with the American fourth quarter already substantially bought.",
"Pandora's own recent numbers set the task. This desk covered the group's first quarter on 29 July, and the shape of that quarter was a business with volume but with the same margin pressure every affordable-jewellery brand carries into a record gold market. Branch's brief, in the company's language, is customer engagement and reach. In practice it is holding an American consumer who has been told for two years that a lab-grown stone costs a fraction of a natural one and that a gold chain costs more than it did last month.",
"The desk's view: hiring a beauty executive to run jewellery in America is the most interesting appointment of the summer, because it concedes the category question. Pandora is not competing for the diamond buyer, it is competing for discretionary gift spend, and beauty has run that fight better than jewellery for a decade. The measure of this hire is not a merchandising change, it is whether the fourth-quarter marketing reads like a cosmetics launch. Watch the November campaign, not the August press release."
],
[
 {"title":"Pandora Names André Branch President of North America — JCK (4 August 2026)","url":"https://www.jckonline.com/editorial-article/pandora-new-president-branch/"},
 {"title":"Pandora appoints André Branch as president of its North America cluster — Jewellery Focus","url":"https://www.jewelleryfocus.co.uk/345830-pandora-appoints-andre-branch-as-president-of-its-north-america-cluster"},
 {"title":"Pandora Names New Head of North America — Rapaport (4 August 2026)","url":"https://rapaport.com/news/pandora-names-new-head-of-north-america/"},
])

# ========== 5. luk-fook-fixed-price ==========
art("luk-fook-fixed-price","retail-tech",False,"Retail & Technology Desk · Greater China",5,"The Retail Desk",
["NUM","GAP"],
"Fifty percent on fixed price: how Luk Fook outran the gold price",
"Net profit rose 88.7% to HK$2.015 billion in the year to 31 March, on revenue up 29% to HK$17.21 billion. Fixed-price jewellery sales rose 50.5% against 22% for gold and platinum by weight.",
[
"Luk Fook's full-year figures have been public since late June, and the number that explains them has not travelled. In the year to 31 March 2026 the Hong Kong group's net profit rose 88.7% to HK$2.015 billion, its highest on record, on revenue up 29% to HK$17.21 billion. Gross profit rose 42.9% to HK$6.31 billion and the gross margin reached 36.7%. This paper is filing it now, a month late, because the driver is in the Cantonese and Mandarin financial press rather than in the English pickups, which compressed the year to a profit-growth headline.",
"That driver is the mix. Sales of fixed-price jewellery, priced by the piece rather than by the gram, rose 50.5%. Sales of gold and platinum products priced by weight rose 22%. A weight-priced chain passes the metal cost to the customer and earns the retailer a labour charge on top; a fixed-price piece carries the margin inside the ticket. When gold is at a record and rising, the weight-priced case is where sticker shock lands and the fixed-price case is where the margin survives. Luk Fook's gross margin moved to 36.7% because the second grew more than twice as fast as the first.",
"This desk has been reporting the same company's quarters from the other side of the ledger. On 21 July we filed Luk Fook's June quarter with retail value up 32% and gold same-store sales up 50%; on 22 July, the split within it, gold up 50 and diamond same-store sales down 58% on the mainland. Put the annual mix figure next to those quarters and the shape is a jeweller that has rebuilt its economics around gold, and then, inside gold, around the pieces whose price is not a spot quote.",
"The risk in the strategy is the same as the reward. Fixed-price merchandise protects margin as metal rises but caps the revenue upside when volume returns, and it requires design and brand strength that weight-selling does not, because the customer is being asked to pay for the piece rather than to audit the gram. It also has to be bought forward, which means the hedging desk carries the exposure the shop floor no longer does. Gold added another 1.99% on Wednesday alone.",
"The desk's view: this is the most transferable idea in Asian retail jewellery this year, and most of the English-speaking trade has not read it. Every independent watching gold pass $4,150 an ounce is facing the identical problem, that the metal now costs more than the customer's budget grew, and Luk Fook's answer is to sell fewer grams at a better margin rather than more grams at a worse one. The results are a month old and this is analysis rather than news. The arithmetic is current."
],
[
 {"title":"Lukfook Group FY2026 annual results — pedaily.cn (26 June 2026, in Chinese)","url":"https://news.pedaily.cn/20260626/132917.shtml"},
 {"title":"Luk Fook Sets Profit Record on Gold-Fuelled Jewellery Demand — TipRanks","url":"https://www.tipranks.com/news/company-announcements/luk-fook-sets-profit-record-on-gold-fuelled-jewellery-demand"},
 {"title":"Strong Gold-Jewelry Demand Boosts Luk Fook Sales — Rapaport","url":"https://rapaport.com/news/strong-gold-jewelry-demand-boosts-luk-fook-sales/"},
])

# ========== 6. eighty-percent-to-the-consumer ==========
art("eighty-percent-to-the-consumer","diamonds",False,"Diamonds Desk · Marketing",5,"The Diamonds Desk",
["NUM","ACTOR"],
"Eighty percent to the consumer: the NDC changes the subject",
"Amber Pepper told a GJEPC meeting in Mumbai that at least 80% of Natural Diamond Council advertising now goes to consumers, with a desire index baseline due in September and a trust mark to be inscribed on stones.",
[
"The Natural Diamond Council has put a number on where its money goes. Chief executive Amber Pepper, speaking at a Gem and Jewellery Export Promotion Council meeting in Mumbai on Monday, said at least 80% of the council's advertising spend will be directed at consumers rather than at the trade. She also set out a Diamond Desire Index and a Natural Diamond Mark, and said the council's budget is up significantly on last year without giving the figure.",
"The three instruments are worth separating. The 80% split is a straightforward reallocation away from industry advertising, which is the category that talks to people who already sell diamonds. The Diamond Desire Index is a measurement programme tracking consideration, purchase intent, sentiment and recommendation in India, China and the United States, with a baseline due in September 2026. The Natural Diamond Mark is a trust device, a mark to be inscribed on natural stones and jewellery globally, aimed at a shopper who can no longer tell the two products apart across a counter.",
"Pepper's framing of the job was blunter than the trade is used to hearing from its own marketing body. \"Stop talking about the crisis and start promoting the desirability of natural diamonds,\" she said. Her six transformational pillars are industry unity, category marketing, organisation evolution, consumer design, cultural relevance and category protection, and the council is working with the agency Artefact on optimising how natural diamonds appear inside large language models, which is where a growing share of the pre-purchase research now happens.",
"The arithmetic the campaign is aimed at has not moved much. This desk reported on Tuesday that the RapNet Diamond Index for 1-carat polished was flat in July, ending thirteen months of decline, and that the 0.30 and 0.50-carat bands rose. De Beers' consolidated average realised price fell 32% across the first half to $105 a carat. An advertising budget can change what a shopper wants; it cannot change what a producer clears at a sight, and the desire index will not report a baseline until September, which means the first honest read on whether any of this works arrives in 2027.",
"The desk's view: an 80% consumer split is the right allocation about three years late, and the mark is the more interesting half of the announcement. A category losing to a chemically identical product at a fraction of the price has exactly two defences, provenance and meaning, and an inscribed mark is the only one of the two you can verify at the counter. Retailers should ask now what the mark costs, who applies it, and whether it appears on goods already in their safe. Marketing that arrives without an operational answer to those three questions is a brochure."
],
[
 {"title":"How The Natural Diamond Council Plans to Win Over Consumers — JCK (4 August 2026)","url":"https://www.jckonline.com/editorial-article/natural-diamond-council-plans/"},
 {"title":"NDC unveils consumer-first global strategy — Heera Zhaveraat","url":"https://heerazhaveraat.com/ndc-unveils-consumer-first-global-strategy/"},
 {"title":"Interview With Natural Diamond Council CEO Amber Pepper — JCK","url":"https://www.jckonline.com/editorial-article/natural-diamond-council-ceo-2/"},
])

# ========== 7. joopiter-keeping-measure ==========
art("joopiter-keeping-measure","auctions",False,"Auctions Desk · Watches",4,"The Auctions Desk",
["NUM","ACTOR"],
"$230,000 bid on a moonwalker's Omega: Joopiter opens its watch room",
"Keeping Measure, the first sale from Joopiter's standalone watch department, closes on a rolling basis through 11 August. The top lot, an Omega Speedmaster engraved for Alan Bean and one of thirty made, carries a $250,000 to $350,000 estimate against a $230,000 bid.",
[
"The summer auction calendar has one priced watch offering running, and it belongs to a platform that did not have a watch department three weeks ago. Joopiter, the digital auction house founded by Pharrell Williams, opened Keeping Measure: Watches and Timepieces, the first sale under the standalone department it announced in July, with lots closing on a rolling basis through 11 August. This desk filed the department's creation on 14 July, when Joopiter hired Nate Borgelt from Bonhams to run it.",
"The top lot is an Omega Speedmaster tied to Alan Bean, the fourth man to walk on the moon, estimated at $250,000 to $350,000 with bidding already at $230,000. Thirty examples of the reference were produced after the first moon landing and distributed to President Nixon, Vice President Agnew and astronauts of the period; this is number 26, engraved to mark Bean's later command of the 1973 Skylab mission. Provenance of that specificity is the one thing a new auction room cannot manufacture, and it is what the estimate is priced on.",
"The rest of the catalogue is a deliberate argument rather than a run of blue chips. An HYT Moon Runner Red Magma from 2022 carries $50,000 to $70,000 and a Ulysse Nardin with a Gay Frères bracelet from around 1960 carries $15,000 to $25,000, alongside Patek Philippe, Audemars Piguet, Piaget, Cartier, Ressence, Speake-Marin and Ōtsuka Lotēc. Borgelt's stated aim is to reach seasoned collectors and newcomers in the same sale, which is a different proposition from the Geneva model of one perfect consignment per rostrum.",
"The timing is the sharpest part of the strategy. Watch auction sales reached $680 million in the first half, up 45%, with 73 lots clearing $1 million against roughly 25 a year earlier, as this desk reported on Tuesday. The traditional houses are dark until autumn, with the next priced offering of note Sotheby's Gem Drop in New York from 10 to 13 August. A rolling online sale in the first week of August competes with nothing, and a new department gets its first result printed without a Geneva evening sale sitting on top of it.",
"The desk's view: an online-native house with rolling closes and a celebrity founder is not a novelty any more, it is a distribution channel with a lower cost base than a saleroom. What Joopiter is testing this week is whether provenance sells without a podium. If the Bean Speedmaster clears its low estimate on a screen in August, the calendar stops being the constraint on when a watch can be sold, and the houses that own the autumn dates lose part of what those dates are worth. Watch the hammer, not the headline."
],
[
 {"title":"Pharrell's Joopiter Launches Dedicated Watches Department — JCK (4 August 2026)","url":"https://www.jckonline.com/editorial-article/joopiter-watch-department/"},
 {"title":"JOOPITER's Keeping Measure Auction Frames Watch Collecting Beyond the Usual Canon — stupidDOPE (August 2026)","url":"https://stupiddope.com/2026/08/joopiters-keeping-measure-auction-frames-watch-collecting-beyond-the-usual-canon/"},
 {"title":"JOOPITER","url":"https://www.joopiter.com/"},
])

# ---------------- editorial specs ----------------
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

specs["four-metals-third-session"] = {
 **strip("By the numbers · Kitco spot, 5:58am New York",[
   {"fig":"$4,157.80","delta":"▲ +1.99%","dir":"up","lab":"gold, third session up"},
   {"fig":"$61.35","delta":"▲ +3.27%","dir":"up","lab":"silver, leads again"},
   {"fig":"$1,747.00","delta":"▲ +1.10%","dir":"up","lab":"platinum"},
   {"fig":"$1,355.00","delta":"▲ +1.96%","dir":"up","lab":"palladium"},
   {"fig":"67.8","lab":"gold to silver ratio, from 69.0"}]),
 "figs":[bars("Plate I","Session change by metal · 5 August 2026",[
   {"l":"SILVER","v":3.27,"d":"+3.27%","hi":True},
   {"l":"PALLADIUM","v":1.96,"d":"+1.96%"},
   {"l":"GOLD","v":1.99,"d":"+1.99%"},
   {"l":"PLATINUM","v":1.10,"d":"+1.10%"}],
   "Per cent against Tuesday's close. Kitco spot, 5:58am New York, 5 August 2026.",181)],
 "flow":flow5("Every metal on the board, a third day running.","The gram, not the ounce.","Two cautions for the record.",
   "Gold rose because the war premium is coming out, not because it is going in.","The Gold & Metals Desk",
   "Gold's oldest rule broke in a war week","a-war-premium-inverts.html"),
 "desk":{"split":"a metals rally built on peace talk is a rate trade wearing a geopolitics costume"},
 "next":nxt("india-confirms-the-turn","India","The domestic futures curve rose with the global bid, not behind it.",
   "platinum-adds-one-seven","Metals","gold-waits-on-payrolls","The Fed")}

specs["india-confirms-the-turn"] = {
 **strip("By the numbers · MCX, 5 August 2026",[
   {"fig":"₹1,45,359","delta":"▲ +0.73%","dir":"up","lab":"October gold, per 10g"},
   {"fig":"₹2,24,109","delta":"▲ +1.13%","dir":"up","lab":"September silver, per kg"},
   {"fig":"₹14,536","lab":"gold, per gram"},
   {"fig":"−15%","dir":"down","lab":"Q2 jewellery demand"},
   {"fig":"75.1t","lab":"Q2 jewellery, from 88.8t"}]),
 "figs":[bars("Plate I","Indian jewellery demand, quarterly change",[
   {"l":"Q2 2026","v":-15,"d":"−15%","hi":True},
   {"l":"Q1 2026","v":-19,"d":"−19%"}],
   "Per cent year on year. World Gold Council, filed 31 July 2026.",182)],
 "flow":flow5("The global bid reaches the counter.","Two bad quarters behind it.","A screen price is not an offtake number.",
   "A domestic contract that rises with global spot rather than lagging it is telling you the rupee is not absorbing the move for the buyer.","The Gold & Metals Desk",
   "India's quarter: 75.1 tonnes, down 15%","a-india-buys-fifteen-percent-less.html"),
 "desk":{"split":"India is now carrying Asian demand on its own, and that is a thin plank to stand a recovery on"},
 "next":nxt("four-metals-third-session","Metals","Every precious metal on the board rose for a third session.",
   "china-lowest-since-2004","China","india-buys-fifteen-percent-less","Demand")}

specs["hong-kong-fourteen-months"] = {
 **strip("By the numbers · Hong Kong retail, June 2026",[
   {"fig":"HK$5.49B","delta":"▲ +20%","dir":"up","lab":"jewellery, watches, clocks"},
   {"fig":"HK$31.49B","delta":"▲ +5%","dir":"up","lab":"all retail, June"},
   {"fig":"17.4%","lab":"hard luxury share of retail"},
   {"fig":"HK$31.07B","delta":"▲ +25%","dir":"up","lab":"hard luxury, first half"},
   {"fig":"14","lab":"consecutive months of growth"}]),
 "figs":[bars("Plate I","First-half growth, Hong Kong retail",[
   {"l":"JEWELLERY, WATCHES, CLOCKS","v":25,"d":"+25%","hi":True},
   {"l":"ALL RETAIL CATEGORIES","v":10,"d":"+10%"}],
   "Per cent year on year, January to June 2026. Census and Statistics Department via Rapaport.",183)],
 "flow":flow5("Four times the pace of the shops around it.","The gold price does part of the arithmetic.","A Hong Kong number, not a China number.",
   "A category growing at two and a half times the pace of the whole market for six months is not a seasonal effect.","The Retail Desk",
   "Hong Kong's gold counters run hot","a-gold-counters-run-hot.html"),
 "desk":{"split":"Hong Kong's recovery is real and it is narrow"},
 "next":nxt("luk-fook-fixed-price","Greater China","The mix, not the metal, made Luk Fook's record year.",
   "china-lowest-since-2004","China","gold-up-fifty-diamonds-down","Luk Fook")}

specs["pandora-fills-the-seat"] = {
 **strip("The appointment · Pandora North America",[
   {"fig":"15 Aug","lab":"Branch starts"},
   {"fig":"~6 mo","lab":"seat empty since February"},
   {"fig":"20 yrs","lab":"consumer brands, none in jewellery"},
   {"fig":"R.E.M.","lab":"arrives from the beauty chair"},
   {"fig":"Q4","lab":"American season already bought"}]),
 "flow":flow5("The biggest open job in mass-market jewellery.","A consumer-marketing career, not a jewellery one.","What the brief actually is.",
   "Pandora's competition for a $70 gift is not a diamond house; it is a fragrance, a handbag and a concert ticket.","The Retail Desk",
   "Who buys diamonds now","a-who-buys-diamonds-now.html"),
 "desk":{"split":"hiring a beauty executive to run jewellery in America is the most interesting appointment of the summer"},
 "next":nxt("hong-kong-fourteen-months","Retail","Hong Kong's hard luxury grew four times faster than the shops around it.",
   "sixty-one-percent-said-lab","Lab-grown","average-ticket-carries-the-half","Counters")}

specs["luk-fook-fixed-price"] = {
 **strip("By the numbers · Luk Fook, year to 31 March 2026",[
   {"fig":"HK$2.015B","delta":"▲ +88.7%","dir":"up","lab":"net profit, a record"},
   {"fig":"HK$17.21B","delta":"▲ +29%","dir":"up","lab":"revenue"},
   {"fig":"+50.5%","dir":"up","lab":"fixed-price jewellery sales"},
   {"fig":"+22%","dir":"up","lab":"gold and platinum, by weight"},
   {"fig":"36.7%","lab":"gross margin"}]),
 "figs":[bars("Plate I","Sales growth by pricing model · FY2026",[
   {"l":"FIXED-PRICE JEWELLERY","v":50.5,"d":"+50.5%","hi":True},
   {"l":"GOLD & PLATINUM, BY WEIGHT","v":22,"d":"+22%"}],
   "Per cent year on year, twelve months to 31 March 2026. Company results via Chinese-language financial press.",184)],
 "flow":flow5("The number that did not travel.","The mix, not the metal.","What the strategy costs.",
   "When gold is at a record and rising, the weight-priced case is where sticker shock lands and the fixed-price case is where the margin survives.","The Retail Desk",
   "Luk Fook's split quarter","a-gold-up-fifty-diamonds-down.html"),
 "desk":{"split":"this is the most transferable idea in Asian retail jewellery this year"},
 "next":nxt("hong-kong-fourteen-months","Hong Kong","Hard luxury took HK$5.49 billion in June, up 20%.",
   "gold-counters-run-hot","Counters","china-lowest-since-2004","China")}

specs["eighty-percent-to-the-consumer"] = {
 **strip("The plan · Natural Diamond Council",[
   {"fig":"80%","lab":"of advertising, to consumers"},
   {"fig":"Sept","lab":"desire index baseline due"},
   {"fig":"3","lab":"markets tracked: India, China, US"},
   {"fig":"6","lab":"transformational pillars"},
   {"fig":"$105","delta":"▼ −32%","dir":"down","lab":"De Beers realised price, H1"}]),
 "flow":flow5("A number on where the money goes.","Three instruments, separated.","The arithmetic it is aimed at.",
   "The Natural Diamond Mark is a trust device, a mark to be inscribed on natural stones and jewellery globally, aimed at a shopper who can no longer tell the two products apart across a counter.","The Diamonds Desk",
   "The 1-carat stops falling","a-the-one-carat-stops-falling.html"),
 "desk":{"split":"an 80% consumer split is the right allocation about three years late"},
 "next":nxt("the-one-carat-stops-falling","Polished","July ended thirteen months of decline at flat.",
   "who-buys-diamonds-now","Demand","lab-grown-finds-its-floor","Lab-grown")}

specs["joopiter-keeping-measure"] = {
 **strip("The sale · Keeping Measure, closes 11 August",[
   {"fig":"$230,000","lab":"standing bid, top lot"},
   {"fig":"$250–350K","lab":"estimate, Bean Speedmaster"},
   {"fig":"30","lab":"examples made after Apollo 11"},
   {"fig":"$680M","delta":"▲ +45%","dir":"up","lab":"H1 watch auction sales"},
   {"fig":"73","lab":"H1 lots over $1 million"}]),
 "flow":flow5("One priced watch offering, and it is not a saleroom.","Provenance is the thing that cannot be manufactured.","The timing is the strategy.",
   "Provenance of that specificity is the one thing a new auction room cannot manufacture, and it is what the estimate is priced on.","The Auctions Desk",
   "73 lots over a million","a-seventy-three-lots-over-a-million.html"),
 "desk":{"split":"an online-native house with rolling closes and a celebrity founder is not a novelty any more"},
 "next":nxt("seventy-three-lots-over-a-million","Auctions","Watch auction sales rose 45% to $680 million in the half.",
   "joopiter-24-million-resume","Joopiter","independents-pass-lvmh","Secondary")}

# ---------------- validation ----------------
existing = {a["slug"] for a in articles} | {d["slug"] for d in NEW}
fail = []
for d in NEW:
    s = d["slug"]
    if len(d["body"]) != 5: fail.append(f"{s}: body has {len(d['body'])} paragraphs, need 5")
    if not d["body"][4].startswith("The desk's view:"): fail.append(f"{s}: last paragraph does not open 'The desk's view:'")
    sp = specs.get(s)
    if not sp: fail.append(f"{s}: no editorial spec"); continue
    split = sp["desk"]["split"]
    if split not in d["body"][4]: fail.append(f"{s}: desk.split not verbatim in last paragraph")
    pull = [f["pull"]["q"] for f in sp["flow"] if "pull" in f][0]
    if not any(pull in p for p in d["body"][:4]): fail.append(f"{s}: pull quote not verbatim in paras 0-3")
    for f in sp["flow"]:
        if "also" in f:
            href = f["also"]["href"]
            slug = href[2:-5]
            if slug not in existing: fail.append(f"{s}: also-read slug {slug} does not exist")
            if slug == s: fail.append(f"{s}: also-read self-reference")
    nx = sp["next"]
    for ns in [nx["lead"]["slug"]] + [m["slug"] for m in nx["minis"]]:
        if ns not in existing: fail.append(f"{s}: next slug {ns} does not exist")
        if ns == s: fail.append(f"{s}: next self-reference")
if fail:
    print("VALIDATION FAILED"); [print(" -",f) for f in fail]; sys.exit(1)

leads = [a for a in NEW if a.get("lead")]
assert len(leads) == 1, leads
for s in specs: editorial[s] = specs[s]
articles = NEW + articles
(C/"articles.json").write_text(json.dumps(articles, ensure_ascii=False, indent=1))
(C/"editorial.json").write_text(json.dumps(editorial, ensure_ascii=False, indent=1))
print("edition No.026 written:", len(NEW), "articles, lead =", leads[0]["slug"], "| total", len(articles))
