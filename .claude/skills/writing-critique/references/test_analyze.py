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
