"""Tier-2 Slice 1: `--character-id` scoping for the vision-critic baseline runner.

The mascot baseline must run reference-blind over ONLY the `claude-mascot` cases
without re-running the frozen sean corpus (whose ratified trace must not move).
`score._select_cases` gained a `character_id` filter; absent the filter, selection
is byte-identical to the legacy behavior (back-compat for every existing run).
"""
from evals.vision_critic.score import CASES, _select_cases


def _cases_for(character_id: str) -> list[dict]:
    # The convention used throughout score.py: an unlabeled case is "sean".
    return [c for c in CASES if c.get("character_id", "sean") == character_id]


def test_character_id_filters_to_only_that_corpus():
    selected, excluded = _select_cases("all", 0, character_id="claude-mascot")
    assert selected == _cases_for("claude-mascot")
    assert excluded == []
    assert selected, "expected a non-empty mascot corpus"
    assert all(c.get("character_id") == "claude-mascot" for c in selected)


def test_character_id_does_not_leak_other_corpus():
    selected, _ = _select_cases("all", 0, character_id="claude-mascot")
    assert not any(c.get("character_id", "sean") == "sean" for c in selected)


def test_character_id_defaults_sean_for_unlabeled_cases():
    selected, _ = _select_cases("all", 0, character_id="sean")
    assert selected == _cases_for("sean")


def test_no_character_id_is_backcompat_all():
    # Legacy callers pass no character_id; selection must be byte-identical.
    assert _select_cases("all", 0) == _select_cases("all", 0, character_id=None)
    selected, excluded = _select_cases("all", 0)
    assert selected == list(CASES)
    assert excluded == []


def test_character_id_composes_with_performs_segment():
    # The filter narrows the universe; segment scoping still applies within it.
    selected, _ = _select_cases("performs", 0, character_id="claude-mascot")
    mascot = _cases_for("claude-mascot")
    expected = [c for c in mascot if c["case_class"] in ("clean", "identity_style")]
    assert selected == expected
