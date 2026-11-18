"""Build the news-image-20261117 front page (1024x1024 PNG, PIL only).

Layout: newspaper front page. Masthead + dateline, lead story with a drawn
bridge illustration, 2x2 grid of further stories, bottom ticker, footer.
All headline text is rendered with PIL so every letter is crisp.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 252, 247)
INK = (17, 17, 17)
RED = (158, 27, 27)
MUTED = (85, 85, 85)
NAVY = (31, 58, 95)
WATER = (120, 160, 200)
BAND = (240, 237, 228)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def spaced(text, n=1):
    return (" " * n).join(list(text))


def draw_bridge(draw, x0, y0, x1, y1):
    """Schematic island with a missile strike: sea, island, descending
    missile trail and an impact burst."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 240, 248))
    # sea
    for yy in range(y0 + 96, y1 - 6, 12):
        draw.line([x0 + 14, yy, x1 - 14, yy], fill=WATER, width=2)
    # island
    ix0, ix1 = x0 + 180, x1 - 180
    draw.polygon([(ix0, y1 - 8), (ix0 + 60, y0 + 62), (ix0 + 220, y0 + 52),
                  (ix0 + 330, y0 + 70), (ix1, y1 - 8)], fill=(96, 110, 88))
    # missile trail (descending from top right)
    mx, my = (x0 + x1) // 2 + 60, y0 + 58
    draw.line([x1 - 90, y0 + 6, mx + 26, my - 6], fill=INK, width=3)
    # missile body
    draw.polygon([(mx, my - 14), (mx + 30, my - 4), (mx, my + 6), (mx - 6, my - 4)], fill=INK)
    # impact burst (orange star)
    bx, by = (x0 + x1) // 2 + 30, y0 + 62
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 26, 10
        a1 = math.radians(ang)
        a2 = math.radians(ang + 15)
        draw.polygon([(bx, by),
                      (bx + r1 * math.cos(a1), by + r1 * math.sin(a1)),
                      (bx + r2 * math.cos(a2), by + r2 * math.sin(a2))],
                     fill=(214, 110, 30))
    draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(158, 27, 27))


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # frame
    d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=4)
    # masthead
    f_mast = font(SERIF_B, 66)
    t = "THE WORLD TODAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 26), t, font=f_mast, fill=INK)
    d.line([28, 108, W - 28, 108], fill=INK, width=3)
    # dateline
    f_date = font(SANS_B, 26)
    t = spaced("WEDNESDAY 18 NOVEMBER 2026")
    d.text(((W - d.textlength(t, font=f_date)) / 2, 118), t, font=f_date, fill=RED)
    f_note = font(SERIF, 20)
    t = "Every story below happened, or was first reported, on this day."
    d.text(((W - d.textlength(t, font=f_note)) / 2, 152), t, font=f_note, fill=MUTED)
    d.line([28, 184, W - 28, 184], fill=INK, width=2)

    # ---- lead story ----
    y = 198
    f_kick = font(SANS_B, 19)
    d.text((36, y), spaced("U.S.  •  IRAN  —  LEAD STORY", 1), font=f_kick, fill=RED)
    y += 30
    f_head = font(SERIF_B, 45)
    for line in wrap(d, "US strikes Iranian missile site on Qeshm Island", f_head, W - 72):
        d.text((36, y), line, font=f_head, fill=INK)
        y += 52
    f_sub = font(SANS, 23)
    for line in wrap(d, "Iran fires drones at Bahrain and Kuwait as the Gulf crisis deepens.", f_sub, W - 72):
        d.text((36, y), line, font=f_sub, fill=MUTED)
        y += 30
    draw_bridge(d, 36, y + 4, W - 36, y + 128)

    # ---- grid ----
    gy = y + 140
    stories = [
        ("UKRAINE", "Kerch Bridge hit for a second day",
         "A road span partly collapses into the strait."),
        ("SUMMIT", "Trump, Xi and Putin to meet Thursday in Shenzhen",
         "The APEC summit puts three leaders at one table."),
        ("HEALTH", "Ebola surges in DR Congo: 11,000 cases",
         "5,400 dead; three in four infected children under five die."),
        ("UNITED STATES", "Democrat Peltola wins Alaska Senate seat",
         "Democrats take 56 seats in the US Senate."),
    ]
    col_w = (W - 72 - 24) // 2
    row_h = 196
    f_gkick = font(SANS_B, 17)
    f_ghead = font(SERIF_B, 27)
    f_gsub = font(SANS, 19)
    for i, (kick, head, sub) in enumerate(stories):
        cx = 36 + (i % 2) * (col_w + 24)
        cy = gy + (i // 2) * row_h
        d.line([cx, cy, cx + col_w, cy], fill=INK, width=2)
        d.text((cx, cy + 8), spaced(kick, 1), font=f_gkick, fill=RED)
        yy = cy + 34
        for line in wrap(d, head, f_ghead, col_w)[:2]:
            d.text((cx, yy), line, font=f_ghead, fill=INK)
            yy += 32
        for line in wrap(d, sub, f_gsub, col_w)[:2]:
            d.text((cx, yy), line, font=f_gsub, fill=MUTED)
            yy += 24

    # ---- ticker (two lines) ----
    ty = gy + 2 * row_h + 8
    d.rectangle([28, ty, W - 28, ty + 48], fill=BAND)
    f_tick = font(SANS_B, 16)
    t1 = "ALSO:  Cyclone Xavier slams Cook Islands  •  North Korea test-fires missile"
    t2 = "GTA VI launches at midnight  •  6.0 quake in Papua New Guinea"
    d.text((36, ty + 7), t1, font=f_tick, fill=INK)
    d.text((36, ty + 26), t2, font=f_tick, fill=INK)
    # footer
    f_foot = font(SANS, 16)
    t = "Compiled from wire reports — BBC • Reuters • Al Jazeera"
    d.text(((W - d.textlength(t, font=f_foot)) / 2, H - 44), t, font=f_foot, fill=MUTED)

    img.save(path, "PNG", optimize=True)
    print("saved", path)


if __name__ == "__main__":
    build("entry.png")
