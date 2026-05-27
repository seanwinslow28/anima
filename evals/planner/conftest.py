"""Shared pytest fixtures for the planner eval suite.

Mirrors the v2 change-map §7 pattern. Cases.yaml is the spec; this file
threads the fixtures every parametrized test consumes.
"""

from __future__ import annotations

import json
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


def make_planning_envelope(criteria_categories: list[str], revised: bool = False) -> str:
    """Build a planning-envelope JSON string with criteria from the named categories.

    Used by runner.py to construct mock SDK responses without hardcoding a giant
    fixture per case. Each category gets one criterion in a closed pattern.
    """
    plan_label = "Plan (revised)" if revised else "Plan"
    criteria = []
    for cat in criteria_categories:
        criteria.append({
            "id": f"AC.{cat}.fixture-{cat}",
            "description": f"Fixture criterion in category {cat}.",
            "cites_phase": [5],
            "cites_personas": ["em"] if cat != "technical" else [],
            "impact_tag": _impact_tag_for_category(cat),
            "parent_id": None,
            "derived_from": [f"studio_brief.{cat}"],
        })
    payload = {
        "production_brief_md": (
            "---\npiece_id: \"eval-fixture\"\nphases_enabled: [0, 5, 6, 8]\n---\n\n"
            "# Production Brief\n\nFixture production brief.\n"
        ),
        "criteria_json": {
            "version": "1.1",
            "locked": False,
            "criteria": criteria,
        },
        "plan_md": (
            f"# {plan_label}\n\n## Cost preview\n\nFixture cost preview.\n\n"
            f"## Phases\n\nPhases enabled: 0, 5, 6, 8.\n"
        ),
    }
    return "```json\n" + json.dumps(payload) + "\n```"


def _impact_tag_for_category(cat: str) -> str:
    return {
        "identity": "identity_critical",
        "proportion": "identity_critical",
        "continuity": "continuity",
        "timing": "aesthetic",
        "tone": "aesthetic",
        "structural": "structural",
        "technical": "technical",
    }.get(cat, "structural")


def make_sonnet_response(kind: str, flag_text: str = "") -> str:
    """Build a Sonnet adversarial envelope JSON string."""
    if kind == "clean":
        return json.dumps({"flag": None, "low_signal": False})
    if kind == "low_signal":
        return json.dumps({"flag": None, "low_signal": True})
    if kind == "flag":
        return json.dumps({"flag": flag_text})
    raise ValueError(f"Unknown sonnet response kind: {kind}")
