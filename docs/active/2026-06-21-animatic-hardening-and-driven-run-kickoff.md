# Kickoff — Animatic hardening + Claude-Code-driven Spark re-run (fix two real bugs, then drive the run)

*Paste into a fresh Claude Code session in the `anima` repo. Self-contained.
Why: the 2026-06-21 Spark-animatic run (DoD #6) was cancelled after surfacing two real bugs — captured below and in [`docs/active/2026-06-21-animatic-frame-count-flaw.md`](2026-06-21-animatic-frame-count-flaw.md). Design of record for the phase: [`docs/active/2026-06-18-animatic-phase-design.md`](2026-06-18-animatic-phase-design.md).*

**Operating-model change (read this first):** from now until the pipeline is complete, **Claude Code drives the runs** — you (Claude Code) run the commands, read the tracebacks, handle retries, place files, and surface to Sean **only the decisions that need his eye.** Sean is done operating the terminal by hand. This kickoff has two parts: a **$0 TDD hardening** pass that fixes the two bugs, then a **costed run you drive end-to-end** to close DoD #6. The eventual frontend is a separate, later workstream — not in scope here.

---

## The two bugs (both verified against the tree)

**Bug 1 — Maya can author an illegal `impact_tag`, and nothing catches it until three gates later.** The cancelled run died with `ValueError: Criterion 'AC.timing.on-twos' has unknown impact_tag 'timing'`. Root cause (confirmed in [`pipeline/criteria.py`](../../pipeline/criteria.py)): there are two closed vocabularies — `VALID_CATEGORIES` (line 41, *includes* `timing`) and `VALID_IMPACT_TAGS` (line 44, does **not**). Maya correctly used `timing` as the AC *category* (`AC.timing.on-twos`) but also stamped `impact_tag: "timing"`, conflating the two. The criterion's own text says *"enforcement is structural, not perceptual"* — so the right tag was `structural`. Worse: the strict check only runs inside `load_all_criteria`, which on the authoring path first fires at the **animatic gate** — so the bad criterion **locked clean at plan-approve and exploded four gates later.** That late explosion is exactly the misery the operator-driven model exists to absorb.

**Bug 2 — the human's frame count is vetoed by the agent's board.** Sean drew **7** placement roughs; Bea had boarded **5**; `--approve-animatic` hard-errored on `F06`. The board's frame count is owned by Bea, and the human's animatic must conform — which inverts PHILOSOPHY's one non-negotiable belief (*the human owns timing*). [`pipeline/agents/storyboard_artist.py`](../../pipeline/agents/storyboard_artist.py) takes **no** frame-count input today.

Read first: the frame-count design seed (above); `pipeline/criteria.py` (the two vocabularies + `validate_criteria`/`_validate_v1_1`); `pipeline/agents/planner.py` (where Maya emits `impact_tag`); `pipeline/orchestration/plan_stage.py` + `storyboard_stage.py` + `animatic_stage.py`; then `PHILOSOPHY.md`, `ROADMAP.md`, `CLAUDE.md`.

## Doctrine — non-negotiable

- **Verify against the tree, never trust a label — including this kickoff.** Confirm the two vocabularies and the exact line where Maya sets `impact_tag`, the gate where `load_all_criteria` first validates on the authoring path, and that Bea has no count input — *before* editing. The cancelled run is the cautionary tale: a criterion that locked clean still exploded downstream.
- **Two md5 guards, both must hold (neither is touched here):** Em baseline `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`; shared voice `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`.
- **Back-compat is a hard gate.** `--frames` is optional (absent → Bea's behavior byte-identical); the impact-tag fix must not reject any *valid* existing criteria. Prove both.
- **Part 1 is $0 stub-green, TDD.** Part 2 is the only spend (Gemini-metered).
- **The taste gate stays Sean's eye.** Em is **not** calibrated (that's Tier 2). You drive the mechanics and *propose*; **you do not auto-approve frames.** At each per-frame gate, present the candidate + Em's read and **wait for Sean's call.**

## §0 — pre-flight

```bash
cd <anima checkout> && git fetch origin
git log --oneline -1 origin/main                        # 6ea67bf (#61) or newer
md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md   # 2af75906…
md5sum pipeline/agents/prompts/sean-screenwriting-voice.md                # 945af824…
echo "ANTHROPIC=${ANTHROPIC_API_KEY:-ABSENT}  GEMINI=${GEMINI:+SET}"      # ANTHROPIC=ABSENT, GEMINI key present for Part 2
python -m pytest tests/ -q                              # green baseline; record the count
```

One isolated worktree off `origin/main` for Part 1; single owner.

## Part 1 — the $0 hardening (TDD, small revertible commits)

### Fix A — legal impact_tags, validated at lock (not four gates later)

1. **Constrain Maya.** In `planner.py`, make Maya's instructions name the closed `VALID_IMPACT_TAGS` set explicitly and forbid using a *category* word (`timing`, `tone`, etc.) as an impact_tag. A timing/structural criterion takes `impact_tag: structural`.
2. **Validate at authoring + lock — fail fast.** Run the existing `validate_criteria` on Maya's output **at plan authoring** (so an illegal tag triggers a re-roll within her call ceiling) **and** at `--approve-plan` (so an invalid criteria file can **never lock**). The error message already names the legal set — surface it at the gate, not at the animatic stage.
3. **Tests (red→green):** a criterion with `impact_tag: "timing"` is rejected at authoring/plan-approve with the legal-set message; a timing criterion tagged `structural` passes; every *currently valid* fixture still validates (back-compat). Do **not** add `timing` to `VALID_IMPACT_TAGS` — that vocabulary drives Em's escalation and timing is not an Em axis; the fix is correct *labeling*, not a wider vocabulary.

### Fix B — the human owns the frame count (`--frames N → Bea`)

The clean, buildable fix — **not** the animatic-appends-frames prompt hack (that has an unresolved prompt-ownership problem and stays the design seed's future slice):

1. **`--frames N`** on `python -m pipeline.run` (and an optional `frames:` brief field), threaded to Bea as a **target loop length.** Bea boards N frames with real, authored prompts (the board is where prompts live — so the count must reach Bea, not be bolted onto the animatic).
2. **Deterministic count check** at the storyboard gate: when a target is set, validate the curated board has exactly N frames; if Bea missed, the board is surfaced for curation to N before lock (you, the operator, curate it).
3. **Surface the board frame count when the ANIMATIC gate opens** (`run_animatic_stage`'s printout already lists frame ids — make the *count* explicit) so a rough/board mismatch is visible **before** dropping, not after.
4. **Tests:** `--frames 7` makes Bea target 7 + the count check fires; absent → Bea byte-identical; the animatic-gate printout states the count.

Docs: CHANGELOG (both fixes, citing the cancelled run); CLAUDE.md (the `--frames` flag + the impact-tag-validated-at-lock note); tick the frame-count design seed's status. Re-assert both md5 guards. One squash PR; merge.

## Part 2 — drive the Spark-animatic re-run (costed; you operate, Sean decides)

After Part 1 merges and is pulled, drive the run end-to-end. **You run every command**; Sean only makes taste calls you surface.

- **Throttle check first.** This run shells out to the Claude SDK for Maya/Sam/Bea. Verify whether driving it from your session nests/throttles those calls (fleet-ops seam #4). If it throttles, handle it (run the authoring stages so they complete, or report the wall-clock honestly) — **never let an authoring stage silently stub** (the stub-marker scan must stay a hard fail).
- **Start with the count set so all seven roughs fit:**
  ```bash
  python -m pipeline.run --brief briefs/2026-06-16-spark-authored --slug spark-animatic --animatic --frames 7
  ```
- **Drive the gates, surfacing only Sean's eye:**
  - PLAN → present `plan.md`, get Sean's approve → `--approve-plan`.
  - SCRIPT → present the script, get Sean's approve → `--approve-script`.
  - STORYBOARD → Bea boards 7; present the board; **you curate** to a clean 7-frame loop (ids 1–7, `chain_from: 1` on 7) and get Sean's sign-off → `--approve-storyboard`.
  - ANIMATIC → copy Sean's roughs in (`cp images/final-animatic-test/F-named/F0*.png runs/<id>/animatic/`), confirm 7 ingest → `--approve-animatic`.
  - Per frame → present the candidate **+ Em's verdict/reasoning**; **wait for Sean's approve or his correction note.** On a note, `--retry-frame N --note`. **Do not auto-approve.**
- **Close DoD #6.** Eye the loop beside the 06-18 export: does placement hold (shoulder / scale / mascot consistency) where 06-18 drifted? Write `docs/anima-test-runs/2026-06-21-spark-animatic-run-post-mortem.md` — spend, retries, the before/after, whether `--frames 7` made the count Just Work, and any new seams.

## Acceptance

- Part 1: `tests/` green (+ new, 0 regressions); illegal impact_tags fail at authoring/plan-approve with the legal-set message; a valid timing criterion (`structural`) passes; `--frames N → Bea` + count check + animatic-gate count surfacing, all proven, all back-compat. Both md5 guards intact; nothing under `evals/vision_critic/`.
- Part 2: the driven run ships a Spark loop whose placement holds; per-frame approvals were Sean's eye, not auto; post-mortem written.
- **On a clean run, DoD #6 is met:** mark TOP-1 Animatic ✅ in ROADMAP and **advance Current Focus to workstream 2 (Tier-2 Em calibration).** Per the anti-drift contract, not before.

## When done

Report: the commits + new test count + full-suite-green-credential-free; both md5 guards intact; the throttle finding; the run's DoD #6 verdict (placement-holds before/after); and a one-paragraph note on any seam that fought you. The deeper "animatic natively defines frame count" fix and the frontend remain parked follow-ons.
