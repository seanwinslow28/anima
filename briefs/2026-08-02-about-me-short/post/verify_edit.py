#!/usr/bin/env python3
"""
EDIT VERIFICATION — did this composite preserve the plate it was drawn onto?

environment-style.md names the method as a standing law but shipped no tool, so it
was run by hand each time and the numbers could not be reproduced. This is the tool.

Frame-delta means are NOT used: FIRST LICKS retired them because they scale with
plate texture, so a busy plate scores "changed" for free. Two measures instead:

  PHASE CORR  FFT cross-power phase correlation between plate and edit. Insensitive
              to brightness and to the added character; collapses if the model
              re-cameraed, re-cropped or re-drew the set. This is the headline
              number. GPT's edit path benchmarks at 0.42; this project lands 0.47-0.58.

  EDGE KEEP   fraction of the plate's edge pixels still present in the edit, measured
              outside the region the character occupies. Answers a different question
              from phase corr — "are the same lines still there", not "is the frame
              still aligned" — so a pass needs both.

  SHIFT       the peak's offset in pixels. Anything but (0,0) means the frame moved.

  INK ADDED   share of new dark pixels, i.e. roughly how much of the frame the new
              character covers. Sanity check on scale, not a pass/fail.

    $0, deterministic.  Usage:  verify_edit.py <plate.png> <edit.png> [...]
"""
import sys

import numpy as np
from PIL import Image

# Floors calibrated 2026-08-31 from the five composites this project has already
# accepted, which score 0.152-0.358 phase and 0.718-0.864 edge keep on THIS estimator.
# NOTE: these numbers are NOT on the same scale as the "0.42 GPT edit-path benchmark"
# and the "0.47-0.58" quoted in prompts/_blocks.md — that session measured by hand and
# left no code, and this implementation does not reproduce its absolute values. Compare
# runs against each other and against the band below, never against those figures.
PHASE_FLOOR = 0.15
EDGE_FLOOR = 0.70


def gray(path, size=None):
    im = Image.open(path).convert("L")
    if size and im.size != size:
        im = im.resize(size, Image.LANCZOS)
    return im, np.asarray(im).astype(float)


def edges(a):
    gx = np.abs(np.diff(a, axis=1))[:-1, :]
    gy = np.abs(np.diff(a, axis=0))[:, :-1]
    return np.hypot(gx, gy)


def verify(plate_path, edit_path):
    imp, p = gray(plate_path)
    ime, e = gray(edit_path, size=imp.size)

    # phase correlation: normalise the cross-power spectrum, the peak is the shift
    P, E = np.fft.rfft2(p - p.mean()), np.fft.rfft2(e - e.mean())
    R = P * np.conj(E)
    R /= np.maximum(np.abs(R), 1e-9)
    corr = np.fft.irfft2(R, s=p.shape)
    peak = float(corr.max())            # unit-magnitude spectrum -> delta of height 1
    iy, ix = np.unravel_index(np.argmax(corr), corr.shape)
    dy = iy - p.shape[0] if iy > p.shape[0] // 2 else iy
    dx = ix - p.shape[1] if ix > p.shape[1] // 2 else ix

    ep, ee = edges(p), edges(e)
    thr = np.percentile(ep, 96)
    strong = ep > thr
    # the character is new ink: exclude where the edit got much darker than the plate
    added = (p - e) > 26
    mask = strong & ~added[:-1, :-1]
    keep = float((ee[mask] > thr * 0.5).mean()) if mask.sum() else float("nan")
    ink = float(added.mean())

    return dict(phase=peak, dx=int(dx), dy=int(dy), edge_keep=keep, ink=ink)


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) % 2 == 0:
        sys.exit("usage: verify_edit.py <plate> <edit> [<plate> <edit> ...]")
    print(f"{'edit':44s} {'phase':>7s} {'shift':>9s} {'edge keep':>10s} {'ink+':>7s}   verdict")
    for i in range(1, len(sys.argv), 2):
        pl, ed = sys.argv[i], sys.argv[i + 1]
        r = verify(pl, ed)
        ok = r["phase"] >= PHASE_FLOOR and r["edge_keep"] >= EDGE_FLOOR and (r["dx"], r["dy"]) == (0, 0)
        print(f"{ed.split('/')[-1]:44s} {r['phase']:7.3f} {str((r['dx'],r['dy'])):>9s} "
              f"{r['edge_keep']:10.3f} {r['ink']:7.3f}   {'pass' if ok else 'CHECK'}")
    print(f"\nfloors: phase >= {PHASE_FLOOR}, edge keep >= {EDGE_FLOOR}, shift == (0,0)"
          " - calibrated from this project's accepted composites, not from the 0.42 figure in _blocks.md")
