# Session sidecar contract — `artdept-session.md`

The running memory of an Art Department session. One file, two blocks, hard
ownership. If the file can't be written (read-only context), hold the same
two-block discipline inline in the conversation. This is the front door's
`frontdoor-session.md` contract, retargeted for design.

## Shape

```markdown
# Art Department session — <slug> — <date>

## LOCKED DECISIONS   <!-- orchestrator-owned; APPEND-ONLY -->

- [L1] SPARK/BUNDLE: <input path — the front-door bundle dir, or the hand brief>
- [L2] BUDGET: <session credit ceiling Sean declared, e.g. "100 Higgsfield credits">
- [L3] design lock — <character>: <the ratified named-specific appearance, one line>
- [L4] register lock — <character>: <the locked style_register + why the winner won>
- [L5] chosen prompt recipe — <character/shot>: <the winning FRESH/EDIT recipe, named>
- [L6] <one line per resolved specific / world lock / scope call>
- ...
- [Ln] SUPERSEDES [Lk]: <new decision + why>   <!-- history is never edited -->

## PROPOSALS LOG   <!-- stage-appended; four content kinds only -->

### micro-expand
- observations: <the personality read per principal, in a line each>
- options: <3 divergent visual directions (silhouette/shape reads) + 3 candidate
  registers from pipeline/registers.py + the loaded-object question surfaced>
- recommendation: <Artie's grounded lean — which direction feels most alive>
- open_questions: <deepen these, or proceed to the grill?>

### interrogate
- observations: <what the grill established — the reference universe, the
  loaded object, palette/line discipline, the world's mood>
- options: <the named-specific candidates surfaced per answered question>
- recommendation: <the stated lean toward a specific>
- open_questions: <the still-generic answers the detector is still pushing on>

### look-test   <!-- ONE block per contested axis (register A/B; a design variant) -->
- observations: <why this axis is contested — the fork Sean can't call from prose>
- options: <the candidate prompts rendered (or emitted for Sean's Desktop-app pass),
  same-composition/different-register so it is apples-to-apples; each a named
  specific, with its credit cost announced against the running total>
- recommendation: <Artie's lean, one line — which look and why>
- open_questions: <register no-fit — surface the gap + the style-register
  authoring playbook pointer; never inline-author>

### expand-outward   <!-- ONE block per named secondary character / key location -->
- observations: <who/what is being designed, and which locked anchor it edits from>
- options: <the edit/composite candidates — reusing the hero anchors as refs,
  never crossing styles; extras captured as extras_guidance prose, not designs>
- recommendation: <the stated lean>
- open_questions: <a location or cast member whose look the room can't settle
  without a decision from Sean>

### synthesize
- open_questions: <only if a hole was found writing the bundle; otherwise empty>
```

## Rules

- **Only the orchestrator writes LOCKED DECISIONS**, and only after Sean
  decides. Locks are append-only: a change is a new `SUPERSEDES` entry, never
  an edit — the sidecar is the session's audit trail.
- **The five locked-entry kinds** are `spark/bundle`, `budget`, per-character
  `design lock`, per-character `register lock`, and `chosen prompt recipe`.
  Plus the ordinary world locks and scope calls. Every one is a named
  specific: "primal-sketch-grit, chosen over samurai-jack-s5 because the
  gritty ink over color carried the kid's face across the transformation (illustrative lock shape — GRANDMASTER's real register was left open by design)" is
  a lock; "we picked a register" is not.
- **Stages append only to their own PROPOSALS section**, and only the four
  kinds: `observations`, `options`, `recommendation`, `open_questions`. A
  stage that wants to decide something global (lock the register, skip a
  stage, individually design an extra) raises an `open_question` instead —
  the decision is Sean's, recorded by the orchestrator.
- **Budget is a locked entry, and spend is announced against it.** Every
  look-test render's cost lands in its `look-test` options block against the
  running total; a render that would cross `[L2]` stops and asks Sean.
- Every fact in the emitted bundle must trace to a locked entry. If SYNTHESIZE
  can't source a sentence here, the sentence doesn't ship.
