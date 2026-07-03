---
type: design-draft
status: ready-for-canonical-edit
topic: writing-voice-modes-didion-addition
created: 2026-05-23
source_trigger: agents-sdk/docs/multi-cli-smoke-2026-05-21/ (Codex + Anti-Gravity convergence on Joan Didion)
parent_skill: .claude/skills/writing-voice-modes/SKILL.md
applies_to_concept: vault/knowledge/concepts/writing-voice-modes.md
interview_method: /superpowers:brainstorming (4 AskUserQuestion rounds, 9 questions answered)
explicit_approvals:
  - mode_name: "Forensic Diagnostic Mode (Didion)"
  - mechanic_selection: "All three — Catalog → Flat Pivot, Held-Camera Sentence, Bookend Reframe"
  - calibration: "All three samples land — ship as drafted"
  - anchor_works: "Primary: The White Album (essay); Secondary: Goodbye to All That"
  - sean_mode_relationship: "Stay separate — specialty register, not a hybrid ingredient"
out_of_scope_for_this_session:
  - "Other 4 missing-mode recommendations from smoke test (McPhee, Maggie Nelson, Baldwin, Byung-Chul Han) — separate sessions later"
  - "Editing canonical SKILL.md — happens in a separate session after Sean reviews this draft"
  - "Invoking skill-optimizer agent — this is a manual design session, not a convergence loop"
---

# Forensic Diagnostic Mode (Didion) — Design Draft

## 1. Brief description (1–2 sentences)

A cold-camera diagnostic mode anchored on Joan Didion's *The White Album* (1979) and *Goodbye to All That* (1967), built to write the version of an essay where the moral charge arrives from arrangement rather than commentary. The mode strips the comic register that lives in Sean Mode and substitutes a held-camera evidentiary stance — useful when comedy would feel like avoidance of the actual material.

## 2. Mode name

**Forensic Diagnostic Mode (Didion)**

Final pick from a three-option AskUserQuestion round (alternatives offered: Held-Camera Mode, Cold Diagnostic Mode). Sean chose this option because the descriptor names the *function* (the held-camera evidence-gathering plus the diagnostic arc) in a way that parallels his existing "Gonzo Technical" two-word functional label.

## 3. Anchor work(s)

- **Primary:** *The White Album* — the titular essay (1979), specifically the first three paragraphs (pp. 11–13 in the FSG edition).
- **Secondary:** *Goodbye to All That* — opening + closing sentences (1967, collected in *Slouching Towards Bethlehem*).

Sean explicitly chose the "primary + secondary" anchor option over both the tightest ("single essay only") and the broadest ("*White Album* full collection + *Slouching* essay + *Goodbye*"). Rationale: primary keeps calibration tight on the consensus essay both CLIs flagged; secondary supplies the Bookend Reframe mechanic which is cleanest in *Goodbye to All That*.

## 4. Sentence patterns — three mechanics, all anchored on verbatim primary specimens

### Mechanic 1 — Catalog → Flat Pivot

**The move:** Cascade of disparate hyper-specific concretes (people, places, factual details that don't obviously belong in a list together) → paragraph break → short flat declarative sentence that reframes the cascade.

**Verbatim specimen — *The White Album*, opening paragraph + break (1979, p. 11):**

> WE TELL OURSELVES stories in order to live. The princess is caged in the consulate. The man with the candy will lead the children into the sea. The naked woman on the ledge outside the window on the sixteenth floor is a victim of accidie, or the naked woman is an exhibitionist, and it would be "interesting" to know which. We tell ourselves that it makes some difference whether the naked woman is about to commit a mortal sin or is about to register a political protest or is about to be, the Aristophanic view, snatched back to the human condition by the fireman in priest's clothing just visible in the window behind her, the one smiling at the tele-photo lens. We look for the sermon in the suicide, for the social or moral lesson in the murder of five. We interpret what we see, select the most workable of the multiple choices. We live entirely, especially if we are writers, by the imposition of a narrative line upon disparate images, by the "ideas" with which we have learned to freeze the shifting phantasmagoria which is our actual experience.
>
> **Or at least we do for a while.**

The pivot ("Or at least we do for a while") is the engine. The cascade earns the right to a single short sentence; the short sentence reframes everything that came before.

### Mechanic 2 — Held-Camera Sentence

**The move:** Report the facts in flat declarative form. Let the moral charge surface from the *arrangement* and *selection* of the evidence, never from a verb of judgment. Didion's own 1976 essay names the principle: "to shift the structure of a sentence alters the meaning of that sentence, as definitely and inflexibly as the position of a camera alters the meaning of the object photographed."

**Verbatim specimen — *The White Album*, second paragraph (1979, p. 11–12):**

> I appeared, on the face of it, a competent enough member of some community or another, a signer of contracts and Air Travel cards, a citizen: I wrote a couple of times a month for one magazine or another, published two books, worked on several motion pictures; participated in the paranoia of the time, in the raising of a small child, and in the entertainment of large numbers of people passing through my house; made gingham curtains for spare bedrooms, remembered to ask agents if any reduction of points would be *pari passu* with the financing studio, put lentils to soak on Saturday night for lentil soup on Sunday, made quarterly F. I. C. A. payments and renewed my driver's license on time, missing on the written examination only the question about the financial responsibility of California drivers.

The cascade ends with a wry, deflating, specific micro-fact ("missing on the written examination only the question about the financial responsibility of California drivers") that does the indictment by selection. No "and yet I felt empty" follows — the held camera trusts the reader to do the work.

### Mechanic 3 — Bookend Reframe

**The move:** The essay (or section) closes by returning to its opening image with *one element changed*. The meaning of the original sentence inverts retroactively.

**Verbatim specimen — *Goodbye to All That* (1967, collected in *Slouching Towards Bethlehem*):**

> Opening: "Nothing was irrevocable; everything was within reach."
>
> Closer: "I could stay up all night and make mistakes, and none of them would count."

The opener is buoyancy; the closer is the same shape ("everything was X / mistakes wouldn't count") but the affect has inverted — what read as freedom now reads as the absence of consequence. The bookend does the work the middle would have over-explained.

### Why three, not one or two

Sean explicitly chose all three over the tighter two-mechanic options. Each mechanic does different work along the essay arc: Catalog → Flat Pivot **opens**, Held-Camera **carries the middle**, Bookend Reframe **closes**. Dropping any one leaves a gap the mode can't fill from the others; together they teach the whole arc.

## 5. Trigger phrases

Sean selected two of four proposed triggers:

1. **"Write this in Didion mode"** — author-named; parallels existing "Use Gonzo mode" / "Write in Beat Flow" conventions; most discoverable.
2. **"Use Forensic Diagnostic"** / **"Diagnose this"** — function-named; cleaner when the goal is the held-camera arrangement rather than Didion-imitation per se.

(Not selected: "Use the White Album voice" and "Make this colder / strip the jokes." These remain available as informal triggers but are not promoted into the canonical Copy/Paste Ready section.)

## 6. Use cases (concrete scenarios from the interview)

Sean selected two of four proposed use cases — explicitly the ones with immediate active relevance:

1. **Substack essays on tech/industry decay or institutional failure** — the natural fit. Sean's existing meaning-over-access manifesto already lives in this neighborhood; Forensic Diagnostic would let him write the *darker* companion essay (the one about what's getting lost in the industry's current pivot) without Sean Mode's comic register softening the blow.
2. **Job-hunt cover letters / About pages needing authority without performance** — both CLIs flagged this. The mode produces "here is what I built, here is what it shows, draw your own conclusion" without the self-implicating comic frame Sean Mode requires.

(Not selected, but available as informal use cases: post-mortems where moral charge needs to land flat, and personal essays about endings. Both remain plausible; flagged in §10 as candidates for re-evaluation after the mode has been used a few times.)

## 7. Anti-patterns (when NOT to deploy)

Sean selected two of four proposed anti-patterns:

1. **Short-form (tweets, Slack messages, daily-note captures)** — the mode needs at least 200–300 words of runway to land the catalog and the flat pivot. Sub-paragraph deployments turn "Or at least we do for a while" into an empty pose.
2. **Anything needing warmth or invitation (welcome notes, intro posts, About pages with founder-energy)** — Held-Camera reads as cold by default. The moral charge it carries works only when the audience is already prepared to look at evidence. Wrong tool for openings that need to feel like a hand on a shoulder.

(Not selected — flagged in §10 as open questions: the past-tense vs. present-tense anti-pattern, and the unresolved-arc anti-pattern. Both have analytical merit but Sean opted to keep the explicit guard tight.)

## 8. Example sentences in Didion mode — Sean topics, generated during the interview

**Sample 1 — The vault silent regression (Catalog → Flat Pivot + Held-Camera):**

> We tell ourselves that observability is the same as observation. The dashboard is green. The job ran on schedule. The manifest reports `status: ok`. The agent has full read access to the vault, full write access to the concepts directory, the right model loaded on the right hardware, the right cron firing at the right minute, the right log line appended at the right second. Nine nights of this. Nine nights of `concepts_written: 0`. We look for the silent failure in the loud success, for the regression hiding inside the OK.
>
> Or at least we do once we know to look.
>
> I had spent the prior week reading evals papers, the production was never meant to be unattended, and the alarm I had built for myself reported only what I had told it to report.

**Sample 2 — The Block restructure (Held-Camera cascade + Flat Pivot):**

> I appeared, on the face of it, a competent enough product manager: I shipped a content calendar that the editors trusted, a campaign-tracking dashboard that the AdOps team trusted, a yield model that the CFO trusted, a runbook that the on-call engineer trusted, a renewal pipeline that finance trusted, a Slack channel called #pm-updates that nobody trusted but everyone read; participated in the quarterly review, in the post-mortem of the launch that nearly worked, in the all-hands where the GM said the runway was eighteen months and meant nine.
>
> The restructure was an adequate enough performance, as improvisations go.
>
> The script was that twelve people made the company go. The plot was that they did, until the day they didn't.

**Sample 3 — The four-minute rollback (Catalog → Flat Pivot + Bookend Reframe):**

> We deploy at 11:47 PM on a Wednesday. The dashboard lights up. The first error arrives in eight seconds. The second in eleven. The 847th arrives at the ninety-second mark, by which time the on-call engineer has thumbs-upped my Slack message, which I read as solidarity and which was, more accurately, a man going back to sleep.
>
> The rollback took four minutes.
>
> The post-mortem took three weeks. The lesson was that I had tested in staging, and staging was wrong, and production was also wrong, but differently. I deploy at 10:30 now. I am older.

Sean's calibration verdict (verbatim from the AskUserQuestion answer): **"All three land — this IS the mode."** Including the comic deflations that survived in Sample 2 ("a Slack channel called #pm-updates that nobody trusted but everyone read") and Sample 3 ("a man going back to sleep") — the mode preserves Sean's wry register inside the cold-camera frame, which both CLIs missed in their original framings.

## 9. Recommended SKILL.md diff — exact text + insertion positions

Apply these five edits to `.claude/skills/writing-voice-modes/SKILL.md` in a separate session. All line numbers reference the canonical file as of 2026-05-23.

### Edit 1 — Frontmatter description (line 3)

**Old:**

```yaml
description: Writing voice and tone control calibrated to Sean's personal style. 5 modes — Domestic Observer (Sedaris), Gonzo Technical (Thompson), Beat Flow (Kerouac), Minimalist Absurdist (Vonnegut), and Sean Mode (calibrated hybrid). Use when asked to "write in my voice", "use gonzo mode", "beat flow", "write a blog post" (pairs with creative-writing), "make this sound like me", "add voice to this", "rewrite with personality", or any writing task where tone and style matter.
```

**New:**

```yaml
description: Writing voice and tone control calibrated to Sean's personal style. 6 modes — Domestic Observer (Sedaris), Gonzo Technical (Thompson), Beat Flow (Kerouac), Minimalist Absurdist (Vonnegut), Sean Mode (calibrated hybrid of the first four), and Forensic Diagnostic (Didion, cold-camera specialty register for institutional/industry essays). Use when asked to "write in my voice", "use gonzo mode", "beat flow", "write this in Didion mode", "diagnose this", "write a blog post" (pairs with creative-writing), "make this sound like me", "add voice to this", "rewrite with personality", or any writing task where tone and style matter.
```

### Edit 2 — Section header (line 71)

**Old:** `## The 5 Voice Modes`

**New:** `## The 6 Voice Modes`

### Edit 3 — Sean Mode description clarification (line 125–132)

**Old:**

```markdown
### 5. Sean Mode (Calibrated Hybrid) — DEFAULT

The natural voice. Load this when no specific mode is requested.

**Base layer:** Sedaris-Thompson — humor, specificity, self-deprecation, self-implication
**Sentence engine:** Kerouac — flowing connective rhythm, sensory anchoring, dash breath marks
**Credibility layer:** Thompson — factual precision (exact numbers, timestamps) dropped AFTER sensory/analogical buildup
**Punctuation:** Vonnegut — refrains as closers, flat one-liners for impact, deployed in bursts
```

**New:**

```markdown
### 5. Sean Mode (Calibrated Hybrid) — DEFAULT

The natural voice. Load this when no specific mode is requested. Hybrid of modes 1–4 only; **Forensic Diagnostic (Didion) is deliberately NOT in the recipe** — it is a specialty register that Sean switches INTO for cold-camera material, not a flavor blended into the default.

**Base layer:** Sedaris-Thompson — humor, specificity, self-deprecation, self-implication
**Sentence engine:** Kerouac — flowing connective rhythm, sensory anchoring, dash breath marks
**Credibility layer:** Thompson — factual precision (exact numbers, timestamps) dropped AFTER sensory/analogical buildup
**Punctuation:** Vonnegut — refrains as closers, flat one-liners for impact, deployed in bursts
```

### Edit 4 — Insert new mode #6 after Sean Mode block (between current line 132 and line 134, before `## Sean's Signature Moves`)

**New text to insert (full block):**

```markdown
### 6. Forensic Diagnostic Mode (Didion-tuned)

Cold-camera specialty register. Anchored on Joan Didion's *The White Album* (1979, titular essay) and *Goodbye to All That* (1967). For diagnostic essays where the moral charge needs to arrive from arrangement, not commentary. Strips Sean Mode's comic register and substitutes a held-camera evidentiary stance.

**Core Mechanics (three):**
- **Catalog → Flat Pivot:** Cascade of disparate hyper-specific concretes (people, places, factual details that don't obviously belong together) → paragraph break → short flat declarative that reframes the cascade. Anchor: "We tell ourselves stories in order to live. [...catalog...] We live entirely, especially if we are writers, by the imposition of a narrative line upon disparate images... // Or at least we do for a while." (*The White Album*, pp. 11)
- **Held-Camera Sentence:** Report the facts in flat declarative form; let the moral charge surface from the *arrangement* of the evidence, never from a verb of judgment. Didion (1976): "to shift the structure of a sentence alters the meaning of that sentence, as definitely and inflexibly as the position of a camera alters the meaning of the object photographed." Cascade ends with a wry, deflating, specific micro-fact that does the indictment by selection — never by "and yet I felt empty" commentary.
- **Bookend Reframe:** Closer returns to the opening image with one element changed; the meaning of the original sentence inverts retroactively. Anchor: *Goodbye to All That* opener "Nothing was irrevocable; everything was within reach" → closer "I could stay up all night and make mistakes, and none of them would count."

**Calibration note (not a fourth mechanic — a guardrail on the three above):** Didion's cascades are funny — "renewed my driver's license on time, missing on the written examination only the question about the financial responsibility of California drivers" is comic deflation. Strip the *jokes-as-jokes*, keep the *deflating specifics*. The mode is cold, not humorless.

**When to deploy:**
- Substack essays on tech/industry decay, institutional failure, or paradigm collapse — when the comic register would soften the blow
- Job-hunt cover letters or About pages needing authority without performance — "here is what I built, here is what it shows, draw your own conclusion"

**When NOT to deploy:**
- Short-form (tweets, Slack, daily-note captures) — needs 200–300 words of runway to land the catalog and pivot
- Anything needing warmth or invitation (welcome notes, intro posts, founder-energy About pages) — Held-Camera reads as cold; the moral charge requires an audience already prepared to look at evidence
```

### Edit 5 — Anti-Patterns table addition (after line 216, the existing "Bad Sean" row, before "Any mode | Desperation Posing as Self-Deprecation")

**New row to insert:**

```markdown
| Forensic Diagnostic | **Bad Didion** | Held-Camera stance without the comic-deflation specifics — turns into LinkedIn thought-leader voice. Or: the abstract "We tell ourselves" opener applied to material the writer doesn't actually have evidence for, which collapses the engine into pose. Or: Bookend Reframe attempted on an unresolved moral arc, forcing a fake resolution. Test: would Didion herself have written this sentence about *her own* material, or does it sound like a writer doing Didion-cosplay? |
```

### Optional Edit 6 — Content Type → Mode Mapping table (lines 168–178)

Sean did not explicitly approve this edit in the interview; treat as a recommendation for the canonical-edit session. Two table rows to add:

```markdown
| Diagnostic essay (institutional/industry decay) | Forensic Diagnostic (Didion) | Vonnegut (flat closers, refrains)        |
| Cover letter / About page (authority without performance) | Forensic Diagnostic (Didion) | Thompson (factual anchoring) at 40-60% dial |
```

## 10. Open questions deferred

These came up during the interview, did not block the design, and are flagged for re-evaluation after the mode has been used 3–5 times in actual writing:

1. **Two use cases dropped during the interview that may want to come back in later:**
   - Post-mortems where the moral charge needs to land flat (currently the SKILL.md routes post-mortems to Kerouac + Thompson; Didion is a plausible alternate when the lesson is structural, not personal)
   - Personal essays about endings (jobs, periods, relationships closing) — *Goodbye to All That* is the canonical anchor; if Sean writes one of these, this use case probably activates retroactively

2. **Two anti-patterns dropped that may resurface in practice:**
   - Present-tense in-the-moment material (Didion is past-tense observational by default; if Sean tries Didion mode on something happening NOW and it feels wrong, codify this guard then)
   - Unresolved moral arcs (Bookend Reframe requires the writer to know what changed; if Sean tries to close a Didion-mode essay on a still-open question and it fakes resolution, codify this guard then)

3. **Professional Dial table (SKILL.md lines 156–164):** Forensic Diagnostic likely needs its own dial logic. Provisional intuition: the mode caps at ~90% in personal writing (full Didion at 100% reads as literary cosplay even at Sean's home register), drops to ~60% for cover letters (where institutional authority requires the held camera but not the full elegiac arc), and is unavailable below 40% (Slack/stakeholder updates can't carry the runway). Not asked during the interview; resolve in a future session after first 2–3 actual uses.

4. **Should the mode require an explicit "I have the evidence" precondition?** Sample 1 in §8 worked because Sean had the *concepts_written: 0* receipts. The Catalog → Flat Pivot mechanic has a known failure mode (it can be invoked rhetorically on material the writer hasn't actually reported); a hard guardrail in the SKILL.md might be useful. Defer until first failure surfaces.

5. **Eval suite update:** `.claude/skills/writing-voice-modes/evals.yaml` currently tests the 5 modes; should grow a Forensic Diagnostic test case before the canonical edit ships. Out of scope for THIS draft per the command args.

## Provenance and how to validate this draft

- All Didion specimens cited in §4 and §9 are **verbatim** from the FSG edition of *The White Album* (1979, pp. 11–12) as retrieved from a hosted PDF on 2026-05-23 (Squarespace CDN; the PDF binary was saved by the WebFetch tool and re-read locally to extract the prose). The *Goodbye to All That* sentences in §4 and §9 are verbatim from the same essay as cited by Qwiklit's stylistic-analysis piece on Didion (2015), corroborated against the Wikipedia entry for *Slouching Towards Bethlehem*.
- The "shift the structure of a sentence alters the meaning" Didion-on-craft quote in §4 is from her 1976 essay *Why I Write* (New York Times Magazine), cited via the Boston Globe's 2021 Vandenberg interview.
- The convergence + divergence analysis in §0 (the implicit pre-interview brief shown to Sean) reconciles Codex's "Forensic Moral Essayist" framing and Anti-Gravity's "Surgical Cultural Synthesis / Anaphoric Flattening" framing as zoom levels on the same essay, not competing readings. Sean confirmed this read in the first AskUserQuestion round.
- The three calibration samples in §8 were generated DURING the interview using Sean's own published material (vault-silent-regression incident from `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/2026-06-19-meaning-over-access-substack-cross.md`; Block restructure from CLAUDE.md context; four-minute rollback from the existing SKILL.md Example 2). All three were approved by Sean before the draft was written.
