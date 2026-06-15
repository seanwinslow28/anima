"""beats.json — the Sam→Bea contract: a structured beat sheet.

Sam (the Phase-3a scriptwriter) authors a studio-voice script.md treatment plus
this machine-readable beat sheet; Bea (Phase-3b, a follow-on slice) turns the
beats into the human-curated shots.yaml. Mirrors pipeline/orchestration/shots.py
— same strict-validator philosophy — so "did Sam produce something Bea can
consume" is a free deterministic gate, and `cast` carries beat → shot → shots.yaml
cast unchanged.

beats.json is machine-emitted (like Maya's acceptance_criteria.json) — JSON, not
the human-authored shots.yaml's YAML — and carries a top-level `locked` flag that
`script approve` flips. load_beats tolerates `locked` so an approved file reloads.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

_SLUG_RE = re.compile(r"^[A-Za-z0-9_-]+$")
_TOP_KEYS = {"slug", "logline", "beats", "locked"}
_BEAT_KEYS = {"id", "title", "intent", "emotional_beat", "cast", "feel", "notes"}


@dataclass(frozen=True)
class Beat:
    id: int                       # strictly ascending — story order (mirrors Shot.id)
    title: str                    # short beat name ("The Spark")
    intent: str                   # what the beat does in the story
    emotional_beat: str           # the felt state ("calm focus → first stir")
    cast: list[str]               # ⊆ manifest IR namespaces; flows to shots.yaml cast
    feel: str = ""                # timing/pacing note ("establishing — let it breathe")
    notes: str = ""               # continuity / loop notes


@dataclass(frozen=True)
class BeatSheet:
    slug: str
    logline: str
    beats: list[Beat]

    def by_id(self, n: int) -> Beat:
        for b in self.beats:
            if b.id == n:
                return b
        raise KeyError(f"no beat with id {n}")


def load_beats(path: Path, *, known_namespaces: set[str]) -> BeatSheet:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("beats.json: top level must be a JSON object")

    unknown_top = set(raw) - _TOP_KEYS
    if unknown_top:
        raise ValueError(f"beats.json: unknown top-level key(s) {sorted(unknown_top)}")
    slug = raw.get("slug")
    if not slug or not _SLUG_RE.match(str(slug)):
        raise ValueError(f"beats.json: slug must match [A-Za-z0-9_-]+, got {slug!r}")
    logline = raw.get("logline") or ""
    if not str(logline).strip():
        raise ValueError("beats.json: logline must be non-empty")
    beats_raw = raw.get("beats")
    if not beats_raw or not isinstance(beats_raw, list):
        raise ValueError("beats.json: beats must be a non-empty list")

    beats: list[Beat] = []
    prev_id = 0
    for i, entry in enumerate(beats_raw):
        if not isinstance(entry, dict):
            raise ValueError(f"beats.json beats[{i}]: must be a JSON object")
        unknown = set(entry) - _BEAT_KEYS
        if unknown:
            raise ValueError(f"beats.json beats[{i}]: unknown key(s) {sorted(unknown)}")
        bid = entry.get("id")
        if not isinstance(bid, int) or isinstance(bid, bool) or bid < 1:
            raise ValueError(f"beats.json beats[{i}]: id must be an int >= 1, got {bid!r}")
        if bid <= prev_id:
            raise ValueError(
                f"beats.json beats[{i}]: id {bid} not strictly ascending "
                f"(duplicate or out of order after {prev_id}) — ids define story order"
            )
        prev_id = bid
        title = entry.get("title") or ""
        if not str(title).strip():
            raise ValueError(f"beats.json beat {bid}: title must be non-empty")
        intent = entry.get("intent") or ""
        if not str(intent).strip():
            raise ValueError(f"beats.json beat {bid}: intent must be non-empty")
        emotional_beat = entry.get("emotional_beat") or ""
        if not str(emotional_beat).strip():
            raise ValueError(f"beats.json beat {bid}: emotional_beat must be non-empty")
        cast = entry.get("cast") or []
        if not cast or not isinstance(cast, list):
            raise ValueError(f"beats.json beat {bid}: cast must be a non-empty list")
        bad_ns = [ns for ns in cast if ns not in known_namespaces]
        if bad_ns:
            raise ValueError(
                f"beats.json beat {bid}: cast names unknown IR namespace(s) {bad_ns} "
                f"(known: {sorted(known_namespaces)})"
            )
        beats.append(
            Beat(
                id=bid,
                title=str(title),
                intent=str(intent),
                emotional_beat=str(emotional_beat),
                cast=[str(c) for c in cast],
                feel=str(entry.get("feel") or ""),
                notes=str(entry.get("notes") or ""),
            )
        )
    return BeatSheet(slug=str(slug), logline=str(logline), beats=beats)


def read_slug(path: Path) -> str | None:
    """Light read of just the slug (used before full validation). Mirrors shots.read_slug."""
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(raw, dict):
        return None
    slug = raw.get("slug")
    return str(slug) if slug else None
