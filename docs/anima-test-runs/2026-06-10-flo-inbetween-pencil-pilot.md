# Field report — Flo-B: the fal in-between pencil-preservation pilot (NB2 pivot)

**Date:** 2026-06-10 · **Spend:** ~$0.58 (2 B0 probes + an 8-frame smoke) · **Outcome:** NB2 pivot
**Branch:** `feature/flo-router-b` (worktree) off `origin/main` `112a99b` · **Plan:** [build-plan §Flo-B](../COMPLETED/flo/2026-06-10-flo-router-build-plan.md) · **Kickoff:** [session-b-kickoff](../COMPLETED/flo/2026-06-10-flo-router-session-b-kickoff.md)

## TL;DR

The costed Flo-B pilot asked: can a fal.ai image-edit model preserve the pencil-test aesthetic AND
character identity through an in-between well enough to wire as Flo's `in_between_*` route? **No.**
Sean's eye disqualified both candidates on the live smoke — **fal Seedream morphs the face through
the tween** (the exact Reve failure DINOv2 misses) and **fal Qwen-Image-Edit-Plus reframes/degrades
("terrible")**. We took the **pre-committed NB2 pivot**: in-betweens route to **NB2** (winner) with
**NB Pro** as the quality backup; the verified fal transports are retained for future non-pencil
creation; **self-hosted FLUX + Shakker sketch-LoRA is ticketed** as the $0-ongoing future.

## Fleet-ops (§0 before AND after)

- Isolated worktree off `origin/main`; divergence `0 0` at start; single owner; orphan sweep clean
  at end. `ANTHROPIC_API_KEY` absent throughout (no API billing; Em never invoked — the smoke was
  decisive). `FAL_KEY` + `GEMINI_API_KEY` bounded from the worktree `.env` (copied in only at the
  costed phase; absent during the $0 harness build so a key couldn't fire a silent call).
- Em's verdict baseline `traces/g6.1b-criteria-attached-2026-06-08.md`
  (`md5 2af75906502f1caf8857e18828ceb2e4`) byte-identical before and after — Flo-B never touched
  `evals/vision_critic/`.
- One operational note: a leftover `--stage all --stub` background process was still in the slow
  DINOv2 score stage at the start of the costed phase; stopped cleanly (TaskStop) before any spend
  to honor the singleton rule.

## STEP B0 — verify the fal transports LIVE (the gate)

The reve-was-wrong lesson, applied: `fal_runner.py` shipped the endpoint ids as **unverified
candidates** that **refuse** the real path until B0. B0 verified against the live fal OpenAPI
(first-party) + confirming single probes:

- **Seedream** `fal-ai/bytedance/seedream/v4/edit` — candidate id correct; `{prompt, image_urls[]}`;
  output `images[].url`; **default 2048² square** → forced 16:9. Probe: real 1376×768, 283 KB.
- **Qwen** — candidate `fal-ai/qwen-image-edit` was **wrong for the task**: it takes a *single*
  image, unusable for a two-endpoint tween. Corrected to **`fal-ai/qwen-image-edit-plus`** (the
  multi-image variant). **No `denoise`/`strength` knob exists** (the kickoff's 0.78–0.82 sweet-spot
  is not exposed on this endpoint) — ran at fal defaults (guidance 4 / 50 steps); default square_hd
  → forced 16:9. Probe: real 1376×768, 904 KB. (Slow: ~3–4 min at 50 steps.)

Both flipped to `verified=True`; snapshots pinned in `variants.yaml`; the refusal mechanism is still
tested by forcing `verified=False`.

## Live smoke (the eyeball gate Sean chose)

`bakeoff.py --stage generate --limit 2` → 8 real frames (4 variants × 2 cases, transition F01→F06,
IB at 25% + 50%), ~$0.53. Per-case 4-way comparison montages built for review. Observations Sean
ratified:

- **nb2 / nb-pro** — hold identity + pencil register; render 1024² square (the Gemini skill ignores
  16:9, a known incumbent quirk, not a regression).
- **fal-seedream** — strongest grain of the four, *close* — but **morphs the face** through the
  edit. The Reve trap exactly: great image, wrong for in-betweens.
- **fal-qwen-plus** — reframes/zooms the shot; composition instability ("terrible").

## Decision + wiring (B5 — NB2 pivot)

- `manifest.yaml generation.routing:` — `in_between_cheap → nb2` (winner), `in_between_mid → nb_pro`
  (backup), both `status: wired`. No new dispatch code: nb2/nb_pro were already in
  `_WIRED_TRANSPORTS`, so the pivot is a manifest repoint. The deferred `mask_edit` (gpt_image_2)
  remains the lone not-wired seam (still raises `RouteNotWiredError`).
- TDD: `tests/test_frame_router.py` +1 positive pivot test (`…in_between_pivot_routes_to_wired_nb…`);
  the old `in_between_cheap`-based not-wired + lowered-confidence tests repointed to `mask_edit`.
  Full contract suite **493 passed**.
- The verified fal transports stay in `pipeline/agents/fal_runner.py` (9 tests) — retained, not
  deleted; the harness is re-runnable for a FLUX or future-model re-test.

## Ticket filed (code-brain manual lane)

**Self-hosted FLUX + Shakker sketch-LoRA for pencil in-betweens** — the $0-ongoing future. API
image-edit models hope-and-pray on grain/identity preservation; a self-hosted FLUX + sketch-LoRA
controls the aesthetic at generation time. Re-evaluate via this same bake-off harness (drop it in as
a variant, run the full 4×14). Until then NB2/NB Pro own in-betweens.

## What was NOT done (by design)

The full 4×14 costed run — Sean stopped at the smoke (Engine Truth: the eye had seen enough, and the
fal morph is the known repeatable signature). The live keyframe-route FloNode smoke (Flo-A's
deferral) was also not spent on separately — nb2 + nb_pro fired live in this very bake-off via the
same `invoke_image_edit` transport FloNode dispatches, so the wired routes are live-proven.
