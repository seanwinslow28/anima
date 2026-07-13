"""Register #3 — samurai-jack-s5: the flat-cinematic Tartakovsky sibling.

Authored from the wire-ready research (registers/samurai-jack-s5/research.md,
LOOK RATIFIED — HERO LOCKED 2026-07-13). The mutually-exclusive FLAT sibling of
primal-sketch-grit: where primal keeps a heavy weight-varying ink line OVER the
color and paints gritty texture everywhere, samurai-jack-s5 inverts every
still-frame axis — almost no visible outline (form reads by adjacent color and
value contrast), clean flat poster-graphic color shapes, and hard-edged flat
shadow masses.

Two load-bearing facts baked into the spec:

- Genericization is doubly load-bearing (research §7 / plan §5): the register is
  a SCHOOL of flat cinematic 2D poster-art captured attribute-only — no show,
  creator, character, or studio name in any clause, marker, comment, or example.
  The one deliberate exception is the machine slug/name-marker `samurai-jack-s5`
  (internal, never a production-prompt string), and because this register's slug
  IS a franchise name the genericization scan is stronger than the siblings':
  it normalizes hyphens to spaces (catching both "samurai jack" and
  "samurai-jack") and exempts ONLY that slug.
- Transport = gpt-image (`gpt-image-2`), UNWIRED, fails loud (plan §2B): the
  existing SUPPORTED_IMAGE_MODELS allowlist guard already covers it — no new
  code. invoke_image_edit raises UnwiredTransportError rather than silently
  falling back to Gemini/NB2. final_model rides the dormant painterly-final seam
  (NB Pro, no consumer yet — same as watercolor/photoreal/3d/primal/nicktoon).

The stub smoke mirrors the two siblings' Task 2.5: driving Cy's stub path with a
samurai-named character produces a coherent stubbed Bible with NO silent pencil
coercion, $0, no keys.
"""

from __future__ import annotations

import pytest

from pipeline.registers import (
    ALL_REGISTERS,
    GPT_IMAGE,
    NB_PRO,
    get_register,
)

_SAMURAI = "samurai-jack-s5"


def test_samurai_register_is_registered():
    assert _SAMURAI in ALL_REGISTERS
    spec = get_register(_SAMURAI)
    assert spec.name == _SAMURAI


def test_samurai_plate_prompt_carries_the_register_clauses():
    """The five-slot emitter framed against the flat cinematic school, not
    pencil or primal: the register's five ratified money-phrases are present;
    no pencil-test vocabulary and no primal/sibling vocabulary leaks in (the two
    drift directions this register has to fence off)."""
    from pipeline.agents.character_designer import _build_plate_prompt

    p = _build_plate_prompt(
        "lone figure at the crest of a vast empty ridge, holding still",
        style_register=_SAMURAI,
        has_pose_ref=False,
    )
    lower = p.lower()
    # the register's own five money-phrases (final strings from research §1)
    assert "almost no visible outlines" in lower
    assert "hard-edged flat shadow" in lower
    assert "single emotional color cast" in lower
    assert "dramatic negative space" in lower
    assert "silent-samurai-film staging" in lower
    # negative controls — no pencil-test vocabulary leak
    assert "cream paper" not in lower
    assert "graphite" not in lower
    assert "cross-hatch" not in lower
    # negative controls — no primal / sibling vocabulary leak
    assert "weight-varying ink" not in lower
    assert "over the color" not in lower
    assert "gritty" not in lower


def test_samurai_routing_is_gpt_image_generation():
    """Plan §2B: transport RESOLVED to gpt-image — the registry records the
    honest model, and invoke_image_edit's UnwiredTransportError guard makes it
    fail LOUD (no gpt-image runner is wired yet) instead of silently falling
    back to Gemini/NB2. Final render rides the painterly-final seam (NB Pro, no
    consumer yet). Imports the constants, not raw strings (plan Task 1)."""
    from pipeline.agents.character_designer import _resolve_plate_model

    assert _resolve_plate_model(_SAMURAI, {}) == GPT_IMAGE
    assert _resolve_plate_model(_SAMURAI, {}, final=True) == NB_PRO


def test_samurai_stub_keyword_inference():
    """'samurai' (the genre word) added to the stub keyword inference —
    appended AFTER the legacy six + primal + nicktoon/grossout, so existing
    precedence is untouched."""
    from pipeline.agents.character_designer import _infer_stub_style_register

    assert _infer_stub_style_register("samurai-ronin") == _SAMURAI
    # earlier keywords still win first (appended-last precedence)
    assert _infer_stub_style_register("pixel-samurai-test") == "pixel-art-8bit"
    assert _infer_stub_style_register("primal-samurai-test") == "primal-sketch-grit"
    assert (
        _infer_stub_style_register("nicktoon-samurai-test")
        == "90s-nicktoon-grossout"
    )
    # no keyword hit still defaults to pencil
    assert _infer_stub_style_register("ronin") == "pencil-test-colored"


def test_samurai_stub_envelope_no_pencil_coercion(tmp_path):
    """The $0 Cy stub smoke: a stub Bible for a samurai-named character carries
    the register end-to-end — never silently pencil."""
    from pipeline.agents.character_designer import CharacterDesignerNode

    char_dir = tmp_path / "characters" / "samurai-ronin"
    char_dir.mkdir(parents=True)
    envelope = CharacterDesignerNode()._build_stub_envelope(char_dir)
    assert envelope["character_yaml"]["style_register"] == _SAMURAI


def test_samurai_markers_are_exact_and_do_not_collide():
    """The exact ratified marker set (Task 2) AND no overlap with any other
    register's markers."""
    from pipeline.registers import REGISTRY

    spec = get_register(_SAMURAI)
    assert spec.markers == frozenset({
        "samurai-jack-s5",
        "outline-sparse flat color shapes",
        "hard-edged flat shadow masses",
        "single emotional color cast",
        "dramatic cinematic negative space",
        "silent-samurai-film staging",
    })
    for name, other in REGISTRY.items():
        if name == _SAMURAI:
            continue
        overlap = spec.markers & other.markers
        assert not overlap, f"marker collision with {name}: {sorted(overlap)}"


def test_samurai_spec_is_genericized_attribute_only():
    """Research §7 / plan §5 — doubly load-bearing: no show, studio, artist,
    creator, or character name anywhere in the spec's semantic fields, markers,
    or stub keywords. The register is a school of flat cinematic 2D captured by
    attributes.

    Stronger than the siblings' raw-substring scan (plan §4.1): this register's
    slug IS a franchise name, so the scan normalizes hyphens to spaces (catching
    both "samurai jack" and a stray "samurai-jack") and exempts ONLY the
    slug/name-marker. After normalization the bare genre word "samurai" (the
    stub keyword + the staging phrase) is not forbidden and stays clean."""
    spec = get_register(_SAMURAI)
    scanned = (
        [spec.summary, spec.identity_lock, spec.preserve, spec.style_token]
        + list(spec.stub_keywords)
        + [m for m in spec.markers if m != _SAMURAI]
    )
    # normalize hyphens to spaces so a hyphenated leak is caught as the space form
    joined = " ".join(scanned).lower().replace("-", " ")
    forbidden = (
        "samurai jack",
        "tartakovsky",
        "genndy",
        "aku",
        "ashi",
        "scotsman",
        "clone wars",
        "cartoon network",
        "adult swim",
        "toonami",
        "primal",
    )
    for name in forbidden:
        assert name not in joined, f"franchise identifier {name!r} leaked into the spec"


def test_samurai_transport_is_honest_and_unwired(tmp_path):
    """Plan §2B: the spec records the honest generation model (gpt-image-2),
    which is NOT in the wired allowlist, so invoke_image_edit fails loud. Binds
    the register's model to the existing boundary; the no-output / no-cache
    filesystem side-effects are already covered at tests/test_nb_pro_runner.py
    (red-team fold — don't duplicate the transport suite)."""
    from pipeline.agents.nb_pro_runner import (
        SUPPORTED_IMAGE_MODELS,
        UnwiredTransportError,
        invoke_image_edit,
    )

    spec = get_register(_SAMURAI)
    assert spec.generation_model == GPT_IMAGE
    assert GPT_IMAGE not in SUPPORTED_IMAGE_MODELS

    with pytest.raises(UnwiredTransportError):
        invoke_image_edit(
            prompt="samurai-jack-s5 plate",
            reference_images=[],
            output_path=tmp_path / "out.png",
            cache_dir=tmp_path,
            model=spec.generation_model,
        )
