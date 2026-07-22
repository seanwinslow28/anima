---
name: artdept-synthesize
description: The Art Department's SYNTHESIZE stage — write the bundle from the session sidecar and emit through the pipeline.artdept code seam. MODEL-INVOKED by the art-department orchestrator only; not for direct user invocation. Use when the orchestrator reaches the synthesize stage of an Art Department session.
---

# SYNTHESIZE — write the bundle, hand it off

The playground is closed. **Synthesize, don't interview** — every input you need
is already a LOCKED DECISION in `artdept-session.md`. Your job is to turn the
locks into the bundle without asking Sean anything new and without inventing
anything the room did not decide. Every fact in the bundle traces to a `[L*]`
lock or a stage proposal Sean ratified; if you can't source a sentence in the
sidecar, the sentence doesn't ship.

If you find a genuine hole — a North-Star point that never got locked, an anchor
that was never saved, a register that was left hanging — **do not fill it with
an invention and do not ask the human.** Append it as an `open_question` in the
PROPOSALS LOG's `### synthesize` block and return control to the orchestrator. A
hole discovered here means a stage stopped early; reopening it is the
orchestrator's call, not yours.

## What you write

**`design-bible.md` — the human-facing artifact.** Museum-worthy design-intent
prose: personality→visual reasoning per principal, the loaded-object logic, the
look-test forks and **why the winner won**. This is the document Sean rereads in
six months to remember why the look mattered. Pull phrasing from the sidecar
**verbatim where it sings** — the locked decisions were written in the room's
voice; don't launder "primal-sketch-grit, because the gritty ink over color
carried the kid's face across the transformation" into neutral summary.

**`prompt-pack.md` — the reproducible recipe.** The **winning recipes from the
look-tests**, not a fresh derivation. Every `[L5] chosen prompt recipe` lock is
a prompt the room already ratified — carry it as written. Structure it by the
FRESH / EDIT / COMPOSITE economy (`art-department/references/prompt-technique-kit.md`):
FRESH = full description + named style + the web-search-the-show clause +
anti-render negation; EDIT / COMPOSITE = terse, style-silent, reference-carried.
**Never re-derive or "improve" a prompt the room already locked** — the pack is
the record of what won Sean's eye, not a second guess at it.

**`chatgpt-orchestration.md` — the batch runner Sean runs in the Codex / ChatGPT
Desktop app.** That app has the project's filesystem, so the orchestration is
**path-based, not attachment-based**: it names an **output folder** (all
generations save there by their listed filenames), cites every input/prior
output **by file path** (quote paths with spaces), and never says "attach" or
"upload." It carries the dependency map (which prompt feeds which), the
**never-cross-styles** rule (a register's edits reference only that register's
anchors), and **checkpointed batches** (one batch, save, show, wait for
"continue"). The GRANDMASTER orchestration prompt is the exact shape — fresh
foundations → edits → composites, in order. This is the deliverable where Sean's
definitive high-quality generation happens; it must be runnable as written.

**`environment-style.md` — the world's locked look.** The key-location design(s)
and the environment-style note: the flat-daylight staging, the palette the world
reads in, the mood — enough that a background prompt inherits the register
without a bespoke design per backdrop.

**`cast_list.yaml` — the scope line made rows.** The design §6 boundary as data:
- `designed:` — one entry per principal + named/recurring character, each with
  `character_id` (lowercase-kebab), `display_name`, `tier` (`principal` |
  `named`), `style_register` (from the closed vocabulary), and `anchors:` (a
  non-empty list of ratified anchor refs that resolve — bundle-local `refs/…`,
  or `characters/{id}/source-refs/…`).
- `world:` — key locations (`id`, `display_name`, optional `refs`).
- `extras_guidance:` — the anonymous-background prose ("background kids aged
  eight to ten, varied heights, one or two in paper party hats"), **never**
  individually designed rows. This field is required; extras are covered by
  guidance, never by silence.

**`artdept.json`** — `slug`, `characters` (must match the `cast_list` designed
ids), `stage_provenance`, `mode: "interactive"`. A real session is interactive;
only test fixtures say `fixture`. List in `stage_provenance` exactly the stages
that ran — a skipped LOOK-TEST is absent, never faked (the orchestrator declared
the skip).

The seventh bundle file, **`cy_readiness_report.md`, is emitted by the seam** —
you do not hand-write it. It names, per character, the gaps to Cy-ready (anchors
copied into `characters/{id}/source-refs/`, register authored, manifest
registered). Present it to the orchestrator; **never** close a gap by editing
`manifest.yaml` (source-of-truth, human-owned — the front door's gap-report
discipline, one stage later).

## How you emit (only through the seam)

```python
import yaml
from pathlib import Path
from pipeline.artdept.emit import emit_artdept_dir
from pipeline.artdept.handoff import Handoff
from pipeline.artdept.validate import validate_artdept_dir

out = emit_artdept_dir(
    Path("<bundle-dir>"),                 # the dir the orchestrator named
    design_bible_md=design_bible_text,
    prompt_pack_md=prompt_pack_text,
    orchestration_md=orchestration_text,
    environment_style_md=environment_style_text,
    cast=cast,                            # the cast_list dict
    handoff=Handoff(slug="<slug>", characters=[...],
                    stage_provenance=[...], mode="interactive"),
    manifest=yaml.safe_load(Path("manifest.yaml").read_text()),
)
problems = validate_artdept_dir(out)
```

Then **call the CLI seam and paste its output into the room**:

```
python -m pipeline.artdept validate <bundle-dir>
```

`validate_artdept_dir` must return `[]` (and the CLI must exit 0) before you hand
back — the seam checks *structure* (files present, cast-list shape, anchor refs
resolve, handoff↔cast cross-check) and **never judges taste** (taste was Sean's
live eye + `art-department/references/good-look-test-rubric.md`). A **FAIL
returns to the orchestrator** — fix the bundle and re-emit until clean; a failing
bundle is **never silently shipped.** An unauthored register only `WARN`s with
the playbook pointer — it does not fail (the hard register gate is Cy execution).

## The boundary (hard)

You emit files **only via `pipeline.artdept.emit`**, and only into the bundle
dir the orchestrator named. You never lock decisions, never alter the sidecar
beyond appending to your own `### synthesize` proposals block, never rewrite the
meaning of a locked decision — synthesis compresses, it does not reinterpret,
and it never invents. When the CLI prints `ok`, present Sean the emitted dir,
the validation result, and the `cy_readiness_report.md`, then hand back.
