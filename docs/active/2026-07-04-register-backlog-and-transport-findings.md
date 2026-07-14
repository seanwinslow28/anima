# Register backlog + transport findings (the powerhouse roster, made concrete)

**Date:** 2026-07-04
**Status:** Living backlog. Captures decisions + candidate registers surfaced during the `primal-sketch-grit` go/no-go spike. **Not a build list** — each candidate gets the doctrine drill (research → `RegisterSpec` → Cy block → markers → refs) only when Sean greenlights it.
**Relation:** extends the [completed animation-vocabulary-expansion plan](../COMPLETED/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md) §2c roster with real candidates, evidence, and the transport rule the spike proved.

---

## 1. The transport finding — NB2 is not the universal generation engine

The `primal-sketch-grit` go/no-go spike (2026-07-04) established, with Sean's four-engine test, that **NB2 cannot render the raw Tartakovsky-*Primal* grit** — and specifically cannot **edit** a frame into it. **ChatGPT Image 2 (gpt-image) was best by far**; NB Pro and NB2 both fell short. This is a **model limit, not a style limit.**

**The rule this sets (bake into the extension pattern + doctrine):**
- **Transport is per-register, decided by a cheap spike.** NB2 (`gemini-3.1-flash-image`) is the **default** — cheapest, fastest, best across-edit identity hold for the pencil/flat registers. But **gritty / painterly / hand-inked registers may need a different engine** (gpt-image today; fal / self-hosted FLUX-LoRA ticketed).
- **The record is first-class, not a loose note:** `RegisterSpec.generation_model` / `final_model` in `pipeline/registers.py` **is** the "which model for which style" map. Setting it is the deliverable, not a comment. (Sean's ask — "make a note about what models we use for which styles" — is this field.)
- **The open question gpt-image raises:** it *generates* well, but Cy's Bible pass is an **edit** pipeline (anchor → turnarounds → expressions, holding identity across every plate). gpt-image's **across-edit identity hold is unproven** (NB2 was chosen for exactly that, per Flo-B). Any register whose transport is gpt-image needs a **small edit-consistency spike before its first costed Bible pass** — this is the real GRANDMASTER production gate (see `briefs/2026-07-02-grandmaster/go-no-go.md`).

**Code change completed 2026-07-11; transport T1 completed 2026-07-13:** `primal-sketch-grit.generation_model` records `gpt-image-2`, and `invoke_image_edit` now dispatches that honest model ID through the fail-closed Higgsfield map. A model in neither the google-genai allowlist nor the Higgsfield map still fails loud; there is never a silent NB2 fallback. The costed, in-register edit-consistency gate remains pending.

---

## 2. Candidate register — `warm-storybook-pencil` (Sean likes the Route-C spike output)

**Source:** [`registers/primal-sketch-grit/refs/spike-2026-07-04/C-route-c-pencil.png`](../../registers/primal-sketch-grit/refs/spike-2026-07-04/C-route-c-pencil.png) — the NB2 render of the pencil-test Route-C prompt came out as a **warm, soft, storybook-pencil illustration** that Sean liked and wants to keep for a **future project** (explicitly **not** GRANDMASTER; possibly **ai-guru** if the `90s-nicktoon-grossout` look disappoints — see §4).

**The prompt to keep** (the exact style clause used in the spike):
> Warm pencil-test animation render: graphite line of varying pressure (not vector black), faint pencil construction lines visible under the figure, flat muted color fills, cross-hatch shadow, on a warm cream-paper texture. Warm desaturated palette.

**Open question when it's authored:** is this a *new* register, or a **warm variant of the existing `pencil-test-colored`**? The output is softer/warmer/more children's-book than Sean's actual pencil-test animation look (cream paper, animation-rough). Decide at authoring; NB2 renders it fine (no transport escalation needed — it's pencil-family).

---

## 3. Register — `samurai-jack-s5` (Tartakovsky final-season "poster art") — **AUTHORED 2026-07-13**

**Greenlight status:** ~~candidate~~ **AUTHORED + committed 2026-07-13** (Step B, the pure doctrine drill; ratified plan [`docs/active/2026-07-11-samurai-jack-s5-register-design.md`](2026-07-11-samurai-jack-s5-register-design.md); Step R research + Step S hero both Sean-ratified). The register is live in `pipeline/registers.py` (register #9), with its Cy Example E, markers, doctrine line, template comment, and per-register test (`tests/test_samurai_jack_s5.py`). Transport = gpt-image (`gpt-image-2`), **Higgsfield-wired since 2026-07-13** through `pipeline/agents/higgsfield_runner.py`. **Role:** GRANDMASTER's **revised style/identity-hold fallback** (a committed future style, one of Sean's two go-to registers) — if primal's gritty look doesn't land, GRANDMASTER pivots to this clean-flat sibling. **Still deferred + gated:** the T2 across-edit identity validation rides the costed, Sean-greenlit GRANDMASTER build; Task 7's production-path live smoke has not run.

**Evidence in hand (strong):**
- Research: [`docs/research/samurai-jack-season-5-art-style-description.md`](../research/samurai-jack-season-5-art-style-description.md) — ChatGPT's craft description + a reusable prompt template + the magic phrase.
- Example (gpt-image / ChatGPT Image 2): [`images/samuria-first-pose-chatgpt.png`](../../images/samuria-first-pose-chatgpt.png) — near-silhouette figure, huge amber sky, cinematic negative space, hard-edged flat shadow shapes. Renders clean on gpt-image.

**The look, in one line (for the eventual `style_token`):** dark minimalist cinematic 2D — clean flat color shapes, **almost no visible outlines**, sharp angular silhouettes, long elegant proportions, hard-edged flat shadow shapes, bold color blocking, dramatic negative space, a single emotional color cast, silent-samurai-film staging. **The negative-control axis vs `primal-sketch-grit`:** *less thick ink, less gritty brushwork, more clean shape design, more silence, more negative space* — the two are **mutually exclusive Tartakovsky registers** (already contrasted in `registers/primal-sketch-grit/research.md` §6).

**Transport:** **gpt-image via Higgsfield, wired 2026-07-13.** The Step-S cross-engine spike selected the locked Higgsfield `gpt_image_2` hero; `RegisterSpec.generation_model` records `gpt-image-2`, and the exact transport map dispatches it through `pipeline/agents/higgsfield_runner.py`.

**Authoring completed 2026-07-13 via the standard drill:** research → `RegisterSpec` → Cy `## What good looks like — samurai-jack-s5` block → markers → `registers/samurai-jack-s5/refs/`. The thin ChatGPT research was only the seed; the authored register is grounded in the full research artifact and locked hero.

---

## 4. `90s-nicktoon-grossout` (ai-guru) — **AUTHORED 2026-07-11**

Sean's 2026-07-04 research-first gate was completed: the corrected appealing-human default passed the cross-engine look spike on NB2, Sean ratified it, and the register shipped as expansion register #2 / registry register #8 in PR #106. It is live in `pipeline/registers.py`, has its Cy worked example, markers, doctrine/template touchpoints, and `tests/test_90s_nicktoon_grossout.py`. Transport remains the direct Gemini NB2 default; ai-guru is its named consumer. `warm-storybook-pencil` (§2) remains a separate candidate, not an unresolved fallback decision for this authored register.

---

## 5. Register-family trigger — **answered FOLD (2026-07-13)**

Two Tartakovsky registers are now authored (`primal-sketch-grit` + `samurai-jack-s5`). The **≥2-Tartakovsky trigger** the plan (§3b) set for reconsidering (a) an optional `family: tartakovsky` metadata field and (b) a standalone `tartakovsky` style skill is now **RESOLVED FOLD** (ratified plan §2A, Sean's call 2026-07-11): with both registers' real content in hand, the honest test found the only shared structure is *timing & staging grammar* (which already lives in the primal `research.md` §8 "for Bea/Mo, not the still register" section) — the `RegisterSpec` still-frame fields **invert on every axis** (line/fill/texture/shadow). A `family` field would have **no reader** in v1 (the front-door red-teams' exact anti-pattern), and the `tartakovsky` skill fails the §3a promotion bar (needs ≥2 real consumers AND standalone reusable structure; there is one named consumer). Sean's **product ceiling** seals it: Samurai Jack + Primal are his only two Tartakovsky styles and Clone Wars collapses into `samurai-jack-s5` — the family caps at two and never grows. The relationship lives as **documentation** (the reciprocal primal↔samurai `research.md` cross-link), not code.

---

## 6. Roster status (updated from plan §2c)

| Register | Status | Transport | Consumer / role |
|---|---|---|---|
| `pencil-test-colored` + 5 legacy | shipped | NB2 | pencil-test reference implementation |
| `primal-sketch-grit` | **authored**; transport-escalated | **gpt-image** (NB2 no) | GRANDMASTER (pending gpt-image edit-identity validation) |
| `samurai-jack-s5` | **authored 2026-07-13**; transport wired | **gpt-image via Higgsfield** | GRANDMASTER fallback (pending gpt-image edit-identity validation); a future flat-cinematic piece |
| `warm-storybook-pencil` | candidate (prompt + frame kept) | NB2 (pencil-family) | a future project; maybe ai-guru fallback |
| `90s-nicktoon-grossout` | **authored** (register #8, PR #106) | NB2 (GO) | ai-guru pilot |
| `flat-cast-painted-world` (the FUSION look) | **authored 2026-07-13** (register #10); transport wired | **gpt-image via Higgsfield** (NB2 confirmation spike NO-GO'd, collapsed the two-media split) | signature look; ai-guru "trash cat" episode (potential); T2 edit-identity validation pending. [Research](../../registers/flat-cast-painted-world/research.md) · [Kickoff](2026-07-13-fusion-register-authoring-kickoff.md) |
| Gritty Storybook · Collage Real · Riso + 6 taste candidates | **banked** (taste brainstorm 2026-07-13) | per-register spike | [taste brainstorm](2026-07-13-signature-style-taste-and-blend-brainstorm.md) §2/§6/§7 |
| roster remainder (§2c) | sketched backlog | per-register spike | post-front-door-DoD sidequest |

---

## 7. Pending actions (so nothing's lost)

- **[DONE 2026-07-11]** `primal-sketch-grit.generation_model` records `gpt-image-2`; its registry/test/research record is current.
- **[DONE 2026-07-11]** `90s-nicktoon-grossout` look-spike + authoring completed; NB2 selected, register #8 shipped in PR #106.
- **[DONE — T1 built 2026-07-13]** gpt-image transport wiring: `gpt-image-2` now dispatches through Higgsfield `gpt_image_2` in [`pipeline/agents/higgsfield_runner.py`](../../pipeline/agents/higgsfield_runner.py), executing T1 of the [Higgsfield switchover plan](2026-07-13-higgsfield-switchover-build-kickoff.md) and decisions D4/D5 in the [ratified transport strategy](2026-07-13-transport-strategy-decision.md). Unknown mappings still fail loud. **T2 remains standing:** the in-register across-edit identity validation still rides the costed, Sean-greenlit GRANDMASTER build — the probe was pencil-register only. Task 7's live production-path smoke is also still gated and unrun.
- **[DONE 2026-07-13]** ~~author `samurai-jack-s5` (drill) + revisit the register-family question.~~ Authored (register #9, §3); the family question is answered **FOLD** (§5).
- **[optional]** ROADMAP note that the register pilot DoD is met and the outward-turn now has a live register-authoring capability + this backlog.
- **[DONE 2026-07-13]** ~~author the **FUSION** register (flat cartoon cast on a hand-painted gritty world) — eye-ratified + Seedance-motion-tested; run the [kickoff](2026-07-13-fusion-register-authoring-kickoff.md) through the [playbook](../architecture/style-register-authoring-playbook.md).~~ **Authored** as `flat-cast-painted-world` (register #10; §6 roster); R→S→B end-to-end, transport = gpt-image via Higgsfield (T1 wired; NB2 spike NO-GO'd). It is the **third gpt-image register**; its T2 production edit-identity validation remains gated.
- **[banked, revisit]** the taste-brainstorm roster — Gritty Storybook (Sean wants it researched later), Collage Real, Riso, + Cartoon Saloon / UPA / Gorillaz-ink / cutout / charcoal-woodcut; and the un-dug **Adult Swim experimental** lane. See [taste brainstorm](2026-07-13-signature-style-taste-and-blend-brainstorm.md) §7.
