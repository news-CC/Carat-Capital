#!/usr/bin/env python3
# Edition No. 021 - 2026-07-31. Prepends 8 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-07-31"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - de-beers-narrows-the-loss ==========
art("de-beers-narrows-the-loss","diamonds",True,"Lead Story · Diamonds Desk",5,"The Diamonds Desk",
["NUM","ACTOR","VS"],
"De Beers loses $188 million and points at a steady index",
"Anglo American's half-year accounts put De Beers revenue at $1.58 billion, down 19%, with an underlying loss of $188 million, 23% narrower. The realised price fell 32% to $105 a carat; unit costs fell 26% to $64.",
[
"De Beers spent the first half of 2026 losing money more slowly. Anglo American's interim results put the diamond unit's revenue at $1.58 billion, 19% lower year on year, with an underlying loss of $188 million that was 23% narrower than a year earlier and an underlying EBITDA loss of $113 million, 40% smaller. Sales volumes fell 20% across the six months. For a business absorbing the worst rough market in a generation, a smaller loss is the only good news on offer, and the company took it.",
"The price line is where the argument sits. The consolidated average realised price fell 32% to $105 a carat, pulled down both by a sales mix weighted toward lower-value goods and by a rough price index 16% below last year. Within the half, though, the index barely moved: 68 in the first quarter and 69 in the second. De Beers has been arguing since its July sight that prices have found their level, and these accounts are the first set of numbers that support the claim rather than the intention.",
"The cost side has done more work than the price side. Unit costs fell 26% to $64 a carat and capital expenditure dropped 33% to $115 million. Annual overheads are more than $100 million lighter than in 2024, and the two-year production pause at Venetia removes volume the market was never going to absorb. The trading division swung to $30 million of underlying EBITDA from a $260 million loss a year earlier, with margin at 2% against negative 16%. Synthetics kept pressure on the cheaper end of the book while stronger pricing for larger goods held the overall index steady.",
"What none of it settles is ownership. Anglo's chief executive said the sale is in its final and most challenging phase and declined to name a buyer, a day after Bloomberg reported that the Gareth Penny consortium would pay about $1 billion for the 85% stake. Anglo still guides to completion by the end of 2026. A buyer reading these accounts sees a business whose losses are shrinking on cost discipline, and whose revenue still rests on an index that has stopped falling for two quarters, which is not the same as one that has started rising.",
"The desk's view: the useful numbers in this set are not the losses but the 68 and the 69. A rough price index that holds flat across two quarters is the precondition for everything else the trade wants, because a cutter cannot fund inventory that reprices underneath him and a sightholder cannot sign a contract against a falling book. De Beers bought that flat line by cutting prices to the market and taking roughly 25 buyers off the roster, which is an expensive way to earn stability. The half says the bleeding is controlled. It does not yet say anyone is selling more diamonds."
],
[
 {"title":"De Beers Trims Losses Amid Price Stabilization, Cost Cuts — Rapaport","url":"https://rapaport.com/news/de-beers-trims-losses-amid-price-stabilization-cost-cuts/"},
 {"title":"De Beers Sale in 'Final, Most Challenging' Phase, Anglo CEO Says — National Jeweler","url":"https://nationaljeweler.com/articles/15178-de-beers-sale-in-final-most-challenging-phase-anglo-ceo-says"},
 {"title":"Anglo American CEO Says De Beers Sale Is Almost Done but Won't Name Buyer — JCK","url":"https://www.jckonline.com/editorial-article/anglo-american-de-beers-sale-almost-done/"},
 {"title":"Half Year Financial Report 2026 — Anglo American","url":"https://www.angloamerican.com/investors/annual-reporting"},
])

# ========== 2. gold-gives-back-thursday ==========
art("gold-gives-back-thursday","gold-metals",False,"Gold & Metals Desk · New York",4,"The Bullion Desk",
["NUM","STAKES"],
"$4,055 gold: Thursday's rally goes back out on a dollar bounce",
"Spot fell 1.19% to $4,054.68 an ounce on the last trading day of July as the dollar rebounded and traders booked the previous session's gains. Gold is still 20.57% higher on the year and about 1.4% higher on the month.",
[
"Gold gave back a day's work on Friday. Spot traded at $4,054.68 an ounce, down 1.19%, after prints earlier in the session held above $4,086. Thursday had been the good day, with the metal cresting $4,100 in the relief that followed the Federal Reserve's decision to hold. Friday reversed most of it. On the year gold is still 20.57% higher, and July closes about 1.4% up on the month, which is a modest result for a month containing a Fed meeting and a war premium.",
"The cause was ordinary. The dollar rebounded from a six-week trough, and a stronger dollar makes bullion dearer for every buyer who does not earn in it. Traders who bought Thursday's rally sold Friday's open. Nothing in the macro picture changed between the two sessions, which is the point. The move was positioning, not information, and positioning unwinds faster than it builds.",
"The spread inside a single day is worth more attention than the close. A market that prints $4,086 in the morning and $4,055 by the afternoon is a market where the marginal seller is a trader rather than a holder. Central banks, which took 289 tonnes in the second quarter, do not trade the tape at that frequency, and neither does a jeweller buying casting metal for autumn. The people who moved the price on Friday will not be the people who own it in October.",
"For the bench, the arithmetic is unchanged by a bad afternoon. At $4,054.68 an ounce, fine gold costs about $130 a gram before refining, alloy, loss or making charge, against roughly $107 a gram this time last year. A retailer quoting a January price list is short about a fifth of the metal cost, and the customer who is trading in old chain to fund a new piece is doing the same arithmetic from the other side of the counter.",
"The desk's view: a 1.19% Friday is noise, and it would be a mistake to write the week from it. What the month says is more useful. Gold spent July in a band, absorbed a hawkish hold, absorbed a dollar bounce, and finished higher anyway. The trade should stop planning for a return to $3,500 and start pricing inventory, insurance and trade-in policy off a $4,000 handle, because a metal that will not break down on bad news is not a metal that is waiting to fall."
],
[
 {"title":"Gold — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/gold"},
 {"title":"Gold prices today: gold prices crest $4,100 after Fed holds rates steady — Yahoo Finance","url":"https://finance.yahoo.com/personal-finance/investing/article/gold-prices-today-thursday-july-30-2026-gold-prices-crest-4100-after-fed-holds-rates-steady-123355668.html"},
 {"title":"Gold price in India: rates on July 31 — FXStreet","url":"https://www.fxstreet.com/news/india-gold-price-today-gold-falls-according-to-fxstreet-data-202607310435"},
])

# ========== 3. three-metals-one-direction ==========
art("three-metals-one-direction","gold-metals",False,"Gold & Metals Desk · New York",4,"The Metals Desk",
["NUM","VS"],
"$57.99 silver, $1,636 platinum: the white metals close July lower",
"Silver fell 1.72% to $57.99, platinum 1.46% to $1,636 and palladium 1.53% to $1,288.50. All three are far higher on the year: silver 56.44%, platinum 24.28%, palladium 6.80%.",
[
"The white metals ended July the way gold did, only harder. Silver fell about 1.72% to $57.99 an ounce, platinum 1.46% to $1,636 and palladium 1.53% to $1,288.50. Three metals with three different demand stories moved the same way on the same afternoon, which usually means the dollar did the moving rather than anything in their own supply and demand.",
"Silver's failure is the one the trade will notice. The metal spent July trying to hold $60 and did not manage it, and at $57.99 against gold at $4,054.68 the gold-silver ratio sits near 69.9. Silver is still 56.44% higher than a year ago, a gain no jewellery buyer has fully passed on, and the silver counter is the part of the trade with the least room to absorb metal cost inside an existing price point.",
"Platinum's month was better than its day. The metal is 2.26% higher over the past month and 24.28% higher on the year, with a fourth consecutive annual supply deficit still forecast on constrained mine supply. Against that, the demand case keeps thinning at the showroom rather than the smelter: global platinum jewellery demand is expected to contract about 6% this year, with China supplying most of the fall. Palladium remains the odd one out, up 6.80% on the year and structurally exposed to a vehicle fleet that is electrifying underneath it.",
"For a manufacturer, the useful comparison is the gap. Platinum at $1,636 is roughly 40% of the gold price, so a bridal ring in a scarcer, denser metal still costs less in raw material than the same ring in gold, even after platinum's year. The obstacle has never been the metal price. It is that fewer benches can work platinum, and a house that cannot set it will not quote it.",
"The desk's view: one down day across three metals is a currency event, not a demand event, and nobody should reprice a case over it. The number that should change behaviour is the ratio near 69.9. Silver has spent the year outrunning gold and has now stalled just under $60, which is exactly the level at which silver jewellery programmes get rebuilt with lighter gauge or repriced outright. The house that has not yet done that arithmetic is carrying the cost quietly in its margin."
],
[
 {"title":"Silver — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/silver"},
 {"title":"Platinum — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/platinum"},
 {"title":"Palladium — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/palladium"},
])

# ========== 4. two-seventy-eight-tonnes ==========
art("two-seventy-eight-tonnes","gold-metals",False,"Gold & Metals Desk · London",4,"The Bullion Desk",
["NUM","RECORD"],
"278 tonnes: the smallest jewellery quarter since the pandemic",
"World Gold Council data put second-quarter jewellery demand at 278 tonnes, down 17% and the lowest quarterly volume since the pandemic, while its value rose 14% to $40 billion. Total gold demand held flat at 1,269 tonnes.",
[
"The jewellery trade bought less gold in the second quarter than in any quarter since the pandemic. The World Gold Council put global jewellery demand at 278 tonnes, down 17% year on year, while the value of that demand rose 14% to $40 billion. The explanation is a single number: the quarter's average London price was $4,506.29 an ounce. At that level the same shop window holds fewer grams, and the same customer goes home with a lighter piece.",
"Everything else in the quarter held up. Total gold demand was flat at 1,269 tonnes. Bar and coin buying was steady at 307 tonnes, central banks took 289 tonnes in a sharp recovery from a slow first quarter, and exchange-traded funds saw 45 tonnes of outflows as prices came off their highs. Investment stayed, jewellery left, and the first half set a record for the value of gold demand at $380 billion.",
"That divergence is the structural story of this cycle. Gold has spent two years being bought as a reserve asset and a hedge. Jewellery is the only demand category in the accounts that has to be paid for out of a household budget rather than a balance sheet. When the price rises, one bid gets stronger and the other gets weaker, and the tonnage line shows exactly which is which.",
"There is a second reading in the price the quarter averaged. At $4,506.29, the April to June period was dearer than the market is now: gold traded at $4,054.68 on Friday, roughly 10% below the quarter's mean. The tonnage that vanished in the second quarter was priced off a level the trade is no longer paying. If price is what suppressed volume, some of that volume should be recoverable in the third quarter, which is also when the Indian festive build begins.",
"The desk's view: 278 tonnes is the clearest measurement yet of what $4,500 gold does to a counter, and it is not a demand collapse but a substitution. Buyers did not stop; they bought lighter, and the value line proves they kept paying. The retailer's job in the second half is to sell that substitution deliberately rather than let it happen by attrition, which means engineered lighter weights, hollow and tube construction, and a bridal price ladder that starts below the metal-driven creep. The alternative is watching the average ticket rise while the boxes leaving the shop keep getting fewer."
],
[
 {"title":"Gold Demand Trends: Q2 2026 — World Gold Council","url":"https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q2-2026"},
 {"title":"Gold buyers shift to lighter jewellery as high prices curb Q2 demand — Gulf News","url":"https://gulfnews.com/business/retail/gold-buyers-shifted-to-lighter-jewellery-as-prices-stayed-high-in-q2-1.500626364"},
 {"title":"Gold — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/gold"},
])

# ========== 5. india-buys-fifteen-percent-less ==========
art("india-buys-fifteen-percent-less","retail-tech",False,"Retail & Tech Desk · Mumbai",4,"The Counter Desk",
["NUM","VS"],
"India's quarter: 75.1 tonnes of jewellery, down 15%",
"Indian jewellery demand fell to 75.1 tonnes in the second quarter from 88.8 tonnes, a 15% decline, and total Indian gold demand fell 6%. The value of that demand rose about 50% as prices set records.",
[
"India bought 75.1 tonnes of gold jewellery in the second quarter, down from 88.8 tonnes a year earlier. That is a 15% fall in weight, against a 6% fall in total Indian gold demand, and the gap between those two numbers is the whole story: Indians did not stop buying gold, they stopped buying it in the form that carries a making charge. The value of the country's demand rose about 50%, which is what a record price does to a shrinking tonnage.",
"Investment took the difference. Bars, coins and funds held up while the jewellery line gave way, the same split visible in the global figures, where bar and coin demand was steady at 307 tonnes and jewellery fell 17%. In a market where gold is simultaneously the savings product and the adornment, price stress does not reduce the allocation. It moves it from the showcase to the locker.",
"The counter has been managing this all year. Carat Capital reported on July 25 that Indian gold fell about 10% in June to a six-month low near 141,000 rupees per 10 grams and that listed jewellers logged 30% to 60% revenue growth as buyers returned, with old-gold trade-ins now funding up to 55% of counter sales. Exports told the same story from the other end of the pipe: June gem and jewellery shipments rose 26.5% to $2.21 billion, with gold jewellery up 54.5%.",
"What all of that describes is a market running on recycled metal and price-led revenue rather than fresh demand. A trade-in ratio above half means the shop is largely turning a customer's existing gold into a new piece and charging for labour, which is a good business in a high price and a fragile one in a falling price. Volume growth, when it returns, will show up in the tonnage line before it shows up in revenue.",
"The desk's view: 75.1 tonnes is a soft quarter but not a broken one, and the third quarter matters far more, because it carries the festive build into Dhanteras and Diwali. Two things will decide it: whether gold stays near $4,000 rather than $4,500, and whether jewellers have restocked light-weight ranges in time. On the evidence of the export data, the manufacturing base is already making the lighter goods. The question is whether the counter has repriced the window to match what the customer can now afford to lift."
],
[
 {"title":"India's Q2 gold demand falls 6%, jewellery consumption drops 15% — IBTimes India","url":"https://www.ibtimes.co.in/indias-q2-gold-demand-falls-6-jewellery-consumption-drops-15-while-investment-demand-stays-904302"},
 {"title":"India Gold Demand Q2 2026: value record, volume down — NewKerala","url":"https://www.newkerala.com/news/a/indias-gold-demand-falls-q2-value-jumps-50-563.htm"},
 {"title":"Gold Demand Trends: Q2 2026 — World Gold Council","url":"https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q2-2026"},
 {"title":"India's Gems, Jewellery Exports Jump 26.5% to $2.21 Bn in June — KNN India","url":"https://knnindia.co.in/news/newsdetails/sectors/indias-gems-jewellery-exports-jump-265-to-usd-221-bn-in-june-gjepc"},
])

# ========== 6. confidence-slips-to-ninety ==========
art("confidence-slips-to-ninety","retail-tech",False,"Retail & Tech Desk · New York",4,"The Counter Desk",
["NUM","GAP"],
"90.8: confidence slips, and the present tense is the weak part",
"The Conference Board's index fell 1.4 points to 90.8 in July against a 92.3 consensus. The present situation index dropped 3.6 points to 114.9, a third consecutive decline, while expectations held at 74.7.",
[
"American consumer confidence fell again in July. The Conference Board's index came in at 90.8, down 1.4 points from an upwardly revised 92.2 in June and below a market consensus near 92.3. The composition matters more than the headline. The present situation index, which measures how people read current business and labour conditions, fell 3.6 points to 114.9, its third consecutive monthly decline. The expectations index was unchanged at 74.7 and remains in negative territory.",
"That is an unusual shape. For most of the past three years the pattern has been a gloomy forward view sitting on top of a solid assessment of the present, which is a consumer who says things will get worse and spends anyway. July inverts part of it: expectations stopped falling while the read on today deteriorated. The board's chief economist, Dana M. Peterson, described it plainly: \"Consumer confidence moderated slightly in July.\"",
"Confidence surveys are weak predictors of jewellery sales and useful predictors of jewellery discounting. The category is discretionary, high-ticket and heavily gifted, so it responds to how secure a household feels rather than to how much it earns. When the present-situation line falls three months running, the first casualty is not the engagement ring but the unplanned second purchase, and the second casualty is full margin, because sales staff start reaching for the discount before the customer asks.",
"The American counter is already showing the split. First-half jewellery revenue rose 8.6% while unit sales fell and the average ticket climbed roughly 19%, which is a market carried by fewer, wealthier buyers. A confidence reading that erodes at the present-situation end is precisely the pressure that thins the middle of that customer base while leaving the top intact. Gold near $4,000 and a new tariff round arriving at the same time do not help the arithmetic.",
"The desk's view: 90.8 is a soft number, not an alarming one, and the trade should treat it as a planning input for the fourth quarter rather than a reason to mark anything down in August. The practical response is inventory discipline: buy the holiday book narrower, weight it toward proven price points, and hold the fine goods rather than the middle. If the present-situation line falls a fourth month, the customer who was going to trade up this Christmas will trade sideways, and the retailer who bought breadth instead of depth will be the one paying for it in January."
],
[
 {"title":"US Consumer Confidence Edged Down in July — The Conference Board","url":"https://www.prnewswire.com/news-releases/us-consumer-confidence-edged-down-in-july-302836484.html"},
 {"title":"U.S. consumer confidence index falls to 90.8 in July 2026 — Quartz","url":"https://qz.com/conference-board-consumer-confidence-july-2026-072826"},
 {"title":"Consumer Confidence Slips in July — National Jeweler","url":"https://nationaljeweler.com/articles/15179-consumer-confidence-slips-in-july"},
 {"title":"US Jewelry Sales Grow 9% in H1 2026 — Tenoris","url":"https://www.tenoris.bi/us-jewelry-sales-continue-to-grow-in-h1-2026/"},
])

# ========== 7. the-ask-is-exclusion ==========
art("the-ask-is-exclusion","retail-tech",False,"Retail & Tech Desk · Washington",4,"The Policy Desk",
["ACTOR","STAKES"],
"Jewelers of America returns to Washington with one ask: exclusion",
"Trade groups met administration officials as a 10% to 12.5% tariff round covering about sixty countries took effect. Seven African producers and diamonds polished in the EU are exempt; India stays at 10%, and a second investigation is open.",
[
"Jewelers of America went back to Washington this week, and its request has narrowed to a single sentence: take diamonds, gemstones and pearls out of the tariff schedule. Industry groups met administration officials days after a fresh round of duties came into force, and the association is asking members to write to their own legislators through its action centre. The lobbying position is no longer about rates. It is about category.",
"The wall those groups are arguing with is now specific. The current round applies 10% to 12.5% duties to imports from roughly sixty countries under a forced-labour investigation, effective from late July. Seven producing states are exempt: Botswana, Namibia, Kenya, Madagascar, Mozambique, Tanzania and Zambia. Diamonds polished in the European Union keep their exemption. India, which cuts the majority of the world's polished goods, carries 10%, and that single line is the one that reaches most American counters.",
"A second front is open behind it. An overproduction investigation covering India, China, Thailand, the European Union and Switzerland could add further duties on top of the current schedule, which would catch Swiss watches and Thai colour at the same time as Indian polished. The watch trade is already litigating: a group of American dealers sued over the tariff regime in late July. Two remedies are being pursued in parallel, one legal and one legislative, because neither is reliable alone.",
"The exclusion argument is stronger than it sounds. Rough diamonds and coloured stones are not manufactured in the United States in commercial quantity, so a duty on them cannot protect a domestic industry that does not exist. It functions as a tax on American cutters, setters and retailers, collected at the border and paid at the counter. That is the case the trade is making, and it is the same one the exempt African producer list already concedes in practice.",
"The desk's view: an exclusion for natural stones is the cheapest possible concession for the administration and the most valuable one available to this industry, which is precisely why it is worth the trip. Retailers should not plan on getting it. The working assumption for the autumn buy should remain 10% on Indian polished, with a contingency for the overproduction case landing on Swiss and Thai goods before Christmas. The houses that repriced early in July are, so far, the ones with a functioning margin."
],
[
 {"title":"JA Heads Back to Washington as New Wave of Tariffs Takes Effect — National Jeweler","url":"https://nationaljeweler.com/articles/15181-ja-heads-back-to-washington-as-new-wave-of-tariffs-takes-effect"},
 {"title":"Jewelry Industry Groups Meet With Government Officials to Talk Tariffs — JCK","url":"https://www.jckonline.com/"},
 {"title":"Legislative Action Center — Jewelers of America","url":"https://www.jewelers.org/advocacy"},
])

# ========== 8. gemfields-covers-the-ruby ==========
art("gemfields-covers-the-ruby","gemstones",False,"Gemstones Desk · London",4,"The Color Desk",
["NUM","VS"],
"$102.9 million, up 72%: Gemfields' emeralds cover for its rubies",
"First-half auction revenue rose 72% to $102.9 million. Net debt stood at $44.2 million on June 30 before $33.3 million of auction receivables, and premium-grade ruby recovery at Montepuez ran at 0.025 carats a tonne.",
[
"Gemfields took $102.9 million from its auctions in the first half of 2026, 72% more than in the same period last year. For a company that spent 2025 raising money and cutting spending, that is the first half-year in a while where the sales line has done the work. The result comes from two very different mines, and only one of them is behaving.",
"Kagem, the Zambian emerald operation, held premium output through the January to June period. Its higher-quality rough auction, held in London across May, took $26.8 million, selling 36 of 37 lots and 183,385 of the 185,135 carats offered at an average $146.08 a carat, a clearance of 99% by weight. A February mixed-quality ruby sale added $53 million from 121 of 135 lots. Between them those two sales account for most of the half, and the emerald book is the part carrying a premium.",
"Montepuez is the problem. Premium-grade ruby recovery at the Mozambican mine ran at 0.025 carats per tonne, a low rate the company has attributed to a prolonged run of poor grade, and it is redirecting mining toward higher-potential areas while commissioning a new processing plant expected to reach full capacity later this year. Operating costs rose on fuel, exchange rates and mining volume. The response has been to schedule ruby auctions cautiously rather than push weak material into a thin market.",
"The balance sheet still needs the auctions. Net debt stood at $44.2 million at June 30, before $33.3 million of auction receivables that had not yet been collected. Full results are due on September 25. For a miner whose revenue arrives in a handful of discrete sales each year, the timing of a single tender can move the debt line more than a quarter of production does, which is why the auction calendar is effectively the financing calendar.",
"The desk's view: this is the colour market's two-speed problem written into one company's accounts. Fine emerald with documented origin clears at 99% by weight and $146 a carat, while ruby waits for grade that the ground is not currently giving up. For dealers, the read is that supply discipline is now the pricing mechanism in colour, and Gemfields is exercising it openly. For jewellers, the practical consequence is that fine Mozambican ruby will stay scarce and dear into 2027, and any programme built on calibrated goods should be sourced now rather than reordered later."
],
[
 {"title":"Gemfields Revenue Skyrockets in First Half — Rapaport","url":"https://rapaport.com/news/gemfields-revenue-skyrockets-in-first-half/"},
 {"title":"Gemfields Emerald Auction Holds Firm as Ruby Outlook Prompts Cautious Auction Strategy — TipRanks","url":"https://www.tipranks.com/news/company-announcements/gemfields-emerald-auction-holds-firm-as-ruby-outlook-prompts-cautious-auction-strategy"},
 {"title":"Gemfields' higher-quality emerald auction achieves $26.8M — National Jeweler","url":"https://nationaljeweler.com/articles/15005-gemfields-higher-quality-emerald-auction-achieves-26-8m"},
 {"title":"Auction Update — Gemfields Group","url":"https://www.gemfieldsgroup.com/category/new-and-announcements/auction-update/"},
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

specs["de-beers-narrows-the-loss"] = {
 **strip("By the numbers · De Beers, first half",[
   {"fig":"$1.58B","dir":"down","lab":"revenue, H1"},
   {"fig":"−19%","dir":"down","lab":"year on year"},
   {"fig":"$188M","lab":"underlying loss"},
   {"fig":"$105","dir":"down","lab":"realised, per carat"},
   {"fig":"$64","dir":"down","lab":"unit cost, per carat"}]),
 "figs":[bars("Plate I","Per carat, De Beers first half",[
   {"l":"REALISED PRICE","v":105,"d":"$105","hi":True},
   {"l":"UNIT COST","v":64,"d":"$64"}],
   "USD per carat, H1 2026. Realised price fell 32%; unit cost fell 26%.",149)],
 "flow":flow5("Losing money more slowly.","Costs did the work.","The owner question.",
   "De Beers has been arguing since its July sight that prices have found their level, and these accounts are the first set of numbers that support the claim rather than the intention.","The Diamonds Desk",
   "One billion for De Beers","a-one-billion-for-de-beers.html"),
 "desk":{"split":"A rough price index that holds flat across two quarters is the precondition for everything else the trade wants"},
 "next":nxt("de-beers-eighty-eight-up","The quarter","De Beers digs 88% more and banks 44% less.",
   "one-billion-for-de-beers","The sale","petra-caves-at-the-bottom","Producers")}

specs["gold-gives-back-thursday"] = {
 **strip("By the numbers · gold, 31 July",[
   {"fig":"$4,054.68","dir":"down","lab":"spot, Friday"},
   {"fig":"−1.19%","dir":"down","lab":"on the day"},
   {"fig":"+20.57%","dir":"up","lab":"year on year"},
   {"fig":"+1.4%","dir":"up","lab":"on the month"},
   {"fig":"$130","lab":"per gram, fine"}]),
 "figs":[bars("Plate I","Two prints, one session",[
   {"l":"FRI 31 JUL, EARLY","v":4086,"d":"$4,086"},
   {"l":"FRI 31 JUL, LATE","v":4055,"d":"$4,055","hi":True},
   {"l":"THU 30 JUL","v":4075,"d":"$4,075"}],
   "USD/oz spot. Trading Economics prints through the final session of July.",150)],
 "flow":flow5("A day's work, returned.","Traders, not holders.","The bench arithmetic.",
   "The move was positioning, not information, and positioning unwinds faster than it builds.","The Bullion Desk",
   "Gold takes back $4,075","a-gold-unwinds-the-hold.html"),
 "desk":{"split":"start pricing inventory, insurance and trade-in policy off a $4,000 handle"},
 "next":nxt("three-metals-one-direction","White metals","Silver, platinum and palladium all close July lower.",
   "gold-unwinds-the-hold","Thursday","two-seventy-eight-tonnes","Demand")}

specs["three-metals-one-direction"] = {
 **strip("By the numbers · the white metals",[
   {"fig":"$57.99","dir":"down","lab":"silver / oz"},
   {"fig":"$1,636","dir":"down","lab":"platinum / oz"},
   {"fig":"$1,288.50","dir":"down","lab":"palladium / oz"},
   {"fig":"69.9","lab":"gold-silver ratio"},
   {"fig":"−6%","dir":"down","lab":"2026 Pt jewellery demand"}]),
 "figs":[bars("Plate I","Year on year, the white metals",[
   {"l":"SILVER","v":56.44,"d":"+56.44%","hi":True},
   {"l":"PLATINUM","v":24.28,"d":"+24.28%"},
   {"l":"PALLADIUM","v":6.8,"d":"+6.80%"}],
   "Percent change over twelve months, at 31 July 2026.",151)],
 "flow":flow5("Three metals, one afternoon.","Platinum's month beat its day.","The gap that matters.",
   "Three metals with three different demand stories moved the same way on the same afternoon, which usually means the dollar did the moving rather than anything in their own supply and demand.","The Metals Desk",
   "White metals lose their heat","a-white-metals-lose-their-heat.html"),
 "desk":{"split":"Silver has spent the year outrunning gold and has now stalled just under $60"},
 "next":nxt("gold-gives-back-thursday","Gold","Gold gives back Thursday's rally on a dollar bounce.",
   "platinum-loses-its-teacher","Platinum","silver-eyes-sixty","Silver")}

specs["two-seventy-eight-tonnes"] = {
 **strip("By the numbers · gold demand, Q2",[
   {"fig":"278t","dir":"down","lab":"jewellery demand"},
   {"fig":"−17%","dir":"down","lab":"year on year"},
   {"fig":"$40B","dir":"up","lab":"jewellery, by value"},
   {"fig":"1,269t","lab":"total demand, flat"},
   {"fig":"$4,506.29","lab":"average price, Q2"}]),
 "figs":[bars("Plate I","Second quarter, by category",[
   {"l":"BAR AND COIN","v":307,"d":"307t"},
   {"l":"JEWELLERY","v":278,"d":"278t","hi":True},
   {"l":"CENTRAL BANKS","v":289,"d":"289t"},
   {"l":"ETF FLOWS","v":-45,"d":"−45t"}],
   "Tonnes, Q2 2026. World Gold Council Gold Demand Trends.",152)],
 "flow":flow5("The lightest quarter since the pandemic.","Investment stayed, jewellery left.","A price the market has left behind.",
   "Jewellery is the only demand category in the accounts that has to be paid for out of a household budget rather than a balance sheet.","The Bullion Desk",

   "China takes 173 tonnes","a-china-takes-173-tonnes.html"),
 "desk":{"split":"278 tonnes is the clearest measurement yet of what $4,500 gold does to a counter, and it is not a demand collapse but a substitution"},
 "next":nxt("india-buys-fifteen-percent-less","India","India's jewellery tonnage falls 15% as the bill hits a record.",
   "gold-gives-back-thursday","Gold","more-dollars-fewer-boxes","Retail")}

specs["india-buys-fifteen-percent-less"] = {
 **strip("By the numbers · India, Q2",[
   {"fig":"75.1t","dir":"down","lab":"jewellery demand"},
   {"fig":"88.8t","lab":"a year earlier"},
   {"fig":"−15%","dir":"down","lab":"jewellery, by weight"},
   {"fig":"−6%","dir":"down","lab":"total gold demand"},
   {"fig":"+50%","dir":"up","lab":"demand, by value"}]),
 "figs":[bars("Plate I","Indian jewellery demand, second quarter",[
   {"l":"Q2 2025","v":88.8,"d":"88.8t"},
   {"l":"Q2 2026","v":75.1,"d":"75.1t","hi":True}],
   "Tonnes. World Gold Council quarterly data for India.",153)],
 "flow":flow5("Seventy-five tonnes.","From the showcase to the locker.","Recycled metal, priced revenue.",
   "In a market where gold is simultaneously the savings product and the adornment, price stress does not reduce the allocation.","The Counter Desk",
   "India buys the dip","a-india-buys-the-dip.html"),
 "desk":{"split":"the third quarter matters far more, because it carries the festive build into Dhanteras and Diwali"},
 "next":nxt("two-seventy-eight-tonnes","Global","Jewellery demand falls to 278 tonnes worldwide.",
   "india-pays-in-old-gold","Trade-ins","india-ships-the-turn","Exports")}

specs["confidence-slips-to-ninety"] = {
 **strip("By the numbers · confidence, July",[
   {"fig":"90.8","dir":"down","lab":"headline index"},
   {"fig":"−1.4","dir":"down","lab":"points on the month"},
   {"fig":"114.9","dir":"down","lab":"present situation"},
   {"fig":"74.7","lab":"expectations, unchanged"},
   {"fig":"92.3","lab":"consensus"}]),
 "figs":[bars("Plate I","The two halves of the index",[
   {"l":"PRESENT SITUATION","v":114.9,"d":"114.9","hi":True},
   {"l":"HEADLINE","v":90.8,"d":"90.8"},
   {"l":"EXPECTATIONS","v":74.7,"d":"74.7"}],
   "Index level, July 2026. The Conference Board.",154)],
 "flow":flow5("Down 1.4 points.","An unusual shape.","What it does to margin.",
   "Confidence surveys are weak predictors of jewellery sales and useful predictors of jewellery discounting.","The Counter Desk",
   "June retail, a thin cushion","a-june-retail-thin-cushion.html"),
 "desk":{"split":"buy the holiday book narrower, weight it toward proven price points, and hold the fine goods rather than the middle"},
 "next":nxt("the-ask-is-exclusion","Policy","Jewelers of America returns to Washington with one ask.",
   "average-ticket-carries-the-half","Tickets","more-dollars-fewer-boxes","Units")}

specs["the-ask-is-exclusion"] = {
 **strip("By the numbers · the tariff wall",[
   {"fig":"10–12.5%","lab":"current round"},
   {"fig":"~60","lab":"countries covered"},
   {"fig":"7","lab":"African producers exempt"},
   {"fig":"10%","lab":"India, polished"},
   {"fig":"5","lab":"states in the second case"}]),
 "figs":[bars("Plate I","Where the duty lands",[
   {"l":"CHINA, THAILAND, UAE","v":12.5,"d":"12.5%","hi":True},
   {"l":"INDIA, CANADA, BRITAIN","v":10,"d":"10%"},
   {"l":"EU POLISHED","v":0,"d":"exempt"},
   {"l":"SEVEN AFRICAN PRODUCERS","v":0,"d":"exempt"}],
   "Import duty on jewellery, diamonds and gemstones, from late July 2026.",155)],
 "flow":flow5("One sentence, repeated.","A second front.","Why exclusion is the cheap concession.",
   "The lobbying position is no longer about rates. It is about category.","The Policy Desk",
   "The tariff wall comes back","a-tariff-wall-returns.html"),
 "desk":{"split":"The working assumption for the autumn buy should remain 10% on Indian polished"},
 "next":nxt("confidence-slips-to-ninety","Demand","Consumer confidence slips to 90.8 in July.",
   "the-watch-trade-sues","Litigation","zero-duty-day-one","Exemptions")}

specs["gemfields-covers-the-ruby"] = {
 **strip("By the numbers · Gemfields H1",[
   {"fig":"$102.9M","dir":"up","lab":"auction revenue"},
   {"fig":"+72%","dir":"up","lab":"year on year"},
   {"fig":"$26.8M","lab":"May emerald sale"},
   {"fig":"0.025ct/t","dir":"down","lab":"premium ruby grade"},
   {"fig":"$44.2M","lab":"net debt, 30 June"}]),
 "figs":[bars("Plate I","Two sales inside the half",[
   {"l":"FEBRUARY RUBY","v":53,"d":"$53.0M","hi":True},
   {"l":"MAY EMERALD","v":26.8,"d":"$26.8M"}],
   "USD millions. Auction revenue by sale, first half 2026.",156)],
 "flow":flow5("Seventy-two percent more.","Montepuez is the problem.","The auction calendar is the financing calendar.",
   "The response has been to schedule ruby auctions cautiously rather than push weak material into a thin market.","The Color Desk",
   "Emeralds hold at $146","a-emeralds-hold-at-146.html"),
 "desk":{"split":"supply discipline is now the pricing mechanism in colour, and Gemfields is exercising it openly"},
 "next":nxt("color-runs-two-speeds","Colour","Two speeds in colour: a record sapphire, demand 30% down.",
   "sixty-six-dollars-a-carat","Ruby","the-guide-marks-ruby-up","Prices")}

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
assert leads==["de-beers-narrows-the-loss"], f"lead set wrong: {leads}"
for s in specs: editorial[s]=specs[s]

(C/"articles.json").write_text(json.dumps(articles,ensure_ascii=False,indent=1))
(C/"editorial.json").write_text(json.dumps(editorial,ensure_ascii=False,indent=1))
print("articles now:",len(articles)," specs now:",len(editorial)," lead:",leads)
for d in NEW: print("  ",d["desk"].ljust(12), str(len(" ".join(d["body"]).split())).rjust(4),"w  ",d["slug"])
print("OK")
