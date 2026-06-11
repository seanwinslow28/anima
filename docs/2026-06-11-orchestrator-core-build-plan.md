# Run Orchestrator — Slice 2: the core build plan

**Date:** 2026-06-11
**Status:** Planned. The build session runs $0/stub-green; a costed end-to-end validation follows out-of-session.
**Predecessors:** Slice 1 (cleanup) landed clean at `ec81cf0` (#49) — `_phase_2_cost` skips locked Bibles, JPEG-as-PNG normalized at the FloNode boundary, `assemble.sh` generalized (PT_A1 byte-identical). The arc + the seam→slice map: [`docs/2026-06-11-run-orchestrator-build-plan.md`](2026-06-11-run-orchestrator-build-plan.md). The seam spec: [`docs/anima-test-runs/2026-06-11-first-integrated-run.md`](anima-test-runs/2026-06-11-first-integrated-run.md).

---

## What this is

`python -m pipeline.run` — the one-command chainer that turns the sixteen hand-wired joins of
the first integrated run into a single resumable program. It drives Maya, stops at the plan
gate, then per frame runs Flo → T1 → Em (per character) → stages patches → stops for Sean's
eye → retries with a correction note → chains the next frame off the approved one → assembles
the loop. The nodes already exist and are proven; **this is the connective tissue, not new
agents.** Museum capture (seam #14) is Slice 3 — explicitly out of this build.

**Decisions carried in (resolved with Sean 2026-06-11):** one full build (not sub-sliced);
runs standalone from a plain shell (heavy Opus nodes uncontended); durable state file +
`--resume` for the human gates; museum deferred to Slice 3.

## The load-bearing finding this build rests on

`pipeline/dag.py`'s `Runner.execute(graph)` is a **batch executor** — topological sort →
thread-pool → content-addressed cache → `post_run` hooks → return. No pause, no resume. So the
orchestrator is **not** "one big graph." It is a **resumable stage machine** that owns the
human gates and the per-frame loop, and *uses* the Runner only where the work genuinely is a
static sub-graph (one frame's Flo→T1→Em fan; the assemble tail). The Phase-5 per-frame gate —
eye + retry, each frame chained off the *approved* prior — can't be a static DAG because its
shape depends on runtime human decisions. That gate is the genuinely new mechanism, and its
prototype is already on disk: `scripts/author_plan.py` (PLAN) + `scripts/spark_frame.py`
(the per-frame loop).

---

## Architecture

### Module + CLI surface

A new `pipeline/run.py`, invoked as `python -m pipeline.run`. (Verified: none exists; the CLI
package today is `bible` / `patches` / `plan`.) Standalone — a plain-shell process that reads
state, advances to the next gate, prints what to look at, and **exits**. Subscription billing
via the `claude` CLI OAuth (fleet-ops-compatible; the `ANTHROPIC_API_KEY`-absent guard from
`author_plan.py` carries over).

```
python -m pipeline.run --brief <dir> [--slug SS] [--run-dir <dir>]
        # start: wire criteria once, run PLAN (drive Maya), stop at the plan gate.

python -m pipeline.run --resume <run-dir> --approve-plan
        # lock criteria, enter GENERATE, generate frame 1, stop at its eye gate.

python -m pipeline.run --resume <run-dir> --approve-frame N [--attempt K]
        # lock attempt → approved/, chain + generate frame N+1 (or → ASSEMBLE if last).

python -m pipeline.run --resume <run-dir> --retry-frame N --note "<correction>"
        # re-roll frame N with the note appended; stop at its eye gate again.

python -m pipeline.run --resume <run-dir> --status     # print state, no advance.
```

### Durable state — `runs/<id>/run_state.json`

The single source of truth across invocations. Concrete shape (the build refines field names
against the prototypes):

```json
{
  "run_id": "2026-06-12-...", "brief_dir": "briefs/...", "slug": "SS",
  "stage": "PLAN | GENERATE | ASSEMBLE | DONE",
  "cast": [{"folder_key": "sean-anchor", "ir_namespace": "sean"},
           {"folder_key": "claude-mascot", "ir_namespace": "claude-mascot"}],
  "plan": {"status": "drafted|approved", "plan_path": "...",
           "criteria_path": "...", "brief_file": "..."},
  "frame_order": [1, 2, 3, 4, 5],
  "frames": {
    "1": {"status": "pending|generated|approved", "attempts": [...],
          "approved_attempt": null, "candidate": "...", "em_verdicts": [...]}
  },
  "holds": {"1": 2, "2": 2, "3": 2, "4": 2, "5": 2}
}
```

Read on `--resume`, written at every gate. Survives a laptop close. `--status` renders it.

### The input contract (the key design decision)

The orchestrator consumes a **brief dir** holding two human-authored inputs:

1. `00_studio_brief.md` — Maya's input (already the convention; `author_plan.py` reads it).
2. A **shot list** — `shots.yaml` — externalizing what `spark_frame.py`'s hard-coded `FRAMES`
   dict held: per frame, the `prompt`, the `beat` (Em's beat_description), the extra references
   (e.g. a mascot motion/expression plate), and which cast members appear in the frame.

This is deliberate and aligns with the philosophy: **Phase 3 (storyboard / shot list) is
human-authored today** (Sam + Bea aren't built). Maya plans and sets the acceptance criteria;
the human shot list drives generation. The orchestrator stays general — it never invents
frame prompts. The build **externalizes `spark_frame.py`'s `FRAMES` into this schema** and the
GENERATE stage consumes it. The spark brief gets a `shots.yaml` derived from that dict, which
doubles as the validation-run input.

A first-cut `shots.yaml` (the build confirms the exact keys against `spark_frame.py`):

```yaml
slug: SS
frames:
  - id: 1
    cast: [sean, claude-mascot]          # IR namespaces present in this frame
    beat: "Establishing two-shot: Sean three-quarter at his desk…"
    prompt: "Wide two-shot establishing frame…"
    extra_references: [characters/claude-mascot/source-refs/sean-with-claude-mascot.png]
    hold: 2
  - id: 2
    cast: [sean, claude-mascot]
    beat: "The draw: Sean stays focused… the mascot turns to LOOK down…"
    prompt: "Same two-shot…"
    extra_references: [characters/claude-mascot/motion_plates/look-01.png]
    hold: 2
  # … F03–F05
```

### Cast / namespace discovery (seams #9 + #11)

`character_id` means different things to different nodes: **Flo** wants the manifest/folder key
(`sean-anchor`, for `style_register`); **Em** wants the IR namespace (`sean`,
`query_by_character("sean")` → 31 rules; `"sean-anchor"` → 0). The orchestrator threads both.
Derive the cast once at run start: folder keys from manifest `characters:`; the IR namespace
from each Bible's `acceptance_criteria.json` (its `IR.<namespace>.*` rule prefix is
unambiguous). Persist to `state.cast`. Per frame, `shots.yaml`'s `cast:` names the namespaces
present (a Sean-only frame runs one Em pass, not two). The build verifies the namespace surface
against `pipeline/criteria.py` (`query_by_character` keys + the criteria id prefixes).

### Stage flow (what each invocation does)

- **PLAN.** Reuse `author_plan.py`'s guards (live-Opus smoke + the stub-marker scan — the
  silent-stub trap), drive `PlannerNode` (the #47 fixes: `MAYA_CALL_TIMEOUT_S`, the
  brace-balanced envelope parse). Emit `plan.md` + `acceptance_criteria.json` + the cost
  preview. `plan.status=drafted`, `stage=PLAN`. Print the plan summary + cost band. **Exit.**
- **`--approve-plan`.** Lock criteria (mirror `pipeline.cli plan approve` → `criteria_locked`).
  Wire `criteria_sources.brief_file` from `brief.active_dir` and build the bundle once via
  `load_all_criteria` (seam #8). `stage=GENERATE`. Generate frame 1, stop at its eye gate.
- **GENERATE (per frame).** Resolve references (frame 1: Bible anchors + the cast pairing;
  frame N: F01 + the prior **approved** frame + the shot's extra plates — the chain). Run the
  per-frame fan (below). Persist candidate + T1 + Em verdicts + staged patches to state +
  `em_verdicts.jsonl`. Print the candidate path + verdicts. **Exit** (eye gate).
- **`--approve-frame N`.** Copy the attempt → `approved/<slug>_F0N_key.png`, mark approved.
  More frames → generate N+1, stop at its gate. Last frame → `stage=ASSEMBLE`.
- **`--retry-frame N --note`.** Re-roll N with the note appended to the prompt (the retry
  ladder). New attempt, stop at the eye gate.
- **ASSEMBLE (auto, all frames approved).** Write `export/sequence.txt` from `frame_order` +
  `holds`, run the generalized `assemble.sh` (#13) with `--slug` + `--sequence-file`, consuming
  the #12-normalized PNGs. Produce the loop. `stage=DONE`. Print the loop paths. (Museum =
  Slice 3.)

### The per-frame fan through the DAG Runner (dissolves seam #7)

For the current frame, build an in-memory `Graph` programmatically: `flo_FN` (flo) →
`audit_FN` (audit_gate, binds `flo_FN.candidate_path`) + one `em_FN_<ns>` (vision_critic) per
cast namespace (also binding the candidate). Run it through `Runner.execute(graph)` with
`runner.add_hook("post_run", stage_patches_hook(run_dir))` — and **patch staging fires for
free** (seam #7: inline `run()` never fired the hook; spark_frame.py called it by hand). The
content-addressed cache means a retry with a different note → different prompt → different
cache key → re-runs only what changed. This is the recommended path — it uses the engine as
designed. *Fallback:* if per-frame graph construction proves heavy in the session, call the
nodes directly and fire `stage_patches_hook` manually (exactly as `spark_frame.py` does today),
and leave a note to move to the Runner later. Lean Runner; don't let the fallback become the
default silently.

### Reuse, don't duplicate

`author_plan.py` (PLAN) and `spark_frame.py` (per-frame) are the prototype internals. Extract
their shared logic — the smoke/stub guards, the Maya drive, reference resolution, the Flo/T1/Em
fan, approve/reject — into functions `pipeline/run.py` imports (an `pipeline/orchestration/`
helper module is fine). Leave the two scripts working (they're the documented prototype and a
useful manual escape hatch); don't fork their logic.

---

## How each seam is absorbed

| # | Seam | This build |
|---|------|-----------|
| 1 | `author_plan.py` missing | Its logic becomes the PLAN stage (extracted, not duplicated) |
| 4 | Nested-SDK throttle | Runs standalone from a plain shell — the whole point of the validation step |
| 6 | Em has no CLI | Driven inside the GENERATE fan |
| 7 | Patch staging needs the `post_run` hook | Dissolved — the per-frame fan runs through the Runner |
| 8 | `ctx.criteria` bundle + `brief_file` auto-wire | Wired once at `--approve-plan` via `load_all_criteria` + `brief.active_dir` |
| 9 | Em single-character, IR-namespace-keyed | Two Em passes on the `shots.yaml` cast namespaces |
| 11 | `character_id` dual meaning | `state.cast` threads folder key (Flo) + IR namespace (Em) |
| 15 | Bash CWD unreliable | One process, absolute run paths in state |
| 16 | Whole chain + per-frame gate hand-wired | **This is the orchestrator** |

Already landed: #2, #3 (#47); #5, #12, #13 (#49, Slice 1). Out: #10 (eval-gated, ticketed);
#14 (Slice 3, ticketed).

---

## Build approach — $0 first, costed validation second

**The build session is $0 / stub-green / TDD.** Every node has a stub fallback (Maya's Opus
text stub, Flo's placeholder PNG, Em's stub verdict), so the state machine + CLI + gates + the
per-frame fan all exercise with faked transports. No model spend in the build.

Suggested internal phases for the single session, each red→green:

- **P0 — state model.** `run_state.json` read/write/resume + stage transitions + `--status`.
- **P1 — PLAN stage.** Drive Maya (stub), emit artifacts, draft the gate, exit; `--approve-plan`
  locks criteria + wires the bundle.
- **P2 — GENERATE loop.** The per-frame fan through the Runner (stub transports), the eye gate,
  `--approve-frame` chaining, `--retry-frame --note` re-roll, cast/namespace threading.
- **P3 — ASSEMBLE tail.** Write `sequence.txt` from state, drive the generalized assembler
  (fake-ffmpeg shim, as Slice 1's golden test does), produce the loop paths, `stage=DONE`.
- **P4 — integration smoke.** A full `brief → loop` stub-green run that auto-approves each gate
  in-test, asserting the state transitions, the resume round-trip (write state, re-instantiate,
  continue), and that the loop outputs exist. Plus a durability test: interrupt mid-GENERATE,
  re-invoke, state intact.

**Then, out of session (the proof):** a costed end-to-end validation — run the real
orchestrator **from a plain terminal** (NOT inside a Claude Code session — the nested-SDK
constraint, seam #4) on a small piece: re-run "The Spark, Shared" via the one-command flow, or
a fresh tiny 2-frame piece. Validates Maya-live + Flo + Em + assemble for real (~$0.66-ish,
subscription-absorbed Opus). Reported back; Cowork verifies against the tree. This is a
separate step after the build session, under fleet-ops §0.

---

## Test plan

- State machine: read/write/resume, every stage transition, `--status` render.
- PLAN: stub Maya → drafted; `--approve-plan` → criteria locked + bundle wired + frame 1 generated.
- GENERATE: `--approve-frame` chains N+1 with the right references; `--retry-frame --note`
  re-rolls (new attempt, prompt carries the note); two-cast frame runs two Em passes on the
  namespaces; one-cast frame runs one.
- ASSEMBLE: `sequence.txt` written from state; assembler invoked with `--slug`/`--sequence-file`
  (fake-ffmpeg); loop outputs present; `stage=DONE`.
- Integration: full stub-green `brief → loop`; resume durability (interrupt + continue).
- Regression: Slice 1's golden PT_A1 assemble test stays green; the per-frame normalize still fires.

## Fleet-ops + guards

- **Build is $0** (stub-green) but the worktree discipline holds: one isolated worktree off
  `origin/main`, single owner, `ANTHROPIC_API_KEY` absent, divergence `0 0` before. (The
  2026-06-10 path-leak happened on a $0 session — the discipline isn't about spend.)
- **Em baseline untouched:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md`
  == `2af75906502f1caf8857e18828ceb2e4`. Nothing here reaches `evals/vision_critic/`.
- **State of record:** CHANGELOG entry (decision-log voice). CLAUDE.md gets a real update — a
  new top-level command (`python -m pipeline.run`) belongs in Key Commands + the orchestrator
  earns a line in the architecture/skills framing.
- TDD red→green; the costed validation is its own §0-gated, out-of-session step.

## Open design points (resolve in-build, against the tree)

- **`shots.yaml` schema** — propose above; confirm exact keys by externalizing `spark_frame.py`'s `FRAMES`.
- **Holds policy** — default on-twos (`hold: 2`) vs per-shot from `shots.yaml` (the schema carries `hold`; default 2 when absent).
- **Per-frame fan** — Runner (recommended, dissolves #7) vs direct-call fallback; lean Runner.
- **Cast/namespace discovery** — derive from each Bible's criteria id prefix vs declare in `shots.yaml`; recommend derive + let `shots.yaml` name per-frame presence.
- **The eye round-trip** — standalone prints candidate path + Em verdict + exits; Sean opens the image, re-invokes. Optional `--open` to auto-open via macOS `open` (nice-to-have, note it).
