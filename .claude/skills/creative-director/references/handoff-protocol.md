# Handoff Protocol

Read this when moving from direction into execution. It is a **template to fill from the
project**, not a description of any one project's pipeline.

**Every bracketed field is supplied by Phase 0 and the interview.** If you find yourself
writing a tool name, a file path, a resolution or a naming convention that you did not read out
of the project, stop — you are inventing a pipeline instead of reporting one.

---

## 1. Strategic directive

- **Single objective:** [one sentence — the ONE thing this has to achieve]
- **Creative intent:** [mood, tone, register, and the arc if there is one]
- **Audience:** [who sees it, and in what state]
- **Distribution:** [where it lives — this decides aspect, duration and formats]

## 2. Asset audit

**Exists and approved:**
- [ ] [character or subject references, with paths]
- [ ] [approved plates, stills or frames]
- [ ] [the prompt archive, including the rejected files]
- [ ] [any spatial or style bible]

**Missing, to be created:**
- [ ] [name each gap, and say which is on the critical path]

**Where work lands:**
- [ ] [the project's existing directory convention — follow it]
- [ ] [the project's existing naming convention — follow it]

> If the project has no convention, propose one **and say that you are proposing it.** Never
> introduce a naming scheme silently; a second scheme is worse than an imperfect first one.

## 3. Technical specifications

Read these out of the project. Do not default them.

- **Register:** [the style token, stated as the project states it]
- **Resolution / aspect / frame rate:** [ ]
- **Route:** [model and settings for stills; model and settings for motion]
- **Cost per unit:** [per still, per clip, in the project's own units]
- **Budget ceiling:** [and what happens at it]
- **Output formats:** [ ]

## 4. Execution roadmap

Each step names a **real** tool with its real invocation.

### Phase A — Scaffold
1. Confirm every input the first generation needs actually exists
2. Dry-run whatever can be dry-run, at zero cost
3. Verify the prompt files are on disk and non-empty

> **Guard against empty prompts.** If a runner can be handed an empty string, it will be, and
> some CLIs accept it as satisfying a required field and charge for the result. Check byte
> count before spending, and read the prompt back out of the job record afterwards.

### Phase B — Generate
1. [the still/plate step, with its tool]
2. [the composite or edit step, with its tool]
3. [the motion step, with its tool]

Generate one unit first and look at it before running the batch.

### Phase C — Verify
1. [structural checks the project has — run them]
2. [the eye: put the work in front of the director]
3. Failures follow the project's retry ladder; record what changed between attempts

### Phase D — Assemble
1. [assembly tool and steps]
2. [format and delivery]

### Phase E — Review
1. Run the critique rubric on the result
2. Consult animation principles for timing and acting
3. Ship or return, against the Definition of Done below

## 5. Verification checkpoints

- [ ] **30% — Rough.** The approach is proven on one unit. It is right in isolation.
- [ ] **60% — Structure.** All units approved. Continuity holds between them.
- [ ] **90% — Polish.** Outputs rendered, consistent end to end, within spec.

## 6. Definition of done

- [ ] **It reads.** The thing a viewer is supposed to understand is understood, at playback speed.
- [ ] **It holds.** Identity, register, scale and continuity survive across every unit.
- [ ] **It is technically sound.** Correct aspect, no artifacts, outputs within spec.
- [ ] **The objective is met** — measured against §1, not against how much work it took.
- [ ] **The director has said so.** No rubric substitutes for that.
- [ ] **The record is complete.** Every prompt on disk with its result, its cost and its
      diagnosis; superseded work preserved rather than overwritten; every reversal explained.

---

## Cost reporting

Announce cost **before** spending it, as a running total: *"12 credits, running 36 of 100."*

At the ceiling, stop and ask — either for a raised ceiling or for permission to continue at
zero cost by emitting prompts for the director to run themselves. **Never quietly spend past
the number.**
