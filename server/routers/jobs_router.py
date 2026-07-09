"""Slice 4 — the /jobs read + cancel surface over the JobRegistry.

The router owns HTTP; the registry (server/jobs.py) owns the lifecycle. No
POST /runs/{id}/<gate> here — submit() is the seam Slice 5 builds those on.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from server.jobs import Job, JobRegistry

router = APIRouter(prefix="/jobs", tags=["jobs"])


def job_view(job: Job) -> dict:
    return {
        "job_id": job.job_id,
        "run_id": job.run_id,
        "state": job.state,
        "rc": job.rc,
        "logs": job.logs,
        "fresh_state": job.fresh_state,
        "load_error": job.load_error,
        "next_action": job.next_action,
    }


def _registry(request: Request) -> JobRegistry:
    return request.app.state.jobs


@router.get("/{job_id}")
def get_job(job_id: str, request: Request) -> dict:
    job = _registry(request).get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"no job {job_id!r}")
    return job_view(job)
