# claude-mascot re-bake — held for a dedicated pass (2026-05-29)

*Phase 6 of the post-fidelity-fix production session. The sean-anchor bake shipped clean; the mascot did not. Sean reviewed the full plate set and chose to **hold** the mascot commit. This is the finding so the next session starts from the result, not from scratch.*

## What ran

A plates-only bake against the **locked** claude-mascot Bible (13 rules, v1.2) — `scripts/author_bible.py characters/claude-mascot/ --plates-only`. Because the criteria is locked, Pass 1 (Opus authoring) was skipped entirely, so there was **no transient-stub risk** this time (the failure mode that limited the 2026-05-28 mascot bake to a single plate). All 8 plates ran: 2 ingest (anchor copies) + 6 generate, each through NB Pro + Gemini Pass-3. Exit 0.

Evidence in this folder: `contact-sheet.png` (anchor + all 8), `anchor.png`, and the labelled key plates. `plate_verdicts.jsonl` is the per-plate trail.

## The result — mixed, split by plate type

The visual gate is the only reliable arbiter on this register (the PIL similarity tier is a documented liar on the tiny-octopus-on-white anchor, and Gemini's prose verdicts were noisy — it even "failed" the two ingest plates, which are byte-identical copies of the anchor).

| Plate | Read | Verdict |
|-------|------|---------|
| `body-front`, `neutral` (ingest) | anchor copies | fine |
| `expressions/contemplative` | round lozenge, dot eyes, **stub legs** — clean octopus on white | **GOOD** (`GOOD-contemplative-octopus.png`) |
| `expressions/surprised` | octopus form (stub legs, surprised mouth)… on a **black background** | fixable re-roll (`octopus-but-black-bg-surprised.png`) |
| `turnarounds/body-profile-right` | creature profile blob | okay |
| `turnarounds/head-front` | round face + neck, **lost the snout** — generic round head | borderline (`lost-snout-head-front.png`) |
| `turnarounds/body-3quarter` | **standing chibi-humanoid** (2 arms, 2 legs) | DRIFT (`DRIFT-body-3quarter-humanoid.png`) |
| `turnarounds/body-back` | **standing chibi-humanoid** | DRIFT (`DRIFT-body-back-humanoid.png`) |

## The root cause — a reference gap, not a prompt problem

This is materially better than the pre-fix 2026-05-28 result (where *every* generated plate was a generic chibi humanoid and silently passed). The fixed mechanism — runner-owned anchor injection — recovers the octopus form on **front / expression / profile** views, where the anchor's frontal creature shape carries.

It does **not** recover the **standing body turnarounds (3-quarter, back)**, because the anchor is a tiny *crouched* octopus on a ledge with **no standing pose**. NB Pro has nothing to extrapolate a "standing 3/4 body" or "back" from, so it invents a standing biped — the humanoid drift. This is a **Bible-silence / reference-gap** failure, categorically different from the sean-anchor `focused` monochrome drift (which was prompt-dominance and was fixed by trimming the prompt). Trimming the mascot body-turnaround prompts will likely **not** fix this — the information simply isn't in the single anchor.

## Recommendation for the dedicated pass

1. **Don't force standing turnarounds on a crouched-octopus anchor.** Either (a) reconsider whether the mascot Bible needs standing `body-3quarter`/`body-back` plates at all — a creature with no legs-apart standing pose may be better represented by front + profile + expression plates — or (b) author/commission a true standing (or seated/crouched-from-multiple-angles) octopus reference and add it to `source-refs/`, then the turnarounds have something to extrapolate from.
2. **Cheap fixes available now:** re-roll `surprised` for a white/cream background; re-roll `head-front` to keep the snout (the defining octopus feature).
3. **Consider a character LoRA** trained on the octopus form (the Bible's `flux_lora_seed_plates` field anticipates this) — the most robust fix for a minimal-reference creature.
4. **The DINOv2 similarity tier (Phase 7)** is what makes the gate trustworthy on this register; re-score this run's `plate_verdicts.jsonl` once it lands and confirm the recovered octopus plates score above the humanoid drifters (the PIL tier could not).

## State on disk

The working-tree plate changes from this bake were **reverted** — the committed claude-mascot Bible (rules, plan, and whatever plates were committed before) is untouched, per Sean's hold decision. The full bake outputs live in the gitignored `runs/2026-05-29-cy-claude-mascot-production/`; the curated evidence is this folder.
