"""Unit suite for the Higgsfield image transport (decision D5, plan T1).

Every test is credential-free AND network-free: the real path is reached only
through the _run_cli seam, which tests monkeypatch. Sean's machine has an
authenticated `higgsfield` binary on PATH, so an unmocked real call would
SPEND CREDITS — never let one escape this file.
"""
from __future__ import annotations

import json
import subprocess as _sp
from pathlib import Path

import pytest

from pipeline.agents import higgsfield_runner as hr
from pipeline.agents.higgsfield_runner import (
    HIGGSFIELD_IMAGE_MODELS,
    HiggsfieldResponse,
    invoke_higgsfield_image_edit,
)
from pipeline.agents.nb_pro_runner import UnwiredTransportError
from pipeline.registers import GPT_IMAGE


def _mk_ref(tmp_path: Path, name: str = "ref.png") -> Path:
    p = tmp_path / name
    p.write_bytes(b"\x89PNG\r\n\x1a\nfakebytes")
    return p


def test_transport_map_carries_gpt_image():
    assert HIGGSFIELD_IMAGE_MODELS == {GPT_IMAGE: "gpt_image_2"}


def test_unmapped_model_raises_unwired(tmp_path):
    with pytest.raises(UnwiredTransportError):
        invoke_higgsfield_image_edit(
            prompt="x", reference_images=[], output_path=tmp_path / "o.png",
            cache_dir=tmp_path / "c", model="not-a-model",
        )


def test_force_stub_writes_placeholder(tmp_path, monkeypatch):
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    resp = invoke_higgsfield_image_edit(
        prompt="plate", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "out" / "o.png", cache_dir=tmp_path / "c",
    )
    assert resp.ok and resp.stub_fallback and not resp.cache_hit
    assert resp.output_path.exists()


def test_missing_cli_stubs(tmp_path, monkeypatch):
    monkeypatch.delenv("ANIMA_FORCE_STUB", raising=False)
    monkeypatch.setattr(
        "pipeline.agents.higgsfield_runner.shutil.which", lambda _: None
    )
    resp = invoke_higgsfield_image_edit(
        prompt="plate", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )
    assert resp.ok and resp.stub_fallback


def test_stub_never_populates_real_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    kwargs = dict(
        prompt="plate", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )
    first = invoke_higgsfield_image_edit(**kwargs)
    second = invoke_higgsfield_image_edit(**kwargs)
    assert not first.cache_hit and not second.cache_hit
    assert first.stub_fallback and second.stub_fallback
    assert first.cache_key == second.cache_key
    assert not list((tmp_path / "c").glob("*.png"))


def test_cache_key_varies_on_explicit_params(tmp_path, monkeypatch):
    """D5: resolution/quality/aspect/reject/model are all part of the key."""
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    base = dict(
        prompt="plate", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )
    k0 = invoke_higgsfield_image_edit(**base).cache_key
    assert invoke_higgsfield_image_edit(**base, quality="medium").cache_key != k0
    assert invoke_higgsfield_image_edit(**base, resolution="2k").cache_key != k0
    assert invoke_higgsfield_image_edit(**base, aspect_ratio="16:9").cache_key != k0
    assert invoke_higgsfield_image_edit(**base, reject_reason="fix jaw").cache_key != k0


def test_cache_key_preserves_anchor_first_reference_order(tmp_path, monkeypatch):
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    anchor = _mk_ref(tmp_path, "anchor.png")
    pose = _mk_ref(tmp_path, "pose.png")
    pose.write_bytes(b"different")
    base = dict(prompt="plate", output_path=tmp_path / "o.png", cache_dir=tmp_path / "c")
    k_anchor_first = invoke_higgsfield_image_edit(
        **base, reference_images=[anchor, pose]
    ).cache_key
    k_pose_first = invoke_higgsfield_image_edit(
        **base, reference_images=[pose, anchor]
    ).cache_key
    assert k_anchor_first != k_pose_first


def _fake_cli(stdout: str, returncode: int = 0, stderr: str = ""):
    def fake(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        return _sp.CompletedProcess(cmd, returncode, stdout=stdout, stderr=stderr)
    return fake


def _no_stub(monkeypatch):
    monkeypatch.delenv("ANIMA_FORCE_STUB", raising=False)
    monkeypatch.setattr(hr.shutil, "which", lambda _: "/fake/bin/higgsfield")


def test_real_path_builds_argv_and_downloads(tmp_path, monkeypatch):
    _no_stub(monkeypatch)
    seen = {}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        seen["cmd"] = cmd
        return _sp.CompletedProcess(
            cmd, 0, stdout=json.dumps({
                "id": "job-123",
                "result_url": "https://cdn.example/hf_result.png",
                "display_name": "GPT Image 2",
            }), stderr="")

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(
        hr, "_download", lambda url, dest, timeout_s: Path(dest).write_bytes(b"png"))
    ref = _mk_ref(tmp_path)
    resp = invoke_higgsfield_image_edit(
        prompt="plate", reference_images=[ref],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
        quality="medium", resolution="1k", aspect_ratio="16:9",
    )
    assert resp.ok and not resp.stub_fallback
    assert resp.result_url == "https://cdn.example/hf_result.png"
    assert resp.job_id == "job-123"
    assert resp.display_name == "GPT Image 2"
    assert resp.cli_version == "0.2.3"
    cmd = seen["cmd"]
    assert cmd[:4] == ["higgsfield", "generate", "create", "gpt_image_2"]
    # D5: explicit params, never surface defaults.
    for flag, val in (("--quality", "medium"), ("--resolution", "1k"),
                      ("--aspect_ratio", "16:9")):
        assert val == cmd[cmd.index(flag) + 1]
    assert cmd[cmd.index("--image") + 1] == str(ref)
    assert "--wait" in cmd
    assert "--json" in cmd
    # Provenance sidecar written next to the cache entry.
    sidecar = tmp_path / "c" / f"{resp.cache_key}.provenance.json"
    provenance = json.loads(sidecar.read_text())
    assert provenance["result_url"] == resp.result_url
    assert provenance["job_id"] == "job-123"
    assert provenance["display_name"] == "GPT Image 2"
    assert provenance["cli_version"] == "0.2.3"
    assert provenance["vendor_model"] == GPT_IMAGE


def test_transient_failure_retries_then_succeeds(tmp_path, monkeypatch):
    _no_stub(monkeypatch)
    calls = {"n": 0}

    def flaky(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        calls["n"] += 1
        if calls["n"] == 1:
            return _sp.CompletedProcess(cmd, 1, stdout="", stderr="HTTP 502")
        return _sp.CompletedProcess(cmd, 0, stdout=json.dumps({
            "id": "job-2", "result_url": "https://cdn.example/r.png",
            "display_name": "GPT Image 2",
        }), stderr="")

    monkeypatch.setattr(hr, "_run_cli", flaky)
    monkeypatch.setattr(hr, "_download", lambda u, d, t: Path(d).write_bytes(b"png"))
    monkeypatch.setattr(hr.time, "sleep", lambda _: None)
    resp = invoke_higgsfield_image_edit(
        prompt="p", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )
    assert resp.ok and calls["n"] == 2


def test_transient_wait_with_job_id_resumes_without_duplicate_create(tmp_path, monkeypatch):
    _no_stub(monkeypatch)
    calls = {"create": 0, "wait": 0}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        if cmd[1:3] == ["generate", "create"]:
            calls["create"] += 1
            return _sp.CompletedProcess(
                cmd, 1, stdout=json.dumps({"id": "existing-job"}), stderr="HTTP 502"
            )
        calls["wait"] += 1
        if calls["wait"] == 1:
            return _sp.CompletedProcess(cmd, 1, stdout="", stderr="HTTP 502")
        return _sp.CompletedProcess(cmd, 0, stdout=json.dumps({
            "id": "existing-job", "result_url": "https://cdn.example/existing.png",
            "display_name": "GPT Image 2",
        }), stderr="")

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(hr, "_download", lambda u, d, t: Path(d).write_bytes(b"png"))
    monkeypatch.setattr(hr.time, "sleep", lambda _: None)
    resp = invoke_higgsfield_image_edit(
        prompt="p", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )
    assert resp.ok
    assert calls == {"create": 1, "wait": 2}


def test_real_cache_hit_rehydrates_provenance_without_cli_call(tmp_path, monkeypatch):
    _no_stub(monkeypatch)
    generation_calls = {"n": 0}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        generation_calls["n"] += 1
        return _sp.CompletedProcess(cmd, 0, stdout=json.dumps({
            "id": "job-cache", "result_url": "https://cdn.example/cache.png",
            "display_name": "GPT Image 2",
        }), stderr="")

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(hr, "_download", lambda u, d, t: Path(d).write_bytes(b"png"))
    kwargs = dict(
        prompt="p", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )
    first = invoke_higgsfield_image_edit(**kwargs)
    second = invoke_higgsfield_image_edit(**kwargs)
    assert first.ok and second.ok and second.cache_hit
    assert second.job_id == "job-cache" and second.display_name == "GPT Image 2"
    assert generation_calls["n"] == 1


def test_unverified_cli_version_fails_before_generation(tmp_path, monkeypatch):
    _no_stub(monkeypatch)
    seen = {"generation": False}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(cmd, 0, stdout="higgsfield 1.1.13\n", stderr="")
        seen["generation"] = True
        raise AssertionError("generation must not run on an unverified CLI")

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    with pytest.raises(hr.UnsupportedHiggsfieldCLIVersion):
        invoke_higgsfield_image_edit(
            prompt="p", reference_images=[_mk_ref(tmp_path)],
            output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
        )
    assert not seen["generation"]


def test_hard_failure_is_errored_not_stub(tmp_path, monkeypatch):
    """Auth/param errors must surface as non-ok — never silent stub."""
    _no_stub(monkeypatch)
    monkeypatch.setattr(
        hr, "_run_cli", _fake_cli("", returncode=1, stderr="not logged in"))
    resp = invoke_higgsfield_image_edit(
        prompt="p", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )
    assert not resp.ok and not resp.stub_fallback and resp.exit_code == 1
