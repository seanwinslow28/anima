"""CLI-flag tests for score.py's --attach-references run-scoped override (G6
references re-test tooling, 2026-06-06). Credential-free / $0: tests 1-2 force the
--stub worker path (no model call ever fires), test 3 monkeypatches subprocess.run.

These guard the SCORE.PY CLI OVERRIDE end-to-end: argparse -> in-memory manifest
mutation -> honest refs= trace label -> per-case worker propagation. The override
exists so the references re-test can attach the Bible bundle for ONE run without ever
committing critics.t2.attach_references: true to manifest.yaml (the repo default stays
false). The NODE-level attach (Em actually receiving the bundle when the flag is true)
is covered by tests/test_vision_critic_references.py; the third test here is the
anti-lie guard — the orchestrator can never claim references a blind worker didn't see.
"""
from __future__ import annotations

import json
import sys

import pytest

from evals.vision_critic import score as em_score

_SEAN_CASE = "clean-c01-idle-front"  # character_id: sean -> sean-anchor Bible bundle


@pytest.fixture
def _isolated_stub_runners():
    """main() in worker --stub mode calls _force_stub_runners(), which permanently
    reassigns the runner refs on pipeline.agents.vision_critic. Snapshot + restore so
    the stub can't leak into the rest of the suite (mirrors test_score_stub_transports)."""
    from pipeline.agents import vision_critic as vc
    orig = (vc.run_antigravity_with_image, vc.run_gemini_api_with_image, vc.invoke_opus_vision)
    try:
        yield
    finally:
        (vc.run_antigravity_with_image, vc.run_gemini_api_with_image, vc.invoke_opus_vision) = orig


def _run_worker(monkeypatch, *extra):
    monkeypatch.setattr(sys, "argv", ["score", "--only", _SEAN_CASE, "--stub", *extra])
    em_score.main()


def test_cli_attach_references_engages_bundle(monkeypatch, capsys, _isolated_stub_runners):
    """--attach-references engages the references path: the worker's refs= label lists
    the real Bible bundle (anchor + turnarounds), proving the flag flowed through
    argparse -> the in-memory manifest mutation -> _refs_label."""
    _run_worker(monkeypatch, "--attach-references")
    err = capsys.readouterr().err
    assert "refs=[" in err, err
    assert "blind" not in err, f"expected a real bundle, got a blind label:\n{err}"
    assert "anchor.png" in err, f"expected anchor.png in the bundle:\n{err}"


def test_cli_default_attaches_no_reference_images(monkeypatch, capsys, _isolated_stub_runners):
    """Without --attach-references, zero reference IMAGES attach. Since G6.1b the shipped
    manifest carries attach_criteria_text: true (RATIFIED 2026-06-08), so the no-flag
    default reads 'criteria-text (images off)' — never a reference bundle. The point this
    guards is unchanged: --attach-references is the only switch that attaches images."""
    _run_worker(monkeypatch)
    err = capsys.readouterr().err
    assert "refs=[criteria-text (images off)]" in err, err
    assert "anchor.png" not in err, f"no reference images without --attach-references:\n{err}"


def test_subprocess_cmd_propagates_attach_references(monkeypatch):
    """Anti-lie guard: the orchestrator MUST forward --attach-references into the
    per-case worker command (a fresh process that re-reads manifest.yaml). Present
    when True, absent when False — else a blind worker would run while the
    orchestrator's refs= label claimed references it never attached."""
    cmds: list[list[str]] = []
    payload = em_score._CASESCORE_SENTINEL + json.dumps({
        "name": "x", "case_class": "clean",
        "expected_verdict": "pass", "predicted_verdict": "pass",
    })

    class _FakeCompleted:
        returncode = 0
        stdout = payload
        stderr = ""

    def _fake_run(cmd, **kwargs):
        cmds.append(cmd)
        return _FakeCompleted()

    monkeypatch.setattr(em_score.subprocess, "run", _fake_run)

    case = {"name": "x"}
    em_score._run_case_subprocess(case, stub=True, attach_references=True)
    em_score._run_case_subprocess(case, stub=True, attach_references=False)

    on_cmd, off_cmd = cmds
    assert "--attach-references" in on_cmd, on_cmd
    assert "--attach-references" not in off_cmd, off_cmd
    assert "--only" in on_cmd and "x" in on_cmd  # sanity: worker still targets the case
