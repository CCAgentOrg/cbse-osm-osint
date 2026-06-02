#!/usr/bin/env python3
"""
Build branded 1200x630 OG/Twitter card images for every page on the site.

Outputs: images/og/<slug>.png  (one per page)
Design: cream editorial, deep-red accent, Georgia-like serif title, page-number stamp.
"""

import os
import re
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO = "/home/workspace/Projects/cbse-osm-osint"
OUT_DIR = os.path.join(REPO, "images", "og")
os.makedirs(OUT_DIR, exist_ok=True)

# --- Fonts ---------------------------------------------------------------
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# --- Palette (matches site theme) ----------------------------------------
BG_TOP = (250, 249, 246)       # #faf9f6 cream
BG_BOTTOM = (235, 228, 215)    # #ebe4d7
RED = (139, 26, 26)            # #8b1a1a
RED_DARK = (90, 15, 15)        # #5a0f0f
RED_LIGHT = (196, 160, 160)    # #c4a0a0
INK = (26, 26, 26)             # #1a1a1a
MUTED = (102, 99, 92)          # #66635c
PAPER = (255, 253, 248)        # #fffdf8

W, H = 1200, 630


def font(path, size):
    return ImageFont.truetype(path, size)


# --- Card data -----------------------------------------------------------
# (slug, section_label, title, subtitle, page_number, accent_side)
CARDS = [
    (
        "index",
        "Investigation",
        "Who Graded 17.8 Lakh Students?",
        "A single vendor's hacked platform, a tender rewritten to fit, and zero accountability.",
        1,
    ),
    (
        "findings",
        "Our Findings",
        "What We Found",
        "OSINT into Coempt EduTeck, OnMark vulnerabilities, and the corporate network behind CBSE's grading vendor.",
        2,
    ),
    (
        "tender",
        "Tender Manipulation",
        "How CBSE Rewrote the Rules for Coempt",
        "Three failed rounds. Conditions relaxed mid-process. Coempt wins. The same playbook repeats at SSC.",
        3,
    ),
    (
        "know-your-coempt",
        "Vendor Profile",
        "Know Your Coempt",
        "How a small Hyderabad firm with 5 directors and \u20B920Cr paid-up became the gatekeeper of India's largest school examination system.",
        4,
    ),
    (
        "know-your-examtech",
        "Sector Analysis",
        "Know Your ExamTech",
        "Coempt (CBSE) and Eduquity (SSC) ran the same playbook. NEET CBT 2027 is next. How India's exam-tech market keeps failing you.",
        5,
    ),
    (
        "ni5arga-vulnerabilities",
        "Security Research",
        "9 Holes in India's Exam System",
        "A 19-year-old found nine security flaws \u2014 including a 457K+ payment data leak. Three months. No fixes. Here's what it means for 17.8 lakh students.",
        6,
    ),
    (
        "terms-of-reference",
        "Investigation Framework",
        "Terms of Reference",
        "A framework for formal investigation and disclosure demands grounded in the RTI Act, IT Act, and digital rights principles.",
        7,
    ),
    (
        "annexure",
        "Technical Evidence",
        "Technical Annexure",
        "Methodology, tool inventory, code evidence, API endpoints, and forensic timeline for the OSINT investigation.",
        8,
    ),
    (
        "api-surface",
        "API Surface",
        "OnMark API Inventory",
        "77 exposed API endpoints, hardcoded credentials, and unauthenticated evaluator access extracted from the OnMark Angular bundle.",
        9,
    ),
    (
        "impacted-entities",
        "Stakeholder Map",
        "Impacted Entities",
        "Every board, university, and institution whose evaluation data passed through Coempt EduTeck's OnMark platform.",
        10,
    ),
]


# --- Drawing helpers -----------------------------------------------------
def gradient_bg():
    """Vertical cream gradient."""
    base = Image.new("RGB", (W, H), BG_TOP)
    top = BG_TOP
    bot = BG_BOTTOM
    px = base.load()
    for y in range(H):
        t = y / (H - 1)
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return base


def wrap_lines(text, font_obj, max_w, draw):
    """Word-wrap to fit max width."""
    words = text.split()
    lines, cur = [], []
    for w in words:
        cand = " ".join(cur + [w])
        bbox = draw.textbbox((0, 0), cand, font=font_obj)
        if bbox[2] - bbox[0] <= max_w or not cur:
            cur.append(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


def draw_card(slug, section, title, subtitle, page_no):
    img = gradient_bg()
    d = ImageDraw.Draw(img)

    # Top red bar
    d.rectangle([(0, 0), (W, 10)], fill=RED)

    # Page-number stamp (top-right)
    stamp_w, stamp_h = 200, 200
    stamp_x, stamp_y = W - stamp_w - 60, 60
    d.rectangle([(stamp_x, stamp_y), (stamp_x + stamp_w, stamp_y + stamp_h)], fill=RED)
    f_num = font(SERIF_BOLD, 110)
    num_str = f"{page_no:02d}"
    bbox = d.textbbox((0, 0), num_str, font=f_num)
    nw, nh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(
        (stamp_x + (stamp_w - nw) // 2 - bbox[0],
         stamp_y + (stamp_h - nh) // 2 - bbox[1] - 8),
        num_str,
        font=f_num,
        fill=PAPER,
    )
    f_lbl = font(SANS_BOLD, 18)
    lbl = "PAGE"
    bbox = d.textbbox((0, 0), lbl, font=f_lbl)
    lw = bbox[2] - bbox[0]
    d.text(
        (stamp_x + (stamp_w - lw) // 2 - bbox[0],
         stamp_y + stamp_h - 40),
        lbl,
        font=f_lbl,
        fill=PAPER,
    )

    # Section label
    f_section = font(SANS_BOLD, 26)
    d.text((80, 100), section.upper(), font=f_section, fill=RED)

    # Small accent line under section
    d.rectangle([(80, 140), (140, 144)], fill=RED)

    # Title (serif, large, multi-line)
    f_title = font(SERIF_BOLD, 76)
    title_lines = wrap_lines(title, f_title, W - 160 - stamp_w - 40, d)
    # Cap at 3 lines
    title_lines = title_lines[:3]
    y = 180
    for line in title_lines:
        d.text((80, y), line, font=f_title, fill=INK)
        y += 88

    # Description (sans, muted, smaller)
    f_sub = font(SANS_REG, 30)
    sub_lines = wrap_lines(subtitle, f_sub, W - 160, d)
    sub_lines = sub_lines[:2]
    sub_y = y + 30
    for line in sub_lines:
        d.text((80, sub_y), line, font=f_sub, fill=MUTED)
        sub_y += 42

    # Bottom red rule
    d.rectangle([(80, H - 90), (160, H - 86)], fill=RED)

    # Brand row
    f_brand = font(SANS_BOLD, 22)
    f_sub2 = font(SANS_REG, 20)
    d.text((80, H - 70), "CBSE OSM  /  OSINT", font=f_brand, fill=RED_DARK)
    d.text((80, H - 42), "Investigation \u00B7 May\u2013Jun 2026", font=f_sub2, fill=MUTED)

    right_x = W - 80
    brand_right = "Cashless Consumer"
    bbox = d.textbbox((0, 0), brand_right, font=f_brand)
    rw = bbox[2] - bbox[0]
    d.text((right_x - rw, H - 70), brand_right, font=f_brand, fill=INK)
    url = "cashlessconsumer.in"
    bbox = d.textbbox((0, 0), url, font=f_sub2)
    uw = bbox[2] - bbox[0]
    d.text((right_x - uw, H - 42), url, font=f_sub2, fill=MUTED)

    # Subtle paper grain overlay (light noise)
    out = img.filter(ImageFilter.SMOOTH)
    out_path = os.path.join(OUT_DIR, f"{slug}.png")
    out.save(out_path, "PNG", optimize=True)
    return out_path


def main():
    for slug, section, title, subtitle, page_no in CARDS:
        path = draw_card(slug, section, title, subtitle, page_no)
        size = os.path.getsize(path)
        with Image.open(path) as im:
            dims = im.size
        print(f"  OK   {slug:<30} {dims[0]}x{dims[1]}  {size/1024:6.1f} KB")
    print(f"\n{len(CARDS)} cards written to {OUT_DIR}")


if __name__ == "__main__":
    main()
