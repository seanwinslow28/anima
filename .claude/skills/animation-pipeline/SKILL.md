---
name: animation-pipeline
description: Manifest-driven 2D animation production pipeline for the Pencil Test project. Covers the 5-stage pipeline (Scaffold, Generate, Audit, Assemble, QA Review), keyframe generation with Gemini Nano Banana 2, in-between generation with ComfyUI OpenPose ControlNet, video model interpolation (Veo 3.1, Wan 2.2, Kling 3.0), QA gates (HF/SF/CC codes), frame chaining, and hold-frame assembly with FFmpeg. Use when asked about "animation pipeline", "production pipeline", "frame generation", "keyframe audit", "in-between generation", "frame chaining", "hold timing", "manifest config", or "pipeline QA".
---

# Pencil Test Animation Pipeline

## Purpose

Orchestrate the Pencil Test animation pipeline from manifest configuration through final export. Manage keyframe generation chains, enforce QA gates between stages, coordinate in-between generation (ComfyUI or video models), and assemble hold-frame sequences for GIF/WebM/MP4 export.

## When to Use

- Setting up a new generation run from manifest.yaml
- Running keyframe generation with frame chaining (generate.py)
- Running QA audits on generated frames (audit.py)
- Planning in-between generation strategy (ComfyUI OpenPose vs video models)
- Assembling approved keyframes with hold-frame timing (assemble.sh)
- Running continuity audits across approved frames (continuity_audit.py)
- Configuring manifest.yaml (keyframes, chains, QA codes, export formats)

## Examples

**Example 1: Starting a New Generation Run**
```
User: "Generate keyframes for Act 1 Chain 1"
Claude: [Uses animation-pipeline]
Running generation chain: F06 -> F10 -> F13 -> F18

python3 pipeline/generate.py --manifest manifest.yaml --chain 1

Each frame generates with references:
- F06: anchor (A-2)
- F10: anchor + approved F06
- F13: anchor + approved F10
- F18: anchor + approved F13

Output: runs/{run_id}/candidates/F{##}/attempt_01.png
After generation, run audit: python3 pipeline/audit.py --run-dir runs/{run_id} --frame F06 --attempt 1
```

**Example 2: Auditing a Generated Frame**
```
User: "Run QA on F06 attempt 1"
Claude: [Uses animation-pipeline]

python3 pipeline/audit.py --run-dir runs/{run_id} --frame F06 --attempt 1

Checks:
- HF01 (aspect ratio): PIL automated -- 16:9 within 2% tolerance
- HF02-HF05: Claude/Gemini vision review (paper texture, direction, pose, aesthetic)
- SF01-SF05: Style/identity/proportion/texture/expression checks

If PASS: python3 pipeline/audit.py --run-dir runs/{run_id} --frame F06 --attempt 1 --approve
If FAIL: python3 pipeline/audit.py --run-dir runs/{run_id} --frame F06 --attempt 1 --reject SF01
Retry ladder: attempt 2 re-anchors from A-2 with correction notes.
```

**Example 3: Planning In-Between Generation**
```
User: "Plan in-betweens for F06 to F10"
Claude: [Uses animation-pipeline]
Analyzing transition: F06 (idle pose) -> F10 (weight shift)

Motion type: Small motion (subtle weight shift, head tilt)
Recommended: Video model interpolation (Veo 3.1)
  - Start frame: approved/PT_A1_F06_key.png
  - End frame: approved/PT_A1_F10_key.png
  - Extract intermediate frames at 12fps
  - Audit each extracted frame against QA gates

Alternative: ComfyUI OpenPose ControlNet
  - Extract pose skeletons from F06 and F10
  - Interpolate 2 intermediate poses
  - Generate with ControlNet + IPAdapter identity lock
```

## Domain Content

### The 5-Stage Pipeline

```
A. SCAFFOLD --> B. GENERATE --> C. AUDIT --> D. ASSEMBLE --> E. QA REVIEW
manifest.yaml   generate.py    audit.py   assemble.sh   creative-director
```

| Stage | Tool | Input | Output | QA Gate |
|:------|:-----|:------|:-------|:--------|
| A. Scaffold | manifest.yaml | Project config | Directory structure, run_id | Schema validation |
| B. Generate | generate.py + Gemini API | Prompts, anchor, references | candidates/F{##}/attempt_*.png | Generation success, file integrity |
| C. Audit | audit.py + Claude/Gemini vision | Candidate frames | approved/ or rejected/ | HF01-HF05 (blockers), SF01-SF05 (retries) |
| D. Assemble | assemble.sh + FFmpeg | Approved keyframes + hold timing | GIF, WebM, MP4 | Frame count, file size, format spec |
| E. QA Review | creative-director skill | Assembled animation | Ship / revise decision | 5-dimension critique rubric |

### Manifest-Driven Generation Loop

**Generation Chains** -- dependencies between keyframes:
- **Chain 1:** F06 -> F10 -> F13 -> F18 (Beat 1-2: idle through mid-gesture)
- **Chain 2:** F31 -> F36 (Beat 3: sprite lands through nod)
- Chains 1 and 2 are independent and can run in parallel

**Frame Chaining** -- each frame receives:
1. A-2 anchor image (`images/2D-Character-Sketch-Sean-v1.png`) for identity lock
2. Previous approved frame in the chain for continuity

**Anchor Frames** -- F01 and F40 use A-2 directly (no generation needed)

**Dependency Resolution** -- generate.py walks the chain, blocking on unapproved predecessors. If F06 is not yet approved, F10 cannot generate.

### AI-Assisted Generation

#### A. Keyframe Generation (Gemini Nano Banana 2)

Primary generator for all keyframes. Uses the 7-Layer prompt framework from `image-generator-prompt-science` skill.

```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "[PROMPT]" \
  --output runs/{run_id}/candidates/F06/attempt_01.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env
```

With frame chaining (F10 references A-2 + approved F06):
```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "[PROMPT]" \
  --output runs/{run_id}/candidates/F10/attempt_01.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png runs/{run_id}/approved/PT_A1_F06_key.png \
  --env-file .env
```

Prompt files: `prompts/F{##}.txt` (auto-loaded by generate.py)

#### B. In-Between Generation (ComfyUI + OpenPose ControlNet)

Phase 2 workflow for generating in-between frames with precise pose control:

1. **Extract pose skeletons** from approved keyframes using OpenPose
2. **Interpolate poses** between consecutive keyframes (linear or eased)
3. **Generate frames** with ControlNet (pose guidance) + IPAdapter (identity lock from A-2)

See `comfyui-workflows` skill for workflow JSON structure and API queuing.

#### C. Video Model Interpolation (Veo 3.1 / Wan 2.2 / Kling 3.0)

Alternative to ComfyUI for generating in-betweens via start-frame/end-frame video generation:

1. Provide approved keyframe pair as start/end frames
2. Generate short video clip (0.5-1s)
3. Extract intermediate frames at 12fps
4. Audit each extracted frame through QA gates (HF/SF checks)

### Video Model Decision Matrix

| Transition Type | Recommended Tool | Reason |
|:----------------|:-----------------|:-------|
| Small motion (head tilt, blink) | Video model (Veo 3.1) | Faster, handles subtle motion well |
| Large motion (arm sweep, full gesture) | ComfyUI OpenPose | More precise pose control |
| Micro-smoothing (Twos to Ones) | RIFE / FILM | Best for frame doubling without new content |
| Complex acting (expression change) | ComfyUI + IPAdapter | Identity preservation during face changes |

### Frame Interpolation (RIFE / FILM)

For micro-smoothing -- doubling frame count without generating new content:

```bash
# RIFE: Real-Time Intermediate Flow Estimation
python -m rife.inference_video \
  --img anim/keys/ \
  --exp 1 \
  --output anim/inbetweens/
# exp=1: 1 in-between (doubles), exp=2: 3 in-betweens (4x)

# FILM: Better for large motion between keys
python -m film.interpolate \
  --input_frames anim/keys/ \
  --output_frames anim/inbetweens/ \
  --times_to_interpolate 1
```

### QA Gates

Three tiers of quality checks. For full definitions and test methods, see `shared/references/pencil-test-pipeline-context.md`.

#### Hard Fails (Blocking -- instant reject)

| Code | Name | Method |
|:-----|:-----|:-------|
| HF01 | Wrong aspect ratio | PIL automated -- 16:9 within 2% tolerance |
| HF02 | Missing paper texture | Vision review -- background must show cream paper grain |
| HF03 | Wrong direction | Vision review -- character orientation vs storyboard |
| HF04 | Wrong pose | Vision review -- pose vs storyboard description |
| HF05 | Wrong aesthetic | Vision review -- must read as pencil test, not digital/3D |

#### Soft Fails (Trigger retry with corrections)

| Code | Name | Retry Strategy |
|:-----|:-----|:---------------|
| SF01 | Style drift | Re-anchor with A-2 + style refinement prompt |
| SF02 | Identity drift | Re-anchor + explicit identity corrections (hair, jaw, eyes) |
| SF03 | Proportion drift | Add proportion constraints referencing A-2 |
| SF04 | Paper texture | Add paper texture refinement block |
| SF05 | Expression mismatch | Add explicit expression direction from storyboard |

#### Continuity Checks (CC01-CC08)

Run after a full generation pass via `python3 pipeline/continuity_audit.py --run-dir runs/{run_id}`.

| Code | Check | Severity |
|:-----|:------|:---------|
| CC01 | Stylus in RIGHT hand | Blocker |
| CC02 | Stylus visible every frame | Blocker |
| CC03 | Same clothing | Blocker |
| CC04 | Facing direction consistent | Warning |
| CC05 | Scale/position consistent | Warning |
| CC06 | Hair shape/volume/part | Warning |
| CC07 | Foot position/ground plane | Warning |
| CC08 | Expression arc follows storyboard | Warning |

#### Retry Ladder

1. **Attempt 1:** Original prompt from `prompts/F{##}.txt`
2. **Attempt 2:** Re-anchor from A-2 + specific correction notes from failure codes
3. **Attempt 3:** Tighten prompt with refinement tips from prompt science skill
4. **Attempt 4:** STOP -- flag for human review with diagnostic report

### Style Profile

```yaml
profile: pencil_test
framerate: 12
exposure: twos
paper_color: "#FAF5E8"
line_color: warm graphite gray (HB-2B)
resolution: 1920x1080
generator: gemini-3.1-flash-image-preview
anchor: images/2D-Character-Sketch-Sean-v1.png
```

### Asset Naming

Primary format for this project:

```
PT_{ActID}_{FrameNumber}_{AssetType}.{ext}
```

| Example | Meaning |
|:--------|:--------|
| `PT_A1_F06_key.png` | Pencil Test, Act 1, Frame 6, keyframe |
| `PT_A1_F18_key.png` | Pencil Test, Act 1, Frame 18, keyframe |
| `PT_A2_F97_key.png` | Pencil Test, Act 2, Frame 97, keyframe |

Candidates: `F{##}/attempt_{##}.png` (e.g., `F06/attempt_01.png`)
Rejected: `F{##}_attempt_{##}_{FAIL_CODE}.png` (e.g., `F06_attempt_01_SF01.png`)

**Reference: Traditional Naming** -- `{SequenceID}_{SceneID}_{ShotID}_{Layer}_{FrameNumber}.{ext}` (e.g., `SEQ02_SC05_SH01_L1Body_0024.png`)

### Reference: Full Production Pipeline (12-Stage)

The traditional animation production pipeline for reference. The Pencil Test project uses a condensed 5-stage version (above).

| # | Stage | Input | Output | QA Gate |
|:--|:------|:------|:-------|:--------|
| 1 | Script | Story concept | Formatted script | Visual density check |
| 2 | Design | Script | Model sheets, color palettes | Animatability/cost check |
| 3 | Storyboard | Script + designs | Boards, animatic | 180-degree rule, silhouette clarity |
| 4 | Audio | Script | Dialogue tracks, phoneme maps | Signal clarity, dead air check |
| 5 | Animatic | Boards + audio | Timed animatic | Pacing threshold (6 frames min, 10s max) |
| 6 | Timing/X-Sheet | Animatic | Exposure sheet, timing data | Sync offset (visual leads audio by 2 frames) |
| 7 | Layout | X-sheet + designs | BG lineart, camera field guides | Field guide validity, ground plane match |
| 8 | Animation | Layout + timing | Key frames, breakdowns | Twinning detector, hold duration |
| 9 | Cleanup | Rough animation | Clean lines | Volume conservation, line consistency |
| 10 | Ink & Paint | Clean lines | Colored frames | Palette lock, gap detection |
| 11 | Compositing | Colored layers + BG | Composited shots | Depth logic, lighting consistency |
| 12 | Final Render | Composited shots | Delivery files | Codec/bitrate spec, audio drift |

## Success Criteria

- [ ] Manifest.yaml defines all keyframes, chains, and QA codes
- [ ] Generation runs produce candidates in standardized directory structure
- [ ] Every frame passes HF01 (aspect ratio) before vision review
- [ ] QA gates run between generation and approval
- [ ] Continuity audit runs across all approved frames
- [ ] Assembly produces correct frame count with hold-frame duplication
- [ ] Exports meet format specs (GIF <5MB, WebM VP9, MP4 H.264)

## Related Skills (Stage Cross-Reference)

| Stage | Skill | What It Covers |
|:------|:------|:---------------|
| B. Generate (keyframes) | `gemini-pencil-animation-image-gen`, `image-generator-prompt-science` | Gemini API generation, 7-Layer prompt framework |
| B. Generate (in-betweens) | `comfyui-workflows` | ComfyUI OpenPose ControlNet, IPAdapter, workflow JSON |
| C. Audit / E. QA Review | `creative-director`, `2d-animation-principles` | Critique rubric, animation physics, acting gates |
| D. Assemble | `video-animation-production` | FFmpeg frame assembly, GIF/WebM/MP4 export |

## Copy/Paste Ready

```
"Start a new generation run for Act 1"
"Generate keyframes for Chain 1"
"Run QA audit on frame F06"
"Approve F06 attempt 1"
"Assemble approved keyframes into exports"
"Run continuity audit across all frames"
"Plan in-between generation for F06 to F10"
```
