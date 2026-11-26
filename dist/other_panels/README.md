# Files for other panels

> **These are not the main files.** The screen-accurate animation is in [`../`](../): the single CoolLED file and the two-part screen-timed set. Use those if your panel can take them. The files here exist only for panels that can't, and each one says how it differs.

| Your panel or app | Use | Kind | How it differs from the main files |
|---|---|---|---|
| CoolLED1248 16×96 that loads `.jt` files and plays 113 frames | [`../Ecto-1A_GB2_16x96.jt`](../Ecto-1A_GB2_16x96.jt), or Part 1 + Part 2 in [`../two_part/`](../two_part/) | **MAIN** | — |
| Older CoolLED1248 16×96, capped at 53 frames and one program | [`compact_for_53frame_panels/`](compact_for_53frame_panels/) | **COMPACT** | Shortened animation (10.4 s): every message, in order, but shorter holds, no wipes except the right-to-left one, one shimmer frame, 4 color swaps and one lines → boxes pass. **Not screen-timed.** |
| Newer 24-bit (full-color) panels or apps that import GIFs | [`converted_24bit_gif/`](converted_24bit_gif/) | **CONVERTED** | The main animation, frame for frame and at the same timing, re-encoded as full-color GIFs. Only the file format differs. |
| Apps that play every GIF frame at one speed (ignoring frame durations) | [`fixed_speed_gif/`](fixed_speed_gif/) | **FIXED-SPEED** | The same animation and colors as CONVERTED, but every frame is stored separately at 200 ms, so timing is right even when the app ignores durations. Files are larger and have more frames. |

## COMPACT: 53-frame CoolLED build

- `Ecto-1A_GB2_16x96_COMPACT-52frames.jt`: 52 frames at 200 ms, 10.4 s loop, for panels that reject longer animations (reported by spectregater on the GBFans release topic).
- `preview_COMPACT_96x16.gif`: what it looks like.
- What's kept: all 13 segments in order, with the same messages, fonts and colors as the main build (WE'RE READY / TO BELIEVE YOU word highlights, drop shadows, the flip, the lines → boxes, the US! arrows and the center reveal).
- What's cut: the shimmer is one frame; the red/green swaps are 4 instead of about 16; the wipes into FOR HIRE…, WE'RE READY and the second GHOSTBUSTERS are cuts; holds are 1–3 frames; the lines → boxes run once, in 5 steps.

## CONVERTED: 24-bit GIFs

Two builds, each in two sizes, each whole and split into chunks of **40 frames or fewer** (a cap reported on newer panels):

| File pattern | Build | Size |
|---|---|---|
| `Ecto-1A_single_96x16_24bit_*` | single file (22.6 s) | 96×16 panel layout, with the green half a pixel lower, as on the real sign |
| `Ecto-1A_single_80x7_24bit_*` | single file (22.6 s) | bare 80×7 sign, 1 image pixel = 1 LED |
| `Ecto-1A_screen-timed_96x16_24bit_*` | screen-timed (44.0 s) | 96×16 panel layout |
| `Ecto-1A_screen-timed_80x7_24bit_*` | screen-timed (44.0 s) | bare 80×7 sign |

- `…_ALL-<n>frames.gif` is the whole loop. `…_chunk<i>of<k>_<n>frames.gif` are the pieces; play them in order.
- **Frame counts are GIF frames.** Repeated frames are stored once with a longer duration (as GIF players expect), so the single build is 79 GIF frames for its 113 animation frames, and the screen-timed build is 117 for 220. If your app ignores per-frame durations, holds will play too fast: use **FIXED-SPEED** below.
- Colors: red `#FF0000`, green `#00FF00`, and red + green as amber `#FFB400`, because pure yellow looks greenish on most RGB LEDs.

## FIXED-SPEED: GIFs for apps that ignore frame durations

Some apps play every GIF frame at the same speed, whatever durations the file stores. These GIFs store **every animation frame separately at 200 ms**, so they play at the right speed in those apps. Based on a report by spectregater on the GBFans release topic, who built the same thing from the two-part files.

| Files | Build | Pieces |
|---|---|---|
| `Ecto-1A_screen-timed_96x16_FIXED-200ms_<i>of6_<n>frames.gif` | screen-timed (44.0 s) | 6, following the CoolLED parts: 1–3 = Part 1 (A–F), 4–6 = Part 2 (G–L) |
| `Ecto-1A_screen-timed_80x7_FIXED-200ms_<i>of6_<n>frames.gif` | screen-timed, bare 80×7 | same 6 pieces |
| `Ecto-1A_single_96x16_FIXED-200ms_<i>of3_<n>frames.gif` | single file (22.6 s) | 3 |
| `Ecto-1A_single_80x7_FIXED-200ms_<i>of3_<n>frames.gif` | single file, bare 80×7 | 3 |

- Every piece is **40 frames or fewer**. Play them in order (most apps let you queue several).
- Same colors and frames as the main build; checked frame by frame against the source.

## Regenerating

```bash
cd src && python -m ecto1a.variants --out ../dist/other_panels
```

Fixed-speed GIFs need ImageMagick (`convert`), because Pillow merges repeated frames.

`manifest.json` lists every file, its kind, frame count and length. Credits and sources are the same as the main build: see the repository README and [docs/ATTRIBUTION.md](../../docs/ATTRIBUTION.md).
