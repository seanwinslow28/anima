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


def test_load_shots_chain_from_round_trips_when_valid(tmp_path):
    data = default_shots()
    data["frames"][1]["chain_from"] = 1  # frame 2 chains off frame 1 (the loop anchor)
    sl = load_shots(_write(tmp_path, data), known_namespaces=KNOWN)
    assert sl.frames[0].chain_from is None
    assert sl.frames[1].chain_from == 1


def test_load_shots_chain_from_absent_defaults_none(tmp_path):
    sl = load_shots(_write(tmp_path, default_shots()), known_namespaces=KNOWN)
    assert all(f.chain_from is None for f in sl.frames)


def test_load_shots_chain_from_must_name_an_earlier_in_sheet_frame(tmp_path):
    # >= id (cannot chain off itself or a later frame)
    data = default_shots()
    data["frames"][1]["chain_from"] = 2
    with pytest.raises(ValueError, match="chain_from"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)

    # earlier-by-value but absent from the sheet (ids are 1, 2 — no frame 5; and
    # forward-reference 99 on frame 1)
    data = default_shots()
    data["frames"][0]["chain_from"] = 99
    with pytest.raises(ValueError, match="chain_from"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)

    # wrong type
    data = default_shots()
    data["frames"][1]["chain_from"] = "1"
    with pytest.raises(ValueError, match="chain_from"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)


def test_load_shots_animatic_ref_round_trips_when_valid(tmp_path):
    data = default_shots()
    data["frames"][0]["animatic_ref"] = "animatic/F01.png"  # placement rough path
    sl = load_shots(_write(tmp_path, data), known_namespaces=KNOWN)
    assert sl.frames[0].animatic_ref == "animatic/F01.png"
    assert sl.frames[1].animatic_ref is None


def test_load_shots_animatic_ref_absent_defaults_none(tmp_path):
    sl = load_shots(_write(tmp_path, default_shots()), known_namespaces=KNOWN)
    assert all(f.animatic_ref is None for f in sl.frames)


def test_load_shots_animatic_ref_must_be_nonempty_string_when_set(tmp_path):
    # empty / whitespace string
    data = default_shots()
    data["frames"][0]["animatic_ref"] = "  "
    with pytest.raises(ValueError, match="animatic_ref"):
        load_shots(_write(tmp_path, data), known_namespaces=KNOWN)

    # wrong type
    data = default_shots()
    data["frames"][0]["animatic_ref"] = 7
    with pytest.raises(ValueError, match="animatic_ref"):
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
