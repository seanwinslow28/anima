# Kickoff — Run Orchestrator: Phase 3 wiring (the STORYBOARD slice) ($0 stub-green, TDD)

*Paste the block below into a fresh Claude Code session in the `anima` repo. Self-contained.
Plan of record: [`docs/2026-06-15-orchestrator-storyboard-wiring-build-plan.md`](2026-06-15-orchestrator-storyboard-wiring-build-plan.md).*

---

You're wiring **Phase 3 into the run orchestrator** — the deliberate third Phase-3 slice. Sam (#52)
and Bea (#54) shipped standalone; this slice makes `python -m pipeline.run` drive Maya → Sam → Bea →
human-curate → Flo/Em → assemble as **one resumable program**, while keeping the existing
hand-authored `shots.yaml` path working byte-unchanged. **$0 stub-green** — running Sam/Bea live is
the deferred costed concern, not this slice. Read first, in order:
[`docs/2026-06-15-orchestrator-storyboard-wiring-build-plan.md`](docs/2026-06-15-orchestrator-storyboard-wiring-build-plan.md)
(the spec), `PHILOSOPHY.md`, `CLAUDE.md`, `docs/pipeline-architecture-v1.md` §Phase 3. The code you're
extending: `pipeline/run.py` (the stage machine), `pipeline/orchestration/{state,plan_stage,generate_stage,
script_stage?,storyboard_stage?}.py`, and the built nodes `pipeline/agents/{scriptwriter,storyboard_artist}.py`.

**Two locked decisions (build-plan §Decisions):** (1) **two gates** — `PLAN → SCRIPT (--approve-script)
→ STORYBOARD (--approve-storyboard) → GENERATE`; (2) **auto-detect back-compat** — a brief that already
carries a `shots.yaml` skips SCRIPT/STORYBOARD and runs `PLAN → GENERATE` as today.

**What you build:** the conditional stage graph; the `enter_generate` refactor; two new stage runners
(`script_stage.py`, `storyboard_stage.py`); the `_start` authoring/back-compat branch + slug rule; two
new resume actions; a minimal authoring brief fixture; the wiring tests; docs.

**Out of scope:** running Sam/Bea **live** (the deferred costed run — prove `beat_id` against a real
Bea draft there); museum capture (its own slice); the bake-off/hardening campaign. Don't touch
`evals/vision_critic/`.

## Doctrine — non-negotiable

- **Verify against the tree, never trust a label — including this kickoff and the plan.**
  Re-confirm before building: that `state.STAGES`/`_STAGE_TRANSITIONS` are where the graph extends;
  that `approve_plan_gate` ends with the load-shots→validate-inputs→seed-frame-state→advance→
  `generate_current_frame` block that becomes `enter_generate` (read it — it's the refactor's whole
  surface); that `--brief` mode currently reads the slug from `shots.yaml` (`run.py:_start`) and that
  the brief snapshot is a full `copytree` (so `beats.json`/`shots.yaml` Sam/Bea write into
  `run_dir/brief/` are covered); that `ScriptwriterNode`/`StoryboardArtistNode` take `{brief_dir}` and
  honor `ANIMA_FORCE_STUB` (so `--stub` walks them offline); that Bea's `storyboard_validate` enforces
  **`beat.cast ⊆ shot.cast`** (the #54 inversion — re-use it at the curation gate, don't reinvent it).
  Cautionary tales: a runbook claimed a loop self-isolated and the run crashed on case #0; Bea's own
  plan had the cast rule backwards and the tree corrected it.
- **Two md5 guards, both must hold:** Em baseline
  `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` == `2af75906502f1caf8857e18828ceb2e4`;
  Sam's voice file `pipeline/agents/prompts/sean-screenwriting-voice.md` == `945af824fa53b948a18ac6bf206d67ef`.
  Nothing here reaches `evals/vision_critic/` or that voice file.
- **Back-compat is a hard gate.** `test_run_integration.py` (the Spark stub-walk) + the existing
  `test_run_*` suite must stay green — that's the proof the `enter_generate` refactor and the
  conditional graph changed no observable behavior for a brief that carries a `shots.yaml`.
- **$0 — stub-green only.** No model spend. The headline deliverable is the authoring chain walking
  `PLAN→SCRIPT→STORYBOARD→GENERATE→…→DONE` with **no key**, via Sam/Bea's stub fallbacks under
  `ANIMA_FORCE_STUB`.
- **TDD red→green.** Graph first, then the refactor (with the back-compat test as its net), then the
  stages, then `run.py` wiring, then the curation-gate test, then docs. Small, revertible commits.

## §0 — fleet-ops gates (before any edit)

```bash
cd <anima main checkout>
git fetch origin
git log --oneline -1 origin/main                        # expect b51440f (#54) or newer
git rev-list --left-right --count origin/main...HEAD    # expect 0 0
md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md  # 2af75906502f1caf8857e18828ceb2e4
md5sum pipeline/agents/prompts/sean-screenwriting-voice.md               # 945af824fa53b948a18ac6bf206d67ef
echo "${ANTHROPIC_API_KEY:-ABSENT}"                     # expect ABSENT
python -m pytest tests/ -q                              # expect green (636+)
```

One isolated worktree off `origin/main`; ALL edits inside it. Single owner.

## Build order (TDD)

1. **`state.py` graph + tests.** `STAGES = ("PLAN","SCRIPT","STORYBOARD","GENERATE","ASSEMBLE","DONE")`;
   `_STAGE_TRANSITIONS` with `PLAN: ("SCRIPT","GENERATE")`, `SCRIPT: ("STORYBOARD",)`,
   `STORYBOARD: ("GENERATE",)`. Add `needs_storyboard: bool` to `new_state`; render_status hints. Red→
   green on legal/illegal transitions (both PLAN targets legal). Run existing state tests — green.

2. **`enter_generate` refactor + the back-compat net.** Extract the load-shots→validate→seed→advance→
   fan-frame-1 block from `approve_plan_gate` into `generate_stage.enter_generate(state, manifest,
   bundle, run_dir)`. Back-compat `approve_plan_gate` (needs_storyboard False) calls it. **Confirm
   `test_run_integration.py` stays green** — that's the refactor's safety net before anything depends
   on it.

3. **`script_stage.py` + `storyboard_stage.py` (stub path) + `tests/test_run_storyboard_wiring.py`.**
   `run_script_stage`/`approve_script_gate` (Sam → `beats.json`; approve flips its `locked`, advances
   to STORYBOARD, runs Bea) and `run_storyboard_stage`/`approve_storyboard_gate` (Bea → draft
   `shots.yaml`; set `state["shots_path"]` here; approve re-validates via `load_shots` +
   `storyboard_validate` against `beats.json`, then `enter_generate`). Add a minimal authoring brief
   fixture (`tests/fixtures/briefs/authoring-min/00_studio_brief.md`, no `shots.yaml`). Assert the full
   offline stub-walk to DONE.

4. **`run.py` wiring.** `_start` branches on `shots.yaml` presence (authoring vs back-compat) + the
   slug rule (`--slug` else `read_slug` else error). Add `--approve-script` / `--approve-storyboard`
   resume actions + their stage guards (mirror `--approve-plan`). `--brief` requires `shots.yaml` OR
   (`00_studio_brief.md` + slug). Test both the authoring walk and that
   `--brief briefs/2026-06-10-spark-shared --stub` still skips to GENERATE.

5. **Curation-gate test.** Between `run_storyboard_stage` and `--approve-storyboard`, mutate the draft
   `shots.yaml` (simulate Sean's edit); assert `approve_storyboard_gate` re-validates coverage +
   conflict and **refuses a board that drops a beat's character** (the `beat.cast ⊆ shot.cast` rule).

6. **Docs.** CHANGELOG.md dated entry (two gates, conditional graph, `enter_generate` refactor,
   back-compat auto-detect). CLAUDE.md — update the run-orchestrator Key Commands + the Phase-3 line
   (now wired); note museum capture stays its own slice. Re-assert both md5 guards.

## Acceptance (all must hold before the PR)

- Authoring stub-walk (`--brief tests/fixtures/briefs/authoring-min --stub`) reaches DONE through both new gates, fully offline ($0) — proven by `test_run_storyboard_wiring.py`.
- `--brief briefs/2026-06-10-spark-shared --stub` still goes `PLAN→GENERATE`; `test_run_integration.py` + existing `test_run_*` green (back-compat proof).
- The curation gate re-validates the human-edited `shots.yaml` and refuses a coverage/conflict break — proven by test.
- `python -m pytest tests/` green (636 + new, 0 regressions); `pipeline/tests/` green.
- Both md5 guards intact (Em baseline + Sam's voice file). Nothing under `evals/vision_critic/`.
- CHANGELOG.md + CLAUDE.md updated. One squash PR off the isolated worktree. Clean teardown.

## When done

Report: the commits, the new test count, full-suite-green-credential-free confirmation, both md5
guards intact, and a one-paragraph field note on any seam that fought you (especially anything the
plan got wrong — the plan is a hypothesis, the tree is truth). Then stop — the named fleet and its
wiring are complete; the remaining orchestrator work is museum capture and the deferred costed run.
