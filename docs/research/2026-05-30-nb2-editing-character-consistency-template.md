# The register-agnostic NB2 editing template — one character, any style, any shot

*2026-05-30. Cy authors a character by editing, not by drawing from scratch: she hands an image model a reference of the character and a short instruction — "same person, new angle / new expression / new pose, keep the identity" — and reads back a plate. That is an **editing** operation, and editing has its own physics, distinct from text-to-image generation. This doc does two things. First, it synthesizes current (mid-2026) research on how Nano Banana 2's editing mode actually behaves — building on, not repeating, [`2026-05-30-nb-pro-nb2-prompting-for-pixel-and-angle-expansion.md`](2026-05-30-nb-pro-nb2-prompting-for-pixel-and-angle-expansion.md). Second — the headline — it lands a **register-agnostic editing-prompt template**: one parameterized structure that plugs into any 2D style anima will ever ship, serves both Character Bible authoring and Phase 3 storyboarding, and encodes the hard-won field lessons rather than fighting them. The companion plan that wires it into Cy lives in [`../2026-05-30-claude-mascot-pencil-register-pivot-kickoff-amendments.md`](../COMPLETED/cy/2026-05-30-claude-mascot-pencil-register-pivot-kickoff-amendments.md).*

---

## The one-paragraph answer

Editing-mode identity preservation is a layering problem, not a description problem. The reference image carries the identity; the text carries only the *change*; and the two compete — so the more you describe the character in words, the more the model drifts away from the reference and toward the generic thing your words happen to spell. Every reliable practitioner template in 2026 converges on the same shape: **name the anchor and lock it by enumerated markers, state exactly one change, name what stays the same, and apply the style register last.** That shape is register-agnostic by construction — the only thing that changes between pencil-test, pixel-art, anime, watercolor, or a 3D-look is which markers you enumerate and which style token you append at the end. What is *not* register-agnostic is the post-processing burden: pixel art needs a grid-snap/quantize pass the model structurally cannot do in-prompt, line-art needs explicit "no shading" negatives, and every register needs a chroma-key path because these models never emit an alpha channel. And the model choice itself flips an assumption anima currently bakes in: for editing and consistency work — which is the entire job — **NB2 (`gemini-3.1-flash-image-preview`) holds identity better, costs half, and runs four times faster than NB Pro**, while NB Pro currently carries a documented multi-reference downsampling regression that makes it the *wrong* default for the exact work Cy does today.

---

## What the research says (building on the prior pass)

The earlier research doc settled three things this one takes as given: pixel-grid fidelity is a post-process problem; angle expansion needs multiple views in the reference (photogrammetric inference); and NB2 may beat NB Pro on cross-generation consistency. This pass went deeper on *editing specifically* — the image+text operation, not generation — and the findings sharpen each of those into a prompt structure.

**Terse text plus a strong reference beats verbose prose — and now we know why.** The single most repeated finding across 2026 practitioner sources is that detailed character descriptions in an edit prompt *reduce* consistency: the model tries to satisfy both the reference pixels and the prose, they diverge, and identity slides toward whatever the words describe. RunDiffusion calls the reference a "latent identity fingerprint" that verbose text overwrites. This is the field report's `focused`-went-monochrome incident stated as a general law: the runner owning framing was necessary, but a loud-enough plate prompt still wins, because *the text and the reference are in tension by design*. The template's job is to keep the text quiet about identity and loud only about the delta.

**Single-shot off a fixed anchor preserves identity; chaining propagates drift.** NB2 reduced inter-iteration drift relative to its predecessor, but the documented failure mode is iterative degradation — artifacts accumulate and instruction-following decays after roughly five to ten chained turns (the "Banana100" replication study is the extreme demonstration). The mitigation every storyboard guide converges on is **re-anchor every frame to the original canonical reference, never chain off the previously generated frame.** This is exactly Cy's existing no-chaining policy (`_resolve_generate_references` strips references to generated plates), and the external evidence is now strong enough to call it load-bearing rather than cautious.

**The reference slot order is load-bearing, and the early slots are privileged.** Google officially endorses the role-assignment idiom — "use Image A for the pose, Image B for the style, Image C for the background." Practitioner testing adds that the first ~6 reference slots get high-fidelity processing and most strongly shape the output; slots 7–14 are supplementary. For a single identity-preserving edit, the winning pattern is **1–3 references with the identity anchor first** — piling on references dilutes the identity signal. anima's runner already injects `anchor.png` first unconditionally; the research says keep it there and keep the count low.

**The "change only X, keep everything else" idiom is the reliable core.** The canonical structure separates three buckets — what is LOCKED (identity from the reference), what CHANGES (the single edit delta), and the STYLE register — and the phrasing that holds each is specific. Lock with enumeration ("match the eyes, nose shape, jawline, hair, proportions of Image 1 exactly"), not generics ("keep the same person"). Change with the **`ONLY CHANGE: X`** construction and exactly one variable per edit; "change" is a safer verb than "transform" or "turn into," which trigger wholesale re-rendering. Name the preserved set explicitly — Google Cloud frames this as text-defined semantic masking, a mask you paint in words. And introduce the **style medium last**, after identity is locked, because a style token placed early competes with the identity markers.

**The failure modes map one-to-one onto prevention clauses.** This is what makes a template possible — each documented way editing breaks has a known clause that prevents it:

| Failure mode | What happens | The clause that prevents it |
|---|---|---|
| Identity drift on large pose deltas | Face/proportions shift when the pose changes a lot | Enumerated identity-lock against Image 1; one variable per edit; re-anchor to the original, never a generated frame |
| Attribute / context bleed | A second reference's color or clothing leaks into the subject | Role-tag each reference explicitly ("Image 2 = pose only, do not copy its colors"); section-delimit subject vs background |
| Reference gap (model invents the unseen) | A front-only anchor is asked for a back view → invented anatomy | Supply a *dedicated* view reference for the new angle (the turnaround sheet); don't ask one anchor to imagine a view it doesn't contain |
| Caption / text rendering | Instruction words render as literal letters in the image | `Do not render any text, captions, labels, or watermarks`; keep instruction words unquoted (the models render only quoted text) |
| Background / lighting drift | Background or lighting changes when only the subject was edited | `Keep the background and lighting identical to Image 1`; positive framing ("warm cream paper"), not negative ("no background") |
| No-op edit (returns the input) | Model hands back the reference unchanged | Lead with a strong action verb naming the operation ("Redraw…", "Render…") |

**For editing, route to NB2 — and this one contradicts current anima behavior.** The 2026 consensus is consistent: NB2 is the "iteration engine," NB Pro the "final polish engine." Independent testing (AIToolsSME ran a single-input identity edit ten times and recognized the subject every time) gives NB2 the character-consistency round; NB Pro wins absolute texture, lighting, and painterly restraint. Decisively, a Google AI Developers Forum thread (4 March 2026) documents a **multi-reference regression**: since the 3.1 Flash launch, `gemini-3-pro-image-preview` "downsamples reference images so aggressively that it can't see or replicate fine details, resulting in generic or inaccurate outputs," and a sibling thread has multiple production teams reporting NB Pro ignoring reference images 10–20% of the time via API. NB2 is ~4× faster and ~½ the cost, which makes a retry ladder cheap. **Cy's `invoke_nb_pro` currently defaults to `gemini-3-pro-image-preview`** — i.e., anima routes its most consistency-sensitive work to the model that is currently worst at consistency. The routing fix is in the companion plan; treat the Pro regression as an operational condition to re-verify, not a permanent law, but route around it now.

---

## The template

The structure is five parameterized blocks, emitted in a fixed order. The order is not cosmetic — it is the layering the research demands: anchor first, identity locked before the delta, the delta stated as a single change, the preserved set named, and the style register applied last, just ahead of the negatives and the output spec.

```
[reference-role preamble]    ← runner-owned, fixed
{identity_lock}              ← runner-owned, parameterized by register + character.yaml
{variation}                  ← Cy-authored: the ONE terse plate intent (the only authored slot)
{preserve_and_negative}      ← runner-owned, parameterized by register
{style_register}             ← runner-owned, looked up from style_register (applied LATE)
{output_spec}                ← runner-owned, from manifest/plate
```

Read the slot names as the contract. Cy authors exactly one of them — `{variation}` — and names an optional pose-target reference. Everything else the runner owns and fills from the character's `style_register` and `character.yaml`. That is the refactor decision realized: the runner is the single source of truth for the template, Cy stays terse, and the "runner owns identity framing" lesson is preserved and extended rather than diluted.

**The reference-role preamble** is fixed and names the slots the runner actually fed, in order: *"Image 1 is the identity anchor — the canonical reference for this character."* If a pose/angle reference survived resolution, *"Image 2 is the angle/pose target — match its viewing angle and framing, but identity always comes from Image 1."* This is close to what `_build_nb_pro_prompt` emits today; the template keeps it.

**`{identity_lock}`** enumerates the markers that define this character *in this register*, and commands an exact match to Image 1. The enumeration is register-parameterized because the markers differ by register: pencil-test locks face, hair, palette-in-pencil-terms, proportions; pixel-art locks the indexed palette, the silhouette, the proportion ratio; watercolor locks the pigment vocabulary and the face. The phrasing is affirmative and specific — "Match the face, hair, color palette, and proportions of Image 1 exactly" — never the generic "keep the same character."

**`{variation}`** is Cy's short plate intent and nothing else — the angle, expression, or pose this plate exists to show, wrapped in the `ONLY CHANGE` idiom by the runner: *"Render: [intent]. Change only the [pose/angle/expression]; keep everything else as in Image 1."* One variable. Under ~30 words. No re-description of the character — that is the prompt-dominance trap, and it stays Cy's contract.

**`{preserve_and_negative}`** names what stays identical and forbids what breaks. The preserve clause is register-aware (pencil keeps the cream paper and cross-hatch vocabulary; line-art forbids shading entirely). The negative clause is partly universal — *"Do not add any text, captions, labels, annotations, or watermarks"* — and partly per-register (line-art: "no gradients, no soft shadows"; pixel-art: "no smooth anti-aliased gradients," with the real grid fix deferred to post-process).

**`{style_register}`** is the medium token, applied late and descriptively. This is the single most register-specific slot and the one that makes the template plug-and-play: swap the token, keep the structure. "Warm pencil-test render: graphite line, flat color fills, cross-hatch shadow, cream paper" for one register; "16-bit pixel-art sprite, limited indexed palette, hard edges" for another; "cel-shaded anime, clean lineart, flat color" for a third. Descriptive, never prescriptive ("soft watercolor wash," not "make it Ghibli").

**`{output_spec}`** carries the mechanical frame: aspect ratio, background/isolation, and the prop-plate exception (isolated object, no figure). It is where the storyboard variant slots its shot framing (below).

### The per-register clause library

The template is one structure; the register fills it. This is the reference table the runner's emitter reads — the closed `style_register` vocabulary mapped to its identity markers, its preserve/negative clauses, its style token, and its model. It is the operative artifact: adding a register is adding a row here, deliberately, not editing prose inline.

| `style_register` | Identity markers to enumerate | Preserve / negative clauses | Style token (applied last) | Model + post-process |
|---|---|---|---|---|
| `pencil-test-colored` | face, hair shape, full color palette, proportions | keep cream paper + cross-hatch shadow; **keep the full color of Image 1**; no photographic shading | "warm pencil-test render: graphite line (not vector black), flat color fills, cross-hatch shadow, warm cream paper, hole-punch production marks" | NB2 default; NB Pro only for a texture-rich final, guarded |
| `pixel-art-8bit` | indexed palette (named hexes), round silhouette, head-to-body ratio | hard edges; no smooth gradients; **grid is NOT a prompt clause** | "16-bit pixel-art sprite, limited indexed palette, hard pixel edges, clean outlines" | **NB2**; mandatory post-process: nearest-neighbor downsample + palette quantize; chroma-key for cutout |
| `line-art-only` | contour shapes, line weight, proportions | **no shading, no gradients, no soft shadow, no texture, no color fill beyond flats** | "clean line art, bold uniform outlines, flat fills" | NB2 default |
| `watercolor` | face, pigment-pool palette, proportions | keep paper grain; let washes bleed; no hard vector edges | "soft watercolor wash, pigment-pool bleed, visible paper grain" | NB2 for drafts; **NB Pro for finals**, with a reference-used verification + regenerate guard |
| `photoreal` | face, skin tone, hair, proportions | keep lighting direction + color temperature of Image 1; clean edges, no halos | "photographic rendering, natural lighting, shallow depth of field" | NB Pro for finals, guarded; NB2 for drafts |
| `3d-rendered` | face, material palette, proportions | keep soft global illumination; no flat-shading artifacts | "3D-rendered look, soft global illumination, subtle ambient occlusion" | NB Pro for finals, guarded; NB2 for drafts |

Two columns are doing the register-agnostic work and two are doing the per-register work. The structure (template) and the identity-lock *mechanism* are constant; the markers and the style token vary, and the model/post-process column is where the honest per-style exceptions live — pixel-art's grid, watercolor's painterly final. That split is the whole thesis: **the template is register-agnostic; the plumbing around it is register-aware.**

---

## Three worked examples, three registers

The proof that it is plug-and-play is to fill the same five slots three times, in three registers, and watch only the markers and the token change.

### Example 1 — `pencil-test-colored`, sean-anchor, the expression that drifted

This is the `focused` plate from the production bake, the one that went monochrome because its verbose monochrome-era prose beat the anchor. Filled through the template, the prompt that would have held it:

> *[Image 1 = `characters/sean-anchor/anchor.png`]*
> **[preamble]** Image 1 is the identity anchor — the canonical reference for this character.
> **{identity_lock}** Match the face, hair, full color palette, skin tone, and proportions of Image 1 exactly.
> **{variation}** Render: focused expression, brow slightly down, eyes on the work, mouth set. Change only the expression; keep everything else as in Image 1.
> **{preserve_and_negative}** Keep the cream paper, the cross-hatch shadow, and the full color of Image 1. Do not render the figure in monochrome. Do not add any text, captions, labels, or watermarks.
> **{style_register}** Warm pencil-test render: graphite line (not vector black), flat color fills, cross-hatch shadow, warm cream paper.
> **{output_spec}** 16:9, character centered, warm cream paper background.

The template makes the monochrome drift structurally unlikely: the identity-lock and the preserve clause both assert the full color of Image 1, and the variation slot carries *only* the expression delta — there is no verbose "warm graphite #3D3530, no skin tone" prose left to compete with the anchor, because Cy never authored any. This is the field report's "trim all plate prompts to short intent" recommendation, enforced by the template's shape rather than left to discipline.

### Example 2 — `pixel-art-8bit`, a 16BitFit humanoid, a pose plate

The cross-register proof. Same five slots, swap the markers and the token — and note the model and the post-process change with the register, not the structure:

> *[Image 1 = the 16BitFit fighter anchor; Image 2 = the multi-view sprite sheet]*
> **[preamble]** Image 1 is the identity anchor. Image 2 is the angle/pose target — match its viewing angle, identity comes from Image 1.
> **{identity_lock}** Match the indexed palette (the four named hexes), the round-shouldered silhouette, and the chibi head-to-body ratio of Image 1 exactly.
> **{variation}** Render: mid-jab contact pose, profile, lead arm extended. Change only the pose; keep the costume and palette as in Image 1.
> **{preserve_and_negative}** Hard pixel edges, no smooth anti-aliased gradients. Do not add any text, labels, or watermarks.
> **{style_register}** 16-bit pixel-art sprite, limited indexed palette, hard edges, clean outlines.
> **{output_spec}** Square, character centered, flat magenta `#FF00FF` background for chroma-key.

Two things are register-specific and both live *outside* the template's identity logic: the prompt routes to **NB2** (not the runner's current NB Pro default), and the output is fed to a **post-process** node — nearest-neighbor downsample to the sprite resolution, quantize to the locked palette, chroma-key the magenta to alpha. The model cannot hold a true integer grid in-prompt (prior research, Finding 1); the template doesn't pretend it can. The structure is identical to Example 1; the plumbing is not.

### Example 3 — `line-art-only` / flat anime, an angle plate

A register anima hasn't shipped yet, to prove the template doesn't assume pencil. A clean cel/line register, three-quarter turnaround:

> *[Image 1 = the character anchor; Image 2 = the turnaround sheet]*
> **[preamble]** Image 1 is the identity anchor. Image 2 is the angle target — match its viewing angle, identity from Image 1.
> **{identity_lock}** Match the contour shapes, line weight, hair silhouette, and proportions of Image 1 exactly.
> **{variation}** Render: three-quarter front view, head turned slightly left. Change only the viewing angle; keep the costume as in Image 1.
> **{preserve_and_negative}** No shading, no gradients, no soft shadow, no texture, flat color fills only. Do not add any text, captions, or watermarks.
> **{style_register}** Cel-shaded anime, clean bold lineart, flat color.
> **{output_spec}** 4:3, character centered, plain white background.

The `{preserve_and_negative}` slot is carrying the register's defining discipline here — the explicit ban on shading and gradients that line-art needs and pencil-test does not. Same template, different clause from the library. That is register-agnosticism working: the structure never moved; the register filled it differently.

---

## The storyboard variant

The same operation that authors a Bible plate authors a storyboard frame — anchor plus a delta — so the storyboard template is the base template with one block extended. The `{variation}` slot now carries an **action** rather than a static pose, and `{output_spec}` absorbs a **`{shot}`** sub-block carrying the cinematic frame. Everything else holds, and the iron rule from the research is the same rule Cy already follows: **re-reference the same canonical anchor on every frame; never chain off the previous frame.**

```
[reference-role preamble]    ← Image 1 = identity anchor (the SAME anchor every frame)
{identity_lock}              ← identical across the whole sequence, restated verbatim each frame
{variation}                  ← the ONE action this beat shows
{shot}                       ← shot size · camera height/angle · lens · staging
{preserve_and_negative}      ← continuity lock + no-text
{style_register}             ← identical across the sequence
{output_spec}                ← aspect ratio
```

The `{shot}` block is a closed vocabulary the models reliably understand, drawn from the tested camera-language libraries: shot size (extreme close-up / close-up / medium / wide / establishing), camera height (eye-level / low-angle / high-angle / bird's-eye / Dutch), lens (wide / telephoto / over-the-shoulder / two-shot / POV), and staging ("character left, negative space right; facing camera-right"). A storyboard frame from anima's own Act 2 — Sean with the mascot on his shoulder, reacting:

> *[Image 1 = `characters/sean-anchor/anchor.png`; Image 2 = `characters/claude-mascot/anchor.png`; Image 3 = the A-7 pairing reference]*
> **[preamble]** Image 1 is Sean's identity anchor; Image 2 is the mascot's identity anchor; Image 3 is the canonical pairing for scale and placement.
> **{identity_lock}** Match Sean's face, hair, palette, and proportions from Image 1, and the mascot's box-body form, terracotta palette, and stub-leg silhouette from Image 2, exactly.
> **{variation}** Render: Sean glances up at the mascot, half-smiling. Change only the pose and expression; keep both characters' identity, costume, and the mascot's shoulder-perch scale as established.
> **{shot}** Medium shot, eye-level, slight over-the-shoulder framing, Sean camera-left.
> **{preserve_and_negative}** Keep the cream paper and full color. Do not add any text or watermarks.
> **{style_register}** Warm pencil-test render: graphite line, flat color fills, cross-hatch shadow, cream paper.
> **{output_spec}** 16:9.

The continuity discipline the research insists on is built into the slots: the same anchors feed every frame (no chaining), the identity-lock and style-register slots are restated *verbatim* across the sequence (trait-lock — "emerald eyes" never becomes "green eyes"), and each frame carries exactly one action. The shot vocabulary is the only slot that varies frame to frame, which is exactly the freedom a storyboard wants — hold the character, move the camera.

---

## How this generalizes — the template is a pipeline primitive, not a Cy helper

It is tempting to file this under Phase 2 and move on. That would undersell it. The template describes the **editing operation itself** — anchor plus a single constrained delta — and that operation recurs at three different phases of the pipeline, which means the template is a shared primitive that three different agents should consume from one source.

**Phase 2, Character Bible (Cy).** This is where it lands first: every generate-plate in a Bible is the base template, with `{variation}` carrying the angle/expression/pose. The refactor in the companion plan makes Cy's runner the template's home.

**Phase 3, Storyboard.** anima's architecture has Phase 3 as a largely human-authored beat sheet and shot list, with agents drafting per-shot prompts and running continuity checks. Those per-shot prompts *are* the storyboard variant of this template — same anchor, action plus shot framing, continuity locked across the beat. When Phase 3's prompt-drafting assist lands, it should emit this structure, not invent a parallel one. The shot list becomes a list of `{variation}` + `{shot}` pairs over a fixed cast of anchors; the continuity audit becomes a check that the identity-lock and style-register slots stayed verbatim across the sequence. The same character that Cy authored in Phase 2 walks into Phase 3 storyboards through the same editing door.

**Phase 5, Generate (Flo), and the T2 critic (Em).** Flo's runtime keyframe prompts are the same operation again, citing Cy's `IR.*` rules to fill the `{identity_lock}` enumeration. And Em, the vision critic, reads a frame against the same decomposition the template encodes — was the identity preserved, was only the intended axis changed, did the register hold — which is why the template's slot names map cleanly onto what Em already checks. A rule Cy writes for `{identity_lock}`, a prompt Flo builds, and a verdict Em returns are three views of one structure.

That is the case for treating this as a primitive: define the template once, in the runner, parameterized by the closed `style_register` vocabulary, and Phase 2, Phase 3, and Phase 5 all draw from it. The alternative — a bespoke prompt shape per phase — is how the same character drifts differently in a Bible plate, a storyboard frame, and a keyframe, which is the continuity failure the whole pipeline exists to prevent.

---

## Sources

**Prior anima research (built on, not repeated):**
- [`docs/research/2026-05-30-nb-pro-nb2-prompting-for-pixel-and-angle-expansion.md`](2026-05-30-nb-pro-nb2-prompting-for-pixel-and-angle-expansion.md) — photogrammetric inference, pixel-grid-as-post-process, NB2-may-beat-Pro.
- [`docs/anima-test-runs/2026-05-29-production-bake-and-gate-hardening.md`](../anima-test-runs/2026-05-29-production-bake-and-gate-hardening.md) — prompt-dominance vs reference-gap drift, the runner owns framing, record-only similarity gate.

**Editing mechanics, identity/variation/style decomposition, failure modes:**
- [Google — Prompting tips for Nano Banana Pro](https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/) — official reference role-assignment idiom, quoted-text rule, "character consistency may vary."
- [Google Cloud — Ultimate prompting guide for Nano Banana](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana) — model slugs, [References]+[Relationship]+[New scenario] formula, text-defined semantic masking, strong-verb-first, positive framing.
- [Google DeepMind — Gemini image (Pro) model page](https://deepmind.google/models/gemini-image/pro/) — identity envelope (up to 5 people / 6 objects), 14-reference blending.
- [nano2image — Character consistency (image-to-image)](https://nano2image.com/nano-banana/image-to-image/character-consistency) — the "ONLY CHANGE: X / No text" template, one-variable-per-edit.
- [Seelab — Nano Banana image-to-image prompting guide](https://help.seelab.ai/en/article/nano-banana-image-to-image-prompting-guide-19jba72/) — "change" safer than "transform," avoid vague pronouns.
- [laozhang — NB Pro face consistency guide](https://blog.laozhang.ai/en/posts/nano-banana-pro-face-consistency-guide) — enumerated identity-lock, `###` section delimiters, style-medium-at-end.
- [RunDiffusion — NB2 consistent characters](https://www.rundiffusion.com/nano-banana-2-consistent-character-images) — terse-text + strong-reference, latent identity fingerprint.
- [flowith — Consistent characters / storyboard](https://flowith.io/blog/nano-banana-consistent-characters-storyboard/) — "drift happens the moment you stop naming the character," one-change-per-turn.
- [wavespeed — NB Pro complete guide 2026](https://wavespeed.ai/blog/posts/google-nano-banana-pro-complete-guide-2026/) — reference-slot priority (first ~6 high-fidelity).
- [arxiv — "Banana100" iterative-replication study](https://arxiv.org/pdf/2604.03400) — multi-turn editing degradation evidence.

**Register-agnosticism + storyboarding:**
- [SpriteCook — NB2 into actual pixel art](https://www.spritecook.ai/blog/nanobanana-pixel-art-for-games) — pixel grid is post-process, not promptable.
- [RoboticApe — Generating game sprites with NB Pro, lessons learned](https://roboticape.com/2026/03/07/generating-game-sprites-with-gemini-image-generation-nano-banana-pro-lessons-learned/) — no alpha channel ever; chroma-key + white-outline + HSV; ban gradients/shadows in line styles.
- [Atlabs — One image into multiple camera angles](https://www.atlabs.ai/blog/turn-one-image-into-multiple-camera-angles-nano-banana-pro) — master-shot-as-source-of-truth; copy-paste camera-angle library.
- [Apiyi — NB Pro storyboard / character consistency guide](https://help.apiyi.com/en/nano-banana-pro-ai-video-storyboard-character-consistency-guide-en.html) — character-sheet-first, reuse-on-every-frame, fixed seed, shot-variety rhythm (vendor blog; trust patterns, discount exact percentages).
- [Google AI — NB Pro prompting guide (dev.to)](https://dev.to/googleai/nano-banana-pro-prompting-guide-strategies-1h9n) — identity locking, multi-panel "generate one at a time / vary angles / one of each character per image."
- [prompting.systems — NB Pro character consistency](https://prompting.systems/blog/nano-banana-pro-character-consistency-guide) — lock facial markers, style medium last, one style stack at a time.

**NB2 vs NB Pro for editing:**
- [Google — Nano Banana 2 announcement](https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/) — NB2 positioned for better character consistency across multiple images.
- [DeepLearning.ai — NB2 makes edits easier and faster](https://www.deeplearning.ai/the-batch/nano-banana-2-aka-gemini-3-1-flash-image-makes-edits-easier-and-faster) — ~4× faster, ~½ cost, full API pricing, editing-leaderboard placements.
- [AIToolsSME — NB Pro vs NB2, tested](https://www.aitoolssme.com/blogs/nano-banana-pro-vs-nano-banana-2) — 10/10 identity retention on single-input edit; NB2 wins consistency, Pro wins artistic restraint.
- [Google AI Developers Forum — NB Pro inconsistent with multiple reference images since 3.1 launch (4 Mar 2026)](https://discuss.ai.google.dev/t/gemini-3-0-pro-image-preview-inconsistent-performance-with-multiple-reference-images-since-3-1-launch/128648) — **the multi-reference downsampling regression**, primary source.
- [Google AI Developers Forum — NB Pro ignoring prompt and reference images](https://discuss.ai.google.dev/t/nano-banan-pro-ignoring-prompt-and-reference-images/112781) — production teams report Pro ignoring references 10–20%; Flash-verification + regenerate workarounds.
- [Magnific — NB2 vs NB Pro](https://www.magnific.com/blog/nano-banana-2-vs-nano-banana-pro/) — "NB2 = iteration engine, Pro = final polish engine," routing guidance.

*A freshness caveat worth keeping: the NB Pro multi-reference regression is an operational issue reported late-Feb to early-Mar 2026 and may be patched at any time. The routing decision should treat "Pro reference handling is currently unreliable" as a condition to re-verify, not a permanent model property. The structural facts — NB2 cheaper, faster, more identity-stable for iteration; NB Pro richer for painterly finals — are stable.*
