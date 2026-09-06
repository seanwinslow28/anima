# Critique Rubrics & the Defect-to-Lever Map

Read this when reviewing generated work. Score with the rubric, then use the map to turn each
observation into a change someone can actually make.

**Everything in angle brackets is supplied by the project, not by this file.** Phase 0 of the
skill is where you find `<the reference>`, `<the register>` and `<the route>`. A rubric that
names one project's character or one project's model is a rubric that lies to every other
project.

---

## Scoring rubric (1–4)

### A. Stills — a generated frame, keyframe or composite

| Score | Identity | Style | Composition | Continuity | Technical |
|---|---|---|---|---|---|
| 4 | Unmistakably the subject; matches `<the reference>` in every named feature | `<the register>` fully intact | Staging reads clearly and matches the boarded intent | Props, wardrobe, facing, scale all match neighbouring frames | Correct aspect, correct ground, correct resolution |
| 3 | Recognizable, minor feature variance | Mostly right, one or two register elements missing | Close, but angle or intensity differs | One minor prop or dressing inconsistency | Aspect right, minor ground issues |
| 2 | Subject-like, but notable drift in a key feature | Mixed — part register, part model default | Partially matches; one key element wrong | Facing, wardrobe or scale changed between frames | Aspect slightly off, ground weak |
| 1 | Not recognizable as the subject | Wrong register entirely | Does not match the intent at all | Major break — missing prop, wrong scale, wrong side | Wrong aspect, ground absent |

### B. Motion — a generated clip

| Score | Identity | Motion quality | Style consistency | Artifacts | Background |
|---|---|---|---|---|---|
| 4 | Held across the whole clip | Reads with weight; accelerates and lands | Line and texture match the source still | Clean throughout | The plate holds; framing is where it started |
| 3 | Slight drift, still reading | Generally right, one spacing issue | Slight variance | One minor artifact | Small drift, recoverable |
| 2 | Noticeable change mid-clip | Uniform spacing (floats), or stutters | Visibly different from the still | Multiple artifacts, ghosting | Background visibly regenerating |
| 1 | Unrecognizable partway through | Broken — limbs teleport or melt | Different aesthetic entirely | Severe throughout | Plate lost, or the camera moved when it was locked |

### C. Assembly

| Score | Timing | Continuity across cuts | Format | Playback |
|---|---|---|---|---|
| 4 | Pacing matches intent; holds feel natural | Every cut lands; matched shots actually match | All outputs within spec | Smooth at target rate |
| 3 | One transition slightly off | One cut soft | One output off spec | Occasional stutter |
| 2 | Several transitions wrong | Repeated framings read as a mistake | Missing output or wrong codec | Playback problems |
| 1 | Timing arbitrary | No continuity | Broken exports | Will not play |

---

## The defect-to-lever map

Columns are **surfaces**, not products. Bind them to the project's real tools in Phase 0.

### 1. Identity drift
*"It stopped looking like the character." / "The face changed."*

| Surface | Lever |
|---|---|
| Still, retry | Re-anchor explicitly from `<the reference>`. Name the features that must hold — *"the same jaw angle, the same eye spacing, the same silhouette"* — rather than saying "keep it on-model". |
| Motion | State identity as a **constant through time**, never as a rest state. *"Its face is exactly two dot eyes and two brows, the same two eyes and two brows in every frame"* holds; *"its face stays…"* loses to the action. |
| Motion | **Check whether a reference image is fighting the start frame.** On some models an extra reference overrides the start frame's composition outright — verify before assuming the prompt is at fault. |

### 2. Style drift
*"Lines are too clean." / "It looks digital." / "It over-rendered."*

| Surface | Lever |
|---|---|
| Still, retry | Name the register positively **and** negate the render modes it must not drift to. The negation half is what stops the drift on image models. |
| Motion | Register belongs in a **constant block that is never edited per shot.** Varying it per beat is how a sequence loses coherence. |
| Post | If generation cannot hold it, do it in post — and make that a rule, not a rescue. Generate clean, apply the look once, downstream. |

### 3. Composition, pose and framing
*"The pose is wrong." / "It cropped the thing I needed."*

| Surface | Lever |
|---|---|
| Still, retry | Quantify. Angles, not adjectives. |
| Still, retry | **A framing clause silently deletes whatever falls outside the frame it names.** "Head and shoulders only" removes a raised arm — the model is obeying, not failing. When the pose lives in the limbs, write the framing around the pose. |
| Composite | Scale and position are **never inferred**. Give an explicit scale clause and an explicit position clause in words. |

### 4. Scale failure
*"It came back twice the size it should be."*

| Surface | Lever |
|---|---|
| Composite | **Anchor to a tall fixture, never a low one.** A knee-high object reads as a floor, not a ceiling. Load `visual-guides/scale-anchor-tall-object.png`. |
| Composite | Four moves together: shout the direction, give a human yardstick, state a fraction of a tall named fixture, and negate the failure explicitly. |

### 5. Timing and pacing
*"It's slow motion." / "The beat happens too late." / "Nothing happens."*

| Surface | Lever |
|---|---|
| Motion | **Duration ÷ events sets the tempo.** One action given the whole duration gets spread across it, and spreading is slow motion. A repeating loop cannot degenerate that way. |
| Motion | **To move a beat earlier, delete an event — do not shorten a sentence.** Models spend time on events, not on words. A described hold is itself an event; write it as a state instead. |
| Motion | **Damping words dampen.** "Gentle", "unhurried", "settle", "small", "ease into" all reduce energy. There is no calm register — calm is a small action at full snap. |
| Assembly | Some timing is not a generation problem at all. Generate long, cut short. |

### 6. Under-motion and smears
*"It barely moves." / "I asked for a smear and got none."*

| Surface | Lever |
|---|---|
| Motion | Pair any effect with a **subject** motion; a static subject stays frozen while the effect fires. |
| Motion | **Smears come from reversals and rotations, never from one-way translations.** No wording will smear a single reach. Load `visual-guides/smear-from-repeated-motion.png`. |
| Still | **The still must hold a rest pose, not an instant.** A mid-action still forces the motion model to repeat or undo the pose. Load `visual-guides/rest-pose-vs-mid-action.png`. |

### 7. Continuity breaks
*"The prop switched hands." / "Two shots that should match don't."*

| Surface | Lever |
|---|---|
| Still, retry | State the continuity requirement as critical and reference the approved neighbouring frame explicitly. |
| Planning | When a new angle **invents** a zone of a location, ratify that frame before any other angle showing the same zone — it becomes that zone's reference. Otherwise the fixtures drift between angles. |
| Audit | Run whatever structural check the project has, and record findings against a frame identifier. |

### 8. Background and plate loss
*"The room redrew itself." / "The camera moved and I locked it."*

| Surface | Lever |
|---|---|
| Motion | Name the camera state deliberately. Locked and free are a dial, not a default. |
| Motion | Prop-dense frames drift most. Consider two keyframes from the same plate, or matting the subject out and re-laying it on the pristine plate. |
| Measurement | Compare frame zero **and** the last frame against the source. A low frame-zero score is a re-camera, not drift, and the two have different fixes. |

### 9. Interpolation artifacts
*"Ghosting." / "Melted features." / "Double exposure."*

| Surface | Lever |
|---|---|
| Motion | Reject and retry with a different seed before changing anything else. |
| Motion | Shorten the span the model has to invent. |
| Route | If it repeats across seeds, it is the route, not the roll. |

### 10. Refusals
*"It came back with no image."*

| Surface | Lever |
|---|---|
| Any | Content filters read **wording**, not intent. Describe the same subject and the same action in plainer, warmer terms. |
| Archive | **Record the wording that passed, verbatim.** A refusal rediscovered twice is a process failure, not a model failure. |

---

## Two standing cautions

**The eye outranks the metric.** A result can pass every measurement and still be wrong. Metrics
catch structural failure — a lost plate, a re-camera, a drifted identity — and nothing else.
Show the work; do not report numbers about it.

**Record the reversal.** When a critique overturns an earlier ruling, write down why, keep the
superseded artifact, and state what the change costs. The prompt archive is the project's
memory, and the files marked REJECTED are the most valuable ones in it.
