# Kickoff — Bea the Storyboard Artist, Phase 3b ($0 stub-green, TDD) — the fleet's last agent

*Paste the block below into a fresh Claude Code session in the `anima` repo. Self-contained.
Plan of record: [`docs/2026-06-15-bea-storyboard-build-plan.md`](2026-06-15-bea-storyboard-build-plan.md).
Build input (vendor it): [`docs/2026-06-15-bea-action-line-bank-context.md`](../../design/2026-06-15-bea-action-line-bank-context.md).
Context: the [Sam+Bea brainstorm](../sam/2026-06-12-sam-bea-phase3-brainstorm.md) + the [voice addendum](../sam/2026-06-15-screenwriting-modes-integration-addendum.md).*

---

You're building **Bea**, the Phase-3b storyboard artist — the **last named agent** in the fleet.
She reads Sam's approved `beats.json` + the Studio Brief and *proposes* two artifacts: a studio-voice
`storyboard.md` and a **draft `shots.yaml`** (the orchestrator's machine input). Both are proposals;
the `shots.yaml` is born unlocked and never auto-runs — Sean curates it through the `storyboard approve`
gate. Text-only v1 (no generated panels). Bea **proposes, the human decides** — Phase 3 is
human-authored ("agents assist; they don't pick beats"). Read first, in order:
[`docs/2026-06-15-bea-storyboard-build-plan.md`](docs/2026-06-15-bea-storyboard-build-plan.md) (the spec),
`PHILOSOPHY.md`, `CLAUDE.md`, `docs/pipeline-architecture-v1.md` §Phase 3. The code you're cloning:
`pipeline/agents/scriptwriter.py` (Sam — the exact AgentSpec shape to mirror, incl. the single-call +
deterministic-pass design and the stub), `pipeline/orchestration/shots.py` (the file you extend +
the validator Bea's gate reuses), `pipeline/orchestration/beats.py` (Sam→Bea contract Bea reads),
`pipeline/cli/script.py` (the CLI shape), `scripts/author_script.py` (the driver shape).

**What you build (Bea slice, standalone):** the two back-compat `shots.yaml` schema additions
(`beat_id`, `locked`); the `storyboard_artist` node; its persona preamble (folding in the vendored
action-line bank); a `stub_fn=` param on `invoke_sonnet_text`; the `storyboard` CLI; the
`author_storyboard.py` driver; the `evals/storyboard_artist/` scaffold; tests; docs.

**Out of scope:** wiring Phase 3 into `pipeline/run.py` (the `STORYBOARD` stage — a separate third
slice after Bea); the Sonnet/Gemini/Codex bake-off (the parked hardening campaign); any live/costed
Sonnet call (deferred). Don't touch `evals/vision_critic/`.

## Doctrine — non-negotiable

- **Verify against the tree, never trust a label — including this kickoff and the plan.**
  Re-confirm before building: that `scriptwriter.py`'s single-call + `structural_validate` +
  `_stub_*` + `_parse_json_envelope`-reuse shape is what you're cloning; that `shots.py:load_shots`'s
  `_FRAME_KEYS`/`_TOP_KEYS` are where `beat_id`/`locked` slot in; that `generate_stage.py` reads only
  `cast`/`extra_references`/`chain_anchors`/`prompt`/`beat`/`hold` from a `Shot` (so `beat_id` is
  inert downstream — confirm); that `known_namespaces` is derived via `derive_cast(ctx.manifest)` →
  `ir_namespace` (Sam's settled seam — `scriptwriter.py:88`; Bea uses the **identical** derivation);
  that `invoke_sonnet_text` currently hardcodes `stub_fn=_stub_sonnet_text` and needs the optional
  param added the way #52 added it to `invoke_opus_text`. Cautionary tales: Sam's own field note —
  the cast vocabulary *looked* like the folder key and was the IR namespace; a docstring once lied
  about `agy -m`; `--stub` once silently spent real money.
- **Two md5 guards, both must hold:**
  - Em verdict-baseline: `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md`
    == `2af75906502f1caf8857e18828ceb2e4`. Nothing here reaches `evals/vision_critic/`.
  - **Sam's voice file stays byte-stable:** `pipeline/agents/prompts/sean-screenwriting-voice.md`
    is md5-pinned for Sam. The action-line bank goes in **`bea-storyboard-context.md`**, NOT the
    shared file. Capture the shared file's md5 at §0 and re-check it at the end — it must not move.
- **Back-compat is a hard gate.** The `shots.yaml` additions are optional. `test_run_shots.py` and
  `test_spark_shots_equivalence.py` must stay green — that's the proof the shipped Spark `shots.yaml`
  (no `beat_id`, no `locked`) still parses and the orchestrator is unaffected.
- **$0 — stub-green only.** No model spend. The headline deliverable is Bea's whole contract layer +
  CLI + driver proving end-to-end with **no key**, via the stub fallback. The real Sonnet path is
  written and guarded, never invoked in CI.
- **TDD red→green.** Schema first, then the runner param, then the node (stub path first), then CLI/
  driver, then eval, then docs. Small, revertible commits.

## §0 — fleet-ops gates (before any edit)

```bash
cd <anima main checkout>
git fetch origin
git log --oneline -1 origin/main                        # expect 807cf99 (#53) or newer
git rev-list --left-right --count origin/main...HEAD    # expect 0 0
md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md  # 2af75906502f1caf8857e18828ceb2e4
md5sum pipeline/agents/prompts/sean-screenwriting-voice.md               # capture — must NOT move by the end
echo "${ANTHROPIC_API_KEY:-ABSENT}"                     # expect ABSENT (Sonnet bills the subscription if ever run)
python -m pytest tests/ -q                              # expect green (605+); note any pre-existing .env-key artifacts
```

One isolated worktree off `origin/main`; ALL edits inside it. Single owner.

## Build order (TDD)

1. **`shots.py` additions + `tests/test_shots.py` (schema first).** Add optional `beat_id`
   (per-frame `int | None = None`, into `_FRAME_KEYS` + the `Shot` dataclass; validate int ≥ 1 when
   present) and optional `locked` (top-level `bool`, into `_TOP_KEYS`). Red→green: a frame with
   `beat_id` round-trips; top-level `locked` round-trips; bad `beat_id` rejects. **Then run
   `tests/test_run_shots.py tests/test_spark_shots_equivalence.py` and confirm green** — the
   back-compat proof.

2. **`invoke_sonnet_text` `stub_fn=` param + a focused test.** Add the optional param exactly as #52
   added it to `invoke_opus_text` (default `_stub_sonnet_text` → Maya's pass byte-unchanged). Confirm
   the existing `test_planner.py` Sonnet-pass tests stay green.

3. **`pipeline/agents/storyboard_artist.py` stub path + `tests/test_storyboard_artist.py`.**
   `@register_node("storyboard_artist")` `StoryboardArtistNode`, `inputs={"brief_dir": str}`,
   `outputs={"storyboard_path": str, "shots_path": str}`, `cites_criteria=[]`,
   `cost_estimate → usd=0.0, latency_s≈120, confidence=0.85`. `run()` reads `00_studio_brief.md`
   (required) + `beats.json` (required, via `load_beats`) + `plan.md` (if present); derives
   `known_namespaces` via `derive_cast` (identical to Sam). Single Sonnet authoring pass (stub-backed)
   emitting `storyboard.md` + draft `shots.yaml`, then `storyboard_validate(beats, shots, known_namespaces)`:
   parse `shots.yaml` via `load_shots`; every beat has ≥1 shot with `beat_id==beat.id` (coverage);
   no orphan shots; each shot's `cast ⊆` its source beat's cast (the script↔board conflict check).
   One re-roll with the error threaded back on failure. Build the **stub first** (credential-free):
   `_stub_bea_*` emits a Spark-shaped, beat_id-linked draft with the `STUB FALLBACK` marker. Tests:
   draft round-trips through `load_shots`; the pass **catches a coverage gap** and **catches an
   off-beat-cast conflict**, and passes a clean sheet.

4. **The Sonnet authoring path** (guarded by the stub). Real `invoke_sonnet_text` with
   `bea-storyboard-context.md` + the shared `sean-screenwriting-voice.md` + `beats.json` + the studio
   brief. Reuse `_parse_json_envelope`; `BEA_CALL_TIMEOUT_S` default 1200s. The per-shot `prompt`
   ends in the pencil-test register clause block (match the Spark `shots.yaml` prompts). No live call
   in CI.

5. **`bea-storyboard-context.md`.** Loads `anima-standing-context.md` + the shared voice file. Carries
   Bea's "how this maps to your job" slice (visual moves: Room-as-Biography / Loaded Object / Haptic
   Visuality / Metaphor-Compression) **and the vendored action-line bank** (verbatim from
   `docs/2026-06-15-bea-action-line-bank-context.md` §"Action-Line Prose Bank") + the pencil-test
   register clause block. Do **not** put the bank in the shared voice file.

6. **CLI + driver.** `pipeline/cli/storyboard.py` — `storyboard init/show/approve/mutate`, registered
   in `__main__.py`. `show` renders the shot-list + beat→shot coverage tear sheet (clean prose on
   disk, boxes only in the renderer). `approve` is the **curation gate**: re-validate the curated
   `shots.yaml` (`load_shots` + `storyboard_validate`), then flip `locked: true` idempotently.
   `mutate` audited → `storyboard_audit.jsonl`. `scripts/author_storyboard.py <brief-dir> --run-dir …
   --manifest …` mirrors `author_script.py` (live-Sonnet smoke + stub-marker guard).

7. **Eval scaffold.** `evals/storyboard_artist/` — `cases.yaml` + fixtures + `runner.py` stub +
   `README.md`. Positive ground truth: the Spark `beats.json` → expected Spark `shots.yaml`
   (round-trip + coverage). Ships-red anti-patterns: a coverage gap, an orphan shot, an off-beat-cast
   conflict (mirror Sam's 2-positive + ships-red shape). **No bake-off** — campaign item.

8. **Docs.** CHANGELOG.md dated entry (Bea built; the two schema additions; the deterministic
   coverage/conflict design; **the fleet roster is now complete**). CLAUDE.md Skills Map: add the Bea
   (`storyboard_artist`) row; mark Phase 3 built (script + board), the only remainder being the
   orchestrator-wiring slice. Re-assert both md5 guards.

## Acceptance (all must hold before the PR)

- `python -m pytest tests/test_shots.py tests/test_storyboard_artist.py tests/test_storyboard_cli.py` green credential-free.
- `python -m pytest tests/` green (no regressions); `test_run_shots.py` + `test_spark_shots_equivalence.py` green (back-compat proof).
- `storyboard init/show/approve` works against a brief with a `beats.json`; a stub draft `shots.yaml` round-trips `load_shots` + passes `storyboard_validate`.
- Coverage gate catches a beat-with-no-shot AND cast-consistency catches a script↔board conflict (both proven by test).
- `invoke_sonnet_text` change is backward-compatible (planner tests green).
- Em baseline md5 == `2af75906502f1caf8857e18828ceb2e4`; nothing under `evals/vision_critic/` changed.
- `sean-screenwriting-voice.md` md5 unchanged from §0.
- CHANGELOG.md + CLAUDE.md updated (incl. fleet-complete note). One squash PR off the isolated worktree. Clean teardown.

## When done

Report: the commits, the new test count, full-suite-green-credential-free confirmation, both md5 guards
intact (Em baseline + Sam's voice file), and a one-paragraph field note on any seam that fought you. Then
stop — the fleet's named agents are complete. The next planned step is the **orchestrator-wiring slice**
(the `STORYBOARD` stage in `pipeline/run.py`), planned in Cowork once Bea merges and the beat_id-linked
`shots.yaml` is proven against a real Bea draft.
