# Kickoff — Animatic phase v1: the placement seed (costed spike → $0 stub-green build, TDD)

*Paste the block below into a fresh Claude Code session in the `anima` repo. Self-contained.
Design of record: [`docs/2026-06-18-animatic-phase-design.md`](2026-06-18-animatic-phase-design.md).
Why: [`docs/anima-test-runs/2026-06-18-tier1-validation-run-post-mortem.md`](anima-test-runs/2026-06-18-tier1-validation-run-post-mortem.md) §3–§6 (the L/R, scale, shoulder, leg-count drift) + Sean's diagnosis: "start with my pre-drawn stick figure so NB2 knows exactly where the characters should be."*

---

You're building the **Animatic phase (TOP-1)** — the keystone PHILOSOPHY calls non-negotiable and the one major idea from the original architecture never built. v1 is the **placement seed**: a human-authored rough that pins where characters stand, which way they face, their scale, the shoulder side, the leg count — *before* any frame is drawn — plus the timing (holds) that drives the loop's pacing. Read the design doc for the full rationale and the rejected options; this kickoff is the execution contract.

**The work is in two phases, and the first gates the second.** Step 1 is a **costed spike** that proves the central bet before any plumbing exists. Steps 2–7 are the **$0 stub-green, TDD build** of the stage — and they run **only if Sean rules the spike GO.** A red spike means stop and report, not build.

Read first: the design doc above; the post-mortem §3–§6; the [NB2 editing research](research/2026-05-30-nb2-editing-character-consistency-template.md) (the reference-gap + attribute-bleed failure modes and their clauses); then `PHILOSOPHY.md`, `ROADMAP.md`, `CLAUDE.md`.

The code you'll touch in the build (verify each against the tree first): `pipeline/orchestration/state.py` (the `STAGES` tuple + `_LEGAL_TRANSITIONS` graph), `pipeline/orchestration/shots.py` (a new optional `animatic_ref` field), `pipeline/orchestration/generate_stage.py` (`resolve_references` + the prompt role-tag in `run_frame_fan`), a new `pipeline/orchestration/animatic_stage.py` (mirror `storyboard_stage.py`), `pipeline/run.py` (the `--approve-animatic` gate + opt-in surface), `manifest.yaml` (a new `animatic:` block; keep the `post_animatic: T3` seam).

**Out of scope:** Seedance / motion conditioning (the timing artifact is captured, not consumed by motion); pinning the loaded object / desk drawing (Finding B — Sean hand-draws the page); the `post_animatic` T3 critic gate (consciously deferred — keep the seam, place the hook point, do not wire the council); anything in Em / `evals/vision_critic/`; Tier-2 calibration. Don't touch the shared `sean-screenwriting-voice.md`.

## Doctrine — non-negotiable

- **Verify against the tree, never trust a label — including this kickoff.** Confirm before editing: that `_LEGAL_TRANSITIONS` is `{PLAN:(SCRIPT,GENERATE), SCRIPT:(STORYBOARD,), STORYBOARD:(GENERATE,), GENERATE:(ASSEMBLE,), ASSEMBLE:(DONE,), DONE:()}` and that the **back-compat PLAN→GENERATE fork must survive** (a brief carrying a `shots.yaml` never enters ANIMATIC); that `shots.py`'s `_FRAME_KEYS` is the back-compat seam new fields slot into (same pattern as `chain_from`/`beat_id`/`locked`, all optional, all inert when absent); that `resolve_references` builds the ref list and `run_frame_fan` builds `prompt` (the two injection points); that the image-edit transport is `pipeline/agents/nb_pro_runner.py::invoke_image_edit` (alias `invoke_nb_pro`), the same transport Flo dispatches and the Flo-B bake-off fired live. *Cautionary tale from Tier-1 Slice A: a kickoff's "the anchors are clean" claim was false on arrival — re-derive from the files, not the prose.*
- **Two md5 guards, both must hold (neither is touched here):** Em baseline `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`; shared voice `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`.
- **Back-compat is a hard gate.** `animatic_ref` is optional; a run with no animatic resolves STORYBOARD→GENERATE **byte-identical to today**. `test_spark_shots_equivalence.py` + `test_run_shots.py` + the existing `test_run_generate_stage.py` must stay green, and a no-animatic run's reference stack + prompts must be unchanged (prove it).
- **The spike gates the build.** Do not write a line of stage code until Sean has eyed the spike output and ruled GO. A red/ambiguous spike → write the spike field report, stop, and surface the result.
- **Fleet-ops for the costed spike** ([`docs/fleet-ops-protocol.md`](fleet-ops-protocol.md)): subscription billing for Claude (never `ANTHROPIC_API_KEY`); the spike's image calls are **Gemini-metered** (`GEMINI_API_KEY` expected), budget ceiling **~$2**, run from a **plain terminal** (no nested-SDK throttle), one isolated worktree, single owner, clean teardown.
- **$0 stub-green for the build (steps 2–7).** No model spend; stubbed Em + the `--stub` offline path prove the stage end-to-end. **TDD red→green**, small revertible commits, in the order below.

## §0 — fleet-ops gates (before anything)

```bash
cd <anima main checkout>
git fetch origin
git log --oneline -1 origin/main                        # record the HEAD you branch from (expect a287ef2 or newer)
git rev-list --left-right --count origin/main...HEAD    # expect 0 0
md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md  # 2af75906502f1caf8857e18828ceb2e4
md5sum pipeline/agents/prompts/sean-screenwriting-voice.md               # 945af824fa53b948a18ac6bf206d67ef
echo "ANTHROPIC=${ANTHROPIC_API_KEY:-ABSENT}  GEMINI=${GEMINI_API_KEY:+SET}"   # expect ANTHROPIC=ABSENT  GEMINI=SET
python -m pytest tests/ -q                              # expect green (~660); record the exact count
```

One isolated worktree off `origin/main`; ALL edits inside it. Single owner.

## Step 1 — the costed spike: the kickflip (HUMAN-GATED; proves the bet before any build)

Goal: does a hand-drawn placement rough make NB2 put **Sean** into poses far outside his sitting-and-drawing register — a skateboard kickflip — respecting position, facing, scale, and the airborne body line, while holding his identity? This is a stronger, more honest test than reproducing the 06-18 drift: a genuinely new action, and a rough that carries a *competing* character so the role-tag quarantine is tested at its hardest. **Single character: `characters/sean-anchor/anchor.png` only — no mascot.**

The corpus is **prepared and turnkey** at `images/anima-frames-test/spike-selection/` (read its `README.md`): six keys that read as a complete kickflip — `key-1_F2` anticipation → `key-2_F3` pop → `key-3_F5` apex → `key-4_F9` mid-flip → `key-5_F14` catch/land → `key-6_F18` ride-out — plus an **A/B** sub-test on two of them (`*_F2`/`*_F5` shipped both as the colored rough and as a stripped pose silhouette). The full 18 frames sit in the parent dir for the proven-bet follow-on.

1. **Verify the corpus + anchor against the tree.** Confirm the six keys + the two silhouettes exist under `spike-selection/` and `sean-anchor/anchor.png` is the identity ref. The roughs already exist (a prior project), so this spike isolates the *mechanism* cleanly — the authoring-effort question (the original #1 risk) gets tested later when Sean draws roughs for a real loop run.
2. **Build a tiny standalone spike harness** (scratch, not committed to `pipeline/`). For each key, call `invoke_image_edit` off **Sean's anchor + that key's rough** — re-anchored every key, **no chaining between keys** (NB2 research: re-anchor to canonical, never chain off a generated frame). Two reference slots: anchor first (identity), rough last (placement), with the positional role-tag clause: *"The final reference is the composition target: match the body pose, position, facing, and scale shown there; do NOT copy its line quality, colour, character, or background — this is Sean (identity from the first reference), warm pencil-test register on cream paper."* Run each key (a) prose-only baseline and (b) with-rough; run the **A/B** (colored rough vs silhouette) on the two prepared keys. Because the cast is a single character, the ref stack is just anchor + rough (2 slots) — minimal dilution risk by construction.
3. **Sean's eye is the arbiter** (engine truth). Build side-by-side contact sheets (baseline vs with-rough; colored vs silhouette). Sean judges: did the rough land Sean in the kickflip pose? Did his identity hold across six radically different poses? Did the quarantine strip the red shirt / face / pink ground? Did the silhouette beat the colored rough, or did both work?
4. **Write the spike field report** to `docs/anima-test-runs/2026-06-18-animatic-spike-field-report.md`: spend, the contact sheets, the colored-vs-silhouette finding, identity-hold-across-poses, and the GO/NO-GO. **On NO-GO: stop here and surface the result** (the mechanism needs rethinking — a stronger conditioning path or heavier prompt-staging — before any stage is built). On GO: the full 18-frame run becomes the proven-bet follow-on and a publishable museum piece.

Budget: six keys × (baseline + with-rough) + the two-frame A/B ≈ **~$2.5**, Gemini-metered, under the ~$2–3 ceiling. **Do not run all 18 in the spike.**

## Steps 2–7 — build the stage (only on GO; $0 stub-green, TDD)

2. **`animatic_ref` schema — `shots.py` + `tests/test_run_shots.py`.** Optional per-frame `animatic_ref: str | None = None` in `Shot` + `_FRAME_KEYS`. Validate lightly when set (a non-empty string; do **not** require the file to exist at load time — the ingest populates it). Red→green: a frame with `animatic_ref` round-trips; absent → unchanged. Then run `test_spark_shots_equivalence.py` + `test_run_shots.py` green (back-compat proof).

3. **Reference + prompt wiring — `generate_stage.py` + `tests/test_run_generate_stage.py`.** In `resolve_references`, append `shot.animatic_ref` **last** when present (after extras, after the dedup keeps it once). In `run_frame_fan`, when `animatic_ref` is set, add the positional role-tag clause to `prompt` (validated in step 1). Test: a frame with `animatic_ref` puts it last in the ref list and the clause in the prompt; **a frame without it produces a byte-identical ref list and prompt to today** (the hard back-compat assertion).

4. **The ANIMATIC stage — `state.py` + new `animatic_stage.py` + `run.py` + tests.** Add `ANIMATIC` to `STAGES` between `STORYBOARD` and `GENERATE`; in `_LEGAL_TRANSITIONS` set `STORYBOARD: ("ANIMATIC", "GENERATE")` (keep GENERATE for skip/back-compat) and add `ANIMATIC: ("GENERATE",)`. New `animatic_stage.py` (mirror `storyboard_stage.py`): on entry, pause and print the author instructions (drop frame-named roughs into `runs/<id>/animatic/` + the holds sidecar). A new `run.py --approve-animatic` runs the **deterministic ingest**: validate each rough maps to a real frame id and the holds sidecar parses; populate each shot's `animatic_ref` from the convention **into run-state** (the locked `shots.yaml` is never mutated); override the run's holds from the sidecar; capture the artifacts; then call the shared `enter_generate`. Opt-in surface: a `manifest.yaml` `animatic:` block (`enabled: false` default + the dir/sidecar convention) and/or a `--animatic` run flag — **default off**. The storyboard gate routes to ANIMATIC only when animatic is enabled; otherwise STORYBOARD→GENERATE unchanged. Tests (stub-green): an opt-in run pauses at ANIMATIC, ingests a stub rough + holds, advances to GENERATE with `animatic_ref` populated + holds overridden; a default (no-animatic) run skips the stage entirely and is byte-identical; the `--stub` offline path still reaches DONE.

5. **Manifest + the deferred T3 seam.** Add the `animatic:` block. Keep `critics.placement.post_animatic: T3` declared; place a **one-line hook point** (a no-op / clearly-commented seam) in `animatic_stage.py` where the gate will wire, and record the promotion trigger (timing feeds an orchestrated Motion phase). Do **not** wire the council.

6. **Holds → ASSEMBLE.** Confirm (and test) that the holds the ingest writes to run-state are what `assemble_stage` consumes — the timing half's real, present consumer. A no-animatic run's holds are unchanged.

7. **Docs.** CHANGELOG.md (the stage, the mechanism, the deferred gate, citing the post-mortem); CLAUDE.md (the 10-phase section's Phase 4 status, the run-orchestrator commands + the new `--approve-animatic` gate, the `animatic_ref`/`animatic:` notes); the design doc's DoD checklist ticked. Re-assert both md5 guards.

## Acceptance (all must hold before the PR)

- **Spike:** field report written; Sean's GO recorded (or NO-GO surfaced and the build not begun).
- `python -m pytest tests/` green (~660 + new, 0 regressions); `pipeline/tests/` green; `test_spark_shots_equivalence.py` + `test_run_shots.py` + `test_run_generate_stage.py` green.
- **Back-compat proven:** a no-animatic run's reference stack + prompts + holds are byte-identical to today; the PLAN→GENERATE fork still bypasses ANIMATIC.
- The opt-in ANIMATIC stage pauses, ingests roughs + holds deterministically, populates `animatic_ref` without mutating the locked board, and advances to GENERATE — proven stub-green.
- `animatic_ref` rides last + role-tagged into generation; holds drive ASSEMBLE; both captured under `runs/<id>/animatic/`.
- `post_animatic` T3 gate consciously deferred — seam declared, hook point placed, trigger recorded; council NOT wired.
- Both md5 guards intact; nothing under `evals/vision_critic/`; shared voice unchanged.
- CHANGELOG.md + CLAUDE.md updated. One squash PR off the isolated worktree. Clean teardown.

## When done

Report: the commits; the spike GO/NO-GO + spend; the new test count + full-suite-green-credential-free confirmation; both md5 guards intact; the back-compat byte-identity proof; and a one-paragraph field note on any seam that fought you. Then a costed run that exercises the new stage end-to-end and ships a loop whose placement holds — the real proof. After that, **update ROADMAP.md: mark TOP-1 Animatic built, advance Current Focus to workstream 2 (Tier-2 Em calibration).** Per the anti-drift contract, do not open Tier 2 until this DoD is met.
