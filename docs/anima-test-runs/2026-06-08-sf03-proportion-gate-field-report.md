# Field report — SF03 proportion gate (G6.4): built, probed, Approach A, merged

*Ran 2026-06-08, executing the [SF03 build handoff](../2026-06-04-sf03-proportion-gate-build-handoff.md) over the parked [design spike](../2026-06-03-sf03-proportion-gate-design.md). Costed Claude Code run under [fleet-ops](../fleet-ops-protocol.md): one isolated worktree, `ANTHROPIC_API_KEY` absent, `GEMINI_API_KEY` bounded from `.env`, two human checkpoints (probe verdict + pre-merge). **Merged to `main` via [PR #33](https://github.com/seanwinslow28/anima/pull/33) (`43987df`)** — Sean approved both gates live. This report is the session retrospective; the in-tree build log + plate evidence + retroactive JSON live alongside it ([`2026-06-08-sf03-probe-and-build.md`](2026-06-08-sf03-probe-and-build.md), [`2026-06-08-sf03-probe-plates/`](2026-06-08-sf03-probe-plates/), [`2026-06-08-sf03-retroactive-sean-anchor.json`](2026-06-08-sf03-retroactive-sean-anchor.json)).*

## TL;DR

SF03 ("proportion drift") — a QA gate anima **declared but never automated** — is now a deterministic, **hard, per-character, spec-driven gate at Bible-lock**. The make-or-break probe answered YES (NB2 honors a heads-tall armature), Sean chose **Approach A**, and the whole thing shipped CI-green with zero regressions. The one conceptual lesson: **Approach A prevents drift at generation; it does not retro-audit existing plates.**

| Axis | Before | After |
|---|---|---|
| SF03 enforcement | declared, **never automated** (1:4–1:5.3 drift sailed into a *locked* Bible) | **hard gate blocks the lock** ([`proportion_gate.py`](../../pipeline/agents/proportion_gate.py)) |
| `IR.sean.proportion.head-to-body-1-to-7` | prose only | **checkable** (`character.yaml` carries `head_to_body_target: 7.0` / `tolerance_heads: [6.5, 7.5]`) |
| contract test suite | 312 passed | **358 passed** (+46, credential-free) |
| seedance suite | 10 passed | 10 passed (0 regressions) |
| probe (4 NB2 plates) | — | front 7.12 · profile 7.15 · back 7.05 · ¾ 8.29→**~7.25 hardened** |

- **The gate is real and enforcing today** — `approve_bible` recomputes on the *committed* body turnarounds and refuses the lock (rc 1) on out-of-tolerance / undeclared / unmeasurable plates.
- **The probe passed decisively** — NB2 seated a clean, on-model pencil-test Sean to the armature crown-to-feet; front/profile/back measured within the [6.5, 7.5] band, view-invariance held.
- **One finding worth carrying forward:** NB2 fits the figure *to* the grid (it drew a full body at 7 heads from a head-only anchor), so the gate works by *constraining generation*, not by auditing a finished plate.

## What we did (scaffold-first, two checkpoints)

Sean's planning call set the build order: because the measurement is deterministic PIL/numpy, build the **entire gate CI-green before spending a cent**, then let the costed probe only decide the input-feeder.

1. **Phase A — scaffold (free, TDD, 8a392da).** Built `pipeline/agents/proportion_gate.py` end-to-end (spec loader, vertical view-invariant primitives, three-mode `measure_proportion`, folder gate, Cy status writer), the hard gate in `approve_bible`, the read-only `bible check-proportion` verb, the per-character `character.yaml` specs (sean declared, mascot `sf03: opt_out`), and 43 tests — all red-then-green. Gate A: 354 → green.
2. **Phase B — the costed probe (9d95cf5).** Generated a heads-tall armature underlay + 4 turnaround views and ran the just-built measurement on them. **STOP → Checkpoint 1**, Sean chose Approach A.
3. **Phase C — Approach A (476d9e6).** Hardened the armature measure (the ¾ finding), promoted `build_armature_underlay`, added the `emit_gridded_model_sheet` feeder primitive + `armature_divisions` spec field.
4. **Phase D+E — retroactive + docs (da2eaa6).** Ran the gate on sean-anchor's locked turnarounds (the A4 loop), persisted verdicts, wrote the CHANGELOG / CLAUDE.md / field report.
5. **Phase F — merge.** **Checkpoint 2** (pre-merge diff review), then PR #33 squash-merged to `main`; worktree + branches torn down, bounded key removed.

## The probe — does NB2 honor an armature underlay?

| view | grid lines (in → out) | heads_tall | verdict | note |
|---|---|---|---|---|
| front | 8 → 8 | **7.12** | pass | crown on top line, feet on bottom line |
| profile-left | 8 → 8 | **7.15** | pass | view-invariant read holds |
| back | 8 → 8 | **7.05** | pass | tightest alignment (0.03) |
| ¾ | 8 → **9** | 8.29 → **~7.25** | fail → pass | NB2 redrew a 9th line; ruler-rescale, not a figure miss |

**Make-or-break answered YES.** The figures are production-quality pencil-test turnarounds, not just test rigs. The lone ¾ "failure" was NB2 redrawing the ladder with 9 lines instead of 8 — a *ruler* problem, fixed by anchoring the measure on the bold crown/feet lines + the **known division count** (7), never the detected line count. Plates: [`2026-06-08-sf03-probe-plates/`](2026-06-08-sf03-probe-plates/).

## What we learned

- **Approach A is PREVENTION, not retroactive AUDIT.** This is the session's load-bearing insight. NB2 fits the figure *to* the provided grid (full body at 7 heads from a head-only anchor), so re-gridding an existing clean plate would *restretch* it and **hide** drift. Sound Approach A = generate body turnarounds against the armature from the start (born 1:7; the gate confirms NB2 obeyed). It sharpens — and is fully consistent with — the design's constrain-first thesis.
- **Don't trust NB2's redrawn grid as the ruler.** The ¾ case proved the model preserves the bold crown/feet anchors but drifts the interior line count. Measuring against the *known* division count makes the read robust; the line-count drift is surfaced in the verdict detail, not silently dropped.
- **View-invariance is real** — the vertical heads-tall read was consistent across front/profile/back (7.05–7.15), exactly as the design predicted for a vertical armature.
- **The silent-pass hole is the dangerous one.** The original drift sailed through because nothing checked. The gate's anti-silent-pass guard (undeclared spec + body plates present = block; `opt_out` the only no-spec lock) is the structural fix, not the tolerance band itself.
- **Scaffold-first paid off.** Every line of the gate was verified green before any spend; the $0.20 probe then changed only one input artifact, never the contract. No wasted costed runs.

## Retroactive verification — the A4 loop close

Ran the built gate against the **already-locked** `characters/sean-anchor/turnarounds/body-*.png` (the 1:7 re-lock from `b7323e3`, where a human gate stood in for SF03). Persisted: [`2026-06-08-sf03-retroactive-sean-anchor.json`](2026-06-08-sf03-retroactive-sean-anchor.json).

| plate | verdict | method |
|---|---|---|
| body-front / back / profile-left / profile-right / 3quarter | **indeterminate** | extent_only |

**A surfaced finding, not a fix.** The gate blocks — it cannot SF03-certify the existing re-lock because those plates predate constrained generation (and per the finding above, can't be retro-audited). This is **not** evidence the plates are off-proportion — the human gate judged them 1:7; the automated gate simply can't *confirm* it retroactively. Certifying deterministically requires re-baking the five through the Approach-A feeder — its own decided work, surfaced for Sean, not done silently.

## Build metrics & cost

- **Code:** `proportion_gate.py` +565, `bible.py` +65 (hard gate + check-proportion), `character_designer.py` +10 (sf03 wiring), `__main__.py` +8 (dispatch), 2 `character.yaml` (+3).
- **Tests:** +46 — `test_proportion_gate.py` (36, synthetic cream/graphite PIL fixtures, no committed binaries), `test_cli_bible.py` (+9 gate/check-proportion), `test_character_designer.py` (+1 wiring). All credential-free. **358 contract + 10 seedance green.**
- **Spend:** 4 NB2 Flash generations, no retries, **~sub-$0.20**. No 429s, no timeouts, no stub fallback. No criteria/baseline/Em-surface touched (SF03 is generation-time, off Em's path).

## Hard guards (verified)

- Built scaffold-first: the full contract suite was green *before* the probe and *after* every phase (312 → 354 → 358).
- The hard gate sits **after** `approve_bible`'s already-locked early-return, so it guards **new** locks only and cannot retro-block an existing Bible (test: `test_bible_approve_already_locked_skips_gate`).
- `approve_bible` recomputes on **committed pixels**, never the ephemeral `runs/{run_id}/plate_verdicts.jsonl` — the committed plates are the exact thing being locked.
- Mascot opt-out verified clean (box-creature, never measured against a human armature); no hardcoded 1:7 anywhere.
- Fleet-ops clean: isolated worktree, `ANTHROPIC_API_KEY` absent, bounded `GEMINI_API_KEY` removed at teardown, no `start_new_session`, local `main` working tree never touched (merge via PR on the remote).

## What's open (no attached timeline — nothing auto-scheduled)

1. **Re-bake sean-anchor's five body turnarounds** through the Approach-A feeder (constrained generation, born 1:7) and re-lock, to convert the `indeterminate` retroactive read into a certified pass. Decided work for Sean.
2. **Cy hot-loop auto-wiring** — wire constrained body-turnaround generation into Cy's authoring loop so future heads-tall characters auto-produce the gridded verification artifact. Deferred: no current consumer (sean locked, mascot opt-out), and naive auto-regridding would be unsound. The primitives (`build_armature_underlay`, `emit_gridded_model_sheet`) + the probe are the reference implementation.

## Recommendation

SF03 is now an enforcing, deterministic, per-character gate — the deterministic SF03 the pipeline declared but never had. Approach A is validated as a **prevention** mechanism. The honest residual is documented and bounded: existing pre-constrained Bibles read `indeterminate` until re-baked constrained, and the gate is correct to refuse to certify what it cannot measure. The two open items above are the natural next decisions when a heads-tall character is next authored or when Sean wants the sean-anchor re-lock certified.
