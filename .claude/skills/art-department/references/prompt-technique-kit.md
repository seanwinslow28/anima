# Prompt technique kit — the look-test toolbox

The reusable techniques Artie uses to write look-test candidates and the final
prompt pack, each proven on the 2026-07-14 GRANDMASTER sprint
(`grandmaster-worked-example.md`; the committed fixture is at
`evals/artdept/fixtures/grandmaster-mini/`). Draw the route language from the
brief, the locked sidecar decisions, and the register research — never invent a
style doctrine in the room.

## (a) The web-search-the-show lever — the sprint's best discovery

When a register reaches for a real show's look, **do not** narrate the render
with long anti-render style prose (on gpt-image that renders realistic by
default — "too real" is primal-sketch-grit's nature, not a prompt slip). Instead
lean on the model's own reference lookup. The working clause, verbatim from the
sprint:

> *"STYLE: a stylized 2D hand-drawn ANIMATED CARTOON in the raw hand-inked
> register of Genndy Tartakovsky's show Primal. Use Web search to research
> Genndy Tartakovsky's show Primal to accurately depict the character animation
> art style."*

This gave Sean the **exact** clean, appealing animated-cartoon look — leaning on
ChatGPT's real reference lookup instead of narrated render prose. It is a
reusable per-style lever: name the show, then instruct the model to web-search
it before drawing. Swap the show for the register's true reference (Samurai Jack
S5 for `samurai-jack-s5`, etc.).

**Worked example:** the fixture's `① FRESH — Boy WIMPY full-body anchor` prompt
ends on exactly this clause; every fresh gen in the GRANDMASTER pack carries it.

## (b) Fresh-vs-edit economy (from `prompt-how-much` + the pack's Rule header)

Two prompt shapes, and the amount of prompt each needs is opposite:

- **FRESH (no reference):** full description + named style + anti-render
  negation. You are establishing identity *and* style from nothing, so the
  prompt carries everything — the full physical description, the loaded object,
  the flat-daylight staging, the web-search style clause, "16:9 aspect ratio,"
  "No text, no watermark."
- **EDIT / COMPOSITE (with reference):** terse — **only the change.** The
  reference image carries identity AND style, so one **style-agnostic** prompt
  each: "Image 1 is the character reference. Keep this exact character, outfit,
  proportions, and art style unchanged. Redraw them as a turnaround…" You never
  re-describe the character or re-name the style in an edit — that fights the
  reference.

**Worked example:** the fixture's `② EDIT — turnaround` and `③ COMPOSITE — warm
keepsake photo` prompts are both terse, reference-carried, and style-silent,
against the verbose fresh anchor above.

## (c) The dependency map

The order in which prompts feed each other, so consistency is structural, not
hoped-for:

```
FRESH  → establishes each character's identity + style (the anchor)
EDIT   → always edits the anchor OF THAT CHARACTER, IN THAT STYLE
          (re-pose, re-costume, turnaround, new state — never a re-gen)
COMPOSITE → feeds BOTH named anchors into one frame (a scene, a photo)
```

**Never cross styles: edit the anchor you made, in its register.** The
trained kid is an *edit* of the wimpy-kid anchor (headband on, glasses off), not
a fresh gen; the keepsake photo is a *composite* of the locked boy + locked
grandma anchors. The ChatGPT orchestration prompt encodes this map so the batch
runner edits the anchors it makes, keeping identity across the whole pack.

## (d) Daytime / neutral reads

For any **design read** — anchors, turnarounds, candid staging — use **flat,
even daylight on a plain neutral background.** Dramatic lighting hides the face:
the sprint's golden-hour kid looked cinematic and told you nothing about the
design. Clean flat-daylight turnaround + candid + a wide isolation-staging shot
gave the real read. Save the dramatic lighting for the *piece*, never for the
design plate.

## (f) Generation-workflow conventions — bake these into every pack header

The pack is run in the **Codex / ChatGPT Desktop app, which has the project
filesystem**. These conventions get re-derived every session; write them into the
pack's Rules header once, verbatim, so the batch holds together:

- **Path-based, never attachments.** Cite every reference BY FILE PATH; save every
  output to a named path in one output folder so later batches read earlier outputs
  from the same folder. Quote paths with spaces.
- **The continuity rule.** When a prompt places a designed character or re-angles a
  designed location, cite the reference image(s) by path and NAME each — never
  re-describe a designed character or location from text (that fights the reference
  and drifts identity). Party-2 scenes use the Y2 anchors, etc.
- **Scene frames render in the scene's own light.** A composite inherits the
  daylight and palette of its location reference — **never a darkened or
  silhouetted grade** applied on top. The FIRST LICKS geyser v1 was darkened and
  "read as a different film"; the fix was to inherit the party-yard daylight.
  (This is the complement to (d): design plates = flat neutral daylight; *scene*
  frames = the location's palette law, never flat-neutral, never re-graded.)
- **Never cross styles in a chain** — see (c). Each register pass edits its own
  anchors; a Primal image never seeds a Samurai-Jack gen or vice versa.

## (g) The cross-style composition/lighting reference

You CAN use an image from a *different* register purely as a **composition and
lighting map** — framing, figure scale, the light direction/god-rays, the depth
layering — while rendering in your own locked register. The lever is an explicit
scope clause: *"Use `<path>` for COMPOSITION AND LIGHTING ONLY — NOT its art style
or color; render entirely in the STYLE clause below."* Proven on FIRST LICKS: the
Samurai-Jack cherry-blossom still drove the tree-meditation framing/backlight while
the frame rendered in `primal-sketch-grit`. Use sparingly and always scoped — an
unscoped off-register reference will pull the style with it.

## (h) Re-angling a designed location — the two-reference reconstruction (2026-08-05)

A new camera on a designed set is **not an edit** — an edit surface preserves
framing by design, so "keep every fixture" + "render from a new position" is a
contradiction the model resolves by returning the source framing with added
dressing. This burned a full nine-plate batch on the FIRST LICKS W1.5 party-yard
cascade (gpt-image-2) before the method below recovered it cleanly. **Transport
provenance matters:** the W1 angle sets that DID work as edits ran on NB2
(Gemini image) — NB2 tolerates re-angle-via-edit; gpt-image's edit path is
surgical-only. On gpt-image, re-angles are **fresh spatial reconstructions**:

- **Image 1 = the ratified master as a WORLD/STYLE/FIXTURE BIBLE only**, with an
  explicit role clause: *"Preserve its fixture designs, materials, palette, light,
  and rendering. Do NOT copy its camera, framing, horizon, perspective, or
  screen-space layout."*
- **Image 2 = a monochrome COMPOSITION ROUGH** for the target camera ($0 to make,
  approve the roughs before any generation): *"Follow its camera, perspective,
  horizon, and left-to-right placement; replace its rough shapes with the
  corresponding fixtures; remove every guide mark."*
- **The prompt states three blocks explicitly:** CAMERA (position, compass
  direction, shot character) · VISIBLE LEFT→RIGHT (screen-space arrangement) ·
  OUT OF FRAME (what's behind the lens — naming it is what keeps it out).
- **Gates:** prove ONE re-angle before the batch; and when an angle *invents* an
  unseen zone of the location, ratify that plate first — it becomes the zone's
  bible for every other angle that shows it (skip this and the zone's fixtures
  drift between angles).
- **True surgical edits stay edits** on any transport: same camera + ONE change
  (remove the piñata, dawn re-key, night re-key) is the edit surface's home turf.

## (e) Register research — read before you write a route

Before writing any candidate prompt in a register, **read
`registers/{name}/research.md`** — the sourced craft write-up (line/ink/paint
process, palette, timing, negative controls). It corrects memory-filled
assumptions: the primal research established that *Primal is NOT flat-angular*
(that's Samurai Jack's sibling register), that the blood-substitution
candy-geyser is a Jack convention borrowed as staging, and that "sketchy"
overstates primal's confident blotted line. A route written from memory drifts;
a route written from `research.md` holds. When no register's research fits the
look, that is the no-fit signal — surface the gap to the style-register
authoring playbook, never inline-author (SKILL.md §7).
