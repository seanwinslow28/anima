# Phase 3 Build Plan — Bea (the storyboard artist), the fleet's last agent

*Dated 2026-06-15. Companion to the [Sam + Bea brainstorm](2026-06-12-sam-bea-phase3-brainstorm.md), the [voice-integration addendum](2026-06-15-screenwriting-modes-integration-addendum.md), and the paste-ready [Bea kickoff](2026-06-15-bea-storyboard-kickoff.md). Sam shipped in #52/#53; this plan turns the Bea half into a buildable, TDD, $0 stub-green slice. Bea is the **last named agent** — landing her completes the canonical roster (Maya / Cy / Em / Mo / Flo / Sam / Bea / T3 / orchestrator).*

---

## Scope boundary (read first)

This build adds **Bea only**, as a standalone AgentSpec node + CLI + driver + eval scaffold — exactly the way Sam (#52) and Cy's `author_bible.py` are standalone from the run orchestrator. It does **not** wire Phase 3 into `pipeline/run.py`. The orchestrator wiring — a `STORYBOARD` stage between `PLAN` and `GENERATE` that enforces the shots.yaml `locked` flag and exits at a `--approve-storyboard` gate — is the deliberate **third slice**, planned after Bea lands. Building Bea standalone keeps this slice lean, stub-green, and mergeable on its own; the loop closes manually (Sam → Bea → human-curate → `python -m pipeline.run`) until the wiring slice.

The build is **$0 at build time**: stub fallback keeps the whole node CI-green credential-free, like Sam and every agent before. The costed validation (real Sonnet authoring a real storyboard) is **deferred** alongside the parked end-to-end run.

**Two standing guards:**

- **Em verdict-baseline:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` stays `2af75906502f1caf8857e18828ceb2e4`. Nothing in this slice reaches `evals/vision_critic/`.
- **Sam's voice file stays byte-stable:** `pipeline/agents/prompts/sean-screenwriting-voice.md` is md5-pinned for Sam. Bea's prose-action exemplars go in **`bea-storyboard-context.md`**, NOT in the shared file. The shared file is loaded by both, unchanged.

---

## Decisions locked 2026-06-15 (the convergence record)

The four 2026-06-12 forks (draft `shots.yaml` + `storyboard.md`, text-only v1, scaffold-eval-now) still hold. These four are the Bea-specific calls made this session:

| # | Fork | Decision | Why |
|---|------|----------|-----|
| 1 | Coverage gate | **Add optional `beat_id` to `shots.yaml`** | Gives every shot a machine link back to its source beat, so "shot-coverage gap" and "script↔board conflict" (Bea's two named failure modes) become *deterministic* free gates — the Bea-equivalent of Sam's cast-coverage. Back-compat: the field is optional; the shipped Spark `shots.yaml` has none and parses unchanged; `generate_stage.py` never reads it. |
| 2 | Model path | **Sonnet single-call + deterministic gate; escalation deferred** | Mirror Sam exactly (one authoring call → free deterministic validation). The Opus-escalation-on-conflict idea is real but needs an LLM conflict-judge (not deterministic), which the eval handbook is wary of for creative calls. Deferred to the campaign with the bake-off. |
| 3 | Build scope | **Bea standalone; orchestrator wiring is a separate follow-on** | Keeps each PR small and independently mergeable (the discipline that landed Slices 1/2/2.1 and Sam clean). The `STORYBOARD`-stage wiring is the third slice. |
| 4 | Voice gap | **Fold the action-line bank into `bea-storyboard-context.md` now** | Bea's hardest output (the per-shot prose-action `prompt`) needs prose-action few-shot, not Sam's dialogue samples. The bank is vendored and ready at [`2026-06-15-bea-action-line-bank-context.md`](2026-06-15-bea-action-line-bank-context.md). Goes in Bea's own context file to keep the shared voice file md5-stable. |

---

## What Bea is, in contract terms

| Field | Value |
|-------|-------|
| Persona | Bea |
| Node id | `storyboard_artist` (role-named, matching `planner`/`character_designer`/`scriptwriter`/`vision_critic`/`museum_writer`) |
| Phase | 3b — Storyboard (board half) |
| Model | Sonnet 4.6, subscription-absorbed. Single authoring call. (Lowest-confidence roster assignment, 65% → the three-way bake-off is a *deferred* campaign item, not a v1 blocker.) |
| Inputs | `{brief_dir: str}` — reads `00_studio_brief.md` (required) + `beats.json` (Sam's approved beat sheet, required) + `plan.md` (if present) + manifest `characters:` registry for cast namespaces + Bible references |
| Outputs | `{storyboard_path: str, shots_path: str}` — `storyboard.md` (human-readable) + `shots.yaml` (draft, unlocked) |
| `cites_criteria` | `[]` |
| `cost_estimate` | `usd=0.0, latency_s≈120, confidence=0.85` — single Sonnet call, subscription-absorbed |
| Failure modes (eval handbook) | script↔board conflict; shot-coverage gaps; composition errors |
| v1 second pass | **deterministic coverage + conflict validation**, not an LLM judge (the taste/composition call is the human gate; the bake-off is deferred) |

Bea mirrors `scriptwriter.py`'s shape precisely: one Sonnet authoring pass emitting both artifacts, then a free deterministic validation pass. On validation failure, **one re-roll** with the error threaded back into the prompt (Cy's reject-reason pattern). No second LLM judge in v1.

---

## The two `shots.yaml` schema additions (the load-bearing new code)

Both additions to `pipeline/orchestration/shots.py` are **optional and back-compat** — the shipped Spark `shots.yaml` (no `beat_id`, no `locked`) must keep parsing and `test_spark_shots_equivalence.py` + `test_run_shots.py` must stay green.

1. **`beat_id` (per-frame, optional `int | None = None`).** Add `"beat_id"` to `_FRAME_KEYS`; add `beat_id: int | None = None` to the `Shot` dataclass; in `load_shots`, if present, validate it's an int ≥ 1. Carries the beat→shot link. `generate_stage.py` ignores it (it reads only `cast`/`extra_references`/`chain_anchors`/`prompt`/`beat`/`hold` — verified), so downstream is untouched.

2. **`locked` (top-level, optional `bool`, default absent/false).** Add `"locked"` to `_TOP_KEYS`. Mirrors `beats.json`'s `locked`. `storyboard approve` flips it true; `show`/`approve` respect it (idempotent "already locked" no-op). It is **read by Bea's own CLI** (so it's not a dead flag), and the orchestrator-wiring slice will later *enforce* it as the gate. The Spark `shots.yaml` (no `locked`) is treated as unlocked and still runs, because nothing enforces it until the wiring slice.

---

## The Sam → Bea seam, made concrete: the Loaded Object

Per the voice addendum, the handoff is not vague "collaboration." Sam writes a **loaded object** into a beat's `intent`/`notes`; **Bea boards that object as the shot.** This is the design contract for how a beat becomes a shot, and it's why Bea loads the same voice instrument plus the action-line bank: the prose-action exemplars (bank items 7, 29, 12) show how a loaded-object shot should *read* in the `prompt` field. It also names the future escalation trigger (deferred): a beat whose emotional payload rides on an object Bea can't realize as a fixed-camera shot is a script↔board conflict worth escalating — but in v1 that's a human-gate call, not an LLM judge.

---

## Bea's deterministic validation pass

`storyboard_validate(beat_sheet, shot_list, *, known_namespaces)` — the Bea-equivalent of Sam's `structural_validate`. `load_shots` has already enforced the schema (ascending ids, `cast ⊆ known_namespaces`, `chain_anchors ⊆ cast`, non-empty beat/prompt, `hold ≥ 1`). This layer adds:

- **Coverage:** every beat in `beats.json` has ≥1 shot whose `beat_id == beat.id`. A beat with no shot raises (the deterministic shot-coverage-gap class).
- **No orphan shots:** every shot's `beat_id` (when set) exists in the beat sheet.
- **Cast consistency (the script↔board conflict check):** each shot's `cast ⊆` its source beat's `cast`. A shot can't introduce a character the beat didn't carry.

Raises `ValueError` on any failure → one re-roll with the message threaded into the prompt. Free, no LLM, mirrors Sam.

---

## File map (Bea slice)

| File | New/edit | Purpose |
|------|----------|---------|
| `pipeline/orchestration/shots.py` | **edit** | Add optional `beat_id` (per-frame) + `locked` (top-level), both back-compat. Update the dataclass + `load_shots` + `_FRAME_KEYS`/`_TOP_KEYS` |
| `pipeline/agents/storyboard_artist.py` | **new** | `@register_node("storyboard_artist")` `StoryboardArtistNode` — Sonnet authoring + deterministic coverage/conflict pass + stub fallback. Mirrors `scriptwriter.py` |
| `pipeline/agents/prompts/bea-storyboard-context.md` | **new** | Persona preamble; loads `anima-standing-context.md` + shared `sean-screenwriting-voice.md`; carries Bea's "how this maps to your job" slice + the **action-line bank** (vendored from `2026-06-15-bea-action-line-bank-context.md`) + the pencil-test register clause block |
| `pipeline/agents/sdk_runners.py` | **edit** | Add optional `stub_fn=` param to `invoke_sonnet_text` (mirror exactly the #52 change to `invoke_opus_text`; defaults to `_stub_sonnet_text` so Maya's adversarial pass is byte-unchanged) |
| `pipeline/cli/storyboard.py` | **new** | `storyboard init / show / approve / mutate` — mirror `script.py`. `show` renders the shot list + beat→shot coverage tear sheet; `approve` is the **curation gate** (validate the curated `shots.yaml` → flip `locked: true`); `mutate` audited → `storyboard_audit.jsonl` |
| `pipeline/cli/__main__.py` | edit | Register the `storyboard` subcommand next to `plan`/`bible`/`patches`/`script` |
| `scripts/author_storyboard.py` | **new** | Driver mirroring `author_script.py` — `python scripts/author_storyboard.py <brief-dir> --run-dir … --manifest …` (live-Sonnet smoke + stub-marker guard) |
| `evals/storyboard_artist/` | **new** | `cases.yaml` + fixtures + `runner.py` stub + `README.md`. Seed with the Spark `beats.json` → expected Spark `shots.yaml` (positive round-trip) + ships-red anti-patterns (coverage gap, orphan shot, off-beat cast) |
| `tests/test_shots.py` | **new/edit** | The `beat_id` + `locked` additions: present-and-valid round-trips; absent stays back-compat; bad `beat_id` rejects |
| `tests/test_storyboard_artist.py` | **new** | Stub-green node contract: emits `storyboard.md` + valid draft `shots.yaml`; coverage pass catches a beat-with-no-shot; cast-consistency catches a script↔board conflict |
| `tests/test_storyboard_cli.py` | **new** | `storyboard init/show/approve/mutate` |
| `CHANGELOG.md` | edit | Dated entry: Bea built; the two schema additions; the deterministic coverage/conflict design; **the fleet roster is now complete** |
| `CLAUDE.md` | edit | Skills Map: add the Bea (`storyboard_artist`) row; mark Phase 3 built (script + board); note the only Phase-3 remainder is the orchestrator-wiring slice |

---

## TDD sequence (the order the build runs)

1. **`shots.py` schema additions + `tests/test_shots.py` first.** The contract before the agent. Red → green on: a frame with `beat_id` round-trips; a top-level `locked` round-trips; the existing Spark `shots.yaml` (neither field) still parses; a non-int `beat_id` rejects. Then run `test_run_shots.py` + `test_spark_shots_equivalence.py` to **prove back-compat green** before touching anything else.
2. **`invoke_sonnet_text` `stub_fn=` param + a focused test.** Backward-compatible; Maya's pass byte-unchanged. (Mirror the #52 `invoke_opus_text` change — verify the diff shape against that commit.)
3. **`storyboard_artist.py` stub path + `tests/test_storyboard_artist.py`.** Build the node with its stub fallback first. The stub emits a Spark-shaped `storyboard.md` + draft `shots.yaml` (beat_id-linked, IR-namespace cast) with the `STUB FALLBACK` marker. Test: the draft `shots.yaml` round-trips through `load_shots` with the manifest namespaces; `storyboard_validate` **catches a coverage gap** (a beat with no shot) and **catches a cast conflict** (a shot with an off-beat character), and passes a clean sheet.
4. **The Sonnet authoring path** (guarded by the stub). Real `invoke_sonnet_text` with `bea-storyboard-context.md` + the shared voice file + `beats.json` + the studio brief. Reuse Maya/Sam's `_parse_json_envelope` hardening and a `BEA_CALL_TIMEOUT_S` (default 1200s — the same Opus/Sonnet authoring-latency lesson). No live call in CI.
5. **CLI + driver.** `storyboard init/show/approve/mutate` + `author_storyboard.py`. `show` renders the tear sheet (clean prose on disk, box-drawing only in the renderer — Maya's rule). `approve` validates the curated `shots.yaml` against `load_shots` + `storyboard_validate`, then flips `locked: true` idempotently — the curation gate.
6. **Eval scaffold.** `evals/storyboard_artist/cases.yaml` — the Spark `beats.json` → expected `shots.yaml` as positive ground truth, plus a few ships-red anti-pattern cases (coverage gap / orphan shot / off-beat cast). `runner.py` is the CI-green mocked mode (mirror `evals/scriptwriter/runner.py`). **Do not** build the bake-off — campaign item.
7. **Docs.** CHANGELOG entry + CLAUDE.md Skills Map row + the "fleet complete" note. Re-assert both md5 guards (Em baseline + Sam's voice file).

---

## Acceptance criteria (all must hold)

- `python -m pytest tests/test_shots.py tests/test_storyboard_artist.py tests/test_storyboard_cli.py` — **green, credential-free.**
- `python -m pytest tests/` — full suite green (605 + new, 0 regressions). **`test_run_shots.py` + `test_spark_shots_equivalence.py` green proves the schema additions are back-compat.**
- `python -m pipeline.cli storyboard init/show/approve` works against a brief dir carrying a `beats.json`; a stub-authored draft `shots.yaml` round-trips through `load_shots` and passes `storyboard_validate`.
- The coverage gate catches a beat-with-no-shot **and** the cast-consistency check catches a script↔board conflict — both proven by test, not asserted.
- `invoke_sonnet_text`'s `stub_fn=` addition is backward-compatible — Maya's adversarial pass unchanged (proven by the existing planner tests staying green).
- `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` == `2af75906502f1caf8857e18828ceb2e4`; nothing under `evals/vision_critic/` changed.
- `pipeline/agents/prompts/sean-screenwriting-voice.md` md5 **unchanged** (the action-line bank went into `bea-storyboard-context.md`, not the shared file).
- No box-drawing characters in `storyboard.md` / `shots.yaml` output. CHANGELOG.md + CLAUDE.md updated, including the **fleet-roster-complete** note.
- Lands as a single squash PR off an isolated worktree from `origin/main`, per fleet-ops. Clean teardown.

---

## The follow-on (the third slice, after Bea) — orchestrator wiring

Once Bea merges, the loop closes *inside* `python -m pipeline.run`: a new `STORYBOARD` stage between `PLAN` and `GENERATE` that runs Sam → Bea, exits at a `--approve-storyboard` human-curation gate, and enforces the `shots.yaml` `locked` flag before `GENERATE` will consume it. That slice turns the standalone Sam→Bea→curate chain into part of the one resumable program — and it's the moment the orchestrator stops needing a hand-written `shots.yaml`. Planned in Cowork after Bea lands and the beat_id-linked `shots.yaml` is proven against a real Bea draft.

## Why this completes the fleet

Bea is the ninth and last named agent. After her, every node of `Maya → Sam → Bea → shots.yaml → Flo/orchestrator → Em/T3 → Mo` has an agent, and the human still owns the only nodes that matter: the `script approve`, `storyboard approve` curation gates, and the final ship call. The hardening campaign (every agent's full eval + Bea's bake-off) and the costed end-to-end run stay parked — but the *design* of the fleet is complete the moment Bea is green.
