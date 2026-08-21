#!/usr/bin/env python3
# Edition No. 040 - 2026-08-21. Wire tape + wire items + record entries.
import json, pathlib
C = pathlib.Path("content")
wire = json.loads((C/"wire.json").read_text())
record = json.loads((C/"record.json").read_text())

wire["date_line"] = "Friday, August 21, 2026"
wire["edition"] = "Vol. I — No. 040"
wire["tape_ts"] = ("21 Aug 2026, 5:59am New York · Kitco, corroborated on TradingEconomics · "
                   "Editor's press-time read; all four metals written back, platinum and palladium off a one-session hold")

TAPE = {
 "XAU": ("4,581.60", "▲ +2.22%", "up",   [24,26,24,22,26,25,23,22,26,28]),
 "XAG": ("69.31",    "▲ +4.08%", "up",   [22,23,25,22,23,26,25,19,26,28]),
 "XPT": ("1,881.00", "▲ +4.56%", "up",   [21,22,21,18,20,23,22,19,24,27]),
}
for t in wire["tape"]:
    if t["code"] in TAPE:
        px, chg, d, pts = TAPE[t["code"]]
        t["px"], t["chg"], t["dir"], t["pts"] = px, chg, d, pts
# NAT1 and LGD1 are locked by build.py to prices.json / lab-prices.json and are left alone.

wire["items"] = [
 {"b":"PLATINUM ADDS 4.56% AND TAKES THE TAPE'S BIGGEST MOVE FROM GOLD",
  "t":"Against this paper's 20 August marks of record, platinum is up $82.00 or 4.56% at $1,881.00, silver $2.72 or 4.08% at $69.31, gold $99.40 or 2.22% at $4,581.60 and palladium $28.00 or 2.14% at $1,336.00. Kitco at 05:59 New York, corroborated on TradingEconomics."},
 {"b":"BOTH BASES POINT THE SAME WAY THIS MORNING, WHICH THEY DID NOT YESTERDAY",
  "t":"Measured on Kitco's own session rather than against this paper's marks, all four metals are also higher: gold 1.40%, silver 1.99%, platinum 2.96%, palladium 1.75%. On 20 August the two bases pointed in opposite directions and both were printed."},
 {"b":"PLATINUM AND PALLADIUM COME OFF A ONE-SESSION HOLD FOR THE SECOND TIME IN THREE DAYS",
  "t":"The 04:58 tape correctly held both, because Kitco and TradingEconomics were 0.81% and 1.56% apart. At press time the held marks of $1,799.00 and $1,308.00 sat below every live reading, so both are written at Kitco's $1,881.00 and $1,336.00."},
 {"b":"THE TWO OUTSIDE SOURCES STILL DISAGREE ON THE WHITE METALS",
  "t":"Platinum's two pages are $13.40 apart, or 0.71%, and palladium's $21.50, or 1.61%, a fourth consecutive session above 1.4%. Gold and silver cleared cleanly at 0.017% and 0.17%. The gold-to-silver ratio reads 66.10 against 67.31, this desk's arithmetic."},
 {"b":"FINSCH WILL NOT REOPEN AFTER 59 YEARS, AND IT CARRIED 34% OF PETRA'S REVENUE",
  "t":"Creditors approved an asset sale on 7 August and the business rescue concluded no viable outcome exists to resume mining. More than 90% of Finsch's output was below two carats. Petra is now a one-mine company and is moving Cullinan up the carat scale."},
 {"b":"ZALES SAYS 67% OF PURCHASES AMONG ITS CORE SHOPPERS ARE SELF-PURCHASES",
  "t":"The Signet banner's You Are The Occasion campaign is built on the retailer's own finding. Two of its three style stories require no occasion at all, and the imagery includes men. It iterates on last year's Own It rather than opening new ground."},
 {"b":"CHINA'S LAB-GROWN EXPORTS ROSE 65.3% IN THE FIRST HALF, AND NOT FOR JEWELLERY",
  "t":"Shanghai Customs data puts them at 1.41 billion yuan, about $210 million, driven by heat spreaders and substrates for advanced semiconductors. Eighty per cent of global lab-grown output still goes to jewellery, where this tape's 1ct reference eased a dollar to $703."},
 {"b":"THE 2,488-CARAT MOTSWEDI HAS SOLD AND LUCARA PUBLISHED NO PRICE",
  "t":"Proceeds sit inside a second quarter that fell 6% to $41.0 million, which bounds the stone without pricing it. The comparison left standing is the 1,109-carat Lesedi La Rona at $53 million in 2017, a whiter stone in a different market."},
 {"b":"RUSSIA'S 8% ROUGH DUTY SLIPS TO 1 MARCH 2027 AND STARTS WITH THE CLUSTER DECREE",
  "t":"A resolution published on 11 August moved it from 1 September. Rapaport puts the cost to Alrosa at 3.12 billion roubles, about $37.9 million. Two outside sources describe the carat coverage differently and both readings are printed in full."},
 {"b":"BONHAMS HAS 287 LOTS OF JEWELLERY OPEN IN LOS ANGELES INSIDE EIGHT DAYS",
  "t":"Weekly: Jewelry closes 25 August with 112 lots and a live Native American sale follows on 26 August with 175. This paper's own Bureau filed the weekly at 48 lots; the house's listing says 112 and the house's figure is printed."},
]
(C/"wire.json").write_text(json.dumps(wire, indent=1, ensure_ascii=False))

ENTRIES = [
 {"d":"gold-metals",
  "h":"Platinum adds 4.56% to $1,881.00 and all four metals are written back at press time",
  "t":"The Editor re-read all four metals at 05:59 New York time on 21 August 2026 under the one-price rule. Kitco read gold $4,581.60 an ounce, silver $69.31, platinum $1,881.00 and palladium $1,336.00, and all four were written back to the tape of record before the edition built. Second page, TradingEconomics, the same morning: $4,582.37, a gap of $0.77 or 0.017%; $69.43, $0.12 or 0.17%; $1,894.40, $13.40 or 0.71%; $1,357.50, $21.50 or 1.61%. Against this paper's 20 August marks of record the moves are gold up $99.40 or 2.22%, silver up $2.72 or 4.08%, platinum up $82.00 or 4.56% and palladium up $28.00 or 2.14%. Measured on Kitco's own session all four are also higher, at 1.40%, 1.99%, 2.96% and 1.75%, so both bases point the same way, which they did not on 20 August. Platinum's $1,799.00 and palladium's $1,308.00 came off a one-session hold, not because the two pages agreed but because both held marks sat below every live reading taken this morning, which is the test applied on 19 August to marks sitting above the live range and on 20 August to marks sitting below it. This desk's arithmetic: the gold-to-silver ratio reads 66.10 against 67.31 on 20 August marks, 1.21 points narrower, with silver outrunning gold by 1.87 points of percentage; at 31.1035 grams to the troy ounce the four marks are $147.30, $2.23, $60.48 and $42.95 a gram, with gold's gram figure up $3.20 in a day; platinum has added close to nine per cent across two of this paper's sessions from the $1,726.00 mark of 19 August."},
 {"d":"diamonds",
  "h":"Finsch closes permanently after 59 years, having carried 34% of Petra's revenue",
  "t":"Business rescue practitioners put a plan to Finsch's creditors on 7 August 2026 and it passed with the required voting thresholds, concluding that no viable outcome exists to resume mining. The mine entered business rescue on 29 May 2026 and production was suspended in June, so the distance from rescue to closure was ten weeks. Finsch generated about 34% of Petra Diamonds' revenue in fiscal 2025 and began producing in 1967, making this the end of 59 years of commercial mining. More than 90% of its output was below two carats, the band in which lab-grown stones compete most directly and natural rough prices have fallen hardest; Petra's own account is that lower diamond prices and a stronger rand overwhelmed the mine's revenue despite strong operating performance. A secured creditor has provided post-commencement funding for limited on-site activity including asset reclamation, and proceeds will be distributed by ranking of claims with that creditor ranking highest. Petra is now a one-mine company and is moving Cullinan toward larger, higher-value stones. This paper reported the suspension on 29 July 2026 and had not previously carried the permanent closure; the report is eleven days old as printed and says so."},
 {"d":"retail-tech",
  "h":"Zales publishes a 67% self-purchase rate among its core shoppers",
  "t":"Zales, a Signet banner, announced a campaign called You Are The Occasion on 19 August 2026 built on its own finding that 67% of purchases among its core shoppers were made for themselves. The campaign is merchandised as three style stories: Everyday Elevated, covering tennis bracelets, rivière necklaces, ear stacks and solitaire pendants; Stacking and Layering, covering mix-and-match gold chains, bracelets, bands and pendants; and Bridal and Engagement, split into four aesthetics named Iconic Classic, Ethereal Romance, Grand Glamour and Modern Muse. Two of the three require no occasion at all. Campaign imagery includes men wearing watches, gold chains and other accessories, and the work runs in store and across digital and social channels. Amanda Rather, Zales' vice president of style and trend brand marketing, framed the intent as helping women make their own rules and celebrate themselves. The campaign iterates on the retailer's Own It campaign of last year rather than opening new ground, which this paper stated in print."},
 {"d":"diamonds",
  "h":"China's lab-grown diamond exports rose 65.3% in the first half on semiconductor demand",
  "t":"Shanghai Customs data reported through the Shanghai Diamond Exchange, China's sole general-trade diamond platform, puts first-half 2026 lab-grown diamond exports at 1.41 billion yuan, about $210 million, up 65.3%. This desk's arithmetic on the two published figures implies about 6.71 yuan to the dollar, offered as a check on the pair rather than as a currency quotation. The demand is industrial rather than ornamental: synthetic diamond is being bought as heat spreaders and substrates in advanced semiconductors, where its thermal conductivity is roughly five times that of copper, with Nvidia's February 2026 announcement that its next-generation graphics processors would use a diamond composite material with liquid cooling named as the catalyst. Approximately 80% of global lab-grown production still goes to jewellery. This paper's own tape carried the one-carat lab-grown reference at $703 on 21 August 2026, down a dollar on the day and down from $705 on 20 August, on CaratRadar. The two markets are supplied by the same reactors, which is the reason the paper ran the two facts together."},
 {"d":"diamonds",
  "h":"Lucara sells the 2,488-carat Motswedi and publishes no price",
  "t":"Lucara Diamond has sold the Motswedi, recovered at Karowe in Botswana in 2024 and the second-largest diamond ever found, at an undisclosed price, reported 11 August 2026. The stone weighed 2,488 carats after cleaning against the 2,492 carats first reported. Proceeds sit inside the company's second-quarter results rather than being disclosed separately; Lucara reported $41.0 million of second-quarter revenue, down 6% on $43.7 million a year earlier, which bounds the stone without pricing it. Chief executive William Lamb has said the Motswedi was not as white as the 1,109-carat Lesedi La Rona and contained inclusions reflecting brown tones. The Lesedi La Rona, also from Karowe, was bought by Graff for $53 million in 2017 and is the comparison the market is left with, nine years old and describing a whiter stone in a different market. This paper reported on 12 August 2026 that Lucara's price per carat rose 24% in the same period while diamond prices generally fell."},
 {"d":"diamonds",
  "h":"Russia defers its 8% rough export duty to 1 March 2027, to start with the cluster decree",
  "t":"A Russian government resolution published on 11 August 2026 moved the 8% export duty on rough and partially processed diamonds leaving the customs territory of the Eurasian Economic Union from 1 September 2026 to 1 March 2027, the date the country's cluster decree takes effect, so the two measures now begin together. Alrosa accounts for roughly 90% of Russia's domestic production. Rapaport reported on 11 August 2026 that the duty would have an impact of 3.12 billion roubles, about $37.9 million, on Alrosa's profit; that estimate was published while the duty was still due to start on 1 September, so it describes an annualised impact rather than a bill falling in this financial year. An outside-source divergence is printed in full rather than resolved: Rapaport and IDEX describe the duty as applying to rough above 0.45 carats including special-size goods over 10.8 carats, a floor with no ceiling, while TASS describes it as applying to rough between 0.45 and 10.8 carats plus special sizes, a band. The difference decides whether the largest Russian rough is taxed or exempt. The cluster decree replaces Russia's open rough sales model with a system in which miners must first offer goods to cutters inside the cluster before selling elsewhere."},
 {"d":"retail-tech",
  "h":"Jewelers Mutual names Mike Alexander chief executive from 1 January 2027",
  "t":"Jewelers Mutual announced on 18 August 2026 that chief executive Scott Murphy will retire at the end of 2026 after twelve years, having joined in January 2015, and will remain a member of the board. Mike Alexander, president since 2025 and an employee since 2015, becomes president and chief executive on 1 January 2027, giving the trade four months of notice. Murphy's tenure took the company from a specialty insurer to a diversified platform of insurance and non-insurance businesses built on technology and data analytics, serving more than two million customers across the United States and Canada, and into Australia through the acquisition of Jewellers Loop. Alexander's responsibilities have spanned digital transformation, product innovation and market and portfolio expansion, and he sits on the boards of Diamonds Do Good and the YMCA of the Fox Cities. Murphy said leading the company has been the greatest honour of his career."},
 {"d":"auctions",
  "h":"Bonhams opens 287 lots of jewellery in Los Angeles inside eight days",
  "t":"Bonhams' own Los Angeles listing, read 21 August 2026, shows Weekly: Jewelry running online from 18 to 25 August with 112 lots, and Modern Native American Art and Jewelry as a live sale on 26 August with 175 lots, 287 lots in total. Neither sale has a published result. A correction of this paper's own record is carried in the article: the Bureau filed the weekly sale at 48 lots and the house's listing says 112, so the house's figure was printed. The aggregator entry for this series resolves to a February 2025 edition of the same sale, which is why the house's own page was used to establish both counts and both dates. That February 2025 edition offered work by Paloma Picasso for Tiffany, Valentin Magro, Gübelin, Gucci and Ippolita in a band running from about $100 to $4,000, cited as a description of a prior edition rather than of the sale now open, because Bonhams has published no verifiable estimate range for the current one. A lot-level estimate reported elsewhere for a Jesse Monongya necklace could not be verified against the house's catalogue and was not printed. The 26 August date settles the question that caused this desk to kill an earlier version of the story on 17 August 2026."},
 {"d":"retail-tech",
  "h":"Jean Dousset opens a third lab-grown-only store, at Westfield Valley Fair",
  "t":"Jean Dousset opened its third store on 13 August 2026 at Westfield Valley Fair in Santa Clara, California, after a Los Angeles flagship and a New York showroom. The brand has sold lab-grown diamonds exclusively since 2023, across engagement rings, eternity bands, necklaces, bracelets, studs and hoops. The founder is the great-great-grandson of Cartier founder Louis-François Cartier. The boutique follows the brand's Dorée collection in its design, with elongated lines, structural forms and an open, gallery-like layout, and carries a screen beside the consultation desk showing views of the Eiffel Tower. Price points are not disclosed, which bounds what can be concluded. This paper ran the opening against two other figures from the same day's edition: the one-carat lab-grown reference on its tape at $703, down a dollar, and Chinese lab-grown exports to industrial buyers up 65.3% in the first half."},
]

wk = record["weeks"][0]
assert wk["label"] == "This week — August 17", wk["label"]
wk["entries"] = ENTRIES + wk["entries"]
record["updated"] = "21 Aug 2026"
(C/"record.json").write_text(json.dumps(record, indent=1, ensure_ascii=False))
print("wire.json: edition %s, %d items" % (wire["edition"], len(wire["items"])))
print("record.json: %d entries prepended, week now %d" % (len(ENTRIES), len(wk["entries"])))
