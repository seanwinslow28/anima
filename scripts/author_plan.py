#!/usr/bin/env python3
"""Drive Maya (PlannerNode) programmatically — the Phase-0 planner.

Sean: this is the Maya sibling to scripts/author_bible.py. The kickoff for the
first integrated end-to-end run ("The Spark, Shared") flagged that there is no
`author_plan.py` — Maya is built as a node (`pipeline.agents.planner.PlannerNode`),
not a CLI. This script is that missing driver: it constructs the AgentContext by
hand, runs Maya's three-call loop live (Opus 4.8 primary → Sonnet 4.6 adversarial
→ resolve), and emits the four Phase-0 artifacts into the brief dir.

It is also one of the orchestration SEAMS the integrated run exists to surface —
a future `run` orchestrator absorbs this hand-wiring.

Usage:

  python scripts/author_plan.py briefs/2026-06-10-spark-shared/ \
      --run-dir runs/2026-06-11-spark-shared-first-integrated/ \
      --manifest manifest.yaml

Prerequisites (costed run — fleet-ops §0):
  - ANTHROPIC_API_KEY ABSENT (subscription billing via claude-agent-sdk → claude
    CLI OAuth). A present key silently bills the API; this script refuses to run
    with it set unless --allow-api-key is passed.
  - claude-agent-sdk installed + the `claude` CLI authenticated (subscription).

SILENT-STUB HARDENING (the highest-risk seam): PlannerNode discards the
SDKResponse.stub_fallback flag and only reads .text. The Opus *text* stub returns
a fully-valid three-key envelope, so a stubbed Maya plan parses cleanly and could
pass the human gate undetected. This driver guards two ways:
  1. A cheap real smoke call to invoke_opus_text BEFORE the costed run — asserts
     the live path (resp.ok and not resp.stub_fallback). If the SDK is absent or
     the CLI can't auth, we stop here rather than burning Maya's three calls on an
     error/stub envelope.
  2. A post-hoc scan of the emitted plan.md + production brief for the "STUB
     FALLBACK" marker. Belt and suspenders.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

import yaml

# Make pipeline.* importable when running from the repo root.
_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT))

from pipeline.agents import AgentContext  # noqa: E402
# Import the node modules so NODE_REGISTRY is populated before Maya runs — she
# calls NODE_REGISTRY["cost_estimator"]() internally for the cost preview.
import pipeline.agents.cost_estimator  # noqa: E402,F401
from pipeline.agents.planner import PlannerNode  # noqa: E402
from pipeline.agents.sdk_runners import invoke_opus_text  # noqa: E402

_STUB_MARKER = "STUB FALLBACK"


def _smoke_live_opus() -> None:
    """Cheap real Opus call to confirm the live (non-stub) subscription path.

    Exits non-zero if the SDK is unavailable (stub) or the call errors (CLI not
    authed / API key absent on the fallback path). Subscription-absorbed — one
    tiny prompt.
    """
    print("Smoke: confirming live Opus path (subscription billing)…")
    resp = asyncio.run(invoke_opus_text(prompt="Reply with exactly: SPARK-OK"))
    if resp.stub_fallback:
        print(
            "\nERROR: Opus smoke returned a STUB envelope — no real SDK path.\n"
            "  Maya would silently produce a stub plan that parses cleanly and could\n"
            "  pass the human gate. Install claude-agent-sdk and authenticate the\n"
            "  `claude` CLI (subscription), then re-run.",
            file=sys.stderr,
        )
        sys.exit(1)
    if not resp.ok:
        print(
            f"\nERROR: Opus smoke failed (exit_code={resp.exit_code}, error={resp.error}).\n"
            "  The claude-agent-sdk path is importable but the call did not succeed —\n"
            "  likely the `claude` CLI isn't authenticated, or it fell through to the\n"
            "  anthropic SDK with no ANTHROPIC_API_KEY. Fix auth, then re-run.",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"  live: model={resp.model} duration={resp.duration_s:.1f}s ok=True")


def main() -> int:
    parser = argparse.ArgumentParser(description="Drive Maya (PlannerNode) for Phase 0.")
    parser.add_argument(
        "brief_dir",
        type=str,
        help="Brief folder holding 00_studio_brief.md (e.g., briefs/2026-06-10-spark-shared/).",
    )
    parser.add_argument(
        "--run-dir", required=True,
        help="Run output directory (e.g., runs/2026-06-11-spark-shared-first-integrated/).",
    )
    parser.add_argument(
        "--manifest", default="manifest.yaml",
        help="Manifest path (default manifest.yaml). Read for generation/phases/tiering/critics.",
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

    print(f"\nDriving Maya — Phase 0 planning for {brief_dir.name}")
    print("  Opus 4.8 primary → Sonnet 4.6 adversarial → resolve (3-call ceiling)")
    print(f"  manifest:    {manifest_path}")
    print(f"  run dir:     {run_dir}")
    print()

    node = PlannerNode()
    result = node.run(ctx)

    # Post-hoc stub guard — scan the emitted artifacts for the stub marker.
    plan_path = Path(result.outputs["plan_path"])
    brief_path = Path(result.outputs["production_brief_path"])
    emitted_text = ""
    for p in (plan_path, brief_path):
        if p.exists():
            emitted_text += p.read_text(encoding="utf-8")
    if _STUB_MARKER in emitted_text:
        print(
            "\nERROR: Maya's emitted artifacts contain the STUB FALLBACK marker — the\n"
            "  plan was NOT really authored. Do not approve it. Fix the SDK/auth and\n"
            "  re-run.",
            file=sys.stderr,
        )
        return 1

    ce = result.outputs["cost_estimate"]
    print("emitted:")
    print(f"  production_brief: {result.outputs['production_brief_path']}")
    print(f"  criteria:         {result.outputs['criteria_path']}")
    print(f"  plan:             {result.outputs['plan_path']}")
    print(f"  notes:            {result.notes}")
    print()
    print("cost preview (RunCostEstimate):")
    print(f"  low ${ce['low_usd']:.2f}  /  median ${ce['median_usd']:.2f}  /  high ${ce['high_usd']:.2f}")
    for phase_id in sorted(ce.get("by_phase", {})):
        band = ce["by_phase"][phase_id]
        print(
            f"    {phase_id}: low ${band.get('low_usd', 0):.2f} / "
            f"median ${band.get('median_usd', 0):.2f} / high ${band.get('high_usd', 0):.2f}"
            + (f"  [confidence={band['confidence']}]" if band.get("confidence") else "")
        )
    print()
    print(f"next: `python -m pipeline.cli plan show --plan {plan_path}` to review,")
    print(f"      then present plan.md + cost preview to Sean at the HUMAN GATE.")
    print("      No generation spend until Sean approves (`pipeline plan approve`).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
