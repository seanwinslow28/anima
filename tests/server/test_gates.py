"""Slice 5 — server/gates.py pure unit.

No FastAPI, no registry: just the gate->(required-stage, action-args) map, the
advisory stage precheck, and the frame arg builders. The load-bearing invariant
is fleet-ops §1: NO action-arg list may ever carry --allow-api-key, so an
API-billed daemon job is impossible, not merely defaulted-off.
"""

import pytest

pytest.importorskip("fastapi")  # server-suite discipline; gates.py itself is pure

from server.gates import (GATE_SPECS, StageMismatch, approve_frame_args,
                          require_stage, retry_frame_args)


def test_require_stage_passes_on_match():
    assert require_stage({"stage": "PLAN"}, "PLAN") is None


def test_require_stage_raises_stage_mismatch_with_both_sides():
    with pytest.raises(StageMismatch) as excinfo:
        require_stage({"stage": "GENERATE"}, "PLAN")
    assert excinfo.value.expected == "PLAN"
    assert excinfo.value.actual == "GENERATE"


def test_require_stage_treats_missing_stage_as_mismatch_not_keyerror():
    # A malformed-but-loadable state must never 500 the gate — a missing stage
    # is just an advisory conflict (actual = None).
    with pytest.raises(StageMismatch) as excinfo:
        require_stage({}, "PLAN")
    assert excinfo.value.actual is None


def test_gate_specs_are_the_five_static_gates_verbatim():
    assert GATE_SPECS == {
        "plan": ("PLAN", ["--approve-plan"]),
        "script": ("SCRIPT", ["--approve-script"]),
        "storyboard": ("STORYBOARD", ["--approve-storyboard"]),
        "animatic": ("ANIMATIC", ["--approve-animatic"]),
        "assemble": ("ASSEMBLE", ["--assemble"]),
    }


def test_approve_frame_args_without_attempt():
    assert approve_frame_args(3) == ["--approve-frame", "3"]


def test_approve_frame_args_appends_attempt_only_when_given():
    assert approve_frame_args(3, 2) == ["--approve-frame", "3", "--attempt", "2"]
    assert approve_frame_args(3, None) == ["--approve-frame", "3"]


def test_retry_frame_args_carry_the_required_note():
    assert retry_frame_args(3, "hold the line weight") == [
        "--retry-frame", "3", "--note", "hold the line weight"]


def test_no_gate_action_args_ever_carry_allow_api_key():
    # fleet-ops §1 — the driver never gets a chance to bill the API.
    for _stage, action_args in GATE_SPECS.values():
        assert "--allow-api-key" not in action_args
    assert "--allow-api-key" not in approve_frame_args(1, 1)
    assert "--allow-api-key" not in retry_frame_args(1, "note")
