# Continuation prompt — mascot colored pass + "what should we build next?"

*Paste the section below into a fresh Cowork session. It carries the full state of where
we left off, the immediate thread (mascot colored pass), and — the real ask — a strategic
step-back: read the plan docs and tell Sean whether continuing to polish Cy is the best use
of effort, or whether something higher-leverage is sitting unbuilt. Written 2026-05-31.*

---

## PASTE FROM HERE

You are the creative director / pipeline partner for **anima**, a human-and-agent 2D
animation pipeline (working dir `/Users/seanwinslow/Code-Brain/anima`). Read `PHILOSOPHY.md`
first, then `CLAUDE.md`, then `docs/pipeline-architecture-v1.md`. Honor the maintenance
conventions (append to `CHANGELOG.md` on every change; update `CLAUDE.md` on significant
structural changes; `COMPLETED/` + `OLD/` archive folders; studio-manual voice, prose over
bullet-dumps). Use the task list, and use AskUserQuestion where taste or scope is Sean's
call rather than guessing.

This session has **two threads**. Thread B is the one Sean actually wants the most thought
on — don't let Thread A eat the session.

### Where we left off (state of the world, precise)

Over recent sessions we built the **claude-mascot** Bible's motion layer end to end:

- Wrote a motion-direction brief (`characters/claude-mascot/source-refs/motion-direction.md`)
  — six motions, the mascot's "watchful, a-touch-bouncier limited-animation" movement
  personality, per-key shot list with Seedance anchor pairs, animation-craft notes, pipeline
  mapping, and a drawing checklist. Sean confirmed: all six motions, hop (not scuttle) for
  locomotion, fuller key counts.
- Wrote NB2 exploration prompts (`characters/claude-mascot/source-refs/nb2-pose-sheet-prompts.md`).
- **Sean hand-drew all six motion sheets** (his own pencil keys — the Phase 4 animatic).
  We cropped them into **22 per-pose plates** (`motion_plates/{idle-01..03, look-01..04,
  perch-01..04, alert-01..03, hop-01..05, sleep-01..03}.png`) via column-projection
  segmentation, mirroring sean-anchor's `head-turn-01..09` flat naming.
- **Ingested them into the locked Bible via `bible add`** with **7 new
  `IR.claude-mascot.motion.*` rules** (idle-breath-volume, tilt-is-whole-body,
  perch-weight-and-squash, alert-snap-eyes-stay-dots, hop-arc-and-gravity, sleep-ease-in,
  no-arms-in-motion). Bible is now **25 criteria / 33 plates**, schema 1.2, `content_version
  1.2.0`, **locked preserved**, validates clean. Spec at
  `characters/claude-mascot/motion-additions.json`; audit at
  `runs/2026-05-30-mascot-motion-ingest/bible_audit.jsonl`.
- **Fixed a real bug:** `python -m pipeline.cli bible add` exited 1 silently — the subparser
  was registered but never wired into the dispatch switch in `pipeline/cli/__main__.py`.
  Added the missing branch + a regression test (`test_cli_main_dispatches_bible_add` in
  `tests/test_cli_bible.py`, the first CLI test to invoke `main([...])`). Bible CLI suite 22
  passing.

**Two things flagged for the colored pass** (recorded in `cy-confidence-notes.md`): on the
`hop-*` side plates the near-nub end-cap reads as too large a circle (should be a small
end-cap disc, never a navel/emblem — IR.claude-mascot.anatomy.nub-side-view-endcap); on
`alert-03` the nubs flare arm-like (keep short and forward).

**The ingested motion plates are line roughs (animatic tier) — they carry no color.** Their
plate entries deliberately cite only the form/anatomy/motion rules they honor, NOT the
palette/style register rules. **Sean is doing the colored pencil-test pass himself, in
parallel, right now.**

### Thread A — the colored-pass continuation (the easy thread; do NOT over-invest)

When Sean's colored motion keys land, the work is: (1) re-crop/replace the line-rough
`motion_plates/*.png` with the colored versions (or add them as colored Seedance-anchor
variants — ask Sean which), fixing the hop-disc and alert-nub issues; (2) the colored plates
now satisfy the full register, so their plate entries / a follow-on rule can cite the color
register too; (3) the extreme keys marked ▸ in the motion-direction brief become the **Phase
6 Seedance start/end anchors** — perch and hop chain through their breakdown keys. That path
ends at an actual moving mascot on Sean's shoulder in Act 2. This is mostly mechanical and
well-specified; handle it when the assets arrive, but it is not where the thinking goes.

### Thread B — the real ask: step back and find the highest-leverage next build

Sean's words: *"I don't mind locking in and making sure Cy is perfect, but I also feel like
we've been focused on Cy for a while and I want to make sure there isn't anything else we
could be building and taking advantage of."* He's right to ask. **Take this seriously as a
strategy question, not a checklist.**

Read these, in order, before recommending anything:

1. `PHILOSOPHY.md` — the six load-bearing beliefs. Two are directly relevant: *"the critic
   earns its keep when it proposes fixes"* and *"the pipeline IS the portfolio piece"* (the
   museum is core, not bolted on).
2. `docs/2026-05-26-agent-fleet-brainstorm-v2.md` — **the locked agent-fleet decision
   artifact.** The full persona roster (Maya, Cy, Sam, Bea, Flo, Em, Mo + T3 council
   Codie/Annie/Sage/Chairman + orchestrator), models, and confidence levels. This is the
   map of what the fleet is *supposed* to be.
3. `docs/2026-05-24-pipeline-v2-change-map.md` — the 9-commit sequence (TOP-1..5 + commits
   1–9), the evals workstream, and what each commit unblocks.
4. `docs/2026-05-24-pipeline-v2-brainstorm.md` — the 15-idea brainstorm behind the lock
   (read for *why*).
5. `docs/pipeline-architecture-v1.md` — the canonical 10-phase lock, draft→pro coverage,
   the critic stack, reserved open questions.
6. Skim `docs/production-checklist.md` (Act 1 done, Act 2 Seedance in flight) and the recent
   field reports in `docs/anima-test-runs/` to see how much of the effort has gone to Cy.

**Then do an honest gap analysis.** Here is the shipped-vs-pending map as of 2026-05-31 so
you don't have to rediscover it — verify it, don't trust it blindly:

| Fleet piece | Phase | Status | Evidence |
|---|---|---|---|
| **Maya** (planner) | 0 | ✅ shipped (commit 3) | `pipeline/agents/planner.py`, `cost_estimator.py` |
| **Cy** (character designer) | 2 | ✅ shipped + heavily iterated across ~8 sessions | `character_designer.py`, `nb_pro_runner.py`, `similarity_gate.py` |
| DAG + AgentSpec + criteria | cross | ✅ shipped (commit 4) | `dag.py`, `criteria.py`, `agents/__init__.py` |
| **Em** (T2 vision critic) | 5/6/8 | ✅ shipped (commit 8) | `vision_critic.py`, `patch_stager.py` |
| **Flo** (Phase 5 generation router) | 5 | ❌ NOT built (manifest has a routing comment only) | no agent file |
| **Sam** (scriptwriter) | 3 | ❌ NOT built | — |
| **Bea** (storyboard artist) | 3 | ❌ NOT built | — |
| **T3 council** (Codie/Annie/Sage/Chairman) | 4→5, pre-museum | ❌ NOT built (commit 9 pending) | referenced in prompts only |
| **Mo** + the **Museum capture layer** | parallel | ❌ NOT built (commit 6 — no `museum/` dir exists) | — |
| Animatic Phase 4 ingestion as a phase | 4 | ❌ NOT built as a pipeline phase (commit 7) | — |
| Bake-off sequence (T2 shoot-out, etc.) | evals | ❌ NOT run | `evals/` has scaffolds, no bakeoffs |

The pattern is unmistakable: deep investment in **Maya, Cy, Em, and the DAG core** — and the
**entire right half of the fleet is unbuilt.** Cy in particular has absorbed many sessions.

**Candidate next workstreams — pressure-test these against Sean's actual goals** (a
shippable Act 2 of the pencil test, AND a job-hunt portfolio where *the pipeline itself* is
the differentiator — see `/Users/seanwinslow/Code-Brain/sw-ai-pm-portfolio`, whose museum
walkthrough is meant to read from anima's `museum/` output):

- **The Museum (commit 6 + Mo).** Arguably the highest-leverage unbuilt thing. PHILOSOPHY
  says *"the pipeline is the portfolio piece… the museum is the evidence."* It's the literal
  bridge to Sean's portfolio job hunt, and it's not even scaffolded. Every approve/reject/
  retry we've already run is ungenerated evidence sitting in `runs/`.
- **The T3 critic stack (commit 9 — Codie/Annie/Sage/Chairman).** The *"judge agent will be
  a staple in all my agentic workflows"* belief made real at phase boundaries. $0
  incremental (subscription-absorbed). The vault-critic pattern already exists in
  `code-brain` and could be ported. Closes the critic-as-principle gap.
- **Flo (Phase 5 generation router).** Turns the legacy single-model `generate.py` into the
  routed, cost-tiered pipeline the v2 brainstorm specced. Directly unblocks cheaper, better
  Act 2 generation.
- **Phase 3 (Sam + Bea).** Storyboard/script agents — un-deferred in v2.
- **The bake-off sequence** (T2 shoot-out first). The *"empirical, not vibes"* belief; low
  cost; validates choices already shipped.
- **Animatic Phase 4 ingestion (commit 7).** Timely — Sean just produced motion keys by
  hand; formalizing the animatic→constraint ingestion contract is the natural generalization
  of what we did ad-hoc for the mascot.

**Your job in Thread B:** read the docs, verify the map, then come back with a *recommendation*
— not code. Rank the candidates by leverage against Sean's two goals, name the one you'd
start, say why, and surface the trade-offs (effort, dependencies, what it unblocks, what it
risks). Use AskUserQuestion to let Sean pick the direction before you plan or build. If you
think the honest answer is "actually, finish X about Cy first because Y depends on it," say
that too — but the default hypothesis to disprove is *"we've over-indexed on Cy; the museum
and the T3 critic are the unbuilt load-bearing pieces."*

### How to run this session

1. Read the docs above. Build a task list.
2. Verify the shipped/pending map against the actual repo (`pipeline/agents/`, `museum/`,
   `evals/`, the manifest blocks).
3. Present a ranked recommendation with trade-offs, in studio voice.
4. AskUserQuestion: which workstream to commit to (offer the top 2–3 + "keep polishing Cy").
5. Only after Sean picks: produce a plan (or a kickoff/implementation prompt in the style of
   the existing `docs/*-implementation-prompt.md` / `*-kickoff.md` docs), or begin the work.
6. Handle Thread A (colored plates) whenever Sean drops the colored assets — it's mechanical
   and specified above; don't let it crowd out Thread B.

Source-of-truth docs to keep open: `CLAUDE.md`, `docs/pipeline-architecture-v1.md`,
`docs/2026-05-26-agent-fleet-brainstorm-v2.md`, `CHANGELOG.md`.

## PASTE TO HERE
