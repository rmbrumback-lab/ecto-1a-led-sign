"""Builds for other LED panels, kept apart from the main screen-accurate files.

Everything here is derived from the same sequence as the main build (generate.py). Two kinds:

* COMPACT: a shortened animation for older CoolLED panels that cap animations at 53 frames
  and can't play two programs in a row. It keeps every message in order but drops or shortens
  holds, wipes, the shimmer and repeats. It is NOT screen-timed and NOT the full sequence.
* CONVERTED: the main animations re-encoded as full-color GIFs for 24-bit panels and apps,
  split into chunks of at most 40 frames for apps that cap GIF length. Same frames and timing
  as the main build; only the file format differs.

Run:  python -m ecto1a.variants --out ../dist/other_panels
"""
import argparse
import json
import os

from PIL import Image

from . import generate as g
from .generate import (W, H, R, G, OFF, DELAY_MS, blank, shift, flip, recolor, narrow, thin,
                       wide, per_word, bitmap, word_green, drop_shadow, stack, wipe_rl,
                       reveal_center, lines_boxes, shimmer, colmix, border,
                       PRODESTRIAN_MAPS, WORD_SPANS, encode_jt, to_panel, Y)

LEGACY_MAX_FRAMES = 53          # reported for older CoolLED panels (GBFans release topic, post #13)
GIF_CHUNK = 40                  # reported GIF frame cap on newer 24-bit panels (post #15)

# Full-color palette for 24-bit panels. Amber is used for red+green: pure yellow looks
# greenish on most RGB LEDs.
RGB24 = {OFF: (0, 0, 0), R: (255, 0, 0), G: (0, 255, 0), Y: (255, 180, 0)}


def build_compact():
    """[(id, label, frames)] in the main sequence order, at most 53 frames in total."""
    A_r = narrow("GHOSTBUSTERS", R)
    A_g = recolor(A_r, G)
    B = border(narrow("FOR HIRE...", R, gap=2, space=6))
    C_red = bitmap(PRODESTRIAN_MAPS["C_red"])
    C_we, C_ready = (word_green(C_red, sp) for sp in WORD_SPANS["C"])
    D_red = bitmap(PRODESTRIAN_MAPS["D_red"])
    D_to, D_bel, D_you = (word_green(D_red, sp) for sp in WORD_SPANS["D"])
    E = thin("CALL JL5-2020", Y)
    s = "WE'RE BACK"
    G_rg, G_gr = wide(s, per_word(s, [R, G])), wide(s, per_word(s, [G, R]))
    Hf = drop_shadow(wide("WHO YA", R, space=6))
    I = drop_shadow(wide("GONNA", R))
    J = drop_shadow(wide("CALL?", R))
    K_on = bitmap(PRODESTRIAN_MAPS["K_on"])
    is_arrow = lambda x: x < 20 or x >= 60
    K_off = [[OFF if is_arrow(x) else v for x, v in enumerate(r)] for r in K_on]
    arrows = [[v if is_arrow(x) else OFF for x, v in enumerate(r)] for r in K_on]

    g2 = [[[ (R if (x % 16) < w else OFF) for x in range(W)] for _ in range(H)] for w in (1, 8, 16)]
    g2 += [[[ (G if (x % 16) < 8 else R) for x in range(W)] for _ in range(H)], blank(G)]
    seg = [
        ("A", "GHOSTBUSTERS rises red, green, swaps with upside-down flips, solid green",
         [shift(A_r, 3), A_r, A_g, A_r, flip(A_r), A_g, flip(A_g), blank(G)]),
        ("B", "FOR HIRE... (cut in, no wipe)", [B, B]),
        ("C", "WE'RE READY red, WE'RE green, READY green", [C_red, C_we, C_ready]),
        ("D", "right-to-left wipe; TO, BELIEVE, YOU green in turn; pushed down by E",
         [wipe_rl(C_red, D_red, 1)[0], D_to, D_bel, D_you, stack(E, D_red, 3)]),
        ("E", "CALL JL5-2020, then solid red", [E, E, blank(R)]),
        ("F", "GHOSTBUSTERS green, one shimmer frame, red",
         [A_g] + shimmer(A_g, (0.5,), seed=2020) + [A_r]),
        ("G", "green flash, WE'RE BACK, words swap", [blank(G), G_rg, G_rg, G_gr]),
        ("G2", "lines -> boxes, one pass in 5 steps", g2),
        ("H", "WHO YA", [Hf, Hf]),
        ("I", "GONNA", [I, I]),
        ("J", "CALL? slides up, blank", [J, J, shift(J, -4), blank()]),
        ("K", "US! alone, arrows on / off / on", [K_off, K_on, K_on, K_on, K_off, K_on]),
        ("L", "CALL JL5-2020 opens from center, holds, slides down",
         [reveal_center(E, arrows, 12), E, E, E, shift(E, 4)]),
    ]
    total = sum(len(f) for _, _, f in seg)
    assert total <= LEGACY_MAX_FRAMES, total
    return seg


def rgb_frame(f, panel=True):
    """One frame as an RGB image, 1 image pixel = 1 LED. panel=True: 96x16 with the half-pixel
    green offset (as on the CoolLED panel); panel=False: the bare 80x7 sign."""
    grid = to_panel(f) if panel else f
    im = Image.new("RGB", (len(grid[0]), len(grid)))
    im.putdata([RGB24[v] for row in grid for v in row])
    return im


def runs(frames):
    """Collapse consecutive identical frames into (frame, duration_ms) steps, as GIF players do."""
    out = []
    for f in frames:
        if out and out[-1][0] == f:
            out[-1][1] += DELAY_MS
        else:
            out.append([f, DELAY_MS])
    return out


def save_gif(steps, path, panel=True):
    """steps: [(frame, ms)], consecutive steps always differ, so the GIF keeps every step."""
    ims = [rgb_frame(f, panel) for f, _ in steps]
    ims[0].save(path, save_all=True, append_images=ims[1:], duration=[ms for _, ms in steps],
                loop=0, optimize=False, disposal=1)


def chunks(steps, n=GIF_CHUNK):
    """Split into near-equal chunks of at most n GIF frames."""
    k = -(-len(steps) // n)
    size = -(-len(steps) // k)
    return [steps[i:i + size] for i in range(0, len(steps), size)]


def save_gif_fixed(frames, path, panel=True):
    """Every animation frame stored as its own GIF frame at a fixed 200 ms, with no merging of
    repeated frames, for apps that ignore per-frame GIF durations. Pillow always merges identical
    consecutive frames, so ImageMagick writes these."""
    import shutil, subprocess, tempfile
    if not shutil.which("convert"):
        raise RuntimeError("ImageMagick 'convert' is needed for fixed-speed GIFs")
    with tempfile.TemporaryDirectory() as tmp:
        names = []
        for i, f in enumerate(frames):
            n = os.path.join(tmp, f"f{i:04d}.png")
            rgb_frame(f, panel).save(n)
            names.append(n)
        subprocess.run(["convert", "-delay", str(DELAY_MS // 10), "-loop", "0", "-dispose", "none",
                        *names, path], check=True)


def split_like_parts(parts, n=GIF_CHUNK):
    """Split each CoolLED part into near-equal pieces of at most n frames, keeping part boundaries."""
    out = []
    for part in parts:
        k = -(-len(part) // n)
        size = -(-len(part) // k)
        out += [part[i:i + size] for i in range(0, len(part), size)]
    return out


def export(out):
    os.makedirs(out, exist_ok=True)
    manifest = []

    # COMPACT: 53-frame legacy CoolLED build
    d = os.path.join(out, "compact_for_53frame_panels")
    os.makedirs(d, exist_ok=True)
    seg = build_compact()
    frames = [f for _, _, fr in seg for f in fr]
    jt, _ = encode_jt(frames)
    name = f"Ecto-1A_GB2_16x96_COMPACT-{len(frames)}frames.jt"
    with open(os.path.join(d, name), "w") as fh:
        json.dump(jt, fh, separators=(",", ":"))
    save_gif(runs(frames), os.path.join(d, "preview_COMPACT_96x16.gif"))
    manifest.append({"folder": "compact_for_53frame_panels", "kind": "COMPACT", "file": name,
                     "frames": len(frames), "seconds": len(frames) * DELAY_MS / 1000,
                     "timeline": [{"id": s, "label": l, "frames": len(f)} for s, l, f in seg]})

    # CONVERTED: full-color GIFs, whole and in <=40-frame chunks
    d = os.path.join(out, "converted_24bit_gif")
    os.makedirs(d, exist_ok=True)
    single = [f for _, _, fr in g.build_segments("single") for f in fr]
    full = [f for _, _, fr in g.build_segments("full") for f in fr]
    for tag, fr in (("single", single), ("screen-timed", full)):
        st = runs(fr)
        for panel, size in ((True, "96x16"), (False, "80x7")):
            whole = f"Ecto-1A_{tag}_{size}_24bit_ALL-{len(st)}frames.gif"
            save_gif(st, os.path.join(d, whole), panel)
            parts = chunks(st)
            names = []
            for i, c in enumerate(parts, 1):
                n = f"Ecto-1A_{tag}_{size}_24bit_chunk{i}of{len(parts)}_{len(c)}frames.gif"
                save_gif(c, os.path.join(d, n), panel)
                names.append(n)
            manifest.append({"folder": "converted_24bit_gif", "kind": "CONVERTED", "build": tag,
                             "size": size, "whole": whole, "chunks": names,
                             "gif_frames": len(st), "seconds": len(fr) * DELAY_MS / 1000})
    # FIXED-SPEED: every frame at 200 ms, for apps that ignore GIF frame durations
    d = os.path.join(out, "fixed_speed_gif")
    os.makedirs(d, exist_ok=True)
    p1, p2 = g.build_parts()
    for tag, groups in (("screen-timed", split_like_parts([p1, p2])), ("single", split_like_parts([single]))):
        for panel, size in ((True, "96x16"), (False, "80x7")):
            names = []
            for i, c in enumerate(groups, 1):
                n = f"Ecto-1A_{tag}_{size}_FIXED-200ms_{i}of{len(groups)}_{len(c)}frames.gif"
                save_gif_fixed(c, os.path.join(d, n), panel)
                names.append(n)
            manifest.append({"folder": "fixed_speed_gif", "kind": "FIXED-SPEED", "build": tag,
                             "size": size, "files": names, "frames": sum(len(c) for c in groups),
                             "seconds": sum(len(c) for c in groups) * DELAY_MS / 1000})
    with open(os.path.join(out, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
    return manifest


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Builds for other LED panels")
    ap.add_argument("--out", default="dist/other_panels")
    a = ap.parse_args()
    for m in export(a.out):
        print(m["kind"], m.get("file") or m.get("whole") or m["files"][0], m.get("frames") or m["gif_frames"], "frames")
