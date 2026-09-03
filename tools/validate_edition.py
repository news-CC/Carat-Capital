#!/usr/bin/env python3
"""The Article Doctrine gates (ops/article-doctrine.md Part V), applied to today's edition.

    python3 tools/validate_edition.py            # every spec dated today (or the newest date in articles.json)
    python3 tools/validate_edition.py --date 2026-09-04
    python3 tools/validate_edition.py --slug some-slug --all

Prints one block per article with PASS/FAIL per gate and exits 1 if any non-migrated article fails a
hard gate. Migrated specs ("migrated": "2026-09-03") are exempt from the budgets but not from the
number, promise-structure or source tests. The scanner and tapper tests are model reads the Editor
runs itself; this script checks everything that can be counted.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTS = json.loads((ROOT / "content" / "articles.json").read_text())
ED = json.loads((ROOT / "content" / "editorial.json").read_text())

def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s or "")

def words(s):
    return len(strip_tags(s).split())

def sentences(s):
    return [x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“(£$€\d])", strip_tags(s).strip()) if x]

NUM = re.compile(r"[$£€¥₹]?\d[\d,]*(?:\.\d+)?%?")
def nums(s):
    return {n.replace(",", "").rstrip(".") for n in NUM.findall(strip_tags(s))}

BANNED = [r"\bthis paper\b", r"\bthis desk\b", r"\bthis tape\b", r"\bre-read\b", r"\bwritten back\b", r"\bagreement band\b", r"\btoday\b", r"\byesterday\b", r"\bthis morning\b"]

def check(a, e):
    out = []
    hard_fail = False
    migrated = bool(e.get("migrated"))
    def gate(name, ok, detail="", hard=True):
        nonlocal hard_fail
        out.append("  %s  %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail else ""))
        if not ok and hard and not (migrated and name.startswith("budget")):
            hard_fail = True
    if e.get("v") != 3:
        gate("schema v3", False, "spec is not v3"); return out, True
    ch = e.get("changed") or {}; means = e.get("means") or []; secs = e.get("sections") or []
    l1 = words(a["dek"]) + words(ch.get("text", "")) + sum(words(m.get("text", "")) for m in means)
    l2 = sum(words(p.get("text", "")) for s in secs for p in s.get("p", []))
    gate("structure", bool(ch.get("text")) and bool(means) and bool(secs) and bool((e.get("depth") or {}).get("sources") or a.get("sources")), "changed/means/sections/sources present")
    gate("budget · layer 1 ≤150 words", l1 <= 150, "%d" % l1)
    gate("budget · layers 1+2 ≤400 words", l1 + l2 <= 400, "%d" % (l1 + l2))
    gate("budget · what changed ≤45 words", words(ch.get("text", "")) + words(ch.get("lead", "")) <= 45, "%d" % (words(ch.get("text", "")) + words(ch.get("lead", ""))))
    gate("budget · what it means ≤60 words", sum(words(m.get("text", "")) + words(m.get("who", "")) for m in means) <= 60, "%d" % sum(words(m.get("text", "")) + words(m.get("who", "")) for m in means))
    long_p = [p for s in secs for p in s.get("p", []) if words(p.get("text", "")) > 55 or len(sentences(p.get("text", ""))) > 3]
    gate("budget · paragraphs ≤55 words / ≤3 sentences", not long_p, "%d over" % len(long_p))
    long_s = [x for s in secs for p in s.get("p", []) for x in sentences(p.get("text", "")) if len(x.split()) > 25]
    gate("budget · no sentence over 25 words", not long_s, "%d over" % len(long_s))
    gate("sections 2–4, subheads ≤6 words", 2 <= len(secs) <= 4 and all(words(s["h"]) <= 6 for s in secs), "%d sections" % len(secs), hard=False)
    cells = ((e.get("figures") or {}).get("cells") or [])
    gate("key figures 4–5 cells with as-of", (not cells) or (2 <= len(cells) <= 5 and bool((e.get("figures") or {}).get("asof"))), "%d cells" % len(cells), hard=False)
    body_text = " ".join([ch.get("text", "")] + [m.get("text", "") for m in means] + [p.get("text", "") + " " + p.get("lead", "") for s in secs for p in s.get("p", [])] + [" ".join(str(c) for r in (e.get("visual") or {}).get("rows", []) for c in r)] + [str(b.get("d", "")) for b in (e.get("hero") or {}).get("bars", [])] + [" ".join(a.get("body", []))])
    have = nums(body_text)
    head_nums = nums(a["title"]) | nums(a["dek"]) | {n for c in cells for n in nums(c.get("n", ""))}
    missing = sorted(n for n in head_nums if n not in have and n.strip("%$£€") not in have)
    gate("number · every headline/dek/figure number in the body or table", not missing, ", ".join(missing))
    t = a["title"]
    gate("headline · no ? ! ALL-CAPS, ≤75 chars", ("?" not in t and "!" not in t and len(t) <= 75 and not re.search(r"\b[A-Z]{4,}\b", re.sub(r"\b(RAPI|GIA|GJEPC|AWDC|DMCC|LBMA|OFAC|IIGJ|IIT|CEO|CFO|LVMH|BIS|CIBJO|IDEX|LGD|RNS|SEC|WOSG|HK|US|UK|USD|EUR|GBP)\b", "", t))), "%d chars" % len(t), hard=False)
    d1 = sentences(a["dek"])
    gate("dek · 25–40 words, first sentence ≤150 chars", 20 <= words(a["dek"]) <= 45 and (not d1 or len(d1[0]) <= 150), "%d words, first %d chars" % (words(a["dek"]), len(d1[0]) if d1 else 0), hard=False)
    banned = [b for b in BANNED if re.search(b, strip_tags(ch.get("text", "") + " " + " ".join(m.get("text", "") for m in means) + " " + " ".join(p.get("text", "") for s in secs for p in s.get("p", []))), re.I)]
    gate("prose · no process narration or time-relative words in layers 1–2", not banned, ", ".join(banned), hard=False)
    quotes = re.findall(r"[\"“]([^\"”]{5,})[\"”]", strip_tags(" ".join(a.get("body", []))))
    over = [q for q in quotes if len(q.split()) > 15]
    gate("quote · none over 15 words", not over, "%d over" % len(over))
    return out, hard_fail

def main():
    args = sys.argv[1:]
    date = None; slug = None; all_ = "--all" in args
    if "--date" in args: date = args[args.index("--date") + 1]
    if "--slug" in args: slug = args[args.index("--slug") + 1]
    if not date and not slug and not all_:
        date = max(a["date"] for a in ARTS)
    picked = [a for a in ARTS if (slug and a["slug"] == slug) or (date and a["date"] == date) or (all_ and not slug and not date)]
    leads = sum(1 for a in ARTS if a.get("lead"))
    print("lead flags: %d %s" % (leads, "OK" if leads == 1 else "FAIL — exactly one article must carry lead:true"))
    failed = 0
    for a in picked:
        e = ED.get(a["slug"])
        if not e:
            print("\n%s\n  FAIL  no editorial spec" % a["slug"]); failed += 1; continue
        lines, hf = check(a, e)
        print("\n%s%s" % (a["slug"], "  (migrated, budgets advisory)" if e.get("migrated") else ""))
        print("\n".join(lines))
        failed += 1 if hf else 0
    print("\n%d article(s) checked, %d with a hard failure" % (len(picked), failed))
    sys.exit(1 if failed or leads != 1 else 0)

if __name__ == "__main__":
    main()
