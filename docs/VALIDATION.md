# Validation

The CoolLED1248 format is undocumented by the vendor, so the output was checked against three independent references.

## 1. Encoder matches the app's own exports

JT-Edit's repository includes `.jt` files exported by the CoolLED1248 app. Each was decoded, then re-encoded with this project's `plane()` function, and compared byte-for-byte:

| App-exported sample | Bytes | Result |
|---|---|---|
| 16×64 animation, 63 frames | 24,192 | identical |
| 16×96 animation, 5 frames | 2,880 | identical |
| 16×64 static image | 384 | identical |
| 16×32 static image | 1,536 | identical |

This confirms the plane order, column-major layout, bytes per column and bit order.

## 2. JT-Edit decodes our file

[`tools/verify_with_jtedit.js`](../tools/verify_with_jtedit.js) loads JT-Edit's own import function (`convertToPixelArrayFrames`) from a local clone. It decodes the output and fails if any pixel isn't black, red, green or yellow.

```bash
git clone https://github.com/auc0le/JT-Edit.git
node tools/verify_with_jtedit.js ./JT-Edit dist/Ecto-1A_GB2_16x96.jt
# JT-Edit decoded 112 frames of 16x96; non-red/green/yellow pixels: 0
```

During development, its output was also compared pixel-by-pixel with the generator's panel frames: **0 mismatches**.

## 3. Test suite

`python -m pytest -q tests` runs these checks:

| Test | Checks |
|---|---|
| `test_protocol_limits` | ≤ 255 frames, ≤ 65,535 bytes, expected length |
| `test_jt_structure_matches_app_export` | keys, key order, `dataType`, `aniType`, byte range |
| `test_roundtrip` | the project's own decoder recovers every panel frame |
| `test_no_blue_channel` | only red/green used |
| `test_were_back_spans_full_sign` | WE'RE BACK covers cols 0–79, as in the book scan |
| `test_ghostbusters_spans_sign` | GHOSTBUSTERS covers cols 0–78, as in the night still |
| `test_green_sits_half_pixel_lower` | hardware offset on the panel |
| `test_playlist_reconstructs_sequence` | the deduplicated playlist expands back to the exact 112 frames |
| `test_dist_jt_is_current` | the committed `.jt` equals freshly generated output |

## Not yet verified

- **On-device playback** on a physical 16×96 panel. The limits above come from the protocol; panel firmware could be stricter.
- **iOS app import** of `.jt` files.
