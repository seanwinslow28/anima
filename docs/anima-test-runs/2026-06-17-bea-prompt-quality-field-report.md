# Field Report — Tier 1 Slice A: Bea prompt quality + reference hygiene ($0 stub-green, TDD)

**Date:** 2026-06-17
**Kickoff:** [`docs/2026-06-17-bea-prompt-quality-kickoff.md`](../COMPLETED/bea/2026-06-17-bea-prompt-quality-kickoff.md)
**Plan of record:** [`docs/2026-06-17-tier1-fixes-build-plan.md`](../COMPLETED/orchestrator/2026-06-17-tier1-fixes-build-plan.md) (Slice A)
**Why (the evidence):** [`docs/anima-test-runs/2026-06-17-spark-authored-costed-run-post-mortem.md`](2026-06-17-spark-authored-costed-run-post-mortem.md) §3 (Findings 2, 3, 6)
**Spend:** $0 (stub-green throughout; the real Bea authoring path is exercised by Sean's next live run, not here)
**Branch / PR:** `tier1-slice-a-bea-prompt-quality` off `origin/main` `a655657` (#57) → [PR #58](https://github.com/seanwinslow28/anima/pull/58); four TDD commits, each revertible alone

---

## What this was

A targeted fix of the three prompt-authoring defects the **first live costed run** ("The Spark, Shared" — Sean + the mascot, a 5-keyframe pencil-test loop) surfaced. All three are in **Bea's storyboard authoring**, all fixable in her persona context + the reference assets with **no orchestrator code**:

- **F2** — Bea wrote rich literary prompts for *every* frame; frames 2–5 are NB2 *edits* off the chained prior frame, where verbose prose competes with the reference and drifts identity. Sean had to curate all four down to `ONLY CHANGE:` deltas — the exact "revision count" cost the run was meant to watch, run high.
- **F3** — the loop-return frame (F5) asked for a multi-step transition; the fix that worked was re-authoring it as "composition identical to frame 1."
- **F6** — the `A-7` production label on the pairing reference bled into every frame, because the register block had no no-text negative.

The slice landed as scoped, plus one tree-verified expansion (below). **5 new contract tests (655 → 658 in `tests/`) + 2 new eval cases (4 → 6); zero regressions.** No live model spend — the stub path + the eval lint prove the behavior credential-free; the real Bea (Sonnet) authoring is validated by Sean's next run.

---

## Failures & corrections (the part worth reading)

There were no runtime failures. As in the Bea build, the doctrine's "verify against the tree, never trust a label — *including this kickoff*" earned its keep — most consequentially on the reference assets.

### #1 — The kickoff assumed the anchors were label-free. They aren't — both carry production labels.

The kickoff scoped the asset work to **one** file (`sean-with-claude-mascot.png`) and its acceptance said "re-check the sean/mascot anchors carry no visible label either" — phrased as a confirmation it expected to pass. Opening the actual anchors disproved it: **`characters/sean-anchor/anchor.png` carries a circled `(A-2)`** top-left and **`characters/claude-mascot/anchor.png` carries `C-B`**. These are not incidental — both anchors are injected as **image 1 / image 2 on every generated frame** (the identity references), so they are a *larger* per-frame text-bleed surface than the A-7 pairing image (image 3) the post-mortem happened to notice.

**Resolution:** surfaced the finding to Sean with the tradeoff (cleaning two locked-Bible identity assets, beyond the kickoff's single-asset scope, vs. relying on the new no-text negative alone given the post-mortem only *observed* A-7 bleeding). Sean chose to clean all three. First confirmed it was **byte-safe**: no test or criteria lock asserts the anchor *image* bytes — the `acceptance_criteria.json` `locked: true` locks the **IR rule graph**, not the PNG; tests reference only the path string and write dummy PNGs in tmp fixtures. Patched all three with grain-matched clean-paper patches sampled from the same vertical band (dims preserved, figures byte-untouched, natural paper specks kept), archived each labeled original verbatim as `*.labeled-original.png`, and recorded the crop in both `source-refs/notes.md`.

**Why it matters:** the kickoff's own acceptance criterion ("no anchor carries a visible label") was *false on arrival* and would have been silently checked off by a build that trusted the prose. The biggest bleed source was the one the kickoff assumed was clean.

### #2 — The patch under-shot the A-7 circle on the first pass; pixel-scanning, not eyeballing, closed it

The first A-7 patch box was sized from a quick visual estimate and clipped the lower-left of the circled label, leaving a faint `(` paren stroke. The fix wasn't a bigger guess — it was to **scan the region for sub-threshold ink** (`numpy`, luminance < 175), separate the label pixels from the natural paper specks (kept) and the figure edge (the mascot starts ~x485), and size the patch to the measured bbox. Final scan: **0 residual ink** in every label box, confirmed both by pixel count and by re-reading the cropped images.

**Lesson:** "looks clean" at thumbnail scale is not "is clean." For an asset whose whole point is that NB2 *won't* find text on it, the acceptance evidence is a pixel scan plus a zoomed read, not a glance.

### #3 — The "update the eval fixture register tails" plan step was unnecessary, and acting on it would have been wrong

The plan (step 2) flagged that adding the no-text negative to `_REGISTER_CLAUSE` might require updating the eval's positive ground-truth fixture and the shipped board to match. Verifying the actual assertions killed that step: `test_spark_shots_equivalence.py` pins the shipped `briefs/2026-06-10-spark-shared/shots.yaml` against **`scripts/spark_frame.py`** (both frozen historical artifacts), **not** against `_REGISTER_CLAUSE`; and the eval positive fixture is a documented derivative of that frozen board, validated only for *structure* (coverage/conflict), never for register-tail equality. So `_REGISTER_CLAUSE` is purely the **forward-emit** constant — changing it touches what Bea emits next, and leaves every historical artifact correctly unchanged. Editing the frozen board's tails to "match" would have broken the equivalence test and falsified the board's provenance.

**Lesson:** before propagating a constant's change to "everything that mentions it," confirm *what actually asserts equality*. Here, nothing did — the right move was the smaller one.

### #4 — Each Edit needed a fresh `Read` of the **worktree** copy

A mechanical but repeated friction: I'd read several files in the main checkout during planning, but all edits happen in the isolated worktree (`/private/tmp/…`), a different path. The Edit tool (correctly) refused until each worktree file was read in-session. No harm — just a reminder that the worktree is a distinct tree and the read-before-edit discipline is per-path, which is exactly the isolation the fleet-ops protocol wants.

---

## What we got right (and why it held)

- **TDD red→green, small revertible commits.** Three behavioral tests written first (no-text negative in the constant; the prompt carries the establishing/edit + loop-return + no-text rules; the stub emits frame-1-full / frame-2+-`ONLY CHANGE:`) — confirmed red, then implemented to green. Four commits: context+stub, asset cleaning, eval lint, docs.
- **The stub became a faithful demonstrator, not just a placeholder.** Per Sean's call, `_make_bea_stub` now emits the real establishing-vs-edit shape, so a `--stub` run *shows* the discipline at $0 — and the eval lint can check actual stub output, not only hand-authored fixtures. This is the "$0 stub-green" ethos doing real work.
- **The lint is a warning, deterministic, and eval-side only.** `edit_frame_form_lint` mirrors Sam's `default_prop_lint`: it flags a non-establishing frame written as a full re-description and accepts the terse `ONLY CHANGE:` / loop-return form. It is **never** wired into production `storyboard_validate` — the composition/taste call stays Sean's at the curation gate. Both new cases are green deterministic catches.
- **The two standing guards never moved.** Em verdict-baseline `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` md5 `2af75906502f1caf8857e18828ceb2e4` and the shared `sean-screenwriting-voice.md` md5 `945af824fa53b948a18ac6bf206d67ef` were captured at §0 and re-checked at the end — byte-identical. The whole slice changed `bea-storyboard-context.md`, never the shared voice file; `git diff --stat origin/main -- evals/vision_critic/` is empty.

---

## What we learned

1. **The most dangerous line in a kickoff is the assumption stated as a fact.** "Re-check the anchors carry no visible label" read as a formality; it was false, and the asset it assumed clean was the primary bleed surface. Re-deriving from the actual files — not the prose — is the whole job.
2. **Image hygiene needs the same evidence discipline as code.** A label is "removed" when a pixel scan says zero ink in the box and a zoomed read agrees — not when the thumbnail looks fine. Measure the bbox; don't guess it.
3. **A constant's blast radius is whatever *asserts* it, not whatever *mentions* it.** `_REGISTER_CLAUSE` is grep-visible in the shipped board, the eval fixture, and `spark_frame.py` — but only the forward-emit path depends on its value. Confirming the assertion graph turned a multi-file edit into a one-line change and kept the frozen artifacts honest.
4. **Prompt discipline mitigates F3; it does not close it.** Authoring the loop-return as "composition identical to frame 1" is the right *prompt*, but `generate_stage` still feeds frame 5 the approved frame 4 (the "delight" mascot) as its chain reference, not frame 1 (the loop anchor). The reference pull is reduced, not removed, until the Slice B chaining change lands. This report flags it so the next run doesn't read the curation drop as a full fix.

---

## How to proceed

1. **Slice B (eye-gate ergonomics) is the next kickoff** — the orchestrator-UX change in `generate_stage` + `run.py` that stops the human-in-loop retry path fighting the user and surfaces the patch Em already proposes (the seam that later becomes propose→apply, Tier 2). The loop-return **chaining** fix (frame N's loop-return should chain off frame 1, not frame N-1) belongs there, alongside the F3 prompt discipline shipped here.
2. **The real proof is Sean's next live run, not this slice.** Everything here is structural ($0): the stub emits the form, the lint checks it, the labels are gone. Whether Bea (Sonnet) *actually* writes terse `ONLY CHANGE:` deltas and whether the cleaned references stop the bleed is confirmed only by the next costed authoring run. The expected signal: far fewer hand-edits at the curation gate, and no `A-2`/`A-7`/`C-B` text in the generated frames.
3. **The Em calibration campaign (Tier 2, the autonomy core) is planned in Cowork after Tier 1 lands** — untouched here by design (`evals/vision_critic/` is byte-identical).

---

## Done criteria — checked

- [x] `bea-storyboard-context.md` carries the establishing-vs-edit rule, the loop-return-as-"match frame 1" rule, and the no-text negative in the register block.
- [x] `sean-with-claude-mascot.png` is label-free (visual + pixel-scan confirm); **no anchor carries a visible label** — `(A-2)` and `C-B` also cleaned (Sean-approved scope expansion); labeled originals archived `*.labeled-original.png`; figures byte-untouched; criteria locks intact.
- [x] The eval lint flags a full re-description on a non-establishing frame and accepts the terse editing form — proven by `edit-form-accepted` (green) + `full-redescription-on-edit-frame` (green).
- [x] `python -m pytest tests/` → **658 passed** (655 + 3 new), 0 regressions; `test_spark_shots_equivalence.py` + `test_run_shots.py` green (back-compat proof). `pipeline/tests/` → 10 passed. `evals/storyboard_artist/runner.py` → 6 passed.
- [x] Both md5 guards intact: Em baseline `2af75906502f1caf8857e18828ceb2e4`; shared voice `945af824fa53b948a18ac6bf206d67ef`. Nothing under `evals/vision_critic/` changed (`git diff --stat origin/main` empty there).
- [x] CHANGELOG.md + CLAUDE.md (Bea row) updated; both md5 guards re-asserted in the entry.
- [x] One squash PR ([#58](https://github.com/seanwinslow28/anima/pull/58)) off the isolated worktree; clean teardown to follow merge.
