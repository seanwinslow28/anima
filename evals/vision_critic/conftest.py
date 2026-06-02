# evals/vision_critic/conftest.py
"""Shared fixtures + mock-verdict builder for the Em vision-critic eval.

Mirrors evals/character_designer/conftest.py. cases.yaml is the spec; this
file threads the fixtures and builds the JSON verdict envelopes the mocked
runner monkey-patches into Em's CLI/SDK wrappers.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml

CASES_PATH = Path(__file__).parent / "cases.yaml"
FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def cases() -> list[dict]:
    return yaml.safe_load(CASES_PATH.read_text(encoding="utf-8"))["cases"]


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return FIXTURES_DIR


def make_vision_verdict(
    *,
    verdict: str = "pass",
    confidence: float = 0.9,
    reasoning: str = "fixture reasoning",
    cites: list[str] | None = None,
) -> str:
    """Build an Em verdict envelope JSON string (matches em-vision-critic-context.md)."""
    return json.dumps({
        "verdict": verdict,
        "confidence": confidence,
        "reasoning": reasoning,
        "proposed_patches": [],
        "cites_criteria": cites or (["AC01"] if verdict in {"fail", "borderline"} else []),
    })


@dataclass
class _FakeCLIResponse:
    text: str
    duration_s: float = 1.0
    exit_code: int = 0
    rate_capped: bool = False
    stub_fallback: bool = False
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.rate_capped and self.error is None


@dataclass
class _FakeSDKResponse:
    text: str
    duration_s: float = 1.0
    exit_code: int = 0
    stub_fallback: bool = False
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and self.error is None


REPO_ROOT = Path(__file__).resolve().parents[2]


def eval_manifest() -> dict:
    """The real critics.t2 + criteria_sources + characters_root, so Em runs in the
    eval exactly as she ships (the parity guarantee — same select_references + same
    merged bundle as production)."""
    full = yaml.safe_load((REPO_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    return {
        "critics": full.get("critics", {}),
        "criteria_sources": full.get("criteria_sources", {}),
        "characters_root": str(REPO_ROOT / "characters"),
    }


def merged_criteria(manifest: dict):
    """Load + merge the Bibles' IR.* graphs into one CriteriaBundle."""
    from pipeline.criteria import load_all_criteria
    return load_all_criteria(manifest)
