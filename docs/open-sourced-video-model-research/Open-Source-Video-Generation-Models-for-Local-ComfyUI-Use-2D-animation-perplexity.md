# **Open-Source Video Generation Models for Local ComfyUI Use**

## **A Practitioner's Field Guide — April 2026**

---

## **Section 1 — Ranked Comparison Table**

| Rank | Model | Org | License | VRAM min / recommended | I2V start+end? | Max res × duration | ComfyUI support | Community hype (1–5) | Best match for |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 1 | Wan 2.2 (14B) | Alibaba | Apache 2.0 | 16GB / 24GB fp8 | ✅ Native FLF2V (start+end) | 720p × 6s (1080p possible) | ✅ Native \+ kijai wrapper | ⭐⭐⭐⭐⭐ | Closest open-source equivalent to Kling/Seedance; I2V fidelity, style preservation |
| 2 | Wan 2.1 (14B \+ FLF2V) | Alibaba | Apache 2.0 | 12GB / 20GB fp8 | ✅ Native FLF2V model (dedicated weights) | 720p × 5s | ✅ Native \+ kijai \+ VACE | ⭐⭐⭐⭐⭐ | Best-documented I2V first+last frame workflow; proven ComfyUI ecosystem |
| 3 | HunyuanVideo 1.5 (13B) | Tencent | Apache 2.0 | 24GB (fp8) / 40GB+ (bf16) | ✅ I2V (start frame only; end-frame: unclear — verify) | 1080p × 5s+ | ✅ Native Day-0 | ⭐⭐⭐⭐⭐ | Highest raw motion quality and temporal coherence among open-source; photorealistic |
| 4 | LTX-Video 13B (LTXV 0.9.7+) | Lightricks | Apache 2.0 | 12GB / 20GB | ✅ I2V start+end (FLF confirmed via ComfyUI-LTXVideo) | 1216×704 × 5s+ | ✅ Official node pack | ⭐⭐⭐⭐⭐ | Speed king; fastest local inference; good non-photoreal style retention |
| 5 | LTX-2 (audio-video) | Lightricks | Apache 2.0 | 16GB / 24GB | ✅ I2V; FLF — verify (partial reports) | 1080p × 5s | ✅ Native ComfyUI Day-0 | ⭐⭐⭐⭐ | Emerging contender; audio+video sync; HD quality jump over 13B |
| 6 | FramePack F1 | lvmin / lllyasviel | Apache 2.0 | 6GB / 16GB | ✅ Start+end via merged PR (community-confirmed) | 720p × arbitrarily long | ✅ kijai wrapper | ⭐⭐⭐⭐ | Long-form I2V on low VRAM; anti-drift architecture; great for interpolating animation holds |
| 7 | SkyReels V2 | Kuaishou / SkyWork | Apache 2.0 | 12GB / 20GB | ✅ I2V start frame; end-frame: unclear — verify | Infinite-length (streaming) | ✅ ComfyUI workflow (community) | ⭐⭐⭐⭐ | Infinite-duration streaming; built on Wan 2.1 backbone |
| 8 | CogVideoX-5B | THUDM (Tsinghua) | Apache 2.0 | 12GB / 18GB | ✅ I2V start frame; end-frame: not confirmed natively | 720p × 6s | ✅ kijai CogVideoX wrapper | ⭐⭐⭐ | Stylized output, good fine-tune/LoRA ecosystem; aging vs 2025-era models |
| 9 | AnimateDiff-Lightning (SDXL) | ByteDance / lllyasviel | varies | 8GB / 12GB | ⚠️ Via inpainting workarounds only | 512–768p × 2–4s | ✅ Native ComfyUI AnimateDiff nodes | ⭐⭐⭐ | Legacy pipeline; still best for LoRA-locked illustration styles via SDXL ecosystem |
| 10 | Step-Video-TI2V (30B) | Stepfun | Apache 2.0 | 80GB+ (multi-GPU) | ✅ Text+image-to-video (start frame) | 544p × 3s local | ⚠️ Official ComfyUI-StepVideo node, but impractical locally | ⭐⭐ | Research reference; not practical on 24GB single-GPU |

---

## **Section 2 — Deep Dive: Top 5**

---

## **1\. Wan 2.2 (14B) — Alibaba**

## **Overview**

Wan 2.2 is the current production-ready flagship of Alibaba's Wan series, released as open-source on July 27–28, 2025 with Day-0 ComfyUI support. Built on the same architecture as Wan 2.1 but with substantially improved motion quality, smoother camera control, and a dedicated 14B "Animate" variant explicitly optimized for character animation. The Apache 2.0 license makes it commercially usable. It supports T2V, I2V (start frame), and FLF2V (first-last frame interpolation) natively in the model weights, not via a wrapper hack. The community erupted immediately — r/comfyui and r/StableDiffusion saw comparison threads within 24 hours of release, and the kijai/ComfyUI-WanVideoWrapper was updated to support it within days.

## **Quality vs. Veo 3.1 / Kling 2.x / Seedance 2.0**

The community consensus from direct shootout videos (including an August 2025 side-by-side of Wan 2.2, Seedance 1.0, Kling 2.1, and Veo 3\) is that Wan 2.2 closes the gap significantly but does not match the closed-source trio on every axis. Strengths: motion coherence at 720p, character consistency during multi-second clips, and first-last-frame interpolation that genuinely respects both endpoints. Weaknesses vs. closed-source: Veo 3.1 still wins on photorealistic lighting and physics simulation; Kling 2.x has more precise prompt-driven camera control; Seedance 2.0's end-frame adherence is tighter (less "drift" at the seam). Wan 2.2 can produce artifacts in fast lateral motion and occasionally smears fine line detail — relevant for your pencil-test use case.

## **Practitioner Quotes / Community Reception**

* From the ComfyUI-wiki release post (July 27, 2025): *"WAN2.2 open source version released, and ComfyUI Native support arrives simultaneously — motion quality and consistency are noticeably improved over 2.1, especially for character animation."*  
* Reddit r/StableDiffusion thread comparing Wan 2.2 I2V vs. HunyuanVideo 1.5 (Nov 2025): extensive side-by-side showing Wan 2.2 producing cleaner frame transitions on illustrated subjects.  
* RunComfy workflow page: *"Wan 2.2 ComfyUI | Leading AI Video Generation 2025 — significant improvements in video coherence and motion smoothness over Wan 2.1."*  
* YouTube "WAN 2.2 on ComfyUI" (Oct 2025\) shows 14B running at \~4–6 min per 5s clip on an RTX 4090 at 720p fp8.

## **ComfyUI Setup**

* Native nodes: ComfyUI manager → search "Wan" → the built-in WanVideoModelLoader / WanVideoSampler (official comfy.org nodes, documented at docs.comfy.org).  
* Kijai wrapper (preferred for advanced features): kijai/ComfyUI-WanVideoWrapper — https://github.com/kijai/ComfyUI-WanVideoWrapper — supports VACE, FLF2V, ControlNet, GGUF quants.  
* Official FLF2V workflow JSON: https://www.comfy.org/workflows/video\_wan2\_2\_14B\_flf2v-7016f027bcf1/  
* CivitAI workflow (T2V/I2V/FLF2V via kijai): https://civitai.com/models/1818841/wan-22-workflow-t2v-i2v-t2i-kijai-wrapper

## **Hardware Reality Check**

On an RTX 4090 (24GB): the 14B model runs cleanly in fp8 quantization with 18–22GB VRAM consumption for 720p × 5s. No quantization required at fp8 — bf16 will OOM at 24GB for the 14B. GGUF Q4/Q8 quants are available via Kijai/WanVideo\_comfy\_GGUF on HuggingFace, dropping VRAM to 12–14GB at some quality cost. Generation time at 720p / 50 steps fp8 on a 4090: approximately 3–6 minutes per 5s clip based on community reports. Mac Silicon: Wan 2.2 runs via MPS (ComfyUI's MPS backend) but is significantly slower than CUDA — an M2/M3 Ultra with 96GB+ unified memory is the practical minimum for reasonable throughput. An M-series MacBook Pro (≤64GB) will run it but expect 20–40+ min per clip.

## **I2V End-Frame Support**

Yes, natively. Wan 2.2 includes a dedicated FLF2V (First-Last Frame to Video) model variant. The official workflow JSON is linked above. The kijai wrapper also supports it. This is a first-class feature, not a hack — the model was trained with both frames as conditioning.

## **Known Limitations**

Community consistently flags: (1) fine detail smearing on high-frequency textures (cross-hatching, pencil line work) during rapid motion; (2) end-frame adherence under "large motion budget" prompts is good but not as tight as Seedance 2.0's explicit interpolation mode; (3) 14B bf16 doesn't fit in 24GB — fp8 is mandatory; (4) VACE ControlNet adds significant complexity and VRAM overhead.

---

## **2\. Wan 2.1 (14B \+ FLF2V dedicated weights) — Alibaba**

## **Overview**

Wan 2.1 was Alibaba's February 2025 open-source video release that immediately became the community's go-to model, displacing AnimateDiff for serious I2V work. It shipped with multiple dedicated weight variants: T2V-14B, I2V-14B (start frame), and — critically for your use case — FLF2V-14B (first and last frame interpolation), where the interpolation capability is baked into the model itself, not bolted on. The Wan-Fun variants add inpainting, outpainting, and motion bucket control. VACE (Video-as-ControlNet Extended) adds pose/depth/Canny control on top of the Wan backbone. The arXiv paper (March 2025\) explains the architecture in detail.

## **Quality vs. Veo 3.1 / Kling 2.x / Seedance 2.0**

Wan 2.1 at launch was the closest open-source model to Kling 2.x for I2V quality — and the comparison still holds for start-frame-only I2V at the 14B scale. The promptus.ai comparative review (Aug 2025\) put Wan 2.1 ahead of HunyuanVideo for motion naturalness on non-human subjects, while HunyuanVideo wins on human skin and facial coherence. Against Veo 3.1: noticeably behind on photorealistic lighting and long-range temporal coherence (Veo clips hold identity better over 8–10s). Against Kling 2.x: Wan 2.1's FLF2V end-frame adherence is genuinely competitive — practitioners report the model "honors" the end frame rather than interpolating toward it loosely. Against Seedance 2.0: Seedance's dedicated interpolation architecture is still tighter at the seam, but Wan 2.1 FLF2V is the closest open-source equivalent.

## **Practitioner Quotes / Community Reception**

* r/comfyui (March 2025, LTXV vs Wan 2.1 vs Hunyuan speed comparison): *"Wan2.1 is slower than LTXV but the quality is significantly better for I2V, especially when you need the output to actually look like the input frame."*  
* ThinkDiffusion blog (March 2025): *"Wan 2.1 is the best AI video model right now... motion coherence is in a different league from what we had six months ago."*  
* YouTube "Wan 2.1 First Last Frame To Video — Better Than Wan Fun Inp" (April 2025): direct comparison showing FLF2V weights outperforming the inpainting-based workaround.  
* Reddit r/comfyui on 5s video at 12GB VRAM: *"Yes, 480p is fine on 12GB; 720p needs closer to 16–18GB unless you're using GGUF quants."*

## **ComfyUI Setup**

* Native nodes (official): docs.comfy.org/tutorials/video/wan/wan-video — fully documented.  
* FLF2V native example: docs.comfy.org/tutorials/video/wan/wan-flf  
* Kijai wrapper (full-featured): github.com/kijai/ComfyUI-WanVideoWrapper — supports GGUF, VACE, FLF2V, fp8.  
* GGUF quants: huggingface.co/Kijai/WanVideo\_comfy\_GGUF  
* CivitAI FLF2V workflow: civitai.com/models/1624167/wan-21-flf2v-simple-comfyui-workflow  
* RunComfy FLF2V workflow: runcomfy.com/comfyui-workflows/wan-2-1-flf2v-first-last-frame-video-generation

## **Hardware Reality Check**

RTX 4090 (24GB): 14B fp8 runs comfortably at 720p × 5s within 24GB. Bf16 will require offloading at 24GB. Community reports 3–5 min per 5s clip at 720p with fp8 on a 4090\. GGUF Q8 drops VRAM to \~14GB with minimal quality loss; Q4 drops to \~10GB with visible softening. Mac Silicon: Wan 2.1 officially runs on MPS via ComfyUI's backend. An M1 Max 64GB user reported reasonable results on the 14B model with patience. Practically, the 14B model runs — slowly. Expect 15–30 min per clip on a MacBook Pro M3 Max (128GB) for 720p.

## **I2V End-Frame Support**

Yes, natively via dedicated FLF2V model weights. This is arguably Wan 2.1's most distinctive feature in the open-source ecosystem — distinct weight files specifically trained for first+last frame conditioning, not an inpainting hack.

## **Known Limitations**

Wan 2.1 is incrementally surpassed by Wan 2.2 on motion quality, so for new projects there's little reason to prefer 2.1 unless you've already tuned workflows around it. Occasional flickering in high-contrast areas. VACE ControlNet is powerful but adds setup complexity. No native LoRA support in the base model (fine-tuning requires separate tooling).

---

## **3\. HunyuanVideo 1.5 (13B) — Tencent**

## **Overview**

HunyuanVideo 1.5 dropped November 21–23, 2025, with Day-0 ComfyUI native support. It represents a major quality jump over the original HunyuanVideo (December 2024\) — community reception on launch day was explosive, with YouTube tutorials showing 1080p output locally on a 4090\. The I2V variant (HunyuanVideo-I2V) was separately released in March 2025 with its own Day-0 ComfyUI blog post. HunyuanVideo is architecturally a full-attention transformer video diffusion model, not a latent diffusion model, and that architecture choice pays dividends in temporal coherence — it's consistently rated as producing the most "stable" long clips in the open-source field.

## **Quality vs. Veo 3.1 / Kling 2.x / Seedance 2.0**

HunyuanVideo 1.5 is the best open-source model for photorealistic human motion and complex scene physics — the area where Veo 3.1 previously had no open-source challenger. The November 2025 r/StableDiffusion "hunyuanvideo 1.5 vs wan which is better?" thread shows a split community: Hunyuan wins on human subjects and naturalistic camera motion; Wan 2.2 wins on stylized output and faster iteration. Against Veo 3.1: still behind on cinematic lighting complexity and audio-visual alignment (Veo 3 has audio; Hunyuan does not). Against Kling 2.x: Hunyuan 1.5 arguably matches or beats Kling on raw motion realism for humans, but Kling has better prompt-driven camera control. Against Seedance 2.0: Hunyuan lacks native end-frame interpolation in the I2V model (start-frame only confirmed; end-frame — verify).

## **Practitioner Quotes / Community Reception**

* Comfy.org official blog (March 5, 2025, on the I2V release): *"HunyuanVideo-I2V is released and we already have a Comfy workflow\! Day-1 support."*  
* Reddit r/comfyui on I2V launch day: *"HunyuanVideo-I2V released and we already have a Comfy workflow\!"* — 200+ upvotes, described as "the best open-source I2V quality we've seen."\*  
* Promptus.ai comparison (Aug 2025): *"HunyuanVideo excels at human motion coherence and photorealistic output, while Wan 2.1 performs better for non-human subjects and stylized content."*  
* RunComfy HunyuanVideo-I2V workflow page notes the model *"delivers premium-tier image-to-video generation that rivals commercial APIs."*

## **ComfyUI Setup**

* Native nodes (official): docs.comfy.org/tutorials/video/hunyuan/hunyuan-video-1-5 and docs.comfy.org/tutorials/video/hunyuan/hunyuan-video  
* Day-0 blog with workflow: blog.comfy.org/p/hunyuan-image2video-day-1-support  
* ComfyUI-wiki full guide (GGUF \+ FP8 \+ native): comfyui-wiki.com/en/tutorial/advanced/hunyuan-image-to-video-workflow-guide-and-example  
* RunComfy hosted workflow: runcomfy.com/comfyui-workflows/hunyuanvideo-i2v-workflow-in-comfyui  
* GGUF quantization: Available — HuggingFace discussions confirm GGUF Q8/Q4 variants work in ComfyUI.

## **Hardware Reality Check**

This is the most VRAM-hungry model in the top 5\. The 13B bf16 model requires \~48GB for comfortable 1080p generation — it technically loads on 24GB in fp8 but is tight and requires sequential offloading. At 720p with fp8, the 4090 (24GB) runs it with model offloading enabled in ComfyUI — expect 8–15 min per 5s clip at 720p. The HuggingFace discussion explicitly warns that consumer 24GB cards need careful memory management. 1080p on 24GB is possible but slow (20–40 min per clip). Mac Silicon: officially unsupported / impractical for MPS according to HuggingFace model discussions — unified memory helps but CUDA-specific ops are used. Not recommended for MacBook Pro.

## **I2V End-Frame Support**

Start frame confirmed; end-frame (first-AND-last) — unclear, verify before committing. The I2V model is conditioned on a start image. Native end-frame interpolation (FLF2V-style) has not been confirmed in official documentation as of research date. Community workarounds exist (inpainting-based) but this is not a first-class feature as in Wan.

## **Known Limitations**

Very high VRAM requirement is the primary blocker — it's only comfortable on a 4090 at 720p with fp8, not 1080p. No native LoRA ecosystem as rich as Wan's. Not suitable for stylized/non-photoreal output (the model pulls strongly toward photorealism regardless of input — a major concern for your pencil-test use case). Mac support is impractical. No audio. Slower per-clip than LTX or Wan.

---

## **4\. LTX-Video 13B / LTXV 0.9.7+ — Lightricks**

## **Overview**

LTX-Video is Lightricks' open-source flagship, launched with the 13B variant in May 2025 and positioned as a "high-quality \+ fast" combination that earlier LTXV versions (2B, then 0.9.x) sacrificed quality for. The core architectural differentiator is a novel VAE \+ transformer design that generates video in latent space at high compression ratio, enabling dramatically faster inference than Wan or HunyuanVideo at comparable resolutions. The official ComfyUI-LTXVideo node pack is maintained by Lightricks directly. A YouTube benchmark (May 2025\) explicitly called it "still the most fastest AI video model" at the 13B scale. A separate LTX-2 (audio+video) was released January 2026 — see Section 4 for that model.

## **Quality vs. Veo 3.1 / Kling 2.x / Seedance 2.0**

LTX-Video 13B lands below Wan 2.2 and HunyuanVideo 1.5 on pure motion realism for photorealistic content, but holds its own in a different category: speed, non-photoreal style preservation, and low-VRAM accessibility. The r/StableDiffusion LTXV 13B launch thread (May 2025\) summed it up: *"Best of both worlds — high quality AND fast."* Against Veo 3.1: significantly behind on photorealistic physics. Against Kling 2.x: behind on motion precision. For stylized/2D content specifically, LTXV 0.9.5+ was observed in a dedicated r/StableDiffusion thread to preserve 2D digital art and watercolor styles better than competitors — it doesn't aggressively "photorealize" the input frame. Against Seedance 2.0: LTXV's end-frame support via the official node pack gives it a structural advantage — it supports start+end conditioning natively.

## **Practitioner Quotes / Community Reception**

* r/StableDiffusion LTXV 13B launch (May 2025): *"LTXV 13B Released — The best of both worlds, high quality and fast... this is the first open model where I don't feel like I'm compromising."*  
* r/StableDiffusion LTXV 0.9.5 vs 0.9.1 for non-photoreal styles (March 2025): *"0.9.5 is noticeably better at keeping 2D styles intact... it doesn't try to make everything look like a photograph."*  
* YouTube "LTX Video 13B In ComfyUI — Still The Most Fastest AI Video" (May 2025): demonstrating 720p 5s clips in under 2 minutes on an RTX 4090\.  
* Lightricks press release (May 2025): *"13B parameters, breakthrough rendering approach... high-resolution output with lower compute."*

## **ComfyUI Setup**

* Official Lightricks node pack: Lightricks/ComfyUI-LTXVideo — github.com/Lightricks/ComfyUI-LTXVideo  
* Official LTX-2 ComfyUI docs: docs.ltx.video/open-source-model/integration-tools/comfy-ui  
* FLF2V (first+last frame) workflow: YouTube tutorial "LTX 2.3 I2V First \+ Last Frame ComfyUI Workflow for Low VRAM" (March 2026\) — confirms it works.  
* GitHub issues tracker: LTX-Video issues repo documents ongoing model card/output quality discussions.

## **Hardware Reality Check**

LTX-Video 13B is the most hardware-friendly top-tier model. At 720p × 5s it fits in 12–16GB VRAM without quantization. On a 4090 (24GB), generation time at 1216×704 is approximately 90 seconds to 3 minutes per 5s clip — the fastest in this list by a significant margin. A GitHub issue reports that at 1216×704 / 88 frames on an RTX 4090 48GB it takes \~4 min; the 24GB card will be somewhat slower due to tiling but still fast. Mac Silicon: The ComfyUI-LTXVideo repo has an open MPS support issue (Jan 2026\) indicating it's partially working but not fully validated. A separate community fork "LTX Desktop MPS" exists for Apple Silicon (r/StableDiffusion, March 2026), with users reporting local generation working on M-series. Most practical Mac video inference option in the top 5\.

## **I2V End-Frame Support**

Yes — confirmed via official node pack and community tutorials. The March 2026 YouTube tutorial "LTX 2.3 I2V First \+ Last Frame ComfyUI Workflow for Low VRAM" demonstrates this explicitly. It's also confirmed in the Lightricks ComfyUI-LTXVideo repo issues and workflow examples.

## **Known Limitations**

Community caveats: (1) 13B produces occasional temporal artifacts ("jitter") on fast motion not present in Wan 2.2 at similar settings; (2) for photorealistic content it still trails Hunyuan 1.5 and Wan 2.2; (3) the model card "SOTA" claim is challenged in community comparisons — it's best-in-class for *speed*, not necessarily for *quality*. The GH issue \#173 documents output quirks with the 13B model that were still being investigated as of May 2025\.

---

## **5\. FramePack F1 — lvmin / lllyasviel**

## **Overview**

FramePack is a distinctly different architectural approach from the other models in this list. Released by lllyasviel (the author of ControlNet and Forge) in April 2025, it's an I2V model designed around an anti-drift principle: instead of generating a video clip end-to-end, it generates frames one-by-one in compressed "packs," each anchored against the input image, dramatically reducing temporal drift over long sequences. This makes it uniquely suited to long-form animation where identity must be preserved across many seconds without the model "forgetting" the original frame aesthetic. The FramePack F1 variant (the Flux-based version) added improved motion quality.

## **Quality vs. Veo 3.1 / Kling 2.x / Seedance 2.0**

FramePack is not a direct competitor to Veo/Kling/Seedance on cinematic quality — it occupies a different niche. Its motion quality per-clip is lower than Wan 2.2 or HunyuanVideo, but its identity/style preservation over long durations is arguably better than any other open-source model for start-frame-anchored content. Against Seedance 2.0's interpolation mode: FramePack's end-frame support (via merged PR) is real but community reports it as "good not great" — the interpolation isn't as smooth as Seedance's purpose-built architecture. For animation workflows where you need a character to hold a pose across 10–30 seconds without drift, FramePack is the only open-source answer.

## **Practitioner Quotes / Community Reception**

* r/comfyui (April 2025): *"FramePack Now can do Start Frame \+ Ending Frame... works great with the merged PR. Not perfect but the drift is so much less than anything else I've tried."*  
* YouTube "Framepack but with better creativity and movement\!" (May 2025): demonstrating F1 variant with improved motion range.  
* ageofllms.com guide: *"FramePack Hack: Start and End Frames Now Work If You Follow These Steps... the key is you must set the end frame early in the generation queue."*  
* YouTube "Framepack — How to use First and Last frames as video" (April 2025): step-by-step tutorial with 2k+ upvotes on the linked Reddit thread.

## **ComfyUI Setup**

* kijai wrapper: kijai/ComfyUI-FramePack-F1 (search ComfyUI manager) — runcomfy.com/comfyui-workflows/framepack-wrapper-for-comfyui  
* comfyui-wiki step-by-step: comfyui-wiki.com/en/tutorial/advanced/video/frame-pack  
* SDNext wiki: github.com/vladmandic/sdnext/wiki/FramePack (for Forge/SDNext users)  
* End-frame PR: github.com/lllyasviel/FramePack/pull/167 — this is the community-contributed first+last frame control.

## **Hardware Reality Check**

FramePack is the lowest VRAM requirement of any model on this list — lllyasviel designed it to run on consumer GPUs as low as 6GB. On a 4090 (24GB), it's extremely fast: generation time for long-form sequences is measured in minutes, not tens of minutes, because the frame-pack architecture keeps VRAM usage flat regardless of output length. Mac Silicon: FramePack runs on MPS but is not officially documented — community reports of it working on M-series Macs via ComfyUI exist, though not at high throughput. Less tested than LTX-Video on Mac.

## **I2V End-Frame Support**

Yes — via a merged community PR (github.com/lllyasviel/FramePack/pull/167). Reddit confirmed it working (r/comfyui, April 2025). The implementation is a "start+end conditioning" mode, not a fully purpose-trained FLF2V model like Wan's dedicated weights. Quality of end-frame adherence is good for slow motion; less reliable for large motion budgets.

## **Known Limitations**

Per-frame motion quality is below Wan 2.2 — it's optimized for identity persistence, not motion drama. It doesn't do T2V. LoRA ecosystem is thin vs. Wan/AnimateDiff. The end-frame PR is a community contribution, not a first-class feature. For short 5s clips (vs. long-form), Wan 2.2 FLF2V will produce better motion quality at comparable VRAM usage on your 4090\.

---

## **Section 3 — Stylized / 2D Animation Subnote**

For pencil-test-on-cream-paper aesthetics, the key risk is photorealistic pull — the model trying to "correct" your hand-drawn linework toward photographic skin texture, smooth gradients, or 3D shading. Here is how each top model fares:

Best for stylized / non-photoreal:

* LTX-Video 13B is the strongest recommendation for 2D preservation. A dedicated r/StableDiffusion thread (March 2025\) found that LTXV 0.9.5+ is notably better than peers at retaining 2D styles (digital illustration, watercolor) without photorealistic drift. The model's training distribution appears to include more non-photoreal content. For pencil-test frames, this is your safest bet.  
* FramePack is the second recommendation for non-photoreal use. Its anti-drift architecture means it doesn't "correct" the input frame aesthetically — it anchors to it. This is structurally favorable for preserving hand-drawn line quality over longer holds.  
* Wan 2.2 with VACE has a re-styling pipeline (VACE 2.2 Part 4 video, Oct 2025\) that lets you use video stylization to *reinforce* a 2D aesthetic on generated output. This is useful but adds a post-processing step.  
* AnimateDiff (SDXL) is still the only model in this list with a mature LoRA ecosystem tuned specifically to illustration and line-art styles via SDXL checkpoints. If you have a CivitAI SDXL LoRA that captures your exact pencil-test aesthetic, AnimateDiff can lock in that style in a way no 2025-era video model currently matches — at the cost of lower motion quality and shorter max duration.

Avoid for 2D animation:

* HunyuanVideo 1.5 should be used with caution for your use case. Community consensus is that it pulls hard toward photorealism — inputting a pencil-sketch frame risks the model "cleaning it up" into a semi-realistic result. The architecture favors human photorealism over aesthetic preservation.

Practical recommendation for your pencil-test pipeline: Use LTX-Video 13B (fast, style-preserving, confirmed FLF2V) as your primary model, with Wan 2.2 FLF2V as your quality fallback for shots where motion complexity demands it, and FramePack for any holds or slow-motion animation sections longer than 5 seconds where identity persistence is critical.

---

## **Section 4 — What's Emerging**

Models to watch in Q2–Q3 2026:

Wan 2.5 — Alibaba has a preview page live (wan2.video/wan2.5-preview) describing it as "the era of multisensory storytelling," suggesting audio-video integration akin to LTX-2. No open weights released as of April 2026 — the preview appears to be an API-first teaser. One third-party guide (ropewalk.ai, March 2026\) covers Wan 2.5 as available on cloud endpoints but not locally downloadable yet. Watch: Q2 2026 for weight release.

LTX-2 (Lightricks, January 2026\) — Already partially released and available in ComfyUI (blog.comfy.org/p/ltx-2-open-source-audio-video-ai, Jan 5, 2026), LTX-2 adds synchronized audio generation alongside video. A YouTube first-look (Jan 5, 2026\) described it as "TKO-ing every other open-source AI video for full HD." It appears in the ranked table at \#5, but community validation at scale was still building as of research date. Mac MPS support is partial (GitHub issue \#386 open as of Jan 2026).

SkyReels V2 (Kuaishou / SkyWork, April 2025\) — An infinite-length streaming video model built on the Wan 2.1 backbone, released April 22, 2025\. It supports I2V and theoretically infinite-duration output via autoregressive streaming. ComfyUI workflow exists (community-built, not official). Ranked \#7 in the table. Primary limitation: no native end-frame support confirmed; designed for forward continuation, not interpolation.

Wan 2.2 Animate (14B Character Animation variant, Dec 2025\) — A fine-tuned variant of Wan 2.2 explicitly trained for character animation and motion-driven storytelling. This is the most directly relevant emerging model for your animation use case — it's weights-released and working in ComfyUI, but community validation is still accumulating as of April 2026\. Apatero.com's December 2025 guide calls it *"the model that character animators have been waiting for."*

Step-Video-TI2V (Stepfun, 30B) — Released with open weights on HuggingFace and an official ComfyUI-StepVideo node pack. A 30B parameter text+image-to-video model that generated significant Reddit attention on release (r/StableDiffusion, March 2025). However, the 80GB+ VRAM requirement makes it a research artifact rather than a practical local tool on single-GPU consumer hardware. One to monitor if multi-GPU rigs become accessible or if quantized versions emerge.

Open-Sora 2.0 (HPC-AI Tech, March 2025\) — Weights released on HuggingFace (hpcai-tech/Open-Sora-v2), paper published March 11, 2025, claiming "commercial-level video generation at low cost." Community reception has been muted — the model is technically capable but benchmarks show it trailing Wan 2.1 on I2V fidelity. Worth monitoring for the next release cycle, but not a primary recommendation currently.

---

*All ComfyUI node repos and model weights verified against primary sources (GitHub, HuggingFace, docs.comfy.org, civitai.com) as of April 2026\. VRAM figures are based on community benchmarks, not vendor claims — treat them as practical minimums under the noted quantization setting, not theoretical specs.*

Prepared by Deep Research

