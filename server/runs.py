from __future__ import annotations

from pathlib import Path

from pipeline.orchestration import state as st


def resolve_run_dir(runs_root: Path, run_id: str) -> Path | None:
    # Reject separators / dot-segments, then confirm the resolved path is a
    # DIRECT child of runs_root (traversal-proof, and not over-broad: a legit id
    # that merely contains ".." as characters is fine — only path segments matter).
    if not run_id or "/" in run_id or "\\" in run_id or run_id.startswith("."):
        return None
    candidate = (runs_root / run_id)
    try:
        if candidate.resolve().parent != runs_root.resolve():
            return None
    except OSError:
        return None
    if (candidate / st.STATE_FILENAME).exists():
        return candidate
    return None
