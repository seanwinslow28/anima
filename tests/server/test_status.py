from server.runs import resolve_run_dir


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
