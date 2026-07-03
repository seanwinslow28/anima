---
name: writing-humanity-pass
description: Remove the documented "Signs of AI writing" from a draft and rebuild human texture, calibrated to Sean's voice. Auto-detects voice-bearing vs neutral text and scrubs accordingly. Cuts em dashes, significance inflation, -ing padding, copula avoidance, chatbot artifacts, filler, hedging, and 24 more tells. Pairs with writing-voice-modes (runs as the final pass after a voice write) and runs standalone. Use when asked to "scrub the AI out of this", "make this less AI", "de-slop this draft", "humanize this", "this sounds like AI", "remove AI tells", or when reviewing any draft (yours or agent-generated) that reads like a machine.
---

# Writing Humanity Pass

## Purpose

Remove the 30 documented "Signs of AI writing" from a draft and rebuild human texture, calibrated to Sean Winslow's voice. This is an editing pass, not a composition skill. It pairs with `writing-voice-modes` (runs as the final pass after a voice write) and runs standalone for cleaning agent-generated or foreign drafts.

The core rule: Sean's voice is the authority. A pattern is only a tell when it is NOT one of his 13 signature moves. The "do-not-flag" allowlist IS the signature-move list in `writing-voice-modes`.

## When to Use

- "Scrub the AI out of this", "make this less AI", "de-slop", "humanize this", "this reads like AI", "remove AI tells"
- As the final editing pass after composing in `writing-voice-modes`
- Cleaning agent-generated drafts (substack-drafter, vault agents) before publishing
- Cleaning neutral docs, specs, or reference notes that read like a machine

## How It Works: Detect Register, Then Scrub

### Step 1. Classify the text

- Voice-bearing (essay, blog, newsletter, LinkedIn, social, post-mortem, personal writing): VOICE-SAFE SCRUB.
- Neutral (docs, specs, runbooks, PRDs, reference notes, API docs, agent-generated reference output): FULL SCRUB.

Classification signals, in priority order:
1. Explicit user cue ("this is a blog post" / "this is a runbook" / "neutral scrub").
2. File path / content type (essays and substack drafts route to voice; `docs/`, `*.spec.md`, runbooks, READMEs route to neutral).
3. Internal signal: first-person + narrative + sensory detail routes to voice; third-person + procedural + reference routes to neutral.
4. Ambiguous routes to VOICE-SAFE (the safer failure: it preserves more, scrubs less).

### Step 2. The scrub loop (both registers)

1. Draft rewrite. Apply `references/ai-tells.md` for the chosen register. Cover everything the original covered (N paragraphs in, N paragraphs out). Preserve meaning.
2. Audit. Ask explicitly: "What makes this still read as AI-generated?" Answer in brief bullets (remaining tells, too-tidy rhythm, slogan-y closer).
3. Final rewrite. Fix the audit bullets. Scan the result for `—`, `–`, and ` -- `; any hit means it is not done.

### Step 3. Deliver

- Interactive: draft, then brief "still-AI" bullets, then final rewrite, then a short change summary.
- Headless / agent chain (e.g. substack-drafter): return final clean text plus a one-line change summary in a trailing HTML comment. No interactive audit prompt (nobody can answer it in a launchd run). Detect non-interactive context and switch to this mode.

## VOICE-SAFE vs FULL: The Difference

VOICE-SAFE. Cut the `[SLOP]` tells; DEFER to Sean's 13 signature moves (see `references/voice-safe-exceptions.md`). Never flatten a deliberate move into "clean" prose. Match Sean's codified voice from `writing-voice-modes` references instead of producing generic clean output. No sample-pasting needed; his calibration is already codified.

FULL. Plain, neutral register IS the correct human voice here. Cut everything in `references/ai-tells.md`. Add NO personality and NO first person. (This mirrors humanizer's own gating: encyclopedic, technical, or reference text wants neutral-and-plain, not injected voice.)

## The Em-Dash Hard Rule (Both Registers)

No em dashes (`—`), en dashes (`–`), spaced ` — `, or double-hyphen ` -- ` in the final output. This is a hard constraint, not a "use sparingly" preference. The em dash is the single most reliable AI tell, and Sean has chosen to retire it from his voice entirely. Replace each, in order of preference: period (new sentence), then comma (tight aside), then colon (introducing an explanation), then parentheses (a true aside), then restructure.

Kerouac survives without it: polysyndeton, the jewel center, sensory cascading, and the dual narrator all stay. Commas and periods carry the breath-mark rhythm that the dash used to. The only retired mechanic is "em dashes as breath marks."

Final-output guard: scan the result for `—` and `–`. Any hit means the rewrite is not finished.

## What NOT to Flag (Don't Gut Real Prose)

A clean human writer can hit several patterns without any AI involvement. These are NOT reliable tells on their own:
- Perfect grammar and consistent style (polish is not AI).
- Mixed casual and formal registers (often a technical person, a young writer, or neurodivergent prose).
- "Bland" prose without the specific tells (generic dryness is just dry writing).
- Formal or academic vocabulary that is not the specific AI-vocabulary words in #7.
- Common transition words in isolation (one "however" is not a tell).
- Curly quotes alone (most editors auto-curl).
- Unsourced claims (most of the web is unsourced).

Look for clusters of tells, not isolated ones. A single em dash is nothing; em dashes plus rule-of-three plus "vibrant tapestry" plus a "Conclusion" section is a confession.

## Signs of Human Writing (Preserve These)

When you see these, lean toward leaving the prose alone. Over-editing destroys what makes it human. For Sean specifically, these map onto his signature moves and `calibration-notes.md`:
- Hyper-specific, hard-to-fabricate detail (a named place, a named substance, "the lawyer upstairs from my dentist").
- Mixed feelings and unresolved tension.
- Dated, era-bound references (slang, memes, music).
- Variety in sentence length (short staccato hits between flowing lines).
- Genuine asides, parentheticals, and self-corrections (his Reader-Dismissal move).
- His Rule-of-Three-plus-pivot, Hard-Cut deflation, sensory-before-numbers, and pop-culture anchoring, all deliberate (see `references/voice-safe-exceptions.md`).

## Integration

This skill runs LAST in the chain. The full Substack pipeline:

```
storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass
   (beat SHAPE + order)       (value GATE + payoff)    (every SENTENCE)      (RED-TEAM, advisory)  (scrub + no em dash)
```

`storytelling-architecture` and `substack-value-engine` shape a beat map (story + value, no prose); `writing-voice-modes` composes every sentence; this skill scrubs.

- Chaining order: shape with `storytelling-architecture` + `substack-value-engine`, compose with `writing-voice-modes` (plus `creative-writing` for format, `technical-writing` for clarity), red-team with `writing-critique` (advisory; one grounded revise pass max), then run `writing-humanity-pass` LAST.
- This skill is where two upstream story mechanics get their punctuation enforced: a slippery-slide "forward-pull" line and a parenthetical particular both gravitate toward the em dash by default. The engagement pass leaves the *function*; this pass realizes it without the dash (period-fragment, colon, restructure). Never assume the dash away upstream; clean it up here.
- It never overrides a format constraint (`creative-writing`), a signature move (`writing-voice-modes`), or a story beat (`storytelling-architecture`).
- For neutral text it agrees with `technical-writing` (plain, front-loaded, no slop).

## References

- `references/ai-tells.md`: all 30 patterns, adapted to Sean's output, each tagged `[SLOP]` (always cut) or `[CLASH->move]` (defer in voice-safe). Its "Evidence quality" section stratifies the catalog by how well each tell is supported, and wires the measurable, baseline-relative signals (sentence-length burstiness, MATTR, pronoun rate) to the `writing-critique` analyzer (`.claude/skills/writing-critique/references/analyze.py` + `baseline.json`).
- `references/voice-safe-exceptions.md`: the crosswalk. Each `[CLASH]` tell maps to the signature move it collides with and how voice-safe resolves it.

Adapted from [`blader/humanizer`](https://github.com/blader/humanizer) (MIT, v2.7.0), itself based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup). MIT permits adaptation; attribution retained.

## Success Criteria

- [ ] Output contains zero em/en dashes (both registers).
- [ ] Voice-safe scrub preserves every signature move; neutral scrub strips to plain register.
- [ ] Meaning preserved; paragraph count matches the original.
- [ ] No tell from `ai-tells.md` survives that is not a protected Sean move.
- [ ] Real human prose (no clusters of tells) is left largely alone, not gutted.

## Copy/Paste Ready

```
"Scrub the AI out of this"
"Make this less AI"
"De-slop this draft"
"Humanize this, it's a blog post"
"Neutral scrub this runbook"
"Run the humanity pass after writing it in my voice"
```
