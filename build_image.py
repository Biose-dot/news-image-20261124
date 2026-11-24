#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Tuesday 24 November 2026.

One 1024x1024 PNG: a masthead, one lead story, four news panels and an
"Also today" strip. Every picture is drawn with plain PIL shapes and
DejaVu type. Fully deterministic: no network, no clock, no randomness.
Run:  python3 build_image.py   -> writes entry.png next to this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
STEEL = (70, 90, 120)
NIGHT = (18, 30, 58)
GOLD = (198, 148, 52)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)         # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)            # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    lh = leading if leading is not None else int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, color=RED, size=16):
    f = SANS_B(size)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + size + 6


def skyline(draw, x0, y_base, x1, heights, color):
    """Row of building silhouettes between x0 and x1, tops from heights."""
    n = len(heights)
    step = (x1 - x0) / n
    for i, h in enumerate(heights):
        bx0 = x0 + i * step + 2
        bx1 = x0 + (i + 1) * step - 2
        draw.rectangle([bx0, y_base - h, bx1, y_base], fill=color)
        # a few lit windows
        for wy in range(y_base - h + 6, y_base - 4, 14):
            for wx in (bx0 + 4, bx0 + 12):
                if wx < bx1 - 4:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=GOLD)


def draw_lead_art(draw, box):
    """Night sky over Kyiv: radar dish, missile trails, city skyline."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=NIGHT)
    # stars
    stars = [(18, 22), (70, 60), (130, 18), (190, 48), (250, 26),
             (310, 66), (360, 30), (46, 96), (160, 88), (290, 96),
             (340, 112), (230, 120), (110, 130), (20, 140)]
    for sx, sy in stars:
        draw.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                     fill=(240, 240, 220))
    # moon
    draw.ellipse([x0 + 330, y0 + 14, x0 + 372, y0 + 56], fill=(238, 232, 200))
    draw.ellipse([x0 + 344, y0 + 22, x0 + 372, y0 + 56], fill=NIGHT)
    # missile trails arcing down
    for tx, ty, dx in ((60, 30, 120), (170, 16, 150), (280, 40, 90)):
        draw.line([(x0 + tx, y0 + ty), (x0 + tx + dx, y0 + ty + 110)],
                  fill=(255, 190, 90), width=4)
        draw.ellipse([x0 + tx + dx - 5, y0 + ty + 105,
                      x0 + tx + dx + 5, y0 + ty + 115], fill=(255, 220, 130))
    # radar dish on a mast
    mx, my = x0 + 90, y1 - 62
    draw.line([(mx, my), (mx, my - 46)], fill=(200, 210, 225), width=5)
    draw.arc([mx - 42, my - 96, mx + 42, my - 12], 200, 340,
             fill=(200, 210, 225), width=5)
    draw.line([(mx - 38, my - 52), (mx + 38, my - 52)],
              fill=(200, 210, 225), width=4)
    # sweeping beam
    draw.line([(mx, my - 52), (mx + 96, my - 108)],
              fill=(120, 200, 120), width=3)
    # city skyline
    skyline(draw, x0 + 6, y1 - 4, x1 - 6,
            [52, 84, 64, 108, 72, 96, 58, 120, 78, 66, 92, 60], (8, 14, 30))
    draw.rectangle([x0, y1 - 4, x1, y1], fill=(8, 14, 30))


def draw_estonia_art(draw, box):
    """Warning triangle over a stylised Baltic map."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(232, 222, 196))
    # stylised land mass on the left (filled, Baltic coast)
    pts = [(x0 + 22, y1 - 8), (x0 + 48, y0 + 10), (x0 + 130, y0 + 6),
           (x0 + 200, y0 + 12), (x0 + 224, y0 + 26), (x0 + 200, y1 - 10),
           (x0 + 120, y1 - 6)]
    draw.polygon(pts, fill=(178, 198, 220), outline=STEEL, width=2)
    draw.line([(x0 + 48, y0 + 10), (x0 + 200, y1 - 10)], fill=STEEL, width=2)
    # warning triangle on the right
    cx, cy = x0 + 340, (y0 + y1) // 2
    tri = [(cx, cy - 22), (cx - 26, cy + 20), (cx + 26, cy + 20)]
    draw.polygon(tri, fill=(245, 200, 40), outline=INK, width=2)
    draw.text((cx - 4, cy - 16), "!", font=SANS_B(24), fill=INK)


def draw_awacs_art(draw, box):
    """AWACS jet with its radar dome over clouds."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(214, 228, 240))
    # clouds
    for cx, cy, r in ((60, 44, 14), (150, 48, 16), (250, 42, 12)):
        draw.ellipse([x0 + cx - r, y0 + cy - r // 2,
                      x0 + cx + r, y0 + cy + r // 2], fill=(255, 255, 255))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 4
    # fuselage
    draw.polygon([(cx - 120, cy), (cx - 60, cy - 12), (cx + 90, cy - 10),
                  (cx + 132, cy - 2), (cx + 90, cy + 6), (cx - 60, cy + 8)],
                 fill=(235, 238, 242), outline=INK, width=2)
    # radar dome
    draw.ellipse([cx - 30, cy - 34, cx + 30, cy - 10],
                 fill=(200, 208, 216), outline=INK, width=2)
    draw.line([(cx, cy - 10), (cx, cy - 6)], fill=INK, width=3)
    # tail + wing
    draw.polygon([(cx - 108, cy - 2), (cx - 124, cy - 30), (cx - 96, cy - 6)],
                 fill=(200, 208, 216), outline=INK, width=2)
    draw.polygon([(cx - 10, cy + 6), (cx + 26, cy + 34), (cx + 46, cy + 6)],
                 fill=(200, 208, 216), outline=INK, width=2)
    # windows
    for i in range(5):
        draw.ellipse([cx + 46 + i * 9, cy - 6, cx + 51 + i * 9, cy - 2],
                     fill=BLUE)


def draw_chip_art(draw, box):
    """A microchip with circuit traces."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(26, 34, 46))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # traces
    for gx in range(x0 + 16, x1 - 16, 28):
        draw.line([(gx, y0 + 6), (gx, y1 - 6)], fill=(60, 120, 90), width=2)
    for gy in range(y0 + 12, y1 - 12, 28):
        draw.line([(x0 + 6, gy), (x1 - 6, gy)], fill=(60, 120, 90), width=2)
    # chip body
    draw.rectangle([cx - 62, cy - 22, cx + 62, cy + 22], fill=(16, 22, 32),
                   outline=(120, 200, 160), width=2)
    draw.rectangle([cx - 40, cy - 13, cx + 40, cy + 13], fill=(52, 120, 84))
    draw.text((cx - 32, cy - 12), "AI", font=SANS_B(22), fill=(255, 255, 255))
    # pins
    for i in range(6):
        px = cx - 48 + i * 20
        draw.rectangle([px, cy - 30, px + 8, cy - 22], fill=(180, 190, 200))
        draw.rectangle([px, cy + 22, px + 8, cy + 30], fill=(180, 190, 200))


def draw_seoul_art(draw, box):
    """Government building with columns and a flag."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(228, 232, 238))
    cx = (x0 + x1) // 2
    # flag pole + flag
    draw.line([(x0 + 26, y0 + 8), (x0 + 26, y0 + 46)], fill=INK, width=3)
    draw.polygon([(x0 + 26, y0 + 8), (x0 + 64, y0 + 16), (x0 + 26, y0 + 26)],
                 fill=(205, 46, 58))
    draw.ellipse([x0 + 22, y0 + 4, x0 + 30, y0 + 12], fill=GOLD)
    # roof and building body
    draw.polygon([(x0 + 84, y0 + 26), (cx + 60, y0 + 8), (x1 - 10, y0 + 26)],
                 fill=STEEL, outline=INK, width=2)
    draw.rectangle([x0 + 90, y0 + 26, x1 - 16, y1 - 6], fill=(245, 244, 238),
                   outline=INK, width=2)
    for i in range(5):
        px = x0 + 106 + i * 34
        draw.rectangle([px, y0 + 34, px + 12, y1 - 14], fill=(200, 196, 182),
                       outline=INK, width=1)
    draw.rectangle([cx + 34, y1 - 14, cx + 82, y1 - 6], fill=STEEL)


def panel(draw, x, y, w, h, kicker_text, headline, body, art_fn):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    aw, ah = w - 20, 54
    art_fn(draw, (x + 10, y + 10, x + 10 + aw, y + 10 + ah))
    ty = kicker(draw, x + 10, y + 10 + ah + 6, kicker_text, size=16)
    ty = text_block(draw, x + 10, ty + 2, headline, SERIF_B(25), w - 20,
                    leading=29)
    text_block(draw, x + 10, ty + 4, body, SANS(16), w - 20, leading=21)


def render():
    """Draw the front page and return the PIL Image (no file written)."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 30  # margin
    # ---- masthead ----
    rule(d, m, 22, W - m, 3)
    d.text((m, 32), "THE WORLD TODAY", font=SERIF_B(84), fill=INK)
    rule(d, m, 126, W - m, 2)
    d.text((m, 136), "TUESDAY 24 NOVEMBER 2026", font=SANS_B(22), fill=RED)
    d.text((W - m - d.textlength("WORLD NEWS IN ONE PAGE", font=SANS_B(19)),
            138), "WORLD NEWS IN ONE PAGE", font=SANS_B(19), fill=INK)
    rule(d, m, 168, W - m, 3)

    # ---- lead story ----
    ly = 178
    kicker(d, m, ly, "Lead — Ukraine", size=16)
    y = text_block(d, m, ly + 26, "KYIV WARNS OF NEW RUSSIAN STRIKES",
                   SERIF_B(42), 560, leading=48)
    deck = ("President Volodymyr Zelenskiy says intelligence shows Moscow "
            "is preparing fresh attacks and urges the US and allies to speed "
            "up air defences.")
    text_block(d, m, y + 8, deck, SERIF(20), 560, leading=26)
    d.text((m, 400), "— Reuters, Kyiv", font=SANS(16), fill=STEEL)
    draw_lead_art(d, (620, 178, W - m, 408))
    d.text((620, 412), "Air defences on alert over Kyiv. (Illustration)",
           font=SANS(14), fill=STEEL)
    rule(d, m, 428, W - m, 2)

    # ---- four panels, 2 x 2 ----
    pw, ph = 467, 206
    gx, gy = m, 442
    gap = 30
    panel(d, gx, gy, pw, ph, "Russia · Estonia",
          "MOSCOW WARNS ESTONIA",
          "Russia accuses Estonia of hostile acts \u201con the verge of "
          "triggering open war\u201d. — Reuters",
          draw_estonia_art)
    panel(d, gx + pw + gap, gy, pw, ph, "NATO · Poland",
          "NATO WATCHES POLAND\u2019S SKIES",
          "NATO sends an AWACS early-warning jet to Poland after three "
          "Russian missiles landed there. — Reuters",
          draw_awacs_art)
    panel(d, gx, gy + ph + 12, pw, ph, "United States · Tech",
          "US TO BLACKLIST MEGASPEED",
          "Washington moves to blacklist the Singapore chip firm at the "
          "centre of the Nvidia scandal. — Reuters",
          draw_chip_art)
    panel(d, gx + pw + gap, gy + ph + 12, pw, ph, "South Korea",
          "SEOUL\u2019S SECURITY RESET",
          "President Lee Jae Myung names a new foreign minister and the "
          "country\u2019s first woman spy chief. — Reuters",
          draw_seoul_art)

    # ---- also today strip ----
    ay = 880
    rule(d, m, ay, W - m, 3)
    d.text((m, ay + 10), "ALSO TODAY", font=SANS_B(18), fill=RED)
    items = ("COP31 ends with no deal  \u2022  Iran vows to counter the US "
             "Hormuz blockade  \u2022  Democrats clinch a 258-seat US House "
             "majority  \u2022  49ers rout Vikings 35\u201310 in Mexico City  "
             "\u2022  BepiColombo enters orbit around Mercury")
    text_block(d, m, ay + 36, items, SANS(18), W - 2 * m, leading=24)
    d.text((m, H - 34), "Sources: Reuters, AP. Drawn with Python + PIL.",
           font=SANS(15), fill=STEEL)
    return img


def build():
    """Render the front page and save it as entry.png next to this file."""
    img = render()
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
