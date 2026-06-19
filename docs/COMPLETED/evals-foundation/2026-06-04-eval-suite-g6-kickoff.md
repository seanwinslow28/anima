# Kickoff — Eval suite G6: from trustworthy baseline to production-ready critic

*2026-06-04. A paste-ready brief for a FRESH Claude Cowork (orient-and-decide) session. The eval-foundation reset is complete and the G5 re-baseline is ratified (performs 0.97 / 1.00 / 0.00 — replacing the void 0.62/1.00/0.15). This session analyzes where the suite actually stands, what G5 surfaced, and lays out the prioritized path to "ready to roll and as accurate as we can get it." Orient, analyze, decide, stage — no model spend here; costed work hands off to Claude Code under fleet-ops discipline.*

**Standing doctrine: verify against the tree, never trust a label — including this brief.** Confirm counts, paths, branch state, and every claim below before acting.

---

## ⚠ BLOCKING FIRST TASK — finish the branch integration

As of this brief's writing, **main does NOT carry the G5 work.** The integration merge ran the wrong direction (`main → eval/em-rebaseline-g5`, commit `57f6384` — the branch caught up with main; main never received the branch). Verify, then fix:

1. Check: `git log main..eval/em-rebaseline-g5 --oneline` — if it lists commits (`b7323e3` G1–G4 corpus + Bible re-lock, `71f8d80` cost-leak fix, `d81546c` G5 run, `9bd3986` baseline ratification), main is stale.
2. Land it: merge `eval/em-rebaseline-g5` into `main` (should be clean — the branch already absorbed main), push, then clean-teardown the worktree at `.claude/worktrees/eval+em-rebaseline-g5/` per `docs/fleet-ops-protocol.md`.
3. Post-merge sanity (all on main): `evals/vision_critic/cases.yaml` header says "v2: the ratified class-isolated corpus" with 50 cases; `fixtures/frames/` has 44 JPEGs; `characters/sean-anchor/turnarounds/body-3quarter.png` is the small ~220×660 region crop (not 655×1110 — that's the drifted plate); `docs/anima-test-runs/2026-06-04-em-rebaseline-g5-field-report.md` exists; `python -m pytest tests/ -q` green (includes the contamination guard); `python -m pytest evals/vision_critic/runner.py -q` green.

Do not start the analysis below until main is the single source of truth again.

---

## Read, in order (the context chain)

1. `PHILOSOPHY.md` — empirical-not-vibes; the human owns taste; critics propose, never decide.
2. `CLAUDE.md` — Critic Stack section (carries the ratified G5 baseline + layer-ownership map post-merge) and Em's Skills Map row.
3. `docs/2026-06-03-eval-foundation-reset-plan.md` — the G1–G6 gate ladder this arc executes. G1–G5 are DONE; this session opens G6.
4. `docs/anima-test-runs/2026-06-04-em-rebaseline-g5-field-report.md` — **the new baseline + its six findings. The core input to this session.**
5. `evals/vision_critic/last-run.md` + `evals/vision_critic/traces/baseline-2026-06-04-scored.md` — the full 50-case × 5-run verdict matrix (flips, errored case-runs).
6. `docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md` — the eval handbook (error-analysis-first, binary single-axis, ships-red, judge calibration). Keep it obeyed.
7. The mistake ledger — what previous arcs taught, so nothing gets re-learned at cost:
   - `docs/anima-test-runs/2026-06-02-em-gemini-transport-rebaseline-postmortem.md` (scorer replication, 429 walls, partial-N is not a baseline)
   - `docs/anima-test-runs/2026-06-02-em-reference-images-field-report.md` (reference confabulation regression — why `attach_references` is off)
   - the DINOv2 NO-GO spike + `docs/2026-06-03-sf03-proportion-gate-design.md` (parked SF03 design; embeddings see identity, not geometry)
   - the 2026-06-02 model-provenance forensics (never call a CLI without pinning the model; read the served model back)
   - CHANGELOG 2026-06-04: the runner.py "mocked" pre-flight that fired real costed calls (mock every transport, verify $0 before trusting a "free" path)
8. `prompts/eval-corpus/sean-anchor-fixture-corpus.md` — the corpus spec (v2 grammar, pairs, the two pending re-roll slots).

## Where we are (verify each)

- **Baseline (ratified):** performs precision 0.97 / recall 1.00 / false_pass 0.00, N=5 majority vote, reference-blind, pinned gemini-3.5-flash. Stable: worst single-run performs false_pass 0.04. **Verdict baseline, not citation baseline.**
- **Corpus:** 50 cases — 16 clean + 28 single-axis (six ratified classes, paired, Sean-ratified 2026-06-03) + 6 motion_proper ships-red. 44 independent fixtures, contamination-guarded by `tests/test_fixture_contamination.py`.
- **Bible:** sean-anchor body turnarounds re-locked at 1:7 from the gold-standard sheet (human gate stood in for SF03; SF03 re-verifies retroactively once built).
- **Known open wounds from G5 (the six findings, condensed):** cites-correct = 0.03 (geometry classes structurally can't cite — their seam handles aren't IR rules; style classes possibly genuinely mis-citing — needs instrumented per-case inspection); `clean-c06` consistent false-positive (all 5 runs — real disagreement, uninvestigated); 3/250 case-runs errored on the empty-cites production invariant (a safety rule eating eval signal); motion 5/6 caught via spatial traces (`motion-t2-arc` is the true temporal blind spot); 7/50 cases flip across runs (majority-resolved).

## What this session does

1. **Integration first** (the blocking task above).
2. **State-of-the-suite analysis.** Read the full verdict matrix and the six findings against the eval handbook. Tell Sean plainly: what does this suite now measure well, what does it measure badly, and what doesn't it measure at all? (Verdicts: strong. Citations: broken/unmeasured. Motion-temporal: structurally blind. Per-class n: 4–5, adequate but thin. Single labeler, no inter-rater check. Em's *proposed prompt diffs* — her actual production job per the Critic Stack — entirely unevaluated.)
3. **Build the G6 roadmap with Sean** — propose, he prioritizes. The candidate workstreams, roughly in dependency order:
   - **Citation grounding decision** (the headline G5 finding): give the geometry classes real citeable IR criteria, or split verdict-vs-citation scoring in the eval (and fix the empty-cites invariant eating geometry verdicts in production). This decision shapes everything downstream — a critic that proposes fixes is only as useful as its grounding.
   - **Instrumented mini-run** (cheap, ~50 calls): persist Em's per-case cites + reasoning to (a) settle whether style-class citing is genuinely broken or scoring-artifact, and (b) read her actual reasoning on `clean-c06`. Stage as a Claude Code handoff.
   - **Corpus completion:** Sean re-rolls P-B1 (~6.5-head true borderline) and PA-D4 (no rendered text) in Flow → ratify → two added cases (no re-baseline needed).
   - **SF03 proportion-gate build** (Approach A armature probe → A or B fallback) — the parked design; retroactively re-verifies the 1:7 re-lock.
   - **References re-test on the clean corpus** — the 2026-06-02 regression is now explained (contaminated fixtures = confabulation trap by construction). Re-test `attach_references: true` against this corpus; the flag flip remains gated on clearing the false-pass gate (decide whether DINOv2 is still a prerequisite or the clean corpus alone justifies the re-test).
   - **DINOv2 deterministic backstop** — still wanted, or superseded by SF03 + clean references? Make the call explicit.
   - **Deferred identity modes** (hair/jaw/eye) — promotion trigger is MET (six-class corpus clean + re-baselined). Extend the corpus or consciously re-defer.
   - **Mascot corpus** — needs its own turnaround sheet first; spec after the Sean corpus pattern proves out.
   - **Citation/judge calibration + Em's prompt-diff evaluation** — the unevaluated production behavior; design how to score "proposes useful fixes," not just "flags correctly."
4. **Stage the chosen next moves** as Claude Code handoff briefs (costed) or do them here (uncosted), per Sean's prioritization.
5. **Maintenance:** CHANGELOG entry per change; CLAUDE.md only if source-of-truth state shifts. Archive the spent kickoff briefs (2026-06-03 reset kickoff, 2026-06-04 integration kickoff) to `docs/COMPLETED/` via `git mv` if Sean wants the root tidy.

## Sean's role

He is the ground truth and the prioritizer. The roadmap is proposed to him gate by gate (use structured questions, batch sensibly, recommend a default). His re-rolls (P-B1, PA-D4) are the only authoring on the critical path. Labels are his; ships-red discipline holds — no case gets tuned to flatter Em, ever.

## Operating rules

- Cowork = orient, analyze, decide, stage. **No model spend.** Costed runs hand off to Claude Code under `docs/fleet-ops-protocol.md` (subscription SDK, `ANTHROPIC_API_KEY` absent, bounded `GEMINI_API_KEY`, isolated worktree, single owner, clean teardown — and merge the branch INTO MAIN when done; the G5 arc's near-miss was integrating the wrong direction).
- Verify against the tree; never trust a label — file counts, SHAs, model IDs, branch states, this brief.
- The baseline is ratified; it moves only via a new replicated run, never by re-scoring or relabeling against it.

## The frame to carry in

The reset made the ruler real: every number is now about the critic, not the fixtures. G5 proved Em's *verdicts* are production-grade reference-blind. What's left is making her *reasons* as trustworthy as her verdicts (citation grounding), closing the geometry gate at the source (SF03), finishing the corpus's edges (re-rolls, identity modes, mascot), and evaluating the thing she's actually for — proposing fixes. When this arc ends, the critic stack's T2 should be something the pipeline can act on without a human second-guessing the *why*.
