"""Tests for the T3 council pre_museum gate (pipeline.museum.t3_gate).

Stub-green with no credentials. The gate runs the council over assembled
exhibits BEFORE render: a `fail` adjudication (or all-peers-errored) blocks the
publish; patches stage with the right proposed_by; a peer erroring is contained
(never a gate-aborting crash — the Gate-3 lesson).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml

import pipeline.agents.t3_council  # noqa: F401 — trigger @register_node
from pipeline.agents.patch_stager import read_staged_patches
from pipeline.museum.schema import Decision, Exhibit, exhibit_dir, write_exhibit
from pipeline.museum.t3_gate import t3_council_gate


@dataclass
class _FakeResp:
    text: str
    ok: bool = True
    stub_fallback: bool = False
    model: str | None = None
    error: str | None = None


def _verdict_json(*, verdict="pass", confidence=0.9, reasoning="ok", patches=None, cites=None):
    return json.dumps({
        "verdict": verdict, "confidence": confidence, "reasoning": reasoning,
        "proposed_patches": patches or [], "cites_criteria": cites or [],
    })


def _patch_peers(monkeypatch, *, codie, annie, sage, chairman):
    def _wrap(value):
        async def _fn(**kw):
            if isinstance(value, Exception):
                raise value
            return value
        return _fn
    monkeypatch.setattr("pipeline.agents.t3_council.run_codex_with_image", _wrap(codie))
    monkeypatch.setattr("pipeline.agents.t3_council.run_gemini_api_with_image", _wrap(annie))
    monkeypatch.setattr("pipeline.agents.t3_council.invoke_opus_vision", _wrap(sage))
    monkeypatch.setattr("pipeline.agents.t3_council.invoke_opus_text", _wrap(chairman))


def _manifest(tmp_path: Path) -> Path:
    p = tmp_path / "manifest.yaml"
    p.write_text(yaml.safe_dump({"critics": {"t3": {"per_call_timeout_s": 5, "wall_budget_s": 30}}}))
    return p


def _make_museum(tmp_path: Path, n: int = 1) -> Path:
    """Write n exhibits into a museum tree, each with one real asset PNG."""
    museum = tmp_path / "museum"
    for i in range(n):
        ex = Exhibit(
            exhibit_id=f"ex{i:02d}",
            project_slug="character-bible",
            run_slug="2026-06-10-smoke",
            title=f"Plate {i}",
            kind="plate_verdict",
            decision=Decision(outcome="approved", rationale="looks right"),
            output="assets/plate.png",
        )
        d = write_exhibit(museum, ex)
        assets = d / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        (assets / "plate.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    return museum


def test_gate_pass_does_not_block(tmp_path, monkeypatch):
    _patch_peers(
        monkeypatch,
        codie=_FakeResp(_verdict_json(verdict="pass")),
        annie=_FakeResp(_verdict_json(verdict="pass")),
        sage=_FakeResp(_verdict_json(verdict="pass")),
        chairman=_FakeResp(_verdict_json(verdict="pass", cites=["AC01"])),
    )
    museum = _make_museum(tmp_path, n=1)
    res = t3_council_gate(museum, _manifest(tmp_path), run_dir=tmp_path / "rundir")

    assert res.exhibits_reviewed == 1
    assert res.blocked is False
    assert res.results[0].verdict == "pass"
    assert res.results[0].n_artifacts == 1


def test_gate_fail_blocks_render(tmp_path, monkeypatch):
    _patch_peers(
        monkeypatch,
        codie=_FakeResp(_verdict_json(verdict="fail")),
        annie=_FakeResp(_verdict_json(verdict="fail")),
        sage=_FakeResp(_verdict_json(verdict="fail")),
        chairman=_FakeResp(_verdict_json(verdict="fail", reasoning="identity drift", cites=["IR.sean.x"])),
    )
    museum = _make_museum(tmp_path, n=1)
    res = t3_council_gate(museum, _manifest(tmp_path), run_dir=tmp_path / "rundir")

    assert res.blocked is True
    assert res.results[0].verdict == "fail"
    assert res.blocking_exhibits and res.blocking_exhibits[0].exhibit_id == "ex00"


def test_gate_stages_patches_with_proposed_by(tmp_path, monkeypatch):
    patch = [{"target": "manifest.lock.yaml", "path": "style.note", "operation": "set",
              "value": "tighten line weight", "rationale": "construction lines weak",
              "cites_criteria": ["IR.sean.style.x"]}]
    _patch_peers(
        monkeypatch,
        codie=_FakeResp(_verdict_json(verdict="borderline", patches=patch)),
        annie=_FakeResp(_verdict_json(verdict="pass")),
        sage=_FakeResp(_verdict_json(verdict="pass")),
        chairman=_FakeResp(_verdict_json(verdict="borderline", cites=["AC01"])),
    )
    museum = _make_museum(tmp_path, n=1)
    run_dir = tmp_path / "rundir"
    res = t3_council_gate(museum, _manifest(tmp_path), run_dir=run_dir)

    staged = read_staged_patches(run_dir)
    assert staged, "patches should stage into the gate run_dir lock"
    assert res.staged_patches == len(staged)
    by = {p["proposed_by"] for p in staged}
    assert by <= {"codie", "annie", "sage", "chairman"}
    assert "codie" in by  # the peer that proposed the patch
    # borderline (not fail) does not block
    assert res.blocked is False


def test_gate_contains_erroring_peer(tmp_path, monkeypatch):
    """One peer raising is a contained gap (status partial), never a crash."""
    _patch_peers(
        monkeypatch,
        codie=RuntimeError("codex boom"),
        annie=_FakeResp(_verdict_json(verdict="pass")),
        sage=_FakeResp(_verdict_json(verdict="pass")),
        chairman=_FakeResp(_verdict_json(verdict="pass", cites=["AC01"])),
    )
    museum = _make_museum(tmp_path, n=1)
    res = t3_council_gate(museum, _manifest(tmp_path), run_dir=tmp_path / "rundir")

    assert res.results[0].status == "partial"
    assert res.results[0].peer_verdicts["codie"]["status"] == "error"
    assert res.blocked is False  # chairman passed; a single contained gap doesn't block


def test_gate_all_peers_error_blocks(tmp_path, monkeypatch):
    _patch_peers(
        monkeypatch,
        codie=RuntimeError("boom"),
        annie=RuntimeError("boom"),
        sage=RuntimeError("boom"),
        chairman=_FakeResp(_verdict_json(verdict="pass")),
    )
    museum = _make_museum(tmp_path, n=1)
    res = t3_council_gate(museum, _manifest(tmp_path), run_dir=tmp_path / "rundir")

    assert res.results[0].status == "error"
    assert res.blocked is True  # all peers errored → no survivors → block


def test_gate_limit_caps_exhibits(tmp_path, monkeypatch):
    _patch_peers(
        monkeypatch,
        codie=_FakeResp(_verdict_json()),
        annie=_FakeResp(_verdict_json()),
        sage=_FakeResp(_verdict_json()),
        chairman=_FakeResp(_verdict_json(cites=["AC01"])),
    )
    museum = _make_museum(tmp_path, n=4)
    res = t3_council_gate(museum, _manifest(tmp_path), run_dir=tmp_path / "rundir", limit=2)
    assert res.exhibits_reviewed == 2


def test_gate_peer_verdicts_carry_live_vs_stub(tmp_path, monkeypatch):
    """The gate surfaces per-peer stub_fallback so the live smoke can prove
    each peer fired live, not stub."""
    _patch_peers(
        monkeypatch,
        codie=_FakeResp(_verdict_json(), stub_fallback=False, model="gpt-5-codex"),
        annie=_FakeResp(_verdict_json(), stub_fallback=True, model="stub-fallback"),
        sage=_FakeResp(_verdict_json(), stub_fallback=False, model="claude-opus-4-7"),
        chairman=_FakeResp(_verdict_json(cites=["AC01"])),
    )
    museum = _make_museum(tmp_path, n=1)
    res = t3_council_gate(museum, _manifest(tmp_path), run_dir=tmp_path / "rundir")
    pv = res.results[0].peer_verdicts
    assert pv["codie"]["stub_fallback"] is False and pv["codie"]["model"] == "gpt-5-codex"
    assert pv["annie"]["stub_fallback"] is True
