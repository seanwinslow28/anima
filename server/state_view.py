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
