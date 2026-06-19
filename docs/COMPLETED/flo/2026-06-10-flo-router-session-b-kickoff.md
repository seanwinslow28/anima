# Kickoff — Flo Router, Session B: the costed fal.ai in-between pencil-preservation pilot

*Paste-ready brief for a **Claude Code** session. **COSTED — bounded fal.ai + Gemini spend** (~$10–15 ceiling). Builds the empirical half of Flo: a pencil-preservation benchmark that runs **Seedream 4.0 + Qwen-Image-Edit (fal.ai)** against the **NB2 / NB Pro** incumbents through identical in-between prompts, scores grain / identity / instruction-follow, and wires the winner as the `in_between_*` route — or pivots in-betweens to NB2 (the locked fallback) if both fal.ai models slick the pencil. Scope LOCKED proceed-as-planned (Sean, 2026-06-10). Plan of record: [`docs/2026-06-10-flo-router-build-plan.md`](2026-06-10-flo-router-build-plan.md) §Flo-B. Builds directly on Flo-A (PR #43, merged).*

**Standing doctrine: verify against the tree AND the real transports — never the label.** Two earned-in-blood lessons govern this session:
1. **The transport schema you assume is probably wrong.** The neighboring Reve bake-off's runner was first written from third-party mirrors and was **flatly incorrect** (`prompt`/`image`/`data[0].b64_json` — none real); it only worked after being corrected from the live API's own error messages. **Verify the fal.ai Seedream + Qwen call shapes against the live API BEFORE the benchmark depends on them** (STEP B0). Do not trust this doc's endpoint guesses.
2. **Sean's eye is ground truth; the metric can lie.** The Reve bake-off (2026-06-08) showed reve-fast **+0.006 DINOv2 vs NB2** on the in-between case and Em **passed** it — by the numbers, a win. Sean's eye then **disqualified it**: Reve *morphs the character through the edit* — great at creating images, wrong for in-betweens. DINOv2 missed the morph entirely. So: **DINOv2 is the headline, Em is secondary, and Sean's review is the final arbiter — especially for grain preservation and character-morph, the two failure modes the embedding metric does not see.** Reve is therefore **out of this lineup** (kept in the kit for future character/background *creation*).

## ⚠ FIRST — divergence + tree guard
1. `git fetch origin && git rev-list --left-right --count main...origin/main` → expect `0 0`. `git log --oneline -3` should show `4560a44` (Flo Session A, #43) in history; `git status -s` → clean.
2. **Verdict-baseline guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` → **`2af75906502f1caf8857e18828ceb2e4`**, byte-identical through ALL of Session B. Flo-B is additive — it writes only under `evals/bakeoffs/` and edits `manifest.yaml` + `pipeline/agents/frame_router.py`; **never touch `evals/vision_critic/`**.
3. Branch an isolated worktree `feature/flo-router-b` off `origin/main`.

## ⚠ §0 — before ANY spend (fleet-ops; this is a costed run)
Full protocol: [`docs/fleet-ops-protocol.md`](../../architecture/fleet-ops-protocol.md) §Pre-costed-run checklist. The one-screen version:
1. `echo "${ANTHROPIC_API_KEY:+SET}"` prints **nothing** · `claude /status` shows **subscription** — so Em's Opus escalation bills the subscription, not the API. (The scoring harness must **refuse `--score-em` if `ANTHROPIC_API_KEY` is set**, mirroring `evals/vision_critic/score.py`'s guard.)
2. `FAL_KEY` + `GEMINI_API_KEY` present in the **worktree** `.env` (FAL_KEY already exists from Seedance). No keys echoed to logs.
3. Singleton confirmed (`ps`/`lsof` clean) · own PID resolved up the ppid chain · single owner.
4. **Smoke first** (`--stage all --stub` for plumbing, then `--limit 2` live), then the full run.
5. At end: orphan sweep clean; worktree removed on merge.

## Read, in order
1. [`docs/2026-06-10-flo-router-build-plan.md`](2026-06-10-flo-router-build-plan.md) **§Flo-B** — the approved plan.
2. **The harness to MIRROR (this is the template — clone its shape):** [`evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/`](../../../evals/bakeoffs/2026-06-07-reve-vs-nb2-editing) — `README.md` (the metric contract + decision rule), `variants.yaml` (pinned snapshots + per-variant engine/tier/cost), `cases.yaml` (per-view-anchor + Em fields; the `t3-inbetween-*` case is your starting shape), `bakeoff.py` (`--stage generate|score|all`, `--stub`, `--score-em`), `reve_runner.py` (the self-stubbing transport pattern to copy for fal), `results.md` (the output format).
3. **The metric law:** [`docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md`](../../research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md) **§3.5** (DINOv2-vs-per-view-anchor is the visual groundedness metric; MLLM judge trustworthy mainly **pairwise**; report Subject-Collapse count + stderr, not just a mean) + **§6** (generator row).
4. **The model facts:** [`docs/Image-Model-DR-2026/SYNTHESIS.md`](../../Image-Model-DR-2026/SYNTHESIS.md) **§2** (Seedream 4.0 ~$0.007–0.03, Qwen-IE-2511 ~$0.021, "zero documented pencil/non-photoreal testing → validate before committing"; Qwen denoise sweet-spot 0.78–0.82).
5. **The existing fal.ai pattern to reuse:** [`pipeline/seedance_generate.py`](../../../pipeline/seedance_generate.py) (`fal_client.subscribe(model_id, arguments=...)`, `fal_client.upload_file`, URL download) — the fal transport idiom already in the repo.
6. **The wire-in target:** [`pipeline/agents/frame_router.py`](../../../pipeline/agents/frame_router.py) (`_WIRED_TRANSPORTS`, the `RouteNotWiredError` seam) + the `generation.routing:` block in [`manifest.yaml`](../../../manifest.yaml).

## The corpus — build it from the approved pencil archive
The in-between ground truth already exists. `runs/run_2026-04-04_174805/approved/` (gitignored, present in the working tree) carries **7 Act-1 transitions with 14 approved in-between targets**:

| transition (endpoints) | approved IB targets |
|---|---|
| `PT_A1_F01_key` → `PT_A1_F06_key` | IB01, IB02, IB03 |
| `PT_A1_F06_key` → `PT_A1_F10_key` | IB01 |
| `PT_A1_F10_key` → `PT_A1_F13_key` | IB01 |
| `PT_A1_F13_key` → `PT_A1_F18_key` | IB01, IB02, IB03 |
| `PT_A1_F28_key` → `PT_A1_F31_key` | IB01, IB02 |
| `PT_A1_F31_key` → `PT_A1_F36_key` | IB01, IB02 |
| `PT_A1_F36_key` → `PT_A1_F40_key` | IB01, IB02 |

- Each case = `{endpoint A keyframe, endpoint B keyframe}` → the model generates the in-between; **score the output's DINOv2 against BOTH endpoints and take the MIN** (the Subject-Collapse floor, per the reve `t3-inbetween` case + eval-strategy §3.5). The approved `IB*` frame is the **visual reference for what a good in-between looks like** (Sean's grain/morph review), not a DINOv2 target.
- **Commit the endpoint keyframes (and the IB references) under `evals/bakeoffs/<dated>/fixtures/`** — `runs/` is gitignored and absent from the worktree, so the bake-off must be self-contained (exactly what the reve bake-off did with F06/F10).
- **n=14 is the self-contained floor** — already far more robust than the reve in-between n=1. If Sean wants the full 20–50-pair power the plan mentions, he can drop additional before/after pairs from his Procreate archive into `fixtures/` and add cases; flag this as an **optional top-up**, don't block on it. SHIPS-RED: do not relax a case so a variant passes.

## STEP B0 — verify the fal transports LIVE, before spend (the gate)
The single most important step — the reve-schema-was-wrong lesson. **Before writing the runners against an assumed shape:**
- Confirm the **Seedream 4.0 edit** endpoint id + argument schema against the live fal.ai model page / a single probe call. The repo's research names `fal-ai/bytedance/seedream/v4/edit` ([SYNTHESIS §2 / prompt-1-perplexity.md ref 47]) — **verify it**, and capture the real arg names (image-to-image edit takes a prompt + reference image URL(s); confirm `image_urls` vs `image_url`, edit-vs-generate route, output field).
- Confirm the **Qwen-Image-Edit-2511** fal endpoint id (candidates: `fal-ai/qwen-image-edit` / `…-plus` / a `-2511` variant) + arg schema + whether denoise/strength is exposed (sweet-spot 0.78–0.82). **Do not assume** — probe or read the live model page.
- **Pin the verified endpoint ids + schemas + observed served-model strings into `variants.yaml` `snapshots:`** (mirroring how the reve `snapshots:` block pins `reve-edit@20250915`). A provider bump re-baselines against this row.
- Reference upload: reuse `fal_client.upload_file` (the Seedance idiom) to get reference image URLs.

## STEP B1 — the fal runners (mirror `reve_runner.py`)
- `evals/bakeoffs/<dated>/fal_runner.py`: one self-stubbing entry point per engine (`invoke_fal_seedream`, `invoke_fal_qwen`), copying `reve_runner.py`'s shape — **stub when `FAL_KEY` absent** (placeholder PNG, `stub_fallback=True`, so the harness is CI-green and a populated `.env` can't fire a silent costed call), content-addressed cache, typed response envelope (`ok`, `cost_usd`, `endpoint`, `cache_hit`). Real path behind `fal_client.subscribe`.
- The runner **refuses an unknown/unverified endpoint** rather than silently calling the wrong thing (the reve fast-version guard pattern).

## STEP B2 — the bake-off harness (clone the reve structure)
A new dated dir `evals/bakeoffs/2026-06-1X-flo-inbetween-pencil-pilot/`:
- `variants.yaml`: `nb2` (incumbent baseline, $0.067) · `nb-pro` (hero ceiling, $0.15) · `fal-seedream` (~$0.02) · `fal-qwen` (~$0.021). Pin snapshots. NB2/NB Pro route through the already-wired `nb_pro_runner.invoke_image_edit`.
- `cases.yaml`: the 14 in-between cases above (endpoints as `references`, both endpoints as `per_view_anchors`, the approved IB as a `reference_target` note, identical in-between `prompt` per case, `register: pencil-test-colored`, Em fields per the reve schema). Hold prompt + references + anchors **constant across variants** — only the engine varies.
- `bakeoff.py`: `--stage generate|score|all`, `--stub`, `--score-em`. Generate → `generated/{variant}/{case}.png` (gitignored). Score → DINOv2 ladder (`compute_similarity`, install `torch torchvision transformers` or it degrades to `pil-perceptual` — the trace must say which tier engaged; a `pil-perceptual` run is **not** a verdict) + optional reference-blind Em (secondary).

## STEP B3 — the costed run (smoke, then full)
1. **Plumbing:** `python …/bakeoff.py --stage all --stub` → gray placeholders, $0, proves wiring.
2. **Live smoke:** `--limit 2` (or 2 cases) live → confirm real fal generations land, costs log, DINOv2 tier engaged. Inspect the 2 outputs by eye before spending on the full set.
3. **Full:** `--stage generate` (all 4 variants × 14 cases ≈ 56 generations) then `--stage score --score-em`. Writes `results.md` + `traces/`. Bounded ceiling ~$10–15; stop and report if it trends over.

## STEP B4 — score + DECIDE (Sean's eye is the arbiter)
Read `results.md`, then **Sean reviews the generated in-betweens directly** — this is the decisive step, because of the Reve morph the metric missed:
- **DINOv2 Δ vs NB2** (headline, per case + Subject-Collapse count + stderr) — identity hold across the in-between.
- **Em verdicts** (secondary corroboration of SF01/register drift).
- **Sean's eye (FINAL):** (a) **grain preservation** — does the output keep graphite line + cream-paper texture, or did the model denoise the pencil into clean digital? (b) **character-morph** — does the figure stay *itself* through the tween, or drift like Reve did? (c) instruction-follow on the in-between pose.
- **Decision rule:** wire the winner ONLY if it holds grain **and** identity by Sean's eye AND its DINOv2 doesn't collapse. **If BOTH fal.ai models slick the pencil aesthetic → pivot: route in-betweens to NB2** (the locked fallback) and ticket self-hosted FLUX + Shakker sketch-LoRA as the $0-ongoing future. Never declare a winner off a `pil-perceptual` or `--stub` run.

## STEP B5 — wire the winner into Flo (or record the NB2 pivot)
- **If a fal model wins:** add its transport to `pipeline/agents/frame_router.py` (extend `_WIRED_TRANSPORTS` + a dispatch branch calling the new `fal_runner` entry point; thread `references`/`prompt`/`tier` through like the nb_pro branch) and **flip its route `status: declared → wired`** in `manifest.yaml` `generation.routing:`. Keep the other fal route `declared`.
- **If NB2 wins the pivot:** point `in_between_cheap`/`in_between_mid` at `transport: nb2` (or set `fallback`-routing), leave the fal routes `declared` with a note, and ticket FLUX.
- Either way: a short **live keyframe-route smoke** (one hero→NB Pro + one standard→NB2 dispatch through `FloNode`) to confirm the wired routes fire live — the smoke Flo-A deferred — then **flip the CLAUDE.md Skills-Map Flo row → built** with the state-of-record (winner, the Reve-disqualified note, the corpus + numbers).

## Deliverables checklist (Flo-B)
- [ ] §0 + tree guard logged (divergence `0 0`, baseline md5 unchanged, `ANTHROPIC_API_KEY` absent, clean worktree).
- [ ] B0: fal Seedream + Qwen endpoints + schemas **verified live** and pinned in `variants.yaml snapshots:`.
- [ ] `evals/bakeoffs/2026-06-1X-flo-inbetween-pencil-pilot/` — `variants.yaml` + `cases.yaml` (14 cases) + `fal_runner.py` + `bakeoff.py` + committed `fixtures/`; `--stub` CI-green.
- [ ] Costed run executed (smoke → full); `results.md` + `traces/` written; DINOv2 tier confirmed real (not `pil-perceptual`).
- [ ] Sean's eye review on grain + morph; decision recorded (fal winner wired, or NB2 pivot + FLUX ticket).
- [ ] Winner wired into `frame_router.py` + route `status` flipped (or NB2 pivot recorded); live keyframe-route smoke passed.
- [ ] CLAUDE.md Flo row → built (with the Reve-disqualified-for-in-betweens note); CHANGELOG entry; field report under `docs/anima-test-runs/`; land via squash PR off `origin/main`; orphan sweep clean.

## Fleet-ops + mistake ledger (carry these)
Isolated worktree off `origin/main` · single owner · §0 before AND after · subscription billing (`ANTHROPIC_API_KEY` absent) · bounded `FAL_KEY`/`GEMINI_API_KEY` from the worktree `.env` · smoke before full · squash PR · clean teardown. **Verify the fal schemas live before the benchmark leans on them. DINOv2 headlines, Em corroborates, Sean's eye decides. A declared route stays an honest not-wired error until B5 wires it. Back-compat intact. Never touch `evals/vision_critic/`.**
