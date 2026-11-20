#!/usr/bin/env python3
"""Generate the make.fun news-image entry for Friday 20 November 2026.

Draws a newspaper front page (1024x1024) using only PIL shapes and text.
Deterministic: fixed layout, no randomness, no time, no network.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
W, H = 1024, 1024
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT_PATH = os.path.join(OUT, "entry.png")

# Palette
PAPER = (244, 238, 224)      # warm off-white newsprint
INK = (24, 22, 20)           # near-black ink
RED = (150, 28, 28)          # deep red accent
BLUE = (24, 48, 92)          # dark blue panel headers
GREY = (120, 116, 108)       # muted grey

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def text_w(draw, txt, fnt):
    b = draw.textbbox((0, 0), txt, font=fnt)
    return b[2] - b[0]


def wrap(draw, txt, fnt, max_w):
    """Greedy word wrap to fit max_w pixels."""
    words = txt.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------------------
# Illustrations (PIL shapes only)
# ---------------------------------------------------------------------------
def draw_three_flags(d, cx, cy):
    d.rectangle([cx - 46, cy + 14, cx + 46, cy + 20], fill=INK)
    colors = [(150, 28, 28), (24, 48, 92), (28, 120, 60)]
    for i, col in enumerate(colors):
        x = cx - 30 + i * 30
        d.line([x, cy + 14, x, cy - 26], fill=INK, width=3)
        d.polygon([(x - 10, cy - 26), (x + 10, cy - 26), (x, cy - 40)], fill=col)
    for i in range(3):
        x = cx - 30 + i * 30
        d.rectangle([x - 8, cy + 20, x + 8, cy + 34], fill=INK)


def draw_cyclone(d, cx, cy):
    d.polygon([(cx - 60, cy + 30), (cx + 60, cy + 30), (cx + 60, cy + 44),
               (cx - 60, cy + 44)], fill=(120, 150, 170))
    pts = []
    for t in range(0, 360, 6):
        r = 5 + t * 0.08
        pts.append((cx + r * math.cos(math.radians(t)),
                    cy - 6 + r * math.sin(math.radians(t))))
    d.line(pts, fill=INK, width=3)
    d.ellipse([cx - 4, cy - 10, cx + 4, cy - 2], fill=INK)


def draw_scales(d, cx, cy):
    d.line([cx, cy - 34, cx, cy + 18], fill=INK, width=4)
    d.line([cx - 40, cy - 34, cx + 40, cy - 34], fill=INK, width=4)
    d.polygon([(cx - 40, cy - 34), (cx - 52, cy - 20), (cx - 28, cy - 20)], outline=INK)
    d.polygon([(cx + 40, cy - 34), (cx + 28, cy - 20), (cx + 52, cy - 20)], outline=INK)
    d.line([cx - 40, cy - 34, cx - 40, cy - 20], fill=INK, width=2)
    d.line([cx + 40, cy - 34, cx + 40, cy - 20], fill=INK, width=2)
    d.polygon([(cx - 12, cy + 18), (cx + 12, cy + 18), (cx + 8, cy + 28), (cx - 8, cy + 28)], fill=INK)
    gx = cx + 44
    d.rectangle([gx - 3, cy - 8, gx + 3, cy + 8], fill=INK)
    d.rectangle([gx - 10, cy + 6, gx + 10, cy + 10], fill=INK)


def draw_tower(d, cx, cy):
    d.polygon([(cx - 16, cy + 30), (cx + 16, cy + 30), (cx + 12, cy - 34),
               (cx - 12, cy - 34)], fill=(150, 150, 150), outline=INK)
    for yy in range(cy - 26, cy + 22, 8):
        d.rectangle([cx - 9, yy, cx - 5, yy + 4], fill=INK)
        d.rectangle([cx + 5, yy, cx + 9, yy + 4], fill=INK)
    d.ellipse([cx - 8, cy - 44, cx + 8, cy - 34], fill=(150, 150, 150))
    d.ellipse([cx - 12, cy - 56, cx + 12, cy - 44], fill=(170, 170, 170))
    d.ellipse([cx - 16, cy - 68, cx + 16, cy - 54], fill=(190, 190, 190))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    f_mast = font(BOLD, 58)
    f_date = font(BOLD, 26)
    mast = "THE WORLD IN ONE PICTURE"
    mw = text_w(d, mast, f_mast)
    d.text(((W - mw) / 2, 24), mast, font=f_mast, fill=INK)

    date = "FRIDAY, 20 NOVEMBER 2026"
    dw = text_w(d, date, f_date)
    d.text(((W - dw) / 2, 100), date, font=f_date, fill=RED)

    d.rectangle([40, 146, W - 40, 150], fill=RED)

    # ---- Story panels (2x2) ----
    margin = 40
    gap = 26
    panel_w = (W - 2 * margin - gap) // 2
    panel_h = 244
    top = 172
    row_gap = 24

    f_label = font(BOLD, 20)
    f_head = font(BOLD, 28)
    f_body = font(REG, 20)

    stories = [
        {
            "label": "SUMMIT",
            "head": "TRUMP, XI, PUTIN MEET",
            "body": ("First three-way summit in Shenzhen. Joint pledge: "
                     "\u201ca nuclear war cannot be won and must never be fought.\u201d"),
            "draw": draw_three_flags,
        },
        {
            "label": "CYCLONE",
            "head": "CYCLONE AKVAN HITS INDIA",
            "body": ("Severe storm crosses India's east coast near Gopalpur, "
                     "winds 90\u2013100 kmph. Odisha moved 100,000+ to shelters; "
                     "red alert for Andhra Pradesh & Odisha."),
            "draw": draw_cyclone,
        },
        {
            "label": "WORLD COURT",
            "head": "ICJ: MYANMAR GENOCIDE RISK",
            "body": ("World Court rules Myanmar's military likely intended to "
                     "destroy a substantial part of the Rohingya minority."),
            "draw": draw_scales,
        },
        {
            "label": "RIYADH",
            "head": "HOUTHI STRIKE HITS RIYADH",
            "body": ("A Houthi attack damaged one of Riyadh's tallest "
                     "skyscrapers, striking the Saudi capital."),
            "draw": draw_tower,
        },
    ]

    positions = [
        (margin, top),
        (margin + panel_w + gap, top),
        (margin, top + panel_h + row_gap),
        (margin + panel_w + gap, top + panel_h + row_gap),
    ]

    for (px, py), st in zip(positions, stories):
        d.rectangle([px, py, px + panel_w, py + panel_h], fill=(250, 246, 236),
                    outline=(200, 194, 180))
        # section label
        d.text((px + 14, py + 10), st["label"], font=f_label, fill=RED)
        # headline (wrap to 2 lines)
        head_lines = wrap(d, st["head"], f_head, panel_w - 28)[:2]
        hy = py + 40
        for ln in head_lines:
            d.text((px + 14, hy), ln, font=f_head, fill=BLUE)
            hy += 32
        # body text (wrap, up to 4 lines)
        body_lines = wrap(d, st["body"], f_body, panel_w - 28 - 96)[:4]
        by = hy + 6
        for ln in body_lines:
            d.text((px + 14, by), ln, font=f_body, fill=INK)
            by += 25
        # illustration on right side
        st["draw"](d, px + panel_w - 60, py + 150)

    # ---- Bottom ticker strip ----
    tick_top = top + 2 * panel_h + row_gap + 30
    d.rectangle([40, tick_top, W - 40, tick_top + 4], fill=BLUE)

    f_tick = font(BOLD, 20)
    tick_items = [
        "GTA VI reviews are in",
        "US\u2013Venezuela military cooperation deal",
        "Fiji drought disaster",
        "Crimean Bridge rail hit",
        "N. Korea expands Yongbyon",
        "NZ 243/5 v India (Nicholls 113*)",
        "Anthropic valued $1.5T",
        "Modi meets Prince & Princess of Wales",
    ]
    tick_txt = "  \u2022  ".join(tick_items)
    tick_lines = wrap(d, tick_txt, f_tick, W - 80)
    ty = tick_top + 12
    for ln in tick_lines[:3]:
        d.text((40, ty), ln, font=f_tick, fill=INK)
        ty += 26

    # footer line
    f_foot = font(REG, 18)
    foot = "THE WORLD IN ONE PICTURE  \u2014  FRIDAY, 20 NOVEMBER 2026"
    fw = text_w(d, foot, f_foot)
    d.text(((W - fw) / 2, H - 34), foot, font=f_foot, fill=GREY)

    os.makedirs(OUT, exist_ok=True)
    img.save(OUT_PATH, "PNG")
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    main()