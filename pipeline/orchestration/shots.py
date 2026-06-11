"""shots.yaml — the human-authored shot list the GENERATE stage consumes.

Externalizes what scripts/spark_frame.py's hard-coded FRAMES dict held.
Phase 3 (storyboard / shot list) is human-authored today; Maya plans and
sets acceptance criteria, the shot list drives generation. The orchestrator
never invents frame prompts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

_SLUG_RE = re.compile(r"^[A-Za-z0-9_-]+$")
_TOP_KEYS = {"slug", "frames"}
_FRAME_KEYS = {"id", "cast", "beat", "prompt", "extra_references", "chain_anchors", "hold"}


@dataclass(frozen=True)
class Shot:
    id: int
    cast: list[str]              # IR namespaces; first = primary (Flo's folder key)
    beat: str                    # Em beat_description + T1 pose_description
    prompt: str                  # Flo's generation prompt
    extra_references: list[str] = field(default_factory=list)
    chain_anchors: list[str] = field(default_factory=list)  # ⊆ cast; default: all of cast
    hold: int = 2                # on-twos default


@dataclass(frozen=True)
class ShotList:
    slug: str
    frames: list[Shot]

    def by_id(self, n: int) -> Shot:
        for s in self.frames:
            if s.id == n:
                return s
        raise KeyError(f"no shot with id {n}")


def load_shots(path: Path, *, known_namespaces: set[str]) -> ShotList:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}

    unknown_top = set(raw) - _TOP_KEYS
    if unknown_top:
        raise ValueError(f"shots.yaml: unknown top-level key(s) {sorted(unknown_top)}")
    slug = raw.get("slug")
    if not slug or not _SLUG_RE.match(str(slug)):
        raise ValueError(f"shots.yaml: slug must match [A-Za-z0-9_-]+, got {slug!r}")
    frames_raw = raw.get("frames")
    if not frames_raw or not isinstance(frames_raw, list):
        raise ValueError("shots.yaml: frames must be a non-empty list")

    frames: list[Shot] = []
    prev_id = 0
    for i, entry in enumerate(frames_raw):
        unknown = set(entry) - _FRAME_KEYS
        if unknown:
            raise ValueError(f"shots.yaml frames[{i}]: unknown key(s) {sorted(unknown)}")
        fid = entry.get("id")
        if not isinstance(fid, int) or fid < 1:
            raise ValueError(f"shots.yaml frames[{i}]: id must be an int >= 1, got {fid!r}")
        if fid <= prev_id:
            raise ValueError(
                f"shots.yaml frames[{i}]: id {fid} not strictly ascending "
                f"(duplicate or out of order after {prev_id}) — ids define the chain order"
            )
        prev_id = fid
        cast = entry.get("cast") or []
        if not cast:
            raise ValueError(f"shots.yaml frame {fid}: cast must be a non-empty list")
        bad_ns = [ns for ns in cast if ns not in known_namespaces]
        if bad_ns:
            raise ValueError(
                f"shots.yaml frame {fid}: cast names unknown IR namespace(s) {bad_ns} "
                f"(known: {sorted(known_namespaces)})"
            )
        beat = entry.get("beat") or ""
        if not beat.strip():
            raise ValueError(f"shots.yaml frame {fid}: beat must be non-empty")
        prompt = entry.get("prompt") or ""
        if not prompt.strip():
            raise ValueError(f"shots.yaml frame {fid}: prompt must be non-empty")
        chain_anchors = entry.get("chain_anchors")
        if chain_anchors is None:
            chain_anchors = list(cast)
        bad_ca = [ns for ns in chain_anchors if ns not in cast]
        if bad_ca:
            raise ValueError(
                f"shots.yaml frame {fid}: chain_anchors {bad_ca} not in the frame's cast {cast}"
            )
        hold = entry.get("hold", 2)
        if not isinstance(hold, int) or hold < 1:
            raise ValueError(f"shots.yaml frame {fid}: hold must be an int >= 1, got {hold!r}")
        frames.append(
            Shot(
                id=fid,
                cast=list(cast),
                beat=beat,
                prompt=prompt,
                extra_references=[str(p) for p in (entry.get("extra_references") or [])],
                chain_anchors=list(chain_anchors),
                hold=hold,
            )
        )
    return ShotList(slug=str(slug), frames=frames)


def read_slug(path: Path) -> str | None:
    """Light read of just the slug (used at run init, before full validation)."""
    try:
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return None
    slug = raw.get("slug")
    return str(slug) if slug else None
