Ecto-1A LED Sign Boards (Ghostbusters II) - build files, {version}
==============================================================
Wiki page: https://www.gbfans.com/wiki/ecto-1a-led-sign-boards
Source code and full documentation: https://github.com/rmbrumback-lab/ecto-1a-led-sign

coolled_16x96/   Ready-to-load CoolLED1248 files for a 16x96 panel.
                 Ecto-1A_GB2_16x96.jt = single file, 113 frames, 22.6 s (compressed timing)
                 two_part/ Part1 + Part2 = screen-timed, 44.2 s; load both, play Part 1 then Part 2
frames_80x7/     One PNG per frame (80x7, 1 pixel = 1 LED), 200 ms each
data/            ecto1a_frames.json (0 off, 1 red, 2 green, 3 both), deduplicated playlist,
                 sprite sheet, Arduino/ESP32 header (ecto1a_frames.h), screen-timed JSON
plans/           Numbered pixel map for every message + plain-text pixel maps + panel mapping
fonts/           The three sign fonts (bold wide, bold narrow, thin 5x7)
preview/         Animated previews

Status: elements are sourced from the GBFans reference thread and reference footage.
Three effects (lines -> boxes, colour wipes, shimmer) are INFERRED reconstructions,
and a few colours (WE'RE READY, GONNA, YOU's highlight) are unconfirmed. See the wiki page.

Credits: research by prodestrian, zerosum, Kingpin, d_osborn and others in the GBFans thread
"Screen Accurate ECTO-1A Dot Matrix LED Sign (Reference)". File format work by auc0le
(JT-Edit) and UpDryTwist (coolledx-driver). Recreation by ryan-brumback.
Code and data: MIT licence. Ghostbusters is a trademark of Columbia Pictures / Sony;
non-commercial fan project.
