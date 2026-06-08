"""G6.9 Gate 3 — the empirical patch-efficacy loop (the fix-rate anchor).

The closest usefulness has to ground truth (Engine Truth): take a corrective clause,
apply it, RE-GENERATE the frame, RE-CRITIQUE, and ask — did the defect clear AND did
identity/style hold? Per re-roll it is binary; across N re-rolls it is a clear-rate
BAND (generation is stochastic — a diff that "works" once may have worked by accident).

Two arms per case:
  - golden  : Sean's ratified golden_diff — the POSITIVE CONTROL. If the golden clause
              can't clear the defect at a high rate, the loop (or the model) is broken,
              not Em. An all-zero em-arm is uninterpretable without this.
  - em      : Em's proposed_patches[].value — the thing under test. May be empty
              (Em proposed no fix) — a real, measured outcome, never a failed fix.

Apply-mechanism: prompt_apply.build_corrected_prompt splices the clause onto the
defect case's CLEAN PAIR prompt (see that module). view-correctness is label-side and
takes a NO-REGENERATION branch (correct the declared view, re-critique the same fixture).

STATUS: this push builds + stub-tests the machinery. The first COSTED run is DEFERRED
behind the §0 pre-flight and ratified goldens (preflight refuses a live run while any
sampled golden is unratified, or ANTHROPIC_API_KEY is set, or GEMINI_API_KEY is absent).

COSTED-RUN HARDENING NOTE: the in-process re-critique below spawns Em's async children
(Opus escalation on identity_critical). Before the first costed baseline, wrap each case
in score.py's subprocess-per-case isolation to dodge the exit-144 interpreter-teardown
race (documented in score.py). The stub path has no async children, so it is safe here.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from evals.vision_critic.prompt_apply import (
    parse_corpus, build_corrected_prompt, NoRegenForView,
)
from evals.vision_critic.scoring import normalize_cite, stderr

HERE = Path(__file__).parent
_CORPUS_MD = HERE.parents[1] / "prompts/eval-corpus/sean-anchor-fixture-corpus.md"

# Unit-cost assumptions (conservative ceilings — confirm at calibration). NB2 Flash
# image ~$0.02; gemini-3.5-flash T2 call ~$0.05; Opus escalation subscription-absorbed.
_C_NB2 = 0.02
_C_EM = 0.05

# The NULL/PLACEBO arm's clause (Sean's locked attribution decision, 2026-06-08): a
# fixed, defect-orthogonal phrase spliced through the SAME clean-pair mechanism as the
# real arms. It measures the FLOOR — how often the clean-pair base regenerates a clean,
# identity-holding frame REGARDLESS of any corrective content. Normalized lift
# (em − null)/(golden − null) cancels that floor; per class, null ≈ golden means the
# instrument has no discriminative power there (a measured finding, not a guess). The
# phrase touches none of the six axes (proportion/view/anatomy/palette/construction/
# shading) so it cannot itself fix or break a defect.
_NULL_CLAUSE = "with a calm, evenly-lit, neutral background"


class PreflightError(Exception):
    """A §0 pre-flight assertion failed — raised before any spend."""


# --------------------------------------------------------------------------- #
# Result records
# --------------------------------------------------------------------------- #
@dataclass
class RerollOutcome:
    idx: int
    regenerated: bool
    cache_hit: bool
    stub_fallback: bool
    verdict: str
    cites: list[str]
    defect_cleared: bool   # the ORIGINAL defect's cite is no longer flagged
    identity_held: bool    # re-critique is a clean pass with no NEW drift cite
    similarity: float | None = None  # record-only view-fair identity diagnostic

    @property
    def fixed(self) -> bool:
        return self.defect_cleared and self.identity_held


@dataclass
class ArmResult:
    arm: str
    clause: str | None
    rerolls: list[RerollOutcome]
    skipped_no_proposal: bool = False

    @property
    def clear_rate(self) -> float:
        if not self.rerolls:
            return 0.0
        return sum(1 for r in self.rerolls if r.fixed) / len(self.rerolls)

    @property
    def band(self) -> dict:
        vals = [1.0 if r.fixed else 0.0 for r in self.rerolls]
        n = len(vals)
        mean = (sum(vals) / n) if n else 0.0
        return {"min": min(vals) if vals else 0.0, "max": max(vals) if vals else 0.0,
                "mean": mean, "stderr": stderr(p=mean, n=n)}


@dataclass
class CaseEfficacy:
    name: str
    corpus_id: str
    defect_label: str
    pair: str | None
    em_proposed: bool
    arms: dict[str, ArmResult] = field(default_factory=dict)


# --------------------------------------------------------------------------- #
# Injectable fakes (tests + --stub) — no model, no spend
# --------------------------------------------------------------------------- #
@dataclass
class _RegenResult:
    output_path: Path
    cache_hit: bool
    stub_fallback: bool


class FakeRegen:
    """A stand-in for invoke_image_edit. Records call count; never touches a model."""
    def __init__(self, stub: bool = True, cache_hit: bool = False):
        self.stub = stub
        self.cache_hit = cache_hit
        self.calls = 0

    def __call__(self, *, prompt, case, reroll):
        self.calls += 1
        return _RegenResult(output_path=Path(f"/tmp/fake-{case['name']}-{reroll}.png"),
                            cache_hit=self.cache_hit, stub_fallback=self.stub)


class FakeCritique:
    """A stand-in for Em's re-critique. Returns a fixed (verdict, cites)."""
    def __init__(self, verdict: str = "pass", cites=None, stub_fallback: bool = True):
        self.verdict = verdict
        self.cites = list(cites or [])
        self.stub_fallback = stub_fallback

    def __call__(self, *, image_path, beat, case, manifest, criteria, reroll):
        return self.verdict, list(self.cites), self.stub_fallback


# --------------------------------------------------------------------------- #
# Sampling + base-prompt resolution
# --------------------------------------------------------------------------- #
def select_sample(defects: list[dict], *, sample: int, labels=None) -> list[dict]:
    """Balanced, DETERMINISTIC selection: round-robin across defect labels (sorted),
    first-seen order within a label. No RNG (resume-safe, reproducible)."""
    pool = [c for c in defects if (not labels or c["defect_label"] in labels)]
    by_label: dict[str, list[dict]] = {}
    for c in pool:
        by_label.setdefault(c["defect_label"], []).append(c)
    ordered = sorted(by_label)
    out: list[dict] = []
    guard = 0
    while len(out) < sample and any(by_label.values()) and guard < 100_000:
        lbl = ordered[guard % len(ordered)]
        if by_label[lbl]:
            out.append(by_label[lbl].pop(0))
        guard += 1
    return out[:sample]


def resolve_base(case: dict, corpus: dict[str, str]) -> tuple[str, str]:
    """(kind, base_prompt). kind 'no-regen' for view-correctness (label-side; correct
    the declared view, re-critique the same fixture), else 'regen'. The base is the
    defect case's CLEAN PAIR prompt — every defect case pairs with a clean C01–C16,
    so PA-D6 (absent from the corpus md) and the hand-drawn borderlines resolve too."""
    pair = case.get("pair")
    prompt = corpus.get(pair) or corpus.get(case.get("corpus_id", ""), "")
    if case["defect_label"] == "view-correctness":
        return "no-regen", prompt
    return "regen", prompt


def _cites_hit(cites: list[str], expected: list[str]) -> bool:
    norm_exp = {normalize_cite(c) for c in expected if c and c.strip()}
    norm_act = {normalize_cite(c) for c in cites if c and c.strip()}
    return bool(norm_exp & norm_act)


def _new_drift(cites: list[str], expected: list[str]) -> bool:
    norm_exp = {normalize_cite(c) for c in expected if c and c.strip()}
    norm_act = {normalize_cite(c) for c in cites if c and c.strip()}
    return bool(norm_act - norm_exp)


_UNSET = object()


def _one_reroll(idx, *, kind, base, clause, case, expected,
                regenerate_fn, recritique_fn, manifest, criteria) -> RerollOutcome:
    label = case["defect_label"]
    if kind == "no-regen":
        # View: re-critique the ORIGINAL fixture under the corrected declared view.
        corrected_beat = _view_corrected_beat(case, clause)
        verdict, cites, stub_fb = recritique_fn(
            image_path=HERE / "fixtures" / case["input"], beat=corrected_beat,
            case=case, manifest=manifest, criteria=criteria, reroll=idx)
        regenerated, cache_hit = False, False
    else:
        prompt = build_corrected_prompt(base, clause, label=label)
        regen = regenerate_fn(prompt=prompt, case=case, reroll=idx)
        verdict, cites, rc_stub = recritique_fn(
            image_path=regen.output_path, beat=case["beat_description"],
            case=case, manifest=manifest, criteria=criteria, reroll=idx)
        regenerated, cache_hit = True, regen.cache_hit
        stub_fb = regen.stub_fallback or rc_stub
    return RerollOutcome(
        idx=idx, regenerated=regenerated, cache_hit=cache_hit, stub_fallback=stub_fb,
        verdict=verdict, cites=list(cites),
        defect_cleared=not _cites_hit(cites, expected),
        identity_held=(verdict == "pass") and not _new_drift(cites, expected))


def _view_corrected_beat(case: dict, clause: str) -> str:
    """Re-critique a view defect under its CORRECTED declared view. The clause is the
    declared-view correction; we prefix it so the beat declares what is actually drawn."""
    return f"Declared view (corrected): {clause}. {case['beat_description']}"


def run_case(case: dict, *, arms, rerolls: int, corpus: dict, manifest, criteria,
             regenerate_fn=None, recritique_fn=None, em_value=_UNSET) -> CaseEfficacy:
    """Run the dual-arm efficacy loop for one case. regenerate_fn/recritique_fn are
    injectable (tests + --stub pass fakes); the real ones spend (deferred)."""
    if regenerate_fn is None or recritique_fn is None:
        raise ValueError("run_case needs regenerate_fn + recritique_fn "
                         "(real ones are wired in main(); tests inject fakes)")
    kind, base = resolve_base(case, corpus)
    expected = case.get("expected_cites", [])
    em_clause = None if em_value is _UNSET else em_value
    out: dict[str, ArmResult] = {}
    for arm in arms:
        if arm == "golden":
            clause = case.get("golden_diff")
        elif arm == "null":
            clause = _NULL_CLAUSE       # the placebo floor (Sean's attribution lock)
        else:  # em
            clause = em_clause
        if arm == "em" and not (clause and str(clause).strip()):
            out["em"] = ArmResult(arm="em", clause=None, rerolls=[], skipped_no_proposal=True)
            continue
        rolls = [_one_reroll(i, kind=kind, base=base, clause=clause, case=case,
                             expected=expected, regenerate_fn=regenerate_fn,
                             recritique_fn=recritique_fn, manifest=manifest,
                             criteria=criteria)
                 for i in range(rerolls)]
        out[arm] = ArmResult(arm=arm, clause=clause, rerolls=rolls)
    return CaseEfficacy(name=case["name"], corpus_id=case.get("corpus_id", "?"),
                        defect_label=case["defect_label"], pair=case.get("pair"),
                        em_proposed=bool(em_clause and str(em_clause).strip()), arms=out)


# --------------------------------------------------------------------------- #
# §0 pre-flight + cost estimate
# --------------------------------------------------------------------------- #
def preflight(sample: list[dict], *, corpus: dict, live: bool, manifest=None) -> None:
    """$0 assertions before any spend. Raises PreflightError on the first failure.
    A LIVE run additionally refuses unratified goldens, a present ANTHROPIC_API_KEY,
    and an absent GEMINI_API_KEY (which would silently fabricate placeholder frames)."""
    if live and os.environ.get("ANTHROPIC_API_KEY"):
        raise PreflightError(
            "ANTHROPIC_API_KEY is set — Em's Opus re-critique escalation would bill "
            "the Anthropic API, not the subscription. `unset ANTHROPIC_API_KEY` first.")
    if not sample:
        raise PreflightError("empty sample")
    for c in sample:
        if c.get("case_class") != "identity_style":
            raise PreflightError(f"{c.get('name')}: not an identity_style defect case")
        if not c.get("golden_diff"):
            raise PreflightError(f"{c.get('name')}: missing golden_diff")
        kind, prompt = resolve_base(c, corpus)
        if not prompt:
            raise PreflightError(f"{c['name']}: no base prompt resolved (pair {c.get('pair')})")
        if kind == "regen":
            try:
                build_corrected_prompt(prompt, c["golden_diff"], label=c["defect_label"])
            except (NoRegenForView, ValueError) as e:
                raise PreflightError(f"{c['name']}: dry splice failed: {e}")
        if live and not c.get("golden_diff_ratified"):
            raise PreflightError(
                f"{c['name']}: golden_diff is NOT ratified — refuse to spend on an "
                "unratified reference. Ratify in cases.yaml first.")
    if live:
        from pipeline.agents.gemini_api_runner import _has_gemini_api_key
        if not _has_gemini_api_key():
            raise PreflightError(
                "GEMINI_API_KEY absent — a live regeneration would emit 1x1 stub "
                "placeholder frames and report fabricated fix-rates.")
        if manifest:
            from pipeline.agents.reference_selection import select_references
            c0 = sample[0]
            refs = select_references(c0.get("character_id", "sean"), c0["checkpoint"],
                                     c0["beat_description"],
                                     characters_root=Path(manifest["characters_root"]))
            missing = [str(p) for p in refs if not Path(p).exists()]
            if not refs or missing:
                raise PreflightError(f"references missing on disk: {missing or 'none resolved'}")


def estimate_cost(*, sample: int, rerolls: int, arms, view_count: int = 0) -> dict:
    """Dollar estimate recorded BEFORE a costed run (fleet-ops). View cases skip the
    NB2 generation (re-critique only). The EM arm adds one Em-capture call per case
    (run Em on the defect fixture to GET the diff), once — not per re-roll."""
    n_arms = len(arms)
    regen_cases = max(0, sample - view_count)
    # NB2: every regen-class case × re-roll × arm. View cases never regenerate.
    nb2_calls = n_arms * regen_cases * rerolls
    # Em re-critiques: every case × re-roll × arm (view re-critiques too). Plus the
    # em arm's one-shot capture of Em's proposed diff per case.
    em_calls = n_arms * sample * rerolls + (sample if "em" in arms else 0)
    dollars = nb2_calls * _C_NB2 + em_calls * _C_EM
    return {
        "dollars": round(dollars, 2),
        "nb2_calls": nb2_calls,
        "em_calls": em_calls,
        "em_capture_calls": sample if "em" in arms else 0,
        "assumptions": {"nb2_per_image": _C_NB2, "em_per_call": _C_EM},
    }


# --------------------------------------------------------------------------- #
# Aggregation + report
# --------------------------------------------------------------------------- #
def aggregate_efficacy(efficacies: list[CaseEfficacy]) -> dict:
    """Per-arm, per-defect-class clear-rate with a band — the verdict suite's shape."""
    def block(effs: list[CaseEfficacy], arm: str) -> dict:
        arms = [e.arms[arm] for e in effs if arm in e.arms and not e.arms[arm].skipped_no_proposal]
        rates = [a.clear_rate for a in arms]
        n = len(rates)
        mean = (sum(rates) / n) if n else 0.0
        return {"n_cases": n, "fix_rate_mean": mean,
                "band": {"min": min(rates) if rates else 0.0,
                         "max": max(rates) if rates else 0.0,
                         "stderr": stderr(p=mean, n=n)}}
    labels = sorted({e.defect_label for e in efficacies})
    arms = sorted({a for e in efficacies for a in e.arms})
    return {
        "proposal_rate": (sum(1 for e in efficacies if e.em_proposed) / len(efficacies))
                         if efficacies else 0.0,
        "by_arm": {arm: {"overall": block(efficacies, arm),
                         "by_label": {lbl: block([e for e in efficacies if e.defect_label == lbl], arm)
                                      for lbl in labels}}
                   for arm in arms},
    }


def normalized_lift(agg: dict) -> dict:
    """Sean's locked attribution (2026-06-08). The clean-pair mechanism has a per-class
    FLOOR — a placebo clause can clear a class whose base isn't really defective. The
    null arm measures that floor; lift = (em − null)/(golden − null) cancels it.

    Needs all three arms (em, golden, null) in the aggregate, else returns {} (N/A).
    Per class + overall: raw em/golden/null rates + lift + a discriminative flag.
      - golden ≈ null (denom ≈ 0) → lift None, discriminative False (NO power here —
        a measured finding: the instrument can't tell em from placebo on this class).
      - else lift: 1.0 = em matches golden's lift over the floor; 0.0 = em no better
        than placebo; <0 = em worse than placebo.
    NB: the em rate is over cases where Em PROPOSED (fix-rate-given-proposed); golden/
    null are over all cases. Read alongside proposal_rate, not in place of it.
    """
    by_arm = agg.get("by_arm", {})
    if not {"em", "golden", "null"} <= set(by_arm):
        return {}
    eps = 1e-9

    def _lift(em_r, gold_r, null_r):
        denom = gold_r - null_r
        if abs(denom) < eps:
            return {"em": em_r, "golden": gold_r, "null": null_r,
                    "lift": None, "discriminative": False}
        return {"em": em_r, "golden": gold_r, "null": null_r,
                "lift": round((em_r - null_r) / denom, 3), "discriminative": True}

    def _rate(arm, lbl=None):
        b = by_arm[arm]["overall"] if lbl is None else by_arm[arm]["by_label"][lbl]
        return b["fix_rate_mean"]

    labels = sorted(by_arm["golden"]["by_label"])
    return {
        "overall": _lift(_rate("em"), _rate("golden"), _rate("null")),
        "by_label": {lbl: _lift(_rate("em", lbl), _rate("golden", lbl), _rate("null", lbl))
                     for lbl in labels},
    }


# --------------------------------------------------------------------------- #
# Real (deferred) regenerate + re-critique — wired, refused live until ratified
# --------------------------------------------------------------------------- #
def _real_regenerate(*, run_dir: Path, manifest: dict):
    from pipeline.agents.nb_pro_runner import invoke_image_edit
    from pipeline.agents.reference_selection import select_references

    def fn(*, prompt, case, reroll):
        refs = select_references(case.get("character_id", "sean"), case["checkpoint"],
                                 case["beat_description"],
                                 characters_root=Path(manifest["characters_root"]))
        out = run_dir / f"{case['name']}-reroll-{reroll}.png"
        # reject_reason varies per re-roll → defeats the content-addressed cache so
        # N re-rolls are genuinely independent samples, not one cached frame.
        resp = invoke_image_edit(prompt=prompt, reference_images=list(refs),
                                 output_path=out, cache_dir=run_dir / ".cache",
                                 reject_reason=f"gate3-reroll-{reroll}", timeout_s=180)
        return _RegenResult(output_path=resp.output_path, cache_hit=resp.cache_hit,
                            stub_fallback=resp.stub_fallback)
    return fn


def _real_recritique(*, manifest: dict, criteria):
    from pipeline.agents import AgentContext
    from pipeline.agents.vision_critic import VisionCriticNode, EmptyCitesInvariant

    def fn(*, image_path, beat, case, manifest=manifest, criteria=criteria, reroll):
        ctx = AgentContext(
            run_dir=Path("/tmp/gate3-recritique"),
            inputs={"image_path": str(image_path), "beat_description": beat,
                    "frame_id": f"{case['name']}-reroll-{reroll}",
                    "impact_tags": case.get("impact_tags", []),
                    "checkpoint": case["checkpoint"],
                    "character_id": case.get("character_id", "sean")},
            manifest=manifest, criteria=criteria, tier="draft",
            cache_dir=Path("/tmp/gate3-recritique/.cache"))
        try:
            res = VisionCriticNode().run(ctx)
            return res.outputs["verdict"], list(res.cites_criteria), False
        except EmptyCitesInvariant as inv:
            # Geometry classes can trip the empty-cites invariant (proportion/view/
            # anatomy). Record as the carried verdict, not an abort (mirrors score.py).
            return inv.verdict, list(inv.cites), False
    return fn


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _load_defects() -> list[dict]:
    cases = yaml.safe_load((HERE / "cases.yaml").read_text(encoding="utf-8"))["cases"]
    return [c for c in cases if c["case_class"] == "identity_style"]


_ARM_SETS = {
    "em": ("em",), "golden": ("golden",), "null": ("null",),
    "both": ("em", "golden"),
    "both+null": ("em", "golden", "null"),   # the first costed baseline (Sean's lock)
    "all": ("em", "golden", "null"),
}


def main() -> None:
    ap = argparse.ArgumentParser(prog="em-patch-efficacy")
    ap.add_argument("--arm", choices=list(_ARM_SETS), default="both+null",
                    help="Arm set. 'both+null' (default) = em + golden control + null "
                         "placebo floor → normalized lift (em−null)/(golden−null).")
    ap.add_argument("--sample", type=int, default=12)
    ap.add_argument("--rerolls", type=int, default=3)
    ap.add_argument("--labels", default=None, help="comma list of defect labels to scope")
    ap.add_argument("--stub", action="store_true",
                    help="Credential-free end-to-end: fake regen + fake re-critique, no "
                         "spend, no scored claim. Proves the harness is wired.")
    ap.add_argument("--check-only", action="store_true",
                    help="$0 §0 pre-flight only (assert wiring), then EXIT before any loop.")
    args = ap.parse_args()

    labels = args.labels.split(",") if args.labels else None
    sample = select_sample(_load_defects(), sample=args.sample, labels=labels)
    arms = _ARM_SETS[args.arm]
    view_count = sum(1 for c in sample if c["defect_label"] == "view-correctness")
    est = estimate_cost(sample=len(sample), rerolls=args.rerolls, arms=arms, view_count=view_count)

    # §0 pre-flight. live = a real costed run (NOT stub). Refuses unratified goldens.
    live = not args.stub
    try:
        preflight(sample, corpus=parse_corpus(_CORPUS_MD), live=live,
                  manifest=_manifest() if live else None)
    except PreflightError as e:
        print(f"PREFLIGHT FAIL: {e}", file=sys.stderr)
        raise SystemExit(4)
    print(f"PREFLIGHT OK: {len(sample)} cases × {args.rerolls} re-rolls × {len(arms)} arm(s); "
          f"estimate ${est['dollars']} (nb2={est['nb2_calls']} em={est['em_calls']}); "
          f"{'STUB (no spend)' if args.stub else 'LIVE'}", file=sys.stderr)

    if args.check_only:
        return

    if args.stub:
        regen = FakeRegen(stub=True)
        crit = FakeCritique(verdict="pass", cites=[], stub_fallback=True)
        manifest, criteria = {}, None
    else:
        # Live path is reachable only after preflight passes (ratified goldens, key
        # present, ANTHROPIC unset). Deferred this push — see module COSTED-RUN NOTE.
        manifest = _manifest()
        criteria = _merged_criteria(manifest)
        run_dir = Path("/tmp/gate3-run"); run_dir.mkdir(parents=True, exist_ok=True)
        regen = _real_regenerate(run_dir=run_dir, manifest=manifest)
        crit = _real_recritique(manifest=manifest, criteria=criteria)

    corpus = parse_corpus(_CORPUS_MD)
    effs = []
    for c in sample:
        em_kw = {}
        if "em" in arms:
            # The em arm needs Em's ACTUAL proposed clause — captured live by running
            # Em on the defect fixture (one call/case). Stub reuses the golden stand-in.
            em_kw = {"em_value": _stub_em_value(c) if args.stub
                     else _capture_em_value(c, manifest=manifest, criteria=criteria)}
        effs.append(run_case(c, arms=arms, rerolls=args.rerolls, corpus=corpus,
                             manifest=manifest, criteria=criteria,
                             regenerate_fn=regen, recritique_fn=crit, **em_kw))
    agg = aggregate_efficacy(effs)
    lift = normalized_lift(agg)  # {} unless all three arms (em+golden+null) ran
    label = "STUB (no efficacy claim)" if args.stub else "LIVE"
    print(json.dumps({"label": label, "estimate": est, "aggregate": agg,
                      "normalized_lift": lift}, indent=2))


def _manifest() -> dict:
    root = HERE.parents[1]
    full = yaml.safe_load((root / "manifest.yaml").read_text(encoding="utf-8"))
    return {"critics": full.get("critics", {}),
            "criteria_sources": full.get("criteria_sources", {}),
            "characters_root": str(root / "characters")}


def _merged_criteria(manifest: dict):
    from pipeline.criteria import load_all_criteria
    return load_all_criteria(manifest)


def _stub_em_value(case: dict) -> str:
    """In --stub mode the 'em arm' has no real Em output; reuse the golden as a
    stand-in so the arm exercises (clearly labelled STUB, no efficacy claim)."""
    return case.get("golden_diff", "")


def _capture_em_value(case: dict, *, manifest: dict, criteria):
    """Capture Em's proposed corrective clause for the em arm: run Em LIVE on the DEFECT
    fixture (Gate 0 capture path) and return the first proposed_patches[].value. Returns
    None when Em proposed nothing (a real outcome → the em arm records skipped_no_proposal,
    never a 0). One Em call per case (accounted as em_capture_calls in estimate_cost).
    The §0 `score.py --dump-patches` proves this capture is non-empty before any spend."""
    from pipeline.agents import AgentContext
    from pipeline.agents.vision_critic import VisionCriticNode, EmptyCitesInvariant
    ctx = AgentContext(
        run_dir=Path("/tmp/gate3-capture"),
        inputs={"image_path": str(HERE / "fixtures" / case["input"]),
                "beat_description": case["beat_description"],
                "frame_id": f"capture-{case['name']}",
                "impact_tags": case.get("impact_tags", []),
                "checkpoint": case["checkpoint"],
                "character_id": case.get("character_id", "sean")},
        manifest=manifest, criteria=criteria, tier="draft",
        cache_dir=Path("/tmp/gate3-capture/.cache"))
    try:
        res = VisionCriticNode().run(ctx)
    except EmptyCitesInvariant:
        return None
    patches = res.proposed_patches
    return patches[0].value if patches else None


if __name__ == "__main__":
    main()
