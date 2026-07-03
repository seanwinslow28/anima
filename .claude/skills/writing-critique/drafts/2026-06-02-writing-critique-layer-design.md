# Design: writing-critique layer + evidence upgrade

- **Date:** 2026-06-02
- **Status:** Approved (brainstorming) — pending implementation plan
- **Author:** Sean Winslow + Claude
- **Branch:** skill/writing-humanity-pass (or a fresh skill/writing-critique branch)

## Context

Sean's writing system is a four-stage **generative** chain:

```
storytelling-architecture → substack-value-engine → writing-voice-modes → writing-humanity-pass
   (beat SHAPE)               (value GATE)            (every SENTENCE)      (scrub, LAST)
```

Every stage *produces*. None *adversarially evaluates*. A comparison against the
external repo [`haowjy/creative-writing-skills`](https://github.com/haowjy/creative-writing-skills)
(Apache-2.0) — a multi-agent **fiction** system — found that ~90% of it (worldbuilding,
lore, continuity, character-sim, POV head-hopping, kb machinery) does not map to Sean's
nonfiction/Substack work, **but** its *evaluative* layer is strong and lands exactly on the
gap above. Three things are worth adopting:

1. **An adversarial critique pass** — their `prose-critique` core ("find what doesn't work,
   not confirm what does") + the **Specific / Reasoned / Directable / Non-obvious** finding
   rubric + stage calibration. Domain-agnostic; ports directly.
2. **A mechanical analyzer** (`analyze.py`) — stdlib, $0, measures sentence-length variance,
   opener variety, repetition, pronoun distribution. Quantifies what humanity-pass currently
   only eyeballs ("variety in sentence length" is a Sign of Human Writing it can't measure).
3. **Evidence-quality discipline** — their `antipatterns.md` stratifies AI tells by evidence
   (research-backed measurable / community folklore / unreliable word-lists). A calibration
   cross-check for the flat 30-pattern catalog in `writing-humanity-pass/references/ai-tells.md`.

### What we are NOT taking
Fiction infra (lore-keeper, continuity-checker, character-sim, kb-management, story-context,
writing-staffing, project-setup); multi-agent orchestration (muse/writer/critic/reviser); their
em-dash guidance (Sean's hard ban is already stronger); their style-analysis method (Sean already
executed it as his five calibrated modes).

## Goals

- Add one new skill, `writing-critique`, that adversarially reads a draft and returns triaged,
  directable findings + a verdict + the single highest-leverage fix. **Critiques; never rewrites.**
- Works **standalone** (on-demand red-team) **and** as a **chain gate** between voice and humanity,
  with interactive-vs-headless detection mirroring `writing-humanity-pass`.
- Ship a stdlib mechanical analyzer with an optional **baseline** captured from Sean's voice corpus,
  so "is this AI-flat?" becomes a comparison against his own prose, not a guess.
- Upgrade `ai-tells.md` to stratify its 30 patterns by evidence quality and wire the measurable
  signals to the analyzer — without deleting any pattern.

## Non-goals (YAGNI)

- No multi-agent orchestration, no fiction machinery, no new runtime dependencies.
- No auto-revise-until-clean loop (max **one** revise pass in headless mode).
- Critique is **advisory**, not a hard block (unlike the value gate, which blocks at the idea stage).
- The skill never edits or rewrites prose. It produces findings; fixes route back to voice-modes /
  humanity-pass or to Sean.

## The chain after this change

```
storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass
   (beat SHAPE)               (value GATE)            (every SENTENCE)      (RED-TEAM, advisory)  (scrub, LAST)
```

Critique sits **between voice and humanity** so humanity-pass keeps its "runs LAST" identity. On a
serious (reader-cost) finding it can trigger **one** revise loop back through voice; humanity-pass
still scrubs last. The analyzer runs at the critique stage on the *voiced* draft (pre-scrub): it
*informs* the revise decision; humanity-pass still does the qualitative scrub afterward. No conflict.

## Components

### New skill: `.claude/skills/writing-critique/`

```
writing-critique/
├── SKILL.md
├── references/
│   ├── finding-rubric.md      # adversarial mindset, the 4-quality rubric, stage calibration, report format
│   ├── analyze.py             # stdlib mechanical analyzer (adapted from upstream)
│   ├── baseline-corpus.md     # curated Sean-only prose extracted from voice-samples.md
│   └── baseline.json          # precomputed baseline metrics (regenerable)
├── drafts/
│   └── 2026-06-02-writing-critique-layer-design.md   # this file
├── evals.yaml
└── evals.sealed.yaml
```

#### SKILL.md spec

- **Frontmatter:** `name: writing-critique`; description with trigger phrases ("red-team this draft",
  "what's weak here", "critique this", "find what doesn't work", "is this ready to ship", "what would
  a skeptical reader catch", "review my draft") + the chain-gate role.
- **Purpose:** adversarial reading. Find what fails, not confirm what works. A critique that says
  "well done" without digging creates false confidence and is worse than none.
- **Two modes:**
  - **Standalone (interactive):** read draft → auto-assess focus or take an assigned one → produce
    findings via the rubric → optionally run the analyzer → return a triaged report with a verdict
    and the one highest-leverage fix. Does not rewrite.
  - **Chain gate:** runs on the voiced draft. Detect interactive vs headless (same mechanism as
    humanity-pass). Interactive → present findings, Sean decides revise/proceed. Headless
    (substack-drafter) → if any reader-cost finding, emit **one** structured revise request back to
    voice, then proceed; else pass through. Always non-destructive. Emit a machine-readable verdict
    block in a trailing HTML comment (mirrors humanity-pass headless output).
- **Five dimensions** (each *defers* to the owning skill; critiques execution, never re-litigates the
  premise):
  1. **Structure** — hook strength, but/therefore seams, open-loop closure, slippery-slide section
     ends. Defers to `storytelling-architecture`.
  2. **Value** — Itch/Solution/Transfer actually delivered, narrative-to-value seam intact, Rule-of-One
     held, one usable thing in 10 minutes. Defers to `substack-value-engine`.
  3. **Voice** — reads as Sean (signature moves present) vs generic-competent narrator; register drift
     (the nonfiction analog of their "flattening voice" / "voice drift"). Defers to `writing-voice-modes`.
  4. **Prose / line** — rhythm, sentence variety, repetition, clarity, show-don't-summarize,
     tidy-summary endings, AI-flatness. **The analyzer plugs in here.**
  5. **Hiring signal** (Sean-specific) — judgment shown not claimed, artifact + blameless
     self-post-mortem present, the ask stays sideways. Defers to `substack-value-engine`.
- **Stage calibration:** early draft → structure + value first (don't polish a scene that shouldn't
  exist); late draft → line-level + flatness. "Fix the bones before the skin."
- **Verdict:** explicit — `ship` / `revise` / `structural-rework` — plus the single most important fix.
- **Chain contract:** runs between voice and humanity; advisory; never rewrites; one revise pass max
  in headless. Hand-off is in-context.
- **Attribution:** adapted from `haowjy/creative-writing-skills` (Apache-2.0); retain notice, mirroring
  how humanity-pass credits `blader/humanizer`.
- **Success criteria + Copy/Paste-Ready block** (match the house style of the other four skills).

#### references/finding-rubric.md spec

Ports the upstream `prose-critique` craft, re-aimed at nonfiction:
- **Adversarial mindset:** interrogate how the prose fails (does the hook promise a closeable gap?
  does the value land as payoff or bolted-on appendix? does it read as Sean or as competent-narrator?
  where does attention drift?).
- **What makes a good finding:** Specific (cite paragraph/line), Reasoned (name the concrete reader
  cost), Directable (the writer knows what to do next), Non-obvious (not spellcheck).
- **What wastes time:** vague "could be stronger"; restating the prose; praising what works; relitigating
  committed premises (critique execution, not the idea).
- **Communicating impact:** lead with reader-cost findings, minor observations follow; signal severity.
- **Stage calibration** (early/mid/late) and **report format** (overall assessment → findings by
  severity → verdict + the one fix). Headless: structured verdict block.

#### references/analyze.py spec

Stdlib only (`re`, `statistics`, `collections`, `json`, `argparse`, `pathlib`). No deps. Optional in chain.

- **Keep from upstream:** markdown/frontmatter/fence stripping; sentence-length distribution + **stdev**;
  sentence-opener variety (pronoun/article/conjunction/other); repetition windows; pronoun distribution.
- **Drop:** dialogue-to-narration ratio (fiction-specific, low signal for Sean's nonfiction).
- **Add — MATTR** (Moving-Average Type-Token Ratio, window ~50 tokens) for lexical variability: the
  research-backed signal and the wiring point for the evidence upgrade. Raw TTR is length-biased; MATTR
  is the correct windowed metric. Stdlib-computable.
- **Add — baseline modes:**
  - `--emit-baseline <corpus.md>` → compute per-metric mean/stdev and write `baseline.json`.
  - `--baseline <baseline.json>` → diff the draft's metrics against the baseline and flag deviations:
    sentence-length stdev far below baseline → "monotonous vs your voice"; opener variety collapsed →
    "too many sentences open the same way"; MATTR below baseline range → "narrow vocabulary".
  - `--json` → machine-readable output for the chain gate.
- **Default (no baseline):** raw metrics + generic AI-flat thresholds (e.g. sentence-length stdev below
  ~4 = monotonous) so it is still useful before/without a baseline.
- **CLI:** `python3 analyze.py <draft.md> [--baseline baseline.json] [--json]`.

#### Baseline pipeline (one-time, regenerable)

1. **`baseline-corpus.md`** ← curated extract of **Sean-only** prose from
   `writing-voice-modes/references/voice-samples.md`: the four "Full Exercise Passages (Final Versions)"
   (Domestic Observer, Gonzo, Beat Flow, Minimalist Absurdist) plus the two Professional-Dial samples
   (Slack update + stakeholder intro) — ~1,500 words spanning all five modes (Sean Mode is the
   Professional-Dial 60% hybrid). **Excludes** the "AI wrote:" counter-samples and all meta-analysis.
   Header comment documents provenance + exclusions.
2. **`baseline.json`** ← `python3 analyze.py --emit-baseline baseline-corpus.md`. Committed so the chain
   never recomputes.
3. **Regeneration:** when `voice-samples.md` gains a new calibration round, re-extract the new Sean prose
   into `baseline-corpus.md` and re-run `--emit-baseline`. Documented in SKILL.md.

### Edit: `writing-humanity-pass/references/ai-tells.md` (evidence upgrade)

Additive and surgical — **keeps all 30 patterns**:
- New **"Evidence quality"** section stratifying the catalog:
  - **Research-backed measurable** — lower lexical variability (MATTR), fewer personal pronouns,
    positive-emotion skew. Cite Kobak et al. (2024), RAID (ACL 2024), Ghostbuster (NAACL 2024). Wire to
    `analyze.py`.
  - **Community folklore (useful triggers, not proof)** — clean-but-hollow prose, tidy-summary endings,
    repetitive emotional choreography, metaphor clusters.
  - **Not reliable: word-level slop lists** — model-dependent, prompt-dependent, genre-confounded,
    near-random for Claude specifically. Reframe any of Sean's 30 that are really word-lists as
    *legitimate taste choices*, not detection.
- Mark the **em-dash ban explicitly as a deliberate taste choice Sean owns** — NOT recast as detection.
  (It stays a hard rule; the upgrade just labels its category honestly.)
- Expand the current one-line "Detection guidance" section to point at the stratification + analyzer.
- Add a one-line pointer from `writing-humanity-pass/SKILL.md` references section.

### Chain-diagram updates (consistency)

The four existing writing skills each hardcode the chain diagram. Update each to insert the critique
stage between voice and humanity:
- `storytelling-architecture/SKILL.md` (chain contract block + related skills)
- `substack-value-engine/SKILL.md` (chain contract block + related skills)
- `writing-voice-modes/SKILL.md` (chain references)
- `writing-humanity-pass/SKILL.md` (integration block + related skills)

### evals

`evals.yaml` + `evals.sealed.yaml` using the repo's manual-review schema (`schema_version: 1`, `cases`
with `id`/`input`/`expect`), modeled on `storytelling-architecture/evals.yaml`. Cases test the SHAPE of
the critique output, not prose. Candidate cases:
- `finds_reader_cost_not_typos` — flags a structural/value problem, not spellcheck.
- `findings_are_directable` — each finding says what to do next.
- `defers_to_owner_skill` — critiques execution of the value gate, doesn't re-litigate the idea.
- `verdict_is_explicit` — output ends with ship/revise/structural-rework + the one fix.
- `never_rewrites` — returns findings, not a rewritten draft.
- `flags_ai_flatness_with_analyzer` — low sentence-variance draft surfaces a flatness finding.
- `headless_emits_structured_verdict` — non-interactive context returns a machine-readable verdict block.

### Repo integration (per CLAUDE.md "When Modifying")

- `CHANGELOG.md` entry for the new skill + the ai-tells.md upgrade.
- Update any skill **count tables** in `CLAUDE.md` / `README.md` (+1 skill).
- `python3 scripts/validate.py` after changes (validator hard-enforces the 3 domain folders; the skill
  lives in `.claude/skills/`, so this is a clean add).
- Attribution notice (Apache-2.0) in `writing-critique/SKILL.md` and at the top of `analyze.py`.

## Data flow

**Standalone (interactive):**
```
Sean: "red-team this draft" + draft
  → writing-critique reads draft
  → picks/takes focus, applies finding-rubric across the 5 dimensions
  → (optional) python3 analyze.py draft.md --baseline baseline.json
  → triaged findings + verdict + the one fix   (NO rewrite)
```

**Chain gate (headless, e.g. substack-drafter):**
```
voiced draft
  → writing-critique (detect headless)
  → analyze.py --baseline --json  +  rubric findings
  → if reader-cost finding: emit ONE structured revise request → voice → (re)critique once
  → else: pass through  → writing-humanity-pass (scrub, LAST)
  → trailing HTML comment: {verdict, serious_findings[]}
```

## Error handling / edge cases

- **No Python available (headless):** analyzer is optional — critique proceeds qualitatively; SKILL.md
  states the degraded path.
- **Baseline stale / missing:** analyzer falls back to generic thresholds; logs that baseline was absent.
- **Tiny draft (e.g. a single tweet):** stdev/MATTR are noisy on short text — analyzer reports
  "insufficient length for variance signal" instead of a false flatness flag (mirrors upstream's
  "not enough paragraphs" guard).
- **Critique disagreeing with a committed premise:** rubric forbids re-litigating the idea; critique the
  execution only.
- **Infinite revise risk:** headless mode caps at one revise pass, then proceeds regardless.

## Testing

- `python3 scripts/validate.py` passes with the new skill present.
- `analyze.py` self-test: run on `baseline-corpus.md` (should report healthy variance) and on a
  deliberately monotone paragraph (should flag low stdev + low MATTR).
- `--emit-baseline` produces a `baseline.json` with mean+stdev for every metric.
- Manual eval pass against `evals.yaml` cases.
- A real end-to-end dry run: take one existing Substack draft, run standalone critique, confirm findings
  are specific/directable and the verdict is explicit.

## Attribution / license

Critique rubric + analyzer adapted from `haowjy/creative-writing-skills` (Apache License 2.0). Retain the
attribution in `SKILL.md` and `analyze.py`, mirroring how `writing-humanity-pass` credits
`blader/humanizer` (MIT). The evidence-quality framing's research citations (Kobak 2024, RAID, Ghostbuster)
carry into `ai-tells.md`.

## Open questions

None blocking. Decided during brainstorming: chain position = both (gate + standalone); baseline =
voice-samples corpus; packaging = Approach A (analyzer + baseline live in writing-critique; evidence
upgrade is an in-place ai-tells.md edit); critique = advisory not blocking; drop dialogue-ratio.
