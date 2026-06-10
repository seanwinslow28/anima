# Flo in-between pencil-preservation pilot — results

> **DECIDED 2026-06-10 — NB2 PIVOT (Sean's eyeball verdict).** The full 4×14 run was **not** run:
> the live smoke was decisive. This is the Engine-Truth pattern — Sean's eye is the final arbiter,
> and on the in-between task it overrides the embedding metric (which demonstrably misses the
> face-morph; that is the whole Reve lesson this pilot was built to re-test). Hand-authored, not
> score-generated — a 2-case DINOv2 matrix would not change a verdict the eye already made.

## What ran (~$0.58 total)

1. **B0 — both fal transports verified LIVE** against the live fal OpenAPI (first-party) **and**
   confirming single probes (real 1376×768 outputs):
   - Seedream = `fal-ai/bytedance/seedream/v4/edit` (candidate id was right).
   - Qwen = **corrected to `fal-ai/qwen-image-edit-plus`** — the base `qwen-image-edit` takes a
     single image, unusable for a two-endpoint tween. **No denoise/strength knob exists** on it
     (the kickoff's "0.78–0.82" is not real here); ran at fal defaults (guidance 4 / 50 steps).
   - Both default to a **square** output → forced to the 16:9 source-frame size.
2. **Live smoke** — 8 real frames, 4 variants × 2 cases (transition F01→F06, IB at 25% and 50%).
   Comparison montages saved to `/tmp/flo-smoke-compare/` at run time; full-res frames in
   `generated/{variant}/` (gitignored).

## The verdict (Sean's eye)

| variant | call | why |
|---|---|---|
| **nb2** | **WINNER** → in-between default | holds identity + pencil register through the tween |
| **nb-pro** | **BACKUP** → in-between quality tier | same, painterly ceiling when NB2 isn't enough |
| **fal-seedream** | DISQUALIFIED | *close*, strong grain — but **morphs the face through the edit** (the exact Reve failure DINOv2 misses) |
| **fal-qwen-plus** | DISQUALIFIED | "terrible" — reframes/zooms the shot, composition instability |

The headline finding repeats the 2026-06-08 Reve postmortem precisely: a fal image-edit model can
score well on grain/embedding yet **morph the character identity through the tween**, which is
fatal for in-betweens and invisible to DINOv2. The metric can pass it; the eye disqualifies it.

## The decision — NB2 pivot (the pre-committed fallback)

Per the decision rule ("if both fal models slick/morph the pencil → pivot: route in-betweens to NB2
and ticket self-hosted FLUX"):

- **`in_between_cheap` → `nb2`** (winner), **`in_between_mid` → `nb_pro`** (backup) in
  `manifest.yaml generation.routing:` — both `status: wired` (they were already-wired transports,
  so the pivot is a manifest repoint, no new dispatch code).
- The **verified** fal transports stay in `pipeline/agents/fal_runner.py` (tested, live-proven) —
  retained for future **non-pencil creation** use, not pencil in-betweens.
- **Ticketed:** self-hosted **FLUX + Shakker sketch-LoRA** as the $0-ongoing in-between future
  (the path that controls grain at generation time instead of hoping an API preserves it).

## Provenance / honesty

- Decision made on the **F01→F06** transition (2 IBs) across all 4 variants — one transition, but
  the failure mode (Seedream face-morph) is the known, repeatable fal/Reve signature, and Sean
  stopped before the full ~$10–15 run by design (cost-disciplined: the eye had seen enough).
- `nb2`/`nb-pro` rendered **1024² square** in the smoke (the Gemini skill ignores 16:9 — a known
  incumbent behavior, not a regression); the fal variants honored 16:9. A framing confound noted
  for completeness; it does not affect the identity-morph verdict.
- The harness (`variants.yaml` + `cases.yaml` (14) + `bakeoff.py` + committed `fixtures/`) and the
  verified `fal_runner.py` are retained and re-runnable — if FLUX or a new fal model warrants a
  re-test, drop it in as a variant and run the full 4×14.
