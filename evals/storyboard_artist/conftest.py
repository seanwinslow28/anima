"""Shared pytest fixtures for the storyboard_artist (Bea) eval suite.

Mirrors evals/scriptwriter/conftest.py. cases.yaml is the spec; this threads the
fixtures the parametrized runner consumes. The suite is scaffold-stage — the
composition pairwise harness + the model bake-off are deferred (campaign items);
see README.md.
"""

from __future__ import annotations

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
