"""Tier-2 Slice 1: `--reference-blind` run-scoped override for the baseline runner.

The mascot baseline mirrors sean's G5 protocol (reference-blind, N=5). But since
G6.1b, production ships `critics.t2.attach_criteria_text: true`, so a default run
is NOT blind. `--reference-blind` forces BOTH attach flags off for the run,
overriding the manifest — and it must propagate to every per-case worker so the
"measured nothing because a flag was silently on" failure mode (the 2026-06-07
miss) cannot recur. `_apply_attach_flags` is the single resolution point.
"""
from evals.vision_critic.score import _apply_attach_flags


def test_reference_blind_forces_both_off_overriding_manifest():
    # Production manifest state: criteria-text ON. Blind must override it.
    manifest = {"critics": {"t2": {"attach_criteria_text": True, "attach_references": False}}}
    refs, crit = _apply_attach_flags(
        manifest, attach_references=False, attach_criteria_text=False, reference_blind=True)
    assert refs is False and crit is False
    assert manifest["critics"]["t2"]["attach_criteria_text"] is False


def test_no_overrides_preserves_manifest_default():
    # Without any override, the shipped manifest default (criteria-text ON) stands.
    manifest = {"critics": {"t2": {"attach_criteria_text": True}}}
    refs, crit = _apply_attach_flags(
        manifest, attach_references=False, attach_criteria_text=False, reference_blind=False)
    assert crit is True
    assert refs is False


def test_attach_flags_turn_on_when_set():
    manifest = {"critics": {"t2": {}}}
    refs, crit = _apply_attach_flags(
        manifest, attach_references=True, attach_criteria_text=True, reference_blind=False)
    assert refs is True and crit is True


def test_reference_blind_wins_over_attach_flags():
    # Defense-in-depth: even if both are somehow passed, blind is the safe default.
    manifest = {"critics": {"t2": {}}}
    refs, crit = _apply_attach_flags(
        manifest, attach_references=True, attach_criteria_text=True, reference_blind=True)
    assert refs is False and crit is False
