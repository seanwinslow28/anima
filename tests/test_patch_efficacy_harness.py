# tests/test_patch_efficacy_harness.py
"""G6.9 Gate 3 — empirical patch-efficacy harness (machinery + §0, $0).

This push builds the loop and PROVES it on stubs; NO live generation runs here.
Covered: base-prompt resolution via the clean pair, view-correctness no-regen
routing, the per-re-roll fix check (defect cleared AND identity held), the §0
pre-flight (green on stub, RED on unratified goldens / ANTHROPIC_API_KEY set /
stub frame in a live run), and the clear-rate band. Regeneration + re-critique are
injected as fakes so the harness is exercised end-to-end credential-free.
"""
from __future__ import annotations

import yaml
from pathlib import Path

import pytest

from evals.vision_critic.prompt_apply import parse_corpus
from evals.vision_critic.patch_efficacy import (
    select_sample, resolve_base, run_case, preflight, estimate_cost,
    CaseEfficacy, RerollOutcome, PreflightError, FakeRegen, FakeCritique,
)

_ROOT = Path(__file__).resolve().parents[1]
_CASES = yaml.safe_load((_ROOT / "evals/vision_critic/cases.yaml").read_text())["cases"]
# patch_efficacy (Gate-3 fix-rate) resolves base prompts from the SEAN corpus spec
# (_CORPUS below). The claude-mascot corpus (ingested 2026-06-22, Tier-2 Slice 1)
# is a measurement baseline only; it is wired into Gate-3 in Slice 2 (mascot-aware
# parse_corpus + character-keyed resolve_base). Scope to sean until then.
_DEFECTS = [c for c in _CASES
            if c["case_class"] == "identity_style" and c.get("character_id") == "sean"]
_CORPUS = parse_corpus(_ROOT / "prompts/eval-corpus/sean-anchor-fixture-corpus.md")


def _case(label, verdict="fail"):
    return next(c for c in _DEFECTS
                if c["defect_label"] == label and c["expected_verdict"] == verdict)


# --------------------------------------------------------------------------- #
# Sampling + base-prompt resolution
# --------------------------------------------------------------------------- #
def test_select_sample_balances_across_labels():
    sample = select_sample(_DEFECTS, sample=12)
    assert len(sample) == 12
    labels = {c["defect_label"] for c in sample}
    assert labels == {"palette", "proportion", "view-correctness",
                      "anatomy-count", "construction-lines", "shading-register"}


def test_resolve_base_uses_clean_pair_prompt():
    kind, prompt = resolve_base(_case("palette"), _CORPUS)
    assert kind == "regen"
    assert "Maintain the warm 2D Disney pencil-test render" in prompt
    assert "Have the subject" in prompt  # the clean pair's scene


def test_resolve_base_view_is_no_regen():
    kind, prompt = resolve_base(_case("view-correctness"), _CORPUS)
    assert kind == "no-regen"


def test_resolve_base_every_defect_case_resolves():
    """No silent gaps: every defect case (incl. PA-D6 absent from the md, and the
    hand-drawn borderlines) resolves a base — via its clean pair."""
    for c in _DEFECTS:
        kind, prompt = resolve_base(c, _CORPUS)
        assert kind in ("regen", "no-regen")
        assert prompt, f"{c['name']} resolved no base prompt"


# --------------------------------------------------------------------------- #
# Per-case loop (injected fakes — no spend)
# --------------------------------------------------------------------------- #
def test_run_case_clean_pass_counts_as_fixed():
    """A regen that Em re-critiques as a clean pass with NO cites = defect cleared
    AND identity held = fixed."""
    eff = run_case(_case("palette"), arms=["golden"], rerolls=3, corpus=_CORPUS,
                   manifest={}, criteria=None,
                   regenerate_fn=FakeRegen(stub=True),
                   recritique_fn=FakeCritique(verdict="pass", cites=[]))
    arm = eff.arms["golden"]
    assert arm.clear_rate == 1.0
    assert all(r.fixed for r in arm.rerolls)


def test_run_case_residual_defect_is_not_fixed():
    """Re-critique still flags the original defect cite → defect NOT cleared."""
    c = _case("palette")
    eff = run_case(c, arms=["golden"], rerolls=2, corpus=_CORPUS, manifest={}, criteria=None,
                   regenerate_fn=FakeRegen(stub=True),
                   recritique_fn=FakeCritique(verdict="fail", cites=c["expected_cites"]))
    assert eff.arms["golden"].clear_rate == 0.0
    assert all(not r.fixed for r in eff.arms["golden"].rerolls)


def test_run_case_new_drift_breaks_identity_even_if_defect_cleared():
    """The subtle trap: the original defect is gone but the regen introduced a NEW
    cite (e.g. broke the face). Cleared-but-not-held = NOT fixed."""
    eff = run_case(_case("proportion"), arms=["em"], rerolls=1, corpus=_CORPUS,
                   manifest={}, criteria=None, em_value="taller",
                   regenerate_fn=FakeRegen(stub=True),
                   recritique_fn=FakeCritique(verdict="fail", cites=["IR.sean.face.jaw-width"]))
    r = eff.arms["em"].rerolls[0]
    assert r.defect_cleared is True       # original proportion cite absent
    assert r.identity_held is False       # a new (face) cite appeared
    assert r.fixed is False


def test_run_case_em_arm_no_proposal_records_not_fixed_not_error():
    eff = run_case(_case("palette"), arms=["em"], rerolls=2, corpus=_CORPUS,
                   manifest={}, criteria=None, em_value=None,
                   regenerate_fn=FakeRegen(stub=True),
                   recritique_fn=FakeCritique(verdict="pass", cites=[]))
    assert eff.em_proposed is False
    assert eff.arms["em"].clear_rate == 0.0   # nothing to apply → no fix credit
    assert eff.arms["em"].skipped_no_proposal is True


def test_view_case_recritiques_without_regenerating():
    c = _case("view-correctness")
    fake = FakeRegen(stub=True)
    eff = run_case(c, arms=["golden"], rerolls=2, corpus=_CORPUS, manifest={}, criteria=None,
                   regenerate_fn=fake, recritique_fn=FakeCritique(verdict="pass", cites=[]))
    assert all(not r.regenerated for r in eff.arms["golden"].rerolls)
    assert fake.calls == 0  # never regenerated a view case


# --------------------------------------------------------------------------- #
# §0 pre-flight
# --------------------------------------------------------------------------- #
def test_preflight_stub_passes(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    sample = select_sample(_DEFECTS, sample=6)
    # stub mode: no key needed, unratified allowed (we're not spending)
    preflight(sample, corpus=_CORPUS, live=False)  # must not raise


def test_preflight_refuses_unratified_when_live(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    # Force one case unratified — decoupled from the corpus's live ratification
    # state (the goldens were ratified 2026-06-08, so we synthesize the unratified
    # condition rather than relying on it).
    sample = select_sample(_DEFECTS, sample=6)
    sample = [dict(sample[0], golden_diff_ratified=False)] + sample[1:]
    with pytest.raises(PreflightError, match="ratif"):
        preflight(sample, corpus=_CORPUS, live=True)


def test_preflight_refuses_anthropic_key_when_live(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-should-refuse")
    sample = select_sample(_DEFECTS, sample=6)
    with pytest.raises(PreflightError, match="ANTHROPIC_API_KEY"):
        preflight(sample, corpus=_CORPUS, live=True)


def test_estimate_cost_is_reported_and_discounts_view():
    est = estimate_cost(sample=12, rerolls=3, arms=("em", "golden"), view_count=2)
    assert est["dollars"] > 0
    # view cases skip the NB2 generation cost (re-critique only)
    est_noview = estimate_cost(sample=12, rerolls=3, arms=("em", "golden"), view_count=0)
    assert est_noview["dollars"] > est["dollars"]


# --------------------------------------------------------------------------- #
# Subprocess-per-case isolation (the exit-144 teardown guard for the live loop)
# --------------------------------------------------------------------------- #
def test_run_case_subprocess_stub_roundtrips_a_caseefficacy():
    """The live loop runs each case in a FRESH process so Em's async Opus children
    can't trigger the exit-144 interpreter-teardown race in the orchestrator. A
    --stub worker must round-trip a CaseEfficacy byte-identical to the in-process
    run — proving the sentinel handshake (worker emits, parent parses) end-to-end,
    credential-free."""
    from dataclasses import asdict
    from evals.vision_critic.patch_efficacy import _run_case_subprocess, _stub_em_value

    c = _case("palette")
    # In-process reference — exactly what main()'s stub path builds for one case.
    ref = run_case(c, arms=("em", "golden", "null"), rerolls=1, corpus=_CORPUS,
                   manifest={}, criteria=None,
                   regenerate_fn=FakeRegen(stub=True),
                   recritique_fn=FakeCritique(verdict="pass", cites=[], stub_fallback=True),
                   em_value=_stub_em_value(c))

    got = _run_case_subprocess(c, arm_set="both+null", rerolls=1, stub=True)

    assert isinstance(got, CaseEfficacy)
    assert got.name == c["name"]
    assert set(got.arms) == {"em", "golden", "null"}
    # Deep structural parity: the worker's run is deterministic, so its serialized
    # CaseEfficacy must match the in-process one field-for-field after the round-trip.
    assert asdict(got) == asdict(ref)


def test_run_case_subprocess_raises_when_worker_emits_no_sentinel():
    """An unknown case never emits the sentinel → the parser raises an honest error
    (with the worker's exit code), rather than silently returning a half-built result."""
    from evals.vision_critic.patch_efficacy import _run_case_subprocess

    with pytest.raises(RuntimeError, match="no CaseEfficacy"):
        _run_case_subprocess({"name": "does-not-exist-zzz"},
                             arm_set="golden", rerolls=1, stub=True)
