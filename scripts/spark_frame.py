#!/usr/bin/env python3
"""Phase 5 per-frame driver for "The Spark, Shared" — the hand-wired Flo → T1 → Em chain.

The first integrated run has no `run` orchestrator; this script IS the Phase-5
hand-wiring (one of the seams the run exists to surface). It drives ONE frame at
a time so the human-gated chain holds: generate frame N, T1 + Em critique, Sean's
eye, approve → only then chain N+1 (which references N's approved frame).

  python scripts/spark_frame.py --frame 1                  # generate + critique F01
  python scripts/spark_frame.py --frame 1 --approve --attempt 1   # lock F01 -> approved/
  python scripts/spark_frame.py --frame 2                  # (after F01 approved) ...

Per frame it:
  - resolves references (Bible anchors + A-7 pairing for F01; F01 + prior-approved
    + the beat's mascot plate for F02-05) — the two-character chain is manual (seam).
  - runs Flo (FloNode, standard_keyframe -> NB2, 16:9) -> candidates/F0n/attempt_NN.png
  - runs T1 HF01 (deterministic 16:9 PIL check).
  - runs Em (VisionCriticNode) TWICE — character_id="sean" then "claude-mascot" — so
    BOTH Bibles' IR rules surface in Em's criteria block (Em is single-character; seam).
    Gemini-tier by default (the validated 0.97/1.00/0.00 baseline; ~15s); confidence
    < threshold auto-escalates to Opus. --escalate forces the Opus read.
  - stages Em's proposed_patches by hand (stage_patches_hook is a DAG post_run hook
    that inline run() does NOT fire — seam) and appends verdicts to em_verdicts.jsonl.

Engine Truth: Sean's eye is the arbiter on the no-morph two-character bar; T1 + Em
corroborate. --approve copies the chosen attempt to approved/SS_F0n_key.png.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT))

# Populate NODE_REGISTRY + import the nodes/helpers we drive by hand.
import pipeline.agents.frame_router  # noqa: F401  (registers "flo")
import pipeline.agents.vision_critic  # noqa: F401  (registers "vision_critic")
from pipeline.agents import AgentContext  # noqa: E402
from pipeline.agents.frame_router import FloNode  # noqa: E402
from pipeline.agents.vision_critic import VisionCriticNode, EmptyCitesInvariant  # noqa: E402
from pipeline.agents.patch_stager import stage_patches_hook  # noqa: E402
from pipeline.criteria import load_all_criteria  # noqa: E402
from pipeline.audit import check_aspect_ratio  # noqa: E402

RUN_DIR = Path("runs/2026-06-11-spark-shared-first-integrated")
SLUG = "SS"  # The Spark, Shared
CHARS = Path("characters")
SEAN_ANCHOR = CHARS / "sean-anchor" / "anchor.png"
MASCOT_ANCHOR = CHARS / "claude-mascot" / "anchor.png"
A7_PAIRING = CHARS / "claude-mascot" / "source-refs" / "sean-with-claude-mascot.png"
MASCOT = CHARS / "claude-mascot"

_STYLE = (
    "Pencil test animation key drawing on cream paper with visible paper grain; "
    "warm graphite line, light construction lines and sparse cross-hatching for shading; "
    "hand-drawn rough animation, soft colored-pencil fills in the pencil-test-colored register. "
    "16:9 widescreen, fixed camera, locked framing. NOT a clean digital, anime, or 3D render."
)

# Per-frame spec: beat (for Em), the NB2 prompt, and the beat-specific mascot plate.
FRAMES: dict[int, dict] = {
    1: {
        "beat": "Establishing two-shot: Sean three-quarter at his desk, focused down on the page, "
                "stylus in his RIGHT hand to paper; the Claude mascot perched on his shoulder, idle/neutral. "
                "Sets look, framing, scale — the compositional anchor the chain hangs from.",
        "prompt": (
            "Wide two-shot establishing frame. A young man (Sean) seated three-quarter view at a drawing "
            "desk, head down and focused on the page, a stylus held in his RIGHT hand touching the paper "
            "mid-stroke. A small terracotta-orange box-shaped creature (the Claude mascot) perches on his "
            "shoulder, idle and neutral, facing forward at a small consistent scale. Both fully in frame, "
            "calm and companionable. " + _STYLE
        ),
        "mascot_plate": None,  # A-7 pairing carries the perch in F01
    },
    2: {
        "beat": "The draw: Sean stays focused, his right hand with the stylus moving along the paper; "
                "the mascot turns its head to LOOK down at what he is making (look plate).",
        "prompt": (
            "Same two-shot, same framing and identities. Sean stays focused down on the page, his RIGHT "
            "hand with the stylus moving along the paper mid-stroke. The terracotta box-creature on his "
            "shoulder turns its head to LOOK down at the drawing, curious, just beginning to notice. " + _STYLE
        ),
        "mascot_plate": MASCOT / "motion_plates" / "look-01.png",
    },
    3: {
        "beat": "The notice: Sean keeps drawing, head down, stylus in right hand; the mascot perks up "
                "alert — body lifting, attention sharpening — the spark of catching the idea (alert-perk).",
        "prompt": (
            "Same two-shot. Sean continues drawing, head down, stylus in his RIGHT hand. The mascot on his "
            "shoulder perks up ALERT — its small box body lifting slightly, attention sharpening on the "
            "drawing, the spark of catching the idea. " + _STYLE
        ),
        "mascot_plate": MASCOT / "expressions" / "alert-perk.png",
    },
    4: {
        "beat": "The delight: Sean stays absorbed in the work, head down, stylus in right hand, unchanged; "
                "the mascot reacts with small, genuine delight at the drawing — a quiet beat, not a gag.",
        "prompt": (
            "Same two-shot. Sean stays absorbed in the work, head down, stylus in his RIGHT hand, unchanged. "
            "The terracotta box-creature on his shoulder reacts with small, genuine DELIGHT at the drawing — "
            "a quiet, happy, earned beat, not a big cartoon take, not mugging at the camera. " + _STYLE
        ),
        "mascot_plate": MASCOT / "expressions" / "delight.png",
    },
    5: {
        "beat": "The settle: the mascot eases back toward idle/perched; Sean's drawing hand returns to its "
                "start position; composition matches F01 so the loop closes cleanly (idle plate).",
        "prompt": (
            "Same two-shot, returning to the opening composition. The terracotta box-creature eases back "
            "down toward its idle perched pose, settling. Sean's RIGHT hand with the stylus returns to its "
            "starting position on the page, head still down. Framing and scale match the establishing frame "
            "so the cycle reads continuous when looped. " + _STYLE
        ),
        "mascot_plate": MASCOT / "motion_plates" / "idle-01.png",
    },
}

EM_CHARS = ("sean", "claude-mascot")  # IR namespaces (NOT folder keys) for Em's criteria block


def approved_path(n: int) -> Path:
    return RUN_DIR / "approved" / f"{SLUG}_F{n:02d}_key.png"


def resolve_references(n: int) -> list[str]:
    """Two-character chain (manual — no schema expresses it). F01 anchors both Bibles +
    the A-7 pairing; F02-05 chain F01 + the prior approved frame + the beat's mascot plate."""
    if n == 1:
        refs = [SEAN_ANCHOR, MASCOT_ANCHOR, A7_PAIRING]
    else:
        f1 = approved_path(1)
        prior = approved_path(n - 1)
        missing = [str(p) for p in (f1, prior) if not p.exists()]
        if missing:
            sys.exit(f"error: F{n:02d} needs approved frames that don't exist yet: {missing}. "
                     f"Approve the prior frame(s) first (--approve).")
        refs = [f1, prior, SEAN_ANCHOR]
        plate = FRAMES[n].get("mascot_plate")
        if plate:
            refs.append(plate)
    # dedup preserving order (F01 == prior when n==2)
    seen: set[str] = set()
    deduped: list = []
    for p in refs:
        if str(p) not in seen:
            seen.add(str(p))
            deduped.append(p)
    return [str(p) for p in deduped]


def _load_ctx_pieces():
    manifest = yaml.safe_load((Path("manifest.yaml")).read_text(encoding="utf-8"))
    bundle = load_all_criteria(manifest)
    return manifest, bundle


def generate(n: int, manifest: dict, bundle, note: str | None = None) -> str:
    spec = FRAMES[n]
    refs = resolve_references(n)
    prompt = spec["prompt"]
    if note:
        prompt = prompt + f"\n\nCORRECTION (re-roll, address the prior attempt's defect): {note}"
    print(f"\n=== Flo: generate F{n:02d} (standard_keyframe -> NB2, 16:9) ===")
    print(f"  references ({len(refs)}):")
    for r in refs:
        print(f"    - {r}")
    if note:
        print(f"  correction note: {note}")
    ctx = AgentContext(
        run_dir=RUN_DIR,
        inputs={
            "frame_num": n,
            "prompt": prompt,
            "references": refs,
            "shot_type": "standard_keyframe",
            "character_id": "sean-anchor",  # FloNode style_register lookup (manifest key)
        },
        manifest=manifest, criteria=bundle, tier="draft",
        cache_dir=RUN_DIR / ".cache", extras={},
    )
    t0 = time.monotonic()
    result = FloNode().run(ctx)
    cand = result.outputs["candidate_path"]
    print(f"  -> {cand}  ({time.monotonic()-t0:.0f}s)  {result.notes}")
    return cand


def t1_audit(cand: str) -> dict:
    print("\n=== T1: HF01 aspect-ratio (16:9 ±2%, deterministic) ===")
    res = check_aspect_ratio(Path(cand))
    print(f"  {res}")
    return res


def em_critique(n: int, cand: str, manifest: dict, bundle, *, escalate: bool) -> list[dict]:
    spec = FRAMES[n]
    verdicts = []
    stage = stage_patches_hook(RUN_DIR)
    impact_tags = ["identity_critical"] if escalate else []  # [] = Gemini-tier; identity_critical forces Opus
    for cid in EM_CHARS:
        print(f"\n=== Em (T2): F{n:02d} vs {cid} Bible  ({'Opus-forced' if escalate else 'Gemini-tier'}) ===")
        ctx = AgentContext(
            run_dir=RUN_DIR,
            inputs={
                "image_path": cand,
                "beat_description": spec["beat"],
                "frame_id": f"{SLUG}_F{n:02d}",
                "impact_tags": impact_tags,
                "checkpoint": "phase_5_generate",
                "character_id": cid,
            },
            manifest=manifest, criteria=bundle, tier="draft",
            cache_dir=RUN_DIR / ".cache", extras={},
        )
        t0 = time.monotonic()
        try:
            r = VisionCriticNode().run(ctx)
            stage(f"vision_critic:{cid}:F{n:02d}", r)  # patches don't stage off-DAG; do it by hand
            v = {
                "frame": f"{SLUG}_F{n:02d}", "character": cid,
                "verdict": r.outputs["verdict"], "confidence": r.outputs["confidence"],
                "cites": r.cites_criteria, "patches": len(r.proposed_patches),
                "reasoning": r.outputs["reasoning"], "notes": r.notes,
            }
        except EmptyCitesInvariant as e:
            v = {
                "frame": f"{SLUG}_F{n:02d}", "character": cid,
                "verdict": "human_review (empty-cites invariant)", "confidence": None,
                "cites": [], "patches": 0, "reasoning": e.reasoning, "notes": "EmptyCitesInvariant",
            }
        dt = time.monotonic() - t0
        print(f"  verdict={v['verdict']} confidence={v['confidence']} cites={v['cites']} "
              f"patches={v['patches']}  ({dt:.0f}s)  {v.get('notes','')}")
        if v.get("reasoning"):
            print(f"  reasoning: {v['reasoning'][:500]}")
        verdicts.append(v)
    # Append to the run's verdict trail (no node does this off-DAG).
    vlog = RUN_DIR / "em_verdicts.jsonl"
    with vlog.open("a", encoding="utf-8") as fh:
        for v in verdicts:
            fh.write(json.dumps(v) + "\n")
    return verdicts


def do_approve(n: int, attempt: int) -> None:
    cand = RUN_DIR / "candidates" / f"F{n:02d}" / f"attempt_{attempt:02d}.png"
    if not cand.exists():
        sys.exit(f"error: candidate not found: {cand}")
    dst = approved_path(n)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(cand, dst)
    log = RUN_DIR / "approved" / "approvals.jsonl"
    with log.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"frame": f"{SLUG}_F{n:02d}", "attempt": attempt,
                             "candidate": str(cand), "approved": str(dst)}) + "\n")
    print(f"approved: {cand} -> {dst}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Phase 5 per-frame driver (Flo + T1 + Em).")
    ap.add_argument("--frame", type=int, required=True, choices=range(1, 6))
    ap.add_argument("--approve", action="store_true", help="Copy --attempt to approved/ (Sean's eye said go).")
    ap.add_argument("--attempt", type=int, default=None, help="Attempt number to approve (with --approve).")
    ap.add_argument("--escalate", action="store_true", help="Force Em's Opus read (identity_critical).")
    ap.add_argument("--note", default=None, help="Correction note appended to the prompt on a re-roll (retry ladder).")
    args = ap.parse_args()

    for sub in ("candidates", "approved", "rejected", "audit", "export"):
        (RUN_DIR / sub).mkdir(parents=True, exist_ok=True)

    if args.approve:
        if args.attempt is None:
            sys.exit("error: --approve needs --attempt N")
        do_approve(args.frame, args.attempt)
        return 0

    manifest, bundle = _load_ctx_pieces()
    cand = generate(args.frame, manifest, bundle, note=args.note)
    t1 = t1_audit(cand)
    verdicts = em_critique(args.frame, cand, manifest, bundle, escalate=args.escalate)

    print("\n=== SUMMARY ===")
    print(f"frame F{args.frame:02d}  candidate: {cand}")
    print(f"  T1 HF01: {t1.get('result', '?')} ({t1.get('dimensions','?')}, dev {t1.get('deviation','?')})")
    for v in verdicts:
        print(f"  Em[{v['character']}]: {v['verdict']} (conf={v['confidence']}, cites={v['cites']})")
    print("\nNext: review the image (Sean's eye on the no-morph bar). If good:")
    attempt_guess = cand.split("attempt_")[-1].split(".")[0]
    print(f"  python scripts/spark_frame.py --frame {args.frame} --approve --attempt {int(attempt_guess)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
