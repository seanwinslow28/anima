# Chain map — stage order, routing, skip conditions

The front door's canonical stage order (Sean's lock; do not reorder):

```
EXPAND → INTERROGATE → ART-VIZ → STRESS-TEST → SYNTHESIZE
```

Slice 1 shipped the walking skeleton: **micro-expand (inline) → INTERROGATE →
SYNTHESIZE**. Slice 2 specified EXPAND as the micro-expand's **workshop
depth** — an inline discipline, not a skill (the ai-guru live run did the
whole job inline; a separate skill would step out of the room). The remaining
stages are named below so the orchestrator can be honest about what hasn't
run — a skipped stage is *declared* skipped in `stage_provenance`, never
silently faked.

## Stage table

| Stage | Skill | Status | What it does | Skip condition |
|---|---|---|---|---|
| micro-expand | inline in orchestrator | **live** | EXPAND's reflex depth (its opening beat): 3 alternate premises / 3 style-tone routes / 3 risk questions, then "deepen or proceed?" | never — always on, even for a rich spark |
| EXPAND | inline in orchestrator / INTERROGATE — **not a skill** | **live (Slice 2)** | per-axis divergence at workshop depth: N≈3–5 mutually distinct options + a synthesized recommendation, inline; converges to one lean Sean accepts/vetoes in a line; never leaves the orchestrator | Sean answers "proceed" at the micro-expand gate AND no axis turns contested mid-grill |
| INTERROGATE | `frontdoor-interrogate` | **live** | the relentless grill → locked specifics | never — even a complete-looking spark gets the North Star check (it usually collapses at "single objective") |
| ART-VIZ | `frontdoor-art-viz` | Slice 3 | ≥3 Flow-ready style-route prompts in concept.md; chosen `style_route` id → frontdoor.json | piece has a locked register already (e.g. an act inside an existing piece) |
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
- **Control always returns to the orchestrator between stages.** A stage that
  wants another stage to run raises an `open_question`; it never invokes a
  sibling directly.
- **Re-entry:** if SYNTHESIZE raises an unresolved-hole `open_question`, the
  orchestrator reopens INTERROGATE scoped to that hole only — not a full
  re-interview.
- **Until Slice 3/4 land:** style-route exploration happens as prose inside
  INTERROGATE's reference questions (borrow the dry-run's A/B/C pattern), and
  risk-carrying happens via the micro-expand's 3 risk questions. Honest
  approximations, recorded as such in the sidecar.

## Provenance

`frontdoor.json.stage_provenance` lists the stages that actually ran, in
order (e.g. `["micro-expand", "interrogate", "synthesize"]`). A stage that
was skipped or approximated inline is simply absent. A workshop-depth
deepening records one axis-tagged entry per contested axis, in the order
worked — `expand:<axis-slug>` (e.g. `["micro-expand", "expand:ending",
"interrogate", "expand:stakes", "synthesize"]`). The seam carries these with
no schema change (provenance strings are values, not fields — pinned by
`tests/test_frontdoor_handoff.py`). Test fixtures carry `mode: "fixture"` so
a copied bundle can never masquerade as a live session
(`mode: "interactive"`).
