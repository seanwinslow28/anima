# Field report — Em instrumented mini-run (G6.2)

*2026-06-04. First costed move of the G6 arc, run under [`docs/fleet-ops-protocol.md`](../architecture/fleet-ops-protocol.md). Single-pass diagnostic (`--runs 1`, 50 cases), config held identical to the ratified G5 baseline so the verdicts are comparable. This run moved no baseline, changed no labels, no prompt, no criteria. Trace: [`evals/vision_critic/traces/2026-06-04-instrumented-mini-run.md`](../../evals/vision_critic/traces/2026-06-04-instrumented-mini-run.md).*

**Standing doctrine: verify against the tree, never trust a label — including this report.**

## What ran

- `python -m evals.vision_critic.score --runs 1 --segment all --trace-name 2026-06-04-instrumented-mini-run`
- Config: reference-blind (`critics.t2.attach_references: false`), `gemini-3.5-flash` pinned by ID via the `gemini_api` transport, Opus 4.7 SDK escalation on `hero`/`identity_critical` below conf 0.7, served model read back from `resp.model_version`.
- 50 cases, subprocess-per-case isolation, **0 errored**, **0 invariant trips** (see §Geometry).
- Instrumentation added this run: per-case `reasoning` + `actual_cites` + `cites_correct` persisted into the trace; a typed `EmptyCitesInvariant(ValueError)` so a tripped geometry case is *captured with its reasoning* (Option B) instead of dying as a blind gap. Production gate unchanged — the invariant still raises.

## Headline (reproduces G5 on the performs segment)

| Segment | n | precision | recall | false_pass | cites-correct | exact-agree |
|---|---|---|---|---|---|---|
| **Performs** (identity/style + clean) | 44 | **0.97** | **1.00** | **0.00** | **0.03** | 0.91 |
| Motion-proper (expected-red) | 6 | 1.00 | 0.83 | 0.17 | 0.00 | 0.00 |
| Overall | 50 | 0.97 | 0.97 | 0.03 | 0.03 | 0.80 |

A single N=1 pass landed the ratified G5 N=5 numbers on the performs segment (0.97 / 1.00 / 0.00): all 28 single-axis defects caught (FN=0), one clean false-positive (`clean-c06`), cites-correct floored at 0.03. The verdict layer is solid; **the diagnostic's job was the cites/reasoning layer, and that is now fully read.**

Motion (5/6 flagged) behaves exactly as G5: `motion-t2-arc` is the lone slip (pass@0.95), and Em's own reasoning explains why — the contact sheet can't see motion-proper, and the t2 strip has no spatial discontinuity for her to flag as a proxy. Not new; carried.

---

## Q1 — style cites (palette / construction / shading): what does Em actually cite?

**Answer: she reasons correctly and reaches for plausible grounding, but almost never cites the exact `IR.sean.*` handle the scorer expects.** The only `cites_correct = yes` in the whole run is `clean-c06` — and that is a scoring quirk (a flagged case with empty `expected_cites` scores `True` on any non-empty cite), not a grounded defect cite. **Every actual defect with a specific expected IR handle scored NO.** cites-correct = 1/29 flagged ≈ 0.03.

Verified against the tree: the locked Bible's namespace is **`IR.sean.*`** ([`characters/sean-anchor/acceptance_criteria.json`](../../characters/sean-anchor/acceptance_criteria.json), 22 rules), and the eval's `expected_cites` correctly reference real handles (e.g. `IR.sean.proportion.head-to-body-1-to-7`, `IR.sean.style.construction-lines-visible-beneath-final` both exist). The scorer ([`scoring.py::cites_correctness`](../../evals/vision_critic/scoring.py)) does **exact list-membership** (`c in actual_cites`). So a cite fails the match unless it is byte-identical.

### Per-class cite classification (handoff taxonomy: a=correct · b=real-but-wrong · c=invented · d=formatting near-miss)

| Class | Expected cite (exists?) | What Em actually cited | Class verdict |
|---|---|---|---|
| **proportion** (pd1/2/3, pb2) | `IR.sean.proportion.head-to-body-1-to-7` ✅ exists | `SF03` (+SF01/SF02), and confabulated `IR.sean-anchor.proportion.head_to_body` / `…head-to-body-1-7` | **d + b** — leaf usually right, *namespace+format* wrong (`sean-anchor` not `sean`; `1-7`/`head_to_body` not `1-to-7`) → **matcher-recoverable** |
| **view** (vd1-4, vb1) | `view.declared-view-matches-drawn-view` ❌ no IR rule | `HF03` + confabulated `IR.sean-anchor.view.{three-quarter\|front-symmetry\|profile-left-orientation\|back-facing}`, `AC.view-correctness` | **c + b** — no IR rule exists to cite; HF03 (wrong-direction) is semantically correct |
| **anatomy** (ad1-4) | `anatomy.count-correct` ❌ no IR rule | confabulated `IR.sean-anchor.anatomy.{finger-count\|hand-finger-count\|limb-count\|leg-count}` + `SF02`/`HF04`/`SF03` | **c + b** — no IR rule exists; her `anatomy.{part}-count` shape is the template for G6.1 |
| **palette** (pad1/2/3/5/6) | `IR.sean.palette.full-color-…` / `IR.sean.costume.navy-tee-cool-gray-jeans` / `IR.sean.hair.dirty-blonde-color` ✅ exist | confabulated `IR.sean-anchor.palette.{hair\|skin\|shirt}`, `…identity.facial_hair` + SF01/SF02/SF05 | **c** — right *target* (hair/shirt color), wrong handle granularity + namespace (`palette.shirt` doesn't exist; real is `costume.navy-tee-cool-gray-jeans`) |
| **construction** (cld1-4, clb1) | `IR.sean.style.construction-lines-visible-beneath-final` ✅ exists | `HF05` + `SF01` (or `AC01`+`SF01`) — **never the IR handle** | **b** — pure reason-code substitution |
| **shading** (shd1-4, shb1) | `IR.sean.style.cross-hatching-shadow-areas` ✅ exists | `HF05`/`AC01` + `SF01` — **never the IR handle** | **b** — pure reason-code substitution |

**The 0.03 is half scoring-artifact, half real grounding gap, and it splits by class:**
- **Matcher-recoverable (d):** proportion is the clearest — Em names the right leaf (`head-to-body`) but prefixes the folder id `sean-anchor` and mangles the format. A namespace-insensitive, leaf-normalized matcher would recover pd2/pd3/pb2 *today* with no change to Em. **This is the single highest-leverage fix and belongs in the G6.1 split verdict/citation scoring work.**
- **Real vocabulary gap (b):** construction + shading — Em defaults to the manifest QA reason-codes (`HF05` wrong-aesthetic, `SF01` style-drift) and **never** reaches for the `IR.sean.style.*` handle, even though it exists in her merged criteria. Making her cite IR handles is a prompt/surfacing problem (the IR style rules are present but not salient against the HF/SF vocabulary she defaults to). This is the citation-grounding change.
- **No rule to cite (c):** view + anatomy have **no IR rule in the Bible at all** (the 22 rules are prop/hair/face/proportion/palette/costume/style/motion — zero view, zero anatomy). Em invents structured `IR.sean-anchor.view.*` / `…anatomy.*-count` handles. → **Q3.**

---

## Q2 — clean-c06 (the lone false-positive): relabel / fix prompt / known disagreement?

**Recommendation: keep as a known disagreement (view/facing-convention seam). Do NOT relabel; do NOT tune away.**

Em flagged `clean-c06` **borderline** (conf 0.95), citing `AC01, HF03`. Her reasoning, verbatim:

> "there is a clear orientation mismatch against the beat description: Sean is leaning against the desk facing screen-right instead of screen-left. While the shot is high-fidelity and on-model, the direction flip breaks storyboard continuity."

The case's ratification note records exactly this seam: *"Declared view RELABELED right→left profile under the facing convention (image faces left; prompt text said right)."* The image is ratified clean (faces left); the beat now says "left profile (facing screen-left)." Em reads the figure as facing **screen-right** and flags the beat↔image mismatch.

So this is **not** a register or identity complaint — it is a left/right **facing perception** call colliding with the screen-left vs character's-left convention. It is the same axis (view-correctness) that has no deterministic backstop yet. Two notes:
- It is **borderline, not fail**, and grounded in a coherent orientation rationale — Em is not hallucinating a defect, she is applying a strict beat-vs-image facing check on the one axis she's weakest at.
- The cost is exactly one FP → precision 0.97 with recall 1.00 / false_pass 0.00. Acceptable.

**Action:** leave the label (ships-red discipline — the image doesn't violate a ratified rule). Treat as the canonical test case for the **G6.1 view-correctness IR rule** (a deterministic declared-view/facing check would resolve it the right way), and flag the beat-description facing convention ("screen-left" vs "left profile") as a candidate prompt clarification — but only as part of the view IR work, not as a one-off tweak to flatter the metric.

---

## Q3 — geometry cites: Em's natural vocabulary (direct input to G6.1)

**0 invariant trips this run** — at N=1 Em cited *something* on every flagged geometry case (the trip is variance-driven; G5's 3 trips were specific runs out of 5). So instead of empty-cites gaps, we have her full geometry vocabulary on the record. The Option B capture path is built and unit-tested; it simply wasn't needed this pass. Her natural handle shapes:

| Geometry class | Em's natural cite vocabulary (verbatim from the run) |
|---|---|
| **proportion** | `IR.sean-anchor.proportion.head-to-body-1-7`, `…head_to_body`, `…head-to-body` + `SF03` |
| **view** | `IR.sean-anchor.view.three-quarter`, `…front-symmetry`, `…profile-left-orientation`, `…back-facing` + `HF03` |
| **anatomy** | `IR.sean-anchor.anatomy.finger-count`, `…hand-finger-count`, `…limb-count`, `…leg-count` + `SF02`/`HF04` |

**G6.1 authoring guidance, grounded in what she already reaches for:**
1. Author the real handle as **`IR.sean.proportion.head-to-body-1-to-7`** already exists — the gap is purely that Em writes `IR.sean-anchor.…-1-7`. Either (a) normalize the matcher, and/or (b) surface the exact handle string in her criteria block so she copies it. Lowest-effort, highest-yield.
2. Author **view** IR rules in her vocabulary: per-view handles (`IR.sean.view.three-quarter-both-eyes-visible`, `…profile-far-eye-occluded`, `…back-no-face`) plus a declared-view↔drawn-view check. She already distinguishes the views correctly in prose; give her the handle.
3. Author **anatomy** IR rules as `IR.sean.anatomy.{finger|hand|limb|leg}-count` — she already cites exactly this shape.
4. Note Em reflexively pairs every geometry defect with the right **manifest QA code** (SF03 proportion, HF03 direction, HF04 pose, SF02 identity). The split verdict/citation scoring should treat a correct reason-code as partial grounding, not zero — that alone would lift cites-correct off the floor without changing Em.

---

## Caveats (read before quoting these numbers)

- **N=1, not the N=5 baseline.** This is a diagnostic. The ratified baseline ([2026-06-04 G5 field report](2026-06-04-em-rebaseline-g5-field-report.md)) is unchanged and unmoved; its trace `traces/baseline-2026-06-04-scored.md` and `last-run.md` were verified byte-identical before and after this run (sha `2138ccd…`).
- **0 invariant trips this run** means the matrix counts no geometry case as a captured trip — so the Option-B "tripped cases count as detections" non-comparability (the planned F12 caveat) **did not arise**: the matrix here is directly G5-comparable.
- **Opus verdict variance is visible**: `clean-c01` returned pass@0.78 / borderline@0.68 / pass@0.82 across the three live touches this session — the same run-to-run wobble G5 diagnosed. A single pass is a snapshot, not a distribution.
- `cites_correct = yes` on `clean-c06` is a scorer quirk (flagged + empty expected_cites), not a grounded cite.

## Bottom line for the G6 sequence

- **cites-correct=0.03 is now de-confounded.** It is *not* mystery mis-citing: it is (1) a namespace+format matcher gap on proportion (recoverable), (2) reason-code substitution on construction/shading (prompt-surfacing), and (3) genuinely missing IR rules for view/anatomy (authoring). All three are addressed by **G6.1 (geometry IR criteria + split verdict/citation scoring)** — and this run hands G6.1 the exact handle vocabulary to author against.
- **clean-c06** is the canonical view-correctness test case for G6.1; keep it red-as-disagreement.
- The verdict layer needs nothing here. The citation layer is the work, and it is now fully specified.
