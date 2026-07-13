# `flat-cast-painted-world/refs/` — what belongs here (and what never does)

This folder holds the register's **style exemplars** — the images the human eye
ratifies the look against, and (only if a go/no-go escalates to a
style-reference feed) the images fed to generation.

**Status:** `LOOK RATIFIED — HERO LOCKED — READY TO AUTHOR (2026-07-13)` (see
[`../research.md`](../research.md)). Human Checkpoint 1 (research) + Human
Checkpoint 2 (cold hero confirm) both passed. The hero bytes are committed
(byte-exact copy below). **Transport RESOLVED — `GPT_IMAGE` (unwired):** the
Step-S NB2 confirmation spike came back NO-GO (NB2 collapsed the two-media split;
see the spike table below + research §4). The register is cleared to author
(Step B) but is **not yet in `pipeline/registers.py`** — that is the $0 authoring
build.

---

## The locked hero

The look was **eye-ratified + motion-tested** at the 2026-07-13 costed spike
(Sean's eye the sole arbiter — a Higgsfield `gpt_image_2` image spike + a Seedance
2.0 motion test; see the [taste/blend brainstorm](../../../docs/active/2026-07-13-signature-style-taste-and-blend-brainstorm.md)
§6). Step S is therefore **light**: the ratified `FU1_fusion.png` bytes are copied
unchanged into `flat-cast-painted-world-hero.png`, and Sean confirms cold
(Checkpoint 2).

- **Hero file:** [`flat-cast-painted-world-hero.png`](flat-cast-painted-world-hero.png)
  — a byte-exact copy of the ratified spike candidate (md5
  `0235b6c6192b798291fe306a776c382e`).
- **Source candidate:** `runs/2026-07-13-signature-blend-spike/round2/out/FU1_fusion.png`
  (gitignored, local-only; the committed hero is the copy here — same md5).
- **Engine / transport:** Higgsfield CLI, `gpt_image_2` (= `GPT_IMAGE`,
  `gpt-image-2`) — the register's provisional declared `generation_model`. **Open
  at Step S:** an NB2 confirmation spike may flip the recorded transport to
  `NB2_FLASH` if NB2 holds the flat-cast-on-painted-world split (research §4). The
  hero is the **look-lock** and stays FU1 regardless of the recorded transport.
- **Date generated:** 2026-07-13.
- **Dimensions:** 2688×1520 (16:9).
- **Motion proof:** `runs/2026-07-13-signature-blend-spike/round2/seedance/out/FU1.mp4`
  (Seedance 2.0, 2026-07-13) — the fusion look survived motion (no melt into
  3D/anime; the flat cast stayed flat, the painted world stayed painted). The
  motion test was the deciding gate.
- **Exact prompt** (verbatim from
  `runs/2026-07-13-signature-blend-spike/round2/prompts/FU1_fusion_gpt.txt`):

  > A flat, boldly hand-drawn 2D cartoon boy and a raggedy one-eyed scruffy
  > orange trash-cat with thick wobbling boiling ink outlines and flat cel colors
  > — deliberately NO rendered volume on the figures — set inside a richly
  > PAINTED, gritty hand-made children's-storybook world: cross-hatched dry-brush
  > weathered urban surfaces, a muted earthy palette (ochre, brick-red, sage,
  > cream), folk-decorative flourishes, soft gouache washes, warm golden-hour
  > grime. NOT a photograph — a painted illustrated world. The flat graphic
  > characters POP against the painterly-gritty painted environment (two media,
  > one frame).
  >
  > SCENE: the lanky early-teen boy (messy hair, oversized striped hoodie,
  > camera-ready showman face — huge unblinking eyes, too-wide grin) crouches on
  > the painted gritty corner-store stoop, proudly holding the raggedy trash-cat
  > (matted fur, one eye scarred shut, torn ear, snaggletooth, unimpressed scowl)
  > toward a phone on a ring-light tripod; a laptop on a crate glows with generic
  > laughing-crying emoji comments and a cute glowing round chibi assistant-mascot.
  > Trash cans, cracked concrete, tangled wires, all painted. Medium shot. 16:9.

- **Sean's reason (keyed to the register's money axes; to be confirmed cold at
  Checkpoint 2):** the two-media split is unmistakable — the flat boiling-line
  cast POPS off a fully **painted** (not photographic) gritty storybook world;
  the muted earthy palette (ochre/brick-red/sage/cream) and warm golden-hour
  grime unify the frame; the cast is flat cel with no rendered volume; and it
  survived the Seedance motion test. It is the most "uniquely ours" of the spike.

**Non-derivative check:** the hero depicts **original** characters (Sean's own
AI-guru kid + the raggedy trash-cat, no franchise character) in an **original**
setting, with **zero franchise tokens** in its prompt. It passes the review test
— a fan of the mixed-media school recognizes the school; no one can name an
episode.

---

## Spike candidates (`spike-2026-07-13/`) — provenance

All images are **Sean's own genericized spike outputs** (no third-party frames),
16:9, original characters (his AI-guru kid + trash-cat), zero franchise tokens.

| File | Engine | Dims | What it is / verdict |
|---|---|---|---|
| `FU1-NB2-transport-spike.png` | Higgsfield MCP `nano_banana_2` (NB2) | 1376×768 | **The Step-S NB2 confirmation spike — NO-GO.** The exact FU1 prompt run on NB2 (varies engine, not art direction). NB2 hit the scene + muted-earthy palette + golden-hour warmth, but **collapsed the two-media split** into one unified illustrated cartoon medium and **dropped the boiling hand-inked outline** (clean uniform digital line; the cat drifted toward rendered fur volume). Landed closer to the banked *Gritty Storybook* (unified medium) than to the fusion split. Sean's eye + the analysis agreed: NB2 can't render the register's core → **record `GPT_IMAGE`.** (Job `c922c19c-8cc5-40aa-a971-27750bf77ef3`.) |

The **hero** (`flat-cast-painted-world-hero.png` = `FU1_fusion.png`, gpt-image) is
the look-lock; the NB2 spike above is retained as the transport-decision evidence,
not a hero candidate.

---

## What NEVER lands here

Third-party frames, artbook scans, or frame grabs from any of the shows named as
craft lineage in [`../research.md`](../research.md) (Cartoon Saloon films, *Over
the Garden Wall*, *Hey Arnold!*, *Ed, Edd n Eddy*, etc.), or any image that
reproduces a specific copyrighted character design, title card, or logo. They are
copyrighted study material — reasoned about with sourced citations in
`research.md`, viewed there, **never committed to the repo and never fed to a
generation call.** The register's non-derivative rule (research.md §7): **capture
the school, never the episode.** The only committed images are Sean's own
genericized spike outputs. The sole unavoidable named identifier anywhere in the
register is the machine slug `flat-cast-painted-world` — internal, never a
production-prompt string.

The `RegisterSpec.reference_images` tuple in `pipeline/registers.py` stays
**empty `()`** by design (no code reads it; research.md §2 / the samurai plan
§4.1). The locked hero is documentation, **not** wired into generation or Em.
Populating `reference_images` becomes real work only when the seeds→Cy style-ref
bridge is wired (a deferred front-door DoD piece).

**Naming convention (reserved):**
- `spike-YYYY-MM-DD/<descriptor>.png` — dated spike candidates (if a Step-S
  confirmation spike runs), one folder per session, engine noted per file.
- `flat-cast-painted-world-hero.png` — the single Sean-locked hero (byte-copy of
  the ratified candidate), locked at Step S.
</content>
