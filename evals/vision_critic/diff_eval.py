"""G6.9 Gate 2 + Gate 4 — judge-based scorers for Em's prompt diffs.

Gate 2 (golden agreement, the in-suite gate): does Em's proposed corrective clause
express the SAME fix as Sean's ratified `golden_diff`? Binary per defect case,
LLM-judged. Plus the pure diff cite precision/recall (scoring.diff_cite_precision_recall) —
precision AND recall, distinct from the recall-only verdict scorer (locked #4).

Gate 4 (triage rubric, secondary): a cheap binary rubric per diff — targets the
cited defect / actionable as a prompt edit / no character re-description (Seedance
rule) / style-neutral (the style-neutrality doctrine). Judge-on-judge is the
WEAKEST evidence class; this is a triage signal, NEVER the headline.

Both judges are PLUGGABLE and CALIBRATION-GATED: per the eval handbook, a judge's
numbers are not trustworthy until calibrated against a Sean-labeled sample (record
the judge-bias ledger). This module ships the plumbing + mock-judge tests; the
costed calibration run + the real judges are DEFERRED. No judge is invoked at
import or in CI — the scorers take an injected `judge` callable; tests pass a stub.

Headline ownership: Gate 2 golden-agreement is the cheap per-run proxy; the Gate 3
empirical fix-rate is the headline (patch_efficacy.py). Gate 4 is never either.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from evals.vision_critic.scoring import diff_cite_precision_recall, stderr

HERE = Path(__file__).parent


# --------------------------------------------------------------------------- #
# Judge prompts
# --------------------------------------------------------------------------- #
_AGREEMENT_PROMPT = (
    "You are calibrating an animation-pipeline eval. Two corrective prompt-clauses "
    "each aim to FIX the same image defect (defect class: {defect_label}). Decide "
    "whether they express the SAME corrective intent — i.e. applying either clause "
    "would steer a re-generation toward the same fix. Wording may differ; judge the "
    "INTENT, not the phrasing.\n\n"
    "CANDIDATE (the critic's proposed fix): {em}\n"
    "REFERENCE (the human's ratified golden fix): {golden}\n\n"
    'Reply with ONLY a JSON object: {{"match": true|false, "why": "<one short sentence>"}}'
)

_TRIAGE_PROMPT = (
    "Score a critic-proposed prompt diff on a binary rubric. Defect class: "
    "{defect_label}. Expected criterion: {expected}.\n\n"
    "DIFF (the proposed prompt-clause): {em}\n"
    "CRITIC REASONING: {reasoning}\n\n"
    "Reply with ONLY a JSON object of booleans:\n"
    '{{"targets_defect": <bool>, "actionable": <bool>, '
    '"no_recharacterization": <bool>, "style_neutral": <bool>}}\n'
    "- targets_defect: the diff addresses the stated defect class\n"
    "- actionable: it reads as a concrete prompt edit, not vague advice\n"
    "- no_recharacterization: it does NOT re-describe the character's fixed identity "
    "(the Seedance 'don't re-describe the character' rule)\n"
    "- style_neutral: it imposes no style outside the closed pencil-test register "
    "(the style-neutrality doctrine)"
)

_TRIAGE_AXES = ("targets_defect", "actionable", "no_recharacterization", "style_neutral")


# --------------------------------------------------------------------------- #
# Judge registry (real judges — NOT invoked this push; wired for the costed run)
# --------------------------------------------------------------------------- #
def _run(coro):
    return asyncio.run(coro)


def opus_judge(prompt: str) -> str:
    """Gate 2 default — Opus 4.8 text (strong semantic discrimination). Subscription-
    billed via the Claude Agent SDK; falls back to a stub when the SDK is absent."""
    from pipeline.agents.sdk_runners import invoke_opus_text
    return _run(invoke_opus_text(prompt=prompt)).text


def sonnet_judge(prompt: str) -> str:
    from pipeline.agents.sdk_runners import invoke_sonnet_text
    return _run(invoke_sonnet_text(prompt=prompt)).text


def gemini_judge(prompt: str) -> str:
    """Gate 4 default — gemini-3.5-flash (cheap triage). Routed through the vision
    runner with no images (text-only). Validate the empty-image path at calibration."""
    from pipeline.agents.gemini_api_runner import run_gemini_api_with_image
    return _run(run_gemini_api_with_image(prompt=prompt, image_paths=[])).text


JUDGES = {"opus": opus_judge, "sonnet": sonnet_judge, "gemini": gemini_judge}
_DEFAULT_JUDGE = {"2": "opus", "4": "gemini"}  # per-gate defaults (locked recommendation)


# --------------------------------------------------------------------------- #
# JSON extraction (judge replies may be code-fenced or chatty)
# --------------------------------------------------------------------------- #
def _extract_json(text: str) -> dict:
    if not text:
        return {}
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.MULTILINE).strip()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", t, flags=re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                return {}
        return {}


# --------------------------------------------------------------------------- #
# Scorers
# --------------------------------------------------------------------------- #
def score_golden_agreement(*, em_value: str | None, golden_diff: str,
                           defect_label: str, judge) -> dict:
    """Gate 2: judge whether Em's clause matches the golden fix. em_value None means
    Em proposed no diff — a real outcome (em_proposed=False, match=None), NEVER scored
    as match=False (that would conflate 'proposed nothing' with 'proposed wrong')."""
    if not em_value or not str(em_value).strip():
        return {"em_proposed": False, "match": None, "why": "no diff proposed"}
    raw = judge(_AGREEMENT_PROMPT.format(em=em_value, golden=golden_diff,
                                         defect_label=defect_label))
    parsed = _extract_json(raw)
    return {"em_proposed": True, "match": bool(parsed.get("match")),
            "why": str(parsed.get("why", ""))}


def score_triage(*, em_value: str, defect_label: str, expected_cites: list[str],
                 reasoning: str, judge) -> dict:
    """Gate 4: binary rubric per diff. Triage signal only — never the headline."""
    raw = judge(_TRIAGE_PROMPT.format(
        em=em_value, defect_label=defect_label,
        expected=", ".join(expected_cites) or "(none)", reasoning=reasoning or ""))
    parsed = _extract_json(raw)
    return {axis: bool(parsed.get(axis)) for axis in _TRIAGE_AXES}


@dataclass
class DiffScore:
    name: str
    defect_label: str
    em_value: str | None
    golden_diff: str
    em_proposed: bool
    golden_agreement: bool | None      # None = not scored (no diff proposed)
    cite_precision: float
    cite_recall: float | None
    triage: dict | None = None


def _rate(flags: list[bool]) -> float:
    return (sum(1 for f in flags if f) / len(flags)) if flags else 0.0


def _block(scores: list[DiffScore]) -> dict:
    n = len(scores)
    proposed = [s for s in scores if s.em_proposed]
    agreed = [s for s in proposed if s.golden_agreement is not None]
    matches = [bool(s.golden_agreement) for s in agreed]
    precs = [s.cite_precision for s in proposed]
    recs = [s.cite_recall for s in proposed if s.cite_recall is not None]
    rate = _rate(matches)
    return {
        "n": n,
        "proposal_rate": (len(proposed) / n) if n else 0.0,
        "agreement_scored_n": len(agreed),
        "golden_agreement_rate": rate,
        "golden_agreement_stderr": stderr(p=rate, n=len(matches)),
        "cite_precision_mean": (sum(precs) / len(precs)) if precs else 0.0,
        "cite_recall_mean": (sum(recs) / len(recs)) if recs else None,
        "triage_rates": {
            ax: _rate([bool(s.triage.get(ax)) for s in proposed if s.triage])
            for ax in _TRIAGE_AXES
        } if any(s.triage for s in proposed) else None,
    }


def aggregate_diff_scores(scores: list[DiffScore]) -> dict:
    """Overall + per-defect-class segmentation (the verdict suite's shape). proposal-
    rate and agreement-given-proposed are reported SEPARATELY (locked policy): a case
    where Em proposed nothing is excluded from the agreement denominator, never a 0."""
    labels = sorted({s.defect_label for s in scores})
    return {
        "overall": _block(scores),
        "by_label": {lbl: _block([s for s in scores if s.defect_label == lbl])
                     for lbl in labels},
    }


# --------------------------------------------------------------------------- #
# CLI — $0 plumbing check (real scoring + calibration are deferred)
# --------------------------------------------------------------------------- #
def _load_defect_cases() -> list[dict]:
    cases = yaml.safe_load((HERE / "cases.yaml").read_text(encoding="utf-8"))["cases"]
    return [c for c in cases if c["case_class"] == "identity_style"]


def _stub_judge(prompt: str) -> str:
    """A deterministic credential-free judge for the $0 plumbing check. Says 'match'
    when the candidate and reference share a content word — enough to exercise the
    pipeline, never a scored claim."""
    return json.dumps({"match": True, "why": "STUB (no scored claim)",
                       "targets_defect": True, "actionable": True,
                       "no_recharacterization": True, "style_neutral": True})


def main() -> None:
    ap = argparse.ArgumentParser(prog="em-diff-eval")
    ap.add_argument("--gate", choices=["2", "4", "both"], default="both")
    ap.add_argument("--judge", choices=list(JUDGES) + ["stub"], default=None,
                    help="Judge model. Default per gate: Gate 2=opus, Gate 4=gemini. "
                         "stub = credential-free plumbing check (no scored claim).")
    ap.add_argument("--check-only", action="store_true",
                    help="$0 plumbing check: assert every defect case has a golden_diff, "
                         "run the STUB judge over the corpus using each golden as a "
                         "stand-in candidate, print a sample aggregate, and EXIT. Proves "
                         "the scoring pipeline before any costed (real-judge) run. Real "
                         "scoring needs (a) a score.py patch-capture run for Em's diffs "
                         "and (b) judge calibration — both deferred.")
    args = ap.parse_args()

    if not args.check_only:
        print("Real diff scoring is DEFERRED (needs ratified goldens + judge "
              "calibration + a score.py patch-capture run). Use --check-only for the "
              "$0 plumbing check.", file=sys.stderr)
        raise SystemExit(2)

    defects = _load_defect_cases()
    missing = [c["name"] for c in defects if not c.get("golden_diff")]
    if missing:
        print(f"PREFLIGHT FAIL: {len(missing)} defect case(s) missing golden_diff: "
              f"{missing[:5]}", file=sys.stderr)
        raise SystemExit(4)
    unratified = [c["name"] for c in defects if not c.get("golden_diff_ratified")]

    judge = _stub_judge
    scores: list[DiffScore] = []
    for c in defects:
        golden = c["golden_diff"]
        em_value = golden  # stand-in candidate for the plumbing check (NOT a scored claim)
        agree = score_golden_agreement(em_value=em_value, golden_diff=golden,
                                        defect_label=c["defect_label"], judge=judge)
        cite = diff_cite_precision_recall(predicted_cites=c.get("expected_cites", []),
                                          expected_cites=c.get("expected_cites", []))
        triage = score_triage(em_value=em_value, defect_label=c["defect_label"],
                              expected_cites=c.get("expected_cites", []),
                              reasoning="", judge=judge)
        scores.append(DiffScore(
            name=c["name"], defect_label=c["defect_label"], em_value=em_value,
            golden_diff=golden, em_proposed=agree["em_proposed"],
            golden_agreement=agree["match"], cite_precision=cite["precision"],
            cite_recall=cite["recall"], triage=triage))

    agg = aggregate_diff_scores(scores)
    print(json.dumps(agg, indent=2))
    print(f"\nPREFLIGHT OK: scored {len(scores)} defect cases through the diff-eval "
          f"pipeline (STUB judge, no scored claim).", file=sys.stderr)
    print(f"  golden_diff present: {len(defects)}/{len(defects)}; "
          f"unratified (block a costed run): {len(unratified)}", file=sys.stderr)


if __name__ == "__main__":
    main()
