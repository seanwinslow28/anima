"""CI contamination guard — eval fixtures must never BE the references.

Born from the 2026-06-03 eval-foundation reset: 19 of 23 old vision-critic
fixtures were byte-identical (SHA-256-matched) copies of Bible/source plates,
which made "clean" mean "is the reference plate" and turned the
reference-grounding experiment into a confabulation trap by construction
(docs/2026-06-03-eval-foundation-reset-plan.md §1, §5).

This test converts the "don't contaminate the fixtures" convention into an
enforced invariant:

  FAIL if any file under evals/vision_critic/fixtures/ either
    (a) shares a SHA-256 digest with any file under characters/ or images/, or
    (b) shares an inode (same device + inode number — a hardlink) with one.

The gold-standard turnaround sheets under characters/sean-anchor/source-refs/
are explicitly in scope: fixtures are generated AGAINST the references and must
never be copies OF them.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = REPO_ROOT / "evals" / "vision_critic" / "fixtures"
REFERENCE_ROOTS = [REPO_ROOT / "characters", REPO_ROOT / "images"]

# Noise we never treat as fixture or reference content.
_SKIP_NAMES = {".DS_Store", ".gitignore", "CACHEDIR.TAG"}
_SKIP_DIR_PARTS = {".pytest_cache", "__pycache__", ".remember", ".git"}


def _iter_files(root: Path):
    if not root.exists():
        return
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        if path.name in _SKIP_NAMES:
            continue
        if _SKIP_DIR_PARTS.intersection(path.parts):
            continue
        yield path


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def test_fixtures_exist():
    """The guard is vacuous without fixtures — make absence loud, not green."""
    files = list(_iter_files(FIXTURES_DIR))
    assert files, f"no fixture files found under {FIXTURES_DIR}"


def test_fixtures_share_no_sha256_with_references():
    ref_hashes: dict[str, Path] = {}
    for root in REFERENCE_ROOTS:
        for path in _iter_files(root):
            ref_hashes.setdefault(_sha256(path), path)

    collisions = []
    for fixture in _iter_files(FIXTURES_DIR):
        digest = _sha256(fixture)
        if digest in ref_hashes:
            collisions.append(
                f"{fixture.relative_to(REPO_ROOT)} is byte-identical to "
                f"{ref_hashes[digest].relative_to(REPO_ROOT)}"
            )

    assert not collisions, (
        "CONTAMINATED FIXTURES (fixture IS a reference plate — see "
        "docs/2026-06-03-eval-foundation-reset-plan.md §5):\n  "
        + "\n  ".join(collisions)
    )


def test_fixtures_share_no_inode_with_references():
    ref_inodes: dict[tuple[int, int], Path] = {}
    for root in REFERENCE_ROOTS:
        for path in _iter_files(root):
            st = os.stat(path)
            ref_inodes.setdefault((st.st_dev, st.st_ino), path)

    collisions = []
    for fixture in _iter_files(FIXTURES_DIR):
        st = os.stat(fixture)
        key = (st.st_dev, st.st_ino)
        if key in ref_inodes:
            collisions.append(
                f"{fixture.relative_to(REPO_ROOT)} is hardlinked to "
                f"{ref_inodes[key].relative_to(REPO_ROOT)}"
            )

    assert not collisions, (
        "HARDLINKED FIXTURES (fixture shares an inode with a reference):\n  "
        + "\n  ".join(collisions)
    )
