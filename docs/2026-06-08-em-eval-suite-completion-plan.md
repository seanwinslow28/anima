# Plan — completing the Em (T2 vision-critic) eval suite: review + the path to "done"

*2026-06-08. Cowork session (orient → analyze → decide → stage). **No model spend.** Reviews the three latest reports (SF03 + G6.9 Gate-3 handoff), confirms the merged work against the git tree, and lays out exactly what remains for the Em eval suite to measure all three of Em's axes. Costed work hands to Claude Code under [`docs/fleet-ops-protocol.md`](fleet-ops-protocol.md). Sequenced from the [G6.9 ratification + costed-Gate-3 plan](COMPLETED/2026-06-08-g6.9-ratification-and-costed-gate3-plan.md) and the [Gate-3 costed handoff](OLD/2026-06-08-g6.9-gate3-costed-handoff.md).*

**Standing doctrine: verify against the tree, never trust a label — including this plan.**

---

## 0. Verification verdict — everything in the kickoff brief holds against the tree

Re-checked every claim against the git object store and re-ran the relevant machinery ($0, credential-free). **Accurate on every material point:**

- **Divergence + stack.** `main...origin/main` = `0 0` (against the cached ref — the sandbox can't reach GitHub, as expected). The merged five-commit stack is exact: `af90a99`(#36) · `e851a66`(#35) · `6f5ed43`(#34) · `604b7e6`(#32) · `43987df`(#33). `git status` clean but for the untracked kickoff doc.
- **Verdict-baseline guard.** `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` md5 = **`2af75906502f1caf8857e18828ceb2e4`** (byte-identical). Last commit to touch it = `f6a2e3a`(#29, the G6.1b ratification) — **none** of the five SF03/G6.9 commits went near it. G6.9 is additive, confirmed.
- **Goldens.** `grep -c 'golden_diff_ratified: true' cases.yaml` = **30**.
- **Branches.** Three stale merged locals confirmed present for cleanup (`g6.9-gate3-costed`, `ratify-g6.9-goldens`, `docs/g6.9-sf03-planning-2026-06-08`) + the remote `feature/em-g6.1-citation-grounding-handoff`. Only `main` is a worktree.
- **SF03 (`pipeline/agents/proportion_gate.py`, 565 lines).** No hardcoded 1:7 (spec-driven `head_to_body_target`, `round(target)` only as the armature-division fallback); `_BLOCKING_VERDICTS = {fail, indeterminate, error}` (so `indeterminate` blocks the lock); anti-silent-pass guard present (“body plates present with no numeric spec → BLOCK”); mascot `opt_out` path clean.
- **G6.9 (`evals/vision_critic/patch_efficacy.py`, 573 lines).** `_NULL_CLAUSE = "with a calm, evenly-lit, neutral background"` (exact); `_ARM_SETS['both+null'] = ("em","golden","null")`, default `both+null`; `normalized_lift` reports per-class em/golden/null + `lift=(em−null)/(golden−null)` + `discriminative:false` when `golden≈null`; live `preflight` refuses a set `ANTHROPIC_API_KEY` and any unratified sampled golden; `--check-only` raises `SystemExit(4)` on failure and prints the estimate.
- **The cost number is real.** `estimate_cost(12, rerolls=3, both+null)` = **$7.80** (nb2=90, em=120 incl. 12 captures, @ $0.02/nb2 + $0.05/em). Matches the handoff exactly.
- **The one open wiring step is genuinely open.** In `patch_efficacy.py`, subprocess-per-case isolation exists **only as a comment** (line 25) — never imported, never called; the live loop runs `run_case(...)` in-process, and the live branch is explicitly marked “Deferred this push — see module COSTED-RUN NOTE.” The reusable pattern (`_run_case_subprocess` / `_CASESCORE_SENTINEL`) lives in `score.py`. **Real pre-spend gate, not skipped.**
- **The §0 capture-proof is real.** `score.py --dump-patches` captures `proposed_patches`, asserts non-empty for a flagged case, and exits — the $0 gate that kills the 2026-06-07 “measured nothing” failure mode.
- **Green.** `patch_efficacy --arm both+null --sample 12 --rerolls 3 --stub` → PREFLIGHT OK + valid lift JSON. The six G6.9 + SF03 machinery test files = **83 passed** (credential-free).

## 1. Review of the three reports — sound, with findings surfaced (not silently accepted)

**SF03 field report + probe-and-build → SOUND.** The two reports are mutually consistent on every number (probe: front 7.12 / profile 7.15 / back 7.05 / ¾ 8.29→~7.25). The load-bearing claim — **Approach A is *prevention*, not retro-audit; `indeterminate` is honesty, not a bug** — is correct and matches the code (`_BLOCKING_VERDICTS` includes `indeterminate`; the gate refuses to certify pre-constrained plates it cannot measure). The ¾ grid-count fix (anchor on bold crown/feet + *known* division count, never NB2’s redrawn interior line count) is the right call and is what shipped. Anti-silent-pass guard, mascot opt-out, and no-hardcoded-1:7 all verified. **Surfaced (not a defect):** sean-anchor’s locked body turnarounds read `indeterminate` retroactively — correct behavior, but it means the suite has **zero deterministic certification** of the one locked human character’s proportions until the five are re-baked constrained. Disposition below.

**G6.9 Gate-3 costed handoff → SOUND and READY.** The attribution lock is built as designed (null/placebo arm, normalized lift, per-class discriminative flag). The §0 gates assert before they spend. The hard prerequisites (ratified goldens, `GEMINI_API_KEY` present, `ANTHROPIC_API_KEY` absent, single costed owner) are all real and enforced in `preflight`. **One refinement** (not a flaw): the handoff buries the subprocess-isolation hardening inside §3 (“do before launching”). It should be elevated to a discrete **$0 pre-step ahead of `--check-only`**, because it’s a code change that must land + be tested green before any spend is even estimated. Spec’d in §3 below.

**Net:** all three reports are accurate, the merged work is sound, and the costed run is ready to hand off once the one $0 wiring step lands.

## 2. The completion frame — Em has three axes; two are measured

| Axis | What it asks | Status | Source |
|---|---|---|---|
| **Verdict** | Does Em flag the right defect? | ✅ **0.97 / 1.00 / 0.00**, ratified | G5, blind baseline `traces/baseline-2026-06-04-scored.md` |
| **Citation** | Does she cite the real `IR.*` handle? | ✅ **cites-correct 0.97**, ratified | G6.1b, `traces/g6.1b-criteria-attached-2026-06-08.md` |
| **Constructive** | Does applying her proposed fix actually clear the defect (identity held)? | ❌ **unmeasured** — the headline that remains | G6.9 Gate 3 (pending spend) |

The constructive axis is *what Em is for*. Closing it is the suite’s completion headline.

## 3. The plan — sequenced, with a recommended default order (Sean prioritizes)

### P1 — the costed Gate 3 fix-rate baseline (the headline; closes the constructive axis)
Hand to Claude Code under fleet-ops, in this order:

1. **(NEW — $0 code) Subprocess-per-case isolation in `patch_efficacy.py`.** Wrap each live `run_case(...)` in `score.py`’s `_run_case_subprocess` / `_CASESCORE_SENTINEL` pattern so Em’s async Opus children can’t trigger the exit-144 interpreter-teardown race. Land + test green **before** any estimate. This is the “one wiring step left” the handoff names — promoted to step 1 because it’s a code change, not a launch checklist item.
2. **($0) `--check-only` pre-flight.** `patch_efficacy --arm both+null --sample 12 --rerolls 3 --check-only` → must print `PREFLIGHT OK` + the **$7.80** estimate (asserts ratified goldens, `GEMINI_API_KEY` present, `ANTHROPIC_API_KEY` unset, every clean-pair splice well-formed). No `PREFLIGHT OK` → stop.
3. **(~$0.05) §0 capture-proof.** `score.py --only palette-pad2-red-shirt --dump-patches` (LIVE Em, no `--stub`) → assert non-empty `proposed_patches` with a clause-like `value` and a real `IR.sean.*` cite. Empty → Em proposes nothing on this corpus → **stop and surface** (don’t spend $7.80 to measure nothing).
4. **(~$7.80) the run.** `patch_efficacy --arm both+null --sample 12 --rerolls 3 > runs/gate3-baseline.json`. Record the estimate in the field report *before* launching.
5. **($0) report.** Dated trace under `evals/vision_critic/traces/` + field report `docs/anima-test-runs/2026-06-XX-em-g6.9-gate3-fixrate.md`: §0 evidence, estimate-vs-actual, per-class null/em/golden bands + `normalized_lift`, proposal-rate, discriminative-power findings. **Headline = fix-rate as normalized lift, per class, with `discriminative:false` where golden ≈ null.**
6. **($0) state-of-record.** Update the **CLAUDE.md Em row** — the first shift G6.9 produces (the row does *not* yet claim a fix-rate, correctly).

### P2 — Gate 2 judge calibration (cheap; can run alongside P1)
The golden-agreement proxy judge (`diff_eval.py`) is **built but uncalibrated**. Dry-read `diff_eval --check-only` ($0), then calibrate against a Sean-labeled sample and record the judge-bias ledger (handbook procedure) before the per-run proxy is trusted. Gate 3 (P1) does **not** depend on it — it’s the cheap signal tracked between costed runs. Independent of P1; parallelizable.

## 4. “What’s left to fully complete the Em eval suite” — inventory with dispositions

| # | Item | Disposition | Note |
|---|---|---|---|
| 1 | **Gate 3 fix-rate baseline (`both+null 12×3`)** | **DO NOW (P1)** | The headline. Closes the constructive axis. Costed (~$7.85 incl. capture-proof), fleet-ops handoff. |
| 2 | **Subprocess-isolation wiring** | **DO NOW (P1 step 1, $0)** | Hard pre-req for #1. Code + test, no spend. |
| 3 | **Gate 2 judge calibration** | **DO NOW / parallel (P2, cheap)** | Makes the cheap per-run proxy trustworthy. Not on #1’s critical path. |
| 4 | **motion-proper (6 cases)** | **ACCEPTED GAP** | Structurally unscoreable by a still contact sheet (eval-strategy §3.5). Ships-red / xfail by design — do not chase. |
| 5 | **motion-citation handles** | **ACCEPTED GAP** | Low-value; not worth authoring. |
| 6 | **Fuller `30×5` Gate 3 run** | **DEFER** | Until `12×3` characterizes the floor + which classes are discriminative. |
| 7 | **Mascot eval corpus** | **DEFER** | Em is corpus-validated only on sean-anchor. The mascot Bible surfaces correctly through `_criteria_block` but has no corpus. Fold in the cosmetic `IR.sean.*`-example nit in `_criteria_block` when mascot validation happens. |
| 8 | **Identity-mode corpus (hair/jaw/eye)** | **DEFER** | Consciously re-deferred at G6; a later coverage extension. |
| 9 | **SF03 sean-anchor re-bake + re-lock** | **DECIDED — bundle with next heads-tall authoring** (Sean, 2026-06-08) | Converts the `indeterminate` retroactive read into a certified pass. No standalone costed run; the re-bake rides the next authoring session that already spins up the Approach-A feeder. Recorded in the CLAUDE.md SF03 "Open:" note as the trigger. |
| 10 | **Cy hot-loop SF03 auto-wiring** | **DEFER** | No current consumer (sean locked, mascot opt-out). Primitives + probe are the reference impl. |
| 11 | **Delete 3 stale merged branches** | **DO NOW ($0, Sean’s machine)** | `g6.9-gate3-costed`, `ratify-g6.9-goldens`, `docs/g6.9-sf03-planning-2026-06-08` (+ remote `feature/em-g6.1-citation-grounding-handoff`). |

**Suite is “complete” when:** items 1–3 land green and the CLAUDE.md Em row carries a measured fix-rate. Items 4–5 are permanent accepted gaps; 6–10 are coverage/robustness extensions outside the “all three axes measured” bar.

**Broader horizon (note only):** beyond Em, the eval handbook’s per-agent matrix (Maya planner, Cy character-designer, Mo museum-writer, the T3 council) is the longer eval arc. Em is the most-built — out of scope here.

## 5. Handoff status

The Gate-3 costed handoff [`docs/OLD/2026-06-08-g6.9-gate3-costed-handoff.md`](OLD/2026-06-08-g6.9-gate3-costed-handoff.md) is **verified ready as written**, with one refinement folded into §3 above: promote the subprocess-isolation wiring to an explicit $0 step-1 (ahead of `--check-only`). No other change needed — the §0 gates, the cost table, the arm config, and the out-of-scope list all hold against the code.

## 6. The mistake ledger we’re honoring

- A brief’s “expected outcome” is not a verified code path — every claim above was dumped/asserted under `--stub`/`--check-only` / direct source read ($0). The 2026-06-07 N=5 run measured nothing because a flag was silently off; the §0 capture-proof exists to kill that.
- The verdict baseline moves **only** via a new replicated run — md5 confirmed byte-identical before this session, and G6.9 never touches it.
- Ships-red is absolute: `clean-c06` and the 6 motion cases stay red. No case is relabeled to flatter Em.
- Fleet-ops or it didn’t happen: subscription SDK (`ANTHROPIC_API_KEY` absent), bounded `GEMINI_API_KEY`, one isolated worktree, single costed owner, divergence check before AND after, squash-PR off `origin/main`, clean teardown.

## Guard

The verdict baseline `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` (`md5 2af75906502f1caf8857e18828ceb2e4`) stays byte-identical through all of P1/P2. G6.9 is additive — the second axis of the ruler, never a re-score of the first.
