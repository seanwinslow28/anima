from __future__ import annotations

from fastapi import FastAPI

from server.config import Settings, get_settings
from server.jobs import Driver, JobRegistry, SubprocessDriver
from server.routers import jobs_router, runs_router


def create_app(settings: Settings | None = None, *,
               driver: Driver | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title="anima daemon", version="0")
    app.state.settings = settings
    # Slice 4: the job layer. Tests inject a stub driver; omitted -> the real
    # subprocess driver, byte-unchanged read behavior.
    app.state.jobs = JobRegistry(runs_root=settings.runs_root,
                                 driver=driver or SubprocessDriver())
    app.include_router(runs_router.router)
    app.include_router(jobs_router.router)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
