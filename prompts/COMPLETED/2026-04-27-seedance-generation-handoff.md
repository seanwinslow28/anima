# Seedance Generation Phase — Continuation Session Prompt (Plan Mode)

> Copy everything below the divider into a fresh Claude Code thread in this repo, then hit `/plan` (or shift-tab into plan mode) BEFORE the assistant takes its first action. The goal of that session is to **plan** the Seedance generation phase, not execute it. After the plan is written and approved, you'll exit plan mode and either execute in that session or hand it off again.

---

You are entering **Plan mode** to design the Seedance Generation phase of the Act 2 pencil-test animation pipeline. Round 3 (production anchor frames + shot list) just shipped on commit `84ffa9d` of branch `ultraplan/seedance-pipeline`. Every anchor frame Seedance needs already exists. Your job is to plan how to turn those anchor frames into 10 generated Seedance clips, extract usable frames, restore pencil-test fidelity where Seedance drifts, and assemble the final ~50-second Act 2 video.

**Read these first to anchor yourself.** Read all four — do not skim.

1. `CLAUDE.md` — full project manual, pipeline architecture, naming conventions, QA gate codes
2. `docs/act2-seedance-shot-list.md` — **THE SPEC for this phase.** 10 Seedance clips + 4 holds + 3 hard cuts, with anchor frame paths, draft 60-100 word Seedance prompts, durations, fallback strategies, and assembly order
3. `docs/seedance-research-findings.md` — Seedance 2.0 API specs, fal.ai params, pricing, prompting rules (60-100 words, single camera move, "fixed camera locked tripod", style anchors), known failure modes (texture crawl, identity drift, feature erosion)
4. `runs/act2-exploration/round3-audit.md` — context on which anchors are production-fidelity vs which carry known caveats (panorama brand-label glitches accepted for Procreate cleanup)

<project_context>
This is a manifest-driven 2D pencil-test animation pipeline. The hero piece is a portfolio animation: hand-drawn graphite character on cream paper #FAF5E8. Act 1 (the hero loop) is complete. Act 2 has just completed pre-production: an 11-beat sheet locked in Round 2 (`runs/act2-exploration/concepts/round2-decisions.md`), production anchor frames audited and generated in Round 3, and a Seedance shot list written.

The aesthetic is non-negotiable: traditional pencil test on cream animation paper, hand-drawn graphite lines with construction marks visible, cross-hatching for shading, hand-lettered text, and a slightly stylized 7–7.5-head character design. If anything starts looking digital, anime, vector-clean, or photorealistic, it has failed.

Three character references already exist:
- **Sean (the protagonist):** A-2 anchor at `images/2D-Character-Sketch-Sean-v1.png`
- **AI Companion:** terracotta-orange loaf creature, dot eyes, stubby arms (turnaround: `runs/act2-exploration/concepts/companion/turnaround_02.png`)
- **RPG Warrior Sprite:** chibi warrior from Act 1 (turnaround: `runs/run_2026-04-04_174805/candidates/sprite/turnaround_01.png`)

The Seedance research has already been done (the docs are real and tested — Seedance 2.0 is live on fal.ai as of April 2026). The shot list has draft Seedance prompts ready to use. Your job is to figure out HOW to run them at scale, not to redo the prompt engineering.
</project_context>

<current_status>
**Anchor frames complete (15 total):**
- 11 locked Round 2 concepts (10 PASS audit + 1 regenerated this commit) under `runs/act2-exploration/concepts/zone{1,3,4}/`
- 4 NEW bridge/transition anchors under `runs/act2-exploration/concepts/bridges/`

**Shot list locked:**
- 10 Seedance interpolation clips (W1, W2, W3, S0, T0, T2, TR, REV, PM, PB)
- 4 FFmpeg holds (S1, T1, T3, FIN)
- 3 hard cuts (T2→T3, T3→TR, REV→PM)
- ~50s total runtime
- Estimated cost: $10–12 on fal.ai Fast tier, $12–15 on Standard tier

**Pipeline tooling that already exists:**
- `pipeline/generate.py` — orchestrates NB2 keyframe generation (NOT Seedance; can be used as architectural reference)
- `pipeline/audit.py` — runs HF/SF QA gates on generated frames (NB2 keyframes; logic mostly portable)
- `pipeline/assemble.sh` — FFmpeg assembly for the Act 1 hero loop
- `.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py` — single-image NB2 generation (used for the anchor frames; reusable for any NB2 cleanup pass)
- `.env` already contains `GEMINI_API_KEY` AND `FAL_KEY`
- `pip install fal-client` — already in dependencies per CLAUDE.md

**What does NOT exist yet (likely deliverables of this plan):**
- Any Seedance orchestration script
- Any Act 2 run directory under `runs/`
- Any frame-extraction automation
- Any NB2 cleanup loop for restoring extracted frames
- Any Act 2 assembly script (Act 1's `assemble.sh` is single-loop; Act 2 is a sequence with cuts)
</current_status>

<your_first_task priority="planning">
**Plan the Seedance Generation phase end-to-end.** The plan should take the project from "15 anchor frames + shot list" to "playable Act 2 video file in a chosen format (GIF/WebM/MP4)."

The plan must explicitly resolve every decision below — not by asking the user mid-execution, but by making and justifying a recommendation now (the user will course-correct if they disagree).

**Decision points the plan must address:**

1. **Test-shot strategy.** Seedance research recommends: "Test with Fast tier at 480p/4s first, scale up after validating aesthetic." Which one Seedance shot is the lowest-risk highest-information test (likely T2 — locked camera, single element materializes)? After the test passes, what's the rollout plan to the other 9 clips?

2. **Frame hosting for the Seedance API.** fal.ai's `image_url` and `end_image_url` accept either a hosted URL or base64. Base64 is simpler (no hosting infra), but anchor PNGs are 700KB–6MB each. Decide: base64 inline, upload to fal storage once and reuse, or push to a temporary bucket. Justify based on cost/complexity.

3. **Orchestration architecture.** Build a new `pipeline/seedance_generate.py` orchestrator (reads shot list, generates all 10 clips, logs status) OR run shots ad-hoc via individual python invocations? If the orchestrator: synchronous (`fal_client.subscribe`, blocks 60–180s per clip) or async batch (`fal_client.submit` + poll)? Sequential or parallel?

4. **Audio.** `generate_audio` defaults to `true`. The Act 2 video has no diegetic audio in scope (music will be added in post). Should we explicitly set `generate_audio: false` to save cost/time? Per the research, it's "included at no extra cost" — but check whether disabling improves generation latency.

5. **Output directory structure.** Where do Seedance MP4s land? Where do extracted PNG frames land? Where do NB2-restored frames land? Where do final assembled segments land? Propose a directory layout under `runs/act2-seedance/` consistent with the existing `runs/{run_id}/` pattern in CLAUDE.md.

6. **Frame extraction.** FFmpeg `-vf fps=12` per the existing pattern in CLAUDE.md. Run per-clip as part of the orchestrator, or as a separate batch step after all clips are generated? Note: Seedance outputs at 24fps; we extract at 12fps to match the 12fps target frame rate.

7. **NB2 cleanup loop.** This is the trickiest part of the plan. Seedance preserves identity decently but degrades style/line confidence. Per the project philosophy "Seedance finds the motion, NB2 protects the aesthetic" — extracted frames need NB2 restoration to bring them back to pencil-test fidelity. Decide:
   - Which extracted frames need cleanup? All? Every Nth? Only frames that fail an automated style audit? Manual visual review?
   - What's the cleanup prompt template? Per-shot or universal?
   - What references go into the cleanup pass (anchor frames? the extracted frame itself?)?
   - Cost implication — NB2 cleanup at scale could be 10×–100× the Seedance cost

8. **Procreate cleanup gating.** The final panorama (`final_panorama_v3_a.png`) has known NB2 brand-label glitches that must be cleaned up in Procreate (manual step) BEFORE the FIN shot's Ken Burns pan can render. When does this manual step happen in the pipeline? Does the assembly stop and wait, or proceed in parallel with the user doing Procreate work?

9. **Hard cuts and holds — assembly only, no Seedance.** Three shots are hard cuts (T2→T3, T3→TR, REV→PM); four shots are FFmpeg holds (S1, T1, T3, FIN). T1 specifically needs a custom blinking-cursor overlay built from two variant frames. Plan the assembly script that stitches Seedance MP4s + holds + cross-fades-on-cuts into a single Act 2 video.

10. **QA gate enforcement.** The shot list defines 8 verification gates per Seedance clip (identity, style, continuity, wardrobe, companion design, no texture crawl, no jitter, end-frame match). Are these enforced automatically (script + Claude vision audit), manually (human review per clip), or hybrid? What triggers a fallback strategy invocation (1st failure auto-retry, 2nd failure invoke documented fallback)?

11. **Phase boundary.** Does this plan stop at "all 10 Seedance clips generated + extracted + NB2-cleaned" (handoff to a separate assembly plan), or include the FFmpeg assembly through to a watchable Act 2 MP4? Propose and justify.

12. **Cost & time budget.** Estimated wall-clock time for one full pass (sequential vs parallel). Estimated dollar cost (Seedance + NB2 cleanup). What gets the user to a first watchable rough cut fastest?

**Plan deliverable shape:**
- One markdown plan file (`docs/superpowers/plans/...` or wherever your plan-mode skill writes plans)
- Should include: Context, Deliverables, Decision Resolutions (covering all 12 above), Critical Files (created/modified), Execution Order, Verification, Out-of-Scope
- Should NOT include: actually running Seedance, generating outputs, or modifying shot prompts (those belong to execution, not planning)

When the plan is written, exit plan mode and stop — let the user decide whether to execute in that session or open a new one.
</your_first_task>

<key_file_paths>
| What | Path |
|------|------|
| Project manual | `CLAUDE.md` |
| THE SPEC for this phase | `docs/act2-seedance-shot-list.md` |
| Seedance API + prompting reference | `docs/seedance-research-findings.md` |
| Anchor frame audit | `runs/act2-exploration/round3-audit.md` |
| Locked Round 2 beat sheet | `runs/act2-exploration/concepts/round2-decisions.md` |
| Round 3 plan (just shipped) | `/Users/seanwinslow/.claude/plans/yes-please-plan-out-warm-kahan.md` |
| Round 2/3 anchor frames | `runs/act2-exploration/concepts/zone{1,3,4}/` and `runs/act2-exploration/concepts/bridges/` |
| A-2 character anchor | `images/2D-Character-Sketch-Sean-v1.png` |
| AI companion turnaround | `runs/act2-exploration/concepts/companion/turnaround_02.png` |
| RPG sprite turnaround (Act 1 Easter egg in panorama) | `runs/run_2026-04-04_174805/candidates/sprite/turnaround_01.png` |
| Existing NB2 generation script | `.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py` |
| Existing NB2 orchestrator (architectural reference) | `pipeline/generate.py` |
| Existing audit script (architectural reference) | `pipeline/audit.py` |
| Existing assembly script (Act 1 single-loop reference) | `pipeline/assemble.sh` |
| API keys | `.env` (GEMINI_API_KEY + FAL_KEY) |
| Previous handoff format reference | `prompts/act2-continuation-handoff.md` |
</key_file_paths>

<known_persistent_issues>
- **NB2 brand-label glitches:** "Anthropic" duplicates, "AGENT HARNESS" / "AGENT USE" / "TOOL" oddities in `final_panorama_v3_a.png`. After ~3 iterations the user accepted these will be cleaned up in Procreate during compositing rather than continuing to iterate against NB2. Same pattern applies to any extracted Seedance frame that has similar text-area distortion — flag for Procreate, don't loop on regen.
- **NB2 word swaps:** NB2 occasionally swaps requested words ("AI AGENTS RUN WORKFLOWS" → "AI GEMINI RUN WORKFLOWS"; "Anthropic" → "Achibic" in the regenerated `ai_discovery.png`). Worth catching but not a blocker for Seedance work.
- **Seedance end-frame is approximate** (per research findings): the generated final frame won't match the end anchor exactly. Plan QA around this — comparing extracted last frame to anchor with some tolerance, not pixel-exact.
- **Seedance identity erosion:** accessories (the stylus from Act 1, the companion's small features) erode first. Clips >6s amplify this. Stay at 3–5s per clip.
- **Texture crawl risk:** cream paper grain may shift/move despite being static background. The shot list already calls this out for FIN (uses Ken Burns pan in FFmpeg post instead of Seedance). Watch for it on any 5s clip.
- **"Stylus in right hand" rule (Act 1 inheritance):** Sean does NOT hold a stylus in any Act 2 shot — his hands are on the keyboard, reaching, or empty. Don't reintroduce this Act 1 rule into Act 2 prompts. The pencil/stylus visible on the desk in `transition_pulled_in.png` and `pre_pulled_in.png` is an incidental desk prop, not in his hand.
- **fal.ai content filters** are aggressive on realistic faces (per research) but should not affect us — our inputs are pencil drawings, not photographs.
- **Stubble continuity:** Sean is CLEAN-SHAVEN in W1, W2, W3 (walking sequence). He has subtle 5-o'clock shadow STARTING at S0 (arrive at desk) and onward. The S0 Seedance clip should show stubble growing in. Don't accidentally introduce stubble into walking-sequence Seedance prompts.
</known_persistent_issues>

<project_rules priority="critical">
- **Identity match to A-2 is the #1 requirement.** Sean must be immediately recognizable in every extracted/cleaned frame. If Seedance breaks identity at any point in a clip, that clip needs a fallback strategy invoked (per shot-list documentation), not a "good enough" pass.
- **Hand-drawn pencil aesthetic on cream paper.** Every extracted frame must look like it was drawn by the same animator on the same paper. NB2 cleanup is mandatory wherever Seedance drifts toward digital cleanness.
- **The 10 explicit negatives** must be in every NB2 cleanup prompt: no vector lines, no black outlines, no cel shading, no anime, no saturation, no digital painting, no gradients, no airbrush, no pure white BG, no pure black lines.
- **Use the prompt-engineering skill** when writing NB2 cleanup prompt templates. Use the **creative-director skill** when auditing Seedance output for QA gate decisions. Use the **video-animation-production skill** for FFmpeg patterns.
- **No premature scope expansion.** This is the Seedance generation phase, not "rebuild the whole pipeline." Reuse `pipeline/generate.py` and `pipeline/audit.py` patterns where they fit; only introduce new infrastructure where the Seedance phase genuinely needs it.
- **Act 1 frames are locked.** Do not regenerate, modify, or re-audit Act 1. The Act 1 hero loop ships as-is.
- **runs/ is gitignored.** Plan how to handle this — same pattern as Round 2/3 (force-add only the planning docs and prompt files; don't commit large MP4s or PNGs unless explicitly requested).
</project_rules>

<reasoning>
Approach the planning in this order:

1. **Read the four anchoring docs in full** before opening any tool. The shot list is THE spec — all 12 decisions trace back to it.
2. **Use Explore subagents in parallel** to answer specific factual questions: what does the existing `pipeline/generate.py` orchestration look like, how does `pipeline/assemble.sh` build the Act 1 video, what are the actual file sizes of the anchor frames (informs the base64-vs-hosted decision), what does `pipeline/audit.py` use for vision audit (informs the QA gate decision).
3. **Use a Plan subagent** to draft the implementation approach, then review and tighten before writing the final plan.
4. **Make recommendations, don't ask the user 12 questions.** The user wants decisions with justification — they'll override what they don't like. Use AskUserQuestion only for the 1–2 highest-leverage forks (e.g., phase boundary: Seedance-only vs Seedance-through-assembly) where the answer fundamentally reshapes the plan.
5. **The riskiest part is the NB2 cleanup loop.** If you skim that decision, the plan will fail at execution. Spend the most thinking on item 7.
6. **Check costs explicitly.** Seedance Fast tier is ~$10–12 for the full batch. NB2 cleanup at scale could be 10×–100× that. The plan must give the user a realistic cost number for first-pass-rough vs full-fidelity.
7. **Use ExitPlanMode** to request plan approval — don't ask in text.
</reasoning>
