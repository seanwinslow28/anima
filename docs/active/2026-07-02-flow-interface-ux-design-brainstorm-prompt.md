# Flow-like Interface — UX/UI Design Brainstorm Prompt

**How to use:** open a **fresh Cowork session** (the PM / sw-creative / design / impeccable / grilling skills are all available there). **Attach your Google Flow screenshots** as the layout reference. Paste everything below the line. This is a **design session, not a build** — it ends with a UX/UI spec + mockups + a clickable HTML prototype that Claude Code will build the frontend from *after* the daemon lands.

---

▼▼▼ PASTE EVERYTHING BELOW THIS LINE ▼▼▼

Help me design the **look and feel** of anima's Flow-like desktop interface — the full app, every screen — before we hand anything to Claude Code. We have the backend mapped (the daemon) and the screens *listed*, but the actual **UX/UI is unmapped**. Run this as a real design brainstorm: diverge wide, grill me hard, and converge on a spec + a clickable prototype. **I'm the one decider** — every stage recommends with a lean; I pick.

## What anima's interface is
A **native desktop app** (Electron/Tauri) that puts a face on my animation pipeline: I drive its gates (plan → script → storyboard → animatic → generate → assemble) visually instead of from a terminal, ending in a **timeline** to string clips, preview, and export. The primary user is **me — a solo creator running an agent fleet to make animated shorts**; the secondary audience is **portfolio viewers / hiring managers** (it doubles as a demo of "the pipeline is the portfolio"). So: **a real daily tool first, a showpiece second.** The philosophy to honor — *read like a studio, not a terminal*; the pipeline's *opinion* (the critic gates, the Bible lock, the run state) is the thing Flow can't show and our differentiator.

## Read first
- `/Users/seanwinslow/Code-Brain/anima/docs/active/2026-06-29-flow-like-interface-design.md` — the direction (phasing v1 chat+gates → v2 stage pages → v3 timeline; the desktop shape; the differentiator).
- `/Users/seanwinslow/Code-Brain/anima/docs/active/2026-07-02-flow-interface-daemon-foundation-plan.md` — the **screen inventory** (each screen ↔ its endpoints ↔ its Flow-screenshot precedent) and the `run_state.json` data each screen shows.
- `/Users/seanwinslow/Code-Brain/anima/docs/active/2026-07-02-daemon-build-plan-CONVERGED.md` — the **API contract** the UI binds to (endpoints, the `next_action` field that drives navigation).
- `/Users/seanwinslow/Code-Brain/anima/CLAUDE.md` + `PHILOSOPHY.md` — voice + the "read like a studio" belief.
- My attached **Google Flow screenshots** — the layout inspiration (project gallery, per-stage workspace, storyboard, the "what to change?" edit view + history, the clip-strip timeline).

## The session flow
1. **Frame + journey.** Use `/pm-product-discovery:brainstorm-ideas-new` for a PM / Designer / Engineer read on the UX, then map the **user journey** through the app end-to-end: New project (or brainstorm) → dashboard → run overview → each gate → the per-frame eye-gate loop → timeline → export. Surface the jobs, the friction, the moments that matter.
2. **Design intent + aesthetic exploration.** Use `/impeccable:impeccable` to establish **design intent** — register (this is *brand-forward* since it's also a portfolio piece, but it must serve the workflow), the anti-slop bans, color (OKLCH), type, motion — and `frontend-design` for a distinctive, non-templated direction. Then generate **3 distinct aesthetic directions** and show each as a mocked **hero screen** (the dashboard or run-overview) so I can *see* them:
   - **A — Flow-style dark pro-tool** (dark, minimal, tool-forward, like the screenshots).
   - **B — Warm-paper studio** (my portfolio identity: warm paper `#FFF9F0` + ink + teal `#0A3E42`, Newsreader + JetBrains Mono — "a studio, not a terminal").
   - **C — Hybrid** (light warm chrome around a focused dark "stage" canvas where the art lives).
   Develop/critique these, don't just label them — **I pick one** (or a blend) before we design screens.
3. **Diverge on layout + interaction.** Use `/sw-creative-toolkit:brainstorm` on the hard UX questions, several options each: how chat + gates coexist; how the **eye-gate** works (candidate review → approve / retry-with-a-note, with Em's read shown); how the **timeline** arranges clips + previews + exports; the stage-navigation model; and how the daemon's **`next_action`** drives "what do I do next."
4. **Grill me.** Use `/grilling` (or `anthropic-skills:grilling`) to resolve every UX fork one at a time, always with your recommendation: navigation model, chat placement (docked vs per-screen), how gates surface, the eye-gate interaction, the timeline interaction, empty / loading / error states, keyboard shortcuts, the desktop window model (single window vs panes). Don't ask what the docs already answer — read them.
5. **Design each screen (full app, v1→v3).** Apply the chosen aesthetic consistently. Cover **all of these**, and for each give layout, key interactions, the states (empty / loading / error / mid-generation), the **daemon endpoints it binds to**, and the microcopy (use `design:ux-writing` for button labels, gate prompts, empty states, errors):
   - **v1:** Dashboard (run gallery + a "New project / Brainstorm" entry) · Run overview / status · Plan gate (plan + cost preview) · Script gate · Storyboard curation gate · Animatic placement gate (rough upload) · **Generate / eye-gate** (the most-used screen) · the persistent Chat shell.
   - **v2:** Character builder (Cy) · Storyboard board (Bea) · Generate grid (Flo + Em) · Motion.
   - **v3:** the **Timeline** (arrange / trim / preview / export — simple, not a full NLE).
   Run `design:design-critique` on the set (hierarchy, consistency, usability) and a quick `design:accessibility-review` pass (contrast, keyboard nav) before finalizing.

## Deliverables
1. **A UX/UI design spec** (save to `/Users/seanwinslow/Code-Brain/anima/docs/active/`, dated) — the design system (color OKLCH / type / spacing / motion tokens + components), the user-journey map, and per-screen layouts + interactions + states + microcopy + endpoint bindings. This is what Claude Code builds from.
2. **Inline mockups** of the key screens as you go (render them so I can react — visualize widget or inline HTML).
3. **A clickable, self-contained HTML prototype** (single file, mock data, no backend) of the **primary flow** — dashboard → run overview → a gate → the eye-gate → the timeline — in the chosen aesthetic, that I can actually poke at in a browser. Save it alongside the spec.

## Rules
- **Design, don't build** the real app — the output is a spec + prototype for Claude Code, not the Electron/Tauri frontend itself.
- **Ground every screen in the real daemon API** (the CONVERGED plan) — no UI that the backend can't feed.
- **One decider — me.** Diverge wide, but converge to *my* picks; keep the spec in a studio voice, not template boilerplate. Honor "read like a studio," and let the pipeline's opinion (the gates, the critic, the run state) be visible — that's the differentiator.
