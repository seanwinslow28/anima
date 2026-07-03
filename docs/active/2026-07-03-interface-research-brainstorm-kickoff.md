# Kickoff — Deep Research + Brainstorm: anima's interface as *my personal AI animation studio*

> **How to use this file:** paste everything below the line into a fresh Cowork session (with the `anima` folder mounted). It's written as a directive brief for that session to execute end to end.

---

You're my design-research and brainstorm partner for one focused mission: take anima's already-specced desktop interface and find the ideas that make it **beautiful, clean, fast, and unmistakably *my* personal AI animation studio** — not a generic AI tool, not a Flow clone. We have a ratified v1 spec. Your job is to mine the best of animation-studio and creative-tool UI/UX, then brainstorm features and touches that elevate it, all grounded in what the pipeline can actually do.

**One decider: me (Sean).** Every stage recommends with a lean; I pick. Diverge wide, converge to my calls.

## Read first (ground truth — don't skip, don't re-litigate what's locked)

Read these before anything else. If a path isn't accessible, tell me and I'll paste the contents.

- `docs/active/2026-07-03-flow-interface-uxui-spec.md` — **the spec you're extending.** Design system (OKLCH tokens, two-font rule, motion, the WCAG contract), the user journey, all 14 screens with layout · states · endpoint bindings · microcopy, the four daemon deltas, the build sequence.
- `docs/active/2026-07-03-flow-interface-ux-prototype.html` — the clickable prototype (open it): dashboard → brainstorm → plan → script → storyboard → animatic → eye-gate → timeline, with the red-pen/pin annotation and the screenplay view.
- `PHILOSOPHY.md` — the soul. "Read like a studio, not a terminal." The human owns taste and timing; the critic proposes; the pipeline is the portfolio piece.
- `CLAUDE.md` — the pipeline architecture, the agent crew (Maya, Sam, Bea, Cy, Flo, Em, Mo, the T3 council), the museum layer.
- `docs/active/2026-07-02-daemon-build-plan-CONVERGED.md` — the API contract the UI binds to (the state machine, `next_action`, the endpoints). **Every new idea must be feedable by this daemon, or flagged as a new delta.**
- `.claude/skills/brainstorm-front-door/SKILL.md` — the front-door brainstorm skill the Brainstorm screen wraps.

## What's already locked (build on it, don't redo it)

- **Aesthetic — Direction C: "warm chrome, dark stage."** Warm-paper studio chrome (paper `#FBF5E9`, ink `#23201B`, teal `#0A3E42`) wrapping a dark judging stage (`#15161A`, teal-bright `#37C7A6`) where the art lives. The load-bearing idea: *warm where you work, neutral/dark where you judge* — the art is the subject and art needs the right wall.
- **Type:** two families only — Newsreader (serif, "what you read") + JetBrains Mono ("what you scan"). Same as my portfolio, so the app and portfolio read as one studio.
- **Interaction model, resolved:** top stepper (not a left rail); a docked command-bar chat; hybrid advance (auto frame-to-frame in the eye-gate, pause at stage boundaries); keyboard-first eye-gate; adaptive run-view (the run *presents* the gate).
- **The signature trio:** the warm/dark seam · the red grease-pencil critic mark (Em in the margin, the annotation pen) · the cel-flip on frame advance.
- **The differentiator:** anima wraps the *same surfaces as Flow* around a **gated pipeline** — the cost preview before spend, Em's critic read, the Bible lock, the human-owned animatic, the run state that always knows your next move. That opinion is the thing Flow can't show.
- **The a11y contract** (WCAG 2.1 AA) is written into the spec — honor it in every new idea.

**Don't reopen these.** Add to them.

## The bar — what "my personal AI animation studio" has to feel like

Push on all of these; they're the scoring rubric for every idea you generate:

1. **Beautiful and clean** — restrained, crafted, nothing gratuitous. The tool disappears into the work.
2. **Fast** — it's a daily tool; the 80% loop (review → approve/retry) is a sprint, keyboard-first.
3. **Reads like a studio, not a terminal** — warmth, editorial voice, the pencil-test materials (paper, hole-punch, exposure sheet, the character).
4. **The pipeline's opinion is visible** — the gates, the cost, the critic, the run state are the craft, not chrome to hide.
5. **The crew are co-creators with presence** — Maya, Sam, Bea, Cy, Flo, Em, Mo are named agents; they should feel like a crew I direct, not faceless functions.
6. **It's *mine*** — it remembers my taste, carries my voice and my character, and feels like walking into my own studio. The unfakeable part.
7. **The museum is alive** — every approve/reject/retry is portfolio evidence; the "how" is visible.

## Stage 1 — Deep research (use the `deep-research` skill)

Run genuine, cited deep research. For **every** finding, extract three things: **the pattern** (what they do), **why it works**, and **steal / avoid** (what transfers to anima's Direction C, what would break it). Organize by category. Search widely; use real sources.

Research these categories, aimed squarely at anima's actual problems:

- **A · Professional 2D animation software** — Toon Boom Harmony & Storyboard Pro, TVPaint, **Procreate Dreams** (the warm/tactile one — study it hard), Callipeg, RoughAnimator, OpenToonz, Cavalry, Rive. *Find:* the x-sheet / dope sheet / exposure-sheet timeline, onion-skinning, the "paper" feel, keyboard-driven frame workflows, how they present a single frame under scrutiny.
- **B · AI generation studios** — Google Flow, Krea, Higgsfield, Runway, LTX Studio, ComfyUI, Freepik. *Find:* the generate→edit loop, the history filmstrip, reference/character injection, the "what do you want to change?" pattern, node graphs, and where they feel *powerful* vs *toylike*.
- **C · Dailies / review / approval tools — THE most directly relevant** — Frame.io, Autodesk Flow Production Tracking (ShotGrid), ftrack, SyncSketch, Filestage. *Find:* frame-accurate annotation (the red pen and the pin), review sessions, approve/reject/notes, versioning/attempts, and the *fastest possible review loop*. This is exactly anima's eye-gate and critic gates — steal the best of how real studios run dailies.
- **D · Pro-tool craft aesthetics** — Linear, Figma, Raycast, Arc, Cursor, Superhuman, Notion. *Find:* how they are clean + dense + fast without feeling sterile; command palettes; keyboard-first accelerators; motion restraint; the small craft details that read as "made with taste."
- **E · Gallery / lightbox / museum presentation** — how galleries and lightboxes present work for judgment (neutral walls, spotlighting, matting), and how museum/exhibit walkthroughs are built online. Feeds the dark stage and the museum layer.
- **F · Timeline / NLE patterns** — DaVinci Resolve, Final Cut, After Effects, Premiere. *Find:* the *simplest* arrange/trim/preview/export subset (my v3 timeline is deliberately not an NLE — find the minimal, elegant version).
- **G · "Personal" / presence / companion software** — what makes a tool feel like *mine* and like it has a crew: memory, naming, agent personalities, ambient atmosphere, ritual, the morning "what's on my easel." Look at how the best tools build presence without gimmick.

**Cross-cutting research questions to answer** (tie findings back to these):
- What does the *fastest* frame-review-and-approve loop in the industry look like, keystroke by keystroke?
- How is spatial annotation (draw + point + comment) done best, and how does it feed back into an edit?
- How do pipeline/node tools show "where am I" and "what's next" without clutter?
- Where does warmth/tactility live in an otherwise-technical tool (Procreate Dreams is the key exemplar) — and how do I get it without tipping into twee?
- What are the *signature delight moments* in great creative tools that don't read as gimmicky?
- What concretely makes software feel *personal* — like it's mine, with my crew?

**Stage 1 deliverable:** a **research brief** — findings by category (pattern · why · steal/avoid · source), plus a shortlist of the **top 15 transferable patterns** mapped to specific anima screens (dashboard, brainstorm, the gates, the eye-gate, the timeline, the museum) and tagged with whether the daemon can already feed it or it needs a new delta. Present it to me and pause for my reaction before brainstorming.

## Stage 2 — Brainstorm (use `/sw-creative-toolkit:brainstorm`)

Feed the research into the brainstorm skill. Generate ideas and features that make anima beautiful, clean, and personal. Diverge wide first (aim for real volume, rotate techniques and lenses to fight semantic clustering), then cluster and surface top picks. Run it in neutral facilitation mode (skip the improv-coach voice — I like it direct).

**Every idea must pass four gates** (state them for each top pick):
1. **Serves the daily workflow first** — beauty in service of the work, never decoration.
2. **Feedable by the daemon** — grounded in the real API, or explicitly flagged as a new delta with what's needed.
3. **Passes the anti-template test** — "why is this *Sean's studio*, not a generic AI tool?" If a generic tool would do it the same way, push further.
4. **Honors Direction C + the a11y contract** — warm/dark, two fonts, the signature trio, WCAG AA.

**Seed the divergence with these angles** (don't limit to them):
- The **crew as characters** — give Maya/Sam/Bea/Cy/Flo/Em/Mo presence, voice, and a visible hand in the work, without gimmick.
- The **museum as a living layer** — the run *becoming* a portfolio walkthrough as I work, felt not bolted on.
- **Ambient studio atmosphere** — the desk, the paper, the light, maybe sound; the feeling of *entering* my studio.
- **The cost and the critic as craft** — surfacing the pipeline's opinion as something beautiful to look at, not a config dump.
- **Onboarding / first-run as "opening your studio,"** and the **morning ritual** ("what's on my easel today").
- **Annotation as art-direction** — the red pen and pin as the way I *direct the crew*, not file bugs.
- **Personalization and memory** — how the app learns and reflects my taste over time.
- **The keyboard-first "instrument" feel** — the app as an instrument I play fast.

**Stage 2 deliverable:** a **brainstorm output** — the full idea list, clusters, and the **top 6–8 picks**, each with: a one-line rationale, the four-gate check, which screen (or new surface) it lands on, the daemon delta if any, and a rough effort read. Keep the wild ideas as exploratory branches. Present it and let me pick.

## Stage 3 — Synthesize

Fold my picks into a **spec addendum (v1.1 proposals)** for `docs/active/` — what to add or change, mapped to screens and daemon deltas, each with your lean. Render inline mockups (visualize widget or HTML) of the 2–3 highest-leverage new ideas so I can see them. Where a pick changes the locked spec, note it clearly so I can ratify it.

## Guardrails (non-negotiable)

- **Ground every idea in the real daemon API**, or flag it as a named new delta. No UI the backend can't feed.
- **Honor Direction C, the philosophy, the anti-slop bans, and the a11y contract.** Don't reopen locked decisions; extend them.
- **The pipeline is the portfolio; read like a studio, not a terminal.** Beauty serves the workflow — a daily tool first, a showpiece second.
- **One decider — me.** Recommend with a lean at every stage; I pick. Use AskUserQuestion at the decision gates. Cite your sources in the research. Render mockups so I can react.
- **Anti-template vigilance.** Before proposing anything, ask: is this drifting toward a generic-AI-tool or generic-creative-tool template? If yes, push until it's specifically *my studio*.

Start by reading the ground-truth files, then run Stage 1.
