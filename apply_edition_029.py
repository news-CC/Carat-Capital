#!/usr/bin/env python3
# Edition No. 029 - 2026-08-08. Prepends 6 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-08"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - the-hundred-six-thousand-miss ==========
art("the-hundred-six-thousand-miss","gold-metals",True,"Lead Story · Gold & Metals Desk",5,"The Gold & Metals Desk",
["GAP","NUM","STAKES"],
"The 106,000 jobs that weren't: payrolls miss puts gold at $4,341.30",
"July payrolls fell 23,000 against a consensus of about 83,000, a miss of 106,000. Gold closed Friday at $4,341.30, up $102.00 or 2.41%. September hike odds fell to 46% from 55% on the print.",
[
"American payrolls did not slow in July. They went backwards. The Bureau of Labor Statistics reported total non-farm employment down 23,000 for the month against a consensus of roughly 83,000 jobs added, and revised June to a loss of 20,000. A miss of 106,000 jobs is not a soft month; it is a different labour market. The unemployment rate edged down to 4.1%, which sounds like a contradiction until the participation rate is read alongside it: 61.4%, the lowest in more than five years. The rate fell because people left, not because they were hired. Average hourly earnings rose two cents on the month and annual wage growth slowed to 3.2%.",
"The metal took it straight. Kitco's spot page closed Friday at 5:00pm New York with gold bid $4,341.30 an ounce, up $102.00 or 2.41% against Thursday's close; silver $63.46, up $2.06 or 3.36%; platinum $1,743.00, up $25.00 or 1.46%; palladium $1,357.00, up $4.00 or 0.30%. Fine gold at that level is $139.58 a gram against $138.72 on Friday morning. Outside sources do not agree on the exact mark and this desk will not pretend otherwise: Trading Economics carried $4,343.43 for 7 August, $2.13 above the Kitco close, and Reuters reporting during the session had spot near $4,356 at its intraday best, some fifteen dollars above where it settled. This paper carries the Kitco close because it is a stated closing print at a stated time.",
"What the print actually moved was the rate path. The CME FedWatch tool had the probability of a September hike at 46% immediately after the release, down from 55% before it; this paper carried 56.9% on Friday morning, and the whole of that decline arrived in the eight-thirty release. A hike being priced out is not the same as a cut being priced in, and the distinction is the reason gold added two and a half percent rather than five. Ellen Zentner of Morgan Stanley Wealth Management put the caveat where it belongs, saying \"next week's inflation data will still likely be the deciding factor\". Consumer prices land next week, and a hot print reverses most of Friday afternoon.",
"For anyone who buys metal by weight rather than by contract, the number that matters is $139.58 a gram. Ten grams of 18-carat gold, three quarters fine, now carries $1,046.85 of metal before a bench touches it. Across the three sessions this paper has marked since Wednesday, gold has added $183.00 an ounce or 4.40%, and a manufacturer who quoted a customer on Wednesday morning and buys the metal on Monday is short that difference. The trade has spent this week watching a jobs report it cannot influence set the cost of its raw material for the quarter.",
"The desk's view: a jeweller cannot hedge a payrolls print, but can hedge a gram, and the gap between those two sentences is the whole of this week's lesson. Gold at $4,341.30 is no longer trading on the Hormuz headlines that carried it through July; it is trading on a labour market that produced a negative month and a participation rate at a five-year low, which is a slower, heavier and far more durable driver than a shipping lane. That matters for planning because geopolitical premium comes off in a day and macro repricing does not. The practical instruction for a fabricator is to stop quoting forward on spot and start quoting on a metal-plus basis, because the next two prints, inflation next week and the September decision after it, will move this number again before most order books clear."
],
[
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (7 August 2026, 5:00pm EST close)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Nonfarm Payrolls Fall by 23,000 in July as Dollar Sinks and Gold Gains — Brisk Markets (7 August 2026)","url":"https://www.briskmarkets.com/blog/nonfarm-payrolls-fall-by-23000-in-july-as-dollar-sinks-and-gold-gains/"},
 {"title":"Odds the Fed will hike in September tumble following big July jobs miss — CNBC (7 August 2026)","url":"https://www.cnbc.com/2026/08/07/odds-the-fed-hikes-in-september-tumble-following-big-july-jobs-miss.html"},
 {"title":"Gold hits seven-week high as weak U.S. jobs data dents rate hike bets — CNBC (7 August 2026)","url":"https://www.cnbc.com/2026/08/07/gold-heads-for-best-week-since-january-us-jobs-data-in-focus.html"},
 {"title":"Gold — commodity price and summary, 7 August 2026 — Trading Economics","url":"https://tradingeconomics.com/commodity/gold"},
])

# ========== 2. gold-kept-it-the-rest-gave-it-back ==========
art("gold-kept-it-the-rest-gave-it-back","gold-metals",False,"Gold & Metals Desk · The Tape",4,"The Gold & Metals Desk",
["NUM","VS"],
"Gold kept $26.80, platinum gave back $29.00: the settle against the spike",
"This paper marked all four metals at 5:58am on Friday. By the 5:00pm close gold had added a further $26.80, while platinum gave back $29.00, palladium $25.00 and silver $0.83. Only gold improved on its morning mark.",
[
"Carat Capital printed four metals at 5:58am New York on Friday, an hour and a half before the payrolls release. The close, eleven hours later, disagreed with three of them. Gold was marked at $4,314.50 in the morning and settled at $4,341.30, adding a further $26.80. Silver was marked at $64.29 and settled at $63.46, giving back $0.83. Platinum was marked at $1,772.00 and settled at $1,743.00, giving back $29.00. Palladium was marked at $1,382.00 and settled at $1,357.00, giving back $25.00. Both readings come from the same Kitco spot page at two stated times, and both were correct when taken.",
"In percentage terms the reversal is sharper than the dollars suggest. Platinum was up 3.14% on the session at the morning mark and closed up 1.46%, surrendering more than half its gain. Palladium was up 2.14% and closed up 0.30%, surrendering almost all of it. Silver was up 4.71% and closed up 3.36%. Gold alone went the other way, up 1.77% in the morning and 2.41% at the close. One number was bought in gold and sold in the white metals, in the same session, which is the cleanest split this tape has printed in a fortnight.",
"The ratio records it. Gold to silver stood at 69.04 on Thursday's close, tightened to 67.11 by Friday morning as silver ran, then widened back to 68.41 by the close as silver faded and gold did not. Platinum told the same story against the same benchmark: 41.1% of the gold price at the morning mark, 40.15% at the close. A white metal that cannot hold its ratio through an afternoon in which gold rises is a metal being traded on industrial demand rather than on monetary fear, and Friday's news was monetary.",
"Set against the marks this paper carried on Wednesday, the three-session picture is starker still. Gold has added $183.00 an ounce, or 4.40%. Silver has added $2.16, or 3.52%. Palladium has added $7.00, or 0.52%. Platinum has added $2.00, or 0.11%, which after three sessions and a jobs report is indistinguishable from standing still. The white metals went along for Thursday and Friday morning and were sold back to roughly where they started.",
"The desk's view: a rally the industrial metals will not follow is a monetary rally, and it should be planned for as one. Platinum's inability to keep eleven hundredths of a per cent over three sessions in which gold took four and a half is the tell, because platinum's demand base is autocatalysts and fabrication rather than reserve buying, and neither of those changes because American payrolls printed negative. For the bench this is good news in one narrow sense: the platinum-to-gold ratio has widened again, and a platinum band is once more costing about forty per cent of the gold equivalent in metal. For the tape it is a warning that the week's move has one buyer behind it, not four."
],
[
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (7 August 2026, 5:00pm EST close)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"$4,314.50 and silver up 4.71%: every metal runs before payrolls — Carat Capital (7 August 2026)","url":"https://caratcapital.org/a-every-metal-runs-before-payrolls.html"},
 {"title":"Nonfarm Payrolls Fall by 23,000 in July as Dollar Sinks and Gold Gains — Brisk Markets (7 August 2026)","url":"https://www.briskmarkets.com/blog/nonfarm-payrolls-fall-by-23000-in-july-as-dollar-sinks-and-gold-gains/"},
])

# ========== 3. thirteen-thousand-for-costume ==========
art("thirteen-thousand-for-costume","auctions",False,"Auctions Desk · Calendar",4,"The Auctions Desk",
["NUM","VS","ACTOR"],
"$13,000 for costume, £2,000 for gold: Bonhams runs Chanel in three cities",
"Bonhams will hold three Chanel sales in September: New York 7 to 17, Paris 14 to 24 with about 400 lots, London 21 September to 1 October. The top jewellery lot is a 1960 Goossens bangle at $13,000 to $20,000.",
[
"Bonhams has put three Chanel sales on the September calendar across three cities. New York runs Chanel: From the Vault II from 7 to 17 September, with highlights on view at the house's Manhattan flagship from 17 August. Paris follows with Chanel: From the Vault II Paris Edition from 14 to 24 September, carrying roughly 400 lots spanning Karl Lagerfeld's nineties work through Virginie Viard's more recent collections. London closes the sequence with Designer Handbags and Fashion from 21 September to 1 October. Three sales, one house, one name, staged consecutively rather than concurrently.",
"London is the sale that concerns this desk, because it skews heaviest toward jewellery. It carries a private collection of Chanel costume pieces dating from the 1960s through the 1990s, led by a filigree snake bangle made by Robert Goossens for Chanel Haute Couture around 1960, estimated at $13,000 to $20,000. In the same sale sits a pair of Chanel Fine Jewelry Comète Géode earrings from 2024 in 18-carat white gold and diamonds, estimated at £2,000 to £3,000, or about $2,690 to $4,040. A signed 1960 costume bangle carries roughly five times the estimate of 2024 gold and diamonds.",
"The rest of the series is priced as a volume business rather than a trophy one. New York leads with a gold-tone bird cage minaudière from Viard's Métiers d'Art Paris-31 rue Cambon collection, set with simulated turquoise and multicoloured crystals, at $20,000 to $30,000. Paris leads with a white tweed jacket from the autumn/winter 2025 ready-to-wear collection at €2,000 to €3,000, about $2,300 to $3,460, and includes a Lagerfeld-era brooch with rhinestones and turquoise-coloured paste at €700 to €900, roughly $810 to $1,040. Four hundred lots at those levels is a sale designed to clear inventory to a wide bidder base, not to set a record.",
"For a paper that has watched the auction calendar thin out through July and August, the value of this is the calendar itself. It is the first substantial house announcement this desk has been able to file in three editions, and it marks the point at which the autumn season starts taking shape. It also fits a pattern this desk recorded at Bonhams earlier in the year, when the house doubled its low estimate on a Piaget sale by leaning on a single named maker rather than on stone weight.",
"The desk's view: the signature is the material, and Bonhams has priced this series as though it knows that better than most of the trade does. A dealer looking at these three catalogues should read the London estimates twice, because a house is publicly stating that a documented Goossens for Chanel, in base metal and paste, is worth several times a current-production 18-carat and diamond earring from the same maison. That is a provenance market, not a materials market, and it prices attribution, date and documentation rather than carat weight. The practical instruction for anyone buying in September is that the paperwork is the asset, and a piece with an uncertain attribution in this category is not cheap, it is unsaleable."
],
[
 {"title":"Bonhams Marks Chanel's Legacy With Three-City Auction Blitz This September — JCK (7 August 2026)","url":"https://www.jckonline.com/editorial-article/bonhams-chanel-sales/"},
 {"title":"Bonhams Sets a Trio of Chanel Sales for September, in New York, Paris and London — WWD","url":"https://wwd.com/fashion-news/fashion-features/bonhams-trio-chanel-sales-september-new-york-paris-london-1239093114/"},
 {"title":"Bonhams — Jewellery department","url":"https://www.bonhams.com/department/JWL/jewellery/"},
])

# ========== 4. twenty-nine-said-diamond ==========
art("twenty-nine-said-diamond","retail-tech",False,"Retail & Technology Desk · Trade Shows",4,"The Retail Desk",
["VS","NUM"],
"29% said diamond, 57% said fashion jewellery: Hong Kong's two answers",
"HKTDC surveyed 1,507 buyers and exhibitors at its twin Hong Kong shows, 29 July to 2 August. Diamond led demand at 29%, ruby 25%, pearl 20%. Trendy fashion jewellery led growth potential at 57%, precious jewellery 35%.",
[
"The Hong Kong Trade Development Council closed its twin jewellery fairs on 2 August and published what the floor told it. The Hong Kong International Jewellery Show and the Hong Kong International Diamond, Gem and Pearl Show ran together from 29 July at the Hong Kong Convention and Exhibition Centre, and the council surveyed 1,507 buyers and exhibitors across both. Asked which stone was most in demand, 29% said diamond, ahead of ruby at 25% and pearl at 20%. On a floor that has spent two years being told colour is taking the counter, the diamond still leads the demand question.",
"Asked a different question, the same floor gave a different answer. On growth potential, 57% named trendy fashion jewellery, 35% precious jewellery and 21% designer jewellery. The stone they are asked about and the product they expect to sell are not the same thing, and the twenty-eight point gap between fashion jewellery and precious is the widest signal in the survey. A diamond leads the demand question because buyers are asked about stones. Fashion jewellery leads the growth question because buyers are asked about volume, and volume is where the margin is being defended.",
"The metal answer sharpens it. Yellow gold was named the most popular precious metal by 40% of respondents, in a week that ended with gold closing at $4,341.30 an ounce, $139.58 a gram. The metal the trade says it wants is the one that has repriced hardest against it. This paper filed China Gold Association half-year figures on Friday showing Chinese gold jewellery consumption down 33.88% by weight while bar and coin demand rose 28.42%, and the Hong Kong answer sits on the same fault line: the appetite for yellow gold is intact, the ability to sell it by weight is not.",
"On timing, respondents were cautious rather than pessimistic, telling the council they expect one to two years before confidence is fully restored. Hong Kong's own trade data gives that estimate a base to work from. In 2025 the territory's exports of fine jewellery rose 5%, carried by precious metal prices rather than by units; exports of pearls, gemstones and rough diamonds fell 8%; and exports of imitation jewellery fell 26%. A market whose fine jewellery line is rising on metal value while its stone line falls is not recovering yet, it is revaluing.",
"The desk's view: demand surveys measure what a buyer admires; order books measure what a buyer risks, and the two answers in this survey are the gap between them. A retailer reading only the 29% diamond figure will over-buy stones for a floor whose growth respondents put in fashion jewellery at 57%, and will discover the mismatch at the November reorder. The useful reading is the pairing rather than either number alone: buy the diamond for the window and the fashion piece for the till, because that is precisely what 1,507 people in Wan Chai just described themselves doing. The one to two year confidence horizon is the honest part of this survey, and it should be planned for rather than argued with."
],
[
 {"title":"Diamonds Lead Trends at Hong Kong Shows — Rapaport (2 August 2026)","url":"https://rapaport.com/news/diamonds-lead-trends-at-hong-kong-shows/"},
 {"title":"Hong Kong International Jewellery Show and International Diamond, Gem & Pearl Show open at end of July — HKTDC Media Room","url":"https://mediaroom.hktdc.com/en/pressrelease/detail/20362/"},
 {"title":"HKTDC Hong Kong International Jewellery Show — Fair at a Glance","url":"https://www.hktdc.com/event/hkjewellery/en/fair-at-a-glance"},
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (7 August 2026, 5:00pm EST close)","url":"https://www.kitco.com/price/precious-metals"},
])

# ========== 5. the-fifteen-hundred-line ==========
art("the-fifteen-hundred-line","retail-tech",False,"Retail & Technology Desk · Demand",4,"The Retail Desk",
["NUM","STAKES","HOWTO"],
"Up 8.6% in dollars, down in units: the $1,500 line splits the counter",
"Tenoris data puts US jewellery sales up 8.6% in the first half on a 19% rise in average purchase price and a fall in units. Sales below $1,500 kept declining. June sales rose 13% year on year.",
[
"American jewellery had a good first half in dollars and a bad one in pieces. Figures from the analytics firm Tenoris, reported by JCK on 5 August, put jewellery sales up 8.6% across the first six months of 2026 while the average purchase price rose 19% and unit sales fell. June alone was up 13% year on year. Underneath the headline, sales of items below $1,500 continued to decline, which is the same threshold the trade has been watching slip since the spring.",
"The arithmetic is worth doing explicitly, because the two published numbers imply a third. Value up 8.6% on a ticket up 19% means unit count fell by roughly 9%. An eight percent gain in dollars sitting on a nine percent fall in units is not growth, it is a smaller number of larger transactions being counted as a larger business. That distinction decides whether a retailer adds staff or adds inventory value, and most of the trade's half-year reporting has quietly presented the first figure without the second.",
"The composition behind it is a spending distribution, not a jewellery trend. The New York Times has the top 10% of American households accounting for nearly half of all consumer spending, and a category priced in discretionary dollars inherits that shape directly. De Beers chief executive Al Cook, speaking at the JCK show, put the industry read plainly: \"I think the larger, higher-quality diamonds are really growing in value and in desire.\" The counterpart to that sentence is a mid-market whose customer has not left but has stopped trading up, and whose transactions now sit below the threshold at which value growth registers.",
"This paper has filed the same shape from three separate companies in the past fortnight. Brilliant Earth reported second-quarter revenue up 6% on total orders down 2.1%, with average order value up 8% to $2,238. Richemont's quarter to 30 June carried jewellery up 24% inside total sales up 20%, a seventh consecutive quarter of double-digit jewellery growth. Luk Fook took a record profit out of fixed-price design rather than gram weight. Four data sets, one mechanism: the ticket is carrying everything and the unit count is carrying nothing.",
"The desk's view: the growth is in the ticket, and a ticket can be withdrawn faster than a customer, which is the risk nobody is pricing. A shop that has replaced nine per cent of its units with nineteen per cent of ticket has concentrated its year into fewer decisions by fewer people, and if the top decile trims discretionary spending by even a modest amount the fall lands on a base with no volume beneath it to absorb the shock. The practical instruction is to defend the sub-$1,500 line rather than abandon it, because that is where the next decade's high-ticket customer is currently making their first purchase, and a floor that has stopped stocking it has stopped recruiting."
],
[
 {"title":"Riding the K-Shaped Market — JCK, Victoria Gomelsky (5 August 2026)","url":"https://www.jckonline.com/editorial-article/trends-k-shaped-market/"},
 {"title":"$2,238 an order: Brilliant Earth turns a profit on fewer orders — Carat Capital (7 August 2026)","url":"https://caratcapital.org/a-twenty-two-thirty-eight-an-order.html"},
 {"title":"Tenoris — jewellery retail sales analytics","url":"https://tenoris.bi/"},
])

# ========== 6. ninety-six-percent-rebooked ==========
art("ninety-six-percent-rebooked","retail-tech",False,"Retail & Technology Desk · Trade Shows",4,"The Retail Desk",
["ACTOR","NUM"],
"Buyers up 5%, 96% already rebooked: Rockview's first NY Now",
"NY Now's summer edition ran 2 to 4 August at the Javits Center with 460 exhibitors, the first under Rockview Management Group. Buyer attendance rose 5% and 96% of exhibitors have renewed for the 31 January winter show.",
[
"NY Now closed its summer edition on 4 August, and the first show under new ownership finished ahead of the last one under the old. The market ran from 2 to 4 August at the Jacob K. Javits Center in New York with 460 exhibitors, more than 70 of them either new to the show or returning after an absence, across its Gift and Lifestyle, Jewelry and Accessories, and Home sections. Buyer attendance was up 5% on the previous summer edition. This paper opened the show on 2 August; this is what it closed at.",
"The harder number is the rebooking. Organisers report a 96% renewal rate for the winter 2027 market, and say 107 prospective exhibitors walked the summer floor to assess taking space. A 96% renewal is a harder number than an attendance figure, because it is paid. Attendance counts people who came through a door that was free to them; renewal counts companies that have signed for stand space eighteen weeks before they will use it, which is the only trade-show statistic that carries a cash commitment behind it.",
"The ownership context explains why the figures were published at all. NY Now and JA New York were sold by Emerald before that company's own acquisition by Apollo, and were bought by Rockview Management Group, which has put the industry veteran Dorothy Belshaw in charge. A new owner's first edition is the one where the numbers get disclosed, because the disclosure is the pitch to next season's exhibitors. The winter 2027 market is set for 31 January to 2 February.",
"For the jewellery trade specifically the read is narrower than the headline. NY Now is a gift and home market with a jewellery and accessories hall inside it, not a jewellery fair, and neither the attendance rise nor the renewal rate is broken out by section. What a jewellery exhibitor can take from it is that the buyer base for independent design at the low-to-middle price point turned up in slightly greater numbers this year than last, in the same week that this desk filed a survey from Hong Kong putting fashion jewellery at the top of the growth question.",
"The desk's view: a renewal rate is the only trade-show statistic a buyer should trust, and 96% is a genuinely strong one that deserves a caveat rather than a discount. The caveat is that renewal was measured in the week of the show, when goodwill is highest and the winter deadline is distant, and the number that will matter is how many of those 96% are still on the floor plan in December. The signal worth acting on is the 107 prospects: companies that paid to walk a floor they do not yet sell on are the leading indicator for a market, and a show adding prospective exhibitors while raising buyer traffic has stopped shrinking. For a jewellery brand at this price tier, winter 2027 is now a show worth costing out."
],
[
 {"title":"NY Now's Summer Show Saw Increased Traffic, Momentum for Winter Edition — Gifts & Decorative Accessories (5 August 2026)","url":"https://www.giftsanddec.com/ny-now/ny-nows-summer-show-saw-increased-traffic-momentum-for-winter-edition/"},
 {"title":"NY Now Returns in August Under New Ownership — National Jeweler","url":"https://nationaljeweler.com/articles/15155-ny-now-returns-in-august-under-new-ownership"},
 {"title":"New York Show — Winter & Summer 2026 dates — NY NOW","url":"https://nynow.com/market/"},
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

specs["the-hundred-six-thousand-miss"] = {
 **strip("By the numbers · US July employment and the Friday close",[
   {"fig":"−23,000","delta":"▼","dir":"down","lab":"July payrolls, against ~+83,000 expected"},
   {"fig":"61.4%","delta":"▼","dir":"down","lab":"participation, five-year low"},
   {"fig":"$4,341.30","delta":"▲ +2.41%","dir":"up","lab":"gold, Kitco 5pm close"},
   {"fig":"46%","delta":"▼ from 55%","dir":"down","lab":"September hike odds, CME FedWatch"},
   {"fig":"$139.58","lab":"fine gold, a gram"}]),
 "figs":[bars("Plate I","US non-farm payrolls · thousands of jobs",[
   {"l":"JULY, CONSENSUS","v":83,"d":"+83,000"},
   {"l":"JUNE, REVISED","v":-20,"d":"−20,000"},
   {"l":"JULY, ACTUAL","v":-23,"d":"−23,000","hi":True}],
   "Thousands of jobs. Bureau of Labor Statistics release, 7 August 2026, as reported; the BLS release page returned 403 to this desk.",194)],
 "flow":flow5("A negative month, and a five-year low.","What it did to the rate path.","The cost, priced by the gram.",
   "A miss of 106,000 jobs is not a soft month; it is a different labour market.","The Gold & Metals Desk",
   "$4,314.50 and silver up 4.71%: every metal runs before payrolls","a-every-metal-runs-before-payrolls.html"),
 "desk":{"split":"a jeweller cannot hedge a payrolls print, but can hedge a gram"},
 "next":nxt("gold-kept-it-the-rest-gave-it-back","Metals","Gold added $26.80 after the morning mark; platinum gave back $29.00.",
   "every-metal-runs-before-payrolls","Metals","silver-alone-in-the-red","Silver")}

specs["gold-kept-it-the-rest-gave-it-back"] = {
 **strip("By the numbers · 5:58am mark against the 5:00pm close, 7 August",[
   {"fig":"+$26.80","delta":"▲","dir":"up","lab":"gold, added after the mark"},
   {"fig":"−$29.00","delta":"▼","dir":"down","lab":"platinum, given back"},
   {"fig":"−$25.00","delta":"▼","dir":"down","lab":"palladium, given back"},
   {"fig":"−$0.83","delta":"▼","dir":"down","lab":"silver, given back"},
   {"fig":"68.41","lab":"gold to silver at the close, from 67.11"}]),
 "figs":[bars("Plate I","Change between the morning mark and the close · percentage points",[
   {"l":"GOLD","v":0.64,"d":"+0.64 pts"},
   {"l":"SILVER","v":-1.35,"d":"−1.35 pts"},
   {"l":"PLATINUM","v":-1.68,"d":"−1.68 pts"},
   {"l":"PALLADIUM","v":-1.84,"d":"−1.84 pts","hi":True}],
   "Session percentage change at 5:58am against session percentage change at the 5:00pm close. Kitco spot, 7 August 2026.",195)],
 "flow":flow5("Two marks, eleven hours apart.","The split, in percentage points.","Three sessions, one metal.",
   "One number was bought in gold and sold in the white metals, in the same session","The Gold & Metals Desk",
   "Silver alone in the red","a-silver-alone-in-the-red.html"),
 "desk":{"split":"a rally the industrial metals will not follow is a monetary rally"},
 "next":nxt("the-hundred-six-thousand-miss","Metals","Payrolls fell 23,000 against a consensus of 83,000, and gold closed at $4,341.30.",
   "platinum-adds-one-seven","Platinum","three-metals-one-direction","Tape")}

specs["thirteen-thousand-for-costume"] = {
 **strip("By the numbers · Bonhams Chanel series, September 2026",[
   {"fig":"3","lab":"sales: New York, Paris, London"},
   {"fig":"~400","lab":"lots, Paris edition"},
   {"fig":"$13–20k","lab":"Goossens bangle, circa 1960"},
   {"fig":"£2–3k","lab":"18kt and diamond Comète earrings, 2024"},
   {"fig":"17 Aug","lab":"New York highlights on view"}]),
 "figs":[bars("Plate I","High estimate by lot · Bonhams Chanel series (USD)",[
   {"l":"MINAUDIÈRE, NEW YORK","v":30000,"d":"$30,000"},
   {"l":"GOOSSENS BANGLE, LONDON","v":20000,"d":"$20,000","hi":True},
   {"l":"COMÈTE GÉODE EARRINGS, LONDON","v":4040,"d":"~$4,040"},
   {"l":"TWEED JACKET, PARIS","v":3460,"d":"~$3,460"},
   {"l":"LAGERFELD BROOCH, PARIS","v":1040,"d":"~$1,040"}],
   "Upper estimate as published, euro and sterling converted at the rates given by the house. JCK, 7 August 2026.",196)],
 "flow":flow5("Three cities, one name.","Where the jewellery sits.","Priced as volume, not trophy.",
   "A signed 1960 costume bangle carries roughly five times the estimate of 2024 gold and diamonds.","The Auctions Desk",
   "Piaget doubles at Bonhams","a-piaget-doubles-at-bonhams.html"),
 "desk":{"split":"the signature is the material"},
 "next":nxt("twenty-nine-said-diamond","Retail","1,507 buyers in Hong Kong put diamond first and fashion jewellery ahead of it.",
   "seventy-three-lots-over-a-million","Auctions","joopiter-keeping-measure","Auctions")}

specs["twenty-nine-said-diamond"] = {
 **strip("By the numbers · HKTDC survey, 1,507 buyers and exhibitors",[
   {"fig":"29%","lab":"diamond, most in demand"},
   {"fig":"25%","lab":"ruby"},
   {"fig":"20%","lab":"pearl"},
   {"fig":"57%","lab":"trendy fashion jewellery, growth potential"},
   {"fig":"40%","lab":"yellow gold, preferred metal"}]),
 "figs":[bars("Plate I","Most in-demand stone · HKTDC survey, twin Hong Kong shows",[
   {"l":"DIAMOND","v":29,"d":"29%","hi":True},
   {"l":"RUBY","v":25,"d":"25%"},
   {"l":"PEARL","v":20,"d":"20%"}],
   "Per cent of 1,507 buyers and exhibitors surveyed at the two shows, 29 July to 2 August 2026. HKTDC via Rapaport.",197)],
 "flow":flow5("The demand question.","The growth question.","The metal, and the horizon.",
   "The stone they are asked about and the product they expect to sell are not the same thing","The Retail Desk",
   "Hong Kong jewellery posts a fourteen-month high","a-hong-kong-fourteen-months.html"),
 "desk":{"split":"demand surveys measure what a buyer admires; order books measure what a buyer risks"},
 "next":nxt("the-fifteen-hundred-line","Retail","US jewellery value rose 8.6% on a unit count that fell about 9%.",
   "hong-kong-fourteen-months","Hong Kong","one-thirty-two-against-three-thirty-nine","China")}

specs["the-fifteen-hundred-line"] = {
 **strip("By the numbers · US jewellery, first half 2026 (Tenoris)",[
   {"fig":"+8.6%","delta":"▲","dir":"up","lab":"sales value, first half"},
   {"fig":"+19%","delta":"▲","dir":"up","lab":"average purchase price"},
   {"fig":"≈ −9%","delta":"▼","dir":"down","lab":"units, derived"},
   {"fig":"+13%","delta":"▲","dir":"up","lab":"June sales, year on year"},
   {"fig":"$1,500","lab":"the line below which sales kept falling"}]),
 "figs":[bars("Plate I","US jewellery, first half 2026 · per cent year on year",[
   {"l":"AVERAGE PURCHASE PRICE","v":19,"d":"+19%"},
   {"l":"SALES VALUE","v":8.6,"d":"+8.6%"},
   {"l":"UNITS (DERIVED)","v":-9,"d":"≈ −9%","hi":True}],
   "Tenoris figures via JCK, 5 August 2026. The unit change is derived by this desk from the published value and average-price figures, not published as such.",198)],
 "flow":flow5("Dollars up, pieces down.","The third number nobody printed.","One mechanism, four companies.",
   "An eight percent gain in dollars sitting on a nine percent fall in units is not growth","The Retail Desk",
   "$2,238 an order: Brilliant Earth turns a profit on fewer orders","a-twenty-two-thirty-eight-an-order.html"),
 "desk":{"split":"the growth is in the ticket, and a ticket can be withdrawn faster than a customer"},
 "next":nxt("ninety-six-percent-rebooked","Retail","NY Now closed its first edition under new ownership with buyers up 5%.",
   "twenty-two-thirty-eight-an-order","Retail","average-ticket-carries-the-half","Demand")}

specs["ninety-six-percent-rebooked"] = {
 **strip("By the numbers · NY Now summer market, 2 to 4 August",[
   {"fig":"460","lab":"exhibitors, Javits Center"},
   {"fig":"+5%","delta":"▲","dir":"up","lab":"buyer attendance, year on year"},
   {"fig":"96%","lab":"renewal rate, winter 2027"},
   {"fig":"107","lab":"prospective exhibitors walking the floor"},
   {"fig":"31 Jan","lab":"winter 2027 market opens"}]),
 "figs":[bars("Plate I","NY Now summer 2026 · exhibitors and prospects",[
   {"l":"EXHIBITORS ON THE FLOOR","v":460,"d":"460","hi":True},
   {"l":"PROSPECTIVE EXHIBITORS VISITING","v":107,"d":"107"},
   {"l":"NEW OR RETURNING","v":70,"d":"70+"}],
   "Counts as reported by the organisers. Gifts & Decorative Accessories, 5 August 2026.",199)],
 "flow":flow5("A show that finished ahead.","The number that carries cash.","New owner, first disclosure.",
   "A 96% renewal is a harder number than an attendance figure, because it is paid.","The Retail Desk",
   "NY Now opens today","a-ny-now-opens-today.html"),
 "desk":{"split":"a renewal rate is the only trade-show statistic a buyer should trust"},
 "next":nxt("the-hundred-six-thousand-miss","Metals","Payrolls fell 23,000 and gold closed the week at $4,341.30.",
   "ny-now-opens-today","Trade Shows","thirteen-hundred-brands-and-a-centenary","Trade Shows")}

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
