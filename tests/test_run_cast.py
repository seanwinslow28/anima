"""P1 — cast/namespace discovery (seams #9 + #11).

`character_id` means two different things: Flo wants the manifest folder key
(`alpha` -> style_register lookup); Em wants the IR namespace (`al` ->
query_by_character). derive_cast() builds the one table that threads both,
reading each Bible's acceptance_criteria.json for its validator-enforced
character_id (never string-parsing rule ids).
"""

from __future__ import annotations

import json

import pytest

from pipeline.orchestration.cast import derive_cast
from tests.orch_fixtures import mk_project, write_bible


def test_derive_cast_maps_folder_key_to_namespace(tmp_path, monkeypatch):
    mk_project(tmp_path, monkeypatch)
    import yaml
    manifest = yaml.safe_load((tmp_path / "proj" / "manifest.yaml").read_text())

    cast = derive_cast(manifest)

    assert [(m["folder_key"], m["ir_namespace"]) for m in cast] == [
        ("alpha", "al"),
        ("beta", "be"),
    ]
    assert cast[0]["anchor"] == "characters/alpha/anchor.png"
    assert cast[0]["criteria"] == "characters/alpha/acceptance_criteria.json"


def test_derive_cast_multi_namespace_bible_raises(tmp_path, monkeypatch):
    root, _ = mk_project(tmp_path, monkeypatch)
    bad = {
        "version": "1.2",
        "locked": False,
        "criteria": [
            {"id": "IR.al.style.line-weight", "description": "x",
             "cites_phase": [5], "cites_personas": ["em"], "character_id": "al"},
            {"id": "IR.zz.style.line-weight", "description": "x",
             "cites_phase": [5], "cites_personas": ["em"], "character_id": "zz"},
        ],
    }
    (root / "characters" / "alpha" / "acceptance_criteria.json").write_text(json.dumps(bad))
    import yaml
    manifest = yaml.safe_load((root / "manifest.yaml").read_text())

    with pytest.raises(ValueError, match="alpha"):
        derive_cast(manifest)


def test_derive_cast_missing_criteria_is_namespace_less(tmp_path, monkeypatch):
    root, _ = mk_project(tmp_path, monkeypatch)
    (root / "characters" / "alpha" / "acceptance_criteria.json").unlink()
    import yaml
    manifest = yaml.safe_load((root / "manifest.yaml").read_text())

    cast = derive_cast(manifest)

    alpha = next(m for m in cast if m["folder_key"] == "alpha")
    assert alpha["ir_namespace"] is None  # registered, not Em-reviewable; errors only if cast
    beta = next(m for m in cast if m["folder_key"] == "beta")
    assert beta["ir_namespace"] == "be"
