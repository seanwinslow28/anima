# tests/test_patch_efficacy_containment.py
"""G6.9 Gate 3 — per-case error containment in the LIVE orchestrator loop.

Regression guard for the 2026-06-08 Gate-2 crash: case #0 (`anatomy-ad1-six-fingers`,
identity_critical) blew the 900s per-case timeout, the `subprocess.TimeoutExpired`
propagated UNCAUGHT out of the orchestrator loop, and the whole run aborted with ZERO
cases recorded (empty JSON) — every completed case lost. The runbook claimed the live
path treats a failed worker as "an honest errored gap, not a silent zero", but the
orchestrator had no per-case try/except (only the worker was teardown-isolated by #37).

These tests pin the contract: a single case's timeout OR worker failure is recorded as a
gap (name, reason) and the run CONTINUES, preserving every completed case. Credential-free
— `_run_case_subprocess` is monkeypatched, so no model is called and nothing is spent.
"""
from __future__ import annotations

import subprocess

import evals.vision_critic.patch_efficacy as pe


def _eff(name: str) -> pe.CaseEfficacy:
    return pe.CaseEfficacy(name=name, corpus_id="X", defect_label="palette",
                           pair="C1", em_proposed=True, arms={})


def test_per_case_timeout_recorded_as_gap_not_fatal(monkeypatch):
    """A worker timeout on one case must NOT abort the run; completed cases survive."""
    sample = [{"name": "case-a"}, {"name": "case-b-timeout"}, {"name": "case-c"}]

    def fake_worker(case, *, arm_set, rerolls, stub):
        if case["name"] == "case-b-timeout":
            raise subprocess.TimeoutExpired(cmd=["worker"], timeout=pe._PER_CASE_TIMEOUT_S)
        return _eff(case["name"])

    monkeypatch.setattr(pe, "_run_case_subprocess", fake_worker)

    effs, errored = pe._run_live_cases(sample, arm_set="both+null", rerolls=3)

    assert [e.name for e in effs] == ["case-a", "case-c"]  # completed cases preserved
    assert [name for name, _ in errored] == ["case-b-timeout"]
    assert "timeout" in errored[0][1].lower()


def test_worker_runtime_error_recorded_as_gap_not_fatal(monkeypatch):
    """A worker that emits no sentinel (RuntimeError) is a gap, not a crash."""
    sample = [{"name": "case-a"}, {"name": "case-dies"}]

    def fake_worker(case, *, arm_set, rerolls, stub):
        if case["name"] == "case-dies":
            raise RuntimeError("worker emitted no CaseEfficacy (exit=1)")
        return _eff(case["name"])

    monkeypatch.setattr(pe, "_run_case_subprocess", fake_worker)

    effs, errored = pe._run_live_cases(sample, arm_set="both+null", rerolls=3)

    assert [e.name for e in effs] == ["case-a"]
    assert [name for name, _ in errored] == ["case-dies"]
    assert "RuntimeError" in errored[0][1]


def test_all_cases_errored_returns_empty_effs_not_crash(monkeypatch):
    """If every case fails, the run still returns cleanly (empty effs, full errored list)
    so aggregation reports an honest all-gap baseline rather than crashing."""
    sample = [{"name": "case-a"}, {"name": "case-b"}]

    def fake_worker(case, *, arm_set, rerolls, stub):
        raise subprocess.TimeoutExpired(cmd=["worker"], timeout=pe._PER_CASE_TIMEOUT_S)

    monkeypatch.setattr(pe, "_run_case_subprocess", fake_worker)

    effs, errored = pe._run_live_cases(sample, arm_set="both+null", rerolls=3)

    assert effs == []
    assert [name for name, _ in errored] == ["case-a", "case-b"]
    # aggregation over zero completed cases must not crash and must report N/A lift
    agg = pe.aggregate_efficacy(effs)
    assert pe.normalized_lift(agg) == {}
