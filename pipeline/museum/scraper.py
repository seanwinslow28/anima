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
import re
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
    # First YYYY-MM-DD anywhere in the slug (handles `run_2026-04-04_…` too).
    m = re.search(r"\d{4}-\d{2}-\d{2}", run_slug)
    return m.group(0) if m else None


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
            # No anchor reference: plate-vs-anchor is the boring "AI matched the
            # reference" comparison. The anchor it was scored against is recorded
            # in verdict.reference; the page shows the plate + its verdict.
            references=[],
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


def scrape_seedance(run_dir: Path, project_slug: str, run_slug: str) -> list[Exhibit]:
    """Per-shot Seedance `*.meta.json` → one seedance_shot exhibit. The prompt +
    seed + tier + timing IS the artifact (the prompt-engineering discipline); the
    video itself is large and not copied into the museum. No critique was logged
    on these shots, so they are honestly `partial` (generated, not gated)."""
    sdir = Path(run_dir) / "seedance"
    if not sdir.is_dir():
        return []
    date = _date_from_run_slug(run_slug)
    exhibits: list[Exhibit] = []
    for meta_path in sorted(sdir.glob("*.meta.json")):
        m = json.loads(meta_path.read_text(encoding="utf-8"))
        shot = m.get("shot_id", meta_path.stem)
        tier = m.get("tier", "?")
        exhibits.append(Exhibit(
            exhibit_id=f"seedance-{shot}-{m.get('attempt', 1):02d}",
            project_slug=project_slug, run_slug=run_slug,
            title=f"Seedance shot {shot} ({tier})", kind="seedance_shot",
            phase=6, persona=None, date=date,
            decision=Decision(outcome="generated", attempts=m.get("attempt"),
                              rationale="", rationale_source=None),
            prompt=m.get("prompt"),
            verdict=None,
            cites_criteria=[],
            evidence_completeness="partial",
            source_paths=[f"runs/{run_slug}/seedance/{meta_path.name}"],
        ))
    return exhibits


_FRAME_EXTS = (".png", ".jpg", ".jpeg", ".gif")


def scrape_approved_keyframes(run_dir: Path, project_slug: str, run_slug: str) -> list[Exhibit]:
    """ONE rollup exhibit per run for its approved/ keyframes — the frame strip,
    not 30 near-identical thin pages. The approval is real evidence (a human kept
    these), but no rationale is logged on disk, so the exhibit is honestly thin."""
    adir = Path(run_dir) / "approved"
    if not adir.is_dir():
        return []
    frames = sorted(p.name for p in adir.iterdir()
                    if p.is_file() and p.suffix.lower() in _FRAME_EXTS)
    if not frames:
        return []
    date = _date_from_run_slug(run_slug)
    return [Exhibit(
        exhibit_id="approved-keyframes",
        project_slug=project_slug, run_slug=run_slug,
        title=f"Approved keyframes ({len(frames)})", kind="frame_keyframe",
        phase=5, persona="human", date=date,
        decision=Decision(outcome="approved", rationale="", rationale_source=None),
        frames=[f"assets/{n}" for n in frames],
        evidence_completeness="thin",
        source_paths=[f"runs/{run_slug}/approved/"],
    )]


def scrape_run(run_dir: Path, slug_rules: dict[str, list[str]]) -> tuple[str, list[Exhibit]]:
    run_dir = Path(run_dir)
    run_slug = run_dir.name
    slug = derive_project_slug(run_slug, slug_rules) or "_unclassified"
    exhibits = (scrape_plate_verdicts(run_dir, slug, run_slug)
                + scrape_bible_audit(run_dir, slug, run_slug)
                + scrape_seedance(run_dir, slug, run_slug)
                + scrape_approved_keyframes(run_dir, slug, run_slug))
    return slug, exhibits


def walk_runs(runs_dir: Path, noise_filter: dict) -> tuple[list[Path], list[tuple[str, str]]]:
    """Return (kept run dirs, [(name, skip_reason), …]).

    The noise filter is honest and logged — every skipped entry comes back with a
    reason so nothing is silently truncated. Skips: any file (incl. `*.log`),
    install runs, and *aborted* dirs (no decision evidence at all: no approved/,
    no plate_verdicts.jsonl, no bible_audit.jsonl, no seedance/)."""
    runs_dir = Path(runs_dir)
    skip_suffixes = tuple(noise_filter.get("skip_suffixes", []))
    skip_contains = list(noise_filter.get("skip_name_contains", []))
    kept: list[Path] = []
    filtered: list[tuple[str, str]] = []
    for entry in sorted(runs_dir.iterdir()):
        name = entry.name
        if name.startswith("."):
            continue
        if entry.is_file():
            reason = "log file" if name.endswith(skip_suffixes) else "not a run directory"
            filtered.append((name, reason))
            continue
        if any(s in name for s in skip_contains):
            filtered.append((name, "install run"))
            continue
        aborted = not any((entry / n).exists() for n in
                          ("approved", "plate_verdicts.jsonl", "bible_audit.jsonl", "seedance"))
        if aborted:
            filtered.append((name, "aborted — no decision evidence on disk"))
            continue
        kept.append(entry)
    return kept, filtered
