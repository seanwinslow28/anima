"""artdept.json — same four-field discipline as frontdoor.json (design §8).

The schema is deliberately identical in shape: slug/characters/stage_provenance/mode.
No register field (registers live per-entry in cast_list.yaml, which the readiness
report reads); no budget field (nothing machine-reads one). No-schema-theater.
"""
import pytest

from pipeline.artdept.handoff import MODES, Handoff


def test_round_trips():
    h = Handoff(
        slug="grandmaster",
        characters=["kid", "grandma", "host-dad"],
        stage_provenance=["micro-expand", "interrogate", "look-test", "synthesize"],
        mode="interactive",
    )
    assert Handoff.from_json(h.to_json()) == h


def test_rejects_unknown_fields():
    with pytest.raises(ValueError, match="unknown artdept.json fields"):
        Handoff.from_json(
            '{"slug":"x","characters":["a"],"stage_provenance":["s"],"register":"primal-sketch-grit"}'
        )


def test_rejects_bad_slug_and_empty_lists():
    with pytest.raises(ValueError):
        Handoff(slug="Not Kebab", characters=["a"], stage_provenance=["s"])
    with pytest.raises(ValueError):
        Handoff(slug="ok", characters=[], stage_provenance=["s"])
    with pytest.raises(ValueError):
        Handoff(slug="ok", characters=["a"], stage_provenance=[])


def test_rejects_unknown_mode():
    assert MODES == ("interactive", "fixture")
    with pytest.raises(ValueError, match="mode"):
        Handoff(slug="ok", characters=["a"], stage_provenance=["s"], mode="live")
