## Phase 2: Act 1 In-Between Frame Generation

**Status:** First pass complete (2026-04-06). 9 of 9 in-betweens generated and assembled into test export. Review and refinement remaining.

---

### Workflow Discovered: OpenPose ControlNet → Gemini

The final pipeline uses **two stages** — ComfyUI for pose extraction/interpolation, Gemini for character generation:

```
Stage 1 (ComfyUI):  Approved Keyframe → DWPose Extraction → Skeleton Image
                     Skeleton A + Skeleton B → ImageBlend at easing ratio → Interpolated Skeleton

Stage 2 (Gemini):   A-2 Anchor + Previous Keyframe + Interpolated Skeleton
                     → Gemini Nano Banana Pro 2 → In-Between Frame
```

**Why this works:** The same engine (Gemini) that produced the keyframes produces the in-betweens, eliminating style mismatch. ComfyUI handles pose math; Gemini handles artistic rendering.

---

### What Was Tried First (and Failed)

**SD 1.5 end-to-end generation via ComfyUI** was the original plan:
- OpenPose ControlNet for pose guidance ✓ (pose was accurate)
- IPAdapter with A-2 anchor for identity lock ✗ (identity drifted heavily)
- Text prompt for pencil test style ✗ (produced completely different art style)
- Result: Wrong face, wrong clothing (teal instead of navy), vignette backgrounds, no resemblance to keyframes

**Key insight:** SD 1.5 and Gemini produce fundamentally different styles. ControlNet controls the pose but everything else (face, clothing, line quality, paper texture) comes from the base model's interpretation. The style gap was unbridgeable via prompting or IPAdapter weight tuning.

---

### What Was Completed

#### 1. ComfyUI Environment Setup
- **Models downloaded** (~8 GB total to `/Users/seanwinslow/Code-Brain/Comfy-UI/models/`):
  - `v1-5-pruned-emaonly.safetensors` (4.0 GB) — SD 1.5 checkpoint
  - `control_v11p_sd15_openpose.pth` (1.3 GB) — OpenPose ControlNet
  - `ip-adapter_sd15.safetensors` (43 MB) — IPAdapter
  - `sd1.5_model.safetensors` (2.4 GB) — CLIP Vision ViT-H
  - `vae-ft-mse-840000-ema-pruned.safetensors` (319 MB) — VAE
- **Custom nodes installed** (via `git clone` into `custom_nodes/`):
  - `comfyui_controlnet_aux` (Fannovel16) — DWPose skeleton extraction
  - `ComfyUI_IPAdapter_plus` (cubiq) — IPAdapter nodes
  - `onnxruntime` — faster DWPose inference
- **ComfyUI Desktop** runs on **port 8000** (not 8188)

#### 2. Workflow Design
Three ComfyUI workflow JSONs created in `workflows/`:
- `skeleton_extract.json` — LoadImage → DWPoseEstimation → SaveImage
- `skeleton_blend.json` — Load 2 skeletons → ImageBlend at ratio → SaveImage
- `openpose_inbetween.json` — Full SD 1.5 generation workflow (retained for reference, not used in final pipeline)

Batch orchestration script: `pipeline/generate_inbetweens.py` (ComfyUI API on port 8000)

#### 3. Skeleton Extraction & Interpolation
DWPose skeletons extracted from all 7 boundary keyframes (F01, F06, F10, F13, F31, F36, F40). Interpolated at Odd Rule easing ratios:

| Transition | In-Betweens | Blend Ratios | Easing | Motion |
|-----------|------------|-------------|--------|--------|
| F01→F06 | 3 | 0.14, 0.43, 0.71 | Ease-out | Slow head settle |
| F06→F10 | 1 | 0.50 | Linear | Head snap up |
| F10→F13 | 1 | 0.50 | Linear | To ready pose |
| F31→F36 | 2 | 0.33, 0.67 | Linear | Nod down |
| F36→F40 | 2 | 0.29, 0.71 | Ease-in | Settle to idle |

Total: **9 interpolated skeletons** stored in ComfyUI `input/` directory.

#### 4. Gemini In-Between Generation
Each in-between generated with 3 reference images:
1. **Image 1:** A-2 anchor (`images/2D-Character-Sketch-Sean-v1.png`) — identity lock
2. **Image 2:** Previous approved keyframe — style continuity
3. **Image 3:** Interpolated skeleton — pose reference

**First pass results:**
- 6 of 9 passed with correct identity, style, clothing, and pose
- 3 had clothing color drift (shirt went white/gray instead of navy)
- All 3 fixed with retry adding explicit "DARK NAVY BLUE t-shirt (not white, not gray)" to prompt

**Prompts saved:** `prompts/in-betweens/` (9 files with reference image notes)

#### 5. Test Assembly
- Test export: `export/pencil-test-act1-with-ibs.gif` (39 frames, 3.2s at 12fps, 1.7 MB)
- Also: `export/pencil-test-act1-with-ibs.mp4` (2.1 MB)
- Frame sequence includes keyframe holds + in-between frames using retry versions for the 3 fixed frames

#### 6. Documentation
- `docs/phase2-model-requirements.md` — model download manifest and generation settings
- `CHANGELOG.md` — full writeup of workflow discovery, what failed, lessons learned
- `docs/production-checklist.md` — updated with Phase 2 status

---

### What's Still Left for Phase 2

#### Immediate (review & approve) — COMPLETE
- [x] **Review test assembly at 12fps** — all 9 in-betweens passed visual QA
- [x] **Approve or reject individual in-betweens** — all 9 approved (3 using retry versions for clothing color fix)
- [x] **Copy approved in-betweens to `approved/`** with final naming

#### F13→F18 Transition (deferred)
- [ ] **Manual skeleton editing in Procreate** — this transition needs arc motion (arm sweep) that linear skeleton blending can't produce
- [ ] DWPose outputs are simple colored stick figures — easy to adjust joint positions in Procreate to follow an arc path
- [ ] Generate 2-3 in-betweens from manually edited skeletons via the same Gemini pipeline

#### Polish & Consistency
- [ ] **Clean up consistency breaks** — any frame-to-frame jumps in line weight, character scale, or ground plane
- [ ] **Procreate touch-up pass** — pencil texture consistency, construction line artifacts where missing
- [ ] **Continuity audit** — run `pipeline/continuity_audit.py` across the expanded frame set (CC01-CC08 checks)

#### Assembly — COMPLETE (except pencil trail)
- [x] **Update `assemble.sh`** with final in-between frame sequence and hold timing (42 frames, 3.5s at 12fps)
- [ ] **Pencil trail effect** (Beat 2, F18→F20) — separate layer or baked in
- [x] **Final export** — GIF (476KB) / WebM (320KB) / MP4 (2.0MB) with all in-betweens integrated

---

### Key Files Reference

| File | Purpose |
|------|---------|
| `workflows/skeleton_extract.json` | ComfyUI: DWPose skeleton extraction |
| `workflows/skeleton_blend.json` | ComfyUI: Skeleton interpolation at ratio |
| `workflows/openpose_inbetween.json` | ComfyUI: SD 1.5 generation (reference only) |
| `pipeline/generate_inbetweens.py` | Batch orchestration (ComfyUI API) |
| `prompts/in-betweens/*.txt` | Per-frame Gemini prompts with reference notes |
| `docs/phase2-model-requirements.md` | Model download manifest |
| `candidates/inbetweens/` | Generated in-between frames |
| `export/pencil-test-act1-with-ibs.gif` | Test assembly with in-betweens |
| ComfyUI data | `/Users/seanwinslow/Code-Brain/Comfy-UI` (port 8000) |

### Lessons Learned

1. **Use the same generation engine for keyframes and in-betweens** — mixing SD 1.5 and Gemini creates uncanny style mismatches
2. **Separate pose control from character generation** — ComfyUI for skeletons, Gemini for rendering
3. **OpenPose skeletons are readable by Gemini** — no mannequin intermediary needed
4. **Clothing color drift requires explicit prompt reinforcement** — "DARK NAVY BLUE t-shirt (not white, not gray)"
5. **Three reference images is the sweet spot** — identity anchor + previous keyframe + pose skeleton
6. **ComfyUI Desktop runs on port 8000**, not 8188
