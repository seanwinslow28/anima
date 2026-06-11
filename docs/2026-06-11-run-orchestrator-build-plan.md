# Run Orchestrator — Build Plan

**Date:** 2026-06-11
**Status:** Planned. Slice 1 (cleanup pass) is the first executable Claude Code session.
**Predecessor:** [`docs/anima-test-runs/2026-06-11-first-integrated-run.md`](anima-test-runs/2026-06-11-first-integrated-run.md) — the field report whose 16 seams are this build's spec.
**The piece that proved the nodes:** `runs/2026-06-11-spark-shared-first-integrated/export/SS_L1_loop.{gif,mp4,webm}` ("The Spark, Shared" — SHIPS, Sean's eye).

---

## Why this exists

The fleet ran end-to-end as one chain for the first time and shipped a piece. The nodes
are solid — Maya plans, Flo routes, Em critiques with grounded citations, FFmpeg assembles,
Mo + the T3 gate capture. But **every join between those nodes was hand-wired**, and the
field report logged sixteen of those joins as seams. Those seams *are* the orchestrator's
spec. This is not a from-scratch agent build: the hard parts (typed nodes, content-addressed
caching, `post_run` hooks) already live in `pipeline/dag.py`. The orchestrator is the missing
connective tissue — the thing that turns sixteen hand-wired steps into `python -m pipeline.run`.

## The decisions that shape this build (forks resolved 2026-06-11)

Four strategy forks were put to Sean before planning. The answers shape everything below.

| Fork | Decision | Consequence |
|------|----------|-------------|
| **Slicing** | Cleanup pass first, then core | Slice 1 = the $0 TDD bug fixes; the orchestrator builds on a clean base. |
| **Run context** | Standalone shell, uncontended | The orchestrator runs from a plain shell, not inside a Claude Code session — heavy Opus nodes (Maya, T3) run without the nested-SDK throttle. |
| **Museum #14** | Defer until after core | The portfolio-museum payoff comes after the orchestrator end-to-end works; the shipped Spark loop waits in `runs/`. |
| **Gate UX** | Durable state file + `--resume` | The human gate is a persisted state machine, not a blocking process — survives a laptop close, pairs with standalone execution. |

`#10` (Em's absolute stylus-hand verdict is noisy in profile) is **deliberately out of every slice
here.** It changes Em's verdicts, which means re-running her eval baseline — it carries
eval-baseline blast radius the cleanup pass must not. It is its own eval-gated track, ticketed
separately. The cleanup pass is the three bugs with *zero* reach into `evals/vision_critic/`.

---

## The load-bearing architecture finding

Before the slices, the one thing that reframes the whole build — verified against the tree this session, not taken from the prompt:

**`pipeline/dag.py`'s `Runner` is a batch executor.** `Runner.execute(graph)` topologically
sorts the graph, runs ready nodes in a thread pool, caches each result by content hash, fires
`post_run` hooks, and returns when the graph is drained. It runs **straight through with no
way to stop.** There is no pause, no human gate, no resume. That is correct for a static
graph and wrong for what the run actually needed.

The run had **two kinds of human gate**:

1. **A coarse gate** after Maya — present `plan.md` + the cost preview, Sean approves, *then*
   any generation spend is unlocked. This one is easy: it's a stage boundary. The orchestrator
   stops between stages.

2. **A per-frame gate inside Phase 5** — generate frame *N*, run T1 + Em (twice, once per
   character), present the image for Sean's eye, maybe retry with a correction note, and only
   once it's approved chain frame *N+1* off that **approved** frame. This one is **not
   expressible as a static DAG.** The graph's shape depends on runtime human decisions (how
   many retries? which attempt becomes the peak?), and each frame's inputs depend on the prior
   frame's *approval*, not just its computation.

So the orchestrator is really two things stitched together:

- **A standalone, resumable stage driver / state machine** — owns the gates, the per-frame
  loop, and the durable run state. This is the genuinely new mechanism. Its prototype already
  exists: `scripts/author_plan.py` (the Maya driver) and `scripts/spark_frame.py` (the
  per-frame Flo→T1→Em loop) are exactly this, hand-written for one run.
- **The DAG `Runner`, used *within* a stage** for the parts that genuinely *are* a static
  graph — a single frame's Flo→T1→Em fan, and the final assemble→museum tail. Here the
  `post_run` hook fires patch staging for free (seam #7 disappears the moment we run through
  the Runner instead of inline).

Running it from a **plain shell** (not inside a Claude Code session) does double duty: it
removes the ~285–390s nested-SDK throttle per Opus call (seams #4 + the stalled T3 gate), and
it makes the pause-resume gate natural — the orchestrator is a process that writes state,
prints what to look at, and **exits** at a gate; Sean approves; a re-invoke resumes from state.

---

## The slice plan

### Slice 1 — Cleanup pass (THIS kickoff) · $0 · TDD · no model spend

Three independent bug fixes the orchestrator's stages will otherwise have to work around.
All verifiable by unit test; none touch `evals/vision_critic/`.

- **#5 — `cost_estimator._phase_2_cost` double-counts locked Bibles.** Skip a character's
  plate cost when its Bible is locked.
- **#12 — Gemini saves JPEG-as-`.png`.** Normalize candidates to real PNG at the source
  (the FloNode return boundary), keep `assemble.sh`'s existing re-encode as a backstop.
- **#13 — `assemble.sh` is hardcoded to the PT_A1 sequence.** Generalize it to accept a
  per-piece sequence + output slug, with the PT_A1 sequence as a byte-identical default.

Full per-bug spec below; the paste-ready session prompt is
[`docs/2026-06-11-orchestrator-cleanup-pass-kickoff.md`](2026-06-11-orchestrator-cleanup-pass-kickoff.md).

### Slice 2 — Orchestrator core · the main build

`python -m pipeline.run` — a standalone, resumable stage machine. Sketch below; gets its own
build plan once Slice 1 lands and the base is clean.

### Slice 3 — Museum capture (seam #14) · the portfolio gate

A keyframe-loop exhibit kind + `project_slug` so a run actually lands in the museum; backfill
the already-shipped Spark loop. Unblocks the `sw-ai-pm-portfolio` Astro export. Sketch below.

---

## Slice 1 — detailed spec

Every fix is grounded in a tree check done this session, stated so the build session can
re-verify rather than trust this doc.

### #5 — Cost estimator skips locked Bibles

**Verified diagnosis.** `pipeline/agents/cost_estimator.py::_phase_2_cost` reads each
registered character's `plate_generation_plan.json` and prices every non-`ingest:` plate at
`_NB_PRO_USD_PER_PLATE`. It **never checks lock state.** Both `characters/sean-anchor/` and
`characters/claude-mascot/` carry `acceptance_criteria.json` with `locked: true`. So an
`animation_piece` run against those locked Bibles bills a phantom ~$5.40 Phase-2 band for a
bake it will never do. The method's own docstring claims animation-piece runs "don't re-pay" —
but the code only returns $0 when there is *no* `characters:` block at all; a registered-but-
locked Bible (exactly what an animation piece needs, to load references) gets priced.

**The fix.** In `_phase_2_cost`, for each character, detect whether its Bible is locked and
contribute $0 if so. The authoritative per-Bible lock signal is the character's own
`acceptance_criteria.json` `locked: true` (this is what `pipeline.cli bible approve` flips, and
`pipeline/criteria.py::load_criteria(...).locked` already reads it). Read it from
`<folder>/acceptance_criteria.json` adjacent to the plate plan. A character with no lock file,
or `locked: false`, prices its plates exactly as today (preserves the genuine
Bible-authoring-run estimate).

**The test.** In `tests/test_cost_estimator.py`: a manifest registering a character whose
`acceptance_criteria.json` is `locked: true` → `phase_2` band is `$0.00`; an unlocked character
with a plate plan → prices the plates (lock the existing behavior so the fix is surgical). Use
a tmp fixture dir; do not point at the real `characters/` (keep the test hermetic).

### #12 — Normalize JPEG-as-PNG at the source

**Verified diagnosis.** `runs/.../approved/SS_F01_key.png` is **JPEG data with a `.png`
extension** (`file` reports "JPEG image data … 1376x768"; PIL reports `format='JPEG'`). The
Gemini pencil skill writes JPEG bytes to `attempt_NN.png`; ffmpeg's PNG decoder rejects them
(`Conversion failed!`). The run worked around it with a hand-staged sequence. Note: this is
entangled with #13 — `assemble.sh` *already* carries a "Step 2b" PIL re-encode, but the run
never reached it because `assemble.sh` is PT_A1-hardcoded (#13) and was bypassed.

**The fix (source, not just pre-ffmpeg).** Every generation route funnels through
`FloNode.run` (`pipeline/agents/frame_router.py`), which emits `candidate_path`. Add a small
`normalize_to_png(path)` helper (PIL: open, and if `img.format != "PNG"`, re-save as PNG in
place) and call it at the FloNode return boundary, before `candidate_path` is handed back. That
makes every downstream consumer — Em, assemble, *and* the future museum capture (#14), which
copies these frames as thumbnails — receive a real PNG. Keep `assemble.sh`'s Step 2b as a
defensive backstop (belt and suspenders, the way `author_plan.py`'s stub guard is). Decide the
helper's home during the build (a `pipeline/` util module or alongside `generate.py`); the call
site is the FloNode boundary regardless.

**The test.** A unit test that writes JPEG bytes to a `*.png` path, runs `normalize_to_png`,
and asserts `Image.open(path).format == "PNG"`; plus a FloNode-level test (stub transport) that
a JPEG-as-PNG candidate comes back PNG. Idempotent on an already-PNG file (no-op, no needless
rewrite).

### #13 — Generalize `assemble.sh` (PT_A1 stays byte-identical)

**Verified diagnosis.** `pipeline/assemble.sh` hardcodes: the `FRAME_SEQ` (a 27-entry PT_A1
key/in-between sequence with holds), the `PT_A1_${ASSET}.png` source-path prefix, the
`pencil-test-act1.{mp4,webm,gif}` output names, and a `1920×1080` scale. A new piece (different
keys like `SS_F01_key`, different holds, a different slug) is invisible to it. The `assemble`
*node* (`pipeline/nodes/assemble.py`) just shells to this script with `run_dir`, and its
docstring makes back-compat load-bearing: "Byte-identical to direct invocation; that's the
verification step."

**The fix.** Let the assembler take a **sequence spec** and an **output slug**, defaulting to
the current PT_A1 behavior when neither is supplied. Concretely:

- A per-run sequence source — e.g. an optional `export/sequence.txt` (the same
  `KEY:hold` line format the script already parses internally) plus a `--slug <name>` (and the
  source-path prefix derived from the keys, e.g. `SS_F03b_key` not `PT_A1_*`). When absent,
  fall back to the embedded PT_A1 `FRAME_SEQ` + `PT_A1_` prefix + `pencil-test-act1` slug.
- Keep Step 2b (the JPEG→PNG re-encode) in the generalized path.
- Thread an optional `slug` / `sequence_file` through `AssembleNode` inputs (default → legacy),
  so Slice 2's orchestrator can drive it; absent inputs = today's behavior.

**The test (the load-bearing one).** A golden back-compat test: assembling the PT_A1 reference
sequence with no slug/sequence args produces a **byte-identical** frame sequence + the same
output filenames as before (mirror how Flo-C regression-locked the NB-Pro cache key against a
captured golden digest). Plus a positive test: a small custom sequence + slug (e.g. two
`SS_*` keys, holds `2,2`) produces the slugged outputs from the right sources. Keep these
hermetic (tmp run dir, tiny generated PNGs).

### Slice 1 guard rails (apply to the whole pass)

- **Em baseline untouched.** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md`
  stays `2af75906502f1caf8857e18828ceb2e4`. Nothing in this slice reaches `evals/vision_critic/`.
- **Fleet-ops even at $0.** One isolated worktree off `origin/main`, single owner, `ANTHROPIC_API_KEY`
  absent, divergence `0 0` before. No model spend in this slice (pure code + unit tests), but the
  worktree discipline still applies (the 2026-06-10 path-leak incident happened on a $0 session).
- **TDD red→green per bug**, independent commits so each fix is revertible alone.
- **State of record.** CHANGELOG entry (decision-log voice, with the md5-guard line); CLAUDE.md
  touch only if a convention/command changed (the assembler's new sequence/slug interface likely
  warrants a one-line note in the assemble command block).

---

## Slice 2 — Orchestrator core (sketch)

`python -m pipeline.run` — a standalone, resumable stage machine run from a plain shell. Its
internals are `author_plan.py` + `spark_frame.py`, generalized and given persistent state.

**Shape.**

- **CLI.** `python -m pipeline.run --brief <dir>` starts a run; `--resume <run-dir>` continues
  one; per-frame controls `--approve-frame N [--attempt K]`, `--retry-frame N --note "..."`;
  `--from <stage>` re-enters a stage. A new `pipeline/run.py` (none exists today; the CLI
  package has `bible`, `patches`, `plan`).
- **Durable state.** `runs/<id>/run_state.json` records: plan status (drafted / approved),
  per-frame status (pending / generated / approved + which attempt), the active stage, and the
  criteria-bundle wiring. The orchestrator reads it on `--resume` and writes it at every gate.
- **Stages.** `PLAN` (drive Maya with `MAYA_CALL_TIMEOUT_S` + the parsed envelope + the stub
  guard → stop at the plan gate) → `GENERATE` (per-frame: Flo → T1 → Em×(both namespaces) →
  stage patches via the Runner's `post_run` hook → stop at the eye; `--retry` re-rolls with a
  correction note; `--approve` chains the next frame off the approved one) → `ASSEMBLE` (the
  generalized #13 assembler, consuming #12-normalized PNGs, arbitrary keys + variable holds) →
  `MUSEUM` (Slice 3). Heavy Opus stages (`PLAN`, and later the T3 gate) run uncontended because
  the process is a plain shell.

**Seams this stage absorbs:** #1, #6, #7, #8, #9, #11, #16 directly; #2, #3 already fixed (#47);
#12, #13 land in Slice 1; #5 lands in Slice 1; #4 is answered by *where* it runs; #14 is Slice 3.

## Slice 3 — Museum capture, seam #14 (sketch)

A new exhibit kind for a keyframe-loop run + a `project_slug` that classifies a fresh
integrated piece, so `scripts/build_museum.py` copies the loop (GIF/WebM/MP4 + filmstrip +
approved keys, including the F03b peak) into a real exhibit instead of a thin `_unclassified`
0-asset one. Mo narrates it. First payoff: **backfill the already-shipped Spark loop** — it's
portfolio-worthy now. Unblocks the `sw-ai-pm-portfolio` Astro export. Schema source of truth:
[`docs/museum-exhibit-schema.md`](museum-exhibit-schema.md). Run the T3 pre-publish gate over
*this* exhibit (it carries real visual assets), **out of session** (the lesson from the stalled
in-session gate).

---

## Seam → slice traceability (all 16)

So nothing in the field report falls through.

| # | Seam | Lands in |
|---|------|----------|
| 1 | No `author_plan.py` | **Done** (#47); generalized into Slice 2's PLAN stage |
| 2 | PlannerNode 120s timeout | **Done** (#47, `MAYA_CALL_TIMEOUT_S`) |
| 3 | PlannerNode envelope parser | **Done** (#47, brace-balanced extraction) |
| 4 | Nested-SDK throttle | **Answered by architecture** — Slice 2 runs standalone (fork: run context) |
| 5 | Cost double-counts locked Bibles | **Slice 1** |
| 6 | Em has no CLI | Slice 2 (driven inside the GENERATE stage) |
| 7 | Patch staging needs the DAG `post_run` hook | Slice 2 (run the frame fan through the Runner) |
| 8 | `ctx.criteria` bundle + `brief_file` auto-wire | Slice 2 (wire the bundle once at run start) |
| 9 | Em is single-character, IR-namespace-keyed | Slice 2 (two Em passes on `sean` / `claude-mascot`) |
| 10 | Em absolute stylus-hand noisy in profile | **Out — separate eval-gated track** (ticketed) |
| 11 | `character_id` means different things to Flo vs Em | Slice 2 (thread both the folder key + the namespace) |
| 12 | Gemini saves JPEG-as-`.png` | **Slice 1** |
| 13 | `assemble.sh` hardcoded to PT_A1 | **Slice 1** |
| 14 | Museum has no keyframe-loop exhibit / slug | **Slice 3** |
| 15 | Bash CWD unreliable between calls | Slice 2 (orchestrator uses absolute run paths; not a code fix so much as a discipline the single process enforces) |
| 16 | Whole chain + per-frame gate hand-wired | **Slice 2** (the orchestrator itself) |

---

## Verification (this session's planning)

Grounded against the tree, not the prompt:

- HEAD `f157564` (#48), clean, divergence `0 0`.
- Em baseline md5 `2af75906502f1caf8857e18828ceb2e4` — intact.
- `pipeline/dag.py` `Runner.execute` confirmed batch-only (no pause/resume) — the architecture finding.
- Registered nodes present: `planner`, `flo`, `audit_gate`, `vision_critic`, `assemble`, `museum_writer` (+ `cost_estimator`, `t3_council`).
- #5 confirmed: `_phase_2_cost` ignores lock state; both Bibles `locked: true`.
- #12 confirmed: `SS_F01_key.png` is JPEG data; the generate write path is the source; `assemble.sh` Step 2b is an existing backstop.
- #13 confirmed: `FRAME_SEQ` + `PT_A1_` prefix + `pencil-test-act1` outputs are hardcoded.
- No `pipeline/run.py` exists; CLI has `bible`/`patches`/`plan`.

## Open questions (for Slice 2, not Slice 1)

- Where the per-frame loop's "present for the eye" boundary lives when run standalone (the
  process prints the candidate path + Em's verdict and exits; Sean opens the image, re-invokes
  to approve/retry) — confirm that round-trip feels right on the first real orchestrated run.
- Whether `ASSEMBLE` reads a human-authored `sequence.txt` or the orchestrator derives the
  sequence from the approved-frame order + a holds policy. (Slice 1 makes the assembler accept
  either; Slice 2 decides who writes it.)
