"""anima — acceptance_criteria.json schema, loader, lock enforcement.

The v2 synthesis identified the Planner-Chairman shared-rubric pattern as
the structural fix for local-optimization drift (Grok-CM3 estimated 60%+
indie animation projects die from it). Maya emits this file at Phase 0
post-approval and the manifest flips criteria_locked: true.

After lock, every critic from T2 onward cites criteria IDs by `cites_criteria`
on AgentResult; the chairman in T3 resolves disputes against these IDs; the
museum writer narrates changes in their terms. The runner refuses to mutate
the file without --force-criteria-mutation + an audit log entry naming the
actor and reason. This is anima's lever against the failure mode where every
phase ships "better" output that no longer matches what Sean approved.

Two schema versions coexist:
- v1.0 (commit 4) — flat list of {id, phase, description, severity}. Still
  loads unchanged; the pencil-test reference implementation uses it.
- v1.1 (commit 3) — graph shape. Mnemonic IDs (AC.{category}.{handle}) with
  closed category vocabulary. Per-criterion cites_phase / cites_personas
  routing edges, impact_tag for Em's escalation hatch, parent_id for
  derived criteria, derived_from for provenance pointing back to the brief.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

Severity = Literal["blocking", "advisory"]
VALID_SEVERITIES = {"blocking", "advisory"}

# v1.1 closed vocabularies. Per Maya brainstorm TOP-2: the category list is
# short and closed so Em / Cy / Sage / Mo can pattern-match against it
# without ambiguity. Expanding the vocabulary is a deliberate brief-update
# commit, not an inline Maya-prompt tweak.
VALID_CATEGORIES = frozenset({
    "identity", "proportion", "continuity", "timing",
    "tone", "structural", "technical",
})
VALID_IMPACT_TAGS = frozenset({
    "hero", "identity_critical", "continuity",
    "aesthetic", "structural", "technical",
})

# v1.2 closed vocabulary for Cy's character-bound identity rules. Per Cy
# brainstorm TOP-2 (2026-05-27): IR.* entries are first-class criteria living
# in the same acceptance_criteria.json graph as Maya's AC.* entries, but use
# their own ten-category vocabulary because Cy reasons in character-design
# terms (anatomy, hair, face, palette, pose) rather than spec-design terms
# (identity, proportion, tone). Em loads style register before identity rules
# and routes its citation rubric against this vocab when judging Phase 5 + 6
# frames against the Bible.
VALID_IR_CATEGORIES = frozenset({
    "anatomy", "hair", "face", "proportion", "palette",
    "costume", "prop", "pose", "motion", "style",
})

# Mnemonic ID pattern: AC.{category}.{handle}. Category is one of the closed
# vocab above; handle is kebab-or-snake lowercase. Em's escalation hatch keys
# off impact_tag (not the ID parse), so handle stays flexible.
_MNEMONIC_ID_PATTERN = re.compile(r"^AC\.([a-z_]+)\.([a-z0-9\-]+)$")

# v1.2 IR.* pattern: three dotted segments — IR.{character_id}.{category}.{handle}.
# character_id is lowercase-kebab (matches the folder name in characters/).
# category is one of VALID_IR_CATEGORIES. handle stays flexible.
_IR_ID_PATTERN = re.compile(r"^IR\.([a-z0-9\-]+)\.([a-z_]+)\.([a-z0-9\-]+)$")


@dataclass(frozen=True)
class AcceptanceCriterion:
    """One criterion. Polymorphic over schema version.

    v1.0 records carry `phase` and `severity`; v1.1 fields default to empty.
    v1.1 records carry the graph fields; v1.0 fields default to None.
    v1.2 records (Cy's IR.* identity rules) carry `character_id` populated
    from the parsed mnemonic ID; AC.* records keep character_id=None.
    Consumers that only care about one version inspect the relevant fields.
    """
    id: str
    description: str
    # v1.0 fields (None on v1.1 / v1.2 records).
    phase: str | None = None
    severity: Severity | None = None
    # v1.1 graph fields (empty / None on v1.0 records).
    cites_phase: tuple[int, ...] = ()
    cites_personas: tuple[str, ...] = ()
    impact_tag: str | None = None
    parent_id: str | None = None
    derived_from: tuple[str, ...] = ()
    # v1.2 Bible-layer field (None on AC.* records; required on IR.* records).
    character_id: str | None = None


@dataclass
class CriteriaBundle:
    """Loaded criteria file. version is the source-of-truth for which fields
    on AcceptanceCriterion are populated."""
    version: str
    locked: bool
    criteria: list[AcceptanceCriterion] = field(default_factory=list)

    def query_by_phase(self, phase: int) -> list[AcceptanceCriterion]:
        """Return v1.1 criteria citing the given phase number. Returns an
        empty list on v1.0 bundles since cites_phase is empty there."""
        return [c for c in self.criteria if phase in c.cites_phase]

    def query_by_persona(self, persona: str) -> list[AcceptanceCriterion]:
        """Return v1.1 criteria citing the given persona name."""
        return [c for c in self.criteria if persona in c.cites_personas]

    def query_by_character(self, character_id: str) -> list[AcceptanceCriterion]:
        """Return v1.2 IR.* criteria bound to the given character_id.

        Returns an empty list on AC.*-only bundles since no records carry a
        character_id there. The Bible authoring workflow calls this when Em
        needs to surface 'just the rules for the character in this Phase 5
        frame' from a merged CriteriaBundle that holds multiple characters.
        """
        return [c for c in self.criteria if c.character_id == character_id]


class CriteriaLockViolation(RuntimeError):
    """Raised when a locked criteria file is being mutated without --force."""


def load_criteria(path: Path) -> CriteriaBundle:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_criteria(raw)
    version = str(raw["version"])
    criteria_list: list[AcceptanceCriterion] = []
    for c in raw["criteria"]:
        if version.startswith("1.0"):
            criteria_list.append(AcceptanceCriterion(
                id=c["id"],
                description=c["description"],
                phase=c["phase"],
                severity=c["severity"],
            ))
        else:
            # v1.1 + v1.2 share the graph fields; v1.2 IR.* records additionally
            # carry character_id. The validator has already enforced that IR.*
            # records' character_id field matches the parsed prefix, so we can
            # trust the value here.
            criteria_list.append(AcceptanceCriterion(
                id=c["id"],
                description=c["description"],
                cites_phase=tuple(c.get("cites_phase") or ()),
                cites_personas=tuple(c.get("cites_personas") or ()),
                impact_tag=c.get("impact_tag"),
                parent_id=c.get("parent_id"),
                derived_from=tuple(c.get("derived_from") or ()),
                character_id=c.get("character_id"),
            ))
    return CriteriaBundle(
        version=version,
        locked=bool(raw.get("locked", False)),
        criteria=criteria_list,
    )


def validate_criteria(raw: dict) -> None:
    if "version" not in raw:
        raise ValueError("acceptance_criteria.json missing 'version'")
    if "criteria" not in raw or not isinstance(raw["criteria"], list):
        raise ValueError("acceptance_criteria.json missing or malformed 'criteria' list")
    version = str(raw["version"])
    if version.startswith("1.0"):
        _validate_v1_0(raw["criteria"])
    elif version.startswith("1.1"):
        _validate_v1_1(raw["criteria"])
    elif version.startswith("1.2"):
        _validate_v1_2(raw["criteria"])
    else:
        raise ValueError(f"unsupported criteria schema version: {version}")


def _validate_v1_0(criteria: list[dict]) -> None:
    seen: set[str] = set()
    for c in criteria:
        for field_name in ("id", "phase", "description", "severity"):
            if field_name not in c:
                raise ValueError(f"Criterion missing required field: {field_name}")
        if c["id"] in seen:
            raise ValueError(f"Duplicate criterion id: {c['id']}")
        seen.add(c["id"])
        if c["severity"] not in VALID_SEVERITIES:
            raise ValueError(
                f"Criterion {c['id']!r} has unknown severity {c['severity']!r}; "
                f"expected one of {sorted(VALID_SEVERITIES)}"
            )


def _validate_v1_1(criteria: list[dict]) -> None:
    seen: set[str] = set()
    for c in criteria:
        for field_name in ("id", "description", "cites_phase", "cites_personas"):
            if field_name not in c:
                raise ValueError(f"Criterion missing required field: {field_name}")
        match = _MNEMONIC_ID_PATTERN.match(c["id"])
        if not match:
            raise ValueError(
                f"Criterion {c['id']!r} has malformed id; expected pattern "
                f"AC.<category>.<handle> (lowercase kebab handle)"
            )
        category = match.group(1)
        if category not in VALID_CATEGORIES:
            raise ValueError(
                f"Criterion {c['id']!r} has unknown category {category!r}; "
                f"expected one of {sorted(VALID_CATEGORIES)}"
            )
        if c["id"] in seen:
            raise ValueError(f"Duplicate criterion id: {c['id']}")
        seen.add(c["id"])
        impact = c.get("impact_tag")
        if impact is not None and impact not in VALID_IMPACT_TAGS:
            raise ValueError(
                f"Criterion {c['id']!r} has unknown impact_tag {impact!r}; "
                f"expected one of {sorted(VALID_IMPACT_TAGS)}"
            )


def _validate_v1_2(criteria: list[dict]) -> None:
    """v1.2 schema: AC.* and IR.* IDs coexist in the same graph.

    AC.* entries validate against the v1.1 rules (AC category vocab, optional
    impact_tag, etc.); they may omit `character_id` (it defaults to None on
    the loaded record). IR.* entries validate against the IR category vocab,
    require a `character_id` field that matches the parsed character_id from
    the ID, and may carry `derived_from` entries with the `#region:X`
    plate-pointer suffix (the validator treats the suffix as opaque metadata —
    a sensible follow-up commit may tighten this to verify the path exists
    on disk, but commit 2 keeps it schema-level only).
    """
    seen: set[str] = set()
    for c in criteria:
        for field_name in ("id", "description", "cites_phase", "cites_personas"):
            if field_name not in c:
                raise ValueError(f"Criterion missing required field: {field_name}")
        if c["id"] in seen:
            raise ValueError(f"Duplicate criterion id: {c['id']}")
        seen.add(c["id"])

        ir_match = _IR_ID_PATTERN.match(c["id"])
        ac_match = _MNEMONIC_ID_PATTERN.match(c["id"])

        if ir_match:
            # IR.{character_id}.{category}.{handle}
            parsed_char_id = ir_match.group(1)
            parsed_category = ir_match.group(2)
            if parsed_category not in VALID_IR_CATEGORIES:
                raise ValueError(
                    f"Criterion {c['id']!r} has unknown IR category "
                    f"{parsed_category!r}; expected one of "
                    f"{sorted(VALID_IR_CATEGORIES)}"
                )
            # character_id field is required and must match the parsed prefix.
            if "character_id" not in c or c["character_id"] is None:
                raise ValueError(
                    f"Criterion {c['id']!r} is IR.* but missing required "
                    f"character_id field (must match parsed prefix "
                    f"{parsed_char_id!r})"
                )
            if c["character_id"] != parsed_char_id:
                raise ValueError(
                    f"Criterion {c['id']!r} has character_id "
                    f"{c['character_id']!r} that does not match parsed prefix "
                    f"{parsed_char_id!r}"
                )
        elif ac_match:
            # AC.{category}.{handle} — existing v1.1 rules.
            parsed_category = ac_match.group(1)
            if parsed_category not in VALID_CATEGORIES:
                raise ValueError(
                    f"Criterion {c['id']!r} has unknown category "
                    f"{parsed_category!r}; expected one of "
                    f"{sorted(VALID_CATEGORIES)}"
                )
        else:
            raise ValueError(
                f"Criterion {c['id']!r} has malformed id; expected pattern "
                f"AC.<category>.<handle> (Maya) or "
                f"IR.<character_id>.<category>.<handle> (Cy)"
            )

        impact = c.get("impact_tag")
        if impact is not None and impact not in VALID_IMPACT_TAGS:
            raise ValueError(
                f"Criterion {c['id']!r} has unknown impact_tag {impact!r}; "
                f"expected one of {sorted(VALID_IMPACT_TAGS)}"
            )


def enforce_lock(
    criteria_path: Path,
    *,
    force: bool,
    audit_log: Path | None = None,
    actor: str = "",
    reason: str = "",
) -> None:
    """Gate any mutation of the criteria file.

    Raises CriteriaLockViolation if the file is locked and force=False.
    Writes a JSONL audit entry if force=True and audit_log is provided.
    Callers are responsible for the actual write to criteria_path — this
    only gates the decision.
    """
    bundle = load_criteria(criteria_path)
    if not bundle.locked:
        return
    if not force:
        raise CriteriaLockViolation(
            f"{criteria_path} has criteria_locked: true. "
            f"Pass --force-criteria-mutation (with --actor and --reason) to override. "
            f"Forcing logs an audit entry to runs/{{run_id}}/criteria_audit.jsonl."
        )
    if audit_log is not None:
        audit_log.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "actor": actor,
            "reason": reason,
            "criteria_path": str(criteria_path),
            "criteria_version": bundle.version,
            "criteria_count": len(bundle.criteria),
        }
        with audit_log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")


def bump_version(criteria_path: Path, *, new_version: str) -> Path:
    """Write a new semver-bumped criteria file and re-point the symlink.

    criteria_path is expected to be a symlink at
    briefs/{slug}/acceptance_criteria.json pointing at the current versioned
    file (e.g. acceptance_criteria-1.1.0.json). The current target's content
    is read, the version field is replaced with new_version in-place, the
    result is written to acceptance_criteria-{new_version}.json in the same
    directory via temp-then-rename, and the symlink is re-pointed atomically.

    Caller is responsible for writing the audit log entry to
    runs/{run_id}/plan_audit.jsonl — this function only does the file write
    and symlink swap. Per v2 lock (Maya brainstorm TOP-4), audit lives in
    the calling CLI command, not in this primitive.
    """
    raw = json.loads(criteria_path.read_text(encoding="utf-8"))
    raw["version"] = new_version
    versioned_path = criteria_path.parent / f"acceptance_criteria-{new_version}.json"
    tmp_path = versioned_path.with_suffix(versioned_path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    tmp_path.replace(versioned_path)
    # First mutation of a regular-file criteria.json (Cy's Pass-1 write,
    # Maya's Opus emit) converts it to a symlink; subsequent mutations just
    # re-point the symlink. Either path leaves criteria_path resolving to the
    # latest versioned file.
    if criteria_path.is_symlink() or criteria_path.exists():
        criteria_path.unlink()
    criteria_path.symlink_to(versioned_path.name)
    return versioned_path
