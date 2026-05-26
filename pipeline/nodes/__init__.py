"""Imports every node module so @register_node side-effects populate
NODE_REGISTRY. The DAG runner relies on this at import time."""

from pipeline.nodes import (  # noqa: F401
    assemble,
    audit_gate,
    frame_generate,
    seedance_motion,
)
