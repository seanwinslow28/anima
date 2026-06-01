# evals/bakeoffs/2026-05-31-t2-vision-critic-gemini-vs-sonnet-vs-opus/bakeoff.py
"""T2 vision-critic three-way bake-off — Gemini vs Sonnet vs Opus.

Mirrors pipeline/seedance_bakeoff.py's variant shape. Only default_model
varies; prompt + standing context + cases held constant. Reuses Em's
_build_prompt + _parse via evals.vision_critic.bakeoff_lib.

Usage (deliberate, costed ~$5, subscription-absorbed):
    .venv/bin/python evals/bakeoffs/2026-05-31-t2-vision-critic-gemini-vs-sonnet-vs-opus/bakeoff.py
    .venv/bin/python evals/bakeoffs/2026-05-31-t2-vision-critic-gemini-vs-sonnet-vs-opus/bakeoff.py --variants gemini
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

from evals.vision_critic.bakeoff_lib import score_config
from evals.vision_critic.scoring import segment_report
from evals.vision_critic.score import _manifest, render_last_run_md  # reuse

HERE = Path(__file__).parent
VC = HERE.parents[1] / "vision_critic"  # evals/vision_critic/
FIXTURES = VC / "fixtures"


def main() -> None:
    ap = argparse.ArgumentParser(prog="t2-bakeoff")
    ap.add_argument("--variants", nargs="+", default=None)
    args = ap.parse_args()

    variants_data = yaml.safe_load((HERE / "variants.yaml").read_text(encoding="utf-8"))
    cases = yaml.safe_load((VC / "cases.yaml").read_text(encoding="utf-8"))["cases"]
    manifest = _manifest()
    chosen = [v for v in variants_data["variants"]
              if not args.variants or v["id"] in args.variants]

    sections = [
        f"# T2 vision-critic bake-off — {datetime.now(timezone.utc):%Y-%m-%d}",
        "",
        "Gemini (agy) vs Sonnet (SDK) vs Opus (SDK). Only the model varies; "
        "prompt + standing context + cases held constant; no escalation.",
        "",
        "**Model snapshots (pin these — the re-runnable baseline a future "
        "provider bump is checked against):**",
        "- gemini: 3.1 Pro via agy v1.0.2 (no model-pin flag — record agy version)",
        "- sonnet: claude-sonnet-4-6 via claude-agent-sdk",
        "- opus: claude-opus-4-7 via claude-agent-sdk",
        "",
    ]
    (HERE / "traces").mkdir(exist_ok=True)
    for v in chosen:
        print(f"Running bake-off for variant: {v['label']}...")
        scores = score_config(variant=v, cases=cases, fixtures=FIXTURES, manifest=manifest)
        report = segment_report(scores)
        md = render_last_run_md(report, model_label=v["label"], n_total=len(scores))
        (HERE / "traces" / f"{v['id']}.md").write_text(md, encoding="utf-8")
        sections.append(f"## {v['label']}\n\n{md}\n")

    (HERE / "results.md").write_text("\n".join(sections), encoding="utf-8")
    print("\n".join(sections))
    print(f"\nWrote {HERE/'results.md'} + per-config traces.")


if __name__ == "__main__":
    main()
