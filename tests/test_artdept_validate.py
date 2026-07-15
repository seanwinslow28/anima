"""Structural gate for an Art Department bundle dir (design §8).

Structure only: files present + non-empty, cast_list shape, anchors resolve,
handoff↔cast cross-check. Look/prompt quality is Sean's rubric, never asserted.
"""
from pathlib import Path

import yaml

from pipeline.artdept.handoff import Handoff
from pipeline.artdept.validate import register_warnings, validate_artdept_dir


def make_bundle(tmp_path: Path, *, register: str = "pencil-test-colored") -> Path:
    d = tmp_path / "artdept"
    (d / "refs").mkdir(parents=True)
    (d / "refs" / "kid-anchor.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (d / "design-bible.md").write_text("# Design bible\nGlasses = shed armor.\n")
    (d / "prompt-pack.md").write_text("# Prompt pack\n```\nFull-body anchor…\n```\n")
    (d / "chatgpt-orchestration.md").write_text("# Orchestration\nBatch 1 …\n")
    (d / "environment-style.md").write_text("# Environment style\nSunlit backyard…\n")
    cast = {
        "designed": [
            {
                "character_id": "kid",
                "display_name": "The Kid",
                "tier": "principal",
                "style_register": register,
                "anchors": ["refs/kid-anchor.png"],
            }
        ],
        "world": [
            {"id": "backyard-party", "display_name": "The backyard party", "refs": []}
        ],
        "extras_guidance": "Background kids 8-10, varied, casual summer clothes.",
    }
    (d / "cast_list.yaml").write_text(yaml.safe_dump(cast, sort_keys=False))
    h = Handoff(slug="grandmaster", characters=["kid"],
                stage_provenance=["interrogate", "look-test", "synthesize"], mode="fixture")
    (d / "artdept.json").write_text(h.to_json())
    (d / "cy_readiness_report.md").write_text("# Cy readiness — grandmaster\n- kid …\n")
    return d


def test_valid_bundle_passes(tmp_path):
    assert validate_artdept_dir(make_bundle(tmp_path)) == []


def test_missing_files_and_empty_prose_fail(tmp_path):
    d = make_bundle(tmp_path)
    (d / "prompt-pack.md").write_text("   \n")
    (d / "environment-style.md").unlink()
    problems = validate_artdept_dir(d)
    assert "prompt-pack.md is empty" in problems
    assert "missing file: environment-style.md" in problems


def test_cast_shape_enforced(tmp_path):
    d = make_bundle(tmp_path)
    cast = yaml.safe_load((d / "cast_list.yaml").read_text())
    cast["designed"][0].pop("style_register")
    cast["designed"][0]["tier"] = "cameo"
    cast["designed"][0]["anchors"] = []
    cast.pop("extras_guidance")
    (d / "cast_list.yaml").write_text(yaml.safe_dump(cast, sort_keys=False))
    problems = validate_artdept_dir(d)
    assert any("missing required field style_register" in p for p in problems)
    assert any("tier 'cameo'" in p for p in problems)
    assert any("anchors must be a non-empty list" in p for p in problems)
    assert any("extras_guidance" in p for p in problems)


def test_anchor_must_resolve_bundle_first_then_repo_root(tmp_path):
    d = make_bundle(tmp_path)
    cast = yaml.safe_load((d / "cast_list.yaml").read_text())
    cast["designed"][0]["anchors"] = ["refs/nonexistent.png"]
    (d / "cast_list.yaml").write_text(yaml.safe_dump(cast, sort_keys=False))
    problems = validate_artdept_dir(d, repo_root=tmp_path)
    assert any("anchor ref 'refs/nonexistent.png' does not resolve" in p for p in problems)
    # …and a repo-root-relative ref resolves even though it is not in the bundle:
    (tmp_path / "characters" / "kid" / "source-refs").mkdir(parents=True)
    (tmp_path / "characters" / "kid" / "source-refs" / "a.png").write_bytes(b"x")
    cast["designed"][0]["anchors"] = ["characters/kid/source-refs/a.png"]
    (d / "cast_list.yaml").write_text(yaml.safe_dump(cast, sort_keys=False))
    assert validate_artdept_dir(d, repo_root=tmp_path) == []


def test_handoff_cast_cross_check(tmp_path):
    d = make_bundle(tmp_path)
    h = Handoff(slug="grandmaster", characters=["kid", "grandma"],
                stage_provenance=["interrogate"], mode="fixture")
    (d / "artdept.json").write_text(h.to_json())
    problems = validate_artdept_dir(d)
    assert any("do not match" in p for p in problems)


def test_unregistered_register_warns_not_fails(tmp_path):
    d = make_bundle(tmp_path, register="not-a-register-yet")
    assert validate_artdept_dir(d) == []          # structure valid
    warnings = register_warnings(d)
    assert len(warnings) == 1
    assert "style-register-authoring-playbook" in warnings[0]


def test_malformed_yaml_reports_not_crashes(tmp_path):
    d = make_bundle(tmp_path)
    (d / "cast_list.yaml").write_text("designed: [\n  - character_id: kid\n")
    problems = validate_artdept_dir(d)
    assert any("cast_list.yaml invalid YAML" in p for p in problems)
    assert register_warnings(d) == []          # degrades quietly, never crashes
