# Run Orchestrator — Slice 2.1: pre-costed hardening build plan

**Date:** 2026-06-11
**Status:** Planned. $0 / stub-green / TDD. De-risks the (currently held) costed validation run.
**Predecessor:** Slice 2 (the core build) landed clean at `dea68e3` (#50) — `python -m pipeline.run` exists. Plan: [`docs/2026-06-11-orchestrator-core-build-plan.md`](2026-06-11-orchestrator-core-build-plan.md). Audited 2026-06-11 (Cowork): merge clean, 562 tests green credential-free, `dag.py` change additive, guard intact.

---

## Why this slice exists

The costed validation run is held. Two findings from the Slice 2 audit make the orchestrator
*provable without spending* — which is exactly what you want before the first costed run:

1. **`--stub` stubs Maya, not Flo's image transport.** A live `--stub` CLI run can't get past
   F01 — Flo's nb2 route (the pencil skill) has no offline placeholder, so with no
   `GEMINI_API_KEY` it errors cleanly and the frame stays `pending`. Verified live in the audit:
   the attempt records `errored: "flo F01 nb2 route returned no candidate"`. So **today the
   costed run would be the first time the real CLI chains GENERATE→ASSEMBLE end to end.** That's
   the thing to fix first.
2. **The PLAN stage writes `plan.md` + `acceptance_criteria.json` into the *brief dir*, and
   `--approve-plan` locks the brief's criteria in place** — overwriting committed files. Verified
   live: a stub run clobbered the real spark `plan.md` / `acceptance_criteria.json` /
   `01_production_brief.md` (restored byte-identical from HEAD). The held costed run against
   `briefs/2026-06-10-spark-shared/` would regenerate those committed artifacts.

Both fixes are small, independent, $0/TDD, and reach nowhere near `evals/vision_critic/`.

**Out of scope:** the costed run (still held); seam #10 (Em CC01, eval-gated, ticketed); seam #14
(museum, Slice 3, ticketed).

---

## Fix A — Offline image stub (the de-risker)

**Goal.** `python -m pipeline.run --brief <dir> --stub` walks the *entire* chain —
PLAN → GENERATE (every frame) → ASSEMBLE → DONE — fully offline, $0, no key. The costed run
stops being the first end-to-end CLI proof and becomes a confirmation.

**What's already true (verified against the tree).** `state["stub"]` is **already persisted at
run level** (`run.py:_start` sets `stub=bool(args.stub)`; `state.py:new_state` stores it) — so no
new flag is needed. The generate fan just has to honor it. And the rest of the offline chain
already works: T1 (`audit_gate`) passes on a 16:9 candidate; Em with no key returns a
`borderline` verdict and **does not raise** (verified live — and the orchestrator contains
`EmptyCitesInvariant` per-namespace regardless); `assemble.sh` runs on placeholders. **The only
missing piece is Flo producing a real 16:9 placeholder instead of calling the live transport.**

**The fix.** Register a tiny `flo_stub` node that writes a real 1376×768 placeholder PNG and
emits `candidate_path` (mirroring the test fixture `tests/orch_fixtures.fake_flo_generate`,
which already writes RGB 1376×768). In `generate_stage.run_frame_fan`, select the node by the
run-level flag:

```python
flo_node_name = "flo_stub" if state.get("stub") else "flo"
```

Everything else in the fan is untouched — the `flo_stub` candidate flows into the same
`audit_gate` + per-namespace `vision_critic` graphs, through the same `Runner` + `post_run`
hook, with the same attempt cache-salt. (Alternative considered: write the placeholder inline
before the graph — rejected; the node keeps Runner/cache symmetry and is the smaller mental
diff.)

**Semantics decision (state it in the docs).** `--stub` becomes the **fully-offline $0 smoke
mode**: it stubs Maya's plan *and* Flo's generation, and Em falls back to its no-key stub. The
`plan.stub` marker still gates approval ("never approve as real"); extend that honesty to the
loop — a stub run's `export/` and any museum capture must never be mistaken for a real piece
(a `stub` breadcrumb in the run state already carries; make sure `--status` keeps showing
`[stub]`). The alternative — a separate `--dry-run` flag distinct from `--stub` — is more
surface for no real gain here; fold it into `--stub`.

**Tests.** A *production-path* offline integration test (stronger than the existing
fixture-monkeypatched one): with `--stub` and **no** `GEMINI_API_KEY`, drive the real CLI
`main()` through PLAN → approve-plan → approve every frame → ASSEMBLE and assert `stage == DONE`
+ the loop files exist. This exercises the real `flo_stub` + real Em-no-key + real
`assemble.sh` (fake-ffmpeg PATH shim as Slice 1/2 tests do), not fixtures. Keep the existing
fixture integration test. Add a unit test that `flo_stub` emits a 16:9 candidate that clears
`audit.check_aspect_ratio`.

---

## Fix B — Brief snapshot (stop clobbering the committed brief)

**Goal.** A run never mutates its committed input brief. Each run owns an immutable snapshot of
exactly the brief + plan it ran (a reproducibility win, too).

**Verified diagnosis.** `run.py:_start` sets `brief_dir = Path(args.brief)` and
`shots_path = brief_dir / "shots.yaml"` — the *committed* paths. Downstream, `PlannerNode`
writes `plan.md` / `acceptance_criteria.json` / `01_production_brief.md` into `brief_dir`;
`approve_plan_gate` calls `_lock_brief_criteria(state["brief_dir"])` (flips `locked:true` on the
brief's criteria file) and `wire_brief_criteria` points `criteria_sources.brief_file` at it. So
four operations target the committed brief. Everything downstream reads `state["brief_dir"]` /
`state["shots_path"]` — a single indirection.

**The fix (snapshot, not re-plumb).** At `_start`, copy the brief dir → `run_dir/brief/` and set
`state.brief_dir` + `state.shots_path` to the **run-local copy**. Because every downstream site
reads those state fields, PlannerNode then writes into the copy, approve locks the copy's
criteria, and `wire_brief_criteria` points at the copy — the committed brief stays pristine. One
site changes; no PlannerNode / plan-CLI / `author_plan.py` signature churn (lowest blast radius).

**Verified safe.** `derive_cast(manifest)` reads the manifest's `characters:` (repo-level, not
brief) — unaffected. `shots.yaml`'s `extra_references` are repo-relative
(`characters/claude-mascot/...`) — they resolve from the run regardless of the brief's location.
`--resume` reads `brief_dir` from state (already the copy) — consistent across invocations.

**Tests.** A regression guard for the exact bug the audit hit: `--brief` against a brief fixture,
run PLAN, assert the **original** brief files are byte-unchanged (md5 before == after), while the
run-local `run_dir/brief/` carries the generated `plan.md` + locked `acceptance_criteria.json`.
Plus a resume test: `--resume` after the snapshot still finds its brief + shots.

---

## Build approach

$0 / stub-green / TDD, two independent commits (Fix A, Fix B), each red→green and revertible
alone. Suggested order: **B first** (so the test runs don't risk touching committed briefs),
then **A**. Both verified end-to-end by the new offline integration test.

Internal phases:
- **B** — snapshot at `_start`; the byte-unchanged regression test; resume test.
- **A** — `flo_stub` node + the `node_name` switch; the unit aspect test; the production-path
  offline integration test (the headline deliverable — prove the real CLI walks to DONE for $0).

## Test plan summary

- `flo_stub` emits a 16:9 candidate clearing `audit.check_aspect_ratio`.
- Production-path offline run (`--stub`, no key): PLAN→GENERATE→ASSEMBLE→DONE, loop files exist.
- Brief byte-unchanged after PLAN (md5 before == after on the committed brief fixture).
- Resume after snapshot finds brief + shots.
- Existing suite stays green; Slice 1 PT_A1 golden + Slice 2's 41 tests untouched.

## Fleet-ops + guards

- **$0** (stub-green) — worktree discipline still holds (one isolated worktree off `origin/main`,
  single owner, `ANTHROPIC_API_KEY` absent, divergence `0 0` before).
- **Em baseline untouched:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md`
  == `2af75906502f1caf8857e18828ceb2e4`. Nothing here reaches `evals/vision_critic/`.
- **State of record:** CHANGELOG entry (decision-log voice). CLAUDE.md — update the
  `python -m pipeline.run` Key Commands note: `--stub` is now the fully-offline smoke; the brief
  is snapshotted per run.

## After this slice

The held costed validation becomes a *confirmation*: run `--stub` first (watch the real CLI walk
to DONE for $0), then drop `--stub` for the real ~$0.66 run from a plain terminal (fleet-ops §0,
out of session per seam #4). The brief snapshot means that costed run won't dirty the committed
spark brief either.
