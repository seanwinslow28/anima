# Continuation prompt — Em re-baseline aftermath: decide the next steps

> Paste the block below `─── PROMPT ───` into a fresh **Cowork** session opened on the `anima` project.
> This session **orients and decides** — it reads the arc, walks Sean through the open calls, and produces a plan/kickoff. It does **not** itself run costed builds or evals (that gets handed to Claude Code, the way the transport session was). Operator notes above the line are for Sean.

**Why this session exists:** the Em reference-grounding re-baseline finally ran (via a Gemini-API transport, off the quota-walled agy CLI) and produced two hard results: (1) a **validity gate caught that the whole T2 eval program had been mismeasured** — agy's headless `-p` mode silently ran `gemini-3.5-flash`, never the `gemini-3.1-pro` every doc claimed; and (2) the references change — the *locked #1 fix*, shipped in PR #13 — **regressed the safety metric** (false_pass 0.00 → 0.15) and was **eval-blocked**. The postmortem ends with six "How to proceed" items and one decision it deliberately did not make. This session makes them.

**Git state the new session must reconcile first (verified 2026-06-02):** the transport work + postmortem are in **PR #15 (`b30039b`)** on branch `eval/em-rebaseline` (and a `docs/em-rebaseline-postmortem` branch). The local checkout may still be on `ops/operational-incidents-remediation` @ `c6a2aed`, which lacks `gemini_api_runner.py` and the postmortem. There's also a stale, prunable worktree at `.claude/worktrees/em-rebaseline`. Sort out what's actually merged into `main` before reading code, and clean the worktree/branches per the fleet-ops teardown rule.

---

─── PROMPT ───

We're resuming anima's agent-fleet work. The Em (T2 vision critic) reference-grounding re-baseline ran and produced two consequential results — a mismeasured-baseline discovery and an eval-blocked "obvious" change. Your job this session is to get fully oriented from the files below, then **help me decide and sequence the next steps** — not to run anything costed. End by drafting a plan/kickoff I can hand to Claude Code.

**READ FIRST, in this order (each carries verified state — don't skip):**

*The anchor — what just happened:*
1. `docs/anima-test-runs/2026-06-02-em-gemini-transport-rebaseline-postmortem.md` — THE session being continued: the transport pivot, the Flash-not-Pro provenance discovery, the false-pass regression that blocked the references change, the diagnosis (Opus variance + confabulation + the prompt-ablation), and its six-item "How to proceed."

*Project canon (the soul + the architecture):*
2. `PHILOSOPHY.md` — read before the architecture; "empirical, not vibes" is the belief this whole episode vindicates.
3. `CLAUDE.md` — the project manual; note the current Em row + the Critic Stack (T1/T2/T3) + the Character Bible primitive.
4. `docs/pipeline-architecture-v1.md` — the canonical 10-phase lock + critic-checkpoint placement.

*The eval handbook (the ruler the fleet is held to):*
5. `docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md` — false-pass-first for critics (§4), the vision-judge limits + "MLLMs pass shuffled frames" (§3.5), the corrected judge-bias ledger (§3.3), the per-agent eval-strategy matrix. The methodological basis for every read in the postmortem.

*Where the agent fleet came from (so the next move respects the original intent):*
6. `docs/2026-05-24-pipeline-v2-brainstorm.md` — the 15-idea PM/Designer/Engineer brainstorm that produced the v2 architecture (read for *why*).
7. `docs/2026-05-25-agent-fleet-brainstorm.md` and `docs/2026-05-26-agent-fleet-brainstorm-v2.md` — the documents that scoped the named-agent crew (Maya/Cy/Em/Mo/...).
8. `docs/2026-05-31-critic-spine-hardening-kickoff.md` — the program this Em work lives inside; its Phase 0/1/2 disciplines are what produced the scored baseline.

*The Em arc + the comparison case + the standing discipline (previous postmortems):*
9. `docs/anima-test-runs/2026-06-01-em-critic-spine-hardening-postmortem.md` — the scored-baseline session; where the 0.62 baseline and the reference-blindness finding came from.
10. `docs/anima-test-runs/2026-06-01-em-reference-blindness-FINDING.md` — the locked #1 fix that PR #13 then built (and this session blocked).
11. `docs/anima-test-runs/2026-06-02-em-reference-images-field-report.md` — the PR #13 code + the twice-deferred run + the agy-quota postscript.
12. `docs/anima-test-runs/2026-06-02-em-rebaseline-runbook.md` — the §9 scoring disciplines (false-pass-first), referenced throughout.
13. `docs/anima-test-runs/2026-06-02-operational-incidents-remediation-plan.md` + `docs/fleet-ops-protocol.md` — the three gates + standing run discipline (subscription billing, worktree isolation, singleton, clean teardown).
14. `docs/anima-test-runs/2026-05-28-cy-bibles-end-to-end-against-live-models.md` and `docs/anima-test-runs/2026-05-29-production-bake-and-gate-hardening.md` — Cy's Bible bakes; relevant because the provenance bug implicates Cy's Pass-3 verification (same agy wrapper, so the two shipped Bibles were verified by **Flash**, not the Pro the docs claim).

**The state you're inheriting (from the postmortem — confirm against the tree, don't trust labels):**
- The Gemini-API transport shipped clean (5 TDD commits, 275 green); the agy teardown/detach saga evaporated by deleting the subprocess.
- **Provenance bug:** every agy caller ran the backend-default model with no `-m` flag → `gemini-3.5-flash` across 272/272 Em-sized calls, including the 0.62 baseline and the 2026-05-31 bake-off. The model was pinned to `gemini-3.5-flash` (the one that actually ran) to hold it constant. **Cy's Pass-3 uses the same wrapper** — its shipped Bibles were Flash-verified too.
- **References regression:** performs false_pass 0.00→0.15 (2 real defects passed: `stylus-hand-f13-cc01`, `proportion-eyes-body-profile-right`), recall 1.00→0.85, precision 0.62→0.73 (disqualified). Diagnosis: part Opus stochasticity, part confabulation (the MLLM recited the reference bundle onto the subject — claimed cream-paper grain that isn't in the fixture). A prompt-ablation showed the "matches references = correct" wording is a lever, not a fix.
- **Blocked** per the false-pass-first gate. References-attach is the shipped PR #13 default and is now eval-blocked — that disposition is the one decision deliberately left open.

**Help me decide and sequence these (the postmortem's six, prioritized). Use AskUserQuestion to structure the genuine forks; recommend, don't just enumerate:**

1. **References-attach disposition (the open decision).** Revert PR #13 / gate it behind a flag, off by default, until a deterministic backstop lands / leave it on and accept the known regression pending DINOv2. This is the headline call.
2. **Model-provenance gap, program-wide (the scariest).** Every agy caller chose the model by label, not ID. Decide the audit scope + urgency: which callers to pin-by-ID + log-actual-model, whether Cy's two shipped Bibles need re-verification on a pinned model, and whether the CLAUDE.md/manifest "Pro" claims get corrected. This touches shipped artifacts, not just Em.
3. **Promote DINOv2 (follow-on #3) to next?** The confabulation finding is its strongest motivation — a deterministic identity/proportion signal can't recite references.
4. **Baseline replication.** Make the costed scorer run N times / per-case majority-vote and report a false_pass band — the stylus case flipped pass↔fail across identical runs, so 0.15 is one noisy draw.
5. **If references survive in any form:** soften the matching-wording lever + ship view-aware reference selection (approach A) so profile shots get profile refs.
6. **Re-run the three-way bake-off with pinned, correctly-labeled models** — the "Gemini" column was Flash; pin it explicitly, and only attach references once #1 is resolved.

**Operating rules (fleet-ops + the new lesson):**
- This is a **Cowork orient-and-decide session** — no costed builds/evals here; produce a plan/kickoff for Claude Code.
- **Plan-first, empirical-not-vibes.** The biggest lesson is that the obvious change regressed safety; treat every proposed fix as eval-gated, and **pin models by ID and verify-from-logs** — never trust a label again.
- **Labels stay locked** (the eval case labels) — any that look wrong come to me for re-ratification.
- Billing/worktree discipline stands: Claude on the subscription SDK (`ANTHROPIC_API_KEY` absent), Gemini on the bounded API key, never route Claude through a non-Anthropic API, costed work in an isolated worktree with a single owner.

**FIRST ACTIONS:**
1. Set up a task list.
2. Reconcile git state: confirm whether PR #15 (`b30039b`) is merged into `main`, get onto a clean main that carries the transport + postmortem, and clean the stale `.claude/worktrees/em-rebaseline` worktree + merged branches per the fleet-ops teardown rule. Report what you find before reading further.
3. Read the files above, then give me a tight synthesis: the two failures, the provenance blast radius (who else ran Flash), and your recommended sequencing of the six items.
4. Walk me through the decisions via AskUserQuestion (lead with #1 references-disposition and #2 provenance-audit-scope), then draft the plan/kickoff for the chosen path.
