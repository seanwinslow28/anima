# FINDING — Em is reference-blind (the #1 critic-spine fix)

**Date:** 2026-06-01
**Severity:** Critical — highest-leverage improvement for the T2 vision critic.
**Surfaced by:** the Em scored baseline (`evals/vision_critic/`), STOP GATE 1.
**Confirmed by:** Sean, looking at the frames — `clean_F13` and `clean_F31` are
unmistakably the correct Sean anchor character, yet Em strongly flagged them.

---

## The finding

Em judges every frame **against text only — she is never shown a reference
image.** `VisionCriticNode.run()` attaches exactly one image (the frame under
review): `image_paths=[model_image_path]` ([pipeline/agents/vision_critic.py:113](../../pipeline/agents/vision_critic.py)).
She receives **no `anchor.png`, no Character-Bible plate, no A-2, no prior
approved frame, no side-by-side.**

Everything she "compares to" is prose, concatenated by `_build_prompt`:
- her standing context (`anima-standing-context.md` + `em-vision-critic-context.md`),
- `default_context_files` = PHILOSOPHY.md, CLAUDE.md (the HF/SF/CC gate
  definitions), docs/pipeline-architecture-v1.md,
- the one-line `beat_description`.
- (`acceptance_criteria.json` isn't loaded either — `ctx.criteria` is never read by Em.)

**The kicker:** Em's own addendum trains her to reason about an anchor she
cannot see — e.g. *"the A-2 anchor and F18 both read closer to 65°… SF02
identity-drift"* ([em-vision-critic-context.md:68](../../pipeline/agents/prompts/em-vision-critic-context.md)).
She is prompted to compare against a reference that is never attached.

## Evidence (the 2026-06-01 baseline)

- **Performs segment: recall 1.00, false-pass 0.00, but precision 0.62** — Em
  caught every real defect AND raised 8 false alarms on clean frames.
- The strongest false alarms — Em **failed** `clean_F13` and `clean_F31`,
  shipped Act 1 hero frames that are visibly the correct Sean. With no anchor to
  confirm "this matches the reference," Em has no licence to say `pass`; she
  flags on whatever text-rule she can measure off the pixels (HF01 16:9, SF05
  expression-vs-beat).
- Interpretation: the recall is real (gross breaks are catchable from text rules
  + measuring the image); the precision gap is largely **reference-blindness**,
  not genuine over-strictness.

## The fix (next workstream — must happen)

Give Em the comparison image(s) she's already prompted to reason about:

1. **Attach references in `run()`** — `image_paths=[frame, anchor, *relevant_bible_plates]`.
   The anchor (and per-view turnaround / costume / prop plates relevant to the
   shot) come from the character's Bible folder via the manifest `characters:` /
   `criteria_sources:` registry.
2. **Tell Em which image is which** in `_build_prompt` — "image 1 is the frame
   under review; images 2..N are the identity/style references — compare against
   them." (Her addendum already speaks this language.)
3. **Per-case reference wiring in the eval** — `cases.yaml` gains a `references:`
   field; the harness attaches them. Then **re-run the baseline** — precision is
   expected to rise sharply as the reference-blind false alarms resolve, while
   recall holds. The eval infra built this session is exactly the instrument to
   measure that pre/post delta (the portfolio artifact).
4. **Bake-off note:** the 2026-06-01 three-way bake-off compares Gemini/Sonnet/
   Opus while all three are *equally* reference-blind, so it is still a valid
   relative comparison — but it should be re-run once references land.

## Why it was out of scope to fix in this session

This session's plan built the *ruler* (scored eval, motion-sight, bake-off). The
ruler did its job: it surfaced the critic's biggest flaw with evidence. Fixing
reference-blindness is a clean, well-defined follow-on that changes Em's inputs
and invalidates/improves the baseline (requiring a re-run + re-ratification) — it
deserves its own TDD'd workstream, not a bolt-on. **It is the locked #1 next
step for the critic spine.**
