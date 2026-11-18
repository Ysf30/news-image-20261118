"""Build the news-image-20261118 v2 front page (1024x1024 PNG, PIL only).

Dense newspaper front page: masthead + dateline, illustrated lead story,
a world-map strip with story dots, a "day in figures" band, a 3x10 grid of
30 short stories (31 stories + 4 ticker items in total), ticker footer.
All text is rendered with PIL so every letter is crisp. Deterministic:
same bytes on every run.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 252, 247)
INK = (17, 17, 17)
RED = (158, 27, 27)
MUTED = (85, 85, 85)
NAVY = (31, 58, 95)
WATER = (120, 160, 200)
BAND = (240, 237, 228)
MAPBG = (232, 240, 248)
LAND = (110, 128, 145)

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


def draw_island(d, x0, y0, x1, y1):
    """Compact schematic island with a missile strike: sea, island,
    descending missile trail and an impact burst."""
    d.rectangle([x0, y0, x1, y1], fill=MAPBG)
    for yy in range(y0 + 56, y1 - 4, 9):
        d.line([x0 + 12, yy, x1 - 12, yy], fill=WATER, width=2)
    ix0, ix1 = x0 + 180, x1 - 180
    d.polygon([(ix0, y1 - 4), (ix0 + 60, y0 + 40), (ix0 + 220, y0 + 34),
               (ix0 + 330, y0 + 44), (ix1, y1 - 4)], fill=(96, 110, 88))
    mx, my = (x0 + x1) // 2 + 60, y0 + 38
    d.line([x1 - 90, y0 + 4, mx + 26, my - 4], fill=INK, width=3)
    d.polygon([(mx, my - 12), (mx + 28, my - 3), (mx, my + 5), (mx - 5, my - 3)],
              fill=INK)
    bx, by = (x0 + x1) // 2 + 30, y0 + 40
    for ang in range(0, 360, 30):
        r1, r2 = 22, 9
        a1 = math.radians(ang)
        a2 = math.radians(ang + 15)
        d.polygon([(bx, by),
                   (bx + r1 * math.cos(a1), by + r1 * math.sin(a1)),
                   (bx + r2 * math.cos(a2), by + r2 * math.sin(a2))],
                  fill=(214, 110, 30))
    d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=(158, 27, 27))


# ---- world map: coarse continent polygons in (lon, lat) ----
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-80, 73),
     (-70, 62), (-60, 47), (-75, 35), (-80, 25), (-90, 20), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-145, 60), (-165, 60)],
    [(-80, 10), (-75, 5), (-60, -5), (-50, -5), (-40, -20), (-48, -28),
     (-58, -35), (-65, -45), (-70, -55), (-73, -40), (-80, -20), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (48, 10), (40, -5), (35, -20), (30, -35), (20, -35),
     (15, -20), (12, -5), (9, 4), (-8, 5), (-15, 10)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 58), (10, 57), (18, 56),
     (21, 54), (28, 45), (23, 40), (19, 42), (12, 44), (3, 43), (-2, 37)],
    [(30, 36), (35, 42), (45, 40), (50, 45), (60, 50), (70, 55), (80, 60),
     (90, 65), (100, 70), (110, 75), (130, 72), (150, 70), (160, 60),
     (155, 50), (140, 40), (130, 35), (120, 30), (110, 20), (105, 10),
     (100, 8), (95, 15), (90, 22), (85, 20), (80, 15), (75, 8), (70, 20),
     (60, 25), (55, 26), (50, 30), (45, 28), (40, 32), (35, 36)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (150, -27),
     (146, -20), (142, -15), (140, -12), (135, -12), (130, -13), (125, -14),
     (120, -20), (114, -22)],
]
LABELS = [
    ("N. AMERICA", -100, 56), ("S. AMERICA", -60, -14), ("EUROPE", 14, 60),
    ("AFRICA", 28, -8), ("ASIA", 88, 56), ("OCEANIA", 134, -24),
]
DOTS = [
    (56.3, 26.9), (50.6, 26.2), (47.5, 29.3), (36.4, 45.3), (114.1, 22.5),
    (15.3, -4.3), (-150, 64), (147, -6.3), (-160, -21.2), (125.8, 39),
    (121, 14.6), (34.5, 31.5),
]


def draw_map(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=MAPBG)

    def proj(lon, lat):
        x = x0 + (lon + 170) / 360.0 * (x1 - x0)
        y = y0 + (75 - lat) / 130.0 * (y1 - y0)
        return (x, y)
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND)
    f_lab = font(SANS_B, 9)
    for text, lon, lat in LABELS:
        x, y = proj(lon, lat)
        d.text((x - d.textlength(text, font=f_lab) / 2, y - 5), text,
               font=f_lab, fill=(70, 70, 70))
    for lon, lat in DOTS:
        x, y = proj(lon, lat)
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=RED,
                  outline=(255, 255, 255), width=1)


LEAD_KICK = "U.S.  •  IRAN  —  LEAD STORY"
LEAD_HEAD = "US strikes Iranian missile site on Qeshm Island"
LEAD_SUB = "Iran fires drones at Bahrain and Kuwait as the Gulf crisis deepens."

FIGURES = [
    ("11,000+", "Ebola cases in DR Congo; 5,400 dead"),
    ("56", "Democrats' seats in the US Senate"),
    ("6.0", "magnitude of the Papua New Guinea quake"),
    ("-1.62%", "CAC 40 as markets slide worldwide"),
]

GRID = [
    ("GULF", "Iran fires drones at Bahrain and Kuwait"),
    ("UKRAINE", "Kerch Bridge hit for a second day"),
    ("SUMMIT", "Trump, Xi and Putin to meet Thursday"),
    ("HEALTH", "Ebola in DR Congo: 11,000 cases, 5,400 dead"),
    ("UNITED STATES", "Peltola wins Alaska; Democrats take 56 seats"),
    ("WEATHER", "Cyclone Xavier slams Northern Cook Islands"),
    ("NORTH KOREA", "Pyongyang test-fires missile into Sea of Japan"),
    ("GAMING", "GTA VI launches at midnight on Thursday"),
    ("EARTHQUAKE", "6.0 quake hits Papua New Guinea"),
    ("UKRAINE", "Zelenskyy in virtual talks with US envoys"),
    ("ISRAEL", "Knesset sworn in; Eisenkot to form government"),
    ("GAZA", "Cold kills displaced in tents; one meal in two days"),
    ("UNITED STATES", "Computer outages hit NSA and Apple"),
    ("MARKETS", "Stocks slide worldwide; VIX jumps 11%"),
    ("VENEZUELA", "US details $12bn in Venezuelan oil revenue"),
    ("FRANCE", "Fourth weekend of protests over living costs"),
    ("GAZA", "NGO: 1,100 child amputees denied treatment"),
    ("EUROPE", "Cyber-attack disables supermarket freezers"),
    ("JUSTICE", "World Court to rule on Myanmar genocide case"),
    ("U.S. – IRAN", "Trump takes Iran dirty-bomb report seriously"),
    ("ASIA", "Trump meets Philippines and Quad partners"),
    ("APEC", "APEC opens in Shenzhen; Xi urges open trade"),
    ("MARKETS", "Anthropic IPO price due; Nasdaq debut Thursday"),
    ("AI", "OpenAI launches GPT-6.2, claims it beats Claude"),
    ("CULTURE", "Bezos 'heavily involved' in casting new 007"),
    ("MARKETS", "Nvidia's first results since Huang resignation"),
    ("TECH", "Waymo pulls driverless taxis from US freeways"),
    ("SCIENCE", "Electric comb 'restores hair nearly 100%'"),
    ("HEALTH", "Viagra-like pill may slow Alzheimer's"),
    ("UKRAINE", "UN: 372 civilians killed in Ukraine in October"),
]

TICKER = ("ALSO:  MS Dhoni retires from IPL, to mentor CSK  •  "
          "Australia v England ODI decider in Hobart  •  "
          "Critical Java flaw found through AI  •  "
          "Oregon sues OpenAI over child safety")


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=4)

    # masthead + dateline
    f_mast = font(SERIF_B, 54)
    t = "THE WORLD TODAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 22), t, font=f_mast, fill=INK)
    d.line([28, 92, W - 28, 92], fill=INK, width=3)
    f_date = font(SANS_B, 22)
    t = spaced("WEDNESDAY 18 NOVEMBER 2026")
    d.text(((W - d.textlength(t, font=f_date)) / 2, 100), t, font=f_date, fill=RED)
    f_note = font(SERIF, 16)
    t = "Every story below happened, or was first reported, on this day."
    d.text(((W - d.textlength(t, font=f_note)) / 2, 128), t, font=f_note, fill=MUTED)
    d.line([28, 152, W - 28, 152], fill=INK, width=2)

    # ---- lead story ----
    y = 160
    f_kick = font(SANS_B, 16)
    d.text((36, y), spaced(LEAD_KICK, 1), font=f_kick, fill=RED)
    y += 24
    f_head = font(SERIF_B, 36)
    for line in wrap(d, LEAD_HEAD, f_head, W - 72)[:2]:
        d.text((36, y), line, font=f_head, fill=INK)
        y += 42
    f_sub = font(SANS, 18)
    for line in wrap(d, LEAD_SUB, f_sub, W - 72)[:2]:
        d.text((36, y), line, font=f_sub, fill=MUTED)
        y += 24
    draw_island(d, 36, y + 6, W - 36, y + 124)
    y += 130

    # ---- world map strip ----
    draw_map(d, 36, y, W - 36, y + 52)
    y += 60

    # ---- day in figures ----
    d.line([28, y, W - 28, y], fill=INK, width=2)
    f_num = font(SERIF_B, 23)
    f_lab = font(SANS, 11)
    col_w = (W - 72) // 4
    for i, (num, lab) in enumerate(FIGURES):
        cx = 36 + i * col_w
        nw = d.textlength(num, font=f_num)
        d.text((cx + (col_w - nw) / 2, y + 5), num, font=f_num, fill=INK)
        for j, line in enumerate(wrap(d, lab, f_lab, col_w - 12)[:1]):
            lw = d.textlength(line, font=f_lab)
            d.text((cx + (col_w - lw) / 2, y + 32), line, font=f_lab, fill=MUTED)
    y += 48
    d.line([28, y, W - 28, y], fill=INK, width=1)

    # ---- dense grid: 3 columns x 10 rows ----
    y += 8
    col_w = (W - 72 - 32) // 3
    row_h = 46
    f_gkick = font(SANS_B, 10)
    f_ghead = font(SERIF_B, 15)
    for i, (kick, head) in enumerate(GRID):
        cx = 36 + (i % 3) * (col_w + 16)
        cy = y + (i // 3) * row_h
        d.line([cx, cy, cx + col_w, cy], fill=(170, 170, 170), width=1)
        d.text((cx, cy + 3), spaced(kick, 1), font=f_gkick, fill=RED)
        yy = cy + 14
        for line in wrap(d, head, f_ghead, col_w)[:2]:
            d.text((cx, yy), line, font=f_ghead, fill=INK)
            yy += 17
    y += 10 * row_h

    # ---- ticker ----
    ty = y + 8
    d.rectangle([28, ty, W - 28, ty + 38], fill=BAND)
    f_tick = font(SANS_B, 14)
    lines = wrap(d, TICKER, f_tick, W - 72)[:2]
    for j, line in enumerate(lines):
        d.text((36, ty + 4 + j * 17), line, font=f_tick, fill=INK)
    y = ty + 38
    assert y <= 1006, f"layout overflow: ends at {y}"
    print("layout ends at", y, "stories:", 1 + len(GRID), "+ ticker")

    img.save(path, "PNG", optimize=True)
    print("saved", path)


if __name__ == "__main__":
    build("entry.png")
