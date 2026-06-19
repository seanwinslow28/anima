# Act 2 Seedance Prompts — v2 (Prompt-Science Rewrite)

> **Purpose:** Manual-generation prompts ready to paste into the [fal.ai Seedance 2.0 Fast playground](https://fal.ai/models/bytedance/seedance-2.0/fast/image-to-video). Each shot rewrites the v1 prompt from [act2-seedance-shot-list.md](../../pencil-test/act2-seedance-shot-list.md) using the `image-generator-prompt-science` skill's video-model framework.
>
> **Companion docs:**
> - [act2-seedance-shot-list.md](../../pencil-test/act2-seedance-shot-list.md) — original v1 spec, fallback strategies, assembly order, QA gates (still authoritative for everything except wording)
> - [2026-04-27-seedance-manual-handoff.md](2026-04-27-seedance-manual-handoff.md) — paused-state context, anchor paths, durations, last-batch seeds, fal.media cached URLs

**Created:** 2026-04-27 • **Branch:** `ultraplan/seedance-pipeline`

---

## Why a v2

The v1 prompts were written before the first batch ran. They average 70–95 words and lean on three over-constraint patterns that video models specifically struggle with:

| v1 pattern | What goes wrong | v2 fix |
|---|---|---|
| Verbatim "Style Anchor Block" (3 sentences, ~30 words) inside every prompt | Re-asserts aesthetic the start/end frames already prove. Eats prompt budget. | Compress to one **medium + style** sentence at the top. The full anchor block is available below as an optional preamble if a clip drifts. |
| `"Maintain pencil line quality, graphite shading, paper grain texture, consistent line weight throughout. Visible construction marks."` repeated each shot | Layered repetition causes the model to over-emphasize line/grain texture, sometimes producing "etched" frames where lines feel re-traced rather than animated. | One short guardrail line per shot. |
| `"Smooth 4-second walking interpolation."` / `"Smooth 3-second materialization interpolation."` | Frame-count and "interpolation" jargon micromanage timing the model already controls via the duration parameter. | Removed entirely. Duration is set in the API form, not the prompt. |
| `"Single slow camera push-in, no other movement."` followed by sentences describing other things moving | Contradicts itself — camera moves AND character pose changes are two motions. | One **camera instruction** sentence; per-shot risk notes in the v1 shot list still apply. |

The v2 rewrites also follow the video-model rule from `image-generator-prompt-science`: **describe WHAT happens with plain action verbs; let the model interpolate HOW.**

**Word count target:** 50–80 words per shot (down from 70–95). Shorter prompts produce more fluid motion in Seedance per the research findings.

---

## Continuity Rules (still locked — do NOT relax)

These are encoded into the rewrites. If you regenerate manually and Seedance drops one, prepend the relevant line:

- **Walking sequence (W1, W2, W3):** Sean is **clean-shaven**.
- **Desk sequence (S0 onward):** Sean has a **subtle 5-o'clock-shadow stubble**. S0 is the shot where it grows in.
- **AI Companion:** terracotta-orange loaf creature, dot eyes, stubby arms.
- **Wardrobe (locked, no variation):** dark navy crew-neck T-shirt, cool gray cuffed jeans, gray-cream sneakers.
- **No stylus in Sean's hand in Act 2.** The pencil visible on the desk in `transition_pulled_in.png` and `pre_pulled_in.png` is an incidental desk prop, not held. (This is the inverse of the Act 1 stylus rule.)

---

## Optional Style Preamble (drop in only if a shot drifts)

If a regenerated clip starts losing pencil-test fidelity (Seedance slipping toward digital cleanness), prepend this verbatim block to the v2 prompt and re-run:

```
Hand-drawn pencil animation on cream paper. Maintain pencil line quality,
graphite shading, paper grain texture, and consistent line weight
throughout. Visible construction marks. No digital effects, no
photorealistic rendering, no glossy polish.
```

Otherwise: skip it. The start/end anchors carry the aesthetic on their own.

---

## fal.ai Playground Settings (apply to every shot below)

| Setting | Value |
|---|---|
| Model | `bytedance/seedance-2.0/fast/image-to-video` |
| Resolution | `720p` |
| Duration | per shot (see card; **API minimum is 4s** — clamp 3s shots to 4s, the extra second is trimmed in assembly) |
| Generate audio | **off** |
| Image (start) | start anchor PNG (per shot) |
| End image | end anchor PNG (per shot) |
| Aspect ratio | inherited from start frame; ignored in start+end mode |

---

## Shot Cards (assembly order)

Each card gives you: anchors, duration, the v2 prompt in a copy-paste block, and a one-line note on what changed from v1.

---

### W1 — Walk Film (Seedance, 4s, low risk)

- **Start:** `runs/act2-exploration/concepts/zone1/film.png`
- **End:** `runs/act2-exploration/concepts/bridges/film_to_animation.png`
- **Duration:** 4s

```
Hand-drawn pencil animation on cream paper. Sean walks steadily left to
right at a relaxed pace, head turning slightly to take in the floating
Film props around him. The props stay still; only Sean moves. Fixed
camera, even diffuse lighting. Keep pencil line quality, paper grain,
and visible construction marks. No digital effects, no anime, no camera
jitter.
```

> *Cuts:* "mid-stride throughout" (model handles gait), "Smooth 4-second walking interpolation" (timing belongs to the duration param), redundant style asserts.

---

### W2 — Walk Animation (Seedance, 4s, low risk)

- **Start:** `runs/act2-exploration/concepts/bridges/film_to_animation.png`
- **End:** `runs/act2-exploration/concepts/bridges/animation_to_ai.png`
- **Duration:** 4s

```
Hand-drawn pencil animation on cream paper. Sean keeps walking left to
right at the same steady pace. The Film props on the left lighten and
fade away as he passes; the Animation props (figure studies, light box,
animation books) brighten around him, then begin to fade as the AI
headlines start to emerge on the right edge. Fixed camera, even diffuse
lighting. Keep pencil line quality and paper grain. No digital effects,
no anime, no camera jitter.
```

> *Cuts:* "via lightening pencil pressure" (the visible behavior is "lighten and fade" — the mechanism is implementation detail). Frame-count language gone.

---

### W3 — Walk AI (Seedance, 4s, low risk)

- **Start:** `runs/act2-exploration/concepts/bridges/animation_to_ai.png`
- **End:** `runs/act2-exploration/concepts/zone1/ai_discovery.png`
- **Duration:** 4s

```
Hand-drawn pencil animation on cream paper. Sean keeps walking left to
right at the same steady pace, eyebrow lifting and head tilting with
growing curiosity. The remaining Animation props fade away; the
hand-lettered AI news clippings (ChatGPT, Karpathy, Vibe Coding,
Anthropic, Gemini) solidify around him. Fixed camera, even diffuse
lighting. Keep pencil line quality and hand-lettered text quality. No
clean digital type, no anime, no camera jitter.
```

> *Adds:* "no clean digital type" — Seedance has been known to clean up hand-lettered text into vector-feeling letterforms; this calls it out.

---

### S0 — Arrive at Desk (Seedance, 4s, **HIGHEST RISK morph**)

- **Start:** `runs/act2-exploration/concepts/zone1/ai_discovery.png`
- **End:** `runs/act2-exploration/concepts/zone3/sit_down.png`
- **Duration:** 4s
- **Stubble:** grows in during this shot — Sean ends with a subtle 5-o'clock shadow.

```
Hand-drawn pencil animation on cream paper. The floating AI headlines
dissolve away as the desk, laptop, second monitor, coffee mug, and
chair sketch themselves into place. Sean shifts from a mid-stride walk
into a seated working pose at the desk. A faint 5-o'clock-shadow
stubble grows in on his jaw as time passes. Fixed camera, even diffuse
desk lighting. Keep pencil line quality and paper grain. No digital
effects, no anime, no camera jitter.
```

> *v1 fallback still stands:* if Seedance breaks identity here, hard-cut from `ai_discovery.png` to `sit_down.png` with a 0.3s cross-fade in FFmpeg post.

---

### T0 — Push-in to Terminal (Seedance, 4s, medium risk — camera + pose change)

- **Start:** `runs/act2-exploration/concepts/zone3/sit_down.png`
- **End:** `runs/act2-exploration/concepts/zone3/terminal_closeup_empty.png`
- **Duration:** 4s

```
Hand-drawn pencil animation on cream paper. Slow camera push-in toward
the laptop screen. Sean's hands settle onto the keyboard as the camera
moves; the dark cross-hatched terminal window grows to fill the frame
while the desk surroundings recede off-frame. One slow camera push,
nothing else moves. Even diffuse desk lighting. Keep pencil line
quality and cross-hatching. No digital effects, no anime, no camera
jitter.
```

> *v1 fallback still stands:* if jitter appears, split into S1.5 (Sean settles hands, no camera move) + T0 (pure camera push-in, Sean static).

---

### T2 — Companion Appears (Seedance, 3s creative → 4s API, **lowest-risk shot**)

- **Start:** `runs/act2-exploration/concepts/zone3/terminal_closeup_empty.png`
- **End:** `runs/act2-exploration/concepts/zone3/terminal_closeup_companion.png`
- **Duration:** 4s (API minimum; trim to 3s in assembly — invisible because hard cut follows)

```
Hand-drawn pencil animation on cream paper. The terracotta-orange
loaf-shaped AI companion (dot eyes, stubby arms) sketches itself into
existence inside the dark cross-hatched terminal window. A few small
pencil sparkle marks pop around it as it forms. The terminal text
shifts from "c:\>_ what is..." to "c:\>_ hello, sean...". Fixed
camera, even lighting from the laptop screen. Keep cross-hatching
density and hand-lettered text. No clean digital type, no anime, no
camera jitter.
```

> *Adds:* explicit companion design recap (loaf, dot eyes, stubby arms) for safety. The end frame already shows the companion, but Seedance has been seen to slim down or simplify the silhouette mid-form. This explicit re-anchor protects it.

---

### TR — Hand Grab (Seedance, 3s creative → 4s API, medium risk, HARD CUT from T3)

- **Start:** `runs/act2-exploration/concepts/bridges/pre_pulled_in.png`
- **End:** `runs/act2-exploration/concepts/zone3/transition_pulled_in.png`
- **Duration:** 4s (API minimum; trim to 3s in assembly)

```
Hand-drawn pencil animation on cream paper. The companion's terracotta
arm fully extends out of the laptop screen; its small hand reaches
across and grabs Sean's right hand. Sean leans forward, eyes widening,
as he's tugged toward the screen. A few pencil motion lines accentuate
the pull. Fixed camera, even desk lighting with a cool blue screen-glow
on Sean's face. Keep pencil line quality and paper grain. No digital
effects, no anime, no camera jitter.
```

> *Note:* "tugged toward" is intentionally a softer verb than "pulled" — Seedance over-pulls Sean clear out of frame when given strong action verbs paired with a 3s window.

---

### REV — The Revelation (Seedance, 5s, **HIGHEST RISK clip overall**)

- **Start:** `runs/act2-exploration/concepts/zone3/transition_pulled_in.png`
- **End:** `runs/act2-exploration/concepts/zone3/revelation.png`
- **Duration:** 5s

```
Hand-drawn pencil animation on cream paper. The companion pulls Sean
forward; the desk and laptop dissolve into open cream-paper space.
Hand-lettered concept words (VIBE CODING, AGENTS, PIPELINES, GENERATE)
and small pencil-drawn diagrams (code editor, neural-net nodes,
prompt-to-output arrows) sketch themselves in around Sean and the
companion as a mind-map. Sean rises upright, arms spreading outward in
a moment of revelation. The companion floats beside him. Fixed camera,
even diffuse lighting. Keep pencil line quality and hand-lettered text.
No digital effects, no anime, no camera jitter.
```

> *v1 fallbacks still stand:* (1) drop to 4s; (2) generate intermediate `bridges/being_pulled.png` and split into REV1 (3s) + REV2 (3s). Big visual leap over 5s is the documented risk.

---

### PM — Grab Kanban (Seedance, 3s creative → 4s API, low risk, HARD CUT from REV)

- **Start:** `runs/act2-exploration/concepts/zone4/pm_role.png`
- **End:** `runs/act2-exploration/concepts/bridges/pm_role_grabbed.png`
- **Duration:** 4s (API minimum; trim to 3s in assembly)

```
Hand-drawn pencil animation on cream paper. Sean reaches forward,
plucks one sticky-note card from the IN PROGRESS column of the Kanban
board with his right hand, and brings it down to chest height. His
expression softens into a small satisfied half-smile. The companion
floats steadily camera-right; the rest of the board stays still. Fixed
camera, even diffuse lighting. Keep hand-lettered text on the board
and pencil line quality. No digital effects, no anime, no camera
jitter.
```

> *Cuts:* "focused selection to a small satisfied half-smile" → "softens into a small satisfied half-smile" (one expression beat is enough; Seedance handles the in-between).

---

### PB — Pull Back (Seedance, 5s, second-highest risk — camera + emerging content)

- **Start:** `runs/act2-exploration/concepts/bridges/pm_role_grabbed.png`
- **End:** `runs/act2-exploration/concepts/zone4/final_panorama_v3_a.png`
- **Duration:** 5s

```
Hand-drawn pencil animation on cream paper. Slow camera pull-back from
the PM scene, gradually revealing the wider workshop panorama — Film
camera, Animation reference materials, AI news clippings, and agentic
workflow diagrams arranged across the cream paper. Sean and the
companion stay locked in their positions camera-right as the world
widens around them. One slow pull-back, nothing else moves. Even
diffuse lighting. Keep pencil line quality and hand-lettered text. No
digital effects, no anime, no camera jitter.
```

> *v1 fallback still stands:* if jitter appears, hard-cut from `pm_role_grabbed.png` to `final_panorama_v3_a.png` with a 0.4s cross-fade in FFmpeg.

---

## What's NOT in this doc (intentionally)

| Shot | Why not |
|---|---|
| **S1, T1, T3, FIN** | FFmpeg static holds — no Seedance call. T1 also gets a custom blinking-cursor overlay built from two variant frames. See [act2-seedance-shot-list.md §S1, §T1, §T3, §FIN](../../pencil-test/act2-seedance-shot-list.md) for the FFmpeg recipes. |
| **Hard cuts** (T2→T3, T3→TR, REV→PM) | Pure assembly cuts — no generation step. |

---

## Workflow recommendation

1. **Walking sequence first (W1 → W2 → W3).** All low-risk, all 4s, all clean-shaven Sean. Generate them back-to-back in one sitting; if any one drifts, the prompt science is solid before you tackle the harder shots.
2. **Lowest-risk inside the desk sequence next: T2.** Locked camera, locked composition, only the companion materializes. If T2 looks great, you've validated the full Sean+companion+terminal pipeline.
3. **PM and TR next (medium-risk).** Both are short (3s creative), both have one focused action.
4. **Then the harder ones in order: T0, S0, PB, REV.** S0 and REV are the documented "if these break, fall back" shots. Try the v2 prompt first — if Seedance breaks identity or fidelity, drop to the v1 fallback strategies (in the shot list).
5. **Drop winning MP4s into:** `runs/act2-seedance-2026-04-27/seedance/` as `<SHOT>_attempt_<NN>.mp4` (e.g., `W1_attempt_02.mp4`). The orchestrator's controller resumes from there at Task 5 (frame extraction).

---

## Per-shot escalation if v2 underperforms

If a v2 prompt gives worse results than the v1 it replaced, escalate in this order:

1. **Re-run with the same v2 prompt** (Seedance is stochastic — same prompt, new seed often clears one-off drift).
2. **Prepend the optional Style Preamble** (above) to the v2 prompt.
3. **Drop back to the v1 prompt** for that single shot — the v1 wording is in [2026-04-27-seedance-manual-handoff.md §4](2026-04-27-seedance-manual-handoff.md). Don't burn budget chasing a v2 win on a shot where v1 worked.
4. **Invoke the v1 shot list's fallback strategy** (split, cross-fade, hard cut) per the per-shot risk notes.

The v2 rewrites are an optimization, not a replacement. The v1 prompts are the safety net.
