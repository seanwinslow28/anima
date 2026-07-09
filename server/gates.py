"""Slice 5 — the pure gate layer under the POST endpoints.

The seven human gates map to `python -m pipeline.run --resume <run_dir> <action>`
invocations. This module owns the FIXED gate->(required-stage, action-args) map,
the advisory stage precheck, and the frame arg builders — no FastAPI, no HTTP.
The router (server/routers/gates_router.py) turns StageMismatch into a 409 and
RunBusyError (from submit) into a 409 + active_job_id.

Two load-bearing disciplines, both mirrored from run.py's own guards:
  * The gate NAME is never interpolated into action_args — only the fixed
    literals below reach the CLI (artifacts.py's fixed-map-is-the-guard).
  * NO action-arg list ever carries --allow-api-key, so pipeline.run's
    _api_key_guard makes an API-billed daemon job impossible (fleet-ops §1).

The stage precheck is ADVISORY: it can go stale before the worker spawns, and
the CLI's own stage/sub-status guard (run.py:282-321) is authoritative — a
raced gate surfaces as the job's rc 2 -> state "failed" on poll. The real
single-writer guard is submit()'s atomic slot reservation, not this precheck.
"""

from __future__ import annotations

# The five gates whose action-args are fully static: (required_stage, action_args).
# The two frame gates are parameterized (n / attempt / note) and built below.
GATE_SPECS: dict[str, tuple[str, list[str]]] = {
    "plan": ("PLAN", ["--approve-plan"]),
    "script": ("SCRIPT", ["--approve-script"]),
    "storyboard": ("STORYBOARD", ["--approve-storyboard"]),
    "animatic": ("ANIMATIC", ["--approve-animatic"]),
    "assemble": ("ASSEMBLE", ["--assemble"]),
}

# Both frame gates require the GENERATE stage (research doc Part A map).
FRAME_STAGE = "GENERATE"


class StageMismatch(Exception):
    """The run is not in the stage this gate requires — an advisory 409.

    Carries both sides so the router's 409 detail can name them; the CLI guard
    remains authoritative if the precheck raced.
    """

    def __init__(self, expected: str, actual: str | None):
        self.expected = expected
        self.actual = actual
        super().__init__(
            f"run is at stage {actual!r}, not {expected!r} (this gate's stage)")


def require_stage(state: dict, expected: str) -> None:
    """Raise StageMismatch unless state['stage'] == expected.

    Reads via .get so a malformed-but-loadable state (missing 'stage') is an
    advisory conflict (actual None), never a KeyError -> 500.
    """
    actual = state.get("stage")
    if actual != expected:
        raise StageMismatch(expected, actual)


def approve_frame_args(n: int, attempt: int | None = None) -> list[str]:
    """`--approve-frame N [--attempt K]` — attempt appended only when given."""
    args = ["--approve-frame", str(n)]
    if attempt is not None:
        args += ["--attempt", str(attempt)]
    return args


def retry_frame_args(n: int, note: str) -> list[str]:
    """`--retry-frame N --note "<correction>"` — the note is required (run.py
    rc 2 without it); the caller validates it is non-empty before building."""
    return ["--retry-frame", str(n), "--note", note]
