# pipeline/agents/reference_selection.py
"""Reference-bundle selection for Em (the T2 vision critic).

Approach B (this version): a FIXED, Bible-driven, capped bundle — the character's
anchor.png + up to `cap` canonical deduped turnarounds (front / 3-quarter /
profile) — resolved FROM THE BIBLE folder, ignoring checkpoint/beat. The signature
already accepts checkpoint/beat so view-aware selection (approach A) drops into
this module later with no change to the eval contract.

Bible-driven, NOT hardcoded filenames: the anchor is <folder>/anchor.png;
turnarounds are globbed from <folder>/turnarounds/ and ranked by a view-preference
list, so the function generalizes to any character (e.g. claude-mascot's all-body
crops) with no code change. Every path is existence-checked; a missing plate is
dropped with a log note — a thin bundle is honest, the critic never crashes on a
gap. The folder key (sean-anchor/) and the IR character_id (sean) are allowed to
differ; character.yaml is the single source of truth for the mapping.
"""
from __future__ import annotations

import logging
from pathlib import Path

import yaml

log = logging.getLogger(__name__)


class ReferenceSelectionError(Exception):
    """Unrecoverable mis-configuration (e.g. characters_root is not a directory).
    A missing INDIVIDUAL plate never raises — it is dropped with a log note."""


# Ordered view preference. For each pattern in order, the resolver picks the first
# UNUSED turnaround whose stem CONTAINS it, until `cap` are chosen. Ordered for view
# DIVERSITY (a front face, a profile face, a body-proportion view) rather than three
# near-identical head shots — so Sean → head-front + head-profile-left + body-3quarter,
# and the mascot (all-body) → body-3quarter + body-front + body-side.
_TURNAROUND_PREFERENCE: tuple[str, ...] = (
    "head-front", "head-profile-left", "body-3quarter",
    "head-profile-right", "head-3quarter", "body-front",
    "body-side", "body-profile-left", "body-profile-right",
    "body-back", "head-back",
    # generic fallbacks for unknown naming conventions:
    "front", "profile", "side", "3quarter", "body", "head",
)


def _resolve_folder(character_id: str, characters_root: Path) -> Path | None:
    """Map a character_id (e.g. 'sean') to its Bible folder (e.g. 'sean-anchor/')
    by reading each <folder>/character.yaml's character_id field. Returns None if
    no Bible declares this character_id."""
    if not characters_root.is_dir():
        raise ReferenceSelectionError(f"characters_root is not a directory: {characters_root}")
    # Fast path: a folder literally named character_id whose yaml confirms it.
    direct = characters_root / character_id
    if (direct / "character.yaml").exists():
        return direct
    for child in sorted(characters_root.iterdir()):
        cy = child / "character.yaml"
        if not cy.exists():
            continue
        try:
            data = yaml.safe_load(cy.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if data.get("character_id") == character_id:
            return child
    return None


def _select_turnarounds(folder: Path, cap: int) -> list[Path]:
    turn_dir = folder / "turnarounds"
    if not turn_dir.is_dir():
        return []
    available = sorted(turn_dir.glob("*.png"))
    picked: list[Path] = []
    used: set[Path] = set()
    for pattern in _TURNAROUND_PREFERENCE:
        if len(picked) >= cap:
            break
        # Prefer an EXACT stem match before a substring match. A specific pattern
        # ("body-3quarter") must bind to body-3quarter.png and not to a longer
        # sibling that merely CONTAINS it (body-3quarter-back.png) — which sorts
        # first ("-" < ".") and would otherwise pull an unwanted back view into a
        # bundle meant to be front/3-quarter/side-diverse (spec §4). The generic
        # tail patterns ("front", "side", ...) still resolve via the substring
        # fallback, since no stem equals them outright.
        match = next((p for p in available if p not in used and p.stem.lower() == pattern), None)
        if match is None:
            match = next((p for p in available if p not in used and pattern in p.stem.lower()), None)
        if match is not None:
            picked.append(match)
            used.add(match)
    return picked[:cap]


def select_references(
    character_id: str,
    checkpoint: str,
    beat: str,
    *,
    characters_root: Path,
    cap: int = 3,
) -> list[Path]:
    """Return the reference bundle (anchor + up to `cap` turnarounds) for one Em
    invocation. v1 ignores checkpoint/beat (approach B). The returned list NEVER
    includes the frame under review — the caller prepends the subject. Missing
    plates are dropped with a log note."""
    if not character_id:
        return []
    folder = _resolve_folder(character_id, Path(characters_root))
    if folder is None:
        log.info("select_references: no Bible folder for character_id=%r under %s",
                 character_id, characters_root)
        return []
    bundle: list[Path] = []
    anchor = folder / "anchor.png"
    if anchor.exists():
        bundle.append(anchor)
    else:
        log.info("select_references: anchor.png missing for %s; dropping", folder)
    for t in _select_turnarounds(folder, cap):
        if t.exists():
            bundle.append(t)
    return bundle
