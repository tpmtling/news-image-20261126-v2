#!/usr/bin/env python3
"""Render the front page for THE WORLD TODAY - Thursday 26 November 2026.

Hand-drawn with Pillow: masthead, lead story (US tariff proposals) with a
rate chart, two middle stories (Pyongyang / Shenzhou-24), three briefs,
and a footer ticker. Deterministic: no timestamps, no randomness.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (22, 21, 19)
RED = (166, 28, 28)
NAVY = (31, 58, 95)
GOLD = (184, 141, 52)
GREY = (96, 92, 86)
LIGHT = (233, 227, 214)

FD = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FDB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, text, fnt, fill=INK, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def rule(draw, y, x0, x1, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
rule(d, 14, 32, 992, width=4)
center(d, 26, "THE WORLD TODAY", font(FDB, 74), INK)
center(d, 104, "THURSDAY  26  NOVEMBER  2026", font(FDB, 27), RED)
rule(d, 140, 32, 992, width=2)
center(d, 148, "ONE DAY  ·  ONE PAGE  ·  THE WORLD IN BRIEF",
       font(FD, 17), GREY)
rule(d, 176, 32, 992, width=4)

# ---------- lead story: tariffs ----------
d.text((32, 196), "TRADE  ·  WASHINGTON", font=font(FDB, 20), fill=RED)
d.text((32, 224), "TRUMP'S NEW", font=font(FDB, 66), fill=INK)
d.text((32, 292), "TARIFF WALL", font=font(FDB, 66), fill=INK)
deck = ("US proposes duties of up to 25% on India \u2014 and 40% "
        "on China \u2014 in a Section 301 crackdown on \u201cexcess capacity\u201d "
        "across 14 economies.")
for i, line in enumerate(wrap(d, deck, font(FD, 22), 560)):
    d.text((32, 372 + i * 30), line, font=font(FD, 22), fill=INK)

# rate chart, right of the deck
cx0, cy0 = 620, 232
d.text((cx0, 200), "PROPOSED TOP RATES", font=font(FDB, 18), fill=NAVY)
bars = [("CHINA", 40, RED), ("VIETNAM", 35, NAVY), ("INDIA", 25, NAVY)]
for i, (name, val, col) in enumerate(bars):
    y = cy0 + i * 62
    d.text((cx0, y), name, font=font(FDB, 20), fill=INK)
    d.text((cx0 + 118, y), f"{val}%", font=font(FDB, 20), fill=col)
    d.rectangle([cx0 + 168, y + 4, cx0 + 168 + val * 4.4, y + 24], fill=col)
d.text((cx0, cy0 + 3 * 62 - 14),
       "EU, Japan and others face 15\u201320%.\nIndia's rate falls to 17% with a deal.",
       font=font(FD, 16), fill=GREY)

rule(d, 470, 32, 992, width=2)

# ---------- middle row: two stories ----------
# left: Pyongyang
d.text((32, 492), "DIPLOMACY  ·  PYONGYANG", font=font(FDB, 18), fill=RED)
d.text((32, 518), "NORTH KOREA SHUTS", font=font(FDB, 34), fill=INK)
d.text((32, 556), "SWISS OFFICE", font=font(FDB, 34), fill=INK)
body1 = ("Pyongyang orders Switzerland's diplomatic office closed and its "
         "envoy out within 48 hours, weeks after it reopened, in a row over "
         "sanctions on a children's camp.")
for i, line in enumerate(wrap(d, body1, font(FD, 19), 420)):
    d.text((32, 604 + i * 26), line, font=font(FD, 19), fill=INK)
# small drawing: flag pole with Swiss cross, clear of the text
d.line([(472, 628), (472, 700)], fill=INK, width=4)
d.rectangle([472, 628, 510, 668], fill=RED)
d.rectangle([486, 636, 496, 660], fill=(255, 255, 255))
d.rectangle([478, 644, 504, 654], fill=(255, 255, 255))
_t48 = "48 HOURS"
_f48 = font(FDB, 15)
d.text((508 - d.textlength(_t48, font=_f48), 706), _t48, font=_f48, fill=RED)

# divider
d.line([(512, 492), (512, 736)], fill=GREY, width=1)

# right: Shenzhou-24
d.text((544, 492), "SPACE  ·  TIANGONG", font=font(FDB, 18), fill=RED)
d.text((544, 518), "FIRST PAKISTANI", font=font(FDB, 34), fill=INK)
d.text((544, 556), "IN ORBIT", font=font(FDB, 34), fill=INK)
body2 = ("Shenzhou-24 carries Muhammad Zeeshan Ali to China's Tiangong "
         "station \u2014 the first foreign crew member to fly there.")
for i, line in enumerate(wrap(d, body2, font(FD, 19), 300)):
    d.text((544, 604 + i * 26), line, font=font(FD, 19), fill=INK)
# small drawing: rocket
rx, ry = 880, 600
d.polygon([(rx, ry), (rx - 16, ry + 62), (rx + 16, ry + 62)], fill=NAVY)
d.ellipse([rx - 16, ry + 52, rx + 16, ry + 84], fill=NAVY)
d.polygon([(rx - 16, ry + 56), (rx - 30, ry + 84), (rx - 12, ry + 74)],
          fill=RED)
d.polygon([(rx + 16, ry + 56), (rx + 30, ry + 84), (rx + 12, ry + 74)],
          fill=RED)
d.polygon([(rx - 7, ry + 84), (rx + 7, ry + 84), (rx, ry + 106)], fill=(232, 122, 26))
d.ellipse([rx - 5, ry + 22, rx + 5, ry + 32], fill=PAPER)
for sx, sy in [(856, 612), (930, 640), (866, 690), (940, 700)]:
    d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)

rule(d, 748, 32, 992, width=2)

# ---------- bottom strip: three briefs ----------
cols = [
    ("BANGLADESH", "PAY RISES 36%",
     "Garment workers win a 36% minimum-wage rise after weeks of protests."),
    ("COLOMBIA", "20 HOSTAGES FREED",
     "Police storm a supermarket and free 20 people held for 17 hours."),
    ("CANARY ISLANDS", "RECORD ARRIVALS",
     "Nearly 2,000 migrants reach Spain's Canary Islands in a single day."),
]
for i, (kick, head, body) in enumerate(cols):
    x = 32 + i * 322
    d.text((x, 770), kick, font=font(FDB, 17), fill=RED)
    for j, line in enumerate(wrap(d, head, font(FDB, 24), 300)):
        d.text((x, 794 + j * 30), line, font=font(FDB, 24), fill=INK)
    for j, line in enumerate(wrap(d, body, font(FD, 18), 300)):
        d.text((x, 852 + j * 25), line, font=font(FD, 18), fill=INK)
    if i < 2:
        d.line([(x + 308, 770), (x + 308, 930)], fill=GREY, width=1)

# ---------- footer ticker ----------
rule(d, 950, 32, 992, width=2)
ticker = ("ALSO: Thanksgiving travellers face long airport lines and storms "
          "across the US  ·  1,220 players register for the IPL 2027 auction")
for i, line in enumerate(wrap(d, ticker, font(FD, 15), 960)):
    d.text((32, 962 + i * 21), line, font=font(FD, 15), fill=GREY)
center(d, 1000, "THE WORLD TODAY  ·  THURSDAY 26 NOVEMBER 2026  ·  PAGE 1",
       font(FDB, 14), GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
