# Act 1 — Seedance v2 Integration Design (AI Companion Loop)

> **Spec deliverable.** Supersedes [docs/2026-05-02-act1-seedance-integration-plan.md](2026-05-02-act1-seedance-integration-plan.md). The original Act 1 (3.5s, 42-slot sprite-emergence loop) remains as a fallback/reference. This design defines a **new** Act 1 hero loop built from two Seedance 2.0 outputs cleaned through Nano Banana 2 and Procreate-polished to match the existing A-series pencil-test aesthetic.
>
> **Engine truth:** *"If the loop plays smoothly and the character is recognizably Sean in pencil test style on cream animation paper, it ships."*

---

## Summary

Build a new Act 1 hero loop that:
- Replaces the pixel-sprite metaphor with an **orange hand-drawn companion** emerging from pencil trails.
- Uses **two stitched Seedance 2.0 outputs** for the motion: `Act-1-Test-2-Seedance-2.0.mp4` (intro: idle → companion lands) + `Act-1-Test-3-Seedance-2.0.mp4` (loop-closer: companion releases → return to idle).
- Cleans every kept frame through Gemini Nano Banana 2 using the existing approved keyframes as **A-series style + identity anchors** (A-2 through A-8).
- Runs at **mixed cadence**: 12fps on idle/hold beats (traditional pencil-test breath), 24fps on hero motion beats (preserves Seedance smoothness). Assembly outputs a uniform 24fps video.
- Polished with Procreate passes on flagged frames before final encode.
- Ships as the new canonical Act 1 hero loop while **leaving the existing approved/ frames and original Act 1 export untouched** for fallback.

---

## Terms used in this spec

- **A-N anchor** — an existing approved keyframe with a baked-in production label (A-2, A-3, … A-8). Each represents the canonical pencil-test style + pose-class for one beat. Files: `runs/run_2026-04-04_174805/approved/PT_A1_*_key.png`.
- **KEEP / DROP / HOLD-COLLAPSE** (used in `selection.md`)
  - **KEEP** — frame goes to NB2 cleanup and occupies its own slot in the final assembly.
  - **DROP** — frame is discarded from the pipeline. Reason logged.
  - **HOLD-COLLAPSE** — frame is dropped from the pipeline, but the surrounding KEEP frame is held for an extra slot in assembly. Used to compress redundant idle/hold stretches without losing the beat.
- **Boil** — visible inter-frame inconsistency (line weight wobble, hair re-drawing, paper grain crawl, identity drift) between adjacent NB2-cleaned frames. Some boil is artistic ("boiling lines" is a traditional pencil-test signature); uncontrolled boil reads as messy AI noise. The chained-reference cleanup approach is the primary mitigation.
- **Chained-reference cleanup** — on 24fps stretches, every cleaned frame after the first uses the previous cleaned frame in this run as an additional reference. This anchors temporal style consistency across the stretch.
- **Mixed cadence** — different beats are cleaned at different fps (12 vs 24). The assembly output runs at a uniform 24fps; 12fps-cleaned frames are simply held for 2 sub-slots each.

---

## Source artifacts (locked at spec time)

**Active run directory:** `runs/run_2026-04-04_174805/` (no new run created).

**Seedance source videos:**
| Video | File | Duration | Frames @ 24fps | Beats covered |
|---|---|---|---|---|
| v2 (intro) | `export/seedance-2.0-output/Act-1-Test-2-Seedance-2.0.mp4` | 6.92s | 166 | idle → arm-up → draw circle → companion emerges → floats to shoulder → hold |
| v3 (loop-closer) | `export/seedance-2.0-output/Act-1-Test-3-Seedance-2.0.mp4` | 6.92s | 166 | companion-on-shoulder → detaches → floats away → return to idle |

**Seedance generation source frames** (already created, used to drive v2/v3):
- `runs/sw-portfolio-frame_0001.png` — A-7 idle (start of v2, end of v3)
- `runs/sw-portfolio-frame_0002.png` — A-7 companion-on-shoulder (end of v2, start of v3)

**Extracted frames** (24fps native, both videos):
- `seedance_frames/raw_24fps/frame_0001.png` … `frame_0166.png` (v2 intro)
- `seedance_frames_v3_loopclose/raw_24fps/frame_0001.png` … `frame_0166.png` (v3 loop-closer)

**A-series anchor map** (existing approved keyframes carry baked A-N labels):

| Anchor | File | Beat purpose | Style notes |
|---|---|---|---|
| **A-2** | `approved/PT_A1_F01_key.png`, `approved/PT_A1_F40_key.png` | Idle, return-to-idle | Neutral stance, stylus right hand, no companion. Canonical rough pencil-test target. |
| **A-3** | `approved/PT_A1_F06_key.png` | Glance-down | Looking at hands/stylus, slight forward lean. |
| **A-4** | `approved/PT_A1_F10_key.png` | Spark / idea moment | Head up, arm raised with stylus, expression alert. |
| **A-5** | `approved/PT_A1_F13_key.png` | Ready / confident | Thumbs-up pose. |
| **A-6** | `approved/PT_A1_F18/F20/F22/F24/F26/F28_key.png` | Arm-sweep → pencil trails → silhouette resolving | **Use F18/F20/F22 only as motion-line + paper-grain references** for the new arm-up + draw-circle beat — they carry the right trail/swirl aesthetic. Avoid F24/F26/F28 as references during companion-emergence cleanup (they embed the pixel-sprite metaphor; NB2 may try to merge the orange creature toward those silhouettes). |
| **A-7** | `approved/PT_A1_F31_key.png`, `runs/sw-portfolio-frame_0001/2.png` | Companion seated on shoulder | Source style of the new Seedance outputs. |
| **A-8** | `approved/PT_A1_F36_key.png` | The nod (companion on shoulder) | Slight head nod, companion seated. |

**Target aesthetic:** Match the line weight, paper grain, hole-punch marks, construction-mark style of **A-2** (`PT_A1_F01_key.png`). The Seedance outputs render in a cleaner, slightly more finished "A-7" style; NB2 cleanup pulls them back toward A-2's rough pencil-test fidelity.

---

## Engine-level decisions (locked)

1. **Loop or one-shot:** Loop. v2 + v3 stitched form a complete cycle (idle → companion-arrives → companion-departs → idle).
2. **Treat-as-canonical vs parallel:** **Parallel.** Existing `approved/` is untouched. New cleaned frames land in `runs/run_2026-04-04_174805/seedance_clean_v2/`. New exports use distinct filenames (`pencil-test-act1-v2.{mp4,webm,gif}`). Original Act 1 export stays at `pencil-test-act1.{mp4,webm,gif}` as fallback.
3. **A-7 vs A-2 anchor:** Both are canonical. A-2 is the **style target** for cleanup output. A-7 is the **source style** of the Seedance input + the established appearance of the companion-on-shoulder beat. They're not in conflict — A-2 dominates the cleanup output regardless of which A-N is used as a reference.
4. **Loop length:** No fixed target. Cull to natural cut points and accept whatever duration results (estimated 5–8s after culling).
5. **Cadence:** Mixed (Spider-Verse style). 12fps on idle/hold beats, 24fps on hero motion beats. Assembly outputs uniform 24fps.
6. **Cleanup cadence:** Cleanup happens at the per-beat target cadence. 12fps beats clean once per 12fps slot. 24fps beats clean once per 24fps slot.
7. **Drop strategy:** Reversible. Every extracted frame is logged in `selection.md` with KEEP / DROP / HOLD-COLLAPSE decisions and rationale. Only KEEP frames are sent to NB2.
8. **Implementation approach:** **Spike-first (Option A)** — validate NB2 24fps consistency on the riskiest beat before committing the full cleanup budget.

---

## Beat structure & cadence map (informs selection.md)

The combined v2 + v3 raw motion covers ~13.8s. The natural-cut-point cull collapses redundant idle/hold stretches and selects a roughly 5–8s loop.

| Beat | Source | Source frame range (24fps) | Cadence | Estimated keep count | A-N anchor references |
|---|---|---|---|---|---|
| **Idle (intro)** | v2 | 1–40 | 12fps | ~4 frames (collapse hold to ~0.3s) | A-2 (F01), A-2 (F40) |
| **Arm-up + draw circle** | v2 | 41–65 | 24fps | ~24 frames | A-4 (F10), A-5 (F13) — gesture energy; **A-6 (F18/F20)** — motion lines / paper grain only |
| **Companion emerges** ⭐ spike target | v2 | 66–105 | 24fps | ~40 frames | A-6 (F22) — swirl/trail aesthetic; A-7 (F31) — companion form |
| **Hold on shoulder** | v2 | 106–166 | 12fps | ~6 frames (collapse hold) | A-7 (F31), A-8 (F36) |
| **Companion detaches + floats away** | v3 | 1–55 | 24fps | ~28 frames | A-7 (F31), A-6 (F22), A-2 (F40) |
| **Return to idle** | v3 | 56–110 | 12fps | ~8 frames | A-2 (F40), A-2 (F01) |
| **Idle tail (loop point)** | v3 | 111–166 | 12fps | ~3 frames (collapse hold) | A-2 (F01) |
| **Total** | | | | **~113 keep frames** | |

Estimated NB2 cleanup volume: ~113 frames × ~1.3 average attempts (retry budget) = **~145 cleanup calls**.

Loop length estimate: 113 frames at the 24fps assembly cadence (12fps holds = each frame held 2 sub-slots; 24fps action = each frame fills 1 sub-slot). Roughly: 21 frames × 12fps (held to 42 sub-slots) + 92 frames × 24fps = 42 + 92 = **134 sub-slots at 24fps = ~5.6s loop**.

These numbers are estimates — actual values determined when `selection.md` is written.

---

## Components & data flow

```
Seedance v2 MP4 ──┐
                  ├──> ffmpeg extract @24fps ──> raw_24fps/*.png
Seedance v3 MP4 ──┘                                    │
                                                       ▼
                                              selection.md (KEEP/DROP/HOLD-COLLAPSE per frame,
                                              cadence per beat, A-N refs per frame)
                                                       │
                                                       ▼
                                    SPIKE: companion-emerges beat only
                                    NB2 cleanup w/ chained-reference approach
                                                       │
                                                       ▼
                                    Mini-assembly of spike beat (24fps clip)
                                                       │
                                              ┌────────┴─────────┐
                                              ▼ pass             ▼ fail
                                    Batch NB2 cleanup           STOP. Replan
                                    (remaining keep frames)     (12fps fallback,
                                              │                  smaller scope, etc.)
                                              ▼
                                    Procreate polish (flagged frames only)
                                              │
                                              ▼
                                    seedance_clean_v2/PT_A1_v2_{beat}_{idx}.png
                                              │
                                              ▼
                                    assemble.sh v2 mode
                                    (uniform 24fps output, 12fps frames held 2 sub-slots)
                                              │
                                              ▼
                                    export/pencil-test-act1-v2.{mp4,webm,gif}
                                              │
                                              ▼
                                    QA pass (CC01–CC08 + Engine Truth)
                                              │
                                              ▼
                                    Ship to portfolio
```

### Component responsibilities (boundaries)

- **Extraction** — pure ffmpeg, no creative judgment. Already done.
- **Selection** — human/Claude review against rubric. Produces a versioned, reviewable `selection.md`. **One artifact, one purpose: declarative source of truth for everything downstream.** No NB2 calls happen until selection.md is approved.
- **NB2 cleanup** — per-frame call to `generate_image.py` with the universal cleanup prompt + matched A-N anchors + previous-cleaned-frame as references on 24fps stretches. Outputs land under `seedance_clean_v2/`. Audited individually against HF01–HF05 + SF01–SF05 + stylus-right-hand check.
- **Spike validation** — assembles just the spike beat into a standalone clip. Has its own pass/fail rubric (see "Spike acceptance criteria" below).
- **Procreate polish** — manual, optional, only on frames flagged by audit or QA.
- **Assembly** — extended `assemble.sh` to support mixed cadence (12fps frames held 2 sub-slots at the 24fps output). New `--mode v2` flag. Existing 12fps mode untouched.
- **QA** — `continuity_audit.py` + creative-director Phase E rubric + Engine Truth verdict. Same gates as original Act 1.

---

## NB2 cleanup approach

### Universal cleanup prompt (used verbatim, every frame)

```
Restore this frame to traditional hand-drawn pencil animation on cream
paper #FAF5E8. Match the line weight, graphite shading, paper grain,
hole-punch marks, and construction-mark style of the A-2 reference.
Keep the character's pose, position, expression, and gesture EXACTLY as
shown in the input frame — only redraw it in pencil-test fidelity. The
stylus must remain in the character's RIGHT hand. The orange creature
companion, if present, stays in its exact position with its exact shape
and color — do not redraw it as a pixel sprite or armored figure.

NEGATIVES: no vector lines, no black outlines, no cel shading, no anime
style, no saturation other than the orange of the companion, no digital
painting, no gradients, no airbrush, no pure white background, no pure
black lines, no pixel art, no armored or spiky humanoid figures.
```

### Reference layering per beat

Every NB2 call uses 3 references in this order:

1. **A-2 anchor** (`approved/PT_A1_F01_key.png`) — always present as reference #1. Anchors the global style target.
2. **Beat-matched A-N anchor** — per the cadence map above. Provides beat-appropriate pose + style context.
3. **Pose reference** — the Seedance source frame (`raw_24fps/frame_NNNN.png` or `seedance_frames_v3_loopclose/raw_24fps/frame_NNNN.png`). Provides the exact pose to preserve.

**On 24fps stretches**, a 4th reference is added: **the previous cleaned frame** in this run (`seedance_clean_v2/...`). This chained-reference approach is the primary mitigation for boil/shimmer risk. The first cleaned frame in a 24fps stretch gets only the 3 references above; from frame 2 onward, the previous cleaned frame anchors the temporal consistency.

### Retry ladder (per frame)

1. **Attempt 1:** Universal prompt + 3 (or 4) references above.
2. **Attempt 2:** Re-anchor — add explicit identity correction notes ("face must match A-2 jaw shape / hair part / eye spacing exactly"). Same references.
3. **Attempt 3:** Tighten — append the paper-texture refinement block from `.claude/skills/gemini-pencil-animation-image-gen/references/pencil-animation-prompt-templates.md`.
4. **Attempt 4:** STOP. Mark frame for Procreate polish OR fall back to "skip — collapse hold over this slot" (handled at assembly time).

### Post-cleanup processing (every output)

1. Re-encode through PIL to fix the JPEG-as-PNG codec issue (per `pipeline/assemble.sh:159-164`).
2. Resize to 1376×768 (existing approved-frame dimensions) using Lanczos resampling. Source Seedance is 1280×720; final assembly upscales to 1920×1080.
3. Audit against HF01–HF05 + SF01–SF05 + stylus-right-hand + orange-companion-shape check.

---

## Spike acceptance criteria

The spike covers the "companion emerges from trails" stretch (v2 source frames 66–105, ~40 cleaned frames at 24fps). It assembles to a standalone ~1.7s mini-clip.

**PASS criteria (all required):**

1. **No visible boil** between adjacent cleaned frames. Lines, hair, paper grain stay coherent. Subjective — but if it reads as "wobbling pencil lines," that's a fail.
2. **Identity holds** — Sean stays on-model across all 40 frames. No SF02 drift.
3. **Stylus stays in right hand** in every frame. Any CC01 failure → instant fail.
4. **Companion stays orange + amorphous** — does not migrate toward the A-6 pixel-sprite / armored figure silhouette. The orange creature can change shape across frames (it's emerging) but it cannot become a different character.
5. **Pencil-test fidelity** — paper grain, construction lines, line weight match A-2 reference within a tolerance the user signs off on.

**FAIL response:** STOP. Replan options:
- Drop to pure 12fps for the whole loop (halves cleanup count, likely eliminates boil).
- Narrow the 24fps stretches to even fewer frames (e.g., only 8–12 frames at the absolute hero peak, rest at 12fps).
- Abandon the v2 integration and ship the existing original Act 1 loop.

---

## Out of scope

- **Generating new Seedance output.** Both source MP4s exist and are locked.
- **Modifying existing `approved/` frames.** They stay as fallback and as A-N reference sources.
- **Reshooting the original 3.5s Act 1 loop.** It remains shipped as `pencil-test-act1.{mp4,webm,gif}` until the v2 loop QA-passes.
- **Portfolio-site deployment.** New loop is delivered as `pencil-test-act1-v2.{mp4,webm,gif}`; portfolio integration is a separate Phase 8 task.
- **Act 2.** Unrelated; handled in the Act 2 plan.
- **Refactoring `pipeline/generate.py` or `pipeline/audit.py`.** Modifications limited to `assemble.sh` (mixed-cadence mode) and net-new scripts named with the `seedance_v2_` prefix.
- **Sound design / SFX / music.** Phase 7 backlog.
- **The original `Act-1-Test-Seedance-2.0.mp4`** (the very first pixel-sprite Seedance test). Stays in `seedance-2.0-output/` as historical reference; not used in the v2 pipeline.

---

## Ship criteria

Concrete, observable definition of "Act 1 v2 complete":

- `runs/run_2026-04-04_174805/seedance_frames/selection.md` exists with KEEP/DROP/HOLD-COLLAPSE per extracted frame, signed off by user.
- `runs/run_2026-04-04_174805/seedance_clean_v2/` contains exactly one cleaned PNG per KEEP frame, each passing HF01–HF05 + SF01–SF05 + stylus-right-hand + companion-shape audit.
- Spike validation log exists at `runs/run_2026-04-04_174805/audit/spike_validation.md` with PASS verdict and user sign-off.
- `runs/run_2026-04-04_174805/export/pencil-test-act1-v2.{mp4,webm,gif}` exist; MP4/WebM are 24fps 1920×1080; GIF is <5MB.
- Final QA at `runs/run_2026-04-04_174805/audit/v2_integration_qa.md` reports PASS against the Engine Truth and `continuity_audit.py` shows CC01–CC08 PASS.
- The loop plays seamlessly in Chrome and Safari for 5+ cycles — no visible seam at the v3→v2 wrap point.
- CHANGELOG entry dated 2026-05-12 documents the v2 integration, cull decisions, spike outcome.
- Existing `approved/`, `export/pencil-test-act1.*`, and the original Act 1 plan/storyboard remain untouched and intact as fallback.

---

## Open questions to resolve during implementation (not blocking spec approval)

These get answered while writing `selection.md` or during the spike — they don't change the architecture:

1. Exact cull thresholds per beat (how aggressive on the idle holds — 3 frames? 6 frames?).
2. Whether the companion-detach beat (v3 frames 1–55) wants 24fps the whole way or only on the moment of release (frames 1–25). Reviewable from the contact sheet.
3. Whether the spike beat should be assembled at 24fps standalone or interleaved with surrounding 12fps idles for context. (Probably standalone for a clean signal; surrounding context for the final review.)
4. Procreate polish budget — how many frames are flagged at QA? Determined empirically post-cleanup.
