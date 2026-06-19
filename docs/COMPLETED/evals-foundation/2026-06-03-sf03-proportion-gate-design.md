# SF03 Proportion Gate — Design (generation-time construction-guide check at Bible-lock)

*2026-06-03. **Design spike only — NOT a build.** A decision artifact for Sean's review before any code is written. It proposes a change to Cy's generation contract; that should be seen and approved first. Produced after the Workstream B DINOv2 NO-GO and the dependency-free proportion-measure NO-GO (both this session).*

---

## Why — the problem, and why "recover proportion from the output" is the wrong frame

**SF03 (proportion drift) is a QA gate anima has declared but never automated.** This session proved why that gap bites: `sean-anchor`'s body turnarounds are baked into the **locked** Bible at ~1:4–1:5.3 heads-tall against a **1:7** target, and nothing caught it. The only proportion-adjacent signal — Cy's Pass-2.5 similarity gate — is **record-only** and measures *identity recognizability*, not *geometry*. The drift sailed through the lock.

Two attempts this session to **recover** proportion from finished art both failed, for the same root reason:

- **DINOv2 embedding similarity (B1b): NO-GO.** Proportion-drifted plates score 0.82–0.89 vs the anchor — still embedding-recognizably Sean. Cosine similarity captures identity/style, *not* head-to-body geometry.
- **Dependency-free silhouette landmark detection (proportion-measure spike): NO-GO.** Locating the *chin* across arbitrary multi-view stylized line art is fragile; the detection noise (±~20% on head height) is as large as the signal it must resolve (4.6 vs 5.5 heads). Back views have no face; profile/¾ confound the neck-narrowing.

The common failure is the **inverse problem**: reconstruct crown/chin/feet landmarks from arbitrary finished art. It is fundamentally fragile on this register. So we stop trying to solve it.

## The pivot — constrain-first (the animatic analog)

> Don't reverse-engineer proportion from the output. **Constrain** it at generation against a known armature, then **verify** the render against the armature you already know.

This is the proportion analog of the **animatic**: constrain timing in simple shapes *first*, then verify motion against that constraint — instead of trying to recover the intended timing from finished frames after the fact. Same move, applied to figure proportion.

## Scope — where the gate lives (and where it does NOT)

**Cy Pass-3 / Bible-lock.** Per-character, tiny volume — a handful of body turnarounds, once per character.

- **Why here, not per-frame T2/Em:** proportion errors **originate at Bible authoring** — that is precisely where the 4.6–5.5-head drift baked into a locked Bible undetected. Once the Bible's turnarounds are clean 1:7, downstream frames inherit correct proportion *because they are generated against the Bible*. The gate that actually pays off lives at the source, where the volume is tiny and a guide-check is entirely affordable.
- **Not on Em's path.** This is a standalone deterministic **SF03 gate**, independent of Em, references, and DINOv2. It does not touch the (still-off) `attach_references` question.

## The core idea — measure VERTICALLY against a view-invariant armature

Head-to-body ratio is a **vertical** measurement (crown→feet ÷ crown→chin) and it is **view-invariant**: a figure is 7 heads tall from front, profile, back, or ¾. The free-detection spike failed partly because it used **view-dependent horizontal width profiles**. A **vertical armature grid is view-independent** — the same ladder validates every turnaround. That is the unlock.

Cy generates each body turnaround against a declared **N-division proportion armature** (the heads-tall ladder: horizontal guide lines at crown=0, chin=1, …, feet=7), with the figure aligned crown→line 0, feet→line N, head filling band 0–1. Verification becomes a **grid-alignment check, not absolute landmark detection**:

1. Detect the **printed armature lines** — clean straight horizontals at known fractions of canvas height. Easy and robust.
2. Detect the **figure's vertical extent** (crown = top of the ink mask, feet = bottom). The spike confirmed this is *reliable* (total-height read was stable ~1024px across plates; only the *chin* was unreliable).
3. Verify the figure **spans the full armature** and the head silhouette's **chin lands at the first division** (±tolerance). Measuring relative to a *printed grid* is tractable where absolute chin detection was not.

## Two implementation approaches (probe A first; B is the guaranteed-feasible fallback)

**Approach A — armature-constrained generation + automated grid-alignment check.** Cy emits a construction-armature **model-sheet** artifact per body turnaround (gridded), alongside the clean Bible plate; the gridded sheet is the verification artifact. The gate auto-measures grid alignment. Fully automated and scalable.
- **Make-or-break risk:** does NB2 (image-edit) actually *honor* a provided armature underlay — align crown/feet to the grid and seat the head in band 0–1? Image models aren't pixel-precise. **This is the one feasibility question that decides everything**, and it's a cheap generation probe (a handful of plates).

**Approach B — lock-time assisted measurement (the affordable human-in-the-loop fallback).** Because the volume at Bible-lock is *tiny* (a few plates, once per character), a guided one-time measurement is entirely affordable: at lock, the authoring step captures crown/chin/feet (a human click, or a guided semi-auto pass) → computes heads-tall → stores it as the **locked proportion spec**, enforced deterministically thereafter. No fragile detection-from-scratch. Slower to author, but guaranteed to work and exactly scoped to the tiny lock-time volume Sean identified.

## Verdict, enforcement, and integration

- **Hard gate at lock** (unlike the record-only similarity gate): a body turnaround measuring outside, say, **[6.5, 7.5] heads** *blocks* the Bible-lock with a proportion verdict. This is the deterministic SF03 the pipeline has been missing.
- **Makes an existing criterion measurable:** `IR.{char}.proportion.head-to-body-1-to-7` is prose today; this gate makes it *checkable* — wires a measured `heads_tall` + per-division alignment into the plate verdict, persisted beside `plate_verdicts.jsonl`.
- **Closes the A4 loop:** this gate is *what `sean-anchor`'s body plates get re-baked against and re-locked through* — turning the A4 re-bake from "redo and hope" into "redo until the gate passes."
- **Mascot caveat:** `claude-mascot` is a box-creature, not "heads tall." The human-figure armature does not transfer; non-human characters need their own declared proportion spec (or opt out of SF03). The gate must be **per-character spec-driven**, not a hardcoded 1:7.

## Open questions for the design review

1. **A's feasibility:** does NB2 honor an armature underlay? (The gating probe.)
2. **Gridded artifact vs. gridded-final:** two artifacts (clean plate + model sheet), or lean on the existing `construction-lines-visible-beneath-final` IR rule as the in-image guide?
3. **Detection robustness:** how reliably can the gate read printed armature lines + chin-at-division on a *gridded* render? (A small measurement spike on one gridded test render.)
4. **View-invariance in practice:** confirm the vertical armature reads consistently across front/profile/back/¾.
5. **Tolerance band + spec schema:** what `heads_tall` window blocks a lock, and how is the per-character target declared (manifest? `character.yaml`? `acceptance_criteria`)?

## What this is NOT (this round)

Not a build. Not a per-frame Em/T2 check. Not references or DINOv2. **Design only** — the generation-contract change goes in front of Sean before any code.

## Recommended next step (if the design is approved)

A small **generation probe of Approach A**: does NB2 align a figure to a provided armature underlay? That single make-or-break question gates the whole build. It is compute-light — the only costed part is a handful of NB2 plate generations; the measurement is $0 API. If A's probe fails, fall back to Approach B (guaranteed feasible at the tiny lock-time volume).
