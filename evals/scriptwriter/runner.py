"""Sam the Scriptwriter — eval suite runner.

Parameterized over evals/scriptwriter/cases.yaml. Scaffold-stage suite:

  - positive cases validate that a Sean-ratified ground-truth beat sheet
    round-trips through pipeline/orchestration/beats.py:load_beats AND passes
    Sam's deterministic structural pass (cast-coverage + sanity — Decision #1).
    This is the brief→beats plumbing/coverage contract, proven on real corpus.

  - ships-red cases are by-ear voice defects v1's deterministic pass does NOT
    catch (LLM aesthetic judges are weak/self-preferring — the handbook bars
    them). They are seed material for the deferred pairwise-preference harness.
    Most xfail by design (documented gap); the one literal default-prop case is
    caught by the deterministic default_prop_lint (the sanctioned exception).

The pairwise-preference harness is intentionally NOT built here (campaign item).

Run with: python -m pytest evals/scriptwriter/runner.py -v
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from pipeline.orchestration.beats import load_beats
from pipeline.agents.scriptwriter import structural_validate

from evals.scriptwriter.checks import default_prop_lint

CASES = yaml.safe_load(
    (Path(__file__).parent / "cases.yaml").read_text(encoding="utf-8")
)["cases"]


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_scriptwriter_case(case, fixtures_dir):
    kind = case["kind"]
    if kind == "positive":
        _run_positive(case, fixtures_dir)
    elif kind == "ships_red":
        _run_ships_red(case, fixtures_dir)
    else:
        raise AssertionError(f"unknown case kind {kind!r}")


def _run_positive(case: dict, fixtures_dir: Path) -> None:
    known = set(case["known_namespaces"])
    beats_path = fixtures_dir / case["expected_beats"]
    # The ground truth must round-trip through the real validator …
    sheet = load_beats(beats_path, known_namespaces=known)
    # … and pass Sam's deterministic structural pass (cast-coverage + sanity).
    structural_validate(sheet, known_namespaces=known)
    assert len(sheet.beats) >= 3
    covered = {ns for b in sheet.beats for ns in b.cast}
    assert known <= covered, f"{case['name']}: a loaded character has no beat"


def _run_ships_red(case: dict, fixtures_dir: Path) -> None:
    script_md = (fixtures_dir / case["fixture_script"]).read_text(encoding="utf-8")
    detector = case.get("detector", "none")
    if detector == "default_prop":
        # The one genuinely-deterministic ships-red lint (sanctioned, eval-side).
        assert default_prop_lint(script_md), (
            f"{case['name']}: default_prop_lint should flag the recycled prop"
        )
    else:
        # By-ear voice defect — v1's deterministic pass does not catch it. Seeded
        # for the deferred pairwise-preference harness; documented red.
        pytest.xfail(case["red_reason"])
