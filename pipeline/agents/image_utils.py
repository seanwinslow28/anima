"""Small image-format utilities shared by the generation agents.

#12: the Gemini pencil skill (and the NB transports it wraps) can hand back
JPEG bytes written under an `attempt_NN.png` name. ffmpeg's PNG decoder then
silently drops those frames, and the future museum capture would copy a
mislabeled thumbnail. normalize_to_png fixes it at the source — the FloNode
return boundary — so every downstream consumer (Em, assemble, museum) gets a
real PNG. assemble.sh keeps its own Step 2b re-encode as a defensive backstop.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, UnidentifiedImageError


def normalize_to_png(path: Path) -> bool:
    """Ensure the file at ``path`` is a real PNG, re-encoding in place if not.

    Returns True if the file was rewritten (it was not already PNG), False if it
    was already a PNG and left byte-identical — so an already-correct candidate
    is never needlessly re-saved.

    Defensive: this runs at FloNode's per-frame return boundary, so a file that
    PIL can't even open (a malformed transport output) is left untouched and
    returns False rather than crashing the node — downstream audit / Em catch a
    genuine non-image; normalization only fixes a mislabeled *valid* image.
    """
    p = Path(path)
    try:
        with Image.open(p) as img:
            if img.format == "PNG":
                return False
            img.load()  # fully read before we overwrite the source
            converted = img.convert("RGB") if img.mode not in ("RGB", "RGBA", "L") else img
    except (UnidentifiedImageError, OSError):
        return False
    converted.save(p, format="PNG")
    return True
