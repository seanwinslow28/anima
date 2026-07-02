"""validate_brief_dir — the structural gate on a front-door brief dir (§8 step 5).

Checks the Studio Brief sections, the concept doc (non-empty + a logline —
its *quality* is the §8.1 eval, not an assert), the frontdoor.json handoff,
and the character-seed shape inline (seeds.py cut per red-team A6). Returns
a list of problems; empty means the dir is ready for `pipeline.run --brief`.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from pipeline.frontdoor.brief import parse
from pipeline.frontdoor.handoff import SLUG_RE, Handoff

REQUIRED_SEED_FIELDS = (
    "character_id",
    "display_name",
    "story_role",
    "style_register",
    "source_notes",
)


def validate_brief_dir(brief_dir: Path) -> list[str]:
    brief_dir = Path(brief_dir)
    problems: list[str] = []

    brief_path = brief_dir / "00_studio_brief.md"
    if brief_path.exists():
        problems += parse(brief_path.read_text(encoding="utf-8")).validate()
    else:
        problems.append("missing file: 00_studio_brief.md")

    concept_path = brief_dir / "concept.md"
    if concept_path.exists():
        concept = concept_path.read_text(encoding="utf-8")
        if not concept.strip():
            problems.append("concept.md is empty")
        elif "logline" not in concept.lower():
            problems.append("concept.md carries no logline")
    else:
        problems.append("missing file: concept.md")

    handoff: Handoff | None = None
    handoff_path = brief_dir / "frontdoor.json"
    if handoff_path.exists():
        try:
            handoff = Handoff.from_json(handoff_path.read_text(encoding="utf-8"))
        except (ValueError, KeyError, TypeError) as e:
            problems.append(f"frontdoor.json invalid: {e}")
    else:
        problems.append("missing file: frontdoor.json")

    seeds_path = brief_dir / "character_seeds.yaml"
    seed_ids: list[str] = []
    if seeds_path.exists():
        seeds = yaml.safe_load(seeds_path.read_text(encoding="utf-8"))
        if not isinstance(seeds, list):
            problems.append("character_seeds.yaml must be a list of seeds")
        else:
            for i, seed in enumerate(seeds):
                if not isinstance(seed, dict):
                    problems.append(f"seed #{i} is not a mapping")
                    continue
                for fld in REQUIRED_SEED_FIELDS:
                    if not seed.get(fld):
                        problems.append(
                            f"seed #{i} ({seed.get('character_id', '?')}): missing required field {fld}"
                        )
                cid = seed.get("character_id")
                if isinstance(cid, str):
                    seed_ids.append(cid)
                    if not SLUG_RE.match(cid):
                        problems.append(f"seed character_id {cid!r} is not lowercase-kebab")
    else:
        problems.append("missing file: character_seeds.yaml")

    if handoff is not None and seeds_path.exists() and sorted(handoff.characters) != sorted(seed_ids):
        problems.append(
            f"frontdoor.json characters {sorted(handoff.characters)} do not match "
            f"character_seeds.yaml ids {sorted(seed_ids)}"
        )

    return problems
