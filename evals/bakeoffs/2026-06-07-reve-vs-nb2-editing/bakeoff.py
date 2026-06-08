# evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/bakeoff.py
"""Reve vs NB2 image-editing bake-off — a GENERATOR head-to-head.

Two stages:
  generate  — each variant EDITS every case; outputs land in generated/{variant}/{case}.png
  score     — DINOv2-vs-per-view-anchor (deterministic SF02, the headline) + optional
              Em verdict (--score-em; SF01/SF02, secondary). Writes results.md + traces/.

Method: docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md
  §3.5 — DINOv2-vs-per-view-anchor is the visual groundedness metric; NO universal
         threshold, so the DECISION is the Reve-vs-NB2 DELTA on the same case + anchor.
         A still-image MLLM judge is trustworthy mainly PAIRWISE — Em-absolute here is
         a SECONDARY corroborator, not the decider (pairwise Em is a documented refinement).
  §6   — generator row: DINOv2-vs-anchor is the visual groundedness metric; report
         per-plate below-threshold COUNT (Subject-Collapse), not a mean that hides one
         catastrophic drift. §5 borrow #2 — stderr() on every metric.

Usage (the costed live run is the operator's; see README + fleet-ops guardrails):
    # credential-free plumbing check (CI-safe; stub outputs, no spend, no scored claim):
    .venv/bin/python evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/bakeoff.py --stage all --stub

    # live (costed): set REVE_API_KEY + GEMINI_API_KEY; run from an isolated worktree
    # with ANTHROPIC_API_KEY UNSET (subscription billing). DINOv2 needs torch+transformers.
    .venv/bin/python evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/bakeoff.py --stage generate
    .venv/bin/python evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/bakeoff.py --stage score --score-em
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
REPO = HERE.resolve().parents[2]  # evals/bakeoffs/<dated>/ -> repo root
sys.path.insert(0, str(REPO))     # so `import pipeline`, `import evals` resolve
sys.path.insert(0, str(HERE))     # so `import reve_runner` resolves (non-package dir)

import yaml
from dotenv import load_dotenv

load_dotenv()

from pipeline.agents.nb_pro_runner import invoke_image_edit
from pipeline.agents.similarity_gate import compute_similarity, SIMILARITY_FLAG_THRESHOLD
from evals.vision_critic.scoring import stderr
import reve_runner

GENERATED = HERE / "generated"
CACHE = HERE / ".cache"
NB2_MODEL = "gemini-3.1-flash-image-preview"


def _load(name: str) -> dict:
    return yaml.safe_load((HERE / name).read_text(encoding="utf-8"))


def _refs(case: dict) -> list[Path]:
    return [REPO / r for r in case["references"]]


def _anchors(case: dict) -> list[Path]:
    """per_view_anchor (str) or per_view_anchors (list). In-betweens score against
    every endpoint and take the MIN (the Subject-Collapse identity floor)."""
    if "per_view_anchors" in case:
        return [REPO / a for a in case["per_view_anchors"]]
    return [REPO / case["per_view_anchor"]]


# --------------------------------------------------------------------------- #
# Stage 1 — generate
# --------------------------------------------------------------------------- #
def generate(variants: list[dict], cases: list[dict], stub: bool = False) -> dict:
    est = sum(v["cost_per_image_usd"] for v in variants) * len(cases)
    print(f"Estimated spend: ${est:.2f}  ({len(variants)} variants x {len(cases)} cases)"
          + ("   [--stub: $0, no calls]" if stub else ""))
    manifest: dict = {"generated_utc": datetime.now(timezone.utc).isoformat(), "rows": []}
    any_stub = False
    for v in variants:
        for case in cases:
            out = GENERATED / v["id"] / f"{case['name']}.png"
            refs = _refs(case)
            if stub:
                # Hard short-circuit: NEVER call a runner under --stub. The runners
                # re-read .env directly (invoke_image_edit's _has_gemini_api_key honors
                # the .env file, not just os.environ), so popping the env var is not
                # enough — a populated .env would otherwise fire a REAL, COSTED call
                # under --stub. Writing the placeholder here guarantees $0 and a
                # consistent keyless stub for every engine.
                reve_runner._write_placeholder_png(out)
                stub_used = True
            elif v["engine"] == "nb2":
                r = invoke_image_edit(
                    prompt=case["prompt"], reference_images=refs, output_path=out,
                    cache_dir=CACHE / "nb2", model=NB2_MODEL,
                )
                stub_used = r.stub_fallback
            elif v["engine"] == "reve":
                r = reve_runner.invoke_reve(
                    prompt=case["prompt"], reference_images=refs, output_path=out,
                    cache_dir=CACHE / "reve", tier=v["tier"], aspect_ratio=case.get("aspect_ratio", "16:9"),
                )
                stub_used = r.stub_fallback
            else:
                raise ValueError(f"unknown engine: {v['engine']}")
            any_stub = any_stub or stub_used
            tag = " [STUB]" if stub_used else ""
            print(f"  {v['id']:>14} | {case['name']:<28} -> {out.name}{tag}")
            manifest["rows"].append({
                "variant": v["id"], "case": case["name"], "engine": v["engine"],
                "tier": v["tier"], "output": str(out.relative_to(HERE)),
                "stub_fallback": stub_used, "cost_usd": v["cost_per_image_usd"],
            })
    manifest["any_stub"] = any_stub
    (HERE / "generate-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if any_stub:
        print("\n⚠ At least one output is a STUB placeholder — DINOv2/Em scores on it are "
              "NOT a scored claim (set REVE_API_KEY + GEMINI_API_KEY for the real run).")
    return manifest


# --------------------------------------------------------------------------- #
# Stage 2 — score (DINOv2 primary; Em optional/secondary)
# --------------------------------------------------------------------------- #
def _dinov2_score(generated: Path, anchors: list[Path]) -> tuple[float, str]:
    """Min DINOv2 cosine across the per-view anchors (Subject-Collapse floor)."""
    results = [compute_similarity(generated, a) for a in anchors]
    worst = min(results, key=lambda r: r.score)
    return worst.score, worst.method


def score(variants: list[dict], cases: list[dict], manifest: dict, score_em: bool) -> str:
    # ---- DINOv2 matrix: case x variant ----
    grid: dict[str, dict[str, tuple[float, str]]] = {}  # case -> variant -> (score, method)
    method_seen = set()
    for v in variants:
        for case in cases:
            gen = GENERATED / v["id"] / f"{case['name']}.png"
            if not gen.exists():
                grid.setdefault(case["name"], {})[v["id"]] = (float("nan"), "missing")
                continue
            s, m = _dinov2_score(gen, _anchors(case))
            grid.setdefault(case["name"], {})[v["id"]] = (s, m)
            method_seen.add(m)

    baseline = next((v["id"] for v in variants if v.get("baseline")), variants[0]["id"])
    vids = [v["id"] for v in variants]

    lines = [
        f"# Reve vs NB2 — image-editing bake-off — {datetime.now(timezone.utc):%Y-%m-%d}",
        "",
        "Generator head-to-head. **Headline metric: DINOv2-vs-per-view-anchor**, read as the "
        f"**Δ vs the `{baseline}` baseline** on the same case + same anchor (eval-strategy §3.5: "
        "no universal DINO threshold — the delta is the signal). Em (if run) is a **secondary** "
        "corroborator; a still-image judge is trustworthy mainly pairwise.",
        "",
        f"**DINOv2 method engaged:** {', '.join(sorted(method_seen)) or 'none'} "
        "(`pil-perceptual` = torch/transformers absent → NOT a real identity read; install "
        "`torch torchvision transformers` for the DINOv2 tier).",
        "",
        f"**Stub run:** {'YES — placeholder outputs, NOT a scored claim' if manifest.get('any_stub') else 'no (real generations)'}",
        "",
        "## DINOv2 identity hold — case × variant (higher = closer to the per-view anchor)",
        "",
        "| case | difficulty | " + " | ".join(vids) + f" | Δ(best Reve − {baseline}) |",
        "|" + "---|" * (len(vids) + 3),
    ]
    case_by_name = {c["name"]: c for c in cases}
    for cname, row in grid.items():
        diff = case_by_name[cname].get("difficulty", "")
        cells = []
        for vid in vids:
            sc, _ = row.get(vid, (float("nan"), ""))
            cells.append("—" if sc != sc else f"{sc:.3f}")
        base_sc = row.get(baseline, (float("nan"), ""))[0]
        reve_scores = [row.get(v["id"], (float("nan"), ""))[0]
                       for v in variants if v["engine"] == "reve"]
        reve_scores = [s for s in reve_scores if s == s]
        if reve_scores and base_sc == base_sc:
            delta = max(reve_scores) - base_sc
            dcell = f"{delta:+.3f}" + ("  ⚠ worse" if delta < -0.03 else "")
        else:
            dcell = "—"
        lines.append(f"| `{cname}` | {diff} | " + " | ".join(cells) + f" | {dcell} |")

    # ---- per-variant aggregates: mean ± stderr + Subject-Collapse count ----
    lines += ["", "## Per-variant aggregate (mean ± stderr; Subject-Collapse = # below "
              f"{SIMILARITY_FLAG_THRESHOLD})", ""]
    lines += ["| variant | mean DINOv2 | stderr | SCR (below-thresh / n) | $/img |",
              "|---|---|---|---|---|"]
    for v in variants:
        scores = [grid[c["name"]][v["id"]][0] for c in cases
                  if grid.get(c["name"], {}).get(v["id"], (float("nan"),))[0] == grid.get(c["name"], {}).get(v["id"], (float("nan"),))[0]]
        n = len(scores)
        mean = sum(scores) / n if n else float("nan")
        se = stderr(p=mean, n=n) if n else 0.0
        scr = sum(1 for s in scores if s < SIMILARITY_FLAG_THRESHOLD)
        lines.append(f"| `{v['id']}` | {mean:.3f} | ±{se:.3f} | {scr}/{n} | "
                     f"${v['cost_per_image_usd']:.3f} |")

    # ---- optional Em (secondary) ----
    if score_em:
        lines += ["", "## Em verdicts (SECONDARY — reference-blind absolute; see §caveat)", ""]
        lines += _score_em_block(variants, cases)

    lines += [
        "", "---", "",
        "## How to read this", "",
        f"- **Decision metric:** the Δ column. A Reve variant earns *adopt for keyframes/Bible* only "
        f"if its DINOv2 **matches or beats `{baseline}`** on the identity cases (`t1-edit-focused`, "
        "`t2-remix-3quarter`, `t2-remix-3ref-pairing`). A `⚠ worse` on `t2-remix-3quarter` means Reve "
        "shares NB-Pro's multi-reference downsampling regression → **disqualified for multi-ref keyframes**.",
        "- **In-between fit:** `t3-inbetween-*` is scored against both endpoints (min). Reve Fast *adopts "
        "for in-betweens* if it holds here and `t2-remix-3quarter` shows no downsampling collapse — a mild "
        "wobble is tolerable on an in-between.",
        "- **Em is secondary.** Reference-blind Em cannot truly verify identity (the documented limitation); "
        "it corroborates SF01/register and flags gross drift. The recommended refinement is **pairwise Em** "
        "(\"is variant A or B closer to the anchor?\") — not built here; see README §Em pairwise.",
        "- **Do not** declare a winner off a `pil-perceptual` run or a stub run — neither is a real identity read.",
    ]
    out = "\n".join(lines)
    (HERE / "results.md").write_text(out, encoding="utf-8")
    (HERE / "traces").mkdir(exist_ok=True)
    for v in variants:
        per = [f"# {v['label']} — DINOv2 detail ({datetime.now(timezone.utc):%Y-%m-%d})", ""]
        for c in cases:
            sc, m = grid.get(c["name"], {}).get(v["id"], (float("nan"), "missing"))
            per.append(f"- `{c['name']}` ({c.get('difficulty','')}): "
                       f"{'—' if sc != sc else f'{sc:.3f}'} [{m}] — {c.get('probe','')}")
        (HERE / "traces" / f"{v['id']}.md").write_text("\n".join(per), encoding="utf-8")
    print(out)
    print(f"\nWrote {HERE/'results.md'} + per-variant traces.")
    return out


def _score_em_block(variants: list[dict], cases: list[dict]) -> list[str]:
    """Run production Em (reference-blind) over each generated frame. SECONDARY signal.

    Reuses the shipped VisionCriticNode + manifest + merged criteria. Guards
    ANTHROPIC_API_KEY (subscription-billing safety, same as evals/vision_critic/score.py).
    """
    if os.environ.get("ANTHROPIC_API_KEY"):
        return ["> ⚠ SKIPPED Em — ANTHROPIC_API_KEY is set (would bill the API, not your "
                "subscription). `unset ANTHROPIC_API_KEY` and re-run. See score.py guard."]
    from pipeline.agents import AgentContext
    from pipeline.agents.vision_critic import VisionCriticNode
    from evals.vision_critic.score import _manifest
    from evals.vision_critic.conftest import merged_criteria

    manifest = _manifest()
    criteria = merged_criteria(manifest)
    node = VisionCriticNode()
    rows = ["| case | " + " | ".join(v["id"] for v in variants) + " |",
            "|" + "---|" * (len(variants) + 1)]
    for c in cases:
        cells = []
        for v in variants:
            gen = GENERATED / v["id"] / f"{c['name']}.png"
            if not gen.exists():
                cells.append("—")
                continue
            ctx = AgentContext(
                run_dir=Path("/tmp/reve-bakeoff"),
                inputs={"image_path": str(gen), "beat_description": c["beat_description"],
                        "frame_id": f"{v['id']}/{c['name']}", "impact_tags": [],
                        "checkpoint": c["checkpoint"], "character_id": c.get("character_id", "sean")},
                manifest=manifest, criteria=criteria, tier="draft",
                cache_dir=Path("/tmp/reve-bakeoff/.cache"),
            )
            try:
                res = node.run(ctx)
                cells.append(res.outputs["verdict"])
            except Exception as exc:  # noqa: BLE001
                cells.append(f"err:{type(exc).__name__}")
        rows.append(f"| `{c['name']}` | " + " | ".join(cells) + " |")
    rows += ["", "_Reference-blind Em. `pass` = Em accepts the output; `fail`/`borderline` = Em "
             "flags drift/register. Read as corroboration of the DINOv2 delta, not the decider._"]
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(prog="reve-nb2-bakeoff")
    ap.add_argument("--stage", choices=["generate", "score", "all"], default="all")
    ap.add_argument("--variants", nargs="+", default=None, help="subset of variant ids")
    ap.add_argument("--stub", action="store_true",
                    help="Force credential-free placeholders (no spend, no scored claim). "
                         "Stubs fire automatically when keys are absent; this is explicit.")
    ap.add_argument("--limit", type=int, default=0, help="first N cases only (smoke).")
    ap.add_argument("--score-em", action="store_true",
                    help="Also run Em (secondary, reference-blind) over the outputs. Costed; "
                         "refuses if ANTHROPIC_API_KEY is set.")
    args = ap.parse_args()

    if args.stub:  # make the explicit stub genuinely keyless even on a configured box
        os.environ.pop("REVE_API_KEY", None)
        os.environ.pop("GEMINI_API_KEY", None)

    variants = [v for v in _load("variants.yaml")["variants"]
                if not args.variants or v["id"] in args.variants]
    cases = _load("cases.yaml")["cases"]
    if args.limit:
        cases = cases[:args.limit]

    manifest = {"any_stub": args.stub}
    if args.stage in ("generate", "all"):
        manifest = generate(variants, cases, stub=args.stub)
    elif (HERE / "generate-manifest.json").exists():
        manifest = json.loads((HERE / "generate-manifest.json").read_text(encoding="utf-8"))
    if args.stage in ("score", "all"):
        score(variants, cases, manifest, args.score_em)


if __name__ == "__main__":
    main()
