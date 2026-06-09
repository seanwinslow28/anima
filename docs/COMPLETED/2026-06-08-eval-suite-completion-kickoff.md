# Kickoff — anima eval-suite completion: review SF03 + G6.9, then plan the path to "done"

*Paste-ready brief for a FRESH Claude Cowork (orient-analyze-decide-stage) session. **SF03** (the proportion gate) and **G6.9's** $0 infra + ratified golden corpus + null-arm machinery are all **MERGED to main and clean**. This session does three things, in order: (1) review the three latest reports and confirm the work is sound, (2) lay out the full plan to finish testing the **Em (T2 vision-critic) eval suite**, (3) tell Sean exactly what's left for the suite to be "complete." The headline of what remains is the **first COSTED measurement of Em's fix-rate** — the constructive axis, the last unmeasured part of what Em is for. **No model spend in this session;** costed runs hand off to Claude Code under fleet-ops.*

**Standing doctrine: verify against the tree, never trust a label — including this brief.** Confirm counts, paths, SHAs, branch state, and every claim below before acting. This arc has had multiple near-misses from a brief asserting a state or code path that didn't hold (the 2026-06-07 run measured nothing because a flag was gated off; the eval foundation was once 19/23 SHA-identical fixtures). Both were caught by verifying first.

## ⚠ FIRST, EVERY SESSION — the divergence + tree check

Run before anything else (a Cowork sandbox usually can't reach GitHub — if `git fetch` fails, the divergence check runs against the *cached* ref; re-run on Sean's machine before any land):

1. `git fetch origin` → `git rev-list --left-right --count main...origin/main` — expect `0 0` (last known clean 2026-06-08, HEAD `af90a99`/#36).
2. `git log --oneline -8` — confirm the merged stack: `af90a99` (#36 planning docs) · `e851a66` (#35 G6.9 Step-3 null-arm machinery) · `6f5ed43` (#34 goldens ratified) · `604b7e6` (#32 G6.9 $0 infra) · `43987df` (#33 SF03 gate).
3. `git status -s` — expect **clean** (everything merged).
4. **Guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` → **`2af75906502f1caf8857e18828ceb2e4`** (the ratified verdict baseline; it moves ONLY via a new replicated run — never by re-score/relabel).
5. `grep -c 'golden_diff_ratified: true' evals/vision_critic/cases.yaml` → **30** (all goldens ratified).
6. `git worktree list` (expect only `main`) + `git branch` — note 3 stale merged branches for cleanup: `g6.9-gate3-costed`, `ratify-g6.9-goldens`, `docs/g6.9-sf03-planning-2026-06-08` (+ remote `feature/em-g6.1-citation-grounding-handoff`).

## Read, in order

**The three reports under review (Sean's ask):**
1. [`docs/anima-test-runs/2026-06-08-sf03-proportion-gate-field-report.md`](anima-test-runs/2026-06-08-sf03-proportion-gate-field-report.md) — SF03 session retrospective: built, probed, Approach A, merged (#33).
2. [`docs/anima-test-runs/2026-06-08-sf03-probe-and-build.md`](anima-test-runs/2026-06-08-sf03-probe-and-build.md) — the probe evidence (4 NB2 plates) + the Approach-A build + the retroactive read.
3. [`docs/2026-06-08-g6.9-gate3-costed-handoff.md`](2026-06-08-g6.9-gate3-costed-handoff.md) — **the pending spend**: the costed Gate 3 fix-rate run spec (null-arm, normalized lift, §0 gates, ~$7.80).

**Context chain (don't re-derive state from older docs):**
4. `PHILOSOPHY.md` — empirical-not-vibes; the human owns taste; critics propose, never decide.
5. `CLAUDE.md` — the **Critic Stack** + the **`vision_critic` — Em row** (canonical state-of-record; carries verdict 0.97/1.00/0.00 + citation 0.97, both ratified) + the **SF03 note** (G6.4 automated 2026-06-08).
6. [`docs/2026-06-08-g6.9-ratification-and-costed-gate3-plan.md`](2026-06-08-g6.9-ratification-and-costed-gate3-plan.md) — the follow-on plan that sequenced Steps 1→3 (Step 3 = the costed run).
7. [`docs/2026-06-04-prompt-diff-eval-design.md`](2026-06-04-prompt-diff-eval-design.md) — the G6.9 design (layered strawman; Gate 1/2/3/4).
8. [`docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md`](research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md) — the eval handbook (error-analysis-first, binary single-axis, ships-red, judge calibration, §3.5 the contact-sheet-can't-see-motion finding, the per-agent eval-strategy matrix).

## Where we are (verify each against the tree)

**SF03 (#33) — DONE, merged, enforcing.** A deterministic, hard, per-character, spec-driven proportion gate at Bible-lock ([`pipeline/agents/proportion_gate.py`](../pipeline/agents/proportion_gate.py)). The make-or-break probe answered **YES** (NB2 honors a heads-tall armature: front 7.12 / profile 7.15 / back 7.05 / ¾ hardened ~7.25); Sean chose **Approach A**. 358 contract + 10 seedance tests green, ~sub-$0.20 spend, verdict baseline + Em surface untouched. **Two open items (no timeline):** (a) re-bake sean-anchor's 5 body turnarounds through the Approach-A feeder + re-lock to certify the `indeterminate` retroactive read (Approach A is *prevention*, not retro-audit — the existing pre-constrained plates can't be deterministically certified); (b) Cy hot-loop auto-wiring (deferred — no current consumer: sean locked, mascot opt-out).

**G6.9 — infra + goldens + null-arm machinery all DONE, merged, $0. The costed fix-rate run is PENDING.**
- #32 `$0` infra (CaseScore.proposed_patches threading, `score.py --dump-patches` §0 pre-flight, `diff_cite_precision_recall`).
- #34 all **30 goldens ratified** (`golden_diff_ratified: true`).
- #35 Step-3 machinery: `_NULL_CLAUSE` placebo, `both+null` arm set, `normalized_lift = (em−null)/(golden−null)` per class — Sean's attribution lock, all $0/stub-green.
- **Not yet run:** the costed Gate 3 baseline. Per the handoff, before spend there is **one $0 wiring step still open** — wrap each case in `score.py`'s subprocess-per-case isolation (`_run_case_subprocess`/`_CASESCORE_SENTINEL`) to dodge the exit-144 interpreter-teardown race from Em's async Opus children (verified: `patch_efficacy.py` only *references* this in a comment, it isn't wired). Then a **~$0.05 §0 capture-proof** (prove live Em emits a non-empty diff on a defect case), then the **~$7.80** `--arm both+null --sample 12 --rerolls 3` run, then report + the **CLAUDE.md Em-row update** (the first state-of-record shift G6.9 produces — the Em row does NOT yet claim fix-rate, correctly).

## The review this session must do (analyze BEFORE planning)

Confirm, against the tree and the reports — don't take them on faith:
- **SF03 is sound, and the `indeterminate` retroactive read is honesty, not a bug.** The gate refuses to certify what it can't measure (pre-constrained plates); that's the correct behavior. Sanity-check: the probe numbers, the bold-anchor + known-division-count fix for the ¾ grid-count drift, the anti-silent-pass guard, mascot opt-out, no hardcoded 1:7.
- **G6.9 machinery is real and the attribution lock is built as designed.** Verify `_ARM_SETS['both+null']`, `_NULL_CLAUSE`, `normalized_lift`; the `--check-only` $0 pre-flight; the exit-4 refusal on unratified/keyed conditions. Confirm the goldens (esp. the 5 view goldens — correct *because* `patch_efficacy` gives view a no-regen/label-side branch; spot-check the `pad3` hair-term and `pad5/pad6` grounding were settled at ratification).
- **The verdict baseline is byte-identical** (md5 above). G6.9 is additive — the second axis of the ruler, never a re-score of the first.
- **The one open wiring step + the §0 capture-proof are real pre-spend gates** — neither was skipped or silently assumed.

## The plan to produce — "what's left to fully complete the Em eval suite"

Validate and sequence this inventory with Sean (recommend a default order; he prioritizes). The three Em axes: **verdict ✅ (G5, ratified) · citation ✅ (G6.1b, ratified) · constructive ❌ (fix-rate, pending)**. To call the suite complete:

**P1 — the costed Gate 3 fix-rate baseline (the headline, closes the constructive axis).** Hand to Claude Code under fleet-ops, in the handoff's order: (1) the $0 subprocess-isolation wiring; (2) `--check-only` $0 pre-flight (prints the ~$7.80 estimate); (3) ~$0.05 §0 capture-proof; (4) the `both+null 12×3` run; (5) dated trace + field report; (6) CLAUDE.md Em-row update. Headline metric = **fix-rate as normalized lift**, per class, with `discriminative` flags where `golden ≈ null`.

**P2 — Gate 2 judge calibration (cheap, separate).** The golden-agreement proxy judge is built but **uncalibrated**; calibrate against a Sean-labeled sample + record the judge-bias ledger (handbook procedure) before the proxy is trusted. Can run alongside P1.

**Accepted-permanent gaps (state them, don't chase):** motion-proper is structurally unscoreable by a still contact sheet (the 6 motion cases ship-red/xfail by design — eval-strategy §3.5); motion-citation handles are low-value.

**Deferred coverage (decide disposition):** the fuller `30×5` Gate 3 run (defer until `12×3` characterizes the floor); the **mascot eval corpus** (Em is only corpus-validated on sean-anchor; the mascot Bible surfaces correctly but has no corpus — plus the cosmetic `IR.sean.*`-example nit in `_criteria_block` to fix during mascot validation); identity-mode corpus extension (hair/jaw/eye).

**SF03 follow-ons (decide whether now):** the 5-body-turnaround re-bake + re-lock to certify the `indeterminate` read (small costed); Cy hot-loop auto-wiring (deferred).

**Housekeeping:** delete the 3 stale merged branches (local + remote).

**Broader horizon (note, scope only if Sean wants it):** beyond Em, the eval handbook's per-agent matrix (Maya planner, Cy character-designer, Mo museum-writer, the T3 council) is the longer eval arc — Em is the most-built.

## The mistake ledger — do not re-learn

- **A brief's "expected outcome" is not a verified code path.** Before any costed run that depends on Em's prompt content or capture, dump/assert under `--stub`/`--check-only` ($0) that the expected blocks/handles/patches are literally present — the 2026-06-07 run burned an N=5 run measuring nothing because a flag was silently off.
- **The verdict baseline moves only via a new replicated run** — never by re-scoring or relabeling. Verify the trace md5 byte-identical before and after.
- **Ships-red is absolute.** No case is relabeled or tuned to flatter Em (`clean-c06` stays red; the 6 motion cases stay red).
- **Verify the data path end-to-end, not just the flag** (does capture survive the N-vote consensus, do the subprocess workers inherit the config, etc.).
- **Fleet-ops or it didn't happen:** subscription SDK (`ANTHROPIC_API_KEY` absent), bounded `GEMINI_API_KEY` from `.env`, one isolated worktree per plan, singleton pre-flight + own-PID, single owner, no `start_new_session` on the costed worker, divergence check before AND after, land via squash PR off `origin/main`, clean teardown. Full protocol: [`docs/fleet-ops-protocol.md`](fleet-ops-protocol.md). Coordinate so only one costed owner acts at a time.

## Deliverables for this session

1. A review verdict on the three reports — is everything sound, with any findings surfaced (not silently accepted).
2. A fully-laid-out, sequenced next-steps plan, with the **costed Gate 3 run confirmed ready** (or refined — e.g., the subprocess-isolation wiring spec'd as its $0 pre-step) and staged as a Claude Code handoff under fleet-ops.
3. The explicit **"what's left to fully complete the Em eval suite"** inventory, with each item's disposition recorded (do-now / defer / accepted-gap).
4. CHANGELOG entry for the planning session; CLAUDE.md only if state-of-record shifts (it won't until the Gate 3 run lands a real fix-rate number).

## Operating rules

- Cowork = orient, analyze, decide, stage. **No model spend.** Costed runs → Claude Code handoff under fleet-ops.
- Sean is ground truth and prioritizer. His authoring/judgment (any golden edits, the SF03 re-bake call) is the only thing on the critical path.
- The verdict + citation baselines are ratified; they move only via new replicated runs.

## The frame to carry in

Em's **verdicts** are production-grade and her **citations** are grounded — two of three axes are measured and strong. The last axis is the thing she's actually *for*: proposing fixes the pipeline can act on. The costed Gate 3 run is how we find out whether her proposals are as trustworthy as her verdicts — and the null-arm attribution means we'll know whether the *instrument itself* can discriminate, not just what number it prints. When it lands, the Em eval suite measures all three axes, and T2 is something the pipeline can act on without a human second-guessing the *why*.
