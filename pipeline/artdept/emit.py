"""emit_artdept_dir — write the Art Department bundle (design §8).

Deterministic and idempotent: same inputs, same bytes. The readiness report
is the honesty artifact — the bundle is Cy-READY only where anchors exist,
the register is authored, and the manifest carries the character; the report
names each gap and the next action. manifest.yaml itself is never touched
(the front door's gap-report discipline, applied one stage later).
"""

from __future__ import annotations

from pathlib import Path

import yaml

from pipeline.artdept.handoff import Handoff
from pipeline.registers import ALL_REGISTERS

BUNDLE_FILES = (
    "design-bible.md",
    "prompt-pack.md",
    "chatgpt-orchestration.md",
    "environment-style.md",
    "cast_list.yaml",
    "artdept.json",
    "cy_readiness_report.md",
)


def emit_artdept_dir(
    out_dir: Path,
    *,
    design_bible_md: str,
    prompt_pack_md: str,
    orchestration_md: str,
    environment_style_md: str,
    cast: dict,
    handoff: Handoff,
    manifest: dict | None = None,
    repo_root: Path | None = None,
) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "design-bible.md").write_text(design_bible_md, encoding="utf-8")
    (out_dir / "prompt-pack.md").write_text(prompt_pack_md, encoding="utf-8")
    (out_dir / "chatgpt-orchestration.md").write_text(orchestration_md, encoding="utf-8")
    (out_dir / "environment-style.md").write_text(environment_style_md, encoding="utf-8")
    (out_dir / "cast_list.yaml").write_text(
        yaml.safe_dump(cast, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    (out_dir / "artdept.json").write_text(handoff.to_json(), encoding="utf-8")
    (out_dir / "cy_readiness_report.md").write_text(
        readiness_report(handoff, cast, manifest, out_dir, repo_root), encoding="utf-8"
    )
    return out_dir


def readiness_report(
    handoff: Handoff,
    cast: dict,
    manifest: dict | None,
    bundle_dir: Path,
    repo_root: Path | None = None,
) -> str:
    repo_root = Path(repo_root) if repo_root is not None else Path(".")
    registered = set((manifest or {}).get("characters") or {})
    designed = [e for e in (cast.get("designed") or []) if isinstance(e, dict)]

    lines = [
        f"# Cy readiness report — {handoff.slug}",
        "",
        "The Art Department emits ratified anchors + a locked register per",
        "designed character. A character is Cy-READY when its anchors are in",
        "`characters/{id}/source-refs/`, its register is in the closed vocabulary,",
        "and it is registered in the manifest `characters:` block. This report",
        "names each remaining gap; the Art Department never mutates manifest.yaml.",
        "",
    ]
    for e in designed:
        cid = e.get("character_id", "?")
        gaps: list[str] = []
        srcdir = repo_root / "characters" / str(cid) / "source-refs"
        if not any((srcdir / Path(a).name).exists() or str(a).startswith(f"characters/{cid}/")
                   for a in (e.get("anchors") or [])):
            gaps.append(
                f"anchors are bundle-local — copy the ratified anchors into `characters/{cid}/source-refs/` "
                "(Cy refuses to author from an empty source-refs/)"
            )
        reg = e.get("style_register")
        if reg not in ALL_REGISTERS:
            gaps.append(
                f"style_register {reg!r} is unauthored — run the style-register authoring "
                "playbook (R→S→B) as the called dependency"
            )
        if cid not in registered:
            gaps.append(
                f"not in manifest `characters:` — after the Bible pass, register `{cid}:` "
                "and its acceptance_criteria.json under `criteria_sources:`"
            )
        if gaps:
            lines.append(f"- **{cid}** ({e.get('display_name', '?')}) — NOT Cy-ready:")
            lines += [f"  {n}. {g}," for n, g in enumerate(gaps, 1)]
            lines.append(
                f"  then: `python scripts/author_bible.py characters/{cid}/ "
                f"--studio-brief \"<from design-bible.md>\" --run-dir runs/<id>/`"
            )
        else:
            lines.append(f"- **{cid}** ({e.get('display_name', '?')}) — registered; Cy-ready.")
    lines.append("")
    return "\n".join(lines)
