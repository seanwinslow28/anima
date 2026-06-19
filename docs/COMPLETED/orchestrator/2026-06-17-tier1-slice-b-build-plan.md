# Build Plan — Tier 1 Slice B: eye-gate ergonomics + loop-return chaining ($0 stub-green, TDD)

*Dated 2026-06-17. The second and final Tier 1 slice. Companion to the [Tier 1 build plan](2026-06-17-tier1-fixes-build-plan.md) and the [Slice A field report](../../anima-test-runs/2026-06-17-bea-prompt-quality-field-report.md). Slice A (Bea prompt quality + reference hygiene) shipped in #58. This slice closes the remaining post-mortem findings (F4, F5, and the structural half of F3) — all in the orchestrator, all $0/stub-green. After it, Tier 1 is complete and the next live run validates the lot.*

> **Scope note vs the original Tier 1 plan:** the loop-return *chaining* fix was deferred there with a promotion trigger. The Slice A field report (lesson #4) promoted it: the "match frame 1" prompt discipline *mitigates* F3 but doesn't close it — frame 5 still chains off the approved frame 4 (the delight mascot), not frame 1. Since this slice is already in `generate_stage`, we fold the chaining fix in. Sean ratified (2026-06-17).

---

## Two halves, one slice

| Half | Post-mortem finding | What it does |
|------|---------------------|--------------|
| **B1 — eye-gate ergonomics** | F4 + F5 | Surface Em's reasoning + her staged proposed-patch at the eye gate (stop discarding what she already computed); steer retry notes toward positive/identity-lock framing. |
| **B2 — loop-return chaining** | F3 (structural half) | A back-compat `shots.yaml` `chain_from` field so a loop-return frame chains off frame 1, not the prior frame — removing the frame-4 reference pull the prompt fix only mitigated. |

Both live in the orchestrator (`generate_stage` + `run.py` + `shots.py`) plus Bea's context for B2. One cohesive slice; one squash PR.

---

## B1 — eye-gate ergonomics

**Root cause (verified against the run):** Em emits a rich `reasoning` paragraph and a staged `proposed_patch` (target / value / rationale / cites) on every borderline/fail verdict — e.g., F02: *"the mascot's front face lacks its pencil construction cross-lines… shading is a flat color step rather than textured graphite cross-hatching."* The eye gate (`generate_stage.run_frame_fan` tail) prints only `Em[character]: verdict (conf, cites)` — it **drops the reasoning and the patch**. So in the costed run Sean wrote retry notes from scratch, named the defect ("light blue shirt"), and the note — appended verbatim as `CORRECTION: <note>` — *reinforced* it. Em had already diagnosed the real issue and proposed a grounded fix; nothing surfaced it.

**Changes:**

| File | Change |
|------|--------|
| `pipeline/orchestration/generate_stage.py` | In the eye-gate print loop, when a verdict is `borderline`/`fail`, also print Em's **`reasoning`** (the in-memory `em_records` already carry it — currently unused at the gate) and her **proposed patch** summary (target / value / rationale — staged to `manifest.lock.yaml` via `stage_patches_hook`, or read off the Em result). Keep it readable: the reasoning is the high-value line. |
| `pipeline/orchestration/generate_stage.py` (retry hint) | Add a one-line steer to the printed `--retry-frame` hint: *"write the note as the desired end-state (positive identity-lock), not the defect — it's appended to the prompt, so naming the flaw reinforces it."* |
| `pipeline/run.py` | Mirror the positive-framing steer in the `--retry-frame` / `--note` help text. |
| `docs/2026-06-16-spark-authored-costed-run-runbook.md` | Update the per-frame + troubleshooting sections: assert the desired state, never name the defect; read Em's surfaced reasoning/patch before writing the note. |

**Deliberately deferred (Tier 2 seam):** a `--apply-em-patch` flag that re-rolls using Em's staged patch directly (propose→apply). Surfacing the patch is this slice; *applying* it autonomously is the first Tier-2 self-correction step — don't build it here, just make the patch visible so the human can hand-apply it now.

**Acceptance (B1):**
- On a `borderline`/`fail` verdict the eye gate prints Em's reasoning and proposed-patch summary — proven by a test with a stubbed Em verdict carrying `reasoning` + a `proposed_patch`.
- The retry hint (gate print + `run.py` help) carries the positive-framing steer.

## B2 — loop-return chaining

**Root cause (verified):** `resolve_references` builds a non-first frame's refs as `approved(first) + approved(prior) + chain_anchors' anchors`, where `prior = order[order.index(shot.id) - 1]`. For the loop-return frame (F5), `prior` is F4 — the *delight* mascot — so the reference set that should anchor "neutral" includes a lit-up face. The Slice A prompt fix ("composition identical to frame 1") fought this and won, but the pull is still there.

**Changes:**

| File | Change |
|------|--------|
| `pipeline/orchestration/shots.py` | Add an optional per-frame **`chain_from: int \| None = None`** to `Shot` + `_FRAME_KEYS`. Validate (when set): an int that names an **earlier** frame present in the sheet (`chain_from < id`, exists). Back-compat: absent → unchanged. |
| `pipeline/orchestration/generate_stage.py` | In `resolve_references`, `prior = shot.chain_from if shot.chain_from is not None else order[order.index(shot.id) - 1]`. The dedup already collapses `approved(first) + approved(prior)` to one ref when they're the same frame — so `chain_from: 1` on F5 yields `approved(1) + anchors`, dropping F4. Keep the existing "chains off approved frames that don't exist yet" guard. |
| `pipeline/agents/prompts/bea-storyboard-context.md` | Teach Bea: when she authors a loop-return frame (the `Composition identical to frame 1` rule from Slice A), **also set `chain_from: 1`** on that shot — so the board declares the loop anchor, not just describes it. One sentence in the establishing-vs-edit section. |
| `pipeline/agents/storyboard_artist.py` (stub) | The `_make_bea_stub` loop-return frame sets `chain_from: 1`, so a `--stub` run demonstrates the field and the eval can check it. |
| `evals/storyboard_artist/` | Extend the form lint (or a sibling check) to assert a loop-return frame carries `chain_from: 1`. Warning-level, eval-side only (consistent with `edit_frame_form_lint`). |

**Acceptance (B2):**
- `load_shots` accepts a frame with `chain_from`; rejects a `chain_from` that isn't an earlier in-sheet frame; absent → unchanged (`test_spark_shots_equivalence.py` + `test_run_shots.py` green = back-compat proof).
- `resolve_references` chains a `chain_from: 1` frame off frame 1 (not the prior) — proven by test (F5 refs = approved(1) + anchors, no F4).
- A stub authoring run's loop-return frame carries `chain_from: 1`; the eval check passes.

---

## File map (whole slice)

| File | Half | New/edit |
|------|------|----------|
| `pipeline/orchestration/generate_stage.py` | B1 + B2 | edit — eye-gate print (reasoning + patch + steer); `resolve_references` honors `chain_from` |
| `pipeline/orchestration/shots.py` | B2 | edit — optional `chain_from` field, validated, back-compat |
| `pipeline/run.py` | B1 | edit — positive retry-note steer in help text |
| `pipeline/agents/prompts/bea-storyboard-context.md` | B2 | edit — loop-return frame sets `chain_from: 1` |
| `pipeline/agents/storyboard_artist.py` | B2 | edit — stub loop-return frame sets `chain_from: 1` |
| `evals/storyboard_artist/` | B2 | edit — lint asserts loop-return `chain_from: 1` |
| `tests/test_run_shots.py` | B2 | edit — `chain_from` validation + back-compat |
| `tests/test_run_generate_stage.py` | B2 | edit — `resolve_references` honors `chain_from` |
| `tests/test_run_*` (eye gate) | B1 | new/edit — gate prints reasoning + patch on borderline/fail |
| `docs/2026-06-16-spark-authored-costed-run-runbook.md` | B1 | edit — positive-note guidance |
| `CHANGELOG.md` / `CLAUDE.md` | both | edit — dated entry; Bea row note for `chain_from` |

## TDD sequence

1. **B2 schema first** — `chain_from` in `shots.py` + `tests/test_run_shots.py`; then run `test_spark_shots_equivalence.py` + `test_run_shots.py` green (back-compat proof) before anything depends on it.
2. **B2 reference recipe** — `resolve_references` honors `chain_from` + `tests/test_run_generate_stage.py` (a `chain_from: 1` frame drops the prior, keeps frame 1 + anchors).
3. **B1 eye-gate print** — surface reasoning + patch on borderline/fail + the retry steer; test with a stubbed Em verdict carrying both.
4. **B2 Bea wiring** — context rule + stub sets `chain_from: 1` on loop-return; eval lint asserts it.
5. **Docs** — CHANGELOG + CLAUDE.md + runbook; re-assert both md5 guards.

## Acceptance (slice)

- `python -m pytest tests/` green (658 + new, 0 regressions); `pipeline/tests/` green; `test_spark_shots_equivalence.py` + `test_run_shots.py` green (back-compat).
- B1: eye gate surfaces Em's reasoning + patch on a flagged verdict; retry hint steers positive (both proven by test).
- B2: `chain_from` validated + back-compat; `resolve_references` honors it; Bea's stub + context set it on loop-return frames.
- Both md5 guards intact — Em baseline `2af75906502f1caf8857e18828ceb2e4`, shared voice `945af824fa53b948a18ac6bf206d67ef`. Nothing under `evals/vision_critic/`; the shared voice file unchanged.
- One squash PR off an isolated worktree. Clean teardown.

## After Slice B — Tier 1 is complete

Bea's edit-frame prompts land terse (Slice A), references are label-free (Slice A), the loop-return frame chains off frame 1 (B2), and the eye gate hands the human Em's grounded diagnosis instead of a blank note (B1). The next move is the **costed validation run** — the real proof of Tier 1 (curation cost should drop, no text bleed, the loop-return holds) and the harvest of more Em-vs-eye labels for **Tier 2: the Em calibration campaign** (the autonomy core), planned in Cowork after this lands.
