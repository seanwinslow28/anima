"""The committed golden fixture stays valid. mode must be 'fixture' —
a fixture bundle can never masquerade as a live Artie session."""
import json
from pathlib import Path

from pipeline.artdept.validate import validate_artdept_dir

FIXTURE = Path("evals/artdept/fixtures/grandmaster-mini")


def test_golden_fixture_validates():
    assert FIXTURE.is_dir()
    assert validate_artdept_dir(FIXTURE) == []


def test_fixture_mode_is_fixture():
    payload = json.loads((FIXTURE / "artdept.json").read_text())
    assert payload["mode"] == "fixture"
