#!/usr/bin/env python3
# Edition No. 023 - 2026-08-02. Prepends 8 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-02"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - nobody-has-de-beers-yet ==========
art("nobody-has-de-beers-yet","diamonds",True,"Lead Story · Diamonds Desk",5,"The Diamonds Desk",
["ACTOR","STAKES","VS"],
"Nobody has De Beers yet, and there will be no listing",
"Anglo American's chief executive says the sale is in its final and hardest phase, that no bidder holds exclusivity, and that a public listing is off the table. Completion is targeted for the second half.",
[
"Anglo American has corrected the story the trade had settled on. Duncan Wanblad, the group's chief executive, said the De Beers sale is now in the final phases of a process that is also the hardest one, because it requires several parties to move at the same time. He put completion in the second half of this year, and regulatory approval roughly a year after signature. That is the first time Anglo has attached both a stage and a sequence to a disposal it announced in May 2024, and the timetable it implies runs well into 2027 before anyone new actually controls the company.",
"The more consequential sentence was about exclusivity. Wanblad said Anglo is not exclusive with any consortium and continues to hold multiple active bidders, which contradicts the reporting that the group assembled by Gareth Penny, De Beers' former chief executive, had been selected. This desk carried that framing on July 26 under the headline that Anglo had picked the Penny group and started a year-end clock. The clock was right. The pick was not, and the correction matters commercially, because a named front-runner and a live auction produce very different prices for the same asset.",
"A listing is now formally excluded. Wanblad said Anglo does not believe the market has the capacity to absorb a De Beers flotation at this point, which removes the exit route that would have given the trade a public share price and a quarterly disclosure obligation. What replaces it is a private sale to a buyer under no duty to publish anything. For sightholders deciding how much rough to fund through the winter, the difference is not abstract. A listed De Beers reports its rough index every quarter. A privately held one need not.",
"The financials the buyers are pricing were published on July 31. De Beers turned over $1.6 billion in the first half, down 19% year on year, and carried an underlying loss before interest, tax, depreciation and amortisation of $113 million, narrowed from $189 million in the first half of 2025 on cost cuts rather than on recovered demand. Against that, the figure reported in late July was a sale near $1 billion with about $750 million payable up front, for a business Anglo carried at $4.9 billion as recently as 2023. Wanblad's word for this stage was blunt: \"That also is the most challenging phase.\"",
"The desk's view: the exclusivity denial is the part to trade on, not the timetable. Anglo has every reason to say an auction is still competitive, and a seller talking up a field of bidders is the oldest position in the book, so the claim deserves scepticism. But it is now on the record from the chief executive, and it means the July reports of a chosen consortium were premature rather than merely early. The practical consequence is that the price is not set, which is why nobody should plan a 2027 supply contract against a number they read in a newspaper. Until a signed agreement is announced, De Beers has a queue, not an owner."
],
[
 {"title":"De Beers Sale in 'Final, Most Challenging' Phase, Anglo CEO Says — National Jeweler","url":"https://nationaljeweler.com/articles/15182-de-beers-sale-in-final-most-challenging-phase-anglo-ceo-says"},
 {"title":"De Beers Trims Losses Amid Price Stabilization, Cost Cuts — Rapaport","url":"https://rapaport.com/news/de-beers-trims-losses-amid-price-stabilization-cost-cuts/"},
 {"title":"Anglo American Mulling $1B De Beers Sale – Report — Rapaport","url":"https://rapaport.com/news/anglo-american-mulling-1b-de-beers-sale-report/"},
 {"title":"JCK Take 3: Is De Beers Worth Only $1 Billion? — JCK","url":"https://www.jckonline.com/editorial-article/jck-take-3-de-beers-only-1-billion/"},
])

# ========== 2. zero-for-antwerp ==========
art("zero-for-antwerp","diamonds",False,"Diamonds Desk · Tariffs",4,"The Diamonds Desk",
["VS","NUM"],
"Zero for Antwerp, and the grown stone pays anyway",
"The Section 301 tariffs that took effect on July 24 exempt loose natural diamonds cut in the European Union at 0%, along with coloured stones and natural pearls. Lab-grown diamonds received no exemption anywhere on the list.",
[
"The tariff schedule that took effect at midnight on July 24 has drawn a line the trade did not expect, and it runs between the two kinds of diamond rather than between two countries. Loose natural diamonds cut in the European Union enter the United States at 0%, exempted outright from the Section 301 duties of 10% to 12.5% now applied to roughly 60 countries on forced-labour grounds. Rough and polished coloured gemstones and natural pearls from the bloc are exempt on the same terms. Lab-grown diamonds received no exemption from any country on the list.",
"Antwerp is the direct beneficiary, and the size of the benefit is measurable. Belgium exported $2.1 billion of polished diamonds to the United States in 2024, a flow that has spent the past eleven months being repriced by three separate regimes. A 10% reciprocal duty applied from September 2025 until it was ruled unlawful in February. A 10% general import surcharge under Section 122 of the Trade Act ran from February until July 24. From July 24 the Section 301 schedule governs, and the Belgian natural stone pays nothing under it. Karen Rentmeesters, chief executive of the Antwerp World Diamond Centre, gave the reasoning: \"No diamonds are still being mined or cut in the US.\"",
"That argument is the whole mechanism, and it explains the shape of the exemption list. Section 301 protects a domestic industry, and the United States has neither a diamond mine of consequence nor a cutting trade to shelter, so a duty on polished naturals would tax American retailers to defend nothing. The same logic exempted raw and semi-manufactured gold, silver, platinum and palladium from all 60 countries. It did not exempt lab-grown stones, which the United States does manufacture, and which therefore sit on the wrong side of a test that was never written with them in mind.",
"The rest of the schedule is uneven in ways that will move goods. India, Canada, Mexico, Pakistan, Sri Lanka and the United Kingdom pay 10%. Angola, Australia, China, Colombia, Hong Kong, Israel, South Africa, Thailand, Turkey and the United Arab Emirates pay 12.5%. Switzerland, Japan and South Korea face a minimum of 12.5% stacked on existing rates, while Brazil carries 37.5% in total. Argentina, Bangladesh, Cambodia, Ecuador, El Salvador, Guatemala, Indonesia, Jordan, Switzerland and Taiwan hold diamond and gem exemptions of their own. Canadian polished diamonds are governed separately and face 50% from August 19.",
"The desk's view: a grower in Surat now ships into the United States at 10% while an Antwerp dealer ships a mined stone at nothing, and no amount of marketing closes a gap that arrives before either stone reaches a display case. The lab-grown trade spent three years arguing it should be treated as a diamond for descriptive purposes and resisting the word synthetic. Washington has now treated it as a manufactured good for tariff purposes, which is the more expensive definition of the two. The category asked to be judged by what it is rather than where it came from, and the customs schedule has obliged."
],
[
 {"title":"Natural Diamonds from Europe Exempt from US Import Tariffs — Rapaport","url":"https://rapaport.com/news/natural-diamonds-from-europe-exempt-from-us-import-tariffs/"},
 {"title":"New Trump Tariffs: What They Mean for Jewelry — National Jeweler","url":"https://nationaljeweler.com/articles/15165-new-trump-tariffs-what-they-mean-for-jewelry"},
 {"title":"New US Tariffs Include Diamonds and Gemstones — Rapaport","url":"https://rapaport.com/news/new-us-tariffs-include-diamonds-and-gemstones/"},
 {"title":"US Tariffs on Canadian Imports to Include Diamonds and Jewelry — Rapaport","url":"https://rapaport.com/news/us-tariffs-on-canadian-imports-to-include-diamonds-and-jewelry/"},
])

# ========== 3. the-tender-ladder ==========
art("the-tender-ladder","diamonds",False,"Diamonds Desk · Tenders",4,"The Diamonds Desk",
["NUM","VS"],
"The tender ladder: 100% in Dubai, 75% in Johannesburg",
"TAGS cleared 100% of a Zimbabwean parcel and 95% of an Angolan one this summer, but only about 75% of South African goods in Johannesburg. Its latest Dubai sale of large South African stones took $15.2 million at above 80%.",
[
"The tender circuit has produced the clearest read on rough demand available this summer, and it does not describe one market. TAGS, which runs competitive tenders out of Dubai and Johannesburg, reported sell-through of 100% on a Zimbabwean parcel offered in early June, 95% on an Angolan sale of stones 10.8 carats and above that took $21.7 million, roughly 75% per tender on South African goods sold through June and July in Johannesburg, and better than 80% on its most recent Dubai sale of large South African production, which realised $15.2 million. Four rates, one quarter, one house.",
"The spread is not random. The two sales that cleared almost everything were both large-stone offerings held in Dubai, where the buyer list is international and the goods were sorted for size. The Johannesburg tenders that left a quarter of the material unsold carried run-of-mine South African production, which means smaller and more variable parcels priced against exactly the segment that lab-grown competition has hollowed out. The tender house did not change its method between June and July. The goods changed, and the bidding followed them.",
"Price direction inside those clearances tells the same story more precisely. On the Zimbabwean sale TAGS reported prices firm in the higher qualities and slightly lower in the bottom ranges, which is the two-speed pattern the polished indices have been printing all year. The Angolan sale drew material from ten separate deposits plus the full run-of-mine output of one additional seller, so its 95% clearance is a genuinely broad sample rather than one favourable parcel. The house said prices again exceeded the participating mines' expectations, and reported record participant attendance in Johannesburg even as a quarter of the goods there went unsold.",
"Attendance rising while sell-through falls is the detail worth keeping. It means the buyers are present and the bids are being made, but the reserves on smaller South African material are still set above what manufacturers will pay. That is a pricing problem rather than a demand problem, and it is the correctable kind. De Beers has spent the year moving its own rough book toward market rather than above it, and the tender houses, which have no long-term contracts to defend, discover the same level faster and in public.",
"The desk's view: the useful number in this set is not the 100% or the 95%. It is the 75%, because a tender that clears three quarters of its book in front of record attendance has found the exact point where a South African run-of-mine parcel stops being worth manufacturing. Anyone pricing rough into the autumn should treat large-stone clearance rates as a poor proxy for the market they actually buy in. The top of the size range has been solid for eighteen months. The bottom is where the argument is, and the bottom is where three of these four tenders left goods on the table."
],
[
 {"title":"Prices for Rough at TAGS Tender Exceed Expectations — Rapaport","url":"https://rapaport.com/news/prices-for-rough-at-tags-tender-exceed-expectations/"},
 {"title":"TAGS — Trans Atlantic Gem Sales, tender results","url":"https://www.tagsauctions.com/"},
 {"title":"De Beers Trims Losses Amid Price Stabilization, Cost Cuts — Rapaport","url":"https://rapaport.com/news/de-beers-trims-losses-amid-price-stabilization-cost-cuts/"},
])

# ========== 4. record-quarter-weakest-half ==========
art("record-quarter-weakest-half","gold-metals",False,"Gold & Metals Desk · Official sector",4,"The Bullion Desk",
["VS","NUM","RECORD"],
"A record second quarter, the weakest half since 2022",
"Central banks bought 289 tonnes of gold in the second quarter, up 62% and a record for any second quarter. The first half still totalled 345 tonnes, the smallest since 2022, because the first quarter collapsed to 57.",
[
"The official sector produced two true statements about the same six months, and they point in opposite directions. Central banks bought a net 289 tonnes of gold in the second quarter of 2026, according to the World Gold Council's Gold Demand Trends published on July 30. That is 62% above the 177.9 tonnes bought in the second quarter of 2025 and a record for any second quarter on the council's numbers. It is also a fivefold jump from the first quarter, which was revised down to 57 tonnes. Add the two together and the first half comes to 345 tonnes, the smallest first half since 2022.",
"Poland did the heavy lifting. The National Bank of Poland was the largest single buyer in the quarter at 51 tonnes, taking its first-half purchases to 82 tonnes as it works toward a self-set reserve target of roughly 700 tonnes. The People's Bank of China added 33 tonnes, its largest quarterly addition since the fourth quarter of 2023, lifting reported holdings to 2,346 tonnes against a first-half total of only 40. Uzbekistan took 16 tonnes, Kazakhstan 15, and Jordan and the Czech Republic 6 each.",
"The sellers are the part the headline rate conceals. The Bank of Russia sold 22 tonnes, the largest disposal of the quarter, with reporting attributing it to a federal budget deficit rather than to any view on the metal. Turkey sold 4 tonnes and reduced its swap position from more than 80 tonnes to around 60. The Bundesbank sold 1. None of these is a strategic exit, but the netting is what turns a strong gross quarter into a merely respectable half, and it is why the 289 tonne figure should not be read as the run rate.",
"For the jewellery trade the official sector matters because it sets the floor the counter has to buy above. Central banks bought this gold into a price that has fallen for most of the year and a quarter in which jewellery demand hit a post-pandemic low of 278 tonnes. That is the whole tension of 2026 in one report: the institutions accumulated on weakness while the retail buyer withdrew on price. The council's own survey of reserve managers has 89% expecting official holdings to rise over the next twelve months.",
"The desk's view: a record second quarter and the weakest first half since 2022 are the same data set read at two different lengths, and the trade should quote the longer one. The quarterly figure flatters because the first quarter was unusually bad, and revisions to official sector data have been running large enough in both directions to make any single quarter a poor guide. What survives at half-year length is steadier and more useful: the official sector is still a net buyer at pace, Poland and China are the marginal demand, and Russia is selling for reasons that have nothing to do with gold."
],
[
 {"title":"Gold Demand Trends Q2 2026: Central Banks — World Gold Council","url":"https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q2-2026/central-banks"},
 {"title":"Gold Demand Trends Q2 2026 — World Gold Council","url":"https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q2-2026"},
 {"title":"Central bank gold purchases jump 62% to 288.9 tonnes in Q2","url":"https://news.bitcoin.com/finance/central-bank-gold-purchases-jump-62-to-288-9-tonnes-in-q2/"},
])

# ========== 5. three-hundred-eighty-billion ==========
art("three-hundred-eighty-billion","gold-metals",False,"Gold & Metals Desk · Demand",4,"The Bullion Desk",
["NUM","RECORD"],
"$380 billion: the half-year that cost the most",
"Total gold demand held flat at 1,269 tonnes in the second quarter and rose 2% to 2,522 tonnes across the half. In money rather than metal, that half-year set a record near $380 billion.",
[
"Gold demand in the second quarter was unchanged from a year earlier at 1,269 tonnes, which is the least interesting way to describe what happened. Across the first six months of 2026 the World Gold Council counted 2,522 tonnes, a rise of 2% on the same period of 2025. Measured in money rather than in metal, the same half-year was worth roughly $380 billion, a record. The tonnage moved by two percentage points. The value moved to an all-time high, and the entire difference between those two facts is the price.",
"That gap is the single most useful thing in the report for anyone who sells finished jewellery. The trade's cost base is denominated in the record, not in the flat line. A quarter in which the world bought the same weight of gold as last year but paid materially more for it describes exactly the position of a retailer replacing sold stock: the same case, the same number of pieces, a substantially larger cheque. Volume stability at record value is not a benign combination at the counter, and it is why margin has compressed in a year with no demand collapse.",
"The composition underneath is a straight substitution. Central banks took 289 tonnes in the quarter, up 62%, and investment demand held. Jewellery fabrication fell to 278 tonnes, the weakest quarter since the pandemic, with India down 15% by weight to 75.1 tonnes even as the value of Indian demand rose about 50%. Institutions bought weight. Consumers bought less weight and paid more for it. The aggregate held flat because the two moved in opposite directions by almost exactly the same amount, which makes the headline number a coincidence rather than a signal.",
"The forward question is whether the value record survives a price that has now risen for a month. Gold closed July at $4,041.70 after its first monthly gain since February, so the second half begins with the cost base higher than the average that produced the $380 billion. If tonnage holds and the price holds, the full year sets a value record without ever setting a volume one. That is a comfortable outcome for miners and central banks and an uncomfortable one for anyone whose business is fabricating metal into inventory.",
"The desk's view: report the tonnage to understand demand and the value to understand your own accounts, and never let the two be quoted in the same sentence without a note. A flat 1,269 tonnes reads as a stable market and is being written up that way. What the same quarter actually contains is an official sector accumulating hard, a jewellery buyer in retreat by weight, and a record half-year bill. The trade has spent 2026 being told demand is steady. Demand is steady. The cost of participating in it is not, and that is the number that decides who is still trading in 2027."
],
[
 {"title":"Gold Demand Trends Q2 2026 — World Gold Council","url":"https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q2-2026"},
 {"title":"Global gold demand remains stable in Q2: World Gold Council","url":"https://www.bignewsnetwork.com/news/279216231/global-gold-demand-remains-stable-in-q2-world-gold-council"},
 {"title":"Gold demand steady in Q2 2026 as central bank buying offsets jewellery slump — IndexBox","url":"https://www.indexbox.io/blog/global-gold-demand-steady-in-q2-2026-as-central-bank-buying-offsets-jewellery-slump/"},
])

# ========== 6. gold-waits-on-payrolls ==========
art("gold-waits-on-payrolls","gold-metals",False,"Gold & Metals Desk · Week ahead",4,"The Bullion Desk",
["NUM","HOWTO"],
"Gold opens August at $4,041.70 and waits on payrolls",
"No session since Friday's Kitco close of $4,041.70, so the tape carries. The week brings the ADP employment report midweek and non-farm payrolls on Friday, into a metal six weeks into a consolidation.",
[
"There is no new price. Markets have been shut since Kitco's 5pm New York close on Friday put spot gold at $4,041.70 an ounce, down $60.90 or 1.48% on the session, and nothing has traded since. That figure is what this tape carries into August, and it is the level the trade opens the month against. The white metals closed alongside it: silver $57.44, platinum $1,644.00 and palladium $1,256.00, all lower on the day and all lower across July even as gold finished the month about half a percent up.",
"The week is built around two labour prints. The ADP employment report lands midweek and the Bureau of Labor Statistics releases non-farm payrolls on Friday, the first full read on hiring since the Federal Reserve held rates on July 29 with three dissents. Gold rose above $4,100 on that decision and gave it back within two sessions when the dollar rebounded from a six-week low, which is a fair summary of how thin the conviction is in either direction. A weak payrolls number revives the case for cuts. A strong one confirms the hold and pressures the metal.",
"Analysts describe the technical position as a consolidation rather than a trend. FOREX.com and City Index put the metal six weeks into a range just above its yearly lows, with resistance identified at the 52-week moving average and the 2026 yearly open around $4,312 to $4,319. FX Leaders, writing before the weekend, marked nearer resistance at $4,070 and support at $4,020. Those are analysts' levels rather than facts about the metal, and they are quoted here as such, but they bracket a range of about $50 that has held for six weeks.",
"For the bench none of this changes the working number. At $4,041.70 an ounce, fine gold costs about $130 a gram before refining, alloy, loss and making charge, and that is the figure a quotation written this week has to survive. The month just closed was the first higher one since February, which means anyone who has been waiting out the decline in the expectation of restocking cheaper has now watched the reason for waiting expire. A four-month slide ended without an announcement and the metal held the $4,000 handle through a Fed hold, a dollar bounce and a war premium.",
"The desk's view: treat Friday as a binary and price accordingly, which mostly means not repricing anything before it. The useful discipline in a six-week range is to quote off the settlement and refuse to chase intraday prints, a lesson this tape learned expensively in July when reference-point drift produced three inconsistent day changes in two weeks. Payrolls will either break the range or extend it, and there is no informational advantage available to a jeweller in guessing which. The advantage is in having the trade-in policy, the insurance schedule and the making charge already written against $4,000 before the number prints."
],
[
 {"title":"Gold Spot Prices — Kitco (July 31, 2026 close)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Gold Price Forecast: XAU/USD Poised for August Breakout After Six Weeks of Consolidation — City Index","url":"https://www.cityindex.com/en-uk/news-and-analysis/gold-price-forecast-xau-usd-poised-for-august-breakout-after-six-weeks-of-consolidation-8-1-2026-2026-07-31/"},
 {"title":"Gold Price Forecast: XAU/USD Holds Above $4,040 Ahead of NFP Week — FX Leaders","url":"https://www.fxleaders.com/news/2026/08/01/gold-price-forecast-xau-usd-holds-above-4040-ahead-of-nfp-week/"},
 {"title":"Gold — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/gold"},
])

# ========== 7. ny-now-opens-today ==========
art("ny-now-opens-today","retail-tech",False,"Retail & Tech Desk · New York",4,"The Retail Desk",
["ACTOR","NUM"],
"NY Now opens today under new owners",
"The summer market runs August 2 to 4 at the Javits Center, the first edition since Rockview Management Group bought the show from Emerald. More than 70 exhibitors are new or returning.",
[
"NY Now opens at the Javits Center this morning and runs to August 4, the first summer market since Rockview Management Group acquired the show from Emerald. The wholesale event covers gift, home, lifestyle, accessories and both fine and fashion jewellery, and the new owner has put its opening statement into the exhibitor list rather than into the floor plan. More than 70 exhibitors are either new or returning after a hiatus, and the organisers count over 90 brands and makers from 19 countries across the show.",
"The fine jewellery presence sits in two named sections. Luxury Lifestyle carries established brands including Brooke Gregson, Heather B. Moore, Bondeye Jewelry, Eden Presley, Carolina Neves, Dana Kellin and Annette Ferdinandsen. Curated is reserved for emerging luxury designers. Exhibiting fine jewellery names include Dilamani, Hine Fine Jewelry, J Fields Jewelry, Jacob Keleher Jewelry, Lauren Newton Jewelry, Tacit Fine Jewelry, Jewels by Sanjam, Jessica Liu Designs and Yael Sonia. Dorothy Belshaw, the chief executive, said buyers now find \"genuine discovery alongside the trusted brands they rely on\".",
"The count of returning exhibitors is the number that carries information. A show that has lost vendors and then wins some of them back under new ownership is being re-underwritten by the people who left it, and 70 is a large enough figure to be a verdict rather than a courtesy. What it does not yet establish is attendance, which the organisers have not published, and which is the only measure that determines whether the exhibitors who came back will book again for winter.",
"The timing places the show at an awkward point in the buying calendar. August is when independent jewellers commit open-to-buy for the fourth quarter, into a market where American consumer confidence slipped to 90.8 in July and gold sits above $4,000 an ounce, which has pushed retail assortments toward lighter pieces and higher price points at the same time. A buyer walking the Javits floor today is choosing holiday inventory against a metal cost that has risen for a month and a customer who has been trading down by weight.",
"The desk's view: the trade show is quietly the most exposed format in this industry, and NY Now's ownership change is worth watching for that reason rather than for its jewellery list. Regional shows have been consolidating for a decade while the buying itself moved to catalogues, video appointments and direct reordering, and the events that survive do it by being where a buyer discovers something they were not searching for. Seventy returning exhibitors say the format still has that. Whether Rockview can convert a strong first floor into a durable one will be answered in January, not this week."
],
[
 {"title":"NY Now Returns in August Under New Ownership — National Jeweler","url":"https://nationaljeweler.com/articles/15155-ny-now-returns-in-august-under-new-ownership"},
 {"title":"NY Now Welcomes 90-Plus International Brands From 19 Countries to Javits Center — InStore","url":"https://instoremag.com/ny-now-welcomes-90-plus-international-brands-from-19-countries-to-javits-center-this-summer/"},
 {"title":"70+ New Exhibitors Test the Waters with New NY Now Management — Gifts & Decorative Accessories","url":"https://www.giftsanddec.com/ny-now/70-new-exhibitors-test-the-waters-with-new-ny-now-management/"},
 {"title":"New York Show, Winter & Summer 2026 Dates — NY NOW","url":"https://nynow.com/market/"},
])

# ========== 8. jewellery-tops-a-flat-market ==========
art("jewellery-tops-a-flat-market","retail-tech",False,"Retail & Tech Desk · Luxury",4,"The Retail Desk",
["NUM","VS"],
"Bain puts jewellery on top of a flat luxury market",
"The Bain and Altagamma spring study has personal luxury goods growing 2% to 4% in 2026, reaching €365 to €373 billion after falling to €358 billion last year. Jewellery is named the strongest category.",
[
"Jewellery has finished 2026's first half as the best-performing category in a luxury market that is barely moving. The spring edition of the Bain and Altagamma Luxury Goods Worldwide Market Study puts personal luxury goods, which covers jewellery, watches, fashion and accessories, at €358 billion in 2025, down from €364 billion the year before, and forecasts €365 billion to €373 billion in 2026, a return to growth of 2% to 4%. Total global luxury spending is put at €1.44 trillion to €1.47 trillion, growing between nothing and 2% at constant exchange rates.",
"The category evidence is in the reported quarters rather than in the forecast. Richemont's jewellery houses grew for a seventh consecutive quarter in the first period of its year, and Kering's jewellery brands posted double-digit growth over the same window, with Boucheron reaching a record. This desk has filed both, along with Tiffany and Bulgari carrying an LVMH group that fell 3% overall. Four separate groups have now reported the same shape: jewellery up, the rest of the portfolio flat or down, in a market where the aggregate is close to zero.",
"The regional split explains where that growth is being found. Bain has American luxury brands up 10% to 15% year on year in the first quarter and United States spending rising, while Europe is described as the weak link on faltering international tourism. China is recovering slowly. Japan is slowing as Chinese tourist traffic falls away from the exchange-rate boom that drove it. A category leading a flat market on American demand is a category with a concentrated dependency, and the tariff schedule that took effect on July 24 sits directly on top of that dependency.",
"Watches are given a separate diagnosis and it is a structural one. Bain describes collectors valuing connoisseurship over hype, with the momentum moving to the resale market. That is consistent with what the secondary indices have shown all year, and with Swiss export figures that recovered 11.2% in June while the first half stayed 0.7% below last year. It is not a description of a weak category. It is a description of a category whose demand has moved to a channel the brands do not own.",
"The desk's view: being the strongest category in a market growing between zero and 2% is a smaller distinction than the press release implies, and it should be read as evidence of where luxury spending retreats to rather than of jewellery's momentum. When discretionary budgets tighten, buyers move toward objects with a metal value and a resale market and away from goods that depreciate on the walk home. Gold above $4,000 an ounce has made that logic explicit rather than instinctive. The risk in the trade's current good run is mistaking a defensive rotation for a structural preference, because rotations reverse when confidence returns."
],
[
 {"title":"Jewelry Leads Luxury Market Amid Stabilization, Bain Says — National Jeweler","url":"https://nationaljeweler.com/articles/15167-jewelry-leads-luxury-market-amid-stabilization-bain-says"},
 {"title":"Bain: Jewellery Emerges as Luxury's Bright Spot as Market Finds Stability — Solitaire (GJEPC)","url":"https://gjepc.org/solitaire/bain-jewellery-emerges-as-luxurys-bright-spot-as-market-finds-stability/"},
 {"title":"Luxury Market Stabilizes: Bain-Altagamma Forecasts Growth and Consumer Shifts for 2026 — WWD","url":"https://wwd.com/business-news/business-features/luxury-market-bain-altagamma-forecasts-growth-2026-1239032562/"},
 {"title":"Global luxury stabilizes amid compounding disruptions — Bain & Company","url":"https://www.bain.com/about/media-center/press-releases/2026/global-luxury-stabilizes-amid-compounding-disruptions-as-brands-race-to-amplify-meaning-and-rebuild-relevance/"},
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

specs["nobody-has-de-beers-yet"] = {
 **strip("By the numbers · the De Beers sale",[
   {"fig":"H2 2026","lab":"completion targeted"},
   {"fig":"~1 year","lab":"approvals after signing"},
   {"fig":"0","dir":"down","lab":"exclusive bidders"},
   {"fig":"$1.6B","dir":"down","lab":"H1 revenue, −19%"},
   {"fig":"−$113M","dir":"up","lab":"H1 EBITDA loss"}]),
 "figs":[bars("Plate I","De Beers underlying EBITDA loss, first half",[
   {"l":"H1 2025","v":100,"d":"−$189M"},
   {"l":"H1 2026","v":60,"d":"−$113M","hi":True}],
   "Loss narrowed on cost cuts rather than recovered demand. Anglo American.",165)],
 "flow":flow5("A stage, and a sequence.","The pick was not right.","No listing, no disclosure.",
   "a named front-runner and a live auction produce very different prices for the same asset","The Diamonds Desk",
   "Anglo picks the Penny group","a-de-beers-sale-gets-a-clock.html"),
 "desk":{"split":"the exclusivity denial is the part to trade on, not the timetable"},
 "next":nxt("one-billion-for-de-beers","Valuation","A consortium would pay $750 million up front.",
   "de-beers-narrows-the-loss","Results","gaborone-answers-penny","Botswana")}

specs["zero-for-antwerp"] = {
 **strip("By the numbers · the July 24 schedule",[
   {"fig":"0%","dir":"down","lab":"EU loose natural diamonds"},
   {"fig":"10–12.5%","dir":"up","lab":"across 60 countries"},
   {"fig":"0","lab":"exemptions for lab-grown"},
   {"fig":"$2.1B","lab":"Belgian polished to US, 2024"},
   {"fig":"50%","dir":"up","lab":"Canada, from Aug 19"}]),
 "figs":[bars("Plate I","What a stone pays entering the United States",[
   {"l":"NATURAL, CUT IN THE EU","v":0,"d":"0%","hi":True},
   {"l":"INDIA, CANADA, UK","v":10,"d":"10%"},
   {"l":"UAE, ISRAEL, SOUTH AFRICA","v":12.5,"d":"12.5%"},
   {"l":"BRAZIL","v":37.5,"d":"37.5%"},
   {"l":"CANADA POLISHED, AUG 19","v":50,"d":"50%"}],
   "Section 301 schedule in force July 24, 2026. Lab-grown exempt nowhere.",166)],
 "flow":flow5("A line between two kinds of stone.","No industry to protect.","An uneven schedule.",
   "Lab-grown diamonds received no exemption from any country on the list.","The Diamonds Desk",
   "The tariff wall comes back","a-tariff-wall-returns.html"),
 "desk":{"split":"no amount of marketing closes a gap that arrives before either stone reaches a display case"},
 "next":nxt("antwerp-thins-india-loads","Antwerp","Antwerp runs short of goods and buyers turn to India.",
   "surat-eats-the-ten","India","russia-bans-the-word","Language")}

specs["the-tender-ladder"] = {
 **strip("By the numbers · TAGS, summer tenders",[
   {"fig":"100%","dir":"up","lab":"Zimbabwe, Dubai"},
   {"fig":"95%","dir":"up","lab":"Angola, $21.7M"},
   {"fig":">80%","lab":"South Africa, Dubai"},
   {"fig":"~75%","dir":"down","lab":"South Africa, Johannesburg"},
   {"fig":"$15.2M","lab":"latest Dubai sale"}]),
 "figs":[bars("Plate I","Sell-through by tender, June and July",[
   {"l":"ZIMBABWE / DUBAI","v":100,"d":"100%","hi":True},
   {"l":"ANGOLA / 10.8CT+","v":95,"d":"95%"},
   {"l":"SOUTH AFRICA / DUBAI","v":80,"d":">80%"},
   {"l":"SOUTH AFRICA / J'BURG","v":75,"d":"~75%"}],
   "Four TAGS tenders, one quarter. Percentage of lots sold.",167)],
 "flow":flow5("Four rates, one house.","Size decided it.","Attendance up, clearance down.",
   "The tender house did not change its method between June and July.","The Diamonds Desk",
   "Ninety-five percent sold in Luanda","a-angolas-rough-clears.html"),
 "desk":{"split":"the useful number in this set is not the 100% or the 95%"},
 "next":nxt("small-stones-lead-again","Prices","Small stones lead again as one-carat goods slip.",
   "thirties-outrun-the-ones","Polished","de-beers-narrows-the-loss","De Beers")}

specs["record-quarter-weakest-half"] = {
 **strip("By the numbers · central banks, Q2 2026",[
   {"fig":"289 t","dir":"up","lab":"net purchases, Q2"},
   {"fig":"+62%","dir":"up","lab":"year on year"},
   {"fig":"57 t","dir":"down","lab":"Q1, revised"},
   {"fig":"345 t","dir":"down","lab":"first half, smallest since 2022"},
   {"fig":"−22 t","dir":"down","lab":"Russia, largest seller"}]),
 "figs":[bars("Plate I","Largest official buyers, Q2 2026",[
   {"l":"POLAND","v":51,"d":"51 t","hi":True},
   {"l":"CHINA","v":33,"d":"33 t"},
   {"l":"UZBEKISTAN","v":16,"d":"16 t"},
   {"l":"KAZAKHSTAN","v":15,"d":"15 t"},
   {"l":"RUSSIA (SOLD)","v":22,"d":"−22 t"}],
   "Net tonnes. World Gold Council, Gold Demand Trends, 30 July 2026.",168)],
 "flow":flow5("Two true statements.","Poland did the lifting.","The sellers the rate conceals.",
   "Add the two together and the first half comes to 345 tonnes, the smallest first half since 2022.","The Bullion Desk",
   "China pulls in 173 tonnes","a-china-takes-173-tonnes.html"),
 "desk":{"split":"a record second quarter and the weakest first half since 2022 are the same data set read at two different lengths"},
 "next":nxt("two-seventy-eight-tonnes","Jewellery","The smallest jewellery quarter since the pandemic.",
   "three-hundred-eighty-billion","Value","gold-ends-july-higher","Prices")}

specs["three-hundred-eighty-billion"] = {
 **strip("By the numbers · gold demand, H1 2026",[
   {"fig":"1,269 t","lab":"Q2 demand, flat"},
   {"fig":"2,522 t","dir":"up","lab":"first half, +2%"},
   {"fig":"$380B","dir":"up","lab":"first-half value, record"},
   {"fig":"278 t","dir":"down","lab":"jewellery, Q2"},
   {"fig":"75.1 t","dir":"down","lab":"India jewellery, −15%"}]),
 "figs":[bars("Plate I","Where the second quarter's gold went",[
   {"l":"CENTRAL BANKS","v":289,"d":"289 t, +62%","hi":True},
   {"l":"JEWELLERY","v":278,"d":"278 t, post-pandemic low"},
   {"l":"OF WHICH INDIA","v":75,"d":"75.1 t, −15%"}],
   "Tonnes, Q2 2026. World Gold Council.",169)],
 "flow":flow5("Flat metal, record money.","The cost base is the record.","A straight substitution.",
   "Institutions bought weight. Consumers bought less weight and paid more for it.","The Bullion Desk",
   "278 tonnes, the smallest jewellery quarter","a-two-seventy-eight-tonnes.html"),
 "desk":{"split":"report the tonnage to understand demand and the value to understand your own accounts"},
 "next":nxt("record-quarter-weakest-half","Official sector","Central banks bought 289 tonnes, up 62%.",
   "india-buys-fifteen-percent-less","India","gold-ends-july-higher","Prices")}

specs["gold-waits-on-payrolls"] = {
 **strip("By the numbers · the week ahead",[
   {"fig":"$4,041.70","lab":"Friday close, carried"},
   {"fig":"$57.44","dir":"down","lab":"silver"},
   {"fig":"$1,644.00","dir":"down","lab":"platinum"},
   {"fig":"Friday","lab":"non-farm payrolls"},
   {"fig":"6 weeks","lab":"of consolidation"}]),
 "figs":[bars("Plate I","The range analysts are watching",[
   {"l":"RESISTANCE, YEARLY OPEN","v":4319,"d":"$4,312–4,319"},
   {"l":"NEAR RESISTANCE","v":4070,"d":"$4,070"},
   {"l":"LAST SETTLEMENT","v":4042,"d":"$4,041.70","hi":True},
   {"l":"NEAR SUPPORT","v":4020,"d":"$4,020"}],
   "Analyst levels, not facts about the metal. City Index and FX Leaders.",170)],
 "flow":flow5("No new price.","Two labour prints.","A range, not a trend.",
   "There is no new price.","The Bullion Desk",
   "Gold's first monthly gain since February","a-gold-ends-july-higher.html"),
 "desk":{"split":"treat Friday as a binary and price accordingly, which mostly means not repricing anything before it"},
 "next":nxt("gold-ends-july-higher","The month","Gold's first monthly gain since February.",
   "white-metals-close-the-month","Metals","fed-holds-gold-exhales","The Fed")}

specs["ny-now-opens-today"] = {
 **strip("By the numbers · NY Now, summer market",[
   {"fig":"Aug 2–4","lab":"Javits Center"},
   {"fig":"70+","dir":"up","lab":"new or returning exhibitors"},
   {"fig":"90+","lab":"brands exhibiting"},
   {"fig":"19","lab":"countries represented"},
   {"fig":"90.8","dir":"down","lab":"US consumer confidence, July"}]),
 "figs":[bars("Plate I","NY Now's fine jewellery floor",[
   {"l":"LUXURY LIFESTYLE","v":100,"d":"established brands","hi":True},
   {"l":"CURATED","v":60,"d":"emerging designers"},
   {"l":"NEW OR RETURNING","v":70,"d":"70+ exhibitors"}],
   "First summer market under Rockview Management Group ownership.",171)],
 "flow":flow5("A new owner's first floor.","Two named sections.","The number that carries information.",
   "More than 70 exhibitors are either new or returning after a hiatus","The Retail Desk",
   "Confidence slips to 90.8","a-confidence-slips-to-ninety.html"),
 "desk":{"split":"the trade show is quietly the most exposed format in this industry"},
 "next":nxt("india-fills-the-hall","Shows","India's big August show fills up early.",
   "confidence-slips-to-ninety","Consumer","the-storefront-that-isnt","Retail")}

specs["jewellery-tops-a-flat-market"] = {
 **strip("By the numbers · Bain and Altagamma",[
   {"fig":"€358B","dir":"down","lab":"personal luxury, 2025"},
   {"fig":"€365–373B","dir":"up","lab":"2026 forecast"},
   {"fig":"+2–4%","dir":"up","lab":"category growth"},
   {"fig":"€1.44–1.47T","lab":"total luxury spending"},
   {"fig":"0–2%","lab":"total market growth"}]),
 "figs":[bars("Plate I","Personal luxury goods, in billions of euros",[
   {"l":"2024","v":364,"d":"€364B"},
   {"l":"2025","v":358,"d":"€358B, −2%"},
   {"l":"2026 FORECAST","v":369,"d":"€365–373B","hi":True}],
   "Bain and Altagamma Luxury Goods Worldwide Market Study, spring 2026.",172)],
 "flow":flow5("Best in a market barely moving.","Four groups, one shape.","Where the growth is found.",
   "Four separate groups have now reported the same shape: jewellery up, the rest of the portfolio flat or down","The Retail Desk",
   "Boucheron carries Kering","a-boucheron-carries-kering.html"),
 "desk":{"split":"being the strongest category in a market growing between zero and 2% is a smaller distinction than the press release implies"},
 "next":nxt("tiffany-carries-lvmh","LVMH","Tiffany and Bulgari carry a group that slipped 3%.",
   "boucheron-carries-kering","Kering","richemont-twenty-percent-quarter","Richemont")}

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
assert leads==["nobody-has-de-beers-yet"], f"lead set wrong: {leads}"
for s in specs: editorial[s]=specs[s]

(C/"articles.json").write_text(json.dumps(articles,ensure_ascii=False,indent=1))
(C/"editorial.json").write_text(json.dumps(editorial,ensure_ascii=False,indent=1))
print("articles now:",len(articles)," specs now:",len(editorial)," lead:",leads)
for d in NEW: print("  ",d["desk"].ljust(12), str(len(" ".join(d["body"]).split())).rjust(4),"w  ",d["slug"])
print("OK")
