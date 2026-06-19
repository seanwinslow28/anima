# Kickoff — Pre-costed-run hardening: raw-dumps + gate smokes ($0 stub-green, TDD)

*Paste the block below into a fresh Claude Code session in the `anima` repo. Self-contained.
This is a small $0 hardening that must land **before** the first live authoring run
([`docs/2026-06-16-spark-authored-costed-run-runbook.md`](2026-06-16-spark-authored-costed-run-runbook.md)).
Two independent changes; both raise visibility/safety for a run that spends real money.*

---

You're adding two small things to the run orchestrator so the first **live** Sam/Bea run is
inspectable and fails-before-it-spends. **$0 / stub-green** — no model call in CI. Read first:
`PHILOSOPHY.md`, `CLAUDE.md`, the runbook above, and the two stage files you're touching
(`pipeline/orchestration/script_stage.py`, `storyboard_stage.py`). The patterns you're mirroring
already exist in the tree — copy them, don't invent.

**Change A — Sam/Bea raw-dumps (visibility).** Maya dumps her raw Opus response to
`run_dir/maya_raw_pass1.txt` (`pipeline/agents/planner.py:_dump_raw`). Sam and Bea don't dump theirs —
so a live run only leaves the *parsed* artifacts, not the raw model envelope. Add the same best-effort
dump to both: Sam → `run_dir/sam_raw.txt`, Bea → `run_dir/bea_raw.txt`.

**Change B — gate smokes (fail before spend).** `run_plan_stage` smokes Opus live before Maya runs
(`if not (stub or skip_smoke): guards.smoke_live_opus()`), so a broken auth fails *before* the spend.
The script and storyboard gates don't — they only catch a silently-stubbed call *after* it returns
(the stub-marker scan). Add the matching pre-authoring smoke to both: `run_script_stage` →
`guards.smoke_live_opus()`; `run_storyboard_stage` → `guards.smoke_live_sonnet()`.

**Out of scope:** the run itself (that's the runbook, human-driven); any live model call (the smokes
and dumps are exercised stub-side in CI); museum capture; the hardening campaign. Don't touch
`evals/vision_critic/`.

## Doctrine — non-negotiable

- **Verify against the tree, never trust a label — including this kickoff.** Confirm before editing:
  `planner._dump_raw(run_dir, name, text)` is best-effort + never raises (mirror it exactly — a dump
  failure must not abort a live run); `scriptwriter.py` already imports from `planner`
  (`_parse_json_envelope`), so it can import `_dump_raw` too; `guards.smoke_live_opus` /
  `guards.smoke_live_sonnet` / `guards.GuardError` exist (`pipeline/orchestration/guards.py`);
  `run_plan_stage`'s smoke shape is `try: guards.smoke_live_opus() except guards.GuardError as e:`
  (mirror its print + return for the two new gates); the agents write to `ctx.run_dir` (so the dump
  lands beside `maya_raw_pass1.txt`).
- **Two md5 guards, both must hold:** Em baseline
  `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` == `2af75906502f1caf8857e18828ceb2e4`;
  Sam's voice file `pipeline/agents/prompts/sean-screenwriting-voice.md` == `945af824fa53b948a18ac6bf206d67ef`.
  Neither is anywhere near this change.
- **$0 — stub-green only.** No live call. The dump writes whatever text the call returned (stub text in
  CI is fine); the smoke is asserted *invoked* via a mock, never actually run against a model in tests.
- **TDD red→green, two independent commits** (A then B), each revertible alone.

## §0 — fleet-ops gates (before any edit)

```bash
cd <anima main checkout>
git fetch origin
git log --oneline -1 origin/main                        # expect 98aeed8 (#55) or newer
git rev-list --left-right --count origin/main...HEAD    # expect 0 0
md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md  # 2af75906502f1caf8857e18828ceb2e4
md5sum pipeline/agents/prompts/sean-screenwriting-voice.md               # 945af824fa53b948a18ac6bf206d67ef
echo "${ANTHROPIC_API_KEY:-ABSENT}"                     # expect ABSENT
python -m pytest tests/ -q                              # expect green (647)
```

One isolated worktree off `origin/main`; ALL edits inside it. Single owner.

## Build order (TDD)

1. **Change A — raw-dumps.** In `pipeline/agents/scriptwriter.py`, import `_dump_raw` from `planner`
   and call it on the model response **before** `_parse` (so a parse failure still leaves the raw on
   disk), exactly as Maya does: `_dump_raw(ctx.run_dir, "sam_raw.txt", resp.text)`. Same in
   `storyboard_artist.py` → `_dump_raw(ctx.run_dir, "bea_raw.txt", resp.text)`. Tests (extend
   `tests/test_scriptwriter.py` + `tests/test_storyboard_artist.py`): after a stub run, the raw file
   exists in `run_dir` and is non-empty. Commit A.

2. **Change B — gate smokes.** Add the pre-authoring smoke to the top of `run_script_stage`
   (`guards.smoke_live_opus()`) and `run_storyboard_stage` (`guards.smoke_live_sonnet()`), each gated
   `if not stub:` (the `stub` flag is already a parameter / in state), wrapped in the same
   `try/except guards.GuardError` shape `run_plan_stage` uses (print the error, return non-zero —
   fail *before* the authoring call). **Optional polish for fidelity:** persist `skip_smoke` in
   `new_state` at `_start` and gate `not (stub or state.get("skip_smoke"))`, matching `run_plan_stage`
   exactly — do this only if it stays small. Tests (extend `tests/test_run_storyboard_wiring.py`):
   with a mock, assert the smoke is **not** called under `--stub`, and **is** called on the non-stub
   path (mock it to a no-op so no real call happens); a `GuardError` from the smoke makes the gate
   return non-zero before any authoring. Commit B.

3. **Docs.** CHANGELOG.md dated entry (both changes, why — visibility + fail-before-spend for the live
   run). Re-assert both md5 guards.

## Acceptance (all must hold before the PR)

- After a stub authoring walk, `run_dir/sam_raw.txt` and `run_dir/bea_raw.txt` exist and are non-empty (proven by test).
- The script gate smokes Opus and the storyboard gate smokes Sonnet on the non-stub path, and neither smokes under `--stub` (proven by test with a mocked smoke — no real call).
- A smoke `GuardError` makes the gate return non-zero before the authoring call (fail-before-spend, proven by test).
- `python -m pytest tests/` green (647 + new, 0 regressions); `pipeline/tests/` green.
- Both md5 guards intact. Nothing under `evals/vision_critic/`; Sam's voice file unchanged.
- CHANGELOG.md updated. One squash PR off the isolated worktree. Clean teardown.

## When done

Report the commits, the new test count, full-suite-green-credential-free confirmation, and both md5
guards intact. Then stop — the live authoring run is human-driven by Sean per the runbook, not from
this session.
