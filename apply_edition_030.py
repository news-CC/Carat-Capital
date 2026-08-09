#!/usr/bin/env python3
# Edition No. 030 - 2026-08-09. Prepends 6 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-09"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - four-times-melt ==========
art("four-times-melt","auctions",True,"Lead Story · Auctions Desk",5,"The Auctions Desk",
["RECORD","NUM","VS"],
"Four times its metal: a Garrard egg makes £123,500",
"A 22-carat gold Cadbury 'Conundrum' egg by Garrard sold for £123,500, about $166,600, at Batemans on 1 August. That is close to six times its estimate and roughly four times the melt value of its 323.6 grams.",
[
"A chocolate company's promotional egg has set an auction record most jewellery houses would take. A 22-carat gold 'Conundrum' egg made by Garrard & Co. of London in 1983 sold for £123,500, about $166,600, at Batemans Auctioneers & Valuers in Stamford, Lincolnshire on 1 August, a result reported by Forbes on 8 August. The house calls it a world auction record for a bejewelled egg of its type. It made close to six times its pre-sale estimate and about eighteen times the £6,500 it fetched the last time it came up. Forbes dates that earlier sale to 2018 and the Batemans catalogue entry for the same lot is dated July 2017; this paper carries both readings rather than picking one.",
"The number worth holding against it is the metal. The catalogue puts the egg at 323.6 grams of 22-carat gold, which is 91.7% fine, or roughly 296.6 grams of pure gold, 9.54 troy ounces. At the $4,341.30 an ounce this paper's tape has carried since Friday's close, that is about $41,400 of bullion, a figure derived by this desk from the stated weight and fineness rather than published by anyone. The record is four times the metal. The rest is signature and story, and a trade that sets its own making charges should be able to say precisely what each is worth, because that difference is the whole business of a goldsmith.",
"What the buyer took home is a piece of British advertising history with a hallmark on it. Cadbury's commissioned twelve individually designed 22-carat eggs from Garrard in 1983 for a nationwide treasure hunt, burying Perspex caskets across the country, each holding a clue to one egg; a thirteenth was made in secret. This one, called Cuckoo Cuckoo, is engraved and enamelled in translucent green, blue, orange and white, worked with a cat, a weather vane, stars, mice, a castle and a treasure hunter finding a golden egg. Greg Bateman, managing director at Batemans, called the eggs \"a fascinating piece of British cultural history\".",
"The result lands on a desk that has had very little to price. This paper has filed one auction story in the past three editions, Bonhams' three-city Chanel series on 8 August, and made the same point there. The house estimated a Robert Goossens costume bangle made for Chanel around 1960 at $13,000 to $20,000, against Chanel Fine Jewelry earrings from 2024 in 18-carat white gold and diamonds at £2,000 to £3,000. Base metal and paste, correctly attributed, carried roughly five times the estimate of current-production gold and stones. The Garrard egg is the same trade running the other way: real gold, sold on who made it, for whom, and in what year.",
"The desk's view: gold at record levels has quietly changed what an auction result means, and this one shows the arithmetic in the clear. When bullion was cheap, four times melt on a signed object read as a strong price. With gold at $4,341.30 an ounce it means the maker's name and the documentation are carrying more than $125,000 of the total on their own, and the metal is the smaller part of a record. For anyone consigning this autumn the practical instruction is that the premium here is documentation, not carat weight, and the paperwork wants assembling before the estimate is agreed. For anyone buying, the melt figure is the floor, and that floor rose 4.40% in three sessions last week, which makes an under-documented lot expensive in two directions at once."
],
[
 {"title":"Cadbury's Gold 'Conundrum' Egg Sells For Record $166,600 At Auction — Forbes (8 August 2026)","url":"https://www.forbes.com/sites/anthonydemarco/2026/08/08/cadburys-gold-conundrum-egg-sells-for-record-166600-at-auction/"},
 {"title":"A large 22ct gold Cadbury's 'Conundrum' egg, by Garrard & Co — Batemans catalogue entry via the-saleroom","url":"https://www.the-saleroom.com/en-gb/auction-catalogues/batemans-auctioneers-and-valuers/catalogue-id-srbat10047/lot-b6785072-acba-474a-928d-a79a00b0b403"},
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (7 August 2026, 5:00pm EST close)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"$13,000 for costume, £2,000 for gold: Bonhams runs Chanel in three cities — Carat Capital (8 August 2026)","url":"https://caratcapital.org/a-thirteen-thousand-for-costume.html"},
])

# ========== 2. six-forty-thousand-ounces ==========
art("six-forty-thousand-ounces","gold-metals",False,"Gold & Metals Desk · Central Banks",5,"The Gold & Metals Desk",
["NUM","ACTOR","RECORD"],
"640,000 ounces: China's biggest gold month since 2023",
"The People's Bank of China added 640,000 troy ounces in July, about 19.9 tonnes and the largest single month since October 2023. Holdings reached 76.08 million ounces, roughly 2,366 tonnes, in a 21st consecutive month of buying.",
[
"China's central bank bought more gold in July than in any month since October 2023. The People's Bank of China lifted its holdings by 640,000 troy ounces, about 19.9 tonnes, taking official reserves to 76.08 million ounces at the end of the month from 75.44 million at the end of June. In tonnes that is roughly 2,366 against 2,346. It was the twenty-first consecutive month in which the bank has reported a purchase and the largest single addition since the 740,000 ounces recorded in October 2023, and it was published on 7 August alongside the monthly reserve data.",
"Set against the quarter this paper reported a week ago, July is a step up rather than a continuation. The World Gold Council put central-bank buying at 289 tonnes in the second quarter, up 62%, with China taking 33 tonnes across those three months to a holding of 2,346 tonnes. July alone is 19.9 tonnes, close to double the monthly pace China ran through the second quarter. Twenty-one months of buying says the policy is the point, not the price. July was also the month gold closed at $4,041.70, up about half a per cent and its first monthly gain since February, so the bank raised its pace into a market that had barely moved.",
"The reserve arithmetic puts the purchase in proportion. China's gold holdings were valued at $306.35 billion at the end of July against $303.72 billion at the end of June, inside total official foreign-exchange assets of $3.419 trillion, up from $3.416 trillion. Gold is therefore about 8% of the reserve, a share that sits low against most Western central banks and is the reason analysts keep describing the programme as unfinished rather than complete. At the $4,341.30 an ounce this paper's tape has carried since Friday's close, 640,000 ounces is worth about $2.78 billion, a figure derived by this desk from the published ounces rather than reported as such.",
"For the jewellery trade the relevance is the floor under the raw material. Official-sector demand is the least price-sensitive buying in the gold market, because a central bank running a twenty-one month programme does not stop when the metal gets dear, and that is exactly what a fabricator watching its metal line needs to price in. This paper reported on 2 August that first-half central-bank demand came to 345 tonnes, the smallest first half since 2022's 241 tonnes, after a first quarter revised down to 57 tonnes. July's print does not overturn that half. It does say the second half has started faster than the first one ended.",
"The desk's view: a central bank that buys every month is not trading, it is provisioning, and the distinction should change how the bench reads a gold headline. Speculative flows reverse on an inflation print. A reserve-diversification programme reverses on a change of national policy, which is measured in years rather than sessions. The number to keep is 8%, because that is gold's share of Chinese reserves and it is the gap the buying is closing; while it stays near that level the official sector is a standing bid underneath the price rather than a swing factor inside it. For anyone quoting a customer into the fourth quarter, that argues for quoting metal-plus rather than forward on spot, because the buyer on the other side of this market is not looking at the chart."
],
[
 {"title":"China's Gold Reserves Climb Nearly 20 Tons in July — The Private Banker (7 August 2026)","url":"https://leprivatebanker.com/2026/08/07/chinas-gold-reserves-climb-nearly-20-tons-in-july/"},
 {"title":"China's Central Bank Adds 20 Tons to Gold Reserves in July — Bloomberg (7 August 2026)","url":"https://www.bloomberg.com/news/articles/2026-08-07/china-s-central-bank-adds-20-tons-to-gold-reserves-in-july"},
 {"title":"A record quarter inside the weakest half: central banks took 289 tonnes — Carat Capital (2 August 2026)","url":"https://caratcapital.org/a-record-quarter-weakest-half.html"},
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (7 August 2026, 5:00pm EST close)","url":"https://www.kitco.com/price/precious-metals"},
])

# ========== 3. nine-thirty-eight-and-twelve-eighty-six ==========
art("nine-thirty-eight-and-twelve-eighty-six","gold-metals",False,"Gold & Metals Desk · China",5,"The Gold & Metals Desk",
["VS","NUM"],
"938 at the exchange, 1,286 at the counter",
"Shanghai Gold Exchange Au99.99 traded at 938 yuan a gram on 8 August, up 7.53 on the day. Chow Tai Fook's 24-carat counter read 1,286 yuan, a spread of 348 yuan a gram, about 37% over the benchmark.",
[
"The gap between what gold costs in China and what a Chinese jewellery counter charges for it is 348 yuan a gram. The Shanghai Gold Exchange's Au99.99 contract traded at 938 yuan a gram on the morning of 8 August, up 7.53 yuan from the previous close. On the same day Chow Tai Fook listed 24-carat jewellery at 1,286 yuan a gram, Chow Sang Sang at 1,285, Lukfook at 1,284, Lao Feng Xiang and Lao Miao at 1,283 and Zhou Liu Fu at 1,281. Every major brand sits within five yuan of every other and roughly 37% above the exchange benchmark.",
"The wider measure is larger still. The same Mandarin tally puts the distance from the Shuibei wholesale price, the Shenzhen market where most of China's gold jewellery is actually made and traded, to the highest brand counter price at 170 yuan a gram. What changed this week is the direction of travel rather than the size of the gap. On 6 August the major brands raised counter prices by close to 60 yuan a gram in a single session, Sina Finance reported, against a benchmark that moved a fraction of that. The counter is no longer following the benchmark. It is running ahead of it.",
"This paper declined to print a Chinese brand-counter figure on 7 August. Two independent reads of the same day's price stood at 1,240 and 1,297 yuan a gram, the main aggregator returned empty price cells, a second site failed on its certificate, and the house rule against printing an unverified price left nothing publishable. The 8 August figures settle it: one Mandarin financial-press table carrying six named brands, cross-checked against two independent brand-price trackers, all agreeing inside five yuan. The story pulled on Friday is the story that prints today, with the number it was missing.",
"The demand backdrop is what makes the spread interesting rather than merely wide. This paper reported on 7 August that the China Gold Association put first-half gold jewellery consumption at 132.13 tonnes, down 33.88%, against bar and coin demand of 339.34 tonnes, up 28.42%. A counter charging 37% over the exchange price into a market that has bought a third less jewellery by weight is not holding that margin out of confidence. It is holding it because the fixed cost of a branded retail network does not fall when tonnage does, and because the customer who left has gone to a product where the spread is visible, printed and small.",
"The desk's view: a 348 yuan spread is a making charge with a market of its own, and it has started moving on its own schedule. For most of the past year Chinese brand counters lagged the metal, absorbing rises and holding list prices for days, which is what a retailer does when it is defending footfall. Moving close to 60 yuan in a session, and moving further than the benchmark across two days, is what a retailer does when it has decided the volume is not coming back and the margin per gram is now the business. Any brand pricing into China this autumn should read six counter prices sitting within five yuan of one another as a collectively held floor rather than a competitive market, and should set its own making charge against 1,286 rather than against 938."
],
[
 {"title":"金价下跌了，2026年8月8日人民币与国内黄金的最新报价 — Tencent News (8 August 2026)","url":"https://news.qq.com/rain/a/20260808A05HQW00"},
 {"title":"周大福、老凤祥、周生生足金单日涨近60元/克 — Sina Finance (6 August 2026)","url":"http://finance.sina.com.cn/wm/2026-08-06/doc-inimkwtf0513950.shtml"},
 {"title":"132 tonnes of jewellery, 339 tonnes of bars: China picks a side — Carat Capital (7 August 2026)","url":"https://caratcapital.org/a-one-thirty-two-against-three-thirty-nine.html"},
])

# ========== 4. turkey-up-america-down ==========
art("turkey-up-america-down","watches",False,"Watches Desk · Exports",5,"The Watches Desk",
["VS","NUM"],
"Turkey +6.9%, America −14.8%: where Swiss watches went",
"Swiss watch exports to Turkey rose 6.9% to 165.2 million francs in the first half. Shipments to the United States fell 14.8%, Germany 10.5% and China 5.0%. India rose 31.5% and Mexico 14.9%.",
[
"The best-performing sizeable market for Swiss watches in the first half of 2026 was not in Europe, America or East Asia. Exports to Turkey rose 6.9% to 165.2 million francs, from 154.5 million in the same period of 2025 and 145.2 million in 2024, on Federation of the Swiss Watch Industry figures carried this week by the Turkish press. Turkey remains the industry's seventeenth largest market. Worldwide exports for the half came to 12.8 billion francs, down 0.7%, a total this paper filed on 21 July when the federation published it.",
"The federation's country table is where the half is decided. The United States, the industry's largest market, fell 14.8%, though it remains 2.6% ahead across two years. Germany fell 10.5%, China 5.0% and Japan 1.6%. Against that, India rose 31.5%, Mexico 14.9%, South Korea 6.5%, the United Kingdom 5.8%, Hong Kong 3.3%, Singapore 2.2% and the United Arab Emirates 1.6%. France rose 63.4%, which the federation attributes to a logistics reclassification rather than to French wrists. The growth in this half sits outside the markets Switzerland built its book on.",
"The material table says the same thing about product. Watches in precious metals fell 6.5% and steel watches fell 6.5%, while bimetallic models rose 20.0% and other metals rose 14.4%. Mechanical watches priced under 500 francs at export rose 23.8%, and the 500 to 3,000 franc band, the traditional home of the aspirational Swiss watch, fell 5.7%. Volume across the half rose even as value did not: seven million wristwatches shipped, up 2.3%, on a wristwatch value of 12.2 billion francs, down 0.6%. Switzerland sold more watches for slightly less money, in cheaper materials, to newer places.",
"The proportions want stating plainly, because a growth percentage on a small base does not replace a decline on a large one. Turkey's 165.2 million francs is about 1.3% of the half's total, a share derived by this desk from the published figures rather than published by the federation. India at 31.5% is the more consequential of the two gains and has been the trade's quiet story all year. The American fall is measured against the largest single line in the table, and whether the newer markets can absorb it is a question the second half will answer. Nothing in the first-half table answers it.",
"The desk's view: a 1.3% market growing is not a substitute for a 14.8% market falling, and the trade should resist reading Turkey as a turn. What the table does say usefully is where the marginal watch is going: to markets with young populations, currencies that make a Swiss watch a store of value, and no established grey-market depth. Turkey and India both fit that description and both grew. For a brand or a retailer planning allocation, though, the actionable line is the material split rather than the geography. Bimetallic up 20.0% against precious metals down 6.5% is a customer buying the look at a lower metal cost, and that is the same substitution this paper has recorded at Chinese and Indian jewellery counters all year."
],
[
 {"title":"Swiss watch exports in the first half of 2026 — Federation of the Swiss Watch Industry (21 July 2026)","url":"https://www.fhs.swiss/eng/2026_07_21_statistics.html"},
 {"title":"Swiss watch exports to Turkey rise as global shipments fall — Turkish Minute (6 August 2026)","url":"https://turkishminute.com/2026/08/06/swiss-watch-exports-to-turkey-rise-as-global-shipments-fall/"},
 {"title":"Swiss watch exports to Türkiye rise as major markets contract — Hürriyet Daily News (6 August 2026)","url":"https://www.hurriyetdailynews.com/swiss-watch-exports-to-turkiye-rise-as-major-markets-contract-225291"},
 {"title":"Plus 11.2%: June hands Swiss watchmaking its month back — Carat Capital (21 July 2026)","url":"https://caratcapital.org/a-plus-eleven-two-in-june.html"},
])

# ========== 5. forty-six-percent-came-back ==========
art("forty-six-percent-came-back","retail-tech",False,"Retail & Technology Desk · India",5,"The Retail Desk",
["NUM","GAP"],
"46% of Kalyan's revenue came back through the door",
"Kalyan Jewellers took ₹10,589 crore of revenue in the June quarter, up 46%, and net profit of ₹349 crore, up 32%. Recycled gold supplied more than 46% of revenue and more than 55% in June alone.",
[
"Kalyan Jewellers reported consolidated revenue of ₹10,589 crore for the quarter to 30 June, up 46% from ₹7,268 crore, and consolidated net profit of ₹349 crore, up 32%. Same-store sales in India grew about 28%. International revenue rose 35%, and Candere, the group's digital business, grew 112%. The company now runs 524 showrooms worldwide, 354 of them Kalyan-branded in India. The results were announced on 4 August.",
"The line that should interest the rest of the trade is not on the profit statement. Kalyan says its gold-recirculation campaign, run under the name Shine with India, contributed more than 46% of revenue across the quarter and more than 55% in the month of June alone. More than 46% of Kalyan's revenue came in as somebody's old gold. That is not a promotion. It is a sourcing strategy, and on the June figure it is the larger half of the business.",
"The refining end of the same trade moved in the same week. MMTC-PAMP, India's only LBMA Good Delivery refiner of gold and silver, launched a limited-edition 10-gram commemorative coin on 4 August struck entirely from 999.9-plus recycled gold, capped at 8,000 pieces in assayer-certified packaging and unveiled in New Delhi by the Olympic medallist Mirabai Chanu. A refiner marketing recycled provenance as a selling point rather than disclosing it as a compromise is a change of position, and it arrives in the same month a listed retailer reports that nearly half its revenue rests on the same metal.",
"The volume backdrop explains why both are happening now. This paper reported that Indian gold jewellery demand fell 15% by weight in the second quarter to 75.1 tonnes, its lowest second quarter since the pandemic, while the value of that demand rose about 50%. A 46% revenue increase against a national tonnage down 15% is not a share gain of that size. It is a price effect, an exchange effect and a store-count effect stacked on top of each other. Kalyan's own same-store figure of about 28% is the honest comparison, and it is still comfortably ahead of the market.",
"The desk's view: an exchange programme is a supply chain, and Kalyan is now running one. With gold above $4,300 an ounce the binding constraint on an Indian jeweller is not demand for finished pieces, it is access to metal that does not have to be imported at duty and financed at working-capital rates, and the household is the cheapest supplier in the country. The number to watch is the June figure rather than the quarterly one, because 55% says the share is still climbing. For a retailer outside India reading this as a local curiosity, the transferable part is simple: a counter that can buy metal back has a second margin and a hedge inside the same transaction, and a counter that cannot is exposed to the price twice."
],
[
 {"title":"Kalyan Jewellers Q1 PAT jumps 32% YoY to Rs 349 cr — Business Standard, Capital Market (5 August 2026)","url":"https://www.business-standard.com/markets/capital-market-news/kalyan-jewellers-q1-pat-jumps-32-yoy-to-rs-349-cr-126080500578_1.html"},
 {"title":"Kalyan Jewellers Q1 profit jumps 32 per cent as revenue tops Rs 10,589 crore — Indian Television (August 2026)","url":"https://indiantelevision.com/mam/kalyan-jewellers-q1-profit-jumps-32-per-cent-as-revenue-tops-rs-10589-crore/"},
 {"title":"Champion Mirabai Chanu Unveils MMTC-PAMP's 'Virasat' Recycled Gold Coin — The Tribune (4 August 2026)","url":"https://www.tribuneindia.com/news/business/champion-mirabai-chanu-unveils-mmtc-pamps-virasat-recycled-gold-coin-to-celebrate-indias-80th-year-of-independence/"},
 {"title":"India buys fifteen percent less — Carat Capital (31 July 2026)","url":"https://caratcapital.org/a-india-buys-fifteen-percent-less.html"},
])

# ========== 6. png-retires-litestyle ==========
art("png-retires-litestyle","retail-tech",False,"Retail & Technology Desk · Brands",4,"The Retail Desk",
["ACTOR","NUM"],
"P.N. Gadgil retires Litestyle and bets on 100 YOOU stores",
"P N Gadgil Jewellers replaced its lightweight diamond line Litestyle with a new brand, YOOU, on 8 August. It runs 13 exclusive outlets and shop-in-shop counters across five states, against a target of 100 stores by 2030.",
[
"P N Gadgil Jewellers retired a brand on Saturday and launched its replacement the same day. Litestyle by PNG, the company's lightweight diamond jewellery line, becomes YOOU, positioned for everyday rather than occasion wear and offered in 9, 14, 18 and 22-carat gold. The line currently trades through 13 exclusive outlets across Maharashtra and Goa plus shop-in-shop counters in five states. The stated target is 100 stores by 2030. Sara Tendulkar continues as brand ambassador, carried over from Litestyle.",
"The reframing is the whole announcement. Saurabh Gadgil, the chairman and managing director, describes the brand as built for contemporary collections and everyday wear rather than for weddings and festivals, which in the Indian market is a specific commercial claim and not a slogan. A lightweight diamond line lives or dies on repeat purchase rather than on occasion, and the store target is sized for that. Thirteen stores becoming a hundred is a bet on frequency, not on ticket.",
"The parent has the balance sheet to try it. P N Gadgil reported first-quarter revenue of ₹2,413 crore, up 41% year on year, and has said it intends to open roughly 103 stores across its whole portfolio by the end of the current financial year. Against that run rate, a hundred YOOU outlets by 2030 is a four-year build at a pace the group is already sustaining elsewhere, which makes the target more credible than most brand-launch numbers in this market.",
"The category is where the risk sits. Lightweight, low-carat diamond jewellery aimed at everyday wear is the most contested segment in Indian retail and the one most exposed to lab-grown substitution. This paper reported on 7 August that the cheapest lab-grown diamond studs in the American mall channel now sell at $29.99, and Indian pricing tends to follow that direction with a lag. A brand that sells the design survives that. A brand selling carat weight at a discount does not, and YOOU's 9-carat gold option suggests the company has already picked its side.",
"The desk's view: this is a positioning story rather than a results story, and it is worth filing because of what it says about where Indian retail thinks its growth is. Two Indian jewellers made news this week and both pointed the same way. Kalyan reported that more than 46% of its revenue came back through the door as recycled gold; P N Gadgil is building a chain around 9 to 18-carat pieces bought without an occasion attached. Both are answers to the same problem, which is a gold price that has made the traditional heavy-gold Indian purchase unaffordable at the old frequency. The measure to hold this against in twelve months is store count against same-store sales, because a hundred outlets that each sell less than thirteen did is an expensive way to lose."
],
[
 {"title":"PNG Jewellers launches YOOU, targets 100 stores by 2030 — ScanX (8 August 2026)","url":"https://scanx.trade/stock-market-news/companies/png-jewellers-launches-yoou-targets-100-stores-by-2030/47749514"},
 {"title":"PNG Jewellers Launches YOOU Diamond Jewellery Brand — InvestyWise (8 August 2026)","url":"https://www.investywise.com/png-jewellers-launches-new-diamond-jewellery-brand-yoou/"},
 {"title":"$29.99 at the counter: America's cheapest lab-grown diamond — Carat Capital (7 August 2026)","url":"https://caratcapital.org/a-twenty-nine-ninety-nine-at-the-counter.html"},
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

specs["four-times-melt"] = {
 **strip("By the numbers · Cuckoo Cuckoo egg, Batemans, 1 August",[
   {"fig":"£123,500","lab":"hammer, a world record for the type"},
   {"fig":"$166,600","lab":"in dollars"},
   {"fig":"≈6×","delta":"▲","dir":"up","lab":"pre-sale estimate"},
   {"fig":"323.6 g","lab":"22-carat gold, per the catalogue"},
   {"fig":"≈$41,400","lab":"metal value, derived by this desk"}]),
 "figs":[bars("Plate I","The Cuckoo Cuckoo egg · price against metal, US dollars",[
   {"l":"SALE PRICE","v":166600,"d":"$166,600","hi":True},
   {"l":"METAL VALUE (DERIVED)","v":41404,"d":"≈$41,400"}],
   "Sale price per Forbes, 8 August 2026. Metal value derived by this desk from the catalogued 323.6 grams at 22 carat and gold at $4,341.30 an ounce; not published by any source.",200)],
 "flow":flow5("A promotional egg sets a jewellery record.","The maker's name against the melt figure.","A desk with almost nothing to price.",
   "The record is four times the metal. The rest is signature and story","The Auctions Desk",
   "$13,000 for costume, £2,000 for gold: Bonhams runs Chanel in three cities","a-thirteen-thousand-for-costume.html"),
 "desk":{"split":"the premium here is documentation, not carat weight"},
 "next":nxt("six-forty-thousand-ounces","Metals","The PBoC added 640,000 ounces in July, its biggest month since 2023.",
   "thirteen-thousand-for-costume","Auctions","the-hundred-six-thousand-miss","Metals")}

specs["six-forty-thousand-ounces"] = {
 **strip("By the numbers · PBoC gold reserves, July 2026",[
   {"fig":"640,000 oz","delta":"▲","dir":"up","lab":"added in July, about 19.9 tonnes"},
   {"fig":"76.08M oz","lab":"holdings, roughly 2,366 tonnes"},
   {"fig":"21","lab":"consecutive months of buying"},
   {"fig":"$306.35B","lab":"value of the gold reserve"},
   {"fig":"≈8%","lab":"gold's share of $3.419tn reserves"}]),
 "figs":[bars("Plate I","Chinese official gold holdings · million troy ounces",[
   {"l":"END JULY 2026","v":76.08,"d":"76.08M","hi":True},
   {"l":"END JUNE 2026","v":75.44,"d":"75.44M"}],
   "People's Bank of China monthly reserve data, published 7 August 2026. Tonnage conversions are approximate.",201)],
 "flow":flow5("The biggest month since October 2023.","A pace that doubled inside a flat market.","The least price-sensitive buyer in the market.",
   "Twenty-one months of buying says the policy is the point, not the price","The Gold & Metals Desk",
   "A record quarter inside the weakest half: central banks took 289 tonnes","a-record-quarter-weakest-half.html"),
 "desk":{"split":"a central bank that buys every month is not trading, it is provisioning"},
 "next":nxt("nine-thirty-eight-and-twelve-eighty-six","Metals","The Chinese brand counter is now running ahead of the exchange benchmark.",
   "three-hundred-eighty-billion","Metals","record-quarter-weakest-half","Central Banks")}

specs["nine-thirty-eight-and-twelve-eighty-six"] = {
 **strip("By the numbers · Chinese gold, 8 August",[
   {"fig":"938","delta":"▲ +7.53","dir":"up","lab":"SGE Au99.99, yuan a gram"},
   {"fig":"1,286","lab":"Chow Tai Fook 24-carat counter"},
   {"fig":"348","lab":"the spread, yuan a gram"},
   {"fig":"≈37%","lab":"counter over benchmark"},
   {"fig":"170","lab":"Shuibei wholesale to top brand counter"}]),
 "figs":[bars("Plate I","Gold in China, 8 August 2026 · yuan a gram",[
   {"l":"CHOW TAI FOOK 24K","v":1286,"d":"1,286","hi":True},
   {"l":"CHOW SANG SANG 24K","v":1285,"d":"1,285"},
   {"l":"LAO FENG XIANG 24K","v":1283,"d":"1,283"},
   {"l":"ZHOU LIU FU 24K","v":1281,"d":"1,281"},
   {"l":"SGE Au99.99 BENCHMARK","v":938,"d":"938"}],
   "Mandarin financial press table, Tencent News, 8 August 2026, cross-checked against two independent brand-price trackers.",202)],
 "flow":flow5("A 348 yuan gap on the same metal.","The counter stops lagging the benchmark.","A margin held into a third less volume.",
   "The counter is no longer following the benchmark. It is running ahead of it","The Gold & Metals Desk",
   "132 tonnes of jewellery, 339 tonnes of bars: China picks a side","a-one-thirty-two-against-three-thirty-nine.html"),
 "desk":{"split":"a 348 yuan spread is a making charge with a market of its own"},
 "next":nxt("forty-six-percent-came-back","Retail","More than 46% of Kalyan's revenue came in as recycled gold.",
   "one-thirty-two-against-three-thirty-nine","Metals","china-lowest-since-2004","Demand")}

specs["turkey-up-america-down"] = {
 **strip("By the numbers · Swiss watch exports, first half 2026",[
   {"fig":"165.2M","delta":"▲ +6.9%","dir":"up","lab":"francs to Turkey, 17th market"},
   {"fig":"−14.8%","delta":"▼","dir":"down","lab":"United States, the largest market"},
   {"fig":"+31.5%","delta":"▲","dir":"up","lab":"India, the biggest gainer"},
   {"fig":"12.8B","delta":"▼ −0.7%","dir":"down","lab":"francs, worldwide"},
   {"fig":"+2.3%","delta":"▲","dir":"up","lab":"wristwatch units, seven million"}]),
 "figs":[bars("Plate I","Swiss watch exports by market · first half 2026, % year on year",[
   {"l":"INDIA","v":31.5,"d":"+31.5%","hi":True},
   {"l":"MEXICO","v":14.9,"d":"+14.9%"},
   {"l":"TURKEY","v":6.9,"d":"+6.9%"},
   {"l":"UNITED KINGDOM","v":5.8,"d":"+5.8%"},
   {"l":"HONG KONG","v":3.3,"d":"+3.3%"},
   {"l":"CHINA","v":-5.0,"d":"−5.0%"},
   {"l":"GERMANY","v":-10.5,"d":"−10.5%"},
   {"l":"UNITED STATES","v":-14.8,"d":"−14.8%"}],
   "Federation of the Swiss Watch Industry, published 21 July 2026. France, up 63.4%, is excluded as a logistics reclassification.",203)],
 "flow":flow5("The half's best market is the seventeenth.","A country table that points away from the core.","Growth on a small base, decline on a large one.",
   "The growth in this half sits outside the markets Switzerland built its book on","The Watches Desk",
   "Plus 11.2%: June hands Swiss watchmaking its month back","a-plus-eleven-two-in-june.html"),
 "desk":{"split":"a 1.3% market growing is not a substitute for a 14.8% market falling"},
 "next":nxt("four-times-melt","Auctions","A 1983 Garrard egg made £123,500, four times the value of its gold.",
   "plus-eleven-two-in-june","Watches","independents-pass-lvmh","Watches")}

specs["forty-six-percent-came-back"] = {
 **strip("By the numbers · Kalyan Jewellers, quarter to 30 June",[
   {"fig":"₹10,589cr","delta":"▲ +46%","dir":"up","lab":"consolidated revenue"},
   {"fig":"₹349cr","delta":"▲ +32%","dir":"up","lab":"consolidated net profit"},
   {"fig":">46%","lab":"of revenue from recycled gold"},
   {"fig":">55%","lab":"recycled share in June alone"},
   {"fig":"524","lab":"showrooms worldwide, 354 in India"}]),
 "figs":[bars("Plate I","Kalyan Jewellers, Q1 FY27 · per cent year on year",[
   {"l":"CANDERE, DIGITAL","v":112,"d":"+112%"},
   {"l":"REVENUE","v":46,"d":"+46%","hi":True},
   {"l":"INTERNATIONAL REVENUE","v":35,"d":"+35%"},
   {"l":"NET PROFIT","v":32,"d":"+32%"},
   {"l":"INDIA SAME-STORE SALES","v":28,"d":"≈+28%"}],
   "Company results announced 4 August 2026, as reported by Business Standard's Capital Market service and Indian Television.",204)],
 "flow":flow5("A quarter carried by a price and a programme.","The line that is not on the profit statement.","Value up 46%, national tonnage down 15%.",
   "More than 46% of Kalyan's revenue came in as somebody's old gold","The Retail Desk",
   "India buys fifteen percent less","a-india-buys-fifteen-percent-less.html"),
 "desk":{"split":"an exchange programme is a supply chain, and Kalyan is now running one"},
 "next":nxt("png-retires-litestyle","Retail","P N Gadgil replaced Litestyle with YOOU and set a 100-store target.",
   "india-buys-fifteen-percent-less","Demand","luk-fook-fixed-price","Retail")}

specs["png-retires-litestyle"] = {
 **strip("By the numbers · YOOU by PNG, launched 8 August",[
   {"fig":"13","lab":"exclusive outlets, Maharashtra and Goa"},
   {"fig":"5","lab":"states with shop-in-shop counters"},
   {"fig":"100","lab":"store target by 2030"},
   {"fig":"9–22kt","lab":"gold range offered"},
   {"fig":"₹2,413cr","delta":"▲ +41%","dir":"up","lab":"parent Q1 revenue"}]),
 "figs":[bars("Plate I","YOOU by PNG · outlets today against the 2030 target",[
   {"l":"TARGET BY 2030","v":100,"d":"100","hi":True},
   {"l":"EXCLUSIVE OUTLETS TODAY","v":13,"d":"13"}],
   "Company announcement, 8 August 2026, as reported by ScanX and InvestyWise.",205)],
 "flow":flow5("A brand retired and replaced in a day.","Everyday wear is a commercial claim, not a slogan.","The most contested segment in Indian retail.",
   "Thirteen stores becoming a hundred is a bet on frequency, not on ticket","The Retail Desk",
   "$29.99 at the counter: America's cheapest lab-grown diamond","a-twenty-nine-ninety-nine-at-the-counter.html"),
 "desk":{"split":"a hundred outlets that each sell less than thirteen did is an expensive way to lose"},
 "next":nxt("turkey-up-america-down","Watches","Turkey grew 6.9% while America fell 14.8% in the Swiss half.",
   "twenty-nine-ninety-nine-at-the-counter","Retail","forty-six-percent-came-back","Retail")}

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
