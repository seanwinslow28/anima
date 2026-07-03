"""Front-door code seam — validate_brief_dir + the validate CLI (§8 step 5).

validate_brief_dir is the one gate SYNTHESIZE must clear before handing a
brief dir to `pipeline.run`: brief sections, handoff descriptor, inline
seed-shape checks (seeds.py was cut per red-team A6 — the shape lives here).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.frontdoor import cli
from pipeline.frontdoor.validate import validate_brief_dir
from tests.test_frontdoor_emit import do_emit

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "frontdoor"
PINATA = FIXTURES / "pinata"


@pytest.mark.parametrize("bundle", ["pinata", "ai-guru"])
def test_validate_passes_on_golden_bundle(bundle):
    assert validate_brief_dir(FIXTURES / bundle) == []


def test_validate_fails_on_truncated_brief(tmp_path):
    out = do_emit(tmp_path / "brief")
    brief_path = out / "00_studio_brief.md"
    text = brief_path.read_text(encoding="utf-8")
    brief_path.write_text(
        text.split("## What are the non-negotiables?")[0], encoding="utf-8"
    )
    problems = validate_brief_dir(out)
    assert any("non-negotiables" in p for p in problems)


def test_validate_checks_seed_shape(tmp_path):
    out = do_emit(tmp_path / "brief")
    (out / "character_seeds.yaml").write_text(
        "- character_id: The Kid\n  display_name: The Kid\n", encoding="utf-8"
    )
    problems = validate_brief_dir(out)
    assert any("lowercase-kebab" in p for p in problems)
    assert any("story_role" in p for p in problems)  # required field missing


def test_validate_flags_handoff_seed_mismatch(tmp_path):
    out = do_emit(tmp_path / "brief")
    seeds_text = (out / "character_seeds.yaml").read_text(encoding="utf-8")
    (out / "character_seeds.yaml").write_text(
        seeds_text.replace("character_id: grandma", "character_id: grandmother"),
        encoding="utf-8",
    )
    problems = validate_brief_dir(out)
    assert any("frontdoor.json" in p and "character_seeds.yaml" in p for p in problems)


def test_validate_fails_on_missing_files(tmp_path):
    out = do_emit(tmp_path / "brief")
    (out / "frontdoor.json").unlink()
    problems = validate_brief_dir(out)
    assert any("frontdoor.json" in p and "missing" in p for p in problems)


def test_cli_validate_exit_codes(tmp_path, capsys):
    assert cli.main(["validate", str(PINATA)]) == 0

    out = do_emit(tmp_path / "brief")
    (out / "00_studio_brief.md").write_text("# not a brief\n", encoding="utf-8")
    assert cli.main(["validate", str(out)]) == 1
    assert "missing section" in capsys.readouterr().out

    assert cli.main(["validate", str(tmp_path / "nowhere")]) == 2
