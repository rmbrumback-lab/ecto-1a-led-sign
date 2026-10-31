#!/usr/bin/env python3
"""
Ecto-1A (Ghostbusters II, 1989) roof sign recreation.

Builds the sign's animation as an 80x7 logical frame sequence, then:
  * encodes it as a CoolLED1248 .jt animation for a 16x96 panel, and
  * exports portable formats (JSON, C header, PNG frames, sprite sheets, GIFs)
    for other LED sign apps and microcontroller projects.

Pixel values: 0 = off, 1 = red, 2 = green, 3 = red+green (reads as amber/yellow).

Run:  python -m ecto1a.generate --out dist     (from the src/ directory)
"""
from __future__ import annotations

import argparse
import json
import os
import random

W, H = 80, 7
OFF, R, G, Y = 0, 1, 2, 3
DELAY_MS = 200          # CoolLED1248 uses one frame delay for the whole animation
PANEL_W, PANEL_H = 96, 16


def _g(*rows):
    return list(rows)


# --------------------------------------------------------------------------- fonts
# THIN: classic 5x7, 1-column gaps. Confirmed by Getty close-ups of CALL / BELIEVE / WE'RE.
THIN = {
    'A': _g(".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': _g("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'C': _g(".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."),
    'D': _g("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'E': _g("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'I': _g(".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    'J': _g("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'L': _g("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'O': _g(".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'R': _g("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    'T': _g("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': _g("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'V': _g("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'W': _g("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    'Y': _g("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    '0': _g(".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    '2': _g(".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    '5': _g("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    '-': _g("....", "....", "....", "####", "....", "....", "...."),
    "'": _g("#", "#", ".", ".", ".", ".", "."),
}

# BOLD_WIDE: 7-wide, 2-px strokes, 2-column gaps. B/A/C/K read pixel-for-pixel from the
# hi-res "WE'RE BACK" book scan; W/E/'/R read from the same scan. "WE'RE BACK" = cols 0-79.
BOLD_WIDE = {
    'W': _g("##......##", "##......##", "##..##..##", "##..##..##", "##..##..##", "##..##..##", ".########."),
    'E': _g("#######", "##.....", "##.....", "######.", "##.....", "##.....", "#######"),
    "'": _g(".##", "##.", "...", "...", "...", "...", "..."),
    'R': _g("######.", "##...##", "##...##", "######.", "##.##..", "##..##.", "##...##"),
    'B': _g("########.", "..##...##", "..##...##", "..######.", "..##...##", "..##...##", "########."),
    'A': _g(".#####.", "##...##", "##...##", "#######", "##...##", "##...##", "##...##"),
    'C': _g(".#####.", "##...##", "##.....", "##.....", "##.....", "##...##", ".#####."),
    'K': _g("##...##", "##..##.", "##.##..", "####...", "##.##..", "##..##.", "##...##"),
    # Below: same style, not directly visible in reference photos (estimated).
    'H': _g("##...##", "##...##", "##...##", "#######", "##...##", "##...##", "##...##"),
    'O': _g(".#####.", "##...##", "##...##", "##...##", "##...##", "##...##", ".#####."),
    'Y': _g("##...##", "##...##", ".##.##.", "..###..", "..###..", "..###..", "..###.."),
    'G': _g(".#####.", "##...##", "##.....", "##.####", "##...##", "##...##", ".#####."),
    'N': _g("##...##", "###..##", "####.##", "##.####", "##..###", "##...##", "##...##"),
    'L': _g("##.....", "##.....", "##.....", "##.....", "##.....", "##.....", "#######"),
    'U': _g("##...##", "##...##", "##...##", "##...##", "##...##", "##...##", ".#####."),
    'S': _g(".#####.", "##...##", "##.....", ".#####.", ".....##", "##...##", ".#####."),
    '?': _g(".#####.", "##...##", ".....##", "...###.", "...##..", ".......", "...##.."),
    '!': _g("##", "##", "##", "##", "##", "..", "##"),
    # Arrows beside US!, both pointing inward (read from blurred premiere footage).
    '<': _g("...##....", "..###....", ".########", "#########", ".########", "..###....", "...##...."),
    '>': _g("....##...", "....###..", "########.", "#########", "########.", "....###..", "....##..."),
}

# BOLD_NARROW: 6-wide (H, S = 5), 2-px strokes, 1-column gaps. Sampled from the night
# GHOSTBUSTERS still; GHOSTBUSTERS spans cols 0-78.
BOLD_NARROW = {
    'G': _g(".####.", "##..##", "##....", "##.###", "##..##", "##..##", ".####."),
    'H': _g("##.##", "##.##", "##.##", "#####", "##.##", "##.##", "##.##"),
    'O': _g(".####.", "##..##", "##..##", "##..##", "##..##", "##..##", ".####."),
    'S': _g(".###.", "##..#", "##...", ".###.", "...##", "#..##", ".###."),
    'T': _g("######", "..##..", "..##..", "..##..", "..##..", "..##..", "..##.."),
    'B': _g("#####.", "##..##", "##..##", "#####.", "##..##", "##..##", "#####."),
    'U': _g("##..##", "##..##", "##..##", "##..##", "##..##", "##..##", ".####."),
    'E': _g("######", "##....", "##....", "#####.", "##....", "##....", "######"),
    'R': _g("#####.", "##..##", "##..##", "#####.", "##.##.", "##..##", "##..##"),
    'F': _g("######", "##....", "##....", "#####.", "##....", "##....", "##...."),
    'I': _g("##", "##", "##", "##", "##", "##", "##"),
    '.': _g("..", "..", "..", "..", "..", "##", "##"),
}

FONTS = {"thin": THIN, "bold_wide": BOLD_WIDE, "bold_narrow": BOLD_NARROW}


# --------------------------------------------------------------------------- frame helpers
def blank(c=OFF):
    return [[c] * W for _ in range(H)]


def layout(text, font, gap, space, colors, start=None):
    """Lay out text in a font. colors: one colour, or a per-character list."""
    cols, prev_space = [], True
    for i, ch in enumerate(text):
        c = colors[i] if isinstance(colors, list) else colors
        if ch == ' ':
            cols += [[OFF] * H] * space
            prev_space = True
            continue
        if not prev_space:
            cols += [[OFF] * H] * gap
        glyph = font[ch]
        for x in range(len(glyph[0])):
            cols.append([c if glyph[y][x] == '#' else OFF for y in range(H)])
        prev_space = False
    if len(cols) > W:
        raise ValueError(f"{text!r} is {len(cols)} columns; sign is {W}")
    x0 = (W - len(cols)) // 2 if start is None else start
    f = blank()
    for x, col in enumerate(cols):
        for y in range(H):
            f[y][x0 + x] = col[y]
    return f


def thin(s, colors):
    return layout(s, THIN, 1, 3, colors)


def wide(s, colors, start=None, space=2):
    return layout(s, BOLD_WIDE, 2, space, colors, start)


def narrow(s, colors, gap=1, space=3):
    return layout(s, BOLD_NARROW, gap, space, colors)


def per_word(s, word_colors):
    out, wi = [], 0
    for ch in s:
        if ch == ' ':
            out.append(OFF)
            wi += 1
        else:
            out.append(word_colors[wi])
    return out


def recolor(f, c):
    return [[c if v else OFF for v in row] for row in f]


def shift(f, dy):
    """Shift vertically; +dy = down. Content leaving the sign is dropped."""
    out = blank()
    for y in range(H):
        sy = y - dy
        if 0 <= sy < H:
            out[y] = list(f[sy])
    return out


def stack(top, bottom, dy):
    """Top frame above bottom frame (1 blank row between), viewed at row offset dy."""
    tall = top + [[OFF] * W] + bottom
    return [list(tall[dy + y]) for y in range(H)]


def colmix(a, b, x):
    """Columns < x from a, the rest from b."""
    return [ra[:x] + rb[x:] for ra, rb in zip(a, b)]


def flipv(f):
    return [list(r) for r in f[::-1]]


def wipe(old, new, color):
    """Colour bar sweeps over old, then new is revealed from the bar (3 frames)."""
    bar = blank(color)
    return [colmix(bar, old, 40), bar, colmix(new, bar, 40)]


def shimmer(f, probs, rng):
    return [[[v if (v and rng.random() > p) else OFF for v in row] for row in f] for p in probs]


PERIM = ([(0, x) for x in range(W)] + [(y, W - 1) for y in range(1, H)] +
         [(H - 1, x) for x in range(W - 2, -1, -1)] + [(y, 0) for y in range(H - 2, 0, -1)])


def border(f, t):
    """Green dotted border chasing round the sign edge, behind the text."""
    out = [list(r) for r in f]
    for i, (y, x) in enumerate(PERIM):
        if out[y][x] == OFF and (i + t) % 5 != 0:
            out[y][x] = G
    return out


def lines_boxes():
    """Five vertical red lines sweep across 16-col segments, then become green boxes."""
    out = []
    for off in (0, 7, 15):
        f = blank()
        for s in range(5):
            for y in range(H):
                f[y][s * 16 + off] = R
        out.append(f)
    box = blank()
    for s in range(5):
        for y in range(1, 6):
            for x in range(s * 16 + 3, s * 16 + 13):
                box[y][x] = G
    out.append(box)
    return out


def hold(f, n):
    return [f] * n


# --------------------------------------------------------------------------- sequence
def build_segments():
    """Return [(id, label, [frames])] in playback order. Ids follow the GBFans A-L scheme."""
    rng = random.Random(1989)
    A_r = narrow("GHOSTBUSTERS", R)
    A_g = recolor(A_r, G)
    B = narrow("FOR HIRE...", R, gap=2, space=6)
    C = thin("WE'RE READY", Y)
    s = "TO BELIEVE YOU"
    D_red, D_tog, D_bely = (thin(s, per_word(s, c)) for c in ([R, R, R], [G, R, R], [R, Y, R]))
    E = thin("CALL JL5-2020", Y)
    s = "WE'RE BACK"
    G_were = wide("WE'RE", R, start=0)
    G_rg, G_gr = wide(s, per_word(s, [R, G])), wide(s, per_word(s, [G, R]))
    Hf, I, J = wide("WHO YA", G), wide("GONNA", R), wide("CALL?", G)
    k = "> US! <"
    K_on = wide(k, [G, OFF, R, R, R, OFF, G], space=6)
    K_off = wide(k, [OFF, OFF, R, R, R, OFF, OFF], space=6)
    L = E

    seg = []
    a = [shift(A_r, 4), shift(A_r, 2)] + hold(A_r, 2)
    a += [shift(A_g, 3), A_g, shift(A_r, -3), A_r, flipv(A_g), A_r]
    a += [A_g if i % 2 == 0 else A_r for i in range(10)]
    a += hold(A_g, 2) + [blank(G), colmix(border(B, 0), blank(G), 40)]
    seg.append(("A", "GHOSTBUSTERS - rises red, bounces/flips, red/green swaps, solid green", a))
    seg.append(("B", "FOR HIRE... - red, chasing green border; green wipe out",
                [border(B, t) for t in range(1, 7)] + wipe(border(B, 7), C, G)))
    seg.append(("C", "WE'RE READY - thin, yellow; green wipe out", hold(C, 5) + wipe(C, D_red, G)))
    seg.append(("D", "TO BELIEVE YOU - thin, word colours cycle; pushed down by E",
                [D_red, D_red, D_tog, D_tog, D_bely, D_bely, stack(E, D_red, 5), stack(E, D_red, 2)]))
    seg.append(("E", "CALL JL5-2020 - thin, yellow; red wipe out", hold(E, 5) + wipe(E, A_g, R)))
    seg.append(("F", "GHOSTBUSTERS - green, shimmer, green, green-to-red, solid red",
                hold(A_g, 2) + shimmer(A_g, (0.3, 0.6, 0.8, 0.6, 0.3), rng) + hold(A_g, 1)
                + [colmix(A_r, A_g, 40), A_r, blank(R)]))
    seg.append(("G", "WE'RE BACK - WE'RE red, green flash, WE'RE BACK, words swap colours",
                hold(G_were, 2) + [blank(G)] + hold(G_rg, 3) + [G_gr, G_rg, G_gr, G_rg]))
    seg.append(("G2", "Five sweeping lines become green boxes (x2)", lines_boxes() + lines_boxes()))
    seg.append(("H", "WHO YA", hold(Hf, 4)))
    seg.append(("I", "GONNA", hold(I, 4)))
    seg.append(("J", "CALL? - slides up and out", hold(J, 4) + [shift(J, -3), shift(J, -6)]))
    seg.append(("K", "US! - red, blinking green arrows pointing in", [K_on, K_off, K_on, K_off, K_on]))
    seg.append(("L", "CALL JL5-2020 - slides down; GHOSTBUSTERS rises to loop",
                hold(L, 4) + [shift(L, 3), shift(L, 6)]))
    return seg


def build():
    return [f for _, _, frames in build_segments() for f in frames]


# --------------------------------------------------------------------------- panel + JT
def to_panel(f, pw=PANEL_W, ph=PANEL_H):
    """Map 80x7 onto the panel: 2 panel rows per sign row, centred.
    Red on rows 2y,2y+1; green on 2y+1,2y+2 - the real sign's green clusters sit lower."""
    p = [[0] * pw for _ in range(ph)]
    x0, y0 = (pw - W) // 2, (ph - (2 * H + 1)) // 2
    for y in range(H):
        for x in range(W):
            v = f[y][x]
            if v & R:
                p[y0 + 2 * y][x0 + x] |= R
                p[y0 + 2 * y + 1][x0 + x] |= R
            if v & G:
                p[y0 + 2 * y + 1][x0 + x] |= G
                p[y0 + 2 * y + 2][x0 + x] |= G
    return p


def plane(p, bit, pw, ph):
    """One colour bit-plane: column-major, 8 rows per byte, MSB = top row."""
    out = []
    for x in range(pw):
        for yb in range(0, ph, 8):
            v = 0
            for k in range(8):
                y = yb + k
                if y < ph and (p[y][x] & bit):
                    v |= 0x80 >> k
            out.append(v)
    return out


def encode_jt(frames, pw=PANEL_W, ph=PANEL_H, delay=DELAY_MS):
    panels = [to_panel(f, pw, ph) for f in frames]
    planes = {1: [], 2: [], 4: []}
    for p in panels:
        for bit in planes:
            planes[bit] += plane(p, bit, pw, ph)
    data = planes[1] + planes[2] + planes[4]          # R, G, B planes, all frames each
    if len(frames) > 255 or len(data) > 65535:
        raise ValueError(f"over protocol limits: {len(frames)} frames, {len(data)} bytes")
    return [{"data": {"pixelWidth": pw, "aniData": data, "frameNum": len(frames),
                      "delays": delay, "aniType": 1, "pixelHeight": ph},
             "dataType": 0}], panels


def decode_jt(jt):
    """Inverse of encode_jt (3-bit, aniType 1). Returns frames as [row][col] of 0-7."""
    d = jt[0]["data"]
    pw, ph = d["pixelWidth"], d["pixelHeight"]
    raw = d.get("aniData") or d["graffitiData"]
    n = d.get("frameNum", 1)
    bpc = (ph + 7) // 8
    per = pw * bpc
    frames = []
    for fi in range(n):
        f = [[0] * pw for _ in range(ph)]
        for pi, bit in enumerate((1, 2, 4)):
            base = pi * per * n + fi * per
            for x in range(pw):
                for b in range(bpc):
                    v = raw[base + x * bpc + b]
                    for k in range(8):
                        y = b * 8 + k
                        if y < ph and v & (0x80 >> k):
                            f[y][x] |= bit
        frames.append(f)
    return frames


# --------------------------------------------------------------------------- exports
RGB = {0: (40, 14, 12), 1: (255, 60, 20), 2: (120, 255, 40), 3: (255, 200, 30)}
RGB_FLAT = {0: (0, 0, 0), 1: (255, 0, 0), 2: (0, 255, 0), 3: (255, 255, 0)}


def playlist(frames):
    """Deduplicate consecutive identical frames: [(frame_index_in_unique, duration_ms)]."""
    uniq, keys, plist = [], {}, []
    for f in frames:
        key = json.dumps(f)
        if key not in keys:
            keys[key] = len(uniq)
            uniq.append(f)
        idx = keys[key]
        if plist and plist[-1][0] == idx:
            plist[-1][1] += DELAY_MS
        else:
            plist.append([idx, DELAY_MS])
    return uniq, plist


def led_image(f, scale=8, offset=False):
    from PIL import Image, ImageDraw
    if offset:  # render the 96x16 panel view (includes green offset)
        f = to_panel(f)
    h, w = len(f), len(f[0])
    im = Image.new("RGB", (w * scale, h * scale), (8, 6, 6))
    d = ImageDraw.Draw(im)
    for y in range(h):
        for x in range(w):
            d.ellipse([x * scale + 1, y * scale + 1, x * scale + scale - 2, y * scale + scale - 2],
                      fill=RGB[f[y][x]])
    return im


def flat_image(f):
    from PIL import Image
    im = Image.new("RGB", (len(f[0]), len(f)))
    im.putdata([RGB_FLAT[v] for row in f for v in row])
    return im


def write_c_header(path, uniq, plist):
    def byte_rows(f):
        # 2 bits per pixel, 4 pixels per byte, row-major, MSB first: bits = (green<<1)|red
        out = []
        for row in f:
            for x in range(0, W, 4):
                b = 0
                for k in range(4):
                    b |= row[x + k] << (6 - 2 * k)
                out.append(b)
        return out
    lines = [
        "// Ecto-1A (Ghostbusters II) roof sign - 80x7, generated by ecto1a/generate.py",
        "// Pixel = 2 bits: bit0 red, bit1 green (3 = both). 4 pixels per byte, MSB first,",
        "// row-major, 20 bytes per row, 140 bytes per frame.",
        "#pragma once",
        "#include <stdint.h>",
        "#ifndef PROGMEM",
        "#define PROGMEM",
        "#endif",
        f"#define ECTO1A_W {W}",
        f"#define ECTO1A_H {H}",
        f"#define ECTO1A_UNIQUE_FRAMES {len(uniq)}",
        f"#define ECTO1A_STEPS {len(plist)}",
        "",
        f"static const uint8_t ecto1a_frames[ECTO1A_UNIQUE_FRAMES][{W * H // 4}] PROGMEM = {{",
    ]
    for i, f in enumerate(uniq):
        lines.append("  {" + ",".join(f"0x{b:02X}" for b in byte_rows(f)) + f"}}, // {i}")
    lines += ["};", "",
              "// Playback: {unique frame index, duration in ms}",
              "static const uint16_t ecto1a_playlist[ECTO1A_STEPS][2] PROGMEM = {"]
    lines += ["  " + ", ".join(f"{{{a},{b}}}" for a, b in plist[i:i + 8]) + ","
              for i in range(0, len(plist), 8)]
    lines += ["};", ""]
    with open(path, "w") as fh:
        fh.write("\n".join(lines))


def export_all(out):
    from PIL import Image
    os.makedirs(out, exist_ok=True)
    segs = build_segments()
    frames = [f for _, _, fr in segs for f in fr]

    jt, _ = encode_jt(frames)
    with open(os.path.join(out, "Ecto-1A_GB2_16x96.jt"), "w") as fh:
        json.dump(jt, fh, separators=(",", ":"))

    uniq, plist = playlist(frames)
    timeline, i = [], 0
    for sid, label, fr in segs:
        timeline.append({"id": sid, "label": label, "first_frame": i, "frames": len(fr),
                         "duration_ms": len(fr) * DELAY_MS})
        i += len(fr)
    meta = {"width": W, "height": H, "frame_ms": DELAY_MS,
            "pixel_values": {"0": "off", "1": "red", "2": "green", "3": "red+green (amber)"},
            "frames_total": len(frames), "loop_ms": len(frames) * DELAY_MS, "timeline": timeline}
    with open(os.path.join(out, "ecto1a_frames.json"), "w") as fh:
        json.dump({**meta, "frames": frames}, fh, separators=(",", ":"))
    with open(os.path.join(out, "ecto1a_playlist.json"), "w") as fh:
        json.dump({**meta, "unique_frames": uniq,
                   "playlist": [{"frame": a, "ms": b} for a, b in plist]}, fh, separators=(",", ":"))
    write_c_header(os.path.join(out, "ecto1a_frames.h"), uniq, plist)

    fdir = os.path.join(out, "frames_80x7")
    os.makedirs(fdir, exist_ok=True)
    for n, f in enumerate(frames):
        flat_image(f).save(os.path.join(fdir, f"frame_{n:03d}.png"))

    sheet = Image.new("RGB", (W, H * len(frames)))
    for n, f in enumerate(frames):
        sheet.paste(flat_image(f), (0, n * H))
    sheet.save(os.path.join(out, "ecto1a_spritesheet_80x7.png"))

    led = [led_image(f, 8) for f in frames]
    led[0].save(os.path.join(out, "ecto1a_80x7.gif"), save_all=True, append_images=led[1:],
                duration=DELAY_MS, loop=0)
    pan = [led_image(f, 6, offset=True) for f in frames]
    pan[0].save(os.path.join(out, "ecto1a_96x16_panel.gif"), save_all=True, append_images=pan[1:],
                duration=DELAY_MS, loop=0)
    return segs, frames


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default="dist")
    a = ap.parse_args()
    segs, frames = export_all(a.out)
    print(f"{len(frames)} frames, {len(frames) * DELAY_MS / 1000:.1f}s loop -> {a.out}")
