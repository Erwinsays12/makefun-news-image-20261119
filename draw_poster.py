#!/usr/bin/env python3
"""Draw the news poster for Thursday 19 November 2026.

Renders a 1024x1024 newspaper-style front page with one lead story and
six further stories, all reported on 19 November 2026, using only Pillow
and the DejaVu fonts shipped with the system. Run:

    python3 draw_poster.py            # writes entry.png beside this file
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (12, 26, 43)
PANEL = (19, 39, 63)
PANEL_EDGE = (52, 79, 104)
GOLD = (233, 180, 76)
CREAM = (245, 239, 224)
MUTED = (159, 179, 200)
SKY = (96, 165, 250)
TEAL = (45, 212, 191)
PINK = (255, 94, 138)
VIOLET = (139, 92, 246)
ORANGE = (255, 122, 89)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width."""
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


def draw_sunset_scene(draw, x0, y0, x1, y1):
    """Vice City sunset: gradient sky, sun, skyline, palm, big VI."""
    top = (255, 122, 89)
    mid = (255, 94, 138)
    bottom = (62, 32, 96)
    height = y1 - y0
    for yy in range(y0, y1):
        t = (yy - y0) / max(1, height)
        if t < 0.55:
            a, b, u = top, mid, t / 0.55
        else:
            a, b, u = mid, bottom, (t - 0.55) / 0.45
        col = tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))
        draw.line([(x0, yy), (x1, yy)], fill=col)
    # Sun.
    cx, cy, r = (x0 + x1) // 2, y0 + 78, 52
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 130))
    # Skyline silhouettes.
    base = y1
    towers = [(0, 150), (46, 105), (96, 168), (150, 88), (196, 140),
              (238, 118), (282, 158), (322, 96)]
    for off, th in towers:
        tx0 = x0 + off
        tx1 = min(x1, tx0 + 44)
        draw.rectangle([tx0, base - th, tx1, base], fill=(24, 12, 44))
        for wy in range(base - th + 12, base - 10, 22):
            draw.rectangle([tx0 + 8, wy, tx0 + 14, wy + 8],
                           fill=(255, 214, 130))
    # Palm tree: leaning trunk, five drooping fronds as two-segment lines.
    import math
    px = x0 + 168
    top_x, top_y = px + 8, base - 96
    draw.line([(px, base), (top_x, top_y)], fill=(24, 12, 44), width=7)
    for ang in (-75, -40, -5, 30, 65):
        rad = math.radians(ang)
        mx = top_x + int(26 * math.cos(rad))
        my = top_y + int(14 * math.sin(rad)) - 8
        ex = top_x + int(52 * math.cos(rad))
        ey = top_y + int(30 * math.sin(rad)) + 16
        draw.line([(top_x, top_y), (mx, my), (ex, ey)], fill=(24, 12, 44),
                  width=5, joint="curve")
    # Big VI.
    vi = font(FONT_SERIF, 92)
    draw.text(((x0 + x1) // 2, y0 + 150), "VI", font=vi, fill=(255, 255, 255),
              anchor="mm", stroke_width=2, stroke_fill=(24, 12, 44))


def icon_capitol(draw, x, y, s, col):
    draw.polygon([(x + s // 2, y + 2), (x + s // 2 - 14, y + 16),
                  (x + s // 2 + 14, y + 16)], fill=col)
    draw.rectangle([x + s // 2 - 16, y + 16, x + s // 2 + 16, y + 22], fill=col)
    for i in range(5):
        cx = x + 6 + i * 9
        draw.rectangle([cx, y + 24, cx + 4, y + s - 4], fill=col)
    draw.rectangle([x + 2, y + s - 4, x + s - 2, y + s], fill=col)


def icon_summit(draw, x, y, s, col):
    import math
    for i, cx in enumerate((x + 10, x + s // 2, x + s - 10)):
        draw.ellipse([cx - 8, y + 6, cx + 8, y + 22], fill=col)
        draw.rectangle([cx - 2, y + 22, cx + 2, y + s - 12], fill=col)
    draw.ellipse([x + s // 2 - 6, y + 30, x + s // 2 + 6, y + 42],
                 fill=(255, 255, 255))
    draw.line([(x + 4, y + s - 10), (x + s - 4, y + s - 10)], fill=col,
              width=3)


def icon_cyclone(draw, x, y, s, col):
    import math
    cx, cy = x + s // 2, y + s // 2
    for k in range(3):
        r0 = 6 + k * 9
        draw.arc([cx - r0, cy - r0, cx + r0, cy + r0],
                 start=40 + k * 120, end=300 + k * 120, fill=col, width=4)


def icon_voyager(draw, x, y, s, col):
    draw.line([(x + 8, y + s - 8), (x + s - 8, y + 8)], fill=col, width=3)
    draw.polygon([(x + s - 18, y + 4), (x + s - 2, y + 4),
                  (x + s - 2, y + 20)], fill=col)
    draw.ellipse([x + 6, y + s - 22, x + 22, y + s - 6], fill=col)
    for sx, sy in ((x + 34, y + 6), (x + 44, y + 16), (x + 12, y + 12)):
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))


def icon_euro(draw, x, y, s, col):
    import math
    cx, cy = x + s // 2, y + s // 2
    for i in range(8):
        ang = math.radians(i * 45 - 90)
        sx = cx + int(19 * math.cos(ang))
        sy = cy + int(19 * math.sin(ang))
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)
    ef = font(FONT_BOLD, 26)
    draw.text((cx, cy), "\u20ac", font=ef, fill=col, anchor="mm")


def icon_globe(draw, x, y, s, col):
    cx, cy = x + s // 2, y + s // 2
    draw.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=col, width=3)
    draw.ellipse([cx - 7, y + 2, cx + 7, y + s - 2], outline=col, width=2)
    draw.line([(x + 2, cy), (x + s - 2, cy)], fill=col, width=2)
    draw.arc([x + 2, y + 10, x + s - 2, y + s - 10], start=200, end=340,
             fill=col, width=2)
    draw.text((x + s - 6, y + s - 8), "\u263e", font=font(FONT_BOLD, 18),
              fill=GOLD, anchor="rb")


STORIES = [
    ("SHENZHEN  •  DIPLOMACY", "THREE LEADERS, ONE TABLE",
     "Trump, Xi and Putin are set for a first trilateral meeting today "
     "in Shenzhen.",
     icon_summit, SKY),
    ("WASHINGTON  •  POLITICS", "JEFFRIES SET TO MAKE HISTORY",
     "Democrats nominate Hakeem Jeffries — poised to be the first Black "
     "Speaker.",
     icon_capitol, GOLD),
    ("INDIA  •  WEATHER", "CYCLONE AKVAN NEARS LAND",
     "The storm is set to cross India's east coast between Machilipatnam "
     "and Puri.",
     icon_cyclone, TEAL),
    ("SPACE  •  SCIENCE", "VOYAGER 1, A LIGHT-DAY AWAY",
     "After almost 50 years in flight, NASA's probe reaches a record "
     "distance from Earth.",
     icon_voyager, VIOLET),
    ("EUROPE  •  UKRAINE", "EU PLANS \u20ac45BN UKRAINE LOAN",
     "Brussels proposes a loan to Kyiv, to be repaid after Russia pays "
     "reparations.",
     icon_euro, SKY),
    ("WORLD  •  SOCIETY", "ISLAM TO BE LARGEST FAITH BY 2035",
     "A Pew Research projection reported today.",
     icon_globe, TEAL),
]


def draw_panel(draw, x0, y0, x1, y1, story):
    kicker, headline, body, icon, col = story
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=PANEL,
                           outline=PANEL_EDGE, width=2)
    ix, iy = x0 + 16, y0 + 14
    icon(draw, ix, iy, 46, col)
    kf = font(FONT_BOLD, 16)
    draw.text((ix + 58, iy + 23), kicker, font=kf, fill=GOLD, anchor="lm")
    hf = font(FONT_BOLD, 25)
    lines = wrap(draw, headline, hf, (x1 - x0) - 32)
    ty = y0 + 72
    for ln in lines[:2]:
        draw.text((x0 + 16, ty), ln, font=hf, fill=CREAM)
        ty += 30
    bf = font(FONT_REG, 18)
    blines = wrap(draw, body, bf, (x1 - x0) - 32)
    ty += 4
    for ln in blines[:3]:
        draw.text((x0 + 16, ty), ln, font=bf, fill=MUTED)
        ty += 23


def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Masthead.
    draw.text((W // 2, 34), "THE WORLD IN ONE DAY", font=font(FONT_BOLD, 22),
              fill=GOLD, anchor="mm")
    draw.text((W // 2, 88), "THURSDAY, 19 NOVEMBER 2026",
              font=font(FONT_SERIF, 46), fill=CREAM, anchor="mm")
    draw.line([(24, 132), (W - 24, 132)], fill=GOLD, width=3)

    # Lead story: GTA VI.
    lx0, ly0, lx1, ly1 = 24, 148, W - 24, 448
    draw.rounded_rectangle([lx0, ly0, lx1, ly1], radius=10, fill=PANEL,
                           outline=PANEL_EDGE, width=2)
    scene_x0 = lx1 - 372
    draw_sunset_scene(draw, scene_x0, ly0 + 2, lx1 - 2, ly1 - 2)
    draw.text((lx0 + 24, ly0 + 26), "CULTURE  •  GAMING  —  THE LEAD STORY",
              font=font(FONT_BOLD, 17), fill=GOLD)
    hf = font(FONT_BOLD, 46)
    ty = ly0 + 62
    for ln in wrap(draw, "VICE CITY OPENS ITS DOORS", hf, scene_x0 - lx0 - 48):
        draw.text((lx0 + 24, ty), ln, font=hf, fill=CREAM)
        ty += 54
    bf = font(FONT_REG, 21)
    ty += 8
    for ln in wrap(draw, "Grand Theft Auto VI begins its global rollout "
                   "today — after a 13-year wait, players return to Vice "
                   "City.", bf, scene_x0 - lx0 - 48)[:4]:
        draw.text((lx0 + 24, ty), ln, font=bf, fill=MUTED)
        ty += 28

    # Six story panels, 3 columns x 2 rows.
    cols, rows = 3, 2
    gap = 16
    pw = (W - 48 - gap * (cols - 1)) // cols
    ph = 246
    top = 464
    for i, story in enumerate(STORIES):
        c, r = i % cols, i // cols
        x0 = 24 + c * (pw + gap)
        y0 = top + r * (ph + gap)
        draw_panel(draw, x0, y0, x0 + pw, y0 + ph, story)

    # Footer.
    draw.line([(24, 988), (W - 24, 988)], fill=PANEL_EDGE, width=2)
    draw.text((W // 2, 1006),
              "All stories reported on 19 November 2026  •  AP, BBC, Reuters, "
              "NDTV, The Hindu, FT, Pew Research",
              font=font(FONT_REG, 15), fill=MUTED, anchor="mm")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
