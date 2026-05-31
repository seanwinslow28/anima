"""Self-contained static HTML renderer (Phase 1 throwaway).

Walks a museum/ tree and emits a browsable static site: an index of projects →
runs → exhibits, plus one page per exhibit. No framework, no CDN, no build step
— it opens by double-clicking a file. Phase 5 promotes this to the finished
pass (Mo's prose, comparison GIFs inline, real markdown→HTML); this first cut
exists only to prove the slice renders and reads as the real story.

Self-containment is asserted in the test: the emitted HTML carries no external
URL the museum can't survive offline.
"""

from __future__ import annotations

import html
import shutil
from pathlib import Path

from pipeline.museum.schema import Exhibit, read_exhibit

_CSS = """
:root { --ink:#2b2b2b; --paper:#faf5e8; --line:#cdb; --muted:#6b6b6b; }
* { box-sizing: border-box; }
body { background: var(--paper); color: var(--ink); font: 16px/1.6 -apple-system, Helvetica, Arial, sans-serif;
       margin: 0; padding: 2rem; max-width: 880px; margin-inline: auto; }
h1 { font-size: 1.7rem; margin: 0 0 .25rem; }
h2 { font-size: 1.15rem; margin: 1.6rem 0 .4rem; border-bottom: 1px solid #ddd2bb; padding-bottom: .2rem; }
a { color: #8a5a2b; }
.meta { color: var(--muted); font-size: .9rem; margin: 0 0 1rem; }
.pill { display: inline-block; padding: .05rem .5rem; border-radius: 1rem; font-size: .78rem;
        border: 1px solid #d8c9a8; margin-right: .35rem; }
.pass { background: #e6f3e6; } .fail { background: #f6e3e3; } .borderline { background: #f6efdd; }
.exhibit-list { list-style: none; padding: 0; }
.exhibit-list li { padding: .35rem 0; border-bottom: 1px dotted #ddd2bb; }
.score { font-variant-numeric: tabular-nums; }
img { max-width: 100%; border: 1px solid #ddd2bb; background: #fff; margin: .4rem 0; }
.cites code { background: #efe7d2; padding: .05rem .3rem; border-radius: .2rem; }
.thin { color: var(--muted); font-style: italic; }
footer { margin-top: 3rem; color: var(--muted); font-size: .82rem; }
"""


def _page(title: str, body: str) -> str:
    return (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{html.escape(title)}</title><style>{_CSS}</style></head>"
        f"<body>{body}"
        "<footer>anima Museum — generated from on-disk run evidence. "
        "The repo carries its receipts.</footer></body></html>"
    )


def _outcome_class(outcome: str) -> str:
    return outcome if outcome in {"pass", "fail", "borderline"} else ""


def _exhibit_page(ex: Exhibit) -> str:
    parts = [f"<p><a href=\"../../../../index.html\">← all projects</a></p>",
             f"<h1>{html.escape(ex.title)}</h1>"]
    meta = [f"<span class=\"pill {_outcome_class(ex.decision.outcome)}\">{html.escape(ex.decision.outcome)}</span>",
            f"<span class=\"pill\">{html.escape(ex.kind)}</span>"]
    if ex.persona:
        meta.append(f"decided by <strong>{html.escape(ex.persona)}</strong>")
    if ex.date:
        meta.append(html.escape(ex.date))
    if ex.verdict and ex.verdict.score is not None:
        meta.append(f"<span class=\"score\">{html.escape(ex.verdict.method or 'similarity')} "
                    f"{ex.verdict.score}</span>")
    parts.append(f"<p class=\"meta\">{' · '.join(meta)}</p>")

    # Images — output + references that were copied alongside this page.
    for img in [ex.output, *ex.references]:
        if img:
            parts.append(f"<img src=\"{html.escape(img)}\" alt=\"{html.escape(img)}\">")

    parts.append("<h2>Rationale</h2>")
    if ex.decision.rationale.strip():
        parts.append(f"<p>{html.escape(ex.decision.rationale.strip())}</p>")
        if ex.decision.rationale_source:
            parts.append(f"<p class=\"meta\">source: {html.escape(ex.decision.rationale_source)}</p>")
    else:
        parts.append("<p class=\"thin\">No rationale recorded in this run's logs. "
                     "This exhibit is intentionally thin — an honest gap is preferable "
                     "to invented narrative.</p>")

    if ex.cites_criteria:
        parts.append("<h2>Cites criteria</h2><p class=\"cites\">"
                     + " ".join(f"<code>{html.escape(c)}</code>" for c in ex.cites_criteria)
                     + "</p>")
    if ex.source_paths:
        parts.append("<h2>Provenance</h2><ul>"
                     + "".join(f"<li><code>{html.escape(p)}</code></li>" for p in ex.source_paths)
                     + "</ul>")
    return _page(ex.title, "".join(parts))


def render_static(museum_root: Path, out_dir: Path) -> Path:
    """Render the museum/ tree under museum_root into a static site at out_dir.

    Returns the path to the generated index.html.
    """
    museum_root = Path(museum_root)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # project_slug -> run_slug -> list[(Exhibit, rel_href)]
    tree: dict[str, dict[str, list[tuple[Exhibit, str]]]] = {}

    for json_path in sorted(museum_root.rglob("exhibits/*/exhibit.json")):
        ex = read_exhibit(json_path)
        src_exhibit_dir = json_path.parent
        rel = Path(ex.project_slug) / ex.run_slug / "exhibits" / ex.exhibit_id
        page_dir = out_dir / rel
        page_dir.mkdir(parents=True, exist_ok=True)

        # Copy this exhibit's assets so relative <img> paths resolve offline.
        src_assets = src_exhibit_dir / "assets"
        if src_assets.is_dir():
            shutil.copytree(src_assets, page_dir / "assets", dirs_exist_ok=True)

        (page_dir / "index.html").write_text(_exhibit_page(ex), encoding="utf-8")
        href = str(rel / "index.html")
        tree.setdefault(ex.project_slug, {}).setdefault(ex.run_slug, []).append((ex, href))

    # Top-level index.
    body = ["<h1>anima Museum</h1>",
            "<p class=\"meta\">A walkthrough generated from real, dated run evidence.</p>"]
    for project in sorted(tree):
        body.append(f"<h2>{html.escape(project)}</h2>")
        for run in sorted(tree[project]):
            body.append(f"<h3>{html.escape(run)}</h3><ul class=\"exhibit-list\">")
            for ex, href in tree[project][run]:
                oc = _outcome_class(ex.decision.outcome)
                body.append(
                    f"<li><a href=\"{html.escape(href)}\">{html.escape(ex.title)}</a> "
                    f"<span class=\"pill {oc}\">{html.escape(ex.decision.outcome)}</span></li>")
            body.append("</ul>")
    index = out_dir / "index.html"
    index.write_text(_page("anima Museum", "".join(body)), encoding="utf-8")
    return index
