# Register backlog + transport findings (the powerhouse roster, made concrete)

**Date:** 2026-07-04
**Status:** Living backlog. Captures decisions + candidate registers surfaced during the `primal-sketch-grit` go/no-go spike. **Not a build list** — each candidate gets the doctrine drill (research → `RegisterSpec` → Cy block → markers → refs) only when Sean greenlights it.
**Relation:** extends the [animation-vocabulary-expansion plan](2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md) §2c roster with real candidates, evidence, and the transport rule the spike proved.

---

## 1. The transport finding — NB2 is not the universal generation engine

The `primal-sketch-grit` go/no-go spike (2026-07-04) established, with Sean's four-engine test, that **NB2 cannot render the raw Tartakovsky-*Primal* grit** — and specifically cannot **edit** a frame into it. **ChatGPT Image 2 (gpt-image) was best by far**; NB Pro and NB2 both fell short. This is a **model limit, not a style limit.**

**The rule this sets (bake into the extension pattern + doctrine):**
- **Transport is per-register, decided by a cheap spike.** NB2 (`gemini-3.1-flash-image-preview`) is the **default** — cheapest, fastest, best across-edit identity hold for the pencil/flat registers. But **gritty / painterly / hand-inked registers may need a different engine** (gpt-image today; fal / self-hosted FLUX-LoRA ticketed).
- **The record is first-class, not a loose note:** `RegisterSpec.generation_model` / `final_model` in `pipeline/registers.py` **is** the "which model for which style" map. Setting it is the deliverable, not a comment. (Sean's ask — "make a note about what models we use for which styles" — is this field.)
- **The open question gpt-image raises:** it *generates* well, but Cy's Bible pass is an **edit** pipeline (anchor → turnarounds → expressions, holding identity across every plate). gpt-image's **across-edit identity hold is unproven** (NB2 was chosen for exactly that, per Flo-B). Any register whose transport is gpt-image needs a **small edit-consistency spike before its first costed Bible pass** — this is the real GRANDMASTER production gate (see `briefs/2026-07-02-grandmaster/go-no-go.md`).

**Pending code change (batch into the next Fable build, TDD):** set `primal-sketch-grit.generation_model` → the gpt-image id in `registers.py`; update `test_primal_sketch_grit.py` + the `research.md` §4 transport line to match. A gpt-image id with no wired runner will fail loud at generation (correct — never silently fall back to NB2).

---

## 2. Candidate register — `warm-storybook-pencil` (Sean likes the Route-C spike output)

**Source:** [`registers/primal-sketch-grit/refs/spike-2026-07-04/C-route-c-pencil.png`](../../registers/primal-sketch-grit/refs/spike-2026-07-04/C-route-c-pencil.png) — the NB2 render of the pencil-test Route-C prompt came out as a **warm, soft, storybook-pencil illustration** that Sean liked and wants to keep for a **future project** (explicitly **not** GRANDMASTER; possibly **ai-guru** if the `90s-nicktoon-grossout` look disappoints — see §4).

**The prompt to keep** (the exact style clause used in the spike):
> Warm pencil-test animation render: graphite line of varying pressure (not vector black), faint pencil construction lines visible under the figure, flat muted color fills, cross-hatch shadow, on a warm cream-paper texture. Warm desaturated palette.

**Open question when it's authored:** is this a *new* register, or a **warm variant of the existing `pencil-test-colored`**? The output is softer/warmer/more children's-book than Sean's actual pencil-test animation look (cream paper, animation-rough). Decide at authoring; NB2 renders it fine (no transport escalation needed — it's pencil-family).

---

## 3. Candidate register — `samurai-jack-s5` (Tartakovsky final-season "poster art")

**Greenlight status:** candidate. **Role:** GRANDMASTER's **revised fallback** (see go-no-go.md) — if gpt-image's across-edit identity hold fails for `primal-sketch-grit`, GRANDMASTER pivots here (same samurai-cinema world, mood preserved) rather than to pencil-test.

**Evidence in hand (strong):**
- Research: [`docs/research/samurai-jack-season-5-art-style-description.md`](../research/samurai-jack-season-5-art-style-description.md) — ChatGPT's craft description + a reusable prompt template + the magic phrase.
- Example (gpt-image / ChatGPT Image 2): [`images/samuria-first-pose-chatgpt.png`](../../images/samuria-first-pose-chatgpt.png) — near-silhouette figure, huge amber sky, cinematic negative space, hard-edged flat shadow shapes. Renders clean on gpt-image.

**The look, in one line (for the eventual `style_token`):** dark minimalist cinematic 2D — clean flat color shapes, **almost no visible outlines**, sharp angular silhouettes, long elegant proportions, hard-edged flat shadow shapes, bold color blocking, dramatic negative space, a single emotional color cast, silent-samurai-film staging. **The negative-control axis vs `primal-sketch-grit`:** *less thick ink, less gritty brushwork, more clean shape design, more silence, more negative space* — the two are **mutually exclusive Tartakovsky registers** (already contrasted in `registers/primal-sketch-grit/research.md` §6).

**Transport:** gpt-image (the ChatGPT example proves it); NB2 likely can't (flat-no-outline is hard, same family of miss). Spike to confirm at authoring.

**When authored, it runs the standard drill** (research → `RegisterSpec` → Cy `## What good looks like — samurai-jack-s5` block → markers → `registers/samurai-jack-s5/refs/` + move the research doc in). The ChatGPT research is the *seed*, not the finished register — the doctrine's depth requirements (§2a) still apply.

---

## 4. `90s-nicktoon-grossout` (ai-guru) — research/test BEFORE authoring

Sean's call (2026-07-04): **research and test the `90s-nicktoon-grossout` (Ren & Stimpy) look before deciding** whether ai-guru uses it — the `warm-storybook-pencil` (§2) is a possible alternative if the grossout output disappoints. So register #2 is **not** "author now"; the next step for it is a **look spike** (like Primal's), across engines, then the authoring decision. This stays the 2nd instance that proves the powerhouse pattern — just gated on Sean liking the look first.

---

## 5. Register-family trigger — approaching, held

Two Tartakovsky registers are now in play (`primal-sketch-grit` authored; `samurai-jack-s5` candidate). That is the **≥2-Tartakovsky trigger** the plan (§3b) set for reconsidering (a) an optional `family: tartakovsky` metadata field and (b) a standalone `tartakovsky` style skill. **Held** until Sean actually greenlights authoring `samurai-jack-s5` — a family field with one member is still a reader-less speculative add. **Revisit at that authoring session**, with both registers' real content in hand to see if any structure is genuinely shared (the honest test, not the count alone).

---

## 6. Roster status (updated from plan §2c)

| Register | Status | Transport | Consumer / role |
|---|---|---|---|
| `pencil-test-colored` + 5 legacy | shipped | NB2 | pencil-test reference implementation |
| `primal-sketch-grit` | **authored**; transport-escalated | **gpt-image** (NB2 no) | GRANDMASTER (pending gpt-image edit-identity validation) |
| `samurai-jack-s5` | candidate (strong evidence) | gpt-image (spike to confirm) | GRANDMASTER fallback; a future samurai piece |
| `warm-storybook-pencil` | candidate (prompt + frame kept) | NB2 (pencil-family) | a future project; maybe ai-guru fallback |
| `90s-nicktoon-grossout` | scoped; **look-spike first** | TBD (spike) | ai-guru (if Sean likes the look) |
| roster remainder (§2c) | sketched backlog | per-register spike | post-front-door-DoD sidequest |

---

## 7. Pending actions (so nothing's lost)

- **[code, next build]** `primal-sketch-grit.generation_model` → gpt-image in `registers.py` + test + `research.md` §4 update.
- **[decision, Sean-paced]** the `90s-nicktoon-grossout` look-spike (across engines) before authoring register #2.
- **[deferred, gated on GRANDMASTER build]** gpt-image transport wiring + across-edit identity validation (or the hand-authored-plates path).
- **[when greenlit]** author `samurai-jack-s5` (drill) + revisit the register-family question.
- **[optional]** ROADMAP note that the register pilot DoD is met and the outward-turn now has a live register-authoring capability + this backlog.
