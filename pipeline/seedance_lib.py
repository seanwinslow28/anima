"""Shared helpers for the Seedance pipeline scripts.

Provides: environment loading, shot-list parsing, run-directory creation,
fal.ai anchor upload with URL caching, structured JSONL event logging,
12fps frame-count math, and JPEG-as-PNG re-encoding.

Import this module from seedance_generate.py, seedance_extract.py,
seedance_cleanup.py, and seedance_audit.py.  It has no CLI entry point.
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Shot-list loader
# ---------------------------------------------------------------------------


def load_shotlist(path: str | Path) -> dict:
    """Load and return the parsed shot-list YAML.

    Raises FileNotFoundError if the file is missing (yaml.safe_load propagates
    it naturally, but we check explicitly for a clear message).
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Shot-list YAML not found: {path}")
    with open(path) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# .env loader
# ---------------------------------------------------------------------------


def load_env(env_file: str | Path = ".env") -> None:
    """Parse a .env file (KEY=VALUE per line) and merge into os.environ.

    Same correctness rules as generate_image.py (skip blanks/comments, strip
    whitespace, no-clobber); extends it with general single/double quote
    stripping rather than the key-specific stripping in that script.

    Rules:
    - Skip blank lines and lines starting with '#'.
    - Strip whitespace around both KEY and VALUE.
    - Strip surrounding single or double quotes from VALUE.
    - Do NOT overwrite a key that is already present in os.environ.
    """
    env_path = Path(env_file)
    if not env_path.exists():
        raise FileNotFoundError(
            f".env file not found: {env_path.resolve()}.  "
            "Create it with FAL_KEY=<your-key> (and optionally GEMINI_API_KEY=...)."
        )
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip("'\"")
            if key and key not in os.environ:
                os.environ[key] = value


# ---------------------------------------------------------------------------
# Run-directory factory
# ---------------------------------------------------------------------------

_STANDARD_SUBDIRS = ("seedance", "extracted", "cleanup", "shots", "audit", "export")


def make_run_dir(
    prefix: str = "act2-seedance",
    base: str | Path = "runs",
) -> Path:
    """Create runs/{prefix}-{YYYY-MM-DD}/ with all standard subdirs.

    Standard subdirs: seedance/, extracted/, cleanup/, shots/, audit/, export/

    Idempotent: if the directory already exists the subdirs are ensured and
    the path is returned without error.

    Returns the Path to the run directory.
    """
    date_stamp = datetime.now().strftime("%Y-%m-%d")
    run_dir = Path(base) / f"{prefix}-{date_stamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    for sub in _STANDARD_SUBDIRS:
        (run_dir / sub).mkdir(exist_ok=True)
    return run_dir


# ---------------------------------------------------------------------------
# Anchor uploader (fal.ai) with local JSON cache
# ---------------------------------------------------------------------------


def upload_anchor(path: str | Path, cache_path: str | Path) -> str:
    """Upload a local anchor image to fal.ai and return its URL.

    Results are cached in *cache_path* (a JSON file mapping path strings to
    URLs).  Subsequent calls for the same *path* return the cached URL
    immediately without re-uploading.

    The fal_client import is deferred to this function so that importing
    seedance_lib never fails if fal_client is absent or FAL_KEY is unset.
    """
    import fal_client  # noqa: PLC0415 — deferred intentionally

    path_key = str(Path(path))
    cache_path = Path(cache_path)

    # Load existing cache (treat missing file as empty).
    if cache_path.exists():
        with open(cache_path) as f:
            cache: dict[str, str] = json.load(f)
    else:
        cache = {}

    if path_key in cache:
        return cache[path_key]

    # Upload and persist.
    url: str = fal_client.upload_file(path_key)
    cache[path_key] = url
    with open(cache_path, "w") as f:
        json.dump(cache, f, indent=2)

    return url


# ---------------------------------------------------------------------------
# Structured JSONL event logger
# ---------------------------------------------------------------------------


def log_event(run_dir: str | Path, event: dict) -> None:
    """Append one JSON line to {run_dir}/audit/seedance_log.jsonl.

    Auto-injects two fields if not already present in the event:
      - timestamp: ISO 8601 with second precision
      - event_id: first 8 hex chars of a random uuid4

    Does NOT mutate the caller's dict — works on a shallow copy.
    """
    record = dict(event)  # shallow copy — don't mutate caller's dict
    if "timestamp" not in record:
        record["timestamp"] = datetime.now().isoformat(timespec="seconds")
    if "event_id" not in record:
        record["event_id"] = uuid.uuid4().hex[:8]

    log_path = Path(run_dir) / "audit" / "seedance_log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(record) + "\n")


# ---------------------------------------------------------------------------
# Frame-count math
# ---------------------------------------------------------------------------


def frame_count_at_12fps(duration_s: float | int) -> int:
    """Return the number of frames in a clip of *duration_s* seconds at 12fps.

    Example: frame_count_at_12fps(5) → 60
    """
    return int(duration_s * 12)


# ---------------------------------------------------------------------------
# JPEG-as-PNG re-encoder
# ---------------------------------------------------------------------------


def reencode_to_png(path: str | Path) -> None:
    """Re-encode a file in place to a true PNG.

    Gemini's NB2 returns JPEG bytes even when the output extension is .png.
    FFmpeg's image2 demuxer then silently drops those frames during assembly.
    This function converts the file to a proper PNG regardless of its current
    internal format.  Calling it on a file that is already a valid PNG is
    safe and idempotent.

    See pipeline/assemble.sh:153-169 for the shell-script equivalent.
    """
    from PIL import Image  # noqa: PLC0415 — deferred to avoid hard PIL dep at import

    img_path = Path(path)
    Image.open(img_path).convert("RGB").save(img_path, format="PNG")
