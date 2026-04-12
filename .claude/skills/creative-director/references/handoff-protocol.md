# Pipeline Handoff Protocol (PHP)

Read this reference when transitioning from the Creative Director's strategic planning to execution in a pipeline phase. Fill in the bracketed fields based on the interview and selected route.

## 1. Strategic Directive (The "North Star")

- **Single Objective:** [One sentence. e.g., "Generate a seamless 3.5-second pencil test loop showcasing Sean's character animation skill for the portfolio hero section."]
- **Creative Intent:** [Mood/tone. e.g., "Hand-drawn warmth, contemplative-to-energetic arc, subtle acting over broad gestures."]
- **Target Audience:** [e.g., "Animation studio recruiters and creative directors reviewing portfolio sites."]
- **Primary Platform:** [e.g., "Web hero section — GIF for preview, WebM for playback, MP4 for archival."]

## 2. Asset Audit

- **Existing Assets:**
  - [ ] A-2 anchor: `images/2D-Character-Sketch-Sean-v1.png`
  - [ ] Approved keyframes: `runs/{run_id}/approved/PT_A1_F*.png`
  - [ ] Prompt files: `prompts/F{##}.txt`
  - [ ] Style cluster: `.claude/skills/gemini-pencil-animation-image-gen/references/pencil-animation-prompt-templates.md`
- **Missing / To-Be-Created:**
  - [ ] [e.g., "In-between frames for F13 to F18 transition need ComfyUI generation"]
  - [ ] [e.g., "Sprite transformation sequence (F24-F28) needs design"]
- **File Structure:**
  - [ ] Run directory: `runs/{run_id}/`
  - [ ] Subfolders: `candidates/`, `approved/`, `rejected/`, `audit/`, `export/`

## 3. Technical Specifications

- **Resolution:** 1920x1080 (16:9)
- **Frame Rate:** 12fps on Twos
- **Total Frames:** 42 (Act 1 hero loop)
- **Style Profile:** Pencil test — cream paper (#FAF5E8), warm graphite gray lines, construction marks
- **Export Formats:**
  - GIF: 480px @ 15fps, <5MB, two-pass palette
  - WebM: 1920x1080, VP9, CRF 30
  - MP4: 1920x1080, H.264, CRF 18
- **Naming Convention:** `PT_{ActID}_{FrameNumber}_{AssetType}.{ext}`

## 4. Execution Roadmap

### Phase A: Scaffold
1. Verify `manifest.yaml` is current with all keyframes, chains, and QA codes
2. Initialize run directory: `python3 pipeline/generate.py --manifest manifest.yaml --dry-run`
3. Confirm prompt files exist in `prompts/F{##}.txt` for all generation targets

### Phase B: Generate
1. **[generate.py]** Run keyframe generation chains (Chain 1 and Chain 2 can run in parallel)
2. **[generate_image.py]** Each frame generated with A-2 anchor + previous approved frame as references
3. **[comfyui-workflows]** For in-betweens: extract OpenPose skeletons, generate with ControlNet
4. **[video models]** For subtle transitions: submit keyframe pairs to Veo/Wan/Kling

### Phase C: Audit
1. **[audit.py]** Run HF01 automated check (PIL aspect ratio) on all candidates
2. **[audit.py]** Run HF02-HF05 + SF01-SF05 vision review on each candidate
3. **[continuity_audit.py]** Run CC01-CC08 cross-frame checks on approved sequence
4. **[Retry]** Failed frames follow retry ladder (re-anchor, tighten, human review)

### Phase D: Assemble
1. **[assemble.sh]** Build hold-frame sequence (duplicate keyframes per manifest hold_frames)
2. **[assemble.sh]** Verify all 42 frames present in sequence
3. **[FFmpeg]** Render MP4, WebM, GIF per export specs
4. **[Verify]** GIF under 5MB, all formats play at correct fps

### Phase E: QA Review
1. **[creative-director]** Run critique rubric on final exports (Identity, Style, Composition, Continuity, Technical)
2. **[2d-animation-principles]** Validate timing, spacing, expression arc
3. **[Decision]** Ship if loop plays smoothly at 12fps and character is recognizably Sean in pencil test style on cream paper

## 5. Verification Checkpoints

- [ ] **30% (Rough):** First 2 keyframes generated and approved. Timing feels right in isolation.
- [ ] **60% (Structure):** All keyframes approved. Continuity audit passes. Frame sequence assembled.
- [ ] **90% (Polish):** Exports rendered. Loop is seamless. Style consistent across all frames.

## 6. Definition of Done

- [ ] **Engine Truth:** Loop plays smoothly at 12fps and character is recognizably Sean in pencil test style on cream animation paper.
- [ ] **Technical Integrity:** No flash frames, aspect ratio correct, all exports within spec.
- [ ] **Objective Met:** Animation clearly demonstrates character animation skill for portfolio.
- [ ] **File Hygiene:** Run directory organized, audit log complete, manifest.lock.yaml frozen.
