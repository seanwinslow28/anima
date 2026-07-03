# Manifest gap report — ai-guru-pilot

The front door emits character *seeds*, not Bibles. This brief is
Maya-ready now; a NEW character is not GENERATE-ready until Cy authors
its Bible and it is registered in the manifest `characters:` block.
The front door never mutates manifest.yaml (a source-of-truth file).

## Unregistered characters (2)

- **aiden** (Aiden) — not in manifest `characters:`. Next Cy action:
  1. populate `characters/aiden/source-refs/` from the seed's `source_notes` (Cy refuses to author from an empty source-refs/),
  2. `python scripts/author_bible.py characters/aiden/ --studio-brief "<from the seed>" --run-dir runs/<id>/`,
  3. register `aiden:` under manifest `characters:` and its acceptance_criteria.json under `criteria_sources:`.
- **orby** (Orby) — not in manifest `characters:`. Next Cy action:
  1. populate `characters/orby/source-refs/` from the seed's `source_notes` (Cy refuses to author from an empty source-refs/),
  2. `python scripts/author_bible.py characters/orby/ --studio-brief "<from the seed>" --run-dir runs/<id>/`,
  3. register `orby:` under manifest `characters:` and its acceptance_criteria.json under `criteria_sources:`.

## Registered characters (0)

- none.
