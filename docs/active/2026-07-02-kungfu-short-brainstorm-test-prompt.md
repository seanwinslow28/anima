# Kung-Fu Short — Live Brainstorm Test (front-door skill + Higgsfield art-viz)

**How to use:** open a **fresh Cowork session** with the **`frontdoor-slice1` worktree** as the working folder (so the `brainstorm-front-door` skill and its `pipeline.frontdoor` emit seam load), and make sure the **Higgsfield MCP** is connected. Paste everything below the line. This does two things at once: exercises the newly-built Slice-1 front-door skill on a real concept, and tests whether the Higgsfield MCP can carry the art-viz layer (which the skill doesn't build until Slice 3).

---

▼▼▼ PASTE EVERYTHING BELOW THIS LINE ▼▼▼

Help me brainstorm and map out my **"GRANDMASTER" kung-fu short** by running our newly-built front-door skill on it — and, as we go, use the **Higgsfield MCP** to generate character concepts and art-style frames so I can *see* the vibe. This is a **test run**: I want to feel how the Slice-1 skill performs live, and whether Higgsfield works as the art-viz engine (that stage isn't built into the skill yet — you'll add it manually).

## The piece
A grieving, wimpy kid trains for a year in the kung-fu movies his late **grandmother** left behind — and in the secret that she was once a warrior — to return to the birthday party that humiliated him and destroy the piñata like a Kurosawa villain. Sincere with a dark edge; a **Genndy Tartakovsky / Samurai Jack** homage; ~2–3 min. We hand-mapped a full concept already — treat it as the **quality bar and reference, not a script to copy**; I want the skill to earn it (or improve on it) live.

## Read first (absolute paths — the main anima checkout)
- Concept doc (the GRANDMASTER version, incl. the Genndy timing/style technique sheet + 3 style-route prompts + the candy-as-oil-geyser mechanic): `/Users/seanwinslow/Code-Brain/anima/docs/active/2026-07-02-frontdoor-dryrun-pinata-short-concept.md`
- Studio Brief (the contract shape): `/Users/seanwinslow/Code-Brain/anima/docs/active/2026-07-02-frontdoor-dryrun-pinata-short-studio-brief.md`
- The skill itself + its worked example: `.claude/skills/brainstorm-front-door/SKILL.md` and `references/pinata-worked-example.md`
- Genndy reference images (use as *style references* for Higgsfield): `/Users/seanwinslow/Downloads/Substack-Post-1-exercise/Substack-Post-1-Art/gendy-tartakovsky-animation/`
- Borrowed-skill details (methods behind the stages + the AKCodez style-prompt shape): `/Users/seanwinslow/Code-Brain/anima/docs/active/2026-07-02-referenced-skills-detail-reference.md`

## How to run it
1. **Invoke the `brainstorm-front-door` skill** (if it's not auto-loaded, read its `SKILL.md` in the worktree and follow it exactly). Open the session sidecar; record my spark verbatim as the first locked decision. My spark is the piece paragraph above.
2. **Run the chain for real** — micro-expand (3 alternate premises / 3 style-tone routes / 3 risk questions), then `frontdoor-interrogate`, then `frontdoor-synthesize`. Because we have the prior concept as the bar, move *efficiently* — but make me make the live decisions; don't just transcribe the doc. If the skill hits friction (a stage skill won't invoke, the emit seam errors, the sidecar can't write), **note it plainly** — that feedback is the point of the test.
3. **Layer the Higgsfield art-viz (the manual part being tested).** At the **style-tone-routes** beat and again when **character seeds** surface, use the Higgsfield MCP to generate images and show me:
   - **Art-style / vibe frames (2–3):** a hero frame (the mid-air ninja-star landing pose, or the candy geyser) in the three registers from the concept doc — **Route A Samurai-Jack-faithful, Route B Primal-grit, Route C hybrid-with-pencil-warmth.** Use the Genndy reference images as **style references**, and build the prompts from the concept doc's style-route prompts + the Genndy technique sheet (no black outlines, silhouette on flat color, painterly bg, per-shot letterbox). A stylized model is the right pick — try **Nano Banana Pro / Nano Banana 2** (use `models_explore` / `presets_show` to confirm options; `generate_image` to render).
   - **Character concepts:** the wimpy kid (+ the too-big headband), **young secret-badass grandma mid-flying-kick**, present-day grandma, and the host dad. Consider `show_characters` to make them reusable refs.
   - Present each batch for me to react to and **lock the look** before moving on. Generate **deliberately — a handful, not a flood** (Higgsfield is credit-metered on my trial month; that cost signal is part of what we're testing).
   - If the Higgsfield MCP isn't connected or a call fails, **don't block the brainstorm** — fall back to $0 Flow-ready prompts (or the anima `gemini-pencil-animation-image-gen` skill) and note that Higgsfield didn't work, so the fallback matters for the Slice-3 design.
4. **Synthesize + emit** the brief bundle (`concept.md`, `00_studio_brief.md`, `character_seeds.yaml`, `frontdoor.json`) through the skill's seam; run the `--stub` smoke; show me the emitted dir, the validation result, and the gap report.

## Capture for the build (I'm mid-way planning Slice 2 / Slice 3)
End with a short **field note**: how the Slice-1 skill *felt* to run (where it was relentless vs where it dragged, any bug), and how Higgsfield performed as art-viz — which model + prompt shape nailed the Genndy look, the rough credit cost, and whether **Higgsfield or Flow** should be the default ART-VIZ engine when Slice 3 gets built. That note feeds the real build.

## Rules
- One decider — **I** make the calls; stages recommend with a lean. Specifics beat categories. Keep the concept doc + brief in *my voice*, not boilerplate. No invented facts. Don't edit `manifest.yaml`. Mind the Higgsfield credits.
