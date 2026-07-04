from pipeline.orchestration import state as st


def test_get_run_returns_full_state(client, make_run):
    run_dir, _ = make_run("2026-07-04-full-state")
    r = client.get("/runs/2026-07-04-full-state")
    assert r.status_code == 200
    body = r.json()
    assert "stage" in body and "plan" in body and "frames" in body
    # Raw passthrough: the response IS the state on disk, no projection.
    assert body == st.load_state(run_dir)


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
