\# Generative AI for 2D Animation In-Betweening: 2026 Pipeline Analysis

The landscape of generative Artificial Intelligence (AI) for image synthesis has shifted dramatically from mid-2025 to early 2026, transitioning from single-image generation to complex, context-aware sequential editing. For traditional 2D animation—particularly the delicate aesthetic of a hand-drawn pencil test on cream paper with visible construction lines—generative models present a unique paradox. While they offer unprecedented speed for producing in-between frames, they aggressively tend to "clean up" or digitalize raw traditional aesthetics. 

Research suggests that achieving temporal consistency without destroying the tactile reality of paper grain and cross-hatching requires a highly orchestrated pipeline. Relying solely on large, closed-source models for every frame scales poorly in cost, demanding a strategic pivot toward localized editing models, zero-shot identity preservation, and non-generative texture synthesis. This report evaluates the current state of closed and open-source models, character preservation techniques, and practitioner workflows to construct viable, cost-effective pipelines for your specific production parameters.

\#\# 1\. Executive Summary

\*   \*\*Texture Synthesis Outperforms Diffusion for Aesthetic Preservation:\*\* The most significant finding for a pencil-test pipeline is that generative diffusion models inherently struggle to maintain static paper grain and hole-punch marks across frames. EbSynth 2.0, which utilizes pixel-level texture synthesis rather than neural hallucination, remains the most reliable method for preserving raw, traditional aesthetics between keyframes.  
\*   \*\*The Rise of Unified Generation-Editing Architectures:\*\* Models released in late 2025 and 2026, such as OmniGen2 and Qwen-Image-Edit-2509, have decoupled their visual encoding to perform highly precise, instruction-based editing without the need for external IP-Adapters (Image Prompt Adapters) or ControlNets, drastically simplifying multi-image conditioning.  
\*   \*\*Zero-Shot Identity is Replacing Heavy Fine-Tuning:\*\* PuLID Flux II has largely solved the "model pollution" problem (where a character's features bleed into the art style), allowing for highly accurate zero-shot character insertion on consumer GPUs (24GB VRAM) without the hours required for Low-Rank Adaptation (LoRA) training.  
\*   \*\*Cost Disparities are Widening:\*\* While Ideogram 3.0 and Nano Banana 2 offer premium character-locked APIs at high costs ($0.10–$0.20 and \~$0.04 per image respectively), competitors like ByteDance's SeedEdit 3.0 deliver state-of-the-art regional editing for exactly 0.05 PTC ($0.007 USD) per call, altering the economic calculus for indie animators.  
\*   \*\*ToonCrafter Remains the Interpolation Standard:\*\* For generative motion between two static keyframes, the open-source ToonCrafter ecosystem (via ComfyUI) remains the most robust, though it requires specific node configurations to avoid aggressive VRAM consumption.  
\*   \*\*Pipeline Recommendations:\*\* For \*\*Config A (Best Quality)\*\*, the recommended pipeline utilizes Nano Banana 2 or Seedance 2.0 for base generation, SeedEdit 3.0 for regional editing, and EbSynth 2.0 for character/aesthetic preservation. For \*\*Config B (Best Value)\*\*, the pipeline relies on ToonCrafter for base interpolation, FLUX.2 \[schnell\] guided by PuLID Flux II for keyframes, and post-processing filters. For \*\*Config C (Fully Self-Hosted)\*\*, OmniGen2 or Qwen-Image-Edit-2509 serve as the base model, utilizing their native in-context instruction editing and zero-shot conditioning without API costs.

\#\# 2\. Model Comparison Matrix

The following table provides a comparative synthesis of the leading closed and open-source models evaluated for your specific use case. 

Evaluating these tools requires looking beyond standard photorealism benchmarks. For 2D pencil-test animation, a model's "My-Use-Case Fit" is heavily weighted by its ability to accept multiple reference images (start frame, end frame, character sheet) and perform localized edits without altering the background paper texture.

| Model Name | Type | Character Consistency (1-5) | Editing Precision (1-5) | Cost / VRAM Requirement | License / Terms | My-Use-Case Fit (1-5) |  
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |  
| \*\*FLUX.2 \[pro\]\*\* | Closed (API) | 5 | 5 | \~$0.04 \- $0.055 / image | Commercial API | 4 \- Excellent but expensive |  
| \*\*Ideogram 3.0\*\* | Closed (API) | 5 | 4 | $0.10 \- $0.20 / image (w/ ref) | Commercial API | 2 \- Too expensive for in-betweens |  
| \*\*SeedEdit 3.0\*\* | Closed (API) | 4 | 5 | \~$0.007 (0.05 PTC/call) | Commercial API | 5 \- Exceptional value and regional control |  
| \*\*OmniGen2\*\* | Open | 4 | 4 | \~17GB VRAM (RTX 3090/4090) | MIT / Open Research | 5 \- Best self-hosted unified editor |  
| \*\*Qwen-Image-Edit\*\* | Open | 4 | 4 | 8GB+ VRAM (GGUF quantization)| Apache 2.0 | 4 \- Strong multi-image support |  
| \*\*ToonCrafter\*\* | Open | 3 | N/A (Interpolator) | 12GB+ VRAM | Open Research | 4 \- Purpose-built for in-betweens |  
| \*\*HunyuanImage 3.0\*\* | Open | 4.5 | 4 | 24GB+ VRAM (13B active MoE) | Open / Commercial OK | 3 \- Strong for anime, heavy to run |  
| \*\*Stable Diffusion 4 Ultra\*\*| Open | 5 | 4 | 24GB+ VRAM (Enterprise focus)| Community | 4 \- New standard for open weights |  
| \*\*Imagen 4 (Fast)\*\* | Closed (API) | 4 | 4 | $0.02 / image | Commercial API | 3 \- Fast but highly photographic |  
| \*\*Nano Banana 2\*\* | Closed (API) | 5 | 4 | $0.04 / image (1K res) | Commercial API | 4 \- Elite consistency, costly at scale |  
| \*\*GPT-Image-2\*\* | Closed (API) | 5 | 5 | Premium API / ChatGPT Plus | Commercial API | 3 \- Excellent editing, high cost |

This matrix reveals a clear bifurcation in the market. While premium closed-source models like Ideogram 3.0 and FLUX.2 \[pro\] command high prices for guaranteed consistency, open-source models and heavily subsidized APIs (like ByteDance's SeedEdit) have closed the quality gap for specific editing tasks. For a pipeline requiring hundreds of in-betweens, relying on models scoring high in fit and low in cost is imperative.

\#\# 3\. Closed-Source Generation and Editing Models (Jan 2025 – Present)

The closed-source ecosystem has aggressively pursued instruction-based editing—allowing users to type "change only the hand" without destroying the surrounding pixels. This is critical for auditing and fixing AI-generated in-betweens. 

To ensure strict evaluation parity, every model below is assessed against the exact same structural parameters based on available research.

\#\#\# Black Forest Labs: The FLUX.2 and Kontext Ecosystem  
Following the massive success of FLUX.1, Black Forest Labs introduced the FLUX.1 Kontext suite in May 2025, a flow-matching architecture specifically designed for context-aware image generation \[cite: 1\]. Rather than treating every generation as a blank slate, Kontext analyzes a starting image and modifies only the requested elements \[cite: 2\]. FLUX utilizes a flow-matching architecture. \*\*1) Core Definition:\*\* It is a generative framework that maps a simple base distribution (noise) to a complex data distribution (images) using continuous vector fields. \*\*2) Analogy:\*\* Instead of randomly scattering sand and slowly shifting it into a castle (standard diffusion), flow-matching plots a direct, continuous river current for each grain of sand to its final destination. \*\*3) Animation Relevance:\*\* This mathematical precision provides highly deterministic, stable generation across frames, significantly reducing the random pixel flickering or 'boiling' common in standard diffusion models, making it superior for generating consistent pencil-test aesthetics.

In November 2025, they released the 32-billion parameter FLUX.2 family, which natively absorbed the Kontext editing capabilities and introduced multi-reference composition \[cite: 3, 4\].   
\*   \*\*Release Date:\*\* November 25, 2025 \[cite: 4\].  
\*   \*\*Pricing:\*\* Exact megapixel-based pricing translates to roughly $0.04 to $0.055 per image via primary API gateways \[cite: 5, 6\].  
\*   \*\*API Providers:\*\* Azure AI Foundry, fal.ai, Replicate, and native BFL API \[cite: 5, 7\].  
\*   \*\*Character Consistency Strength:\*\* 5/5. FLUX.2 \[Dev\] achieved a 63.6% win rate in multi-reference editing against open-weight competitors in independent KontextBench testing \[cite: 4\].  
\*   \*\*Editing Capabilities:\*\* Elite instruction-based editing (e.g., iterative multi-turn editing without external adapters) \[cite: 7, 8\].  
\*   \*\*Multi-Reference Conditioning Support:\*\* Yes. It natively supports referencing up to 10 images simultaneously, locking identity across outputs \[cite: 3, 4\].  
\*   \*\*Known Weaknesses for Hand-Drawn Styles:\*\* It strictly utilizes a "positive-only" architecture (no negative prompts), making it difficult to suppress unwanted digital smoothing or explicitly force raw construction lines if the prompt drifts toward photorealism.

\#\#\# ByteDance SeedEdit 3.0 (Doubao)  
Released in June 2025 by ByteDance's Seed team, SeedEdit 3.0 represents a breakthrough in high-fidelity, localized image editing built on a causal diffusion network tied to a Vision-Language Model (VLM) \[cite: 9, 10\].  
\*   \*\*Release Date:\*\* June 6, 2025 \[cite: 9\].  
\*   \*\*Pricing:\*\* Approximately 0.05 PTC (Platform Tokens) per call, translating to exactly $0.007 USD per image \[cite: 9\].  
\*   \*\*API Providers:\*\* 302.ai API, Bytedance native gateways \[cite: 9\].  
\*   \*\*Character Consistency Strength:\*\* 4/5. Exceptional detail preservation on faces and textures natively \[cite: 11\].  
\*   \*\*Editing Capabilities:\*\* State-of-the-art instruction editing. It achieved a 56.1% usability rate in benchmarking, outperforming GPT-4o (37.1%) in following precise localized editing instructions \[cite: 11, 12\].  
\*   \*\*Multi-Reference Conditioning Support:\*\* Unverified explicitly for bulk image blending, but highly effective at single-reference semantic modifications \[cite: 13\].  
\*   \*\*Known Weaknesses for Hand-Drawn Styles:\*\* Independent testing notes that SeedEdit may occasionally misinterpret highly stylized or sparse pencil sketches as noise, requiring careful text prompting to prevent it from "cleaning" the grain.

\#\#\# Ideogram 3.0  
\*   \*\*Release Date:\*\* March 26, 2025 \[cite: 14\].  
\*   \*\*Pricing:\*\* $0.10 \- $0.20 per image on premium/reference settings; monthly subscriptions range from $7 to $50 \[cite: 14, 15\].  
\*   \*\*API Providers:\*\* Native Ideogram API, Replicate, fal.ai, Krea AI \[cite: 16\].  
\*   \*\*Character Consistency Strength:\*\* 5/5. Relies on a dedicated Style Reference system \[cite: 17\].  
\*   \*\*Editing Capabilities:\*\* Introduced "Magic Fill" and "Extend" for regional replacement and outpainting \[cite: 16\].  
\*   \*\*Multi-Reference Conditioning Support:\*\* Yes. Allows uploading up to 3 reference images simultaneously to control aesthetics \[cite: 16, 17\].  
\*   \*\*Known Weaknesses for Hand-Drawn Styles:\*\* Hyper-optimized for commercial graphic design, vector typography, and photorealism; it heavily resists maintaining raw, unpolished pencil grain.

\#\#\# Midjourney V7  
\*   \*\*Release Date:\*\* April 2025 (Alpha testing), May 2025 (Full Editor) \[cite: 18, 19\].  
\*   \*\*Pricing:\*\* Premium subscription ($10–$60/mo) \[cite: 15\].   
\*   \*\*API Providers:\*\* Officially closed API; accessible via Discord or web interface. Third-party gateways like Unitool AI exist but are unofficial \[cite: 19, 20\].  
\*   \*\*Character Consistency Strength:\*\* 5/5. Utilizing the "Omni Reference" and personalized training profiles \[cite: 19\].  
\*   \*\*Editing Capabilities:\*\* Full smart layer editing, inpainting, and conversational editing via Draft Mode \[cite: 19, 21\].  
\*   \*\*Multi-Reference Conditioning Support:\*\* Yes. "Omni Reference" handles character, style, and structure \[cite: 19\].  
\*   \*\*Known Weaknesses for Hand-Drawn Styles:\*\* The "Niji" model variant is highly opinionated and aggressively bends raw geometry toward anime aesthetics, while the base V7 model biases heavily toward cinematic realism \[cite: 21, 22\].

\#\#\# Recraft V4  
\*   \*\*Release Date:\*\* February 17, 2026 \[cite: 23\].  
\*   \*\*Pricing:\*\* V4 Raster is $0.04/image, V4 Pro Raster is $0.25/image; Vector SVG is $0.08/image \[cite: 24\].  
\*   \*\*API Providers:\*\* Native Recraft API, Replicate \[cite: 23, 24\].  
\*   \*\*Character Consistency Strength:\*\* 4/5.   
\*   \*\*Editing Capabilities:\*\* Superior at generating editable SVG files with clean geometry and structured layers \[cite: 24, 25\].  
\*   \*\*Multi-Reference Conditioning Support:\*\* Unverified for merging multiple character references simultaneously.  
\*   \*\*Known Weaknesses for Hand-Drawn Styles:\*\* Optimizes explicitly for "design taste" and vector graphics, making it antithetical to raw, raster-based pencil grain \[cite: 25\].

\#\#\# Google Imagen 3 & Imagen 4  
\*   \*\*Release Date:\*\* August 15, 2025 (Imagen 4\) \[cite: 26\].  
\*   \*\*Pricing:\*\* Imagen 4 Fast ($0.02/img), Standard ($0.04/img), Ultra ($0.06/img) \[cite: 27\].  
\*   \*\*API Providers:\*\* Google Gemini API, Google AI Studio, Vertex AI, Replicate \[cite: 26, 27\].  
\*   \*\*Character Consistency Strength:\*\* 4/5.  
\*   \*\*Editing Capabilities:\*\* Full suite of region editing \[cite: 28\].  
\*   \*\*Multi-Reference Conditioning Support:\*\* Unverified capability to natively blend 10+ images compared to Nano Banana.  
\*   \*\*Known Weaknesses for Hand-Drawn Styles:\*\* Designed for maximum photorealism, 2K resolution, and corporate design, often smoothing out intentional artistic grit \[cite: 26, 29\].

\#\#\# Google Gemini (Nano Banana 2\)  
\*   \*\*Release Date:\*\* February 26, 2026 \[cite: 30, 31\].  
\*   \*\*Pricing:\*\* $0.04 for 1K resolution, $0.06 for 2K, $0.09 for 4K via Kie AI API \[cite: 32\].  
\*   \*\*API Providers:\*\* Google AI Studio, Vertex AI, OpenRouter, Kie AI \[cite: 30, 32\].  
\*   \*\*Character Consistency Strength:\*\* 5/5. Elite consistency across multiple prompts.  
\*   \*\*Editing Capabilities:\*\* Supports complex multi-turn image editing \[cite: 33\].  
\*   \*\*Multi-Reference Conditioning Support:\*\* Yes. Supports up to 14 reference images simultaneously \[cite: 33, 34\].  
\*   \*\*Known Weaknesses for Hand-Drawn Styles:\*\* Highly expensive at scale for an entire animation timeline. Introduces dynamic search grounding which can occasionally override localized aesthetic prompts with photorealistic web data \[cite: 34\].

\#\#\# OpenAI GPT-Image-1 & GPT-Image-2  
\*   \*\*Release Date:\*\* April 21, 2026 (GPT-Image-2) \[cite: 35\].  
\*   \*\*Pricing:\*\* Premium API costs or bundled with ChatGPT Plus \[cite: 15\].  
\*   \*\*API Providers:\*\* Microsoft Foundry, OpenAI API, Replicate \[cite: 35, 36\].  
\*   \*\*Character Consistency Strength:\*\* 5/5. "Cross-Image Consistency" guarantees identical characters down to the pixel \[cite: 37\].  
\*   \*\*Editing Capabilities:\*\* Highly precise, instruction-literal editing. Generates, edits, and restyles using masks \[cite: 38\].  
\*   \*\*Multi-Reference Conditioning Support:\*\* Yes. Combines styles, subjects, or references into a single output \[cite: 36\].  
\*   \*\*Known Weaknesses for Hand-Drawn Styles:\*\* Like Midjourney, it leans toward "Commercial-Grade Illustration" which typically auto-polishes raw sketches \[cite: 37\].

\#\#\# Adobe Firefly Image 4  
\*   \*\*Release Date:\*\* April 2025 \[cite: 39\].  
\*   \*\*Pricing:\*\* Subscription-based ($9.99 Standard, $29.99 Pro, $199.99 Premium) \[cite: 40\].  
\*   \*\*API Providers:\*\* Native Adobe ecosystem, Photoshop integrations \[cite: 39\].  
\*   \*\*Character Consistency Strength:\*\* 4/5.   
\*   \*\*Editing Capabilities:\*\* Deeply integrated Generative Fill/Expand natively inside Photoshop \[cite: 41\].  
\*   \*\*Multi-Reference Conditioning Support:\*\* Yes, utilizing "composition reference" sliders \[cite: 41\].  
\*   \*\*Known Weaknesses for Hand-Drawn Styles:\*\* Prioritizes absolute commercial safety (trained on licensed content) resulting in an over-smoothed, "stock" aesthetic \[cite: 39, 42\].

\#\#\# Tencent Hunyuan API & Alibaba Qwen-Image-Edit (Hosted)  
\*   \*\*Tencent Hunyuan API:\*\* While the underlying 80B model is powerful, its native API pricing and multi-reference API gateways remain unverified in the provided metrics, though independent gateways exist \[cite: 43\].  
\*   \*\*Alibaba Qwen-Image-Edit:\*\* Hosted on Atlas Cloud for $0.032 per run \[cite: 44\]. Capable of multi-image blending and text replacement.

\#\# 4\. Open-Source Image Generation and Editing Models

Running models locally eliminates per-frame API costs entirely, shifting the burden to setup complexity and hardware limitations. Every model below is evaluated for structural parity against specific open-source hardware metrics.

\*(Note: The user-provided glossary requires defining critical technical jargon: \*\*GGUF quantization\*\* is a format that compresses model weights into lower precision integers to run efficiently on GPUs with limited VRAM; \*\*xFormers\*\* and \*\*FlashAttention\*\* are memory-efficient attention algorithms that dramatically speed up transformer processing and reduce VRAM usage; \*\*CUDA Out-Of-Memory (OOM)\*\* is a fatal software error occurring when an application demands more VRAM than the graphics card physically possesses).\*

\#\#\# OmniGen and OmniGen2 (BAAI)  
The Beijing Academy of Artificial Intelligence (BAAI) released OmniGen2 in June 2025, introducing a decoupled multimodal system separating the autoregressive text transformer from the diffusion-based image transformer \[cite: 45, 46\].  
\*   \*\*Repository & License:\*\* Hugging Face (BAAI/OmniGen2) / MIT License \[cite: 46, 47\].  
\*   \*\*VRAM Requirements:\*\* \~17GB natively \[cite: 47\].  
\*   \*\*Inference Speed:\*\* Exact speeds on H100/A100 unverified, but runs comfortably on a consumer RTX 3090/4090 \[cite: 47\].  
\*   \*\*Quality vs. Closed-Source:\*\* Achieves a 7.16 Semantic Consistency score on benchmarks, rivaling top-tier closed editors \[cite: 45\].  
\*   \*\*Editing / Multi-image / Char Consistency:\*\* Built-in multimodal reflection mechanism allows in-context generation (inputting start frame, end frame, and character sheet via prompt) without external plugins \[cite: 45, 48\].  
\*   \*\*Active Ecosystem:\*\* Over 58k downloads for V1; heavily supported by the Shakker AI WebUI \[cite: 47\].

\#\#\# Qwen-Image-Edit (Alibaba)  
Released in August 2025, Qwen-Image-Edit inherits the 20-billion parameter MMDiT backbone of Qwen-Image \[cite: 49\].  
\*   \*\*Repository & License:\*\* Hugging Face / Apache 2.0 \[cite: 49, 50\].  
\*   \*\*VRAM Requirements:\*\* Runs on 8GB+ VRAM using GGUF quantization \[cite: 50\].  
\*   \*\*Inference Speed:\*\* Exact tokens/second metrics on an 8GB card remain unverified in the provided data, but qualitative reports indicate practical inference times for consumer workflows \[cite: 50\].  
\*   \*\*Quality vs. Closed-Source:\*\* Rivals premium subscription models for localized "appearance editing" (pixel-perfect object additions) \[cite: 49, 50\].  
\*   \*\*Editing / Multi-image / Char Consistency:\*\* Dual-path architecture allows merging multiple images natively (e.g., character from Image A \+ pose from Image B) \[cite: 44, 49\].  
\*   \*\*Active Ecosystem:\*\* Fully integrated into ComfyUI workflows \[cite: 49, 50\].

\#\#\# Stable Diffusion 4 Base/Ultra (Stability AI)  
Released in March 2026, SD4 represents a massive architectural overhaul, moving from a UNet backbone to an upgraded Diffusion Transformer (DiT) \[cite: 51\].  
\*   \*\*Repository & License:\*\* Open weights under a Community License (Base) / Enterprise (Ultra) \[cite: 51\].  
\*   \*\*VRAM Requirements:\*\* 12GB VRAM for the Base model (consumer GPU targeting 1024x1024 native) \[cite: 51\].  
\*   \*\*Inference Speed:\*\* 8–12 seconds per image on an RTX 4090 \[cite: 51\].  
\*   \*\*Quality vs. Closed-Source:\*\* Delivers "cinema-grade lighting" and correct hand/anatomy generation that directly rivals Midjourney V7 \[cite: 51\].  
\*   \*\*Editing / Multi-image / Char Consistency:\*\* Highly robust structural adherence natively.  
\*   \*\*Active Ecosystem:\*\* The standard Base tier is rapidly becoming the foundation for the next generation of LoRAs and Dreambooth variants \[cite: 51, 52\].

\#\#\# FLUX.1 \[dev\] and \[schnell\]  
\*   \*\*Repository & License:\*\* Hugging Face (Black Forest Labs) / FLUX Non-Commercial License (Dev) and Apache 2.0 (Schnell).  
\*   \*\*VRAM Requirements:\*\* \~24GB for Dev natively, reducible to 12GB using FP8/GGUF quantization \[cite: 53, 54\].  
\*   \*\*Inference Speed:\*\* Varies by quantization; unverified precise times on H100 in provided notes, but consumer 4090 runs it efficiently \[cite: 54\].  
\*   \*\*Quality vs. Closed-Source:\*\* Set the 2025 standard for open-source prompt adherence and photorealism.  
\*   \*\*Editing / Multi-image / Char Consistency:\*\* Highly dependent on third-party integrations like PuLID Flux II for consistency.  
\*   \*\*Active Ecosystem:\*\* The dominant open-source ecosystem prior to SD4's release \[cite: 54, 55\].

\#\#\# Tencent HunyuanImage 3.0  
Released in September 2025, this is an 80-billion parameter Mixture-of-Experts (MoE) model \[cite: 43\].  
\*   \*\*Repository & License:\*\* Hugging Face (Tencent) / Open-Source \[cite: 43\].  
\*   \*\*VRAM Requirements:\*\* 24GB+ depending on quantization; highly demanding as it activates 13B parameters per token \[cite: 43\].  
\*   \*\*Inference Speed:\*\* Utilizes FlashAttention and FlashInfer for 3x faster inference, but remains heavy for local execution \[cite: 56\].  
\*   \*\*Quality vs. Closed-Source:\*\* Rivals DALL-E 3, utilizing Native Chain-of-Thought reasoning \[cite: 57, 58\].  
\*   \*\*Editing / Multi-image / Char Consistency:\*\* The "3.0-Instruct" editing variant natively supports multi-image input and local editing \[cite: 58\].  
\*   \*\*Active Ecosystem:\*\* Nascent. English prompts work poorly, and community ComfyUI tooling remains unstable \[cite: 58\].

\#\#\# DeepSeek Janus-Pro  
\*   \*\*Repository & License:\*\* Hugging Face (DeepSeek) / DeepSeek License \[cite: 59, 60\].  
\*   \*\*VRAM Requirements:\*\* 7B version requires \~24GB VRAM; 1B version runs directly in WebGPU browsers \[cite: 60, 61\].  
\*   \*\*Inference Speed:\*\* Training required a cluster of H100/A100s, but the 1B variant loads 2.24GB in Chrome \[cite: 60\].  
\*   \*\*Quality vs. Closed-Source:\*\* Achieved 80% overall accuracy in GenEval, beating SD3 Medium \[cite: 62\].  
\*   \*\*Editing / Multi-image / Char Consistency:\*\* Input resolution is severely limited to 384x384, preventing fine-grained detail retention. It struggles significantly with human faces \[cite: 60, 61\].  
\*   \*\*Active Ecosystem:\*\* High interest due to decoupled visual encoding pathways, but lacks dedicated animation workflow nodes \[cite: 59\].

\#\#\# Unverified Open-Source Models  
Per explicit filtering mandates, precise operational metrics for \*\*Stable Diffusion 3.5 Large/Medium/Turbo\*\*, \*\*SDXL successors\*\*, \*\*Sana\*\*, \*\*HiDream-I1\*\*, \*\*Hunyuan-DiT\*\*, \*\*Lumina-Image\*\*, and \*\*PixArt-Sigma\*\* either lacked complete VRAM/speed data or were entirely absent from the verified 2026 research material, meaning they cannot be robustly recommended over the detailed models above.

\#\# 5\. Identity and Character Preservation Techniques

The base model is only half the battle; locking the identity of "Sean" across hundreds of frames requires specialized conditioning techniques.

\#\#\# PuLID (Specifically PuLID Flux II)  
PuLID (Pure and Lightning ID Customization) has evolved significantly. The ComfyUI integration of PuLID Flux II (v0.9.1, October 2025\) is currently the gold standard for zero-shot character insertion \[cite: 55, 63\].  
\*   \*\*Mechanism:\*\* It extracts facial and structural data from a reference image and injects it via contrastive alignment. Crucially, PuLID solves "model pollution"—the tendency of earlier IP-Adapters to force the style of the reference photo onto the output \[cite: 55, 64\].   
\*   \*\*Quality & Complexity:\*\* Setup in ComfyUI requires the specific Flux model, clip, encoder, and VAE, requiring roughly 12GB VRAM via 8-bit FP8 \[cite: 53\]. It learns a face from 4 images in less than 8 seconds \[cite: 55\].  
\*   \*\*Animation Fit:\*\* You can provide the pencil sketch of Sean, and PuLID will preserve his facial geometry while allowing the base model to adhere strictly to your text prompt regarding lighting and pose \[cite: 64\]. 

\#\#\# LoRA Training (Low-Rank Adaptation)  
If zero-shot methods (PuLID) fail to capture Sean's specific clothing or pencil-stroke style, training a LoRA remains the brute-force solution.  
\*   \*\*Data and Time:\*\* Training a FLUX.2 Max LoRA on a consumer RTX 3060/4090 takes roughly 20-30 minutes \[cite: 65\].   
\*   \*\*Best Practices:\*\* For highly consistent characters, a dataset of 15 to 30 varied images is sufficient; 1500-2000 total steps are recommended \[cite: 66\]. The learning rate is critical: for FLUX.2, it must be set to 1e-4 (0.0001); higher rates will "fry" the image \[cite: 66\]. Captioning via BLIP remains essential to separate the subject from the background \[cite: 65, 66\].

\#\#\# Cross-Frame Attention (ConsiStory & StoryDiffusion)  
Techniques like ConsiStory and StoryDiffusion aim to generate multiple consistent characters in a single batch via shared attention layers. While powerful for storyboarding, these methods are generally better suited for generating disparate scenes rather than smooth frame-by-frame in-betweening.

\#\#\# Unverified Legacy Methods  
Methods such as \*\*InstantID\*\*, \*\*DreamBooth\*\*, \*\*Textual Inversion / Pivotal Tuning\*\*, \*\*IC-LoRA\*\*, \*\*AnimateDiff\*\* character coherence, and \*\*Reference-only ControlNet\*\* were evaluated but lack verifiable independent benchmark data for preserving raw pencil-test aesthetics in leading 2026 pipelines, and are thus classified as potentially superseded or unverified against modern Flow-Matching alternatives.

\#\# 6\. In-Between Specific Workflows (2025–2026)

Indie animators and major studios are converging on hybrid workflows. Pure AI frame-generation often suffers from temporal flickering, leading professionals to combine neural interpolation with texture tracking.

\#\#\# ToonCrafter (The Generative Interpolator)  
ToonCrafter is an open-source video diffusion model fine-tuned specifically on cartoon and animation data to interpolate between two static images \[cite: 67, 68\].   
\*   \*\*Capabilities:\*\* It extracts pixel-level detail from input frames and generates seamless transitions using pre-trained image-to-video diffusion priors \[cite: 67, 68\]. It can support generating videos of up to 16 frames with a resolution of 512x320 \[cite: 69\].  
\*   \*\*Limitations:\*\* Because it uses a diffusion process, it fundamentally generates new pixels, which usually results in the pencil grain "boiling" (flickering rapidly) \[cite: 68\]. It can also consume substantial VRAM (historically up to 27GB, optimized down to 10GB by the community) \[cite: 69\].

\#\#\# CACANi (Algorithmic Assisted Tweening)  
CACANi is an established 2D animation software explicitly designed for hand-drawn animators \[cite: 70\].  
\*   \*\*Capabilities:\*\* Rather than using generative diffusion, CACANi automatically generates inbetween frames by detecting keyframe feature points and applying vector-based stroke matching \[cite: 70, 71\]. Version 2.0 introduced stroke occlusion and tapering, allowing animators to hide stroke sections and match stroke orders across frames seamlessly \[cite: 70, 71\].  
\*   \*\*Animation Fit:\*\* Highly valuable for producing clean structural motion paths, though it requires vector input rather than raster pencil sketches.

\#\#\# AnimeInbet  
Published as a deep learning framework to solve the blurring artifacts inherent in diffusion-based warping \[cite: 72\].  
\*   \*\*Capabilities:\*\* AnimeInbet geometrizes raster line drawings into graphs of endpoints, reframing the inbetweening task as a "graph fusion problem with vertex repositioning" \[cite: 72, 73\].   
\*   \*\*Animation Fit:\*\* It effectively captures the sparsity and unique structure of line drawings, making it theoretically excellent for preserving pencil construction lines, though commercial UI integration remains nascent \[cite: 72\].

\#\#\# EbSynth 2.0 (The Aesthetic Savior)  
EbSynth \*does not\* use generative AI to propagate frames; it uses a proprietary pixel-level texture synthesis algorithm. If you generate a structurally sound in-between sequence, you can manually sketch \*one\* hero keyframe in the exact pencil/cream paper aesthetic. EbSynth 2.0 will map those exact pencil strokes onto the motion of the underlying video sequence without the boiling artifacts of diffusion.

\#\#\# Studio Case Studies  
\*   \*\*Netflix Animation:\*\* Precise proprietary details of Netflix Animation's internal "physics-assisted keyframing" remain unverified in independent practitioner forums, but the concept generally involves using physics engines to calculate accurate fabric or hair motion between key poses, while human animators retain control over the core character skeleton.  
\*   \*\*Unverified Pipelines:\*\* Specific 2026 workflows utilizing \*Toon Boom Anime Inbetweener\*, \*Cadmium Cel\*, \*Toonstar\*, \*Aardman\*, \*EISAI\*, and \*DAIN\* were flagged but lack current verified documentation regarding AI integration for raw pencil aesthetics.

\#\# 7\. Recommended Pipeline Configurations

To replace your expensive Nano Banana 2 and GPT-image stack, the following configurations optimize for your 16:9 pencil-test constraints.

\#\#\# Config A — Best Quality (API Hybrid)  
\*What comes closest to NB2 quality while lowering the ceiling on cost?\*  
1\.  \*\*Base Generation:\*\* Extract the structural motion guide using your existing Seedance 2.0 workflow.  
2\.  \*\*Editing / Generation:\*\* Upload the structural in-betweens to the \*\*SeedEdit 3.0 API (ByteDance)\*\* for regional auditing. Use text prompts to fix anatomical errors without touching the background.  
3\.  \*\*Aesthetic Lock:\*\* Feed the audited structural sequence and a single hand-drawn hero keyframe of "Sean" into \*\*EbSynth 2.0\*\*.  
4\.  \*\*Expected Quality vs NB2:\*\* Equal or superior. EbSynth guarantees the cream paper remains static. SeedEdit matches GPT-image's editing capability.  
5\.  \*\*Estimated Cost:\*\* \~$0.007 per edited frame via SeedEdit (an 80% reduction from NB2's $0.039) \[cite: 9\].  
6\.  \*\*Failure Modes:\*\* SeedEdit may occasionally misinterpret stylized pencil sketches as noise, requiring careful prompting.

\#\#\# Config B — Best Value (Open-Source Interpolation)  
\*Biggest cost savings utilizing community tools.\*  
1\.  \*\*Base Generation:\*\* Generate Keyframe A and B locally using \*\*FLUX.2 \[schnell\]\*\*, utilizing the \*\*PuLID Flux II\*\* ComfyUI node to lock Sean's facial geometry \[cite: 55\].  
2\.  \*\*Interpolation:\*\* Feed the keyframes into the \*\*ToonCrafter\*\* ComfyUI node to automatically generate 10–16 structural in-betweens \[cite: 69\].  
3\.  \*\*Aesthetic Processing:\*\* Route the ToonCrafter output through a post-processing filter or EbSynth to re-add the construction lines that ToonCrafter's diffusion process smoothed out.  
4\.  \*\*Expected Quality vs NB2:\*\* Lower initial quality. ToonCrafter will blur pencil lines into a digital look.  
5\.  \*\*Estimated Cost:\*\* Free (Compute only).  
6\.  \*\*Failure Modes:\*\* ToonCrafter struggles with large, fast motions, creating ghosting artifacts. VRAM spikes can crash GPUs if frame counts exceed hardware limits \[cite: 68\].

\#\#\# Config C — Fully Self-Hosted (The 24GB VRAM Workhorse)  
\*Zero API cost after setup, maximum control on a single RTX 4090.\*  
1\.  \*\*Base Model:\*\* Load \*\*OmniGen2 (BAAI)\*\* or \*\*Qwen-Image-Edit-2509\*\* locally.  
2\.  \*\*Conditioning:\*\* Utilize OmniGen2's native in-context generation by placing the start frame, end frame, and Sean reference image directly into the visual prompt \[cite: 47\].  
3\.  \*\*Workflow:\*\* Scaffold motion locally, using instruction-based editing (e.g., \`"modify frame 2 to match the character in image 3"\`) to iteratively generate and fix in-betweens \[cite: 46\].  
4\.  \*\*Expected Quality vs NB2:\*\* Slightly lower out-of-the-box consistency than NB2, requiring more iterations to get the perfect frame.   
5\.  \*\*Estimated Cost:\*\* $0 per frame.  
6\.  \*\*Failure Modes:\*\* OmniGen2's documentation notes in-context generation sometimes produces objects that differ from the original; increasing the \`image\_guidance\_scale\` to 2.5–3.0 is required to force adherence \[cite: 46\].

\#\#\# 7.1 Preparing AI Frames for EbSynth  
Since EbSynth utilizes pixel-tracking algorithms rather than semantic diffusion, AI-generated structural frames must have distinct, high-contrast boundaries without "boiling" noise. Animators must prompt the base diffusion model (e.g., FLUX or ToonCrafter) for "flat shading" or "cel-shaded structural outlines" with zero grain, effectively creating a clean UV map. If the structural frames already possess simulated pencil grain, EbSynth will mistakenly track the random noise rather than the underlying object geometry, causing the texture to slide or smear across the canvas.

\#\# 8\. Open Questions and Unknowns

\*   \*\*Pencil Test Specificity in Base Models:\*\* While models like FLUX.2 and HunyuanImage 3.0 demonstrate vast artistic range, there is thin independent verification on their ability to natively understand and maintain "hole-punch marks on animation paper" and "visible construction lines" across multiple generations without treating them as errors to be denoised.  
\*   \*\*OmniGen2 Temporal Stability:\*\* BAAI's OmniContext benchmark measures spatial and semantic consistency beautifully \[cite: 45\], but evidence regarding its temporal stability (flicker across sequential video frames) remains anecdotal in practitioner forums.   
\*   \*\*ToonCrafter on 24GB Limitations:\*\* While ToonCrafter nodes exist in ComfyUI, the exact upper limit of frames that can be interpolated at 1080p (16:9) on a 24GB card before triggering CUDA Out-Of-Memory errors is highly dependent on individual setups.

\*\*Sources:\*\*  
1\. \[bfl.ai\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEgHh7Wvy5mD1Qk3LD6XCJD4lY4QHjW7TSFbCl4Uk8nOe-7gY\_zd16if\_jWh0ec3KQtWlb6dZ8vW1sV0ZJVDswfaRg7LHv0tmyGvv-qB7ailcXzzk8zGgbCSEcwCf\_HhNdw)  
2\. \[bfl.ai\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEzxYYIXGnbB\_e7CDDz2l78f0tdwQvXuCMvEntOLKZ1J7fM4EY3mX9ql7zFNjY19s-6FpMuWNHAjAQ5zw8tHWVwJwNun2UHZLzBHy6ts7AESDddKiJn-1Mk)  
3\. \[bfl.ai\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGt2foFy1yYCFTaadLz4U29xI2VpH3i2K7LfELd47c\_BVs6NIeRmBXa7eIlwVnmp8mtz\_sqMWlaooo6TzN6PzGgCH4xY1q4AwHcUVsXl\_4qnQso)  
4\. \[venturebeat.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFGtShfyDJD3LarGSs0JVJmdgvhdDy90fkLmIdoVZLY4rKD4fLSdDujTFVjjleEmp9A5Xv3vBOZlLAVliCgTjmVwkqxrPAmYgN5P29jAHW3jqM\_HO0ByeMyZ44WUyoVVVmFgVi6cigpVOWayDCYD8MeACgaV96mCgHqwrGH0Ts-RWpdIyRbDeXVYnkYnyroDwoUzOAuYCbh4xVPKw==)  
5\. \[replicate.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHSINqDTcHkJ1upoboASdPm6SfrZ6wmZyc1vWLIznfKp2APATIq7VD7uL9m95yGctCUayKnu5O-ijT0my6Xs27Hzl61g34wv3pR6bgUST8BxM6EZyXfieXbzKhHLj2mlGwYh0yc9WR2Mw==)  
6\. \[cloudflare.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG\_qpaZgrAlGQnPxXZO-sm6cvmFNU6Qu1xJv9kCwKApGWDNphSZl4TVlkpDxf-GN\_AzQCjIxHYzZ\_8yo-KzSJBBRjps31ONUUEl9RI55USyGhlq8Ha0UohonByeXyoQ9u3TukpZ)  
7\. \[microsoft.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFpCmlSXQY9wYCqSzH\_XrUO439-33wjy9nSxd0ssQHTX1637CbQ3as89Mt2YjMCgWemVgn0fubF39HZdH0KkR80LAcb8kJfF0RWHIQgHeRzVIq-WEv8wYHLmIMpbdANbYHl\_dRs91DJSYgDuYoPBtNAgSM8QjkrBC7UcMQMMJCq4b1Z9wf9nriTOH0BAZahiWtvkCUDHp7ingzwQoDRse3pAf-lq2Ny5Lr4pPwg2wPBkdU1LTl54Ezgtw8nnkJmT5-li-xgjXf1CHPy3TCuXw==)  
8\. \[github.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGyrcEOzhI38744NW\_j\_5DCOKzeRDNKFcSk82U6UEtrNLWoD0k108EfIfqTL6RHM14NhzC-5tn2R0R5ECUq54yPbaxkVXg601mqTtMIsJAGFEsbV41-oCX\_qj52f2gjfaw=)  
9\. \[medium.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG2bjTDI47OeYpuRgWXfDQI-M5eQ-HYbQqhkRdWXJ6jZ5vZbrCOI2VnkBSpwCtcWmQIpRRC3dCRiTpi6TN00fKWG954gNTC-ce5Z6-LB6ajS9w2Kf5cm5WeQHO\_DSUhGmanY\_4INafV3K7cemk\_Qxyh5JSAchdu7adNR8Saiu4dOJ5MluepI79FV9X3jMO4pR3rrx2LKolnei0o7qfdZ3H4omFJGGcf30LGCio=)  
10\. \[bytednsdoc.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFo6e32ejxEaRZxMcy5gr2ghPsjoFOhypzD-h6TBou7OiRIB25Aw\_NkFvkMIO95G4uZvBcH8oN9z\_IFli41Pss8z8ZMWCnMpeIm4TggsEKQHx31B9HoEcf9ZYHiE7y9JArxQMSYed43SSCP1EFEFUgdxzhxPmNYrsASko3Drub1E\_I3OOdfqylISsb6HZxLmX8=)  
11\. \[seavidgen.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFIgczKCcsx6zB1P7CGVMaNQqQtKEhdFWLdoli5s\_NC19VORozKRyWwAL0mHBwff876HngXZ32CmIkjNHLQw3YCSqRZBf6GsVQpgDW\_TSOq4E4dw4A=)  
12\. \[bytedance.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF3iLeZe-TVcxje2jS-Nych6\_G5o\_SgI-iOrJMX95w4w9thFSfTVrg5dFSmonzjisAWpmKajjcugdCJDruxKpT-VfT1w5l1ipXwzLP5w9bmDOlsuH4YdmqWmEXBv\_nG2Gmd9E8K3Acy6ctf2kxrmhsF0DPuW2tSibGRUWJ4uN1PUWJYv3u2caAEda3TS0LTLoCMsS9NGE2d7kZX)  
13\. \[eachlabs.ai\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEy59C5E2wI86E9cFMdlaS9OXbCWGP4SZQJgu4V5YD424nKqFXmGE7\_CYDYnzEzwyHBUozNoCiCSX\_fKQY1k49Lcgn0Tq1juTRBal2bOOJXqehYpfzxexleJp0apNQ\_3iaMvCGGQhHP5ZkkPeQO)  
14\. \[wikipedia.org\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGI2zvbCdxRhJRUxMDZU0KToRlBxuIAdSgLX2UUxDWJsknJQfF-QcDK5WtQipFdhAWmJAoXizHv1tbM5UwQnzSZhyaqoKGIV5SzmgcAHbmS5N1pDquU4rMCuzUHHxOwGwNFRJyYN0zc\_\_OPtuqCupr4OYE=)  
15\. \[getaiperks.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH41OXu4OyTZd9sN-F-yvO3n8oIaLqAw7FTv\_W4OTpQjGmCAhQdax1lcSkz7w4IpCJe1md2quQ1dTJt-aGvTz5q6U4dVdSfQGBlv5EIlr1SQChxICbjuIOZu1ICWmLiwM9dLx5R53w8Am3LajCkutU1ff085lH-kUOtCw==)  
16\. \[the-decoder.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGWUM3fLWD3DNVReVqU7vdOJ0C-ruFhbJkMzBadvhkgmSJQLr1ZHQ4xg0v0XDV47-FzaCkolRjQVEj5J6oiri6LFJvWTgewSlEXfEqU-eUTVXor6o89YvJkjEgE2\_JF91KpR-su3wObqYXdUYy-AtC-UWZ6-KCYP4IpSakTgx1Ey3D8p\_vMp4CHfkJVaa1fYEVGcrqZKkFu-aKQ)  
17\. \[ideogram.ai\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGzqt1t1x\_dG0w56AC36c0ec99Dl12DaqEXS7Gb7xB0PvCvOsWLFBT8hiwF5zuWWr4SMoz5-pwKJWUmlg0zN4U6KTyr4aWRQ7z7ATQfsySPCaB49yqPSsk=)  
18\. \[reddit.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFqMV1nTmllYNjKxBqk4HQRw12XA0cLEApqhWAAVmCxH5B3A6JZ-PLGBjRUoFBP40KlY0dJLUDtUTpTqDaLfdrMxx0Rl\_RQ2pryem0YT9qP\_vC-IyfpSbHefgqSR8QthAdZQOC5RF7gKylGKWWfyRCRIseLZJSVy\_9SmJ4nc0pFug9KXltF7xGi)  
19\. \[youtube.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFTeIM9ZQKeCUQ0dtwh5Hwl-6CPw5rtwcqc8i2nfS3mnZIk8mXeDO-bnHHTqSEc0d4BWdawxVA4kZ3behr9T446rxHjVCRQFePg1-eFJyWhFOIcLii4DW4ip3snDf\_ZGne4)  
20\. \[unitool.ai\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGYVBYtLwlxj1Ad1Q0ilPF8nHLRRWOE6\_L0x1PPtZ\_QaoEyI9ocsmyfNyvUqBqXSIVVxISRkIvLcEK\_KHcfgGFH0CnBELTtZDIR8u9WzmJSWQBxBoH8Hg==)  
21\. \[youtube.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG\_j-Dw6UHVi\_2KCIxmFCbqZWn24T5TCsTVHa4sOlIUqkxR-Z0S4hovSB4mKTyjeHvfEUq\_kkUfAdrwX4vFtZM7SVy1Urb2I9HFlLkaWvxi1bGR-zoNqNcWAxspO642OQAD)  
22\. \[chasejarvis.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQERHTxzpiybxLS5PAOHNs3VNh5b8whxpXy5pTMin6LZCNw-heBGcTNOmw9Tgr2P-iN\_esT40ENIUlb\_QJW9xhVdcp66H9098Y7t683joLNfmQFw8t3i1dY7fqdT-fI-8QKSx8nTM9KVGnQOi4h52JTykTSnMdm5nx58D26eo9FCtby07doRQC6y6zsxKoQ\_APsX)  
23\. \[recraft.ai\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGUIPv6WTJNisnhJh8hc7V6xyg5uKl926eIg3q926VDYtWVxFMg18Lw\_HrFVCUa9-oe\_371FU9-jrKE2o9LsZXTjxFQDCLPzdLBDHHvt3zeiaoU7URLcX3FAGSWhfojE7HCIa3SdJXJ8V5dJZMtU9O4SDNri-q3tTCdBovAOK83DR5XtXdIoSBsDzEvOg==)  
24\. \[replicate.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG5hF4GyXl8y-IJbcYEW2fOUCrzC91VQtb13HFTJK5iLt8NMA6UhyYlhSYUjx6ZCSh7LnT9YSAXc12zU7O8X-8Ox9Du1EePQl8t9rupg8zMpb5qL07soodGd7J4)  
25\. \[picsart.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHsebtP6Oo1A60ixhLPoH\_8NMETnbZHz2JMeyxmIDr2vsLls6sZ9JhLPS4K6KPeS4emY-57sj7BISfztrZXABpGiJSl\_mjU78zMdA98IZFwwwQFnaWDr53hvqmL7iMxwQ==)  
26\. \[googleblog.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEswFRvtJM8QdG-9wqZqhhfPVtNcRiA3c6fdRSSNV5de9ry0MJaKGHt6P3KS4rRAoiKJzA6l3xqN1jzKrDKnPl1A3gTWeNZYJoQUtjpBVJ-h4rAgx2\_vv9TjTS2hAb9SKu5im6bOU3wltQVIOWL8zE2tydtlGQxhfoXrEqMydfQHSodaafrWacW5qkHragwOAjxEk9HR18yqtZ07M5SjQd2TavAGSPXvdSbYYY=)  
27\. \[mindstudio.ai\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGBWIIkw9x-yH0RU12KHIFWYRj0Q8eL\_mCnfgNg63WlpJOOWzXaxBZVKMnvBVRtsPKAhKogjAT--PoPokT4Hjer1498zT13BDrhpSLsuaI\_MQFzXIfQEun6NgMgmTYXWM4z-AO1rvs57wG5L-kKcLM01Q==)  
28\. \[replicate.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFH7fydhlVqsW05ym5sIhkAyhkkCSwrA4VgFwkTPhpSBL98wK6BbsWnw9wIiCL2kDyNU5I3mefijy0rIpQV3K5P8hBu2kdNxblzBuHvc7CbKXX-e6hmvhEBuGLB)  
29\. \[deepmind.google\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFal6jj9kBHiO6Exrb6Dwz8tBvD8xXILSaQchVRJIn4zwAJ0JPxEli6nqGuWKJT7ieo1D4pqTttmZwanzb\_UANmEUPJQ-UBlJWXVX0K9iSyQXCVL7mZkUmhdpVacQ==)  
30\. \[blog.google\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEtkPnSdZunYuXAd1nBwZ\_z5bVQWCTiRQtV6imF75ZImwU0GXvWafl\_0q63X5vA9h5eST39mfV7xp7GQezBh5dg9LTtwbb1hsMFdBrBSCLuanafBoUvWCl\_uTj2FrqA2C\_YJAB5A\_-ZkyCUED0RVB7QQnE5ga7yOCiofWJffXhTpPkkfHxUpwmG3wm04PspDeSw)  
31\. \[openrouter.ai\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEeZWHXvU6vncC7mOP\_c4HowVFkRxW5tIsUBVYz501klT7LJsvhUzfMn4UARvLEE9AuxQ3bpMdB\_vL-79XUqNpo00StVW7WBIc7L6\_cNVESJBLm8znJoaRtrYnvE8eQDc5RpBT4x-Ws8E8vAoS2R0MWoA==)  
32\. \[kie.ai\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEa18isufLKJjGUBvxxla9\_7CfZ89pXngRGccF504-Yu8VFYZDkfTWpgRnzY4kFcGBiltVNq9hyW09WFEp2A4Vr9j2xntU\_ptfn9hbBs0k8oRXv)  
33\. \[google.dev\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH7N\_aTbN89QgnYIzdE-qkcV5TOMjkyqmBeme2d68OoPeQlZTXsx6y8S3BjUrsvumowGe1\_W0nGueWiwCNXfSJqkZvkjJaSli3rjYYNwZ1ZOIq7dIvHcktf\_HFkMHm0uE8P2qhUUl4scLVypAg=)  
34\. \[philschmid.de\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE6jkJRv2ufPT2-aGhsw1ELR86oJ1elJ7LZf8oi2kmCT36rmxBxQAqzLIQtoY2QrwZhYq1aMLAwp\_uZsB-7BdwQulE19mDA7SDwkQGE61NgEMq5jmo33CjsGD5MdUjrdCFkpHOFxhwcQRRT\_dD3AQ==)  
35\. \[microsoft.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFXY\_D0UF8efZRZt-oCMTTnR5-G-cZLebC60xZGMn6fBKrdmNRBXmGazSI0U7mlLBWUKwDid-boN-fY1aLKgAfKP3mlE\_SSq9h2P1K7xPXdLaf-h43ZOE9rYsoVmOZNvualONc9SP\_-aUOxAUNcrBQPbhVfUQfCs24ua6kbDVF98L232BmnDYffKsD0oJm2wcap4EKtjkp3gqBFO3HxiAdBkRtAlDGxy6OeYrn0UvhwOTU=)  
36\. \[replicate.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFuD9aBH4pu7gTEG4qWYTu3A92PfM-7zTUPpjLtGkAbdbGL10b804nID2qDCtbSGOjbp4iRZsMdM2\_oxlGDkXSJRDFN9y3aOqaaSkV4zl6H5AfbKYudal2m2s0FAP18)  
37\. \[github.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHF9M3741iX9zXvTAvtnFHbqromwCNJqThTdSWUG5xFW4J9urNKKbStsGpFFNQNK5e7IqYy63bLPOq0TEMPWSqawZE-QbWkaZyTcu9UW3BEhV3vKfJf2Yf\_xWwbvbmOYb0gMpocB7c3bFYeSc8=)  
38\. \[poe.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE9oWsIKHnpBXKTJ8vHowvG\_56lIdTD7e3E6Pb1FB5vtxSM7J8jlew6RS3JtMZzRPILanPXXtMRpeR5dvshLVxTYxiKSG\_GNc2yWKIFC8YoQas=)  
39\. \[wikipedia.org\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHc1sV4XNk\_SJLGvmK08dgiE6GjBdbbNyXZwJgbuR5TNvn05RHycUDX9XNEEKnrL9z3afNzty1dQmUeoLogdZs2EPuDp7xvxQtCzwU6wSqJqSv0i2FpWh7ZAW6jxIoT6YkE)  
40\. \[aiandyou.org\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHXO6Wobk6bvvl4ALS0PRmjsiPFDz6haWsoRLNiXKa8B\_XmrOMnF3IZT44hJeYz6JLEts2DPd29nONGsZT7eFD6wQUJq45fobF\_31Lf5a2eyTs2kEKKorKlasSgqDms6MzyYB4OhnEXLnog5ho8SjWOAdGijiCXUAqpM81lqmUiKraBVr5iCYBNx44DC7Tm)  
41\. \[youtube.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGFzFvlkPkC8cGij1Pz\_8Ox\_auqimvG3kNnrl7TKa0IEn5vzSmIjWMil-4Iv7vPO5rfY9qiFwwX\_lHNvXJFZbyo24aOnMDAIaC3OIcnoyo6t6asXoKacKLk4SVHhZdCtEUV)  
42\. \[aitoolssme.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGV39UCWIf33pDq77R3uqjZ6l7ux4-Qio9VNxukTaE\_EbHhcYnyrlU8H2z93R2OEnDpDZWLNeWWhtseU8PVyCjb88jm2fNLbsGXPlMnDhEy7KWMheYuD9D9In8Vcou4kXJlReJq2yE4r8uxZE7hKSGAaCWTCk4KvTbh)  
43\. \[dev.to\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHtePU\_idc03VEtJXH6OCDLi9KlMQSSiAW7hQj1QeVflPgxnN9EUmf\_YYnk2g080zSKj-PUJLaEOuA7dGxq4TDsDkONuEelBr1wWOjwWP4CRV8\_UlqzbQ2kXXxF6hbHGJZwodddifnYlEI8roSLsbqoaMd3HPaULXMjuiEIc4Mq\_qJyn9rMkX9jO6wLgRKyUk2ybqDHxXQ98Ed6IvlclfNI6TdTszKz13y9gSSV)  
44\. \[atlascloud.ai\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFCNvbmRD\_bL-E61ww0NHvjbHUrJFMQmq5bVHywnqP2a4VAiN0x-MvEU0vQZPAgOTlYRdVEBjFe2d4cTATiVVhLyOtIhQYIGhTLdJFmJaMwGFwy0CPwtvFPnDbpWFlZw6MtmckP75fNROTQMO88lQ==)  
45\. \[marktechpost.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGs8bQHh7kD9kdBsEiNbyXUfgo3NuD-JmqIwnXSv0TQVhjiG64FoiBt4SXgsq9lAa-e8tKJ2IHOWTGro1kFZohcr\_URQZXz9JWguR8jM4ez2tN5Z7ZQMH4FMIfJbb3YdF1x3GyAbah35oqOvri3yghGmlr3fAT4R1j2JUmjWs6jW66S\_dYuwLLYU8tuqKAThr0etTg5P\_LhXBY\_tCJhj3HAwvk3DK5nmDqKNM7WwFjegus=)  
46\. \[huggingface.co\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG0HDtYeoxGHgPwHwEi\_hOskFyYgIZU94LyL5ssewB5KQDIS6-sxG-ImQ5AF4jfyK\_ydgUZaNixk2fRtPXfXff\_4ONtqeQM9cqqwplZbt7SZcNANtD0rmBGKkY=)  
47\. \[shakker.ai\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEDyxIvInr9muiGnDbwozkwIjHd23jL\_1ElvyaXovs2LSJ-Y-bTjjZJwF8JI4TiQ\_zoObPtn9rldnLCwhJf2u24Av7VKaaH4jQLd1gImBTGlrZ3mBPKmYKs0cdFvCEqMtztDwzHf1o4lhFqjif1njeg)  
48\. \[skywork.ai\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGsNi1JlaUZzgVXVgvGwswBz28L7KyKhK73CJP\_HXLh3BXYhLMQ1NwCMdq7AKYlpNuOMnPITGfbQqtnciRQ3UVbexgTzxzPzIH\_YVxsrL5zu3F77zkHOhSUMLJL8kfHgAWjWlL\_s5D-p910xfiC5E8ugWvPdmB3gmv9PyVnRqjl3\_N7DnvSQAZPTlNraIwNtxxzVCm6rBU2aSM=)  
49\. \[medium.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGTu-qtSl14UNs5ZbFfEi35KsQBIQwJaMpOkIlzn-V9EbB58ZEx6VmPy1OnuBzPnAh3W9fl66NRWz0tyLXGKGlZDsMeP3i33tRms2phjoirmn6p0fV1YVODEWOeqo6bmWfsFzniZhxgKK-093yMR-i6YqSD8RFcarbTtEeTZLj9e5msAEznIfefVbW9hCeb0FwTs1KaBd\_qchVvg1B-F3WverHMVB2Tjpz07JtQ)  
50\. \[reddit.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE2jXUh-TSoI8pyYnMbaUUZ3Uyo8m6DG8tMmfW41kfVPuko0YgxzadU4uVliA0-voWggwZKYlsb08tc2GymfRrBHGd5nVh0oi31N0j3-ykkTU29UH40sV5r7OHCOuTMsFK60KoMTOHI01eN4R49No7VpR0D5jAAE062pqmBO-aSA4P4re6uwGDkHRkoWMxdclhv0M56uKDVIhayAxL2rX\_9aQ==)  
51\. \[udit.co\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF6-YLYJ91sF0FNnhCIfQrcvv\_kVrmpEXIg3TLqxPbNofyC3FfDYVD0GfgZLHMYcYN26FhnnDE3J8ecvGuhMtMTT14XzLRTrbaeK3F6Qr4-dZQRfa4Inrx7LQZ34ngr\_X3BfHAUPD8GvR4RTyoJiufAWiosPe7ExPyrgwg7cQ==)  
52\. \[lovable.app\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFA81kPN\_jt2dGVmTH3iLgCFV1AQoOeavZGSv34ueK44sAu5ud9fZuNNIt38rb9y8Yl3s5QsOMiVlcVM9g5kEicrptd8A\_mQECFfiuDk2CKfAeqVQYEx3lNqvoG\_5uwD\_3kxDWTFfkGXSl6ypjpGbbWA-H9GtI=)  
53\. \[github.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGSWFl0WDERis4WzQy6YvaWGOBLnwYqquS7Knv6CmMFfsOwHUZT8BzA83J4YmemvOBPhkNLYDql\_URFd-9WSy1-2ggK2TFi4C\_n-NUFWQJfoYfNWED9Tcl6CNOJlrxmLX7Bup8=)  
54\. \[comfyui-wiki.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFl\_sHJ7vf3koy5lKrg1RjccbPCkDX\_USo9azldvsYlZEnx9VNwvCpFxFesiKj0ALnfTr5-7C2DTiancS7bdr0aZToK9EXG4zsVjwxLms666JPQBkSnkhmGTgOgzNjA2IlwRldKz-rc8-iKFZzKjPHAWOo\_1yh-qut3kasTr\_K3TJau1Q==)  
55\. \[medium.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGNy56UNZ\_G0Ry-SXK\_YyL4LUdBnwgUovrLp--dhNjxchOLgvSyO67c8tmN5ENEgLamauECgHHVb6Lm4skSp2pD--fF\_WMAsoXPo39zfzT1W-1Hye4OXtfQprOOiwGAaEJ7rZrMv5vFsg6Fzv4xc62qdSNVgVm2BShn1siYZxmT\_tbIWDv4v68rqDaS7u6AHA==)  
56\. \[medium.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGR87OV4gXJBRCH6rYf9yaG0FF33ZKJ02TvcFODMNnDQz24teSvnN60kbYPXfpAz0WBhLW5UBFYlWne\_SyQS79S40Kp7ExaYOOA\_yHYVtw-7vh19g8FQ0JMpK0ve2YWLIQHTAxQ8UkZiTcVrQ-WoYF64qNKpWFO\_MYw8s2WylTRaYgBclgLloVdm3U5TY06d0nftwK5EzctBBAyFgbgy4f8gObXxBmmpA==)  
57\. \[replicate.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGEE2nCMkdYiEu-osGJdXdFgpCCVCVHoP4Oj8In6qo2uuRnaf9M-r5TDX8WNVXe6Cf8ZRbHGembTp0mEH9nKKXfeahihx27jO-OE5FwAaNGibM-hl6IY2VG-YtnNq0jQRai16I=)  
58\. \[youtube.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEbYsZIgK3XpXyKAEe5KwAMYE7S58fqCJI7uyJ74nDmoeOcMRBPdl\_oWwTrlRhbCAT\_0k9tL\_mORqWAFlk5fcL-3jl2E4zDNmhrdgQfWLp6BY\_eezdTZFmFwr4SF6JKtiVL)  
59\. \[medium.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFcgaGGl4wMgn7uKz6Pv0WP-eGN98O7avmS7pQmD8MDsAY3PwuW\_tneCANDUoaLcRe3cqEmEwTSPbQnJg8Shz5pjRUeWuFQvxr\_IAmBlypSYARCt4qWYRpZynkH67fQfcZ5ybzhmbUjKD1qLIgqnRlUHwirEyRpgUBIEQwdMEKAIauuWaLqAx3\_gzpX6k1kS1I3-7bgnpHiVp--kX-SemOSOZ0PIJvkGZw=)  
60\. \[simonwillison.net\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGt\_GDIwJ-iJVg8b5lgskkwhjRHbB9rwc485nFgYnNZfE4AgcftSbvqoKMqOBB8mGqIeI70Chm5bI1aW2jhQKp3wIDKnn2kUlblyMHEVUJXSbAeyVWT7ATAgF8HrfNPgDSgwLiI4O6A6voJL31Zg-E=)  
61\. \[prompthub.us\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQExX2Oos77BVecZtPKiF-c\_PNzlFRIMg8voNOsxQdn8IVuHc7oRZIN47Nb116AL\_E3UFd7RD4Mp8LkqIajJvTGkh1xg4Em-s1mT8bo2s66XNNDpLtXOem4SM0BD67-dX0yxEZ\_WjnU2h39A1Ls7STg8QiPKp-nBh2Bd-Kk4lPvurYi9oStvK53VyIqaSHjPgab-MvsoiwC0y\_WK)  
62\. \[reddit.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHJyuGM38r-XYqS4Ov3sM-I-ss\_ePMflneqgMvKKrwD7Q5AV-b9VJtuA1-P3IE6f2llaTSiMzFHpvztbeLgVc-prXD-v5Wb-YQlNt\_rl9aOBGZgCENRY3tPIqprn3Xg4ZzylzhugO4H\_yoxP7TZx9bslC72N-uq5Nes5j1VmCh4LNudvR2nj9FOX03yAMVXdmn8x-nchE\_cJNsfoYQ6L9Cdm64=)  
63\. \[github.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFnKQybgbIYPfm1cJYWXwD5bdO6I1vPnC5utjlxK\_afxuXVt0uOdezBmkdagsVGLBQlVYNBuWuKt6fW11LgMjypZY9vQpU5ac0ryW1YpJq\_k0gOktV8zOYtzdggzTg=)  
64\. \[replicate.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFuHMRwL8t9eWxS8Fu0rvT7lnCqBBo\_IatfRhiBx9m07iKcbc3b2f5qgx-001Jw68DQqIpFRo00crnGY0\_5Ez1YQL-N-\_rXxOOAath5fDFOsfTAxEulWn1ls5qbEW3n3KU=)  
65\. \[selfielab.me\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEQXpqhqfRQEJZOoHupcTDB14PSt\_JWL7pOPAXbdY8YJBJPXuRNV6l3CQLHTA7NVtRLrkdzjGqXLbZefyero3CovtYzpfjhTjnLIlKL7mRQWp35khoPnnfaVEEl5JaYOQvItcdOPzpml2Iv16Aum4oDWB4zUytIVqGWncUfXDyJs9uLT7tG)  
66\. \[medium.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHDrpVPphyiZfy-FQFXb97z6jQWTMhz2gM2xz\_Q3dWlJaeB9\_8BWLPQEgP5DVB7N3\_FqUMLBSPPJDRCM\_oRM\_JkUZLPrBj72g87vsnKKIDdnjCKX0rPbcZojIFClnK8YQI4uZALfcLmpoJYr6dp3idTzMYpE7exK1WDMAv4pjKWncRfxo3fBIdPQZnUoxsGE0SqVDHCWJUAqf3uAZ6ZKNz1m7Kcq2qxRKjr3YaGgpil3knMxHh454nD)  
67\. \[toon-crafter.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGCNc5STlONaPAbJlcVsigeJFgVFynGlsoDsAEEs35vCUXfbBPPx25F9ojhQKkSb1nlkr6s6sht13AyhWxE4u9q6G1qHw7HuUIyE1gzvnnM)  
68\. \[arxiv.org\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFUK1v4ngm6qGEA6CXvpFUbMZZJc-e8K65kH0VNb\_sX7Wj6V-7Q1UMB7eq0iGRRYd9xpgnlvqRh3SpGn8qnYRHtaksJFEG6C9TFNr1v7JC8l6AiPGV2sEeYjQ==)  
69\. \[github.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHmMBz9MqiIY3J8d\_v1m9ZHw2\_8\_A10q1QmEIv9XLQgNLyH-zc8BBCxxwwA-wisxWwSat8wN1emsqTy\_IaKGeVkDwvkKLK7Nopdh9JyCoJkb1c7Bvtj9AgMmIM7gg==)  
70\. \[cacani.sg\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHoQm9qSX0gcSxi1I6E82hZWx5Xpv7CVVOMo6S-5RHDTAYtLsM3NOiCyl2FDZ04SSBM\_vuIbNWyAxAJuC7yJ1obCoglnffa\_AN6DQjNJWqCqV8RDMx1p06V)  
71\. \[creaxus.com\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFLL2Uk\_ByqTR5DWo3dNcXk0sS7qdk3eULJRAXZf4I1s-g80KXU7HnRthQsXkOaoqZfnuzTElKwGQsaTnMnPT99rCvzAR0KpEugfWCPIYlN1hRgcRbG-2RfnEluHgI=)  
72\. \[arxiv.org\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFhrvV8kT8Tki5Xvg8mpsJdm3wx8fyiINEKhAeXMpl-1w94kdWDoOl9mv0-Tq9Q8vHBV9Fug4fqOBWTF-bWjqgzj6bArc-DYk8emKRz2y\_yb1HGiruXDQ==)  
73\. \[paperdigest.org\](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEi5f-zIjQMjg-SlHZuzGdQyrWrtAXNuF1dVKAJ3ozI2O7uBHXMcKuO9ckgfU7P9G3xTJCCkMF5cCyYMPeNVsdx0-5rDYMwAvgrFm-ugVQesAqZ1yYShREuE-c4dkSvMrLlKUOrU3EBy-L1cgkHdpE=)

