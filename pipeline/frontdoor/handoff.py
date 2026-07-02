"""Handoff — the frontdoor.json machine descriptor (§5.3).

Slice-1 minimal: slug (the run's --slug), characters (the gap report's
input), stage_provenance, plus the R1 `mode` marker (a fixture-built brief
in tests can never masquerade as a real interactive run). style_route /
stress_verdict land with Slices 3/4 — the schema grows with real consumers.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass

SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
MODES = ("interactive", "fixture")


@dataclass
class Handoff:
    slug: str
    characters: list[str]
    stage_provenance: list[str]
    mode: str = "interactive"

    def __post_init__(self) -> None:
        if not (isinstance(self.slug, str) and SLUG_RE.match(self.slug)):
            raise ValueError(
                f"slug {self.slug!r} is not a clean lowercase-kebab token"
            )
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
            raise ValueError("frontdoor.json must be a JSON object")
        known = {f for f in cls.__dataclass_fields__}
        unknown = set(payload) - known
        if unknown:
            raise ValueError(f"unknown frontdoor.json fields: {sorted(unknown)}")
        return cls(**payload)
