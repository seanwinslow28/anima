from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from pipeline.orchestration import state as st
from server.runs import resolve_run_dir
from server.state_view import status_view

router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("/{run_id}")
def get_run(run_id: str, request: Request) -> dict:
    run_dir = resolve_run_dir(request.app.state.settings.runs_root, run_id)
    if run_dir is None:
        raise HTTPException(status_code=404, detail=f"no run {run_id!r}")
    try:
        # Raw passthrough — the projector never runs, so no KeyError guard needed.
        return st.load_state(run_dir)
    except st.StateError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/{run_id}/status")
def get_status(run_id: str, request: Request) -> dict:
    run_dir = resolve_run_dir(request.app.state.settings.runs_root, run_id)
    if run_dir is None:
        raise HTTPException(status_code=404, detail=f"no run {run_id!r}")
    try:
        state = st.load_state(run_dir)
        return status_view(state)
    except st.StateError as e:
        # missing file / unparseable JSON / bad schema_version
        raise HTTPException(status_code=422, detail=str(e))
    except (KeyError, TypeError) as e:
        # load_state does NOT validate object shape (state.py:89-104); a parseable
        # but malformed state makes the projector raise. Map to 422, not 500.
        raise HTTPException(status_code=422, detail=f"malformed run_state.json: {e}")
