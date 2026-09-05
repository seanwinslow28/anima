# CONTINUATION — 2026-08-31 · from plates to composites

Hand-off from the session that built the room bible and generated all six Movement 1 plates.
**Read this, then [`room-bible/README.md`](room-bible/README.md), before generating anything.**

Ticket: [#212](https://github.com/seanwinslow28/code-brain/issues/212) ·
Room bible: <https://claude.ai/code/artifact/0bbe2b86-d961-497f-99c4-986e1d7ef6cd> ·
Plates: <https://claude.ai/code/artifact/e573712a-a13c-4649-86cf-b8d21e001ff7> ·
Shot sheet: <https://claude.ai/code/artifact/aa1db30c-0f4e-49e5-90a3-5a96a30e8ce2>

Working directory: `/Users/seanwinslow/Code-Brain/anima/briefs/2026-08-02-about-me-short`

---

## The film

A **~90-second animated short** for Sean's portfolio: a PM and four AI-mascot sidekicks in a
break-room HQ. An alarm fires, each sidekick builds a brilliant *wrong* solution, Sean steps
back, asks the user one question, and the same team ships the tiny right fix. Pencil-test
register, 1950s Goofy "How To" grammar. Locked brief: [`00_studio_brief.md`](00_studio_brief.md)
(**amended 2026-08-31, read the amendment at its foot**). 20-beat sheet: [`beats-v1.md`](beats-v1.md).
Locked lines: [`lines-v1.md`](lines-v1.md).

**Movement 1 "Quiet Morning" is the current scope** — beats 1–3, ~15 seconds, seven setups.
It is also the fallback deliverable: stripped of narration it becomes Anima's project-tile piece.

---

## THE ORDER OF WORK — Sean's ruling, and it does not vary

> "We have to treat this like a sculpture that we chip away at one piece at a time. In 2D
> animation, everything is fully planned out, full extended rooms are drawn, character
> turnarounds are drawn, then the scenes, individual characters, and sectioned off backgrounds
> get drawn out and created separately and then composited."

    ground plan → elevations → rendered elevations → shot roughs → PLATES →
    CHARACTERS COMPOSITED → motion → timing

**Steps 1–5 are done.** You are starting at **characters composited**. Do not jump to motion,
and do not discuss timing until the frames are all approved — that was an explicit instruction.

The reason this order exists: shots used to be generated independently and continuity checked
afterwards, which makes continuity something you *catch* rather than something *true by
construction*. Three errors came out of that and they are documented in the room-bible README.

---

## The state of the seven setups

Everything below is normalised and lives in [`normalised/`](normalised/), **which is the
working set** — motion, edit and delivery all read from it.

| # | Setup | Plate | Composite | Next |
|---|---|---|---|---|
| S01 | Title card (Card D) | ✓ approved | n/a | Typography still undecided |
| S02 | Sean's station | ✓ `S02-plate-v1.png` | — | Sean, seated, back to camera, typing |
| S03 | Claude's nook · NW corner | ✓ | — | Claude at rest |
| S04 | Codex's rack · SW corner | ✓ | — | Codex at rest |
| S05 | Gemini's moodboard | ✓ | — | Gemini at rest |
| S06 | Grok's dartboard · NE corner | ✓ | — | Grok at rest |
| S07 | The CRT alarm | **RE — see below** | n/a (no character) | Re-roll the plate first |

Plates are at `plates/rev2/`, normalised copies at `normalised/S0X-plate-v1.png`.
**Every earlier plate and composite is superseded**; they are kept in `plates/`, `composites/`
and `m1-guides/old/` rather than deleted.

---

## FIRST JOB — re-roll S07, and the diagnosis is specific

Sean, 2026-08-31: *"I'd want to re-roll the CRT alarm wall. There isn't a line where the corner
should be and some objects are facing right while a couple of others face left. The SVG looks
good though, so it seems to have just been a prompt or GPT Image 2 generation issue."*

He is right on all three counts, and the geometry backs him:

- **The SE corner IS in frame.** Camera `(15.0, 12.0)`, yaw −7.8°, hfov 82.5°. The SE corner
  bears 28.6°, which is 36.4° off-axis against a 41.2° half-angle. The NE corner is in frame too
  at −39.7°. `room-bible/SHOT-S07-rough.png` draws both seams correctly.
- **The plate flattened it.** Everything came back drawn square-on, as if lifted straight off the
  elevation, with the moodboard sketches on the same plane as the credenza and no seam between.

**Most likely cause, and it is actionable.** S07 was the only shot given **one** elevation
reference and the **least angled** rough (yaw −7.8° is nearly square to the wall). The elevation
and the rough therefore looked similar to the model, and the elevation's flat orthographic camera
won despite the "do NOT copy its flat orthographic camera" clause. Every corner shot that came
back correct — S03, S04, S06 — had **two** wall elevations and a steeply angled rough.

**What to try, in order:**

1. **Give it two elevation refs like the other corners** — `normalised/ELEV-east-v3.png` *and*
   `normalised/ELEV-south-v2.png` — plus the rough. Two walls in the references signals a
   two-wall shot.
2. **State the perspective in words.** The prompt should say: *"A single vanishing point sits
   near the centre of frame. Everything left of centre shows its right-hand side; everything
   right of centre shows its left-hand side. The shelving and the credenza are seen at a slight
   angle, not square on. At the right of frame the wall turns a corner — the vertical seam is
   visible, and the taped-up sketches beyond it are on the receding wall."*
3. **Consider narrowing the lens.** 82.5° is the widest of the six and catches both corners.
   Raising `fill` for `S07` in `room-bible/make_shot_roughs.py` narrows it; re-run the script
   ($0) and regenerate the rough before the plate.

Prompt to edit: [`prompts/plates-rev2/S07.txt`](prompts/plates-rev2/S07.txt).
**Keep the screen DARK** — the alarm is the movement, and the `PROBLEM!` frame is a surgical
edit on top of the finished plate (that pair is beat 3's start/end keyframes).

**Sean's verdict on the other five: "the rest of the corners look perfect."** Do not touch them.

---

## SECOND JOB — the composites

### Use the real turnarounds. They exist and they were ignored for a week.

`runs/Act-Rework-Backlog/02-AI-company-character-refs/` — **five-view sheets for all four
mascots**, drawn 2026-06-30: front, ¾ front, profile, ¾ back, back.
`claude-turnaround.jpeg` · `codex-turnaround.jpeg` · `gemini-star-turnaround.jpeg` ·
`grok-gremlin-turnaround.png`. Sean's anchor turnarounds are at
`runs/Act-Rework-Backlog/01-sean-character-refs/`.

Three Gemini composites were burned asking the model to invent a back view that was already
drawn. **Crop the view you need out of the turnaround and pass that as Image 1.** Do not pass
the five-character `cast-scale-lineup.png` — Codex and Gemini are the same colour family and
NB2 corrupted one with the other 4/4 in July.

### The composite recipe, with the two clauses that were lost and found

Per `prompt-how-much`: ~50–70 words for the change, role-tag both refs, one scale clause, one
position clause, *"Keep Image 2 unchanged"*, style token, anti-text. **Never re-describe the
scene.** The two clauses that must be in every one:

- **`with a soft graphite contact shadow`** — this was in the proven S04 probe prompt, I dropped
  it when rewriting, and Gemini ended up standing on the baseboard. It is why.
- **feet on the floor, explicitly**: *"both feet flat on the tiled floor in front of the
  baseboard."*

### THE REST-POSE LAW — binding

Sean, 2026-08-31: *"whenever we generate images where the subject is already performing an
action, it looks awkward in Seedance motion because we're prompting the model to generate the
action that the character is already in the middle of performing."*

**The still holds a rest pose. Seedance supplies the movement.** Wording that works:

> It stands still and upright at rest, both arms hanging down at its sides, both feet flat on
> the floor, turned three-quarters away from us to face <the thing it is about to act on>.

**Held is not transient.** Hands resting on a keyboard, an arm laid on a rack: fine. Mid-throw,
an arm extended mid-reach, a hand pressing something onto a wall: not fine.

### Scale and facing — state both, always

Cast ratios: Sean 1.00 · Grok 0.42 · Codex 0.36 · Gemini 0.30 · Claude 0.26. **Anchor scale to a
named prop in that shot** ("knee-high to a person, its head reaching about a quarter of the paper
tower"), never to a percentage of frame. Facing goes in every prompt: absorbed in its own task,
never addressing the lens — the all-corners wide was cut because facing was unstated and
everything defaulted to the camera.

**Measured from the last round, for reference** — apparent frame height ÷ true cast scale is a
camera-distance proxy: S05 101, S06 105, S03 75, S04 54. The four corners should land closer
together this time now that the cameras are solved from one plan.

### NSFW hazard, recorded

Grok's first composite prompt — *"grey gremlin shape, bat ears, red eyes, fanged grin"*, *"arm
cocked back mid-throw"* — came back `status: nsfw` with no image. The softened wording in
`prompts/S06-grok-composite.txt` passed first time: *"a round grey cartoon creature with big
pointed ears, a wide friendly cartoon grin and a tufted tail."* Reuse that.

---

## The standing laws

| Law | Where it lives |
|---|---|
| **Normalise every frame in post** — `post/normalize_paper.py` → `normalised/`, the working set. Canonical cream `#f5e8d1`, tolerance ±8 | [`environment-style.md`](environment-style.md) |
| **One source of truth** — `WALLS` in `room-bible/make_room_bible.py` is the only description of the set. Plan, elevations and roughs all derive from it | [`room-bible/README.md`](room-bible/README.md) |
| **Rest pose, never mid-action** | above |
| **The look lives in post** — every plate and composite generates CLEAN (FIRST LICKS DR #41) | [`environment-style.md`](environment-style.md) |
| **Preserve superseded work** — move to `old/`, never overwrite | throughout |
| **Verify edits** with FFT phase correlation + edge-diff against the source plate, not frame-delta means. GPT's edit path benchmarks at 0.42; this project has been landing 0.47–0.58 | [`prompts/_blocks.md`](prompts/_blocks.md) |

**Generation still carries the palette clause** even though the normaliser exists. A plate that
comes back needing a gain near 1.0 is the cheapest signal that a new reference has not dragged
the paper. The six new plates needed **1.005–1.056**; the old ones, generated against a
pre-clause bible, needed **1.08–1.27**.

---

## Production route — settled, do not re-derive

| Step | Tool |
|---|---|
| Plate generation | `gpt_image_2`, 2k, quality `high`, aspect `16:9` |
| Character into plate | `gpt_image_2` **edit**, refs = turnaround crop + plate |
| Re-angles | reconstruction pattern: elevation(s) as fixture/style bible with camera explicitly excluded, plus the projected shot rough |
| Motion | `seedance_2_0`, **`mode: fast`**, **7s**, 720p, `generate_audio: false`. `std` stutters and Sean rejected it |
| Motion prompt | **`prompts/motion/04-single-character-7s-ADOPTED.txt`** — the recipe Sean named |

CLI: `higgsfield generate create <model> --prompt "$(cat p.txt)" --image ... --quality high
--resolution 2k --aspect_ratio 16:9 --json --wait`. Write prompts to `.txt`; apostrophes break
inline. `gpt_image_2` is 8.5 credits, `seedance_2_0` fast/7s/720p is 24.5.

**Seedance takes NO negative prompts.** State locks positively. Damping words ("light taps",
"small bounce") dampen — genre anchor plus vivid verbs plus zero negation gave +55% motion energy
with slightly *less* drift.

---

## The brief was amended today — know what changed

Sean ruled that the USER lives **on screens only** and that the Sean character **never speaks
aloud**; his one question is typed into a **chat box** on his monitor. `00_studio_brief.md`
carries a dated amendment at its foot; `beats-v1.md` beat 13 is restaged from the doorway to his
monitors; `lines-v1.md` keeps the question verbatim and notes only that its delivery moved. This
also resolved a contradiction that had sat flagged in `beats-v1.md` since 2026-08-04.

Consequence for the boards: **beats 2, 4, 12 and 13 all play at S02**, which is why the north
wall is drawn as the richest in the room. The doorway is pure dressing and never carries a beat.

---

## Open, and none of it blocks the composites

1. **S07 re-roll** — first job, above.
2. **The confetti cannon in S02 reads as a telescope** — a narrow tube on a tripod; it should be a
   stubby wide-mouthed barrel. One surgical edit. Only matters from beat 9.
3. **S02 needs a Movement 3 state** with a chat box on the centre monitor and the faceless USER
   in it. Not a Movement 1 frame — do not add it to the current plate.
4. **Title-card typography** (S01). The one setup Seedance never touches.
5. **`CHECKOUT COMPLETIONS` label** on S07's falling graph — left off deliberately so the plate
   would not sprout captions. One edit if Sean wants it.
6. **Codex's face goes off-model under Seedance `fast`** — it grows a mouth. `std` holds the face
   but stutters. **This is the last gate before motion** and it is Sean's eye, not a measurement.
7. **The matte-and-relay drift test** is still unrun — matting the character out of the animated
   clip and re-laying it on the pristine plate, which would make plate drift structurally
   impossible. Worth more now that the corners are prop-dense; measured drift was 22–27%.
8. **The runtime arithmetic.** Beat 2 is 8s across five setups — 1.6s each — while its narration
   alone reads ~9–10s at the brief's pace. The stopwatch table-read
   ([#206](https://github.com/seanwinslow28/code-brain/issues/206)) is $0, Sean-only, and settles
   it. Do not raise timing until the frames are approved.

---

## Working discipline

Sean directs; propose with a stated lean and let his eye decide. **Measure rather than assert** —
several premises here survived until they were measured and then did not. When a ruling reverses
an earlier one, record why, keep the superseded artifact, and say plainly what it costs. Instrument
as you go: wall-clock, rolls per shot, credits. The 4-hour gate on Movement 1 is about *Sean's* gate
time, and the ratio that would blow it is rolls-per-shot, not the clock — this round was **six
plates, six first-roll successes, 51 credits**.
