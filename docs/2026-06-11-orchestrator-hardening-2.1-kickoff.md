# Kickoff — Run Orchestrator, Slice 2.1: pre-costed hardening ($0 stub-green, TDD)

*Paste the block below into a fresh Claude Code session in the `anima` repo. Self-contained.
Plan of record: [`docs/2026-06-11-orchestrator-hardening-2.1-build-plan.md`](2026-06-11-orchestrator-hardening-2.1-build-plan.md).*

---

You're hardening the run orchestrator (`python -m pipeline.run`, shipped in #50) so it can be
proven **without spending** — the prerequisite for the held costed validation run. Two
independent $0/TDD fixes. Read first, in order:
[`docs/2026-06-11-orchestrator-hardening-2.1-build-plan.md`](docs/2026-06-11-orchestrator-hardening-2.1-build-plan.md)
(the spec), `PHILOSOPHY.md`, `CLAUDE.md`. The code you're touching:
`pipeline/orchestration/{run? ,generate_stage,plan_stage,state}.py`, `pipeline/run.py`,
`pipeline/orchestration/cast.py`, and a new tiny stub node.

**Fix A — offline image stub:** make `--stub` walk the *whole* CLI chain offline ($0, no key).
Today `--stub` stubs Maya but not Flo, so a live `--stub` run errors at F01
(`flo F01 nb2 route returned no candidate`). **Fix B — brief snapshot:** stop the PLAN stage
clobbering the committed brief (`plan.md` / `acceptance_criteria.json` are written into the brief
dir and approval locks the brief's criteria in place).

**Out of scope:** the costed run (held); seam #10 (Em CC01 — eval-gated); seam #14 (museum —
Slice 3). Don't touch `evals/vision_critic/`.

## Doctrine — non-negotiable

- **Verify against the tree, never trust a label — including this kickoff and the plan.**
  Re-confirm before building: that `state["stub"]` is already persisted (`run.py:_start` →
  `state.py:new_state`); that the Em no-key path returns a verdict and doesn't raise (the plan
  claims `borderline`, no raise — confirm); that `generate_stage.run_frame_fan` dispatches Flo
  via `node_name="flo"`; that the four brief-writing sites are the ones named in the plan
  (`PlannerNode` output paths, `_lock_brief_criteria`, `wire_brief_criteria`, and they all read
  `state["brief_dir"]`). Cautionary tales: a runbook claimed a loop self-isolates and the run
  crashed on case #0; Flo's CHANGELOG read "built" while nothing dispatched it.
- **Em verdict-baseline guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md`
  must stay `2af75906502f1caf8857e18828ceb2e4`. Nothing here reaches `evals/vision_critic/`.
- **$0 — stub-green only.** No model spend; the headline deliverable is precisely that the CLI
  proves end-to-end with no key.
- **TDD red→green, two independent commits** (Fix B, then Fix A), each revertible alone.

## §0 — fleet-ops gates (before any edit)

```bash
cd <anima main checkout>
git fetch origin
git log --oneline -1 origin/main          # expect dea68e3 (#50) or newer
git rev-list --left-right --count origin/main...HEAD   # expect 0 0
md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md  # 2af75906502f1caf8857e18828ceb2e4
echo "${ANTHROPIC_API_KEY:-ABSENT}"        # expect ABSENT
```

One isolated worktree off `origin/main`; ALL edits inside it. Baseline green (the `.env`
artifact note still applies — 2 `test_frame_router` nb_pro failures only if a `.env`/key is
present; confirm by running them with the key unset):

```bash
python -m pytest tests/ -q          # expect 560 passed / 2 skipped credential-free
python -m pytest pipeline/tests/ -q
```

## Fix B — brief snapshot (do this first)

**Re-verify.** `run.py:_start` sets `brief_dir = Path(args.brief)` + `shots_path = brief_dir /
"shots.yaml"`. `plan_stage` + `cli.plan.approve_plan` write/lock inside `state["brief_dir"]`.
Confirm every downstream consumer reads `state["brief_dir"]` / `state["shots_path"]` (so
repointing them is sufficient).

**Test first.** A regression guard: `--brief` against a brief fixture that carries a committed
`plan.md` + `acceptance_criteria.json`, run through PLAN (stub), assert the **original** brief
files are byte-unchanged (md5 before == after) while `run_dir/brief/` holds the generated
artifacts. Plus a `--resume` test that still finds brief + shots after the snapshot.

**Fix.** At `_start`, copy the brief dir → `run_dir/brief/` (e.g. `shutil.copytree`) and set
`state.brief_dir` + `state.shots_path` to the run-local copy before `new_state`. One site; no
`PlannerNode` / plan-CLI / `author_plan.py` signature changes. Verify `derive_cast` (reads the
manifest, not the brief) and `shots.yaml`'s repo-relative `extra_references` are unaffected.

## Fix A — offline image stub (the headline)

**Re-verify.** `state["stub"]` is already persisted — confirm. The offline chain already works
except Flo: T1 passes on a 16:9 candidate; Em no-key → `borderline`, no raise (confirm with a
quick no-key `VisionCriticNode().run` on a 1376×768 PNG); `assemble.sh` runs on placeholders.

**Test first.** (1) Unit: a new `flo_stub` node emits a candidate that clears
`audit.check_aspect_ratio` (16:9 ±2%). (2) The headline — a **production-path** offline
integration test (NOT the fixture-monkeypatched one): with `--stub` and `GEMINI_API_KEY` unset,
drive the real `pipeline.run.main()` through PLAN → `--approve-plan` → `--approve-frame` for
every frame → ASSEMBLE, asserting `stage == DONE` and the loop files exist. Use the fake-ffmpeg
PATH shim (as `tests/test_assemble.py` / the Slice 2 integration test do) so no real encode runs;
everything else is the real production stub path (`flo_stub` + Em-no-key + `assemble.sh`). Keep
the existing fixture integration test.

**Fix.** Register a tiny `flo_stub` node (writes a real 1376×768 placeholder PNG, emits
`candidate_path` — mirror `tests/orch_fixtures.fake_flo_generate`). In
`generate_stage.run_frame_fan`, select the Flo node by the run-level flag:
`flo_node_name = "flo_stub" if state.get("stub") else "flo"` — everything else (audit, per-
namespace Em, the Runner + `post_run` hook, the attempt cache-salt) is untouched. Make `--status`
keep surfacing `[stub]` so a stub loop is never mistaken for real.

## Done criteria

- `python -m pipeline.run --brief <dir> --stub` (no `GEMINI_API_KEY`) walks PLAN → GENERATE
  (all frames) → ASSEMBLE → DONE and produces a loop — proven by the production-path integration
  test.
- `--brief` leaves the committed brief byte-unchanged; the run-local `brief/` carries the plan.
- `python -m pytest tests/ -q` + `pipeline/tests/ -q` green credential-free; Slice 1 PT_A1 golden
  + Slice 2's 41 orchestrator tests still green.
- `md5sum …/g6.1b-criteria-attached-2026-06-08.md` == `2af75906502f1caf8857e18828ceb2e4`.
- `git -C <main> status -s` clean (no worktree leak).
- CHANGELOG.md entry (decision-log voice + the md5 line + test counts). CLAUDE.md — update the
  `python -m pipeline.run` Key Commands note (`--stub` = fully-offline smoke; brief snapshotted
  per run).
- One squash PR off `origin/main`; clean worktree teardown.

When done, report: the `flo_stub` node + the switch site; the production-path offline test (and
that it reaches DONE with no key); the brief-byte-unchanged proof; and the final test counts.
