---
type: design-draft
status: ready-for-canonical-edit
topic: writing-humanity-pass-new-skill + writing-voice-modes-dedash-reconciliation
created: 2026-06-02
source_trigger: Sean request — adapt blader/humanizer (Wikipedia "Signs of AI writing", v2.7.0, 30 patterns, MIT) into a Sean-calibrated companion that makes output more human
new_skill: .claude/skills/writing-humanity-pass/
parent_skill: .claude/skills/writing-voice-modes/SKILL.md
upstream_reference: https://github.com/blader/humanizer (v2.7.0, MIT) — based on https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
interview_method: /superpowers:brainstorming (1 solo pivotal question + 1 batched round of 4 + 1 reconciliation question)
explicit_approvals:
  - integration_shape: "Standalone companion skill (not folded into voice-modes, not layered)"
  - register_handling: "Auto-detect + branch (voice-safe scrub vs full neutral scrub)"
  - em_dash_policy: "Remove em dashes ALTOGETHER — both registers. Keep the rest of Kerouac. (Sean got burned by dash-abuse output.)"
  - pattern_scope: "All 30 patterns, adapted + annotated with Sean's-voice exceptions"
  - skill_name: "writing-humanity-pass"
  - voice_modes_reconciliation: "Full reconciliation now — de-dash instructions, all examples, AND voice-samples.md anchors"
out_of_scope_for_this_session:
  - "Re-running skill-optimizer convergence loop on either skill — this is a manual design session"
  - "Adding the skill to export-groups / presets / installer manifests (note as a follow-up doc-update task in the plan, not a redesign)"
  - "Wiring writing-humanity-pass into autonomous agents beyond the substack-drafter chain note (substack-drafter already loads voice-modes verbatim)"
needs_sean_review_before_implementation:
  - "voice-samples.md de-dash: punctuation-substitution-only on REAL writing samples. Confirm you're OK editing calibration anchors (vs. adding a normalization note and leaving the raw samples)."
---

# writing-humanity-pass — Design Draft

## 1. Brief description

A standalone editing-pass skill that removes the 30 documented "Signs of AI writing" from a draft and rebuilds human texture, **calibrated to Sean's codified voice**. It pairs with `writing-voice-modes` the way `creative-writing` and `technical-writing` already do: invokable alone ("scrub the AI out of this") or chained as the final pass after a voice write. Its defining feature over upstream `blader/humanizer` is that Sean's voice is the *authority* — a pattern only counts as a tell when it is **not** one of his 13 signature moves.

Companion change in the same project: `writing-voice-modes` is de-dashed end to end so the two skills stop contradicting each other (see §9).

## 2. The core idea (the integration in one sentence)

> **`writing-humanity-pass`'s "do NOT flag" allowlist = `writing-voice-modes`' 13 signature moves.**

Upstream humanizer is voice-agnostic and asks the user to paste a writing sample each run. Sean already has a codified voice (5 modes, 13 signature moves, anti-patterns, `voice-samples.md`, `calibration-notes.md`). So the calibration step is **replaced** by a reference to that existing voice, and the "preserve these / do not flag" lists are bound to Sean's actual craft moves. This is what makes it a Sean-skill rather than a clone.

## 3. Decisions locked (from brainstorming)

| Decision | Choice |
|---|---|
| Integration shape | **Standalone companion skill** |
| Register handling | **Auto-detect + branch** (voice-safe vs neutral) |
| Em dash policy | **Cut entirely, both registers** — keep the rest of Kerouac |
| Pattern scope | **All 30, annotated** with voice exceptions |
| Skill name | **`writing-humanity-pass`** |
| voice-modes reconciliation | **Full de-dash now** (instructions + examples + voice-samples.md) |

## 4. Architecture / file layout

```
.claude/skills/writing-humanity-pass/
  SKILL.md                          # the pass: frontmatter, register branch, scrub loop,
                                    #   conflict rules, the highest-frequency tells inline,
                                    #   integration rules, success criteria, copy/paste triggers
  references/
    ai-tells.md                     # all 30 patterns, adapted to Sean's output, each tagged
                                    #   [pure slop] or [voice clash → defer to move X]
    voice-safe-exceptions.md        # the crosswalk: each [voice clash] tell → the signature move
                                    #   it collides with → how voice-safe mode resolves it
  evals.yaml                        # before/after scrub cases (mirrors voice-modes' eval convention)
  evals.sealed.yaml                 # held-out cases (mirrors voice-modes)
```

`SKILL.md` stays lean (the verbatim-loaded surface for agents like substack-drafter); the 30-pattern detail lives in `references/ai-tells.md` and is read on demand, matching the progressive-disclosure pattern voice-modes already uses for `voice-samples.md`.

### YAML frontmatter (draft)

```yaml
---
name: writing-humanity-pass
description: Remove the documented "Signs of AI writing" from a draft and rebuild human
  texture, calibrated to Sean's voice. Auto-detects voice-bearing vs neutral text and
  scrubs accordingly. Cuts em dashes, significance inflation, -ing padding, copula
  avoidance, chatbot artifacts, filler, hedging, and 24 more tells. Pairs with
  writing-voice-modes (runs as the final pass after a voice write) and runs standalone
  ("scrub the AI out of this", "make this less AI", "de-slop this draft", "humanize this").
  Use when reviewing/editing any draft — yours or agent-generated — that reads like a machine.
---
```

(Description is trigger-tuned: "scrub the AI out", "make this less AI", "de-slop", "humanize this", "sounds like AI", "remove AI tells".)

## 5. Auto-detect register branch

On any input, classify the text, then route:

- **Voice-bearing** (essay, blog, newsletter, LinkedIn, social, post-mortem, personal writing) → **voice-safe scrub**. Cut pure slop; defer to Sean's signature moves. Pull the voice target from `writing-voice-modes` references — **no sample-pasting required**.
- **Neutral** (docs, specs, runbooks, PRDs, reference notes, API docs, agent-generated reference text) → **full aggressive scrub**. Plain, neutral register *is* the correct human voice here (per humanizer's own PERSONALITY-AND-SOUL gating). No personality injection, no first person added.

**Classification signals** (in priority order):
1. Explicit user cue ("this is a blog post" / "this is a runbook" / "neutral scrub").
2. File path / content type (`vault/.../essays/` and substack drafts → voice; `docs/`, `*.spec.md`, runbooks, READMEs → neutral).
3. Internal signal: first-person + narrative + sensory detail → voice; third-person + procedural + reference → neutral.
4. **Default when ambiguous: voice-safe** (the safer failure — it preserves more, scrubs less).

## 6. The scrub loop (kept from humanizer — it's the good part)

The three-step loop is retained because the "what's still AI?" audit is what catches second-order tells:

1. **Draft rewrite** — apply the pattern catalog for the chosen register. Cover everything the original covered (five paragraphs in → five paragraphs out). Preserve meaning.
2. **Audit** — ask explicitly: *"What makes this still read as AI-generated?"* Answer in brief bullets (remaining tells, too-tidy rhythm, slogan-y closer).
3. **Final rewrite** — address the audit bullets. Scan for `—` / `–` / ` -- `; any hit = not done.

**Deliverable (interactive):** draft → brief "still-AI" bullets → final → short change summary.

**Deliverable (headless / agent chain, e.g. substack-drafter):** collapse to final clean text + a one-line change summary in a trailing HTML comment. No interactive audit prompt (nobody can answer it in a launchd run). The skill detects non-interactive context and switches to this mode.

## 7. The 30 patterns — adapted + annotated

All 30 carried in `references/ai-tells.md`. Each gets a tag:

### [pure slop] → always cut, both registers
Significance inflation (#1), notability name-dropping (#2), superficial -ing analyses (#3), promotional language (#4), vague/weasel attributions (#5), formulaic "challenges" sections (#6), AI-vocabulary words (#7), copula avoidance (#8), elegant variation / synonym cycling (#11), passive/subjectless fragments (#13), **em/en dashes (#14 — see §8)**, boldface overuse (#15), inline-header lists (#16), title case headings (#17), emojis (#18), curly quotes (#19), chatbot artifacts (#20), cutoff disclaimers / speculative gap-fill (#21), sycophancy (#22), filler phrases (#23), excessive hedging (#24), generic positive conclusions (#25), persuasive-authority tropes (#27), signposting (#28), fragmented headers (#29), diff-anchored writing (#30).

### [voice clash] → in voice-safe mode, defer to the named move and cite it
These are the patterns where upstream humanizer would gut Sean's craft. The crosswalk (`references/voice-safe-exceptions.md`):

| Tell | Sean's move it collides with | Voice-safe resolution |
|---|---|---|
| #1 Significance inflation | **Hard Cut / Deflation** | Keep the epic build *when* it lands on a mundane/absurd deflation in the final clause. Cut it when it inflates and never deflates. |
| #9 Negative parallelism / tailing negation | (none — but check) | Cut. Sean doesn't use "not just X, it's Y." Confirm in eval. |
| #10 Rule of three | **Rule of Three + Emotional Pivot** | Keep when items 1–2 are concrete/light and item 3 pivots to genuine feeling. Cut decorative triples that don't pivot. |
| #11 Synonym cycling | (none) | Cut — Sean repeats the clearest noun. |
| #12 False ranges | (none, but adjacent to metaphor stacking) | Cut "from X to Y" non-scales. Keep escalating metaphor stacks that describe the *same* thing (calibration-notes: ship of the damned → sheep → hamster wheel). |
| #26 Hyphenated word-pair overuse | (none) | Apply upstream rule (attributive keeps hyphen, predicate drops it). |
| Polysyndeton ("and…and…and") | **Beat Flow polysyndeton** | NOT a tell for Sean — protected. The drumbeat accumulation is a deliberate move. Flag only if it appears with zero rhythmic variation across a whole piece (Bad Kerouac). |
| Sensory cascade / pop-culture anchor | **Sensory Before Numbers, Pop Culture Anchoring** | Protected. The "one strong reference earns it, three is self-indulgence" rule (calibration-notes) is the *only* cap. |

**Also imported from humanizer and bound to Sean's existing anti-patterns:**
- **"Signs of human writing (preserve these)"** → maps onto Sean's signature moves + `calibration-notes.md` ("hyper-specific anecdote," "mixed feelings," "dated references," "variety in sentence length," "genuine asides"). The voice-safe scrub treats these as protected and will *not* flatten them.
- **"What NOT to flag (false positives)"** → carried verbatim-in-spirit so the skill doesn't gut legitimate prose (clusters of tells, not isolated ones).

## 8. Em dashes — hard universal rule (Sean's call)

Em/en dashes move into **[pure slop] → always cut, both registers**. Rationale: Sean received output that abused them (dashes all over the page) and prefers them gone from his voice entirely. Replacement order per humanizer §14: period (new sentence) › comma (tight aside) › colon (explanation) › parentheses (true aside) › restructure. Catch spaced ` — ` and double-hyphen ` -- ` too.

**Kerouac survives without the dash.** The retired mechanic is *only* "em dashes as breath marks." Everything else stays: polysyndeton, the jewel center, sensory cascading, dual narrator. Commas and periods carry the breath-mark rhythm instead. This is the single most important note for the voice-modes edit in §9.

Final-output guard: scan for `—` and `–`; any hit means the rewrite isn't finished.

## 9. writing-voice-modes reconciliation (full de-dash)

Because §8 makes dashes a hard cut, `writing-voice-modes` must stop *teaching* and *producing* them. Three edit layers:

### 9a. Instructions (SKILL.md prose)
- **Kerouac mode** — replace "**Dash rhythm:** Em dashes as breath marks between phrases" with comma/period-based breath guidance. Keep polysyndeton, jewel center, sensory cascading, dual narrator.
- **Thompson mode** — replace "Em dashes for urgent interruptions" in the typographic-notation line with commas / short sentences for interruption.
- Add a one-line cross-reference: *"No em dashes — `writing-humanity-pass` enforces this; use commas, periods, colons, or parentheses for the same rhythm."*
- Update any signature-move *mechanic* text that prescribes em dashes (e.g. Hard Cut / Deflation's "Long elevated clause → comma → deflation" already uses a comma — good; audit the rest).

### 9b. Examples (SKILL.md)
Rewrite every em-dash-bearing example so it reads naturally with comma/period/colon/parens. Known instances to fix (non-exhaustive — implementation does a full `—` sweep):
- Example 1 (IKEA / Zapier intro)
- Example 2 (Gonzo→Vonnegut post-mortem)
- Example 3 (Slack at 60%)
- The Signature Moves table examples
- The Professional Dial / Content-Type / Integration / Anti-Pattern tables

### 9c. Calibration anchors (voice-samples.md, ~43KB)
**Punctuation-substitution only — never alter Sean's actual words.** Swap each `—`/`–`/` -- ` for the contextually correct comma/period/colon/parens. Add a header note:

> _Note (2026-06-02): em dashes in these historical samples were normalized to commas/periods to match the no-dash standard enforced by `writing-humanity-pass`. Wording is unchanged._

**⚠ Sean-review flag:** these are real samples of how Sean actually writes. Editing them rewrites the calibration record. Alternative (if Sean prefers at review): leave the raw samples intact and only add the normalization note, so the anchors stay honest while the *standard* is documented. Default per the approved decision: edit them (punctuation only).

### 9d. Consistency check
After edits, grep both skills + references for `—`, `–`, ` -- `; zero hits outside this design doc and any intentional "before" examples in `ai-tells.md` that demonstrate the tell.

## 10. Integration rules

`writing-humanity-pass` sits downstream of composition:

- **With `writing-voice-modes`:** voice-modes composes → humanity-pass scrubs (voice-safe). The pass never overrides a signature move; it removes slop *around* the moves. The "do not flag" list IS the move list.
- **With `creative-writing` (format):** the pass operates within format constraints — it doesn't add/remove paragraphs to hit a structure; it cleans the prose inside the given shape.
- **With `technical-writing` (clarity):** for neutral scrubs, the pass and technical-writing agree (plain, front-loaded, no slop). No conflict.
- **Chaining order (recommended):** compose (voice-modes + creative-writing/technical-writing) → **humanity-pass last**. Document this in both skills' "Related Skills" sections.
- **substack-drafter:** already loads voice-modes verbatim. Plan notes (not implements this session) that the drafter should run humanity-pass in headless mode as its final step.

## 11. Evals

`evals.yaml` cases (before → expected-after), covering:
1. A voice-bearing draft with em dashes → dashes gone, voice intact, signature moves preserved.
2. A voice-bearing draft where AI added significance inflation + -ing padding around a real Sean move → slop cut, move kept.
3. A rule-of-three that pivots (keep) vs a decorative rule-of-three (cut).
4. A neutral runbook with chatbot artifacts + boldface + emojis + title case → full aggressive scrub.
5. A false-positive guard: clean human prose with one em dash and one "however" → minimal change, not gutted.
6. Polysyndeton + sensory cascade in voice text → preserved (not flagged as overuse).

`evals.sealed.yaml`: 2–3 held-out cases in the same shape.

## 12. Success criteria

- [ ] `writing-humanity-pass` exists with SKILL.md + references/ai-tells.md + references/voice-safe-exceptions.md + evals.
- [ ] Voice-safe scrub preserves all 13 signature moves; neutral scrub strips to plain register.
- [ ] Auto-detect routes essays→voice, docs→neutral, defaults to voice-safe when ambiguous.
- [ ] Em/en dashes are cut in both registers; final-output guard catches any survivors.
- [ ] All 30 patterns present and tagged [pure slop] or [voice clash]; every [voice clash] cites the colliding move.
- [ ] `writing-voice-modes` SKILL.md, examples, and voice-samples.md contain zero em dashes (outside intentional "before" demos).
- [ ] `grep -rn '—\|–' .claude/skills/writing-voice-modes .claude/skills/writing-humanity-pass` returns only intentional demo lines.
- [ ] CHANGELOG.md entry added; CLAUDE.md + README.md count tables / skill lists updated for the new skill.
- [ ] `python3 scripts/validate.py` passes.
- [ ] Headless mode returns clean text + one-line change comment, no interactive prompt.

## 13. Out of scope (this session)

- skill-optimizer convergence loop on either skill.
- Adding to export-groups / presets / installer manifests (capture as a doc-update task in the plan).
- Implementing the substack-drafter chain (note only; the drafter already loads voice-modes).
- Building any autonomous/scheduled wiring.

## 14. Attribution

`writing-humanity-pass` is adapted from `blader/humanizer` (MIT, v2.7.0), itself based on Wikipedia's "Signs of AI writing" (WikiProject AI Cleanup). Attribution + license note goes in the new skill's SKILL.md References section. MIT permits adaptation; retain the copyright/attribution.
