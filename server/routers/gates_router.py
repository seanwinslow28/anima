"""Slice 5 — the POST gate endpoints over the Slice-4 job layer.

Each endpoint is one submit() call: resolve the run (404), load its state
(422), advisory stage precheck (409), then reserve-and-dispatch (409 if the run
is busy, else 202 {job_id}). The router owns HTTP; server/gates.py owns the pure
gate map + precheck (mirroring runs_router over artifacts.py). The daemon NEVER
writes run-state — the CLI subprocess the worker drives is the sole writer.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from pipeline.orchestration import state as st
from server.gates import (GATE_SPECS, StageMismatch, approve_frame_args,
                          require_stage, retry_frame_args)
from server.jobs import RunBusyError
from server.runs import resolve_run_dir

router = APIRouter(prefix="/runs", tags=["gates"])


class RetryBody(BaseModel):
    """The retry ladder's correction note — required and non-empty (the CLI
    returns rc 2 without it). A missing field is a Pydantic 422; an
    empty/whitespace value is caught in the handler (also 422)."""

    note: str


def _resolve_and_load(run_id: str, request: Request) -> tuple:
    """resolve_run_dir -> 404, load_state -> 422 (the runs_router idiom)."""
    run_dir = resolve_run_dir(request.app.state.settings.runs_root, run_id)
    if run_dir is None:
        raise HTTPException(status_code=404, detail=f"no run {run_id!r}")
    try:
        return run_dir, st.load_state(run_dir)
    except st.StateError as e:
        raise HTTPException(status_code=422, detail=str(e))


def _require_stage_or_409(state: dict, expected: str) -> None:
    try:
        require_stage(state, expected)
    except StageMismatch as e:
        raise HTTPException(status_code=409, detail=str(e))


def _submit_or_409(request: Request, run_dir, action_args: list[str]) -> dict:
    """Reserve the run's single-writer slot and dispatch. A run already holding
    a job -> 409 + the active job_id (submit()'s atomic guard); else 202-time
    {job_id}. This is the authoritative single-writer guard; the stage precheck
    above is advisory only."""
    try:
        job = request.app.state.jobs.submit(run_dir, list(action_args))
    except RunBusyError as e:
        raise HTTPException(status_code=409,
                            detail={"active_job_id": e.active_job_id,
                                    "reason": "a job already owns this run"})
    return {"job_id": job.job_id}


def _run_gate(run_id: str, request: Request,
              expected_stage: str, action_args: list[str]) -> dict:
    run_dir, state = _resolve_and_load(run_id, request)
    _require_stage_or_409(state, expected_stage)
    return _submit_or_409(request, run_dir, action_args)


# -- the four static approves + assemble (fully-fixed action-args) -----------


@router.post("/{run_id}/plan/approve", status_code=202)
def approve_plan(run_id: str, request: Request) -> dict:
    stage, args = GATE_SPECS["plan"]
    return _run_gate(run_id, request, stage, args)


@router.post("/{run_id}/script/approve", status_code=202)
def approve_script(run_id: str, request: Request) -> dict:
    stage, args = GATE_SPECS["script"]
    return _run_gate(run_id, request, stage, args)


@router.post("/{run_id}/storyboard/approve", status_code=202)
def approve_storyboard(run_id: str, request: Request) -> dict:
    stage, args = GATE_SPECS["storyboard"]
    return _run_gate(run_id, request, stage, args)


@router.post("/{run_id}/animatic/approve", status_code=202)
def approve_animatic(run_id: str, request: Request) -> dict:
    stage, args = GATE_SPECS["animatic"]
    return _run_gate(run_id, request, stage, args)


@router.post("/{run_id}/assemble", status_code=202)
def assemble(run_id: str, request: Request) -> dict:
    stage, args = GATE_SPECS["assemble"]
    return _run_gate(run_id, request, stage, args)


# -- the two GENERATE-stage frame gates (parameterized action-args) ----------


@router.post("/{run_id}/frames/{n}/approve", status_code=202)
def approve_frame(run_id: str, n: int, request: Request,
                  attempt: int | None = None) -> dict:
    return _run_gate(run_id, request, "GENERATE", approve_frame_args(n, attempt))


@router.post("/{run_id}/frames/{n}/retry", status_code=202)
def retry_frame(run_id: str, n: int, body: RetryBody, request: Request) -> dict:
    run_dir, state = _resolve_and_load(run_id, request)
    _require_stage_or_409(state, "GENERATE")  # stage before the note check
    if not body.note.strip():
        raise HTTPException(status_code=422,
                            detail="retry requires a non-empty note")
    return _submit_or_409(request, run_dir, retry_frame_args(n, body.note))
