# Seedance Generation Phase — Execution Kickoff

> Paste everything below the divider into a fresh Claude Code thread in this repo. **Do NOT enter plan mode** — the plan is locked. Execution begins immediately at Task 1.

---

You are kicking off the **Seedance Generation Phase** of the Act 2 pencil-test animation pipeline. The full 12-task implementation plan was written, approved, and committed on `8a0d64e` of branch `ultraplan/seedance-pipeline`. Your job is to **execute** it task-by-task to deliver a watchable Act 2 video.

**Mode:** Execution, not planning. The plan resolves all 12 architectural decisions with explicit justification — do not redesign, re-litigate, or re-plan. If you find a case the plan doesn't cover, **ask the user** rather than assume.

**Read these first, in this order. Do not skim.**

1. `CLAUDE.md` — project manual + the **Maintenance Conventions** section (CHANGELOG.md updated on every change; CLAUDE.md on significant ones; COMPLETED/OLD archive convention)
2. **`docs/2026-04-27-act2-seedance-execution-plan.md`** — THE plan you are executing. End-to-end before any tool call.
3. `docs/act2-seedance-shot-list.md` — the spec the plan implements (10 Seedance clips + 4 holds + 3 hard cuts → ~50s)
4. `docs/seedance-research-findings.md` — Seedance API reference, prompting rules, known failure modes
5. `runs/act2-exploration/round3-audit.md` — anchor audit (gives per-shot risk context)

<project_context>
This is a manifest-driven 2D pencil-test animation pipeline. Hand-drawn graphite character on cream paper #FAF5E8. **Act 1 ships.** Act 2 has been in pre-production through Round 1 (concepts) → Round 2 (beat sheet) → Round 3 (production anchors + shot list). All 15 production anchor frames are locked (700KB–1MB each, validated on disk). This phase converts those anchors into a watchable ~50s Act 2 MP4 via Seedance interpolation + NB2 cleanup + FFmpeg assembly. The aesthetic is non-negotiable: traditional pencil test on cream animation paper; if it looks digital, anime, vector-clean, or photorealistic, it has failed.

The pipeline philosophy locked in by the plan: **Seedance finds the motion, NB2 protects the aesthetic.** Two-engine pipeline, ~50/50 cost split: Seedance ~$10 for motion intelligence; NB2 ~$10 for aesthetic restoration at Tier A+B.
</project_context>

<execution_mode>
**REQUIRED SUB-SKILL:** Use `superpowers:subagent-driven-development` (recommended per the plan's frontmatter) — fresh subagent per task, two-stage review between tasks, fast iteration, protects the main context window. Alternative: `superpowers:executing-plans` for inline batch execution if you prefer a single-thread flow.

**Tracking:** Use `TodoWrite` to mirror the 12 tasks. Mark each task `in_progress` before starting; mark `completed` only after every checkbox in that task is done AND the human gate (if any) has passed.

**Human gates are HARD gates.** When the plan says "HUMAN GATE" — STOP and wait for explicit user approval before proceeding. Do not auto-proceed assuming pass. The hard gates are:
- Task 3.4 (T2 visual review — first Seedance test)
- Task 4.3 (batch inspection — 9 more Seedance clips)
- Task 6.3 (M1 rough-cut milestone — single highest-leverage QA gate)
- Task 8.3 (T2 cleanup review — first NB2 pass)
- Task 8.4 (full cleanup batch authorization)
- Task 10.1 (Procreate manual step — user does this off-pipeline)
- Task 11.3 (M2 final milestone)

Real money is being spent (~$20 budget). A wrong autodecision wastes $5–10 on the next batch.

**Procreate step is an absolute hard gate (Task 10).** The assembly script in `--full` mode MUST error out with clear instructions if `runs/{run_id}/manual_panorama_cleaned.png` is absent. Do NOT bypass it. Do NOT generate a substitute via NB2 — the panorama's brand-label glitches require human Procreate work.
</execution_mode>

<your_first_task>
**Start with Task 1 from `docs/2026-04-27-act2-seedance-execution-plan.md`:** freeze the shot list as `pipeline/seedance_shotlist.yaml`. The full sub-step spec (1.1 → 1.5) lives in the plan. Mirror the schema exactly — top-level `version` / `created` / `style_anchor`; arrays for `shots[]` (10 entries), `holds[]` (4 entries), `hard_cuts[]` (3 pairs), and `assembly_order` (14 IDs in order).

After Task 1 commits, proceed to Task 2 (build `pipeline/seedance_lib.py`). The library helpers in Task 2 are dependencies for everything that follows — do NOT skip to Task 3.

Once Task 2 commits, Task 3 is the test-shot run (T2 sync, ~$0.72, ~2 min). Stop at the human gate (3.4) and wait for the user's go/no-go before continuing to batch.
</your_first_task>

<key_file_paths>
| What | Path |
|---|---|
| Project manual + Maintenance Conventions | `CLAUDE.md` |
| **THE plan you are executing** | `docs/2026-04-27-act2-seedance-execution-plan.md` |
| Shot list spec (source for shotlist.yaml) | `docs/act2-seedance-shot-list.md` |
| Seedance API + prompting reference | `docs/seedance-research-findings.md` |
| Round 3 anchor audit (per-shot risk) | `runs/act2-exploration/round3-audit.md` |
| Round 2 locked beat sheet | `runs/act2-exploration/concepts/round2-decisions.md` |
| 11 production anchor frames | `runs/act2-exploration/concepts/{zone1,zone3,zone4}/` |
| 4 NEW bridge anchors | `runs/act2-exploration/concepts/bridges/` |
| A-2 identity anchor | `images/2D-Character-Sketch-Sean-v1.png` |
| AI companion turnaround | `runs/act2-exploration/concepts/companion/turnaround_02.png` |
| RPG sprite turnaround (Act 1 panorama Easter egg) | `runs/run_2026-04-04_174805/candidates/sprite/turnaround_01.png` |
| NB2 generation script (invoked by cleanup loop) | `.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py` |
| Existing orchestrator (architectural reference, do NOT modify) | `pipeline/generate.py` |
| Existing audit script (markdown template reference at lines 52–82) | `pipeline/audit.py` |
| Existing assembly script (FFmpeg patterns + JPEG-as-PNG fix at 159–164) | `pipeline/assemble.sh` |
| Archived Act 1 keyframe prompts | `docs/COMPLETED/act1-keyframe-prompts.md` |
| Archived legacy Seedance plan (do NOT use) | `docs/OLD/seedance-production-plan.md` |
| API keys | `.env` (`GEMINI_API_KEY` + `FAL_KEY`) |
</key_file_paths>

<project_rules priority="critical">
- **Identity match to A-2 is the #1 requirement.** Sean must be immediately recognizable in every visible frame of the final cut. If Seedance breaks identity at any point in a clip, invoke that shot's documented fallback strategy (per shot list) — do NOT settle for "good enough."
- **Hand-drawn pencil aesthetic on cream paper #FAF5E8.** Every visible frame must look like the same animator drew it on the same paper. NB2 cleanup is mandatory wherever Seedance drifts toward digital cleanness.
- **The universal cleanup prompt is verbatim, every shot.** Do NOT write per-shot variants. The 10 explicit negatives (no vector lines, no black outlines, no cel shading, no anime, no saturation, no digital painting, no gradients, no airbrush, no pure white BG, no pure black lines) are mandatory.
- **Tier A+B is the M2 default** (user-confirmed). Do NOT default to Tier C; only escalate to Tier C for a specific shot if M2 review shows visible flicker at that boundary.
- **No premature scope expansion.** Only the 7 new files from the plan get created (`seedance_shotlist.yaml`, `seedance_lib.py`, `seedance_generate.py`, `seedance_extract.py`, `seedance_cleanup.py`, `seedance_audit.py`, `seedance_assemble.sh`). The existing pipeline scripts (`generate.py`, `audit.py`, `assemble.sh`) are READ for reference, never modified.
- **Act 1 is locked.** Hero loop ships as-is. Do not regenerate, modify, or re-audit Act 1 content. The Act 1 prompts now live at `prompts/COMPLETED/F##.txt`.
- **`runs/` is gitignored.** Commit pipeline scripts and configs (e.g. `seedance_shotlist.yaml`); never force-add MP4s, extracted PNG sequences, or per-run audit outputs.
- **Maintenance Conventions apply** (per CLAUDE.md): every code/doc/config change appends a CHANGELOG.md entry capturing what + why; significant project-state changes update CLAUDE.md. Don't batch CHANGELOG updates at the end — append during each commit.
- **Stylus is NOT in Sean's hand in Act 2.** The "stylus in right hand" rule from Act 1 does NOT apply — Sean's hands are on the keyboard, reaching, or empty. The stylus visible on the desk in `transition_pulled_in.png` and `pre_pulled_in.png` is an incidental desk prop. Do not inherit the Act 1 rule into Seedance prompts.
- **Use the right skills:** `prompt-engineering` for any new prompt text (universal cleanup template, T1 cursor variants); `creative-director` for QA gate decisions on Seedance output; `video-animation-production` for FFmpeg patterns; `gemini-pencil-animation-image-gen` for NB2 calls (invoked via the cleanup loop's subprocess).
</project_rules>

<known_persistent_issues>
- **Panorama brand-label glitches** in `zone4/final_panorama_v3_a.png` ("ANTHROPIC" duplicated, "AGENT HARNESS"/"AGENT USE"/"TOOL" garbled). Accepted for Procreate cleanup — do NOT iterate against NB2. The PB shot uses the dirty panorama as end anchor (camera pull-back masks the labels); FIN uses the user's manually-cleaned export.
- **NB2 returns JPEG bytes with `.png` extension.** FFmpeg silently drops these as input — every NB2 cleanup output MUST be re-encoded via `seedance_lib.reencode_to_png()` (built in Task 2.1) before any FFmpeg ingestion. This is non-negotiable; the failure is silent and produces broken concat output.
- **`audit.py` writes review prompts to stdout, not disk** ([pipeline/audit.py:52-82](pipeline/audit.py#L52-L82)). The new `seedance_audit.py` (Task 7) MUST write `audit/qa_{shot}.md` directly to disk — depart from `audit.py`'s I/O pattern. Mirror the *content* of the gate framing, not the I/O.
- **Seedance end-frame is approximate** per the research findings — generated final frame won't match end anchor pixel-exact. QA tolerance is SSIM ≥ 0.6, not equality.
- **Seedance identity erosion** — accessories erode first; clips >6s amplify it. Stay at 3–5s per clip per the locked shot list. Do NOT increase any clip's duration to "fix" something else.
- **Texture crawl risk** — cream paper grain may shift on long static-content shots. Plan mitigates FIN by using FFmpeg Ken Burns instead of Seedance; if texture crawl appears on any other clip, that's a fallback trigger.
- **NB2 word swaps** ("Anthropic" → "Achibic", "AI AGENTS RUN WORKFLOWS" → "AI GEMINI RUN WORKFLOWS"). Catch them in QA but do not loop on regen — Procreate fix at compositing.
- **Stubble continuity** — Sean is CLEAN-SHAVEN in W1/W2/W3 (walking sequence) and gains 5-o'clock shadow at S0 onward (desk sequence). The S0 Seedance prompt grows it in. Do NOT re-introduce stubble into walking-sequence Seedance prompts; do NOT remove stubble from desk-sequence prompts.
- **fal.ai content filters** are aggressive on realistic faces but should not affect us — pencil drawings, not photographs.
</known_persistent_issues>

<budget_expectations>
| Milestone | Wall-clock | $ Cost |
|---|---|---|
| **M1 — rough cut** (Seedance + extract + naive assembly) | ~40 min | ~$10 |
| **M2 — full-fidelity cut** (M1 + Tier A+B cleanup + Procreate + final assembly) | ~3 hr | ~$20 total |
| Worst-case (Tier C escalation per-shot) | ~6–8 hr | ~$60 |

**Stop and confirm with the user before each of these spend points:**
- Running the `--all` Seedance batch (Task 4) — locks in ~$8–9
- Running `--all` cleanup at Tier A+B (Task 8.4) — locks in ~$10
- Escalating to Standard tier OR Tier C (any per-shot rerun under fallback)

**Do not silently exceed $25 cumulative without explicit approval.** Track running cost in `audit/run_summary.json` and surface it at each gate.
</budget_expectations>

<reasoning>
Approach in this order:

1. **Read the plan end-to-end before any tool call.** All 12 decisions are resolved; do not re-litigate. If something genuinely seems wrong (not aesthetic preference), ASK before deviating.
2. **Use `superpowers:subagent-driven-development`** as the primary execution sub-skill. Fresh subagent per task with the relevant slice of context; you review between tasks. Protects context window and gets independent eyes on each task's output.
3. **Test-shot first (Task 3, T2 sync mode).** This is the single highest-leverage validation in the plan: locked camera, single element materializes, gold-standard anchors. If T2 fails identity or aesthetic at Fast tier, the whole approach needs rethinking — surface to the user immediately rather than batching 9 more clips that will also fail.
4. **M1 before M2 is non-negotiable.** The rough cut (Task 6) is the cheapest QA gate: timing, pacing, hard-cut placement, and obviously-broken Seedance clips all surface here. Skipping M1 to "save time" risks burning $10 of cleanup on broken source frames.
5. **Append CHANGELOG.md entries per commit, not at the end.** Each numbered task in the plan ends with "Commit." — that's a real commit boundary. Add the CHANGELOG entry as part of each commit (per Maintenance Conventions). Helps the user roll back precisely if something breaks downstream.
6. **Documented fallback strategies are the playbook for failure.** When a Seedance retry fails its 2nd attempt on a high-risk shot (S0, REV, PB), invoke the documented fallback from the shot list — do NOT invent new fallbacks. Specifically: S0 → hard cut + 0.3s cross-fade in FFmpeg post; REV → split into REV1/REV2 with intermediate `bridges/being_pulled.png` (would require generating that bridge — surface to user); PB → hard cut + 0.4s cross-fade.
7. **Move this kickoff prompt to `prompts/COMPLETED/` once Task 12 ships.** Per the archive convention, this prompt is "active" only while execution is in flight; on completion it joins the other shipped handoffs.
</reasoning>
