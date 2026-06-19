# Build Plan — Run Orchestrator: Phase 3 wiring (the STORYBOARD slice)

*Dated 2026-06-15. Companion to the paste-ready [wiring kickoff](2026-06-15-orchestrator-storyboard-wiring-kickoff.md). This is the deliberate **third Phase-3 slice**: after Sam (#52) and Bea (#54) landed standalone, this wires them into `python -m pipeline.run` so the loop closes inside one resumable program. $0 stub-green, TDD — the live authoring run is the deferred costed concern, not this slice.*

> **Naming note:** "Slice 3" in `run.py`'s docstring already refers to **museum capture** — a different, separately-tracked piece. This doc calls its work **the Phase 3 wiring slice** to avoid the collision. Museum capture stays its own slice.

---

## What this does, in one picture

Today the orchestrator runs `PLAN → GENERATE → ASSEMBLE → DONE` and consumes a **hand-authored `shots.yaml`** (it reads the slug from it at start; GENERATE generates from it). Sam and Bea exist but stand outside that program. This slice inserts them as two gated stages, and keeps the hand-authored path working untouched:

```
authoring brief (00_studio_brief.md, no shots.yaml):
   PLAN ──approve-plan──► SCRIPT ──approve-script──► STORYBOARD ──approve-storyboard──► GENERATE ─► ASSEMBLE ─► DONE
        (Maya)                 (Sam → beats.json)         (Bea → draft shots.yaml)        (Flo …)

back-compat brief (carries a shots.yaml, e.g. the Spark brief):
   PLAN ──approve-plan──► GENERATE ─► ASSEMBLE ─► DONE          (SCRIPT + STORYBOARD skipped — byte-unchanged)
```

This is the moment the orchestrator stops *needing* a hand-written `shots.yaml` — Bea drafts it, Sean curates it at the storyboard gate, GENERATE consumes the locked board.

---

## Decisions locked 2026-06-15

| # | Fork | Decision | Why |
|---|------|----------|-----|
| 1 | Gate shape | **Two gates: SCRIPT then STORYBOARD** | Sean reviews Sam's beats before Bea boards them, then curates Bea's `shots.yaml` — two distinct human decisions. Matches the standalone CLIs (`script approve` + `storyboard approve` already exist) and the human-owns-story-AND-board thesis. |
| 2 | Back-compat | **Auto-detect: a provided `shots.yaml` skips authoring** | A brief that already carries a `shots.yaml` runs `PLAN → GENERATE` exactly as today — the Spark brief is byte-unchanged. Sam→Bea run only when there's no board yet. The hand-authored escape hatch stays alive (Phase 3 is human-authored by design; the agents draft when asked, not always). |
| 3 | Spend | **$0 stub-green build; live authoring deferred** | `--stub` walks the whole authoring chain offline (Sam + Bea have stub fallbacks; `ANIMA_FORCE_STUB` gates every transport). Running Sam (Opus) + Bea (Sonnet) **live** costs money — that's the deferred costed run, Sean's gate, not this slice. |

---

## The conditional stage graph (the load-bearing state-machine change)

`pipeline/orchestration/state.py` today: `STAGES = ("PLAN", "GENERATE", "ASSEMBLE", "DONE")` with a static transition table. The slice extends it so PLAN can go to **either** SCRIPT (authoring) or GENERATE (back-compat), chosen at runtime by a `needs_storyboard` flag set at start:

```python
STAGES = ("PLAN", "SCRIPT", "STORYBOARD", "GENERATE", "ASSEMBLE", "DONE")
_STAGE_TRANSITIONS = {
    "PLAN":       ("SCRIPT", "GENERATE"),   # authoring | back-compat
    "SCRIPT":     ("STORYBOARD",),
    "STORYBOARD": ("GENERATE",),
    "GENERATE":   ("ASSEMBLE",),
    "ASSEMBLE":   ("DONE",),
    "DONE":       (),
}
```

`advance_stage` already validates against this table — adding both PLAN targets keeps the legality check honest while letting the gate logic pick the path. `new_state` records `needs_storyboard: bool`; `render_status` gets hints for the two new stages.

---

## The `enter_generate` refactor (the clean reuse)

`approve_plan_gate` today ends with the block that enters GENERATE: lock criteria → `load_shots` → validate cast anchors + extra refs exist → seed `frame_order`/`holds`/per-frame state → `advance_stage("GENERATE")` → `generate_stage.generate_current_frame` (fan frame 1). In authoring mode that block must run at the **storyboard** gate instead (the `shots.yaml` doesn't exist until Bea writes it).

Factor the load-shots-through-fan-frame-1 block into a shared helper — `generate_stage.enter_generate(state, manifest, bundle, run_dir)` — and call it from **both** gates:

- **back-compat** `approve_plan_gate` (`needs_storyboard == False`): lock criteria → `enter_generate()`. (Today's behavior, unchanged.)
- **authoring** `approve_plan_gate` (`needs_storyboard == True`): lock criteria → `advance_stage("SCRIPT")` → `run_script_stage` (Sam) → stop at the script gate.
- **authoring** `approve_storyboard_gate`: validate the curated `shots.yaml` (`load_shots` + `storyboard_validate` against `beats.json`) → `enter_generate()`.

Criteria locking stays at the plan gate in both modes (it's plan-level, happens once). `enter_generate` is the single place that loads the board and fans the first frame, so the two entry paths can't drift.

---

## The two new stages (mirror `plan_stage.py`)

**`pipeline/orchestration/script_stage.py`:**
- `run_script_stage(state, manifest, run_dir, *, stub)` — invoke Sam (`ScriptwriterNode`) over `run_dir/brief/`; Sam writes `script.md` + `beats.json` into the brief snapshot. Print the script gate hint (`script show` to review, `--approve-script` to lock). Record `state["script"] = {"status": "drafted", "stub": …}`.
- `approve_script_gate(state, manifest, run_dir)` — require script drafted; flip `locked: true` on `beats.json` (reuse `pipeline/cli/script.py`'s approve logic); `advance_stage("STORYBOARD")`; then `run_storyboard_stage` (Bea) and stop at the storyboard gate.

**`pipeline/orchestration/storyboard_stage.py`:**
- `run_storyboard_stage(state, manifest, run_dir, *, stub)` — invoke Bea (`StoryboardArtistNode`) over the brief (reads `beats.json`); Bea writes `storyboard.md` + **draft `shots.yaml`** (unlocked) into the brief snapshot. Set `state["shots_path"]` now (authoring mode establishes it here, not at start). Print the curation-gate hint: *edit `run_dir/brief/shots.yaml`, then `--approve-storyboard`.*
- `approve_storyboard_gate(state, manifest, run_dir)` — re-validate the (human-curated) `shots.yaml`: `load_shots` + `storyboard_validate(beats, shots, known_namespaces)` (Bea's own gate, re-run on the edited file); flip `locked: true`; `advance_stage` is handled inside `enter_generate`. **This is the curation gate** — Sean has edited the draft between the stage running and this approve.

Both stages run their agent under the `--stub`/`ANIMA_FORCE_STUB` flag, so `--stub` walks them offline at $0.

---

## `pipeline/run.py` changes

- **`_start` branches on `shots.yaml` presence.** Present → `needs_storyboard=False`, `shots_path` set, slug from `read_slug(shots.yaml)` or `--slug` (today's path, unchanged). Absent → `needs_storyboard=True`, slug from `--slug` (required in authoring mode — there's no board to read it from yet; error clearly if missing), `shots_path` established later by the STORYBOARD stage. The brief snapshot (`copytree`) already carries any `plan.md`/`beats.json` the brief holds.
- **Two new resume actions:** `--approve-script` (legal only in SCRIPT) and `--approve-storyboard` (legal only in STORYBOARD), mirroring `--approve-plan`'s stage-guard + dispatch in `_resume`. Update the mutually-exclusive action set and the per-stage guards.
- **`--brief` no longer hard-requires `shots.yaml`** — it requires `shots.yaml` **or** (`00_studio_brief.md` + a slug source for authoring). Keep the existing clear errors.

---

## Slug source (the one wiring detail to get right)

Today slug = `read_slug(shots.yaml)` or `--slug`. In authoring mode there is no `shots.yaml` at start. Rule: **slug = `--slug` if given, else `read_slug(shots.yaml)` if present, else error** asking for `--slug`. The run's slug (used for the run-dir name) is fixed at start; Sam/Bea author their own `slug` into `beats.json`/`shots.yaml` (which should match, but the run dir is named once and doesn't chase it). Note this in the run-dir naming path.

---

## File map

| File | New/edit | Purpose |
|------|----------|---------|
| `pipeline/orchestration/state.py` | edit | Extend `STAGES` + `_STAGE_TRANSITIONS` (add SCRIPT, STORYBOARD; PLAN→{SCRIPT,GENERATE}); add `needs_storyboard` to `new_state`; render_status hints |
| `pipeline/orchestration/script_stage.py` | **new** | `run_script_stage` + `approve_script_gate` (Sam) — mirrors `plan_stage.py` |
| `pipeline/orchestration/storyboard_stage.py` | **new** | `run_storyboard_stage` + `approve_storyboard_gate` (Bea) — the curation gate |
| `pipeline/orchestration/plan_stage.py` | edit | `approve_plan_gate` branches on `needs_storyboard` (→SCRIPT+Sam, or →GENERATE via `enter_generate`) |
| `pipeline/orchestration/generate_stage.py` | edit | Factor out `enter_generate(state, manifest, bundle, run_dir)` (load_shots → validate inputs → seed frame state → advance → fan frame 1); call it from both gates |
| `pipeline/run.py` | edit | `_start` authoring/back-compat branch + slug rule; `--approve-script` / `--approve-storyboard` resume actions + stage guards; `--brief` no longer hard-requires `shots.yaml` |
| `tests/fixtures/briefs/authoring-min/` | **new** | A minimal authoring brief (`00_studio_brief.md` only, no `shots.yaml`) for the stub-walk test |
| `tests/test_run_storyboard_wiring.py` | **new** | The authoring stub-walk (PLAN→SCRIPT→STORYBOARD→GENERATE) + the back-compat skip (PLAN→GENERATE with a provided board) |
| `CHANGELOG.md` | edit | Dated entry: the two gates, the conditional graph, the `enter_generate` refactor, back-compat auto-detect |
| `CLAUDE.md` | edit | Update the run-orchestrator Key Commands + the Phase 3 line (now wired end-to-end); note museum capture remains its own slice |

---

## TDD sequence

1. **`state.py` graph + `tests` for it first.** Extend `STAGES`/`_STAGE_TRANSITIONS` + `needs_storyboard`; red→green on legal/illegal transitions including both PLAN targets. Run the existing `test_run_*` state tests — confirm green (back-compat).
2. **`enter_generate` refactor + its test.** Extract the block from `approve_plan_gate`; prove the back-compat `PLAN→GENERATE` path is byte-behavior-identical (the existing `test_run_integration.py` Spark stub-walk stays green — that's the refactor's safety net).
3. **`script_stage.py` + `storyboard_stage.py` (stub path) + `tests/test_run_storyboard_wiring.py`.** Build against the stubbed Sam/Bea. Assert the authoring stub-walk: `--brief authoring-min --stub` → PLAN gate → `--approve-plan` → SCRIPT gate (beats.json written) → `--approve-script` → STORYBOARD gate (draft shots.yaml written) → `--approve-storyboard` → GENERATE frame 1 → … → DONE, all offline ($0).
4. **`run.py` wiring.** `_start` branch + slug rule + the two resume actions + stage guards. Test both the authoring walk and that `--brief briefs/2026-06-10-spark-shared --stub` still skips to GENERATE.
5. **Curation-gate test.** Between `run_storyboard_stage` and `--approve-storyboard`, mutate the draft `shots.yaml` (simulate Sean's edit) and assert `approve_storyboard_gate` re-validates it (coverage + conflict via `storyboard_validate`) and refuses a board that breaks coverage.
6. **Docs.** CHANGELOG + CLAUDE.md. Re-assert both md5 guards.

---

## Acceptance criteria

- **Authoring stub-walk** (`--brief tests/fixtures/briefs/authoring-min --stub`) reaches DONE through both new gates, fully offline ($0) — proven by `test_run_storyboard_wiring.py`.
- **Back-compat green:** `--brief briefs/2026-06-10-spark-shared --stub` still goes `PLAN→GENERATE` (skips SCRIPT/STORYBOARD); `test_run_integration.py` and the existing `test_run_*` suite stay green — the refactor changed no observable back-compat behavior.
- The curation gate re-validates the human-edited `shots.yaml` (coverage + conflict) and refuses a broken board — proven by test.
- `python -m pytest tests/` green (636 + new, 0 regressions); `pipeline/tests/` green.
- Both md5 guards hold: Em baseline `2af75906502f1caf8857e18828ceb2e4`; Sam's voice file `945af824fa53b948a18ac6bf206d67ef`. Nothing under `evals/vision_critic/`.
- CHANGELOG.md + CLAUDE.md updated. One squash PR off an isolated worktree from `origin/main`. Clean teardown.

---

## Scope boundary

**In:** the conditional stage graph, the two gates + their stage runners, the `enter_generate` refactor, the `_start` branch + slug rule, the authoring-brief fixture, the wiring tests, docs.

**Out (deferred / separate):**
- **The live authoring costed run** — running Sam (Opus) + Bea (Sonnet) for real, authoring a real `beats.json` + `shots.yaml`, and confirming the beat_id-linked board survives `--approve-storyboard → GENERATE` end-to-end. That's the field report's "prove `beat_id` against a real Bea draft" concern, and it's the deferred costed run (Sean's gate), not this $0 slice.
- **Museum capture** (the orchestrator's own separate slice).
- **The hardening campaign** (Bea's bake-off + composition harness, Sam's pairwise voice harness) — parked.

## After this slice

The fleet runs as one program: `python -m pipeline.run --brief <studio-brief>` drives Maya → Sam → Bea → curate → Flo/Em → assemble, stopping at four human gates (plan, script, storyboard, per-frame eye). The only remaining orchestrator work is **museum capture** (Slice 3) and the **costed validation run** — both already tracked. The named fleet and its wiring are then complete; everything after is hardening.
