# Deep Research Prompts — Character-Consistent Image Models for 2D Animation In-Betweens

**Created:** 2026-05-22
**Purpose:** Three prompts engineered for Perplexity Deep Research, Gemini Deep Research, and ChatGPT Deep Research. Goal is to identify 2025–2026 closed-source and open-source image generation + editing models that can replace Nano Banana 2 for in-between frames in the pencil-test pipeline, preserving character identity (Sean) and hand-drawn pencil aesthetic at a fraction of the per-frame cost.

**How to use:**
1. Run **Prompt 1 — Master Survey** first in *all three* tools (Perplexity, Gemini, ChatGPT). Compare outputs — the three engines surface different corners of the web and the overlap is your high-confidence signal.
2. Run **Prompt 2 — Identity Preservation Deep-Dive** next. The base model rarely matters more than the adapter / LoRA / training stack on top of it; this is where the real cost savings live.
3. Run **Prompt 3 — Image Editing Deep-Dive** to find precise edit tooling so you can fix one hand or one expression without re-generating the whole frame.

When pasting, you may strip the `# Role` block in tools that already set their own system message — keep it for ChatGPT and Gemini, optional for Perplexity.

---

## Prompt 1 — Master Survey (run in all three engines)

```
# Role
You are a research analyst specializing in generative AI image models for animation production pipelines. You have access to the latest information from model release notes, technical papers, benchmark studies, practitioner forums (Reddit r/StableDiffusion, Hugging Face discussions, X/Twitter, Civitai, ComfyUI workflow shares), and animation studio case studies.

# Project Context
I am producing a 2D pencil-test animation portfolio piece. The pipeline runs in five phases (Scaffold → Generate → Motion → Audit → Assemble). Every frame must match:
- A single character reference image of "Sean" (3/4 head + full body, hand-drawn pencil style on cream paper)
- Aesthetic: hand-drawn pencil test on cream animation paper, visible construction lines, cross-hatching, pencil grain, hole-punch marks on the page
- Aspect ratio: 16:9

# Current Stack (DO NOT re-recommend these — find alternatives)
- Keyframes: Google Gemini Nano Banana 2 (~$0.039/image) — excellent character consistency via multi-reference conditioning, but expensive at scale
- Keyframes (secondary): OpenAI's GPT image model ("gpt-image-1" / "ChatGPT image 2.0") — strong editing
- Motion interpolation: ByteDance Seedance 2.0 via fal.ai (start+end frame video, then frame extract)
- In-betweens currently: NB2 redraw of selected Seedance frames (expensive)

# The Problem
Nano Banana 2 produces beautiful, character-consistent output but costs add up across hundreds of in-between frames. I want a cheaper-or-free tier of models for IN-BETWEENS — frames that already have strong context (an approved start frame + end frame + reference character). For in-betweens, I need:
1. Strong character/identity preservation given 1–3 reference images
2. Aesthetic preservation (pencil test on cream paper — no slick digital look)
3. Image editing — modify specific regions while leaving the rest untouched (Photoshop generative-fill quality)
4. Multi-image conditioning (start frame + end frame + style/character reference)
5. Affordable or self-hostable (consumer GPU, e.g., 24GB VRAM, or low API cost)

# Research Tasks
Produce a thorough, citation-rich report covering ALL of the following:

## 1. Closed-source image generation + editing models (Jan 2025 – present)
For each model, document: release date, pricing (per-image and bulk), API availability and providers (fal.ai, Replicate, Together, native), character consistency strength (cite tests if available), editing capabilities (inpaint, region edit, instruction-edit like "change only the hand"), multi-reference conditioning support, known weaknesses for hand-drawn / non-photoreal styles.

Investigate at minimum (find more):
- Black Forest Labs: FLUX.1 Pro, FLUX.1.1 Pro, FLUX.1 Kontext (Pro / Max / Dev), any 2026 successors
- Ideogram 2.0 / 3.0
- Recraft V3 and successors
- Midjourney V7 + character reference + Edit features
- Google: Imagen 3 / 4, any Gemini image-edit modes beyond Nano Banana 2
- OpenAI: gpt-image-1, gpt-image-2, edit endpoints
- Adobe Firefly Image 4 + Generative Fill APIs
- Stability AI: Stable Image Core / Ultra / 3.5 hosted APIs
- ByteDance Doubao / SeedEdit
- Tencent Hunyuan API
- Alibaba: Qwen-Image, Qwen-Image-Edit (hosted versions)
- Any newer 2026 entrants (search: "best image editing model 2026", "FLUX successor", "best character consistency model 2026")

## 2. Open-source image generation + editing models (Jan 2025 – present)
For each: HF / GitHub repo and license (research-only vs commercial OK), VRAM requirements (8 / 12 / 16 / 24 / 48 GB), inference speed on common GPUs (4090, A100, H100), quality vs closed-source equivalents, editing / multi-image / character consistency support, active ecosystem (LoRA training, ComfyUI nodes, community size).

Investigate at minimum:
- FLUX.1 [dev], [schnell], Kontext [dev]
- Qwen-Image, Qwen-Image-Edit
- Stable Diffusion 3.5 Large / Medium / Turbo
- SDXL successors
- HiDream-I1
- HunyuanImage, HunyuanImage-2.1, Hunyuan-DiT
- OmniGen, OmniGen2 (unified gen+edit)
- DeepSeek Janus-Pro
- Lumina-Image, PixArt-Sigma
- Sana (NVIDIA)
- Any 2026 releases not in my list

## 3. Identity / character preservation techniques (often matters more than the base model)
- IP-Adapter (latest variants — FaceID, FaceID-Plus-v2, FaceID-Portrait, Plus-Face-SDXL)
- InstantID and successors
- PuLID, PuLID-FLUX, PuLID-Lightning
- LoRA training: minimum dataset size, time on a 4090, character LoRA best practices for FLUX vs SDXL vs SD3.5
- DreamBooth-style fine-tunes
- Textual Inversion / Pivotal Tuning
- ConsiStory, StoryDiffusion, IC-LoRA, AnimateDiff character coherence
- Reference-only ControlNet
- Cross-frame attention techniques
For each: compatible base models, quality, setup complexity, evidence from independent comparisons.

## 4. In-between specific workflows — case studies + practitioner reports
- How are indie animators and studios using AI for tweening in 2025–2026?
- Toon Boom Anime Inbetweener, CACANi, Cadmium Cel, EbSynth — do any wrap AI models now?
- Studio case studies (Netflix Animation, Toonstar, Corridor Digital, Aardman, others)
- Open-source workflows: ComfyUI graphs that do "frame N → frame N+1 with character lock"
- Are there models trained specifically on traditional animation in-between data (e.g., AnimeInbet, ToonCrafter, EISAI, DAIN-derived)?

## 5. Recommended pipeline configurations for my use case
Synthesize the above into 3 concrete configurations:
- **Config A — Best Quality:** even if expensive, what comes closest to NB2 quality for in-betweens?
- **Config B — Best Value:** biggest cost savings while keeping recognizable character consistency
- **Config C — Fully Self-Hosted:** runs on a single 4090 (24 GB), zero API cost after setup
For each: base model, editing/conditioning approach, character preservation technique, expected quality vs NB2 baseline, estimated cost per frame (or capex), known failure modes.

# Output Format
A structured report with:
1. Executive summary (5 bullets) — top recommendations and biggest surprises
2. Comparison table — all models side-by-side: name, type (closed/open), character-consistency rating (1–5), editing rating (1–5), cost per image or VRAM req, license, my-use-case fit (1–5)
3. Detailed sections per the research tasks above
4. Three recommended configurations with reasoning
5. Open questions / unknowns where evidence was thin
6. Citations with URLs and dates for every claim

# Hard Rules
- Cite sources for every claim with URLs and publication dates
- Flag anything older than 12 months as "potentially superseded"
- Prefer benchmarks and side-by-side comparisons over marketing copy
- Do NOT invent capabilities — if you can't confirm a feature, say so
- Distinguish "claimed" capabilities from "verified by independent users"
- Search practitioner sources, not just vendor pages: r/StableDiffusion, HF Spaces, X.com, YouTube tutorials, Civitai, ComfyUI workflow repos
```

---

## Prompt 2 — Identity Preservation Deep-Dive

```
# Role
You are an AI research analyst specializing in identity and character preservation techniques for diffusion image models.

# Project Context
I am conditioning image models to consistently render the same character ("Sean") across hundreds of frames in a 2D pencil-test animation. I have:
- 1 hero reference image of the character (3/4 head, full body, pencil-drawn)
- ~30 approved keyframes already generated by Nano Banana 2 (could become a LoRA training set or extra references)
- A consumer rig with a 24 GB GPU (RTX 4090 equivalent)
- Goal: drop API cost by running in-betweens locally without losing character likeness

# Research Task
Produce a 2025–2026 guide to identity preservation for character-consistent image generation, covering:

## 1. Adapter-based methods (no training required)
- IP-Adapter family: FaceID, FaceID-Plus, FaceID-Plus-v2, FaceID-Portrait, Plus-Face-SDXL
- InstantID, InstantID-XL
- PuLID, PuLID-FLUX, PuLID-Lightning
- PhotoMaker v1 / v2
- Storyboard / scene-coherence adapters: ConsiStory, StoryDiffusion, IC-LoRA
- HyperLoRA, Tencent ID adapters
- Any 2026 successors
For each: how it works (high-level), supported base models, VRAM, similarity preservation 1–5, edit-ability of pose/expression while preserving identity, recent independent comparisons.

## 2. Training-based methods
- LoRA character training: optimal dataset size (5 / 20 / 100+ images), augmentation strategy, captioning approach, training time on a 4090, recommended trainers (kohya_ss, ai-toolkit, OneTrainer, SimpleTuner)
- DreamBooth and modern variants
- Textual Inversion / Pivotal Tuning
- FLUX-specific: best 2025–2026 LoRA training workflows, working sample configs
- SDXL: still relevant in 2026 or surpassed?
- SD3.5: maturity of LoRA training ecosystem

## 3. Hybrid / combined approaches
- LoRA + IP-Adapter combos
- ControlNet (pose, openpose, depth) + identity adapter for the in-between use case
- Multi-reference attention manipulation
- Style LoRA + character LoRA stacking

## 4. Specifically for the in-between use case
Given start frame + end frame + reference, what's the state of the art for generating a frame that (a) looks like the same character, (b) smoothly interpolates pose/expression, (c) preserves a specific art style (pencil / hand-drawn)? Identify 2025–2026 papers and ComfyUI workflows that target this exact problem (e.g., ToonCrafter, AnimeInbet, EISAI, FILM, RIFE-derived, custom diffusion-based interpolation).

## 5. Practical recipe recommendations
Three setups optimized for my rig (24 GB):
- **Fast & flexible** — adapter-only, no training
- **High-fidelity** — LoRA-trained on existing keyframes + adapter
- **Style-locked** — combo of character LoRA + style LoRA + control conditioning
Each: exact models/files, ComfyUI graph description, expected quality, common failure modes.

# Output Format
- Executive summary (5 bullets)
- Side-by-side comparison table: technique × base model × quality × setup difficulty × VRAM
- Detailed sections
- Three pipeline recipes
- Citations for every claim with URLs and dates

# Hard Rules
- Prioritize 2025–2026 sources; flag pre-2025 info as "may be superseded"
- Cite HF model cards, GitHub repos, arXiv papers, independent benchmarks
- Verify availability — flag if a method is "research only" or has been abandoned
- Don't conflate similar-named methods (InstantID ≠ InstantStyle, IP-Adapter-FaceID ≠ IP-Adapter-Plus)
```

---

## Prompt 3 — Image Editing Deep-Dive

```
# Role
You are a research analyst evaluating image editing models for an animation production pipeline.

# Project Context
I produce 2D pencil-test animation frames. After generating a keyframe, I often need to make targeted edits — e.g., "change only the hand pose," "redraw the eyes with a different expression," "extend the paper canvas to add background," "fix the stylus angle without redrawing the face." Currently I either re-generate the whole frame (expensive, character drifts) or hand-fix in Procreate (slow). I want models that perform precise, instruction-driven edits while preserving the rest of the image exactly.

# Research Task
Produce a 2025–2026 state-of-the-art report on instruction-driven and region-based image editing, suitable for hand-drawn / non-photorealistic content.

## 1. Closed-source editing models
- Google Nano Banana 2 (confirm latest edit capabilities for comparison)
- OpenAI gpt-image-1 / image-edit endpoint
- Black Forest Labs FLUX Kontext Pro / Max
- ByteDance SeedEdit
- Adobe Firefly Generative Fill (API)
- Ideogram Magic Fill / Edit
- Recraft Inpaint / Edit
- Any 2026 entrants
For each: edit invocation (mask vs instruction vs reference), preservation of un-edited areas, identity preservation, multi-edit chains, cost per edit, API stability.

## 2. Open-source editing models
- FLUX.1 Kontext [dev]
- Qwen-Image-Edit, Qwen-Image-Edit-Plus (or latest)
- OmniGen, OmniGen2 (unified gen+edit)
- SD3.5 + ControlNet-Inpaint, BrushNet, PowerPaint
- HiDream-Edit (if released)
- InstructPix2Pix, MagicBrush, UltraEdit
- Anole, Emu-Edit (if open-released)
For each: install/run reqs, edit quality, instruction following, region precision, character preservation, license.

## 3. Editing techniques (model-agnostic)
- Inpainting with masks — best 2026 inpaint pipelines
- Instruction-edit ("change X to Y") vs reference-edit (here's a target)
- Latent blending and seed-locking for preservation
- Multi-region simultaneous edits
- Differential diffusion / region-aware sampling

## 4. Specifically for hand-drawn / pencil / non-photoreal content
- Which models preserve a hand-drawn aesthetic during edits without slicking the output?
- Practitioner reports from indie illustrators and animators
- Style-locked editing techniques (LoRA + edit pipeline)

## 5. Recommended editing setups for my use case
Three configurations:
- **Cheapest reliable closed-source** edit per frame
- **Best-quality open-source** edit on a 24 GB GPU
- **Hybrid:** open-source bulk edits + closed-source for hero shots

# Output Format
- Executive summary
- Comparison table: model × edit type × instruction-follow rating × preservation rating × cost/VRAM × style flexibility
- Detailed model sections
- Three recommended setups
- Citations for every claim

# Hard Rules
- Cite all sources with URLs and dates
- Link to actual edit-result examples when sources provide them
- Note whether each model handles non-photorealistic styles or only photoreal
- Distinguish models that edit by mask vs by instruction vs by reference image
```

---

## Notes on engine differences

- **Perplexity Deep Research** — favors recent web sources and citations; will rank well on practitioner forums and recent vendor docs. Strongest for "what's the latest model?" sections.
- **Gemini Deep Research** — strong on academic papers (arXiv) and Google-indexed technical blogs; tends to produce the longest, most structured reports. Strongest for "techniques deep dive" sections.
- **ChatGPT Deep Research** — broad synthesis with strong reasoning across multiple sources; will produce the cleanest comparison tables and recommendations. Strongest for "synthesize into 3 configs" sections.

Compare the three reports — overlap = high-confidence signal; uniques = leads to verify directly.
