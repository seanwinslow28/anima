# evals/bakeoffs/2026-06-10-flo-inbetween-pencil-pilot/bakeoff.py
"""Flo in-between pencil-preservation pilot — a GENERATOR head-to-head for in-betweens.

Four generators (nb2 / nb-pro / fal-seedream / fal-qwen) run the SAME 14 approved Act-1
in-between cases (held prompt + references + anchors); only the engine varies. Two stages:
  generate  — each variant produces the in-between; outputs land in generated/{variant}/{case}.png
  score     — DINOv2-vs-both-endpoints (MIN; the Subject-Collapse floor, the headline) + optional
              reference-blind Em (--score-em, SECONDARY). Writes results.md + traces/.

DOCTRINE (the two earned-in-blood lessons that govern Flo-B):
  1. Verify fal transports against the LIVE API, never the doc's guesses — fal_runner REFUSES an
     unverified endpoint (STEP B0 flips it). The reve runner was first written from mirrors and was
     flatly WRONG.
  2. Sean's eye is ground truth; the metric can lie. Reve scored +0.006 DINOv2 vs NB2 on the
     in-between and Em PASSED it — but Reve MORPHS the character through the edit (DINOv2 missed it).
     So DINOv2 headlines, Em corroborates, and Sean's eye DECIDES — especially grain-preservation
     and character-morph, the two failure modes the embedding metric cannot see.

Method: docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md §3.5 (DINOv2 has
no universal threshold → the DECISION is the fal-vs-nb2 DELTA on the same case + both endpoints; a
still-image MLLM is trustworthy mainly pairwise → Em-absolute is a secondary corroborator) + §6
(report per-case below-threshold COUNT, not a mean that hides one catastrophic drift; stderr()).

Usage:
    # credential-free plumbing check (CI-safe; stub outputs, no spend, no scored claim):
    .venv/bin/python evals/bakeoffs/2026-06-10-flo-inbetween-pencil-pilot/bakeoff.py --stage all --stub

    # live (costed): set FAL_KEY (+ GEMINI_API_KEY for nb2/nb-pro); ANTHROPIC_API_KEY UNSET
    # (subscription billing). DINOv2 needs torch+transformers. Smoke first with --limit 2.
    .venv/bin/python evals/bakeoffs/2026-06-10-flo-inbetween-pencil-pilot/bakeoff.py --stage generate --limit 2
    .venv/bin/python evals/bakeoffs/2026-06-10-flo-inbetween-pencil-pilot/bakeoff.py --stage score --score-em
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

import yaml
from dotenv import load_dotenv

load_dotenv()

from pipeline.agents import fal_runner
from pipeline.agents.fal_runner import invoke_fal_qwen, invoke_fal_seedream
from pipeline.agents.nb_pro_runner import invoke_image_edit
from pipeline.agents.similarity_gate import SIMILARITY_FLAG_THRESHOLD, compute_similarity
from evals.vision_critic.scoring import stderr

GENERATED = HERE / "generated"
CACHE = HERE / ".cache"


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
                # Hard short-circuit: NEVER call a runner under --stub. The nb runners re-read
                # .env directly (invoke_image_edit's _has_gemini_api_key honors the .env FILE),
                # so popping the env var is not enough — a populated .env would otherwise fire a
                # REAL, COSTED call under --stub. Writing the placeholder here guarantees $0 and
                # a consistent keyless stub for every engine.
                fal_runner._write_placeholder_png(out)
                stub_used = True
            elif v["engine"] in ("nb2", "nb_pro"):
                r = invoke_image_edit(
                    prompt=case["prompt"], reference_images=refs, output_path=out,
                    cache_dir=CACHE / v["id"], model=v["model"],
                )
                stub_used = r.stub_fallback
            elif v["engine"] == "fal_seedream":
                r = invoke_fal_seedream(
                    prompt=case["prompt"], reference_images=refs, output_path=out,
                    cache_dir=CACHE / v["id"],
                )
                stub_used = r.stub_fallback
            elif v["engine"] == "fal_qwen":
                r = invoke_fal_qwen(
                    prompt=case["prompt"], reference_images=refs, output_path=out,
                    cache_dir=CACHE / v["id"], denoise=v.get("denoise"),
                )
                stub_used = r.stub_fallback
            else:
                raise ValueError(f"unknown engine: {v['engine']}")
            any_stub = any_stub or stub_used
            tag = " [STUB]" if stub_used else ""
            print(f"  {v['id']:>14} | {case['name']:<16} -> {out.name}{tag}")
            manifest["rows"].append({
                "variant": v["id"], "case": case["name"], "engine": v["engine"],
                "tier": v.get("tier"), "output": str(out.relative_to(HERE)),
                "stub_fallback": stub_used, "cost_usd": v["cost_per_image_usd"],
            })
    manifest["any_stub"] = any_stub
    (HERE / "generate-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if any_stub:
        print("\n⚠ At least one output is a STUB placeholder — DINOv2/Em scores on it are "
              "NOT a scored claim (set FAL_KEY + GEMINI_API_KEY and verify endpoints in B0).")
    return manifest


# --------------------------------------------------------------------------- #
# Stage 2 — score (DINOv2 primary; Em optional/secondary)
# --------------------------------------------------------------------------- #
def _dinov2_score(generated: Path, anchors: list[Path]) -> tuple[float, str]:
    """Min DINOv2 cosine across both endpoints (Subject-Collapse floor)."""
    results = [compute_similarity(generated, a) for a in anchors]
    worst = min(results, key=lambda r: r.score)
    return worst.score, worst.method


def _fal_ids(variants: list[dict]) -> list[str]:
    return [v["id"] for v in variants if str(v["engine"]).startswith("fal")]


def score(variants: list[dict], cases: list[dict], manifest: dict, score_em: bool) -> str:
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
    fal_ids = _fal_ids(variants)

    lines = [
        f"# Flo in-between pencil-preservation pilot — {datetime.now(timezone.utc):%Y-%m-%d}",
        "",
        "In-between generator head-to-head. **Headline metric: DINOv2 vs BOTH endpoints (MIN)**, "
        f"read as the **Δ vs the `{baseline}` baseline** on the same case (eval-strategy §3.5: no "
        "universal DINO threshold — the delta is the signal). Em (if run) is a **secondary** "
        "corroborator. **Sean's eye on grain + character-morph is the FINAL arbiter** — the two "
        "failure modes DINOv2 cannot see (the Reve lesson).",
        "",
        f"**DINOv2 method engaged:** {', '.join(sorted(method_seen)) or 'none'} "
        "(`pil-perceptual` = torch/transformers absent → NOT a real identity read; install "
        "`torch torchvision transformers` for the DINOv2 tier).",
        "",
        f"**Stub run:** {'YES — placeholder outputs, NOT a scored claim' if manifest.get('any_stub') else 'no (real generations)'}",
        "",
        "## DINOv2 identity hold — case × variant (MIN over both endpoints; higher = closer)",
        "",
        "| case | difficulty | " + " | ".join(vids) + f" | Δ(best fal − {baseline}) |",
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
        fal_scores = [row.get(fid, (float("nan"), ""))[0] for fid in fal_ids]
        fal_scores = [s for s in fal_scores if s == s]
        if fal_scores and base_sc == base_sc:
            delta = max(fal_scores) - base_sc
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
                  if grid.get(c["name"], {}).get(v["id"], (float("nan"),))[0]
                  == grid.get(c["name"], {}).get(v["id"], (float("nan"),))[0]]
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
        f"- **Decision metric:** the Δ column (best fal − `{baseline}`) + the Subject-Collapse "
        "count. A fal variant earns *wire as the in-between route* only if its DINOv2 **matches or "
        f"beats `{baseline}`** and shows no collapse — AND Sean's eye confirms grain + identity.",
        "- **Sean's eye is the FINAL arbiter** (the Reve lesson — DINOv2 missed the morph). On the "
        "generated frames vs each case's `reference_target` IB, judge: (a) **grain preservation** — "
        "graphite line + cream-paper texture kept, or denoised to clean digital? (b) **character-"
        "morph** — does the figure stay *itself* through the tween, or drift like Reve? (c) "
        "instruction-follow on the tween pose.",
        "- **Em is secondary.** Reference-blind Em corroborates SF01/register and flags gross drift; "
        "it cannot truly verify identity (the documented limitation).",
        "- **Decision rule:** wire the winner ONLY if it holds grain **and** identity by Sean's eye "
        f"AND its DINOv2 doesn't collapse. **If BOTH fal models slick the pencil → pivot: route "
        f"in-betweens to `{baseline}`** (the locked fallback) and ticket self-hosted FLUX + Shakker "
        "sketch-LoRA. **Never** declare a winner off a `pil-perceptual` run or a `--stub` run.",
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
                run_dir=Path("/tmp/flo-inbetween-bakeoff"),
                inputs={"image_path": str(gen), "beat_description": c["beat_description"],
                        "frame_id": f"{v['id']}/{c['name']}", "impact_tags": [],
                        "checkpoint": c["checkpoint"], "character_id": c.get("character_id", "sean")},
                manifest=manifest, criteria=criteria, tier="draft",
                cache_dir=Path("/tmp/flo-inbetween-bakeoff/.cache"),
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
    ap = argparse.ArgumentParser(prog="flo-inbetween-bakeoff")
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
        os.environ.pop("FAL_KEY", None)
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
