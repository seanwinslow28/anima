"""Front-door code seam — the Handoff descriptor (§5.3) + the Maya-gate acceptance.

frontdoor.json is the one deterministic contract the orchestrator writes:
minimal in Slice 1 (slug / characters / stage_provenance, plus the R1 `mode`
marker so a fixture-built brief can't masquerade as a real interactive run).

test_maya_plan_gate_accepts_frontdoor_brief is honestly named (red-team A5):
it proves Maya consumes the Studio Brief at the plan gate — NOT that Cy can
author the new characters or that the brief is GENERATE-ready. The
manifest_gap_report.md names that remaining work.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.frontdoor.handoff import Handoff

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "frontdoor"
PINATA = FIXTURES / "pinata"


def make_handoff(**overrides) -> Handoff:
    kwargs = dict(
        slug="grandmaster",
        characters=["kid", "grandma", "host-dad"],
        stage_provenance=["micro-expand", "interrogate", "synthesize"],
    )
    kwargs.update(overrides)
    return Handoff(**kwargs)


def test_handoff_json_roundtrip():
    handoff = make_handoff()
    assert Handoff.from_json(handoff.to_json()) == handoff
    payload = json.loads(handoff.to_json())
    assert payload["slug"] == "grandmaster"
    assert payload["mode"] == "interactive"


def test_rejects_bad_slug():
    with pytest.raises(ValueError, match="slug"):
        make_handoff(slug="Grandmaster")
    with pytest.raises(ValueError, match="slug"):
        make_handoff(slug="grand master")


def test_characters_must_be_slug_list():
    with pytest.raises(ValueError, match="character"):
        make_handoff(characters=["kid", "The Grandma"])
    with pytest.raises(ValueError, match="character"):
        make_handoff(characters="kid")


def test_rejects_unknown_mode():
    with pytest.raises(ValueError, match="mode"):
        make_handoff(mode="stubbed-live")


def test_maya_plan_gate_accepts_frontdoor_brief(tmp_path, monkeypatch):
    """--brief <pinata golden> --slug grandmaster --stub reaches the PLAN gate."""
    from pipeline import run as run_cli
    from pipeline.orchestration import state as st

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    run_dir = tmp_path / "grandmaster-run"

    rc = run_cli.main([
        "--brief", str(PINATA),
        "--slug", "grandmaster",
        "--stub",
        "--manifest", str(FIXTURES / "manifest_pinata.yaml"),
        "--run-dir", str(run_dir),
    ])
    assert rc == 0

    state = st.load_state(run_dir)
    assert state["stage"] == "PLAN"
    assert state["needs_storyboard"] is True  # no shots.yaml: an authoring run
    assert state["plan"]["status"] == "drafted"
    assert state["plan"]["stub"] is True  # a stub plan can never pass as real
    # kid/grandma/host-dad registered as namespaces by the test manifest
    assert [m["folder_key"] for m in state["cast"]] == ["kid", "grandma", "host-dad"]
    # the committed golden fixture is snapshotted, never mutated (Slice 2.1)
    assert Path(state["brief_dir"]) == run_dir / "brief"
