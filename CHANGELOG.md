# Changelog

## Run: run_2026-04-04_174805

### Phase 2: In-Between Generation — OpenPose ControlNet → Gemini Workflow

**Date:** 2026-04-06

**What was discovered:** A two-stage pipeline for generating animation in-between frames that maintains style and identity consistency with the approved keyframes.

**Stage 1 — Pose extraction and interpolation (ComfyUI):**
1. Extract DWPose skeletons from approved keyframes using `comfyui_controlnet_aux` (OpenPose ControlNet)
2. Blend skeleton pairs at easing ratios (Odd Rule: 1:3:5:7 for ease-in/out, linear for even spacing)
3. Output: colored stick-figure skeleton images showing the intermediate pose

**Stage 2 — Character generation (Gemini Nano Banana Pro 2):**
1. Pass 3 reference images to `gemini-3.1-flash-image-preview`:
   - Image 1: A-2 anchor (identity lock)
   - Image 2: Previous approved keyframe (style continuity)
   - Image 3: Interpolated skeleton (pose reference)
2. Prompt describes the specific movement and expression for this in-between
3. Output: pencil test drawing matching the established style

**What was tried first (and failed):**
SD 1.5 with OpenPose ControlNet + IPAdapter in ComfyUI was tested for end-to-end generation. The pose control was accurate but the output had severe identity drift, wrong clothing (light teal instead of navy), inconsistent backgrounds, and a completely different art style from the Gemini-generated keyframes. The style gap between SD 1.5 and Gemini was too wide to bridge with prompting or IPAdapter weight tuning.

**Why the two-stage approach works:**
- ComfyUI/OpenPose handles what it's good at: precise skeletal pose extraction and interpolation
- Gemini handles what it's good at: maintaining character identity, pencil test style, and clothing consistency from reference images
- The same engine (Gemini) that produced the keyframes produces the in-betweens, eliminating style mismatch
- This mirrors the traditional animation workflow: roughs/pose planning first, then clean character pass

**Results:**
- 9 in-betweens generated across 5 transitions (F01→F06, F06→F10, F10→F13, F31→F36, F36→F40)
- 6 of 9 passed first attempt with correct identity, style, and clothing
- 3 had clothing color drift (shirt went white/gray) — fixed with stronger "DARK NAVY BLUE t-shirt" prompt language
- F13→F18 transition deferred (needs manual skeleton editing in Procreate for arc motion)

**Easing ratios used:**

| Transition | Count | Ratios | Type |
|-----------|-------|--------|------|
| F01→F06 | 3 | 0.14, 0.43, 0.71 | Ease-out (slow settle) |
| F06→F10 | 1 | 0.50 | Linear (head snap) |
| F10→F13 | 1 | 0.50 | Linear |
| F31→F36 | 2 | 0.33, 0.67 | Linear (nod) |
| F36→F40 | 2 | 0.29, 0.71 | Ease-in (settle to idle) |

**Prompt files:** `prompts/in-betweens/` — 9 prompt text files with reference image notes.

**Key infrastructure created:**
- `workflows/skeleton_extract.json` — DWPose skeleton extraction
- `workflows/skeleton_blend.json` — Skeleton interpolation at specified ratio
- `workflows/openpose_inbetween.json` — Full ComfyUI generation workflow (used for SD 1.5 test, retained for reference)
- `pipeline/generate_inbetweens.py` — Batch orchestration script (ComfyUI API)
- `docs/phase2-model-requirements.md` — Model download manifest

**Models installed in ComfyUI (`/Users/seanwinslow/Code-Brain/Comfy-UI/models/`):**
- `v1-5-pruned-emaonly.safetensors` (4.0 GB) — SD 1.5 checkpoint
- `control_v11p_sd15_openpose.pth` (1.3 GB) — OpenPose ControlNet
- `ip-adapter_sd15.safetensors` (43 MB) — IPAdapter (used for SD 1.5 test)
- `sd1.5_model.safetensors` (2.4 GB) — CLIP Vision ViT-H
- `vae-ft-mse-840000-ema-pruned.safetensors` (319 MB) — VAE

**Custom nodes installed:**
- `comfyui_controlnet_aux` (Fannovel16) — DWPose skeleton extraction
- `ComfyUI_IPAdapter_plus` (cubiq) — IPAdapter nodes

**Lessons learned:**

1. **Use the same generation engine for keyframes and in-betweens.** SD 1.5 and Gemini produce fundamentally different styles. Mixing engines creates uncanny mismatches even with ControlNet + IPAdapter identity lock.
2. **Separate pose control from character generation.** ComfyUI excels at pose extraction/interpolation; Gemini excels at style-consistent character rendering. Each tool does what it's best at.
3. **Clothing color drift requires explicit prompt reinforcement.** Without "DARK NAVY BLUE t-shirt (not white, not gray)" the model occasionally defaults to lighter clothing. The keyframe reference alone isn't enough — explicit color callouts are needed.
4. **Three reference images is the sweet spot for in-betweens:** identity anchor + previous keyframe + pose skeleton. More references risk bleed; fewer lose consistency.
5. **OpenPose skeletons are readable by Gemini.** No mannequin intermediary step was needed — Gemini interprets DWPose colored stick-figure skeletons directly as pose references.
6. **ComfyUI Desktop runs on port 8000, not 8188.** The default API port differs from standalone ComfyUI installations.

---

### Phase 3: Sprite Transformation Sequence (F20-F28)

**What was created:** 5 full-frame transformation images showing pencil trail lines from F18's gesture evolving into the RPG warrior sprite. These replace the static F18 hold (frames 18-30) with an animated metamorphosis.

**Approach — full-frame generation, not overlays:**
Gemini can't produce true alpha transparency, and the assembly pipeline has no compositing step. Following the F31/F36 precedent (sprite baked in using red circle technique), each transformation frame is a complete 1376x768 image with Sean holding his F18 pose while the pencil marks evolve.

**The 5-frame sequence:**
| Frame | Hold | Description |
|-------|------|-------------|
| F20 | 2 | Pencil trails intensify — 8-10 overlapping lines converging |
| F22 | 2 | Abstract swirl — tight cluster of circular scribble strokes |
| F24 | 2 | Silhouette emergence — spiky hair points recognizable |
| F26 | 2 | Clear form — RPG warrior identifiable, residual pencil wisps |
| F28 | 3 | Fully formed sprite with bounce squash, speed lines below feet |

Total: 13 frames (same as the original F18 hold). 42-frame count preserved.

**Reference image strategy — graduated sprite introduction:**
- F20/F22: Only F18 + A-2/previous frame. No sprite references — prevents premature formation.
- F24: concept_B.png added as silhouette guide (lighter identity pressure than turnaround).
- F26/F28: turnaround_01.png for full identity lock, with "ONE drawing on the page" constraint.

Each frame chained to the previous approved transformation frame to maintain spatial continuity of the swirl-to-sprite metamorphosis.

**Key decisions:**
- Started transformation at F20 (not F24 as originally planned) to avoid a dead 4-frame hold before motion begins. 5 frames = ~0.83s at 12fps, enough for the hero moment to register.
- Used concept_B (single standing sprite) for the silhouette stage instead of the turnaround sheet — lighter identity pressure at the half-formed stage.
- All frames passed on first attempt — the sequential chaining and graduated reference strategy produced consistent results.

**Lesson learned:**
- **Graduated reference introduction controls formation timing.** By withholding sprite references from early frames and only introducing the turnaround at the nearly-formed stage, the model naturally produces abstract pencil energy first and detailed character second. This is more reliable than describing "don't draw the full character yet" in the prompt.
- **Sequential chaining maintains spatial coherence for multi-frame effects.** Each transformation frame inheriting its predecessor's swirl position prevents the convergence point from jumping around frame-to-frame.

---

### F13 — Wind Up (A-5): Pose redesigned for continuity

**Original storyboard:** Right arm raised with elbow leading, stylus at head height, body coils forward in anticipation pose — classic animation wind-up before the F18 sweeping gesture.

**What happened:** Initial generation (attempt_01) placed the stylus in the character's LEFT hand despite the prompt specifying right. Attempt_02 used a heavily reinforced "CRITICAL CONTINUITY" prompt block with camera-left/camera-right callouts, but the 3/4 angle made the hand assignment ambiguous. F18 consistently generated with the RIGHT arm sweeping forward — fighting both frames to match wasn't working.

**Resolution:** Sean manually regenerated F13 with a new pose: left arm extended forward with a thumbs-up gesture, stylus held in the right hand down at his side. This creates a natural flow into F18 where the right arm sweeps forward with the stylus.

**Lesson learned:**
- **Adapt choreography to what the model produces well, don't fight it.** When the model consistently generates a gesture a certain way, redesign the surrounding frames to match rather than adding more constraint text.
- **Camera-left / camera-right callouts in prompts are unreliable** for specifying which hand holds a prop at 3/4 angles. The model interprets "right hand" relative to the character's body orientation, which shifts with the 3/4 pose.
- **Continuity audit should run BEFORE assembly, not after.** The hand-swap between F13 and F18 would have been caught earlier with a pairwise visual check.

---

### F18 — Mid-Gesture (A-6): Reverted to original generation

**What happened:** After the F13 continuity issue, attempt_02 of F18 was generated with a left-hand-forward-push gesture to match the (since-replaced) F13. When F13 was redesigned by Sean, the original F18 attempt_01 (right-arm sweep) was restored.

**Lesson learned:**
- **Keep all candidates.** The artifact preservation principle from the sprite pipeline paid off — attempt_01 was available to restore without re-generating.

---

### F31 — Sprite Lands (A-7): Evolved through multiple iterations

**Original storyboard:** Sean looks at his left shoulder where a tiny pixel sprite has landed. The sprite is composited separately.

**Iteration 1 — Sprite drawn despite "DO NOT" instruction:**
The initial F31 generation drew a tiny stick figure on the shoulder despite the prompt containing "DO NOT draw the sprite" twice. Lesson: negative instructions are weaker than positive ones for Gemini. The model sometimes ignores negatives when the surrounding context describes the thing being excluded.

**Iteration 2 — Sprite removed for clean compositing:**
The stick figure was patched out using PIL (sampling clean paper texture from above the sprite area and pasting it over). Later, Sean used Google AI Studio for a cleaner edit. This created a sprite-free F31 for potential compositing workflows.

**Iteration 3 — Universal game sprite baked in (first attempts):**
Pivoted from compositing to baking the sprite directly into the frame. First attempts used the 16BitFit sprite references, which produced a "tiny jacked person" rather than a recognizable game sprite. Also placed on the wrong shoulder (camera left instead of camera right). Lesson: detailed realistic character references push the model toward miniature realism, not game-sprite iconography.

**Iteration 4 — RPG warrior sprite with red circle marker (final):**
Three sprite concept directions were explored:
- **Concept A:** Retro platformer hero (Mega Man-style helmet, armor)
- **Concept B:** RPG warrior (spiky JRPG hair, tunic, sword) — **selected**
- **Concept C:** Minimal arcade hero (square head, dot eyes, maximum simplicity)

A character turnaround sheet was generated from Concept B to lock the design. The final F31 was generated using:
1. Sean's red-circle-marked F31 image (red oval drawn on the correct shoulder as a visual placement guide)
2. The sprite turnaround sheet as character reference
3. Prompt instructing to "replace the red circle with the sprite character and remove the red circle"

**Why the red circle technique works:** Text-based spatial instructions ("put it on the LEFT shoulder, which is camera RIGHT") are unreliable — the model confuses character-relative vs camera-relative directions. A visual marker on the actual image removes all ambiguity. The prompt only needs to say "put it where the red circle is."

**Final result:** `attempt_with_sprite_03.png` — RPG warrior sprite sitting on the correct shoulder, red circle fully removed, Sean's pose preserved.

---

### F36 — The Nod (A-8): Sprite added with same technique

**What happened:** Same red circle marker + turnaround reference technique as F31. First attempt (attempt_with_sprite_03) bled the turnaround sheet views into the background — the model reproduced all 5 turnaround views alongside Sean. Fixed in attempt_04 by adding explicit "do NOT draw the turnaround views, ONLY Sean with the tiny sprite, ONE drawing on the page" constraints.

**Lesson learned:**
- **Reference images can bleed into output composition.** When using a multi-view turnaround sheet as reference, the model may try to reproduce the sheet layout. Counter with explicit "output shows ONLY one character" instructions.
- **Tighter, more direct prompts recover from reference bleed.** The retry prompt was shorter and more emphatic about the single-figure output, which worked.

**Final result:** `attempt_with_sprite_04.png` — Sean doing the nod with sprite on shoulder mirroring the gesture.

---

### Sprite Character Design: RPG Warrior (S-1)

**Why a universal game sprite instead of the 16BitFit character:**
The original storyboard referenced Sean's 16BitFit pixel art character. Initial attempts used the 16BitFit sprite reference images (muscular blonde fighter in tank top and blue pants), but the results looked like "a tiny jacked version of my character sitting on his shoulder" — too realistic, not enough "video game sprite" energy. The sprite needs to read as a game character at any size, including when scaled down to ~15% of Sean's head height on his shoulder.

**Design exploration:**
Three concepts generated without character references (to let the model produce universally recognizable game archetypes):
- **Concept A (S-A):** Retro platformer hero — Mega Man-esque helmet, armor, fist raised
- **Concept B (S-B):** RPG warrior — spiky JRPG hair, tunic, belt, sword, determined expression — **SELECTED**
- **Concept C (S-C):** Minimal arcade hero — square head, dot eyes, waving, maximum simplicity

Concept B was selected because it has the strongest "video game character" silhouette at small sizes — the spiky hair is iconic and readable even at thumbnail scale.

**Assets produced:**

| Asset | File | Dimensions | Purpose |
|-------|------|-----------|---------|
| Standing idle | `candidates/sprite/concept_B.png` | 896x1200 | Original design reference |
| Turnaround sheet | `candidates/sprite/turnaround_01.png` | 1376x768 | 5-view reference (front, 3/4, side, 3/4 back, back) for consistent reproduction |
| Seated idle | `candidates/sprite/seated_sprite_01.png` | 896x1200 | Standalone seated pose for compositing backup if video models have trouble |

**How the turnaround was created:**
Used the `gemini-pencil-animation-image-gen` skill with the Template 4 (Turnaround Sheet) structure from `pencil-animation-prompt-templates.md`, adapted for sprite proportions. Key additions to the standard template:
- "CRITICAL — MAINTAIN SPRITE PROPORTIONS" block preventing the model from correcting toward realism
- Explicit "3 heads tall" ratio constraint
- "blocky, angular, iconic" repeated to reinforce game-sprite aesthetic
- Concept B passed as `--reference` for identity locking

**How the seated sprite was created:**
Same skill, with the turnaround as reference, requesting a seated pose with "legs dangling over the edge" for shoulder-sitting compositing. Matched to concept_B dimensions (896x1200) so it can be used as a drop-in compositing asset.

---

### Assembly: Resolution normalization required

**What happened:** Sean's manually generated F13 was 2752x1536 (matching the anchor) while Gemini-generated frames were 1376x768. The mixed resolutions caused visual jumps in the first assembly. Additionally, the original GIF was encoded at fps=15 (resampled from 12fps source), which created 53 frames and blurred the F13/F18 transition.

**Resolution:** All frames normalized to 1376x768 via PIL before assembly. GIF encoding changed from fps=15 to fps=12 (native) for exact 42-frame output. The assembly pipeline now uses a Python pre-step that opens each frame with PIL, resizes to 1376x768 if needed, and saves as PNG before FFmpeg encoding.

**Lesson learned:**
- **Normalize frame dimensions in the assembly pipeline** before encoding. Mixed resolutions from different sources (anchor image, Gemini generations, manual edits from AI Studio) are inevitable.
- **Encode GIF at the native framerate** (12fps) rather than resampling to 15fps. Resampling hold-based keyframe animation creates frame interpolation artifacts.

---

### Pipeline: Continuity audit added

**What was added:** `pipeline/continuity_audit.py` — a post-run review script that checks 8 continuity dimensions (stylus hand, stylus presence, clothing, facing direction, scale, hair, feet, expression arc) across all consecutive frame pairs. Generates structured Claude Code vision review prompts.

**Why:** The F13 hand-swap was caught during manual review but should have been caught systematically. The continuity audit formalizes this as a pipeline step.

---

### Prompt Technique: Red Circle Visual Marker

**What it is:** Draw a red circle or oval directly on the reference image at the exact location where you want the model to place a new element. In the prompt, instruct the model to "replace the red circle with [element] and remove the red circle."

**Why it works:** Text-based spatial instructions ("put it on the LEFT shoulder, which is camera RIGHT") are fundamentally ambiguous for image models. The model confuses:
- Character-relative left/right vs camera-relative left/right
- "Left shoulder" at different body angles
- Spatial descriptions that require understanding 3D space from 2D reference

A visual marker removes ALL spatial ambiguity. The model can see exactly where the red circle is and place the element there. It's the difference between giving someone written directions vs pointing at a map.

**How to apply:**
1. Duplicate the approved frame
2. Draw a red circle/oval at the exact placement location (use any tool — Procreate, Preview, AI Studio)
3. Save as a separate file (don't overwrite the approved frame)
4. Pass as reference to Gemini with prompt: "Replace the red circle with [description]. Remove the red circle completely."

**Limitations:**
- The model sometimes leaves faint red artifacts — inspect the output
- Works best with high-contrast markers (red on cream paper is ideal)
- The marker should be simple (circle/oval) — complex shapes may confuse

---

### Prompt Technique: Reference Image Bleed Prevention

**What it is:** When using a multi-element reference image (turnaround sheet, expression sheet, sprite sheet), the model may reproduce the reference layout instead of extracting just the character identity.

**How to prevent:**
- Add explicit constraints: "Output shows ONLY one character. ONE drawing on the page. Do NOT reproduce the reference sheet layout."
- Keep the prompt short and direct when retrying — verbose prompts with many references increase bleed risk
- If bleed happens on first attempt, retry with a tighter prompt rather than adding more references

---

## Lessons Summary

1. **Adapt to the model, don't fight it** — redesign surrounding frames when the model consistently produces a gesture a certain way
2. **Keep all candidates** — artifact preservation enables reverting without re-generation
3. **Negative prompts are weak** — avoid describing what you don't want; omit it entirely
4. **Normalize dimensions before assembly** — mixed resolutions from different sources are inevitable
5. **Encode at native framerate** — don't resample hold-based keyframe animation
6. **Run continuity audit before assembly** — catch prop/hand/clothing errors systematically
7. **Camera-relative hand callouts are unreliable** at 3/4 angles — the model interprets "right/left" relative to character orientation which shifts with pose
8. **Use visual markers (red circle) for spatial placement** — text-based spatial instructions are ambiguous; a colored circle on the reference image removes all ambiguity
9. **Reference images can bleed into output** — multi-view sheets may be reproduced in the output; counter with explicit "ONE drawing" constraints
10. **Universal archetypes read better than specific characters at small sizes** — a generic RPG warrior reads as "game sprite" instantly; a specific character reference pushes toward miniature realism
11. **Build a character turnaround before using in scenes** — the turnaround sheet locks the design and provides angle references for consistent reproduction across frames
12. **Create standalone compositing backups** — generate key poses as standalone assets in case the baked-in approach fails in later pipeline stages (video models, interpolation)
