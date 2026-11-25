#!/usr/bin/env python3
"""Draw the news-image-20261125 entry: a one-day newspaper front page.

Renders a 1024x1024 PNG summing up Wednesday 25 November 2026: a lead
story from Cartagena plus five more from around the world. Build-time
only, drawn with PIL + DejaVu fonts; the graded program (main.py) merely
copies the finished image. Fully deterministic: same input, same bytes.

Stories checked 25 Nov 2026 against Reuters, Xinhua, OneTurn and
Horizon roundups of the day: the Cartagena supermarket siege, the
Houthi strike on Riyadh's tallest tower, the Asian tech sell-off,
Shenzhou-24 launching and docking with Tiangong, miners trapped in a
flooded Indonesian mine, and Senegal getting the Africa Cup title back.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 238)
INK = (24, 24, 24)
MUTED = (92, 88, 80)
RED = (178, 34, 24)
NAVY = (28, 52, 88)
GREEN = (28, 122, 48)
AMBER = (176, 84, 10)
PURPLE = (88, 34, 178)
ORANGE = (190, 64, 12)
TEAL = (14, 116, 108)
RULE = (198, 190, 172)
WHITE = (250, 246, 238)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


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


def fit_font(draw, text, path, start, max_w):
    size = start
    while size > 12 and draw.textlength(text, font=font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def centre(draw, cx, y, text, fnt, fill):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


# ---------------------------------------------------------------- icons
def icon_store(d, x, y, s, fg, bg):
    # sign board on top, awning, shop front with door and windows
    d.rectangle([x + s * 0.14, y + s * 0.12, x + s * 0.86, y + s * 0.22], fill=fg)
    d.polygon([(x + s * 0.06, y + s * 0.30), (x + s * 0.94, y + s * 0.30),
               (x + s * 0.86, y + s * 0.46), (x + s * 0.14, y + s * 0.46)], fill=fg)
    d.rectangle([x + s * 0.14, y + s * 0.46, x + s * 0.86, y + s * 0.88], fill=fg)
    d.rectangle([x + s * 0.42, y + s * 0.62, x + s * 0.58, y + s * 0.88], fill=bg)
    d.rectangle([x + s * 0.20, y + s * 0.56, x + s * 0.34, y + s * 0.72], fill=bg)
    d.rectangle([x + s * 0.66, y + s * 0.56, x + s * 0.80, y + s * 0.72], fill=bg)


def icon_tower(d, x, y, s, fg, bg):
    # tapered tower, antenna, starburst where the strike hits
    d.polygon([(x + s * 0.42, y + s * 0.34), (x + s * 0.58, y + s * 0.34),
               (x + s * 0.64, y + s * 0.88), (x + s * 0.36, y + s * 0.88)], fill=fg)
    d.line([(x + s * 0.50, y + s * 0.34), (x + s * 0.50, y + s * 0.18)],
           fill=fg, width=5)
    cx, cy = x + s * 0.50, y + s * 0.10
    for dx, dy in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)):
        d.line([(cx, cy), (cx + dx * s * 0.10, cy + dy * s * 0.10)],
               fill=fg, width=5)
    for wy in (0.46, 0.60, 0.74):
        d.rectangle([x + s * 0.44, y + s * wy, x + s * 0.56, y + s * wy + 6],
                    fill=bg)


def icon_chart(d, x, y, s, fg, bg):
    # four falling bars and a downward arrow: a market sell-off
    bw = s * 0.14
    for i, h in enumerate((0.62, 0.50, 0.42, 0.26)):
        bx = x + s * 0.12 + i * s * 0.20
        d.rectangle([bx, y + s * 0.86 - s * h, bx + bw, y + s * 0.86], fill=fg)
    d.line([(x + s * 0.10, y + s * 0.14), (x + s * 0.38, y + s * 0.28),
            (x + s * 0.55, y + s * 0.24), (x + s * 0.88, y + s * 0.46)],
           fill=fg, width=6)
    d.polygon([(x + s * 0.88, y + s * 0.46), (x + s * 0.70, y + s * 0.40),
               (x + s * 0.84, y + s * 0.28)], fill=fg)


def icon_rocket(d, x, y, s, fg, bg):
    # nose, body, window, fins, flame
    d.polygon([(x + s * 0.50, y + s * 0.06), (x + s * 0.64, y + s * 0.26),
               (x + s * 0.36, y + s * 0.26)], fill=fg)
    d.rectangle([x + s * 0.36, y + s * 0.26, x + s * 0.64, y + s * 0.62], fill=fg)
    d.ellipse([x + s * 0.43, y + s * 0.32, x + s * 0.57, y + s * 0.46], fill=bg)
    d.polygon([(x + s * 0.36, y + s * 0.52), (x + s * 0.16, y + s * 0.76),
               (x + s * 0.36, y + s * 0.68)], fill=fg)
    d.polygon([(x + s * 0.64, y + s * 0.52), (x + s * 0.84, y + s * 0.76),
               (x + s * 0.64, y + s * 0.68)], fill=fg)
    d.polygon([(x + s * 0.42, y + s * 0.62), (x + s * 0.58, y + s * 0.62),
               (x + s * 0.50, y + s * 0.92)], fill=fg)


def icon_helmet(d, x, y, s, fg, bg):
    # miner's hard hat: dome, ridge, brim, headlamp
    d.pieslice([x + s * 0.18, y + s * 0.20, x + s * 0.82, y + s * 0.80],
               180, 360, fill=fg)
    d.rectangle([x + s * 0.46, y + s * 0.16, x + s * 0.54, y + s * 0.72], fill=fg)
    d.rectangle([x + s * 0.10, y + s * 0.70, x + s * 0.90, y + s * 0.80], fill=fg)
    d.ellipse([x + s * 0.44, y + s * 0.40, x + s * 0.56, y + s * 0.52], fill=bg)


def icon_trophy(d, x, y, s, fg, bg):
    # cup with handles, stem and base
    d.polygon([(x + s * 0.24, y + s * 0.14), (x + s * 0.76, y + s * 0.14),
               (x + s * 0.68, y + s * 0.52), (x + s * 0.32, y + s * 0.52)], fill=fg)
    d.arc([x + s * 0.06, y + s * 0.16, x + s * 0.30, y + s * 0.44],
          90, 270, fill=fg, width=6)
    d.arc([x + s * 0.70, y + s * 0.16, x + s * 0.94, y + s * 0.44],
          270, 90, fill=fg, width=6)
    d.rectangle([x + s * 0.45, y + s * 0.52, x + s * 0.55, y + s * 0.70], fill=fg)
    d.rectangle([x + s * 0.32, y + s * 0.70, x + s * 0.68, y + s * 0.80], fill=fg)
    d.ellipse([x + s * 0.45, y + s * 0.26, x + s * 0.55, y + s * 0.36], fill=bg)


ICONS = {
    "store": icon_store, "tower": icon_tower, "chart": icon_chart,
    "rocket": icon_rocket, "helmet": icon_helmet, "trophy": icon_trophy,
}

# kicker, colour, icon, headline, summary
STORIES = [
    ("CONFLICT", PURPLE, "tower",
     "Houthi strike hits Riyadh's tallest tower",
     "Eleven wounded in a strike on the capital's tallest tower."),
    ("MARKETS", GREEN, "chart",
     "Asian tech stocks slide as AI rally fades",
     "Japan's Nikkei falls 2.8% in a broad sell-off; Nvidia down 7%."),
    ("SPACE", TEAL, "rocket",
     "Shenzhou-24 launches and docks with Tiangong",
     "Shenzhou-24 docks with Tiangong; first foreign astronaut aboard."),
    ("DISASTER", ORANGE, "helmet",
     "Rescuers race to reach dozens trapped in mine",
     "Rains flood a 100-metre-deep mine; dozens of miners trapped."),
    ("SPORT", AMBER, "trophy",
     "Senegal gets Africa Cup title back",
     "CAS hands the 2025 Africa Cup title back to Senegal."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead: navy band + red rule + date ----
    d.rectangle([0, 0, W, 104], fill=NAVY)
    centre(d, W // 2, 24, "THE WORLD IN ONE DAY", font(SERIF_B, 56), WHITE)
    d.line([(48, 118), (W - 48, 118)], fill=RED, width=4)
    centre(d, W // 2, 132, "W E D N E S D A Y  ·  2 5  N O V E M B E R  2 0 2 6",
           font(SANS_B, 28), RED)

    # ---- lead story: Cartagena supermarket siege ----
    ly = 182
    d.rectangle([48, ly, 256, ly + 200], fill=RED)
    icon_store(d, 48, ly, 208, WHITE, RED)
    tx = 284
    d.text((tx, ly + 4), "COLOMBIA  ·  CARTAGENA", font=font(SANS_B, 20), fill=NAVY)
    headline = "All 20 hostages freed in Cartagena supermarket siege"
    hl = wrap(d, headline, font(SANS_B, 38), W - 48 - tx)
    yy = ly + 38
    for line in hl:
        d.text((tx, yy), line, font=font(SANS_B, 38), fill=INK)
        yy += 46
    summary = ("Armed men held shoppers in a supermarket; the standoff ends "
               "with every hostage freed unharmed.")
    sl = wrap(d, summary, font(SANS, 23), W - 48 - tx)
    yy += 8
    for line in sl:
        d.text((tx, yy), line, font=font(SANS, 23), fill=MUTED)
        yy += 30

    # ---- divider + section label ----
    d.line([(48, 400), (W - 48, 400)], fill=RULE, width=2)
    centre(d, W // 2, 412, "ALSO ON THIS DAY", font(SANS_B, 20), MUTED)

    # ---- five story strips ----
    y = 452
    for kicker, color, icon, headline, summary in STORIES:
        d.rectangle([48, y, 48 + 84, y + 84], fill=color)
        ICONS[icon](d, 48, y, 84, WHITE, color)
        tx = 152
        d.text((tx, y + 2), kicker, font=font(SANS_B, 18), fill=color)
        hfnt = fit_font(d, headline, SANS_B, 26, W - 48 - tx)
        d.text((tx, y + 26), headline, font=hfnt, fill=INK)
        d.text((tx, y + 58), summary, font=font(SANS, 21), fill=MUTED)
        y += 104

    # ---- footer ----
    fy = 972
    d.line([(48, fy), (W - 48, fy)], fill=RED, width=3)
    centre(d, W // 2, fy + 12,
           "25 NOVEMBER 2026  ·  SIX STORIES THAT DEFINED THE DAY",
           font(SANS_B, 18), MUTED)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
