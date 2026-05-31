# Museum Exhibit Schema (v1.0)

> **Read before touching anything under `pipeline/museum/` or `museum/`.** This
> is the source-of-truth for the durable shape of a Museum exhibit. The schema
> is the load-bearing thing; the scraper, Mo, the renderer, and the live capture
> hook all read and write *this*. Implementation: [`pipeline/museum/schema.py`](../pipeline/museum/schema.py).

## What the Museum is

The Museum is anima's orthogonal **capture layer** (canonical spec:
[`docs/pipeline-architecture-v1.md`](pipeline-architecture-v1.md) §Museum). Not a
phase — it runs in parallel with every phase and turns the production process
into durable, dated, public-ready artifacts. PHILOSOPHY: *"the pipeline is the
portfolio piece… the museum is core, not bolted on"* and *"empirical, not vibes
— the repo carries its receipts."* The Museum is the receipts made visible.

Two delivery decisions are locked (2026-05-31): **backfill everything** (a
read-only retroactive scraper over the real artifacts in `runs/`, noise-filtered)
and **standalone first** (a self-contained static site inside `anima/`; the Astro
export into `sw-ai-pm-portfolio` is an explicit follow-on, not coupled here).

## The unit: an Exhibit

An **exhibit** is the structured record of one decision-bearing moment in the
pipeline — a plate verdict, a Bible mutation, a Seedance shot, an audit gate.
It carries the prompt, references, output, rationale, critic verdict(s), and the
outcome, plus the criteria IDs it cites (reusing the existing `IR.*` / `AC.*`
graph vocabulary verbatim — never reinvented).

## Tree layout

```
museum/
  {project_slug}/                       # e.g. character-bible/ — derive_project_slug()
    project.json                        # machine: slug, title, run + exhibit counts
    project.md                          # human: Mo's project overview (placeholder until Phase 3)
    {run_slug}/                         # e.g. 2026-05-30-cy-claude-mascot-pencil-bake/
      run.json                          # machine: run metadata, source path, filtered list
      run.md                            # human: Mo's run narrative (placeholder until Phase 3)
      exhibits/
        {exhibit_id}/
          exhibit.json                  # machine: the structured Exhibit record (this schema)
          exhibit.md                    # human: clean prose (Mo narrates in Phase 3)
          assets/                        # images copied READ-ONLY out of runs/ + characters/
  _site/                                # Phase 5 self-contained static render target
```

`museum/` **is committed** — it is the durable, portable artifact. `runs/` stays
gitignored; the scraper is the only thing that lifts run evidence into a
committable form (under `museum/`).

## `project_slug` derivation

Config-driven, in `manifest.yaml` → `museum.project_slugs` (first match wins; an
unmatched run goes to `_unclassified`, never silently misfiled). Two projects
exist today:

- **`character-bible`** — every Cy bake, the register pivot, two-character
  first-light, emitter validation. *The agent built and hardened in the open.*
- **`pencil-test`** — Act 1 + Act 2 Seedance + head-turn / pose runs. *The
  shipped animation.*

## Field reference — `Exhibit`

| Field | Type | Meaning |
|-------|------|---------|
| `exhibit_id` | str | Unique within a run (e.g. `03-expr-neutral`, `audit-01-bible_mutation`). |
| `project_slug` | str | The owning project (see derivation above). |
| `run_slug` | str | The source run directory name. |
| `title` | str | Human title (e.g. `Plate — expressions/neutral.png`). |
| `kind` | enum | `plate_verdict` \| `bible_mutation` \| `bible_add` \| `seedance_shot` \| `audit_gate` \| `frame_keyframe` \| `note`. |
| `decision` | Decision | The outcome + rationale (below). |
| `phase` | int? | Pipeline phase number (0–9), or null. |
| `persona` | str? | Who decided: `cy` \| `em` \| `maya` \| `mo` \| `human` \| null. |
| `date` | str? | `YYYY-MM-DD`, derived from the run slug, or null. |
| `prompt` | str? | Prompt text **if recoverable on disk**, else null. |
| `references` | list[str] | Reference image paths (relative to the exhibit's `assets/`). |
| `output` | str? | The produced artifact (relative to `assets/`), if recoverable. |
| `comparison_gif` | str? | Set by Phase 4 where a manual shape-block left exists; else null. |
| `verdict` | Verdict? | Critic / gate read (below), when present on disk. |
| `cites_criteria` | list[str] | `IR.*` / `AC.*` IDs **verbatim** from the logs. |
| `evidence_completeness` | enum | `rich` \| `partial` \| `thin` — the honesty signal. |
| `source_paths` | list[str] | Exact on-disk provenance (e.g. `runs/…/plate_verdicts.jsonl#L6`). |
| `schema_version` | str | `"1.0"`. |

### `Decision`

| Field | Type | Meaning |
|-------|------|---------|
| `outcome` | str | `pass`\|`fail`\|`borderline`\|`retry`\|`approved`\|`rejected`\|`ingested`\|`human_gate_required`\|`added`\|`mutated`. |
| `attempts` | int? | Attempt count, when recorded. |
| `rationale` | str | **NEVER invented.** Empty string when the logs are silent. |
| `rationale_source` | str? | Provenance file for the rationale; `null` when none exists on disk. |

### `Verdict`

| Field | Type | Meaning |
|-------|------|---------|
| `method` | str? | `dinov2` \| `clip` \| `pil-perceptual` \| `gemini`. |
| `score` | float? | Similarity score vs the reference. |
| `reference` | str? | The reference the score was measured against (e.g. `anchor.png`). |
| `model_verdict` | str? | The prose model's verdict (e.g. Gemini `pass`/`fail`/`borderline`). |
| `model_confidence` | float? | The prose model's confidence. |

## The honesty contract (load-bearing)

The Museum's whole value is that it is real and dated. Two rules are encoded in
the schema itself, not left to discipline:

1. **A thin exhibit is honest; an invented one is the template trap.** Where the
   logs carry no rationale, `decision.rationale` stays `""` and
   `rationale_source` stays `null`. `to_markdown()` then renders an explicit
   *"No rationale recorded in this run's logs… an honest gap is preferable to
   invented narrative."* Mo (Phase 3) is forbidden by her preamble from
   manufacturing rationale an exhibit doesn't carry.
2. **`evidence_completeness` is the sortable honesty signal.** `rich` = the run
   left full reasoning; `partial` = structured verdict but no prose; `thin` =
   sparse, surfaced as such.

## Export-friendly (not export-coupled)

Field names are chosen to map cleanly onto the future Astro MDX frontmatter in
`sw-ai-pm-portfolio` (`exhibit_id`, `title`, `kind`, `date`, `cites_criteria`,
etc.). That mapping is a **named follow-on session** — this schema does not read
or depend on the portfolio's content-collection schema. Standalone first.

## Worked example

```json
{
  "exhibit_id": "03-expr-neutral",
  "project_slug": "character-bible",
  "run_slug": "2026-05-30-cy-claude-mascot-pencil-bake",
  "title": "Expression plate — neutral",
  "kind": "plate_verdict",
  "decision": {
    "outcome": "fail",
    "attempts": 3,
    "rationale": "NB2 invented a hair tuft; no-hair invariant violated.",
    "rationale_source": "plate_verdicts.jsonl"
  },
  "phase": 2,
  "persona": "cy",
  "date": "2026-05-30",
  "prompt": null,
  "references": ["assets/anchor.png"],
  "output": "assets/neutral.png",
  "comparison_gif": null,
  "verdict": {
    "method": "dinov2",
    "score": 0.8857,
    "reference": "anchor.png",
    "model_verdict": "fail",
    "model_confidence": 0.7
  },
  "cites_criteria": ["IR.claude-mascot.anatomy.no-hair"],
  "evidence_completeness": "rich",
  "source_paths": ["runs/2026-05-30-cy-claude-mascot-pencil-bake/plate_verdicts.jsonl#L6"],
  "schema_version": "1.0"
}
```
