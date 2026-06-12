# Field Report — Run Orchestrator Slice 2.1: pre-costed hardening ($0 stub-green, TDD)

**Date:** 2026-06-11
**Kickoff:** [`docs/2026-06-11-orchestrator-hardening-2.1-kickoff.md`](../2026-06-11-orchestrator-hardening-2.1-kickoff.md)
**Plan of record:** [`docs/2026-06-11-orchestrator-hardening-2.1-build-plan.md`](../2026-06-11-orchestrator-hardening-2.1-build-plan.md)
**Spend:** $0 (one in-flight Maya Opus call killed before completion — see Surprise #1)
**Branch:** `worktree-orch-hardening-2.1` off `origin/main` `dea68e3` (#50); three TDD commits, each revertible alone

---

## What the kickoff asked to report

### 1. The `flo_stub` node + the switch site

- **Node:** [`pipeline/agents/flo_stub.py`](../../pipeline/agents/flo_stub.py) — `@register_node("flo_stub")`, same `inputs`/`outputs` contract as `FloNode` (`frame_num`/`prompt`/`references` → `candidate_path`), `cost_estimate` usd=0.0. Writes a real RGB **1376×768** PNG to `candidates/F{n:02d}/attempt_{k:02d}.png` (attempt via the same `generate.get_attempt_number` the real nb_pro route uses); bytes vary per attempt so a re-roll yields fresh Em cache keys — mirrors `tests/orch_fixtures.fake_flo_generate`. 1376×768 clears HF01 at 0.78% deviation (≤2%).
- **Switch site:** `generate_stage.run_frame_fan` — `flo_node_name = "flo_stub" if state.get("stub") else "flo"`, threaded into the existing `Node(id=f"flo_{fid}", …)`. Node **id** is unchanged, so audit bindings and `gen_results` lookups are untouched; `node_name` is the first component of the DAG cache key (`dag.py`), so a stub result can never serve a real `flo` node or vice versa. Registration rides the same import-side-effect line as the other fan nodes (`generate_stage.py` imports `pipeline.agents.flo_stub` next to `frame_router`).

### 2. The production-path offline test — DONE with no key

`tests/test_run_integration.py::test_production_path_offline_stub_run_reaches_done`: with `--stub` and `GEMINI_API_KEY` unset (asserted), **no flo monkeypatch, no spies** — env shaping only (`stub_critic_env` + the fake-ffmpeg PATH shim) — it drives the real `pipeline.run.main()` through PLAN → `--approve-plan` → `--approve-frame` for every frame → ASSEMBLE and asserts `stage == DONE`, the loop files (`TT.gif`/`TT.webm`/`TT.mp4`) exist, the flo_stub placeholder candidates are on disk, and `[stub]` appears in `--status` output. The real production stub chain (flo_stub + Em-no-key fallback + `assemble.sh`) is what runs.

Belt-and-braces, the same was proven **live from a shell** against the real committed brief (plain documented command, claude-agent-sdk installed, $0 — post force-stub fix):

```
python -m pipeline.run --brief briefs/2026-06-10-spark-shared --stub --run-dir /tmp/orch-smoke-run
…approve-plan, approve F01..F05…
stage:   DONE  [stub]
brief:   /tmp/orch-smoke-run/brief  (snapshot of briefs/2026-06-10-spark-shared)
exports: SS.gif  SS.mp4  SS.webm  sequence.txt  sequence/
```

### 3. The brief-byte-unchanged proof

- **Regression test:** `tests/test_run_plan_stage.py::test_brief_snapshot_leaves_committed_brief_byte_unchanged` — a brief fixture pre-seeded with committed `plan.md`/`acceptance_criteria.json` (locked)/`01_production_brief.md`, run through PLAN (stub): md5 of every committed file **before == after**, while `run_dir/brief/` carries the freshly generated artifacts and `state.brief_dir`/`state.shots_path` point at the snapshot. Plus `test_resume_after_snapshot_finds_brief_and_shots` (approve-plan locks the snapshot's criteria; shots load via the snapshot).
- **Live:** after the full smoke run against `briefs/2026-06-10-spark-shared/` itself, `git status -s briefs/` and `git diff --stat briefs/` were both **empty** — the exact brief the Slice 2 audit clobbered now survives a full run untouched.
- **Mechanism:** one site — `run.py:_start` copies the brief dir → `run_dir/brief/` (`shutil.copytree`, `dirs_exist_ok=True` for crash-re-entry) and repoints `brief_dir`/`shots_path` before `new_state`. All four brief-writing operations (PlannerNode's three artifacts, `_lock_brief_criteria`, plus `wire_brief_criteria`'s pointer) read `state["brief_dir"]`, verified before building. New optional `brief_src` state field carries provenance (surfaced in `--status` and the Maya gate print). **Residual:** `scripts/author_plan.py` still writes into whatever brief dir it's handed — the snapshot protects only `python -m pipeline.run`.

### 4. Final test counts

| Suite | Before | After | Delta |
|---|---|---|---|
| `python -m pytest tests/ -q` | 562 passed | **576 passed** | +2 snapshot, +3 flo_stub unit, +1 production-path offline, +2 switch (parametrized), +6 force-stub |
| `python -m pytest pipeline/tests/ -q` | 10 passed | 10 passed | — |

Slice 1 PT_A1 golden (`tests/test_assemble.py`) green; Slice 2's orchestrator tests green (8 sites migrated, every assertion's intent preserved — see Surprise #2). Em verdict-baseline guard held: `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4` before and after; nothing touched `evals/vision_critic/`.

---

## Surprises (the part worth reading)

### #1 — `--stub` could silently SPEND: the third fix the plan didn't contain

The build plan's locked semantics said "`--stub` stubs Maya's plan and Flo's generation, and Em falls back to its no-key stub." Verify-against-the-tree (and the first in-session live smoke) showed the Maya half was only true **when no transport was reachable**: `plan_stage` drives `PlannerNode` unconditionally, and `sdk_runners._sdk_available()` returns True whenever `claude-agent-sdk` imports — subscription OAuth, **no API key needed**, so the fleet-ops `ANTHROPIC_API_KEY`-absent gate doesn't catch it. Worse, `gemini_api_runner._resolve_gemini_key()` reads the project **`.env`** as a fallback, so Em would also go live on the main checkout even with the env var unset. The first smoke attempt had to be **killed mid-flight** (~40s into a real Opus call, before completion — negligible spend, zero artifacts) to honor the $0 doctrine. This is the inverse of the silent-stub trap the marker guard already catches: silent SPEND on a run whose contract is $0.

**Fix (TDD, 6 tests):** `pipeline.run` exports `ANIMA_FORCE_STUB=1` for the dynamic extent of a `--stub` invocation — set in `_start`/`_resume`, restored in `main()`'s `finally` so in-process callers (tests) never leak it — and all three model-transport gates honor it: `sdk_runners._sdk_available`, `gemini_api_runner.run_gemini_api_with_image`, `cli_runners.run_antigravity_with_image`. A non-stub run never sets it; a manually exported flag fails closed (Maya's stub-marker guard, rc 1). After the fix, the plain documented smoke command ran $0 on a machine with the SDK installed — re-verified live.

**Operational note for the held costed run:** this also closes the trap where a stub *resume* against a stub run could go live mid-loop. The costed run itself is unaffected (no `--stub`, no env var).

### #2 — The spec's "existing suite stays green" was false: an 8-site test-boundary migration

Every Slice 2 orchestrator test starts runs with `--stub` (the stub-marker guard forces it for stub-SDK Maya) while faking Flo at the `pipeline.generate.generate_frame` boundary. The Fix A switch bypasses that boundary entirely, so 8 test sites broke — and the worst one, the interrupt-recovery test, would have gone **vacuously green** (its flaky fake simply never fires; the test passes while testing nothing). Migrated to the new boundary: `tests/orch_fixtures.spy_flo_stub` (a spy, not a fake — the real node still runs; same call-dict shape as `fake_flo_generate`, so assertions carried over unchanged); the errored-attempt and interrupt tests now raise from `FloStubNode.run`. Coverage that lived on the old boundary was not dropped: a new parametrized `run_frame_fan` switch test drives the fan directly with `stub=False` to prove the real `flo` node still dispatches — including seam #11 (FOLDER key threading) on the real path.

### #3 — Kickoff deltas (small, recorded per the verify-against-the-tree doctrine)

- "Slice 2's **41** orchestrator tests" — the actual count was **36** across 7 `tests/test_run_*.py` files.
- "expect **560 passed / 2 skipped** credential-free" — baseline was **562 passed / 0 skipped**.
- The "`.env` present → 2 `test_frame_router` nb_pro failures" note didn't reproduce in exploration (all 13 frame_router tests are credential-free with no key-conditional paths); the baseline ran keyless regardless, so the claim was moot for this slice.
- `--status` already surfaced `[stub]` (`state.py:render_status`) — no code needed, locked with an assertion in the production-path test.

None of these changed the build; all are why the doctrine exists.

---

## Done criteria — checked

- [x] `python -m pipeline.run --brief <dir> --stub` (no `GEMINI_API_KEY`) walks PLAN → GENERATE (all frames) → ASSEMBLE → DONE and produces a loop — proven by the production-path integration test **and** the live smoke.
- [x] `--brief` leaves the committed brief byte-unchanged; the run-local `brief/` carries the plan.
- [x] `tests/` 576 + `pipeline/tests/` 10 green credential-free; Slice 1 PT_A1 golden + Slice 2 orchestrator tests green.
- [x] Em baseline md5 `2af75906502f1caf8857e18828ceb2e4` unchanged.
- [x] Main checkout clean (the two formerly-untracked kickoff/build-plan docs ship with this PR).
- [x] CHANGELOG.md entry (decision-log voice, md5 line, counts); CLAUDE.md Key Commands updated (`--stub` = fully-offline smoke; brief snapshotted per run).
- [x] One squash PR off `origin/main`; clean worktree teardown.

## What's next

The held **costed validation run** is now a confirmation, not a first proof: run the `--stub` smoke (watch it walk to DONE for $0), then drop `--stub` for the real ~$0.66 run from a **plain terminal** (fleet-ops §0; nested-SDK throttle, seam #4). The brief snapshot means that run won't dirty `briefs/2026-06-10-spark-shared/` either. Slice 3 (museum capture) and seam #10 (Em CC01) remain ticketed.
