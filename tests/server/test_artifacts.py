from pipeline.orchestration import state as st


def test_artifact_plan_happy_path(client, make_generate_run):
    make_generate_run("gen-run")
    r = client.get("/runs/gen-run/artifacts/plan")
    assert r.status_code == 200
    assert "# The Plan" in r.text
    assert r.headers["content-type"].startswith("text/markdown")


def test_artifact_every_kind_serves_its_canonical_file(client, make_generate_run):
    make_generate_run("gen-run")
    expected = {
        "plan": ("# The Plan", "text/markdown"),
        "brief": ("# Studio Brief", "text/markdown"),
        "script": ("# Script", "text/markdown"),
        "beats": ('"beats"', "application/json"),
        "storyboard": ("# Storyboard", "text/markdown"),
        "shots": ("frames:", "text/plain"),
    }
    for kind, (marker, media) in expected.items():
        r = client.get(f"/runs/gen-run/artifacts/{kind}")
        assert r.status_code == 200, f"{kind}: {r.status_code}"
        assert marker in r.text, kind
        assert r.headers["content-type"].startswith(media), kind


def test_artifact_prefers_path_recorded_in_state(client, make_generate_run):
    # plan_path in state names a differently-named file; it must win over the
    # canonical brief_dir/plan.md.
    run_dir, s = make_generate_run("gen-run")
    (run_dir / "brief" / "plan-final.md").write_text("# Final Plan\n", encoding="utf-8")
    s["plan"]["plan_path"] = "runs/gen-run/brief/plan-final.md"
    st.save_state(run_dir, s)
    r = client.get("/runs/gen-run/artifacts/plan")
    assert r.status_code == 200
    assert "# Final Plan" in r.text


def test_artifact_missing_file_404_not_500(client, make_run):
    # A back-compat run legitimately has no script/beats — the default make_run
    # has no brief files on disk at all.
    make_run("bare-run")
    for kind in ["plan", "brief", "script", "beats", "storyboard", "shots"]:
        assert client.get(f"/runs/bare-run/artifacts/{kind}").status_code == 404, kind


def test_artifact_recorded_path_pointing_at_missing_file_404(client, make_generate_run):
    run_dir, s = make_generate_run("gen-run")
    (run_dir / "brief" / "plan.md").unlink()  # plan_path still recorded in state
    r = client.get("/runs/gen-run/artifacts/plan")
    assert r.status_code == 404


def test_artifact_unknown_run_404(client):
    assert client.get("/runs/does-not-exist/artifacts/plan").status_code == 404


def test_artifact_kind_outside_allowed_set_404(client, make_generate_run):
    make_generate_run("gen-run")
    for bad in ["secrets", "run_state.json", "PLAN", "plan.md", "..%2fplan"]:
        r = client.get(f"/runs/gen-run/artifacts/{bad}")
        assert r.status_code == 404, bad


def test_artifact_corrupt_state_422(client, runs_root):
    run_dir = runs_root / "corrupt"
    run_dir.mkdir(parents=True)
    (run_dir / "run_state.json").write_text("{ not json", encoding="utf-8")
    r = client.get("/runs/corrupt/artifacts/plan")
    assert r.status_code == 422
    assert "run_state.json" in r.json()["detail"]
