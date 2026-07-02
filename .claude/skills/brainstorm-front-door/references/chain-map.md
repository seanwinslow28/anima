# Chain map — stage order, routing, skip conditions

The front door's canonical stage order (Sean's lock; do not reorder):

```
EXPAND → INTERROGATE → ART-VIZ → STRESS-TEST → SYNTHESIZE
```

Slice 1 ships the walking skeleton: **micro-expand (inline) → INTERROGATE →
SYNTHESIZE**. The other stages are named below so the orchestrator can be
honest about what hasn't run — a skipped stage is *declared* skipped in
`stage_provenance`, never silently faked.

## Stage table

| Stage | Skill | Status | What it does | Skip condition |
|---|---|---|---|---|
| micro-expand | inline in orchestrator | **live** | 3 alternate premises / 3 style-tone routes / 3 risk questions, then "deepen or proceed?" | never — always on, even for a rich spark |
| EXPAND | `frontdoor-expand` | Slice 2 | full fan-out (≥8 avenues, domain rotation) on "deepen" | Sean answers "proceed" at the micro-expand gate |
| INTERROGATE | `frontdoor-interrogate` | **live** | the relentless grill → locked specifics | never — even a complete-looking spark gets the North Star check (it usually collapses at "single objective") |
| ART-VIZ | `frontdoor-art-viz` | Slice 3 | ≥3 Flow-ready style-route prompts in concept.md; chosen `style_route` id → frontdoor.json | piece has a locked register already (e.g. an act inside an existing piece) |
| STRESS-TEST | `frontdoor-stress-test` | Slice 4 | pre-mortem + red-team prose in concept.md; `stress_verdict` → frontdoor.json | never once built (always-on, non-blocking) |
| SYNTHESIZE | `frontdoor-synthesize` | **live** | write concept + brief + seeds; emit via the code seam; §8.1 self-check | never — the session's whole output |

## Routing rules

- **Always micro-expand first.** No thin/rich classification — the binary
  classifier was cut (red-team A4). Divergence is a reflex, not a route.
- **One gate question after micro-expand:** deepen (→ EXPAND when built) or
  proceed (→ INTERROGATE). Sean's call, one line.
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
was skipped or approximated inline is simply absent. Test fixtures carry
`mode: "fixture"` so a copied bundle can never masquerade as a live session
(`mode: "interactive"`).
