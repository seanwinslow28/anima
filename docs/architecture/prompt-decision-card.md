# Prompt decision card — how much to prompt, by surface

*2026-07-12. A one-page answer to "how much should I prompt?" for each generation surface anima uses, distilled from the live prompt-ladder run ([`runs/2026-07-11-prompt-ladder-grandmaster/`](../../runs/2026-07-11-prompt-ladder-grandmaster/), gitignored). Every rule here is a ranked A/B, not a borrowed claim. Companion docs: the [compositing doctrine](../research/2026-07-12-compositing-doctrine.md) and the [reusable harness](../research/2026-07-12-prompt-ladder-harness.md).*

---

## The one-line rule per surface

| Surface | Reference? | How much to prompt | The failure mode of over-prompting |
|---|---|---|---|
| **Image gen (from scratch)** | none | **More is fine — spend words on composition, not identity** | literal-noun drift (name a katana, get a katana) — but no identity melt (nothing to melt) |
| **Image edit (identity)** | 1 (the character) | **Terse. Rung 2 is the ceiling.** | breaks framing + style-register + hallucinates prose details (NOT the face — NB2 holds identity) |
| **Compositing (char → scene)** | 2 (char + background) | **Terse, ~50–70 words. Command scale + position, protect the background.** | verbose *scene* prose regenerates the background (flat → CGI) |
| **Video (Seedance, start+end)** | 2 frames | **~80 words, action not mechanics.** | `<30w` under-directs; `>150w` collapses; the frames carry identity, so re-describing the subject is wasted words |
| **Video (Seedance, single frame)** | 1 frame | **match technique to motion: terse imperative for big body moves, vivid description for effects/throws** | wrong-technique = under-travelled motion (or a frozen subject) |

---

## Image generation (from scratch)

There's no reference to compete with, so detail doesn't hurt identity — it *builds* it. But two things learned:

- **Spend words on composition and completeness, not the character.** Detail fixed framing (a terse prompt clipped the figure's feet; the detailed one gave a clean full body). The bigger lever was the *pose/composition* brief, not verbosity.
- **Watch literal-noun drift.** Every incidental object you name, the model draws exactly — asking for a "bokken" in an over-written prompt produced a bladed katana. Name only what you mean.
- **Flatness (or any surface register) is prompt-reachable.** gpt-image-2 rendered painterly-anime by default; adding **anti-rendering negatives** ("no gradients, no rendered volume, no outlines; hard-edged flat shadow shapes; screenprint/vector flatness; every edge a hue/value break, not a drawn line") flipped it to true flat poster-art in one shot. That negative block is the reusable flat-poster recipe.

## Image edit (single-reference identity)

**The reference is the identity; the text is the diff.** State the ONE change, enumerate the identity-lock to hold, role-tag the reference ("Image 1 is the character reference"), end with the anti-text clause — and stop. **Rung 2 (~50 words) is the ceiling.** The ladder was decisive: rungs 1–3 near-identical and correct; the 150-word rung visibly degraded — it broke the full-body framing (cropped to a close-up), drifted off the flat register into rendered comic shading, and hallucinated sweat + musculature from the prose. On NB2, over-prompting doesn't melt the face (its reference-hold is robust) — it corrupts **composition and style** and invents detail.

## Compositing (character into a pre-made scene)

Full doctrine: [compositing doctrine](../research/2026-07-12-compositing-doctrine.md). The card version:

1. Role-tag both references ("Image 1 is the character. Image 2 is the background scene.").
2. Enumerate the identity-lock.
3. **Command scale** — terse defaults to a large center hero; say "small, dwarfed by the sky" for negative space.
4. **Command position in words** — "left, near the porch" beats a drawn placeholder shape.
5. **Protect the background** — one "keep Image 2 unchanged" clause; **never re-describe the scene** (verbose scene prose regenerates the plate into CGI).
6. For a **specific/dynamic pose**, draw a **solid** silhouette (carries pose) and still command size in text (the silhouette does NOT carry size).
7. ~50–70 words total. Longer only hurts.

## Video — Seedance, start+end interpolation

- **~80 words is the sweet spot.** The 30-word clip under-directed; the 147-word clip stayed coherent but materialized every incidental noun it named (dust + cracked ground appeared) — the same literal-drift tell; past ~150 the doctrine says it collapses.
- **The start+end frames carry identity — the prompt is for motion.** Re-describing the subject was neutral-to-wasteful: identity held regardless because the anchor frames dominate. Spend the words on the action, not the character.
- **Lead with a genre anchor, one camera line ("fixed camera, locked tripod"), action-focused (what happens, not body mechanics), and NO negation** (Seedance has no negative-prompt support — the opposite of the NB2 image path).

## Video — Seedance, single start frame (no interpolation)

**Single-frame image-to-video works** — Seedance drives a target motion from ONE frame + prompt, holding identity + flat style, and can even spawn objects/effects (a candy burst, a flung staff) that aren't in the frame. You don't always need to author an end frame. But the winning prompt technique is **motion-dependent** — there is no one shape:

- **Large body displacement (leap, fall):** a **strong terse imperative** wins ("explodes upward into a high leap"). **Drop any "settle / hold / hangs a beat / then descends" language** — the model obeys it and *reduces* the motion. The 80-word "doctrine" prompt lost the leap for exactly this reason (Sean's pick: the terse leap).
- **Throw / directional limb motion:** the **vivid 80-word description** wins — the evocative follow-through drove the best throw (Sean's pick, "no question"). Opposite of the leap: here the detail helped.
- **Effects / bursts:** vivid evocative verbs ("erupts a geyser, over-saturated fountain") drive the biggest effect; **step-by-step mechanics is read literally** (a contained "pour" vs an explosion). **Known limit:** single-frame i2v does *not* yet nail "static subject holds while the effect erupts around him" — the effect fires but the subject freezes. Unsolved; needs an end-frame or a better prompt.
- **Small contained motion (throw arm, catch):** technique matters least — most shapes work.

**Rule of thumb:** the prompt is the *only* steering (no end frame to aim at), so say exactly the motion you want in the register that motion lives in — imperative and lean for big physical moves, vivid and specific for throws and effects — and never include words that describe the motion *ending* or *settling*.

### Two closing discoveries (the burst rework, 15s clips)

- **Pair every effect with an action the subject performs.** A static "hold while it bursts" freezes the subject. Give the subject a full motion beat in the same clip (e.g., sprint → jump → strike → land, *then* the piñata bursts) and both the body and the effect animate. **A rainbow *liquid* geyser** ("liquid accelerates outward and downward, wide arcing spray, thins as it empties") reads far better than discrete particles for a burst.
- **Locked vs free camera is a creative dial.** Keep "fixed camera, locked tripod" for one clean continuous shot. **Drop it and name shots/angles** (whip-pan, low-angle track, hero push-in, hard cut, slow-mo) and Seedance will **direct a genuine multi-shot, multi-angle cut sequence** from a single frame — a Tartakovsky-style edit, not just a drifting camera. Identity + register survive the cuts.
