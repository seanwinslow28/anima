# Referenced Skills — Detail Reference (for the Front-Door + Daemon builds)

**Date:** 2026-07-02
**Why this exists:** the [① front-door build plan](2026-07-02-brainstorm-front-door-build-plan.md) and [② daemon-foundation build plan](2026-07-02-flow-interface-daemon-foundation-plan.md) reference skills that live in Sean's *global* plugin set but are **not** in `anima/.claude/skills/`. This doc vendors each missing skill's essential details so Claude Code (or Fable 5) building in anima has the substance inline — no plugin install required. Faithful to each SKILL.md; organized by the build stage it powers.

---

## Already in `anima/.claude/skills/` — no vendoring needed

`creative-director` · `writing-voice-modes` · `gemini-image-gen` · `gemini-pencil-animation-image-gen` · `image-generator-prompt-science` · `frontend-design` · `prompting-beautiful-ui` · `storytelling-architecture` · `screenwriting-modes` · `script-writing` · `writing-critique` · `writing-humanity-pass`. Reference these directly.

## Where each *missing* skill is used

| Skill | Source | Build | Stage / role |
|---|---|---|---|
| `brainstorm` | sw-creative-toolkit | ① | EXPAND (divergence engine) |
| `innovation-strategy` | sw-creative-toolkit | ① | EXPAND (idea-qualifying lenses) |
| Grill Me `grill-me`/`grilling` | mattpocock/skills | ① | INTERROGATE (the relentless loop) |
| `voiceprint-interviewing` | voiceprint | ① | INTERROGATE (elicitation craft) |
| `storytelling` | sw-creative-toolkit | ① | INTERROGATE (narrative spine) |
| AKCodez style skills | AKCodez (ext.) | ① | ART-VIZ (prompt-craft shape to customize) |
| Grill Me `prototype` | mattpocock/skills | ① | ART-VIZ ("variations behind a switch") |
| `pre-mortem` | pm-execution | ① | STRESS-TEST |
| `strategy-red-team` | pm-execution | ① | STRESS-TEST |
| `problem-solving` | sw-creative-toolkit | ① | STRESS-TEST (support) |
| Grill Me `to-prd` | mattpocock/skills | ① | SYNTHESIZE (synthesize-don't-interview) |
| `brainstorming` | superpowers | ①②  | the front-door pattern + pre-build gate |
| `test-driven-development` | superpowers | ①② | build discipline |
| `using-git-worktrees` | superpowers | ①② | build discipline |
| `verification-before-completion` | superpowers | ①② | build discipline |
| `impeccable` | impeccable | ② | v1 UI polish (with `frontend-design`) |

---

# ① — EXPAND stage

## sw-creative-toolkit: `brainstorm`
- **Purpose:** technique-driven ideation on a *defined* topic — drive to 100+ ideas before any convergence. Persona "Carson" (improv coach).
- **Core techniques (curated):** SCAMPER, Six Thinking Hats, Brainwriting/Round Robin, Reverse Brainstorming, Worst Possible Idea, Five Whys, Random Word, Mind Mapping, Crazy 8s, Yes-And Building, Provocation, Cross-Pollination, Alien Anthropologist, Persona Journey, Dream Fusion Lab, Time Shifting, First Principles, Resource Constraints, Trait Transfer, Sensory Exploration, Emotion Orchestra. Four modes: User-pick / AI-recommend / Random / Progressive.
- **Process:** (1) Establish Topic & Constraints (+ quantity goal, energy state); (2) Select technique mode; (3) Run for volume; (4) Capture → Cluster into 5–10 themes → surface 3–5 Top Picks + Exploratory Branches + Next Steps. Checkpoints after phase 1 and 3.
- **Hard rules:** defer judgment; quantity over quality; wild ideas welcome; build ("Yes, and") not critique; cluster **only after** expansion. **Signature rule: anti-bias rotation — shift creative domain every ~10 ideas** (practical → UX → edge-case → cross-domain analogy → absurd → failure-mode → sensory → time-shifted), because "LLMs cluster semantically without prompting." Keep three prose registers separate (facilitation voice / clean artifact / plain rationale). The good ideas live past #50.
- **Borrow for EXPAND:** the domain-rotation-every-10 rule (fights the LLM's semantic clustering) and the Topic→Generate→Cluster→Top-Picks skeleton *is* the adaptive-expand flow.

## sw-creative-toolkit: `innovation-strategy`
- **Purpose:** turn a fuzzy strategic question into a sequenced, defensible strategy. Persona "Victor" (chess grandmaster).
- **Core frameworks:** Porter's Five Forces, TAM/SAM/SOM, PESTLE, competitive positioning; **Jobs-to-be-Done (functional / emotional / social jobs)**; **Blue Ocean four-actions (Eliminate / Reduce / Raise / Create)**; Business Model + Value Proposition Canvas; moat categories (network effects, scale, switching costs, brand, IP, data loops, regulatory, distribution); Three Horizons; Scenario Planning; Lean Startup.
- **Process:** 8 phases, Strategic Question → Market/Forces → JTBD → Blue Ocean → Business Model → Moats → 3-phase roadmap (each with a **decision gate**) → Assumption Validation Plan.
- **Rules:** brutal truth over consensus; moats are **structural not narrative**; substitutes + non-consumption matter more than the obvious competitor; every strategy needs an explicit **Abandon Trigger**.
- **Borrow for EXPAND:** JTBD's functional/emotional/social split and the "structural vs narrative" honesty test are strong idea-qualifying lenses when EXPAND needs to weigh which avenue is worth pursuing.

---

# ① — INTERROGATE stage

## Grill Me: `grill-me` / `grilling` (mattpocock/skills, external)
- **Purpose:** interview the user relentlessly about a plan/design until shared understanding — stress-test before building. (`grilling` is the reusable loop behind `grill-me`.)
- **Method (the whole thing — these skills are tiny):** "Walk down each branch of the design tree, resolving dependencies between decisions one at a time. **For each question, provide your recommended answer.**"
- **Rules:** **ask one question at a time** (multiple at once is bewildering — wait for each answer); **if a question can be answered by exploring the codebase, explore instead of asking.**
- **Borrow for INTERROGATE:** the minimal high-signal loop — one question at a time + always volunteer your recommendation + resolve the dependency tree branch by branch + discover-don't-ask. (This is exactly how the piñata dry-run was run.)

## voiceprint: `voiceprint-interviewing`
- **Purpose:** the interview *craft* — pull a person's real voice/idea out through questions, not a questionnaire.
- **The one rule:** collect **EVIDENCE, never DESCRIPTIONS** (a real quoted line/title/detail beats "witty, conversational").
- **Techniques:** the **generic-answer detector** (after every answer, check for a *named specific* — title/line/place/person/price/date; if none, push); the **follow-up ladder** (climb one rung at a time: exact instance → the why → the scene → the association → the embarrassing version); the **respectability correction** ("the wrong-but-true answer beats the impressive one"); per-stage **saturation** counts (interview ~8–15 specifics).
- **Rules:** if you catch yourself asking "how would you *describe* your…" — **stop, ask for an instance.** Never batch into a numbered list. Capture **verbatim — looseness is data.** Deep beats wide.
- **Borrow for INTERROGATE:** the single most transplantable elicitation engine — the generic-answer detector + follow-up ladder is how the front door extracts a *specific* spark from a vague one instead of accepting mush.

## sw-creative-toolkit: `storytelling`
- **Purpose:** take a fuzzy "I need a story" to a complete, platform-adapted narrative in the *user's* voice. Persona "Sophia" (bardic).
- **Frameworks:** Hero's Journey, StoryBrand, Three-Act, **Pixar Pitch/Spine**, Before-After-Bridge, Problem-Solution-Benefit, Situation-Complication-Resolution, Brand/Origin/Vision Story, Data Storytelling. Sensory principle: "one vivid detail beats five generic ones."
- **Process:** 9 phases with a **sidecar memory** (`storyteller-sidecar.md`) — load prefs → Purpose/Audience/Subject → Emotional Arc → Framework Selection → Character & Voice → Draft → Sensory pass → Platform Adaptation → Impact Plan → sidecar update.
- **Rules:** audience first; emotion before information; **one clear arc — don't stack frameworks**; **voice belongs to the user** (facilitation voice ≠ artifact voice).
- **Borrow for INTERROGATE:** the Pixar-spine/Three-Act frameworks give the narrative backbone for a short; the **sidecar-memory pattern** (persist a user's confirmed preferences + anti-patterns between runs, fall back to inline if unwritable) is how the front door remembers Sean across sessions.

---

# ① — ART-VIZ stage

## AKCodez style skills (external — reference to *customize*, not install)
Five Seedance-2.0-on-Higgsfield prompt libraries (`01-cinematic`, `03-cartoon`, `05-fight-scenes`, `08-anime-action`, `04-comic-to-video`). Drive generation through **your Higgsfield MCP, not their Playwright automation.**
- **Shared scaffold (the borrowable shape):** platform I/O spec (up to 9 img / 3 vid / 3 audio; the **`@material[name]` token** to reference uploaded assets inside a prompt — fully worked in `01-cinematic`); **the 2-Second Hook Framework** (10+ hook templates, hook-stacking); a **Master Prompt Construction Template** with `[BRACKETED]` variables; a **Timeline Segmentation Guide** (4s/8s/10s/15s beat structures); a **Camera-Movement Encyclopedia** (15–20+ named moves); Lighting/Color/Sound libraries; a style encyclopedia; **5 large fully-worked example prompts** each; Common-Mistakes + Platform-Optimization + Output-Instructions.
- **What each covers:** `01-cinematic` (film/noir/anamorphic/DoF — best `@material` treatment) · `03-cartoon` (2D/cel/Ghibli/rubber-hose + the 12 animation principles) · `05-fight-scenes` (combat choreography, 30+ named moves, multi-character coordination, impact effects) · `08-anime-action` (limited-animation-with-impact-frames, speed lines, shonen/mecha/isekai) · `04-comic-to-video` (panel-to-motion, reading-order, speech-bubble/onomatopoeia).
- **Borrow for ART-VIZ:** the repeatable scaffold — **2-second hook → master template with bracketed variables → timeline segmentation → domain encyclopedia → 5 worked examples** — is the shape for the `genndy-tartakovsky` style skill (fill it with this session's research sheet), plus `05-fight-scenes` + `03-cartoon` are the closest genre references for the samurai-piñata work.

## Grill Me: `prototype` (mattpocock/skills, external)
- **Purpose:** build throwaway code/output that answers a design question before committing. "**The question decides the shape.**"
- **Two branches:** LOGIC ("does this state model feel right?" → a tiny interactive terminal app) vs **UI ("what should this look like?" → several *radically different* variations on one route, switchable via a URL param + a floating bottom bar).**
- **Rules:** throwaway + clearly marked from day one; one command to run; no persistence; skip the polish; **capture only the *answer*** (the verdict), then delete or absorb.
- **Borrow for ART-VIZ:** the UI branch — generate 2–3 *radically different* style routes, let the human pick, **keep the verdict not the artifacts** — is exactly the "see the look before compute" loop (the piñata's 3 style routes).

---

# ① — STRESS-TEST stage

## pm-execution: `pre-mortem`
- **Purpose:** imagine the launch *failed* and work backward to surface real risks while there's still time to act.
- **The signature taxonomy:** **Tigers** (real problems you personally see → require action) · **Paper Tigers** (others' overblown concerns → document to align, don't invest) · **Elephants** (unspoken worries nobody's validating → investigate). Tigers then classified: **Launch-Blocking / Fast-Follow (30 days) / Track.**
- **Process:** "imagine it ships in 14 days and fails — what went wrong, what did we miss, where were we overconfident" → categorize each failure → classify Tigers by urgency → action plan (Risk / Mitigation / Owner / Due Date) per Launch-Blocking Tiger.
- **Rules:** **default to "Tiger" if unsure**; constructive, not blame-assigning.
- **Borrow for STRESS-TEST:** the Tiger/Paper-Tiger/Elephant trichotomy is a fast, memorable way to triage a raw *concept's* risks; "default to Tiger if unsure" is the right bias for a gate deciding what to flag.

## pm-execution: `strategy-red-team`
- **Purpose:** attack a plan's **load-bearing assumptions now** and return the **cheapest test** for each — sharper judgment, not a longer risk list. Explicitly **NOT** a pre-mortem.
- **The loop:** extract every claim → separate load-bearing from cosmetic → **steelman then attack** (attack the strongest version, no strawman) → write each failure as "**Fails if ___**" (concrete, falsifiable) → **rank by (impact if wrong) × (likelihood wrong) × (cheapness to test)**. Per surviving assumption: Fails-if / Evidence-to-get-this-week / Kill-criterion / Cheapest-test.
- **Output:** "Top Kill-Assumptions (3–5 max)" + "What's Well-Reasoned" + "What I Couldn't Assess."
- **Rules:** **no strawmanning, no generic risk lists, no fabrication** — if a claim is sound, say so plainly. "Five real kill-assumptions with tests beat twenty generic risks." End with what to *do*.
- **Borrow for STRESS-TEST:** the steelman-then-attack + "Fails if ___" + rank-by-cheapest-test loop is the ideal converge/pressure-test after divergence; the "don't manufacture doubt" rule keeps the critique credible.

## sw-creative-toolkit: `problem-solving` (support)
- **Purpose:** diagnose a recurring/unclear-root-cause problem, then generate/evaluate/plan a validated fix. Persona "Dr. Quinn."
- **Methods:** diagnostic — **Is/Is-Not Analysis, Five Whys, Fishbone, Systems Thinking**; constraints — Force Field, **real-vs-assumed constraints** (Theory of Constraints); generation — TRIZ, Morphological, Lateral Thinking, Assumption Busting, Biomimicry; evaluation — Decision Matrix, Risk Matrix, FMEA, Pareto; + PDCA.
- **Rules:** diagnose before prescribing; **symptoms lie, structure doesn't**; the right question beats a fast answer; every solution gets **Adjustment Triggers** ("if X, then pivot to Y").
- **Borrow for STRESS-TEST:** the Is/Is-Not boundary-mapping and "real vs assumed constraints" cut sharpen a fuzzy spark *before* ideation, and give the front door a rigor exit if a concept is structurally broken rather than merely risky.

---

# ① — SYNTHESIZE stage

## Grill Me: `to-prd` (mattpocock/skills, external)
- **Purpose:** synthesize the conversation + context into a structured doc — **do NOT interview, just synthesize what you already know.** (The model for our SYNTHESIZE stage that emits the concept doc + Studio Brief.)
- **Template:** Problem Statement (user's POV) / Solution (user's POV) / **User Stories** (extensive "As an `<actor>`, I want `<feature>`, so that `<benefit>`" list) / Implementation Decisions / Testing Decisions / **Out of Scope** / Further Notes.
- **Rules:** synthesize-don't-interview; **no file paths or code snippets** (they go stale); good tests test external behavior.
- **Borrow for SYNTHESIZE:** the "synthesize-don't-interview" mode + a fixed template with an explicit **Out-of-Scope** section is exactly the clean hand-off artifact — map it onto anima's Studio-Brief contract (`What is this about / Who / Tone / What this is NOT / Format / Medium / Deadline / Non-negotiables`).

---

# ①② — Build discipline

## superpowers: `brainstorming`
- **Purpose:** MANDATORY before any creative/implementation work — turn ideas into designs/specs through dialogue **before** code. (This is itself the canonical "front door" pattern.)
- **The HARD-GATE:** no implementation skill / code / scaffold until a design is presented AND the user approves. 9-item checklist (a task per item, in order): explore context → **offer Visual Companion (its own message)** → clarifying questions **one at a time** → **propose 2–3 approaches with trade-offs + a recommendation** → present design in complexity-scaled sections (approval after each) → write a design doc + commit → spec self-review (placeholder / consistency / scope / ambiguity) → user reviews spec → transition to `writing-plans` (**the only terminal skill**).
- **Rules:** one question at a time; multiple-choice preferred; YAGNI ruthlessly; always 2–3 approaches; incremental validation; decompose multi-subsystem requests first.
- **Borrow:** this is the spine of the front door itself — the HARD-GATE, one-question-at-a-time, 2–3-approaches-with-recommendation, spec-doc + review-gate. Use it to run the *build's* own design phase too.

## superpowers: `test-driven-development`
- **Iron Law:** NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST. **Red → verify-RED (watch it fail for the right reason) → Green (simplest, YAGNI) → verify-GREEN → Refactor (stay green) → repeat.**
- **Rules:** wrote code before the test? **Delete it** ("delete means delete" — don't keep as reference). Real code over mocks. "If you didn't watch it fail, you don't know it tests the right thing." Violating the letter is violating the spirit; no exceptions without the human's OK.
- **Use:** every build slice (① skeleton, ② tracer-bullet) is stub-green-first per this.

## superpowers: `using-git-worktrees`
- **Principle:** detect existing isolation first → use native tools → fall back to git → **never fight the harness.** Step 0: `git rev-parse --git-dir` vs `--git-common-dir` (+ submodule guard). Dir priority: existing `.worktrees/` > `worktrees/` > instruction preference > default `.worktrees/`.
- **Rules:** never `git worktree add` when a native worktree tool exists ("the #1 mistake"); never create one when isolation already exists; verify the dir is gitignored (`git check-ignore`) before creating; don't proceed on a failing test baseline without asking.
- **Use:** one isolated worktree per build (fleet-ops protocol).

## superpowers: `verification-before-completion`
- **Iron Law:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE. **Gate Function:** identify the proving command → run it fresh/full → read full output + exit code + failure count → verify it confirms the claim → *then* claim, with the evidence.
- **Rules:** applies before any "done"/"passing"/"Great!"/commit/PR/task-complete. "Agent said success" → verify independently via VCS diff. Regressions need the full revert→fail→restore→pass cycle. "Claiming complete without verification is dishonesty, not efficiency."
- **Use:** the gate before any slice is called done.

---

# ② — v1 UI polish (daemon plan's cheapest-next-step)

## `impeccable`
- **Purpose:** design/critique/polish production-grade frontend with committed, non-templated craft. (Pairs with `frontend-design`, which anima already has.)
- **Command surface:** Build (`craft`/`shape`/`init`), Evaluate (`critique`/`audit`), Refine (`polish`/`bolder`/`quieter`/`distill`/`harden`), Enhance (`animate`/`colorize`/`typeset`/`layout`/`delight`), Fix (`clarify`/`adapt`/`optimize`), Iterate (`live`). Register split: **brand** (design IS the product) vs **product** (design SERVES the product). Color in **OKLCH**, four-step strategy (Restrained / Committed / Full-palette / Drenched).
- **The AI-slop bans (match-and-refuse):** side-stripe borders, gradient text, glassmorphism-by-default, the hero-metric template, identical card grids, tiny-uppercase-tracked eyebrows on every section, numbered `01/02/03` section markers as default, text overflow. **The cream/sand/beige body background is "the saturated AI default of 2026"** (`--paper`/`--cream` token names are tells). Contrast ≥4.5:1; reduced-motion not optional.
- **Borrow for ②:** the **AI-slop test** (first- and second-order reflex checks) + the ban list are the guardrails that keep the v1 desktop UI from reading as a template; the context-first setup ritual (read `PRODUCT.md`/`DESIGN.md` first) is a good pattern for the interface build. *(Note: the anima portfolio's own warm-paper palette is a deliberate brand choice — impeccable's "cream = slop" ban is about un-considered defaults, not a considered brand token. Apply judgment.)*

---

## The more durable alternative (recommended follow-up)

This doc is the **self-contained immediate fix** — it travels with the repo and needs no install. But it will drift as the upstream skills evolve. The more maintainable option is to **install the actual plugins into anima's `.claude/`** (or add them to anima's plugin marketplace) so the skills are live and invocable:

- **sw-creative-toolkit** (`brainstorm`, `innovation-strategy`, `storytelling`, `problem-solving`)
- **pm-execution** (`pre-mortem`, `strategy-red-team`)
- **superpowers** (`brainstorming`, `test-driven-development`, `using-git-worktrees`, `verification-before-completion`)
- **voiceprint** (`voiceprint-interviewing`)
- **impeccable**
- Grill Me (`mattpocock/skills`) and the AKCodez creative style skills are external — vendor/customize the ones we use (the `genndy-tartakovsky` style skill is the first) rather than depend on them live.

If you install the plugins, keep this doc as the "why each is referenced + what to borrow" index and let the live SKILL.md carry the full detail.
