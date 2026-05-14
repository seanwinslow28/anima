"""Tests for the bake-off helpers in seedance_lib.py.

These cover only the pure-function logic (variant loading + run-dir naming).
The orchestrator's API-call paths are integration-tested via the smoke run
in Task 4 and have no unit tests, matching the existing pipeline pattern.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
from seedance_lib import load_bakeoff_variants, make_bakeoff_run_dir


# --- load_bakeoff_variants ---

def test_load_bakeoff_variants_returns_dict_with_expected_keys(tmp_path):
    yaml_path = tmp_path / "v.yaml"
    yaml_path.write_text(
        "version: 1\n"
        "test_shots: [W1, S0]\n"
        "seeds: [42, 1337]\n"
        "defaults:\n"
        "  tier: fast\n"
        "  resolution: 720p\n"
        "variants:\n"
        "  - id: V00\n"
        "    name: control\n"
        "    isolates_axis: control\n"
        "    prompts:\n"
        "      W1: hello\n"
        "      S0: world\n"
    )
    data = load_bakeoff_variants(yaml_path)
    assert data["test_shots"] == ["W1", "S0"]
    assert data["seeds"] == [42, 1337]
    assert len(data["variants"]) == 1
    assert data["variants"][0]["id"] == "V00"
    assert data["variants"][0]["prompts"]["W1"] == "hello"


def test_load_bakeoff_variants_raises_on_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_bakeoff_variants(tmp_path / "missing.yaml")


def test_load_bakeoff_variants_raises_on_missing_required_key(tmp_path):
    yaml_path = tmp_path / "v.yaml"
    yaml_path.write_text("version: 1\ntest_shots: [W1]\n")  # no 'variants' key
    with pytest.raises(ValueError, match="variants"):
        load_bakeoff_variants(yaml_path)


# --- make_bakeoff_run_dir ---

def test_make_bakeoff_run_dir_creates_dir_with_date_suffix(tmp_path):
    run_dir = make_bakeoff_run_dir(base=tmp_path)
    today = datetime.now().strftime("%Y-%m-%d")
    assert run_dir.exists()
    assert run_dir.name == f"seedance-bakeoff-{today}"


def test_make_bakeoff_run_dir_is_idempotent(tmp_path):
    a = make_bakeoff_run_dir(base=tmp_path)
    b = make_bakeoff_run_dir(base=tmp_path)
    assert a == b
    assert a.exists()
