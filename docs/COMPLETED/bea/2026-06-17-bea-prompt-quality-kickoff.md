# Kickoff — Tier 1 Slice A: Bea prompt quality + reference hygiene ($0 stub-green, TDD)

*Paste the block below into a fresh Claude Code session in the `anima` repo. Self-contained.
Plan of record: [`docs/2026-06-17-tier1-fixes-build-plan.md`](../orchestrator/2026-06-17-tier1-fixes-build-plan.md) (Slice A).
Why: [`docs/anima-test-runs/2026-06-17-spark-authored-costed-run-post-mortem.md`](../../anima-test-runs/2026-06-17-spark-authored-costed-run-post-mortem.md) (F2/F3/F6).*

---

You're fixing the three prompt-authoring problems the **first live costed run** surfaced — all in Bea's
authoring, all fixable in her context + one asset, no orchestrator code. **$0 / stub-green / TDD.** The
goal: the next human-in-loop run needs far less curation because Bea's edit-frame prompts land terse and
no reference text bleeds into the frames. Read first: the build plan (Slice A) and post-mortem §3
(Findings 2, 3, 6) above; then `PHILOSOPHY.md`, `CLAUDE.md`, and the NB2 editing research
[`docs/research/2026-05-30-nb2-editing-character-consistency-template.md`](docs/research/2026-05-30-nb2-editing-character-consistency-template.md)
(the storyboard-variant template is exactly what Bea should emit).

**What you change:** Bea's persona context (`pipeline/agents/prompts/bea-storyboard-context.md`), one
reference asset (`characters/claude-mascot/source-refs/sean-with-claude-mascot.png`), the
`evals/storyboard_artist/` scaffold, and docs.

**Out of scope:** Slice B (eye-gate ergonomics — next kickoff); the loop-return *chaining* change in
`generate_stage` (deferred — the prompt discipline below fixes it); anything in Em / Tier 2. Don't
touch `evals/vision_critic/` or the shared `sean-screenwriting-voice.md`.

## Doctrine — non-negotiable

- **Verify against the tree, never trust a label — including this kickoff.** Confirm before editing:
  that `bea-storyboard-context.md` today says "every prompt ends in the register clause block" with
  **no** establishing-vs-edit distinction and **no** no-text negative (that's the gap); that the
  `A-7` label is actually on `sean-with-claude-mascot.png` (open it) and isn't also on the anchors;
  that the shipped run's frames 2–5 prompts were full re-descriptions (the defect) and the curated
  fixes that worked opened `Same fixed two-shot … ONLY CHANGE: …`; that Bea infers frame roles from
  `beats.json` (first beat = establishing, ascending ids = the chain) so this is a context rule, not
  a code change. Cautionary tale from the build itself: the Bea kickoff once had the cast rule
  backwards and the tree corrected it — re-derive from the run evidence, don't trust prose.
- **Two md5 guards, both must hold:** Em baseline
  `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`;
  shared voice `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`.
  This slice changes **`bea-storyboard-context.md`**, not the shared voice file.
- **$0 — stub-green only.** No model spend; Bea's stub path + the eval lint prove the behavior
  credential-free. (The real Bea authoring is exercised by Sean's next live run, not here.)
- **TDD red→green**, small revertible commits: context rule, then the no-text negative, then the asset
  crop, then the eval, then docs.

## §0 — fleet-ops gates (before any edit)

```bash
cd <anima main checkout>
git fetch origin
git log --oneline -1 origin/main                        # expect 98aeed8 (#55) or newer
git rev-list --left-right --count origin/main...HEAD    # expect 0 0
md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md  # 2af75906502f1caf8857e18828ceb2e4
md5sum pipeline/agents/prompts/sean-screenwriting-voice.md               # 945af824fa53b948a18ac6bf206d67ef
echo "${ANTHROPIC_API_KEY:-ABSENT}"                     # expect ABSENT
python -m pytest tests/ -q                              # expect green (647)
```

One isolated worktree off `origin/main`; ALL edits inside it. Single owner.

## Build order (TDD)

1. **The establishing-vs-edit rule in `bea-storyboard-context.md`.** Add a clear section: the **first
   shot** is the establishing generation (built from the Bibles) → a **full descriptive prompt**.
   **Every subsequent shot is an NB2 edit off the previous approved frame** → write it as a **terse
   `ONLY CHANGE: <single delta>`** opening with a continuity anchor (`Same fixed two-shot, same
   framing/identities/scale as the previous frame.`). One change per frame; no re-describing the whole
   scene (that competes with the reference and drifts — cite the 2026-05-30 storyboard-variant
   template). **If the piece loops, the final shot returns to the opening** → author it as
   `composition identical to frame 1`, an end-state match, **not** a multi-step "drains back / returns"
   transition (that was the F05 failure).

2. **The no-text negative in the register clause block.** In the same file's register-block
   instruction, add `Do not render any text, captions, labels, or watermarks.` so every emitted prompt
   carries it (prevents reference-text bleed).

3. **Crop the `A-7` label from the pairing reference.** Clean `A-7` out of
   `characters/claude-mascot/source-refs/sean-with-claude-mascot.png` (the frame-1 extra-reference and
   the bleed source). Preserve the original elsewhere under `source-refs/` if useful; the run-facing
   file must be label-free. Re-check the sean/mascot anchors carry no visible label either.

4. **Eval scaffold case (`evals/storyboard_artist/`).** Add a case asserting the behavior: on a
   multi-beat looping sheet, frame 1's prompt is full and frames ≥2 open with the `Same … ONLY
   CHANGE:` editing form — a deterministic substring/length **lint (warning, not a hard gate)**, since
   the human still curates. Mirror the existing ships-red case style; keep it CI-green mocked.

5. **Docs.** CHANGELOG.md entry (the rule, the negative, the crop, citing the post-mortem F2/F3/F6).
   One-line CLAUDE.md update to the Bea row (establishing-vs-edit discipline). Re-assert both md5 guards.

## Acceptance (all must hold before the PR)

- `bea-storyboard-context.md` carries: the establishing-vs-edit rule, the loop-return-as-"match frame 1"
  rule, and the no-text negative in the register block.
- `sean-with-claude-mascot.png` is label-free (visual confirm); no anchor carries a visible label.
- The eval lint flags a full re-description on a non-establishing frame and accepts the terse editing
  form (proven by the case).
- `python -m pytest tests/` green (647 + any new, 0 regressions); `pipeline/tests/` green.
- Both md5 guards intact; the shared `sean-screenwriting-voice.md` unchanged; nothing under
  `evals/vision_critic/`.
- One squash PR off the isolated worktree. Clean teardown.

## When done

Report the commits, the new test/eval count, full-suite-green-credential-free confirmation, both md5
guards intact, and a one-paragraph field note on any seam that fought you. Then stop — Slice B
(eye-gate ergonomics) is the next kickoff, and the Em calibration campaign (Tier 2, the autonomy core)
is planned in Cowork after Tier 1 lands.
