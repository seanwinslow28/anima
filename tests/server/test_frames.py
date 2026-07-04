from pipeline.orchestration import state as st


def test_candidates_lists_attempts_as_recorded(client, make_generate_run):
    make_generate_run("gen-run")
    r = client.get("/runs/gen-run/frames/1/candidates")
    assert r.status_code == 200
    body = r.json()
    assert [a["attempt"] for a in body] == [1, 2]
    first, second = body
    assert first["image_url"] == "/runs/gen-run/frames/1/image?attempt=1"
    assert second["image_url"] == "/runs/gen-run/frames/1/image?attempt=2"
    # per-attempt status: the approved_attempt is "approved", the rest "generated"
    assert first["status"] == "generated"
    assert second["status"] == "approved"
    # the verdicts ride through AS RECORDED — the eye gate reads Em's reasoning
    # + proposed fixes from here
    assert first["t1"] == {"verdict": "needs_vision_review", "fail_codes": []}
    assert first["em"][0]["verdict"] == "flag"
    assert first["em"][0]["reasoning"] == "line weight drifts on the arm"
    assert second["em"][0]["verdict"] == "pass"
    assert second["note"] == "hold the line weight from the anchor"


def test_candidates_errored_attempt_has_no_image_url(client, make_generate_run):
    run_dir, s = make_generate_run("gen-run")
    s["frames"]["1"]["attempts"].append(
        {"index": 3, "candidate": None, "note": None, "t1": None, "em": [],
         "errored": "RuntimeError: transport fell over", "ts": "2026-07-04T00:10:00+00:00"}
    )
    st.save_state(run_dir, s)
    body = client.get("/runs/gen-run/frames/1/candidates").json()
    assert body[2]["attempt"] == 3
    assert body[2]["image_url"] is None
    assert body[2]["status"] == "errored"
    assert body[2]["errored"] == "RuntimeError: transport fell over"


def test_candidates_unknown_frame_404(client, make_generate_run):
    make_generate_run("gen-run")
    assert client.get("/runs/gen-run/frames/9/candidates").status_code == 404


def test_candidates_unknown_run_404(client):
    assert client.get("/runs/nope/frames/1/candidates").status_code == 404


def test_candidates_corrupt_state_422(client, runs_root):
    run_dir = runs_root / "corrupt"
    run_dir.mkdir(parents=True)
    (run_dir / "run_state.json").write_text("{ not json", encoding="utf-8")
    assert client.get("/runs/corrupt/frames/1/candidates").status_code == 422
