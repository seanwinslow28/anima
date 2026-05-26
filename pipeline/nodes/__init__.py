"""Imports every node module so @register_node side-effects populate
NODE_REGISTRY. The DAG runner relies on this at import time.

Em (the T2 vision critic) lives under pipeline/agents/, not pipeline/nodes/,
because it's an agent — not a passthrough wrapper around a legacy script.
The import side-effect is what matters: importing vision_critic fires its
@register_node("vision_critic") decorator and populates NODE_REGISTRY.
"""

from pipeline.nodes import (  # noqa: F401
    assemble,
    audit_gate,
    frame_generate,
    seedance_motion,
)
from pipeline.agents import vision_critic  # noqa: F401
