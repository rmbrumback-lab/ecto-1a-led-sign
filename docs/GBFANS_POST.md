<!--
GBFans post draft (Discourse markdown). Suggested title:
  "Screen-accurate ECTO-1A sign animation — CoolLED file + open data for any LED build"
Suggested category: Equipment > Ectomobiles. Reply in the reference thread too, linking here.
REPO_URL and RAW_URL are filled in automatically when the repo is published.
-->

# Screen-accurate ECTO-1A sign animation — CoolLED file + open data for any LED build

Building on the incredible research in @prodestrian's [Screen Accurate ECTO-1A Dot Matrix LED Sign (Reference)](https://forum.gbfans.com/t/screen-accurate-ecto-1a-dot-matrix-led-sign-reference/26454) thread, I've turned the community's findings into a working animation of the full sign loop. Everything is open and free to use:

* **A ready-to-load file for CoolLED1248 LED panels** (the cheap Bluetooth panels sold on AliExpress and Amazon), 16×96 size.
* **Open frame data** (GIF, PNG frames, sprite sheet, JSON, and an Arduino/C header) so you can drive any LED sign, app, or scratch-built replica.
* **Full documentation** of how every pixel and colour was decided, including which parts are confirmed and which are educated guesses.

![preview](RAW_URL/docs/images/preview_96x16.gif)

**Download + docs:** REPO_URL
**Direct CoolLED file:** REPO_URL/raw/main/dist/Ecto-1A_GB2_16x96.jt

---

## Credit where it's due

None of this exists without the people in the reference thread:

* **@prodestrian** worked out the 80×7 red/green matrix, the green-sits-lower quirk, the complete text list, the A–L sequence, and a scene-by-scene breakdown of the film, deleted scenes and premiere footage. That breakdown is the backbone of the animation.
* **@zerosum** contributed the pixel maps, premiere screen grabs, and the **WE'RE BACK book scan**. I read most of the bold font from that scan.
* **@Kingpin** found the 1989 premiere footage (YouTube + Getty), the best reference we have for the sequence. He also nailed that the "yellow" is just red and green lit together.
* **@d_osborn** pointed to the EPK and posted the close-ups.

Thanks also to **auc0le** ([JT-Edit](https://github.com/auc0le/JT-Edit)) and **UpDryTwist** ([coolledx-driver](https://github.com/UpDryTwist/coolledx-driver)). Their open-source work is the only public documentation of the CoolLED file format.

---

## What the sign does (as recreated)

![storyboard](RAW_URL/docs/images/storyboard.png)

The IDs match prodestrian's A–L frames. It's one 22-second loop:

1. **GHOSTBUSTERS** slides up in red, bounces, then flashes red/green and settles green.
2. **FOR HIRE…** in red, with a **green dotted border chasing round the edge**.
3. **WE'RE READY**, then **TO BELIEVE YOU**, with the word colours cycling.
4. **CALL JL5-2020** in amber.
5. **GHOSTBUSTERS** in green with the **shimmer**, then wipes to red.
6. **WE'RE** (red) → green flash → **WE'RE BACK**, with the words swapping colours.
7. The **five sweeping lines** that turn into green boxes.
8. **WHO YA**, **GONNA**, **CALL?**, then **US!** with blinking arrows pointing in.
9. **CALL JL5-2020** slides down, and GHOSTBUSTERS rises to start again.

---

## How I worked it out

**1. The file format.** CoolLED's `.jt` files turn out to be JSON containing the frames as colour bit-planes. I worked out the layout from JT-Edit and the coolledx driver. I then proved it by re-encoding four files exported by the CoolLED app and getting byte-identical results. One catch: the panel's upload protocol caps a 16×96 animation at **113 frames**. That's why the timing is tighter than in the film.

**2. The sequence.** I took this straight from prodestrian's analysis: what transitions into what, every wipe and slide, the shimmer, the flashing, and the lines-to-boxes graphic.

**3. The photos.** I enlarged the stills posted in the thread and laid an 80×7 grid over each one, with perspective correction on the angled shots. That turned up things I'd missed in my first versions:

* **The sign uses three fonts**, not one:
  * **Bold wide** for WE'RE BACK. B, A, C and K came pixel-for-pixel from zerosum's scan, and the phrase adds up to exactly 80 columns.
  * **Bold narrow** for GHOSTBUSTERS, which runs edge to edge.
  * **Thin 5×7** for CALL JL5-2020, TO BELIEVE YOU and WE'RE READY.

![bold wide font](RAW_URL/docs/images/font_bold_wide.png)

* **FOR HIRE…** has the green border.
* **CALL JL5-2020** is amber. You can see both colours lit in the Getty close-up.
* **TO BELIEVE YOU** shows three different colour states across the film and premiere shots.
* The green shapes beside **US!** are arrows pointing *in* at the word. I first read them as crosses because of the motion blur.

**4. The green offset.** The panel version uses two panel rows per sign row. That let me draw the green half a pixel lower than the red, just like the real sign, where "BACK" doesn't line up with "WE'RE":

![offset](RAW_URL/docs/images/offset_closeup.png)

---

## Confirmed vs. guessed

I want to be upfront about this:

* **Confirmed from reference:** the matrix and offset, all the text, the order, and the fonts for GHOSTBUSTERS / WE'RE BACK / the thin frames. Also confirmed: the colours of GHOSTBUSTERS, FOR HIRE, TO BELIEVE YOU, CALL JL5-2020, WE'RE BACK and US!, and the types of effect.
* **Educated guesses:**
  * WE'RE READY being amber.
  * The font and colours for **WHO YA / GONNA / CALL?**.
  * The exact arrow shape.
  * The border chase pattern.
  * All the timing.

The full table is in the repo's README. **If anyone has clear shots of WHO YA, GONNA or CALL?**, post them and I'll update the file.

---

## Using it

* **CoolLED1248 (16×96):** download the `.jt` to your phone (Android), tap it, and open with CoolLED1248. The app versions that support `.jt` import are 2.x. iOS import isn't confirmed yet.
* **Any other sign or app:** the repo's `dist/` folder has:
  * `frames_80x7/` — 111 PNGs, 200 ms each
  * a sprite sheet
  * `ecto1a_frames.json` — every frame as 0/1/2/3 values (off/red/green/both, the same scheme prodestrian proposed)
  * `ecto1a_playlist.json` — deduplicated
  * `ecto1a_frames.h` — for Arduino/ESP32
* The `docs/PORTING.md` guide covers making a pixel-exact GIF, scaling to other panel sizes, and driving true red/green LEDs for a full-size replica.
* **Other CoolLED sizes:** the generator script is included. Change two numbers and re-run it.

Code and data are MIT-licensed. Use it, remix it, put it on your car. I haven't included any film frames or the reference photos in the repo; those stay here in the thread.

If you load it on a panel, I'd love to see a photo. 👻
