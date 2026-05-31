import json
from pathlib import Path

from pipeline.museum.motion import scrape_motion_plates


def _additions(character_dir: Path):
    spec = {"plates": [
        {"target_path": "motion_plates/idle-01.png",
         "source": "ingest:motion_plates/Idle-settle-loop.png#region:idle-01",
         "cites_identity_rules": ["IR.claude-mascot.motion.idle-breath-volume",
                                  "IR.claude-mascot.anatomy.no-arms-no-hands"]},
        {"target_path": "motion_plates/idle-02.png",
         "source": "ingest:motion_plates/Idle-settle-loop.png#region:idle-02",
         "cites_identity_rules": ["IR.claude-mascot.motion.idle-breath-volume",
                                  "IR.claude-mascot.anatomy.no-hair"]},
        {"target_path": "motion_plates/hop-01.png",
         "source": "ingest:motion_plates/Hop-side-profile.png#region:hop-01",
         "cites_identity_rules": ["IR.claude-mascot.motion.hop-arc-and-gravity"]},
    ]}
    (character_dir / "motion-additions.json").write_text(json.dumps(spec), encoding="utf-8")


def test_scrape_motion_plates_one_exhibit_per_motion(tmp_path: Path):
    cdir = tmp_path / "claude-mascot"
    cdir.mkdir()
    _additions(cdir)
    exs = scrape_motion_plates(cdir, "character-bible", "2026-05-30-mascot-motion-ingest")

    assert [e.exhibit_id for e in exs] == ["motion-idle", "motion-hop"]  # first-appearance order
    idle = exs[0]
    assert idle.kind == "motion_keys"
    assert idle.persona == "human"
    assert idle.references == ["assets/Idle-settle-loop.png"]            # the hand-drawn key sheet
    assert idle.frames == ["assets/idle-01.png", "assets/idle-02.png"]
    assert idle.output == "assets/idle-loop.gif"
    # cites are the union across the motion's plates, deduped, order-preserved
    assert idle.cites_criteria == [
        "IR.claude-mascot.motion.idle-breath-volume",
        "IR.claude-mascot.anatomy.no-arms-no-hands",
        "IR.claude-mascot.anatomy.no-hair",
    ]
    assert idle.decision.rationale_source == "source-refs/motion-direction.md"
    assert idle.decision.rationale.strip()                              # real, sourced intent text
    assert idle.evidence_completeness == "rich"
    assert any("motion-additions.json" in p for p in idle.source_paths)

    hop = exs[1]
    assert hop.frames == ["assets/hop-01.png"]
    assert hop.cites_criteria == ["IR.claude-mascot.motion.hop-arc-and-gravity"]
