"""Scrape the claude-mascot motion plates into comparison exhibits.

This is the Museum's signature artifact in its truest form: Sean draws a motion
key sheet BY HAND (the manual shape-block, the human-authored timing constraint),
and the pipeline ingests it into colored animatic frames. One exhibit per motion
pairs the two — hand-drawn sheet on the left, the colored loop on the right —
which is the single clearest picture of what the human did and what the agents
did.

Provenance is real and recorded: `characters/{id}/motion-additions.json` maps
each colored frame to its source sheet + region and lists the IR rules it cites;
`source-refs/motion-direction.md` carries Sean's per-motion direction (the
rationale — quoted, never invented); and the ingest itself is logged in
`runs/2026-05-30-mascot-motion-ingest/bible_audit.jsonl`.
"""

from __future__ import annotations

import json
from pathlib import Path

from pipeline.museum.schema import Exhibit, Decision

# Per-motion title + intent. The intent text is quoted from
# source-refs/motion-direction.md §2 (the committed shot list) — it is sourced,
# not invented. rationale_source points readers back to that doc.
MOTION_META: dict[str, dict[str, str]] = {
    "idle": {
        "title": "Motion — Idle / settle loop",
        "intent": ("The most-used clip: ambient life on Sean's shoulder. A slow breath — "
                   "the box sinks and softens, then rises and lengthens, then sinks again, "
                   "in a loop. The baseline is stillness; the creature earns its charm by "
                   "not over-moving."),
    },
    "look": {
        "title": "Motion — Head/body-tilt look (curiosity)",
        "intent": ("Its signature reaction. The eyes dart to the target first, then the whole "
                   "creature cants toward it — a whole-body lean, not a head turn, because no "
                   "neck exists. The eye-lead breakdown is what makes the look read as thought."),
    },
    "perch": {
        "title": "Motion — Perch-settle",
        "intent": ("The establishing motion: arriving onto Sean's shoulder — the A-7 pairing in "
                   "motion. Principle-heavy, four keys: contact/reach, impact-squash, a small "
                   "overshoot bob, then settle. The squash must not be left to the interpolator "
                   "to invent."),
    },
    "alert": {
        "title": "Motion — Alert-perk (alarm in motion)",
        "intent": ("Alarm in motion. A quick wind-up, a fast snap up, then a long held stare. "
                   "Shock anticipation is short (1–2 frames), not a slow crouch; the nubs project "
                   "up-and-forward and the dot eyes widen but stay dots."),
    },
    "hop": {
        "title": "Motion — Hop (locomotion)",
        "intent": ("The walk-cycle analogue for a four-stub-legged box — Sean chose the hop over a "
                   "scuttle as the richer motion. Anticipation crouch, takeoff, a high apex that "
                   "carries the hang, landing squash, recover. The apex is the load-bearing key."),
    },
    "sleep": {
        "title": "Motion — Sleep-settle",
        "intent": ("The slowest motion in the set — everything decelerates into rest. Awake, droop, "
                   "then fully settled with the body at its lowest and the eyes closed as two small "
                   "downward graphite arcs riding the construction midline."),
    },
}


# Locomotion reads wrong as a ping-pong (hop-then-rewind); it loops forward so
# repeated hops read as continuous travel. Settle motions ping-pong (seamless).
_FORWARD_LOOP_MOTIONS = {"hop"}


def motion_loop_pingpong(motion: str) -> bool:
    """True if the motion's loop should ping-pong (forward then back)."""
    return motion not in _FORWARD_LOOP_MOTIONS


def _date_from_run_slug(run_slug: str) -> str | None:
    head = run_slug[:10]
    return head if head[:4].isdigit() and head.count("-") == 2 else None


def _motion_key(target_path: str) -> str:
    # "motion_plates/idle-01.png" -> "idle"
    return Path(target_path).name.split("-", 1)[0]


def _sheet_name(source: str) -> str:
    # "ingest:motion_plates/Idle-settle-loop.png#region:idle-01" -> "Idle-settle-loop.png"
    return source.split("#region:")[0].split("/")[-1]


def scrape_motion_plates(character_dir: Path, project_slug: str, run_slug: str) -> list[Exhibit]:
    """One exhibit per motion, pairing the hand-drawn key sheet with the colored
    frame sequence. Reads the recorded ingest spec — never globs the directory,
    so stray files not part of the ingest are honestly excluded."""
    character_dir = Path(character_dir)
    character_id = character_dir.name
    spec_path = character_dir / "motion-additions.json"
    if not spec_path.exists():
        return []
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    date = _date_from_run_slug(run_slug)

    # Group plates by motion, preserving first-appearance order.
    order: list[str] = []
    by_motion: dict[str, dict] = {}
    for plate in spec.get("plates", []):
        motion = _motion_key(plate["target_path"])
        bucket = by_motion.setdefault(motion, {"sheet": None, "frames": [], "cites": []})
        if motion not in order:
            order.append(motion)
        if bucket["sheet"] is None:
            bucket["sheet"] = _sheet_name(plate["source"])
        bucket["frames"].append(Path(plate["target_path"]).name)
        for rule in plate.get("cites_identity_rules", []):
            if rule not in bucket["cites"]:
                bucket["cites"].append(rule)

    exhibits: list[Exhibit] = []
    for motion in order:
        b = by_motion[motion]
        meta = MOTION_META.get(motion, {"title": f"Motion — {motion}", "intent": ""})
        exhibits.append(Exhibit(
            exhibit_id=f"motion-{motion}",
            project_slug=project_slug, run_slug=run_slug,
            title=meta["title"], kind="motion_keys",
            phase=4, persona="human", date=date,
            decision=Decision(
                outcome="ingested",
                rationale=meta["intent"],
                rationale_source="source-refs/motion-direction.md" if meta["intent"] else None,
            ),
            references=[f"assets/{b['sheet']}"],
            frames=[f"assets/{name}" for name in b["frames"]],
            output=f"assets/{motion}-loop.gif",
            cites_criteria=b["cites"],
            evidence_completeness="rich" if meta["intent"] else "partial",
            source_paths=[
                f"characters/{character_id}/motion-additions.json",
                f"characters/{character_id}/motion_plates/{b['sheet']}",
                f"runs/{run_slug}/bible_audit.jsonl",
            ],
        ))
    return exhibits
