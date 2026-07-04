from __future__ import annotations

from pathlib import Path

from pipeline.orchestration import state as st

from server.state_view import run_summary


def list_runs(runs_root: Path) -> list[dict]:
    """Project every run under runs_root; newest first.

    An unreadable run_state.json is SURFACED as an error item (the Dashboard's
    "Couldn't read this run" state), never dropped and never a 500. A subdir
    without a state file isn't a run and is skipped.
    """
    items: list[dict] = []
    if not runs_root.is_dir():
        return items
    for entry in sorted(runs_root.iterdir()):
        if not entry.is_dir() or not (entry / st.STATE_FILENAME).exists():
            continue
        try:
            items.append(run_summary(st.load_state(entry)))
        except (st.StateError, KeyError, TypeError) as e:
            items.append({"run_id": entry.name, "stage": None, "error": str(e)})
    # ISO-8601 strings sort lexicographically; error items (no updated_at) last.
    items.sort(key=lambda i: i.get("updated_at") or "", reverse=True)
    return items


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
