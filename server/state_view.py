from __future__ import annotations

from pipeline.orchestration import state as st


def next_action(state: dict) -> dict:
    """Project run-state onto a machine token + the pipeline's own CLI hint.

    Reuses state._next_hint for the human string so the daemon never re-derives
    the pipeline's 'what to do next' logic. `kind` is the UI navigation token.
    """
    stage = state["stage"]
    hint = st._next_hint(state)
    if stage == "PLAN":
        kind = "approve_plan" if state["plan"]["status"] == "drafted" else "planning"
        return {"kind": kind, "hint": hint}
    if stage == "SCRIPT":
        drafted = state.get("script", {}).get("status") == "drafted"
        return {"kind": "approve_script" if drafted else "scripting", "hint": hint}
    if stage == "STORYBOARD":
        drafted = state.get("storyboard", {}).get("status") == "drafted"
        return {"kind": "approve_storyboard" if drafted else "storyboarding", "hint": hint}
    if stage == "ANIMATIC":
        return {"kind": "approve_animatic", "hint": hint}
    if stage == "GENERATE":
        n = st.current_frame(state)
        if n is None:
            return {"kind": "assemble", "hint": hint}
        rec = state["frames"].get(str(n), {})
        kind = "review_frame" if rec.get("status") == "generated" else "generating"
        return {"kind": kind, "frame": n, "hint": hint}
    if stage == "ASSEMBLE":
        return {"kind": "assemble", "hint": hint}
    return {"kind": "done", "hint": hint}


def run_summary(state: dict) -> dict:
    return {
        "run_id": state["run_id"],
        "stage": state["stage"],
        "slug": state["slug"],
        "stub": bool(state.get("stub")),
        "updated_at": state.get("updated_at"),
        "next_action": next_action(state),
    }


def status_view(state: dict, active_job: dict | None = None) -> dict:
    """Project run-state for the status endpoint.

    active_job (Slice 4) is the job-layer overlay — {job_id, mutation_status}
    while a job owns the run, else None. The key is always present. Codex
    blocker-2 context: a cascading gate saves an intermediate stage mid-job, so
    a bare next_action can invite a duplicate action (e.g. approve_frame saves
    ASSEMBLE before assemble finishes -> a GET offers a duplicate --assemble).
    Slice 5 suppresses that: while a job owns the run, next_action carries an
    additive `blocked_by_job` = the owning job_id (kind unchanged), so the UI
    disables the mutating action until the job goes terminal. Idle -> the key is
    absent, not None.
    """
    frames = []
    for n in state.get("frame_order", []):
        rec = state["frames"].get(str(n), {})
        frames.append({
            "n": n,
            "status": rec.get("status", "pending"),
            "attempts": len(rec.get("attempts", [])),
            "hold": st.get_hold(state, n),
        })
    na = next_action(state)
    if active_job:
        na = {**na, "blocked_by_job": active_job["job_id"]}
    return {
        "run_id": state["run_id"],
        "stage": state["stage"],
        "stub": bool(state.get("stub")),
        "plan_status": state["plan"]["status"],
        "next_action": na,
        "active_job": active_job,
        "frames": frames,
        "updated_at": state.get("updated_at"),
    }
