"""Register #4 of the vocabulary expansion — flat-cast-painted-world.

The mixed-media "fusion" register Sean selected by eye (costed Higgsfield image
spike + Seedance 2.0 motion test, 2026-07-13; his eye the sole arbiter). A flat,
boldly hand-inked 2D cartoon CAST (living boiling outline, flat cel color, no
rendered volume) that visibly POPS against a richly hand-PAINTED gritty
children's-storybook WORLD (dry-brush weathered urban surfaces, muted earthy
palette, folk-decorative flourishes, gouache washes, golden-hour grime) — two
media in one frame, unified only by the shared warm light + a faint grain.
Authored from the wire-ready research (registers/flat-cast-painted-world/
research.md, LOOK RATIFIED — HERO LOCKED 2026-07-13).

Its identity IS the deliberate TWO-MEDIA SPLIT — the axis that makes it mutually
exclusive from its neighbors:
- vs Collage Real (banked): painted world, NOT photographic (the firewall);
- vs Gritty Storybook (banked): two media split, NOT one unified paint;
- vs primal-sketch-grit: grit stays OFF the flat-cel figure, on the painted
  world only — vs weight-varying ink kept OVER the color across everything;
- vs samurai-jack-s5: bold boiling OUTLINE + gritty painterly world — vs
  near-no-outline + clean flats + dramatic negative space.

Two load-bearing facts baked into the spec:

- Genericization is doubly load-bearing (research §7): the register is a SCHOOL
  of mixed-media 2D craft captured attribute-only — no show, creator, character,
  studio, or artist name in any clause, marker, comment, or example. The sole
  permitted named identifier is the machine slug `flat-cast-painted-world`, which
  is NOT a franchise name (so the raw-substring scan the two siblings use is
  sufficient here — no hyphen-normalization carve-out). Named-source negatives
  stay OUT of `preserve` (naming a neighbor look can evoke it in the image
  model); in particular the world's real cross-hatched texture is written as
  "dry-brush / hatched" so the exact compound `cross-hatch` (pencil-test's
  signature) never leaks in.
- Transport = gpt-image (`gpt-image-2`), wired through Higgsfield (research §4): the
  Step-S NB2 confirmation spike came back NO-GO (NB2 collapsed the two-media
  split into one unified medium and dropped the boiling line), so the honest
  recorded model is GPT_IMAGE. The google-genai SUPPORTED_IMAGE_MODELS allowlist
  remains Gemini-only; the separate Higgsfield mapping owns this route.
  final_model rides the dormant painterly-final seam (NB Pro, no consumer yet —
  same as watercolor/photoreal/3d/primal/samurai).
"""

from __future__ import annotations

from pipeline.registers import (
    ALL_REGISTERS,
    GPT_IMAGE,
    NB_PRO,
    get_register,
)

_FUSION = "flat-cast-painted-world"


def test_fusion_register_is_registered():
    assert _FUSION in ALL_REGISTERS
    spec = get_register(_FUSION)
    assert spec.name == _FUSION


def test_fusion_plate_prompt_carries_the_register_clauses():
    """The five-slot emitter framed against the mixed-media school: the
    register's own money-phrases are present; no pencil-test vocabulary, no
    primal/sibling ink-over-color vocabulary, and no samurai flat-minimal
    vocabulary leaks in (the drift directions this register fences off)."""
    from pipeline.agents.character_designer import _build_plate_prompt

    p = _build_plate_prompt(
        "the cast crouched on a weathered corner-store stoop at golden hour",
        style_register=_FUSION,
        has_pose_ref=False,
    )
    lower = p.lower()
    # the register's own money-phrases (final strings from research §2)
    assert "boiling" in lower
    assert "flat cel color" in lower
    assert "no rendered volume" in lower
    assert "two media in one frame" in lower
    assert "hand-painted" in lower
    assert "muted earthy" in lower
    assert "golden-hour" in lower
    # negative controls — no pencil-test vocabulary leak (incl. the cross-hatch
    # trap: the world IS cross-hatched, but the spec says "dry-brush / hatched")
    assert "cream paper" not in lower
    assert "graphite" not in lower
    assert "cross-hatch" not in lower
    # negative controls — no primal / ink-over-color sibling vocabulary leak
    assert "weight-varying ink" not in lower
    assert "over the color" not in lower
    # negative controls — no samurai flat-minimal vocabulary leak
    assert "outline-sparse" not in lower
    assert "negative space" not in lower


def test_fusion_routing_is_gpt_image_generation():
    """Research §4: transport RESOLVED to gpt-image (the NB2 spike NO-GO'd) — the
    registry records the honest model and invoke_image_edit dispatches it through
    Higgsfield. Final render rides the painterly-final seam (NB Pro, no consumer
    yet). Imports the constants, not raw strings."""
    from pipeline.agents.character_designer import _resolve_plate_model

    assert _resolve_plate_model(_FUSION, {}) == GPT_IMAGE
    assert _resolve_plate_model(_FUSION, {}, final=True) == NB_PRO


def test_fusion_stub_keyword_inference():
    """'fusion' (Sean's mental name for the look) added to the stub keyword
    inference — appended AFTER the legacy six + primal + nicktoon/grossout +
    samurai, so existing precedence is untouched (earlier keywords still win)."""
    from pipeline.agents.character_designer import _infer_stub_style_register

    assert _infer_stub_style_register("fusion-trashcat") == _FUSION
    # earlier keywords still win first (appended-last precedence)
    assert _infer_stub_style_register("pixel-fusion-test") == "pixel-art-8bit"
    assert _infer_stub_style_register("primal-fusion-test") == "primal-sketch-grit"
    assert (
        _infer_stub_style_register("nicktoon-fusion-test")
        == "90s-nicktoon-grossout"
    )
    assert _infer_stub_style_register("samurai-fusion-test") == "samurai-jack-s5"
    # no keyword hit still defaults to pencil
    assert _infer_stub_style_register("trashcat") == "pencil-test-colored"


def test_fusion_stub_envelope_no_pencil_coercion(tmp_path):
    """The $0 Cy stub smoke: a stub Bible for a fusion-named character carries
    the register end-to-end — never silently pencil."""
    from pipeline.agents.character_designer import CharacterDesignerNode

    char_dir = tmp_path / "characters" / "fusion-trashcat"
    char_dir.mkdir(parents=True)
    envelope = CharacterDesignerNode()._build_stub_envelope(char_dir)
    assert envelope["character_yaml"]["style_register"] == _FUSION


def test_fusion_markers_are_exact_and_do_not_collide():
    """The exact ratified marker set (Task 2) AND no overlap with any other
    register's markers."""
    from pipeline.registers import REGISTRY

    spec = get_register(_FUSION)
    assert spec.markers == frozenset({
        "flat-cast-painted-world",
        "boiling hand-inked cast outline",
        "flat cel cast no rendered volume",
        "hand-painted gritty storybook world",
        "two-media split",
        "muted earthy ochre-brick-sage-cream",
    })
    for name, other in REGISTRY.items():
        if name == _FUSION:
            continue
        overlap = spec.markers & other.markers
        assert not overlap, f"marker collision with {name}: {sorted(overlap)}"


def test_fusion_spec_is_genericized_attribute_only():
    """Research §7 — doubly load-bearing: no show, studio, artist, creator, or
    character name anywhere in the spec's semantic fields, markers, or stub
    keywords. The register is a school of mixed-media 2D captured by attributes.
    The slug `flat-cast-painted-world` is NOT a franchise name, so the raw
    substring scan (mirroring primal/nicktoon) is sufficient — no
    hyphen-normalization carve-out. The forbidden list is the craft lineage the
    research names as sources (which must never enter the spec)."""
    spec = get_register(_FUSION)
    scanned = (
        [spec.summary, spec.identity_lock, spec.preserve, spec.style_token]
        + list(spec.stub_keywords)
        + [m for m in spec.markers if m != _FUSION]
    )
    joined = " ".join(scanned).lower()
    forbidden = (
        "cartoon saloon",
        "wolfwalkers",
        "song of the sea",
        "secret of kells",
        "hey arnold",
        "ed edd",
        "over the garden wall",
        "gumball",
        "plympton",
        "hilda",
        "ezra jack keats",
        "mary blair",
        "tomm moore",
        "eyvind earle",
        "tartakovsky",
    )
    for name in forbidden:
        assert name not in joined, f"franchise identifier {name!r} leaked into the spec"


def test_fusion_transport_is_wired_via_higgsfield(tmp_path, monkeypatch):
    """Research §4: the spec records the honest generation model (gpt-image-2),
    which is not a google-genai model but is mapped to Higgsfield."""
    from pipeline.agents.higgsfield_runner import HIGGSFIELD_IMAGE_MODELS
    from pipeline.agents.nb_pro_runner import SUPPORTED_IMAGE_MODELS, invoke_image_edit

    spec = get_register(_FUSION)
    assert spec.generation_model == GPT_IMAGE
    assert GPT_IMAGE not in SUPPORTED_IMAGE_MODELS
    assert GPT_IMAGE in HIGGSFIELD_IMAGE_MODELS

    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    resp = invoke_image_edit(
        prompt="flat-cast-painted-world plate",
        reference_images=[],
        output_path=tmp_path / "out.png",
        cache_dir=tmp_path,
        model=spec.generation_model,
    )
    assert resp.ok and resp.stub_fallback
