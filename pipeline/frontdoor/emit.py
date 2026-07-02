"""emit_brief_dir — write the front-door bundle (§4, §8 step 4).

Deterministic and idempotent: same inputs, same bytes. The gap report is the
A5 honesty artifact — the front door's output is Maya-ready, not
GENERATE-ready; the report names each seed character not registered in the
manifest and the next Cy action. manifest.yaml itself is never touched.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from pipeline.frontdoor.handoff import Handoff

BUNDLE_FILES = (
    "00_studio_brief.md",
    "concept.md",
    "character_seeds.yaml",
    "frontdoor.json",
    "manifest_gap_report.md",
)


def emit_brief_dir(
    out_dir: Path,
    *,
    studio_brief_md: str,
    concept_md: str,
    seeds: list[dict],
    handoff: Handoff,
    manifest: dict | None = None,
) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "00_studio_brief.md").write_text(studio_brief_md, encoding="utf-8")
    (out_dir / "concept.md").write_text(concept_md, encoding="utf-8")
    (out_dir / "character_seeds.yaml").write_text(
        yaml.safe_dump(seeds, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    (out_dir / "frontdoor.json").write_text(handoff.to_json(), encoding="utf-8")
    (out_dir / "manifest_gap_report.md").write_text(
        gap_report(handoff, seeds, manifest), encoding="utf-8"
    )
    return out_dir


def gap_report(handoff: Handoff, seeds: list[dict], manifest: dict | None) -> str:
    registered = set((manifest or {}).get("characters") or {})
    gaps = [s for s in seeds if s["character_id"] not in registered]
    done = [s for s in seeds if s["character_id"] in registered]

    lines = [
        f"# Manifest gap report — {handoff.slug}",
        "",
        "The front door emits character *seeds*, not Bibles. This brief is",
        "Maya-ready now; a NEW character is not GENERATE-ready until Cy authors",
        "its Bible and it is registered in the manifest `characters:` block.",
        "The front door never mutates manifest.yaml (a source-of-truth file).",
        "",
        f"## Unregistered characters ({len(gaps)})",
        "",
    ]
    if gaps:
        for s in gaps:
            cid = s["character_id"]
            target = s.get("cy_target_dir") or f"characters/{cid}/"
            lines += [
                f"- **{cid}** ({s['display_name']}) — not in manifest `characters:`. Next Cy action:",
                f"  1. populate `{target}source-refs/` from the seed's `source_notes`"
                " (Cy refuses to author from an empty source-refs/),",
                f"  2. `python scripts/author_bible.py {target} --studio-brief \"<from the seed>\""
                " --run-dir runs/<id>/`,",
                f"  3. register `{cid}:` under manifest `characters:` and its"
                " acceptance_criteria.json under `criteria_sources:`.",
            ]
    else:
        lines.append("- none — every seed character is registered.")
    lines += ["", f"## Registered characters ({len(done)})", ""]
    if done:
        for s in done:
            lines.append(f"- {s['character_id']} ({s['display_name']}) — registered.")
    else:
        lines.append("- none.")
    lines.append("")
    return "\n".join(lines)
