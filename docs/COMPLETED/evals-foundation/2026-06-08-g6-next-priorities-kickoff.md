# Kickoff — anima G6 next priorities: prompt-diff eval (G6.9) + SF03, post citation-grounding

*2026-06-08. Paste-ready brief for a FRESH Claude Cowork (orient-analyze-decide-stage) session. The citation-grounding arc (G6.1/G6.1b) is **DONE, ratified, and merged to main** — criteria-text grounding is the production default and Em's cites went 0.03 → 0.97 with safety held. This session plans what's left: the prompt-diff eval (Em's last unmeasured production behavior, now unblocked), SF03 in parallel, and the deferred set. Orient, analyze, decide, stage — **no model spend here**; costed runs hand off to Claude Code under fleet-ops.*

**Standing doctrine: verify against the tree, never trust a label — including this brief.** Confirm counts, paths, SHAs, branch state, and every claim below before acting. This arc has had multiple near-misses from work living somewhere a brief didn't account for, and from a brief asserting a code path that didn't hold (the 2026-06-07 run measured nothing because the criteria block was gated off — see the mistake ledger). Both classes were caught by verifying first.

## ⚠ FIRST, EVERY SESSION — the divergence + tree check

Run before anything else:
1. `git fetch origin` (note: a Cowork sandbox often cannot reach GitHub — if fetch fails, the divergence check below runs against the *cached* ref; re-run on Sean's machine before any land).
2. `git rev-list --left-right --count main...origin/main` — expect `0  0` (last known clean 2026-06-08).
3. `git log --oneline -6` — confirm `f6a2e3a` (#29, G6.1/G6.1b ratified) is on main.
4. Search for any in-flight branch/worktree before starting new work: `git worktree list` + `git branch -a`.

## Where we are (verify each against the tree)

- **Citation grounding shipped.** `manifest.yaml` carries `critics.t2.attach_references: false` (reference *images* stay off) and **`critics.t2.attach_criteria_text: true`** (the criteria-TEXT lever, flipped ON in production 2026-06-08). These are decoupled flags — `vision_critic.py::_attach_criteria_text` gates the criteria block independent of images.
- **The ratified baseline (moves ONLY via a new replicated run):** performs n=46, **precision 0.97 / recall 1.00 / false_pass 0.00 / cites-correct 0.97**, N=5 majority, criteria-text ON / images OFF, gemini-3.5-flash pinned. Verified real (not a block-dump artifact — cites are class-coherent, max 5 per flagged case; the expected handle is grounded, not echoed). The void G5 numbers (0.62/1.00/0.15) and the blind control (0.94/0.27) are retired.
- **Bible:** sean-anchor `acceptance_criteria.json` = 31 IR rules, content_version 1.3.0, locked. Includes the 9 G6.1 geometry rules (5 `IR.sean.view.*` + 4 `IR.sean.anatomy.*`) + the scoped conditional `IR.sean.prop.stylus-right-hand-always`. `view` is in `criteria.py::VALID_IR_CATEGORIES`.
- **Mascot spot-check done ($0):** the 25-rule claude-mascot Bible surfaces correctly through the same criteria block at phase 5/6 (no image, no wrong-character rule leak). **Known cosmetic nit:** the criteria-block instruction in `_criteria_block` hardcodes an `IR.sean.*` *example* string that shows even on non-sean frames — deferred to mascot validation. Mascot is **not yet corpus-validated** (eval corpus still deferred).
- **Corpus:** 52 cases / 46 fixtures, contamination-guarded (`tests/test_fixture_contamination.py`).
- **The CLAUDE.md `vision_critic` — Em row is the state-of-record** and already carries all of the above (G6.1/G6.1b ratified). Read it; do not re-derive state from older docs.

## Read, in order (the context chain)

1. `PHILOSOPHY.md` — empirical-not-vibes; the human owns taste; critics propose, never decide.
2. `CLAUDE.md` — the **Critic Stack** section + the **`vision_critic` — Em row** (the canonical state-of-record; it carries the ratified G6.1b baseline, the production flip, the mascot spot-check, and the deferred set).
3. `CHANGELOG.md` — top entries: 2026-06-08 G6.1b ratification; the G6.1 scoped/staged + run entries; the references re-test adoption. (Note: a Reve-vs-NB2 editing bake-off also landed 2026-06-07 (#30, verdict: Reve FAILS) — unrelated to Em, just don't be confused by it in the log.)
4. `docs/anima-test-runs/2026-06-08-em-g6.1b-criteria-attached-run.md` — **the run that closed citation grounding (Outcome A). The core input.** Both axes per-class, the clean-c01 resolution, partial-credit moot.
5. `docs/anima-test-runs/2026-06-07-em-g6.1-rebaseline.md` — the blind control + the discovery that the criteria block was gated off (why a run can measure nothing).
6. `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` — the full 52-case × 5-run matrix + per-case actual_cites (the grounding evidence).
7. `docs/2026-06-04-prompt-diff-eval-design.md` — **the draft design for G6.9 (this session's headline). Its hard dependency — citation grounding — is now CLEARED.**
8. `docs/2026-06-04-sf03-proportion-gate-build-handoff.md` + `docs/2026-06-03-sf03-proportion-gate-design.md` — the parallel, ready-to-run SF03 build (generation-time; never touches Em).
9. `docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md` — **the eval handbook. Keep it obeyed** (error-analysis-first, binary single-axis, ships-red, judge calibration; §3.5 the contact-sheet-can't-see-motion finding; the per-agent eval-strategy matrix).
10. `docs/2026-06-07-em-g6.1b-criteria-text-decoupling-handoff.md` — the handoff that just shipped; read it for the §0 pre-flight-prompt-inspection gate pattern (reuse it for any future run that changes Em's input surface).

## The mistake ledger — what this arc learned at cost (do not re-learn)

- **A brief's "expected outcome" is not a verified code path.** The 2026-06-07 run was designed to measure the Bible/surfacing work, but the criteria block was gated behind `attach_references` (off) — so it measured nothing and burned a costed N=5 run. **Fix that became standing practice: the §0 pre-flight gate** — before any costed run that depends on Em's prompt content, dump the built prompt under `--stub` (`--dump-prompt`) and assert the expected block/handles are literally present (and images absent), $0, before spending.
- **The baseline moves only via a new replicated run** — never by re-scoring or relabeling. Verify the ratified trace byte-identical (md5) before and after every run.
- **Ships-red is absolute.** No case is ever relabeled or tuned to flatter Em. `clean-c06` stays red (a real facing-convention disagreement). A clean case passing must be the *image* honoring the rule, never a relabel.
- **Citation scoring is citation-RECALL, not precision.** The scorer credits a case if the expected handle is *among* Em's cites; it does not penalize extra/irrelevant cites. This was fine for verdict grounding, but **G6.9 must decide whether prompt-diff grounding needs cite-precision** (a diff citing 5 rules incl. 2 irrelevant ones is weaker than one citing the 1 right rule). Flagged as a G6.9 design input.
- **Verify the data path end-to-end before a run, not just the flag.** For G6.1b the checks that mattered were: does the manifest load the Bible into `ctx.criteria`, does the phase filter (`query_by_phase`) return the rules (they need `cites_phase` tags), does the flag propagate to subprocess workers. Any one silently false → a wasted run.
- **Fleet-ops or it didn't happen:** subscription SDK (`ANTHROPIC_API_KEY` absent), bounded `GEMINI_API_KEY` from `.env`, one isolated worktree per plan, singleton pre-flight + own-PID, single owner, no `start_new_session` on the costed worker, divergence check before AND after, land via squash PR off `origin/main`, clean teardown. Full protocol: `docs/fleet-ops-protocol.md`.

## What this session does — plan the remaining priorities, gate by gate

Propose to Sean; he prioritizes. Use structured questions, batch sensibly, recommend a default. Recommended order:

### P1 (headline) — G6.9: evaluate Em's prompt diffs (her actual production job)

"Flags correctly" is now measured and strong (0.97/1.00/0.00). "Proposes a fix that helps" has **zero** eval coverage — and per the Critic Stack, T2's contract is *"proposes prompt diffs, not pass/fail."* The hard dependency (cites-correct at 0.03) that blocked diff-grounding measurement is now **resolved (0.97)**, so this is unblocked and is the last unmeasured part of what Em is for.

Re-read `docs/2026-06-04-prompt-diff-eval-design.md` **in light of G6.1b being done**, then scope it with Sean, gate by gate. The decisions to drive (the draft's open questions, now answerable):
1. **Design shape.** Draft proposes: Design 2 (golden-diff agreement) as the fast per-case gate + Design 1 (Outcome A/B: apply diff → re-generate → re-critique, empirical) as periodic validation + Design 3 (judge rubric) as triage only. Confirm or revise.
2. **Golden-diff authoring** (the critical path, like the P-B1/PA-D4 re-rolls were): does each defect case gain a `golden_diff` field Sean authors? That's ~30 reference fixes — his authoring, his call.
3. **Design 1 spend** as a *periodic* (not per-run) empirical validation — acceptable cost? It's ~1 NB2 generation + 1 Em call × sampled cases × N re-rolls.
4. **Patch scope** — score only `prompt` diffs, or all of Em's patch targets (manifest fields, criteria-cited mutations)?
5. **Cite-precision** (the new input from the trace review): should diff grounding score cite-precision, not just the recall the verdict scorer uses?

**Verify before speccing any run:** does the eval harness currently persist Em's `proposed_patches` (it persists cites + reasoning since the mini-run instrumentation; patches may need wiring)? Check `pipeline/agents/patch_stager.py`, the `patches list` CLI, and `score.py`. A diff eval needs the diffs captured first. Stage the chosen design as a Claude Code handoff (or, if a measurement run is involved, gate it behind a §0-style pre-flight that proves the patches are captured).

### P2 (parallel, ready now) — SF03 proportion-gate build

`docs/2026-06-04-sf03-proportion-gate-build-handoff.md` is ready to hand to Claude Code **any time** — it's generation-time (Cy Pass-3 / Bible-lock), independent of Em, references, and citation work, so it never touches Em's surface and has no re-baseline interaction. It can run concurrently with G6.9 (different worktree, single owner each). It also retroactively re-verifies the 1:7 Bible re-lock. Confirm it's still ready and, if Sean wants parallelism, hand it off.

### Deferred / backlog (record decisions; most are not now)

- **References-images path is now largely moot for grounding.** criteria-TEXT delivered the grounding (0.97) that reference-IMAGES were meant to provide — without the precision regression (images cost 0.85; text holds 0.97). What images would still add is *visual identity-drift* detection, a different axis that is SF03/DINOv2 territory. **So DINOv2's case is weaker, not stronger.** Recommend folding the formal references/DINOv2 call into the post-SF03 decision, and not treating references re-open as live.
- **Motion-citation gap** (newly visible in the G6.1b trace): motion cases cite wrong handles because `motion.no-foot-skating` / `motion.no-temporal-flicker` etc. are not IR rules (the same gap view/anatomy had pre-G6.1). But motion-proper is structurally unscoreable by a still-image contact sheet, so authoring motion citation handles is **low-value — log it, don't chase it.**
- **Identity modes (hair/jaw/eye)** — promotion trigger met long ago, consciously deferred each session. Extend the corpus or re-defer.
- **Mascot corpus** — needs its own turnaround-sheet-based fixtures; spec after the Sean corpus pattern (now proven). Plus the cosmetic `IR.sean.*`-example nit in `_criteria_block` to fix during mascot validation.
- **Minor:** Em occasionally cites honored rules on a *pass* verdict (e.g. clean-c04 cited 7 on a pass) despite the block's "a rule the frame honors is not a citation" instruction — n/a to the metric, prompt-adherence polish only.

## Deliverables for this session

1. A G6.9 design scoped gate-by-gate with Sean, staged as a Claude Code handoff under fleet-ops (with the data-path + §0 pre-flight checks baked in if it involves a costed run).
2. SF03 confirmed ready (and handed off if Sean wants parallel execution).
3. The strategic calls recorded: references/DINOv2 folded into post-SF03; the deferred set's dispositions.
4. CHANGELOG entry for the planning session; CLAUDE.md only if state-of-record shifts.

## Operating rules

- Cowork = orient, analyze, decide, stage. **No model spend.** Costed runs → Claude Code handoff under `docs/fleet-ops-protocol.md`.
- The baseline is ratified; it moves only via a new replicated run.
- Sean is ground truth and prioritizer. His authoring (golden diffs, any re-rolls) is the only thing on the critical path. Ships-red holds — no case tuned to flatter Em, ever.
- Any run that changes Em's input surface gets a §0 pre-flight prompt-inspection gate ($0) before it spends.

## The frame to carry in

Em's *verdicts* are production-grade and her *citations* are now grounded — the two things the eval suite measures are both strong. What's left is the thing she's actually *for*: proposing fixes the pipeline can act on. G6.9 is how we find out whether her proposals are as trustworthy as her verdicts. When it lands, T2 is something the pipeline can act on without a human second-guessing the *why* — which was the whole point of the arc.
