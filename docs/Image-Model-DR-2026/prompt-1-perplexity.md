# AI In-Between Frame Generation for Pencil-Test Animation: Model Research Report (2025–2026)

*Prepared for Sean Winslow | Animation Portfolio Pipeline: Scaffold → Generate → Motion → Audit → Assemble*

***

## Executive Summary

1. **FLUX.1 Kontext [dev] is the most compelling self-hosted candidate** for in-betweens: open weights (non-commercial free), native character consistency through in-context editing, ComfyUI day-0 support, and — with FP8 quantization — runs on a 4090's 24 GB VRAM with ~30–80 second generation times.[^1][^2]
2. **Qwen-Image-Edit-2511 is a fierce challenger**: Apache 2.0 license, 20B MMDiT architecture, "100% face consistency" ComfyUI workflows already circulating on Civitai, direct multi-image input, and a dedicated Face-to-Portrait LoRA in the wild — but it pushes the limits of 24 GB VRAM and may need quantization tricks.[^3][^4][^5]
3. **FLUX.1 Kontext [pro] at $0.04/image on fal.ai is your API sweet spot**: 8× faster than GPT-Image, native style transfer including pencil-to-painted conversions, and iterative editing up to ~6 rounds without degradation — at roughly the same per-image cost as NB2 but with faster turnaround.[^6][^7][^8]
4. **The biggest surprise: FLUX.2 [pro/flex] added multi-reference conditioning (up to 10 images, November 2025)** — meaning you can simultaneously condition on start frame + end frame + character sheet in one call, something no FLUX 1.x model could do natively.[^9][^10]
5. **For pure hand-drawn/non-photorealistic aesthetics, all generative models show a significant weakness**: they understand the concept of "pencil sketch" but tend to polish or digitize it. The workaround — already validated by the community — is training a pencil-style LoRA on Kontext [dev] directly (a "Pencil Drawing Kontext LoRA" already exists on Hugging Face) or using EbSynth V2 as a style-propagation post-processor rather than a generator.[^11][^12][^13]

***

## Master Comparison Table

| Model | Type | Char. Consistency (1–5) | Editing (1–5) | Cost/Image or VRAM | License | Pipeline Fit (1–5) |
|---|---|---|---|---|---|---|
| FLUX.1 Kontext [pro] | Closed API | 5 | 5 | $0.04 (fal.ai, Replicate, Fireworks) | Commercial | 5 |
| FLUX.1 Kontext [max] | Closed API | 5 | 5 | $0.08 (fal.ai, Replicate) | Commercial | 5 |
| FLUX.1 Kontext [dev] | Open weights | 4 | 4 | 24 GB base / 12 GB FP8 | Non-commercial free; $999/mo commercial | 5 |
| FLUX.2 [pro] | Closed API | 5 | 5 | ~$0.04–0.07 (TogetherAI) | Commercial | 5 |
| FLUX.2 [flex] | Closed API | 5 | 4 | ~$0.03 (TogetherAI) | Commercial | 4 |
| Qwen-Image-Edit-2511 | Open weights | 4 | 4 | 24 GB (needs tricks) / API ~$0.02/MP | Apache 2.0 | 4 |
| Seedream 4.0 / SeedEdit 3.0 | Closed API | 4 | 4 | $0.03 (fal.ai) | Commercial | 4 |
| Midjourney V7 (Omni Reference) | Closed web/API | 4 | 3 | $0.04–0.16/image (est. from plans) | Commercial | 3 |
| Ideogram 3.0 | Closed API | 2 | 3 | Subscription/API credits | Commercial | 2 |
| Google Imagen 4 | Closed API | 2 | 2 | $0.04 (standard) / $0.06 (Ultra) | Commercial | 2 |
| Adobe Firefly Image 4 | Closed API | 2 | 4 | $0.02–$0.10/image (enterprise $1K/mo min) | Commercial IP-safe | 3 |
| Stable Diffusion 3.5 Large | Open weights | 2 | 2 | ~15–18 GB base (11 GB FP8 TensorRT) | Community (restricted commercial) | 2 |
| HiDream-I1-Full / E1 | Open weights | 2 | 3 | 35 GB model; ~24 GB run | MIT | 2 |
| Z-Image-Turbo | Open weights | 2 | 1 | <16 GB; edit variant pending | Apache 2.0 | 2 |
| OmniGen2 | Open weights | 3 | 4 | ~17 GB VRAM | Apache 2.0 | 3 |
| IP-Adapter FaceID Plus v2 (addon) | Adapter | 4 | N/A | Runs on base model VRAM | Apache 2.0 | 4 |
| PuLID-FLUX (addon) | Adapter | 5 | N/A | Runs on FLUX.1 [dev] | Apache 2.0 | 5 |
| Character LoRA (FLUX) | Fine-tune | 5 | N/A | ~1–3 h on 4090 | Inherits base | 5 |

*Ratings are relative to this specific use case (pencil test in-betweens with character lock). "Pipeline Fit" penalizes photorealism bias and rewards editing + multi-ref conditioning.*

***

## Section 1: Closed-Source Image Generation + Editing Models

### Black Forest Labs: FLUX Family

**FLUX.1 Kontext [pro] — Released May 29, 2025**

Black Forest Labs launched FLUX.1 Kontext [pro] as a multimodal flow transformer that unifies text-to-image and image editing in a single 12B-parameter model. It accepts both text prompts and reference images as inputs, enabling targeted local edits, full-scene transformations, and — critically — character consistency without fine-tuning. The model achieves the highest scores in KontextBench for text editing and character preservation, running up to 8× faster than GPT-Image according to BFL's own benchmark.[^14][^15][^6]

**API availability and pricing:** FLUX.1 Kontext [pro] is $0.04/image on fal.ai, Fireworks AI, and Replicate. At that price point it is cost-competitive with NB2 (~$0.039/image) while offering faster throughput and a native image-edit endpoint. FLUX.1 Kontext [max] — the experimental variant with improved prompt adherence and typography — runs $0.08/image.[^16][^17]

**Editing capabilities:** The model supports instruction-edit prompts such as "change only the hand" or "convert to pencil sketch with natural graphite lines, cross-hatching, and visible paper texture" (this exact prompt was demonstrated on fal.ai's Kontext playground). Independent practitioner tests on r/FluxAI confirm it "maintains the integrity of the original image" for style-transfer tasks and handles sketch-to-painting conversions well. A published ComfyUI test on a 2D comic page demonstrated that Kontext [dev] colourized and edited without destroying line work, though the style-reference inference is somewhat shallow — it cross-references a small number of "stock styles" rather than genuinely distilling a novel aesthetic.[^8][^18][^19]

**Known weaknesses for hand-drawn styles:** The model defaults to a polished digital aesthetic when not strongly constrained. A practitioner who tried Moebius-style line art reported the output "mapped to a naff colouring-book page" rather than the original's subtle style. Mitigation: pair with a pencil-style LoRA trained on Kontext [dev] (see Section 3). Multi-turn degradation after ~6 iterative edits is documented by BFL.[^19][^6]

**Multi-image conditioning:** Single reference image per edit call in Kontext [pro/max]. True multi-reference (start + end + style simultaneously) requires FLUX.2 (see below).

***

**FLUX.2 [pro], [flex], [max], [klein] — Released November–December 2025 / January 2026**

BFL's second-generation system launches multi-reference conditioning as a native capability, accepting up to 8 images (FLUX.2 [pro/dev]) or up to 10 images (FLUX.2 [flex]) per call. This is the key upgrade for your pipeline: you can simultaneously pass start frame, end frame, and character reference sheet as conditioning inputs without fine-tuning. FLUX.2 was explicitly positioned to challenge NB2 ("Nano Banana") according to VentureBeat's coverage of the launch.[^10][^9]

FLUX.2 [flex] (~$0.03/image on TogetherAI) supports tunable parameters and is designed for typography and UI work alongside character generation. FLUX.2 [max] ($25 credits on Melies, ~$0.04–0.08 on direct API) delivers the highest quality with 4K output. FLUX.2 [dev] is an open-weight model requiring a commercial license from BFL, running ~73 GB VRAM at full precision (A6000 territory) but being fine-tuned by the community down to 4090-runnable quantizations.[^20][^21][^9]

FLUX.2 [klein], released January 2026, is BFL's fastest model — sub-second inference at lower quality, 5 credits on Melies — suited for rapid draft iterations.[^22]

***

### Ideogram 3.0 — Released March 26, 2025 / Updated May 1, 2025

Ideogram 3.0 is Ideogram's most capable model, with improved realism, prompt following, and style control. The May 2025 update added Magic Fill (inpainting) and Extend (outpainting) with style references (up to 3 reference images). **For your use case, Ideogram 3.0 is a weak fit:** it is optimized for photorealism, typographic design, and brand assets. Its style reference system can transfer aesthetics, but community reports consistently note it underperforms FLUX Kontext on non-photorealistic or hand-drawn material. No multi-image conditioning for animation consistency has been confirmed independently.[^23][^24][^25][^26]

***

### Recraft V3 — Released October 2024; V4/successors unconfirmed at time of research

Recraft V3 held the #1 position on the Artificial Analysis Text-to-Image Leaderboard on Hugging Face for over five consecutive months post-launch, with a 1172 ELO rating and 72% win rate — outperforming Midjourney v6.1 (1093 ELO) and FLUX 1.1 Pro (1143 ELO). Recraft's March 2025 pricing update reduced editing API costs significantly (erase region now $0.002, creative upscale $0.25). Recraft introduced Style Sharing in March 2025 for cross-team visual consistency. **Weakness for your pipeline:** Recraft V3 is not a multi-image or character-consistency-optimized model. It has no documented in-context editing comparable to Kontext and no animation-inbetween use cases in practitioner reports. Potentially superseded in quality by FLUX.2 and Kontext [max] as of late 2025.[^27][^28][^29]

***

### Midjourney V7 with Omni Reference — Released 2025

Midjourney V7 replaced the earlier `--cref` character reference with **Omni Reference (OW)**, which practitioners report is "a true game changer" for generating fully consistent characters. The workflow involves setting optimal Omni Reference weight (OW), style weight (SW), and image weight (IW) values to balance facial accuracy against stylistic expression. Midjourney's pricing has not changed since 2023: Basic $10/month (~200 images), Standard $30/month (unlimited Relax), Pro $60/month, Mega $120/month. A 2025 academic study confirms Midjourney V7 prompt parameters affect 2D character design consistency in measurable ways. However, Midjourney's editing pipeline (the Editor tool) is weaker than FLUX Kontext for region-specific in-place edits. **Key weakness:** No programmatic API with image-reference conditioning comparable to Kontext. The Omni Reference feature requires using the Midjourney web interface or Discord bot, making batch automation difficult. V8.1 alpha was available to some users as of early 2026.[^30][^31][^32][^33][^34]

***

### Google Imagen 4 — Released June 24, 2025; GA August 15, 2025

Google launched Imagen 4 in paid preview June 24, 2025, making it generally available August 15, 2025. Pricing: Imagen 4 Fast at $0.02/image, standard Imagen 4 at $0.04/image, Imagen 4 Ultra at $0.06/image — with 2K resolution support. Imagen 4 delivers "significant improvements in quality, particularly for text generation, over Imagen 3." **For your use case, weak fit:** Imagen 4 has no multi-image conditioning, no character reference system, and no image-edit endpoint as of the GA date. It is a pure text-to-image system positioned for marketing content and UI asset generation. Its photorealism bias makes pencil-test style output require heavy prompting.[^35][^36][^37]

***

### OpenAI gpt-image-1 / GPT Image 2.0

GPT-image-1 (the API version of ChatGPT's image generation, as distinct from DALL-E 3) is already listed in your current stack as a secondary keyframe model. The DigitalOcean image editing benchmark places "Nano Banana" (NB2) as the dominant model on leaderboards as of mid-2025, and KontextBench confirms Kontext [pro] is 8× faster than GPT-Image while delivering competitive quality. No "gpt-image-2" as a distinct new API model has been independently confirmed at time of research; the model referenced in some community discussions appears to be the same gpt-image-1 endpoint with updates. OpenAI has not published a new standalone image editing model with multi-reference conditioning as of May 2026.[^38][^6]

***

### Adobe Firefly Image 4 + Generative Fill API

Adobe Firefly consumer plans run $9.99–$199.99/month. Enterprise API pricing starts at ~$0.02–$0.10/image with a reported ~$1,000/month enterprise minimum. Adobe launched significant Firefly AI tools in April 2025, including expanded generative fill and sketch-to-image features with crosshatching and line-art presets. Firefly's key differentiator is its IP-safe training data (licensed Adobe Stock), which matters for commercial output. **For your use case, moderate fit only:** Firefly's editing tools are strong for region-in, region-out workflows, and its sketch generator handles pencil/line-art prompts. However, there is no multi-image conditioning for character consistency, and the API requires enterprise contracts for production-scale use. Generative Fill quality for non-photorealistic illustration is community-rated below FLUX Kontext.[^39][^40][^41][^42]

***

### Stability AI: Stable Image Core / Ultra / SD 3.5 Hosted APIs

Stability AI's hosted APIs (Stable Image Core, Ultra, SD 3.5) remain available but the ecosystem has fragmented since 2024. SD 3.5 Large requires ~18–20 GB VRAM in base form, reduced to ~11 GB with FP8 TensorRT (NVIDIA collaboration). Practitioner tests on a 4070 Ti Super (16 GB) show 40-step runs completing in ~45 seconds after setup. SD 3.5 Large Turbo (4-step distillation) runs significantly faster. **For your use case, weak fit:** SD 3.5 has limited character consistency support, no native multi-image conditioning, and a photorealism-biased training set. Its hosted API lacks the iterative editing features of FLUX Kontext.[^43][^44]

***

### ByteDance Seedream 4.0 + SeedEdit 3.0 — Released September 2025 / June 2025

ByteDance's Seed team released **Seedream 4.0** in September 2025 — a unified model handling T2I, image editing, and multi-image composition in a single architecture, available on fal.ai at $0.03/image. SeedEdit 3.0 (June 2025) was explicitly designed as a large diffusion model for instruction-based image editing, with "4K resolution, fine processing of edited areas and high-fidelity retention of non-edited areas." SeedEdit 3.0 achieves rapid inference within 10 seconds and has a 56.1% availability rate in human evaluations, significantly up from prior versions. Seedream 4.5 launched in May 2026 with further refinements. **For your use case, strong secondary option:** Seedream 4.0 provides a cost-effective ($0.03) editing and multi-image composition API. The identity preservation features are strong for portrait work, though practitioner testing of pencil-test/traditional animation aesthetics specifically is thin in available sources. SeedEdit is notably *not* open-source.[^45][^46][^47][^48][^49]

***

### Tencent Hunyuan API

HunyuanImage and its successors are available via Tencent Cloud API. Limited practitioner documentation for the specific use case (pencil-test animation, Western-style hand-drawn) is available in English-language sources. Evidence was insufficient to make a strong characterization — **flag as open question**.

***

### Alibaba Qwen-Image (Hosted) + Z-Image

**Qwen-Image-2512** (December 2025) is a 20B MMDiT text-to-image model that "ranks as the strongest open-source image model" in 10,000+ blind rounds on AI Arena, while staying competitive with closed-source systems. The hosted API on fal.ai is priced at $0.02/megapixel (approximately $0.02 per 1MP image).[^50][^3]

**Z-Image-Turbo** (Alibaba Tongyi Lab, November 27, 2025) is a 6B-parameter Apache 2.0 model that generates 1024×1024 images in 2.3 seconds on an RTX 4090, within 16 GB VRAM. A Z-Image-Omni-Base variant supporting both generation and editing is planned. **For your use case, weak current fit:** Z-Image-Turbo is a T2I model optimized for photorealistic portraits and Chinese/English text rendering. The edit variant (Z-Image-Edit) was not yet publicly released as of research date. Strong candidate to monitor.[^51][^52][^53]

***

## Section 2: Open-Source Image Generation + Editing Models

### FLUX.1 [dev] and FLUX.1 Kontext [dev]

**FLUX.1 [dev]** (Black Forest Labs, August 2024) is a 12B-parameter diffusion transformer licensed under the FLUX.1 Non-Commercial License (free for research; commercial license available via BFL's self-serve portal). At FP16, inference on a 4090 (24 GB) takes ~14–18 seconds per image at 20 steps. With CPU offloading and optimized ComfyUI configurations, it can run on as little as 12 GB VRAM at 1–1.5 it/s.[^54][^55][^56][^1]

**FLUX.1 Kontext [dev]** (released June 26, 2025) is the open-weights editing-focused variant. Base model uses 24 GB VRAM; NVIDIA TensorRT FP8 quantization reduces this to 12 GB (2.1× faster); FP4 for Blackwell architecture reduces to 7 GB. On a 4090 (24 GB), base FP16 takes ~80 seconds per image in ComfyUI (practitioner report); FP8 via TensorRT or standard ComfyUI quantization reduces this to approximately 30–45 seconds. A Pencil Drawing Kontext Dev LoRA has already been trained and published on Hugging Face, using the trigger phrase "Convert this image into pastel drawing style. Loose drawing, lines." The BFL self-serve commercial portal charges $999/month for commercial use of Kontext [dev]. For non-commercial portfolio work, it is free under the Non-Commercial License.[^57][^2][^13][^1][^19]

***

### Qwen-Image-Edit-2511 (Alibaba, December 2025)

This is a 20B MMDiT model under Apache 2.0 license — the key distinction from FLUX Kontext dev, which requires a $999/month commercial license for commercial use. Key improvements in 2511 over 2509 include: significantly improved character consistency (especially in multi-person group photos), integrated LoRA capabilities, enhanced geometric reasoning, and mitigated image drift. VRAM requirement in base FP16 is 18–22 GB just to load weights, bursting higher with activations — a 24 GB 4090 requires using the FastDM inference framework or GGUF quantization. Generation time is ~95 seconds per image edit at 16 GB VRAM usage on an RTX 3090 in a community script.[^58][^59][^4][^60][^3]

A fully realized "100% face consistency" ComfyUI workflow using Qwen-Image-Edit-2511 with a dedicated Face-to-Portrait LoRA (from DiffSynth-Studio) has been demonstrated publicly, showing identical facial features across different poses. A multi-image multi-edit ComfyUI workflow accepts 3 input images in a single prompt call, enabling start-frame + end-frame + reference conditioning. The community ComfyUI Blog confirms Qwen Image Edit 2511 is natively supported in ComfyUI as of December 2025.[^4][^61][^5]

***

### Stable Diffusion 3.5 Large / Medium / Turbo

SD 3.5 Large (8.1B parameters) requires ~15.5 GB dedicated VRAM at standard settings on 4070 Ti Super, with 40 steps completing in ~45 seconds after proper initialization. GGUF Q8_0 quantization reduces this to 14.5 GB; Q4_0 reduces to 8.2 GB. NVIDIA TensorRT FP8 reduces SD3.5 Large from 18+ GB to ~11 GB, delivering 2.3× performance improvement. License: Stability AI Community License (restricted commercial use without paid license for >1M monthly users). **For your pipeline, weak fit:** SD 3.5 has no in-context editing or multi-image character conditioning. Its UNet-based ControlNet ecosystem is large but the character consistency toolchain (IP-Adapter, InstantID) lags behind the FLUX ecosystem as of 2025–2026. ⚠️ *Potentially superseded* by FLUX Kontext and Qwen-Image for editing use cases.[^62][^44][^43]

***

### HiDream-I1 + HiDream-E1

HiDream.ai open-sourced HiDream-I1 on April 7, 2025: a 17B-parameter Mixture-of-Experts DiT model under MIT license, achieving state-of-the-art scores on HPSv2.1 (human preference). Model weights are 35 GB; runtime requires ~24 GB VRAM. HiDream-E1-Full (instruction-based editing) was released April 28, 2025; HiDream-E1-1 (updated editing model) was released July 16, 2025. **For your use case, moderate experimental fit:** MIT license is permissive, and the editing model exists — but community adoption for character consistency workflows has been thin (ComfyUI members flagged lack of image-to-image open-source support at launch). The model does not have documented multi-reference conditioning. Monitor for LoRA ecosystem development.[^63][^64][^65]

***

### OmniGen2 (VectorSpaceLab, June 16, 2025)

OmniGen2 is an Apache 2.0 open-source unified model for text-to-image, image editing, and in-context generation, built on Qwen-VL-2.5. It achieves state-of-the-art performance among open-source models for consistency on the OmniContext benchmark. VRAM requirement: ~17 GB (RTX 3090 or equivalent); can run on 3 GB with CPU offloading (much slower). An RL-enhanced variant (OmniGen2-RL with EditScore) was released September 30, 2025. **For your use case, good fit as a free alternative:** OmniGen2's "in-context generation" capability accepts multiple reference images and understands subject-driven tasks — meaning start-frame + end-frame + character reference conditioning is architecturally supported. However, independent comparison benchmarks against FLUX Kontext for pencil-test aesthetics are not yet available.[^66][^67][^68]

***

### DeepSeek Janus-Pro

Janus-Pro is DeepSeek's unified multimodal model (generation + understanding). Research for this specific use case yielded insufficient practitioner evidence for animation pipelines. Flag as **open question**.

***

### Z-Image (Apache 2.0, open source)

As described above, Z-Image-Turbo (6B parameters, Apache 2.0, November 2025) runs 1024×1024 in 2.3 seconds on a 4090 within 16 GB VRAM. The Z-Image-Omni-Base variant (generation + editing) has been released for community fine-tuning, with Z-Image-Edit targeting instruction-driven editing pending as of research date. **Monitor closely** — if Z-Image-Edit delivers instruction-based editing at comparable quality to Qwen-Image-Edit but with lower VRAM footprint, it could become the strongest self-hosted option.[^52][^53][^51]

***

## Section 3: Identity / Character Preservation Techniques

### IP-Adapter FaceID Plus v2 / FaceID-Portrait / SDXL FaceID Plus v2

IP-Adapter FaceID Plus v2 uses a ViT-H image encoder to extract facial identity features and inject them into cross-attention layers. Compatible with SD 1.5 and SDXL base models. In ComfyUI, the recommended workflow uses 4 reference images batched together for a stronger identity lock, then applies a two-pass (FaceID → general IP-Adapter) pipeline. Community reports on r/StableDiffusion note that FaceID is effective but tends to replicate the expression from the source image, and reducing LoRA weight to allow different expressions compromises face consistency. **For your pipeline:** FaceID is well-suited as an auxiliary conditioning layer for SDXL-based workflows, but the SDXL ecosystem has been largely superseded by FLUX-based tooling for quality work in 2025–2026. IP-Adapter nodes for FLUX exist via the cubiq/ComfyUI_IPAdapter_plus repo.[^69][^70][^71]

***

### InstantID

InstantID (2024) achieves "zero-shot identity-preserving generation with a single facial image" using an IdentityNet that combines spatial (landmark) and semantic (face embedding) conditioning. Compatible with SD 1.5 and SDXL. A 2025 r/StableDiffusion thread asks whether "InstantID + Canny is still the best method in 2025" — the consensus response is that for characters with diverse training datasets (varied poses, angles), a LoRA still outperforms InstantID for consistency. **No confirmed FLUX 1.x or FLUX 2 native port of InstantID** was found at research date; most 2025 practitioners have migrated to PuLID-FLUX for FLUX-based identity preservation.[^72][^73][^74]

***

### PuLID and PuLID-FLUX

PuLID-FLUX is the de facto standard for identity preservation on FLUX.1 [dev] as of 2025. It "allows image generation based on a single input image, preserving facial features while enabling modifications to other image aspects (clothing, background, style)." A dedicated "Flux Kontext PuLID" ComfyUI workflow (published August 2025 on RunComfy) combines FLUX DiT architecture + Kontext Adapter + PuLID identity control, allowing identity lock from a single face reference with full pose/scene freedom. Users control identity strength via `Weight`, `Start At`, and `End At` parameters during the sampling timeline.[^75][^76]

**PuLID-FLUX** works on FLUX.1 [dev] running on ComfyUI; VRAM requirements mirror FLUX.1 [dev] (~12–24 GB depending on quantization). Setup complexity: moderate (requires ComfyUI, cubiq IPAdapter nodes, and PuLID models — multiple installs). A YouTube tutorial from February 2025 demonstrates building and using PuLID in ComfyUI step-by-step.[^77]

***

### Character LoRA Training (FLUX Best Practices)

Training a character LoRA on FLUX.1 [dev] on a 4090 (24 GB) is the gold-standard approach for maximum consistency — allowing the model to memorize a specific character's visual identity. Key parameters from practitioner consensus:

- **Dataset size:** 20–30 high-quality images are widely recommended; some practitioners report strong results with as few as 10 carefully curated images. Diversity matters more than quantity: varied lighting, angles, expressions, and distances.[^78][^79]
- **Training time on 4090:** Full-layer training takes "hours" (2.5–3 seconds/iteration); partial layer training (2 layers only) reduces to 20–30 minutes but at lower quality. With AI-Toolkit and reasonable settings, 1,000–1,500 steps on 20 images typically takes 30–90 minutes on a 4090.[^80][^78]
- **Recommended settings for small dataset (20–30 images):** `learning_rate=1e-4`, `max_train_steps=1500`, `network_dim=32`, `network_alpha=16`. For 60+ images: scale steps proportionally to 3,000+.[^78]
- **FLUX vs SDXL for character LoRA:** FLUX character LoRAs produce noticeably higher fidelity identity preservation than SDXL counterparts, at the cost of larger LoRA file size and longer training. The FLUX architecture's joint text-image attention makes identity-prompt alignment stronger.
- **Kontext LoRA training:** BFL published a guide for Flux Kontext LoRA training (June 30, 2025) covering image-to-image translation tasks. This is specifically useful for training a "pencil-test style" LoRA that converts character frames into the target aesthetic.[^81]

For your workflow: training a **character LoRA on FLUX.1 Kontext [dev]** (rather than FLUX.1 [dev]) allows the identity lock to work *within* the editing pipeline, meaning Kontext can edit a frame while simultaneously referring to your character LoRA. This is more efficient than chaining separate identity + editing adapters.

***

### Textual Inversion / Pivotal Tuning / DreamBooth

These older techniques (Textual Inversion, DreamBooth-style fine-tuning) are largely superseded for FLUX-based workflows. For SDXL they remain viable but the ecosystem focus has shifted. DreamBooth LoRA on FLUX (available via diffusers) is essentially equivalent to LoRA training in practice.

***

### ConsiStory, StoryDiffusion, IC-LoRA

These research techniques address multi-scene character consistency through cross-frame attention mechanisms. StoryDiffusion (cross-image attention) and ConsiStory (subject-driven) are academic methods showing strong results for illustration but limited public ComfyUI adoption as of 2025–2026. The Consistent Character Creator 3.8 workflow on RunComfy (March 2026) uses **Qwen Image Edit** with specialized conditioning groups as the practical equivalent.[^82]

***

### Reference-Only ControlNet

Reference-Only ControlNet (for SDXL/SD 1.5) allows using an image as a soft structural reference without training. Less precise than IP-Adapter FaceID for character identity. Relevant for maintaining *pose and construction line layout* from your reference frame in in-betweens — can be combined with IP-Adapter for dual conditioning (pose from reference + face from FaceID). FLUX-compatible ControlNet variants (Canny, Depth, etc.) are available via InstantX and other community contributors.

***

## Section 4: In-Between Specific Workflows

### ToonCrafter: Generative Cartoon Interpolation

ToonCrafter (arXiv May 2024, open source on GitHub/HuggingFace) is a generative video interpolation model specifically designed for cartoon-style in-betweening. It accepts two keyframes and generates intermediate frames, handling non-linear motion and occlusion that traditional optical-flow methods fail on. Practitioner tests show "fantastic consistency" for character motion on simple scenes at 10 FPS outputs; more complex scenes with rapid direction changes may show artifacts. Available free on Hugging Face Spaces. **Key limitation:** ToonCrafter outputs video frames at fixed resolution (typically 512×320 or 512×512); upscaling to 16:9 at production resolution requires a separate pass. It does not support arbitrary character reference injection — it interpolates between the two provided frames only, using their visual content as the character source.[^83][^84][^85]

A January 2025 survey of GenAI for Cel-Animation names ToonCrafter alongside AniDoc and AniSora as the leading tools for automating inbetween frame generation.[^86][^87]

***

### EbSynth V2 — Released September 2025

EbSynth V2 launched in September 2025 as a browser-based tool with a new UI featuring real-time preview, timeline, layers, and brush tools — "around 10× faster" texture synthesis than the original. EbSynth is **not a generative AI model** — it uses example-based texture synthesis to propagate a painted keyframe across a video sequence, guided by optical flow. This makes it uniquely relevant for your workflow: you can use EbSynth to propagate your hand-drawn pencil-test aesthetic from a single stylized keyframe across the Seedance-interpolated frames, without hallucination or identity drift.[^88][^12][^11]

**Pricing:** Free tier (720p MP4 export); Pro $20/month (4K, PNG sequence export, 100 AI-generated keyframes/month using Stability AI SDXL 1.0). An offline command-line version is available for studios at negotiated pricing. **Recommended role in your pipeline:** Post-processing layer to apply hand-drawn style after motion generation, rather than as a primary in-between generator.[^12]

A 2025–2026 academic study confirms EbSynth's value in optimizing rotoscope animation for stylized characters, including research on facial marker strategies to improve propagation fidelity.[^89]

***

### CACANi

CACANi remains the specialist tool for traditional 2D animation in-betweening, using curve-based "assisted tweening" that does not require generative AI. It is designed for clean-line animation with frame-by-frame structure, making it a better fit for pre-digital production workflows than for AI-augmented pencil-test generation. No generative AI integration announced as of research date.[^90]

***

### Toon Boom Harmony with Ember — Beta March 2025

Toon Boom launched Ember (beta March 2025) as a suite of AI tools for Harmony Premium and Storyboard Pro. Current features: Script Breakdown, Mask Generation, Image Eraser, Expand Image, Increase Image Resolution, and Rough Track Generation. **Notably absent:** Generative in-between frame synthesis. Toon Boom Ember is focused on productivity tools (mask generation, background extension, upscaling) rather than replacing the inbetweener role. Ember remains in beta as of March 2025 through Harmony 25 release timeline.[^91]

***

### Netflix INKubator (Internal Program)

Netflix launched a quiet internal generative AI animation initiative called INKubator in March 2025 — job listings for producers, engineers, and CG artists, with no public press release. No confirmed external workflow details are available. The program signals that major studios are actively investing in production-grade AI animation pipelines rather than one-off demos.[^92]

***

### AI-Specific Inbetween Workflows in ComfyUI

The IF-Animation-Workflows repository (GitHub: if-ai/IF-Animation-Workflows) provides a production-grade ComfyUI workflow suite for animation, including:
- `IF_Inbetweeners`: Select a few frames, create in-betweens
- `IF_KeyAnimation_Helper`: Extract keyframes, redraw externally, reimport
- `IF_Animator`: Full animation pipeline wrapping FLUX LoRA, ControlNet, and WAN wrapper[^93][^94]

The recommended workflow for 2D animation at 12 FPS is 8-frame chunks, corresponding to AnimateDiff's native 2-second output window. WAN 2.2 Animate (14B parameter model for character animation from a single portrait) runs at 16 GB VRAM (FP8) in ComfyUI, generating animations in 10–15 minutes per sequence on a 4090.[^95][^93]

For the specific "frame N → frame N+1 with character lock" workflow, the current practitioner best practice is:
1. Seedance (your existing tool) for motion interpolation
2. FLUX Kontext [dev] or Qwen-Image-Edit-2511 for redraw/style correction of selected frames
3. PuLID-FLUX or Character LoRA for identity lock during redraw
4. EbSynth V2 for aesthetic propagation of pencil-test style across the full sequence

***

## Section 5: Recommended Pipeline Configurations

### Config A — Best Quality (Closest to NB2 for In-Betweens)

**Goal:** Maximum character fidelity and aesthetic authenticity, cost secondary.

| Component | Choice | Rationale |
|---|---|---|
| Base model | FLUX.2 [pro] (TogetherAI or fal.ai) | Multi-reference conditioning accepts start frame + end frame + character sheet simultaneously; highest FLUX generation quality |
| Multi-reference input | Up to 8 reference images | Pass start keyframe, end keyframe, and 1–6 character reference angles |
| Editing / in-place correction | FLUX.1 Kontext [max] ($0.08/image) | Premium consistency for targeted edits (fix hand, correct ear, adjust line weight) |
| Character lock | Character LoRA for FLUX (Kontext dev training) + PuLID-FLUX | LoRA for identity; PuLID for zero-shot cross-scene consistency |
| Aesthetic | Pencil-style Kontext LoRA ("Pencil Drawing Kontext Dev LoRA" on HuggingFace) or custom fine-tuned equivalent | Locks pencil-test on cream paper aesthetic at inference, no post-processing needed |
| Post-processing | EbSynth V2 Pro ($20/month) | Propagate pencil grain, hole-punch marks, paper texture across interpolated frames |
| **Estimated cost** | ~$0.07–0.10/frame (FLUX.2 + selective Kontext max edits) | ~50% cheaper than NB2 at scale, with superior multi-ref conditioning |
| **Expected quality vs NB2** | Equivalent for character consistency; potentially better for in-betweens due to native start+end frame conditioning | NB2 currently has no documented multi-reference in-between use case |
| **Known failure modes** | FLUX.2 [pro] multi-ref can "ignore" background or style references when primary character reference dominates (practitioner report)[^21]; Kontext max degrades after ~6 iterative edits[^6] |

***

### Config B — Best Value (Biggest Cost Savings, Recognizable Character Consistency)

**Goal:** Maximize cost reduction while keeping the character recognizably "Sean" across in-betweens.

| Component | Choice | Rationale |
|---|---|---|
| Base model | FLUX.1 Kontext [pro] ($0.04/image, fal.ai) | Same cost as NB2, but natively optimized for editing from reference; 8× faster than GPT-Image |
| Character conditioning | Character LoRA (trained once on 4090, ~1–3 hours) + Kontext [pro] reference input | One-time LoRA training amortizes across all in-betweens; LoRA embedded into Kontext call |
| Editing | FLUX.1 Kontext [pro] iterative edits | Re-use the same $0.04/call model for targeted corrections |
| Aesthetic | Prompt engineering ("hand-drawn pencil test on cream animation paper, visible construction lines, cross-hatching, pencil grain") + Pencil LoRA from HuggingFace | No extra per-image cost |
| Post-processing | EbSynth V2 free tier (720p) or Pro ($20/month for 4K PNG) | Style propagation catches texture drift without per-frame API cost |
| **Estimated cost** | ~$0.04/frame for generation; LoRA training ~$5–10 Runpod one-time capex | ~50% cheaper than NB2 at equivalent volume |
| **Expected quality vs NB2** | 85–90% of NB2 for character fidelity; pencil-test aesthetic requires prompt discipline or LoRA to avoid digital polish | Acceptable for in-betweens where start + end frames are NB2-grade |
| **Known failure modes** | Kontext [pro] single-reference only (no native multi-ref) — workaround: run character LoRA for identity + use Kontext for scene edit; expression replication from reference (PuLID mitigates) |

***

### Config C — Fully Self-Hosted (Single RTX 4090, 24 GB, Zero API Cost)

**Goal:** $0 ongoing cost after hardware/setup. Non-commercial portfolio use.

| Component | Choice | Rationale |
|---|---|---|
| Base model | FLUX.1 Kontext [dev] (FP8 quantized via GGUF or TensorRT) | 12 GB VRAM at FP8; non-commercial free; ComfyUI day-0 support[^1][^2] |
| Multi-image conditioning | OmniGen2 (17 GB VRAM, Apache 2.0) as alternative for 3-input editing | Accepts start + end + character ref; lower quality than Kontext but zero API cost |
| Character lock | Character LoRA (FLUX Kontext [dev] trained locally on 4090) + PuLID-FLUX nodes in ComfyUI | PuLID weights load alongside Kontext [dev] in 24 GB with FP8 | 
| Aesthetic | Custom "pencil-test on cream paper" LoRA (train on 20–30 cropped NB2 approved frames, ~1–2 hours) | Best aesthetic fidelity; no per-image cost after training |
| In-betweens | ToonCrafter (free HuggingFace Spaces or local) for motion interpolation prior to redraw | Replace Seedance's role for fully local workflow |
| Post-processing | EbSynth V2 CLI (free for offline, pricing on enquiry for studio license) or EbSynth free web for 720p | Pencil grain propagation |
| **Estimated cost** | $0 ongoing (4090 electricity); $2,500–4,000 capex if purchasing 4090 | Amortized across entire animation career |
| **Expected quality vs NB2** | 70–80% on character consistency (FP8 Kontext dev vs NB2 closed API); 90%+ with well-trained LoRA | Sufficient for in-betweens where NB2 handles keyframes |
| **Known failure modes** | 4090 24 GB is *exactly* at the limit for FP8 Kontext dev — other apps must be closed; OmniGen2 requires offloading tricks at 24 GB; ToonCrafter works best at ≤512 resolution, requiring upscale pass[^2][^96] |

***

## Open Questions / Evidence Gaps

1. **Tencent HunyuanImage 2.1 API capabilities** — English-language practitioner reports for pencil-test animation are thin. Official documentation exists in Chinese; API availability and Western ecosystem adoption unconfirmed at research date.

2. **DeepSeek Janus-Pro for animation in-betweens** — Insufficient evidence found for this specific use case. Janus-Pro is primarily benchmarked for visual QA and T2I, not editing pipelines.

3. **FLUX.2 [dev] character LoRA stability** — Community testing of multi-reference FLUX.2 [dev] with 6–8 input images shows VRAM usage of 73+ GB at full precision (A6000 territory). Quantized/community-optimized versions for 4090 were not yet widely available at research date.[^21]

4. **SeedEdit 3.0 / Seedream 4.0 hand-drawn aesthetic fidelity** — Strong for photorealistic portrait editing; no confirmed practitioner tests with traditional animation pencil-test aesthetics in available sources.

5. **AnimateDiff + Character LoRA quality for pencil-test frames** — AnimateDiff for in-betweens (temporal consistency layer) is widely used for photorealistic animation but community reports for hand-drawn / non-photorealistic output are sparse.

6. **FLUX.2 [dev] open-weight commercial license terms** — BFL confirmed a commercial license is required, but pricing structure for [dev] (vs. the $999/month Kontext [dev] commercial license) was not clearly documented at research date.

7. **OmniGen2 ComfyUI workflow for start+end frame conditioning** — Architecturally supported but a turnkey ComfyUI workflow for this specific animation use case was not found in available community sources.

***

## Citations Index

All claims above are cited inline. Key primary sources:

- Black Forest Labs official announcements: bfl.ai/announcements/flux-1-kontext-dev, bfl.ai/blog/flux-2[^97][^1]
- Together AI FLUX.2 launch: together.ai/blog/flux-2-multi-reference[^9]
- fal.ai pricing pages: fal.ai/models/fal-ai/flux-pro/kontext, fal.ai/pricing[^7][^50]
- Lumenfall pricing aggregator: lumenfall.ai[^17][^98][^16]
- NVIDIA TensorRT Kontext optimization: gigazine.net/gsc_news, nvidia.com/blog[^99][^2]
- BFL GitHub: github.com/black-forest-labs/flux[^100]
- Qwen-Image GitHub: github.com/QwenLM/Qwen-Image[^3]
- OmniGen2 arXiv: arxiv.org/abs/2506.18871[^67]
- HiDream-I1 GitHub: github.com/HiDream-ai/HiDream-I1[^64]
- ToonCrafter arXiv: arxiv.org/pdf/2405.17933[^83]
- EbSynth V2 launch: cgchannel.com/2025/10, digitalproduction.com[^11][^12]
- Toon Boom Ember: toonboom.com[^91]
- Pencil Drawing Kontext LoRA: huggingface.co/gokaygokay[^13]
- ComfyUI Qwen 2511 integration: blog.comfy.org[^4]
- r/StableDiffusion LoRA training: reddit.com/r/StableDiffusion[^79][^80]
- PuLID-FLUX ComfyUI: runcomfy.com/flux-kontext-pulid[^76]
- Z-Image-Turbo: github.com/Tongyi-MAI/Z-Image, comfyui-wiki.com[^53][^52]
- Ideogram 3.0: ideogram.ai/features/3.0, ideogram_ai on X[^25][^26]
- Google Imagen 4: developers.googleblog.com[^36][^37]
- ByteDance SeedEdit 3.0: seed.bytedance.com[^101][^45]
- Seedream 4.0: fal.ai/models/bytedance/seedream/v4[^47][^48]

---

## References

1. [FLUX.1 Kontext [dev] - Open Weights for Image Editing](https://bfl.ai/announcements/flux-1-kontext-dev) - June 26, 2025. FLUX.1 ... Human preference evaluations on KontextBench, our newly released image edi...

2. [NVIDIA has developed a memory-saving, high-speed ... - GIGAZINE](https://gigazine.net/gsc_news/en/20250703-nvidia-flux-1-kontext-vram-tensorrt/) - The base model of FLUX.1 Kontext [dev] uses 24GB of VRAM and requires an expensive graphics card wit...

3. [QwenLM/Qwen-Image](https://github.com/QwenLM/Qwen-Image) - Qwen-Image is a powerful image generation foundation model capable of complex text rendering and pre...

4. [Qwen Image Edit 2511 & Qwen Image Layered in ComfyUI](https://blog.comfy.org/p/qwen-image-edit-2511-and-qwen-image) - Better Character Consistency Significantly improved character consistency, especially in multi-perso...

5. [100% Face Consistency with Qwen Image Edit 2511 in ComfyUI](https://www.youtube.com/watch?v=ydzMmHhm_9c) - The workflow has been updated to use the Qwen Edit 2511 model Join our premium community and try it ...

6. [Black Forest Labs Releases FLUX.1 Kontext: Context-Aware Image ...](https://comfyui-wiki.com/en/news/2025-05-30-flux-kontext-release) - As a multimodal flow model, FLUX.1 Kontext combines advanced character consistency preservation, con...

7. [FLUX.1 Kontext [pro] (Image to Image) API on fal - Fal.ai](https://fal.ai/models/fal-ai/flux-pro/kontext) - FLUX.1 Kontext [pro] handles both text and reference images as inputs, seamlessly enabling targeted,...

8. [FLUX.1 Kontext: AI Image Editor | Generative Photoshop Fill | fal.ai](https://fal.ai/flux-kontext) - Edit images intelligently with FLUX Kontext AI Image Editor. Advanced typography, precise editing. P...

9. [FLUX.2: Multi-reference image generation now ... - Together AI](https://www.together.ai/blog/flux-2-multi-reference-image-generation-now-available-on-together-ai) - Production-grade image generation with multi-reference consistency, exact brand colors, and reliable...

10. [Black Forest Labs launches Flux.2 AI image models to ... - VentureBeat](https://venturebeat.com/ai/black-forest-labs-launches-flux-2-ai-image-models-to-challenge-nano-banana) - FLUX.2 introduces multi-reference conditioning, higher-fidelity outputs and improved text rendering,...

11. [EbSynth V2: Real-Time Preview, Timeline & Layers](https://digitalproduction.com/2025/09/24/ebsynth-v2-real-time-preview-timeline-layers/) - EbSynth – a tool for animations from videos by style transfer of reference images. EbSynth is a free...

12. [EbSynth 2 can turn video into animation without using AI - CG Channel](https://www.cgchannel.com/2025/10/ebsynth-2-can-turn-video-into-animation-without-using-ai/) - Neat browser-based stylization, retouching and roto tool uses texture synthesis to transfer the look...

13. [gokaygokay/Pencil-Drawing-Kontext-Dev-LoRA - Hugging Face](https://huggingface.co/gokaygokay/Pencil-Drawing-Kontext-Dev-LoRA) - Convert this image into pastel drawing style. Loose drawing, lines. Download model Weights for this ...

14. [FLUX.1 Kontext models: Character consistency and precise image ...](https://www.together.ai/blog/flux-1-kontext) - FLUX.1 Kontext allows you to prompt with both text and images, and seamlessly extract and modify vis...

15. [What is FLUX.1 Kontext? Pro vs Max, Capabilities & Examples](https://fireworks.ai/blog/flux-kontext-launch) - As a multimodal flow model, it combines state-of-the-art character consistency, context understandin...

16. [FLUX.1 Kontext [max] Pricing & Providers - Lumenfall](https://lumenfall.ai/models/black-forest-labs/flux.1-kontext-max/providers) - Compare 4 providers and pricing for FLUX.1 Kontext [max]. Find the cheapest API provider through Lum...

17. [FLUX.1 Kontext [pro] Pricing & Providers - Lumenfall](https://lumenfall.ai/models/black-forest-labs/flux.1-kontext-pro/providers) - Compare 4 providers and pricing for FLUX.1 Kontext [pro]. Find the cheapest API provider through Lum...

18. [Flux Kontext is great at finishing sketches/illustrations - Reddit](https://www.reddit.com/r/FluxAI/comments/1l2ifd0/flux_kontext_is_great_at_finishing/) - Flux Kontext is great for character design. You could go further with prompt like: Make a fullbody f...

19. [Flux Kontext Dev – first tests - 2D digital art and painting](https://sketchbooky.wordpress.com/2025/06/30/flux-kontext-dev-first-tests/) - Takes about 80 seconds per image, for me. I'm definitely not impressed by its rather basic colourisa...

20. [FLUX Models Comparison: Schnell vs Dev vs Pro vs Max (2026)](https://melies.co/compare/flux-models) - 2 Max) deliver the best quality with 4K output, character consistency across images, and advanced ed...

21. [FLUX.2 image reference experiments with generation times - Reddit](https://www.reddit.com/r/StableDiffusion/comments/1p7fx0x/flux2_image_reference_experiments_with_generation/) - With 20 steps, using official Comfy UI workflow: 1 reference image, 26sec, 1.38s/it. 4 reference ima...

22. [Black Forest Labs - Frontier AI Lab](https://bfl.ai) - Black Forest Labs is the AI company behind FLUX, the state-of-the-art image generation model. Try FL...

23. [Ideogram 3.0 Deep Review & Comparison with 2.0 and 2a](https://blog.laprompt.com/ai-news/ideogram-3-0-deep-review-comparison-with-2-0-and-2a) - Is Ideogram 3.0 the best AI art generator yet? Compare Ideogram 3.0 vs. 2.0 and 2a in this in-depth ...

24. [Available Models - Ideogram](https://docs.ideogram.ai/using-ideogram/generation-settings/available-models)

25. [Ideogram - X](https://x.com/ideogram_ai/status/1917985285679530232)

26. [3.0](https://ideogram.ai/features/3.0) - Our most capable model yet. Photorealistic images, legible text, and precise style control in a sing...

27. [Big update for Recraft API users! We've refined our ... - Instagram](https://www.instagram.com/p/DHbhMhFMr6K/) - 30 likes, 4 comments - recraftai on March 20, 2025: "Big update for Recraft API users! We've refined...

28. [Introducing Recraft AI Recraft V3 on WaveSpeedAI | WaveSpeed Blog](https://wavespeed.ai/blog/posts/introducing-recraft-ai-recraft-v3-on-wavespeedai/) - Style consistency: Maintains visual coherence across multiple generations—crucial for brand work ......

29. [Introducing Style Sharing: Maintain Design Consistency Across Teams](https://www.recraft.ai/blog/introducing-style-sharing-maintain-design-consistency-across-teams) - Recraft lets designers share saved styles with teammates, clients, and collaborators — keep visuals ...

30. [A Study on the Consistency and Commercial Applicability of 2D Characters in AI-Based Design - Focusing on Midjourney V7 Prompt Parameters -](https://kiss.kstudy.com/Detail/Ar?key=4196740)

31. [Creating Consistent Characters with Midjourney V7 - Facebook](https://www.facebook.com/groups/mj.prompt.tricks/posts/1823843728163035/) - By following these tips, users can effectively utilize Omni Reference to maintain consistency in the...

32. [Midjourney Pricing 2026: Any Changes? 3-Year History](https://www.saaspricepulse.com/tools/midjourney) - Did Midjourney raise prices? Track 3 years of pricing: Basic $10, Standard $30, Pro $60, Mega $120. ...

33. [Midjourney May 2026 Update: V8.1, Pricing & Video - PixVerse AI](https://pixverse.ai/en/blog/midjourney-ai-image-generator-review) - Midjourney has four main monthly plans: Basic at $10, Standard at $30, Pro at $60, and Mega at $120....

34. [Comparing Midjourney Plans](https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans) - Monthly Price, $10, $30, $60, $120 ; Annual Price, $96 ($8 / month), $288 ($24 / month), $576 ($48 /...

35. [Imagen 4 - API, Specs, Playground & Pricing - Puter Developer](https://developer.puter.com/ai/google/imagen-4.0/) - Imagen 4 is Google DeepMind's flagship text-to-image generation model, available through the Gemini ...

36. [Imagen 4 is now available in the Gemini API and Google AI Studio](https://developers.googleblog.com/en/imagen-4-now-available-in-the-gemini-api-and-google-ai-studio/) - Explore Imagen 4, Google's advanced text-to-image model, now in paid preview via Gemini API and Goog...

37. [Announcing Imagen 4 Fast and the general availability of the Imagen 4 ...](https://developers.googleblog.com/en/announcing-imagen-4-fast-and-imagen-4-family-generally-available-in-the-gemini-api/) - Discover Imagen 4 Fast, Google's new speed-optimized text-to-image model, now generally available wi...

38. [Comparing the best Image Editing AI Models - DigitalOcean](https://www.digitalocean.com/community/tutorials/image-editing-model-review) - Nano Banana is an image editing model that excels at all tasks and measurements, and dominates the i...

39. [Compare plans that include generative AI | Adobe Firefly](https://www.adobe.com/products/firefly/plans.html) - Unlimited access to standard image features like Generative Fill. Access to premium features like Te...

40. [Adobe Firefly API Pricing 2026 (Credits + Generative Fill) | SudoMock](https://sudomock.com/blog/adobe-firefly-api-pricing-2026) - Adobe Firefly API costs $0.02-0.10 per image with a ~$1,000/month enterprise minimum. Consumer plans...

41. [Adobe Revolutionizes AI-Assisted Creativity with Firefly, the All-In ...](https://news.adobe.com/news/2025/04/adobe-revolutionizes-ai-assisted-creativity-firefly) - Firefly empowers creators to generate images, video, audio and vectors from a single place with unma...

42. [AI Sketch Generator: Create AI sketches free – Adobe Firefly](https://www.adobe.com/products/firefly/features/ai-sketch-generator.html) - The Firefly AI sketch generator turns text or images into hand-drawn sketches instantly. Create sket...

43. [Is SD 3.5 Large supposed to use over 16 GB VRAM and run ... - Reddit](https://www.reddit.com/r/StableDiffusion/comments/1hjkc92/is_sd_35_large_supposed_to_use_over_16_gb_vram/) - I have just installed ComfyUI and downloaded Stable Diffusion 3.5 Large. I downloaded first just CLI...

44. [TensorRT Boosts Stable Diffusion 3.5 on RTX GPUs | NVIDIA Blog](https://blogs.nvidia.com/blog/rtx-ai-garage-gtc-paris-tensorrt-rtx-nim-microservices/) - To address the VRAM limitations of SD3.5 Large, the model was quantized with TensorRT to FP8, reduci...

45. [ByteDance Releases Image Editing Model SeedEdit 3.0 ... - AIBase](https://www.aibase.com/news/www.aibase.com/news/18708) - This new version of the image editing model has made significant progress in aspects such as maintai...

46. [ByteDance SeedEdit, OpenSource image editor to change text ...](https://www.reddit.com/r/singularity/comments/1guuirr/bytedance_seededit_opensource_image_editor_to/) - What is even the point of a photo in this world? I watch people on the train editing a photo for 45 ...

47. [Bytedance Seedream V4 Edit (Image to Image) API on fal - Fal.ai](https://fal.ai/models/fal-ai/bytedance/seedream/v4/edit) - A new-generation image creation model ByteDance, Seedream 4.0 integrates image generation and image ...

48. [Seedream 4.0 on fal: Fast, Consistent, 4K-Ready Image Creation](https://blog.fal.ai/seedream-4-0-on-fal-fast-consistent-4k-ready-image-creation/) - Seedream 4.0 is a multi-purpose image model that unifies text-to-image, image editing, and multi-ima...

49. [fal.ai Blog | Generative AI Model Releases & Tutorials](https://blog.fal.ai) - Seedream 4.5 is Now Available on fal. We're excited to bring Seedream 4.5 to fal at day 0. Latest up...

50. [GenAI API Pricing: Haliuo, Vidu, Pixverse | Pay-Per-Use - Fal.ai](https://fal.ai/pricing) - fal offers a simple pricing model for developers to generate media with AI. Get started with a free ...

51. [What Is Z Image Model? Alibaba's Open-Source AI Generator](https://pxz.ai/blog/what-is-z-image-model) - Z Image is a 6 billion parameter open source text to image AI model developed by Alibaba's Tongyi La...

52. [Alibaba Tongyi Lab Releases Z-Image-Turbo - ComfyUI Wiki](https://comfyui-wiki.com/en/news/2025-11-27-alibaba-z-image-turbo-release) - On November 27, 2025, Alibaba Tongyi Lab officially released Z-Image-Turbo, a next-generation effici...

53. [Tongyi-MAI/Z-Image - GitHub](https://github.com/Tongyi-MAI/Z-Image) - Z-Image is a powerful and highly efficient image generation model family with 6B parameters. Current...

54. [How much VRAM do I need for FLUX? : r/StableDiffusion - Reddit](https://www.reddit.com/r/StableDiffusion/comments/1eqvvg3/how_much_vram_do_i_need_for_flux/) - At fp16 they take around 24gb of vram to run but can be busted down to around 8 or lower but you wil...

55. [This gist shows how to run Flux on a 24GB 4090 card with Diffusers.](https://gist.github.com/sayakpaul/23862a2e7f5ab73dfdcc513751289bea) - Simply version that works well on RTX 4090. Avg 4.5->5s for text encoder, 1->1.2 it/s for denoise mo...

56. [Share Your GPU and Flux Dev Render Times - Reddit](https://www.reddit.com/r/StableDiffusion/comments/1epnb8i/share_your_gpu_and_flux_dev_render_times_help/) - For reference, here are my results with a 4090 GPU and 64GB RAM: UI: Comfy. FP16: 18 seconds. FP8: 1...

57. [Flux.1 kontext dev released as free tool - Facebook](https://www.facebook.com/groups/comfyui/posts/717282867711083/) - For commercial use it is not free, they changed the license of their models. To use Kontext commerci...

58. [Qwen/Qwen-Image-Edit · Run locally with 24 GB VRAM some GPU's ...](https://api-inference.huggingface.co/Qwen/Qwen-Image-Edit/discussions/25) - Hi guys ! There is no need to give much detail, Once you examine the script, you will understand eve...

59. [Qwen-Image-Edit-2509适配哪些硬件配置？GPU需求说明](https://blog.csdn.net/weixin_35636570/article/details/155606672) - 文章浏览阅读911次，点赞18次，收藏28次。本文详细分析Qwen-Image-Edit-2509模型的GPU配置要求，涵盖显存、精度、带宽和并行计算等关键指标，明确A100/H100为生产首选，RT...

60. [unsloth/Qwen-Image-Edit-2511-GGUF - Hugging Face](https://huggingface.co/unsloth/Qwen-Image-Edit-2511-GGUF) - Key enhancements in Qwen-Image-Edit-2511 include: mitigate image drift, improved character consisten...

61. [Qwen image edit 2511 multi edit workflow - Facebook](https://www.facebook.com/groups/comfyui/posts/895256466580388/) - • Improved character & identity consistency • Stronger ... Qwen Edit workflows for smarter and more ...

62. [How much VRAM do I need for SD3.5 in ComfyUI?](https://www.reddit.com/r/StableDiffusion/comments/1kz6w0h/how_much_vram_do_i_need_for_sd35_in_comfyui/) - How much VRAM do I need for SD3.5 in ComfyUI?

63. [HiDream-I1 Open Source Release - Next Generation Image ...](https://comfyui-wiki.com/en/news/2025-04-08-hidream-i1-open-source-release) - HiDream.ai officially open-sourced their latest text-to-image model HiDream-I1 on April 7, 2025. Wit...

64. [HiDream-I1 - GitHub](https://github.com/HiDream-ai/HiDream-I1) - May 28, 2025: We've released our technical report HiDream-I1: A High-Efficient Image Generative Foun...

65. [hidream-i1 open-source image generative model - Facebook](https://www.facebook.com/groups/comfyui/posts/657178970388140/) - In April 2025, HiDream's self‑developed open‑source image generation model HiDream‑I1 reached the to...

66. [OmniGen2 AI: Advanced Multimodal Generation & Image Editing](https://omnigen2.net) - OmniGen2 is a versatile open-source generative model for visual understanding, text-to-image generat...

67. [OmniGen2: Towards Instruction-Aligned Multimodal Generation - arXiv](https://arxiv.org/abs/2506.18871) - In this work, we introduce OmniGen2, a versatile and open-source generative model designed to provid...

68. [OmniGen2/OmniGen2-RL - Hugging Face](https://huggingface.co/OmniGen2/OmniGen2-RL) - We’re on a journey to advance and democratize artificial intelligence through open source and open s...

69. [Create Consistent Characters in ComfyUI with IPAdapter FaceID Plus](https://www.runcomfy.com/comfyui-workflows/create-consistent-characters-in-comfyui-with-ipadapter-faceid-plus) - Achieve consistency in character design using ComfyUI with the IPAdapter FaceID Plus model — ideal f...

70. [IP Adapter FaceID for character consistency : r/StableDiffusion - Reddit](https://www.reddit.com/r/StableDiffusion/comments/1ihjdrb/ip_adapter_faceid_for_character_consistency/) - I do occasionally encounter posts that claim how IPAdapter FaceID does not work, and one should use ...

71. [IPAdapter FaceID Plus Workflow Guide (ComfyUI Shortcut) - YouTube](https://www.youtube.com/watch?v=Q8ymEUprDaM) - Master face consistency in ComfyUI using the IPAdapter FaceID Plus workflow. This 3-minute shortcut ...

72. [InstantID: Zero-shot Identity-Preserving Generation in Seconds](https://github.com/instantX-research/InstantID) - InstantID is a new state-of-the-art tuning-free method to achieve ID-Preserving generation with only...

73. [InstantID](https://instantid.github.io) - InstantID demonstrates exceptional performance and efficiency, proving highly beneficial in real-wor...

74. [Is InstantID + Canny still the best method in 2025 for generating ...](https://www.reddit.com/r/StableDiffusion/comments/1p22zbb/is_instantid_canny_still_the_best_method_in_2025/) - Yes, if you craft a dataset of a character in a vast variety of poses then you can use the resulting...

75. [Flux PuLID Face Swap Inpainting Consistent Character Workflow](https://civitai.com/models/929131/flux-pulid-face-swap-inpainting-consistent-character-workflow) - Flux PuLID Face Swap Inpainting ComfyUI Tutorial: This summarizes the key points from the provided e...

76. [Flux Kontext Pulid | Consistent Character Generation - RunComfy](https://www.runcomfy.com/comfyui-workflows/flux-kontext-pulid-consistent-character-generation) - Flux Kontext Pulid is a specialized character generation workflow that utilizes FLUX DiT architectur...

77. [Making Consistent Faces with PuLID for Flux - YouTube](https://www.youtube.com/watch?v=9FxeBiE-uJE) - comfyui #aitutorials #fluxai This Tutorial explains how to build and utilize PuLID to create consist...

78. [Perfect LoRA Training parameters human character - Models](https://discuss.huggingface.co/t/perfect-lora-training-parameters-human-character/147211) - To create a precise LoRA model of your human character using Kohya_ss scripts with FLUX, SD1.5, and ...

79. [Most posts I've read says that no more than 25-30 images should be ...](https://www.reddit.com/r/StableDiffusion/comments/1j8ntgi/most_posts_ive_read_says_that_no_more_than_2530/) - Most posts I've read says that no more than 25-30 images should be used when training a Flux LoRA, b...

80. [At least last time, training Flux Lora with GPU 4090 is really slow, it ...](https://www.reddit.com/r/StableDiffusion/comments/1ii8w2b/at_least_last_time_training_flux_lora_with_gpu/) - Training Flux Lora with GPU 4090 is really slow, it takes hours. But if I train only 2 layers it is ...

81. [Noobs guide to Flux Kontext LoRA training | by Saquib Alam, MS](https://blog.thefluxtrain.com/noobs-guide-to-flux-kontext-lora-training-7ea8a106d9c2) - This is a live document for all my experiments and results related to Flux Kontext training, coverin...

82. [Consistent Character Creator 3.0 | Consistency Made Simple](https://www.runcomfy.com/comfyui-workflows/consistent-character-creator-3-0) - Consistent Character Creator 3.0 keeps your characters identical across angles, scenes, and styles w...

83. [ToonCrafter: Generative Cartoon Interpolation](http://arxiv.org/pdf/2405.17933.pdf) - We introduce ToonCrafter, a novel approach that transcends traditional
correspondence-based cartoon ...

84. [An AI tool that helps you filling in the animation between keyframes ...](https://www.reddit.com/r/singularity/comments/1d5i0nb/toocrafter_an_ai_tool_that_helps_you_filling_in/) - Because anime sort of already operated with a 'prompting' method, the prompt is the beginning and en...

85. [Ai animation from two frames using toon crafter - YouTube](https://www.youtube.com/watch?v=ymzctSLwKoU) - aianimation #ai #stablediffusion #animation in this video we will be exploring a new tool called too...

86. [Generative AI for Cel-Animation: A Survey](https://ieeexplore.ieee.org/document/11375603/) - Traditional Celluloid (Cel) Animation production pipeline encompasses multiple essential steps, incl...

87. [Generative AI for Cel-Animation: A Survey](https://arxiv.org/html/2501.06250v1) - ...innovative solutions by automating tasks such as inbetween frame
generation, colorization, and st...

88. [EbSynth - Transform videos by changing one frame](https://ebsynth.com) - Change your video by editing one frame · Paint over Videos. Turn your performance into hand‑drawn an...

89. [Optimizing rotoscope animation in the age of artificial intelligence](https://intellectdiscover.com/content/journals/10.1386/ap3_00061_1) - This study examines the use of enhanced trackable markings in semi-automatic animation rotoscoping w...

90. [CACANi: 2D Animation & Inbetween Software](https://cacani.sg) - Use CACANi to accelerate your clean up and inbetween animation creation! 2D characters with rich det...

91. [Toon Boom Animation Launches Beta Program for Ember, its New ...](https://www.toonboom.com/toon-boom-animation-launches-beta-program-for-ember-its-new-suite-of-productivity-tools) - Toon Boom Animation announces the beta program for Ember, a suite of AI-powered tools designed to en...

92. [Netflix is in the generative artificial intelligence animation ...](https://www.instagram.com/reel/DYiK7tQyMdo/) - It's called INKubator. Launched March 2025. No press release, no announcement — just quiet job listi...

93. [GitHub - if-ai/IF-Animation-Workflows: This are a series of ComfyUI workflows that work together to create and repurpose animation](https://github.com/if-ai/IF-Animation-Workflows) - This are a series of ComfyUI workflows that work together to create and repurpose animation - if-ai/...

94. [IF-Animation-Workflows/README.md at main · if-ai/IF-Animation-Workflows](https://github.com/if-ai/IF-Animation-Workflows/blob/main/README.md) - This are a series of ComfyUI workflows that work together to create and repurpose animation - if-ai/...

95. [WAN 2.2 Animate: Character Animation in ComfyUI 2025 | Apatero ...](https://apatero.com/blog/wan-2-2-animate-character-animation-revolution-comfyui-2025) - Learn WAN 2.2 Animate for character animation. Facial expression replication, pose-driven workflows,...

96. [black-forest-labs/FLUX.1-Kontext-dev · VRAM? - Hugging Face](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/discussions/11) - my 5090 with 32gb is not enough without optimizations. it using 31.5gb vram and around 4-5gb RAM. in...

97. [FLUX.2: Frontier Visual Intelligence | Black Forest Labs](https://bfl.ai/blog/flux-2) - FLUX.2 now provides multi-reference support, with the ability to combine up to 10 images into a nove...

98. [FLUX.1 Kontext [dev] Pricing & Providers - Lumenfall](https://lumenfall.ai/models/black-forest-labs/flux.1-kontext-dev/providers) - Compare 3 providers and pricing for FLUX.1 Kontext [dev]. Find the cheapest API provider through Lum...

99. [RTX AI Accelerates FLUX.1 Kontext - NVIDIA Blog](https://blogs.nvidia.com/blog/rtx-ai-garage-flux-kontext-nim-tensorrt/) - FLUX.1 Kontext is an open-weight generative model built for image editing using a guided, step-by-st...

100. [black-forest-labs/flux: Official inference repo for FLUX.1 models](https://github.com/black-forest-labs/flux) - This repo contains minimal inference code to run image generation & editing with our Flux open-weigh...

101. [Edit Images With a Single Phrase! ...](https://seed.bytedance.com/zh/blog/edit-images-with-a-single-phrase-bytedance-announces-image-editing-model-seededit-available-for-test-use) - Edit Images With a Single Phrase! ByteDance Announces Image Editing Model SeedEdit, Available for Te...

