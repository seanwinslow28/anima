"""Eval-side ships-red lints for the scriptwriter suite.

These are NOT production gates — Sam's production structural pass is cast-coverage
+ sanity only (Decision #1, 2026-06-15). The by-ear voice defects (narrator-quip,
register collapse, theme-spoken, …) are the deferred pairwise-preference harness's
job. default_prop_lint is the ONE genuinely-deterministic ships-red check the voice
instrument sanctions: the literal default-prop reach (especially coffee) that reads
as a lazy scene-setting crutch.
"""

from __future__ import annotations

import re

# The chronic crutches the voice instrument calls out by name (Anti-Patterns §
# "Recycled props / default anchors — especially coffee"). Deliberately crude: a
# diegetic, premise-native mention can be legitimate — this flags the lazy default
# reach so a ships-red fixture has one deterministic catch. The by-ear judgment
# stays the pairwise harness's job.
_BANNED_DEFAULT_PROPS = ("coffee", "ferry")


def default_prop_lint(script_md: str) -> bool:
    """True if the script reaches for a banned default prop (a ships-red signal)."""
    text = script_md.lower()
    return any(re.search(rf"\b{re.escape(prop)}\b", text) for prop in _BANNED_DEFAULT_PROPS)
