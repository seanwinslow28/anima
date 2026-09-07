#!/usr/bin/env python3
"""
TYPEWRITER REVEAL — beat 13. The question appears on the chat-box still line by line, left to
right, the way typing reads. Post, exact, $0: the still already carries the finished text in
the model's own hand-lettering; this masks it with the bubble's own paper colour and unmasks it.

    $0.  Usage:  typewriter_reveal.py <chat-still.png> <out.mp4> [seconds=4] [hold=1.5] [fps=24]
    LINES are the text bands in the still's pixel space (2688x1520); PAPER_SAMPLE is where the
    bubble's blank paper is sampled for the mask colour.
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw

LINES = [(935, 660, 1665, 740), (935, 740, 1665, 815), (935, 815, 1665, 890), (935, 890, 1665, 968)]
PAPER_SAMPLE = (1690, 700, 1710, 720)
FRAME_W, FRAME_H = 1280, 720

def main():
    still = Image.open(sys.argv[1]).convert("RGB"); out = sys.argv[2]
    seconds = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
    hold = float(sys.argv[4]) if len(sys.argv) > 4 else 1.5
    fps = int(sys.argv[5]) if len(sys.argv) > 5 else 24
    # mask colour = the bubble's own paper: the bright 85th-percentile of the text bands themselves
    import numpy as np
    px = np.concatenate([np.asarray(still.crop(b)).reshape(-1, 3) for b in LINES])
    patch = tuple(int(v) for v in np.percentile(px, 85, axis=0))
    type_frames = int(seconds * fps); total = type_frames + int(hold * fps)
    per_line = type_frames / len(LINES)
    tmp = tempfile.mkdtemp()
    for f in range(total):
        fr = still.copy(); d = ImageDraw.Draw(fr)
        progress = f / per_line  # lines revealed so far, fractional
        for i, (x0, y0, x1, y1) in enumerate(LINES):
            done = max(0.0, min(1.0, progress - i))
            if f % 2 and done < 1.0: done = max(0.0, min(1.0, (f - 1) / per_line - i))  # held on twos
            xr = int(x0 + (x1 - x0) * done)
            if xr < x1: d.rectangle([xr, y0, x1, y1], fill=patch)
        fr = fr.resize((FRAME_W, FRAME_H), Image.LANCZOS)
        fr.save(os.path.join(tmp, f"f{f:04d}.png"))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(fps), "-i", os.path.join(tmp, "f%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out], check=True)
    print(f"{out}  {total} frames ({seconds}s typing + {hold}s hold) · mask colour {patch}")

if __name__ == "__main__":
    main()
