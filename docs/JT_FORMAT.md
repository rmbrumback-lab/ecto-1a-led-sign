# CoolLED1248 `.jt` file format

`.jt` is the file format the CoolLED1248 mobile app uses to import and export images and animations for its LED panels. It is undocumented by the vendor. This description comes from the open-source [JT-Edit](https://github.com/auc0le/JT-Edit) editor (its encoder/decoder and sample files exported by the app) and the [coolledx-driver](https://github.com/UpDryTwist/coolledx-driver) Bluetooth driver. It was confirmed by reproducing the app's own exports byte-for-byte.

## Container

A JSON array with one object:

```json
[{"data": { ... }, "dataType": 0}]
```

| `dataType` | Meaning | Pixel key |
|---|---|---|
| `0` | animation | `aniData` |
| `1` | static image | `graffitiData` |

### Animation (`dataType: 0`), key order as exported by the Android app

| Key | Type | Meaning |
|---|---|---|
| `pixelWidth` | int | panel width, e.g. 96 |
| `aniData` | int[] | pixel bytes (below) |
| `frameNum` | int | number of frames |
| `delays` | int | milliseconds per frame (one value for all frames) |
| `aniType` | int | `1` = 3-bit color; `2` = 24-bit RGB (newer "CoolLEDU" panels) |
| `pixelHeight` | int | panel height, e.g. 16 |

Static images use `graffitiData`, `graffitiType` (1/2), `mode`, `speed`, `stayTime`, `pixelWidth` and `pixelHeight`.

## 3-bit pixel data (`aniType 1`)

Each pixel has 3 bits: red, green, blue. That gives 8 colors: black, red, green, yellow, blue, magenta, cyan, white.

`aniData` is three **bit-planes concatenated**, each covering *all* frames:

```
aniData = [ red plane: frame 0, frame 1, ... frame N-1 ]
        + [ green plane: frame 0 ... N-1 ]
        + [ blue plane:  frame 0 ... N-1 ]
```

Within one plane for one frame:

- **column-major**: column 0 first, then column 1, and so on;
- each column is `ceil(height / 8)` bytes, top 8 rows first;
- in each byte, **bit 7 (MSB) is the topmost row** of that group of 8.

```
bytes per plane per frame = width * ceil(height/8)
total length              = frames * width * ceil(height/8) * 3
```

For 16×96: 96 × 2 = 192 bytes per plane per frame, so 576 bytes per frame.

### Encoder (Python)

```python
def plane(pixels, bit, w, h):            # pixels[y][x] is a 3-bit value: 1=R 2=G 4=B
    out = []
    for x in range(w):
        for yb in range(0, h, 8):
            v = 0
            for k in range(8):
                if yb + k < h and pixels[yb + k][x] & bit:
                    v |= 0x80 >> k
            out.append(v)
    return out

aniData = sum((plane(f, 1, w, h) for f in frames), []) \
        + sum((plane(f, 2, w, h) for f in frames), []) \
        + sum((plane(f, 4, w, h) for f in frames), [])
```

## 24-bit data (`aniType 2`)

Each pixel is 3 bytes (R, G, B), row-major. **Exception:** JT-Edit notes that 24×48 and 24×64 panels split the image into a left half and a right half, each stored column-major. This project uses `aniType 1` only.

## Size limits

When the app uploads to the panel, it builds a payload with the **frame count in 1 byte** and the **data length in 2 bytes**. So:

- `frameNum ≤ 255`
- `len(aniData) ≤ 65,535`

| Panel | Bytes/frame (3-bit) | Max frames |
|---|---|---|
| 16×32 | 192 | 255 |
| 16×64 | 384 | 170 |
| 16×96 | 576 | 113 |
| 16×128 | 768 | 85 |

These limits are derived from the protocol fields. Panel firmware may impose a lower limit. Animations exported by the app itself have been seen at 63 frames (16×64).

## Importing

- Android CoolLED1248 2.x: tap the `.jt` file in a file manager and choose *Open with → CoolLED1248*. Version 2.1.4 is recommended if imports fail.
- Browser: [jt-edit.com](https://jt-edit.com/) opens, edits and exports `.jt`.
