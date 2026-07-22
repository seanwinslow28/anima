"""validate_artdept_dir — the structural gate on an Art Department bundle (design §8).

Checks files + cast_list shape + anchor resolution + handoff cross-check.
Look quality, prompt-pack quality, and register *fit* are Sean's live eye +
the good-look-test rubric — never asserted here. Cast shape is validated
inline (no cast.py: the front door's red-team cut seeds.py as schema theater;
the same call holds).
"""

from __future__ import annotations

from pathlib import Path

import yaml

from pipeline.artdept.handoff import Handoff
from pipeline.frontdoor.handoff import SLUG_RE
from pipeline.registers import ALL_REGISTERS

PROSE_FILES = (
    "design-bible.md",
    "prompt-pack.md",
    "chatgpt-orchestration.md",
    "environment-style.md",
    "cy_readiness_report.md",
)
TIERS = ("principal", "named")
REQUIRED_DESIGNED_FIELDS = (
    "character_id",
    "display_name",
    "tier",
    "style_register",
    "anchors",
)


def _resolves(ref: str, bundle_dir: Path, repo_root: Path) -> bool:
    """Bundle-dir-first, then repo root — fixture refs live in the bundle;
    ratified production anchors live in characters/{id}/source-refs/."""
    return (bundle_dir / ref).exists() or (repo_root / ref).exists()


def validate_artdept_dir(bundle_dir: Path, repo_root: Path | None = None) -> list[str]:
    bundle_dir = Path(bundle_dir)
    repo_root = Path(repo_root) if repo_root is not None else Path(".")
    problems: list[str] = []

    for name in PROSE_FILES:
        p = bundle_dir / name
        if not p.exists():
            problems.append(f"missing file: {name}")
        elif not p.read_text(encoding="utf-8").strip():
            problems.append(f"{name} is empty")

    handoff: Handoff | None = None
    handoff_path = bundle_dir / "artdept.json"
    if handoff_path.exists():
        try:
            handoff = Handoff.from_json(handoff_path.read_text(encoding="utf-8"))
        except (ValueError, KeyError, TypeError) as e:
            problems.append(f"artdept.json invalid: {e}")
    else:
        problems.append("missing file: artdept.json")

    _UNPARSED = object()
    designed_ids: list[str] = []
    cast_path = bundle_dir / "cast_list.yaml"
    cast = _UNPARSED
    if cast_path.exists():
        try:
            cast = yaml.safe_load(cast_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            problems.append(f"cast_list.yaml invalid YAML: {e}")

        if cast is not _UNPARSED:
            if not isinstance(cast, dict):
                problems.append("cast_list.yaml must be a mapping")
            else:
                designed = cast.get("designed")
                if not isinstance(designed, list) or not designed:
                    problems.append("cast_list.yaml: designed must be a non-empty list")
                    designed = []
                for i, entry in enumerate(designed):
                    if not isinstance(entry, dict):
                        problems.append(f"designed #{i} is not a mapping")
                        continue
                    for fld in REQUIRED_DESIGNED_FIELDS:
                        if not entry.get(fld):
                            problems.append(
                                f"designed #{i} ({entry.get('character_id', '?')}): "
                                f"missing required field {fld}"
                            )
                    cid = entry.get("character_id")
                    if isinstance(cid, str):
                        designed_ids.append(cid)
                        if not SLUG_RE.match(cid):
                            problems.append(f"designed character_id {cid!r} is not lowercase-kebab")
                    tier = entry.get("tier")
                    if tier and tier not in TIERS:
                        problems.append(
                            f"designed #{i} ({cid or '?'}): tier {tier!r} not in {TIERS} — "
                            "a non-recurring identity is extras_guidance, not a designed entry"
                        )
                    anchors = entry.get("anchors")
                    if anchors is not None and (not isinstance(anchors, list) or not anchors):
                        problems.append(
                            f"designed #{i} ({cid or '?'}): anchors must be a non-empty list of refs"
                        )
                    elif isinstance(anchors, list):
                        for ref in anchors:
                            if not (isinstance(ref, str) and _resolves(ref, bundle_dir, repo_root)):
                                problems.append(
                                    f"designed #{i} ({cid or '?'}): anchor ref {ref!r} does not "
                                    "resolve (checked bundle dir, then repo root)"
                                )
                world = cast.get("world")
                if world is not None:
                    if not isinstance(world, list):
                        problems.append("cast_list.yaml: world must be a list of locations")
                    else:
                        for j, loc in enumerate(world):
                            if not isinstance(loc, dict) or not loc.get("id"):
                                problems.append(f"world #{j}: missing id")
                                continue
                            for ref in loc.get("refs") or []:
                                if not (isinstance(ref, str) and _resolves(ref, bundle_dir, repo_root)):
                                    problems.append(
                                        f"world #{j} ({loc['id']}): ref {ref!r} does not resolve"
                                    )
                if not (isinstance(cast.get("extras_guidance"), str) and cast["extras_guidance"].strip()):
                    problems.append(
                        "cast_list.yaml: missing extras_guidance — extras are covered by "
                        "guidance baked into the prompt pack, never by silence (design §6)"
                    )
    else:
        problems.append("missing file: cast_list.yaml")

    if handoff is not None and cast_path.exists() and cast is not _UNPARSED and isinstance(cast, dict) and sorted(handoff.characters) != sorted(designed_ids):
        problems.append(
            f"artdept.json characters {sorted(handoff.characters)} do not match "
            f"cast_list.yaml designed ids {sorted(designed_ids)}"
        )

    return problems


def register_warnings(bundle_dir: Path) -> list[str]:
    """SOFT flags. The Art Department locks a register by look-test, but a
    design can legitimately complete while the register's authoring rides the
    playbook as a called dependency (design §7 — the GRANDMASTER shape). So an
    unregistered register WARNS with the playbook pointer; the hard gate stays
    Cy execution (pipeline.registers raises UnknownRegisterError)."""
    bundle_dir = Path(bundle_dir)
    warnings: list[str] = []
    cast_path = bundle_dir / "cast_list.yaml"
    if not cast_path.exists():
        return warnings
    try:
        cast = yaml.safe_load(cast_path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return warnings
    if not isinstance(cast, dict) or not isinstance(cast.get("designed"), list):
        return warnings
    for i, entry in enumerate(cast["designed"]):
        if not isinstance(entry, dict):
            continue
        reg = entry.get("style_register")
        if isinstance(reg, str) and reg and reg not in ALL_REGISTERS:
            warnings.append(
                f"designed #{i} ({entry.get('character_id', '?')}): style_register "
                f"{reg!r} is not in the closed vocabulary yet — run "
                f"docs/architecture/style-register-authoring-playbook.md (R→S→B) "
                f"before the Cy pass (Cy fails loud on an unregistered register)."
            )
    return warnings


def location_angle_warnings(bundle_dir: Path) -> list[str]:
    """SOFT flags for the single-angle-location trap (DR #20, 2026-07-20).

    Every key location must be designed from a *set* of camera angles (master +
    reverse/180° + an angle per recurring character standing-position) with a
    spatial placement map in environment-style.md, so composites place
    characters consistently and shot/reverse-shot holds — a location carrying
    one ref is the trap that made the FIRST LICKS geyser shots read as two
    figures a foot apart and left grandma's room single-angle. WARN, never fail:
    a location genuinely seen once may legitimately have one angle, and the call
    is Sean's eye (mirrors register_warnings — the hard gate stays Cy)."""
    bundle_dir = Path(bundle_dir)
    warnings: list[str] = []
    cast_path = bundle_dir / "cast_list.yaml"
    if not cast_path.exists():
        return warnings
    try:
        cast = yaml.safe_load(cast_path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return warnings
    if not isinstance(cast, dict) or not isinstance(cast.get("world"), list):
        return warnings
    for loc in cast["world"]:
        if not isinstance(loc, dict) or not loc.get("id"):
            continue
        refs = loc.get("refs")
        n = len(refs) if isinstance(refs, list) else 0
        if n < 2:
            warnings.append(
                f"location {loc['id']!r} has {n} angle ref(s) — DR #20 wants a "
                "multi-angle set (master + reverse/180° + per-character-position) "
                "plus a placement map in environment-style.md. Confirm this "
                "location is truly single-angle, or add its angle set (the montage "
                "+ room single-angle slips are why this check exists)."
            )
    return warnings
