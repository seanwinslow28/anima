# Em References Re-Test — Field Report

*2026-06-04. G6 sequence step 2 (instrumented mini-run ✅ → **references re-test** → G6.1 citation grounding). Run brief: [`docs/2026-06-04-em-references-retest-handoff.md`](../2026-06-04-em-references-retest-handoff.md). Result trace: [`evals/vision_critic/traces/references-retest-2026-06-04.md`](../../evals/vision_critic/traces/references-retest-2026-06-04.md). Control = the ratified G5 blind baseline ([`traces/baseline-2026-06-04-scored.md`](../../evals/vision_critic/traces/baseline-2026-06-04-scored.md)).*

**This was a diagnostic-with-teeth, not a flag flip.** The repo default `critics.t2.attach_references: false` did NOT change. The flip is a separate, Sean-gated decision against the §Decision-rules below.

---

## TL;DR

The 2026-06-02 reference-grounding regression **does not reproduce on the trustworthy corpus** — and that is the load-bearing result. On the clean fixtures, references-on **holds both safety axes**: `false_pass = 0.00` (= blind) and `recall = 1.00` (= blind). The old false-pass blow-out (0.00→0.15, recall 1.00→0.85) was a *contaminated-fixture artifact*, exactly as the contamination hypothesis predicted. **The fixture-borne diagnosis is confirmed.**

References do cost **precision** (0.97 → 0.85 on `performs`, 5 clean false-positives vs. 1 blind) — but the cost is **rule-scoping, not confabulation**: 4 of the 5 clean FPs fail because the attached criteria block surfaces `IR.sean.prop.stylus-right-hand-always` (the production stylus-continuity rule) onto clean character-consistency fixtures that simply don't depict a stylus. `cites_correct = yes` on those FPs — Em is *enforcing a real rule*, not hallucinating. The stylus rule is cited in **37 of 50 cases**: it is a "cite magnet."

References **fix citation grounding**: `cites-correct 0.03 → 0.73` on `performs`, and geometry **empty-cites invariant trips 3/250 → 0/250**.

**Recommendation: flag stays OFF** — fails the `precision ≥ 0.97` flip-gate. But this is NOT a "confirmed real regression, stop relitigating references" outcome. References make grounding work; the precision cost is mostly an eval-corpus / rule-scoping interaction that G6.1 (real view/anatomy IR rules) + a stylus-rule scoping fix should clear, after which a re-test is warranted. **Sean ratifies.** `clean-c06` stays red (ships-red; G6.1 view-rule acceptance case).

---

## Run config (identical to G5 except the one scoped flag)

| Knob | Value |
|---|---|
| Cases | 50 (16 clean + 28 identity_style + 6 motion_proper); two pending re-roll slots excluded |
| Replication | `--runs 5`, per-case **majority vote** (conservative tie-break fail > borderline > pass) |
| Model | `gemini-3.5-flash` pinned via `gemini_api` transport (served model read back from `resp.model_version` = `gemini-3.5-flash`, `stub_fallback=False`); Opus 4.7 escalation unchanged |
| References | **ON** — `critics.t2.attach_references: true` set **run-local in the worktree manifest only** (reverted before commit; repo default stays `false`). Bundle = `select_references` view-aware B1a path (anchor + deduped checkpoint-appropriate turnarounds, 4 plates/case) + the `IR.*/AC.*` criteria block. |
| Corpus / prompt / criteria / labels | Untouched from G5 |
| Result | **250/250 case-runs scored, 0 errored, 0× 429** on the API transport |
| Control | Ratified G5 blind baseline (not re-burned). Optional N=1 blind sanity **skipped** (the brief permits it; control already ratified, and it would have added ~50 calls to an already multi-hour run) |

Pre-flight: all 7 brief rows + the fleet-ops pre-costed checklist passed before the first costed call (remote divergence `0 0`; isolated worktree; guards green — 302 contract + vision-critic runner; ratified-trace SHA-256 tripwire recorded and re-verified **byte-identical at every checkpoint and at teardown**; `--stub` $0 proof; served-model + references-attach verified live in the smoke).

---

## Side-by-side vs. the blind G5 baseline

### `performs` segment (n=44 — the segment the decision rules live on)

| Metric | Blind G5 (control) | References-ON | Δ |
|---|---|---|---|
| **false_pass_rate** | **0.00** | **0.00** | **0.00** ✅ (gate metric HELD) |
| **recall** | **1.00** | **1.00** | **0.00** ✅ (FN=0, all 28 defects caught) |
| **precision** | **0.97** | **0.85** | **−0.12** ✗ (5 clean FP vs 1) |
| confusion (TP/FP/FN/TN) | 28 / 1 / 0 / 15 | 28 / 5 / 0 / 11 | +4 FP |
| cites-correct | 0.03 | **0.73** | **+0.70** ✅ |
| false-pass band (per-run) | 0.00–0.04 `[0,0,0,0,0.04]` | 0.00–0.04 `[0,0,0,0.04,0.04]` | same band, worst run 0.04 = bar |
| 3-way exact agreement | 0.91 | 0.80 | −0.11 |
| empty-cites invariant trips | 3 / 250 | **0 / 250** | ✅ eliminated |
| mean wall | 30.6s | 57.7s | +27s (refs + criteria + 5 images) |

### `motion_proper` (n=6, expected-red, segmented) and `overall` (n=50)

| Metric | Blind G5 | References-ON |
|---|---|---|
| motion: TP/FN, false_pass (majority) | 5 / 1, **0.17** (`motion-t2-arc` passed) | **6 / 0, 0.00** (all caught) |
| motion false-pass band | 0.17–0.33 `[.17,.17,.17,.17,.33]` | 0.00–0.17 `[0,.17,.17,0,0]` |
| overall precision / recall / false_pass | 0.97 / 0.97 / 0.03 | 0.87 / **1.00** / **0.00** |

References-on caught all six motion clips at majority (blind let `motion-t2-arc` through) — but via the **stylus magnet + spatial traces**, not motion-perception (Em still explicitly defers motion-proper in every motion reasoning). `cites-correct` on motion stays **0.00** (motion IR handles never match the expected `motion.*` axis). Treat the motion improvement as a side-effect of the stylus rule, not a motion-sight gain.

---

## The five priority reads

### 1. Safety axes vs. blind (the gate) — **HELD; no confabulation on defects**

`false_pass = 0.00` (= blind) and `recall = 1.00` (= blind), majority vote. Every one of the 28 single-axis defects was caught (FN=0). **The brief's central question — "does Em recite the reference register onto a defect subject?" — answers NO** on this corpus. There is no defect that references talked Em into passing. The 2026-06-02 false-pass regression (false_pass 0.00→0.15) **did not reproduce**. Combined with the eval-foundation reset's finding that 19/23 old "clean" fixtures were SHA-identical Bible plates, this **confirms the old regression was fixture-borne** — Em was reciting the reference register onto defects *because the defects' "clean" twins literally were the reference plates*. On independent fixtures, that trap is gone.

### 2. Precision / the clean set — **regressed 0.97→0.85, but as rule-enforcement**

5 clean false-positives (majority `fail`) vs. 1 blind. Per-clean verdicts (all 16):

| clean case | majority | why (from Em's cited reasoning) |
|---|---|---|
| c01 idle-front | **pass** (TN) ⚠flip | stylus on desk not in hand — Em passed it "in the spirit of the rule"; flipped to `fail` in run 4 |
| c02 explaining-3q | **fail** (FP) | stylus absent from gesturing right hand (+ off-register open-mouth expression) |
| c03 walk-profile-right | **fail** (FP) | stylus absent from swung-back right hand |
| c04 reach-3q-back | **pass** (TN) ⚠flip | stylus not held — Em passed: "reaching to retrieve the pencil"; flipped to `fail` in run 4 |
| c05 relaxed-back | **fail** (FP) | stylus absent from hanging right hand |
| c06 leaning-profile-left | **fail** (FP) | **HF03 wrong direction** (right profile vs declared left) + stylus absent — *also the blind FP* |
| c07–c12 portraits | pass ×6 (TN) | clean — portraits, no stylus expectation triggered |
| c13 computer-desk | **fail** (FP) | stylus absent (desk scene) |
| c14 drawing-desk-waistup | **pass** (TN) ⚠flip | borderline in run 5 |
| c15 glance-up-smile, c16 stool-sketching | pass (TN) | clean |

**4 of the 5 FPs (c02, c03, c05, c13) are pure stylus-continuity enforcement**; c06 is orientation (HF03) + stylus. `cites_correct = yes` on every FP — these are **real IR-rule citations, not confabulated namespaces**. The portraits (c07–c12) are unaffected because a head-and-shoulders shot doesn't trigger a stylus expectation; the failures cluster on full-body/desk fixtures where the absent stylus is conspicuous.

**On the brief's c06 question** ("references may FIX c06's orientation read — the 0.97→1.00 headroom — or spread doubt"): references did **not** fix c06 (still majority `fail`, now on orientation + stylus) and **spread doubt onto 4 more cleans**. This is the regression shape, not the fix shape — but the doubt is a real rule, conspicuously enforced, not a hallucinated register recitation.

### 3. Citations — **the strongest positive; references make grounding work**

`cites-correct 0.03 → 0.73` on `performs`. Giving Em the IR handles via the criteria block moved it from "never cites the right rule" to "cites the right rule 73% of the time." Class split (confirming the G6.2 mini-run diagnosis):

- **Fixed (now cite real IR handles):** proportion (`IR.sean.proportion.head-to-body-1-to-7` — was a namespace near-miss blind), palette, costume, construction-lines, shading — all `cites_correct = yes`.
- **Still missing (cites_correct = NO):** **view** and **anatomy** — because the *expected* cite (`view.declared-view-matches-drawn-view`, `anatomy.count-correct`) **is a placeholder handle that does not yet exist as a real IR rule in the Bible**. Em cites the closest real rules it can find (HF03, `IR.sean.view.front-facing-when-declared`, proportion rules) but cannot hit a handle that isn't authored. **This is precisely the G6.1 gap.**
- **Noise source:** the stylus rule is a **cite magnet (37/50 cases)** — Em cites it whenever a stylus is absent, even on defects whose actual axis is something else (e.g., `anatomy-ad1-six-fingers` cites the stylus rule, not `anatomy.count`). This pulls citations off the true defect axis and is part of why view/anatomy cites_correct stays low.

### 4. Variance — **safety band unchanged; clean-set verdict flips appear**

`performs` false-pass band is **0.00–0.04** (worst run 0.04 = the bar), *identical band to blind* — the safety number did not widen. But verdict **flips** rose: 4 clean cases flip across runs (c01, c04, c06, c14), all on the stylus judgment call (Em alternates between strict enforcement and "spirit of the rule" passes). 3-way exact agreement dropped 0.91→0.80. The clean-set instability is real and is the same stylus-rule ambiguity surfacing as run-to-run inconsistency — the reason the N=5 majority (not N=1) is the honest read.

### 5. Geometry classes — **all caught; proportion grounding fixed, view/anatomy gap exposed**

All geometry defects caught at majority (proportion pd1–3 `fail`, pb2 `borderline`; view vd1–4 `fail`/`borderline`; anatomy ad1–4 `fail`/`borderline`) — recall intact. References **fixed proportion citation** (real `IR.sean.proportion.*` handle) and **eliminated the empty-cites invariant trips** (3/250 blind → 0/250) because the criteria block always gives Em *some* handle to ground a block. The residual view/anatomy cites_correct misses are the missing-IR-rule gap, not a detection failure — Layer-ownership already assigns geometry to the Bible-lock in production; this run is informational for SF03/G6.1.

---

## Decision against the brief's rules (proposed to Sean, not self-executing)

| Rule | Condition | This run | Met? |
|---|---|---|---|
| **Flip-eligible** | false_pass=0.00 AND recall=1.00 AND precision≥0.97 AND worst-run band ≤0.04 | 0.00 ✓ / 1.00 ✓ / **0.85 ✗** / 0.04 ✓ | **NO** |
| **Wash** (same numbers, no c06 fix) | point estimates unchanged | precision −0.12, cites +0.70 — materially changed | No |
| **False-pass regression** (→ confirmed real) | false_pass regressed | false_pass **held 0.00** | **No** |

The outcome fits none of the three pre-written buckets cleanly, because it is a **better** result than any of them anticipated: **safety holds, citation grounding improves sharply, and the only regression (precision) is diagnosed as an eval-corpus / rule-scoping interaction rather than confabulation.**

**Recommendation:**
1. **Keep `attach_references: false`** — it fails the `precision ≥ 0.97` flip-gate. (Done — the flag was reverted; this run never changed the repo default.)
2. **Record the references question as re-openable, not closed.** Unlike 2026-06-02, do *not* treat this as a confirmed-real regression that ends references work. The safety regression was fixture-borne (now proven false on clean fixtures); references demonstrably fix grounding.
3. **The precision cost is mostly fixable.** It is the criteria block importing a *production continuity rule* (stylus-always) into a *character-consistency eval* whose clean fixtures were never built to carry the stylus. Three non-exclusive fixes for a future re-test: (a) scope which IR rules are in-play per eval case (continuity-prop rules don't belong in a single-frame consistency check), (b) depict the stylus in clean fixtures, or (c) exclude continuity-prop rules from the per-frame T2 criteria block in production. After G6.1 authors the real view/anatomy IR rules **and** the stylus-rule scoping is resolved, re-run this exact comparison.
4. **`clean-c06` stays red** (ships-red; G6.1 view-rule acceptance case). No relabel.

## Hard lines honored

No baseline moved (ratified traces byte-identical at teardown). No label / prompt / criterion edits. No default-flag flip committed (the scoped `true` was reverted; `git diff manifest.yaml` is empty on the landed branch). Nothing tuned to flatter Em in either arm. Ships-red discipline intact.
