"""Tasks 1.1 + 1.3 — the registry module contract + the completeness sync.

pipeline/registers.py is the single canonical home of the closed
style_register vocabulary (the CONVERGED plan §1.2). These tests are the
enforcement that makes "closed" real:

- every register's spec is COMPLETE (clauses, models, markers) — an
  incomplete registration fails loud, not silent;
- every register has its human touch-points: a mention in Cy's context
  (the closed-vocab lines) and a line in the character.yaml template
  comment. A register added to REGISTRY without them goes red;
- a nonempty unknown register RAISES (UnknownRegisterError), never
  silently coerces to pencil-test-colored.

Deviation from the plan's Task 1.3 snippet, per its own R5 mitigation
("pick the matcher that's green for all 6 today, red only for a forgetful
new register"): only pencil-test-colored and pixel-art-8bit carry a
`## What good looks like` example block on main — the other four legacy
registers predate the worked-example convention and no character has ever
shipped in them. They are explicitly grandfathered below; every register
added after the registry landed (starting with primal-sketch-grit) MUST
ship an example block, and is NOT grandfathered.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.registers import (
    ALL_REGISTERS,
    REGISTRY,
    RegisterSpec,
    UnknownRegisterError,
    get_register,
)

_REPO = Path(__file__).resolve().parents[1]
_CY_CONTEXT = _REPO / "pipeline" / "agents" / "prompts" / "cy-character-designer-context.md"
_TEMPLATE = _REPO / "templates" / "bible" / "character.yaml.template"

_SIX_EXISTING = frozenset({
    "pencil-test-colored",
    "pixel-art-8bit",
    "line-art-only",
    "watercolor",
    "photoreal",
    "3d-rendered",
})

# Historical debt, not a waiver for new work: these four registers were in
# the closed vocabulary before the worked-example convention existed and
# have never had a shipped character. A NEW register may not be added here
# without Sean's explicit sign-off in the plan doc.
_PRE_REGISTRY_REGISTERS_WITHOUT_CY_EXAMPLE = frozenset({
    "line-art-only",
    "watercolor",
    "photoreal",
    "3d-rendered",
})


def test_registry_carries_the_six_existing_registers():
    assert _SIX_EXISTING <= ALL_REGISTERS


def test_every_register_is_complete():
    for name, spec in REGISTRY.items():
        assert isinstance(spec, RegisterSpec)
        assert spec.name == name
        assert spec.summary, f"{name}: empty summary"
        assert spec.identity_lock, f"{name}: empty identity_lock"
        assert spec.preserve, f"{name}: empty preserve"
        assert spec.style_token, f"{name}: empty style_token"
        assert spec.generation_model, f"{name}: empty generation_model"
        assert spec.final_model, f"{name}: empty final_model"
        assert spec.markers, f"{name}: markers must be non-empty (at least the name)"


def test_register_specs_are_frozen():
    spec = get_register("pencil-test-colored")
    with pytest.raises(Exception):
        spec.style_token = "mutated"  # type: ignore[misc]


def test_every_register_is_named_in_cy_context():
    """Cy must know the register is legal — the closed-vocab enumerations in
    cy-character-designer-context.md must name every registered register."""
    cy = _CY_CONTEXT.read_text(encoding="utf-8")
    for name in ALL_REGISTERS:
        assert name in cy, (
            f"{name} is in REGISTRY but never named in "
            f"cy-character-designer-context.md — add it to the closed-vocab "
            f"lines (and a What-good-looks-like example block)."
        )


def test_every_post_registry_register_has_a_cy_example_block():
    """Section-scoped matcher (red-team fold): the register label must appear
    INSIDE the `## What good looks like` H2 section, matching the real
    `### Example X — {char} (style_register: {name})` structure."""
    cy = _CY_CONTEXT.read_text(encoding="utf-8")
    section = cy.split("## What good looks like", 1)[1]
    section = section.split("\n## ", 1)[0]
    for name in ALL_REGISTERS - _PRE_REGISTRY_REGISTERS_WITHOUT_CY_EXAMPLE:
        assert f"style_register: {name}" in section, (
            f"{name} has no example block under '## What good looks like' in "
            f"cy-character-designer-context.md. Every register added since the "
            f"registry landed must ship a worked example of the look."
        )


def test_every_register_is_in_the_template_comment():
    tmpl = _TEMPLATE.read_text(encoding="utf-8")
    for name in ALL_REGISTERS:
        assert name in tmpl, (
            f"{name} is in REGISTRY but not in the "
            f"character.yaml.template permitted-values comment."
        )


def test_get_register_returns_the_matching_spec():
    for name in ALL_REGISTERS:
        assert get_register(name).name == name


def test_unknown_register_raises_not_coerces():
    with pytest.raises(UnknownRegisterError):
        get_register("totally-made-up-register")


def test_unknown_register_error_is_a_value_error():
    """Callers that guard broadly on ValueError still catch it."""
    assert issubclass(UnknownRegisterError, ValueError)
