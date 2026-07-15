from pathlib import Path

import yaml

from pipeline.artdept.emit import BUNDLE_FILES, emit_artdept_dir
from pipeline.artdept.handoff import Handoff
from pipeline.artdept.validate import validate_artdept_dir


def _cast(anchor: str) -> dict:
    return {
        "designed": [
            {"character_id": "kid", "display_name": "The Kid", "tier": "principal",
             "style_register": "pencil-test-colored", "anchors": [anchor]}
        ],
        "world": [],
        "extras_guidance": "Background kids, varied, casual.",
    }


def _emit(tmp_path: Path, manifest: dict | None = None) -> Path:
    out = tmp_path / "artdept"
    out.mkdir(exist_ok=True)
    (out / "refs").mkdir(exist_ok=True)
    (out / "refs" / "kid.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    h = Handoff(slug="grandmaster", characters=["kid"],
                stage_provenance=["interrogate", "look-test", "synthesize"], mode="fixture")
    return emit_artdept_dir(
        out,
        design_bible_md="# Design bible\nGlasses = shed armor.\n",
        prompt_pack_md="# Prompt pack\n```\nanchor prompt\n```\n",
        orchestration_md="# Orchestration\nBatch 1…\n",
        environment_style_md="# Environment style\nSunlit backyard.\n",
        cast=_cast("refs/kid.png"),
        handoff=h,
        manifest=manifest,
        repo_root=tmp_path,
    )


def test_emits_all_bundle_files_and_validates(tmp_path):
    out = _emit(tmp_path)
    for name in BUNDLE_FILES:
        assert (out / name).exists(), name
    assert validate_artdept_dir(out, repo_root=tmp_path) == []


def test_emit_is_deterministic(tmp_path):
    out = _emit(tmp_path)
    first = {n: (out / n).read_bytes() for n in BUNDLE_FILES}
    out2 = _emit(tmp_path)
    assert {n: (out2 / n).read_bytes() for n in BUNDLE_FILES} == first


def test_readiness_report_names_the_gap_and_the_ready(tmp_path):
    report = (_emit(tmp_path, manifest={"characters": {}}) / "cy_readiness_report.md").read_text()
    assert "kid" in report
    assert "not in manifest `characters:`" in report
    assert "author_bible.py" in report
    report2 = (_emit(tmp_path, manifest={"characters": {"kid": {}}}) / "cy_readiness_report.md").read_text()
    # Strengthen: the registration gap should NOT appear when kid is in manifest
    assert "not in manifest `characters:`" not in report2


def test_readiness_report_ready_branch_fires_when_all_gaps_clear(tmp_path):
    # Create the anchor in source-refs so the anchor gap clears
    srcdir = tmp_path / "characters" / "kid" / "source-refs"
    srcdir.mkdir(parents=True)
    (srcdir / "kid.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    # Emit with kid in manifest (register is pencil-test-colored, which is authored)
    out = _emit(tmp_path, manifest={"characters": {"kid": {}}})
    report = (out / "cy_readiness_report.md").read_text()
    # The ready branch should fire: "registered; Cy-ready."
    assert "registered; Cy-ready." in report
    # The NOT Cy-ready branch should NOT fire
    assert "NOT Cy-ready" not in report


def test_cast_round_trips_through_yaml(tmp_path):
    out = _emit(tmp_path)
    assert yaml.safe_load((out / "cast_list.yaml").read_text()) == _cast("refs/kid.png")
