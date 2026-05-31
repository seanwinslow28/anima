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
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

import yaml
from PIL import Image

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from pipeline.museum.scraper import scrape_run, walk_runs  # noqa: E402
from pipeline.museum.motion import scrape_motion_plates, motion_loop_pingpong  # noqa: E402
from pipeline.museum.motion_gif import assemble_loop_gif  # noqa: E402
from pipeline.museum.schema import Exhibit, exhibit_dir, write_exhibit, read_exhibit  # noqa: E402
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


def _thumb(src: Path, dest: Path, max_w: int = 400) -> None:
    """Copy an image downscaled to max_w (preserve aspect) and palette-quantized,
    so the committed museum stays light. The full-res original stays in gitignored
    runs/ (and the locked character dir). Opaque images quantize to a 256-color
    PNG (near-lossless for the flat pencil-test palette); images with alpha keep
    their transparency."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        if im.width > max_w:
            h = round(im.height * max_w / im.width)
            im = im.resize((max_w, h))
        has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
        if has_alpha:
            im.save(dest, optimize=True)
        else:
            im.convert("RGB").quantize(colors=256, method=Image.MAXCOVERAGE).save(dest, optimize=True)


def _copy_assets(museum_root: Path, ex: Exhibit, runs_dir: Path) -> int:
    """Copy the images an exhibit needs into its assets/, by kind. Read-only on
    sources — we only ever copy OUT. Returns count copied."""
    dest = exhibit_dir(museum_root, ex) / "assets"
    copied = 0
    if ex.kind == "plate_verdict":
        cdir = _character_dir_for(ex.run_slug)
        if cdir:
            for rel in [p for p in [ex.output, *ex.references] if p]:
                name = Path(rel).name
                matches = ([cdir / "anchor.png"] if name == "anchor.png"
                           else list(cdir.rglob(name)))
                if matches and matches[0].exists():
                    _thumb(matches[0], dest / name)   # light web thumbnail
                    copied += 1
    elif ex.kind == "frame_keyframe":
        adir = runs_dir / ex.run_slug / "approved"
        for rel in ex.frames:
            src = adir / Path(rel).name
            if src.exists():
                _thumb(src, dest / Path(rel).name)   # downscale the heavy keyframes
                copied += 1
    return copied


_PLACEHOLDER = "_(placeholder — Mo not yet run; Phase 3 narrates this.)_\n"


def _write_run_json(museum_root: Path, project_slug: str, run_slug: str,
                    exhibits: list[Exhibit], source: str) -> None:
    kinds = Counter(e.kind for e in exhibits)
    completeness = Counter(e.evidence_completeness for e in exhibits)
    (museum_root / project_slug / run_slug).mkdir(parents=True, exist_ok=True)
    (museum_root / project_slug / run_slug / "run.json").write_text(json.dumps({
        "run_slug": run_slug, "project_slug": project_slug,
        "exhibit_count": len(exhibits), "kinds": dict(kinds),
        "evidence": dict(completeness), "source": source,
    }, indent=2), encoding="utf-8")


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
        # Copy the key sheet + colored frames (light thumbnails) out of the
        # read-only character dir. Sheets are wide multi-frame → allow 720px.
        for rel in ex.references:
            src = motion_plates / Path(rel).name
            if src.exists():
                _thumb(src, dest / src.name, max_w=720)
                total_assets += 1
        for rel in ex.frames:
            src = motion_plates / Path(rel).name
            if src.exists():
                _thumb(src, dest / src.name)
                total_assets += 1
        # Assemble the colored loop GIF beside them — locomotion loops forward,
        # settle motions ping-pong; downscaled so the committed GIF stays light.
        motion_key = ex.exhibit_id.removeprefix("motion-")
        frame_srcs = [motion_plates / Path(f).name for f in ex.frames]
        gif = assemble_loop_gif(frame_srcs, dest / Path(ex.output).name,
                                pingpong=motion_loop_pingpong(motion_key), max_w=480)
        if gif:
            total_assets += 1
        print(f"[museum] {ex.exhibit_id}: {len(ex.frames)} frames"
              f"{' + loop.gif' if gif else ''}")

    print(f"[museum] motion batch -> {project_slug}/{run_slug}: "
          f"{len(exhibits)} exhibits, {total_assets} assets")
    return exhibits


def build_all(runs_dir: Path, museum_root: Path, manifest_path: Path) -> dict:
    """Full backfill: walk every run, noise-filter (logged), scrape, write
    exhibits + assets + run.json, and emit per-project project.json. Read-only on
    runs/. Returns a summary dict."""
    cfg = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    museum_cfg = cfg.get("museum") or {}
    slug_rules = {slug: (spec.get("match") or [])
                  for slug, spec in (museum_cfg.get("project_slugs") or {}).items()}
    titles = {slug: spec.get("title", slug)
              for slug, spec in (museum_cfg.get("project_slugs") or {}).items()}

    kept, filtered = walk_runs(runs_dir, museum_cfg.get("noise_filter") or {})
    print(f"[museum] {len(kept)} runs kept, {len(filtered)} filtered:")
    for name, reason in filtered:
        print(f"[museum]   skip {name}: {reason}")

    project_runs: dict[str, list[tuple[str, int]]] = {}
    totals: dict[str, int] = {}
    for run_dir in kept:
        slug, exhibits = scrape_run(run_dir, slug_rules)
        if not exhibits:
            # Kept by the noise filter (had a marker dir/file) but no structured
            # evidence to synthesize — honestly empty, so no stray run in the tree.
            print(f"[museum] {run_dir.name} -> {slug}: 0 exhibits (skipped, empty)")
            continue
        for ex in exhibits:
            write_exhibit(museum_root, ex)
            _copy_assets(museum_root, ex, runs_dir)
        _write_run_json(museum_root, slug, run_dir.name, exhibits, f"runs/{run_dir.name}/")
        project_runs.setdefault(slug, []).append((run_dir.name, len(exhibits)))
        totals[slug] = totals.get(slug, 0) + len(exhibits)
        print(f"[museum] {run_dir.name} -> {slug}: {len(exhibits)} exhibits")

    # Also fold in any character's motion comparison batch.
    for cdir in sorted((REPO / "characters").glob("*/motion-additions.json")):
        cid = cdir.parent.name
        ms = build_motion(museum_root, cid, "2026-05-30-mascot-motion-ingest", manifest_path)
        slug = ms[0].project_slug if ms else "character-bible"
        project_runs.setdefault(slug, [])
        if not any(r == "2026-05-30-mascot-motion-ingest" for r, _ in project_runs[slug]):
            project_runs[slug].append(("2026-05-30-mascot-motion-ingest", len(ms)))
        totals[slug] = totals.get(slug, 0) + len(ms)

    for slug, runs in project_runs.items():
        (museum_root / slug).mkdir(parents=True, exist_ok=True)
        (museum_root / slug / "project.json").write_text(json.dumps({
            "project_slug": slug, "title": titles.get(slug, slug),
            "run_count": len(runs), "exhibit_count": totals.get(slug, 0),
            "runs": sorted({r: n for r, n in runs}.items()),
        }, indent=2), encoding="utf-8")

    print(f"[museum] backfill complete: "
          + ", ".join(f"{s}={totals[s]}" for s in sorted(totals)))
    return {"kept": [p.name for p in kept], "filtered": filtered, "totals": totals}


def narrate_all(museum_root: Path) -> dict:
    """Run Mo over every scraped exhibit, replacing the auto-generated exhibit.md
    with her docent narration. Credential-free via Mo's faithful local fallback."""
    from pipeline.agents.museum_writer import narrate
    count = stub = 0
    for json_path in sorted(Path(museum_root).rglob("exhibits/*/exhibit.json")):
        ex = read_exhibit(json_path)
        prose, used_stub = narrate(ex)
        (json_path.parent / "exhibit.md").write_text(prose, encoding="utf-8")
        count += 1
        stub += int(used_stub)
    mode = "all stub (no SDK)" if stub == count else f"{count - stub} via Sonnet, {stub} stub"
    print(f"[museum] Mo narrated {count} exhibits — {mode}")
    return {"narrated": count, "stub": stub}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build the standalone anima Museum.")
    ap.add_argument("--runs", default="runs/", type=Path)
    ap.add_argument("--all", action="store_true", help="full backfill across all of runs/")
    ap.add_argument("--only", help="single run directory name to scrape (JSONL artifacts)")
    ap.add_argument("--motion", help="character id — build the motion comparison batch")
    ap.add_argument("--motion-run", default="2026-05-30-mascot-motion-ingest",
                    help="run slug the motion keys were ingested under")
    ap.add_argument("--museum", default="museum/", type=Path)
    ap.add_argument("--manifest", default=REPO / "manifest.yaml", type=Path)
    ap.add_argument("--narrate", action="store_true", help="run Mo over scraped exhibits")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--site", default="museum/_site/", type=Path)
    args = ap.parse_args(argv)

    if not any([args.all, args.only, args.motion, args.narrate, args.render]):
        ap.error("pass at least one of --all / --only / --motion / --narrate / --render")

    museum_root = Path(args.museum)
    if args.all:
        build_all(Path(args.runs), museum_root, Path(args.manifest))
    if args.only:
        build(Path(args.runs), args.only, museum_root, Path(args.manifest))
    if args.motion:
        build_motion(museum_root, args.motion, args.motion_run, Path(args.manifest))
    if args.narrate:
        narrate_all(museum_root)

    if args.render:
        index = render_static(museum_root, Path(args.site))
        print(f"[museum] rendered -> file://{index.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
