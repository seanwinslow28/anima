# Design seed — the animatic should define the loop's frame count (a PHILOSOPHY-level v1 flaw)

*2026-06-21. Surfaced live during the Spark-animatic DoD #6 run ([runbook](2026-06-18-spark-animatic-costed-run-runbook.md)). Captured here so it isn't lost; it needs its own short brainstorm before it's built. Not designed in full here.*

---

## What happened

Sean drew **7** placement roughs to stage the Spark loop better than the 5-frame version. Bea had authored a **5**-frame board. At `--approve-animatic` the ingest hard-errored:

```
error: animatic ingest failed: animatic rough F06.png names frame 6,
which is not in the board (frames: [1, 2, 3, 4, 5])
```

The run was unblocked by re-mapping the 5 strongest roughs onto the 5 board frames — a workaround, not a fix.

## Why it matters (this is the disease, not the symptom)

The hard error is *correct defensive behavior* — it refused to silently drop two frames Sean drew. The real problem is upstream: **the loop's frame count is owned by the agent (Bea's board), and the human's animatic must conform to it.** That inverts PHILOSOPHY's one non-negotiable belief — *the human owns timing*. A creative decision ("this loop is better at 7 frames") was made illegal by an agent's earlier choice. In a studio the animatic *defines* the timing and the boards conform; here it's backwards.

This is exactly the kind of flaw the costed run existed to surface, and it did so immediately — the system working as intended, finding the seam.

## The three ways to fix it (to be weighed in the brainstorm)

1. **Animatic extends the board (recommended starting point — most surgical).** When the ingest sees a rough naming a frame beyond the board, *append* that frame instead of erroring. The rough supplies placement; the new frame's prompt/cast/beat clone from the nearest board frame (human-editable), and the loop-return `chain_from` retargets to the new last frame. Smallest flow change (keeps STORYBOARD → ANIMATIC → GENERATE), and it makes the animatic literally able to *grow* the loop. Open questions: prompt derivation for appended frames (clone vs. prompt-the-human-at-the-gate), and keeping the locked-board contract honest (append into run-state, never mutate the committed board — the pattern already used for `animatic_ref`).

2. **Frame count as a human input upstream.** The human declares the loop length early (brief or plan gate) and Bea boards to it. Conceptually clean, but a bigger change to the authoring flow and Bea's frame-count behavior.

3. **Reorder: animatic before the board.** Block the animatic first (placement + timing + count), then Bea boards against it — the truest studio order. The biggest change; inverts the locked Phase 3 → Phase 4 sequence.

## Status

**Interim fix BUILT (2026-06-21, $0 stub-green TDD — Part 1 of the [hardening kickoff](2026-06-21-animatic-hardening-and-driven-run-kickoff.md)): `--frames N → Bea`** — design-seed **option 2**. Landed: `--frames N` on `pipeline.run` + a `target_frames` run-state field, threaded to Bea via `ctx.extras` (the live prompt states the target loop length; the stub boards exactly N keeping coverage valid); a deterministic count gate at `approve_storyboard_gate` refuses to lock a board that isn't exactly N; the ANIMATIC gate now prints `Board has N frame(s).`. +10 tests, back-compat (absent `--frames`) byte-identical. See CHANGELOG 2026-06-21. On reflection, **option 1 (animatic appends frames) was rejected**: appended frames would lack authored generation prompts, and the rough is placement-only — so a cloned/derived prompt would fight the rough's intent and mis-cite against Em's beat check. The board is where prompts live, so the human's frame count must reach **Bea**, not be bolted onto the animatic ingest. The interim fix lets the human declare the loop length up front; Bea boards N frames with real prompts; the animatic supplies placement for all N.

**Still a future slice:** the *deeper* "animatic natively defines/extends frame count after the board" (design-seed option 3 — the true studio order, animatic upstream of the board) stays parked; it's a bigger reorder and `--frames N` covers the common "I know my loop length" case. Per the anti-drift contract this all belongs to the same workstream (TOP-1) until DoD #6 closes. The Spark run's post-mortem records whether `--frames N` made the count Just Work.
