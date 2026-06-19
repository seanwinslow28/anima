# Field Report — Tier 1 Slice B: eye-gate ergonomics + loop-return chaining ($0 stub-green, TDD)

**Date:** 2026-06-18
**Kickoff:** [`docs/2026-06-17-tier1-slice-b-kickoff.md`](../COMPLETED/orchestrator/2026-06-17-tier1-slice-b-kickoff.md)
**Plan of record:** [`docs/2026-06-17-tier1-slice-b-build-plan.md`](../COMPLETED/orchestrator/2026-06-17-tier1-slice-b-build-plan.md)
**Why:** [`docs/anima-test-runs/2026-06-17-spark-authored-costed-run-post-mortem.md`](2026-06-17-spark-authored-costed-run-post-mortem.md) (F3/F4/F5) + the [Slice A field report](2026-06-17-bea-prompt-quality-field-report.md) lesson #4
**Spend:** $0 (stub-green throughout; no model transport invoked in this session — the suite is green with `ANTHROPIC_API_KEY` ABSENT)
**Branch / PR:** `worktree-tier1-slice-b` off `origin/main` `99dc389` (#59) → [PR #60](https://github.com/seanwinslow28/anima/pull/60); four TDD commits, each revertible alone

---

## What this was

The **second and final Tier 1 slice** — two orchestrator fixes from the first live costed run, both `$0`/stub-green. **B1 (ergonomics, F4+F5):** the per-frame eye gate was throwing away Em's grounded diagnosis. She emits a `reasoning` paragraph and a staged proposed-patch on every borderline/fail verdict, but the gate printed only `Em[ns]: verdict (conf, cites)` — so in the costed run Sean wrote retry notes from scratch, named the defect ("light blue shirt"), and the note (appended verbatim as `CORRECTION:`) *reinforced* it. **B2 (loop-return chaining, F3 structural half):** the loop-return frame chained off the *prior* approved frame (the delight mascot), not frame 1 — the Slice A prompt fix ("composition identical to frame 1") mitigated but didn't close it.

Both halves landed exactly as scoped: the `chain_from` schema + validation, the `resolve_references` recipe change, the eye-gate print + positive-note steer, Bea's context/stub/eval wiring, and docs. **7 new contract tests (658 → 665 in `tests/`) + 2 new eval cases (6 → 8 in `evals/storyboard_artist/`); zero regressions.** After this slice, **Tier 1 is complete.**

---

## Failures & corrections (the part worth reading)

There were no runtime failures, and — notably — **the kickoff verified clean on arrival.** Slice A's doctrine note warned that the prior kickoff's "re-check the anchors are clean" was false against the tree; this kickoff's every checkable claim (the eye-gate print loop iterating `em_records` that carry `reasoning`; `prior = order[order.index(shot.id) - 1]`; `_FRAME_KEYS` as the `beat_id`/`locked` precedent; the dedup collapsing duplicate refs) held against the source. That's worth recording precisely *because* the doctrine assumes the opposite — this time the document and the tree agreed. The corrections below are smaller, and three of the four are decisions the kickoff explicitly left open ("read off the Em result" / "or a sibling check").

### #1 — `em_records` carried a patch *count*, not the patch fields

The kickoff said the in-memory `em_records` "already carry `reasoning` (currently unprinted)" and to surface the patch "staged to `manifest.lock.yaml` via `stage_patches_hook`, **or read off the Em result**." Verifying the append site (`generate_stage.py:214`) showed `reasoning` is indeed carried, but the patch was stored only as `"patches": len(r.proposed_patches)` — a bare integer. So printing `target/value/rationale` needed a real source, not just a re-print.

**Resolution:** took the kickoff's "read off the Em result" fork — enriched each `em_record` with a `proposed_patches` summary list (`target/path/value/rationale`) built from `r.proposed_patches` at append time, keeping the `patches` count untouched for back-compat with any reader of `em_verdicts.jsonl` or the attempt trail. This keeps the gate print **purely in-memory** — no re-reading `manifest.lock.yaml` at print time, no coupling the gate to the patch-stager's on-disk format. The empty-cites branch got `"proposed_patches": []` for symmetry so the print loop can't `KeyError`.

**Why it matters:** the obvious read of "already carry it" would have had me print `v['patches']` and get `2` instead of Em's actual fix. The cheap verification of the append site (not just the print loop) caught it.

### #2 — Making the lint *meaningful on stub output* forced a faithful-loop change to Slice A's stub

The kickoff asked the stub's loop-return frame to set `chain_from: 1` "so a `--stub` run demonstrates the field and the eval can check it," and to extend the lint "like `edit_frame_form_lint`." But Slice A's `_make_bea_stub` authored **every** non-first frame — including the final one — as an `ONLY CHANGE:` delta. My `chain_from_lint` fires on loop-return *prompts* (`composition identical to frame 1`); the stub's final frame wasn't one, so the lint could never "check" the stub the way the kickoff intended.

**Resolution:** made the stub faithful to a real pencil-test loop — the **final** frame is now authored as a frame-1 *match* (`Composition identical to frame 1: …`) carrying `chain_from: 1`, while the **middle** frames stay terse `ONLY CHANGE:` deltas. This is a deliberate revision of a Slice A decision (which lumped the loop-return in with the edit deltas), so it required rewriting the Slice A test `test_stub_emits_establishing_then_edit_form` to express the new three-role shape (establishing / edit / loop-return). The new `test_stub_board_is_chain_from_lint_clean` then proves the lint runs clean on real stub output — exactly what the kickoff wanted.

**Why it matters:** `is_edit_delta` already accepts both the `ONLY CHANGE:` and the `identical to frame 1` forms, so `edit_frame_form_lint` stayed green either way — the change was invisible to the *other* lint, which is why the Slice A test had quietly encoded the wrong final-frame shape. Building the new lint surfaced that the stub and a real board (the `edit-form-board` fixture, whose frame 5 *is* a loop-return) had diverged.

### #3 — One validation, two failure modes, via `seen_ids`

`chain_from` must reject both "names a later/self frame" (`>= id`) and "names a frame that isn't in the sheet" (a gap, e.g. `chain_from: 2` when ids are `1, 3, 5`). Since ids are validated strictly-ascending in order, I track a `seen_ids` set and check `chain_from < id` **and** `chain_from in seen_ids` — one guard covers both, and the bool-is-an-int trap (`isinstance(True, int)`) is excluded explicitly, matching the `beat_id` precedent's spirit.

**Why it matters:** minor, but it's the kind of validation that looks like a one-liner (`chain_from < id`) and silently accepts a dangling reference. The membership check is what makes "earlier *and exists*" a single honest assertion.

### #4 — The runbook's own example note named the defect

While updating the runbook (docs step) I found its Gate-5 example `--note` was `"mascot drifted toward red — hold the terracotta box-creature palette"` — the exact anti-pattern B1 exists to fix (it *names* the defect, which the `CORRECTION:` append then reinforces). Corrected it to a pure end-state (`"hold the terracotta box-creature palette — warm clay-orange box body"`) and added a troubleshooting bullet for "a re-roll keeps reproducing the defect you named."

**Lesson:** the doc that teaches the fix had modeled the bug. Fixing the code without fixing the worked example would have left the trap baited.

---

## What we got right (and why it held)

- **TDD with small revertible commits, schema-first.** Four commits, each red→green with a targeted run before the full suite. B2 schema landed (and the back-compat proof ran green) *before* the recipe depended on it; the eye-gate test used the existing `fake_em_transport` fixture (one additive `reasoning=` param) rather than a bespoke harness.
- **Back-compat was load-bearing and proven, not asserted.** `chain_from` is optional; the shipped Spark board has none; `test_spark_shots_equivalence.py` + `test_run_shots.py` stayed green the whole way. The dedup did the real work — `chain_from: 1` makes `first == prior == 1`, and the order-preserving dedup collapses the duplicate, so the recipe change is three tokens of code (`shot.chain_from if … else …`) and the rest is the existing machinery.
- **The eye-gate change is in-memory and additive.** Enriching `em_records` (not re-reading the lock), gating the new print on `verdict != "pass"` (a superset of the kickoff's "borderline/fail" that also catches the `human_review` empty-cites state where the reasoning is most useful), and keeping the `patches` count — nothing downstream of the gate changed shape.
- **The two standing guards never moved.** Em verdict-baseline `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` md5 `2af75906502f1caf8857e18828ceb2e4` and the shared `sean-screenwriting-voice.md` md5 `945af824fa53b948a18ac6bf206d67ef` were captured at §0 and re-checked before the docs commit — both byte-identical. Nothing under `evals/vision_critic/` was touched.

---

## What we learned

1. **A clean kickoff is not a license to skip the verify — it's the reward for doing it.** Every claim still got checked against the tree; the payoff was confidence, not corrections. The one place "already carries it" was loosely true (#1) is exactly where a skipped verify would have shipped `2` instead of a fix.
2. **A new check can expose that an old artifact encoded the wrong thing.** `chain_from_lint` didn't just add coverage — building it revealed that Slice A's stub had quietly mis-shaped the loop-return frame, invisible to the lint that already existed (#2). When you add a discriminator, run it against the things you already believed were correct.
3. **Surface, don't apply — and say so.** B1 deliberately stops at *showing* Em's proposed patch; `--apply-em-patch` (propose→apply) is the first Tier-2 self-correction step and was left unbuilt on purpose. The slice's value is making the patch *visible* so the human can hand-apply it now, while the autonomy core is still ahead.
4. **Fix the worked example, not just the mechanism (#4).** Positive-framing guidance in the code is undercut if the runbook still demonstrates the negative. The teaching surface is part of the change.

---

## How to proceed

1. **The costed validation run is the real proof of Tier 1.** Slice A made Bea's edit-frame prompts terse and the references label-free; Slice B chains the loop-return off frame 1 (B2) and hands the human Em's grounded diagnosis instead of a blank note (B1). None of this is proven against *live model output* yet — the stub demonstrates the field and the form, but a real Sonnet board + a real Em verdict are what validate the curation-cost drop, the no-text-bleed, and the loop-return hold. Run "The Spark, Shared" end-to-end per the [runbook](../COMPLETED/orchestrator/2026-06-16-spark-authored-costed-run-runbook.md).
2. **Harvest the Em-vs-eye labels.** That same run is the label source for **Tier 2: the Em calibration campaign** (the autonomy core, planned in Cowork). Every eye-gate decision where Sean agrees or overrides Em's surfaced reasoning/patch is a calibration datum — B1 is precisely what makes that comparison legible at the gate.
3. **`--apply-em-patch` is the Tier-2 seam, not a follow-on bug.** It was scoped out on purpose. When the calibration campaign establishes that Em's patches clear defects at an acceptable rate (the Gate-3 fix-rate work is the precedent), wiring a propose→apply flag onto the now-visible patch is the natural next step.
4. **Tier 1 is done. Stop hardening the orchestrator seams and run it.** `chain_from` is validated + back-compat, the eye gate is legible, the retry note steers positive, the stub + eval cover the new field. The remaining named-but-unbuilt orchestrator work (museum capture) is its own slice; the immediate move is the costed run, not more `$0` polish.

---

## Done criteria — checked

- [x] `python -m pytest tests/` → **665 passed** (658 + 7 new), no regressions; credential-free (`ANTHROPIC_API_KEY` ABSENT). `pipeline/tests/` 10 passed.
- [x] `test_spark_shots_equivalence.py` + `test_run_shots.py` green (back-compat: the shipped Spark board has no `chain_from` and parses unchanged).
- [x] B1: on a flagged (non-pass) verdict the eye gate prints Em's `reasoning` + her proposed-patch summary, and the retry hint + `run.py --note` help steer the note positive — proven by `test_eye_gate_surfaces_em_reasoning_and_patch_on_flagged_verdict`.
- [x] B2: `chain_from` validated (earlier in-sheet frame only) + back-compat; `resolve_references` chains a `chain_from: 1` frame off frame 1 with no prior-frame ref — proven by `test_resolve_references_chain_from_chains_off_the_named_frame_not_prior` (+ the no-`chain_from` control).
- [x] B2: Bea's context + `_make_bea_stub` set `chain_from: 1` on the loop-return frame; `evals/storyboard_artist/runner.py` 8 passed (6 → 8) — the `chain_from_lint` accepts the declared board and flags the missing-`chain_from` ships-red fixture; the stub board is lint-clean.
- [x] Em baseline md5 `2af75906502f1caf8857e18828ceb2e4` and shared voice md5 `945af824fa53b948a18ac6bf206d67ef` both unchanged from §0; nothing under `evals/vision_critic/` touched; shared voice file untouched.
- [x] CHANGELOG.md (2026-06-18) + CLAUDE.md (Bea row third `shots.yaml` addition + loop-anchor note; run-orchestrator eye-gate/chain_from notes) + runbook (Gate 5 + troubleshooting) updated. One squash PR ([#60](https://github.com/seanwinslow28/anima/pull/60)) off the isolated worktree; clean teardown to follow merge.
