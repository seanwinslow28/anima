# The compositing doctrine — placing one character into a pre-made scene

*2026-07-12. anima's editing template ([`2026-05-30-nb2-editing-character-consistency-template.md`](2026-05-30-nb2-editing-character-consistency-template.md)) covers the one-image case: a character reference plus a change instruction. **Compositing is a different operation** — two references (a character and a pre-made background/frame) fused into one image where the character must stay identical, land in the right spot, and read at the right size. anima had no documented doctrine for this; Sean's hardest named pain (a character into a scene, true-to-framing) had no answer. This doc lands one, proven live on the Higgsfield Nano-Banana-2 (`nano_banana_flash`) transport with the GRANDMASTER kid-samurai subject. Full run + scoring sheets: [`runs/2026-07-11-prompt-ladder-grandmaster/C_compositing/`](../../runs/2026-07-11-prompt-ladder-grandmaster/C_compositing/) (gitignored; local). Method: the prompt-ladder harness — hold subject/references/target fixed, vary only the prompt, let Sean's eye rank.*

---

## The one-paragraph answer

Compositing is editing with a second reference, and the second reference changes the physics: the character carries identity, the background carries the stage, and the text's only job is to say **where** and **how big** — never to re-describe either image. **NB2 composites cleanly** — given `Image 1 = character` and `Image 2 = background scene`, it lifts the character in, holds identity with zero melt, matches the scene's flat style, and relights the figure into the scene's color cast. But three things do not come for free and must be commanded: **scale** (terse prompts default to a large, center-frame hero — you must explicitly say "small, dwarfed by the sky" to get the negative-space look), **position** (a text description of location — "left side, near the porch" — beats a drawn placeholder shape, which the model erases without honoring its geometry), and **pose** (the one thing text can't nail — for a specific or dynamic pose, hand-draw a **solid, filled silhouette**; an open outline sketch fails, read as an annotation to keep). The single load-bearing failure mode is over-prompting the *scene*: any verbose re-description of the background overrides the "keep Image 2 unchanged" clause and makes NB2 **regenerate** the plate — collapsing a flat poster into rendered CGI and hallucinating props. The winning compositing prompt is ~50–70 words: role-tag both references, enumerate the identity-lock, one scale clause, one position clause, protect the background, ban text. Longer only hurts.

---

## What the ladder proved (the evidence)

Every claim below is a ranked A/B from the live run, not a borrowed rule.

**NB2 composites two references, and identity survives.** Passing the character anchor as `--image` #1 and the background plate as `--image` #2, NB2 reliably placed the boy into the scene, held his face/hair/headband/garments against the anchor, matched the flat poster style of the plate, and relit him into its amber cast. No identity melt across the entire block. This alone is the unlock anima was missing.

**Terse composites, but defaults to a large center hero.** The bare instruction ("place the boy from Image 1 into the scene in Image 2") produced a clean, identity-correct composite — placed **huge, center-frame**, killing the negative space. Scale is not inferred from the plate's emptiness; it is a thing you command.

**Scale is fully prompt-driven with one clause (C2).** Holding character + plate fixed and varying only a scale clause produced the entire range on demand — close-up (head-and-shoulders fills frame) → medium → wide → extreme-wide (a tiny figure dwarfed by the sky) — identity, flat style, and background preserved in every one. The model does **not** lock to one scale; "small, dwarfed by the sky" / "medium" / "large close-up" each land.

**Position: text beats a drawn shape (C3).** A magenta figure-sized ellipse painted into the plate at a deliberately off-center spot was **erased cleanly but spatially ignored** — the model reverted to its default center-large placement, honoring only "remove the marker." The same location stated in words — "on the LEFT side of the yard, near the porch, medium size" — **landed first try.** On NB2, a text description of location + size out-places an abstract drawn placeholder.

**Pose: a solid hand-drawn silhouette is the escape hatch, but it carries pose ONLY — not size (C4).** With a *pose-agnostic* prompt (no words describing the pose — the drawing had to carry it), a **solid, dark-filled** silhouette of a leaping overhead sword-swing transferred the **pose exactly** — the boy rendered in that precise aerial pose, silhouette removed, identity held. A pose text could never specify, nailed by the drawing. But two caveats sharpened on review:
- **Size does not come from the silhouette.** The model matched the *pose* but scaled the figure up past the silhouette's footprint — the character read too large/dominant. Sean's web-app re-prompts (ChatGPT + NB2) fixed it by **commanding size explicitly in text** (a small, true-to-framing figure in the negative space). So size stays text's job even when a silhouette drives the pose — exactly consistent with C2/C3 (text owns size + position; the drawing owns pose). Instruct "…in that pose, rendered small/at medium size" — don't trust the silhouette's scale.
- **Solid fill, not outline.** A **grey, open-outline** sketch of a second pose **failed**: the model read the outline as an annotation to *keep*, left it in place as a ghost figure, and spawned a separate character center-frame. Fill the silhouette solid.

**Over-prompting the scene is destructive (base Rung 4).** The verbosity ladder on the composite showed the same terse-wins shape as the identity-edit block — but with a compositing-specific failure. Rungs 1–3 (terse → medium) all held; Rung 4, a 150-word literary re-description of the *whole scene*, made NB2 **regenerate the background**: the flat poster plate became rendered CGI (soft volumetric clouds, gradient sky, 3D dirt) and grew hallucinated balloons and eggs. In compositing, over-prompting doesn't hurt the character — **it destroys the background you were trying to preserve.** The "keep Image 2 unchanged" clause is the whole ballgame, and verbose scene prose overrides it.

---

## The template

```
Image 1 is the character. Image 2 is the background scene.
Place the boy from Image 1 [SCALE CLAUSE] [POSITION CLAUSE] in Image 2.
Keep his exact identity from Image 1 (face, spiky black hair, red headband
and tails, sleeveless white gi, black sash, gray cropped trousers).
Keep Image 2's flat poster style, background, and amber color cast unchanged.
Do not add any text.
```

- **`[SCALE CLAUSE]`** — always present. "small, standing in the open ground, dwarfed by the vast sky" (negative-space signature) · "at medium size" · "as a large close-up filling the frame." Terse-with-no-scale defaults to large-center.
- **`[POSITION CLAUSE]`** — in words. "roughly center-frame" · "on the left, near the porch" · "far back on the ground." Beats a drawn marker.
- **Identity-lock** — enumerate; don't say "the same boy."
- **Keep-clause** — load-bearing. Name the plate's style + the elements to preserve. Never re-describe the scene beyond this.
- **Anti-text** — mandatory, as in all NB2 work.

**For a specific or dynamic pose**, draw a **solid, filled silhouette** into the plate at the exact spot for the pose, **and keep the text scale clause** — the silhouette carries pose, text still carries size: *"The figure-shaped placeholder marks the pose; render the boy in that exact pose, at [small/medium] size, and remove the placeholder completely."* Fill the silhouette solid — an outline sketch is read as an annotation and left as a ghost.

## Failure-mode → clause map (compositing-specific, extends the editing table)

| Failure mode | What happens | The clause that prevents it |
|---|---|---|
| Default hero scale | Terse composite places the character huge/center; negative space lost | Explicit scale clause: "small, dwarfed by the sky" / "medium" / "close-up" |
| Placement ignored | Character lands center regardless of intent | State position in **words** ("left, near the porch"); do not rely on a drawn marker |
| Placeholder ghost | An outline sketch is kept as a second figure; a new character spawns elsewhere | Use a **solid filled** silhouette, not an outline; instruct "remove the placeholder completely" |
| **Background regeneration** | Verbose scene prose makes NB2 re-render the plate → flat becomes CGI + hallucinated props | **Never re-describe the scene.** One "keep Image 2's style/background/cast unchanged" clause and stop |
| Pose unspecifiable in words | A dynamic/aerial pose can't be reliably worded | Hand-draw a **solid** silhouette in the target pose; let it carry the pose (position/size stay in text) |

## Workflow note

Sean's observed pipeline — anchor → turnaround → separate background → place — is validated, with one simplification: **the placeholder step is usually unnecessary.** Text drives size (C2) and position (C3) well enough that you go straight from a clean background plate + character anchor to a composite. Reach for a hand-drawn silhouette only when you need a *specific pose* the model won't infer — and draw it solid.

## Scope / caveats

- Transport: Higgsfield `nano_banana_flash` (Nano Banana 2), 16:9, 2k, ~1.5–2 cr/composite. The character anchor was a single flat full-body plate; the anchor-as-source held perfectly throughout, so the turnaround-as-source comparison (C1) was not needed.
- Style tested: the flat cinematic poster register (`samurai-jack-s5`). The clauses are register-agnostic by construction (identity markers + a style token), but the "keep the plate flat" instruction matters most where the plate is flat — a painterly plate would swap the style token, not the structure.
- Single subject, single scene. Multi-character compositing (two figures into one plate, occlusion, interaction) is untested and the obvious next probe.
