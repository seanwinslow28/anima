#!/usr/bin/env python3
"""
CLIP ANALYSIS — motion energy, background drift, and where the character is.

Three numbers per clip, all measured the same way so two clips can be compared:

  MOTION ENERGY  mean absolute luma difference between consecutive frames, x100.
                 How much is actually moving. The project's ADOPTED 7s Codex clip
                 measured 4.44 by the previous session's method; this is a fresh
                 implementation, so compare clips to each other, not to that figure.

  BG DRIFT       mean absolute luma difference between each frame and frame 0,
                 measured ONLY outside the character box, as a percentage of the
                 frame-0 signal. This is the plate coming apart under the model.

  CHAR TRAVEL    centroid movement of the "new ink" mask inside the character box,
                 in pixels. Distinguishes a character that acts from one that
                 vibrates in place.

    $0.  Usage:  analyze_clip.py <box=x0,y0,x1,y1> <clip.mp4> [<clip.mp4> ...]
"""
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image


def frames(path, fps=8):
    d = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps}",
                    os.path.join(d, "f%04d.png")], check=True)
    fs = sorted(os.listdir(d))
    return [np.asarray(Image.open(os.path.join(d, f)).convert("L")).astype(float) for f in fs]


def analyse(path, box):
    fr = frames(path)
    H, W = fr[0].shape
    x0, y0, x1, y1 = [int(v) for v in box]
    outside = np.ones((H, W), bool)
    outside[y0:y1, x0:x1] = False

    energy = np.mean([np.abs(fr[i] - fr[i - 1]).mean() for i in range(1, len(fr))])
    base = fr[0]
    drift = np.mean([np.abs(f[outside] - base[outside]).mean() for f in fr[1:]])
    drift_pct = 100.0 * drift / max(base[outside].std(), 1e-6)

    cents = []
    for f in fr:
        sub, b = f[y0:y1, x0:x1], base[y0:y1, x0:x1]
        m = np.abs(sub - b) > 18
        if m.sum() > 40:
            ys, xs = np.nonzero(m)
            cents.append((xs.mean(), ys.mean()))
    travel = 0.0
    if len(cents) > 1:
        travel = float(np.mean([np.hypot(cents[i][0] - cents[i - 1][0],
                                         cents[i][1] - cents[i - 1][1])
                                for i in range(1, len(cents))]))
    return dict(n=len(fr), energy=energy, drift=drift_pct, travel=travel, size=(W, H))


if __name__ == "__main__":
    box = [float(v) for v in sys.argv[1].split(",")]
    print(f"{'clip':28s} {'frames':>7s} {'motion':>8s} {'bg drift':>9s} {'travel':>8s}")
    for p in sys.argv[2:]:
        r = analyse(p, box)
        print(f"{os.path.basename(p):28s} {r['n']:7d} {r['energy']:8.2f} "
              f"{r['drift']:8.1f}% {r['travel']:8.1f}px")
    print("\nmotion = mean |frame - prev|; bg drift = mean |frame - frame0| outside the "
          "character box,\nnormalised by the plate's own contrast; travel = centroid "
          "movement of new ink inside the box.")
