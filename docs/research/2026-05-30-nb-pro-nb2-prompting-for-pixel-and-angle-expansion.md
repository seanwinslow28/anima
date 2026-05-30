# Prompting NB Pro & NB2 for the mascot — pixel grids, angle expansion, and the model choice

*2026-05-30. Research synthesis commissioned after the production-bake session held the mascot re-bake on a reference-gap finding: the legless octopus anchor has no standing pose, so NB Pro invented a biped for the `body-3quarter`/`body-back` turnarounds. This doc answers the two questions that pass raised — how to prompt NB Pro/NB2 for the pixel register, and how to expand a character to new angles from limited references — and applies both directly to the mascot dedicated pass and the Cy workflow. Three of the findings flip an assumption the pipeline currently bakes in.*

---

## The one-paragraph answer

You cannot prompt your way to a faithful mascot turnaround from one flat sprite, and you were right to stop trying. Two structural facts: (1) **pixel-grid fidelity is a post-process problem, not a prompt problem** — every NB model paints "pixel-looking" art at 1024px with sub-pixel noise and 6px-vs-7px cells, and no prompt snaps it to a grid; the fix is a downsample-and-quantize pass after generation. (2) **Angle expansion works by giving the model multiple views in a single reference image** — front + 45° + 90° — which lets it do "photogrammetric inference" (estimate the 3D shape and re-render new angles); from one view it has nothing to infer and invents. The mascot reference gap is therefore real and unpromptable: the move is to *author the additional views first*, lock them as a multi-view reference sheet, then let Cy expand. And the model itself is worth reconsidering — **NB2 (gemini-3.1-flash-image-preview) is reported to beat NB Pro on cross-generation character consistency**, which is what the pixel register actually needs, even though Pro wins on texture/lighting (which pixel art doesn't use). A small NB2-vs-Pro bake-off on the mascot is cheap and may be the single highest-leverage change.

---

## Finding 1 — The integer-pixel-grid rule is unenforceable at the prompt layer

The mascot Bible's `IR.claude-mascot.style.integer-pixel-grid-no-subpixel` and `…no-gradient-interpolation` rules were *visually violated* on the generated plates (soft-edged shading, anti-aliased diagonals) and Gemini passed them anyway. The research explains why this is structural, not a prompt failure:

> "Nano Banana typically generates images at high resolution (usually 1024×1024), but the pixels aren't snapped to a consistent grid, with sub-pixel noise everywhere. Colors bleed between what should be hard edges, some 'pixels' are 6px wide while others are 7px… Rather than fighting the model to get perfect pixel snapping in the prompt (which it won't achieve), focus on getting the right character design, pose, and color palette, then **fix the grid in post-processing.**" — SpriteCook

Prompt hygiene still helps the *design* ("no anti-aliasing," "limited color palette," "clean outlines" are worth including), but it will never produce a true integer grid. The model paints an *impression* of pixel art.

**What this means for anima.** The pixel register needs a **post-process node** that the pencil register doesn't: after NB generation, nearest-neighbor downsample 1024px → the target sprite resolution, then quantize to the locked 4-color palette (`#E89B6B / #F4DDB8 / #A86B45 / #5C3A24`). That single step makes `integer-pixel-grid-no-subpixel` *true by construction* instead of *hoped for in the prompt* — and it makes the rule mechanically checkable (count unique colors == 4; assert every edge lands on the grid). This is the pixel-register analogue of "the runner owns identity": for pixel art, **the post-processor owns the grid.** It also fixes the Phase-7 similarity-gate noise on the mascot — quantized plates compare far more stably than soft-edged ones.

## Finding 2 — Angle expansion is "photogrammetric inference," and it needs more than one view

This is the direct answer to the mascot reference gap. The technique practitioners use to get consistent turnarounds:

> "The recommended approach is generating a single image containing three views: a direct frontal shot, a 45° profile, and a full 90° side profile. Uploading this sheet provides the model with a complete 3D understanding of the character's head structure… the model performs a 'Photogrammetric Inference.' It estimates the depth map and bone structure… **It extracts the shape of the face, not the pixels of the face.**" — Nano Banana three-view guides

The mechanism is the crux: NB infers geometry from *multiple* views and re-renders unseen angles from that inferred 3D shape. **From a single view it has no geometry to infer, so it falls back to a prior — and its prior for "3-quarter body turnaround" is a standing biped.** That is exactly the gingerbread-man the mascot pass produced. It is not prompt-dominance and not a model defect; it is the model doing the only thing it can with one reference.

**What this means for anima.** The production-bake report's instinct ("add a true multi-angle reference") is precisely right, and the research sharpens the *form*: not several separate images, but **one reference sheet containing front + 45° + side (+ back) in a single image**, on a neutral isolating background. That is what unlocks photogrammetric inference. The supporting prompt structure:

> "Create a professional Character Design Sheet… Composition: split view showing the character from Front view, Side view, Back view. Pose: Static A-Pose. Style: [register]. Background: neutral grey/white to isolate the silhouette." — plus **trait-locking**: reuse the exact same descriptive tokens verbatim in every generation (don't drift "emerald eyes" → "green eyes").

**The bootstrap catch, stated honestly:** photogrammetric inference needs the multiple views to *exist first*. The octopus has one. So someone has to author the additional canonical views before the technique applies — you can't infer 3D from 1 image. That's the real work of the mascot pass, and it's Finding 4.

## Finding 3 — For the pixel register, NB2 may be the better model than NB Pro

anima currently routes both registers to NB Pro (`gemini-3-pro-image-preview`). The research suggests that's backwards for the mascot:

- **NB2 (`gemini-3.1-flash-image-preview`) is reported to hold character consistency better across multiple generations** — "Nano Banana 2 delivered better results and kept the character consistent across all outputs" (Google's claim, corroborated by third-party testing). Consistency across views is exactly what a turnaround set needs.
- **NB Pro wins on texture richness, natural lighting, and spatial composition** — none of which pixel art uses. Pro reaches higher *absolute* quality; NB2 reaches ~95% of it far faster and cheaper.
- Both are equally bad at the literal grid (Finding 1), so that's a wash settled by post-processing either way.
- This dovetails with the earlier Google-dev-forum finding that NB **Pro** specifically regressed on multi-reference fidelity since the 3.1 launch ("downsamples references… generic outputs"), while NB2 is the more consistent path.

**What this means for anima.** Run a small **NB2-vs-NB-Pro bake-off on the mascot**, scored with the now-installed DINOv2 tier. If NB2 holds the octopus identity better across the view set, route the `pixel-art-8bit` register to NB2 and keep `pencil-test-colored` on NB Pro (Pro's texture/line richness genuinely helps the pencil look). That's a per-register model assignment, which the v2 manifest already supports — a clean, cheap, possibly decisive change. Pencil register: stay on Pro. Pixel register: probably switch.

## Finding 4 — How to produce the lockable mascot reference set (three paths)

Sean's plan — "come into a Cy session with a few locked assets so he can expand" — is the right shape. The question is how to *make* those 2–4 canonical views of a creature that only exists in one. Three paths, cheapest first:

1. **NB2 generate-then-clean-then-lock.** Feed the single octopus anchor to NB2 with an explicit "turn this exact creature to a 45°/side/back view, same palette, same proportions, no new limbs" prompt; generate candidates; **hand-pick and hand-clean** the few that hold the form; run them through the Finding-1 post-process; lock them as `source-refs/` multi-view material. Cheapest, fastest, but each new view is a small identity gamble you curate by eye. *Best first attempt.*
2. **A pixel-art-specialized tool or LoRA.** Retro Diffusion / RD-Animation (purpose-built for sprite sheets and multi-direction poses with shared palette/line/shading), or a pixel LoRA (Pixel Art XL, or Z Image Turbo's pixel LoRA — reported to hold dithering + proportions better than SDXL). These are built for exactly "consistent sprite across poses from one reference." More setup, more register-faithful output. *Best if path 1's curation gets tedious.*
3. **Train a character LoRA on the octopus.** The Bible's `flux_lora_seed_plates` field already anticipates this. Heaviest (needs a handful of clean octopus images and a training run on a 4090), but it's the only path that makes the creature *reproducible at will* in any view — the durable fix if the mascot becomes load-bearing for a real piece. *Reserve for when the mascot earns it.*

**The honest constraint that precedes all three:** a legless crouched creature may not *have* a meaningful "standing 3-quarter body" view. Before authoring anything, decide the mascot's real view vocabulary — front / profile-L / profile-R / back, all *in-character* (crouched), and maybe no "standing body" plate at all. Authoring references for views the creature doesn't have is how the gingerbread-man got in. **Redefine the plate set to the creature, then source references for that set.**

## Prompt templates (drop-in)

**Pixel-art turnaround sheet (NB2), from a multi-view reference once you have one:**

> *[attach the multi-view octopus reference sheet as Image 1]*
> "Image 1 is the canonical reference for this creature. Render a turnaround sheet of the *exact same creature* — same four-color palette, same round-lozenge body, same stub legs, same snout, same eye dots. Views: front, 45°, side, back, all in the creature's natural crouched pose. Do NOT add arms, legs, or limbs the reference does not have. No anti-aliasing, hard pixel edges, limited palette, clean outlines. Neutral white background. No text or labels."
> *→ then post-process: nearest-neighbor downsample to target px + quantize to the 4 locked hexes.*

**Trait-lock token block (reuse verbatim every generation):** `round-topped lozenge silhouette · primary orange #E89B6B body · cream #F4DDB8 crown highlight · warm-brown #A86B45 shadow · deep-brown #5C3A24 eye dots + mouth stroke · stub legs, no arms · snout-nose, no muzzle · chibi 2:3 head-to-body`.

The discipline mirrors the pencil-fix lesson: **terse intent + a strong reference + trait-locked tokens beats a long verbal description.** The verbose-prose-loses rule that bit `focused` applies to the mascot too.

---

## What this changes — recommendations for the mascot dedicated pass

1. **Redefine the mascot plate vocabulary first** (taste decision, Sean's): which views a crouched legless creature actually has. Probably drop "standing body" plates entirely. *(Blocks everything else — do it first.)*
2. **Author a multi-view reference sheet** via Finding 4 path 1 (NB2 generate-then-clean) for the redefined view set; lock it into `source-refs/`. This is the asset Cy expands from.
3. **Add a pixel-register post-process node** (downsample + 4-color quantize) so `integer-pixel-grid-no-subpixel` is true by construction and mechanically checkable — not a prompt's hope. Pencil register skips this node.
4. **Bake off NB2 vs NB Pro on the mascot**, scored with DINOv2; route the pixel register to whichever holds identity, likely NB2. Per-register model assignment in the manifest.
5. **Re-bake the mascot plates-only** against the richer source-refs + the chosen model + the post-process node. The reference gap is closed by step 2; the grid by step 3; the consistency by step 4.

This also generalizes the **Cy workflow** the way Sean intuited: Cy authors best when she *expands from a small set of locked, multi-view assets* rather than extrapolating from one flat image. The `source-refs-checklist` already invites turnarounds and motion refs — the lesson is that for any non-trivial character, "drop a real multi-view sheet" should move from *strongly recommended* to *required before authoring*, because single-view authoring is where reference-gap drift is born.

## Open questions to validate empirically (the project's "empirical, not vibes" rule)

- Does NB2 actually out-hold the octopus vs NB Pro on the redefined view set? (Bake-off + DINOv2 settles it.)
- Does the downsample+quantize post-process preserve the creature's read at the target sprite resolution, or does it crush the snout/legs at small px? (Render and eyeball.)
- Is path-1 (generate-then-clean) curation good enough, or does the octopus need path-3 (LoRA) to stay itself across views? (Try cheap first; escalate only if curation fails.)

---

## Sources

- [SpriteCook — Turning Nano Banana 2 AI Images into Actual Pixel Art](https://www.spritecook.ai/blog/nanobanana-pixel-art-for-games)
- [Nano Banana three-view / orthographic sheet generation](https://nanoprompts.org/use-cases/character-creative-transformation/three-view-generation)
- [pIXELsHAM — Creating a character reference sheet for AI using Nano Banana](https://www.pixelsham.com/2026/04/18/creating-a-character-sheet-for-ai-videos-using-nano-banana/)
- [Atlabs AI — Turn one image into multiple camera angles with Nano Banana Pro](https://www.atlabs.ai/blog/turn-one-image-into-multiple-camera-angles-nano-banana-pro)
- [Nano Banana Pro character-sheet prompt library](https://nanobanana.pro/character-sheet-prompt)
- [AIToolsSME — Nano Banana 2 vs Pro, tested](https://www.aitoolssme.com/blogs/nano-banana-pro-vs-nano-banana-2)
- [Beebom — Nano Banana 2 vs Nano Banana Pro: Bigger Isn't Always Better](https://beebom.com/nano-banana-2-vs-nano-banana-pro-comparison/)
- [Google — Nano Banana 2 announcement](https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/)
- [Mage — Best AI Pixel Art Generators 2026](https://blog.mage.space/article/best-ai-pixel-art-generators-2026/83330b2b-607d-4ef3-bca0-19e8ef307e2e)
- [Apatero — Z Image Turbo Pixel Art LoRA guide](https://apatero.com/blog/z-image-turbo-pixel-art-lora-complete-guide-2025)
- [Picasso IA — RD-Animation (Retro Diffusion) sprite generator](https://picassoia.com/en/collection/text-to-image/retro-diffusion-rd-animation)
