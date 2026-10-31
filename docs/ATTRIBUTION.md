# Attribution audit

Every screen, text, colour and effect in the animation is listed here with its source.

**Rule applied (v4):** an element stays only if a reference shows it, or the GBFans thread reports it as an observation. Reports hedged as "possibly", "seems", "my guess" or "?" don't count. Where something is confirmed to exist but nobody has documented *how it looks*, it is **not rendered**, because rendering it would mean inventing it.

Sources:

- **T** — the GBFans thread [Screen Accurate ECTO-1A Dot Matrix LED Sign (Reference)](https://forum.gbfans.com/t/screen-accurate-ecto-1a-dot-matrix-led-sign-reference/26454). Post #1–3 and #14 are by prodestrian; #10 is by zerosum.
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
  - P14: book scan, WE'RE BACK
  - P15: Getty close-up, thin amber "WE"/"VE"
  - P16: Getty close-up, red O, amber BELIEVE

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
| Bold wide H, O, Y, G, N, L, U, S, ?, ! | ⚠️ kept, **glyphs estimated** | No reference supplied. WHO YA / GONNA / CALL? / US! need these letters. |
| Thin 5×7 font family | ✅ kept | P12, P13, P16 (CALL, BELIEVE, O) |
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
| H | WHO YA | ✅ | T #2 |
| I | GONNA | ✅ | T #2 |
| J | CALL? | ✅ | T #2 |
| K | US! | ✅ | T #2; P5, P6 |
| L | CALL JL5-2020 (second instance) | ✅ | T #14; P7 |
| — | Playback order A→L | ✅ | T #14 (film timecodes + Getty clip) |

## Colours

| Element | Status | Source |
|---|---|---|
| A: red, rapid red/green swaps, settles green | ✅ | T #14: film 01:22:59; Getty clip, about 16 swaps; P1 |
| B: red text, green border | ✅ | P2 |
| C: WE'RE READY colour **and font** | ⚠️ **unknown**, shown thin amber | P15 could be WE'RE or BELIEVE's "VE" |
| D: all red / TO green / BELIEVE amber | ✅ states observed | P8, P3, P16. Order of the states is not documented. |
| E, L: amber | ✅ | P12, P13, P7 |
| F: green, then red | ✅ | T #14 |
| G: WE'RE red then BACK green, words swapping | ✅ | T #14 (Getty); P4, P14 |
| H, I, J colours | ⚠️ **unknown**, shown green / red / green | Thread had crops; not supplied here |
| K: red US!, green arrows | ✅ | P5, P6; T #14 ("green arrows start to blink") |

## Effects and transitions

| Element | v3.1 | v4 | Source / reason |
|---|---|---|---|
| L slides down, A slides up in red | rendered | ✅ **kept** | T #14 (film 01:23:17); museum shot 00:49:44 |
| A: bounce (slides up/down while swapping) | rendered | ❌ **removed** | T #14 says it "seems to", from a blurry shot |
| A: upside-down flip | rendered | ❌ **removed** | T #14 says "possibly"; T #3 marks it "?" |
| A: shimmer before the swaps | not shown | ⏸ **not rendered**, held green instead | T #14 (Getty): shimmer clearly present, but its appearance is undocumented |
| A: rapid red/green swaps | 10 | ✅ **16 swaps** | T #14: "about 16 times" |
| A→B: solid green, then B | rendered as a wipe | ✅ **solid green frame, then B** | T #14. Wipe direction is undocumented, so no sweep is drawn. |
| B: border chase animation | rendered | ❌ **removed**, border static | Motion was inferred from uneven dots in P2 and isn't documented |
| B→C: green wipe | sweep | ✅ **solid green frame, then C** | T #14 (Getty: solid green wipe). Direction undocumented. |
| C→D transition | green wipe | ❌ **removed**, straight cut | No source for this transition |
| D: colour states | rendered | ✅ kept | P3, P8, P16 |
| D→E: D wipes down, E slides in from the top | rendered | ✅ kept | T #14 (film 01:24:46; Getty) |
| E→F: red wipe | sweep | ✅ **solid red frame, then F** | T #14. Direction undocumented. |
| F: shimmer | random dropout | ⏸ **not rendered**, held green | T #14 (film 01:23:28). Appearance undocumented. |
| F: green-to-red wipe | half-sweep | ✅ **cut green → red** | T #14. Direction undocumented. |
| F→G: solid red | rendered | ✅ kept | T #14 (Getty) |
| G: "WE'RE" red → green flash → WE'RE BACK → words swap | rendered | ✅ kept | T #14 (Getty) |
| Five lines sweeping, then green boxes | rendered | ❌ **removed** | T #14 describes it only in words. Line colour, line positions, box size and timing are unknown, so v3.1's version was invented. |
| J slides upward, then K | rendered | ✅ kept | T #14 (Getty) |
| K: arrows blink | rendered | ✅ kept | T #14 (Getty) |
| L: slides down | rendered | ✅ kept | T #14 |

## Timing

All durations are **estimates**. No uninterrupted footage of the full loop is known (T #3). The 16 swaps follow T #14. Holds are sized to fit the CoolLED upload limit of 113 frames at 16×96.

## How to help

These would replace estimates with facts:

- clear frames of **WHO YA, GONNA, CALL?** (the thread has crops);
- a clear look at the **shimmer** and the **lines → boxes** graphic;
- the **direction of the wipes**;
- whether the **FOR HIRE border** moves.
