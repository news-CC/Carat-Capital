#!/usr/bin/env python3
# Edition No. 048 - editorial.json entries (strip, flow, plates, desk split, next).
import json, pathlib
C = pathlib.Path("content")
ed = json.loads((C/"editorial.json").read_text())

ed["minus-one-fifty-on-gold"] = {
 "strip": {
  "cap": "By the numbers - Friday's close, against Thursday's mark of record",
  "cells": [
   {"fig":"$4,454.40","delta":"▼ −3.26%","dir":"down","lab":"gold the ounce, off $150.10"},
   {"fig":"$66.253","delta":"▼ −5.85%","dir":"down","lab":"silver the ounce, off $4.117"},
   {"fig":"$1,819.00","delta":"▼ −3.40%","dir":"down","lab":"platinum, off $64.00"},
   {"fig":"$1,405.00","delta":"▲ +1.74%","dir":"up","lab":"palladium, the only riser"},
   {"fig":"23","lab":"sessions on this tape; both falls are the worst"}
  ]
 },
 "flow": [
  {"sub":"Four marks read again this morning, and none of them moved.","n":"§1"},
  {"p":0},
  {"sub":"Worst on the record, and not close.","n":"§2"},
  {"p":1},
  {"fig":0},
  {"sub":"Named in Wyoming, priced in New York.","n":"§3"},
  {"p":2,"split":"The market read a rate rise"},
  {"pull":{"q":"Otherwise, we have work to do.","attr":"Kevin Warsh, Federal Reserve chair, at Jackson Hole"}},
  {"sub":"The width of the day, and one outside disagreement.","n":"§4"},
  {"p":3}
 ],
 "desk": {"split":"The gold-to-silver ratio moved"},
 "next": {
  "lead": {"slug":"one-more-year-for-the-grandfathered","tag":"Diamonds",
           "blurb":"OFAC buys a closed and ageing population of Russian stones another 365 days."},
  "minis": [{"slug":"a-fourth-source-for-paraiba","tag":"Gemstones"},
            {"slug":"one-thirty-nine-on-seventeen","tag":"Retail & Tech"}]
 },
 "figs": [
  {"no":"Plate I","title":"One-day falls on this tape, 5-29 August",
   "rows":[
    {"l":"SILVER, 29 AUG","v":585,"d":"−5.85%","hi":True},
    {"l":"PLATINUM, 29 AUG","v":340,"d":"−3.40%"},
    {"l":"GOLD, 29 AUG","v":326,"d":"−3.26%","hi":True},
    {"l":"SILVER, 19 AUG","v":289,"d":"−2.89%"},
    {"l":"GOLD, 27 AUG","v":93,"d":"−0.93%"}
   ],
   "note":"Twenty-three sessions of this paper's own marks of record. Nothing else comes close",
   "cap":"Bars scaled to the largest fall. Carat Capital graphics desk. &nbsp;CC/2026/048"}
 ]
}

ed["one-more-year-for-the-grandfathered"] = {
 "strip": {
  "cap": "By the numbers - General License No. 104B, issued 27 August",
  "cells": [
   {"fig":"1 Sep 2027","lab":"the new deadline, from 1 September 2026"},
   {"fig":"365","lab":"days added to the window"},
   {"fig":"1,279","lab":"days a 1ct stone will have been out of Russia"},
   {"fig":"1,095","lab":"days for a half-carat stone, to the day"},
   {"fig":"0","lab":"carats published, of what is still waiting"}
  ]
 },
 "flow": [
  {"sub":"A deadline moved, and a licence numbered twice over.","n":"§1"},
  {"p":0},
  {"sub":"What three and a half years of shelf life means.","n":"§2"},
  {"p":1},
  {"fig":0},
  {"pull":{"q":"Three and a half years, and the parcels still cannot land.","attr":"The Diamonds Desk"}},
  {"sub":"Nobody has published the size of it.","n":"§3"},
  {"p":2},
  {"sub":"Documented goods cost money to keep documented.","n":"§4"},
  {"p":3}
 ],
 "desk": {"split":"A dealer looking at this notice"},
 "next": {
  "lead": {"slug":"minus-one-fifty-on-gold","tag":"Gold & Metals",
           "blurb":"Gold off $150.10 and silver off 5.85%, the worst session this paper's tape has carried."},
  "minis": [{"slug":"a-fourth-source-for-paraiba","tag":"Gemstones"},
            {"slug":"one-number-in-three-cities","tag":"Retail & Tech"}]
 },
 "figs": [
  {"no":"Plate I","title":"How long the grandfathered goods will have sat",
   "rows":[
    {"l":"1CT AND ABOVE","v":1279,"d":"1,279 days out of Russia","hi":True},
    {"l":"0.50 TO 1.00CT","v":1095,"d":"1,095 days"},
    {"l":"THIS EXTENSION","v":365,"d":"365 days added"},
    {"l":"CARATS PUBLISHED","v":10,"d":"none"}
   ],
   "note":"Measured from each cutoff to 1 September 2027. Carat weight of the population is unpublished",
   "cap":"Bars scaled to the longest wait. Carat Capital graphics desk. &nbsp;CC/2026/048"}
 ]
}

ed["a-fourth-source-for-paraiba"] = {
 "strip": {
  "cap": "By the numbers - GIA and Gübelin, joint statement of 27 August",
  "cells": [
   {"fig":"4","lab":"producing sources, from three"},
   {"fig":"100+","lab":"rough and faceted stones in GIA's parcel"},
   {"fig":"3","lab":"markers named: vanadium, lead, gallium"},
   {"fig":"0","lab":"ppm thresholds published so far"},
   {"fig":"$10-12k","lab":"a carat, Mozambican material, from $7,000"}
  ]
 },
 "flow": [
  {"sub":"Two laboratories, separate samples, one answer.","n":"§1"},
  {"p":0},
  {"sub":"In June the same material could not be told from Brazil.","n":"§2"},
  {"p":1},
  {"fig":0},
  {"pull":{"q":"In May the same material could not be told from Brazil.","attr":"The Gemstones Desk"}},
  {"sub":"Origin is most of the price, and nobody has one yet.","n":"§3"},
  {"p":2},
  {"sub":"The report, not the mine, is where this lands.","n":"§4"},
  {"p":3}
 ],
 "desk": {"split":"For a dealer the near-term instruction"},
 "next": {
  "lead": {"slug":"minus-one-fifty-on-gold","tag":"Gold & Metals",
           "blurb":"Gold off $150.10 and silver off 5.85%, the worst session this paper's tape has carried."},
  "minis": [{"slug":"one-more-year-for-the-grandfathered","tag":"Diamonds"},
            {"slug":"one-thirty-nine-on-seventeen","tag":"Retail & Tech"}]
 },
 "figs": [
  {"no":"Plate I","title":"Three months from first look to confirmed source",
   "rows":[
    {"l":"GÜBELIN FIRST SEES IT","v":1,"d":"early May 2026"},
    {"l":"SSEF: INCONCLUSIVE","v":2,"d":"June 2026"},
    {"l":"GIA BEGINS STUDY","v":2,"d":"June 2026"},
    {"l":"JOINT CONFIRMATION","v":4,"d":"27 August 2026","hi":True}
   ],
   "note":"Bars mark sequence, not duration. Full findings are going to Gems & Gemology",
   "cap":"Carat Capital graphics desk, from both laboratories' statements. &nbsp;CC/2026/048"}
 ]
}

ed["one-thirty-nine-on-seventeen"] = {
 "strip": {
  "cap": "By the numbers - Chow Sang Sang, six months to 30 June 2026",
  "cells": [
   {"fig":"HK$12.88bn","delta":"▲ +17%","dir":"up","lab":"revenue, about $1.64 billion"},
   {"fig":"HK$2.15bn","delta":"▲ +139%","dir":"up","lab":"profit, about $274.6 million"},
   {"fig":"16.69%","lab":"net margin, against about 8.17%"},
   {"fig":"+38%","lab":"same-store, Hong Kong and Macau"},
   {"fig":"47","lab":"shops closed on a net basis"}
  ]
 },
 "flow": [
  {"sub":"The half, as the company files it.","n":"§1"},
  {"p":0},
  {"sub":"The margin did the work, not the sales.","n":"§2"},
  {"p":1},
  {"fig":0},
  {"pull":{"q":"key collections, including Cultural Blessings and Noir, recorded strong growth","attr":"Chow Sang Sang, in its results statement"}},
  {"sub":"Two markets crossing inside one half.","n":"§3"},
  {"p":2},
  {"sub":"Forty-seven, or forty-nine.","n":"§4"},
  {"p":3}
 ],
 "desk": {"split":"The durable number in the release"},
 "next": {
  "lead": {"slug":"minus-one-fifty-on-gold","tag":"Gold & Metals",
           "blurb":"The metal that doubled this margin fell 3.26% in a single session on Friday."},
  "minis": [{"slug":"one-number-in-three-cities","tag":"Retail & Tech"},
            {"slug":"one-more-year-for-the-grandfathered","tag":"Diamonds"}]
 },
 "figs": [
  {"no":"Plate I","title":"Same-store growth, quarter by quarter",
   "rows":[
    {"l":"HK & MACAU, Q1","v":46,"d":"+46%"},
    {"l":"HK & MACAU, Q2","v":30,"d":"+30%","hi":True},
    {"l":"MAINLAND, Q1","v":7,"d":"+7%"},
    {"l":"MAINLAND, Q2","v":17,"d":"+17%","hi":True}
   ],
   "note":"The home market decelerating, the mainland accelerating, inside one six-month period",
   "cap":"Company figures as reported. Carat Capital graphics desk. &nbsp;CC/2026/048"}
 ]
}

ed["one-number-in-three-cities"] = {
 "strip": {
  "cap": "By the numbers - the Gujarat board, 27 August, per 10 grams",
  "cells": [
   {"fig":"₹1,63,790","lab":"24-carat, identical in all three cities"},
   {"fig":"₹1,50,140","lab":"22-carat, which is 24-carat × 22/24"},
   {"fig":"₹1,22,840","lab":"18-carat, which is 24-carat × 18/24"},
   {"fig":"₹17,850","delta":"▲ +12.23%","dir":"up","lab":"added since 27 July"},
   {"fig":"91.667%","lab":"the ratio that gives the trick away"}
  ]
 },
 "flow": [
  {"sub":"One page, three cities, one number.","n":"§1"},
  {"p":0},
  {"sub":"Two of the three karats are division, not quotation.","n":"§2"},
  {"p":1},
  {"fig":0},
  {"pull":{"q":"Two of the three karat prices are not prices. They are division.","attr":"The Retail Desk"}},
  {"sub":"Separate markets, identical to the rupee.","n":"§3"},
  {"p":2},
  {"sub":"The trend is honest, and the date now matters.","n":"§4"},
  {"p":3}
 ],
 "desk": {"split":"None of this makes the board useless"},
 "next": {
  "lead": {"slug":"minus-one-fifty-on-gold","tag":"Gold & Metals",
           "blurb":"Gold fell 3.26% on Friday, after this board was printed and before anyone read it."},
  "minis": [{"slug":"one-thirty-nine-on-seventeen","tag":"Retail & Tech"},
            {"slug":"a-fourth-source-for-paraiba","tag":"Gemstones"}]
 },
 "figs": [
  {"no":"Plate I","title":"What the board prints, and what the arithmetic gives",
   "rows":[
    {"l":"24-CARAT, PRINTED","v":163790,"d":"₹1,63,790"},
    {"l":"22-CARAT, PRINTED","v":150140,"d":"₹1,50,140"},
    {"l":"24CT × 22/24","v":150141,"d":"₹1,50,140.83","hi":True},
    {"l":"18-CARAT, PRINTED","v":122840,"d":"₹1,22,840"},
    {"l":"24CT × 18/24","v":122843,"d":"₹1,22,842.50","hi":True}
   ],
   "note":"Per 10 grams, 27 August 2026. Pure karat ratio, rounded to the nearest ten rupees",
   "cap":"Carat Capital graphics desk, arithmetic on the board's own figures. &nbsp;CC/2026/048"}
 ]
}

(C/"editorial.json").write_text(json.dumps(ed, indent=1, ensure_ascii=False))
print("editorial entries", len(ed))
