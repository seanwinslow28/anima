---
name: prompt-how-much
description: How much to prompt an image or video model for ANY art style, per surface. Use when writing or refining an image or video prompt, unsure whether to add or cut detail, matching a target art style or register, compositing or placing a character into a background, driving a motion from a single frame or start+end frames, or diagnosing why a generation drifted, cropped, over-rendered, under-moved, froze, or lost identity (Nano Banana, gpt-image, Seedance, Higgsfield). Skip for engineering an LLM or system prompt (use prompt-engineering); for the full 7-layer image-prompt construction framework and refinement tips (use image-generator-prompt-science); for the canonical Seedance v4 video template (use seedance-prompting); for actually running a generation (use the gemini / openai / higgsfield generation skills).
---

# Prompt How Much

## Purpose

Decide how much to prompt — and which single lever to pull — for each image/video generation surface, in **any** art style. The mechanics are style-agnostic; the target style is a parameter you **name**, never over-describe. Pull the right lever per surface and stop: over-prompting fails by competing with what a reference already provides, or by *describing* a style/motion instead of *naming* it.

## When to Use

- Writing or refining a prompt for image generation, image editing, compositing, or video motion
- Unsure whether to add or cut detail from a prompt
- Matching a specific art style or register (flat, pencil, painterly, pixel, watercolor, 3D…)
- Compositing or placing a character into a pre-made background/scene
- Driving a motion from a single start frame, or between start+end frames
- Diagnosing a result that drifted, cropped, over-rendered, under-moved, froze, or lost identity
- **Not for:** engineering an LLM/system prompt → `prompt-engineering`; the full 7-layer image-prompt construction framework + refinement tips → `image-generator-prompt-science`; the canonical Seedance v4 template → `seedance-prompting`; actually running a generation → the `gemini-*` / `openai-image-gen` / `higgsfield-*` skills

## Examples

**Example 1 — the composite keeps making the character huge and centered**
> User: "Every composite drops the character big in the middle. I want him tiny in the corner of the scene."
> Claude [prompt-how-much]: Compositing defaults to a large center hero — **scale and position are never inferred**. Add one scale clause ("small, tiny in the frame") + one position clause in words ("far back, left of the tree"), keep "Image 2 unchanged," and don't re-describe the scene.

**Example 2 — the single-frame clip barely moves**
> User: "The subject just stands there while the effect fires, and my big jump barely leaves the ground."
> Claude [prompt-how-much]: Two levers. (1) **Pair the effect with a subject motion** — give a full beat (approach → act → land), *then* the effect. (2) For the jump, use a **terse imperative** and **cut any "hold/settle/then descends" words** — that language dampens the motion.

## The through-line

In every surface: a **reference image carries identity**; **the text carries only what is changing or new** (the edit, the placement, the motion) **plus one named style token**. Drop your register's own vocabulary into every `[STYLE]` slot below.

## One-line rule per surface

| Surface | Reference | How much to prompt | Over-prompting's failure mode |
|---|---|---|---|
| **Image gen (scratch)** | none | more is fine — spend words on **composition, not identity/style-prose** | literal-noun drift (name an object → get exactly it); no identity melt |
| **Image edit (identity)** | 1 (character) | **terse — lock, ONE change, style token, stop** | breaks framing + drifts style + hallucinates prose details (NOT the face) |
| **Compositing (char→scene)** | 2 (char + bg) | **~50–70 words; command scale + position, protect the background** | verbose *scene* prose regenerates the background |
| **Video (start+end)** | 2 frames | **~80 words, action not mechanics** | too few → under-directs; too many → collapses; re-describing the subject is wasted |
| **Video (single frame)** | 1 frame | **match technique to the motion type** | wrong technique → under-travelled motion or a frozen subject |

## Per-surface levers

- **Image gen (scratch):** detail doesn't hurt — spend it on composition/completeness. **Name the style; don't narrate the render.** Every incidental noun gets drawn literally.
- **Hitting a target style (ANY style) — the universal recipe:** models drift to a built-in default render. Pin your surface by **naming it positively AND negating the render modes you don't want** — the `no <…>` half is what stops the drift:
  - *Flat/vector:* "flat color shapes, hard-edged flat shadows, screenprint flatness — no gradients, no rendered volume, no outlines."
  - *Pencil-test:* "graphite line, cross-hatch shadow, cream paper — no flat vector fill, no digital gradients."
  - *Painterly:* "visible brushwork, soft tonal transitions — no hard vector edges, no flat cel fill."
  - *Pixel-art:* "hard pixel grid, limited palette, dithering — no anti-aliasing, no soft gradients."
- **Image edit:** role-tag the reference (*"Image 1 is the character reference"*), enumerate the identity-lock to HOLD, state the **ONE** change, append `[STYLE]`, end with *"Do not add any text."* Then stop.
- **Compositing:** *"Image 1 is the character. Image 2 is the background scene."* + identity-lock + **one scale clause** (size is not inferred) + **one position clause in words** (beats a drawn marker) + *"keep Image 2 unchanged"* + `[STYLE]` + anti-text. **Never re-describe the scene.** For a specific pose, hand-draw a **solid** silhouette (carries pose only — still command size in text).
- **Video motion:** frames carry identity — the prompt is for motion. **Match technique to motion:** big body moves → terse imperative, **cut "settle/hold/then descends"** (it dampens); throws/directional → vivid ~80w; effects → evocative verbs, not step-by-step mechanics; small moves → anything. **Pair every effect with a subject motion** (static subject stays frozen). The model can **generate objects/effects not in the frame**. **Locked vs free camera is a dial:** "fixed camera, locked tripod" = one shot; drop it + name shots/angles (whip-pan, low-angle, push-in, hard cut, slow-mo) = a multi-shot cut sequence. **Lead with a genre anchor; use NO negation** (video models here have no negative-prompt support — the opposite of the image path).

## Tooling (Higgsfield CLI) + model notes

Model-specific facts behind the universal rules: **NB2** (`nano_banana_flash`) holds identity so well that over-prompting an edit breaks *framing/style*, not the face; **gpt-image** (`gpt_image_2`) renders painterly by default (the anti-render clause matters most there); **Seedance** (`seedance_2_0`) has no negative-prompt support.

```bash
higgsfield generate create nano_banana_flash --prompt "$(cat p.txt)" --image char.png [--image bg.png] --aspect_ratio 16:9 --resolution 2k --json --wait   # edit / composite
higgsfield generate create gpt_image_2 --prompt "$(cat p.txt)" --quality high --resolution 2k --aspect_ratio 16:9 --json --wait                              # gen from scratch
higgsfield generate create seedance_2_0 --prompt "$(cat p.txt)" --start-image s.png [--end-image e.png] --mode fast --resolution 720p --duration 15 --generate_audio false --json --wait  # video, 4–15s
```
Write prompts to a `.txt` and pass `--prompt "$(cat p.txt)"` (apostrophes break inline). `higgsfield generate cost <model> …` is a $0 pre-check.

## Success Criteria

- [ ] Identified the surface (gen / edit / composite / video-interp / video-single-frame) before choosing lever count
- [ ] Style is **named** with a token (+ anti-render clause if pinning a non-default surface), not narrated
- [ ] **Edit** prompt = role-tag + identity-lock + ONE change + style + anti-text, and nothing more
- [ ] **Composite** prompt carries an explicit scale clause AND a position clause, keeps "Image 2 unchanged," and never re-describes the scene
- [ ] **Video** prompt matches technique to motion type, pairs any effect with a subject motion, and uses no negation
- [ ] Chose locked vs free camera deliberately

## Copy/Paste Ready

```
"How much detail should this prompt have?"
"Make this image/video prompt shorter (or longer)"
"Why did my generation drift / crop / over-render / freeze / lose the character?"
"How do I composite this character into that background at the right size?"
"How do I drive this motion from a single frame?"
"How do I hit a <flat/pencil/painterly/pixel> style and stop it rendering default?"
```
