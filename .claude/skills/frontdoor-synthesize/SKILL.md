---
name: frontdoor-synthesize
description: The front door's SYNTHESIZE stage — write the concept doc + Studio Brief + character seeds from the session sidecar and emit the brief bundle through the pipeline.frontdoor code seam. MODEL-INVOKED by the brainstorm-front-door orchestrator only; not for direct user invocation. Use when the orchestrator reaches the synthesis stage of a brainstorm session.
---

# SYNTHESIZE — write it down, hand it off

The interview is over. **Synthesize, don't interview** — every input you need
is in `frontdoor-session.md`'s locked decisions; your job is to turn them into
the bundle without asking Sean anything new. If you find a genuine hole (a
North-Star point that never got locked), do not fill it with an invention and
do not ask the human — append it as an `open_question` in the proposals log
and return control to the orchestrator. A hole discovered here means
INTERROGATE stopped early; that's the orchestrator's call to reopen.

## What you write

**`concept.md` — the human-facing artifact.** Museum-worthy prose in the
session's own language, shaped by
`brainstorm-front-door/references/concept-doc-template.md`. This is the
document Sean rereads in six months to remember why the piece mattered. Pull
phrasing from the sidecar verbatim where it sings — the locked decisions were
written in the room's voice; don't launder them into neutral summary.

When the sidecar carries an `### art-viz` block, **fold its proposals into
the concept doc's Style-routes, timing-bible, and money-shot movements** —
the routes are prose you *emit*, not invent; they were authored in the room
and your job is to place them. If Sean picked a route, carry the chosen-route
lock as prose (e.g. "Chosen route: C — hybrid"). Never re-derive or
"improve" a route the room already wrote.

When the sidecar carries a `### stress-test` block, **fold its proposals into
the concept doc's Stress-test movement** — the Tiger / Paper-Tiger / Elephant
triage with the Launch-Blocking Tigers named, each risk as its "Fails if ___"
with the cheapest test — and carry the verdict lock as prose (e.g. "Stress
verdict: proceed — residuals: the register-gap Tiger"). **Populate the
Open-threads movement from the non-launch-blocking residuals** (Fast-Follow /
Track) — Open threads is the stress test's downstream tail. Never soften a
Tiger into an observation, and never re-run the red-team here — you place
findings, you don't re-litigate them.

**`00_studio_brief.md` — the machine-facing distillation.** The 8-section
shape in `brainstorm-front-door/references/studio-brief-contract.md`, exact
headers, in order, with the `### What this is NOT` block under tone. Maya,
Sam, and Bea consume this as free text: every sentence should be a directive
or a constraint, nothing decorative. The non-negotiables section is the
piece's contract — checkable phrasing only.

**A production-binding stress residual reaches this file — this is the
load-bearing fold.** A Launch-Blocking Tiger, or a proceed-with-residual that
changes buildability / budget / constraints, lands under `### What this is
NOT` or the non-negotiables as one more checkable directive (see
`brainstorm-front-door/references/studio-brief-contract.md` §Where stress
residuals land). Maya reads only this brief — a Tiger left in `concept.md`
alone is invisible to planning. Non-binding (Fast-Follow / Track) findings
stay in `concept.md`.

**`character_seeds.yaml` — the hand to Cy.** One entry per character:
`character_id` (lowercase-kebab), `display_name`, `story_role`,
`style_register`, `source_notes` (multi-line: the design-bearing specifics Cy
seeds `source-refs/notes.md` from), `anchor_ref`, `style_ref_ids`,
`cy_target_dir`. Seeds, not Bibles — write what a designer needs to start,
not what the Bible will conclude. **Populate `anchor_ref` /
`style_ref_ids` only when actual refs exist** (e.g. Sean rendered the chosen
route on Flow and the file is on disk); otherwise keep `anchor_ref: null` /
`style_ref_ids: []`. Never invent a ref path for a route that was only
prose.

**`frontdoor.json`** — slug, characters, stage_provenance, `mode:
"interactive"` (a real session is interactive; only test fixtures say
`fixture`). Include `art-viz` in `stage_provenance` when the sidecar carries
an `### art-viz` block, and `stress-test` when it carries a `### stress-test`
block; leave either absent when the stage was skipped — the provenance list
records what actually ran.

## How you emit (only through the seam)

```python
import yaml
from pathlib import Path
from pipeline.frontdoor.emit import emit_brief_dir
from pipeline.frontdoor.handoff import Handoff
from pipeline.frontdoor.validate import validate_brief_dir

out = emit_brief_dir(
    Path("briefs/<date>-<slug>/"),
    studio_brief_md=studio_brief_text,
    concept_md=concept_text,
    seeds=seeds,                       # the list of seed dicts
    handoff=Handoff(slug="<slug>", characters=[...],
                    stage_provenance=[...], mode="interactive"),
    manifest=yaml.safe_load(Path("manifest.yaml").read_text()),
)
problems = validate_brief_dir(out)
```

`validate_brief_dir` must return `[]` before you hand back — fix and re-emit
until it does. The emitted `manifest_gap_report.md` names every character not
yet registered and the Cy work remaining; present it, never "fix" it by
editing `manifest.yaml` (source-of-truth file, human-owned).

## Before handing back

Self-check the emitted brief against the anti-pattern rubric in
`brainstorm-front-door/references/pinata-worked-example.md` (§Companion
checklist) — generic grief, stereotype characters, the-protagonist-is-the-joke,
a missing signature mechanic, an absent timing bible, a concept too broad to
plan. Report every hit honestly to the orchestrator; the rubric exists
because a structurally valid brief can still be a flat one.

## The boundary (hard)

You emit files **only via `pipeline.frontdoor.emit`**, and only into the brief
dir the orchestrator named. You never lock decisions, never alter the sidecar
beyond appending proposals, never rewrite the meaning of a locked decision —
synthesis compresses, it does not reinterpret.
