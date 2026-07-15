"""Handoff — the artdept.json machine descriptor (design §8).

Deliberately the same four fields as frontdoor.json: the schema grows only
when a real consumer exists. Registers live per-entry in cast_list.yaml
(the readiness report reads them); there is no top-level register or
budget field because nothing machine-reads either.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from pipeline.frontdoor.handoff import SLUG_RE

MODES = ("interactive", "fixture")


@dataclass
class Handoff:
    slug: str
    characters: list[str]
    stage_provenance: list[str]
    mode: str = "interactive"

    def __post_init__(self) -> None:
        if not (isinstance(self.slug, str) and SLUG_RE.match(self.slug)):
            raise ValueError(f"slug {self.slug!r} is not a clean lowercase-kebab token")
        if not (isinstance(self.characters, list) and self.characters):
            raise ValueError("characters must be a non-empty list of character slugs")
        for c in self.characters:
            if not (isinstance(c, str) and SLUG_RE.match(c)):
                raise ValueError(f"character id {c!r} is not lowercase-kebab")
        if not (isinstance(self.stage_provenance, list) and self.stage_provenance):
            raise ValueError("stage_provenance must be a non-empty list of stage names")
        if self.mode not in MODES:
            raise ValueError(f"mode {self.mode!r} not in {MODES}")

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2) + "\n"

    @classmethod
    def from_json(cls, text: str) -> "Handoff":
        payload = json.loads(text)
        if not isinstance(payload, dict):
            raise ValueError("artdept.json must be a JSON object")
        known = {f for f in cls.__dataclass_fields__}
        unknown = set(payload) - known
        if unknown:
            raise ValueError(f"unknown artdept.json fields: {sorted(unknown)}")
        return cls(**payload)
