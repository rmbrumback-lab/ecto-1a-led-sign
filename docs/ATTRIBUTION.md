# Attribution audit

Every screen, text, color and effect in the animation is listed here with its source.

**Rule applied (v4):** an element stays only if a reference shows it, or the GBFans thread reports it as an observation. Reports hedged as "possibly", "seems", "my guess" or "?" don't count. Where something is confirmed to exist but nobody has documented *how it looks*, it is **not rendered**, because rendering it would mean inventing it. **Exceptions, at Ryan's request (v6–v7):** three effects that are confirmed to exist but whose look is undocumented are rendered as clearly labeled **inferred** reconstructions: the lines → boxes graphic (G2), the color wipes, and the shimmer. Their sourced and inferred parts are separated below. **v11:** prodestrian's review and new reference (8 November 2026, T #41 and RT #12) turned most of the lines → boxes graphic, WE'RE READY, TO BELIEVE YOU, US! and the GHOSTBUSTERS flip into sourced elements; the changes are marked **v11** below. Visual evidence for every row is in [evidence/](evidence/), one card per element.

Sources:

- **T** — the GBFans thread [Screen Accurate ECTO-1A Dot Matrix LED Sign (Reference)](https://forum.gbfans.com/t/screen-accurate-ecto-1a-dot-matrix-led-sign-reference/26454). Post #1–3 and #14 are by prodestrian; #10 is by zerosum.
- **T #41** — prodestrian, reference thread, 8 November 2026: pixel maps of WE'RE READY and TO BELIEVE YOU (each word turning green in turn) and of the lines → boxes wipe, read from the Getty premiere footage; notes on the shimmer and on WHO YA / GONNA / CALL? colors.
- **RT #12** — prodestrian, [release topic](https://forum.gbfans.com/t/screen-accurate-ecto-1a-sign-animation-coolled-file-open-data-for-any-led-build/219532) post #12, 8 November 2026: review of v10 (WHO YA spacing, WE'RE READY red, drop shadow on WHO YA / GONNA / CALL? / US!, no gaps in the lines → boxes), a pixel map of US! with its drop shadow and arrows, and a short clip showing the upside-down GHOSTBUSTERS flip (**X1**).
- Pixel maps from T #41 and RT #12 were decoded from prodestrian's 2000 × 160 diagrams into 80 × 7 frames; the images themselves stay on GBFans.
- **P** — reference photos from that thread, used for measurement:
  - P1: night still, GHOSTBUSTERS
  - P2: night still, FOR HIRE…
  - P3: film still, TO BELIEVE YOU
  - P4: WE'RE BACK video still
  - P5–P6: premiere frames, US!
  - P7: film still, CALL JL5-2020 after US!
  - P8–P9: museum stills, TO BELIEVE / CALL JL5-
  - P10–P11: deleted-scene GIFs, red GHOS…
  - P12–P13: Getty premiere close-ups, CALL JL5-2020
  - P14: book scan, WE'RE BACK (a *Ghostbusters II* production still, Columbia Pictures / Sony; source book unidentified)
  - P15: Getty close-up, thin amber "WE"/"VE"
  - P16: Getty close-up, red O, amber BELIEVE
  - Credits and rights holders for every image: [evidence/README.md](evidence/README.md)
- **V1** — deleted-scene GIF (Hardemeyer at the museum): 181 frames, 14.8 s, 654×376. It matches the thread's description of `i.imgur.com/yjkGYPb.gif`. The sign sits out of focus behind the actors and is partly blocked, so letter shapes can't be read, but colors, transitions and timing can. Colors were calibrated against elements already confirmed: US! red (green/red ratio 0.65), the arrows green (0.95), CALL JL5-2020 amber (0.85). Frame numbers below refer to V1.

## Hardware

| Element | Status | Source |
|---|---|---|
| 80 × 7 pixel matrix | ✅ kept | T #1: counted from film frames |
| Red and green clusters; both lit reads as amber | ✅ kept | T #1; Kingpin, page 2 |
| Green clusters sit lower than red | ✅ kept | T #1 (WE'RE/BACK misalignment); P14 |

## Fonts

| Element | Status | Source |
|---|---|---|
| Bold narrow font, GHOSTBUSTERS layout | ✅ kept | P1, sampled on grid |
| Bold narrow, FOR HIRE… | ✅ kept | P2 |
| Bold wide B, A, C, K | ✅ kept, pixel-exact | P14 |
| Bold wide W, E, ', R | ✅ kept | P14 (red, softer focus) |
| Bold wide H, O, Y, G, N, L, U, S, ?, ! | ⚠️ kept, **glyphs estimated** | V1 shows WHO YA, CALL? and US! in a bold style, but too blurred to read letter shapes |
| Thin 5×7 font family | ✅ kept | P12, P13, P16 (CALL, BELIEVE, O) |
| WE'RE READY and TO BELIEVE YOU: exact letters and layout | ✅ **v11**, prodestrian's pixel maps used verbatim | T #41 |
| Thin glyphs not seen in a reference (e.g. R, A, D, Y, T, U) | ⚠️ kept, standard 5×7 forms | Family confirmed; individual letters not seen |

## Screens (text)

| ID | Text | Status | Source |
|---|---|---|---|
| A | GHOSTBUSTERS | ✅ | T #2; P1 |
| B | FOR HIRE… | ✅ | T #2; P2 |
| C | WE'RE READY | ✅ | T #2 |
| D | TO BELIEVE YOU | ✅ | T #2; P3, P8, P16 |
| E | CALL JL5-2020 | ✅ | T #2; P12, P13 |
| F | GHOSTBUSTERS (second instance) | ✅ | T #3, #14 |
| G | WE'RE BACK | ✅ | T #2; P4, P14 |
| H | WHO YA (two words, full word space — **v11**) | ✅ | T #2; RT #12 |
| I | GONNA | ✅ | T #2 |
| J | CALL? | ✅ | T #2 |
| K | US! | ✅ | T #2; P5, P6 |
| L | CALL JL5-2020 (second instance) | ✅ | T #14; P7 |
| — | Playback order A→L | ✅ | T #14 (film timecodes + Getty clip) |

## Colors

| Element | Status | Source |
|---|---|---|
| A: red, rapid red/green swaps, settles green | ✅ | T #14: film 01:22:59; Getty clip, about 16 swaps; P1 |
| B: red text, green border | ✅ | P2 |
| C: WE'RE READY | ✅ **v11**: thin font, red; WE'RE then READY turn green in turn | T #41 (pixel maps); RT #12 ("red, not yellow"). Replaces the amber estimate. |
| D: all red, then TO, BELIEVE and YOU each turn green in turn | ✅ **v11** | T #41 (pixel maps), consistent with P3 and P8 and Ryan's word-by-word observation. Replaces v9–v10's amber BELIEVE (read from P16) and inferred green YOU. The rate is estimated. |
| E, L: amber | ✅ | P12, P13, P7 |
| F: green, then red | ✅ | T #14 |
| G: WE'RE red and BACK green, words swapping | ✅ | T #14 (Getty); P4, P14 |
| H, I, J: WHO YA, GONNA, CALL? | ✅ **v11**: red letters with a green drop shadow one column to the right | RT #12 (drop shadow); red letters measured in V1 (frames 44–57 ratio 0.62, frames 66–75 ratio 0.60). prodestrian reads all three as amber in the Getty footage (T #41); red letters plus a green shadow reconcile both observations. GONNA isn't visible in V1 and follows the other two. |
| K: US! red with green drop shadow; green arrows (no shadow) pointing inward | ✅ **v11**, prodestrian's pixel map used verbatim, including arrow positions (columns 8–15 and 64–71) | RT #12; P5, P6; T #14 ("green arrows start to blink") |

## Effects and transitions

| Element | v3.1 | v4 | Source / reason |
|---|---|---|---|
| L slides down, A slides up in red | rendered | ✅ **kept** | T #14 (film 01:23:17); museum shot 00:49:44 |
| A: bounce (slides up/down while swapping) | rendered | ❌ **removed** | T #14 says it "seems to", from a blurry shot |
| A: upside-down flip | rendered | ✅ **restored (v11)**: during the swaps GHOSTBUSTERS also shows mirrored top to bottom, letters in place, in red and green | RT #12 and clip X1 (prodestrian), with the deleted museum scene and behind-the-scenes photos he cites. Removed in v4 when the thread only said "possibly". **The order of upright and flipped states is estimated.** |
| A: shimmer before the swaps | not shown | ⚠️ **v11**: a short repeating cycle of random sparkle masks, then GHOSTBUSTERS again in green | T #14 (Getty): shimmer present for a few seconds before the swaps. T #41: the pattern looks partly repeated, and a suitably randomized sequence is fine. The exact pixels are **inferred**. |
| A: rapid red/green swaps | 10 | ✅ **16 swaps** | T #14: "about 16 times" |
| A→B: solid green, then B | rendered as a wipe | ⚠️ **solid green (sourced), then B wiped in left to right (INFERRED, v7)** | T #14 ("solid green frame, which wipes to frame B"). Direction inferred from the left-to-right sweep in V1 frames 20–23. |
| B: border chase animation | rendered | ❌ **removed**, border static | Motion was inferred from uneven dots in P2 and isn't documented |
| B→C: green wipe | sweep | ⚠️ **green covers B left to right, solid green, C wiped in (INFERRED direction, v7)** | T #14 (Getty: solid green wipe). Direction inferred from V1. |
| C→D transition | green wipe | ✅ **v11: right-to-left wipe** (TO BELIEVE YOU replaces WE'RE READY from the right edge) | T #41 ("Right to Left Wipe transition"). Direction sourced; the wipe's look is **inferred** as a moving edge. |
| D: color states | rendered | ✅ **v11**, see Colors | T #41; P3, P8 |
| D→E: D wipes down, E slides in from the top | rendered | ✅ kept | T #14 (film 01:24:46; Getty) |
| E→F: red wipe | sweep | ⚠️ **red covers E left to right, solid red, F wiped in green (INFERRED direction, v7)** | T #14 ("transitions out with a red wipe into frame F"). Direction inferred from V1. |
| F: shimmer | random dropout | ⚠️ **v11**: green, sparkle from the same repeating cycle, green again | T #14 (film 01:23:28); T #3 behind-the-scenes ("GHOSTBUSTERS, then shimmer, then GHOSTBUSTERS again"). Look inferred. |
| F: green-to-red wipe | half-sweep | ⚠️ **left-to-right half step, then red (INFERRED direction, v7)** | T #14 (Getty: F "wiping from green to red"). Direction inferred from V1. |
| F→G: solid red | rendered | ✅ kept | T #14 (Getty) |
| G: green flash → WE'RE BACK → words swap | rendered | ✅ kept | T #14 (Getty) |
| G: "WE'RE" alone before the green flash | rendered (v2–v9) | ❌ **removed (v10)**, not used anywhere | T #14 lists it before WE'RE BACK (Getty description). Ryan judges it doesn't belong there. It was briefly reused as a WE'RE READY build (v9–v10), then reverted, so WE'RE READY is shown as sourced: the full phrase. |
| Five lines → green boxes | rendered | ✅ **v11: sourced shape** — five equal 16-column boxes filling the sign with **no gaps**; in each box a red line starts at the left edge and grows to the full 16 columns, then shrinks from that same edge, revealing green; loops | T #41 (pixel map of one wipe step, from the Getty footage) and RT #12 (the apparent gaps are an optical illusion from the offset LEDs); consistent with V1 frames 6–31. v6–v10 showed dark or red divider columns and green growing from each box's center: **removed**. **Inferred:** the number of steps per pass. |
| J slides upward, then K | rendered | ✅ kept | T #14 (Getty) |
| Blank sign between CALL? and US! | not shown | ✅ **added**, about 0.8 s | V1 frames 81–90 (800 ms) |
| US! appears before the arrows | not shown | ✅ **added**, about 0.6 s | V1 frames 91–98 (640 ms) |
| K: arrows blink | rendered | ✅ **retimed**: on about 1.2 s, off 0.8 s, on 0.6 s | V1 frames 99–131 (read visually; the camera moves) |
| K→L: CALL JL5-2020 revealed outward from the center while the arrows stay lit | not shown | ✅ **added** | V1 frames 132–137 (470 ms): frame 132 shows "JL5" between the arrows, frame 135 "L JL5-20", then the full text with the arrows off |
| L: hold | estimate | ✅ **retimed** to about 2 s | V1 frames 138–164 (2,140 ms) |
| L: slides down, red GHOSTBUSTERS rises | rendered | ✅ kept, **video-confirmed** | T #14; V1 frames 165–170 (390 ms) |

## Timing

**Single file (113 frames):** J (blank), K and L are **measured from V1**, rounded to 200 ms frames. V1 is a GIF, so its timing is assumed close to, but not guaranteed to be, real time. All other durations are **estimates**, compressed to fit the 113-frame CoolLED upload limit. The 16 swaps follow T #14.

**Two-part, screen-timed version (111 + 109 frames, 44.0 s):** there are no frame-budget compromises.

| Element | Duration | Basis |
|---|---|---|
| J, K, L | as measured (2.0 s, 3.2 s, 3.0 s) | **measured**, V1 |
| A swaps | 16 frames, upright and flipped | **sourced**, T #14, RT #12; order **estimated** |
| A shimmer | 1.6 s; F shimmer 1.2 s | T #14 says "a few seconds"; **estimated** within that |
| Message holds (B, C, E, H, I) | 2.0 s each | **estimated** from the measured 2.1 s hold of CALL JL5-2020 (V1) |
| D word-by-word highlight | 2.4 s plus the push | **estimated** |
| G2 lines → boxes | 3 passes, 5.4 s | number of passes **estimated**; T #14 says it "loops multiple times" |
| Wipes | 2 half-steps each side; C→D right to left (T #41) | other directions **inferred** |

Part 1 = A–F, Part 2 = G–L. The parts join at the WE'RE BACK cut, and Part 2's ending (CALL JL5-2020 sliding down) leads straight into Part 1's opening (GHOSTBUSTERS rising).

## How to help

These would replace estimates with facts:

- pixel maps of **WHO YA, GONNA and CALL?**, for exact letter shapes and shadow;
- the **color wipes** (prodestrian plans to look at these), to confirm the inferred left-to-right sweeps;
- the exact **order of upright and flipped** GHOSTBUSTERS during the swaps;
- whether the **FOR HIRE border** moves.
