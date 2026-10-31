# Porting guide — using the sign in other LED apps and builds

Every export uses the same pixel values:

| Value | Meaning | Suggested RGB |
|---|---|---|
| 0 | off | `#000000` |
| 1 | red | `#FF0000` |
| 2 | green | `#00FF00` |
| 3 | red + green | `#FFFF00` (amber/yellow) |

The base timing is **200 ms per frame**. The full loop is 109 frames, or 21.8 s.

## Which file to use

| Your target | Use |
|---|---|
| App that imports animated GIFs | `ecto1a_80x7.gif`, or build a pixel-exact GIF (below) |
| App that imports a folder of frames | `frames_80x7/frame_000.png` … `frame_108.png` |
| App that imports a sprite sheet | `ecto1a_spritesheet_80x7.png`, 80 × 7 per frame, stacked vertically |
| Arduino / ESP32 / Teensy | `ecto1a_frames.h` |
| Raspberry Pi, web, Python, JS | `ecto1a_frames.json` or `ecto1a_playlist.json` |
| CoolLED1248, 16×96 | `Ecto-1A_GB2_16x96.jt` |
| CoolLED1248, other size | regenerate (see the README) |

`ecto1a_80x7.gif` and `ecto1a_96x16_panel.gif` are **LED-style previews** (round dots, 8× scale). Apps that rescale a GIF onto their own grid want a **pixel-exact** GIF instead, where 1 image pixel equals 1 LED:

```python
from PIL import Image
import json
d = json.load(open("ecto1a_frames.json"))
pal = {0: (0, 0, 0), 1: (255, 0, 0), 2: (0, 255, 0), 3: (255, 255, 0)}
imgs = []
for f in d["frames"]:
    im = Image.new("RGB", (80, 7))
    im.putdata([pal[v] for row in f for v in row])
    imgs.append(im)
imgs[0].save("ecto1a_exact.gif", save_all=True, append_images=imgs[1:],
             duration=d["frame_ms"], loop=0)
```

## JSON

`ecto1a_frames.json`:

```json
{
  "width": 80, "height": 7, "frame_ms": 200, "frames_total": 109, "loop_ms": 21800,
  "timeline": [{"id": "A", "label": "...", "first_frame": 0, "frames": 24, "duration_ms": 4800}, ...],
  "frames": [ [[0,1,1,...80 values], ...7 rows], ...109 frames ]
}
```

`ecto1a_playlist.json` contains the same metadata. It stores `unique_frames` (26) and a `playlist` of `{"frame": index, "ms": duration}` (54 steps). Use it when memory matters or when you want to stretch holds to film-like timing: multiply `ms` on steps longer than 400 ms.

## Arduino / C (`ecto1a_frames.h`)

- `ecto1a_frames[ECTO1A_UNIQUE_FRAMES][140]` (26 frames): 2 bits per pixel, 4 pixels per byte, MSB first, row-major. Each row is 20 bytes.
- `ecto1a_playlist[ECTO1A_STEPS][2]` (54 steps): `{unique frame index, duration ms}`.
- Marked `PROGMEM`. On AVR, read with `pgm_read_byte` / `pgm_read_word`.

```cpp
#include "ecto1a_frames.h"

uint8_t ectoPixel(uint8_t frame, uint8_t x, uint8_t y) {
  uint8_t b = pgm_read_byte(&ecto1a_frames[frame][y * 20 + (x >> 2)]);
  return (b >> (6 - 2 * (x & 3))) & 0x03;          // 0 off, 1 red, 2 green, 3 both
}

void loop() {
  for (uint16_t s = 0; s < ECTO1A_STEPS; s++) {
    uint8_t  f  = pgm_read_word(&ecto1a_playlist[s][0]);
    uint16_t ms = pgm_read_word(&ecto1a_playlist[s][1]);
    for (uint8_t y = 0; y < ECTO1A_H; y++)
      for (uint8_t x = 0; x < ECTO1A_W; x++) {
        uint8_t v = ectoPixel(f, x, y);
        setLed(x, y, v & 1, v & 2);                // your driver: red on/off, green on/off
      }
    showLeds();
    delay(ms);
  }
}
```

**True red/green hardware**, such as a scratch-built replica with separate red and green LEDs: drive `v & 1` and `v & 2` independently. To reproduce the film's look, mount the green LEDs slightly below the red ones.

**RGB matrices** (HUB75, WS2812): map 3 to amber, such as `(255, 180, 0)`. Pure yellow looks greenish on many panels.

## Other panel sizes

- **At least 80 wide, at least 7 tall:** place 1:1 and centre. For 14+ rows, double each row as the CoolLED version does. For 15+ rows, optionally use the half-row green offset (`to_panel()` in `generate.py`).
- **Narrower than 80:** the sign's messages are designed for 80 columns; WE'RE BACK and GHOSTBUSTERS fill it edge to edge. Options:
  1. **Scroll** each frame horizontally, which works best for the long messages.
  2. **Scale down** horizontally with nearest-neighbour. Expect bold strokes to break below about 64 columns.
  3. **Two lines** on tall panels (e.g. 32×64): split long words. This is not screen-accurate.
- **Integer scaling up:** use nearest-neighbour only. Never smooth or interpolate; LED art turns to mush.

## Regenerating the `.jt` for another CoolLED size

Edit `PANEL_W` / `PANEL_H` in `src/ecto1a/generate.py`, then run the generator. Check the frame budget:

```
frames × width × ceil(height/8) × 3 ≤ 65,535
```

If you're over, shorten holds in `build_segments()`, or reduce the red/green swap count in segment A.
