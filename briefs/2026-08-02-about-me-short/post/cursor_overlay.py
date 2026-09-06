#!/usr/bin/env python3
"""
CURSOR OVERLAY — beat 14, THE REPLAY. A drawn cursor circling a still of the checkout page and
never finding the buy button. Post, not generation: the model has never had to hold a UI, a
sprite on a path is exact and loopable, and it costs nothing (wave-3 doc, beat 14's lean).

The page still is the S08 replay edit; the cursor is a hand-drawn-looking arrow sprite (graphite
fill, paper-white outline, a one-pixel wobble held on twos) moving through waypoints with a
small circling loop at three of them. The path stays out of the bottom-right corner, where the
tiny grey buy button sits — the joke is that it never goes there.

    $0.  Usage:  cursor_overlay.py <page-still.png> <out.mp4> [seconds=7] [fps=24]
    Waypoints are in the still's own pixel space (2688x1520); edit WAYPOINTS to re-block the path.
"""
import math, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw

# (x, y, dwell_frames, circle_radius) — circle_radius>0 means the cursor circles here for the dwell.
WAYPOINTS = [
    (1250, 470, 10, 0),   # start on the product picture
    (1420, 300, 14, 40),  # up to the banner, circle it
    (1610, 420, 12, 0),   # over to the title / price
    (1560, 530, 16, 45),  # the stack of boxes, circle
    (1300, 640, 10, 0),   # down-left to the related items
    (1240, 420, 12, 0),   # back to the picture
    (1380, 250, 14, 38),  # the menu bar, circle
    (1600, 480, 10, 0),   # price again
    (1330, 560, 12, 0),   # middle of the page, lost
    (1250, 470, 8, 0),    # and back to the picture, where it started
]
FRAME_W, FRAME_H = 1280, 720

def ease(t):  # ease-in-out between waypoints; a cursor darts and settles
    return 0.5 - 0.5 * math.cos(math.pi * t)

def path(total_frames):
    """Yield (x, y) per frame: travel between waypoints, dwell (optionally circling) at each."""
    pts = []
    n = len(WAYPOINTS)
    travel = 14  # frames per hop
    for i in range(n):
        x0, y0, dwell, rad = WAYPOINTS[i]
        for k in range(dwell):
            if rad:
                a = 2 * math.pi * k / dwell
                pts.append((x0 + rad * math.cos(a), y0 + rad * math.sin(a)))
            else:
                pts.append((x0, y0))
        x1, y1, _, _ = WAYPOINTS[(i + 1) % n]
        for k in range(travel):
            t = ease(k / travel)
            pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    while len(pts) < total_frames:
        pts += pts
    return pts[:total_frames]

def draw_cursor(d, x, y, s=1.0, wob=0):
    # classic arrow pointer, slightly hand-drawn: outline in paper-white, fill graphite
    p = [(0, 0), (0, 46), (12, 35), (21, 54), (30, 50), (21, 31), (35, 30)]
    poly = [(x + px * s + (wob if i % 2 else -wob), y + py * s + (wob if i % 3 else 0)) for i, (px, py) in enumerate(p)]
    d.polygon(poly, fill=(52, 52, 52), outline=(246, 240, 226))
    d.line(poly + [poly[0]], fill=(246, 240, 226), width=3)
    d.polygon(poly, fill=(52, 52, 52))

def main():
    still = Image.open(sys.argv[1]).convert("RGB")
    out = sys.argv[2]
    seconds = float(sys.argv[3]) if len(sys.argv) > 3 else 7.0
    fps = int(sys.argv[4]) if len(sys.argv) > 4 else 24
    total = int(seconds * fps)
    sx, sy = FRAME_W / still.size[0], FRAME_H / still.size[1]
    base = still.resize((FRAME_W, FRAME_H), Image.LANCZOS)
    pts = path(total)
    tmp = tempfile.mkdtemp()
    for f in range(total):
        x, y = pts[f - (f % 2)]  # held on twos
        fr = base.copy(); d = ImageDraw.Draw(fr)
        wob = 1 if (f // 2) % 2 else 0
        draw_cursor(d, x * sx, y * sy, s=0.9, wob=wob)
        fr.save(os.path.join(tmp, f"f{f:04d}.png"))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(fps), "-i", os.path.join(tmp, "f%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out], check=True)
    print(f"{out}  {total} frames @ {fps}fps ({seconds}s), {len(WAYPOINTS)} waypoints, cursor never enters the bottom-right corner")

if __name__ == "__main__":
    main()
