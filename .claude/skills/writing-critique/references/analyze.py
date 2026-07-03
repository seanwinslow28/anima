#!/usr/bin/env python3
"""
Mechanical prose metrics for a markdown draft, Sean-calibrated.

Adapted from haowjy/creative-writing-skills (Apache License 2.0). The
markdown/frontmatter/fence stripping and the sentence-length, sentence-opener,
repetition, and pronoun-distribution mechanics are a faithful port (sentence-
length stdev keeps upstream's population stdev, statistics.pstdev).

NEW in this version (NOT in upstream, which prints raw numbers with no
thresholds and no baseline):
  - MATTR@50 (Moving-Average Type-Token Ratio) lexical diversity
  - MTLD-Original (threshold 0.72) as a deterministic short-text fallback
  - sentence-length coefficient of variation (burstiness) advisory flag
  - --emit-baseline / --baseline / --json baseline pipeline
These additions are grounded in
.claude/skills/writing-critique/drafts/2026-06-02-writing-critique-research-findings.md.
The dropped upstream feature is the dialogue-to-narration ratio (fiction-only).

Stdlib only. No third-party dependencies.

Usage:
    python3 analyze.py <draft.md>                          # report (default advisory thresholds)
    python3 analyze.py <draft.md> --baseline baseline.json # add baseline-relative flags
    python3 analyze.py <draft.md> --json                   # machine-readable metrics (chain gate)
    python3 analyze.py --emit-baseline corpus.md [--out baseline.json]
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

# --- Constants -------------------------------------------------------------

# MATTR token window. LOCKED at 50 (TAALED reference default; Covington & McFall
# 2010). DO NOT TUNE: changing it breaks comparability with the literature and
# with any committed baseline.json. Kept distinct from the repetition paragraph
# window (--rep-window) on purpose; upstream's window_size=5 was the latter.
MATTR_WINDOW = 50

# MTLD-Original TTR factor threshold (McCarthy & Jarvis 2010).
MTLD_THRESHOLD = 0.72

# Below this token count MATTR@50 is meaningless (draft near/under the window);
# fall back to MTLD-Original, flagged low-confidence. 60 ~= 1.2 x window.
MIN_MATTR_TOKENS = 60

# Burstiness flag: sentence-length coefficient of variation (sigma/mu). Human CV
# ~0.6-1.0+, AI ~0.15-0.40; 0.45 sits in the gap. Advisory only (perplexity, the
# stronger signal, is not available in stdlib).
CV_MONOTONY_FLAG = 0.45

WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")

PRONOUN_STARTS = {
    "i", "me", "my", "we", "our", "you", "your", "he", "his", "him",
    "she", "her", "they", "their", "them", "it", "its",
}
ARTICLE_STARTS = {"the", "a", "an", "this", "that", "these", "those"}
CONJUNCTION_STARTS = {
    "and", "but", "or", "so", "yet", "for", "nor", "because", "although",
    "though", "while", "when", "if", "after", "before", "since", "until",
    "as", "once",
}
PRONOUN_GROUPS = {
    "1st person singular (I/me/my)": {"i", "me", "my", "mine", "myself"},
    "1st person plural (we/us/our)": {"we", "us", "our", "ours", "ourselves"},
    "2nd person (you/your)": {"you", "your", "yours", "yourself", "yourselves"},
    "3rd person masc (he/him/his)": {"he", "him", "his", "himself"},
    "3rd person fem (she/her/hers)": {"she", "her", "hers", "herself"},
    "3rd person plural (they/them)": {"they", "them", "their", "theirs", "themselves"},
    "3rd person neuter (it/its)": {"it", "its", "itself"},
}
FIRST_PERSON = {
    "i", "me", "my", "mine", "myself", "we", "us", "our", "ours", "ourselves",
}

# --- Text prep (faithful port) ---------------------------------------------


def strip_frontmatter_and_fences(text: str) -> str:
    lines = text.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                start = idx + 1
                break
    cleaned: list[str] = []
    in_fence = False
    for line in lines[start:]:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            cleaned.append(line)
    return "\n".join(cleaned)


def strip_markdown(text: str) -> str:
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"_([^_]+)_", r"\1", text)
    return text


def get_sentences(dense_text: str) -> list[str]:
    flattened = " ".join(
        line.strip() for line in dense_text.splitlines() if line.strip())
    return [p.strip() for p in SENTENCE_SPLIT_RE.split(flattened) if p.strip()]


def words(text: str) -> list[str]:
    return [m.group(0).lower() for m in WORD_RE.finditer(text)]


def paragraphs(prose_text: str) -> list[str]:
    return [c.strip() for c in re.split(r"\n\s*\n", prose_text) if c.strip()]


# --- Metrics ---------------------------------------------------------------


def sentence_length_stats(sentences: list[str]) -> dict:
    lengths = [len(words(s)) for s in sentences if words(s)]
    n = len(lengths)
    if n == 0:
        return {"n": 0, "mean": None, "median": None, "min": None, "max": None,
                "pstdev": None, "cv": None, "monotony_flag": False,
                "note": "no sentences found"}
    mean_value = statistics.fmean(lengths)
    pstdev_value = statistics.pstdev(lengths) if n > 1 else 0.0
    cv = (pstdev_value / mean_value) if (n > 1 and mean_value > 0) else None
    return {
        "n": n,
        "mean": round(mean_value, 2),
        "median": statistics.median(lengths),
        "min": min(lengths),
        "max": max(lengths),
        "pstdev": round(pstdev_value, 2),
        "cv": round(cv, 3) if cv is not None else None,
        "monotony_flag": cv is not None and cv < CV_MONOTONY_FLAG,
        "note": ("insufficient length for variance signal (need >= 2 sentences)"
                 if n < 2 else None),
    }


def opener_variety(sentences: list[str]) -> dict:
    opener_words = []
    for s in sentences:
        m = WORD_RE.search(s)
        if m:
            opener_words.append(m.group(0).lower())
    total = len(opener_words)
    if total == 0:
        return {"total": 0, "pronouns": 0, "articles": 0, "conjunctions": 0,
                "other": 0, "pronoun_pct": None, "article_pct": None,
                "conjunction_pct": None, "other_pct": None}
    cats = Counter()
    for o in opener_words:
        if o in PRONOUN_STARTS:
            cats["pronouns"] += 1
        elif o in ARTICLE_STARTS:
            cats["articles"] += 1
        elif o in CONJUNCTION_STARTS:
            cats["conjunctions"] += 1
        else:
            cats["other"] += 1
    return {
        "total": total,
        "pronouns": cats["pronouns"], "articles": cats["articles"],
        "conjunctions": cats["conjunctions"], "other": cats["other"],
        "pronoun_pct": round(cats["pronouns"] / total * 100, 1),
        "article_pct": round(cats["articles"] / total * 100, 1),
        "conjunction_pct": round(cats["conjunctions"] / total * 100, 1),
        "other_pct": round(cats["other"] / total * 100, 1),
    }


def mattr(tokens: list[str], window: int = MATTR_WINDOW):
    n = len(tokens)
    if n < window:
        return None
    if n == window:
        return len(set(tokens)) / window
    total = 0.0
    count = 0
    for i in range(0, n - window + 1):
        total += len(set(tokens[i:i + window])) / window
        count += 1
    return total / count


def _mtld_one_direction(tokens: list[str], threshold: float):
    factors = 0.0
    types: set = set()
    token_count = 0
    ttr = 1.0
    for tok in tokens:
        token_count += 1
        types.add(tok)
        ttr = len(types) / token_count
        if ttr <= threshold:
            factors += 1
            types = set()
            token_count = 0
            ttr = 1.0
    if token_count > 0 and (1.0 - threshold) > 0:
        factors += (1.0 - ttr) / (1.0 - threshold)
    if factors == 0:
        return None
    return len(tokens) / factors


def mtld(tokens: list[str], threshold: float = MTLD_THRESHOLD):
    if not tokens:
        return None
    fwd = _mtld_one_direction(tokens, threshold)
    bwd = _mtld_one_direction(list(reversed(tokens)), threshold)
    if fwd is None or bwd is None:
        return None
    return (fwd + bwd) / 2.0


def lexical_diversity(tokens: list[str]) -> dict:
    n = len(tokens)
    m = mattr(tokens)
    md = mtld(tokens)
    if n < MIN_MATTR_TOKENS:
        return {"tokens": n, "mattr": m, "mtld": md,
                "primary_metric": "mtld", "primary_value": md,
                "low_confidence": True,
                "note": (f"draft < {MIN_MATTR_TOKENS} tokens; MATTR@{MATTR_WINDOW} "
                         "suppressed/low-confidence, MTLD-Original reported instead")}
    return {"tokens": n, "mattr": m, "mtld": md,
            "primary_metric": "mattr", "primary_value": m,
            "low_confidence": False, "note": None}


def repetition(paragraph_list: list[str], window_size: int = 5) -> dict:
    if len(paragraph_list) < 2:
        return {"window": window_size, "findings": [], "more": 0,
                "note": "not enough paragraphs for window analysis"}
    findings: dict = {}
    for start in range(0, max(len(paragraph_list) - window_size + 1, 1)):
        window = paragraph_list[start:start + window_size]
        counts = Counter(
            w for p in window for w in words(p) if len(w) >= 5)
        for word, count in counts.items():
            if count >= 3:
                findings[(word, start + 1, start + len(window))] = count
    ordered = sorted(findings.items(),
                     key=lambda it: (-it[1], it[0][0], it[0][1]))
    return {
        "window": window_size,
        "findings": [{"word": w, "count": c, "paragraphs": [s, e]}
                     for (w, s, e), c in ordered[:20]],
        "more": max(len(ordered) - 20, 0),
        "note": None,
    }


def pronoun_distribution(dense_text: str) -> dict:
    all_words = words(dense_text)
    total = len(all_words)
    if total == 0:
        return {"total_words": 0, "groups": {}, "first_person_rate": None}
    counts = Counter(all_words)
    groups = {}
    for label, variants in PRONOUN_GROUPS.items():
        c = sum(counts[v] for v in variants)
        groups[label] = {"count": c, "pct": round(c / total * 100, 2)}
    fp = sum(counts[v] for v in FIRST_PERSON)
    return {"total_words": total, "groups": groups,
            "first_person_rate": round(fp / total * 100, 2)}


# --- Aggregation -----------------------------------------------------------


def _prep(raw_text: str):
    prose = strip_markdown(strip_frontmatter_and_fences(raw_text))
    dense_lines = [ln for ln in prose.splitlines() if ln.strip()]
    return prose, "\n".join(dense_lines)


def metrics_from_raw(raw_text: str, file_label: str = "<text>",
                     rep_window: int = 5) -> dict:
    prose, dense_text = _prep(raw_text)
    sentences = get_sentences(dense_text)
    return {
        "file": file_label,
        "sentence_length": sentence_length_stats(sentences),
        "openers": opener_variety(sentences),
        "lexical_diversity": lexical_diversity(words(dense_text)),
        "repetition": repetition(paragraphs(prose), rep_window),
        "pronouns": pronoun_distribution(dense_text),
    }


def compute_metrics(path: str, rep_window: int = 5) -> dict:
    raw = Path(path).read_text(encoding="utf-8", errors="ignore")
    return metrics_from_raw(raw, Path(path).name, rep_window)


# --- Baseline pipeline -----------------------------------------------------


def segment_corpus(body_text: str) -> list[str]:
    """Split post-frontmatter corpus text into segments on top-level '## ' headings.
    Heading lines are dropped; only the passage bodies are returned. Content before
    the first '## ' heading (a metadata/provenance comment, say) is preamble, not a
    passage, so it is discarded and never pollutes the baseline."""
    segments, current = [], []
    seen_heading = False
    for line in body_text.splitlines():
        if line.startswith("## "):
            if seen_heading and any(l.strip() for l in current):
                segments.append("\n".join(current))
            seen_heading = True
            current = []
        elif seen_heading:
            current.append(line)
    if seen_heading and any(l.strip() for l in current):
        segments.append("\n".join(current))
    return [s for s in segments if s.strip()]


def emit_baseline(corpus_path: str, out_path: str) -> dict:
    raw = Path(corpus_path).read_text(encoding="utf-8", errors="ignore")
    body = strip_frontmatter_and_fences(raw)
    segments = segment_corpus(body) or [body]
    buckets = {"cv": [], "mattr": [], "first_person_rate": [], "opener_other_pct": []}
    for seg in segments:
        m = metrics_from_raw(seg)
        if m["sentence_length"]["cv"] is not None:
            buckets["cv"].append(m["sentence_length"]["cv"])
        if m["lexical_diversity"]["mattr"] is not None:
            buckets["mattr"].append(m["lexical_diversity"]["mattr"])
        if m["pronouns"]["first_person_rate"] is not None:
            buckets["first_person_rate"].append(m["pronouns"]["first_person_rate"])
        if m["openers"]["other_pct"] is not None:
            buckets["opener_other_pct"].append(m["openers"]["other_pct"])
    metrics = {}
    for key, vals in buckets.items():
        if vals:
            metrics[key] = {
                "mean": round(statistics.fmean(vals), 4),
                "stdev": round(statistics.pstdev(vals), 4) if len(vals) > 1 else 0.0,
                "n": len(vals),
            }
    baseline = {
        "schema_version": 1,
        "generated_from": Path(corpus_path).name,
        "mattr_window": MATTR_WINDOW,
        "segments": len(segments),
        "metrics": metrics,
    }
    Path(out_path).write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")
    return baseline


def baseline_flags(metrics: dict, baseline: dict) -> list[str]:
    """Baseline-RELATIVE deviation flags. Fire only when a metric sits below its
    own baseline mean minus one population stdev. Pronoun rate is intentionally
    baseline-relative ONLY (Sean's voice is pronoun-heavy by design)."""
    flags: list[str] = []
    bm = baseline.get("metrics", {})
    cv = metrics["sentence_length"].get("cv")
    if cv is not None and "cv" in bm:
        lo = bm["cv"]["mean"] - bm["cv"]["stdev"]
        if cv < lo:
            flags.append(
                f"monotonous vs your voice: sentence-length CV {cv} below your "
                f"baseline range (mean {bm['cv']['mean']}, -1sigma {round(lo, 3)})")
    mt = metrics["lexical_diversity"].get("mattr")
    if mt is not None and "mattr" in bm:
        lo = bm["mattr"]["mean"] - bm["mattr"]["stdev"]
        if mt < lo:
            flags.append(
                f"narrower vocabulary vs your voice: MATTR@{MATTR_WINDOW} "
                f"{round(mt, 3)} below your baseline range (mean {bm['mattr']['mean']})")
    fp = metrics["pronouns"].get("first_person_rate")
    if fp is not None and "first_person_rate" in bm:
        lo = bm["first_person_rate"]["mean"] - bm["first_person_rate"]["stdev"]
        if fp < lo:
            flags.append(
                f"fewer personal pronouns than your norm: first-person rate {fp}% "
                f"below your baseline range (mean {bm['first_person_rate']['mean']}%). "
                "Baseline-relative, not an absolute AI signal.")
    other = metrics["openers"].get("other_pct")
    if other is not None and "opener_other_pct" in bm:
        lo = bm["opener_other_pct"]["mean"] - bm["opener_other_pct"]["stdev"]
        if other < lo:
            flags.append(
                f"too many sentences open the same way: 'other' opener variety "
                f"{other}% below your baseline range "
                f"(mean {bm['opener_other_pct']['mean']}%)")
    return flags


# --- Reporting -------------------------------------------------------------


def print_report(metrics: dict, flags: list[str], has_baseline: bool) -> None:
    sl = metrics["sentence_length"]
    op = metrics["openers"]
    ld = metrics["lexical_diversity"]
    rep = metrics["repetition"]
    pr = metrics["pronouns"]
    print("==========================================")
    print(f"  Prose Analysis: {metrics['file']}")
    print("==========================================\n")

    print("## Sentence Length + Burstiness")
    if sl["n"] == 0:
        print("  (no sentences found)\n")
    else:
        print(f"  Sentences: {sl['n']}   Mean: {sl['mean']}   Median: {sl['median']}")
        print(f"  Min/Max:   {sl['min']}/{sl['max']}   StdDev(pop): {sl['pstdev']}")
        print(f"  CV (sigma/mu): {sl['cv']}"
              + ("   [FLAG: monotonous, CV < %.2f]" % CV_MONOTONY_FLAG
                 if sl["monotony_flag"] else ""))
        if sl["note"]:
            print(f"  note: {sl['note']}")
        print()

    print("## Lexical Diversity")
    print(f"  Tokens: {ld['tokens']}   MATTR@{MATTR_WINDOW}: {ld['mattr']}   "
          f"MTLD: {ld['mtld']}")
    print(f"  primary: {ld['primary_metric']} = {ld['primary_value']}"
          + ("   [low confidence]" if ld["low_confidence"] else ""))
    if ld["note"]:
        print(f"  note: {ld['note']}")
    print()

    print("## Sentence Opener Variety")
    if op["total"]:
        print(f"  pronoun {op['pronoun_pct']}%  article {op['article_pct']}%  "
              f"conjunction {op['conjunction_pct']}%  other {op['other_pct']}%  "
              f"(n={op['total']})")
    else:
        print("  (no openers found)")
    print()

    print("## Pronoun Distribution")
    print(f"  first-person rate: {pr['first_person_rate']}%   "
          f"total words: {pr['total_words']}")
    print()

    print(f"## Repetition (window {rep['window']} paragraphs)")
    if rep["note"]:
        print(f"  {rep['note']}")
    elif not rep["findings"]:
        print("  (no notable repetitions)")
    else:
        for f in rep["findings"]:
            print(f"  {f['count']}x \"{f['word']}\" "
                  f"(paragraphs {f['paragraphs'][0]}-{f['paragraphs'][1]})")
        if rep["more"]:
            print(f"  ... and {rep['more']} more")
    print()

    print("## Baseline-Relative Flags")
    if not has_baseline:
        print("  (no baseline supplied: only CV is flagged absolutely; "
              "MATTR/pronouns need a baseline to flag)")
    elif not flags:
        print("  (within your baseline ranges)")
    else:
        for f in flags:
            print(f"  - {f}")
    print()
    print("  Analyzer is advisory. It informs the revise decision; it never blocks.")


def main() -> int:
    p = argparse.ArgumentParser(description="Sean-calibrated prose mechanics.")
    p.add_argument("file", nargs="?", help="Markdown draft to analyze")
    p.add_argument("--baseline", help="baseline.json to diff against")
    p.add_argument("--emit-baseline", help="corpus.md to compute a baseline from")
    p.add_argument("--out", help="output path for --emit-baseline (default: sibling baseline.json)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--rep-window", type=int, default=5,
                   help="repetition paragraph window (NOT the MATTR token window)")
    args = p.parse_args()

    if args.emit_baseline:
        out = args.out or str(Path(args.emit_baseline).with_name("baseline.json"))
        bl = emit_baseline(args.emit_baseline, out)
        print(f"Wrote baseline ({bl['segments']} segments) to {out}")
        return 0

    if not args.file:
        print("Usage: python3 analyze.py <draft.md> [--baseline baseline.json] "
              "[--json] | --emit-baseline corpus.md", file=sys.stderr)
        return 1
    path = Path(args.file)
    if not path.is_file():
        print(f"File not found: {args.file}", file=sys.stderr)
        return 1
    if args.rep_window <= 0:
        print("--rep-window must be a positive integer", file=sys.stderr)
        return 1

    metrics = compute_metrics(str(path), args.rep_window)
    flags: list[str] = []
    has_baseline = False
    if args.baseline:
        baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
        flags = baseline_flags(metrics, baseline)
        has_baseline = True

    if args.json:
        print(json.dumps({"metrics": metrics, "baseline_flags": flags}, indent=2))
    else:
        print_report(metrics, flags, has_baseline)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
