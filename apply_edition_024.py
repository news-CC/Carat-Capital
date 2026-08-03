#!/usr/bin/env python3
# Edition No. 024 - 2026-08-03. Prepends 5 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-03"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - seventy-three-million-in-shoes ==========
art("seventy-three-million-in-shoes","diamonds",True,"Lead Story · Diamonds Desk",5,"The Diamonds Desk",
["NUM","STAKES","GAP"],
"$73 million in shoes, and a serial number to collect it",
"Vietnamese police have re-scaled the smuggling case this desk reported on July 16. The ring now stands at $73 million of stones, more than 30 detained, and a state-owned retailer holding 3,400 of the diamonds.",
[
"The Vietnamese diamond-smuggling case has been re-scaled, and the new arithmetic is roughly seven times the old one. Investigators now put the network at $73 million of diamonds moved into Vietnam, of which about $57 million of stones have been identified, with more than 30 people arrested or detained. The count of stones is unchanged at at least 28,000, carried on 141 separate occasions since 2024. This desk filed the case on July 16 with 22 people charged and a value of 280 billion dong, about $10.65 million, which was the figure in the charge sheet at the time. That number described the prosecution. The $73 million describes the pipeline.",
"The mechanism is the part the trade should read twice. Couriers carried stones in luggage, shoes and clothing on commercial flights from Hong Kong into Vietnamese airports, with orders and prices arranged over WhatsApp. Handover was controlled by a device that costs nothing and leaves no record: the courier released the goods only to a recipient holding a bank note whose eleven-character code matched one agreed in advance. Police describe couriers using the serial numbers from US dollar bills as a secret authentication code. There is no ledger to subpoena, no wallet to trace, and no message that has to name a stone.",
"The stones did not stay in a back room. Saigon Jewelry Company, the state-owned retailer that sets Vietnam's benchmark gold price, bought more than 3,400 of them for about $19 million. Goods moved at roughly a third below market, which is the discount that makes an undocumented parcel attractive and also the discount that should have prompted a question. Police believe the operation was directed by an Indian national living in Hong Kong, sourcing in India and consolidating in Hong Kong before the flights.",
"The certification layer is what turns a customs case into a trade case. The former director of P-Lab, the grading subsidiary wholly owned by Phu Nhuan Jewelry that handles about 70% of Vietnamese certification, is among those charged, and the allegation is that smuggled stones were re-papered with the lab's own certificates before distribution. A country that runs most of its consumer trust through one laboratory has a single point of failure, and this case is what failure looks like when it is discovered rather than prevented.",
"The desk's view: the number that changed is less important than the number that did not. Twenty-eight thousand stones crossed a border 141 times over two years and were absorbed by named retailers, which means the failure was not at the airport but at the counter, where a parcel priced a third below market was bought without a paper trail anyone could later produce. Every jurisdiction with a dominant domestic grading lab should read the P-Lab allegation as a description of its own exposure. Certification is a trust monopoly, and a trust monopoly is worth exactly what its weakest director decides it is worth."
],
[
 {"title":"$73m Diamond Smuggling Suspects and the Dollar Bill Codes — IDEX Online (July 30, 2026)","url":"https://www.idexonline.com/FullArticle?Id=51313"},
 {"title":"Vietnam jeweller rattled after India-Hong Kong diamond-smuggling ring bust — South China Morning Post","url":"https://www.scmp.com/news/asia/southeast-asia/article/3360597/vietnam-jeweller-rattled-ex-officials-arrest-over-india-hong-kong-gem-smuggling-ring"},
 {"title":"Gems Hidden in Shoes as Vietnam Details India Smuggling Link — Bloomberg","url":"https://www.bloomberg.com/news/articles/2026-07-16/gems-hidden-in-shoes-as-vietnam-highlights-india-smuggling-link"},
 {"title":"Vietnam diamond scandal shakes trust in certification system — Nikkei Asia","url":"https://asia.nikkei.com/spotlight/society/crime/vietnam-diamond-scandal-shakes-trust-in-certification-system"},
])

# ========== 2. china-lowest-since-2004 ==========
art("china-lowest-since-2004","gold-metals",False,"Gold & Metals Desk · Jewellery demand",4,"The Bullion Desk",
["ACTOR","RECORD","NUM"],
"China's gold counter falls to its lowest since 2004",
"Chinese gold jewellery demand fell 28% to 50 tonnes in the second quarter, the weakest since 2004, and 30% across the half to 136 tonnes. The value of that demand still rose 11%.",
[
"The weakest jewellery quarter of the modern gold era belongs to China. Mainland Chinese gold jewellery demand fell to 50.0 tonnes in the second quarter of 2026, down 28% from 69.2 tonnes a year earlier and the lowest second-quarter figure since 2004, according to the World Gold Council's Gold Demand Trends published on July 30. Across the first half the country consumed 136 tonnes, down 30%. The council called the global quarter \"one of the weakest second quarters in our data series\", and China is where most of that weakness sits.",
"The value line moves the other way, and the gap is the whole story. Chinese jewellery demand was worth about $21 billion in the first half, up 11% year on year, against a tonnage that fell almost a third. Consumers in the world's largest gold jewellery market bought roughly 30% less metal and paid roughly 11% more for it. For a manufacturer that is not a demand collapse so much as a change in what is being sold: fewer grams, higher price per gram, and a product mix drifting toward lighter pieces and higher labour content.",
"The rest of the map fell in the same direction at different speeds. India took 75.1 tonnes in the quarter, down 15% and its lowest second quarter since the pandemic, on first-half demand of 141 tonnes worth about $21 billion, up 26% by value. The Middle East fell 19% to 32.2 tonnes. The United States fell 25% to 22.2 tonnes, the sharpest percentage decline among the major markets and one that has attracted almost no comment in a trade that has spent the summer describing American demand as the strong lane. Global fabrication came to 278.2 tonnes against 335.3 tonnes a year earlier.",
"That American figure deserves separating out, because it sits awkwardly beside the retail data. Tenoris put United States jewellery revenue up 13% in June and about 9% across the half, and Bain named jewellery the strongest category in luxury. Both can be true alongside a 25% fall in gold tonnage, because revenue is measured in dollars and fabrication is measured in grams. What the two together describe is an American counter selling roughly the same money through materially less metal, which is exactly the substitution the price has been forcing everywhere else.",
"The desk's view: the tonnage series is now the only honest measure of jewellery demand, and it is the one nobody quotes. Value figures rise mechanically with the metal and will keep printing records for as long as gold holds above $4,000 an ounce, which makes them useless for judging whether anyone is actually buying. China at its lowest second quarter in twenty-two years, on a value line that rose, is the cleanest example available of a market that looks healthy in money and is contracting in metal. Price your inventory in grams and read the press releases in dollars."
],
[
 {"title":"Gold Demand Trends Q2 2026: Jewellery — World Gold Council (30 July 2026)","url":"https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q2-2026/jewellery"},
 {"title":"Gold Demand Trends Q2 2026 — World Gold Council","url":"https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q2-2026"},
 {"title":"US Jewelry Sales Grow in H1 2026 — Tenoris","url":"https://www.tenoris.bi/us-jewelry-sales-continue-to-grow-in-h1-2026/"},
])

# ========== 3. silver-leads-the-reopen ==========
art("silver-leads-the-reopen","gold-metals",False,"Gold & Metals Desk · The tape",4,"The Bullion Desk",
["NUM","VS"],
"Silver leads the reopen at $58.05, gold adds 0.29%",
"The first session since Friday has gold at $4,053.30, up $11.60, and silver at $58.05, up 1.06%. Platinum is $1,647.00. The ADP report lands midweek and payrolls on Friday.",
[
"Metals reopened higher and silver did the work. At 6:01am New York time on Monday, Kitco's spot page had gold bid at $4,053.30 an ounce, up $11.60 or 0.29% against Friday's 5pm close of $4,041.70, having traded a session range of $4,045.80 to $4,083.50. This tape prints that live quotation rather than a settlement because Friday's close has now been carried through two editions, and a third day of unchanged would report a stillness the market no longer has.",
"Silver is the mover. It bid $58.05, up 61.1 cents or 1.06%, on a range of $57.68 to $58.76, which is the largest percentage gain of the four metals and takes the gold to silver ratio to about 69.8 ounces. Platinum bid $1,647.00, up $3.00 or 0.18%, on a range of $1,641.00 to $1,676.00. Palladium bid $1,259.00, up $3.00, on a range of $1,257.00 to $1,322.00. All four are higher, none by much, and the two wide intraday ranges in platinum and palladium say more about thin holiday liquidity than about conviction.",
"The week is built around labour data. The ADP employment report lands midweek and the Bureau of Labor Statistics releases non-farm payrolls on Friday, the first complete read on American hiring since the Federal Reserve held rates on July 29 with three dissents. Gold traded above $4,100 on that decision and gave the move back within two sessions as the dollar recovered, which is a fair description of how little either side of this market currently believes.",
"At the bench the working figure has barely moved. Gold at $4,053.30 an ounce is about $130.32 a gram of fine metal before refining, alloy, loss and making charge, against $129.95 on Friday's close. Silver above $58 matters more for the sterling and alternative-metals side of a case, where a dollar an ounce on the raw material is a real percentage of a finished item's cost in a way it never is on a gold chain. July closed with gold up about half a percent, its first higher month since February, and the white metals lower across the same month.",
"The desk's view: quote off the settlement, not off the screen, and this edition's tape is the exception that proves it. A 0.29% gain in an Asian and European session before New York has opened is not a price discovery event, it is a placeholder until Friday, and a jeweller who repriced a window on it would be repricing again by the weekend. The number worth writing down is Friday's payroll print, which will either break a range that has held for six weeks or extend it. Everything between now and then is noise with a decimal point."
],
[
 {"title":"Precious Metals Spot Prices — Kitco (3 August 2026, 6:01am New York)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Gold — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/gold"},
])

# ========== 4. michael-hill-adds-two ==========
art("michael-hill-adds-two","retail-tech",False,"Retail & Tech Desk · Results",4,"The Retail Desk",
["ACTOR","NUM","VS"],
"Michael Hill adds 2%, and closes eight stores to do it",
"Group revenue rose 2% to A$654.7 million in the year to June 28, with same-store sales up 3% and Canada a record 7%. The chain closed eight stores and opened two.",
[
"Michael Hill has finished its financial year with the shape a mature chain wants and rarely gets: sales up, footprint down. Group revenue for the twelve months to June 28 was A$654.7 million, about $459.5 million, an increase of 2%. Same-store sales, the measure that strips out the effect of opening and closing shops, rose 3% across the group. The chain closed eight stores over the year and opened two, ending with 281: 157 in Australia, 81 in Canada and 43 in New Zealand.",
"Canada is the number that stands out. Same-store sales there rose 7%, which the company describes as a record, on segment revenue of C$169.3 million, about $120.8 million. Australia, much the largest market, grew same-store sales 4.8% on revenue of A$364.6 million. New Zealand, the group's home market and its smallest, grew 3.6% on NZ$108.9 million. All three markets grew on a like-for-like basis in the same year, which has not been a common outcome in mid-market jewellery retail through 2026.",
"The closures are the strategy rather than the casualty. Four Australian stores, two Canadian and two New Zealand shops went, against one opening in Australia and one in Canada, a net reduction of six on a base of 287. A chain that removes 2% of its doors while adding 3% on a like-for-like basis is converting store count into store productivity, which is the only lever available to a mall-anchored jeweller facing rents that do not fall and a metal cost that does not either.",
"The result belongs to a wider pattern this desk has been tracking all summer. Gold above $4,000 an ounce has pushed the mid-market toward lighter pieces, higher average tickets and fewer units, and the chains reporting well are the ones with pricing architecture rather than volume. Chief executive Jonathan Waecker put the emphasis on the second half, saying growth was \"significantly accelerating in Canada and New Zealand\". The group has not disclosed earnings alongside these sales figures, which is the missing half of the picture.",
"The desk's view: judge this one again when the profit line lands, because 2% of revenue growth against a metal that rose for most of the year is compatible with several very different margin outcomes. What is already legible is the store maths, and it is the right maths. Mid-market jewellery has spent a decade being told to close doors and has mostly closed them in defeat, after the like-for-like number had already collapsed. Closing eight while the remaining shops each sell 3% more is the same action taken from a position of choice, and it is the difference between managing a decline and managing a portfolio."
],
[
 {"title":"Streamlined Focus Buoys Michael Hill Revenue — Rapaport (2 August 2026)","url":"https://rapaport.com/news/streamlined-focus-buoys-michael-hill-revenue/"},
 {"title":"Michael Hill International — investor centre","url":"https://investor.michaelhill.com/"},
])

# ========== 5. shoplifting-down-fraud-up ==========
art("shoplifting-down-fraud-up","retail-tech",False,"Retail & Tech Desk · Security",4,"The Retail Desk",
["NUM","VS"],
"Shoplifting falls 12.4%, and the fraud desk fills up",
"The National Retail Federation's 2026 study has shoplifting incidents down 12.4% and merchandise theft down 8.1%, while 69% of retailers report rising phone scams and 42% report gift-card fraud.",
[
"The theft numbers improved and the loss numbers did not, which is the whole of the 2026 retail crime picture in one sentence. The National Retail Federation's Impact of Retail Theft and Violence study, published in late July, found shoplifting incidents down 12.4% in 2025 and merchandise theft down 8.1% against 2024. Against that, 69% of retailers reported an increase in phone scams, 42% reported growth in gift-card theft and fraud, 40% reported organised retail crime driving shoplifting, 36% reported rising cargo and supply-chain theft, and half reported more repeat offenders. Jewellery, gold and watches rank among the categories generating the highest dollar losses to organised groups.",
"The jewellery-specific series says the same thing in harder numbers. The Jewelers' Security Alliance annual report, published in May, counted 1,233 crimes against United States jewellery firms in 2025, down 13% from 1,420. Total dollar losses rose to $144.7 million from $142.5 million. On-premises burglaries fell 14% to 262 and robberies were flat at 218. Fewer incidents, each one more expensive, is the same divergence the federation found across all of retail, and it is what happens when casual theft declines while organised theft does not.",
"The violence line is the one that should change behaviour. Robberies involving guns, mace or vehicles rose to 27% of the total in 2025 from 17% in 2024. Incidents involving mace or pepper spray went from 3 to 14. Vehicles driven into stores during or shortly after trading hours went from none reported in 2024 to 13. Crimes at jewellers' own homes rose from 4 to 11. Two people in the industry died in 2025, against four the year before. Scott Guginsky of the alliance framed the priority in six words: \"Jewelry can be replaced. Human lives can't.\"",
"For an independent the practical exposure has migrated away from the display case. A phone scam, a fraudulent gift-card transaction or a diverted shipment does not require anyone to enter the shop, does not appear on the security camera, and is frequently written off as a bad debt rather than logged as a crime, which means the true figure sits above the reported one. The categories growing fastest are precisely the ones least likely to be counted, and a 12.4% fall in shoplifting is not evidence that the total is falling.",
"The desk's view: the declining headline is the dangerous part of this data set, because a jeweller reading only the first line will conclude the risk is receding at exactly the point the loss per incident is rising and the weapons are more common. Insurance schedules, opening procedures and shipment verification should be written against the second and third paragraphs of these reports, not the first. Two deaths is a better year than four and is not a good year. The correct reading of 2025 is that the trade got hit less often and hurt more each time."
],
[
 {"title":"Shoplifting Declines, but Fraud and Organized Retail Crime Challenge Jewelers — JCK (31 July 2026)","url":"https://www.jckonline.com/editorial-article/shoplifting-fraud-crime-jewelers/"},
 {"title":"JSA's 2025 Crime Report Shows 'Concerning' Rise in Violence — National Jeweler (13 May 2026)","url":"https://nationaljeweler.com/articles/14966-jsa-s-2025-crime-report-shows-concerning-rise-in-violence"},
 {"title":"U.S. Jewelry Crime Statistics — Jewelers' Security Alliance","url":"https://jewelerssecurity.org/crime-statistics/"},
 {"title":"Dollar Losses Up, Number of Crimes Down: JSA 2025 Annual Crime Report — AGTA","url":"https://agta.org/dollar-losses-up-number-of-crimes-down-takeaways-from-the-jewelers-security-alliance-2025-annual-crime-report/"},
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

specs["seventy-three-million-in-shoes"] = {
 **strip("The case · restated",[
   {"fig":"$73M","dir":"up","lab":"value of the ring"},
   {"fig":"28,000+","lab":"stones, 141 trips"},
   {"fig":"30+","dir":"up","lab":"arrested or detained"},
   {"fig":"3,400","lab":"stones bought by SJC"},
   {"fig":"−33%","dir":"down","lab":"typical discount to market"}]),
 "figs":[bars("Plate I","What the case was said to be worth",[
   {"l":"CHARGE SHEET, 16 JULY","v":10.65,"d":"$10.65M"},
   {"l":"STONES IDENTIFIED","v":57,"d":"$57M"},
   {"l":"NETWORK, 30 JULY","v":73,"d":"$73M","hi":True}],
   "US dollars. The stone count of 28,000 has not changed. Vietnamese police via IDEX.",173)],
 "flow":flow5("Seven times the old arithmetic.","A code that leaves no record.","One lab, one point of failure.",
   "the serial numbers from US dollar bills as a secret authentication code","The Diamonds Desk",
   "28,000 diamonds, one lab","a-vietnam-certificate-scandal.html"),
 "desk":{"split":"the failure was not at the airport but at the counter"},
 "next":nxt("vietnam-certificate-scandal","The case","The former head of P-Lab is among those charged.",
   "gia-lights-up-fluorescence","Grading","zero-for-antwerp","Tariffs")}

specs["china-lowest-since-2004"] = {
 **strip("By the numbers · gold jewellery, Q2 2026",[
   {"fig":"50.0 t","dir":"down","lab":"China, −28%"},
   {"fig":"2004","lab":"last weaker Chinese quarter"},
   {"fig":"136 t","dir":"down","lab":"China, first half, −30%"},
   {"fig":"22.2 t","dir":"down","lab":"United States, −25%"},
   {"fig":"$21B","dir":"up","lab":"Chinese H1 value, +11%"}]),
 "figs":[bars("Plate I","Second-quarter jewellery demand, by market",[
   {"l":"INDIA","v":75.1,"d":"75.1 t, −15%"},
   {"l":"CHINA","v":50.0,"d":"50.0 t, −28%","hi":True},
   {"l":"MIDDLE EAST","v":32.2,"d":"32.2 t, −19%"},
   {"l":"UNITED STATES","v":22.2,"d":"22.2 t, −25%"}],
   "Tonnes, Q2 2026. World Gold Council, Gold Demand Trends, 30 July 2026.",174)],
 "flow":flow5("The weakest quarter of the modern era.","Thirty percent less metal, eleven percent more money.","The American line nobody quoted.",
   "Consumers in the world's largest gold jewellery market bought roughly 30% less metal and paid roughly 11% more for it.","The Bullion Desk",
   "278 tonnes, the smallest jewellery quarter","a-two-seventy-eight-tonnes.html"),
 "desk":{"split":"the tonnage series is now the only honest measure of jewellery demand"},
 "next":nxt("two-seventy-eight-tonnes","Jewellery","The smallest jewellery quarter since the pandemic.",
   "india-buys-fifteen-percent-less","India","china-takes-173-tonnes","Imports")}

specs["silver-leads-the-reopen"] = {
 **strip("The tape · 3 August, 6:01am New York",[
   {"fig":"$4,053.30","dir":"up","lab":"gold, +0.29%"},
   {"fig":"$58.05","dir":"up","lab":"silver, +1.06%"},
   {"fig":"$1,647.00","dir":"up","lab":"platinum, +0.18%"},
   {"fig":"69.8","lab":"gold to silver ratio"},
   {"fig":"Friday","lab":"non-farm payrolls"}]),
 "figs":[bars("Plate I","Change against Friday's 5pm close, in percent",[
   {"l":"SILVER","v":1.06,"d":"+1.06%","hi":True},
   {"l":"GOLD","v":0.29,"d":"+0.29%"},
   {"l":"PALLADIUM","v":0.24,"d":"+0.24%"},
   {"l":"PLATINUM","v":0.18,"d":"+0.18%"}],
   "Kitco spot bids at 6:01am New York, 3 August 2026, against the 31 July close.",175)],
 "flow":flow5("Higher, and silver did the work.","Two wide ranges, thin liquidity.","The bench number barely moved.",
   "All four are higher, none by much","The Bullion Desk",
   "Gold opens August and waits on payrolls","a-gold-waits-on-payrolls.html"),
 "desk":{"split":"quote off the settlement, not off the screen"},
 "next":nxt("gold-waits-on-payrolls","Week ahead","Six weeks into a range, with payrolls on Friday.",
   "gold-ends-july-higher","The month","white-metals-close-the-month","Metals")}

specs["michael-hill-adds-two"] = {
 **strip("By the numbers · Michael Hill, year to 28 June",[
   {"fig":"A$654.7M","dir":"up","lab":"group revenue, +2%"},
   {"fig":"+3%","dir":"up","lab":"same-store sales, group"},
   {"fig":"+7%","dir":"up","lab":"Canada, a record"},
   {"fig":"281","dir":"down","lab":"stores, from 287"},
   {"fig":"8","dir":"down","lab":"closures against 2 openings"}]),
 "figs":[bars("Plate I","Same-store sales growth, by market",[
   {"l":"CANADA","v":7.0,"d":"+7.0%","hi":True},
   {"l":"AUSTRALIA","v":4.8,"d":"+4.8%"},
   {"l":"NEW ZEALAND","v":3.6,"d":"+3.6%"},
   {"l":"GROUP","v":3.0,"d":"+3.0%"}],
   "Financial year to 28 June 2026. Michael Hill via Rapaport.",176)],
 "flow":flow5("Sales up, footprint down.","Canada is the number that stands out.","The closures are the strategy.",
   "A chain that removes 2% of its doors while adding 3% on a like-for-like basis is converting store count into store productivity","The Retail Desk",
   "The average ticket did the lifting","a-average-ticket-carries-the-half.html"),
 "desk":{"split":"judge this one again when the profit line lands"},
 "next":nxt("average-ticket-carries-the-half","US retail","Fewer buyers, spending more, carried the half.",
   "titan-makes-it-three","India","the-storefront-that-isnt","Retail")}

specs["shoplifting-down-fraud-up"] = {
 **strip("By the numbers · retail crime, 2025",[
   {"fig":"−12.4%","dir":"down","lab":"shoplifting incidents"},
   {"fig":"1,233","dir":"down","lab":"crimes against jewellers, −13%"},
   {"fig":"$144.7M","dir":"up","lab":"jewellery losses, from $142.5M"},
   {"fig":"27%","dir":"up","lab":"robberies with a weapon, from 17%"},
   {"fig":"13","dir":"up","lab":"vehicle ram-raids, from 0"}]),
 "figs":[bars("Plate I","Retailers reporting an increase, by crime type",[
   {"l":"PHONE SCAMS","v":69,"d":"69%","hi":True},
   {"l":"REPEAT OFFENDERS","v":50,"d":"50%"},
   {"l":"GIFT-CARD FRAUD","v":42,"d":"42%"},
   {"l":"ORGANISED SHOPLIFTING","v":40,"d":"40%"},
   {"l":"CARGO THEFT","v":36,"d":"36%"}],
   "National Retail Federation, Impact of Retail Theft and Violence, 2026.",177)],
 "flow":flow5("Theft down, losses up.","Fewer incidents, each more expensive.","The exposure left the display case.",
   "Fewer incidents, each one more expensive","The Retail Desk",
   "Consumer confidence slips to 90.8","a-confidence-slips-to-ninety.html"),
 "desk":{"split":"the declining headline is the dangerous part of this data set"},
 "next":nxt("the-storefront-that-isnt","Retail","The storefront that is not a storefront.",
   "confidence-slips-to-ninety","Consumer","gia-lights-up-fluorescence","Grading")}

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
assert leads==["seventy-three-million-in-shoes"], f"lead set wrong: {leads}"
for s in specs: editorial[s]=specs[s]

(C/"articles.json").write_text(json.dumps(articles,ensure_ascii=False,indent=1))
(C/"editorial.json").write_text(json.dumps(editorial,ensure_ascii=False,indent=1))
print("articles now:",len(articles)," specs now:",len(editorial)," lead:",leads)
for d in NEW: print("  ",d["desk"].ljust(12), str(len(" ".join(d["body"]).split())).rjust(4),"w  ",d["slug"])
print("OK")
