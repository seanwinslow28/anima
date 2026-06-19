# Field Report — Animatic phase v1: the placement seed (costed spike GO → $0 stub-green build, TDD)

**Date:** 2026-06-18
**Kickoff:** [`docs/2026-06-18-animatic-phase-kickoff.md`](../active/2026-06-18-animatic-phase-kickoff.md)
**Design of record:** [`docs/2026-06-18-animatic-phase-design.md`](../active/2026-06-18-animatic-phase-design.md)
**Spike report:** [`docs/anima-test-runs/2026-06-18-animatic-spike-field-report.md`](2026-06-18-animatic-spike-field-report.md)
**Spend:** **~$1.3** Gemini-metered (15 spike calls + 4 trail-off-fix calls; subscription untouched, `ANTHROPIC_API_KEY` absent). The stage build was **$0 stub-green**.
**Branch:** `animatic-phase-v1` off `main` `71ad992` (isolated worktree) — 9 commits, each revertible.
**Tests:** `tests/` **665 → 685** (+20), 0 regressions; `pipeline/tests/` 10 green; both md5 guards intact.

---

## What this was

Built **TOP-1, the Animatic phase** — the keystone idea from the original architecture never built, and the one belief PHILOSOPHY calls non-negotiable (*the human owns timing*). v1 is the **placement seed**: a human-authored rough that pins where characters stand, which way they face, their scale, and the leg count *before* a frame is drawn, plus the timing (holds) that drives the loop's pacing. The need was re-derived by the 2026-06-18 validation run (wrong-shoulder mascot, inconsistent scale, 2↔4 legs) — *"the image model cannot reliably tell left from right, and it guesses placement from prose."*

The work ran in two phases, **the first gating the second**, exactly as the kickoff demanded:

- **Phase A — a costed spike** (the kickflip, ~$1.3) proved the load-bearing bet before a line of stage code: a hand-drawn placement rough makes NB2 put Sean into poses far outside his sitting register while identity holds and the role-tag clause quarantines the rough's look. **Sean ruled GO.**
- **Phase B — the $0 stub-green, TDD build** of the opt-in ANIMATIC stage: an `animatic_ref` schema field, the reference + role-tag wiring, the stage + its `--approve-animatic` ingest gate, the manifest block + deferred T3 seam, the holds→ASSEMBLE consumer, and docs.

The headline deliverable is a real, opt-in pipeline stage proven end-to-end with no key — plus a costed spike that turned the central bet from a hope into evidence (and caught a real prompt defect along the way).

---

## Failures & corrections (the part worth reading)

The doctrine's *"verify against the tree, never trust a label — including this kickoff"* earned its keep repeatedly. Each is recorded because that's why the doctrine exists.

### #1 — The kickoff contradicted itself on where `animatic_ref` lives

Kickoff Step 3 says `resolve_references` reads `shot.animatic_ref` (a board field). Step 4 says the ingest writes the ref "into run-state (the locked `shots.yaml` is never mutated)." Those can't both be literally true: a `Shot` loaded from the unmutated board carries no ref. Surfaced to Sean in planning; resolved **run-state primary** — `animatic_ref_for(shot, state)` reads `state["animatic"]["refs"]` first, falling back to the optional `Shot.animatic_ref` for an inline-authored board. The board is never mutated (honors the design lock), the schema field still exists, and both authoring paths work. A build that "followed Step 3 literally" would have produced a stage whose ingest writes a ref that generation never reads.

### #2 — `enter_generate` would have silently clobbered the holds override

`enter_generate` unconditionally reseeds `state["holds"]` from the board on every entry. Since the animatic gate routes *through* `enter_generate`, the sidecar holds the ingest had just written would have been overwritten — the timing half would have silently done nothing. Caught by tracing the call path before writing the gate (not by a failing test — by reading). Fixed with a one-line **overlay** (`state["holds"].update(animatic_holds)`), back-compat-safe because an empty/absent override leaves the board holds byte-identical. This is the kind of bug a green test suite hides: every existing test has no animatic holds, so they'd all stay green while the feature quietly failed.

### #3 — The spike corpus, the design/kickoff docs, and ROADMAP were all UNTRACKED

A `git ls-files` at §0 found **zero** tracked files under `images/anima-frames-test/`, and the design doc, kickoff, post-mortem, and ROADMAP all untracked. A fresh worktree off `origin/main` would have contained **none of them** — the spike would have had no corpus, and Step 7's "update ROADMAP" would have edited a file that isn't on main. Surfaced to Sean (decision: commit prep first). Landed a "Track Animatic prep docs + spike corpus + ROADMAP" commit on `main` (matching the established `a287ef2`/`99dc389` pattern), *then* branched the worktree — which then had everything. The `.env` (gitignored, not shared across worktrees) was copied in so `nb_pro_runner`'s `_PROJECT_ROOT/.env` resolved and the spike didn't silently stub.

### #4 — Sean's eye caught a real defect the metric would have passed: the trail-off

After ruling GO, Sean noticed both colored and silhouette outputs "start off great but trail off at the end of the run." At full res the cause was unambiguous and it was **a prompt gap, not a model limit**: "warm pencil-test register" cues the model toward real *animation production sheets*, so later/action frames sprouted hallucinated label text ("KICKFLIP APEX / CLEAN SKETCH / POSE B", frame numbers), hole-punch marks, and a drift from finished shading toward loose line-rough. The spike prompt had no negative against any of it. A cheap before/after (4 calls, ~$0.28) confirmed a strengthened no-text/no-production-artifact + finished-frame negative clears the text and the sketch-looseness reliably (residual: hole-punches greatly reduced but can persist faintly). That negative is now baked into the stage's role-tag clause. **Engine truth caught what an automated check would not** — exactly the PHILOSOPHY claim, demonstrated.

### #5 — A silhouette generator that "worked" was numerically broken (int16 overflow)

Sean asked, before the build, to extend the silhouette test from the 2 A/B keys to all six — so four silhouettes had to be made from the colored roughs (no ImageMagick on the box; built in PIL/numpy). The first pass color-keyed the uniform pink ground correctly *by luck*: `(a - BG)` in `int16` overflowed on the squared distance (`254² > 32767`), so `dist` was NaN-poisoned — yet the figure pixels still came out black because NaN comparisons fall to the "not background" branch. The output looked right; the math was wrong. Caught the `RuntimeWarning`, recast to `float32`, regenerated cleanly. A silent NaN that produces a plausible image is the worst kind — only the warning gave it away.

### #6 — A test-count assertion from memory was wrong (+19/684, actually +20/685)

While writing the CHANGELOG I wrote "+19 contract tests (665 → 684)" before the final suite run. The runner printed **685** (+20). Corrected in the CHANGELOG and both ROADMAP spots before committing. The trustworthy number is the one the runner just printed — the same lesson the Bea report logged, re-confirmed.

---

## What we got right (and why it held)

- **The spike genuinely gated the build.** No stage code was written until Sean eyed the output and ruled GO. The corpus was *harder* than the real use case (a competing character on a pink ground, six poses outside Sean's register), so a pass is strong evidence, and the "colored ≈ silhouette" finding lowered the design's #1 risk (authoring effort) as a bonus.
- **TDD with small revertible commits.** Six build commits, each red→green with its own targeted suite run, schema-first (the back-compat hinge locked before anything depended on it). RED was verified for the right reason each time (e.g. the `frame_prompt` tests failed on a missing symbol, the ingest tests on a missing module).
- **Back-compat as a hard, *proven* gate, not a hope.** A no-animatic run's ref list, prompt, and holds are byte-identical to today — asserted directly (`test_resolve_references_no_animatic_ref_byte_identical`, `test_frame_prompt_byte_identical_without_animatic_ref`, `test_authoring_without_animatic_skips_stage_to_generate`), not assumed. The back-compat brief still goes PLAN→GENERATE and never enters ANIMATIC.
- **The deferred T3 gate is honest.** Seam declared in the manifest, a clearly-marked no-op hook point in `animatic_stage.py`, promotion trigger recorded (wire when timing feeds Motion). Cosmetic-honest: the gate is *not* secretly half-wired.
- **The stage is human-authored — no LLM call.** Unlike the storyboard gate it mirrors, the animatic stage runs zero model calls; the deterministic `ingest_animatic` is the whole "intelligence." That keeps it cheap, fast, and fully testable.

---

## What we learned

1. **The most dangerous plan errors are the plausible ones.** The `animatic_ref` read-path contradiction (#1) and the holds clobber (#2) both read fine on the page and would both have produced a stage that *looks* built but silently does nothing for the feature it exists to deliver. Tracing the call path beats trusting the prose.
2. **A green suite hides feature-inert bugs.** The holds clobber (#2) would have left every test green — because no existing test exercises animatic holds. New behavior needs new assertions on the *new* path, not just "the old tests still pass."
3. **The human eye is a real gate, not a formality.** Sean's trail-off catch (#4) found a defect that contact-sheet inspection and any pixel metric would have passed — the outputs were "good images," just decorated with production-sheet cruft. The fix improves every future pencil-register generation, not just animatic.
4. **A silent NaN is worse than a crash (#5).** Code that produces a plausible artifact while being numerically broken is the hardest failure to catch; treat warnings as errors when the output is "judged by eye."
5. **Counts and corpus claims are not free (#3, #6).** Both the kickoff (untracked corpus) and my own draft (test count) carried assertions the tree/runner contradicted. Don't assert what you can run.

---

## How to proceed

1. **The costed end-to-end run is the one open DoD item (#6).** The build is stub-green complete, but the real proof is Sean drawing actual placement roughs for a real loop and running `--animatic` end to end — does the loop's placement hold where the 06-18 run drifted? That run also tests the design's original #1 risk (*will Sean actually draw these every run?*), which the turnkey spike corpus deliberately did not.
2. **The full 18-frame kickflip is a proven-bet follow-on + museum piece.** The spike ran six keys; the full sequence ("Sean lands a kickflip, generated from his own roughs") is a publishable walkthrough once the costed loop run lands.
3. **Consider growing Bea's base register negative.** The trail-off fix lives in the *animatic* role-tag clause; Bea's per-shot register negative ([`storyboard_artist.py`](../../pipeline/agents/storyboard_artist.py)) still only covers text/labels, not production-sheet artifacts or sketch-looseness. Extending it would help non-animatic frames too — but it's out of this phase's scope (touches Bea's emit + the Spark equivalence guard) and should be its own slice.
4. **Promote the `post_animatic` T3 gate when Motion is orchestrated.** The seam and hook point are in place; the trigger is a real Seedance burn to protect. Not before.
5. **Anti-drift: do not open Tier 2 yet.** Per the ROADMAP contract, Current Focus stays on Animatic until DoD #6 (the costed run) closes. Tier-2 Em calibration is next, not now.

---

## Done criteria — checked

- [x] **Spike:** field report written; Sean's **GO** recorded (+ silhouette-recommended + trail-off fixed).
- [x] `python -m pytest tests/` → **685 passed** (665 + 20), 0 regressions; `pipeline/tests/` 10 passed.
- [x] `test_spark_shots_equivalence.py` + `test_run_shots.py` + `test_run_generate_stage.py` green.
- [x] **Back-compat proven:** a no-animatic run's reference stack + prompt + holds are byte-identical to today (asserted, not assumed); the PLAN→GENERATE fork still bypasses ANIMATIC.
- [x] The opt-in ANIMATIC stage pauses, ingests roughs + holds deterministically, populates `animatic_ref` without mutating the locked board, and advances to GENERATE — proven stub-green.
- [x] `animatic_ref` rides last + role-tagged into generation; holds drive ASSEMBLE; both captured under `runs/<id>/animatic/`.
- [x] `post_animatic` T3 gate consciously deferred — seam declared, hook point placed, trigger recorded; council NOT wired.
- [x] Both md5 guards intact (`2af75906…` / `945af824…`); nothing under `evals/vision_critic/`; shared voice unchanged.
- [x] CHANGELOG.md + CLAUDE.md + ROADMAP + design-doc DoD updated. Squash PR off the isolated worktree (next); clean teardown to follow merge.
- [ ] **A costed run exercising the stage end-to-end (DoD #6)** — the real proof; deferred follow-on (needs Sean's roughs for a real loop).
