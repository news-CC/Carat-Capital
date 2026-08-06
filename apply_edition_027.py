#!/usr/bin/env python3
# Edition No. 027 - 2026-08-06. Prepends 6 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-06"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - silver-alone-in-the-red ==========
art("silver-alone-in-the-red","gold-metals",True,"Lead Story · Gold & Metals Desk",5,"The Gold & Metals Desk",
["NUM","VS"],
"$4,270.90, a seven-week high, and silver alone in the red",
"At 6:03am New York gold bid $4,270.90, up 0.58% and a fourth consecutive session higher. Platinum added 1.33% to $1,753.00 and palladium 1.48% to $1,367.00. Silver fell 0.41% to $61.67, widening the ratio to 69.3.",
[
"Gold reached its highest level in seven weeks on Thursday, and the metal that carried it there stopped. At 6:03am New York time Kitco had gold bid at $4,270.90 an ounce, up $24.70 or 0.58% on the session, a fourth consecutive advance. Platinum was bid at $1,753.00, up $23.00 or 1.33%; palladium at $1,367.00, up $20.00 or 1.48%. Silver was bid at $61.67, down 25 cents or 0.41%, the only one of the four in the red. Against the 5:58am mark this paper carried on Wednesday, $4,157.80, gold has added $113.10 an ounce, or 2.72%, in twenty-four hours.",
"Silver has been the engine of this rally all week, and on Thursday it was the only metal in the red. It rose 3.27% on Wednesday against gold's 1.99%, and 3.2% the session before that, pulling the gold to silver ratio down to 67.8 from about 69.0. Thursday's divergence pushes that ratio back out to 69.3, undoing two sessions of tightening in one. A rally in which the high-beta metal turns first is a rally that has stopped recruiting new money and started running on the slower leg, which is what the platinum and palladium prints look like: both are up on the day and both are up less than silver was up yesterday.",
"For the bench the number is the gram, and it has moved again. Fine gold at $4,270.90 an ounce is $137.31 a gram, against $133.68 on Wednesday and $130.17 on Tuesday. That is $3.63 a gram added to the metal cost of every piece in a case since yesterday morning, and $7.14 a gram since Tuesday. Platinum at $1,753.00 now stands at 41.0% of the gold price, a shade below the 42.0% this desk marked on Wednesday, because gold rose faster than platinum did.",
"Two things belong on the record before anyone quotes off this. First, the marks disagree by the hour: this paper's own overnight tape recorded gold at $4,276.60 at 4:58am, $5.70 above the 6:03am bid carried here, and read silver as dead flat at $61.92 rather than down. A reader working from a headline rather than a timestamp is working from a different number. Second, Friday is the event. The Bureau of Labor Statistics releases July non-farm payrolls at 8:30am, the first full read on American hiring since the Federal Reserve held on 29 July with three dissents, and June's print came in at 57,000. This desk flagged that release as a binary on 2 August and has nothing to add until it lands.",
"The desk's view: a rally that loses its fastest metal first is a rally in its late innings, and Friday decides whether it has another one. Silver turning red while gold makes a seven-week high is the clearest internal warning this tape has printed all week, because silver leads both directions and it has now led down. On the diamond lines nothing moved: NAT1 and LGD1 are both carried unchanged, the lab-grown reference again because two trackers stood 28% apart at $709 and $555 and neither can honestly be printed as a market. Quote the timestamp with the price this week, and do not reprice a case before Friday morning."
],
[
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (6 August 2026, 6:03am EST)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Gold Price Surges to Seven-Week High: XAU/USD Eyes $4,334 as Dollar Slides — FX Leaders (6 August 2026)","url":"https://www.fxleaders.com/news/2026/08/06/gold-price-surges-seven-week-high-xau-usd-eyes-4334-dollar-slides/"},
 {"title":"The Same Force That Crushed Gold All Year Just Flipped — GoldSilver (August 2026)","url":"https://goldsilver.com/industry-news/goldsilver-news/gold-price-iran-oil-drop-august-2026/"},
 {"title":"US Employment Situation (Non-Farm Payrolls), release 7 August 2026 — Bureau of Labor Statistics","url":"https://www.bls.gov/news.release/empsit.nr0.htm"},
])

# ========== 2. alrosa-books-the-loss ==========
art("alrosa-books-the-loss","diamonds",False,"Diamonds Desk · Russia",5,"The Diamonds Desk",
["ACTOR","NUM","STAKES"],
"Alrosa books a $134 million loss and starts idling the pits",
"Revenue fell 36% to 74.2 billion roubles, about $932.5 million, and the world's largest rough producer swung to a net loss of 10.67 billion roubles, about $134.1 million, from a $490.1 million profit. Several open pits go to care and maintenance this year.",
[
"The world's largest diamond producer by volume has stopped making money. Alrosa's first-half accounts show revenue of 74.2 billion roubles, about $932.5 million, down 36% year on year, and a net loss of 10.67 billion roubles, about $134.1 million, against a net profit of 39 billion roubles, about $490.1 million, in the first half of 2025. Cost of sales fell 20% to 69.5 billion roubles, about $873.4 million, which is the whole problem in one line: revenue fell nearly twice as fast as the cost of producing it.",
"Part of the swing is arithmetic rather than trading. The comparative half carried about 53.1 billion roubles, some $667.3 million, of non-operating income, including roughly 30 billion roubles, about $377 million, from the sale of Alrosa's stake in Angola's Catoca venture. Strip that out and the 2025 base was already a thin operating year dressed up by a disposal. What is not arithmetic is the 36% revenue fall, which is a volume and price statement about rough demand, and it sits alongside De Beers' consolidated realised price of $105 a carat for the same six months, down 32%, which this desk filed on 31 July.",
"The operational response is the part the trade should read twice. Alrosa is preparing to place several open-pit mines into care and maintenance during 2026, and has suspended mining at Severalmaz, which accounts for roughly 10% of Russian diamond output. Care and maintenance is not a closure and it is not a pause in the Venetia sense. It is a mine kept alive at minimum cost with the option to restart, and it is the cheapest way a producer can take carats out of the market without conceding the reserve. The company has been explicit for months that the intent is supply discipline rather than incapacity.",
"The guidance figure now circulating with this news needs dating honestly, because it is not new. Alrosa's plan to mine 25 to 26 million carats in 2026, down 14% from 29.7 million carats in 2025, was set out by the company's head in December 2025, with the stated reason that it was not a question of capacity but of regulating demand and global inventories. That target has stood for eight months. What changed this week is that the half-year accounts now show what holding it costs, and the answer is a loss.",
"The desk's view: the two largest rough producers in the world are both shrinking on purpose, and that is the supply story of 2026. De Beers is pausing Venetia and Alrosa is idling open pits, neither because the ore ran out and both because the midstream will not absorb the carats at a price that covers the digging. For a retailer the practical read is on natural rough-fed goods in the 2027 buying calendar, not on today's case: production decisions taken this quarter reach the counter in eighteen months. The figures here come from a single English-language report of Alrosa's half-year filing and no second outlet has yet carried them, which is why they are printed with the source named rather than as settled fact."
],
[
 {"title":"World's Largest Diamond Producer Posts $134 Million Loss in First Half of 2026 — Sada Elbalad (August 2026)","url":"https://see.news/worlds-largest-diamond-producer-posts-134-million-loss-in-first-half-of-2026"},
 {"title":"Alrosa's production will fall 14% in 2026 to 25 mln - 26 mln carats, company must regulate market — Interfax (24 December 2025)","url":"https://interfax.com/newsroom/top-stories/115424/"},
 {"title":"Production Report for the Second Quarter of 2026 — De Beers Group (23 July 2026)","url":"https://www.debeersgroup.com/news-insights/latest-group-news/2026/production-report-for-the-second-quarter-of-2026"},
])

# ========== 3. tiffany-goes-to-blue-nile ==========
art("tiffany-goes-to-blue-nile","retail-tech",False,"Retail & Technology Desk · People",4,"The Retail Desk",
["ACTOR","NUM"],
"Signet puts 25 years of Tiffany into Blue Nile",
"Pam Cloud becomes president of Blue Nile on 10 August, reporting to chief operating and financial officer Joan Hilson. She spent more than 25 years at Tiffany, latterly as senior vice president and chief merchandising officer, and founded a direct-to-consumer pearl brand.",
[
"Signet has given its online engagement business to a merchant. Pam Cloud becomes president of Blue Nile on 10 August, the company announced on Wednesday, reporting to Joan Hilson, Signet's chief operating and financial officer. Cloud brings more than thirty years in luxury retail, of which more than twenty-five were at Tiffany and Co., where she was senior vice president and chief merchandising officer and sat on the executive committee. She later founded Roseate Jewelry, a direct-to-consumer pearl brand.",
"The shape of the hire is the signal. Blue Nile was built as a price-transparency business, the site that let a buyer sort loose stones by the four Cs and see the number before walking into a store, and Signet bought it in 2022 for $360 million. Putting a chief merchandising officer from Tiffany in charge of it is a decision about assortment and presentation rather than about traffic or conversion. A merchant's instinct is to edit the offer down; a marketplace's instinct is to widen it. Those two instincts pull in opposite directions, and the appointment says which one won.",
"The timing sits against a hard problem in the category. Lab-grown stones now sit in a large share of American engagement rings and the wholesale price of them has collapsed, which means a site whose original promise was to show you the cheapest honest price for a given specification is competing in a market where the specification no longer carries the price. This desk filed the Natural Diamond Council's answer to that on Wednesday, an inscribed provenance mark and 80% of the advertising budget aimed at consumers. Blue Nile's answer, on this evidence, is merchandising.",
"It is also the second senior jewellery seat filled in a week. Pandora named Andre Branch to run North America from 15 August, a post empty since February, and this desk covered that appointment on Wednesday as a bet on consumer marketing over category expertise. Signet has made close to the opposite bet, hiring depth in the category rather than breadth outside it. Both companies are selling into the same American fourth quarter, which is already substantially bought, and both new presidents start in the middle of August.",
"The desk's view: two of the largest jewellery groups in the West have just made opposite bets on what the job now requires, and the fourth quarter will grade them. Signet's read is that the differentiated product wins; Pandora's is that the differentiated campaign does. For an independent watching from the outside, the useful question is not which is right but which describes your own shop, because a business with a distinctive assortment and a business with a distinctive voice need different money spent on them. Neither hire changes anything before November."
],
[
 {"title":"Signet Levels Up Blue Nile's Luxury Team with Pam Cloud — JCK (5 August 2026)","url":"https://www.jckonline.com/editorial-article/signet-blue-nile-pam-cloud/"},
 {"title":"Tiffany veteran appointed president of Blue Nile — The Jewelry Wire (August 2026)","url":"https://thejewelrywire.substack.com/p/tiffany-veteran-appointed-president"},
 {"title":"Pandora Names New Head of North America — Rapaport (4 August 2026)","url":"https://rapaport.com/news/pandora-names-new-head-of-north-america/"},
])

# ========== 4. bnpl-inside-the-perimeter ==========
art("bnpl-inside-the-perimeter","retail-tech",False,"Retail & Technology Desk · Finance",5,"The Retail Desk",
["NUM","HOWTO"],
"£13 billion of buy-now-pay-later is now inside the FCA's perimeter",
"Deferred payment credit came under Financial Conduct Authority supervision on 15 July. The market ran from £60 million of transactions in 2017 to more than £13 billion in 2024, with about 11 million British users. Lenders now owe affordability checks and Ombudsman access.",
[
"Three weeks ago the interest-free instalment plan at the jewellery counter stopped being unregulated, and most of the trade has not noticed. From 15 July, deferred payment credit, the model that underpins buy-now-pay-later, came inside the United Kingdom's regulatory perimeter under the Financial Conduct Authority. This is a three-week-old rule change rather than news of the day, and it is being filed now because its operative consequences land on retailers over the next five months rather than on the day it commenced.",
"The scale explains why the regulator moved. Buy-now-pay-later transaction value in Britain went from about £60 million in 2017 to more than £13 billion in 2024, and the FCA puts the number of British consumers using these products at around 11 million. That is a consumer credit market the size of a mid-tier bank that grew for seven years with no affordability rules, no disclosure standard and no route of complaint. Jewellery sits squarely inside it, because a £900 ring split into four payments is exactly the ticket the product was designed for.",
"What the rules actually require is short to state. Lenders must carry out proportionate checks that a customer can afford to repay before the credit is offered. Consumers must be given clear upfront terms covering when payments fall due, how much they are, and what happens if one is missed. And a customer who is treated badly can now take the complaint to the Financial Ombudsman Service, which is the change with teeth, because it converts a commercial dispute into a supervised one. Firms could register for a temporary permissions regime between 15 May and 1 July, and those holding temporary permission have six months from commencement to apply for full authorisation.",
"For a jeweller the exposure is indirect but real. Most independents do not lend; they accept a provider's plug-in at checkout, and the authorisation obligation sits with the provider. But a shop that promotes a finance option in its window or its email is making a representation about credit, and the January deadline for providers to be fully authorised is the date at which some smaller providers will fail to clear the bar and withdraw. A retailer whose average ticket depends on a four-payment split should be asking its provider now, in writing, whether it holds full authorisation or temporary permission.",
"The desk's view: the useful question is not compliance but conversion, because affordability checks introduce friction into the exact moment a customer decides. A proportionate check at a £900 ring is a pause, and a pause at the till costs sales in a way no rule can price. That is the trade-off Britain has chosen and the American trade should watch it, because the same product has grown the same way in the United States with the same absence of rules. Ask your provider two questions this month: are you fully authorised, and what does your check add to checkout time."
],
[
 {"title":"New protections confirmed for Buy Now Pay Later borrowers — Financial Conduct Authority","url":"https://www.fca.org.uk/news/press-releases/new-protections-confirmed-buy-now-pay-later-borrowers"},
 {"title":"Regulating Buy Now Pay Later (BNPL) — Financial Conduct Authority","url":"https://www.fca.org.uk/firms/regulating-buy-now-pay-later"},
 {"title":"Government delivers fairer deal for shoppers as Buy-Now, Pay-Later rules come into force — GOV.UK (15 July 2026)","url":"https://www.gov.uk/government/news/government-delivers-fairer-deal-for-shoppers-as-buy-now-pay-later-rules-come-into-force"},
 {"title":"New FCA Regulation of Buy Now Pay Later: What You Need to Know — Reed Smith","url":"https://www.reedsmith.com/our-insights/blogs/viewpoints/102mmmf/new-fca-regulation-of-buy-now-pay-later-what-you-need-to-know/"},
])

# ========== 5. nine-thirty-four-for-one-seventeen ==========
art("nine-thirty-four-for-one-seventeen","retail-tech",False,"Retail & Technology Desk · Property",4,"The Retail Desk",
["NUM","ACTOR"],
"$934 million for 117 anchors: a second run at the JCPenney estate",
"Onyx Partners has bid $934 million for 117 J.C. Penney stores covering 15.7 million square feet across 35 states, about $8 million a store. A $947 million offer was rejected in December. The firm says financing is in place to close on 25 September.",
[
"The property under a large share of America's mall jewellery counters is on the block again. Onyx Partners, a Boston-area private equity firm, has offered $934 million for a portfolio of 117 J.C. Penney stores spanning 15.7 million square feet across 35 states, working out at roughly $8 million a store. It is the firm's second attempt: a slightly higher bid of $947 million was rejected in December. Onyx says financing is fully in place and that it is prepared to close on 25 September.",
"The seller is the reason this matters to the trade. The estate is held by Copper Property CTL Pass Through Trust, a vehicle created after J.C. Penney's 2020 Chapter 11 filing with a mandate to liquidate real estate for the benefit of investors. A trust with a liquidation mandate is a seller with a clock. A second bid from the same buyer at a lower price is a negotiation about how fast that clock is running rather than about what the buildings are worth.",
"J.C. Penney is not a peripheral jewellery retailer. It has run fine jewellery departments in its stores for decades, and the anchor position at a regional mall is the piece of real estate that determines the footfall past every specialist jeweller in the concourse. Ownership of 117 anchors passing to a financial buyer with a return horizon rather than a merchandising plan is the kind of change that reaches an independent tenant through the traffic count and the lease renewal, not through a press release.",
"The arithmetic is worth sitting with. At about $8 million a store for 15.7 million square feet, the implied price is roughly $59 a square foot, which is land-and-shell pricing rather than going-concern retail pricing. That is a market clearing anchor space at a level that assumes the current use may not be the final use. For any jeweller whose lease sits in one of these 117 centres, the question for the landlord is not whether the store stays a department store but what the anchor box becomes if it does not.",
"The desk's view: the mall jewellery counter's economics were never set by the jeweller, they were set by whoever owned the anchor, and that owner is changing hands at scrap-adjacent pricing. A specialist paying concourse rent on footfall generated by a neighbour bought at $59 a foot is carrying a risk that does not appear anywhere in its own accounts. The deal has not closed and a December bid at a higher number was already turned down once, so nothing is settled. Independents in those centres should read their co-tenancy clause this month, before September answers the question for them."
],
[
 {"title":"Private Equity Firm Wants to Buy 100+ JCPenney Stores — National Jeweler (5 August 2026)","url":"https://nationaljeweler.com/articles/15196-private-equity-firm-wants-to-buy-100-jcpenney-stores"},
 {"title":"Onyx Partners takes another swing at buying national J.C. Penney portfolio — CoStar","url":"https://www.costar.com/article/459575800/onyx-partners-takes-another-swing-at-buying-national-j-c-penney-portfolio"},
 {"title":"Private equity firm tries again to buy 100-plus J.C. Penney stores — Retail Dive","url":"https://www.retaildive.com/news/private-equity-firm-onyx-partners-tries-to-buy-117-jcpenney-stores/826804/"},
])

# ========== 6. sixty-seven-percent-asked-a-chatbot ==========
art("sixty-seven-percent-asked-a-chatbot","retail-tech",False,"Retail & Technology Desk · Consumer",4,"The Retail Desk",
["NUM","GAP"],
"67% asked a chatbot: the gift search has left the search box",
"Attentive's survey of 600 American adults finds 67% used an AI chatbot to help them shop in the past three months, rising to 80% of Gen Z. Separately 62% will plan holiday purchases before November and 71% will start buying before Black Friday.",
[
"Two thirds of American shoppers have started asking a machine what to buy. Attentive's holiday research, conducted online among 600 United States adults and published this week, finds that 67% used an AI chatbot such as ChatGPT, Gemini or Perplexity to help with shopping in the past three months, rising to 80% among Gen Z respondents. Among those users, the most common tasks were researching specific products, comparing brands and features, seeking recommendations and finding deals, with 51% using the tools to compare brands.",
"The second finding moves the calendar. Attentive puts 62% of consumers planning holiday purchases before November and 71% expecting to start buying before Black Friday, with 46% beginning to shop before November arrives. A jewellery business that treats the season as a five-week sprint from the last Friday in November is now planning for a window in which most of the intent has already formed and a substantial share of the money has already been committed.",
"Put the two together and the operational consequence is specific rather than atmospheric. If two thirds of buyers consult a language model and most of them form intent in October, then the sentence a model produces about your shop in October is doing the work a shop window used to do in December. This is the same mechanism the Natural Diamond Council is spending against, which this desk reported on Wednesday: the council has engaged the agency Artefact specifically to work on how natural diamonds appear inside large language models.",
"Two cautions on the number. A sample of 600 adults surveyed online is small and self-selecting toward people comfortable answering surveys on a screen, which is the same population most likely to have tried a chatbot, so 67% is probably a ceiling rather than a floor. And using a chatbot to research is not the same as buying through one; the survey measures consultation, not conversion, and no figure in it says a single ring was sold by a model. What it does establish is where the consideration happens.",
"The desk's view: the gift search has left the search box, and a jeweller's product copy is now being read by a machine before it is read by a customer. That makes plain, specific, factual descriptions worth more than atmospheric ones, because a model summarising a page rewards carat weight, metal, setting and price stated clearly and has nothing to do with an adjective. The cheapest action available this month is to write the specification into the page text rather than leaving it in an image, and to do it before October rather than after."
],
[
 {"title":"Holiday Shopping Is Starting Earlier and Using AI — JCK (5 August 2026)","url":"https://www.jckonline.com/editorial-article/holiday-shopping-ai/"},
 {"title":"Holiday Shopping Starts Earlier, Raising the Stakes for Brands, New Attentive Research Finds — Global Toy News (3 August 2026)","url":"https://globaltoynews.com/2026/08/03/holiday-shopping-starts-earlier-raising-the-stakes-for-brands-new-attentive-research-finds/"},
 {"title":"As the holidays near, two-thirds of shoppers are using AI — Retail Dive","url":"https://www.retaildive.com/news/holiday-shoppers-using-ai-gift-purchases/826939/"},
])

# ================= SPECS =================
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

specs["silver-alone-in-the-red"] = {
 **strip("By the numbers · Kitco spot, 6:03am New York",[
   {"fig":"$4,270.90","delta":"▲ +0.58%","dir":"up","lab":"gold, fourth session up"},
   {"fig":"$61.67","delta":"▼ −0.41%","dir":"down","lab":"silver, alone in the red"},
   {"fig":"$1,753.00","delta":"▲ +1.33%","dir":"up","lab":"platinum"},
   {"fig":"$1,367.00","delta":"▲ +1.48%","dir":"up","lab":"palladium"},
   {"fig":"69.3","lab":"gold to silver ratio, from 67.8"}]),
 "figs":[bars("Plate I","Session change by metal · 6 August 2026",[
   {"l":"PALLADIUM","v":1.48,"d":"+1.48%"},
   {"l":"PLATINUM","v":1.33,"d":"+1.33%"},
   {"l":"GOLD","v":0.58,"d":"+0.58%"},
   {"l":"SILVER","v":-0.41,"d":"−0.41%","hi":True}],
   "Per cent against Wednesday's close. Kitco spot, 6:03am New York, 6 August 2026.",184)],
 "flow":flow5("A seven-week high, and the leader turns.","The gram, and the platinum ratio.","Two marks, and one release.",
   "Silver has been the engine of this rally all week, and on Thursday it was the only metal in the red.","The Gold & Metals Desk",
   "Four metals, third session: gold $4,157.80","a-four-metals-third-session.html"),
 "desk":{"split":"a rally that loses its fastest metal first is a rally in its late innings"},
 "next":nxt("alrosa-books-the-loss","Diamonds","The largest rough producer by volume swung to a half-year loss.",
   "four-metals-third-session","Metals","gold-waits-on-payrolls","The Fed")}

specs["alrosa-books-the-loss"] = {
 **strip("By the numbers · Alrosa, first half 2026",[
   {"fig":"$932.5M","delta":"▼ −36%","dir":"down","lab":"revenue, half year"},
   {"fig":"−$134.1M","dir":"down","lab":"net loss, from +$490.1M"},
   {"fig":"$873.4M","delta":"▼ −20%","dir":"down","lab":"cost of sales"},
   {"fig":"25–26Mct","delta":"▼ −14%","dir":"down","lab":"2026 guidance, set Dec 2025"},
   {"fig":"~10%","lab":"Russian output at Severalmaz, suspended"}]),
 "figs":[bars("Plate I","Alrosa first half, year-on-year change",[
   {"l":"REVENUE","v":-36,"d":"−36%","hi":True},
   {"l":"COST OF SALES","v":-20,"d":"−20%"},
   {"l":"2026 OUTPUT GUIDANCE","v":-14,"d":"−14%"}],
   "Per cent year on year. Half-year accounts as reported; guidance set December 2025.",185)],
 "flow":flow5("Revenue fell twice as fast as cost.","A disposal flattered the base.","Care and maintenance, not closure.",
   "Care and maintenance is not a closure and it is not a pause in the Venetia sense.","The Diamonds Desk",
   "De Beers narrows the loss, and the price","a-de-beers-narrows-the-loss.html"),
 "desk":{"split":"the two largest rough producers in the world are both shrinking on purpose"},
 "next":nxt("silver-alone-in-the-red","Metals","Gold made a seven-week high and silver turned red beneath it.",
   "de-beers-narrows-the-loss","De Beers","the-one-carat-stops-falling","Polished")}

specs["tiffany-goes-to-blue-nile"] = {
 **strip("By the numbers · Blue Nile",[
   {"fig":"10 Aug","lab":"Cloud starts as president"},
   {"fig":"25+ yrs","lab":"at Tiffany and Co."},
   {"fig":"30+ yrs","lab":"in luxury retail"},
   {"fig":"$360M","lab":"Signet's 2022 purchase price"},
   {"fig":"15 Aug","lab":"Pandora's new president starts"}]),
 "figs":[bars("Plate I","Two senior seats filled in one week",[
   {"l":"BLUE NILE · MERCHANT HIRE","v":25,"d":"25+ yrs in jewellery","hi":True},
   {"l":"PANDORA NA · MARKETER HIRE","v":0,"d":"none in jewellery"}],
   "Years of category experience in the appointee's background. Company statements, 4–5 August 2026.",186)],
 "flow":flow5("A merchant, not a marketer.","The instinct that won.","The opposite bet, one week apart.",
   "A merchant's instinct is to edit the offer down; a marketplace's instinct is to widen it.","The Retail Desk",
   "Six months empty: Pandora hands North America to a beauty CEO","a-pandora-fills-the-seat.html"),
 "desk":{"split":"two of the largest jewellery groups in the West have just made opposite bets on what the job now requires"},
 "next":nxt("sixty-seven-percent-asked-a-chatbot","Consumer","Two thirds of American shoppers now consult a model before buying.",
   "pandora-fills-the-seat","Pandora","eighty-percent-to-the-consumer","Marketing")}

specs["bnpl-inside-the-perimeter"] = {
 **strip("By the numbers · UK deferred payment credit",[
   {"fig":"15 July","lab":"regulation day"},
   {"fig":"£13B+","lab":"transaction value, 2024"},
   {"fig":"£60M","lab":"transaction value, 2017"},
   {"fig":"~11M","lab":"British users"},
   {"fig":"6 months","lab":"to apply for full authorisation"}]),
 "figs":[bars("Plate I","UK buy-now-pay-later transaction value",[
   {"l":"2024","v":13000,"d":"£13bn+","hi":True},
   {"l":"2017","v":60,"d":"£60m"}],
   "Millions of pounds of transaction value. Financial Conduct Authority.",187)],
 "flow":flow5("Three weeks old, and not yet noticed.","Why the regulator moved.","What the rules actually require.",
   "That is a consumer credit market the size of a mid-tier bank that grew for seven years with no affordability rules, no disclosure standard and no route of complaint.","The Retail Desk",
   "A dollar battery and a fifteen dollar job","a-dollar-battery-fifteen-dollar-job.html"),
 "desk":{"split":"the useful question is not compliance but conversion"},
 "next":nxt("nine-thirty-four-for-one-seventeen","Property","117 mall anchors are changing hands at $59 a square foot.",
   "shoplifting-down-fraud-up","Loss","the-storefront-that-isnt","Retail")}

specs["nine-thirty-four-for-one-seventeen"] = {
 **strip("By the numbers · Onyx Partners bid",[
   {"fig":"$934M","lab":"offer for 117 stores"},
   {"fig":"$947M","lab":"December bid, rejected"},
   {"fig":"15.7M","lab":"square feet, 35 states"},
   {"fig":"~$8M","lab":"implied price a store"},
   {"fig":"25 Sept","lab":"target close"}]),
 "figs":[bars("Plate I","J.C. Penney portfolio bids",[
   {"l":"DECEMBER 2025 · REJECTED","v":947,"d":"$947m"},
   {"l":"AUGUST 2026 · PENDING","v":934,"d":"$934m","hi":True}],
   "Millions of dollars offered for 117 stores. Copper Property CTL Pass Through Trust process.",188)],
 "flow":flow5("A second run at the estate.","A seller with a clock.","Land pricing, not retail pricing.",
   "A trust with a liquidation mandate is a seller with a clock.","The Retail Desk",
   "The storefront that isn't","a-the-storefront-that-isnt.html"),
 "desk":{"split":"the mall jewellery counter's economics were never set by the jeweller"},
 "next":nxt("tiffany-goes-to-blue-nile","People","Signet hands Blue Nile to a Tiffany merchandising veteran.",
   "michael-hill-adds-two","Stores","the-storefront-that-isnt","Retail")}

specs["sixty-seven-percent-asked-a-chatbot"] = {
 **strip("By the numbers · Attentive, 600 US adults",[
   {"fig":"67%","lab":"used an AI chatbot to shop"},
   {"fig":"80%","lab":"of Gen Z respondents"},
   {"fig":"51%","lab":"used it to compare brands"},
   {"fig":"71%","lab":"start buying before Black Friday"},
   {"fig":"62%","lab":"plan purchases before November"}]),
 "figs":[bars("Plate I","Where the holiday season now starts",[
   {"l":"START BUYING BEFORE BLACK FRIDAY","v":71,"d":"71%","hi":True},
   {"l":"USED AN AI CHATBOT TO SHOP","v":67,"d":"67%"},
   {"l":"PLAN PURCHASES BEFORE NOVEMBER","v":62,"d":"62%"},
   {"l":"BEGIN SHOPPING BEFORE NOVEMBER","v":46,"d":"46%"}],
   "Per cent of 600 US adults surveyed online. Attentive holiday research, August 2026.",189)],
 "flow":flow5("Two thirds asked a machine.","The calendar moves to October.","Consultation is not conversion.",
   "A jewellery business that treats the season as a five-week sprint from the last Friday in November is now planning for a window in which most of the intent has already formed and a substantial share of the money has already been committed.","The Retail Desk",
   "Eighty percent to the consumer: the NDC changes the subject","a-eighty-percent-to-the-consumer.html"),
 "desk":{"split":"the gift search has left the search box"},
 "next":nxt("bnpl-inside-the-perimeter","Finance","Britain's instalment-credit market came under FCA supervision on 15 July.",
   "eighty-percent-to-the-consumer","Marketing","tiffany-goes-to-blue-nile","People")}

# ================= VALIDATION =================
existing = {a["slug"] for a in articles} | {a["slug"] for a in NEW}
fail = []
for a in NEW:
    if len(a["body"]) != 5:
        fail.append(f"{a['slug']}: body has {len(a['body'])} paragraphs, need 5")
    if not a["body"][-1].startswith("The desk's view:"):
        fail.append(f"{a['slug']}: last paragraph does not start 'The desk's view:'")
    if a["slug"] not in specs:
        fail.append(f"{a['slug']}: no spec")
for s, sp in specs.items():
    a = next((x for x in NEW if x["slug"] == s), None)
    if a is None:
        fail.append(f"spec {s}: no article"); continue
    split = sp["desk"]["split"]
    if split not in a["body"][-1]:
        fail.append(f"{s}: desk split not verbatim in last paragraph")
    pull = next((b["pull"]["q"] for b in sp["flow"] if "pull" in b), None)
    if pull and not any(pull in p for p in a["body"][0:4]):
        fail.append(f"{s}: pull quote not verbatim in paragraphs 0-3")
    also = next((b["also"]["href"] for b in sp["flow"] if "also" in b), None)
    if also:
        aslug = also[2:-5]
        if aslug not in existing: fail.append(f"{s}: also slug {aslug} does not exist")
        if aslug == s: fail.append(f"{s}: also self-reference")
    nx = sp["next"]
    for ns in [nx["lead"]["slug"]] + [m["slug"] for m in nx["minis"]]:
        if ns not in existing: fail.append(f"{s}: next slug {ns} does not exist")
        if ns == s: fail.append(f"{s}: next self-reference")
if fail:
    print("VALIDATION FAILED"); [print(" -",f) for f in fail]; sys.exit(1)

leads = [a for a in NEW if a.get("lead")]
assert len(leads) == 1, leads
for s in specs: editorial[s] = specs[s]
articles = NEW + articles
(C/"articles.json").write_text(json.dumps(articles, ensure_ascii=False, indent=1))
(C/"editorial.json").write_text(json.dumps(editorial, ensure_ascii=False, indent=1))
print("edition No.027 written:", len(NEW), "articles, lead =", leads[0]["slug"], "| total", len(articles))
