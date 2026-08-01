#!/usr/bin/env python3
# Edition No. 022 - 2026-08-01. Prepends 8 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-01"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - russia-bans-the-word ==========
art("russia-bans-the-word","diamonds",True,"Lead Story · Diamonds Desk",5,"The Diamonds Desk",
["ACTOR","STAKES","VS"],
"Russia bans the word: synthetics lose diamond, carat and natural",
"Government Resolution No. 657 of May 30 takes effect on September 1. Tags must say synthetic, weight must be shown in grams rather than carats, and precious, natural, real and eco-friendly are struck from the vocabulary.",
[
"Russia has given the synthetic stone trade thirty-one days to rewrite its labels. Government Resolution No. 657, signed on May 30 and effective September 1, prohibits the word diamond and all its derivatives in any consumer-facing description of man-made material sold in Russia. The tag must instead carry the word synthetic, or the abbreviation Synth., and the approved full term is cut synthetic diamond. The rule covers physical tags, showcase cards and online listings alike, so a Russian retailer cannot describe on a website what it may not print in a store.",
"The banned vocabulary runs well past the noun. Precious, real, genuine, natural, mined, mineral and eco-friendly are struck, along with similar expressions and their derivatives, from every piece of information a buyer sees. The colour and clarity descriptors borrowed from natural grading go with them. What remains is a product that may be sold, may be set in gold, and may not be marketed with any of the language that has carried it for a decade. The finance ministry has not restricted supply. It has restricted the sentence.",
"The weight rule is the sharpest instrument in the document. Synthetic stones must be described in grams, and carat weight is prohibited outright. A one-carat lab-grown stone sold in Russia after September 1 is a 0.2 gram stone. Every reference point a shopper uses to compare a grown stone against a mined one, and every marketing claim built on carats per dollar, dies with that substitution. Alongside it sits a full tagging schedule: product name, maker or importer, country of origin, model number, total weight, metal and fineness, stone particulars, and a unique identification number matching a two-dimensional barcode. Alexey Moiseev, the deputy finance minister, said the aim is to \"improve transparency in the jewelry display and protect consumers\".",
"Russia is not acting alone, and it is not acting on a large market. CIBJO is expected to strike laboratory-grown and laboratory-created from its Blue Book at a congress on September 4 and mandate the single word synthetic, and India, the African producers and the GIA have all moved the same way this year. Russia's contribution is that it wrote the rules down and attached a date. The ministry's own framing notes wholesale synthetic prices below $70 for 0.2 grams in some categories, which is the commercial fact the language rules are built around. A product at that price does not need a defence in Moscow. It needs one wherever the natural trade still competes for the same shopper.",
"The desk's view: the adjectives were always going to go. Eco-friendly and precious were marketing borrowed against a definition, and every regulator that has looked at them has taken them back. What matters here is that the carat rule is the one that travels, because a unit of measure is harder to lobby away than an adjective, and because a trade that cannot quote carats cannot run a price list. Any grower selling into a market with a Russian-style rulebook has to rebuild its catalogue, its comparison charts and its e-commerce filters around grams. The trade should read September 1 as a rehearsal, not an outlier."
],
[
 {"title":"Russian Government Approves New Guidelines to Inform Jewelry Buyers — Alrosa","url":"https://www.alrosa.ru/en/media/news/2026/russian-government-approves-new-guidelines-to-inform-jewelry-buyers-only-natural-stones-can-be-calle/"},
 {"title":"Russian Govt. Announces New Regulations for Lab-Grown Jewelry — Rapaport","url":"https://rapaport.com/news/russian-govt-announces-new-regulations-for-lab-grown-jewelry/"},
 {"title":"Russia Tightens Rules on Synthetic Diamond Labelling — Solitaire (GJEPC)","url":"https://gjepc.org/solitaire/russia-tightens-rules-on-synthetic-diamond-labelling/"},
 {"title":"Russia adopts new resolution on labelling and sale of synthetic diamonds — The Retail Jeweller India","url":"https://retailjewellerindia.com/russia-adopts-new-resolution-on-labelling-and-sale-of-synthetic-diamonds-in-jewellery/"},
])

# ========== 2. dubai-diamond-week-returns ==========
art("dubai-diamond-week-returns","diamonds",False,"Diamonds Desk · Dubai",4,"The Diamonds Desk",
["ACTOR","NUM"],
"Dubai sets a second Diamond Week for October 26",
"DMCC will run the second Dubai Diamond Week from October 26 to 29, with the Italian Exhibition Group co-hosting a sourcing show. The emirate traded a record $41.7 billion and 359.5 million carats last year.",
[
"Dubai has put a date on its second attempt to become the room the diamond trade meets in. DMCC will hold Dubai Diamond Week from October 26 to 29, four days of conference sessions alongside a sourcing exhibition co-hosted with the Italian Exhibition Group. The first edition ran last year. The second arrives with a stronger set of numbers behind it and a weaker market in front of it, which is the combination that decides whether a trade fair becomes a fixture.",
"The numbers are the argument. Dubai's rough and polished trade reached $41.7 billion and 359.5 million carats in 2025, the highest on record, with natural stones accounting for 95.8% of the value. The Dubai Diamond Exchange now anchors an ecosystem of close to 1,400 companies and operates the largest tender facility in the business. A city that clears that volume does not need a conference to prove it matters, but it does need one to convert throughput into governance.",
"That is the harder part of the pitch. Antwerp, Ramat Gan and Mumbai were built on long-standing bourse membership, arbitration and credit, not on tonnage alone. Dubai has spent the past year buying the missing pieces: the 41st World Diamond Congress met there in July, Okavango Diamond Company signed a tender arrangement with the exchange, and Qatar's new bourse joined the World Federation of Diamond Bourses. October's programme is the follow-through, with governments, producers, manufacturers, retailers and technology firms all on the invitation list.",
"The timing is uncomfortable and probably deliberate. October lands after the summer trough and before the festive restock, at the point in the calendar when sightholders decide how much rough they will fund into the new year. De Beers' rough index has sat flat at 68 and 69 across two quarters, Angolan tenders have cleared above expectation, and nobody in the room will be short of an opinion on where the floor is. A trade fair held while prices are still finding their level produces better conversation than one held in a boom.",
"The desk's view: the useful measure of Dubai Diamond Week will not be attendance. It will be whether any binding trade infrastructure comes out of it, because a conference that convenes the industry without producing arbitration, credit terms or a tender calendar is a very expensive networking event. Dubai has the volume, the exchange and now the diary slot. What it has not yet demonstrated is that a producer in Gaborone or a manufacturer in Surat changes a commercial decision because of something agreed in the emirate rather than merely announced there."
],
[
 {"title":"DMCC to Host Second Edition of Dubai Diamond Week This October — DMCC","url":"https://dmcc.ae/latest-news/dmcc-to-host-second-edition-of-dubai-diamond-week-this-october-as-global-diamond-industry-convenes-in-dubai"},
 {"title":"US$41.7 Billion Trade Milestone Powers Dubai Diamond Week — Solitaire (GJEPC)","url":"https://gjepc.org/solitaire/us41-7-billion-trade-milestone-powers-dubai-diamond-week/"},
 {"title":"Dubai Diamond Week 2026 announced after record $41.7bn trade milestone — Arabian Business","url":"https://www.arabianbusiness.com/business/dubai-diamond-week-2026"},
 {"title":"Dubai Diamond Week Returns Oct. 26-29 With Diamond Conference and JGTD Sourcing Exhibition — InStore","url":"https://instoremag.com/dubai-diamond-week-returns-oct-26-29-with-diamond-conference-and-jgtd-sourcing-exhibition/"},
])

# ========== 3. gold-ends-july-higher ==========
art("gold-ends-july-higher","gold-metals",False,"Gold & Metals Desk · New York",4,"The Bullion Desk",
["NUM","RECORD"],
"$4,041.70: gold's first monthly gain since February",
"Kitco's Friday close puts gold at $4,041.70, down $60.90 or 1.48% on the day. July still finished about 0.5% higher, ending a four-month losing run, as the dollar rebounded from a six-week low.",
[
"Gold lost the day and won the month. Kitco's Friday close, timed at 5pm New York, put spot at $4,041.70 an ounce, down $60.90 or 1.48%, the weakest session of the week. Across July as a whole the metal still finished roughly 0.5% higher, its first monthly gain since February and the end of a four-month losing run. Trading Economics puts gold 20.22% above where it stood a year ago. Markets are shut until Monday, so this is the number the trade opens August against.",
"Friday's fall had a single cause. The dollar rebounded from a six-week low, and traders unwound the rally that followed the Federal Reserve's decision to hold rates, a decision that had carried gold above $4,100 on Thursday. Softer inflation data and an unchanged policy rate should have been supportive. They were outweighed by expectations that the Fed's next move is more likely to tighten than to ease, and by the ordinary mechanics of a crowded position being closed before a weekend.",
"This desk carried a higher figure yesterday. An intraday print put July's gain at about 1.4%, and Friday's close revises that down to roughly half a percent. The correction matters less for its size than for its source: reference-point drift between morning quotes and settlement prices has produced three inconsistencies in this tape in two weeks. From today the tape carries the Kitco 5pm New York close and nothing else, so a day change here means a change against the previous settlement rather than against whichever intraday snapshot happened to be visible.",
"For the bench the month is the only number worth planning against. Gold spent July absorbing a Fed hold, a war premium and a dollar bounce, and finished higher regardless. At $4,041.70 an ounce fine metal costs about $130 a gram before refining, alloy, loss or making charge. A retailer still quoting from a January card is short roughly a fifth of its metal cost, and a customer funding a new piece with old chain is working the same arithmetic from the other side of the counter.",
"The desk's view: five months of falling prices ended without a catalyst, which is the most informative thing about them. Nothing was announced in July that gold did not already know, and the metal rose anyway, which says the marginal buyer is no longer waiting for a reason. The practical instruction is unchanged and now better evidenced: price inventory, insurance and trade-in policy off a $4,000 handle, because a metal that will not break down on bad news is not a metal that is waiting to fall. Anyone budgeting for a return to $3,500 has now had five months to be right and was not."
],
[
 {"title":"Gold Spot Prices — Kitco (July 31, 2026 close)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Gold slips as US dollar regains footing; heads for first monthly gain in five — Kitco News","url":"https://www.kitco.com/news/off-the-wire/2026-07-31/gold-slips-us-dollar-regains-footing-heads-first-monthly-gain-five"},
 {"title":"Gold retreats but poised to end best month since February — CNBC","url":"https://www.cnbc.com/2026/07/31/gold-slips-but-on-track-to-end-four-month-losing-streak.html"},
 {"title":"Gold — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/gold"},
])

# ========== 4. white-metals-close-the-month ==========
art("white-metals-close-the-month","gold-metals",False,"Gold & Metals Desk · New York",4,"The Metals Desk",
["NUM","VS"],
"$1,256 palladium: the white metals give the month back",
"Kitco's Friday close puts palladium at $1,256, down 3.38%, silver at $57.44, down 2.45%, and platinum at $1,644, down 0.60%. The gold-silver ratio widened to about 70.4.",
[
"The white metals took Friday harder than gold did. Kitco's 5pm close put palladium at $1,256.00, down $44.00 or 3.38%, silver at $57.44, down $1.445 or 2.45%, and platinum at $1,644.00, down $10.00 or 0.60%. Three metals with three unrelated demand stories fell together on the same afternoon, which is almost always a currency event rather than a supply one. The dollar rebounded, and everything priced in it went the other way.",
"Silver's failure is the one the counter will feel. The metal spent July working at $60 and did not clear it, and at $57.44 against gold at $4,041.70 the ratio sits near 70.4, wider than it has been for most of the past month. Silver has run ahead of gold all year and has now stalled just under a round number, which is precisely the level at which a silver programme is either rebuilt in lighter gauge or repriced outright. A house that has done neither is absorbing the difference in its own margin.",
"Where the month ended for silver and platinum is genuinely unsettled, and this desk is not going to pretend otherwise. One data provider shows silver down about 2.5% over the month and platinum up about 3.5%. Wire reports from the same session had both metals heading for a monthly gain. The two readings cannot both be right, and neither can be reconciled without a settlement series this desk can verify. So today's entry carries the day move from a single source at a single print time and leaves the month blank until it can be checked.",
"Platinum's relative calm is worth noting inside a bad session. A 0.60% fall against palladium's 3.38% separates a metal with a forecast fourth consecutive supply deficit from one exposed to a vehicle fleet electrifying underneath it. At $1,644 platinum trades at roughly 41% of the gold price, so a bridal ring in the scarcer, denser metal still costs less in raw material than the same ring in gold. That gap has been open for a year and the trade has not taken it, because the constraint was never the metal price. Fewer benches can set platinum, and a house that cannot set it will not quote it.",
"The desk's view: one down session across three metals is a dollar story and should change nobody's inventory plan. The number that should change behaviour is the ratio near 70.4, because a ratio that widens while silver sits under $60 is telling silver houses that their input cost has stopped rising without falling either. That is the moment to reprice, not the moment to wait. The other lesson is procedural: a tape that quotes three metals from three different snapshots is worse than useless, and this edition fixes it."
],
[
 {"title":"Silver, Platinum and Palladium Spot Prices — Kitco (July 31, 2026 close)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Silver — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/silver"},
 {"title":"Platinum — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/platinum"},
 {"title":"Gold falls but posts its strongest monthly performance since February — Economies.com","url":"https://www.economies.com/commodities/gold-news/gold-falls-but-posts-its-strongest-monthly-performance-since-february-49403"},
])

# ========== 5. hermes-watches-flat ==========
art("hermes-watches-flat","watches",False,"Watches Desk · Paris",4,"The Watch Desk",
["ACTOR","NUM","VS"],
"Hermès sells €269 million of watches and calls it stable",
"First-half watch revenue fell 4.2% as published and rose 0.2% at constant rates. The second quarter grew 4.4%. Jewellery and home together took €1.065 billion, up 5.4%, on a group margin of 41%.",
[
"Hermès reported a first half in which its watch division did almost exactly nothing, and that counts as a result. Watch revenue was €269 million, down 4.2% as published and up 0.2% at constant exchange rates, meaning the entire decline was currency. The second quarter was better: €134 million, up 3.0% published and 4.4% at constant rates, with the house crediting its established collections, Cape Cod among them. For a division that competes against Swiss houses still working through inventory, flat is the shape of a soft landing.",
"The jewellery side did the growing. Other Hermès sectors, the line that carries jewellery and home, took €1.065 billion in the half, up 0.8% published and 5.4% at constant rates, with the second quarter up 4.0% on the same basis. That segment is now roughly four times the size of watches at Hermès and is growing where watches are holding. It is the same split visible at Kering, where the jewellery houses grew 20% on a comparable basis while the group as a whole barely moved.",
"The group figures give the divisional numbers their weight. Revenue was €8.2 billion for the half, up 6.1% at constant rates and 1.6% as published, with recurring operating income of €3.4 billion and a margin of 41.0%. Net profit was €2.2 billion. Very few businesses in any industry hold a forty-one percent operating margin through a luxury slowdown, and none of the groups Hermès is usually compared against did so this half.",
"Geography explains more than product does. The Americas grew 15.3% at constant rates and Japan 11.0%, while Europe excluding France added 8.8% and the Middle East fell 4.2%. American strength through a tariff round is the surprise in that table, and it lines up with US jewellery sales running roughly 9% ahead in the first half on stronger high-ticket demand. Axel Dumas, executive chairman, said the performance reflects the desirability of the group's sixteen métiers and expressed confidence in the second half.",
"The desk's view: read the watch line as a control experiment. Hermès makes watches without the secondary-market dependency that governs Rolex, Patek and Audemars Piguet, sells them through its own doors, and produced a flat half in a market where flat is respectable. What that isolates is the difference between a watch business and a watch investment market, because a house whose watches were never bought as an asset does not have to wait for resale prices to recover before it can sell the next one. The rest of the trade is still waiting."
],
[
 {"title":"Hermès International: 2026 Half-year Results — GlobeNewswire","url":"https://www.globenewswire.com/news-release/2026/07/29/3334976/0/en/herm%C3%A8s-international-2026-half-year-results.html"},
 {"title":"Hermès H1 2026 revenue rises 2% to €8.16bn — Retail Insight Network","url":"https://www.retail-insight-network.com/news/hermes-h1-2026-revenue-rises-8-16/"},
 {"title":"Hermès: H1 2026 Revenue Reaches €8.2 Billion As Operating Margin Holds At 41% — Pulse 2","url":"https://pulse2.com/hermes-h1-2026-revenue-reaches-e8-2-billion-as-operating-margin-holds-at-41/"},
 {"title":"US Jewelry Sales Grow 9% in H1 2026 — Tenoris","url":"https://www.tenoris.bi/us-jewelry-sales-continue-to-grow-in-h1-2026/"},
])

# ========== 6. bucherer-gets-fifth-avenue ==========
art("bucherer-gets-fifth-avenue","watches",False,"Watches Desk · New York",4,"The Watch Desk",
["ACTOR","NUM","RECORD"],
"Bucherer will run Rolex's Fifth Avenue flagship",
"The Swiss retailer, bought by Rolex in 2023, confirmed it will operate the four-floor Fifth Avenue store. WatchPro puts it at 43,000 square feet, more than four times the current largest Rolex showroom, opening around the turn of the year.",
[
"The largest Rolex showroom in the world will be run by Rolex's own retailer. Bucherer, which the brand bought in 2023, has confirmed it will operate the Fifth Avenue flagship in Manhattan, a store WatchPro reports at 43,000 square feet across four floors. That is more than four times the size of the current record holder in Dubai. Rolex's chief executive has said the building opens at the end of 2026; Bucherer's confirmation points to the turn of the year or early 2027.",
"The building is not a fit-out. It is a David Chipperfield tower on Fifth Avenue, designed to be among the most environmentally efficient new-build offices in New York, with the showroom occupying its base. Rolex has spent three years converting American retail from a network of authorised dealers into something closer to a controlled estate, opening Bucherer-operated boutiques at pace and confirming four more US Rolex showrooms alongside this one. Fifth Avenue is where that programme becomes visible to people who do not follow the trade.",
"The commercial logic runs through the certified pre-owned business. Rolex CPO turned over about $186 million in the second quarter, up 67% year on year, against total secondhand Rolex sales across all sellers of just under $6 billion. A single very large door that can hold new and certified pre-owned inventory under one roof, with the brand controlling both price lists, is the most efficient instrument anyone has yet built for taking share of that secondary market back from the platforms.",
"The scale invites an obvious question about demand. Swiss exports rose 11.2% in June but fell 0.7% in value across the first half, and the secondary market has only just returned all four tracked Swiss groups to positive territory year on year. Committing 43,000 square feet in the most expensive retail corridor in America against that backdrop is a statement about the next decade rather than the next quarter, which is roughly how Rolex has always made these decisions.",
"The desk's view: the square footage is the story only if you think this is a shop. It is closer to a distribution decision, because the store that controls both the waiting list and the certified pre-owned counter controls the price of every Rolex in the city. Independent dealers on Forty-seventh Street and the resale platforms have spent three years watching that structure assemble itself, and this is the piece that completes it. The relevant number is not 43,000 square feet. It is how much of that $6 billion secondary market moves inside the brand's own walls."
],
[
 {"title":"Bucherer Confirms It Will Be Running Rolex USA Flagship — WatchPro","url":"https://www.watchpro.com/bucherer-confirms-it-will-run-rolex-usa-flagship/"},
 {"title":"Bucherer to Operate World's Largest Rolex Showroom on New York's Fifth Avenue — The Centurion","url":"https://news.centurionjewelry.com/articles/detail/bucherer-to-operate-worlds-largest-rolex-showroom-on-new-yorks-fifth-avenue"},
 {"title":"Rolex CEO reveals Manhattan flagship will open at the end of 2026 — WatchPro USA","url":"https://usa.watchpro.com/rolex-ceo-reveals-manhattan-flagship-will-open-at-the-end-of-2026/"},
 {"title":"July 31 Aurea Informatio: Your Friday Web Roundup — JCK","url":"https://www.jckonline.com/editorial-article/july-31-aurea-informatio/"},
])

# ========== 7. sixty-stores-for-friendship-day ==========
art("sixty-stores-for-friendship-day","retail-tech",False,"Retail & Tech Desk · Mumbai",4,"The Counter Desk",
["ACTOR","NUM","GAP"],
"De Beers takes Friendship Day into 60 Indian stores",
"The second edition of Love, from Bestie runs August 1 and 2 across 60 retail partners in nine cities, built on four paired natural diamond bracelets, one spelling BFF in Morse code.",
[
"De Beers is spending this weekend trying to sell diamonds to people who are not in love. Its India arm has launched the second edition of Love, from Bestie, an experiential campaign running today and tomorrow across 60 retail partner stores in nine cities, Forevermark outlets among them. Mumbai, Delhi, Bengaluru, Chennai, Pune, Kanpur, Kochi, Coimbatore and Nagpur are on the list. The occasion is Friendship Day, which in India falls on the first Sunday of August.",
"The product is designed around the premise. Four natural diamond bracelet designs are made to be worn in pairs, including a signature piece that spells BFF in Morse code using baguette and round stones, and interlocking and split-circle motifs. Buying one is buying two, which is the whole commercial idea. The in-store programme runs to three stations: nail art, a bag charm each duo makes for the other, and a photograph with a signed Bestie Contract.",
"The reason this is more than a promotion is arithmetic. Indian jewellery demand fell 15% by weight in the second quarter, to 75.1 tonnes from 88.8 tonnes, while the value of that demand rose about 50% on record gold prices. A counter selling fewer, dearer pieces needs occasions, and the Indian calendar's diamond occasions are overwhelmingly bridal. Friendship Day is an attempt to manufacture a second one at a lower ticket, in the gap between the summer trough and the festive build into Dhanteras.",
"It also puts the natural category in front of the buyer most exposed to the alternative. Young Indian consumers are the group that lab-grown marketing has moved fastest, and a bracelet bought for a friend is exactly the discretionary, non-bridal purchase where a grown stone's price argument works best. De Beers is answering with rarity rather than price, running a second edition of a campaign in the same week that Russia moved to strip synthetic stones of the word diamond entirely.",
"The desk's view: a two-day campaign in 60 doors is small, and the number that matters is whether it runs again in a third year. Category marketing works by repetition, not by novelty, and the diamond trade's long problem in India is that it owns one occasion and rents the rest. A second edition means last year's version cleared enough stock to justify the spend, which is more evidence than most campaigns in this trade ever produce. What nobody has published is a sell-through figure, and until someone does, this remains a good idea with no scoreboard."
],
[
 {"title":"De Beers India launches Friendship Day 'Love, from Bestie' campaign across 60 retail partner stores — The Retail Jeweller India","url":"https://retailjewellerindia.com/de-beers-india-launches-friendship-day-love-from-bestie-campaign-across-60-retail-partner-stores/"},
 {"title":"De Beers India launches 'Love, from Bestie' Campaign to celebrate Friendship Day — Medianews4u","url":"https://www.medianews4u.com/de-beers-india-launches-love-from-bestie-campaign-to-celebrate-friendship-day-with-natural-diamond-collection/"},
 {"title":"Some Friendships are as Rare as Natural Diamonds — Business Standard (ANI)","url":"https://www.business-standard.com/content/press-releases-ani/some-friendships-are-as-rare-as-natural-diamonds-de-beers-celebrates-friendship-day-with-love-from-bestie-campaign-126072800698_1.html"},
 {"title":"July 31 Aurea Informatio: Your Friday Web Roundup — JCK","url":"https://www.jckonline.com/editorial-article/july-31-aurea-informatio/"},
])

# ========== 8. dollar-battery-fifteen-dollar-job ==========
art("dollar-battery-fifteen-dollar-job","retail-tech",False,"Retail & Tech Desk · Dallas",4,"The Counter Desk",
["NUM","HOWTO"],
"A $1 battery, a $15 ticket: the counter's quietest margin",
"Sy Kessler's new battery starter kit lists from $235. The battery inside costs about $1 and the job sells for more than $15, one of the few service lines a jeweller still prices alone.",
[
"The most reliable margin in a jewellery store this year costs a dollar. Sy Kessler, the Dallas supplier, has launched a watch battery starter kit built to put battery replacement back behind the counter: an assortment of the common cells, an organiser, the tools, the consumables and the training material, with kits listing from $235. The supplier's own arithmetic is the pitch. The average watch battery costs about $1 and the job sells for more than $15. One trade publication puts the average ticket nearer $18.79.",
"That spread survives conditions almost nothing else in the store survives. Gold at $4,041.70 an ounce has compressed every margin built on metal weight, Indian jewellery tonnage fell 15% in the second quarter, and US unit sales have been falling while average tickets rise. A battery change is priced against neither a metal quote nor a competitor's website. The customer is not comparison shopping a five-minute job, which makes it one of the last lines in the store where the retailer sets the number.",
"The traffic argument is stronger than the margin argument. A battery change brings a person through the door with a reason to wait, holding a watch they own and value, at a counter displaying goods they do not. Retailers who have run the service consistently describe it as the cheapest footfall they buy, and unlike advertising it produces a customer who is already inside the store. The kit is effectively a fixed cost of about $235 against a service that pays for itself somewhere around the twentieth battery.",
"The catch is competence and liability. A pressure-tested diver or a watch under warranty is not a job for an untrained hand, and a scratched caseback or a broken gasket converts a $15 sale into a repair claim worth many multiples of it. The kits ship with training material for that reason. The trade-off is the same one that governs sizing, restringing and prong retipping: a service line only earns its margin if the store can also afford to say no to the jobs that do not belong on it.",
"The desk's view: this is a supplier press release with a real number inside it, and the real number is the ratio. A dollar of cost against fifteen or more of price is a fifteen-to-one gross line at a moment when the metal side of the same business is fighting over percentage points. Independent jewellers have spent two years being told to chase high-ticket demand, which is correct and also crowded. The overlooked instruction is that the service counter still prices on skill rather than on spot, and there is no version of $4,000 gold that changes what a battery costs."
],
[
 {"title":"Supplier News: July 30 — JCK","url":"https://www.jckonline.com/editorial-article/supplier-news-july-27/"},
 {"title":"GemOro Murata Deluxe Watch Battery Starter Kit — Sy Kessler","url":"https://www.sykessler.com/product/murata-deluxe-watch-battery-starter-kit/"},
 {"title":"SY Kessler Sales Introduces the Profitable Traffic Generator — InStore","url":"https://instoremag.com/sy-kessler-sales-introduces-the-profitable-traffic-generator/"},
 {"title":"US Jewelry Sales Grow 9% in H1 2026 — Tenoris","url":"https://www.tenoris.bi/us-jewelry-sales-continue-to-grow-in-h1-2026/"},
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

specs["russia-bans-the-word"] = {
 **strip("By the numbers · Resolution No. 657",[
   {"fig":"Sept 1","lab":"in force"},
   {"fig":"May 30","lab":"signed"},
   {"fig":"grams","lab":"weight unit allowed"},
   {"fig":"0 carats","dir":"down","lab":"permitted for synthetics"},
   {"fig":"Sept 4","lab":"CIBJO congress"}]),
 "figs":[bars("Plate I","What a synthetic stone may be called in Russia",[
   {"l":"SYNTHETIC / SYNTH.","v":100,"d":"required","hi":True},
   {"l":"DIAMOND, AND DERIVATIVES","v":0,"d":"banned"},
   {"l":"NATURAL, REAL, PRECIOUS","v":0,"d":"banned"},
   {"l":"ECO-FRIENDLY, MINED","v":0,"d":"banned"},
   {"l":"CARAT WEIGHT","v":0,"d":"banned"}],
   "Consumer-facing description rules, in force September 1, 2026.",157)],
 "flow":flow5("Thirty-one days to relabel.","Grams, not carats.","A template, not an outlier.",
   "A one-carat lab-grown stone sold in Russia after September 1 is a 0.2 gram stone.","The Diamonds Desk",
   "Not lab-grown, synthetic","a-say-synthetic-not-lab-grown.html"),
 "desk":{"split":"the carat rule is the one that travels, because a unit of measure is harder to lobby away than an adjective"},
 "next":nxt("sixty-one-percent-said-lab","Demand","Sixty-one percent of American buyers chose a grown stone.",
   "say-synthetic-not-lab-grown","Language","lab-grown-finds-its-floor","Prices")}

specs["dubai-diamond-week-returns"] = {
 **strip("By the numbers · Dubai, 2025 trade",[
   {"fig":"$41.7B","dir":"up","lab":"diamond trade, record"},
   {"fig":"359.5M ct","dir":"up","lab":"volume traded"},
   {"fig":"95.8%","lab":"of value, natural"},
   {"fig":"~1,400","lab":"companies in the ecosystem"},
   {"fig":"Oct 26-29","lab":"second edition"}]),
 "figs":[bars("Plate I","Dubai's 2025 diamond trade, by type",[
   {"l":"NATURAL","v":95.8,"d":"95.8%","hi":True},
   {"l":"ALL OTHER","v":4.2,"d":"4.2%"}],
   "Share of $41.7 billion traded value. DMCC.",158)],
 "flow":flow5("A date on the diary.","Volume is not governance.","October is the point of decision.",
   "A city that clears that volume does not need a conference to prove it matters","The Diamonds Desk",
   "Dubai's $41 billion year","a-dubai-41-billion-year.html"),
 "desk":{"split":"the useful measure of Dubai Diamond Week will not be attendance"},
 "next":nxt("doha-opens-a-diamond-door","Gulf","Qatar's new bourse joins the world federation.",
   "greenest-stones-locked-out","Trade","angolas-rough-clears","Tenders")}

specs["gold-ends-july-higher"] = {
 **strip("By the numbers · gold, July close",[
   {"fig":"$4,041.70","dir":"down","lab":"Kitco close, July 31"},
   {"fig":"−$60.90","dir":"down","lab":"on the day"},
   {"fig":"−1.48%","dir":"down","lab":"session change"},
   {"fig":"+0.5%","dir":"up","lab":"on the month"},
   {"fig":"+20.22%","dir":"up","lab":"year on year"}]),
 "figs":[bars("Plate I","Gold's monthly run, five months to July",[
   {"l":"MARCH TO JUNE","v":0,"d":"four months lower"},
   {"l":"JULY","v":0.5,"d":"+0.5%","hi":True}],
   "Percent change, month on month. First monthly gain since February.",159)],
 "flow":flow5("The day and the month.","One dollar bounce.","A correction, and a new standard.",
   "Markets are shut until Monday, so this is the number the trade opens August against.","The Bullion Desk",
   "Gold gives back $4,086","a-gold-gives-back-thursday.html"),
 "desk":{"split":"five months of falling prices ended without a catalyst, which is the most informative thing about them"},
 "next":nxt("white-metals-close-the-month","Metals","Palladium down 3.38%, silver 2.45%, platinum 0.60%.",
   "two-seventy-eight-tonnes","Demand","gold-unwinds-the-hold","The Fed")}

specs["white-metals-close-the-month"] = {
 **strip("By the numbers · Kitco close, July 31",[
   {"fig":"$57.44","dir":"down","lab":"silver, −2.45%"},
   {"fig":"$1,644.00","dir":"down","lab":"platinum, −0.60%"},
   {"fig":"$1,256.00","dir":"down","lab":"palladium, −3.38%"},
   {"fig":"70.4","lab":"gold-silver ratio"},
   {"fig":"41%","lab":"platinum as share of gold"}]),
 "figs":[bars("Plate I","Friday's session, by metal",[
   {"l":"PALLADIUM","v":3.38,"d":"−3.38%","hi":True},
   {"l":"SILVER","v":2.45,"d":"−2.45%"},
   {"l":"GOLD","v":1.48,"d":"−1.48%"},
   {"l":"PLATINUM","v":0.60,"d":"−0.60%"}],
   "Percent fall, July 31, 2026, Kitco 5pm New York close.",160)],
 "flow":flow5("All three, one direction.","Silver stalls under $60.","What we will not print.",
   "The two readings cannot both be right, and neither can be reconciled without a settlement series this desk can verify.","The Metals Desk",
   "Three metals, one direction","a-three-metals-one-direction.html"),
 "desk":{"split":"the ratio near 70.4, because a ratio that widens while silver sits under $60 is telling silver houses that their input cost has stopped rising without falling either"},
 "next":nxt("gold-ends-july-higher","Gold","Gold closes July higher for the first time since February.",
   "platinum-loses-its-teacher","Platinum","silver-eyes-sixty","Silver")}

specs["hermes-watches-flat"] = {
 **strip("By the numbers · Hermès H1 2026",[
   {"fig":"€269M","lab":"watches, first half"},
   {"fig":"+0.2%","lab":"watches, constant rates"},
   {"fig":"€1.065B","dir":"up","lab":"jewellery and home"},
   {"fig":"€8.2B","dir":"up","lab":"group revenue"},
   {"fig":"41.0%","lab":"operating margin"}]),
 "figs":[bars("Plate I","Hermès first half, by growth at constant rates",[
   {"l":"AMERICAS","v":15.3,"d":"+15.3%","hi":True},
   {"l":"JAPAN","v":11.0,"d":"+11.0%"},
   {"l":"EUROPE EX-FRANCE","v":8.8,"d":"+8.8%"},
   {"l":"JEWELLERY AND HOME","v":5.4,"d":"+5.4%"},
   {"l":"WATCHES","v":0.2,"d":"+0.2%"}],
   "Percent change year on year, first half 2026, constant exchange rates.",161)],
 "flow":flow5("Flat is a result.","Jewellery does the growing.","Geography, not product.",
   "That segment is now roughly four times the size of watches at Hermès and is growing where watches are holding.","The Watch Desk",
   "Tiffany carries LVMH","a-tiffany-carries-lvmh.html"),
 "desk":{"split":"the difference between a watch business and a watch investment market"},
 "next":nxt("four-groups-in-the-black","Resale","All four Swiss groups turn positive year on year.",
   "boucheron-carries-kering","Kering","richemont-twenty-percent-quarter","Richemont")}

specs["bucherer-gets-fifth-avenue"] = {
 **strip("By the numbers · Fifth Avenue",[
   {"fig":"43,000 sq ft","lab":"showroom, per WatchPro"},
   {"fig":"4","lab":"floors"},
   {"fig":"4×","lab":"the current largest, in Dubai"},
   {"fig":"$186M","dir":"up","lab":"Rolex CPO, Q2"},
   {"fig":"~$6B","lab":"all secondhand Rolex sales"}]),
 "figs":[bars("Plate I","Rolex's secondary market, second quarter",[
   {"l":"ALL SELLERS, ANNUAL","v":6000,"d":"~$6.0B","hi":True},
   {"l":"ROLEX CPO, QUARTER","v":186,"d":"$186M"}],
   "USD. Certified pre-owned turnover against the total secondhand market.",162)],
 "flow":flow5("The largest, run in-house.","A tower, not a fit-out.","Scale against a soft market.",
   "That is more than four times the size of the current record holder in Dubai.","The Watch Desk",
   "The crown premium shrinks","a-crown-premium-shrinks.html"),
 "desk":{"split":"the store that controls both the waiting list and the certified pre-owned counter controls the price of every Rolex in the city"},
 "next":nxt("hermes-watches-flat","Paris","Hermès holds its watch division flat at €269 million.",
   "rolex-on-the-main-corridor","Retail","the-big-three-pull-away","Resale")}

specs["sixty-stores-for-friendship-day"] = {
 **strip("By the numbers · Love, from Bestie",[
   {"fig":"60","lab":"retail partner stores"},
   {"fig":"9","lab":"cities"},
   {"fig":"2","lab":"days, August 1 and 2"},
   {"fig":"4","lab":"paired bracelet designs"},
   {"fig":"2nd","lab":"edition of the campaign"}]),
 "figs":[bars("Plate I","Indian jewellery demand, second quarter",[
   {"l":"Q2 2025","v":88.8,"d":"88.8t"},
   {"l":"Q2 2026","v":75.1,"d":"75.1t","hi":True}],
   "Tonnes. The demand backdrop the campaign is selling into.",163)],
 "flow":flow5("Two days, sixty doors.","Buying one is buying two.","An occasion, manufactured.",
   "A counter selling fewer, dearer pieces needs occasions","The Counter Desk",
   "India buys 15% less","a-india-buys-fifteen-percent-less.html"),
 "desk":{"split":"the number that matters is whether it runs again in a third year"},
 "next":nxt("russia-bans-the-word","Language","Russia strips synthetics of the word diamond.",
   "india-buys-the-dip","India","china-weighs-in-on-gold","China")}

specs["dollar-battery-fifteen-dollar-job"] = {
 **strip("By the numbers · the battery counter",[
   {"fig":"~$1","lab":"average battery cost"},
   {"fig":"$15+","dir":"up","lab":"average job price"},
   {"fig":"$18.79","lab":"one trade estimate"},
   {"fig":"$235","lab":"starter kit, from"},
   {"fig":"~20","lab":"batteries to repay the kit"}]),
 "figs":[bars("Plate I","One battery change, cost against price",[
   {"l":"PRICE TO CUSTOMER","v":15,"d":"$15+","hi":True},
   {"l":"COST OF THE CELL","v":1,"d":"~$1"}],
   "USD per job. Supplier and trade-press estimates.",164)],
 "flow":flow5("A dollar in, fifteen out.","The traffic is the point.","Where it goes wrong.",
   "The customer is not comparison shopping a five-minute job, which makes it one of the last lines in the store where the retailer sets the number.","The Counter Desk",
   "The average ticket carries the half","a-average-ticket-carries-the-half.html"),
 "desk":{"split":"the service counter still prices on skill rather than on spot"},
 "next":nxt("sixty-stores-for-friendship-day","India","De Beers takes Friendship Day into 60 stores.",
   "more-dollars-fewer-boxes","Units","richline-splits-the-till","Supply")}

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
assert leads==["russia-bans-the-word"], f"lead set wrong: {leads}"
for s in specs: editorial[s]=specs[s]

(C/"articles.json").write_text(json.dumps(articles,ensure_ascii=False,indent=1))
(C/"editorial.json").write_text(json.dumps(editorial,ensure_ascii=False,indent=1))
print("articles now:",len(articles)," specs now:",len(editorial)," lead:",leads)
for d in NEW: print("  ",d["desk"].ljust(12), str(len(" ".join(d["body"]).split())).rjust(4),"w  ",d["slug"])
print("OK")
