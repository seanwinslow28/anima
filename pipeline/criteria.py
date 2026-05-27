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

# Mnemonic ID pattern: AC.{category}.{handle}. Category is one of the closed
# vocab above; handle is kebab-or-snake lowercase. Em's escalation hatch keys
# off impact_tag (not the ID parse), so handle stays flexible.
_MNEMONIC_ID_PATTERN = re.compile(r"^AC\.([a-z_]+)\.([a-z0-9\-]+)$")


@dataclass(frozen=True)
class AcceptanceCriterion:
    """One criterion. Polymorphic over schema version.

    v1.0 records carry `phase` and `severity`; v1.1 fields default to empty.
    v1.1 records carry the graph fields; v1.0 fields default to None.
    Consumers that only care about one version inspect the relevant fields.
    """
    id: str
    description: str
    # v1.0 fields (None on v1.1 records).
    phase: str | None = None
    severity: Severity | None = None
    # v1.1 graph fields (empty / None on v1.0 records).
    cites_phase: tuple[int, ...] = ()
    cites_personas: tuple[str, ...] = ()
    impact_tag: str | None = None
    parent_id: str | None = None
    derived_from: tuple[str, ...] = ()


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
            criteria_list.append(AcceptanceCriterion(
                id=c["id"],
                description=c["description"],
                cites_phase=tuple(c.get("cites_phase") or ()),
                cites_personas=tuple(c.get("cites_personas") or ()),
                impact_tag=c.get("impact_tag"),
                parent_id=c.get("parent_id"),
                derived_from=tuple(c.get("derived_from") or ()),
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
    elif version.startswith("1.1") or version.startswith("1.2"):
        _validate_v1_1(raw["criteria"])
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
    if criteria_path.is_symlink():
        criteria_path.unlink()
    criteria_path.symlink_to(versioned_path.name)
    return versioned_path
