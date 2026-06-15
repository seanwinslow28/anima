"""anima — `pipeline script {init|show|approve|mutate}` subcommands (Sam).

Mirrors pipeline/cli/plan.py structurally. Sam operates on beats.json (the
Sam→Bea contract) instead of acceptance_criteria.json:

  - `init`    scaffolds a beats.json template + script.md stub (idempotent).
  - `show`    renders beats.json as a terminal tear sheet — boxes live in the
              renderer (this file); beats.json on disk stays clean (Maya's rule).
  - `approve` flips `locked: true` on beats.json, idempotent (mirrors plan approve).
  - `mutate`  audited force-flag edit of one beat field → script_audit.jsonl
              (mirrors plan mutate).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Reuse plan.py's stable box-rendering primitives (DRY — same tear-sheet look).
from pipeline.cli.plan import _render_box, _render_header

_STRIP_WIDTH = 76  # truncate long beat lines in the strip for terminal scanning


# ---------------------------------------------------------------------------
# `script init` — scaffold a beats.json template + script.md stub
# ---------------------------------------------------------------------------

_BEATS_TEMPLATE = {
    "slug": "REPLACE-ME",
    "logline": "Author via: python scripts/author_script.py <brief-dir> --run-dir ...",
    "locked": False,
    "beats": [
        {
            "id": 1,
            "title": "TODO",
            "intent": "TODO — what does this beat do in the story?",
            "emotional_beat": "TODO",
            "cast": [],
            "feel": "",
            "notes": "",
        }
    ],
}

_SCRIPT_STUB = (
    "# Script\n\n"
    "Authored by Sam (the Phase-3a scriptwriter). To author for real, run:\n\n"
    "    python scripts/author_script.py <brief-dir> --run-dir runs/<id> --manifest manifest.yaml\n\n"
    "This stub is a placeholder; author_script.py overwrites it with the treatment.\n"
)


def init_script(target: str) -> int:
    """Scaffold beats.json + script.md into the target dir. Idempotent."""
    target_path = Path(target)
    target_path.mkdir(parents=True, exist_ok=True)

    created, skipped = [], []
    plan_files = {
        "beats.json": json.dumps(_BEATS_TEMPLATE, indent=2) + "\n",
        "script.md": _SCRIPT_STUB,
    }
    for name, content in plan_files.items():
        dst = target_path / name
        if dst.exists():
            skipped.append(dst)
            continue
        dst.write_text(content, encoding="utf-8")
        created.append(dst)

    if created:
        print(f"scaffolded script artifacts at {target_path}")
        for c in created:
            print(f"  created: {c.relative_to(target_path.parent)}")
    if skipped:
        print(f"  (existing, untouched: {len(skipped)} file(s))")
    print("\nnext: author with scripts/author_script.py, then `script show` / `script approve`.")
    return 0


# ---------------------------------------------------------------------------
# `script show` — render beats.json as a terminal tear sheet
# ---------------------------------------------------------------------------


def show_script(beats_path: str) -> int:
    """Render beats.json with ASCII-box-decorated sections."""
    p = Path(beats_path)
    if not p.exists():
        print(f"error: beats file not found at {p}", file=sys.stderr)
        return 1
    try:
        rendered = render_beats(p.read_text(encoding="utf-8"))
    except (ValueError, json.JSONDecodeError) as e:
        print(f"error: {p} is not parseable beats.json: {e}", file=sys.stderr)
        return 1
    print(rendered)
    return 0


def render_beats(beats_json: str) -> str:
    """Pure function: beats.json text in, ASCII-box tear sheet out.

    Boxes live here (terminal presentation only); beats.json on disk stays clean
    machine JSON. Extracted so tests assert the rendered string without a
    subprocess.
    """
    data = json.loads(beats_json)
    slug = str(data.get("slug", "(no slug)"))
    logline = str(data.get("logline", ""))
    locked = bool(data.get("locked", False))
    beats = data.get("beats", []) or []

    lines: list[str] = [
        _render_header(f"{slug}  —  {'LOCKED' if locked else 'draft'}  ({len(beats)} beats)"),
        "",
    ]
    if logline:
        lines.append(_render_box("Logline", logline))
        lines.append("")

    strip: list[str] = []
    for b in beats:
        cast = ", ".join(str(c) for c in (b.get("cast") or []))
        strip.append(_clip(f"[{b.get('id')}] {b.get('title', '')}  ({b.get('emotional_beat', '')})"))
        strip.append(_clip(f"      intent: {b.get('intent', '')}"))
        strip.append(_clip(f"      cast:   {cast}"))
        if b.get("feel"):
            strip.append(_clip(f"      feel:   {b['feel']}"))
        if b.get("notes"):
            strip.append(_clip(f"      notes:  {b['notes']}"))
    lines.append(_render_box("Beat strip", "\n".join(strip) if strip else "(no beats)"))
    return "\n".join(lines)


def _clip(s: str) -> str:
    return s if len(s) <= _STRIP_WIDTH else s[: _STRIP_WIDTH - 1] + "…"


# ---------------------------------------------------------------------------
# `script approve` — flip locked: true on beats.json
# ---------------------------------------------------------------------------


def approve_script(brief_dir: str) -> int:
    """Flip locked=true on the brief's beats.json. Mirrors plan approve.

    The file may be a direct file or a symlink; locked=true is written through
    to the resolved target. Idempotent — a second call is a no-op.
    """
    bd = Path(brief_dir)
    beats_path = bd / "beats.json"
    if not beats_path.exists():
        print(f"error: beats file not found at {beats_path}", file=sys.stderr)
        return 1
    target = beats_path.resolve()
    raw = json.loads(target.read_text(encoding="utf-8"))
    if raw.get("locked"):
        print(f"already locked: {beats_path} (no-op)")
        return 0
    raw["locked"] = True
    _atomic_write(target, json.dumps(raw, indent=2))
    print(f"approved: locked=true on {target}")
    return 0


# ---------------------------------------------------------------------------
# `script mutate` — audited mutation of one beat field
# ---------------------------------------------------------------------------


def mutate_script(
    *,
    run_dir: str,
    brief_dir: str,
    force: bool,
    actor: str,
    reason: str,
    target: str,
    field: str,
    value: str,
) -> int:
    """Audited edit of one beat's field. Mirrors plan mutate's force gate + audit.

    Refuses without --force. Edits the beat whose id == int(target) in place,
    sets [field] = value, writes back atomically, and appends one JSONL line to
    runs/{run_id}/script_audit.jsonl. An unknown --target id is a hard error.
    """
    if not force:
        print(
            "error: script mutate refuses to run without --force.\n"
            "       Pass --force --actor <name> --reason \"<rationale>\"\n"
            "       to audited-override the locked: true flag.",
            file=sys.stderr,
        )
        return 1
    if not actor or not reason:
        print("error: --force requires both --actor and --reason.", file=sys.stderr)
        return 1

    bd = Path(brief_dir)
    rd = Path(run_dir)
    beats_path = bd / "beats.json"
    if not beats_path.exists():
        print(f"error: beats file not found at {beats_path}", file=sys.stderr)
        return 1

    try:
        beat_id = int(target)
    except ValueError:
        print(f"error: --target must be a beat id (int), got {target!r}", file=sys.stderr)
        return 1

    resolved = beats_path.resolve()
    current = json.loads(resolved.read_text(encoding="utf-8"))
    matched = [b for b in current.get("beats", []) if b.get("id") == beat_id]
    if not matched:
        print(
            f"error: no beat with id {beat_id} in {beats_path}. "
            f"mutate edits an existing beat's field; check the --target id.",
            file=sys.stderr,
        )
        return 1
    old_value = matched[0].get(field)
    matched[0][field] = value

    _atomic_write(resolved, json.dumps(current, indent=2))

    rd.mkdir(parents=True, exist_ok=True)
    audit_path = rd / "script_audit.jsonl"
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "actor": actor,
        "reason": reason,
        "target": target,
        "field": field,
        "old_value": old_value,
        "value": value,
        "beats_path": str(resolved),
    }
    with audit_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    print(f"mutated: beat {beat_id}.{field} = {value!r}")
    print(f"  audit:    appended to {audit_path}")
    return 0


def _atomic_write(path: Path, content: str) -> None:
    """temp-then-rename atomic write. Mirrors plan.py / patch_stager."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)
