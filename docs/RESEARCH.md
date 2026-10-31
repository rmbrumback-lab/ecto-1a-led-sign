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
- Used one generic 5×7 font, guessed colours, and 5-frame wipes.
- Established the JT encoder and validated it against the app-exported samples.

## v2: full frame-by-frame analysis

Built from a closer reading of the thread's scene-by-scene and premiere analysis:

- added the **green-below-red hardware offset**;
- added A's bounce, colour swaps and possible flip;
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
- **TO BELIEVE YOU colour states:** TO green with the rest red, all red, and BELIEVE amber.

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
  - wipes are shown as a single solid frame of the reported colour, because the wipe direction is unknown;
  - F's green→red is now a cut.
- **Flagged as unknown:** the colours of WE'RE READY, WHO YA, GONNA and CALL?, and all timing.

## v5: deleted-scene clip analysis

A 181-frame GIF of the deleted museum scene was analysed frame by frame. Colours were calibrated against confirmed elements (red US!, green arrows, amber CALL JL5-2020).

- **Corrected:** WHO YA and CALL? are **red** (v4 showed them green).
- **Added, with measured timing:**
  - the sign goes blank for about 0.8 s after CALL?;
  - US! appears alone for about 0.6 s before the arrows;
  - the arrows show on about 1.2 s, off about 0.8 s, then on again;
  - CALL JL5-2020 is revealed outward from the centre while the arrows are still lit, then holds about 2 s.
- **Video-confirmed:** L slides down and red GHOSTBUSTERS rises.
- **Lines → boxes:** confirmed to exist, in red lines and red/green fills with dividers, but still not rendered. Only a third of the sign is visible and it is out of focus.

## Open questions

- GONNA's colour, and sharp frames of WHO YA / GONNA / CALL? for letter shapes.
- Whether the FOR HIRE border animates.
- What the shimmer and the lines → boxes graphic actually look like, and the direction of the wipes.
- A sharp frame of the US! arrows.
- True film timing. Uninterrupted footage of the full loop isn't known to exist.

Contributions with better reference are welcome via an issue or pull request.
