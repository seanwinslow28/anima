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
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

Severity = Literal["blocking", "advisory"]
VALID_SEVERITIES = {"blocking", "advisory"}


@dataclass(frozen=True)
class AcceptanceCriterion:
    id: str
    phase: str
    description: str
    severity: Severity


@dataclass
class CriteriaBundle:
    version: str
    locked: bool
    criteria: list[AcceptanceCriterion] = field(default_factory=list)


class CriteriaLockViolation(RuntimeError):
    """Raised when a locked criteria file is being mutated without --force."""


def load_criteria(path: Path) -> CriteriaBundle:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_criteria(raw)
    return CriteriaBundle(
        version=raw["version"],
        locked=bool(raw.get("locked", False)),
        criteria=[
            AcceptanceCriterion(
                id=c["id"],
                phase=c["phase"],
                description=c["description"],
                severity=c["severity"],
            )
            for c in raw["criteria"]
        ],
    )


def validate_criteria(raw: dict) -> None:
    if "version" not in raw:
        raise ValueError("acceptance_criteria.json missing 'version'")
    if "criteria" not in raw or not isinstance(raw["criteria"], list):
        raise ValueError("acceptance_criteria.json missing or malformed 'criteria' list")
    seen: set[str] = set()
    for c in raw["criteria"]:
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
