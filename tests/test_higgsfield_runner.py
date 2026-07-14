"""Unit suite for the Higgsfield image transport (decision D5, plan T1).

Every test is credential-free AND network-free: the real path is reached only
through the _run_cli seam, which tests monkeypatch. Sean's machine has an
authenticated `higgsfield` binary on PATH, so an unmocked real call would
SPEND CREDITS — never let one escape this file.
"""
from __future__ import annotations

import fcntl
import json
import multiprocessing
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


def _hold_cache_lock(lock_path: str, held, release) -> None:
    """Child-process probe for the real interprocess lock contract."""
    with hr._cache_key_lock(Path(lock_path)):
        held.set()
        release.wait(5)


def test_transport_map_carries_gpt_image():
    assert HIGGSFIELD_IMAGE_MODELS == {GPT_IMAGE: "gpt_image_2"}


def test_invoke_image_edit_dispatches_gpt_image_to_higgsfield(
    tmp_path, monkeypatch
):
    """D4: the register's honest gpt-image-2 record now routes through the
    Higgsfield transport instead of raising UnwiredTransportError. Cy's and
    Flo's call sites reach this without modification."""
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    from pipeline.agents.nb_pro_runner import invoke_image_edit

    resp = invoke_image_edit(
        prompt="primal plate",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
        model=GPT_IMAGE,
    )
    assert resp.ok and resp.stub_fallback
    assert isinstance(resp, HiggsfieldResponse)


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
    def fail_cli(*_):
        raise AssertionError("test reached unmocked Higgsfield CLI")

    def fail_download(*_):
        raise AssertionError("test reached unmocked Higgsfield download")

    monkeypatch.delenv("ANIMA_FORCE_STUB", raising=False)
    monkeypatch.setattr(hr.shutil, "which", lambda _: "/fake/bin/higgsfield")
    monkeypatch.setattr(hr, "_run_cli", fail_cli)
    monkeypatch.setattr(hr, "_download", fail_download)


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
            return _sp.CompletedProcess(cmd, 1, stdout="", stderr="HTTP 598")
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
            return _sp.CompletedProcess(cmd, 1, stdout="", stderr="HTTP 599")
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


@pytest.mark.parametrize(
    ("returncode", "message", "expected"),
    [
        (1, "HTTP 500", True),
        (1, "HTTP 599", True),
        (1, "HTTP 400", False),
        (1, "HTTP 600", False),
        (1, "request timeout", True),
        (1, "temporarily unavailable", True),
        (0, "HTTP 599", False),
    ],
)
def test_transient_classifier_covers_all_5xx_and_retry_signals(
    returncode, message, expected
):
    result = _sp.CompletedProcess(
        ["higgsfield"], returncode, stdout="", stderr=message
    )
    assert hr._is_transient_failure(result) is expected


def test_failed_create_with_job_id_resumes_before_transient_classification(
    tmp_path, monkeypatch
):
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
                cmd,
                1,
                stdout=json.dumps({"id": "existing-hard-failure"}),
                stderr="unexpected provider response",
            )
        calls["wait"] += 1
        return _sp.CompletedProcess(
            cmd,
            0,
            stdout=json.dumps({
                "id": "existing-hard-failure",
                "result_url": "https://cdn.example/resumed.png",
            }),
            stderr="",
        )

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(hr, "_download", lambda u, d, t: Path(d).write_bytes(b"png"))
    resp = invoke_higgsfield_image_edit(
        prompt="p", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )
    assert resp.ok
    assert calls == {"create": 1, "wait": 1}


def test_resume_accumulates_create_metadata_when_wait_returns_bare_url(
    tmp_path, monkeypatch
):
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
                cmd,
                1,
                stdout=json.dumps({
                    "id": "existing-bare-url",
                    "display_name": "GPT Image 2",
                }),
                stderr="HTTP 502",
            )
        calls["wait"] += 1
        return _sp.CompletedProcess(
            cmd, 0, stdout="https://cdn.example/bare-result.png\n", stderr=""
        )

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(hr, "_download", lambda u, d, t: Path(d).write_bytes(b"png"))
    resp = invoke_higgsfield_image_edit(
        prompt="p", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )
    assert resp.ok
    assert calls == {"create": 1, "wait": 1}
    assert resp.job_id == "existing-bare-url"
    assert resp.result_url == "https://cdn.example/bare-result.png"
    assert resp.display_name == "GPT Image 2"
    sidecar = tmp_path / "c" / f"{resp.cache_key}.provenance.json"
    provenance = json.loads(sidecar.read_text())
    assert provenance["job_id"] == resp.job_id
    assert provenance["result_url"] == resp.result_url
    assert provenance["display_name"] == resp.display_name


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


@pytest.mark.parametrize(
    "sidecar_text",
    [None, "not-json", "{}"],
    ids=["missing", "malformed", "incomplete"],
)
def test_cache_requires_valid_provenance(tmp_path, monkeypatch, sidecar_text):
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    ref = _mk_ref(tmp_path)
    kwargs = dict(
        prompt="p", reference_images=[ref],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )
    probe = invoke_higgsfield_image_edit(**kwargs)
    cached = tmp_path / "c" / f"{probe.cache_key}.png"
    sidecar = tmp_path / "c" / f"{probe.cache_key}.provenance.json"
    cached.write_bytes(b"untrusted-cache-bytes")
    if sidecar_text is not None:
        sidecar.write_text(sidecar_text)

    monkeypatch.delenv("ANIMA_FORCE_STUB")
    monkeypatch.setattr(hr.shutil, "which", lambda _: None)
    try:
        resp = invoke_higgsfield_image_edit(**kwargs)
    except (json.JSONDecodeError, OSError) as exc:
        pytest.fail(f"invalid provenance must be a cache miss, not an error: {exc}")

    assert not resp.cache_hit
    assert resp.stub_fallback
    assert not cached.exists()


def test_cache_publishes_valid_provenance_before_image(tmp_path, monkeypatch):
    _no_stub(monkeypatch)
    monkeypatch.setattr(
        hr,
        "_run_cli",
        _fake_cli(json.dumps({
            "id": "job-atomic",
            "result_url": "https://cdn.example/atomic.png",
            "display_name": "GPT Image 2",
        })),
    )
    monkeypatch.setattr(hr, "_download", lambda u, d, t: Path(d).write_bytes(b"png"))
    real_replace = hr.os.replace
    real_fsync = hr.os.fsync
    real_durable_unlink = hr._durable_unlink
    publications = []
    fsyncs = []
    removals = []

    def observe_replace(src, dst):
        src_path, dst_path = Path(src), Path(dst)
        if dst_path.suffix == ".png":
            sidecar = dst_path.with_suffix(".provenance.json")
            provenance = json.loads(sidecar.read_text())
            assert provenance["job_id"] == "job-atomic"
            assert dst_path.with_suffix(".pending.json").exists()
        publications.append((src_path, dst_path))
        real_replace(src, dst)

    def observe_fsync(fd):
        fsyncs.append(fd)
        real_fsync(fd)

    def observe_durable_unlink(path):
        removals.append((Path(path).name, len(publications), len(fsyncs)))
        real_durable_unlink(path)

    monkeypatch.setattr(hr.os, "replace", observe_replace)
    monkeypatch.setattr(hr.os, "fsync", observe_fsync)
    monkeypatch.setattr(hr, "_durable_unlink", observe_durable_unlink)
    resp = invoke_higgsfield_image_edit(
        prompt="p", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )

    assert resp.ok
    assert [dest.name for _, dest in publications] == [
        f"{resp.cache_key}.create_in_flight.json",
        f"{resp.cache_key}.pending.json",
        f"{resp.cache_key}.provenance.json",
        f"{resp.cache_key}.png",
    ]
    assert all(source != dest for source, dest in publications)
    assert not (tmp_path / "c" / f"{resp.cache_key}.pending.json").exists()
    assert not (
        tmp_path / "c" / f"{resp.cache_key}.create_in_flight.json"
    ).exists()
    assert [name for name, _, _ in removals] == [
        f"{resp.cache_key}.create_in_flight.json",
        f"{resp.cache_key}.pending.json",
    ]
    assert removals[0][1:] == (2, 4)  # after durable pending publication
    assert removals[1][1:] == (4, 8)  # after durable cache-pair publication
    # Four staged files + five parent-directory transitions.
    assert len(fsyncs) == 9


def test_cache_directory_fsync_failure_retains_pending_receipt(
    tmp_path, monkeypatch
):
    """Visible cache renames cannot supersede the pending receipt until the
    cache directory fsync confirms the pair durably."""
    _no_stub(monkeypatch)
    calls = {"create": 0, "directory_fsync": 0}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        calls["create"] += 1
        return _sp.CompletedProcess(
            cmd,
            0,
            stdout=json.dumps({
                "id": "job-cache-not-durable",
                "result_url": "https://cdn.example/cache-not-durable.png",
                "display_name": "GPT Image 2",
            }),
            stderr="",
        )

    real_fsync_directory = hr._fsync_directory

    def fail_cache_directory_fsync(path):
        calls["directory_fsync"] += 1
        if calls["directory_fsync"] == 4:
            raise OSError("cache directory fsync failed")
        real_fsync_directory(path)

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(
        hr, "_download", lambda _url, dest, _timeout: Path(dest).write_bytes(b"png")
    )
    monkeypatch.setattr(hr, "_fsync_directory", fail_cache_directory_fsync)
    resp = invoke_higgsfield_image_edit(
        prompt="cache durability fault",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )

    pending = tmp_path / "c" / f"{resp.cache_key}.pending.json"
    assert not resp.ok and resp.exit_code == 1
    assert resp.job_id == "job-cache-not-durable"
    assert pending.exists()
    assert calls == {"create": 1, "directory_fsync": 4}


def test_intent_unlink_fsync_failure_returns_non_ok_with_durable_pending(
    tmp_path, monkeypatch
):
    """A durable pending receipt makes the transition safe, but the caller
    cannot receive success when intent removal durability is unconfirmed."""
    _no_stub(monkeypatch)
    calls = {"create": 0, "download": 0, "directory_fsync": 0}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        calls["create"] += 1
        return _sp.CompletedProcess(
            cmd, 0, stdout=json.dumps({
                "id": "job-intent-unlink-fsync",
                "result_url": "https://cdn.example/intent-unlink.png",
                "display_name": "GPT Image 2",
            }), stderr="",
        )

    real_fsync_directory = hr._fsync_directory

    def fail_intent_unlink_fsync(path):
        calls["directory_fsync"] += 1
        if calls["directory_fsync"] == 3:
            raise OSError("intent unlink fsync failed")
        real_fsync_directory(path)

    def fail_download(*_args):
        calls["download"] += 1
        raise AssertionError("cache work must wait for intent transition")

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(hr, "_download", fail_download)
    monkeypatch.setattr(hr, "_fsync_directory", fail_intent_unlink_fsync)
    resp = invoke_higgsfield_image_edit(
        prompt="intent unlink durability",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )

    pending = tmp_path / "c" / f"{resp.cache_key}.pending.json"
    assert not resp.ok and resp.exit_code == 78
    assert resp.error and "intent removal" in resp.error
    assert pending.exists()
    assert calls == {"create": 1, "download": 0, "directory_fsync": 3}


def test_pending_unlink_fsync_failure_cannot_report_success(tmp_path, monkeypatch):
    """The durable cache pair is safe, but success waits for durable pending
    removal rather than treating a visible unlink as confirmation."""
    _no_stub(monkeypatch)
    calls = {"create": 0, "directory_fsync": 0}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        calls["create"] += 1
        return _sp.CompletedProcess(
            cmd, 0, stdout=json.dumps({
                "id": "job-pending-unlink-fsync",
                "result_url": "https://cdn.example/pending-unlink.png",
                "display_name": "GPT Image 2",
            }), stderr="",
        )

    real_fsync_directory = hr._fsync_directory

    def fail_pending_unlink_fsync(path):
        calls["directory_fsync"] += 1
        if calls["directory_fsync"] == 5:
            raise OSError("pending unlink fsync failed")
        real_fsync_directory(path)

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(
        hr, "_download", lambda _url, dest, _timeout: Path(dest).write_bytes(b"png")
    )
    monkeypatch.setattr(hr, "_fsync_directory", fail_pending_unlink_fsync)
    resp = invoke_higgsfield_image_edit(
        prompt="pending unlink durability",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )

    cached = tmp_path / "c" / f"{resp.cache_key}.png"
    sidecar = tmp_path / "c" / f"{resp.cache_key}.provenance.json"
    assert not resp.ok and resp.exit_code == 78
    assert resp.error and "pending-receipt removal" in resp.error
    assert cached.exists() and sidecar.exists()
    assert calls == {"create": 1, "directory_fsync": 5}


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


def test_completed_job_download_failure_resumes_without_duplicate_create(
    tmp_path, monkeypatch
):
    """A completed charged job survives a terminal download failure and the
    identical retry re-downloads that same receipt before any new create."""
    _no_stub(monkeypatch)
    calls = {"create": 0, "download": 0}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        assert cmd[1:3] == ["generate", "create"]
        calls["create"] += 1
        return _sp.CompletedProcess(
            cmd,
            0,
            stdout=json.dumps({
                "id": "job-download-retry",
                "result_url": "https://cdn.example/retry.png",
                "display_name": "GPT Image 2",
            }),
            stderr="",
        )

    def flaky_download(url, dest, timeout_s):
        calls["download"] += 1
        receipts = list((tmp_path / "c").glob("*.pending.json"))
        assert len(receipts) == 1
        receipt = json.loads(receipts[0].read_text())
        assert receipt["job_id"] == "job-download-retry"
        assert receipt["result_url"] == url
        if calls["download"] <= hr._MAX_ATTEMPTS:
            raise TimeoutError("cdn timed out")
        Path(dest).write_bytes(b"recovered-png")

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(hr, "_download", flaky_download)
    monkeypatch.setattr(hr.time, "sleep", lambda _: None)
    kwargs = dict(
        prompt="same charged plate",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )

    first = invoke_higgsfield_image_edit(**kwargs)
    assert not first.ok and first.exit_code != 0
    assert first.job_id == "job-download-retry"
    assert first.result_url == "https://cdn.example/retry.png"
    assert first.display_name == "GPT Image 2"
    assert first.cli_version == "0.2.3"
    pending = tmp_path / "c" / f"{first.cache_key}.pending.json"
    assert pending.exists()

    second = invoke_higgsfield_image_edit(**kwargs)
    assert second.ok and not second.cache_hit
    assert second.job_id == first.job_id
    assert calls == {"create": 1, "download": hr._MAX_ATTEMPTS + 1}
    assert not pending.exists()


def test_resume_timeout_returns_known_job_identity(tmp_path, monkeypatch):
    """TimeoutExpired while waiting on a known job is bounded and honest."""
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
                cmd,
                1,
                stdout=json.dumps({
                    "id": "job-wait-timeout",
                    "display_name": "GPT Image 2",
                }),
                stderr="HTTP 502",
            )
        calls["wait"] += 1
        raise _sp.TimeoutExpired(cmd, timeout_s)

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(hr.time, "sleep", lambda _: None)
    resp = invoke_higgsfield_image_edit(
        prompt="p",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )

    assert not resp.ok and resp.exit_code == 124
    assert resp.job_id == "job-wait-timeout"
    assert resp.display_name == "GPT Image 2"
    assert resp.cli_version == "0.2.3"
    assert calls == {"create": 1, "wait": hr._MAX_ATTEMPTS}


def test_cache_key_lock_is_exclusive_across_processes(tmp_path):
    """The same cache key cannot be held by two OS processes at once."""
    ctx = multiprocessing.get_context("spawn")
    held = ctx.Event()
    release = ctx.Event()
    lock_path = tmp_path / "same-key.lock"
    process = ctx.Process(
        target=_hold_cache_lock,
        args=(str(lock_path), held, release),
    )
    process.start()
    try:
        assert held.wait(5), "child never acquired the cache-key lock"
        with lock_path.open("a+") as contender:
            with pytest.raises(BlockingIOError):
                fcntl.flock(contender.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    finally:
        release.set()
        process.join(5)
        if process.is_alive():
            process.terminate()
            process.join(5)
    assert process.exitcode == 0


def test_create_timeout_receipt_prevents_duplicate_create(tmp_path, monkeypatch):
    """TimeoutExpired may still carry the charged job's JSON envelope; persist
    it and let an identical retry recover that job before any second create."""
    _no_stub(monkeypatch)
    calls = {"create": 0, "download": 0}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        assert cmd[1:3] == ["generate", "create"]
        calls["create"] += 1
        raise _sp.TimeoutExpired(
            cmd,
            timeout_s,
            output=json.dumps({
                "id": "job-create-timeout",
                "display_name": "GPT Image 2",
            }).encode(),
            stderr=json.dumps({
                "result_url": "https://cdn.example/create-timeout.png",
            }).encode(),
        )

    def fake_download(url, dest, timeout_s):
        calls["download"] += 1
        Path(dest).write_bytes(b"recovered-timeout-job")

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(hr, "_download", fake_download)
    kwargs = dict(
        prompt="timeout charged plate",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )

    first = invoke_higgsfield_image_edit(**kwargs)
    assert not first.ok and first.exit_code == 124
    assert first.job_id == "job-create-timeout"
    assert first.result_url == "https://cdn.example/create-timeout.png"
    assert (tmp_path / "c" / f"{first.cache_key}.pending.json").exists()

    second = invoke_higgsfield_image_edit(**kwargs)
    assert second.ok and second.job_id == first.job_id
    assert calls == {"create": 1, "download": 1}


def test_outputless_create_timeout_intent_blocks_duplicate_create(
    tmp_path, monkeypatch
):
    """An ambiguous combined create/wait timeout has no recoverable job ID,
    so its pre-create intent must block every identical automatic retry."""
    _no_stub(monkeypatch)
    calls = {"create": 0}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        assert cmd[1:3] == ["generate", "create"]
        calls["create"] += 1
        raise _sp.TimeoutExpired(cmd, timeout_s)

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    kwargs = dict(
        prompt="ambiguous timeout",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )

    first = invoke_higgsfield_image_edit(**kwargs)
    second = invoke_higgsfield_image_edit(**kwargs)

    intent = tmp_path / "c" / f"{first.cache_key}.create_in_flight.json"
    assert not first.ok and first.exit_code == 124
    assert not second.ok and second.exit_code == 78
    assert second.error and "operator" in second.error.lower()
    assert intent.exists()
    assert calls == {"create": 1}


def test_pre_create_intent_write_failure_prevents_create(tmp_path, monkeypatch):
    """Create is never invoked unless the pre-charge intent is durable."""
    _no_stub(monkeypatch)
    calls = {"create": 0}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        calls["create"] += 1
        raise AssertionError("create ran without a durable intent")

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(
        hr, "_publish_create_intent",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("disk full")),
    )
    resp = invoke_higgsfield_image_edit(
        prompt="intent publication failure",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )

    assert not resp.ok and resp.exit_code == 78
    assert resp.error and "not invoked" in resp.error.lower()
    assert calls == {"create": 0}


def test_pending_write_failure_quarantines_job_and_blocks_recreate(
    tmp_path, monkeypatch
):
    """If the canonical receipt cannot publish after create, retain identity in
    a durable quarantine marker and fail closed on every identical retry."""
    _no_stub(monkeypatch)
    calls = {"create": 0}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        calls["create"] += 1
        return _sp.CompletedProcess(
            cmd,
            0,
            stdout=json.dumps({
                "id": "job-receipt-write-failed",
                "result_url": "https://cdn.example/quarantined.png",
                "display_name": "GPT Image 2",
            }),
            stderr="",
        )

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(
        hr, "_atomic_write_json",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("disk hiccup")),
    )
    kwargs = dict(
        prompt="receipt failure",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )

    first = invoke_higgsfield_image_edit(**kwargs)
    assert not first.ok and first.job_id == "job-receipt-write-failed"
    assert first.error and "quarantine" in first.error.lower()
    quarantine = tmp_path / "c" / f"{first.cache_key}.quarantine.json"
    assert quarantine.exists()
    assert json.loads(quarantine.read_text())["job_id"] == first.job_id

    second = invoke_higgsfield_image_edit(**kwargs)
    assert not second.ok and second.job_id == first.job_id
    assert second.error and "operator" in second.error.lower()
    assert calls == {"create": 1}


def test_pending_and_quarantine_write_failure_retains_create_intent(
    tmp_path, monkeypatch
):
    """If neither post-create receipt can publish, the durable pre-create
    intent remains the last-resort duplicate-spend barrier across retries."""
    _no_stub(monkeypatch)
    calls = {"create": 0}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        calls["create"] += 1
        return _sp.CompletedProcess(
            cmd,
            0,
            stdout=json.dumps({
                "id": "job-unpublished-receipt",
                "result_url": "https://cdn.example/unpublished.png",
                "display_name": "GPT Image 2",
            }),
            stderr="",
        )

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(
        hr, "_atomic_write_json",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("disk full")),
    )
    monkeypatch.setattr(
        hr, "_durable_write_quarantine",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("read only")),
    )
    kwargs = dict(
        prompt="both receipts fail",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )

    first = invoke_higgsfield_image_edit(**kwargs)
    second = invoke_higgsfield_image_edit(**kwargs)

    intent = tmp_path / "c" / f"{first.cache_key}.create_in_flight.json"
    assert not first.ok and first.exit_code == 78
    assert first.job_id == "job-unpublished-receipt"
    assert first.error and "intent" in first.error.lower()
    assert not second.ok and second.exit_code == 78
    assert intent.exists()
    assert calls == {"create": 1}


def test_visible_receipts_without_directory_fsync_retain_create_intent(
    tmp_path, monkeypatch
):
    """Visible pending/quarantine renames are not durable successors when
    their directory fsyncs fail, so they cannot authorize intent removal."""
    _no_stub(monkeypatch)
    calls = {"create": 0, "directory_fsync": 0}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        assert cmd[1:3] == ["generate", "create"]
        calls["create"] += 1
        return _sp.CompletedProcess(
            cmd,
            0,
            stdout=json.dumps({
                "id": "job-visible-not-durable",
                "result_url": "https://cdn.example/not-durable.png",
                "display_name": "GPT Image 2",
            }),
            stderr="",
        )

    real_fsync_directory = hr._fsync_directory

    def fail_receipt_directory_fsync(path):
        calls["directory_fsync"] += 1
        if calls["directory_fsync"] in {2, 3}:
            raise OSError("directory fsync failed")
        real_fsync_directory(path)

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(hr, "_fsync_directory", fail_receipt_directory_fsync)
    kwargs = dict(
        prompt="visible is not durable",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )

    first = invoke_higgsfield_image_edit(**kwargs)
    second = invoke_higgsfield_image_edit(**kwargs)

    intent = tmp_path / "c" / f"{first.cache_key}.create_in_flight.json"
    pending = tmp_path / "c" / f"{first.cache_key}.pending.json"
    quarantine = tmp_path / "c" / f"{first.cache_key}.quarantine.json"
    assert not first.ok and first.exit_code == 78
    assert first.job_id == "job-visible-not-durable"
    assert not second.ok and second.exit_code == 78
    assert pending.exists() and quarantine.exists()
    assert intent.exists()
    assert calls["create"] == 1


@pytest.mark.parametrize("receipt_kind", ["malformed", "stale-version"])
def test_invalid_pending_receipt_is_preserved_and_blocks_create(
    tmp_path, monkeypatch, receipt_kind
):
    """An existing unreadable or version-stale receipt is evidence of a
    possible charged job, never permission to unlink it and create again."""
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    kwargs = dict(
        prompt=f"invalid receipt {receipt_kind}",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )
    probe = invoke_higgsfield_image_edit(**kwargs)
    pending = tmp_path / "c" / f"{probe.cache_key}.pending.json"
    if receipt_kind == "malformed":
        original = "not-json"
    else:
        original = json.dumps({
            "cache_key": probe.cache_key,
            "transport": "higgsfield",
            "vendor_model": GPT_IMAGE,
            "job_type": "gpt_image_2",
            "quality": "high",
            "resolution": "1k",
            "aspect_ratio": None,
            "job_id": "job-stale-version",
            "result_url": "https://cdn.example/stale.png",
            "display_name": "GPT Image 2",
            "cli_version": "0.2.2",
        })
    pending.write_text(original)

    _no_stub(monkeypatch)
    calls = {"create": 0}

    def fake_run(cmd, timeout_s):
        if cmd == ["higgsfield", "--version"]:
            return _sp.CompletedProcess(
                cmd, 0, stdout="higgsfield 0.2.3 (test) built test\n", stderr=""
            )
        calls["create"] += 1
        return _sp.CompletedProcess(cmd, 1, stdout="", stderr="blocked")

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    resp = invoke_higgsfield_image_edit(**kwargs)

    assert not resp.ok and resp.exit_code == 78
    assert resp.error and "operator" in resp.error.lower()
    assert pending.read_text() == original
    assert calls == {"create": 0}


def test_expired_pending_url_refreshes_same_job_before_download_retry(
    tmp_path, monkeypatch
):
    """A stale retained URL with a valid job ID is refreshed by waiting on the
    same job; it never creates, and the replacement URL is persisted."""
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    kwargs = dict(
        prompt="expired result url",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )
    probe = invoke_higgsfield_image_edit(**kwargs)
    pending = tmp_path / "c" / f"{probe.cache_key}.pending.json"
    pending.write_text(json.dumps({
        "cache_key": probe.cache_key,
        "transport": "higgsfield",
        "vendor_model": GPT_IMAGE,
        "job_type": "gpt_image_2",
        "quality": "high",
        "resolution": "1k",
        "aspect_ratio": None,
        "job_id": "job-expired-url",
        "result_url": "https://cdn.example/expired.png",
        "display_name": "GPT Image 2",
        "cli_version": "0.2.3",
    }))

    _no_stub(monkeypatch)
    calls = {"create": 0, "wait": 0, "old_download": 0, "new_download": 0}

    def fake_run(cmd, timeout_s):
        if cmd[1:3] == ["generate", "create"]:
            calls["create"] += 1
            raise AssertionError("a pending job must never be recreated")
        assert cmd[1:3] == ["generate", "wait"]
        calls["wait"] += 1
        return _sp.CompletedProcess(
            cmd,
            0,
            stdout=json.dumps({
                "id": "job-expired-url",
                "result_url": "https://cdn.example/refreshed.png",
                "display_name": "GPT Image 2",
            }),
            stderr="",
        )

    def fake_download(url, dest, timeout_s):
        if url.endswith("expired.png"):
            calls["old_download"] += 1
            raise OSError("HTTP 403 expired")
        calls["new_download"] += 1
        Path(dest).write_bytes(b"refreshed-result")

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(hr, "_download", fake_download)
    monkeypatch.setattr(hr.time, "sleep", lambda _: None)
    resp = invoke_higgsfield_image_edit(**kwargs)

    assert resp.ok and resp.job_id == "job-expired-url"
    assert resp.result_url == "https://cdn.example/refreshed.png"
    assert calls == {
        "create": 0,
        "wait": 1,
        "old_download": hr._MAX_ATTEMPTS,
        "new_download": 1,
    }
    provenance = json.loads(
        (tmp_path / "c" / f"{resp.cache_key}.provenance.json").read_text()
    )
    assert provenance["result_url"] == resp.result_url


def test_wait_job_id_mismatch_preserves_original_receipt_and_fails_closed(
    tmp_path, monkeypatch
):
    """A wait response for another job can never overwrite, download, or
    publish against the requested charged-job receipt."""
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    kwargs = dict(
        prompt="wait identity mismatch",
        reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png",
        cache_dir=tmp_path / "c",
    )
    probe = invoke_higgsfield_image_edit(**kwargs)
    pending = tmp_path / "c" / f"{probe.cache_key}.pending.json"
    original = json.dumps({
        "cache_key": probe.cache_key,
        "transport": "higgsfield",
        "vendor_model": GPT_IMAGE,
        "job_type": "gpt_image_2",
        "quality": "high",
        "resolution": "1k",
        "aspect_ratio": None,
        "job_id": "job-original",
        "result_url": None,
        "display_name": "GPT Image 2",
        "cli_version": "0.2.3",
    })
    pending.write_text(original)

    _no_stub(monkeypatch)
    calls = {"create": 0, "wait": 0, "download": 0}

    def fake_run(cmd, timeout_s):
        if cmd[1:3] == ["generate", "create"]:
            calls["create"] += 1
            raise AssertionError("recovery must not create")
        assert cmd[1:3] == ["generate", "wait"]
        calls["wait"] += 1
        return _sp.CompletedProcess(
            cmd,
            0,
            stdout=json.dumps({
                "id": "job-other",
                "result_url": "https://cdn.example/wrong-job.png",
                "display_name": "GPT Image 2",
            }),
            stderr="",
        )

    def fail_download(*_args):
        calls["download"] += 1
        raise AssertionError("mismatched job output must not download")

    monkeypatch.setattr(hr, "_run_cli", fake_run)
    monkeypatch.setattr(hr, "_download", fail_download)
    resp = invoke_higgsfield_image_edit(**kwargs)

    assert not resp.ok and resp.exit_code == 78
    assert resp.job_id == "job-original"
    assert resp.error and "job ID mismatch" in resp.error
    assert pending.read_text() == original
    assert not list((tmp_path / "c").glob("*.png"))
    assert calls == {"create": 0, "wait": 1, "download": 0}
