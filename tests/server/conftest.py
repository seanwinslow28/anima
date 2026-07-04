import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from pathlib import Path

from fastapi.testclient import TestClient

from pipeline.orchestration import state as st
from server.app import create_app
from server.config import Settings


def _cast() -> list[dict]:
    return [{
        "folder_key": "sean-anchor", "ir_namespace": "sean",
        "anchor": "characters/sean-anchor/anchor.png",
        "criteria": "characters/sean-anchor/acceptance_criteria.json",
    }]


@pytest.fixture
def runs_root(tmp_path) -> Path:
    root = tmp_path / "runs"
    root.mkdir()
    return root


@pytest.fixture
def client(runs_root) -> TestClient:
    return TestClient(create_app(Settings(runs_root=runs_root)))


@pytest.fixture
def make_run(runs_root):
    """Write a real run_state.json under runs_root; return (run_dir, state)."""
    def _make(run_id: str = "2026-07-02-demo-run", **overrides):
        s = st.new_state(
            run_id=run_id, brief_dir="brief", manifest_path="manifest.yaml",
            shots_path="brief/shots.yaml", slug="DEMO", stub=True, cast=_cast(),
        )
        for k, v in overrides.items():
            s[k] = v
        run_dir = runs_root / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        st.save_state(run_dir, s)
        return run_dir, s
    return _make
