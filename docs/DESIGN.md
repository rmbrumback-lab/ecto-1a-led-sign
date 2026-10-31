# Design

This document records how every element of the recreation was decided: what the reference showed, how it was measured, and what was estimated.

## 1. The physical sign

| Property | Value | Source |
|---|---|---|
| Resolution | 80 × 7 pixels | GBFans thread (counted from film frames) |
| Pixel | a cluster of 4 LEDs, never driven separately | GBFans thread close-ups |
| Colours | separate red and green clusters per pixel; both lit reads as amber | GBFans thread |
| Vertical offset | green clusters sit lower than red | GBFans thread; visible in the WE'RE BACK scan |
| Count | 560 pixels per colour, 4,480 LEDs per sign | GBFans thread |
| Two signs | one per side, always showing the same content | GBFans thread |
| Manufacturer | unknown | thread investigation is ongoing |

### Modelling choices

- **Logical model:** 80 × 7 grid, each pixel `0` off, `1` red, `2` green, `3` both. This matches the 4-state encoding prodestrian proposed in the thread, so the data can be shared with other projects as-is.
- **Panel mapping (16×96):** the 80 columns map 1:1, centred with 8 columns of margin each side. Each sign row becomes 2 panel rows. Red uses panel rows `2y, 2y+1`; green uses `2y+1, 2y+2`. So green sits half a sign pixel lower, as on the real hardware. A red+green pixel shows red on top, amber in the middle, and green underneath. 15 of the 16 panel rows are used.

![Offset close-up](images/offset_closeup.png)

## 2. Fonts

The sign uses three fonts. They were identified by enlarging the reference stills and sampling them on a fitted 80×7 grid; where the sign was photographed at an angle, the grid was perspective-corrected.

### Bold wide — WE'RE BACK, WHO YA, GONNA, CALL?, US!

![bold wide](images/font_bold_wide.png)

- Letters are 7 columns wide with 2-pixel strokes. Letters are separated by 2 blank columns, and words by 2.
- **B, A, C, K** were read pixel-for-pixel from the green half of the hi-res WE'RE BACK book scan, where every LED cluster is distinct. B has a 2-column serif on its top and bottom rows.
- **W, E, ', R** were read from the red half of the same scan. The red is softer, so these are slightly less certain. W is 10 wide, with an "LIJ" shape: a centre stroke from row 2 and joined feet.
- **Check:** W10+E7+'3+R7+E7 plus gaps is 42 columns, a 2-column space follows, and B9+A7+C7+K7 plus gaps is 36 columns. That totals exactly **80**, so the phrase fills columns 0–79 as in the photo.
- H, O, Y, G, N, L, U, S, ?, ! are drawn in the same style but **not seen in any reference** (estimate).
- `<` and `>` are the US! arrows. In both premiere frames the shaft runs away from the word and the tall head faces it, so both arrows point inward.

### Bold narrow — GHOSTBUSTERS, FOR HIRE…

![bold narrow](images/font_bold_narrow.png)

- Letters are 6 wide (H and S are 5), with 2-pixel strokes and 1-column gaps.
- Sampled from the night GHOSTBUSTERS still with a tilted-grid fit. **GHOSTBUSTERS spans columns 0–78**, edge to edge as in the photo.
- FOR HIRE… uses the same font with 2-column letter gaps and 6-column word spaces, which matches its looser spacing in the still. The ellipsis is three 2×2 dots.

### Thin 5×7 — TO BELIEVE YOU, CALL JL5-2020 (and WE'RE READY, unconfirmed)

![thin](images/font_thin.png)

- Classic 5×7 with 1-column gaps and 3-column spaces.
- Confirmed by premiere-footage close-ups of CALL, BELIEVE and a thin amber "WE". In the close-up, the E's top and bottom rows are 5 pixels and its middle row is 4.
- TO BELIEVE YOU is 75 columns wide, so it fills the sign, matching the film still.

## 3. Colours per frame

| Frame | Colours | Evidence |
|---|---|---|
| A GHOSTBUSTERS | red; green; ~16 red/green swaps; settles green | night still (red); thread: film 01:22:59 and Getty clip |
| B FOR HIRE… | red text, green border | night still |
| C WE'RE READY | **unknown**, shown amber (font also unconfirmed) | no clear reference |
| D TO BELIEVE YOU | all red / TO green / BELIEVE amber, in that order | three observed states; the order is not documented |
| E / L CALL JL5-2020 | amber | premiere close-ups (red and green clusters both lit) |
| F GHOSTBUSTERS | green, then red | thread (film 01:23:28; Getty clip) |
| G WE'RE BACK | WE'RE red, BACK green, then swapped | book scan; thread (Getty clip) |
| H WHO YA / I GONNA / J CALL? | **unknown**, shown green / red / green | thread had crops; not supplied |
| K US! | red word, green arrows | premiere frames |

## 4. Sequence and effects

![Storyboard](images/storyboard.png)

The order and the transitions come from the thread's analysis of the film (timecodes 00:37:06, 00:38:10, 00:49:44, 01:22:59–01:24:54), deleted scenes, behind-the-scenes footage, and the 42-second Getty premiere clip. **Only effects whose appearance is documented are drawn.** Per-element sources are in [ATTRIBUTION.md](ATTRIBUTION.md).

| Effect | Implementation | Source |
|---|---|---|
| L slides down, A slides up (red) | content shifted 2–3 rows per frame | film 01:23:17; museum arrival |
| J slides up and out | as above | Getty clip |
| D wipes down as E slides in from the top | E above D on a 15-row strip, viewed at offsets 5, then 2 | film 01:24:46; Getty clip |
| Red/green swaps (A) | the same glyphs alternate colour every frame, 16 times | Getty clip: "about 16 times" |
| Colour wipe (A→B, B→C, E→F) | **one solid frame of the reported colour**, then the next message. No sweep is drawn because the wipe direction is undocumented. | thread reports the colours |
| Green → red (F) | cut | thread |
| Solid red (F→G), green flash (G) | one solid frame | Getty clip |
| Word colour swap (G) | WE'RE/BACK alternate red/green | Getty clip |
| Static border (B) | perimeter pixels green where the text is unlit | FOR HIRE still |
| Arrow blink (K) | arrows on/off over 5 frames | Getty clip |

### Known but not rendered

| Effect | Where | Why it's not drawn |
|---|---|---|
| Shimmer | A (before the swaps), F | its look is undocumented; the green frame is held instead |
| Five sweeping lines → green boxes | between G and H | described in words only: line colour, positions, box size and timing are unknown |
| Wipe motion | A→B, B→C, E→F, F | direction is undocumented |
| Possible slide/flip in A | A | the thread hedges it ("seems", "possibly") |

## 5. Timing

The CoolLED1248 format has **one delay for the whole animation**. Holds are therefore made by repeating frames. The upload protocol limits a 16×96 animation to 113 frames (65,535 bytes ÷ 576 bytes per frame).

At 200 ms per frame this gives a 21.8-second loop of 109 frames. **All durations are estimates.** No uninterrupted footage of the full loop is known, and message holds of 0.8–1.4 s are likely shorter than the real sign's. A microcontroller build is not bound by the frame limit: use `ecto1a_playlist.json` and stretch the holds.
