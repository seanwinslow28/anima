"""P1/P2 — the shots.yaml loader (the externalized spark_frame FRAMES dict).

Per frame: id / cast (IR namespaces) / beat / prompt / extra_references /
chain_anchors / hold. The human authors this (Phase 3 is human-authored);
the orchestrator never invents frame prompts.
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


def test_load_shots_defaults_hold_2_and_chain_anchors_cast(tmp_path):
    sl = load_shots(_write(tmp_path, default_shots()), known_namespaces=KNOWN)

    assert sl.slug == "TT"
    f1, f2 = sl.frames
    assert (f1.id, f1.cast, f1.hold) == (1, ["al", "be"], 2)
    assert f1.chain_anchors == ["al", "be"]  # default: all of cast
    assert f1.extra_references == []
    assert (f2.id, f2.hold) == (2, 3)
    assert f2.chain_anchors == ["al"]


def test_load_shots_duplicate_or_descending_ids_raise(tmp_path):
    data = default_shots()
    data["frames"][1]["id"] = 1
    with pytest.raises(ValueError, match="id"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)

    data = default_shots()
    data["frames"] = list(reversed(data["frames"]))
    with pytest.raises(ValueError, match="ascending"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)


def test_load_shots_unknown_cast_namespace_raises(tmp_path):
    data = default_shots()
    data["frames"][0]["cast"] = ["al", "nope"]
    with pytest.raises(ValueError, match="nope"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)


def test_load_shots_chain_anchors_must_be_subset_of_cast(tmp_path):
    data = default_shots()
    data["frames"][1]["chain_anchors"] = ["be"]  # frame 2 casts only al
    with pytest.raises(ValueError, match="chain_anchors"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)


def test_load_shots_unknown_key_raises(tmp_path):
    data = default_shots()
    data["frames"][0]["mascot_plate"] = "x.png"  # the old FRAMES key — typo guard
    with pytest.raises(ValueError, match="mascot_plate"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)

    data = default_shots()
    data["fps"] = 12
    with pytest.raises(ValueError, match="fps"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)


def test_load_shots_requires_nonempty_prompt_beat_cast_and_valid_slug(tmp_path):
    for field, value in (("prompt", ""), ("beat", ""), ("cast", [])):
        data = default_shots()
        data["frames"][0][field] = value
        with pytest.raises(ValueError, match=field):
            load_shots(_write(tmp_path, data), known_namespaces=KNOWN)

    data = default_shots()
    data["slug"] = "bad slug!"
    with pytest.raises(ValueError, match="slug"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)

    data = default_shots()
    data["frames"][0]["hold"] = 0
    with pytest.raises(ValueError, match="hold"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)
