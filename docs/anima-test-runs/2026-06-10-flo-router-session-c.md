# Field report — Flo-C: dispatch FloNode in the run path + HF01 fix ($0 stub-green)

**Date:** 2026-06-10 · **Spend:** $0 (stub-green wiring; no model calls, no real frames) · **Outcome:** Flo dispatched + HF01 fixed
**Branch:** `worktree-feature+flo-router-c` (worktree) off `origin/main` `3659032` · **Merged:** PR #45 (squash → `15dc7c0`)
**Plan:** [build-plan](../2026-06-10-flo-router-build-plan.md) · **Kickoff:** [session-c-kickoff](../2026-06-10-flo-router-session-c-kickoff.md)

## TL;DR

Flo-A (#43) built the router and Flo-B (#44) chose the in-between routes, but **Flo was registered,
not dispatched** — no run chained through `FloNode`. Flo-C made it the **dispatched** Phase-5
generation node via the declarative DAG path, threaded the routing signals onto frame specs, and
fixed the **HF01** square-frame bug on the NB Pro keyframe path — the two prerequisites for the first
integrated end-to-end run ("The Spark, Shared"). All five steps shipped TDD red→green at **$0**:
`tests/` 506 passed, `pipeline/tests/` 10 passed, Em verdict baseline byte-identical.

The single notable event was an **operational incident** — early test edits leaked to the main-repo
path instead of the worktree — caught by the "wrong test count" signal and fully corrected. It is the
post-mortem centerpiece below, because it is exactly the class of mistake [`fleet-ops-protocol.md`](../fleet-ops-protocol.md)
exists to prevent.

## Fleet-ops (§0 before AND after)

- Isolated worktree off `origin/main` `3659032`; divergence `0 0` at start and end; single owner.
  `ANTHROPIC_API_KEY` absent throughout (no spend; Em never invoked). No `.env`/key needed — the
  whole session is stub-green by construction.
- Em's verdict baseline `traces/g6.1b-criteria-attached-2026-06-08.md`
  (`md5 2af75906502f1caf8857e18828ceb2e4`) **byte-identical** before and after — Flo-C never touched
  `evals/vision_critic/`. Production `manifest.yaml` untouched (`phases:` stays `enabled: []`, so a
  real run is byte-identical). Legacy `frame_generate` node untouched.

## C0 — the gap (confirmed against the tree, not the doc)

The kickoff's standing doctrine ("verify against the tree — never the label, including this doc")
paid off three times:

- `grep '"flo"|FloNode|resolve_route'` hit only `frame_router.py` + the registration import in
  `pipeline/nodes/__init__.py` — **nothing dispatched `flo`.**
- The declarative dispatch mechanism **already existed.** `dag.load_graph_from_manifest` reads
  `phases.*.nodes[*]` and dispatches whatever `node:` names; `run_from_legacy_cli` **ignores** the
  `node_id="frame_generate"` arg that `generate.py main()` passes (vestigial). → **No `generate.py`
  change was needed** — the kickoff's "preferred declarative" path was the easy path, and the
  "FrameGenerateNode delegation" fallback was rejected (would conflate the two nodes).
- `nb_pro_runner._build_skill_cmd` built the skill argv with **no `--aspect-ratio`** → the skill
  defaults to 1:1 → fails `audit.check_aspect_ratio` (16:9 ±2%). Only the `nb_pro` routes were
  affected (the `nb2` path goes through `generate_frame`, which already passes `--aspect-ratio 16:9`).

## What shipped

| Step | Change | Files |
|------|--------|-------|
| C1 | `literal_json:` binding form — a node entry can bind a list-valued `references` (and real ints) inline; the keyframe-spec ↔ DAG-input impedance. JSON-parse with a clear `ValueError` on malformed input. Three legacy forms regression-locked. | `pipeline/dag.py`, `tests/test_dag.py` (+7) |
| C2/C3 | `flo` dispatched declaratively via `phases.phase_5.nodes`; bindings supply `shot_type`/`character_id`/`references` so routing is real (hero→NB Pro, standard→NB2; `style_register` from the named character). Worked example as a template, not in production manifest. | `docs/examples/flo-phase5-example.yaml` (new) |
| C4 | HF01 — `aspect_ratio` param on `invoke_image_edit` + `_build_skill_cmd` (appended only when set), folded into the cache key **only when non-None**, and Flo's `nb_pro` branch passes `"16:9"`. | `pipeline/agents/nb_pro_runner.py`, `pipeline/agents/frame_router.py`, `tests/test_nb_pro_runner.py` (+4), `tests/test_frame_router.py` (+1) |
| C5 | stub-green integration smoke `test_flo_phase5_graph_dispatches_via_dag`: a declared two-node `flo` graph dispatches through `load_graph_from_manifest` → `Runner` with both transports faked — proves dispatch, real-list reference binding, 16:9 on nb_pro, route-in-`notes`, no real call. | `tests/test_dag.py` |

**Cy regression-lock (the load-bearing safety property).** Cy's locked-Bible plate generation calls
`invoke_image_edit` with no `aspect_ratio`. To guarantee her cache stays valid, `aspect_ratio` is
folded into the cache key **only when non-None**. Verified by capturing the pre-change digest of a
deterministic no-reference input (`7a84b9130f7bb71ff37bbdcf95bc45cbdf951ca05fa0031e828a7c3281d4258d`)
*before* the edit and asserting the `aspect_ratio=None` path still produces it *after* — a golden-digest
byte-identity lock, not just a "None == omitted" tautology.

## ⚠ Operational incident — test edits leaked to the main repo (caught + corrected)

**What happened.** After `EnterWorktree` switched the session cwd into
`.claude/worktrees/feature+flo-router-c`, I wrote the first C1 test edits using **main-repo absolute
paths** (`/Users/seanwinslow/Code-Brain/anima/tests/test_dag.py`) instead of the worktree path. The
edits landed in the **main working tree**, not the isolated worktree.

**Detection signal.** Running `pytest tests/test_dag.py -k resolve_bindings` from the worktree cwd
returned **"10 deselected"** — i.e. only the *original* 10 tests collected, none of my 7 new ones.
The wrong test count was the tell: the file I was editing and the file pytest was collecting were two
different files. (The PostToolUse diagnostics also reported the edit against the main-repo path, a
second signal.)

**Root cause.** `Edit`/`Read`/`Write` take absolute paths; I reused the main-repo absolute paths from
the Phase-1 exploration reads (which legitimately ran against main, pre-worktree) without re-pointing
them at the worktree after `EnterWorktree`. cwd had changed; my hardcoded paths had not.

**Correction.** `git -C <main-repo> checkout -- tests/test_dag.py` restored main to pristine (the
file was unmodified at session start, so the restore was clean), then re-applied every edit against
the worktree absolute path. Confirmed main clean and the worktree carried the changes before
continuing. No work lost; no main-branch pollution shipped.

**Prevention (for the next worktree session).**
- After `EnterWorktree`, treat the worktree path as the *only* valid edit root. Prefer
  **worktree-relative** invocations or the worktree absolute path; do not reuse pre-worktree
  exploration paths verbatim.
- Re-`Read` a file at its worktree path before the first `Edit` (the tool requires it anyway — that
  requirement is itself a guard if you respect it per-path).
- **"Wrong test/collection count" is an isolation tell, not a test-filter quirk** — when `-k` deselects
  everything you expect to match, suspect a path/cwd split before suspecting the filter.
- A `git -C <main-repo> status -s` spot-check after the first worktree edit cheaply confirms the main
  tree is still clean.

This mirrors the operational-incident class that prompted [`fleet-ops-protocol.md`](../fleet-ops-protocol.md)
(adopted 2026-06-02 after three incidents) — "one isolated worktree per plan" only protects you if
every mutation actually lands *in* it.

## Verification

- `python -m pytest tests/` → **506 passed**; `python -m pytest pipeline/tests/` → **10 passed**
  (run separately per the duplicate-`tests`-package rule).
- Focused touched-suite re-run (`test_dag.py test_frame_router.py test_nb_pro_runner.py`) → 47 passed.
- Read-only graph-load of `docs/examples/flo-phase5-example.yaml` confirmed it parses (two `flo`
  nodes, full routing table) **without executing** — the example is deliberately *not* run live (its
  nb2 node would abort without a key or spend with one; the stub-green CI smoke is the authoritative
  proof).
- §0 guard clean before and after; baseline md5 unchanged; main-repo working tree clean at teardown.

## Out of scope (the run session this unblocks)

Authoring the real Sean-+-mascot scene graph, the Maya brief/plan, the costed generation, the Em/T3
critique pass, assembly, and museum capture — i.e. the first integrated end-to-end run, "The Spark,
Shared" ([studio brief](../../briefs/2026-06-10-spark-shared/00_studio_brief.md)). Flo-C is the $0
wiring that makes those possible.
