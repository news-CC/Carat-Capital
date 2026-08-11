#!/usr/bin/env python3
# Edition No. 032 - 2026-08-11. Prepends 3 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-11"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - three-prices-one-carat ==========
art("three-prices-one-carat","diamonds",True,"Lead Story · Diamonds Desk",5,"The Diamonds Desk",
["NUM","VS","GAP"],
"$711, $650, $511: one lab-grown carat, three prices",
"CaratRadar's 1-carat lab-grown average read $711 on 11 August. TheDiamondPrice puts fair market at $650 inside a $590 to $760 range. This paper carried $511 from a third page on 7 August.",
[
"Two public reference pages for a one-carat lab-grown diamond were read at the same hour this morning and returned $711 and $650. CaratRadar, republished today, puts the one-carat average at $711 and states on the page that its figures are asking-price averages by shape, carat, colour and clarity, drawn from active certified listings across major online retailers and refreshed daily. TheDiamondPrice, carrying an August 2026 date, puts the fair market price of a one-carat round at $650 and says most comparable stones sit between $590 and $760, on a benchmark of E to F colour and VVS clarity. The gap is $61, or 9.4% on the lower figure, derived by this desk. One is what sellers ask. The other is what stones fetch.",
"The two are not in conflict, and that is the more useful finding. CaratRadar's $711 sits inside TheDiamondPrice's own $590 to $760 band, above its $675 midpoint and above its $650 central mark. An asking-price average built from live listings should sit above a transaction estimate, because a listing is an offer and a sale is an agreement, and the distance between them is the discount a buyer negotiates. What neither page publishes is that distance as a number, so a jeweller reading one of them has no way to know which side of the trade it describes. This paper carried a third reference on 9 August, StoneAlgo at $511 dated 7 August, and that page has not been re-read today; taken with today's two, the published span for the same stone runs from $511 to $711, about 39%.",
"The span matters because of what this stone now is. Lab-grown took 61% of United States engagement centre stones in 2025, a figure this desk published on 30 July, which makes the one-carat lab-grown round the single most-bought diamond in the American market. It is also the one with no settled price. Natural goods have the Rapaport list, published weekly on Thursdays, and the RapNet Diamond Index behind it. Grown goods have a set of independent aggregators, each computing a different quantity, none of them clearing a market, and none of them stating which side of the bid they stand on.",
"This paper's own instrument is inside the problem, and today it moves. The wire tape has carried a lab-grown one-carat line at $727 marked unchanged for several sessions with no source attached to the level. From this edition the line carries $711, the CaratRadar reading republished today, with the source and the date named on the tape, so the number on the tape is the number in this article and both can be checked against the page they came from. The two natural-diamond indices this tape also tries to carry, RAPI and the Zimnisky rough index, returned no numeric reading again this morning, the seventh consecutive session, and both continue to print unreachable rather than a figure this desk cannot stand behind.",
"The desk's view: the most-bought stone in America does not have a price, it has a range, and the trade has been quoting the middle of that range as though it were a fact. Nothing on either page read today is wrong. CaratRadar is measuring offers and says so; TheDiamondPrice is estimating transactions and says so. The failure is at the counter, where a single figure gets repeated without the qualifier that makes it meaningful, and a 9.4% error on a $650 stone is most of a retailer's margin on it. The practical instruction is to stop asking what a lab-grown carat costs and start asking which of the two questions the number answers. Until one of these pages publishes an ask-to-sale spread, a jeweller pricing a case should treat every published lab-grown reference as an upper bound and find the lower one in its own till receipts."
],
[
 {"title":"Lab-Grown Diamond Prices, 1 carat average — CaratRadar (read 11 August 2026)","url":"https://caratradar.com/diamond-prices/lab-grown-diamonds/"},
 {"title":"Lab Grown Diamond Prices by Carat, August 2026 — TheDiamondPrice (read 11 August 2026)","url":"https://thediamondprice.com/diamond-prices/lab-grown/"},
 {"title":"Sixty-one percent said lab — Carat Capital (30 July 2026)","url":"https://caratcapital.org/a-sixty-one-percent-said-lab.html"},
 {"title":"Rapaport Price List, published weekly — Rapaport","url":"https://rapaportauctions.com/rapaport-price-list/"},
])

# ========== 2. ten-forty-four-and-holding ==========
art("ten-forty-four-and-holding","gold-metals",False,"Gold & Metals Desk · Gulf",5,"The Gold & Metals Desk",
["NUM","VS"],
"AED 10.44 between two Dubai gold pages, and holding",
"Peg arithmetic on Kitco's 06:00 spot puts Dubai 24-carat gold at AED 516.31 a gram. LivePriceOfGold reads 516.26 and Goodreturns 526.75. Both pages moved with the metal today; the distance between them did not.",
[
"This paper reported yesterday that two widely quoted Dubai gold pages were publishing different quantities under one label, and left an open question about whether the distance between them would move. It has not. Kitco's live board at 06:00 New York time this morning, the reading this paper's tape now carries, puts gold at $4,372.80 an ounce. At 31.1035 grams to the troy ounce that is $140.59 a gram, and at the dirham's fixed peg of 3.6725 to the dollar it is AED 516.31 a gram, both conversions this desk's arithmetic. LivePriceOfGold's Dubai board, timestamped 11 August at 10:04 UTC, reads AED 516.26. That is five fils from the peg figure, about one hundredth of one per cent. Goodreturns' Dubai page, dated today, reads AED 526.75. The gap is a level, not a drift.",
"The three readings moved almost in lockstep overnight, which is the new information. Against yesterday's marks the peg figure added AED 3.72 a gram, LivePriceOfGold added AED 3.81 and Goodreturns added AED 3.50. All three moves sit inside AED 0.31 of each other. Yesterday's article described a counter page that had stepped up AED 13.25 between 7 and 8 August against a metal move of AED 3.13 and then held flat for three days while spot kept moving. Today it tracked. The step was a one-off repricing rather than a page that had stopped updating, and the wedge it opened has stayed where it was put.",
"That wedge can now be dated. On 7 August the peg arithmetic gave AED 509.42 against Goodreturns at AED 510.50, a difference of AED 1.08. On 10 August the peg gave AED 512.59 against 523.25, a difference of AED 10.66. Today it is AED 516.31 against 526.75, a difference of AED 10.44, or 2.02% of the metal. Three sessions at roughly AED 10.5 either side of a single AED 9.6 step taken on 8 August. A margin that arrives in one move and then holds through a metal rally is a pricing decision, not a data lag, and it is the sort of thing a buyer can plan around once it has a number on it.",
"The metals themselves opened firmer against this paper's own previous mark. The tape carries gold $4,372.80, silver $64.79, platinum $1,764.00 and palladium $1,362.00, each read at 06:00 New York time and each higher than the mark of record this paper set 24 hours earlier: gold by $31.40 or 0.72%, silver by $0.80 or 1.25%, platinum by $27.00 or 1.55%, palladium by $22.00 or 1.64%. Those changes measure desk to desk across a day, not one trading session, and Kitco's own session line at the same moment read gold and silver lower on the day against its previous close. Two conventions, one price, and the tape states which it uses. Fine gold is $140.59 a gram and the gold-to-silver ratio narrows to 67.49 from 67.84.",
"The desk's view: a step you can name is a cost you can price, and the Gulf counter lane has now given the trade a number to work with. Two mornings ago the honest answer to what Dubai gold costs was that it depended which page you opened. It still does, but the difference is no longer moving, and a stable AED 10.44 on a AED 516 metal is a fixed 2% that a jeweller can put into a quotation rather than discover at settlement. That is the difference between a spread and a surprise. The instruction from yesterday stands and gets easier to follow today: quote the peg arithmetic beside whatever page you use, and if the two lanes ever converge or the wedge steps again, that is the event worth reacting to rather than the daily print."
],
[
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (11 August 2026, 06:00 EST live board)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Dubai Gold Price Live, in United Arab Emirates dirhams — LivePriceOfGold (11 August 2026, 10:04 UTC)","url":"https://www.livepriceofgold.com/dubai-gold-price.html"},
 {"title":"Today's Gold Rate in Dubai, 18, 22 & 24 Carat — Goodreturns (11 August 2026, with ten-day table)","url":"https://www.goodreturns.in/gold-rates/dubai.html"},
 {"title":"Two Dubai gold rates, 2% apart. Neither one is wrong — Carat Capital (10 August 2026)","url":"https://caratcapital.org/a-neither-one-is-wrong.html"},
])

# ========== 3. one-state-one-banner ==========
art("one-state-one-banner","retail-tech",False,"Retail & Technology Desk · India",4,"The Retail Desk",
["ACTOR","GAP"],
"Kalyan builds a second brand for one Indian state",
"Kalyan Jewellers opens Akshaya Thanga Maligai at Panagal Park in Chennai on 21 August, a Tamil Nadu-only banner it intends to expand by franchise. The group already runs more than 400 showrooms across seven countries.",
[
"Kalyan Jewellers is launching a second retail brand that will trade in one Indian state and nowhere else. Akshaya Thanga Maligai, announced on 3 August, opens its first showroom at Panagal Park in T. Nagar, Chennai, on 21 August, selling hallmarked gold and certified diamond jewellery cut to Tamil Nadu design preferences. The company intends to expand it through franchising within the state before considering any other, and has signed the actor Sivakarthikeyan to carry it. Kalyan itself already operates more than 400 showrooms across India, the United Arab Emirates, Kuwait, Qatar, Oman, the United States and the United Kingdom. A national chain does not build a second sign for one state casually.",
"The logic is a bet about where volume is left. India's organised jewellery chains have spent a decade taking share from family jewellers by putting a national brand into a regional high street, and Kalyan's own footprint is the result. What the new banner concedes is that the last tranche of that share does not come to a national name. Rajesh Kalyanaraman, the executive director, framed the reasoning as regional markets offering long-term growth when approached with a local proposition. Tamil Nadu is one of the deepest gold markets in the country and one of the most resistant to outside brands, and a separate banner with its own name, its own designs and a Tamil film star attached is a different instrument to a Kalyan store with a Tamil window display.",
"The financing choice is the part the trade should read. Franchising, rather than owned showrooms, is how the group has said it will grow the new brand inside the state. That puts the working capital for the gold on somebody else's balance sheet at a moment when the metal is the most expensive it has ever been, with spot at $4,372.80 an ounce on this paper's tape this morning. A jewellery showroom is mostly a pile of financed inventory, and the cost of carrying that pile has risen with every gold rally this year. Expanding a new format on franchise capital transfers that carry.",
"The demand backdrop is the one this paper has been filing all month, and it is not a growth story on volume. Indian gold jewellery demand fell 15% by weight in the second quarter to 75.1 tonnes, the lowest second quarter since the pandemic, while the value of that demand rose about 50%. Kalyan took more than 46% of its June-quarter revenue in recycled metal and more than 55% in the month of June alone. Those two facts describe a market where customers are still coming in but bringing their own gold with them. A new banner does not change that arithmetic; it changes who the customer walks past on the way in.",
"The desk's view: the growth left in Indian jewellery is local, and it is being bought one state at a time. Kalyan is not adding a store, it is admitting that its own name has a ceiling in a market it has traded in for years, and paying to get under that ceiling with a different sign. For independents in Tamil Nadu the read is direct and unwelcome, because the competitor arriving on 21 August is not a national chain with a regional accent, it is a purpose-built local brand with national buying behind it, and franchising means it can arrive in more places faster than an owned rollout could. The number to watch is not the opening. It is how many franchise agreements the group announces in the state before the festival season, because that is the figure that will say whether the format works."
],
[
 {"title":"Kalyan Jewellers launches regional jewellery brand 'Akshaya Thanga Maligai' in Tamil Nadu — The Retail Jeweller (3 August 2026)","url":"https://retailjewellerindia.com/kalyan-jewellers-launches-regional-jewellery-brand-akshaya-thanga-maligai-in-tamil-nadu/"},
 {"title":"Forty-six percent came back — Carat Capital (9 August 2026)","url":"https://caratcapital.org/a-forty-six-percent-came-back.html"},
 {"title":"India buys fifteen percent less — Carat Capital (31 July 2026)","url":"https://caratcapital.org/a-india-buys-fifteen-percent-less.html"},
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (11 August 2026, 06:00 EST live board)","url":"https://www.kitco.com/price/precious-metals"},
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

specs["three-prices-one-carat"] = {
 **strip("By the numbers · One-carat lab-grown, 11 August",[
   {"fig":"$711","lab":"CaratRadar, asking-price average"},
   {"fig":"$650","lab":"TheDiamondPrice, fair market"},
   {"fig":"9.4%","delta":"▲","dir":"up","lab":"the gap, derived by this desk"},
   {"fig":"$590-760","lab":"the range the second page states"},
   {"fig":"61%","lab":"US engagement centre stones grown, 2025"}]),
 "figs":[bars("Plate I","One-carat lab-grown diamond, published references · dollars",[
   {"l":"CARATRADAR, ASKING AVERAGE (11 AUG)","v":711,"d":"$711","hi":True},
   {"l":"THEDIAMONDPRICE, FAIR MARKET (AUG)","v":650,"d":"$650"},
   {"l":"STONEALGO (7 AUG, NOT RE-READ TODAY)","v":511,"d":"$511"}],
   "Two pages read live on 11 August 2026; the third is the figure this paper carried in its wire on 9 August, dated 7 August, and not re-read today. The three describe different quantities.",211)],
 "flow":flow5("Two pages, one stone, sixty-one dollars apart.","An offer is not a sale.","The tape carries the number the article prints.",
   "One is what sellers ask. The other is what stones fetch","The Diamonds Desk",
   "Lab-grown finds its floor","a-lab-grown-finds-its-floor.html"),
 "desk":{"split":"the most-bought stone in America does not have a price, it has a range"},
 "next":nxt("ten-forty-four-and-holding","Metals","Two Dubai gold pages moved together overnight and stayed AED 10.44 apart.",
   "lab-grown-finds-its-floor","Diamonds","sixty-one-percent-said-lab","Retail")}

specs["ten-forty-four-and-holding"] = {
 **strip("By the numbers · Dubai 24-carat gold, 11 August",[
   {"fig":"AED 526.75","delta":"▲ +3.50","dir":"up","lab":"Goodreturns, 24-carat, a gram"},
   {"fig":"AED 516.31","lab":"peg arithmetic on spot, derived"},
   {"fig":"AED 516.26","delta":"▲ +3.81","dir":"up","lab":"LivePriceOfGold, same carat"},
   {"fig":"AED 10.44","lab":"the wedge, third session at the level"},
   {"fig":"$4,372.80","lab":"gold spot, Kitco 06:00 EST"}]),
 "figs":[bars("Plate I","The Dubai wedge · Goodreturns less peg arithmetic, dirhams a gram",[
   {"l":"11 AUGUST","v":10.44,"d":"AED 10.44","hi":True},
   {"l":"10 AUGUST","v":10.66,"d":"AED 10.66"},
   {"l":"7 AUGUST","v":1.08,"d":"AED 1.08"}],
   "Peg arithmetic is this desk's conversion of Kitco spot at the dirham's fixed 3.6725 rate. The step between 7 and 10 August was taken in one move on 8 August and has held since.",212)],
 "flow":flow5("Five fils from the arithmetic, ten dirhams from the counter.","Three readings, one overnight move.","The wedge, dated.",
   "The gap is a level, not a drift","The Gold & Metals Desk",
   "Two Dubai gold rates, 2% apart","a-neither-one-is-wrong.html"),
 "desk":{"split":"a step you can name is a cost you can price"},
 "next":nxt("one-state-one-banner","Retail","Kalyan is opening a Tamil Nadu-only banner in Chennai on 21 August.",
   "neither-one-is-wrong","Metals","the-fourteen-percent-that-isnt","Metals")}

specs["one-state-one-banner"] = {
 **strip("By the numbers · Kalyan's Tamil Nadu banner",[
   {"fig":"21 Aug","lab":"first Akshaya Thanga Maligai opens, Chennai"},
   {"fig":"400+","lab":"Kalyan showrooms, seven countries"},
   {"fig":"1","lab":"state the new brand will trade in"},
   {"fig":"46%","lab":"June-quarter revenue taken in recycled metal"},
   {"fig":"75.1t","delta":"▼ −15%","dir":"down","lab":"Indian Q2 jewellery demand by weight"}]),
 "figs":[bars("Plate I","Kalyan Jewellers · recycled metal as a share of revenue, per cent",[
   {"l":"JUNE 2026, THE MONTH","v":55,"d":">55%","hi":True},
   {"l":"JUNE QUARTER 2026","v":46,"d":">46%"}],
   "Company figures previously filed by this paper on 9 August 2026. Customers exchanging old gold rather than buying new is the demand backdrop the new banner opens into.",213)],
 "flow":flow5("A second sign, one state.","What a separate banner concedes.","Franchise capital carries the gold.",
   "A national chain does not build a second sign for one state casually","The Retail Desk",
   "Forty-six percent came back","a-forty-six-percent-came-back.html"),
 "desk":{"split":"the growth left in Indian jewellery is local, and it is being bought one state at a time"},
 "next":nxt("three-prices-one-carat","Diamonds","Two reference pages priced the same lab-grown carat $61 apart this morning.",
   "forty-six-percent-came-back","Retail","india-buys-fifteen-percent-less","Demand")}

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
