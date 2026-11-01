#!/usr/bin/env python3
"""Render documentation images into docs/images/ (font sheets, storyboard, offset close-up)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ecto1a.generate import (FONTS, build_segments, led_image, to_panel, wide, per_word,
                             R, G, Y, RGB, H)

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "images")
os.makedirs(OUT, exist_ok=True)
BG = (14, 12, 12)


def font_obj(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def glyph_img(glyph, color, s=12):
    h, w = len(glyph), len(glyph[0])
    im = Image.new("RGB", (w * s, h * s), (8, 6, 6))
    d = ImageDraw.Draw(im)
    for y in range(h):
        for x in range(w):
            c = RGB[color] if glyph[y][x] == '#' else RGB[0]
            d.ellipse([x * s + 1, y * s + 1, x * s + s - 2, y * s + s - 2], fill=c)
    return im


def font_sheet(name, font, color):
    s, pad = 12, 14
    keys = list(font.keys())
    cells = [glyph_img(font[k], color, s) for k in keys]
    per_row = 13 if name == "thin" else 10
    cw = max(c.width for c in cells) + pad
    ch = H * s + 34
    rows = (len(cells) + per_row - 1) // per_row
    im = Image.new("RGB", (per_row * cw + pad, rows * ch + 50), BG)
    d = ImageDraw.Draw(im)
    d.text((pad, 10), f"{name} font", fill=(230, 230, 230), font=font_obj(20))
    lf = font_obj(13)
    for i, (k, c) in enumerate(zip(keys, cells)):
        x = pad + (i % per_row) * cw
        y = 44 + (i // per_row) * ch
        im.paste(c, (x, y))
        d.text((x, y + H * s + 4), repr(k), fill=(160, 160, 160), font=lf)
    im.save(os.path.join(OUT, f"font_{name}.png"))


font_sheet("bold_narrow", FONTS["bold_narrow"], R)
font_sheet("bold_wide", FONTS["bold_wide"], G)
font_sheet("thin", FONTS["thin"], Y)

# Storyboard: a representative frame from each segment
pick = {"A": 2, "B": 1, "C": 1, "D": 3, "E": 0, "F": 1, "G": 4, "G2": 3,
        "H": 0, "I": 0, "J": 0, "K": 3, "L": 2}
segs = build_segments()
scale, lab_w = 7, 430
rows = [led_image(fr[pick[sid]], scale) for sid, _, fr in segs]
rh = rows[0].height + 16
im = Image.new("RGB", (rows[0].width + lab_w + 30, rh * len(rows) + 20), BG)
d = ImageDraw.Draw(im)
f1, f2 = font_obj(17), font_obj(12)
start = 0
for i, ((sid, label, fr), r) in enumerate(zip(segs, rows)):
    y = 10 + i * rh
    im.paste(r, (10, y))
    head, _, tail = label.partition(" - ")
    d.text((rows[0].width + 24, y + 2), f"{sid}  {head}", fill=(235, 235, 235), font=f1)
    d.text((rows[0].width + 24, y + 24), f"frames {start}-{start + len(fr) - 1}  ({len(fr) * 0.2:.1f}s)",
           fill=(150, 150, 150), font=f2)
    start += len(fr)
im.save(os.path.join(OUT, "storyboard.png"))

# Offset close-up: WE'RE BACK join on the 96x16 panel
s = "WE'RE BACK"
f = wide(s, per_word(s, [R, G]))
p = to_panel(f)
crop = [row[8 + 28:8 + 56] for row in p]
led_image(crop, 22).save(os.path.join(OUT, "offset_closeup.png"))

# Hero: one frame each of the three fonts, panel view
hero = [segs[0][2][2], segs[6][2][4], segs[3][2][2]]
imgs = [led_image(h, 7, offset=True) for h in hero]
im = Image.new("RGB", (imgs[0].width, sum(i.height for i in imgs) + 8 * 2), BG)
y = 0
for i_ in imgs:
    im.paste(i_, (0, y)); y += i_.height + 8
im.save(os.path.join(OUT, "hero.png"))
print("doc images written to", os.path.abspath(OUT))

# Inferred lines -> boxes graphic: every step, labeled (our rendering only; no film frames)
g2 = [fr for sid, _, fr in segs if sid == "G2"][0]
labels = ["1 red line wipes", "2 half filled", "3 full red, dark dividers",
          "4 green grows from centers", "5 full green, red dividers", "6 red sweeps back from left",
          "7 full red", "8 full green again"]
steps = [led_image(f, 6) for f in g2]
lh = steps[0].height + 22
im = Image.new("RGB", (steps[0].width + 330, lh * len(steps) + 40), BG)
d = ImageDraw.Draw(im)
d.text((10, 8), "Lines -> boxes (G2): INFERRED reconstruction, 200 ms per step", fill=(235, 235, 235), font=font_obj(16))
for i, (st, lab) in enumerate(zip(steps, labels)):
    y = 34 + i * lh
    im.paste(st, (10, y))
    d.text((st.width + 22, y + st.height // 2 - 8), lab, fill=(200, 200, 200), font=font_obj(14))
im.save(os.path.join(OUT, "lines_boxes_steps.png"))

# Inferred wipes and shimmer: example frames (our rendering only)
from ecto1a.generate import blank, wipe_cover, wipe_reveal, shimmer, narrow, thin, recolor, R as _R, G as _G, Y as _Y
_A = recolor(narrow("GHOSTBUSTERS", _R), _G)
_E = thin("CALL JL5-2020", _Y)
ex = [(thin("CALL JL5-2020", _Y), "E: CALL JL5-2020"), (wipe_cover(_E, _R), "red wipe covers E (left to right)"),
      (blank(_R), "solid red (sourced)"), (wipe_reveal(_A, _R), "F revealed from red (left to right)"),
      (_A, "F: GHOSTBUSTERS green")] + [(f, lab) for f, lab in zip(shimmer(_A, (0.4, 0.7), seed=2020), ["shimmer 40% (inferred)", "shimmer 70% (inferred)"])] + [(_A, "GHOSTBUSTERS again")]
tiles = [led_image(f, 5) for f, _ in ex]
lh = tiles[0].height + 20
im = Image.new("RGB", (tiles[0].width + 360, lh * len(tiles) + 40), BG)
d = ImageDraw.Draw(im)
d.text((10, 8), "Wipes and shimmer: INFERRED reconstructions, 200 ms per step", fill=(235, 235, 235), font=font_obj(16))
for i, (t, (_, lab)) in enumerate(zip(tiles, ex)):
    y = 34 + i * lh
    im.paste(t, (10, y))
    d.text((t.width + 22, y + t.height // 2 - 8), lab, fill=(200, 200, 200), font=font_obj(14))
im.save(os.path.join(OUT, "wipes_shimmer_steps.png"))
