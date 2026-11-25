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

# --------------------------------------------------------------------------- sourced bitmaps
# Full-frame pixel maps posted by prodestrian (GBFans, 8 Nov 2026: reference thread post #41
# and release topic post #12), read from the 1989 Getty premiere footage and decoded here from
# his 2000x160 diagrams. R = red, G = green, Y = both, . = off.
PRODESTRIAN_MAPS = {
    # WE'RE READY: all red, then each word turns green in turn (post #41)
    "C_red": (
        "......R...R.RRRRR....R..RRRR..RRRRR........RRRR..RRRRR..RRR..RRRR..R...R........",
        "......R...R.R.......R...R...R.R............R...R.R.....R...R.R...R.R...R........",
        "......R...R.R...........R...R.R............R...R.R.....R...R.R...R..R.R.........",
        "......R.R.R.RRRR........RRRR..RRRR.........RRRR..RRRR..RRRRR.R...R...R..........",
        "......R.R.R.R...........R.R...R............R.R...R.....R...R.R...R...R..........",
        "......R.R.R.R...........R..R..R............R..R..R.....R...R.R...R...R..........",
        ".......R.R..RRRRR.......R...R.RRRRR........R...R.RRRRR.R...R.RRRR....R.........."),
    # TO BELIEVE YOU: all red, then TO, BELIEVE and YOU each turn green in turn (post #41)
    "D_red": (
        "RRRRR..RRR.......RRRR..RRRRR.R......R..RRRRR.R...R.RRRRR......R...R..RRR..R...R.",
        "..R...R...R.......R..R.R.....R......R..R.....R...R.R..........R...R.R...R.R...R.",
        "..R...R...R.......R..R.R.....R......R..R.....R...R.R...........R.R..R...R.R...R.",
        "..R...R...R.......RRR..RRRR..R......R..RRRR...R.R..RRRR.........R...R...R.R...R.",
        "..R...R...R.......R..R.R.....R......R..R......R.R..R............R...R...R.R...R.",
        "..R...R...R.......R..R.R.....R......R..R.......R...R............R...R...R.R...R.",
        "..R....RRR.......RRRR..RRRRR.RRRRR..R..RRRRR...R...RRRRR........R....RRR...RRR.."),
    # US! with its green drop shadow, between the inward-pointing green arrows (post #12)
    "K_on": (
        "............G................RRG..RRG.RRRRRRRG.RRG.................G............",
        "............GG...............RRG..RRG.RRYRRRRG.RRG................GG............",
        "........GGGGGGG..............RRG..RRG.RRG...R..RRG...............GGGGGGG........",
        "........GGGGGGGG.............RRG..RRG..RRRRR...RY...............GGGGGGGG........",
        "........GGGGGGG..............RRG..RRG.R....RRG...................GGGGGGG........",
        "............GG...............RRRRRRG..RRRRRRRG.RRG................GG............",
        "............G.................RYYYY...RYYYYYY..RY..................G............"),
}
WORD_SPANS = {"C": [(6, 35), (43, 72)], "D": [(0, 11), (17, 56), (62, 80)]}


def bitmap(rows):
    code = {".": OFF, "R": R, "G": G, "Y": Y}
    return [[code[ch] for ch in row] for row in rows]


def word_green(f, span):
    """Turn the lit pixels inside one word's column span green (prodestrian, post #41)."""
    a, b = span
    return [[G if (v and a <= x < b) else v for x, v in enumerate(row)] for row in f]


# --------------------------------------------------------------------------- frame helpers
def blank(c=OFF):
    return [[c] * W for _ in range(H)]


def layout(text, font, gap, space, colors, start=None):
    """Lay out text in a font. colors: one color, or a per-character list."""
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


def border(f):
    """Static green border round the sign edge, behind the text (seen in the FOR HIRE still).
    Whether it animates is undocumented, so it is drawn static."""
    out = [list(r) for r in f]
    for y in range(H):
        for x in range(W):
            if (y in (0, H - 1) or x in (0, W - 1)) and out[y][x] == OFF:
                out[y][x] = G
    return out


def colmix(a, b, x):
    """Columns < x from a, the rest from b."""
    return [ra[:x] + rb[x:] for ra, rb in zip(a, b)]


def wipe_cover(old, color, x=W // 2):
    """INFERRED wipe, left to right: a solid color advances over the old frame (one half step).
    Direction inferred from the left-to-right red sweep seen in the deleted-scene clip (V1)."""
    return colmix(blank(color), old, x)


def wipe_reveal(new, color, x=W // 2):
    """INFERRED wipe, left to right: the new frame is revealed from a solid color (one half step)."""
    return colmix(new, blank(color), x)


def shimmer(f, probs, seed, cycle=3):
    """Shimmer: lit pixels drop out and return. Reported in the thread (film, deleted scene,
    behind-the-scenes, premiere). prodestrian (reference thread post #41) sees the pattern in the
    Getty footage as partly repeating and says a suitably randomized sequence is fine, so a short
    cycle of seeded random masks repeats (pixel pattern INFERRED, repetition per his reading)."""
    rng = random.Random(seed)
    masks = [[[rng.random() for _ in range(W)] for _ in range(H)] for _ in range(cycle)]
    return [[[v if (v and masks[i % cycle][y][x] > p) else OFF for x, v in enumerate(row)]
             for y, row in enumerate(f)] for i, p in enumerate(probs)]


def flip(f):
    """Upside-down state: the frame mirrored top to bottom, each letter staying in place.
    Seen during the GHOSTBUSTERS red/green swaps in the clip prodestrian posted (release topic
    post #12), with the deleted museum scene and behind-the-scenes photos (his citations)."""
    return [list(r) for r in f[::-1]]


def drop_shadow(f, color=G):
    """Green drop shadow one column right of the text, on unlit pixels only. prodestrian
    (release topic post #12): WHO YA, GONNA, CALL? and US! have it; the arrows do not."""
    out = [list(r) for r in f]
    for y in range(H):
        for x in range(1, W):
            if f[y][x - 1] and not f[y][x]:
                out[y][x] = color
    return out


def wipe_rl(old, new, steps):
    """Right-to-left wipe: the new frame replaces the old from the right edge leftwards.
    Direction sourced (prodestrian, post #41: WE'RE READY -> TO BELIEVE YOU); style inferred."""
    xs = [round(W * (steps - i) / (steps + 1)) for i in range(steps)]
    return [colmix(old, new, x) for x in xs]


def hold(f, n):
    return [f] * n


# --------------------------------------------------------------------------- sequence
def lines_boxes(full=False, first=True):
    """The "five lines -> green boxes" graphic.

    Sourced: five equal full-height boxes, 16 columns each, with no gaps between them (the
    apparent gaps are an optical illusion from the offset red/green LEDs); in each box a red line
    starts at the box's left edge and expands until it is 16 columns wide, then shrinks from the
    same starting edge, revealing green; it loops (prodestrian, reference thread post #41 and
    release topic post #12, from the Getty premiere footage; confirmed by the deleted-scene clip V1).
    Inferred: the number of steps per pass.
    """
    SEG, N = 16, 5

    def frame(fill):                       # fill(col within box 0..15) -> color
        return [[fill(x % SEG) for x in range(N * SEG)] for _ in range(H)]

    grow = (1, 4, 8, 12, 16) if full else (1, 6, 11, 16)
    shrink = (4, 8, 12) if full else (6, 11)
    base = OFF if first else G             # first pass draws over a dark sign, loops over green
    out = [frame(lambda c, w=w: R if c < w else base) for w in grow]
    out += [frame(lambda c, s=s: G if c < s else R) for s in shrink]
    out.append(frame(lambda c: G))
    return out


def reveal_center(new, old_keep, half):
    """New frame revealed outward from the center column; outside the revealed span the
    old frame's pixels (old_keep) stay lit. Seen in the deleted-scene clip for US! -> CALL."""
    lo, hi = W // 2 - half, W // 2 + half
    return [[new[y][x] if lo <= x < hi else old_keep[y][x] for x in range(W)] for y in range(H)]


PROFILES = ("single", "full")


def wipe_steps(old, new, color, solid, steps):
    """INFERRED left-to-right wipe: color covers old in `steps` half-steps, optional solid
    frames, then new is revealed from the color in `steps` steps. old/new may be None."""
    xs = [round(W * (i + 1) / (steps + 1)) for i in range(steps)]
    out = [wipe_cover(old, color, x) for x in xs] if old is not None else []
    out += [blank(color)] * solid
    out += [wipe_reveal(new, color, x) for x in xs] if new is not None else []
    return out


def build_segments(profile="single"):
    """Return [(id, label, [frames])] in playback order. Ids follow the GBFans A-L scheme.

    profile="single": one CoolLED file, compressed to the 113-frame upload limit.
    profile="full":   screen-timed version, split into two files (Part 1 = A-F, Part 2 = G-L),
                      each within the 113-frame limit, played back to back.

    Every element is attributed in docs/ATTRIBUTION.md. Three effects whose appearance is not
    documented are rendered as INFERRED reconstructions at the owner's request: the color wipes
    (left to right), the shimmer (random sparkle) and the lines -> boxes graphic. Timings for J-L
    are measured from the deleted-scene clip (V1). In "full", other message holds use 2.0 s, based
    on the measured CALL JL5-2020 hold (2.1 s); the 16 swaps follow the thread; the shimmer runs
    "a few seconds" (thread). These remain estimates where marked.
    """
    full = profile == "full"
    A_r = narrow("GHOSTBUSTERS", R)
    A_g = recolor(A_r, G)
    B = border(narrow("FOR HIRE...", R, gap=2, space=6))
    # WE'RE READY and TO BELIEVE YOU: prodestrian's pixel maps (post #41). Each is all red, then
    # each word turns green in turn.
    C_red = bitmap(PRODESTRIAN_MAPS["C_red"])
    C_we, C_ready = (word_green(C_red, sp) for sp in WORD_SPANS["C"])
    D_red = bitmap(PRODESTRIAN_MAPS["D_red"])
    D_to, D_bel, D_you = (word_green(D_red, sp) for sp in WORD_SPANS["D"])
    E = thin("CALL JL5-2020", Y)
    s = "WE'RE BACK"
    G_rg, G_gr = wide(s, per_word(s, [R, G])), wide(s, per_word(s, [G, R]))
    # WHO YA, GONNA, CALL?: red letters with a green drop shadow (prodestrian, post #12; red
    # letters measured in V1). WHO YA is two words, so it gets a full word space.
    Hf = drop_shadow(wide("WHO YA", R, space=6))
    I = drop_shadow(wide("GONNA", R))
    J = drop_shadow(wide("CALL?", R))
    # US! with drop shadow and arrows: prodestrian's pixel map (post #12)
    K_on = bitmap(PRODESTRIAN_MAPS["K_on"])
    is_arrow = lambda x: x < 20 or x >= 60
    K_off = [[OFF if is_arrow(x) else v for x, v in enumerate(r)] for r in K_on]
    arrows_only = [[v if is_arrow(x) else OFF for x, v in enumerate(r)] for r in K_on]
    L = E

    MSG = 10 if full else None                 # 2.0 s message hold in the full profile
    WS = 2 if full else 1                      # wipe half-steps
    seg = []

    # A
    a = [shift(A_r, 4), shift(A_r, 2)] + hold(A_r, 3 if full else 1)   # rises red after L (V1)
    a += shimmer(A_g, (0.2, 0.4, 0.6, 0.7, 0.6, 0.4, 0.3, 0.2) if full else (0.3, 0.6, 0.3), seed=1989)
    a += hold(A_g, 3 if full else 1)                                   # GHOSTBUSTERS again, green
    # ~16 rapid red/green swaps with upside-down states (flip: prodestrian post #12 clip;
    # the exact order of upright/flipped states is estimated)
    a += [A_r, flip(A_r), A_g, flip(A_g)] * 4
    a += [A_g] + [blank(G)] * (2 if full else 1)                       # ends green, solid green
    seg.append(("A", "GHOSTBUSTERS - rises red, shimmer, green, ~16 red/green swaps with upside-down flips, solid green", a))
    # B
    seg.append(("B", "FOR HIRE... - wiped in from green (inferred L-R); green border; green wipe out",
                wipe_steps(None, B, G, 0, WS) + hold(B, MSG or 2)
                + wipe_steps(B, None, G, 2 if full else 1, WS)))
    # C
    # C: red, each word green in turn, red; right-to-left wipe into D (prodestrian post #41)
    c = (hold(C_red, 2) + hold(C_we, 2) + hold(C_ready, 2) + hold(C_red, 2)) if full \
        else [C_red, C_we, C_ready, C_red]
    seg.append(("C", "WE'RE READY - wiped in from green (inferred L-R); red, WE'RE then READY turn green; "
                "right-to-left wipe to D", wipe_steps(None, C_red, G, 0, WS) + c))
    # D: red, then TO, BELIEVE and YOU each turn green in turn (prodestrian post #41)
    d = wipe_rl(C_red, D_red, WS)
    d += (hold(D_red, 2) + hold(D_to, 2) + hold(D_bel, 2) + hold(D_you, 2) + hold(D_red, 2)) if full \
        else [D_red, D_to, D_bel, D_you, D_red]
    seg.append(("D", "TO BELIEVE YOU - red; TO, BELIEVE, YOU turn green in turn; wipes down as E slides in",
                d + [stack(E, D_red, 5), stack(E, D_red, 2)]))
    # E
    seg.append(("E", "CALL JL5-2020 - thin, amber; red wipe out (inferred L-R)",
                hold(E, MSG or 3) + wipe_steps(E, None, R, 2 if full else 1, WS)))
    # F
    f = wipe_steps(None, A_g, R, 0, WS) + hold(A_g, 3 if full else 1)
    f += shimmer(A_g, (0.3, 0.5, 0.7, 0.7, 0.5, 0.3) if full else (0.4, 0.7), seed=2020)
    f += hold(A_g, 3 if full else 1)
    f += ([colmix(A_r, A_g, 27), colmix(A_r, A_g, 54)] if full else [colmix(A_r, A_g, W // 2)])
    f += hold(A_r, 4 if full else 1) + [blank(R)] * (2 if full else 1)
    seg.append(("F", "GHOSTBUSTERS - wiped in green from red, shimmer (inferred), green, green-to-red wipe, solid red", f))
    # G
    # No WE'RE-alone frame (listed before WE'RE BACK in T #14 Getty): removed at the owner's direction
    g = [blank(G)] * (2 if full else 1) + hold(G_rg, 11 if full else 3)
    g += ([G_gr, G_gr, G_rg, G_rg] * 2) if full else [G_gr, G_rg]
    seg.append(("G", "WE'RE BACK - green flash, WE'RE BACK, words swap colors", g))
    # G2
    g2 = lines_boxes(full) + (lines_boxes(full, first=False) * 2 if full else [])
    seg.append(("G2", "Five lines -> green boxes: red grows from each box's left edge, then shrinks "
                "from it revealing green (no gaps); loops", g2))
    seg.append(("H", "WHO YA - red with green drop shadow", hold(Hf, MSG or 2)))
    seg.append(("I", "GONNA - red with green drop shadow", hold(I, MSG or 2)))
    seg.append(("J", "CALL? - red with green drop shadow; slides up and out; blank ~0.8 s",
                hold(J, 4) + [shift(J, -3), shift(J, -6)] + hold(blank(), 4)))
    seg.append(("K", "US! - red alone, then green arrows (on ~1.2 s, off ~0.8 s, on)",
                hold(K_off, 3) + hold(K_on, 6) + hold(K_off, 4) + hold(K_on, 3)))
    seg.append(("L", "CALL JL5-2020 - reveals from center (arrows stay), holds ~2 s, slides down",
                [reveal_center(L, arrows_only, 8), reveal_center(L, arrows_only, 16)]
                + hold(L, 11 if full else 10) + [shift(L, 3), shift(L, 6)]))
    return seg


PART1 = ("A", "B", "C", "D", "E", "F")
PART2 = ("G", "G2", "H", "I", "J", "K", "L")


def build_parts():
    segs = build_segments("full")
    p1 = [f for sid, _, fr in segs if sid in PART1 for f in fr]
    p2 = [f for sid, _, fr in segs if sid in PART2 for f in fr]
    return p1, p2


def build():
    return [f for _, _, frames in build_segments() for f in frames]


# --------------------------------------------------------------------------- panel + JT
def to_panel(f, pw=PANEL_W, ph=PANEL_H):
    """Map 80x7 onto the panel: 2 panel rows per sign row, centered.
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
    """One color bit-plane: column-major, 8 rows per byte, MSB = top row."""
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
    export_two_part(os.path.join(out, "two_part"))
    return segs, frames


def export_two_part(out):
    """Screen-timed version as two CoolLED files (Part 1 = A-F, Part 2 = G-L), plus
    full-timing JSON and GIF previews for other apps."""
    os.makedirs(out, exist_ok=True)
    segs = build_segments("full")
    p1, p2 = build_parts()
    for name, fr in (("Part1", p1), ("Part2", p2)):
        jt, _ = encode_jt(fr)
        with open(os.path.join(out, f"Ecto-1A_GB2_16x96_{name}.jt"), "w") as fh:
            json.dump(jt, fh, separators=(",", ":"))
        pan = [led_image(f, 6, offset=True) for f in fr]
        pan[0].save(os.path.join(out, f"ecto1a_96x16_{name}.gif"), save_all=True,
                    append_images=pan[1:], duration=DELAY_MS, loop=0)
    frames = p1 + p2
    timeline, i = [], 0
    for sid, label, fr in segs:
        timeline.append({"id": sid, "part": 1 if sid in PART1 else 2, "label": label,
                         "first_frame": i, "frames": len(fr), "duration_ms": len(fr) * DELAY_MS})
        i += len(fr)
    uniq, plist = playlist(frames)
    meta = {"width": W, "height": H, "frame_ms": DELAY_MS, "profile": "full (screen-timed)",
            "pixel_values": {"0": "off", "1": "red", "2": "green", "3": "red+green (amber)"},
            "frames_total": len(frames), "loop_ms": len(frames) * DELAY_MS,
            "part1_frames": len(p1), "part2_frames": len(p2), "timeline": timeline}
    with open(os.path.join(out, "ecto1a_full_frames.json"), "w") as fh:
        json.dump({**meta, "frames": frames}, fh, separators=(",", ":"))
    with open(os.path.join(out, "ecto1a_full_playlist.json"), "w") as fh:
        json.dump({**meta, "unique_frames": uniq,
                   "playlist": [{"frame": a, "ms": b} for a, b in plist]}, fh, separators=(",", ":"))
    led = [led_image(f, 6, offset=True) for f in frames]
    led[0].save(os.path.join(out, "ecto1a_96x16_full.gif"), save_all=True, append_images=led[1:],
                duration=DELAY_MS, loop=0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default="dist")
    a = ap.parse_args()
    segs, frames = export_all(a.out)
    print(f"{len(frames)} frames, {len(frames) * DELAY_MS / 1000:.1f}s loop -> {a.out}")
