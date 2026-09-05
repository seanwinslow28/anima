#!/usr/bin/env python3
"""
CLOSE-UP END FRAME — crop a push-in target out of a plate that already exists.

For a two-keyframe push-in, the end frame has to be the SAME DRAWING seen closer, not a new
drawing of the same thing. Generating a close-up would be a re-angle, and gpt_image_2 will not
re-camera from an edit (see prompts/_blocks.md) — it would have to be reconstructed, at cost,
with a real risk the television comes back a different television.

Cropping is free and cannot drift: it IS the plate. The only cost is resolution, and there
almost isn't one here. The crop is ~1000px wide out of a 2688px plate and the clip renders at
1280x720, so the real upscale at output is ~1.3x on a soft graphite drawing.

    $0.  Usage:  make_closeup.py <src.png> <cx,cy,w,h> <out.png>
"""
import sys

from PIL import Image

if __name__ == "__main__":
    src = Image.open(sys.argv[1]).convert("RGB")
    cx, cy, w, h = [int(v) for v in sys.argv[2].split(",")]
    box = (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2)
    if box[0] < 0 or box[1] < 0 or box[2] > src.size[0] or box[3] > src.size[1]:
        sys.exit(f"crop {box} falls outside {src.size}")
    out = src.crop(box).resize(src.size, Image.LANCZOS)
    out.save(sys.argv[3])
    print(f"{sys.argv[3]}  crop {w}x{h} of {src.size[0]}x{src.size[1]} "
          f"({src.size[0]/w:.2f}x push-in) · effective upscale at 720p output "
          f"{1280/w:.2f}x")
