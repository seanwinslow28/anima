"""Front-door code seam — emit_brief_dir (§4/§8 step 4).

The bundle: 00_studio_brief.md + concept.md + character_seeds.yaml +
frontdoor.json + manifest_gap_report.md. The gap report is red-team A5's
honesty artifact — it names each seed character not registered in the
manifest and the next Cy action (the front door never mutates manifest.yaml).
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from pipeline.frontdoor.brief import parse
from pipeline.frontdoor.emit import BUNDLE_FILES, emit_brief_dir
from pipeline.frontdoor.handoff import Handoff
from pipeline.frontdoor.validate import validate_brief_dir

FIXTURES = Path(__file__).resolve().parent / "fixtures"

# The golden front-door bundles: manifest fixture + expected cast per bundle.
GOLDEN_BUNDLES = {
    "pinata": ("manifest_pinata.yaml", ["kid", "grandma", "host-dad"]),
    "ai-guru": ("manifest_ai_guru.yaml", ["aiden", "orby"]),
}


def seed_brief_text() -> str:
    return (FIXTURES / "studio_brief_seed.md").read_text(encoding="utf-8")


def make_seeds() -> list[dict]:
    return [
        {
            "character_id": "kid",
            "display_name": "The Kid",
            "story_role": "protagonist — smallest at the party; something coiled underneath",
            "style_register": "pencil-test-colored",
            "source_notes": "Angular Tartakovsky design. Grandmother's faded headband.\n",
            "anchor_ref": None,
            "style_ref_ids": [],
            "cy_target_dir": "characters/kid/",
        },
        {
            "character_id": "grandma",
            "display_name": "The Late Grandmother",
            "story_role": "the engine — present only through objects, one photo, one ghost-beat",
            "style_register": "pencil-test-colored",
            "source_notes": "Never on screen living. Young-and-mid-fight snapshot is the reveal.\n",
            "anchor_ref": None,
            "style_ref_ids": [],
            "cy_target_dir": "characters/grandma/",
        },
    ]


def do_emit(out_dir: Path, manifest: dict | None = None) -> Path:
    return emit_brief_dir(
        out_dir,
        studio_brief_md=seed_brief_text(),
        concept_md="# Concept\n\n## Logline\n\nA tiny test concept.\n",
        seeds=make_seeds(),
        handoff=Handoff(
            slug="testpiece",
            characters=["kid", "grandma"],
            stage_provenance=["micro-expand", "interrogate", "synthesize"],
        ),
        manifest=manifest,
    )


def test_emit_writes_bundle(tmp_path):
    out = do_emit(tmp_path / "brief")
    assert sorted(p.name for p in out.iterdir()) == sorted(BUNDLE_FILES)
    assert set(BUNDLE_FILES) == {
        "00_studio_brief.md",
        "concept.md",
        "character_seeds.yaml",
        "frontdoor.json",
        "manifest_gap_report.md",
    }


def test_emitted_studio_brief_revalidates(tmp_path):
    out = do_emit(tmp_path / "brief")
    text = (out / "00_studio_brief.md").read_text(encoding="utf-8")
    assert parse(text).validate() == []


def test_gap_report_lists_unregistered_characters(tmp_path):
    manifest = {"characters": {"kid": {"folder": "characters/kid/"}}}
    out = do_emit(tmp_path / "brief", manifest=manifest)
    report = (out / "manifest_gap_report.md").read_text(encoding="utf-8")
    assert "grandma" in report
    assert "author_bible" in report  # the next Cy action is named
    # kid is registered — it must not be listed as a gap
    unregistered_block = report.split("## Registered")[0]
    assert "grandma" in unregistered_block
    assert "- **kid**" not in unregistered_block


def test_emit_is_idempotent(tmp_path):
    out = do_emit(tmp_path / "brief")
    first = {p.name: p.read_bytes() for p in out.iterdir()}
    out2 = do_emit(tmp_path / "brief")
    second = {p.name: p.read_bytes() for p in out2.iterdir()}
    assert first == second


def emit_from_fixture(bundle: str, out_dir: Path, manifest: dict | None = None) -> Path:
    """Emit a bundle from a committed golden fixture's own inputs."""
    src = FIXTURES / "frontdoor" / bundle
    return emit_brief_dir(
        out_dir,
        studio_brief_md=(src / "00_studio_brief.md").read_text(encoding="utf-8"),
        concept_md=(src / "concept.md").read_text(encoding="utf-8"),
        seeds=yaml.safe_load((src / "character_seeds.yaml").read_text(encoding="utf-8")),
        handoff=Handoff.from_json((src / "frontdoor.json").read_text(encoding="utf-8")),
        manifest=manifest,
    )


@pytest.mark.parametrize("bundle", ["pinata", "ai-guru"])
def test_golden_bundle_reemits_and_revalidates(bundle, tmp_path):
    out = emit_from_fixture(bundle, tmp_path / "brief")
    assert sorted(p.name for p in out.iterdir()) == sorted(BUNDLE_FILES)
    assert validate_brief_dir(out) == []


@pytest.mark.parametrize("bundle", ["pinata", "ai-guru"])
def test_golden_bundle_gap_report(bundle, tmp_path):
    manifest_name, characters = GOLDEN_BUNDLES[bundle]
    manifest = yaml.safe_load(
        (FIXTURES / "frontdoor" / manifest_name).read_text(encoding="utf-8")
    )

    # Against the registering manifest: zero unregistered.
    out = emit_from_fixture(bundle, tmp_path / "registered", manifest=manifest)
    report = (out / "manifest_gap_report.md").read_text(encoding="utf-8")
    unregistered_block = report.split("## Registered")[0]
    assert "## Unregistered characters (0)" in unregistered_block
    for cid in characters:
        assert f"- **{cid}**" not in unregistered_block

    # Against no manifest: every seed character is a gap.
    out = emit_from_fixture(bundle, tmp_path / "empty", manifest=None)
    report = (out / "manifest_gap_report.md").read_text(encoding="utf-8")
    unregistered_block = report.split("## Registered")[0]
    assert f"## Unregistered characters ({len(characters)})" in unregistered_block
    for cid in characters:
        assert f"- **{cid}**" in unregistered_block
