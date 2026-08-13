#!/usr/bin/env python3
# Edition No. 034 - 2026-08-13. Prepends 4 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-13"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - the-loss-that-wasnt-revenue ==========
art("the-loss-that-wasnt-revenue","diamonds",True,"Lead Story · Diamonds Desk",5,"The Diamonds Desk",
["REVERSAL","NUM","STAKES"],
"Sarine's revenue fell 6%. Its loss grew 21 times.",
"Sarine Technologies took $14.4 million in the first half against a net loss of $3.5 million, where a year earlier the loss was $166,000. Revenue fell about $0.9 million. The deficit widened by $3.3 million.",
[
"Sarine Technologies reported its first half of 2026 on 11 August with revenue of $14.4 million, down 6% on the year, and a net loss of $3.5 million against a loss of $166,000 in the same half of 2025. No dividend was declared. Dividing one deficit by the other gives 21.1 times, this desk's arithmetic on the company's two published figures, and the multiple is the number every summary of these results has led with. It is also the least useful number in them, because a loss that starts at $166,000 will produce a frightening multiple out of almost any deterioration. The figure worth holding is the distance between the two smaller numbers underneath it.",
"Take 6% off the published revenue and the first half of 2025 comes out at roughly $15.3 million, which puts this half's revenue decline at about $0.9 million. The deficit widened by $3.334 million over the same period. That is a loss growing by something close to three and a half times the fall in revenue, all of it this desk's arithmetic on rounded published figures. The loss did not come from the top line. The company names two causes and only one of them is a diamond-market fact: operating expenses rose, driven by a weaker US dollar against the Israeli shekel, and natural-diamond processing volumes fell against lab-grown competition. A currency move between Washington and Tel Aviv is not a verdict on the polishing floor, and it is carrying a large share of this result.",
"The growth lines run the other way and they are not small. Revenue from GCAL grading rose more than 50% in the half. Revenue from the MVP rough-planning service more than doubled. Kitov.ai, the industrial-inspection associate in which Sarine holds 33%, booked $1.5 million of revenue and also more than doubled. Those are the recurring-service lines the company has spent years pivoting towards, and they grew through a half in which the group lost twenty-one times what it lost a year earlier. The shape is a business whose new revenue is compounding off a base still too small to cover what the old one is giving up, which is a slower and more ordinary problem than a 21-fold multiple suggests.",
"For anyone outside the technology end of the trade, Sarine is worth reading as an instrument rather than a company. It sells the scanning, planning and grading that stones pass through on the way to a polished parcel, so its revenue tracks how many stones are being worked, not how many are being sold at retail. The company's own framing is that a 6% revenue decline is modest against a significantly greater contraction in rough supply, and if that holds, the factories processed a larger share of a smaller pile. This paper published global rough production down 8% to 98.8 million carats in 2025 on 27 July, and yesterday reported Lucara selling 24% fewer carats in its second quarter. A 6% fall at the machine end against those two figures is the more encouraging reading available in this release.",
"The desk's view: the loss did not come from the top line, and a trade paper that prints the 21-fold multiple without that sentence has told its readers the opposite of what happened. The processing floor held up better than rough supply did. What broke was the cost side, and a shekel that will not stay where the budget assumed is a problem Sarine can hedge rather than a signal about diamonds. The number to watch in the second half is not the deficit but whether GCAL and MVP keep compounding at these rates, because the arithmetic only turns when the recurring lines are big enough to absorb a currency move without the group noticing. Until they are, this company will keep reporting the diamond market's weather and its own bank's weather in the same sentence."
],
[
 {"title":"Sarine's Deficit Widens More Than 20-Fold in First Half — Rapaport (11 August 2026)","url":"https://rapaport.com/news/sarines-deficit-widens-more-than-20-fold-in-first-half/"},
 {"title":"Sarine Technologies Ltd. H1 2026 Results: revenue down 6% to US$14.4M, net loss US$3.5M, no dividend declared — Minichart (11 August 2026)","url":"https://www.minichart.com.sg/2026/08/11/sarine-technologies-ltd-h1-2026-results-revenue-down-6-to-us14-4m-net-loss-us3-5m-no-dividend-declared/"},
 {"title":"Thirty-pointers run while the one-carat stalls — Carat Capital (27 July 2026)","url":"https://caratcapital.org/a-thirties-outrun-the-ones.html"},
 {"title":"Lucara's price a carat rose 24% as its prices fell — Carat Capital (12 August 2026)","url":"https://caratcapital.org/a-the-mix-did-the-work.html"},
])

# ========== 2. three-sessions-undone ==========
art("three-sessions-undone","gold-metals",False,"Gold & Metals Desk · The Tape",5,"The Gold & Metals Desk",
["REVERSAL","NUM","VS"],
"Three sessions of silver's gain undone in one",
"Gold reads $4,384.10 and silver $64.52 on this paper's tape this morning. The gold-to-silver ratio widened to 67.95 from 66.59, giving back 1.36 of the 1.82 points silver had taken out of gold across four sessions.",
[
"It takes 67.95 ounces of silver to buy an ounce of gold this morning, against 66.59 yesterday. Kitco's live board at 06:00 New York time read gold at $4,384.10 and silver at $64.52, and those are the readings this paper's tape now carries: the Editor re-read both metals at press time and wrote the fresher marks back over caratwire's 04:59 figures of $4,374.20 and $64.31, with the timestamp and the source named on the tape. Both were checked against a second page the same morning. TradingEconomics read gold $4,383.54 and silver $64.65, which is 0.01% and 0.20% away from the board this paper used. Measured against this paper's own mark of record 24 hours earlier, gold is down $31.10 or 0.70% and silver is down $1.78 or 2.68%.",
"Yesterday this desk published a four-session series and said in print that four consecutive narrowings was not yet a trend anybody should trade. One session has now made the point better than the caution did. The ratio ran 68.41 on 9 August, 67.84 on 10 August, 67.49 on 11 August and 66.59 on 12 August, every figure this desk's division of its own published gold mark by its own published silver mark, and this morning it is 67.95. Silver gave back in one session what it took in three. The four-session narrowing was worth 1.82 points; today's widening is 1.36 of them, or 74.7% of the whole run, and the ratio now sits above every reading since 9 August. Fine gold works out at $140.95 a gram and fine silver at $2.07, at 31.1035 grams to the troy ounce, also this desk's arithmetic.",
"Platinum and palladium were not written back, for the second consecutive morning and for a sharper reason than yesterday's. Kitco's board read platinum $1,717.00, down $31.00 or 1.77%. TradingEconomics read $1,731.60 and JM Bullion's board at 06:01 New York time read $1,731.10. The two pages this desk does not use as its mark of record agree with each other to within 50 cents and put Kitco $14.60 low, a gap of 0.85% of the metal, which makes the board this paper reads the outlier rather than the market unsettled. That is not a verified press-time reading, so under the one-price rule caratwire's 04:59 mark of $1,710.00 stands as filed and prints as-is. Palladium has no comparable second page at all this morning: Kitco bid $1,324.00 and the only other board reachable quoted an ask of $1,360.65, which is a different side of the spread and not a check. The 04:59 mark of $1,319.00 stands.",
"For a bench the practical reading is that silver is still ahead on the week and is now moving in both directions fast enough to matter. Against the $63.46 this paper's tape carried on 9 August, this morning's $64.52 is up 1.67%, so a workshop that repriced silver stock after yesterday's article is not wrong today, merely less right. Gold is the calmer leg and is up 5.43% on the $4,158.30 the tape carried on 5 August. The white metals are where the quoting risk sits: this paper has now declined to take a platinum mark on two consecutive mornings from three different sets of readings, and a jeweller quoting platinum off a single public board today is choosing one of two numbers 0.85% apart without being told there is a choice.",
"The desk's view: a four-session series is a description, not a direction, and this morning is the cheapest possible demonstration of it. The honest lesson is about how a tape should be read rather than about silver. Four narrowings in a row invited a story about silver closing on gold, this desk wrote the series and refused the story, and one session has now removed three-quarters of the move. What survives is the arithmetic, because both legs come from the same mark on the same tape at the same hour, and what does not survive is any reader who took four sessions as a trend. Watch whether the ratio settles above or below 67.49, the 11 August reading, before treating either direction as anything at all."
],
[
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (13 August 2026, 06:00 EST live board)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Gold — price, chart, historical data (read 13 August 2026)","url":"https://tradingeconomics.com/commodity/gold"},
 {"title":"Platinum Prices Today Per Ounce, 24hr spot chart — JM Bullion (13 August 2026, 06:01 EST)","url":"https://www.jmbullion.com/charts/platinum-price/"},
 {"title":"66.59: silver takes a fourth session out of gold — Carat Capital (12 August 2026)","url":"https://caratcapital.org/a-sixty-six-fifty-nine.html"},
])

# ========== 3. titan-calls-the-price-stable ==========
art("titan-calls-the-price-stable","retail-tech",False,"Retail & Technology Desk · Demand",4,"The Retail Desk",
["ACTOR","NUM","VS"],
"Titan's jewellery arm grew 43% and says diamond prices settled",
"Titan's jewellery division took Rs 18,253 crore in the June quarter, up 43% excluding bullion and digital gold. Its managing director says the natural-diamond market has stabilised and the lab-grown argument has quietened.",
[
"India's largest branded jeweller has put a view on natural-diamond pricing on the record, and it is the first time in this paper's archive that the counter rather than the index has said it. Arun Narayan, Titan's jewellery chief executive, told an earnings call that the company has seen more stability in the pricing of both solitaires and small diamonds. Ajoy Chawla, Titan's managing director, went further on the comparison that has run underneath the trade for two years. \"I think at the market level, it has stabilized,\" Chawla said of natural-diamond pricing, adding that the lab-grown-versus-natural narrative has faded from the conversation. Titan reported a resurgence in diamond-jewellery buying in the fourth quarter of its fiscal 2026 and into the first quarter of fiscal 2027, with demand strengthening through April to June. The remarks were published on 12 August.",
"The quarter behind the statement is large enough to give it weight. Titan's consolidated income for the three months to 30 June was Rs 20,753 crore, up 40%, with profit before tax of Rs 2,429 crore, up 64%, on an 11.7% margin. The jewellery division took Rs 18,253 crore, up 43% excluding bullion and digital gold, at an EBIT of Rs 2,360 crore and a 12.9% margin. Watches and wearables took Rs 1,543 crore, up 21%. The group added a net 77 stores in the quarter to reach 3,680. This paper published the same quarter on 28 July from the company's own business update at about 41% revenue growth and 39% for jewellery; the 43% figure here excludes bullion and digital gold and is therefore a different basis, not a revision. A third figure is circulating in secondary coverage, revenue from operations of Rs 21,356 crore and growth of 29.25% on a base of Rs 16,523 crore, which is internally consistent on its own basis and does not agree with the 40% headline. This desk prints the company's own segment disclosure and flags the divergence rather than choosing quietly.",
"What makes the remark worth a story is which side of the trade it comes from. Everything this paper has published on polished pricing this month has come from the index end: the RapNet one-carat unchanged in July after thirteen months of falls, published here on 4 August, and the colour split inside that flat month, with K to M goods averaging 1.7% against 0.1% for better colours, published yesterday. Those are price series describing what dealers quote each other. Titan is describing what customers did at roughly 3,680 counters. When a supply-side index and a demand-side retailer stop disagreeing about direction in the same fortnight, the reading is firmer than either on its own, and neither of them is saying prices have risen. The counter is telling the mine that the price stopped falling.",
"The limits are real and they run in one direction. Titan sells natural diamonds and has been notably careful about lab-grown, so a statement that the natural market has stabilised is made by an interested party, on its own earnings call, in the same week it reported a 43% jewellery quarter. It is one company in one market, and the Indian counter is not the American one: this paper reported Indian gold jewellery demand down 15% by weight in the second quarter even as value rose. Stabilised is also not the same word as recovered. Nothing in the remarks puts a number on the pricing of anything, which is why the index reporting still has to carry the arithmetic.",
"The desk's view: the counter is telling the mine that the price stopped falling, and that is worth more than another month of the same index print. The useful part is not the claim but the convergence. Two independent readings of the polished market, one made of quotations and one made of till receipts, have arrived at the same word within a fortnight, after two years in which the demand side would not say it out loud. For an independent retailer the practical instruction is narrow: stability in small-stone and solitaire pricing is the condition under which restocking stops being a bet on the price and starts being a bet on the customer. Watch whether Titan repeats the language at its second-quarter call. Said once on a good quarter it is commentary; said twice it is a position."
],
[
 {"title":"Titan: Natural Diamonds Gain Stability Against Lab-Grown — Rapaport (12 August 2026)","url":"https://rapaport.com/news/titan-natural-diamonds-gain-stability-against-lab-grown/"},
 {"title":"Titan Q1 FY27 income jumps 40% to Rs 20,753 crore on strong festive demand — afaqs (8 August 2026)","url":"https://www.afaqs.com/news/brands/titan-q1-fy27-income-jumps-40-to-rs-20753-crore-on-strong-festive-demand-12241372"},
 {"title":"Titan Q1 Results 2027: PAT jumps 63% YoY to Rs 1,777 crore — Sahi (7 August 2026)","url":"https://www.sahi.com/blogs/titan-q1-results-fy2027"},
 {"title":"Titan makes it three: revenue up 41% on India's gold counter — Carat Capital (28 July 2026)","url":"https://caratcapital.org/a-titan-makes-it-three.html"},
 {"title":"1.7% in the cheap colours: what July's flat month hid — Carat Capital (12 August 2026)","url":"https://caratcapital.org/a-what-the-flat-month-hid.html"},
])

# ========== 4. priced-like-1999 ==========
art("priced-like-1999","diamonds",False,"Diamonds Desk · Polished",4,"The Diamonds Desk",
["ACTOR","NUM","GAP"],
"The half-carat is priced like 1999, says Kiran Gems",
"Senil Lakhani, president of Kiran Gems USA, says stones from 0.30 to 0.70 carats are selling at 1990s and early-2000s prices, in the $1,000 to $5,000 band that carries the American counter.",
[
"The claim was made on a trade panel rather than in a release, and it is the sharpest thing said about polished prices this week. Senil Lakhani, president of Kiran Gems USA, told Rapaport's Heard on the Street that diamonds below one carat and up to 1.5 carats are less expensive than ever before and are selling at prices from the 1990s and early 2000s. He put the range that matters at 0.30, 0.40, 0.50 and 0.70 carats, calling those sizes \"the bread and butter for America,\" and placed the money at $1,000, $2,000 and $5,000 rather than the half-million and million-dollar stones that get photographed. The episode was published on 12 August. Kiran Gems is one of the largest diamond manufacturers in the world, so this is the cutting floor talking about the shelf.",
"This paper has been reporting the same goods from the other end all month, and the two accounts fit together only if you separate level from direction. The RapNet index had 0.30-carat goods up 1.6% and 0.50-carat goods up 1.8% in July against a flat one-carat, published here on 4 August, and yesterday's colour split had K to M goods averaging 1.7% against 0.1% for better colours. Those are monthly moves. Lakhani is describing where the price sits, not which way it went, and a 1.6% month on a price that has fallen back to a 1999 level is a very small repair on a very long decline. The bread-and-butter stone is priced where it sat in 1999 and is rising at under two per cent a month, and both halves of that sentence have to be read together or the trade will mistake a floor for a recovery.",
"The same panel produced the answer to a question this paper has circled for weeks, which is whether traceable origin is actually available or merely announced. Jeff Angel, head buyer at RDI Diamonds, said he can find a diamond of traceable Botswana origin in about five minutes, and that he recently filled a million-dollar order in which every stone had to come from Botswana. That is a different picture from the one the compliance conversation paints. Origin is not a shortage at the buying desk for anyone who asks for it; it is a search that a professional buyer already knows how to run. What has not arrived is the part where a retailer can put that fact in front of a customer without building the story themselves, and the panel spent its time on exactly that gap.",
"The limits of all this should be stated plainly, because a panel is not a data series. No index this desk can reach publishes a 1999 comparison for 0.30 to 0.70-carat goods, so the level claim cannot be checked against a price history the way a monthly move can. What can be checked is the direction, and the direction agrees with him. The claim also comes from a manufacturer, which is the part of the chain with the least to gain from suggesting polished is cheap, and that cuts in favour of taking it seriously rather than against it. This desk is reporting it as a named executive's characterisation of his own market, not as a price, and is not putting a figure on 1999 that it cannot source.",
"The desk's view: the interesting number in this market is no longer the monthly percentage, it is the level, and almost nobody is publishing the level. A retailer reading that small goods rose 1.6% in July will restock differently from one who also knows those goods are priced where they were a quarter of a century ago, and the second reader is being told something about margin, not about momentum. The practical instruction is to price the case rather than the index: if the American counter's core stone genuinely sits at 1990s money, the recovery worth waiting for is in what the customer will pay, not in what the dealer quotes. Watch whether a second manufacturer of Kiran's size says the same thing on the record. One is a characterisation; two would be a market."
],
[
 {"title":"Rapaport's Heard on the Street Delves into Diamond Origin and Branding — Rapaport (12 August 2026)","url":"https://rapaport.com/news/rapaports-heard-on-the-street-delves-into-diamond-origin-and-branding/"},
 {"title":"The 1-carat stops falling: polished's best month since the tariffs — Carat Capital (4 August 2026)","url":"https://caratcapital.org/a-the-one-carat-stops-falling.html"},
 {"title":"1.7% in the cheap colours: what July's flat month hid — Carat Capital (12 August 2026)","url":"https://caratcapital.org/a-what-the-flat-month-hid.html"},
 {"title":"Thirty-pointers run while the one-carat stalls — Carat Capital (27 July 2026)","url":"https://caratcapital.org/a-thirties-outrun-the-ones.html"},
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

specs["the-loss-that-wasnt-revenue"] = {
 **strip("By the numbers · Sarine Technologies, first half 2026",[
   {"fig":"$3.5m","delta":"▼ 21.1x","dir":"down","lab":"net loss, against $166,000"},
   {"fig":"$14.4m","delta":"▼ −6%","dir":"down","lab":"revenue for the half"},
   {"fig":"$0.9m","lab":"the revenue decline, derived here"},
   {"fig":"+50%","delta":"▲","dir":"up","lab":"GCAL grading revenue"},
   {"fig":"$1.5m","lab":"Kitov.ai revenue, 33% held"}]),
 "figs":[bars("Plate I","Sarine · what moved in the first half of 2026 · millions of dollars",[
   {"l":"THE LOSS WIDENED BY","v":3.334,"d":"$3.334m","hi":True},
   {"l":"REVENUE FELL BY","v":0.919,"d":"$0.919m"}],
   "This desk's subtraction on the company's published figures: the loss went from $166,000 to $3.5 million, while revenue of $14.4 million was 6% below an implied $15.3 million. The deficit widened by about three and a half times the revenue decline.",218)],
 "flow":flow5("A frightening multiple off a tiny base.","Where the money actually went.","An instrument, not a company.",
   "The loss did not come from the top line","The Diamonds Desk",
   "Lucara's price a carat rose 24% as its prices fell","a-the-mix-did-the-work.html"),
 "desk":{"split":"the loss did not come from the top line"},
 "next":nxt("three-sessions-undone","Metals","Silver gave back in one session three-quarters of a four-session run on gold.",
   "titan-calls-the-price-stable","Retail","the-mix-did-the-work","Diamonds")}

specs["three-sessions-undone"] = {
 **strip("By the numbers · The tape, 13 August",[
   {"fig":"$4,384.10","delta":"▼ −0.70%","dir":"down","lab":"gold, Kitco 06:00 EST, written back"},
   {"fig":"$64.52","delta":"▼ −2.68%","dir":"down","lab":"silver, same board, same read"},
   {"fig":"67.95","delta":"▲ +1.36","dir":"up","lab":"gold-to-silver ratio, derived"},
   {"fig":"$1,710.00","lab":"platinum, the 04:59 mark, not rewritten"},
   {"fig":"0.85%","lab":"gap between three platinum pages"}]),
 "figs":[bars("Plate I","Gold-to-silver ratio on this paper's own marks · ounces of silver to one of gold",[
   {"l":"13 AUGUST","v":67.95,"d":"67.95","hi":True},
   {"l":"12 AUGUST","v":66.59,"d":"66.59"},
   {"l":"11 AUGUST","v":67.49,"d":"67.49"},
   {"l":"10 AUGUST","v":67.84,"d":"67.84"},
   {"l":"9 AUGUST","v":68.41,"d":"68.41"}],
   "Each figure is this desk's division of its own published gold mark by its own published silver mark on the same tape at the same hour. The four-session narrowing to 12 August was worth 1.82 points; 1.36 of them came back in one session.",219)],
 "flow":flow5("Two marks written back, two refused.","One session against four.","The mark this desk would not take, again.",
   "Silver gave back in one session what it took in three","The Gold & Metals Desk",
   "66.59: silver takes a fourth session out of gold","a-sixty-six-fifty-nine.html"),
 "desk":{"split":"a four-session series is a description, not a direction"},
 "next":nxt("the-loss-that-wasnt-revenue","Diamonds","Sarine's deficit widened 21-fold on a revenue decline of about $0.9 million.",
   "sixty-six-fifty-nine","Metals","neither-one-is-wrong","Metals")}

specs["titan-calls-the-price-stable"] = {
 **strip("By the numbers · Titan, quarter to 30 June 2026",[
   {"fig":"Rs 18,253cr","delta":"▲ +43%","dir":"up","lab":"jewellery, excluding bullion"},
   {"fig":"Rs 20,753cr","delta":"▲ +40%","dir":"up","lab":"consolidated income"},
   {"fig":"Rs 2,429cr","delta":"▲ +64%","dir":"up","lab":"profit before tax"},
   {"fig":"Rs 1,543cr","delta":"▲ +21%","dir":"up","lab":"watches and wearables"},
   {"fig":"3,680","delta":"▲ +77","dir":"up","lab":"stores, net additions in the quarter"}]),
 "figs":[bars("Plate I","Titan · June quarter 2026 growth by line · per cent on the year",[
   {"l":"PROFIT BEFORE TAX","v":64,"d":"+64%"},
   {"l":"JEWELLERY, EX-BULLION","v":43,"d":"+43%","hi":True},
   {"l":"CONSOLIDATED INCOME","v":40,"d":"+40%"},
   {"l":"WATCHES AND WEARABLES","v":21,"d":"+21%"}],
   "Company segment disclosure for the quarter to 30 June 2026. The jewellery figure excludes bullion and digital gold, a different basis to the 39% this paper published from the July business update. Secondary coverage carries a third basis at 29.25%, disclosed in the article.",220)],
 "flow":flow5("The counter puts a view on the record.","The quarter behind the statement.","Which side of the trade is talking.",
   "The counter is telling the mine that the price stopped falling","The Retail Desk",
   "Titan makes it three: revenue up 41%","a-titan-makes-it-three.html"),
 "desk":{"split":"the counter is telling the mine that the price stopped falling"},
 "next":nxt("priced-like-1999","Diamonds","Kiran Gems USA says the 0.30 to 0.70-carat stone is selling at 1990s money.",
   "titan-makes-it-three","Retail","what-the-flat-month-hid","Diamonds")}

specs["priced-like-1999"] = {
 **strip("By the numbers · The bread-and-butter stone",[
   {"fig":"0.30–0.70ct","lab":"the sizes Lakhani calls America's core"},
   {"fig":"$1,000–$5,000","lab":"where he places the money"},
   {"fig":"+1.6%","delta":"▲","dir":"up","lab":"0.30ct goods, July, RapNet"},
   {"fig":"+1.8%","delta":"▲","dir":"up","lab":"0.50ct goods, July, RapNet"},
   {"fig":"5 min","lab":"to source a traceable Botswana stone"}]),
 "figs":[bars("Plate I","July 2026 moves on the goods in question · per cent for the month",[
   {"l":"0.50-CARAT","v":1.8,"d":"+1.8%","hi":True},
   {"l":"K TO M COLOURS, 1CT","v":1.7,"d":"+1.7%"},
   {"l":"0.30-CARAT","v":1.6,"d":"+1.6%"},
   {"l":"1-CARAT INDEX","v":0.0,"d":"flat"}],
   "RapNet monthly moves published by Rapaport and reported by this paper on 4 and 12 August. These are directions for one month; the 1990s price level described on the panel is a level, and no index this desk can reach publishes that comparison.",221)],
 "flow":flow5("A manufacturer prices the shelf.","Level and direction are not the same fact.","Origin, in five minutes.",
   "The bread-and-butter stone is priced where it sat in 1999","The Diamonds Desk",
   "1.7% in the cheap colours: what July's flat month hid","a-what-the-flat-month-hid.html"),
 "desk":{"split":"the interesting number in this market is no longer the monthly percentage, it is the level"},
 "next":nxt("the-loss-that-wasnt-revenue","Diamonds","Sarine's loss widened 21-fold while its revenue fell about $0.9 million.",
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
    print("  %-32s %2d words" % (a["slug"], len(pull.split())))

articles = NEW + articles
for s in specs: editorial[s] = specs[s]
(C/"articles.json").write_text(json.dumps(articles, ensure_ascii=False, indent=1))
(C/"editorial.json").write_text(json.dumps(editorial, ensure_ascii=False, indent=1))
print("OK: %d articles prepended, %d specs written, total %d" % (len(NEW), len(specs), len(articles)))
