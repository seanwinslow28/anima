# Phase 3 Build Plan — Sam first (the scriptwriter), Bea scoped behind it

*Dated 2026-06-12. Companion to the [Sam + Bea brainstorm](2026-06-12-sam-bea-phase3-brainstorm.md) and the paste-ready [Sam kickoff](2026-06-12-sam-scriptwriter-kickoff.md). The four forks are locked in the brainstorm §6; this plan turns the Sam half into a buildable, TDD, $0 stub-green slice and scopes Bea for the follow-on kickoff.*

> **⚠ Updated 2026-06-15 — read [`2026-06-15-screenwriting-modes-integration-addendum.md`](2026-06-15-screenwriting-modes-integration-addendum.md) before building.** Sam's persona preamble now loads the **full vendored voice instrument** `sean-screenwriting-voice.md` (ready at [`2026-06-15-sam-bea-screenwriting-voice-context.md`](2026-06-15-sam-bea-screenwriting-voice-context.md)) — NOT the "condensed Sean's register note" this plan's file map describes. The eval-scaffold step also gains a few ships-red anti-pattern cases. Contract, single-call design, sequencing, and the $0/TDD discipline are unchanged.

---

## Scope boundary (read first)

This build adds **Sam only**, as a standalone AgentSpec node + CLI + driver + eval scaffold — exactly the way Cy's `author_bible.py` is standalone from the run orchestrator. It does **not** wire Phase 3 into `pipeline/run.py`. The orchestrator wiring (a new `STORYBOARD` stage between `PLAN` and `GENERATE`, with a draft-shots.yaml→curate→lock gate) is a deliberate follow-on that depends on *both* Sam and Bea existing — it lands after Bea, as its own slice. Building Sam standalone keeps this slice lean, stub-green, and mergeable on its own.

The build is **$0 at build time**: stub fallback keeps the whole node CI-green credential-free, like every agent before it. The costed validation (real Opus authoring a real script) is **deferred** alongside the already-parked end-to-end run — it is not part of this slice.

**Verdict-baseline guard:** this slice must not touch `evals/vision_critic/`. `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` stays `2af75906502f1caf8857e18828ceb2e4` before and after.

---

## What Sam is, in contract terms

| Field | Value |
|-------|-------|
| Persona | Sam |
| Node id | `scriptwriter` (role-named, matching `planner`/`character_designer`/`vision_critic`/`museum_writer`) |
| Phase | 3a — Storyboard (script half) |
| Model | Opus 4.8, subscription-absorbed (`ANTHROPIC_API_KEY` absent → bills the Pro plan) |
| Inputs | `{brief_dir: str}` — reads `00_studio_brief.md` (required) + `plan.md` (if present) + manifest `characters:` registry for cast |
| Outputs | `{script_path: str, beats_path: str}` |
| `cites_criteria` | `[]` (Sam authors story, doesn't cite IR rules) |
| `cost_estimate` | `usd=0.0, latency_s≈120, confidence=0.85` — single Opus authoring call, subscription-absorbed |
| Failure modes (eval handbook) | surface pastiche vs real stylistic-mechanism modeling; beat/structure failures; voice drift |
| v1 second pass | **deterministic structural validation**, not an LLM aesthetic judge (handbook: LLM judges are weak/self-preferring on creative quality) |

Sam mirrors `planner.py`'s shape but is **single-call**: one Opus authoring pass that emits `script.md` + `beats.json`, followed by a free, deterministic structural-validation pass (beat coverage, arc presence, cast consistency, sane count). No second LLM call in v1 — the taste call is the human gate.

---

## The Sam → Bea contract: `beats.py`

The load-bearing new artifact. Mirror `pipeline/orchestration/shots.py` precisely — same module shape, same strict validator philosophy — so the Sam→Bea handoff is a typed dataclass, not loose prose. New file `pipeline/orchestration/beats.py`:

```python
@dataclass(frozen=True)
class Beat:
    id: int                       # strictly ascending — story order (mirrors Shot.id)
    title: str                    # short beat name ("The Spark")
    intent: str                   # what the beat does in the story
    emotional_beat: str           # the felt state ("calm focus → first stir")
    cast: list[str]               # ⊆ manifest IR namespaces; flows to shots.yaml cast
    feel: str = ""                # timing/pacing note ("establishing — let it breathe")
    notes: str = ""               # continuity / loop notes

@dataclass(frozen=True)
class BeatSheet:
    slug: str
    logline: str
    beats: list[Beat]

def load_beats(path: Path, *, known_namespaces: set[str]) -> BeatSheet: ...
```

`load_beats` enforces: slug matches `[A-Za-z0-9_-]+`; `beats` is a non-empty list; ids are strictly ascending integers ≥ 1; `title`/`intent`/`emotional_beat` non-empty; `cast` non-empty and `⊆ known_namespaces` (same namespace check `load_shots` runs). This is what makes "did Sam produce something Bea can consume" a free deterministic gate — and `cast` carries beat → shot → `shots.yaml` cast unchanged.

---

## File map (Sam slice)

| File | New/edit | Purpose |
|------|----------|---------|
| `pipeline/orchestration/beats.py` | **new** | `Beat`/`BeatSheet`/`load_beats` — the Sam→Bea contract (mirror `shots.py`) |
| `pipeline/agents/scriptwriter.py` | **new** | `@register_node("scriptwriter")` `ScriptwriterNode` — Opus authoring + deterministic structural pass + stub fallback |
| `pipeline/agents/prompts/sean-screenwriting-voice.md` | **new (vendored)** | The full voice instrument, vendored verbatim from `docs/2026-06-15-sam-bea-screenwriting-voice-context.md` (anti-distillation contract + moves table + WHAT/taste layers + §8 verbatim samples). Shared — Bea loads it too. |
| `pipeline/agents/prompts/sam-scriptwriter-context.md` | **new** | Persona preamble; loads `anima-standing-context.md` + `sean-screenwriting-voice.md` (the full vendor, NOT a condensed note — see the 2026-06-15 addendum) |
| `pipeline/cli/script.py` | **new** | `script init / show / approve / mutate` — mirror `plan.py` (`show` renders the beat sheet tear sheet; `approve` locks `beats.json`) |
| `pipeline/cli/__main__.py` | edit | Register the `script` subcommand alongside `plan`/`bible`/`patches` |
| `scripts/author_script.py` | **new** | Driver mirroring `author_plan.py` — `python scripts/author_script.py <brief-dir> --run-dir …` |
| `evals/scriptwriter/` | **new** | `cases.yaml` + fixtures + `runner.py` stub + `README.md`. Seed with the Spark beats as ground-truth reference cases |
| `tests/test_beats.py` | **new** | `load_beats` validation: ascending ids, namespace check, round-trip |
| `tests/test_scriptwriter.py` | **new** | Stub-green node contract: emits `script.md` + valid `beats.json`; structural pass catches a coverage gap; CLI init/show/approve |
| `CHANGELOG.md` | edit | Dated entry: what Sam is, why single-call, the deterministic-pass decision |
| `CLAUDE.md` | edit | Skills Map: add the Sam (`scriptwriter`) row; note Phase 3 is now half-built |

---

## TDD sequence (the order the build runs)

1. **`beats.py` + `tests/test_beats.py` first.** The contract before the agent. Red → green on: valid sheet round-trips; non-ascending ids reject; `cast` with an unknown namespace rejects; empty `intent` rejects. This is pure Python, no model — fast, deterministic, the foundation Bea will later depend on.
2. **`scriptwriter.py` stub path + `tests/test_scriptwriter.py`.** Build the node with its stub fallback first (credential-free). Test: node emits a `script.md` and a `beats.json` that `load_beats` accepts; the deterministic structural pass flags a beat sheet that misses a `plan.md` story point (coverage gap) and passes a complete one.
3. **The Opus authoring path** (guarded by the stub fallback). The real `invoke_opus_text` call with `sam-scriptwriter-context.md` + the studio brief + `plan.md`. Reuse Maya's envelope-parsing hardening (`_parse_json_envelope` tolerating a persona preamble; the `MAYA_CALL_TIMEOUT_S` lesson — Opus authoring runs minutes, not 120s; give Sam its own `SAM_CALL_TIMEOUT_S`, default 1200s). No live call in CI.
4. **CLI + driver.** `script init/show/approve/mutate` + `author_script.py`. `show` renders the beat-sheet tear sheet (clean prose on disk, boxes in the renderer — Maya's rule). `approve` flips `locked: true` on `beats.json`, idempotent.
5. **Eval scaffold.** `evals/scriptwriter/cases.yaml` with a few real hand-labeled cases (the Spark beat sheet is ready-made ground truth: plan.md → expected beats). A `runner.py` stub parameterized over cases, in the CI-green mocked mode. The pairwise-preference harness is **not** built here — it's a campaign item.
6. **Docs.** CHANGELOG entry + CLAUDE.md Skills Map row. Re-assert the md5 guard.

---

## Acceptance criteria (all must hold)

- `python -m pytest tests/test_beats.py tests/test_scriptwriter.py` — **green, credential-free.**
- `python -m pytest tests/` — full suite stays green (576 + new, 0 regressions).
- `python -m pipeline.cli script init --target <brief>` scaffolds; `script show` renders the beat sheet; `script approve` locks `beats.json` idempotently.
- A stub-authored `beats.json` round-trips through `pipeline/orchestration/beats.py:load_beats` with the manifest's known namespaces — the Sam→Bea contract is proven by test.
- The deterministic structural pass catches at least one real failure class (a beat-coverage gap against `plan.md`) — proven by test, not asserted.
- `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` == `2af75906502f1caf8857e18828ceb2e4`. No file under `evals/vision_critic/` changed.
- CHANGELOG.md + CLAUDE.md updated. No box-drawing characters written into `script.md` output (Maya's rule — renderer owns boxes).
- Lands as a single squash PR off an isolated worktree from `origin/main`, per fleet-ops.

---

## Bea — scoped for the follow-on kickoff (built after Sam merges)

Captured here so the Sam→Bea contract is designed with Bea's needs in view; **not built in this slice.**

| Field | Value |
|-------|-------|
| Persona / node id | Bea / `storyboard_artist` |
| Phase | 3b — Storyboard (board half) |
| Model | Sonnet 4.6, subscription-absorbed. Lowest-confidence assignment (65%) → bake-off candidate (deferred) |
| Inputs | `{brief_dir: str, beats_path: str}` — Sam's approved `beats.json` + `plan.md` + Bible refs |
| Outputs | `{storyboard_path: str, shots_path: str}` — `storyboard.md` (human-readable) + **draft `shots.yaml`** (unlocked) |
| The free deterministic gate | Validate the draft `shots.yaml` through the real `pipeline/orchestration/shots.py:load_shots` with the manifest's known namespaces — coverage + parse + chain integrity, zero cost |
| Re-roll | One attempt on validation failure, error threaded back into the prompt (Cy's reject-reason pattern) |
| Hard part | The per-shot `prompt` field (the Flo generation prompt in pencil-test register) — seed Bea with the register clause exemplars + the Spark prompts as few-shot; headline metric is **revision count** |
| Deferred | Sonnet/Gemini/Codex bake-off; draft silhouette panels; pro composition panels; camera-move vocabulary — all per brainstorm §8 |

**Bea's file map** mirrors Sam's: `pipeline/agents/storyboard_artist.py`, `prompts/bea-storyboard-context.md`, `pipeline/cli/storyboard.py`, `scripts/author_storyboard.py`, `evals/storyboard_artist/`, `tests/test_storyboard_artist.py`. Its `storyboard approve` is the **curation gate** where Sean's edited `shots.yaml` becomes the run input.

**Then (after both):** the orchestrator wiring slice — a `STORYBOARD` stage in `pipeline/run.py` between `PLAN` and `GENERATE`, exiting at a `--approve-storyboard` gate, turning the standalone Sam→Bea chain into part of the one resumable program. That's where the loop literally closes inside `python -m pipeline.run`.

---

## Why this sequencing is right

Sam is the lower-risk, higher-certainty build (text-only, Opus, closest clone of Maya), and his output *is* Bea's input. Landing Sam first lets the `beats.py` contract harden against a real authored beat sheet before Bea is built to consume it — so Bea is built against a proven contract, not a hypothetical one. It also keeps each PR small and independently mergeable, which is the discipline that got Slices 1/2/2.1 in clean. The fleet gets completed in two lean slices plus a wiring slice, not one big risky one.
