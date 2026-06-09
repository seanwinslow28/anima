# Design draft — evaluating Em's prompt diffs (G6.9): scoring the job she's actually for

*2026-06-04. DRAFT design, opened in the G6 Cowork session. Uncosted thinking — no build, no spend. The Critic Stack's contract is that T2 "proposes prompt diffs, not pass/fail" — and after G5, verdicts are the ONLY thing the eval suite measures. Em's actual production output (`proposed_patches` staged into `manifest.lock.yaml`) has zero eval coverage. This doc frames how to score it. Iterate with Sean before any of this becomes a handoff.*

---

## The problem

"Flags correctly" is now measured (0.97/1.00/0.00). "Proposes a fix that helps" is not. These can diverge arbitrarily: Em could catch every defect and propose diffs that are useless, harmful, or ungrounded. Per the eval handbook (error-analysis-first, binary single-axis, judge calibration), scoring "useful fix" is a judge-calibration problem — fundamentally harder than verdict scoring because usefulness has no deterministic ground truth.

## Hard dependency

**G6.1 citation grounding lands first.** A prompt diff's rationale cites criteria (`cites_criteria` on the Patch). With cites-correct at 0.03, diff *grounding* can't be scored before citations are fixed — we'd be measuring noise. Diff-eval design can proceed now; diff-eval *measurement* waits for the post-G6.1 re-baseline.

## What "useful" could mean — three candidate designs, cheapest signal first

### Design 1 — Outcome A/B: does applying the diff fix the defect? (the empirical anchor)
For a defect case, capture Em's proposed diff → apply it → re-generate the frame (same seed-ish conditions, content-hashed node) → run Em (or T1, where the defect class is deterministic) on the re-roll. Binary per case: **defect cleared, identity/style held**.
- *Pro:* empirical, not vibes — the closest thing usefulness has to ground truth; aligns with Engine Truth.
- *Con:* costed (one generation + one critique per case); confounded by generation stochasticity (mitigate: N re-rolls per diff, report clear-rate, exactly like the N=5 verdict band); a diff can "work" by accident.
- *Estimated unit cost per case:* 1 NB2 generation + 1 Em call ≈ the cheapest empirical signal available.

### Design 2 — Golden-diff agreement (the labeled-set analog)
Sean authors the *reference fix* for each corpus defect case (e.g. palette-pad2 red shirt → the prompt clause he would actually add). Score Em's diff against the golden one — judge-scored semantic match, binary.
- *Pro:* uncosted at eval time after authoring; deterministic-ish; extends the existing corpus pattern (every defect case gains a `golden_diff` field).
- *Con:* 28+ golden diffs is real Sean authoring; penalizes valid alternative fixes (a diff can disagree with the golden one and still work — Design 1 catches what this misses); the judge needs calibration per the handbook's bias ledger.

### Design 3 — Judge-scored usefulness rubric (the fallback, use sparingly)
An LLM judge scores each diff on a binary rubric: targets the cited defect / actionable as a prompt edit / doesn't re-describe the character (Seedance rule) / doesn't violate style-neutrality doctrine. Calibrate the judge against a Sean-labeled sample first (handbook procedure).
- *Pro:* cheap, runs on existing traces.
- *Con:* judge-on-judge — weakest evidence class; only trustworthy after calibration; never the headline number.

## Proposed shape (strawman for Sean to react to)

Layer them like the critic stack itself: **Design 2 as the fast per-case gate** (golden agreement, binary, runs in the suite) + **Design 1 as the periodic empirical validation** (clear-rate on a sampled subset, dated runs like the baselines) + Design 3 only as a triage signal. Headline metric candidate: **fix-rate** (Design 1 clear-rate) with golden-agreement as the cheap proxy tracked per run. Both segmented like verdicts (per-class, with bands).

## Open questions for Sean

1. Does the corpus gain a `golden_diff` field per defect case (Design 2), and is that authoring he wants to do alongside the P-B1/PA-D4 re-rolls?
2. Is Design 1's spend (≈1 generation + 1 critique × sampled cases × N re-rolls) acceptable as a *periodic* validation rather than per-run?
3. Should diff-eval wait for the post-G6.1 re-baseline entirely, or is a Design-3-only dry read on the mini-run's persisted reasoning worth having early?
4. Patch scope: score only `prompt` diffs, or also Em's other patch targets (manifest fields, criteria-cited mutations)?

## Non-goals

Auto-applying patches (stage-first per v2 lock is untouched) · scoring T3 council output (not built) · replacing the verdict suite (this is additive, the second axis of the same ruler).
