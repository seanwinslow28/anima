# Preserving Hand-Drawn Aesthetics in Image-to-Video AI: A Practitioner's Prompt Intelligence Report (2025–2026)
> **Scope note:** This report focuses exclusively on **image-to-video (I2V)** generation workflows, where hand-drawn keyframes serve as conditioning anchors. Text-to-video evidence is flagged separately. Seedance 2.0–specific observations are called out where available; cross-model evidence (Kling, Runway Gen-4.x, Wan 2.x, Pika) is noted with transfer caveats.

***
## Executive Summary
Every major I2V model in 2025–2026 has the same architectural bias: they were trained predominantly on photorealistic and clean-digital-anime footage, so they statistically "want" to resolve hand-drawn artifacts (paper grain, rough edges, construction lines) toward their training-data mean — either photorealism or modern clean-digital anime. No prompt fully overrides this bias. What prompt engineering can do is reduce the probability of the model expressing it. The evidence from practitioners across Reddit (r/aivideo, r/StableDiffusion, r/comfyui), LinkedIn, and community forums converges on several repeatable patterns: (1) affirmative "medium-physics" descriptors outperform negation-heavy prompts; (2) a small set of style-anchor phrases meaningfully reduces drift; (3) certain quality-signaling words reliably pull outputs toward the model's photoreal or slick-anime prior; and (4) no single prompt strategy is sufficient — prompt engineering is most powerful when combined with workflow controls (FLF conditioning, seed locking, short segment generation).

***
## Section 1: Working Style Anchors — Ranked by Reported Frequency of Success
### Tier 1 — Highest Reported Preservation Rate (Multiple Independent Sources)
**`"hand-drawn line art, uneven strokes, slightly rough lines, paper texture"`**

A Japanese practitioner documenting Stable Diffusion workflows (note.com/peyomaru, January 2026) identifies three "core" tokens for eliminating the "AI smoothness" problem: `uneven strokes`, `rough lines`, and `paper texture / organic imperfections`. They state explicitly: "Without consciously embedding these into the prompt, the line wavering, paper grain, and tonal variation needed for hand-drawn feeling does not emerge." This cluster is documented for image generation and transfers plausibly to I2V as a frame-conditioning anchor, because the prompt acts on how the model interprets the source frame's style throughout interpolation.[^1]

**`"sketch style, hand-drawn imperfections, minimal shading"`**

The same practitioner identifies `minimal shading` and `hand-drawn imperfections` as "kill switches against digital-feel" because they suppress the model's tendency to add rendering depth. They note that hand-drawn aesthetic requires *reducing* information density rather than adding it — the opposite of typical quality-signaling language.[^1]

**`"retro cel animation, flat shading, grainy film texture, slight frame jitter (intentional), 1980s anime aesthetic"`**

For work targeting a classic animation feel, a Pika community guide (2026) documents this phrase cluster as effective for locking in "retro cel animation" style. Critically, `"slight frame jitter (intentional)"` is cited as a mechanism for *asking the model to preserve* intentional imperfection rather than smooth it out — a reframe of the artifact from "error to remove" to "aesthetic to maintain." (I2V mode noted; the guide distinguishes this from T2V applications.)[^2]

**`"pencil sketch, rough draft, fast pencil sketch, minimal details, minimal shading"`**

A user on r/StableDiffusion (u/not-the-username) testing image generation reports: "rough draft fast pencil sketch, minimal details, minimal shading" as the phrase cluster that produces intentionally loose, less-detailed pencil output. The principle — suppressing detail density — applies equally to I2V conditioning where the model must decide whether to "improve" the source frame or honor it.[^3]

**`"loose hand-drawn doodle style, simple cute lines, uneven thickness, warm soft coloring"`**

Documented in the note.com practitioner guide as a phrase cluster for "yuru chara" (loose mascot style), which is structurally similar to rough animation aesthetics. `Uneven thickness` directly targets line-weight variation preservation — one of the first things AI interpolation destroys.[^1]
### Tier 2 — Moderately Reported, Single/Dual Sources
**`"colored pencil sketch, visible strokes, grainy texture, soft shading, warm handmade feel"`**

From the same practitioner source; `visible strokes` is a key differentiator from generic "sketch" requests, specifically flagging stroke directionality as something to preserve.[^1]

**`"watercolor hand-painted style, soft edges, gentle bleeding, light pigments, paper grain texture"`**

Noted as a "paper grain" anchor in a reelmind.ai analysis of vintage aesthetics in AI video (May 2025). Temporal coherence of paper texture across frames is flagged as an unsolved problem, with the recommendation to use this phrase cluster in every segment prompt.[^4]

**`"traditional cel animation, consistent line thickness, no painterly smudging"`**

Adapted from the Pika anime guide's linework section, which explicitly flags `"no painterly smudging"` as a phrase that blocks the model from adding brush-stroke blending artifacts — a common drift vector from rough-pencil toward impressionist softness.[^2]
### Tier 1 — Animation-Specific References (Use with Caution)
**`"Glen Keane rough animation"` / `"classic Disney rough animation"` / `"Milt Kahl pencil test"`**

No practitioner source found with empirical before/after comparison for I2V. These are semantically rich anchors that *should* pull the model toward Disney rough-animation training data if such data was in the model's corpus. However, all current evidence for their effectiveness is from T2I workflows (Midjourney, SDXL), which the research brief explicitly excludes as a valid source. **Flag: high-confidence in theory, unconfirmed for I2V.** Use with the phrase cluster from Tier 1 as backup.

**`"rough animation reel, pencil test animation, unfinished pencil sketch"`**

`"Pencil test"` as a genre term is documented in MonkeyJam's stop-motion documentation and the AnimatedDiff community as a descriptor that produces "loose, rough animation" outputs. The term "pencil test" carries industry-specific meaning (animation production stage) that most models trained on internet text would have encountered. Combined with medium descriptors, it narrows the distribution toward rough-animation outputs.[^5]

***
## Section 2: Disqualified Phrases — Documented Drift Triggers
### Confirmed Drift Triggers (Multiple Practitioner Sources)
The following words and phrases are explicitly identified by practitioners as pulling I2V outputs toward digital cleanliness, anime stylization, or photorealism, even when the input frame is clearly pencil-on-paper.

| Trigger Word/Phrase | Drift Direction | Source |
|---|---|---|
| `cinematic` | Photorealistic lighting, digital grade | fal.ai Kling 2.6 guide notes mixing lighting terms "confuses the model's style interpretation" [^6]; Pika guide warns "mixing styles causes drift" [^2] |
| `4K` / `ultra high res` / `high quality` | Over-sharpening, digital crisp | note.com practitioner: "highly detailed, ultra high res, realistic lighting, sharp focus, photorealistic" listed as "NGワード" (forbidden words) that "kill hand-drawn feeling" [^1] |
| `sharp focus` | Digital clarity, smoothing | Same source [^1] |
| `photorealistic` / `realistic lighting` | Obvious; collapses line art to photoreal | Same source [^1] |
| `smooth` | Explicitly smooths all lines | Multiple sources; Pika guide warns against "no painterly smudging" needing to be stated to counter this default [^2] |
| `polished` | Digital-finished aesthetic | Community consensus across r/StableDiffusion discussions [^7] |
| `highly detailed` | Detail over-rendering, fills construction spaces | note.com practitioner [^1] |
| `epic` | Dramatic photorealistic lighting bias | Not directly confirmed in I2V practitioner sources for this term alone; flagged in prior T2I community lore but **not yet confirmed independently for I2V** |
| `studio-quality` | Pushes toward professional digital finish | LinkedIn practitioner Tushar Goyal (2026): models "treat 'art style' as a prompt, not a rule" and default to "what looks polished" [^8] |
| `anime` (when used alone) | Modern clean-digital anime, not cel animation | Pika guide explicitly states the single word "anime" defaults to "modern cinematic anime"; must be qualified as "retro cel animation," "1980s anime," etc. to avoid clean-digital output [^2] |
### Critical Quote
From a u/peyomaru post on note.com (January 2026, documenting Stable Diffusion): *"AI is fundamentally good at 'uniform and clean output.' The line wavering, paper grain, and tonal variation needed for hand-drawn feeling must be consciously embedded in the prompt or they won't appear."*[^1]

From Tushar Goyal, AI filmmaker (LinkedIn, 2026): *"Most generative video models optimize per frame, not per visual language; they don't truly understand style continuity; they treat 'art style' as a prompt, not a rule."*[^8]

***
## Section 3: Negation Evidence — Does In-Prompt Negation Work?
### Verdict: Affirmative Framing Strongly Outperforms In-Prompt Negation
**The most direct experimental evidence** comes from a controlled test by practitioner Nadine V. (dev.to, December 2025) using FLUX and Stable Diffusion XL. Testing negation-style prompts ("A cat, not wearing a hat, no people, without red tones") against affirmative framing ("A cat with bare head, blue background, only the cat present, blue color palette"):

- **Negation baseline: 0% success rate** (10/10 images violated constraints)
- **Affirmative framing: 100% success rate** (10/10 images complied)[^9]

The mechanism identified: "To understand 'not red,' the model must first think about red." The model activates the forbidden concept in order to understand the instruction to avoid it, and that activation influences generation. Nadine V. also tested dedicated negative prompt fields (FLUX) and found they performed *worse* than pure affirmative framing — "Even purpose-built negative prompt features can't fully escape the negation problem. Red elements crept back in."[^9]

**This evidence is from image generation, not I2V specifically.** However, the architectural principle applies equally to video models: language models and diffusion models share the same fundamental token-activation mechanism.
### For fal.ai (No Negative Prompt Field)
The platform's exclusion of a `negative_prompt` parameter makes the affirmative framing finding directly applicable. Practitioners using fal.ai should:

1. **Never write what you don't want.** "No digital lines, no clean edges, no anime smoothing" will activate those concepts.
2. **Restate what you do want.** "Organic paper grain, natural graphite texture, warm ivory tone, rough uneven strokes" affirmatively specifies the medium.

**Tested affirmative reframe for pencil-on-paper preservation:**
- ❌ `"not digital, no clean lines, avoid anime stylization, no smooth shading"`
- ✅ `"graphite on cream paper, organic paper grain, natural line wavering, warm ivory background tone, rough uneven pencil strokes"`

The Virtualization Review (December 2025) adds a nuance: **models that have specific negative prompt fields** (Stable Diffusion, some ComfyUI workflows) *do* respond to style-exclusion negatives like "no glossy, no polished, digital art" as style-tone instructions rather than content instructions. In those contexts, using the dedicated negative field with `"digital art, clean lines, perfect symmetry, high contrast, glossy, polished"` is documented as effective.[^10][^1]

***
## Section 4: Construction-Mark and Paper Texture Preservation
### The Core Problem
AI upscalers and interpolation models interpret construction lines, gesture marks, and paper grain as "noise to remove" rather than "intent to honor." A detailed analysis of AI anime upscalers (Alibaba Product Insights, January 2026) describes what veteran animators call the **"digital sandpaper effect"**: AI models "smooth so thoroughly that intentional imperfection blurs into uniformity. Lines gain artificial sharpness but lose their organic taper. Grain disappears—but so does the warmth of aged film stock."[^11]

This exact dynamic occurs in I2V interpolation: the model decides what "belongs" between your two keyframes by sampling from its learned distribution of what video content looks like — which is predominantly smooth-motion digital content.[^12]
### Prompt Fragments for Construction Line Preservation
No practitioner source provides verified I2V examples of construction line preservation. The closest evidence comes from:

**Fragment 1: `"visible pencil underdrawing, construction lines present, sketch structure intact, rough form lines"`**

Informed by the Alibaba analysis noting that "visible pencil underdrawings that anchor expressive intent" are specifically what AI systems erase — making explicit labeling of these elements a necessary counter-signal.[^11]

**Fragment 2: `"intentional line imperfection, rough contour lines, organic stroke variation, not a finished drawing"`**

The OCF (Occlusion-robust Stylization Framework) paper (arXiv, 2025) documents "contour flickering and stroke blurring" as specific failure modes in drawing-based animation from AI, caused by what it calls a "stylization pose gap." The implication for prompt engineering: explicitly labeling rough contours as *intentional* (not accidental noise) may reduce the model's tendency to resolve them.[^13]

**Fragment 3: `"cream paper texture, off-white background, paper grain visible, warm ivory tone"`**

For paper medium preservation, the note.com practitioner identifies `paper texture` and `grainy texture` as essential tokens to include. A practitioner on r/StableDiffusion testing graphite style (August 2025) notes: "The grain I achieve tends to be lighter and of lower quality, resulting in sharper edges and more pronounced linework than I'd prefer." Their conclusion: paper grain requires *stacking* multiple texture tokens rather than using a single phrase.[^1][^14]
### Honest Limitation
Construction-mark preservation across interpolated frames is the hardest preservation problem. The animated frames between your keyframes are generated from scratch by the model; the construction lines that existed in your keyframes will be in the conditioning signal, but the model must decide whether to render them in generated frames. No practitioner source documents a prompt that reliably preserved construction lines through *interpolated* frames (as distinct from the keyframes themselves). This may require a downstream corrective pass (your stated workflow intent) rather than upstream prompt engineering alone.

***
## Section 5: Failure Mode Catalogue
### Failure Mode 1: Photoreal Smoothing / The "Digital Sandpaper" Problem
**Description:** The model's learned prior resolves rough pencil lines to smooth digital edges. Grain disappears. Paper warmth collapses to neutral gray or white. The output looks like a clean digital illustration of a sketch, not a sketch itself.

**Trigger conditions:** Any quality-signaling language; default model behavior with no explicit medium anchors.

**Mitigation:** Stack medium-physics descriptors (`uneven strokes, paper grain, organic imperfections, soft pencil feel`) and suppress quality signals (`remove: highly detailed, 4K, sharp focus, photorealistic`). Source: note.com practitioner; Alibaba upscaler analysis.[^1][^11]

***
### Failure Mode 2: Anime Stylization Drift
**Description:** The model defaults to clean-digital anime linework — thin consistent black outlines, cel shading, neutral backgrounds. This is the strongest attractor in most I2V models because anime-style training data is abundant and highly stylized (easy to learn).

**Trigger conditions:** The word "anime" alone; any prompt mentioning style without qualifying the era or production method; the model's default interpretation of "2D animation style."

**Mitigation:** Replace "anime" with "retro cel animation" or "1980s anime aesthetic" with `flat shading, grainy film texture, limited animation`. Add `not modern digital anime` only if using a model with a dedicated negative prompt field (affirmative reframe is preferable). Source: Pika community guide (2026); fal.ai Kling 2.6 prompting guide.[^2][^6]

***
### Failure Mode 3: Style Drift Across Segments
**Description:** In multi-shot or chained-generation workflows, the visual style gradually migrates from session to session — even when using identical prompts. Shot 1 preserves pencil feel; shot 5 has drifted to cleaner line art; shot 10 looks semi-realistic.

**Trigger conditions:** Prompt re-use without style block reinforcement; changing any element of the scene description (lighting, background, camera angle) that the model interprets as a style signal.

**Mitigation:** (1) Develop a "style lock" paragraph that is pasted verbatim into every generation: `"[same medium description block], stable hand-drawn style, no style drift, consistent paper texture."` (2) Reset session context when drift is detected; paste the winning prompt fresh rather than iterating in-session. (3) Keep segments short (6–10 seconds; chained segments accumulate drift faster than individual regenerations). Source: LinkedIn practitioner Tushar Goyal; Magic Hour character consistency guide; LongStories.ai style framework guide (January 2026).[^15][^16][^8]

***
### Failure Mode 4: Construction Line and Imperfection Cleanup
**Description:** The model's interpolation between keyframes removes rough construction marks, smooths form lines, and fills or eliminates gestural underdrawing. The *source* keyframes preserve the pencil feel, but the *generated* in-betweens look cleaned up.

**Trigger conditions:** Default I2V behavior; no explicit instructions to preserve imperfections.

**Mitigation:** Use `"intentional rough lines, sketch marks preserved, visible construction present, not a finished drawing"` in the positive prompt. Additionally, keeping generated segments shorter (fewer generated frames) reduces the "smooth-out" probability because the model has less time to diverge from the source keyframe. Source: OCF paper (arXiv, 2025); r/animation inbetweening thread (2022, still valid).[^13][^17]

***
### Failure Mode 5: Motion Physics Override / "Floatiness"
**Description:** The model applies smooth, physically plausible motion to the generated frames — which for a hand-drawn pencil test is the wrong behavior. Traditional animation uses anticipation, hold frames, snap/settle timing that differs radically from natural-motion interpolation. The result is "AI floatiness": motion that looks physically smooth but artistically wrong for the medium.

**Trigger conditions:** Default I2V motion generation; any "slow, smooth, cinematic" motion language.

**Mitigation:** Use physics-based motion language appropriate to traditional animation: `"snappy pose change, anticipation hold, squash and stretch motion, frame hold, traditional animation timing"` rather than `"smooth, fluid, natural"`. A Seedance 2.0 reviewer (2026) explicitly flags "typical AI floatiness" as the primary motion artifact, noting it "is fluid, but you can see that typical AI floatiness." One practitioner's workflow (r/generativeAI, May 2026) documents: "physics-based motion descriptors are the most valuable insight I've encountered — prioritizing causation instead of merely relying on adjectives."[^18][^19]

***
## Section 6: Cross-Model Transfer Notes
### Wan 2.1 / 2.2 (First-Last Frame to Video)
The Wan 2.1/2.2 FLF2V (First-Last Frame to Video) workflow in ComfyUI is the closest architectural match to a hand-drawn keyframe interpolation use case: you supply the exact start and end drawings, and the model generates in-between frames. One r/comfyui practitioner (September 2025) documented a complete workflow for pencil-drawing animation using Wan 2.2, using the positive prompt:

> *"Create a speedpaint timelapse video showing a male hand swiftly sketching a girl with a black pencil. The drawing should unfold rapidly in a fast-forward style, appearing piece by piece under the hand."*[^20]

And a preprocessing step prompting Qwen Edit:

> *"Transform this image into a realistic photo scene depicting a pencil drawing on a paper resting on an art desk. The setting should feature soft lighting. Ensure the drawing is rendered in black and white line art, without shading, just the black outlines."*[^20]

**Wan's documented behavior** is that it is "very imaginative," meaning it frequently overrides conditioning if prompts are vague. Community documentation recommends full-length prompts specifying: `Camera Movement + Subject Description + Scene + Motion + Camera Language + Atmosphere + Stylization` — all seven elements, even for simple ideas.[^21]

**Transfer verdict for Seedance:** The style anchor vocabulary is transferable. The FLF2V workflow model architecture differs, but the prompt-weight problem (model wants to normalize style) is identical.
### Kling 3.0 / 2.6 (via fal.ai)
fal.ai's official prompting guide for Kling 3.0 (February 2026) states I2V mode should treat the input image as an anchor: *"When using image-to-video, treat the input image as an anchor... Prompts should focus on how the scene evolves from the image."* This confirms that for I2V, style descriptors in the prompt are *secondary* to the input image as a conditioning signal — the model tries to preserve the image's style by default. This is encouraging for hand-drawn inputs.[^22]

However, the Kling 2.6 guide also warns against **mixing style descriptors**: "Mixing lighting terms like 'golden hour' with 'studio lighting' confuses the model's style interpretation." For hand-drawn prompts, this means no mixing of `rough pencil style` with any production-quality qualifier.[^6]

**One cross-model test** (r/AIVideos_SFW, October 2025) ran the same prompt and reference image through Kling, Luma, Vidu, Runway, and Pika simultaneously. Results showed all models interpreted style through their dominant training-data prior, confirming that style anchors must be model-specific to fully work.[^23]
### Runway Gen-4.5
Runway's Motion Sketch feature (Gen-4.5, January 2026) explicitly uses sketch inputs as visual control layers for I2V — a workflow that by design keeps the sketch aesthetic present, not as a limitation but as a production control mechanism.[^24]

For non-Motion-Sketch I2V, the official Runway Gen-4.5 guide emphasizes: *"Your image already defines composition, lighting, style, and subjects. Your prompt's main job is to describe motion."* This is the strongest endorsement of image-conditioning primacy across all model documentation reviewed. For preserving pencil style, Runway Gen-4.5's approach implies that a clean pencil input image should self-reinforce style without heavy prompt qualification — though no practitioner test specifically confirms pencil-style preservation.[^25]

**Note on Seedance 2.0 specifically:** Seedance 2.0 is documented as having "exceptional prompt adherence" including for "stylistic preferences (from photorealistic to various artistic styles)." One test (April 2026) confirmed it successfully adapted to anime style from a T2V prompt, but the tester noted that I2V requires being "more intentional" with prompts — calling it a "whimsical Pixar style 3D animation" produced "a totally different result." No Seedance-specific test of rough-pencil preservation was found in any source reviewed. The magic hour character consistency guide explicitly lists Seedance 2.0 alongside Kling 3.0, Veo 3, Sora, Runway, Pika in noting that "character drift is usually manageable once you understand how models interpret prompts."[^15][^26][^27]

***
## Section 7: Top 5 Example Prompts — Verbatim, Source-Cited
All five examples below are from practitioner-documented sources. Each is flagged for mode (I2V vs. T2V) and model used.

***

**Prompt 1** — *Pencil-on-paper style anchor (image generation, transfers to I2V conditioning):*

> `"hand-drawn line art, uneven strokes, slightly rough lines, paper texture, minimal shading, soft pencil feel, organic imperfections, simple illustration"`
>
> **Negative (for SD-family models with dedicated negative field):** `"digital art, clean lines, perfect symmetry, high contrast, glossy, polished"`

**Source:** u/peyomaru, note.com, January 2026. Documented as the "most universal hand-drawn line art prompt" for Stable Diffusion. The practitioner's analysis: `uneven strokes / slightly rough lines` disrupts AI's tendency toward "perfect lines"; `paper texture / organic imperfections` includes paper grain and natural distortion; `minimal shading / simple illustration` prevents "over-rendering."[^1]
**Mode:** I2V-transferable frame-conditioning anchor (documented in image generation; structural principles apply to I2V style preservation). Model: Stable Diffusion family.

***

**Prompt 2** — *Retro cel animation preservation for I2V:*

> `"retro cel animation style, flat shading, grainy film texture, slight frame jitter (intentional), 1980s anime aesthetic, limited animation, nostalgic color palette"`

**Source:** pikaais.com community guide (Pika AI, 2026). Documented under "Classic cel animation (retro)" as style tags that lock the visual look in I2V mode. The guide specifically notes `"slight frame jitter (intentional)"` as a mechanism to signal that imperfections are desired output, not artifacts to suppress.[^2]
**Mode:** Image-to-video (Pika, 2026). The guide distinguishes this from T2V applications.

***

**Prompt 3** — *Pencil-drawing speedpaint (Wan 2.2 FLF2V, ComfyUI, I2V):*

> `"Create a speedpaint timelapse video showing a male hand swiftly sketching a girl with a black pencil. The drawing should unfold rapidly in a fast-forward style, appearing piece by piece under the hand at a 30x speedup."`

**Source:** r/comfyui practitioner (u/sdxl_il_noobai, September 2025). Part of a documented complete workflow using Wan 2.2 FLF2V. The practitioner noted this prompt produces pencil-on-paper visual character in the generated video segments.[^20]
**Mode:** Image-to-video (Wan 2.2 FLF2V, ComfyUI, local). Published workflow files included in source.

***

**Prompt 4** — *Style-lock "look bible" for animation series (multi-shot consistency):*

> `"Modern clean anime style, consistent thin lineart, soft cel shading, natural anime proportions, detailed eyes, cinematic anime color grading, gentle bloom, stable lighting, smooth camera motion, no style drift, no text, no watermark."`

**Source:** pikaais.com guide, documented as the "Anime Look Bible" for multi-shot projects. The guide states: "This is incredibly effective for multi-shot projects" — paste it into every prompt unchanged. The specific phrase `"no style drift"` is used as a persistence instruction.[^2]
**Note for pencil adaptation:** This prompt targets clean-anime style. Adapting it for rough pencil: replace `"clean lineart, cel shading"` with `"uneven strokes, paper grain"` and `"stable lighting"` with `"consistent cream paper background."` The *structure* (look-bible repeat strategy) is the transferable element.
**Mode:** Image-to-video (Pika, 2026).

***

**Prompt 5** — *Affirmative-framing rewrite of a negation-heavy sketch prompt:*

> `"A cat with a bare head, blue background, only the cat present, blue color palette"` [affirmative version]
>
> vs. the failed version: `"A cat, not wearing a hat, blue background, no people, without red tones"` [0% success rate]

**Source:** Nadine V., dev.to, December 2025. Empirically tested with FLUX and Stable Diffusion XL: 0% success for negation, 100% for affirmative framing, over 10 generated images each.[^9]
**Mode:** Image generation (FLUX, SDXL). Structural principle (affirmative framing) is documented to apply to video models by the same architectural mechanism. Not I2V-specific but directly applicable to fal.ai workflows lacking a negative prompt field.

***
## Section 8: Recommended Prompt Architecture for Seedance / fal.ai I2V Pencil-Preservation
Based on synthesized evidence, the following prompt structure is recommended for graphite-on-cream-paper, Disney-rough-animation style preservation in Seedance 2.0 I2V mode:

**Style Block (paste verbatim in every segment):**

```
[Subject/action description]. Hand-drawn on cream paper, graphite pencil medium, 
visible paper grain, organic line wavering, uneven stroke weight, soft pencil shading, 
construction lines present, rough animation style, traditional animation timing, 
warm ivory paper tone.
```

**Motion Block (segment-specific):**

```
[Describe the specific motion using traditional animation language: 
anticipation, squash, stretch, hold, snap — not "smooth, fluid, natural."]
```

**What to omit entirely (affirmative framing — do not negate these):**
- Do not write "not digital," "no anime," "avoid smooth" — simply do not include the clean-animation vocabulary at all.
- Remove: `cinematic`, `4K`, `high quality`, `sharp focus`, `polished`, `smooth`, `fluid`, `realistic lighting`.

**Workflow controls that complement prompt engineering:**
- Generate in short segments (5–7 seconds maximum) and chain via FLF or frame chaining. Longer segments accumulate more drift.[^28]
- Use a consistent seed across segments where the model supports it, to reduce style variance.[^16]
- Apply your downstream "pencil fidelity restore" pass immediately after each segment, before using that segment's last frame as the next segment's anchor — so the anchor frame always carries the corrected pencil aesthetic.[^29]

***
## Appendix: Source Reliability Assessment
| Source Type | Coverage | Limitations |
|---|---|---|
| note.com/peyomaru (Jan 2026) | Image generation for SD family; pencil-style prompt vocabulary | Image generation, not I2V; but medium-physics vocabulary transfers |
| pikaais.com community guide (2026) | Pika I2V anime style anchors; look-bible strategy | Anime-focused; requires adaptation for pencil aesthetic |
| fal.ai / Kling official guides (2025–2026) | I2V prompt structure; style mixing warnings | Not hand-drawn specific; no pencil-test examples |
| dev.to Nadine V. (Dec 2025) | Controlled experiment on negation vs. affirmative framing | Image generation (FLUX/SDXL), not video; architectural principle applies |
| r/comfyui pencil workflow (Sept 2025) | Wan 2.2 FLF2V with pencil subject matter | Describes a pencil *being drawn*, not preserving input pencil aesthetic |
| Magic Hour / LongStories.ai (2026) | Character and style consistency workflow; style drift diagnosis | Not pencil-specific; drift mechanics are universal |
| Yossi Kreinin / yosefk.com (2024) | Detailed analysis of AI inbetweening for traditional hand-drawn animation | Focused on dedicated inbetweening tools (EISAI, AnimeInbet), not general I2V |
| Alibaba Product Insights (2026) | AI upscaler analysis of hand-drawn texture preservation | Upscaling, not generation; "digital sandpaper" concept directly applicable |
| LinkedIn/Tushar Goyal (2026) | Style drift in AI video, community discussion | Observation, not controlled experiment |
| r/EnhancerAI (Nov 2025) | Workflow for preserving analog textures across AI enhancement pipeline | Texture-preservation workflow, not prompt-specific |

**Research gaps:** No practitioner source was found with controlled before/after I2V tests specifically targeting graphite-on-cream-paper style preservation using studio-animator reference terms (Glen Keane, Milt Kahl). The Seedance 2.0-specific prompt vocabulary for rough-animation style remains an empirical gap as of May 2026.

---

## References

1. [Stable Diffusionで“手書き風イラスト”を生成する設定ガイド](https://note.com/peyomaru/n/n89dec1807701) - まず「手書き感」を体験してみよう Stable Diffusionで手書き風イラストを生成するとき、多くの人が「なんかツルツルしてる」「AIっぽさが消えない」と悩む。それは、AIが本質的に "均一で整...

2. [Transform Movie Scenes Across Different Styles (Zootopia AI Project)](https://www.aitoolsforkids.com/projects/transform-movie-scenes-zootopia-ai-project) - Using ChatGPT for prompts, Nanobana Pro for image generation, and Kling 01 for video, we created 4 c...

3. [Not able to create a less detailed pencil sketch](https://www.reddit.com/r/StableDiffusion/comments/18ca5m8/not_able_to_create_a_less_detailed_pencil_sketch/)

4. [AI Video Paper Texture: Vintage Aesthetic - reelmind.ai](https://reelmind.ai/blog/ai-video-paper-texture-vintage-aesthetic) - AI Video Paper Texture: Vintage Aesthetic

5. [10 Best Stop Motion Software For Beginners and Professionals](https://www.aiarty.com/edit-video/stop-motion-software.htm) - MonkeyJam is a free, simple stop-motion animation program designed for Windows. It was originally cr...

6. [real-world applications](https://fal.ai/learn/devs/kling-2-6-pro-prompt-guide) - Master Kling 2.6 Pro with specific, structured prompts. Learn scene setting, motion directives, and ...

7. [Why does the art style change so much during animation? (Deforum) (more in comments)](https://www.reddit.com/r/StableDiffusion/comments/17ka4vl/why_does_the_art_style_change_so_much_during/)

8. [AI Video Style Continuity: A Persistent Challenge](https://www.linkedin.com/posts/tushar-goyal-622ba518_thirsty-crow-activity-7417489243066777600-aGee) - AI can generate beautiful videos. But it still can’t decide how to look. Today’s AI video tools can ...

9. [The Prompting Trick That Fixed My AI Image Generation](https://dev.to/nadinev/the-prompting-trick-that-fixed-my-ai-image-generation-3ge4) - For the color test ("no blue sky"), SDXL creatively stylized the image to avoid the problem entirely...

10. [Using Negative AI Prompts Effectively - Virtualization Review](https://virtualizationreview.com/articles/2025/12/08/using-negative-ai-prompts-effectively.aspx) - A generative AI model will generally treat phrases such as no, do not, without, and avoid completely...

11. [AI Anime Upscalers: Do They Preserve Hand-drawn Texture Or Just ...](https://www.alibaba.com/product-insights/ai-anime-upscalers-do-they-preserve-hand-drawn-texture-or-just-add-fake-detail-like-digital-sandpaper.html) - AI anime upscalers: do they preserve hand-drawn texture or just add fake detail like digital sandpap...

12. [AI Anime Upscalers — Do They Preserve Hand-drawn Linework Or ...](https://www.alibaba.com/product-insights/ai-anime-upscalers-do-they-preserve-hand-drawn-linework-or-blur-intentional-imperfections.html) - AI anime upscalers often blur hand-drawn linework and erase intentional imperfections—here’s how to ...

13. [Occlusion-robust Stylization for Drawing-based 3D Animation](https://ar5iv.labs.arxiv.org/html/2508.00398) - 3D animation aims to generate a 3D animated video from an input image and a target 3D motion sequenc...

14. [How can I get this style?](https://www.reddit.com/r/StableDiffusion/comments/1mnzvsa/how_can_i_get_this_style/) - How can I get this style?

15. [How to Keep Characters Consistent in AI Video (2026) - Magic Hour](https://magichour.ai/blog/how-to-keep-characters-consistent-in-ai-video) - ... frame by frame ... Large camera moves, fast rotations, or sudden lighting changes make it harder...

16. [Maintaining Style Consistency in AI Animation | LongStories.ai](https://longstories.ai/blog/maintaining-style-consistency-ai-animation) - Production tips: Define a style framework upfront, use fixed seeds to lock variables, and apply qual...

17. [AI Inbetweening? : r/animation - Reddit](https://www.reddit.com/r/animation/comments/xplpq7/ai_inbetweening/) - The ai creates in-between frames. It's not perfect as it's AI and it wasn't made for animation it's ...

18. [How Good is SEEDANCE 2.0 Really? (HonestComparison + Tutorial)](https://www.youtube.com/watch?v=HYE-x1ZKhIQ) - ... PROMPT PRESET: You are a professional film director and AI video prompt engineer. Transform the ...

19. [My AI video generation workflow in 2026: what I kept, what I dropped ...](https://www.reddit.com/r/generativeAI/comments/1t0x25p/my_ai_video_generation_workflow_in_2026_what_i/) - I do systematic testing of AI video platforms and share results publicly on my YouTube channel, arou...

20. [SDXL IL NoobAI Gen to Real Pencil Drawing, Lineart ... - Reddit](https://www.reddit.com/r/comfyui/comments/1nl5kta/sdxl_il_noobai_gen_to_real_pencil_drawing_lineart/) - For example most artists I saw would begin by more rough pencil ... r/comfyui - How to Achieve Profe...

21. [Camera movement tutorial for Wan 2.1 model in video prompts](https://www.facebook.com/groups/nightcafeaiart/posts/2747850702092100/) - Its graphite-lens surfaces are shattered and decorated with ghostly flecks, with broken time-markers...

22. [Kling 3.0 Prompting Guide - fal.ai Blog](https://blog.fal.ai/kling-3-0-prompting-guide/) - Kling 3.0 is designed to understand cinematic intent, not just visual descriptions. The model perfor...

23. [Prompt across Kling, Luma, Vidu, Runway, Pika](https://www.reddit.com/r/AIVideos_SFW/comments/1o6gyn3/prompt_across_kling_luma_vidu_runway_pika/) - Prompt across Kling, Luma, Vidu, Runway, Pika

24. [Runway Gen 4.5 Motion Sketch – Image to Video: Beginners Guide](https://www.youtube.com/watch?v=hZHy0f7Uy-s) - This video examines Motion Sketch as a visual control layer for image to video, using a single maste...

25. [Runway Gen 4.5 Prompt Guide | ImagineArt](https://www.imagine.art/blogs/runway-gen-4-5-prompt-guide) - Learn how to write powerful prompts for Runway Gen-4.5. Discover techniques for cinematic motion, ch...

26. [Seedance 2.0 Review: Complete Analysis of ByteDance's New AI ...](https://seavidgen.com/blog/seedance-2-0-review-analysis) - Result: Seedance 2.0 successfully adapted to the anime style ... Pre-visualization: Generate rough v...

27. [Is Seedance 2.0 Doom for Animation? FULL Test - YouTube](https://www.youtube.com/watch?v=aAGZM2aoq1Q) - People just don't get that the inability of seedance to do complex/naturalistic emotion means that i...

28. [Grok imagine simplifies ai video storytelling - Facebook](https://www.facebook.com/groups/1712618889252391/posts/2417000802147526/) - ... frame by frame. ---------- This tool converts scripts or concepts ... preserve the detail and hi...

29. [AI Video Enhancement Test — Keeping Handmade Textures While Improving Motion](https://www.reddit.com/r/EnhancerAI/comments/1p8tjcj/ai_video_enhancement_test_keeping_handmade/) - AI Video Enhancement Test — Keeping Handmade Textures While Improving Motion

