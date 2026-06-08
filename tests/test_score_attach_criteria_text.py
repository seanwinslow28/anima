"""CLI-flag tests for score.py's --attach-criteria-text run-scoped override (G6.1b
criteria-text decoupling, 2026-06-07). Credential-free / $0: tests 1-2 force the
--stub worker path (no model call ever fires), test 3 monkeypatches subprocess.run.

These guard the SCORE.PY CLI OVERRIDE end-to-end: argparse -> in-memory manifest
mutation -> honest refs= trace label -> per-case worker propagation. The override
attaches the IR criteria block (text handles) for ONE run WITHOUT attaching reference
images and WITHOUT committing critics.t2.attach_criteria_text: true to manifest.yaml
(the repo default stays false). It is INDEPENDENT of --attach-references: the
2026-06-07 re-baseline proved the criteria block was inert reference-blind because it
shared the attach_references gate. The third test is the anti-lie guard — the
orchestrator can never claim a criteria block a blind worker didn't actually see.

The NODE-level decoupling guarantee (criteria block present, zero images) is covered
by the anti-repeat test in tests/test_vision_critic_criteria.py.
"""
from __future__ import annotations

import json
import sys

import pytest

from evals.vision_critic import score as em_score

_SEAN_CASE = "clean-c01-idle-front"  # character_id: sean -> sean-anchor Bible criteria


@pytest.fixture
def _isolated_stub_runners():
    """main() in worker --stub mode calls _force_stub_runners(), which permanently
    reassigns the runner refs on pipeline.agents.vision_critic. Snapshot + restore so
    the stub can't leak into the rest of the suite (mirrors test_score_attach_references)."""
    from pipeline.agents import vision_critic as vc
    orig = (vc.run_antigravity_with_image, vc.run_gemini_api_with_image, vc.invoke_opus_vision)
    try:
        yield
    finally:
        (vc.run_antigravity_with_image, vc.run_gemini_api_with_image, vc.invoke_opus_vision) = orig


def _run_worker(monkeypatch, *extra):
    monkeypatch.setattr(sys, "argv", ["score", "--only", _SEAN_CASE, "--stub", *extra])
    em_score.main()


def test_cli_attach_criteria_text_engages_block(monkeypatch, capsys, _isolated_stub_runners):
    """--attach-criteria-text engages the criteria-text path: the worker's refs= label
    reads 'criteria-text (images off)', proving the flag flowed through argparse -> the
    in-memory manifest mutation -> _refs_label. Crucially it is NOT 'blind' (the prior
    run's invisible miss) and NOT a reference bundle (no images attached)."""
    _run_worker(monkeypatch, "--attach-criteria-text")
    err = capsys.readouterr().err
    assert "refs=[criteria-text (images off)]" in err, err
    assert "blind" not in err, f"criteria-text must never read blind:\n{err}"
    assert "anchor.png" not in err, f"criteria-text must attach ZERO images:\n{err}"


def test_cli_default_reflects_shipped_criteria_text(monkeypatch, capsys, _isolated_stub_runners):
    """The shipped manifest carries attach_criteria_text: true (RATIFIED 2026-06-08), so
    the no-flag default already engages criteria-text with images off — the production
    state. (Pre-G6.1b this asserted a bare 'blind' default; that is no longer shipped.
    The unit-level both-flags-off blind control lives in test_vision_critic_criteria.py.)"""
    _run_worker(monkeypatch)
    err = capsys.readouterr().err
    assert "refs=[criteria-text (images off)]" in err, err
    assert "anchor.png" not in err, f"criteria-text must attach ZERO images:\n{err}"


def test_subprocess_cmd_propagates_attach_criteria_text(monkeypatch):
    """Anti-lie guard: the orchestrator MUST forward --attach-criteria-text into the
    per-case worker command (a fresh process that re-reads manifest.yaml). Present when
    True, absent when False — else a blind worker would run while the orchestrator's
    refs= label claimed a criteria block it never attached."""
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
    em_score._run_case_subprocess(case, stub=True, attach_criteria_text=True)
    em_score._run_case_subprocess(case, stub=True, attach_criteria_text=False)

    on_cmd, off_cmd = cmds
    assert "--attach-criteria-text" in on_cmd, on_cmd
    assert "--attach-criteria-text" not in off_cmd, off_cmd
    assert "--only" in on_cmd and "x" in on_cmd  # sanity: worker still targets the case


def test_subprocess_cmd_independent_of_attach_references(monkeypatch):
    """Decoupling at the cmd level: --attach-criteria-text rides WITHOUT
    --attach-references (and vice-versa). The two flags are orthogonal."""
    cmds: list[list[str]] = []

    class _FakeCompleted:
        returncode = 0
        stdout = em_score._CASESCORE_SENTINEL + json.dumps({
            "name": "x", "case_class": "clean",
            "expected_verdict": "pass", "predicted_verdict": "pass",
        })
        stderr = ""

    monkeypatch.setattr(em_score.subprocess, "run",
                        lambda cmd, **kw: cmds.append(cmd) or _FakeCompleted())

    em_score._run_case_subprocess({"name": "x"}, stub=True,
                                  attach_references=False, attach_criteria_text=True)
    (cmd,) = cmds
    assert "--attach-criteria-text" in cmd
    assert "--attach-references" not in cmd, cmd
