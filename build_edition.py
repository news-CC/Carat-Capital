#!/usr/bin/env python3
import json, datetime, sys

DATE = "2026-07-27"

# ---------------- ARTICLES ----------------
articles_new = [
{
 "slug":"israel-exchange-loses-its-chief","desk":"diamonds","date":DATE,"lead":True,
 "kicker":"Diamonds Desk · Ramat Gan","minutes":4,"byline":"The Diamonds Desk",
 "tags":["ACTOR","STAKES","NUM"],
 "title":"Israel's diamond chief resigns as exports hit a record low",
 "dek":"Nissim Zuaretz stepped down after two years with first-half exports at $2.4 billion, the lowest on record and down from roughly $7 billion at the 2015 peak. Dubai, lab-grown and a new 10% US tariff were all named.",
 "body":[
  "Nissim Zuaretz resigned as president of the Israel Diamond Exchange on July 26 after two years in the role, and the figure he left behind explained the exit more plainly than any statement could. Israeli diamond exports came to $2.4 billion in the first half of 2026, the lowest half on record and a fraction of the roughly $7 billion the country shipped at its 2015 peak. A trade that once ran through Ramat Gan is running somewhere else.",
  "Zuaretz named the pressures without softening them: dealers and their goods relocating to Dubai for its tax treatment, lab-grown stones hollowing out the middle of the natural market, weakening global demand, and a new 10% United States tariff on diamond imports that took effect over the weekend. Without a change of course, he warned, \"we will be able to say goodbye to the Israel Diamond Exchange.\"",
  "The exchange is not a small room. Its four-tower complex in Ramat Gan has for decades been one of the world's principal trading floors, a place where memo goods and sight boxes changed hands under one roof. The migration Zuaretz described is the quiet kind: not a closure but a slow draining of the firms, the workers and the inventory that gave the floor its liquidity, each one following a lower cost of doing business to the Gulf.",
  "The tariff is the sharpest of the new cuts. The 10% American duty, part of the Section 301 bands that hit roughly sixty countries on July 24, lands on a trade already competing with a Dubai that charges little to nothing, and it compounds rather than replaces the structural drift. An election to replace Zuaretz, already expected in November, now carries the weight of deciding whether the exchange fights the drift or manages the decline.",
  "The desk's view: a bourse is only as strong as the reasons to trade inside it, and Ramat Gan is watching those reasons move to the Gulf one lease at a time. A record-low half is not a headline the next president inherits so much as a mandate, and the mandate is blunt: give the floor a reason to stay that is larger than a tax bill, or preside over the goodbye Zuaretz already named."
 ],
 "sources":[
  {"title":"Israel's diamond exports plunge to historic low as exchange chief resigns — Ynetnews","url":"https://www.ynetnews.com/business/article/h100005gxrfg"},
  {"title":"Israel Diamond Exchange President Resigns — Rapaport","url":"https://rapaport.com/news/israel-diamond-exchange-president-resigns/"}
 ]
},
{
 "slug":"say-synthetic-not-lab-grown","desk":"diamonds","date":DATE,"minutes":4,
 "kicker":"Diamonds Desk · Milan","byline":"The Diamonds Desk",
 "tags":["VS","STAKES","ACTOR"],
 "title":"Not lab-grown, synthetic: CIBJO moves to redraw the label",
 "dek":"The confederation expects to strike \"laboratory-grown\" and \"laboratory-created\" from its Blue Book at a September 4 congress and mandate \"synthetic\" instead, joining Russia, India, the African producers and the GIA in a coordinated tightening of language.",
 "body":[
  "The word on the tag is about to change. CIBJO, the world jewelry confederation, expects to remove \"laboratory-grown\" and \"laboratory-created\" from its Blue Book and require the single term \"synthetic\" for man-made gemstones, with a formal decision due at its congress on September 4. The body concluded the older phrasing described the product poorly, and that a plainer word serves the shopper better.",
  "Charles Abouchar, who heads CIBJO's colored-stone commission, framed the aim as \"protecting consumer confidence through the adoption of clear and descriptive language.\" The confederation's own definition does the heavy lifting: a synthetic is an artificial product with essentially the same chemical composition, physical properties and structure as its natural counterpart. That is precisely the claim lab-grown marketers have leaned on, now recast in a word the trade has historically used to mean cheaper.",
  "CIBJO is not moving alone. Russia ordered lab-grown jewelry labeled \"synthetic\" from September 1, the African Diamond Producers Association made the same call in May, India's Bureau of Indian Standards issued standardized terminology, and the GIA updated its own terms in 2025. Read together, the moves are a natural-diamond counteroffensive fought on the dictionary rather than the price list, aimed at stripping the borrowed romance out of a category whose wholesale prices have fallen about 96% since 2018.",
  "For retailers the change is not cosmetic. A sales associate who has spent three years teaching customers to say \"lab-grown\" now has to unlearn it, and a word that markets a product as modern and guilt-free becomes a word that markets it as manufactured. The stakes are largest for the brands that built their pitch on the friendlier phrase, and smallest for the naturals houses that lobbied for the harder one.",
  "The desk's view: language is the cheapest lever in this trade and the slowest to move, which is exactly why the naturals side is pulling it now. Call a stone synthetic often enough and the market stops arguing about whether it is a diamond, and that argument, not the carat price, is the one that has always been worth winning."
 ],
 "sources":[
  {"title":"CIBJO Expects to Nix 'Lab-Grown' Terminology — Rapaport","url":"https://rapaport.com/news/cibjo-expects-to-nix-lab-grown-terminology/"},
  {"title":"CIBJO Mulls Whether to Call Lab-Grown Diamonds \"Synthetic\" — JCK","url":"https://www.jckonline.com/editorial-article/cibjo-lab-growns-synthetic"}
 ]
},
{
 "slug":"thirties-outrun-the-ones","desk":"diamonds","date":DATE,"minutes":3,
 "kicker":"Diamonds Desk · Mumbai","byline":"The Diamonds Desk",
 "tags":["NUM","GAP"],
 "title":"Thirty-pointers run while the one-carat stalls",
 "dek":"The RapNet index for 0.30-carat diamonds rose 4.2% in June, up from 2.1% in May, and 0.50-carat goods added 1.3%, while the one-carat slipped 0.7%. The recovery is real, and it is happening at the bottom of the carat scale.",
 "body":[
  "The diamond recovery has a size, and the size is small. The RapNet Diamond Index for 0.30-carat stones rose 4.2% in June, accelerating from a 2.1% gain in May, and half-carat goods added 1.3%, while the one-carat index slipped 0.7% on the month. Three-carat stones edged back to positive at 0.4%. The turn is genuine, but it is running from the bottom of the scale upward, not the top down.",
  "The engine is scarcity, not exuberance. Sustained inventory reductions have let dealers correct small-stone prices upward, helped by steady United States retail demand through June and healthy Hong Kong counters at Chow Tai Fook and Luk Fook. Indian wholesalers expect activity to firm further into the August IIJS Premiere show in Mumbai and the October wedding season, the two dates that usually decide whether a soft summer becomes a real fourth quarter.",
  "Supply has been thinning at the source as well. De Beers cut official rough prices sharply, particularly for goods under 0.75 carats, to meet the market it actually faces, and global rough production fell 8% to 98.8 million carats in 2025, with Russia leading by value for a third straight year. Indian manufacturers, still cautious, have kept polishing lines deliberately short rather than betting on a broad rebound.",
  "The divergence is the story worth watching. Large stones, two carats and up in the better colors and clarities, remain the strongest sellers on the American counter, yet the price recovery is starting in the smalls, where tight inventory bites first. A market that heals from both ends at once is rare, and this one is choosing the cheaper end to start.",
  "The desk's view: when the thirty-pointer moves before the one-carat, it is telling you the recovery is being made in the back office, not the boutique. Watch the half-carat into IIJS, because if the smalls hold their gains through a restocked August, the middle of the book is next, and the middle is where the money is."
 ],
 "sources":[
  {"title":"Small-Diamond Recovery Accelerates in June — Rapaport","url":"https://rapaport.com/news/small-diamond-recovery-accelerates-in-june/"},
  {"title":"Rapaport Press Release: Small-Diamond Recovery Accelerates in June — BusinessWire","url":"https://www.businesswire.com/news/home/20260712762140/en/Rapaport-Press-Release-Small-Diamond-Recovery-Accelerates-in-June"}
 ]
},
{
 "slug":"gold-coils-for-the-fed","desk":"gold-metals","date":DATE,"minutes":4,
 "kicker":"Gold & Metals Desk · New York","byline":"The Metals Desk",
 "tags":["NUM","STAKES"],
 "title":"Gold coils under $4,100 into a three-headline Fed week",
 "dek":"Spot holds the low $4,000s with support at $4,022 and $3,964 and resistance at $4,100, as the Federal Reserve decides July 28–29 alongside second-quarter GDP and core PCE. A hold at 3.50–3.75% is widely expected; the messaging is the trade.",
 "body":[
  "Gold enters the most consequential week of its summer wound tight. Spot held the low $4,000s to start Monday, capped by resistance near $4,100 and floored by support at $4,022 and, below it, the triple-bottom zone around $3,964. Chart readers call the shape a symmetrical triangle, the kind that resolves into a decisive move rather than a drift, and this week hands it three reasons to break.",
  "The calendar is dense. The Federal Reserve announces its decision on July 28–29, with a hold at 3.50–3.75% widely expected but markets still pricing a small chance of a hike. Second-quarter GDP lands the same week, with the Atlanta Fed's tracker near 1.7% growth, and core PCE, the Fed's preferred inflation gauge, is seen around 3.3% against a headline near 3.7%. Any one of the three can move the metal; the combination can set its direction into August.",
  "The risk is in the tone, not the number. A hold read as \"higher for longer\" would lift Treasury yields and press gold back under $4,100, while balanced language paired with softer yields would let bullion test the resistance and, beyond it, the $4,132 and $4,173 markers. The white metals sit in the same current: silver held near $58 with $60 in view, and platinum steadied around $1,585 after a soft week.",
  "Physical demand is doing the quiet work beneath the chart. Central-bank appetite remains firm, and Asian buying has stayed heavy even as Western funds hesitate, a split that has kept the floor higher than the technicals alone would justify. That is the tension into Wednesday: a nervous financial bid above ground, a patient physical bid beneath it, and a Fed that gets to decide which one sets the price.",
  "The desk's view: the triangle will not hold through three top-tier prints, so position for the break rather than the level. For the jewelry counter the number that matters is not the peak but the floor, and as long as $3,964 holds, gold stays the value story a nervous shopper is already buying."
 ],
 "sources":[
  {"title":"Gold Price Forecast: Fed, FOMC and the Week Ahead — FX Leaders","url":"https://www.fxleaders.com/news/2026/07/27/gold-price-forecast-fed-fomc-xau-usd-week-ahead-july-2026/"},
  {"title":"Gold Forecast: XAU/USD Defends $4,000 ahead of Fed, GDP and PCE — FX Leaders","url":"https://www.fxleaders.com/news/2026/07/26/gold-forecast-xau-usd-defends-4000-as-china-imports-soar-ahead-of-fed-gdp-and-pce-inflation/"}
 ]
},
{
 "slug":"china-takes-173-tonnes","desk":"gold-metals","date":DATE,"minutes":3,
 "kicker":"Gold & Metals Desk · Shanghai","byline":"The Metals Desk",
 "tags":["NUM","VS"],
 "title":"China pulls in 173 tonnes of gold in a single June",
 "dek":"China imported about 173 tonnes of gold in June, its strongest monthly inflow since March 2024, lifting the first half toward 820 tonnes. Softer prices reopened the counter in the East just as Western funds turned cautious.",
 "body":[
  "China bought the dip in size. The country imported roughly 173 tonnes of gold in June, its heaviest monthly inflow since March 2024, carrying first-half imports toward 820 tonnes. The number matters because of its timing: it landed as gold pulled back from above $4,100 toward $4,000, the exact move that chills Western investors and warms Chinese buyers.",
  "The pattern is now familiar but no less telling. When the price sags, the East restocks. Chow Tai Fook reported weight-based gold jewelry up 63.7% in Hong Kong and Macau and 38% on the mainland last quarter as softer prices revived demand, and the import figure is the wholesale echo of that retail pull, metal moving toward the counters that sell it by the gram rather than the story.",
  "It is a split market. Western fund flows have wavered into the Federal Reserve's July 28–29 meeting, wary that a hawkish hold lifts yields and dulls a metal that pays no interest. Chinese demand runs on the opposite logic: a lower dollar price is a buying signal, not a warning, and central-bank and household appetite has kept building through the very weakness that unsettles the paper market.",
  "The consequence shows up as a floor. Heavy physical offtake in the East is a large part of why gold has held the low $4,000s rather than retracing further, cushioning the pullbacks that the charts keep threatening. The question into Wednesday is whether Fed messaging can pull Western money back to the same side of the trade the East has never left.",
  "The desk's view: 173 tonnes in a month is not a headline, it is a foundation, and it is being poured while the West debates whether to buy at all. For the jewelry trade the read is simple: the world's largest gold-buying public treats every dip as a discount, and that habit is worth more to the price than any single Fed sentence."
 ],
 "sources":[
  {"title":"Gold Forecast: XAU/USD Defends $4,000 as China Imports Soar — FX Leaders","url":"https://www.fxleaders.com/news/2026/07/26/gold-forecast-xau-usd-defends-4000-as-china-imports-soar-ahead-of-fed-gdp-and-pce-inflation/"},
  {"title":"New Collection Boosts Chow Tai Fook's Revenue — Rapaport","url":"https://rapaport.com/news/new-collection-boosts-chow-tai-fooks-revenue/"}
 ]
},
{
 "slug":"the-big-three-pull-away","desk":"watches","date":DATE,"minutes":4,
 "kicker":"Watches Desk · Zurich","byline":"The Watches Desk",
 "tags":["ACTOR","NUM","VS"],
 "title":"Patek, Rolex and AP pull away on the resale board",
 "dek":"Morgan Stanley's second-quarter read puts value retention at 15.4% above retail for Patek Philippe, 9.8% for Rolex and 3.0% for Audemars Piguet, while every other tracked brand sits below list, Cartier at −27.4% and Omega at −32.3%.",
 "body":[
  "The secondary market recovered in the second quarter, and it recovered unevenly. Morgan Stanley's latest read, built on WatchCharts data snapshotted June 29, puts value retention, the gap between retail and resale, at 15.4% above list for Patek Philippe, 9.8% for Rolex and 3.0% for Audemars Piguet. Every other brand the bank tracks trades below retail, with Cartier at −27.4%, Omega at −32.3% and IWC at −37.9%.",
  "The gap is widening, not closing. Patek's retention improved by more than ten points year on year and Rolex's by seven, so the recovery that lifted the market as a whole lifted the top three fastest. The bank's own verdict was cool on everyone else: gains for the listed players remain modest, and the numbers still suggest limited pricing power outside the big three in the coming quarters.",
  "Underneath the brand averages, the models tell a sharper story. Patek's Aquanaut trades about 90% above retail and the Nautilus 74% above, while the dressier Calatrava sits 34% below. Rolex's Oyster Perpetual runs 35% over list and the Sea-Dweller 21% under. The premium is not to a maker so much as to a specific steel sports reference the waiting list never satisfied.",
  "For retailers and collectors the signal is a barbell. The pieces that hold or gain are a narrow band of hyped sports models from three houses; almost everything else, including some very good watchmaking, is a depreciating asset the moment it leaves the boutique. A recovery that concentrates this hard is really a flight to the same handful of names buyers already trusted.",
  "The desk's view: value retention is a popularity contest with a price attached, and the big three keep winning it by making less than the market wants. For anyone buying to hold, the lesson is unromantic: the badge and the reference matter more than the movement, and the resale board has been saying so for three straight quarters."
 ],
 "sources":[
  {"title":"Rolex, Patek and AP Tighten Secondary Market Grip — WatchPro","url":"https://www.watchpro.com/rolex-patek-and-ap-tighten-secondary-market-grip/"},
  {"title":"Morgan Stanley × WatchCharts Q2 2026 secondary-market report — WatchCharts","url":"https://watchcharts.com/about/press"}
 ]
},
{
 "slug":"seventy-carats-no-reserve","desk":"auctions","date":DATE,"minutes":3,
 "kicker":"Auctions Desk · Los Angeles","byline":"The Auctions Desk",
 "tags":["NUM","GAP"],
 "title":"Seventy carats, no reserve, on the block at Bonhams",
 "dek":"A 70-carat diamond necklace of pear, oval and marquise stones carries a top estimate near $50,000 and no reserve when Bonhams sells more than 300 California jewels on July 28, alongside pieces by Van Cleef & Arpels, Graff and Boucheron.",
 "body":[
  "The arithmetic is the hook. When Bonhams sells its California Jewels auction in Los Angeles on July 28, the marquee lot is a 70-carat diamond necklace of pear, oval and marquise stones estimated at up to $50,000, and offered without reserve. Seventy carats of graded diamond for the price of a single fine solitaire is not a market on the diamonds; it is a market on the setting, the certification and the story.",
  "That is the estate logic of a no-reserve sale. Older mounted pieces, whose individual stones are hard to certify and expensive to break out, trade at a steep discount to the loose-goods price sheet, and a seller who wants a clean, guaranteed sale accepts it. The estimate is a floor to walk in the door, not a valuation of the carats, and the room, not the book, sets the price.",
  "The catalogue runs deeper than one lot. Bonhams lists more than 300 jewels including a 1920s necklace built around a 7.10-carat diamond at a $35,000 high estimate, a necklace set with 34.95 carats of multicolored sapphires and 4.20 carats of diamonds at $28,000, and three unmounted diamonds estimated between $35,000 and $50,000, with signed pieces from Van Cleef & Arpels, Graff and Boucheron threaded through the sale.",
  "The venue is the point as much as the goods. A California day sale is where the accessible middle of the jewelry market clears, the estate and secondary material that never reaches a Geneva evening, and it is a fair gauge of what ordinary collectors will pay in a summer when the metal underneath every lot has rarely been dearer.",
  "The desk's view: a 70-carat necklace with no reserve is a dare disguised as a lot, and someone will take it. Watch the hammer against the low estimates rather than the highs, because in a no-reserve room the honest signal is not what the trophy makes but what the ordinary lots hold."
 ],
 "sources":[
  {"title":"70ct. Diamond Necklace to Hit Auction Block at Bonhams — Rapaport","url":"https://rapaport.com/news/70ct-diamond-necklace-to-hit-auction-block-at-bonhams/"},
  {"title":"Van Cleef & Arpels, Cartier, and Boucheron Highlight Bonhams' Fine Jewelry Sale — JCK","url":"https://www.jckonline.com/editorial-article/bonhams-california-fine-jewels/"}
 ]
},
{
 "slug":"gia-lights-up-fluorescence","desk":"retail-tech","date":DATE,"minutes":3,
 "kicker":"Retail-Tech Desk · Carlsbad","byline":"The Retail Desk",
 "tags":["GAP","HOWTO"],
 "title":"The GIA turns a light on fluorescence",
 "dek":"From the fourth quarter the laboratory will add language to its reports separating fluorescence that changes a diamond's look from fluorescence that does not, addressing a stigma that has discounted a quarter to a third of all stones since the 1990s.",
 "body":[
  "One of the most persistent discounts in diamonds is about to get a footnote. From the fourth quarter of 2026, the GIA will add clarifying language to its grading reports to distinguish when fluorescence changes a diamond's appearance from when it does not. The trade has called it one of the biggest steps a laboratory has taken to address a trait that between 25% and 35% of diamonds carry to some degree.",
  "Fluorescence, the soft glow some diamonds give under ultraviolet light, has been priced as a defect for decades even though it rarely is one. In most stones it does nothing visible; in a small share it can lend a milky or oily cast to high-color goods, and the market long ago collapsed those two very different cases into a single penalty. Rapaport has published fluorescence discount estimates since 1993, tracking a haircut that persisted through every swing of the market.",
  "The fix is information, not chemistry. By stating on the report whether the fluorescence actually affects the look of the specific stone, the GIA lets a buyer separate the harmless from the compromised, and lets a seller defend a price rather than accept a reflex discount. For a sizable, long-misunderstood slice of the market, transparency about the trait could carry real weight with the trade and the shopper alike.",
  "The commercial stakes sit with the middle of the counter. Faint and medium fluorescence in the near-colorless grades is exactly the material a value-minded consumer buys, and a clearer report gives the honest retailer a tool to reclaim margin that the blanket stigma has been quietly bleeding away.",
  "The desk's view: this is a rare case of a grading change that helps the buyer and the seller at once, by pricing a stone for what it looks like instead of what it might do. Read the new line when it lands, because a diamond that glows and shows nothing for it may be the best-value stone in the case."
 ],
 "sources":[
  {"title":"Rapaport Intelligence Report: Shining a Light on Fluorescent Diamonds — Rapaport","url":"https://rapaport.com/news/rapaport-intelligence-report-shining-a-light-on-fluorescent-diamonds/"},
  {"title":"GIA grading report updates — Gemological Institute of America","url":"https://www.gia.edu/gia-news-research"}
 ]
}
]

# ---------------- EDITORIAL SPECS ----------------
def flow_std(pull_q, pull_attr, subs, also_t, also_href, split0=None):
    f=[{"sub":subs[0],"n":"§1"},{"p":0}]
    if split0: f.append({"p":1,"split":split0})
    else: f.append({"p":1})
    f += [{"sub":subs[1],"n":"§2"},{"p":2},
          {"pull":{"q":pull_q,"attr":pull_attr}},
          {"sub":subs[2],"n":"§3"},{"p":3},
          {"also":{"t":also_t,"href":also_href}}]
    return f

specs = {
 "israel-exchange-loses-its-chief":{
  "spec":{"cap":"On the record · Ramat Gan","rows":[
    {"l":"Who resigned","v":"<b>Nissim Zuaretz</b>, president, after two years"},
    {"l":"H1 2026 exports","v":"<b>$2.4 billion</b> — lowest on record"},
    {"l":"2015 peak","v":"roughly <b>$7 billion</b>"},
    {"l":"New US tariff","v":"<b>10%</b> on diamond imports, from July 24"},
    {"l":"Successor vote","v":"expected <b>November 2026</b>"}]},
  "figs":[{"no":"Plate I","title":"Israeli diamond exports · the long slide","rows":[
    {"l":"2015 PEAK","v":7.0,"d":"~$7.0B"},
    {"l":"H1 2026","v":2.4,"d":"$2.4B","hi":True}],
    "note":"Polished diamond export value. Half-year 2026 vs. 2015 full-year peak.",
    "cap":"The floor that took a president with it. Carat Capital graphics desk. &nbsp;CC/2026/125"}],
  "flow":flow_std(
    "A trade that once ran through Ramat Gan is running somewhere else.","The Diamonds Desk",
    ["A record-low half.","Where the trade went.","The cut that compounds."],
    "Surat eats the ten as India loads the polished","a-surat-eats-the-ten.html"),
  "desk":{"split":"give the floor a reason to stay that is larger than a tax bill, or preside over the goodbye Zuaretz already named."},
  "next":{"lead":{"slug":"de-beers-sale-gets-a-clock","tag":"Diamonds","blurb":"Anglo's sale of De Beers gets a year-end clock."},
    "minis":[{"slug":"antwerp-thins-india-loads","tag":"Diamonds"},{"slug":"surat-eats-the-ten","tag":"Diamonds"}]}
 },
 "say-synthetic-not-lab-grown":{
  "spec":{"cap":"On the record · the terminology turn","rows":[
    {"l":"Body","v":"<b>CIBJO</b> (world jewelry confederation)"},
    {"l":"The change","v":"strike \"laboratory-grown\" / \"laboratory-created\""},
    {"l":"New rule","v":"one term: <b>synthetic</b>"},
    {"l":"Formal decision","v":"congress, <b>September 4</b>"},
    {"l":"Also moved","v":"Russia, India BIS, ADPA, GIA (2025)"}]},
  "figs":[{"no":"Plate I","title":"Who has hardened the language","rows":[
    {"l":"RUSSIA (from Sept 1)","v":3,"d":"'synthetic', grams only"},
    {"l":"ADPA (May)","v":2,"d":"same call"},
    {"l":"INDIA (BIS)","v":2,"d":"standard terms"},
    {"l":"GIA (2025)","v":2,"d":"updated terms"},
    {"l":"CIBJO (Sept)","v":3,"d":"Blue Book","hi":True}],
    "note":"Bars mark relative reach of each rule, not a measured quantity.",
    "cap":"The dictionary as a price list. Carat Capital graphics desk. &nbsp;CC/2026/126"}],
  "flow":flow_std(
    "That is precisely the claim lab-grown marketers have leaned on, now recast in a word the trade has historically used to mean cheaper.","The Diamonds Desk",
    ["One word, by decree.","A coordinated push.","What it costs the counter."],
    "Sixty-one percent said lab, and meant it","a-sixty-one-percent-said-lab.html"),
  "desk":{"split":"and that argument, not the carat price, is the one that has always been worth winning."},
  "next":{"lead":{"slug":"sixty-one-percent-said-lab","tag":"Diamonds","blurb":"Most 2025 couples chose a lab-grown center stone."},
    "minis":[{"slug":"lab-grown-finds-its-floor","tag":"Diamonds"},{"slug":"surat-eats-the-ten","tag":"Diamonds"}]}
 },
 "thirties-outrun-the-ones":{
  "strip":{"cap":"By the numbers · RapNet index, June","cells":[
    {"fig":"+4.2%","delta":"▲","dir":"up","lab":"0.30ct"},
    {"fig":"+1.3%","delta":"▲","dir":"up","lab":"0.50ct"},
    {"fig":"−0.7%","delta":"▼","dir":"dn","lab":"1.00ct"},
    {"fig":"+0.4%","delta":"▲","dir":"up","lab":"3.00ct"},
    {"fig":"98.8M","lab":"ct rough, 2025 (−8%)"}]},
  "figs":[{"no":"Plate I","title":"June price move by size · smalls lead","rows":[
    {"l":"0.30ct","v":4.2,"d":"+4.2%","hi":True},
    {"l":"0.50ct","v":1.3,"d":"+1.3%"},
    {"l":"3.00ct","v":0.4,"d":"+0.4%"},
    {"l":"1.00ct","v":0.7,"d":"−0.7%"}],
    "note":"RapNet Diamond Index, month-on-month, June 2026. Bars show size, not sign.",
    "cap":"The recovery starts small. Carat Capital graphics desk. &nbsp;CC/2026/127"}],
  "flow":flow_std(
    "The turn is genuine, but it is running from the bottom of the scale upward, not the top down.","The Diamonds Desk",
    ["Small stones, real gains.","Scarcity, not exuberance.","The divergence to watch."],
    "Small stones lead the turn, again","a-small-stones-lead-again.html"),
  "desk":{"split":"because if the smalls hold their gains through a restocked August, the middle of the book is next, and the middle is where the money is."},
  "next":{"lead":{"slug":"small-stones-lead-again","tag":"Diamonds","blurb":"The sub-carat book leads the diamond turn."},
    "minis":[{"slug":"antwerp-thins-india-loads","tag":"Diamonds"},{"slug":"de-beers-sale-gets-a-clock","tag":"Diamonds"}]}
 },
 "gold-coils-for-the-fed":{
  "strip":{"cap":"By the numbers · gold into Fed week","cells":[
    {"fig":"$4,100","lab":"resistance"},
    {"fig":"$4,022","lab":"first support"},
    {"fig":"$3,964","lab":"triple-bottom floor"},
    {"fig":"3.50–3.75%","lab":"Fed rate (hold seen)"},
    {"fig":"~3.3%","lab":"core PCE, expected"}]},
  "figs":[{"no":"Plate I","title":"The levels that box gold in","rows":[
    {"l":"RESISTANCE 2","v":4173,"d":"$4,173"},
    {"l":"RESISTANCE 1","v":4132,"d":"$4,132"},
    {"l":"THE LINE","v":4100,"d":"$4,100","hi":True},
    {"l":"SUPPORT 1","v":4022,"d":"$4,022"},
    {"l":"FLOOR","v":3964,"d":"$3,964"}],
    "note":"USD/oz. Technical markers into the July 28–29 FOMC.",
    "cap":"A triangle waiting on the Fed. Carat Capital graphics desk. &nbsp;CC/2026/128"}],
  "flow":flow_std(
    "Chart readers call the shape a symmetrical triangle, the kind that resolves into a decisive move rather than a drift, and this week hands it three reasons to break.","The Metals Desk",
    ["Wound tight under $4,100.","Three prints, one week.","A patient physical bid."],
    "Gold waits on the Fed","a-gold-waits-on-the-fed.html"),
  "desk":{"split":"as long as $3,964 holds, gold stays the value story a nervous shopper is already buying."},
  "next":{"lead":{"slug":"gold-waits-on-the-fed","tag":"Gold & Metals","blurb":"Gold holds a high plateau into the July meeting."},
    "minis":[{"slug":"silver-narrows-the-ratio","tag":"Gold & Metals"},{"slug":"gold-defends-four-thousand-again","tag":"Gold & Metals"}]}
 },
 "china-takes-173-tonnes":{
  "strip":{"cap":"By the numbers · China's June gold","cells":[
    {"fig":"173t","delta":"▲","dir":"up","lab":"June imports"},
    {"fig":"~820t","lab":"H1 imports"},
    {"fig":"Mar '24","lab":"last month this heavy"},
    {"fig":"+63.7%","delta":"▲","dir":"up","lab":"CTF gold by weight, HK/Macau"},
    {"fig":"+38%","delta":"▲","dir":"up","lab":"CTF gold by weight, mainland"}]},
  "figs":[{"no":"Plate I","title":"East vs. West · who is buying the dip","rows":[
    {"l":"CHINA IMPORTS, JUNE","v":173,"d":"173 tonnes","hi":True},
    {"l":"CHINA IMPORTS, H1 (avg/mo)","v":137,"d":"~137 t/mo"}],
    "note":"Bullion imports, tonnes. H1 monthly average implied from ~820t half.",
    "cap":"The floor the East is pouring. Carat Capital graphics desk. &nbsp;CC/2026/129"}],
  "flow":flow_std(
    "When the price sags, the East restocks.","The Metals Desk",
    ["A 173-tonne month.","A split market.","The floor it builds."],
    "China weighs in on gold","a-china-weighs-in-on-gold.html"),
  "desk":{"split":"the world's largest gold-buying public treats every dip as a discount, and that habit is worth more to the price than any single Fed sentence."},
  "next":{"lead":{"slug":"silver-narrows-the-ratio","tag":"Gold & Metals","blurb":"Silver's gain tightens the gold-silver ratio."},
    "minis":[{"slug":"gold-waits-on-the-fed","tag":"Gold & Metals"},{"slug":"oil-talks-gold-listens","tag":"Gold & Metals"}]}
 },
 "the-big-three-pull-away":{
  "strip":{"cap":"By the numbers · value retention, Q2","cells":[
    {"fig":"+15.4%","delta":"▲","dir":"up","lab":"Patek Philippe"},
    {"fig":"+9.8%","delta":"▲","dir":"up","lab":"Rolex"},
    {"fig":"+3.0%","delta":"▲","dir":"up","lab":"Audemars Piguet"},
    {"fig":"−27.4%","delta":"▼","dir":"dn","lab":"Cartier"},
    {"fig":"−32.3%","delta":"▼","dir":"dn","lab":"Omega"}]},
  "figs":[{"no":"Plate I","title":"Above retail, below retail · the resale board","rows":[
    {"l":"PATEK PHILIPPE","v":15.4,"d":"+15.4%","hi":True},
    {"l":"ROLEX","v":9.8,"d":"+9.8%"},
    {"l":"AUDEMARS PIGUET","v":3.0,"d":"+3.0%"},
    {"l":"CARTIER","v":27.4,"d":"−27.4%"},
    {"l":"OMEGA","v":32.3,"d":"−32.3%"}],
    "note":"Value retention vs. retail, Q2 2026 (Morgan Stanley × WatchCharts). Bars show size, not sign.",
    "cap":"Three names hold the line. Carat Capital graphics desk. &nbsp;CC/2026/130"}],
  "flow":flow_std(
    "The premium is not to a maker so much as to a specific steel sports reference the waiting list never satisfied.","The Watches Desk",
    ["Three names, everyone else.","The gap is widening.","A barbell for buyers."],
    "List up, resale down","a-list-up-resale-down.html"),
  "desk":{"split":"the badge and the reference matter more than the movement, and the resale board has been saying so for three straight quarters."},
  "next":{"lead":{"slug":"list-up-resale-down","tag":"Watches","blurb":"US list prices rise as the secondary market slips."},
    "minis":[{"slug":"swatch-nine-up-six-down","tag":"Watches"},{"slug":"rolex-on-the-main-corridor","tag":"Watches"}]}
 },
 "seventy-carats-no-reserve":{
  "spec":{"cap":"On the block · Bonhams California, July 28","rows":[
    {"l":"Marquee lot","v":"<b>70ct</b> diamond necklace, pear/oval/marquise"},
    {"l":"Estimate","v":"up to <b>$50,000</b>, no reserve"},
    {"l":"1920s necklace","v":"<b>7.10ct</b> diamond, to $35,000"},
    {"l":"Sapphire necklace","v":"<b>34.95ct</b> color + 4.20ct diamond, $28,000"},
    {"l":"Catalogue","v":"<b>300+</b> lots; Van Cleef, Graff, Boucheron"}]},
  "figs":[{"no":"Plate I","title":"Top California estimates · high end","rows":[
    {"l":"70ct DIAMOND NECKLACE","v":50,"d":"$50k","hi":True},
    {"l":"UNMOUNTED DIAMONDS (to)","v":50,"d":"$50k"},
    {"l":"1920s 7.10ct NECKLACE","v":35,"d":"$35k"},
    {"l":"SAPPHIRE + DIAMOND NECKLACE","v":28,"d":"$28k"}],
    "note":"High estimates, USD thousands. Bonhams California Jewels, July 28.",
    "cap":"The room, not the book, sets the price. Carat Capital graphics desk. &nbsp;CC/2026/131"}],
  "flow":flow_std(
    "Seventy carats of graded diamond for the price of a single fine solitaire is not a market on the diamonds; it is a market on the setting, the certification and the story.","The Auctions Desk",
    ["The dare in the catalogue.","Estate logic.","What the day sale measures."],
    "Piaget doubles at Bonhams","a-piaget-doubles-at-bonhams.html"),
  "desk":{"split":"in a no-reserve room the honest signal is not what the trophy makes but what the ordinary lots hold."},
  "next":{"lead":{"slug":"sothebys-thirty-one-million","tag":"Auctions","blurb":"A New York high-jewelry sale makes $31.4 million."},
    "minis":[{"slug":"piaget-doubles-at-bonhams","tag":"Auctions"},{"slug":"ninety-percent-sold","tag":"Auctions"}]}
 },
 "gia-lights-up-fluorescence":{
  "spec":{"cap":"On the record · the report change","rows":[
    {"l":"Laboratory","v":"<b>GIA</b>"},
    {"l":"The change","v":"language separating fluorescence that shows from fluorescence that doesn't"},
    {"l":"Effective","v":"<b>Q4 2026</b>"},
    {"l":"Stones affected","v":"<b>25–35%</b> fluoresce to some degree"},
    {"l":"Discount tracked since","v":"<b>1993</b> (Rapaport)"}]},
  "figs":[{"no":"Plate I","title":"How common is fluorescence","rows":[
    {"l":"SHOW SOME FLUORESCENCE","v":30,"d":"25–35%","hi":True},
    {"l":"NONE","v":70,"d":"~65–75%"}],
    "note":"Share of diamonds exhibiting fluorescence, per GIA. Midpoint shown.",
    "cap":"A quarter of the case, finally explained. Carat Capital graphics desk. &nbsp;CC/2026/132"}],
  "flow":flow_std(
    "The market long ago collapsed those two very different cases into a single penalty.","The Retail Desk",
    ["A footnote on a discount.","Priced as a defect.","Information, not chemistry."],
    "Seventy-three percent cheaper, and reclaiming the ring","a-seventy-three-percent-cheaper.html"),
  "desk":{"split":"a diamond that glows and shows nothing for it may be the best-value stone in the case."},
  "next":{"lead":{"slug":"seventy-three-percent-cheaper","tag":"Retail-Tech","blurb":"Lab-grown's discount reshapes the engagement counter."},
    "minis":[{"slug":"china-weighs-in-on-gold","tag":"Retail-Tech"},{"slug":"average-ticket-carries-the-half","tag":"Retail-Tech"}]}
 }
}

# ---------------- WIRE ----------------
wire = {
 "date_line":"Monday, July 27, 2026",
 "edition":"Vol. I — No. 017",
 "items":[
  {"b":"ISRAEL'S DIAMOND CHIEF RESIGNS","t":" — Nissim Zuaretz stepped down as Israel Diamond Exchange president as first-half exports fell to $2.4 billion, the lowest on record and down from roughly $7 billion in 2015; he blamed Dubai, lab-grown and a new 10% US tariff, with an election expected in November"},
  {"b":"CIBJO MOVES TO SAY 'SYNTHETIC'","t":" — The world jewelry confederation expects to strike 'laboratory-grown' and 'laboratory-created' from its Blue Book and mandate 'synthetic' at its September 4 congress, joining Russia, India's BIS, the African producers and the GIA"},
  {"b":"SMALL STONES ACCELERATE","t":" — The RapNet 0.30ct index rose 4.2% in June, up from 2.1% in May, and 0.50ct added 1.3% while the one-carat slipped 0.7%; inventory cuts and steady US demand drive the recovery ahead of IIJS and wedding season"},
  {"b":"GOLD COILS FOR THE FED","t":" — Spot held the low $4,000s below $4,100 resistance into a heavy week: the FOMC decides July 28–29 with a hold at 3.50–3.75% expected, alongside second-quarter GDP and core PCE seen near 3.3%"},
  {"b":"CHINA TAKES 173 TONNES","t":" — China imported about 173 tonnes of gold in June, its strongest month since March 2024, lifting first-half imports toward 820 tonnes as softer prices revived Eastern demand"},
  {"b":"THE BIG THREE PULL AWAY","t":" — Morgan Stanley's Q2 read put value retention at 15.4% above retail for Patek Philippe, 9.8% for Rolex and 3.0% for Audemars Piguet; every other tracked brand sat below list, Cartier at −27.4%, Omega −32.3%"},
  {"b":"SEVENTY CARATS, NO RESERVE","t":" — Bonhams sells more than 300 California jewels on July 28, led by a 70-carat diamond necklace estimated to $50,000 without reserve, with pieces by Van Cleef & Arpels, Graff and Boucheron"},
  {"b":"GIA LIGHTS UP FLUORESCENCE","t":" — From the fourth quarter the GIA will add language separating fluorescence that changes a diamond's look from fluorescence that does not; 25–35% of diamonds fluoresce, a trait discounted since the 1990s"},
  {"b":"SILVER PRESSES $60","t":" — Silver held near $58 with $60 in view while platinum steadied around $1,585 after a soft week; oil and Fed nerves keep the risk tape live into Wednesday's decision"}
 ],
 "tape_ts":"27 Jul 2026, into the London open · Fed decides Wed. (July 28–29)",
 "tape":[
  {"name":"Gold / oz","code":"XAU","px":"4,060.00","chg":"— little changed","dir":"flat","pts":[13,14,14,15,15,16,15,16,16,17]},
  {"name":"Natural 1ct (RAPI proxy)","code":"NAT1","px":"5,232.00","chg":"— unch.","dir":"flat","pts":[13,13,13,13,13,13,13,13,13,13]},
  {"name":"Lab-grown 1ct wholesale","code":"LGD1","px":"727.00","chg":"— unch.","dir":"flat","pts":[13,13,13,13,13,13,13,13,13,13]},
  {"name":"Platinum / oz","code":"XPT","px":"1,585.00","chg":"▲ +0.70%","dir":"up","pts":[13,13,14,14,15,15,16,16,16,17]},
  {"name":"Silver / oz","code":"XAG","px":"58.20","chg":"▲ +0.30%","dir":"up","pts":[16,16,16,17,17,17,17,18,18,18]}
 ]
}

# ---------------- RECORD ----------------
record_new_week = {
 "label":"This week — July 27",
 "entries":[
  {"d":"diamonds","h":"Israel Diamond Exchange president resigns as exports hit a record low",
   "t":"Nissim Zuaretz stepped down after two years as first-half 2026 diamond exports fell to $2.4 billion, the lowest on record and a fraction of the roughly $7 billion shipped at the 2015 peak. He cited dealers and goods relocating to Dubai, lab-grown competition, weak demand and a new 10% US tariff effective July 24, warning that without change the exchange could disappear. A successor election is expected in November.",
   "s":"Ynetnews / Rapaport"},
  {"d":"diamonds","h":"CIBJO expects to replace 'lab-grown' with 'synthetic'",
   "t":"The world jewelry confederation expects to strike 'laboratory-grown' and 'laboratory-created' from its Blue Book and require 'synthetic' for man-made stones, with a formal decision at its September 4 congress. Charles Abouchar of the colored-stone commission framed the goal as protecting consumer confidence through clearer language. The move follows Russia (from September 1), the African producers (May), India's BIS and the GIA's 2025 update.",
   "s":"Rapaport / JCK"},
  {"d":"diamonds","h":"Small-diamond recovery accelerates — 0.30ct index up 4.2% in June",
   "t":"The RapNet Diamond Index for 0.30-carat stones rose 4.2% in June, up from 2.1% in May, and half-carat goods added 1.3%, while the one-carat slipped 0.7% and three-carat edged up 0.4%. Inventory reductions, steady US retail demand and firm Hong Kong counters drove the correction; De Beers cut rough under 0.75 carats, and 2025 global rough production fell 8% to 98.8 million carats.",
   "s":"Rapaport"},
  {"d":"watches","h":"Morgan Stanley: only Patek, Rolex and AP hold value above retail",
   "t":"The bank's Q2 read (WatchCharts, June 29) put value retention at 15.4% above retail for Patek Philippe, 9.8% for Rolex and 3.0% for Audemars Piguet, with every other tracked brand below list — Cartier −27.4%, Omega −32.3%, IWC −37.9%. Patek's Aquanaut trades ~90% over retail and the Nautilus 74%; Rolex's Oyster Perpetual 35% over. Gains remain modest outside the big three.",
   "s":"Morgan Stanley × WatchCharts / WatchPro"},
  {"d":"gold-metals","h":"China imports about 173 tonnes of gold in June",
   "t":"China's June bullion imports reached roughly 173 tonnes, the strongest monthly inflow since March 2024, lifting first-half imports toward 820 tonnes as softer prices revived demand. The buying helped gold defend the low $4,000s into the Federal Reserve's July 28–29 meeting, which sits alongside second-quarter GDP and core PCE inflation seen near 3.3%.",
   "s":"FX Leaders"}
 ]
}

# ================= APPLY =================
A=json.load(open('content/articles.json'))
for x in A:
    if x.get('lead'): x.pop('lead',None)
newslugs={a['slug'] for a in articles_new}
existing={a['slug'] for a in A}
assert not (newslugs & existing), f"DUP SLUG: {newslugs & existing}"
A = articles_new + A

E=json.load(open('content/editorial.json'))
E.update(specs)

W=wire
R=json.load(open('content/record.json'))
# rename current top week if it is the July 20 label
if R['weeks'] and R['weeks'][0]['label'].startswith('This week'):
    R['weeks'][0]['label']='Week of July 20'
R['weeks'].insert(0, record_new_week)
R['updated']="27 Jul 2026"

# ---- validation ----
allslugs={a['slug'] for a in A}
for a in articles_new:
    sp=specs[a['slug']]
    n=len(a['body'])
    # last para desk split
    assert sp['desk']['split'] in a['body'][-1], f"desk split miss {a['slug']}"
    # flow paragraph coverage 0..n-2
    ps=[e['p'] for e in sp['flow'] if 'p' in e]
    assert sorted(ps)==list(range(n-1)), f"flow coverage {a['slug']}: {ps} vs {n-1}"
    # splits present
    for e in sp['flow']:
        if 'split' in e:
            assert e['split'] in a['body'][e['p']], f"flow split miss {a['slug']}"
    subs=[e for e in sp['flow'] if 'sub' in e]
    assert len(subs)==3, f"subs {a['slug']}"
    pulls=[e for e in sp['flow'] if 'pull' in e]; assert len(pulls)==1
    alsos=[e for e in sp['flow'] if 'also' in e]; assert len(alsos)==1
    # next slugs real, not self
    nx=sp['next']; assert nx['lead']['slug'] in allslugs and nx['lead']['slug']!=a['slug'], f"next lead {a['slug']} {nx['lead']['slug']}"
    for m in nx['minis']:
        assert m['slug'] in allslugs and m['slug']!=a['slug'], f"mini {a['slug']} {m['slug']}"
    # dek length
    assert len(a['dek'])<=300, f"dek long {a['slug']} {len(a['dek'])}"

leads=[a['slug'] for a in A if a.get('lead')]
assert leads==['israel-exchange-loses-its-chief'], f"lead issue {leads}"

json.dump(A, open('content/articles.json','w'), ensure_ascii=False, indent=1)
json.dump(E, open('content/editorial.json','w'), ensure_ascii=False, indent=1)
json.dump(W, open('content/wire.json','w'), ensure_ascii=False, indent=1)
json.dump(R, open('content/record.json','w'), ensure_ascii=False, indent=1)
print("OK articles:",len(A)," specs:",len(E)," lead:",leads)
print("new slugs:", [a['slug'] for a in articles_new])
print("record weeks:", [w['label'] for w in R['weeks'][:3]])
