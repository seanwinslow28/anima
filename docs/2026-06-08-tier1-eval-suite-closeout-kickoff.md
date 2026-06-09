# Kickoff — Tier 1 Em eval-suite close-out: calibrate the Gate-2 proxy + housekeeping

*Paste-ready brief for a **Claude Code** session (NOT Cowork — this one spends, under fleet-ops). The Em (T2 vision-critic) eval suite now measures all three axes — verdict (0.97/1.00/0.00), citation (0.97), and the new constructive fix-rate (G6.9 Gate-3, normalized lift 0.667, merged #39). Tier 1 makes the suite **usable going forward**, not just measured-once: (A) calibrate the Gate-2 golden-agreement proxy judge so fix-rate can be tracked between costed runs **without** re-spending the $7.80 Gate-3 run; (B) tidy the merge debris (stale branches + superseded docs). Total spend is small (~$1.50–2 Gemini for Em-diff capture; the Opus judge is subscription-absorbed). Tier 2/3 are ticketed separately — out of scope here.*

**Standing doctrine: verify against the tree, never trust a label — including this brief and the runbooks it points at.** This arc's worst moments came from trusting a label over the tree: the 2026-06-07 run measured nothing because a flag was silently off; the Gate-3 v1 run **crashed on case #0** because the runbook claimed the loop "self-isolates" when the orchestrator had no try/except. Both were caught by verifying first. Assert before you spend.

## ⚠ FIRST, EVERY SESSION — divergence + tree guard

A Cowork sandbox can't reach GitHub; you (Claude Code) can. Run before anything else:

1. `git fetch origin && git rev-list --left-right --count main...origin/main` → expect `0 0` (last known clean 2026-06-08, HEAD `1c4cd9e`/#39).
2. `git log --oneline -6` — confirm the merged Gate-3 stack: `1c4cd9e` (#39 Gate-3 run + containment) · `c01920c` (#38 Stage-2 handoff) · `cc9d0f5` (#37 subprocess isolation) · `943612b` (completion plan) · `af90a99` (#36).
3. `git status -s` → expect **clean**.
4. **Verdict-baseline guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` → **`2af75906502f1caf8857e18828ceb2e4`**. This is the verdict baseline; it stays byte-identical through ALL of Tier 1. Calibration is additive — a new axis of trust over Em's *diffs*, never a re-score of her verdicts.
5. `grep -c 'golden_diff_ratified: true' evals/vision_critic/cases.yaml` → **30** (the goldens calibration scores against).

## Read, in order

1. [`docs/2026-06-08-em-eval-suite-completion-plan.md`](2026-06-08-em-eval-suite-completion-plan.md) — the inventory this closes Tier 1 of (P2 = this calibration; housekeeping items 11 + doc-archive).
2. [`docs/anima-test-runs/2026-06-08-em-g6.9-gate3-fixrate.md`](anima-test-runs/2026-06-08-em-g6.9-gate3-fixrate.md) — the just-landed Gate-3 result + **the v1-crash retrospective** (why "the runbook over-claimed containment" — your cautionary tale for trusting a harness's self-description).
3. [`evals/vision_critic/diff_eval.py`](../evals/vision_critic/diff_eval.py) — **the Gate-2 surface you're calibrating.** `score_golden_agreement` (the judge call), `opus_judge` (the real Gate-2 judge, subscription SDK), `_AGREEMENT_PROMPT`, and the `--check-only` stub. **Note the gap:** the CLI ships only the $0 stub plumbing check; there is **no calibration harness** — you build it (scaffold-first, like SF03).
4. [`docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md`](research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md) **§3.1–3.3 + §5** — the calibration *method* (don't reinvent it): Critique Shadowing (§3.1), the class-imbalance trap (§3.2 — **report precision/recall on the match class, never raw agreement; the dangerous error is the judge over-calling "match"**), sampling-consistency over verbalized confidence, the κ≥0.6 bar, and the corrected literature bias ledger (§3.3) your Em-specific ledger extends.
5. `CLAUDE.md` — the **`vision_critic` — Em row** (state-of-record; carries the three axes) and `PHILOSOPHY.md` (critics propose, the human owns taste — Sean's labels are ground truth).

## Where we are (verify each)

- **Em's three axes are all measured.** Verdict + citation ratified; constructive fix-rate landed #39 (overall lift 0.667, discriminative on all six classes, proposal-rate 1.00 — but a **small-N first read**, 6 outcomes/class/arm).
- **The Gate-2 golden-agreement proxy is BUILT but UNCALIBRATED.** `diff_eval.py::score_golden_agreement` + `opus_judge` exist; the module docstring states plainly that "a judge's numbers are not trustworthy until calibrated against a Sean-labeled sample (record the judge-bias ledger)." Until calibrated, the cheap per-run proxy can't be trusted to stand in for the $7.80 empirical run. **Closing that is Part A.**
- **Merge debris.** 1 stale local branch + **7 stale remote branches** (`git branch -r` minus main/HEAD); several Gate-3 planning/handoff docs are now superseded or executed and belong in `docs/COMPLETED/` / `docs/OLD/` per the archive convention. **Part B.**

---

## PART A — calibrate the Gate-2 golden-agreement judge (the substantive deliverable)

**What "calibrated" buys.** Gate 3 (empirical fix-rate) is the headline but costs ~$7.80 and ~2.5 hr per run. Gate 2 asks the cheap proxy question — *does Em's proposed clause express the same fix as Sean's ratified golden?* — judge-scored, runnable any time for ~pennies. If the judge agrees with Sean reliably, you can track Em's constructive quality between costed runs. An **uncalibrated** judge "launders a guess into a verdict" (handbook §3) — worse than no proxy.

**The dangerous error to measure explicitly.** For *this* proxy the costly failure is the judge **over-calling "match"** (says Em's clause matches the golden when Sean says it doesn't) — that would inflate Em's tracked fix-rate in her own favor. So the calibration set must be **balanced** (enough genuine non-matches to give the false-positive rate statistical power), and the headline is **precision/recall on the match class + the false-positive rate**, never raw agreement (which misleads under imbalance — §3.2).

### A0 — scaffold first ($0, TDD, no spend)

Build the calibration harness CI-green *before* any model call (the SF03 discipline). Suggested: `evals/vision_critic/calibrate_diff_judge.py` (+ `tests/test_calibrate_diff_judge.py`), reusing `score_golden_agreement`, `opus_judge`, `_extract_json`, and `scoring.stderr`. It must:
- Load (a) a captured-Em-diffs file (case → Em's `.value`), (b) a Sean-labels file (pair → match/no-match ground truth).
- Run the judge **N times per pair** (N=5, majority vote — sampling consistency, since verbalized confidence is unreliable per §3.5) and record per-pair vote spread.
- Emit a confusion matrix vs Sean: **precision + recall on "match", the false-positive rate, raw agreement (flagged as imbalance-sensitive), and Cohen's κ** — segmented overall + by defect class.
- A `--stub`/`--check-only` path that runs the whole pipeline on a credential-free stub judge + a tiny synthetic label set (proves the plumbing, makes no scored claim). Tests assert: stub pipeline runs; FPR/precision/recall math; "no diff proposed" stays `match=None` (never a 0); N-vote majority logic.
- Confirm green: `python -m pytest tests/test_calibrate_diff_judge.py -q` + the full contract suite still passes (it was **410** after #39).

### A1 — the costed calibration run (fleet-ops; ~$1.50–2 Gemini + subscription Opus)

In order, each gate $0 unless noted:

1. **§0 gates ($0).** Divergence `0 0`; baseline md5 guard byte-identical; `ANTHROPIC_API_KEY` **absent** (the Opus judge must bill the subscription via the SDK — `diff_eval.opus_judge` → `invoke_opus_text`); `GEMINI_API_KEY` present in `.env` (for Em capture). Stub harness green.
2. **Capture Em's real diffs (~$1.50, the only real spend).** Run Em LIVE on the 30 `identity_style` defect cases and persist her first `proposed_patches[].value` per case to a JSONL. Use the existing capture path — either a loop over `score.py --only <case> --dump-patches` (it captures + asserts non-empty + exits) or a thin script calling `patch_efficacy._capture_em_value` per case. **Assert non-empty** before proceeding (the §0 capture-proof discipline — an empty capture means the proxy has nothing to score, stop and surface). Identity_critical cases force Opus escalation (subscription-absorbed; budget wall-time, ~100s/escalated call).
3. **Build the balanced calibration set.** The 30 real (Em-clause, golden-clause) pairs — ground truth is **not** assumed (Em may genuinely match or differ) — **plus ~20–25 constructed non-match pairs** (pair a golden with a *different defect class's* clause) to give the false-positive rate power. Target ≈ 25 plausible-match + ≈ 25 designed-non-match ≈ 50 pairs (§ "30–60 balanced, real, labeled cases" is the honest v1).
4. **⚖ SEAN LABELING CHECKPOINT (human ground truth — the real artifact, NOT yours to fabricate).** Emit a labeling sheet (one row per pair: defect class, candidate clause, reference golden, blank `match: ` + blank `why: `). **Pause.** Sean labels each pair binary match/no-match + a one-line critique (Critique Shadowing — his critiques, not the judge, are the real output). Resume from his completed sheet. Do not proceed on synthesized labels.
5. **Run the judge + score (~pennies, subscription).** `opus_judge` N=5 per pair via `score_golden_agreement`; build the confusion matrix vs Sean's labels: precision/recall on match, **false-positive rate**, raw agreement (note imbalance), κ. Position/verbosity bias note where relevant (§3.4).
6. **Iterate if below bar.** Bar: κ ≥ 0.6 (substantial) and an FPR low enough to trust the proxy in Em's favor. If short, tighten `_AGREEMENT_PROMPT` seeded with Sean's critiques as few-shot (§3.1 — convergence is often ≤3 iterations), re-run on the same set, re-measure. Cap iterations; if it won't converge, that itself is the finding (the proxy isn't trustworthy yet — say so).
7. **Verdict.** State plainly whether the Gate-2 proxy is now trustworthy enough to track fix-rate between costed runs, with the calibrated numbers and the residual biases named.

### A2 — deliverables (Part A)

- The harness (`calibrate_diff_judge.py`) + tests, green.
- The captured-Em-diffs JSONL + Sean's labels file (both committed as the calibration corpus).
- A **dated trace** under `evals/vision_critic/traces/` (the confusion matrix, per-class, N-vote spreads, raw JSON) + a **field report** `docs/anima-test-runs/2026-06-XX-em-gate2-judge-calibration.md` (the §0 evidence, the labeling-checkpoint provenance, the calibrated precision/recall/FPR/κ, the **Em-Gate-2 judge-bias ledger**, the trustworthy-or-not verdict).
- **CLAUDE.md Em-row update** — flip the Gate-2 proxy from "built but uncalibrated" to its calibrated state (a real state-of-record shift). Keep the verdict/citation/Gate-3 lines untouched.
- **CHANGELOG entry.**

---

## PART B — housekeeping (secondary; safe first, careful second)

### B1 — prune stale merged branches (safe — do first)
After confirming each is fully merged into `main` (`git branch -r --merged origin/main`), delete:
- **Local:** `docs/em-g6.9-gate3-stage2-handoff`.
- **Remote (7):** `origin/docs/em-g6.9-gate3-stage2-handoff`, `origin/docs/g6.9-sf03-planning-2026-06-08`, `origin/em-g6.9-gate3-subprocess-isolation`, `origin/feature/em-g6.1-citation-grounding-handoff`, `origin/feature/em-g6.9-gate3-fixrate`, `origin/g6.9-gate3-costed`, `origin/ratify-g6.9-goldens`.
Verify-merged before each delete; do not force-delete an unmerged branch.

### B2 — archive superseded/executed docs (careful — link-fix discipline)
Per the archive convention (`COMPLETED/` = executed/shipped, `OLD/` = superseded), `git mv` these and **fix inbound links in *active* docs only** (leave CHANGELOG's historical entries as-is — a decision log records where things were):
- `docs/2026-06-08-g6.9-gate3-costed-handoff.md` → `docs/OLD/` (superseded by the Stage-2 handoff; banner already added). Inbound active refs to fix: the completion plan, the original kickoff, the stage-2 handoff.
- `docs/2026-06-08-em-g6.9-gate3-stage2-fleet-ops-handoff.md` → `docs/COMPLETED/` (executed by #39). Inbound active ref: the Gate-3 field report.
- `docs/2026-06-08-g6.9-ratification-and-costed-gate3-plan.md` → `docs/COMPLETED/` (executed). Inbound active ref: the completion plan, the original kickoff.
- `docs/2026-06-08-eval-suite-completion-kickoff.md` → `docs/COMPLETED/` (this whole arc's kickoff, executed).
- `docs/2026-06-04-prompt-diff-eval-design.md` → `docs/COMPLETED/` (design now implemented through Gate 3).
**Leave the living index in root:** `docs/2026-06-08-em-eval-suite-completion-plan.md` stays (it tracks the still-open Tier 2/3) — just update its inventory: P1 → DONE, P2 → this session, Tier 2/3 → ticketed.
After moving: `grep -rl` each moved filename to confirm no *active* doc has a dangling link; run `python -m pytest tests/` + `python -m pytest pipeline/tests/` to confirm nothing import-references a moved path. **If link-fixing balloons beyond these, stop at B1 and ticket B2** — it's tidy-up, not load-bearing.

---

## Fleet-ops (Part A1 spend)

Isolated worktree off updated `origin/main` · single owner · `git fetch` + divergence check before AND after · subscription billing (`ANTHROPIC_API_KEY` absent; no `--allow-api-key` hatch) · `GEMINI_API_KEY` bounded from `.env` · singleton pre-flight + own-PID · no `start_new_session` on a costed worker · §0 gates before spend · land via squash PR off `origin/main` · clean teardown. Full protocol: [`docs/fleet-ops-protocol.md`](fleet-ops-protocol.md).

## The mistake ledger — do not re-learn

- **A harness's self-description is not a verified code path.** The Gate-3 runbook claimed the loop "self-isolates"; the orchestrator had no try/except and the v1 run crashed on case #0. Read the loop, don't trust the docstring.
- **Don't fabricate Sean's labels.** Calibration ground truth is human (the labeling checkpoint pauses for him). A judge calibrated against synthesized labels measures nothing.
- **Raw agreement lies under imbalance.** Headline = precision/recall on match + FPR, not agreement %. Balance the set.
- **The verdict baseline is byte-identical** (md5 above) before AND after. Calibration is additive — a ruler for Em's diffs, never a re-score of her verdicts.
- **§0 before spend**; capture must be non-empty before scoring; **fleet-ops billing or it didn't happen.**

## Deliverables checklist

- [ ] Part A harness + tests green; captured-diffs + Sean-labels corpus committed.
- [ ] Calibration trace + field report + Em-Gate-2 judge-bias ledger; trustworthy-or-not verdict stated.
- [ ] CLAUDE.md Em-row Gate-2 line flipped to calibrated; CHANGELOG entry; verdict baseline md5 unchanged.
- [ ] B1 stale branches pruned (1 local + 7 remote, verify-merged first).
- [ ] B2 docs archived + active links fixed + suites green (or B2 ticketed if it balloons).
- [ ] Completion-plan inventory updated (P1 done, P2 this session, Tier 2/3 ticketed).
