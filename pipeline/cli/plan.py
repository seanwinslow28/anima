"""anima — `pipeline plan {init|show|approve|mutate}` subcommands.

Per Maya brainstorm TOP-1 + TOP-4. Mirrors pipeline/cli/patches.py structurally.

`plan show` is the rendering layer. Maya emits plan.md as clean markdown (no
box-drawing characters, zero Opus tokens spent on terminal aesthetics);
`plan show` post-processes the load-bearing sections into ASCII box-decorated
views using plain Python string ops. Downstream consumers (Cy, Em, Sage, the
chairman, Mo the museum writer) read clean markdown directly — the box
rendering is a presentation concern, not an artifact concern.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from pipeline.criteria import bump_version

# templates/brief/ at the repo root.
TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates" / "brief"

# Sections rendered with ASCII boxes in `plan show`. The rest stays as
# plain markdown so the section structure isn't lost when scanning. Matched
# case-insensitively against the H2 heading text.
_BOX_SECTIONS = frozenset({
    "cost preview",
    "criteria summary",
    "character box",
    "beat strip",
    "routing legend",
})


# ---------------------------------------------------------------------------
# `plan init` — scaffold a new brief directory
# ---------------------------------------------------------------------------


def init_plan(target: str) -> int:
    """Copy both anchored templates into the target directory."""
    target_path = Path(target)
    target_path.mkdir(parents=True, exist_ok=True)

    if not TEMPLATES_DIR.exists():
        print(f"error: templates/brief/ not found at {TEMPLATES_DIR}", file=sys.stderr)
        return 1

    created = []
    skipped = []
    for name in ("00_studio_brief.md", "01_production_brief.md"):
        src = TEMPLATES_DIR / name
        dst = target_path / name
        if dst.exists():
            skipped.append(dst)
            continue
        shutil.copy2(src, dst)
        created.append(dst)

    if created:
        print(f"scaffolded brief directory at {target_path}")
        for c in created:
            print(f"  created: {c.relative_to(target_path.parent)}")
    if skipped:
        print(f"  (existing, untouched: {len(skipped)} file(s))")
    print(f"\nnext: fill in 00_studio_brief.md, then run `python -m pipeline.cli plan ...`")
    return 0


# ---------------------------------------------------------------------------
# `plan show` — render plan.md as a terminal tear sheet with ASCII boxes
# ---------------------------------------------------------------------------


def show_plan(plan_path: str) -> int:
    """Render plan.md with ASCII-box-decorated load-bearing sections."""
    plan = Path(plan_path)
    if not plan.exists():
        print(f"error: plan not found at {plan}", file=sys.stderr)
        return 1
    md = plan.read_text(encoding="utf-8")
    rendered = render_plan_markdown(md)
    print(rendered)
    return 0


def render_plan_markdown(md: str) -> str:
    """Pure function: clean markdown in, ASCII-box-decorated string out.

    Extracted from show_plan() so tests can assert against the rendered
    string without subprocess invocation. The source markdown is not
    mutated — the rendering only adds box decoration to terminal output.
    """
    sections = _parse_markdown_sections(md)
    lines: list[str] = []
    if sections["title"]:
        lines.append(_render_header(sections["title"]))
        lines.append("")
    for heading, body in sections["sections"]:
        if heading.lower() in _BOX_SECTIONS:
            lines.append(_render_box(heading, body))
        else:
            lines.append(_render_plain(heading, body))
        lines.append("")
    return "\n".join(lines)


def _render_box(heading: str, body: str) -> str:
    body_lines = [ln for ln in body.strip().split("\n") if ln.strip()]
    if not body_lines:
        body_lines = ["(empty)"]
    width = max((len(line) for line in body_lines), default=0)
    width = max(width, len(heading) + 4, 40)
    top = "╔" + "═" * (width + 2) + "╗"
    title = "║ " + heading.ljust(width) + " ║"
    sep = "╠" + "═" * (width + 2) + "╣"
    body_rendered = ["║ " + line.ljust(width) + " ║" for line in body_lines]
    bottom = "╚" + "═" * (width + 2) + "╝"
    return "\n".join([top, title, sep] + body_rendered + [bottom])


def _render_plain(heading: str, body: str) -> str:
    return f"## {heading}\n\n{body.strip()}\n"


def _render_header(title: str) -> str:
    width = max(50, len(title) + 4)
    top = "┌" + "─" * (width - 2) + "┐"
    mid = "│ " + title.center(width - 4) + " │"
    bot = "└" + "─" * (width - 2) + "┘"
    return "\n".join([top, mid, bot])


def _parse_markdown_sections(md: str) -> dict:
    """Split markdown into {title, sections: [(heading, body), ...]} by H2."""
    lines = md.split("\n")
    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    sections: list[tuple[str, str]] = []
    current_heading: str | None = None
    current_body: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if current_heading is not None:
                sections.append((current_heading, "\n".join(current_body)))
            current_heading = line[3:].strip()
            current_body = []
        elif current_heading is not None:
            current_body.append(line)
    if current_heading is not None:
        sections.append((current_heading, "\n".join(current_body)))
    return {"title": title, "sections": sections}


# ---------------------------------------------------------------------------
# `plan approve` — flip criteria_locked: true on the criteria file
# ---------------------------------------------------------------------------


def approve_plan(brief_dir: str) -> int:
    """Flip locked=true on the brief's acceptance_criteria.json.

    The brief's criteria file may be a direct file or a symlink (Maya
    brainstorm TOP-4 — the semver-bumped pattern symlinks
    acceptance_criteria.json → acceptance_criteria-1.1.0.json). Either way,
    locked=true gets written through.
    """
    bd = Path(brief_dir)
    criteria_path = bd / "acceptance_criteria.json"
    if not criteria_path.exists():
        print(f"error: criteria file not found at {criteria_path}", file=sys.stderr)
        return 1
    # Resolve symlinks before mutation so we write to the versioned file.
    target = criteria_path.resolve()
    raw = json.loads(target.read_text(encoding="utf-8"))
    if raw.get("locked"):
        print(f"already locked: {criteria_path} (no-op)")
        return 0
    raw["locked"] = True
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    tmp.replace(target)
    print(f"approved: criteria_locked=true on {target}")
    print(f"  symlink: {criteria_path} -> {target.name}")
    return 0


# ---------------------------------------------------------------------------
# `plan mutate` — audited mutation of an approved plan
# ---------------------------------------------------------------------------


def mutate_plan(
    *,
    run_dir: str,
    brief_dir: str,
    force: bool,
    actor: str,
    reason: str,
    target: str,
    field: str,
    value: str,
    new_version: str,
) -> int:
    """Audited mutation of an approved plan.

    Refuses to run without --force. On success:
      1. Bumps the criteria file to new_version via pipeline.criteria.bump_version
         (the symlink at acceptance_criteria.json re-points to the new file).
      2. Writes one JSONL line to runs/{run_id}/plan_audit.jsonl with the
         mutation record (atomic append).
      3. Prepends a delta block to plan.md naming the change.
    """
    if not force:
        print(
            "error: plan mutate refuses to run without --force.\n"
            "       Pass --force --actor <name> --reason \"<rationale>\"\n"
            "       to audited-override the criteria_locked: true flag.",
            file=sys.stderr,
        )
        return 1
    if not actor or not reason:
        print(
            "error: --force requires both --actor and --reason.",
            file=sys.stderr,
        )
        return 1

    bd = Path(brief_dir)
    rd = Path(run_dir)
    criteria_path = bd / "acceptance_criteria.json"
    if not criteria_path.exists():
        print(f"error: criteria file not found at {criteria_path}", file=sys.stderr)
        return 1

    current = json.loads(criteria_path.resolve().read_text(encoding="utf-8"))
    old_version = str(current.get("version", "1.0"))

    new_versioned_path = bump_version(criteria_path, new_version=new_version)

    rd.mkdir(parents=True, exist_ok=True)
    audit_path = rd / "plan_audit.jsonl"
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "actor": actor,
        "reason": reason,
        "target": target,
        "field": field,
        "value": value,
        "criteria_version_from": old_version,
        "criteria_version_to": new_version,
        "criteria_path": str(new_versioned_path),
    }
    with audit_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    plan_path = bd / "plan.md"
    if plan_path.exists():
        _prepend_delta_block(plan_path, record)

    print(f"mutated: {target}.{field} = {value!r}")
    print(f"  criteria: {old_version} -> {new_version} (new file: {new_versioned_path.name})")
    print(f"  audit:    appended to {audit_path}")
    return 0


def _prepend_delta_block(plan_path: Path, record: dict) -> None:
    """Prepend a '## Plan changes since approval' block to plan.md.

    Idempotent count: re-prepending bumps the parenthetical (N) counter so
    Sean can see how many mutations have landed against the approved plan
    without reading the audit log.
    """
    existing = plan_path.read_text(encoding="utf-8")
    delta_count = _existing_delta_count(existing) + 1
    block = (
        f"## Plan changes since approval ({delta_count})\n\n"
        f"- **{record['ts']}** — {record['actor']}: {record['reason']}\n"
        f"  - target: `{record['target']}.{record['field']}` = `{record['value']}`\n"
        f"  - criteria: {record['criteria_version_from']} → {record['criteria_version_to']}\n\n"
        f"---\n\n"
    )

    # Insert after the H1 title if present, otherwise prepend.
    title_match = re.match(r"^(# .+\n+)", existing)
    if title_match:
        prefix = existing[: title_match.end()]
        rest = existing[title_match.end():]
        # Strip any prior delta block so we don't accumulate stale copies.
        rest_stripped = re.sub(
            r"## Plan changes since approval \(\d+\).*?---\n\n",
            "",
            rest,
            count=1,
            flags=re.DOTALL,
        )
        new = prefix + block + rest_stripped
    else:
        rest_stripped = re.sub(
            r"^## Plan changes since approval \(\d+\).*?---\n\n",
            "",
            existing,
            count=1,
            flags=re.DOTALL,
        )
        new = block + rest_stripped

    tmp = plan_path.with_suffix(plan_path.suffix + ".tmp")
    tmp.write_text(new, encoding="utf-8")
    tmp.replace(plan_path)


def _existing_delta_count(plan_md: str) -> int:
    match = re.search(r"## Plan changes since approval \((\d+)\)", plan_md)
    if match:
        return int(match.group(1))
    return 0
