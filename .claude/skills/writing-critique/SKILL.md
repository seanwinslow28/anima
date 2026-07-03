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
