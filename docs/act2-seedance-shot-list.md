# Act 2 — Seedance Shot List

> Round 3 deliverable. Maps the locked 11-beat sheet (`runs/act2-exploration/concepts/round2-decisions.md`) into 10 Seedance interpolation clips + 4 holds. Each Seedance shot has a start frame, end frame, duration, and draft prompt ready to feed `bytedance/seedance-2.0/image-to-video` via fal.ai.
>
> **Status:** anchor frames complete (Round 3). Seedance generation is the next phase, NOT executed in Round 3.
>
> **Supersedes:** `docs/seedance-production-plan.md` (frozen, written before Round 2 beat sheet existed)

**Created:** 2026-04-26 • **Branch:** `ultraplan/seedance-pipeline`

## Summary

| | Count | Runtime |
|---|---|---|
| Seedance interpolation clips | 10 | ~40s |
| Holds (FFmpeg, no Seedance) | 4 | ~11s |
| Hard cuts | 3 | 0s (instant) |
| **Total Act 2 runtime** | | **~50s** |

**Estimated Seedance cost (720p, 5s @ $0.30/s standard, ~$0.24/s fast):**
- Standard tier: ~$12 for all 10 clips
- Fast tier: ~$10 for all 10 clips
- Recommended: Fast tier first pass; switch to Standard for any clips that fail identity preservation

## Style Anchor Block (reuse verbatim in every Seedance prompt)

```
Hand-drawn pencil animation on cream paper. Maintain pencil line quality,
graphite shading, paper grain texture, and consistent line weight throughout.
Visible construction marks. No digital effects, no photorealistic rendering,
no glossy polish.
```

## Camera Discipline (Seedance research-derived rules)

- **One camera instruction max per shot** — multiple movements produce jitter
- Default: "Fixed camera, locked tripod" unless the shot is a deliberate move
- Avoid: "cinematic", "4K", "glow", "glimmer", "epic", unqualified "fast"
- Always include: "Even, diffuse lighting" or shot-specific lighting (the single biggest quality lever per the research findings)

## Production Constraints (fal.ai API behaviors discovered in execution)

> Added 2026-04-27 after first execution batch. Update if API behavior changes.

- **fal.ai Seedance 2.0 minimum duration is 4s.** Durations below 4s are rejected by the API even though the model card lists 4–15. T2, TR, and PM are creatively spec'd at 3s below; in execution they are clamped to 4s and the extra second is trimmed in FFmpeg assembly. All three sit immediately before a hard cut, so the trim is invisible. **If regenerating manually via fal.ai's web UI, send 4s for those shots, not 3s — the playback duration in the final cut is still 3s.**
- **Locked tier for the first generation pass: Fast** (`bytedance/seedance-2.0/fast/image-to-video`, $0.24/s @ 720p). Per-shot escalation to Standard ($0.30/s) only if Fast fails identity/aesthetic on a specific shot.
- **Default resolution: 720p.** Native max for Seedance 2.0; output aspect inherits from the start frame (the `aspect_ratio` parameter is ignored in start+end frame mode).
- **`generate_audio: false` always** — no diegetic audio in scope; disabling cuts latency and avoids stripping a silent track downstream.

## Continuity Rules (locked across all shots)

- **Walking sequence (W1, W2, W3):** Sean is CLEAN-SHAVEN
- **Desk sequence (S0 onward):** Sean has subtle 5-o'clock shadow stubble
- **S0 (arrive at desk)** is the transition shot where stubble grows in — call this out in the prompt
- **AI Companion design:** terracotta-orange loaf creature, dot eyes, stubby arms — locked from companion turnaround references
- **Sean's wardrobe:** dark navy crew-neck T-shirt, cool gray jeans (cuffed), gray-cream sneakers — LOCKED, no variation
- **Stylus rule reversal vs Act 1:** the Act 1 "stylus in Sean's right hand" rule does **NOT** apply in Act 2. Sean's hands are on the keyboard, reaching, or empty. The pencil/stylus visible on the desk in `transition_pulled_in.png` and `pre_pulled_in.png` is an **incidental desk prop**, not held. Do not write Act 2 prompts that say "stylus in right hand."

## Shot List

### W1 — Walk Film (Seedance, 4s)

| Field | Value |
|---|---|
| **Type** | Seedance interpolation |
| **Start anchor** | `runs/act2-exploration/concepts/zone1/film.png` |
| **End anchor** | `runs/act2-exploration/concepts/bridges/film_to_animation.png` |
| **Duration** | 4s |
| **Aspect** | 16:9 (inherited from start frame) |

**Draft Seedance prompt (~70 words):**
```
Hand-drawn pencil animation on cream paper. Sean walks steadily from left
to right at a relaxed pace, mid-stride throughout, head turning slightly
to take in the floating Film props around him. The Film props remain
stationary; only Sean walks. Fixed camera, locked tripod. Even, diffuse
natural lighting. Maintain pencil line quality, graphite shading, paper
grain, consistent line weight, visible construction marks. No digital
effects. Smooth 4-second walking interpolation.
```

---

### W2 — Walk Animation (Seedance, 4s)

| Field | Value |
|---|---|
| **Type** | Seedance interpolation |
| **Start anchor** | `runs/act2-exploration/concepts/bridges/film_to_animation.png` |
| **End anchor** | `runs/act2-exploration/concepts/bridges/animation_to_ai.png` |
| **Duration** | 4s |
| **Aspect** | 16:9 |

**Draft Seedance prompt (~80 words):**
```
Hand-drawn pencil animation on cream paper. Sean continues walking left
to right at the same steady pace through the Animation world. The Film
props on the left fade out via lightening pencil pressure; the Animation
props (figure studies, light box, animation books) brighten then start
to fade as the AI headlines emerge on the right. Fixed camera, locked
tripod. Even, diffuse lighting. Maintain pencil line quality, paper
grain, consistent line weight. No digital effects. Smooth 4-second
walking interpolation.
```

---

### W3 — Walk AI (Seedance, 4s)

| Field | Value |
|---|---|
| **Type** | Seedance interpolation |
| **Start anchor** | `runs/act2-exploration/concepts/bridges/animation_to_ai.png` |
| **End anchor** | `runs/act2-exploration/concepts/zone1/ai_discovery.png` |
| **Duration** | 4s |
| **Aspect** | 16:9 |

**Draft Seedance prompt (~75 words):**
```
Hand-drawn pencil animation on cream paper. Sean continues walking left
to right at the same steady pace, eyebrow lifting and head turning in
growing curiosity. The remaining Animation props fade out; the AI news
clippings (ChatGPT, Karpathy, Vibe Coding, Anthropic, Gemini headlines)
solidify with hand-lettered text. Fixed camera, locked tripod. Even,
diffuse lighting. Maintain pencil line quality, hand-lettered text
quality, paper grain, consistent line weight. No digital effects.
Smooth 4-second walking interpolation.
```

---

### S0 — Arrive at Desk (Seedance, 4s)

| Field | Value |
|---|---|
| **Type** | Seedance interpolation |
| **Start anchor** | `runs/act2-exploration/concepts/zone1/ai_discovery.png` |
| **End anchor** | `runs/act2-exploration/concepts/zone3/sit_down.png` |
| **Duration** | 4s |
| **Aspect** | 16:9 |

**Draft Seedance prompt (~85 words):**
```
Hand-drawn pencil animation on cream paper. The floating AI news headlines
dissolve away from the frame as the desk, laptop, second monitor, coffee
mug, and chair materialize in their place. Sean transitions from a
mid-stride walk to a seated working pose at the desk. A subtle 5-o'clock
shadow stubble grows in on his face as time passes. Fixed camera, locked
tripod. Even, diffuse desk lighting. Maintain pencil line quality, paper
grain, consistent line weight. No digital effects. Smooth 4-second
transition interpolation.
```

> **Risk note:** This is the most ambitious Seedance morph in Act 2 (full environment swap + character pose change + stubble grow-in). If Seedance fails identity here, the fallback is a hard cut from `ai_discovery.png` to `sit_down.png` with a 0.3s cross-fade in FFmpeg post.

---

### S1 — Sitting Beat (Hold, 2s)

| Field | Value |
|---|---|
| **Type** | FFmpeg static hold (no Seedance) |
| **Frame** | `runs/act2-exploration/concepts/zone3/sit_down.png` |
| **Duration** | 2s |

Static hold to give the viewer breathing room before the terminal sequence. No motion needed.

```bash
ffmpeg -loop 1 -i sit_down.png -t 2 -r 24 -pix_fmt yuv420p shots/S1_sitting_hold.mp4
```

---

### T0 — Push-in to Terminal (Seedance, 4s)

| Field | Value |
|---|---|
| **Type** | Seedance interpolation |
| **Start anchor** | `runs/act2-exploration/concepts/zone3/sit_down.png` |
| **End anchor** | `runs/act2-exploration/concepts/zone3/terminal_closeup_empty.png` |
| **Duration** | 4s |
| **Aspect** | 16:9 |

**Draft Seedance prompt (~75 words):**
```
Hand-drawn pencil animation on cream paper. Camera pushes slowly forward
into the laptop screen on the desk. Sean's hands settle onto the keyboard
as the camera approaches. The laptop and dark cross-hatched terminal
window grow to fill the frame as the desk surroundings recede outside
the frame. Single slow camera push-in, no other movement. Even, diffuse
desk lighting. Maintain pencil line quality, graphite shading, paper
grain, consistent line weight. No digital effects. Smooth 4-second
push-in interpolation.
```

> **Risk note:** "Camera push-in" is one camera instruction (per Seedance rule), but combined with Sean's pose change it's two changes. If jitter appears, split into S1.5 (Sean settles hands, no camera move) + T0 (pure camera push-in, Sean static).

---

### T1 — Empty Terminal Hold (Hold, 2s)

| Field | Value |
|---|---|
| **Type** | FFmpeg static hold + cursor blink overlay |
| **Frame** | `runs/act2-exploration/concepts/zone3/terminal_closeup_empty.png` |
| **Duration** | 2s |

The held breath. Add a blinking pencil-block cursor in post (Procreate or After Effects: alternate the cursor block visible/invisible at 1Hz over the held image). Build the cursor blink from two frames — one with cursor, one without — and assemble in FFmpeg.

```bash
# Pseudo: cursor blink built from two variant frames
ffmpeg -framerate 2 -i cursor_blink_%d.png -t 2 -pix_fmt yuv420p shots/T1_terminal_hold.mp4
```

---

### T2 — Companion Appears (Seedance, 3s)

| Field | Value |
|---|---|
| **Type** | Seedance interpolation |
| **Start anchor** | `runs/act2-exploration/concepts/zone3/terminal_closeup_empty.png` |
| **End anchor** | `runs/act2-exploration/concepts/zone3/terminal_closeup_companion.png` |
| **Duration** | 3s |
| **Aspect** | 16:9 |

**Draft Seedance prompt (~75 words):**
```
Hand-drawn pencil animation on cream paper. The terracotta-orange AI
companion creature materializes inside the dark cross-hatched terminal
window. Small pencil sparkle marks appear around it as it forms. The
terminal text shifts from "c:\>_ what is..." to "c:\>_ hello, sean...".
Fixed camera, locked tripod. Even, diffuse lighting from the laptop
screen. Maintain pencil line quality, cross-hatching density, hand-
lettered text quality, paper grain. Consistent line weight. No digital
effects. Smooth 3-second materialization interpolation.
```

> **Low-risk shot:** Locked camera, locked composition, only one element (companion) appears. Should be Seedance's strongest type of shot.

---

### T3 — Sean POV Reaction (Hold + HARD CUT from T2, 2s)

| Field | Value |
|---|---|
| **Type** | FFmpeg static hold (no Seedance) |
| **Frame** | `runs/act2-exploration/concepts/zone3/terminal_pov_sean.png` |
| **Duration** | 2s |

**HARD CUT from T2.** This is a shot/reverse-shot — the camera flips from external view of the laptop to POV from inside the terminal looking out at Sean. Cannot be Seedance interpolated. Just an instant cut, then hold on Sean's surprised face for 2 beats.

```bash
ffmpeg -loop 1 -i terminal_pov_sean.png -t 2 -r 24 -pix_fmt yuv420p shots/T3_pov_hold.mp4
```

---

### TR — Hand Grab (Seedance, 3s, HARD CUT from T3)

| Field | Value |
|---|---|
| **Type** | Seedance interpolation |
| **Start anchor** | `runs/act2-exploration/concepts/bridges/pre_pulled_in.png` |
| **End anchor** | `runs/act2-exploration/concepts/zone3/transition_pulled_in.png` |
| **Duration** | 3s |
| **Aspect** | 16:9 |

**HARD CUT from T3.** Shot returns to external view of Sean at his desk.

**Draft Seedance prompt (~80 words):**
```
Hand-drawn pencil animation on cream paper. The companion's terracotta
arm fully emerges from the laptop screen and the small terracotta hand
reaches across and grabs Sean's right hand. Sean leans further forward
and his eyes widen as he is pulled toward the screen. A few pencil
motion-line marks accentuate the lean. Fixed camera, locked tripod.
Even, diffuse desk lighting with cool blue screen-light tint on Sean's
face. Maintain pencil line quality, paper grain, consistent line weight.
No digital effects. Smooth 3-second action interpolation.
```

---

### REV — The Revelation (Seedance, 5s)

| Field | Value |
|---|---|
| **Type** | Seedance interpolation |
| **Start anchor** | `runs/act2-exploration/concepts/zone3/transition_pulled_in.png` |
| **End anchor** | `runs/act2-exploration/concepts/zone3/revelation.png` |
| **Duration** | 5s |
| **Aspect** | 16:9 |

**Draft Seedance prompt (~95 words):**
```
Hand-drawn pencil animation on cream paper. Sean is pulled forward by
the companion. The desk and laptop dissolve into open cream paper space.
Hand-lettered concept words (VIBE CODING, AGENTS, PIPELINES, GENERATE)
and small pencil-drawn diagrams (code editors, neural network nodes,
prompt-to-output flow) emerge around Sean and the companion as a mind-
map. Sean stands upright with arms spreading outward in a moment of
revelation. The companion floats nearby. Fixed camera, locked tripod.
Even, diffuse lighting. Maintain pencil line quality, hand-lettered
text, paper grain, consistent line weight. No digital effects. Smooth
5-second revelation interpolation.
```

> **Highest-risk shot in Act 2.** Big visual leap (desk → opened mind-map world) over 5s. If Seedance breaks identity or feature consistency:
> 1. **First fallback:** drop duration to 4s
> 2. **Second fallback:** generate intermediate `bridges/being_pulled.png` (Sean and companion mid-transition, partially dissolved laptop, world opening) and split into REV1 (`transition_pulled_in.png` → `bridges/being_pulled.png`, 3s) + REV2 (`bridges/being_pulled.png` → `revelation.png`, 3s)

---

### PM — Grab Kanban (Seedance, 3s, HARD CUT from REV)

| Field | Value |
|---|---|
| **Type** | Seedance interpolation |
| **Start anchor** | `runs/act2-exploration/concepts/zone4/pm_role.png` |
| **End anchor** | `runs/act2-exploration/concepts/bridges/pm_role_grabbed.png` |
| **Duration** | 3s |
| **Aspect** | 16:9 |

**HARD CUT from REV.** Scene change from the abstract revelation space to the concrete PM/Kanban scene.

**Draft Seedance prompt (~85 words):**
```
Hand-drawn pencil animation on cream paper. Sean reaches forward to the
Kanban board, plucks one card from the IN PROGRESS column with his right
hand, and brings it down to chest height. His expression shifts from
focused selection to a small satisfied half-smile. The companion floats
steadily in the same position camera-right of Sean. The Kanban board
columns and sticky notes remain stationary. Fixed camera, locked tripod.
Even, diffuse lighting. Maintain pencil line quality, hand-lettered text
on the board, paper grain, consistent line weight. No digital effects.
Smooth 3-second action interpolation.
```

> **Low-risk shot:** Locked camera, only Sean's arm and one card move. Should hold identity well.

---

### PB — Pull Back (Seedance, 5s)

| Field | Value |
|---|---|
| **Type** | Seedance interpolation |
| **Start anchor** | `runs/act2-exploration/concepts/bridges/pm_role_grabbed.png` |
| **End anchor** | `runs/act2-exploration/concepts/zone4/final_panorama_v3_a.png` |
| **Duration** | 5s |
| **Aspect** | 16:9 |

**Draft Seedance prompt (~80 words):**
```
Hand-drawn pencil animation on cream paper. Camera pulls slowly backward
from the medium PM scene, revealing the wider workshop panorama with
Film camera, Animation reference materials, AI news clippings, and
agentic workflow diagrams arranged across the cream paper space. Sean
and the companion remain in their positions on the right side of the
frame as the panorama widens around them. Single slow camera pull-back,
no other movement. Even, diffuse lighting. Maintain pencil line quality,
hand-lettered text, paper grain. No digital effects. Smooth 5-second
pull-back interpolation.
```

> **Risk note:** Pull-back camera move + new content emerging at the edges is two simultaneous changes. If jitter appears, this becomes the single hardest cut to mask — fallback is a hard cut from `pm_role_grabbed.png` to `final_panorama_v3_a.png` with a 0.4s cross-fade in FFmpeg.

---

### FIN — Panorama Hold (Hold, 5s)

| Field | Value |
|---|---|
| **Type** | FFmpeg slow Ken Burns pan (no Seedance) |
| **Frame** | `runs/act2-exploration/concepts/zone4/final_panorama_v3_a.png` |
| **Duration** | 5s |

Avoid Seedance here — texture crawl risk on a 5s static cream-paper shot is high, per the research. Apply a slow Ken Burns pan in FFmpeg instead (gentle horizontal drift across the panorama, no zoom).

```bash
# Slow horizontal pan (drift right ~5% across 5s)
ffmpeg -loop 1 -i final_panorama_v3_a.png -vf \
  "scale=2400:-1,zoompan=z='1.0':x='if(gte(in_time,0),(in_time/5)*120,0)':y='ih/2-(ih/2)':d=120:s=1920x1080" \
  -t 5 -r 24 -pix_fmt yuv420p shots/FIN_panorama_pan.mp4
```

> **Pre-FIN cleanup:** This is where the panorama's known NB2 brand-label glitches ("Anthropic" duplicated, "AGENT HARNESS"/"AGENT USE"/"TOOL" oddities) must be cleaned up in Procreate before the Ken Burns pan is applied.

## Assembly Order

```
W1 → W2 → W3 → S0 → S1 → T0 → T1 → T2 → [HARD CUT] → T3 → [HARD CUT] → TR → REV → [HARD CUT] → PM → PB → FIN
```

**Hard cuts (3):** T2→T3 (shot/reverse-shot to POV), T3→TR (POV back to external), REV→PM (scene change).

## Verification Gates (per shot, post-Seedance)

For each Seedance clip after generation, check:
- [ ] **Identity:** Sean still recognizable vs A-2 (no jaw drift, eye-spacing drift)
- [ ] **Style:** pencil line quality intact end-to-end (no slide toward digital/clean)
- [ ] **Continuity:** stubble state correct (clean-shaven W1-W3; stubble S0+)
- [ ] **Wardrobe:** dark navy tee + cool gray jeans throughout (no color drift)
- [ ] **Companion design:** terracotta orange loaf, dot eyes (T2, TR, REV, PM, PB, FIN)
- [ ] **No texture crawl:** background paper grain stays static
- [ ] **No camera jitter:** single camera move executes cleanly
- [ ] **End frame matches anchor:** within ~80% (Seedance end-frame is approximate by spec)

Failures trigger one retry with prompt refinement; second failure escalates to the listed fallback strategy per shot.

## Phase Boundary

Round 3 ends here. The Seedance generation phase (Phase B.5 in CLAUDE.md) picks up next:
1. Upload anchor frames to a fal.ai-accessible URL or pass as base64
2. Run all 10 Seedance clips (Fast tier first pass)
3. Extract frames at 12fps from each clip
4. NB2 cleanup pass on extracted frames
5. Procreate cleanup of panorama brand labels (gate to FIN)
6. FFmpeg assembly per the order above

That work is its own plan, not Round 3's responsibility.
