# Worked example — the GRANDMASTER character-design sprint

The quality bar for an Art Department session. This is a condensation of the
[2026-07-14 field report](../../../../docs/anima-test-runs/2026-07-14-grandmaster-character-design-sprint.md)
— read that for the full record. The committed structural shape is the fixture
at [`evals/artdept/fixtures/grandmaster-mini/`](../../../../evals/artdept/fixtures/grandmaster-mini).
The sprint ran the whole loop by hand, *before the room existed* — it is the
proof the stage was missing, and the template for what Artie now runs.

## What the loop looked like

Sean opened GRANDMASTER (the piñata / samurai-homage piece) whose three
characters had no locked Bibles. Rather than fire a blind costed Cy pass, the
session ran a **collaborative design sprint**: creative-director lens + cheap
gpt-image/Higgsfield look-tests, **Sean's eye arbitrating every call.** The
shape was exactly the room's chain — read the brief, take each character from
personality → visual design, look-test the register on cheap generations, lock,
then expand outward to the second character, the backgrounds, and the staging.

**Spend:** 48 Higgsfield credits (3999.64 → 3951.64), all gpt-image-2 edits via
the Task-7-proven `invoke_image_edit` runner. Fleet-ops clean — Higgsfield
credits, **no `ANTHROPIC_API_KEY`**, no Claude SDK. Plus Sean's own uncounted
Codex / ChatGPT Desktop app generations (subscription; path-based, project filesystem) — the definitive batch.

## Decisions locked

**The kid.**
- **Register:** primal-sketch-grit, chosen over samurai-jack-s5 and a warm-cream
  variant after look-testing the wimpy kid in each. (Register kept alive in both
  styles for Sean's final ChatGPT call — the pack ships both.)
- **Glasses = shed armor.** Wimpy kid: too-big glasses, no headband. Trained kid:
  fitted headband, no glasses. **The glasses↔headband swap carries the whole
  transformation.**
- **Same body, new attitude.** One physique; posture + headband + gaze do the
  transformation, not growth.
- **Locked look:** pale skin, messy brown hair, thick square too-big glasses,
  chunky worn sneakers; trained = headband, torn sleeves, dirt-smudged, sterner
  brow.

**The grandma.**
- **Heritage:** refined to match the boy's family look (pale skin, silver-grey
  hair, warm lined face) so she reads as *his* grandmother.
- **Two artifact looks:** the warm old keepsake photo + the 1970s kung-fu-heroine
  flying-kick reveal — **unmistakably one woman** across both (aged same face).
  She appears only as artifacts, so these two looks are close to her whole design.

## The three craft findings

1. **Across-edit identity holds** on gpt-image/Higgsfield: editing a master
   reference into a re-posed / re-costumed variant kept the face across
   significant changes — the "T2 across-edit identity" question, answered
   favorably for both primal and jack. (This is the rubric's criterion 2.)
2. **"Too real" is the primal register's nature, not a prompt slip.** Primal is
   inherently gritty-painterly-semirealistic; naming it isn't enough on gpt-image
   (it renders realistic by default).
3. **The web-search technique — the session's best discovery.** Replacing long
   anti-render style prose with *"STYLE: a stylized 2D hand-drawn ANIMATED
   CARTOON … Genndy Tartakovsky's show Primal. Use Web search to research …"*
   gave Sean the exact clean animated-cartoon look, leaning on ChatGPT's real
   reference lookup. A reusable per-style lever (technique-kit (a)).

## The deliverables shape

All in `runs/2026-07-14-grandmaster-kid-design/` (gitignored):

- **`GRANDMASTER-PROMPT-PACK.md`** — 5 fresh gens × 2 styles (web-search pattern,
  Sean's locked appearances) + 5 style-agnostic edits/composites, fresh-vs-edit
  economy baked in.
- **`ORCHESTRATION-PROMPT-FOR-CHATGPT.md`** — a batch runner for ChatGPT: reads
  the pack, web-searches the shows, follows the dependency map so it *edits the
  anchors it makes*, two style folders, checkpointed batches.
- **`Manually-Tinkered-Pass/`** — Sean's ratified primal-grit anchors (timid /
  mid-train / trained), the ratified `source-refs/` inputs.
- **Look-test PNGs** (kid two-state + grandma two-look + register A/B) + the
  one-off exploration scripts as the repro method.

**What the room turns this into:** the same shape, emitted as a validated bundle
— `design-bible.md`, `prompt-pack.md`, `chatgpt-orchestration.md`,
`environment-style.md`, `cast_list.yaml`, `artdept.json`,
`cy_readiness_report.md`, and populated `characters/{id}/source-refs/` — so Cy
can start. **Open thread:** host-dad (the third character) was never designed;
the register verdict was still Sean's eye between primal-cartoon and
samurai-jack-s5, run through the full pack in ChatGPT. That is exactly the live
Checkpoint-3 session the room is built to run.
