"""Slice 3 — the read-only artifact/candidate/image surface over run-state.

Pure path/projection helpers; the router owns HTTP. Run-state records file
paths relative to the repo root the pipeline ran from (e.g.
"runs/<id>/candidates/F01/attempt_01.png"). The daemon resolves them against
runs_root.parent — identical to CWD-relative under the default `runs` root the
CLI and daemon both run from, and hermetic under a test tmp root. Nothing here
writes: no save_state, no gate function, no model call.
"""

from __future__ import annotations

from pathlib import Path

# kind -> (state block, key of the exact recorded path, canonical brief_dir
# filename). A FIXED map: `kind` is never interpolated into a path — membership
# here is the artifacts endpoint's traversal guard (resolve_run_dir guards the
# run id).
ARTIFACT_KINDS: dict[str, tuple[str | None, str | None, str]] = {
    "plan": ("plan", "plan_path", "plan.md"),
    "brief": (None, None, "00_studio_brief.md"),
    "script": ("script", "script_path", "script.md"),
    "beats": ("script", "beats_path", "beats.json"),
    "storyboard": ("storyboard", "storyboard_path", "storyboard.md"),
    "shots": ("storyboard", "shots_path", "shots.yaml"),
}

_TEXT_MEDIA = {
    ".md": "text/markdown",
    ".json": "application/json",
    ".yaml": "text/plain",
    ".yml": "text/plain",
}


def resolve_state_path(runs_root: Path, recorded: str) -> Path:
    """Map a state-recorded path onto this daemon's filesystem view."""
    p = Path(recorded)
    return p if p.is_absolute() else runs_root.parent / p


def artifact_path(state: dict, runs_root: Path, kind: str) -> Path | None:
    """The on-disk file for an artifact kind, or None (unknown kind / no file).

    Prefers the exact path recorded in state where present — a back-compat run
    has no script/storyboard block, so those fall to the canonical filename
    under brief_dir and 404 honestly when absent.
    """
    spec = ARTIFACT_KINDS.get(kind)
    if spec is None:
        return None
    block, key, canonical = spec
    recorded = (state.get(block) or {}).get(key) if block else None
    if recorded:
        path = resolve_state_path(runs_root, recorded)
    else:
        path = resolve_state_path(runs_root, state["brief_dir"]) / canonical
    return path if path.is_file() else None


def artifact_media_type(path: Path) -> str:
    return _TEXT_MEDIA.get(path.suffix.lower(), "text/plain")
