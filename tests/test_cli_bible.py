"""Tests for pipeline.cli.bible — the `pipeline bible {init|show|approve|mutate|iterate}`
subcommands.

Mirrors tests/test_plan_cli.py in shape. Boxes live in the renderer; on disk
the artifacts stay clean prose. The renderer is a pure function so we assert
against the rendered string without subprocess invocation.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from PIL import Image

from pipeline.cli import bible

_CREAM = (242, 230, 204)


def _add_body_plate(character_dir: Path, name: str = "body-front") -> Path:
    """Drop a minimal cream body turnaround into the Bible so the SF03 gate has
    something to measure. Pixels are irrelevant in landmarks/opt-out modes."""
    ta = character_dir / "turnarounds"
    ta.mkdir(parents=True, exist_ok=True)
    p = ta / f"{name}.png"
    Image.new("RGB", (200, 400), _CREAM).save(p)
    return p


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_bible(
    character_dir: Path,
    *,
    character_id: str = "test-char",
    display_name: str = "Test Character",
    style_register: str = "pencil-test-colored",
    palette: list[dict] | None = None,
    proportions: dict | None = None,
    criteria: list[dict] | None = None,
    locked: bool = False,
    risk_bible_md: str = "## Test risk bible\n\nThe Bible covers front + profile only.",
    cy_notes_md: str = "## Confidence\n\nCy hedged on the back angle.",
    plate_plan: list[dict] | None = None,
) -> None:
    """Write a complete (or partial) Bible to character_dir for show/approve/mutate tests."""
    import yaml as _yaml

    character_dir.mkdir(parents=True, exist_ok=True)
    char_yaml = {
        "character_id": character_id,
        "display_name": display_name,
        "style_register": style_register,
        "palette": palette if palette is not None else [
            {"name": "warm cream", "hex": "#FAF5E8", "role": "paper-base"},
            {"name": "graphite", "hex": "#5B5B5B", "role": "line-contour"},
        ],
        "proportions": proportions if proportions is not None else {
            "head_to_body": "1:7",
            "shoulder_to_hip": "1.2:1",
            "notes": "Heroic-realistic.",
        },
        "identity_rules_pointer": "./acceptance_criteria.json",
        "cy_confidence_notes": "(see cy-confidence-notes.md)",
        "flux_lora_seed_plates": ["anchor.png"],
        "risks": "./risk-bible.md",
        "source_refs_consumed": [],
    }
    (character_dir / "character.yaml").write_text(
        _yaml.safe_dump(char_yaml, sort_keys=False), encoding="utf-8"
    )

    if criteria is None:
        criteria = [
            {
                "id": f"IR.{character_id}.hair.center-cowlick",
                "description": "Center cowlick at the crown.",
                "cites_phase": [5, 6],
                "cites_personas": ["em"],
                "impact_tag": "identity_critical",
                "character_id": character_id,
                "derived_from": [f"characters/{character_id}/anchor.png#region:hair"],
            },
            {
                "id": f"IR.{character_id}.prop.stylus-right-hand",
                "description": "Stylus stays in right hand.",
                "cites_phase": [5],
                "cites_personas": ["em"],
                "impact_tag": "identity_critical",
                "character_id": character_id,
                "derived_from": [f"characters/{character_id}/anchor.png#region:right-hand"],
            },
        ]
    (character_dir / "acceptance_criteria.json").write_text(
        json.dumps({"version": "1.2", "locked": locked, "criteria": criteria}, indent=2),
        encoding="utf-8",
    )
    (character_dir / "risk-bible.md").write_text(risk_bible_md, encoding="utf-8")
    (character_dir / "cy-confidence-notes.md").write_text(cy_notes_md, encoding="utf-8")

    if plate_plan is not None:
        (character_dir / "plate_generation_plan.json").write_text(
            json.dumps({"plates": plate_plan}, indent=2), encoding="utf-8"
        )


# ---------------------------------------------------------------------------
# init
# ---------------------------------------------------------------------------


def test_bible_init_scaffolds_folder_structure_and_templates(tmp_path, capsys):
    target = tmp_path / "characters" / "first-char"
    rc = bible.init_bible(str(target))
    assert rc == 0
    # Subdirectories scaffolded.
    for sub in ("turnarounds", "expressions", "motion_plates", "costumes",
                "props", "source-refs"):
        assert (target / sub).exists(), f"{sub} not scaffolded"
    # Templates copied.
    assert (target / "character.yaml").exists()
    assert (target / "source-refs" / "0-sean-author-this.md").exists()


def test_bible_init_idempotent(tmp_path):
    """Second invocation does not overwrite the templates Sean already edited."""
    target = tmp_path / "characters" / "idempotent"
    bible.init_bible(str(target))
    # Sean edits the template.
    edited = "character_id: idempotent\n# Sean's edits.\n"
    (target / "character.yaml").write_text(edited, encoding="utf-8")
    # Re-init.
    bible.init_bible(str(target))
    # The file is preserved.
    assert (target / "character.yaml").read_text() == edited


# ---------------------------------------------------------------------------
# show
# ---------------------------------------------------------------------------


def test_bible_show_renders_palette_swatch(tmp_path):
    cd = tmp_path / "characters" / "show-test"
    _write_bible(cd)
    rendered = bible.render_bible_tear_sheet(cd)
    # ANSI background escape present for each palette entry hex.
    assert "\x1b[48;2;250;245;232m" in rendered  # warm cream #FAF5E8
    assert "\x1b[48;2;91;91;91m" in rendered     # graphite #5B5B5B
    # Hex strings and role labels appear.
    assert "#FAF5E8" in rendered
    assert "paper-base" in rendered


def test_bible_show_groups_rules_by_category(tmp_path):
    cd = tmp_path / "characters" / "group-test"
    _write_bible(
        cd,
        character_id="grouptest",
        criteria=[
            {
                "id": "IR.grouptest.hair.front-cowlick",
                "description": "Front cowlick.",
                "cites_phase": [5],
                "cites_personas": ["em"],
                "impact_tag": "identity_critical",
                "character_id": "grouptest",
            },
            {
                "id": "IR.grouptest.hair.back-tuft",
                "description": "Back tuft.",
                "cites_phase": [5],
                "cites_personas": ["em"],
                "impact_tag": "aesthetic",
                "character_id": "grouptest",
            },
            {
                "id": "IR.grouptest.prop.stylus-right-hand",
                "description": "Stylus in right hand.",
                "cites_phase": [5],
                "cites_personas": ["em"],
                "impact_tag": "identity_critical",
                "character_id": "grouptest",
            },
        ],
    )
    rendered = bible.render_bible_tear_sheet(cd)
    # hair and prop both rendered as category subheadings.
    assert "### hair" in rendered
    assert "### prop" in rendered
    # The two hair rules sit under the same heading.
    hair_idx = rendered.index("### hair")
    prop_idx = rendered.index("### prop")
    assert hair_idx < prop_idx, "hair section should precede prop section (alphabetical)"
    hair_block = rendered[hair_idx:prop_idx]
    assert "front-cowlick" in hair_block
    assert "back-tuft" in hair_block


def test_bible_show_surfaces_lock_state_in_header(tmp_path):
    cd = tmp_path / "characters" / "lock-state"
    _write_bible(cd, locked=False)
    draft_render = bible.render_bible_tear_sheet(cd)
    _write_bible(cd, locked=True)
    locked_render = bible.render_bible_tear_sheet(cd)
    assert "draft" in draft_render
    assert "LOCKED" in locked_render


def test_bible_show_handles_missing_files_gracefully(tmp_path):
    """Bare folder with character.yaml only — show renders what it can."""
    cd = tmp_path / "characters" / "bare"
    cd.mkdir(parents=True)
    (cd / "character.yaml").write_text(
        "character_id: bare\ndisplay_name: Bare\nstyle_register: line-art-only\n",
        encoding="utf-8",
    )
    rendered = bible.render_bible_tear_sheet(cd)
    # Doesn't crash; header rendered.
    assert "bare" in rendered.lower()
    assert "line-art-only" in rendered


# ---------------------------------------------------------------------------
# approve
# ---------------------------------------------------------------------------


def test_bible_approve_flips_locked_true(tmp_path):
    cd = tmp_path / "characters" / "approve-test"
    _write_bible(cd, locked=False)
    rc = bible.approve_bible(str(cd))
    assert rc == 0
    payload = json.loads((cd / "acceptance_criteria.json").read_text())
    assert payload["locked"] is True


def test_bible_approve_idempotent(tmp_path):
    cd = tmp_path / "characters" / "approve-idempotent"
    _write_bible(cd, locked=True)
    rc = bible.approve_bible(str(cd))
    assert rc == 0  # already-locked is a no-op success


# ----- approve: SF03 proportion gate (G6.4) is a HARD gate at lock -----


def test_bible_approve_blocks_out_of_tolerance_body(tmp_path, capsys):
    """A body turnaround measuring 5 heads against a [6.5, 7.5] target BLOCKS the
    lock (rc 1) and leaves locked=false — the deterministic SF03 the pipeline
    declared but never enforced."""
    cd = tmp_path / "characters" / "drifted"
    _write_bible(
        cd,
        proportions={
            "head_to_body": "1:7",
            "head_to_body_target": 7.0,
            "tolerance_heads": [6.5, 7.5],
            "landmarks": {"crown_frac": 0.10, "chin_frac": 0.28, "feet_frac": 1.0},  # 5.0 heads
        },
    )
    _add_body_plate(cd)
    rc = bible.approve_bible(str(cd))
    assert rc == 1
    assert json.loads((cd / "acceptance_criteria.json").read_text())["locked"] is False
    assert "SF03" in capsys.readouterr().err


def test_bible_approve_blocks_undeclared_with_body_plates(tmp_path, capsys):
    """Prose-only proportions + body plates present = the silent-pass hole → BLOCK."""
    cd = tmp_path / "characters" / "prose-only"
    _write_bible(cd, proportions={"head_to_body": "1:7 — prose only", "notes": ""})
    _add_body_plate(cd)
    rc = bible.approve_bible(str(cd))
    assert rc == 1
    assert "undeclared" in capsys.readouterr().err.lower()


def test_bible_approve_passes_opt_out_character(tmp_path):
    """A box-creature that opts out of SF03 locks cleanly even with body plates."""
    cd = tmp_path / "characters" / "mascot"
    _write_bible(cd, proportions={"head_to_body": "N/A", "sf03": "opt_out"})
    _add_body_plate(cd)
    rc = bible.approve_bible(str(cd))
    assert rc == 0
    assert json.loads((cd / "acceptance_criteria.json").read_text())["locked"] is True


def test_bible_approve_passes_in_tolerance_body(tmp_path):
    """A body turnaround inside tolerance (stored landmarks ~7 heads) locks."""
    cd = tmp_path / "characters" / "clean"
    _write_bible(
        cd,
        proportions={
            "head_to_body": "1:7",
            "head_to_body_target": 7.0,
            "tolerance_heads": [6.5, 7.5],
            "landmarks": {"crown_frac": 0.05, "chin_frac": 0.175, "feet_frac": 0.93},  # ~7.04
        },
    )
    _add_body_plate(cd)
    rc = bible.approve_bible(str(cd))
    assert rc == 0
    assert json.loads((cd / "acceptance_criteria.json").read_text())["locked"] is True


def test_bible_approve_already_locked_skips_gate(tmp_path):
    """An already-locked Bible re-approves as a no-op WITHOUT re-running the gate —
    so a previously-locked character (e.g. sean-anchor) can't be retro-blocked by
    a newly-built gate. The gate guards NEW locks, not existing ones."""
    cd = tmp_path / "characters" / "already"
    _write_bible(
        cd,
        locked=True,
        proportions={
            "head_to_body": "1:7",
            "head_to_body_target": 7.0,
            "tolerance_heads": [6.5, 7.5],
            "landmarks": {"crown_frac": 0.10, "chin_frac": 0.28, "feet_frac": 1.0},  # would fail
        },
    )
    _add_body_plate(cd)
    rc = bible.approve_bible(str(cd))
    assert rc == 0  # no-op success; the out-of-tolerance plate is NOT re-gated


# ----- check-proportion: read-only retroactive SF03 verifier (G6.4) -----


def test_check_proportion_blocks_out_of_tolerance(tmp_path, capsys):
    cd = tmp_path / "characters" / "drifted"
    _write_bible(
        cd,
        proportions={
            "head_to_body_target": 7.0,
            "tolerance_heads": [6.5, 7.5],
            "landmarks": {"crown_frac": 0.10, "chin_frac": 0.28, "feet_frac": 1.0},  # 5 heads
        },
    )
    _add_body_plate(cd)
    rc = bible.check_proportion_bible(str(cd))
    assert rc == 1
    out = capsys.readouterr()
    assert "body-front" in out.out


def test_check_proportion_passes_in_tolerance(tmp_path):
    cd = tmp_path / "characters" / "clean"
    _write_bible(
        cd,
        proportions={
            "head_to_body_target": 7.0,
            "tolerance_heads": [6.5, 7.5],
            "landmarks": {"crown_frac": 0.05, "chin_frac": 0.175, "feet_frac": 0.93},
        },
    )
    _add_body_plate(cd)
    assert bible.check_proportion_bible(str(cd)) == 0


def test_check_proportion_is_read_only(tmp_path):
    """check-proportion never touches locked — it is a finding tool, not a gate."""
    cd = tmp_path / "characters" / "untouched"
    _write_bible(
        cd,
        locked=False,
        proportions={
            "head_to_body_target": 7.0,
            "tolerance_heads": [6.5, 7.5],
            "landmarks": {"crown_frac": 0.05, "chin_frac": 0.175, "feet_frac": 0.93},
        },
    )
    _add_body_plate(cd)
    bible.check_proportion_bible(str(cd))
    assert json.loads((cd / "acceptance_criteria.json").read_text())["locked"] is False


def test_cli_main_dispatches_check_proportion(tmp_path):
    """Regression guard (cf. the `bible add` dispatch test): the argv path must
    reach check_proportion_bible, not fall through to the bare `return 1`."""
    from pipeline.cli.__main__ import main

    cd = tmp_path / "characters" / "dispatch-check"
    _write_bible(
        cd,
        proportions={
            "head_to_body_target": 7.0,
            "tolerance_heads": [6.5, 7.5],
            "landmarks": {"crown_frac": 0.05, "chin_frac": 0.175, "feet_frac": 0.93},
        },
    )
    _add_body_plate(cd)
    rc = main(["bible", "check-proportion", "--character-dir", str(cd)])
    assert rc == 0, "check-proportion must dispatch through main()"


# ---------------------------------------------------------------------------
# mutate
# ---------------------------------------------------------------------------


def test_bible_mutate_refuses_without_force(tmp_path, capsys):
    cd = tmp_path / "characters" / "mutate-noforce"
    _write_bible(cd, locked=True)
    rd = tmp_path / "runs" / "x"
    rc = bible.mutate_bible(
        run_dir=str(rd),
        character_dir=str(cd),
        force=False,
        actor="sean",
        reason="test",
        target="IR.test-char.hair.center-cowlick",
        field="description",
        value="updated",
        content_version="1.3.0",
    )
    assert rc == 1
    err = capsys.readouterr().err
    assert "--force" in err


def test_bible_mutate_requires_actor_and_reason(tmp_path, capsys):
    cd = tmp_path / "characters" / "mutate-fields"
    _write_bible(cd, locked=True)
    rd = tmp_path / "runs" / "x"
    rc = bible.mutate_bible(
        run_dir=str(rd),
        character_dir=str(cd),
        force=True,
        actor="",
        reason="",
        target="IR.test-char.hair.center-cowlick",
        field="description",
        value="x",
        content_version="1.3.0",
    )
    assert rc == 1
    assert "--actor" in capsys.readouterr().err


def test_bible_mutate_writes_audit_record(tmp_path):
    cd = tmp_path / "characters" / "mutate-audit"
    _write_bible(cd, locked=True)
    rd = tmp_path / "runs" / "the-run"
    rc = bible.mutate_bible(
        run_dir=str(rd),
        character_dir=str(cd),
        force=True,
        actor="sean",
        reason="tighten the cowlick description",
        target="IR.test-char.hair.center-cowlick",
        field="description",
        value="Center cowlick rises 2cm forward of the crown.",
        content_version="1.3.0",
    )
    assert rc == 0
    audit_log = rd / "bible_audit.jsonl"
    assert audit_log.exists()
    lines = audit_log.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["actor"] == "sean"
    assert record["target"] == "IR.test-char.hair.center-cowlick"
    assert record["content_version_to"] == "1.3.0"
    # The schema version field stays loadable (the §4 regression).
    payload = json.loads((cd / "acceptance_criteria.json").read_text())
    assert payload["version"] == "1.2"
    rule = next(c for c in payload["criteria"] if c["id"] == "IR.test-char.hair.center-cowlick")
    assert rule["description"] == "Center cowlick rises 2cm forward of the crown."


# ---------------------------------------------------------------------------
# iterate
# ---------------------------------------------------------------------------


def test_bible_iterate_preserves_passing_plates(tmp_path):
    """Only the rejected plates land in the narrowed plan; the rest are preserved."""
    cd = tmp_path / "characters" / "iterate-test"
    plates = [
        {"target_path": "expressions/neutral.png", "source": "generate", "prompt": "neutral"},
        {"target_path": "expressions/angry.png", "source": "generate", "prompt": "angry"},
        {"target_path": "expressions/surprised.png", "source": "generate", "prompt": "surprised"},
        {"target_path": "turnarounds/body-front.png", "source": "generate", "prompt": "front"},
    ]
    _write_bible(cd, plate_plan=plates)

    rc = bible.iterate_bible(
        character_dir=str(cd),
        targets=["expressions"],
        rejected=["angry", "surprised"],
        reason="cy critic flagged inconsistent eyebrow ridges",
        run_dir=None,
    )
    assert rc == 0
    narrowed = json.loads((cd / "plate_generation_plan_iterate.json").read_text())
    paths = {p["target_path"] for p in narrowed["plates"]}
    # angry + surprised are queued; neutral and turnarounds are preserved (NOT in narrowed plan).
    assert paths == {"expressions/angry.png", "expressions/surprised.png"}
    # reject_reason is threaded into each plate.
    for plate in narrowed["plates"]:
        assert "cy critic" in plate["reject_reason"]


def test_bible_iterate_missing_plan_returns_error(tmp_path):
    cd = tmp_path / "characters" / "iterate-noplan"
    cd.mkdir(parents=True)
    rc = bible.iterate_bible(
        character_dir=str(cd),
        targets=["expressions"],
        rejected=["x"],
        reason="test",
        run_dir=None,
    )
    assert rc == 1


# ---------------------------------------------------------------------------
# CLI dispatch (main) — guards the argv → function wiring, not just the funcs
# ---------------------------------------------------------------------------


def test_cli_main_dispatches_bible_add(tmp_path):
    """Regression: `bible add` was registered as a subparser but never wired
    into the dispatch switch in __main__.py, so `python -m pipeline.cli bible
    add ...` fell through to the bare `return 1` and exited silently without
    touching the Bible. This test exercises the real argv path end-to-end so
    the silent no-op can't regress. (Bug found + fixed 2026-05-30.)"""
    from pipeline.cli.__main__ import main

    cd = tmp_path / "characters" / "dispatch-add"
    _write_bible(
        cd,
        character_id="dispatchadd",
        locked=True,
        plate_plan=[{"target_path": "anchor.png", "source": "ingest:anchor.png"}],
    )
    spec = {
        "plates": [{"target_path": "motion_plates/idle-01.png",
                    "source": "ingest:motion_plates/sheet.png#region:idle-01",
                    "cites_identity_rules": ["IR.dispatchadd.motion.idle-breath"]}],
        "rules": [{"id": "IR.dispatchadd.motion.idle-breath",
                   "description": "Idle breath, volume conserved.",
                   "cites_phase": [4, 6], "cites_personas": ["em"],
                   "impact_tag": "continuity", "character_id": "dispatchadd",
                   "derived_from": [f"characters/dispatchadd/anchor.png"]}],
    }
    spec_path = cd / "motion-additions.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    rd = tmp_path / "runs" / "dispatch-run"

    rc = main([
        "bible", "add",
        "--character-dir", str(cd),
        "--spec", str(spec_path),
        "--force", "--actor", "sean", "--reason", "dispatch regression",
        "--run-dir", str(rd),
        "--content-version", "1.3.0",
    ])
    assert rc == 0, "bible add must dispatch through main(), not fall through to return 1"
    payload = json.loads((cd / "acceptance_criteria.json").read_text())
    assert any(c["id"] == "IR.dispatchadd.motion.idle-breath" for c in payload["criteria"])
    assert payload["locked"] is True  # add never unlocks
    assert (rd / "bible_audit.jsonl").exists()
