#!/usr/bin/env python3
# Edition No. 035 - 2026-08-14. Prepends 3 articles + specs.
import json, pathlib, sys
C = pathlib.Path("content")
articles = json.loads((C/"articles.json").read_text())
editorial = json.loads((C/"editorial.json").read_text())

DATE = "2026-08-14"

for a in articles:
    if a.get("lead"): a["lead"] = False

NEW = []
def art(slug, desk, lead, kicker, minutes, byline, tags, title, dek, body, sources):
    d = {"slug":slug,"desk":desk,"date":DATE,"lead":lead,"kicker":kicker,"minutes":minutes,
         "byline":byline,"tags":tags,"title":title,"dek":dek,"body":body,"sources":sources}
    NEW.append(d); return d

# ========== 1. LEAD - nine-forty-and-thirteen-twelve ==========
art("nine-forty-and-thirteen-twelve","gold-metals",True,"Lead Story · Gold & Metals Desk",5,"The Gold & Metals Desk",
["PLAIN","NUM"],
"China's jewellery counter charges 39.5% over the exchange price",
"The Shanghai Gold Exchange closed Au99.99 at 940.72 yuan a gram on 14 August. Chow Tai Fook's counter reads 1,312. The gap is 371.28 yuan, and it is wider than it was six days ago.",
[
"The Shanghai Gold Exchange closed its Au99.99 contract at 940.72 yuan a gram today, from an opening of 955.00 and a session low of 933.01, on 3,886.14 kilogrammes of volume. The exchange's deferred contract, Au(T+D), closed at 940.44 on 41,646 kilogrammes. Those are the exchange's own published daily quotations rather than an aggregator's copy of them. On the same day Chow Tai Fook listed 24-carat jewellery at 1,312 yuan a gram, a figure carried identically by two independent Chinese price aggregators, jinjia.com.cn and cngold, which is the strongest agreement available on a counter price. Dividing one by the other, this desk's arithmetic, puts the counter 39.47% above the exchange, a gap of 371.28 yuan on every gram sold.",
"That gap is not closing. This paper published the same pair on 9 August at 938 yuan on the exchange and 1,286 at the counter, a spread of 348 yuan and a markup of 37.10%. Six days later the exchange has moved 2.72 yuan, or 0.29%, and the counter has moved 26 yuan, or 2.02%. The gap did not close; it widened by 23.28 yuan a gram. Two disclosures belong with that sentence. One aggregator's series carries 1,286 against 7 August rather than 8 August, and the same two aggregators disagree about 13 August by 11 yuan, one reading 1,340 and the other 1,329. This desk cannot establish which board hour either page is reading and does not resolve it here. The 14 August figure is the one both of them agree on, which is why the comparison is anchored there.",
"Today's session moved both legs down and moved them at very different speeds. The exchange closed 8.52 yuan lower than its 13 August close of 949.24, a fall of 0.90%. The counter came off 28 yuan from 1,340, a fall of 2.09%, cutting about two and a third times as fast as the metal it is made of. The premium therefore narrowed today, from 41.17% on one aggregator's 13 August counter price or 40.01% on the other's, to 39.47%. The counter moves in steps and the exchange moves in fractions: across the sessions the aggregator series records this month, the Chow Tai Fook price went 1,231, then 1,240, then 1,297, then 1,286, then 1,308, held at 1,308, then 1,336, 1,329, 1,340 and 1,312. Almost every one of those is a round jump of tens of yuan against an exchange that rarely moves one per cent in a day.",
"For anyone pricing against China, the useful figure is the band rather than the day. On the readings this desk can verify, the Chinese jewellery markup has run between 37.10% and 41.17% this month, and it is currently near the top half of that range while the metal itself is falling. This paper reported on 3 August that China's gold jewellery consumption fell to its lowest since 2004, and on 9 August that the country's bullion buying was its heaviest month since 2023. A widening retail markup against a shrinking jewellery volume and a rising bar-and-coin volume is the same story told three ways. The limit on all of it should be stated plainly: a listed counter price is an asking price, not a transacted one, and workmanship charges, store discounts and buy-back terms sit outside both numbers here.",
"The desk's view: the counter is not a gold price, it is a retail price that happens to be quoted in grams, and the last six days are the clearest demonstration of it this paper has had. The exchange has barely moved since 8 August and the shop window has moved eight times as far, in both directions, in round steps that no metal market produced. That is a merchant setting a margin, not a market clearing. The number worth watching is not 1,312 and not 940.72 but the 39.47% between them, because that is the only one of the three that describes a decision somebody made. Watch whether the markup settles below 39% now that the counter has started cutting faster than the exchange. If it does not, the Chinese shopper is paying a wider margin into a falling market, which is the opposite of what a falling market is supposed to do to margins."
],
[
 {"title":"Daily quotations, Au99.99 and Au(T+D), 14 August 2026 — Shanghai Gold Exchange","url":"https://www.sge.com.cn/sjzx/quotation_daily_new"},
 {"title":"周大福今日金价 — Chow Tai Fook daily counter price series, read 14 August 2026 — 金价网","url":"https://www.jinjia.com.cn/chowtaifook/"},
 {"title":"周大福黄金价格查询 — Chow Tai Fook quotation page, read 14 August 2026 — 金投网","url":"https://m.cngold.org/quote/gjs/swhj_zdf.html"},
 {"title":"938 at the exchange, 1,286 at the counter — Carat Capital (9 August 2026)","url":"https://caratcapital.org/a-nine-thirty-eight-and-twelve-eighty-six.html"},
 {"title":"China's gold counter falls to its lowest since 2004 — Carat Capital (3 August 2026)","url":"https://caratcapital.org/a-china-lowest-since-2004.html"},
])

# ========== 2. the-platinum-hold-ends ==========
art("the-platinum-hold-ends","gold-metals",False,"Gold & Metals Desk · The Tape",5,"The Gold & Metals Desk",
["NUM","REVERSAL"],
"The platinum hold ends at $1,725 after three mornings",
"Kitco's board read gold $4,356.20, silver $64.77, platinum $1,725.00 and palladium $1,297.00 at 06:00 New York time. All four are written back to this paper's tape. Two of them had been held for days.",
[
"Kitco's live board at 06:00 New York time read gold at $4,356.20 an ounce, silver at $64.77, platinum at $1,725.00 and palladium at $1,297.00, and all four readings are now this paper's marks of record, written back over caratwire's 04:59 marks with the source named and the timestamp new. Measured against this paper's own marks 24 hours earlier, gold is down $27.90 or 0.64%, silver is up $0.25 or 0.39%, platinum is up $15.00 or 0.88% and palladium is down $22.00 or 1.67%. The gold-to-silver ratio, this desk's division of its own gold mark by its own silver mark on the same board at the same minute, narrowed to 67.26 from 67.95. Gold and silver were each checked against TradingEconomics the same morning, at $4,356.79 and $64.89, differences of 0.01% and 0.19%.",
"The change worth explaining is platinum, which this paper has now refused twice and is taking today. On 12 August Kitco's platinum cell was stale and the mark was held. On 13 August the cell was live but sat $14.60 below TradingEconomics and JM Bullion, which agreed with each other to within 50 cents, so the mark was held again. At 04:59 this morning the tape desk found the same shape a third time, Kitco $13.30 below TradingEconomics, and held once more. At 06:00 the gap is $12.70 against TradingEconomics at $1,737.70 and $14.90 against JM Bullion at $1,739.90, and those two pages again agree with each other, this time to $2.20 or 0.13%. Three mornings of the same gap in the same direction is a basis difference between outside pages rather than a market nobody can read, and treating it as the second thing had a cost: the held mark of $1,710.00 was two sessions old and 1.62% below where two other pages put the metal.",
"So platinum is written back on Kitco, the board that carries every other mark on this tape, and palladium with it at Kitco's $1,297.00 bid. JM Bullion read palladium at $1,336.71 at 06:01 New York time, $39.71 or 3.06% higher, which on a metal this thin reads as the other side of a spread rather than a disagreement about the price. The alternative was to leave one Kitco mark frozen and three Kitco marks fresh, taken from the same board at the same minute, which is precisely the two-numbers problem the one-price rule was written to remove. The divergence between the outside pages is disclosed here rather than reconciled, because that rule is untouched and it is the more important one: a jeweller quoting platinum off a single public board this morning is choosing between $1,725.00 and $1,739.90 without being told there is a choice.",
"At the bench the four marks work out at $140.05 a gram of fine gold, $2.08 a gram of fine silver, $55.46 a gram of fine platinum and $41.70 a gram of fine palladium, at 31.1035 grams to the troy ounce and all four this desk's arithmetic. Palladium's 1.67% fall is the largest single-day move on the tape today and it comes off a mark that had itself been held for two sessions, so a workshop repricing palladium stock is absorbing two days of movement in one step rather than one day's. Silver has now recovered $0.25 of the $1.78 it lost yesterday, and gold has given back $27.90 of a week in which it has still gained ground. The ratio at 67.26 sits between Monday's 67.49 and Wednesday's 66.59 and has told nobody anything for five sessions.",
"The desk's view: a rule that stops a paper printing a number it cannot stand behind is not the same as a rule that stops it printing numbers, and the difference showed up here as a mark going quietly stale under the protection of good procedure. Holding platinum on 12 and 13 August was right on the evidence available on those mornings. Holding it a third time would have been the habit rather than the judgement, because by the third morning the evidence had changed shape: a gap that recurs at the same size and sign is information about how two pages are quoting, not about whether a price exists. The tape is better for taking the mark and disclosing the spread than it was for holding a two-day-old figure and calling it caution. The test for tomorrow is simple. If Kitco is still $13 light on platinum, this paper says so again in print and keeps its own basis consistent."
],
[
 {"title":"Gold, Silver, Platinum & Palladium Spot Prices — Kitco (14 August 2026, 06:00 EST live board)","url":"https://www.kitco.com/price/precious-metals"},
 {"title":"Gold — price, chart, historical data (read 14 August 2026)","url":"https://tradingeconomics.com/commodity/gold"},
 {"title":"Platinum Prices Today Per Ounce, 24hr spot chart — JM Bullion (14 August 2026, 06:01 EST)","url":"https://www.jmbullion.com/charts/platinum-price/"},
 {"title":"Three sessions of silver's gain undone in one — Carat Capital (13 August 2026)","url":"https://caratcapital.org/a-three-sessions-undone.html"},
])

# ========== 3. seventy-one-million-from-america ==========
art("seventy-one-million-from-america","gold-metals",False,"Gold & Metals Desk · Investment Demand",5,"The Gold & Metals Desk",
["NUM","VS"],
"$71 million from America in a $3 billion gold month",
"Gold ETFs took in $3bn in July, the World Gold Council reported on 6 August. Europe supplied $2bn of it and North America $71mn. Collective holdings rose 23 tonnes to 4,068.",
[
"Global gold-backed exchange-traded funds took in $3 billion in July, reversing two consecutive months of outflows, in figures the World Gold Council published on 6 August under the title Europe's golden heatwave. Collective holdings rose 23 tonnes to 4,068 tonnes and assets under management rose 1% to $530 billion. This paper has cited the World Gold Council fifteen times and has never once covered its monthly flows series, which is a gap on this desk rather than a scoop, and the figures are eight days old as they print here. They are reported now because this paper has spent August printing a gold mark every morning and reporting the physical buyer, and has never said who was on the other side of the trade.",
"The regional split is the finding. Europe took $2 billion of the month's inflow, with the United Kingdom alone at $875 million and Switzerland at $657 million. Asia took $616 million, with China the strongest contributor and Japan in outflow. North America took $71 million. Other regions, chiefly Australia and South Africa, took $140 million. Two European countries raised nearly twice what the rest of the world did: $1,532 million from Britain and Switzerland against $827 million from Asia, North America and everywhere else combined, a ratio of 1.85 to one and this desk's arithmetic. North America, the largest gold ETF market in the world by assets, supplied 2.5% of the named regional total. The named regions sum to $2,827 million against a headline of $3 billion, because every component is rounded, and that difference is this desk's subtraction rather than a discrepancy in the source.",
"Set that against what this paper has already published about the physical buyer and the year stops looking contradictory. Global jewellery demand fell to 278 tonnes in the second quarter, the smallest since the pandemic, reported here on 31 July. India took 75.1 tonnes, down 15% by weight, reported the same day. China's gold jewellery consumption fell to its lowest since 2004, reported here on 3 August. Through all of that the gold price rose, and the question this desk kept leaving open was who was buying what the bride was not. Part of the answer is a European investor putting $2 billion into a fund in a single month while the American investor sat out with $71 million, and the rest is central banks and the Chinese bar buyer this paper covered on 9 August.",
"Three limits belong on this. The series is monthly and it is eight days old, so it describes July and says nothing about the $27.90 gold gave back this morning. Holdings at 4,068 tonnes remain 108 tonnes, or 2.59%, below the record of 4,176 tonnes set on 27 February, so a month of inflow has not undone the year's withdrawal. And the 1% rise in assets under management against a 23-tonne rise in holdings means most of the gain in the dollar figure is the gold price rather than new money arriving. Activity thinned in the same month: average daily trading volumes across the gold market fell 3.5% to $356 billion and over-the-counter volumes fell 3.4% to $205 billion. Money came in through a quieter door than usual.",
"The desk's view: the marginal buyer of gold in July was European, and a trade paper that prints a dollar-an-ounce number every morning without ever naming that buyer has been reporting half the market. The useful correction is to stop reading gold demand as one number. The jewellery counter is shrinking in India and China, the bar buyer is heavy in China, the fund buyer is British and Swiss, and the American fund buyer is barely present at all. Those four move on different reasons and they can point in opposite directions for months at a time, which is exactly what they did in July. The number to watch next month is North America's $71 million, because that is a market of a size that could reverse the whole global figure by itself if the American investor came back, and the only thing keeping it small is that so far he has not."
],
[
 {"title":"Gold ETF Flows: July 2026, Europe's golden heatwave — World Gold Council (6 August 2026)","url":"https://www.gold.org/goldhub/research/gold-etfs-holdings-and-flows/2026/08"},
 {"title":"278 tonnes: the smallest jewellery quarter since the pandemic — Carat Capital (31 July 2026)","url":"https://caratcapital.org/a-two-seventy-eight-tonnes.html"},
 {"title":"India's quarter: 75.1 tonnes of jewellery, down 15% — Carat Capital (31 July 2026)","url":"https://caratcapital.org/a-india-buys-fifteen-percent-less.html"},
 {"title":"China's gold counter falls to its lowest since 2004 — Carat Capital (3 August 2026)","url":"https://caratcapital.org/a-china-lowest-since-2004.html"},
 {"title":"640,000 ounces: China's biggest gold month since 2023 — Carat Capital (9 August 2026)","url":"https://caratcapital.org/a-six-forty-thousand-ounces.html"},
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

specs["nine-forty-and-thirteen-twelve"] = {
 **strip("By the numbers · China's gold counter, 14 August",[
   {"fig":"940.72","delta":"▼ −0.90%","dir":"down","lab":"Au99.99 close, yuan a gram"},
   {"fig":"1,312","delta":"▼ −2.09%","dir":"down","lab":"Chow Tai Fook counter, same day"},
   {"fig":"371.28","lab":"the gap in yuan, derived here"},
   {"fig":"39.47%","lab":"the markup, derived here"},
   {"fig":"+23.28","delta":"▲","dir":"up","lab":"yuan added to the gap since 8 August"}]),
 "figs":[bars("Plate I","China's counter against China's exchange · yuan a gram",[
   {"l":"COUNTER, 14 AUGUST","v":1312,"d":"1,312","hi":True},
   {"l":"COUNTER, 8 AUGUST","v":1286,"d":"1,286"},
   {"l":"EXCHANGE, 14 AUGUST","v":940.72,"d":"940.72"},
   {"l":"EXCHANGE, 8 AUGUST","v":938,"d":"938.00"}],
   "Exchange figures are the Shanghai Gold Exchange's own published Au99.99 quotations. The 8 August pair is as this paper published it on 9 August. In six days the exchange moved 0.29% and the counter moved 2.02%, widening the markup from 37.10% to 39.47%, this desk's arithmetic.",222)],
 "flow":flow5("Two prices for the same gram.","Six sessions, and the gap is wider.","A stepped price against a traded one.",
   "The gap did not close; it widened by 23.28 yuan a gram","The Gold & Metals Desk",
   "938 at the exchange, 1,286 at the counter","a-nine-thirty-eight-and-twelve-eighty-six.html"),
 "desk":{"split":"the counter is not a gold price, it is a retail price that happens to be quoted in grams"},
 "next":nxt("the-platinum-hold-ends","Metals","Kitco's board carried all four metals back onto the tape at 06:00 New York time.",
   "seventy-one-million-from-america","Metals","nine-thirty-eight-and-twelve-eighty-six","Metals")}

specs["the-platinum-hold-ends"] = {
 **strip("By the numbers · The tape, 14 August",[
   {"fig":"$4,356.20","delta":"▼ −0.64%","dir":"down","lab":"gold, Kitco 06:00 EST, written back"},
   {"fig":"$64.77","delta":"▲ +0.39%","dir":"up","lab":"silver, same board, same read"},
   {"fig":"$1,725.00","delta":"▲ +0.88%","dir":"up","lab":"platinum, the two-day hold ends"},
   {"fig":"$1,297.00","delta":"▼ −1.67%","dir":"down","lab":"palladium, written back with it"},
   {"fig":"67.26","delta":"▼ −0.69","dir":"down","lab":"gold-to-silver ratio, derived"}]),
 "figs":[bars("Plate I","Platinum on three pages, 14 August · dollars an ounce",[
   {"l":"JM BULLION, 06:01 EST","v":1739.90,"d":"$1,739.90"},
   {"l":"TRADINGECONOMICS","v":1737.70,"d":"$1,737.70"},
   {"l":"KITCO, 06:00 EST","v":1725.00,"d":"$1,725.00","hi":True},
   {"l":"THE HELD MARK, 13 AUG","v":1710.00,"d":"$1,710.00"}],
   "The two pages this paper does not carry as its mark of record agree to $2.20, or 0.13%, and sit $12.70 to $14.90 above Kitco for a third consecutive morning. The mark this paper had been holding sat 1.62% below both of them. Divergence between outside sources, disclosed rather than resolved.",223)],
 "flow":flow5("Four marks, one board, one minute.","Why the hold ended.","What it costs at the bench.",
   "Three mornings of the same gap in the same direction is a basis difference","The Gold & Metals Desk",
   "Three sessions of silver's gain undone in one","a-three-sessions-undone.html"),
 "desk":{"split":"a mark going quietly stale under the protection of good procedure"},
 "next":nxt("seventy-one-million-from-america","Metals","Europe put $2bn into gold funds in July. North America put in $71mn.",
   "three-sessions-undone","Metals","sixty-six-fifty-nine","Metals")}

specs["seventy-one-million-from-america"] = {
 **strip("By the numbers · Gold ETF flows, July 2026",[
   {"fig":"$3bn","delta":"▲","dir":"up","lab":"global inflow, two outflow months reversed"},
   {"fig":"$2bn","lab":"Europe, of which UK $875mn"},
   {"fig":"$71mn","lab":"North America, the whole month"},
   {"fig":"4,068t","delta":"▲ +23t","dir":"up","lab":"collective holdings"},
   {"fig":"−108t","lab":"still below the 27 February record"}]),
 "figs":[bars("Plate I","Where July's gold ETF money came from · millions of dollars",[
   {"l":"EUROPE","v":2000,"d":"$2,000m","hi":True},
   {"l":"ASIA","v":616,"d":"$616m"},
   {"l":"OTHER REGIONS","v":140,"d":"$140m"},
   {"l":"NORTH AMERICA","v":71,"d":"$71m"}],
   "World Gold Council figures published 6 August 2026. The named regions sum to $2,827m against a rounded headline of $3bn because every component is rounded; that subtraction is this desk's. Britain and Switzerland alone contributed $1,532m, 1.85 times everything raised outside Europe.",224)],
 "flow":flow5("A reversal, and where it came from.","Two countries against the world.","The buyer this paper had not named.",
   "Two European countries raised nearly twice what the rest of the world did","The Gold & Metals Desk",
   "278 tonnes: the smallest jewellery quarter since the pandemic","a-two-seventy-eight-tonnes.html"),
 "desk":{"split":"the marginal buyer of gold in July was European"},
 "next":nxt("nine-forty-and-thirteen-twelve","Metals","China's jewellery counter is charging 39.47% over the Shanghai exchange price.",
   "two-seventy-eight-tonnes","Metals","six-forty-thousand-ounces","Metals")}

# ---------------- validation ----------------
existing = {a["slug"] for a in articles} | {a["slug"] for a in NEW}
errs = []
for a in NEW:
    s = a["slug"]
    if len(a["body"]) != 5: errs.append("%s: body has %d paragraphs, need 5" % (s, len(a["body"])))
    if not a["body"][4].startswith("The desk's view:"): errs.append("%s: para 5 does not open 'The desk's view:'" % s)
    if "!" in " ".join(a["body"]): errs.append("%s: exclamation mark in body" % s)
    em = " ".join(a["body"]).count("—")
    if em > 1: errs.append("%s: %d em-dashes in body" % (s, em))
    if len(a["dek"].split()) > 40: errs.append("%s: dek is %d words" % (s, len(a["dek"].split())))
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
    print("  %-34s %2d words" % (a["slug"], len(pull.split())))

articles = NEW + articles
for s in specs: editorial[s] = specs[s]
(C/"articles.json").write_text(json.dumps(articles, ensure_ascii=False, indent=1))
(C/"editorial.json").write_text(json.dumps(editorial, ensure_ascii=False, indent=1))
print("OK: %d articles prepended, %d specs written, total %d" % (len(NEW), len(specs), len(articles)))
