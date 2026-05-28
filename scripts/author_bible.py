#!/usr/bin/env python3
"""Author a Character Bible by invoking Cy programmatically.

Sean: this is the orchestrator for the two Bible authoring runs that ship as
commit 2's load-bearing portfolio artifacts (Tasks 1.10 + 1.11). The
infrastructure work — folder scaffolding, source-refs population, manifest
registration — already shipped in earlier commits. This script binds it all
to a real Cy invocation against live Opus + NB Pro + Gemini.

Usage:

  # Author the sean-anchor Bible (Task 1.10 — the control case):
  python scripts/author_bible.py characters/sean-anchor/ \
      --studio-brief "Pencil Test reference character — see source-refs/notes.md" \
      --run-dir runs/2026-05-28-cy-sean-anchor-bake/

  # Author the claude-mascot Bible (Task 1.11 — the validation case):
  python scripts/author_bible.py characters/claude-mascot/ \
      --studio-brief "Pixel-art mascot — see source-refs/notes.md" \
      --run-dir runs/2026-05-28-cy-claude-mascot-bake/

Prerequisites:
  - .env carries GEMINI_API_KEY for NB Pro
  - claude-agent-sdk installed and authenticated for Opus calls
  - agy CLI on PATH and authenticated for Gemini 3.1 Pro verification calls
  - source-refs/ for the target character is populated (Sean drops material)

Without real API access, this script falls back to stub envelopes that
still exercise the AgentSpec contract end-to-end. The stub Bible is
deterministic but minimal — Sean should not approve a stub-authored Bible.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make pipeline.* importable when running from the repo root.
_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT))

from pipeline.agents import AgentContext  # noqa: E402
from pipeline.agents.character_designer import CharacterDesignerNode  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Author a Character Bible via Cy.")
    parser.add_argument(
        "character_dir",
        type=str,
        help="Path to the character folder (e.g., characters/sean-anchor/).",
    )
    parser.add_argument(
        "--studio-brief", default="",
        help="One-line Studio Brief excerpt; Cy reads source-refs/notes.md for the rest.",
    )
    parser.add_argument(
        "--run-dir", required=True,
        help="Run output directory (e.g., runs/2026-05-28-cy-sean-anchor-bake/).",
    )
    args = parser.parse_args()

    character_dir = Path(args.character_dir)
    if not character_dir.exists():
        print(f"error: character folder not found: {character_dir}", file=sys.stderr)
        return 1
    source_refs = character_dir / "source-refs"
    if not source_refs.exists() or not any(source_refs.iterdir()):
        print(
            f"error: {source_refs} is missing or empty. Drop source material first; "
            f"see source-refs/0-sean-author-this.md for the checklist.",
            file=sys.stderr,
        )
        return 1

    run_dir = Path(args.run_dir)
    cache_dir = run_dir / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    ctx = AgentContext(
        run_dir=run_dir,
        inputs={
            "character_dir": str(character_dir),
            "studio_brief": args.studio_brief or _default_studio_brief(character_dir),
        },
        manifest={},
        criteria=None,
        tier="draft",
        cache_dir=cache_dir,
        extras={},
    )

    print(f"Authoring {character_dir.name} Bible — Pass 1 (Opus) → Pass 2 (NB Pro) → Pass 3 (Gemini)")
    print(f"  source-refs: {sum(1 for _ in source_refs.rglob('*') if _.is_file())} file(s)")
    print(f"  run dir:     {run_dir}")
    print()

    node = CharacterDesignerNode()
    result = node.run(ctx)

    print()
    print("emitted:")
    for port, value in result.outputs.items():
        if port == "plate_results":
            continue
        print(f"  {port}: {value}")
    plate_results = result.outputs.get("plate_results", {})
    if plate_results:
        print(f"  plates: {len(plate_results)} total")
        human_gate = sum(1 for v in plate_results.values() if v.get("status") == "human_gate_required")
        if human_gate:
            print(f"    {human_gate} plate(s) flagged for human gate — review before approval")
    print()
    print(f"next: `python -m pipeline.cli bible show --character-dir {character_dir}` "
          f"to review, then `pipeline bible approve` to lock the criteria graph.")
    return 0


def _default_studio_brief(character_dir: Path) -> str:
    """Compose a minimal Studio Brief excerpt from the character folder name +
    source-refs/notes.md if present, so the run doesn't fail when --studio-brief
    isn't passed."""
    notes_path = character_dir / "source-refs" / "notes.md"
    if notes_path.exists():
        return (
            f"# Studio Brief — {character_dir.name}\n\n"
            f"Cy: read source-refs/notes.md for the full character voice. "
            f"This is the brief excerpt for the {character_dir.name} Bible authoring run."
        )
    return (
        f"# Studio Brief — {character_dir.name}\n\n"
        f"(no source-refs/notes.md present; Cy infers from images alone.)"
    )


if __name__ == "__main__":
    sys.exit(main())
