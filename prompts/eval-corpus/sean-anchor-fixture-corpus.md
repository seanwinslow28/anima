# Sean-anchor — eval fixture corpus spec + prompts (v2, minimal grammar)

*2026-06-03. The class-isolated fixture corpus for the eval-foundation reset (`docs/2026-06-03-eval-foundation-reset-plan.md`). Decisions locked: **shared clean pool**, **paired** clean/defect, **generate-first** (hand-draw borderlines).*

*v2 (same day): the v1 five-slot scaffold was empirically too verbose — a 4-prompt Flow test showed the model-sheet language pushed NB2 into sheet mode (3 panels + ladder lines) and the long keep-lists degraded scene coherence (the PA-D2 desk). Sean's minimal prompt won outright. v2 adopts it: **the references carry identity; the text carries only the beat + one corruption.** This is the NB2 editing doc's own headline finding ("terse text plus a strong reference beats verbose prose"), now enforced.*

---

## How to run every prompt

- **Attach two references:** `characters/sean-anchor/anchor.png` + the matching turnaround (`sean-character-full-body-turnaround.png` for body/beat fixtures, `sean-head-turnaround.png` for portraits).
- **Copy the prompt verbatim.** Each is complete — no filling in.
- **Save outputs at 1K**, one file per fixture, named by its ID. *(Format amended 2026-06-03 at ratification: the corpus shipped as uniform JPEG 1376×768 — uniformity matters more than format; don't mix. Match JPEG for any re-roll.)*
- **Never** add identity descriptions, keep-lists, or the words *turnaround / model sheet / views / reference sheet* to a fixture prompt — that's what broke the v1 tests.
- Framing knobs you can tweak freely per Sean's "mess with angles/placement": `full body visible · framed from the waist up · head-and-shoulders` / `front view · three-quarter view · left profile · right profile · from behind` / `character centered · character on the left third · character on the right third`.

**The style line (verbatim, every prompt):**
> Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**The one structural rule:** when a defect corrupts something the style line itself asserts (cross-hatch → shading defects; color wash → monochrome), that phrase is removed from the style line in that prompt. Already done below where needed.

---

## Corpus at a glance

| Class | Owner | Clean | Defect | Borderline | Author |
|---|---|---|---|---|---|
| proportion | Bible-lock | ← pool | 3 | 2 | gen + draw |
| view-correctness | Bible-lock | ← pool | 4 | 1 | gen (label-side defect) |
| anatomy-count* | Bible-lock | ← pool | 4 | 0 | gen |
| palette | Em / T2 | ← pool | 5 | 0 | gen |
| construction-lines | Em / T2 | ← pool | 4 | 1 | gen + draw |
| shading-register | Em / T2 | ← pool | 4 | 1 | gen + draw |
| **shared clean pool** | (negative for all) | **16** | — | — | gen |

**Totals: 45 Sean fixtures** (16 clean + 24 defect + 5 hand-drawn borderline). Mascot = separate batch, needs its own turnaround first.

\* *anatomy-count* interpreted for a human as hand/digit/limb correctness — **pending Sean's confirm/redirect/drop.**

---

## A. Shared clean pool (16)

*Production-keyframe style, never sheet-style. C13 is Sean's proven test prompt verbatim — its output (`seans-simple-prompt`) can simply be kept as the fixture.*

**C01** — Have the subject from the attached reference images standing idle beside his drawing desk, full body visible, front view, character centered. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C02** — Have the subject from the attached reference images standing and explaining something with one hand raised mid-gesture, three-quarter view, full body visible. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C03** — Have the subject from the attached reference images walking mid-stride, left profile, full body visible. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C04** — Have the subject from the attached reference images reaching up for a pencil on a shelf, seen from a three-quarter back angle, full body visible. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C05** — Have the subject from the attached reference images standing relaxed with his weight on one leg, seen from behind, full body visible. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C06** — Have the subject from the attached reference images leaning against his drawing desk with arms loosely crossed, right profile, full body visible. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C07** — Have the subject from the attached reference images in a head-and-shoulders portrait, front view, neutral relaxed expression. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C08** — Have the subject from the attached reference images in a head-and-shoulders portrait, three-quarter view, warm half-smile. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C09** — Have the subject from the attached reference images in a head-and-shoulders portrait, left profile, contemplative, looking off into the distance. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C10** — Have the subject from the attached reference images in a head-and-shoulders portrait, right profile, mildly surprised with eyebrows raised. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C11** — Have the subject from the attached reference images in a head-and-shoulders portrait, three-quarter view, mid-speech with mouth open. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C12** — Have the subject from the attached reference images in a head-and-shoulders portrait, front view, focused concentration with brow slightly furrowed. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C13** *(Sean's proven prompt — keep its existing output)* — Have the subject within the attached reference images sitting at a computer desk. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C14** — Have the subject from the attached reference images standing at a tilted drawing desk, drawing with a pencil in his right hand, three-quarter view, framed from the waist up. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C15** — Have the subject from the attached reference images glancing up from his work and smiling, three-quarter view, framed from the waist up. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**C16** — Have the subject from the attached reference images sitting on a stool sketching on a pad in his lap, three-quarter view, full body visible. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

---

## B. Proportion defects (3 gen + 2 hand-drawn) — pair noted per fixture

**P-D1** *(pair C01 — proven in test)* — Have the subject from the attached reference images standing idle, front view, full body visible, but drawn at chibi proportions, about four heads tall, with an oversized head and a shortened body. Change only the proportion. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**P-D2** *(pair C02)* — Have the subject from the attached reference images standing and explaining something with one hand raised, three-quarter view, full body visible, but drawn short and stocky, about five heads tall. Change only the proportion. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**P-D3** *(pair C03)* — Have the subject from the attached reference images walking mid-stride, left profile, full body visible, but drawn stretched and over-elongated, about eight and a half heads tall. Change only the proportion. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**P-B1** *(pair C01 — HAND-DRAW)* — standing idle, front, full body at **~6.5 heads** (just under target).
**P-B2** *(pair C01 — HAND-DRAW)* — standing idle, front, full body at **~7.5 heads** (just over target).

---

## C. View-correctness defects (4 gen + 1) — the defect is in the LABEL, not the prompt

*These prompts are clean prompts of the "wrong" view. The corruption happens in `cases.yaml`: the case **declares** one view while the image draws another. Generate fresh files (one file = one label) — don't reuse clean-pool images.*

**V-D1** *(case declares: three-quarter, full body)* — Have the subject from the attached reference images standing and explaining something with one hand raised, **left profile**, full body visible. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**V-D2** *(case declares: front portrait)* — Have the subject from the attached reference images in a head-and-shoulders portrait, **three-quarter view**, neutral expression. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**V-D3** *(case declares: left-profile portrait)* — Have the subject from the attached reference images in a head-and-shoulders portrait, **right profile**, contemplative. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**V-D4** *(case declares: back view, full body)* — Have the subject from the attached reference images standing relaxed, seen from a **three-quarter back angle**, full body visible. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**V-B1** *(case declares: three-quarter portrait — borderline)* — Have the subject from the attached reference images in a head-and-shoulders portrait, turned about sixty degrees away from camera, between a three-quarter view and a profile. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

---

## D. Anatomy-count defects (4 gen) — pending your confirm on the interpretation

**A-D1** *(pair C13)* — Have the subject from the attached reference images sitting at a computer desk, but the hand on the keyboard has six fingers. Change only that hand. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**A-D2** *(pair C02)* — Have the subject from the attached reference images standing and explaining something with one hand raised, three-quarter view, full body visible, but the raised hand is fused and malformed with indistinct fingers. Change only that hand. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**A-D3** *(pair C01)* — Have the subject from the attached reference images standing idle, front view, full body visible, but with three arms — an extra arm at one shoulder. Change only the limb count. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**A-D4** *(pair C16)* — Have the subject from the attached reference images sitting on a stool sketching on a pad in his lap, three-quarter view, full body visible, but with only one leg visible where two should be. Change only that. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

---

## E. Palette defects (5 gen)

**PA-D1** *(pair C07 — style line edited: color wash removed)* — Have the subject from the attached reference images in a head-and-shoulders portrait, front view, neutral expression, rendered entirely in graphite monochrome with no color wash. Change only the color. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), cross-hatch shadow, warm cream paper.

**PA-D2** *(pair C13 — proven in test)* — Have the subject from the attached reference images sitting at a computer desk, but his t-shirt is red instead of navy blue. Change only the shirt color. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**PA-D3** *(pair C08)* — Have the subject from the attached reference images in a head-and-shoulders portrait, three-quarter view, warm half-smile, but his hair is dark brown instead of sandy blonde. Change only the hair color. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**PA-D4** *(pair C01)* — Have the subject from the attached reference images standing idle, front view, full body visible, but rendered in an oversaturated high-chroma candy-color palette. Change only the color saturation. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**PA-D5** *(pair C03)* — Have the subject from the attached reference images walking mid-stride, left profile, full body visible, but his jeans are brown and his sneakers are white. Change only those colors. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

---

## F. Construction-lines defects (4 gen + 1 hand-drawn)

*Pure axis: the visible under-drawing is erased; the final pencil line stays.*

**CL-D1** *(pair C07)* — Have the subject from the attached reference images in a head-and-shoulders portrait, front view, neutral expression, drawn as a fully cleaned-up final with no construction lines or under-drawing visible anywhere. Change only that. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**CL-D2** *(pair C01)* — Have the subject from the attached reference images standing idle, front view, full body visible, drawn as a fully cleaned-up final with no construction lines or under-drawing visible anywhere. Change only that. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**CL-D3** *(pair C08)* — Have the subject from the attached reference images in a head-and-shoulders portrait, three-quarter view, warm half-smile, drawn as a fully cleaned-up final with no construction lines or under-drawing visible anywhere. Change only that. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**CL-D4** *(pair C14)* — Have the subject from the attached reference images standing at a tilted drawing desk drawing with a pencil in his right hand, three-quarter view, framed from the waist up, drawn as a fully cleaned-up final with no construction lines or under-drawing visible anywhere. Change only that. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, cross-hatch shadow, warm cream paper.

**CL-B1** *(pair C07 — HAND-DRAW)* — front portrait with construction lines **almost fully erased; only the faintest trace remains** (deliberately ambiguous).

---

## G. Shading-register defects (4 gen + 1 hand-drawn)

*Style line edited in each: "cross-hatch shadow" removed (it's the axis being corrupted).*

**SH-D1** *(pair C07)* — Have the subject from the attached reference images in a head-and-shoulders portrait, front view, neutral expression, but shaded with smooth photographic soft shading instead of cross-hatch pencil shading. Change only the shading. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, warm cream paper.

**SH-D2** *(pair C08)* — Have the subject from the attached reference images in a head-and-shoulders portrait, three-quarter view, warm half-smile, but shaded with hard anime cel-shading bands instead of cross-hatch pencil shading. Change only the shading. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, warm cream paper.

**SH-D3** *(pair C01)* — Have the subject from the attached reference images standing idle, front view, full body visible, but completely flat with no shading at all. Change only the shading. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, warm cream paper.

**SH-D4** *(pair C03)* — Have the subject from the attached reference images walking mid-stride, left profile, full body visible, but shaded with glossy digital airbrush gradients instead of cross-hatch pencil shading. Change only the shading. Maintain the warm 2D Disney pencil-test render: soft graphite line (not vector black), light hand-painted color wash, warm cream paper.

**SH-B1** *(pair C08 — HAND-DRAW)* — three-quarter portrait shaded **slightly too smoothly** — pencil tooth mostly gone but not fully rendered (deliberately ambiguous).

---

## Workflow

1. **Clean pool first** (C01–C16) — generate, eyeball each against the turnarounds (proportion especially; the text never mentions it now, the body-turnaround reference carries it — reject and re-roll any that come back off-model).
2. **Defects second**, each against its pair's pose.
3. **Hand-drawn borderlines last** (P-B1/2, CL-B1, SH-B1).
4. **You ratify every image** before it enters `cases.yaml`.
5. If NB2 refuses a corruption after 2–3 tries (it may "fix" defects back toward clean), hand-draw it and note the refusal — that's data.

## Mascot (separate batch — not yet)

Needs its own turnaround sheet first (one body+face sheet, 5 views). Classes concentrate on **anatomy-count (nub count), box-proportion (1:1.2 w:h), palette, view-correctness** + construction/shading. ~15 fixtures. Spec it after the Sean corpus proves the pattern.
