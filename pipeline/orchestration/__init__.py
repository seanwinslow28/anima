"""Orchestration helpers for `python -m pipeline.run` (Slice 2).

The run orchestrator is a resumable stage machine over the existing nodes:
PLAN (Maya) -> GENERATE (per-frame Flo -> T1 -> Em fan, human eye gates) ->
ASSEMBLE -> DONE. State lives in runs/<id>/run_state.json; every invocation
reads state, advances to the next gate, prints, and exits. The prototypes
these helpers generalize: scripts/author_plan.py + scripts/spark_frame.py.
"""
