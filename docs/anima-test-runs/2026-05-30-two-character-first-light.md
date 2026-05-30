# Two-character first light — Sean + claude-mascot

*2026-05-30. The first time anima loaded two real Character Bibles into one scene. This is an exploratory probe from the claude-mascot pencil-register pivot session (Phase 5): exercise the two-character path, see what it produces, and scope what a real cross-character continuity system needs — explicitly **without building that system here.***

---

## What was exercised

1. **Criteria merge.** `load_all_criteria(manifest)` over the manifest's `criteria_sources.bibles` (sean-anchor + claude-mascot) returned a single `CriteriaBundle` with **36 entries — 22 `IR.sean.*` + 14 `IR.claude-mascot.*` — and zero ID collisions.** Per-character `IR.{character_id}.*` namespacing did its job: the two rule graphs coexist in one bundle cleanly, and `CriteriaBundle.for_character(id)` can slice either set. This is the load-bearing precondition for any two-character verdict pass, and it holds.

2. **One two-character frame, generated through the editing-template storyboard variant** (Amendment C). Image 1 = `characters/sean-anchor/anchor.png`, Image 2 = `characters/claude-mascot/anchor.png`, Image 3 = the A-7 pairing (`source-refs/sean-with-claude-mascot.png`) for scale/placement. `{identity_lock}` enumerated both characters; `{variation}` carried one action (Sean glances up at the mascot, stylus in right hand); `{shot}` = medium / eye-level / over-the-shoulder; register held constant. Generated on NB2. Output: `runs/2026-05-30-two-character-first-light/sean-mascot-frame.png` (committed as evidence).

## What the frame showed (continuity vs A-7)

A-7 is the canonical pairing — mascot perched on Sean's shoulder. The first-light frame held against it on every axis Sean checked:

- **Sean identity** — recognizable: hair, beard, blue eyes, dark tee, **stylus in his right hand** (the Act-1 continuity invariant), sketchbook under the other arm.
- **Mascot identity** — the terracotta rounded-box creature, two dot eyes + brows, near ear/arm nub reading, **no hair** (the invariant added this session held), perched leaning toward Sean's head. Not a new creature, not a humanoid.
- **Relative scale** — the box reads ≈ one adult-head tall on the shoulder, matching `IR.claude-mascot.proportion.shoulder-companion-scale` and A-7.
- **Shared register** — one consistent pencil-test-colored medium across both figures (warm cream paper, graphite line, cross-hatch, hole-punch marks). No two-style clash — the whole reason the mascot was re-authored into Sean's register.

Minor, expected: the mascot's four stub legs are occluded behind the shoulder (fine for a perch), and only the near nub reads (correct for the angle).

**Verdict:** the two-Bible path works end to end for a single frame, and continuity holds against the ground-truth pairing. Good enough to feed Act 2 two-shots, with the gaps below scoped for a dedicated session.

## The gap — what a real cross-character continuity check needs (future session, NOT built here)

`pipeline/continuity_audit.py`'s CC01–CC08 checks are hardcoded to Sean / Act-1 (stylus-in-right-hand, hair shape, single-character facing/scale). There is **no generalized cross-character continuity audit.** A real one needs, at minimum:

1. **Per-character IR loading into one verdict pass.** A frame asserting two characters should be scored against *both* `IR.sean.*` and `IR.claude-mascot.*` in the same critique, with each finding attributed to the character it concerns. The merged `CriteriaBundle` (proven above) + `for_character()` is the substrate; the missing piece is a critic prompt/runner that grounds a two-subject verdict in two rule sets at once.
2. **A relative-scale rule.** Today scale is per-character (`shoulder-companion-scale` grounds on A-7 alone). A two-character audit needs an explicit *ratio* invariant — "mascot box height ≈ Sean's head height when perched" — checkable between the two subjects in-frame, not just against each character's own anchor.
3. **Occlusion / who-occludes-whom.** The perch means the mascot occludes part of Sean's shoulder and its own legs. A continuity check needs to know that's expected (and conversely flag wrong-depth ordering — mascot behind the shoulder, Sean's arm through the mascot, etc.). No depth/occlusion vocabulary exists today.
4. **A shared-register consistency check.** The single most important cross-character invariant for this pair: both must render in the *same* style register. A check that the register held across both subjects (not one pencil-test + one drifted) belongs in the audit — it's the failure the whole re-author was meant to prevent.
5. **Placement invariants from the pairing reference.** A-7 fixes "mascot on the shoulder, not floating beside / not on the ground." `IR.claude-mascot.pose.shoulder-perch-canonical-pairing` states this prose-side; a cross-character audit should be able to cite it against an actual two-shot.

These are inputs to a future dedicated multi-character-continuity session. This session deliberately stopped at scoping.

## Pointers

- Frame: `runs/2026-05-30-two-character-first-light/sean-mascot-frame.png`
- Ground truth: `characters/claude-mascot/source-refs/sean-with-claude-mascot.png` (A-7)
- Bibles: `characters/sean-anchor/`, `characters/claude-mascot/` (pencil-test-colored, locked)
- Merge substrate: `pipeline/criteria.py` `load_all_criteria` / `CriteriaBundle.for_character`
- Single-character audit (the thing that needs generalizing): `pipeline/continuity_audit.py` CC01–CC08
