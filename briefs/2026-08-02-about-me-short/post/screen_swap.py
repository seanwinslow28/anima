#!/usr/bin/env python3
"""
SCREEN SWAP — build a two-keyframe END frame that differs from the START frame ONLY
inside one rectangle.

Why this exists. S07's first two-keyframe roll handed seedance_2_0 a dark plate and a
gpt_image_2 edit of that plate. The edit passed post/verify_edit.py (phase 0.272, shift
(0,0)) and was still, pixel for pixel, a slightly DIFFERENT ROOM everywhere — a marginally
larger CRT bezel, a hair of line variation across every fixture. Given two subtly different
rooms the model reconciled them by MOVING THE CAMERA: layout against the start frame fell
0.989 -> 0.931 and the framing visibly breathes.

A surgical edit is surgical by the verifier's standards, not by a video model's. So compose
the end keyframe in post instead: take the start frame, paste in the one rectangle that is
supposed to change, and the model is left with nothing to reconcile.

    $0.  Usage:  screen_swap.py <start.png> <lit.png> <x0,y0,x1,y1> <out.png>
"""
import sys

from PIL import Image

if __name__ == "__main__":
    start = Image.open(sys.argv[1]).convert("RGB")
    lit = Image.open(sys.argv[2]).convert("RGB")
    x0, y0, x1, y1 = [int(v) for v in sys.argv[3].split(",")]
    if lit.size != start.size:
        lit = lit.resize(start.size, Image.LANCZOS)
    out = start.copy()
    out.paste(lit.crop((x0, y0, x1, y1)), (x0, y0))
    out.save(sys.argv[4])
    px = (x1 - x0) * (y1 - y0)
    print(f"{sys.argv[4]}  changed {px:,} px = {100.0*px/(start.size[0]*start.size[1]):.2f}% "
          f"of frame; every other pixel is byte-identical to the start frame")
