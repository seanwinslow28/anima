# Field Report — Run Orchestrator: Phase 3 wiring (the STORYBOARD slice) ($0 stub-green, TDD)

**Date:** 2026-06-16
**Kickoff:** [`docs/2026-06-15-orchestrator-storyboard-wiring-kickoff.md`](../2026-06-15-orchestrator-storyboard-wiring-kickoff.md)
**Plan of record:** [`docs/2026-06-15-orchestrator-storyboard-wiring-build-plan.md`](../2026-06-15-orchestrator-storyboard-wiring-build-plan.md)
**Spend:** $0 (stub-green throughout; running Sam (Opus) + Bea (Sonnet) live is the deferred costed run, never invoked in CI or this session)
**Branch / PR:** `worktree-phase3-storyboard-wiring` off `origin/main` `b51440f` (#54) → [PR #55](https://github.com/seanwinslow28/anima/pull/55); six commits, each revertible alone

---

## What this was

The deliberate **third Phase-3 slice**: Sam (#52) and Bea (#54) shipped standalone, outside the run orchestrator. This wires them in so `python -m pipeline.run --brief <dir>` drives **Maya → Sam → Bea → human-curate → Flo/Em → assemble** as one resumable program, stopping at four human gates (plan, script, storyboard, per-frame eye). The hand-authored `shots.yaml` path stays **byte-unchanged** — a brief that already carries a board auto-detects into the back-compat `PLAN → GENERATE` flow. No live model spend — the headline deliverable is the whole authoring chain walking `PLAN → SCRIPT → STORYBOARD → GENERATE → … → DONE` with **no key**, via Sam/Bea's stub fallbacks under `ANIMA_FORCE_STUB`. Not a costed run; the post-mortem below is about *build-time* failures and corrections, not generation quality.

The slice landed exactly as scoped: the conditional stage graph (`state.py`), the `enter_generate` refactor (`generate_stage.py`), two new gated stages (`script_stage.py`, `storyboard_stage.py`), the `approve_plan_gate` branch, the `run.py` `_start` auto-detect + slug rule + two new resume actions, the hermetic `mk_project` extension, the wiring + curation tests, and docs. **11 new contract tests (636 → 647); zero regressions; `pipeline/tests/` 10 green.**

---

## Failures & corrections (the part worth reading)

There was one real implementation seam (a circular import) and one operational slip (editing the wrong checkout). The rest are the planning-doc corrections the doctrine predicts — "verify against the tree, never trust a label, *including this kickoff and the plan*" earned its keep again.

### #1 — A circular import the plan didn't see: `plan_stage → script_stage → storyboard_stage → plan_stage`

The natural module shape — `approve_plan_gate` hands off to `script_stage.run_script_stage`, which on approve hands off to `storyboard_stage.run_storyboard_stage`, which (at its curation gate) needs `plan_stage.wire_brief_criteria` to rebuild the criteria bundle — closes a three-module import cycle. With all three imports at module top, importing `plan_stage` (which `run.py` does first) deadlocks: `plan_stage` → `script_stage` → `storyboard_stage` → back to a half-initialized `plan_stage`.

**Resolution:** lazy-import `wire_brief_criteria` *inside* `approve_storyboard_gate`, the exact pattern `cli/storyboard.py` already uses for its own validator imports. That breaks the back-edge (storyboard_stage no longer imports plan_stage at module load) while keeping the forward chain at the top where it reads cleanly. The IDE flagged the cycle the instant the top-level import was written; it never reached a test run.

**Why it matters:** the plan's File Map listed the modules and their call relationships but not their *import* relationships. The call graph is a DAG (plan → script → storyboard → generate); the import graph wasn't, because the storyboard gate reuses a plan-stage helper. A faithful "import what you call at the top" build would have crashed on first import.

### #2 — The plan's `enter_generate` extraction boundary was too narrow; gates run as separate processes

The kickoff described the refactor as extracting "the load-shots → … → fan-frame-1 block" and cited "lines 136-148" of `approve_plan_gate`. But the block that *matters* starts earlier: `wire_brief_criteria` + `load_all_criteria` (the bundle) at lines 111-112, then `load_shots` + the anchor/extra-ref existence validation at 115-134, *then* the seed/advance/fan at 136-148. The first integrated-run lesson (and Slice 2.1's design) is that **each gate is a separate `python -m pipeline.run` process** — so the storyboard gate cannot inherit the plan gate's in-memory `criteria_sources.brief_file` patch or its built bundle. It must re-wire and rebuild.

**Resolution:** `enter_generate(state, manifest, bundle, run_dir)` owns load_shots → validate → seed → advance → fan; the **caller** does criteria locking (plan-level, once) + `wire_brief_criteria` + `load_all_criteria`. The plan gate (back-compat) wires+builds then calls it; the storyboard gate re-wires+rebuilds (its own process) then calls it. I flagged this exact correction during planning — it held under implementation and is the reason the authoring path produces a correctly-merged bundle at GENERATE.

**Why it matters:** had `enter_generate` been the narrow 136-148 slice with the bundle passed through from a stale caller, the authoring run would have entered GENERATE with an unwired manifest — Em's criteria bundle missing the brief's `AC.*` rules, silently.

### #3 — The build plan named an on-disk fixture that doesn't match the test convention

The build plan's File Map called for a new `tests/fixtures/briefs/authoring-min/` directory, and the acceptance criteria cited `--brief tests/fixtures/briefs/authoring-min --stub` literally. Verifying against the tree: **there is no `tests/fixtures/briefs/` directory** — every `test_run_*` test builds its brief on-the-fly in `tmp_path` via the hermetic `mk_project` (`tests/orch_fixtures.py`). Worse, **Sam's stub hardcodes its beat cast as `["sean", "claude-mascot"]`** (`scriptwriter._stub_sam_text`), so an authoring stub-walk needs a manifest whose IR namespaces are exactly those — but `mk_project`'s default cast is `al`/`be`, which would fail `load_beats`' namespace validation.

**Resolution:** surfaced as the one genuine design fork at planning time; Sean chose **extend `mk_project` hermetically**. Added two knobs — `with_shots=False` (omit the board → the authoring brief shape) and `cast=` (override the folder-key/namespace pairs) — with defaults preserving the legacy alpha/beta + shots.yaml project byte-for-byte. The authoring test builds `sean-anchor`/`claude-mascot` Bibles matching Sam's stub. No on-disk fixture, consistent with the suite, fully offline.

**Why it matters:** Bea's stub is a closure over the real beat sheet (adapts to any beats), but Sam's stub is a fixed blob with hardcoded namespaces. The fixture had to satisfy Sam's constants, not just be "a brief without a board." A build that created the named fixture against the real repo manifest would have worked too, but coupled a unit test to committed Bibles; the hermetic route is the cleaner match.

### #4 — Operational slip: my first edits landed in the main checkout, not the worktree

The fleet-ops protocol mandates one isolated worktree; I created it (`EnterWorktree`) and the session cwd switched correctly. But my first `Read`/`Edit` calls used absolute paths into the **main checkout** (`/Users/.../anima/tests/...`) out of habit, so the Step-1 test edit landed there. The tell was unmistakable: the worktree's pytest reported "8 passed" when my 5 new tests should have run — they weren't in the file pytest collected. This also surfaced a stale `.git/index.lock` (0 bytes) in the shared `.git` when I went to revert.

**Resolution:** reverted the main checkout clean (`git restore`), removed the stale lock (verified no live git process first), and redirected every subsequent edit to the worktree path. Caught within one test run, before any commit.

**Lesson:** after `EnterWorktree`, the session cwd is the worktree but absolute paths don't follow it. Either use cwd-relative paths or paste the worktree prefix deliberately. The "wrong test count" anomaly is a cheap tripwire — a new RED test that reports the *old* green count means you edited the wrong tree.

### #5 — Self-introduced test-count drift, caught by running the suite

The kickoff's §0 expected "636+" and the build plan said "636 + new"; memory and CLAUDE.md carried 562 / 576 from earlier slices. Rather than trust any of them I captured the real baseline first — `python -m pytest tests/` → **636** (the kickoff number was right; the stale ones weren't). Every per-step count in the commits and docs is the number the runner printed (645 after steps 1-4, 647 after step 5), never asserted from memory.

**Lesson:** the only trustworthy count is the one the test runner just printed — and "the plan says 636" is not the same as "the suite reports 636." Capture the baseline; don't inherit it.

---

## What we got right (and why it held)

- **TDD with small revertible commits, the refactor net first.** Six commits, each red→green with its own targeted run before the full suite. The order mattered: graph (step 1) → `enter_generate` extraction *proven behavior-preserving by the existing `test_run_integration.py`* (step 2) → stages + wiring (steps 3-4) → curation gate (step 5) → docs (step 6). The back-compat integration test was the safety net under the refactor before anything new depended on it.
- **One shared GENERATE entry, so the two paths can't drift.** Both the plan gate and the storyboard gate reach `enter_generate`. There is exactly one place that loads the board, validates inputs, seeds frame state, and fans frame 1 — a future change to the GENERATE entry can't silently diverge between back-compat and authoring.
- **The curation gate reuses Bea's own validator, not a reimplementation.** `approve_storyboard_gate` calls `cli.storyboard.approve_storyboard`, which runs `load_shots` + `storyboard_validate` (the `beat.cast ⊆ shot.cast` rule from #54) against the *human-edited* file and refuses to lock a broken board. The orchestrator didn't reinvent the conflict check; it re-runs the standalone one on the curated artifact — exactly the kickoff's instruction.
- **Auto-detect keeps the hand-authored path sacred.** `needs_storyboard = not (brief has shots.yaml)` means the Spark brief and every existing run are byte-identical: `PLAN → GENERATE`, no Sam, no Bea. The agents draft only when there's no board yet. Phase 3 stays human-authored by design; the orchestrator never invents frame prompts.
- **The two standing guards never moved.** Em verdict-baseline `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` md5 `2af75906502f1caf8857e18828ceb2e4` and Sam's voice file `sean-screenwriting-voice.md` md5 `945af824fa53b948a18ac6bf206d67ef` were captured at §0 and re-checked at the end — both byte-identical. Nothing under `evals/vision_critic/` was touched.

---

## What we learned

1. **The plan's call graph is not its import graph.** The cleanest stage decomposition (plan → script → storyboard, each handing off to the next) produced a circular *import* because the last stage reuses a first-stage helper. Lazy imports at the reuse point are the standard break; the lesson is to check the import direction, not just the call direction, when modules hand off in a chain.
2. **"Separate process per gate" is the orchestrator's load-bearing invariant.** It dictated the `enter_generate` boundary (#2): anything in-memory the plan gate built is gone by the storyboard gate. Every gate must rebuild what it needs from durable state + disk. The refactor is correct only because the caller re-wires criteria each time.
3. **Verify the fixture convention, not just the code.** The plan named a fixture directory that doesn't exist in this suite (#3). Test infrastructure has conventions as load-bearing as production code; "add a fixture file" assumed a layout the tree doesn't use.
4. **cwd is not the same as your edit paths.** The worktree slip (#4) cost one test run to catch. After entering a worktree, absolute paths still point wherever you typed them — the discipline is cwd-relative paths or a deliberate worktree prefix, and the "wrong baseline count" tripwire catches it fast.
5. **Capture the baseline; don't inherit the number.** Three documents carried three different test counts (#5). The runner settled it in 50 seconds. Don't assert what you can run — including in the §0 pre-flight.

---

## How to proceed

1. **The fleet runs as one program now; the live authoring costed run is the next real step.** This slice proved the chain *structurally* — Sam's stub (fixed `sean`/`claude-mascot` blob) and Bea's stub (one-shot-per-beat closure) are not real model output. The deferred costed run should author a real `beats.json` from the Spark Studio Brief (Sam, Opus) → `script approve` → a real `shots.yaml` (Bea, Sonnet) → curate → `--approve-storyboard` → GENERATE, and confirm the **beat_id-linked board survives end to end** against live model output. That's the "prove `beat_id` against a real Bea draft" concern carried over from #54, now reachable through one command.
2. **Museum capture is the remaining orchestrator slice.** `pipeline/run.py` still has no museum hook (the docstring's "Slice 3"). With Phase 3 wired, a full authoring run now produces plan + script + board + frames + assembly evidence in one `run_dir` — the richest exhibit input yet. Wire the capture layer to walk a completed `run_state.json`.
3. **The hardening campaign items stay parked, unchanged by this slice.** Bea's composition pairwise-preference harness and the Sonnet/Gemini/Codex bake-off (Bea's ≈65%-confidence Sonnet assignment); Sam's by-ear voice harness. None are v1 blockers; all are post-merge campaign work.
4. **A pre-gate live smoke for Sam/Bea is a deferred-run decision, not a $0-slice one.** The plan gate smokes Opus before Maya; the script/storyboard gates currently rely on the post-hoc stub-marker scan (which blocks a silently-stubbed script/board in a non-stub run — the silent-stub trap caught). For the costed run, consider adding `smoke_live_opus`/`smoke_live_sonnet` at the script/storyboard gates as belt-and-suspenders, matching the standalone drivers. Out of scope here because this slice never goes live.

---

## Done criteria — checked

- [x] Authoring stub-walk (`--brief <authoring> --stub`) reaches **DONE** through both new gates, fully offline ($0) — proven by `tests/test_run_storyboard_wiring.py::test_authoring_stub_walk_plan_to_script_to_storyboard_to_done`.
- [x] `--brief <back-compat-with-shots> --stub` still goes `PLAN → GENERATE` (SCRIPT/STORYBOARD skipped); `test_run_integration.py` + the existing `test_run_*` suite green — the refactor changed no observable back-compat behavior.
- [x] The curation gate re-validates the human-edited `shots.yaml` and refuses both a coverage gap and a cast-conflict break (`beat.cast ⊆ shot.cast`) — proven by two tests; the run stays at STORYBOARD and the board is never locked.
- [x] `python -m pytest tests/` → **647 passed** (636 + 11), no regressions. `pipeline/tests/` → 10 passed. Credential-free (`ANTHROPIC_API_KEY` ABSENT throughout).
- [x] `new_state` records `needs_storyboard`; `mk_project`'s `with_shots`/`cast` knobs default byte-identical (legacy callers unchanged).
- [x] Em baseline md5 `2af75906502f1caf8857e18828ceb2e4` unchanged; nothing under `evals/vision_critic/` touched.
- [x] `sean-screenwriting-voice.md` md5 `945af824fa53b948a18ac6bf206d67ef` unchanged from §0.
- [x] CHANGELOG.md + CLAUDE.md updated (Phase-3-wired status, Key Commands, orchestration helpers, Sam/Bea rows). One squash-ready PR (#55) off the isolated worktree; clean teardown to follow merge.
