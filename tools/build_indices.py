#!/usr/bin/env python3
"""The Carat indices — computed, never quoted from anyone else.

Fetches a year of daily closes for every constituent from Yahoo Finance's
public chart API, rebases each name to 100 at the first trading day of the
year in its own currency (price relatives are unitless, so the mix of USD,
EUR, CHF, HKD, INR, GBp, DKK, CAD and JPY cancels out), and averages them
equal-weight into five indices plus the derived spreads.

Writes content/indices.json. build.py reads that file and never touches the
network, so the CI build cannot silently print a stale or fabricated number:
if this script has not run, the page says so.

Dates and sessions (managing editor's order, 2026-11-09): every bar is dated in
its own exchange's local calendar, a bar whose session is still open at run time
is dropped, and the headline date is the latest date on which at least MIN_BARS of
the twenty constituents have a completed bar. A name with no completed bar on a
date is carried from its own last completed bar and listed in "carried". 1D, 1W
and 1M count those qualifying dates only, so a half-open Asian Monday can never
become a day of its own.

Run:  python3 tools/build_indices.py
"""
import json, time, datetime, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT  = ROOT / "content" / "indices.json"

BASE_YEAR = 2026            # rebased to 100 at the year's first trading day
MIN_BARS  = 18              # constituents (of 20) with a completed bar for a date to count

# ── the roster ───────────────────────────────────────────────────────────
# seg: M maisons · C the counter · P the pit · W the movement
# cc20 marks membership of the composite twenty.
ROSTER = [
 ("MC.PA",     "LVMH",                   "Paris",      "M", True),
 ("RMS.PA",    "Hermès",                 "Paris",      "M", True),
 ("KER.PA",    "Kering",                 "Paris",      "M", True),
 ("CFR.SW",    "Richemont",              "Zurich",     "M", True),
 ("UHR.SW",    "Swatch Group",           "Zurich",     "M", True),
 ("SIG",       "Signet Jewelers",        "New York",   "C", True),
 ("PNDORA.CO", "Pandora",                "Copenhagen", "C", True),
 ("1929.HK",   "Chow Tai Fook",          "Hong Kong",  "C", True),
 ("0590.HK",   "Luk Fook",               "Hong Kong",  "C", True),
 ("0116.HK",   "Chow Sang Sang",         "Hong Kong",  "C", True),
 ("TITAN.NS",  "Titan Company",          "Mumbai",     "C", True),
 ("WOSG.L",    "Watches of Switzerland", "London",     "C", True),
 ("BRLT",      "Brilliant Earth",        "New York",   "C", True),
 ("AAL.L",     "Anglo American",         "London",     "P", True),
 ("GEMD.L",    "Gem Diamonds",           "London",     "P", True),
 ("LUC.TO",    "Lucara Diamond",         "Toronto",    "P", True),
 ("7762.T",    "Citizen Watch",          "Tokyo",      "W", True),
 ("8050.T",    "Seiko Group",            "Tokyo",      "W", True),
 ("MOV",       "Movado Group",           "New York",   "W", True),
 ("6952.T",    "Casio",                  "Tokyo",      "W", True),
]
# the movement index also carries the three watch-heavy names from other rows
MOVEMENT_EXTRA = ["UHR.SW", "CFR.SW", "WOSG.L"]

GOLD = "XAUUSD=X"   # spot; falls back to GC=F (COMEX front month) if dark

INDICES = {
  "CC20": dict(name="The Jewelry Twenty",
               dek="twenty listed names, the whole trade in one line",
               members=lambda r: [t for t,_,_,_,cc in r if cc]),
  "CC-M": dict(name="The Maisons",
               dek="the luxury houses",
               members=lambda r: [t for t,_,_,s,_ in r if s=="M"]),
  "CC-C": dict(name="The Counter",
               dek="jewelry retail, five markets",
               members=lambda r: [t for t,_,_,s,_ in r if s=="C"]),
  "CC-P": dict(name="The Pit",
               dek="the miners left standing, and De Beers' parent",
               members=lambda r: [t for t,_,_,s,_ in r if s=="P"]),
  "CC-W": dict(name="The Movement",
               dek="the watchmakers, Swiss and Japanese",
               members=lambda r: [t for t,_,_,s,_ in r if s=="W"]+MOVEMENT_EXTRA),
}

def fetch(sym, tries=3):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1y"
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
            d = json.loads(urllib.request.urlopen(req, timeout=20).read())
            res = d["chart"]["result"][0]
            ts  = res["timestamp"]; cl = res["indicators"]["quote"][0]["close"]
            meta = res["meta"]; off = meta.get("gmtoffset", 0)
            local = lambda e: datetime.datetime.fromtimestamp(e+off, datetime.timezone.utc).date().isoformat()
            out = {}
            for t, c in zip(ts, cl):
                if c is None: continue
                out[local(t)] = float(c)
            # the newest bar is a live price while its session is open: drop it
            reg = (meta.get("currentTradingPeriod") or {}).get("regular") or {}
            dropped = None
            if out and reg.get("start") and reg["start"] <= time.time() < reg["end"] \
                    and max(out) == local(reg["start"]):
                dropped = max(out); del out[dropped]
            return out, meta.get("currency",""), dict(
                name=meta.get("longName") or meta.get("shortName",""), dropped=dropped)
        except Exception as e:
            if k == tries-1: raise
            time.sleep(2.0*(k+1))

def main():
    series, meta, open_dropped = {}, {}, {}
    for sym, name, ex, seg, cc in ROSTER:
        s, cur, info = fetch(sym)
        series[sym] = s
        meta[sym] = dict(name=name, ex=ex, seg=seg, cc20=cc, cur=cur)
        if info["dropped"]: open_dropped[sym] = info["dropped"]
        print(f"  {sym:10} {name:24} {len(s):3} closes  last completed {sorted(s)[-1]}"
              + (f"  (open bar {info['dropped']} dropped)" if info["dropped"] else ""))
        time.sleep(0.6)
    try:
        gold, gcur, _ = fetch(GOLD); gold_label = "gold spot (XAU/USD)"
    except Exception:
        gold, gcur, _ = fetch("GC=F"); gold_label = "gold, COMEX front month"
    print(f"  gold: {gold_label}, {len(gold)} closes")

    # master calendar: exchange-local dates on which MIN_BARS names have a completed bar
    nbars = {}
    for s in series.values():
        for d in s: nbars[d] = nbars.get(d, 0) + 1
    all_dates = sorted(nbars)
    base_day = next(d for d in all_dates if d >= f"{BASE_YEAR}-01-01" and nbars[d] > len(series)//2)
    cal = sorted({d for d, n in nbars.items() if n >= MIN_BARS} | {base_day})
    head = cal[-1]
    calset = set(cal)
    carried = [dict(sym=k, name=meta[k]["name"], last_bar=max(d for d in s if d <= head))
               for k, s in series.items() if head not in s]

    def ffill(s):
        # a name keeps its own last completed bar on dates where it has none
        out, last = {}, None
        for d in sorted(calset | set(s)):
            if d > head: break
            if d in s: last = s[d]
            if d in calset and last is not None: out[d] = last
        return out
    F = {k: ffill(s) for k, s in series.items()}
    FG = ffill(gold)

    def rebase(s):
        b = s.get(base_day)
        return {d: 100.0*v/b for d, v in s.items() if d >= base_day} if b else {}
    R  = {k: rebase(s) for k, s in F.items()}
    RG = rebase(FG)

    days = [d for d in cal if d >= base_day]
    def index_series(members):
        out = {}
        for d in days:
            vals = [R[m][d] for m in members if d in R[m]]
            if len(vals) >= max(3, int(0.7*len(members))):
                out[d] = sum(vals)/len(vals)
        return out

    def stats(s):
        ds = sorted(s)
        def back(n):
            i = max(0, len(ds)-1-n); return s[ds[i]]
        last = s[ds[-1]]
        peak = 0.0; mdd = 0.0; hi = -1e9
        for d in ds:
            hi = max(hi, s[d]); mdd = min(mdd, (s[d]-hi)/hi*100)
        return dict(level=round(last,2),
                    d1=round(last-back(1),2),   d1p=round((last/back(1)-1)*100,2),
                    w1p=round((last/back(5)-1)*100,2), m1p=round((last/back(21)-1)*100,2),
                    ytdp=round(last-100,2), hi=round(max(s.values()),2),
                    lo=round(min(s.values()),2), mddp=round(mdd,2))

    out_idx = {}
    for code, spec in INDICES.items():
        members = spec["members"](ROSTER)
        s = index_series(members)
        out_idx[code] = dict(name=spec["name"], dek=spec["dek"], members=members,
                             series=[[d, round(v,3)] for d, v in sorted(s.items())],
                             **stats(s))

    # constituent table with 50-day breadth
    cons = []
    for sym, m in meta.items():
        s = F[sym]; ds = sorted(s); last = s[ds[-1]]
        d50 = sum(s[d] for d in ds[-50:])/min(50, len(ds))
        r = R[sym]
        cons.append(dict(sym=sym, **m,
            last=round(last, 4 if last < 1 else 2),
            ytdp=round(r[sorted(r)[-1]]-100, 2) if r else None,
            m1p=round((last/s[ds[max(0,len(ds)-22)]]-1)*100, 2),
            above50=last > d50))
    breadth = round(100*sum(1 for c in cons if c["cc20"] and c["above50"]) /
                    sum(1 for c in cons if c["cc20"]))

    # gold overlay + the metal gap + 63-day correlation of daily returns
    gser = [[d, round(v,3)] for d, v in sorted(RG.items())]
    cc = dict(out_idx["CC20"]["series"])
    common = [d for d in sorted(RG) if d in cc][-64:]
    rc = [cc[common[i+1]]/cc[common[i]]-1 for i in range(len(common)-1)]
    rg = [RG[common[i+1]]/RG[common[i]]-1 for i in range(len(common)-1)]
    n = len(rc); mc, mg = sum(rc)/n, sum(rg)/n
    cov = sum((a-mc)*(b-mg) for a, b in zip(rc, rg))/n
    sc = (sum((a-mc)**2 for a in rc)/n)**.5; sg = (sum((b-mg)**2 for b in rg)/n)**.5
    corr = round(cov/(sc*sg), 2) if sc and sg else None

    OUT.write_text(json.dumps(dict(
        as_of=head,
        rule=f"headline date = latest exchange-local date with at least {MIN_BARS} of {len(series)} completed bars; open sessions dropped",
        carried=carried, open_bars_dropped=open_dropped,
        built=datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        base_day=base_day, base_note=f"100 = first trading day of {BASE_YEAR} ({base_day})",
        source="exchange closes via Yahoo Finance chart API, each stock in its home currency",
        gold=dict(label=gold_label, series=gser,
                  ytdp=round(RG[sorted(RG)[-1]]-100, 2)),
        metal_gap=round(RG[sorted(RG)[-1]] - out_idx["CC20"]["level"], 2),
        corr63=corr, breadth50=breadth,
        indices=out_idx, constituents=cons), separators=(",", ":")))
    print(f"\nwrote {OUT}  as of {head}  ({nbars.get(head,0)} of {len(series)} names have a bar on it)")
    print(f"  carried on {head}: " + (", ".join(f"{c['sym']} (last bar {c['last_bar']})" for c in carried) or "none"))
    print(f"  open bars dropped: " + (", ".join(f"{k} {v}" for k, v in open_dropped.items()) or "none"))
    for code, x in out_idx.items():
        print(f"  {code:5} {x['level']:8.2f}  ytd {x['ytdp']:+6.2f}%  1d {x['d1p']:+5.2f}%")
    print(f"  gold ytd {round(RG[sorted(RG)[-1]]-100,2):+.2f}%  metal gap {round(RG[sorted(RG)[-1]]-out_idx['CC20']['level'],2):+.2f}pts  corr63 {corr}  breadth {breadth}%")

if __name__ == "__main__":
    main()
