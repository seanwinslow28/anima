from pipeline.orchestration import state as st

from server.runs import resolve_run_dir
from server.state_view import next_action, status_view


def _base():
    return st.new_state(run_id="r", brief_dir="b", manifest_path="m",
                        shots_path="s", slug="X", stub=True, cast=[])


def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_resolve_run_dir_found(make_run, runs_root):
    run_dir, _ = make_run("abc")
    assert resolve_run_dir(runs_root, "abc") == run_dir


def test_resolve_run_dir_missing(runs_root):
    assert resolve_run_dir(runs_root, "nope") is None


def test_resolve_run_dir_rejects_traversal(runs_root):
    for bad in ["../etc", "a/b", "..", ".hidden", "", "a\\b"]:
        assert resolve_run_dir(runs_root, bad) is None


def test_next_action_plan_planning_then_approve():
    s = _base()
    assert next_action(s)["kind"] == "planning"       # plan.status == "pending"
    s["plan"]["status"] = "drafted"
    na = next_action(s)
    assert na["kind"] == "approve_plan"
    assert "--approve-plan" in na["hint"]             # provenance from _next_hint


def test_next_action_script_in_progress_then_approve():
    s = _base(); s["stage"] = "SCRIPT"
    assert next_action(s)["kind"] == "scripting"          # no script.status yet
    s["script"] = {"status": "drafted"}
    assert next_action(s)["kind"] == "approve_script"


def test_next_action_storyboard_in_progress_then_approve():
    s = _base(); s["stage"] = "STORYBOARD"
    assert next_action(s)["kind"] == "storyboarding"      # no storyboard.status yet
    s["storyboard"] = {"status": "drafted"}
    assert next_action(s)["kind"] == "approve_storyboard"


def test_next_action_animatic():
    s = _base(); s["stage"] = "ANIMATIC"
    assert next_action(s)["kind"] == "approve_animatic"


def test_next_action_generate_generating_review_then_assemble():
    s = _base(); s["stage"] = "GENERATE"; s["frame_order"] = [1]
    st.set_frame(s, 1, {"status": "pending", "attempts": []})
    assert next_action(s)["kind"] == "generating"         # frame not yet generated
    st.get_frame(s, 1)["status"] = "generated"
    na = next_action(s)
    assert na["kind"] == "review_frame" and na["frame"] == 1
    st.get_frame(s, 1)["status"] = "approved"
    assert next_action(s)["kind"] == "assemble"           # current_frame is None


def test_next_action_assemble_stage_and_done():
    s = _base(); s["stage"] = "ASSEMBLE"
    assert next_action(s)["kind"] == "assemble"
    s["stage"] = "DONE"
    assert next_action(s)["kind"] == "done"


def test_status_view_shape_plan_stage():
    s = _base()
    view = status_view(s)
    assert view["run_id"] == "r"
    assert view["stage"] == "PLAN"
    assert view["stub"] is True
    assert view["plan_status"] == "pending"
    assert view["next_action"]["kind"] == "planning"
    assert view["frames"] == []


def test_status_view_frames_projection():
    s = _base(); s["stage"] = "GENERATE"; s["frame_order"] = [1, 2]
    s["holds"] = {"1": 3}
    st.set_frame(s, 1, {"status": "approved", "attempts": [{"index": 1}, {"index": 2}]})
    st.set_frame(s, 2, {"status": "generated", "attempts": [{"index": 1}]})
    frames = status_view(s)["frames"]
    assert [f["n"] for f in frames] == [1, 2]
    assert frames[0] == {"n": 1, "status": "approved", "attempts": 2, "hold": 3}
    assert frames[1]["status"] == "generated" and frames[1]["hold"] == 2  # default hold
