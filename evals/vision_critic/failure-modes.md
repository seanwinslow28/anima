# Em — observed failure-mode taxonomy

This is the **open-coded** taxonomy for Em, anima's T2 vision critic. It was
written *after* reading real anima output, not from imagination (the
error-analysis-first discipline — `docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md` §2).

**Sources read (the open-coding pass, 2026-05-31):**

- **40 real verdict rows** from `runs/*cy*/plate_verdicts.jsonl` — every row is
  a real Cy plate + Gemini-3.1-Pro verdict + the exact `IR.*` rules it cited +
  free-text reasoning + a DINOv2/CLIP similarity score. The richest defect
  evidence in the repo: real "fail" rows with measured reasons ("head-to-body
  ~1:6.2 instead of 1:7", "stylus entirely missing", "8,987 unique colors
  instead of four indexed").
- **Act 1 frames** — approved (`PT_A1_F06/F13/F31_key.png`) and rejected
  (`PT_A1_F31_key-bad.png` = sprite-scale wrong; `F13_attempt_02_CC01.png` =
  stylus-hand continuity).
- **An Act 2 motion contact sheet** — built from the committed
  `museum/pencil-test/act2-seedance-2026-04-27/.../W1_attempt_01.mp4` and looked
  at directly. Six time-ordered panels of Sean walking through the studio: you
  can read identity and style across the strip, and you genuinely *cannot* tell
  whether the motion between panels is smooth or jittery. That is the gap, seen.

The taxonomy splits into two halves on a single axis: **what a contact sheet
can structurally show Em, and what it cannot.** That split is the load-bearing
idea of this whole workstream, so it organizes the document.

---

## Part A — identity/style across time (the contact sheet CAN catch these)

These are the families Em *should* perform on. Every one is recoverable from a
single still or a strip of stills — it is a content question, not a motion
question. Each is illustrated by a real cited row from `plate_verdicts.jsonl`.

### A1. proportion-drift

**What it looks like.** Head-to-body ratio, shoulder width, or hip-to-floor
height drifts off the locked figure. The single most common defect in the Cy
runs.

**Real case.** `sean-anchor-production / turnarounds/body-3quarter.png` —
`fail` @1.0, sim 0.51. Cited `IR.sean.proportion.head-to-body-1-to-7` +
`IR.sean.proportion.shoulder-width-1-5-head-widths`; reasoning: "Only one of
the five identity rules is honored." Also `sean-anchor-rebake / body-3quarter`
— "head-to-body proportion is ~1:6.2 instead of 1:7."

**Fix vector.** Re-anchor from the figure reference with an explicit ratio
correction in the prompt. This is the SF03 retry-ladder mode in manifest terms.

### A2. missing-prop (the stylus)

**What it looks like.** A required prop (Sean's stylus) is absent, or present
in the wrong hand.

**Real case.** `sean-anchor-rebake / body-3quarter.png` — `fail` @0.8: "stylus
is entirely missing from all views" (`IR.sean.prop.stylus-right-hand-always`).
The Act 1 continuity mode `CC01` (stylus in the RIGHT hand) is the motion-clip
analogue — `F13_attempt_02_CC01.png` is the rejected real frame.

**Fix vector.** Add explicit prop placement to the prompt; CC01/CC02 continuity
gate across a clip's contact sheet.

### A3. costume-drift

**What it looks like.** Outfit deviates from the locked costume — wrong shirt,
uncuffed jeans, missing sneaker detail.

**Real case.** `sean-anchor-production / body-profile-left.png` — `fail` @0.98,
cited `IR.sean.costume.default-outfit-locked` +
`IR.sean.costume.navy-tee-cool-gray-jeans`. Contrast the *pass*:
`sean-anchor-rebake / body-back.png` honored `cuffed-jeans-gray-sneakers`
("single cuff, two back pockets, gray low-top sneakers") — Em reads this detail
reliably.

**Fix vector.** Costume clause in the prompt; this is a clean contact-sheet
continuity check (same outfit t0→tN).

### A4. palette / register break

**What it looks like.** Colors fall outside the locked vocabulary, or the image
is in the wrong *register* entirely (a polished render where a pencil sketch
was specified, or a JPEG-compressed file saved with a `.png` extension blowing
the indexed palette open).

**Real case.** `claude-mascot-production / body-3quarter.png` (the superseded
pixel register) — `fail` @1.0: "saved as a JPEG (with a .png extension) and
containing 12,238 unique colors instead of 4." And the most instructive row of
all: `claude-mascot-production / expressions/neutral.png` — `fail` @1.0 at
**similarity 1.0**, because the plate was "identical to the canonical anchor"
but in the *wrong register* (pencil sketch where pixel art was required). A
high pixel-similarity can sit on top of a total register failure — see the
false-pass note (Part C) and the boil wrinkle (Part D).

**Fix vector.** Style-register clause; the closed-vocabulary register library.
Note the similarity gate alone cannot separate register from identity (it is
record-only in anima for exactly this reason).

### A5. construction-line / line-weight drift

**What it looks like.** The pencil-test register's visible construction lines
disappear, or line weight flattens to a uniform stroke instead of the varied
HB–2B contour.

**Real case.** `sean-anchor-production / body-3quarter.png` also cited
`IR.sean.style.construction-lines-visible-beneath-final`. Act 1 retry notes
describe trails reading "1px flat vs F13's varied 1–3px."

**Fix vector.** Line-weight + construction-line clause; SF01 style-drift retry.

### A6. jaw-line / face-feature drift

**What it looks like.** Jaw squares up or rounds off the locked angle; eyes
drift in color, spacing, or shape.

**Real case.** `sean-anchor-production / body-profile-right.png` — `fail` @1.0,
cited `IR.sean.face.jaw-line-angular-not-rounded` + `IR.sean.face.blue-eyes`.
The mascot analogue: `mascot-pencil-bake / neutral.png` — "eyes are positioned
extremely far apart (~196px gap)" (`IR.claude-mascot.face.two-dot-eyes-with-brows`).

**Fix vector.** Face-feature clause; SF02 identity-drift re-anchor.

### A7. missing-anatomical-feature in a non-front view

**What it looks like.** A feature visible in one view drops out of another — a
far-side limb/ear omitted in a ¾-back view.

**Real case.** `mascot-pencil / body-3quarter-back.png` — `fail` @0.95: "only
the left (near) ear/arm nub is drawn; the right (far) nub is completely [missing]"
(`IR.claude-mascot.anatomy.two-ear-arm-nubs`). This is exactly the kind of
view-dependent drift a single front anchor cannot police — it needs the strip.

**Fix vector.** Per-view reference; flagged in CLAUDE.md as future Bible work.

### A8. parse-failure → defensive borderline (an Em-side mode, not a frame mode)

**What it looks like.** The model's response isn't valid JSON; Em's `_parse`
defensively returns `borderline @0.0` rather than crashing.

**Real case.** `claude-mascot-production / head-front.png` and
`sean-anchor-rebake / body-front.png` both carry "Gemini's response could not
be parsed as JSON," verdict `borderline`, cites `[]`. This is correct behavior
(an uninterpretable response must never read as a pass), but it is a real
source of borderlines in the baseline and must not be miscounted as a *judgment*
borderline. The eval's `cites_correctness` returns `None` for these, and the
harness must not let a flagged-but-uncited parse-failure violate Em's
`cites_criteria` invariant — `make_vision_verdict` supplies a cite for flagged
verdicts so the *harness* exercises the path; we never weaken the invariant.

---

## Part B — motion-proper (the contact sheet CANNOT catch these — ships RED)

These families are **invisible in a contact sheet by construction.** A strip of
6 stills shows you *where* the figure is at t0…t5; it cannot show you *how* it
got between them. The decisive finding (arXiv 2505.14321, summarized in the
eval-strategy doc §3.5): MLLMs answer video questions correctly even on
*shuffled* frames — so a model "reasoning" about motion from a contact sheet is
guessing from content priors, not seeing motion. The honesty clause in
`vision_critic._build_prompt` (`phase_6_motion`) tells Em this explicitly and
instructs her to **defer**, not guess.

We add these cases anyway, labeled with the true defect, and they **ship red**:
Em is *expected to miss them*, and the miss is the artifact. They double as the
pre-stocked validation set for the deferred deterministic motion metric
(E_warp / VBench), per Sean's locked decision.

### B1. motion-arc smoothness
A walk or gesture that should follow a smooth arc instead snaps or eases wrong.
The endpoints can both be perfect stills.

### B2. jitter / skating
Sub-frame instability or feet that slide instead of plant. A contact sheet's
sampled panels can each be individually plausible.

### B3. temporal flicker
A region that strobes in brightness/detail between frames. Sampling 6 of N
frames will usually miss the strobe entirely.

### B4. texture-crawl / boiling (as an *artifact*)
The generated line/texture crawls frame-to-frame in a way the artist did not
intend. **Distinct from intentional pencil boil** — see Part D.

**Why red, not a bug.** Scoring these inside the `motion_proper` segment means a
miss registers as a false-pass *within that segment only*, which is the intended
red. Segmenting (Part C) keeps these expected failures from burying the contact
sheet's real `performs` number.

---

## Part C — the false-pass danger (the costly error, and where it hides)

The expensive mistake is **not** a false alarm (Em flags a clean frame — cheap,
a human waves it through). The expensive mistake is the **false pass**: a
drifted frame Em lets through, which then ships. Per the metric contract (§4),
`false_pass_rate` is reported front and center, and raw agreement is never the
headline (it flatters under class imbalance).

The false pass hides in **borderline→pass slippage.** A frame that should have
been a hard `fail` gets softened to `borderline`, and a `borderline` that should
have triggered rework gets waved to `pass`. So the eval scores a second question
beyond the verdict: *should this borderline have been a fail?* (`borderline_slippage`
in `scoring.py`). The Cy ledger is full of `borderline @0.95` rows that are one
judgment call away from either side (`mascot-pencil-bake / body-side.png`: "honors
five of six… borderline on the leg configuration rule") — exactly where
slippage lives.

---

## Part D — wrinkles to hold, not to "fix"

### D1. intentional pencil boil vs. artifact texture-crawl
The pencil-test register *wants* a living, slightly-boiling line. A naive
flicker-minimizing metric (the kind E_warp rewards) would punish the very thing
that makes the style read as hand-drawn. So motion-proper texture quality is a
**human-look candidate, not a deterministic gate** (§3.5). Any future E_warp/VBench
work must be calibrated against this — which is part of why the red motion cases
exist as a validation set first.

### D2. inter-rater reliability is deferred by scale, not by principle
Cohen's κ and inter-rater agreement need a *second* labeler. At anima's current
solo scale, Sean is the single benevolent dictator of the labels (§2): the cases
encode his rubric, he ratifies them at the STOP gate, and a disagreement between
Em and a label is resolved by him. κ becomes meaningful "later, if ever" — when
a second labeler exists. Until then, "agreement with Sean" is the ground truth,
and the honest move is to say so rather than dress a solo rubric in a
two-rater statistic.

---

*Eval discipline: ships-red is the artifact, never tune-a-case-until-Em-passes
(that measures the thermometer against itself). Editing a label is legitimate
only when the label was wrong — a validity fix — never to flatter the score. The
list grows as real motion runs surface modes the seed cases didn't predict.*
