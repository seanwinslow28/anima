# Build Plan — Tier 1 fixes from the first costed run (the quick wins)

*Dated 2026-06-17. Companion to the [costed-run post-mortem](../../anima-test-runs/2026-06-17-spark-authored-costed-run-post-mortem.md) §5. These are the cheap, high-leverage fixes that remove the failure classes the first live run surfaced — so the next human-in-loop run is clean before we take on the hard autonomy work (Em calibration, Tier 2). All $0 / stub-green / TDD.*

> **The framing (post-mortem §4):** Tier 1 is *autonomy-enabling*, not autonomy-blocking. Each item is a place the agents produced work a human had to fix at a gate. Removing them shrinks the curation burden now and deletes drift sources a critic would otherwise have to catch later. The autonomy *blocker* — Em matching Sean's eye — is Tier 2, planned separately.

---

## Packaging — two slices + one deferral

The four post-mortem quick wins group by where they live:

| # | Fix (post-mortem finding) | Slice |
|---|---|---|
| 1 | Bea writes edit-frame prompts as terse `ONLY CHANGE` deltas, not full re-descriptions (F2) | **A** |
| 2 | Bea authors the loop-return frame as "match frame 1" (F3, authoring half) | **A** |
| 3 | Reference hygiene — `no text/labels/watermarks` negative + crop the A-7 label (F6) | **A** |
| 4 | Eye-gate ergonomics — surface Em's proposed patch + steer the retry note positive (F4 + F5) | **B** |
| — | Loop-return *chaining* off frame 1 in `generate_stage` (F3, structural half) | **Deferred** |

**Slice A — Bea prompt quality + reference hygiene** is a pure agent-context + asset change (no orchestrator code). Biggest payoff: it attacks the run's largest cost (four hand-edited prompts) and removes the label bleed. Build first.

**Slice B — eye-gate ergonomics** is an orchestrator-UX change (`generate_stage` print + `run.py`). It makes the human-in-loop retry path stop fighting the user, and surfaces the patch Em already proposes — the seam that later becomes propose→apply (Tier 2).

**Deferred — loop-return chaining.** The frame-5 fix that *worked* this run was purely the prompt rewrite ("composition identical to frame 1"); we never changed the chain recipe. So teaching Bea to author the loop frame as a match (Slice A) is the suspenders; changing `generate_stage` so loop-return frames chain off frame 1 instead of the prior frame is the belt. Skip it now — **promotion trigger:** if loop-return drift recurs after Slice A ships, build the chaining change (a `shots.yaml` per-frame `chain_from`/`loop_return` field + `resolve_references` honoring it).

---

## Slice A — Bea prompt quality + reference hygiene ($0, stub-green)

**Root cause (verified):** `pipeline/agents/prompts/bea-storyboard-context.md` tells Bea every prompt is "prose-action ending in the register clause block" but carries **no establishing-vs-edit distinction** and **no no-text negative**. So Bea wrote full literary re-descriptions for frames 2–5 (NB2 *edits* off the chained reference), which the 2026-05-30 NB2 research says induces drift — and the register block she appends has no `no text` clause, so the A-7 label on the pairing reference bled into every frame.

**Changes:**

| File | Change |
|------|--------|
| `pipeline/agents/prompts/bea-storyboard-context.md` | Add the **establishing-vs-edit rule**: the first shot is the establishing generation → a full descriptive prompt; **every subsequent shot is an NB2 edit off the previous approved frame → write it as a terse `ONLY CHANGE: <single delta>` opening "Same fixed two-shot, …"** (cite the 2026-05-30 storyboard-variant template). If the piece loops, **the final shot returns to the opening → author it as "composition identical to frame 1"**, not a multi-step transition. Add the **no-text negative** to the register clause block: `Do not render any text, captions, labels, or watermarks.` |
| `characters/claude-mascot/source-refs/sean-with-claude-mascot.png` | **Crop/clean the `A-7` production label** from the pairing reference (the bleed source). Keep a copy of the original under `source-refs/` if useful; the run-facing reference must be label-free. Re-verify no other anchor carries a visible label. |
| `evals/storyboard_artist/` | Add a scaffold case asserting the establishing-vs-edit behavior: given a multi-beat looping sheet, frame 1's prompt is full and frames ≥2 open with the `Same … ONLY CHANGE:` editing form (a deterministic substring/length check — a **lint/warning**, not a hard gate, since the human still curates). Mirror the existing ships-red case style. |
| `CHANGELOG.md` | Dated entry: the establishing-vs-edit rule, the no-text negative, the A-7 crop, why (the costed-run post-mortem F2/F3/F6). |
| `CLAUDE.md` | One-line update to the Bea row noting the establishing-vs-edit prompt discipline. |

**Why context, not code:** Bea infers frame roles from the beat sheet she already reads — first beat = establishing, ascending ids = the chain, the brief's "loops back to frame 1" = the return. The distinction is a prompt-authoring rule, so it lives in her context. No `storyboard_artist.py` structural change required for v1 (the eval lint is the only new check).

**Acceptance:**
- `bea-storyboard-context.md` carries the establishing-vs-edit rule + loop-return-as-match-frame-1 + the no-text negative; the shared `sean-screenwriting-voice.md` md5 stays `945af824…` (Bea-only change).
- The pairing reference is label-free (visual confirm); a stub authoring run's frame-2+ prompts open with the editing form.
- The eval case passes (lint flags a full re-description on a non-establishing frame; accepts the terse form).
- `python -m pytest tests/` green credential-free; Em baseline md5 `2af75906…` untouched; nothing under `evals/vision_critic/`.
- One squash PR off an isolated worktree.

## Slice B — eye-gate ergonomics ($0, stub-green)

**Root cause (verified):** the eye gate (`generate_stage.run_frame_fan` tail) prints `Em[character]: verdict (conf, cites)` but **not the proposed patch** Em emits (`patches: N` in `em_verdicts.jsonl`, staged to `manifest.lock.yaml`). And `--retry-frame --note` appends the note verbatim as `CORRECTION (address the prior attempt's defect): <note>` with no steer toward the positive/identity-lock framing the NB2 research requires — so naming a defect reinforces it (the F05 light-blue loop).

**Changes:**

| File | Change |
|------|--------|
| `pipeline/orchestration/generate_stage.py` | At the eye gate, when Em proposed a patch, **print the proposed correction** (the staged prompt diff / its rationale + cited rule) so the human can see Em's grounded fix. Add a one-line steer to the retry hint: *"write the note as the desired state (positive identity-lock), not the defect — it's appended to the prompt."* |
| `run.py` (retry hint) | Mirror the positive-framing steer in the `--retry-frame` help/usage text. (Optional stretch: a `--apply-em-patch` flag that re-rolls using Em's staged patch instead of a free-text note — the first concrete propose→apply step; gate behind Tier 2 if it grows.) |
| `docs/2026-06-16-spark-authored-costed-run-runbook.md` | Update the per-frame + troubleshooting sections: assert the desired state in retry notes, never name the defect; mention Em's surfaced patch. |
| `CHANGELOG.md` | Dated entry: eye-gate patch surfacing + positive-retry-note steer (post-mortem F4/F5). |

**Acceptance:**
- A stub run's eye gate prints Em's proposed patch when one exists (proven by test against a stubbed Em verdict carrying a patch).
- The retry hint text steers positive framing.
- `python -m pytest tests/` green credential-free; both md5 guards intact.
- One squash PR off an isolated worktree.

---

## Sequencing & guards

Build **Slice A first** (biggest payoff, pure context+asset, zero orchestrator risk), then **Slice B**. Each is its own small squash PR off an isolated worktree from `origin/main`, $0 stub-green, TDD — the discipline that landed Sam/Bea/the wiring clean.

Two standing guards on both slices: Em verdict-baseline `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`, and Sam's shared voice file `sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`. Neither slice touches `evals/vision_critic/` or the shared voice file.

## After Tier 1

The next human-in-loop run should need far less curation (Bea's edit-frame prompts land terse; no label bleed; the retry path helps instead of fights). That clean run is also the ideal place to **gather more Em-vs-eye labels** for Tier 2 — the Em calibration campaign, which is the actual road to stepping away. Planned in Cowork once Tier 1 lands.
