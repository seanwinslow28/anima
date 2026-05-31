"""Assemble a set of colored motion frames into a seamless looping GIF.

The colored animatic frames are RGBA with transparent backgrounds and varying
dimensions. We composite each onto cream paper (#F2E6CC — the pencil-test-colored
register's paper) on a uniform canvas so the loop doesn't jitter, then write an
animated GIF that ping-pongs (forward then back) for a seamless settle loop.

Pillow only — no FFmpeg subprocess. The true side-by-side comparison GIF
(hand-drawn key sheet left, this loop right, hstacked) is Phase 4; this is the
'right side' on its own, which is enough to apply the engine-truth test in a
browser: does the loop play, and is the character recognizably itself?
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

PAPER = (0xF2, 0xE6, 0xCC)  # cream — matches the register
_PAD = 0.08                  # 8% breathing room around the largest frame


def _hex_to_rgb(value) -> tuple[int, int, int]:
    if isinstance(value, tuple):
        return value
    v = value.lstrip("#")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


def assemble_loop_gif(
    frame_paths: list[Path],
    out_path: Path,
    *,
    bg=PAPER,
    duration_ms: int = 170,
    pingpong: bool = True,
) -> Path | None:
    """Composite frames onto a uniform cream canvas and write a looping GIF.

    Returns out_path, or None when there are no frames (skip cleanly — not every
    exhibit has a frame sequence).
    """
    paths = [Path(p) for p in frame_paths if Path(p).exists()]
    if not paths:
        return None

    bg_rgb = _hex_to_rgb(bg)
    loaded = [Image.open(p).convert("RGBA") for p in paths]

    pad_w = int(max(im.width for im in loaded) * (1 + _PAD))
    pad_h = int(max(im.height for im in loaded) * (1 + _PAD))

    composited: list[Image.Image] = []
    for im in loaded:
        canvas = Image.new("RGBA", (pad_w, pad_h), (*bg_rgb, 255))
        offset = ((pad_w - im.width) // 2, (pad_h - im.height) // 2)
        canvas.alpha_composite(im, offset)
        composited.append(canvas.convert("RGB"))

    # Ping-pong: forward then back (excluding the endpoints) so the loop is
    # seamless regardless of whether the motion is a true cycle.
    sequence = list(composited)
    if pingpong and len(composited) > 2:
        sequence = composited + composited[-2:0:-1]

    # Stable shared palette so colors don't flicker frame-to-frame.
    palette_src = sequence[0].quantize(colors=128)
    quantized = [f.quantize(palette=palette_src) for f in sequence]

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    quantized[0].save(
        out_path, save_all=True, append_images=quantized[1:],
        duration=duration_ms, loop=0, optimize=False, disposal=2,
    )
    return out_path
