# tests/test_reference_selection.py
"""select_references: the fixed, Bible-driven, capped reference bundle (approach B)."""
from __future__ import annotations

from pathlib import Path

from pipeline.agents.reference_selection import select_references


def _make_char(tmp_path: Path, char_id: str, turnarounds: list[str], *, anchor: bool = True) -> Path:
    """A synthetic Bible: folder name deliberately != character_id (mirrors
    sean-anchor/ holding character_id 'sean')."""
    folder = tmp_path / f"{char_id}-folder"
    (folder / "turnarounds").mkdir(parents=True)
    (folder / "character.yaml").write_text(f"character_id: {char_id}\n", encoding="utf-8")
    if anchor:
        (folder / "anchor.png").write_bytes(b"x")
    for name in turnarounds:
        (folder / "turnarounds" / f"{name}.png").write_bytes(b"x")
    return folder


def test_resolves_folder_by_character_yaml_not_foldername(tmp_path):
    _make_char(tmp_path, "sean", ["head-front", "body-3quarter"])
    refs = select_references("sean", "phase_5_generate", "", characters_root=tmp_path)
    assert refs and refs[0].name == "anchor.png"
    assert refs[0].parent.name == "sean-folder"  # found via character.yaml, not name


def test_sean_like_bundle_is_diverse_views(tmp_path):
    _make_char(tmp_path, "sean", [
        "head-front", "head-3quarter", "head-profile-left", "head-profile-right",
        "head-back", "body-3quarter", "body-back", "body-profile-left", "body-profile-right",
    ])
    refs = select_references("sean", "phase_5_generate", "", characters_root=tmp_path, cap=3)
    assert [p.name for p in refs] == [
        "anchor.png", "head-front.png", "head-profile-left.png", "body-3quarter.png",
    ]


def test_mascot_all_body_generalizes(tmp_path):
    _make_char(tmp_path, "claude-mascot", [
        "body-front", "body-3quarter", "body-side", "body-back", "body-3quarter-back",
    ])
    refs = select_references("claude-mascot", "phase_5_generate", "", characters_root=tmp_path, cap=3)
    # No head-* plates → falls through to body views; still diverse, anchor + 3.
    assert [p.name for p in refs] == [
        "anchor.png", "body-3quarter.png", "body-front.png", "body-side.png",
    ]


def test_missing_anchor_dropped_not_raised(tmp_path):
    _make_char(tmp_path, "x", ["head-front"], anchor=False)
    refs = select_references("x", "phase_5_generate", "", characters_root=tmp_path)
    assert [p.name for p in refs] == ["head-front.png"]


def test_unknown_character_returns_empty(tmp_path):
    (tmp_path / "other").mkdir()
    assert select_references("nobody", "phase_5_generate", "", characters_root=tmp_path) == []


def test_empty_character_id_returns_empty(tmp_path):
    assert select_references("", "phase_5_generate", "", characters_root=tmp_path) == []


def test_real_sean_bible_target_bundle():
    """Integration: the committed (locked) Sean Bible → the brainstorm target bundle."""
    repo_characters = Path(__file__).resolve().parents[1] / "characters"
    refs = select_references("sean", "phase_5_generate", "", characters_root=repo_characters, cap=3)
    assert [p.name for p in refs] == [
        "anchor.png", "head-front.png", "head-profile-left.png", "body-3quarter.png",
    ]


# ---------------------------------------------------------------------------
# B1a — view-aware selection (approach A, eval path). When the beat carries an
# inferable view ("right profile", "3/4 turnaround", "back view"), the matching
# turnaround leads the bundle so a profile subject gets a profile reference; a
# beat with no view word preserves the approach-B diversity order exactly. The
# subject's view is read from beat metadata (cheap + exact in the eval); prod
# view-inference is a separate, harder follow-on (a view classifier / manifest
# hint), deliberately out of scope here.
# ---------------------------------------------------------------------------


def test_profile_right_beat_ranks_profile_match_first(tmp_path):
    _make_char(tmp_path, "sean", [
        "head-front", "head-3quarter", "head-profile-left", "head-profile-right",
        "head-back", "body-3quarter", "body-back", "body-profile-left", "body-profile-right",
    ])
    refs = select_references("sean", "phase_5_generate", "Sean full-body right profile",
                             characters_root=tmp_path, cap=3)
    assert refs[0].name == "anchor.png"                 # anchor still leads
    assert "profile-right" in refs[1].stem.lower()      # view-matched plate leads the turnarounds


def test_3quarter_beat_ranks_3quarter_match_first(tmp_path):
    _make_char(tmp_path, "sean", [
        "head-front", "head-profile-left", "body-3quarter", "body-back",
    ])
    refs = select_references("sean", "phase_5_generate", "Sean 3/4 turnaround",
                             characters_root=tmp_path, cap=3)
    assert "3quarter" in refs[1].stem.lower()


def test_no_view_in_beat_preserves_diversity_order(tmp_path):
    _make_char(tmp_path, "sean", [
        "head-front", "head-3quarter", "head-profile-left", "head-profile-right",
        "head-back", "body-3quarter", "body-back", "body-profile-left", "body-profile-right",
    ])
    refs = select_references("sean", "phase_5_generate", "idle at the desk, fixed camera",
                             characters_root=tmp_path, cap=3)
    assert [p.name for p in refs] == [
        "anchor.png", "head-front.png", "head-profile-left.png", "body-3quarter.png",
    ]


def test_best_view_reference_returns_view_match(tmp_path):
    from pipeline.agents.reference_selection import best_view_reference
    _make_char(tmp_path, "sean", ["head-front", "head-profile-right", "body-profile-right"])
    ref = best_view_reference("sean", "Sean right profile", characters_root=tmp_path)
    assert ref is not None and "profile-right" in ref.stem.lower()


def test_best_view_reference_none_when_no_view(tmp_path):
    from pipeline.agents.reference_selection import best_view_reference
    _make_char(tmp_path, "sean", ["head-front", "body-3quarter"])
    assert best_view_reference("sean", "idle, fixed camera", characters_root=tmp_path) is None


def test_best_view_reference_none_when_no_matching_turnaround(tmp_path):
    from pipeline.agents.reference_selection import best_view_reference
    _make_char(tmp_path, "sean", ["head-front"])  # no profile plate to match
    assert best_view_reference("sean", "Sean right profile", characters_root=tmp_path) is None
