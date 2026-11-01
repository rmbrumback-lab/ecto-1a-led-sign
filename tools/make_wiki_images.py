#!/usr/bin/env python3
"""Render build plans: a numbered 80x7 pixel map for every message (docs/plans/),
plus a plain-text pixel-map file builders can read without any software.

Each plan shows the message's frame(s) on a grid with column numbers (0-79) and
row numbers (0-6). Cell colors: red, green, amber (red + green both lit), off.
All images are our own renderings of the generator's frames; no film material.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ecto1a.generate import build_segments, to_panel, W, H, R, G, Y

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "plans")
os.makedirs(OUT, exist_ok=True)

BG = (250, 250, 248)
INK = (30, 30, 30)
GRID = (205, 205, 205)
FILL = {0: (236, 236, 232), 1: (220, 30, 30), 2: (30, 170, 40), 3: (240, 175, 0)}
CHAR = {0: ".", 1: "R", 2: "G", 3: "Y"}

# (segment id, frame index, caption): frames taken from the screen-timed ("full") build
PLANS = [
    ("A", "GHOSTBUSTERS", "Bold narrow font, spans columns 0-78",
     [(2, "red"), (13, "green")]),
    ("B", "FOR HIRE...", "Bold narrow font, red text, static green border", [(5, "")]),
    ("C", "WE'RE READY", "Thin 5x7 font; color and font UNCONFIRMED (shown amber)", [(2, "")]),
    ("D", "TO BELIEVE YOU", "Thin 5x7 font; highlight moves word by word (YOU's color inferred)",
     [(0, "all red"), (2, "TO green"), (4, "BELIEVE amber"), (6, "YOU green (inferred)")]),
    ("E", "CALL JL5-2020", "Thin 5x7 font, amber", [(0, "")]),
    ("F", "GHOSTBUSTERS (second)", "Green, then red", [(2, "green"), (16, "red")]),
    ("G", "WE'RE BACK", "Bold wide font, spans columns 0-79; words swap colors",
     [(2, "WE'RE red / BACK green"), (13, "swapped")]),
    ("G2", "Five lines -> boxes", "INFERRED reconstruction (5 x 16-column sections)",
     [(0, "red lines"), (2, "full red, dark dividers"), (4, "green, red dividers")]),
    ("H", "WHO YA", "Bold wide font, red (glyphs estimated)", [(0, "")]),
    ("I", "GONNA", "Bold wide font; color UNCONFIRMED (shown red)", [(0, "")]),
    ("J", "CALL?", "Bold wide font, red", [(0, "")]),
    ("K", "US!", "Bold wide, red word; green arrows point inward",
     [(0, "US! alone"), (3, "arrows on")]),
    ("L", "CALL JL5-2020 (second)", "Thin 5x7 font, amber; opens out from the center", [(2, "")]),
]


def font(size, bold=False):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else "")
    return ImageFont.truetype(p, size) if os.path.exists(p) else ImageFont.load_default()


def grid(frame, s=14, label=""):
    """One frame on a numbered grid."""
    left, top = 34, 26 + (18 if label else 0)
    im = Image.new("RGB", (left + W * s + 10, top + H * s + 8), BG)
    d = ImageDraw.Draw(im)
    f = font(10)
    if label:
        d.text((left, 4), label, fill=INK, font=font(13, True))
    for x in range(0, W, 5):
        d.text((left + x * s + 1, top - 15), str(x), fill=INK, font=f)
    for y in range(H):
        d.text((8, top + y * s + 1), str(y), fill=INK, font=f)
    for y in range(H):
        for x in range(W):
            x0, y0 = left + x * s, top + y * s
            d.rectangle([x0, y0, x0 + s - 1, y0 + s - 1], fill=FILL[frame[y][x]], outline=GRID)
    for x in range(0, W + 1, 10):  # heavier line every 10 columns
        d.line([left + x * s - 1, top, left + x * s - 1, top + H * s], fill=(120, 120, 120))
    return im


def legend(width):
    im = Image.new("RGB", (width, 28), BG)
    d = ImageDraw.Draw(im)
    x = 34
    for v, name in ((1, "red"), (2, "green"), (3, "amber = red + green"), (0, "off")):
        d.rectangle([x, 8, x + 13, 21], fill=FILL[v], outline=GRID)
        d.text((x + 19, 8), name, fill=INK, font=font(12))
        x += 40 + d.textlength(name, font=font(12))
    return im


def main():
    segs = {sid: fr for sid, _, fr in build_segments("full")}
    txt = ["Ecto-1A LED sign boards - pixel maps (80 columns x 7 rows)",
           "R = red, G = green, Y = amber (red + green both lit), . = off",
           "Column 0 is the left edge; row 0 is the top. The ruler marks every 10 columns (0, 10, 20 ... 70).",
           "Generated from https://github.com/rmbrumback-lab/ecto-1a-led-sign "
           "(MIT). Status of each message: see the wiki page / docs/ATTRIBUTION.md.", ""]
    for sid, name, cap, picks in PLANS:
        tiles = [grid(segs[sid][i], label=lab) for i, lab in picks]
        w = tiles[0].width
        head = Image.new("RGB", (w, 46), BG)
        d = ImageDraw.Draw(head)
        d.text((34, 6), f"{sid}  {name}", fill=INK, font=font(17, True))
        d.text((34, 28), cap, fill=(80, 80, 80), font=font(12))
        parts = [head] + tiles + [legend(w)]
        im = Image.new("RGB", (w, sum(p.height for p in parts)), BG)
        y = 0
        for p in parts:
            im.paste(p, (0, y)); y += p.height
        im.save(os.path.join(OUT, f"plan_{sid}.png"), optimize=True)
        for i, lab in picks:
            txt.append(f"== {sid} {name}" + (f" - {lab}" if lab else "") + f" ({cap})")
            txt.append("    " + "".join(str(x // 10) if x % 10 == 0 else " " for x in range(W)))
            for y_, row in enumerate(segs[sid][i]):
                txt.append(f"  {y_} " + "".join(CHAR[v] for v in row))
            txt.append("")
    with open(os.path.join(OUT, "ecto1a_pixel_maps.txt"), "w") as fh:
        fh.write("\n".join(txt))

    # Panel mapping: how one sign row becomes two panel rows, green half a pixel lower
    s = 22
    im = Image.new("RGB", (560, 330), BG)
    d = ImageDraw.Draw(im)
    d.text((14, 8), "Sign pixel -> 16-row panel mapping (green sits half a pixel lower)",
           fill=INK, font=font(14, True))
    labels = ["off", "red", "green", "amber (both)"]
    for k, v in enumerate((0, 1, 2, 3)):
        frame = [[0] * W for _ in range(H)]
        frame[0][0] = v
        p = to_panel(frame)
        x0 = 30 + k * 130
        d.text((x0, 40), labels[k], fill=INK, font=font(12))
        for py in range(5):
            row = p[py][8]
            c = FILL[{(0, 0, 0): 0}.get(row, 0)] if isinstance(row, tuple) else FILL[row]
            d.rectangle([x0, 62 + py * s, x0 + s * 2, 62 + py * s + s - 2], fill=c, outline=GRID)
            d.text((x0 + s * 2 + 6, 64 + py * s), f"panel row {py}", fill=(90, 90, 90), font=font(10))
    d.multiline_text((14, 190),
                     "Sign row y -> red on panel rows 2y and 2y+1, green on rows 2y+1 and 2y+2.\n"
                     "A red + green pixel therefore shows red on top, amber in the middle and\n"
                     "green underneath, like the real boards. The 80 sign columns sit 1:1 in the\n"
                     "middle of the 96-column panel (8 blank columns each side).\n"
                     "Scratch-built boards: drive red and green separately and mount the green\n"
                     "LED clusters slightly below the red ones.",
                     fill=INK, font=font(12), spacing=5)
    im.save(os.path.join(OUT, "panel_mapping.png"), optimize=True)
    print("plans written to", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
