import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ecto1a import generate as g

FRAMES = g.build()
JT, PANELS = g.encode_jt(FRAMES)


def test_protocol_limits():
    d = JT[0]["data"]
    assert d["frameNum"] == len(FRAMES) <= 255           # frame count is 1 byte on the wire
    assert len(d["aniData"]) <= 65535                     # payload length is 2 bytes on the wire
    assert len(d["aniData"]) == len(FRAMES) * 96 * 2 * 3  # 2 bytes/column x 3 colour planes


def test_jt_structure_matches_app_export():
    assert JT[0]["dataType"] == 0
    assert list(JT[0]["data"].keys()) == ["pixelWidth", "aniData", "frameNum", "delays",
                                          "aniType", "pixelHeight"]
    assert JT[0]["data"]["aniType"] == 1 and all(0 <= b <= 255 for b in JT[0]["data"]["aniData"])


def test_roundtrip():
    assert g.decode_jt(JT) == PANELS


def test_no_blue_channel():
    assert all(v & 4 == 0 for p in PANELS for row in p for v in row)


def test_were_back_spans_full_sign():
    f = g.wide("WE'RE BACK", g.per_word("WE'RE BACK", [g.R, g.G]))
    lit = [x for x in range(g.W) if any(f[y][x] for y in range(g.H))]
    assert lit[0] == 0 and lit[-1] == 79


def test_ghostbusters_spans_sign():
    f = g.narrow("GHOSTBUSTERS", g.R)
    lit = [x for x in range(g.W) if any(f[y][x] for y in range(g.H))]
    assert lit[0] == 0 and lit[-1] >= 78


def test_green_sits_half_pixel_lower():
    f = g.blank()
    f[0][0] = g.R
    f[0][1] = g.G
    p = g.to_panel(f)
    red_rows = [y for y in range(16) if p[y][8] & g.R]
    green_rows = [y for y in range(16) if p[y][9] & g.G]
    assert green_rows == [r + 1 for r in red_rows]


def test_playlist_reconstructs_sequence():
    uniq, plist = g.playlist(FRAMES)
    expanded = [uniq[i] for i, ms in plist for _ in range(ms // g.DELAY_MS)]
    assert expanded == FRAMES


def test_dist_jt_is_current():
    path = os.path.join(os.path.dirname(__file__), "..", "dist", "Ecto-1A_GB2_16x96.jt")
    with open(path) as fh:
        assert json.load(fh) == JT
