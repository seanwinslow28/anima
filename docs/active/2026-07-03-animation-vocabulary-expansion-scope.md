# Animation vocabulary expansion — from six registers to a style powerhouse (scope + next-session kickoff)

**Date:** 2026-07-03
**Status:** Scope + kickoff — documents the near-term register-extension pilot (the immediate next Claude Code session) and the long-term multi-animator powerhouse (a sidequest after the front door's DoD). **Not a build; not a full plan** — it frames the problem, records the decisions, and sets up the sessions that do the work.
**Relation to ROADMAP:** this is a facet of the **active "outward turn — the tool + more characters/styles"** workstream (ROADMAP §Current focus), which already names *"a second character in a different style — does any of the pipeline hold outside pencil-test?"* as the concrete first test of the many-styles goal. This doc is that test, made concrete by two real pieces.
**Trigger evidence:** the two live front-door ART-VIZ passes ([GRANDMASTER](../../briefs/2026-07-02-grandmaster/concept.md), [ai-guru](../../briefs/2026-07-02-ai-guru-pilot/concept.md)) — both locked a register the six-vocabulary doesn't have.

---

## 1. The trigger — every real piece needs a register the six don't have

The closed `style_register` vocabulary is six values: `pencil-test-colored`, `pixel-art-8bit`, `line-art-only`, `watercolor`, `photoreal`, `3d-rendered`. **Both of Sean's real pieces landed outside it:**

- **GRANDMASTER** locked **Route B — Tartakovsky's *Primal* register** (raw, visible, weight-varying hand ink; gritty painterly texture) over the orchestrator's buildable `pencil-test-colored` lean. The nearest existing register (`line-art-only`) mandates bold uniform outlines — the *opposite* of Primal's sketch. Flagged in the concept doc's "buildability gap" and `[L16]/[L17]`, kept-not-softened. **Cy cannot author the GRANDMASTER Bible until this register exists.**
- **ai-guru** locked **Route A — Ren & Stimpy** in a `90s-nicktoon-grossout` register, carried into both character seeds' `style_register` with the NEW-flag + doctrine pointer. No register-safe fallback existed at all.

This is the signal: **register-blindness is the norm, not the edge case.** The front door reliably *surfaces* the gap (the good-ART-VIZ rubric's criterion 6 fired on both), and reliably *routes the fix to Cy* — but the fix itself (extend the vocabulary) has never been built, because until a real piece was greenlit it was speculative. **GRANDMASTER greenlights it.**

## 2. Two horizons

| | **Near-term pilot (NEXT session)** | **Long-term powerhouse (sidequest, after front-door DoD)** |
|---|---|---|
| Goal | Author the `genndy-primal` register so Cy can build GRANDMASTER | A systematically growing, still-**closed**, first-class style vocabulary — anima builds *whatever* style, deliberately | 
| Driver | A production blocker (GRANDMASTER) | The portfolio thesis: "a pipeline for whatever 2D character/style I decide to make" |
| Scope | One animator, one register, deeply researched — the reusable *pattern* | Many animators / animation types, each researched, added via the same pattern |
| Consumer | GRANDMASTER's Cy Bible pass (and, next, ai-guru's `90s-nicktoon-grossout`) | Every future piece the front door surfaces a new register for |
| Output | 1 new register + its Cy "what good looks like" block (+ maybe a style skill) | The register library + the extension playbook + per-style research |

The near-term pilot **is** the first instance of the powerhouse pattern — do genndy well and the reusable workflow (research → register → Cy block → optional style skill → neutrality markers) falls out for free.

## 3. The mechanism already exists — the doctrine 3-step

[`docs/architecture/prompt-style-neutrality-doctrine.md`](../architecture/prompt-style-neutrality-doctrine.md) already specifies **how** a register is added, deliberately, not inline:

1. **Extend the closed vocabulary** in [`pipeline/criteria.py`](../../pipeline/criteria.py) (+ the `character.yaml.template` comment) — the schema-level first-class commitment.
2. **Add a `## What good looks like — {register}` block** to `cy-character-designer-context.md` (three sample `IR.*` entries + a four-paragraph risk-bible excerpt in the new register's vocabulary).
3. **Update `_STYLE_REGISTERS` + `_REGISTERS_TO_MARKERS`** in [`tests/test_prompt_style_neutrality.py`](../../tests/test_prompt_style_neutrality.py) — the register's load-bearing visual markers.

**The load-bearing constraint the powerhouse must not break:** the vocabulary stays **closed** — each register is authored deliberately with its own "what good looks like" block and neutrality markers. The powerhouse is *a bigger closed vocabulary + a reusable extension pattern + deep per-style research*, **not** an open-ended freeform style string. That closedness is what keeps every agent prompt style-neutral and testable (the doctrine's whole thesis: *validators cannot recover taste that was absent at generation time*). Scaling to fifty registers without that discipline turns the architecture decorative.

**Already captured (raw material for the research):** each concept doc carries a per-piece **timing/craft bible** (GRANDMASTER's 8 Tartakovsky directives; ai-guru's 8) + the money-shot mechanic + the three Flow-ready route prompts. That prose is exactly what a register block + a style skill would be extracted from.

## 4. Near-term — the `genndy-primal` register pilot (the immediate next session)

**Why now / why it bends nothing:** it's within the active outward-turn workstream (*more styles*), and it's a **production blocker** for GRANDMASTER — not a speculative new feature. Reordering *which piece of the outward turn* comes next (register before front-door Slice 4) is a within-workstream call; it opens no new workstream. Sean's call, 2026-07-03.

**What the session does:**
- **Deep research on Genndy Tartakovsky's craft** — with an emphasis on the ***Primal* register specifically** (the locked GRANDMASTER pick), distinct from *Samurai Jack*'s flat-no-outline register (they are mutually exclusive looks, per `[L16]`). Tartakovsky is a master and one of Sean's favorites — the research should be **extensive and first-class**, the kind of thing Fable 5's parallel deep-research subagents are built for. Sources beyond the concept doc's starter list; the goal is a real understanding of *what makes the look the look* (line treatment, palette logic, silhouette/hold timing, texture), not a surface pastiche.
- **Author the register via the doctrine 3-step** — `genndy-primal` (or the name the research settles) into the closed vocabulary + a Cy "what good looks like" block + neutrality markers.
- **Prove it green** — a Cy authoring smoke (stub-green first; then, when Sean's ready, a costed Bible pass for a GRANDMASTER character) confirms the register drives Cy correctly and the neutrality test stays green.
- **The form question (standalone skill vs. folded block) is decided *by* the research** (Sean's call, 2026-07-03): the research reveals how much reusable structure Tartakovsky's style has. My prior lean (fold first, promote on 2nd reuse) is a default the research can override — e.g. if the AKCodez scaffold (master template + timing bible + worked examples) has clear standalone value across Primal *and* Samurai-Jack looks, a standalone `genndy-tartakovsky` skill may earn its place immediately.
- **Then ai-guru's `90s-nicktoon-grossout`** rides the same pattern (second instance — the first reuse that tests the standalone-vs-folded promotion trigger).

**Method:** this is a genuine brainstorm + build, so run it like the front-door slices — a co-planned design (Opus + Codex + red-team) *if* the shape is non-obvious, then TDD/stub-green, `superpowers:verification-before-completion`, the two md5 guards held (a register extension touches `criteria.py` + the neutrality test + `cy-character-designer-context.md`; it does **not** touch the two frozen guards). Leverage Fable 5's deep-research capacity for the Tartakovsky pass — don't constrain it.

## 5. Long-term — the multi-animator powerhouse (sidequest, after the front door's DoD)

**The vision (Sean's, 2026-07-03):** *"anima is about creating animations in whatever style I want, not just 6 style choices."* Turn anima into a powerhouse for animation by researching and incorporating many animators and animation types — each a first-class, deliberately-authored register (or family of registers).

**The approach (a systematic scaling of the pilot pattern):**
- **A per-style research pass** (Fable 5 deep-research, parallelizable per animator/style) → the craft understanding.
- **The doctrine 3-step** per register → first-class vocabulary + Cy block + neutrality markers.
- **Optional per-animator style skills** (the AKCodez scaffold) where a look has enough reusable structure and ≥2 consumers.
- **A growing-but-closed vocabulary** — the powerhouse is scale *with* the closedness discipline, not without it (§3).

**Candidate animators / styles / animation types to research (a starter list — the sidequest expands it):**
- *Animators/studios:* Tartakovsky (Primal grit; Samurai-Jack flat-no-outline), John K / Ren & Stimpy (`90s-nicktoon-grossout`), Miyazaki/Ghibli (painterly cel), the Spider-Verse comic-halftone-plus-motion look, Fleischer/Cuphead 1930s rubber-hose, UPA mid-century limited-modernist, Bakshi/Linklater rotoscope, Adventure Time / CN flat-graphic, Aardman claymation.
- *Animation types/media:* cel/traditional, cutout, stop-motion/clay, vector-flat, painterly, sketch/pencil (have it), pixel-art (have it), rotoscope, mixed-media/collage.

**Open questions the sidequest resolves:**
- Standalone-skill-per-animator vs. folded register blocks vs. a hybrid library — the general policy (the pilot gives the first data point).
- How the register interacts with Cy's `_REGISTER_CLAUSE_LIBRARY`, Flo's routing (`_REGISTER_MODELS`), and Em's neutrality test as the count grows from 6 → many.
- Where the closed-vocabulary discipline should stay strict vs. where a "register family" abstraction helps (e.g. "Tartakovsky" as a family with Primal + Samurai-Jack members).
- Which generation engines/models each register needs (NB2 today; some looks may want a different transport — this connects to Flo's route table and the fal/self-hosted-FLUX ticket).

## 6. Decisions recorded (2026-07-03, AskUserQuestion)
1. **The fresh Opus 4.8 session plans Slice 4 (STRESS-TEST) in full + roadmaps the remaining front-door pieces** (the SPEND-OK/Higgsfield render gate, front-door museum capture, the seeds→Cy→registration bridge). Prompt below / in the handoff message.
2. **The register-extension work is the *immediate next* session, before Slice 4** — unblock GRANDMASTER first. The Opus/Slice-4 session names it as the parallel priority but does **not** plan it.
3. **The genndy build form (standalone skill vs. folded register) is decided *after* the research** — not pre-committed.

## 7. Sequencing + anti-drift honesty
Order: **(next) the `genndy-primal` register pilot → (then) front-door Slice 4 STRESS-TEST → (after ①'s DoD) the powerhouse sidequest.** The register pilot runs ahead of Slice 4 by Sean's call; this is honest against the anti-drift contract because the register work is (a) *within* the active outward-turn workstream, not a new one, and (b) a *production blocker* for a greenlit piece, not a speculative rabbit hole. The front door still reaches its Definition of Done (Slice 4 + the roadmapped pieces) — it is not abandoned, just interleaved behind one production unblock. If the register pilot starts sprawling into the full powerhouse before GRANDMASTER is unblocked, that *is* drift — hold it to the one register the production needs, and defer the rest to the post-DoD sidequest.

## 8. Next-session setup — the `genndy-primal` register brainstorm
**Read first:** this doc; [`prompt-style-neutrality-doctrine.md`](../architecture/prompt-style-neutrality-doctrine.md) (the 3-step); the GRANDMASTER concept doc's "Genndy style + timing bible" + "buildability gap" + Route B; `cy-character-designer-context.md`'s existing "what good looks like" blocks (the shape to mirror); [`pipeline/criteria.py`](../../pipeline/criteria.py) (the closed vocabulary) + [`tests/test_prompt_style_neutrality.py`](../../tests/test_prompt_style_neutrality.py).
**Decide:** the register name; standalone-skill vs. folded (from the research); the Cy block content; the marker phrases; the smoke that proves Cy drives correctly.
**DoD for the pilot:** `genndy-primal` is a first-class register (3-step done, neutrality test green, both md5 guards held), a Cy authoring smoke is stub-green, and the reusable extension pattern is written down so the powerhouse can scale it. **Then** GRANDMASTER's Cy Bible pass is unblocked.
