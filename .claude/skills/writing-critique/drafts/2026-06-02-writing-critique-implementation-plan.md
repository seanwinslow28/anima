# writing-critique skill + ai-tells.md evidence upgrade — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a new `writing-critique` skill (adversarial reader + stdlib `analyze.py` + Sean-voice baseline) that sits between `writing-voice-modes` and `writing-humanity-pass`, and re-ground the evidence tiers in `writing-humanity-pass/references/ai-tells.md`.

**Architecture:** One new skill folder under `.claude/skills/writing-critique/` (SKILL.md + 4 reference files + 2 eval files), one in-place surgical edit to `ai-tells.md`, and chain-diagram updates across the four existing writing skills. The analyzer is pure-stdlib Python that faithfully ports `haowjy/creative-writing-skills` mechanics and adds MATTR@50 + MTLD fallback + sentence-length coefficient-of-variation (burstiness) + a regenerable `baseline.json` pipeline. Critique is advisory, never rewrites, and caps at one grounded revise pass.

**Tech Stack:** Markdown skill files; Python 3 standard library only (`re`, `statistics`, `collections`, `json`, `argparse`, `sys`, `pathlib`); YAML eval files (manual-review schema).

---

## Locked decisions (do NOT relitigate — build around these)

Em-dash ban; critique sits between voice and humanity; the five voice modes; advisory-not-blocking; one-revise-pass cap; **packaging Approach A** (analyzer + baseline live in `writing-critique`; the evidence upgrade is an in-place `ai-tells.md` edit); drop dialogue-ratio; baseline = the voice-samples corpus.

## Source-of-truth precedence

1. `drafts/2026-06-02-writing-critique-research-findings.md` — **fact-checked; SUPERSEDES the spec on every conflict.**
2. `drafts/2026-06-02-writing-critique-layer-design.md` — approved design, superseded by the report where they differ.
3. House style: mirror `writing-humanity-pass` (interactive-vs-headless detection, verdict block, attribution form) and the manual-review eval schema of `storytelling-architecture/evals.yaml`.

## Research deltas baked into this plan (the spec alone is NOT enough)

| # | Delta (from the research report) | Where it lands in this plan |
|---|---|---|
| 1 | Re-ground `ai-tells.md` citations: keep Kobak only for word-frequency fingerprint (→ slop bullet, NOT diversity); move RAID + Ghostbuster to a detection-caution note; add real lexical-diversity cites WITH comparison-class caveat; do NOT import BEA/Nature HSSCOMMS. | Task 8 |
| 2 | Split the top tier into (a) measurable + baseline-relative and (b) research-cited-but-qualitative (positive-emotion: NOT stdlib-measurable). | Task 8 |
| 3 | Promote burstiness / sentence-length CV to a first-class measurable signal. | Task 1 (analyzer), Task 8 (ai-tells) |
| 4 | Reword slop bullet: drop "near-random" and "for Claude specifically"; keep model/genre-transfer argument; note deliberate divergence from upstream. | Task 8 |
| 5 | Pronoun rate strictly baseline-relative, never absolute. | Task 1 (`baseline_flags`), Task 8 |
| 6 | analyze.py: MATTR window LOCKED at 50; add MTLD-Original (0.72) fallback for drafts < ~60 tokens; no HD-D/vocd-D; replace "stdev < 4" with CV = σ/μ flag < ~0.45; guard single-sentence div-by-zero; keep `pstdev` (population) to match upstream; keep MATTR token window distinct from upstream's repetition paragraph window. | Task 1 |
| 7 | finding-rubric.md gets STRUCTURAL anti-sycophancy scaffolding: hard persona separation, per-finding grounding (quote + concrete reader cost), severity-ranked floor with explicit license to report FEWER issues (not a forced count); cap/forbid praise. | Task 4 |
| 8 | SKILL.md names persona separation as the explicit mitigation for the same-model voice-then-critique path; frames the single revise pass as "revise against [specific finding]" routed through voice-modes; any 2nd pass requires new external input. | Task 5 |
| 9 | Eval `flags_ai_flatness_with_analyzer` is written against CV / baseline-relative signal, NOT the absolute stdev. | Task 9 |

## Faithful-port constraints

Port the prose-critique RUBRIC and the analyzer MECHANICS faithfully (text-prep, sentence/opener/repetition/pronoun functions, `pstdev`), but FIX the citations in the port. Upstream has **no MATTR, no thresholds, no baseline JSON** — those are new additions, correctly labeled "new," not ports.

## File map (what each file owns)

```
.claude/skills/writing-critique/
├── SKILL.md                       # Task 5  — the skill contract, two modes, 5 dimensions, verdict, attribution
├── references/
│   ├── analyze.py                 # Task 1  — stdlib analyzer (faithful port + MATTR/MTLD/CV/baseline)
│   ├── test_analyze.py            # Task 1  — pytest-compatible + standalone self-test
│   ├── baseline-corpus.md         # Task 2  — Sean-only prose, 6 passages under '## ' headings
│   ├── baseline.json              # Task 3  — generated by analyze.py --emit-baseline (committed)
│   └── finding-rubric.md          # Task 4  — adversarial rubric + anti-sycophancy scaffolding + report format
├── drafts/                        # exists (design spec, research report, this plan)
├── evals.yaml                     # Task 9
└── evals.sealed.yaml              # Task 9

.claude/skills/writing-humanity-pass/references/ai-tells.md   # Task 8  — evidence upgrade (additive, keeps all 30)
.claude/skills/writing-humanity-pass/SKILL.md                 # Task 6/7 — chain diagram + ai-tells pointer
.claude/skills/writing-voice-modes/SKILL.md                   # Task 7  — chain diagram + related skills
.claude/skills/storytelling-architecture/SKILL.md             # Task 7  — chain contract + related skills
.claude/skills/substack-value-engine/SKILL.md                 # Task 7  — chain contract + related skills
CHANGELOG.md / README.md / CLAUDE.md                          # Task 10 — repo integration
```

## Dependency order (build bottom-up)

Task 1 (analyzer) → Task 2 (corpus) → Task 3 (baseline.json, needs 1+2) → Task 4 (rubric) → Task 5 (SKILL.md) → Task 6 (humanity-pass SKILL pointer) → Task 7 (chain diagrams ×4) → Task 8 (ai-tells evidence upgrade) → Task 9 (evals) → Task 10 (repo integration + validate) → Task 11 (end-to-end dry run).

> **Note on validation timing:** `scripts/validate.py` iterates every directory in `.claude/skills/` and errors if a dir has no `SKILL.md`. The `writing-critique/` dir already exists (drafts only), so validate.py **errors until Task 5 lands**. That is expected mid-build; the clean validate run is Task 10.

---

## Task 1: The mechanical analyzer (`analyze.py` + tests)

**Files:**
- Create: `.claude/skills/writing-critique/references/analyze.py`
- Test: `.claude/skills/writing-critique/references/test_analyze.py`

**What it does:** Faithful port of the upstream text-prep + sentence/opener/repetition/pronoun mechanics, plus the new MATTR@50, MTLD-Original fallback, sentence-length CV (burstiness) flag, and the `--emit-baseline` / `--baseline` / `--json` pipeline. Pure stdlib. Every metric is computed into a dict (so `--json` and the tests can read data, not parse printed text).

**Design rules locked here:**
- `MATTR_WINDOW = 50`, a module constant, NOT a CLI arg. Comment says DO NOT TUNE.
- Repetition paragraph window stays a CLI arg `--rep-window` (default 5), distinct from the MATTR token window (the upstream `window_size=5` was the repetition window; never conflate).
- Sentence-length stdev uses `statistics.pstdev` (population) to match upstream; the burstiness flag is CV = `pstdev / mean`.
- No-baseline mode flags ONLY low CV (< 0.45) as an absolute advisory. MATTR and pronoun rate are reported raw but NEVER flagged absolutely (comparison-class / Sean's-voice-is-pronoun-heavy reasons). They are flagged only against a baseline.
- Guards: `cv` is `None` for < 2 sentences (div-by-zero guard); MATTR is `None` for < 50 tokens; for < 60 tokens MTLD is the primary metric, flagged low-confidence.

- [ ] **Step 1: Write the failing tests**

Create `.claude/skills/writing-critique/references/test_analyze.py`:

```python
#!/usr/bin/env python3
"""Stdlib-only tests for analyze.py. Run either way:
    python3 -m pytest .claude/skills/writing-critique/references/test_analyze.py -v
    python3 .claude/skills/writing-critique/references/test_analyze.py   # zero-dependency fallback
"""
import importlib.util
import json
import tempfile
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "analyze", str(Path(__file__).with_name("analyze.py")))
analyze = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(analyze)


def test_mattr_window_is_locked_50():
    assert analyze.MATTR_WINDOW == 50


def test_strip_frontmatter_and_fences():
    raw = "---\ntitle: x\n---\nHello world.\n```\ncode\n```\nReal prose here."
    out = analyze.strip_frontmatter_and_fences(raw)
    assert "title: x" not in out
    assert "code" not in out
    assert "Real prose here." in out


def test_words_tokenizes_lowercase():
    assert analyze.words("The Cat's hat.") == ["the", "cat's", "hat"]


def test_cv_high_for_varied_sentences():
    sents = ["Short.", "This one is a good deal longer than the first sentence here.",
             "Mid length sentence now.", "Tiny.",
             "Another fairly long winding clause that keeps going and going for a while."]
    stats = analyze.sentence_length_stats(sents)
    assert stats["cv"] is not None and stats["cv"] >= 0.45
    assert stats["monotony_flag"] is False


def test_cv_low_for_monotone_sentences():
    sents = ["The agent ran the nightly job again.",
             "The system logged the result to disk.",
             "The report listed the total for today.",
             "The metric stayed inside the normal band."]
    stats = analyze.sentence_length_stats(sents)
    assert stats["cv"] is not None and stats["cv"] < 0.45
    assert stats["monotony_flag"] is True


def test_cv_guards_single_sentence():
    stats = analyze.sentence_length_stats(["Only one sentence here."])
    assert stats["cv"] is None          # no div-by-zero
    assert stats["monotony_flag"] is False


def test_mattr_none_for_short_text():
    assert analyze.mattr(["a", "b", "c"]) is None


def test_mattr_value_for_long_text():
    toks = (["the", "cat", "sat", "on", "a", "mat"] * 20)
    val = analyze.mattr(toks)
    assert val is not None and 0.0 < val <= 1.0


def test_mtld_lower_for_repetitive_text():
    diverse = "alpha beta gamma delta epsilon zeta eta theta iota kappa".split() * 6
    repetitive = "the the the the cat the the the the the".split() * 6
    assert analyze.mtld(repetitive) < analyze.mtld(diverse)


def test_lexical_diversity_uses_mtld_under_60_tokens():
    toks = "the agent ran the job and then it failed and i fixed it fast".split()
    ld = analyze.lexical_diversity(toks)
    assert ld["primary_metric"] == "mtld"
    assert ld["low_confidence"] is True


def test_emit_baseline_has_mean_and_stdev_per_metric():
    corpus = (
        "## one\n" + "I ran the fleet at dawn and the agents sang back to me. "
        "Short. A longer winding line that keeps unspooling across the morning quiet.\n\n"
        + " ".join(f"word{i}" for i in range(80)) + "\n\n"
        "## two\n" + "We shipped it late. The ferry horn blew across the cold gray water again. "
        "Tiny. Another long meandering clause that refuses to end for quite a while now.\n\n"
        + " ".join(f"alt{i}" for i in range(80)) + "\n"
    )
    with tempfile.TemporaryDirectory() as d:
        cpath = Path(d) / "corpus.md"
        cpath.write_text(corpus, encoding="utf-8")
        out = Path(d) / "baseline.json"
        bl = analyze.emit_baseline(str(cpath), str(out))
        assert bl["segments"] == 2
        assert bl["mattr_window"] == 50
        assert "cv" in bl["metrics"]
        assert "mean" in bl["metrics"]["cv"] and "stdev" in bl["metrics"]["cv"]
        assert json.loads(out.read_text(encoding="utf-8"))["schema_version"] == 1


def test_baseline_flags_fire_below_range():
    metrics = {
        "sentence_length": {"cv": 0.10, "monotony_flag": True},
        "lexical_diversity": {"mattr": 0.50},
        "pronouns": {"first_person_rate": 0.1},
        "openers": {"other_pct": 5.0},
    }
    baseline = {"metrics": {
        "cv": {"mean": 0.70, "stdev": 0.10},
        "mattr": {"mean": 0.80, "stdev": 0.03},
        "first_person_rate": {"mean": 4.0, "stdev": 1.0},
        "opener_other_pct": {"mean": 40.0, "stdev": 8.0},
    }}
    flags = analyze.baseline_flags(metrics, baseline)
    assert any("monotonous" in f for f in flags)
    assert any("vocabulary" in f for f in flags)
    assert any("pronoun" in f for f in flags)
    assert any("open the same way" in f for f in flags)


def test_compute_metrics_and_json(tmp_path=None):
    import os
    d = tempfile.mkdtemp()
    p = Path(d) / "draft.md"
    p.write_text("# Title\n\nThe agent ran. It failed. I fixed it. So it goes.\n", encoding="utf-8")
    m = analyze.compute_metrics(str(p))
    assert m["sentence_length"]["n"] >= 3
    assert "lexical_diversity" in m and "pronouns" in m and "openers" in m
    os.remove(p)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {fn.__name__}: {exc}")
    raise SystemExit(1 if failed else 0)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 .claude/skills/writing-critique/references/test_analyze.py`
Expected: FAIL — `analyze.py` does not exist yet (`FileNotFoundError` on the spec load).

- [ ] **Step 3: Write `analyze.py`**

Create `.claude/skills/writing-critique/references/analyze.py` exactly as below:

```python
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
    Heading lines are dropped; only the passage bodies are returned."""
    segments, current = [], []
    for line in body_text.splitlines():
        if line.startswith("## "):
            if any(l.strip() for l in current):
                segments.append("\n".join(current))
            current = []
        else:
            current.append(line)
    if any(l.strip() for l in current):
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 .claude/skills/writing-critique/references/test_analyze.py`
Expected: every line prints `PASS ...`, exit code 0.
Also run (if pytest is available — it is in the agents-sdk venv):
`python3 -m pytest .claude/skills/writing-critique/references/test_analyze.py -v` → all green.

- [ ] **Step 5: Smoke-test the CLI on a monotone specimen**

Run:
```bash
printf '# t\n\nThe agent ran the nightly job again. The system logged the result to disk. The report listed the total for today. The metric stayed inside the normal band.\n' > /tmp/mono.md
python3 .claude/skills/writing-critique/references/analyze.py /tmp/mono.md
```
Expected: the "Sentence Length + Burstiness" block prints a CV value with `[FLAG: monotonous, CV < 0.45]`.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/writing-critique/references/analyze.py .claude/skills/writing-critique/references/test_analyze.py
git commit -m "feat(writing-critique): stdlib prose analyzer (faithful port + MATTR/MTLD/CV/baseline)"
```

---

## Task 2: The baseline corpus (`baseline-corpus.md`)

**Files:**
- Create: `.claude/skills/writing-critique/references/baseline-corpus.md`
- Source (read-only): `.claude/skills/writing-voice-modes/references/voice-samples.md`

**What it does:** Curated **Sean-only** prose, one passage per `## ` heading (so `analyze.py --emit-baseline` segments it into 6 samples and produces a per-metric mean+stdev). It is the four "Full Exercise Passages (Final Versions)" + the two Professional-Dial samples. It **excludes** every "AI wrote:" counter-sample and all meta-analysis.

**Provenance to copy verbatim** (verify each block char-for-char against `voice-samples.md`; strip the leading `> ` blockquote markers; re-level the `### ` sub-headings to `## `):
- Domestic Observer passage — voice-samples.md lines 84–90
- Gonzo Technical passage — lines 93–103
- Beat Flow passage — lines 106–112
- Minimalist Absurdist passage — lines 115–127
- Professional-Dial Slack sample — line 136
- Professional-Dial Stakeholder sample — line 139

- [ ] **Step 1: Create `baseline-corpus.md`**

Write the file exactly as below (header comment + 6 `## ` segments). The passage bodies must match `voice-samples.md` verbatim:

````markdown
<!--
baseline-corpus.md: Sean-only prose for the writing-critique analyzer baseline.

PROVENANCE: extracted verbatim from
  ../../writing-voice-modes/references/voice-samples.md
  - "Full Exercise Passages (Final Versions)" x4 (Domestic Observer, Gonzo,
    Beat Flow, Minimalist Absurdist)
  - "Professional Dial: 60%" x2 (Slack update, stakeholder intro)
  ~1,500 words spanning all five modes (Sean Mode = the Professional-Dial hybrid).

EXCLUDES: every "AI wrote:" counter-sample and all meta-analysis/commentary.
Only finished Sean prose belongs here, or the baseline is contaminated.

REGENERATION: when voice-samples.md gains a new calibration round, re-extract the
new Sean prose into this file (one passage per '## ' heading) and re-run
  python3 analyze.py --emit-baseline baseline-corpus.md --out baseline.json
The MATTR window is LOCKED at 50 in analyze.py. DO NOT tune it. Changing it
breaks comparability with the committed baseline and the literature.
-->

## Domestic Observer

For nine years I commuted two hours each way to organize media files in the windowless basement of a building so old it smelled like it was working toward its second millennium. New York Life Insurance Company. The name alone should've been the tell. I was insuring someone else's life while mine collected dust between hard drives and hollow water cooler conversations. I smiled through them like a man who'd been smiling so long his face forgot it was a choice.

I had three animated shorts, five scripts, and thousands of dollars distributed across the pockets of people who swore they could get my work in front of the right people. The right people were apparently busy. Screenwriting was supposed to be the exit, but the more I learned about Hollywood, the more it sounded like the same basement with better lighting. Writers rooms had shrunk to fit nepo babies and the friends of friends of friends, and the golden age of the evergreen sitcom had packed its bags sometime around 2015 without telling anyone where it was going.

Then one Tuesday in March (I remember it was a Tuesday because the bathroom stalls at New York Life were marginally less repulsive on Tuesdays), I was scrolling Instagram while perched on a toilet older than my freelance career, and I saw it. People were posting pictures of themselves in the style of Studio Ghibli. ChatGPT had learned to draw. I'd seen the Will Smith spaghetti video. I was a non-believer. But sitting there, something shifted. It was the kind of epiphany you'd expect to happen on a mountaintop or in a therapist's office, not in a bathroom stall that smelled like it was staging an intervention of its own.

I no longer organize media files. Agents do.

## Gonzo Technical

January 1st, 2024. High on mushrooms, staring at myself in a bathroom mirror at, I want to say 2 AM but time had stopped being reliable about three hours earlier. I made a declaration to the stranger in the reflection: this is the year I begin again. The stranger did not look convinced.

By 7:15 the next morning, I was slowly migrating onto the Staten Island ferry with the rest of the lost souls stuck in the same pattern. Our baggy, bloodshot eyes staring into the void as we collectively migrate towards the ship of the damned. Sheep heading to the slaughterhouse we call our office. New year. New resolutions. New ways to trick ourselves into happiness. The hamster wheel rolls on.

The escape plan was screenwriting. I had five scripts, three animated shorts, and a growing portfolio of receipts from consultants, coverage services, and festival submission fees: $4,200 across 2022 and 2023 alone, paid to people whose primary skill was maintaining eye contact while saying "it's all about getting it in front of the right people." The right people were apparently on a different planet. Meanwhile, Hollywood's writers went on strike over AI, which I found amusing in the way you find something amusing right before it becomes your entire life. I'd seen the Will Smith spaghetti video. Computers couldn't do what humans do.

MARCH 25TH, 2025. New York Life bathroom stall. Instagram open. Studio Ghibli portraits flooding every feed. ChatGPT-4o image generation had dropped and the internet lost its collective mind. I was sitting on a toilet that had seen more human despair than most therapists, scrolling through AI-generated art with the quiet horror of a man who had just bet his career on the wrong horse and the horse was now being rendered in watercolor by a machine.

I charged forward. Screenwriting podcasts replaced by AI tutorials. Writing exercises replaced by vibecoding sessions. A profession called "Product Management" materialized in my vocabulary like a cheat code I'd been walking past for a decade. By November I had the job. By March I was building autonomous agents in my terminal at 5 AM.

The bathroom epiphanies have not stopped. I'm choosing not to examine that pattern.

## Beat Flow

I was high on mushrooms staring at my own face in the mirror, the face of a man who had been commuting to the same windowless basement for nine years and organizing the same media files in the same dead air of a building so old it had given up pretending to smell like anything other than what it was, and I said to myself, to the stranger behind the glass with the bloodshot eyes and the jaw clenched tight like a fist that forgot how to open, I said this is the year, this is the one, and the stranger just stared back like he'd heard it all before because he had.

And the ferry the next morning, the Staten Island ferry packed with the same lost souls shuffling aboard in their winter coats and their dead eyes and their travel mugs filled with caffeine and hair of the dog, an elixir of motivation and a way to cope, all of us migrating across that gray water toward Manhattan like a slow parade of the professionally damned, and I remember thinking even then, even in the middle of the resolution and the mushroom afterglow and the desperate wanting, I remember thinking this feels exactly like last year.

Nine years of fluorescent light and lanyard swipes and water cooler small talk about nothing, nine years of animated shorts nobody watched and scripts nobody read and thousands of dollars hemorrhaged into the pockets of consultants who promised the right people and delivered the same empty room, nine years of screenwriting podcasts and festival submission fees and the slow erosion of believing your own talent means anything when the door won't open, and then one morning in March, sitting in a bathroom stall at New York Life Insurance Company, scrolling Instagram on a toilet older than my ambition, I saw the Studio Ghibli portraits flooding every feed and felt something crack open in my chest like a door I didn't know was there, and I walked through it and I kept walking and I never turned around.

That was then. Now I wake up before my alarm. Fuelled by the new found skills that didn't exist 18 months ago, fresh brewed coffee, and for once in my life, a glimmer of hope. I hear the ferry horn blast from across the Hudson. It still shepards the herd to and fro ... but I no longer rub elbows with sheep.

## Minimalist Absurdist

Here is what happened. I organized media files in a basement for nine years. The building was 150 years old. It smelled like it. I commuted two hours each way on the Staten Island ferry. So did everyone else. We did not discuss this.

I had three animated shorts and five screenplays and several thousand dollars' worth of advice from people who knew the right people. The right people never materialized. I began again.

In 2024 I saw the Will Smith spaghetti video and decided AI was not a threat. Writers went on strike over it. I found this amusing. I began again.

In March 2025 I was sitting on a toilet at New York Life Insurance Company scrolling Instagram. Everyone was a Studio Ghibli character. ChatGPT had learned to draw. I had not learned to draw in nine years of art school. The machine learned in an afternoon. I began again.

I replaced screenwriting podcasts with AI tutorials. I replaced writing exercises with vibecoding. I learned a phrase called "Product Management." By November I had a job doing it. I was thirty-three years old. Most product managers start at twenty-four.

I now wake up at 4:45 AM on purpose. I build things in a terminal. I talk to machines and the machines talk back. Sometimes they are more helpful than the consultants were. They are always cheaper. I began again.

The ferry still runs. I hear it from across the Hudson some mornings, if the coffee hasn't kicked in yet and the apartment is quiet enough. It sounds the same as it always did. I sound different... I have begun.

## Professional Dial Slack

Hey team, quick update on the computer use rollout. We're pushing it back a week. The agent works beautifully in our test environments, which based on prior experience means it will find novel ways to misclick its way through someone's personal inbox and start emailing previous coworkers about their anal warts medication. Latency on screenshot loops is hovering 200ms over target, and we'd rather ship something that doesn't summon a support ticket avalanche on day one. New target: next Friday. Updating the roadmap and beta tester comms now. Let me know if you have any questions.... Also, on a side note, ignore any of my previous emails.

## Professional Dial Stakeholder

Sprint 14 closed Friday with /buddy in production, on schedule, and somehow under budget: three things that have not happened simultaneously in the recorded history of this team. The team shipped a feature whose entire pitch is "what if your terminal had a digital ferret" which sounded ridiculous in planning and feels marginally less ridiculous now that 1,247 users have invoked it in the first 48 hours. The word "buddy" appears in our internal docs 316 times. Engineering hit every milestone, including two I had privately bet against in the standup chat. Design caught two edge cases QA missed, including one where /buddy responded to existential prompts with a recipe for cornbread. We patched it. It is, by every reasonable definition, a buddy. Full metrics, post-mortem notes, and the cornbread recipe below. Who knew a ferret could bake?
````

- [ ] **Step 2: Verify the segmentation count**

Run:
```bash
python3 -c "import importlib.util,sys; s=importlib.util.spec_from_file_location('a','.claude/skills/writing-critique/references/analyze.py'); a=importlib.util.module_from_spec(s); s.loader.exec_module(a); from pathlib import Path; body=a.strip_frontmatter_and_fences(Path('.claude/skills/writing-critique/references/baseline-corpus.md').read_text()); print('segments=', len(a.segment_corpus(body)))"
```
Expected: `segments= 6`. If not 6, a `## ` heading is missing or an extra one leaked in.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/writing-critique/references/baseline-corpus.md
git commit -m "feat(writing-critique): Sean-only baseline corpus (6 passages, all 5 modes)"
```

---

## Task 3: Generate the committed baseline (`baseline.json`)

**Files:**
- Create (generated): `.claude/skills/writing-critique/references/baseline.json`

**What it does:** Precomputed per-metric mean+stdev so the chain never recomputes at runtime. Generated by the analyzer; committed.

- [ ] **Step 1: Emit the baseline**

Run:
```bash
python3 .claude/skills/writing-critique/references/analyze.py \
  --emit-baseline .claude/skills/writing-critique/references/baseline-corpus.md \
  --out .claude/skills/writing-critique/references/baseline.json
```
Expected stdout: `Wrote baseline (6 segments) to .../baseline.json`.

- [ ] **Step 2: Sanity-check the JSON**

Run: `python3 -m json.tool .claude/skills/writing-critique/references/baseline.json`
Expected shape (values will differ — do NOT hand-edit them):
```json
{
  "schema_version": 1,
  "generated_from": "baseline-corpus.md",
  "mattr_window": 50,
  "segments": 6,
  "metrics": {
    "cv": { "mean": <float>, "stdev": <float>, "n": 6 },
    "mattr": { "mean": <float>, "stdev": <float>, "n": 6 },
    "first_person_rate": { "mean": <float>, "stdev": <float>, "n": 6 },
    "opener_other_pct": { "mean": <float>, "stdev": <float>, "n": 6 }
  }
}
```
Check: `cv.mean` should land roughly in the 0.4–0.8 band and `mattr.n == 6` (every passage is > 50 tokens, so MATTR computes for all six). If `mattr.n < 6`, a passage is too short — recheck Task 2.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/writing-critique/references/baseline.json
git commit -m "feat(writing-critique): commit precomputed voice baseline.json"
```

---

## Task 4: The finding rubric (`finding-rubric.md`)

**Files:**
- Create: `.claude/skills/writing-critique/references/finding-rubric.md`

**What it does:** Ports the upstream `prose-critique` craft (adversarial mindset, the four-quality finding rubric, "critique the execution not the premise," stage calibration "fix the bones before the skin," report shape) and adds the STRUCTURAL anti-sycophancy scaffolding the research report requires (persona separation, per-finding grounding, severity-ranked floor with explicit license to report fewer, capped praise). This is the prompt the SKILL.md tells the model to run.

**Faithful-port lines to preserve (from the upstream read in the research report):** the "find what doesn't work / a critique that says 'well done' without digging is worse than no critique" framing; the four qualities **Specific / Reasoned / Directable / Non-obvious**; the "what wastes everyone's time" list including *critique the execution, not the premise*; *fix the bones before the skin*; report order **overall assessment → findings by severity → verdict + the one highest-leverage change**.

**Anti-sycophancy additions (research §1.2, ranked by evidence × leverage):** persona separation (#1), bounded adversarial framing with a defensible-choice guard (#3), per-finding tuple grounding (#2/#4/#5), severity-ranked floor not a fixed count (#8 avoided), capped praise (#6).

- [ ] **Step 1: Create `finding-rubric.md`**

Write the file exactly as below:

````markdown
# Finding Rubric: adversarial reading for nonfiction

Adapted from the `prose-critique` skill in
[`haowjy/creative-writing-skills`](https://github.com/haowjy/creative-writing-skills)
(Apache License 2.0), re-aimed at Sean's nonfiction/Substack work. The rubric and
report shape are a faithful port; the structural anti-sycophancy scaffolding
below is added per the writing-critique research findings (sycophancy is a
measured RLHF consequence, and self-enhancement bias is worst when the same model
that voiced the draft also critiques it).

## The mindset

Find what does not work. Not what does. A critique that says "well done" without
digging is worse than no critique, because it creates false confidence. Your job
is to interrogate how the prose fails a real reader, then hand the author the
single change with the most leverage.

## Persona separation (read this first: it is the load-bearing guard)

**You did not write this draft.** You are a hostile expert reviewer whose
reputation depends on catching what the author missed. You have no stake in the
draft being good and no social reason to be kind. This matters most in the chain
gate, where the same model just composed the draft in `writing-voice-modes`:
without this separation the reviewer flatters its own prior output (self-
enhancement bias). Adopt the reviewer identity fully before reading a line.

## Bounded adversarial framing (with the guard that keeps it honest)

Find what would make a skeptical reader stop trusting this draft. **Only raise an
issue you can defend with a direct quote and a concrete reader cost.** Distinguish
genuine defects from defensible authorial choices: Sean's voice is deliberately
pronoun-heavy, polysyndetic, self-deprecating, and pop-culture-anchored. Flagging
a signature move as a defect is the failure mode that destroys trust. Once the
author catches you inventing a flaw, every finding is discounted.

## What makes a good finding (the four qualities)

- **Specific**: cite the exact paragraph or quote the exact span. "The third
  paragraph" beats "the middle." "Could be stronger" is not a finding.
- **Reasoned**: name the concrete reader cost. *Why* does it fail: the reader
  loses the thread, stops trusting, skims, or quits here.
- **Directable**: the author knows what to do next. A finding the author cannot
  act on is an observation, not a critique.
- **Non-obvious**: not spellcheck, not what a linter already catches.

## Every finding is a tuple

```
quoted span  →  why it fails (which of the 5 dimensions)  →  severity (blocking / major / minor)  →  the directed fix
```

If you cannot fill all four cells, you do not have a finding yet.

## Severity-ranked floor, NOT a fixed count

Surface **every blocking and major issue, ranked by severity.** If the draft is
genuinely strong, say so and report fewer. **Do not invent issues to fill a
quota.** Forcing a fixed number of findings is the one popular technique with a
documented fabrication failure mode: on a clean draft it manufactures nitpicks.
A short, honest critique of a strong draft is a success, not a failure.

## Cap the praise

Do not write a "what works" section. At most one calibration line naming the
draft's single real strength, and only if it is true. Praise is the slot the
model uses to discharge its agreement bias; remove the slot.

## The five dimensions (each defers to the owning skill)

Critique the *execution* of each; never re-litigate the committed premise.

1. **Structure**: hook strength, but/therefore seams, open-loop closure,
   slippery-slide section ends. Defers to `storytelling-architecture`.
2. **Value**: Itch / Solution / Transfer actually delivered, narrative-to-value
   seam intact (payoff, not bolted-on appendix), Rule-of-One held, one usable
   thing in 10 minutes. Defers to `substack-value-engine`.
3. **Voice**: reads as Sean (signature moves present) vs generic-competent
   narrator; register drift. Defers to `writing-voice-modes`.
4. **Prose / line**: rhythm, sentence variety, repetition, clarity,
   show-don't-summarize, tidy-summary endings, AI-flatness. **The analyzer plugs
   in here** (sentence-length CV / burstiness, MATTR, opener variety; see
   `analyze.py` and `baseline.json`). Analyzer output is advisory evidence for a
   finding, never a finding on its own.
5. **Hiring signal** (Sean-specific): judgment shown not claimed, artifact +
   blameless self-post-mortem present, the ask stays sideways. Defers to
   `substack-value-engine`.

## Critique the execution, not the premise

If the draft commits to an idea, a structure, or a scaffold, do not argue it
should have been a different piece. Critique how well it executes the choice it
made. Re-litigating the premise wastes the author's time and is out of scope.

## Stage calibration: fix the bones before the skin

- **Early draft** → weight Structure + Value first. Do not polish a scene that
  should not exist. A line-level note on a section the author may cut is wasted.
- **Late draft** → weight Prose/line + AI-flatness. The bones are set; sharpen
  the skin.
Detect the stage from the draft (rough outline-ish vs near-final) or take an
assigned stage.

## What wastes everyone's time

- Vague "could be stronger" with no span and no cost.
- Restating the prose back to the author.
- Praising what works (capped above).
- Re-litigating a committed premise.
- Flagging a signature move as a defect (defensible choice, not a flaw).
- Inventing issues to look rigorous.

## Report format

1. **Overall assessment**: 1 to 3 sentences on does it ship, and the single
   biggest risk to a reader. At most one calibration line of praise.
2. **Findings by severity**: blocking first, then major, then minor. Each is a
   tuple (quoted span → dimension → severity → directed fix).
3. **Verdict**: exactly one of `ship` / `revise` / `structural-rework`, plus
   **the one highest-leverage fix** stated in a single sentence.

### Headless verdict block

In a non-interactive run, after the report, emit a machine-readable trailing HTML
comment (mirrors `writing-humanity-pass`):

```
<!-- writing-critique: {"verdict":"revise","serious_findings":["<one-line span+cost>", ...],"analyzer_flags":["<flag>", ...],"revise_target":"<the single finding to revise against>"} -->
```

`serious_findings` holds only blocking/major items. If `verdict` is `ship`,
`serious_findings` is `[]` and `revise_target` is `null`.
````

- [ ] **Step 2: Verify it renders and has no em dashes**

Run:
```bash
grep -nE '—|–| -- ' .claude/skills/writing-critique/references/finding-rubric.md && echo "DASH FOUND (fix)" || echo "clean: no dashes"
```
Expected: `clean: no dashes`.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/writing-critique/references/finding-rubric.md
git commit -m "feat(writing-critique): adversarial finding rubric + anti-sycophancy scaffolding"
```

---

## Task 5: The skill contract (`SKILL.md`)

**Files:**
- Create: `.claude/skills/writing-critique/SKILL.md`

**What it does:** The skill's front door. Mirrors `writing-humanity-pass` house style: trigger-rich frontmatter, two modes with the SAME interactive-vs-headless detection, the five dimensions, the analyzer's optional/degraded path, the explicit verdict, persona separation named as the mitigation for the same-model path, the one-grounded-revise-pass framing, the updated chain contract, Apache-2.0 attribution (mirroring how humanity-pass credits blader/humanizer), references, success criteria, copy/paste-ready.

> **Validate.py note:** frontmatter `name:` MUST equal the directory name `writing-critique`, and a `description:` field MUST be present, or validate.py warns. The body MUST contain at least one Markdown heading.

- [ ] **Step 1: Create `SKILL.md`**

Write the file exactly as below:

````markdown
---
name: writing-critique
description: Adversarially red-team a draft and return triaged, directable findings plus an explicit verdict and the single highest-leverage fix. Critiques execution across structure, value, voice, prose/line, and hiring signal; never rewrites. Runs standalone (on-demand red-team) and as the chain gate between writing-voice-modes and writing-humanity-pass, with the same interactive-vs-headless detection as writing-humanity-pass. Ships a stdlib analyzer (sentence-length burstiness, MATTR, opener variety) with a baseline captured from Sean's voice corpus. Use when asked to "red-team this draft", "what's weak here", "critique this", "find what doesn't work", "is this ready to ship", "what would a skeptical reader catch", or "review my draft".
---

# Writing Critique

## Purpose

Adversarial reading. Find what fails, not confirm what works. A critique that says
"well done" without digging creates false confidence and is worse than none. This
skill produces triaged, directable findings, an explicit verdict, and the one
highest-leverage fix. **It critiques; it never rewrites.** Fixes route back to
`writing-voice-modes` / `writing-humanity-pass` or to Sean.

It is the only *evaluative* stage in an otherwise generative chain: every other
writing skill produces; this one red-teams.

## When to Use

- "Red-team this draft", "what's weak here", "critique this", "find what doesn't
  work", "is this ready to ship", "what would a skeptical reader catch", "review
  my draft".
- As the chain gate between `writing-voice-modes` (compose) and
  `writing-humanity-pass` (scrub), on the voiced draft.
- Gating an agent-drafted post (e.g. Substack-Drafter) before it ships.

## The anti-sycophancy mitigation (why this skill is built the way it is)

Sycophancy is a measured consequence of RLHF, and self-enhancement bias is at its
worst when the same model that produced the draft also critiques it, which is
exactly the chain-gate path here (the model just ran `writing-voice-modes`). The
named mitigation is **hard persona separation**: the critic explicitly did NOT
write this draft and is a hostile expert reviewer. `references/finding-rubric.md`
encodes this plus per-finding grounding (quote + concrete reader cost) and a
severity-ranked floor (report fewer issues on a strong draft; never invent issues
to hit a count). Load that rubric before critiquing.

## Two modes (same interactive-vs-headless detection as writing-humanity-pass)

### Standalone (interactive)

1. Read the draft. Adopt the reviewer persona (you did not write this).
2. Detect or take the stage (early → structure + value; late → line + flatness).
3. Apply `references/finding-rubric.md` across the five dimensions.
4. Optionally run the analyzer for line-level evidence (see below).
5. Return: overall assessment → findings by severity → verdict + the one fix.
   **No rewrite.**

### Chain gate (headless, e.g. Substack-Drafter)

Detect non-interactive context the same way `writing-humanity-pass` does (no human
can answer a prompt in a launchd run). Then:

1. Run the analyzer with `--baseline references/baseline.json --json` and apply the
   rubric.
2. If any reader-cost (blocking/major) finding exists, emit **one** structured
   revise request, *"revise against [this specific finding]"*, routed back
   through `writing-voice-modes` (which carries Sean's calibrated target), then
   re-critique once.
3. Else pass through to `writing-humanity-pass`.
4. Always non-destructive. Emit the machine-readable verdict block as a trailing
   HTML comment (see the rubric's "Headless verdict block").

**One revise pass, grounded.** The cap is a proxy for the real lever: the single
pass must be anchored to an external target (a specific finding + Sean's voice
baseline), never "make it better." Un-anchored self-judged iteration degrades
prose toward bland/generic. Any second pass would require **new external input**
(a human note, a new finding from a different source), never a self-judged re-roll.

## The five dimensions

Each critiques execution and defers to the owning skill; never re-litigates the
premise.

1. **Structure** → defers to `storytelling-architecture` (hook, but/therefore
   seams, open-loop closure, slippery-slide ends).
2. **Value** → defers to `substack-value-engine` (Itch/Solution/Transfer
   delivered, seam is payoff not appendix, Rule-of-One, one usable thing in 10
   minutes).
3. **Voice** → defers to `writing-voice-modes` (signature moves present vs
   generic narrator; register drift).
4. **Prose / line** → rhythm, sentence variety, repetition, clarity, AI-flatness.
   **The analyzer plugs in here.**
5. **Hiring signal** (Sean-specific) → defers to `substack-value-engine`
   (judgment shown not claimed, artifact + blameless self-post-mortem, ask stays
   sideways).

## The analyzer (optional, advisory)

`references/analyze.py` is pure stdlib. It measures sentence-length burstiness
(coefficient of variation), lexical diversity (MATTR@50, MTLD fallback for short
drafts), opener variety, and repetition, and diffs them against
`references/baseline.json` (Sean's own voice corpus).

```bash
python3 references/analyze.py <draft.md> --baseline references/baseline.json
python3 references/analyze.py <draft.md> --baseline references/baseline.json --json   # chain gate
```

- It is **advisory**: it informs the revise decision and supplies evidence for a
  prose/line finding. It never blocks and is never a finding on its own.
- **Burstiness (sentence-length CV) is the headline signal**: the best-supported,
  analyzer-computable AI-flatness tell. Low CV vs the baseline → "monotonous vs
  your voice."
- Pronoun rate and MATTR are flagged **only** against the baseline, never as
  absolute AI signals (Sean's voice is pronoun-heavy and varied by design).
- **Degraded paths:** no Python in a headless run → critique proceeds
  qualitatively (the rubric still works). Missing/stale baseline → the analyzer
  falls back to its one absolute advisory (low CV) and logs that the baseline was
  absent. Tiny draft (a tweet) → it reports "insufficient length for variance
  signal" and MTLD low-confidence instead of a false flatness flag.

**Baseline regeneration:** when `writing-voice-modes/references/voice-samples.md`
gains a calibration round, re-extract the new Sean prose into
`references/baseline-corpus.md` (one passage per `## ` heading) and re-run
`python3 references/analyze.py --emit-baseline references/baseline-corpus.md --out references/baseline.json`.
The MATTR window is locked at 50; do not tune it.

## Verdict

Always explicit, exactly one of: `ship` / `revise` / `structural-rework`, plus the
single highest-leverage fix in one sentence.

## The chain after this change

```
storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass
   (beat SHAPE)               (value GATE)            (every SENTENCE)      (RED-TEAM, advisory)  (scrub + no em dash, LAST)
```

Critique sits between voice and humanity so `writing-humanity-pass` keeps its
"runs LAST" identity. The analyzer runs on the *voiced* draft (pre-scrub) and
informs the revise decision; humanity-pass still does the qualitative scrub
afterward. Critique is advisory, never rewrites, caps at one grounded revise pass,
and hands off in-context.

## Related Skills

- `storytelling-architecture`: owns structure; this skill critiques structural
  execution, never the chosen scaffold.
- `substack-value-engine`: owns the value gate + hiring signal; this skill checks
  they actually landed.
- `writing-voice-modes`: owns the sentences and Sean's signature moves; this skill
  routes a grounded revise request back here, and treats signature moves as
  defensible choices, not defects.
- `writing-humanity-pass`: runs after this skill. Its `references/ai-tells.md`
  evidence stratification shares this skill's measurable signals (burstiness,
  MATTR, pronoun rate) and the same analyzer.

## Attribution

The critique rubric and the analyzer mechanics are adapted from the
`prose-critique` skill in
[`haowjy/creative-writing-skills`](https://github.com/haowjy/creative-writing-skills)
(Apache License 2.0). Attribution retained, mirroring how `writing-humanity-pass`
credits `blader/humanizer`. The citations in the evidence tiers were re-grounded
for this repo (a deliberate divergence from upstream); MATTR, the thresholds, and
the baseline pipeline are new additions, not ports.

## References

- `references/finding-rubric.md`: the adversarial mindset, persona separation, the
  four-quality finding rubric, the five dimensions, stage calibration, and the
  report + headless-verdict format. Load before critiquing.
- `references/analyze.py`: the stdlib mechanical analyzer (advisory).
- `references/baseline.json`: Sean's precomputed voice baseline (regenerable).
- `references/baseline-corpus.md`: the Sean-only prose the baseline is built from.

## Success Criteria

- [ ] Findings are specific (quoted span), reasoned (named reader cost),
      directable, and non-obvious, never spellcheck.
- [ ] The critic persona is separated ("you did not write this"), especially in
      the chain gate.
- [ ] Severity-ranked floor honored: a strong draft yields fewer findings, never
      invented ones; praise is capped to one line.
- [ ] Verdict is explicit (`ship` / `revise` / `structural-rework`) + the one fix.
- [ ] The skill never rewrites; fixes route to voice-modes / humanity-pass / Sean.
- [ ] Headless runs emit the machine-readable verdict block.
- [ ] The analyzer stays advisory; burstiness/MATTR/pronoun flags are
      baseline-relative (pronoun rate never absolute).

## Copy/Paste Ready

```
"Red-team this draft"
"What's weak here? Be a hostile reviewer"
"Critique this, find what doesn't work"
"Is this ready to ship?"
"What would a skeptical reader catch?"
"Run the analyzer against my voice baseline"
"Critique gate this before humanity-pass"
```
````

- [ ] **Step 2: Verify frontmatter, headings, and no dashes**

Run:
```bash
head -5 .claude/skills/writing-critique/SKILL.md
grep -nE '—|–| -- ' .claude/skills/writing-critique/SKILL.md && echo "DASH FOUND (fix)" || echo "clean: no dashes"
```
Expected: frontmatter shows `name: writing-critique` + a `description:`; `clean: no dashes`.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/writing-critique/SKILL.md
git commit -m "feat(writing-critique): SKILL.md two modes, 5 dimensions, persona-separation mitigation, verdict"
```

---

## Task 6: Wire the critique stage into `writing-humanity-pass/SKILL.md`

**Files:**
- Modify: `.claude/skills/writing-humanity-pass/SKILL.md`

**What it does:** Insert the critique stage into humanity-pass's chain diagram and chaining-order sentence (humanity-pass still runs LAST), and add a References pointer to the upgraded ai-tells stratification + the writing-critique analyzer.

- [ ] **Step 1: Update the Integration chain diagram**

Replace (the fenced block under "This skill runs LAST in the chain. The full Substack pipeline:"):
```
storytelling-architecture  →  substack-value-engine  →  writing-voice-modes  →  writing-humanity-pass
   (beat SHAPE + order)        (value GATE + payoff)       (every SENTENCE)        (scrub + no em dash)
```
with:
```
storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass
   (beat SHAPE + order)       (value GATE + payoff)    (every SENTENCE)      (RED-TEAM, advisory)  (scrub + no em dash)
```

- [ ] **Step 2: Update the chaining-order sentence**

Replace:
```
- Chaining order: shape with `storytelling-architecture` + `substack-value-engine`, compose with `writing-voice-modes` (plus `creative-writing` for format, `technical-writing` for clarity), then run `writing-humanity-pass` LAST.
```
with:
```
- Chaining order: shape with `storytelling-architecture` + `substack-value-engine`, compose with `writing-voice-modes` (plus `creative-writing` for format, `technical-writing` for clarity), red-team with `writing-critique` (advisory; one grounded revise pass max), then run `writing-humanity-pass` LAST.
```

- [ ] **Step 3: Add a References pointer to the evidence stratification + analyzer**

Replace:
```
- `references/ai-tells.md`: all 30 patterns, adapted to Sean's output, each tagged `[SLOP]` (always cut) or `[CLASH->move]` (defer in voice-safe).
```
with:
```
- `references/ai-tells.md`: all 30 patterns, adapted to Sean's output, each tagged `[SLOP]` (always cut) or `[CLASH->move]` (defer in voice-safe). Its "Evidence quality" section stratifies the catalog by how well each tell is supported, and wires the measurable, baseline-relative signals (sentence-length burstiness, MATTR, pronoun rate) to the `writing-critique` analyzer (`.claude/skills/writing-critique/references/analyze.py` + `baseline.json`).
```

- [ ] **Step 4: Verify and commit**

Run: `grep -nE '—|–| -- ' .claude/skills/writing-humanity-pass/SKILL.md && echo "DASH FOUND" || echo "clean"`
Expected: `clean` (the new text uses `→` arrows, which are allowed in diagrams; the dash guard targets em/en/double-hyphen only — confirm no `—`/`–`/` -- ` slipped in).
```bash
git add .claude/skills/writing-humanity-pass/SKILL.md
git commit -m "docs(writing-humanity-pass): insert critique stage in chain + point ai-tells at analyzer"
```

---

## Task 7: Update the chain diagrams in the other three writing skills

**Files:**
- Modify: `.claude/skills/storytelling-architecture/SKILL.md`
- Modify: `.claude/skills/substack-value-engine/SKILL.md`
- Modify: `.claude/skills/writing-voice-modes/SKILL.md`

**What it does:** Every skill that hardcodes the chain diagram must show the 5-stage chain so the cross-references stay consistent.

- [ ] **Step 1: `storytelling-architecture/SKILL.md` — Chain Contract diagram**

Replace (the fenced block under "## The Chain Contract"):
```
storytelling-architecture  →  substack-value-engine  →  writing-voice-modes  →  writing-humanity-pass
   (beat SHAPE + order)        (value GATE + payoff)       (every SENTENCE)        (scrub + no em dash)
```
with:
```
storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass
   (beat SHAPE + order)       (value GATE + payoff)    (every SENTENCE)      (RED-TEAM, advisory)  (scrub + no em dash)
```

- [ ] **Step 2: `storytelling-architecture/SKILL.md` — Related Skills bullet**

After the `writing-voice-modes:` bullet in "## Related Skills", insert a new bullet:
```
- `writing-critique`: red-teams the voiced draft between voice and humanity-pass. It critiques structural execution (hook, but/therefore seams, loop closure) but never re-litigates the beat map this skill committed.
```

- [ ] **Step 3: `substack-value-engine/SKILL.md` — Chain Contract diagram**

Replace (the fenced block under "## The Chain Contract"):
```
storytelling-architecture  →  substack-value-engine  →  writing-voice-modes  →  writing-humanity-pass
   (beat SHAPE + order)        (value GATE + payoff)       (every SENTENCE)        (scrub + no em dash)
```
with:
```
storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass
   (beat SHAPE + order)       (value GATE + payoff)    (every SENTENCE)      (RED-TEAM, advisory)  (scrub + no em dash)
```

- [ ] **Step 4: `substack-value-engine/SKILL.md` — Related Skills bullet**

After the `writing-voice-modes:` bullet in "## Related Skills", insert:
```
- `writing-critique`: red-teams the voiced draft. It checks whether the Value Gate and hiring signal actually landed (Itch/Solution/Transfer delivered, ask stays sideways) but defers to this skill on the gate itself; it critiques execution, not the verdict.
```

- [ ] **Step 5: `writing-voice-modes/SKILL.md` — inline chain in "## Related Skills"**

Replace:
```
This skill is the SENTENCE author in the Substack chain: `storytelling-architecture` → `substack-value-engine` → **`writing-voice-modes`** → `writing-humanity-pass`. The two upstream skills emit a beat map (story shape + value gate); voice-modes writes 100% of the prose fresh against it and must never reorder beats.
```
with:
```
This skill is the SENTENCE author in the Substack chain: `storytelling-architecture` → `substack-value-engine` → **`writing-voice-modes`** → `writing-critique` → `writing-humanity-pass`. The two upstream skills emit a beat map (story shape + value gate); voice-modes writes 100% of the prose fresh against it and must never reorder beats. The downstream `writing-critique` gate may route ONE grounded revise request back here ("revise against [this specific finding]"); voice-modes writes that revision, still without reordering beats.
```

- [ ] **Step 6: `writing-voice-modes/SKILL.md` — add a Related Skills bullet**

After the `writing-humanity-pass:` bullet (the last bullet in "## Related Skills"), insert:
```
- `writing-critique`: the adversarial gate that runs after voice and before humanity-pass. It never rewrites; when it finds a reader-cost defect it sends a single grounded revise request back to this skill. It treats Sean's signature moves as defensible choices, not defects.
```

- [ ] **Step 7: Verify all three and commit**

Run:
```bash
for f in storytelling-architecture substack-value-engine writing-voice-modes; do \
  grep -nE '—|–| -- ' .claude/skills/$f/SKILL.md && echo "DASH in $f" || echo "$f clean"; done
grep -rl "writing-critique" .claude/skills/storytelling-architecture/SKILL.md .claude/skills/substack-value-engine/SKILL.md .claude/skills/writing-voice-modes/SKILL.md
```
Expected: all three `clean`; all three files listed (each now references writing-critique).
```bash
git add .claude/skills/storytelling-architecture/SKILL.md .claude/skills/substack-value-engine/SKILL.md .claude/skills/writing-voice-modes/SKILL.md
git commit -m "docs(writing-chain): insert writing-critique stage in all chain diagrams + related-skills"
```

---

## Task 8: The `ai-tells.md` evidence upgrade (re-grounded citations)

**Files:**
- Modify: `.claude/skills/writing-humanity-pass/references/ai-tells.md`

**What it does:** Additive and surgical. **Keeps all 30 patterns untouched.** Replaces the single closing "## Detection guidance" section with a full "## Evidence quality" stratification that bakes in research deltas 1–5: split the top tier into measurable+baseline-relative vs research-cited-qualitative; re-ground Kobak to its real claim and move RAID/Ghostbuster to a detection-caution note; reword the slop bullet (drop "near-random" / "for Claude specifically", note the deliberate divergence from upstream); promote burstiness; make pronoun-rate strictly baseline-relative; keep the em-dash ban labeled as an owned taste choice, not detection.

> **Do not touch patterns #1–#30 or the tag legend.** Only the closing section changes.

- [ ] **Step 1: Replace the closing section**

Replace the entire current closing block:
```
---

## Detection guidance

See SKILL.md "What NOT to Flag" and "Signs of Human Writing." Rule of thumb: rewrite on clusters of tells, never on a single isolated one. When the text is Sean's voice, the signature moves in `voice-safe-exceptions.md` are protected.
```
with:
````markdown
---

## Evidence quality

The 30 patterns above are useful editing triggers, but they are not equally
well-supported as "AI detection." This section stratifies them by how strong the
evidence is, and wires the measurable ones to the `writing-critique` analyzer
(`.claude/skills/writing-critique/references/analyze.py` + `baseline.json`). The
honest framing matters: an over-claimed tell that flags Sean's own voice destroys
trust in the whole catalog.

> Citations here were re-grounded against primary sources and deliberately diverge
> from the upstream `creative-writing-skills/antipatterns.md` they were adapted
> from. Two upstream cites (BEA 2025, Nature HSSCOMMS 2025) were NOT carried over
> because they were not verified; do not re-import them without reading them.

### Tier A1: Measurable AND baseline-relative (wired to the analyzer)

These can be computed from the draft and compared against Sean's own voice
baseline. Treat them as evidence for a finding, never as a finding alone; all are
advisory.

- **Burstiness / sentence-length coefficient of variation (σ/μ).** The
  best-supported, analyzer-computable AI-flatness signal: humans vary sentence
  length more (higher CV), AI is smoother. Low CV vs Sean's baseline → "monotonous
  vs your voice." (Decoding AI Authorship, arXiv:2603.23219 / arXiv:2408.00769.)
  This is the headline measurable tell. Relates to "variety in sentence length" in
  SKILL.md's "Signs of Human Writing."
- **Lexical variability (MATTR@50).** Lower lexical diversity shows up in AI text
  **relative to a comparison class**: lower than polished/expert human prose, but
  *higher* than L2 / constrained-vocabulary writers. So it is only meaningful
  against a baseline, never as an absolute "AI = low diversity" claim. (Diversity
  Boosts AI-Generated Text Detection, arXiv:2509.18880; human-vs-AI TTR 55.3 vs
  45.5, SSRN 5833302. MATTR is itself window/length-sensitive (arXiv:2507.15092),
  which is why the window is locked at 50.)
- **Personal-pronoun rate, STRICTLY baseline-relative, NEVER absolute.** Sean's
  calibrated modes are pronoun-heavy by design; an absolute "low pronouns = AI"
  check would flag his *most* characteristic prose. Only flag a drop below Sean's
  own first-person-rate baseline. (No support among the detection papers for an
  absolute claim; treat as a heuristic.)

### Tier A2: Research-cited but qualitative (NOT analyzer-measurable)

- **Positive-emotion skew** ("more positive-emotion language even in dark scenes").
  A reviewer cue only. There is no sentiment lexicon in the stdlib analyzer, so
  this **cannot be wired** to `analyze.py`. Thin independent evidence; use as a
  human read, not a metric.

### Detection-caution note (why two former "support" cites are NOT evidence)

- **Kobak et al. (2024):** kept, but for its *real* claim: LLMs leave a detectable
  **word-frequency fingerprint** (excess vocabulary in scientific abstracts),
  genre- and model-bound. This supports the slop-list framing below, NOT the
  lexical-*diversity* signal (excess vocabulary is the opposite construct from
  vocabulary diversity). (arXiv:2406.07016.)
- **RAID (ACL 2024)** and **Ghostbuster (NAACL 2024)** are a detection benchmark and
  a black-box classifier. They make **no per-feature stylometric claim**. Citing
  them as evidence for a human-readable tell is a category error. Keep them only as
  cautions: RAID's standing result is that any fixed surface signal degrades on
  unseen models and under simple manipulation; Ghostbuster shows likelihood-feature
  classifiers can detect AI text but expose no interpretable tell.
  (arXiv:2405.07940; arXiv:2305.15047.)

### Tier B: Community folklore (useful triggers, not proof)

Widely recognized, largely unstudied. Good editing prompts; not detection evidence:
clean-but-hollow prose, tidy-summary endings, repetitive emotional choreography,
overused metaphor clusters. Most of the structural patterns (#1, #25, #29) live
here.

### Tier C: Not reliable: word-level slop lists

Word-level slop lists (pattern #7 territory) are largely derived from GPT-era
output in specific genres; they transfer poorly across models and domains, and
their hit-rate against Claude in particular is lower and unreliable. Treat them as
**editorial taste choices, not a model-agnostic detection signal.** (This is a
deliberate divergence from upstream's verbatim "near-random for Claude
specifically" line. The claim rests on a model/genre-transfer argument, not a
measured Claude-specific hit-rate.)

### The em-dash ban is an owned taste choice, NOT detection

Pattern #14 (em/en dashes) stays a **hard cut**, but its category is honest: Sean
retired the em dash as a deliberate voice choice. It is not listed here as a
"research-backed AI tell." It is a rule Sean owns. (See SKILL.md "The Em-Dash Hard
Rule.")

## Detection guidance

See SKILL.md "What NOT to Flag" and "Signs of Human Writing." Rule of thumb:
rewrite on clusters of tells, never on a single isolated one. When the text is
Sean's voice, the signature moves in `voice-safe-exceptions.md` are protected. For
the measurable signals (burstiness, MATTR, pronoun rate), the `writing-critique`
analyzer supplies baseline-relative evidence; it is advisory and never blocks.
````

- [ ] **Step 2: Confirm all 30 patterns survived and no dashes were introduced**

Run:
```bash
grep -cE '^\*\*#[0-9]+\.' .claude/skills/writing-humanity-pass/references/ai-tells.md
grep -nE '—|–| -- ' .claude/skills/writing-humanity-pass/references/ai-tells.md && echo "DASH FOUND" || echo "clean"
```
Expected: pattern count `30` unchanged; `clean`.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/writing-humanity-pass/references/ai-tells.md
git commit -m "docs(ai-tells): re-grounded evidence stratification (burstiness promoted, citations fixed)"
```

---

## Task 9: Evals (`evals.yaml` + `evals.sealed.yaml`)

**Files:**
- Create: `.claude/skills/writing-critique/evals.yaml`
- Create: `.claude/skills/writing-critique/evals.sealed.yaml`

**What it does:** Manual-review schema (`schema_version: 1`, `cases` / `surprise_cases` with `id`/`input`/`expect`), modeled on `storytelling-architecture/evals.yaml`. Cases test the SHAPE of the critique output, not prose. **Delta #9:** `flags_ai_flatness_with_analyzer` is written against the **CV / baseline-relative** signal, not the absolute stdev, so the sealed eval never ossifies a weak constant.

- [ ] **Step 1: Create `evals.yaml`**

Write exactly:
```yaml
# Eval suite for writing-critique.
# Manual-review schema (input -> expected critique-output properties). Not wired to skill_optimizer.
# These test the SHAPE of the critique (findings, verdict, deferral, advisory analyzer),
# never prose. The skill critiques, it never rewrites.
schema_version: 1

cases:
  - id: finds_reader_cost_not_typos
    input: "Critique this draft intro: a structurally flat 200-word piece whose hook promises a vague 'secret to great AI products' and whose value section is a bolted-on '5 tips' list. Also it has one typo."
    expect:
      - "leads with a reader-cost finding (vague chasm hook OR bolted-on value seam), not the typo"
      - "each finding cites a span and names the concrete reader cost"
      - "the typo, if mentioned at all, is a minor, ranked below the structural findings"

  - id: findings_are_directable
    input: "Red-team this post and make sure I know what to do next with each note."
    expect:
      - "every finding is a tuple: quoted span -> why it fails (dimension) -> severity -> directed fix"
      - "no vague 'could be stronger' findings with no action"
      - "the author can act on each finding without guessing"

  - id: defers_to_owner_skill
    input: "Critique this: the Value Gate already PASSED (real itch, artifact, concrete transfer), but the post buries the artifact in paragraph 9."
    expect:
      - "critiques execution (artifact buried too late) without re-litigating the passed Value Gate"
      - "defers the gate verdict itself to substack-value-engine"
      - "frames it as a value-DELIVERY finding, not a premise argument"

  - id: verdict_is_explicit
    input: "Is this ready to ship? Give me a straight answer."
    expect:
      - "output ends with exactly one verdict: ship / revise / structural-rework"
      - "names the single highest-leverage fix in one sentence"

  - id: never_rewrites
    input: "This paragraph is flat. Critique it."
    expect:
      - "returns findings about the flatness, NOT a rewritten paragraph"
      - "if a fix is needed, routes it back to writing-voice-modes / writing-humanity-pass / Sean"
      - "no rewritten prose appears in the output"

  - id: flags_ai_flatness_with_analyzer
    input: "Critique this draft where every sentence is nearly the same length and opens with 'The system': run the analyzer against my baseline."
    expect:
      - "surfaces a prose/line flatness finding grounded in the analyzer's sentence-length CV (burstiness), NOT an absolute stdev cutoff"
      - "frames the flatness as baseline-relative ('monotonous vs your voice'), not an absolute AI verdict"
      - "treats the analyzer output as advisory evidence for the finding, never as a finding on its own"

  - id: persona_separation_when_same_model_voiced_it
    input: "You just wrote this draft in voice-modes. Now critique it as the chain gate."
    expect:
      - "adopts the hostile-reviewer persona explicitly ('you did not write this')"
      - "does not flatter its own prior output (no self-enhancement praise)"
      - "praise is capped to at most one calibration line"
```

- [ ] **Step 2: Create `evals.sealed.yaml`**

Write exactly:
```yaml
# SEALED surprise cases for writing-critique. Held out to test generalization.
# Same manual-review schema as evals.yaml. Do not train/tune against these.
schema_version: 1

surprise_cases:
  - id: headless_emits_structured_verdict
    input: "[non-interactive chain-gate run] Critique this voiced Substack draft before humanity-pass."
    expect:
      - "no interactive question is asked (headless detected, like writing-humanity-pass)"
      - "emits a trailing HTML comment verdict block: {verdict, serious_findings[], analyzer_flags[], revise_target}"
      - "serious_findings holds only blocking/major items; revise_target is null when verdict is ship"

  - id: adversarial_not_hypercritical
    input: "Critique this genuinely strong, tight draft with a real itch, a closeable hook, and visible artifact."
    expect:
      - "reports FEWER findings (severity-ranked floor), does not invent issues to fill a quota"
      - "does not flag Sean's signature moves (pronoun-heavy voice, polysyndeton, self-deprecation) as defects"
      - "verdict can be ship; honesty over manufactured criticism"

  - id: revise_routes_through_voice_grounded
    input: "[chain gate] You found one blocking reader-cost defect. Issue the revise request."
    expect:
      - "emits ONE revise request phrased as 'revise against [the specific finding]', routed to writing-voice-modes"
      - "does not rewrite the draft itself"
      - "states that any second pass would require new external input, not a self-judged re-roll"
```

- [ ] **Step 3: Validate YAML parses and commit**

Run:
```bash
python3 -c "import yaml,sys; [yaml.safe_load(open(f)) for f in ['.claude/skills/writing-critique/evals.yaml','.claude/skills/writing-critique/evals.sealed.yaml']]; print('yaml ok')"
```
Expected: `yaml ok`. (If PyYAML is not on system python, use the agents-sdk venv: `agents-sdk/.venv/bin/python3`.)
```bash
git add .claude/skills/writing-critique/evals.yaml .claude/skills/writing-critique/evals.sealed.yaml
git commit -m "test(writing-critique): manual-review evals (flatness eval uses CV, not absolute stdev)"
```

---

## Task 10: Repo integration (CHANGELOG, README, CLAUDE.md, export-groups, validate)

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `README.md`
- Verify (likely no numeric edit): `CLAUDE.md`
- Verify (no edit expected): `export-groups/*/playground.json`

**What it does:** Records the new skill + the ai-tells upgrade per CLAUDE.md "When Modifying," bumps the headline skill count, and runs the validator clean.

- [ ] **Step 1: Add the CHANGELOG entry**

In `CHANGELOG.md`, under `## [Unreleased]` → `### Added`, insert this bullet as the FIRST item in the Added list (immediately before the existing `- **`storytelling-architecture` + `substack-value-engine` skills...` bullet):
```
- **`writing-critique` skill (the adversarial gate) + `ai-tells.md` evidence re-grounding.** A new evaluative stage inserted between `writing-voice-modes` and `writing-humanity-pass`, completing a five-skill chain: `storytelling-architecture` -> `substack-value-engine` -> `writing-voice-modes` -> **`writing-critique`** -> `writing-humanity-pass`. Every prior stage *produces*; this one *red-teams*. It returns triaged, directable findings + an explicit verdict (`ship`/`revise`/`structural-rework`) + the single highest-leverage fix across five dimensions (structure, value, voice, prose/line, hiring signal), each deferring to the skill that owns it. **It critiques; it never rewrites** — fixes route back to voice-modes/humanity-pass or to Sean, capped at one *grounded* revise pass ("revise against [this specific finding]") because un-anchored self-judged iteration degrades prose toward generic. Built with structural anti-sycophancy scaffolding (hard persona separation, per-finding grounding, a severity-ranked floor that reports FEWER issues on a strong draft instead of a forced count) because self-enhancement bias is worst exactly in the chain-gate path where the same model just voiced the draft. Ships `references/analyze.py`, a pure-stdlib mechanical analyzer (sentence-length burstiness via coefficient of variation, MATTR@50 with an MTLD-Original fallback for short drafts, opener variety, repetition) that diffs a draft against `references/baseline.json` — a regenerable baseline computed from Sean's own voice corpus (`references/baseline-corpus.md`, six passages spanning all five modes). The analyzer is advisory and never blocks; burstiness/MATTR/pronoun flags are strictly baseline-relative (pronoun rate is never absolute — Sean's voice is pronoun-heavy by design). Adapted from the `prose-critique` skill in [`haowjy/creative-writing-skills`](https://github.com/haowjy/creative-writing-skills) (Apache-2.0): the rubric and analyzer mechanics are a faithful port; MATTR, the CV threshold, and the baseline pipeline are new additions. The companion change re-grounds `writing-humanity-pass/references/ai-tells.md` (additive, all 30 patterns kept): the evidence tier is split into measurable-and-baseline-relative (burstiness promoted to the headline signal, MATTR with its comparison-class caveat, baseline-relative pronoun rate) vs research-cited-but-qualitative (positive-emotion skew, not stdlib-measurable); Kobak is kept only for its real word-frequency-fingerprint claim; RAID + Ghostbuster are moved out of "support" into a detection-caution note; the slop-list bullet drops the unverifiable "near-random for Claude specifically" line (a deliberate divergence from upstream); the em-dash ban is labeled an owned taste choice, not detection. Citations were fact-checked against primary sources; two upstream cites (BEA 2025, Nature HSSCOMMS) were intentionally not carried over. Ships `SKILL.md`, four `references/` files, and an `evals.yaml` + `evals.sealed.yaml` pair (manual-review schema; the flatness eval is written against CV, not an absolute stdev, so the sealed eval doesn't lock in a weak constant). Design + research spine: [2026-06-02-writing-critique-layer-design.md](.claude/skills/writing-critique/drafts/2026-06-02-writing-critique-layer-design.md), [2026-06-02-writing-critique-research-findings.md](.claude/skills/writing-critique/drafts/2026-06-02-writing-critique-research-findings.md). Skill count 122 -> 123. Not yet in an export group (personal-use writing companion, like `writing-humanity-pass`; follow-up tracked).
```

- [ ] **Step 2: Bump the README headline count**

In `README.md` line ~5, replace `**122** skills` with `**123** skills`.

Run to confirm the exact string and that it is unique:
```bash
grep -n "122\*\* skills\|\*\*122\*\* skills" README.md
```
Apply the edit (`**122** skills` → `**123** skills`).

- [ ] **Step 3: Add writing-critique to the README export-group exclusion note**

In `README.md` line ~95, the sentence currently reads:
```
> The 12 export groups roll up 117 of the 120 skills. The `llm-council` skill (v3.35.0), `openai-image-gen` skill (v4.1.2), and `writing-humanity-pass` skill are not in any export group. All three are personal-use companions that depend on in-tree assets or pair with another skill, so they don't ship via the installer. See [`tools/llm-council/README.md`](tools/llm-council/README.md) and [`.claude/skills/openai-image-gen/SKILL.md`](.claude/skills/openai-image-gen/SKILL.md).
```
Replace it with:
```
> The 12 export groups roll up 117 of the 120 base skills. The `llm-council` skill (v3.35.0), `openai-image-gen` skill (v4.1.2), `writing-humanity-pass` skill, and `writing-critique` skill are not in any export group. All four are personal-use companions that depend on in-tree assets or pair with another skill, so they don't ship via the installer. See [`tools/llm-council/README.md`](tools/llm-council/README.md) and [`.claude/skills/openai-image-gen/SKILL.md`](.claude/skills/openai-image-gen/SKILL.md).
```
(Note: the "120 base skills" figure on README line ~93 is a pre-existing export-group framing that already lags the line-5 headline count; reconciling it fully is out of scope. Do not introduce a NEW inconsistency, but this `+1` lands on the headline count, which is the authoritative one.)

- [ ] **Step 4: Verify CLAUDE.md has no hardcoded skill count to bump**

Run:
```bash
grep -nE "1[0-9][0-9] skills|skill count|skills\b.*1[0-9][0-9]" CLAUDE.md
```
Expected: no hardcoded total (CLAUDE.md line 7 says "Live counts via `ls .claude/{skills,agents,hooks}/`"). If the grep finds a real count table, +1 it; if not (expected), no CLAUDE.md numeric edit is needed — record that CLAUDE.md uses live counts so the "+1" requirement is satisfied by the README headline bump.

- [ ] **Step 5: Confirm no export-group manifest references writing-critique**

`writing-critique` is intentionally NOT added to any export group (personal-use companion, mirroring `writing-humanity-pass`). Confirm nothing needs editing:
```bash
grep -rl "writing-critique" export-groups/ presets/ 2>/dev/null || echo "no export-group references (correct)"
```
Expected: `no export-group references (correct)`. Do NOT add it to a `playground.json`.

- [ ] **Step 6: Run the validator — must be clean**

Run: `python3 scripts/validate.py`
Expected: `Found 123 skills in .claude/skills/`, zero errors, zero warnings about `writing-critique` (the previous "missing SKILL.md" error for the drafts-only dir is now resolved). If validate.py warns `Skill dir 'writing-critique' vs frontmatter name '...'`, the SKILL.md `name:` does not equal `writing-critique` — fix Task 5.

- [ ] **Step 7: Commit**

```bash
git add CHANGELOG.md README.md
git commit -m "docs: changelog + README count for writing-critique (122 -> 123)"
```

---

## Task 11: End-to-end verification (analyzer self-test + real critique dry run)

**Files:** none created — this is a verification gate.

- [ ] **Step 1: Analyzer reports HEALTHY variance on Sean's own corpus**

Run:
```bash
python3 .claude/skills/writing-critique/references/analyze.py \
  .claude/skills/writing-critique/references/baseline-corpus.md \
  --baseline .claude/skills/writing-critique/references/baseline.json
```
Expected: the burstiness block does NOT raise the monotony flag (Sean's prose is bursty), and the "Baseline-Relative Flags" block reads "(within your baseline ranges)" or fires nothing meaningful (the corpus IS the baseline, so it should sit inside its own ranges).

- [ ] **Step 2: Analyzer FLAGS a deliberately monotone specimen against the baseline**

Run:
```bash
printf '# t\n\nThe system runs the job. The system logs the output. The system writes the file. The system checks the value. The system sends the report. The system closes the loop.\n' > /tmp/flat.md
python3 .claude/skills/writing-critique/references/analyze.py /tmp/flat.md \
  --baseline .claude/skills/writing-critique/references/baseline.json
```
Expected: the CV monotony flag fires AND the baseline-relative flags include "monotonous vs your voice" (and likely "narrower vocabulary vs your voice").

- [ ] **Step 3: `--json` produces a parseable chain-gate payload**

Run:
```bash
python3 .claude/skills/writing-critique/references/analyze.py /tmp/flat.md \
  --baseline .claude/skills/writing-critique/references/baseline.json --json \
  | python3 -m json.tool > /dev/null && echo "json ok"
```
Expected: `json ok` (top-level keys `metrics` + `baseline_flags`).

- [ ] **Step 4: Tiny-draft guard (no false flatness flag on a tweet)**

Run:
```bash
printf 'Claude finished 7 tasks and I did not finish my eggs. Good ass morning.\n' > /tmp/tweet.md
python3 .claude/skills/writing-critique/references/analyze.py /tmp/tweet.md
```
Expected: lexical-diversity block reports MTLD as primary with `[low confidence]` and the "draft < 60 tokens" note; no confident flatness claim.

- [ ] **Step 5: Real standalone critique dry run (skill behavior, manual)**

Pick one existing Substack draft under `.claude/skills/*/drafts/` or `vault/` and run the skill interactively: load `writing-critique`, read the draft, apply `finding-rubric.md` across the five dimensions, optionally run the analyzer with `--baseline`. Confirm by inspection:
- findings are specific + directable (each a quoted-span tuple),
- the verdict is explicit (`ship`/`revise`/`structural-rework`) + one fix,
- nothing was rewritten,
- signature moves were not flagged as defects.

- [ ] **Step 6: Full validator + dash sweep across all touched files**

Run:
```bash
python3 scripts/validate.py
grep -rlE '—|–| -- ' .claude/skills/writing-critique/ \
  && echo "DASH in writing-critique (fix)" || echo "writing-critique clean of dashes"
```
Expected: validator clean (`Found 123 skills`, no errors); `writing-critique clean of dashes` (the analyzer prints `→` arrows only in skill prose, never em/en/double-hyphen).

- [ ] **Step 7: Final commit (if Step 5 surfaced any doc tweaks)**

```bash
git add -A .claude/skills/writing-critique/
git commit -m "chore(writing-critique): end-to-end verification pass" || echo "nothing to commit"
```

---

## Plan self-review — spec coverage map

| Requirement (spec + research deltas + kickoff) | Task |
|---|---|
| New `writing-critique` skill, advisory, never rewrites, standalone + chain gate | 4, 5 |
| Interactive-vs-headless detection mirrors `writing-humanity-pass`; headless verdict block | 4 (block), 5 (modes) |
| Five dimensions, each defers to owner; critique execution not premise | 4, 5 |
| Stage calibration ("fix the bones before the skin") | 4 |
| Explicit verdict (`ship`/`revise`/`structural-rework`) + the one fix | 4, 5, 9 |
| Apache-2.0 attribution in SKILL.md + analyze.py header (mirrors humanity-pass) | 1 (header), 5 (attribution) |
| Faithful port of rubric + analyzer mechanics; pstdev kept; rep-window vs MATTR-window kept distinct | 1, 4 |
| Delta 1 — re-ground citations (Kobak only for word-frequency; RAID/Ghostbuster → caution; real diversity cites w/ caveat; no BEA/Nature) | 8 |
| Delta 2 — split top tier (measurable+baseline-relative vs research-cited-qualitative) | 8 |
| Delta 3 — promote burstiness / sentence-length CV to first-class measurable | 1, 8 |
| Delta 4 — reword slop bullet (drop "near-random"/"for Claude"; keep transfer argument; note divergence) | 8 |
| Delta 5 — pronoun rate strictly baseline-relative | 1 (`baseline_flags`), 8 |
| Delta 6 — MATTR locked@50; MTLD-Original 0.72 fallback <60 tokens; no HD-D/vocd-D; CV<0.45 replaces stdev<4; div-by-zero guard; advisory | 1 |
| Delta 7 — structural anti-sycophancy scaffolding (persona separation, per-finding grounding, severity-ranked floor, capped praise) | 4 |
| Delta 8 — SKILL names persona separation as the same-model mitigation; revise framed as "revise against [finding]" via voice-modes; 2nd pass needs new external input | 5 |
| Delta 9 — `flags_ai_flatness_with_analyzer` written against CV/baseline-relative, not absolute stdev | 9 |
| Drop dialogue-ratio (clean removal) | 1 (omitted from port) |
| Baseline pipeline: `baseline-corpus.md` extraction + `baseline.json` via `--emit-baseline` | 2, 3 |
| evals.yaml + evals.sealed.yaml, manual-review schema | 9 |
| ai-tells.md upgrade keeps all 30 patterns (additive) | 8 |
| Chain-diagram updates across all four existing writing skills | 6, 7 |
| Pointer from humanity-pass SKILL.md to the stratification + analyzer | 6 |
| CHANGELOG entry; +1 README headline count; CLAUDE.md verified (live counts); validate.py clean | 10 |
| Apache-2.0 attribution form mirrors how humanity-pass credits blader/humanizer | 1, 5 |
| End-to-end dry run (healthy-corpus + monotone specimen + tiny-draft guard + real critique) | 11 |

**Locked decisions honored (not relitigated):** em-dash ban (dash sweeps in every task); chain position between voice and humanity (6, 7); five voice modes (corpus spans all five, Task 2); advisory-not-blocking (1, 4, 5); one-revise-pass cap (5); packaging Approach A — analyzer + baseline in `writing-critique`, evidence upgrade an in-place `ai-tells.md` edit (1–3 vs 8); drop dialogue-ratio (1); baseline = voice-samples corpus (2).

**Type/name consistency check (cross-task):** analyzer public surface referenced by tests, SKILL.md, and Task 11 is consistent — `MATTR_WINDOW`, `strip_frontmatter_and_fences`, `words`, `sentence_length_stats` (keys `cv`, `monotony_flag`, `pstdev`, `note`), `mattr`, `mtld`, `lexical_diversity` (keys `mattr`, `mtld`, `primary_metric`, `low_confidence`), `opener_variety` (key `other_pct`), `pronoun_distribution` (key `first_person_rate`), `repetition`, `compute_metrics`, `emit_baseline`, `baseline_flags`, `segment_corpus`. CLI flags consistent everywhere: `--baseline`, `--emit-baseline`, `--out`, `--json`, `--rep-window`. Baseline JSON metric keys consistent between `emit_baseline` (writes `cv`/`mattr`/`first_person_rate`/`opener_other_pct`) and `baseline_flags` (reads the same four).

---

## Execution handoff

Plan complete and saved to `.claude/skills/writing-critique/drafts/2026-06-02-writing-critique-implementation-plan.md`. Two execution options:

1. **Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks, fast iteration (`superpowers:subagent-driven-development`).
2. **Inline Execution** — execute tasks in this session with checkpoints (`superpowers:executing-plans`).

Suggested batching for review checkpoints: **Task 1** (the analyzer — the one load-bearing artifact; review the code closely), **Tasks 2–3** (corpus + baseline), **Tasks 4–5** (rubric + SKILL.md), **Tasks 6–8** (chain + ai-tells edits — all surgical string edits), **Task 9** (evals), **Tasks 10–11** (integration + verification).
