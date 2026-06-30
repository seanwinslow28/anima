# Claude-mascot — eval fixture corpus spec + prompts (v1, minimal grammar)

*2026-06-22. The class-isolated fixture corpus for **Tier-2 Slice 1** (the Em-calibration measurement foundation, [`docs/active/2026-06-22-tier2-mascot-corpus-design.md`](../../docs/active/2026-06-22-tier2-mascot-corpus-design.md)). Mirrors the proven sean-anchor corpus ([`sean-anchor-fixture-corpus.md`](sean-anchor-fixture-corpus.md)) — same six single-axis classes, same minimal grammar — adapted to the box-creature. This supersedes the old ~15-fixture sketch in the sean spec's "Mascot" stub: Sean's call is a **full mirror** (~46 fixtures), for a real baseline comparable to the sean one.*

*The grammar is the sean spec's hard-won v2 lesson, restated: **the references carry identity; the text carries only the beat + one corruption.** No identity descriptions, no keep-lists, no "turnaround / model sheet / views" — that pushes NB2 into sheet mode.*

---

## How to run every prompt

- **Attach two references:** `characters/claude-mascot/anchor.png` (the ¾ hero portrait) + `characters/claude-mascot/source-refs/turnaround-c1.png` (the 5-view sheet). Same two on every prompt — the mascot has no separate head, so there's no portrait/body split.
- **Copy the prompt verbatim.** Each is complete — no filling in.
- **Save outputs at 1K, uniform JPEG** (match the sean corpus: 1376×768, JPEG — uniformity over format; don't mix), one file per fixture, named by its ID.
- **Never** add identity descriptions, keep-lists, or the words *turnaround / model sheet / views / reference sheet* to a fixture prompt.
- The mascot is the **only** character in every fixture — no Sean, no shoulder. Isolation keeps each defect single-axis. Place it perched on a plain surface / ledge / sheet of paper, never on a figure.
- Framing knobs you can vary freely: `full box visible · close on the face` / `front view · three-quarter view · left side · right side · from behind` / `box centered · box on the left third · box on the right third`.

**The style line (verbatim, every prompt):**
> Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**The one structural rule:** when a defect corrupts something the style line itself asserts (cross-hatch → shading defects; the terracotta body → palette defects), that phrase is removed from the style line in that prompt. Already done below where needed.

**The identity the references carry (do NOT type — for your eye when ratifying):** a single fused rounded-box body ~1:1.2 (w:h, slightly taller than wide), generously radiused corners — never a sharp cube, never a sphere, never a biped; **four stub legs** close together beneath the footprint; **two ear/arm nubs** on the left and right faces at mid-height; two dot eyes + two short brow strokes on the upper-front face; terracotta body, warm-graphite line, cream paper; reads about one adult-human-head tall.

---

## Corpus at a glance

| Class | Owner | Clean | Defect | of which borderline | Author |
|---|---|---|---|---|---|
| box-proportion | Bible-lock | ← pool | 5 | 2 | gen + draw |
| view-correctness | Bible-lock | ← pool | 5 | 1 | gen (label-side) |
| anatomy-count (nubs/legs) | Bible-lock | ← pool | 6 | 0 | gen |
| palette | Em / T2 | ← pool | 5 | 0 | gen |
| construction-lines | Em / T2 | ← pool | 4 | 1 | gen + draw |
| shading-register | Em / T2 | ← pool | 5 | 1 | gen + draw |
| **shared clean pool** | (negative for all) | **16** | — | — | gen |

**Totals: 46 mascot fixtures** (16 clean + 30 single-axis). Anatomy-count is weighted to 6 on purpose — the 4-leg / ear-nub count is the exact Em detection blind spot the 06-18 + 06-21 runs surfaced.

---

## A. Shared clean pool (16)

*The box-creature alone, perched/sitting, production-keyframe style — never sheet-style. View + expression variety so every defect has a clean pair.*

**C01** — Have the box-creature character from the attached reference images sitting idle on a plain surface, full box visible, front view, box centered. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C02** — Have the box-creature character from the attached reference images perched on a plain surface looking curious, full box visible, three-quarter view. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C03** — Have the box-creature character from the attached reference images sitting on a plain surface, full box visible, left side view. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C04** — Have the box-creature character from the attached reference images sitting on a plain surface, full box visible, three-quarter back angle. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C05** — Have the box-creature character from the attached reference images sitting on a plain surface, full box visible, seen from directly behind. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C06** — Have the box-creature character from the attached reference images sitting content on a plain surface, full box visible, right side view. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C07** — Have the box-creature character from the attached reference images in a close view of its face, front view, neutral relaxed expression. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C08** — Have the box-creature character from the attached reference images in a close view of its face, three-quarter view, warm delighted expression with the eyes arched into happy crescents. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C09** — Have the box-creature character from the attached reference images in a close view of its face, front view, alert with the two brow strokes raised. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C10** — Have the box-creature character from the attached reference images in a close view of its face, three-quarter view, sleepy and content with the eyes nearly closed. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C11** — Have the box-creature character from the attached reference images perked up alert on a plain surface, full box visible, front view. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C12** — Have the box-creature character from the attached reference images on a plain surface tilting to look upward, full box visible, three-quarter view. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C13** — Have the box-creature character from the attached reference images perched on the edge of a plain ledge, full box visible, three-quarter view. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C14** — Have the box-creature character from the attached reference images sitting on a plain surface in private delight, full box visible, front view. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C15** — Have the box-creature character from the attached reference images sitting on a loose sheet of drawing paper, full box visible, three-quarter view. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**C16** — Have the box-creature character from the attached reference images sitting on a plain surface seen from a low three-quarter angle, full box visible. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

---

## B. Box-proportion defects (3 gen + 2 hand-drawn) — the ~1:1.2 w:h is the axis

**P-D1** *(pair C01)* — Have the box-creature character from the attached reference images sitting idle, front view, full box visible, but the box body is drawn too flat and wide — wider than it is tall, about 1.4 wide to 1 tall. Change only the box proportion. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**P-D2** *(pair C01)* — Have the box-creature character from the attached reference images sitting idle, front view, full box visible, but the box body is drawn too tall and narrow, a stretched column about 1 wide to 2 tall. Change only the box proportion. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**P-D3** *(pair C02)* — Have the box-creature character from the attached reference images perched looking curious, three-quarter view, but its body is drawn as a near-perfect round ball with no box silhouette at all. Change only the silhouette. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**P-B1** *(pair C01 — HAND-DRAW if NB2 won't land it)* — sitting idle, front, full box at **~1:1.4 w:h** (just slightly too tall — deliberately ambiguous, just off target).
**P-B2** *(pair C01 — HAND-DRAW)* — sitting idle, front, full box at **~1:1.05 w:h** (just slightly too square — deliberately ambiguous, just off target).

---

## C. View-correctness defects (4 gen + 1) — the defect is in the LABEL, not the prompt

*Clean prompts of the "wrong" view. The corruption happens in `cases.yaml`: the case **declares** one view while the image draws another. Generate fresh files (one file = one label) — don't reuse clean-pool images.*

**V-D1** *(case declares: front, full box)* — Have the box-creature character from the attached reference images sitting on a plain surface, **left side view**, full box visible. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**V-D2** *(case declares: three-quarter, full box)* — Have the box-creature character from the attached reference images sitting on a plain surface, **seen from directly behind**, full box visible. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**V-D3** *(case declares: left side, full box)* — Have the box-creature character from the attached reference images sitting on a plain surface, **front view**, full box visible. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**V-D4** *(case declares: back, full box)* — Have the box-creature character from the attached reference images sitting on a plain surface, **three-quarter front view**, full box visible. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**V-B1** *(case declares: three-quarter — borderline)* — Have the box-creature character from the attached reference images on a plain surface, turned about sixty degrees away from camera, between a three-quarter view and a side view. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

---

## D. Anatomy-count defects (6 gen) — the nub/leg count (the Em blind spot)

**A-D1** *(pair C01 — THE leg-count case)* — Have the box-creature character from the attached reference images sitting idle, front view, full box visible, but with only two stub legs beneath it instead of four. Change only the leg count. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**A-D2** *(pair C01)* — Have the box-creature character from the attached reference images sitting idle, front view, full box visible, but with three stub legs beneath it instead of four. Change only the leg count. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**A-D3** *(pair C02 — the far-nub view-dependent miss)* — Have the box-creature character from the attached reference images perched looking curious, three-quarter view, but only the near ear/arm nub is drawn — the far-side nub is completely missing. Change only the nub count. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**A-D4** *(pair C01)* — Have the box-creature character from the attached reference images sitting idle, front view, full box visible, but with a third extra ear/arm nub sticking out of the top of the box. Change only the nub count. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**A-D5** *(pair C01)* — Have the box-creature character from the attached reference images sitting idle, front view, full box visible, but the four stub legs are fused into one solid base with no separate legs. Change only the legs. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**A-D6** *(pair C03)* — Have the box-creature character from the attached reference images sitting, left side view, full box visible, but with six stub legs beneath it instead of four. Change only the leg count. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

---

## E. Palette defects (5 gen)

**PA-D1** *(pair C07 — style line edited: terracotta body removed)* — Have the box-creature character from the attached reference images in a close view of its face, front view, neutral expression, rendered entirely in graphite monochrome with no color at all. Change only the color. Maintain the warm 2D pencil-test render: warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**PA-D2** *(pair C01 — style line edited: terracotta body removed)* — Have the box-creature character from the attached reference images sitting idle, front view, full box visible, but its body is slate blue-gray instead of terracotta clay-orange. Change only the body color. Maintain the warm 2D pencil-test render: warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**PA-D3** *(pair C02 — style line edited: terracotta body removed)* — Have the box-creature character from the attached reference images perched curious, three-quarter view, but its body is bright lime green instead of terracotta clay-orange. Change only the body color. Maintain the warm 2D pencil-test render: warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**PA-D4** *(pair C01 — style line edited: terracotta body removed)* — Have the box-creature character from the attached reference images sitting idle, front view, full box visible, but rendered in an oversaturated high-chroma neon orange. Change only the color saturation. Maintain the warm 2D pencil-test render: warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**PA-D5** *(pair C02)* — Have the box-creature character from the attached reference images perched curious, three-quarter view, but the warm cream paper is replaced with a flat cool-white background. Change only the background. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow.

---

## F. Construction-lines defects (3 gen + 1 hand-drawn)

*Pure axis: the visible construction cross-line / spherical-mass swirl is erased; the final pencil contour stays.*

**CL-D1** *(pair C07)* — Have the box-creature character from the attached reference images in a close view of its face, front view, neutral expression, drawn as a fully cleaned-up final with no construction lines or under-drawing visible anywhere. Change only that. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**CL-D2** *(pair C01)* — Have the box-creature character from the attached reference images sitting idle, front view, full box visible, drawn as a fully cleaned-up final with no construction lines or under-drawing visible anywhere. Change only that. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**CL-D3** *(pair C02)* — Have the box-creature character from the attached reference images perched curious, three-quarter view, drawn as a fully cleaned-up final with no construction lines or under-drawing visible anywhere. Change only that. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), cross-hatch warm-graphite shadow, warm cream paper.

**CL-B1** *(pair C07 — HAND-DRAW)* — front face view with construction lines **almost fully erased; only the faintest trace remains** (deliberately ambiguous).

---

## G. Shading-register defects (4 gen + 1 hand-drawn)

*Style line edited in each: "cross-hatch warm-graphite shadow" removed (it's the axis being corrupted).*

**SH-D1** *(pair C07)* — Have the box-creature character from the attached reference images in a close view of its face, front view, neutral expression, but shaded with smooth photographic soft shading instead of cross-hatch pencil shading. Change only the shading. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), warm cream paper.

**SH-D2** *(pair C08)* — Have the box-creature character from the attached reference images in a close view of its face, three-quarter view, delighted expression, but shaded with hard anime cel-shading bands instead of cross-hatch pencil shading. Change only the shading. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), warm cream paper.

**SH-D3** *(pair C01)* — Have the box-creature character from the attached reference images sitting idle, front view, full box visible, but completely flat with no shading at all. Change only the shading. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), warm cream paper.

**SH-D4** *(pair C03)* — Have the box-creature character from the attached reference images sitting, left side view, full box visible, but shaded with glossy 3D-rendered gradient shading instead of cross-hatch pencil shading. Change only the shading. Maintain the warm 2D pencil-test render: flat muted terracotta clay-orange body, warm graphite line (not vector black), warm cream paper.

**SH-B1** *(pair C08 — HAND-DRAW)* — three-quarter face view shaded **slightly too smoothly** — the pencil cross-hatch tooth mostly gone but not fully rendered (deliberately ambiguous).

---

## Workflow

1. **Clean pool first** (C01–C16) — generate, eyeball each against the anchor + turnaround (box proportion ~1:1.2, four legs, two nubs, terracotta — reject and re-roll any that come back off-model; the text never mentions identity, the references carry it).
2. **Defects second**, each against its pair's pose.
3. **Hand-drawn borderlines last** (P-B1/2, CL-B1, SH-B1) if NB2 won't land them.
4. **You ratify every image** before it enters `cases.yaml`. Your eye is the ground truth (the sean discipline).
5. If NB2 refuses a corruption after 2–3 tries (it may "fix" defects back toward clean — especially the leg-count, which it likes to normalize to four), hand-draw it and note the refusal — that's data about Em's own blind spot.

*When the 46 are generated + ratified, hand off to Claude Code for the ingest + the costed reference-blind baseline (the kickoff). The mascot baseline is a separate trace; the sean verdict-baseline md5 stays frozen.*
