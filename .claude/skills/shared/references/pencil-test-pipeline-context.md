# Pencil Test Pipeline Context

Shared reference for all pipeline skills. Read this when you need project-specific context for the Pencil Test animation pipeline.

## Tool Stack

| Phase | Tool | Role |
|-------|------|------|
| B. Generate (keyframes) | Google Gemini Nano Banana 2 (`gemini-3.1-flash-image-preview`) | Primary keyframe generator via `generate_image.py` |
| B. Generate (in-betweens) | ComfyUI + OpenPose ControlNet | Pose-guided in-between frame generation |
| B. Generate (interpolation) | Veo 3.1 / Wan 2.2 / Kling 3.0 | Start-frame/end-frame video interpolation |
| C. Audit (automated) | Python PIL | HF01 aspect ratio check (16:9, 2% tolerance) |
| C. Audit (vision) | Claude vision + Gemini 2.5 Pro vision | HF02-HF05 hard fails, SF01-SF05 soft fails |
| C. Audit (continuity) | Claude vision | CC01-CC08 cross-frame consistency checks |
| D. Assemble | FFmpeg | Hold-frame duplication, GIF/WebM/MP4 export |
| E. QA Review | creative-director skill | Observation-Impact-Action critique rubric |

## Pipeline Stages

```
A. SCAFFOLD (manifest.yaml) → B. GENERATE (generate.py) → C. AUDIT (audit.py) → D. ASSEMBLE (assemble.sh) → E. QA REVIEW (creative-director)
```

## Generation Chains

Keyframes are generated in dependency chains. Each frame depends on the previous being approved.

- **Chain 1:** F06 → F10 → F13 → F18 (Beat 1-2: idle through mid-gesture)
- **Chain 2:** F31 → F36 (Beat 3: sprite lands through nod)
- **Anchors:** F01 and F40 use A-2 directly (no generation)

Chains 1 and 2 are independent and can run in parallel.

## Frame Chaining

Each generated frame receives these reference images:
1. **A-2 anchor** (always) — identity lock
2. **Previous approved frame** in the chain — pose continuity

Implemented in `generate.py:resolve_references()`.

## QA Code Tables

### Hard Fails (Blocking — instant reject)

| Code | Name | Method |
|------|------|--------|
| HF01 | Wrong aspect ratio (not 16:9) | PIL automated |
| HF02 | Missing paper texture | Vision model |
| HF03 | Character facing wrong direction | Vision model |
| HF04 | Wrong pose | Vision model vs storyboard |
| HF05 | Wrong aesthetic (digital/anime/3D) | Vision model |

### Soft Fails (Trigger retry with corrections)

| Code | Name | Retry Strategy |
|------|------|---------------|
| SF01 | Style drift from A-2 | Re-anchor + style refinement prompt |
| SF02 | Identity drift | Re-anchor + explicit identity corrections |
| SF03 | Proportion drift | Add proportion constraints from A-2 |
| SF04 | Paper texture issues | Paper texture refinement block |
| SF05 | Expression mismatch | Explicit expression direction |

### Continuity Checks (Cross-frame)

| Code | Name | Severity |
|------|------|----------|
| CC01 | Stylus hand (must be RIGHT) | Blocker |
| CC02 | Stylus presence | Blocker |
| CC03 | Clothing consistency | Blocker |
| CC04 | Facing direction | Warning |
| CC05 | Scale/position | Warning |
| CC06 | Hair consistency | Warning |
| CC07 | Foot position/ground plane | Warning |
| CC08 | Expression arc | Warning |

### Retry Ladder

1. Original prompt from `docs/act1-keyframe-prompts.md`
2. Re-anchor from A-2 + specific correction notes
3. Tighten with refinement tips from `pencil-animation-prompt-templates.md`
4. STOP — flag for human review

## Style Profile

```yaml
profile: pencil_test
framerate: 12
exposure: twos
aesthetic: traditional animation pencil test
paper_color: "#FAF5E8"  # warm cream
line_color: warm graphite gray (HB-2B range, NOT black ink)
line_weight: 1-3px (thick contour, thin interior)
color_palette: limited desaturated flat fills
resolution: 1920x1080
aspect_ratio: 16:9
generator: gemini-3.1-flash-image-preview
anchor: images/2D-Character-Sketch-Sean-v1.png
```

## Asset Naming

```
PT_{ActID}_{FrameNumber}_{AssetType}.{ext}
```

Examples: `PT_A1_F06_key.png`, `PT_A1_F06toF10_IB01.png` (in-between)

Candidates: `F{##}/attempt_{##}.png`
Rejected: `F{##}_attempt_{##}_{FAIL_CODE}.png`

## Video Model Decision Matrix

| Transition Type | Recommended Tool | Reason |
|----------------|-----------------|--------|
| Small motion (head tilt, blink) | Video model (Veo/Wan/Kling) | Faster, handles subtle motion well |
| Large motion (arm sweep, full body) | ComfyUI OpenPose ControlNet | More control over intermediate poses |
| Micro-smoothing (Twos → Ones) | RIFE/FILM frame interpolation | Best for doubling frame count |
| Post-assembly polish | Video model on final sequence | Only for specific deliverables (festival MP4) |

## Cross-Skill Routing

| If you need... | Invoke... |
|---------------|-----------|
| Animation timing, spacing, physics | `2d-animation-principles` |
| Pipeline orchestration, QA gates, generation chains | `animation-pipeline` |
| Creative critique, art direction, prompt refinement strategy | `creative-director` |
| ComfyUI workflow design, OpenPose in-betweens | `comfyui-workflows` |
| Keyframe generation prompts, Gemini API | `gemini-pencil-animation-image-gen` |
| 7-Layer prompt framework, prompt refinement | `image-generator-prompt-science` |
| FFmpeg assembly, format conversion | `video-animation-production` |

## Key File Paths

| File | Purpose |
|------|---------|
| `manifest.yaml` | Pipeline source of truth |
| `docs/production-checklist.md` | Current status (check first every session) |
| `docs/pencil-test-storyboard.md` | Creative direction blueprint |
| `docs/act1-keyframe-prompts.md` | 7-Layer formatted prompts for all keyframes |
| `images/2D-Character-Sketch-Sean-v1.png` | A-2 anchor character |
| `pipeline/generate.py` | Generation orchestrator |
| `pipeline/audit.py` | QA gate checker |
| `pipeline/assemble.sh` | FFmpeg assembly |
| `pipeline/continuity_audit.py` | Cross-frame continuity checks |
| `prompts/F{##}.txt` | Individual prompt files per frame |
