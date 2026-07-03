"""StudioBrief — parse / validate / render the 8-section Studio Brief (§5.1).

parse() is lenient (collects whatever H2 sections are present, byte-exact
round-trip); validate() is the strict shape gate: the seven headers, in
order, non-empty, plus the `### What this is NOT` sub-block under tone.
"""

from __future__ import annotations

from dataclasses import dataclass, field

REQUIRED_SECTIONS = (
    "What is this story about?",
    "Who is this character?",
    "What is the tone?",
    "What is the format?",
    "What is the target medium?",
    "What is the deadline?",
    "What are the non-negotiables?",
)

TONE_SECTION = "What is the tone?"
WHAT_THIS_IS_NOT = "### What this is NOT"


@dataclass
class StudioBrief:
    """Sections keyed by H2 title (document order); preamble = text before the first H2."""

    preamble: str = ""
    sections: dict[str, str] = field(default_factory=dict)

    def validate(self) -> list[str]:
        problems: list[str] = []
        present = list(self.sections)
        for title in REQUIRED_SECTIONS:
            if title not in present:
                problems.append(f"missing section: ## {title}")
            elif not self.sections[title].strip():
                problems.append(f"empty body: ## {title}")
        found_order = [t for t in present if t in REQUIRED_SECTIONS]
        expected_order = [t for t in REQUIRED_SECTIONS if t in found_order]
        if found_order != expected_order:
            problems.append(
                f"sections out of order: found {found_order}, expected {expected_order}"
            )
        tone = self.sections.get(TONE_SECTION, "")
        if TONE_SECTION in present and WHAT_THIS_IS_NOT not in tone:
            problems.append(f"tone section is missing the `{WHAT_THIS_IS_NOT}` sub-block")
        return problems

    def render(self) -> str:
        parts = [self.preamble]
        for title, body in self.sections.items():
            parts.append(f"## {title}\n{body}")
        return "".join(parts)


def parse(text: str) -> StudioBrief:
    preamble_lines: list[str] = []
    sections: dict[str, str] = {}
    current: str | None = None
    body_lines: list[str] = []
    for line in text.splitlines(keepends=True):
        if line.startswith("## "):
            if current is not None:
                sections[current] = "".join(body_lines)
            current = line[3:].rstrip("\n")
            body_lines = []
        elif current is None:
            preamble_lines.append(line)
        else:
            body_lines.append(line)
    if current is not None:
        sections[current] = "".join(body_lines)
    return StudioBrief(preamble="".join(preamble_lines), sections=sections)
