#!/usr/bin/env python3
"""Drive Sam (ScriptwriterNode) programmatically — the Phase-3a scriptwriter.

The sibling to scripts/author_plan.py (Maya) and scripts/author_bible.py (Cy).
Sam is built as a node (`pipeline.agents.scriptwriter.ScriptwriterNode`), not a
CLI; this script is the driver: it constructs the AgentContext by hand, runs
Sam's single Opus 4.8 authoring call live, runs the free deterministic structural
pass, and emits script.md + beats.json into the brief dir.

Usage:

  python scripts/author_script.py briefs/2026-06-10-spark-shared/ \
      --run-dir runs/2026-06-XX-sam-spark/ \
      --manifest manifest.yaml

Prerequisites (costed run — fleet-ops §0):
  - ANTHROPIC_API_KEY ABSENT (subscription billing via claude-agent-sdk → claude
    CLI OAuth). A present key silently bills the API; this script refuses to run
    with it set unless --allow-api-key is passed.
  - claude-agent-sdk installed + the `claude` CLI authenticated (subscription).

SILENT-STUB HARDENING: ScriptwriterNode (like PlannerNode) reads SDKResponse.text
and the Sam text stub returns a fully-valid {script_md, beats_json} envelope, so a
stubbed script parses + round-trips through load_beats cleanly and could pass the
human gate undetected. Two guards (shared with author_plan.py):
  1. A cheap real smoke call to invoke_opus_text BEFORE the costed run.
  2. A post-hoc scan of the emitted script.md + beats.json for the "STUB FALLBACK"
     marker. Belt and suspenders.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import yaml

# Make pipeline.* importable when running from the repo root.
_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT))

from pipeline.agents import AgentContext  # noqa: E402
from pipeline.agents.scriptwriter import ScriptwriterNode  # noqa: E402
from pipeline.orchestration.guards import (  # noqa: E402
    GuardError,
    scan_stub_marker,
    smoke_live_opus,
)


def _smoke_live_opus() -> None:
    try:
        smoke_live_opus()
    except GuardError as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Drive Sam (ScriptwriterNode) for Phase 3a.")
    parser.add_argument(
        "brief_dir",
        type=str,
        help="Brief folder holding 00_studio_brief.md (e.g., briefs/2026-06-10-spark-shared/).",
    )
    parser.add_argument(
        "--run-dir", required=True,
        help="Run output directory (e.g., runs/2026-06-XX-sam-spark/).",
    )
    parser.add_argument(
        "--manifest", default="manifest.yaml",
        help="Manifest path (default manifest.yaml). Read for the characters: registry (cast).",
    )
    parser.add_argument(
        "--allow-api-key", action="store_true",
        help="Permit running with ANTHROPIC_API_KEY set (bills the API). Default: refuse.",
    )
    parser.add_argument(
        "--skip-smoke", action="store_true",
        help="Skip the pre-run live-Opus smoke call (not recommended for costed runs).",
    )
    args = parser.parse_args()

    # Fleet-ops §0: subscription billing, never the API key.
    if os.environ.get("ANTHROPIC_API_KEY") and not args.allow_api_key:
        print(
            "ERROR: ANTHROPIC_API_KEY is set — this would bill the Anthropic API, not\n"
            "  the subscription. Unset it (fleet-ops §1) or pass --allow-api-key.",
            file=sys.stderr,
        )
        return 1

    brief_dir = Path(args.brief_dir)
    studio_brief = brief_dir / "00_studio_brief.md"
    if not studio_brief.exists():
        print(f"error: Studio Brief not found at {studio_brief}", file=sys.stderr)
        return 1

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"error: manifest not found at {manifest_path}", file=sys.stderr)
        return 1
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}

    run_dir = Path(args.run_dir)
    cache_dir = run_dir / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    if not args.skip_smoke:
        _smoke_live_opus()

    ctx = AgentContext(
        run_dir=run_dir,
        inputs={"brief_dir": str(brief_dir)},
        manifest=manifest,
        criteria=None,
        tier="draft",
        cache_dir=cache_dir,
        extras={},
    )

    print(f"\nDriving Sam — Phase 3a script for {brief_dir.name}")
    print("  Opus 4.8 single authoring call → deterministic structural pass")
    print(f"  manifest:    {manifest_path}")
    print(f"  run dir:     {run_dir}")
    print()

    node = ScriptwriterNode()
    result = node.run(ctx)

    # Post-hoc stub guard — scan the emitted artifacts for the stub marker.
    script_path = Path(result.outputs["script_path"])
    beats_path = Path(result.outputs["beats_path"])
    if scan_stub_marker([script_path, beats_path]):
        print(
            "\nERROR: Sam's emitted artifacts contain the STUB FALLBACK marker — the\n"
            "  script was NOT really authored. Do not approve it. Fix the SDK/auth and\n"
            "  re-run.",
            file=sys.stderr,
        )
        return 1

    print("emitted:")
    print(f"  script:  {result.outputs['script_path']}")
    print(f"  beats:   {result.outputs['beats_path']}")
    print(f"  notes:   {result.notes}")
    print()
    print(f"next: `python -m pipeline.cli script show --beats {beats_path}` to review,")
    print(f"      then present script.md + the beat sheet to Sean at the HUMAN GATE.")
    print(f"      Lock with `python -m pipeline.cli script approve --brief-dir {brief_dir}`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
