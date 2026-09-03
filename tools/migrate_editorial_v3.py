#!/usr/bin/env python3
"""Migrate every article's editorial spec from v2 (strip/plate/flow) to v3 (the Article Doctrine).

Run from the site folder:  python3 tools/migrate_editorial_v3.py [--dry-run] [--only slug,slug]

Nothing is deleted: the old v2 spec is kept under "v2" and articles.json is untouched. The renderer
(build.py article_page_v3) reads only the v3 keys. Overrides in content/v3-overrides.json win over
the automatic mapping for the slugs they name (used for the hand-built editions).
"""
import json, re, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
ARTS = json.loads((CONTENT / "articles.json").read_text())
ED = json.loads((CONTENT / "editorial.json").read_text())
PH = json.loads((ROOT / "assets" / "ph" / "manifest.json").read_text()) if (ROOT / "assets" / "ph" / "manifest.json").exists() else {}
OVR = json.loads((CONTENT / "v3-overrides.json").read_text()) if (CONTENT / "v3-overrides.json").exists() else {}
AM = {a["slug"]: a for a in ARTS}
TITLE_TO_SLUG = {a["title"].strip().lower(): a["slug"] for a in ARTS}

ABBR = ("no", "st", "mr", "mrs", "ms", "dr", "vs", "ref", "ct", "inc", "ltd", "co", "fig", "vol", "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec", "approx", "est", "ave")

def sentences(text):
    """Split prose into sentences without breaking decimals, abbreviations or initials."""
    text = re.sub(r"\s+", " ", text or "").strip()
    out, buf = [], ""
    i = 0
    while i < len(text):
        ch = text[i]; buf += ch
        if ch in ".!?" and i + 1 < len(text) and text[i + 1] == " ":
            nxt = text[i + 2:i + 3]
            last = re.findall(r"([A-Za-z]+)\.$", buf)
            if nxt and (nxt.isupper() or nxt in "\"'“(£$€" or nxt.isdigit()) and not (last and last[0].lower() in ABBR) and not re.search(r"\b[A-Z]\.$", buf):
                out.append(buf.strip()); buf = ""
                i += 1
        i += 1
    if buf.strip():
        out.append(buf.strip())
    return out

def words(s):
    return len(re.sub(r"<[^>]+>", " ", s or "").split())

def lead_split(par):
    """Bold lead-in rule: the first sentence if it is 12 words or fewer, else none."""
    ss = sentences(par)
    if not ss:
        return "", par
    if words(ss[0]) <= 12 and len(ss) > 1:
        return ss[0], " ".join(ss[1:])
    return "", par

def chunk(par, cap=55):
    """Split a paragraph at sentence boundaries into runs of at most `cap` words."""
    ss = sentences(par)
    out, cur = [], []
    for s in ss:
        if cur and words(" ".join(cur + [s])) > cap:
            out.append(" ".join(cur)); cur = [s]
        else:
            cur.append(s)
    if cur:
        out.append(" ".join(cur))
    return out or [par]

def para_obj(par):
    lead, text = lead_split(par)
    return {"lead": lead, "text": text}

SIGNED = re.compile(r"^\s*([+\-−])\s*([\d.,]+)\s*(%|pp|pts?|bps?)?\s*$")

def parse_signed(d):
    m = SIGNED.match((d or "").replace("▲", "+").replace("▼", "-"))
    if not m:
        return None
    v = float(m.group(2).replace(",", ""))
    return -v if m.group(1) in "-−" else v

def strip_cap(cap):
    cap = re.sub(r"^\s*(By the numbers|The numbers|Key figures)\s*[-–—·:]\s*", "", cap or "", flags=re.I)
    return cap.strip()

def migrate(a, e):
    body = list(a["body"])
    view = body[-1] if body and body[-1].startswith("The desk's view:") else ""
    view_txt = view[len("The desk's view:"):].strip() if view else ""
    if view_txt:
        view_txt = view_txt[0].upper() + view_txt[1:]
    corrections = [p for p in body[:-1] if re.match(r"\s*(Correction|CORRECTION|Corrected)\b", p)]

    # figures + hero
    cells, asof = [], ""
    if e.get("strip"):
        asof = strip_cap(e["strip"].get("cap", ""))
        for c in e["strip"]["cells"][:4]:
            cells.append({"n": c["fig"], "dir": c.get("dir") or ("up" if str(c["fig"]).startswith("+") else "dn" if str(c["fig"]).startswith(("−", "-")) else ""), "label": c.get("lab", ""), "q": ""})
    elif e.get("spec"):
        asof = strip_cap(e["spec"].get("cap", ""))
        for r in e["spec"]["rows"][:4]:
            v = re.sub(r"<[^>]+>", "", str(r.get("v", "")))
            cells.append({"n": v if len(v) <= 14 else v[:60], "dir": "", "label": r.get("l", ""), "q": ""})
    hero = {}
    fig0 = (e.get("figs") or [None])[0]
    if fig0 and "rows" in fig0 and 2 <= len(fig0["rows"]) <= 6:
        rows = fig0["rows"]
        sv = [parse_signed(r.get("d", "")) for r in rows]
        if all(v is not None for v in sv):
            hero["bars"] = [{"l": r["l"].title() if r["l"].isupper() else r["l"], "v": v, "d": r["d"], "hi": bool(r.get("hi"))} for r, v in zip(rows, sv)]
        elif all(isinstance(r.get("v"), (int, float)) for r in rows):
            hero["bars"] = [{"l": r["l"].title() if r["l"].isupper() else r["l"], "v": float(r["v"]), "d": r.get("d", ""), "hi": bool(r.get("hi"))} for r in rows]
        if hero.get("bars"):
            hero["bars_cap"] = fig0.get("title", "")
    if cells:
        hero.setdefault("n", cells[0]["n"]); hero.setdefault("what", cells[0]["label"]); hero.setdefault("since", "")
    if asof:
        hero["src"] = asof

    # what changed: the first paragraph's sentences to about 45 words (at least one, at most three)
    first = body[0] if body else ""
    ss = sentences(first)
    take, n = [], 0
    for s in ss[:3]:
        if take and n + words(s) > 55:
            break
        take.append(s); n += words(s)
        if n >= 45:
            break
    changed = para_obj(" ".join(take)) if take else {"lead": "", "text": first}
    rest_of_first = " ".join(ss[len(take):]) if take else ""

    # what it means: the desk's view, whole, in paragraphs of two sentences
    means = []
    vs = sentences(view_txt)
    for i in range(0, len(vs), 2):
        means.append({"who": "", "text": " ".join(vs[i:i + 2])})
    if means:
        lead, text = lead_split(means[0]["text"])
        if lead:
            means[0] = {"who": lead, "text": text}

    # sections from the flow
    flow = e.get("flow") or []
    secs, cur = [], None
    used = set()
    def add_par(par):
        for c in chunk(par):
            cur["p"].append(para_obj(c))
    for it in flow:
        if "sub" in it:
            cur = {"h": it["sub"].rstrip("."), "p": []}
            secs.append(cur)
        elif "p" in it:
            idx = it["p"]
            if idx >= len(body) - 1 or idx in used:
                continue
            used.add(idx)
            par = body[idx]
            if par in corrections:
                continue
            if idx == 0:
                if not rest_of_first:
                    continue
                par = rest_of_first
            if cur is None:
                cur = {"h": "The story", "p": []}; secs.append(cur)
            parts = [par]
            if it.get("split"):
                k = par.find(it["split"])
                if k > 0:
                    parts = [par[:k].rstrip(), par[k:]]
            for p in parts:
                add_par(p)
    # any body paragraph the flow never placed
    for idx in range(1, len(body) - 1):
        if idx not in used and body[idx] not in corrections:
            if cur is None:
                cur = {"h": "The story", "p": []}; secs.append(cur)
            add_par(body[idx])
    secs = [s for s in secs if s["p"]]

    # visual: the plate becomes a table (or keeps its svg)
    visual = None
    if fig0 and "svg" in fig0:
        visual = {"type": "svg", "cap": fig0.get("title", "Plate"), "asof": "", "svg": fig0["svg"], "note": fig0.get("cap", ""), "plate": "CC/%s" % a["date"][-5:]}
    elif fig0 and "rows" in fig0:
        rows = [[(r["l"].title() if r["l"].isupper() else r["l"]), r.get("d", "")] for r in fig0["rows"]]
        hi = next((i for i, r in enumerate(fig0["rows"]) if r.get("hi")), None)
        note = " ".join(x for x in [fig0.get("note", ""), fig0.get("cap", "")] if x)
        visual = {"type": "table", "cap": "Table I · %s" % fig0.get("title", ""), "asof": "", "cols": ["", "Figure"], "rows": rows, "hi": hi, "note": note, "plate": ""}

    # prior coverage: self-citations, the see-also link and the old minis
    prior, seen = [], set()
    def add_prior(slug, title="", date="", claim=""):
        if not slug or slug == a["slug"] or slug in seen or slug not in AM:
            return
        seen.add(slug)
        t = AM[slug]
        prior.append({"date": (date or t["date"]), "slug": slug, "title": title or t["title"], "claim": claim})
    for s in a.get("sources", []):
        if s.get("title", "").startswith("Carat Capital"):
            m = re.match(r"Carat Capital,\s*(.+?),\s*(\d{1,2} \w+ \d{4})\s*$", s["title"])
            t = (m.group(1) if m else s["title"].split(",", 1)[-1]).strip()
            slug = TITLE_TO_SLUG.get(t.lower()) or re.sub(r"^.*a-([^/]+?)(\.html)?$", r"\1", s.get("url", ""))
            add_prior(slug, t)
    for it in flow:
        if "also" in it:
            add_prior(re.sub(r"^a-|\.html$", "", it["also"].get("href", "")), it["also"].get("t", ""))
    for m in (e.get("next") or {}).get("minis", []):
        add_prior(m.get("slug"))
    for p in prior:
        p["date"] = p["date"]
    sources = []
    seen_u = set()
    for s in a.get("sources", []):
        if s.get("title", "").startswith("Carat Capital") or s.get("url", "") in seen_u:
            continue
        seen_u.add(s.get("url", ""))
        sources.append(s)

    method = ""
    if fig0 and fig0.get("note"):
        method = fig0["note"]
    nxt = (e.get("next") or {}).get("lead") or {}
    v3 = {
        "v": 3,
        "figures": {"asof": asof, "cells": cells},
        "hero": hero,
        "changed": changed,
        "means": means,
        "visual": visual,
        "sections": secs,
        "watch": [],
        "depth": {"reverse": "", "built": None, "method": method, "prior": prior, "sources": sources, "corrections": corrections},
        "next": {"slug": nxt.get("slug", ""), "why": nxt.get("blurb", "")},
        "migrated": "2026-09-03",
        "v2": e,
    }
    if a["slug"] in PH:
        v3["photo"] = None  # renderer picks the article's own photo from the manifest
    return v3

def main():
    dry = "--dry-run" in sys.argv
    only = None
    for i, x in enumerate(sys.argv):
        if x == "--only":
            only = set(sys.argv[i + 1].split(","))
    out, stats = {}, collections.Counter()
    for a in ARTS:
        e = ED.get(a["slug"])
        if only and a["slug"] not in only:
            out[a["slug"]] = e; continue
        if e is None:
            stats["no-spec"] += 1; continue
        if e.get("v") == 3 and a["slug"] not in OVR:
            out[a["slug"]] = e; stats["already"] += 1; continue
        base = e.get("v2", e) if e.get("v") == 3 else e
        v3 = migrate(a, base)
        if a["slug"] in OVR:
            o = OVR[a["slug"]]
            for k, v in o.items():
                v3[k] = v
            v3["v"] = 3; stats["override"] += 1
        out[a["slug"]] = v3
        stats["migrated"] += 1
        stats["sections:%d" % len(v3["sections"])] += 1
        if v3["hero"].get("bars"): stats["bars"] += 1
        if v3["visual"]: stats["visual"] += 1
        if v3["depth"]["corrections"]: stats["corrections"] += 1
        if v3["depth"]["prior"]: stats["prior"] += 1
    print(dict(stats))
    if dry:
        for slug in list(out)[:3]:
            print(json.dumps({k: v for k, v in out[slug].items() if k != "v2"}, indent=1, ensure_ascii=False)[:2500])
        return
    (CONTENT / "editorial.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print("wrote", CONTENT / "editorial.json", len(out), "specs")

if __name__ == "__main__":
    main()
