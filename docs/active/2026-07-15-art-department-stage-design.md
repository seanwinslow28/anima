# The Art Department — a visual-development stage between the Front Door and Cy

**Date:** 2026-07-15
**Status:** Design — ratified in a live grill with Sean (2026-07-15). Design only; no implementation this session.
**Persona:** **Artie**, an art-director (proposed — see §12). Domain lens: the [`creative-director`](../../.claude/skills/creative-director) skill.
**Prompted by:** the [2026-07-14 GRANDMASTER character-design sprint](../anima-test-runs/2026-07-14-grandmaster-character-design-sprint.md), which ran an entire human-driven visual-development loop *outside* the pipeline and proved a stage was missing.

---

## 1. The one-sentence goal

Give anima a **playground for finding a piece's look and cast** — a relentless, one-question-at-a-time art-direction room (in the mold of the [Brainstorm Front Door](../architecture/pipeline-architecture-v1.md#brainstorm-front-door-①--the-creative-entry-point-to-phase-0) and Grill-Me) that reads the brief, interrogates Sean about style, character, and world, offers suggestions grounded in the idea, plays with cheap look-tests, and narrows a wide exploration down to the exact bundle Cy and the rest of the pipeline consume: **ratified anchors, a locked register, and the reproducible prompt pack that hits Sean's vision.**

## 2. Why it exists — the missing middle

The GRANDMASTER sprint set out to run a piece through the pipeline and instead discovered a whole creative loop with no home. Designing the kid and the grandma meant: personality→visual design, look-testing the register on cheap generations, then expanding to backgrounds, the birthday girl, background children, the host dad. That loop is **neither the front door nor Cy:**

- **The front door** is deliberately *lean, pre-greenlight, and mostly $0*. Its whole proven identity (four slices, two red-teams) is "don't step out of the room for a bounded move, don't build render/spend machinery ahead of need, stay prompt-only." Its ART-VIZ step emits **≥3 route prompts as prose** and explicitly *defers the render path and the style skill to "the first greenlit piece's Cy authoring run."* Its output is declared **"Maya-ready, not GENERATE-ready,"** and [`manifest_gap_report.md`](../../pipeline/frontdoor/emit.py) *names* the seed→Bible gap it stops at.
- **Cy** is the downstream that *requires a non-empty `characters/{id}/source-refs/` before it will start*, and bakes an **already-locked** design into Bible plates.

The Art Department is the stage that **fills the gap the front door names.** It consumes terse character seeds + a style-route pick and produces the ratified anchors + locked register Cy needs to begin. It is a *different lifecycle phase* from the front door — post-greenlight, real design commitment, real (if cheap) spend — which is exactly why it earns its own stage rather than bloating the front door or overloading Cy.

The field report also flagged the load-bearing workflow discovery, which this design is built around: **the winning path was the pipeline producing a prompt pack + a ChatGPT batch-orchestration prompt, with Sean driving the final generation in the web app** — where his best taste work happens. In Sean's words: *"This is about playing around and finding the right style. Not reading the brief and register and giving me a prompt pack based on those. It should be a fun playground for art and characters."*

## 3. Where it sits

```
Brainstorm Front Door  →  THE ART DEPARTMENT  →  Cy (Character Bible)  →  Maya / Sam / Bea / GENERATE …
   (spark → seeds +          (seeds → ratified          (source-refs →
    style route, $0)          anchors + locked            baked Bible)
                              register + prompt pack)
```

Opt-in and additive, exactly like the front door: a piece whose look is already locked skips the Art Department entirely, and anything already carrying ratified `source-refs/` is byte-identical to today.

## 4. Architecture — an orchestrator that runs the room, over a thin code seam

Mirror the front door's proven two-layer split (it is the reference implementation this stage copies):

- **The skill layer** (`.claude/skills/`, human-facing, markdown). **`art-department`** is the **user-invoked orchestrator** — it runs the room, owns every locked decision, and is the only thing that emits the bundle. Like the front door, it reaches for model-invoked discipline skills *only where a sustained, genuinely-different mode earns one*, and inlines the bounded moves:
  - **`artdept-interrogate`** (a skill) — the **relentless art-direction grill**, one question at a time, with a generic-answer detector that pushes toward *named specifics* (not "make him look cool" but "square black glasses a size too big, sliding down his nose"), gated by a creative-director **North Star** (the six-point Identity/Style/Composition/Continuity/Technical rubric adapted for design). This is the spine Sean asked for — the reason the room reads like `/brainstorm-front-door` and `/grill-me`. It earns a skill for the same reason `frontdoor-interrogate` does: it is a long, sustained, distinct way of behaving, not a bounded authoring move.
  - **`artdept-synthesize`** (a skill) — synthesize-don't-interview; writes the bundle from the running session sidecar and owns the emit-seam call.
  - **Inline orchestrator disciplines** (no sibling skills, following the front-door reversal where EXPAND/ART-VIZ/STRESS-TEST shipped inline): the **micro-expand** opener (alternate visual directions before grilling), the **look-test discipline** (write candidate prompts, cheaply render a few, react), and the **cast-&-world expansion** discipline. Each is a section of the room, not a mode-switch. *(Promotion trigger, YAGNI-honest: any of these earns a skill only if ≥2 live runs show the inline form underperforming — the same bar the front door set.)*
- **The code seam** (`pipeline/artdept/`) — pure Python, credential-free, TDD-tested, CI-green without keys. It validates *structure* and emits the handoff; it never judges taste (taste is Sean's live eye + a rubric, never a unit test). This is the [`pipeline/frontdoor/`](../../pipeline/frontdoor/) pattern applied a second time.

**The propose-vs-decide invariant, inherited from the front door:** a discipline returns only proposals (`observations` / `options` / `recommendation` / `open_questions`); only the orchestrator writes locked-decision fields, append-only, after Sean decides. Sean is the one decider throughout — this is the "critics propose, humans decide" spine, one stage upstream of Cy.

## 5. The loop (how the playground runs)

A resumable, human-gated session — a wide exploration that narrows:

1. **Read + micro-expand.** Artie reads the front-door bundle (or a hand brief), and before grilling, offers a few *alternate visual directions* per principal — divergent starting points, not a single guess.
2. **INTERROGATE — the grill (`artdept-interrogate`).** One question at a time, narrowing: personality→silhouette and shape language; the **loaded object** that carries the character (GRANDMASTER's glasses↔headband swap was the whole transformation); palette and line discipline; the *reference universe* ("which show's look is this reaching for?"); the world's mood and key locations; the register question. The generic-answer detector refuses "make her warm" and pushes to the specific. Artie **gives suggestions grounded in the brief** as it goes — it is a collaborator with taste, not a form.
3. **Look-test forks (inline).** Where a fork is contested (primal-vs-jack), Artie writes candidate prompts using a **kit of techniques** — the **web-search-the-show lever** (*"Use web search to research Genndy Tartakovsky's Primal to accurately depict the art style"* — the sprint's best discovery), register research, the [`prompt-how-much`](../../.claude/skills/prompt-how-much) fresh-vs-edit economy — and can **cheaply generate** a few candidates to show Sean where the fork lands. Sean's eye arbitrates; Artie iterates.
4. **Lock.** When Sean's eye says "that's it," the winner is captured: the anchor is ratified into `source-refs/`, the register is locked (§7), and the **winning prompt recipe** is recorded.
5. **Expand outward.** The same grill-and-lock loop for named secondary cast + key locations + the environment style, reusing the locked hero anchors as references (the GRANDMASTER dependency-map discipline: *edit the anchors you make, never cross styles*).
6. **SYNTHESIZE + emit (`artdept-synthesize`).** Assemble the bundle (§8) — headlined by the **prompt pack + ChatGPT batch-orchestration prompt** Sean takes to the web app for the final high-quality generation.

**In-stage generation is a live tool, but cheap and exploratory** — the definitive batch is always Sean's in ChatGPT. The stage's job is *find the look with Sean*, then hand him the reproducible recipe.

## 6. Scope boundary — the one crisp line

The line is **designed anchor vs generation guidance**, and it is checkable:

| Gets a designed, locked anchor (Cy-Bible-worthy) | Covered by generation guidance (never individually designed) |
|---|---|
| Every principal + every named / recurring secondary character | Anonymous background extras, set-dressing |

**The world:** key location/background designs + a locked `environment-style.md` note — the backgrounds that set the visual identity, not every backdrop. Anonymous extras and props inherit the look through the prompt pack + the locked register, not through bespoke design.

## 7. Register behavior — pick, or trigger authoring

The Art Department is where a register gets **truly locked** — the look-test *is* the lock (primal-vs-jack was exactly a look-test lock).

- **Pick by default** — look-tests over the closed vocabulary in [`pipeline/registers.py`](../../pipeline/registers.py).
- **On no-fit** — surface the gap and **hand off to the style-register-authoring playbook** ([R→S→B](../architecture/style-register-authoring-playbook.md)) as a *called dependency*. The Art Department **never inline-authors a register** (that would violate the [prompt-style-neutrality doctrine](../architecture/prompt-style-neutrality-doctrine.md)'s "extend deliberately, not inline," the playbook's TDD/CI discipline, and fleet-ops).

This is the clean reconciliation with the **active style-register-expansion workstream**: that workstream becomes the **authoring subroutine the Art Department invokes** when a look-test proves nothing fits. They compose; they do not compete. It is precisely the "surface, don't extend" boundary the front door already proved in production (GRANDMASTER's Tartakovsky-flat gap surfaced as a Launch-Blocking Tiger and gated the Bible pass until the register was authored).

## 8. The output contract — a checkable Art Department bundle

Per greenlit piece, validated for *structure* by the code seam (taste is never asserted):

- **Populated `characters/{id}/source-refs/`** for each principal + named character — ratified anchor(s), turnaround roughs, and `notes.md`. This is exactly what Cy ingests to start (it satisfies Cy's non-empty-`source-refs/` precondition).
- **Ratified register** per character (the `style_register` the manifest + Cy read).
- **`design-bible.md`** — the museum-worthy design-intent doc: personality→visual reasoning, the loaded-object logic, the look-test forks and why the winner won.
- **`prompt-pack.md` + the ChatGPT orchestration prompt** — the reproducible recipe and the batch runner Sean hands to the web app (the GRANDMASTER deliverables are the reference shape: fresh-vs-edit economy, the dependency map, two-style folders, checkpointed batches).
- **World set** — key location designs + `environment-style.md`.
- **Cast list** — named cast (→ anchors) vs extras (→ generation guidance).
- **`artdept.json`** handoff descriptor + an updated **gap report** naming which characters are now design-complete vs which still need a Cy Bible + manifest registration.

**Code seam:** `pipeline/artdept/` — `bundle.py` (schema + parse/render/validate), `emit.py`, `validate.py`, `cli.py` → `python -m pipeline.artdept validate <dir>`. Pure Python, credential-free, no schema field without a real consumer (the front door's no-schema-theater discipline).

## 9. The input contract

Consumes the **front-door bundle** (`concept.md` + `00_studio_brief.md` + `character_seeds.yaml` + `frontdoor.json`). **Additive:** a hand-written brief that skipped the front door is also accepted (the room can seed characters from prose — it is a playground, not a strict consumer), and a piece with an already-locked look skips the Art Department. Anything already carrying ratified `source-refs/` is byte-identical to today.

## 10. Spend & fleet-ops posture *(proposed — open for Sean)*

Because in-stage generation is a *live playground tool* rather than a rare escalation, a per-render `SPEND OK` phrase is too heavy. Proposed: a **session budget** — Sean declares a credit ceiling at the start (Higgsfield credits / subscription, **never `ANTHROPIC_API_KEY`**); cheap look-tests draw against it; the room announces spend as it goes and **hard-stops at the ceiling.** Otherwise fleet-ops is unchanged: one known owner, one isolated worktree per run, clean teardown.

## 11. Museum tie-in

The look-test forks are native museum content — *"we tried primal, we tried jack, here's the fork and why the eye chose."* The `design-bible.md` + the discarded look-tests are draft→pro evidence the Museum layer already renders. The visual-development story becomes a free byproduct, per PHILOSOPHY's "the pipeline is the portfolio piece."

## 12. Open items — proposed, not decided

- **Persona name.** Proposed: **Artie** (Art Department → art director → Artie; warm and mnemonic like Maya/Cy/Bea). Alternates: **Ren**, **Dex**.
- **Spend governance.** The session-budget model (§10).
- **Build sequencing (anti-drift).** This is a **newly-scoped workstream**, and the ROADMAP's active thread is style-register expansion. *Designing it this session does not violate the anti-drift contract (no build).* For building: recommendation is that it does not compete with the style-register thread — it is the **home that thread plugs into** (§7) — and should be sequenced as the **next workstream once the current taste-driven register thread reaches its DoD**, with the first real Art Department run naturally paired with "the first non-pencil piece" (ROADMAP's NEXT; GRANDMASTER the obvious first customer). Whether it jumps the queue is Sean's call, to be reflected in ROADMAP before any build.

## 13. What this design deliberately does NOT do

- **Does not generate the final art.** The high-quality batch is Sean's, in ChatGPT. In-stage generation is cheap/exploratory only.
- **Does not author registers.** It picks, or it triggers the playbook (§7).
- **Does not individually design extras or every background** (§6).
- **Does not mutate `manifest.yaml`** — like the front door, it names the gap; registration is downstream.
- **Does not add a schema field without a consumer**, or a discipline-skill for a bounded move (§4).

---

*Provenance: ratified in a live design grill with Sean, 2026-07-15. Reference architecture: the [Brainstorm Front Door](../architecture/pipeline-architecture-v1.md#brainstorm-front-door-①--the-creative-entry-point-to-phase-0) (①) and its [`pipeline/frontdoor/`](../../pipeline/frontdoor/) code seam. Origin evidence: the [GRANDMASTER character-design sprint](../anima-test-runs/2026-07-14-grandmaster-character-design-sprint.md).*
