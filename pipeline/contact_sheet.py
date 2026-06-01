"""Deterministic contact-sheet builder for motion-clip review.

Em is a still-image judge. To let her assess *identity and style across a
clip* (NOT motion-proper — see docs/research/2026-05-31-ai-evals-...md §3.5),
we sample N evenly-spaced frames from a Seedance clip and tile them into one
PNG where left->right, top->bottom is time. Each panel carries a small index
label so the temporal order is explicit in the pixels, not just implied.

The decisive research finding (arXiv 2505.14321): MLLMs frequently answer
video questions correctly even on *shuffled* frames — so a contact sheet does
NOT give Em motion-proper sight. It gives her content-across-time:
identity-drift, style/register-drift, stylus-hand continuity, outfit
consistency. The honesty clause in vision_critic._build_prompt makes that
limit explicit to the model.

Source can be a video file (ffmpeg extracts frames) or a directory of
pre-extracted frames (Act 1 already has these). Sampling is deterministic.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

_VIDEO_SUFFIXES = {".mp4", ".webm", ".mov", ".gif"}
_LABEL_STRIP_H = 14


def sample_frame_indices(*, total_frames: int, n: int) -> list[int]:
    """Return n evenly-spaced 0-based frame indices spanning [0, total-1].

    Always includes the first and last frame. If total <= n, returns all
    indices. No duplicates, sorted ascending.
    """
    if total_frames <= 0:
        return []
    if total_frames <= n:
        return list(range(total_frames))
    # Evenly spaced including endpoints: round(i * (total-1) / (n-1)).
    step = (total_frames - 1) / (n - 1)
    idx = sorted({round(i * step) for i in range(n)})
    # Rounding can collide near the ends on tiny clips; backfill to n if so.
    if len(idx) < n:
        for cand in range(total_frames):
            if cand not in idx:
                idx.append(cand)
            if len(idx) == n:
                break
        idx = sorted(idx)
    return idx


def _extract_frames_to_dir(video: Path, work: Path) -> list[Path]:
    """ffmpeg-extract every frame of `video` into `work` as f_%04d.png."""
    out_pattern = str(work / "f_%04d.png")
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(video), out_pattern,
    ]
    subprocess.run(cmd, check=True)
    return sorted(work.glob("f_*.png"))


def _collect_source_frames(source: Path, work: Path) -> list[Path]:
    if source.is_dir():
        frames = sorted(p for p in source.iterdir()
                        if p.suffix.lower() in {".png", ".jpg", ".jpeg"})
        if not frames:
            raise FileNotFoundError(f"No image frames found in {source}")
        return frames
    if not source.exists():
        raise FileNotFoundError(str(source))
    if source.suffix.lower() in _VIDEO_SUFFIXES:
        return _extract_frames_to_dir(source, work)
    raise ValueError(f"Unsupported source: {source}")


def build_contact_sheet(
    *,
    source: Path,
    out_path: Path,
    n: int = 6,
    cols: int = 3,
    panel_width: int = 320,
    label: bool = True,
) -> Path:
    """Tile n evenly-spaced frames from `source` into one PNG at `out_path`.

    `source` may be a video file or a directory of pre-extracted frames.
    Panels are scaled to `panel_width` (height preserves aspect). A small
    index strip (`t0`, `t1`, ...) is drawn under each panel when `label`.
    Returns out_path.
    """
    source = Path(source)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        all_frames = _collect_source_frames(source, work)
        idx = sample_frame_indices(total_frames=len(all_frames), n=n)
        picked = [Image.open(all_frames[i]).convert("RGB") for i in idx]

        # Uniform panel size from the first frame's aspect.
        ar = picked[0].height / picked[0].width
        pw = panel_width
        ph = round(pw * ar)
        strip = _LABEL_STRIP_H if label else 0
        panels = [p.resize((pw, ph)) for p in picked]

        rows = (len(panels) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * pw, rows * (ph + strip)), (255, 255, 255))
        draw = ImageDraw.Draw(sheet)
        for slot, panel in enumerate(panels):
            r, c = divmod(slot, cols)
            x, y = c * pw, r * (ph + strip)
            sheet.paste(panel, (x, y))
            if label:
                draw.text((x + 3, y + ph + 1), f"t{slot}", fill=(0, 0, 0))

        sheet.save(out_path)
    return out_path
