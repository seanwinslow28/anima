"""Slice 3 — the read-only artifact/candidate/image surface over run-state.

Pure path/projection helpers; the router owns HTTP. Run-state records file
paths relative to the repo root the pipeline ran from (e.g.
"runs/<id>/candidates/F01/attempt_01.png"). The daemon resolves them against
runs_root.parent — identical to CWD-relative under the default `runs` root the
CLI and daemon both run from, and hermetic under a test tmp root. Nothing here
writes: no save_state, no gate function, no model call.
"""

from __future__ import annotations

import mimetypes
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


def candidates_view(state: dict, run_id: str, n: int) -> list[dict] | None:
    """Project frame n's attempts for the eye-gate screen; None if n isn't a frame.

    Verdict data (T1 + the Em records, incl. reasoning and proposed_patches)
    rides through AS RECORDED — the daemon never re-derives a verdict. Status is
    per-attempt: the frame's approved_attempt is "approved", a failed fan is
    "errored", the rest are "generated".
    """
    if n not in state.get("frame_order", []):
        return None
    rec = state["frames"].get(str(n), {})
    approved = rec.get("approved_attempt")
    out: list[dict] = []
    for a in rec.get("attempts", []):
        idx = a.get("index")
        if idx == approved:
            status = "approved"
        elif a.get("errored"):
            status = "errored"
        else:
            status = "generated"
        out.append({
            "attempt": idx,
            "image_url": (f"/runs/{run_id}/frames/{n}/image?attempt={idx}"
                          if a.get("candidate") else None),
            "status": status,
            "t1": a.get("t1"),
            "em": a.get("em", []),
            "note": a.get("note"),
            "errored": a.get("errored"),
            "ts": a.get("ts"),
        })
    return out


def image_path(state: dict, runs_root: Path, run_dir: Path,
               n: int, attempt: int | None) -> Path | None:
    """The on-disk image for frame n's attempt; None -> 404, never a 500.

    attempt omitted -> the approved key if the frame has one, else the latest
    attempt with a candidate. SECURITY: this feeds a byte-serving endpoint, so
    the resolved path is CONFINED to run_dir — a recorded path that escapes
    (absolute or via dot-segments) returns None and is never served.
    """
    if n not in state.get("frame_order", []):
        return None
    rec = state["frames"].get(str(n), {})
    candidates = [a for a in rec.get("attempts", []) if a.get("candidate")]
    recorded: str | None = None
    if attempt is None:
        if rec.get("approved_attempt") is not None:
            chosen = next((a for a in candidates
                           if a.get("index") == rec["approved_attempt"]), None)
            recorded = rec.get("approved_path") or (chosen["candidate"] if chosen else None)
        elif candidates:
            recorded = max(candidates, key=lambda a: a["index"])["candidate"]
    else:
        chosen = next((a for a in candidates if a.get("index") == attempt), None)
        recorded = chosen["candidate"] if chosen else None
    if not recorded:
        return None
    try:
        resolved = resolve_state_path(runs_root, recorded).resolve()
        confined = resolved.is_relative_to(Path(run_dir).resolve())
    except OSError:
        return None
    if not confined:
        return None
    return resolved if resolved.is_file() else None


def image_media_type(path: Path) -> str:
    return mimetypes.guess_type(path.name)[0] or "application/octet-stream"
