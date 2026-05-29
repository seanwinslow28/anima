"""Shared pytest fixtures for the character-designer eval suite.

Mirrors evals/planner/conftest.py's pattern. cases.yaml is the spec; this
file threads the fixtures every parametrized test consumes plus the
mock-envelope builders that translate case-spec entries into the raw JSON
strings the test runner monkey-patches into the SDK + CLI wrappers.
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


def make_character_envelope(
    *,
    character_id: str,
    style_register: str = "pencil-test-colored",
    ir_count: int = 5,
    ir_categories: list[str] | None = None,
    plate_count: int = 3,
    risk_bible_md: str = "## Risk bible\n\nCy authored against the well-specified fixture; back angle extrapolated.",
    cy_confidence_notes_md: str = "## Confidence notes\n\nCy hedged on the 3-quarter back view.",
) -> str:
    """Build a Pass-1 envelope JSON string matching Cy's contract.

    The fixture is intentionally minimal: a small IR.* graph covering the
    requested categories, a plate plan with `generate` plates citing the
    rules, prose artifacts in clean markdown. Used by runner.py to mock
    invoke_opus_text without hardcoding a giant fixture per case.
    """
    if ir_categories is None:
        ir_categories = ["hair", "prop", "palette"]

    ir_entries: list[dict] = []
    handles = ["primary", "secondary", "tertiary", "quaternary", "quintenary",
               "senary", "septenary", "octonary"]
    for i in range(ir_count):
        category = ir_categories[i % len(ir_categories)]
        handle = handles[i % len(handles)]
        ir_entries.append({
            "id": f"IR.{character_id}.{category}.{handle}",
            "description": (
                f"Fixture rule for {character_id} in {category} category; "
                f"{handle} handle. Specific enough that Em can cite it."
            ),
            "cites_phase": [5, 6],
            "cites_personas": ["em"],
            "impact_tag": "identity_critical",
            "character_id": character_id,
            "derived_from": [f"characters/{character_id}/anchor.png#region:{category}"],
        })

    plates: list[dict] = []
    for i in range(plate_count):
        plates.append({
            "target_path": f"turnarounds/plate-{i + 1}.png",
            "source": "generate",
            "prompt": f"plate {i + 1} prompt for {character_id}",
            "reference_images": ["anchor.png"],
            "cites_identity_rules": [ir_entries[0]["id"]] if ir_entries else [],
        })

    envelope = {
        "character_yaml": {
            "character_id": character_id,
            "display_name": character_id.replace("-", " ").title(),
            "style_register": style_register,
            "palette": [{"name": "cream", "hex": "#FAF5E8", "role": "paper-base"}],
            "proportions": {"head_to_body": "1:7", "shoulder_to_hip": "1.2:1", "notes": ""},
            "identity_rules_pointer": "./acceptance_criteria.json",
            "cy_confidence_notes": "(see cy-confidence-notes.md)",
            "flux_lora_seed_plates": ["anchor.png"],
            "risks": "./risk-bible.md",
            "source_refs_consumed": ["source-refs/notes.md"],
        },
        "ir_entries": ir_entries,
        "risk_bible_md": risk_bible_md,
        "cy_confidence_notes_md": cy_confidence_notes_md,
        "plate_generation_plan": {"plates": plates},
    }
    return "```json\n" + json.dumps(envelope) + "\n```"


def make_gemini_verdict(
    *,
    verdict: str = "pass",
    confidence: float = 0.9,
    reasoning: str = "The plate honors the cited rules.",
    cites: list[str] | None = None,
) -> str:
    """Build a Gemini Pass-3 verdict envelope JSON string."""
    return json.dumps({
        "verdict": verdict,
        "confidence": confidence,
        "reasoning": reasoning,
        "cites_identity_rule": cites or [],
    })
