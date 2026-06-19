# Act 1 — Seedance Integration & Ship Plan

> **Plan-mode deliverable.** Take Act 1 from "approved NB2 keyframes + ComfyUI in-betweens, Seedance test exists in isolation" to "Act 1 final hero loop, shipped, marked complete." Following the Phase B.5 philosophy: **Seedance finds the motion, NB2 protects the aesthetic.**
>
> Active run: [runs/run_2026-04-04_174805](../../../runs/run_2026-04-04_174805) — stays the active run; no new run.

<plan>

  <summary>
  Cherry-pick the strongest motion frames from the existing 24fps Seedance test pass (`runs/run_2026-04-04_174805/export/seedance-2.0-output/Act-1-Test-Seedance-2.0.mp4`) and run them through NB2 cleanup so they recover cream-paper pencil-test fidelity, then drop them into the existing 42-slot assembly as IB-slot replacements only — keyframe slots stay locked. End-state: a re-encoded `pencil-test-act1.mp4`/`.webm`/`.gif` in the same export dir, F38–F41 sprite-fade verified, Phase 4 marked complete, and a final QA pass against the Engine Truth before shipping the GIF/WebM to the portfolio site.
  </summary>

  <assumptions_and_open_questions>
  1. **What action span does the Seedance test cover?** The video is 6.04s @ 24fps (145 frames) vs. Act 1's 3.5s @ 12fps (42 frames). I'm assuming Seedance was run with anchor-chained interpolation across the **full** Act 1 keyframe set (F01→F06→F10→F13→F18→F31→F36→F40 = 7 segments), producing one continuous fluid pass that's slower than the final Act 1 because Seedance generated more in-between motion than the staccato 12fps target uses. **Task 1 of this plan resolves this — we watch the video end-to-end and log a beat-aligned timecode map before committing to selections.** If Seedance only covers a subset (e.g., F01→F18), then only those slots get candidate replacements; sprite-sequence and post-F18 slots stay as-is.
  2. **Resolution mismatch.** Seedance is 1280×720, current approved frames are ~1376×768 (per `assemble.sh` resolution-normalize comment). Both are 16:9. NB2 cleanup will be invoked at 16:9; we'll verify each cleaned PNG matches the existing approved-frame footprint before assembly. The final FFmpeg encode upscales to 1920×1080 with lanczos regardless.
  3. **Sprite-sequence slots are off-limits.** Slots 18–29 (frames F18 through F28 plus the sprite-flight composites at F28→F31) are full-frame creative-director art — pencil trails morphing into a pixel sprite. Seedance can't reproduce that metaphor. Plan assumes those 12 slots stay sourced from the existing `approved/` files.
  4. **Sprite-fade verification, not regeneration.** Phase 4c already shows F38 (66%) and F39 (33%) sprite-fade composites are done (`*_comp.png`). The "F38–F41 sprite fade" unchecked item in production-checklist.md is a **verification/QA gate** at this point, not new compositing. Confirming with the user.
  5. **Layered P-32A background is a deferred polish step.** Phase 4e's "Layer character animation over P-32A background" remains deferred unless QA reveals frame-to-frame paper-grain crawl. Each approved frame already has cream paper baked in; a shared underlay only matters if we see the grain shift between frames at 12fps playback.
  6. **Pencil trail effect (Beat 2)** — F18→F22 already shows pencil trails resolving into sprite (verified in approved/F18, F20, F22). Treating any further trail polish as deferred-Procreate work, not blocking ship.
  7. **Audit will use Claude vision (you, in execution session), not a separate vision API.** Per `pipeline/audit.py`'s pattern — generate the structured prompt, paste into the next session, get HF/SF verdict.
  8. **No new run created.** All new artifacts land in subdirs of the existing run: `runs/run_2026-04-04_174805/seedance_frames/` (extraction + analysis) and `runs/run_2026-04-04_174805/seedance_clean/` (NB2-restored frames).
  </assumptions_and_open_questions>

  <comparison_method>

  **Concrete artifact set produced before any frame is selected:**

  1. **Beat-aligned timecode map** at `runs/run_2026-04-04_174805/seedance_frames/timecode_map.md`. Two-column table: storyboard beat (idle / glance-down / spark / ready / mid-gesture / sprite-lands / nod / return-to-idle) → Seedance timestamp at which that pose is recognizable. Built by scrubbing the 6.04s video with QuickTime/VLC. This **answers Open Question #1** and tells us which Act 1 slots have Seedance coverage at all.

  2. **12fps frame extraction** of the Seedance MP4: `seedance_frames/raw_12fps/frame_%04d.png` (~72 PNGs). Decision rationale: extract at 12fps native, not 24fps + decimate. Assembly is 12fps; matching cadence at extraction keeps the analysis aligned with the slot grid we're selecting into. Cost of off-grid choice is low — we can always re-extract a single frame at 24fps if a particular sub-frame is visibly stronger.

  3. **Side-by-side comparison MP4** at `seedance_frames/compare.mp4` — `pencil-test-act1.mp4` (current ship candidate) on the left, Seedance MP4 resampled to 12fps and 1920×1080 on the right, hstacked. Watched at 0.5× and 1× to spot motion-quality wins.

  4. **Beat-aligned contact sheet** at `seedance_frames/contact_sheet.png` — 2-row grid showing, for every candidate IB slot, (current approved IB) vs. (proposed Seedance source frame) at the matched timecode. Lets the eye compare arcs at a single glance.

  **Scoring rubric, applied per candidate IB slot:**

  | Dimension | Seedance wins if… | Existing IB wins if… |
  |---|---|---|
  | **Arc quality** | Smoother weight shift, more breath, recognizable easing | IB is sharp/crisp where motion should be subtle |
  | **In-between physics** | Gravity / overlap / follow-through visible | IB freezes pose mid-motion |
  | **Identity (A-2 match)** | Face still on-model — jaw, hair, eye spacing | Seedance face has drifted (SF02) |
  | **Stylus hand** | Stylus visibly in **right** hand | Seedance dropped or mirrored stylus → instant reject |
  | **Aesthetic** | Pencil grain + cream paper + construction lines visible | Seedance went digital-clean / vector / anime → instant reject (HF02/HF05) |
  | **Paper grain** | Static, no texture crawl | Background grain shifts/crawls between frames |

  **Decision rule:** Seedance frame must win on at least **two** dimensions (one being Arc or Physics), AND must not have ANY instant-reject failures (stylus hand, aesthetic). Otherwise the existing IB stays. Tie goes to existing IB (the "first, do no harm" rule — current Act 1 already ships).

  **Selection log** at `seedance_frames/selection.md` — for every candidate IB slot, record: target slot index (1-42), current source filename, Seedance candidate timestamp, **decision** (KEEP existing / REPLACE with Seedance), rationale (1 sentence), reject codes if rejected.

  </comparison_method>

  <tasks>

  ### Task 1: Watch the Seedance test, build the beat-aligned timecode map

  - **Goal:** Resolve which Act 1 beats the Seedance video actually covers, before committing to any extraction or selection budget.
  - **Inputs:**
    - [runs/run_2026-04-04_174805/export/seedance-2.0-output/Act-1-Test-Seedance-2.0.mp4](../../../runs/run_2026-04-04_174805/export/seedance-2.0-output/Act-1-Test-Seedance-2.0.mp4)
    - [docs/pencil-test-storyboard.md](../../pencil-test/pencil-test-storyboard.md) (beat structure)
    - [runs/run_2026-04-04_174805/approved/](../../../runs/run_2026-04-04_174805/approved) (8 anchor poses to recognize)
  - **Steps:**
    1. Open the Seedance MP4 in QuickTime / VLC. Watch end-to-end at 1× then 0.5×.
    2. For each of the 8 storyboard anchor poses (F01 idle, F06 glance-down, F10 spark, F13 ready, F18 mid-gesture, F31 sprite-lands, F36 nod, F40 return), record the Seedance timestamp at which that pose is recognizable. Use 0.04s precision (1 frame at 24fps).
    3. Write `runs/run_2026-04-04_174805/seedance_frames/timecode_map.md` with a 3-column table: `Storyboard beat | Seedance timestamp | Seedance frame index (24fps)`.
    4. **HUMAN GATE.** If the map shows Seedance only covers F01→F18 (Beat 1+2 entry), reduce the candidate IB slot budget from 12 to ~6. If it covers the full loop, proceed with full budget.
  - **Outputs:** `seedance_frames/timecode_map.md`
  - **Acceptance:** Markdown file exists with at least 8 timestamp rows; ambiguous beats are explicitly flagged "not present in Seedance pass."
  - **Risks / fallbacks:** If Seedance covers a wildly different action (say, the order of beats is wrong), we abandon Seedance integration on Act 1 and re-run a fresh Seedance pass — but that decision and cost ($1.21–$1.52) needs the user's go-ahead before scope expands.

  ### Task 2: Extract Seedance frames at 12fps

  - **Goal:** Get a 12fps-aligned PNG sequence ready for visual comparison and selection.
  - **Inputs:** `Act-1-Test-Seedance-2.0.mp4`
  - **Steps:**
    1. `mkdir -p runs/run_2026-04-04_174805/seedance_frames/raw_12fps`
    2. `ffmpeg -i runs/run_2026-04-04_174805/export/seedance-2.0-output/Act-1-Test-Seedance-2.0.mp4 -vf fps=12 runs/run_2026-04-04_174805/seedance_frames/raw_12fps/frame_%04d.png`
  - **Outputs:** ~72 PNG frames at 1280×720, 16:9.
  - **Acceptance:** `ls runs/run_2026-04-04_174805/seedance_frames/raw_12fps/ | wc -l` returns 72 (±1, depending on ffmpeg fps rounding); each PNG opens cleanly; first frame visually matches the F01 idle pose.
  - **Risks / fallbacks:** If extraction count drops dramatically (e.g., <60), the source video duration doesn't match the 6.04s ffprobe report — re-probe and reconcile before proceeding. JPEG-as-PNG gotcha (per `assemble.sh:159-164`) doesn't apply here because Seedance MP4 → ffmpeg → PNG is a clean codec path; no Gemini in this step.

  ### Task 3: Build the comparison artifacts

  - **Goal:** Have a side-by-side video and a contact-sheet PNG so frame selection is observable, not a vibe call.
  - **Inputs:**
    - `runs/run_2026-04-04_174805/export/pencil-test-act1.mp4` (current Act 1)
    - `runs/run_2026-04-04_174805/export/seedance-2.0-output/Act-1-Test-Seedance-2.0.mp4`
    - `seedance_frames/timecode_map.md` (from Task 1)
    - `runs/run_2026-04-04_174805/approved/PT_A1_*_IB*.png` (current IBs to compare against)
  - **Steps:**
    1. Build the side-by-side compare MP4:
       ```bash
       ffmpeg -i runs/run_2026-04-04_174805/export/seedance-2.0-output/Act-1-Test-Seedance-2.0.mp4 \
              -vf "fps=12,scale=1920:1080:flags=lanczos" -c:v libx264 -crf 18 -pix_fmt yuv420p \
              runs/run_2026-04-04_174805/seedance_frames/seedance_12fps_1080p.mp4

       ffmpeg -i runs/run_2026-04-04_174805/export/pencil-test-act1.mp4 \
              -i runs/run_2026-04-04_174805/seedance_frames/seedance_12fps_1080p.mp4 \
              -filter_complex "[0:v]pad=iw*2:ih[bg];[bg][1:v]overlay=w" \
              -c:v libx264 -crf 18 \
              runs/run_2026-04-04_174805/seedance_frames/compare.mp4
       ```
    2. Build the contact-sheet PNG. For each IB slot in the candidate list (Slot 4-6, 9, 12, 15-17, 34-35, 38-39 — see `<frame_inventory>`), pair the existing approved IB with the Seedance frame at the matched timecode (from Task 1's map). Use ImageMagick:
       ```bash
       montage -tile 2x12 -geometry +4+4 \
         "approved/PT_A1_F01toF06_IB01.png" "seedance_frames/raw_12fps/frame_NNNN.png" \
         "approved/PT_A1_F01toF06_IB02.png" "seedance_frames/raw_12fps/frame_MMMM.png" \
         ...etc... \
         seedance_frames/contact_sheet.png
       ```
       (Real frame numbers come from the timecode map.)
  - **Outputs:** `seedance_frames/compare.mp4`, `seedance_frames/contact_sheet.png`, `seedance_frames/seedance_12fps_1080p.mp4`
  - **Acceptance:** Compare MP4 plays cleanly with both panes synced at 0:00; contact sheet PNG opens and shows ~12 paired thumbnails.
  - **Risks / fallbacks:** Hstack alignment is approximate because the two videos are different durations (3.5s vs 6.04s). If sync is too misleading at 1×, the contact sheet is the authoritative artifact; the compare video is just a vibe-check.

  ### Task 4: Score and select Seedance frames per the rubric

  - **Goal:** Produce a written, reviewable selection log committing to which IB slots will be replaced.
  - **Inputs:** Comparison artifacts from Task 3, scoring rubric in `<comparison_method>` above, all `approved/PT_A1_*_IB*.png` for context.
  - **Steps:**
    1. For each candidate IB slot (Slot 4, 5, 6, 9, 12, 15, 16, 17, 34, 35, 38, 39 — 12 slots), apply the scoring rubric.
    2. Write `seedance_frames/selection.md` with one row per candidate slot: `slot, current_source, seedance_ts, seedance_frame_idx, decision (KEEP|REPLACE), rationale, instant_reject_codes`.
    3. **HUMAN GATE.** User reviews `selection.md`. Approves, edits, or rejects. Plan does not advance until approved.
  - **Outputs:** `seedance_frames/selection.md` (approved by user).
  - **Acceptance:** Markdown file exists; every candidate slot has an explicit KEEP or REPLACE decision; user has signed off (date stamp at top of file).
  - **Risks / fallbacks:** If 0 slots score as REPLACE → abandon Seedance integration; ship Act 1 as-is and skip to Task 9 (sprite-fade verify) and Task 11 (final assembly + ship). If >12 slots score as REPLACE → reject; we said "12 slots max" because the keyframe slots are locked. (This shouldn't happen given keyframes are excluded by definition.)

  ### Task 5: NB2 cleanup of selected Seedance frames

  - **Goal:** For each REPLACE-decision frame from Task 4, produce an NB2-restored PNG that recovers cream-paper pencil-test fidelity while preserving Seedance's pose and gesture.
  - **Inputs:**
    - `seedance_frames/selection.md` (the REPLACE list)
    - `seedance_frames/raw_12fps/frame_NNNN.png` (each selected source frame)
    - [images/2D-Character-Sketch-Sean-v1.png](../../../images/2D-Character-Sketch-Sean-v1.png) (A-2 anchor — identity reference)
    - The flanking approved keyframes (e.g., for slot 4 = F01→F06 IB01, flank = F01_key + F06_key)
  - **Steps:**
    1. `mkdir -p runs/run_2026-04-04_174805/seedance_clean`
    2. **Universal cleanup prompt** (verbatim, every frame — adapted from Act 2 plan Task 8):
       ```
       Restore this frame to traditional hand-drawn pencil animation on cream paper #FAF5E8.
       Match the line weight, graphite shading, paper grain, hole-punch marks, and
       construction-mark style of the A-2 reference. Keep the character's pose, position,
       expression, and gesture EXACTLY as shown in the input frame — only redraw it in
       pencil-test fidelity. Stylus must remain in the character's RIGHT hand.

       NEGATIVES: no vector lines, no black outlines, no cel shading, no anime style,
       no saturation, no digital painting, no gradients, no airbrush, no pure white
       background, no pure black lines.
       ```
    3. For each REPLACE frame, invoke `generate_image.py` with **3 references**: A-2 + flanking start anchor + the Seedance source frame. Example for slot 4 (F01→F06 IB01):
       ```bash
       python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
         "[universal cleanup prompt above]" \
         --output runs/run_2026-04-04_174805/seedance_clean/PT_A1_F01toF06_IB01_seedance_attempt_01.png \
         --aspect-ratio 16:9 \
         --reference images/2D-Character-Sketch-Sean-v1.png \
                     runs/run_2026-04-04_174805/approved/PT_A1_F01_key.png \
                     runs/run_2026-04-04_174805/seedance_frames/raw_12fps/frame_0006.png \
         --env-file .env
       ```
    4. **Re-encode every cleanup output through PIL** to fix the JPEG-as-PNG gotcha (`assemble.sh:159-164`):
       ```python
       from PIL import Image
       Image.open(path).convert("RGB").save(path, "PNG")
       ```
    5. Audit each cleanup output against HF01-HF05 + SF02 (identity drift) + stylus-hand check. Use `pipeline/audit.py --run-dir runs/run_2026-04-04_174805 --frame F##_seedance --attempt 1` if the script accepts that frame name; otherwise paste each cleanup PNG into a Claude vision review with the structured prompt at `pipeline/audit.py:52-82`.
    6. **Retry ladder** (per CLAUDE.md):
       - Attempt 1: prompt above, 3 references.
       - Attempt 2: re-anchor — prompt + explicit identity correction notes ("face must match A-2 jaw shape / hair part / eye spacing exactly").
       - Attempt 3: tighten — add the paper-texture refinement block from `.claude/skills/gemini-pencil-animation-image-gen/references/pencil-animation-prompt-templates.md`.
       - Attempt 4: STOP. Flag for human review with diagnostic. **Fallback:** keep the existing approved IB for that slot; record in `selection.md`.
  - **Outputs:** `runs/run_2026-04-04_174805/seedance_clean/PT_A1_<slot_label>_seedance_attempt_NN.png` for each REPLACE slot.
  - **Acceptance:** Every REPLACE slot has at least one cleanup attempt that passes HF01-HF05 + SF02 + stylus-hand check. Slots that fail 3 attempts are documented in `selection.md` as "fallback to existing IB."
  - **Risks / fallbacks:**
    - **Stylus drift to left hand.** Listed in seedance-research-findings.md as identity-drift pattern #2. Mitigation: explicit "stylus in RIGHT hand" line in cleanup prompt; reject any output where stylus has moved.
    - **Identity drift in face.** SF02. Mitigation: A-2 is always reference #1. If still drifting on attempt 3, fallback to existing IB.
    - **Seedance source frame already has corrupted content** (e.g., morphing fingers). Cleanup can't restore what isn't there. If detected at audit, decision = "fallback to existing IB" without burning attempts 2/3.

  ### Task 6: Promote approved cleanup attempts to integration namespace

  - **Goal:** Lock in the chosen cleanup attempt per slot under a stable filename for assembly to consume.
  - **Inputs:** `seedance_clean/PT_A1_<slot_label>_seedance_attempt_NN.png` (audited PASS frames)
  - **Steps:**
    1. For each REPLACE slot with a passing attempt, copy the chosen attempt to a stable name:
       ```bash
       cp runs/run_2026-04-04_174805/seedance_clean/PT_A1_F01toF06_IB01_seedance_attempt_01.png \
          runs/run_2026-04-04_174805/seedance_clean/PT_A1_F01toF06_IB01_seedance.png
       ```
       (Drop the `_attempt_NN` suffix on the chosen one.)
    2. Verify dimensions match what `assemble.sh` expects (1376×768 or whatever the existing approved IB is). If Seedance-cleanup outputs at a different aspect/size, run a one-pass resize:
       ```bash
       python3 -c "from PIL import Image; im = Image.open('path'); im.resize((1376, 768), Image.LANCZOS).save('path')"
       ```
  - **Outputs:** Final cleanup PNGs at `seedance_clean/PT_A1_<slot_label>_seedance.png`.
  - **Acceptance:** For every REPLACE slot in `selection.md`, there's exactly one `_seedance.png` file in `seedance_clean/` with the right dimensions and PASSed audit.
  - **Risks / fallbacks:** Resolution mismatch with existing approved frames could cause a perceptible jump at IB slot boundaries. If detected, normalize all 42 source frames to 1376×768 before assembly (the assembly script already does scale-to-1080 at encode time, so source-side normalization is a precaution, not strictly required).

  ### Task 7: Update assembly script to consume Seedance-cleaned frames

  - **Goal:** Produce a deterministic 42-frame assembly that uses the Seedance-cleaned IB at every REPLACE slot and the existing approved IB at every KEEP slot.
  - **Inputs:** `selection.md`, `seedance_clean/`, `approved/`, [pipeline/assemble.sh](../../../pipeline/assemble.sh)
  - **Steps:**
    1. Edit `pipeline/assemble.sh` — extend the FRAME_SEQ definition (lines 76-104) to support a per-entry source-directory override. Two options, pick one:

       **Option A (preferred): inline the source path resolution.** Replace the unconditional `SRC="$APPROVED/PT_A1_${ASSET}.png"` (line 111) with a lookup that checks `seedance_clean/` first when the asset name ends in `_seedance`, else `approved/`:
       ```bash
       if [[ "$ASSET" == *_seedance ]]; then
           SRC="$RUN_DIR/seedance_clean/PT_A1_${ASSET}.png"
       else
           SRC="$APPROVED/PT_A1_${ASSET}.png"
       fi
       ```

       **Option B: keep `assemble.sh` untouched, fork a sibling `assemble_with_seedance.sh`.** Lower-risk, but creates duplication.

       Recommend Option A — single script, the suffix is a cleanly-typed signal.

    2. Update FRAME_SEQ entries for each REPLACE slot. Example: if Slot 4 (F01→F06 IB01) is REPLACE, change `F01toF06_IB01:1` to `F01toF06_IB01_seedance:1`.
    3. Run `bash pipeline/assemble.sh runs/run_2026-04-04_174805 --dry-run` if dry-run exists; else just inspect the FRAME_SEQ output before encoding.
  - **Outputs:** Modified `pipeline/assemble.sh`. New SEQ produces 42 frames in `runs/run_2026-04-04_174805/export/sequence/` on next full run.
  - **Acceptance:** Script logs every entry resolves to an existing file (no "Warning: Missing" lines). FRAME_COUNTER terminates at 42. Manifest hold durations unchanged from the locked manifest.
  - **Risks / fallbacks:** If Option A introduces shell-quoting edge cases on the `_seedance` suffix, fall back to Option B — fork the script.

  ### Task 8: Verify F38–F41 sprite fade reads cleanly at 12fps

  - **Goal:** Resolve the unchecked "Sprite fade effect (F38-F41 dissolve)" item from production-checklist.md line 70 — by either confirming the existing F38/F39 composites carry it, or compositing F40/F41 fades.
  - **Inputs:**
    - `runs/run_2026-04-04_174805/approved/PT_A1_F36toF40_IB01.png` (sprite at ~66% in current chain — check)
    - `runs/run_2026-04-04_174805/approved/PT_A1_F36toF40_IB02.png` (sprite at ~33% — check)
    - `runs/run_2026-04-04_174805/approved/PT_A1_F40_key.png` (A-2 anchor, no sprite)
    - [pipeline/composite_sprite.py](../../../pipeline/composite_sprite.py)
  - **Steps:**
    1. Open the four candidate frames in Preview / quicklook. Visually confirm sprite opacity progression: F36_key (full) → F36toF40_IB01 (~66%) → F36toF40_IB02 (~33%) → F40_key (gone).
    2. If the progression is correct → **DONE**, mark "Sprite fade effect (F38-F41 dissolve)" as complete in the production-checklist update (Task 12).
    3. If sprite is NOT fading correctly in the F36→F40 IBs, run `composite_sprite.py` to add the fade:
       ```bash
       python3 pipeline/composite_sprite.py --base approved/PT_A1_F36toF40_IB01.png --sprite candidates/sprite/sprite_seated_alpha.PNG --opacity 0.66 --output approved/PT_A1_F36toF40_IB01.png
       python3 pipeline/composite_sprite.py --base approved/PT_A1_F36toF40_IB02.png --sprite candidates/sprite/sprite_seated_alpha.PNG --opacity 0.33 --output approved/PT_A1_F36toF40_IB02.png
       ```
       (Adjust opacity / shoulder-anchor coords to match the F36 lands-on-shoulder position.)
  - **Outputs:** Either no change (current frames pass) or two updated approved IBs.
  - **Acceptance:** Quicklook scrub through F36 → F36toF40_IB01 → F36toF40_IB02 → F40 shows sprite fading naturally to gone before the loop restart, and storyboard line "starts F38, fully gone by F41" is satisfied.
  - **Risks / fallbacks:** Per CLAUDE.md no-destructive constraint, if compositing IS needed, **first** copy the existing approved F36toF40_IB01/IB02 to `runs/run_2026-04-04_174805/approved/_pre_fade_backup/` before overwriting. Or output to new `_fade.png` filenames and update `assemble.sh` SEQ accordingly.

  ### Task 9: Run the full assembly and produce new exports

  - **Goal:** Encode the integrated 42-frame sequence into MP4, WebM, and GIF.
  - **Inputs:** Modified `assemble.sh`, all 42 source frames available (mix of `approved/` and `seedance_clean/`).
  - **Steps:**
    1. Backup the existing exports for safe rollback:
       ```bash
       mkdir -p runs/run_2026-04-04_174805/export/_pre_seedance_backup
       cp runs/run_2026-04-04_174805/export/pencil-test-act1.{mp4,webm,gif} runs/run_2026-04-04_174805/export/_pre_seedance_backup/
       ```
    2. `bash pipeline/assemble.sh runs/run_2026-04-04_174805`
    3. Inspect output: `ffprobe runs/run_2026-04-04_174805/export/pencil-test-act1.mp4` → expect `nb_frames=42`, `r_frame_rate=12/1`, `duration=3.500`.
    4. Inspect GIF size — must be <5MB per manifest export config.
  - **Outputs:**
    - `runs/run_2026-04-04_174805/export/pencil-test-act1.mp4` (replaces existing; backup preserved)
    - `runs/run_2026-04-04_174805/export/pencil-test-act1.webm`
    - `runs/run_2026-04-04_174805/export/pencil-test-act1.gif`
  - **Acceptance:** `ffprobe` reports 42 frames at 12fps, 3.5s duration, 1920×1080. GIF under 5MB. All three files newer than the backup directory.
  - **Risks / fallbacks:** If assembly fails on a missing frame, the script's `Warning: Missing` line reveals which slot. If it's a `_seedance` slot, restore that slot's KEEP fallback in `assemble.sh` SEQ (use the existing approved IB) and re-run.

  ### Task 10: Final QA pass against the Engine Truth

  - **Goal:** Confirm the integrated loop ships — i.e., "plays smoothly at 12fps and the character is recognizably Sean in pencil test style on cream animation paper."
  - **Inputs:** New `pencil-test-act1.gif`, `.webm`, `.mp4`.
  - **Steps:**
    1. Open `pencil-test-act1.gif` in Chrome / Safari and watch the loop seamlessly cycle 5+ times. **Watch for:**
       - Loop seam at F40→F01 — must be invisible.
       - Sprite fade out before loop point — must complete by F41.
       - Stylus stays in right hand every frame (most importantly through Seedance-replaced slots).
       - Identity holds — no SF02 drift in any frame.
       - Paper grain stable — no texture crawl.
       - Hold timing reads as breath, not stutter.
    2. Run the continuity audit one more time:
       ```bash
       python3 pipeline/continuity_audit.py --run-dir runs/run_2026-04-04_174805
       ```
       (CLAUDE.md → "Continuity Audit" section.) Expect CC01-CC08 PASS.
    3. Apply `creative-director` skill's Phase E rubric (Identity / Style / Composition / Continuity / Technical). Document verdict in a short `runs/run_2026-04-04_174805/audit/seedance_integration_qa.md`.
    4. **HUMAN GATE.** User reviews QA doc. Sign-off → Task 11. Reject → loop back to Task 4 (re-score) or Task 5 (re-cleanup).
  - **Outputs:** `runs/run_2026-04-04_174805/audit/seedance_integration_qa.md` with explicit PASS / FAIL per Engine Truth criterion.
  - **Acceptance:** Markdown file shows PASS on every criterion, signed-off date, and a one-line Engine Truth verdict.
  - **Risks / fallbacks:** If QA fails on a specific slot — narrowest fix is to flip that slot back to KEEP (existing approved IB) in `assemble.sh` and re-run Task 9. Don't re-cleanup unless multiple slots fail.

  ### Task 11: Update production checklist + CHANGELOG, then ship

  - **Goal:** Mark Act 1 complete, document the integration decisions, and stage the GIF/WebM for portfolio embedding.
  - **Inputs:** Final exports, QA doc, this plan file.
  - **Steps:**
    1. Edit [docs/production-checklist.md](../../architecture/production-checklist.md):
       - Tick **Phase 4d** "Phase E QA re-review on transitions" (with date stamp).
       - Tick **Phase 4** keyframe assembly "Sprite fade effect (F38-F41 dissolve)" (line 70).
       - Tick **Phase 4e** "Layer character animation over P-32A background" — IF QA found no grain crawl, mark complete with note "verified P-32A baked into each frame is consistent; no separate underlay needed." If crawl found, tick "deferred — see polish backlog."
       - Tick **Phase 4e** "Add pencil trail effect (Beat 2)" — mark complete with note "F18→F22 sequence carries the trail moment; no additional Procreate pass needed for ship." If user disagrees in QA, tick "deferred — Procreate polish post-ship."
       - Tick **Phase 4e** "Export final hero loop" — point to `runs/run_2026-04-04_174805/export/pencil-test-act1.{gif,webm,mp4}`.
       - Leave **Phase 4e** "Ship to portfolio" UNCHECKED — that requires the portfolio site update (out of scope for this plan).
       - Update top of file: "Last updated: 2026-05-02".
    2. Append to [CHANGELOG.md](../../../CHANGELOG.md) under a new dated heading (`## 2026-05-02 — Act 1 Seedance Integration`):
       - One-line summary.
       - List of REPLACE slots + rationale (one-line each).
       - Note that the existing Seedance test was incorporated; no new Seedance generation was run.
       - Link to this plan file and to `selection.md` for decision history.
       - Note JPEG-as-PNG re-encode applied to all cleanup outputs.
    3. Stage the portfolio-ready artifact:
       ```bash
       cp runs/run_2026-04-04_174805/export/pencil-test-act1.{gif,webm} <portfolio-deploy-dir>
       ```
       (Only if the user has a deploy dir defined; otherwise note "ready to ship — awaiting portfolio site update".)
  - **Outputs:** Updated `docs/production-checklist.md`, new `CHANGELOG.md` entry, portfolio assets staged or path documented.
  - **Acceptance:** `git diff docs/production-checklist.md CHANGELOG.md` shows the expected updates; the unchecked items remaining are exactly Phase 4e "Ship to portfolio" + Phase 7 + Phase 8 (Act 2 / sound / portfolio site).
  - **Risks / fallbacks:** If user wants the layered P-32A composite or a Procreate trail polish before ship, both move into a separate post-ship task list in the checklist; this plan deliberately doesn't block ship on them.

  </tasks>

  <frame_inventory>

  All 42 final assembly slots, with proposed source. **REPLACE candidates are flagged "candidate"** — final REPLACE/KEEP decision is made in Task 4 selection.md. KEEP-LOCKED slots are non-negotiable per the constraints.

  | Slot | Beat | Storyboard frame | Source filename | Status |
  |------|------|------------------|-----------------|--------|
  | 1 | Idle hold | F01 | `approved/PT_A1_F01_key.png` | KEEP-LOCKED (keyframe) |
  | 2 | Idle hold | F01 | `approved/PT_A1_F01_key.png` | KEEP-LOCKED (hold) |
  | 3 | Idle hold | F01 | `approved/PT_A1_F01_key.png` | KEEP-LOCKED (hold) |
  | 4 | Glance-down anticipation | F01→F06 IB01 | `approved/PT_A1_F01toF06_IB01.png` OR `seedance_clean/PT_A1_F01toF06_IB01_seedance.png` | **CANDIDATE** |
  | 5 | Glance-down deeper tilt | F01→F06 IB02 | `approved/PT_A1_F01toF06_IB02.png` OR Seedance cleanup | **CANDIDATE** |
  | 6 | Near full glance-down | F01→F06 IB03 | `approved/PT_A1_F01toF06_IB03.png` OR Seedance cleanup | **CANDIDATE** |
  | 7 | Glance-down hold | F06 | `approved/PT_A1_F06_key.png` | KEEP-LOCKED (keyframe) |
  | 8 | Glance-down hold | F06 | `approved/PT_A1_F06_key.png` | KEEP-LOCKED (hold) |
  | 9 | Head lifting (spark anticipation) | F06→F10 IB01 | `approved/PT_A1_F06toF10_IB01.png` OR Seedance cleanup | **CANDIDATE** |
  | 10 | Spark | F10 | `approved/PT_A1_F10_key.png` | KEEP-LOCKED (keyframe) |
  | 11 | Spark hold | F10 | `approved/PT_A1_F10_key.png` | KEEP-LOCKED (hold) |
  | 12 | Transitioning to ready | F10→F13 IB01 | `approved/PT_A1_F10toF13_IB01.png` OR Seedance cleanup | **CANDIDATE** |
  | 13 | Ready pose | F13 | `approved/PT_A1_F13_key.png` | KEEP-LOCKED (keyframe) |
  | 14 | Ready hold | F13 | `approved/PT_A1_F13_key.png` | KEEP-LOCKED (hold) |
  | 15 | Arm begins to lift | F13→F18 IB01 | `approved/PT_A1_F13toF18_IB01.png` OR Seedance cleanup | **CANDIDATE** |
  | 16 | Arm at arc apex | F13→F18 IB02 | `approved/PT_A1_F13toF18_IB02.png` OR Seedance cleanup | **CANDIDATE** |
  | 17 | Arm sweeping forward | F13→F18 IB03 | `approved/PT_A1_F13toF18_IB03.png` OR Seedance cleanup | **CANDIDATE** |
  | 18 | Mid-gesture | F18 | `approved/PT_A1_F18_key.png` | KEEP-LOCKED (keyframe) |
  | 19 | Mid-gesture hold | F18 | `approved/PT_A1_F18_key.png` | KEEP-LOCKED (sprite-sequence start) |
  | 20 | Trails intensify | F20 | `approved/PT_A1_F20_key.png` | KEEP-LOCKED (sprite sequence) |
  | 21 | Trails intensify hold | F20 | `approved/PT_A1_F20_key.png` | KEEP-LOCKED (sprite sequence) |
  | 22 | Abstract swirl | F22 | `approved/PT_A1_F22_key.png` | KEEP-LOCKED (sprite sequence) |
  | 23 | Abstract swirl hold | F22 | `approved/PT_A1_F22_key.png` | KEEP-LOCKED (sprite sequence) |
  | 24 | Silhouette emerges | F24 | `approved/PT_A1_F24_key.png` | KEEP-LOCKED (sprite sequence) |
  | 25 | Silhouette hold | F24 | `approved/PT_A1_F24_key.png` | KEEP-LOCKED (sprite sequence) |
  | 26 | Clear form | F26 | `approved/PT_A1_F26_key.png` | KEEP-LOCKED (sprite sequence) |
  | 27 | Clear form hold | F26 | `approved/PT_A1_F26_key.png` | KEEP-LOCKED (sprite sequence) |
  | 28 | Sprite bounces | F28 | `approved/PT_A1_F28_key.png` | KEEP-LOCKED (sprite sequence) |
  | 29 | Sprite bounces hold | F28 | `approved/PT_A1_F28_key.png` | KEEP-LOCKED (sprite sequence) |
  | 30 | Sprite mid-flight | F28→F31 IB01 (composited) | `approved/PT_A1_F28toF31_IB01_comp.png` | KEEP-LOCKED (sprite-comp) |
  | 31 | Sprite approaching shoulder | F28→F31 IB02 (composited) | `approved/PT_A1_F28toF31_IB02_comp.png` | KEEP-LOCKED (sprite-comp) |
  | 32 | Sprite lands | F31 | `approved/PT_A1_F31_key.png` | KEEP-LOCKED (keyframe, sprite-baked) |
  | 33 | Sprite lands hold | F31 | `approved/PT_A1_F31_key.png` | KEEP-LOCKED (hold) |
  | 34 | Nod begins | F31→F36 IB01 | `approved/PT_A1_F31toF36_IB01.png` OR Seedance cleanup | **CANDIDATE** |
  | 35 | Deeper nod | F31→F36 IB02 | `approved/PT_A1_F31toF36_IB02.png` OR Seedance cleanup | **CANDIDATE** |
  | 36 | The nod | F36 | `approved/PT_A1_F36_key.png` | KEEP-LOCKED (keyframe, sprite-baked) |
  | 37 | The nod hold | F36 | `approved/PT_A1_F36_key.png` | KEEP-LOCKED (hold) |
  | 38 | Returning to idle (sprite fade ~66%) | F36→F40 IB01 | `approved/PT_A1_F36toF40_IB01.png` OR Seedance cleanup | **CANDIDATE** (Task 8 verifies fade) |
  | 39 | Near idle (sprite fade ~33%) | F36→F40 IB02 | `approved/PT_A1_F36toF40_IB02.png` OR Seedance cleanup | **CANDIDATE** (Task 8 verifies fade) |
  | 40 | Return to idle | F40 | `approved/PT_A1_F40_key.png` | KEEP-LOCKED (keyframe = A-2) |
  | 41 | Return hold | F40 | `approved/PT_A1_F40_key.png` | KEEP-LOCKED (hold) |
  | 42 | Loop tail | F40 | `approved/PT_A1_F40_key.png` | KEEP-LOCKED (loop point) |

  **Tally:** 30 KEEP-LOCKED slots, 12 CANDIDATE slots. Maximum Seedance integration footprint = 12 slots (~29% of the loop). Realistic expectation per the rubric in `<comparison_method>`: 4-8 actual REPLACE decisions.

  </frame_inventory>

  <ship_criteria>

  Concrete, observable definition of "Act 1 complete":

  - **`runs/run_2026-04-04_174805/export/pencil-test-act1.gif`** exists, plays seamlessly in Chrome and Safari, is < 5MB, and is the version produced by Task 9 (newer than the `_pre_seedance_backup/` copy).
  - **`runs/run_2026-04-04_174805/export/pencil-test-act1.webm`** exists with `nb_frames=42`, `r_frame_rate=12/1`, `duration=3.500`, 1920×1080.
  - **`runs/run_2026-04-04_174805/export/pencil-test-act1.mp4`** same metadata as WebM.
  - **`runs/run_2026-04-04_174805/audit/seedance_integration_qa.md`** exists with PASS verdict on the Engine Truth: "plays smoothly at 12fps and the character is recognizably Sean in pencil test style on cream animation paper."
  - **`pipeline/continuity_audit.py`** run reports CC01-CC08 PASS across the new 42-frame sequence.
  - **Stylus is verifiably in the right hand in every frame** — including all REPLACE-decision Seedance-cleaned frames (per scoring rubric instant-reject rule).
  - **F38-F41 sprite fade reads correctly** (Task 8 verified) — sprite fully invisible by Slot 41 so the F40→F01 loop restart looks like a clean "page turn."
  - **`docs/production-checklist.md` shows Phase 4 fully ticked** with the exception of Phase 4e "Ship to portfolio" (which requires portfolio-site work outside this run).
  - **CHANGELOG.md has a 2026-05-02 entry** documenting the Seedance integration decisions, REPLACE slots, and rationale, with links to this plan and to `selection.md`.
  - **Pencil trail effect (Beat 2)** — either confirmed as carried by the F18-F22 sprite-emergence sequence, or explicitly deferred-with-note in the checklist. Not a ship blocker per assumption #6.
  - **Layered P-32A background** — either confirmed as not-needed (paper baked into each frame is stable), or explicitly deferred-with-note. Not a ship blocker per assumption #5.

  </ship_criteria>

  <out_of_scope>

  - **Generating any new Seedance video.** This plan integrates the *existing* test pass at `Act-1-Test-Seedance-2.0.mp4`. A fresh Seedance run on the full Act 1 anchor chain (or on specific narrow transitions) is a separate plan, gated by Open Question #1 in Task 1.
  - **Act 2.** Active in `docs/2026-04-27-act2-seedance-execution-plan.md`. Untouched here.
  - **Sound design / pencil-scratch SFX / music.** Phase 7 backlog.
  - **Title card "Sean Winslow / Creative Technologist" draw-on effect.** Phase 7 / Act 2 transition work.
  - **Page-lift / portfolio-page-turn transition into the portfolio site.** Phase 8 (Beat 7 of Act 2 storyboard).
  - **Shipping to the portfolio site itself** (DNS, deploy, hero-section embed). Phase 8.
  - **Portfolio-site Lighthouse audit, image-format fallbacks, lazy loading.** Out-of-pipeline.
  - **Procreate-pass polish** beyond what Task 8 verifies — any line-quality cleanup, paper-grain unification across frames, pencil-trail enhancement on Beat 2 — captured as deferred items in the checklist if QA flags them, but not blocking ship.
  - **Refactoring `pipeline/generate.py`, `pipeline/audit.py`, or the existing approved-frames namespace.** Per the constraint, no destructive moves on `approved/`.
  - **Re-running F13→F18 in-betweens or any other ComfyUI-sourced existing IB.** Those passed continuity audit and ship as-is unless the Seedance integration explicitly REPLACES them at the SEQ level.

  </out_of_scope>

</plan>

---

## Self-check (per `<validation>`)

1. ✅ All six must-read files were read; one decision quoted from each at the top of the response.
2. ✅ Frame inventory enumerates all 42 slots.
3. Seedance source timestamps + target slots: pending Task 1 (timecode_map.md). Plan flags this as Open Question #1 and gates downstream tasks on its resolution. The candidate slot list (12 CANDIDATEs) is explicit; the source timestamps for each become concrete only after Task 1 fills the map.
4. ✅ Phase 4 unchecked items addressed: F38-F41 sprite fade → Task 8; pencil trail (Beat 2) → assumption #6 (defer); P-32A layer → assumption #5 (verify, defer if not needed); ship to portfolio → out_of_scope (acknowledged Phase 8); Phase E QA re-review → Task 10.
5. ✅ Acceptance criteria are observable (file exists, ffprobe metadata, < 5MB, audit PASS verdict, checkbox ticked).
6. ✅ NB2 cleanup retry-3-fails fallback explicit in Task 5 step 6: "keep the existing approved IB for that slot; record in selection.md."
