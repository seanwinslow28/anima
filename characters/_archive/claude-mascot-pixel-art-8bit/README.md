# Retired — claude-mascot, pixel-art-8bit register

**Retired 2026-05-30.** The pixel-art-8bit mascot failed on a *reference gap*: a
single flat anchor (`anchor.png`, one ¾ sprite) gave NB Pro nothing to infer
new angles from, so the turnaround plates invented a standing biped instead of
holding the round-lozenge sprite. See
`docs/anima-test-runs/2026-05-29-production-bake-and-gate-hardening.md` §6.

Superseded by the **pencil-test-colored** claude-mascot Bible (re-authored in
place at `characters/claude-mascot/` on 2026-05-30), which closes the reference
gap with a real five-view turnaround sheet (C-1) and lives in the same register
as sean-anchor — and is the actual Act 2 shoulder companion.

Kept as **register-vocabulary validation evidence**: the schema authored clean,
internally-consistent pixel-art rules (indexed palette, integer-pixel grid,
dither vocabulary). The failure was *generation* (reference gap), not *schema*.
The pixel-register cross-style validation is deferred to a future
16BitFit-humanoid pass (its own session) per
`docs/research/2026-05-30-nb2-editing-character-consistency-template.md`.

Restore point: this folder is the rollback target if the pencil pivot is reversed.
