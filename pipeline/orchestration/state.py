"""Durable orchestrator state — runs/<id>/run_state.json.

The single source of truth across `python -m pipeline.run` invocations.
JSON object keys are strings, so `frames`/`holds` are keyed by str(frame_num)
on disk AND in memory; the int-taking accessors below own that boundary.
Writes are atomic (serialize first, tmp + replace) so a crash mid-save never
corrupts a resumable run.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

STATE_FILENAME = "run_state.json"
STAGES = ("PLAN", "GENERATE", "ASSEMBLE", "DONE")
_LEGAL_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "PLAN": ("GENERATE",),
    "GENERATE": ("ASSEMBLE",),
    "ASSEMBLE": ("DONE",),
    "DONE": (),
}


class StateError(Exception):
    """Unusable or illegal run state — missing file, corrupt JSON, bad transition."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_state(
    *,
    run_id: str,
    brief_dir: str,
    manifest_path: str,
    shots_path: str,
    slug: str,
    stub: bool,
    cast: list[dict],
    brief_src: str | None = None,
) -> dict:
    now = _now()
    return {
        "schema_version": 1,
        "run_id": run_id,
        "created_at": now,
        "updated_at": now,
        "brief_dir": brief_dir,
        "brief_src": brief_src,
        "manifest_path": manifest_path,
        "shots_path": shots_path,
        "slug": slug,
        "stub": stub,
        "stage": "PLAN",
        "cast": cast,
        "plan": {
            "status": "pending",
            "plan_path": None,
            "criteria_path": None,
            "production_brief_path": None,
            "cost_estimate": None,
            "stub": stub,
        },
        "frame_order": [],
        "holds": {},
        "frames": {},
        "assemble": {"sequence_file": None, "gif": None, "webm": None, "mp4": None},
    }


def load_state(run_dir: Path) -> dict:
    path = Path(run_dir) / STATE_FILENAME
    if not path.exists():
        raise StateError(
            f"no {STATE_FILENAME} at {path} — not an orchestrator run dir "
            "(start a run with --brief <dir>)"
        )
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise StateError(f"corrupt {STATE_FILENAME} at {path}: {e}") from e
    if state.get("schema_version") != 1:
        raise StateError(
            f"unsupported run_state schema_version={state.get('schema_version')!r} at {path}"
        )
    return state


def save_state(run_dir: Path, state: dict) -> None:
    state["updated_at"] = _now()
    text = json.dumps(state, indent=2)  # serialize BEFORE touching disk
    path = Path(run_dir) / STATE_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def advance_stage(state: dict, to: str) -> None:
    cur = state["stage"]
    if to not in _LEGAL_TRANSITIONS.get(cur, ()):
        raise StateError(f"illegal stage transition {cur} -> {to} (legal: {STAGES})")
    state["stage"] = to


def get_frame(state: dict, n: int) -> dict:
    try:
        return state["frames"][str(n)]
    except KeyError:
        raise StateError(f"frame {n} is not in this run's state") from None


def set_frame(state: dict, n: int, record: dict) -> None:
    state["frames"][str(n)] = record


def get_hold(state: dict, n: int) -> int:
    return int(state["holds"].get(str(n), 2))


def current_frame(state: dict) -> int | None:
    """First frame in frame_order not yet approved — the one at (or before) the eye gate."""
    for n in state["frame_order"]:
        if state["frames"].get(str(n), {}).get("status") != "approved":
            return n
    return None


def render_status(state: dict) -> str:
    lines = [
        f"run:     {state['run_id']}",
        f"stage:   {state['stage']}" + ("  [stub]" if state.get("stub") else ""),
        f"brief:   {state['brief_dir']}"
        + (f"  (snapshot of {state['brief_src']})" if state.get("brief_src") else ""),
        f"slug:    {state['slug']}",
        f"plan:    {state['plan']['status']}"
        + ("  [stub plan — do not approve as real]" if state["plan"].get("stub") else ""),
    ]
    if state["frame_order"]:
        lines.append("frames:")
        for n in state["frame_order"]:
            rec = state["frames"].get(str(n), {})
            attempts = rec.get("attempts", [])
            mark = {"approved": "x", "generated": "o"}.get(rec.get("status"), " ")
            lines.append(
                f"  [{mark}] F{n:02d}  {rec.get('status', 'pending'):9s}"
                f"  attempts={len(attempts)}  hold={get_hold(state, n)}"
            )
    lines.append(_next_hint(state))
    return "\n".join(lines)


def _next_hint(state: dict) -> str:
    stage = state["stage"]
    if stage == "PLAN":
        if state["plan"]["status"] == "drafted":
            return "next:    review the plan, then --resume <run-dir> --approve-plan"
        return "next:    run --brief <dir> to draft the plan"
    if stage == "GENERATE":
        n = current_frame(state)
        if n is None:
            return "next:    all frames approved — re-invoke to assemble"
        rec = state["frames"].get(str(n), {})
        if rec.get("status") == "generated":
            return (
                f"next:    eye F{n:02d}, then --approve-frame {n} [--attempt K] "
                f"or --retry-frame {n} --note \"...\""
            )
        return f"next:    generate F{n:02d} (re-invoke with --retry-frame {n} --note if stuck)"
    if stage == "ASSEMBLE":
        return "next:    re-invoke to run the assemble tail"
    return f"done:    {state['assemble']}"
