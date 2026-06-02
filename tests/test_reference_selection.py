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
