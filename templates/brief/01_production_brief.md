---
piece_id: "{slug}"                  # kebab-case, e.g. "pencil-test-act2"
project_type: animation_piece       # animation_piece | bible_authoring.
                                    # animation_piece (default): Maya plans
                                    # all enabled phases. bible_authoring:
                                    # Maya scopes the plan to Phase 0 + Phase
                                    # 2 only — Cy authors a Character Bible
                                    # as the deliverable; Phases 3-9 are out
                                    # of scope for the run.
phases_enabled: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]   # which phases run this piece
characters_loaded:
  - sean-anchor                     # references characters/{id}/ folders
target_medium: gif                  # gif | webm | mp4 | museum-walkthrough
target_runtime_s: 60
deadline:
  hard: 2026-MM-DD
  soft: 2026-MM-DD
routing_tier_defaults:
  generate: draft                   # draft | pro
  motion: draft
  assemble: draft
retry_budget_per_frame: 4
---

# Production Brief

*This is the brief that says how we'll make it. Maya drafts it from the Studio Brief and the manifest; Sean reads it, edits where the routing or the schedule needs adjusting, and approves before any model burns compute. The orchestrator reads it when scheduling. Annie reads it during continuity passes. After approval, the criteria file locks alongside it.*

The frontmatter above is the structured contract — the fields the runner consumes. Everything below is free-form production notes — the things a line producer would write in the margins of a shooting schedule.

---

## Production notes

*Anything about how to make this piece that isn't already constrained by `manifest.yaml`. Examples of what belongs here:*

- *"This is Act 2 of the Pencil Test. Sean has already authored the animatic in Procreate Dreams; Phase 4 ingests `runs/act2-exploration/animatic.mp4` directly rather than running its own draft."*
- *"First multi-character piece — two characters get loaded per shot. Check `characters/{id}/character.yaml` for proportion rules; flag if any beat asks for a side-by-side that violates them."*
- *"The hero loop is the last 5 seconds; everything before is setup. Concentrate the pro-tier budget at the end."*

*Bullet list or prose, whichever reads cleaner.*

---

## Per-phase routing overrides

*Defaults come from `manifest.yaml`'s `tiering:` block. Override only when this piece needs something different. Examples:*

- *"Phase 5 keyframes: pro tier throughout (this is a portfolio hero piece, not a draft run)."*
- *"Phase 6 motion: Fast tier for the first 9 clips, Pro tier for clip 10 only (the closing beat)."*

*Leave this section as `(no overrides — defaults apply)` if the manifest's defaults are right.*

---

## Risks Maya flagged

*Maya populates this section, not Sean. Hidden costs, schedule risks, brief ambiguities Maya noticed while drafting. Each risk is one bullet: what the risk is, what would trigger it, what mitigation Maya proposes.*

*Example:*

- *Risk: the Studio Brief's tone section calls the piece both "warm" and "melancholy." These can coexist but the criterion `AC.tone.warm-and-melancholy` is interpretive — Em will return borderline on most frames. Mitigation: tighten the tone language to one of the two before locking criteria, or accept that 30%+ of frames will route to Opus escalation.*

*Empty section is fine. Maya leaves it blank when the brief is unambiguous.*
