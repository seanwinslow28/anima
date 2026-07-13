# Signature style taste profile + the blend brainstorm

**Date:** 2026-07-13 · **Workstream:** the outward turn — style-register expansion (the active thread; see [ROADMAP](../../ROADMAP.md) "Current focus"). · **Status:** **SPIKE COMPLETE — WINNER LOCKED. The FUSION concept ("flat cartoon cast on a hand-painted gritty world") is the next register to author** (see §6). Gritty Storybook (GS1/GS2) banked for a later research pass; Collage Real explored-not-chosen; Riso banked. · **Method:** a one-question-at-a-time taste brainstorm (superpowers:brainstorming) → a costed 2-round Higgsfield image spike + a Seedance motion test, Sean's eye the sole arbiter. · **Next:** the FUSION register enters the [style-register authoring playbook](../architecture/style-register-authoring-playbook.md) via the [kickoff prompt](2026-07-13-fusion-register-authoring-kickoff.md) (a fresh session runs Step R → S → B). The taste brainstorm is **not exhausted** — see §7 for the un-explored lanes to revisit.

---

## 1. The taste profile (Sean's fingerprint — derived, not assumed)

Across five rounds of reactions, a coherent aesthetic emerged. Sean's registers already encode part of it (`pencil-test`, `primal-sketch-grit`, `samurai-jack-s5`, `90s-nicktoon-grossout`); the brainstorm surfaced the rest. **What he grabbed** (✓) **and passed** (✗) is equally diagnostic.

**The four through-lines:**
1. **Mixed-media / collage** — things that don't belong on one screen together; cartoon-on-real; different media coexisting. *(Courage mixed-media horror ✓, Amazing World of Gumball, Adult Swim experimental, cutout/paper collage ✓, "blend into something our own.")*
2. **A living hand-made line** — imperfection that moves and breathes: the boil, the jitter, misregistration, the visible mark. *(Ed Edd n Eddy 'boil' ✓, risograph ✓, charcoal/woodcut ✓.)*
3. **Warm, grounded, textured** — muted-earthy, urban, folk, hand-crafted; **never cold, gothic, or glossy.** *(Hey Arnold urban-geometric ✓, Cartoon Saloon folk-decorative ✓, Craig of the Creek, Moon Girl.)*
4. **Bold flat graphic design underneath.** *(UPA / mid-century flat ✓, Moon Girl and Devil Dinosaur, samurai-jack-s5.)*

**What he passed on (the negative space of the taste):** anime lanes ✗, comic/graphic-novel ink ✗, golden-age rubber-hose bounce ✗, stop-motion dimensionality ✗, Invader Zim cold-gothic ✗. → **Not** slick, not cold, not vintage-bouncy, not dimensional-physical, not Japanese-idiom. The taste is **hand-made Western 2D with real texture and a mixed-media instinct.**

---

## 2. The banked roster (six candidates from the exploration)

Not authored — banked for the backlog, each with a craft line + a transport estimate (per the playbook's ladder) + a neighbor-collision flag. Pull one through the playbook when a project (or a spike) calls for it.

| # | Candidate | Craft one-liner | Transport estimate | Neighbor flag |
|---|---|---|---|---|
| 1 | **Cartoon Saloon folk-decorative** | Flat ornamental layered shapes, folk-pattern, warm storybook palette | NB2 likely (flat-designed) | none — fully distinct |
| 2 | **Risograph / screenprint** | Limited spot inks, misregistration, halftone, overprint, paper grain | NB2 spike → gpt-image if grain fails | none — nearly a texture-over-any-style |
| 3 | **UPA / mid-century flat** | Geometric icon-reduction, bright, playful, limited palette | NB2 likely | **close to `samurai-jack-s5`** — needs the bright/decorative-vs-cinematic negative control |
| 4 | **Gorillaz / Tank Girl grunge-ink** | Heavy confident ink, splattered texture, dirty-saturated color, urban-punk | gpt-image likely (grit, like Primal) | **close to `primal-sketch-grit`** — flatter/cleaner-lined/graphic-punk distinguishes it |
| 5 | **Cutout / paper collage** | Flat paper shapes, torn/scissor edges, layered, slight drop-shadow | gpt-image likely (edge realism) | none |
| 6 | **Charcoal / woodcut / ink-wash** | Smudged charcoal OR carved-black woodcut OR sumi-e brush-wash (pick one) | gpt-image likely (expressive marks) | none — but must disambiguate which medium |

---

## 3. The three signature-blend concepts (the "unique and our own" goal)

Rather than only banking existing looks, the brainstorm converged on **blending Sean's ingredients into a signature anima register** — something no single show fully is. Three directions, each pulling a different subset of the taste profile. **These are what the spike tests.**

### Concept A — "The Collage Real" *(the recommendation)*
Flat, boiling-line cartoon characters composited onto **textured real / painted** worlds; the character reads as obviously *drawn and flat* while the world behind is *real and dimensional*; unified by a warm muted grade + faint halftone print grain. The friction between the drawn figure and the real world is the point. Pulls through-lines **1 + 2 + 3**.
- **Why recommended:** it's the strongest expression of Sean's #1 thread (mixed-media), it's the most "uniquely ours" / hardest to copy, and **it reuses the compositing doctrine Sean already built** ([`docs/research/2026-07-12-compositing-doctrine.md`](../research/2026-07-12-compositing-doctrine.md) — NB2 composites a drawn character onto a scene, holds identity, relights).
- **Honest scope note:** this is really *a drawn-character register + a compositing recipe*, not a single `RegisterSpec`. May be a register plus a staging convention (Bea/Flo).

### Concept B — "Riso Cartoon"
Bold flat graphic characters (Moon-Girl / UPA punch) rendered as a **risograph screen-print**: 2–3 flat spot inks, halftone, deliberate misregistration, overprint-multiply, a boil on the line, cream paper grain. A printed-object aesthetic — maximally anti-slick. Pulls through-lines **2 + 4**.
- **Cleanest single-RegisterSpec** of the three (no compositing recipe); transport risk is the print grain (NB2 spike first, gpt-image fallback).

### Concept C — "Hand-Made Urban Storybook"
Hey-Arnold geometric character shapes + Cartoon-Saloon folk-decoration + Craig-of-the-Creek warmth: bold character geometry, muted earthy palette, cross-hatched dry-brush hand-textured backgrounds, folk-pattern flourishes, soft gouache washes. Grounded, gentle, tactile. Pulls through-lines **3 + 4**.
- The warmest / most coherent single look; NB2-plausible.

---

## 4. The spike plan (Sean-gated: review prompts → then run)

A **pre-spike** look-test to choose the concept *before* committing it to the full playbook. Informal — Sean's eye picks the direction; the winner then gets Step R (research) + Step S (formal hero lock) + Step B (authoring).

- **Engines (CLI-confirmed live 2026-07-13, `higgsfield` v0.2.3):** `gpt_image_2` ("GPT Image 2" — supports 16:9 + up to 4k + reference `medias`; the exact model anima's registers pin to, `GPT_IMAGE`) + NB2 (`nano_banana_flash` = the CLI's "Nano Banana 2"). gpt-image for the print/photo/composite recipes; NB2 for the flat-cartoon + compositing (per Sean's ART-VIZ doctrine, [`docs/research/2026-07-12-prompt-ladder-harness.md`](../research/2026-07-12-prompt-ladder-harness.md) + [`docs/architecture/prompt-decision-card.md`](../architecture/prompt-decision-card.md)). **Not** `openai_hazel` (the CLI's other OpenAI image model): it lacks 16:9 (only 1:1/3:2/2:3/auto) and isn't the pipeline's pinned model.
- **Constant subject + scene across all three concepts** (so the spike varies *style*, not art direction — the Step-S discipline). An **original, genericized** character + world (no franchise character or setting — the neutrality doctrine applies to spike prompts too):
  > *An original 11-year-old character: round cheeks, a gap-toothed grin, a mop of curly hair under a knit beanie, an oversized striped hoodie, a canvas backpack. A scruffy one-eared orange stray cat at their feet. Standing on the cracked stoop of a weathered corner-store brownstone at golden hour; a hand-painted shop sign, tangled telephone wires overhead. Medium-wide, 16:9.*
- **Genericization:** the prompts describe the **look by attributes only** — no "Gumball / Courage / Hey Arnold / Cartoon Saloon / Adult Swim / risograph-brand" show or studio names. (Same rule every register prompt follows.)
- **Process:** ~2–3 iterations per concept per engine; Sean reviews the contact sheet by eye; picks the concept(s) he's drawn to; costs tracked per the [Higgsfield runbook](../anima-test-runs/2026-06-22-higgsfield-seedance-generation-runbook.md) (subscription credits, ~soft cap to confirm with Sean).

### Draft spike prompts (for Sean's review — DO NOT run until approved)

**Concept A — The Collage Real**
- *gpt_image:* `Flat, boldly hand-drawn 2D cartoon character with a thick wobbling boiling hand-inked outline and simple flat cel colors — deliberately NO rendered volume, NO airbrushed shading on the figure — composited onto a fully PHOTOGRAPHIC, real-textured background: a real weathered brownstone corner-store stoop at golden hour, real cracked concrete, real tangled telephone wires. The character reads as obviously flat and drawn; the world behind is real and dimensional. Unify the whole frame with a warm muted color grade and a faint halftone print grain. [constant subject/scene]. 16:9.`
- *NB2 (compositing form):* feed the drawn character ref + a photographic stoop background; `Composite the flat cartoon character onto the photographic stoop, keep the character flat and hand-drawn with a boiling outline, relight it into the golden-hour scene, warm muted grade, faint print grain. Keep the photo background unchanged.`

**Concept B — Riso Cartoon**
- *gpt_image:* `The entire image rendered as a risograph screen-print: a limited palette of exactly three flat spot inks (warm vermilion, teal-blue, near-black), bold flat graphic cartoon shapes, a boiling hand-inked outline, visible halftone dot texture, DELIBERATE misregistration where the ink layers sit slightly offset, overprint-multiply where two inks overlap into a darker third color, printed on cream uncoated paper with visible paper grain. NO gradients, NO rendered volume, NO photographic realism. [constant subject/scene]. 16:9.`
- *NB2:* `Render as a 3-ink risograph print: flat spot inks, halftone dots, slight misregistration, overprint where colors overlap, boiling ink outline, cream paper grain, bold flat cartoon shapes. No gradients, no rendered volume. [constant subject/scene]. 16:9.`

**Concept C — Hand-Made Urban Storybook**
- *gpt_image:* `A warm hand-made storybook illustration: bold geometric cartoon character shape-design, a muted earthy palette (ochre, brick-red, sage, cream), cross-hatched and dry-brush hand-textured backgrounds, folk-decorative pattern flourishes worked into the environment, soft gouache washes, visible pencil-and-ink construction lines. Grounded, gentle, tactile, warm. NO glossy digital rendering, NO photographic realism, NO anime. [constant subject/scene]. 16:9.`
- *NB2:* `Warm hand-made storybook illustration: bold geometric character shapes, muted earthy palette (ochre, brick, sage, cream), cross-hatched dry-brush textured background, folk-pattern flourishes, soft gouache washes, visible construction lines. Grounded and tactile, no glossy rendering. [constant subject/scene]. 16:9.`

*(`[constant subject/scene]` = the italic subject paragraph above, pasted in full. Write each prompt to a file per the Higgsfield runbook; zsh `setopt shwordsplit` gotcha applies.)*

---

## 5. What this feeds

- **Winner → the playbook.** Whichever concept(s) Sean is drawn to enters Step R (deep research grounds the craft), Step S (formal cross-engine hero lock), Step B (the $0 TDD authoring drill). A blend concept may resolve into a `RegisterSpec` + a compositing convention (Concept A) rather than one spec — decided at Step R.
- **The other five banked candidates** stay in the [register backlog](2026-07-04-register-backlog-and-transport-findings.md) §6, pulled one at a time on Sean's greenlight with a named consumer (the anti-drift rule).
- **No register is authored from this brainstorm alone** — the taste is chosen; the craft still gets researched and the look still gets ratified by Sean's eye before any `RegisterSpec` lands.

---

## 6. Spike results + the decision (2026-07-13, Sean's eye)

The spike ran in the Higgsfield CLI (`gpt_image_2` + `nano_banana_flash`; Seedance 2.0 for motion). Sean's eye was the sole arbiter at every gate. Artifacts (gitignored, local): `runs/2026-07-13-signature-blend-spike/` — round-1 contact sheet, `round2/` (the AI-guru scene), `round2/seedance/` (motion). **~116 credits total** (round 1 = 27, round 2 = 37, Seedance = 52.5).

- **Round 1 (generic kid-on-a-stoop, 3 concepts × 2 engines, 27 cr):** Sean kept **Collage Real** + **Gritty Storybook**; **Riso Cartoon** was cool but "feels more like a Nike ad / music video — doesn't belong in any stories I'd tell right now" → **banked, not killed**.
- **Round 2 ("Trash Cat Superstar" — a real AI-guru scene, 6 images, 37 cr):** rendered the keeper styles + a **Fusion** experiment on Sean's own characters (Aiden + a raggedy one-eyed trash-cat). `gpt_image_2` was the stronger engine throughout; the fusion and the tight storybook two-shot were the standouts.
- **Seedance motion test (3 clips × 5s, 52.5 cr) — the deciding gate:** frame-strips confirmed **all three keeper looks survive motion** (no melt into 3D/anime); Sean judged the playback.
- **DECISION:** **FU1 — the FUSION look — is the WINNER and the next register to author.** Flat, boiling-outline 2D cartoon characters that visibly pop against a hand-**painted** gritty storybook world (two media, one frame); it survived the motion test and is the most "uniquely ours." Locked hero candidate: `runs/2026-07-13-signature-blend-spike/round2/out/FU1_fusion.png`; motion proof: `.../round2/seedance/out/FU1.mp4`.
- **Banked for a later research pass (NOT discarded):** **Gritty Storybook** (GS1 wide + GS2 tight — the warm painterly "gritty children's book" look; GS2's tight two-shot is a superb character-design proof). Sean wants this researched at another time. **Collage Real** (flat char on *photographic* world) — explored, distinct, cooler/deadpan, not chosen now. **Riso Cartoon** — banked (see round 1).

**The AI-guru cat episode idea (Sean sparked it this session):** the AI-guru kid (Aiden) tries to make his raggedy one-eyed "trash cat" into a YouTube star / meme, but people mock how raggedy and trash-looking it is. A candidate episode for the [AI-guru series](../../briefs/2026-07-02-ai-guru-pilot/) — and the fusion register's first *potential* consumer (adoption not locked; the pilot's authored register is `90s-nicktoon-grossout`). The one-eyed trash-cat is a possible new series character. *Captured here so the idea isn't lost; it lives fuller wherever the AI-guru series brainstorm continues.*

---

## 7. Un-explored — the taste brainstorm to revisit (nothing here is closed)

The brainstorm converged on ONE next register (fusion); it did **not** exhaust Sean's taste. Pick these up in a future style-brainstorm session (the register-expansion thread stays open):

- **Adult Swim experimental / weird** — Sean named this lane explicitly; we never dug in (we pivoted to the childhood-core round, then to the blend concepts). Superjail! psychedelic-ornate, ATHF crude-flat, Off-the-Air montage, VHS/collage/surreal — a real vein to mine.
- **The six banked candidates, un-spiked** (§2): Cartoon Saloon folk-decorative, UPA / mid-century flat, Gorillaz / Tank Girl grunge-ink, cutout / paper collage, charcoal / woodcut / ink-wash. Each can get its own spike when a project or curiosity calls.
- **Gritty Storybook** (§6) — banked for its own research pass; Sean explicitly wants to keep it.
- **Modern-show references** to mine further: Moon Girl and Devil Dinosaur (graphic / halftone / hip-hop-collage energy), Craig of the Creek (warm CN-house naturalism) — only partly fed into the concepts.
- **Method note for next time:** the taste brainstorm → costed image spike → Seedance motion test → Sean's eye loop worked well and is repeatable. The motion test is the load-bearing gate (stills lie about animatability).
