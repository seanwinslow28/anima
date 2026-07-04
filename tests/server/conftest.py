import base64

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from pathlib import Path

from fastapi.testclient import TestClient

from pipeline.orchestration import state as st
from server.app import create_app
from server.config import Settings

# A real, valid 1x1 PNG — the image endpoint serves genuine bytes, not stand-ins.
TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
    "AAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
)


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


@pytest.fixture
def make_generate_run(runs_root, make_run):
    """A GENERATE-stage run with the Slice-3 read surface on disk: the six brief
    artifacts, one frame with two attempts (real PNGs), attempt 2 approved.

    Paths are recorded repo-root-relative ("runs/<id>/…"), exactly as
    pipeline.run writes them into real run-states; the server resolves them
    against runs_root.parent, which here is the fixture's repo root (tmp_path).
    """
    def _make(run_id: str = "2026-07-04-gen-run"):
        run_dir, s = make_run(run_id)
        rel = f"runs/{run_id}"

        brief = run_dir / "brief"
        brief.mkdir()
        (brief / "plan.md").write_text("# The Plan\n\nOne frame, one loop.\n", encoding="utf-8")
        (brief / "00_studio_brief.md").write_text("# Studio Brief\n", encoding="utf-8")
        (brief / "script.md").write_text("# Script\n", encoding="utf-8")
        (brief / "beats.json").write_text('{"slug": "DEMO", "beats": []}', encoding="utf-8")
        (brief / "storyboard.md").write_text("# Storyboard\n", encoding="utf-8")
        (brief / "shots.yaml").write_text("frames: []\n", encoding="utf-8")

        cand = run_dir / "candidates" / "F01"
        cand.mkdir(parents=True)
        (cand / "attempt_01.png").write_bytes(TINY_PNG)
        (cand / "attempt_02.png").write_bytes(TINY_PNG)
        approved = run_dir / "approved"
        approved.mkdir()
        (approved / "DEMO_F01_key.png").write_bytes(TINY_PNG)

        s["brief_dir"] = f"{rel}/brief"
        s["plan"]["status"] = "approved"
        s["plan"]["plan_path"] = f"{rel}/brief/plan.md"
        s["stage"] = "GENERATE"
        s["frame_order"] = [1]
        s["frames"]["1"] = {
            "status": "approved",
            "attempts": [
                {"index": 1, "candidate": f"{rel}/candidates/F01/attempt_01.png",
                 "note": None, "t1": {"verdict": "needs_vision_review", "fail_codes": []},
                 "em": [{"frame": "DEMO_F01", "character": "sean", "verdict": "flag",
                         "confidence": 0.8, "cites": ["IR.sean.style.line-weight"],
                         "patches": 0, "proposed_patches": [],
                         "reasoning": "line weight drifts on the arm",
                         "notes": "em@phase_5_generate frame=DEMO_F01 (gemini)"}],
                 "errored": None, "ts": "2026-07-04T00:00:00+00:00"},
                {"index": 2, "candidate": f"{rel}/candidates/F01/attempt_02.png",
                 "note": "hold the line weight from the anchor",
                 "t1": {"verdict": "needs_vision_review", "fail_codes": []},
                 "em": [{"frame": "DEMO_F01", "character": "sean", "verdict": "pass",
                         "confidence": 1.0, "cites": [], "patches": 0,
                         "proposed_patches": [], "reasoning": "Ship.",
                         "notes": "em@phase_5_generate frame=DEMO_F01 (gemini)"}],
                 "errored": None, "ts": "2026-07-04T00:05:00+00:00"},
            ],
            "approved_attempt": 2,
            "approved_path": f"{rel}/approved/DEMO_F01_key.png",
        }
        st.save_state(run_dir, s)
        return run_dir, s
    return _make
