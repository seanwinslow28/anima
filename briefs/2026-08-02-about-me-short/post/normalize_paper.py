#!/usr/bin/env python3
"""
PAPER NORMALISATION — the film's one standing post step, run on every frame.

Ruled by Sean 2026-08-31: "Normalize each in post. It makes the characters stand
out more. They all seem to blend or just not look right with the tan."

WHY THIS EXISTS. The corner plates were generated with the S04 rack plate as their
world/style bible, and S04 predates the palette clause — its own paper sits at
(218, 191, 152), some 27/41/57 levels warm of canonical. The clause and the
reference pulled opposite ways and the reference won about two thirds of the
argument, so every plate landed on a consistent tan instead of the canonical cream.
Consistent, but wrong, and the cost is exactly what Sean names: the mascots are warm
mid-tones and a warm mid-tone ground swallows them.

Fighting it at generation time costs a re-roll per plate and buys nothing. Fixing it
here costs nothing and is reversible — which is also what FIRST LICKS DR #41 already
says: the look lives in post, and every plate generates CLEAN.

HOW THE WALL IS FOUND. Not by hand-tuned sample coordinates — those broke on the
first pass (a patch near the top edge of the S07 alarm plate ran off the image and
returned NaN, and a patch that lands on a prop measures the prop). Instead the script
sweeps small patches across the upper band, scores each by local variance, and takes
the flattest ones. Flat and pale in the top of a frame is the wall, in every one of
these setups. The chosen patch is reported so the choice can be argued with.

Correction is a per-channel gain, not an offset: paper is a multiplicative tint, and
a gain leaves the graphite blacks black instead of lifting them into grey.

    $0, deterministic, idempotent. Re-run it after any new generation.
    Usage:  python3 post/normalize_paper.py            (all registered frames)
            python3 post/normalize_paper.py <path>...  (ad hoc)
"""
import os
import sys

from PIL import Image
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BRIEF = os.path.dirname(HERE)
OUT = os.path.join(BRIEF, "normalised")

# The canonical cream, measured from the approved S02 desk medium. environment-style.md
# is the authority on this value; if it changes there, change it here.
TARGET = np.array([245.0, 232.0, 209.0])
TOL = 8

# Where the automatic wall-finder needs steering. The S04 rack plate is the only one:
# its upper band is server rack on the left and moodboard on the right, so the sweep
# scored a mid-tone fixture as "flattest pale" and blew the highlights. The one clean
# strip of wall is above the coffee counter.
WINDOWS = {
    "U-codex-corner.png": dict(band=(0.03, 0.22), xband=(0.28, 0.46), patch=0.020),
}

# Every frame in the film's working set. Order is shot order.
FRAMES = [
    # --- the working set: room-bible rev 2 plates + their composites (2026-08-31) ---
    "titlecards/cardD-sean-thinking.png",
    "plates/rev2/S02-plate-v1.png",
    "composites/rev2/S02-sean-composite-v1.png",
    "plates/rev2/S03-plate-v1.png",
    "composites/rev2/S03-claude-composite-v1.png",
    "plates/rev2/S04-plate-v1.png",
    "composites/rev2/S04-codex-composite-v1.png",
    "composites/rev2/S04-codex-composite-v2.png",
    "plates/rev2/S05-plate-v1.png",
    "composites/rev2/S05-gemini-composite-v1.png",
    "composites/rev2/S05-gemini-composite-v2.png",
    "plates/rev2/S06-plate-v1.png",
    "composites/rev2/S06-grok-composite-v1.png",
    "composites/rev2/S06-grok-composite-v2.png",
    "plates/rev2/S07-plate-v2.png",
    # --- Sean ruled the mascots face us 3/4 FRONT so Seedance is never asked to
    #     invent an unseen half. These supersede the composites above. ---
    "composites/frontal/S03-claude-composite-frontal-v1.png",
    "composites/frontal/S04-codex-composite-frontal-v1.png",
    "composites/frontal/S05-gemini-composite-frontal-v1.png",
    "composites/frontal/S06-grok-composite-frontal-v1.png",
    # --- superseded, kept so their normalised copies stay reproducible ---
    "plates/S02-sean-desk-v2-dressed.png",
    "plates/S03-claude-nook-v2.png",
    "composites/S03-claude-nook-composite-v2.png",
    "probe-205/U-codex-corner.png",
    "plates/S05-gemini-moodboard-v2-crt.png",
    "composites/S05-gemini-moodboard-composite-v4-crt.png",
    "plates/S06-grok-dartboard-v1.png",
    "composites/S06-grok-dartboard-composite-v2.png",
    "plates/S07-alarm-v1.png",
    "composites/S07-alarm-screenoff-v1.png",
]



def find_wall(a, band=(0.02, 0.34), patch=0.035, keep=6, xband=(0.0, 1.0)):
    """Return the median colour of the flattest pale patches in the upper band.

    Flat + pale + high in frame is the wall in every setup in this film. Scoring by
    variance is what keeps the sample off the props; taking several patches and
    pooling them is what keeps one unlucky patch from setting the whole gain."""
    h, w = a.shape[:2]
    r = max(int(patch * min(w, h)), 8)
    ys = range(int(band[0] * h) + r, max(int(band[1] * h) - r, int(band[0] * h) + r + 1), r)
    x_lo, x_hi = int(xband[0] * w) + r, max(int(xband[1] * w) - r, int(xband[0] * w) + r + 1)
    xs = range(x_lo, x_hi, r)
    cands = []
    for y in ys:
        for x in xs:
            p = a[y - r:y + r, x - r:x + r].reshape(-1, 3)
            if p.size == 0:
                continue
            med = np.median(p, axis=0)
            if med.mean() < 150:            # a dark patch is a prop, not paper
                continue
            cands.append((float(p.std()), med, (x, y)))
    if not cands:                            # nothing pale: fall back to the whole band
        p = a[int(band[0] * h):int(band[1] * h),
              int(xband[0] * w):int(xband[1] * w)].reshape(-1, 3)
        return np.median(p, axis=0), None
    cands.sort(key=lambda c: c[0])
    top = cands[:keep]
    return np.median(np.stack([c[1] for c in top]), axis=0), top[0][2]


def normalise(path):
    src = path if os.path.isabs(path) else os.path.join(BRIEF, path)
    a = np.asarray(Image.open(src).convert("RGB")).astype(float)
    win = WINDOWS.get(os.path.basename(src), {})
    wall, at = find_wall(a, **win)
    gain = TARGET / np.maximum(wall, 1.0)
    out = np.clip(a * gain, 0, 255).astype(np.uint8)

    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, os.path.basename(src))
    Image.fromarray(out).save(dst)

    after, _ = find_wall(np.asarray(Image.open(dst).convert("RGB")).astype(float), **win)
    delta = after - TARGET
    ok = "pass" if np.all(np.abs(delta) <= TOL) else "CHECK"
    return dict(name=os.path.basename(src), before=wall, gain=gain, after=after,
                delta=delta, at=at, ok=ok)


def main(argv):
    frames = argv[1:] or FRAMES
    print(f"{'frame':46} {'wall before':>17} {'gain':>20} {'wall after':>17}   ")
    for f in frames:
        p = f if os.path.isabs(f) else os.path.join(BRIEF, f)
        if not os.path.exists(p):
            print(f"{os.path.basename(f):46} {'MISSING':>17}")
            continue
        r = normalise(f)
        b = ", ".join(f"{v:3.0f}" for v in r["before"])
        g = " ".join(f"{v:5.3f}" for v in r["gain"])
        a = ", ".join(f"{v:3.0f}" for v in r["after"])
        print(f"{r['name']:46} {b:>17} {g:>20} {a:>17}   {r['ok']}")
    print(f"\n→ {OUT}   target {tuple(int(v) for v in TARGET)}  tolerance ±{TOL}")


if __name__ == "__main__":
    main(sys.argv)
