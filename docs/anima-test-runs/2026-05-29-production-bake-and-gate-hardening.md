# The production bake + gate hardening — what over-reached, what we held, what we learned

*2026-05-29 (filed 2026-05-30). The session after the fidelity fix. The mechanism was supposed to be done; this session was supposed to be the easy part — approve the Bible, bake the plates, install the gate, ship. Instead it became a study in the difference between a mechanism and a judgment: four times the mechanism proposed something wrong (a prop drawn as a person, a bake that would erase the approval, a critic that failed the artist's own drawings, a similarity gate that would reject good plates), and four times a human read — of the code, of the plates, of the data — overrode it. Nine phases, eight commits, 176 → 187 tests green throughout, two human-review gates that changed the outcome. This is the field report.*

---

## What the session was supposed to be

The 2026-05-29 fidelity fix had closed the mechanism-level identity gap: runner-owned anchor injection, no reference-chaining, role-tag prompts, the Pass-2.5 similarity gate, the robust JSON parser. 176 tests green. It deliberately left the production bake undone — the sean-anchor Bible's rules/plan/regions were fixed but `locked: false`, and its plate PNGs were never regenerated, because "the director approves the Bible, and the new plates should be baked against the approved rules, not pre-empted." The mascot had baked exactly one plate before hitting a transient stub.

The plan inherited from that handoff was nine phases, each its own commit: fix one remaining mechanism bug (the prop-plate defect), tighten the crop boxes, approve the sean-anchor Bible, bake its production plates, re-bake the mascot, install the DINOv2 similarity tier and promote the gate to a hard reject, and wire a Pass-1 retry. Honor the human-review gates marked STOP. Keep the suite green.

What actually happened: the prop fix was clean, but every phase after it surfaced a place where the planned mechanism — or the planned command — was subtly wrong, and only a human read caught it before it shipped. The most dangerous of them never ran.

---

## Phase 1 — the prop fix: a correct fix that over-generalized

The fidelity fix made the runner the source of truth for identity: inject `anchor.png` first on every generate plate, frame the prompt around "match Image 1 exactly." This was right for turnarounds and expressions and wrong for one class of plate. The re-baked `props/stylus.png` had rendered the full character with a stylus floating beside an empty-gripping hand, plus the prompt's meta-prose rendered as handwritten captions — because a full-body anchor with a "match this person" prompt tells NB Pro to draw the person.

The fix taught the runner that a plate under `props/` is a distinct class: no anchor injection (`_resolve_generate_references` returns `is_prop`), an isolated-object prompt that forbids any figure and any text (`_build_prop_prompt`), and exemption from the Pass-2.5 anchor-similarity gate (an isolated object scored against a full-character anchor is always near-zero — recorded for the audit trail, never used to reject). The stylus plan entry was trimmed to a short object-intent.

**The deepest lesson**: a fix can be correct and still over-generalize. "The runner owns identity" was the right correction; "every plate is the character" was the over-reach hidden inside it. The fidelity fix's own validation never caught the stylus because the stylus is the one plate where identity *isn't* the thing being referenced. When you centralize a rule, enumerate the classes it doesn't apply to before you trust it everywhere.

Validated live in Phase 5: the re-baked stylus came back a clean isolated object.

---

## Phase 2 — the crops, and a director who hand-cropped

The committed `#region` crop mechanism worked. The plan was a one-line box nudge (`body-front` left edge `0.02 → 0.05`) to clear the "A-2" production label. The render showed it still caught the label fragment. At the STOP, Sean elected to hand-crop the four body views himself rather than tune boxes — and his `body-3quarter` crop *kept* the "(A-2)" label, the exact thing Phase 2 set out to remove.

This is a small thing, but it's a clean instance of the session's shape: the human review changed the artifact set. Sean's crops dropped the `body-front` plate entirely (the sheet's top row is front/profile-L/profile-R/back — there's no distinct standing front body pose), added `body-profile-left`, and the plate plan was repointed to ingest his hand-trimmed files. The label got trimmed off `body-3quarter` only because a one-line confirm surfaced that his "those are fine" might conflict with the phase's whole purpose.

**The deepest lesson**: "the crops are fine" from the director is an approval of framing, not a waiver of the phase's stated goal. Surface the conflict in one line; don't silently ship the contradiction or silently override the director.

---

## Phase 4 — the bug that never ran

This is the one that would have cost the most, and it never executed, because it was caught by reading the code before running the planned command.

The plan's Phase 5 said: `python scripts/author_bible.py characters/sean-anchor/ …`. The plan's own rollback note said: "the approved rules (`locked: true`) are not touched by a bake." Those two statements are incompatible with the code as it stood. `author_bible.py` → `CharacterDesignerNode.run` **always ran Pass 1** — Opus re-authors the *entire* envelope every invocation: `character.yaml`, `acceptance_criteria.json` (written with `locked: false`), risk-bible, confidence-notes, **and `plate_generation_plan.json`**. Running the planned Phase 5 command would have:

- overwritten the plan committed in Phases 1–2 (Opus would re-emit region-based body crops and the verbose stylus prompt, erasing the trimmed stylus and Sean's hand crops),
- overwritten the approved criteria back to `locked: false` with freshly-authored rules, erasing the Phase 4 approval.

`bible iterate`, the apparent escape hatch, only writes a narrowed `*_iterate.json` plan that nothing executes. The capability the entire "approve → bake" flow assumed — bake plates against an approved Bible without re-authoring it — **did not exist.**

The fix (Phase 4a, its own commit) added it: `run()` branches on `_resolve_plates_only`, which is true when an explicit `plates_only` flag is set *or* the on-disk criteria is `locked: true`. The locked auto-detect is the safety net — an approved Bible can never be silently re-authored even if the caller forgets the flag. Plates-only loads the on-disk Bible and runs Passes 2+3 against it, rewriting nothing. This also turned out to sidestep the transient-Opus-stub problem entirely (Phases 5 and 6 both ran with no Opus call at all).

**The deepest lesson**: the most dangerous failure of the session is the one that exited zero in your imagination. The plan was internally contradictory — a stated command and a stated invariant that the code couldn't both honor — and the only thing that caught it was reading `CharacterDesignerNode.run` before trusting `author_bible.py`. A plan is a proposal about a mechanism; verify the mechanism actually has the shape the plan assumes before you run it. Approval has to be *enforceable* (the lock routes the bake), not merely *conventional* (everyone agrees not to re-author).

The same phase surfaced a quieter version: the full-color decision (commit 3) had been ported into `acceptance_criteria.json` but never into the sibling docs — `character.yaml` still carried a 4-color monochrome palette and "no dedicated skin color," `risk-bible.md` said "skin tone is intentionally absent," `cy-confidence-notes.md` referenced a rule ID (`IR.sean.palette.no-explicit-skin-tone`) that no longer existed. `bible show` rendered the contradiction. Locking the Bible on inconsistent docs would have shipped it. Fixed before the `bible approve`.

---

## Phase 5 — the bake, and prompt-dominance again

The plates-only bake ran clean — exit 0, no stub, 24 plates. Gemini flagged **12 of 24 for human gate**, which sounds catastrophic and wasn't. Ten of the twelve were *ingested plates* — Sean's own hand-trimmed body crops, the colored `#region` head crops, the line-art motion frames. Gemini "failed" them because it's skeptical of small crops, and it failed the two ingest plates that are byte-identical copies of the anchor. Ingests can't regenerate, so they surface to the human by design. The real signal was two generated drifters.

`props/stylus.png` came back clean (Phase 1 validated). But `expressions/focused.png` came back **monochrome** — no color, no blue eyes, no navy tee, more realistic than the cartoon anchor — and Gemini gated it after three attempts that all stayed mono. The root cause was instructive: the expression plate prompts in the plan *still carried the monochrome-era verbose prose* ("no explicit skin tone," heavy "warm graphite #3D3530") that the full-color port never reached. The runner's framing says "keep the full color of Image 1"; the plate text says "warm graphite, no skin tone." Three plates (neutral, surprised, contemplative) resolved that conflict toward color; `focused` resolved it toward monochrome — and the reject-reason feedback loop, fed Gemini's line-weight complaints, pushed NB Pro *harder* into pencil-sketch on each retry.

This is the original fidelity bug, recurring in the one place the fidelity fix didn't reach: **prompt-dominance**. The fix moved framing into the runner, but it never re-authored the plate prompts, so a plate whose verbose text fought the framing could still lose. The re-roll fix was to trim `focused`'s prompt to a short expression-intent and let the runner's anchor framing drive — similarity jumped 0.23 → 0.81, full color recovered. (`stylus` was re-rolled the other direction: from a too-short prompt that rendered metallic-realistic to one naming the pencil register.) Both surgically, via changed prompts that auto-busted the content-addressed cache, leaving the passing plates untouched.

**The deepest lesson**: a centralized fix only holds where the inputs it competes with stay quiet. The runner owning framing is necessary but not sufficient; a loud-enough plate prompt still wins. The latent risk remains — neutral/surprised/contemplative carry the same verbose prose and merely got lucky this bake. The durable fix is to trim *all* plate prompts to short intent, not just the one that drifted.

---

## Phase 6 — the drift you can't prompt away

The mascot re-bake (plates-only, locked Bible, no Opus call, no stub risk) ran all 8 plates. The result was genuinely better than the pre-fix run — where *every* generated plate was a generic chibi-humanoid that silently passed — but it was a split decision. The orange pixel-octopus recovered on the **front / expression / profile** views: `contemplative` is a clean round-lozenge octopus with stub legs; `surprised` is the octopus (on a wrong black background); `body-profile-right` reads as the creature. But the **standing body turnarounds** — `body-3quarter`, `body-back` — drifted to standing chibi-humanoids with two arms and two legs.

The cause is categorically different from `focused`. The mascot anchor is a tiny *crouched* octopus on a ledge, with no standing pose. Asked for a "3-quarter body" or "back" turnaround, NB Pro has nothing to extrapolate from, so it invents a standing biped. This is a **reference gap**, not prompt-dominance. Trimming the prompt — the `focused` fix — won't recover it, because the information simply isn't in the single anchor.

Sean held the commit. The working-tree plates were reverted (the committed mascot Bible is untouched), and the result was preserved as labelled evidence + a finding for a dedicated pass: reconsider whether a legless creature needs standing turnarounds at all, add a true multi-angle reference, or train a character LoRA on the octopus form.

**The deepest lesson**: distinguish the two drifts, because they have different fixes. Prompt-dominance drift (a wordy prompt beating the anchor) is fixable by trimming. Reference-gap drift (asking the model to invent an angle the references don't contain) is not — it needs more reference, not a better prompt. Holding is the correct move when the fix you have doesn't match the failure you have.

---

## Phase 7 — the promotion the data killed

The plan was to install the DINOv2 similarity tier and *promote* the Pass-2.5 gate from record-only to a hard pre-Gemini reject. The install (`pip install torch transformers`) surfaced a familiar shape first: the gate still reported `pil-perceptual` even with torch present. transformers 5.x's `AutoImageProcessor` requires **torchvision**, which the documented install command never pulled in; without it the DINOv2 rung raised inside its own try/except and *silently* fell back to PIL. The `SimilarityResult.method` label was the only tell. This is the 2026-05-28 stub-fallback lesson wearing a different coat — a guarded fallback hiding the fact that the real capability never engaged.

With torchvision installed, DINOv2 worked and the regression eval was decisive: recovered scores above drifted on *both* registers, including the mascot register where the PIL tier had inverted (sean 0.838 > 0.755, mascot 0.858 > 0.715). The tier upgrade was real.

Then the promotion died on its own data. Re-scoring the full sean-anchor production bake against the anchor:

```
good plates (Sean-approved):  head-back 0.695 · neutral 0.722 · head-profile-left 0.729 ·
                              surprised 0.740 ... body-profile-right 0.887
drifted references:           sean monochrome 0.755 · mascot chibi-humanoid 0.715
```

The drifted references sit *inside* the good-plate range. A threshold high enough to catch the drift (>0.76) false-rejects `head-back`, `neutral`, `surprised`; a threshold safe enough to keep them (<0.69) catches nothing. DINOv2 separates recovered-from-drifted only *at the same view* — a back-of-head plate is genuinely as far from a front anchor in embedding space as a wrong-character front view is. No blanket threshold against a single front anchor can gate without harming good plates. At the STOP, Sean chose to ship the tier + the regression eval + persisted DINOv2 scores and keep the gate **record-only**, documenting why a hard gate isn't safe yet (it needs per-view references).

**The deepest lesson**: a negative result, fully measured, is a result worth shipping. The honest landing — "the tier is better, the regression eval proves it, and here is precisely why a blanket hard gate would do more harm than good" — beats shipping a gate that false-rejects good plates to satisfy a plan written before the data existed. The plan assumed a clean separation; the measurement showed an overlap; the measurement wins.

---

## Phase 8 — auto-healing the loud guard

The 2026-05-28 session's organizing fix was to make a silent stub into a *loud* failure: when Cy's Pass-1 Opus call returns malformed output, the orchestrator exits non-zero instead of shipping a stub Bible. That was correct, but it left the common transient case — Opus 4.8's chattier disposition occasionally malforming a large structured emission — requiring a human re-run.

Phase 8 wired the auto-heal: `_author_pass1` retries a transient malformed emission (the SDK ran but returned empty or unparseable text) within the three-call budget. It deliberately does *not* retry a missing SDK (`stub_fallback=True` is deterministic — retrying can't help) or a contract violation (parseable JSON missing required keys raises `ValueError` and propagates as a real rejection). The loud guard still fires when all three attempts fail.

**The deepest lesson**: loud-failure and auto-recovery are two stages of the same maturity curve. First you make the failure visible (don't let it ship silently); then, once you understand which instances are transient, you make the transient ones self-heal — without swallowing the deterministic ones, which would put you right back to hiding real failures.

---

## What we learned

The structural takeaways meant to outlive this session.

**The mechanism is a proposal, not a verdict — this is the organizing lesson.** Four times the automated mechanism proposed something wrong and a human read overrode it: the anchor injection proposed drawing a person where a prop belonged; the bake command proposed erasing the approval; Gemini proposed failing ten of the artist's own drawings; the similarity gate proposed rejecting good plates. Each was caught by judgment — reading the code, looking at the plates, reading the data — not by another automated check. This is the project's own philosophy enforced from the inside: agents propose, humans decide. The corollary for the operator is that the STOP gates are not ceremony. Two of them (Phase 4 approval, Phase 5/6 plate review) materially changed what shipped.

**The most dangerous bug is the one that doesn't run.** The plates-only conflict (Phase 4) would have silently destroyed three phases of work on the first bake. It was caught only by reading `CharacterDesignerNode.run` before trusting the plan's `author_bible.py` command. When a plan states both a command and an invariant, confirm the code can honor both before executing — internal contradictions in a plan are real and they exit zero in your head.

**Silent fallback hides the real capability — again.** torchvision-missing → DINOv2 silently degrades to PIL is the exact shape of 2026-05-28's stub-fallback lesson. The `method` label was the tell, the same way the "(STUB FALLBACK)" sentinel was. Any graceful-degradation ladder needs a visible signal of *which rung actually ran*, or "it's installed" silently means "it's not engaged."

**Distinguish prompt-dominance drift from reference-gap drift.** They look identical from the outside (a plate that doesn't look like the character) and have opposite fixes. `focused` went monochrome because a wordy prompt beat the anchor — fixed by trimming. The mascot turnarounds went humanoid because the anchor has no standing pose — *not* fixed by trimming; it needs more reference. Misdiagnosing the second as the first wastes re-rolls and erodes confidence in a mechanism that's actually working.

**A centralized fix holds only where its competing inputs stay quiet.** Moving framing into the runner closed the fidelity gap, but the plate prompts the runner wraps were never re-authored, so a loud-enough plate prompt still won (`focused`). The passing expression plates carry the same latent prose and got lucky. Centralization reduces the surface; it doesn't eliminate it. Finish the job by quieting the inputs too.

**Automated verdicts mislead at the edges; the eye is the arbiter at the edges.** Gemini gated 12 plates; 10 were noise (ingests of Sean's own art, small-crop skepticism). A reviewer trusting the gate count would have concluded the bake failed. The visual review found one real drifter and a clean win. The engine truth — "recognizably itself in its intended medium" — is a human judgment by construction, and the automated gates are inputs to it, not substitutes for it.

**Approval must be enforceable, not conventional.** The whole "approve → bake" flow rested on an honor system until Phase 4a made the lock *route* the bake. A locked Bible now structurally cannot be re-authored. Conventions that depend on everyone remembering the rule are bugs waiting for the one run that forgets.

**Negative results ship.** Phase 7's hard-gate promotion was the plan; the data said no; shipping the tier + the eval + the documented "why not" is the correct landing. Don't ship a worse gate to honor a pre-data plan.

---

## How to proceed

In rough priority order, carrying the findings forward:

1. **The mascot dedicated pass.** The reference gap is the blocker, not the prompt. Decide whether a legless creature needs standing `body-3quarter`/`body-back` turnarounds at all; if it does, author a true multi-angle (or seated/crouched-from-angles) octopus reference, or train a character LoRA on the octopus form (the Bible's `flux_lora_seed_plates` field anticipates this). The cheap re-rolls (`surprised` background, `head-front` snout) are worth doing in the same pass. Evidence is staged in `docs/anima-test-runs/2026-05-29-mascot-rebake-hold/`.

2. **Trim the remaining sean-anchor expression prompts.** `neutral`, `surprised`, `contemplative` carry the same monochrome-era verbose prose that drifted `focused`; they passed this bake but they are latent prompt-dominance risk. Trim them to short intent now, while it's cheap, rather than after a future re-bake drifts one of them.

3. **A per-view-reference hard gate.** This is the real fix the Phase 7 data points to: score a plate against a *same-view* reference instead of the single front anchor. It's a design change (the Bible would need per-view reference plates, or the gate would need to pick the nearest-angle reference) beyond this session's scope, but it's the only way the gate becomes a trustworthy hard reject. Until then, record-only + the human eye is correct.

4. **Sean-anchor identity tuning.** The generated faces lean a touch more realistic than the round-cartoon anchor — shipped knowingly, logged as `cy-confidence-notes.md` §6. A future tuning pass (a "rounder cartoon proportions" prompt nudge, or the same LoRA approach) should pull them back toward the anchor's register.

5. **Em's closing-the-loop (case 7), still xfailed.** Unchanged from the prior handoff: it flips green when Em loads the merged CriteriaBundle's `IR.*` entries at run start. With two registers' worth of locked, baked Bibles now on disk (sean-anchor fully; mascot's rules locked, plates pending its pass), Em citing an `IR.sean.prop.stylus-right-hand-always` or an `IR.claude-mascot.style.integer-pixel-grid-no-subpixel` violation against a Phase 5 frame is the next operational milestone.

---

## What landed on disk

| Commit | What | Phase |
|--------|------|-------|
| `8d17c1f` | prop plates are isolated objects — no anchor, no identity gate, no caption | 1 |
| `ba1815f` | body turnarounds use Sean's hand-trimmed crops; tighten head-front box | 2 |
| `214f22b` | plates-only bake mode — bake against an approved Bible, no re-author | 4a |
| `bde0258` | full-color doc consistency + approve sean-anchor Bible (22 rules, v1.2, locked) | 4 |
| `e8f4c92` | bake sean-anchor production plates (focused + stylus re-rolled) | 5 |
| `7c548ab` | hold claude-mascot re-bake; document the reference-gap finding | 6 |
| `5f0e61c` | DINOv2 similarity tier + regression eval; gate stays record-only | 7 |
| `c11f92f` | Cy Pass-1 retry-on-parse-failure | 8 |
| `d95fdbf` | CLAUDE.md + CHANGELOG wrap | 9 |

Test suite: 176 → **187 passing**, green before and after every commit; green with *and* without torch installed (the regression eval skips, the PIL-specific tests force their tier). `.venv` grew ~2GB (torch + torchvision + transformers — torchvision the silently-required piece). Live spend: two plates-only bakes (sean-anchor full, mascot full) + a two-plate re-roll, all NB Pro + Gemini, no Opus (plates-only skips Pass 1) — roughly $3–5.

The receipts: one new mechanism contract (prop plates), one new enforceable safety property (plates-only against a locked Bible), one recognizable full-color sean-anchor plate set baked against an approved Bible, one honestly-held mascot with its reference gap documented, one trustworthy-where-it's-trustworthy similarity tier with the eval that bounds it, and one auto-heal that retires a manual re-run. The pipeline didn't get a clean win on everything it touched — it got an *honest* result on everything it touched, which is the harder and more durable thing.

*Engine truth: the character must be "recognizably itself in its intended medium." Sean reads as Sean, in full color, in the pencil-test register, baked against rules he approved. The mascot reads as the octopus where the anchor could carry it and as a gingerbread man where it couldn't — and we said so out loud instead of shipping the gingerbread man. — filed 2026-05-30*
