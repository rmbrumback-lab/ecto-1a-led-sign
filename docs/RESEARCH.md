# Research log

How the recreation evolved. Each version was driven by new reference material.

## Sources

- **GBFans reference thread:** [Screen Accurate ECTO-1A Dot Matrix LED Sign (Reference)](https://forum.gbfans.com/t/screen-accurate-ecto-1a-dot-matrix-led-sign-reference/26454). This is the primary source for the hardware, text, sequence and effects.
- **Getty Images premiere footage**, clip 1032076844, found by Kingpin. It was viewed through stills posted in the thread and is not redistributed here.
- **Book scan of WE'RE BACK**, posted by zerosum. This is the sharpest pixel reference.
- **Film stills, deleted scenes and behind-the-scenes frames** posted in the thread.
- **[JT-Edit](https://github.com/auc0le/JT-Edit)** and **[coolledx-driver](https://github.com/UpDryTwist/coolledx-driver)** for the file format and upload limits.

## v1: text model

- Built from the thread's text inventory and its draft A–L sequence.
- Used one generic 5×7 font, guessed colors, and 5-frame wipes.
- Established the JT encoder and validated it against the app-exported samples.

## v2: full frame-by-frame analysis

Built from a closer reading of the thread's scene-by-scene and premiere analysis:

- added the **green-below-red hardware offset**;
- added A's bounce, color swaps and possible flip;
- added F's green → shimmer → green → red sequence;
- matched the loop seam (L slides down, red GHOSTBUSTERS slides up);
- shortened wipes to 3 frames to free up frames for the effects.

## v3: photo analysis

Reference stills from the thread were enlarged and sampled on a fitted, perspective-corrected 80×7 grid.

- **Three fonts were discovered.** v1 and v2 had used one thin font for everything.
  - Bold wide: read from the WE'RE BACK scan. B/A/C/K are pixel-exact, and the phrase totals exactly 80 columns.
  - Bold narrow: GHOSTBUSTERS runs edge to edge.
  - Thin 5×7: CALL JL5-2020 / TO BELIEVE YOU / WE'RE READY.
- **FOR HIRE… has a green dotted border**, animated as a chase.
- **CALL JL5-2020 is amber.** The premiere close-ups show both clusters lit, with the offset visible.
- **TO BELIEVE YOU color states:** TO green with the rest red, all red, and BELIEVE amber.

## v3.1: US! arrows

The blurred green shapes beside US! were first read as crosses. On re-examination, in each frame the shaft runs away from the word and the tall head faces it. They are **arrows pointing inward** at US!.

## v4: attribution audit

Every element was checked against the thread text and the reference photos (see [ATTRIBUTION.md](ATTRIBUTION.md)). Anything without a source, or with an undocumented appearance, was removed.

- **Removed:**
  - the five lines → green boxes graphic (only described in words, so v3.1's version was invented);
  - the shimmer rendering, in A and F;
  - the bounce and upside-down flip in A (hedged in the thread);
  - the FOR HIRE border chase (the motion was inferred);
  - the C→D wipe (no source).
- **Corrected:**
  - A now has the reported **~16** red/green swaps (v3.1 had 10);
  - wipes are shown as a single solid frame of the reported color, because the wipe direction is unknown;
  - F's green→red is now a cut.
- **Flagged as unknown:** the colors of WE'RE READY, WHO YA, GONNA and CALL?, and all timing.

## v5: deleted-scene clip analysis

A 181-frame GIF of the deleted museum scene was analyzed frame by frame. Colors were calibrated against confirmed elements (red US!, green arrows, amber CALL JL5-2020).

- **Corrected:** WHO YA and CALL? are **red** (v4 showed them green).
- **Added, with measured timing:**
  - the sign goes blank for about 0.8 s after CALL?;
  - US! appears alone for about 0.6 s before the arrows;
  - the arrows show on about 1.2 s, off about 0.8 s, then on again;
  - CALL JL5-2020 is revealed outward from the center while the arrows are still lit, then holds about 2 s.
- **Video-confirmed:** L slides down and red GHOSTBUSTERS rises.
- **Lines → boxes:** confirmed to exist, in red lines and red/green fills with dividers, but still not rendered. Only a third of the sign is visible and it is out of focus.

## v6: inferred lines → boxes

At Ryan's request, the lines → boxes graphic was reconstructed rather than omitted, and is labeled **inferred** throughout.

- **Sourced:** the thread's description, plus the clip's phase order, colors and seed spacing.
- **Inferred:** 5 × 16-column sections, divider placement, full-height fill and step counts.
- **Scale check:** the clip's seed spacing is 14–15 columns against the 16 that five even sections imply.
- **Frame budget:** to fit the 9 new frames inside the 113-frame upload limit, the estimated holds in A–G and I were shortened. The measured J–L timings were left as they were.

## v7: inferred wipes and shimmer, evidence cards

At Ryan's request, the remaining undocumented effects were reconstructed, and the evidence was published:

- **Wipes:** each solid frame that stood in for a wipe is now a left-to-right sweep. The color advances over the old message, then the new one is revealed. Direction is inferred from the red sweep entering from the left in the deleted-scene clip.
- **Shimmer:** rendered as seeded random per-pixel sparkle on green GHOSTBUSTERS. In A it comes before the swaps (Getty); in F it sits between two plain green frames (film, behind-the-scenes).
- **Evidence:** `docs/evidence/` holds one card per element, with a credited source extract beside our rendering, plus the full PDF. These extracts are excluded from the MIT license.
- **Frame budget:** the extra frames were paid for from estimated holds (B, C, D, E, G, H) and one inferred G2 step. The measured J–L timings were left as they were. Still 113 frames.

## v8: TO BELIEVE YOU alternation; two-part screen-timed build

- **TO BELIEVE YOU:** following Ryan's observation, TO and BELIEVE now alternate colors (green / amber) while YOU stays red. That matches all three stills, where YOU is always red.
- **Two-part build:** a second, screen-timed version is split into two CoolLED files that play in order. Part 1 is A–F (112 frames); Part 2 is G–L (109 frames); 44.2 s in total. It uses measured J–L timing, 2.0 s message holds (from the measured CALL hold), the thread's "few seconds" shimmer, and three passes of lines → boxes. The single-file build is kept.
- Full-timing JSON and GIF exports were added for other apps.

## v9: word-by-word builds

- **TO BELIEVE YOU (correction):** v8 misread Ryan's note and kept YOU red. The highlight now moves word by word: TO (green), BELIEVE (amber), YOU (green, inferred color), with the other words red. The stills each show exactly one word highlighted.
- **WE'RE READY:** now built word by word, WE'RE first and then READY. This mirrors the sign's WE'RE-alone build of WE'RE BACK (Getty, thread post #14), following Ryan's inference.
- Still 113 frames (single) and 112 + 109 (two-part).

## v10: WE'RE-alone frame removed; WE'RE READY reverted

- WE'RE BACK no longer opens with "WE'RE" alone. At Ryan's direction, that frame from the thread's Getty description has been removed, and WE'RE BACK now opens with the green flash. The freed frames lengthen the WE'RE BACK hold.
- The v9 word-by-word build of WE'RE READY was reverted at Ryan's direction. WE'RE READY is again shown as sourced: the full phrase.
- Frame counts are unchanged.

## Open questions

- GONNA's color, and sharp frames of WHO YA / GONNA / CALL? for letter shapes.
- YOU's highlight color.
- Whether the FOR HIRE border animates.
- What the shimmer really looks like, and the real wipe direction (both currently inferred).
- The real geometry of the lines → boxes graphic (currently inferred).
- A sharp frame of the US! arrows.
- True film timing. Uninterrupted footage of the full loop isn't known to exist.

Contributions with better reference are welcome via an issue or pull request.
