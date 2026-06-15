"""Bea the Storyboard Artist — eval suite runner.

Parameterized over evals/storyboard_artist/cases.yaml. Scaffold-stage suite:

  - positive cases validate that a beat_id-annotated ground-truth board
    round-trips through pipeline/orchestration/shots.py:load_shots AND passes
    Bea's deterministic storyboard_validate (coverage + no-orphans + the
    script<->board cast-conflict check) against its source beat sheet. This is
    the beats->board plumbing/coverage contract, proven on real corpus.

  - ships-red cases are Bea's NAMED failure modes — coverage gap, orphan shot,
    cast conflict. Unlike Sam's by-ear voice defects (which xfail), these are
    DETERMINISTIC: beat_id makes the beat<->shot link checkable, so the runner
    asserts storyboard_validate RAISES with the expected error. Green catches.

The composition pairwise-preference harness + the Sonnet/Gemini/Codex model
bake-off are intentionally NOT built here (campaign items — see README.md).

Run with: python -m pytest evals/storyboard_artist/runner.py -v
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from pipeline.orchestration.beats import load_beats
from pipeline.orchestration.shots import load_shots
from pipeline.agents.storyboard_artist import storyboard_validate

CASES = yaml.safe_load(
    (Path(__file__).parent / "cases.yaml").read_text(encoding="utf-8")
)["cases"]


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_storyboard_artist_case(case, fixtures_dir):
    kind = case["kind"]
    if kind == "positive":
        _run_positive(case, fixtures_dir)
    elif kind == "ships_red":
        _run_ships_red(case, fixtures_dir)
    else:
        raise AssertionError(f"unknown case kind {kind!r}")


def _run_positive(case: dict, fixtures_dir: Path) -> None:
    known = set(case["known_namespaces"])
    sheet = load_beats(fixtures_dir / case["beats"], known_namespaces=known)
    shot_list = load_shots(fixtures_dir / case["expected_shots"], known_namespaces=known)
    # The ground-truth board must pass Bea's deterministic gate …
    storyboard_validate(sheet, shot_list, known_namespaces=known)
    # … and board every beat.
    boarded = {f.beat_id for f in shot_list.frames if f.beat_id is not None}
    beat_ids = {b.id for b in sheet.beats}
    assert beat_ids <= boarded, f"{case['name']}: a beat is unboarded"


def _run_ships_red(case: dict, fixtures_dir: Path) -> None:
    known = set(case["known_namespaces"])
    sheet = load_beats(fixtures_dir / case["beats"], known_namespaces=known)
    # load_shots accepts the malformed board (schema is fine); the RELATIONAL
    # defect is what storyboard_validate must catch.
    shot_list = load_shots(fixtures_dir / case["fixture_shots"], known_namespaces=known)
    with pytest.raises(ValueError, match=case["expect_error"]):
        storyboard_validate(sheet, shot_list, known_namespaces=known)
