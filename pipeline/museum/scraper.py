"""Read-only retroactive scraper — synthesizes exhibits from on-disk evidence.

This is the minimal slice: it reads the two richest evidence layers every Cy
bake already leaves behind — `plate_verdicts.jsonl` (the DINOv2→CLIP→PIL +
Gemini verdict trail) and `bible_audit.jsonl` (the mutate / add / iterate log)
— and turns each line into an Exhibit (the schema is the contract). Phase 2
generalizes this to walk all of runs/, add the Seedance + early-audit readers,
and apply the noise-filter.

STRICTLY READ-ONLY against runs/ and the locked Bibles. It synthesizes new
artifacts under museum/; it does not mutate a single byte of run history.
"""

from __future__ import annotations

import json
from pathlib import Path

from pipeline.museum.schema import Exhibit, Decision, Verdict, derive_project_slug

# plate_verdicts.jsonl `status` values map through to Decision.outcome. The
# identity map is explicit so an unexpected status surfaces as itself rather
# than being silently coerced.
_OUTCOME_FROM_STATUS = {
    "pass": "pass", "fail": "fail", "borderline": "borderline",
    "ingested": "ingested", "human_gate_required": "human_gate_required",
}


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def _date_from_run_slug(run_slug: str) -> str | None:
    head = run_slug[:10]
    return head if head[:4].isdigit() and head.count("-") == 2 else None


def scrape_plate_verdicts(run_dir: Path, project_slug: str, run_slug: str) -> list[Exhibit]:
    rows = _read_jsonl(Path(run_dir) / "plate_verdicts.jsonl")
    date = _date_from_run_slug(run_slug)
    exhibits: list[Exhibit] = []
    for i, r in enumerate(rows, start=1):
        target = r.get("target_path", f"plate-{i}")
        handle = target.replace("/", "-").rsplit(".", 1)[0]
        reasoning = (r.get("reasoning") or "").strip()
        exhibits.append(Exhibit(
            exhibit_id=f"{i:02d}-{handle}",
            project_slug=project_slug, run_slug=run_slug,
            title=f"Plate — {target}", kind="plate_verdict",
            phase=2, persona="cy", date=date,
            decision=Decision(
                outcome=_OUTCOME_FROM_STATUS.get(r.get("status", ""), r.get("status", "unknown")),
                attempts=r.get("attempts"),
                rationale=reasoning,
                rationale_source="plate_verdicts.jsonl" if reasoning else None,
            ),
            output=f"assets/{Path(target).name}",
            references=["assets/anchor.png"],
            verdict=Verdict(
                method=r.get("similarity_method"),
                score=r.get("similarity_score"),
                reference=r.get("similarity_reference"),
                model_verdict=r.get("gemini_verdict"),
                model_confidence=r.get("gemini_confidence"),
            ),
            cites_criteria=list(r.get("cites_identity_rule") or []),
            evidence_completeness="rich" if reasoning else "partial",
            source_paths=[f"runs/{run_slug}/plate_verdicts.jsonl#L{i}"],
        ))
    return exhibits


def scrape_bible_audit(run_dir: Path, project_slug: str, run_slug: str) -> list[Exhibit]:
    rows = _read_jsonl(Path(run_dir) / "bible_audit.jsonl")
    date = _date_from_run_slug(run_slug)
    exhibits: list[Exhibit] = []
    for i, r in enumerate(rows, start=1):
        is_add = r.get("kind") == "add"
        if is_add:
            cites = list(r.get("added_rule_ids") or [])
            title = f"Bible add — {len(r.get('added_plate_paths') or [])} plates"
            kind, outcome = "bible_add", "added"
        else:
            cites = [r["target"]] if r.get("target") else []
            title = f"Bible mutation — {r.get('target', 'rule')}"
            kind, outcome = "bible_mutation", "mutated"
        exhibits.append(Exhibit(
            exhibit_id=f"audit-{i:02d}-{kind}",
            project_slug=project_slug, run_slug=run_slug,
            title=title, kind=kind, phase=2, persona="human", date=date,
            decision=Decision(outcome=outcome, rationale=(r.get("reason") or "").strip(),
                              rationale_source="bible_audit.jsonl" if r.get("reason") else None),
            cites_criteria=cites,
            evidence_completeness="rich" if r.get("reason") else "partial",
            source_paths=[f"runs/{run_slug}/bible_audit.jsonl#L{i}"],
        ))
    return exhibits


def scrape_run(run_dir: Path, slug_rules: dict[str, list[str]]) -> tuple[str, list[Exhibit]]:
    run_dir = Path(run_dir)
    run_slug = run_dir.name
    slug = derive_project_slug(run_slug, slug_rules) or "_unclassified"
    exhibits = (scrape_plate_verdicts(run_dir, slug, run_slug)
                + scrape_bible_audit(run_dir, slug, run_slug))
    return slug, exhibits
