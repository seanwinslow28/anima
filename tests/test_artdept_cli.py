from pipeline.artdept.cli import main


def test_missing_dir_is_usage_error(tmp_path, capsys):
    assert main(["validate", str(tmp_path / "nope")]) == 2
    assert "not a directory" in capsys.readouterr().out


def test_invalid_dir_exits_1(tmp_path, capsys):
    d = tmp_path / "empty"
    d.mkdir()
    assert main(["validate", str(d)]) == 1
    assert "FAIL:" in capsys.readouterr().out


def test_valid_dir_exits_0(tmp_path, capsys, monkeypatch):
    import pipeline.artdept.cli as cli
    monkeypatch.setattr(cli, "validate_artdept_dir", lambda d: [])
    monkeypatch.setattr(cli, "register_warnings", lambda d: ["w1"])
    d = tmp_path / "ok"
    d.mkdir()
    assert main(["validate", str(d)]) == 0
    out = capsys.readouterr().out
    assert "WARN: w1" in out and "ok:" in out
