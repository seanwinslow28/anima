#!/usr/bin/env python3
"""
BEAT TIMES — when did the screen light, and when did the camera start moving?

Sean's notes on S07 are about SECONDS, and reading seconds off a contact sheet is guesswork
at the sheet's own frame rate. This measures two things per clip at 24fps:

  SCREEN ON   first time the brightest patch inside the given screen box crosses the midpoint
              between its darkest and brightest values over the clip. Also reports every later
              crossing, which is how a BLINK shows up: on/off/on is three crossings, a held
              screen is one.
  ZOOM START  first frame where the layout correlation against frame 0 drops below 0.97,
              measured with the SCREEN BOX MASKED OUT. That mask is not optional: the screen
              lighting up is itself a big local change, and unmasked it trips the detector at
              the exact moment of the flash, reporting every clip's zoom as simultaneous with
              its flash. Masked, the number is the camera and only the camera.

    $0.  Usage:  beat_times.py <screenbox=x0,y0,x1,y1> <clip.mp4> [<clip.mp4> ...]
"""
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

FPS = 24


def load(path):
    d = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={FPS}",
                    os.path.join(d, "f%04d.png")], check=True)
    return [np.asarray(Image.open(os.path.join(d, f)).convert("L")).astype(float)
            for f in sorted(os.listdir(d))]


def thumb(a, mask=None, fill=None):
    a = a.copy()
    if mask is not None:
        a[mask[1]:mask[3], mask[0]:mask[2]] = fill
    v = np.asarray(Image.fromarray(a.astype(np.uint8)).resize((160, 90),
                                                              Image.BILINEAR)).astype(float).ravel()
    return (v - v.mean()) / max(v.std(), 1e-6)


if __name__ == "__main__":
    x0, y0, x1, y1 = [int(v) for v in sys.argv[1].split(",")]
    for p in sys.argv[2:]:
        fr = load(p)
        lum = np.array([np.percentile(f[y0:y1, x0:x1], 90) for f in fr])
        mid = (lum.min() + lum.max()) / 2
        on = lum > mid
        crossings = [i for i in range(1, len(on)) if on[i] != on[i - 1]]
        box = (x0, y0, x1, y1)
        fill = float(fr[0][y0:y1, x0:x1].mean())
        base = thumb(fr[0], box, fill)
        corr = np.array([float(np.dot(base, thumb(f, box, fill)) / len(base)) for f in fr])
        # 0.97 is tripped by the room JOLT (a hopping mug, fluttering paper), so it marks
        # "something in the room moved", not the camera. A push-in is a whole-frame scale
        # change and drives the correlation far lower than any prop can, so 0.85 is the
        # threshold that isolates it. Report both: the gap between them IS the jolt.
        dist = np.nonzero(corr < 0.97)[0]
        below = np.nonzero(corr < 0.85)[0]
        first = dist[0] / FPS if len(dist) else None
        zoom = below[0] / FPS if len(below) else None
        print(f"\n{os.path.basename(p)}")
        print(f"  screen first ON   {crossings[0]/FPS:5.2f}s" if crossings else "  screen never lit")
        print(f"  on/off crossings  {len(crossings)}  at "
              f"{', '.join(f'{c/FPS:.2f}s' for c in crossings[:10])}")
        print(f"  room first moves  {first:5.2f}s" if first is not None
              else "  room never moves")
        print(f"  camera committed  {zoom:5.2f}s" if zoom is not None
              else "  camera never left the plate")
