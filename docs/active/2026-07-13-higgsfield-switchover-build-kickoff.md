# Kickoff — Higgsfield transport switchover build (red-team, then implement)

**Date:** 2026-07-13 · **Workstream:** the outward turn / animation-vocabulary-expansion (executes phases T1+T3 of the ratified [transport strategy decision](2026-07-13-transport-strategy-decision.md)) · **Status:** kickoff — not yet run · **Executor:** Codex 5.6 Sol High (the ratified pattern: Codex builds, Claude planned, only Sean merges) · **Prereq:** PR #112 merged to main.

---

## The pasteable kickoff prompt

> You are running the **Higgsfield transport switchover build** for anima — first as a **red-team of the implementation plan**, then (after Sean's go) as the **implementation itself using superpowers:subagent-driven-development**. Claude wrote the plan; your job is to break it before you build it, then build it exactly.
>
> **The plan (the primary artifact):** `docs/superpowers/plans/2026-07-13-higgsfield-transport-switchover.md` — local-only (that directory is gitignored), 7 TDD tasks. It executes phases T1+T3 of the ratified decision doc.
>
> **Read first, in order:**
> 1. `docs/active/2026-07-13-transport-strategy-decision.md` — the RATIFIED decision (D1–D6 + phased plan). The design calls are settled; do not re-litigate them.
> 2. The plan itself, end to end.
> 3. `docs/anima-test-runs/2026-07-13-transport-probes-and-pricing-field-report.md` — the probe evidence + first-party Higgsfield facts the plan's mitigations come from.
> 4. `docs/architecture/style-register-authoring-playbook.md` §Transport + §Standing guards — the frozen md5 guards and the fail-loud boundary the build must preserve.
> 5. `docs/architecture/fleet-ops-protocol.md` — worktree isolation, `ANTHROPIC_API_KEY` absent, singleton pre-flight.
> 6. The code surface: `pipeline/agents/nb_pro_runner.py` (the shape being mirrored + the dispatch site), `pipeline/registers.py` (constants), `pipeline/agents/character_designer.py:732,824` + `pipeline/agents/frame_router.py:213` (the call sites that must need ZERO changes), `tests/test_nb_pro_runner.py` + the three per-register test files (primal/samurai/fusion).
>
> **PHASE 1 — RED-TEAM THE PLAN (no code changes yet; $0).**
> Hunt for blocking defects, not style nits. Verify every plan assumption against ground truth on this machine. Specific attack surfaces (start here, don't stop here):
> 1. **CLI contract drift.** The plan's argv (`--prompt/--quality/--resolution/--aspect_ratio/--image/--wait/--wait-timeout`) was proven on CLI v0.2.3, but upstream is already v1.x. Run `higgsfield --version` and `higgsfield model get gpt_image_2 --json` (read-only, $0) and diff every assumed flag/param/enum against reality. Decide (with Sean) whether to pin the installed CLI version or upgrade-and-verify first — a wrong flag surfaces as a silent hard-fail path.
> 2. **Output parsing.** `_parse_cli_output` assumes a bare https URL in stdout (proven on the 2026-07-13 probe) with a JSON fallback whose field names are guessed. Verify what `--wait` actually prints on the current CLI (a read-only `generate cost` call and the probe logs at `runs/2026-07-13-transport-probes/*/log.txt` are evidence; do NOT run a live generation to check).
> 3. **Duck-typing completeness.** Cy's two call sites and Flo read fields off the response (`ok`, `stub_fallback`, `cache_hit`, `cache_key`, `exit_code`, `output_path`). Grep every consumer of `invoke_image_edit`'s return (incl. bake-offs and `pipeline/tests/`) and confirm `HiggsfieldResponse` satisfies all of them.
> 4. **Import cycle.** `higgsfield_runner` imports from `nb_pro_runner` at module level; `nb_pro_runner` imports `higgsfield_runner` lazily inside `invoke_image_edit`. Confirm no path imports them in an order that breaks.
> 5. **Test-flip completeness.** `grep -rn UnwiredTransportError tests/ pipeline/tests/ evals/` — the plan flips three per-register tests; find any OTHER test/eval asserting gpt-image raises (Maya's cost-estimator `confidence: lowered` path reads route `status:` — check whether any fixture claims gpt_image_2 is deferred).
> 6. **GA-repin blast radius.** The plan enumerates the raw-string sites for `gemini-3.1-flash-image-preview`/`gemini-3-pro-image-preview`; re-grep the whole repo (incl. `evals/`, `scripts/`, `.claude/skills/`) for stragglers, and sanity-check the claim that only the characterization oracle's model table (not the `_SIX` clause pins) moves.
> 7. **Spend safety.** Every unit test must be incapable of a live call on THIS machine (an authenticated `higgsfield` binary is on PATH): confirm the `_run_cli` seam + `ANIMA_FORCE_STUB` cover every real-path test, and that Task 6's verification commands are all $0.
> 8. **The plan's own self-consistency:** signatures across Tasks 1→3, the `HiggsfieldResponse` positional-arg usage, the `import json` hoist note, Task 7's field-report path.
>
> **Output of Phase 1:** a findings list (severity-ranked: BLOCKING / should-fix / note), each with file:line evidence. **Fold accepted fixes directly into the plan file** (edit `docs/superpowers/plans/2026-07-13-higgsfield-transport-switchover.md` in place), then **STOP and present the findings + plan diff to Sean for his go** before any implementation.
>
> **PHASE 2 — IMPLEMENT (after Sean's explicit go).**
> Use **superpowers:subagent-driven-development**: a fresh subagent per plan task, two-stage review between tasks, exactly as the plan's task/step structure specifies. Rules of engagement:
> - Isolated git worktree on a fresh branch off `main` (post-#112), e.g. `feature/higgsfield-transport`. Fleet-ops pre-flight before starting.
> - **$0 through Task 6.** TDD as written: run the failing test, verify RED for the right reason, implement, verify GREEN, commit per task. `python -m pytest tests/` and `python -m pytest pipeline/tests/` are separate runs, always.
> - **Task 7 (live smoke, ~8–12 credits) is Sean-gated — do not run it without his in-session go.** If he defers it, note that in the CHANGELOG entry and stop after Task 6.
> - Standing guards: both md5s unchanged (`2af75906…` g6.1b trace, `945af824…` screenwriting voice); `SUPPORTED_IMAGE_MODELS` stays exactly the two GA Gemini IDs; unmapped models still raise `UnwiredTransportError`; the six legacy registers' clauses byte-identical.
> - Ship as **one PR** with the evidence in the description (per-task test output, the verification-gate checklist, the red-team findings ledger + dispositions). **Only Sean merges.**
>
> Start with the six reads, then open Phase 1 with your highest-severity finding first.

---

## Context notes (not part of the paste)

- **Why red-team first:** the plan was written same-session as the decision; its CLI argv/parse assumptions ride on a v0.2.3 probe while upstream is at v1.x. That version gap is the most likely blocking defect — check it before any code exists.
- **The pattern is the ratified one** (memory: Codex executes / Claude reviews / only Sean merges). Claude reviews the per-task diffs at Sean's request after Codex ships the PR — don't trust the evidence pack alone.
- **The plan file is local-only** (gitignored dir). If Codex runs somewhere without this filesystem, copy the plan content into the session first.
- Task 7's smoke doubles as the first real generation through the production path — if Sean greenlights it in-session, its field report starts the evidence trail the T2 GRANDMASTER validation will extend.
