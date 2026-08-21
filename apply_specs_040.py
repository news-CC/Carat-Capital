#!/usr/bin/env python3
# Edition No. 040 - editorial specs for the 9 articles.
import json, pathlib
C = pathlib.Path("content")
editorial = json.loads((C/"editorial.json").read_text())

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

specs["platinum-takes-the-biggest-move"] = {
 **strip("By the numbers · The tape, 21 August",[
   {"fig":"$4,581.60","delta":"▲ +2.22%","dir":"up","lab":"gold, vs this paper's 20 Aug mark"},
   {"fig":"$69.31","delta":"▲ +4.08%","dir":"up","lab":"silver, same basis"},
   {"fig":"$1,881.00","delta":"▲ +4.56%","dir":"up","lab":"platinum, a one-session hold ends"},
   {"fig":"$1,336.00","delta":"▲ +2.14%","dir":"up","lab":"palladium, same hold ends"},
   {"fig":"66.10","delta":"▼ −1.21","dir":"down","lab":"gold-to-silver ratio, derived"}]),
 "figs":[bars("Plate I","Platinum on two pages against the mark it retires · dollars an ounce, 21 August",[
   {"l":"TRADINGECONOMICS","v":1894.40,"d":"$1,894.40"},
   {"l":"KITCO, 05:59 EDT","v":1881.00,"d":"$1,881.00","hi":True},
   {"l":"THE HELD MARK, 20 AUG","v":1799.00,"d":"$1,799.00"},
   {"l":"THE MARK BEFORE IT, 19 AUG","v":1726.00,"d":"$1,726.00"}],
   "The two outside pages remain $13.40, or 0.71%, apart on platinum and are disclosed rather than reconciled. The mark being retired is not one of the two live readings and sits below both. Kitco is taken because it is the board already carrying gold and silver on this tape. Against 19 August's mark, platinum has added close to nine per cent across two of this paper's sessions.",234)],
 "flow":flow5("Four marks, one board, two bases.","The two marks that sat below everybody.","What the move is, and what it is not.",
   "Both bases point the same way this morning, which they did not yesterday","The Gold & Metals Desk",
   "Two held marks come off the tape at once","a-both-holds-end-at-once.html"),
 "desk":{"split":"a rule that retires a stale mark is only worth having if it fires in both directions"},
 "next":nxt("fifty-nine-years-and-thirty-four-percent","Diamonds","Finsch will not reopen, and it carried 34% of Petra's revenue.",
   "both-holds-end-at-once","Metals","four-metals-four-write-backs","Metals")}

specs["fifty-nine-years-and-thirty-four-percent"] = {
 **strip("By the numbers · Finsch, at closure",[
   {"fig":"59","lab":"years of commercial mining, 1967–2026"},
   {"fig":"34%","lab":"of Petra's revenue, fiscal 2025"},
   {"fig":">90%","lab":"of output below two carats"},
   {"fig":"7 Aug","lab":"creditors approve the asset sale"},
   {"fig":"1","lab":"mine Petra has left"}]),
 "figs":[bars("Plate I","Rescue to closure in ten weeks · Finsch, 2026",[
   {"l":"29 MAY · BUSINESS RESCUE BEGINS","v":0,"d":"day 0"},
   {"l":"JUNE · PRODUCTION SUSPENDED","v":30,"d":"about day 30"},
   {"l":"28 JULY · MARKET UPDATE","v":60,"d":"day 60"},
   {"l":"7 AUGUST · CREDITORS APPROVE SALE","v":70,"d":"day 70","hi":True}],
   "Counted by this desk from Petra's own announcements. The plan approved on 7 August concludes that no viable outcome exists to resume mining, which converts a suspension into a closure. Proceeds are distributed by ranking of claims, with the secured creditor that provided post-commencement funding ranking highest.",235)],
 "flow":flow5("A rescue that found nothing to rescue.","The goods, not the operation.","One mine left, at the other end of the scale.",
   "More than 90% of Finsch's output was below two carats","The Diamonds Desk",
   "Petra's revenue caves as the small-stone squeeze bites","a-petra-caves-at-the-bottom.html"),
 "desk":{"split":"the number that should travel from this is not 59 years, it is 34%"},
 "next":nxt("sixty-seven-percent-buy-it-for-themselves","Retail","Zales publishes a 67% self-purchase rate and rebuilds a campaign around it.",
   "petra-caves-at-the-bottom","Diamonds","alrosa-books-the-loss","Diamonds")}

specs["sixty-seven-percent-buy-it-for-themselves"] = {
 **strip("By the numbers · Zales, You Are The Occasion",[
   {"fig":"67%","lab":"of core-shopper purchases, self-purchase"},
   {"fig":"3","lab":"style stories in the campaign"},
   {"fig":"2 of 3","lab":"need no occasion at all"},
   {"fig":"4","lab":"bridal aesthetics inside the third"},
   {"fig":"2025","lab":"the Own It campaign this iterates on"}]),
 "figs":[bars("Plate I","What the campaign merchandises · Zales, August 2026",[
   {"l":"EVERYDAY ELEVATED · NO OCCASION","v":1,"d":"tennis, rivière, ear stacks, solitaire pendants","hi":True},
   {"l":"STACKING & LAYERING · NO OCCASION","v":1,"d":"chains, bracelets, bands, pendants","hi":True},
   {"l":"BRIDAL & ENGAGEMENT · OCCASION","v":1,"d":"four named aesthetics"}],
   "Read from Zales' own campaign description. Two of the three story lines are built on repeat purchase of pieces requiring no event; only the third depends on the calendar the campaign argues against. Campaign imagery includes men wearing watches and gold chains.",236)],
 "flow":flow5("A number, and a campaign attached to it.","What is actually being merchandised.","What a self-purchase counter changes.",
   "Sixty-seven per cent of purchases among its core shoppers were made for themselves","The Retail & Technology Desk",
   "Signet gives Zales and Banter to a Mattel executive","a-zales-goes-to-mattel.html"),
 "desk":{"split":"the 67% is a disclosure and should be read as one"},
 "next":nxt("sixty-five-percent-on-a-chip-substrate","Diamonds","China's lab-grown exports rose 65.3%, and not because of jewellery.",
   "zales-goes-to-mattel","Retail","tiffany-goes-to-blue-nile","Retail")}

specs["sixty-five-percent-on-a-chip-substrate"] = {
 **strip("By the numbers · China lab-grown exports, H1 2026",[
   {"fig":"+65.3%","delta":"▲","dir":"up","lab":"exports, first half on first half"},
   {"fig":"¥1.41bn","lab":"about $210 million"},
   {"fig":"5×","lab":"thermal conductivity vs copper"},
   {"fig":"80%","lab":"of global output still to jewellery"},
   {"fig":"$703","delta":"▼ −$1","dir":"down","lab":"1ct lab-grown reference, this tape"}]),
 "figs":[bars("Plate I","Two customers, opposite signals · lab-grown, August 2026",[
   {"l":"CHINA INDUSTRIAL EXPORTS, H1","v":65,"d":"+65.3%","hi":True},
   {"l":"1CT JEWELLERY REFERENCE, DAY","v":-0.14,"d":"−0.14%"},
   {"l":"1CT JEWELLERY REFERENCE, VS 20 AUG","v":-0.28,"d":"−0.28%"}],
   "The export figure is a half-year total from Shanghai Customs; the reference prices are daily marks from this paper's own tape, read on CaratRadar. The two series are not on the same basis and are set side by side to show direction, not magnitude. Both markets are supplied by the same reactors.",237)],
 "flow":flow5("A 65.3% number from the wrong customer.","Why a chipmaker buys a diamond.","Two signals pulling opposite ways.",
   "Eighty per cent of global lab-grown production still goes to jewellery","The Diamonds Desk",
   "Ninety-six down, eighty up","a-ninety-six-down-eighty-up.html"),
 "desk":{"split":"the jewellery trade has been waiting for lab-grown prices to find a floor and has assumed the floor would come from demand"},
 "next":nxt("second-largest-and-no-price","Diamonds","The 2,488-carat Motswedi has sold, and Lucara published no figure.",
   "ninety-six-down-eighty-up","Diamonds","hundred-billion-on-two-point-four","Diamonds")}

specs["second-largest-and-no-price"] = {
 **strip("By the numbers · The Motswedi",[
   {"fig":"2,488 ct","lab":"after cleaning, from 2,492 reported"},
   {"fig":"2nd","lab":"largest diamond ever recovered"},
   {"fig":"$41.0m","delta":"▼ −6%","dir":"down","lab":"Lucara Q2 revenue, sale included"},
   {"fig":"$53m","lab":"Lesedi La Rona, 1,109 ct, 2017"},
   {"fig":"0","lab":"figures published for the sale"}]),
 "figs":[bars("Plate I","What is known and what is not · the Motswedi sale",[
   {"l":"LESEDI LA RONA, 1,109 CT, 2017","v":53.0,"d":"$53.0m, published"},
   {"l":"LUCARA Q2 2026 REVENUE, ALL SOURCES","v":41.0,"d":"$41.0m, sale inside it","hi":True},
   {"l":"LUCARA Q2 2025 REVENUE","v":43.7,"d":"$43.7m"},
   {"l":"THE MOTSWEDI ITSELF","v":0,"d":"not published"}],
   "The only quantitative bound the disclosure permits: the stone's proceeds sit inside a quarter that fell 6% year on year, so whatever it made did not lift the quarter above the prior year. The Lesedi La Rona bar is a 2017 transaction on a whiter stone and is shown as the comparison the market is left with, not as a valuation.",238)],
 "flow":flow5("A record stone, sold quietly.","What fills the space where a price should be.","The comparison set gets thinner.",
   "A stone that size has no comparables and now it has no price either","The Diamonds Desk",
   "Lucara's price a carat rose 24% as its prices fell","a-the-mix-did-the-work.html"),
 "desk":{"split":"an undisclosed price is a commercial right and it is also a transfer"},
 "next":nxt("eight-percent-deferred-to-march","Diamonds","Russia's rough duty moves to March and starts alongside the cluster decree.",
   "the-mix-did-the-work","Diamonds","lucara-tenth-thousand-carat","Diamonds")}

specs["eight-percent-deferred-to-march"] = {
 **strip("By the numbers · Russia's rough duty",[
   {"fig":"8%","lab":"export duty on rough leaving the EAEU"},
   {"fig":"1 Mar 2027","lab":"deferred from 1 September 2026"},
   {"fig":"$37.9m","lab":"₽3.12bn, estimated cost to Alrosa"},
   {"fig":"~90%","lab":"of Russian output is Alrosa's"},
   {"fig":"0.45 ct","lab":"the threshold, on both readings"}]),
 "figs":[bars("Plate I","Two readings of the same duty · what it covers",[
   {"l":"RAPAPORT / IDEX · FLOOR, NO CEILING","v":2,"d":"above 0.45 ct, incl. specials over 10.8 ct","hi":True},
   {"l":"TASS · A BAND","v":1,"d":"between 0.45 and 10.8 ct, plus specials"}],
   "Two outside sources describe the coverage differently and this desk cannot resolve which is right, so both are printed. The difference decides whether the largest Russian rough is taxed or exempt. The threshold at 0.45 carats is common to both readings and is the only part not in dispute.",239)],
 "flow":flow5("A six-month deferral, and why the new date.","What the duty covers, on two readings.","The bigger change is not the tax.",
   "The duty is the smaller change and the cluster decree is the larger","The Diamonds Desk",
   "Alrosa books a $134 million loss and starts idling the pits","a-alrosa-books-the-loss.html"),
 "desk":{"split":"sanctions were supposed to be the thing that separated Russian rough from the world market"},
 "next":nxt("one-january-and-two-million-customers","Retail","Jewelers Mutual changes chief executive on 1 January, four months pre-announced.",
   "alrosa-books-the-loss","Diamonds","fifty-nine-years-and-thirty-four-percent","Diamonds")}

specs["one-january-and-two-million-customers"] = {
 **strip("By the numbers · Jewelers Mutual",[
   {"fig":"1 Jan 2027","lab":"Alexander becomes president and CEO"},
   {"fig":"12","lab":"years of Murphy's tenure, from Jan 2015"},
   {"fig":"11","lab":"years Alexander has been inside"},
   {"fig":"2m+","lab":"customers, United States and Canada"},
   {"fig":"4","lab":"months of notice to the trade"}]),
 "figs":[bars("Plate I","A handover built for continuity · Jewelers Mutual",[
   {"l":"MURPHY, CEO SINCE JAN 2015","v":12,"d":"12 years, stays on the board"},
   {"l":"ALEXANDER, INSIDE SINCE 2015","v":11,"d":"11 years, president since 2025","hi":True},
   {"l":"NOTICE GIVEN TO THE TRADE","v":4,"d":"4 months"}],
   "Announced 18 August 2026 for a transition effective 1 January 2027. An internal president elevated while the retiring chief executive remains on the board is the standard shape of a handover designed to signal no change of direction. Murphy's tenure took the company from specialty insurer to a diversified insurance and non-insurance platform, including an entry into Australia via Jewellers Loop.",240)],
 "flow":flow5("The dates, and the overlap.","What is being handed over.","Why an insurance succession is a trade story.",
   "more than two million customers across the United States and Canada","The Retail & Technology Desk",
   "One fund cut 806,676 Signet shares. An index fund bought 665,182","a-eight-oh-six-out-six-sixty-five-in.html"),
 "desk":{"split":"this trade reads people moves as gossip and price moves as news"},
 "next":nxt("one-twelve-online-one-seventy-five-live","Auctions","Bonhams has 287 lots of jewellery open in Los Angeles inside eight days.",
   "eight-oh-six-out-six-sixty-five-in","Retail","zales-goes-to-mattel","Retail")}

specs["one-twelve-online-one-seventy-five-live"] = {
 **strip("By the numbers · Bonhams Los Angeles",[
   {"fig":"112","lab":"lots, Weekly: Jewelry, closes 25 Aug"},
   {"fig":"175","lab":"lots, live sale, 26 August"},
   {"fig":"287","lab":"lots in eight days, one city"},
   {"fig":"0","lab":"results published so far"},
   {"fig":"48","lab":"the lot count this paper's Bureau filed"}]),
 "figs":[bars("Plate I","Two Bonhams jewellery sales, Los Angeles · lots",[
   {"l":"MODERN NATIVE AMERICAN, LIVE 26 AUG","v":175,"d":"175 lots"},
   {"l":"WEEKLY: JEWELRY, ONLINE TO 25 AUG","v":112,"d":"112 lots","hi":True},
   {"l":"WEEKLY: JEWELRY, AS THE BUREAU FILED IT","v":48,"d":"48 lots, corrected"}],
   "Both live counts read from Bonhams' own Los Angeles listing on 21 August 2026. This paper's Bureau filed the weekly sale at 48 lots; the house says 112, and the house's figure is printed. The aggregator entry for this series currently resolves to a February 2025 edition of the same sale, which is why the house's own page was used.",241)],
 "flow":flow5("Two sales, 287 lots, eight days.","The weekly format nobody covers.","The volume end is the transparent end.",
   "Neither sale has a result yet and this is a calendar note","The Auctions Desk",
   "Two Sotheby's jewel sales closed. Neither has published a number","a-no-total-for-the-gem-drop.html"),
 "desk":{"split":"the auction jewellery market that gets written about is four trophy nights a year"},
 "next":nxt("a-third-door-for-lab-grown","Retail","A lab-grown-only brand opens its third store, in a Silicon Valley mall.",
   "no-total-for-the-gem-drop","Auctions","fifty-thousand-and-no-number","Auctions")}

specs["a-third-door-for-lab-grown"] = {
 **strip("By the numbers · Jean Dousset",[
   {"fig":"3","lab":"stores, after Los Angeles and New York"},
   {"fig":"13 Aug","lab":"Westfield Valley Fair opening"},
   {"fig":"2023","lab":"the year the brand went lab-grown only"},
   {"fig":"$703","lab":"1ct lab-grown reference, this tape"},
   {"fig":"n/d","lab":"price points, not disclosed"}]),
 "figs":[bars("Plate I","Three facts that describe one category · August 2026",[
   {"l":"CHINA INDUSTRIAL LGD EXPORTS, H1","v":65,"d":"+65.3%","hi":True},
   {"l":"JEAN DOUSSET STORE COUNT","v":3,"d":"3 doors"},
   {"l":"1CT LGD REFERENCE, DAY","v":-0.14,"d":"−0.14%"}],
   "Three series on three different bases, set together to describe a category rather than to be compared with one another: an input price that keeps easing, industrial demand climbing fast off a small base, and a retail end being built out by brands selling design rather than carat weight. Price points at Jean Dousset are not disclosed, which bounds what can be concluded.",242)],
 "flow":flow5("A third door, and where it is.","A surname doing commercial work.","What the address is arguing.",
   "Three doors is not a chain and the location is the argument","The Retail & Technology Desk",
   "China's lab-grown exports rise 65.3% on demand from chipmakers","a-sixty-five-percent-on-a-chip-substrate.html"),
 "desk":{"split":"the interesting number here is three, not the lineage"},
 "next":nxt("platinum-takes-the-biggest-move","Metals","Platinum adds 4.56% and takes the tape's biggest move from gold.",
   "sixty-five-percent-on-a-chip-substrate","Diamonds","ninety-six-down-eighty-up","Diamonds")}

editorial.update(specs)
(C/"editorial.json").write_text(json.dumps(editorial, indent=1, ensure_ascii=False))
print("editorial.json: %d specs added, %d total" % (len(specs), len(editorial)))
