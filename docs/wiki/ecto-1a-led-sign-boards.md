![Ecto-1A LED sign boards, recreated](IMG:hero.png)

The **Ecto-1A LED sign boards** are the two roof-mounted dot-matrix signs added to the Ecto-1 for *Ghostbusters II* (1989), when the car was upgraded to the Ecto-1A. One board faces each side of the car and both always show the same content: a looping sequence of red, green and amber messages such as GHOSTBUSTERS, WE'RE BACK and WHO YA GONNA CALL? US!, along with the phone number CALL JL5-2020.

This page collects what the community has worked out about the boards: the hardware, the full message list and running order, the fonts, colours and animations, and build plans and files for making a screen-accurate replica. Most of it comes from the GBFans reference thread *Screen Accurate ECTO-1A Dot Matrix LED Sign (Reference)*.[^thread] Details that are still uncertain are marked **unconfirmed**, and effects that have been reconstructed rather than observed are marked **inferred**.

## Hardware

- **Resolution:** 80 columns × 7 rows, counted from film frames.[^thread]
- **Pixels:** each pixel is a cluster of 4 LEDs. The clusters are never driven separately.[^thread]
- **Colours:** every pixel has a red cluster and a green cluster. Lighting both reads as amber or yellow on screen; there is no separate yellow LED.[^thread][^kingpin]
- **Green offset:** the green clusters sit slightly lower than the red ones. It shows wherever red and green text meet, for example where "BACK" doesn't line up with "WE'RE".[^thread][^book]
- **LED count:** 560 pixels per colour, 4,480 LEDs per board.[^thread]
- **Two boards**, one per side, always showing the same content.[^thread]
- **Manufacturer:** unknown. The thread's investigation is ongoing.

![Panel mapping](IMG:plans/panel_mapping.png)

## Messages

The boards cycle through twelve screens. The IDs A–L follow prodestrian's breakdown in the reference thread.[^thread]

- **A — GHOSTBUSTERS:** bold narrow font, edge to edge. Red, then green, with rapid red/green swaps.
- **B — FOR HIRE…:** bold narrow font, red text inside a green border.
- **C — WE'RE READY:** font and colour **unconfirmed**. Shown here in the thin font in amber.
- **D — TO BELIEVE YOU:** thin font. Red, with one word highlighted at a time: TO in green, BELIEVE in amber, then YOU (YOU's colour is **inferred** as green).
- **E — CALL JL5-2020:** thin font, amber.
- **F — GHOSTBUSTERS:** second appearance, green and then red.
- **G — WE'RE BACK:** bold wide font, filling all 80 columns. WE'RE red and BACK green, then the colours swap.
- **G2 — five lines → green boxes:** a graphic between WE'RE BACK and WHO YA (see *Inferred effects*).
- **H — WHO YA:** bold wide font, red.
- **I — GONNA:** bold wide font, colour **unconfirmed** (shown red).
- **J — CALL?:** bold wide font, red.
- **K — US!:** bold wide font, red, between two green arrows that point inward at the word.
- **L — CALL JL5-2020:** second appearance, amber, which then loops back to A.

## Fonts

Enlarging the reference stills and sampling them on a fitted 80 × 7 grid showed that the boards use **three different fonts**.

- **Bold wide** (WE'RE BACK, WHO YA, GONNA, CALL?, US!): 7-column letters with 2-pixel strokes. B, A, C and K were read pixel for pixel from a book scan of WE'RE BACK,[^book] and the phrase totals exactly 80 columns. The letters of WHO YA, GONNA, CALL? and US! are drawn in the same style, but no sharp reference of them exists yet (**unconfirmed glyphs**).
- **Bold narrow** (GHOSTBUSTERS, FOR HIRE…): 6-column letters with 1-column gaps. GHOSTBUSTERS spans columns 0–78.
- **Thin 5 × 7** (TO BELIEVE YOU, CALL JL5-2020): confirmed by premiere-footage close-ups of CALL, BELIEVE and O.[^getty]

![Bold wide font](IMG:font_bold_wide.png)

![Bold narrow font](IMG:font_bold_narrow.png)

![Thin 5x7 font](IMG:font_thin.png)

## Sequence and animation

The running order comes from the thread's analysis of the film (around 00:37:06, 00:38:10, 00:49:44 and 01:22:59–01:24:54), the deleted scenes, behind-the-scenes footage, and the 1989 premiere footage found by Kingpin.[^thread][^getty] The timing of the end of the loop (CALL? to CALL JL5-2020) was measured frame by frame from a deleted museum scene.[^deleted]

1. **GHOSTBUSTERS** slides up in red, turns green and shimmers, swaps between red and green about 16 times, then settles on green.
2. A solid green frame wipes to **FOR HIRE…**, followed by a green wipe.
3. **WE'RE READY**.
4. **TO BELIEVE YOU**, with the highlight moving word by word. It then wipes downward as **CALL JL5-2020** slides in from the top.
5. A red wipe into **GHOSTBUSTERS** in green, which shimmers, wipes from green to red, and is followed by a solid red frame.
6. A green flash, then **WE'RE BACK**, with the two words swapping colours.
7. The **five lines → green boxes** graphic, looping several times.
8. **WHO YA**, **GONNA**, then **CALL?**, which slides up and out. The board then goes dark for about 0.8 s.
9. **US!** appears alone for about 0.6 s. The arrows then come on for about 1.2 s, go off for 0.8 s, and come back.
10. **CALL JL5-2020** opens outward from the centre while the arrows are still lit, holds for about 2 s, then slides down as red GHOSTBUSTERS rises to restart the loop.

![Storyboard of the full loop](IMG:storyboard.png)

![Animated preview](IMG:preview_96x16.gif)

## Inferred effects

Three effects are confirmed to happen on the boards, but their exact appearance hasn't been documented. The recreation renders them as clearly labelled best guesses.

- **Colour wipes:** the colour of each wipe is reported in the thread (green into FOR HIRE…, green before WE'RE READY, red into the second GHOSTBUSTERS, green to red within it), but the direction is not. In the deleted museum scene, red sweeps in from the left on this board, so the recreation draws every wipe **left to right**.[^deleted]
- **Shimmer:** reported on green GHOSTBUSTERS, both before the red/green swaps and after the red wipe. The recreation renders it as random per-pixel sparkle.
- **Five lines → green boxes:** the thread describes five vertical lines that each wipe across and are replaced by a green box, looping several times.[^thread] The deleted museum scene confirms red fills with dark dividers, then green growing outward from inside each section with red dividers, then red sweeping back from the left.[^deleted] Only the right third of the board is visible, out of focus, so the recreation **assumes** five 16-column sections. The measured spacing of 14–15 columns is consistent with that.

![Wipes and shimmer (inferred)](IMG:wipes_shimmer_steps.png)

![Lines to boxes (inferred)](IMG:lines_boxes_steps.png)

The thread also mentions a possible bounce and an upside-down flip of GHOSTBUSTERS. These are hedged ("seems", "possibly") and are left out of the recreation.

## Plans

The plans below show every message as a numbered pixel map. Columns run 0–79 from the left and rows 0–6 from the top. Cells are coloured red, green or amber (both lit). The same maps are available as plain text in the downloads.

![Plan A: GHOSTBUSTERS](IMG:plans/plan_A.png)

![Plan B: FOR HIRE](IMG:plans/plan_B.png)

![Plan C: WE'RE READY](IMG:plans/plan_C.png)

![Plan D: TO BELIEVE YOU](IMG:plans/plan_D.png)

![Plan E: CALL JL5-2020](IMG:plans/plan_E.png)

![Plan F: GHOSTBUSTERS (second)](IMG:plans/plan_F.png)

![Plan G: WE'RE BACK](IMG:plans/plan_G.png)

![Plan G2: five lines to boxes (inferred)](IMG:plans/plan_G2.png)

![Plan H: WHO YA](IMG:plans/plan_H.png)

![Plan I: GONNA](IMG:plans/plan_I.png)

![Plan J: CALL?](IMG:plans/plan_J.png)

![Plan K: US!](IMG:plans/plan_K.png)

![Plan L: CALL JL5-2020 (second)](IMG:plans/plan_L.png)

### Timing

- The end of the loop is measured from the deleted museum scene: CALL? about 0.8 s, dark 0.8 s, US! with arrows 3.2 s, and CALL JL5-2020 about 2.4 s including its reveal.[^deleted]
- The 16 red/green swaps in GHOSTBUSTERS follow the thread's count.[^thread]
- All other holds are **estimates**. The screen-timed version uses 2-second holds, based on the measured CALL JL5-2020 hold, for a loop of about 44 seconds.

## Building your own

- **CoolLED1248 panels (16 × 96):** these inexpensive Bluetooth panels can load a ready-made animation file. A single file holds at most 113 frames, so there are two versions:
  - a **single file** with compressed timing (22.6 s);
  - a **two-part, screen-timed** version (44.2 s). Load both files and play Part 1 then Part 2.
  
  Each board row uses two panel rows, so the green can sit half a pixel lower than the red, as on the real boards.
- **Arduino, ESP32 and other microcontrollers:** use the C header, or the JSON frame data, which stores every pixel as 0 (off), 1 (red), 2 (green) or 3 (both). A microcontroller isn't limited to 113 frames, so the holds can be stretched to film timing.
- **RGB matrices (HUB75, WS2812):** map "both" to an amber such as RGB (255, 180, 0). Pure yellow looks greenish on most panels.
- **Scratch-built replica:** use separate red and green LED clusters in an 80 × 7 grid, drive the two colours independently, and mount the green slightly below the red.
- **Other panel sizes:** the messages are designed for 80 columns. On narrower panels, scroll or scale with nearest-neighbour; never smooth the image. The generator script can produce CoolLED files for other sizes.

## Downloads

All files below are on GitHub. A single zip of the build files will also be hosted on GBFans.com.

### CoolLED1248 files (16 × 96 panel)

- **Single file**, compressed timing, 113 frames, 22.6 s: [Ecto-1A_GB2_16x96.jt](https://github.com/rmbrumback-lab/ecto-1a-led-sign/raw/main/dist/Ecto-1A_GB2_16x96.jt)
- **Two-part, screen-timed**, 44.2 s. Load both and play Part 1 then Part 2:
  - [Ecto-1A_GB2_16x96_Part1.jt](https://github.com/rmbrumback-lab/ecto-1a-led-sign/raw/main/dist/two_part/Ecto-1A_GB2_16x96_Part1.jt) (A–F, 112 frames)
  - [Ecto-1A_GB2_16x96_Part2.jt](https://github.com/rmbrumback-lab/ecto-1a-led-sign/raw/main/dist/two_part/Ecto-1A_GB2_16x96_Part2.jt) (G–L, 109 frames)

On iOS or Android, download the file, tap it, and open it with CoolLED1248 (app version 2.x).

### Attribution evidence

- **[Ecto-1A_Attribution_Evidence_v10.pdf](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/evidence/Ecto-1A_Attribution_Evidence_v10.pdf)**: one card per element, showing a credited source extract beside the recreation and marking it sourced, measured, estimate or inferred.

The source extracts in the PDF (film stills, Getty Images news footage, a book scan) belong to their owners. They are included only for attribution and comparison, and aren't covered by the project's MIT licence.

### Image files

- **Frames:** [113 PNG frames](https://github.com/rmbrumback-lab/ecto-1a-led-sign/tree/main/dist/frames_80x7), 80 × 7, 1 pixel = 1 LED, 200 ms each; [sprite sheet](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/dist/ecto1a_spritesheet_80x7.png).
- **Animated previews:** [80 × 7 GIF](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/dist/ecto1a_80x7.gif), [16 × 96 panel GIF](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/dist/ecto1a_96x16_panel.gif), [screen-timed GIF](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/dist/two_part/ecto1a_96x16_full.gif).
- **Plans:** [A: GHOSTBUSTERS](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/plan_A.png), [B: FOR HIRE…](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/plan_B.png), [C: WE'RE READY](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/plan_C.png), [D: TO BELIEVE YOU](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/plan_D.png), [E: CALL JL5-2020](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/plan_E.png), [F: GHOSTBUSTERS (second)](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/plan_F.png), [G: WE'RE BACK](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/plan_G.png), [G2: five lines → boxes](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/plan_G2.png), [H: WHO YA](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/plan_H.png), [I: GONNA](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/plan_I.png), [J: CALL?](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/plan_J.png), [K: US!](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/plan_K.png), [L: CALL JL5-2020 (second)](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/plan_L.png); [plain-text pixel maps](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/ecto1a_pixel_maps.txt); [panel mapping](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/plans/panel_mapping.png).
- **Fonts:** [bold wide](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/images/font_bold_wide.png), [bold narrow](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/images/font_bold_narrow.png), [thin 5 × 7](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/images/font_thin.png).
- **Diagrams:** [storyboard](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/images/storyboard.png), [red/green offset close-up](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/images/offset_closeup.png), [wipes and shimmer](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/images/wipes_shimmer_steps.png), [lines → boxes](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/images/lines_boxes_steps.png).

### Code for other platforms

- **[Porting guide](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/PORTING.md):** which file to use for each app or board, building a pixel-exact GIF, an Arduino example, RGB matrices, true red/green hardware, and scaling to other panel sizes.
- **Arduino / ESP32 / Teensy:** [ecto1a_frames.h](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/dist/ecto1a_frames.h), the deduplicated frames and playlist as `PROGMEM` arrays (2 bits per pixel).
- **Raspberry Pi, web, Python, JavaScript:** [ecto1a_frames.json](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/dist/ecto1a_frames.json) (every frame), [ecto1a_playlist.json](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/dist/ecto1a_playlist.json) (deduplicated), and the screen-timed [ecto1a_full_frames.json](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/dist/two_part/ecto1a_full_frames.json) / [ecto1a_full_playlist.json](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/dist/two_part/ecto1a_full_playlist.json).
- **Generator:** [generate.py](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/src/ecto1a/generate.py) builds every frame and export, including CoolLED files for other panel sizes. The [file-format notes](https://github.com/rmbrumback-lab/ecto-1a-led-sign/blob/main/docs/JT_FORMAT.md) document the `.jt` format.
- **Full repository:** [github.com/rmbrumback-lab/ecto-1a-led-sign](https://github.com/rmbrumback-lab/ecto-1a-led-sign), with design notes, validation and the research log. The code and data are MIT-licensed.

### Discussion

- [Screen-accurate ECTO-1A sign animation](https://forum.gbfans.com/t/screen-accurate-ecto-1a-sign-animation-coolled-file-open-data-for-any-led-build/219532) in the forum.

## Open questions

These would replace estimates and inferences with facts. If you have reference, please post it in the reference thread.

- Clear frames of **GONNA** (colour and letters), and sharp frames of WHO YA and CALL?.
- The font and colour of **WE'RE READY**.
- YOU's highlight colour in TO BELIEVE YOU.
- What the **shimmer** really looks like, and the direction of the **wipes**.
- A sharp, full-width view of the **five lines → green boxes** graphic.
- A sharp frame of the US! arrows.
- Whether the FOR HIRE… border moves.
- Uninterrupted footage of the full loop, for true timing.

## Credits

This page builds on research shared in the GBFans forum:

- **prodestrian** worked out the 80 × 7 red/green matrix, the green offset, the complete message list, the A–L sequence, and a scene-by-scene breakdown of the film, deleted scenes and premiere footage.
- **zerosum** contributed pixel maps, premiere screen grabs, and the WE'RE BACK book scan.
- **Kingpin** found the 1989 premiere footage, and identified the "yellow" as red and green lit together.
- **d_osborn** pointed to the EPK and posted close-ups.
- **auc0le** (JT-Edit) and **UpDryTwist** (coolledx-driver) documented the CoolLED file format in their open-source projects.
- Recreation, plans and build files by **ryan-brumback**.

## References

[^thread]: prodestrian et al. "Screen Accurate ECTO-1A Dot Matrix LED Sign (Reference)". GBFans.com forum, Ectomobiles. https://forum.gbfans.com/t/screen-accurate-ecto-1a-dot-matrix-led-sign-reference/26454

[^kingpin]: Kingpin, in the reference thread (page 2): the "yellow" is red and green lit together.

[^book]: zerosum, in the reference thread (post #10): hi-res book scan of the WE'RE BACK sign.

[^getty]: 1989 *Ghostbusters II* premiere footage, Getty Images clip 1032076844, found by Kingpin and analysed in the reference thread.

[^deleted]: *Ghostbusters II* deleted scene (Hardemeyer at the museum), analysed frame by frame (181 frames, about 14.8 s). Colours were calibrated against the confirmed red US!, green arrows and amber CALL JL5-2020.
