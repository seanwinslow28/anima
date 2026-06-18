# Kickoff — Tier 1 Slice B: eye-gate ergonomics + loop-return chaining ($0 stub-green, TDD)

*Paste the block below into a fresh Claude Code session in the `anima` repo. Self-contained.
Plan of record: [`docs/2026-06-17-tier1-slice-b-build-plan.md`](2026-06-17-tier1-slice-b-build-plan.md).
Why: [`docs/anima-test-runs/2026-06-17-spark-authored-costed-run-post-mortem.md`](anima-test-runs/2026-06-17-spark-authored-costed-run-post-mortem.md) (F4/F5/F3) + the [Slice A field report](anima-test-runs/2026-06-17-bea-prompt-quality-field-report.md) lesson #4.*

---

You're shipping the **second and final Tier 1 slice** — two orchestrator fixes from the first live
run, both $0/stub-green. **B1 (ergonomics):** the eye gate throws away Em's grounded diagnosis — she
emits a `reasoning` paragraph and a staged proposed-patch, but the gate prints only `verdict + cites`,
so the human writes retry notes from scratch (and naming the defect *reinforces* it, since the note is
appended verbatim as `CORRECTION:`). Surface what Em already computed, and steer the note positive.
**B2 (loop-return chaining):** the loop-return frame still chains off the *prior* approved frame (the
delight mascot), not frame 1 — the Slice A prompt fix mitigated this but didn't close it. Add a
back-compat `chain_from` field so the closing frame chains off the loop anchor.

Read first: the build plan above; post-mortem F3/F4/F5; then `PHILOSOPHY.md`, `CLAUDE.md`. The code you
touch: `pipeline/orchestration/generate_stage.py` (eye-gate print + `resolve_references`),
`pipeline/orchestration/shots.py` (the `chain_from` field), `pipeline/run.py` (retry help),
`pipeline/agents/prompts/bea-storyboard-context.md` + `storyboard_artist.py` (Bea sets `chain_from`).

**Out of scope:** a `--apply-em-patch` flag (Tier 2 propose→apply — surface the patch here, don't apply
it); anything in Em / `evals/vision_critic/`; Tier 2 calibration. Don't touch the shared
`sean-screenwriting-voice.md`.

## Doctrine — non-negotiable

- **Verify against the tree, never trust a label — including this kickoff.** Confirm before editing:
  that `generate_stage.run_frame_fan`'s eye-gate print loop iterates in-memory `em_records` that
  **already carry `reasoning`** (currently unprinted) and that Em's proposed-patch is staged to
  `manifest.lock.yaml` by `stage_patches_hook` (fields: target/path/operation/value/rationale/
  cites_criteria — see `pipeline/cli/patches.py`); that `resolve_references` sets
  `prior = order[order.index(shot.id) - 1]` and that the dedup collapses `approved(first) +
  approved(prior)` so `chain_from: 1` yields `approved(1) + anchors` (F4 dropped); that `shots.py`'s
  `_FRAME_KEYS` is where `chain_from` slots in (same back-compat pattern as `beat_id`/`locked`).
  Cautionary tale from Slice A: the kickoff's "re-check the anchors are clean" was *false on arrival* —
  re-derive from the files, not the prose.
- **Two md5 guards, both must hold:** Em baseline
  `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`;
  shared voice `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`.
  Neither is touched here.
- **Back-compat is a hard gate.** `chain_from` is optional; `test_spark_shots_equivalence.py` +
  `test_run_shots.py` must stay green (the shipped Spark board has no `chain_from` and parses unchanged).
- **$0 — stub-green only.** No model spend; stubbed Em verdicts + the stub board prove both halves.
- **TDD red→green**, small revertible commits, in the build plan's order (B2 schema → B2 recipe → B1
  gate → B2 Bea wiring → docs).

## §0 — fleet-ops gates (before any edit)

```bash
cd <anima main checkout>
git fetch origin
git log --oneline -1 origin/main                        # expect 99dc389 (#59) or newer
git rev-list --left-right --count origin/main...HEAD    # expect 0 0
md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md  # 2af75906502f1caf8857e18828ceb2e4
md5sum pipeline/agents/prompts/sean-screenwriting-voice.md               # 945af824fa53b948a18ac6bf206d67ef
echo "${ANTHROPIC_API_KEY:-ABSENT}"                     # expect ABSENT
python -m pytest tests/ -q                              # expect green (658)
```

One isolated worktree off `origin/main`; ALL edits inside it. Single owner.

## Build order (TDD)

1. **B2 schema — `chain_from` in `shots.py` + `tests/test_run_shots.py`.** Optional per-frame
   `chain_from: int | None = None` in `Shot` + `_FRAME_KEYS`. Validate when set: int naming an
   **earlier** in-sheet frame (`chain_from < id`, exists). Red→green: a frame with valid `chain_from`
   round-trips; a `chain_from` ≥ id or absent-from-sheet rejects; absent → unchanged. **Then run
   `test_spark_shots_equivalence.py` + `test_run_shots.py` green** (back-compat proof).

2. **B2 recipe — `resolve_references` honors `chain_from` + `tests/test_run_generate_stage.py`.**
   `prior = shot.chain_from if shot.chain_from is not None else order[order.index(shot.id) - 1]`. Keep
   the existing approved-frames-exist guard. Test: a `chain_from: 1` frame's refs = `approved(1) +
   anchors` (no prior-frame ref); absent → prior-frame (unchanged).

3. **B1 eye-gate print + `tests`.** In `run_frame_fan`'s gate print, on `borderline`/`fail` also print
   Em's `reasoning` and her proposed-patch summary (target/value/rationale). Add the positive-framing
   steer to the printed retry hint + `run.py` `--retry-frame`/`--note` help. Test with a stubbed Em
   verdict carrying `reasoning` + a `proposed_patch`: the gate output contains both.

4. **B2 Bea wiring.** `bea-storyboard-context.md`: a loop-return frame sets `chain_from: 1` (one
   sentence in the establishing-vs-edit section). `storyboard_artist.py` `_make_bea_stub`: the
   loop-return frame sets `chain_from: 1`. Extend the `evals/storyboard_artist/` lint to assert it
   (warning-level, eval-side, like `edit_frame_form_lint`).

5. **Docs.** CHANGELOG.md (both halves, citing F3/F4/F5); CLAUDE.md (Bea row + the run-orchestrator
   `chain_from` note); the runbook's per-frame/troubleshooting positive-note guidance. Re-assert both
   md5 guards.

## Acceptance (all must hold before the PR)

- `python -m pytest tests/` green (658 + new, 0 regressions); `pipeline/tests/` green; `test_spark_shots_equivalence.py` + `test_run_shots.py` green (back-compat).
- B1: the eye gate surfaces Em's reasoning + proposed patch on a flagged verdict, and the retry hint steers positive — both proven by test.
- B2: `chain_from` validated + back-compat; `resolve_references` chains a `chain_from: 1` frame off frame 1 (no prior-frame ref); Bea's stub + context set it on loop-return frames; the eval lint asserts it.
- Both md5 guards intact; shared voice file unchanged; nothing under `evals/vision_critic/`.
- CHANGELOG.md + CLAUDE.md + runbook updated. One squash PR off the isolated worktree. Clean teardown.

## When done

Report the commits, the new test/eval count, full-suite-green-credential-free confirmation, both md5
guards intact, and a one-paragraph field note on any seam that fought you. Then stop — **Tier 1 is
complete.** The next move is the costed validation run (the real proof of Tier 1 + the Em-vs-eye label
harvest), then **Tier 2: the Em calibration campaign** — the autonomy core — planned in Cowork.
