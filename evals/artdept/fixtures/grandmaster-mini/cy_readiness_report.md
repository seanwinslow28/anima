# Cy readiness report — grandmaster

The Art Department emits ratified anchors + a locked register per
designed character. A character is Cy-READY when its anchors are in
`characters/{id}/source-refs/`, its register is in the closed vocabulary,
and it is registered in the manifest `characters:` block. This report
names each remaining gap; the Art Department never mutates manifest.yaml.

- **kid** (The Kid) — NOT Cy-ready:
  1. anchors are bundle-local — copy the ratified anchors into `characters/kid/source-refs/` (Cy refuses to author from an empty source-refs/),
  2. not in manifest `characters:` — after the Bible pass, register `kid:` and its acceptance_criteria.json under `criteria_sources:`,
  then: `python scripts/author_bible.py characters/kid/ --studio-brief "<from design-bible.md>" --run-dir runs/<id>/`
- **grandma** (Grandma) — NOT Cy-ready:
  1. anchors are bundle-local — copy the ratified anchors into `characters/grandma/source-refs/` (Cy refuses to author from an empty source-refs/),
  2. not in manifest `characters:` — after the Bible pass, register `grandma:` and its acceptance_criteria.json under `criteria_sources:`,
  then: `python scripts/author_bible.py characters/grandma/ --studio-brief "<from design-bible.md>" --run-dir runs/<id>/`
