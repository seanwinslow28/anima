# Changelog

## 2026-04-27 — Task 2: Build `pipeline/seedance_lib.py` shared helper library

**What changed:** Created `pipeline/seedance_lib.py` — the shared helper module imported by all four upcoming Seedance pipeline scripts (`seedance_generate.py`, `seedance_extract.py`, `seedance_cleanup.py`, `seedance_audit.py`). Implements 7 helpers:

- `load_shotlist(path)` — YAML loader with explicit FileNotFoundError.
- `load_env(env_file)` — `.env` parser that mirrors `generate_image.py`'s behavior: skips blanks/comments, strips whitespace and quotes, never overwrites existing env vars.
- `make_run_dir(prefix, base)` — creates `runs/{prefix}-{YYYY-MM-DD}/` with 6 standard subdirs (`seedance/`, `extracted/`, `cleanup/`, `shots/`, `audit/`, `export/`); idempotent.
- `upload_anchor(path, cache_path)` — uploads a local anchor to fal.ai, caches the resulting URL in a JSON file, returns cached URL on repeat calls without re-uploading.
- `log_event(run_dir, event)` — appends a JSON line to `{run_dir}/audit/seedance_log.jsonl`; auto-injects `timestamp` and 8-char `event_id`; never mutates the caller's dict.
- `frame_count_at_12fps(duration_s)` — returns `int(duration_s * 12)`.
- `reencode_to_png(path)` — re-encodes a file in place to true PNG format, fixing the JPEG-as-PNG gotcha (same fix as `assemble.sh:153-169` but as a reusable Python helper).

`fal_client` and `PIL` imports are deferred to their respective functions so importing the module never fails when those dependencies are absent or keys are unset.

Both smoke tests passed: `make_run_dir` + `log_event` (2.2) and `upload_anchor` cache round-trip against `zone1/film.png` (2.3 — first call uploaded to fal.ai, second returned same URL instantly from JSON cache).

**Why:** Centralizing these helpers prevents the same logic from being copy-pasted across four scripts. `load_env` and `upload_anchor` in particular have subtle correctness requirements (don't overwrite os.environ, deferred fal_client import, atomic-ish cache writes); doing them once and testing them here means the downstream scripts are mechanical. The JPEG-as-PNG issue has already burned Act 1 assembly; encoding the fix as a named helper makes it impossible to forget in Act 2.

---

## 2026-04-27 — Task 1: Freeze shot list as machine-readable YAML

**What changed:** Created `pipeline/seedance_shotlist.yaml` — a machine-readable translation of `docs/act2-seedance-shot-list.md`. Encodes all 10 Seedance shots (W1, W2, W3, S0, T0, T2, TR, REV, PM, PB) with id, type, duration, risk level, start/end anchor paths, verbatim prompts, and fallback strategies. Encodes all 4 holds (S1 static, T1 cursor_blink, T3 static, FIN ken_burns with requires_manual_cleanup) and the 3 hard cuts. Assembly order (14 entries) matches the shot list spec. All 14 unique anchor paths validated as present on disk.

**Why:** The orchestrator (`seedance_generate.py`), extractor (`seedance_extract.py`), cleanup loop (`seedance_cleanup.py`), auditor (`seedance_audit.py`), and assembler (`seedance_assemble.sh`) — all to be built in Tasks 2–11 — need a single machine-readable source of truth to drive generation, hold construction, hard-cut placement, and assembly order. Freezing this as YAML before writing any scripts ensures the spec is authoritative and version-controlled, not embedded in script logic.

---

## Seedance Execution Kickoff Prompt

**Date:** 2026-04-27

### What changed

Wrote `prompts/2026-04-27-seedance-execution-kickoff.md` — a fresh-session kickoff prompt for executing the locked 12-task plan in `docs/2026-04-27-act2-seedance-execution-plan.md`. Constructed via the `prompt-engineering` skill checklist: clarity (mode declaration up front, "do NOT enter plan mode"), XML structure (`<execution_mode>`, `<your_first_task>`, `<key_file_paths>`, `<project_rules>`, `<known_persistent_issues>`, `<budget_expectations>`, `<reasoning>`), validation (explicit human-gate enumeration with Task IDs), long-context-at-top with first-task-at-bottom.

### Why

The plan is now in-repo and the prior planning handoff (`prompts/COMPLETED/2026-04-27-seedance-generation-handoff.md`) was about *writing* the plan. This new prompt is about *executing* it — a different mode with different guardrails (real money spent, hard human gates, fallback playbook on failure). Specifically encodes:

- **Mode lock:** "Do NOT enter plan mode" — prevents a fresh session from re-planning the already-resolved 12 decisions.
- **Sub-skill recommendation:** `superpowers:subagent-driven-development` per the plan's frontmatter (fresh subagent per task, two-stage review).
- **Hard human gates listed by Task ID:** 3.4, 4.3, 6.3, 8.3, 8.4, 10.1, 11.3 — pause-and-wait, no auto-proceed.
- **Spend triggers requiring explicit user OK:** before `--all` Seedance batch (~$9), before `--all` cleanup (~$10), before any Tier C / Standard escalation; do not silently exceed $25 cumulative.
- **Critical inheritances:** Maintenance Conventions (CHANGELOG every commit), the JPEG-as-PNG re-encode requirement (silent failure mode), the `audit.py` stdout-vs-disk departure for the new auditor, and the "stylus is NOT in Sean's hand in Act 2" clarification (Act 1 rule does not transfer).
- **Fallback playbook:** explicitly references the shot-list-documented fallbacks for S0, REV, PB rather than inventing new ones at runtime.

The prompt itself ends with self-care instructions: move to `prompts/COMPLETED/` after Task 12 ships, per the archive convention.

---

## Repo Reorganization + Maintenance Conventions

**Date:** 2026-04-27

### What changed

- **Saved the canonical Seedance execution plan in-repo with a date prefix:** `docs/2026-04-27-act2-seedance-execution-plan.md`. The plan is the refined version of the prior execution plan, with three validation refinements baked in (`seedance_audit.py` writes markdown to disk vs `audit.py`'s stdout pattern, `reencode_to_png` helper for the JPEG-as-PNG gotcha, anchor sizes confirmed at 700KB–1MB). Defaults to Tier A+B cleanup. Mirror copy of the planning artifact at `~/.claude/plans/please-read-through-prompts-seedance-gen-twinkly-cake.md`.
- **Deleted the prior duplicate** `docs/act2-seedance-execution-plan.md` (untracked, superseded by the dated version above).
- **Reorganized `docs/` and `prompts/`:** introduced `COMPLETED/` (shipped/done plans + prompts) and `OLD/` (superseded docs) subfolders inside each. The roots now contain only active source-of-truth material.
  - **Moved to `docs/COMPLETED/`:** `act1-keyframe-prompts.md`, `kickoff-phase3-sprite-transformation.md`, `phase4-compositing-plan.md`, `procreate-sprite-extraction-guide.md`.
  - **Moved to `docs/OLD/`:** `seedance-production-plan.md`, `Seedance 2 Skill.md`, `kickoff-phase2-comfyui-inbetweens.md`, `kimodo-setup-guide.md`, `phase2-model-requirements.md`, `seedance-pipeline-session-prompt.md`. Debug screenshots (`api-error-2.png`, `sw-portfolio-animation-structure-{1,2}.png`, `ultra-plan-issue.png`) moved to `docs/OLD/screenshots/`.
  - **Moved to `prompts/COMPLETED/`:** all Act 1 keyframe (F06/F10/F13/F18/F31/F36), transition (F20–F28), sprite (F31/F36 with-sprite + 6 sprite design prompts), the entire `in-betweens/` subdir, and the just-completed `seedance-generation-handoff.md` (renamed `2026-04-27-seedance-generation-handoff.md`).
  - **Moved to `prompts/OLD/`:** `act2-continuation-handoff.md`, `act2-exploration-kickoff-prompt.md`, `seedance-pipeline-session-prompt.md`.
- **Updated CLAUDE.md** to match the new layout: fixed four stale path references, updated the Directory Structure diagram to show `COMPLETED/OLD`, rewrote the Prompt Files section.
- **Patched `pipeline/generate.py`** prompt-loader: now checks `prompts/F{##}.txt` first and falls back to `prompts/COMPLETED/F{##}.txt`, so Act 1 re-runs still work after the move.
- **Added a `Maintenance Conventions` section to CLAUDE.md** declaring two rules for every future Claude Code session:
  1. **CHANGELOG.md — update on every change** (what + why).
  2. **CLAUDE.md — update on significant project changes** (so it always reflects current state).
  Plus the archive-folder convention itself.

### Why

Sean started this session in plan mode because he couldn't find the prior Seedance execution plan — it had been written but buried among ~25 other unsorted files in `docs/` (10+ of them stale or shipped). The same pattern applied to `prompts/`: 16 Act 1 prompt files mixed with 3 superseded handoffs and 1 active handoff, no separation between active and archived.

Two systemic fixes:
1. **Active vs archived separation.** `COMPLETED/` and `OLD/` subfolders inside `docs/` and `prompts/` keep the roots scannable. Findability for the *current* work is the primary goal.
2. **Maintenance discipline as a documented convention.** The reason this drift accumulated is that there was no rule about updating CLAUDE.md / CHANGELOG.md as the project evolved. Encoding both as Maintenance Conventions in CLAUDE.md (which is auto-loaded into every session's context) means every future Claude reads the rule before doing any work. No hook is needed because Claude does the writing — a hook would just duplicate what CLAUDE.md already says.

### Lessons learned

25. **Findability is a system property, not a documentation problem.** Adding a sixth README to explain where things live is worse than reorganizing so the location is obvious. Active material in roots, archives in subfolders.
26. **Conventions live in CLAUDE.md, not in memory or hooks.** CLAUDE.md is project-scoped, version-controlled, and auto-loaded — the right home for "every session must do X." Memory is per-user and per-machine; hooks can't write content that requires judgment.
27. **Date-prefix dated artifacts.** `2026-04-27-act2-seedance-execution-plan.md` sorts naturally and tells you when it was authored at a glance. Avoid generic `act2-seedance-execution-plan.md` for things you'll author multiple times.
28. **`git mv` over `mv` for tracked files.** Preserves history and makes the rename visible in `git log --follow`. Use `mv` only for untracked files.

---

## Act 2 Pre-Production Complete — Rounds 1, 2, 3 + Seedance Execution Plan

**Date:** 2026-04-26

### Round 1 — Act 2 Concept Exploration

Generated initial concept frames across the 4 storyworlds (Film, Animation, AI Discovery, Workshop) and explored the AI Companion creature design. Final companion design selected: terracotta-orange loaf creature with dot eyes and stubby arms. Companion turnaround locked at `runs/act2-exploration/concepts/companion/turnaround_02.png`.

Concept directories: `runs/act2-exploration/concepts/zone1/`, `zone3/`, `zone4/`, `companion/`.

### Round 2 — Beat Sheet Locked

**Date:** 2026-04-25

Locked an 11-beat sheet for Act 2: clean walking sequence through Film → Animation → AI Discovery, sit at desk, terminal close-ups (empty + companion appears + Sean POV), pulled-in transition, original revelation moment with mind-map words, PM Kanban scene with grab, pull-back to workshop panorama v3a.

Decision document: `runs/act2-exploration/concepts/round2-decisions.md`.

### Round 3 — Production Anchor Frames + Seedance Shot List

**Date:** 2026-04-26 (commit `84ffa9d`)

Audited the 11 Round 2 concepts against a 6-criterion production checklist (Identity / Aesthetic / Line confidence / Aspect / Continuity / Clean for Seedance). Result: 10 PASS, 1 FAIL.

**Failure caught and fixed:** `zone1/ai_discovery.png`
1. **Stage-direction text leak:** "Beat 1c / Act 2" rendered as visible hand-lettered text in the upper-left next to the production label — NB2 had interpreted prompt planning language as a string to draw.
2. **Stubble continuity break:** Sean had 5-o'clock shadow stubble despite the surrounding walking sequence (`film.png`, `animation.png`) being clean-shaven. The stubble convention is desk-only, not for the walking-through-history beats.

Regenerated with explicit "DO NOT WRITE STAGE-DIRECTION LANGUAGE" + "clean-shaven, no stubble" constraints — passed re-audit.

**4 NEW bridge anchors generated** to support smooth Seedance interpolation between non-adjacent storyboard beats:
- `bridges/film_to_animation.png` (W1→W2 transition)
- `bridges/animation_to_ai.png` (W2→W3 transition)
- `bridges/pre_pulled_in.png` (TR shot start anchor)
- `bridges/pm_role_grabbed.png` (PM end / PB start)

**Act 2 Seedance Shot List written** (`docs/act2-seedance-shot-list.md`): 10 Seedance interpolation clips + 4 FFmpeg holds + 3 hard cuts → ~50s total Act 2 runtime. Each Seedance shot has a start anchor, end anchor, draft 60–100 word prompt, duration, risk tier, and documented fallback strategy.

**Audit document:** `runs/act2-exploration/round3-audit.md`.

### Seedance Generation Phase — Execution Plan Approved

**Date:** 2026-04-26

Wrote and locked the 12-task implementation plan for the Seedance generation phase: `docs/act2-seedance-execution-plan.md`. Resolved 12 architectural decisions from the handoff prompt with explicit justification for each:

| # | Decision | Choice |
|---|---|---|
| 1 | Test shot | T2 (companion appears) on Fast tier 720p — locked camera, single element materializes, gold-standard anchors |
| 2 | Frame hosting | `fal_client.upload_file()` once, cache URLs in `anchor_urls.json` |
| 3 | Orchestration | New `pipeline/seedance_generate.py` modeled on `generate.py`. Sync test mode + async batch (`fal_client.submit` + poll) for production |
| 4 | Audio | `generate_audio: false` (saves latency, avoids stripping silent audio) |
| 5 | Output dir | `runs/act2-seedance-{YYYY-MM-DD}/` with `seedance/`, `extracted/`, `cleanup/`, `shots/`, `audit/`, `export/` subdirs |
| 6 | Frame extraction | Per-clip inside orchestrator at 12fps |
| 7 | NB2 cleanup | **Tiered:** A (always) + B (every 3rd) by default; C (skip) unless flicker observed. 3-reference chaining per call: A-2 + start anchor + extracted frame |
| 8 | Procreate gate | Hard wait at FIN — assembly script blocks until `manual_panorama_cleaned.png` exists |
| 9 | Hard cuts + holds | New `seedance_assemble.sh` with concat demuxer; no default cross-fades (the 3 hard cuts are intentional) |
| 10 | QA enforcement | Hybrid — automated PIL/SSIM checks + structured markdown for Claude vision review (mirrors existing `audit.py` pattern) |
| 11 | Phase boundary | Plan includes assembly through to watchable Act 2 MP4. Two milestones: M1 rough cut, M2 full-fidelity |
| 12 | Cost & time | M1: ~40 min, ~$10. M2: ~3 hr, ~$20 total. Worst-case Tier C: ~$60 |

**6 new pipeline scripts to build** plus 1 YAML to freeze:
- `pipeline/seedance_shotlist.yaml` — machine-readable copy of the shot list
- `pipeline/seedance_lib.py` — shared helpers (fal upload caching, JSONL log, run dir)
- `pipeline/seedance_generate.py` — orchestrator (sync + async batch)
- `pipeline/seedance_extract.py` — FFmpeg `-vf fps=12` wrapper
- `pipeline/seedance_cleanup.py` — NB2 cleanup loop (subprocess to existing `generate_image.py`)
- `pipeline/seedance_audit.py` — automated checks + structured markdown for vision review
- `pipeline/seedance_assemble.sh` — per-shot MP4 build + concat to final Act 2

### Lessons Learned (Act 2 Pre-Production)

19. **Round-based pre-production scales.** Splitting Act 2 prep into Round 1 (concepts) → Round 2 (beat sheet) → Round 3 (production anchors + shot list) prevented scope creep. Each round produced a locked deliverable that the next round consumed without revisiting.
20. **Audit anchor frames against neighbors, not just the A-2 anchor.** The `ai_discovery.png` failure was a within-sequence continuity break (stubble state) that a single-anchor identity audit missed. Continuity-against-neighbors should be its own audit step.
21. **NB2 leaks prompt stage-direction language as visible text.** Words like "Beat 1c", "Act 2", or scene-direction phrasing in the prompt sometimes get rendered into the image as hand-lettered text. Add explicit "DO NOT RENDER STAGE-DIRECTION TEXT" negative to all production prompts; treat it as a continuity gate during audit.
22. **Two-engine philosophy validated at the planning level.** "Seedance finds the motion, NB2 protects the aesthetic" became the structural backbone of the plan: Seedance owns motion intelligence (10 clips, ~$10), NB2 owns aesthetic restoration (Tier A+B cleanup, ~$10). Cost split is ~50/50 — neither engine dominates the other.
23. **Plan with milestones, not endpoints.** Splitting the Seedance phase into M1 (rough cut, no cleanup) → M2 (full-fidelity) lets the user catch unusable Seedance clips before paying for cleanup of those clips. The rough cut is the single highest-leverage QA gate in the plan.
24. **Make decisions, don't ask 12 questions.** The execution plan resolved all 12 architectural decisions from the handoff with explicit justification rather than punting to the user. The user can override any decision they disagree with — but starting from a concrete recommendation is faster than starting from a question.

---

## Seedance 2.0 Pipeline — Research & Planning

**Date:** 2026-04-12

### Creative Interview + Alignment

Conducted Phase 1 creative interview to establish the north star for the Seedance pipeline integration. Key decisions:

**North star:** "This person bridges traditional craft and modern tools." The piece should feel hand-drawn; viewers shouldn't realize it's an AI workflow until they dig into the portfolio projects. The Pixar analogy — they didn't abandon the 12 principles when they moved to CGI.

**Pipeline philosophy — "Seedance finds the motion, NB2 protects the aesthetic":**
Seedance 2.0 generates fluid motion between anchor keyframes. Extracted frames are then redrawn/cleaned by NB2 to restore full pencil test fidelity (line weight, construction lines, paper texture, stylus continuity). This is a two-engine pipeline: Seedance for motion intelligence, NB2 for aesthetic protection.

**Act 1 approach:** Enhance, don't restrict. The existing 42-frame structure is a foundation, not a ceiling. Seedance can add fluidity and breathing room. Frame count is flexible.

**Act 2 approach:** Seedance-guided exploration. Test beats incrementally, let results inform scope. Don't commit to all 250 frames upfront. Stay open to creative possibilities beyond the storyboard.

**Sprite strategy:** The existing Seedance test (`Act-1-Test-Seedance-2.0.mp4`) produced sprite motion that matched Sean's vision. Plan: trace Seedance sprite motion in Procreate to create standalone hand-drawn sprite frames.

**Quality bar:** Every frame must pass the "is this hand-drawn?" test both in motion at 12fps AND in isolation. If it looks digital to a casual viewer, it fails.

### Seedance 2.0 Deep Research

Comprehensive research across three parallel investigations: model capabilities + API, prompting strategies + style preservation, and community results + comparisons.

**Key findings:**
- **Start+end frame interpolation:** Supported. Generates "plausible path between two known states." End frame match is approximate, not pixel-exact.
- **Resolution:** 480p, 720p (no native 1080p). 720p adequate for web portfolio.
- **Duration:** 4–15 seconds per generation at 24fps.
- **Fal.ai API:** `bytedance/seedance-2.0/image-to-video` (standard) and `fast/image-to-video`. Pricing: ~$0.24–0.30/sec. Auth via `FAL_KEY` env var. Python SDK: `fal-client`.
- **Prompting:** 60–80 words. Action-focused (what happens, not body mechanics). Include "fixed camera, locked tripod" always. Include "stylus in right hand" always (feature erosion risk). No "cinematic", "4K", "glow" keywords.
- **Style preservation:** Model handles illustrated/non-photorealistic styles well (anime, cel, line art). No one has tested pencil-on-paper specifically. Risks: "thin, high-contrast edges" are a known limitation; paper texture may "crawl."
- **Character consistency:** 2–3 reference images max. Start+end frame mode is the strongest consistency tool.
- **No negative prompt parameter** on fal.ai. Style control is prompt-only via positive descriptors.
- **Content filters:** Aggressive for realistic human faces, but pencil drawings should pass without issues.
- **Best model for our use case:** Seedance > Kling for illustrated styles. Already proven with our test.

**Documents created:**
- `docs/seedance-research-findings.md` — Full research findings with API specs, prompting guide, code examples
- `docs/seedance-production-plan.md` — Beat-by-beat production plan with all Seedance prompts, QA gates, cost estimates

**Estimated cost:** ~$35 for all 13 clips (26 generations including retries at Fast tier). Budget $50–75 with experimentation.

### Seedance Test Review

Reviewed the existing Seedance 2.0 test output (`Act-1-Test-Seedance-2.0.mp4`): 6 seconds, 1280x720, 24fps, 145 frames.

**What Seedance nailed:**
- Pencil test aesthetic survived (cream paper, warm gray graphite lines, A-2 label)
- Sprite motion arc along pencil trails was exactly as envisioned — natural physics path
- Character identity held across all frames (same hair, jaw, proportions)
- Production label convention (A-2 → A-7) was picked up from anchor frames

**What needs NB2 cleanup (expected):**
- Line weight softened compared to NB2 keyframes — cross-hatching and construction lines diminished
- Stylus disappeared by mid-clip (feature erosion)
- Hand anatomy lost definition in later frames

These findings validated the two-engine pipeline: Seedance contributes motion intelligence, NB2/Procreate restores aesthetic fidelity.

### Lessons Learned

13. **Seedance finds motion, NB2 protects aesthetic** — use video models for motion discovery and image models for final frame quality. Two engines, each doing what they're best at.
14. **Video model prompts: action arcs, not body mechanics** — describe WHAT happens in 60–80 words. Include "fixed camera" and prop continuity notes ("stylus in right hand"). Avoid "cinematic", "4K", or style-pulling keywords.
15. **Start+end frame interpolation is the key mode** — providing both anchor frames produces more constrained, coherent motion than extrapolation from a single frame.
16. **Short clips hold style better** — 4–5 second Seedance clips maintain pencil test aesthetic; longer clips risk style drift.
17. **Feature erosion targets small props first** — the stylus disappears before other features drift. Include explicit prop anchoring in every prompt.
18. **Test cheaply before committing** — use Fast tier at 480p/4s for initial tests, scale to 720p Standard only after validating aesthetic survival.

---

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
