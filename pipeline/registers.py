"""The canonical home of anima's closed style_register vocabulary.

One frozen RegisterSpec per register; every register touch-point reads from
here instead of carrying its own copy:

- ``character_designer._build_plate_prompt`` / ``_resolve_plate_model``
  (the clause library + model routing that used to live in
  ``_REGISTER_CLAUSE_LIBRARY`` / ``_REGISTER_MODELS``),
- ``character_designer._STUB_STYLE_REGISTER_BY_KEYWORD`` (derived from the
  specs' ``stub_keywords``),
- ``tests/test_prompt_style_neutrality.py`` (``ALL_REGISTERS`` + markers),
- the human touch-points — the ``character.yaml.template`` permitted-values
  comment and Cy's ``## What good looks like`` blocks — stay prose, and
  ``tests/test_register_registry.py`` enforces they exist per register.

The vocabulary is CLOSED (the style-neutrality doctrine's thesis:
validators cannot recover taste that was absent at generation time). The
registry makes closedness enforced rather than conventional:

- a **nonempty, unrecognized** register (a typo, or a style nobody has
  authored yet) raises :class:`UnknownRegisterError` — loud, never a
  silent coercion to the pencil default;
- an **empty/missing** register is the CALLER's back-compat case — every
  pre-registry character folder relies on empty defaulting to
  ``pencil-test-colored``, so callers pass
  ``get_register(value or DEFAULT_REGISTER)``.

Adding a register is the five-step drill in
docs/active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md
§1.3: research → one RegisterSpec entry here → the Cy example block → the
template-comment line → run the suite (the completeness tests refuse to
pass until all of them exist).

Values for the six existing registers are copied VERBATIM from the
pre-registry tables in character_designer.py / test_prompt_style_neutrality.py
(commit 4a75500); tests/test_register_characterization.py is the
byte-identical oracle proving nothing shifted for the locked Bibles.
"""

from __future__ import annotations

from dataclasses import dataclass

# Model ids match the pre-registry _REGISTER_MODELS table. NB2 is the
# generation/editing default for every register (cheaper, faster, more
# identity-stable across edits); NB Pro is reserved for painterly FINAL
# renders — a documented seam with no consumer yet.
NB2_FLASH = "gemini-3.1-flash-image-preview"
NB_PRO = "gemini-3-pro-image-preview"

# The back-compat default. Empty/missing style_register still means the
# pencil-test reference register; the constant lives here so callers spell
# the rule identically.
DEFAULT_REGISTER = "pencil-test-colored"


class UnknownRegisterError(ValueError):
    """A nonempty style_register that is not in the closed vocabulary.

    Raised loud at lookup time so a typo (or an unauthored style) can never
    silently author a pencil-test character. Subclasses ValueError so broad
    caller guards still catch it.
    """

    def __init__(self, name: str):
        self.name = name
        known = ", ".join(sorted(REGISTRY))
        super().__init__(
            f"unknown style_register {name!r} — not in the closed vocabulary "
            f"({known}). Adding a register is a deliberate commit: see "
            f"docs/architecture/prompt-style-neutrality-doctrine.md and "
            f"pipeline/registers.py."
        )


@dataclass(frozen=True)
class RegisterSpec:
    """One deliberately-authored style register. All fields are data the
    touch-points read; the register's *taste* (the Cy worked example, the
    research write-up, the refs/) stays prose and files, enforced-present
    by tests/test_register_registry.py."""

    name: str
    summary: str  # one line for the character.yaml.template human list
    identity_lock: str  # was _REGISTER_CLAUSE_LIBRARY[name]["identity_lock"]
    preserve: str  # was _REGISTER_CLAUSE_LIBRARY[name]["preserve"]
    style_token: str  # was _REGISTER_CLAUSE_LIBRARY[name]["style_token"]
    generation_model: str  # was _REGISTER_MODELS[name]["generation"]
    final_model: str  # was _REGISTER_MODELS[name]["final"]
    markers: frozenset[str]  # was test_prompt_style_neutrality._REGISTERS_TO_MARKERS
    stub_keywords: tuple[str, ...] = ()  # reverse of _STUB_STYLE_REGISTER_BY_KEYWORD
    reference_images: tuple[str, ...] = ()  # registers/{name}/refs/ exemplars


# NOTE: insertion order is load-bearing for ONE consumer — the derived stub
# keyword map (character_designer._STUB_STYLE_REGISTER_BY_KEYWORD) preserves
# the pre-registry precedence (mascot, pixel, watercolor, lineart, photoreal,
# 3d), which requires watercolor's spec to come before line-art-only's.
# tests/test_register_characterization.py pins the precedence edges.
REGISTRY: dict[str, RegisterSpec] = {
    spec.name: spec
    for spec in (
        RegisterSpec(
            name="pencil-test-colored",
            summary=(
                "Sean's Act 1/2 register. Warm cream paper, varied graphite "
                "line weight, hand-drawn construction lines, limited "
                "desaturated palette, visible cross-hatching."
            ),
            identity_lock=(
                "Match the face, hair, full color palette, skin tone, and "
                "proportions of Image 1 exactly."
            ),
            preserve=(
                "Keep the warm cream paper, the cross-hatch shadow, and the full "
                "color of Image 1. Do not render the figure in monochrome. No "
                "photographic shading."
            ),
            style_token=(
                "Warm pencil-test render: graphite line (not vector black), flat "
                "color fills, cross-hatch shadow, warm cream paper, hole-punch "
                "production marks."
            ),
            generation_model=NB2_FLASH,
            final_model=NB2_FLASH,
            markers=frozenset({
                "cross-hatching",
                "construction lines",
                "graphite",
                "cream paper",
                "varied 1-3px",
                "pencil-test rough",
                "pencil-test-colored",
            }),
        ),
        RegisterSpec(
            name="pixel-art-8bit",
            summary=(
                "Claude mascot's register. Quantized palette, dithering "
                "patterns, sub-32-color flat fills."
            ),
            identity_lock=(
                "Match the indexed palette, the round silhouette, and the "
                "head-to-body ratio of Image 1 exactly."
            ),
            preserve="Hard pixel edges. No smooth anti-aliased gradients.",
            style_token=(
                "16-bit pixel-art sprite, limited indexed palette, hard pixel "
                "edges, clean outlines."
            ),
            generation_model=NB2_FLASH,
            final_model=NB2_FLASH,
            markers=frozenset({
                "dithering",
                "integer-pixel grid",
                "anti-aliasing",
                "closed palette",
                "indexed palette",
                "closed indexed palette",
                "limited indexed palette",
                "pixel-art-8bit",
            }),
            stub_keywords=("mascot", "pixel"),
        ),
        RegisterSpec(
            name="watercolor",
            summary="Soft wet-media bleeds, paper grain, layered washes.",
            identity_lock=(
                "Match the face, the pigment-pool palette, and the proportions of "
                "Image 1 exactly."
            ),
            preserve="Keep the paper grain; let washes bleed; no hard vector edges.",
            style_token="Soft watercolor wash, pigment-pool bleed, visible paper grain.",
            generation_model=NB2_FLASH,
            final_model=NB_PRO,
            markers=frozenset({
                "watercolor",
                "edge-feathering",
                "pigment-pool",
                "paper grain",
                "wet-media",
            }),
            stub_keywords=("watercolor",),
        ),
        RegisterSpec(
            name="line-art-only",
            summary="Pure black-on-white linework, no color, no fill.",
            identity_lock=(
                "Match the contour shapes, line weight, hair silhouette, and "
                "proportions of Image 1 exactly."
            ),
            preserve=(
                "No shading, no gradients, no soft shadow, no texture; flat color "
                "fills only."
            ),
            style_token="Clean line art, bold uniform outlines, flat fills.",
            generation_model=NB2_FLASH,
            final_model=NB2_FLASH,
            markers=frozenset({"line-art-only"}),
            stub_keywords=("lineart",),
        ),
        RegisterSpec(
            name="photoreal",
            summary="Photographic rendering, lit volumes, surface detail.",
            identity_lock=(
                "Match the face, skin tone, hair, and proportions of Image 1 exactly."
            ),
            preserve=(
                "Keep the lighting direction and color temperature of Image 1; "
                "clean edges, no halos."
            ),
            style_token=(
                "Photographic rendering, natural lighting, shallow depth of field."
            ),
            generation_model=NB2_FLASH,
            final_model=NB_PRO,
            markers=frozenset({
                "photoreal",
                "lit volume",
                "surface detail",
                "specular",
            }),
            stub_keywords=("photoreal",),
        ),
        RegisterSpec(
            name="3d-rendered",
            summary="Constructed geometry, raytraced or PBR shading.",
            identity_lock=(
                "Match the face, material palette, and proportions of Image 1 exactly."
            ),
            preserve="Keep soft global illumination; no flat-shading artifacts.",
            style_token=(
                "3D-rendered look, soft global illumination, subtle ambient "
                "occlusion."
            ),
            generation_model=NB2_FLASH,
            final_model=NB_PRO,
            markers=frozenset({"3d-rendered", "raytraced", "pbr shading"}),
            stub_keywords=("3d",),
        ),
    )
}

ALL_REGISTERS: frozenset[str] = frozenset(REGISTRY)


def get_register(name: str) -> RegisterSpec:
    """Look up a register by exact name. Nonempty-unknown raises loud.

    Callers own the empty/missing back-compat rule:
    ``get_register(value or DEFAULT_REGISTER)``.
    """
    try:
        return REGISTRY[name]
    except KeyError:
        raise UnknownRegisterError(name) from None
