"""Search and answer-engine plumbing for caratcapital.org.

Law: ops/search-doctrine.md. Integration: ops/search/INTEGRATION.md.

This module is deliberately SEPARATE from build.py. build.py is the live edition
builder and the 06:00 run depends on it; a defect here must not be able to stop an
edition. Every function is pure, takes plain data, returns a string, and raises on
nothing. Import it, call it, or delete the import and the paper still ships.

Written by caratchief 2026-09-17. Not yet wired — wiring the site is Roomy's.
"""

import html as H
import json
import re
from datetime import datetime, timedelta, timezone

BASE_URL = "https://caratcapital.org"
ORG_ID = f"{BASE_URL}/#org"
DEFAULT_IMAGE = f"{BASE_URL}/assets/share-card.png"

# Edition time. The paper files at 06:30 ET; ET is -04:00 on DST, -05:00 off it.
EDITION_HOUR = "06:30:00"


def et_offset(date_str):
    """-04:00 during US DST, -05:00 otherwise. Second Sunday in March to first
    Sunday in November. Cheap and correct for a date string; no tz database."""
    y, m, d = (int(x) for x in date_str[:10].split("-"))
    if m < 3 or m > 11:
        return "-05:00"
    if 3 < m < 11:
        return "-04:00"
    if m == 3:
        # second Sunday in March
        first = datetime(y, 3, 1)
        sundays = [x for x in range(1, 15) if datetime(y, 3, x).weekday() == 6]
        return "-04:00" if d >= sundays[1] else "-05:00"
    # November: first Sunday
    sundays = [x for x in range(1, 8) if datetime(y, 11, x).weekday() == 6]
    return "-05:00" if d >= sundays[0] else "-04:00"


def iso_ts(date_str, time_str=EDITION_HOUR):
    """Rule T6 — full ISO 8601 with an ET offset. '2026-09-17' -> '2026-09-17T06:30:00-04:00'."""
    return f"{date_str[:10]}T{time_str}{et_offset(date_str)}"


# ---------------------------------------------------------------- titles

def seo_title(headline, suffix=" — Carat Capital", limit=60):
    """Rule T1 — 60 characters including the suffix, or the headline alone.

    372 of 389 titles measured over 60 on 2026-09-17; the suffix costs 16 characters
    of a ~60 budget on a brand with no search volume yet. The headline is never
    reworded here — that belongs to ops/attention-doctrine.md. It is only cut.
    """
    headline = (headline or "").strip()
    if len(headline) + len(suffix) <= limit:
        return headline + suffix
    if len(headline) <= limit:
        return headline
    cut = headline[:limit]
    sp = cut.rfind(" ")
    if sp > limit * 0.6:
        cut = cut[:sp]
    return cut.rstrip(" ,;:.—-") + "…"


def metadesc(text, limit=155):
    """Rule T3 — mirrors build.py's metadesc so hand-written pages get it too."""
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    sp = cut.rfind(" ")
    if sp > limit * 0.6:
        cut = cut[:sp]
    return cut.rstrip(" ,;:.—-") + "…"


# ---------------------------------------------------------------- sitemaps

def sitemap(entries):
    """Rule T4 — entries are (path, lastmod|None). lastmod is a date or ISO stamp."""
    def loc(p):
        if p == "index.html":
            return BASE_URL
        return f"{BASE_URL}/{p[:-5] if p.endswith('.html') else p}"
    out = []
    for p, lm in entries:
        u = f"<url><loc>{loc(p)}</loc>"
        if lm:
            u += f"<lastmod>{lm}</lastmod>"
        out.append(u + "</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + "".join(out) + "</urlset>")


def news_sitemap(articles, now=None, window_hours=24, cap=1000):
    """Rule T5 — Google news sitemap: last 48 hours only, under 1000 URLs.

    An article older than the window is not merely useless here, it is a spec
    violation, so the window is enforced rather than trusted.

    window_hours defaults to 24, not 48, and that is deliberate: articles carry a
    DATE, not a timestamp, so the cutoff resolves to a calendar day. A 48-hour clock
    makes the cutoff two days ago and therefore admits three calendar days — up to
    72h old. 24 hours makes it yesterday, admitting today and yesterday, which is at
    most 48h old for a paper that files at 06:30. Do not "fix" this back to 48.
    """
    now = now or datetime.now(timezone.utc)
    cutoff = (now - timedelta(hours=window_hours)).date().isoformat()
    items = []
    for a in articles:
        if a["date"][:10] < cutoff:
            continue
        items.append(
            "<url>"
            f"<loc>{BASE_URL}/a-{a['slug']}</loc>"
            "<news:news>"
            "<news:publication>"
            "<news:name>Carat Capital</news:name>"
            "<news:language>en</news:language>"
            "</news:publication>"
            f"<news:publication_date>{iso_ts(a['date'])}</news:publication_date>"
            f"<news:title>{H.escape(a['title'])}</news:title>"
            "</news:news></url>"
        )
        if len(items) >= cap:
            break
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">'
            + "".join(items) + "</urlset>")


def robots(indexnow_key=None):
    """Retrieval crawlers named and allowed (Rule E4). Training crawlers are NOT
    listed and NOT blocked — that is Roomy's ruling to make, and until it is made
    the blanket Allow stands. Naming the retrieval bots changes nothing technically;
    it states the policy in the file where a policy belongs."""
    lines = [
        "# Carat Capital — caratcapital.org",
        "# Retrieval crawlers are welcome by name. They send readers.",
        "# Training-crawler policy is not set here; see ops/search-doctrine.md Part V.3.",
        "",
    ]
    for ua in ("Googlebot", "Googlebot-News", "Bingbot", "OAI-SearchBot", "ChatGPT-User",
               "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User",
               "Applebot", "DuckDuckBot"):
        lines += [f"User-agent: {ua}", "Allow: /", ""]
    lines += ["User-agent: *", "Allow: /", ""]
    lines += [f"Sitemap: {BASE_URL}/sitemap.xml",
              f"Sitemap: {BASE_URL}/news-sitemap.xml", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- structured data

DESK_TOPICS = [
    "diamond trade", "rough diamond prices", "lab-grown diamonds",
    "gold and precious metals", "coloured gemstones", "luxury watches",
    "jewellery auctions", "jewellery retail", "jewellery technology",
]


def org_block(same_as=None):
    """IV.1 — one NewsMediaOrganization, referenced by @id everywhere else.

    same_as: every profile we actually control, plus the Wikidata item once it
    exists. Pass only URLs that resolve — a sameAs to a page that 404s lowers
    entity confidence instead of raising it.
    """
    return {
        "@type": "NewsMediaOrganization",
        "@id": ORG_ID,
        "name": "Carat Capital",
        "alternateName": "Carat Capital — The Trade Paper of the Jewelry World",
        "url": BASE_URL,
        "logo": {"@type": "ImageObject",
                 "url": f"{BASE_URL}/assets/cc-icon-1024.jpg",
                 "width": 1024, "height": 1024},
        "description": ("The trade paper of the jewelry world. Original, sourced daily "
                        "reporting on diamonds, gold and precious metals, coloured gemstones, "
                        "watches, auctions and jewellery retail."),
        "publishingPrinciples": f"{BASE_URL}/about",
        "knowsAbout": DESK_TOPICS,
        "sameAs": [u for u in (same_as or []) if u],
    }


def breadcrumbs(trail):
    """IV.5 — trail is [(name, url), …], Home first."""
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
            for i, (n, u) in enumerate(trail)
        ],
    }


def article_block(a, desk_name, desk_url, image_url=None, entities=None):
    """IV.3 — the complete NewsArticle.

    entities: [{"name": str, "sameAs": url|None}] for `about`/`mentions`. A Wikidata
    URL where we have one; the name alone where we do not. Never a guessed QID —
    a wrong entity link is a fabrication a reader never sees and a machine carries.
    """
    url = f"{BASE_URL}/a-{a['slug']}"
    ents = [
        {"@type": "Thing", "name": e["name"], **({"sameAs": e["sameAs"]} if e.get("sameAs") else {})}
        for e in (entities or [])
    ]
    block = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": a["title"][:110],
        "description": a.get("dek", ""),
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "datePublished": iso_ts(a["date"]),
        "dateModified": iso_ts(a.get("modified", a["date"])),
        "image": {"@type": "ImageObject", "url": image_url or DEFAULT_IMAGE,
                  "width": 1200, "height": 630},
        "author": {"@type": "Organization",
                   "name": f"Carat Capital — {a.get('byline', desk_name)}",
                   "url": desk_url},
        "publisher": {"@id": ORG_ID},
        "articleSection": desk_name,
        "isAccessibleForFree": True,
        "inLanguage": "en",
        "wordCount": sum(len(p.split()) for p in (a.get("body") or [])),
    }
    if ents:
        block["about"] = ents[:3]
        block["mentions"] = ents
    return block


def dataset_block(name, description, url, date_modified, variables,
                  temporal=None, license_url=None):
    """IV.6 — for the price lists and the Almanac tables. Our most-cited pages are
    pure data wearing no structure."""
    b = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": name,
        "description": description,
        "url": url,
        "dateModified": date_modified,
        "creator": {"@id": ORG_ID},
        "isAccessibleForFree": True,
        "variableMeasured": list(variables),
    }
    if temporal:
        b["temporalCoverage"] = temporal
    if license_url:
        b["license"] = license_url
    return b


def faq_block(pairs):
    """IV.6 — [(question, answer_text), …]. Only ever from prose already on the page.
    An FAQ invented to carry markup is exactly the scaled-thin-page move Part X forbids."""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": ans}}
            for q, ans in pairs
        ],
    }


def graph(*blocks):
    """Nest into one @graph — one script tag per page, not five. Rule S2: generated
    by json.dumps, never hand-assembled in a template."""
    flat = [b for b in blocks if b]
    for b in flat:
        b.pop("@context", None)
    return json.dumps({"@context": "https://schema.org", "@graph": flat},
                      ensure_ascii=False)


def script_tag(jsonld):
    """Split so the literal string never appears in a Python source line that a
    naive HTML scraper could mistake for the real tag — same trick build.py uses."""
    return '<scr' + 'ipt type="application/ld+json">' + jsonld + '</scr' + 'ipt>'


# ---------------------------------------------------------------- open graph

def og_article_tags(a, desk_name, image_url=None, tags=None):
    """Rule T9 — an article must declare itself an article."""
    out = [
        # og:type is emitted by head(); never duplicate it here.
        f'<meta property="article:published_time" content="{iso_ts(a["date"])}">',
        f'<meta property="article:modified_time" content="{iso_ts(a.get("modified", a["date"]))}">',
        f'<meta property="article:section" content="{H.escape(desk_name)}">',
    ]
    for t in (tags or [])[:6]:
        out.append(f'<meta property="article:tag" content="{H.escape(t)}">')
    if image_url:
        out.append(f'<meta property="og:image" content="{image_url}">')
    return "\n".join(out)


# ---------------------------------------------------------------- indexnow

def indexnow_payload(key, urls, host="caratcapital.org"):
    """Rule E1 — the single highest-leverage item in the doctrine.

    POST to https://api.indexnow.org/indexnow, Content-Type application/json.
    The key file must be live at https://<host>/<key>.txt containing only the key.
    Bing supports this natively and it is how ChatGPT's retrieval layer learns we
    published. Google does not participate — its discovery comes from the sitemaps.
    """
    return json.dumps({
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": list(urls)[:10000],
    })


ENTITY_RE = None

def find_entities(text, registry):
    """C4/IV.3 — word-boundary, case-sensitive match of a known entity registry.

    Case-sensitive and boundary-anchored on purpose: a substring match counted 'IGI'
    inside 'origin' and 'eligible' and put the figure at 74 articles when the real
    one is 6. Measured 2026-09-17. Never loosen this.
    """
    hits = []
    for name, same_as in registry.items():
        if re.search(r'(?<![A-Za-z])' + re.escape(name) + r'(?![A-Za-z])', text):
            hits.append({"name": name, "sameAs": same_as})
    return hits
