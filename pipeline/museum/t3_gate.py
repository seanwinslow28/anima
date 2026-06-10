"""The T3 council `pre_museum` gate — runs the council over assembled exhibits
BEFORE the static site renders, and blocks the publish on a `fail` adjudication.

Placement is locked in manifest.yaml (`critics.placement.pre_museum_publish: T3`).
The council engine (pipeline/agents/t3_council.T3CouncilNode) is gate-agnostic, so
this module is *wiring + input-prep*, not engine logic: it maps each on-disk
exhibit to the council's input contract (artifact_paths / beat_description /
frame_id / checkpoint / gate), runs the council, stages any proposed patches via
the existing stage_patches_hook (auto_apply: false — never auto-apply), and rolls
the per-exhibit verdicts up into a single gate decision.

Gate semantics (per the Session B plan):
  - chairman `fail`, OR all-peers-errored (council status == "error") → BLOCK render.
  - `borderline` → surface, but proceed (a human call).
  - `pass` → proceed.

Read-only against the exhibits' images: the council reads them, never writes them.
The only writes are the staged-patches lock under the gate's own run_dir.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from pipeline.agents import AgentContext
from pipeline.agents.patch_stager import stage_patches_hook, read_staged_patches
from pipeline.agents.t3_council import T3CouncilNode
from pipeline.museum.schema import Exhibit, read_exhibit

GATE_NAME = "pre_museum_publish"
_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
_VIDEO_SUFFIXES = {".mp4", ".webm", ".mov", ".gif"}


@dataclass
class ExhibitVerdict:
    exhibit_id: str
    project_slug: str
    verdict: str
    status: str
    agreement_score: float
    chairman_note: str
    peer_verdicts: dict[str, Any]
    n_artifacts: int


@dataclass
class GateResult:
    blocked: bool
    exhibits_reviewed: int
    results: list[ExhibitVerdict] = field(default_factory=list)
    staged_patches: int = 0
    run_dir: Path | None = None

    @property
    def blocking_exhibits(self) -> list[ExhibitVerdict]:
        return [r for r in self.results if r.verdict == "fail" or r.status == "error"]


def _resolve_artifacts(ex: Exhibit, ex_dir: Path) -> list[Path]:
    """Map an exhibit's referenced images to absolute paths the council can read.

    Prefers the declared output + references + frames; falls back to globbing the
    exhibit's assets/ dir so a thinly-recorded exhibit still gets reviewed. Videos
    are kept — the council reduces them to a contact sheet itself."""
    rels: list[str] = []
    if ex.output:
        rels.append(ex.output)
    rels.extend(ex.references or [])
    rels.extend(ex.frames or [])

    seen: set[Path] = set()
    out: list[Path] = []
    for rel in rels:
        p = (ex_dir / rel).resolve()
        if p in seen:
            continue
        if p.exists() and p.suffix.lower() in (_IMAGE_SUFFIXES | _VIDEO_SUFFIXES):
            seen.add(p)
            out.append(p)

    if not out:
        assets = ex_dir / "assets"
        if assets.is_dir():
            for p in sorted(assets.iterdir()):
                if p.suffix.lower() in (_IMAGE_SUFFIXES | _VIDEO_SUFFIXES):
                    out.append(p.resolve())
    return out


def _beat_description(ex: Exhibit) -> str:
    """A faithful context bundle for the council — never invents narrative. Folds
    the exhibit title, kind/outcome, and the (possibly-empty) recorded rationale."""
    parts = [f"Exhibit: {ex.title}", f"kind: {ex.kind} | outcome: {ex.decision.outcome}"]
    if ex.persona:
        parts.append(f"decided by: {ex.persona}")
    rationale = (ex.decision.rationale or "").strip()
    parts.append(f"recorded rationale: {rationale}" if rationale
                 else "recorded rationale: (none on disk — thin exhibit, do not invent one)")
    return "\n".join(parts)


def t3_council_gate(
    museum_root: Path,
    manifest_path: Path,
    *,
    run_dir: Path | None = None,
    limit: int | None = None,
    project_slug: str | None = None,
) -> GateResult:
    """Run the T3 council over the assembled exhibits and return the gate decision.

    Args:
        museum_root: the museum tree root (holds {project}/{run}/exhibits/*).
        manifest_path: manifest.yaml — supplies critics.t3 (per_call_timeout_s etc).
        run_dir: where staged patches land (manifest.lock.yaml); defaults to
                 museum_root/"_t3_gate". Never inside the published tree's exhibits.
        limit: cap the number of exhibits reviewed (smoke/cost control). None = all.
        project_slug: restrict to one project_slug subtree. None = whole museum.
    """
    museum_root = Path(museum_root)
    manifest = yaml.safe_load(Path(manifest_path).read_text(encoding="utf-8")) or {}

    run_dir = Path(run_dir) if run_dir else (museum_root / "_t3_gate")
    run_dir.mkdir(parents=True, exist_ok=True)
    hook = stage_patches_hook(run_dir)

    search_root = museum_root / project_slug if project_slug else museum_root
    exhibit_jsons = sorted(search_root.rglob("exhibits/*/exhibit.json"))
    if limit is not None:
        exhibit_jsons = exhibit_jsons[:limit]

    node = T3CouncilNode()
    results: list[ExhibitVerdict] = []

    for json_path in exhibit_jsons:
        ex = read_exhibit(json_path)
        ex_dir = json_path.parent
        artifacts = _resolve_artifacts(ex, ex_dir)

        ctx = AgentContext(
            run_dir=run_dir,
            inputs={
                "artifact_paths": [str(p) for p in artifacts],
                "beat_description": _beat_description(ex),
                "frame_id": ex.exhibit_id,
                "checkpoint": GATE_NAME,
                "gate": GATE_NAME,
            },
            manifest=manifest,
            criteria=None,
            tier="draft",
            cache_dir=run_dir / ".cache",
        )
        result = node.run(ctx)
        hook(f"t3_council:{ex.exhibit_id}", result)

        out = result.outputs
        results.append(ExhibitVerdict(
            exhibit_id=ex.exhibit_id,
            project_slug=ex.project_slug,
            verdict=str(out.get("verdict", "borderline")),
            status=str(out.get("status", "error")),
            agreement_score=float(out.get("agreement_score", 0.0)),
            chairman_note=str(out.get("chairman_note", "")),
            peer_verdicts=dict(out.get("peer_verdicts", {})),
            n_artifacts=len(artifacts),
        ))

    blocked = any(r.verdict == "fail" or r.status == "error" for r in results)
    return GateResult(
        blocked=blocked,
        exhibits_reviewed=len(results),
        results=results,
        staged_patches=len(read_staged_patches(run_dir)),
        run_dir=run_dir,
    )
