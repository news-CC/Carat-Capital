#!/usr/bin/env python3
# Edition No. 020 - 2026-07-30. Prepends 8 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-07-30"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - one-billion-for-de-beers ==========
art("one-billion-for-de-beers","diamonds",True,"Lead Story · Diamonds Desk",5,"The Diamonds Desk",
["NUM","ACTOR","STAKES"],
"One billion for De Beers, and $750 million of it up front",
"Bloomberg puts the Gareth Penny consortium's price at about $1 billion: roughly $750 million on closing and $250 million later, with some $500 million of working capital going in behind it. Book value earlier this year was $2.3 billion.",
[
"Anglo American's exit from diamonds now has a number attached, and it is a small one. Bloomberg reported on Wednesday that the Global Diamond Consortium, the group led by former De Beers chief executive Gareth Penny, would pay about $1 billion for Anglo's 85% stake: roughly $750 million on closing and a further $250 million deferred. The consortium would then put around $500 million of working capital into the business it had just bought. Terms are not final, and neither side has confirmed them on the record.",
"Set that against the ledger. De Beers carried a book value of about $2.3 billion earlier this year, after Anglo took $3.5 billion of write-downs against the asset. When the business was taken private in 2001 it was valued at $17.6 billion. A price of $1 billion is therefore not a discount to a peak so much as an admission that the peak belonged to a different industry.",
"The June quarter explains where the bid sits. De Beers dug 88% more rough than a year earlier, 7.8 million carats, and banked 44% less for it: revenue of $665 million at an average price of $105 a carat, down 32%. Producing into the weakest market in a generation is what a miner does when its mine plans were set years ago and its buyers were not. A purchaser is pricing that inventory, not the marketing.",
"The politics are the harder part of the arithmetic. Botswana owns the other 15% and has told its parliament that the stake carries complete freedom: join the consortium, exercise pre-emption alone, or bid alongside a third party. Namibia and Angola already sit inside the Penny group, so three producer governments would end up on the same side of the table as the traders who buy from them. Anglo still expects to close by the end of 2026.",
"The desk's view: a billion dollars is the trade's own valuation of the story it has been telling itself since 2022. What the buyer gets is the Forevermark shelf space, the Botswana relationship, the Element Six industrials arm, and a rough book that now has to be sold into the market rather than above it. The number that matters is not the $1 billion but the $500 million going in behind it, because the price of the asset is now smaller than the cost of carrying it through another soft year."
],
[
 {"title":"Anglo Said to Be in Talks to Sell De Beers for About $1 Billion — Bloomberg","url":"https://www.bloomberg.com/news/articles/2026-07-29/anglo-said-to-be-in-talks-to-sell-de-beers-for-about-1-billion"},
 {"title":"Anglo American Mulling $1B De Beers Sale — Rapaport","url":"https://rapaport.com/news/anglo-american-mulling-1b-de-beers-sale-report/"},
 {"title":"JCK Take 3: Is De Beers Worth Only $1 Billion? — JCK","url":"https://www.jckonline.com/editorial-article/jck-take-3-de-beers-only-1-billion/"},
 {"title":"Production Report for the Second Quarter of 2026 — De Beers Group","url":"https://www.debeersgroup.com/news-insights/latest-group-news/2026/production-report-for-the-second-quarter-of-2026"},
])

# ========== 2. angolas-rough-clears ==========
art("angolas-rough-clears","diamonds",False,"Diamonds Desk · Luanda",4,"The Rough Desk",
["NUM","GAP"],
"Ninety-five percent sold in Luanda, and Sodiam beats its book by 23%",
"TAGS cleared 95% of a Luanda tender of goods above 10.8 carats and called trading near normal. Sodiam's seventeenth auction took about $21.7 million net from 6,586.89 carats, 23.46% above expected value.",
[
"Angola's rough is finding buyers, and at prices its own sellers did not forecast. Trans Atlantic Gem Sales, the Dubai tender house that markets Angolan production alongside the state trader Sodiam, closed a Luanda sale of goods above 10.8 carats with a 95% sell-through and described the result as a \"return to near normal trading.\" In a year when nearly every rough seller has cut prices, withdrawn goods or done both, a 95% clearance is worth writing down.",
"The state channel says the same thing with more detail. Sodiam took approximately $21.7 million net from its seventeenth rough auction, selling 6,586.89 carats and beating its own expected value by 23.46%. Twenty-seven of the thirty-four houses invited put in bids; viewing ran at Sodiam's Luanda premises from 22 to 25 June and electronic bidding closed on the morning of 26 June. An auction that lands nearly a quarter above the reserve book is not the behaviour of a market in retreat.",
"The split is by size, not by geography. In the same soft market, Petra's fourth-quarter revenue fell 44% to $38 million on weak tender prices and small goods, and De Beers' average price dropped 32% to $105 a carat. Gem Diamonds, selling Letseng's large Type IIa material, lifted its average about 17% to roughly $1,501 a carat. Angolan tenders are built around exactly that end of the size curve, which is why they read as strength while the near-commercial book stays under water.",
"Angola intends to sell more of it. Endiama, the state mining company, has set out an expansion programme, and its commercial director Elton Escrivão has been making the case for the country as a growth source rather than a legacy one. The government is also a member of the Global Diamond Consortium bidding for De Beers, which would put Angola on both sides of the rough market at once: producing the goods and owning a share of the channel that prices them.",
"The desk's view: two Luanda results do not turn a market, and the 95% figure covers only the top of the size range, where money has been comfortable all year. But the direction is useful. Buyers are paying up for stones that cannot be replaced by a factory and walking away from the ones that can, and Angola happens to sit on the right side of that line. For a cutter, the read is simple: the scarcity premium is real above ten carats and still absent below one."
],
[
 {"title":"TAGS: 'Return to Near Normal Trading' — IDEX Online","url":"https://www.idexonline.com/"},
 {"title":"17th Rough Diamond Auction Organised by Sodiam E.P. Generates Approximately USD 21.7 Million — Mines to Market","url":"https://minestomarket.news/17th-rough-diamond-auction-organised-by-sodiam-e-p-generates-approximately-usd-21-7-million/"},
 {"title":"Q&A: The Past and Future of Angola's Diamond Industry — National Jeweler","url":"https://nationaljeweler.com/articles/15170-q-a-the-past-and-future-of-angola-s-diamond-industry"},
 {"title":"Weak Market and Product Mix Dent Petra Revenue — Rapaport","url":"https://rapaport.com/news/weak-market-and-product-mix-dent-petra-revenue/"},
])

# ========== 3. gold-unwinds-the-hold ==========
art("gold-unwinds-the-hold","gold-metals",False,"Gold & Metals Desk · New York",4,"The Bullion Desk",
["NUM","STAKES"],
"Gold takes back $4,075 the morning after the hold",
"Spot recovered to about $4,074.98, up 0.22% on the day and 23.84% on the year, erasing Wednesday's post-FOMC slip to $4,029. Silver eased to $57.79 and the gold-silver ratio widened to 70.37.",
[
"Gold undid the Fed in a single session. Spot traded near $4,074.98 an ounce on Thursday, up about 0.22% on the day, which puts it roughly $46 above Wednesday's post-decision level of $4,029 and back inside the range it occupied before the Federal Open Market Committee met. On the year the metal is 23.84% higher. A hawkish hold with three dissents moved the price for an afternoon and not much longer.",
"That is the tell worth keeping. The market spent two days pricing a genuinely two-sided meeting, sold the outcome, and bought it back before the week was out. What did not change is the bid underneath: central banks took a net 244 tonnes in the first quarter and 41 tonnes in May, and reserve managers surveyed this year expect official holdings to keep rising. Official buying is indifferent to a quarter-point, which is why every dip since spring has found a floor before it found a seller of consequence.",
"Silver did not join in. The metal slipped to $57.79 from $57.94 on Wednesday, a fall of about 0.25%, and the gold-silver ratio widened to 70.37 from 70.22. Silver has spent July trying and failing to hold $60 after an intraday $60.11 earlier in the month, and the ratio drifting back above 70 is the quiet way of saying gold is doing the work while silver looks for an industrial reason to follow.",
"For the counter, the number that matters is the one on the tag rather than the one on the screen. At $4,075 an ounce, fine gold runs about $131 a gram before any making charge, and the buyer who walked in at $3,300 last summer is looking at the same chain for close to a quarter more. India's July demand picture from the World Gold Council showed exactly how that resolves: jewellery buyers trading down and funding purchases with old gold, while bar, coin and fund demand stayed firmer.",
"The desk's view: a market that recovers a hawkish hold in twenty-four hours is telling you the rate path is no longer the main driver. The floor to watch is still $3,964, and above it the trade should plan for a $4,000 handle as the operating assumption rather than the exception. That means retail buying gold at these levels is behaving rationally, not exuberantly, and the retailer who is still quoting last year's price points is the one carrying the risk."
],
[
 {"title":"Gold — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/gold"},
 {"title":"Silver price today: silver falls, 30 July 2026 — FXStreet","url":"https://www.fxstreet.com/news/silver-price-today-silver-falls-according-to-fxstreet-data-202607300931"},
 {"title":"The price of gold today, July 29, 2026 — CNBC Select","url":"https://www.cnbc.com/select/the-price-of-gold-today-july-29-2026/"},
])

# ========== 4. platinum-loses-its-teacher ==========
art("platinum-loses-its-teacher","gold-metals",False,"Gold & Metals Desk · New York",4,"The Metals Desk",
["VS","ACTOR","NUM"],
"Platinum jumps to $1,628 as the man who taught it retires",
"Platinum rose 1.62% to $1,628.20 and is 26.13% higher on the year, yet global platinum jewellery demand is forecast to contract 6% in 2026. PGI USA announced Kevin Reilly's retirement on July 28.",
[
"Platinum had a good Thursday and a bad forecast. The metal rose 1.62% to $1,628.20 an ounce, up 1.77% on the month and 26.13% on the year, with palladium alongside it at $1,284.00 after a 2.51% jump. Analysts still expect a fourth consecutive annual supply deficit. Set against January's all-time high of $2,923.70, the metal is both far off its peak and comfortably above where the jewellery trade was buying it a year ago.",
"The showroom is pointing the other way. Global platinum jewellery demand is expected to contract about 6% in 2026, with growth in North America and Europe consolidating after two strong years, India facing tariff-related headwinds, and China supplying most of the decline. That is the awkward shape of this market: a metal whose investment and industrial case keeps strengthening while the counter that carries its name sells less of it.",
"The timing of the trade's other platinum news is hard to ignore. Platinum Guild International USA announced on July 28 that Kevin Reilly, its senior vice president, had retired at the end of June after twenty years with the organisation and a thirty-nine-year career in the industry. Reilly built the education side of the American platinum business, establishing programmes at the Gemological Institute of America, Pratt Institute, the Savannah College of Art and Design, the Rhode Island School of Design, the 92Y Jewelry Center and the Miami Jewelry School.",
"That work is why platinum has a bench in the United States at all. A metal that melts near 1,770 degrees Celsius and behaves nothing like gold under a torch does not get used unless someone teaches people to set it, and the difference between a house that can sell platinum and one that cannot is usually a training programme rather than a price list. Reilly says he will take on some consulting and stay with special events, including the Macy's Thanksgiving Day Parade committee, which he has served for forty-eight years.",
"The desk's view: platinum at $1,628 with a fourth deficit forecast and a 6% demand contraction is a metal being repriced by industry while jewellery watches from the sidelines. The opportunity is the discount to gold, which at these levels buys a bridal ring in a rarer metal for less money per gram of finished weight. Whether the American counter can still make that argument now depends on whether the teaching Reilly institutionalised outlasts the man, and that is a question for PGI's next hire rather than for the tape."
],
[
 {"title":"Platinum — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/platinum"},
 {"title":"Palladium — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/palladium"},
 {"title":"Kevin Reilly Retires After 39 Years in the Jewelry Industry — National Jeweler","url":"https://nationaljeweler.com/articles/15176-kevin-reilly-retires-after-39-years-in-the-jewelry-industry"},
 {"title":"Kevin Reilly Retires After 20 Years at Platinum Guild International — JCK","url":"https://www.jckonline.com/editorial-article/kevin-reilly-platinum-retire/"},
])

# ========== 5. four-groups-in-the-black ==========
art("four-groups-in-the-black","watches",False,"Watches Desk · Zurich",4,"The Movement Desk",
["RECORD","NUM"],
"All four Swiss groups turn positive for the first time since 2022",
"Morgan Stanley's second-quarter secondary-market index rose 1.5%, with Swatch Group up 5.4% and Richemont 4.2% year on year. April was the market's best single month since March 2022 at plus 2.5%.",
[
"The secondhand watch market has finished the job it started in 2022. Morgan Stanley's second-quarter index of Swiss watch resale prices rose 1.5%, and for the first time since early 2022 all four of the groups it tracks are positive year on year. Swatch Group is up 5.4% over twelve months and Richemont 4.2%. Sequentially, Richemont gained 1.3% in the quarter and Swatch 1.0%. After three years in which the resale tape only told bad news, the bad news has stopped.",
"April did most of the lifting. The WatchCharts overall market index gained 2.5% that month, its best single month since March 2022, carried by the run-up to Watches and Wonders. Dealers responded the way dealers do, pushing secondary supply to record levels, and demand could not keep pace through May and June. That is why a quarter that contains the market's best month in four years still only prints 1.5% overall.",
"Read against the primary market, the picture is coherent rather than contradictory. Swiss exports rose 11.2% in June to nearly 2.4 billion francs, and first-half volumes were up 2.3% with 162,000 more units shipped. Exports to the United States fell 14.8% in the half, against a comparison base inflated by the 150% April 2025 surge ahead of tariffs. The Middle East, roughly a tenth of Swiss exports, has been unsettled since February.",
"What makes a resale floor matter to a retailer is collateral. A rising secondary index means a trade-in has a defensible number on it, a pre-owned case is financeable, and a client considering a five-figure watch can be shown a residual value rather than asked to ignore one. Falling resale prices did the opposite for three years, and the pawn and consignment desks priced accordingly.",
"The desk's view: 1.5% in a quarter is not a boom and nobody should sell it as one, particularly with dealer inventory at record levels and demand that faded in May and June. The signal is narrower and more useful than a rally. The direction of the secondary market has flipped from headwind to mild tailwind, and that changes the arithmetic on every trade-in, every financing conversation and every pre-owned case in the window."
],
[
 {"title":"Morgan Stanley's Q2 2026 Swiss Watch Market Report — ScrewDownCrown","url":"https://www.screwdowncrown.com/p/morgan-stanley-q2-2026"},
 {"title":"July 2026 Watch Market Update — WatchCharts","url":"https://watchcharts.com/articles/p/9418/july-2026-watch-market-update"},
 {"title":"Swiss Watch Exports Rise in June, Show Stability for Future — JCK","url":"https://www.jckonline.com/editorial-article/swiss-watch-exports-up-june/"},
 {"title":"Watch industry statistics — Federation of the Swiss Watch Industry","url":"https://www.fhs.swiss/eng/statistics.html"},
])

# ========== 6. heritage-books-a-record-half ==========
art("heritage-books-a-record-half","auctions",False,"Auctions Desk · Dallas",4,"The Saleroom Desk",
["NUM","RECORD"],
"Heritage books $1.41 billion, and its biggest jewelry sale ever",
"First-half sales rose 47% to more than $1.41 billion, the highest midyear total in the firm's fifty years. Its May 4 jewelry auction made $9,713,640, led by a 6.59-carat Kashmir sapphire at $906,250.",
[
"Heritage Auctions took more than $1.41 billion in the first six months of 2026, a 47% increase on the same period last year and the highest midyear total in the company's fifty-year history. The Dallas house is not where the trade usually looks for a read on jewelry, which is precisely why the number is interesting: Heritage sells to collectors who arrived through sports cards, comics and coins, and it has now sold more jewelry in a single session than at any point in its history.",
"That session was the Spring Fine Jewelry Signature auction on May 4, which realised $9,713,640 and passed the firm's previous jewelry record of $9.2 million set in September 2025. The top lot was a platinum ring set with a 6.59-carat octagonal Kashmir sapphire at $906,250, more than $300,000 above its high estimate. One stone accounted for roughly 9% of the sale, which is the shape of every strong jewelry auction this year.",
"The wider saleroom tape agrees. Global sales at Christie's, Sotheby's and Phillips rose 70% year on year in the first half to $6.8 billion with fees, Sotheby's alone printing a record $4.4 billion, and Christie's luxury division running $539 million so far in 2026, up 15%. Watches, jewels, cars and memorabilia have been the entry point rather than the afterthought, and houses have restructured their calendars around that.",
"For a jeweller, the auction record is a pricing instrument. When a Kashmir sapphire clears $906,250 against a $600,000 high estimate, the estate counter has a defensible comparable for unheated origin material and the insurance appraisal that was written three years ago is wrong in a direction the client will not like. Heritage's growth also matters structurally: it is a low-friction consignment route for the mid-market estate goods that the London and Geneva houses will not take.",
"The desk's view: $1.41 billion across fifty categories tells you about the collectibles cycle, but $9.7 million in one jewelry room tells you about ours. The buyers turning up are new to jewelry and old to bidding, and they price scarcity the way a coin collector does, on origin and condition rather than on brand. The house that learns to write a condition report like an auction cataloguer will win those clients; the one still selling on carat weight alone will not."
],
[
 {"title":"Heritage Auctions' Record $1.41 B. First Half Suggests Collecting Is Getting Broader — ARTnews","url":"https://www.artnews.com/art-news/market/heritage-auctions-record-first-half-2026-1-41-billion-sales-1234791884/"},
 {"title":"Heritage Celebrates Largest Jewelry Auction Total in Its History With $9.7 Million Spring Event — Intelligent Collector","url":"https://intelligentcollector.com/heritage-celebrates-largest-jewelry-auction-total-in-its-history-with-9-7-million-spring-event/"},
 {"title":"'Spectacular' Kashmir Sapphire Headlines Heritage Spring Jewelry Sale — National Jeweler","url":"https://nationaljeweler.com/articles/14947-spectacular-kashmir-sapphire-headlines-heritage-spring-jewelry-sale"},
 {"title":"Trophy lots and luxury goods fuel rebound for Christie's and Sotheby's 2026 half-year results — The Art Newspaper","url":"https://www.theartnewspaper.com/2026/07/15/trophy-lots-and-luxury-goods-fuel-rebound-for-christies-and-sothebys-2026-half-year-results"},
])

# ========== 7. the-storefront-that-isnt ==========
art("the-storefront-that-isnt","retail-tech",False,"Retail & Tech Desk · London",4,"The Counter Desk",
["STAKES","GAP"],
"The 80% closing-down sale that was never a shop",
"AI-built jewellery storefronts are running fake retirement and bereavement sales at 80% to 90% off, using scraped product photography and synthetic voiceovers. Buyers report receiving resin, plastic and plated metal, or nothing at all.",
[
"A category of jewellery retailer has appeared this year that has no bench, no stock and no address. IDEX reported on Thursday that buyers had been defrauded by a jewellery website advertising 80% discounts in a closing-down sale that was never happening. It is not an isolated site. Seren Cardiff Jewellery presented itself as a Welsh independent and took hundreds of pounds from shoppers who never received goods, its product photographs lifted from other sellers.",
"The pattern is consistent enough to be a template. A storefront claims a long family history and a forced ending: Maya and Henry advertised a thirty-three-year business retiring and selling handmade solid gold at 80% to 90% off, narrated by a British-accented synthetic voice over a claim to be an American family firm. C'est La Vie ran a bereavement story and an 80% clearance; buyers described receiving lumps of resin, plastic and cheap plated metal. Aisha Jewelry stacked up-to-80% discounts with multi-buy offers.",
"What has changed is the cost of looking legitimate. Generative tools now produce the product photography, the founder's biography, the voiceover and the review copy for the price of a domain and a card processor, which removes the friction that used to make a convincing fake shop expensive. Bitdefender has documented the ad side of it, where emotional narratives about closure and bereavement do the work that a discount alone no longer does. Countdown timers and stock warnings finish the job.",
"The cost lands on real jewellers twice. The first hit is the sale that goes to a fake competitor at an impossible price. The second is slower and worse: a customer who has been burned by an 80%-off gold ring becomes harder to sell to at any discount, and the independent jeweller who genuinely is retiring after thirty years now shares a script with a fraud. Trust is the working capital of a business that asks people to buy something they cannot value.",
"The desk's view: this is a marketing problem, not an IT one, and the trade should answer it with proof rather than warnings. A verifiable street address, a named registered company, a hallmarking record, a real returns route and a payment method with recourse are all things a fake storefront cannot cheaply manufacture, and all things most independents already have and rarely show. The retailer's job now is to make the boring evidence of being real as visible as the discount."
],
[
 {"title":"Jewelry Buyers Duped by AI Scam Website — IDEX Online","url":"https://www.idexonline.com/"},
 {"title":"We thought we were buying Welsh jewellery but the shop was an AI scam — WelshWave","url":"https://welshwave.co.uk/6664143/we-thought-we-were-buying-welsh-jewellery-but-the-shop-was-an-ai-scam/"},
 {"title":"Scammers Use Fake Jewelry Store Ads to Steal Your Money — Bitdefender","url":"https://www.bitdefender.com/en-us/blog/hotforsecurity/scam-alert-fake-jewelry-store-ads-exploit-heart-felt-stories-to-steal-your-money"},
 {"title":"Maya and Henry Jewelry Scam: Fake Store Exposed — TempoMail","url":"https://tempomailusa.com/post/maya-and-henry-jewelry-scam-fake-store-exposed"},
])

# ========== 8. color-runs-two-speeds ==========
art("color-runs-two-speeds","gemstones",False,"Gemstones Desk · New York",4,"The Color Desk",
["VS","NUM"],
"Two speeds in color: $906,250 for one sapphire, demand still 30% down",
"A 6.59-carat Kashmir sapphire cleared $906,250 in Dallas while ICA members report colored-stone demand roughly 30% below 2022. Mahenge spinel is up 150% since the pandemic; tsavorite has fallen 15% to 20% in a year.",
[
"Two numbers describe the colored-stone market and they point in opposite directions. A platinum ring set with a 6.59-carat Kashmir sapphire made $906,250 at Heritage in May, more than $300,000 above its high estimate, in the largest jewelry auction that house has held. Meanwhile members of the International Colored Gemstone Association report demand running roughly 30% below 2022 levels, with association president Damien Cody describing slow trading across the membership.",
"The gap is a size and quality gap, not a confusion. Rapaport's survey of the trade in January put Mahenge spinel up about 150% since the pandemic and Mozambican Paraiba up from around $7,000 a carat to between $10,000 and $12,000. Untreated calibrated tsavorite, calibrated pink sapphire and single blue sapphires above three carats had each gained more than 50%. A one-carat untreated royal-blue sapphire moved from about $3,000 to $4,000 or $5,000.",
"The same survey shows where the softness sits. Tsavorite has given back 15% to 20% over the last twelve months as Chinese demand thinned, and the broad commercial book has been flat to weaker throughout. Currency has muddied the read further: Colombian emeralds are up close to 20% on exchange rates alone, and Zambian emeralds 25% to 30%, which means part of what a dealer calls a price rise is a dollar story rather than a stone story.",
"Retail is the part of this market nobody is measuring well. The dealer and designer Kimberly Collins reports demand up 30% to 35% since the pandemic and says she now fields \"at least one inquiry a day\" for colored-stone engagement rings, which is not the picture a 30% wholesale decline suggests. Both can be true: bridal has genuinely shifted toward color while the tourist, gift and mid-commercial channels that once absorbed most calibrated goods have not come back.",
"The desk's view: this is a market that has stopped clearing in the middle. Fine untreated material with documented origin is scarce enough to keep setting records, the commercial book is discounting, and the space between them is where inventory now goes to die. For a jeweller, that argues for buying fewer stones with better reports rather than more stones at better prices, and for treating the lab document as the product. The ICA's first Plus event lands in Hong Kong in September, and the pricing conversation there will be about paper as much as color."
],
[
 {"title":"An Incongruous Moment for the Gemstone Industry — Rapaport Magazine","url":"https://rapaport.com/magazine-article/an-incongruous-moment-for-the-gemstone-industry/"},
 {"title":"'Spectacular' Kashmir Sapphire Headlines Heritage Spring Jewelry Sale — National Jeweler","url":"https://nationaljeweler.com/articles/14947-spectacular-kashmir-sapphire-headlines-heritage-spring-jewelry-sale"},
 {"title":"ICA Plus — International Colored Gemstone Association","url":"https://www.gemstone.org/events/ica-plus"},
 {"title":"From Prism Volume II 2026: Welcome to the Color Show — AGTA","url":"https://agta.org/from-prism-volume-ii-2026-welcome-to-the-color-show/"},
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

specs["one-billion-for-de-beers"] = {
 **strip("By the numbers · the De Beers price",[
   {"fig":"$1B","lab":"reported total"},
   {"fig":"$750M","lab":"paid on closing"},
   {"fig":"$250M","lab":"deferred"},
   {"fig":"$500M","dir":"up","lab":"working capital in"},
   {"fig":"$2.3B","lab":"book value, earlier 2026"}]),
 "figs":[bars("Plate I","What De Beers has been worth",[
   {"l":"2001 TAKE-PRIVATE","v":17600,"d":"$17.6B"},
   {"l":"BOOK, EARLY 2026","v":2300,"d":"$2.3B"},
   {"l":"REPORTED PRICE","v":1000,"d":"$1.0B","hi":True}],
   "USD. Take-private valuation vs. carrying value vs. reported bid.",141)],
 "flow":flow5("A number, at last.","Producing into the trough.","Three governments at one table.",
   "A price of $1 billion is therefore not a discount to a peak so much as an admission that the peak belonged to a different industry.","The Diamonds Desk",
   "Anglo picks the Penny group","a-de-beers-sale-gets-a-clock.html"),
 "desk":{"split":"The number that matters is not the $1 billion but the $500 million going in behind it, because the price of the asset is now smaller than the cost of carrying it through another soft year."},
 "next":nxt("de-beers-eighty-eight-up","The quarter","De Beers digs 88% more and banks 44% less.",
   "gaborone-answers-penny","Botswana","angolas-rough-clears","Rough")}

specs["angolas-rough-clears"] = {
 **strip("By the numbers · Luanda",[
   {"fig":"95%","dir":"up","lab":"TAGS sell-through"},
   {"fig":"10.8ct+","lab":"goods on offer"},
   {"fig":"$21.7M","lab":"Sodiam 17th auction"},
   {"fig":"6,586.89ct","lab":"carats sold"},
   {"fig":"+23.46%","dir":"up","lab":"above expected value"}]),
 "figs":[bars("Plate I","Average price per carat, by seller",[
   {"l":"GEM DIAMONDS (LETSENG)","v":1501,"d":"$1,501","hi":True},
   {"l":"DE BEERS Q2","v":105,"d":"$105"}],
   "USD per carat. Large-stone producers vs. the mainstream rough book.",142)],
 "flow":flow5("Ninety-five out of a hundred.","Size, not geography.","Both sides of the table.",
   "An auction that lands nearly a quarter above the reserve book is not the behaviour of a market in retreat.","The Rough Desk",
   "Petra caves at the bottom","a-petra-caves-at-the-bottom.html"),
 "desk":{"split":"the scarcity premium is real above ten carats and still absent below one"},
 "next":nxt("one-billion-for-de-beers","The sale","Anglo's price for De Beers comes in at about $1 billion.",
   "gem-diamonds-rides-the-big-ones","Large stones","angola-bids-for-the-house","Angola")}

specs["gold-unwinds-the-hold"] = {
 **strip("By the numbers · gold after the Fed",[
   {"fig":"$4,074.98","dir":"up","lab":"spot, Thursday"},
   {"fig":"+0.22%","dir":"up","lab":"on the day"},
   {"fig":"+23.84%","dir":"up","lab":"year on year"},
   {"fig":"$57.79","dir":"down","lab":"silver / oz"},
   {"fig":"70.37","lab":"gold-silver ratio"}]),
 "figs":[bars("Plate I","Three days around the decision",[
   {"l":"THU 30 JUL","v":4075,"d":"$4,075","hi":True},
   {"l":"TUE 28 JUL","v":4046,"d":"$4,046"},
   {"l":"WED 29 JUL (CLOSE)","v":4029,"d":"$4,029"}],
   "USD/oz spot. The FOMC held at 3.50–3.75% on 29 July.",143)],
 "flow":flow5("Undone in a session.","Silver stays behind.","The tag, not the screen.",
   "Official buying is indifferent to a quarter-point, which is why every dip since spring has found a floor before it found a seller of consequence.","The Bullion Desk",
   "The Fed holds, gold exhales","a-fed-holds-gold-exhales.html"),
 "desk":{"split":"the trade should plan for a $4,000 handle as the operating assumption rather than the exception"},
 "next":nxt("platinum-loses-its-teacher","White metals","Platinum jumps to $1,628 as PGI's US educator retires.",
   "fed-holds-gold-exhales","The decision","india-gold-signals-mixed","Demand")}

specs["platinum-loses-its-teacher"] = {
 **strip("By the numbers · platinum",[
   {"fig":"$1,628.20","dir":"up","lab":"platinum / oz"},
   {"fig":"+1.62%","dir":"up","lab":"on the day"},
   {"fig":"+26.13%","dir":"up","lab":"year on year"},
   {"fig":"−6%","dir":"down","lab":"2026 jewellery demand"},
   {"fig":"39 yrs","lab":"Reilly in the trade"}]),
 "figs":[bars("Plate I","The metal and the counter",[
   {"l":"PLATINUM, Y/Y","v":26,"d":"+26.13%","hi":True},
   {"l":"PALLADIUM, Y/Y","v":7,"d":"+6.64%"},
   {"l":"PT JEWELLERY DEMAND, 2026F","v":-6,"d":"−6%"}],
   "Percent change. Metal price vs. forecast jewellery offtake.",144)],
 "flow":flow5("A good day, a bad forecast.","The bench nobody sees.","Forty-eight parades.",
   "That is the awkward shape of this market: a metal whose investment and industrial case keeps strengthening while the counter that carries its name sells less of it.","The Metals Desk",
   "Platinum, short a fourth year","a-platinum-short-a-fourth-year.html"),
 "desk":{"split":"The opportunity is the discount to gold, which at these levels buys a bridal ring in a rarer metal for less money per gram of finished weight."},
 "next":nxt("gold-unwinds-the-hold","Gold","Gold takes back $4,075 the morning after the hold.",
   "white-metals-lose-their-heat","Reversal","platinum-short-a-fourth-year","Deficit")}

specs["four-groups-in-the-black"] = {
 **strip("By the numbers · Swiss resale, Q2",[
   {"fig":"+1.5%","dir":"up","lab":"Morgan Stanley index"},
   {"fig":"+5.4%","dir":"up","lab":"Swatch Group, y/y"},
   {"fig":"+4.2%","dir":"up","lab":"Richemont, y/y"},
   {"fig":"+2.5%","dir":"up","lab":"April, best since Mar 2022"},
   {"fig":"4 of 4","lab":"groups positive y/y"}]),
 "figs":[bars("Plate I","Secondary prices, year on year",[
   {"l":"SWATCH GROUP","v":5.4,"d":"+5.4%","hi":True},
   {"l":"RICHEMONT","v":4.2,"d":"+4.2%"},
   {"l":"MS INDEX, Q2 Q/Q","v":1.5,"d":"+1.5%"}],
   "Percent change. Morgan Stanley Q2 2026 Swiss watch report.",145)],
 "flow":flow5("Three years, undone.","April did the lifting.","Why a floor matters.",
   "After three years in which the resale tape only told bad news, the bad news has stopped.","The Movement Desk",
   "Plus 11.2% in June","a-plus-eleven-two-in-june.html"),
 "desk":{"split":"The direction of the secondary market has flipped from headwind to mild tailwind, and that changes the arithmetic on every trade-in, every financing conversation and every pre-owned case in the window."},
 "next":nxt("plus-eleven-two-in-june","Exports","Swiss exports rise 11.2% in June.",
   "cartier-secondhand-heat","Resale","list-up-resale-down","Spread")}

specs["heritage-books-a-record-half"] = {
 **strip("By the numbers · Heritage H1",[
   {"fig":"$1.41B","dir":"up","lab":"first-half sales"},
   {"fig":"+47%","dir":"up","lab":"year on year"},
   {"fig":"$9,713,640","lab":"May 4 jewelry sale"},
   {"fig":"$906,250","lab":"6.59ct Kashmir sapphire"},
   {"fig":"50 yrs","lab":"highest midyear ever"}]),
 "figs":[bars("Plate I","Heritage's jewelry record",[
   {"l":"MAY 2026 SIGNATURE","v":9.71,"d":"$9.71M","hi":True},
   {"l":"SEPT 2025 (PREVIOUS)","v":9.2,"d":"$9.2M"}],
   "USD millions. Highest-grossing jewelry auctions in the firm's history.",146)],
 "flow":flow5("A record from Dallas.","One stone, 9% of the room.","Comparables, not trophies.",
   "One stone accounted for roughly 9% of the sale, which is the shape of every strong jewelry auction this year.","The Saleroom Desk",
   "Trophy lots carry the half","a-trophy-lots-carry-the-half.html"),
 "desk":{"split":"The house that learns to write a condition report like an auction cataloguer will win those clients; the one still selling on carat weight alone will not."},
 "next":nxt("color-runs-two-speeds","Color","The sapphire that beat its estimate by $300,000.",
   "trophy-lots-carry-the-half","The half","three-fancies-no-reserve","No reserve")}

specs["the-storefront-that-isnt"] = {
 **strip("By the numbers · the fake shop",[
   {"fig":"80–90%","lab":"advertised discount"},
   {"fig":"33 yrs","lab":"fabricated trading history"},
   {"fig":"£100s","lab":"reported losses per buyer"},
   {"fig":"4+","lab":"named storefronts"},
   {"fig":"$0","lab":"cost of a synthetic founder"}]),
 "figs":[bars("Plate I","The template, in four sites",[
   {"l":"MAYA AND HENRY","v":90,"d":"up to 90% off","hi":True},
   {"l":"C'EST LA VIE","v":80,"d":"80% off"},
   {"l":"AISHA JEWELRY","v":80,"d":"up to 80% off"},
   {"l":"SEREN CARDIFF","v":0,"d":"goods never sent"}],
   "Advertised discount on fabricated closing-down sales.",147)],
 "flow":flow5("A retailer with no bench.","The template.","Two bills for real jewellers.",
   "What has changed is the cost of looking legitimate.","The Counter Desk",
   "Guess lets the machine draw","a-guess-lets-the-machine-draw.html"),
 "desk":{"split":"The retailer's job now is to make the boring evidence of being real as visible as the discount."},
 "next":nxt("heritage-books-a-record-half","Salerooms","Heritage books $1.41 billion and a jewelry record.",
   "vietnam-certificate-scandal","Paper","guess-lets-the-machine-draw","AI")}

specs["color-runs-two-speeds"] = {
 **strip("By the numbers · colored stones",[
   {"fig":"$906,250","lab":"6.59ct Kashmir sapphire"},
   {"fig":"−30%","dir":"down","lab":"demand vs. 2022"},
   {"fig":"+150%","dir":"up","lab":"Mahenge spinel, since 2020"},
   {"fig":"$10–12k","lab":"Paraiba per carat"},
   {"fig":"−15–20%","dir":"down","lab":"tsavorite, 12 months"}]),
 "figs":[bars("Plate I","Since the pandemic, by stone",[
   {"l":"MAHENGE SPINEL","v":150,"d":"+150%","hi":True},
   {"l":"BLUE SAPPHIRE 3ct+","v":50,"d":"+50%"},
   {"l":"ZAMBIAN EMERALD","v":28,"d":"+25–30%"},
   {"l":"COLOMBIAN EMERALD","v":20,"d":"+20% (FX)"},
   {"l":"TSAVORITE, LAST 12M","v":-18,"d":"−15–20%"}],
   "Percent change. Rapaport trade survey, January 2026.",148)],
 "flow":flow5("Two numbers, opposite ways.","A size and quality gap.","Bridal says otherwise.",
   "The gap is a size and quality gap, not a confusion.","The Color Desk",
   "The guide marks ruby up","a-the-guide-marks-ruby-up.html"),
 "desk":{"split":"that argues for buying fewer stones with better reports rather than more stones at better prices, and for treating the lab document as the product"},
 "next":nxt("heritage-books-a-record-half","Salerooms","The room where the Kashmir sapphire cleared $906,250.",
   "the-guide-marks-ruby-up","Ruby","emeralds-hold-at-146","Emerald")}

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
    if len(set(sp["strip"]["cells"].__len__() for _ in [0]))!=1: pass
    # house style checks
    joined=" ".join(body)+" "+d["title"]+" "+d["dek"]
    if "!" in joined: errs.append(f"{s}: exclamation mark")
    if joined.count("—") > 1: errs.append(f"{s}: {joined.count(chr(8212))} em-dashes (max 1)")
    for w in ["insane","stunning","shocking","incredible","unbelievable"]:
        if w in joined.lower(): errs.append(f"{s}: hype word '{w}'")
    if len(d["dek"].split()) > 40: errs.append(f"{s}: dek {len(d['dek'].split())} words > 40")
    wc=len(" ".join(body).split())
    if not (330 <= wc <= 620): errs.append(f"{s}: body {wc} words outside 330-620")
if errs:
    print("SPEC ERRORS:"); [print(" -",e) for e in errs]; sys.exit(1)

# ---------------- PREPEND + write ----------------
articles = NEW + articles
leads=[a["slug"] for a in articles if a.get("lead")]
assert leads==["one-billion-for-de-beers"], f"lead set wrong: {leads}"
for s in specs: editorial[s]=specs[s]

(C/"articles.json").write_text(json.dumps(articles,ensure_ascii=False,indent=1))
(C/"editorial.json").write_text(json.dumps(editorial,ensure_ascii=False,indent=1))
print("articles now:",len(articles)," specs now:",len(editorial)," lead:",leads)
for d in NEW: print("  ",d["desk"].ljust(12), str(len(" ".join(d["body"]).split())).rjust(4),"w  ",d["slug"])
print("OK")
