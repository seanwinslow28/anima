"""anima — `pipeline bible {init|show|approve|mutate|iterate}` subcommands.

Per Cy brainstorm TOP-4. Mirrors pipeline/cli/plan.py structurally — the
renderer lives in the CLI layer (boxes, palette swatches, ANSI color blocks);
Cy writes clean prose on disk. Downstream consumers (Em, Sage, the chairman,
Mo the museum writer) read clean markdown directly.

The five subcommands:

  init      Scaffold the character folder structure and copy templates.
            Idempotent — re-running won't overwrite existing files.

  show      Render the Bible as a terminal tear sheet: character header,
            palette swatch line, identity rules grouped by category, motion
            plate inventory, risk-bible callouts, Cy's confidence hedges.
            Reads character.yaml + acceptance_criteria.json + risk-bible.md +
            cy-confidence-notes.md from the character folder.

  approve   Flip locked=true on the character's acceptance_criteria.json.
            Idempotent. After approval, IR.* rules lock; mutation requires
            --force --actor --reason.

  mutate    Audited mutation of an approved Bible. Refuses without --force.
            Bumps the criteria file's semver, re-points the symlink, and
            appends one JSONL line to runs/{run_id}/bible_audit.jsonl.

  iterate   Re-run Cy narrowed to rejected plates. Cy's nb_pro_runner cache
            key encodes the reject_reason, so the rejected plates regenerate
            fresh while the cached plates that passed Pass 3 stay untouched.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from pipeline.criteria import validate_criteria

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates" / "bible"

# Six top-level subdirectories every Bible folder has. Mirrors the brainstorm
# TOP-1 schema — anchor + turnarounds + expressions + motion_plates (with
# source/derived split) + costumes + props + source-refs.
_BIBLE_SUBDIRS = (
    "turnarounds",
    "expressions",
    "motion_plates/walk-cycle/source",
    "motion_plates/walk-cycle/derived",
    "motion_plates/head-turn/source",
    "motion_plates/head-turn/derived",
    "costumes/default",
    "props",
    "source-refs/3d-mannequin",
)


# ---------------------------------------------------------------------------
# `bible init` — scaffold a new character folder
# ---------------------------------------------------------------------------


def init_bible(target: str) -> int:
    """Scaffold a character folder. Copies the two anchored templates.

    Idempotent: subdirectories that already exist are left alone; template
    files that already exist are not overwritten.
    """
    target_path = Path(target)
    target_path.mkdir(parents=True, exist_ok=True)

    for sub in _BIBLE_SUBDIRS:
        (target_path / sub).mkdir(parents=True, exist_ok=True)

    if not TEMPLATES_DIR.exists():
        print(f"error: templates/bible/ not found at {TEMPLATES_DIR}", file=sys.stderr)
        return 1

    created: list[Path] = []
    skipped: list[Path] = []

    char_yaml_src = TEMPLATES_DIR / "character.yaml.template"
    char_yaml_dst = target_path / "character.yaml"
    if char_yaml_dst.exists():
        skipped.append(char_yaml_dst)
    else:
        shutil.copy2(char_yaml_src, char_yaml_dst)
        created.append(char_yaml_dst)

    checklist_src = TEMPLATES_DIR / "source-refs-checklist.md"
    checklist_dst = target_path / "source-refs" / "0-sean-author-this.md"
    if checklist_dst.exists():
        skipped.append(checklist_dst)
    else:
        shutil.copy2(checklist_src, checklist_dst)
        created.append(checklist_dst)

    print(f"scaffolded bible folder at {target_path}")
    for c in created:
        print(f"  created: {c.relative_to(target_path)}")
    for s in skipped:
        print(f"  (existing, untouched: {s.relative_to(target_path)})")
    print(
        f"\nnext: drop source material per source-refs/0-sean-author-this.md, "
        f"then invoke Cy to author the Bible."
    )
    return 0


# ---------------------------------------------------------------------------
# `bible show` — render the Bible as a terminal tear sheet
# ---------------------------------------------------------------------------


def show_bible(character_dir: str) -> int:
    """Render the Bible at character_dir as an ANSI-decorated tear sheet."""
    cd = Path(character_dir)
    if not cd.exists():
        print(f"error: character folder not found at {cd}", file=sys.stderr)
        return 1
    rendered = render_bible_tear_sheet(cd)
    print(rendered)
    return 0


def render_bible_tear_sheet(character_dir: Path) -> str:
    """Pure function: character folder in, tear-sheet string out.

    Extracted from show_bible() so tests can assert against the rendered
    string without subprocess invocation. The renderer reads from disk but
    does not mutate any artifact — `bible show` is read-only by design.
    """
    char_yaml_path = character_dir / "character.yaml"
    criteria_path = character_dir / "acceptance_criteria.json"
    risk_bible_path = character_dir / "risk-bible.md"
    confidence_notes_path = character_dir / "cy-confidence-notes.md"

    sections: list[str] = []

    char_yaml: dict = {}
    if char_yaml_path.exists():
        try:
            char_yaml = yaml.safe_load(char_yaml_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            char_yaml = {}

    sections.append(_render_header(char_yaml, character_dir))
    sections.append(_render_palette_swatch(char_yaml))
    sections.append(_render_proportions(char_yaml))

    criteria_payload: dict = {}
    if criteria_path.exists():
        try:
            criteria_payload = json.loads(criteria_path.read_text(encoding="utf-8")) or {}
        except json.JSONDecodeError:
            criteria_payload = {}
    sections.append(_render_identity_rules(criteria_payload))

    sections.append(_render_motion_plate_inventory(character_dir))

    if risk_bible_path.exists():
        sections.append(_render_prose_block(
            "Risks (Cy's negative space)",
            risk_bible_path.read_text(encoding="utf-8"),
        ))

    if confidence_notes_path.exists():
        sections.append(_render_prose_block(
            "Cy's confidence hedges",
            confidence_notes_path.read_text(encoding="utf-8"),
        ))

    return "\n\n".join(s for s in sections if s.strip())


def _render_header(char_yaml: dict, character_dir: Path) -> str:
    display = char_yaml.get("display_name") or character_dir.name
    cid = char_yaml.get("character_id") or character_dir.name
    register = char_yaml.get("style_register") or "(unset)"
    locked_marker = ""
    criteria_path = character_dir / "acceptance_criteria.json"
    if criteria_path.exists():
        try:
            payload = json.loads(criteria_path.read_text(encoding="utf-8"))
            locked_marker = " — LOCKED" if payload.get("locked") else " — draft"
        except json.JSONDecodeError:
            pass

    title = f"{display} [{cid}, {register}{locked_marker}]"
    width = max(50, len(title) + 4)
    top = "┌" + "─" * (width - 2) + "┐"
    mid = "│ " + title.center(width - 4) + " │"
    bot = "└" + "─" * (width - 2) + "┘"
    return "\n".join([top, mid, bot])


def _render_palette_swatch(char_yaml: dict) -> str:
    palette = char_yaml.get("palette") or []
    if not palette:
        return "## Palette\n\n(no palette entries authored)"
    lines = ["## Palette", ""]
    for entry in palette:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name", "?")
        hexstr = entry.get("hex", "")
        role = entry.get("role", "")
        swatch = _ansi_swatch(hexstr)
        lines.append(f"  {swatch}  {hexstr:<10}  {name:<24}  {role}")
    return "\n".join(lines)


def _ansi_swatch(hex_color: str) -> str:
    """Two-block ANSI background swatch for a hex color.

    Falls back to a placeholder if the hex is empty or unparsable so the
    show command never breaks because of malformed palette data.
    """
    h = (hex_color or "").lstrip("#")
    if len(h) != 6:
        return "[????]"
    try:
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
    except ValueError:
        return "[????]"
    # 24-bit ANSI background. Two spaces per block × two blocks → a small
    # color tile that reads on most terminals; falls back to literal text on
    # terminals that swallow the escapes (e.g., CI logs).
    return f"\x1b[48;2;{r};{g};{b}m    \x1b[0m"


def _render_proportions(char_yaml: dict) -> str:
    p = char_yaml.get("proportions") or {}
    if not p:
        return ""
    h_to_b = p.get("head_to_body") or "(unset)"
    s_to_h = p.get("shoulder_to_hip") or "(unset)"
    notes = (p.get("notes") or "").strip()
    block = [
        "## Proportions",
        "",
        f"  head_to_body:    {h_to_b}",
        f"  shoulder_to_hip: {s_to_h}",
    ]
    if notes:
        block.append("")
        block.append(f"  notes: {notes}")
    return "\n".join(block)


def _render_identity_rules(criteria_payload: dict) -> str:
    criteria = criteria_payload.get("criteria") or []
    if not criteria:
        return "## Identity rules\n\n(no IR.* entries authored)"
    grouped: dict[str, list[dict]] = {}
    for entry in criteria:
        cid = entry.get("id", "")
        if not cid.startswith("IR."):
            continue
        # IR.{character_id}.{category}.{handle}
        parts = cid.split(".")
        category = parts[2] if len(parts) >= 4 else "_unknown"
        grouped.setdefault(category, []).append(entry)

    if not grouped:
        return "## Identity rules\n\n(no IR.* entries — Bible only carries AC.* criteria)"

    lines = ["## Identity rules", ""]
    for category in sorted(grouped):
        lines.append(f"### {category}")
        lines.append("")
        for entry in grouped[category]:
            cid = entry.get("id", "")
            description = (entry.get("description") or "").strip()
            impact = entry.get("impact_tag") or "(no impact tag)"
            derived = entry.get("derived_from") or []
            lines.append(f"  - **{cid}** ({impact})")
            if description:
                lines.append(f"      {description}")
            if derived:
                for d in derived:
                    lines.append(f"      derived: {d}")
            lines.append("")
    return "\n".join(lines).rstrip()


def _render_motion_plate_inventory(character_dir: Path) -> str:
    motion_root = character_dir / "motion_plates"
    if not motion_root.exists():
        return ""
    lines = ["## Motion plates"]
    found_any = False
    for category in sorted(p for p in motion_root.iterdir() if p.is_dir()):
        source_dir = category / "source"
        derived_dir = category / "derived"
        source_count = len(list(source_dir.glob("*.*"))) if source_dir.exists() else 0
        derived_count = len(list(derived_dir.glob("*.*"))) if derived_dir.exists() else 0
        if source_count == 0 and derived_count == 0:
            continue
        found_any = True
        lines.append("")
        lines.append(
            f"  {category.name}: {source_count} source / {derived_count} derived"
        )
    if not found_any:
        lines.append("")
        lines.append("  (no motion plates present yet)")
    return "\n".join(lines)


def _render_prose_block(heading: str, body: str) -> str:
    return f"## {heading}\n\n{body.strip()}"


# ---------------------------------------------------------------------------
# `bible approve` — flip locked=true on the character's criteria file
# ---------------------------------------------------------------------------


def approve_bible(character_dir: str) -> int:
    """Flip locked=true on the character's acceptance_criteria.json.

    Idempotent. The Bible's criteria file is a regular file; resolve() is a
    no-op for it but kept so a legacy symlinked file (from the retired
    bump_version path) still has locked=true written through to its target.
    """
    cd = Path(character_dir)
    criteria_path = cd / "acceptance_criteria.json"
    if not criteria_path.exists():
        print(f"error: criteria file not found at {criteria_path}", file=sys.stderr)
        return 1
    target = criteria_path.resolve()
    raw = json.loads(target.read_text(encoding="utf-8"))
    if raw.get("locked"):
        print(f"already locked: {criteria_path} (no-op)")
        return 0
    raw["locked"] = True
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    tmp.replace(target)
    print(f"approved: locked=true on {target}")
    if criteria_path != target:
        print(f"  symlink: {criteria_path} -> {target.name}")
    return 0


# ---------------------------------------------------------------------------
# `bible mutate` — audited mutation of an approved Bible
# ---------------------------------------------------------------------------


def mutate_bible(
    *,
    run_dir: str,
    character_dir: str,
    force: bool,
    actor: str,
    reason: str,
    target: str,
    field: str,
    value: str,
    content_version: str | None = None,
) -> int:
    """Audited mutation of an approved Bible. Refuses without --force.

    Edits the rule content in place and keeps the schema `version` field
    untouched (the loader gates `version` on a 1.0/1.1/1.2 allowlist — a
    content semver written there makes the Bible unloadable; that was the
    2026-05-30 §4 break). A content revision, if supplied, is recorded in a
    separate top-level `content_version` field that the loader ignores.

    On success:
      1. Sets criteria[<id == target>][field] = value, re-validates, writes
         the file back in place (resolved-path atomic write, no symlink).
      2. Records content_version if provided.
      3. Appends one JSONL line to runs/{run_id}/bible_audit.jsonl.
    """
    if not force:
        print(
            "error: bible mutate refuses to run without --force.\n"
            "       Pass --force --actor <name> --reason \"<rationale>\"\n"
            "       to audited-override the locked criteria file.",
            file=sys.stderr,
        )
        return 1
    if not actor or not reason:
        print(
            "error: --force requires both --actor and --reason.",
            file=sys.stderr,
        )
        return 1

    cd = Path(character_dir)
    rd = Path(run_dir)
    criteria_path = cd / "acceptance_criteria.json"
    if not criteria_path.exists():
        print(f"error: criteria file not found at {criteria_path}", file=sys.stderr)
        return 1

    resolved = criteria_path.resolve()
    current = json.loads(resolved.read_text(encoding="utf-8"))
    schema_version = str(current.get("version", "1.2"))
    old_content_version = current.get("content_version")

    matched = [c for c in current.get("criteria", []) if c.get("id") == target]
    if not matched:
        print(
            f"error: no criterion with id {target!r} in {criteria_path}. "
            f"mutate edits an existing rule's field; check the --target id.",
            file=sys.stderr,
        )
        return 1
    old_value = matched[0].get(field)
    matched[0][field] = value

    if content_version is not None:
        current["content_version"] = content_version

    # Re-validate before writing so a mutate can never persist an invalid graph.
    validate_criteria(current)

    tmp = resolved.with_suffix(resolved.suffix + ".tmp")
    tmp.write_text(json.dumps(current, indent=2), encoding="utf-8")
    tmp.replace(resolved)

    rd.mkdir(parents=True, exist_ok=True)
    audit_path = rd / "bible_audit.jsonl"
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "actor": actor,
        "reason": reason,
        "character_dir": str(cd),
        "target": target,
        "field": field,
        "old_value": old_value,
        "value": value,
        "schema_version": schema_version,
        "content_version_from": old_content_version,
        "content_version_to": content_version,
        "criteria_path": str(resolved),
    }
    with audit_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    print(f"mutated: {target}.{field} = {value!r}")
    if content_version is not None:
        print(
            f"  content_version: {old_content_version} -> {content_version} "
            f"(schema stays {schema_version})"
        )
    print(f"  audit:    appended to {audit_path}")
    return 0


# ---------------------------------------------------------------------------
# `bible iterate` — re-run Cy narrowed to rejected plates
# ---------------------------------------------------------------------------


def iterate_bible(
    *,
    character_dir: str,
    targets: list[str],
    rejected: list[str],
    reason: str,
    run_dir: str | None = None,
) -> int:
    """Re-run Cy narrowed to rejected plates.

    `targets` is the high-level plate-category list (turnarounds /
    expressions / motion_plates / ...); `rejected` is the specific plate
    handles to regenerate (e.g., 'angry', 'surprised'). Cached plates that
    passed Pass 3 stay untouched; the reject_reason invalidates the cache
    key on the rejected plates so NB Pro regenerates fresh.

    The actual re-run requires AgentContext + the SDK runtime; for the
    Bible workflow today this command prepares the narrowed plate plan and
    threads the reject_reason into the runner. When Cy is invoked from a
    Maya bible_authoring run, the same narrowing logic applies in-process.
    """
    cd = Path(character_dir)
    plan_path = cd / "plate_generation_plan.json"
    if not plan_path.exists():
        print(
            f"error: plate plan not found at {plan_path}; "
            f"iterate requires a previously-authored Bible.",
            file=sys.stderr,
        )
        return 1
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"error: plate plan at {plan_path} is malformed: {exc}", file=sys.stderr)
        return 1

    target_set = set(targets) if targets else set()
    rejected_set = set(rejected) if rejected else set()

    narrowed: list[dict] = []
    preserved: list[dict] = []
    for plate in plan.get("plates", []):
        path = str(plate.get("target_path", ""))
        category = path.split("/", 1)[0] if "/" in path else path
        handle = Path(path).stem
        if target_set and category not in target_set:
            preserved.append(plate)
            continue
        if rejected_set and handle not in rejected_set and not any(
            r in path for r in rejected_set
        ):
            preserved.append(plate)
            continue
        narrowed.append({**plate, "reject_reason": reason})

    if not narrowed:
        print(
            f"no plates matched the narrowing (targets={targets!r}, rejected={rejected!r}); "
            f"nothing to iterate.",
            file=sys.stderr,
        )
        return 1

    narrowed_plan = {**plan, "plates": narrowed}
    iterate_plan_path = cd / "plate_generation_plan_iterate.json"
    tmp = iterate_plan_path.with_suffix(iterate_plan_path.suffix + ".tmp")
    tmp.write_text(json.dumps(narrowed_plan, indent=2), encoding="utf-8")
    tmp.replace(iterate_plan_path)

    if run_dir:
        rd = Path(run_dir)
        rd.mkdir(parents=True, exist_ok=True)
        audit_path = rd / "bible_audit.jsonl"
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "actor": os.environ.get("USER", "unknown"),
            "kind": "iterate",
            "character_dir": str(cd),
            "targets": targets,
            "rejected": rejected,
            "reason": reason,
            "narrowed_count": len(narrowed),
            "preserved_count": len(preserved),
        }
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    print(
        f"iterate prepared: {len(narrowed)} plate(s) staged for regeneration, "
        f"{len(preserved)} preserved (cache hits).\n"
        f"  narrowed plan written to {iterate_plan_path}\n"
        f"  next: invoke CharacterDesignerNode with this narrowed plan."
    )
    return 0
