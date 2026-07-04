from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, Response

from pipeline.orchestration import state as st
from server.artifacts import artifact_media_type, artifact_path
from server.runs import list_runs, resolve_run_dir
from server.state_view import status_view

router = APIRouter(prefix="/runs", tags=["runs"])


def _load_state_or_http_error(run_dir) -> dict:
    """load_state with the Slice 1-2 error conventions (422, never 500)."""
    try:
        return st.load_state(run_dir)
    except st.StateError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("")
def get_runs(request: Request) -> list[dict]:
    return list_runs(request.app.state.settings.runs_root)


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


@router.get("/{run_id}/artifacts/{kind}")
def get_artifact(run_id: str, kind: str, request: Request) -> Response:
    runs_root = request.app.state.settings.runs_root
    run_dir = resolve_run_dir(runs_root, run_id)
    if run_dir is None:
        raise HTTPException(status_code=404, detail=f"no run {run_id!r}")
    state = _load_state_or_http_error(run_dir)
    try:
        path = artifact_path(state, runs_root, kind)
    except (KeyError, TypeError) as e:
        raise HTTPException(status_code=422, detail=f"malformed run_state.json: {e}")
    if path is None:
        # Unknown kind AND legitimately-absent file are both 404, never 500 —
        # a back-compat run simply has no script/beats.
        raise HTTPException(status_code=404, detail=f"no artifact {kind!r} for run {run_id!r}")
    return Response(content=path.read_text(encoding="utf-8"),
                    media_type=artifact_media_type(path))


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
