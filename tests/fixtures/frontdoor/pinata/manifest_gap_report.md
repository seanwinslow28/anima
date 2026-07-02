# Manifest gap report — grandmaster

The front door emits character *seeds*, not Bibles. This brief is
Maya-ready now; a NEW character is not GENERATE-ready until Cy authors
its Bible and it is registered in the manifest `characters:` block.
The front door never mutates manifest.yaml (a source-of-truth file).

## Unregistered characters (3)

- **kid** (The Kid) — not in manifest `characters:`. Next Cy action:
  1. populate `characters/kid/source-refs/` from the seed's `source_notes` (Cy refuses to author from an empty source-refs/),
  2. `python scripts/author_bible.py characters/kid/ --studio-brief "<from the seed>" --run-dir runs/<id>/`,
  3. register `kid:` under manifest `characters:` and its acceptance_criteria.json under `criteria_sources:`.
- **grandma** (The Late Grandmother) — not in manifest `characters:`. Next Cy action:
  1. populate `characters/grandma/source-refs/` from the seed's `source_notes` (Cy refuses to author from an empty source-refs/),
  2. `python scripts/author_bible.py characters/grandma/ --studio-brief "<from the seed>" --run-dir runs/<id>/`,
  3. register `grandma:` under manifest `characters:` and its acceptance_criteria.json under `criteria_sources:`.
- **host-dad** (The Host Dad) — not in manifest `characters:`. Next Cy action:
  1. populate `characters/host-dad/source-refs/` from the seed's `source_notes` (Cy refuses to author from an empty source-refs/),
  2. `python scripts/author_bible.py characters/host-dad/ --studio-brief "<from the seed>" --run-dir runs/<id>/`,
  3. register `host-dad:` under manifest `characters:` and its acceptance_criteria.json under `criteria_sources:`.

## Registered characters (0)

- none.
