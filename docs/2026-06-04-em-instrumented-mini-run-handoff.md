# Handoff — Em instrumented mini-run (G6.2): persist cites + reasoning, diagnose the citation axis

*2026-06-04. Costed Claude Code handoff under [`docs/fleet-ops-protocol.md`](fleet-ops-protocol.md). First costed move of the G6 arc (decided in the 2026-06-04 Cowork session). This is a DIAGNOSTIC, not a baseline: 1 run × 50 cases (~50 Gemini calls + occasional Opus escalations), config held identical to the ratified G5 baseline so the results are comparable. **No relabeling, no prompt changes, no criteria changes, no baseline movement.***

**Standing doctrine: verify against the tree, never trust a label — including this brief.**

---

## Why now / why first

G5 ratified Em's verdicts (performs 0.97 / 1.00 / 0.00) but measured **cites-correct = 0.03** with the cause confounded: geometry classes structurally can't cite (their `expected_cites` are seam handles that don't exist as IR rules in Em's merged criteria), while style classes (palette/construction/shading) map to real `IR.sean.*` handles and *still* scored near-zero — genuine mis-citing or scoring artifact, undiagnosable because G5 didn't render per-case cites or persist reasoning. Separately, `clean-c06` failed in all 5 runs — a consistent Em-vs-ground-truth disagreement nobody has read her reasoning on.

**Sequencing constraint (why this runs BEFORE the citation-grounding fix):** G6.1 will add geometry IR criteria, which changes Em's input surface — every number after that is a new baseline. The diagnostics that need comparability with G5 (this run, then the references re-test) must run against the *current* criteria bundle first.

## Pre-work (uncosted, mocked — verify $0 before any live call)

1. Extend the trace writer so the dated trace persists, **per case**: `expected_cites`, `actual_cites`, `reasoning`, `confidence`, verdict. Note: `evals/vision_critic/score.py` already carries `actual_cites` in `CaseScore` (cites taken from a run matching the majority verdict) — this is mostly a rendering/persistence change plus capturing `reasoning`. Verify against the tree what's already there; minimal diff.
2. Mocked pre-flight must cover the **`gemini_api` transport**, not just legacy `agy` — the exact cost-leak fixed in `71f8d80` (CHANGELOG 2026-06-04). Run the mocked path and confirm zero live calls before trusting it.
3. `python -m pytest tests/ -q` and `python -m pytest evals/vision_critic/runner.py -q` green before and after the instrumentation diff.

## The run

- `python -m evals.vision_critic.score --runs 1` (or the equivalent single-pass invocation — verify the CLI surface).
- Config **identical to G5**: reference-blind (`critics.t2.attach_references: false`), `gemini-3.5-flash` pinned by ID via `gemini_api` transport, Opus 4.7 SDK escalation rules unchanged, served model read back from `resp.model_version`.
- Subprocess-per-case isolation; an empty-cites invariant error lands as an honest gap, not an abort. Expect the geometry classes to trip it sporadically — **that's data here, not failure**: record which cases trip it.

## Questions this run must answer

- **Q1 (style cites):** For palette/construction/shading cases, what does Em actually put in `cites_criteria`? Classify each: (a) correct rule, (b) real-but-wrong rule, (c) generic/invented handle, (d) formatting near-miss the scorer rejects. (d) means scoring artifact → fix the matcher; (b)/(c) mean genuine grounding weakness → shapes the G6.1 criteria work.
- **Q2 (clean-c06):** Read Em's reasoning on the left-profile false positive. What does she claim to see? Is it a view mis-read, a register complaint, or something actually in the image? Output: a recommendation — relabel (only if the image genuinely violates a ratified rule — ships-red discipline, no tuning cases to flatter Em), fix a prompt ambiguity, or keep as a known disagreement.
- **Q3 (geometry cites):** When Em flags a proportion/view/anatomy defect, what does she cite (when anything)? Her natural vocabulary here is direct input to authoring the G6.1 geometry IR criteria — write the rules in handles she already reaches for where possible.

## Deliverables

1. Instrumentation diff (trace writer), tests green, mocked-$0 verified.
2. Dated trace `evals/vision_critic/traces/2026-06-XX-instrumented-mini-run.md` with the full per-case cite/reasoning table.
3. Short field report `docs/anima-test-runs/2026-06-XX-em-instrumented-mini-run.md` answering Q1–Q3 with a per-class cite-classification table.
4. CHANGELOG entry.
5. Merge the branch **INTO MAIN**, push, clean-teardown the worktree. (The G5 arc's near-miss was integrating the wrong direction.)

## Fleet-ops checklist

Isolated worktree (one per plan) · `ANTHROPIC_API_KEY` absent (subscription SDK for escalations) · `GEMINI_API_KEY` bounded from `.env` · singleton pre-flight + own-PID resolution · single owner · no `start_new_session` on the costed worker · clean teardown · merge into main.

## Out of scope

Relabeling cases · changing Em's prompt or criteria · flipping `attach_references` · touching the ratified baseline (it moves only via a new replicated run) · the references re-test (separate handoff, runs after this one, also before G6.1 lands).
