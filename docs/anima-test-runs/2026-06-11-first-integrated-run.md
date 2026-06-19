# Field Report — The First Integrated End-to-End Run: "The Spark, Shared"

**Date:** 2026-06-11 (kickoff written 2026-06-10: [`docs/2026-06-10-first-integrated-run-kickoff.md`](../COMPLETED/orchestrator/2026-06-10-first-integrated-run-kickoff.md))
**Branch:** `feature/first-integrated-run` (isolated worktree off `origin/main`)
**Billing:** subscription-absorbed (Maya, Em-escalation, T3 Sage/chairman) + ~$0.66 real (NB2 + Gemini critic)
**Verdict:** **SHIPS** — Sean's eye on the assembled loop. The fleet ran as one chain for the first time.

---

## What this was

The first time Maya → Flo → Em → T3 → Mo ran as a single chain on one piece. The deliverable
is a 6-keyframe two-character pencil-test micro-loop (Sean draws; the Claude mascot perched on his
shoulder notices, gets excited, delights, settles — looping back). **The piece is the proof; exercising
the integrated fleet was the point.** Per the kickoff: there is no `run` orchestrator — every node was
chained by hand, and **capturing every orchestration seam is half the value** (it scopes that future
orchestrator). That seam list is the heart of this report.

## The chain, end to end (what actually happened)

| Phase | Node | Result |
|-------|------|--------|
| 0 Plan | **Maya** (`PlannerNode`, live Opus 4.8 → Sonnet 4.6 → resolve) | 3 calls. Strong `plan.md` + 14-criterion `acceptance_criteria.json` + cost preview. Sonnet caught a real mis-tag (below). **Human gate → Sean approved.** |
| 5 Generate | **Flo** (`FloNode`) | Every frame routed `standard_keyframe → nb2` ($0.07, status=wired), 16:9 from manifest. Dispatched correctly on the **declarative inline path** every time. |
| 5 T1 | `audit.check_aspect_ratio` | HF01 **PASS** on all frames (1376×768, 0.78% dev). |
| 5 T2 | **Em** (`VisionCriticNode`, gemini-3.5-flash via API, criteria-text grounding ON) | Two passes/frame (`sean` + `claude-mascot`). Cited **real IR handles**, caught real defects, drove the retry ladder. Empty-cites invariant never tripped. |
| 8 Assemble | FFmpeg (direct recipe) | 6 keys on twos → GIF/WebM/MP4, clean F05→F01 close. |
| 8 T2 | **Em** phase_8 | Sean **pass 1.0** ("seamless... no sliding/jitter"); mascot **borderline** confirming "t5→t0 no visible jump" + flagging the intended peak grin. |
| Museum | **Mo** + T3 gate | Thin `_unclassified` exhibit (seam #14); T3 pre-publish gate (see below). |
| 9 QA | Sean | **Engine Truth: ships.** |

## Per-agent behavior

**Maya** — performed well. The **Sonnet adversarial pass earned its keep**: Maya's first draft folded
the piece's narrative premise (the mascot reacts while Sean stays heads-down) into a *single
aesthetic-tagged* criterion — which would not trip Em's Opus escalation. The resolution split it into
two **identity-critical** criteria (`sean-stays-absorbed` + `mascot-carries-reaction`). Maya also
**caught the cost-estimator phantom herself** in prose ("a Bible bake this run will not do, because both
Bibles are already locked"). Box-char contract held; clean markdown on disk.

**Flo** — the quiet success. Every dispatch resolved the route correctly (`nb2`, wired) and generated
through the same `invoke_image_edit`/`generate_frame` transport, 16:9 honored. Zero route surprises.
Flo-C's wiring is sound.

**Em** — strong corroborator at Gemini tier (the validated 0.97/1.00/0.00 baseline; no Opus escalation
needed). Cited **real `IR.*` handles** throughout (citation grounding from G6.1b working in production):
caught F02's stylus dual-wield (`IR.sean.prop.stylus-right-hand-always`), F03's angry brows then the
over-grin (`IR.claude-mascot.face.*`), the F04/F05 stylus-hand reads. **One real weakness:** Em's
*absolute* left/right stylus-hand verdict is **noisy in a screen-right profile** — it **passed F01** and
then **failed F02/F04/F05 on the identical near-hand-draws configuration**. CC01 continuity is better
judged frame-to-frame than per-frame-absolute (seam #10).

**Mo / Museum** — produced a thin, honest `_unclassified` exhibit (0 assets). The scraper has no rich
exhibit type for a keyframe-loop run and no `project_slug` classifies a fresh integrated piece, so the
**loop itself was not captured into the museum** (it lives in `runs/.../export/`). Seam #14.

**T3 council** — _(pre-publish gate result; see the T3 section at the end once the gate run lands.)_

## Engine Truth — the human overrode the critic three times (working as designed)

1. **F01** approved as-is despite my flag that the mascot read tucked-behind-the-neck.
2. **F02 attempt 1** chosen over Em's stylus-dual-wield `fail` — Sean's eye on the composition.
3. **F03 attempt 2** — the one Em flagged as identity-drift (open-mouthed grin violating
   `minimal-mouth-line`) — chosen by Sean as the **expressive PEAK** of a 6-frame cut, because the
   5-frame restrained cut had "very little reaction." The critic proposes; the human decides. This is
   the clearest demonstration of the doctrine in the whole run.

## Cost — actual vs estimate

| | Maya's Phase-5 estimate | Actual |
|---|---|---|
| | low $0.35 / median $0.93 / high $2.25 | **~$0.66** |

8 NB2 generations (F01×1, F02×2, F03×3, F04×1, F05×1) × $0.07 ≈ **$0.56** + ~16 Gemini critic calls
≈ **$0.10**. Right at the median band, well under the $5 ceiling. Subscription-absorbed: Maya's 3 calls,
the T3 Opus seats. **The estimator's headline ($5.75/$7.95/$18.45) was dominated by a phantom Phase-2
band** ($5.40–$16.20) for a Bible bake this run never did — seam #5.

## The seams (the scoping list for a `run` orchestrator)

Every place the chain needed hand-wiring. **This is the deliverable.**

1. **No `author_plan.py`** — Maya is a node, not a CLI. Built + committed `scripts/author_plan.py`
   (mirrors `author_bible.py`), with the silent-stub loud-fail Maya lacks (a smoke call + marker scan).
2. **`PlannerNode` 120s timeout — a real bug.** Live Opus-4.8 authoring (extended thinking + one large
   3-key JSON emission) runs **~350s/call**; the 120s default silently timed out into an empty-text
   `_parse_opus` crash. **Fixed:** env-tunable `MAYA_CALL_TIMEOUT_S` (default 1200s). Proven by a probe
   that completed at 349.8s with a real 19K-char plan.
3. **`PlannerNode` envelope parser — a real bug.** Opus 4.8 prefaces its JSON with persona prose
   ("Maya here — Pass 1 ...") *intermittently*; the anchored-fence-or-raw parser crashed at char 0.
   **Fixed:** string-literal-aware brace-balanced extraction tolerant of preamble/postamble + internal
   braces/backticks. +5 regression tests (all 19 planner tests green).
4. **Nested-SDK rate-limit contention.** Driving an Opus node (Maya, T3 Sage/chairman) via
   `claude-agent-sdk` from *inside* a live Opus Claude Code session adds **~285–390s of throttle latency
   before first output**. The single biggest "this is rough" finding for orchestration-from-a-session.
5. **`cost_estimator._phase_2_cost` double-counts locked Bibles.** It prices every generate-plate in a
   registered character's `plate_generation_plan.json` regardless of lock state, so an *animation_piece*
   run against already-locked Bibles shows ~$5.40 of phantom Phase-2 spend it will never pay. (Its own
   docstring says animation-piece runs "don't re-pay" — the code does.) Maya flagged it in prose; the
   estimator should skip locked Bibles. **Not fixed this run** (costed-path file, deserves a TDD fix).
6. **Em has no CLI** — only `VisionCriticNode`. Driven inline in `scripts/spark_frame.py`.
7. **Patch staging needs the DAG runner.** `stage_patches_hook` is a `post_run` hook; inline `run()`
   does not fire it. Called the hook by hand after each Em result.
8. **`ctx.criteria` is a `CriteriaBundle` object, not a path**, and **`criteria_sources.brief_file`
   never auto-wires from `brief.active_dir`** — hand-set after approval (built via `load_all_criteria`).
9. **Em is single-character, keyed on the IR namespace.** `query_by_character("sean")` → 31 rules;
   `"sean-anchor"` (the manifest/folder key) → **0**. A two-character frame needs two Em passes with the
   *namespace* ids (`sean`, `claude-mascot`), not the folder keys.
10. **Em's absolute stylus-hand (left/right) verdict is noisy in profile** (see Em above). CC01 wants a
    frame-to-frame continuity check, not per-frame-absolute.
11. **`character_id` means different things to different nodes.** Flo wants the manifest/folder key
    (`sean-anchor`, for `style_register`); Em wants the IR namespace (`sean`). The driver threads both.
12. **Gemini saves JPEG-as-`.png`.** The generated candidates are JPEG data with a `.png` extension;
    ffmpeg's PNG decoder rejects them (`Conversion failed!`). Re-encode via PIL before assembly.
13. **`assemble.sh` is hardcoded to the PT_A1 frame sequence** — won't see SPARK frames. Used the direct
    FFmpeg two-pass-palette recipe + a hand-staged on-twos `export/frames/` sequence.
14. **Museum has no exhibit type for a keyframe-loop run + no `project_slug`** for a fresh integrated
    piece → thin `_unclassified` exhibit, **0 assets copied** (the loop isn't captured). Needs a new
    exhibit kind + slug.
15. **Bash CWD is unreliable between calls** in this harness (foreground vs background; worktree vs main
    checkout). Every command needs an explicit `cd <worktree>` — a stray default-CWD run silently hit the
    main checkout's unfixed code once.
16. **The whole chain — and the human gate between every frame — is hand-wired.** No queue, no resume,
    no one-command run. Seven hand-built steps (plan driver, brief-file wire, env copy, per-frame driver,
    retry-note plumbing, peak-frame staging, assembly) the orchestrator would absorb.

## What a `run` orchestrator should absorb (synthesis)

A `python -m pipeline.run --brief <dir>` that: drives Maya with the right timeout + a parsed envelope +
a stub guard; stops at the human gate; wires `brief_file` + builds the bundle once; per frame runs
Flo → T1 → Em (multi-character) → stages patches → presents for the eye → retries with a correction
note; assembles (re-encoding JPEG-as-PNG, arbitrary key names, variable holds); and captures a real
loop exhibit to the museum. The estimator should skip locked Bibles. Em should get a frame-to-frame
continuity check for CC01.

## Artifacts

- Plan: [`briefs/2026-06-10-spark-shared/plan.md`](../../briefs/2026-06-10-spark-shared/plan.md) +
  `acceptance_criteria.json` (14 criteria, locked).
- Loop: `runs/2026-06-11-spark-shared-first-integrated/export/SS_L1_loop.{gif,mp4,webm}` +
  `SS_filmstrip_6.png`.
- Approved keys: `runs/.../approved/SS_F01..F05_key.png` + `SS_F03b_key.png` (the peak).
- Em verdict trail: `runs/.../em_verdicts.jsonl`. Maya raw evidence: `runs/.../maya_raw_pass1.txt`.
- Drivers (committed): `scripts/author_plan.py`, `scripts/spark_frame.py`.

## T3 pre-publish gate — stopped (and that is itself the finding)

All three peer CLIs were available (codex/Codie, gemini_api/Annie, Claude-SDK/Sage + chairman). The
gate was launched (`build_museum.py --t3-gate`) but **Sean stopped it after ~10+ minutes with no output**
— the council's **Opus chairman + Sage seats crawled under the same nested-SDK rate-limit contention as
seam #4**, made worse by concurrent main-loop Opus work (this report + the CHANGELOG). It was terminated
to avoid burning usage on a **thin 0-asset exhibit the council had nothing visual to review** anyway
(seam #14). Clean teardown: `TaskStop` reaped the process + its SDK children; orphan sweep confirmed no
gate processes survived.

**Takeaway:** the T3 council is **built + live-validated separately (2026-06-10 smoke — all three peers
fired live, chairman synthesized, fail→blocked / borderline→proceeded both proven)**. Re-running it as a
*nested* in-session gate over a thin exhibit added cost without signal. The future `run` orchestrator
should run the T3 gate **out of the interactive session** (uncontended Opus) and only over an exhibit
that actually carries the assembled loop — which requires fixing seam #14 first. Net: the gate is real,
the integration point is real, and the lesson is *where* to run it.
