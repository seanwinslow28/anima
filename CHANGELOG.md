# Changelog

## 2026-05-24 — Synthesize 9 deep-research reports into Image-Model-DR-2026 decision doc

**What changed:** Created `docs/Image-Model-DR-2026/SYNTHESIS.md` — cross-source synthesis of the 9 deep-research reports (Perplexity / Gemini / ChatGPT × Prompts 1–3) Sean ran, plus 3 last30days raw scans and 2 Gemini-produced PNG charts (`gemini-api-cost-graph.png`, `gemini-proposed-workflow.png`). Three parallel general-purpose subagents (per `superpowers:dispatching-parallel-agents`) each consumed 4 reports — one per prompt theme (master survey / identity preservation / image editing) — and returned ~700–900-word consensus extracts noting agreement strength (4/4, 3/4, 1/4 outlier), disagreements with adjudication, surprises from the last30days scan vs DR, and three recommended configs per theme. Main session then integrated the three syntheses + both charts into a single decision doc with: 5 headline findings, a consensus pick table by job (keyframe / in-between / mask edit / instruction edit / identity / pencil-lock / interpolation / aesthetic propagation), three unified configurations (Best Quality / Best Value / Fully Self-Hosted on 4090), a tomorrow-morning experiment plan ranked by ROI (~5hrs total / ~$5 cost), defer list, open questions, and a source-map table flagging each engine's strongest and weakest contributions.

**Why:** The 14-file research dump (~1.2MB markdown + 2 PNGs) is too dense to act on without integration, and Sean explicitly delegated "be smart about how you'll analyze and synthesize." Parallel subagents preserve main-session context while letting three independent investigations run concurrently (~70 sec each vs ~3+ min sequential). Synthesis surfaced five plan-changing findings the user could not have spotted by reading any single report: (1) **Sean's NB2 cost baseline is wrong** — $0.039/img was NB1; NB2 is actually ~$0.067–0.151/img, so the cost case for replacement is even stronger than the original brief assumed (caught only by Perplexity Prompt 3); (2) **Seedream 4.0 / SeedEdit 3.0 at ~$0.007–$0.03/img** is the consensus value play at ~80% savings vs NB2 (matches Gemini's $7-per-1K-frames cost chart but is missing from Gemini's own proposed workflow diagram — an integration gap only visible when cross-referencing both PNGs); (3) **GPT-Image-2 was missed by Perplexity and Gemini DR** (post-cutoff) but dominates the last30days practitioner scan — Sean should upgrade from gpt-image-1 before swapping vendors; (4) **ByteDance "Lance" (3B, Apache 2.0, May 18 2026)** was missed by all 3 DR reports but is the top r/StableDiffusion thread in last30days — single-model collapse of generate+edit+interpolate if it delivers; (5) **pencil-on-cream preservation is an unsolved benchmark** — Sean would be among the first practitioners building this pipeline, so the synthesis recommends he construct his own 20-pair before/after benchmark as part of the work. Doc closes with three time-boxed experiments ranked by ROI (train character LoRA on FLUX.1-dev via ai-toolkit → Qwen-Image-Edit-2511 ComfyUI edit test → $5 Seedream 4.0 fal.ai pilot) so the next session has a concrete action plan instead of a 1.2MB reading list. Filed inside `docs/Image-Model-DR-2026/` alongside the raw reports (precedent: `docs/open-sourced-video-model-research/SYNTHESIS.md`) so future sessions read SYNTHESIS.md first and only descend into raw reports when verifying a specific claim.

---

## 2026-05-22 — Add deep-research prompts for cheaper character-consistent image models

**What changed:** Created `docs/research/deep-research-prompts-image-models.md` — three engineered prompts to run in Perplexity Deep Research, Gemini Deep Research, and ChatGPT Deep Research. Prompt 1 is a master survey of 2025–2026 closed-source and open-source image generation + editing models scored against the Pencil Test use case (character preservation, hand-drawn aesthetic, multi-image conditioning, cost/VRAM). Prompt 2 is an identity-preservation deep-dive (IP-Adapter family, InstantID, PuLID, LoRA training, ConsiStory/StoryDiffusion/IC-LoRA, and in-between-specific workflows like ToonCrafter / AnimeInbet / EISAI). Prompt 3 is an editing deep-dive (FLUX Kontext, Qwen-Image-Edit, OmniGen2, SeedEdit, InstructPix2Pix variants, hand-drawn style preservation during edits). Each prompt is XML-light but structurally rich — labeled role, project context, current-stack exclusions, numbered research tasks, comparison-table output spec, and hard rules requiring URL + date citations. Doc ends with engine-specific notes (Perplexity strongest for recent web/practitioner sources, Gemini for arXiv/academic, ChatGPT for synthesis tables).

**Why:** Nano Banana 2 is excellent for keyframes but uneconomic across hundreds of in-between frames. Sean wants to reserve NB2 + GPT-image-1 for keyframes and route in-betweens through cheaper closed-source or self-hosted open-source models without losing recognizable likeness or the pencil-test aesthetic. Web-search-enabled deep research is the right tool because the image-model landscape moved hard in late 2025 / early 2026 (FLUX Kontext, Qwen-Image-Edit, HiDream, OmniGen2, HunyuanImage 2.1, PuLID-FLUX) and a knowledge-cutoff-only answer would miss the most recent and cheapest options. Filed under `docs/research/` (not `docs/COMPLETED/` or `docs/OLD/`) because it's an active research artifact — once Sean runs the three prompts and selects models, the resulting findings doc will land alongside (similar to how `docs/open-sourced-video-model-research/` houses the parallel video-model survey). Three prompts instead of one because the base-model question, the identity-preservation question, and the editing question are independent axes with different best-in-class winners; running them separately produces sharper signal than one mega-prompt that the deep-research engines would compress unevenly.

---

## 2026-05-14 — Reorganize research notes into `docs/research/` + update CLAUDE.md pointers

- **Moved:** `docs/seedance-research-findings.md` → `docs/research/seedance-research-findings.md`. The new `docs/research/` directory now collects external research source material (Seedance findings, ChatGPT/Gemini/Perplexity query packets, autoresearch skill optimizer prompt) separate from active project plans in `docs/`.
- **CLAUDE.md path fixes:** Source-of-truth table row for Seedance Research, the directory-tree diagram, and the Seedance prompting rules link all now point at the new path.
- **Why:** keeps the active `docs/` root focused on production plans/specs; research dumps were starting to clutter the root and obscure what's actionable.

---

## 2026-05-10 — Package Seedance v4 template as portable `seedance-prompting` skill

- **New skill:** `~/.claude/skills/seedance-prompting/SKILL.md` — packages the locked v4 template + bake-off-derived rules as a personal Claude Code skill so the prompt structure is available in any project, not just this one.
- **Scope:** Universal Seedance 2.0 image-to-video prompting principles (word count, no negation, banned words, no audio, single camera, transition-arc framing, Fast tier default, dual-seed runs) plus the locked pencil-test fills (genre anchor, style block) and an "Adapting to other aesthetics" section with substitution patterns for cel/gouache/rotoscope styles.
- **Skill description triggers** on "Seedance", "fal.ai video", "image-to-video", "I2V", "video between two keyframes", "animate keyframes", "pencil test video", "in-between video model", "Bytedance video model".
- **Validated via TDD:** Baseline subagent (no skill) violated 7 of 9 locked rules on a generic mouse/cardboard-moon test shot (negation, frame re-description, multi-camera directives, missing genre anchor, missing transition-arc, wrong style block, ~105 words). Verification subagent with skill invoked produced textbook compliance — exact locked structure, ~95 words, all 9 rules satisfied, Fast tier + dual-seed recommendation.
- **Cross-references added:** `prompts/seedance-template-v4.md` notes the portable skill in its header. `CLAUDE.md` row for the v4 template now mentions the skill path.
- **Why a separate skill rather than just relying on the project doc:** project-local files only load when working in this repo; the portable skill lets future Claude Code sessions on other animation projects (or repurposed pencil-test work in other directories) automatically apply the bake-off-validated structure without copying files around.

---

## 2026-05-10 — Seedance prompt template v4 (bake-off)

- **Locked `prompts/seedance-template-v4.md`** as the canonical Seedance 2.0 prompt template, replacing v3 (`docs/2026-05-02-act2-seedance-prompts-v3-conversation-style.md`).
- Winning variant: **V08 combined_best** — score 12/20 across W1 (walk shot) + S0 (identity-stress shot) test shots. Three-way tie at 12 (V01, V02, V08); V08 won tiebreaker 1 (S0 score = 6 vs V01's 4) and tiebreaker 2 (shorter prompt at ~91 words vs V02's ~95 words). Sean confirmed V08 has the best overall outputs for walking, background movements, head movements, and transitions.
- **Fast tier locked as production default.** Two Standard-tier verifications (V08/S0 identity-stress + V08/PM→PB panorama harder scene) both showed Fast producing smoother motion and cleaner transitions at half the cost. The design-spec assumption that "Standard ≥ Fast" was wrong for pencil-test aesthetic content.
- Process: 3-phase plan (deep research → 9-variant structured bake-off → tier verification). Spec at [docs/2026-05-09-seedance-prompt-bakeoff-design.md](docs/2026-05-09-seedance-prompt-bakeoff-design.md). Results at [docs/2026-05-09-seedance-prompt-bakeoff-results.md](docs/2026-05-09-seedance-prompt-bakeoff-results.md). Phase 1 deep research surfaced 5 settled priors (drop negation; trim word count; don't redescribe frames; banned-words list; structured prose beats JSON). Phase 2 bake-off resolved 6 testable axes with empirical evidence on Sean's specific aesthetic.
- Per-axis findings:
  - Genre anchor ("classic Disney rough animation"): **load-bearing** (V06 without it dropped to 4/20).
  - Transition-arc framing ("Starting with… transitioning through… ending with…"): **helps S0 by +2 points**.
  - Animation-timing language (anticipation/weight shift/follow-through): **helps W1, hurts S0** — embed only on physical-motion shots.
  - In-prompt audio descriptors: **catastrophic** (V04 = 4/20). Never use.
  - "Micro push-in 2%, 50mm look" canonical camera: hurts standalone (V05 = 8/20) but works inside the V08 stack.
  - Trimmed style block ("Graphite on cream paper, organic line wavering, warm ivory tone"): hurts standalone (V07 = 6/20) but works inside the V08 stack.
- Total cost: $39.36 (Phase 1 free; Phase 2 = $0.96 smoke + $33.60 full bake-off + $1.92 S0 verify + $2.88 PM→PB Fast+Standard verify). Total wall-clock: ~11 min for generation; manual scoring + analysis spread across 2026-05-09 / 2026-05-10.
- New infrastructure: `pipeline/seedance_bakeoff.py` (orchestrator), `pipeline/seedance_bakeoff_variants.yaml` (variant matrix), `tests/test_seedance_bakeoff_lib.py` (first unit tests in the repo). Helpers `load_bakeoff_variants()` and `make_bakeoff_run_dir()` added to `pipeline/seedance_lib.py`.
- Sean used a 3-tier ordinal scoring system (great / liked / not noted) instead of the 5-binary-criteria rubric the plan anticipated — translated to {5, 3, 1} per cell. Halt 2 (≥14/20) was raised under strict reading; Sean reviewed the per-axis findings and confirmed V08 as winner. Halt 1 (V00 wins by 2+ over V01) did not fire — V01 actually beat V00 by 2, validating Phase 1 research priors.

---

## 2026-05-09 — Add load_bakeoff_variants + make_bakeoff_run_dir helpers; establish tests/ directory

**What changed:**
1. `pipeline/seedance_lib.py` — appended two new helpers at end of file (after `reencode_to_png`):
   - `load_bakeoff_variants(path)` — loads and validates the bake-off variants YAML, raises `FileNotFoundError` for missing files and `ValueError` for missing required top-level keys (`test_shots`, `seeds`, `variants`).
   - `make_bakeoff_run_dir(base)` — creates `runs/seedance-bakeoff-{YYYY-MM-DD}/` and returns the Path; idempotent.
   No existing imports were added (yaml, datetime, Path already at module top).
2. `tests/__init__.py` — empty file; establishes the `tests/` package, the first unit-test directory in the codebase.
3. `tests/test_seedance_bakeoff_lib.py` — 5 unit tests covering the two new helpers: dict-shape validation, FileNotFoundError on missing file, ValueError on missing required key, date-stamped dir creation, and idempotency.

**Why:** Task 2 of the Seedance Prompt Bake-off plan (2026-05-09). The bake-off orchestrator (Task 3) needs a validated way to load the variants YAML and a stable run-dir naming scheme that matches the standard `runs/` layout. Pure-function helpers are isolated here so they can be unit-tested without any fal.ai API calls — matching the existing pattern where `upload_anchor` (API-dependent) has no unit tests and only integration coverage via live smoke runs. TDD cycle followed: tests written first (Step 3 confirmed `ImportError: cannot import name 'load_bakeoff_variants'`), then implementation, then 5/5 passing (Step 5).

---

## 2026-05-02 — Add Act 1 Seedance integration plan + supporting reference artifacts

**What changed:** Added five additional artifacts created during the v2/v3 Seedance prompt iteration and the Act 1 finishing kickoff:

1. `docs/2026-05-02-act1-seedance-integration-plan.md` — the plan deliverable produced from running `prompts/2026-05-02-act1-seedance-finishing-plan-kickoff.md`. Covers cherry-picking strong motion frames from the existing 24fps Seedance test pass, NB2 cleanup of selected frames, drop-in IB-slot replacement only (keyframe slots stay locked), Phase 4 sprite-fade verification, and a final QA pass against the Engine Truth before shipping the GIF/WebM. Builds against the existing run `runs/run_2026-04-04_174805` — no new run created.
2. `docs/Conversation-that-utilized-prompt-science-successfully.md` — verbatim Veo 3.1 Street Fighter II conversation transcript that produced the project's strongest video output to date. Source material for the v3 prompt restructure (named genre anchor, delimited `CRITICAL STYLE REQUIREMENTS:` block, labeled `CAMERA:` paragraph, `Duration:` closer). Kept in `docs/` so v3's lineage is reproducible — anyone reviewing v3 can read the source the structural patterns came from.
3. `prompts/2026-04-27-seedance-execution-kickoff.md` — companion kickoff prompt for the Seedance Generation Phase plan committed in `8a0d64e`. Read-these-first ordering, locked-execution mode (no plan re-litigation), and per-task hand-off cues. Referenced by name from the 2026-05-02 Act 1 finishing kickoff entry as the format precedent.
4. `docs/open-sourced-video-model-research/` — 4-file research synthesis (Perplexity + Gemini deep-research outputs, a Compass artifact, and a `SYNTHESIS.md` consensus). Top consensus: Wan 2.2 (14B) FLF2V is the closest open-source equivalent to Seedance 2.0 for start+end frame interpolation; LTX-Video is the speed king on Mac via MLX; FramePack handles long holds and identity preservation. **Status: post-portfolio-project testing only** — the production pipeline stays on NB2 + Seedance 2.0 through portfolio completion. Filed in `docs/` (not `docs/COMPLETED/` or `docs/OLD/`) because it's an active reference for the next phase, not a shipped or superseded artifact.
5. `images/Claude-Mascot/` — 3 reference mascot images used during v3 prompt iteration to test prompt-science framing on a different character archetype. Reference-only; not part of the Pencil Test character set and not linked from `manifest.yaml` or any source-of-truth doc.

**Why:** All five files were produced as part of the active Seedance iteration work but weren't yet captured in the CHANGELOG. Documenting them now so the decision history stays trustworthy and future sessions don't mistake the integration plan for a stale draft, the conversation transcript for ad-hoc material, or the open-source research for a production pivot. The mascot images are noted explicitly as reference-only to prevent a future session from threading them into the Pencil Test asset chain. Production checklist also updated in this commit to reflect Act 2 pre-production complete, Phase 6 ready-to-execute structure, and split Act 1 / Act 2 active-run pointers.

---

## 2026-05-02 — Add v3 Seedance prompts (conversation-style structured blocks)

**What changed:** Created `docs/2026-05-02-act2-seedance-prompts-v3-conversation-style.md` — a third pass at the 10 manual Seedance shots (W1, W2, W3, S0, T0, T2, TR, REV, PM, PB) restructured to mirror the prompt structure that produced strong results in `docs/Conversation-that-utilized-prompt-science-successfully.md` (the Veo 3.1 Street Fighter II idle-bounce / walk-cycle / neutral-jump conversation). Each v3 prompt now has four labeled structural elements v2 had quietly lost: (1) a **named genre anchor** ("Traditional 2D animation pencil test in the style of classic Disney rough animation") instead of v2's medium-only description; (2) a delimited **`CRITICAL STYLE REQUIREMENTS:`** bulleted block at the bottom with explicit per-bullet negatives ("no anti-aliasing on edges", "no digital gradients", "no clean digital typography"); (3) **`CAMERA:`** as its own labeled section — for static shots a single line, for moving shots (T0 push-in, PB pull-back) a dedicated paragraph naming the intended axis and listing axis-negatives on every other axis ("locked dolly on rails"); (4) a **`Duration: Xs.`** closer. Action arcs are also restructured — multi-verb compound sentences are split into discrete sentences so the model treats each beat as its own interpolation target. v3 lands at ~100–130 words per shot vs v2's 50–80; the conversation evidence shows the structure matters more than the word count. Doc preserves the v2 continuity rules block (clean-shaven W1–W3, stubble S0+, terracotta loaf companion, no stylus in Act 2), the fal.ai playground settings table, the workflow recommendation order, and a per-shot escalation ladder (re-run v3 → fall back to v2 → fall back to v1 → invoke v1 shot-list fallback strategies). Closes with a side-by-side W1 v2-vs-v3 comparison so future sessions can see the structural delta on one worked example.

**Why:** Sean reported that the v2 rewrites — while structurally cleaner than v1 — were producing underwhelming Seedance output during manual generation. Cross-referencing the recent Veo 3.1 conversation (which produced the project's best video output to date) surfaced that v2 had over-corrected toward prose minimalism and lost four structural patterns the conversation specifically credited for success: named genre anchoring (Veo locked onto "Street Fighter II" where "fighting game" alone was vague), delimited bullet-list guardrails (the conversation's Option B walk cycle was ~120 words and worked GREAT — proving the 50–80 word target was over-tightened), labeled `CAMERA:` paragraphs (the neutral-jump conversation's "locked vertical dolly" + axis-negatives format was what got camera tracking to actually track instead of drift), and the `Duration:` closer (acts as a structural closure signal even when the API parameter is set separately). v3 is filed as a new doc rather than overwriting v2 because v2 remains a valid fallback in the escalation ladder — if a v3 prompt drifts, the user has a known-acceptable v2 baseline to drop back to before invoking the v1 shot-list fallbacks (split, cross-fade, hard cut). v3 is the new recommended default; v2 stays as the safety net. Filename uses today's date and the descriptive suffix `-conversation-style` to make the lineage from the source conversation findable in a directory listing.

---

## 2026-05-02 — Add Act 1 Seedance-finishing planning kickoff prompt

**What changed:** Created `prompts/2026-05-02-act1-seedance-finishing-plan-kickoff.md` — a self-contained kickoff prompt to be pasted into a fresh Claude Code session in plan mode. The next session's job is to produce a written implementation plan (not execute it) that takes Act 1 from its current state — approved NB2 keyframes + ComfyUI in-betweens + an isolated Seedance test video (`runs/run_2026-04-04_174805/export/seedance-2.0-output/Act-1-Test-Seedance-2.0.mp4`, 6.04s/24fps/145 frames) — to a shipped final hero loop that integrates cleaned-up frames from the Seedance output via NB2 redraw. Prompt was engineered using the `prompt-engineering` skill: XML-tagged sections (`<role>`, `<must_read_first>`, `<task>`, `<deliverable_plan_structure>`, `<constraints>`, `<validation>`), six required-reading file references, an explicit `<plan>`-shaped output schema with a 42-frame inventory table, and a six-item self-check the planner runs before delivering.

**Why:** Sean realized while ramping up Act 2 that Act 1 was never actually shipped — the production checklist still has unchecked items under "Phase 4: Act 1 Compositing" (sprite fade F38–F41, pencil trail effect, layered export over P-32A background, ship to portfolio). Rather than start that planning cold next session, this prompt front-loads the context the planner needs (Phase B.5 philosophy "Seedance finds the motion, NB2 protects the aesthetic", stylus-right-hand constraint, identity lock to A-2, no destructive moves on existing approved frames, active-run pin to `runs/run_2026-04-04_174805`) and locks down the deliverable structure so the next session produces a reviewable plan instead of drifting into execution. Filename follows the existing `prompts/YYYY-MM-DD-*-kickoff.md` precedent set by `2026-04-27-seedance-execution-kickoff.md`.

---

## 2026-04-27 — Add v2 Seedance prompt rewrite using image-generator-prompt-science

**What changed:** Created `docs/2026-04-27-act2-seedance-prompts-v2-prompt-science.md` — a copy-paste-ready set of v2 Seedance prompts for manual generation in the fal.ai web playground. Each of the 10 Seedance shots (W1, W2, W3, S0, T0, T2, TR, REV, PM, PB) gets a rewrite that compresses the v1 prompt to 50–80 words by applying the video-model rules from `image-generator-prompt-science`: one **medium + style** sentence, an **action arc** in plain verbs, and one **guardrails + negatives** sentence. Drops the verbatim "Style Anchor Block", the per-shot "Smooth N-second interpolation" timing language, and redundant `"Maintain pencil line quality, graphite shading, paper grain, consistent line weight"` repetition. Each card preserves: anchor paths, duration (creative + API-clamped), continuity rules (clean-shaven W1–W3, stubble S0+, no stylus in hand, terracotta loaf companion), and a one-line "what was cut and why" note. Doc also includes an optional verbatim Style Preamble to prepend if a regenerated clip drifts, a per-shot escalation ladder (re-run → prepend preamble → fall back to v1 → invoke v1 shot-list fallback), and a recommended generation order (walking sequence → T2 → PM/TR → harder shots).

**Why:** The user is regenerating mixed-quality clips manually via fal.ai's web playground (Task 4 human gate found drift in the first batch). The v1 prompts were written before the first batch ran and lean on three patterns that video models specifically over-constrain on: verbatim style blocks the start/end frames already prove, layered "maintain pencil line quality" repetition that produces "etched" frames, and `"Smooth 4-second walking interpolation"` jargon that micromanages timing the duration parameter already controls. The v2 doc gives the user a tested-against-prompt-science alternative without forcing it — v1 stays as the safety net (referenced explicitly in the escalation ladder), and the optional Style Preamble lets them add the full anchor block back per-shot if Seedance drifts. Lives in `docs/` (not `prompts/act2/`) because it's an active operations doc, not a single-frame NB2 prompt; intentionally NOT linked from CLAUDE.md's source-of-truth table because it's a manual-route helper, not a shift in the canonical spec (which remains the v1 shot list).

---

## 2026-04-27 — Update Act 2 shot list with execution-discovered constraints

**What changed:** Added two sections to `docs/act2-seedance-shot-list.md`:
- New "Production Constraints" block (between Camera Discipline and Continuity Rules) capturing fal.ai API behaviors that surfaced during the first execution batch — 4s API minimum (affects T2/TR/PM duration clamping), Fast tier as locked default, 720p default resolution, `generate_audio: false`. Anyone regenerating manually via the fal.ai web UI now sees the 4s minimum without having to read the orchestrator code.
- New bullet under Continuity Rules calling out the **stylus rule reversal** vs Act 1: stylus is NOT in Sean's hand in Act 2; the pencil visible on the desk in `transition_pulled_in.png` and `pre_pulled_in.png` is an incidental desk prop. Prevents an Act 1-trained prompt-engineer from re-introducing the rule.

**Why:** The shot list was creatively complete but missed two production-relevant facts that emerged during the first execution pass — the 4s API floor (T2's first 3s submit was rejected and clamped) and the Act 2 stylus-prop framing. Both are creative-spec-relevant: anyone working from the shot list alone would have hit the API rejection and could plausibly have written prompts that put the stylus back in Sean's hand. The handoff doc captures these in execution context; the shot list now captures them in spec context.

---

## 2026-04-27 — Pause Task 4 human gate; create manual-generation handoff doc

**What changed:** Added `docs/2026-04-27-seedance-manual-handoff.md` capturing the paused state of the 12-task plan and a self-contained inventory for running Seedance manually outside the Python orchestrator: per-shot start/end anchor paths, verbatim prompts, durations (raw + API-clamped), seeds used in the first batch, fal.media cached URLs, holds/hard-cuts/assembly-order, drop-zone for winning MP4s on return, and a list of deferred code-fixes flagged by the spec/quality reviewers (sync path missing `fal_request_id`, partial meta on download failure, duplicate `seedance_submit` log events, `--skip` ID validation).

**Why:** The Task 4 batch ran successfully (10/10 MP4s generated) but the human-gate review found mixed quality across the 9 new clips. The user paused execution to redo failing shots manually via the fal.ai web UI rather than auto-retrying through the script, then plans to bring winning MP4s back so the controller can resume at Task 5 (frame extraction). The handoff doc keeps the runtime context (seeds, cached URLs, deferred fixes) findable without trawling the JSONL log.

---

## 2026-04-27 — Task 4: Add `--all` async batch mode to `seedance_generate.py` + run 9-shot batch

**What changed:** Replaced the `NotImplementedError` stub in `pipeline/seedance_generate.py` with a full async batch implementation. New code:

- `_API_MIN_DURATION = 4` moved to module level (shared constant for sync and async paths).
- `_build_arguments(shot, start_url, end_url, resolution)` — builds fal.ai API arguments dict with duration clamp; returns `(arguments, raw_duration, effective_duration)`.
- `_download_mp4(video_url, local_mp4, run_dir)` — download helper that raises `RuntimeError` instead of calling `sys.exit` (lets batch continue on failure).
- `_submit_one(shot, model_id, run_dir, tier, resolution, attempt, cache_path)` — uploads anchors, logs `seedance_submit` + `seedance_submit_async` events, calls `fal_client.submit()`, captures `handler.request_id`, returns in-flight job dict.
- `run_all_async(args)` — main batch orchestrator: resolves run dir, pre-flight skips (explicit `--skip` + defensive MP4-exists check), uploads all unique anchors with HIT/UPLOAD console feedback, submits all jobs in sequence, polls every 10s using `fal_client.status()` + `Queued/InProgress/Completed` type checks, downloads + writes meta JSON per completed job, logs `seedance_generated`/`seedance_failed` events, prints final summary with success list, failure list, wall-clock, cost estimate, cache entry count, and human gate instructions.
- `--skip` arg added to `build_parser()` with `action="append"` (repeatable: `--skip T2 --skip W1`).
- `--seed` guard in `main()`: rejected with clear error message in `--all` mode.

**Batch run result (2026-04-27, ~$9.12 at Fast tier 720p):**
- Command: `python3 pipeline/seedance_generate.py --all --skip T2 --tier fast --resolution 720p --run-dir runs/act2-seedance-2026-04-27`
- Submitted: W1, W2, W3, S0, T0, TR, REV, PM, PB (9 shots)
- Generated: all 9 — 0 failures
- Wall-clock: 2m 7s (all 9 jobs processed in parallel on fal.ai, first result at ~98s)
- Total cost: ~$9.12 (38s effective × $0.24/s fast tier; TR and PM clamped 3s→4s)
- Cache: 2 entries (T2 anchors) → 13 entries (all unique anchors across 9 shots uploaded)
- JSONL log: 30 lines (2 submit events × 9 shots + 9 seedance_generated events + 3 pre-existing T2 lines)
- Per-shot seeds: W1=1372653108, W2=2049001023, W3=1537961300, S0=268853034, T0=1934474032, TR=376898827, REV=76012933, PM=2104407469, PB=1936106111
- MP4 sizes: W1=2.51MB, W2=3.27MB, W3=3.04MB, S0=2.60MB, T0=3.46MB, TR=1.54MB, REV=2.63MB, PM=1.20MB, PB=4.52MB
- fal request IDs recorded in each meta JSON (not None this time — `submit()` exposes `handler.request_id`)
- **Human gate queued:** All 10 MP4s in `runs/act2-seedance-2026-04-27/seedance/` surfaced for visual review before Task 5 (frame extraction).

**Anomalies:** Cache landed at 13 entries (not 14 as the Task 1 spec estimated) — the spec counted `final_panorama_v3_a.png` twice (as PB end + FIN hold anchor), and T2's two anchors were already cached. 14 was an overcount; 13 unique paths is correct for T2 + the 9 new shots.

**Why:** Async batch via `fal_client.submit()` + 10s polling is the right approach for 9 independent shots. All 9 were processing in parallel on fal.ai (all showed IN_PROGRESS immediately after submit), which cut wall-clock from ~18 min sequential to 2m 7s. The `--skip` mechanism with defensive MP4-exists detection ensures re-runs and partial batches are safe. Capturing `handler.request_id` at submit time (not result time) means fal request IDs are in the log even if a download fails — the clip can be recovered manually via the logged URL.

---

## 2026-04-27 — Task 3: Build `pipeline/seedance_generate.py` + run T2 sync test shot

**What changed:** Created `pipeline/seedance_generate.py` — the Seedance orchestrator with sync `--shot <ID>` mode (Task 3) and a stubbed `--all` mode that raises `NotImplementedError` (Task 4 lands that). The script:

- Parses args with argparse (`--shotlist`, `--shot`, `--tier`, `--resolution`, `--attempt`, `--seed`, `--run-dir`).
- Loads `.env` and shot list via `seedance_lib` helpers.
- Resolves the shot by id from `shots[]`, failing with available ids listed if not found.
- Uploads/caches both anchor images to fal.ai via `upload_anchor` (JSON cache at `{run_dir}/anchor_urls.json`).
- Clamps duration to API minimum of 4s when the shotlist specifies < 4s (T2 is 3s; API rejects anything below 4). Logs a warning; the extra second is trimmed in assembly. Records both `duration_s` (requested) and `effective_duration_s` (sent to API) in the meta JSON.
- Calls `fal_client.subscribe(model_id, arguments={...})` — blocks until result lands.
- Downloads the MP4 via `urllib.request.urlretrieve` with fallback to `urlopen`.
- Writes `{run_dir}/seedance/{shot_id}_attempt_{NN}.meta.json` with full provenance (model_id, seed, request_id, urls, paths, sizes, timestamps, wall-clock).
- Logs `seedance_submit` and `seedance_generated` events to `audit/seedance_log.jsonl` via `log_event`.
- Prints a human-readable summary block to stdout.

**T2 test shot result (real money: ~$0.96 at 4s fast tier):**
- MP4: `runs/act2-seedance-2026-04-27/seedance/T2_attempt_01.mp4` — 1.37 MB.
- ffprobe duration: 4.04s (4s requested from API; assembly will trim to 3s).
- Seed: 96653238. fal_request_id: None (subscribe mode doesn't return one).
- Wall-clock: 118s. JSONL log: 3 events (2 submit + 1 generated — first submit was from the failed 3s attempt that surfaced the API minimum).
- **Human gate queued:** MP4 surfaced for visual review before proceeding to Task 4 batch.

**Why:** T2 (companion materializes in terminal) is the highest-leverage validation in the plan — locked camera, single new element, both anchors are gold-standard Round 3 fidelity. If it passes, the 9-shot batch (Task 4, ~$9) is authorized. If it fails, we surface before spending the batch budget. The API minimum duration discovery (4s not 3s) is a real finding: the shotlist spec for T2 (3s) and TR (3s) will generate 4s clips that get trimmed to their spec length in `seedance_assemble.sh`. Both are hard-cut shots, so the extra second is fine — it just means the materialization and pull-in animations may extend slightly before the cut.

**Note:** The T2 MP4 lives in `runs/` (gitignored). Only the script is committed.

---

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
