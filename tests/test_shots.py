"""Schema additions for Bea (Phase 3b): per-frame `beat_id` + top-level `locked`.

Both are optional and back-compat — the shipped Spark shots.yaml (neither field)
must keep parsing (proven separately by test_run_shots.py +
test_spark_shots_equivalence.py). `beat_id` carries the beat->shot link Bea's
coverage gate reads; `locked` is the storyboard-approve curation flag. Both are
inert downstream (generate_stage / assemble_stage never read them).
"""

from __future__ import annotations

import yaml
import pytest

from pipeline.orchestration.shots import load_shots
from tests.orch_fixtures import default_shots

KNOWN = {"al", "be"}


def _write(tmp_path, data: dict):
    p = tmp_path / "shots.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    return p


def test_beat_id_absent_defaults_to_none(tmp_path):
    """Back-compat: a frame without beat_id loads with beat_id None."""
    sl = load_shots(_write(tmp_path, default_shots()), known_namespaces=KNOWN)
    assert all(f.beat_id is None for f in sl.frames)


def test_beat_id_present_round_trips(tmp_path):
    data = default_shots()
    data["frames"][0]["beat_id"] = 1
    data["frames"][1]["beat_id"] = 3
    sl = load_shots(_write(tmp_path, data), known_namespaces=KNOWN)
    assert [f.beat_id for f in sl.frames] == [1, 3]


def test_beat_id_non_int_rejects(tmp_path):
    data = default_shots()
    data["frames"][0]["beat_id"] = "two"
    with pytest.raises(ValueError, match="beat_id"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)


def test_beat_id_below_one_rejects(tmp_path):
    data = default_shots()
    data["frames"][0]["beat_id"] = 0
    with pytest.raises(ValueError, match="beat_id"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)


def test_locked_absent_defaults_false(tmp_path):
    """Back-compat: a shots.yaml without `locked` is unlocked."""
    sl = load_shots(_write(tmp_path, default_shots()), known_namespaces=KNOWN)
    assert sl.locked is False


def test_locked_true_round_trips(tmp_path):
    data = default_shots()
    data["locked"] = True
    sl = load_shots(_write(tmp_path, data), known_namespaces=KNOWN)
    assert sl.locked is True


def test_locked_non_bool_rejects(tmp_path):
    data = default_shots()
    data["locked"] = "yes"
    with pytest.raises(ValueError, match="locked"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)
