"""Flo — the Phase 5 generation router.

Today the pipeline generates every frame with one model (NB2) at a flat cost
(pipeline/nodes/frame_generate.py wraps the legacy generate_frame()). Flo makes
generation **cost-routed + quality-tiered**: it consults manifest.yaml's
`generation.routing:` block per shot to pick the right generator — hero
keyframes to NB Pro, standard keyframes to NB2, in-between cleanups to the
cheap-edit tiers — and feeds Maya an accurate Phase-0 cost preview.

Flo-A (this build) is the $0 skeleton: the already-wired NB Pro (hero) / NB2
(standard) transports dispatch live; the fal.ai/GPT in-between + mask-edit tiers
are **declared seams** — config exists, transport NOT wired, so Flo raises a
clear RouteNotWiredError rather than silently mis-generating (the T2/T3
cosmetic-honesty lesson). Flo-B wires the in-between pilot.

Build plan: docs/2026-06-10-flo-router-build-plan.md. Routing table:
docs/Image-Model-DR-2026/SYNTHESIS.md §2.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pipeline import generate as _legacy_generate
from pipeline.agents import (
    AgentContext,
    AgentResult,
    CostEstimate,
    register_node,
)
from pipeline.agents.nb_pro_runner import invoke_image_edit

# The shot type assumed when a frame spec carries no explicit `shot_type`.
DEFAULT_SHOT_TYPE = "standard_keyframe"
# Transports Flo-A actually dispatches. Everything else in the routing table is
# a declared/deferred seam that raises RouteNotWiredError until Flo-B wires it.
_WIRED_TRANSPORTS = frozenset({"nb_pro", "nb2"})


class RouteNotWiredError(RuntimeError):
    """Raised when Flo resolves a route whose transport isn't wired yet.

    A declared/deferred route (fal_seedream, fal_qwen, gpt_image_2) is honest
    config, not a live generator. Flo refuses to silently mis-generate — it
    fails loudly so the caller knows the route awaits Flo-B.
    """


@dataclass(frozen=True)
class Route:
    """A resolved generation route for one shot.

    transport: the wired backend key (nb_pro | nb2) or a declared seam
               (fal_seedream | fal_qwen | gpt_image_2).
    model: the model slug to pass the transport (None for seams that don't pin
           one yet).
    usd_per_frame: the route's config price — feeds Maya's cost preview.
    tier: draft | pro — the route's declared tier.
    status: wired | declared | deferred — cosmetic-honest wiring state.
    shot_type: the route table key resolved to (after any draft→pro escalation).
    style_register: threaded through from the character for provenance + future
                    per-register routing (today all registers share a route).
    """
    transport: str
    model: str | None
    usd_per_frame: float
    tier: str | None
    status: str
    shot_type: str
    style_register: str | None = None


def resolve_route(
    shot: dict[str, Any],
    manifest: dict,
    character: dict | None = None,
) -> Route | None:
    """Map {shot_type, tier, style_register} → a Route.

    Returns None when the manifest carries no `generation.routing:` block — the
    back-compat signal that tells FloNode to fall through to the legacy
    single-model path (pencil-test reference runs must not break).

    Draft→pro escalation (build-plan A2 "standard→hero"): a `standard_keyframe`
    shot resolved at `tier=pro` escalates to the `hero_keyframe` route. At draft
    it stays standard. Hero / in-between / mask shots resolve to their own entry
    regardless of tier.
    """
    routing = (manifest.get("generation") or {}).get("routing") or {}
    if not routing:
        return None

    shot_type = shot.get("shot_type") or DEFAULT_SHOT_TYPE
    tier = shot.get("tier")

    # Draft→pro escalation: a standard keyframe asked for at pro tier escalates
    # to the hero route.
    if shot_type == "standard_keyframe" and tier == "pro":
        shot_type = "hero_keyframe"

    entry = routing.get(shot_type)
    if entry is None:
        raise ValueError(
            f"Flo: unknown shot_type {shot_type!r} — not in generation.routing "
            f"(have: {sorted(routing)})."
        )

    style_register = (character or {}).get("style_register")
    return Route(
        transport=str(entry["transport"]),
        model=entry.get("model"),
        usd_per_frame=float(entry.get("usd_per_frame", 0.0)),
        tier=entry.get("tier"),
        status=str(entry.get("status", "declared")),
        shot_type=shot_type,
        style_register=style_register,
    )


@register_node("flo")
class FloNode:
    """Phase 5 generation router. Resolves a route per shot and dispatches it."""

    name = "flo"
    inputs: dict = {
        "frame_num": int,
        "prompt": str,
        "references": list,
        # optional: "shot_type": str (default standard_keyframe),
        #           "character_id": str (looks up style_register)
    }
    outputs: dict = {
        "candidate_path": str,
    }
    cites_criteria: list[str] = []  # routing decides the generator, not criteria

    def _resolve(self, ctx: AgentContext) -> Route | None:
        shot = {
            "shot_type": ctx.inputs.get("shot_type", DEFAULT_SHOT_TYPE),
            "tier": ctx.tier,
        }
        character = None
        cid = ctx.inputs.get("character_id")
        if cid:
            character = (ctx.manifest.get("characters") or {}).get(cid)
        return resolve_route(shot, ctx.manifest, character)

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        route = self._resolve(ctx)
        if route is None:
            # Legacy single-model fall-through — same flat NB2 estimate the
            # frame_generate node carries.
            return CostEstimate(usd=0.067, latency_s=15.0, confidence=0.6)
        # Declared/deferred routes price at config estimate but with lowered
        # confidence — the real cost is unproven until Flo-B measures it.
        confidence = 0.7 if route.status == "wired" else 0.3
        latency = 25.0 if route.tier == "pro" else 15.0
        return CostEstimate(usd=route.usd_per_frame, latency_s=latency, confidence=confidence)

    def run(self, ctx: AgentContext) -> AgentResult:
        frame_num = int(ctx.inputs["frame_num"])
        prompt = str(ctx.inputs["prompt"])
        references = [str(r) for r in ctx.inputs.get("references", [])]

        route = self._resolve(ctx)

        # Back-compat: no routing block → legacy single-model path unchanged.
        if route is None:
            candidate = _legacy_generate.generate_frame(
                frame_num=frame_num,
                prompt=prompt,
                references=references,
                manifest=ctx.manifest,
                run_dir=ctx.run_dir,
            )
            if candidate is None:
                raise RuntimeError(f"flo F{frame_num:02d} legacy path returned no candidate")
            return AgentResult(
                outputs={"candidate_path": str(candidate)},
                tier=ctx.tier,
                notes=f"F{frame_num:02d} legacy single-model fall-through (no generation.routing block)",
            )

        if route.transport not in _WIRED_TRANSPORTS:
            raise RouteNotWiredError(
                f"Flo route {route.shot_type!r} declared (transport={route.transport}, "
                f"status={route.status}) but the transport is not wired — wire it in "
                f"Flo-B before routing to it."
            )

        if route.transport == "nb2":
            candidate = _legacy_generate.generate_frame(
                frame_num=frame_num,
                prompt=prompt,
                references=references,
                manifest=ctx.manifest,
                run_dir=ctx.run_dir,
            )
            if candidate is None:
                raise RuntimeError(f"flo F{frame_num:02d} nb2 route returned no candidate")
            candidate_path = Path(candidate)
        else:  # nb_pro
            candidates_dir = ctx.run_dir / "candidates" / f"F{frame_num:02d}"
            candidates_dir.mkdir(parents=True, exist_ok=True)
            attempt = _legacy_generate.get_attempt_number(candidates_dir)
            output_path = candidates_dir / f"attempt_{attempt:02d}.png"
            resp = invoke_image_edit(
                prompt=prompt,
                reference_images=[Path(r) for r in references],
                output_path=output_path,
                cache_dir=ctx.cache_dir / "flo",
                model=route.model or "gemini-3-pro-image-preview",
            )
            if not resp.ok:
                raise RuntimeError(
                    f"flo F{frame_num:02d} nb_pro route failed (exit_code={resp.exit_code})"
                )
            candidate_path = Path(resp.output_path)

        return AgentResult(
            outputs={"candidate_path": str(candidate_path)},
            tier=ctx.tier,
            notes=(
                f"F{frame_num:02d} routed → {route.transport} "
                f"({route.shot_type}, tier={route.tier}, ${route.usd_per_frame:g}/frame, "
                f"status={route.status})"
            ),
        )
