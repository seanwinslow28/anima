"""Style-neutrality guardrail tests for anima's standing-context preambles.

Per Task 1.4.6. The audit that drove Task 1.4.5 found pencil-test as the
default register baked into four prompt files. This test prevents regression:
register-anchored markers in load-bearing prompt sections must be paired
with at least one cross-register example, proving the language is
comparative rather than default-anchored.

The doctrine note at docs/prompt-style-neutrality-doctrine.md is the
human-readable companion explaining the principle and the procedure for
adding a new style register or new prompt file.

Test scope — load-bearing sections only:

  The "what you must not do" and "the lens you bring" sections drive Opus's
  seed behavior. Single-register language there is a structural failure.

  The "what good looks like" sections are explicit examples. Single-register
  language in a scaffolded `## What good looks like — {register}` /
  `### Example A — sean-anchor (...)` style heading is allowed because
  scope is named at the boundary.

Failure surfaces tell the contributor specifically which file and which
register pairing is missing so the fix is mechanical.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

PROMPTS_DIR = Path(__file__).resolve().parents[1] / "pipeline" / "agents" / "prompts"

# The closed style-register vocabulary anima supports. Every register named
# in a prompt is fine; the failure mode the guardrail catches is naming
# pencil-test (or any one register) as the implicit default.
_STYLE_REGISTERS = frozenset({
    "pencil-test-colored",
    "pixel-art-8bit",
    "line-art-only",
    "watercolor",
    "photoreal",
    "3d-rendered",
})

# Register-specific marker phrases. When any pencil marker appears in a
# load-bearing section, at least one pixel / watercolor / photoreal marker
# (or a different-register name) must also appear in the same section.
# Phrases are searched case-insensitively as whole substrings.
_PENCIL_MARKERS = frozenset({
    "cross-hatching",
    "construction lines",
    "graphite",
    "cream paper",
    "varied 1-3px",
    "pencil-test rough",
    "pencil-test-colored",
})

_PIXEL_MARKERS = frozenset({
    "dithering",
    "integer-pixel grid",
    "anti-aliasing",
    "closed palette",
    "indexed palette",
    "closed indexed palette",
    "limited indexed palette",
    "pixel-art-8bit",
})

_WATERCOLOR_MARKERS = frozenset({
    "watercolor",
    "edge-feathering",
    "pigment-pool",
    "paper grain",
    "wet-media",
})

_PHOTOREAL_MARKERS = frozenset({
    "photoreal",
    "lit volume",
    "surface detail",
    "specular",
})

_LINEART_MARKERS = frozenset({
    "line-art-only",
})

_3D_MARKERS = frozenset({
    "3d-rendered",
    "raytraced",
    "pbr shading",
})

# Map register-name → its marker set, for the failure-message companion-find.
_REGISTERS_TO_MARKERS = {
    "pencil-test-colored": _PENCIL_MARKERS,
    "pixel-art-8bit": _PIXEL_MARKERS,
    "watercolor": _WATERCOLOR_MARKERS,
    "photoreal": _PHOTOREAL_MARKERS,
    "line-art-only": _LINEART_MARKERS,
    "3d-rendered": _3D_MARKERS,
}

# Prompt files this test audits. Adding a new addendum to anima's fleet means
# adding it here; the doctrine note names the procedure.
_AUDITED_FILES = (
    "anima-standing-context.md",
    "cy-character-designer-context.md",
    "em-vision-critic-context.md",
    "maya-planner-context.md",
)


# H2 headings whose bodies are EXAMPLE blocks (scope is named at the
# boundary so single-register content inside is allowed). The match is
# case-insensitive and partial — "What good looks like" catches subheadings.
_EXAMPLE_SECTION_PATTERNS = frozenset({
    "what good looks like",
    "example a",
    "example b",
})


def _split_into_sections(md: str) -> list[tuple[str, str]]:
    """Split markdown into (heading_text_lowercased, body) tuples at every H2
    boundary. Body for the implicit pre-first-H2 section is keyed under '' ."""
    lines = md.splitlines()
    sections: list[tuple[str, list[str]]] = [("", [])]
    for line in lines:
        if line.startswith("## "):
            sections.append((line[3:].strip().lower(), []))
        elif line.startswith("### "):
            # Subheading inside the current H2; carries forward in same body.
            sections[-1][1].append(line)
        else:
            sections[-1][1].append(line)
    return [(heading, "\n".join(body)) for heading, body in sections]


def _is_example_section(heading: str) -> bool:
    return any(pattern in heading for pattern in _EXAMPLE_SECTION_PATTERNS)


def _detect_register_markers(text_lower: str) -> dict[str, set[str]]:
    """Return {register: {marker_phrase, ...}} for markers present in text."""
    hits: dict[str, set[str]] = {}
    for register, markers in _REGISTERS_TO_MARKERS.items():
        for marker in markers:
            if marker in text_lower:
                hits.setdefault(register, set()).add(marker)
    return hits


@pytest.mark.parametrize("filename", _AUDITED_FILES)
def test_load_bearing_sections_carry_comparative_register_language(filename):
    """Pencil markers in any load-bearing section must be paired with at
    least one cross-register marker. Single-register defaults are the bias
    the audit caught; the test prevents regression.
    """
    path = PROMPTS_DIR / filename
    assert path.exists(), f"audited file {filename} not found at {path}"
    md = path.read_text(encoding="utf-8").lower()

    sections = _split_into_sections(md)
    failures: list[str] = []
    for heading, body in sections:
        if _is_example_section(heading):
            continue
        if not body.strip():
            continue
        hits = _detect_register_markers(body)
        if not hits:
            continue
        # Section names at least one register's markers. If only one register
        # appears, the language reads as default-anchored — fail with a
        # message naming the missing companion registers.
        if len(hits) == 1:
            (only_register,) = hits.keys()
            failures.append(
                f"{filename} section {heading!r}: register-anchored markers "
                f"for {only_register!r} appear without companion examples "
                f"from another register. Markers found: {sorted(hits[only_register])}. "
                f"Add at least one parallel example (pixel-art / watercolor / "
                f"photoreal / line-art / 3d) so the language reads as "
                f"comparative, not default."
            )

    assert not failures, "\n".join(failures)


@pytest.mark.parametrize("filename", _AUDITED_FILES)
def test_no_implicit_pencil_default_in_failure_modes(filename):
    """The "what you must not do" / failure-modes section in each preamble
    must mention at least two style registers by name when it discusses
    aesthetic / template-trap / register drift. This catches the specific
    bias the Task 1.4.5 audit found.
    """
    path = PROMPTS_DIR / filename
    md = path.read_text(encoding="utf-8").lower()
    sections = _split_into_sections(md)
    for heading, body in sections:
        if "must not" not in heading and "non-negotiables" not in heading:
            continue
        if not body.strip():
            continue
        # Count distinct style register names mentioned by literal name.
        registers_named = {r for r in _STYLE_REGISTERS if r in body}
        # If the section mentions style register concepts (drift, register,
        # aesthetic) at all, it must name at least two registers.
        mentions_register = (
            "style register" in body
            or "style_register" in body
            or "aesthetic drift" in body
            or "template-trap" in body
            or "register drift" in body
        )
        if mentions_register and len(registers_named) < 2:
            pytest.fail(
                f"{filename} section {heading!r} mentions style-register drift "
                f"but names < 2 distinct registers (found: {sorted(registers_named)}). "
                f"Failure-mode prose must compare across registers, not anchor "
                f"on a default."
            )


def test_doctrine_note_exists_and_names_the_principle():
    """The companion doctrine note must exist and reference the test + procedure."""
    doctrine_path = (
        Path(__file__).resolve().parents[1]
        / "docs" / "prompt-style-neutrality-doctrine.md"
    )
    assert doctrine_path.exists(), (
        f"doctrine note not found at {doctrine_path}; Task 1.4.6 ships both "
        f"the test and the doctrine note. See the plan."
    )
    body = doctrine_path.read_text(encoding="utf-8")
    # The test filename should appear so the doctrine doubles as a pointer
    # to the enforcement mechanism.
    assert "test_prompt_style_neutrality.py" in body
    # The closed vocabulary should be named.
    for register in _STYLE_REGISTERS:
        assert register in body, f"doctrine note must name {register} register"
