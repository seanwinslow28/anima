"""Self-contained static renderer for the museum/ tree (finished pass).

Three levels: an index of projects → a walkthrough per project (Mo's overview +
its runs) → a page per exhibit (Mo's docent narration, the comparison artifact or
plate, the decision trail, verdict scores, cited criteria, provenance). No
framework, no CDN, no build step — it browses by opening a file. Clean prose lives
on disk in exhibit.md; the boxes and chrome live here.
"""

from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path

from pipeline.museum.schema import Exhibit, read_exhibit

_CSS = """
:root { --ink:#2b2b2b; --paper:#faf5e8; --muted:#6b6b6b; --rule:#ddd2bb; }
* { box-sizing: border-box; }
body { background: var(--paper); color: var(--ink); font: 16px/1.65 -apple-system, Helvetica, Arial, sans-serif;
       margin: 0; padding: 2rem 1.5rem; max-width: 860px; margin-inline: auto; }
a { color: #8a5a2b; text-decoration: none; } a:hover { text-decoration: underline; }
h1 { font-size: 1.8rem; margin: 0 0 .3rem; } h2 { font-size: 1.15rem; margin: 1.7rem 0 .5rem;
     border-bottom: 1px solid var(--rule); padding-bottom: .25rem; } h3 { font-size: 1rem; margin: 0 0 .35rem; }
.crumbs { color: var(--muted); font-size: .85rem; margin-bottom: 1rem; }
.meta { color: var(--muted); font-size: .9rem; margin: 0 0 1rem; }
.lede { color: var(--muted); font-size: 1.02rem; margin: .2rem 0 1.4rem; }
.pill { display: inline-block; padding: .05rem .55rem; border-radius: 1rem; font-size: .78rem;
        border: 1px solid var(--rule); margin-right: .35rem; background:#f4ecd7; }
.pass,.ingested,.approved,.added { background:#e6f3e6; } .fail { background:#f6e3e3; }
.borderline,.human_gate_required { background:#f6efdd; }
.runs, .exhibits { list-style: none; padding: 0; }
.runs > li { margin: 1.1rem 0; } .exhibits li { padding: .3rem 0; border-bottom: 1px dotted var(--rule); }
.score { font-variant-numeric: tabular-nums; }
img, video { max-width: 100%; border: 1px solid var(--rule); background:#fff; border-radius: 3px; }
.prompt { margin: .4rem 0 1rem; padding: .6rem .9rem; border-left: 3px solid #c9a25e;
          background:#f4ecd7; color:#4a4434; font-size: .95rem; }
.compare { display: flex; gap: 1.5rem; flex-wrap: wrap; align-items: flex-start; margin: .6rem 0 1rem; }
.compare > div { flex: 1 1 280px; } .compare .who { color: var(--muted); font-size: .8rem; font-weight: normal; }
.strip { display: flex; gap: .5rem; flex-wrap: wrap; } .strip img { max-width: 110px; }
.narrative p { margin: .7rem 0; } .narrative code, .cites code { background:#efe7d2; padding: .05rem .3rem; border-radius:.2rem; }
.thin { color: var(--muted); font-style: italic; }
.trail { font-size: .92rem; } .trail ul { margin:.2rem 0; }
footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--rule);
         color: var(--muted); font-size: .82rem; }
"""


def _page(title: str, body: str) -> str:
    return ("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            f"<title>{html.escape(title)}</title><style>{_CSS}</style></head><body>{body}"
            "<footer>anima Museum — generated from real, dated run evidence. "
            "The repo carries its receipts.</footer></body></html>")


def md_to_html(md: str) -> str:
    """Tiny Markdown→HTML for Mo's prose: headings, bold, inline code, bullet
    lists, paragraphs. Everything is escaped first, so it is safe + self-contained."""
    def inline(t: str) -> str:
        t = html.escape(t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
        return t

    out: list[str] = []
    list_open = False
    for raw in md.strip().split("\n"):
        line = raw.rstrip()
        if not line.strip():
            if list_open:
                out.append("</ul>"); list_open = False
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            if list_open:
                out.append("</ul>"); list_open = False
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
        elif line.lstrip().startswith(("- ", "* ")):
            if not list_open:
                out.append("<ul>"); list_open = True
            out.append(f"<li>{inline(line.lstrip()[2:])}</li>")
        else:
            if list_open:
                out.append("</ul>"); list_open = False
            out.append(f"<p>{inline(line)}</p>")
    if list_open:
        out.append("</ul>")
    return "\n".join(out)


def _outcome_class(outcome: str) -> str:
    return outcome


def _seedance_block(ex: Exhibit) -> str:
    parts = []
    if ex.output and ex.output.endswith(".mp4"):
        parts.append(f"<video src=\"{html.escape(ex.output)}\" autoplay muted loop "
                     "playsinline controls></video>")
    if ex.prompt:
        parts.append("<h2>The prompt</h2><blockquote class=\"prompt\">"
                     f"{html.escape(ex.prompt)}</blockquote>")
    if ex.meta:
        items = " · ".join(f"{html.escape(str(k))}: <strong>{html.escape(str(v))}</strong>"
                           for k, v in ex.meta.items())
        parts.append(f"<p class=\"meta\">{items}</p>")
    return "".join(parts)


def _images_block(ex: Exhibit) -> str:
    if ex.kind == "seedance_shot":
        return _seedance_block(ex)
    if ex.kind == "motion_keys":
        left = ex.references[0] if ex.references else None
        left_html = (f"<img src=\"{html.escape(left)}\" alt=\"hand-drawn keys\">"
                     if left else "<p class=\"thin\">no key sheet on disk</p>")
        right_html = (f"<img src=\"{html.escape(ex.output)}\" alt=\"colored loop\">"
                      if ex.output else "<p class=\"thin\">no loop assembled</p>")
        strip = "".join(f"<img src=\"{html.escape(f)}\" alt=\"frame\">" for f in ex.frames)
        return ("<div class=\"compare\">"
                f"<div><h3>Hand-drawn keys <span class=\"who\">— Sean, by hand</span></h3>{left_html}</div>"
                f"<div><h3>Colored animatic <span class=\"who\">— the loop plays</span></h3>{right_html}</div>"
                "</div>"
                + (f"<div class=\"strip\">{strip}</div>" if strip else ""))
    blocks = [f"<img src=\"{html.escape(i)}\" alt=\"{html.escape(i)}\">"
              for i in [ex.output, *ex.references, *ex.frames] if i]
    return ("<div class=\"strip\">" + "".join(blocks) + "</div>") if blocks else ""


def _decision_trail(ex: Exhibit) -> str:
    rows = [f"<li>outcome: <strong>{html.escape(ex.decision.outcome)}</strong>"
            + (f" · {ex.decision.attempts} attempts" if ex.decision.attempts else "") + "</li>"]
    if ex.verdict and ex.verdict.score is not None:
        v = ex.verdict
        rows.append(f"<li><span class=\"score\">{html.escape(v.method or 'similarity')} "
                    f"{v.score}</span>"
                    + (f" · vision read: {html.escape(v.model_verdict)}" if v.model_verdict else "")
                    + "</li>")
    if ex.cites_criteria:
        rows.append("<li class=\"cites\">cites " +
                    " ".join(f"<code>{html.escape(c)}</code>" for c in ex.cites_criteria) + "</li>")
    if ex.source_paths:
        rows.append("<li>provenance: " +
                    " ".join(f"<code>{html.escape(p)}</code>" for p in ex.source_paths) + "</li>")
    return "<div class=\"trail\"><h2>Decision trail</h2><ul>" + "".join(rows) + "</ul></div>"


def _exhibit_page(ex: Exhibit, mo_md: str, project_title: str) -> str:
    crumbs = (f"<div class=\"crumbs\"><a href=\"../../../../index.html\">Museum</a> / "
              f"<a href=\"../../../index.html\">{html.escape(project_title)}</a> / "
              f"{html.escape(ex.run_slug)}</div>")
    meta = [f"<span class=\"pill {_outcome_class(ex.decision.outcome)}\">{html.escape(ex.decision.outcome)}</span>",
            f"<span class=\"pill\">{html.escape(ex.kind)}</span>"]
    if ex.persona:
        meta.append(f"decided by <strong>{html.escape(ex.persona)}</strong>")
    if ex.date:
        meta.append(html.escape(ex.date))
    meta.append(f"evidence: {ex.evidence_completeness}")
    narrative = (f"<div class=\"narrative\">{md_to_html(mo_md)}</div>"
                 if mo_md.strip() else "<p class=\"thin\">No narration yet.</p>")
    body = (crumbs + f"<h1>{html.escape(ex.title)}</h1>"
            + f"<p class=\"meta\">{' · '.join(meta)}</p>"
            + _images_block(ex) + narrative + _decision_trail(ex))
    return _page(ex.title, body)


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def render_static(museum_root: Path, out_dir: Path) -> Path:
    """Render museum_root into a self-contained static site at out_dir. Returns
    the index.html path."""
    museum_root = Path(museum_root)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # project_slug -> {title, runs: {run_slug: [(Exhibit, href)]}}
    tree: dict[str, dict] = {}
    for json_path in sorted(museum_root.rglob("exhibits/*/exhibit.json")):
        ex = read_exhibit(json_path)
        proj = tree.setdefault(ex.project_slug, {"runs": {}})
        rel = Path(ex.project_slug) / ex.run_slug / "exhibits" / ex.exhibit_id
        page_dir = out_dir / rel
        page_dir.mkdir(parents=True, exist_ok=True)
        src_assets = json_path.parent / "assets"
        if src_assets.is_dir():
            shutil.copytree(src_assets, page_dir / "assets", dirs_exist_ok=True)
        mo_md = ""
        md_path = json_path.parent / "exhibit.md"
        if md_path.exists():
            mo_md = md_path.read_text(encoding="utf-8")
        proj_title = _read_json(museum_root / ex.project_slug / "project.json").get(
            "title", ex.project_slug)
        (page_dir / "index.html").write_text(_exhibit_page(ex, mo_md, proj_title), encoding="utf-8")
        proj["runs"].setdefault(ex.run_slug, []).append(
            (ex, str(Path(ex.run_slug) / "exhibits" / ex.exhibit_id / "index.html")))

    # Project pages.
    for slug, proj in sorted(tree.items()):
        meta = _read_json(museum_root / slug / "project.json")
        title = meta.get("title", slug)
        proj["title"] = title
        proj_md_path = museum_root / slug / "project.md"
        overview = (md_to_html(proj_md_path.read_text(encoding="utf-8"))
                    if proj_md_path.exists() else "")
        n_ex = sum(len(v) for v in proj["runs"].values())
        body = [f"<div class=\"crumbs\"><a href=\"../index.html\">Museum</a></div>",
                f"<h1>{html.escape(title)}</h1>",
                f"<p class=\"lede\">{len(proj['runs'])} runs · {n_ex} exhibits, "
                "scraped from real on-disk evidence.</p>",
                f"<div class=\"narrative\">{overview}</div>" if overview else "",
                "<ul class=\"runs\">"]
        for run_slug in sorted(proj["runs"]):
            body.append(f"<li><h3>{html.escape(run_slug)}</h3><ul class=\"exhibits\">")
            for ex, href in proj["runs"][run_slug]:
                body.append(
                    f"<li><a href=\"{html.escape(href)}\">{html.escape(ex.title)}</a> "
                    f"<span class=\"pill {_outcome_class(ex.decision.outcome)}\">"
                    f"{html.escape(ex.decision.outcome)}</span></li>")
            body.append("</ul></li>")
        body.append("</ul>")
        (out_dir / slug).mkdir(parents=True, exist_ok=True)
        (out_dir / slug / "index.html").write_text(_page(title, "".join(body)), encoding="utf-8")

    # Top index.
    body = ["<h1>anima Museum</h1>",
            "<p class=\"lede\">A walkthrough of a 2D-animation pipeline built by a human and "
            "a fleet of agents — generated from the real, dated evidence each run left on disk.</p>",
            "<ul class=\"runs\">"]
    for slug, proj in sorted(tree.items()):
        n_ex = sum(len(v) for v in proj["runs"].values())
        body.append(f"<li><h3><a href=\"{html.escape(slug)}/index.html\">"
                    f"{html.escape(proj['title'])}</a></h3>"
                    f"<span class=\"meta\">{len(proj['runs'])} runs · {n_ex} exhibits</span></li>")
    body.append("</ul>")
    index = out_dir / "index.html"
    index.write_text(_page("anima Museum", "".join(body)), encoding="utf-8")
    return index
