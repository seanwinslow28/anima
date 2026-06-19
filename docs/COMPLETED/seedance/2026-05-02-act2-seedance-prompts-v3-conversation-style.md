# Act 2 Seedance Prompts — v3 (Conversation-Style Structured Block)

> **Purpose:** Manual-generation prompts ready to paste into the [fal.ai Seedance 2.0 Fast playground](https://fal.ai/models/bytedance/seedance-2.0/fast/image-to-video). Each shot adopts the prompt structure that produced strong results in the [Veo 3.1 Street Fighter II conversation](../../examples/Conversation-that-utilized-prompt-science-successfully.md) — a structure that v2 partially abandoned in favor of pure prose minimalism.
>
> **Companion docs:**
> - [Conversation-that-utilized-prompt-science-successfully.md](../../examples/Conversation-that-utilized-prompt-science-successfully.md) — the source conversation; idle-bounce + walk-cycle + neutral-jump tests on Veo 3.1
> - [act2-seedance-shot-list.md](../../pencil-test/act2-seedance-shot-list.md) — original v1 spec, fallback strategies, assembly order, QA gates (still authoritative for everything except wording)
> - [2026-04-27-act2-seedance-prompts-v2-prompt-science.md](2026-04-27-act2-seedance-prompts-v2-prompt-science.md) — v2 rewrite (still valid as fallback if a v3 prompt drifts)
> - [2026-04-27-seedance-manual-handoff.md](2026-04-27-seedance-manual-handoff.md) — paused-state context, anchor paths, durations, last-batch seeds, fal.media cached URLs

**Created:** 2026-05-02 • **Branch:** `ultraplan/seedance-pipeline`

---

## Why a v3

The v2 rewrites were valid — they correctly compressed prompt budget and dropped the worst over-constraint patterns from v1. But **manual generation runs reported underwhelming Seedance output** even with v2. Cross-referencing the recent Veo 3.1 conversation that produced the best video output of the project surfaced four structural differences v2 had quietly lost:

| What worked on Veo 3.1 | What v2 does | v3 fix |
|---|---|---|
| **Named genre anchor.** "Classic 2D fighting game idle in the style of Street Fighter II" — invokes a tradition the model has training-set evidence of. | "Hand-drawn pencil animation on cream paper" — describes the medium but doesn't anchor to a known tradition. | Anchor every shot to **"Traditional 2D animation pencil test in the style of classic Disney rough animation"** — a tradition video models have seen heavily during training (Disney pencil tests are widely circulated reference material). |
| **`CRITICAL STYLE REQUIREMENTS:` as a delimited bulleted block** at the bottom of the prompt, with explicit negatives ("No anti-aliasing on edges", "No gradients", "Solid background must remain solid"). | Style guardrails dissolved into prose ("Keep pencil line quality, paper grain, and visible construction marks"). | Restore the labeled bulleted block. Each bullet calls out one style attribute or one explicit negative. |
| **`CAMERA:` as its own labeled section** with explicit negatives — "no zoom, no rotation, no horizontal drift, locked vertical dolly". | Camera tucked mid-sentence ("Fixed camera, even diffuse lighting"). | Promote camera direction to its own labeled section. For static shots: "Completely static, locked tripod. No pan, no zoom, no jitter, no rotation." For moving shots: explicit named axis + a list of negatives on every other axis. |
| **`Duration: Xs.` as a structural closer.** | No closer. | Add it back. The duration parameter is set in the API form, but the closing line acts as a structural signal that helps the model treat the action as a self-contained beat. |

The v2 rewrites were also too aggressive on word count. The Veo conversation's best-performing prompts were ~110–120 words, not 50–80. The right target is **structural discipline, not minimum words** — a compact action arc PLUS explicit guardrail blocks lands around 100–130 words and consistently outperforms the same content as terse prose.

---

## Continuity Rules (still locked — do NOT relax)

These are encoded into the v3 rewrites. If you regenerate manually and Seedance drops one, prepend the relevant line:

- **Walking sequence (W1, W2, W3):** Sean is **clean-shaven**.
- **Desk sequence (S0 onward):** Sean has a **subtle 5-o'clock-shadow stubble**. S0 is the shot where it grows in.
- **AI Companion:** terracotta-orange loaf creature, dot eyes, stubby arms.
- **Wardrobe (locked, no variation):** dark navy crew-neck T-shirt, cool gray cuffed jeans, gray-cream sneakers.
- **No stylus in Sean's hand in Act 2.** The pencil visible on the desk in `transition_pulled_in.png` and `pre_pulled_in.png` is an incidental desk prop, not held. (This is the inverse of the Act 1 stylus rule.)

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

## Prompt Template (the v3 structure)

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. [ACTION ARC — what happens, in plain verbs, 1–3 sentences]. [Continuity reminder if relevant — clean-shaven, stubble, no stylus, etc.]

CAMERA: [Static or named axis with explicit negatives on every other axis].

CRITICAL STYLE REQUIREMENTS:
- Rough graphite pencil line quality on every frame
- Cream paper grain texture stays consistent
- Visible construction marks on the character
- Bold dark pencil outlines, no anti-aliasing on edges
- Flat graphite shading only, no digital gradients or smooth blending
- Even diffuse animation paper lighting
- No anime stylization, no digital polish, no photorealistic rendering
- [Per-shot extras: hand-lettered text preservation, cross-hatching density, screen-glow, etc.]

Duration: Xs.
```

---

## Shot Cards (assembly order)

Each card gives you: anchors, duration, the v3 prompt in a copy-paste block, and a one-line note on what changed from v2.

---

### W1 — Walk Film (Seedance, 4s, low risk)

- **Start:** `runs/act2-exploration/concepts/zone1/film.png`
- **End:** `runs/act2-exploration/concepts/bridges/film_to_animation.png`
- **Duration:** 4s

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props remain stationary — only Sean moves. Sean is clean-shaven throughout.

CAMERA: Completely static, locked tripod. No pan, no zoom, no jitter, no rotation.

CRITICAL STYLE REQUIREMENTS:
- Rough graphite pencil line quality on every frame
- Cream paper grain texture stays consistent
- Visible construction marks on the character
- Bold dark pencil outlines, no anti-aliasing on edges
- Flat graphite shading only, no digital gradients or smooth blending
- Even diffuse animation paper lighting, no cinematic shadows
- No anime stylization, no digital cleanness, no glossy polish

Duration: 4 seconds.
```

> *vs v2:* Adds the named genre anchor ("classic Disney rough animation") and promotes guardrails to a delimited bulleted block. Action arc is unchanged in substance — only the structural framing around it changed.

---

### W2 — Walk Animation (Seedance, 4s, low risk)

- **Start:** `runs/act2-exploration/concepts/bridges/film_to_animation.png`
- **End:** `runs/act2-exploration/concepts/bridges/animation_to_ai.png`
- **Duration:** 4s

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean keeps walking left to right at the same steady pace. Behind him, the Film props lighten and fade out of the paper. Around him, the Animation props (figure studies, light box, animation books) become more prominent. On the right edge, hand-lettered AI news clippings begin to sketch themselves in. Sean stays clean-shaven.

CAMERA: Completely static, locked tripod. No pan, no zoom, no jitter, no rotation.

CRITICAL STYLE REQUIREMENTS:
- Rough graphite pencil line quality on every frame
- Cream paper grain texture stays consistent
- Visible construction marks on the character
- Hand-lettered text quality preserved on emerging clippings
- Bold dark pencil outlines, no anti-aliasing on edges
- Flat graphite shading only, no digital gradients
- Even diffuse animation paper lighting
- No anime stylization, no clean digital typography, no glossy polish

Duration: 4 seconds.
```

> *vs v2:* "lighten and fade away" → "lighten and fade out of the paper" (anchors the fade-mechanism to the paper substrate, which the model handles better than abstract opacity). Adds explicit hand-lettered-text negative.

---

### W3 — Walk AI (Seedance, 4s, low risk)

- **Start:** `runs/act2-exploration/concepts/bridges/animation_to_ai.png`
- **End:** `runs/act2-exploration/concepts/zone1/ai_discovery.png`
- **Duration:** 4s

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean keeps walking left to right at the same steady pace. His eyebrow lifts and his head tilts with growing curiosity. The remaining Animation props fade out of the paper behind him. Around him, hand-lettered AI news clippings (ChatGPT, Karpathy, Vibe Coding, Anthropic, Gemini) sketch themselves into solid form. Sean stays clean-shaven.

CAMERA: Completely static, locked tripod. No pan, no zoom, no jitter, no rotation.

CRITICAL STYLE REQUIREMENTS:
- Rough graphite pencil line quality on every frame
- Cream paper grain texture stays consistent
- Hand-lettered text quality preserved on every clipping
- Bold dark pencil outlines, no anti-aliasing on edges
- Flat graphite shading only, no digital gradients
- Even diffuse animation paper lighting
- No anime stylization, no clean digital typography, no glossy polish

Duration: 4 seconds.
```

> *vs v2:* Splits the curiosity beat ("eyebrow lifting and head tilting") into its own short sentence so the model treats it as a discrete action rather than a modifier on "walks". The AVOID-list lesson from the conversation: keep modifiers compact and discrete.

---

### S0 — Arrive at Desk (Seedance, 4s, **HIGHEST RISK morph**)

- **Start:** `runs/act2-exploration/concepts/zone1/ai_discovery.png`
- **End:** `runs/act2-exploration/concepts/zone3/sit_down.png`
- **Duration:** 4s
- **Stubble:** grows in during this shot — Sean ends with a subtle 5-o'clock shadow.

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. The floating AI headlines around Sean dissolve out of the paper. The desk, laptop, second monitor, coffee mug, and chair sketch themselves into existence on the paper around him. Sean shifts from a mid-stride walk into a seated working pose at the desk. A faint 5-o'clock-shadow stubble grows in on his jaw as time passes.

CAMERA: Completely static, locked tripod. No pan, no zoom, no jitter, no rotation.

CRITICAL STYLE REQUIREMENTS:
- Rough graphite pencil line quality on every frame
- Cream paper grain texture stays consistent
- Visible construction marks on Sean and the desk furniture
- Bold dark pencil outlines, no anti-aliasing on edges
- Flat graphite shading only, no digital gradients
- Even diffuse desk lighting, no harsh cinematic shadows
- No anime stylization, no digital polish, no photorealistic rendering

Duration: 4 seconds.
```

> *vs v2:* Same risk profile, same fallback (hard-cut from `ai_discovery.png` to `sit_down.png` with 0.3s cross-fade in FFmpeg if Seedance breaks identity). Explicit "dissolve out of the paper" framing replaces the more abstract "dissolve away".

---

### T0 — Push-in to Terminal (Seedance, 4s, medium risk — camera + pose change)

- **Start:** `runs/act2-exploration/concepts/zone3/sit_down.png`
- **End:** `runs/act2-exploration/concepts/zone3/terminal_closeup_empty.png`
- **Duration:** 4s

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean's hands settle onto the keyboard. The dark cross-hatched terminal window grows to fill the frame as the desk surroundings recede off-frame.

CAMERA: Slow, smooth push-in toward the laptop screen. The camera moves only forward — no horizontal drift, no rotation, no shake, no zoom changes other than the push itself. Treat the camera as a locked dolly on rails. One continuous push, nothing else moves.

CRITICAL STYLE REQUIREMENTS:
- Rough graphite pencil line quality on every frame
- Cross-hatched terminal density preserved throughout
- Cream paper grain texture stays consistent
- Bold dark pencil outlines, no anti-aliasing on edges
- Flat graphite shading only, no digital gradients
- Even diffuse desk lighting
- No anime stylization, no digital polish, no glossy rendering

Duration: 4 seconds.
```

> *vs v2:* This is the biggest structural change. The Veo conversation's neutral-jump prompt nailed camera tracking by writing CAMERA as a dedicated paragraph with explicit negatives on every axis except the intended one ("locked vertical dolly"). v3 mirrors that exact structure for the push-in. v1 fallback (split into S1.5 + T0) still stands if jitter appears.

---

### T2 — Companion Appears (Seedance, 3s creative → 4s API, **lowest-risk shot**)

- **Start:** `runs/act2-exploration/concepts/zone3/terminal_closeup_empty.png`
- **End:** `runs/act2-exploration/concepts/zone3/terminal_closeup_companion.png`
- **Duration:** 4s (API minimum; trim to 3s in assembly — invisible because hard cut follows)

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Inside the dark cross-hatched terminal window, the terracotta-orange loaf-shaped AI companion (dot eyes, stubby arms) sketches itself into existence. A few small pencil sparkle marks pop around it as it forms. The terminal text shifts from "c:\>_ what is..." to "c:\>_ hello, sean...".

CAMERA: Completely static, locked tripod. No pan, no zoom, no jitter, no rotation.

CRITICAL STYLE REQUIREMENTS:
- Rough graphite pencil line quality on every frame
- Cross-hatched terminal density preserved throughout
- Hand-lettered terminal text quality preserved (no clean digital typography)
- Bold dark pencil outlines on the companion silhouette, no anti-aliasing
- Flat graphite shading only, no digital gradients
- Even cool screen-glow lighting on the companion
- No anime stylization, no digital polish, no glossy rendering

Duration: 4 seconds.
```

> *vs v2:* Keeps the explicit companion design recap (loaf, dot eyes, stubby arms) and adds a per-shot guardrail for cross-hatching density — Seedance has been observed to "clean up" cross-hatching mid-clip into solid blacks.

---

### TR — Hand Grab (Seedance, 3s creative → 4s API, medium risk, HARD CUT from T3)

- **Start:** `runs/act2-exploration/concepts/bridges/pre_pulled_in.png`
- **End:** `runs/act2-exploration/concepts/zone3/transition_pulled_in.png`
- **Duration:** 4s (API minimum; trim to 3s in assembly)

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. The companion's terracotta arm extends out of the laptop screen. Its small hand reaches across and grabs Sean's right hand. Sean leans forward, eyes widening, as he is gently tugged toward the screen. A few short pencil motion lines accentuate the pull.

CAMERA: Completely static, locked tripod. No pan, no zoom, no jitter, no rotation.

CRITICAL STYLE REQUIREMENTS:
- Rough graphite pencil line quality on every frame
- Cream paper grain texture stays consistent
- Visible construction marks on Sean and the companion
- Bold dark pencil outlines, no anti-aliasing on edges
- Flat graphite shading only, no digital gradients
- Even desk lighting with a cool blue screen-glow on Sean's face
- No anime stylization, no digital polish, no photorealistic rendering

Duration: 4 seconds.
```

> *vs v2:* Same softer-verb choice ("gently tugged" vs "pulled") to prevent Seedance over-pulling Sean clean out of frame. Splits the action into discrete sentences so the model treats arm-extend, hand-grab, lean-forward, and motion-lines as four distinct beats it can interpolate between rather than one tangled instruction.

---

### REV — The Revelation (Seedance, 5s, **HIGHEST RISK clip overall**)

- **Start:** `runs/act2-exploration/concepts/zone3/transition_pulled_in.png`
- **End:** `runs/act2-exploration/concepts/zone3/revelation.png`
- **Duration:** 5s

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. The companion pulls Sean forward as the desk and laptop dissolve out of the paper. Hand-lettered concept words (VIBE CODING, AGENTS, PIPELINES, GENERATE) and small pencil-drawn diagrams (code editor, neural-net nodes, prompt-to-output arrows) sketch themselves into the cream-paper space around Sean and the companion as a mind-map. Sean rises upright, arms spreading outward in a moment of revelation. The companion floats steadily beside him.

CAMERA: Completely static, locked tripod. No pan, no zoom, no jitter, no rotation.

CRITICAL STYLE REQUIREMENTS:
- Rough graphite pencil line quality on every frame
- Cream paper grain texture stays consistent
- Hand-lettered text and pencil-drawn diagram quality preserved
- Bold dark pencil outlines, no anti-aliasing on edges
- Flat graphite shading only, no digital gradients
- Even diffuse animation paper lighting
- No anime stylization, no clean digital typography, no glossy polish

Duration: 5 seconds.
```

> *vs v2 fallbacks still stand:* (1) drop to 4s; (2) generate intermediate `bridges/being_pulled.png` and split into REV1 (3s) + REV2 (3s). The big visual leap over 5s remains the documented risk — try v3 first, then v2, then split.

---

### PM — Grab Kanban (Seedance, 3s creative → 4s API, low risk, HARD CUT from REV)

- **Start:** `runs/act2-exploration/concepts/zone4/pm_role.png`
- **End:** `runs/act2-exploration/concepts/bridges/pm_role_grabbed.png`
- **Duration:** 4s (API minimum; trim to 3s in assembly)

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean reaches forward and plucks one sticky-note card from the IN PROGRESS column of the Kanban board with his right hand. He brings the card down to chest height. His expression softens into a small satisfied half-smile. The companion floats steadily camera-right; the rest of the board stays still.

CAMERA: Completely static, locked tripod. No pan, no zoom, no jitter, no rotation.

CRITICAL STYLE REQUIREMENTS:
- Rough graphite pencil line quality on every frame
- Hand-lettered text on the Kanban board preserved (no clean digital typography)
- Cream paper grain texture stays consistent
- Bold dark pencil outlines, no anti-aliasing on edges
- Flat graphite shading only, no digital gradients
- Even diffuse animation paper lighting
- No anime stylization, no digital polish, no glossy rendering

Duration: 4 seconds.
```

> *vs v2:* Splits "reaches forward, plucks ... and brings it down" into two sentences (reach+pluck, then bring-down). The Veo conversation found compound multi-verb sentences with commas confused the interpolation more than three short sentences.

---

### PB — Pull Back (Seedance, 5s, second-highest risk — camera + emerging content)

- **Start:** `runs/act2-exploration/concepts/bridges/pm_role_grabbed.png`
- **End:** `runs/act2-exploration/concepts/zone4/final_panorama_v3_a.png`
- **Duration:** 5s

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean and the companion stay locked in their positions camera-right. The wider workshop panorama is revealed around them — Film camera, Animation reference materials, AI news clippings, and agentic workflow diagrams arranged across the cream paper.

CAMERA: Slow, smooth dolly pull-back from the PM scene out to the wider panorama. The camera moves backward only — no horizontal drift, no rotation, no shake, no zoom changes other than the pull itself. Treat the camera as a locked dolly on rails. One continuous pull-back, nothing else moves.

CRITICAL STYLE REQUIREMENTS:
- Rough graphite pencil line quality on every frame
- Hand-lettered text quality preserved across all assets
- Cream paper grain texture stays consistent
- Bold dark pencil outlines, no anti-aliasing on edges
- Flat graphite shading only, no digital gradients
- Even diffuse animation paper lighting
- No anime stylization, no clean digital typography, no glossy polish

Duration: 5 seconds.
```

> *vs v2:* Same dedicated-paragraph CAMERA structure as T0. The Veo neutral-jump conversation showed this exact phrasing — "locked dolly on rails" + a list of axis-negatives — was what got the camera to actually track instead of drift. v1 fallback (hard-cut from `pm_role_grabbed.png` to `final_panorama_v3_a.png` with 0.4s cross-fade in FFmpeg) still stands if jitter appears.

---

## What's NOT in this doc (intentionally)

| Shot | Why not |
|---|---|
| **S1, T1, T3, FIN** | FFmpeg static holds — no Seedance call. T1 also gets a custom blinking-cursor overlay built from two variant frames. See [act2-seedance-shot-list.md §S1, §T1, §T3, §FIN](../../pencil-test/act2-seedance-shot-list.md) for the FFmpeg recipes. |
| **Hard cuts** (T2→T3, T3→TR, REV→PM) | Pure assembly cuts — no generation step. |

---

## Workflow recommendation

Same generation order as v2 — risk profile is unchanged. The v3 prompts are a **structural rewrite of the same content**, not a re-prioritization of which shots to attempt first.

1. **Walking sequence first (W1 → W2 → W3).** All low-risk, all 4s, all clean-shaven Sean. Generate them back-to-back. If any one drifts, you've validated whether the v3 structure produces measurably better output before tackling harder shots.
2. **Lowest-risk inside the desk sequence next: T2.** Locked camera, locked composition, only the companion materializes.
3. **PM and TR next (medium-risk).** Both are short (3s creative), both have one focused action.
4. **Then the harder ones in order: T0, S0, PB, REV.** S0 and REV are the documented "if these break, fall back" shots. Try v3 first — if Seedance still breaks identity or fidelity, drop to v2, then v1 fallback strategies.
5. **Drop winning MP4s into:** `runs/act2-seedance-2026-04-27/seedance/` as `<SHOT>_attempt_<NN>.mp4` (e.g., `W1_attempt_03.mp4`). The orchestrator's controller resumes from there at Task 5 (frame extraction).

---

## Per-shot escalation if v3 underperforms

If a v3 prompt gives worse results than the v2 it replaces, escalate in this order:

1. **Re-run with the same v3 prompt** (Seedance is stochastic — same prompt, new seed often clears one-off drift).
2. **Drop back to v2 for that single shot** — see [2026-04-27-act2-seedance-prompts-v2-prompt-science.md](2026-04-27-act2-seedance-prompts-v2-prompt-science.md). v3 is an optimization; v2 is the proven-acceptable baseline.
3. **Drop back to the v1 prompt** — see [2026-04-27-seedance-manual-handoff.md §4](2026-04-27-seedance-manual-handoff.md). Don't burn budget chasing a v3 win on a shot where v1 worked.
4. **Invoke the v1 shot list's fallback strategy** (split, cross-fade, hard cut) per the per-shot risk notes in [act2-seedance-shot-list.md](../../pencil-test/act2-seedance-shot-list.md).

The v3 rewrites are an experiment grounded in a single conversation's validated structure on Veo 3.1. Seedance is a different model — most of the structural lessons should transfer, but some may not. Treat v3 as the new default and v2/v1 as the safety net.

---

## Quick comparison: v2 vs v3 (W1 as the worked example)

**v2:**
```
Hand-drawn pencil animation on cream paper. Sean walks steadily left to right at a relaxed pace, head turning slightly to take in the floating Film props around him. The props stay still; only Sean moves. Fixed camera, even diffuse lighting. Keep pencil line quality, paper grain, and visible construction marks. No digital effects, no anime, no camera jitter.
```
*~62 words. One paragraph. Style guardrails dissolved into the closing sentence.*

**v3:**
```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props remain stationary — only Sean moves. Sean is clean-shaven throughout.

CAMERA: Completely static, locked tripod. No pan, no zoom, no jitter, no rotation.

CRITICAL STYLE REQUIREMENTS:
- Rough graphite pencil line quality on every frame
- Cream paper grain texture stays consistent
- Visible construction marks on the character
- Bold dark pencil outlines, no anti-aliasing on edges
- Flat graphite shading only, no digital gradients or smooth blending
- Even diffuse animation paper lighting, no cinematic shadows
- No anime stylization, no digital cleanness, no glossy polish

Duration: 4 seconds.
```
*~110 words. Three labeled blocks (action arc / camera / style requirements + duration closer). Same content, structurally surfaced.*

The hypothesis: Seedance — like Veo 3.1 in the documented conversation — pays more attention to delimited labeled blocks than to the same content as continuous prose. v3 makes that bet explicit.
