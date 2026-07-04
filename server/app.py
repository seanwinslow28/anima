from __future__ import annotations

from fastapi import FastAPI

from server.config import Settings, get_settings
from server.routers import runs_router


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title="anima daemon", version="0")
    app.state.settings = settings
    app.include_router(runs_router.router)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
