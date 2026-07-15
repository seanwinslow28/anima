# Good-look-test rubric — the six-criterion live-review checklist

**This is a live human-review checklist for Sean — not a CI gate, not a
prose-grep, not a self-assessment. A model cannot self-pass it.** Every
criterion is a taste judgment; the honesty of this instrument is that it stays
in human hands. (The art-viz red-team lesson: any single automatable bar is
gameable — a "≥3 route bullets naming the register" lint passes a flat look-test
and fails a superb one phrased differently.) The code seam
(`python -m pipeline.artdept validate`) checks *structure only*; this rubric is
where *quality* is judged, by Sean, against the captured session.

The worked positives throughout are the GRANDMASTER sprint's live look-tests:
the **kid two-state** test (wimpy ↔ trained, glasses↔headband) and the **grandma
two-look** test (warm old keepsake photo ↔ 1970s kung-fu-heroine reveal,
unmistakably one woman).

## The six criteria

A good Art Department session exhibits **all six**:

### 1. Contested forks rendered apples-to-apples
Every contested fork is shown as **same-composition, different-register (or
different-design)** comparisons — the look varies, the frame does not, so it is
a true look-to-look read.
- **Worked positive:** the register A/B fork rendered the *same* grandma-and-boy
  keepsake photo in both primal-cartoon and samurai-jack — one composition, two
  rendering languages, a clean comparison.
- **Anti-example:** two "Genndy-ish" candidates that also change the pose and
  crop — nothing to compare, and the difference you see might be composition,
  not register.

### 2. Identity survives the fork — the sprint's craft finding #1
The character is **recognizably itself across every look** — across-edit
identity holds when a master anchor is edited into a re-posed / re-costumed /
re-registered variant.
- **Worked positive:** the kid's face held from wimpy anchor → trained edit
  (headband on, glasses off, sterner brow) — same boy, new attitude; the grandma
  aged as one face across the old photo and the young-warrior reveal.
- **Anti-example:** the trained kid comes back with a subtly different face — the
  edit drifted identity, and the "transformation" is really two different boys.

### 3. Every lock is a named specific Sean chose, recorded with why the winner won
No lock is a category. Each is a named specific, in the sidecar, with the reason
it beat the alternative.
- **Worked positive:** "[L4] register lock — kid: primal-sketch-grit, chosen
  over samurai-jack-s5 because the gritty ink-over-color carried his face across
  the transformation." "Pale skin, messy brown hair, thick square too-big
  glasses, chunky worn sneakers."
- **Anti-example:** "[L4] register: primal (looked good)" — no named specific,
  no why, nothing Cy or a future session can reproduce.

**Criteria 1, 2, and 3 block together.** A single bar is gameable — a look-test
can be apples-to-apples (1) yet quietly drift identity (2), or hold identity yet
lock nothing specific (3). The block requires all three: fair comparison **and**
identity survives the fork **and** the lock is a recorded named specific. Still
Sean's live judgment, never a lint. Criteria 4–6 are findings to fold, at Sean's
call.

### 4. The prompt pack reproduces the locked look
The pack Sean takes to ChatGPT actually regenerates the ratified look —
fresh-vs-edit economy respected (FRESH = full + named style + anti-render;
EDIT = terse, reference-carried, style-silent), the dependency map present
(edits edit the anchor they made, never crossing styles), and the batches
checkpointed.
- **Worked positive:** the GRANDMASTER pack — 5 fresh × 2 styles + 5
  style-agnostic edits/composites, with the ChatGPT orchestration prompt
  encoding the dependency map and checkpointing each batch.
- **Anti-example:** a pack of ten verbose fresh prompts that re-describe the
  character every time — identity drifts across the batch, the dependency map is
  absent.

### 5. Scope line held
No individually-designed extras. Every principal + named/recurring character has
a designed anchor; anonymous extras + set-dressing are covered by
`extras_guidance` prose; the world is key locations + `environment-style.md`,
not every backdrop.
- **Worked positive:** the fixture's `extras_guidance` ("background kids aged
  eight to ten, varied heights, one or two in paper party hats — never
  individually designed") covers the party crowd through the prompt pack.
- **Anti-example:** three bespoke background-kid designs baked as anchors — scope
  blown, effort spent where the register + pack should carry it.

### 6. Register no-fit surfaced to the playbook, never inline-authored
When nothing in the closed vocabulary fits, the gap is surfaced with the
style-register authoring playbook pointer as a called dependency — the room
never writes a new register.
- **Worked positive:** GRANDMASTER's Tartakovsky-flat gap surfaced to the
  playbook and gated the Bible pass until the register was authored properly.
- **Anti-example:** a candidate prompt quietly invents a bespoke "gritty-flat"
  style with no register behind it — inline authoring, doctrine violated.

## Live validation protocol — Checkpoint 3

Built to structural-green plus this protocol; **Sean runs the live session and
renders.** The capture is his — a copied fixture cannot stand in for it.

1. **Pick a piece with a live look question** — GRANDMASTER's undesigned
   host-dad, or the next greenlit piece.
2. **Run the chain:** orchestrator → micro-expand → INTERROGATE → LOOK-TEST
   forks → lock → EXPAND-OUTWARD → SYNTHESIZE → validate. Sean declares the
   credit budget first; spend is announced against it and hard-stops at the
   ceiling.
3. **Capture the artifacts:** the sidecar's `look-test` / `expand-outward`
   proposal blocks, the LOCKED DECISIONS (design + register + recipe locks),
   `stage_provenance`, and the emitted bundle.
4. **Score against the six criteria above** — all six judged, by Sean, against
   the captured session, never against the model's account of itself.
5. **Blocking rule:** a miss on the criteria 1+2+3 block blocks the session;
   misses on 4–6 are findings to fold, at Sean's call.
