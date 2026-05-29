# Act 2 Seedance Generation Phase — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Take Act 2 from "15 anchor frames + locked shot list" → "watchable Act 2 video file (MP4 + WebM + GIF)" via a Seedance-driven orchestrator, NB2 cleanup loop, and FFmpeg assembly.

**Architecture:** New `pipeline/seedance_generate.py` orchestrator (mirrors the existing `pipeline/generate.py` subprocess + JSONL pattern) drives `fal-client` to produce 10 Seedance interpolation clips. `pipeline/seedance_extract.py` extracts frames at 12fps. `pipeline/seedance_cleanup.py` invokes the existing `generate_image.py` to NB2-restore tiered frame subsets. `pipeline/seedance_audit.py` writes structured markdown QA reports to disk. `pipeline/seedance_assemble.sh` stitches clips + holds + Ken Burns + hard cuts into the final Act 2 video. **Two-milestone delivery: rough cut (M1) → full-fidelity cut (M2).**

**Tech Stack:** Python 3, `fal-client`, `google-genai`, PyYAML, Pillow, FFmpeg, bash.

---

## Context

Round 3 just shipped on `ultraplan/seedance-pipeline` (commit `84ffa9d`). All 15 production anchor frames are locked (10 PASS audit, 1 regenerated, 4 NEW bridges). The shot list (`docs/act2-seedance-shot-list.md`) defines 10 Seedance clips + 4 FFmpeg holds + 3 hard cuts → ~50s Act 2 runtime. Seedance API research is complete (`docs/seedance-research-findings.md`). `FAL_KEY` and `GEMINI_API_KEY` are in `.env`.

**Why now:** Act 1 hero loop has been done for weeks. Act 2 has been in pre-production through Round 1 (concepts) → Round 2 (beat sheet) → Round 3 (production anchors + shot list). This phase converts that planning into a watchable artifact, which is the unblock for portfolio publish.

**The only fundamentally new work** is the bytedance/seedance-2.0 integration. Everything else (NB2 cleanup, FFmpeg assembly, audit logs) reuses existing patterns adapted for video output.

**Note on parallel artifact:** A near-identical execution doc lived at `docs/act2-seedance-execution-plan.md` (untracked, written this session — never committed, no longer on disk). This file is the canonical plan; the in-repo doc serves as the engineer-facing handoff. Both stay aligned.

---

## Validation Findings (codebase audit, 2026-04-27)

Refinements applied on top of prior planning:

1. **Anchor sizes confirmed: 700KB–1MB each** (not 700KB–6MB as initially estimated). All 15 anchors verified on disk under `runs/act2-exploration/concepts/{zone1,zone3,zone4,bridges}/`. Base64 inline is *technically* feasible (~16MB encoded < fal's 100MB limit), but `fal_client.upload_file()` is still the right call — uploads persist across retries and avoid re-uploading 1MB on every `fal_client.subscribe`/`submit` call.

2. **`pipeline/audit.py` writes vision-review prompts to stdout, not disk** (its `get_vision_review_prompt()` at [pipeline/audit.py:52-82](../pipeline/audit.py#L52-L82) returns a string for piping to Claude Code). The new `seedance_audit.py` must instead **write `audit/qa_{shot}.md` files directly to disk** so the user can review them as artifacts and check off boxes. Mirror the *content* of the audit.py template, not its I/O.

3. **`pipeline/assemble.sh` has a known JPEG-as-PNG gotcha** at [pipeline/assemble.sh:159-164](../pipeline/assemble.sh#L159-L164) — Gemini returns JPEG bytes even when the output extension is `.png`, and FFmpeg silently drops them. The cleanup loop's NB2 outputs must be re-encoded with PIL (`Image.open(...).save(..., 'PNG')`) or piped through ImageMagick before FFmpeg ingestion.

4. **`generate_image.py` accepts multiple `--reference` args** (`nargs="+"` at [generate_image.py:202-204](../.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py#L202-L204)) — confirms the cleanup loop's 3-reference invocation pattern works as designed.

5. **`manifest.yaml` is strictly Act 1**, no `act2` section. Decision: do **not** retrofit `manifest.yaml`. Create a new `pipeline/seedance_shotlist.yaml` with its own schema, and add a one-line pointer to it from `manifest.yaml` if discoverability becomes an issue. Keeps Act 1 frozen.

6. **`pipeline/` already contains 8 scripts** (assemble.sh, audit.py, continuity_audit.py, generate.py, generate_inbetweens.py, blender_render_bvh.py, render_bvh_2d.py, composite_sprite.py). The 6 new files this plan adds (`seedance_*.py`, `seedance_*.sh`, `seedance_lib.py`, `seedance_shotlist.yaml`) sit alongside without conflict.

---

## 12 Decision Resolutions

| # | Decision | Resolution |
|---|---|---|
| 1 | **Test-shot strategy** | T2 (companion appears) on Fast tier 720p, 3s, sync via `fal_client.subscribe`. Lowest-risk highest-information: locked camera, single element materializes, both anchors are gold-standard fidelity per Round 3 audit. After T2 passes → Wave 1 (W1, W2, W3, T0, PM, PB) parallel batch, then Wave 2 (S0, TR, REV) Fast tier with Standard escalation if identity fails. |
| 2 | **Frame hosting** | `fal_client.upload_file()` once, cache URLs in `runs/{run_id}/anchor_urls.json`. 15 PNGs × ~1MB = ~15MB. Single upload pass at orchestrator startup; reuse for all retries. |
| 3 | **Orchestration** | New `pipeline/seedance_generate.py` mirroring `generate.py`'s subprocess + manifest + JSONL audit log pattern. Two modes: `--shot <ID>` sync (test mode, iterate prompts) and `--all` async batch (`fal_client.submit` + 10s polling). |
| 4 | **Audio** | `generate_audio: false` always. No diegetic audio in scope; disabling cuts latency and avoids stripping a silent track. |
| 5 | **Output dir** | `runs/act2-seedance-{YYYY-MM-DD}/` matching `runs/{run_id}/` convention. Subdirs: `seedance/` (raw MP4s + meta JSON), `extracted/{shot}/frame_%04d.png`, `cleanup/{shot}/`, `shots/` (per-shot final MP4s), `audit/` (JSONL + per-shot markdown), `export/` (final MP4/WebM/GIF). |
| 6 | **Frame extraction** | Per-clip, inside the orchestrator, immediately after MP4 download via FFmpeg `-vf fps=12`. Tightly coupled to clip generation; failed extraction = failed download (fail fast). |
| 7 | **NB2 cleanup loop** | **Tiered, with explicit reference chaining.** NB2 ≈ $0.08/call, not 10–100× Seedance — full-frame cleanup is ~$48, not ~$1000. Real risk is frame-to-frame style flicker between independently-generated cleanup frames. **Tier A** (always): first + last extracted frame per clip. **Tier B** (default): every 3rd frame. **Tier C** (skip by default): remaining ~60%; re-evaluate after rough cut. Universal cleanup prompt template; per-call references = `[A-2 anchor, shot's start anchor, the extracted frame]`. **User-confirmed: Tier A+B is the M2 default.** |
| 8 | **Procreate gating** | Hard wait at FIN. Pipeline generates ALL Seedance clips first (PB uses dirty panorama — fine, the camera pull-back hides brand-label glitches). FIN Ken Burns is the absolute last step. Assembly script checks for `runs/{run_id}/manual_panorama_cleaned.png`; absent → exit non-zero with clear instructions; present → builds FIN from the cleaned PNG. |
| 9 | **Hard cuts + holds + assembly** | New `pipeline/seedance_assemble.sh` using FFmpeg `concat` demuxer. Per-shot MP4s built individually → concatenated by `assembly_order` from shotlist. **No default cross-fades** — hard cuts are design intent; Seedance interpolations flow naturally. Optional `--crossfade-fallbacks` flag for documented fallbacks (S0 0.3s, PB 0.4s). T1 cursor blink = special case (two NB2-generated cursor variants alternated at 1Hz over 2s). |
| 10 | **QA gate enforcement** | Hybrid. `seedance_audit.py` writes per-clip artifacts: automated PIL/SSIM checks (aspect ratio, MP4 plays, frame count = duration × 12, last extracted frame SSIM vs end anchor ≥ 0.6) + structured markdown `audit/qa_{shot}.md` with the 8 verification gates as checklists for human/Claude vision review. Retry: 1st fail = auto retry with new seed; 2nd fail = invoke documented per-shot fallback (per shot list); 3rd fail = human escalate. |
| 11 | **Phase boundary** | Include FFmpeg assembly through to a watchable Act 2 MP4. Two milestones inside the plan: **M1 (rough cut)** = Seedance + extract + naive assembly, NO cleanup, ~40 min wall-clock, ~$10. **M2 (full-fidelity)** = M1 + Tier A+B cleanup + Procreate panorama + final assembly, ~3 hr wall-clock, ~$20. M1 lets the user judge timing/Seedance fidelity before paying for cleanup. |
| 12 | **Cost & time** | M1: ~40 min, ~$10. M2 (Tier A+B default): ~3 hr, ~$20 total ($10 Seedance + ~$10 NB2). Worst case (Tier C escalation): ~6–8 hr, ~$60. Default path: M1 → review → M2 with Tier A+B → only escalate to Tier C if visible flicker. |

---

## File Structure

**New files (all under `pipeline/`):**

| File | Responsibility |
|---|---|
| `pipeline/seedance_shotlist.yaml` | Frozen, machine-readable copy of the 10 Seedance shots, 4 holds, 3 hard cuts (anchor paths, prompts, durations, fallbacks). Single source of truth for the orchestrator. |
| `pipeline/seedance_lib.py` | Shared helpers: `load_shotlist`, `load_env`, `make_run_dir`, `upload_anchor` (with JSON cache), `log_event` (JSONL appender), `frame_count_at_12fps`, `reencode_to_png` (handles JPEG-as-PNG gotcha). |
| `pipeline/seedance_generate.py` | Orchestrator. `--shot <ID>` sync mode (test) and `--all` async batch mode. Uploads anchors, submits jobs, downloads MP4s, writes `seedance/{shot}_attempt_NN.meta.json`, logs to `audit/seedance_log.jsonl`. |
| `pipeline/seedance_extract.py` | FFmpeg `-vf fps=12` extraction wrapper. Per-shot or `--all`. |
| `pipeline/seedance_cleanup.py` | Tiered NB2 cleanup. Invokes `generate_image.py` per Tier A+B frame with universal prompt + 3 references. Re-encodes outputs to true PNG (gotcha fix). |
| `pipeline/seedance_audit.py` | Per-clip QA. Automated PIL/SSIM checks + writes `audit/qa_{shot}.md` to disk for vision review. |
| `pipeline/seedance_assemble.sh` | Build per-shot MP4s + concat to final Act 2. `--rough` (M1) and `--full` (M2) modes. Special-cases T1 cursor blink, FIN Ken Burns + Procreate gate. |

**Modified files:** `CLAUDE.md` (Phase B.5 commands), `docs/production-checklist.md` (mark phase complete). Optional: one-line pointer in `manifest.yaml` to `seedance_shotlist.yaml`.

**Existing files read but not modified:**

| File | Why |
|---|---|
| [pipeline/generate.py](../pipeline/generate.py) | Subprocess + JSONL pattern template (lines 29–157) |
| [pipeline/audit.py](../pipeline/audit.py) | Markdown vision-review template at lines 52–82 (re-cast to write-to-file) |
| [pipeline/assemble.sh](../pipeline/assemble.sh) | FFmpeg patterns (lines 173–226), JPEG-as-PNG re-encode (lines 159–164) |
| [.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py](../.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py) | NB2 CLI invoked by `seedance_cleanup.py` (multi-`--reference` confirmed) |
| `docs/act2-seedance-shot-list.md` | Source spec for `seedance_shotlist.yaml` |
| `docs/seedance-research-findings.md` | API code template (lines 86–125) |

---

## Execution Order (12 Tasks)

### Task 1: Freeze the shot list as YAML

**Files:** Create `pipeline/seedance_shotlist.yaml`

- [ ] **1.1** Read `docs/act2-seedance-shot-list.md` end-to-end.
- [ ] **1.2** Write `pipeline/seedance_shotlist.yaml` with: top-level `version`, `created`, `style_anchor` (verbatim block from shot list); `shots[]` for the 10 Seedance clips (id, type=seedance, duration, risk, start, end, prompt, fallback); `holds[]` for S1, T1, T3, FIN (id, duration, frame, type ∈ {static, cursor_blink, ken_burns}, optional `requires_manual_cleanup`); `hard_cuts[]` as pairs `[T2,T3]`, `[T3,TR]`, `[REV,PM]`; `assembly_order: [W1,W2,W3,S0,S1,T0,T1,T2,T3,TR,REV,PM,PB,FIN]`.
- [ ] **1.3** Validate: `python3 -c "import yaml; yaml.safe_load(open('pipeline/seedance_shotlist.yaml'))"` → silent success.
- [ ] **1.4** Cross-check anchor paths exist: `for p in $(yq '.shots[].start, .shots[].end, .holds[].frame' pipeline/seedance_shotlist.yaml | sort -u); do test -f "$p" && echo OK $p || echo MISSING $p; done` → 15 OK, 0 MISSING.
- [ ] **1.5** Commit: `git add pipeline/seedance_shotlist.yaml && git commit -m "seedance: freeze shot list as machine-readable YAML"`.

### Task 2: Build `seedance_lib.py`

**Files:** Create `pipeline/seedance_lib.py`

- [ ] **2.1** Implement helpers (full code, not stubs):
  - `load_shotlist(path) -> dict`: `yaml.safe_load`.
  - `load_env(env_file=".env") -> None`: parse `KEY=VALUE` lines, set `os.environ`. Strip whitespace (matches generate_image.py:33-34 behavior).
  - `make_run_dir(prefix="act2-seedance") -> Path`: create `runs/{prefix}-{YYYY-MM-DD}/` with all subdirs (`seedance/`, `extracted/`, `cleanup/`, `shots/`, `audit/`, `export/`).
  - `upload_anchor(path, cache_path) -> str`: read JSON cache; if path missing, call `fal_client.upload_file(path)`, write back. Cache keyed by relative path string.
  - `log_event(run_dir, event_dict) -> None`: append one JSON line to `audit/seedance_log.jsonl` with auto-injected `timestamp` (ISO 8601) and `event_id`.
  - `frame_count_at_12fps(duration_s) -> int`: `int(duration_s * 12)`.
  - `reencode_to_png(path) -> None`: `Image.open(path).convert("RGB").save(path, "PNG")` — fixes JPEG-as-PNG gotcha for any output written by NB2.
- [ ] **2.2** Smoke `make_run_dir` + `log_event`: prints a path, dir + subdirs exist, JSONL has one line.
- [ ] **2.3** Smoke `upload_anchor` against `zone1/film.png`: returns `https://...fal.media/...`; second call returns same URL from cache (no re-upload).
- [ ] **2.4** Commit.

### Task 3: Test-shot mode (T2 sync)

**Files:** Create `pipeline/seedance_generate.py`

- [ ] **3.1** Implement `--shot <ID>` sync path:
  1. `load_env()`; `load_shotlist(...)`; `make_run_dir()`.
  2. `upload_anchor(start)` and `upload_anchor(end)`; cache to `runs/{run_id}/anchor_urls.json`.
  3. `fal_client.subscribe("bytedance/seedance-2.0/fast/image-to-video", arguments={prompt, image_url, end_image_url, resolution: "720p", duration: str(shot.duration), generate_audio: False})`.
  4. Download `result["video"]["url"]` to `runs/{run_id}/seedance/{shot}_attempt_01.mp4`.
  5. Write `seedance/{shot}_attempt_01.meta.json` with `{prompt, seed, fal_request_id, model, duration, tier, timestamp}`.
  6. `log_event({event: "seedance_generated", shot, attempt: 1, ...})`.
- [ ] **3.2** Run: `python3 pipeline/seedance_generate.py --shotlist pipeline/seedance_shotlist.yaml --shot T2 --tier fast --resolution 720p`. Expected: ~2 min wall-clock, MP4 exists, ~$0.72 cost.
- [ ] **3.3** Open the MP4 (`open` on macOS or VLC). **HUMAN GATE.** Check: companion materializes smoothly? Pencil aesthetic preserved? Identity holds? No texture crawl in cream background?
- [ ] **3.4** If FAIL → refine prompt, retry, repeat. If PASS → continue.
- [ ] **3.5** Commit.

### Task 4: Batch mode for the remaining 9 shots

**Files:** Modify `pipeline/seedance_generate.py` (add `--all` async path)

- [ ] **4.1** Implement `--all` path: upload all 15 anchors first (~1 min); `fal_client.submit()` for each non-T2 shot, record `request_id`s; poll `fal_client.status()` every 10s; on completion, `fal_client.result()` + download MP4. Log per-shot success/failure.
- [ ] **4.2** Run: `python3 pipeline/seedance_generate.py --shotlist pipeline/seedance_shotlist.yaml --all --tier fast --resolution 720p --skip T2`. Expected: ~3-5 min wall-clock (longest single clip), 9 MP4s land. Cost: ~$8-9.
- [ ] **4.3** **HUMAN GATE.** Inspect all 9 MP4s. For any clearly broken clip, re-run that shot via `--shot <ID> --attempt 2 --seed <new>` or invoke documented fallback.
- [ ] **4.4** Commit.

### Task 5: Frame extraction

**Files:** Create `pipeline/seedance_extract.py`

- [ ] **5.1** Implement: given a Seedance MP4 path, run `ffmpeg -i {mp4} -vf fps=12 {extracted}/{shot}/frame_%04d.png`. Modes: `--shot <ID>` and `--all`.
- [ ] **5.2** Run: `python3 pipeline/seedance_extract.py --run-dir runs/act2-seedance-2026-04-27 --all`. Expected: ~480-600 PNGs across `extracted/{W1..PB}/`. Wall-clock ~30s.
- [ ] **5.3** Spot-check: `ls runs/{run_id}/extracted/T2 | wc -l` → ~36 (3s × 12fps).
- [ ] **5.4** Commit.

### Task 6: M1 (rough cut) assembly

**Files:** Create `pipeline/seedance_assemble.sh`

- [ ] **6.1** Implement `--rough` mode:
  - Build per-shot MP4s by transcoding raw Seedance MP4s to a uniform codec/fps: `ffmpeg -i {seedance/T2_attempt_01.mp4} -r 24 -c:v libx264 -crf 18 -pix_fmt yuv420p shots/T2.mp4`.
  - Build the 4 hold MP4s from anchor PNGs (S1 static `-loop 1 -t 2`; T1 = stub for rough cut, just hold the empty terminal 2s, no blink yet; T3 static; FIN simple Ken Burns from the **dirty** panorama for rough cut, since Procreate hasn't run yet).
  - Concat per `assembly_order` via `ffmpeg -f concat -i shotlist.txt -c copy export/pencil-test-act2-rough.mp4`.
  - Reuse [pipeline/assemble.sh:205-226](../pipeline/assemble.sh#L205-L226) for two-pass GIF + WebM export.
- [ ] **6.2** Run: `bash pipeline/seedance_assemble.sh runs/act2-seedance-2026-04-27 --rough`. Expected: `export/pencil-test-act2-rough.mp4` (~50s). Wall-clock ~5 min.
- [ ] **6.3** **M1 MILESTONE — HUMAN REVIEW.** Validate timing/pacing. Decide: are holds the right duration? Are any clips so broken they need re-generation, not just cleanup? Are hard cuts working visually?
- [ ] **6.4** Commit.

### Task 7: QA audit

**Files:** Create `pipeline/seedance_audit.py`

- [ ] **7.1** Implement (CLI: `--run-dir <dir> --shot <ID>` or `--all`):
  - Automated checks: aspect ratio (PIL HF01), MP4 plays (ffprobe returncode), frame count at 12fps matches duration, last extracted frame SSIM vs end anchor (PIL fallback if `pillow-simd` unavailable, target ≥ 0.6).
  - **Markdown writer (writes-to-file, departs from audit.py:52-82 stdout pattern):** emit `audit/qa_{shot}.md` with: shot ID, anchor paths, prompt, automated check results, the 8 verification gates from the shot list as `- [ ] PASS / FAIL / NEEDS_CLEANUP` checkboxes, embedded image links to start anchor / end anchor / first extracted / last extracted / Seedance MP4. Mirror audit.py's gate framing.
  - Aggregate to `audit/run_summary.json` with per-shot status.
- [ ] **7.2** Run: `python3 pipeline/seedance_audit.py --run-dir runs/{run_id} --all`. Expected: 10 markdown files + summary JSON.
- [ ] **7.3** **HUMAN + Claude vision review:** open each `qa_{shot}.md`, fill in checkboxes. Any FAIL or NEEDS_CLEANUP shapes Tasks 8/11.
- [ ] **7.4** Commit (the markdown reports themselves are inside `runs/` which is gitignored — the *script* is committed).

### Task 8: NB2 cleanup loop

**Files:** Create `pipeline/seedance_cleanup.py`

- [ ] **8.1** Implement (CLI: `--run-dir <dir> --shot <ID> --tier {A|AB|ABC}` or `--all`):
  - **Tier A:** clip's first + last extracted frame.
  - **Tier B:** every 3rd frame between A's.
  - **Tier C:** remaining frames.
  - For each frame: `subprocess.run([sys.executable, ".claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py", PROMPT, "--output", cleanup/{shot}/{frame}_clean.png, "--aspect-ratio", "16:9", "--reference", "images/2D-Character-Sketch-Sean-v1.png", shot.start, extracted_path, "--env-file", ".env"])`.
  - **Universal cleanup prompt** (verbatim, every shot):
    ```
    Restore this frame to traditional hand-drawn pencil animation on cream paper #FAF5E8.
    Match the line weight, graphite shading, paper grain, and construction-mark style of the
    reference image. Keep the character's pose, position, and expression EXACTLY as shown
    in the input frame — only redraw it in pencil-test fidelity.

    NEGATIVES: no vector lines, no black outlines, no cel shading, no anime style, no
    saturation, no digital painting, no gradients, no airbrush, no pure white background,
    no pure black lines.
    ```
  - **Critical post-step:** call `seedance_lib.reencode_to_png(output_path)` to fix the JPEG-as-PNG gotcha before FFmpeg ingestion.
  - Per-frame `log_event({event: "cleanup", shot, frame, tier, returncode, ...})`.
- [ ] **8.2** Test on T2 first (~36 frames → ~16 cleanup calls): `python3 pipeline/seedance_cleanup.py --run-dir runs/{run_id} --shot T2 --tier AB`. Expected: ~16 cleaned PNGs. Wall-clock ~5 min. Cost: ~$1.50.
- [ ] **8.3** Visually compare 3-4 cleaned vs raw frames. Pencil fidelity restored without losing pose/expression?
- [ ] **8.4** **HUMAN GATE.** If T2 cleanup is good → run all: `python3 pipeline/seedance_cleanup.py --run-dir runs/{run_id} --all --tier AB`. Expected: ~120-200 cleaned frames. Wall-clock ~1.5 hr. Cost: ~$10.
- [ ] **8.5** Commit.

### Task 9: T1 cursor blink (special case)

**Files:** Modify `pipeline/seedance_assemble.sh` (replace cursor-blink stub)

- [ ] **9.1** Generate two cursor variants via `generate_image.py`:
  ```bash
  python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
    "Hand-drawn pencil animation on cream paper. The terminal close-up frame, identical to the reference, except a small dark pencil-block cursor is visible to the right of 'c:\\>_'. No other changes." \
    --output runs/{run_id}/cleanup/T1/cursor_blink_1.png \
    --aspect-ratio 16:9 \
    --reference runs/act2-exploration/concepts/zone3/terminal_closeup_empty.png \
    --env-file .env

  python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
    "Hand-drawn pencil animation on cream paper. The terminal close-up frame, identical to the reference, with NO cursor visible. No other changes." \
    --output runs/{run_id}/cleanup/T1/cursor_blink_2.png \
    --aspect-ratio 16:9 \
    --reference runs/act2-exploration/concepts/zone3/terminal_closeup_empty.png \
    --env-file .env
  ```
  Re-encode both via `reencode_to_png`.
- [ ] **9.2** Update `seedance_assemble.sh` T1: `ffmpeg -framerate 2 -loop 1 -i cleanup/T1/cursor_blink_%d.png -t 2 -r 24 -pix_fmt yuv420p shots/T1_terminal_hold.mp4`.
- [ ] **9.3** Visual check: rebuild T1 alone, play. Cursor blinks at 1Hz over 2s?
- [ ] **9.4** Commit.

### Task 10: Procreate panorama gate + final FIN

**Files:** Modify `pipeline/seedance_assemble.sh` (Procreate gate logic for FIN)

- [ ] **10.1** **HUMAN STEP.** User opens `runs/act2-exploration/concepts/zone4/final_panorama_v3_a.png` in Procreate, fixes brand-label glitches ("ANTHROPIC" duplicate, "AGENT HARNESS"/"AGENT USE"/"TOOL" garbled labels). Exports to `runs/act2-seedance-2026-04-27/manual_panorama_cleaned.png`.
- [ ] **10.2** Update `seedance_assemble.sh` FIN section: in `--full` mode, check for `manual_panorama_cleaned.png`. Absent → print clear instructions ("Open final_panorama_v3_a.png in Procreate, fix brand labels, export to {expected_path}, re-run.") and exit non-zero. Present → run Ken Burns:
  ```bash
  ffmpeg -loop 1 -i manual_panorama_cleaned.png -vf \
    "scale=2400:-1,zoompan=z='1.0':x='if(gte(in_time,0),(in_time/5)*120,0)':y='ih/2-(ih/2)':d=120:s=1920x1080" \
    -t 5 -r 24 -pix_fmt yuv420p shots/FIN_panorama_pan.mp4
  ```
- [ ] **10.3** Dry-run gate (no cleaned PNG) → expect clear error + instructions.
- [ ] **10.4** Drop in cleaned PNG → re-run → expect successful FIN MP4.
- [ ] **10.5** Commit.

### Task 11: M2 (full-fidelity) assembly

**Files:** Modify `pipeline/seedance_assemble.sh` (add `--full` mode)

- [ ] **11.1** In `--full` mode: per-shot MP4s rebuilt from **cleaned frames** (Tier A+B from `cleanup/{shot}/`), interleaved with raw extracted frames where no cleanup exists (Tier C kept raw):
  ```bash
  # Per shot: copy cleaned frames over raw frames in a temp dir (cleaned wins),
  # then ffmpeg -framerate 12 -i {temp}/frame_%04d.png shots/{shot}.mp4
  ```
- [ ] **11.2** Run: `bash pipeline/seedance_assemble.sh runs/act2-seedance-2026-04-27 --full`. Expected: `export/pencil-test-act2.mp4` + `.webm` + `.gif`. Wall-clock ~10 min.
- [ ] **11.3** **M2 MILESTONE — FINAL HUMAN REVIEW.** Validate: identity match to A-2 in every visible frame? Pencil-test aesthetic on cream paper throughout? No flicker between cleaned and uncleaned frames? All 8 per-shot QA gates pass?
- [ ] **11.4** If flicker visible at any boundary → invoke Tier C for that shot only:
  ```bash
  python3 pipeline/seedance_cleanup.py --run-dir runs/{run_id} --shot {ID} --tier ABC
  bash pipeline/seedance_assemble.sh runs/{run_id} --full
  ```
- [ ] **11.5** Commit final pipeline scripts (`runs/` itself is gitignored).

### Task 12: Update CLAUDE.md and production checklist

**Files:** Modify `CLAUDE.md`, `docs/production-checklist.md`

- [ ] **12.1** Append to `CLAUDE.md` Phase B.5 section:
  ```
  ### Act 2 Seedance Pipeline

  Test single shot:    python3 pipeline/seedance_generate.py --shotlist pipeline/seedance_shotlist.yaml --shot T2 --tier fast --resolution 720p
  Batch all 10 shots:  python3 pipeline/seedance_generate.py --shotlist pipeline/seedance_shotlist.yaml --all --tier fast --resolution 720p
  Extract:             python3 pipeline/seedance_extract.py --run-dir runs/{run_id} --all
  Cleanup (Tier A+B):  python3 pipeline/seedance_cleanup.py --run-dir runs/{run_id} --all --tier AB
  Audit:               python3 pipeline/seedance_audit.py --run-dir runs/{run_id} --all
  Assemble (rough):    bash pipeline/seedance_assemble.sh runs/{run_id} --rough
  Assemble (full):     bash pipeline/seedance_assemble.sh runs/{run_id} --full
  ```
- [ ] **12.2** Mark Seedance generation phase complete in `docs/production-checklist.md`.
- [ ] **12.3** Final commit.

---

## Verification

**End-to-end:** Running the full pipeline against the locked anchors produces `runs/act2-seedance-{YYYY-MM-DD}/export/pencil-test-act2.mp4` — a ~50-second, native-aspect (1376×768 inherited from anchors), 24fps MP4 that:
- Plays cleanly in QuickTime / VLC without dropped frames.
- Shows Sean recognizable as A-2 in every visible frame.
- Has cream-paper pencil aesthetic throughout (no digital/anime drift).
- Hits all 14 shot beats in `assembly_order` correctly.
- Has the 3 hard cuts at T2→T3, T3→TR, REV→PM.
- Has cursor blinking in T1.
- Ends on a slow Ken Burns pan over the (Procreate-cleaned) panorama.

**Per-shot QA:** 10 `audit/qa_{shot}.md` reports filled in, all 8 gates passing. Any FAIL gate triggered a documented retry/fallback that's logged in `audit/seedance_log.jsonl`.

**Cost & time:** `audit/run_summary.json` reports total Seedance dollars, total NB2 cleanup dollars, total wall-clock per phase. Should match budget within 30% (~$20 total, ~3 hr).

**Regression smoke:** Act 1's `bash pipeline/assemble.sh runs/run_2026-04-04_174805` still produces a working hero loop — these new scripts don't touch existing files.

---

## Out of Scope

- **Re-generating any anchor frame.** All 15 are locked per Round 3 audit.
- **Music / sound design.** Diegetic audio off; soundtrack is a separate post phase.
- **Procreate brand-label cleanup** for the panorama is a manual user step gated by Task 10; the plan does not automate it.
- **Hand-drawn cleanup beyond Tier A+B.** Tier C only invoked if M2 review shows visible flicker.
- **Act 1 changes.** The hero loop ships as-is.
- **Refactoring `pipeline/generate.py`, `pipeline/audit.py`, or `pipeline/assemble.sh`.** New `seedance_*` files are siblings; existing scripts are untouched.
- **Image hosting infrastructure** (S3, R2, etc.). `fal_client.upload_file()` is sufficient.
- **CI / automated runs.** Pipeline is invoked by hand; no GitHub Actions.
