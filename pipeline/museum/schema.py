"""The durable exhibit data model — the spine the whole Museum reads and writes.

An *exhibit* is the structured record of one decision-bearing moment in the
pipeline: a plate verdict, a Bible mutation, a Seedance shot, an audit gate.
It carries the prompt / references / output / rationale / critic verdict(s) /
outcome and the criteria IDs it cites — reusing the existing IR.*/AC.* graph
vocabulary verbatim rather than reinventing one.

Two honesty contracts are encoded structurally here, because the Museum's whole
value is that it is real and dated (PHILOSOPHY: empirical, not vibes):

  - `Decision.rationale` is NEVER invented. When the logs are silent it stays
    an empty string and `rationale_source` is None. A thin exhibit is truthful;
    an invented one is the template trap.
  - `evidence_completeness` (rich | partial | thin) is the honesty signal a
    renderer or a reader can sort on.

Field names are chosen to map cleanly onto the future Astro MDX frontmatter
(the sw-ai-pm-portfolio export follow-on) without coupling to it now.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Literal

SCHEMA_VERSION = "1.0"

ExhibitKind = Literal[
    "plate_verdict", "bible_mutation", "bible_add",
    "seedance_shot", "audit_gate", "frame_keyframe", "motion_keys", "note",
]
Completeness = Literal["rich", "partial", "thin"]


@dataclass
class Verdict:
    """A critic / gate read on the output, when one exists on disk."""
    method: str | None = None            # dinov2 | clip | pil-perceptual | gemini
    score: float | None = None
    reference: str | None = None
    model_verdict: str | None = None
    model_confidence: float | None = None


@dataclass
class Decision:
    """The outcome of the decision-bearing moment + its rationale provenance."""
    outcome: str                         # pass|fail|borderline|retry|approved|rejected|ingested|human_gate_required|added|mutated
    attempts: int | None = None
    rationale: str = ""                  # NEVER invented; empty string when the logs are silent
    rationale_source: str | None = None  # provenance file; None when no rationale exists on disk


@dataclass
class Exhibit:
    exhibit_id: str
    project_slug: str
    run_slug: str
    title: str
    kind: ExhibitKind
    decision: Decision
    phase: int | None = None
    persona: str | None = None           # cy | em | maya | mo | human | None
    date: str | None = None
    prompt: str | None = None
    references: list[str] = field(default_factory=list)
    output: str | None = None
    frames: list[str] = field(default_factory=list)   # ordered sequence for motion / shot exhibits
    comparison_gif: str | None = None
    verdict: Verdict | None = None
    cites_criteria: list[str] = field(default_factory=list)   # reuse IR.*/AC.* IDs verbatim
    evidence_completeness: Completeness = "thin"
    source_paths: list[str] = field(default_factory=list)
    schema_version: str = SCHEMA_VERSION

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_markdown(self) -> str:
        """Clean studio-manual prose on disk. Boxes / chrome live in the renderer."""
        lines = [f"# {self.title}", ""]
        meta = [f"- kind: {self.kind}", f"- outcome: {self.decision.outcome}"]
        if self.persona:
            meta.append(f"- decided by: {self.persona}")
        if self.date:
            meta.append(f"- date: {self.date}")
        if self.verdict and self.verdict.score is not None:
            meta.append(f"- {self.verdict.method} similarity: {self.verdict.score}")
        meta.append(f"- evidence: {self.evidence_completeness}")
        lines += meta + [""]
        if self.decision.rationale.strip():
            lines += ["## Rationale", "",
                      self.decision.rationale.strip(),
                      "", f"_(source: {self.decision.rationale_source})_", ""]
        else:
            lines += ["## Rationale", "",
                      "No rationale recorded in this run's logs. "
                      "This exhibit is intentionally thin — the evidence is sparse, "
                      "and an honest gap is preferable to invented narrative.", ""]
        if self.cites_criteria:
            lines += ["## Cites criteria", ""] + [f"- `{c}`" for c in self.cites_criteria] + [""]
        if self.source_paths:
            lines += ["## Provenance", ""] + [f"- `{p}`" for p in self.source_paths] + [""]
        return "\n".join(lines)


def _verdict_from_dict(d: dict | None) -> Verdict | None:
    return Verdict(**d) if d else None


def exhibit_from_dict(d: dict) -> Exhibit:
    d = dict(d)
    d["decision"] = Decision(**d["decision"])
    d["verdict"] = _verdict_from_dict(d.get("verdict"))
    return Exhibit(**d)


def exhibit_dir(museum_root: Path, ex: Exhibit) -> Path:
    return (Path(museum_root) / ex.project_slug / ex.run_slug
            / "exhibits" / ex.exhibit_id)


def write_exhibit(museum_root: Path, ex: Exhibit) -> Path:
    d = exhibit_dir(museum_root, ex)
    d.mkdir(parents=True, exist_ok=True)
    (d / "exhibit.json").write_text(
        json.dumps(ex.to_json_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    (d / "exhibit.md").write_text(ex.to_markdown(), encoding="utf-8")
    return d


def read_exhibit(json_path: Path) -> Exhibit:
    return exhibit_from_dict(json.loads(Path(json_path).read_text(encoding="utf-8")))


def derive_project_slug(run_name: str, slug_rules: dict[str, list[str]]) -> str | None:
    """Config-driven classifier. Returns None (→ _unclassified) when no rule
    matches — never silently misfiles a run."""
    name = run_name.lower()
    for slug, needles in slug_rules.items():
        if any(n.lower() in name for n in needles):
            return slug
    return None
