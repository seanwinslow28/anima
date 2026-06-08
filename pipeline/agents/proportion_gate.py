"""anima — SF03 proportion gate (G6.4): a hard, deterministic, per-character
proportion check at Cy Pass-3 / Bible-lock.

Why this module exists
----------------------
SF03 ("proportion drift") is a QA gate anima DECLARED but never AUTOMATED. The
cost was concrete: sean-anchor's body turnarounds were baked into a LOCKED Bible
at ~1:4-1:5.3 heads-tall against a 1:7 target, and nothing caught it. The only
proportion-adjacent signal — Cy's Pass-2.5 similarity gate — is record-only and
measures identity recognizability, not geometry.

Two prior spikes proved you cannot reliably RECOVER head-to-body ratio from
finished stylized art (DINOv2 NO-GO; dependency-free chin-detection NO-GO). The
common failure is the inverse problem: reconstruct crown/chin/feet from arbitrary
art. So this gate does the opposite — it CONSTRAINS proportion against a known
vertical armature and VERIFIES the render against it. Head-to-body ratio is a
vertical, view-invariant measurement (a figure is 7 heads tall from front,
profile, back, or 3-quarter), which is why one ladder validates every turnaround.

Design doc: docs/2026-06-03-sf03-proportion-gate-design.md.

What this module is (and is not)
--------------------------------
- A HARD gate, unlike the record-only similarity gate: a body turnaround outside
  tolerance BLOCKS the Bible-lock (enforced in pipeline/cli/bible.py).
- Per-character SPEC-DRIVEN, never a hardcoded 1:7. The target + tolerance live in
  the character's character.yaml `proportions:` block; a non-heads-tall character
  (claude-mascot, a box-creature) declares `sf03: opt_out`.
- Three input modes, ONE verdict shape, so the probe outcome (Approach A vs B)
  changes only the INPUT artifact, never this contract:
    * Approach A — an armature-gridded model-sheet → auto grid-alignment measure.
    * Approach B — stored crown/chin/feet landmarks → deterministic re-check.
    * extent_only fallback — figure extent is reliable but head height is not, so
      the gate returns `indeterminate` (an honest non-measurement) rather than a
      faked pass. This is the gate's pre-feeder shipping state.

Deterministic PIL/numpy only (mirrors pipeline/audit.py HF01 + similarity_gate's
never-raise contract). Credential-free; tests synthesize their own fixtures.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Module-level so emit_gridded_model_sheet is monkeypatchable in tests and the
# measurement core (which never calls it) stays import-light. Guarded so a
# missing runner never breaks the spec/measurement path. nb_pro_runner is
# import-light (no heavy deps at module top) and does not import this module,
# so there is no cycle.
try:  # pragma: no cover - import wiring
    from pipeline.agents.nb_pro_runner import invoke_image_edit
except Exception:  # pragma: no cover
    invoke_image_edit = None


# ---------------------------------------------------------------------------
# Spec
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProportionSpec:
    """The per-character proportion contract, read from character.yaml.

    status:
      - "declared"   — a numeric heads-tall target + tolerance are present.
      - "opt_out"    — the character is not heads-tall (e.g. a box-creature);
                       the human-figure armature does not transfer. Never blocks.
      - "undeclared" — a heads-tall character with prose only and no numeric
                       target. The silent-pass-on-missing-spec hole that let the
                       1:4-1:5.3 drift through; the folder gate treats it as a
                       BLOCK, never a pass.
    target/tolerance are None unless status == "declared".
    landmarks carries the optional Approach-B {crown_frac, chin_frac, feet_frac}.
    """

    status: str
    target: float | None = None
    tolerance: tuple[float, float] | None = None
    landmarks: dict | None = None
    # Approach-A armature: how many head-bands the ladder divides into. Defaults
    # to round(target) when absent. Used as the KNOWN division count so a measure
    # never trusts the line count NB2 redrew (the ¾ probe finding).
    armature_divisions: int | None = None


def load_proportion_spec(character_yaml_path) -> ProportionSpec:
    """Parse the proportions block of a character.yaml into a ProportionSpec.

    Never raises — a missing file, missing block, or malformed numbers all
    degrade to status="undeclared" (which the folder gate blocks on, so the
    failure is loud, not silent)."""
    path = Path(character_yaml_path)
    if not path.exists():
        return ProportionSpec(status="undeclared")
    try:
        import yaml

        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return ProportionSpec(status="undeclared")

    proportions = raw.get("proportions") or {}
    if not isinstance(proportions, dict):
        return ProportionSpec(status="undeclared")

    if str(proportions.get("sf03", "")).strip().lower() == "opt_out":
        return ProportionSpec(status="opt_out")

    target = proportions.get("head_to_body_target")
    tol = proportions.get("tolerance_heads")
    if target is None or not isinstance(tol, (list, tuple)) or len(tol) != 2:
        return ProportionSpec(status="undeclared")

    try:
        target_f = float(target)
        tol_t = (float(tol[0]), float(tol[1]))
    except (TypeError, ValueError):
        return ProportionSpec(status="undeclared")

    landmarks = proportions.get("landmarks")
    if not isinstance(landmarks, dict):
        landmarks = None

    divisions = proportions.get("armature_divisions")
    try:
        divisions = int(divisions) if divisions is not None else None
    except (TypeError, ValueError):
        divisions = None

    return ProportionSpec(
        status="declared", target=target_f, tolerance=tol_t,
        landmarks=landmarks, armature_divisions=divisions,
    )


# ---------------------------------------------------------------------------
# Plate classification — only full-figure body turnarounds are gated
# ---------------------------------------------------------------------------


def is_body_turnaround(rel_path) -> bool:
    """True for `turnarounds/body-*.png` — the full-figure plates SF03 gates.

    Head plates (`turnarounds/head-*.png`), the anchor, expressions, props, and
    motion plates are NOT full figures, so the vertical heads-tall measurement
    does not apply; they are gate-skipped."""
    p = Path(str(rel_path)).as_posix()
    name = Path(p).name
    return "/turnarounds/" in f"/{p}" and name.startswith("body-") and name.endswith(".png")


# ---------------------------------------------------------------------------
# Vertical measurement primitives (PIL/numpy, lazy-imported like audit.py)
# ---------------------------------------------------------------------------

# Background substrate of the pencil-test-colored register (#F2E6CC). A pixel is
# "ink" when its RGB euclidean distance from cream exceeds _INK_DISTANCE. The
# cream→warm-graphite (#3D3530) distance is ~297, so a 60 floor keeps paper grain
# and JPEG ringing out of the mask while admitting faint construction lines and
# all colored fills.
_CREAM_RGB = (242, 230, 204)
_GRAPHITE_RGB = (61, 53, 48)  # #3D3530 — warm graphite line / armature ink
_INK_DISTANCE = 60.0

# A row is figure-bearing when its ink count is at least 1% of the width (de-noise
# the grain floor) AND below 90% (a row that is ~full-width ink is a printed
# armature rule, not the figure — exclude it so the figure extent reads crown/feet
# even on a gridded model-sheet). 90%+ ink rows ARE the armature.
_FIGURE_MIN_ROW_FRAC = 0.01
_ARMATURE_MIN_ROW_FRAC = 0.90


@dataclass(frozen=True)
class FigureExtent:
    """The figure's vertical extent in pixels — the one read the spikes proved
    RELIABLE (total height was stable while absolute chin detection was not).

    crown_y / feet_y are None when no figure ink is present (blank paper)."""

    crown_y: int | None
    feet_y: int | None
    height_px: int


def _row_ink_counts(path):
    """Return (height, width, per-row ink-pixel-count array) for an image.

    Lazy-imports PIL + numpy so the spec layer above stays dependency-free."""
    from PIL import Image
    import numpy as np

    img = Image.open(path).convert("RGB")
    arr = np.asarray(img, dtype=np.float32)  # (h, w, 3)
    cream = np.array(_CREAM_RGB, dtype=np.float32)
    dist = np.sqrt(((arr - cream) ** 2).sum(axis=2))  # (h, w)
    ink = dist > _INK_DISTANCE
    return ink.shape[0], ink.shape[1], ink.sum(axis=1)  # h, w, (h,)


def figure_extent(path) -> FigureExtent:
    """Measure crown (top) and feet (bottom) of the figure ink mask.

    Excludes full-width armature rules so the read tracks the FIGURE, not the
    printed grid, on a gridded model-sheet."""
    h, w, row_counts = _row_ink_counts(path)
    lo = _FIGURE_MIN_ROW_FRAC * w
    hi = _ARMATURE_MIN_ROW_FRAC * w
    figure_rows = [y for y in range(h) if lo <= row_counts[y] < hi]
    if not figure_rows:
        return FigureExtent(crown_y=None, feet_y=None, height_px=h)
    return FigureExtent(crown_y=figure_rows[0], feet_y=figure_rows[-1], height_px=h)


def detect_armature_lines(path) -> list[int]:
    """Detect printed horizontal armature rules — rows that are ~full-width ink.

    Adjacent rows (a rule a few px thick) cluster to one centroid y. Returns the
    sorted y-positions. A narrow figure bar never reaches the full-width
    threshold, so a figure-only plate returns []."""
    h, w, row_counts = _row_ink_counts(path)
    thresh = _ARMATURE_MIN_ROW_FRAC * w
    rule_rows = [y for y in range(h) if row_counts[y] >= thresh]

    lines: list[int] = []
    cluster: list[int] = []
    for y in rule_rows:
        if cluster and y == cluster[-1] + 1:
            cluster.append(y)
        else:
            if cluster:
                lines.append(int(round(sum(cluster) / len(cluster))))
            cluster = [y]
    if cluster:
        lines.append(int(round(sum(cluster) / len(cluster))))
    return lines


# ---------------------------------------------------------------------------
# Verdict — one shape across all three input modes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProportionVerdict:
    """The result of measuring one plate against a proportion spec.

    verdict: "pass" | "fail" | "indeterminate" | "error" | "skipped".
    method:  "armature" | "landmarks" | "extent_only" | "opt_out" | "none" | "error".
    heads_tall is None unless a real measurement was possible (A or B).
    division_alignment (A only) is the figure's crown/feet deviation from the
    grid's end lines, in head-units — a misalignment signal even when heads_tall
    happens to land in band.
    target / tolerance echo the spec so the verdict is self-describing on disk."""

    verdict: str
    heads_tall: float | None
    target: float | None
    tolerance: tuple[float, float] | None
    division_alignment: float | None
    method: str
    detail: str


def measure_proportion(plate_path, spec: ProportionSpec, *, armature_path=None) -> ProportionVerdict:
    """Measure one plate's head-to-body ratio against `spec`. Never raises.

    Mode is chosen by available input, NOT by which approach the probe picked —
    so the probe outcome only changes what feeds this function:
      - armature_path given  → Approach A (grid-alignment on a gridded sheet).
      - spec.landmarks given → Approach B (deterministic re-check from fractions).
      - neither              → extent_only fallback → `indeterminate` (honest
                               non-measurement; the chin read is unreliable)."""
    if spec.status == "opt_out":
        return ProportionVerdict(
            "skipped", None, None, None, None, "opt_out",
            "character opted out of SF03 (not heads-tall)",
        )
    if spec.status != "declared":
        return ProportionVerdict(
            "indeterminate", None, None, None, None, "none",
            "no numeric proportion spec declared",
        )

    target, tol = spec.target, spec.tolerance
    try:
        if armature_path is not None:
            lines = detect_armature_lines(armature_path)
            if len(lines) < 2:
                return ProportionVerdict(
                    "error", None, target, tol, None, "armature",
                    f"expected >=2 armature lines, found {len(lines)}",
                )
            ext = figure_extent(armature_path)
            if ext.crown_y is None or ext.feet_y is None:
                return ProportionVerdict(
                    "error", None, target, tol, None, "armature",
                    "no figure ink found on the gridded model-sheet",
                )
            # Anchor on the bold first/last lines (crown + feet) and the KNOWN
            # division count — NOT the detected line count. NB2 reliably keeps the
            # bold crown/feet lines but sometimes redraws the INTERIOR with a wrong
            # count (the ¾ probe: 9 lines, not 8); dividing by detected count then
            # rescales the ruler and corrupts heads_tall. Known divisions = the
            # explicit spec field or round(target).
            divisions = spec.armature_divisions or round(target)
            spacing = (lines[-1] - lines[0]) / divisions
            heads = (ext.feet_y - ext.crown_y) / spacing
            align = max(abs(ext.crown_y - lines[0]), abs(ext.feet_y - lines[-1])) / spacing
            verdict = "pass" if tol[0] <= heads <= tol[1] else "fail"
            detail = f"{heads:.2f} heads tall vs target {target} {list(tol)}"
            expected_lines = divisions + 1
            if len(lines) != expected_lines:
                # surfaced, not silently dropped — a human sees the grid drift
                detail += (
                    f" [grid line-count drift: detected {len(lines)} lines, "
                    f"expected {expected_lines}; measured via bold crown/feet anchors]"
                )
            return ProportionVerdict(
                verdict, round(heads, 3), target, tol, round(align, 3), "armature",
                detail,
            )

        if spec.landmarks:
            lm = spec.landmarks
            crown_f = float(lm["crown_frac"])
            chin_f = float(lm["chin_frac"])
            feet_f = float(lm["feet_frac"])
            head_band = chin_f - crown_f
            if head_band <= 0:
                return ProportionVerdict(
                    "error", None, target, tol, None, "landmarks",
                    "invalid landmarks (chin must sit below crown)",
                )
            heads = (feet_f - crown_f) / head_band
            verdict = "pass" if tol[0] <= heads <= tol[1] else "fail"
            return ProportionVerdict(
                verdict, round(heads, 3), target, tol, None, "landmarks",
                f"{heads:.2f} heads tall (stored landmarks) vs target {target} {list(tol)}",
            )

        # extent_only fallback — figure extent is reliable, head height is not.
        ext = figure_extent(plate_path)
        if ext.crown_y is None:
            return ProportionVerdict(
                "indeterminate", None, target, tol, None, "extent_only",
                "no figure ink found; no armature or landmarks to measure against",
            )
        return ProportionVerdict(
            "indeterminate", None, target, tol, None, "extent_only",
            "figure extent read, but head height needs a gridded armature or "
            "stored landmarks (the chin read is unreliable on its own)",
        )
    except Exception as exc:  # never crash a Bible bake — return an error verdict
        return ProportionVerdict(
            "error", None, target, tol, None, "error", str(exc)[:200],
        )


# ---------------------------------------------------------------------------
# Folder-level gate — measures every body turnaround + applies the block policy
# ---------------------------------------------------------------------------

# A verdict in this set is grounds to BLOCK a Bible-lock. `indeterminate` blocks
# on purpose: the gate refuses to certify a proportion it cannot measure (the
# honest pre-feeder state), rather than letting an un-measured plate through.
_BLOCKING_VERDICTS = frozenset({"fail", "indeterminate", "error"})


@dataclass(frozen=True)
class GateResult:
    """Aggregate of the SF03 gate over a character's body turnarounds.

    verdicts maps each body plate's relative path → its ProportionVerdict.
    blocked is True when the lock must be refused; reason is operator-facing."""

    verdicts: dict
    blocked: bool
    reason: str


def _rel_turnaround(path) -> str:
    """`turnarounds/<name>.png` from any path ending in that — robust to abs/rel."""
    p = Path(path)
    return f"{p.parent.name}/{p.name}"


def _find_armature(plate_path) -> Path | None:
    """The Approach-A seam: a gridded model-sheet lives beside the clean plate at
    `turnarounds/armature/<plate-name>.png`. Absent (the scaffold / Approach-B
    state) → None, so measurement falls to landmarks or the extent_only
    fallback. When Cy's A-feeder is wired, it writes the gridded sheet here."""
    p = Path(plate_path)
    candidate = p.parent / "armature" / p.name
    return candidate if candidate.exists() else None


def gate_body_turnarounds(character_dir) -> GateResult:
    """Measure every `turnarounds/body-*.png` and decide whether to block the lock.

    Recomputes from the committed plate pixels (and the character.yaml spec) — it
    does NOT read the ephemeral runs/{run_id}/plate_verdicts.jsonl, because the
    committed plates are the exact thing being locked."""
    character_dir = Path(character_dir)
    spec = load_proportion_spec(character_dir / "character.yaml")

    turn_dir = character_dir / "turnarounds"
    body_plates = sorted(turn_dir.glob("body-*.png")) if turn_dir.exists() else []

    # Opt-out: the human-figure armature does not transfer; never block.
    if spec.status == "opt_out":
        verdicts = {
            _rel_turnaround(p): measure_proportion(p, spec) for p in body_plates
        }
        return GateResult(verdicts=verdicts, blocked=False, reason="")

    # Undeclared: a heads-tall character with prose only. Blank folders are fine;
    # body plates present with no numeric spec is the silent-pass hole → BLOCK.
    if spec.status != "declared":
        verdicts = {
            _rel_turnaround(p): measure_proportion(p, spec) for p in body_plates
        }
        if body_plates:
            return GateResult(
                verdicts=verdicts,
                blocked=True,
                reason=(
                    f"proportion spec undeclared but {len(body_plates)} body "
                    f"turnaround(s) present — declare head_to_body_target + "
                    f"tolerance_heads in character.yaml, or set proportions.sf03: "
                    f"opt_out for a non-heads-tall character"
                ),
            )
        return GateResult(verdicts={}, blocked=False, reason="")

    # Declared: measure each body plate (armature if a gridded sheet exists, else
    # landmarks, else extent_only → indeterminate).
    verdicts = {}
    offending = []
    for p in body_plates:
        v = measure_proportion(p, spec, armature_path=_find_armature(p))
        rel = _rel_turnaround(p)
        verdicts[rel] = v
        if v.verdict in _BLOCKING_VERDICTS:
            offending.append(f"{rel} [{v.verdict}: {v.detail}]")

    if offending:
        return GateResult(
            verdicts=verdicts,
            blocked=True,
            reason="SF03 proportion gate blocks the lock — "
            + "; ".join(offending),
        )
    return GateResult(verdicts=verdicts, blocked=False, reason="")


# ---------------------------------------------------------------------------
# Cy integration — mutate a plate's status dict (mirrors _score_plate_identity)
# ---------------------------------------------------------------------------


def plate_status_fields(target_path, character_dir, status: dict, *, armature_path=None) -> None:
    """Write the sf03_* verdict fields into a Cy plate `status` dict, in place.

    Mirrors CharacterDesignerNode._score_plate_identity's contract: mutates
    status, never raises, so the fields persist through _persist_plate_verdicts
    unchanged. Only `turnarounds/body-*.png` plates are gated; everything else
    (head plates, props, expressions, motion) gets sf03_gate='skipped'. An
    opt-out character's body plate is also skipped."""
    character_dir = Path(character_dir)
    rel = _rel_turnaround(target_path)
    if not is_body_turnaround(rel):
        status["sf03_gate"] = "skipped"
        return

    spec = load_proportion_spec(character_dir / "character.yaml")
    if spec.status == "opt_out":
        status["sf03_gate"] = "skipped"
        status["sf03_verdict"] = "opt_out"
        return

    if armature_path is None:
        armature_path = _find_armature(target_path)
    v = measure_proportion(target_path, spec, armature_path=armature_path)
    status["sf03_gate"] = "hard"
    status["sf03_verdict"] = v.verdict
    status["sf03_heads_tall"] = v.heads_tall
    status["sf03_target"] = v.target
    status["sf03_tolerance"] = list(v.tolerance) if v.tolerance else None
    status["sf03_division_alignment"] = v.division_alignment
    status["sf03_method"] = v.method


# ---------------------------------------------------------------------------
# Approach-A feeder — the deterministic armature + the gridded-model-sheet emit
# ---------------------------------------------------------------------------


def build_armature_underlay(
    path, *, divisions: int = 7, size: tuple[int, int] = (768, 1024), margin: int = 64
):
    """Write the canonical heads-tall armature underlay: a cream canvas with
    `divisions + 1` full-width graphite lines (crown=0 .. feet=divisions), crown
    and feet bolded so NB2's redraw keeps the load-bearing anchors. This is the
    one canonical armature the probe used, Cy's feeder generates against, and the
    gate measures — promoted here so all three share it. Deterministic, $0."""
    from PIL import Image, ImageDraw

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    w, h = size
    top, bot = margin, h - margin
    img = Image.new("RGB", (w, h), _CREAM_RGB)
    d = ImageDraw.Draw(img)
    for i in range(divisions + 1):
        y = top + round(i * (bot - top) / divisions)
        thick = 4 if i in (0, divisions) else 2  # bold crown + feet anchors
        d.rectangle([0, y - thick // 2, w - 1, y + thick // 2], fill=_GRAPHITE_RGB)
    img.save(path)
    return path


_GRIDDED_SHEET_PROMPT = (
    "The FIRST image is a proportion armature: {lines} evenly spaced horizontal "
    "lines dividing the canvas into {divisions} equal head-height bands (the "
    "heroic 1:{divisions} ladder), with the top and bottom lines bolded. The "
    "SECOND image is a finished pencil-test character turnaround. Redraw that same "
    "character — identical identity, pose, view, outfit, and pencil-test style — "
    "seated strictly to the armature: crown of the head exactly ON the top line, "
    "soles of the feet exactly ON the bottom line, head (crown to chin) filling "
    "the single top band. Keep ALL {lines} horizontal guide lines clearly visible "
    "through and behind the figure. Cream paper, warm-graphite line. Add no text."
)


def emit_gridded_model_sheet(clean_plate, character_dir, *, cache_dir, divisions: int | None = None):
    """Approach-A feeder: generate the gridded model-sheet (the verification
    artifact) from a clean body turnaround, and write it where _find_armature
    looks — `turnarounds/armature/<plate-name>.png`. The clean Bible plate is
    untouched; the gridded sheet is a SEPARATE artifact (two-artifacts design).

    Generation goes through the module-level invoke_image_edit (NB2 Flash);
    tests monkeypatch it. Returns the gridded-sheet path (which may be a stub
    placeholder if no API key — the gate then reads it as error/indeterminate,
    never a faked pass)."""
    clean_plate = Path(clean_plate)
    character_dir = Path(character_dir)
    spec = load_proportion_spec(character_dir / "character.yaml")
    n = divisions or spec.armature_divisions or (round(spec.target) if spec.target else 7)

    armature_dir = clean_plate.parent / "armature"
    armature_dir.mkdir(parents=True, exist_ok=True)
    underlay = build_armature_underlay(armature_dir / "_underlay.png", divisions=n)
    out = armature_dir / clean_plate.name

    if invoke_image_edit is None:  # pragma: no cover - runner unavailable
        return out
    invoke_image_edit(
        prompt=_GRIDDED_SHEET_PROMPT.format(divisions=n, lines=n + 1),
        reference_images=[underlay, clean_plate],
        output_path=out,
        cache_dir=Path(cache_dir),
    )
    return out
