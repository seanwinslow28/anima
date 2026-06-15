"""anima — `pipeline storyboard {init|show|approve|mutate}` subcommands (Bea).

Mirrors pipeline/cli/script.py structurally. Bea operates on shots.yaml (the
draft shot list) + reads beats.json (Sam's contract) for the coverage check:

  - `init`    scaffolds a shots.yaml template + storyboard.md stub (idempotent).
  - `show`    renders shots.yaml as a terminal tear sheet + beat coverage — boxes
              live in the renderer (this file); shots.yaml on disk stays clean.
  - `approve` the CURATION GATE: re-validates the curated shots.yaml against
              beats.json (load_shots + storyboard_validate) and only then flips
              `locked: true`. Idempotent. Refuses to lock a failing board.
  - `mutate`  audited force-flag edit of one frame field → storyboard_audit.jsonl.

`approve`/`mutate` flip/edit shots.yaml *textually* where possible so a human's
comments and formatting survive (mutate's nested-field edit is a yaml round-trip
— acceptable for the deliberate, audited override path).
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# Reuse plan.py's stable box-rendering primitives (DRY — same tear-sheet look).
from pipeline.cli.plan import _render_box, _render_header

_STRIP_WIDTH = 76  # truncate long shot lines in the strip for terminal scanning


# ---------------------------------------------------------------------------
# `storyboard init` — scaffold a shots.yaml template + storyboard.md stub
# ---------------------------------------------------------------------------

_SHOTS_TEMPLATE = (
    "# Draft shot list — author via:\n"
    "#   python scripts/author_storyboard.py <brief-dir> --run-dir runs/<id> --manifest manifest.yaml\n"
    "# Then curate and lock with `storyboard approve`.\n"
    "slug: REPLACE-ME\n"
    "frames:\n"
    "- id: 1\n"
    "  beat_id: 1            # the beats.json beat this shot boards\n"
    "  cast: []              # IR namespaces in frame (first = primary)\n"
    "  beat: 'TODO — what the shot shows'\n"
    "  prompt: 'TODO — prose-action ending in the pencil-test register clause block'\n"
    "  chain_anchors: []\n"
    "  hold: 2\n"
)

_STORYBOARD_STUB = (
    "# Storyboard\n\n"
    "Authored by Bea (the Phase-3b storyboard artist). To author for real, run:\n\n"
    "    python scripts/author_storyboard.py <brief-dir> --run-dir runs/<id> --manifest manifest.yaml\n\n"
    "This stub is a placeholder; author_storyboard.py overwrites it with the board.\n"
)


def init_storyboard(target: str) -> int:
    """Scaffold shots.yaml + storyboard.md into the target dir. Idempotent."""
    target_path = Path(target)
    target_path.mkdir(parents=True, exist_ok=True)

    created, skipped = [], []
    files = {
        "shots.yaml": _SHOTS_TEMPLATE,
        "storyboard.md": _STORYBOARD_STUB,
    }
    for name, content in files.items():
        dst = target_path / name
        if dst.exists():
            skipped.append(dst)
            continue
        dst.write_text(content, encoding="utf-8")
        created.append(dst)

    if created:
        print(f"scaffolded storyboard artifacts at {target_path}")
        for c in created:
            print(f"  created: {c.relative_to(target_path.parent)}")
    if skipped:
        print(f"  (existing, untouched: {len(skipped)} file(s))")
    print("\nnext: author with scripts/author_storyboard.py, then `storyboard show` / `storyboard approve`.")
    return 0


# ---------------------------------------------------------------------------
# `storyboard show` — render shots.yaml as a terminal tear sheet
# ---------------------------------------------------------------------------


def show_storyboard(shots_path: str) -> int:
    """Render shots.yaml with ASCII-box-decorated sections."""
    p = Path(shots_path)
    if not p.exists():
        print(f"error: shots file not found at {p}", file=sys.stderr)
        return 1
    try:
        rendered = render_shots(p.read_text(encoding="utf-8"))
    except (ValueError, yaml.YAMLError) as e:
        print(f"error: {p} is not parseable shots.yaml: {e}", file=sys.stderr)
        return 1
    print(rendered)
    return 0


def render_shots(shots_yaml: str) -> str:
    """Pure function: shots.yaml text in, ASCII-box tear sheet out.

    Boxes live here (terminal presentation only); shots.yaml on disk stays clean
    human YAML. Extracted so tests assert the rendered string without a subprocess.
    """
    data = yaml.safe_load(shots_yaml) or {}
    slug = str(data.get("slug", "(no slug)"))
    locked = bool(data.get("locked", False))
    frames = data.get("frames", []) or []

    lines: list[str] = [
        _render_header(f"{slug}  —  {'LOCKED' if locked else 'draft'}  ({len(frames)} shots)"),
        "",
    ]

    strip: list[str] = []
    covered: list[int] = []
    for f in frames:
        bid = f.get("beat_id")
        if isinstance(bid, int):
            covered.append(bid)
        cast = ", ".join(str(c) for c in (f.get("cast") or []))
        strip.append(_clip(f"[{f.get('id')}] -> beat {bid}   cast: {cast}   hold {f.get('hold', 2)}"))
        strip.append(_clip(f"      shows:  {f.get('beat', '')}"))
        strip.append(_clip(f"      prompt: {f.get('prompt', '')}"))
    lines.append(_render_box("Shot strip", "\n".join(strip) if strip else "(no shots)"))
    lines.append("")
    coverage = (
        "beats boarded: " + ", ".join(str(b) for b in sorted(set(covered)))
        if covered else "no beat_id links (back-compat shot list)"
    )
    lines.append(_render_box("Beat coverage", coverage))
    return "\n".join(lines)


def _clip(s: str) -> str:
    return s if len(s) <= _STRIP_WIDTH else s[: _STRIP_WIDTH - 1] + "…"


# ---------------------------------------------------------------------------
# `storyboard approve` — the curation gate: validate, then lock
# ---------------------------------------------------------------------------


def approve_storyboard(brief_dir: str, manifest_path: str = "manifest.yaml") -> int:
    """Re-validate the curated shots.yaml against beats.json, then flip locked=true.

    The curation gate: load_shots + storyboard_validate must pass (coverage, no
    orphans, no script↔board conflict) before the board locks. A failing board is
    NOT locked. Idempotent — a second call on a locked board is a no-op. The
    locked flag is set textually so the human's comments/formatting survive.
    """
    # Imported here so the module registers the node and the CLI stays import-light.
    from pipeline.orchestration.beats import load_beats
    from pipeline.orchestration.cast import derive_cast
    from pipeline.orchestration.shots import load_shots
    from pipeline.agents.storyboard_artist import storyboard_validate

    bd = Path(brief_dir)
    shots_path = bd / "shots.yaml"
    beats_path = bd / "beats.json"
    if not shots_path.exists():
        print(f"error: shots file not found at {shots_path}", file=sys.stderr)
        return 1
    if not beats_path.exists():
        print(f"error: beats file not found at {beats_path} (run Sam first)", file=sys.stderr)
        return 1

    target = shots_path.resolve()
    raw = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
    if raw.get("locked"):
        print(f"already locked: {shots_path} (no-op)")
        return 0

    try:
        manifest = yaml.safe_load(Path(manifest_path).read_text(encoding="utf-8")) or {}
        known = {m["ir_namespace"] for m in derive_cast(manifest) if m["ir_namespace"]}
        sheet = load_beats(beats_path, known_namespaces=known)
        shot_list = load_shots(target, known_namespaces=known)
        storyboard_validate(sheet, shot_list, known_namespaces=known)
    except (ValueError, FileNotFoundError, KeyError) as e:
        print(
            f"error: curation gate failed — not locking {shots_path}:\n  {e}",
            file=sys.stderr,
        )
        return 1

    _atomic_write(target, _set_locked_true(target.read_text(encoding="utf-8")))
    print(f"approved: validated + locked=true on {target}")
    return 0


_LOCKED_LINE_RE = re.compile(r"^locked:.*$", re.MULTILINE)


def _set_locked_true(text: str) -> str:
    """Set a top-level `locked: true` while preserving the rest of the file.

    Replaces an existing top-level `locked:` line in place; otherwise prepends the
    flag (valid YAML — key order is immaterial). Comments and formatting survive.
    """
    if _LOCKED_LINE_RE.search(text):
        return _LOCKED_LINE_RE.sub("locked: true", text, count=1)
    return "locked: true\n" + text


# ---------------------------------------------------------------------------
# `storyboard mutate` — audited mutation of one frame field
# ---------------------------------------------------------------------------


def mutate_storyboard(
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
    """Audited edit of one frame's field. Mirrors script mutate's force gate + audit.

    Refuses without --force. Edits the frame whose id == int(target) in place,
    sets [field] = value, writes back, and appends one JSONL line to
    runs/{run_id}/storyboard_audit.jsonl. An unknown --target id is a hard error.
    (The write is a yaml round-trip — acceptable for the deliberate audited path.)
    """
    if not force:
        print(
            "error: storyboard mutate refuses to run without --force.\n"
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
    shots_path = bd / "shots.yaml"
    if not shots_path.exists():
        print(f"error: shots file not found at {shots_path}", file=sys.stderr)
        return 1

    try:
        frame_id = int(target)
    except ValueError:
        print(f"error: --target must be a frame id (int), got {target!r}", file=sys.stderr)
        return 1

    resolved = shots_path.resolve()
    current = yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}
    matched = [f for f in current.get("frames", []) if f.get("id") == frame_id]
    if not matched:
        print(
            f"error: no frame with id {frame_id} in {shots_path}. "
            f"mutate edits an existing frame's field; check the --target id.",
            file=sys.stderr,
        )
        return 1
    old_value = matched[0].get(field)
    matched[0][field] = value

    _atomic_write(resolved, yaml.safe_dump(current, sort_keys=False, allow_unicode=True))

    rd.mkdir(parents=True, exist_ok=True)
    audit_path = rd / "storyboard_audit.jsonl"
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "actor": actor,
        "reason": reason,
        "target": target,
        "field": field,
        "old_value": old_value,
        "value": value,
        "shots_path": str(resolved),
    }
    with audit_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    print(f"mutated: frame {frame_id}.{field} = {value!r}")
    print(f"  audit:    appended to {audit_path}")
    return 0


def _atomic_write(path: Path, content: str) -> None:
    """temp-then-rename atomic write. Mirrors plan.py / patch_stager."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)
