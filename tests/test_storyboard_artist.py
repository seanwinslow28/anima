"""Tests for pipeline/agents/storyboard_artist.py — Bea, the Phase-3b board artist.

Credential-free: the stub-run tests force ANIMA_FORCE_STUB so invoke_sonnet_text
returns Bea's deterministic stub envelope — no model spend, $0. The deterministic
coverage + script↔board-conflict pass is exercised directly (both are the named
red failure classes — proven by test, not asserted).

storyboard_validate's cast-consistency rule is beat.cast ⊆ shot.cast (every
character a beat is *about* must appear in its boarded shot; the board may add
others). This is the defensible direction: the real Spark board legitimately
shows BOTH sean and the mascot in shot 3 while beat 3's focal cast is just
[claude-mascot] — so the reverse rule (shot ⊆ beat) would flag the shipped board.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from pipeline.agents import AgentContext, CostEstimate, NODE_REGISTRY
import pipeline.agents.storyboard_artist  # noqa: F401 — registers "storyboard_artist"
from pipeline.agents.storyboard_artist import StoryboardArtistNode, storyboard_validate
from pipeline.orchestration.beats import Beat, BeatSheet
from pipeline.orchestration.cast import derive_cast
from pipeline.orchestration.shots import Shot, ShotList, load_shots

KNOWN = {"sean", "claude-mascot"}


def _manifest() -> dict:
    return {
        "characters": {
            "sean-anchor": {"folder": "characters/sean-anchor/", "style_register": "pencil-test-colored"},
            "claude-mascot": {"folder": "characters/claude-mascot/", "style_register": "pencil-test-colored"},
        }
    }


def _ctx(tmp_path: Path, brief_dir: Path) -> AgentContext:
    return AgentContext(
        run_dir=tmp_path,
        inputs={"brief_dir": str(brief_dir)},
        manifest=_manifest(),
        criteria=None,
        tier="draft",
        cache_dir=tmp_path / ".cache",
    )


def _beat(bid: int, cast: list[str], emo: str = "x") -> Beat:
    return Beat(id=bid, title=f"B{bid}", intent="does a thing", emotional_beat=emo, cast=cast)


def _shot(sid: int, cast: list[str], beat_id: int | None) -> Shot:
    return Shot(id=sid, cast=cast, beat="boarded", prompt="draw it", beat_id=beat_id)


def _spark_beats() -> dict:
    # The real Sam Spark beat sheet — beat 3 ("The notice") cast is mascot-only.
    return {
        "slug": "the-spark-shared",
        "logline": "Sean draws; the mascot notices and delights; it settles back.",
        "beats": [
            {"id": 1, "title": "Establishing", "intent": "set look", "emotional_beat": "calm focus",
             "cast": ["sean", "claude-mascot"]},
            {"id": 2, "title": "The draw", "intent": "hand moves", "emotional_beat": "first stir",
             "cast": ["sean", "claude-mascot"]},
            {"id": 3, "title": "The notice", "intent": "mascot perks", "emotional_beat": "spark",
             "cast": ["claude-mascot"]},
            {"id": 4, "title": "The delight", "intent": "mascot delights", "emotional_beat": "delight",
             "cast": ["sean", "claude-mascot"]},
            {"id": 5, "title": "The settle", "intent": "loop closes", "emotional_beat": "settled warmth",
             "cast": ["sean", "claude-mascot"]},
        ],
    }


def _write_brief(brief_dir: Path, *, beats: dict | None = None) -> None:
    brief_dir.mkdir(parents=True, exist_ok=True)
    (brief_dir / "00_studio_brief.md").write_text(
        "# Brief\nSean draws; the mascot notices and delights; the loop returns.\n",
        encoding="utf-8",
    )
    (brief_dir / "beats.json").write_text(
        json.dumps(beats or _spark_beats(), indent=2), encoding="utf-8"
    )


# ----- contract -----

def test_node_registered_and_contract():
    assert "storyboard_artist" in NODE_REGISTRY
    node = NODE_REGISTRY["storyboard_artist"]()
    assert isinstance(node, StoryboardArtistNode)
    assert node.name == "storyboard_artist"
    assert node.inputs == {"brief_dir": str}
    assert node.outputs == {"storyboard_path": str, "shots_path": str}
    assert node.cites_criteria == []
    est = node.cost_estimate(None)
    assert isinstance(est, CostEstimate)
    assert est.usd == 0.0


def test_missing_studio_brief_raises(tmp_path):
    brief_dir = tmp_path / "brief"
    brief_dir.mkdir()
    (brief_dir / "beats.json").write_text(json.dumps(_spark_beats()), encoding="utf-8")
    with pytest.raises(FileNotFoundError, match="Studio Brief"):
        StoryboardArtistNode().run(_ctx(tmp_path, brief_dir))


def test_missing_beats_raises(tmp_path):
    brief_dir = tmp_path / "brief"
    brief_dir.mkdir()
    (brief_dir / "00_studio_brief.md").write_text("# Brief\n", encoding="utf-8")
    with pytest.raises(FileNotFoundError, match="beats.json"):
        StoryboardArtistNode().run(_ctx(tmp_path, brief_dir))


# ----- stub authoring path (credential-free) -----

def test_stub_run_emits_storyboard_and_valid_shots(tmp_path, monkeypatch):
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    brief_dir = tmp_path / "brief"
    _write_brief(brief_dir)
    result = StoryboardArtistNode().run(_ctx(tmp_path, brief_dir))

    storyboard_path = Path(result.outputs["storyboard_path"])
    shots_path = Path(result.outputs["shots_path"])
    assert storyboard_path.exists()
    assert shots_path.exists()

    # The emitted shots.yaml round-trips through the real load_shots with the
    # real manifest's known namespaces — the Bea contract, proven.
    known = {m["ir_namespace"] for m in derive_cast(_manifest()) if m["ir_namespace"]}
    sl = load_shots(shots_path, known_namespaces=known)
    assert len(sl.frames) >= 3
    assert all(f.beat_id is not None for f in sl.frames)  # every shot beat-linked
    assert sl.locked is False  # born unlocked

    # The stub marker is present so author_storyboard.py's guard can refuse it.
    assert "STUB FALLBACK" in storyboard_path.read_text(encoding="utf-8")
    assert result.notes


def test_stub_run_dumps_raw_response(tmp_path, monkeypatch):
    """Bea dumps her raw model envelope to run_dir/bea_raw.txt (mirrors Maya's
    maya_raw_pass1.txt) — visibility for the live run; best-effort, never fatal."""
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    brief_dir = tmp_path / "brief"
    _write_brief(brief_dir)
    StoryboardArtistNode().run(_ctx(tmp_path, brief_dir))

    raw_path = tmp_path / "bea_raw.txt"  # _ctx sets run_dir=tmp_path
    assert raw_path.exists()
    assert raw_path.read_text(encoding="utf-8").strip()


def test_stub_draft_has_no_box_drawing(tmp_path, monkeypatch):
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    brief_dir = tmp_path / "brief"
    _write_brief(brief_dir)
    result = StoryboardArtistNode().run(_ctx(tmp_path, brief_dir))
    text = Path(result.outputs["storyboard_path"]).read_text(encoding="utf-8")
    text += Path(result.outputs["shots_path"]).read_text(encoding="utf-8")
    for ch in "╔═╗║╚╝┌─┐│└┘":
        assert ch not in text, f"output contains box char {ch!r}"


# ----- prompt assembly (the Sonnet authoring path wiring) -----

def test_prompt_loads_voice_instrument_and_context():
    # Guards the wiring: a renamed/dropped prompt file would silently strip the
    # voice or the action-line bank. Assert the load-bearing §8 voice samples,
    # Bea's own context, the action-line bank, and the task payload reach it.
    prompt = StoryboardArtistNode()._build_prompt(
        "STUDIO_BRIEF_BODY", "PLAN_BODY", _spark_beats(), {"sean", "claude-mascot"}
    )
    assert "§8 Voice Samples" in prompt            # shared instrument header
    assert "You are Bea" in prompt                 # Bea's role addendum
    assert "Action-Line Prose Bank" in prompt      # the vendored bank (Bea-only)
    assert "STUDIO_BRIEF_BODY" in prompt
    assert "claude-mascot" in prompt
    assert "pencil test" in prompt.lower()         # the register clause requirement


# ----- deterministic validation pass (coverage + conflict) -----

def test_validate_accepts_clean_beat_linked_sheet():
    sheet = BeatSheet(slug="t", logline="l", beats=[_beat(i, ["sean", "claude-mascot"], str(i)) for i in (1, 2, 3)])
    # Shot 3 boards both even though beat 3 here carries both — clean.
    sl = ShotList(slug="t", frames=[_shot(i, ["sean", "claude-mascot"], beat_id=i) for i in (1, 2, 3)])
    storyboard_validate(sheet, sl, known_namespaces=KNOWN)  # no raise


def test_validate_accepts_board_superset_of_beat_cast():
    # The Spark reality: beat 3 is mascot-only, but its shot boards both. Legal.
    sheet = BeatSheet(slug="t", logline="l", beats=[
        _beat(1, ["sean", "claude-mascot"], "a"),
        _beat(2, ["claude-mascot"], "b"),
        _beat(3, ["sean", "claude-mascot"], "c"),
    ])
    sl = ShotList(slug="t", frames=[_shot(i, ["sean", "claude-mascot"], beat_id=i) for i in (1, 2, 3)])
    storyboard_validate(sheet, sl, known_namespaces=KNOWN)  # no raise — board ⊇ beat


def test_validate_catches_coverage_gap():
    # Beat 2 has no shot pointing at it → coverage gap.
    sheet = BeatSheet(slug="t", logline="l", beats=[_beat(i, ["sean"], str(i)) for i in (1, 2, 3)])
    sl = ShotList(slug="t", frames=[_shot(1, ["sean"], 1), _shot(2, ["sean"], 3)])
    with pytest.raises(ValueError, match="coverage gap"):
        storyboard_validate(sheet, sl, known_namespaces={"sean"})


def test_validate_catches_orphan_shot():
    sheet = BeatSheet(slug="t", logline="l", beats=[_beat(i, ["sean"], str(i)) for i in (1, 2, 3)])
    sl = ShotList(slug="t", frames=[_shot(i, ["sean"], i) for i in (1, 2, 3)] + [_shot(4, ["sean"], 9)])
    with pytest.raises(ValueError, match="orphan"):
        storyboard_validate(sheet, sl, known_namespaces={"sean"})


def test_validate_catches_script_board_conflict():
    # Beat 3 is about the mascot, but shot 3 drops it (boards sean only) → conflict.
    sheet = BeatSheet(slug="t", logline="l", beats=[
        _beat(1, ["sean", "claude-mascot"], "a"),
        _beat(2, ["sean", "claude-mascot"], "b"),
        _beat(3, ["claude-mascot"], "c"),
    ])
    sl = ShotList(slug="t", frames=[
        _shot(1, ["sean", "claude-mascot"], 1),
        _shot(2, ["sean", "claude-mascot"], 2),
        _shot(3, ["sean"], 3),  # drops claude-mascot
    ])
    with pytest.raises(ValueError, match="conflict"):
        storyboard_validate(sheet, sl, known_namespaces=KNOWN)
