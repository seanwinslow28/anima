# Implementation prompt — Cy visual-fidelity fix

*Paste-ready continuation prompt for the next Claude Code session. The diagnosis is done; this session executes. Mirrors the structure of the earlier Cy implementation prompts: binding docs → work plan → working-pattern constraints → verification. This is a CODE session — unlike the 2026-05-29 analysis session, you ship commits here.*

---

You're implementing the fix for the visual-fidelity gap diagnosed on 2026-05-29: Cy's generated Bible plates pass Gemini's Pass-3 verification but read as a *different character* than the source-ref anchor. The poses are good; the identity drifts. The full diagnosis, drift table, and root-cause trace are in `docs/2026-05-29-cy-visual-fidelity-post-mortem.md` — read it first; it is the spec for this work.

## Three decisions Sean already locked (do not re-litigate)

1. **Full-color is canonical Sean.** `anchor.png` is a color illustration; the `pencil-test-colored` IR rules are mis-specified toward monochrome graphite and must be rewritten to carry the real palette (blonde hair, navy tee, gray jeans, warm skin, blue eyes).
2. **Run the model bake-off in parallel**, not after the cheap fixes. External evidence (Google AI dev forum, Feb–Mar 2026) shows NB Pro multi-ref is structurally degraded since the 3.1 launch, so prompt-tightening alone may be capped.
3. **Adopt Opus 4.8 now** for Cy + Maya (released 2026-05-28, same price as 4.7, better judgment/honesty). Fold into the first fidelity commit. It helps author the fix; it is not itself the fix.

## Read these binding docs first, in order

1. `docs/2026-05-29-cy-visual-fidelity-post-mortem.md` — the diagnosis. §3 root cause, §5 fix candidates, §6 sequence are your marching orders.
2. `docs/anima-test-runs/2026-05-28-cy-bibles-end-to-end-against-live-models.md` — the runner-robustness history you're building on.
3. `pipeline/agents/character_designer.py` — `_run_plate` (~449), `_build_pass1_prompt` (~214). The reference-injection and prompt-construction surfaces you'll edit.
4. `pipeline/agents/nb_pro_runner.py` — `invoke_nb_pro` (81), `_build_skill_cmd` (267), `_compute_cache_key` (222). The runner contract.
5. `.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py` — confirmed correct; references reach genai as `types.Part`. Don't "fix" what isn't broken here.
6. `pipeline/agents/prompts/cy-character-designer-context.md` — the addendum whose "what good looks like" example currently models the chaining anti-pattern. You'll rewrite the reference guidance.
7. `docs/Image-Model-DR-2026/SYNTHESIS.md` §4 (layered identity defense) + the routing table — for the Track-B model candidates.

## Work plan

### Phase 0 — the disambiguating experiment (do this FIRST, ~15 min)

Before any code: re-run one drifted plate (e.g. `turnarounds/head-front.png`) by hand with **anchor-only reference + a terse prompt** ("Redraw this exact character — same face, same hair, front view. Pencil-test colored style.") via the skill script:

```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "Redraw this exact character — same face, same hair, front-facing view." \
  --reference characters/sean-anchor/anchor.png \
  --output /tmp/fidelity-test.png \
  --model gemini-3-pro-image-preview --env-file .env
```

View the output. **If fidelity jumps** → prompt-dominance was the lever; Track A will largely recover it; weight effort there. **If it stays generic** → NB Pro is the limit (root cause c); Track B is load-bearing; prioritize the bake-off. Record the result in the commit message and CHANGELOG.

### Phase 1 — Track A commit 1: prompts + runner + Opus 4.8

- **Prompt re-weighting.** In `_build_pass1_prompt` and the Cy addendum, change the contract so generated-plate prompts are **short and reference-role-tagged** ("Image A: identity anchor, match exactly; Image B: angle target"), not verbal re-descriptions of the character. Forbid pipeline-meta text in prompts (it renders as captions — see `props/stylus.png`).
- **Unconditional anchor injection.** Make the runner the source of truth: every `source: generate` plate is seeded with `anchor.png` + the relevant source-ref turnaround, **regardless of what Opus emits**, and **never** references another generated plate. Implement in `_run_plate` (resolve + prepend anchor) or `invoke_nb_pro`. Update the addendum example so it stops modeling the chaining anti-pattern.
- **Opus 4.8 bump.** Point Cy + Maya's authoring tier at the 4.8 slug. Keep it isolated enough in the diff to revert independently if an eval regresses.
- Re-bake both Bibles (live). Inspect plates visually. Expect the cache to invalidate (prompt + reference set changed → new cache keys).

### Phase 2 — Track A commit 2: the pixel-similarity gate + persisted verdicts

- Add a **Pass-2.5 node**: CLIP or DINOv2 (preferred — better for identity) or SSIM similarity between the generated plate and its target source-ref; reject below a threshold *before* Pass-3 Gemini fires.
- **Persist per-plate verdicts** to a run artifact (`runs/{run_id}/plate_verdicts.jsonl`): similarity score, Gemini verdict, confidence, cited rules. The 2026-05-28 run left no per-plate trail; fix that.

### Phase 3 — Track B (parallel): model bake-off

- Stand up a bake-off harness using the **same source-refs and the same Pass-2.5 similarity gate as the scoreboard.** Candidates: NB Pro (baseline), **FLUX.2 multi-reference** (fal/Together — up to 8–10 refs), **GPT-Image-2** edit/coherent-set, **self-hosted FLUX.1 Kontext [dev] + custom character LoRA** trained on the ~30 approved Act 1 frames (Image-Model-DR Config C), optionally + a FLUX sketch-style LoRA for the pencil register.
- Score each on identity similarity to the anchor. Pick empirically. Land the winner as the Bible-authoring generation tier in `manifest.yaml` / v2 §6.

### Phase 4 — Track A commit 3: full-color rule rewrite

- Rewrite the `pencil-test-colored` IR.\* graph and plate prompts to carry the anchor's actual color palette. Fix the `#region` crop bug (body turnarounds are currently full-sheet copies). Resolve the line-art-vs-color register inconsistency in the turnaround set. Do this *after* the winning model is known so rules are written against the renderer that will execute them.

## Working-pattern constraints

- **Each phase is a discrete commit.** Tests stay green (157 baseline) or the commit rolls back. Run `.venv/bin/pytest tests/ -q` before and after each.
- **Visual inspection is the acceptance gate**, not Gemini's pass. A plate ships when it's recognizably Sean/the-mascot, per the engine truth. Use the `Read` tool on the PNGs.
- **Don't re-enable or re-scope** the closing-the-loop Em case (7) — that's a separate follow-up session. Don't touch commit 5/6/9 work.
- **CHANGELOG every commit;** update `CLAUDE.md` only if the model assignment or the Bible-authoring contract changes structurally (Track B winner will).
- Stub-fallback is a **loud failure** now — if a re-bake stubs, fix it before proceeding (carry the test report's lesson forward).

## Verification commands

```bash
# Baseline before you start
.venv/bin/pytest tests/ -q                       # expect 157 passed

# Phase 0 experiment
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py "<terse prompt>" \
  --reference characters/sean-anchor/anchor.png --output /tmp/fidelity-test.png \
  --model gemini-3-pro-image-preview --env-file .env

# Re-bake a Bible (live)
python scripts/author_bible.py characters/sean-anchor/ \
  --studio-brief "Pencil Test reference character — see source-refs/notes.md" \
  --run-dir runs/2026-MM-DD-cy-sean-anchor-rebake/

# Review
python -m pipeline.cli bible show --character-dir characters/sean-anchor/

# After every commit
.venv/bin/pytest tests/ -q                       # must stay 157
```

The bar: open the re-baked plates next to `anchor.png` and `source-refs/turnaround-1.png`. If a stranger would say "same character," it ships. If they'd say "similar character," keep going.
