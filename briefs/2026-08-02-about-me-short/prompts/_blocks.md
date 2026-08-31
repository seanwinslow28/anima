# Shared prompt blocks — Movement 1

Two blocks go into every plate prompt **verbatim**. Do not edit them per shot
(FIRST LICKS DR #41: the look lives in post; every plate generates CLEAN).

## PALETTE — from `environment-style.md`, binding

Warm cream drawing paper throughout, a pale putty cream, never white and never yellow. The floor is the same cream a half-step darker. Walls and floor are flat, quiet, and low-contrast — the room is a pale ground, and colour lives only on the characters and on small props. Graphite line and cross-hatch shadow carry all the form. Overall value stays high-key and even: no dark corners, no pooled shadow, no colour cast, no vignette, no dramatic lighting.

## REGISTER — style token + anti-render clause

Hand-drawn animation pencil test: graphite line, visible construction lines, cross-hatch shadow, light coloured-pencil wash on props only, paper tooth showing — no flat vector fill, no digital gradients, no painterly rendering, no photographic lighting, no 3D.

## REF ROLES — the re-angle reconstruction pattern

These corner plates are **re-angles of one designed set**, not edits, and `gpt_image_2`
will not re-camera from an edit instruction. Every plate therefore role-splits two refs:

- **Image 1 = `probe-205/U-codex-corner.png`** — the ratified S04 plate, used as the
  world / style / fixture bible. Matching plate-to-plate beats matching both to a third
  image, and S04 is the only corner proven end to end.
- **Image 2 = `m1-guides/M1-S0X-…-plate-rough.png`** — the character-free, guide-mark-free
  composition rough for this camera.

---

## Session log — 2026-08-30, 21:29 → 21:52

| Prompt file | Model | Refs | Result |
|---|---|---|---|
| `S03-claude-nook-plate.txt` | gpt_image_2 2k high | S04 bible + S03 plate-rough | `plates/S03-claude-nook-v2.png` |
| `S05-gemini-moodboard-plate.txt` | gpt_image_2 2k high | S04 bible + S05 plate-rough | `plates/S05-gemini-moodboard-v1.png` |
| `S06-grok-dartboard-plate.txt` | gpt_image_2 2k high | S04 bible + S06 plate-rough | `plates/S06-grok-dartboard-v1.png` |
| `S07-alarm-plate.txt` | gpt_image_2 2k high | S04 bible + S07 plate-rough | `plates/S07-alarm-v1.png` |
| `S03-claude-composite.txt` | gpt_image_2 edit | `refs/char-claude.png` + plate | composite v1, phase-corr 0.52 |
| `S05-gemini-composite.txt` | gpt_image_2 edit | `refs/char-gemini.png` + plate | v1 / v2 / v3 — v3 is the lean |
| `S06-grok-composite.txt` | gpt_image_2 edit | `refs/char-grok.png` + plate | composite v1, phase-corr 0.47 |
| `S07-alarm-off.txt` | gpt_image_2 edit | S07 alarm plate | screen-dark keyframe, phase-corr 0.47 |

**Single-character refs beat the lineup.** `refs/char-{claude,gemini,grok}.png` are crops of
`cast-scale-lineup.png`, upscaled 3×. Handing the composite a five-character lineup invites the
Codex/Gemini colour-family confusion that corrupted four July generations; one character per ref
removes the question.

**NSFW refusal, recorded so it is not rediscovered.** The first S06 composite prompt —
"grey gremlin shape, bat ears, red eyes, fanged grin", "arm cocked back mid-throw" — came back
`status: nsfw` with no image. Same character and same action described as "a round grey cartoon
creature with big pointed ears, a wide friendly cartoon grin", "one arm drawn back holding a small
dart, cheerful and mid-play" passed first time. The saved file carries the wording that works.

**Verification method for every edit:** FFT phase correlation + edge-diff ratio against the source
plate, per `environment-style.md`. All four edits landed **0.47–0.58**, at or above the 0.42 that
ruled the GPT edit path in over NB2's 0.077. Frame-delta means stay retired.
