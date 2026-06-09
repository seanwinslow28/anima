"""Tier 1 — calibrate the Gate-2 golden-agreement judge against Sean-labeled truth.

Gate 2 ([`diff_eval.py`]) asks the cheap proxy question — does Em's proposed
corrective clause express the SAME fix as Sean's ratified golden? — judge-scored,
runnable any time for pennies, so Em's constructive quality can be tracked between
the costed ~$7.80 Gate-3 fix-rate runs. But per the eval handbook a judge's numbers
are NOT trustworthy until calibrated against a human-labeled sample. This module is
that calibration harness.

The dangerous error is the judge OVER-CALLING "match" (says Em's clause matches the
golden when Sean says it doesn't) — that would inflate Em's tracked fix-rate in her
own favor. So the headline is precision/recall on the MATCH class + the false-positive
rate FPR = FP/(FP+TN), NOT raw agreement (which misleads under imbalance, handbook
§3.2). MATCH is the positive class — distinct from the verdict suite's scoring.py,
where the positive class is the DEFECT and false_pass_rate = FN/(TP+FN).

Method (handbook §3.1 Critique Shadowing, §3.5 sampling consistency): the judge votes
N=5 per pair (majority); Sean's binary labels + critiques are the ground truth (his
critiques, not the judge, are the real artifact). Bar: κ ≥ 0.6 AND FPR ≤ 0.10.

No judge is invoked at import or in CI — scorers take an injected `judge` callable;
the --check-only path uses a stub. The costed run is `--capture` (live Em) then
`--score` (Opus judge), both fleet-ops-gated.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from evals.vision_critic.diff_eval import opus_judge, score_golden_agreement
from evals.vision_critic.scoring import stderr

HERE = Path(__file__).parent


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #
@dataclass
class Pair:
    """One (candidate clause, reference golden) pair to be judged + Sean-labeled.

    kind: "real" (Em's captured clause vs its own golden), "cross_negative"
    (golden paired with a DIFFERENT defect class's clause — an easy non-match),
    or "hard_negative" (same defect class, genuinely different fix — stresses the
    dangerous over-call). candidate=None means Em proposed no diff (match N/A).
    """
    pair_id: str
    defect_label: str
    kind: str
    candidate: str | None
    golden: str


@dataclass
class Scored:
    pair_id: str
    defect_label: str
    kind: str
    em_proposed: bool
    judge_match: bool | None     # N=5 majority; None iff Em proposed no diff
    sean_match: bool | None      # ground truth; None = N/A (no diff) or unlabeled
    votes: list[bool] = field(default_factory=list)
    why: str = ""


# --------------------------------------------------------------------------- #
# Stub judge (credential-free plumbing; mirrors diff_eval._stub_judge)
# --------------------------------------------------------------------------- #
def _stub_judge(prompt: str) -> str:
    """Deterministic credential-free judge for --check-only. Always says match;
    exercises the pipeline, NEVER a scored claim."""
    return json.dumps({"match": True, "why": "STUB (no scored claim)"})


# --------------------------------------------------------------------------- #
# N=5 majority vote (sampling consistency, handbook §3.5)
# --------------------------------------------------------------------------- #
def judge_pair_majority(*, candidate: str | None, golden: str, defect_label: str,
                        judge, n: int = 5) -> dict:
    """Run the Gate-2 judge N times on one pair, majority-vote the match verdict.

    A pair where Em proposed no diff short-circuits to majority_match=None and the
    judge is NEVER called — 'proposed nothing' is excluded from the matrix, never a 0.
    """
    if not candidate or not str(candidate).strip():
        return {"em_proposed": False, "majority_match": None, "votes": [],
                "spread": (0, 0), "why": "no diff proposed"}
    votes: list[bool] = []
    whys: list[str] = []
    for _ in range(n):
        r = score_golden_agreement(em_value=candidate, golden_diff=golden,
                                   defect_label=defect_label, judge=judge)
        votes.append(bool(r["match"]))
        whys.append(str(r.get("why", "")))
    n_match = sum(1 for v in votes if v)
    return {"em_proposed": True, "majority_match": (n_match * 2) > len(votes),
            "votes": votes, "spread": (n_match, len(votes)),
            "why": whys[0] if whys else ""}


# --------------------------------------------------------------------------- #
# Match-class confusion matrix + metrics (positive class = MATCH)
# --------------------------------------------------------------------------- #
def match_confusion(scored: list[Scored]) -> dict[str, int]:
    """2x2 over pairs with BOTH a judge verdict and a Sean label. positive = match.
    FP (judge match ∧ Sean no-match) is the dangerous over-call."""
    tp = fp = fn = tn = 0
    for s in scored:
        if s.judge_match is None or s.sean_match is None:
            continue
        if s.judge_match and s.sean_match:
            tp += 1
        elif s.judge_match and not s.sean_match:
            fp += 1
        elif (not s.judge_match) and s.sean_match:
            fn += 1
        else:
            tn += 1
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def match_metrics(cm: dict[str, int]) -> dict[str, float]:
    tp, fp, fn, tn = cm["tp"], cm["fp"], cm["fn"], cm["tn"]
    n = tp + fp + fn + tn
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    fpr = fp / (fp + tn) if (fp + tn) else 0.0   # the dangerous over-call rate
    raw_agreement = (tp + tn) / n if n else 0.0  # imbalance-sensitive; never headline
    return {"precision": precision, "recall": recall, "fpr": fpr,
            "raw_agreement": raw_agreement, "n": n}


def cohens_kappa(cm: dict[str, int]) -> float:
    """Cohen's κ for the 2x2 judge-vs-Sean agreement (no helper existed in scoring.py).
    κ ≥ 0.6 is the substantial-agreement bar. Degenerate (no variance) → 1.0 when
    fully agreed, else 0.0; empty → 0.0."""
    tp, fp, fn, tn = cm["tp"], cm["fp"], cm["fn"], cm["tn"]
    n = tp + fp + fn + tn
    if n == 0:
        return 0.0
    po = (tp + tn) / n
    p_judge_yes = (tp + fp) / n
    p_sean_yes = (tp + fn) / n
    p_judge_no = (fn + tn) / n
    p_sean_no = (fp + tn) / n
    pe = p_judge_yes * p_sean_yes + p_judge_no * p_sean_no
    if (1 - pe) == 0:
        return 1.0 if po >= 1.0 else 0.0
    return (po - pe) / (1 - pe)


# --------------------------------------------------------------------------- #
# Aggregation
# --------------------------------------------------------------------------- #
def _block(items: list[Scored]) -> dict:
    cm = match_confusion(items)
    m = match_metrics(cm)
    scored_n = cm["tp"] + cm["fp"] + cm["fn"] + cm["tn"]
    return {
        "cm": cm,
        **m,
        "kappa": cohens_kappa(cm),
        "n_scored": scored_n,
        "n_no_proposal": sum(1 for s in items if not s.em_proposed),
        "precision_stderr": stderr(p=m["precision"], n=cm["tp"] + cm["fp"]),
        "recall_stderr": stderr(p=m["recall"], n=cm["tp"] + cm["fn"]),
        "fpr_stderr": stderr(p=m["fpr"], n=cm["fp"] + cm["tn"]),
    }


def aggregate(scored: list[Scored]) -> dict:
    """Overall + per-defect-class segmentation (the verdict suite's shape). Per-class
    κ is noisy at small N — the headline is overall; by_label is diagnostic."""
    labels = sorted({s.defect_label for s in scored})
    return {
        "overall": _block(scored),
        "by_label": {lbl: _block([s for s in scored if s.defect_label == lbl])
                     for lbl in labels},
    }


def run_calibration(pairs: list[Pair], labels: dict, *, judge, n: int = 5
                    ) -> tuple[list[Scored], dict]:
    """Judge every pair N times, join Sean's labels, score. labels: pair_id ->
    {sean_match: bool|None, sean_why: str}. An unlabeled pair → sean_match None
    (excluded from the matrix, surfaced in the trace)."""
    scored: list[Scored] = []
    for p in pairs:
        res = judge_pair_majority(candidate=p.candidate, golden=p.golden,
                                  defect_label=p.defect_label, judge=judge, n=n)
        lab = labels.get(p.pair_id, {})
        scored.append(Scored(
            pair_id=p.pair_id, defect_label=p.defect_label, kind=p.kind,
            em_proposed=res["em_proposed"], judge_match=res["majority_match"],
            sean_match=lab.get("sean_match"), votes=res["votes"], why=res["why"]))
    return scored, aggregate(scored)


# --------------------------------------------------------------------------- #
# Live Em-diff capture (capture_fn injected for tests; live default at runtime)
# --------------------------------------------------------------------------- #
_CAPTURE_TIMEOUT_S = 600  # per-case worker ceiling (Opus escalation can run minutes)


def _subprocess_capture_value(case_name: str) -> str | None:
    """Capture Em's first proposed-patch value for ONE case in a FRESH interpreter
    via `score.py --only <case> --dump-patches` (live, no --stub). Per-case
    subprocess isolation dodges the exit-144 teardown race (#37) that an in-process
    30-case loop of Em+Opus calls would hit. rc 4 (flagged case captured no diffs)
    is a real outcome → None. A STUB value means the live path silently fell back —
    hard stop, never score it."""
    import subprocess
    proc = subprocess.run(
        [sys.executable, "-m", "evals.vision_critic.score", "--only", case_name,
         "--dump-patches"],
        capture_output=True, text=True, timeout=_CAPTURE_TIMEOUT_S,
        cwd=str(HERE.parents[1]))
    if proc.returncode == 4:          # PREFLIGHT FAIL: flagged case, no diffs
        return None
    if proc.returncode != 0:
        raise RuntimeError(f"capture worker for {case_name} failed rc="
                           f"{proc.returncode}: {proc.stderr[-400:]}")
    out = proc.stdout.strip()
    try:
        patches = json.loads(out)
    except json.JSONDecodeError:      # tolerate any leading log noise
        i, j = out.find("["), out.rfind("]")
        patches = json.loads(out[i:j + 1]) if i >= 0 and j > i else []
    if not patches:
        return None
    val = patches[0].get("value")
    if val and "STUB" in str(val):
        raise RuntimeError(f"capture for {case_name} returned STUB text — the live "
                           "path is not real; stop (do not score a stub).")
    return val


def capture_em_diffs(cases: list[dict], *, manifest, criteria, capture_fn=None,
                     on_row=None) -> list[dict]:
    """Run Em LIVE per defect case and assemble {name, defect_label, golden_diff,
    em_value, expected_cites} rows. Per-case failures are contained as honest None
    gaps (with an `error` reason) so one bad case can't abort the run (the Gate-3 v1
    containment lesson). `on_row(row)` fires after each case for incremental
    persistence. Asserts at least one non-empty em_value — an all-empty capture
    means the proxy has nothing to score; stop and surface (the 2026-06-07
    'measured nothing' guard). capture_fn defaults to the real
    patch_efficacy._capture_em_value; injected as a fake in tests."""
    if capture_fn is None:
        from evals.vision_critic.patch_efficacy import _capture_em_value
        capture_fn = _capture_em_value
    rows = []
    for case in cases:
        row = {"name": case["name"], "defect_label": case["defect_label"],
               "golden_diff": case.get("golden_diff", ""),
               "expected_cites": case.get("expected_cites", []),
               "em_value": None, "error": None}
        try:
            row["em_value"] = capture_fn(case, manifest=manifest, criteria=criteria)
        except Exception as exc:  # contained gap, never a run-aborting crash
            row["error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
        if on_row is not None:
            on_row(row)
    if not any(r["em_value"] and str(r["em_value"]).strip() for r in rows):
        raise RuntimeError(
            "capture produced 0 non-empty Em diffs — the proxy has nothing to "
            "score; stop and surface (do not spend to measure nothing).")
    return rows


# --------------------------------------------------------------------------- #
# IO helpers
# --------------------------------------------------------------------------- #
def load_jsonl(path: str | Path) -> list[dict]:
    text = Path(path).read_text(encoding="utf-8")
    return [json.loads(ln) for ln in text.splitlines() if ln.strip()]


def write_jsonl(path: str | Path, rows: list[dict]) -> None:
    Path(path).write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def pairs_from_rows(rows: list[dict]) -> list[Pair]:
    return [Pair(pair_id=r["pair_id"], defect_label=r["defect_label"],
                 kind=r.get("kind", "real"), candidate=r.get("candidate"),
                 golden=r["golden"]) for r in rows]


def labels_from_rows(rows: list[dict]) -> dict:
    return {r["pair_id"]: {"sean_match": r.get("sean_match"),
                           "sean_why": r.get("sean_why", "")} for r in rows}


def load_defect_cases() -> list[dict]:
    """The 30 identity_style defect cases (each carries a ratified golden_diff)."""
    cases = yaml.safe_load((HERE / "cases.yaml").read_text(encoding="utf-8"))["cases"]
    return [c for c in cases if c.get("case_class") == "identity_style"]


def _eval_manifest_and_criteria():
    root = HERE.parents[1]
    full = yaml.safe_load((root / "manifest.yaml").read_text(encoding="utf-8"))
    manifest = {"critics": full.get("critics", {}),
                "criteria_sources": full.get("criteria_sources", {}),
                "characters_root": str(root / "characters")}
    from pipeline.criteria import load_all_criteria
    return manifest, load_all_criteria(manifest)


# --------------------------------------------------------------------------- #
# --check-only synthetic pipeline (credential-free; no scored claim)
# --------------------------------------------------------------------------- #
def _synthetic_check() -> dict:
    """Run the whole pipeline on a stub judge + a tiny synthetic label set. Proves
    the plumbing; makes NO scored claim (the stub always says match)."""
    pairs = [
        Pair("syn-real-match", "palette", "real", "recolor it", "use the full palette"),
        Pair("syn-cross-neg", "palette", "cross_negative", "add the sixth finger",
             "use the full palette"),
        Pair("syn-hard-neg", "view-correctness", "hard_negative", "redraw as profile",
             "redraw as three-quarter"),
        Pair("syn-noprop", "anatomy-count", "real", None, "five fingers per hand"),
    ]
    labels = {
        "syn-real-match": {"sean_match": True, "sean_why": "synthetic"},
        "syn-cross-neg": {"sean_match": False, "sean_why": "synthetic"},
        "syn-hard-neg": {"sean_match": False, "sean_why": "synthetic"},
    }
    _, agg = run_calibration(pairs, labels, judge=_stub_judge, n=5)
    return agg


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _cmd_check_only() -> None:
    agg = _synthetic_check()
    print(json.dumps(agg, indent=2))
    print("\nPREFLIGHT OK: ran the calibration pipeline end-to-end (STUB judge, "
          "synthetic labels — NO scored claim).", file=sys.stderr)


def _cmd_capture(out: str) -> None:
    cases = load_defect_cases()
    out_path = Path(out)
    out_path.write_text("", encoding="utf-8")  # truncate; we append per case

    def _append(row: dict) -> None:
        with out_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row) + "\n")
        tag = "OK" if (row["em_value"] and str(row["em_value"]).strip()) else \
              ("ERROR" if row["error"] else "no-proposal")
        print(f"  [{tag}] {row['name']}", file=sys.stderr, flush=True)

    # capture_fn ignores manifest/criteria — each worker reads the live manifest in
    # its own fresh interpreter (production attach_criteria_text honored there).
    def _cap(case, *, manifest, criteria):
        return _subprocess_capture_value(case["name"])

    rows = capture_em_diffs(cases, manifest=None, criteria=None,
                            capture_fn=_cap, on_row=_append)
    n_nonempty = sum(1 for r in rows if r["em_value"] and str(r["em_value"]).strip())
    n_err = sum(1 for r in rows if r["error"])
    print(f"CAPTURE OK: {n_nonempty}/{len(rows)} non-empty Em diffs "
          f"({n_err} errored gaps) → {out}", file=sys.stderr)


def _cmd_score(set_path: str, labels_path: str, *, judge_name: str, n: int,
               out: str | None) -> None:
    pairs = pairs_from_rows(load_jsonl(set_path))
    labels = labels_from_rows(load_jsonl(labels_path))
    judge = _stub_judge if judge_name == "stub" else opus_judge
    scored, agg = run_calibration(pairs, labels, judge=judge, n=n)
    payload = {
        "judge": judge_name, "n": n,
        "bar": {"kappa_min": 0.6, "fpr_max": 0.10},
        "pass": (agg["overall"]["kappa"] >= 0.6 and agg["overall"]["fpr"] <= 0.10),
        "aggregate": agg,
        "pairs": [{"pair_id": s.pair_id, "defect_label": s.defect_label,
                   "kind": s.kind, "em_proposed": s.em_proposed,
                   "judge_match": s.judge_match, "sean_match": s.sean_match,
                   "spread": [sum(1 for v in s.votes if v), len(s.votes)],
                   "why": s.why} for s in scored],
    }
    out_str = json.dumps(payload, indent=2)
    if out:
        Path(out).write_text(out_str + "\n", encoding="utf-8")
    print(out_str)
    o = agg["overall"]
    print(f"\nκ={o['kappa']:.3f} (bar ≥0.60)  FPR={o['fpr']:.3f} (bar ≤0.10)  "
          f"precision={o['precision']:.3f}  recall={o['recall']:.3f}  "
          f"→ {'PASS' if payload['pass'] else 'BELOW BAR'}", file=sys.stderr)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="calibrate-diff-judge")
    ap.add_argument("--check-only", action="store_true",
                    help="$0 credential-free plumbing check (stub judge, synthetic labels). EXIT.")
    ap.add_argument("--capture", metavar="OUT.jsonl",
                    help="Run Em LIVE on the 30 defect cases → captured-diffs JSONL "
                         "(asserts non-empty). Costed (~$1.50). EXIT.")
    ap.add_argument("--score", action="store_true",
                    help="Score a calibration set against Sean's labels (judge N=5).")
    ap.add_argument("--set", dest="set_path", help="Calibration-set JSONL (with --score).")
    ap.add_argument("--labels", dest="labels_path", help="Sean-labels JSONL (with --score).")
    ap.add_argument("--judge", choices=["opus", "stub"], default="opus")
    ap.add_argument("--n", type=int, default=5, help="Votes per pair (majority).")
    ap.add_argument("--out", help="Write the scored payload JSON here.")
    args = ap.parse_args(argv)

    if args.check_only:
        _cmd_check_only()
    elif args.capture:
        _cmd_capture(args.capture)
    elif args.score:
        if not (args.set_path and args.labels_path):
            ap.error("--score requires --set and --labels")
        _cmd_score(args.set_path, args.labels_path, judge_name=args.judge,
                   n=args.n, out=args.out)
    else:
        ap.error("one of --check-only / --capture / --score is required")


if __name__ == "__main__":
    main()
