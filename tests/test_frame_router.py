"""Flo — the Phase 5 generation router. Tests for frame_router.resolve_route +
FloNode dispatch.

Flo-A is the $0 skeleton: wire the already-available NB Pro (hero) / NB2
(standard) transports, declare the fal.ai/GPT in-between tiers as honest
not-wired seams, and preserve the legacy single-model fall-through when no
`generation.routing:` block is present.

These tests run CI-green with no credentials:
  - the nb_pro route exercises invoke_image_edit's stub fallback (no
    GEMINI_API_KEY → placeholder PNG, ok=True);
  - the nb2 route + back-compat path monkeypatch the legacy generate_frame
    subprocess boundary (it shells to the Gemini skill script — unavoidable
    external dependency).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline import generate as legacy_generate
from pipeline.agents import AgentContext, AgentResult, NODE_REGISTRY
from pipeline.agents.frame_router import (
    Route,
    RouteNotWiredError,
    resolve_route,
)

# Importing pipeline.nodes fires the @register_node side effects (incl. flo).
import pipeline.nodes  # noqa: F401,E402


# --------------------------------------------------------------------------- #
# Fixtures / helpers
# --------------------------------------------------------------------------- #

ROUTING_BLOCK = {
    "hero_keyframe": {
        "transport": "nb_pro",
        "model": "gemini-3-pro-image-preview",
        "usd_per_frame": 0.15,
        "tier": "pro",
        "status": "wired",
    },
    "standard_keyframe": {
        "transport": "nb2",
        "model": "gemini-3.1-flash-image-preview",
        "usd_per_frame": 0.07,
        "tier": "draft",
        "status": "wired",
    },
    "in_between_cheap": {
        "transport": "fal_seedream",
        "usd_per_frame": 0.02,
        "tier": "draft",
        "status": "declared",
    },
    "mask_edit": {
        "transport": "gpt_image_2",
        "usd_per_frame": 0.21,
        "status": "deferred",
    },
}


def _manifest(*, routing=True):
    gen = {
        "model": "gemini-3.1-flash-image-preview",
        "aspect_ratio": "16:9",
        "script": "scripts/generate_image.py",
        "env_file": ".env",
    }
    if routing:
        gen["routing"] = ROUTING_BLOCK
        gen["fallback"] = "nb2"
    return {
        "generation": gen,
        "characters": {
            "sean-anchor": {
                "folder": "characters/sean-anchor/",
                "style_register": "pencil-test-colored",
            }
        },
    }


def _ctx(tmp_path, manifest, *, inputs, tier="draft"):
    return AgentContext(
        run_dir=tmp_path / "run",
        inputs=inputs,
        manifest=manifest,
        criteria=None,
        tier=tier,
        cache_dir=tmp_path / "cache",
    )


# --------------------------------------------------------------------------- #
# resolve_route
# --------------------------------------------------------------------------- #

def test_resolve_route_hero_keyframe_routes_to_nb_pro():
    route = resolve_route({"shot_type": "hero_keyframe"}, _manifest())
    assert isinstance(route, Route)
    assert route.transport == "nb_pro"
    assert route.model == "gemini-3-pro-image-preview"
    assert route.usd_per_frame == 0.15
    assert route.status == "wired"


def test_resolve_route_standard_keyframe_routes_to_nb2():
    route = resolve_route({"shot_type": "standard_keyframe"}, _manifest())
    assert route.transport == "nb2"
    assert route.usd_per_frame == 0.07


def test_resolve_route_defaults_to_standard_keyframe():
    # No shot_type on the spec → standard_keyframe (the default).
    route = resolve_route({}, _manifest())
    assert route.shot_type == "standard_keyframe"
    assert route.transport == "nb2"


def test_resolve_route_standard_at_pro_tier_escalates_to_hero():
    # Draft→pro escalation: a standard shot resolved at pro tier escalates to
    # the hero (nb_pro) route, per build-plan A2 "standard→hero".
    route = resolve_route({"shot_type": "standard_keyframe", "tier": "pro"}, _manifest())
    assert route.transport == "nb_pro"
    assert route.shot_type == "hero_keyframe"


def test_resolve_route_standard_at_draft_tier_stays_standard():
    route = resolve_route({"shot_type": "standard_keyframe", "tier": "draft"}, _manifest())
    assert route.transport == "nb2"
    assert route.shot_type == "standard_keyframe"


def test_resolve_route_returns_none_when_no_routing_block():
    # Back-compat signal: no routing block → None → FloNode falls through to
    # the legacy single-model path.
    assert resolve_route({"shot_type": "standard_keyframe"}, _manifest(routing=False)) is None


def test_resolve_route_threads_style_register():
    character = {"style_register": "pencil-test-colored"}
    route = resolve_route({"shot_type": "hero_keyframe"}, _manifest(), character)
    assert route.style_register == "pencil-test-colored"


def test_resolve_route_unknown_shot_type_raises():
    with pytest.raises(ValueError):
        resolve_route({"shot_type": "no_such_type"}, _manifest())


# --------------------------------------------------------------------------- #
# FloNode — registration + dispatch
# --------------------------------------------------------------------------- #

def test_flonode_registered_and_satisfies_agentspec():
    assert "flo" in NODE_REGISTRY
    cls = NODE_REGISTRY["flo"]
    inst = cls()
    assert inst.name == "flo"
    assert "candidate_path" in inst.outputs


def test_flonode_dispatches_nb_pro_hero(tmp_path):
    # nb_pro route runs invoke_image_edit's stub fallback (no key) → placeholder.
    cls = NODE_REGISTRY["flo"]
    ctx = _ctx(
        tmp_path,
        _manifest(),
        inputs={"frame_num": 6, "prompt": "hero pose", "references": [], "shot_type": "hero_keyframe"},
        tier="pro",
    )
    result = cls().run(ctx)
    assert isinstance(result, AgentResult)
    candidate = Path(result.outputs["candidate_path"])
    assert candidate.exists()
    assert "nb_pro" in result.notes


def test_flonode_dispatches_nb2_standard(tmp_path, monkeypatch):
    # nb2 route reuses the legacy generate_frame() path (subprocess boundary
    # monkeypatched).
    calls = {}

    def fake_generate_frame(*, frame_num, prompt, references, manifest, run_dir):
        calls["hit"] = True
        out = Path(run_dir) / "candidates" / f"F{frame_num:02d}" / "attempt_01.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(b"png")
        return out

    monkeypatch.setattr(legacy_generate, "generate_frame", fake_generate_frame)
    cls = NODE_REGISTRY["flo"]
    ctx = _ctx(
        tmp_path,
        _manifest(),
        inputs={"frame_num": 10, "prompt": "idle", "references": [], "shot_type": "standard_keyframe"},
    )
    result = cls().run(ctx)
    assert calls.get("hit") is True
    assert Path(result.outputs["candidate_path"]).exists()
    assert "nb2" in result.notes


def test_flonode_declared_route_raises_not_wired(tmp_path):
    cls = NODE_REGISTRY["flo"]
    ctx = _ctx(
        tmp_path,
        _manifest(),
        inputs={"frame_num": 12, "prompt": "tween", "references": [], "shot_type": "in_between_cheap"},
    )
    with pytest.raises(RouteNotWiredError) as exc:
        cls().run(ctx)
    assert "fal_seedream" in str(exc.value)
    assert "not wired" in str(exc.value).lower()


def test_flonode_backcompat_fallthrough_no_routing_block(tmp_path, monkeypatch):
    # No routing block → legacy single-model generate_frame path, unchanged.
    def fake_generate_frame(*, frame_num, prompt, references, manifest, run_dir):
        out = Path(run_dir) / "candidates" / f"F{frame_num:02d}" / "attempt_01.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(b"png")
        return out

    monkeypatch.setattr(legacy_generate, "generate_frame", fake_generate_frame)
    cls = NODE_REGISTRY["flo"]
    ctx = _ctx(
        tmp_path,
        _manifest(routing=False),
        inputs={"frame_num": 6, "prompt": "idle", "references": []},
    )
    result = cls().run(ctx)
    assert Path(result.outputs["candidate_path"]).exists()
    assert "legacy" in result.notes.lower()


def test_flonode_draft_to_pro_escalates_dispatch_to_nb_pro(tmp_path):
    # A standard shot run at pro tier escalates to the nb_pro (hero) route.
    cls = NODE_REGISTRY["flo"]
    ctx = _ctx(
        tmp_path,
        _manifest(),
        inputs={"frame_num": 6, "prompt": "idle", "references": [], "shot_type": "standard_keyframe"},
        tier="pro",
    )
    result = cls().run(ctx)
    assert Path(result.outputs["candidate_path"]).exists()
    assert "nb_pro" in result.notes


def test_flonode_cost_estimate_prices_route(tmp_path):
    cls = NODE_REGISTRY["flo"]
    # hero shot → hero price.
    ctx = _ctx(
        tmp_path, _manifest(),
        inputs={"frame_num": 6, "prompt": "x", "references": [], "shot_type": "hero_keyframe"},
        tier="pro",
    )
    est = cls().cost_estimate(ctx)
    assert est.usd == 0.15
    # declared route → lowered confidence.
    ctx2 = _ctx(
        tmp_path, _manifest(),
        inputs={"frame_num": 6, "prompt": "x", "references": [], "shot_type": "in_between_cheap"},
    )
    est2 = cls().cost_estimate(ctx2)
    assert est2.confidence < est.confidence
