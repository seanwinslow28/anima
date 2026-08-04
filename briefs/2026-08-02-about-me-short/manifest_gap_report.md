# Manifest gap report — about-me-short

The front door emits character *seeds*, not Bibles. This brief is
Maya-ready now; a NEW character is not GENERATE-ready until Cy authors
its Bible and it is registered in the manifest `characters:` block.
The front door never mutates manifest.yaml (a source-of-truth file).

## Unregistered characters (4)

- **codex-cloud** (Codex) — not in manifest `characters:`. Next Cy action:
  1. populate `characters/codex-cloud/source-refs/` from the seed's `source_notes` (Cy refuses to author from an empty source-refs/),
  2. `python scripts/author_bible.py characters/codex-cloud/ --studio-brief "<from the seed>" --run-dir runs/<id>/`,
  3. register `codex-cloud:` under manifest `characters:` and its acceptance_criteria.json under `criteria_sources:`.
- **gemini-star** (Gemini) — not in manifest `characters:`. Next Cy action:
  1. populate `characters/gemini-star/source-refs/` from the seed's `source_notes` (Cy refuses to author from an empty source-refs/),
  2. `python scripts/author_bible.py characters/gemini-star/ --studio-brief "<from the seed>" --run-dir runs/<id>/`,
  3. register `gemini-star:` under manifest `characters:` and its acceptance_criteria.json under `criteria_sources:`.
- **grok-gremlin** (Grok) — not in manifest `characters:`. Next Cy action:
  1. populate `characters/grok-gremlin/source-refs/` from the seed's `source_notes` (Cy refuses to author from an empty source-refs/),
  2. `python scripts/author_bible.py characters/grok-gremlin/ --studio-brief "<from the seed>" --run-dir runs/<id>/`,
  3. register `grok-gremlin:` under manifest `characters:` and its acceptance_criteria.json under `criteria_sources:`.
- **user** (The USER) — not in manifest `characters:`. Next Cy action:
  1. populate `characters/user/source-refs/` from the seed's `source_notes` (Cy refuses to author from an empty source-refs/),
  2. `python scripts/author_bible.py characters/user/ --studio-brief "<from the seed>" --run-dir runs/<id>/`,
  3. register `user:` under manifest `characters:` and its acceptance_criteria.json under `criteria_sources:`.

## Registered characters (2)

- sean-anchor (Sean) — registered.
- claude-mascot (Claude) — registered.
