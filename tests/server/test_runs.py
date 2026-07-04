import json

from pipeline.orchestration import state as st

from server.runs import list_runs
from server.state_view import next_action, run_summary


def _stamp_updated_at(run_dir, value: str) -> None:
    """Write updated_at directly (save_state would restamp it with wall-clock)."""
    path = run_dir / st.STATE_FILENAME
    data = json.loads(path.read_text(encoding="utf-8"))
    data["updated_at"] = value
    path.write_text(json.dumps(data), encoding="utf-8")


def test_run_summary_shape(make_run):
    run_dir, _ = make_run("summary-run")
    state = st.load_state(run_dir)  # post-save state carries the stamped updated_at
    summary = run_summary(state)
    assert summary == {
        "run_id": "summary-run",
        "stage": "PLAN",
        "slug": "DEMO",
        "stub": True,
        "updated_at": state["updated_at"],
        "next_action": next_action(state),
    }


def test_get_run_returns_full_state(client, make_run):
    run_dir, _ = make_run("2026-07-04-full-state")
    r = client.get("/runs/2026-07-04-full-state")
    assert r.status_code == 200
    body = r.json()
    assert "stage" in body and "plan" in body and "frames" in body
    # Raw passthrough: the response IS the state on disk, no projection.
    assert body == st.load_state(run_dir)


def test_list_runs_empty_root(runs_root):
    assert list_runs(runs_root) == []


def test_list_runs_two_runs_present(make_run, runs_root):
    make_run("run-a")
    make_run("run-b")
    items = list_runs(runs_root)
    assert {i["run_id"] for i in items} == {"run-a", "run-b"}
    for item in items:
        assert item["stage"] == "PLAN"
        assert item["slug"] == "DEMO"
        assert item["next_action"]["kind"] == "planning"


def test_list_runs_skips_dir_without_state_file(make_run, runs_root):
    make_run("real-run")
    (runs_root / "not-a-run").mkdir()  # no run_state.json — not a run
    items = list_runs(runs_root)
    assert [i["run_id"] for i in items] == ["real-run"]


def test_list_runs_sorted_by_updated_at_desc(make_run, runs_root):
    # save_state stamps updated_at itself and two calls can collide; write two
    # DISTINCT values directly into the state files, then assert order.
    older, _ = make_run("older-run")
    newer, _ = make_run("newer-run")
    _stamp_updated_at(older, "2026-07-01T00:00:00")
    _stamp_updated_at(newer, "2026-07-04T00:00:00")
    items = list_runs(runs_root)
    assert [i["run_id"] for i in items] == ["newer-run", "older-run"]


def test_list_runs_surfaces_corrupt_run_as_error_item(make_run, runs_root):
    good, _ = make_run("good-run")
    _stamp_updated_at(good, "2026-07-04T00:00:00")
    corrupt = runs_root / "corrupt-run"
    corrupt.mkdir()
    (corrupt / st.STATE_FILENAME).write_text("{ not json", encoding="utf-8")
    items = list_runs(runs_root)
    assert [i["run_id"] for i in items] == ["good-run", "corrupt-run"]  # error sorts last
    err = items[1]
    assert err["stage"] is None
    assert "run_state.json" in err["error"]


def test_list_endpoint_empty(client):
    r = client.get("/runs")
    assert r.status_code == 200
    assert r.json() == []


def test_list_endpoint_two_runs_newest_first(client, make_run):
    older, _ = make_run("older-run")
    newer, _ = make_run("newer-run")
    _stamp_updated_at(older, "2026-07-01T00:00:00")
    _stamp_updated_at(newer, "2026-07-04T00:00:00")
    r = client.get("/runs")
    assert r.status_code == 200
    body = r.json()
    assert [i["run_id"] for i in body] == ["newer-run", "older-run"]
    assert set(body[0]) == {"run_id", "stage", "slug", "stub", "updated_at", "next_action"}


def test_list_endpoint_surfaces_corrupt_run_not_500(client, make_run, runs_root):
    make_run("good-run")
    corrupt = runs_root / "corrupt-run"
    corrupt.mkdir()
    (corrupt / st.STATE_FILENAME).write_text("{ not json", encoding="utf-8")
    # A parseable-but-malformed state (valid JSON, missing 'stage'/'plan') must
    # also surface as an error item, not blow up the whole list.
    malformed = runs_root / "malformed-run"
    malformed.mkdir()
    (malformed / st.STATE_FILENAME).write_text('{"schema_version": 1}', encoding="utf-8")
    r = client.get("/runs")
    assert r.status_code == 200  # never a 500 — the list must always render
    body = r.json()
    assert {i["run_id"] for i in body} == {"good-run", "corrupt-run", "malformed-run"}
    errors = {i["run_id"]: i for i in body if i["stage"] is None}
    assert set(errors) == {"corrupt-run", "malformed-run"}
    assert all("error" in i for i in errors.values())


def test_get_run_unknown_404(client):
    assert client.get("/runs/does-not-exist").status_code == 404


def test_get_run_traversal_404(client):
    assert client.get("/runs/..%2f..%2fetc").status_code == 404


def test_get_run_corrupt_state_422(client, runs_root):
    run_dir = runs_root / "corrupt"
    run_dir.mkdir(parents=True)
    (run_dir / "run_state.json").write_text("{ not json", encoding="utf-8")
    r = client.get("/runs/corrupt")
    assert r.status_code == 422
    assert "run_state.json" in r.json()["detail"]
