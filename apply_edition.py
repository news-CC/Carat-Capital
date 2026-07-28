#!/usr/bin/env python3
# Edition No. 018 — 2026-07-28. Prepends 8 articles + specs, refreshes wire + record.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())
wire = json.loads((C/"wire.json").read_text())
record = json.loads((C/"record.json").read_text())

DATE = "2026-07-28"

# ---- remove old lead flag ----
for a in articles:
    a.pop("lead", None) if False else None
for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD — gold-idles-into-the-fed ==========
art("gold-idles-into-the-fed","gold-metals",True,"Gold & Metals Desk · New York",4,"The Bullion Desk",
["STAKES","NUM"],
"Gold idles at $4,046 as the Fed splits the room",
"Spot sits in a $4,021–$4,080 triangle on the eve of the July 29 decision. Futures price a 62% hold at 3.50–3.75% but a 38% hike, and 81% odds of a September move.",
[
"Gold spent the eve of the Federal Reserve's decision going almost nowhere, and that stillness is the story. Spot traded near $4,046 an ounce on Tuesday, boxed inside a symmetrical triangle between roughly $4,021 in support and $4,080 in resistance, with the market unwilling to commit a dollar in either direction until Wednesday afternoon. Beneath the near-term floor sit the familiar markers at $3,964 and $3,914; above the ceiling, $4,133, $4,173 and $4,220.",
"What makes this meeting different from the last several is that the outcome is genuinely in doubt. CME FedWatch put the odds of a hold at the current 3.50–3.75% at about 62 percent, leaving a full 38 percent chance of a quarter-point hike — an unusually two-sided read for a decision day. Further out, futures assign roughly 81 percent odds to a move by September. A hold is still the base case; it is no longer the only case.",
"The data does not stop at the rate. Second-quarter GDP, personal income and spending, and core PCE — the Fed's preferred inflation gauge, seen near 3.3 percent — all land on Thursday, which means the decision and the numbers that justify or undercut it arrive within forty-eight hours of each other. Softer oil, as tension around Iran eased, has taken some heat out of the inflation argument and let Treasury yields drift lower into the print.",
"For the jewelry trade the mechanics matter more than the drama. A hold paired with cautious language keeps gold in its plateau and lets manufacturers hold the $4,000-plus planning price they have already redesigned mountings around. A surprise hike, or a hold read as hawkish, would lift yields and press bullion toward the lower rails of the triangle — testing whether the physical bid from Asia and central banks is deep enough to catch it.",
"The desk's view: a coil this tight into three top-tier prints does not resolve gently, so the counter should plan for a move, not a drift. The level to watch is not the ceiling but the floor — hold $3,964 and gold stays the value story a cautious buyer is already choosing; lose it and the summer's calm ends in a hurry.",
],
[{"title":"Gold Price Forecast Today: XAU/USD Tests $4,020 Support Ahead of Fed Decision — FX Leaders","url":"https://www.fxleaders.com/news/2026/07/28/gold-price-forecast-today-xauusd-tests-dollar4020-support-ahead-of-fed-decision-july-28/"},
 {"title":"Gold Spot Prices — Kitco","url":"https://www.kitco.com/price/precious-metals"}])

# ========== 2. silver-eyes-sixty ==========
art("silver-eyes-sixty","gold-metals",False,"Gold & Metals Desk · New York",3,"The Metals Desk",
["VS","NUM"],
"Silver eyes $60 as palladium jumps and platinum firms",
"While gold idles, the white metals move: palladium added 3.3% and platinum 1.7% on Monday to about $1,268 and $1,612, and silver near $58 keeps $60 in view — up more than 50% on the year.",
[
"Gold gets the headlines this week, but the money in motion is in the white metals. On Monday palladium jumped about 3.3 percent to roughly $1,268 an ounce and platinum added 1.7 percent to about $1,612, while silver held near $58.50 with $60 back in sight after touching $60.11 intraday earlier in the month. Silver now sits more than 50 percent above where it traded a year ago; platinum is up about 14 percent on the same basis.",
"The moves cut against the metals' own fundamentals in interesting ways. The World Platinum Investment Council still forecasts a fourth straight platinum deficit for 2026, but it also sees jewelry demand for the metal falling 12 percent on the year — so the firmness is coming from industrial use and bar-and-coin investment, not from the counter. Platinum jewelry is cheap against gold; the metal is expensive against its own showroom.",
"Silver is the one the workshop feels directly. A push toward $60 lifts the cost of every silver finding, chain and fashion piece at exactly the moment gold's price has driven shoppers toward lighter, lower-karat and silver alternatives. The gold-silver ratio has compressed toward the high 60s from above 70, the market's way of saying silver has been the stronger horse this summer.",
"None of it happens in isolation. The same Fed meeting that pins gold will set the tone for the whole complex on Wednesday, and the white metals — thinner, more volatile, more exposed to industrial sentiment — tend to move further on the news than bullion does. The tape into the decision is quiet at the top and restless underneath.",
"The desk's view: watch silver, not gold, for the first real tell after the Fed. It is the metal with the least room to hide, the most industrial leverage, and the round number — $60 — that a nervous market will treat as a verdict.",
],
[{"title":"Gold, Silver, Platinum, Palladium spot prices — Kitco","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Platinum — Price, Chart, Historical Data — Trading Economics","url":"https://tradingeconomics.com/commodity/platinum"},
 {"title":"WPIC Platinum Quarterly — fourth straight deficit for 2026","url":"https://platinuminvestment.com/supply-and-demand/platinum-quarterly"}])

# ========== 3. titan-makes-it-three ==========
art("titan-makes-it-three","retail-tech",False,"Retail-Tech Desk · Bengaluru",4,"The Retail Desk",
["ACTOR","NUM"],
"Titan makes it three: revenue up 41% on India's gold counter",
"The Tanishq owner's June quarter grew 41 percent — a third straight quarter above 40 — with jewellery up 39, watches 23 and eyewear 23. Buyers rose in the early double digits; the average ticket rose far faster.",
[
"India's largest branded jeweller keeps printing the same remarkable number. Titan Company reported roughly 41 percent revenue growth for the June quarter, its third consecutive quarter above 40 percent, powered by a jewellery division — Tanishq, Mia and CaratLane — that grew about 39 percent. Plain and studded pieces each rose in the mid-thirties, and gold coins sold strongly on investment demand as buyers treated the metal as savings as much as adornment.",
"The texture beneath the headline is the story the whole trade is living. Titan said buyer growth came in at early double digits while average ticket sizes rose in the high double digits — more customers, yes, but each spending markedly more, against a backdrop of relatively stable gold prices through April to June. It is the fewer-but-dearer pattern that has defined jewelry from New York to Hong Kong this year, stated in the numbers of a company that sells to the Indian middle class at scale.",
"The other divisions kept pace. Watches and wearables grew about 23 percent, with analogue watches up in the high twenties on premiumisation even as smart watches slipped in the low teens. Eyewear rose 23 percent, and the emerging businesses — fragrances and women's bags among them — grew 19 percent together. The international business, still small, expanded 128 percent as Tanishq pushed into North America and the Gulf.",
"Stable gold did the heavy lifting. Festive buying around Akshaya Tritiya, the spring gold-buying festival, arrived into a metal that was not lurching day to day, and Indian shoppers who postpone when prices spike showed up when they did not. That is the quiet dependency in every one of these results: the counter needs gold expensive enough to feel like value and calm enough to feel safe.",
"The desk's view: Titan is the cleanest read on the Indian consumer the trade has, and it is saying the same thing as the West in a different accent. Volume is grinding, price is soaring, and the business that wins is the one big enough to sell coins to savers and solitaires to brides in the same quarter.",
],
[{"title":"Titan Co Ltd Q1 FY27 revenue rises 41% on jewellery, watches, eyewear — Goodreturns","url":"https://www.goodreturns.in/news/titan-co-ltd-q1-fy27-revenue-up-41-percent-jewellery-watches-eyewear-011-1520381.html"},
 {"title":"Titan Q1 FY27 Revenue Rises 41 Pc on Strong Jewellery Demand — Indian Retailer","url":"https://www.indianretailer.com/news/titan-q1-fy27-revenue-rises-41-pc-strong-jewellery-demand"}])

# ========== 4. the-watch-trade-sues ==========
art("the-watch-trade-sues","watches",False,"Watches Desk · Los Angeles",4,"The Watches Desk",
["ACTOR","STAKES","VS"],
"A watch retailer takes the tariffs to court",
"California's Collective Horology sued the US over the Section 301 duties that have made Swiss watches at least 12.5 percent dearer since April 2025, arguing Washington skipped the country-by-country analysis the law requires.",
[
"The watch trade has taken its tariff fight from the invoice to the courtroom. Collective Horology, a California independent that sells and makes watches, filed suit at the US Court of International Trade challenging the Section 301 duties layered onto imports this year, joined by the spice importer Burlap & Barrel and backed by the Liberty Justice Center. It is the first time a watch retailer has tried to overturn the tariff regime rather than simply pay it.",
"The legal argument is procedural, and pointed. The complaint says the US Trade Representative applied a near-uniform tariff across dozens of countries without the country-by-country investigation the Trade Act of 1974 requires. USTR applied a uniform tariff to nearly every country, co-founder Asher Rapkin said, arguing the government skipped the work the statute demands. The relief sought is a block on enforcement and the preservation of importers' right to claw duties back if the measures are struck down.",
"The dollars behind the principle are real. Collective says Swiss watch imports have run at least 12.5 percent more expensive since April 2025, and that it is owed more than $164,000 in refunds from the earlier IEEPA tariffs the Supreme Court has already vacated — money still not returned — on top of what it has paid under Section 122 and now Section 301. For a small importer, that is not an accounting footnote; it is working capital.",
"The case lands into a trade already doing the tariff arithmetic daily. New duties of 10 and 12.5 percent took effect on jewelry, stones and metals from some sixty countries on July 24, stacking onto country measures that reach 50 percent on Canada. Swiss watches, sourced from a single high-cost country, have nowhere to reroute — which is precisely why a Swiss-heavy retailer is the one testing the policy in court.",
"The desk's view: the outcome matters far beyond one California showroom. If the court agrees the process was defective, the refund door reopens for every importer who kept its receipts — and the tariff wall that has quietly repriced the American watch counter starts to look less permanent than the trade has been forced to assume.",
],
[{"title":"Collective Horology Takes Trump Tariff Fight To Court Over Soaring Watch Costs — WatchPro","url":"https://www.watchpro.com/collective-horology-takes-trump-tariff-fight-to-court-over-soaring-watch-costs/"},
 {"title":"New US tariffs on jewelry, diamonds and gemstones — National Jeweler","url":"https://nationaljeweler.com/articles/industry"}])

# ========== 5. three-fancies-no-reserve ==========
art("three-fancies-no-reserve","auctions",False,"Auctions Desk · Los Angeles",4,"The Auctions Desk",
["GAP","NUM"],
"Three fancy-color diamonds go up with no reserve",
"Bonhams' 300-lot California sale on Tuesday sets modest estimates on serious color — a pink-purple oval, a deep pink and a heart-shaped blue, each topping near $35,000–$50,000 — and lets a 70-carat necklace sell with no floor at all.",
[
"Bonhams brings more than three hundred jewels to the block in California on Tuesday, and the most telling lots are the smallest. Three unmounted fancy-color diamonds anchor the sale: a 1.01-carat oval fancy pink-purple estimated to about $50,000, a 1.64-carat fancy deep pink to roughly $35,000, and a 0.53-carat heart-shaped fancy blue also near $35,000. In a category where top color can command seven figures, these are deliberately accessible numbers.",
"Above them sits the sale's marquee curiosity: a 70-carat diamond necklace of pear, oval and marquise stones carrying an upper estimate of just $50,000 — and offered with no reserve, meaning it will sell to the highest bid however low. A 1920s necklace built around a 7.10-carat center stone is estimated near $35,000, and a multicolored sapphire-and-diamond necklace, 34.95 carats of sapphires to 4.20 of diamonds, at about $28,000. Van Cleef & Arpels, Graff and Boucheron appear throughout.",
"The strategy is legible in the estimates. No-reserve lots and conservative valuations are how a house generates competition and clears estate material in a cautious market: set the bar low, let the room find the price. It is the opposite of the trophy-lot playbook that carried the spring's headline sales, and a useful barometer of where mid-market demand actually sits when the eight-figure stones are not in the room.",
"It also reads against the week's other diamond story. Natural stones are competing on rarity and provenance as lab-grown collapses the price of size; fancy color — genuinely scarce, impossible to grow to order at scale — is where that argument is strongest. A room bidding up small pinks and blues is a room still paying for what cannot be manufactured.",
"The desk's view: watch the no-reserve necklace as the sale's honest number. Estimates are a house's opinion; a lot with no floor prints whatever the market truly thinks a 70-carat necklace is worth on a Tuesday in July — and that figure will say more about the mid-market than any record would.",
],
[{"title":"70ct. Diamond Necklace to Hit Auction Block at Bonhams — Rapaport","url":"https://rapaport.com/news/70ct-diamond-necklace-to-hit-auction-block-at-bonhams/"},
 {"title":"Van Cleef & Arpels, Cartier, and Boucheron Highlight Bonhams' Fine Jewelry Sale — JCK","url":"https://www.jckonline.com/editorial-article/bonhams-california-fine-jewels/"}])

# ========== 6. doha-opens-a-diamond-door ==========
art("doha-opens-a-diamond-door","diamonds",False,"Diamonds Desk · Doha",4,"The Diamonds Desk",
["ACTOR","GAP"],
"Doha opens a diamond exchange, and eyes Dubai's lane",
"The Qatar Free Zones Authority launched the Qatar Diamond Exchange this week — a Kimberley-compliant hub at Ras Bufontas with sorting, vaulting and tenders under one roof, and the Gulf's newest bid to sit alongside Dubai.",
[
"Qatar has opened its first diamond exchange, and its ambition is not subtle. The Qatar Free Zones Authority launched the Qatar Diamond Exchange this week at the Ras Bufontas free zone near Doha, describing it as a regulated hub that gathers the full diamond and precious-stones value chain within a single regulated ecosystem, in the words of chief executive Sheikh Mohammed Bin Hamad Bin Faisal Al-Thani. Its natural rival sits an hour's flight away in Dubai.",
"The plumbing is built for the trade's real needs. Members — traders, manufacturers, cutters, polishers and service firms — get trading licences, on-site sorting and independent valuation, secure vaulting, specialist insurance, and the right to take part in rough and polished tenders. Free-zone terms in Qatar typically allow full foreign ownership and favorable tax treatment, the incentives every aspiring hub uses to pull goods and dealers off established routes.",
"Qatar has been laying the groundwork quietly. It joined the Kimberley Process as a full member in 2021 and, in 2025, designated the free-zone authority as the country's sole authorized entry and exit point for rough diamonds — the regulatory spine an exchange needs before it can credibly host tenders. The launch turns that framework into a marketplace.",
"Whether it draws real liquidity is the harder question. Dubai posted a record $41.7 billion in diamond trade in 2025 and has spent two decades building the relationships that route stones through it; Antwerp and Mumbai are older still. A new exchange can offer better terms, but volume follows trust, and trust in this trade is measured in decades, not incentives.",
"The desk's view: the Gulf is not short of diamond capacity, so Doha's real target is not Antwerp or Surat but the dealer deciding where to clear the next parcel. Qatar has built the room and written the rules; now it has to give the trade a reason to walk in rather than fly on to Dubai.",
],
[{"title":"Qatar Launches First Diamond Exchange — Rapaport","url":"https://rapaport.com/news/qatar-launches-first-diamond-exchange/"},
 {"title":"Qatar launches exchange to expand its role in global diamond trade — Euronews","url":"https://www.euronews.com/business/2026/07/28/qatar-launches-exchange-to-expand-its-role-in-global-diamond-trade"}])

# ========== 7. the-guide-marks-ruby-up ==========
art("the-guide-marks-ruby-up","gemstones",False,"Gemstones Desk · Glenview",3,"The Color Desk",
["GAP","ACTOR"],
"The trade's price book bends to ruby",
"GemGuide pushed Mozambique ruby prices sharply higher and scrapped its ten-point scale for Burma stones, pricing only four grades — an admission that fine ruby is now too scarce to chart the usual way.",
[
"When the reference book changes shape, the market has already moved. GemGuide, the pricing service the American colored-stone trade leans on, has revised its ruby charts: Mozambique prices raised sharply on strong demand for unenhanced, untreated material, and the Burma section rebuilt from the ground up. Research director Stuart Robertson said Mozambique prices have, in effect, skyrocketed as tender buyers chase clean goods.",
"The Burma change is the more striking admission. GemGuide abandoned its traditional one-to-ten quality scale for unenhanced Burmese ruby and now publishes just four grades — Middle Commercial, Lower Good, Upper Fine and Upper Extra Fine — leaving users to interpolate the rest. The reason is scarcity: fine Mogok material has become so hard to source that availability now matters more than price. You cannot chart a stone that does not come to market.",
"Mozambique has carried the category for over a decade, and its tenders — Gemfields' chief among them — now set the global reference for gem and near-gem ruby. That is where the price pressure is coming from: a single dominant source, buyers competing for untreated goods, and a treatment-disclosure culture that has taught the trade to pay a real premium for stones that have not seen the furnace.",
"The revisions go live in the service's app immediately and reach print in the July–August issue. For appraisers and retailers that means the number under a ruby changed this week whether or not the stone did — the kind of quiet repricing that ripples through insurance values and estate valuations long after the tender room empties.",
"The desk's view: ruby is quietly running the colored-stone story diamonds used to own — a scarce natural material getting scarcer, priced by origin and honesty rather than size. When the guide stops grading a stone the old way, it is telling you the supply, not the demand, is the thing that broke.",
],
[{"title":"GemGuide Updates Ruby Prices — National Jeweler","url":"https://nationaljeweler.com/articles/15051-gemguide-updates-ruby-prices"}])

# ========== 8. india-fills-the-hall ==========
art("india-fills-the-hall","diamonds",False,"Diamonds Desk · Mumbai",3,"The Diamonds Desk",
["GAP","HOWTO"],
"India's big August show fills up early",
"GJEPC's IIJS Premiere returns to Mumbai on August 6–10 with pre-registration past 25,000, landing just as June gems-and-jewellery exports jumped 26.5 percent — a confident sourcing season into an uncertain tariff year.",
[
"The Indian trade is voting with its badges. GJEPC's IIJS Premiere, the country's flagship gem-and-jewellery show, returns to Mumbai on August 6–10, and pre-registration has already crossed 25,000 with the first deadline extended to absorb demand. For a domestic industry that spent the spring absorbing tariff shocks, an early sell-out of visitor slots is its own kind of forecast.",
"The confidence has a number behind it. India's gross gems-and-jewellery exports rose 26.5 percent in June to about $2.21 billion, led by gold jewellery up 54.5 percent and cut-and-polished diamonds up 8.7 percent. The quarter as a whole was flat, and rough imports fell by roughly a third, so the June jump is a restart rather than a boom — but a restart is what the show floor is built to convert into orders.",
"The backdrop is anything but settled. A new 10 percent US duty on Indian goods took effect on July 24, landing on the single largest market for Surat's polished output, and the European exemption for stones finished in Antwerp gives buyers a reason to route work away from India. A strong domestic show is partly a hedge: if the American door narrows, the Indian counter and Gulf buyers have to carry more of the weight.",
"That is why GJEPC has spent the summer courting retailers well beyond Mumbai, from Lucknow to Abu Dhabi, ahead of the doors opening. The show is no longer only an export shop window; it is where India's own fast-growing jewellery retail — the demand behind Titan's 39 percent quarter — meets its supply base under one roof.",
"The desk's view: watch the order books, not the footfall. Registrations measure hope; the tickets written between August 6 and 10, against a live US tariff and a soft rough market, will show whether India's recovery is broad enough to survive the loss of a little American duty-free room.",
],
[{"title":"IIJS Bharat Premiere 2026 Crosses 25,000 Registrations — Indian Jeweller","url":"https://www.indianjeweller.in/Indian-Jewellery-News/16302/iijs-bharat-premiere-2026-crosses-25000-registrations-phase-1-deadline-extended"},
 {"title":"India June gems & jewellery exports +26.5% — GJEPC / IANS","url":"https://gjepc.org/"}])

# ---------------- EDITORIAL SPECS ----------------
def strip(cap, cells): return {"strip":{"cap":cap,"cells":cells}}
def spec(cap, rows): return {"spec":{"cap":cap,"rows":rows}}
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

specs["gold-idles-into-the-fed"] = {
 **strip("By the numbers · gold on Fed eve",[
   {"fig":"$4,046","lab":"spot, Tuesday"},
   {"fig":"$4,021","lab":"triangle support"},
   {"fig":"$4,080","lab":"triangle resistance"},
   {"fig":"62%","lab":"odds of a hold"},
   {"fig":"38%","lab":"odds of a hike"}]),
 "figs":[bars("Plate I","The rails that box gold in",[
   {"l":"RESISTANCE","v":4133,"d":"$4,133"},
   {"l":"CEILING","v":4080,"d":"$4,080","hi":True},
   {"l":"SPOT","v":4046,"d":"$4,046"},
   {"l":"SUPPORT","v":4021,"d":"$4,021"},
   {"l":"FLOOR","v":3964,"d":"$3,964"}],
   "USD/oz. Technical markers into the July 28–29 FOMC.",133)],
 "flow":flow5("Wound tight, going nowhere.","A genuinely two-sided meeting.","The floor is the story.",
   "A hold is still the base case; it is no longer the only case.","The Bullion Desk",
   "China takes 173 tonnes","a-china-takes-173-tonnes.html"),
 "desk":{"split":"The level to watch is not the ceiling but the floor — hold $3,964 and gold stays the value story a cautious buyer is already choosing; lose it and the summer's calm ends in a hurry."},
 "next":nxt("silver-eyes-sixty","White metals","Palladium jumps, platinum firms, silver eyes $60.",
   "china-takes-173-tonnes","Demand","gold-coils-for-the-fed","Setup")}

specs["silver-eyes-sixty"] = {
 **strip("By the numbers · the white metals",[
   {"fig":"~$58.5","lab":"silver / oz"},
   {"fig":"$60","delta":"in view","dir":"up","lab":"silver's next line"},
   {"fig":"+3.3%","dir":"up","lab":"palladium, Monday"},
   {"fig":"$1,612","lab":"platinum / oz"},
   {"fig":"+51%","dir":"up","lab":"silver, year on year"}]),
 "figs":[bars("Plate I","A year in the white metals",[
   {"l":"SILVER","v":51,"d":"+51%","hi":True},
   {"l":"PLATINUM","v":14,"d":"+14%"}],
   "Approximate change, year on year.",134)],
 "flow":flow5("Gold idles; the whites move.","Firm metal, soft showroom.","The Fed sets the whole board.",
   "Gold gets the headlines this week, but the money in motion is in the white metals.","The Metals Desk",
   "Platinum, short a fourth year","a-platinum-short-a-fourth-year.html"),
 "desk":{"split":"It is the metal with the least room to hide, the most industrial leverage, and the round number — $60 — that a nervous market will treat as a verdict."},
 "next":nxt("gold-idles-into-the-fed","The decision","Gold coils under $4,050 as the Fed splits the room.",
   "platinum-short-a-fourth-year","Deficit","silver-narrows-the-ratio","Ratio")}

specs["titan-makes-it-three"] = {
 **strip("By the numbers · Titan Q1 FY27",[
   {"fig":"+41%","dir":"up","lab":"group revenue"},
   {"fig":"+39%","dir":"up","lab":"jewellery"},
   {"fig":"+23%","dir":"up","lab":"watches"},
   {"fig":"+23%","dir":"up","lab":"eyewear"},
   {"fig":"3rd","lab":"quarter above 40%"}]),
 "figs":[bars("Plate I","Where Titan grew",[
   {"l":"INTERNATIONAL","v":128,"d":"+128%"},
   {"l":"JEWELLERY","v":39,"d":"+39%","hi":True},
   {"l":"WATCHES","v":23,"d":"+23%"},
   {"l":"EYEWEAR","v":23,"d":"+23%"},
   {"l":"EMERGING","v":19,"d":"+19%"}],
   "Segment revenue growth, year on year, June quarter.",135)],
 "flow":flow5("A third 40-percent quarter.","Fewer buyers, dearer tickets.","The gold it all rests on.",
   "It is the fewer-but-dearer pattern that has defined jewelry from New York to Hong Kong this year, stated in the numbers of a company that sells to the Indian middle class at scale.","The Retail Desk",
   "India buys the dip","a-india-buys-the-dip.html"),
 "desk":{"split":"Volume is grinding, price is soaring, and the business that wins is the one big enough to sell coins to savers and solitaires to brides in the same quarter."},
 "next":nxt("average-ticket-carries-the-half","The pattern","Fewer buyers, dearer tickets — the year in one line.",
   "india-buys-the-dip","India","china-weighs-in-on-gold","Asia")}

specs["the-watch-trade-sues"] = {
 **spec("The case, in brief",[
   {"l":"Plaintiffs","v":"Collective Horology, with Burlap & Barrel"},
   {"l":"Backer","v":"Liberty Justice Center"},
   {"l":"Court","v":"US Court of International Trade"},
   {"l":"Target","v":"Section 301 duties, <b>1974 Trade Act</b>"},
   {"l":"Swiss impact","v":"imports <b>&ge;12.5%</b> dearer since Apr 2025"},
   {"l":"Refunds owed","v":"<b>$164,000+</b> in vacated IEEPA duties"}]),
 "figs":[bars("Plate I","US import-duty bands in force",[
   {"l":"CANADA (goods)","v":50,"d":"50%"},
   {"l":"CHINA / UAE band","v":12.5,"d":"12.5%","hi":True},
   {"l":"INDIA / UK band","v":10,"d":"10%"}],
   "Selected 2026 duty bands the complaint sits against.",136)],
 "flow":flow5("From the invoice to the court.","A procedural argument.","Nowhere to reroute.",
   "It is the first time a watch retailer has tried to overturn the tariff regime rather than simply pay it.","The Watches Desk",
   "The tariff wall returns","a-tariff-wall-returns.html"),
 "desk":{"split":"the tariff wall that has quietly repriced the American watch counter starts to look less permanent than the trade has been forced to assume."},
 "next":nxt("tariff-wall-returns","The duties","The Section 301 bands that reset the counter.",
   "list-up-resale-down","Prices","the-big-three-pull-away","Value")}

specs["three-fancies-no-reserve"] = {
 **strip("By the numbers · the California sale",[
   {"fig":"300+","lab":"lots, Tuesday"},
   {"fig":"1.01ct","lab":"fancy pink-purple"},
   {"fig":"$50k","lab":"top color estimate"},
   {"fig":"70ct","lab":"necklace, no reserve"},
   {"fig":"$28k","lab":"sapphire necklace est."}]),
 "figs":[bars("Plate I","The lots, by high estimate",[
   {"l":"PINK-PURPLE 1.01ct","v":50,"d":"$50k","hi":True},
   {"l":"DEEP PINK 1.64ct","v":35,"d":"$35k"},
   {"l":"HEART BLUE 0.53ct","v":35,"d":"$35k"},
   {"l":"1920s NECKLACE","v":35,"d":"$35k"},
   {"l":"SAPPHIRE NECKLACE","v":28,"d":"$28k"}],
   "Upper estimates, USD thousands. Bonhams California, July 28.",137)],
 "flow":flow5("The smallest lots say the most.","A necklace with no floor.","Paying for the unmanufacturable.",
   "No-reserve lots and conservative valuations are how a house generates competition and clears estate material in a cautious market: set the bar low, let the room find the price.","The Auctions Desk",
   "Seventy carats, no reserve","a-seventy-carats-no-reserve.html"),
 "desk":{"split":"a lot with no floor prints whatever the market truly thinks a 70-carat necklace is worth on a Tuesday in July — and that figure will say more about the mid-market than any record would."},
 "next":nxt("seventy-carats-no-reserve","The preview","The 70-carat necklace, before the hammer.",
   "sothebys-thirty-one-million","June","piaget-doubles-at-bonhams","Bonhams")}

specs["doha-opens-a-diamond-door"] = {
 **spec("The exchange, in brief",[
   {"l":"Operator","v":"Qatar Free Zones Authority (QFZ)"},
   {"l":"Home","v":"Ras Bufontas free zone, Doha"},
   {"l":"Compliance","v":"Kimberley Process, member since <b>2021</b>"},
   {"l":"For members","v":"licences, sorting, valuation, vaulting, tenders"},
   {"l":"The rival","v":"Dubai — <b>$41.7B</b> traded in 2025"}]),
 "figs":[bars("Plate I","A giant and a newborn",[
   {"l":"DUBAI (2025)","v":41.7,"d":"$41.7B","hi":True},
   {"l":"DOHA (day one)","v":0.2,"d":"opens"}],
   "Annual diamond trade. Doha starts from zero.",138)],
 "flow":flow5("A hub with ambition.","The plumbing is real.","Liquidity follows trust.",
   "A new exchange can offer better terms, but volume follows trust, and trust in this trade is measured in decades, not incentives.","The Diamonds Desk",
   "Antwerp thins, India loads","a-antwerp-thins-india-loads.html"),
 "desk":{"split":"Qatar has built the room and written the rules; now it has to give the trade a reason to walk in rather than fly on to Dubai."},
 "next":nxt("antwerp-thins-india-loads","The routes","Where the tariff map sends the stones now.",
   "india-ships-the-turn","India","de-beers-sale-gets-a-clock","Supply")}

specs["the-guide-marks-ruby-up"] = {
 **spec("What changed in the book",[
   {"l":"Source","v":"GemGuide, the trade's pricing service"},
   {"l":"Mozambique","v":"prices raised <b>sharply</b> on untreated demand"},
   {"l":"Burma","v":"10-point scale cut to <b>4 grades</b>"},
   {"l":"The grades","v":"Middle Commercial · Lower Good · Upper Fine · Upper Extra Fine"},
   {"l":"Live","v":"app now; print in the <b>Jul–Aug</b> issue"}]),
 "figs":[bars("Plate I","Burma ruby, regraded",[
   {"l":"UPPER EXTRA FINE","v":10,"d":"Grade 10","hi":True},
   {"l":"UPPER FINE","v":8,"d":"Grade 8"},
   {"l":"LOWER GOOD","v":5,"d":"Grade 5"},
   {"l":"MIDDLE COMMERCIAL","v":3,"d":"Grade 3"}],
   "The only four grades GemGuide now prices for unenhanced Burma ruby.",139)],
 "flow":flow5("The book changes shape.","Too scarce to grade.","Origin over size.",
   "When the reference book changes shape, the market has already moved.","The Color Desk",
   "Emeralds hold at $146","a-emeralds-hold-at-146.html"),
 "desk":{"split":"When the guide stops grading a stone the old way, it is telling you the supply, not the demand, is the thing that broke."},
 "next":nxt("emeralds-hold-at-146","Color","Gemfields' emeralds hold their price.",
   "sixty-six-dollars-a-carat","Ruby","twelve-point-five-for-color","Tariff")}

specs["india-fills-the-hall"] = {
 **strip("By the numbers · IIJS Premiere",[
   {"fig":"Aug 6–10","lab":"Mumbai show"},
   {"fig":"25,000+","lab":"pre-registered"},
   {"fig":"+26.5%","dir":"up","lab":"June exports, y/y"},
   {"fig":"+54.5%","dir":"up","lab":"gold jewellery exports"},
   {"fig":"10%","lab":"new US duty, Jul 24"}]),
 "figs":[bars("Plate I","India's June export tape",[
   {"l":"GOLD JEWELLERY","v":54.5,"d":"+54.5%","hi":True},
   {"l":"TOTAL EXPORTS","v":26.5,"d":"+26.5%"},
   {"l":"CUT & POLISHED","v":8.7,"d":"+8.7%"}],
   "Year-on-year change, June 2026. GJEPC.",140)],
 "flow":flow5("Voting with their badges.","A restart, not a boom.","A hedge against the duty.",
   "For a domestic industry that spent the spring absorbing tariff shocks, an early sell-out of visitor slots is its own kind of forecast.","The Diamonds Desk",
   "Surat eats the ten","a-surat-eats-the-ten.html"),
 "desk":{"split":"the tickets written between August 6 and 10, against a live US tariff and a soft rough market, will show whether India's recovery is broad enough to survive the loss of a little American duty-free room."},
 "next":nxt("surat-eats-the-ten","The duty","India's cutters absorb a 10% US tariff.",
   "doha-opens-a-diamond-door","Gulf","thirties-outrun-the-ones","Prices")}

# ---------------- VALIDATE specs ----------------
allslugs = set(a["slug"] for a in articles) | set(a["slug"] for a in NEW)
errs=[]
for d in NEW:
    s=d["slug"]; sp=specs[s]; body=d["body"]; n=len(body)
    # paragraph coverage: 0..n-2 once
    ps=[f["p"] for f in sp["flow"] if "p" in f]
    if sorted(ps)!=list(range(n-1)): errs.append(f"{s}: flow paras {sorted(ps)} != {list(range(n-1))}")
    # pull verbatim in some para 0..n-2
    pq=[f["pull"]["q"] for f in sp["flow"] if "pull" in f][0]
    if not any(pq in body[i] for i in range(n-1)): errs.append(f"{s}: pull not verbatim")
    # desk split verbatim in last para
    if sp["desk"]["split"] not in body[-1]: errs.append(f"{s}: desk split not in last para")
    if not body[-1].startswith("The desk's view:"): errs.append(f"{s}: last para not desk's view")
    # also + next slugs exist
    _href=[f["also"]["href"] for f in sp["flow"] if "also" in f][0]
    also=_href[2:-5] if _href.startswith("a-") and _href.endswith(".html") else _href
    if also not in allslugs: errs.append(f"{s}: also slug {also} missing")
    for m in [sp["next"]["lead"]["slug"]]+[x["slug"] for x in sp["next"]["minis"]]:
        if m not in allslugs: errs.append(f"{s}: next slug {m} missing")
        if m==s: errs.append(f"{s}: next points to self")
    # exactly one lead flag overall handled below
if errs:
    print("SPEC ERRORS:"); [print(" -",e) for e in errs]; sys.exit(1)

# ---------------- PREPEND + write ----------------
articles = NEW + articles
leads=[a["slug"] for a in articles if a.get("lead")]
assert leads==["gold-idles-into-the-fed"], f"lead set wrong: {leads}"
for s in specs: editorial[s]=specs[s]

(C/"articles.json").write_text(json.dumps(articles,ensure_ascii=False,indent=1))
(C/"editorial.json").write_text(json.dumps(editorial,ensure_ascii=False,indent=1))
print("articles now:",len(articles)," specs now:",len(editorial)," lead:",leads)
print("OK")
