"""Tests for pipeline.agents.proportion_gate — the SF03 proportion gate (G6.4).

SF03 ("proportion drift") is a QA gate anima declared but never automated: the
sean-anchor body turnarounds baked into a LOCKED Bible at ~1:4-1:5.3 heads-tall
against a 1:7 target, and nothing caught it. This gate makes
`IR.{char}.proportion.head-to-body-1-to-7` checkable.

Design (docs/2026-06-03-sf03-proportion-gate-design.md): don't reverse-engineer
proportion from finished art — measure VERTICALLY against a view-invariant
armature. A figure is 7 heads tall from front/profile/back/3-quarter. Two
input modes share one verdict shape:
  - Approach A: an armature-gridded model-sheet → auto grid-alignment measure.
  - Approach B: stored crown/chin/feet landmarks → deterministic re-check.
  - extent_only fallback: figure extent is reliable but head height is not, so
    the gate returns `indeterminate` rather than a faked pass.

These tests are credential-free and synthesize their own PIL fixtures (cream
paper + warm-graphite ink), so CI stays green without API keys or committed
binaries.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from PIL import Image, ImageDraw

from pipeline.agents.proportion_gate import (
    FigureExtent,
    GateResult,
    ProportionSpec,
    ProportionVerdict,
    detect_armature_lines,
    figure_extent,
    gate_body_turnarounds,
    is_body_turnaround,
    load_proportion_spec,
    measure_proportion,
    plate_status_fields,
)

# Register colors from the sean-anchor Bible (style_register: pencil-test-colored).
CREAM = (242, 230, 204)      # #F2E6CC — paper substrate / background
GRAPHITE = (61, 53, 48)      # #3D3530 — warm graphite line / ink


# ---------------------------------------------------------------------------
# Fixture helpers — synthetic cream-paper plates with graphite ink
# ---------------------------------------------------------------------------


def _write_char_yaml(character_dir: Path, proportions: dict) -> Path:
    """Write a minimal character.yaml carrying just the proportions block."""
    character_dir.mkdir(parents=True, exist_ok=True)
    path = character_dir / "character.yaml"
    path.write_text(
        yaml.safe_dump(
            {"character_id": character_dir.name, "proportions": proportions},
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return path


# ---------------------------------------------------------------------------
# is_body_turnaround — only turnarounds/body-*.png are gated
# ---------------------------------------------------------------------------


def test_body_turnaround_paths_are_recognized():
    for rel in (
        "turnarounds/body-front.png",
        "turnarounds/body-back.png",
        "turnarounds/body-profile-left.png",
        "turnarounds/body-profile-right.png",
        "turnarounds/body-3quarter.png",
    ):
        assert is_body_turnaround(rel) is True, rel


def test_non_body_plates_are_not_gated():
    for rel in (
        "turnarounds/head-front.png",       # head plate, not a full figure
        "anchor.png",
        "expressions/neutral.png",
        "props/stylus.png",
        "motion_plates/idle-01.png",
    ):
        assert is_body_turnaround(rel) is False, rel


# ---------------------------------------------------------------------------
# load_proportion_spec — declared / opt_out / undeclared
# ---------------------------------------------------------------------------


def test_declared_spec_parses_target_and_tolerance(tmp_path):
    yaml_path = _write_char_yaml(
        tmp_path / "sean",
        {"head_to_body": "1:7", "head_to_body_target": 7.0, "tolerance_heads": [6.5, 7.5]},
    )
    spec = load_proportion_spec(yaml_path)
    assert isinstance(spec, ProportionSpec)
    assert spec.status == "declared"
    assert spec.target == 7.0
    assert spec.tolerance == (6.5, 7.5)
    assert spec.landmarks is None


def test_opt_out_spec_is_recognized(tmp_path):
    yaml_path = _write_char_yaml(
        tmp_path / "claude-mascot",
        {"head_to_body": "N/A — box creature", "sf03": "opt_out"},
    )
    spec = load_proportion_spec(yaml_path)
    assert spec.status == "opt_out"
    assert spec.target is None


def test_prose_only_proportions_are_undeclared(tmp_path):
    """A heads-tall character with only prose (no numeric target) is UNDECLARED —
    the silent-pass-on-missing-spec failure that let the 1:4-1:5.3 drift through.
    The folder gate must treat this as a block, not a pass."""
    yaml_path = _write_char_yaml(
        tmp_path / "sean",
        {"head_to_body": "1:7 — head fits seven times into body height."},
    )
    spec = load_proportion_spec(yaml_path)
    assert spec.status == "undeclared"


def test_missing_character_yaml_is_undeclared(tmp_path):
    spec = load_proportion_spec(tmp_path / "ghost" / "character.yaml")
    assert spec.status == "undeclared"


def test_declared_spec_carries_landmarks_when_present(tmp_path):
    """Approach B: stored crown/chin/feet fractions ride in the spec."""
    yaml_path = _write_char_yaml(
        tmp_path / "sean",
        {
            "head_to_body": "1:7",
            "head_to_body_target": 7.0,
            "tolerance_heads": [6.5, 7.5],
            "landmarks": {"crown_frac": 0.05, "chin_frac": 0.175, "feet_frac": 0.93},
        },
    )
    spec = load_proportion_spec(yaml_path)
    assert spec.status == "declared"
    assert spec.landmarks == {"crown_frac": 0.05, "chin_frac": 0.175, "feet_frac": 0.93}


# ---------------------------------------------------------------------------
# Image-fixture helpers — cream paper, graphite ink (the reliable primitives)
# ---------------------------------------------------------------------------


def _cream(path: Path, w: int = 200, h: int = 400) -> Image.Image:
    """Make a blank cream-paper canvas, save it to `path`, and return it so the
    caller can draw on it and re-save."""
    img = Image.new("RGB", (w, h), CREAM)
    img.save(path)
    return img


def _vbar(img: Image.Image, crown_y: int, feet_y: int, width: int = 20) -> None:
    """Draw a vertical graphite bar (a stand-in figure) crown_y..feet_y inclusive."""
    d = ImageDraw.Draw(img)
    cx = img.size[0] // 2
    d.rectangle([cx - width // 2, crown_y, cx + width // 2, feet_y], fill=GRAPHITE)


def _hline(img: Image.Image, y: int, thickness: int = 2) -> None:
    """Draw a full-width graphite horizontal rule (an armature division line)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, y, img.size[0] - 1, y + thickness - 1], fill=GRAPHITE)


# ---------------------------------------------------------------------------
# figure_extent — crown = top of figure ink, feet = bottom (the reliable read)
# ---------------------------------------------------------------------------


def test_figure_extent_reads_crown_and_feet(tmp_path):
    img = _cream(tmp_path / "f.png", h=400)
    _vbar(img, crown_y=100, feet_y=300)
    p = tmp_path / "f.png"
    img.save(p)
    ext = figure_extent(p)
    assert isinstance(ext, FigureExtent)
    assert abs(ext.crown_y - 100) <= 2, ext.crown_y
    assert abs(ext.feet_y - 300) <= 2, ext.feet_y
    assert ext.height_px == 400


def test_figure_extent_blank_paper_is_none(tmp_path):
    """Bare cream paper (with no figure) yields no extent — grain is below the
    1%-of-width floor, so it never reads as a figure."""
    p = tmp_path / "blank.png"
    _cream(p, h=400).save(p)
    ext = figure_extent(p)
    assert ext.crown_y is None and ext.feet_y is None


def test_figure_extent_excludes_full_width_armature_lines(tmp_path):
    """The crucial separation: on a gridded sheet the figure extent must read the
    FIGURE (crown/feet), not the printed grid. Armature rules above the crown and
    below the feet are full-width and must be excluded from the figure read."""
    img = _cream(tmp_path / "g.png", h=400)
    _hline(img, 50)    # grid line ABOVE the figure crown
    _hline(img, 350)   # grid line BELOW the figure feet
    _vbar(img, crown_y=100, feet_y=300)
    p = tmp_path / "g.png"
    img.save(p)
    ext = figure_extent(p)
    assert abs(ext.crown_y - 100) <= 3, f"crown should track the figure, not the grid line at 50: {ext.crown_y}"
    assert abs(ext.feet_y - 300) <= 3, f"feet should track the figure, not the grid line at 350: {ext.feet_y}"


# ---------------------------------------------------------------------------
# detect_armature_lines — printed full-width rules at known fractions
# ---------------------------------------------------------------------------


def test_detect_armature_lines_finds_eight_division_ladder(tmp_path):
    img = _cream(tmp_path / "ladder.png", h=400)
    ys = [40, 80, 120, 160, 200, 240, 280, 320]
    for y in ys:
        _hline(img, y)
    p = tmp_path / "ladder.png"
    img.save(p)
    lines = detect_armature_lines(p)
    assert len(lines) == len(ys), f"expected {len(ys)} lines, got {len(lines)}: {lines}"
    for got, want in zip(lines, ys):
        assert abs(got - want) <= 2, f"line {got} vs expected {want}"


def test_detect_armature_lines_ignores_the_figure(tmp_path):
    """A narrow vertical figure bar fills only ~10% of each row — it is never a
    full-width rule, so it produces zero armature lines."""
    img = _cream(tmp_path / "fig.png", h=400)
    _vbar(img, crown_y=80, feet_y=360)
    p = tmp_path / "fig.png"
    img.save(p)
    assert detect_armature_lines(p) == []


# ---------------------------------------------------------------------------
# measure_proportion — three input modes, one verdict shape
# ---------------------------------------------------------------------------


_LADDER_8 = [40, 80, 120, 160, 200, 240, 280, 320]  # 8 lines, 7 divisions, spacing 40


def _gridded(path: Path, lines_y: list[int], crown_y: int, feet_y: int, h: int = 400) -> Path:
    """A gridded model-sheet: a printed armature ladder + a figure spanning it."""
    img = _cream(path, h=h)
    for y in lines_y:
        _hline(img, y)
    _vbar(img, crown_y, feet_y)
    img.save(path)
    return path


def _declared(target: float = 7.0, tol=(6.5, 7.5), landmarks=None) -> ProportionSpec:
    return ProportionSpec(status="declared", target=target, tolerance=tol, landmarks=landmarks)


def test_armature_figure_spanning_grid_passes(tmp_path):
    """Approach A: a figure aligned crown→line0, feet→line7 reads 7.0 heads."""
    p = _gridded(tmp_path / "a.png", _LADDER_8, crown_y=40, feet_y=320)
    v = measure_proportion(p, _declared(), armature_path=p)
    assert isinstance(v, ProportionVerdict)
    assert v.method == "armature"
    assert v.verdict == "pass", v
    assert abs(v.heads_tall - 7.0) <= 0.15, v.heads_tall
    assert v.division_alignment is not None and v.division_alignment <= 0.1


def test_armature_short_figure_fails(tmp_path):
    """A figure that fills only 5 of the 7 divisions is out of [6.5, 7.5] → fail,
    and the misalignment surfaces in division_alignment."""
    p = _gridded(tmp_path / "short.png", _LADDER_8, crown_y=40, feet_y=240)
    v = measure_proportion(p, _declared(), armature_path=p)
    assert v.verdict == "fail", v
    assert abs(v.heads_tall - 5.0) <= 0.2, v.heads_tall
    assert v.division_alignment >= 1.5  # ~2 heads of feet misalignment


def test_landmarks_in_tolerance_passes(tmp_path):
    """Approach B: stored crown/chin/feet fractions yield ~7 heads → pass, and
    the plate pixels are not needed (deterministic re-check from the spec)."""
    spec = _declared(landmarks={"crown_frac": 0.05, "chin_frac": 0.175, "feet_frac": 0.93})
    p = _cream(tmp_path / "plain.png", h=400)
    p.save(tmp_path / "plain.png")
    v = measure_proportion(tmp_path / "plain.png", spec)
    assert v.method == "landmarks"
    assert v.verdict == "pass", v
    assert abs(v.heads_tall - 7.04) <= 0.1, v.heads_tall


def test_landmarks_out_of_tolerance_fails(tmp_path):
    spec = _declared(landmarks={"crown_frac": 0.10, "chin_frac": 0.28, "feet_frac": 1.0})
    p = tmp_path / "plain.png"
    _cream(p, h=400).save(p)
    v = measure_proportion(p, spec)
    assert v.method == "landmarks"
    assert v.verdict == "fail", v  # (1.0-0.10)/(0.28-0.10) = 5.0 heads


def test_extent_only_without_armature_or_landmarks_is_indeterminate(tmp_path):
    """The honest pre-feeder state: a declared character with a plain plate (no
    gridded sheet, no stored landmarks) reads figure extent but CANNOT measure
    head height — so the verdict is indeterminate, never a faked pass."""
    img = _cream(tmp_path / "plain.png", h=400)
    _vbar(img, crown_y=60, feet_y=360)
    p = tmp_path / "plain.png"
    img.save(p)
    v = measure_proportion(p, _declared())
    assert v.method == "extent_only"
    assert v.verdict == "indeterminate"
    assert v.heads_tall is None


def test_opt_out_spec_is_skipped(tmp_path):
    p = tmp_path / "plain.png"
    _cream(p, h=400).save(p)
    v = measure_proportion(p, ProportionSpec(status="opt_out"))
    assert v.verdict == "skipped"
    assert v.method == "opt_out"


def test_measure_never_raises_on_bad_input(tmp_path):
    """A missing armature artifact returns an `error` verdict, never an exception —
    a measurement failure must not crash a Bible bake (similarity_gate contract)."""
    spec = _declared()
    missing = tmp_path / "nope.png"
    v = measure_proportion(missing, spec, armature_path=missing)
    assert v.verdict == "error"
    assert v.target == 7.0  # spec context is preserved even on error


# ---------------------------------------------------------------------------
# gate_body_turnarounds — folder-level aggregation + block policy
# ---------------------------------------------------------------------------


def _char_with_bodies(
    character_dir: Path,
    proportions: dict,
    body_names=("body-front", "body-back"),
) -> Path:
    """Write a character.yaml + plain-figure body turnarounds (cream + a bar)."""
    _write_char_yaml(character_dir, proportions)
    ta = character_dir / "turnarounds"
    ta.mkdir(parents=True, exist_ok=True)
    for nm in body_names:
        p = ta / f"{nm}.png"
        img = _cream(p, h=400)
        _vbar(img, 60, 360)
        img.save(p)
    return character_dir


_LANDMARKS_7 = {"crown_frac": 0.05, "chin_frac": 0.175, "feet_frac": 0.93}   # ~7.04 heads
_LANDMARKS_5 = {"crown_frac": 0.10, "chin_frac": 0.28, "feet_frac": 1.0}      # 5.0 heads


def test_gate_all_pass_is_unblocked(tmp_path):
    cd = _char_with_bodies(
        tmp_path / "sean",
        {"head_to_body_target": 7.0, "tolerance_heads": [6.5, 7.5], "landmarks": _LANDMARKS_7},
    )
    result = gate_body_turnarounds(cd)
    assert isinstance(result, GateResult)
    assert result.blocked is False, result.reason
    assert len(result.verdicts) == 2
    assert all(v.verdict == "pass" for v in result.verdicts.values())


def test_gate_out_of_tolerance_blocks(tmp_path):
    cd = _char_with_bodies(
        tmp_path / "sean",
        {"head_to_body_target": 7.0, "tolerance_heads": [6.5, 7.5], "landmarks": _LANDMARKS_5},
    )
    result = gate_body_turnarounds(cd)
    assert result.blocked is True
    assert "body-front" in result.reason or "body-back" in result.reason


def test_gate_undeclared_with_body_plates_blocks(tmp_path):
    """The anti-silent-pass guard: prose-only spec + body plates present = BLOCK.
    This is the exact hole that let the 1:4-1:5.3 drift into a locked Bible."""
    cd = _char_with_bodies(
        tmp_path / "sean",
        {"head_to_body": "1:7 — prose only, no numeric target"},
    )
    result = gate_body_turnarounds(cd)
    assert result.blocked is True
    assert "undeclared" in result.reason.lower() or "opt_out" in result.reason


def test_gate_opt_out_never_blocks(tmp_path):
    cd = _char_with_bodies(
        tmp_path / "claude-mascot",
        {"head_to_body": "N/A — box creature", "sf03": "opt_out"},
    )
    result = gate_body_turnarounds(cd)
    assert result.blocked is False
    assert all(v.verdict == "skipped" for v in result.verdicts.values())


def test_gate_no_body_plates_is_unblocked(tmp_path):
    """A declared character with zero body turnarounds has nothing to gate."""
    _write_char_yaml(
        tmp_path / "sean",
        {"head_to_body_target": 7.0, "tolerance_heads": [6.5, 7.5]},
    )
    (tmp_path / "sean" / "turnarounds").mkdir(parents=True, exist_ok=True)
    result = gate_body_turnarounds(tmp_path / "sean")
    assert result.blocked is False
    assert result.verdicts == {}


def test_gate_passes_via_gridded_armature_sheet(tmp_path):
    """Approach A through the folder gate: a sibling gridded model-sheet under
    turnarounds/armature/ feeds the auto grid-alignment measure → pass."""
    cd = _char_with_bodies(
        tmp_path / "sean",
        {"head_to_body_target": 7.0, "tolerance_heads": [6.5, 7.5]},
        body_names=("body-front",),
    )
    armature_dir = cd / "turnarounds" / "armature"
    armature_dir.mkdir(parents=True, exist_ok=True)
    _gridded(armature_dir / "body-front.png", _LADDER_8, crown_y=40, feet_y=320)
    result = gate_body_turnarounds(cd)
    assert result.blocked is False, result.reason
    v = result.verdicts["turnarounds/body-front.png"]
    assert v.method == "armature" and v.verdict == "pass"


def test_gate_extent_only_is_indeterminate_and_blocks(tmp_path):
    """The honest pre-feeder state: declared spec, plain body plates, no armature
    and no landmarks → indeterminate → BLOCKED (the gate refuses to certify what
    it cannot measure). This is the A4 finding sean-anchor returns today."""
    cd = _char_with_bodies(
        tmp_path / "sean",
        {"head_to_body_target": 7.0, "tolerance_heads": [6.5, 7.5]},
        body_names=("body-front",),
    )
    result = gate_body_turnarounds(cd)
    assert result.blocked is True
    assert result.verdicts["turnarounds/body-front.png"].verdict == "indeterminate"


# ---------------------------------------------------------------------------
# plate_status_fields — mutates the Cy plate status dict (persists via JSONL)
# ---------------------------------------------------------------------------


def test_plate_status_fields_body_declared_populates(tmp_path):
    cd = _char_with_bodies(
        tmp_path / "sean",
        {"head_to_body_target": 7.0, "tolerance_heads": [6.5, 7.5], "landmarks": _LANDMARKS_7},
        body_names=("body-front",),
    )
    status: dict = {"status": "ingested"}
    plate_status_fields(cd / "turnarounds" / "body-front.png", cd, status)
    assert status["sf03_gate"] == "hard"
    assert status["sf03_verdict"] == "pass"
    assert status["sf03_target"] == 7.0
    assert status["sf03_tolerance"] == [6.5, 7.5]
    assert status["sf03_method"] == "landmarks"


def test_plate_status_fields_non_body_is_skipped(tmp_path):
    cd = tmp_path / "sean"
    _write_char_yaml(cd, {"head_to_body_target": 7.0, "tolerance_heads": [6.5, 7.5]})
    status: dict = {"status": "ingested"}
    plate_status_fields(cd / "turnarounds" / "head-front.png", cd, status)
    assert status["sf03_gate"] == "skipped"
    assert "sf03_heads_tall" not in status  # non-body plates carry only the gate marker


def test_plate_status_fields_opt_out_is_skipped(tmp_path):
    cd = _char_with_bodies(
        tmp_path / "claude-mascot",
        {"head_to_body": "N/A", "sf03": "opt_out"},
        body_names=("body-front",),
    )
    status: dict = {"status": "ingested"}
    plate_status_fields(cd / "turnarounds" / "body-front.png", cd, status)
    assert status["sf03_gate"] == "skipped"
    assert status["sf03_verdict"] == "opt_out"


def test_plate_status_fields_are_json_serializable(tmp_path):
    """Guards persistence through _persist_plate_verdicts (json.dumps each status)."""
    import json

    cd = _char_with_bodies(
        tmp_path / "sean",
        {"head_to_body_target": 7.0, "tolerance_heads": [6.5, 7.5], "landmarks": _LANDMARKS_7},
        body_names=("body-front",),
    )
    status: dict = {"status": "ingested", "target_path": "turnarounds/body-front.png"}
    plate_status_fields(cd / "turnarounds" / "body-front.png", cd, status)
    round_tripped = json.loads(json.dumps(status, sort_keys=True))
    assert round_tripped["sf03_verdict"] == "pass"


# ---------------------------------------------------------------------------
# Real Bibles — the committed character.yaml specs (sean declared, mascot opt-out)
# ---------------------------------------------------------------------------

_REPO = Path(__file__).resolve().parents[1]


def test_sean_anchor_declares_seven_heads():
    """sean-anchor (heroic-realistic 1:7 human) carries the numeric spec that
    makes IR.sean.proportion.head-to-body-1-to-7 checkable."""
    spec = load_proportion_spec(_REPO / "characters" / "sean-anchor" / "character.yaml")
    assert spec.status == "declared"
    assert spec.target == 7.0
    assert spec.tolerance == (6.5, 7.5)


def test_claude_mascot_opts_out_of_sf03():
    """claude-mascot is a box-creature, not heads-tall — it opts out rather than
    being measured against a human armature (per-character spec-driven, never a
    hardcoded 1:7)."""
    spec = load_proportion_spec(_REPO / "characters" / "claude-mascot" / "character.yaml")
    assert spec.status == "opt_out"


# ---------------------------------------------------------------------------
# Phase C — Approach-A hardening (the ¾ probe finding) + the feeder primitives
# ---------------------------------------------------------------------------


def test_armature_uses_known_divisions_not_detected_line_count(tmp_path):
    """The ¾ probe finding: NB2 redrew the ladder with 9 lines (8 bands) instead
    of 8 while the figure stayed seated crown-to-feet. The measure must anchor on
    the bold first/last lines + the KNOWN division count (7), not the detected
    line count — so it reads ~7 (pass), not the 8.3 detected-count artifact."""
    img = _cream(tmp_path / "q.png", w=768, h=1024)
    nine = [58, 171, 284, 397, 510, 623, 736, 848, 960]  # NB2's 9-line redraw
    for y in nine:
        _hline(img, y)
    _vbar(img, crown_y=54, feet_y=989)  # figure spans crown..feet
    p = tmp_path / "q.png"
    img.save(p)
    spec = _declared()  # target 7.0 → known divisions 7 (no explicit field needed)
    v = measure_proportion(p, spec, armature_path=p)
    assert v.verdict == "pass", v
    assert 6.7 <= v.heads_tall <= 7.5, v.heads_tall
    # the line-count drift is surfaced for transparency, not silently dropped
    assert "9" in v.detail and "8" in v.detail  # detected 9 vs expected 8 lines


def test_armature_explicit_divisions_override(tmp_path):
    """A character may declare armature_divisions explicitly (defaults to
    round(target))."""
    yaml_path = _write_char_yaml(
        tmp_path / "c",
        {
            "head_to_body_target": 7.0,
            "tolerance_heads": [6.5, 7.5],
            "armature_divisions": 7,
        },
    )
    spec = load_proportion_spec(yaml_path)
    assert spec.armature_divisions == 7


def test_build_armature_underlay_produces_detectable_ladder(tmp_path):
    """The canonical deterministic armature: divisions+1 full-width lines on cream,
    crown + feet bolded, readable by detect_armature_lines."""
    from pipeline.agents.proportion_gate import build_armature_underlay

    p = build_armature_underlay(tmp_path / "arm.png", divisions=7, size=(768, 1024))
    assert p.exists()
    lines = detect_armature_lines(p)
    assert len(lines) == 8, f"7 divisions → 8 lines, got {len(lines)}: {lines}"


def test_emit_gridded_model_sheet_writes_to_armature_dir(tmp_path, monkeypatch):
    """The Approach-A feeder primitive: generate a gridded model-sheet from a
    clean body plate (armature underlay + the plate as references) and write it
    where _find_armature looks — turnarounds/armature/<name>.png. Generation is
    monkeypatched so this stays credential-free."""
    from pipeline.agents import proportion_gate as pg

    cd = _char_with_bodies(
        tmp_path / "sean",
        {"head_to_body_target": 7.0, "tolerance_heads": [6.5, 7.5]},
        body_names=("body-front",),
    )
    plate = cd / "turnarounds" / "body-front.png"

    captured = {}

    def fake_invoke(*, prompt, reference_images, output_path, cache_dir, **kw):
        captured["refs"] = list(reference_images)
        captured["out"] = output_path
        # Stand in for NB2: write a valid gridded sheet to the output path.
        pg.build_armature_underlay(output_path, divisions=7, size=(768, 1024))
        from types import SimpleNamespace
        return SimpleNamespace(ok=True, stub_fallback=False, exit_code=0,
                               output_path=output_path, cache_key="k", cache_hit=False)

    monkeypatch.setattr(pg, "invoke_image_edit", fake_invoke)

    out = pg.emit_gridded_model_sheet(plate, cd, cache_dir=tmp_path / ".cache")
    assert out == cd / "turnarounds" / "armature" / "body-front.png"
    assert out.exists()
    # The armature underlay is one of the references handed to the generator.
    assert any("armature" in str(r) or "underlay" in str(r) for r in captured["refs"])
    # And the gate now finds it (Approach-A path is live).
    from pipeline.agents.proportion_gate import _find_armature
    assert _find_armature(plate) == out
