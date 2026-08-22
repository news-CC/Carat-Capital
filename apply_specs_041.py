#!/usr/bin/env python3
# Edition No. 041 - editorial specs for the 6 articles.
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

specs["four-five-five-four-in-beijing"] = {
 **strip("By the numbers · The tape, Friday's last print",[
   {"fig":"$4,602.40","delta":"▲ +0.45%","dir":"up","lab":"gold, vs this paper's 21 Aug mark"},
   {"fig":"$68.86","delta":"▼ −0.65%","dir":"down","lab":"silver, the only metal lower"},
   {"fig":"$1,881.00","delta":"— unch.","dir":"flat","lab":"platinum, held on a 1.00% two-page gap"},
   {"fig":"$1,336.00","delta":"— unch.","dir":"flat","lab":"palladium, held on a 1.47% gap"},
   {"fig":"66.84","delta":"▲ +0.74","dir":"up","lab":"gold-to-silver ratio, derived"}]),
 "figs":[bars("Plate I","One session, four readings · spot gold, dollars an ounce, 21 August",[
   {"l":"TRADINGECONOMICS, CROSS-READ","v":4607.35,"d":"$4,607.35"},
   {"l":"KITCO, FRIDAY'S LAST PRINT","v":4602.40,"d":"$4,602.40","hi":True},
   {"l":"THIS PAPER'S 21 AUG MARK","v":4581.60,"d":"$4,581.60"},
   {"l":"EASTMONEY, 14:51 BEIJING","v":4554.44,"d":"$4,554.44"}],
   "The Beijing reading and the New York last print are the same session ten hours apart, not two sources disagreeing. The two outside pages that can be compared at the same hour, Kitco and TradingEconomics, are $4.95 or 0.11% apart on gold, inside the band this tape treats as agreement. The mark of record is Kitco's, re-read at press time on 22 August and unchanged, because Saturday has no session.",241)],
 "flow":flow5("A round number, broken twice.","What the Chinese counter did with it.","The Gulf leg, and what one rate looks like.",
   "Beijing's 14:51 is 02:51 in New York, roughly ten hours before Friday's last print","The Gold & Metals Desk",
   "938 at the exchange, 1,286 at the counter","a-nine-thirty-eight-and-twelve-eighty-six.html"),
 "desk":{"split":"The metal is being bought against a fiscal story rather than a jewellery one"},
 "next":nxt("four-point-one-six-billion-in-july","Metals","India's July imports more than doubled, and the window has closed.",
   "one-in-two-out-at-the-lbma","Metals","platinum-takes-the-biggest-move","Metals")}

specs["four-point-one-six-billion-in-july"] = {
 **strip("By the numbers · India, July 2026",[
   {"fig":"$4.16bn","delta":"▲ +111%","dir":"up","lab":"gold imports, on June's $1.97bn"},
   {"fig":"40–45t","lab":"estimated volume, against 20t in June"},
   {"fig":"14.9t","lab":"MCX average daily turnover"},
   {"fig":"−55%","delta":"▼","dir":"down","lab":"ETF net inflows, month on month"},
   {"fig":"120t","delta":"▲ +1t","dir":"up","lab":"Indian gold ETF holdings"}]),
 "figs":[bars("Plate I","Imports rebound while the investment leg halves · US$ billion",[
   {"l":"JULY IMPORTS","v":4.16,"d":"$4.16bn","hi":True},
   {"l":"JUNE IMPORTS","v":1.97,"d":"$1.97bn"},
   {"l":"JULY ETF NET INFLOW","v":0.163,"d":"$163m"},
   {"l":"1–14 AUGUST ETF NET INFLOW","v":0.124,"d":"$124m"}],
   "All four bars are converted to US dollars for comparison; the council publishes the ETF figures in rupees, at INR15.6bn and INR11.79bn. Imports and ETF flows are different series set on one scale to show relative size, not to be summed. The council states the July ETF figure was 55% lower month on month, citing AMFI data.",242)],
 "flow":flow5("A doubling, and the month it belongs to.","The leg that went the other way.","What to do with a backward-looking number.",
   "The window that produced those imports has already closed at a higher price","The Gold & Metals Desk",
   "India buys fifteen percent less gold","a-india-buys-fifteen-percent-less.html"),
 "desk":{"split":"The festival season will be bought at a level no part of this dataset covers"},
 "next":nxt("one-in-two-out-at-the-lbma","Metals","Three Good Delivery notices in seventeen days, all of them Chinese.",
   "four-five-five-four-in-beijing","Metals","india-buys-fifteen-percent-less","Metals")}

specs["one-in-two-out-at-the-lbma"] = {
 **strip("By the numbers · The Good Delivery Lists, August",[
   {"fig":"3","lab":"list changes in seventeen days"},
   {"fig":"3 of 3","lab":"are Chinese refiners"},
   {"fig":"67","lab":"accredited gold refiners, read 22 August"},
   {"fig":"86","lab":"accredited silver refiners, same read"},
   {"fig":"1997","lab":"Zhonghenglong's founding year"}]),
 "figs":[bars("Plate I","Three notices, seventeen days · day of August 2026",[
   {"l":"5 AUG · SHANDONG GOLD SUSPENDED, BOTH LISTS","v":5,"d":"UFLPA entity listing"},
   {"l":"17 AUG · ZHONGHENGLONG ADDED, GOLD LIST","v":17,"d":"accreditation granted","hi":True},
   {"l":"21 AUG · SKS SUSPENDED, SILVER LIST","v":21,"d":"modified assurance opinion"}],
   "Bars are plotted on the day of the month each action took effect, so the length shows sequence rather than magnitude. The Shandong suspension was an interim measure under the association's incident review process, with its investigation still to conclude. All three notices name Chinese refiners; no two share a cause.",243)],
 "flow":flow5("Three notices, two directions.","What the gate is actually worth.","Two failure modes, neither of them metal.",
   "Neither suspension alleges a bar that failed assay","The Gold & Metals Desk",
   "Forty-six percent came back","a-forty-six-percent-came-back.html"),
 "desk":{"split":"The transferable lesson is in the failure modes rather than the names"},
 "next":nxt("dvash-takes-the-odc-chair","Diamonds","Botswana's state rough trader fills a chair that was empty since November.",
   "four-point-one-six-billion-in-july","Metals","four-five-five-four-in-beijing","Metals")}

specs["dvash-takes-the-odc-chair"] = {
 **strip("By the numbers · Okavango Diamond Company",[
   {"fig":"30%","lab":"of Debswana output, years 1–5"},
   {"fig":"40%","lab":"of Debswana output, years 6–10"},
   {"fig":"Nov","lab":"when the previous chairman left, after five years"},
   {"fig":"2020","lab":"Dvash's first year as WFDB president"},
   {"fig":"0","lab":"figures published with the announcement"}]),
 "figs":[bars("Plate I","The share the seat governs · ODC's allocation of Debswana rough, %",[
   {"l":"YEARS 1–5 OF THE TERM","v":30,"d":"30%","hi":True},
   {"l":"YEARS 6–10 OF THE TERM","v":40,"d":"40%"},
   {"l":"FIVE-YEAR EXTENSION, IF TRIGGERED","v":50,"d":"50%"}],
   "Read from the ten-year sales agreement signed with De Beers in February 2025. The extension is conditional on criteria the parties have not published. The earlier agreement in principle, announced in July 2023, had projected ODC reaching 50% by the final year of the base term; the signed document does not.",244)],
 "flow":flow5("A chair filled after nine months.","The rough behind the seat.","What the announcement does not carry.",
   "What the appointment does not come with is a number","The Diamonds Desk",
   "Mehul Shah takes the gavel","a-mehul-shah-takes-the-gavel.html"),
 "desk":{"split":"Watch where the tenders go next"},
 "next":nxt("vasant-mehta-dies-at-81","Diamonds","A chairman who spent his later years on banking rather than the podium.",
   "dubai-diamond-week-returns","Diamonds","mehul-shah-takes-the-gavel","Diamonds")}

specs["vasant-mehta-dies-at-81"] = {
 **strip("By the numbers · Vasant Mehta, at 81",[
   {"fig":"81","lab":"years old, reported 18 August"},
   {"fig":"1991–92","lab":"first term as GJEPC vice chairman"},
   {"fig":"2006–08","lab":"second term as vice chairman"},
   {"fig":"2008–10","lab":"chairman, through the financial crisis"},
   {"fig":"5","lab":"international bodies he represented India at"}]),
 "flow":flow5("Four decades of seats.","Why the dates matter.","The committees, not the podium.",
   "Running the export council through those two years was a job about liquidity","The Diamonds Desk",
   "India ships the turn","a-india-ships-the-turn.html"),
 "desk":{"split":"That is the work the Indian industry has always been short of"},
 "next":nxt("fifty-three-percent-at-the-top","Retail","The fastest-growing American retailers are all value formats.",
   "dvash-takes-the-odc-chair","Diamonds","india-ships-the-turn","Diamonds")}

specs["fifty-three-percent-at-the-top"] = {
 **strip("By the numbers · NRF Hot 25, 2026",[
   {"fig":"53%","delta":"▲","dir":"up","lab":"Miniso US sales growth, first"},
   {"fig":"49%","delta":"▲","dir":"up","lab":"Dick's Sporting Goods, second"},
   {"fig":"26%","delta":"▲","dir":"up","lab":"Daiso Sangyo, third"},
   {"fig":"24%","delta":"▲","dir":"up","lab":"Primark, fourth"},
   {"fig":"23%","delta":"▲","dir":"up","lab":"Five Below, fifth"}]),
 "figs":[bars("Plate I","The top five, on domestic sales growth 2024 to 2025 · %",[
   {"l":"MINISO","v":53,"d":"53%","hi":True},
   {"l":"DICK'S SPORTING GOODS","v":49,"d":"49%"},
   {"l":"DAISO SANGYO","v":26,"d":"26%"},
   {"l":"PRIMARK","v":24,"d":"24%"},
   {"l":"FIVE BELOW","v":23,"d":"23%"}],
   "Compiled by Kantar for the National Retail Federation and published 21 August 2026. The metric is growth in domestic sales between 2024 and 2025, so the ranking measures momentum off each chain's own base rather than size. Dick's second place follows its acquisition of Foot Locker and is not organic. No jewellery specialist appears in the top five.",245)],
 "flow":flow5("A list with no jewellers on it.","What the top five have in common.","The limits of the ranking.",
   "None of these are jewellers and that is the reason to read it","The Retail & Technology Desk",
   "Zales says 67% of its core shoppers now buy for themselves","a-sixty-seven-percent-buy-it-for-themselves.html"),
 "desk":{"split":"The lesson is the entry price and the permission to browse, not the merchandise"},
 "next":nxt("four-five-five-four-in-beijing","Metals","Gold broke $4,550 in Beijing and kept going after China went home.",
   "sixty-seven-percent-buy-it-for-themselves","Retail","the-fifteen-hundred-line","Retail")}

editorial.update(specs)
(C/"editorial.json").write_text(json.dumps(editorial, indent=1, ensure_ascii=False))
print("editorial.json: %d specs written, %d total" % (len(specs), len(editorial)))
