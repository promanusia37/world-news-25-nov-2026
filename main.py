#!/usr/bin/env python3
"""World news, Wednesday 25 November 2026, in one image.

Deterministic, offline renderer: draws the 1024x1024 front page with PIL
from the story data below and the hero illustration shipped beside this
file (hero.png). Running it twice writes byte-identical PNGs.

Usage:  python3 main.py
Output: /output/entry.png when /output exists, else ./entry.png
Requires: Pillow (PIL), DejaVu fonts (present on Debian/Ubuntu).
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
NAVY = (14, 42, 71)
RED = (178, 34, 34)
GOLD = (198, 154, 44)
GREY = (90, 86, 78)
LINE = (180, 172, 156)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SERIF_I = os.path.join(FONT_DIR, "DejaVuSerif.ttf")  # no italic shipped; use regular serif


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


LEAD = {
    "kicker": "LEAD  ·  STRAIT OF HORMUZ",
    "headline": "TWO TANKERS HIT BY MINES IN THE STRAIT OF HORMUZ",
    "body": (
        "Iran's Revolutionary Guard says two oil tankers struck naval mines, "
        "exploded and caught fire while crossing the world's most important "
        "oil chokepoint."
    ),
    "caption": (
        "Burning tankers in the Strait of Hormuz, through which a fifth of the "
        "world's seaborne oil passes.  —  Illustration"
    ),
}

STORIES = [
    {
        "kicker": "WAR  ·  SAUDI ARABIA",
        "headline": "HOUTHIS HIT SAUDI REFINERY",
        "body": (
            "Yemen's Houthis say they struck the Ras Tanura refinery, a day "
            "after a strike on a Riyadh tower injured 11 people."
        ),
    },
    {
        "kicker": "TECH  ·  UNITED STATES",
        "headline": "HUAWEI FOUND GUILTY",
        "body": (
            "A US federal court convicts the Chinese tech giant of conspiring "
            "to steal trade secrets and bank fraud; the racketeering charge fails."
        ),
    },
    {
        "kicker": "CLIMATE  ·  VATICAN",
        "headline": "POPE LAMENTS COP31 FAILURE",
        "body": (
            "Pope Leo XIV voices concern as the UN climate talks end with no "
            "deal, warning extreme weather is growing more frequent."
        ),
    },
    {
        "kicker": "ECONOMY  ·  UNITED STATES",
        "headline": "US ECONOMY ROARS",
        "body": (
            "Third-quarter growth surges while October inflation stays hot; "
            "Trump unveils new tariffs on Brazil, 10% on aircraft."
        ),
    },
    {
        "kicker": "SPACE  ·  CHINA",
        "headline": "CHINA FLIES FIRST FOREIGN ASTRONAUT",
        "body": (
            "Shenzhou-24 docks at China's space station carrying a Pakistani "
            "national — the first foreign astronaut aboard."
        ),
    },
]

NUMBERS = [
    ("2", "tankers hit by mines in the Strait of Hormuz"),
    ("31", "killed in a fuel-tanker fire near Cairo"),
    ("19", "civilians killed in Sudan drone strikes"),
    ("11", "hurt in the Houthi strike on a Riyadh tower"),
]

TICKER = (
    "ALSO — Solomon Islands & Australia bar foreign military bases  •  "
    "Lukoil sells overseas assets to a Boehly-led group  •  A second US judge "
    "blocks Trump's birthright order  •  Bangladesh raises the garment "
    "minimum wage 36%"
)

FOOTER = (
    "Sources: Just Security Early Edition, Reuters, AP, LA Post — 25 November 2026  ·  "
    "Built by an AI agent for make.fun's news-image-20261125 bounty"
)


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.rectangle([0, 96, W, 100], fill=GOLD)
    f_title = font(SERIF_B, 58)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 8), title, font=f_title, fill=(250, 246, 236))
    f_date = font(SANS_B, 19)
    date = "WEDNESDAY, 25 NOVEMBER 2026  ·  WORLD NEWS IN ONE IMAGE"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 68), date, font=f_date, fill=(212, 175, 90))

    # ---- Hero -----------------------------------------------------------
    hero_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hero.png")
    hero = Image.open(hero_path).convert("RGB")
    hero = ImageOps.fit(hero, (W, 296), method=Image.LANCZOS)
    img.paste(hero, (0, 100))
    d.rectangle([0, 396, W, 397], fill=NAVY)

    # ---- Caption --------------------------------------------------------
    f_cap = font(SERIF_I, 15)
    d.text((24, 404), LEAD["caption"], font=f_cap, fill=GREY)

    # ---- Lead story (flow layout: y advances as text is drawn) ---------
    y = 430
    f_kick = font(SANS_B, 17)
    d.text((24, y), LEAD["kicker"], font=f_kick, fill=RED)
    y += 26
    f_head = font(SERIF_B, 40)
    for line in wrap(d, LEAD["headline"], f_head, W - 48):
        d.text((24, y), line, font=f_head, fill=INK)
        y += 46
    y += 4
    f_body = font(SANS, 20)
    for line in wrap(d, LEAD["body"], f_body, W - 48):
        d.text((24, y), line, font=f_body, fill=(40, 38, 34))
        y += 27
    y += 10

    # ---- Divider --------------------------------------------------------
    d.line([24, y, W - 24, y], fill=LINE, width=2)
    y += 14

    # ---- Story cards: 2 columns x 3 rows -------------------------------
    # Row 3, right cell = "the day in numbers" panel.
    col_w = (W - 48 - 24) // 2
    row_h = 104
    positions = [(24, y), (24 + col_w + 24, y),
                 (24, y + row_h), (24 + col_w + 24, y + row_h),
                 (24, y + 2 * row_h)]
    f_ck = font(SANS_B, 13)
    f_ch = font(SERIF_B, 21)
    f_cb = font(SANS, 16)
    for story, (x, yy) in zip(STORIES, positions):
        d.text((x, yy), story["kicker"], font=f_ck, fill=RED)
        hy = yy + 18
        for line in wrap(d, story["headline"], f_ch, col_w):
            d.text((x, hy), line, font=f_ch, fill=INK)
            hy += 25
        by = hy + 2
        for line in wrap(d, story["body"], f_cb, col_w):
            d.text((x, by), line, font=f_cb, fill=(40, 38, 34))
            by += 21

    # Numbers panel (4 entries; the Bangladesh wage line lives in the ticker)
    px, py = 24 + col_w + 24, y + 2 * row_h
    d.rectangle([px, py, px + col_w, py + row_h - 8], fill=(232, 226, 210))
    d.text((px + 12, py + 6), "THE DAY IN NUMBERS", font=f_ck, fill=NAVY)
    ny = py + 26
    f_num = font(SANS_B, 15)
    f_nlab = font(SANS, 14)
    for num, label in NUMBERS:
        d.text((px + 12, ny), num, font=f_num, fill=RED)
        d.text((px + 78, ny + 1), label, font=f_nlab, fill=(40, 38, 34))
        ny += 18

    # ---- Ticker ---------------------------------------------------------
    ty = y + 3 * row_h + 8
    d.rectangle([0, ty, W, ty + 52], fill=NAVY)
    f_tick = font(SANS, 15)
    tick_lines = wrap(d, TICKER, f_tick, W - 48)
    tyy = ty + 6
    for line in tick_lines:
        d.text((24, tyy), line, font=f_tick, fill=(235, 230, 220))
        tyy += 19

    # ---- Footer ---------------------------------------------------------
    f_foot = font(SANS, 12)
    d.text((24, ty + 58), FOOTER, font=f_foot, fill=GREY)

    return img


def main():
    img = draw_page()
    out = "/output/entry.png" if os.path.isdir("/output") else "entry.png"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.save(out, format="PNG")
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
