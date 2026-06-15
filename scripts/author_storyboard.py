#!/usr/bin/env python3
"""Drive Bea (StoryboardArtistNode) programmatically — the Phase-3b board artist.

The sibling to scripts/author_script.py (Sam) and scripts/author_plan.py (Maya).
Bea is built as a node (`pipeline.agents.storyboard_artist.StoryboardArtistNode`),
not a CLI; this script is the driver: it constructs the AgentContext by hand, runs
Bea's single Sonnet 4.6 authoring call live, runs the free deterministic
coverage/conflict pass, and emits storyboard.md + a draft shots.yaml into the
brief dir.

Usage:

  python scripts/author_storyboard.py briefs/2026-06-10-spark-shared/ \
      --run-dir runs/2026-06-XX-bea-spark/ \
      --manifest manifest.yaml

Prerequisites (costed run — fleet-ops §0):
  - ANTHROPIC_API_KEY ABSENT (subscription billing via claude-agent-sdk → claude
    CLI OAuth). A present key silently bills the API; this script refuses to run
    with it set unless --allow-api-key is passed.
  - claude-agent-sdk installed + the `claude` CLI authenticated (subscription).
  - A `beats.json` (Sam's approved beat sheet) in the brief dir — Bea boards it.

SILENT-STUB HARDENING: StoryboardArtistNode reads SDKResponse.text and the Bea
stub returns a fully-valid {storyboard_md, shots_yaml} envelope, so a stubbed
board parses + round-trips through load_shots cleanly and could pass the human
gate undetected. Two guards (shared idiom with author_script.py):
  1. A cheap real smoke call to invoke_sonnet_text BEFORE the costed run.
  2. A post-hoc scan of the emitted storyboard.md + shots.yaml for the
     "STUB FALLBACK" marker. Belt and suspenders.
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
from pipeline.agents.storyboard_artist import StoryboardArtistNode  # noqa: E402
from pipeline.orchestration.guards import (  # noqa: E402
    GuardError,
    scan_stub_marker,
    smoke_live_sonnet,
)


def _smoke_live_sonnet() -> None:
    try:
        smoke_live_sonnet()
    except GuardError as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Drive Bea (StoryboardArtistNode) for Phase 3b.")
    parser.add_argument(
        "brief_dir",
        type=str,
        help="Brief folder holding 00_studio_brief.md + beats.json (e.g., briefs/2026-06-10-spark-shared/).",
    )
    parser.add_argument(
        "--run-dir", required=True,
        help="Run output directory (e.g., runs/2026-06-XX-bea-spark/).",
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
        help="Skip the pre-run live-Sonnet smoke call (not recommended for costed runs).",
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
    beats_path = brief_dir / "beats.json"
    if not beats_path.exists():
        print(
            f"error: Sam's beats.json not found at {beats_path} — run Sam and "
            f"`script approve` first.",
            file=sys.stderr,
        )
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
        _smoke_live_sonnet()

    ctx = AgentContext(
        run_dir=run_dir,
        inputs={"brief_dir": str(brief_dir)},
        manifest=manifest,
        criteria=None,
        tier="draft",
        cache_dir=cache_dir,
        extras={},
    )

    print(f"\nDriving Bea — Phase 3b board for {brief_dir.name}")
    print("  Sonnet 4.6 single authoring call → deterministic coverage/conflict pass")
    print(f"  manifest:    {manifest_path}")
    print(f"  run dir:     {run_dir}")
    print()

    node = StoryboardArtistNode()
    result = node.run(ctx)

    # Post-hoc stub guard — scan the emitted artifacts for the stub marker.
    storyboard_path = Path(result.outputs["storyboard_path"])
    shots_path = Path(result.outputs["shots_path"])
    if scan_stub_marker([storyboard_path, shots_path]):
        print(
            "\nERROR: Bea's emitted artifacts contain the STUB FALLBACK marker — the\n"
            "  board was NOT really authored. Do not approve it. Fix the SDK/auth and\n"
            "  re-run.",
            file=sys.stderr,
        )
        return 1

    print("emitted:")
    print(f"  storyboard:  {result.outputs['storyboard_path']}")
    print(f"  shots:       {result.outputs['shots_path']}")
    print(f"  notes:       {result.notes}")
    print()
    print(f"next: `python -m pipeline.cli storyboard show --shots {shots_path}` to review,")
    print(f"      then CURATE the draft shots.yaml and present it to Sean at the HUMAN GATE.")
    print(f"      Lock with `python -m pipeline.cli storyboard approve --brief-dir {brief_dir}`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
