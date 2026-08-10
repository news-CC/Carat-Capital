#!/usr/bin/env python3
# Edition No. 031 - 2026-08-10. Prepends 5 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-10"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - neither-one-is-wrong ==========
art("neither-one-is-wrong","gold-metals",True,"Lead Story · Gold & Metals Desk",5,"The Gold & Metals Desk",
["REVERSAL","VS","NUM"],
"Two Dubai gold rates, 2% apart. Neither one is wrong",
"Two widely quoted Dubai gold pages read AED 512.45 and AED 523.25 a gram for 24-carat this morning, a gap of AED 10.80 or 2.11%. One is publishing the metal, the other the counter.",
[
"Two of the most widely quoted Dubai gold pages disagree this morning by AED 10.80 a gram. LivePriceOfGold's Dubai board, timestamped 10 August at 10:07 UTC, reads AED 512.45 a gram for 24-carat gold and AED 470.43 for 22-carat. Goodreturns' Dubai page, dated the same day, reads AED 523.25 and AED 484.50. That is a gap of 2.11% on the 24-carat line and 2.99% on the 22-carat line, both percentages derived by this desk from the two published figures. A jeweller quoting a customer off one page and buying off the other is out by a meaningful part of a making charge before anyone has cut anything.",
"The arithmetic says which is which. Kitco's live board at 5:57am New York time on 10 August, the reading this paper's tape now carries, puts gold at $4,341.40 an ounce. At 31.1035 grams to the troy ounce that is $139.58 a gram, and at the dirham's fixed peg of 3.6725 to the dollar it is AED 512.59 a gram. Both conversions are this desk's arithmetic and are published by nobody. LivePriceOfGold's 512.45 sits AED 0.14 from that figure, three hundredths of one per cent, and the page states that it prints a raw gold rate to which commission and labour charges are added. Goodreturns' 523.25 sits AED 10.66 above it. Neither page is wrong. They are not publishing the same quantity.",
"The series makes the point harder than a single morning can. Goodreturns' own ten-day table for Dubai runs AED 485.25 on 1 August, 487.25 on the 2nd and 3rd, 485.50 on the 4th, 492.25 on the 5th, 510.25 on the 6th, 510.50 on the 7th, 523.75 on the 8th, and 523.25 on the 9th and again today, the page reporting no change at all against yesterday. Between 7 and 8 August that page stepped up AED 13.25 a gram. Spot gold across the same span moved from $4,314.50 to $4,341.30 an ounce, which is AED 3.13 a gram at the peg. Roughly AED 10 of that step was not the metal, and the page has held the new level flat for three days while spot has kept moving.",
"This resolves a question this paper left open. On 7 August the edition printed three UAE retail readings for the same session and declined to choose between them: Khaleej Times at AED 517.50 a gram, one bureau desk at AED 510.25 and another at AED 514.00. Read against today's finding, those are not three attempts at one number. The peg arithmetic for 7 August gives AED 509.42, so the 510.25 sits on the raw-metal lane and the 517.50 sits on the counter lane. The spread this desk carried as an unresolved divergence across three editions was a category error rather than a data error, because it had not yet been established that two different quantities circulate under one name.",
"The desk's view: the number you quote is only as good as the lane it came from, and the Gulf gold trade currently runs two lanes under one label. There is nothing improper about either page. A raw-metal converter is the right instrument for hedging and for costing scrap; a counter rate is the right instrument for pricing a retail window. The failure is that neither is labelled clearly enough for a buyer to tell them apart, and the distance between them was 0.21% on 7 August against 2.11% today, so the error is not even stable enough to correct for by habit. The practical instruction for anyone dealing into the UAE this month is to stop quoting the Dubai gold rate as a single figure and to state the peg arithmetic beside it. At $4,341.40 an ounce the metal is AED 512.59 a gram, and everything above that line is somebody's margin rather than the metal."
],
[
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (10 August 2026, 5:57am EST live board)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Dubai Gold Price Live, 24-hour, in United Arab Emirates dirhams — LivePriceOfGold (10 August 2026, 10:07 UTC)","url":"https://www.livepriceofgold.com/dubai-gold-price.html"},
 {"title":"Today's Gold Rate in Dubai, 18, 22 & 24 Carat — Goodreturns (10 August 2026, with ten-day table)","url":"https://www.goodreturns.in/gold-rates/dubai.html"},
 {"title":"Every metal runs before payrolls — Carat Capital (7 August 2026)","url":"https://caratcapital.org/a-every-metal-runs-before-payrolls.html"},
])

# ========== 2. five-point-nine-million-pieces ==========
art("five-point-nine-million-pieces","gold-metals",False,"Gold & Metals Desk · India",5,"The Gold & Metals Desk",
["NUM","VS","STAKES"],
"5.9 million pieces: India's silver rush reaches the assay office",
"Hallmarked silver articles in India nearly doubled to 5.9 million in the 2025-26 financial year from 3.2 million. About 230 centres handle the testing, and the standards bureau says its own labs cover roughly two more years.",
[
"India hallmarked 5.9 million silver articles in the 2025-26 financial year, against 3.2 million the year before, an increase of about 84% that this desk derives from the two published counts. The Bureau of Indian Standards disclosed the figures on 9 August alongside a plan to scale up testing and certification capacity, and named the cause plainly: consumers moving into silver because gold has become unaffordable. Silver hallmarking in India has been voluntary since 2005, and the bureau has set no timeline for making it mandatory.",
"The infrastructure numbers give the scale of the build. About 230 bureau-recognised assaying and hallmarking centres currently handle silver testing across the country. The bureau's recognised laboratory network has gone from 147 in 2014 to 440 today, and government-empanelled laboratories from 24 to 350, against ten standalone bureau laboratories and roughly 270,000 product samples tested. Nishat S Haque, the bureau's deputy director general for laboratories, said the expansion runs over the next two years: \"Within that period, we will be expanding referral and assay laboratories across the country.\" Gold surveillance stays in-house; silver testing is being pushed out to the recognised centres while capacity catches up.",
"The substitution behind the number is one this paper has been tracking in pieces all year without a volume measure attached to it. Indian gold jewellery demand fell 15% by weight in the second quarter to 75.1 tonnes, its lowest second quarter since the pandemic, while the value of that demand rose about 50%. Kalyan Jewellers took more than 46% of its June-quarter revenue in recycled metal and more than 55% in the month of June alone. Those are demand-side and sourcing-side readings of the same pressure. A hallmarking count is neither: it is a physical count of finished articles passing through a testing centre. The assay office is where a substitution stops being anecdote and becomes volume.",
"What is missing from the announcement is the thing the trade would most like to know. There is no mandatory-hallmarking date for silver, which means the 5.9 million figure is a count of articles voluntarily submitted rather than a census of what India actually made. Gold's own mandatory regime, phased in from 2021, roughly tripled the certified count in its first three years, so the silver series is measuring the leading edge of a market rather than its size. The bureau introduced a hallmark unique identification number for silver in September 2025, which is the piece of plumbing a mandatory regime would need, and it is already in place.",
"The desk's view: hallmarking capacity is the least glamorous leading indicator in the metals trade, and this week it is the clearest one. Consumer surveys record intent, retailers report revenue that gold's price inflates on its own, and both can move without a single extra piece being made. An assay count cannot: every article in it physically exists and physically passed a test. Silver bid $63.99 an ounce on this paper's tape this morning, up 0.83% while gold sat flat, and the gold-to-silver ratio narrowed to 67.84 from 68.41. For a manufacturer weighing a silver line for the Indian festival season, the number to plan against is not the ratio, it is 230 testing centres against a submission count that has nearly doubled in a year. That is where the queue will form."
],
[
 {"title":"Gold price surge drives silver rush: BIS ramps up hallmarking labs across India — Business Today (9 August 2026)","url":"https://www.businesstoday.in/india/story/gold-price-surge-drives-silver-rush-bis-ramps-up-hallmarking-labs-across-india-548176-2026-08-09"},
 {"title":"BIS to scale up silver hallmarking testing as buyers shift from costly gold — Business Standard (9 August 2026)","url":"https://www.business-standard.com/industry/news/bis-to-scale-up-silver-hallmarking-testing-as-buyers-shift-from-costly-gold-126080900171_1.html"},
 {"title":"BIS to Scale Up Silver Jewellery Testing as Hallmarking Demand Rises — The Daily Pioneer (9 August 2026)","url":"https://dailypioneer.com/news/bis-to-scales-up-silver-testing-as-buyers-shift-from-gold"},
 {"title":"India buys fifteen percent less — Carat Capital (31 July 2026)","url":"https://caratcapital.org/a-india-buys-fifteen-percent-less.html"},
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (10 August 2026, 5:57am EST live board)","url":"https://www.kitco.com/price/precious-metals"},
])

# ========== 3. etsy-calls-it-speed ==========
art("etsy-calls-it-speed","retail-tech",False,"Retail & Technology Desk · Marketplaces",5,"The Retail Desk",
["ACTOR","NUM","GAP"],
"Etsy cuts 12% of staff, and calls it speed",
"Etsy is cutting about 220 jobs, roughly 12% of the marketplace workforce, at a $35 million charge, leaving about 1,600 staff. It announced the cut alongside revenue up 6.2% to $668.3 million.",
[
"Etsy is removing about 220 roles, roughly 12% of its marketplace workforce, in a restructuring that falls mainly on the product and engineering organisation. The company put the estimated charge at about $35 million, primarily severance and benefits, booked in the third quarter and completed before the quarter closes. About 1,600 employees remain. The plan was disclosed on 6 August alongside second-quarter results, and the company said explicitly that the cuts are not a cost-reduction exercise and are not related to artificial intelligence.",
"The results it was announced against were not weak ones. Revenue for the quarter was $668.3 million, up 6.2% year on year, against a FactSet consensus of $646.1 million. Gross merchandise sales from continuing operations were $2.58 billion, with Etsy-only gross merchandise sales up 7.5%. The take rate improved to 25.9%. Active sellers grew 5.9% to 5.7 million while active buyers slipped 0.4% to 87.0 million. The reported net loss of $46.7 million is a discontinued-operations figure, carrying $161 million of losses on Depop rather than anything from the core marketplace. Etsy cut its product and engineering bench in a quarter it beat.",
"The reason this belongs on a jewellery desk rather than a technology one is the seller count. Jewellery and personal accessories is one of the six largest categories by gross merchandise sales in Etsy's own filings, and third-party estimates put it near 30% of the platform total, a figure this desk carries as an outside estimate rather than as an Etsy number because Etsy does not publish a category split. Against 5.7 million active sellers, a large share of the world's independent jewellery makers reach their customers through this one company's search ranking, fee schedule and product decisions. Those decisions are now being made by a product and engineering organisation that is materially smaller than it was a week ago.",
"The company's framing is that structure, not headcount, was the problem. Leadership described the goal as \"flatter teams with wider remits, fewer handoffs, and quicker decisions\", and the chief executive, Kruti Patel Goyal, who took the role earlier this year, put it to staff as building an organisation that can move faster. Wedbush read the reduction as supportive of the gross merchandise sales trend rather than a signal of trouble with it. Whether that holds is a question about execution speed on a marketplace where sellers feel every ranking change directly, and it will be visible in the seller count long before it is visible in revenue.",
"The desk's view: a flatter org chart is a bet that coordination, not headcount, was the constraint, and it is a bet a company only makes from a position of some confidence. The figures support the confidence. Gross merchandise sales are growing, the take rate is rising and sellers are still joining. The risk sits on the other side of the ledger and it is specific to makers: 220 people leaving product and engineering means fewer hands on the mechanisms an independent jeweller depends on, and the buyer count has already gone slightly backwards while the seller count climbs. More sellers competing for fewer buyers is a ranking problem before it is anything else. For any maker with meaningful revenue on the platform, the useful action this quarter is to price the risk of a single channel rather than to react to the headline: 5.7 million sellers is the number to hold, not 220."
],
[
 {"title":"Etsy, Inc. Q2 2026 quarterly report (Form 10-Q), quarter ended 30 June 2026 — via StockTitan","url":"https://www.stocktitan.net/sec-filings/ETSY/10-q-etsy-inc-quarterly-earnings-report-775df6d362ca.html"},
 {"title":"Etsy lays off 220 employees, about 12% of its workforce, in a restructuring that mainly hits product and engineering teams — Shopifreaks (6 August 2026)","url":"https://www.shopifreaks.com/etsy-lays-off-220-employees-about-12-of-its-workforce-in-a-restructuring-that-mainly-hits-product-and-engineering-teams/"},
 {"title":"Etsy lays off 12% of workforce as part of restructuring plan — Reuters via Yahoo Finance (5 August 2026)","url":"https://finance.yahoo.com/markets/stocks/articles/etsy-lays-off-12-worker-200744617.html"},
 {"title":"Etsy's Workforce Reduction May Help Sustain Gross Merchandise Sales Uptrend, Wedbush Says — MarketScreener","url":"https://www.marketscreener.com/news/etsy-s-workforce-reduction-may-help-sustain-gross-merchandise-sales-uptrend-wedbush-says-ce7f50d2d180f12d"},
])

# ========== 4. five-billion-in-one-thirteen ==========
art("five-billion-in-one-thirteen","retail-tech",False,"Retail & Technology Desk · Restructuring",5,"The Retail Desk",
["NUM","RECORD","ACTOR"],
"$5 billion of debt, gone in 113 days: QVC exits",
"QVC Group left Chapter 11 on 7 August, 113 days after filing, having cut more than $5 billion of debt. It issued $1.2 billion of 10% notes due 2032 and secured a $600 million facility.",
[
"QVC Group formally emerged from Chapter 11 protection on 7 August, having filed on 16 April. That is 113 days from filing to exit, a count derived by this desk from the two dates, and an unusually fast passage for a company of this size. The restructuring removed more than $5 billion of debt from the balance sheet. The parent of QVC and HSN went into court with a pre-negotiated plan specifically to compress the timetable, and the plan was approved in July before the exit closed last week.",
"The financing that came out the other side is the part worth reading closely. Five billion dollars of debt left the business in 113 days, and $1.2 billion of new paper walked back in at 10%. Those take-back notes, disclosed in a regulatory filing, run to 2032 and carry a 10% coupon, which is what the credit market charges a television retailer emerging from bankruptcy this year. Alongside them sits a $600 million asset-based lending facility, secured against inventory and receivables rather than against the business's prospects. The equity has been approved for trading on Nasdaq under the ticker QVCG.",
"The board and the corner office turned over with the capital structure. David Rawlinson, chief executive since 2021, stepped down at the exit. Mike George, who ran QVC for more than a decade before Rawlinson, returns as interim chief executive and board chair with immediate effect, alongside a new eight-member board appointed by the incoming owners. A company that has just handed control to its creditors bringing back the executive who ran it through its strongest years is a specific statement about which period it intends to imitate.",
"For the jewellery trade the exposure is direct rather than theoretical. Fine and fashion jewellery has been among the top-selling categories on the QVC platform, and for a set of suppliers the network has functioned as a volume channel that no other retail format replicates: long-form demonstration, repeat scheduling and a house diamond-simulant brand with three decades of customer recognition behind it. Alex Hennick, president and chief executive of A.D. Hennick & Associates, said of the exit that \"QVC still has tremendous brand recognition, loyal customers, and strong vendor relationships\". Vendor relationships are the ones that survived the filing; the audience is the one that has been shrinking for years and is the reason for it.",
"The desk's view: a balance sheet can be fixed in four months; a viewing habit cannot. The court process did exactly what it was designed to do, and it did it fast, but nothing in 113 days addresses the structural problem, which is that live television shopping is losing the audience it monetises and the fix requires building a digital business against platforms that started there. The 10% coupon is the honest verdict on the odds, because that is the price of money for this company after the debt was cut by more than $5 billion, and it is the number a supplier should weigh rather than the headline reduction. For anyone with jewellery inventory committed to the channel, the practical read is that the counterparty risk is materially lower than it was in April and the demand risk is exactly where it was."
],
[
 {"title":"QVC Exits Chapter 11 With Focus on 'Innovative Shopping Experiences' — JCK (7 August 2026)","url":"https://www.jckonline.com/editorial-article/qvc-cuts-debt-exits-chapter-11/"},
 {"title":"QVC Group exits Chapter 11, CEO steps down — Retail Dive (August 2026)","url":"https://www.retaildive.com/news/qvc-exits-chapter-11-ceo-steps-down/827314/"},
 {"title":"QVC Issues $1.2 Billion of 10% Yield Debt as It Exits Bankruptcy — Bloomberg (7 August 2026)","url":"https://www.bloomberg.com/news/articles/2026-08-07/qvc-issues-1-2-billion-of-10-yield-debt-as-it-exits-bankruptcy"},
 {"title":"QVC Group Emerges From Bankruptcy With $600 Million Asset-Backed Facility — PYMNTS (August 2026)","url":"https://www.pymnts.com/news/retail/2026/qvc-group-emerges-from-bankruptcy-with-600-million-dollar-asset-backed-facility/"},
])

# ========== 5. pandoras-third-seat ==========
art("pandoras-third-seat","retail-tech",False,"Retail & Technology Desk · Brands",4,"The Retail Desk",
["ACTOR","GAP","STAKES"],
"Pandora's third seat in a year comes from Walmart",
"Paulo Garcia joins Pandora on 1 October and becomes chief financial officer on 1 December, succeeding Anders Boyer after more than 14 years. He arrives from Walmart's $50 billion Mexican and Central American business.",
[
"Pandora named Paulo Garcia as chief financial officer on 6 August. He joins the company on 1 October and takes the role on 1 December, succeeding Anders Boyer, who retires on 30 November after more than fourteen years and stays on until 31 March 2027 to hand over. A two-month overlap before the title changes and a four-month tail afterwards is a long handover by the standards of a listed company, and it is the shape a board uses when it wants continuity rather than a break.",
"The curriculum vitae is the announcement. Garcia is a Portuguese national with twenty-five years of international executive experience and arrives from the chief financial officer's seat at Walmart de Mexico y Centroamerica, a separately listed subsidiary with about $50 billion of revenue and 240,000 employees. Before that he was chief financial officer for Europe and Indonesia at Ahold Delhaize, and before that he was at Unilever. Grocery, discount retail and fast-moving consumer goods, at very large scale, three times over. There is no jewellery on it.",
"That is now a pattern rather than a hire. Three of the top seats turn over inside twelve months at the largest jewellery company in the world by units. Berta de Pablos-Barbier takes office as chief executive on 1 January, arriving from beauty, a move this paper noted on 5 August when the company also named Andre Branch president of its North America cluster. The finance seat completes the set. A jewellery company with about 7,000 points of sale, more than 2,800 concept stores and roughly 39,000 employees on its own published figures is being handed to executives whose track record is in moving volume through large distribution networks.",
"There is a coherent argument for it. Pandora has never really been a jeweller in the trade's sense; it is a charm and silver business that sells enormous quantities at accessible prices, and it now sells lab-grown diamonds in eight markets, having added Spain and Italy in June with flagships in Barcelona and Milan. Read that way, the binding constraints are supply chain, store productivity and price architecture, which is precisely what a Walmart or an Ahold finance chief spends a career on. Read the other way, the company is about to make a series of judgements about materials, provenance and what a diamond is worth, and nobody at the top of it has made those judgements before.",
"The desk's view: Pandora is being rebuilt by people who sell volume, not by people who sell jewellery, and the trade should treat that as information about where the category is going rather than as a comment on the individuals. This is the largest jewellery company in the world deciding that its next problems are retail-operations problems. If it is right, the competitive pressure on independents shifts further away from design and further towards price, availability and store economics, which is the terrain a $50 billion grocery operator knows and a bench jeweller does not. The date to mark is 1 January rather than 1 December. A chief financial officer arriving eight weeks before a new chief executive takes office means the first full budget this company writes will be written by two people who both arrived from somewhere else."
],
[
 {"title":"Pandora appoints Paulo Garcia as new CFO as Anders Boyer will retire — Pandora Group (6 August 2026)","url":"https://www.pandoragroup.com/news/27941"},
 {"title":"Pandora Taps Paulo Garcia as CFO, with Anders Boyer Set to Retire — WWD (6 August 2026)","url":"https://wwd.com/business-news/human-resources/pandora-chief-financial-officer-paulo-garcia-1239095598/"},
 {"title":"Pandora names Paulo Garcia as new CFO, Anders Boyer to retire — FashionUnited (6 August 2026)","url":"https://fashionunited.uk/news/people/pandora-names-paulo-garcia-as-new-cfo-anders-boyer-to-retire/2026080689651"},
 {"title":"Pandora fills the seat — Carat Capital (5 August 2026)","url":"https://caratcapital.org/a-pandora-fills-the-seat.html"},
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

specs["neither-one-is-wrong"] = {
 **strip("By the numbers · Dubai 24-carat gold, 10 August",[
   {"fig":"AED 523.25","lab":"Goodreturns, 24-carat, a gram"},
   {"fig":"AED 512.45","lab":"LivePriceOfGold, same day, same carat"},
   {"fig":"2.11%","delta":"▲","dir":"up","lab":"the gap, derived by this desk"},
   {"fig":"AED 512.59","lab":"peg arithmetic on spot, derived"},
   {"fig":"$4,341.40","lab":"gold spot, Kitco 5:57am EST"}]),
 "figs":[bars("Plate I","Dubai 24-carat gold, 10 August 2026 · dirhams a gram",[
   {"l":"GOODRETURNS","v":523.25,"d":"523.25","hi":True},
   {"l":"PEG ARITHMETIC ON SPOT","v":512.59,"d":"512.59"},
   {"l":"LIVEPRICEOFGOLD","v":512.45,"d":"512.45"}],
   "Both pages read 10 August 2026. The peg line is this desk's arithmetic on Kitco spot at the dirham's fixed 3.6725 rate, published by nobody.",206)],
 "flow":flow5("Two pages, one label, AED 10.80 between them.","The peg arithmetic says which is which.","A step of AED 13 against a metal move of AED 3.",
   "Neither page is wrong. They are not publishing the same quantity","The Gold & Metals Desk",
   "Every metal runs before payrolls","a-every-metal-runs-before-payrolls.html"),
 "desk":{"split":"the number you quote is only as good as the lane it came from"},
 "next":nxt("five-point-nine-million-pieces","Metals","India hallmarked 5.9 million silver articles, nearly double the year before.",
   "nine-thirty-eight-and-twelve-eighty-six","Metals","six-forty-thousand-ounces","Central Banks")}

specs["five-point-nine-million-pieces"] = {
 **strip("By the numbers · Indian silver hallmarking",[
   {"fig":"5.9M","delta":"▲ +84%","dir":"up","lab":"articles hallmarked, FY2025-26"},
   {"fig":"3.2M","lab":"the year before"},
   {"fig":"230","lab":"recognised assay and hallmarking centres"},
   {"fig":"440","lab":"recognised laboratories, from 147 in 2014"},
   {"fig":"Sept 2025","lab":"silver unique identification introduced"}]),
 "figs":[bars("Plate I","Silver articles hallmarked in India · millions of pieces",[
   {"l":"FY 2025-26","v":5.9,"d":"5.9M","hi":True},
   {"l":"FY 2024-25","v":3.2,"d":"3.2M"}],
   "Bureau of Indian Standards figures disclosed 9 August 2026. The 84% increase is derived by this desk from the two published counts.",207)],
 "flow":flow5("Nearly double in a single financial year.","230 centres, and a two-year build behind them.","A count of finished articles, not of intent.",
   "The assay office is where a substitution stops being anecdote and becomes volume","The Gold & Metals Desk",
   "India buys fifteen percent less","a-india-buys-fifteen-percent-less.html"),
 "desk":{"split":"hallmarking capacity is the least glamorous leading indicator in the metals trade"},
 "next":nxt("etsy-calls-it-speed","Retail","Etsy is cutting 220 jobs from product and engineering in a quarter it beat.",
   "forty-six-percent-came-back","Retail","india-buys-fifteen-percent-less","Demand")}

specs["etsy-calls-it-speed"] = {
 **strip("By the numbers · Etsy, quarter to 30 June",[
   {"fig":"220","delta":"▼ −12%","dir":"down","lab":"roles cut, marketplace workforce"},
   {"fig":"$35M","lab":"restructuring charge, third quarter"},
   {"fig":"$668.3M","delta":"▲ +6.2%","dir":"up","lab":"revenue"},
   {"fig":"$2.58B","lab":"GMS, continuing operations"},
   {"fig":"5.7M","delta":"▲ +5.9%","dir":"up","lab":"active sellers"}]),
 "figs":[bars("Plate I","Etsy, second quarter 2026 · per cent year on year",[
   {"l":"ETSY-ONLY GMS","v":7.5,"d":"+7.5%","hi":True},
   {"l":"REVENUE","v":6.2,"d":"+6.2%"},
   {"l":"ACTIVE SELLERS","v":5.9,"d":"+5.9%"},
   {"l":"ACTIVE BUYERS","v":-0.4,"d":"−0.4%"}],
   "Etsy's Q2 2026 quarterly report, quarter ended 30 June 2026. Take rate 25.9%; restructuring charge booked in the third quarter.",208)],
 "flow":flow5("220 roles out of product and engineering.","A beat, and a cut announced the same day.","5.7 million sellers on one company's decisions.",
   "Etsy cut its product and engineering bench in a quarter it beat","The Retail Desk",
   "Sixty-seven percent asked a chatbot","a-sixty-seven-percent-asked-a-chatbot.html"),
 "desk":{"split":"a flatter org chart is a bet that coordination, not headcount, was the constraint"},
 "next":nxt("five-billion-in-one-thirteen","Retail","QVC left Chapter 11 in 113 days, having cut more than $5 billion of debt.",
   "sixty-seven-percent-asked-a-chatbot","Retail","the-storefront-that-isnt","Retail")}

specs["five-billion-in-one-thirteen"] = {
 **strip("By the numbers · QVC Group's Chapter 11 exit",[
   {"fig":"113","lab":"days from filing to exit, derived"},
   {"fig":">$5B","delta":"▼","dir":"down","lab":"debt removed"},
   {"fig":"$1.2B","lab":"take-back notes issued, due 2032"},
   {"fig":"10%","lab":"coupon on the new paper"},
   {"fig":"$600M","lab":"asset-based lending facility"}]),
 "figs":[bars("Plate I","QVC Group · the exit in numbers, dollars billion",[
   {"l":"DEBT REMOVED","v":5.0,"d":">$5.0B","hi":True},
   {"l":"TAKE-BACK NOTES ISSUED","v":1.2,"d":"$1.2B"},
   {"l":"ASSET-BASED FACILITY","v":0.6,"d":"$0.6B"}],
   "Filed 16 April 2026, exited 7 August 2026. The 113-day count is derived by this desk from the two dates.",209)],
 "flow":flow5("113 days from filing to exit.","Five billion out, 1.2 billion back in at 10%.","The channel the jewellery suppliers sell through.",
   "Five billion dollars of debt left the business in 113 days","The Retail Desk",
   "$934 for 117: the mall anchors change hands","a-nine-thirty-four-for-one-seventeen.html"),
 "desk":{"split":"a balance sheet can be fixed in four months; a viewing habit cannot"},
 "next":nxt("pandoras-third-seat","Retail","Pandora's incoming finance chief arrives from Walmart's Mexican business.",
   "nine-thirty-four-for-one-seventeen","Retail","bnpl-inside-the-perimeter","Retail")}

specs["pandoras-third-seat"] = {
 **strip("By the numbers · Pandora's executive bench",[
   {"fig":"1 Dec","lab":"Paulo Garcia becomes chief financial officer"},
   {"fig":"14 yrs","lab":"Anders Boyer's tenure, retiring 30 November"},
   {"fig":"$50B","lab":"revenue at Garcia's last employer, Walmex"},
   {"fig":"3","lab":"top seats turning over in twelve months"},
   {"fig":"≈7,000","lab":"Pandora points of sale worldwide"}]),
 "figs":[bars("Plate I","Pandora's three incoming seats · month the role begins, 2026-27",[
   {"l":"NORTH AMERICA PRESIDENT","v":8,"d":"Aug 2026"},
   {"l":"CHIEF FINANCIAL OFFICER","v":12,"d":"Dec 2026"},
   {"l":"CHIEF EXECUTIVE","v":13,"d":"Jan 2027","hi":True}],
   "Company announcements of 5 and 6 August 2026 and the previously announced chief executive transition. Bar length marks the month the role begins.",210)],
 "flow":flow5("A long handover, deliberately built.","Grocery, discount retail and consumer goods.","Three seats, none of them from jewellery.",
   "Three of the top seats turn over inside twelve months","The Retail Desk",
   "Pandora fills the seat","a-pandora-fills-the-seat.html"),
 "desk":{"split":"Pandora is being rebuilt by people who sell volume, not by people who sell jewellery"},
 "next":nxt("neither-one-is-wrong","Metals","Two Dubai gold pages read 2% apart this morning, and neither is wrong.",
   "pandora-fills-the-seat","Retail","luk-fook-fixed-price","Retail")}

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

articles = NEW + articles
for s in specs: editorial[s] = specs[s]
(C/"articles.json").write_text(json.dumps(articles, ensure_ascii=False, indent=1))
(C/"editorial.json").write_text(json.dumps(editorial, ensure_ascii=False, indent=1))
print("OK: %d articles prepended, %d specs written, total %d" % (len(NEW), len(specs), len(articles)))
