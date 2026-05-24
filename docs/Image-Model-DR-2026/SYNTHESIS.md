# Image Model Research — Cross-Source Synthesis

**Created:** 2026-05-24
**Sources:** 9 deep-research reports (Perplexity / Gemini / ChatGPT × Prompts 1–3) + 3 last30days scans + 2 Gemini charts in this directory.
**Purpose:** Decision doc for replacing Nano Banana 2 on in-between frames without losing character identity or pencil aesthetic. Read this first; raw reports are the receipts.

---

## 1. Headlines (the 5 things that change the plan)

1. **Sean's NB2 cost baseline is wrong.** $0.039/img was Nano Banana **1** (Gemini 2.5 Flash). NB2 is token-priced at ~$0.067/img (1K) and ~$0.151/img (4K). Perplexity Prompt 3 caught this; ChatGPT and Gemini Prompt 1 both repeated the legacy figure. The economics for replacing NB2 are even better than the original brief assumed.

2. **The cheapest legitimate alternative is ByteDance — Seedream 4.0 / SeedEdit 3.0 at ~$0.007–$0.03/image** on fal.ai. That's the $7-per-1,000-frames figure on Gemini's cost chart. 5–10× cheaper than NB2 with the strongest content-preservation benchmarks in any closed editor (56.1% usability vs GPT-4o 37.1%). The catch: zero documented testing on pencil/non-photoreal content. Validate before committing.

3. **The consensus self-hosted stack is settled.** FLUX.1 Kontext [dev] FP8 + character LoRA (ai-toolkit, ~30 NB2 keyframes, ~2hrs on a 4090) + PuLID-FLUX v0.9.1 + ControlNet OpenPose/Lineart + Shakker-Labs pencil-style LoRA. 4/4 sources converge here. Runs in 24GB; $0 marginal cost after training.

4. **Qwen-Image-Edit-2511 is the open-source dark horse.** 3/4 sources rank it the #1 open editor for sketch input ("handles even the most awful sketches" — r/StableDiffusion). Apache 2.0, ~24GB VRAM (8GB via GGUF), native ComfyUI, dual VL+VAE encoder purpose-built for appearance preservation. ~$0.021/img on fal.ai if Sean doesn't want to self-host. **This is the single highest-ROI experiment** — one Sunday afternoon in ComfyUI tells you whether the in-between problem is solved.

5. **Pencil aesthetic preservation is an unsolved benchmark.** Every editing and identity model in the survey was trained on photoreal/clean digital — they treat pencil grain as noise to denoise away. No public benchmark exists for cream-paper preservation. Mitigations exist (Shakker sketch LoRA, custom pencil-style LoRA, EbSynth 2.0 pixel propagation), but Sean would be among the first practitioners building this — community workflows for "pencil-aesthetic editing" don't yet exist as discoverable Reddit threads. Plan to build the benchmark himself.

---

## 2. Consensus picks by job

| Job | Consensus pick | Confidence | Cost | Backup |
|---|---|---|---|---|
| **Keyframe (hero quality)** | Nano Banana **Pro** (the new NB2 hero tier) | 4/4 | ~$0.15/img | GPT-Image-2, FLUX.2 [pro] multi-ref |
| **Keyframe (standard)** | Nano Banana 2 OR GPT-Image-2 | 4/4 | ~$0.07/img | FLUX.2 [pro] |
| **In-between generation (closed)** | **FLUX.1 Kontext [pro]** | 4/4 | $0.04/img | FLUX.2 [pro] multi-ref |
| **In-between generation (open, 24GB)** | **FLUX.1 Kontext [dev]** FP8 + char LoRA | 4/4 | $0 | Qwen-Image-Edit-2511 |
| **Frame edit (cheap, instruction)** | **Seedream 4.0 / SeedEdit 3.0** | 3/4 | $0.007–0.03/img | Qwen-IE-2511 via fal.ai ($0.021) |
| **Frame edit (mask-precise)** | GPT-Image-2 `/images/edits` | 3/4 | ~$0.21/img | BrushNet + SD3.5 (open) |
| **Frame edit (open, 24GB)** | **Qwen-Image-Edit-2511 + Canny ControlNet** | 4/4 | $0 | FLUX Kontext [dev] + Shakker LoRA |
| **Identity lock (FLUX, no training)** | **PuLID-FLUX v0.9.1** (face) + InstantCharacter (body) | 3/4 + 2/4 | $0 | — |
| **Identity lock (FLUX, trained)** | **Character LoRA via ai-toolkit (ostris)** | 4/4 | $0 + ~2hr train | SimpleTuner, kohya |
| **Pencil/style lock** | **Shakker-Labs `FLUX.1-Kontext-dev-LoRA-Sketch-Style`** | 3/4 | $0 | Train custom LoRA on 30+ pencil frames |
| **In-between interpolation (pencil-safe)** | **GMFSS Fortuna VFI** (optical flow, anime-tuned) | 1/4 outlier but credible | $0 | ToonCrafter (line-art diffusion, 512px cap) |
| **Aesthetic propagation (boiling grain fix)** | **EbSynth 2.0** | 1/4 outlier (Gemini) | $0–$ | — |

**Disqualified:** Midjourney V7 (no programmatic API — 4/4 unanimous), IP-Adapter-FaceID / InstantID / PhotoMaker for FLUX (superseded, photoreal-only), Ideogram 3.0 ($0.10–0.15/img with character ref — pricier than NB2), OmniGen2 pointed at raw pencil frames (paper explicitly flags sensitivity to noisy/textured input — Gemini missed this).

---

## 3. Things the DR engines missed (worth investigating)

- **GPT-Image-2 multi-image coherent sets** — up to 8 frames of the same character/world from one prompt. Practitioner-confirmed in April–May 2026 YouTube head-to-heads, absent from Perplexity and Gemini DR (likely post-cutoff). Structurally this is what the in-between problem needs. Sean already uses gpt-image-1; upgrading to v2 is the smaller hop than a model swap.
- **ByteDance "Lance" (3B, Apache 2.0, May 18 2026)** — unified image+video understanding/generation/editing. Top r/StableDiffusion thread in last30days (369 upvotes). Missing from all 3 DR reports. Worth a 1-hour evaluation; potential single-model collapse of the entire generate+edit+interpolate stack if it delivers.
- **"Grid Method" with Qwen + LTX Two** for character consistency across video frames (Jan 2026) — surfaced in last30days, no DR coverage. Worth a 1-hour test if Qwen-IE pans out.
- **PuLID-FLUX2 Klein node** (March 2026) — work-in-progress port. Revisit Q3 2026.

---

## 4. Pencil aesthetic — the risk that could kill any plan

Every model in this survey will, by default, "fix" Sean's pencil lines into clean digital strokes. The fix isn't model selection alone — it's a layered defense:

1. **Style-lock LoRA**, always. Either Shakker-Labs `FLUX.1-Kontext-dev-LoRA-Sketch-Style` (free, generic) or — better — a custom LoRA trained on 30–50 of Sean's own approved pencil keyframes (~30–60 min on a 4090 via ai-toolkit). The training set IS the style anchor.
2. **Aggressive negative prompting**: "no digital polish, no clean render, no anti-aliasing, no smoothing, no vector lines".
3. **Lower denoise on edit operations** — Qwen-IE community sweet spot is 0.78–0.82, not the default. Above 0.85 it fully re-renders; below 0.75 the edit doesn't take.
4. **For motion sequences: EbSynth 2.0 propagation** of one hand-drawn hero pencil look across generative motion frames. Non-generative pixel-level texture synthesis = solves the "boiling grain" failure mode that all diffusion models share. Genuinely worth piloting given Sean already has hand-drawn hero frames.
5. **Differential Diffusion** (no public ComfyUI implementation yet, but documented) — gradient mask blending preserves cream-paper texture at edit boundaries. Theoretical best for seam-free local edits.

**No formal benchmark exists** for pencil-on-cream preservation. Sean should build a 20-pair before/after benchmark from his own archive, run Qwen-IE-2511, Nano Banana Pro, and FLUX+Shakker through identical prompts, and score for grain preservation, identity, instruction-follow. That benchmark becomes a competitive moat for the portfolio piece itself ("how I evaluated and chose").

---

## 5. The three unified configurations

### Config A — Best Quality (hero keyframes, money-no-object)
- **Generate:** Nano Banana **Pro** OR FLUX.2 [pro] with up to 8–10 reference images (start + end + A-2 anchor + 2–3 character sheet angles)
- **Edit:** GPT-Image-2 `/images/edits` with mask for precise region work
- **Identity:** native multi-ref conditioning (NB Pro takes up to 14 refs; FLUX.2 takes 10)
- **Pencil lock:** Shakker sketch LoRA via Replicate FLUX wrapper OR custom-trained LoRA
- **Cost:** ~$0.10–0.21/frame, similar to current NB2 spend
- **Use for:** hero keyframes that ship to the portfolio
- **Failure mode:** FLUX.2's photorealism bias scrubs pencil grain unless aggressively negative-prompted

### Config B — Best Value (in-between fixes, biggest cost cut)
- **Generate in-between candidates:** Seedance 2.0 (current) → keep
- **Edit in-betweens:** **Seedream 4.0 on fal.ai at ~$0.007–$0.03/img** for routine fixes → fall back to **Qwen-Image-Edit-2511 on fal.ai at $0.021/img** when Seedream slicks the pencil → escalate to **Nano Banana Pro at ~$0.15** only for hero shots
- **Identity:** rely on multi-image conditioning + good prompting; no LoRA needed for this tier
- **Pencil lock:** prompt-locked + GPT-Image-2 mask endpoint for region isolation
- **Cost:** $7–$30 per 1,000 in-between edits vs ~$70 at NB2's actual price → **80% cost reduction**
- **Use for:** the bulk of Act 2 in-between editing work
- **Failure mode:** Seedream has zero documented non-photoreal testing — needs a 50-frame pilot first

### Config C — Fully Self-Hosted (24GB rig, $0 ongoing)
- **Generate:** FLUX.1 Kontext [dev] FP8 (12GB VRAM, ~30–80s/frame on 4090)
- **Identity (custom, required for quality):** Character LoRA trained on ~30 NB2 keyframes via ai-toolkit (ostris) — FLUX.1-dev base, rank 16–32, 2,000 steps, LR 1e-4 cosine, empty captions, fp8, ~30–45 min on 4090
- **Identity (face lock, optional):** PuLID-FLUX v0.9.1 with `timestep_to_start_inserting_ID=1`, strength 0.75, fake CFG
- **Pencil style:** Shakker-Labs `FLUX.1-Kontext-dev-LoRA-Sketch-Style` OR custom pencil LoRA, loaded at 0.5–0.7 strength
- **Control:** ControlNet OpenPose + Lineart at 0.55–0.65 strength
- **Edit:** Qwen-Image-Edit-2511 in ComfyUI with Canny ControlNet (strength 0.6–0.8, denoise 0.78–0.82)
- **Interpolate (pencil-safe upsample):** GMFSS Fortuna VFI post-process for 2×/4× frame interpolation; fallback to ToonCrafter for full diffusion-based in-betweens (caps at 512×320, needs upscale)
- **Aesthetic glue:** EbSynth 2.0 to propagate hand-drawn hero pencil look across motion sequences
- **Cost:** $0 marginal after ~2hr training run
- **Failure mode:** combined LoRA strength sum > 1.2 causes interference; ToonCrafter 512px cap; PuLID + LoRAs at 12GB FP8 is at the 24GB ceiling — close everything else

---

## 6. Tomorrow-morning experiment plan (ranked by ROI)

Three time-boxed experiments. Stop at the first one that solves the problem.

### Experiment 1 — Train a character LoRA on FLUX.1-dev (one Sunday afternoon, ~3hrs total)
- Install ai-toolkit on the 4090
- Curate 30 of the best NB2-approved Act 1 keyframes (already exist in `runs/run_2026-04-04_*/approved/`)
- Train at rank 16, 2,000 steps, empty captions, fp8 — ~45 min
- Inference test: generate 10 in-between candidates with LoRA @ 0.65 + Shakker sketch LoRA @ 0.6 + PuLID-FLUX (no training needed) + ControlNet OpenPose
- **Pass criterion:** identity recognizable as Sean across 8/10 frames AND pencil grain preserved (no slicking)
- **ROI:** unlocks Config C entirely. This is the highest-leverage single move. Required for any serious self-hosted plan.

### Experiment 2 — Qwen-Image-Edit-2511 in ComfyUI for targeted edits (~1 hr)
- Install Qwen-IE-2511 ComfyUI node (native support)
- Take 5 existing NB2 keyframes, attempt 5 representative edits: "change hand pose", "redraw eyes with different expression", "extend paper canvas", "fix stylus angle", "add background detail"
- Use Canny ControlNet @ 0.6–0.8, denoise 0.78–0.82
- **Pass criterion:** 4/5 edits preserve pencil aesthetic AND only modify the requested region
- **ROI:** if Qwen-IE works for edits, Sean's per-edit cost drops from $0.07–0.21 (NB2/GPT) to $0. This is the single highest-ROI cost cut available.

### Experiment 3 — $5 Seedream 4.0 pilot via fal.ai (~30 min)
- Send 50 Seedance-extracted in-between candidates through Seedream 4.0 with cleanup prompts
- Compare against NB2 cleanup of the same 50 (already-existing cost reference)
- **Pass criterion:** 35/50 outputs are usable in-betweens (vs NB2's ~45/50 baseline) AND retain pencil character
- **ROI:** if Seedream passes, that's 80% cost reduction on bulk in-between cleanup with zero infrastructure work. Even at 35/50 (70% usability) the math still wins.

**Total time investment for all three: ~5 hours. Total dollar cost: ~$5.** Outcomes drive which configuration ships.

---

## 7. What to defer

- **FLUX.2 [dev] on the 4090** — community quantized ports were not stable at research date. Revisit when r/StableDiffusion confirms a working FP8 build.
- **OmniGen2** — the paper explicitly flags sensitivity to noisy/textured input; do not point at raw pencil. Revisit only if a pencil-tuned community variant ships.
- **HunyuanImage 3.0 Instruct (80B MoE)** — even NF4-quantized needs ~48GB. Out of reach.
- **InstantCharacter beyond a 1hr sanity test** — promising but no benchmarks for pencil-extreme-pose preservation.
- **"Grid Method"** with Qwen + LTX Two — 1-hour test only if Qwen-IE passes Experiment 2.
- **ByteDance Lance** — 1-hour evaluation only if it gains community traction in next 30 days; right now it's a single Reddit thread.

---

## 8. Open questions (Sean must test himself)

- Pencil "boil" (frame-to-frame line micro-jitter) — every source flags this as untested by current models. EbSynth pilot may be the answer.
- Whether a custom pencil-style LoRA trained on Sean's own frames beats the generic Shakker sketch LoRA — likely yes but unmeasured.
- Differential Diffusion + Qwen — theoretically the cleanest seam-free local-edit pipeline, no public ComfyUI implementation yet.
- Optimal Qwen denoise for Sean's specific paper grain (community range 0.75–0.85 is wide).
- HiDream-O1-Image pixel-space (no VAE) architecture — theoretically superior for raw grain preservation, untested in production.

---

## 9. Source map (where each claim came from)

| Source | Strongest on | Weakest on |
|---|---|---|
| Perplexity Prompt 1/2/3 | Recent practitioner sources, correct NB2 pricing, model limitations | Long synthesis tables |
| Gemini Prompt 1/2/3 | Long structured tables, academic citations, cost graphs | Missed NB1→NB2 pricing change; over-rated OmniGen2 |
| ChatGPT Prompt 1/2/3 | Synthesis logic, hybrid recommendations | Prompt 2 came back short (~1.5KB); legacy NB2 pricing |
| last30days scan | Caught GPT-Image-2 dominance and ByteDance Lance — both post-DR-cutoff | Thin signal overall (community hasn't built pencil workflows yet) |
| Gemini cost graph (PNG) | Confirmed SeedEdit 3.0 = $7/1K-frames ≈ 82% cheaper than NB2 tier | Excluded SeedEdit from its own proposed workflow |
| Gemini workflow diagram (PNG) | OmniGen2-for-bulk + Recraft-for-hero hybrid concept | Routed to wrong open model (OmniGen2 fails on pencil per Perplexity); skipped the cheaper SeedEdit option |

Raw reports: `prompt-{1,2,3}-{chatgpt,gemini,perplexity}.md` and `*-raw-last30days.md` in this directory.
