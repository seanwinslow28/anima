"""Mo — the Museum writer. Phase: Museum (orthogonal capture layer).

Mo is a competent docent, not a poet: she writes fluent expository prose on top
of an already-structured exhibit, in the studio-manual voice, and never invents a
fact the exhibit does not carry. Sonnet 4.6 live (via sdk_runners); a deterministic,
faithful local fallback runs credential-free so the museum builds in CI and Mo
never fabricates from a stubbed model.

The schema is the load-bearing thing; Mo is the prose layer over it.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import ClassVar

from pipeline.agents import (
    AgentContext, AgentResult, CostEstimate, register_node,
)
from pipeline.agents.sdk_runners import invoke_museum_prose
from pipeline.museum.schema import Exhibit, exhibit_from_dict, exhibit_dir

_PROMPTS = Path(__file__).parent / "prompts"
_ANIMA_PREAMBLE = _PROMPTS / "anima-standing-context.md"
_MO_ADDENDUM = _PROMPTS / "mo-museum-writer-context.md"

_PERSONA_NAME = {
    "cy": "Cy", "em": "Em", "maya": "Maya", "mo": "Mo", "human": "Sean",
}


def _who(persona: str | None) -> str:
    return _PERSONA_NAME.get(persona or "", "The pipeline")


def build_prompt(ex: Exhibit, sources: str = "") -> str:
    sections: list[str] = []
    if _ANIMA_PREAMBLE.exists():
        sections.append(_ANIMA_PREAMBLE.read_text(encoding="utf-8"))
    if _MO_ADDENDUM.exists():
        sections.append(_MO_ADDENDUM.read_text(encoding="utf-8"))
    import json
    sections.append("## The exhibit to narrate (structured — do not invent beyond it)\n\n"
                    + "```json\n" + json.dumps(ex.to_json_dict(), indent=2, ensure_ascii=False)
                    + "\n```")
    if sources.strip():
        sections.append("## Source context (field report / CHANGELOG excerpts)\n\n" + sources.strip())
    sections.append("Write Mo's 2–4 paragraph Markdown narration of this exhibit now. "
                    "Prose only — no heading, no front-matter.")
    return "\n\n".join(sections)


def _fallback_prose(ex: Exhibit) -> str:
    """Deterministic, strictly-faithful narration built only from the exhibit's
    own fields. No invented scores, dates, or causes."""
    who = _who(ex.persona)
    d = ex.decision
    parts: list[str] = []

    lead = f"{who} recorded this as **{d.outcome}**"
    if ex.date:
        lead += f" on {ex.date}"
    lead += f" — {ex.title.lower()}."
    if d.attempts:
        lead += f" It took {d.attempts} attempt{'s' if d.attempts != 1 else ''}."
    parts.append(lead)

    if d.rationale.strip():
        note = f"The note on record reads: \"{d.rationale.strip()}\""
        if d.rationale_source:
            note += f" (from {d.rationale_source})"
        parts.append(note + ".")
    else:
        parts.append(
            "The logs record the outcome but carry no written rationale, so this "
            "exhibit stays intentionally sparse rather than dressed up with a reason "
            "the evidence does not hold.")

    if ex.verdict and ex.verdict.score is not None:
        v = ex.verdict
        line = f"Measured similarity to the reference: {v.score}"
        if v.method:
            line += f" via {v.method}"
        if v.model_verdict:
            line += f"; the vision read was {v.model_verdict}"
        parts.append(line + ".")

    if ex.cites_criteria:
        shown = ", ".join(f"`{c}`" for c in ex.cites_criteria[:4])
        more = "" if len(ex.cites_criteria) <= 4 else f" (and {len(ex.cites_criteria) - 4} more)"
        parts.append(f"It cites {shown}{more}.")

    return "\n\n".join(parts) + "\n"


def narrate(ex: Exhibit, sources: str = "") -> tuple[str, bool]:
    """Return (markdown prose, used_stub). Real path uses Sonnet 4.6; the stub /
    empty-text path falls back to faithful local prose."""
    prompt = build_prompt(ex, sources)
    resp = asyncio.run(invoke_museum_prose(prompt=prompt))
    if resp.stub_fallback or not (resp.text or "").strip():
        return _fallback_prose(ex), True
    return resp.text.strip() + "\n", False


@register_node("museum_writer")
class MuseumWriterNode:
    """Mo as an AgentSpec node so she sits in the fleet contract like Cy and Em."""

    name: ClassVar[str] = "museum_writer"
    inputs: ClassVar[dict] = {"museum_root": str, "exhibit": dict}
    outputs: ClassVar[dict] = {"narrative_path": str}
    cites_criteria: ClassVar[list[str]] = []

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        # Sonnet 4.6 is subscription-absorbed → $0 incremental.
        return CostEstimate(usd=0.0, latency_s=8.0, confidence=0.5)

    def run(self, ctx: AgentContext) -> AgentResult:
        museum_root = Path(ctx.inputs["museum_root"])
        ex = exhibit_from_dict(ctx.inputs["exhibit"])
        sources = ctx.inputs.get("sources", "") if isinstance(ctx.inputs, dict) else ""
        prose, used_stub = narrate(ex, sources)
        path = exhibit_dir(museum_root, ex) / "exhibit.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(prose, encoding="utf-8")
        return AgentResult(
            outputs={"narrative_path": str(path)},
            notes=f"mo:{'stub' if used_stub else 'sonnet'} narrated {ex.exhibit_id}",
        )
