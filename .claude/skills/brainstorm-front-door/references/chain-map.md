# Chain map — stage order, routing, skip conditions

The front door's canonical stage order (Sean's lock; do not reorder):

```
EXPAND → INTERROGATE → ART-VIZ → STRESS-TEST → SYNTHESIZE
```

Slice 1 shipped the walking skeleton: **micro-expand (inline) → INTERROGATE →
SYNTHESIZE**. Slice 2 specified EXPAND as the micro-expand's **workshop
depth** — an inline discipline, not a skill (the ai-guru live run did the
whole job inline; a separate skill would step out of the room). Slice 3
shipped ART-VIZ the same way — an inline discipline (all four by-hand/live
runs wrote the style routes inline as prose in `concept.md`; the style skill
and the render path are deferred, see below). The one remaining stage is
named below so the orchestrator can be honest about what hasn't run — a
skipped stage is *declared* skipped in `stage_provenance`, never silently
faked.

## Stage table

| Stage | Skill | Status | What it does | Skip condition |
|---|---|---|---|---|
| micro-expand | inline in orchestrator | **live** | EXPAND's reflex depth (its opening beat): 3 alternate premises / 3 style-tone routes / 3 risk questions, then "deepen or proceed?" | never — always on, even for a rich spark |
| EXPAND | inline in orchestrator / INTERROGATE — **not a skill** | **live (Slice 2)** | per-axis divergence at workshop depth: N≈3–5 mutually distinct options + a synthesized recommendation, inline; converges to one lean Sean accepts/vetoes in a line; never leaves the orchestrator | Sean answers "proceed" at the micro-expand gate AND no axis turns contested mid-grill |
| INTERROGATE | `frontdoor-interrogate` | **live** | the relentless grill → locked specifics | never — even a complete-looking spark gets the North Star check (it usually collapses at "single objective") |
| ART-VIZ | inline in orchestrator — **not a skill** | **live (Slice 3)** | ≥3 distinct Flow-ready route prompts + signature mechanic, inline prose in concept.md; chosen route → prose + seed `anchor_ref`/`style_ref_ids` (no `style_route` field) | piece has a locked register already (e.g. an act inside an existing piece) |
| STRESS-TEST | `frontdoor-stress-test` | Slice 4 | pre-mortem + red-team prose in concept.md; `stress_verdict` → frontdoor.json | never once built (always-on, non-blocking) |
| SYNTHESIZE | `frontdoor-synthesize` | **live** | write concept + brief + seeds; emit via the code seam; §8.1 self-check | never — the session's whole output |

## Routing rules

- **Always micro-expand first.** No thin/rich classification — the binary
  classifier was cut (red-team A4). Divergence is a reflex, not a route.
- **One gate question after micro-expand:** deepen (→ the inline contested-axis
  workshop, EXPAND at workshop depth) or proceed (→ INTERROGATE). Sean's
  call, one line.
- **EXPAND keeps its nominal first position without a reorder.** The
  always-on micro-expand is its opening beat, before INTERROGATE; workshop
  depth is *invoked inline throughout* — at the deepen gate or on any
  contested axis mid-grill. INTERROGATE deepens **in place** (it does not
  raise-and-return); divergence is a move the room makes at a fork, not a
  sibling stage invocation, so the control-returns rule below is not in
  play. Locks stay orchestrator-only, append-only.
- **EXPAND's discipline is the SKILL.md workshop spec** (distinct options,
  named specifics with tradeoffs, converge, protect the intuition, flag
  buildability) — **not a volume metric**. The old "≥8 avenues across ≥4
  domains" count is dead: gameable by semantic neighbours. Quality is judged
  live against `good-expand-rubric.md`, by Sean, never by CI.
- **Promotion trigger (YAGNI-honest):** EXPAND becomes a standalone skill
  only if ≥2 live runs show inline deepening demonstrably underperforming
  (routing confusion, dropped discipline). Until then it stays in the room.
- **ART-VIZ runs inline as Step 2.5** (orchestrator SKILL.md), between
  INTERROGATE and SYNTHESIZE: one fixed hero frame, ≥3 mutually-distinct
  Flow-ready route prompts, the signature mechanic never dropped, the
  timing/craft bible captured as prose, un-buildable registers surfaced as
  `open_questions`. $0 prompt-only — no render, no spend; Sean runs the
  routes on Flow himself and picks. Quality is judged live against
  `good-art-viz-rubric.md`, by Sean, never by CI.
- **ART-VIZ promotion trigger (YAGNI-honest):** promote to a standalone
  `frontdoor-art-viz` skill only if ≥2 live runs show inline route-writing
  demonstrably underperforming (thin routes, dropped signature mechanic,
  routing confusion). Four runs of evidence say inline works.
- **Deferred, on purpose:** the SPEND OK gate + Higgsfield render path is
  specified as deferred design in `good-art-viz-rubric.md` (appendix) — it
  is built only when a greenlit piece + a shipped STRESS-TEST `proceed`
  verdict both exist. The `genndy-tartakovsky` style skill (the AKCodez
  scaffold) is a Cy/generation-layer asset — the first real style skill
  rides the first greenlit piece's Cy authoring run, not the front door.
- **Control always returns to the orchestrator between stages.** A stage that
  wants another stage to run raises an `open_question`; it never invokes a
  sibling directly.
- **Re-entry:** if SYNTHESIZE raises an unresolved-hole `open_question`, the
  orchestrator reopens INTERROGATE scoped to that hole only — not a full
  re-interview.
- **Until Slice 4 lands:** risk-carrying happens via the micro-expand's 3
  risk questions and the concept doc's Open-threads movement — honest
  proto-stress-tests, recorded as such in the sidecar; never presented as a
  STRESS-TEST pass.

## Provenance

`frontdoor.json.stage_provenance` lists the stages that actually ran, in
order (e.g. `["micro-expand", "interrogate", "art-viz", "synthesize"]`). A
stage that was skipped or approximated inline is simply absent. A
workshop-depth deepening records one axis-tagged entry per contested axis,
in the order worked — `expand:<axis-slug>` (e.g. `["micro-expand",
"expand:ending", "interrogate", "expand:stakes", "synthesize"]`). An inline
ART-VIZ pass records a plain `art-viz` entry. The seam carries these with
no schema change (provenance strings are values, not fields — pinned by
`tests/test_frontdoor_handoff.py`). Test fixtures carry `mode: "fixture"` so
a copied bundle can never masquerade as a live session
(`mode: "interactive"`).
