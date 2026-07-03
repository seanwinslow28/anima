# AI Tells: Adapted Pattern Catalog (Sean-calibrated)

The 30 documented "Signs of AI writing," adapted from `blader/humanizer` (MIT, v2.7.0) and Wikipedia "Signs of AI writing." Upstream numbering kept for re-sync.

Tag legend:
- `[SLOP]`: always cut, both registers. Pure machine residue.
- `[CLASH->X]`: collides with Sean's signature move X. In VOICE-SAFE, defer to the move (see `voice-safe-exceptions.md`). In FULL (neutral) scrub, cut it.

---

## Content patterns

**#1. Significance / legacy / broader-trend inflation** `[CLASH->Hard Cut/Deflation]`
Watch: stands/serves as, is a testament/reminder, pivotal moment, underscores its importance, reflects broader, marking a shift, evolving landscape, indelible mark.
Cut: puffed-up "this represents a broader movement" framing. Voice-safe: KEEP the epic build only when it lands on a mundane or absurd deflation in the final clause; cut it when it inflates and never deflates.
Ex: "marking a pivotal moment in the evolution of regional statistics" becomes "established in 1989 to publish regional statistics."

**#2. Notability / media-coverage name-dropping** `[SLOP]`
Watch: cited in [outlet list], active social media presence, written by a leading expert.
Cut: source lists without context. Ex: "cited in NYT, BBC, FT, and The Hindu" becomes "In a 2024 NYT interview, she argued X."

**#3. Superficial -ing analyses** `[SLOP]`
Watch: highlighting..., ensuring..., reflecting/symbolizing..., contributing to..., showcasing...
Cut: present-participle tails that fake depth. Ex: "...resonates with the region, symbolizing X, reflecting Y" becomes a plain fact with a source.

**#4. Promotional / advertisement language** `[SLOP]`
Watch: boasts a, vibrant, rich (figurative), nestled, in the heart of, breathtaking, must-visit, renowned, stunning.
Cut: brochure tone. Ex: "Nestled within the breathtaking region, stands as a vibrant town" becomes "is a town in the X region, known for its weekly market."

**#5. Vague attributions / weasel words** `[SLOP]`
Watch: Industry reports, Observers have cited, Experts argue, Some critics argue, several sources (when few cited).
Cut: opinions pinned to vague authorities. Ex: "Experts believe it plays a crucial role" becomes "supports endemic fish species, per a 2019 survey by X."

**#6. Formulaic "Challenges and Future Prospects" sections** `[SLOP]`
Watch: Despite its, faces several challenges, Despite these challenges, Future Outlook, Challenges and Legacy.
Cut: the boilerplate section. Replace with specific facts.

## Language and grammar patterns

**#7. Overused "AI vocabulary"** `[SLOP]`
Watch: actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (v), interplay, intricate, key (adj), landscape (abstract), pivotal, showcase, tapestry, testament, underscore (v), valuable, vibrant.
Cut: especially when these co-occur. Replace with plain words ("also", "remain common").

**#8. Copula avoidance** `[SLOP]`
Watch: serves as / stands as / marks / represents [a], boasts / features / offers [a].
Cut: restore is/are/has. Ex: "Gallery 825 serves as LAAA's exhibition space and boasts 3,000 sq ft" becomes "Gallery 825 is LAAA's exhibition space and has 3,000 sq ft."

**#9. Negative parallelisms / tailing negations** `[SLOP]`
Watch: "Not only...but...", "It's not just X, it's Y", clipped tails like "no guessing", "no wasted motion".
Cut: state the point directly. Sean does NOT use these; confirm in eval. Ex: "It's not just a song, it's a statement" becomes "The beat sets the aggressive tone."

**#10. Rule of three overuse** `[CLASH->Rule of Three + Emotional Pivot]`
Watch: forced triples ("innovation, inspiration, and insights").
Cut: decorative triples. Voice-safe: KEEP when items 1 and 2 are concrete or light and item 3 pivots to genuine feeling ("skills, coffee, and for once in my life, a glimmer of hope"). The pivot is the point.

**#11. Elegant variation (synonym cycling)** `[SLOP]`
Watch: protagonist, then main character, then central figure, then hero, all for one subject.
Cut: repeat the clearest noun. Ex: collapse the cycle to "the protagonist eventually triumphs and returns home."

**#12. False ranges** `[CLASH->metaphor stacking]`
Watch: "from X to Y" where X and Y are not a real scale.
Cut: non-scale ranges become a plain list. Voice-safe: KEEP escalating metaphor stacks that describe the SAME thing (ship of the damned, then sheep, then hamster wheel); those are not false ranges.

**#13. Passive voice / subjectless fragments** `[SLOP]`
Watch: "No configuration file needed", "The results are preserved automatically".
Cut: name the actor when active voice is clearer. Ex: "No configuration file needed" becomes "You don't need a configuration file."

## Style patterns

**#14. Em / en dashes** `[SLOP]` (HARD CUT, see SKILL.md)
Watch: `—`, `–`, spaced ` — `, double-hyphen ` -- `.
Cut: ALL of them, both registers. Replace in order: period, comma, colon, parentheses, restructure. Final-output guard: grep for the characters; any hit means not done.

**#15. Boldface overuse** `[SLOP]`
Cut: mechanical phrase-bolding. Ex: "**OKRs**, **KPIs**, **BMC**" becomes "OKRs, KPIs, BMC."

**#16. Inline-header vertical lists** `[SLOP]`
Watch: "- **Performance:** Performance improved..."
Cut: convert to prose. Ex: three bolded-header bullets become one sentence covering all three.

**#17. Title Case in headings** `[SLOP]`
Cut: "## Strategic Negotiations And Partnerships" becomes "## Strategic negotiations and partnerships" (sentence case).

**#18. Emojis** `[SLOP]`
Cut: decorative emojis on headings or bullets. Ex: a rocket-emoji "Launch Phase:" header becomes "The product launches in Q3."

**#19. Curly quotation marks** `[SLOP]` (low confidence alone)
Cut: convert curly quotes to straight quotes only when stacked with other tells (auto-curl is common and innocent on its own).

## Communication patterns

**#20. Collaborative / chatbot artifacts** `[SLOP]`
Watch: I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...
Cut: entirely. Ex: "Here is an overview... I hope this helps!" becomes the content, starting directly.

**#21. Cutoff disclaimers / speculative gap-fill** `[SLOP]`
Watch: as of [date], while specific details are limited, based on available information, maintains a low profile, keeps personal details private, likely [grew up/studied], it is believed that.
Cut: say what isn't known, or cut the sentence. Don't dress a guess as fact.

**#22. Sycophantic / servile tone** `[SLOP]`
Watch: Great question!, You're absolutely right!, That's an excellent point.
Cut: respond directly. Ex: "Great question! You're absolutely right that..." becomes "The economic factors you mentioned are relevant."

## Filler and hedging

**#23. Filler phrases** `[SLOP]`
Cut: "in order to" becomes "to"; "due to the fact that" becomes "because"; "at this point in time" becomes "now"; "has the ability to" becomes "can"; "it is important to note that the data shows" becomes "the data shows."

**#24. Excessive hedging** `[SLOP]`
Watch: could potentially possibly, might have some effect.
Cut: "It could potentially possibly be argued that the policy might have some effect" becomes "The policy may affect outcomes."

**#25. Generic positive conclusions** `[CLASH->Callback Closer]`
Watch: the future looks bright, exciting times lie ahead, a step in the right direction.
Cut: the vague-upbeat shape. Voice-safe: the closer is Sean's strongest move, so defer the closer SLOT to the Callback Closer (it must transform the opening image). Never let any closer default to this vague-upbeat shape.

**#26. Hyphenated word-pair overuse** `[SLOP]`
Watch: third-party, cross-functional, data-driven, decision-making, well-known, high-quality, real-time, long-term, end-to-end.
Cut: keep the hyphen in attributive position ("a high-quality report"); drop it in predicate position ("the report is high quality").

**#27. Persuasive-authority tropes** `[SLOP]`
Watch: the real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter.
Cut: drop the ceremony, state the point. Ex: "At its core, what really matters is organizational readiness" becomes "That mostly depends on whether the org will change its habits."

**#28. Signposting / announcements** `[SLOP]`
Watch: Let's dive in, let's explore, let's break this down, here's what you need to know, without further ado.
Cut: do the thing instead of announcing it. Ex: "Let's dive into how caching works." becomes "Next.js caches data at multiple layers: ..."

**#29. Fragmented headers** `[SLOP]`
Watch: a heading followed by a one-line paragraph that restates the heading.
Cut: delete the warm-up line; let the heading do its work.

**#30. Diff-anchored writing** `[SLOP]`
Watch: docs or comments narrating a change ("This was added to replace...") in a non-version-scoped doc.
Cut: describe the thing as it is. Ex: "This function was added to replace the old O(n^2) loop" becomes "This function uses a hash map for O(1) lookups."

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
