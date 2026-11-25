import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ecto1a import generate as g

FRAMES = g.build()
JT, PANELS = g.encode_jt(FRAMES)


def test_protocol_limits():
    d = JT[0]["data"]
    assert d["frameNum"] == len(FRAMES) <= 255           # frame count is 1 byte on the wire
    assert len(d["aniData"]) <= 65535                     # payload length is 2 bytes on the wire
    assert len(d["aniData"]) == len(FRAMES) * 96 * 2 * 3  # 2 bytes/column x 3 color planes


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


def test_two_parts_within_limits():
    p1, p2 = g.build_parts()
    for part in (p1, p2):
        jt, _ = g.encode_jt(part)
        assert jt[0]["data"]["frameNum"] <= 113
        assert len(jt[0]["data"]["aniData"]) <= 65535


def test_two_parts_cover_full_sequence_in_order():
    p1, p2 = g.build_parts()
    full = [f for _, _, fr in g.build_segments("full") for f in fr]
    assert p1 + p2 == full


def test_dist_parts_are_current():
    p1, p2 = g.build_parts()
    base = os.path.join(os.path.dirname(__file__), "..", "dist", "two_part")
    for name, part in (("Part1", p1), ("Part2", p2)):
        with open(os.path.join(base, f"Ecto-1A_GB2_16x96_{name}.jt")) as fh:
            assert json.load(fh) == g.encode_jt(part)[0]


def test_to_believe_you_highlights_one_word_at_a_time():
    # TO, then BELIEVE, then YOU; the other words stay red (P3, P16)
    spans = {"TO": range(0, 15), "BELIEVE": range(15, 58), "YOU": range(58, 80)}
    for prof in g.PROFILES:
        d = [fr for sid, _, fr in g.build_segments(prof) if sid == "D"][0][:-2]   # skip push frames
        order = []
        for f in d:
            lit = [w for w, xs in spans.items()
                   if {f[y][x] for y in range(g.H) for x in xs if f[y][x]} - {g.R}]
            assert len(lit) <= 1
            if lit and (not order or order[-1] != lit[0]):
                order.append(lit[0])
        assert order[:3] == ["TO", "BELIEVE", "YOU"]



def test_prodestrian_maps_used_verbatim():
    # WE'RE READY, TO BELIEVE YOU and US! frames are prodestrian's pixel maps (GBFans, 8 Nov 2026)
    segs = {sid: fr for sid, _, fr in g.build_segments("full")}
    for sid, key in (("C", "C_red"), ("D", "D_red"), ("K", "K_on")):
        assert g.bitmap(g.PRODESTRIAN_MAPS[key]) in segs[sid]


def test_we_re_ready_is_red_with_green_words():
    segs = {sid: fr for sid, _, fr in g.build_segments("full")}
    colors = {v for f in segs["C"] for row in f for v in row if v} 
    assert g.Y not in {v for f in segs["C"][-8:] for row in f for v in row}
    assert {g.R, g.G} <= colors


def test_lines_boxes_have_no_gaps():
    # Each box fills all 16 columns; no dark divider columns once the boxes are drawn (post #41)
    for prof in g.PROFILES:
        g2 = [fr for sid, _, fr in g.build_segments(prof) if sid == "G2"][0]
        full_lit = [all(v != g.OFF for row in f for v in row) for f in g2]
        first = full_lit.index(True)                    # first pass grows over a dark sign
        assert all(full_lit[first:])


def test_who_ya_has_a_word_space():
    f = g.wide("WHO YA", g.R, space=6)
    lit = [any(f[y][x] for y in range(g.H)) for x in range(g.W)]
    runs, n = [], 0
    for v in lit:
        if not v:
            n += 1
        else:
            if n:
                runs.append(n)
            n = 0
    assert max(runs[1:]) >= 6          # the gap between WHO and YA


def test_drop_shadow_and_flip_present():
    segs = {sid: fr for sid, _, fr in g.build_segments("single")}
    for sid in ("H", "I", "J"):
        vals = {v for row in segs[sid][0] for v in row}
        assert {g.R, g.G} <= vals                       # red letters, green shadow
    a_r = g.narrow("GHOSTBUSTERS", g.R)
    assert g.flip(a_r) in segs["A"]
