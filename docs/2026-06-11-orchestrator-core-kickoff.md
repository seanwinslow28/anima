# Kickoff — Run Orchestrator, Slice 2: the core build ($0 stub-green, TDD)

*Paste the block below into a fresh Claude Code session in the `anima` repo. Self-contained.
Plan of record: [`docs/2026-06-11-orchestrator-core-build-plan.md`](2026-06-11-orchestrator-core-build-plan.md).*

---

You're building the **run orchestrator** — `python -m pipeline.run` — the one-command chainer
that turns the 16 hand-wired joins of the first integrated run into a single resumable program.
The build is **$0 / stub-green / TDD**; a costed end-to-end validation runs separately, out of
session. Read these first, in order: [`docs/2026-06-11-orchestrator-core-build-plan.md`](docs/2026-06-11-orchestrator-core-build-plan.md)
(the spec), [`docs/anima-test-runs/2026-06-11-first-integrated-run.md`](docs/anima-test-runs/2026-06-11-first-integrated-run.md)
(the 16 seams), `PHILOSOPHY.md`, `CLAUDE.md`. The prototype you're generalizing:
`scripts/author_plan.py` (PLAN stage) + `scripts/spark_frame.py` (per-frame loop).

**What it does:** drive Maya → stop at the plan gate → per frame run Flo → T1 → Em (per
character) → stage patches → stop for Sean's eye → retry with a correction note → chain the
next frame off the approved one → assemble the loop. **Museum capture (seam #14) is Slice 3 —
explicitly OUT.** So is seam #10 (Em CC01 — eval-gated, ticketed). Don't touch
`evals/vision_critic/`.

## The load-bearing finding (verify it yourself first)

`pipeline/dag.py`'s `Runner.execute(graph)` is a **batch executor** — no pause/resume (confirm:
read it). So the orchestrator is a **resumable stage machine** that owns the human gates and the
per-frame loop, and *uses* the Runner only for static sub-graphs (one frame's Flo→T1→Em fan).
The per-frame gate (eye + retry, each frame chained off the *approved* prior) is the genuinely
new mechanism. Don't try to express it as one static graph.

## Doctrine — non-negotiable

- **Verify against the tree, never trust a label — including this kickoff and the plan.**
  Re-confirm every claim before building on it: that `Runner` has no resume; that
  `_resolve_bindings` supports the upstream-output binding form you need for the per-frame fan;
  that `query_by_character` keys on the IR namespace (`sean`), not the folder key
  (`sean-anchor`); that `stage_patches_hook` is a `post_run` hook. Cautionary tales: a runbook
  claimed a loop self-isolates and the run crashed on case #0; Flo's CHANGELOG read "built"
  while nothing dispatched it.
- **Em verdict-baseline guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md`
  must stay `2af75906502f1caf8857e18828ceb2e4`. Nothing here reaches `evals/vision_critic/`.
- **$0 — stub-green only.** Every node has a stub fallback (Maya Opus-text stub, Flo placeholder
  PNG, Em stub verdict). The whole build exercises with faked transports. No model spend this
  session. The costed validation is a separate out-of-session step (below).
- **TDD red→green per phase.** Reuse the prototypes' logic (extract shared helpers); don't fork it.

## §0 — fleet-ops gates (before any edit)

Per [`docs/fleet-ops-protocol.md`](docs/fleet-ops-protocol.md). $0, but the worktree discipline
holds (the 2026-06-10 path-leak was a $0 session).

```bash
cd <anima main checkout>
git fetch origin
git log --oneline -1 origin/main          # expect ec81cf0 (#49) or newer
git rev-list --left-right --count origin/main...HEAD   # expect 0 0 on a clean base
md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md  # 2af75906502f1caf8857e18828ceb2e4
echo "${ANTHROPIC_API_KEY:-ABSENT}"        # expect ABSENT
```

One isolated worktree off `origin/main`; ALL edits inside it (after the worktree switch, that
path is the only valid edit root — treat a surprising test-collection count as an isolation
tell; spot-check `git -C <main> status -s` clean after your first edit). Baseline green:

```bash
python -m pytest tests/ -q          # contract suite (Slice 1 left it at 519 passed / 2 skipped credential-free)
python -m pytest pipeline/tests/ -q # Seedance (run separately — duplicate `tests` basename)
```

If you see 2 `test_frame_router` nb_pro failures, check for a `.env` in the checkout — those
tests are credential-free by design and attempt a real call only when a `.env`/`GEMINI_API_KEY`
is present (`nb_pro_runner._has_gemini_key` reads the project `.env`). That's an env artifact,
not a regression — confirm by running them with the key unset.

## Build it in phases, each red→green

**P0 — state model.** `pipeline/run.py` + `runs/<id>/run_state.json` (schema in the plan):
read / write / `--resume` / `--status`, the stage enum (`PLAN→GENERATE→ASSEMBLE→DONE`), and the
transitions. Tests: round-trip the state file; resume re-instantiates and continues; `--status`
renders without advancing.

**P1 — PLAN stage.** Extract `author_plan.py`'s guards (live-Opus smoke + the stub-marker scan)
+ the Maya drive into a shared helper `pipeline/run.py` imports. `--brief` runs Maya (stub),
emits `plan.md` + `acceptance_criteria.json` + the cost preview, sets `plan.status=drafted`,
prints the summary, exits at the gate. `--approve-plan` locks criteria (mirror
`pipeline.cli plan approve`), wires `criteria_sources.brief_file` from `brief.active_dir` +
builds the bundle once via `load_all_criteria` (seam #8), advances to GENERATE. Tests on the
stub path (no real Opus).

**P2 — GENERATE loop.** Externalize `spark_frame.py`'s `FRAMES` into a `shots.yaml` the brief
dir carries (schema in the plan — `id` / `cast` (IR namespaces) / `beat` / `prompt` /
`extra_references` / `hold`). Derive `state.cast` once (folder keys from manifest `characters:`;
IR namespace from each Bible's `acceptance_criteria.json` id prefix — seams #9 + #11). Per
frame: resolve references (chain off the prior **approved** frame + the shot's plates), build an
in-memory `Graph` (`flo_FN` → `audit_FN` + one `em_FN_<ns>` per cast namespace), run it through
`Runner.execute` with `add_hook("post_run", stage_patches_hook(run_dir))` — **patch staging
fires for free** (seam #7). Persist candidate + verdicts + patches; print; exit at the eye gate.
`--approve-frame N [--attempt K]` locks the attempt → `approved/<slug>_F0N_key.png` and chains
N+1 (or → ASSEMBLE if last); `--retry-frame N --note "..."` re-rolls with the note appended.
*Fallback* if the per-frame graph proves heavy: call the nodes directly + fire
`stage_patches_hook` by hand (as `spark_frame.py` does) and leave a TODO to move to the Runner —
but lean Runner. Tests: chaining references, retry-with-note, two-cast vs one-cast Em passes.

**P3 — ASSEMBLE tail.** Write `export/sequence.txt` from `frame_order` + `holds`, drive the
generalized `assemble.sh` (#13) with `--slug` + `--sequence-file` (consuming the
#12-normalized PNGs), produce the loop, set `stage=DONE`, print the paths. Test with the
fake-ffmpeg PATH shim Slice 1 already uses (`tests/test_assemble.py`) — assert the staged
sequence + planned output names, no real encode.

**P4 — integration smoke + durability.** A full stub-green `brief → loop` run that auto-approves
each gate in-test: assert the stage transitions, the resume round-trip (write state,
re-instantiate, continue), and the loop outputs exist. Plus: interrupt mid-GENERATE, re-invoke,
assert state intact.

## Done criteria

- `python -m pipeline.run` works end to end on the **stub path**: `--brief` → plan gate →
  `--approve-plan` → per-frame eye gates (`--approve-frame` / `--retry-frame --note`) →
  ASSEMBLE → `DONE`, all driven by `--resume` against a durable `run_state.json`.
- `shots.yaml` authored for "The Spark, Shared" (externalized from `spark_frame.py`'s `FRAMES`) —
  the costed validation input.
- `python -m pytest tests/ -q` + `python -m pytest pipeline/tests/ -q` green credential-free;
  Slice 1's golden PT_A1 assemble test still green.
- `md5sum …/g6.1b-criteria-attached-2026-06-08.md` == `2af75906502f1caf8857e18828ceb2e4`.
- `git -C <main> status -s` clean (no worktree leak).
- CHANGELOG.md entry (decision-log voice + the md5 line + test counts). CLAUDE.md updated — a new
  top-level command (`python -m pipeline.run`) in Key Commands + the orchestrator framed in the
  architecture/skills section.
- Land as one squash PR off `origin/main`. Clean worktree teardown.

## What's NOT in this session

- **No costed run.** The real Maya/Flo/Em/assemble end-to-end is a **separate, out-of-session**
  step: run `python -m pipeline.run` from a **plain terminal** (not inside Claude Code — the
  nested-SDK throttle, seam #4) on "The Spark, Shared" or a fresh tiny 2-frame piece, under
  fleet-ops §0. That's the proof; this session is the $0 machine that makes it possible.
- **No museum capture (#14)** — Slice 3. **No Em CC01 (#10)** — eval-gated, ticketed.

When done, report: the CLI surface as built, the `run_state.json` schema, how the per-frame fan
runs (Runner vs fallback + why), the `shots.yaml` you authored, and the final test counts.
