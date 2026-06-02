#!/usr/bin/env python3
"""
Inject a complete OG + Twitter card meta tag block into every page.

Idempotent: removes any existing contiguous block of og:* / twitter:* meta
tags and re-inserts the canonical block for the page. The block is positioned
right after the page's <meta name="description"> line.

Per-page data lives in PAGES below; add a new page by appending a tuple.
"""

import os
import re

REPO = "/home/workspace/Projects/cbse-osm-osint"
SITE = "CBSE OSM OSINT \u2014 Cashless Consumer"
BASE_URL = "https://ccagentorg.github.io/cbse-osm-osint"
LOCALE = "en_IN"

# (filename, og_type, og_title, og_description, twitter_title, twitter_description, image_alt)
PAGES = [
    (
        "index.html",
        "website",
        "CBSE OSM Investigation \u2014 Who Graded 17.8 Lakh Students?",
        "17.8 lakh students graded on one vendor's hacked platform. Tender rules rewritten. An open-source OSINT investigation.",
        "CBSE OSM Investigation \u2014 Who Graded 17.8 Lakh Students?",
        "17.8 lakh students graded on one vendor's hacked platform. An open-source OSINT investigation.",
        "CBSE OSM OSINT homepage card \u2014 red page-01 stamp, headline 'Who Graded 17.8 Lakh Students?' on cream background.",
    ),
    (
        "findings.html",
        "article",
        "Our Findings \u2014 CBSE OSM Investigation",
        "OSINT investigation into Coempt EduTeck, the vendor behind CBSE's On-Screen Marking system. Technical vulnerabilities, corporate network analysis, and structural reform questions.",
        "Our Findings \u2014 CBSE OSM OSINT",
        "OSINT investigation into Coempt EduTeck, the vendor behind CBSE's On-Screen Marking system.",
        "CBSE OSM OSINT findings card \u2014 page 02, headline 'What We Found' on cream background with red stamp.",
    ),
    (
        "tender.html",
        "article",
        "Tender Manipulation \u2014 How CBSE Rewrote the Rules for Coempt",
        "Three failed rounds. Conditions relaxed mid-process. Coempt wins. The identical playbook was used at SSC too. Sarthak Sidhant's India Today investigation.",
        "Tender Manipulation \u2014 How CBSE Rewrote the Rules",
        "Three failed rounds. Conditions relaxed. Coempt wins. The identical playbook used at SSC too.",
        "CBSE OSM OSINT tender manipulation card \u2014 page 03, headline 'How CBSE Rewrote the Rules for Coempt' with red stamp.",
    ),
    (
        "know-your-coempt.html",
        "article",
        "Know Your Coempt \u2014 The Chary Family, S. Sadagopan, and Ventureast",
        "How a small Hyderabad firm with 5 directors and \u20B920Cr paid-up became the gatekeeper of India's largest school examination system.",
        "Know Your Coempt \u2014 The Chary Family Network",
        "A small Hyderabad firm with 5 directors and \u20B920Cr paid-up became the gatekeeper of India's largest school exam system.",
        "CBSE OSM OSINT vendor profile card \u2014 page 04, headline 'Know Your Coempt' on cream background with red stamp.",
    ),
    (
        "know-your-examtech.html",
        "article",
        "Know Your ExamTech \u2014 Why India's Exam System Keeps Getting Captured",
        "Coempt (CBSE) and Eduquity (SSC) followed the same playbook. NEET CBT 2027 is next. Here's how India's exam-tech market works \u2014 and why it keeps failing you.",
        "Know Your ExamTech \u2014 The Capture Pattern",
        "Coempt (CBSE) and Eduquity (SSC) ran the same playbook. NEET CBT 2027 is next.",
        "CBSE OSM OSINT sector analysis card \u2014 page 05, headline 'Know Your ExamTech' on cream background with red stamp.",
    ),
    (
        "ni5arga-vulnerabilities.html",
        "article",
        "ni5arga's Findings \u2014 9 Holes in India's Exam System",
        "A 19-year-old found 9 security holes including a 457K+ payment data leak. The system that graded 17.8 lakh students was wide open for 3+ months.",
        "ni5arga's Findings \u2014 9 Holes in India's Exam System",
        "9 security holes including a 457K+ payment data leak. The system that graded 17.8 lakh students was wide open for 3+ months.",
        "CBSE OSM OSINT security research card \u2014 page 06, headline '9 Holes in India's Exam System' with red stamp.",
    ),
    (
        "terms-of-reference.html",
        "article",
        "Terms of Reference for Investigation \u2014 CBSE OSM",
        "A framework for formal investigation and disclosure demands concerning the CBSE On-Screen Marking controversy, grounded in the RTI Act, IT Act, and digital rights principles.",
        "Terms of Reference for Investigation \u2014 CBSE OSM",
        "Framework for formal investigation into the CBSE OSM controversy \u2014 vendor due diligence, infrastructure audit, data protection.",
        "CBSE OSM OSINT framework card \u2014 page 07, headline 'Terms of Reference' on cream background with red stamp.",
    ),
    (
        "annexure.html",
        "article",
        "Technical Annexure \u2014 CBSE OSM OSINT Evidence",
        "Full code evidence, API endpoints, XPath selectors, and methodology for the CBSE OSM OSINT investigation.",
        "Technical Annexure \u2014 CBSE OSM OSINT Evidence",
        "Methodology, tool inventory, code evidence, API endpoints, and forensic timeline for the OSINT investigation.",
        "CBSE OSM OSINT technical annexure card \u2014 page 08, headline 'Technical Annexure' on cream background with red stamp.",
    ),
    (
        "api-surface.html",
        "article",
        "API Surface Analysis \u2014 CBSE OnMark Platform",
        "77 exposed API endpoints, hardcoded credentials, and unauthenticated evaluator access on CBSE's OSM vendor platform.",
        "API Surface Analysis \u2014 CBSE OnMark Platform",
        "77 exposed API endpoints, hardcoded credentials, and unauthenticated evaluator access on CBSE's OSM vendor platform.",
        "CBSE OSM OSINT API surface card \u2014 page 09, headline 'OnMark API Inventory' on cream background with red stamp.",
    ),
    (
        "impacted-entities.html",
        "article",
        "Impacted Entities \u2014 CBSE OSM OSINT",
        "Every board, university, and institution whose evaluation data passed through Coempt EduTeck's OnMark platform.",
        "Impacted Entities \u2014 CBSE OSM OSINT",
        "Every board, university, and institution whose evaluation data passed through Coempt EduTeck's OnMark platform.",
        "CBSE OSM OSINT impacted entities card \u2014 page 10, headline 'Impacted Entities' on cream background with red stamp.",
    ),
]


def page_url(filename: str) -> str:
    if filename == "index.html":
        return f"{BASE_URL}/"
    return f"{BASE_URL}/{filename}"


def build_block(filename, og_type, og_title, og_desc, tw_title, tw_desc, img_alt):
    page = page_url(filename)
    slug = filename.replace(".html", "")
    img_rel = f"images/og/{slug}.png"
    return (
        f'<meta name="og-meta-marker" content="cbse-osm-osint">\n'
        f'<meta property="og:site_name" content="{SITE}">\n'
        f'<meta property="og:locale" content="{LOCALE}">\n'
        f'<meta property="og:type" content="{og_type}">\n'
        f'<meta property="og:title" content="{og_title}">\n'
        f'<meta property="og:description" content="{og_desc}">\n'
        f'<meta property="og:url" content="{page}">\n'
        f'<meta property="og:image" content="{BASE_URL}/{img_rel}">\n'
        f'<meta property="og:image:secure_url" content="{BASE_URL}/{img_rel}">\n'
        f'<meta property="og:image:type" content="image/png">\n'
        f'<meta property="og:image:width" content="1200">\n'
        f'<meta property="og:image:height" content="630">\n'
        f'<meta property="og:image:alt" content="{img_alt}">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:site" content="@CashlessConsumr">\n'
        f'<meta name="twitter:creator" content="@CashlessConsumr">\n'
        f'<meta name="twitter:title" content="{tw_title}">\n'
        f'<meta name="twitter:description" content="{tw_desc}">\n'
        f'<meta name="twitter:image" content="{BASE_URL}/{img_rel}">\n'
        f'<meta name="twitter:image:alt" content="{img_alt}">\n'
    )


OG_TWITTER_RE = re.compile(
    r'<meta\s+(?:property="og:|name="twitter:|name="og-meta-marker")[^>]+>\s*',
    re.IGNORECASE,
)


def inject(filepath, page_data):
    filename, og_type, og_title, og_desc, tw_title, tw_desc, img_alt = page_data
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Remove existing block
    matches = list(OG_TWITTER_RE.finditer(html))
    if matches:
        start = matches[0].start()
        end = matches[-1].end()
        html = html[:start] + html[end:]

    # Insert new block right after <meta name="description" ...>
    new_block = build_block(filename, og_type, og_title, og_desc, tw_title, tw_desc, img_alt)
    m = re.search(r'(<meta\s+name="description"[^>]+>)', html)
    if not m:
        # Fallback: insert before <style>
        m = re.search(r'(<style)', html, re.IGNORECASE)
    if not m:
        print(f"  SKIP {filename} (no insertion anchor)")
        return False

    html = html[:m.end()] + "\n" + new_block + html[m.end():]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def main():
    by_name = {p[0]: p for p in PAGES}
    pages = [f for f in os.listdir(REPO) if f.endswith(".html")]
    for name in sorted(pages):
        if name not in by_name:
            print(f"  ???  {name} (no PAGES entry)")
            continue
        path = os.path.join(REPO, name)
        ok = inject(path, by_name[name])
        print(f"  {'OK  ' if ok else 'SKIP'} {name}")
    print(f"\n{len(pages)} pages processed")


if __name__ == "__main__":
    main()
