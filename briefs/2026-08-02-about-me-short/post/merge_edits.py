#!/usr/bin/env python3
"""
MERGE EDITS — matte each character off its own edit and lay all of them on the pristine plate.

    python post/merge_edits.py <plate.png> <edit1.png> [<edit2.png> ...] -o <out.png>
        [--zone x0,y0,x1,y1 ...]   one fractional zone per edit, in edit order (optional guard)
        [--thresh 20] [--open 4] [--close 10] [--dilate 14] [--minarea 3000] [--debug dir]

A gpt_image_2 edit re-renders the whole frame with a little noise (verify_edit phase ≈ 0.1–0.2
on accepted composites), so a raw difference against the plate is speckled everywhere. What
separates the character from the speckle is COHERENCE: blur the difference, threshold it, and
keep only the big connected blobs. Each blob is optionally required to touch a zone so a stray
change elsewhere (a re-drawn mug) is never pasted. Edits are laid down in the order given, so
give them far-to-near and overlaps resolve by depth.

numpy + PIL only (the venv has no scipy): connected components are a BFS on a 4× downsample.
FOUND 2026-09-04: thresh 18 / dilate 10 CLIPS thin extremities (an ear tip, a tail) — the
difference under a one-pixel-wide graphite line does not clear the threshold. Use --thresh 12
--dilate 22 for character edits; the wider band pastes a little of the edit's re-rendered
paper around the figure, which the normaliser evens out.

$0, deterministic. Built 2026-09-03 for the S09 five-character composite — the first real run
of the matte-and-relay idea (open item 8), in still form.

CALIBRATED on the S10 Sean composite (v2) against its plate, 2026-09-03: a bare threshold
pasted 41% of the frame (the edit re-draws the lamp and the cork board slightly); opening 4 +
closing 10 + threshold 20 pasted 13.3% — the figure and the chair, whole, nothing else — and
the merge is seamless by eye. Those are the defaults.
"""
import argparse
import os
from collections import deque

import numpy as np
from PIL import Image, ImageFilter


def lum_diff(plate, edit, blur):
    a = np.asarray(plate.convert("L").filter(ImageFilter.GaussianBlur(blur)), dtype=np.float32)
    b = np.asarray(edit.convert("L").filter(ImageFilter.GaussianBlur(blur)), dtype=np.float32)
    # colour matters too (a lavender star on cream): add a chroma term
    pa = np.asarray(plate.convert("RGB"), dtype=np.float32)
    pb = np.asarray(edit.convert("RGB"), dtype=np.float32)
    chroma = np.abs(pa - pb).max(axis=2)
    chroma = np.asarray(Image.fromarray(chroma.astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur)),
                        dtype=np.float32)
    return np.maximum(np.abs(a - b), chroma)


def components(mask):
    """Label 4-connected blobs on a small boolean mask. Returns (labels, sizes)."""
    h, w = mask.shape
    lab = np.zeros((h, w), dtype=np.int32)
    sizes = []
    cur = 0
    for y in range(h):
        for x in range(w):
            if mask[y, x] and lab[y, x] == 0:
                cur += 1
                q = deque([(y, x)]); lab[y, x] = cur; n = 0
                while q:
                    cy, cx = q.popleft(); n += 1
                    for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = cur; q.append((ny, nx))
                sizes.append(n)
    return lab, sizes


def character_mask(plate, edit, zone, thresh, dilate, minarea, ds=4, opening=0, closing=0):
    d = lum_diff(plate, edit, blur=2)
    W, H = plate.size
    small = d[::ds, ::ds] > thresh
    if opening:
        # erode then dilate: thin stroke differences (a re-drawn lamp arm) vanish, solid blobs
        # (a character) survive. Done on the downsample, so `opening` is in ds-pixels.
        sm = Image.fromarray((small * 255).astype(np.uint8))
        k = 2 * opening + 1
        sm = sm.filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))
        small = np.asarray(sm) > 127
    if closing:
        # dilate then erode: fills the holes the opening leaves inside a figure (a torso the
        # same tone as the wall behind it) without growing its outline.
        sm = Image.fromarray((small * 255).astype(np.uint8))
        k = 2 * closing + 1
        sm = sm.filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.MinFilter(k))
        small = np.asarray(sm) > 127
    lab, sizes = components(small)
    keep = np.zeros_like(small)
    for i, n in enumerate(sizes, start=1):
        if n * ds * ds < minarea:
            continue
        ys, xs = np.nonzero(lab == i)
        if zone:
            x0, y0, x1, y1 = zone
            bx0, bx1 = xs.min() * ds / W, (xs.max() + 1) * ds / W
            by0, by1 = ys.min() * ds / H, (ys.max() + 1) * ds / H
            if bx1 < x0 or bx0 > x1 or by1 < y0 or by0 > y1:
                continue
        keep[lab == i] = True
    if zone:                                   # clip to the zone: nothing outside it is ever pasted
        x0, y0, x1, y1 = zone
        clip = np.zeros_like(keep)
        clip[int(y0 * keep.shape[0]):int(y1 * keep.shape[0]) + 1,
             int(x0 * keep.shape[1]):int(x1 * keep.shape[1]) + 1] = True
        keep &= clip
    m = Image.fromarray((keep * 255).astype(np.uint8)).resize((W, H), Image.NEAREST)
    m = m.filter(ImageFilter.MaxFilter(2 * (dilate // 2) + 1))     # dilate
    m = m.filter(ImageFilter.GaussianBlur(2))                       # feather
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plate"); ap.add_argument("edits", nargs="+")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--zone", action="append", default=[])
    ap.add_argument("--thresh", type=float, default=20)
    ap.add_argument("--dilate", type=int, default=14)
    ap.add_argument("--minarea", type=int, default=3000)
    ap.add_argument("--open", type=int, default=4, help="opening radius in 4x-downsampled px")
    ap.add_argument("--close", type=int, default=10, help="closing radius in 4x-downsampled px")
    ap.add_argument("--debug")
    a = ap.parse_args()
    plate = Image.open(a.plate).convert("RGB")
    out = plate.copy()
    zones = [tuple(float(v) for v in z.split(",")) for z in a.zone]
    for i, ep in enumerate(a.edits):
        edit = Image.open(ep).convert("RGB").resize(plate.size, Image.LANCZOS)
        zone = zones[i] if i < len(zones) else None
        m = character_mask(plate, edit, zone, a.thresh, a.dilate, a.minarea, opening=a.open, closing=a.close)
        cov = np.asarray(m).mean() / 255
        print(f"{os.path.basename(ep):40s} zone={zone} pasted {cov*100:5.2f}% of frame")
        out = Image.composite(edit, out, m)
        if a.debug:
            os.makedirs(a.debug, exist_ok=True)
            m.save(os.path.join(a.debug, os.path.basename(ep).replace(".png", "-mask.png")))
    out.save(a.out)
    print("→", a.out)


if __name__ == "__main__":
    main()
