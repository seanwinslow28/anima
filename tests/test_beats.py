"""Tests for pipeline/orchestration/beats.py — the Sam→Bea beat-sheet contract.

Mirrors tests/test_shots.py in spirit: the strict load_beats validator is what
makes "did Sam produce something Bea can consume" a free deterministic gate.
beats.json is machine-emitted JSON (like Maya's acceptance_criteria.json), and
carries a top-level `locked` flag that `script approve` flips — load_beats must
tolerate it so an approved file still reloads.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.orchestration.beats import Beat, BeatSheet, load_beats

# IR namespaces (the cast vocabulary load_shots/load_beats validate against —
# `sean`, not the `sean-anchor` folder key; see pipeline/orchestration/cast.py).
KNOWN = {"sean", "claude-mascot"}


def _write(tmp_path: Path, payload: dict) -> Path:
    p = tmp_path / "beats.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return p


def _valid_payload() -> dict:
    return {
        "slug": "the-spark-shared",
        "logline": "Sean draws; the mascot notices and delights; the loop returns.",
        "beats": [
            {
                "id": 1,
                "title": "Establishing two-shot",
                "intent": "Set the look, framing, and scale; the compositional anchor.",
                "emotional_beat": "calm focus",
                "cast": ["sean", "claude-mascot"],
                "feel": "establishing — let it breathe",
                "notes": "frame 5 loops back here",
            },
            {
                "id": 2,
                "title": "The draw",
                "intent": "Sean's hand moves; the mascot turns to look.",
                "emotional_beat": "first stir",
                "cast": ["sean", "claude-mascot"],
            },
        ],
    }


def test_valid_sheet_round_trips(tmp_path):
    sheet = load_beats(_write(tmp_path, _valid_payload()), known_namespaces=KNOWN)
    assert isinstance(sheet, BeatSheet)
    assert sheet.slug == "the-spark-shared"
    assert sheet.logline.startswith("Sean draws")
    assert len(sheet.beats) == 2
    assert isinstance(sheet.beats[0], Beat)
    assert sheet.beats[0].title == "Establishing two-shot"
    assert sheet.beats[0].cast == ["sean", "claude-mascot"]
    assert sheet.beats[1].feel == ""  # default
    assert sheet.beats[1].notes == ""  # default


def test_non_ascending_ids_reject(tmp_path):
    payload = _valid_payload()
    payload["beats"][1]["id"] = 1  # duplicate — not strictly ascending
    with pytest.raises(ValueError, match="ascending"):
        load_beats(_write(tmp_path, payload), known_namespaces=KNOWN)


def test_unknown_namespace_cast_rejects(tmp_path):
    payload = _valid_payload()
    payload["beats"][0]["cast"] = ["sean-anchor", "gandalf"]
    with pytest.raises(ValueError, match="unknown IR namespace"):
        load_beats(_write(tmp_path, payload), known_namespaces=KNOWN)


def test_empty_intent_rejects(tmp_path):
    payload = _valid_payload()
    payload["beats"][0]["intent"] = "   "
    with pytest.raises(ValueError, match="intent"):
        load_beats(_write(tmp_path, payload), known_namespaces=KNOWN)


def test_empty_beats_list_rejects(tmp_path):
    payload = _valid_payload()
    payload["beats"] = []
    with pytest.raises(ValueError, match="beats must be a non-empty list"):
        load_beats(_write(tmp_path, payload), known_namespaces=KNOWN)


def test_bad_slug_rejects(tmp_path):
    payload = _valid_payload()
    payload["slug"] = "not a slug!"
    with pytest.raises(ValueError, match="slug"):
        load_beats(_write(tmp_path, payload), known_namespaces=KNOWN)


def test_empty_logline_rejects(tmp_path):
    payload = _valid_payload()
    payload["logline"] = ""
    with pytest.raises(ValueError, match="logline"):
        load_beats(_write(tmp_path, payload), known_namespaces=KNOWN)


def test_locked_flag_tolerated(tmp_path):
    # `script approve` writes locked: true; an approved file must still reload.
    payload = _valid_payload()
    payload["locked"] = True
    sheet = load_beats(_write(tmp_path, payload), known_namespaces=KNOWN)
    assert len(sheet.beats) == 2


def test_unknown_top_key_rejects(tmp_path):
    payload = _valid_payload()
    payload["bogus"] = 1
    with pytest.raises(ValueError, match="unknown top-level key"):
        load_beats(_write(tmp_path, payload), known_namespaces=KNOWN)


def test_unknown_beat_key_rejects(tmp_path):
    payload = _valid_payload()
    payload["beats"][0]["camera"] = "wide"
    with pytest.raises(ValueError, match="unknown key"):
        load_beats(_write(tmp_path, payload), known_namespaces=KNOWN)


def test_empty_cast_rejects(tmp_path):
    payload = _valid_payload()
    payload["beats"][0]["cast"] = []
    with pytest.raises(ValueError, match="cast"):
        load_beats(_write(tmp_path, payload), known_namespaces=KNOWN)


def test_by_id_helper(tmp_path):
    sheet = load_beats(_write(tmp_path, _valid_payload()), known_namespaces=KNOWN)
    assert sheet.by_id(2).title == "The draw"
    with pytest.raises(KeyError):
        sheet.by_id(99)
