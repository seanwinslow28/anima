"""Register #2 — 90s-nicktoon-grossout: the ai-guru pilot's register.

Authored from the wire-ready research (registers/90s-nicktoon-grossout/
research.md, Sean-ratified 2026-07-04 cross-engine spike). The two
load-bearing craft corrections baked into the spec:

- THE DEFAULT IS THE APPEALING, WARM, CLEAN CEL-CARTOON HUMAN (~90% of
  frames); the hyper-rendered grotesque gross-out extreme close-up is
  SPARSE comedic punctuation (one or two beats), never the lead's resting
  state. The style_token is authored appealing-default-forward (research
  §0 — the first grotesque-forward draft produced constantly-ugly results
  Sean rejected).
- Genericization is DOUBLY load-bearing here (research §7): no show,
  artist, tool, or creator name in any clause, marker, comment, or
  example — the register is a school of grotesque cel animation,
  attribute-only.

Transport: NB2 GO (the 2026-07-04 spike) — the register stays on the
pipeline default, unlike primal-sketch-grit; NB Pro rides the
painterly-final seam.

The stub smoke mirrors primal's Task 2.5: driving Cy's stub path with a
nicktoon-named character produces a coherent stubbed Bible with NO silent
pencil coercion, $0, no keys.
"""

from __future__ import annotations

from pipeline.registers import ALL_REGISTERS, get_register

_NICKTOON = "90s-nicktoon-grossout"


def test_nicktoon_register_is_registered():
    assert _NICKTOON in ALL_REGISTERS
    spec = get_register(_NICKTOON)
    assert spec.name == _NICKTOON


def test_nicktoon_plate_prompt_carries_the_register_clauses():
    """The five-slot emitter framed against the gross-out school, not pencil:
    the corrected appealing-default + quarantined gross-up vocabulary is
    present; no pencil-test vocabulary leaks in (the pipeline-default drift
    every new register has to fence off)."""
    from pipeline.agents.character_designer import _build_plate_prompt

    p = _build_plate_prompt(
        "camera-ready showman grin, mid-gesture at the ring light",
        style_register=_NICKTOON,
        has_pose_ref=False,
    )
    lower = p.lower()
    # the register's own vocabulary
    assert "thick-and-thin" in lower
    assert "self-colored" in lower
    assert "gross-out extreme close-up" in lower
    assert "hue-turned" in lower
    # the §0 correction: appealing default forward, gross-up reserved
    assert "appealing" in lower
    assert "never the default" in lower
    # the negative controls: no pencil-test vocabulary leak
    assert "cream paper" not in lower
    assert "graphite" not in lower
    assert "cross-hatch" not in lower


def test_nicktoon_routing_is_nb2_generation():
    """§4: NB2 GO — the 2026-07-04 cross-engine spike found NB2 renders both
    poles (flat appealing base AND the gross-up ECU, best of the engines
    tested), so the register stays on the pipeline default with NO forced
    escalation (unlike primal). Final render rides the painterly-final seam
    (NB Pro, no consumer yet — same as watercolor/photoreal/3d-rendered)."""
    from pipeline.agents.character_designer import _resolve_plate_model

    assert _resolve_plate_model(_NICKTOON, {}) == "gemini-3.1-flash-image-preview"
    assert _resolve_plate_model(_NICKTOON, {}, final=True) == "gemini-3-pro-image-preview"


def test_nicktoon_stub_keyword_inference():
    """'nicktoon' + 'grossout' added to the stub keyword inference — appended
    AFTER the legacy six + primal, so existing precedence is untouched."""
    from pipeline.agents.character_designer import _infer_stub_style_register

    assert _infer_stub_style_register("nicktoon-aiden") == _NICKTOON
    assert _infer_stub_style_register("grossout-orb") == _NICKTOON
    # legacy keywords still win first (appended-last precedence)
    assert _infer_stub_style_register("pixel-nicktoon-test") == "pixel-art-8bit"
    # primal (register #7) also precedes the nicktoon keywords
    assert _infer_stub_style_register("primal-nicktoon-test") == "primal-sketch-grit"
    # no keyword hit still defaults to pencil
    assert _infer_stub_style_register("aiden") == "pencil-test-colored"


def test_nicktoon_stub_envelope_no_pencil_coercion(tmp_path):
    """The $0 Cy stub smoke: a stub Bible for a nicktoon-named character
    carries the register end-to-end — never silently pencil."""
    from pipeline.agents.character_designer import CharacterDesignerNode

    char_dir = tmp_path / "characters" / "nicktoon-aiden"
    char_dir.mkdir(parents=True)
    envelope = CharacterDesignerNode()._build_stub_envelope(char_dir)
    assert envelope["character_yaml"]["style_register"] == _NICKTOON


def test_nicktoon_style_token_is_appealing_default_forward():
    """Research §0, Sean-ratified: the style_token leads with the appealing
    warm cel-cartoon default and frames the gross-up as reserved punctuation
    ('for occasional comedy beats only', 'never the default') — the
    grotesque-forward first draft is the documented failure mode."""
    spec = get_register(_NICKTOON)
    token = spec.style_token.lower()
    assert token.index("appealing") < token.index("gross-out")
    assert "occasional comedy beats only" in token
    assert "never the default" in token


def test_nicktoon_spec_is_genericized_attribute_only():
    """Research §7 — doubly load-bearing: no show, studio, artist, or creator
    name anywhere in the spec's clauses, markers, or stub keywords. The
    register is a school of grotesque cel animation, captured by attributes.
    (Named-source negatives are also banned from `preserve` — naming a
    neighbor register's source can evoke it in the image model.)"""
    spec = get_register(_NICKTOON)
    joined = " ".join(
        [spec.summary, spec.identity_lock, spec.preserve, spec.style_token]
        + list(spec.markers)
        + list(spec.stub_keywords)
    ).lower()
    forbidden = (
        "stimpy",
        "kricfalusi",
        "spumco",
        "spümcø",
        "rugrats",
        "klasky",
        "csupo",
        "wolverton",
        "nickelodeon",
        "rocko",
        "wray",
        "fleischer",
        "clampett",
    )
    for name in forbidden:
        assert name not in joined, f"named source {name!r} leaked into the spec"


def test_nicktoon_markers_do_not_collide_with_other_registers():
    from pipeline.registers import REGISTRY

    nicktoon_markers = get_register(_NICKTOON).markers
    for name, spec in REGISTRY.items():
        if name == _NICKTOON:
            continue
        overlap = nicktoon_markers & spec.markers
        assert not overlap, f"marker collision with {name}: {sorted(overlap)}"
