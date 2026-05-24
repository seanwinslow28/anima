# 2026 State-of-the-Art: Instruction-Driven Image Editing for 2D Animation Pipelines

*Prepared for a pencil-test animation workflow. Research conducted May 24, 2026. All leaderboard data current as of research date.*

***

## Executive Summary

The instruction-driven image editing landscape has undergone substantial restructuring since early 2025. The closed-source tier has consolidated around four serious competitors — **Nano Banana 2 (Gemini 3.1 Flash Image)**, **Nano Banana Pro (Gemini 3 Pro Image)**, **GPT Image 2**, and **ByteDance SeedEdit 3.0 / Seedream 4.0** — while the open-source tier has been reshaped by three high-impact releases: **FLUX.1 Kontext**, **Qwen-Image-Edit-2509**, and **OmniGen2**, with two newcomers (**ByteDance Lance** and **HiDream-O1-Image**) entering directly in May 2026.

**The single most important finding for your use case** is that the benchmark gap everyone missed is real and remains unsolved: no 2026 head-to-head benchmark has explicitly tested *pencil-on-cream / non-photorealistic preservation during targeted edits*. However, practitioner evidence from Reddit, Hugging Face, and YouTube is strong enough to rank models with reasonable confidence. The short answer: **Qwen-Image-Edit-2509 is the safest bet for non-photoreal preservation among open-source options**, and **Nano Banana Pro is the safest closed-source option**, but neither has been formally tested against pencil-test animation frames.

A critical platform note: the mask-based editing endpoint `imagen-3.0-capability-001` that supported explicit mask input is being retired June 30, 2026, with the recommended migration being `gemini-2.5-flash-image` (i.e., Nano Banana 2), which uses a different invocation paradigm without explicit mask support.[^1]

***

## Verdict on the Known State

### Nano Banana 2 — Current Production Editor

**Verdict: Confirmed leading, significant caveats.**

The "Nano Banana 2" in your Known State corresponds to **Gemini 2.5 Flash Image**, launched August 2025 at $0.039/image. However, the product line has advanced substantially:[^2]

- **Nano Banana Pro (Gemini 3 Pro Image)** launched November 2025, leads the Artificial Analysis Image Editing Arena at Elo 1240 and is positioned as the premium option for complex edits.[^3]
- **Nano Banana 2 (Gemini 3.1 Flash Image)** launched February 2026 is a *different, newer model* — faster, roughly half the cost of Nano Banana Pro, with 4K resolution support. On Artificial Analysis it scores Elo 1236 on image editing, very close to the Pro tier at 4–6× lower cost.[^4][^3]

Your pipeline's "$0.039/image" figure was accurate for Gemini 2.5 Flash Image (Nano Banana 1). Nano Banana 2 pricing is output-token based: approximately $0.067 per 1024×1024 image, $0.101 per 2K, $0.151 per 4K. **This is materially more expensive than the baseline you noted.** Gemini 2.5 Flash Image at $0.039 is still available but is the previous-generation model.[^4]

The claim that NB2 wins "category 3 (image editing) on integration quality" over GPT Image 2 is largely borne out by independent testing: DigitalOcean's October 2025 head-to-head confirmed Nano Banana and Qwen as leaders in style-coherent edits, with Nano Banana winning on background inpainting quality.[^5]

Nano Banana Pro now supports **handwriting replication and style consistency across hand-drawn inputs** — users on r/nanobanana have documented it successfully preserving sketch-style character identity across re-prompts. This is the only closed-source model with *any* documented user evidence of non-photorealistic handling.[^6][^7]

### GPT Image 2 — Text Rendering & Face Lock Leader

**Verdict: Confirmed but superseded in key respects.**

GPT Image 2 launched April 21, 2026. On Artificial Analysis, **GPT Image 1.5 (high) actually leads image editing at Elo 1264**, with GPT Image 2 (high) at Elo 1253 — a slight regression in the editing arena despite overall generation improvements. The resolution cap claim (1K) in your Known State is incorrect: GPT Image 1.5 supported up to 1536×1024, and GPT Image 2 is expected to support higher, though exact maximums have not been officially confirmed at time of writing.[^8][^9][^10][^3]

Pricing via OpenAI API (token-based): approximately $0.006 (low/1024), $0.053 (medium), $0.211 (high) per image at standard sizes. At high quality, this is roughly 5–14× more expensive than Nano Banana 2, confirming your cost estimate directionally.[^11]

The known advantage of GPT Image 2 for locking a reference face pixel-perfect appears confirmed by the observation that it uses native image generation inside the GPT-5 neural network rather than a separate diffusion model, which enables better reference fidelity. However, the DigitalOcean test shows that Qwen-Image-Edit-2509 now matches or exceeds GPT Image on many precise editing tasks.[^12][^5]

### SeedEdit 3.0 — "Evidence Too Thin" → **Now Confirmed**

**Verdict: Confirmed leading on content preservation benchmarks; commercial availability thin; superseded by Seedream 4.0 for unified workflows.**

SeedEdit 3.0's technical report confirms it achieves a **56.1% usability rate** on ByteDance's internal benchmark vs. GPT-4o (37.1%) and Gemini 2.0 (30.3%). Specific strengths: face/ID preservation, background fidelity, and 4K processing. The model was available via Imdream web platform and Doubao app as of June 2025, but there is no self-hosted open API.[^13][^14][^15]

More importantly, **ByteDance released Seedream 4.0 in September 2025**, which merges Seedream 3.0 text-to-image and SeedEdit 3.0 editing into a single unified model. Priced at ~$0.03/image on fal.ai — below Nano Banana 2. User reports indicate "accurate text-driven edits, 2K in under 2s, 4K support," but these are community claims not audited lab tests. Public leaderboards still show Gemini above Seedream 4.0 on editing.[^16]

**Critical gap for your use case**: Neither SeedEdit 3.0 nor Seedream 4.0 has any documented testing on hand-drawn or pencil-style inputs. The model's training data is described as real and synthetic photographic images.[^14][^13]

### FLUX.1 Kontext [dev] — Character Preservation Leader

**Verdict: Confirmed leading on character/identity preservation; caveats on non-photoreal styles.**

FLUX.1 Kontext released May 2025, 12B parameters, rectified flow transformer. The [dev] variant runs locally and was confirmed to fit on a 24GB GPU (full model) or 16GB GPU (FP8 quantized version). Non-commercial license confirmed for [dev]; commercial use requires Kontext [pro] or [max] via API.[^17][^18]

**Critical finding for your use case**: Multiple Reddit threads and practitioner reports confirm FLUX.1 Kontext [dev] has documented problems with anime/manga/illustrative styles. Specifically: oversaturated colors, wrong proportions, and style drift when editing non-photorealistic inputs. The FLUX base model has a photorealistic bias — users report it "defaults to anime happy" unexpectedly but simultaneously produces inauthentic-looking anime when deliberately prompted for it. The [dev] version's style transfer capability is described as "quite limited" compared to Pro/Max.[^19][^20][^21][^22]

**However**, a mitigation exists: the Shakker-Labs sketch-style LoRA (`FLUX.1-Kontext-dev-LoRA-Sketch-Style`) released July 2025 explicitly enables conversion of real photos to/from sketch style using FLUX Kontext. This is the most relevant practitioner tool for your workflow. Training your own sketch→edit LoRA using before/after pencil-frame pairs is also well-documented via Scenario and Hugging Face.[^23][^24]

Multi-turn artifact degradation is a confirmed limitation: Black Forest Labs acknowledged this in their own technical report — after ~6 iterative edits, images show visible quality degradation. Independently confirmed by practitioners.[^25][^18]

### Qwen-Image-Edit — Targeted Edit Leader

**Verdict: Confirmed leading; 2509 update is the recommended version.**

The original Qwen-Image-Edit (August 2025) is 20B, Apache 2.0, and confirmed as the best open-source model on Artificial Analysis editing rankings at the time of the DigitalOcean review. **Qwen-Image-Edit-2509** (September 2025) materially improves on it: multi-image editing (1–3 inputs), better face/identity preservation, native ControlNet support for depth maps, edge maps, and keypoint maps.[^26][^27][^5]

The most relevant practitioner evidence: a YouTube tutorial from October 2025 shows **converting a hand-drawn UFO sketch into a finished image using Qwen-Image-Edit-2509**, adjusting denoise strength (0.80–0.85) to control how much the model deviates from the original sketch lines. A Reddit thread from September 2025 confirms the model handles "even the most awful sketches" effectively, converting rough pencil drawings to finished images. A Hugging Face discussion from November 2025 mentions using Qwen Image Edit for colouring rough sketches, though with noted difficulty getting it to preserve a "pencil/light sketch aesthetic" rather than fully rendering the image.[^28][^29][^30]

**Qwen-Image-Edit-2511** was released December 2025 with further improvements. Apache 2.0 license confirmed for all versions.[^31]

The dual architecture (Qwen2.5-VL semantic encoder + VAE appearance encoder) is specifically designed to balance instruction-following with appearance preservation — directly relevant to your "change the hand pose, preserve the face" use case.[^5]

### OmniGen2 — Complex Instruction Leader

**Verdict: Confirmed leading among open-source on complex instruction tasks; sensitivity to low-res/noisy inputs is a specific concern for pencil frames.**

OmniGen2 released June 2025, paper updated April 2026. Architecture: Qwen2.5-VL-3B MLLM + 4B Diffusion Transformer with unshared parameters. Achieves SOTA among open-source on ImgEdit-Bench, particularly strong on "action editing" due to video-sourced training data. License: Apache 2.0 (confirmed via GitHub).[^32][^33][^34]

**Critical caveat for your use case**: The OmniGen2 paper explicitly lists "sensitivity to input image quality (noise, low resolution)" as a known limitation. Pencil-test frames on cream paper with graphite grain may trigger this sensitivity. Not recommended as primary editor for raw pencil frames without pre-processing.[^32]

### ByteDance Lance

**Verdict: Too new to fully evaluate; promising architecture but 40GB RAM requirement is a constraint.**

Lance (released May 21, 2026, Apache 2.0) is a 3B unified model covering image/video understanding, generation, and editing. YouTube reviewers confirm image editing benchmarks claim wins over FLUX.1-dev, Qwen-Image, and GPT Image 1. However, the inference requirement is 40GB+ RAM, which exceeds a typical 24GB VRAM GPU setup. Independent editing quality tests are not yet available as of the research date. **Treat as experimental; monitor the ecosystem over the next 2–3 months.**[^35][^36][^37][^38]

***

## Section 1: Closed-Source Landscape — Verified & Extended

### Google Nano Banana Family

| Model | Official Name | Release | Price/Image (1K) | Editing Invocation | Max Res |
|---|---|---|---|---|---|
| Nano Banana 1 | Gemini 2.5 Flash Image | Aug 2025 | ~$0.039 | Instruction | 2K[^2] |
| Nano Banana Pro | Gemini 3 Pro Image | Nov 2025 | Higher | Instruction / multi-turn | 4K[^39] |
| Nano Banana 2 | Gemini 3.1 Flash Image | Feb 2026 | ~$0.067–0.151 | Instruction / multi-turn | 4K[^4] |

Nano Banana 2 is the current production-tier option. Its API uses `generateContent` without explicit mask input — instruction-based only. Character consistency is confirmed for up to 5 characters/14 objects. **For non-photorealistic inputs**: users document successful preservation of handwriting style and sketch-style character identity, making it the closed-source model with the most evidence of non-photoreal handling, though no formal pencil-animation tests exist.[^7][^1][^6][^4]

Nano Banana Pro (Gemini 3 Pro Image) scored highest on the SiliconFlow image editing leaderboard at Elo 1,257 and is described as offering "state-of-the-art reasoning" for complex multi-turn edits. For hero-shot quality, Nano Banana Pro is the recommended closed-source option.[^39][^40]

### OpenAI GPT Image Family

GPT Image 2 (released April 2026) adds native 4K, improved multilingual text rendering, and stronger reference-locking vs. GPT Image 1.5. Invocation: instruction-based (`/v1/images/edits`), with optional mask image input — the only major closed-source model that still accepts explicit mask files. This is architecturally important for your pipeline: mask input means you can precisely isolate a hand region for editing without risking context bleed.[^41][^9][^8]

GPT Image 2 Artificial Analysis Elo: 1253 (editing, high quality) — currently second overall behind GPT Image 1.5 in the editing arena. Cost at high quality: ~$0.133–0.211 per standard image. **Verdict**: Best option if you need exact mask-based region isolation (e.g., "change only the hand pose") and can tolerate 5–14× the cost.[^11][^3]

### ByteDance SeedEdit 3.0 / Seedream 4.0

SeedEdit 3.0 achieved SOTA on ByteDance's internal 23-category benchmark with 56.1% usability rate, outperforming GPT-4o and Gemini 2.0 significantly. Strong specifically on: face alignment, text rendering, complex lighting transformations, and shadow coherence during object removal. Invocation: instruction-based, image URL + prompt + guidance scale.[^42][^13][^14]

**Seedream 4.0** (September 2025) integrates SeedEdit 3.0 into a unified model available on fal.ai at $0.03/image. Claims wins on instruction adherence and editing retention vs. Gemini, but no leaderboard confirmation yet. API stability: fal.ai hosted, not self-deployable, no SLA documentation found.[^16]

**Non-photoreal testing**: None documented. The model's benchmark suite covers portrait editing, background changes, and scene transitions — all photorealistic categories.[^13]

### Adobe Firefly (Generative Fill API)

Adobe Firefly's April 2026 update added **Precision Flow** (slider-based edit strength control, regional selection) and **AI Markup** (draw/annotate directly on image to specify edit regions). The API supports mask-based inpainting, outpainting, generative remove, and reference-image-guided fill. License: Commercial use permitted via enterprise agreement; per-edit credit consumption varies by model.[^43][^44][^45]

**Key differentiator for your use case**: Firefly Image 4 is trained exclusively on Adobe Stock — the cleanest licensing position of any closed-source model. If your animation production has content licensing concerns, Firefly is the safest commercial option. The Generative Fill mask+brush paradigm is directly analogous to Photoshop workflows animators already use.

**Non-photoreal testing**: Not documented in available sources, but Firefly's generation model produces illustration and stylized outputs alongside photoreal, and the mask approach (filling only the selected region) minimizes style bleed by design.

### Recraft V3 / V4

Recraft V3 ($0.04/image, released May 7, 2026 on OpenRouter) offers **100+ explicit style presets including "hand-drawn" and sketch styles** for both generation and editing. Inpainting available at $0.04. The model is specifically designed for stylized and vector outputs — making it the only closed-source model with a native "hand-drawn" style mode. However: editing is mask+instruction based; the `strength` parameter controls deviation from source. At 1K resolution cap, it cannot match the 4K outputs of Nano Banana/GPT Image.[^46][^47][^48][^49]

**Non-photoreal handling**: Recraft is the closest thing to a confirmed hand-drawn-aware editing model in the closed-source tier, via explicit style selection. This does not mean it *preserves* an existing pencil aesthetic — it imposes one. Use case: recreating a lost aesthetic on a corrected frame, not preserving an existing one.

***

## Section 2: Open-Source Landscape — Verified & Extended

### FLUX.1 Kontext [dev]

- **Architecture**: 12B rectified flow transformer, in-context image editing via image+text input[^18]
- **License**: Non-commercial ([dev]); commercial via Pro/Max API[^18]
- **VRAM**: Full model ~24GB (confirmed on 16GB with FP8)[^17]
- **Invocation**: Instruction-based; no explicit mask required; supports LoRA stacking[^50]
- **Editing arena Elo**: FLUX.2 [klein] 9B at 1161 open-weights (FLUX.1 Kontext not separately listed on current Artificial Analysis open-weights)[^3]
- **Multi-turn**: Yes, with degradation after ~6 edits[^18]
- **Non-photoreal preservation**: **Documented problems.** Reddit confirms oversaturation, proportion drift on anime/manga inputs. Style transfer to non-photoreal styles is limited in [dev] vs. Pro/Max.[^20][^21][^19]
- **Key mitigation**: Sketch-style LoRA (Shakker-Labs `FLUX.1-Kontext-dev-LoRA-Sketch-Style`) available on Hugging Face; training custom pencil-frame editing LoRAs is well-documented via Scenario platform.[^24][^23]
- **Ecosystem health**: Very active. LoRAShop framework enables multi-LoRA blending; SpecEdit accelerates inference up to 7–10×; VeloEdit adds velocity-field preservation[^51][^52][^53]
- **Best for your workflow**: Style-locked LoRA edits where you train on pencil-frame pairs; NOT recommended for zero-shot raw pencil edits

### Qwen-Image-Edit-2509

- **Architecture**: 20B MMDiT; Qwen2.5-VL semantic + VAE appearance dual encoder[^5]
- **License**: Apache 2.0[^31]
- **VRAM**: ~24GB for full model; quantized GGUF variants available[^54]
- **Invocation**: Instruction-based; native ControlNet support for edge/depth/keypoint maps; multi-image (1–3 inputs)[^27]
- **Editing arena Elo**: Best open-source on Artificial Analysis editing leaderboard at time of August 2025 benchmark[^26]
- **Non-photoreal preservation**: **Most promising among open-source.** Practitioner evidence:
  - Reddit (Sep 2025): handles "even the most awful sketches" converting rough pencil drawings[^30]
  - YouTube (Oct 2025): confirmed sketch-to-finished-image workflow with Qwen-IE-2509, adjusting denoise from 0.80–0.85 to control fidelity to original sketch lines[^29]
  - Hugging Face discussion (Nov 2025): noted difficulty *preserving* a rough pencil aesthetic (model wants to fully render), but confirmed it respects structural sketch content[^28]
  - Reddit (Sep 2025): excellent face/body proportion preservation; style transfer works but can require the original model (2508) rather than 2509 for some style tasks[^55]
  - DigitalOcean (Sep 2025): best overall on style transfer, object placement, and instruction-following across multiple image styles[^5]
- **Key finding**: Qwen-IE-2509 is confirmed to work with sketch input. The challenge is *preservation mode* (keep pencil look, change only X) vs. *rendering mode* (convert sketch to finished art). Preservation mode requires careful denoise control (0.75–0.82 range appears optimal per community evidence).[^29]
- **Qwen-Image-Edit-2511**: December 2025 release with improved realism and textures; likely the best current version but fewer independent tests than 2509.[^31]
- **Best for your workflow**: Primary open-source editing engine for targeted, region-specific edits on pencil frames

### OmniGen2

- **Architecture**: Qwen2.5-VL-3B MLLM + 4B Diffusion Transformer, decoupled paths[^33][^32]
- **License**: Apache 2.0[^34]
- **VRAM**: ~20–24GB estimated (4B DiT + 3B MLLM active parameters)
- **Invocation**: Instruction-based; in-context generation (multi-image reference)[^32]
- **Editing quality**: SOTA on ImgEdit-Bench among open-source; Emu-Edit CLIP-I: 0.876, DINO: 0.822; action editing particularly strong due to video training data[^32]
- **Non-photoreal preservation**: **Explicitly problematic** — paper notes "sensitivity to input image quality (noise, low resolution)." Pencil-test frames are exactly the "noisy, textured" inputs this warning refers to. Community reinforcement with SpatialReward boosted OmniGen2 by +0.90 GEdit-Bench but this is for photorealistic content.[^56][^32]
- **Best for your workflow**: Complex multi-reference compositions (e.g., combining a character reference sheet with a background reference to produce a new pose); not recommended for direct pencil-frame edits

### ByteDance Lance

- **Architecture**: 3B unified model (image+video understanding/generation/editing)[^37][^38]
- **License**: Apache 2.0[^37]
- **VRAM/RAM**: 40GB RAM required for inference — exceeds standard 24GB VRAM setup[^35]
- **Invocation**: Unified; multi-modal (text, image, video)
- **Editing benchmarks**: Claims to outperform FLUX.1-dev, Qwen-Image, and GPT Image 1 on image editing, but no independent verification at time of research[^36]
- **Non-photoreal testing**: None documented
- **Assessment**: Compelling architecture at 3B parameters but hardware requirements and lack of independent tests make it premature for production. Revisit in Q3 2026.

### HiDream-O1-Image

- **Architecture**: Pixel-space Unified Transformer (UiT), 8B (base) to 200B+ (Pro); natively unified without external VAE[^57][^58]
- **License**: Weights available on Hugging Face; license details unclear at research date[^59]
- **VRAM**: HiDream-O1-Image-Dev confirmed on fal.ai at ~$0.04/inference[^60]
- **Editing arena Elo**: 1213 open-weights (Artificial Analysis), second among open-source after HunyuanImage 3.0[^3]
- **Invocation**: Instruction-based; subject-driven personalization[^58]
- **Non-photoreal testing**: None documented
- **Assessment**: Strong open-source contender. Worth testing specifically on pencil-frame inputs given its pixel-space architecture (no VAE = potentially better texture preservation). Monitor for the full weights release and license clarification.

### Step1X-Edit

- **Architecture**: 19B MLLM (multimodal LLM) + DiT; latent embedding integration[^61][^62]
- **License**: Open-source (Stepfun/Apache-compatible, verify specific terms)
- **VRAM**: 48GB+ required — exceeds 24GB consumer GPU[^61]
- **Performance**: GEdit-Bench SOTA at time of April 2025 release, approaching proprietary models[^62]
- **Assessment**: Exceeds VRAM budget. Relevant for cloud-hosted workflows.

### SD3.5 + ControlNet-Inpaint / BrushNet / PowerPaint

These represent the previous generation of architecture-level inpainting solutions. They remain relevant for specific pipeline stages:

**BrushNet** (Tencent ARC): Plug-and-play dual-branch model that adds inpainting to any SD-based model without fine-tuning the base. Runs parallel U-Nets to separate masked image features from noise. License: Apache 2.0. Key advantage: works with any base checkpoint, including illustration-specific models. Strong at pixel-level mask region preservation.[^63][^64]

**PowerPaint v2 + BrushNet**: Combined architecture that adds learnable task prompts to BrushNet, enabling context-aware vs. text-guided inpainting switching. Best inpaint/outpaint combo for SD-based pipelines as of the available benchmarks.[^65]

**For pencil-test workflows**, BrushNet stacked on an illustration-tuned SD3.5 checkpoint (e.g., Illustrious or a pencil-style fine-tune) may produce better pencil-texture preservation than any of the flow-matching models above. This is an underexplored but plausible pipeline.

***

## Section 3: The Hand-Drawn / Pencil Preservation Question

This is the critical gap in current benchmarks. All 2026 head-to-head comparisons tested on photorealistic subjects or stylized-digital inputs (anime, oil painting). No benchmark explicitly tests the *preservation of pencil-on-cream texture through a targeted instruction edit*. Here is what the available evidence supports:

### What "Slicking Up" Means Mechanically

Modern flow-matching models (FLUX Kontext, Qwen-IE, OmniGen2) are trained predominantly on clean, high-contrast digital images. When given a noisy, low-contrast pencil-on-cream input, their denoising process tends to:
1. Interpret grain/texture as "noise to be removed"
2. Sharpen edges toward the model's learned manifold (digital sheen)
3. Boost contrast to match training distribution

This is the mechanism behind "slicking up." The degree to which each model does this depends on how strongly it is conditioned on the source image vs. the target prompt.

### Evidence-Based Model Rankings for Non-Photoreal Preservation

**Closed-source:**

1. **Nano Banana Pro** — Highest documented evidence of preserving stylistic inputs. Users confirmed it can replicate handwriting style and maintain sketch-character identity through edits. Most likely explanation: Gemini's world-knowledge backbone recognizes "pencil sketch" as a legitimate semantic category rather than noise.[^6][^7]
2. **Nano Banana 2** — Likely similar behavior at lower cost; less user documentation on non-photoreal specifically.
3. **Adobe Firefly** — Mask-based approach minimizes bleed into unedited regions by construction; style drift risk limited to edited zone only. No documentation on pencil aesthetics.
4. **GPT Image 2** — No documented evidence of pencil preservation. Its photorealistic bias in face generation suggests it will over-render pencil lines.
5. **Seedream 4.0** — No documentation. Training data appears photorealistic.

**Open-source:**

1. **Qwen-Image-Edit-2509** — Best documented evidence. The "denoise at 0.80–0.82 preserves sketch structure" finding from YouTube practitioner is directly relevant. The dual VL+VAE architecture specifically designed for "appearance consistency" suggests it has better signal separation between "pencil texture to preserve" and "hand pose to change." Reddit confirms it handles rough sketch input structurally.[^30][^29]
2. **FLUX.1 Kontext [dev] + Sketch LoRA** — With the Shakker-Labs sketch LoRA or a custom-trained editing LoRA, FLUX Kontext can target pencil style. Without LoRA, it will drift toward its photorealistic training distribution.[^66][^23][^24]
3. **OmniGen2** — Not recommended for raw pencil input. Explicit sensitivity to noisy/textured inputs confirmed in paper.[^32]
4. **HiDream-O1-Image** — Pixel-space architecture theoretically preserves texture better; unconfirmed for pencil inputs.
5. **Lance** — No tests; hardware constraint.

### Style LoRA Stacking as the Primary Solution

The most reliable technique for preserving pencil aesthetics through an edit is **training a style LoRA on your own pencil-frame pairs and stacking it with an editing model**:

- **FLUX Kontext + pencil-style LoRA**: Train before/after pairs (raw pencil frame → same frame with specific edit applied in Procreate) using the Scenario or Hugging Face training pipeline. The LoRA learns the "delta" — the editing model then applies it consistently. 5–20 training pairs documented as sufficient.[^23]
- **Qwen-IE-2509 + ControlNet edge map**: Using Canny edge maps of your original frame as ControlNet conditioning preserves line structure through edits. Combined with low denoise (0.78–0.82), this is the closest available technique to "change only the hand pose, preserve all lines."[^27]
- **B-LoRA style separation (SDXL)**: For SD-based pipelines, B-LoRA separates style and content into independently trainable components from a single image, enabling style preservation through textual stylization edits. Requires SDXL base, not FLUX.[^67]
- **LoRAShop multi-LoRA blending** (FLUX): Allows blending an editing instruction LoRA with a style preservation LoRA simultaneously, with spatial disentanglement based on early denoising masks.[^53]

### Practitioner Sources on Non-Photoreal Editing

- Reddit r/StableDiffusion (Sep 2025): Qwen-IE-2509 confirmed on rough sketches[^30]
- Reddit r/StableDiffusion (Sep 2025): Qwen style transfer "superior to even GPT-4o in several aspects"; better for anime than FLUX Kontext[^68][^26]
- YouTube (Oct 2025): Complete sketch→animation workflow with Qwen-IE-2509 and WAN2.2[^29]
- Hugging Face (Nov 2025): Discussion of pencil sketch colouring with Qwen, noting the preservation challenge[^28]
- Instagram (Jul 2025): FLUX Kontext LoRA training on sketching style documented as working[^66]
- Reddit (Jun 2025): FLUX Kontext [dev] style transfer "quite limited" vs. Pro; anime and sketch styles noted as feasible but imperfect[^20]
- Reddit r/nanobanana (Nov 2025): Nano Banana Pro preserving handwriting-style character identity[^7][^6]

***

## Section 4: Editing Techniques for 2026

### Inpainting with Masks — Best 2026 Pipelines

Explicit mask-based inpainting is the highest-precision editing paradigm. The 2026 options are:

- **GPT Image 2 API** (`/v1/images/edits` with `mask` parameter): Only major closed-source model retaining explicit mask input. Best for hero-shot precision.[^8]
- **Adobe Firefly AI Markup + Generative Fill**: Brush/rectangle mask directly annotated on image; supports reference image guidance.[^45][^43]
- **BrushNet + SD3.5**: Plug-and-play dual-branch inpainting for any SD-based checkpoint. Best for preserving illustration aesthetics when stacked with a pencil-style fine-tune.[^64][^63]
- **Qwen-IE-2509 + explicit region prompt**: While not mask-based per se, ControlNet edge conditioning plus regioned instruction ("only edit the left hand in the lower-right quadrant") approximates mask behavior.[^27]
- **RAD (Region-Aware Diffusion)**: Per-pixel noise scheduling for inpainting; allows different regions to be generated asynchronously while considering global context. Training-free LoRA adaptation. Published at CVPR 2025.[^69]

### Instruction-Edit vs. Reference-Edit vs. Mask-Edit

| Paradigm | When to Use | Best Models | Risk |
|---|---|---|---|
| **Instruction-edit** | "Redraw the eyes with closed expression" | Qwen-IE-2509, Nano Banana 2, FLUX Kontext | Context misinterpretation |
| **Reference-edit** | "Make the hand look like this reference image" | GPT Image 2, Nano Banana Pro, Qwen-IE-2509 multi-image | Identity drift toward reference |
| **Mask-edit** | "Change only this 200px region" | GPT Image 2, Adobe Firefly, BrushNet | None — highest precision |
| **ControlNet-conditioned** | "Preserve these exact lines, change color/detail" | Qwen-IE-2509 + Canny/edge map | ControlNet strength calibration |

For pencil-test animation: **mask-edit** is the gold standard for single-region changes (hand pose, eye expression). **Instruction-edit** is appropriate for global style adjustments (soften lines throughout). **Reference-edit** is best for character consistency across frames when generating new keyframes.

### Latent Blending and Seed-Locking

Seed locking (fixed random seed across edits) produces consistent outputs for iterative refinement but does not guarantee preservation of specific image regions. More reliable approaches:

- **VeloEdit** (FLUX Kontext, Qwen-IE): Velocity-field decomposition that identifies edit vs. preservation regions, then enforces source-restoring velocity in preservation regions. Training-free. Published March 2026. Directly addresses the "consistency in non-edited regions" failure mode.[^52]
- **ERec (Editing by Reconstruction)**: Synchronizes reconstruction and editing sampling paths; improves background preservation without fine-tuning; published November 2025.[^70]
- **Agent Banana framework**: Layer decomposition for localized edits with context folding for multi-turn memory; achieves IC 0.871, SSIM-OM 0.84 on 4K images. Best for long editing chains.[^71]

### Differential Diffusion / Region-Aware Sampling

**Differential Diffusion** (Levin & Fried, published in CGF 2025) assigns different change-strength values *per pixel* or per region, enabling:[^72][^73]
- Soft inpainting: edit target zone with high strength, let boundary pixels blend at reduced strength
- Gradient-strength masks: maximum change at center of edit, fading to zero at unedited region boundary

This is the most principled solution to the "seam artifact" problem in pencil-frame edits. The framework integrates into any existing diffusion model at inference time, no training required. Directly applicable to FLUX Kontext and SD3.5 pipelines.[^72]

### Multi-Region Simultaneous Edits

Several 2025–2026 approaches address this:

- **ADE-CoT** (Adaptive Edit CoT): Dynamic budget allocation for multi-region edits based on estimated difficulty; 2× speedup on FLUX Kontext.[^74]
- **OmniGen2 in-context generation**: Can process a character reference + scene reference + target pose to generate edits referencing all three.[^33][^32]
- **Qwen-IE-2509 multi-image**: Native support for 2–3 input images (person + product + scene).[^27]
- **FireRed-Image-Edit-1.0**: 19B DiT with multi-region bucket sampler; Consistency Loss for identity preservation across multi-region edits.[^75]

***

## Section 5: Three Recommended Editing Setups

### Setup 1 — Cheapest Reliable Closed-Source

**Recommendation: Nano Banana 2 (Gemini 3.1 Flash Image) at $0.067–0.101/image at 1–2K resolution.**

Nano Banana 2 beats Nano Banana 1's pricing model for large-batch workflows while offering 4K resolution and improved multi-turn editing. It is the only closed-source model with user-documented evidence of preserving non-photorealistic/hand-drawn style characteristics.[^4][^6][^7]

**However**, this is a material price increase from your current $0.039 baseline. If cost is the primary constraint, **Seedream 4.0 at $0.03/image on fal.ai** may be the cheapest option if its editing quality proves sufficient — but it lacks any documented pencil-style handling and no production SLA is confirmed.[^16]

**Do not move off Nano Banana 2 to GPT Image 2** for budget editing; GPT Image 2 high quality at ~$0.211 is 3–4× more expensive with no confirmed advantage for pencil-frame edits.

**Operational note**: The mask-based `imagen-3.0-capability-001` endpoint retires June 30, 2026. Migrate to `gemini-3.1-flash-image-preview` instruction-based editing immediately if you have not done so.[^1]

**When to upgrade to Nano Banana Pro**: For hero-shot keyframes where quality matters over cost, or when multi-step instruction chains (5+ edits on a single frame) are needed. Pro's Elo 1240 vs. Nano Banana 2's 1236 is marginal for standard tasks.[^3]

### Setup 2 — Best-Quality Open-Source on 24GB GPU

**Primary engine: Qwen-Image-Edit-2511 (or 2509) on a 24GB VRAM GPU.**

**Head-to-head verdict for pencil-test use case:**

| Model | Pencil Preservation | Instruction Precision | 24GB Fit | License | Verdict |
|---|---|---|---|---|---|
| FLUX.1 Kontext [dev] | Poor (w/o LoRA) / Good (with sketch LoRA) | Excellent | Yes (FP8) | Non-commercial | Secondary |
| Qwen-IE-2509 | Good (denoise tuning required) | Excellent | Yes (GGUF) | Apache 2.0 | **Primary** |
| OmniGen2 | Not recommended | Strong | Yes | Apache 2.0 | Complex tasks only |
| Lance | Unknown | Unknown | No (40GB RAM) | Apache 2.0 | Experimental |

**Full pipeline for a pencil-test edit:**

1. Take your pencil-test frame as input image
2. Generate a Canny edge map (preserves line structure for ControlNet conditioning)[^27]
3. Run Qwen-IE-2509 in ComfyUI with:
   - Denoise: 0.78–0.82 (community-confirmed for sketch preservation)[^29]
   - ControlNet edge map active at strength 0.6–0.8
   - Prompt: targeted instruction ("Redraw the left hand so the fingers are open, maintaining pencil-sketch style on cream paper, all other lines unchanged")
4. Compare output to original; re-run with adjusted denoise if too rendered or too unedited

**For FLUX Kontext as secondary tool** (when iterative multi-turn editing matters more than pencil preservation):
- Install FP8 version (~12GB VRAM)[^17]
- Load Shakker-Labs sketch-style LoRA or custom-trained pencil-frame editing LoRA[^24][^23]
- Use for multi-turn iterative refinement chains; keep edits under 5–6 iterations to avoid artifact degradation[^18]

**For multi-reference compositions** (e.g., combining a character model sheet + background reference):
- Use Qwen-IE-2509's multi-image mode (2–3 inputs)[^27]
- Or OmniGen2 for in-context generation with multiple references[^32]

### Setup 3 — Hybrid Pipeline

**Logic: Open-source Qwen handles volume; closed-source Nano Banana Pro handles hero shots and difficult cases.**

**Edit type ownership:**

| Edit Type | Model | Invocation | Rationale |
|---|---|---|---|
| Hand pose correction | Qwen-IE-2509 + Canny ControlNet | Instruction + edge map | Best structure preservation; local edit precision[^27] |
| Eye/facial expression change | Qwen-IE-2509 multi-image | Instruction + reference face | Identity preservation via VL encoder[^5] |
| Canvas extension / outpainting | BrushNet + illustration SD checkpoint | Mask + instruction | Pencil-texture-consistent outpainting[^63] |
| Stylus angle / linework fix | Nano Banana 2 (instruction) | Natural language | Best for local linework semantics |
| New pose from character sheet | OmniGen2 or Qwen multi-image | Reference + instruction | Multi-image in-context generation[^32][^27] |
| Hero shot final composite | Nano Banana Pro | Instruction | Highest fidelity, quality ceiling[^3] |

**Cost structure:**
- Assume 80% of edits are volume work (hand corrections, eye fixes) → Qwen-IE-2509 locally = near-zero marginal cost
- 15% require closed-source quality → Nano Banana 2 at ~$0.07–0.10/image
- 5% hero shots → Nano Banana Pro at ~$0.15–0.20/image (estimated, Vertex AI pricing)

**Total cost vs. pure Nano Banana 2 pipeline**: Approximately 80–85% cost reduction on volume work, while matching or exceeding quality on hero shots.

**ComfyUI implementation**: Both Qwen-IE-2509 and FLUX Kontext have native ComfyUI support. OmniGen2 runs via Gradio. The hybrid pipeline can be orchestrated in ComfyUI with model-routing logic based on edit type or frame designation.[^76][^17][^27]

***

## Comparison Table

| Model | Edit Type | Instruction-Follow | Preservation | Cost / VRAM | License | **Hand-Drawn Score** |
|---|---|---|---|---|---|---|
| **Nano Banana Pro** | Instruction | ★★★★★ | ★★★★☆ | ~$0.15–0.20/img | API-only | ★★★★☆ (user evidence)[^6][^7] |
| **Nano Banana 2** | Instruction | ★★★★★ | ★★★★☆ | $0.067–0.151/img | API-only | ★★★☆☆ (inferred)[^4] |
| **GPT Image 2** | Instruction + Mask | ★★★★★ | ★★★★★ (face) | $0.133–0.211/img | API-only | ★★☆☆☆ (no evidence; likely over-renders)[^12] |
| **Seedream 4.0** | Instruction | ★★★★☆ | ★★★★☆ | $0.03/img | API-only | ★★☆☆☆ (no evidence)[^16] |
| **Adobe Firefly** | Mask + Instruction | ★★★★☆ | ★★★★☆ (mask-limited) | Credit-based | Commercial | ★★★☆☆ (mask prevents bleed)[^45] |
| **Recraft V3** | Instruction + style | ★★★★☆ | ★★★☆☆ | $0.04/img | Commercial | ★★★☆☆ (explicit hand-drawn style preset)[^48] |
| **FLUX.1 Kontext [dev]** | Instruction (+ LoRA) | ★★★★★ | ★★★★☆ | Non-commercial / 24GB | Non-commercial | ★★☆☆☆ raw; ★★★★☆ with sketch LoRA[^21][^24] |
| **Qwen-IE-2509** | Instruction + ControlNet | ★★★★★ | ★★★★★ | Apache 2.0 / 24GB | Apache 2.0 | ★★★★☆ (practitioner-confirmed)[^29][^30] |
| **OmniGen2** | Instruction + multi-ref | ★★★★☆ | ★★★★☆ | Apache 2.0 / ~24GB | Apache 2.0 | ★★☆☆☆ (noisy-input sensitivity)[^32] |
| **HiDream-O1-Image** | Instruction | ★★★★☆ | ★★★☆☆ | License TBD / 24GB+ | TBD | ★★★☆☆ (pixel-space; theoretically better) |
| **Lance** | Instruction + multi-modal | ★★★★☆ | Unknown | Apache 2.0 / 40GB RAM | Apache 2.0 | ★★☆☆☆ (too new)[^37] |
| **BrushNet + SD3.5** | Mask-based | ★★★☆☆ | ★★★★★ | Apache 2.0 / 16GB | Apache 2.0 | ★★★★☆ (mask = no bleed; SD-style checkpoint compatible)[^63] |

*Hand-Drawn Score methodology: ★★★★★ = confirmed testing on pencil/non-photoreal inputs with positive results; ★★★★☆ = user evidence positive; ★★★☆☆ = architectural reason to expect positive result, no tests; ★★☆☆☆ = no evidence; ★☆☆☆☆ = evidence of problematic behavior*

***

## Open Research Questions

The following gaps remain genuinely unresolved as of May 2026 and would benefit from first-party testing:

1. **Systematic pencil-texture retention benchmark**: No public dataset of pencil-test animation frames exists for editing model evaluation. Building one (20–50 before/after pairs from your own archive) and running Qwen-IE-2509, Nano Banana Pro, and FLUX Kontext+LoRA through it would produce the field's first non-photoreal editing benchmark.

2. **HiDream-O1-Image on pencil inputs**: Its pixel-space architecture (no VAE compression) theoretically preserves fine texture better. Untested.

3. **Differential Diffusion + Qwen-IE-2509**: VeloEdit already implements velocity-field preservation for Qwen; combining with Differential Diffusion's per-pixel change strength could produce the precision-preservation combination needed for animation frame edits. No documented implementations found.[^52]

4. **Lance at reduced resolution**: At lower inference resolutions, the 40GB RAM requirement may scale down. Could become viable on 24GB cards with quantization.

5. **SeedEdit 3.0 / Seedream 4.0 on illustration inputs**: ByteDance's models have the strongest *preservation* metrics among closed-source (56.1% usability vs. GPT-4o's 37.1%). Testing on pencil inputs could reveal hidden capability.[^14]

---

## References

1. [Imagen-3.0-capability-001 retiring June 30 — no mask-based ...](https://discuss.google.dev/t/imagen-3-0-capability-001-retiring-june-30-no-mask-based-editing-replacement-exists/343602) - I received a Google Cloud email on March 23, 2026 stating that imagen-3.0-capability-001 will be ret...

2. [Introducing Gemini 2.5 Flash Image, our state-of-the-art image modeldevelopers.googleblog.com › introducing-gemini-2-5-flash-image](https://developers.googleblog.com/introducing-gemini-2-5-flash-image/) - Explore Gemini 2.5 Flash Image, a powerful new image generation and editing model with advanced feat...

3. [Image Editing Leaderboard - Top AI Image Models - Artificial Analysis](https://artificialanalysis.ai/image/leaderboard/editing) - Find the best Image Editing models, see rankings from blind votes, and compare quality, generation s...

4. [Nano Banana 2, aka Gemini 3.1 Flash Image, Makes Edits Easier ...](https://www.deeplearning.ai/the-batch/nano-banana-2-aka-gemini-3-1-flash-image-makes-edits-easier-and-faster) - Nano Banana 2 Ups Performance/Price Gemini 3.1 Flash Image makes photo generation and edits easier a...

5. [Comparing the best Image Editing AI Models - DigitalOcean](https://www.digitalocean.com/community/tutorials/image-editing-model-review) - Qwen Image Edit 2509 is the updated version of the model, exceeding the abilities of Qwen Image Edit...

6. [Gemini Nano Banana Pro can solve math exercises and ... - Facebook](https://www.facebook.com/groups/703007927897194/posts/1380554560142524/) - Gemini Nano Banana Pro can solve math exercises and rewrite the full solution using your own handwri...

7. [Why gemini-3-pro-image-preview cannot just take a character from ...](https://www.reddit.com/r/nanobanana/comments/1p3s9mm/why_gemini3proimagepreview_cannot_just_take_a/) - Right at release of 3 pro, I made a whole bunch of new images using my character. Not only did I hav...

8. [GPT Image 2 Model | OpenAI API](https://developers.openai.com/api/docs/models/gpt-image-2) - It supports flexible image sizes and high-fidelity image inputs. Learn more in our image generation ...

9. [Introducing gpt-image-2 - available today in the API and Codex](https://community.openai.com/t/introducing-gpt-image-2-available-today-in-the-api-and-codex/1379479) - It is designed for complex visual tasks and produces precise, usable images with stronger editing, b...

10. [Text to Image Leaderboard - Top AI Image Models - Artificial Analysis](https://artificialanalysis.ai/image/leaderboard/text-to-image) - HiDream-O1-Image-Dev-2604 currently leads among open weights models in the Artificial Analysis Text ...

11. [GPT Image 2 Pricing in 2026: What Teams Pay | WaveSpeed Blog](https://wavespeed.ai/blog/posts/gpt-image-2-pricing-2026/) - Via the API, a 1024×1024 image at low quality runs about ​$0.006, medium about ​$0.053**, and high a...

12. [What Will GPT Image 2 Be? Predictions Based on OpenAI's Trajectory](https://wavespeed.ai/blog/posts/what-is-gpt-image-2/) - If the same cadence holds, GPT Image 2 could arrive between mid-2026 and late 2026. But competitive ...

13. [ByteDance Releases Image Editing Model SeedEdit 3.0 ... - AIBase](https://www.aibase.com/news/www.aibase.com/news/18708) - The model can process and generate images with a resolution of 4K, performing exceptionally well in ...

14. [SeedEdit 3.0: Fast and High-Quality Generative Image Editing - arXiv](https://arxiv.org/abs/2506.05083) - We introduce SeedEdit 3.0, in companion with our T2I model Seedream 3.0, which significantly improve...

15. [SeedEdit 3.0: Fast and High-Quality Generative Image Editing - arXiv](https://arxiv.org/html/2506.05083v2)

16. [ByteDance launched Seedream 4.0, a unified image generator and ...](https://x.com/rohanpaul_ai/status/1966070362556260611) - User feedback highlights accurate text-driven edits, 2K images in under 2s, 4K support, multi-image ...

17. [Flux.1 Kontext (Dev) Multimodal Image Editing | by Chris Greenmedium.com › diffusion-doodles › flux-1-kontext-dev-multimodal-image-...](https://medium.com/diffusion-doodles/flux-1-kontext-dev-multimodal-image-editing-19a003714b40) - Unleashing AI image manipulation locally on your computer

18. [Introducing FLUX.1 Kontext and the BFL Playground](https://bfl.ai/announcements/flux-1-kontext) - Today, we are excited to release FLUX.1 Kontext, a suite of generative flow matching models that all...

19. [Flux Kontext Prompting Guide : r/StableDiffusion - Reddit](https://www.reddit.com/r/StableDiffusion/comments/1llew66/flux_kontext_prompting_guide/) - First, take that CGI image and use the prompt "make image line art" and then take the resulting imag...

20. [Tip - kontext prompt. Don't write "transform to anime". Write "transform realistic image to anime". I believe flux works best with prompt like "A to B". Even if A is obvious](https://www.reddit.com/r/StableDiffusion/comments/1lonhox/tip_kontext_prompt_dont_write_transform_to_anime/) - Tip - kontext prompt. Don't write "transform to anime". Write "transform realistic image to anime". ...

21. [Flux Kontext bad with Anime/Manga? : r/StableDiffusion - Reddit](https://www.reddit.com/r/StableDiffusion/comments/1lmt1i0/flux_kontext_bad_with_animemanga/) - Is it just me, or is Flux Kontext not good with anime or manga? Attached are the images, and the col...

22. [Flux is great at manga & anime](https://www.reddit.com/r/StableDiffusion/comments/1eqvjqd/flux_is_great_at_manga_anime/)

23. [How to Train a Flux Kontext LoRA in Scenario: Master Custom Editing](https://www.scenario.com/blog/train-flux-kontext-lora-scenario) - Learn to train Flux Kontext LoRA models in Scenario. Pair before/after images with instructions to c...

24. [Shakker-Labs/FLUX.1-Kontext-dev-LoRA-Sketch-Style - Hugging Face](https://huggingface.co/Shakker-Labs/FLUX.1-Kontext-dev-LoRA-Sketch-Style) - You should use convert real photos into sketches , sketch to trigger the image generation. Inference...

25. [AI image editing model review: Flux 1 Kontext | Adam Holter posted ...](https://www.linkedin.com/posts/adam-holter-b5334327a_flux1kontext-aiimageediting-blackforestlabs-activity-7339608440689881088-Pnth) - I've been testing Black Forest Labs' Flux 1 Kontext for a while now, and here's my honest take on th...

26. [Qwen-Image-Edit is the best open-source image editing model by ...](https://www.reddit.com/r/StableDiffusion/comments/1mvni4c/qwenimageedit_is_the_best_opensource_image/) - Qwen-Image-Edit is the best open-source image editing model by far on Artificial Analysis rankings, ...

27. [WAN2.2 Animate & Qwen-Image-Edit 2509 Native Support in ComfyUI](https://blog.comfy.org/p/wan22-animate-and-qwen-image-edit-2509) - The model can animate any character based on a performer's video, precisely replicating the performe...

28. [possible to make a photo/illustration style to pencil sketch style ...](https://huggingface.co/dx8152/Qwen-Image-Edit-2509-Light_restoration/discussions/1) - I have 50 rough sketches that an artist wants before proper lineart, but colouring them with Qwen Im...

29. [How to Turn Sketches into Moving Scenes Using Qwen Image Edit + ...](https://www.youtube.com/watch?v=TWvN0p5qaog) - Turn a simple sketch into a moving scene using Qwen Image Edit and Wan 2.2 FLF (First Last Frame). A...

30. [qwen image edit 2509 delivers, even with the most awful sketches](https://www.reddit.com/r/StableDiffusion/comments/1nsczuj/qwen_image_edit_2509_delivers_even_with_the_most/) - Transform the sketch into a realistic photography. a grotesque toaster with eyes and mouth and a hap...

31. [Qwen-Image is a powerful image generation foundation ... - GitHub](https://github.com/QwenLM/Qwen-Image) - Tested in 10,000+ blind rounds on AI Arena, Qwen-Image-2512 ranks as the strongest open-source image...

32. [[Revue de papier] OmniGen2: Exploration to Advanced Multimodal Generation](https://www.themoonlight.io/fr/review/omnigen2-exploration-to-advanced-multimodal-generation) - OmniGen2 is an open-source, versatile generative model designed for unified text-to-image (T2I) gene...

33. [OmniGen2: Towards Instruction-Aligned Multimodal Generation - arXiv](https://arxiv.org/abs/2506.18871) - In this work, we introduce OmniGen2, a versatile and open-source generative model designed to provid...

34. [OmniGen2](https://github.com/VectorSpaceLab/OmniGen2) - OmniGen2: Exploration to Advanced Multimodal Generation. - VectorSpaceLab/OmniGen2

35. [All In One Video and Image Generation and Editing AI - YouTube](https://www.youtube.com/watch?v=nUMXqKpzm5Q) - How to use ByteDance Lance for free ? #ai #datascience #machinelearning #programming.

36. [Lance (ByteDance), lightweight multimodal model image & video understanding, generation, and editing](https://www.youtube.com/watch?v=cCtv6FOxkjA) - #Lance #ByteDance #multimodal #wonwizard

중국 ByteDance에서 발표한 Lance는 이미지 및 동영상 이해, 생성, 편집을 위한 경량 네이티브...

37. [Lance by ByteDance: 3B Apache2 model for image and ... - Reddit](https://www.reddit.com/r/StableDiffusion/comments/1tgjrm2/lance_by_bytedance_3b_apache2_model_for_image_and/) - Lance by ByteDance: 3B Apache2 model for image and video understanding, generation, and editing.

38. [One Model, Three Modalities: ByteDance Releases Lance for Image ...](https://www.marktechpost.com/2026/05/21/one-model-three-modalities-bytedance-releases-lance-for-image-and-video-understanding-generation-and-editing/) - ByteDance releases Lance, a 3B native unified multimodal model for image and video understanding, ge...

39. [Gemini 3 Pro Image | Gemini Enterprise Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-pro-image) - Learn about Gemini 3 Pro Image, which is a reasoning model ideal for complex and multi-turn image ge...

40. [AI Image Editing Models - SiliconFlow](https://www.siliconflow.com/articles/benchmark/image-editing-models) - Image Editing Leaderboard. All Models Open Weights. Rank, Model, Creator, Release Date, ELO Score. 1...

41. [Introducing ChatGPT Images 2.0 - OpenAI](https://openai.com/index/introducing-chatgpt-images-2-0/) - ChatGPT Images 2.0 introduces a state-of-the-art image generation model with improved text rendering...

42. [SeedEdit 3.0 i2i API - Segmind](https://www.segmind.com/models/seededit-v3) - SeedEdit 3.0 enables seamless, high-quality image edits through advanced AI-driven techniques.

43. [Use Generative Fill - Adobe Help Center](https://helpx.adobe.com/firefly/web/edit-images/prompt-to-edit/generative-fill.html) - Generative fill combines generative AI capabilities with manual selection controls, allowing you to ...

44. [Adobe's Firefly Services makes over 20 new generative and creative ...](https://techcrunch.com/2024/03/26/adobes-firefly-services-makes-over-20-new-generative-and-creative-apis-available-to-developers/) - In addition to these AI features, Firefly Services also exposes tools for editing text layers, taggi...

45. [New image editing features in Adobe Firefly get you from 'almost ...](https://blog.adobe.com/en/publish/2026/04/09/new-image-editing-features-adobe-firefly-get-you-from-almost-there-to-exactly-right) - Discover Precision Flow and AI Markup — two new Adobe Firefly tools that give you precise, intuitive...

46. [Recraft V3 – API Quickstart | OpenRouter](https://openrouter.ai/recraft/recraft-v3/api) - Sample code and API for Recraft: Recraft V3 - Recraft V3 is an image generation model from Recraft. ...

47. [Recraft V3 - API Pricing & Providers - OpenRouter](https://openrouter.ai/recraft/recraft-v3) - Recraft V3 is an image generation model from Recraft. $0 per million input tokens, $0 per million ou...

48. [Recraft Image Generation API: Vector, Style, Brand Output](https://www.recraft.ai/blog/discover-the-power-of-recrafts-image-generation-api) - Recraft's image generation API gives developers vector output, style consistency, brand colors, and ...

49. [Pricing and plans - Recraft](https://www.recraft.ai/pricing?tab=api) - Generate and edit vector art, icons, 3d images and illustrations in a wide range of styles suitable ...

50. [FLUX Kontext Dev Detailed Local Windows How To Tutorial - GitHub](https://github.com/FurkanGozukara/Stable-Diffusion/discussions/95) - With FLUX Kontext you can edit any part of the image in any way with just prompt. No-masking, no-Con...

51. [SpecEdit: Training-Free Acceleration for Diffusion based Image Editing via Semantic Locking](https://www.semanticscholar.org/paper/04db319c9489666412e497630635350ae283ddaa) - Diffusion-based image editing offers strong semantic controllability, but remains computationally ex...

52. [VeloEdit: Training-Free Consistent and Continuous Instruction-Based Image Editing via Velocity Field Decomposition](https://www.semanticscholar.org/paper/0b22154770e202d5bb98f3c4c888701aec016165) - Instruction-based image editing aims to modify source content according to textual instructions. How...

53. [LoRAShop: Training-Free Multi-Concept Image Generation ... - arXiv](https://arxiv.org/html/2505.23758v1) - We present LoRAShop, a training-free framework enabling the simultaneous use of multiple LoRA adapte...

54. [Turn Sketches, Anime & Stick Figures into Real Photos - YouTube](https://www.youtube.com/watch?v=-gI_T6uiCA0) - ... test this workflow across multiple ... Qwen Image Edit 2511–Local Image Editing in ComfyUI | Mul...

55. [Has anyone managed to do style transfer with qwen-image-edit-2509?](https://www.reddit.com/r/StableDiffusion/comments/1nsvokq/has_anyone_managed_to_do_style_transfer_with/) - What I really like about qwen-image-edit-2509 is that it seems really good at preserving faces and b...

56. [SpatialReward: Bridging the Perception Gap in Online RL for Image Editing via Explicit Spatial Reasoning](https://arxiv.org/abs/2602.07458) - Online Reinforcement Learning (RL) offers a promising avenue for complex image editing but is curren...

57. [HiDream-O1-Image: A Natively Unified Image Generative Foundation Model with Pixel-level Unified Transformer](https://www.semanticscholar.org/paper/3f8596d9075121c02b48e9a5aa6b4ff2053be009) - The evolution of visual generative models has long been constrained by fragmented architectures rely...

58. [HiDream-O1-Image: A Natively Unified Image Generative ... - arXiv](https://arxiv.org/html/2605.11061v1) - In this way, HiDream-O1-Image treats diverse tasks (text-to-image, image editing, and subject-driven...

59. [HiDream-ai/HiDream-O1-Image - Hugging Face](https://huggingface.co/HiDream-ai/HiDream-O1-Image) - 🛠️ May 13, 2026: Inference & pipeline updates — accelerated IP inference; the IP pipeline now suppor...

60. [Hidream O1 Image (Text to Image) API on fal - Fal.ai](https://fal.ai/models/fal-ai/hidream-o1-image) - Create, edit, and personalize high-resolution images up to 2K—single native model handles text-to-im...

61. [Platform For AI:Deploy Step1X-Edit model - Alibaba Cloud](https://www.alibabacloud.com/help/en/pai/use-cases/one-click-deploy-step1x-edit) - Step1X-Edit is an advanced, open-source image editing model from Stepfun designed to improve editing...

62. [Step1X-Edit: A Practical Framework for General Image Editing](https://huggingface.co/papers/2504.17761) - Step1X-Edit, an image editing model that uses multimodal LLM and diffusion image decoder, outperform...

63. [BrushNet: A Plug-and-Play Image Inpainting Model with ...](https://tencentarc.github.io/BrushNet/) - BrushNet: A Plug-and-Play Image Inpainting Model with Decomposed Dual-Branch Diffusion

64. [BrushNet: A Plug-and-Play Image Inpainting Model with ...](https://arxiv.org/html/2403.06976v1)

65. [当前 inpainting/outpainting 最优解：PowerPaint + BrushNet](https://www.51cto.com/aigc/639.html) - 一、概述PowerPaint是一种图像修复模型，它能够实现多种内绘图任务，包括文本引导的对象内绘图、上下文感知图像内绘图、可控形状拟合的对象内绘图以及外绘图。如果单纯从这篇文章来看，并不能达到最好的效...

66. [Have you ever wanted to turn your images into a specific style, like a ...](https://www.instagram.com/p/DMA1TuwMu6G/) - I have shared a video tutorial on this + giving access to the workflow files and the sketch LoRA mod...

67. [Implicit Style-Content Separation using B-LoRA - GitHub Pages](https://b-lora.github.io/B-LoRA/) - In this paper, we introduce B-LoRA, a method that leverages LoRA (Low-Rank Adaptation) to implicitly...

68. [Flux 2 Is Amazing at Manga Coloring](https://www.reddit.com/r/StableDiffusion/comments/1p6t35p/flux_2_is_amazing_at_manga_coloring/) - Flux 2 Is Amazing at Manga Coloring

69. [RAD: Region-Aware Diffusion Models for Image Inpainting](https://cvpr.thecvf.com/virtual/2025/poster/33149) - In this paper, we present region-aware diffusion models (RAD) for inpainting with a simple yet effec...

70. [Editing by Reconstruction: Background Preservation for Instruction ...](https://openreview.net/forum?id=7uamWbf0BB) - This paper proposes ERec (Editing by Reconstruction), a finetuning-free method to improve background...

71. [Agent Banana: High-Fidelity Image Editing with Agentic Thinking and Tooling](https://arxiv.org/abs/2602.09084) - We study instruction-based image editing under professional workflows and identify three persistent ...

72. [Differential Diffusion: Giving Each Pixel Its Strength](https://diglib.eg.org/items/e5b55d65-3a92-4d1e-934e-7b26fb42fa4e) - Diffusion models have revolutionized image generation and editing, producing state-of-the-art result...

73. [Differential Diffusion: Giving Each Pixel Its Strength](https://differential-diffusion.github.io) - Differential Diffusion modifies an image according to a text prompt, and according to a map that spe...

74. [From Scale to Speed: Adaptive Test-Time Scaling for Image Editing](https://arxiv.org/abs/2603.00141) - Image Chain-of-Thought (Image-CoT) is a test-time scaling paradigm that improves image generation by...

75. [FireRed-Image-Edit-1.0 Technical Report](https://arxiv.org/abs/2602.13344) - We present FireRed-Image-Edit, a diffusion transformer for instruction-based image editing that achi...

76. [OmniGen2 - a Powerful Image Editing Model](https://www.digitalocean.com/community/tutorials/omnigen2) - In this tutorial, show how to run and use the new Omnigen2 model on a GPU Droplet and their custom G...

