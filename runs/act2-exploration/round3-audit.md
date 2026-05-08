# Round 3 — Production Anchor Audit

> Audit of the 11 locked Round 2 concepts against the Round 3 production checklist. PASS = ready to use as a Seedance start/end anchor. FAIL = must be regenerated at production fidelity before Seedance use.

**Audit date:** 2026-04-26 • **Auditor:** Claude Opus 4.7 (creative-director skill) • **Reference:** `images/2D-Character-Sketch-Sean-v1.png` (A-2 anchor)

## Checklist

| Code | Criterion | Pass = |
|------|-----------|--------|
| C1 | **Identity** | Sean immediately recognizable vs A-2 — same hair shape/parting, jaw, eye spacing, nose, body proportions |
| C2 | **Aesthetic** | Hand-drawn pencil on cream paper #FAF5E8 — warm graphite lines, visible construction marks, cross-hatching for shading |
| C3 | **Line confidence** | Polished line weight (not sketchy/loose) — comparable density to `terminal_closeup_companion.png` |
| C4 | **Aspect ratio** | True 16:9 |
| C5 | **Continuity** | Style/lighting/wardrobe consistent with neighboring beats in the sequence |
| C6 | **Clean for Seedance** | No leaked stage-direction text, no garbled labels (panorama exception), composition leaves room for motion |

## Results

| # | Beat | File | C1 | C2 | C3 | C4 | C5 | C6 | Verdict | Notes |
|---|------|------|----|----|----|----|----|----|---------|-------|
| 1 | 1a — Walk Film | `zone1/film.png` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** | Clean-shaven (correct for walking sequence) |
| 2 | 1b — Walk Animation | `zone1/animation.png` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** | Clean-shaven; matches 1a |
| 3 | 1c — Walk AI Discovery | `zone1/ai_discovery.png` | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | **FAIL** | Two issues — see "Failures" section |
| 4 | 2 — Sit Down | `zone3/sit_down.png` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** | Stubble appropriate (now at desk, "been working") |
| 5 | 3a — Terminal Empty | `zone3/terminal_closeup_empty.png` | — | — | — | — | — | — | **PASS** | Locked — regenerated this session against companion-shot style target |
| 6 | 3b — Companion Appears | `zone3/terminal_closeup_companion.png` | — | — | — | — | — | — | **PASS** | Locked — gold-standard style reference for the whole project |
| 7 | 3c — Sean POV | `zone3/terminal_pov_sean.png` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** | Cool-blue screen-light cross-hatching is a beautiful continuity element with the terminal beats |
| 8 | Trans — Pulled In | `zone3/transition_pulled_in.png` | ✓ | ✓ | ✓ | ✓ | ✓ | ⚠ | **PASS** | Pencil/stylus visible on desk to right of laptop. Not in Sean's hand, framed as incidental desk prop. Acceptable since this beat is post-terminal-closeups (the close-ups intentionally cropped the desk surface). Flag if it later conflicts with PM beat continuity |
| 9 | 4 — Revelation | `zone3/revelation.png` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** | Hand-lettered concept words (VIBE CODING, AGENTS, PIPELINES, GENERATE, POST /generate) are intentional content, not stage-direction leak |
| 10 | 5 — PM Role | `zone4/pm_role.png` | ✓ | ✓ | ✓ | ✓ | ✓ | ⚠ | **PASS** | Tiny garbled chat-window text on the right laptop ("yov, we are ongoing?", "amare the int?") — too small to read at video scale, acceptable. Gamified "FEATURE_COMPLETE 6//" + XP bar at top is intentional UI, not a leak |
| 11 | 6 — Final Panorama | `zone4/final_panorama_v3_a.png` | ✓ | ✓ | ✓ | ✓ | ✓ | ⚠ | **PASS (with known exception)** | Per Round 2 handoff: duplicated/garbled brand labels ("ANTHROPIC" twice, "AGENT HARNESS", "AGENT USE", "TOOL") accepted for Procreate cleanup, NOT regenerated. Bonus: RPG warrior sprite from Act 1 visible on companion's back as Easter egg ✓ |

**Summary:** 10 PASS, 1 FAIL. Only `zone1/ai_discovery.png` requires regeneration before Seedance use.

## Failures — Detail and Remediation

### `zone1/ai_discovery.png` — FAIL

**Issue 1 — Stage-direction text leak (C6):**
Top-left corner contains visible hand-lettered "Beat 1c / Act 2" text alongside the A-2 production label. This is a NB2 prompt-leak failure (the planning language from the prompt got rendered as visible text). It will read on screen at video scale and breaks the diegetic illusion.

**Issue 2 — Stubble continuity break (C5):**
Sean has visible 5-o'clock shadow stubble in this frame, but the preceding `film.png` and `animation.png` (Beats 1a, 1b — same walking sequence) are clean-shaven. The handoff established stubble as continuity for "frames where he's been working" (i.e. desk beats), not for the walking-through-history sequence. This breaks within-shot continuity for the W3 Seedance clip and across the full walking trio.

**Remediation:**
1. Rewrite `prompts/act2/zone1_ai_discovery.txt` to F06-style 7-Layer structure with:
   - Explicit "clean-shaven, no stubble, no facial hair" identity constraint (matching `film.png` and `animation.png`)
   - Explicit "DO NOT WRITE THE WORDS 'Beat 1c', 'Act 2', or any stage-direction language as text in the image" negative constraint
   - The hand-lettered AI headlines (ChatGPT, Vibe Coding, Karpathy, Anthropic, Gemini, etc.) ARE intentional content and stay
   - Production label stays as just "A-2" circled in upper-left (no "Beat 1c")
2. Regenerate with A-2 anchor + `zone1/film.png` + `zone1/animation.png` as references (style + identity + walking-sequence continuity)
3. Re-audit against the same checklist; retry up to 2x if it fails

## Pre-Flight Notes for Step 3 (NEW Bridge Anchors)

The audit revealed style/continuity facts that the 4 NEW bridge anchors must respect:

- **Walking-sequence bridges (`film_to_animation`, `animation_to_ai`):** Sean must be **clean-shaven** to match film.png/animation.png/regen-of-ai_discovery.png. Reference film.png + animation.png/ai_discovery.png as style anchors.
- **`pre_pulled_in.png`:** Sean has **stubble** (matches sit_down → terminal sequence → transition_pulled_in). Reference transition_pulled_in.png as the immediate style/composition anchor.
- **`pm_role_grabbed.png`:** Sean has **stubble**. Reference pm_role.png as the immediate style/composition anchor; Kanban board layout, sticky notes, and companion position must match exactly (it's the same scene, just one frame later in time).

## Pre-Flight Notes for Step 5 (Seedance Shot List)

Key continuity moments the shot list and per-shot Seedance prompts must call out:

- **Shot S0 (`ai_discovery → sit_down`):** Sean transitions from clean-shaven to stubbled. Acknowledge in the Seedance prompt or accept as a "time passing" cut. Easiest fix: add "subtle 5-o'clock shadow grows in" to the Seedance prompt for S0. This is exactly the kind of motion Seedance can handle in 4s.
- **Shot REV (`transition_pulled_in → revelation`):** The pencil on the desk in the Trans frame disappears in the Revelation frame because the desk dissolves. Seedance should naturally handle this if the prompt mentions "desk dissolves into mind-map space."
- **Shot PM (`pm_role → pm_role_grabbed`):** Same composition, only the Kanban card moves from the board into Sean's hand. Locked camera, locked everything else — this is a low-risk Seedance clip.
