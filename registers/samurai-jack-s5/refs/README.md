# `samurai-jack-s5/refs/` — what belongs here (and what never does)

This folder holds the register's **style exemplars** — the images the human
eye ratifies the look against, and (only if a go/no-go escalates to a
style-reference feed) the images fed to generation.

**Status:** **LOOK RATIFIED — HERO LOCKED (2026-07-13).** Human Checkpoint 2
passed — Sean picked one hero by eye across the cross-engine spike (his eye the
sole arbiter, no LLM aesthetic judge). The research is complete + ratified
(see [`../research.md`](../research.md)); the register is now cleared to author
(Step B) but is **not yet in `pipeline/registers.py`** — that is the $0
authoring build.

---

## The locked hero

- **File:** [`samurai-jack-s5-hero.png`](samurai-jack-s5-hero.png) — a
  byte-exact copy of the chosen spike candidate
  `spike-2026-07-11/beta_3_flat.png` (md5 `4010abff22a542046286d0e6d4a7af53`).
- **Engine / transport:** Higgsfield CLI, `gpt_image_2` — the register's own
  declared `generation_model` (`gpt-image-2`). Not NB2.
- **Date generated:** 2026-07-11 (the 2026-07-12 Higgsfield prompt-ladder run,
  Block A; run tree `runs/2026-07-11-prompt-ladder-grandmaster/A_generation/`,
  gitignored — the committed hero is the copy here).
- **Dimensions:** 2688×1520 (16:9).
- **Exact prompt** (verbatim; also saved beside the candidate as
  `spike-2026-07-11/beta_3_flat.prompt.txt`):

  > Wide cinematic establishing shot: a lone young boy warrior stands small in
  > the lower-third of the frame, dwarfed by an immense empty sky and a bare
  > flat field to a low horizon, gripping a plain wooden staff point-down at
  > his side, seen from behind. Spiky black hair, red headband with trailing
  > tails, sleeveless white top, gray cropped trousers. FLAT poster-art
  > rendering: the whole image is clean flat color shapes with almost no
  > visible outlines; the figure reads as a stark flat silhouette against the
  > lit field. Any clouds are flat hard-edged shapes, never soft-shaded.
  > Shadows are hard-edged flat shapes, never soft. One muted amber-dusk color
  > cast unifying figure and sky. Vast dramatic negative space, locked camera,
  > silent-samurai-film staging. Absolutely no gradients, no airbrushed or
  > rendered volume, no painterly texture, no outlines. Screenprint/vector
  > poster flatness with bold value blocking.

- **Sean's reason (keyed to the five money axes):** the cleanest flat-poster
  **surface** of the whole spike — clouds and shadows read as **hard-edged flat
  shapes** (not the softer gradient sky of the ChatGPT wanderer), the figure is
  a stark **outline-free silhouette** carried by value contrast alone, one
  **amber-dusk emotional cast** unifies figure and field, the boy is tiny in
  **vast negative space**, and it stages like a **silent-film** standoff. It is
  also on the register's **own `gpt-image` transport** and is the actual named
  consumer (the GRANDMASTER kid), at the highest resolution in the batch.

**Non-derivative check:** the hero depicts an **original** character (the
GRANDMASTER kid, not any franchise character) in an **original** setting, with
**zero franchise tokens** in its prompt. It passes the review test — a fan of
the school recognizes the school; no one can name an episode.

---

## The register spans ALL of these — the hero pins the *surface*, not the *shot*

The full spike spread is retained below **on purpose**: it documents that this
register is a **surface treatment** that survives across shot type, camera
angle, scale, and lighting scenario — it is **not** a "one epic wide shot"
template. Wide vistas, dead-center mediums, dynamic action, tight character
anchors, an office medium two-shot, and four distinct emotional casts
(amber-red / cool blue dawn / ember dusk / cold-gray rain) all read as the same
register. Cy authors only the **surface** (outline-free flat shapes, single
cast, silhouette identity — all valid IR categories); Em judges only the
surface; composition/angle/negative-space is a **per-shot storyboard** decision,
never a register-enforced rule. The hero is the surface look-lock.

**Composition-phrase A/B (2026-07-13, Sean's eye):** we live-tested whether
`dramatic negative space` + `silent-samurai-film staging` in the always-injected
register clause would over-constrain a mundane, non-cinematic scene (a
water-cooler medium two-shot), with vs. without those two phrases. **Result:
keep all five money-phrases as-is.** WITH the phrases the medium shot stayed a
proper medium two-shot (no forced emptiness) and gained a hard-edged flat
shadow + moodier single cast; WITHOUT it read flatter and more stock. The
phrases *enrich* rather than *over-constrain*, even off-genre — so Step B authors
the ratified spec byte-for-byte (no demotion).

---

## Spike candidates (`spike-2026-07-11/`) — provenance

All images below are **Sean's own genericized spike outputs** (no third-party
frames). Everything is 16:9. Prompts marked *(in-session)* were authored in the
look-spike conversation and generated by Sean, who may have lightly adapted
wording; the **hero's** prompt above is verbatim from its saved `.txt`.

### Register-hero candidates — cross-engine (the look-lock comparison)

| File | Engine | Dims | What it is / note |
|---|---|---|---|
| `beta_3_flat.png` **(→ HERO)** | Higgsfield `gpt_image_2` | 2688×1520 | The locked hero. Hardest-edged flat-poster surface; GRANDMASTER kid, amber-dusk plain, seen from behind. |
| `prompt-1-chatgpt.png` | ChatGPT (gpt-image) | 1672×941 | The §10 canonical neutral spike — lone adult wanderer, red salt plain. Textbook and gorgeous; **not** locked only because its clouds read softer than the hero's hard flat shapes and it isn't the named-consumer character. Retained as the plan-canonical neutral exemplar. |
| `prompt-a-chatgpt.png` | ChatGPT | 1672×941 | Variant A *(in-session)* — kid + piñata, dead-center, cool blue dawn cast. |
| `prompt-b-chatgpt.png` | ChatGPT | 1672×941 | Variant B *(in-session)* — kid coiled mid-wind-up, ember dusk cast. |
| `prompt-c-chatgpt.png` | ChatGPT | 1672×941 | Variant C *(in-session)* — kid on a stone platform, cold-gray rain cast. |
| `prompt-1/a/b/c-NB2.jpeg` | NB2 (`nano_banana_flash`) | 16:9 | The **same four prompts** run on NB2 (cross-engine). Honest observation: NB2's *single-frame* output came out more on-register than the research §4 predicted (clean flats, silhouettes, one cast) — but `prompt-1-NB2` uses a **soft gradient sky** (not hard flat cloud shapes) and NB2 added its own letterbox bars. This does **not** reopen the ratified `gpt-image` transport decision (that concerns identity-hold across *edits* + the flat surface, gated on GRANDMASTER; see CHANGELOG 2026-07-12 Block B). |

### Character anchors — GRANDMASTER kid (Bible seed, not register-hero candidates)

| File | Engine | Dims | What it is |
|---|---|---|---|
| `kid-samurai-chatgpt-1.png` | ChatGPT | 1672×941 | Trained kid — single front full-body anchor. |
| `kid-samurai-chatgpt-2.png` | ChatGPT | 1672×941 | Trained kid — 3-view turnaround sheet (front / ¾ / profile). |
| `kid-samurai-chatgpt-3.png` | ChatGPT | 1672×941 | Before-training kid (timid) — single front full-body anchor. |
| `kid-samurai-chatgpt-4.png` | ChatGPT | 1672×941 | Before-training kid — 3-view turnaround sheet. |

Identity thread across all four: round face, spiky black cowlick, **red
headband**. These are GRANDMASTER **character** material for Cy's Bible pass, not
register look-lock candidates — kept here as register-range documentation.

### Scene exemplars — the backyard before/after arc

| File | Engine | Dims | What it is |
|---|---|---|---|
| `kid-samurai-scene-before-1.png` | ChatGPT | 1672×941 | BEFORE — hesitant kid, oversized stick, warm-amber party. |
| `kid-samurai-scene-before-2.png` | ChatGPT | 1672×941 | BEFORE — clumsy blindfold swing, silhouette guests. |
| `kid-samurai-scene-after-1.png` | ChatGPT | 1672×941 | Backyard party beat (Sean's filename label; reads as a party/standing beat rather than the empty-dusk "returns a master" frame). |
| `kid-samurai-scene-after-2.png` | ChatGPT | 1672×941 | Backyard swing beat (Sean's filename label; reads as a party/swing beat). |

---

## What NEVER lands here

Third-party *Samurai Jack* stills, artbook scans, frame grabs, or any image that
reproduces a specific copyrighted character design (Jack, Aku, Ashi, the
Scotsman, the Daughters of Aku), title card, or logo. They are copyrighted study
material — reasoned about with sourced citations in
[`../research.md`](../research.md), viewed there, **never committed to the repo
and never fed to a generation call.** The register's non-derivative rule
(research.md §7): **capture the school, never the episode.** The only committed
images are Sean's own genericized spike outputs. The sole unavoidable named
identifier anywhere in the register is the machine slug `samurai-jack-s5` —
internal, never a production-prompt string.

The `RegisterSpec.reference_images` tuple in `pipeline/registers.py` stays
**empty `()`** by design (no code reads it; see research.md §1 / the plan §4.1).
The locked hero above is documentation, **not** wired into generation or Em.
Populating `reference_images` becomes real work only when the seeds→Cy style-ref
bridge is wired (a deferred front-door DoD piece); at that point, update it
(paths relative to the repo root) in the same commit that adds the files.

**Naming convention (reserved):**
- `spike-YYYY-MM-DD/<descriptor>.png` — dated spike candidates, one folder per
  spike session, engine noted per file in the provenance table above.
- `samurai-jack-s5-hero.png` — the single Sean-locked hero (byte-copy of the
  chosen candidate).
