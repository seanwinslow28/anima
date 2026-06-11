# Studio Brief — "The Spark, Shared"

The first integrated end-to-end fleet run: a small two-character pencil-test loop,
planned by Maya, generated through Flo, critiqued by Em + the T3 council, assembled,
and captured to the museum. The piece is the proof; the run is the point.

## What is this story about?

Sean at his desk, stylus in his right hand, mid-draw. The Claude mascot is perched on
his shoulder, idle. Sean draws something on the page; the mascot notices, perks up, and
reacts with a small, genuine delight — then settles, and the loop returns to the start.
A five-keyframe micro-loop, no dialogue. The smallest possible expression of anima's
premise: **the human makes the mark; the companion responds.**

The beat, in five (intent, not the shot list — Maya formalizes that in the Production brief):

1. **Establishing two-shot** — Sean ¾ view at the desk, stylus to paper; mascot perched on his shoulder, neutral/idle. Sets the look, framing, and scale. The compositional anchor every other frame chains from.
2. **The draw** — Sean's hand moves on the page; the mascot turns to *look* at what he's making.
3. **The notice** — the mascot perks up (alert-perk) — the spark of catching the idea.
4. **The delight** — the mascot reacts with delight to the drawing; Sean stays on the work.
5. **The settle** — the mascot eases back toward perched/idle, Sean's hand returns to the start position → loops cleanly back to frame 1.

## Who is the character?

Two characters, both already authored as locked Character Bibles in the
`pencil-test-colored` register:

- **Sean** — `characters/sean-anchor/` (the pencil-test reference identity). The maker. Stylus in right hand; relaxed, focused at his desk.
- **Claude mascot** — `characters/claude-mascot/` (the terracotta box-creature). The companion. Perched on Sean's shoulder; its motion vocabulary (`idle`, `look`, `alert-perk`, `delight`) carries the whole arc.

Scale and placement follow the canonical A-7 pairing reference,
`characters/claude-mascot/source-refs/sean-with-claude-mascot.png`.

## What is the tone?

Warm, companionable, a quiet spark. The delight is small and real — a beat, not a gag.
Sean stays absorbed in the work throughout; the *mascot* carries the reaction. The
emotional center is the moment of being-noticed, not a punchline.

### What this is NOT

- Not Sean reacting — he keeps making; the human owns the work, the companion responds to it.
- Not cute-for-cute's-sake — the mascot's delight is earned by the drawing, not mugging at the camera.
- Not pencil-test glossy — graphite-rough, cream paper, hand-drawn. Never a clean digital/3D render.
- Not two separate shots — one continuous two-shot that loops.
- Not a morph — Sean and the mascot stay two distinct identities the whole way through.

## What is the format?

A five-keyframe loop, on twos — a short browser GIF/WebM micro-loop. One continuous
two-shot, no act break. The loop must return cleanly (frame 5 → frame 1).

## What is the target medium?

A museum walkthrough exhibit — the first artifact produced by a full integrated fleet
run — and, downstream, the portfolio. Browser GIF/WebM loop.

## What is the deadline?

No hard external deadline. This is the first integrated end-to-end run; the soft target
is this week. The goal is to exercise the whole fleet on one small piece and produce a
shippable loop + a museum walkthrough as the proof.

## What are the non-negotiables?

- Sean's stylus stays in his **right hand**, present in every frame (CC01/CC02).
- **No identity morphing** — Sean stays Sean and the mascot stays the mascot across all five frames. This is the two-character consistency bar the run exists to test; it's the exact failure mode (face-drift through a sequence) Flo-B caught in the fal models.
- The mascot holds its **terracotta box-creature form + palette** — no drift to a different creature or color.
- The mascot stays **perched on Sean's shoulder** at consistent scale/placement (per the A-7 pairing).
- **Cream paper texture + warm graphite line** across all five frames (the `pencil-test-colored` register; HF02/SF01/SF04).
- **16:9** within 2% tolerance, every frame (HF01).
- **Clean loop** — frame 5 returns to frame 1's pose so the cycle reads continuous.
- **All frames generated at standard tier (NB2).** The establishing frame is the compositional anchor (Act-1-style frame chaining), not an NB Pro hero. NB2 throughout — chosen for reliability.
