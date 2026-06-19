# Act 2 Seedance — Manual-Generation Handoff (PAUSED)

> **Status as of 2026-04-27:** The 12-task Seedance execution plan is paused mid-Task-4 human gate. Pipeline scripts are built and a first batch generated, but several clips need manual re-takes. The user will run those manually via the fal.ai web UI (or another route they choose), then bring winning MP4s back into `runs/act2-seedance-2026-04-27/seedance/` so the controller can resume at Task 5 (frame extraction).

**This document is the active handoff. Do NOT archive to `COMPLETED/` until the manual round finishes and Task 5 resumes.**

---

## 1. Where we left off in the 12-task plan

| Task | Status | Artifact |
|---|---|---|
| 1. Freeze shot list as YAML | ✅ DONE | `pipeline/seedance_shotlist.yaml` (commit `9b1fafb`) |
| 2. Build `seedance_lib.py` helpers | ✅ DONE | `pipeline/seedance_lib.py` (commits `5cf3793`, `5374279`, `6a1b98a`) |
| 3. Test-shot mode (T2 sync) | ✅ DONE — gate PASSED | `pipeline/seedance_generate.py` (commits `33dc78f`, `7a9ed74`); T2 MP4 in `runs/act2-seedance-2026-04-27/seedance/T2_attempt_01.mp4` |
| **4. Batch mode for 9 remaining shots** | ⏸ **PAUSED at human gate** | `pipeline/seedance_generate.py --all` (commit `d99b3bf`); 9 MP4s + meta JSONs in `runs/act2-seedance-2026-04-27/seedance/` |
| 5. Frame extraction | ⏳ Pending — resumes when winning MP4s land back | `pipeline/seedance_extract.py` (not yet built) |
| 6. M1 rough-cut assembly | ⏳ Pending | `pipeline/seedance_assemble.sh --rough` (not yet built) |
| 7. QA audit | ⏳ Pending | `pipeline/seedance_audit.py` (not yet built) |
| 8. NB2 cleanup loop | ⏳ Pending | `pipeline/seedance_cleanup.py` (not yet built) |
| 9. T1 cursor blink | ⏳ Pending | extends `seedance_assemble.sh` |
| 10. Procreate panorama gate + FIN | ⏳ Pending — hard human gate | extends `seedance_assemble.sh` |
| 11. M2 full-fidelity assembly | ⏳ Pending — final human gate | `seedance_assemble.sh --full` |
| 12. Update CLAUDE.md + production checklist | ⏳ Pending | docs only |

**Cumulative spend so far:** ~$10.08 on fal.ai (T2 sync $0.96 + 9-shot batch $9.12).

---

## 2. Where the prompts live

The 10 Seedance prompts are the **single source of truth** in `pipeline/seedance_shotlist.yaml`. Each shot's `prompt:` field is a YAML literal block (verbatim copy from `docs/act2-seedance-shot-list.md`). The orchestrator passed `shot["prompt"]` straight to fal.ai with no edits — the prompt the model saw is exactly what's in the YAML. Style anchor block sits at top of the same file (lines 3–7) but is **not** prepended to per-shot prompts — every prompt already includes its own style language.

---

## 3. Where the anchor frames live

All 15 production anchors are locked under `runs/act2-exploration/concepts/`. Round 3 audit (`runs/act2-exploration/round3-audit.md`) marks them PASS. Sizes 700KB–1MB each.

| Subdir | Files | Notes |
|---|---|---|
| `zone1/` | `film.png`, `animation.png`, `ai_discovery.png` | Walking sequence (clean-shaven) |
| `zone3/` | `sit_down.png`, `terminal_closeup_empty.png`, `terminal_closeup_companion.png`, `terminal_pov_sean.png`, `transition_pulled_in.png`, `revelation.png` | Desk/terminal/revelation (stubble) |
| `zone4/` | `pm_role.png`, `final_panorama_v3_a.png` | PM/panorama |
| `bridges/` | `film_to_animation.png`, `animation_to_ai.png`, `pre_pulled_in.png`, `pm_role_grabbed.png` | Round 3 bridge anchors |

---

## 4. Per-shot reference cards (start → end + prompt + actual seed used)

**API parameters used in every call** (fast tier):
- Model: `bytedance/seedance-2.0/fast/image-to-video`
- `resolution: "720p"`
- `duration: "<see effective_duration_s below>"`
- `generate_audio: false`
- `image_url`: start anchor (uploaded to fal.media, URLs cached — see §6)
- `end_image_url`: end anchor

**fal.ai web playground:** https://fal.ai/models/bytedance/seedance-2.0/fast/image-to-video — upload the start frame in the "Image" slot, the end frame in the "End Image" slot, paste the prompt, set duration + resolution, generate.

**Note on duration clamping:** The fal.ai Seedance 2.0 API requires `duration ≥ 4`. T2, TR, PM are spec'd at 3s in the shotlist (creative intent) but were sent to the API at 4s and will be trimmed during assembly. If you regenerate manually, send 4s — the extra second is invisible because all three sit immediately before a hard cut.

---

### W1 — Walk Film (low risk)
- **Start:** `runs/act2-exploration/concepts/zone1/film.png`
- **End:** `runs/act2-exploration/concepts/bridges/film_to_animation.png`
- **Duration:** 4s (sent: 4s)
- **Last seed:** `1372653108`
- **Prompt:**
  > Hand-drawn pencil animation on cream paper. Sean walks steadily from left to right at a relaxed pace, mid-stride throughout, head turning slightly to take in the floating Film props around him. The Film props remain stationary; only Sean walks. Fixed camera, locked tripod. Even, diffuse natural lighting. Maintain pencil line quality, graphite shading, paper grain, consistent line weight, visible construction marks. No digital effects. Smooth 4-second walking interpolation.

### W2 — Walk Animation (low risk)
- **Start:** `runs/act2-exploration/concepts/bridges/film_to_animation.png`
- **End:** `runs/act2-exploration/concepts/bridges/animation_to_ai.png`
- **Duration:** 4s (sent: 4s)
- **Last seed:** `2049001023`
- **Prompt:**
  > Hand-drawn pencil animation on cream paper. Sean continues walking left to right at the same steady pace through the Animation world. The Film props on the left fade out via lightening pencil pressure; the Animation props (figure studies, light box, animation books) brighten then start to fade as the AI headlines emerge on the right. Fixed camera, locked tripod. Even, diffuse lighting. Maintain pencil line quality, paper grain, consistent line weight. No digital effects. Smooth 4-second walking interpolation.

### W3 — Walk AI (low risk)
- **Start:** `runs/act2-exploration/concepts/bridges/animation_to_ai.png`
- **End:** `runs/act2-exploration/concepts/zone1/ai_discovery.png`
- **Duration:** 4s (sent: 4s)
- **Last seed:** `1537961300`
- **Prompt:**
  > Hand-drawn pencil animation on cream paper. Sean continues walking left to right at the same steady pace, eyebrow lifting and head turning in growing curiosity. The remaining Animation props fade out; the AI news clippings (ChatGPT, Karpathy, Vibe Coding, Anthropic, Gemini headlines) solidify with hand-lettered text. Fixed camera, locked tripod. Even, diffuse lighting. Maintain pencil line quality, hand-lettered text quality, paper grain, consistent line weight. No digital effects. Smooth 4-second walking interpolation.

### S0 — Arrive at Desk (HIGH risk — most ambitious morph in Act 2)
- **Start:** `runs/act2-exploration/concepts/zone1/ai_discovery.png`
- **End:** `runs/act2-exploration/concepts/zone3/sit_down.png`
- **Duration:** 4s (sent: 4s)
- **Last seed:** `268853034`
- **Documented fallback:** hard cut from `ai_discovery.png` to `sit_down.png` with 0.3s cross-fade in FFmpeg post.
- **Prompt:**
  > Hand-drawn pencil animation on cream paper. The floating AI news headlines dissolve away from the frame as the desk, laptop, second monitor, coffee mug, and chair materialize in their place. Sean transitions from a mid-stride walk to a seated working pose at the desk. A subtle 5-o'clock shadow stubble grows in on his face as time passes. Fixed camera, locked tripod. Even, diffuse desk lighting. Maintain pencil line quality, paper grain, consistent line weight. No digital effects. Smooth 4-second transition interpolation.

### T0 — Push-in to Terminal (medium risk — push-in + pose change)
- **Start:** `runs/act2-exploration/concepts/zone3/sit_down.png`
- **End:** `runs/act2-exploration/concepts/zone3/terminal_closeup_empty.png`
- **Duration:** 4s (sent: 4s)
- **Last seed:** `1934474032`
- **Documented fallback:** split into S1.5 (Sean settles hands, no camera move) + T0 (pure camera push-in, Sean static) if jitter appears.
- **Prompt:**
  > Hand-drawn pencil animation on cream paper. Camera pushes slowly forward into the laptop screen on the desk. Sean's hands settle onto the keyboard as the camera approaches. The laptop and dark cross-hatched terminal window grow to fill the frame as the desk surroundings recede outside the frame. Single slow camera push-in, no other movement. Even, diffuse desk lighting. Maintain pencil line quality, graphite shading, paper grain, consistent line weight. No digital effects. Smooth 4-second push-in interpolation.

### T2 — Companion Appears (low risk; PASSED gate; in seedance/T2_attempt_01.mp4)
- **Start:** `runs/act2-exploration/concepts/zone3/terminal_closeup_empty.png`
- **End:** `runs/act2-exploration/concepts/zone3/terminal_closeup_companion.png`
- **Duration:** 3s spec → sent 4s (will trim to 3s in assembly; sits immediately before a hard cut)
- **Last seed:** `96653238`
- **Prompt:**
  > Hand-drawn pencil animation on cream paper. The terracotta-orange AI companion creature materializes inside the dark cross-hatched terminal window. Small pencil sparkle marks appear around it as it forms. The terminal text shifts from "c:\\>_ what is..." to "c:\\>_ hello, sean...". Fixed camera, locked tripod. Even, diffuse lighting from the laptop screen. Maintain pencil line quality, cross-hatching density, hand-lettered text quality, paper grain. Consistent line weight. No digital effects. Smooth 3-second materialization interpolation.

### TR — Hand Grab (medium risk; HARD CUT from T3)
- **Start:** `runs/act2-exploration/concepts/bridges/pre_pulled_in.png`
- **End:** `runs/act2-exploration/concepts/zone3/transition_pulled_in.png`
- **Duration:** 3s spec → sent 4s
- **Last seed:** `376898827`
- **Prompt:**
  > Hand-drawn pencil animation on cream paper. The companion's terracotta arm fully emerges from the laptop screen and the small terracotta hand reaches across and grabs Sean's right hand. Sean leans further forward and his eyes widen as he is pulled toward the screen. A few pencil motion-line marks accentuate the lean. Fixed camera, locked tripod. Even, diffuse desk lighting with cool blue screen-light tint on Sean's face. Maintain pencil line quality, paper grain, consistent line weight. No digital effects. Smooth 3-second action interpolation.

### REV — The Revelation (HIGH risk — biggest visual leap)
- **Start:** `runs/act2-exploration/concepts/zone3/transition_pulled_in.png`
- **End:** `runs/act2-exploration/concepts/zone3/revelation.png`
- **Duration:** 5s (sent: 5s)
- **Last seed:** `76012933`
- **Documented fallbacks:** (1) drop duration to 4s; (2) generate intermediate `bridges/being_pulled.png` and split into REV1 (transition_pulled_in.png → being_pulled.png, 3s) + REV2 (being_pulled.png → revelation.png, 3s).
- **Prompt:**
  > Hand-drawn pencil animation on cream paper. Sean is pulled forward by the companion. The desk and laptop dissolve into open cream paper space. Hand-lettered concept words (VIBE CODING, AGENTS, PIPELINES, GENERATE) and small pencil-drawn diagrams (code editors, neural network nodes, prompt-to-output flow) emerge around Sean and the companion as a mind-map. Sean stands upright with arms spreading outward in a moment of revelation. The companion floats nearby. Fixed camera, locked tripod. Even, diffuse lighting. Maintain pencil line quality, hand-lettered text, paper grain, consistent line weight. No digital effects. Smooth 5-second revelation interpolation.

### PM — Grab Kanban (low risk; HARD CUT from REV)
- **Start:** `runs/act2-exploration/concepts/zone4/pm_role.png`
- **End:** `runs/act2-exploration/concepts/bridges/pm_role_grabbed.png`
- **Duration:** 3s spec → sent 4s
- **Last seed:** `2104407469`
- **Prompt:**
  > Hand-drawn pencil animation on cream paper. Sean reaches forward to the Kanban board, plucks one card from the IN PROGRESS column with his right hand, and brings it down to chest height. His expression shifts from focused selection to a small satisfied half-smile. The companion floats steadily in the same position camera-right of Sean. The Kanban board columns and sticky notes remain stationary. Fixed camera, locked tripod. Even, diffuse lighting. Maintain pencil line quality, hand-lettered text on the board, paper grain, consistent line weight. No digital effects. Smooth 3-second action interpolation.

### PB — Pull Back (medium risk — pull-back + new content at edges)
- **Start:** `runs/act2-exploration/concepts/bridges/pm_role_grabbed.png`
- **End:** `runs/act2-exploration/concepts/zone4/final_panorama_v3_a.png`
- **Duration:** 5s (sent: 5s)
- **Last seed:** `1936106111`
- **Documented fallback:** hard cut from `pm_role_grabbed.png` to `final_panorama_v3_a.png` with 0.4s cross-fade in FFmpeg.
- **Prompt:**
  > Hand-drawn pencil animation on cream paper. Camera pulls slowly backward from the medium PM scene, revealing the wider workshop panorama with Film camera, Animation reference materials, AI news clippings, and agentic workflow diagrams arranged across the cream paper space. Sean and the companion remain in their positions on the right side of the frame as the panorama widens around them. Single slow camera pull-back, no other movement. Even, diffuse lighting. Maintain pencil line quality, hand-lettered text, paper grain. No digital effects. Smooth 5-second pull-back interpolation.

---

## 5. Holds, hard cuts, and assembly order

These are NOT generated by Seedance — they're FFmpeg operations downstream.

| Hold | Type | Duration | Frame |
|---|---|---|---|
| S1 | static | 2s | `zone3/sit_down.png` |
| T1 | cursor_blink (1Hz) | 2s | `zone3/terminal_closeup_empty.png` (+ NB2 cursor variants in Task 9) |
| T3 | static | 2s | `zone3/terminal_pov_sean.png` |
| FIN | ken_burns pan | 5s | `zone4/final_panorama_v3_a.png` (Procreate-cleaned version, Task 10) |

**Hard cuts:** `T2 → T3`, `T3 → TR`, `REV → PM`.

**Assembly order:** `W1 → W2 → W3 → S0 → S1 → T0 → T1 → T2 → T3 → TR → REV → PM → PB → FIN` (≈50s total at 24fps assembly).

---

## 6. Cached fal.media anchor URLs (skip re-uploading)

If you regenerate via the fal.ai web UI and want to reuse the same anchor URLs the script already uploaded, point at these (also in `runs/act2-seedance-2026-04-27/anchor_urls.json`):

| Anchor | URL |
|---|---|
| `zone1/film.png` | https://v3b.fal.media/files/b/0a97fc9a/Ei2pfejGBMOTO0_1MSWQd_film.png |
| `zone1/ai_discovery.png` | https://v3b.fal.media/files/b/0a97fc9a/YkQcBX0BowD5Fc6HHtFkN_ai_discovery.png |
| `bridges/film_to_animation.png` | https://v3b.fal.media/files/b/0a97fc99/wEz1-5lY6lK5xxnnTnile_film_to_animation.png |
| `bridges/animation_to_ai.png` | https://v3b.fal.media/files/b/0a97fc99/6vVpedlNcZyjXXcUp8sqY_animation_to_ai.png |
| `bridges/pre_pulled_in.png` | https://v3b.fal.media/files/b/0a97fc9a/K4X1YSmPzyZf7Ewr9pCwj_pre_pulled_in.png |
| `bridges/pm_role_grabbed.png` | https://v3b.fal.media/files/b/0a97fc99/ItYZOmsawLOPzeT-76pf7_pm_role_grabbed.png |
| `zone3/sit_down.png` | https://v3b.fal.media/files/b/0a97fc9a/JJjDCiYslD1z6Fm8dVtSg_sit_down.png |
| `zone3/terminal_closeup_empty.png` | https://v3b.fal.media/files/b/0a97fbf0/LyKsvDT4h-Rat2_bBLfGu_terminal_closeup_empty.png |
| `zone3/terminal_closeup_companion.png` | https://v3b.fal.media/files/b/0a97fbf0/Px4MW8Vw9IdNtzF2jPpHJ_terminal_closeup_companion.png |
| `zone3/transition_pulled_in.png` | https://v3b.fal.media/files/b/0a97fc9a/6saN3OPxyYUrXKplpp4J7_transition_pulled_in.png |
| `zone3/revelation.png` | https://v3b.fal.media/files/b/0a97fc9a/qq04EvJHorCbUiS9UNTeU_revelation.png |
| `zone4/pm_role.png` | https://v3b.fal.media/files/b/0a97fc9a/emcq7q2R7_eyNOF0FfSIq_pm_role.png |
| `zone4/final_panorama_v3_a.png` | https://v3b.fal.media/files/b/0a97fc9a/HfCvQkHC3W2pZmw0KwIiz_final_panorama_v3_a.png |

(`zone3/terminal_pov_sean.png` is only used as a hold frame, never as a Seedance anchor — not uploaded.)

---

## 7. Where to drop winning MP4s when you return

To resume the pipeline, place each kept clip at:

```
runs/act2-seedance-2026-04-27/seedance/{shot_id}_attempt_{NN}.mp4
```

…where `{shot_id}` is one of `W1, W2, W3, S0, T0, T2, TR, REV, PM, PB` and `{NN}` is `01`, `02`, etc. The current 10 attempt-01 MP4s already exist; replace any clip in-place by either:

- **Overwriting the attempt-01 file** (delete the old one, drop in the new with the same name), OR
- **Adding a fresh attempt** (e.g. `S0_attempt_02.mp4`) and we'll point the extractor + assembly at the chosen attempt during Task 5.

**Optional but useful:** alongside each MP4 you keep, drop a sibling `{shot_id}_attempt_{NN}.meta.json` with at least `{"shot_id": "...", "duration_s": <int>, "effective_duration_s": <int>, "source": "manual"}`. Without it, the audit script will still work but won't know what duration/seed produced the clip. The existing meta JSONs from this batch can be a template.

If you regenerate via the fal.ai web UI, you can `curl -L -o {dest} '{video_url}'` to download once it's done.

---

## 8. Deferred code-fixes (apply when we resume the pipeline; non-blocking for manual round)

The two background reviewers flagged these on Task 4 — they're fine for a manual round but should be addressed before Task 5 runs against the new MP4s:

**Important — sync path lacks `fal_request_id`** (`pipeline/seedance_generate.py:145`)
The sync `--shot` flow uses `fal_client.subscribe`, which does NOT expose `request_id`. T2's meta JSON has `fal_request_id: null`. Backport `fal_client.submit` + `handler.request_id` capture from the async path so single-shot reruns are also traceable in fal.ai's dashboard.

**Important — meta JSON not written on batch download failure** (`pipeline/seedance_generate.py:625-638`)
If `fal_client.result()` succeeds but the local download raises, the `video_url`/`seed`/`request_id` survive only in the JSONL. Write a partial meta with `"video_path": null, "error": ...` in the except block before `failed.append(...)`.

**Minor — duplicate submit log events** (`pipeline/seedance_generate.py:331-363`)
`_submit_one` emits `seedance_submit` and then `seedance_submit_async` per shot — nearly identical payloads. Drop the first; keep `seedance_submit_async` (which carries `fal_request_id`).

**Minor — `--skip` doesn't validate IDs** (`pipeline/seedance_generate.py:403`)
Typing `--skip T9` silently skips nothing. Two-line check: warn or fail if a `--skip` ID is not in the shotlist.

**Minor — `_rel` helper duplicated** between sync (`run_shot_sync` line 232) and absent from async summary. Hoist to module scope; reuse in the batch summary so paths print relative when possible.

**T2 has 2 `seedance_submit` JSONL events**, not 1 — artifact of the first 3s submit being rejected by the API before Task 3 added the 4s clamp. Documented here so it doesn't surprise the auditor.

---

## 9. To resume

When manual videos are ready:

1. Drop them into `runs/act2-seedance-2026-04-27/seedance/{shot_id}_attempt_NN.mp4` (per §7).
2. Tell the controller "manual round done — winning MP4s are in place; resume at Task 5."
3. The controller will optionally apply the deferred fixes from §8, then proceed to Task 5 (frame extraction at 12fps), Task 6 (M1 rough cut), and onward through the gates.

**Files this handoff supersedes / extends:**
- Does NOT supersede `docs/2026-04-27-act2-seedance-execution-plan.md` — that's still the master plan.
- Does NOT supersede `pipeline/seedance_shotlist.yaml` — that's still the source of truth for prompts and anchors.
- Captures the runtime inventory (seeds, fal.media URLs, attempt files) that the YAML doesn't track.
