#!/usr/bin/env python3
"""
LAYOUT HOLD — did the model keep the plate's composition, or re-camera it?

The check the project has been running by hand since 2026-08-31 and never committed.
Reduce the start image and a clip's frame 0 and last frame to 160x90 greyscale and
correlate. 1.00 is an identical layout.

Why frame 0 AND the last frame: the A/B on Codex proved a reference can lose the plate
at frame ZERO (0.273 — the camera had already pushed in before a single frame of motion),
while ordinary drift shows up only at the end. One number cannot see both failures.

    Claude tidy (rejected, slow motion) : f0 0.985  last 0.987   <- best ever measured, bad clip
    Codex arm A  (banked M2 asset)      : f0 0.988
    Codex arm B  (character refs)       : f0 0.273  <- the plate was gone at frame zero

READ THIS BEFORE TRUSTING THE NUMBER: the rejected Claude clip holds the record. Layout hold
catches a re-camera and nothing else. It cannot see slow motion, moon gravity, a lost face, or
a bad performance. Sean's eye is the verdict; this is a tripwire.

    $0.  Usage:  layout_hold.py <start-image.png> <clip.mp4> [<clip.mp4> ...]
"""
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

SIZE = (160, 90)


def thumb_from_array(a):
    im = Image.fromarray(a.astype(np.uint8)).convert("L").resize(SIZE, Image.BILINEAR)
    v = np.asarray(im).astype(float).ravel()
    return (v - v.mean()) / max(v.std(), 1e-6)


def corr(a, b):
    return float(np.dot(a, b) / len(a))


def endpoints(path):
    d = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", "fps=8",
                    os.path.join(d, "f%04d.png")], check=True)
    fs = sorted(os.listdir(d))
    first = np.asarray(Image.open(os.path.join(d, fs[0])).convert("L"))
    last = np.asarray(Image.open(os.path.join(d, fs[-1])).convert("L"))
    return first, last, len(fs)


if __name__ == "__main__":
    ref = thumb_from_array(np.asarray(Image.open(sys.argv[1]).convert("L")))
    print(f"{'clip':34s} {'layout f0':>10s} {'layout last':>12s}")
    for p in sys.argv[2:]:
        f0, fl, n = endpoints(p)
        print(f"{os.path.basename(p):34s} {corr(ref, thumb_from_array(f0)):10.3f} "
              f"{corr(ref, thumb_from_array(fl)):12.3f}")
    print("\n1.00 = identical layout. >=0.95 at BOTH ends is the Movement 1 bar, because "
          "Movement 2\ncuts back to these same corners. A low f0 means a re-camera, not drift.")
