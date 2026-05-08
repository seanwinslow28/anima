# Act 1 Finishing Plan — Seedance + NB2 Cleanup Kickoff Prompt

**Use this prompt to start a fresh Claude Code session in plan mode.**
The next session's job is to produce a written implementation plan — NOT to run scripts or generate frames. After review and approval, plan execution will happen in a follow-up session.

---

<role>
You are an animation pipeline planner for the **Pencil Test** portfolio project. Your output for this session is a written implementation plan, structured for review and approval. You will not generate frames, run shell commands, or call APIs in this session. Plan mode is active.
</role>

<project_context>
This is a 2D pencil-test animation portfolio piece on cream production paper. Act 1 is a 42-frame hero loop at 12fps. The pipeline philosophy (see `CLAUDE.md` → "Seedance Pipeline (Phase B.5)") is:

> **Seedance finds the motion, NB2 protects the aesthetic.**

Seedance 2.0 (fal.ai/bytedance) interpolates between approved NB2 anchor keyframes to generate fluid motion video. We then extract individual frames, cherry-pick the best ones for timing and arcs, and redraw them with Nano Banana 2 (Gemini) to restore the cream-paper pencil-test aesthetic before assembly.

Act 1 was originally finished as keyframe-only at 42 frames with FFmpeg holds + ComfyUI/DWPose in-betweens. A Seedance test pass was later run across the full Act 1 anchor chain to explore fluid interpolation. The user has now decided to **incorporate selected Seedance frames into the final Act 1** to combine the best of both worlds before shipping.
</project_context>

<must_read_first>
Read these in order before planning. Do not skip.

1. `CLAUDE.md` — full project manual, especially the **Seedance Pipeline (Phase B.5)** section and the **Engine Truth** at the bottom.
2. `docs/production-checklist.md` — Act 1 status, phase-by-phase. Note especially the "Remaining Work" sections under Phase 4 (compositing) and the unchecked items: sprite fade F38–F41, pencil trail effect, final export, ship to portfolio.
3. `docs/pencil-test-storyboard.md` — beat structure and intent for each frame range.
4. `docs/seedance-research-findings.md` — Seedance prompting rules, 60–80 word action-focused budget, "stylus in right hand" / "fixed camera, locked tripod" musts.
5. `manifest.yaml` — frame timing (hold durations) and audit gates (HF01–HF05, SF01–SF05).
6. `runs/run_2026-04-04_174805/manifest.lock.yaml` — frozen config for the active run.

Then survey the actual assets you'll be working with:

- `runs/run_2026-04-04_174805/approved/` — 30 files. NB2 keyframes (`PT_A1_F##_key.png`) + ComfyUI in-betweens (`PT_A1_F##toF##_IB##.png`). 16:9, ~1280×720.
- `runs/run_2026-04-04_174805/export/seedance-2.0-output/Act-1-Test-Seedance-2.0.mp4` — 6.04s, 1280×720, **24fps**, 145 frames.
- `runs/run_2026-04-04_174805/export/pencil-test-act1.mp4` — current Act 1 hero loop (keyframes + IBs, no Seedance content yet). Watch this so you understand what currently ships.

Use `ffprobe` to confirm the Seedance video's metadata. Use `ffmpeg -i <video> -vf fps=12 frame_%04d.png` (mentally — do NOT run it) as the extraction model.
</must_read_first>

<task>
Produce a plan that takes Act 1 from its current state ("approved NB2 keyframes + ComfyUI in-betweens, Seedance test exists in isolation") to "Act 1 final hero loop, shipped, marked complete." The plan must integrate the Seedance test output through NB2 cleanup, not replace the existing approved frames wholesale.

**Plan must cover:**

1. **Comparison phase.** How will we systematically compare the existing 12fps NB2+IB Act 1 against the 24fps Seedance video? What's the side-by-side method (synchronized playback, frame-pair grid, beat-aligned table)? Identify which **specific frame ranges** of the Seedance output are stronger than the current approved sequence (better arcs, more breathing, smoother weight shifts) vs. where the approved NB2/IB frames win (identity, line quality, expression).
2. **Selection phase.** Which Seedance frames will we extract for NB2 cleanup? Express as time ranges in the source 24fps video AND target 12fps frame slots in the final hero loop. Apply the principle: pick frames where Seedance found motion the IBs missed; reject frames where Seedance drifted on identity, stylus hand, or paper texture (these will fail HF02/HF05/SF02).
3. **Extraction phase.** Specify the exact `ffmpeg` extraction commands and output naming. Choose a target FPS (the assembly is 12fps; do we extract at 12fps, or extract at 24fps and decimate?). Decide where extracted frames live: propose `runs/run_2026-04-04_174805/seedance_frames/` or similar.
4. **NB2 cleanup phase.** Spec the redraw loop: each chosen Seedance frame is fed to `generate_image.py` as a reference (alongside `images/2D-Character-Sketch-Sean-v1.png`) with a cleanup prompt that says "redraw in pencil test style on cream paper, preserve pose and gesture exactly, identity must match A-2." Reference Phase B.5 step 4 in CLAUDE.md and the Tier A/B cleanup approach in `docs/2026-04-27-act2-seedance-execution-plan.md` (Task 8) for the pattern. Propose naming: e.g., `PT_A1_F##_seedance_clean.png` or insert into existing slot names. Define the audit pass (HF/SF gates) and retry ladder (max 3 attempts per frame).
5. **Integration phase.** How are the cleaned Seedance frames merged into the existing approved frame sequence? Update `manifest.yaml` hold durations? Replace specific IB slots? Insert new frames between existing ones? Be explicit about what changes in the assembly's frame-by-frame ordering.
6. **Outstanding-work phase.** Address the remaining unchecked Act 1 items from `docs/production-checklist.md`: sprite fade F38–F41, pencil trail effect (Beat 2), final layered export over P-32A background. Decide which are required to "ship Act 1" and which can be deferred.
7. **Final assembly + ship phase.** New FFmpeg assembly run, GIF/WebM/MP4 exports, QA review against the Engine Truth ("plays smoothly at 12fps, recognizably Sean"), update `docs/production-checklist.md` to mark Act 1 complete, append CHANGELOG entry.
</task>

<deliverable_plan_structure>
Output the plan in this structure:

<plan>
  <summary>2–3 sentences. What the plan does, what ships at the end.</summary>

  <assumptions_and_open_questions>
    Numbered list. Anything you had to assume, anything that needs the user's input before execution. Be explicit about uncertainty.
  </assumptions_and_open_questions>

  <comparison_method>
    Concrete method (not "we will compare them"). Tools, side-by-side artifact, decision criteria. Include the criteria you'll use to score Seedance frames vs. existing NB2/IB frames.
  </comparison_method>

  <tasks>
    Numbered, each with:
    - **Goal:** one sentence
    - **Inputs:** files / prior task outputs
    - **Steps:** ordered actions (commands, prompts, file moves)
    - **Outputs:** files written, including paths
    - **Acceptance:** how we know this task is done
    - **Risks / fallbacks:** what could go wrong, what we do if it does
  </tasks>

  <frame_inventory>
    Table: target Act 1 frame slot → source (existing approved file, or Seedance extraction at timestamp X.XXs → NB2 cleanup) → status. Cover all 42 frames at minimum.
  </frame_inventory>

  <ship_criteria>
    Bulleted list. What "Act 1 complete" means concretely. Tie back to Engine Truth and the production checklist's outstanding items.
  </ship_criteria>

  <out_of_scope>
    Anything explicitly NOT in this plan (e.g., Act 2, sound design, title cards, portfolio site embed).
  </out_of_scope>
</plan>
</deliverable_plan_structure>

<constraints>
- **Aesthetic protection.** Never assemble raw Seedance frames into the final loop. Every Seedance-sourced frame goes through NB2 cleanup first.
- **Stylus rule (Act 1 only).** Stylus must remain in Sean's RIGHT hand in every frame. Reject Seedance frames that put it in the left hand or drop it.
- **Identity lock.** A-2 (`images/2D-Character-Sketch-Sean-v1.png`) is the identity reference for every NB2 cleanup call.
- **Aspect / paper.** 16:9, cream production paper with grain, hole-punch label visible. Anything pure white background or digital-clean is HF02/HF05.
- **No destructive moves on existing approved frames.** Cleaned Seedance frames go into a new namespace; the current approved NB2 keyframes and ComfyUI IBs remain on disk untouched until final assembly. Plan must not delete from `approved/`.
- **Active run is `runs/run_2026-04-04_174805`.** Stay in this run dir. Do not propose a new run unless you make the case for it explicitly.
- **Maintenance conventions (CLAUDE.md).** The plan must include a CHANGELOG entry on completion and a `docs/production-checklist.md` update marking Act 1 complete.
- **Plan only.** Do not call generate_image.py, fal_client, or ffmpeg in this session. Read files, list directories, run ffprobe — that's it.
</constraints>

<validation>
Before delivering the plan, self-check:

1. Did I actually read all six files in `<must_read_first>`? Quote one specific decision or constraint from each.
2. Does my frame_inventory account for all 42 frames in the Act 1 hero loop?
3. For every Seedance frame I propose to use, did I name a specific timestamp in the 6.04s source video AND a target slot in the assembly?
4. Did I address every unchecked item under "Phase 4: Act 1 Compositing — IN PROGRESS" in the production checklist, even if the resolution is "deferred to post-ship"?
5. Are my acceptance criteria observable (a file exists, a video plays, a checklist item is ticked) rather than subjective?
6. Did I include a fallback for the case where NB2 cleanup of a chosen Seedance frame fails the audit 3 times?

If any check fails, revise before delivering.
</validation>

---

**Session kickoff line for the user to paste after this prompt:**

> Read the six files in `<must_read_first>`, survey the assets in `runs/run_2026-04-04_174805/`, then produce the plan in the structure specified. Stay in plan mode. When you're done, present the plan for review — do not start execution.
