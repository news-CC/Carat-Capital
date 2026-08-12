#!/usr/bin/env python3
# Edition No. 033 - 2026-08-12. Prepends 4 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-12"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - the-mix-did-the-work ==========
art("the-mix-did-the-work","diamonds",True,"Lead Story · Diamonds Desk",5,"The Diamonds Desk",
["ACTOR","VS","NUM"],
"Lucara's price a carat rose 24% as its prices fell",
"Lucara sold 58,553 carats in the second quarter against 77,167 a year earlier and took $41.0 million against $43.7 million. That is 24% fewer stones for 6% less money, and the company says both its sales channels quoted lower prices.",
[
"Lucara Diamond sold 58,553 carats out of Karowe in the second quarter of 2026, against 77,167 carats in the same quarter of 2025, and took $41.0 million for them against $43.7 million. Twenty-four per cent fewer stones left the mine's sales channels and revenue fell only 6%. The distance between those two figures is the quarter. Dividing the company's own revenue by its own carats gives $700.22 a carat realised this quarter against $566.30 a year ago, a rise of 23.7%, arithmetic this desk has done and no source publishes. The results were released on 7 August. The company's own commentary points the other way: average prices per carat declined across both channels, with tender prices down 5% and Clara prices down 17%, which it attributes to continued pricing pressure on mid-range and lower-grade stones.",
"Both statements are true at once, and the reconciliation is the finding. All of the gain came from the mix, none of it from price. What Lucara sold this quarter was a smaller and heavier parcel into a market quoting less for everything in it. The company does not publish a size breakdown of the goods it sold, so the mix cannot be traced line by line from the release, and it is worth saying plainly that it is not a story about more big stones reaching the surface either: specials, the stones above 10.8 carats, came in at 176 for the quarter against 242 a year ago, down 27%. Fewer carats sold, fewer specials recovered, lower quoted prices in both channels, and a realised average up almost a quarter. Only the composition of what went to market can carry that.",
"The profit line has the same double reading and it needs subtraction to see. Second-quarter net income was $15.6 million against $12.5 million a year earlier, up about 25%. First-half net income was $1.0 million against $12.4 million, down 92%. Take the quarter out of the half and the first quarter of 2026 carried a loss of roughly $14.6 million, this desk's arithmetic from the company's two published figures. The second quarter did not lift the year; it repaired a first quarter that had gone badly. Underneath, the plant ran well: 761,848 tonnes of ore processed, 90,082 carats recovered at a grade of 10.9 carats per hundred tonnes, of which 6,973 came from tailings, and an operating cost of $23.76 a tonne, down 11% from $26.76.",
"The guidance held, and holding it is a bigger commitment than it looks. Full-year revenue guidance stays at $100 million to $130 million against $62.8 million banked in the first half, which leaves $37.2 million to $67.2 million to find in the second. Carats-sold guidance stays at 340,000 to 360,000 against 138,297 sold in the half, requiring between 201,703 and 221,703 carats in the remaining two quarters, or 59% to 62% of the year's sales after halfway. Those three second-half figures are this desk's subtraction, not the company's. Behind it sits $243.6 million of cash at 30 June against $342.8 million of bonds payable with nothing drawn on the working capital or project facilities, an underground project with $275.9 million of completion cost still to spend including contingency and full production expected in the first half of 2028, and an open pit on track to finish in the fourth quarter of this year. In July the Botswana Department of Mines licensed the 15-person auxiliary winder and the 105-person man and material winder on the production shaft.",
"The desk's view: the mix is doing work the price cannot, and that is a thinner kind of good news than a 24% realisation gain sounds. A miner that sells fewer and better stones into a falling market has bought itself a quarter, not a recovery, because the pile of better stones is finite and the price it is being measured against keeps dropping. The number that decides Lucara's year is not the $700 a carat it realised in the second quarter but the 202,000 to 222,000 carats it has to sell in the second half to stand behind its own guidance, into channels that have just quoted 5% and 17% lower. Watch the third-quarter carats sold before the third-quarter price. If the volume does not arrive, no mix will cover it."
],
[
 {"title":"Lucara Announces Q2 2026 Results — Lucara Diamond Corp via CNW (7 August 2026)","url":"https://www.newswire.ca/news-releases/lucara-announces-q2-2026-results-844041946.html"},
 {"title":"Lucara Announces Q2 2026 Results — Lucara Diamond newsroom","url":"https://lucaradiamond.com/newsroom/news-releases/lucara-announces-q2-2026-results-122939/"},
 {"title":"Lucara Revenue Falls as Average Price of Small Stones Drops — Rapaport","url":"https://rapaport.com/news/lucara-revenue-falls-as-average-price-of-small-stones-drops/"},
 {"title":"1,305 carats: Karowe finds its tenth thousand-carat diamond — Carat Capital (15 July 2026)","url":"https://caratcapital.org/a-lucara-tenth-thousand-carat.html"},
])

# ========== 2. sixty-six-fifty-nine ==========
art("sixty-six-fifty-nine","gold-metals",False,"Gold & Metals Desk · The Tape",5,"The Gold & Metals Desk",
["NUM","VS"],
"66.59: silver takes a fourth session out of gold",
"Gold reads $4,415.20 and silver $66.30 on this paper's tape this morning. The ratio between them has fallen on four consecutive sessions, from 68.41 to 66.59. Platinum was not written back, and the reason is printed below.",
[
"It takes 66.59 ounces of silver to buy an ounce of gold this morning, against 67.49 yesterday. Kitco's live board at 05:59 New York time read gold at $4,415.20 and silver at $66.30, and those are the readings this paper's tape now carries: the Editor re-read the metals at press time and wrote the fresher marks back over caratwire's 04:59 figures of $4,401.70 and $66.03, with the timestamp and the source named on the tape. Both were checked against a second page the same morning. TradingEconomics read gold $4,416.14 and silver $66.39, which is 0.02% and 0.14% away from the board this paper used. Measured against this paper's own mark of record 24 hours earlier, gold is up $42.40 or 0.97% and silver is up $1.51 or 2.33%.",
"The ratio is the series worth keeping. On 9 August it stood at 68.41, on 10 August at 67.84, on 11 August at 67.49 and this morning at 66.59, every one of those four figures this desk's own division of its own published gold mark by its own published silver mark. That is 1.82 points, or 2.66%, taken out of gold's purchasing power over silver in three sessions, and today's 0.90-point narrowing is the largest single step of the four. Silver has taken something out of gold on each of four sessions. Fine gold works out at $141.95 a gram at 31.1035 grams to the troy ounce, also this desk's arithmetic.",
"The tape did not take a fresh platinum mark today, and the reason belongs in print rather than in a note nobody reads. Kitco's platinum cell read $1,764.00, up $27.00 or 1.55% — the identical value and the identical change this paper printed yesterday morning. JM Bullion's board at 04:52 New York time bid $1,748.00. TradingEconomics read $1,761.30, up 0.36% on the day. That is a span of $33.90 across three published pages read inside an hour, or 1.94% of the metal, this desk's arithmetic. Against that spread, and against a cell that reproduced yesterday exactly, this desk would not call any of the three a verified press-time reading. So caratwire's 04:59 mark of $1,747.00 stands as filed, which is the figure JM Bullion's bid corroborates within a dollar. Palladium is handled the same way and for the same reason: the tape carries $1,351.00, against $1,368.00 on Kitco's board and $1,392.59 on JM Bullion's at 00:13, a 3.1% spread.",
"For anyone quoting metal across a counter the practical number today is silver, not gold. A workshop pricing silver stock off a sheet printed two days ago is 2.33% behind on this morning alone, and 4.5% behind the mark this paper carried on 9 August, when silver sat at $63.46. Gold has moved too, but at 0.97% it is inside the range a quotation usually survives. The ratio is the cleaner instrument for the same reason: it strips the dollar out and says what the two metals are doing to each other, and what they have been doing for four sessions is silver closing on gold. Nothing in that series depends on which board a reader opens, because both legs of it come from the same mark on the same tape at the same hour.",
"The desk's view: silver is repricing against gold and the tape has the series to prove it, which is worth more to a bench than either price on its own. Four consecutive narrowings is not yet a trend anybody should trade, but it is long enough that a silver quotation written last week is now materially wrong, and that is a bill somebody pays. The other lesson is duller and more useful. Three public pages disagreed on platinum by nearly 2% this morning and one of them was serving yesterday's number with yesterday's change attached, which is exactly the failure a reader cannot see. This paper would rather carry an hour-old mark it can stand behind than a fresh-looking one it cannot, and it will keep saying so on the page when it happens."
],
[
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (12 August 2026, 05:59 EST live board)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Gold — price, chart, historical data (read 12 August 2026)","url":"https://tradingeconomics.com/commodity/gold"},
 {"title":"Platinum Prices Today Per Ounce, 24hr spot chart — JM Bullion (12 August 2026, 04:52 EST)","url":"https://www.jmbullion.com/charts/platinum-price/"},
 {"title":"AED 10.44 between two Dubai gold pages, and holding — Carat Capital (11 August 2026)","url":"https://caratcapital.org/a-ten-forty-four-and-holding.html"},
])

# ========== 3. zales-goes-to-mattel ==========
art("zales-goes-to-mattel","retail-tech",False,"Retail & Technology Desk · People",4,"The Retail Desk",
["ACTOR","GAP"],
"Signet gives Zales and Banter to a Mattel executive",
"Jamie Cygielman becomes president of Zales and Banter on 24 August, reporting to chief executive J.K. Symancyk. She arrives from Mattel, where she was global head of dolls, having earlier run American Girl.",
[
"Signet Jewelers named Jamie Cygielman president of Zales and Banter on 11 August, and she starts on 24 August. She arrives from Mattel, where she was global head of dolls, a portfolio she came to after running American Girl as general manager and president and which she later widened to include Barbie. She will be based in Dallas and reports directly to J.K. Symancyk, Signet's chief executive. The appointment did not come alone. The same release named Pam Cloud president of Blue Nile with effect from 10 August, out of more than twenty-five years at Tiffany and Co., latterly as senior vice president and chief merchandising officer, an appointment this paper reported on 6 August.",
"Two of Signet's four brand families changed president inside eight days, and the two hires are not the same kind of hire. Under Grow Brand Love, the strategy Symancyk launched in March 2025, Signet is organised into four customer families: Kay and Peoples for core milestone and romantic gifting, Zales and Banter for style and trend, Jared for inspired luxury, and Blue Nile for luxury. Blue Nile went to a merchant with a quarter-century inside the most recognised name in American jewellery. Style and trend went to somebody who has never sold jewellery. One seat was filled from the trade and the other from a toy company, in the same announcement, by the same chief executive, on the same strategy.",
"The split is a statement about what the two jobs are. A merchandising officer's craft is the assortment: what is bought, at what margin, in what depth, and how quickly the wrong thing is cleared. A doll portfolio is a licensing and franchise craft: what the brand means, who it means it to, and how far it stretches before it breaks. Signet has decided that Blue Nile's problem is the first kind and that Zales and Banter's problem is the second. That is a defensible reading of a business whose stated aim is to move its chains from operating as retail banners to operating as brands, and it is also a bet that fashion-jewellery customers choose a sign before they choose a stone.",
"The cost side is where the bet meets the metal. The everyday and fashion end that Grow Brand Love is pushing into is the end where the price of gold lands hardest per unit sold, and gold reads $4,415.20 an ounce on this paper's tape this morning, up 0.97% on the mark this paper carried 24 hours earlier and up 6.2% on the $4,158.30 this paper's tape carried a week ago on 5 August. A brand president can change what a chain means. She cannot change what the metal costs, and the two brands she has just been given sell into the price points with the least room to absorb it. This paper has spent the month filing the same pressure from the demand side, with Indian gold jewellery demand down 15% by weight in the second quarter and Kalyan taking more than 46% of a quarter's revenue in recycled metal.",
"The desk's view: the brand job and the merchant job are not the same job, and Signet has just said out loud which of its banners has which problem. That is more information than a personnel notice usually carries, and independents should read it as a competitive signal rather than a press release. If Zales and Banter come back at the customer with a sharper story rather than a sharper assortment, the pressure on a local store will land on identity rather than on price, which is the harder kind to answer with a discount. The measurable test arrives with Signet's next set of results: whether the style and trend family's comparable sales move before its gross margin does. Brand work shows up in traffic first and in margin last."
],
[
 {"title":"Signet Jewelers Announces New Leadership for Zales, Banter and Blue Nile — Signet Jewelers (11 August 2026)","url":"https://www.signetjewelers.com/investors/financial-news-releases/financial-news-release/2026/Signet-Jewelers-Announces-New-Leadership-for-Zales-Banter-and-Blue-Nile/default.aspx"},
 {"title":"Signet Jewelers Appoints New Leaders For Zales, Banter And Blue Nile — Forbes (11 August 2026)","url":"https://www.forbes.com/sites/anthonydemarco/2026/08/11/signet-jewelers-appoints-new-leaders-for-zales-banter-and-blue-nile/"},
 {"title":"Diamonds, Brands and Fashion Jewelry: Signet's New Strategy — Rapaport","url":"https://rapaport.com/analysis/diamonds-brands-and-fashion-jewelry-signets-new-strategy/"},
 {"title":"Signet puts 25 years of Tiffany into Blue Nile — Carat Capital (6 August 2026)","url":"https://caratcapital.org/a-tiffany-goes-to-blue-nile.html"},
])

# ========== 4. what-the-flat-month-hid ==========
art("what-the-flat-month-hid","diamonds",False,"Diamonds Desk · Polished",4,"The Diamonds Desk",
["NUM","GAP"],
"1.7% in the cheap colours: what July's flat month hid",
"This paper led on 4 August with the one-carat index flat in July, ending a thirteen-month slide. Rapaport's August newsletter breaks that flat month open by colour: K to M goods averaged 1.7% while the better colours averaged 0.1%.",
[
"A flat month has a shape inside it. This paper led on 4 August with the RapNet Diamond Index for one-carat polished unchanged across July, closing a slide that had run without a positive print since June 2025. Rapaport's Diamond Pulse for August now breaks that same month open by colour, and the flat line turns out to be an average of two different markets. One-carat goods in D to F and G to J colour, in IF to VVS and VS clarity, averaged a gain of 0.1% in July. K to M colours averaged 1.7%. K to M in VS swung from a 0.1% loss to a 2.8% gain.",
"A flat index is an average, and averages hide the thing that moved. On the newsletter's own figures the cheapest colour band ran seventeen times the gain of the better bands last month, this desk's division of 1.7 by 0.1, which is the sort of ratio that only survives while the numerator is small. The point is not the multiple. The point is that the recovery this paper has been describing since 14 July as a bottom-up move now has a second dimension. It was already running from the bottom of the size chart: in the same July, 0.30-carat goods gained 1.6% and 0.50-carat goods 1.8% against a flat one-carat, figures this paper published on 4 August. It is now also running from the bottom of the colour scale.",
"That fits what the trade has been buying rather than what it has been saying. The goods moving are the goods a cautious retailer reorders, and a K to M stone at VS clarity is exactly the compromise a buyer makes when the budget is fixed and the carat weight is not negotiable. It also means the headline number a jeweller quotes as evidence of a turn is the one number in the set that did not turn. The one-carat index was flat because a near-flat top and a rising bottom cancelled inside it, and anyone reading the single figure took away the opposite of what the components say.",
"The limits of this should be stated. It is one source, and that source is the owner of the index reporting on its own index, which makes it primary and interested at the same time; there is no second publisher of RapNet colour-band moves to check it against. The rest of the August newsletter is material this paper has already run and re-checked rather than new: global rough production down 8% to 98.8 million carats in 2025 ran here on 27 July, De Beers' first-half revenue down 19% to $1.58 billion ran here on 31 July, and the Section 301 bands of 10% and 12.5% on jewellery and gemstone imports ran here on 25 July. The colour split is the one line in it this paper had not published.",
"The desk's view: the recovery is starting at the cheap end of the colour scale too, and that is worth more to a buyer than another month of watching the one-carat headline. Two dimensions now point the same way, size and colour, and both say the same thing about who is doing the buying: the money is coming back at the bottom and working upward, slowly, one price point at a time. The instruction is practical. A dealer holding K to M goods has just been told those parcels moved while better colours did not, and a dealer waiting for the one-carat headline to turn before restocking has been reading a number that averages away the only part of the market that is working. Watch whether the August figures put a second positive month on the cheap colours. One month is composition; two is a trend."
],
[
 {"title":"The Diamond Pulse, August 2026 — Rapaport trade newsletter (read 12 August 2026)","url":"https://rapaport.com/trade/newsletters/the-diamond-pulse-august-2026/"},
 {"title":"The 1-carat stops falling: polished's best month since the tariffs — Carat Capital (4 August 2026)","url":"https://caratcapital.org/a-the-one-carat-stops-falling.html"},
 {"title":"Thirty-pointers run while the one-carat stalls — Carat Capital (27 July 2026)","url":"https://caratcapital.org/a-thirties-outrun-the-ones.html"},
 {"title":"Ten and twelve-and-a-half: the tariff wall comes back — Carat Capital (25 July 2026)","url":"https://caratcapital.org/a-tariff-wall-returns.html"},
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

specs["the-mix-did-the-work"] = {
 **strip("By the numbers · Lucara, second quarter 2026",[
   {"fig":"$700.22","delta":"▲ +23.7%","dir":"up","lab":"realised a carat, derived by this desk"},
   {"fig":"58,553","delta":"▼ −24%","dir":"down","lab":"carats sold in the quarter"},
   {"fig":"$41.0m","delta":"▼ −6%","dir":"down","lab":"quarterly revenue"},
   {"fig":"−5% / −17%","lab":"tender and Clara prices, company figures"},
   {"fig":"$1.0m","delta":"▼ −92%","dir":"down","lab":"first-half net income"}]),
 "figs":[bars("Plate I","Lucara · realised price a carat, revenue divided by carats sold · dollars",[
   {"l":"Q2 2026","v":700.22,"d":"$700.22","hi":True},
   {"l":"Q2 2025","v":566.30,"d":"$566.30"},
   {"l":"H1 2026","v":454.10,"d":"$454.10"},
   {"l":"H1 2025","v":493.21,"d":"$493.21"}],
   "This desk's division of the company's published revenue by its published carats sold; Lucara does not publish these four figures. The quarter's realisation rose 23.7% while the half's fell 7.9%.",214)],
 "flow":flow5("Twenty-four per cent fewer stones, six per cent less money.","A quarter that repaired a quarter.","What the second half has to carry.",
   "All of the gain came from the mix, none of it from price","The Diamonds Desk",
   "Karowe finds its tenth thousand-carat diamond","a-lucara-tenth-thousand-carat.html"),
 "desk":{"split":"the mix is doing work the price cannot"},
 "next":nxt("sixty-six-fifty-nine","Metals","The gold-to-silver ratio has narrowed on four consecutive sessions, to 66.59.",
   "what-the-flat-month-hid","Diamonds","thirties-outrun-the-ones","Polished")}

specs["sixty-six-fifty-nine"] = {
 **strip("By the numbers · The tape, 12 August",[
   {"fig":"$4,415.20","delta":"▲ +0.97%","dir":"up","lab":"gold, Kitco 05:59 EST, written back"},
   {"fig":"$66.30","delta":"▲ +2.33%","dir":"up","lab":"silver, same board, same read"},
   {"fig":"66.59","delta":"▼ −0.90","dir":"down","lab":"gold-to-silver ratio, derived"},
   {"fig":"$1,747.00","lab":"platinum, the 04:59 mark, not rewritten"},
   {"fig":"1.94%","lab":"spread across three platinum pages"}]),
 "figs":[bars("Plate I","Gold-to-silver ratio on this paper's own marks · ounces of silver to one of gold",[
   {"l":"12 AUGUST","v":66.59,"d":"66.59","hi":True},
   {"l":"11 AUGUST","v":67.49,"d":"67.49"},
   {"l":"10 AUGUST","v":67.84,"d":"67.84"},
   {"l":"9 AUGUST","v":68.41,"d":"68.41"}],
   "Each figure is this desk's division of its own published gold mark by its own published silver mark on the same tape at the same hour. Down 1.82 points, or 2.66%, in three sessions.",215)],
 "flow":flow5("Two marks, checked twice, written back.","Four sessions of the same direction.","The mark this desk would not take.",
   "Silver has taken something out of gold on each of four sessions","The Gold & Metals Desk",
   "AED 10.44 between two Dubai gold pages","a-ten-forty-four-and-holding.html"),
 "desk":{"split":"silver is repricing against gold and the tape has the series to prove it"},
 "next":nxt("zales-goes-to-mattel","Retail","Signet has given its style and trend brands to a Mattel executive.",
   "ten-forty-four-and-holding","Metals","neither-one-is-wrong","Metals")}

specs["zales-goes-to-mattel"] = {
 **strip("By the numbers · Signet's two new presidents",[
   {"fig":"24 Aug","lab":"Cygielman starts at Zales and Banter"},
   {"fig":"10 Aug","lab":"Cloud started at Blue Nile"},
   {"fig":"2 of 4","lab":"brand families with a new president"},
   {"fig":"8 days","lab":"between the two starts"},
   {"fig":"Mar 2025","lab":"Grow Brand Love launched"}]),
 "figs":[bars("Plate I","Signet's four customer families under Grow Brand Love · brands in each",[
   {"l":"CORE MILESTONE - KAY, PEOPLES","v":2,"d":"2"},
   {"l":"STYLE AND TREND - ZALES, BANTER","v":2,"d":"2 · new president","hi":True},
   {"l":"INSPIRED LUXURY - JARED","v":1,"d":"1"},
   {"l":"LUXURY - BLUE NILE","v":1,"d":"1 · new president"}],
   "The four-family structure is Signet's own, set out under the Grow Brand Love strategy launched by J.K. Symancyk in March 2025. Two of the four changed president between 10 and 24 August 2026.",216)],
 "flow":flow5("A doll portfolio takes a jewellery chain.","Two seats, two different crafts.","Where the bet meets the metal.",
   "Style and trend went to somebody who has never sold jewellery","The Retail Desk",
   "Signet puts 25 years of Tiffany into Blue Nile","a-tiffany-goes-to-blue-nile.html"),
 "desk":{"split":"the brand job and the merchant job are not the same job"},
 "next":nxt("the-mix-did-the-work","Diamonds","Lucara's realised price a carat rose 24% while both its sales channels cut prices.",
   "tiffany-goes-to-blue-nile","Retail","one-state-one-banner","Retail")}

specs["what-the-flat-month-hid"] = {
 **strip("By the numbers · One-carat polished, July",[
   {"fig":"1.7%","delta":"▲","dir":"up","lab":"K to M colours, monthly average"},
   {"fig":"0.1%","delta":"▲","dir":"up","lab":"D to F and G to J, IF-VVS and VS"},
   {"fig":"2.8%","delta":"▲","dir":"up","lab":"K to M in VS, from a 0.1% loss"},
   {"fig":"flat","lab":"the one-carat index this paper led on"},
   {"fig":"17x","lab":"the ratio between the bands, derived"}]),
 "figs":[bars("Plate I","One-carat polished, July 2026 · monthly move by colour band, per cent",[
   {"l":"K TO M, VS","v":2.8,"d":"+2.8%","hi":True},
   {"l":"K TO M, AVERAGE","v":1.7,"d":"+1.7%"},
   {"l":"D-F AND G-J, IF-VVS AND VS","v":0.1,"d":"+0.1%"}],
   "Figures from Rapaport's Diamond Pulse, August 2026, describing July moves. The headline one-carat index was unchanged for the month; these are its components.",217)],
 "flow":flow5("The shape inside a flat month.","Bottom-up in two dimensions now.","One source, and it owns the index.",
   "A flat index is an average, and averages hide the thing that moved","The Diamonds Desk",
   "The 1-carat stops falling","a-the-one-carat-stops-falling.html"),
 "desk":{"split":"the recovery is starting at the cheap end of the colour scale too"},
 "next":nxt("the-mix-did-the-work","Diamonds","Lucara sold 24% fewer carats and realised 24% more for each of them.",
   "the-one-carat-stops-falling","Polished","small-stones-lead-the-turn","Polished")}

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
    print("  %-30s %2d words" % (a["slug"], len(pull.split())))

articles = NEW + articles
for s in specs: editorial[s] = specs[s]
(C/"articles.json").write_text(json.dumps(articles, ensure_ascii=False, indent=1))
(C/"editorial.json").write_text(json.dumps(editorial, ensure_ascii=False, indent=1))
print("OK: %d articles prepended, %d specs written, total %d" % (len(NEW), len(specs), len(articles)))
