"""P2 — golden equivalence: the spark shots.yaml IS spark_frame's FRAMES dict.

scripts/spark_frame.py stays untouched (the documented prototype + manual
escape hatch); "don't fork" is enforced here instead — the committed
briefs/2026-06-10-spark-shared/shots.yaml must carry the prototype's prompts,
beats, and plates verbatim, and the generalized resolve_references must
reproduce the prototype's exact reference recipe for every frame. This file
is also the costed-validation input ("The Spark, Shared" via the one-command
flow).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml
import pytest

from pipeline.orchestration.cast import derive_cast
from pipeline.orchestration.generate_stage import resolve_references
from pipeline.orchestration.shots import load_shots
from pipeline.orchestration import state as st
from tests.orch_fixtures import write_png

SHOTS_PATH = Path("briefs/2026-06-10-spark-shared/shots.yaml")


def _spark_frame_module():
    spec = importlib.util.spec_from_file_location("spark_frame", "scripts/spark_frame.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # module level = constants + defs only
    return mod


def _load_spark_shots():
    return load_shots(SHOTS_PATH, known_namespaces={"sean", "claude-mascot"})


def test_spark_shots_yaml_matches_frames_dict_verbatim():
    spark = _spark_frame_module()
    sl = _load_spark_shots()

    assert sl.slug == spark.SLUG == "SS"
    assert [s.id for s in sl.frames] == sorted(spark.FRAMES)
    for shot in sl.frames:
        spec = spark.FRAMES[shot.id]
        assert shot.prompt == spec["prompt"], f"F{shot.id:02d} prompt drifted"
        assert shot.beat == spec["beat"], f"F{shot.id:02d} beat drifted"
        assert shot.cast == ["sean", "claude-mascot"]  # EM_CHARS, per-frame
        assert shot.chain_anchors == ["sean"]  # spark chains SEAN_ANCHOR only
        assert shot.hold == 2
        if shot.id == 1:
            assert shot.extra_references == [str(spark.A7_PAIRING)]
        else:
            assert shot.extra_references == [str(spec["mascot_plate"])]
        # every plate the shot list names exists in the locked Bibles
        for ref in shot.extra_references:
            assert Path(ref).exists(), f"missing plate {ref}"


def test_spark_shots_resolve_references_reproduces_prototype_recipe(tmp_path):
    sl = _load_spark_shots()
    manifest = yaml.safe_load(Path("manifest.yaml").read_text(encoding="utf-8"))
    state = st.new_state(
        run_id="equiv", brief_dir="briefs/2026-06-10-spark-shared",
        manifest_path="manifest.yaml", shots_path=str(SHOTS_PATH),
        slug="SS", stub=True, cast=derive_cast(manifest),
    )
    state["frame_order"] = [s.id for s in sl.frames]
    run_dir = tmp_path / "run"
    write_png(run_dir / "approved" / "SS_F01_key.png")
    write_png(run_dir / "approved" / "SS_F02_key.png")

    # F01 — spark: [SEAN_ANCHOR, MASCOT_ANCHOR, A7_PAIRING]
    assert resolve_references(sl.by_id(1), state, run_dir) == [
        "characters/sean-anchor/anchor.png",
        "characters/claude-mascot/anchor.png",
        "characters/claude-mascot/source-refs/sean-with-claude-mascot.png",
    ]
    # F02 — spark: [F01, prior(=F01, deduped), SEAN_ANCHOR, look plate]
    assert resolve_references(sl.by_id(2), state, run_dir) == [
        str(run_dir / "approved" / "SS_F01_key.png"),
        "characters/sean-anchor/anchor.png",
        "characters/claude-mascot/motion_plates/look-01.png",
    ]
    # F03 — spark: [F01, F02, SEAN_ANCHOR, alert-perk plate]
    assert resolve_references(sl.by_id(3), state, run_dir) == [
        str(run_dir / "approved" / "SS_F01_key.png"),
        str(run_dir / "approved" / "SS_F02_key.png"),
        "characters/sean-anchor/anchor.png",
        "characters/claude-mascot/expressions/alert-perk.png",
    ]
    # F03 without F02 approved — the prototype's hard guard carries over
    (run_dir / "approved" / "SS_F02_key.png").unlink()
    with pytest.raises(FileNotFoundError, match="SS_F02_key"):
        resolve_references(sl.by_id(3), state, run_dir)
