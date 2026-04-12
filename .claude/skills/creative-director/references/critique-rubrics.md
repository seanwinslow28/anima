# Critique Rubrics & Critique-to-Action Map

Read this reference when reviewing or critiquing AI-generated animation frames. Use the scoring rubric to evaluate each dimension, then use the Critique-to-Action Map to translate observations into pipeline-specific fixes.

## Scoring Rubric (1-4 Scale)

### A. Keyframe Quality (Gemini Generation)

| Score | Identity | Style | Composition | Continuity | Technical |
|-------|----------|-------|-------------|------------|-----------|
| 4 | Unmistakably Sean — matches A-2 in all features | Full pencil test aesthetic: graphite lines, construction marks, cross-hatching, cream paper | Pose reads clearly, matches storyboard beat exactly | Props, clothing, direction all match previous frames | 16:9 aspect, correct paper texture, proper resolution |
| 3 | Recognizably Sean with minor feature variance | Mostly pencil test but missing 1-2 elements (e.g., no construction lines) | Pose is close but angle or intensity differs slightly | Minor prop inconsistency (e.g., stylus angle) | Aspect ratio correct, minor texture issues |
| 2 | Sean-like but notable drift in key features (jaw, hair) | Mixed aesthetic — some pencil test, some digital artifacts | Pose partially matches but key element wrong (arm position) | Direction or clothing change from previous frame | Aspect ratio slightly off, paper texture weak |
| 1 | Not recognizable as Sean | Wrong aesthetic entirely (anime, vector, 3D) | Pose doesn't match storyboard at all | Major continuity break (missing prop, wrong outfit) | Wrong aspect ratio, missing paper texture |

### B. In-Between Quality (ComfyUI / Video Model)

| Score | Identity Preservation | Motion Quality | Style Consistency | Artifact Check |
|-------|----------------------|----------------|-------------------|---------------|
| 4 | Character identical across all interpolated frames | Smooth arc, proper easing, follows physics | Line weight and texture match keyframes exactly | No ghosting, no double exposure, clean edges |
| 3 | Minor drift in 1-2 frames, still recognizable | Generally smooth with 1 minor spacing issue | Mostly consistent, slight line weight variance | Minor artifact in 1 frame, not distracting |
| 2 | Noticeable identity change mid-sequence | Linear spacing (floaty), or jerky transitions | Visible style difference from keyframes | Multiple artifacts, ghosting visible |
| 1 | Character unrecognizable in interpolated frames | Broken motion, limbs teleport or distort | Completely different aesthetic from keyframes | Severe artifacts throughout |

### C. Assembly Quality (FFmpeg Export)

| Score | Timing | Loop | Format | Playback |
|-------|--------|------|--------|----------|
| 4 | Hold durations feel natural, pacing matches storyboard | F40 to F01 seamless, no visible cut | All formats within spec (GIF <5MB, correct codecs) | Smooth at target fps, no dropped frames |
| 3 | Minor pacing issue in 1 transition | Slight visible seam at loop point | 1 format slightly off spec | Occasional stutter |
| 2 | Multiple transitions feel wrong (too fast or dragging) | Obvious loop cut | Missing format or wrong codec | Playback issues |
| 1 | Timing completely off, feels random | No loop continuity | Broken exports | Won't play |

## Critique-to-Action Map

### 1. Identity Drift
*"The character doesn't look like Sean." / "Face shape changed." / "Wrong hair."*

| Tool | Actions |
|------|---------|
| **Gemini (retry)** | Re-anchor from A-2 with explicit identity corrections. Add SF02-specific prompt block. Emphasize "same hair shape, same jaw angle, same eye spacing, same nose." |
| **ComfyUI** | Increase IPAdapter weight (0.7-0.8) with A-2 as identity reference. Verify ControlNet isn't overriding facial features. |
| **Video model** | Reject interpolation. Try different model or increase identity preservation weight. Consider shorter interpolation span. |

### 2. Style Drift
*"Lines are too clean." / "Looks digital." / "Missing construction lines." / "Too dark."*

| Tool | Actions |
|------|---------|
| **Gemini (retry)** | Add style refinement block from pencil-animation-prompt-templates.md. Emphasize "warm gray graphite, NOT black ink" and "visible construction line artifacts." |
| **ComfyUI** | Add pencil-texture style LoRA. Reduce CFG to avoid over-sharpening. Adjust negative prompt for digital artifacts. |
| **Post-process** | Apply paper texture overlay in compositing phase if generation can't achieve it. |

### 3. Composition and Pose
*"Pose doesn't match." / "Arms are wrong." / "Facing wrong direction."*

| Tool | Actions |
|------|---------|
| **Gemini (retry)** | Quantify pose: specify exact angles ("right arm extended 45 degrees forward"), add red circle marker technique for prop placement. |
| **ComfyUI** | Increase ControlNet strength (0.9+) for pose skeleton. Verify OpenPose skeleton matches intended pose. |
| **manifest.yaml** | If storyboard needs updating, revise the pose description in the keyframe entry. |

### 4. Timing and Pacing
*"The nod feels too fast." / "The hold drags." / "Motion is monotonous."*

| Tool | Actions |
|------|---------|
| **manifest.yaml** | Adjust `hold_frames` for the affected keyframe. |
| **assemble.sh** | Rebuild frame sequence with updated holds. Re-export all formats. |
| **2d-animation-principles** | Consult Duration Defaults table. Check if hold >12 frames needs moving hold treatment. |

### 5. Expression Mismatch
*"Expression doesn't match the beat." / "Face is blank." / "Wrong emotion."*

| Tool | Actions |
|------|---------|
| **Gemini (retry)** | Add explicit expression direction: "eyebrows lifted, mouth open to half-smile, eyes wide with recognition." Reference storyboard beat description. |
| **Continuity audit** | Check CC08 (expression arc) — does the emotion flow logically from the previous keyframe? |

### 6. Paper Texture Issues
*"Background is too white." / "Missing hole punches." / "Wrong grain."*

| Tool | Actions |
|------|---------|
| **Gemini (retry)** | Add paper texture refinement block. Specify "#FAF5E8 warm cream with visible grain texture, three hole-punch marks at bottom edge, hand-written production label." |
| **Post-process** | Overlay scanned paper texture if generation consistently fails this check (SF04). |

### 7. Continuity Breaks
*"Stylus switched hands." / "Outfit changed." / "Scale is off."*

| Tool | Actions |
|------|---------|
| **Gemini (retry)** | Add CRITICAL CONTINUITY note to prompt. Use red circle marker technique for prop hand placement. Reference the approved previous frame explicitly. |
| **continuity_audit.py** | Run full CC01-CC08 check. Log findings with frame number and description. |
| **Frame chaining** | Ensure the correct approved frame is being passed as reference in generate.py. |

### 8. AI Interpolation Artifacts
*"Ghosting between frames." / "Melted features." / "Double exposure."*

| Tool | Actions |
|------|---------|
| **Video model** | Reject and retry with different seed. Try a different model (Veo vs Wan vs Kling). Reduce interpolation span (fewer frames between keyframes). |
| **ComfyUI** | Reduce denoise strength. Increase ControlNet weight. Verify pose skeleton is clean. |
| **RIFE/FILM** | Lower exp value. Use FILM instead of RIFE for large motion gaps. |
