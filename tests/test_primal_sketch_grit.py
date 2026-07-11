"""Checkpoint 2 — primal-sketch-grit: the first post-registry register.

The Tartakovsky-*Primal* register that unblocks GRANDMASTER (its live
STRESS-TEST returned `revise` because the register had no home in the
pipeline). Authored from the CORRECTED 2026-07-03 deep research
(registers/primal-sketch-grit/research.md), NOT the concept doc's craft
claims — the two load-bearing corrections:

- Primal is organic-illustrative with a heavy weight-varying ink contour
  kept OVER the color ("very new for us" — Tartakovsky), NOT flat-angular.
- Primal's blood tell is explicit shock-colored blood. The candy/oil-geyser
  substitution is SAMURAI JACK's convention; GRANDMASTER borrows it as a
  deliberate cross-register staging choice, and the register spec must not
  claim it as its own feature (guarded below).

The stub smoke here is the plan's Task 2.5: driving Cy's stub path with
this register produces a coherent stubbed Bible with NO silent pencil
coercion, $0, no keys.
"""

from __future__ import annotations

from pipeline.registers import ALL_REGISTERS, get_register

_PRIMAL = "primal-sketch-grit"


def test_primal_register_is_registered():
    assert _PRIMAL in ALL_REGISTERS
    spec = get_register(_PRIMAL)
    assert spec.name == _PRIMAL


def test_primal_plate_prompt_carries_the_register_clauses():
    """The five-slot emitter framed against Primal, not pencil: the corrected
    line rule (weight-varying ink OVER the color) is present; no pencil-test
    vocabulary leaks in (the drift direction the research flags hardest)."""
    from pipeline.agents.character_designer import _build_plate_prompt

    p = _build_plate_prompt(
        "landing in a ninja crouch, follow-through pose",
        style_register=_PRIMAL,
        has_pose_ref=False,
    )
    lower = p.lower()
    assert "weight-varying ink" in lower
    assert "over the color" in lower
    # the three negative controls: pencil-test, line-art-only, Samurai Jack
    assert "cream paper" not in lower
    assert "graphite" not in lower
    assert "cross-hatch" not in lower
    assert "uniform outline" not in lower.replace("no clean uniform outlines", "")


def test_primal_routing_is_gpt_image_generation():
    """Fork #1 (2026-07-11, Sean-ratified): the NB2 hypothesis was judged by
    the costed spike and RESOLVED to gpt-image — the registry records the
    honest model, and invoke_image_edit's UnwiredTransportError guard makes
    it fail LOUD (no gpt-image runner is wired yet) instead of silently
    falling back to Gemini/NB2. Final render still rides the painterly-final
    seam (NB Pro, no consumer yet — a documented dormant seam; fork #1
    scopes only generation_model)."""
    from pipeline.agents.character_designer import _resolve_plate_model

    assert _resolve_plate_model(_PRIMAL, {}) == "gpt-image-2"
    assert _resolve_plate_model(_PRIMAL, {}, final=True) == "gemini-3-pro-image-preview"


def test_primal_stub_keyword_inference():
    """Task 2.5: 'primal' added to the stub keyword inference — appended
    AFTER the legacy six keywords, so existing precedence is untouched."""
    from pipeline.agents.character_designer import _infer_stub_style_register

    assert _infer_stub_style_register("primal-kid") == _PRIMAL
    # legacy keywords still win first (appended-last precedence)
    assert _infer_stub_style_register("pixel-primal-test") == "pixel-art-8bit"
    # no keyword hit still defaults to pencil
    assert _infer_stub_style_register("kid") == "pencil-test-colored"


def test_primal_stub_envelope_no_pencil_coercion(tmp_path):
    """The $0 Cy stub smoke: a stub Bible for a primal-named character
    carries the register end-to-end — never silently pencil."""
    from pipeline.agents.character_designer import CharacterDesignerNode

    char_dir = tmp_path / "characters" / "primal-kid"
    char_dir.mkdir(parents=True)
    envelope = CharacterDesignerNode()._build_stub_envelope(char_dir)
    assert envelope["character_yaml"]["style_register"] == _PRIMAL


def test_primal_spec_does_not_claim_the_candy_geyser():
    """Sean's ratified correction: the candy/oil-geyser blood-substitution is
    Samurai Jack's convention — a deliberate cross-register STAGING choice in
    GRANDMASTER, never a primal-sketch-grit register feature. The spec's own
    text must not claim it."""
    spec = get_register(_PRIMAL)
    joined = " ".join(
        [spec.summary, spec.identity_lock, spec.preserve, spec.style_token]
        + list(spec.markers)
        + list(spec.stub_keywords)
    ).lower()
    assert "candy" not in joined
    assert "geyser" not in joined
    assert "oil" not in joined


def test_primal_markers_do_not_collide_with_other_registers():
    from pipeline.registers import REGISTRY

    primal_markers = get_register(_PRIMAL).markers
    for name, spec in REGISTRY.items():
        if name == _PRIMAL:
            continue
        overlap = primal_markers & spec.markers
        assert not overlap, f"marker collision with {name}: {sorted(overlap)}"
