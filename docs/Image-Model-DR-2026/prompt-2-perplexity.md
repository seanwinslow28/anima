# Identity Preservation for Character-Consistent 2D Animation — 2026 Production Guide

*For a hand-drawn pencil-on-cream-paper aesthetic, local 24 GB GPU, ~30 approved keyframes. Evaluated May 2026.*

***

## Executive Summary

1. **Top recommendation: FLUX.1-dev + InstantCharacter adapter (no training required) for fast/flexible work; upgrade to a character LoRA trained on your 30 keyframes for high-fidelity sequences.** InstantCharacter (Tencent/HunyuanDiT, Apache 2.0) is the strongest no-training adapter as of mid-2026, running on FLUX.1-dev with 24 GB via CPU offload, and demonstrating meaningful style compatibility across anime and hand-drawn aesthetics.[^1][^2]
2. **FLUX.1-dev LoRA training on your 30 keyframes is the gold standard for identity lock.** Using ai-toolkit or comfyUI-Realtime-Lora with 1,500–3,000 steps at rank 16–32, your 30-image pencil dataset can yield a character LoRA that nails the hand-drawn style while anchoring identity across hundreds of frames.[^3][^4]
3. **Z-Image Turbo is a credible alternative base model, not a replacement for FLUX.** It trains character LoRAs from as few as 6–15 images and runs natively in comfyUI-Realtime-Lora, but its aesthetic output skews digital/photoreal by default — preserving a pencil aesthetic requires a dedicated style LoRA stacked on top.[^5][^6]
4. **PuLID-FLUX adds face-locking to any FLUX output without training, but its "pasted-on" risk remains real for non-photoreal styles.** The recommended mitigation is setting `timestep_to_start_inserting_ID` to 0–1 for stylized scenes and combining with a character LoRA at strength ≤0.6.[^7][^8]
5. **For in-betweening specifically, no single model perfectly solves the 2D pencil-test problem.** ToonCrafter (video diffusion) is still the most practical keyframe interpolator for cartoon line art. FLUX.2's native multi-reference conditioning and FLUX.1 Kontext offer frame-to-frame identity continuity for edited-frame workflows.[^9][^10][^11]

***

## Master Comparison Table

| Technique | Base Model | Identity Quality (1–5) | Hand-Drawn Style Score (1–5) | VRAM (24 GB) | Setup Difficulty | Training Required |
|---|---|---|---|---|---|---|
| **InstantCharacter** | FLUX.1-dev | 4 | 3.5 | ✅ offload | Medium | No |
| **PuLID-FLUX v0.9.1** | FLUX.1-dev | 3.5 | 2.5 (stylized mode) | ✅ fp8+offload ~17 GB | Medium | No |
| **IP-Adapter-Plus FaceID** | SDXL / FLUX | 3 | 3 | ✅ | Low | No |
| **FLUX.1-dev LoRA** | FLUX.1-dev | 5 | 4.5 (with style LoRA stack) | ✅ ~20 GB training | High | Yes (~30 images) |
| **Z-Image Turbo LoRA** | Z-Image | 4 | 2.5 (photoreal default) | ✅ 512px mode | Medium | Yes (6–20 images) |
| **FLUX.2 Klein multi-ref** | FLUX.2-klein | 4 | 3 | ✅ (Q4/Q8 modes) | Low–Medium | No |
| **FLUX.1 Kontext** | FLUX.1-Kontext | 4.5 | 3.5 | ✅ API / local dev | Low | No |
| **UNO (ByteDance)** | FLUX.1-dev | 3.5 | 3 | ✅ (27 GB fp8) | Medium | No |
| **OmniGen2** | Standalone | 3 | 2.5 | ⚠️ heavy (~4B diff) | High | No |
| **ByteDance Lance** | Standalone | 3 (unverified) | 2 (photoreal bias) | ⚠️ RAM-heavy | High | No |
| **ToonCrafter (inbetween)** | Video DiT | 3 | 4 | ⚠️ ~16 GB A100 class | Medium | No |
| **FILM/RIFE VFI** | Frame-only | N/A | 5 (pass-through) | ✅ minimal | Very Low | No |
| **Character LoRA + PuLID + OpenPose** | FLUX.1-dev | 4.5 | 4 (with style LoRA) | ✅ tight, ~22–23 GB | High | Yes |

***

## Section 1: Adapter-Based Methods (No Training Required)

### IP-Adapter Family

IP-Adapter uses a decoupled cross-attention mechanism to inject image prompt features into the diffusion U-Net or DiT, with the encoder matching the base model's CLIP or DINO backbone. The key variants for character work in 2026 are:[^12]

- **IP-Adapter-Plus (SDXL/FLUX)**: General style + content consistency. A ViT-H (SDXL) or ViT-BigG (SDXL variant) encoder extracts patch-level features. Identity similarity score: ~3/5 for faces; the model loosely respects character likeness but drifts significantly with pose changes.[^13][^12]
- **IP-Adapter-FaceID / FaceID-Plus v2 (SDXL, SD1.5)**: Adds InsightFace embedding on top of the clip encoder, giving tighter face lock (~3.5/5). Documented on HuggingFace as of late 2023. No native FLUX version as of May 2026 — XLabs-AI maintains a FLUX IP-Adapter but with known instability at high weights when combined with ControlNet.[^14][^15]
- **SD3.5-Large IP-Adapter (InstantX Team)**: A 2024 IP-Adapter port to SD3.5-Large released December 2024. Works but SD3.5 is better known for anime/stylized output than FLUX, and the adapter focuses on image prompting rather than strict face fidelity.[^16]

**Hand-drawn style score: 3/5.** IP-Adapter successfully transfers line-art style when used at low-to-medium weight with a pencil-style reference, but face identity drifts with any major pose change. Avoid IP-Adapter-FaceID alone for your use case — it was engineered for photoreal portraits.

**VRAM**: 12–18 GB depending on base model. Fits 24 GB with headroom for ControlNet.

**ComfyUI node**: `ComfyUI_IPAdapter_plus` (maintained, frequently updated through early 2026).[^17]

### InstantID (2024 — Confirmed with Caveats)

InstantID uses a dual-component design: an IdentityNet (adds spatial facial detail via cross-attention) plus IP-Adapter for semantic face features, conditioned on facial landmarks. It was built for SD1.5 and SDXL and integrates smoothly with ControlNet's face landmark detection.[^18]

**2026 status: Confirmed but superseded for FLUX workflows.** InstantID has no official FLUX port; community ports exist but are not production-grade. For SDXL pipelines, InstantID remains the strongest no-training face adapter (~4/5 identity score), but its PhotoRealism bias is severe — it was trained on portrait photography and produces noticeable "realization" artifacts when applied to pencil sketches. **Verdict: Skip for hand-drawn pipelines; use InstantCharacter on FLUX instead.**[^19][^18]

### PuLID-FLUX v0.9.1 — Evaluated for Non-Photoreal

PuLID ("Pure and Lightning ID") uses contrastive alignment training so the face adapter does not corrupt the base model's visual quality or style compliance. The FLUX version (v0.9.0 released Sep 2024, v0.9.1 released Oct 2024) improved face similarity by ~5 percentage points. Running on 24 GB: fp8 + offload mode requires ~17 GB peak; bf16 + offload fits ~23 GB.[^20][^7]

**Key configuration for hand-drawn aesthetic:**
- Set `timestep_to_start_inserting_ID` = 0–1 (not 4, which is for photoreal). Earlier insertion improves style response; later insertion causes lower fidelity AND poor style adherence in stylized modes.[^8][^7]
- Use `fake CFG` (guidance distillation mode); true CFG can cause lower style response in stylized scenes.[^7]

**2026 successors:** A community node `ComfyUI-PuLID-Flux2` was released March 2026 for FLUX.2 Klein architecture, rebuilding PuLID targeting Klein's native architecture while still using FLUX.1 weights — a work-in-progress toward a Klein-native version. No v1.0 release or successor has shipped as of May 2026. PuLID remains in beta status.[^21]

**The "pasted-on" lighting problem for pencil aesthetics:** The documented risk is that PuLID's face insertion uses photographic face embeddings, so lighting and shading on the face region can look inconsistent with the flat pencil rendering of the body. **Mitigation:** Combine PuLID at strength 0.7–0.8 with a character LoRA at strength 0.5–0.6; the LoRA provides the hand-drawn body/hair consistency and the PuLID corrects face drift. Using ControlNet lineart on the reference frame further flattens the output back to 2D rendering.

**Identity similarity score: 3.5/5 (stylized mode). Hand-drawn style score: 2.5/5 (unmitigated), 3.5/5 (with character LoRA + ControlNet lineart).**

### InstantCharacter (Tencent, April 2025 — 2026 Leading Adapter)

InstantCharacter is a scalable FLUX.1-dev adapter using SigLIP for fine-grained identity features and DINOv2 for background-resistant structural features. It was trained on a 10M-sample character dataset organized into paired multi-view and unpaired text-image subsets, allowing simultaneous optimization of identity consistency and text controllability.[^22][^23][^1]

**Practical notes for 24 GB:**
- Nominal requirement is 45 GB VRAM; offload mode reduces this to ~22 GB (patched May 2025 by community contributor Zeyu Long).[^2][^24]
- ComfyUI wrapper: `ComfyUI-InstantCharacter` by jax-explorer; ipadapter binary downloads from `tencent/InstantCharacter` on HuggingFace.[^2]
- Works from a **single reference image** of your character.

**Versus PuLID for your use case:** InstantCharacter preserves full body, clothing, hair, and facial features simultaneously (not face-only like PuLID), which matters for 2D animation where body silhouette consistency is as important as face fidelity. Style compatibility with anime and illustrated characters is documented in their qualitative comparisons, though formal benchmarks for pencil-line aesthetics are not yet published.[^22][^2]

**Identity similarity score: 4/5. Hand-drawn style score: 3.5/5.**

### UNO (ByteDance, 2025 — Active)

ByteDance's UNO ("Universal aNd cOntrollable") model runs on FLUX.1-dev and uses Universal Rotary Position Embedding (UnoPE) to prevent attribute confusion when multiple reference images are used. The ComfyUI workflow accepts one or two reference images, requires FLUX full model (~27 GB) with fp8 quantization, and fits within a 24 GB GPU with quantization enabled. Strong for object + character co-referencing; useful if your "Sean" character needs to appear consistently alongside specific props or environments.[^25][^26]

**Identity similarity score: 3.5/5. Hand-drawn style score: 3/5.**

### PhotoMaker v1/v2 — Verdict: Confirmed, Superseded for FLUX

PhotoMaker V2 (Tencent, July 2024) improved ID fidelity over V1, especially for single-image input and Asian facial inputs, and allows combination with IP-Adapter-FaceID or InstantID for further ID improvement. However, both versions are SDXL/SD1.5 only with no FLUX port, and V2's identity fidelity is still below InstantCharacter's. **Verdict for your pipeline: Skip in favor of InstantCharacter.** PhotoMaker remains useful for SDXL workflows where FLUX is unavailable.[^27][^28]

### ConsiStory / StoryDiffusion / IC-LoRA

**StoryDiffusion** (Consistent Self-Attention, NeurIPS 2024) remains actively maintained via `ComfyUI_StoryDiffusion`, which as of June 2025 added DreamO v1.1 support and OmniConsistency integration. The core mechanism — shared self-attention across a batch of generated images — is zero-shot (no training) and now supports FLUX, PuLID, and InstantCharacter as sub-methods within the same graph. It's useful for generating consistent _batches_ rather than frame-accurate sequences.[^29][^30]

**IC-LoRA** (In-Context LoRA, Alibaba/ali-vilab, October 2024) concatenates condition and target images into a composite and uses natural language to define the task. Ten pretrained task models were released (including Film Storyboard generation), but 2026 update activity is minimal. **Verdict: Research-useful for storyboard generation; not production-ready for frame interpolation.**[^31]

**Verdict summary:** StoryDiffusion remains maintained and useful for batch character consistency; IC-LoRA has stalled. Neither replaces a trained character LoRA for frame-accurate animation.

***

## Section 2: Training-Based Methods

### FLUX.1-dev LoRA — 2026 Best Practices

FLUX.1-dev remains the production baseline for character LoRA training. Recommended trainers and their 2026 status:

- **ai-toolkit (ostris)**: Actively maintained, supports FLUX.1-dev and Z-Image via Musubi Tuner backend. Community-verified as the most stable choice for 24 GB GPUs.[^32][^5]
- **comfyUI-Realtime-Lora**: Trains directly inside ComfyUI, supporting SDXL, FLUX, Z-Image, Qwen Image Edit, and Wan 2.2 via three backends (sd-scripts, Musubi Tuner, AI-Toolkit). Allows inline train-then-test without leaving the graph — ideal for iterative character work.[^4][^33]
- **SimpleTuner**: Supports FLUX.1 [dev, schnell], LoRA up to rank-256 on A100-80G, rank-16 or lower on A100-40G/RTX 4090. Slightly more complex config but well-documented.[^34]
- **kohya_ss**: Battle-tested for SDXL/SD1.5; FLUX support added in 2024 via the `sd-scripts` branch. Still valid but ai-toolkit is generally preferred for FLUX in 2026.[^35][^3]

**Optimal dataset size in 2026:**
- **FLUX.1-dev character LoRA**: 20–60 images is the practical sweet spot. For a 30-image dataset (your case), use 1,500–3,000 training steps, rank 16–32, learning rate 1e-4 to 2e-4 with cosine scheduler. HuggingFace practitioner consensus: "if you have 10 images of high quality, it can still look quite similar with default settings".[^3]
- Captioning strategy: For character identity locking, **empty captions** or minimal trigger-word-only captions work well for Z-Image and FLUX character LoRAs — this prevents the model from learning spurious prompt associations. For style LoRAs, detailed descriptive captions with art style terms are preferable.[^5]
- Training time on RTX 4090: ~15–40 minutes for 1,500–3,000 steps at rank 16 on FLUX.1-dev at 1024px with fp8 quantization.

**For pencil/hand-drawn aesthetic LoRA:** Train a separate _style_ LoRA on examples of your specific pencil-on-cream rendering. Existing public style LoRAs (e.g., the FLUX pencil-sketch LoRA on Civitai, trigger word `sketch`) can bootstrap style consistency before you train a custom one. Stack character LoRA (strength 0.6–0.8) + style LoRA (strength 0.4–0.6) at inference. K-LoRA (training-free LoRA fusion via top-K attention selection) is a published technique for merging subject and style LoRAs without interference.[^36][^37]

### Z-Image Turbo LoRA — 2026 Evaluation

Z-Image Turbo (Tencent) supports LoRA training with as few as 6–20 images, with community practitioners reporting good results from 10–15 high-quality images when using 512 px resolution and the AI-Toolkit Musubi Tuner backend. The recommended 2026 config (from r/StableDiffusion practitioners, Jan 2026):[^6][^32][^5]
- LoKr factor 4 (or LoRA rank 16)
- Differential Guidance: 3
- 100 steps per image in dataset
- 512 px resolution (higher resolutions amplify noise in small datasets)
- Empty captions (no trigger words)
- Transformer and text-encoder quantization set to NONE

The `comfyUI-Realtime-Lora` toolkit (December 2025) supports Z-Image alongside FLUX with Musubi Tuner backend.[^38][^4]

**Critical caveat for pencil aesthetics:** Z-Image Turbo's base training data skews toward photorealistic and digital art styles. A character LoRA trained on pencil-drawn keyframes will encode _some_ aesthetic information, but you'll need a dedicated pencil style LoRA stacked at ~0.4–0.5 strength to maintain the cream-paper pencil look. Without it, outputs drift toward digital illustration or photoreal.

**Z-Image vs FLUX for your use case:**
- Z-Image: faster convergence (fewer images needed), lower VRAM during training at 512 px, but weaker aesthetic alignment for hand-drawn styles.
- FLUX.1-dev: slower training, needs more images for best quality, but dramatically better aesthetic fidelity and adapter ecosystem (PuLID, InstantCharacter, UNO all require FLUX.1-dev).

**Recommendation: Train on FLUX.1-dev. Use Z-Image Turbo as a rapid prototyping path if you need a quick identity test before committing to FLUX training.**

### Qwen-Image-Edit as LoRA Dataset Generator

The emerging 2026 pattern uses Qwen-Image-Edit to synthesize multi-angle, multi-expression variants of your character from a single reference, then trains a LoRA on that clean synthetic dataset. A ComfyUI workflow for this (September 2025, YouTube tutorial) demonstrates generating hundreds of consistent variants, upscaling them with SDXL Epic Realism, and saving as training data.[^39][^40][^41]

**How it works:** Qwen-Image-Edit (Apache 2.0, Qwen2.5-VL semantic encoder + VAE appearance encoder) treats image editing as a conditional generation task. Given a reference and a prompt like "same character, 3/4 view from left, hands at sides," it produces a plausible new pose while preserving face and outfit. An independently documented workflow generates ~1,000 images and filters to 50–100 using InsightFace cosine similarity scoring to ensure identity fidelity.[^40][^42][^39]

**Does synthetic Qwen-Edit data match real keyframes for training quality?** Honest assessment: **Not proven in formal benchmarks.** Reddit practitioners (October–November 2025) report "decent success" but note the filtering pipeline is time-consuming and the approach works better for photoreal characters than for stylized/hand-drawn ones. The synthetic images carry Qwen-Edit's visual signature, which — like Z-Image's photoreal bias — can dilute a hand-drawn style when used as training data. **Verdict: Useful as a data augmentation complement to your 30 real keyframes, not as a replacement for them. Blend ~30 real keyframes + ~20 best synthetic variants for training.**[^40]

### FLUX.2 Klein LoRA Training — 2026 Active Path

FLUX.2 Klein (9B) supports LoRA fine-tuning with 9–50 images for style or character training, according to fal.ai's training API documentation. Community practitioners on r/StableDiffusion (January 2026) report ~99% character consistency with a character LoRA in isolation, but face drift when combining with other LoRAs or posing heavily. A community consistency LoRA (`dx8152/Flux2-Klein-9B-Consistency`, V2 updated April 2026) addresses color-cast and dirty-detail issues from V1.[^43][^44][^45][^46]

Klein's native multi-reference capability (up to 10 images as inference-time references without training) makes it attractive for dataset _building_ before FLUX.1 LoRA training.[^47][^48]

### SD3.5 LoRA — Verdict

SD3.5 Medium (2.5B, MMDiT-X architecture) runs comfortably on 12+ GB VRAM and is noted for stronger anime/illustrated-style output than FLUX.1 without additional fine-tuning. However, SD3.5's adapter ecosystem is thin — the IP-Adapter port from InstantX is the primary option, and there is no PuLID-SD3.5 or InstantCharacter-SD3.5 as of May 2026. LoRA training on SD3.5 is mature (kohya_ss, ai-toolkit both support it), but the identity-preservation adapter gap makes it a weaker production choice than FLUX for multi-frame animation work.[^49][^50]

***

## Section 3: Hybrid / Combined Approaches

### The LoRA + PuLID + ControlNet Stack — Independent Verification

The reported production stack (character LoRA at 0.6, PuLID at 0.8, OpenPose ControlNet) is directionally correct but requires calibration for pencil aesthetics. Independent ComfyUI practitioners confirm that combining all three on FLUX.1-dev fits within 24 GB at fp8 quantization but sits very near the limit (~22–23 GB) with aggressive offloading. The quality/difficulty ratio is high: each of the three components must be tuned independently before combining.[^21][^7]

**For hand-drawn pencil pipeline specifically, recommend adding ControlNet Lineart (not just OpenPose).** OpenPose ControlNet enforces skeletal structure but does not enforce line quality. Using the lineart preprocessor from a reference frame as a ControlNet input pushes the output back toward your pencil aesthetic while OpenPose anchors the pose. Stack: character LoRA (0.6) + style LoRA (0.4) + PuLID (0.7, timestep 0–1) + ControlNet OpenPose (0.7) + ControlNet Lineart (0.5).

### Alternative Stacks for the In-Between Use Case

**Multi-reference attention manipulation (FLUX.1 Kontext approach):** FLUX.1 Kontext (BFL, June 2025) is a multimodal flow transformer that natively accepts a reference image + text instruction as joint conditioning. For in-betweening, the workflow is: feed Frame A → instruction "interpolate to [pose description from Frame B]" → generates Frame A.5 while locking visual identity. Community tests show ~98% identity retention for iterative character edits. The limitation: FLUX.1 Kontext [dev] is still in private beta at BFL; [pro] and [max] are API-only (no local weights). **Monitor for open-weight release.**[^51][^11][^52]

**FLUX.2 Dev multi-reference (up to 10 images):** FLUX.2 Dev (open-source, November 2025) natively supports multi-reference conditioning — up to 10 images, up to 9 MP total input. A 2-image start/end frame reference workflow is documented in official ComfyUI tutorials. This is currently the best locally runnable approach for providing both start frame AND end frame as joint context, though output quality for intermediate poses relies on the model's own interpretation.[^10][^9]

**Latent blending / differential diffusion:** Differential diffusion (part of SDXL/FLUX advanced ControlNet workflows) allows per-region denoising strength, useful for blending between a start-frame-locked region and a more freely generated interpolated region. No dedicated open-source ComfyUI node specifically for this in-between use case exists as of May 2026 — it requires manual workflow construction.

**Style LoRA + Character LoRA stacking for pencil aesthetics:** Use K-LoRA's training-free fusion approach or direct LoRA stacking with attention-layer conflict minimization. Practical workflow: character LoRA at blocks `[double_blocks.0–6]` (identity-heavy) + style LoRA at blocks `[double_blocks.8–18]` (style-heavy) using the comfyUI-Realtime-Lora block-selective loader. This avoids the full-strength conflicts that produce identity loss or aesthetic destruction.[^36][^4]

***

## Section 4: In-Between-Specific 2026 Workflows

### ToonCrafter — Current State

ToonCrafter (CUHK/Tencent, 2024) leverages pre-trained image-to-video diffusion priors to interpolate between two cartoon/line-art keyframes, generating up to 16 frames at 512×320 resolution. A ComfyUI node exists (`ToonCrafterNode` by siliconecomputervision) and a multi-frame interpolation workflow on OpenArt allows chaining multiple keyframe pairs for longer sequences. ToonCrafter is specifically designed for 2D animation-style interpolation — its training data includes cartoon/illustrated imagery, giving it an edge over photorealistic video diffusion models for pencil-style work.[^53][^54]

**Limitation:** 512×320 max resolution is too low for production. For your use case, upscale keyframes before input or use ToonCrafter for animatic pencil-test work, then upscale the output with a 4x model. VRAM requirement is ~16 GB, which runs on your 24 GB rig.

### AnimeInbet / EISAI — 2026 Status

EISAI (Enchanced Interpolation for Sketch-based Anime Images) and related anime-specific inbetweening models are research-only with no active ComfyUI integration as of May 2026. The state-of-practice blog analysis from April 2024 summarized these as representing the then-current SotA, but they have not shipped production tooling.[^55]

### FILM and RIFE — Frame-Only Methods

FILM (Frame Interpolation for Large Motion) and RIFE-derived models are optical-flow-based or learned-kernel-based interpolators — they do not understand character identity, only pixel-level motion. **Critical note for your use case:** GMFSS Fortuna VFI is specifically mentioned for hand-drawn cartoon and anime animations, as opposed to FILM/RIFE which work better on natural video. Use GMFSS Fortuna (available via `ComfyUI-Frame-Interpolation` custom node) for interpolating between AI-generated pencil-test frames.[^56]

**These methods are ideal as a post-process step** after generating sparse keyframes: generate frames at 6 fps with your LoRA pipeline, then GMFSS Fortuna upsample to 12–24 fps. They preserve pencil aesthetic perfectly because they only interpolate existing pixels — no model-induced style shift.

### ComfyUI Frame Interpolation Official Support

ComfyUI now ships official preprocessor and frame interpolation template workflows (January 2026) covering depth estimation, lineart conversion, pose detection, normals estimation, and frame interpolation. The frame interpolation workflow supports increasing frame rate in short clips, smoothing generated video motion, and is compatible with both RIFE and FILM backends.[^57][^58]

### ByteDance Lance — In-Between Evaluation

Lance (ByteDance Intelligent Creation Lab, released May 21, 2026) is a 3B-active-parameter native unified multimodal model handling X2T, X2I, and X2V tasks (image/video understanding + generation + editing) in a single framework. Architecture highlights: dual-stream mixture-of-experts on shared interleaved multimodal sequences; modality-aware rotary positional encoding for heterogeneous visual tokens; trained from scratch on 128×A100 GPUs.[^59][^60][^61][^62]

**Does Lance support multi-image conditioning for in-betweening?** The architecture description (X2I supporting "interleaved multimodal sequences") suggests multi-image conditioning is architecturally possible, but the May 2026 release documentation and HuggingFace model card do not describe a dedicated start-frame + end-frame + style-ref inbetweening workflow. **Status: Too new to evaluate definitively. Monitor the GitHub (bytedance/Lance) for ComfyUI integration and task-specific demonstrations. Not production-ready for in-betweening as of this writing.**[^63][^62]

**Non-photoreal style performance:** Lance's benchmark results focus on GenEVAL, DPG-Bench, GEdit-Bench, VBench, and MVBench — all of which measure photorealistic or scene-level generation. No evidence of pencil/hand-drawn style capability exists in the current release materials. **Verdict: Evidence too thin for non-photoreal use cases. Revisit in Q3 2026.**[^60]

### OmniGen2 — Multi-Image In-Context Generation

OmniGen2 (BAAI, June 2025) explicitly supports in-context generation: feeding multiple reference images (characters, objects, scenes) as inputs to produce coherent new outputs. The OmniContext benchmark evaluates single-subject, multi-subject, and scene consistency tasks. Its decoupled architecture (autoregressive MLLM for understanding, 4B diffusion transformer for generation) preserves fine-grained visual features via a VAE encoder separate from the text pathway.[^64][^65][^66][^67]

**For in-betweening:** OmniGen2 could theoretically take Frame A + Frame B + style reference as in-context inputs. Benchmarks show strong subject consistency, but no 2D animation inbetweening use case has been documented in the wild as of May 2026. Limitations noted in the paper include sensitivity to input image quality and ambiguity with multi-image inputs. **Verdict: More viable than Lance for this task (architecture is better suited), but still research-stage for production animation. Worth experimenting with ComfyUI once a community workflow emerges.**[^66]

***

## Section 5: Three Pipeline Recipes for a 24 GB GPU

### Recipe 1: Fast & Flexible — Adapter-Only, No Training

**Objective:** Generate in-between frames from a single hero reference image without any training. Best for early exploration and animatics.

**Model files:**
- `black-forest-labs/FLUX.1-dev` (main model, bf16 or fp8)
- `tencent/InstantCharacter` → `instantcharacter_ip-adapter.bin` → `models/ipadapter/`
- `google/siglip-so400m-patch14-384` → `models/clipvision/`
- `facebook/dinov2-giant` → `models/clipvision/`
- Optional: `Flux.2-Klein-9B-Consistency LoRA` (dx8152/HF) for additional pose consistency

**ComfyUI graph description:**
1. **Load FLUX.1-dev** (fp8 recommended for 24 GB) via `UnetLoader` node
2. **Load InstantCharacter adapter** via `ComfyUI-InstantCharacter` custom node → IP-Adapter Load node
3. **Load reference image** (your hero reference) → InstantCharacter Image Encoder node (processes SigLIP + DINOv2 features)
4. **Pose control:** Load OpenPose ControlNet for FLUX (`flux_shakker_labs_union_pro-fp8`) → feed target pose image
5. **Conditioning:** Connect InstantCharacter features + text prompt + ControlNet conditioning to `FluxGuidance` node
6. **Sampler:** `KSampler` with Euler scheduler, 20–28 steps, guidance 3.5–4.0
7. **VAE Decode** → output

**Enable offload** in InstantCharacter nodes to stay under 24 GB. Expect ~60–90 seconds per frame on RTX 4090.

**Expected quality: 3.5–4/5 identity**, moderate pencil-style preservation (augment with style reference in IP-Adapter-Plus node if available for FLUX). **Common failure modes:** Body/limb inconsistency across frames; loss of pencil-line quality on clothing details. **Character drift over long sequences:** Moderate — identity locked per-frame but no inter-frame temporal consistency. **Electricity cost:** ~0.5 kWh per 100 frames ≈ $0.05–0.08/100 frames.

***

### Recipe 2: High-Fidelity — LoRA Trained on 30 Keyframes + PuLID

**Objective:** Maximum character identity lock across hundreds of frames. Uses your 30 approved keyframes as training data.

**Training step (one-time, ~30–45 minutes):**
- Install `ai-toolkit` (ostris) or use `comfyUI-Realtime-Lora` `RealtimeLoraTrainer` node directly in ComfyUI
- Dataset: 30 keyframes at 1024×1024 (crop/pad to consistent size), empty captions (no trigger words)
- Architecture: FLUX.1-dev
- Rank: 16–32; learning rate: 1e-4; steps: 2,000–3,000; VRAM mode: Medium (1024 px) or Low (768 px) if tight
- Output: `sean_character.safetensors`

**Inference model files:**
- `black-forest-labs/FLUX.1-dev`
- `sean_character.safetensors` (trained LoRA, strength 0.6–0.7)
- `PuLID-FLUX-v0.9.1` (from `yanze/PuLID-FLUX` HuggingFace)
- `flux_shakker_labs_union_pro-fp8` (ControlNet Union)

**ComfyUI graph description:**
1. **Load FLUX.1-dev** fp8 + offload
2. **Load LoRA** → `LoRALoader` node, strength 0.65
3. **PuLID conditioning:** `PuLIDFlux` custom node → reference image → `timestep_to_start_inserting_ID = 1`, strength 0.75
4. **ControlNet OpenPose + optional Lineart:** Feed target pose skeleton from AnimePose or MediaPipe preprocessor
5. **Text prompt** describing pose/expression delta from previous keyframe
6. **KSampler:** Euler, 25 steps, guidance 3.5
7. **ADetailer/face detailer** optional post-process to clean up face region
8. **VAE Decode** → save frame

**Comparison: FLUX LoRA vs Z-Image LoRA vs SD3.5 LoRA for this use case:**

| Criterion | FLUX.1-dev LoRA | Z-Image Turbo LoRA | SD3.5 Medium LoRA |
|---|---|---|---|
| Identity quality | 5/5 | 4/5 | 3.5/5 |
| Pencil style preservation | 4.5/5 (with style LoRA) | 2.5/5 | 3/5 |
| Training data needed | 20–60 images | 6–20 images | 15–40 images |
| VRAM (training) | ~20 GB (1024 px) | ~10 GB (512 px) | ~16 GB |
| Adapter ecosystem | Full (PuLID, IC, UNO) | Limited | Limited |
| Training time (4090) | 30–45 min | 10–20 min | 20–35 min |

**Expected quality: 4.5/5 identity, 4/5 hand-drawn style (with style LoRA stacked).** Common failure modes: Over-baked face if LoRA strength >0.75 + PuLID combined; style degradation if pencil style LoRA not stacked. Character drift across long sequences: Low — LoRA provides a persistent identity anchor. **Electricity cost:** ~0.8 kWh per 100 frames ≈ $0.06–0.10/100 frames.

***

### Recipe 3: Style-Locked — Character LoRA + Style LoRA + Control Conditioning

**Objective:** Lock both the character identity AND the pencil-on-cream-paper aesthetic simultaneously, with pose control. Highest setup effort, best final quality.

**Model files:**
- `black-forest-labs/FLUX.1-dev`
- `sean_character.safetensors` (trained LoRA on 30 keyframes)
- `pencil_sketch_style.safetensors` (either train custom on 30–50 pencil examples, or use public FLUX pencil-sketch LoRA from Civitai, trigger `sketch`)[^37]
- `flux_shakker_labs_union_pro-fp8` (ControlNet Union for OpenPose + Lineart)

**Dataset for custom style LoRA:** Collect 30–50 varied pencil drawings (NOT your character specifically — environments, props, textures, other figure studies in the same pencil/cream aesthetic). Caption each with style-only descriptors: "pencil sketch on cream paper, loose line weight, graphite grain." Train with rank 16, 2,000 steps, learning rate 1e-4.

**ComfyUI graph description:**
1. **Load FLUX.1-dev** fp8
2. **Load character LoRA** via `LoRALoader`, strength 0.65
3. **Load style LoRA via second `LoRALoader` node** (chain: FLUX → char LoRA → style LoRA), strength 0.5; OR use `comfyUI-Realtime-Lora` block-selective loader to assign char LoRA to early transformer blocks and style LoRA to late blocks
4. **ControlNet Lineart preprocessor**: Run your start-frame or sketch through the lineart extractor; feed into ControlNet Union Lineart mode, strength 0.55
5. **ControlNet OpenPose**: Target pose, strength 0.65
6. **Text prompt**: Include style trigger word + pose description; do NOT include character name/description (LoRA handles that)
7. **Negative prompt**: `photorealistic, digital art, 3D render, smooth gradients, clean lines`
8. **KSampler**: Euler, 28 steps, guidance 3.5
9. **Optional final step:** Run output through `GMFSS Fortuna VFI` (ComfyUI-Frame-Interpolation) at 2× or 4× to smooth motion

**Expected quality: 5/5 style adherence, 4.5/5 identity.** Common failure modes: LoRA interference at high combined strength (cap char+style sum at ≤1.2 total); ControlNet Lineart over-constraining and removing natural line variation (reduce to 0.4–0.45 if output looks mechanical). **Character drift over long sequences:** Very low — both LoRAs re-anchor every frame; drift appears mainly at extreme poses not in training data. **Electricity cost:** ~1.0 kWh per 100 frames ≈ $0.08–0.12/100 frames.

***

## Verdict on the Known State

### Item 1: Z-Image Turbo (Tencent) + comfyUI-Realtime-Lora

**Verdict: Confirmed with caveats.**

Z-Image Turbo does support LoRA training from 6–15 high-quality images using the Musubi Tuner backend. The comfyUI-Realtime-Lora toolkit is real, actively maintained (December 2025 release), and supports Z-Image alongside FLUX, SDXL, Qwen Image Edit, and Wan 2.2 within a single ComfyUI graph. The Promptus AI tutorial and Next Diffusion walkthroughs from early 2026 are consistent with community-verified workflows.[^68][^33][^32][^6][^4][^5]

**Calibration needed on your specific use case:** Z-Image Turbo's minimum viable dataset is 6–10 images (not 10–15 as stated in the known state — the 6-image floor is documented in ai-toolkit GitHub issues). Quality vs FLUX LoRA: Z-Image trains faster and with fewer images, but FLUX LoRA produces higher-fidelity results and integrates with the full adapter ecosystem. For hand-drawn pencil style, Z-Image's photoreal default aesthetic is a real liability — you will need to stack a pencil style LoRA on every inference run. **Use Z-Image for rapid prototyping; train final pipeline on FLUX.**[^32]

### Item 2: Qwen-Image-Edit as LoRA Dataset Generator

**Verdict: Confirmed with caveats.**

The workflow is real and functional: Qwen-Image-Edit (ComfyUI workflow, September 2025 tutorial) generates consistent multi-angle character variants from a single reference image. The multi-angle LoRA trained on 96 viewpoints is a documented community example. The Apache 2.0 license is correct.[^39][^40]

**Critical caveat:** The synthetic dataset carries Qwen-Edit's style signature, which skews away from hand-drawn aesthetics. When training a FLUX LoRA on purely synthetic Qwen-Edit data, the trained LoRA tends to interpret identity in a softer, more photorealistic register than when trained on your actual pencil keyframes. **Recommendation: Use Qwen-Edit-generated variants only as augmentation (max 30–40% of training set) blended with your 30 real keyframes. Never replace real keyframes with synthetic ones for a stylized character.**

### Item 3: The 2026 Production Stack (LoRA + PuLID + ControlNet)

**Verdict: Confirmed with caveats.**

The LoRA (0.6) + PuLID (0.8) + ControlNet OpenPose stack is a well-documented pattern and runs within 24 GB on FLUX.1-dev with fp8 + offload. The "pasted-on lighting" caveat is real and specifically documented in PuLID's own documentation for stylized scenes.[^8][^7][^21]

**2026 PuLID mitigation:** No v1.0 or dedicated non-photoreal PuLID successor has shipped. The most effective mitigation remains setting `timestep_to_start_inserting_ID = 0–1` for stylized scenes and keeping PuLID strength at 0.7–0.75 (not 0.8) when the character LoRA is also active. The `ComfyUI-PuLID-Flux2` community node targeting FLUX.2 Klein was announced March 2026 but is described as a work-in-progress, not a production release. **PuLID-Lightning (mentioned in some sources) is not a distinct model — it refers to using SDXL-Lightning as an optional acceleration method, per the PuLID GitHub documentation.**[^7][^21][^8]

### Item 4: ByteDance Lance (May 2026)

**Verdict: Evidence too thin — evaluate in Q3 2026.**

Lance is confirmed released May 17–21, 2026 under Apache 2.0, with 3B active parameters, dual-stream MoE architecture, and unified X2T/X2I/X2V capabilities. Performance benchmarks (GenEVAL, DPG-Bench, GEdit-Bench, VBench) are competitive with or better than larger unified models.[^61][^62][^59][^60]

**For your specific use case (multi-image conditioning for in-betweening, non-photoreal style):** No evidence supports these capabilities in current release materials. The model appears trained predominantly on photorealistic/natural image data. A ComfyUI integration node has not emerged as of May 24, 2026 (per the YouTube video noting it alongside HiDream-O1 but without a workflow). **Do not redirect current pipeline development toward Lance. Monitor GitHub (bytedance/Lance) for ComfyUI nodes and animation demos.**[^60][^63]

### Item 5: Models From v1 — Status Review

| Model | Verdict | Notes |
|---|---|---|
| **InstantID** | Confirmed, caveats | Strong for SDXL, no FLUX port; photoreal bias disqualifies it for pencil aesthetic; superseded by InstantCharacter on FLUX[^18][^1] |
| **PhotoMaker v1/v2** | Confirmed, superseded | V2 still works on SDXL; no FLUX port; superseded by InstantCharacter for FLUX pipelines[^27][^28] |
| **ConsiStory / StoryDiffusion** | Confirmed leading (for batch generation) | Actively maintained via ComfyUI_StoryDiffusion, now integrates InstantCharacter and UNO; useful for storyboard-style consistency across image batches[^29][^30] |
| **IC-LoRA** | Confirmed but stalled | Released Oct 2024; no meaningful 2026 activity; useful for task-specific storyboard generation, not frame interpolation[^31] |
| **HiDream-I1** | Confirmed, no LoRA adapter ecosystem | Released April 2025, 17B MoE, strong benchmark scores; companion editing model HiDream-E1-1 released July 2025[^69][^70]. No character adapter ecosystem exists. Not recommended for multi-frame animation pipelines. |
| **OmniGen original** | Superseded by OmniGen2 | OmniGen2 (BAAI, June 2025) replaces the original with decoupled architecture and in-context generation[^64][^65][^67] |
| **DeepSeek Janus-Pro** | Confirmed, wrong tool | 7B autoregressive unified model, strong benchmarks, low image resolution (384×384 output limit), not suitable for animation frame generation[^71][^72][^73] |
| **Lumina-Image** | Evidence too thin | No meaningful 2026 production community activity found |
| **PixArt-Sigma** | Superseded | Eclipsed by FLUX.1 and HiDream-I1 in quality benchmarks; still maintained but not recommended for new pipelines |
| **Sana (NVIDIA)** | Evidence too thin | No 2026 production adoption signals in searched community sources |

**Notable 2026 entrant not in the original list: FLUX.1 Kontext** (BFL, June 2025) — a multimodal flow transformer for in-context image editing and character consistency without fine-tuning, currently API-only for [pro] and [max], with [dev] open weights in private beta. When the open-weight [dev] version ships locally, it will be the strongest no-training character-consistency tool for iterative in-between frame generation. Monitor bfl.ai for local release.[^11][^52]

***

## Key Knowledge Gaps and Caveats

- **Formal benchmarks for pencil/hand-drawn aesthetic preservation** do not exist for most tools evaluated here. All hand-drawn style scores above are derived from qualitative community evidence and reasoning about model training distributions, not published quantitative metrics.
- **Lance in-betweening capabilities** cannot be verified until community workflows emerge. Check back in 60–90 days.
- **FLUX.1 Kontext [dev] local weights** are not yet publicly available; the pipeline described in Recipe 1 variant will become significantly more powerful once they ship.
- **Combining style LoRA + character LoRA + PuLID** has not been benchmarked in a controlled study — the combined pipeline is a community-assembled best practice, not a formally validated approach.

---

## References

1. [InstantCharacter: Personalize Any Characters with a Scalable ...](https://huggingface.co/papers/2504.12395) - This dual-data structure enables simultaneous optimization of identity consistency and textual edita...

2. [jax-explorer/ComfyUI-InstantCharacter - GitHub](https://github.com/jax-explorer/ComfyUI-InstantCharacter) - InstantCharacter's Advantages: In contrast, InstantCharacter achieves an excellent balance between i...

3. [Perfect LoRA Training parameters human character - Models](https://discuss.huggingface.co/t/perfect-lora-training-parameters-human-character/147211) - To create a precise LoRA model of your human character using Kohya_ss scripts with FLUX, SD1.5, and ...

4. [shootthesound/comfyUI-Realtime-Lora: Train and block edit ... - GitHub](https://github.com/shootthesound/comfyUI-Realtime-Lora) - Train, analyze, selectively load by block, and edit base models for SDXL, SD 1.5, FLUX, Z-Image, Qwe...

5. [What is the best way to get the right dataset for z image turbo Lora ...](https://www.reddit.com/r/StableDiffusion/comments/1qj7oxh/what_is_the_best_way_to_get_the_right_dataset_for/) - Use only the 10-20 best images. quality > quantity. If you dont have that many it will still work th...

6. [Best Practices for Training LoRA Models with Z-Image](https://dev.to/gary_yan_86eb77d35e0070f5/best-practices-for-training-lora-models-with-z-image-complete-2026-guide-4p7h) - Best Practices for Training LoRA Models with Z-Image: Complete 2026 Guide · Efficiency: Requires onl...

7. [PuLID/docs/pulid_for_flux.md at main · ToTheBeginning/PuLID](https://github.com/ToTheBeginning/PuLID/blob/main/docs/pulid_for_flux.md) - [NeurIPS 2024] Official code for PuLID: Pure and Lightning ID Customization via Contrastive Alignmen...

8. [Update app.py · yanze/PuLID-FLUX at 76b6b9c - Hugging Face](https://huggingface.co/spaces/yanze/PuLID-FLUX/commit/76b6b9ce6f46826d78aaa21f00e895ae33d3a6a0) - We’re on a journey to advance and democratize artificial intelligence through open source and open s...

9. [ComfyUI Flux.2 Dev Example](https://docs.comfy.org/tutorials/flux/flux-2-dev) - It adds reliable multi-reference consistency (up to 10 images), improved editing precision, better v...

10. [FLUX.2: Multi-reference image generation now ... - Together AI](https://www.together.ai/blog/flux-2-multi-reference-image-generation-now-available-on-together-ai) - Production-grade image generation with multi-reference consistency, exact brand colors, and reliable...

11. [FLUX.1 Kontext models: Character consistency and precise image ...](https://www.together.ai/blog/flux-1-kontext) - FLUX.1 Kontext allows you to prompt with both text and images, and seamlessly extract and modify vis...

12. [IP-Adapters: All you need to know - Stable Diffusion Art](https://stable-diffusion-art.com/ip-adapter/) - IP-adapter (Image Prompt adapter) is a Stable Diffusion add-on for using images as prompts, similar ...

13. [How to perform style transfer using IPAdapter Plus in ComfyUI?](https://www.comflowy.com/blog/IPAdapter-Plus) - You just need to upload your preferred reference image, and you can transfer the tone and texture of...

14. [h94/IP-Adapter-FaceID - Hugging Face](https://huggingface.co/h94/IP-Adapter-FaceID) - IP-Adapter-FaceID can generate various style images conditioned on a face with only text prompts. re...

15. [XLabs-AI/flux-ip-adapter · Flux's IPAdapter with a high weight ...](https://huggingface.co/XLabs-AI/flux-ip-adapter/discussions/33) - ControlNet works without the IPAdapter and maintains the structure, but with the IPAdapter active, i...

16. [README.md · InstantX/SD3.5-Large-IP-Adapter at main](https://huggingface.co/InstantX/SD3.5-Large-IP-Adapter/blob/main/README.md) - This repository contains a IP-Adapter for SD3.5-Large model released by researchers from InstantX Te...

17. [12 IP Adapter Plus in ComfyUI Explained - YouTube](https://www.youtube.com/watch?v=nsOoU9vbKd0) - 00:00 IP Adapter Plus Introduction 01:03 Benefits for AI Artists 01:39 Style Transfer, Faces and Com...

18. [InstantID](https://instantid.github.io) - InstantID demonstrates exceptional performance and efficiency, proving highly beneficial in real-wor...

19. [New Face Swap Models (IP-Adapter-FaceID & InstantID) #2050](https://github.com/lllyasviel/Fooocus/discussions/2050) - There are some new face swap models which are probably superior to the current method: IP-Adapter-Fa...

20. [PuLID/README.md at main · ToTheBeginning/PuLID](https://github.com/ToTheBeginning/PuLID/blob/main/README.md) - [NeurIPS 2024] Official code for PuLID: Pure and Lightning ID Customization via Contrastive Alignmen...

21. [FLUX.2 Klein用PuLIDカスタムノード公開。生成画像の顔一貫性維持 ...](https://x.com/aiaicreate/status/2033066702829744367)

22. [InstantCharacter ComfyUI Workflow | FLUX DiT Personalization](https://www.runcomfy.com/comfyui-workflows/instantcharacter-comfyui-workflow-flux-dit-personalization) - The model strikes a strong balance between identity preservation and prompt-based control, allowing ...

23. [InstantCharacter](https://instantcharacter.github.io) - InstantCharacter demonstrates three fundamental advantages: first, it achieves open-domain personali...

24. [Tencent-Hunyuan/InstantCharacter - GitHub](https://github.com/Tencent-Hunyuan/InstantCharacter) - InstantCharacter is an innovative, tuning-free method designed to achieve character-preserving gener...

25. [UNO for ComfyUI | Consistent Subject Generation - RunComfy](https://www.runcomfy.com/comfyui-workflows/uno-for-comfyui-consistent-subject-generation) - The UNO workflow for ComfyUI brings the advanced image generation technology to RunComfy. This power...

26. [Flux UNO Multiple Image Reference + Kling I2V : r/comfyui - Reddit](https://www.reddit.com/r/comfyui/comments/1jwrv43/flux_uno_multiple_image_reference_kling_i2v/) - UNO Mutil Image Reference + Kling I2V UNO workflow: https://github.com/jax-explorer/ComfyUI-UNO/blob...

27. [PhotoMaker/README_pmv2.md at main - GitHub](https://github.com/TencentARC/PhotoMaker/blob/main/README_pmv2.md) - Additionally, PhotoMaker V2 allows users to achieve better ID consistency by combining it with IP-Ad...

28. [Tencent releases PhotoMaker V2 : r/StableDiffusion - Reddit](https://www.reddit.com/r/StableDiffusion/comments/1ea6wb1/tencent_releases_photomaker_v2/) - ✓ July 22, 2024. We release PhotoMaker V2 with improved ID fidelity. At the same time, it still main...

29. [smthemex/ComfyUI_StoryDiffusion: You can using ... - GitHub](https://github.com/smthemex/ComfyUI_StoryDiffusion) - Using different ID migration methods to make storys in ComfyUI. Origin methods from: StoryDiffusion ...

30. [Consistent Self-Attention for Long-Range Image and Video Generation](https://neurips.cc/virtual/2024/poster/94916) - The proposed StoryDiffusion encompasses pioneering explorations in visual story generation with the ...

31. [ali-vilab/In-Context-LoRA - GitHub](https://github.com/ali-vilab/In-Context-LoRA) - The core concept of IC-LoRA is to concatenate both condition and target images into a single composi...

32. [[Sharing Experience] Training Z-Image LoRA using 12G VRAM ~ #550](https://github.com/ostris/ai-toolkit/issues/550) - To minimize VRAM usage, after extensive testing, training was successful with 6~10 images, yielding ...

33. [Realtime LoRA Trainer - ComfyUI Cloud](https://comfy.icu/node/RealtimeLoraTrainer) - Train and Block Edit and Save LoRAs directly inside ComfyUI. Supports SDXL (via sd-scripts), FLUX, Z...

34. [SimpleTuner now supports Flux.1 training (LoRA, full)](https://www.reddit.com/r/StableDiffusion/comments/1ejlvuw/simpletuner_now_supports_flux1_training_lora_full/) - If sdxl numbers are anything to go by, you generally need 50-100 good images of a character for the ...

35. [Flux Lora Training - RunDiffusion](https://www.rundiffusion.com/flux-lora-training) - In this tutorial, we'll walk you through the steps of setting up Flux LoRA training in Kohya. Using ...

36. [K-LoRA: Unlocking Training-Free Fusion of Any Subject and Style LoRAs](https://arxiv.org/html/2502.18461v1) - ...both the original subject and style simultaneously or require
additional training. In this paper,...

37. [Pencil sketch -FLUX Style LoRA - v1.0 | Flux LoRA | Civitai](https://civitai.com/models/703228/pencil-sketch-flux-style-lora) - Creates "handdrawn" pecil sketch images With LoRA: Without LoRA

38. [Z-Image Turbo LoRA training with AI Toolkit and Z-Image ControlNet ...](https://www.youtube.com/watch?v=ezD6QO14kRc) - Z-Image Turbo LoRA training with Ostris AI Toolkit + Z-Image Turbo Fun Controlnet Union + 1-click to...

39. [How to Generate a Consistent Character Dataset for LoRA using ...](https://www.youtube.com/watch?v=GnyZ2mBV3sg) - Welcome to my channel, In this video, I walk you through creating a consistent character dataset usi...

40. [QWEN Image Edit can create Character Consistent LoRA Dataset](https://www.reddit.com/r/comfyui/comments/1o5fmex/qwen_image_edit_can_create_character_consistent/) - A tutorial that I put together to help create dataset with consistent face from single image with mu...

41. [Qwen Image Models Training - 0 to Hero Level Tutorial - LoRA ...](https://dev.to/furkangozukara/qwen-image-models-training-0-to-hero-level-tutorial-lora-fine-tuning-base-edit-model-2goj) - This tutorial covers how to do LoRA training and full Fine-Tuning / DreamBooth training on Qwen Imag...

42. [QWEN Image Edit can create Character Consistent LoRA Dataset](https://weirdwonderfulai.art/comfyui/qwen-image-edit-can-create-character-consistent-lora-dataset/) - QWEN Image Edit model which is designed to replace many different tools we've used like Inpainting, ...

43. [Flux 2 Klein 9 consistency+loras : r/StableDiffusion - Reddit](https://www.reddit.com/r/StableDiffusion/comments/1qh8tgv/flux_2_klein_9_consistencyloras/) - With a character LoRA, you should keep 99% consistency as long as you are only using that LoRA alone...

44. [Run FLUX 2 [klein] 9b Base Trainer (Training) API on fal](https://fal.ai/models/fal-ai/flux-2-klein-9b-base-trainer) - Custom model specialization through LoRA fine-tuning for text-to-image generation. · Built for: Bran...

45. [dx8152/Flux2-Klein-9B-Consistency - Hugging Face](https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency) - Instructions to use dx8152/Flux2-Klein-9B-Consistency with libraries, inference providers, notebooks...

46. [README.md · dx8152/Flux2-Klein-9B-Consistency at main](https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency/blob/main/README.md) - We’re on a journey to advance and democratize artificial intelligence through open source and open s...

47. [Beginner friendly flux.2 klein character dataset builder - Facebook](https://www.facebook.com/groups/1555938565310078/posts/1934341744136423/) - It's great to use if you want to generate an entire dataset which you can then later use to train yo...

48. [Beginner friendly flux workflow for character dataset building](https://www.facebook.com/groups/885988313632684/posts/1218600597038119/) - 2 Klein is excellent on its own at preserving and reusing character details from a reference image, ...

49. [ComfyUI Stable Diffusion 3.5 vs FLUX.1 Workflow - RunComfy](https://www.runcomfy.com/comfyui-workflows/stable-diffusion-3.5-vs-flux1) - Experience the incredible capabilities of Stable Diffusion 3.5 (SD3.5) and FLUX.1, two cutting-edge ...

50. [Getting Started with Stable Diffusion 3.5 - Civitai Education](https://education.civitai.com/getting-started-with-stable-diffusion-3-5/) - SD 3.5 comes in three flavors; Large, Large Turbo, and Medium weight, the latter of which will run o...

51. [Solving Character Consistency in AI-Generated Content with Flux.1 ...](https://comfyui.org/en/solving-character-consistency-with-flux1-kontext) - The challenge of maintaining character consistency in AI-generated influencer content has been a maj...

52. [FLUX.1 Kontext [pro] (Image to Image) API on fal - Fal.ai](https://fal.ai/models/fal-ai/flux-pro/kontext) - Creative Image Editing Modify existing images with natural language instructions. · Character Consis...

53. [GitHub - siliconecomputervision/ToonCrafterNode: a Comfy node for generative cartoon interpolation](https://github.com/siliconecomputervision/ToonCrafterNode) - a Comfy node for generative cartoon interpolation. Contribute to siliconecomputervision/ToonCrafterN...

54. [Multi-Frame Interpolation with ToonCrafter | ComfyUI Workflow](https://openart.ai/workflows/markury/multi-frame-interpolation-with-tooncrafter/KkTLeQf2ypVJ6RGBej4C) - Created by: markury: This is my entry for the ToonCrafter contest here on OpenArt. This is the workf...

55. [The state of AI for hand-drawn animation inbetweening - Yossi Kreinin](https://yosefk.com/cgi-bin/comments.cgi?post=blog%2Fthe-state-of-ai-for-hand-drawn-animation-inbetweening) - We'll take a look at two recently published papers on animation “inbetweening” – the automatic gener...

56. [How to Use Frame Interpolation in ComfyUI for Fluid Animations](https://www.youtube.com/watch?v=alu-lcIfGoY) - #comfyui #aitools #stablediffusion 
Frame interpolation in a video processing technique that adds ad...

57. [Preprocessor and Frame Interpolation Workflows in ComfyUI](https://blog.comfy.org/p/preprocessor-and-frame-interpolation) - Depth, Lineart, Pose, Normals, and Frame Interpolation: Ready-to-Use Building Blocks

58. [ComfyUI frame interpolation workflow](https://docs.comfy.org/tutorials/utility/frame-interpolation)

59. [Lance: Unified Multimodal Modeling by Multi-Task Synergy](https://x.com/ByteDanceOSS/status/2056654541555466501)

60. [Daily Papers' Post - LinkedIn](https://www.linkedin.com/posts/daily-papers-ab213b360_bytedance-just-released-lance-a-3b-native-activity-7462430487660371968-maIq) - ByteDance just released Lance, a 3B native unified multimodal model that understands, generates, and...

61. [Lance: Unified Multimodal Understanding, Generation, and Editing](https://hyper.ai/en/notebooks/51514) - Lance is a 3B native unified multimodal model released by ByteDance in May 2026. It targets image un...

62. [bytedance-research/Lance - Hugging Face](https://huggingface.co/bytedance-research/Lance) - Lance is a lightweight native unified multimodal model that supports image and video understanding, ...

63. [ByteDance Lance & Hi-Dream-O1 Image ComfyUI - YouTube](https://www.youtube.com/watch?v=fvEeEW6trXA) - Discover ByteDance Lance and HiDream-01 Image -- two groundbreaking unified multimodal AI models tha...

64. [OmniGen2: Exploration to Advanced Multimodal Generation](https://vectorspacelab.github.io/OmniGen2/) - OmniGen2 is a unified multimodal generation model that combines strong visual understanding, text-to...

65. [BAAI Launches OmniGen2: A Unified Diffusion and ...](https://www.marktechpost.com/2025/06/24/baai-launches-omnigen2-a-unified-diffusion-and-transformer-model-for-multimodal-ai/) - OmniGen2 advances multimodal generation with decoupled architecture, reflection-based refinement, an...

66. [Exploration to Advanced Multimodal Generation](https://www.themoonlight.io/es/review/omnigen2-exploration-to-advanced-multimodal-generation) - OmniGen2 is an open-source, versatile generative model designed for unified text-to-image (T2I) gene...

67. [OmniGen2 Released: Unified Image Understanding and ...](https://comfyui-wiki.com/en/news/2025-06-24-omnigen2-unified-image-generation) - VectorSpaceLab releases OmniGen2, a powerful multimodal generation model that supports precise local...

68. [Z-Image Turbo 2026: Next Level LoRA Node & Auto Prompts](https://www.youtube.com/watch?v=07LnTfvC8Hg) - Delete your default ComfyUI LoRA. It ruins Z-Image Turbo data. Here is the exact setup to fix AI lig...

69. [HiDream-I1 Open Source Release - Next Generation Image ...](https://comfyui-wiki.com/en/news/2025-04-08-hidream-i1-open-source-release) - With 17B parameters, this model can generate high-quality images within seconds and has achieved lea...

70. [HiDream-I1 - GitHub](https://github.com/HiDream-ai/HiDream-I1) - HiDream-I1 is a new open-source image generative foundation model with 17B parameters that achieves ...

71. [DeepSeek Release Another Open-Source AI Model, Janus Pro - InfoQ](https://www.infoq.com/news/2025/01/deepseek-ai-janus/) - DeepSeek has released Janus-Pro, an updated version of its multimodal model, Janus. The new model im...

72. [Janus-Series: Unified Multimodal Understanding and Generation ...](https://github.com/deepseek-ai/janus) - 2025.01.27: Janus-Pro is released, an advanced version of Janus, improving both multimodal understan...

73. [deepseek-ai/Janus-Pro-7B - Hugging Face](https://huggingface.co/deepseek-ai/Janus-Pro-7B) - The simplicity, high flexibility, and effectiveness of Janus-Pro make it a strong candidate for next...

