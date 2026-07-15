# Field report — GRANDMASTER character-design sprint (2026-07-14)

**What this was.** The session opened as "first real production through the screening room" but Sean chose an existing brief — **GRANDMASTER** (the piñata / samurai-homage piece, `briefs/2026-07-02-grandmaster/`) — whose three characters have **no locked Bibles yet**. Rather than fire a blind costed 3-Bible Cy pass against the still-open across-edit-identity gate, we ran a **collaborative character-design sprint** (creative-director lens + cheap gpt-image/Higgsfield look-tests, Sean's eye arbitrating every call). The room was **not** exercised — this is pre-production design, upstream of both the front door (already ran for GRANDMASTER) and Cy (the downstream builder).

**Spend.** 48 Higgsfield credits (3999.64 → 3951.64), all gpt-image-2 edits via the Task-7-proven `invoke_image_edit` runner. Fleet-ops clean (no `ANTHROPIC_API_KEY`; Higgsfield credits, no Claude SDK, no nested-throttle concern). Plus Sean's own uncounted ChatGPT-web-app generations (subscription).

## Decisions locked (the kid)

- **Register:** primal-sketch-grit (re-ratified) — chosen over samurai-jack-s5 and a warm-cream variant after look-testing the wimpy kid in each. **Register is NOT finally locked** — see the open thread below.
- **Glasses = shed armor.** Wimpy kid wears too-big glasses + no headband; trained kid wears the fitted headband + no glasses. The glasses↔headband swap carries the whole transformation.
- **Same body, new attitude.** One physique; posture + headband + gaze do the transformation, not growth.
- **Three states designed:** wimpy (Act 1) → mid-train → trained (Act 3). Sean's final locked look (via his own web-app tinkering): **pale skin, messy brown hair, thick square too-big glasses, chunky worn sneakers**; trained = headband, sleeves torn off, dirt-smudged, sterner brow.
- **Daytime/neutral reads matter.** The dramatic golden-hour lighting hid the face; clean flat-daylight turnaround + candid + a wide isolation-staging shot (other kids playing frame-right, our kid alone in the distant background) gave the real design read.

## Decisions locked (grandma)

- **Heritage:** family is mixed/ambiguous → later refined to **match the boy's family look** (pale skin, silver-grey hair, warm lined face) so she reads as *his* grandmother.
- **Two artifact looks:** the warm old photo-with-the-kid + the **1970s kung-fu-film-heroine** flying-kick reveal snapshot; **unmistakably one woman** across both (aged same face). She only ever appears as artifacts (+ one ghost-beat), so these two looks are close to her whole design.

## The load-bearing craft findings

1. **Across-edit identity holds** on gpt-image/Higgsfield: editing a master reference into a re-posed/re-costumed variant kept the character's face across significant changes — the exact "T2 across-edit identity" question the GRANDMASTER go/no-go flagged, answered *favorably* for both primal and jack on the look-tests.
2. **"Too real" is the primal register's nature, not a prompt slip.** Primal-sketch-grit is inherently gritty-painterly-semirealistic; naming it isn't enough on gpt-image (it renders realistic by default).
3. **Sean's fix — the web-search technique (the session's best discovery).** Replacing the long anti-render style prose with *"STYLE: a stylized 2D hand-drawn ANIMATED CARTOON … Genndy Tartakovsky's show Primal. Use Web search to research Genndy Tartakovsky's show Primal to accurately depict the character animation art style."* gave him the **exact** clean, appealing animated-cartoon look — leaning on ChatGPT's real reference lookup instead of narrated render prose. This is a reusable per-style prompt lever.

## Deliverables (all in `runs/2026-07-14-grandmaster-kid-design/`, gitignored)

- `GRANDMASTER-PROMPT-PACK.md` — the full pack: 5 fresh gens × 2 styles (web-search pattern, Sean's locked appearances) + 5 style-agnostic edits/composites, with the fresh-vs-edit economy baked in.
- `ORCHESTRATION-PROMPT-FOR-CHATGPT.md` — a batch runner for ChatGPT (reads the pack, web-searches the shows, follows the dependency map so it *edits the anchors it makes* for consistency, two style folders, checkpointed batches).
- `Manually-Tinkered-Pass/` — Sean's ratified primal-grit boy anchors (timid / mid-train / trained).
- Look-test PNGs (kid two-state + grandma two-look + register A/B) + the four one-off exploration scripts in `scripts/` (`kid_design_looktest.py`, `kid_design_daytime.py`, `grandma_design.py`, `grandma_register_test.py`) as the repro method.

## Open threads / next steps

- **Register verdict is still Sean's eye** — primal-cartoon (web-search) vs samurai-jack-s5. Sean is running the full pack through ChatGPT in both styles to decide. The pack + orchestration keep both alive.
- **Then Cy** — once the register + anchors are ratified, the anchors ingest as `characters/{kid,grandma,host-dad}/source-refs/` and Cy authors the real Bibles (register + across-edit identity now de-risked). **host-dad is not yet designed** (the third character).
- **Product-gap note (for v1c/v2 planning, not the in-room v1c-triggers ledger):** this entire pre-production design loop happened **outside the screening room** — CLI + ChatGPT web app. Character-design/authoring has no home in the browser room today (character builder is scoped v2). That the best design work flowed through ad-hoc web-app tinkering is a real signal about where the room's edge is.
- The GRANDMASTER go/no-go's across-edit-identity gate is now favorably informed; the register-extension half is subsumed by the live design work.
