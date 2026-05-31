#!/usr/bin/env python3
"""Build the standalone Museum from on-disk run evidence.

Mirrors scripts/author_bible.py structurally: a thin orchestrator over the
museum package. This first cut scrapes one run (the vertical slice), copies the
referenced images READ-ONLY out of runs/ + characters/ into the museum tree, and
renders a self-contained static site.

  python scripts/build_museum.py \
      --runs runs/ --only 2026-05-30-cy-claude-mascot-pencil-bake \
      --museum museum/ --render --site museum/_site/

Strictly read-only against runs/ and the locked Bibles: it copies assets OUT,
never mutates a byte of run history or any acceptance_criteria.json. Phase 2
generalizes --only into a full-breadth walk with the manifest noise-filter;
Phase 3 adds --narrate (Mo).
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from pipeline.museum.scraper import scrape_run  # noqa: E402
from pipeline.museum.motion import scrape_motion_plates  # noqa: E402
from pipeline.museum.motion_gif import assemble_loop_gif  # noqa: E402
from pipeline.museum.schema import Exhibit, exhibit_dir, write_exhibit  # noqa: E402
from pipeline.museum.render import render_static  # noqa: E402


def _slug_rules(manifest_path: Path) -> dict[str, list[str]]:
    cfg = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    slugs = (cfg.get("museum") or {}).get("project_slugs") or {}
    return {slug: (spec.get("match") or []) for slug, spec in slugs.items()}


def _character_dir_for(run_slug: str) -> Path | None:
    """Find the character whose id appears in the run slug (skip _archive)."""
    chars = REPO / "characters"
    if not chars.is_dir():
        return None
    for d in sorted(chars.iterdir()):
        if d.is_dir() and not d.name.startswith("_") and d.name in run_slug:
            return d
    return None


def _copy_exhibit_assets(museum_root: Path, ex: Exhibit, character_dir: Path | None) -> int:
    """Copy the images an exhibit references into its assets/ dir. Returns the
    count copied. Sources are read-only; we only ever copy OUT."""
    if character_dir is None:
        return 0
    dest = exhibit_dir(museum_root, ex) / "assets"
    copied = 0
    wanted = [p for p in [ex.output, *ex.references] if p]
    for rel in wanted:
        name = Path(rel).name
        # anchor.png lives at the character root; plates live in subdirs.
        if name == "anchor.png":
            src = character_dir / "anchor.png"
            matches = [src] if src.exists() else []
        else:
            matches = list(character_dir.rglob(name))
        if matches:
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy2(matches[0], dest / name)
            copied += 1
    return copied


_PLACEHOLDER = "_(placeholder — Mo not yet run; Phase 3 narrates this.)_\n"


def build(runs_dir: Path, only: str, museum_root: Path, manifest_path: Path) -> tuple[str, list[Exhibit]]:
    run_dir = runs_dir / only
    if not run_dir.is_dir():
        raise SystemExit(f"run not found: {run_dir}")
    slug_rules = _slug_rules(manifest_path)
    slug, exhibits = scrape_run(run_dir, slug_rules)
    character_dir = _character_dir_for(only)

    # Per-project + per-run narrative placeholders (Mo replaces them in Phase 3).
    (museum_root / slug).mkdir(parents=True, exist_ok=True)
    (museum_root / slug / "project.md").write_text(
        f"# {slug}\n\n{_PLACEHOLDER}", encoding="utf-8")
    (museum_root / slug / only).mkdir(parents=True, exist_ok=True)
    (museum_root / slug / only / "run.md").write_text(
        f"# {only}\n\n{len(exhibits)} exhibits scraped from on-disk evidence.\n\n{_PLACEHOLDER}",
        encoding="utf-8")

    total_assets = 0
    for ex in exhibits:
        write_exhibit(museum_root, ex)
        total_assets += _copy_exhibit_assets(museum_root, ex, character_dir)

    print(f"[museum] {only} -> {slug}: {len(exhibits)} exhibits, {total_assets} assets copied")
    return slug, exhibits


def build_motion(museum_root: Path, character_id: str, run_slug: str, manifest_path: Path) -> list[Exhibit]:
    """Build the motion comparison batch for a character — the signature artifact.

    For each motion: write the exhibit, copy the hand-drawn key sheet + the colored
    frames out of the (read-only) character dir, and assemble the colored frames into
    a looping GIF beside them.
    """
    character_dir = REPO / "characters" / character_id
    motion_plates = character_dir / "motion_plates"
    slug_rules = _slug_rules(manifest_path)
    from pipeline.museum.schema import derive_project_slug
    project_slug = derive_project_slug(run_slug, slug_rules) or "_unclassified"

    exhibits = scrape_motion_plates(character_dir, project_slug, run_slug)
    if not exhibits:
        raise SystemExit(f"no motion-additions.json under {character_dir}")

    (museum_root / project_slug / run_slug).mkdir(parents=True, exist_ok=True)
    (museum_root / project_slug / run_slug / "run.md").write_text(
        f"# {run_slug}\n\nHand-drawn motion keys → colored animatic frames "
        f"({len(exhibits)} motions).\n\n{_PLACEHOLDER}", encoding="utf-8")

    total_assets = 0
    for ex in exhibits:
        write_exhibit(museum_root, ex)
        dest = exhibit_dir(museum_root, ex) / "assets"
        dest.mkdir(parents=True, exist_ok=True)
        # Copy the key sheet + colored frames out of the read-only character dir.
        for rel in [*ex.references, *ex.frames]:
            src = motion_plates / Path(rel).name
            if src.exists():
                shutil.copy2(src, dest / src.name)
                total_assets += 1
        # Assemble the colored loop GIF beside them.
        frame_srcs = [motion_plates / Path(f).name for f in ex.frames]
        gif = assemble_loop_gif(frame_srcs, dest / Path(ex.output).name)
        if gif:
            total_assets += 1
        print(f"[museum] {ex.exhibit_id}: {len(ex.frames)} frames"
              f"{' + loop.gif' if gif else ''}")

    print(f"[museum] motion batch -> {project_slug}/{run_slug}: "
          f"{len(exhibits)} exhibits, {total_assets} assets")
    return exhibits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build the standalone anima Museum.")
    ap.add_argument("--runs", default="runs/", type=Path)
    ap.add_argument("--only", help="single run directory name to scrape (JSONL artifacts)")
    ap.add_argument("--motion", help="character id — build the motion comparison batch")
    ap.add_argument("--motion-run", default="2026-05-30-mascot-motion-ingest",
                    help="run slug the motion keys were ingested under")
    ap.add_argument("--museum", default="museum/", type=Path)
    ap.add_argument("--manifest", default=REPO / "manifest.yaml", type=Path)
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--site", default="museum/_site/", type=Path)
    args = ap.parse_args(argv)

    if not args.only and not args.motion:
        ap.error("pass --only <run> and/or --motion <character_id>")

    museum_root = Path(args.museum)
    if args.only:
        build(Path(args.runs), args.only, museum_root, Path(args.manifest))
    if args.motion:
        build_motion(museum_root, args.motion, args.motion_run, Path(args.manifest))

    if args.render:
        index = render_static(museum_root, Path(args.site))
        print(f"[museum] rendered -> file://{index.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
