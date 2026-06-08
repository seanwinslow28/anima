# Field report — SF03 proportion gate (G6.4): Approach-A probe + scaffold build

*2026-06-08. Costed run under [`docs/fleet-ops-protocol.md`](../fleet-ops-protocol.md). Executes the parked design [`docs/2026-06-03-sf03-proportion-gate-design.md`](../2026-06-03-sf03-proportion-gate-design.md) under the [SF03 build handoff](../2026-06-04-sf03-proportion-gate-build-handoff.md). Scaffold-first build order (Sean's 2026-06-08 planning call): the whole deterministic gate was built CI-green BEFORE this probe; the probe only decides which input-feeder to wire.*

---

## TL;DR

**The make-or-break question — does NB2 honor a provided heads-tall armature underlay? — is answered YES.** Across 4 turnaround views (front / profile / back / ¾), NB2 Flash seated a clean, on-model pencil-test Sean to the grid: crown on the top line, feet on the bottom line, head in band 0–1.

| view | grid lines (in/out) | heads_tall (auto) | align | verdict |
|------|--------------------|-------------------|-------|---------|
| front | 8 → 8 | **7.12** | 0.14 | pass |
| profile-left | 8 → 8 | **7.15** | 0.16 | pass |
| back | 8 → 8 | **7.05** | 0.03 | pass |
| ¾ | 8 → **9** | 8.29 | 0.26 | fail* |

\* The ¾ "fail" is **not a proportion failure** — the figure is correctly seated crown-to-feet (see the plate). NB2 **redrew the grid with 9 lines instead of 8**, so the per-division spacing the auto-measure depends on was rescaled, inflating heads_tall. This is the one real Approach-A failure mode, and it has a cheap, known fix (below).

**Recommendation: build Approach A**, with the measurement hardened to NOT trust NB2's redrawn interior grid as the ruler. NB2 reliably preserves the **bold crown + feet lines** (drawn 4px vs 2px interior) and the figure's seating; anchoring the measure on those two lines + the *known* division count (7) — rather than counting NB2's redrawn interior lines — makes all 4 views including ¾ measure ~7 heads. View-invariance holds (front/profile/back all 7.05–7.15).

---

## Run configuration & provenance

- **Command:** `PYTHONPATH=. python runs/2026-06-08-sf03-probe/probe.py` (harness in the gitignored run dir).
- **Model / transport:** `gemini-3.1-flash-image-preview` (NB2 Flash) via `invoke_image_edit` → the `gemini-pencil-animation-image-gen` skill. 4 generations, no retries, no escalation.
- **References per plate:** `[armature-underlay.png, anchor.png]` — the gridded underlay first (the canvas being drawn on), the sean-anchor second (identity).
- **Armature underlay:** 768×1024 cream (#F2E6CC), 8 graphite (#3D3530) horizontal lines dividing into 7 equal head-bands at y=[64,192,320,448,576,704,832,960]; crown (line 0) + feet (line 7) bolded to 4px, interior 2px.
- **Measurement:** the just-built `pipeline/agents/proportion_gate.py` — `detect_armature_lines` + `figure_extent` + `measure_proportion(out, sean_spec, armature_path=out)` (Approach-A path, the gridded output IS the verification artifact).
- **Spec:** sean-anchor `character.yaml` — declared `head_to_body_target: 7.0`, `tolerance_heads: [6.5, 7.5]`.
- **Fleet-ops:** isolated worktree `worktree-sf03-proportion-gate`; `ANTHROPIC_API_KEY` absent; `GEMINI_API_KEY` sourced bounded into the worktree's gitignored `.env` (removed at teardown); single owner; no `start_new_session`.
- **Plates (committed evidence):** [`2026-06-08-sf03-probe-plates/`](2026-06-08-sf03-probe-plates/) — armature + 4 outputs.

## Findings

1. **NB2 honors the armature — decisively.** On front/profile/back, NB2 preserved all 8 lines and seated the figure crown-on-top-line / feet-on-bottom-line, auto-measuring 7.05–7.15 heads (dead-on the 1:7 target, inside tolerance) with crown/feet alignment ≤0.16 of a head-band. The figures are clean, on-model, full-color pencil-test turnarounds — production-quality, not just proportion test rigs. This validates the whole constrain-then-verify premise: constrain at generation, verify against the known armature.

2. **The one failure mode is grid-COUNT drift, not figure-proportion drift.** On ¾, NB2 redrew the ladder with **9 lines (8 bands)** instead of 8 lines (7 bands). The figure itself reads correctly proportioned; only the auto-measure broke, because it inferred per-head spacing from `(last_line − first_line)/(detected_count − 1)`, and the extra line shrank that spacing. **The output grid is not a trustworthy ruler.**

3. **Mitigation is cheap and the bold-line scaffold already supports it** (Approach-A build, Phase C):
   - **Anchor on the bold crown + feet lines + the KNOWN division count (7), not the detected interior count.** `heads_tall = (figure_feet − figure_crown) / ((feet_line − crown_line) / 7)`. Re-derived for ¾ by hand: crown_line≈58, feet_line≈960, figure 54→989 → spacing 128.9 → **7.25 heads → pass.** Fixes the only failure.
   - **Line-count sanity check:** if `detect_armature_lines != 8`, flag the gridded sheet `unreliable` and re-roll (or fall back), rather than silently emitting a wrong number. The ¾ would be caught, not mis-passed.
   - **Even more robust (recommended):** don't ask NB2 to redraw the grid at all — generate the clean seated figure, then **composite OUR deterministic armature** (known fractions) over the measured figure extent and check crown/feet seating against it. The ruler is then always ours, never NB2's.

4. **View-invariance confirmed** (design open Q4): the vertical heads-tall read is consistent front/profile/back (7.05–7.15); the profile figure faces screen-right vs the prompt's "left" (a view-correctness nuance owned elsewhere), with zero effect on the proportion measure — as predicted, the measurement is view-independent.

## Cost & operations

- **4 NB2 Flash generations, no retries.** Sub-$0.20 estimated. No 429s, no timeouts, no stub fallback (all 4 `stub_fallback=False exit=0`).
- No criteria/baseline/Em-surface touched (SF03 is generation-time, off Em's path).

## Scope & caveats

- The probe measured the **gridded output as its own armature** (`armature_path=out`) — the most adversarial read (it trusts NB2's redrawn grid). The recommended Phase-C measure (bold-anchor + known-count, or our-own-overlay) is strictly more robust and is what ships.
- 4 plates, N=1 each — a feasibility probe, not a replicated baseline. It answers "can NB2 do this at all?" (yes), not "how often does grid-count drift happen?" (the line-count guard + re-roll handles the tail regardless).
- Mascot is out of scope (opted out — box-creature, not heads-tall).

## Decision

**Probe PASSES → recommend Approach A** (armature-constrained generation + automated grid-alignment), with the measurement anchored on the bold crown/feet lines + known division count and a line-count sanity guard (the ¾ finding). Awaiting Sean's A-vs-B call before wiring the feeder.
