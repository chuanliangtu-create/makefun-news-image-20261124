#!/usr/bin/env python3
"""Draw the 24 November 2026 front page as a 1024x1024 PNG.

Run: python3 draw_news.py [output-path]
Default output is entry.png next to this script. Pure Pillow drawing,
no network, no downloaded images, no wall-clock time, no randomness,
so the same script always paints the same bytes.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (90, 90, 90)
LIGHT = (238, 238, 238)
RED = (166, 25, 46)  # the one strong accent colour

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
]


def font(name, size):
    for d in FONT_DIRS:
        path = os.path.join(d, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def para(draw, x, y, text, fnt, max_width, leading, fill=BLACK):
    """Draw wrapped text, return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=BLACK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    mx = 36  # side margin; content runs mx .. W - mx
    rx = W - mx

    d.rectangle([20, 20, W - 20, H - 20], outline=BLACK, width=3)

    # ---- Masthead ----
    title = "THE WORLD IN ONE PAGE"
    tf = SERIF_BOLD(58)
    d.text(((W - d.textlength(title, font=tf)) / 2, 44), title,
           font=tf, fill=BLACK)
    rule(d, mx, 128, rx, 3)
    rule(d, mx, 134, rx, 6, RED)
    date = "TUESDAY 24 NOVEMBER 2026"
    df = SANS_BOLD(30)
    d.text(((W - d.textlength(date, font=df)) / 2, 146), date,
           font=df, fill=RED)
    sub = "FOUR STORIES THAT DEFINED THE DAY  ·  ONE DAY, ONE IMAGE"
    sf = SANS(17)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 188), sub,
           font=sf, fill=GREY)

    # ---- Lead story: Nvidia ----
    ly = 224
    d.rectangle([mx, ly, rx, 528], outline=BLACK, width=2)
    d.text((mx + 20, ly + 16), "TECH & MARKETS", font=SANS_BOLD(21), fill=RED)
    y = para(d, mx + 20, ly + 52, "HUANG IS BACK AT NVIDIA",
             SANS_BOLD(54), 600, 62)
    y = para(d, mx + 20, y + 10,
             "The board reinstates Jensen Huang as chief executive "
             "after President Trump intervenes. Nvidia shares jump 33% "
             "and the AI rally roars back.",
             SANS(23), 600, 30)
    # Rising-bars motif with the +33% call-out.
    px0, py0, px1, py1 = 692, ly + 16, rx - 20, 508
    d.rectangle([px0, py0, px1, py1], fill=LIGHT, outline=BLACK, width=2)
    base = py1 - 52
    bars = [34, 52, 44, 66, 84, 108]
    bw, gap = 30, 12
    bx = px0 + 18
    for h in bars:
        d.rectangle([bx, base - h, bx + bw, base], fill=BLACK)
        bx += bw + gap
    d.line([(px0 + 14, base - 58), (px1 - 30, base - 128)],
           fill=RED, width=5)
    d.polygon([(px1 - 30, base - 128), (px1 - 52, base - 132),
               (px1 - 44, base - 112)], fill=RED)
    d.text((px0 + 18, py0 + 12), "+33%", font=SANS_BOLD(46), fill=RED)
    d.text((px0 + 18, py0 + 66), "NVIDIA SHARES",
           font=SANS_BOLD(18), fill=BLACK)

    # ---- Three stories in a grid ----
    gy = 548
    col_w = 304
    cols = [
        ("WAR IN UKRAINE",
         "KYIV HIT AS UKRAINE SINKS WARSHIP OFF LIBYA",
         "Russian strikes kill at least 14 in the Kyiv region. "
         "Sea drones sink the corvette Merkury at Benghazi.",
         "ship"),
        ("CLIMATE",
         "COP31 COLLAPSES WITH NO DEAL",
         "Antalya talks end with no pact after fossil-fuel "
         "language is stripped from the final text.",
         "sun"),
        ("UNITED STATES",
         "DEMOCRATS WIN BIGGEST HOUSE MAJORITY SINCE 1992",
         "258 seats clinched nationwide, the largest majority "
         "since 1992. Storms on both coasts threaten "
         "Thanksgiving travel.",
         "storm"),
    ]
    for i, (kicker, head, summ, motif) in enumerate(cols):
        x0 = mx + i * (col_w + 20)
        x1 = x0 + col_w
        rule(d, x0, gy, x1, 5, RED)
        d.text((x0, gy + 12), kicker, font=SANS_BOLD(18), fill=RED)
        y = para(d, x0, gy + 42, head, SANS_BOLD(29), col_w, 35)
        y = para(d, x0, y + 8, summ, SANS(19), col_w, 26)
        my0, my1 = 852, 942
        d.rectangle([x0, my0, x1, my1], fill=LIGHT, outline=BLACK, width=2)
        cx = (x0 + x1) // 2
        if motif == "ship":
            d.polygon([(x0 + 40, my1 - 34), (x1 - 40, my1 - 34),
                       (x1 - 70, my1 - 12), (x0 + 70, my1 - 12)], fill=BLACK)
            d.line([(cx, my1 - 34), (cx, my1 - 66)], fill=BLACK, width=4)
            d.polygon([(cx, my1 - 66), (cx + 34, my1 - 46), (cx, my1 - 46)],
                      fill=RED)
            for wy in (my1 - 62, my1 - 74):
                d.line([(x0 + 24, wy), (x1 - 24, wy)], fill=GREY, width=2)
        elif motif == "sun":
            d.ellipse([cx - 26, my0 + 22, cx + 26, my0 + 74],
                      outline=BLACK, width=4)
            for a in range(0, 360, 45):
                import math
                r1, r2 = 34, 46
                x_a = cx + r1 * math.cos(math.radians(a))
                y_a = my0 + 48 + r1 * math.sin(math.radians(a))
                x_b = cx + r2 * math.cos(math.radians(a))
                y_b = my0 + 48 + r2 * math.sin(math.radians(a))
                d.line([(x_a, y_a), (x_b, y_b)], fill=RED, width=3)
            d.line([(x0 + 24, my1 - 18), (x1 - 24, my1 - 18)],
                   fill=BLACK, width=3)
        else:  # storm
            d.ellipse([cx - 52, my0 + 18, cx - 2, my0 + 52],
                      outline=BLACK, width=3)
            d.ellipse([cx - 18, my0 + 8, cx + 52, my0 + 52],
                      outline=BLACK, width=3)
            for rx0 in (cx - 40, cx - 8, cx + 24):
                d.line([(rx0, my0 + 62), (rx0 - 8, my0 + 88)],
                       fill=RED, width=4)

    # ---- Footer ----
    rule(d, mx, 958, rx, 2)
    foot = "TUESDAY 24 NOVEMBER 2026  ·  THE WORLD IN ONE PAGE"
    ff = SANS_BOLD(17)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 970), foot,
           font=ff, fill=BLACK)

    img.save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
