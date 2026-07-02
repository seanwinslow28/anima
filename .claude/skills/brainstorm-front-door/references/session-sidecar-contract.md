# Session sidecar contract — `frontdoor-session.md`

The running memory of a front-door session. One file, two blocks, hard
ownership. If the file can't be written, keep the same two-block discipline
inline in the conversation (the storytelling-skill sidecar rule).

## Shape

```markdown
# Front-door session — <slug> — <date>

## LOCKED DECISIONS   <!-- orchestrator-owned; APPEND-ONLY -->

- [L1] SPARK (verbatim): "<Sean's words, unedited>"
- [L2] premise: <the picked micro-expand premise, one line>
- [L3] tonal lean: <...>
- [L4] live risks: <the carried risk questions>
- [L5] single objective: <...>
- [L6] <one line per resolved North-Star point / character specific / non-negotiable>
- ...
- [Ln] SUPERSEDES [Lk]: <new decision + why>   <!-- history is never edited -->

## PROPOSALS LOG   <!-- stage-appended; four content kinds only -->

### micro-expand
- observations: ...
- options: <3 premises / 3 routes / 3 risks>
- recommendation: <the stated lean>
- open_questions: ...

### interrogate
- observations: ...
- options: ...
- recommendation: ...
- open_questions: ...

### synthesize
- open_questions: <only if a hole was found; otherwise empty>
```

## Rules

- **Only the orchestrator writes LOCKED DECISIONS**, and only after Sean
  decides. Locks are append-only: a change is a new `SUPERSEDES` entry, never
  an edit — the sidecar is the session's audit trail.
- **Stages append only to their own PROPOSALS section**, and only the four
  kinds: `observations`, `options`, `recommendation`, `open_questions`. A
  stage that wants to decide something global (choose the style, skip a
  stage, rewrite the premise) raises an `open_question` instead.
- **Locks are written as named specifics.** "The grandmother's faded
  headband, too big until the return" is a lock; "a meaningful object" is a
  proposal that hasn't finished cooking.
- Every fact in the emitted bundle must trace to a locked entry. If
  SYNTHESIZE can't source a sentence here, the sentence doesn't ship.
