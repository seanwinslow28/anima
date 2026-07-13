---
name: prompt-how-much
description: How much to prompt an image or video model, by surface — image generation, image editing, compositing a character into a scene, and video (Seedance start+end vs single-frame). Distilled from the 2026-07-12 live Higgsfield prompt-ladder run (Sean's eye, ranked A/Bs). Use when writing or refining a prompt for Nano Banana / gpt-image / Seedance, deciding whether to add or cut detail, compositing a character into a background, driving a specific motion from a frame, chasing a flat-poster look, or diagnosing why a generated image/clip drifted, cropped, over-rendered, or under-moved. Triggers: "how much detail", "make the prompt shorter/longer", "over-prompting", "composite into", "place the character", "flat poster look", "why did it drift/crop/regenerate", "single-frame motion", "seedance prompt".
---

# How much to prompt — by surface

Full companions: [compositing doctrine](../../../docs/research/2026-07-12-compositing-doctrine.md) · [harness](../../../docs/research/2026-07-12-prompt-ladder-harness.md) · [decision card](../../../docs/architecture/prompt-decision-card.md). Every rule below is a ranked A/B from the live run, not a guess.

## The one-line rule per surface

| Surface | How much | Over-prompting's failure mode |
|---|---|---|
| **Image gen (scratch)** | more is fine — spend words on **composition, not identity** | literal-noun drift (name a katana → get a katana); no identity melt |
| **Image edit (identity)** | **terse — Rung 2 is the ceiling** | breaks framing + style register + hallucinates prose details (NOT the face) |
| **Compositing (char→scene)** | **~50–70 words; command scale + position, protect the bg** | verbose *scene* prose regenerates the background (flat → CGI) |
| **Video (start+end frames)** | **~80 words, action not mechanics** | `<30w` under-directs; `>150w` collapses; re-describing the subject is wasted (frames carry it) |
| **Video (single frame)** | **match technique to motion** (see below) | wrong technique → under-travelled motion or a frozen subject |

## The recipes

- **Flat poster look (gpt-image):** it renders painterly by default. Add the anti-rendering block — *"clean flat color shapes, almost no visible outlines, hard-edged flat shadow shapes, no gradients, no rendered volume, no painterly texture, screenprint/vector flatness, every edge a hue/value break not a drawn line."*
- **Image edit:** role-tag the reference ("Image 1 is the character reference"), enumerate the identity-lock to HOLD, state the ONE change, end with *"Do not add any text."* Stop. More prose breaks framing/style, it doesn't help identity.
- **Compositing:** "Image 1 is the character. Image 2 is the background scene." + identity-lock + **one scale clause** ("small, dwarfed by the sky" / "medium" / "close-up") + **one position clause in words** ("left, near the porch") + "keep Image 2 unchanged" + anti-text. **Never re-describe the scene.** For a specific pose, hand-draw a **solid** silhouette (carries pose only — still command size in text); an outline sketch fails.
- **Video single-frame:** the prompt is the *only* steering (no end frame). **Big body moves** → strong terse imperative, and **drop any "settle/hold/hangs a beat/then descends" language** (it dampens the motion). **Throws/directional** → vivid ~80w description. **Effects/bursts** → evocative verbs ("erupts a geyser"), not step-by-step mechanics (read literally). **A static subject won't move while an effect fires — pair every effect with a full motion beat the subject performs** (sprint → jump → strike → land, *then* it bursts). A **rainbow liquid geyser** beats discrete particles. Seedance can generate objects/effects not in the frame.
- **Locked vs free camera = a creative dial.** "fixed camera, locked tripod" → one clean continuous shot. **Drop it and name shots/angles** (whip-pan, low-angle, hero push-in, hard cut, slow-mo) → Seedance directs a genuine **multi-shot cut sequence** from a single frame (identity + register survive the cuts).
- **Video (any):** lead with a genre anchor, one camera line ("fixed camera, locked tripod" — or drop it to let the camera move/cut), and **never use negation** (Seedance has no negative-prompt support).

## Higgsfield CLI quick-ref

```bash
higgsfield generate create nano_banana_flash --prompt "$(cat p.txt)" --image char.png [--image bg.png] --aspect_ratio 16:9 --resolution 2k --json --wait   # NB2 edit/composite, ~2cr
higgsfield generate create gpt_image_2 --prompt "$(cat p.txt)" --quality high --resolution 2k --aspect_ratio 16:9 --json --wait                              # flat-poster gen, ~7cr
higgsfield generate create seedance_2_0 --prompt "$(cat p.txt)" --start-image s.png [--end-image e.png] --mode fast --resolution 720p --duration 15 --generate_audio false --json --wait  # video, ~3.5cr/s, 4–15s
```
Always write prompts to `.txt` and pass `--prompt "$(cat p.txt)"` (apostrophes break inline). `higgsfield generate cost <model> …` is a $0 pre-check.
