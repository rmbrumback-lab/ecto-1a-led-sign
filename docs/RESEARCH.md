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

## Open questions

- The WHO YA, GONNA and CALL? frames: their font and colours, if reference images exist.
- Exact border-chase pattern and speed.
- A sharp frame of the US! arrows.
- True film timing. Uninterrupted footage of the full loop isn't known to exist.

Contributions with better reference are welcome via an issue or pull request.
