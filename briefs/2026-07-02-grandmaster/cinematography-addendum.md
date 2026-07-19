# FIRST LICKS — Cinematography Addendum (the Tartakovsky shot-language pass)

*Produced 2026-07-18 by the `/watch` pass over Sean's six Tartakovsky breakdown videos — the pass named in [`concept.md`](concept.md) §Open items — **plus the same-day second pass (Part 4)** over Sean's seven follow-up picks: the V6 narration capture, the geyser waterfall look-refs, the camcorder VHS refs, and four more Tartakovsky sources, with the Sean-ratified triptych device spec'd as Recipe 6b. Sam and Bea read this alongside the concept doc and [`00_studio_brief.md`](00_studio_brief.md). **Nothing here overrides a lock**: where a video taught something that conflicts with a locked rule, it is flagged in Part 3 (+ Part 4's F8), never silently absorbed. Every claim carries a video + timestamp citation; where a rule extends an R1–R10 finding from the [writers'-room digest](2026-07-18-writers-room-session.md#1-research-digest-keyed-r1r10-provenance-tags-used-throughout), the R# is named.*

## The six videos (citation key)

| Key | Video | Source quality caveat |
|-----|-------|----------------------|
| **V1** | "The Cinematography of Genndy Tartakovsky" — Lavapasta, 20:54 ([link](https://www.youtube.com/watch?v=y2jLVvBJhQM)) | Video essay; timings are our own ffmpeg scene-detect measurements of the excerpted clips (hold lengths are minimums — the essayist trims). Narration masks source audio, so it yields no sound-timing data. |
| **V2** | "Genndy Tartakovsky Answers Animation Questions From Twitter" — WIRED, 15:47 ([link](https://youtu.be/4uvlCjcT7oM)) | Interview + sketch-pad demos. Zero measured timings; its value is doctrine in Genndy's own words + the storyboard/composition rules he draws on camera. |
| **V3** | "Genndy Tartakovsky \| Reading the Action" — Any-mation, 16:18 ([link](https://youtu.be/iZAcRJafmD4)) | Video essay with long uninterrupted clip plays; the best cut-grammar math in the set (ASLs, burst counts, hold census). Auto-captions garble names. |
| **V4** | "Behind The Scenes: Genndy Tartakovsky's Primal" — Adult Swim, 10:32 ([link](https://www.youtube.com/watch?v=2ZUWGoEbbSs)) | BTS featurette. Doctrine + palette data + one measured burst floor; cut counts are floors (100 of 208 scene changes sampled). |
| **V5** | "How Samurai Jack Mastered The Art of 'Nothing'" — Nerdstalgic, 9:48 ([link](https://youtu.be/H3DN6hKh_EA)) | Video essay; measured silence/foley data (audio silencedetect was run). Scene detection under-counts in white-on-white/black-on-black passages. |
| **V6** | "Samurai Jack Season 5 opening with Genndy's storyboard narration" — Veto, 6:00 ([link](https://www.youtube.com/watch?v=T2ue-mr7sz8)) | **Broadcast footage of the S5E1 opening — real screen timings.** No captions; the first pass was frame-only. **Narration since captured via Whisper (second pass, 2026-07-18)** — beat-by-beat live performance narration, mined in Part 4 §A. |

**Second-pass sources (Part 4, 2026-07-18 — Sean-directed):** **V7** "Rainbow Waterfall Animation Process" — roseshards Short, 0:23 ([link](https://youtube.com/shorts/KzKoTzIjlyQ)) · **V8** "2D Waterfall Animation Green Screen" — Green Screen FX, 2:06 ([link](https://youtu.be/4kQTauplWqk)) · **V9a** "90s Party Vlog | VHS Camcorder" — Kloud Envy, 6:36 ([link](https://www.youtube.com/watch?v=nKv-pevKj3I)) / **V9b** "VHS Found Footage — 1999 House Party" — SkyCorp Home Video, 1:00 ([link](https://www.youtube.com/watch?v=qqC9QKW0KKI)) / **V9c** "Proof The 90s Were Awesome — Old VHS Tape" — Adrian Gray Comedy, 1:37 ([link](https://www.youtube.com/watch?v=ir1noY95kso)) · **V10** "What is The 'SAMURAI JACK' Art Style?" — LP Lucas, 8:30 ([link](https://youtu.be/RAKanwgHlao)) · **V11** "The Subtle Worldbuilding of Samurai Jack" — Santi Barrios, 23:50 ([link](https://www.youtube.com/watch?v=a-B-OtVnHP8)) · **V12** "Samurai Jack — The Action and Emotion" — IGN/Adult Swim Blu-ray featurette, 1:09 ([link](https://youtu.be/iLuavgLp7vg)) · **V13** "Samurai Jack & Clone Wars: Action Directing with Genndy Tartakovsky" — Dan Fox, 10:33 ([link](https://youtu.be/zKJcIY1NbRM)).

**How to read the numbers.** All sub-second figures come from ffmpeg scene-change detection (dissolve-blind, strobe-over-triggering; cleaned where noted). Treat ±1 cut / ±0.3s tolerance. Where five independent videos converge on the same number, trust the convergence.

---

# PART 1 — THE DISTILLED RULEBOOK

## 1. Cut grammar

**CG-1. The three-beat unit (the master rule).** Every action, no matter how small, gets all three beats in order: *what is about to happen → what happens → relax with the aftermath* [V3 15:02–15:14, stated over the Mace Windu fight]. No action ever launches without its anticipation or lands without its aftermath shot. Extends R3 with the unit that organizes it.

**CG-2. The measured tempo bands.** From the Mace fight (~24 real cuts in 34s, ASL ≈ 1.4s) [V3 00:31–01:05] and the full S5 opening (~50–55 cuts over 122s, ASL ≈ 2.2–2.4s) [V3 11:13–13:15]:
- Anticipation holds inside action: **2–3s** [V3 00:33–00:38].
- Burst cuts: **0.67–0.92s each** [V3 00:44–00:49].
- Aftermath wides: **3.5s+** [V3 01:04].
- Flurry/recovery rhythm: flurry shots ≤1.5s each, then a recovery hold ≥3.5s before the next flurry [V5 03:20–03:34, the 300-homage charge].
- A complete action scene = long-hold bookends (~8s), mid-tempo middle (1.6–3s), exactly one strobe peak [V3 11:13–13:15]. This is the direct tempo template for Act 3.

**CG-3. The burst, quantified (R3 gets its number).** At full burst Genndy drops to **15–20 pieces of 1–5 frames each, ~2.5s total**, bracketed by multi-second holds on both sides. Independently measured four times: ~20 cuts in 2.3s (S5 knife fight, pieces 0.04–0.2s) [V1 14:04.1–14:06.4]; ≥12 transitions in 2.5s (S4 assassin duel) [V5 04:56–05:18]; ~24 detections in ~3s (S5 gatling burst) [V6 01:44–01:47]; ≥8 cuts in ~6s at 0.7s/shot (Primal rampage — a floor) [V4 07:49–07:55]. **The burst is editorial as much as animated**: it can be realized as cut-strobe and full-frame polarity flips rather than extra drawings [V5 04:56, V6 01:46]. If the sever multi-cut is boarded at 1.5–2s per cut it will read *slower* than the reference [V1 flag].

**CG-4. Cut-budget concentration.** Quiet = no cuts; loud = all the cuts at once. The 6-minute S5 opening averages well under 20 real scenes, with uncut stretches of 15s/23s/25s/32s/37s/47s and its cut budget spent in exactly two dense clusters [V6 macro distribution]. R2's quiet/loud song, visible as cut-density contrast.

**CG-5. The storyboard-cut contract.** "Every time you cut, there's a new storyboard; every time there's a change of emotion, there's a new storyboard; every time anything semi-significant happens, there's a new drawing" [V2 11:30–11:42]. Board panels ≈ animation extremes [V2 11:42–11:48]. Planning density for action: **"30, 40, 50 poses for like five seconds"** [V3 07:44–07:49, Genndy over his own thumbnails]; the essay corpus corroborates "60 poses in 5 seconds" [V5 03:16–03:19]. This is Bea's panel-granularity contract.

**CG-6. The Copernicus rule (few setups, many panels).** A whole rise-from-the-grave action used ~3 camera setups: (a) hold on the spot — 4–5 panels of action inside ONE setup; (b) cut to a new angle **landing on the action's articulation point** (the rise-and-land); (c) "then we start cutting close" — coverage tightens only AFTER the big action resolves [V2 11:55–12:20]. Cuts are spent on articulation moments, not coverage.

**CG-7. Anticipation is the star; the strike can leave the frame.** For a cartoony hit, "the anticipation is crazy… and then the punch would be completely off the page" — the wind-up gets the drawings, the strike itself can be one drawing that exits frame [V2 03:12–03:28]. The mechanism: poses are held as keyframes and the travel frames compressed to near-invisibility "so our eyes register a longer held pose" [V3 06:49–06:56]. Extends R3.

**CG-8. Smash-to-black as percussion.** A hard cut to a 100%-black frame, held ≥1s, functions as a beat separator mid-sequence [V6 04:25–04:26]; a title card on black carries 1.1s of total silence before the next cut [V5 06:17–06:19]. The black frame is the drum hit between registers.

**CG-9. Dissolve chains for reverence.** The S5 cold open runs ~26s on 4 transitions — 4–10s elements joined by slow cross-dissolves, zero hard cuts until the inciting motion [V6 00:00–00:26]. Slow-dissolve chains are the "sacred/mythic" alternative to cutting. Extends R1/R10.

## 2. Camera discipline

**CD-1. The camera does not move.** Locked frames throughout; all energy is in-frame (smoke, dissolve ghosts, action) [V6 00:00–00:16; V5 07:52–08:12 — consecutive frames 2s apart are pixel-identical]. The single moving-camera shot in every measured window is a slow lateral track tied to a walking body [V1 09:52.9–09:59.8]. Camera movement is rationed to bodies in motion; everything else is a cut.

**CD-2. Push-ins are cut-in steps.** The "push" is achieved by cutting to tighter framings — the S5 mask hold is ~10s across ~4 discrete scale steps ≈ 2.5s per step, no interpolated zoom [V6 01:53–02:05, 00:57→01:04]. Emotional peaks are handled by cutting IN, not pushing in [V4 08:12–08:14]. A true continuous push is therefore a *marked event* — reserve it (FIRST LICKS has exactly one sanctioned: the cold-open Sacred Object push).

**CD-3. Speed is art direction, not camera.** Fast travel reads via horizontal speed-streak backgrounds under a locked camera and a crisp subject [V3 11:54, 12:19; V6 03:05]. Cheap, boardable, register-compatible.

**CD-4. Low angle = power, and it's rationed.** Worm's-eye and low angles are reserved for the armored/powerful party or the surrounded moment [V6 01:24, 03:00; V3 12:42–12:45; V1 04:52]. Whoever holds power in the scene gets the low angle — the dad in Act 1, the kid in Act 3.

**CD-5. Composition defaults.** Thirds; lower the horizon and put the character off-center for "drama, and interest, and scale" — centered horizon + centered character is Genndy's drawn definition of boring [V2 14:34–14:50]. Exception with teeth: dead-center symmetry is *reserved for ritual/sacred weight* (tiny figure centered between mirrored giant Buddha faces [V1 04:58]; dead-frontal symmetrical close-ups for ritual gestures [V5 07:27]).

**CD-6. Per-shot letterbox is verified Genndy grammar.** Letterbox crashes in AT peak tension and releases: a ~4:1 wide-slice band for an arena wide, an eyes-only slit for an ECU, both mid-sequence [V1 04:47.5, 04:56]; wides letterboxed while interleaved close-ups run full-bleed inside one action sequence [V3 11:38–13:08, 05:25]. Two named variants for us: **wide-slice** (arena geography) and **eye-slit** (pre-strike). See Part 3 for the scope tension with our lock.

**CD-7. Empty stage first.** The environment is observed before the characters enter and disrupt it — vast held masters pre-locate where the action will occur [V3 04:58, 05:15, narration 04:23]. Extends R6.

**CD-8. Format-as-event devices (adjacent to letterbox).** The tiny-window: footage shrunk to a small floating rectangle in a black void, held 10.3s, to compress focus [V5 02:53–03:03]. Panel-stacking: new panels pop onto a held base at ~1.0–2.5s intervals, **the previous panel's moment stays held** [V3 09:49–10:18, narration 10:30; V5 08:14–08:22 — 3 simultaneous season-panels accumulating]. Comic-slit mosaic: one screen divided into wide/eyes/mouth crops simultaneously — shot-sizes without cuts [V5 ~00:52]. Eye-iris framing: a whole battlefield composited inside a pupil [V5 08:23]. The full development of the panel device — **the triptych insert, Sean-ratified for the sever sequence** — is Recipe 6b in Part 2. Otherwise these are candidates, not locks; see Part 3 for the tiny-window flag.

## 3. Staging & silhouette

**SS-1. One rendered figure; everything else is value-mass.** Mid-ground crowds are flat silhouettes with only glowing eyes; the protagonist is the sole modeled figure [V1 04:43]. Two-value staging at climax intensity: black figure on white field ↔ white contour lines on pure black, red as the only third value [V1 13:42–13:47; V5 04:48–05:16; V3 09:15]. The show abandons ALL interior rendering when intensity peaks.

**SS-2. The figure can be the hole in the pattern.** Overhead wide: the frame tiled edge-to-edge with black drones, the fleeing characters read as two tiny gaps of negative space at center, held 2–3s [V6 00:29]. The strongest single composition in the corpus — isolation staged as absence.

**SS-3. Two-step reveal: silhouette first, detail second.** The armored-Jack reveal is a full-black silhouette against a flat gradient (identity withheld), THEN a cut to mask detail [V6 00:57 → 01:04]. Reveals are staged in two cuts, not one.

**SS-4. Threat geometry is drawn as a shape.** ~25 raptors encircling the heroes read as a clean C-arc from overhead — a crowd blocked as a single legible shape, readable at any size [V4 04:24–04:29]. Crowds are shapes, not head-counts.

**SS-5. Profile = glyph.** Action staged in pure profile reads left-to-right like a glyph — run cycles, a spear held horizontal [V1 15:51], a solid-black T-rex profile on a flat pink field [V4 04:39], a silhouetted arm catching a staff, perfectly horizontal, against empty sky, dead-stop [V6 03:17]. Single actions that must read instantly get profile staging.

**SS-6. Scale disparity as dread/reverence.** Subject at ≤5% of frame height against the dominating element: Jack at 2% against a whale skeleton [V1 03:42], a lone hilltop figure held 9.6s [V1 16:24–16:31], a tiny rider under a giant dry-brush spiral sky [V5 05:00–05:08], antagonist-as-landscape (Aku's face fills half the frame, tiny Jack lower-left) [V1 03:44].

**SS-7. Foreground black cutouts build depth.** Flat black thorn/horn/grass shapes cropping the frame edges; a face fragmented behind hard grass verticals, backlit [V6 01:16, 02:05; V4 09:28, 09:21]. Depth from silhouette strips, no rendering. Extends R6.

**SS-8. Posture is the emotion at thumbnail scale.** Happy = arched open; defeated = slumped — the spine-line reads before any facial detail exists [V2 06:57–07:19]. Proportions stay "special": big/small/medium, never even [V2 14:10–14:30, the football-player demo]. The kid-vs-dad size gap should be exaggerated, not naturalistic.

**SS-9. One accent hue on a two-value scheme.** Black silhouette archers + red bows against whiteout [V5 07:26, tower wide]; black drone masses with red-checkered eyes [V3 12:10]. When the frame is two values, a single accent color carries all the reads.

## 4. Silence & sound structure

**SN-1. The single-foley grammar, measured.** In a silence stretch, **every shot names its own foley**: the dark-sequence chain runs one readable element per shot (hoof/stream, hand/ground, two birds, one falling snowflake), 3–7s each, one sound source per shot [V5 07:20–07:52, one 10.5s hold]. Extends R1 with the boarding rule: shot = foley = information unit.

**SN-2. The snowflake principle.** "A snowflake touching the ground tells you a samurai has found his advantage" [V5 08:03–08:08] — the smallest sound carries the biggest information. The climactic foley should be the quietest, not the loudest.

**SN-3. No privileged sound.** "You and Jack are getting the same information through the same means" [V5 07:35–07:39] — the audience hears exactly what the character hears, when they hear it. The string-creak and the sever should hit our ears when they hit the kid's.

**SN-4. Audio leads image out of black.** The Blind Archers reveal: "we blinded him and it was black, and as the audio came up we started to see it" [V2 10:55–11:15, Genndy verbatim]. Sound arrives first, picture follows — the canon inverse of drop-sound-then-snap (R1).

**SN-5. Silence begins ON the cut.** The measured 11.1s of continuous dead air (below −35dB) starts exactly at the cut to black, inside a 24.3s cut-free stretch [V5 06:54–07:08]. Silence is an edit event, not a fade.

**SN-6. The post-climax single-object insert.** Immediately after the loudest moment: one shot, one object, one implied sound — shell casings raining [V6 01:50–01:51] — then the long face hold. The decompression valve between burst and stillness.

**SN-7. Palette removal = sound removal made visible.** The S5 opening ends by draining to black-and-white graphic rain on a held face, ~15s of stillness capping a 24-cut sequence [V6 05:49–05:50]. Color drain signals the emotional dead-stop the way a music drop does. Extends R7/R10.

**SN-8. Production notes for the one-song plan.** Primal's score kit is raw and small — percussion, bass, distorted elements, no orchestra ("complex but still very very simple") [V4 02:32–03:20]. Genndy vocalizes each SFX himself and the designer builds that exact object [V4 03:51–03:58] — **author the single-foley beats as onomatopoeia in Bea's shot cards**. Creature sounds come from wrong-but-right sources (chickens, not lions) [V4 04:19–04:35] — license for the geyser to sound wrong-but-right rather than literal. For a wordless film, Primal's pipeline applies: lock picture timing first, sound reacts to picture [V2 01:34–02:07]. Any kid vocal (an effort grunt) is *cast and directed as acting*, never filler [V4 05:05–05:22].

## 5. Montage & passage of time

**MT-1. The static-shot chain, measured.** The Clone Wars forging montage: **0.4–1.0s locked shots, each showing one action and its consequence**, followable on mute [V3 10:52–11:07]. This is R8's Jump Good grammar with numbers — the montage vignette cell is 0.5–1.5s, one action + its result, then the next cell.

**MT-2. Season = total palette re-key, never a tint.** SJ re-keys the ENTIRE palette per location — one dominant hue + one accent [V1 04:10–04:26]; Primal cycles a full register wheel (teal jungle, red inferno, blue-white blizzard, magenta-on-teal, dusty pink, acid dawn…) with one palette = one sequence = one emotional unit, and never green-grass/blue-sky [V4 palette census across all excerpts; V3 S5 olive fields/green skies; V7-corroborating pastoral frame V1 07:46]. Extends R6/R7/R9: each season vignette hard-swaps the register.

**MT-3. Decay-state prologue.** Elapsed catastrophe established purely through object/environment state over ~26s of dissolves (ruined horizon → smoking village → survivors) [V6 00:00–00:26]. R7's object-decay clock working at sequence scale.

**MT-4. Abstract frames as connective tissue.** Memory/haunting compressed to 1–2s of pure graphics (gold calligraphic swirls on black) instead of a scene [V6 05:00]. Cheap, register-legal transition material between vignettes.

**MT-5. Vignettes may flatten.** Montage interludes drop into flatter, more decorative rendering than surrounding scenes (tapestry-patterned background, repeated grass stars, no perspective) [V1 15:58]. The montage is allowed its own simplified look.

**MT-6. Register-shift-as-flashback is canon.** An entire backstory episode rendered in a one-off style ("literally just line work") [V5 04:12–04:25]. Direct precedent for the 1970s VHS footage living in its own visual register.

**MT-7. Repetition-with-variation mechanics.** Same element at two scales one cut apart (butterfly on the eye → hundreds on the log) [V4 01:51–01:55]; same silhouette repeated at three depths = escalation [V5 06:03]. Extends R4.

## 6. Emotional-beat staging

**EB-1. The fixed-frame feeling shot, measured.** The 8.7s two-shot: camera never moves, bodies never move, the entire content is 3–4 micro facial changes (glance, glance-away, lip press) [V1 09:29.4–09:38.2]. **Template: fixed frame, ≥8s, ≤3 micro-changes.** Extends R10 with a duration.

**EB-2. Holds are alive, not frozen.** "Blinking is part of keeping a character alive, and sometimes even breathing" [V2 04:30–04:53]. Budget one blink or one breath cycle per held frame — nothing else moves.

**EB-3. Emotion lives in duration, not the face.** A literally expressionless mask carries menace for ~10s via stepped push [V6 01:53–02:05]; re-use the same setup and redraw ONE line (a harder brow) for a new emotion [V6 04:26]. Limited-animation acting: change one thing.

**EB-4. Fear/grief = stillness + one drifting layer.** Held close-ups with only smoke drifting over the cel [V6 00:31–00:34]; wide low-angle silhouette against flame CUT TO static face-filling close-up, dead eyes [V4 00:15–00:19]. Two shots, no camera move.

**EB-5. The ritual-gesture shot.** Jack tying his own blindfold: dead-frontal, symmetrical, locked camera, no dialogue [V5 07:27]. Ritual carried entirely by composition — the pre-solved staging for the headband tie-on.

**EB-6. One-shot premise delivery.** A single look establishes the archers are blind — "one that Genndy trusted audiences were smart enough to catch" [V5 06:25–06:32]. One insert, no lingering, no explanation. The photo and the star get this treatment.

**EB-7. Loneliness = figure-to-frame ratio.** A figure walking small behind a window grid, frame dominated by architecture, 6.9s [V1 09:52.9]; grief staged as a centered, tiny, symmetrical figure in a fog field [V4 00:27]. No acting required.

**EB-8. The dread standoff hold: 6–12s.** The bamboo-rain standoff: four consecutive shots of 8.0s / 6.0s / **12.0s** / 11.9s, ~38s total, nothing moves but rain, feeling carried by duration + a single eye-line shift [V3 05:27–06:10]. The fear close-up chain: three consecutive held wide-eye shots, 1.0–2.4s each [V3 12:56–13:04]. The measured ceiling for "past comfort."

**EB-9. Deadpan terminal hold.** Gag → cut to expressionless close-up → hold. The reaction IS the punchline (arrows-in-hat → Jack deadpan) [V5 07:52–08:12]. R4's terminal line as pure image; the Act-3 silence gags land on reaction holds, not on the gag action.

**EB-10. Warm/cool split for quiet scenes.** Campfire two-shot: red fire-side vs blue night-side doing the emotional geometry, held 7.0s [V1 14:48.7–14:55.7].

**EB-11. Mood is enough.** "It sets up a mood… that's the biggest thing from animation that we forget to do… sometimes a mood is enough" [V4 01:14–01:24]. The cold open owes the audience mood, not information.

**EB-12. Choppy is authorial.** "Nobody cares about fluid or smooth. You want great acting… if it's a little choppy, I don't care" [V2 00:53–01:06], with the 24/12/6fps split-screen demos [V2 00:38–00:43]. Motion blur is removed/reduced so poses read as drawings [V1 11:41–11:44] — but the fastest burst pieces are deliberately smeared single frames [V1 15:46–15:48]. Rule: **poses sharp, transitions may smear.** Standing guard for the Motion phase: Seedance must not "helpfully" smooth the burst.

**EB-13. Cap maximal action with maximal stillness.** The 6-minute opening answers its 24-cut burst with ~15 final seconds of one motionless face in the rain [V6 05:49–05:50]; the aftermath of the spider kill is a held gore-reveal then 1.3–2.3s reaction cuts and staring silence [V3 13:16–13:30]. The bigger the burst, the longer the stillness that buys it back.

---

# PART 2 — APPLIED RECIPES

*Shot-level guidance Bea can board from. Hold lengths marked ⚑ exceed the 2–4s in-action band and sit in the hero-hold 6–10s band — **ratified by Sean's §F1 ruling, 2026-07-19** (two-band spec adopted); board them at the stated length, trim at the stopwatch table-read if the runtime demands it (montage trims first — the lock).*

## Recipe 1 — The cold open ("The Sacred Object" push-in + smash-cut)

1. **Empty stage first** [CD-7]: letterboxed dawn wide, locked camera, low horizon, piñata off-center [CD-5]. The yard is observed before anyone enters it — the audience pre-locates the altar.
2. Optional 2-element dissolve chain into position (~5–8s per element, no hard cuts) [CG-9] — e.g., wide yard → the tree/rope. Dawn palette carries "before the world wakes" [MT-2].
3. **The push-in — the film's ONE true camera move** [CD-2]. Everything else in the film cuts in steps; this shot alone pushes continuously, slow, toward the hanging piñata. Total shot ⚑ 6–8s. One foley only: the streamer tick [SN-1, SN-2]. Hold the final framing ~2s past the point it feels done [EB-11 — this shot delivers mood, not information].
4. Optional insert before the cut: the reverent low-angle of Sparkle Horse's face played dead straight [CD-4 — low angle = power, here applied to the absurd relic; the concept doc already plants this].
5. **The SMASH-CUT** [CG-8]: consider 2–4 frames of pure black as the percussion frame between dawn silence and camcorder chaos; the *audio* is the violence — dead silence cuts to clipped, hot camcorder sound ON the cut, not a beat after [SN-5 inverted]. The 4:3 inset + timestamp arrive at full intensity, no ramp.
6. Camcorder-POV grammar per the writers'-room spec (§2.2): POV shots 1–2s and jittery; when the film's own camera takes over at the CLICK, the first composed shot of the kid is a long Cannon hold [EB-1] — fixed frame, one blink [EB-2], world ambience fading up. **The full camcorder behavior spec — the fifteen boardable rules + the artifact reproduce/skip shortlist — is Part 4 §C** (second-pass study of Sean's chosen VHS refs); the POV inventory's long-uncomfortable-hold, drift-reframing, lens-mode cast introductions, and damage-coupled timestamp all come from there.

## Recipe 2 — The Act-1 string-yank humiliation

1. **The ritual staging**: party guests blocked as one legible shape — a C-arc/semicircle around the piñata [SS-4]; from overhead or a wide, the kid reads as the gap in the crowd-shape [SS-2]. Optional god's-eye for maximum isolation [CD-8 usage V3 11:50].
2. **The dad from kid height**: low angle, dad as landscape filling half the frame [CD-4, SS-6]. The size gap is exaggerated, never naturalistic [SS-8]. The kid's walk-up can read through foreground legs/streamer cutouts [SS-7].
3. The call-up line lands in a held frame; the stick toss and flinch are a two-pose switch [R3], the laughter a hot audio bed.
4. **The swing runs the three-beat unit** [CG-1]: *about-to-happen* — kid winds up, 2–3s anticipation hold [CG-2]; *happens* — the yank + face-plant in 0.7–0.9s cuts, or one drawing exiting frame [CG-7]; *relax* — 3.5s+ aftermath wide of the kid down [CG-2].
5. **The yank itself** is one static cell: dad's hand insert, one action + its consequence [MT-1]. We hear the string creak exactly when the kid does [SN-3].
6. Aftermath: stillness + one drifting layer (a settling streamer) over the face-plant [EB-4]; the cruelty calibration (kids roar / adults wince / dad alone enjoying) reads in ONE held wide — posture does the work at thumbnail scale [SS-8].

## Recipe 3 — The Act-2 turn (room / box / tape — the no-joke zone's pacing)

*The zone where cut density falls to near zero. 20s+ cut-free stretches are licensed by the reference [CG-4, V6's 23s fear sequence]; drift and micro-dissolves only.*

1. **Party exit → hallway**: loneliness as figure-to-frame ratio — the kid small behind the house's architecture, locked camera, 6s+ [EB-7]. No music from here to the tape (the lock).
2. **Her door / the room**: the palette drains toward the desaturated end of the register as he crosses the threshold [SN-7 — color drain = sound drain]; warm/cool split once the TV comes on [EB-10]. Room foley only, one source at a time [SN-1]. The room reads as set dressing in held frames — no inventory cutting; the Room-as-Biography texture sits in ONE composed wide plus at most two inserts.
3. **The box**: single-element close-ups, 3–7s each, each cut naming its own foley — lid-slide, cloth, the headband's weight [SN-1]. Near-black surrounds; the object is the only rendered thing [SS-1].
4. **Photo + inscription**: one-shot premise delivery [EB-6] — one insert of the photo (her mid-kick, the star in hand — never called out), one insert of the handwriting. No lingering, no re-cut back to it. Trust the audience; the freeze-frame reward stays unspoken.
5. **The grief beat**: fragment close-ups + concealment — never a full clear face at the thesis moment [V4 08:33–09:15]; fear/grief = stillness + one drifting layer (dust in the TV light) [EB-4]. Fixed-frame holds ⚑ ≥8s with ≤3 micro-changes, one blink [EB-1, EB-2].
6. **The headband tie-on** (the zone's exit): the ritual-gesture shot, pre-solved — dead-frontal, symmetrical, locked camera, no dialogue [EB-5, CD-5's sacred-symmetry exception]. This is the one dead-center composition the kid gets before Act 3.

## Recipe 4 — The VHS glitch match-cut (the film's hinge)

1. **He presses play**: the 4:3 inset returns exactly as the cold open taught it [shared-treatment lock]. The home movie runs warm: her boombox song thin through the camcorder mic, the laugh — her only voice — inside it.
2. **The glitch**: sound drops ON the glitch cut [SN-5] — the song/laugh dies mid-phrase, not fading. The intrusion may pass through 1–2 abstract graphic frames before resolving to the literal 1970s footage [MT-4] — tracking-noise as calligraphy, register-legal.
3. **The 1970s footage lives in its own visual register** [MT-6] — degraded, higher-contrast, its own linework weight; the reference canon explicitly supports a flashback carrying a different render style. (Two-value white-on-black abstraction [SS-1] is available if the literal-footage version reads too soft — Art Dept option, not a lock.)
4. **Audio leads image** [SN-4]: her 1970s audio (a mat-slap, a breath, the same song on a worse speaker) resolves a beat BEFORE her image stabilizes. The reveal arrives through the ears first.
5. **The match cut lands on the articulation point** [CG-6]: his childhood game-move and her form cut together at the identical pose apex — both staged in profile so the shared silhouette reads as one glyph [SS-5]. Repetition-with-variation is the proof mechanism [MT-7]: same silhouette, two eras, one cut. **Second-pass alternative (Part 4 §F): the same-composition match-DISSOLVE** [V12 00:39–00:48] — hold one composition line-for-line constant and dissolve time through it (~3s per stage, darkening as it lands); S5 uses exactly this for its young-eyes→adult-eyes age transition. The hard cut and the dissolve are both reference-canon; the animatic A/Bs them.
6. **The detonation is in him, not on screen**: after the match cut, return to the kid — fixed frame, ≥8s ⚑, ≤3 micro-changes [EB-1]. The wordless-reveal verification gate (concept §gates) tests exactly this sequence; nothing in this recipe adds narration.

## Recipe 5 — The montage vignette template + the Lane-D tree visits

**The vignette cell** [MT-1]: locked camera, 0.5–1.5s per cell, one action + its visible consequence per cell, followable on mute. A vignette = 3–6 cells + ONE recovery hold ≥3.5s [CG-2's flurry/recovery]. The delayed-payoff gags (snowmen, dandelion) put the consequence in the recovery hold — the flurry plants, the hold pays.

- **Season = total palette re-key** [MT-2]: one dominant hue + one accent per vignette, never green-grass/blue-sky. The boombox-decay calendar rides inside whatever palette owns the season [R7].
- Speed reads via streak backgrounds, never camera [CD-3]. Vignettes may flatten into more decorative rendering than the acts [MT-5].
- Escalation staging: same silhouette at growing scale/depth [MT-7]; posture tells the year — the spine-line straightens vignette to vignette [SS-8].
- **Panel-stacking is the sanctioned season-rotation device** [CD-8]: 2–3 season panels accumulating on black at 1–2.5s intervals, the prior panel held — one composite shot instead of three cuts. Candidate for the seasons-turn joint between vignette blocks.
- Abstract 1–2s graphic frames as connective tissue between blocks [MT-4].
- **The Lane-D tree visits** (D3 rope-spine + D5 home-movie rhyme, per the room rec): quiet-beat camera — locked flat-profile framing, the waterline/horizon rule [V4 04:24 Fang-drinking grammar]. Each visit re-stages the tape's composition exactly [D5]; the rope close-ups are single-element single-foley shots [SN-1]. The final full replica wide is earned ONCE and held ⚑ 8–10s, her space empty, petals filling it for one beat [EB-13's stillness logic; the concept's lock].
- The mid-montage second-compartment discovery replays Recipe 3's box grammar in miniature (two shots: lid, star) — same foley discipline, no new staging vocabulary.

## Recipe 6 — The Act-3 snatch-leap-throw-sever multi-cut

*The film's one burst. Total sequence board quota: 30–60 thumbnail poses for ~5s of screen action [CG-5].*

1. **The standoff**: kid and dad at extreme opposite frame edges, tiny, huge negative center [V3 06:12]; eye-slit letterbox on the kid [CD-6]. Pre-strike hold ⚑ 6–8s [EB-8] — the reference's dread band, well past the locked 2–4s (Sean's §F1 call). One foley inside it [SN-2 — the smallest sound: the string settling, a cicada stopping].
2. **The stick-snatch — pre-solved by the reference** [SS-5, V6 03:17]: empty sky field, stick enters horizontal, the kid's arm enters, FREEZE. One-pose silhouette against nothing. Hold the caught pose 2–3s [CG-2]. (This is also the competence plant's payoff — same staging as the Act-1 catch, escalated.)
3. Optional last breath: one pure-object/weather shot before the burst — a petal, the taut string vibrating [V4 09:46–10:06's atmosphere dead-stop; SN-1].
4. **The burst** [CG-3]: ~2.5s total. Two legal constructions: (a) 6–8 editorial cuts at 0.7–0.9s — charge / leap low-angle [CD-4 — the kid now owns the low angle] / dad's hand starting the yank (the ONLY dad cut, hand only, never in the sever frame — the lock) / the throw's wind-up / release; or (b) fewer cuts + 15–20 pieces of 1–5 frames at the peak. The throw itself: anticipation gets the drawings, the release is ONE drawing exiting frame [CG-7].
5. **The sever instant**: a 1–2 frame white or palette-color flash as the impact punctuation [V4 10:06] — register-safe percussion. (The polarity-inversion strobe is the stronger reference device but is flagged, not applied — Part 3 §F4.) The flight line composes toward tree/piñata; profile staging keeps the trajectory a glyph [SS-5; the star-targets-string lock].
6. **The angle-change cut lands on the articulation** [CG-6]: the one new setup is spent on the sever/land moment, not on coverage. Full-silhouette rendering is licensed at the peak [SS-1].
7. *Relax with the aftermath* [CG-1]: the kid lands, dead-stop, held 3.5s+ before anything else happens [CG-2].

The triptych insert (Recipe 6b) is sanctioned inside this sequence — as the pre-strike simultaneity beat or the sever instant itself.

## Recipe 6b — The triptych insert (the split-panel simultaneity shot)

*Sean-ratified 2026-07-18 for the piñata cutting scene (his supplied reference still: the Three Blind Archers triptych excerpted in V1 — described below). This develops CD-8's panel devices into a full spec for boards, frame generation, and motion.*

**What it is.** One dramatic moment split across three vertical panels inside the 16:9 frame, hard black gutters between them — the comic-page inheritance made literal. It is NOT three cuts: it is **simultaneity** — three facets of the same instant held together, substituting for coverage [CG-6's economy: it replaces the close-up cuts you'd otherwise spend]. Measured panel behavior from the reference corpus: panels can pop on sequentially at ~1.0–2.5s intervals with **each previous panel's moment staying held** [V3 09:49–10:18], or sit as one static composite [V5 ~00:52, 08:14–08:22].

**Anatomy of the reference still** (SJ, the Blind Archers tower fight, via V1's excerpt): three vertical panels, each ~1:2.4 portrait inside the widescreen frame.
- *Left panel — the face.* Jack close-up, hat brim, locked stern eyes, the sword's wrapped hilt raised vertical before his face; dark teal night-forest field behind him. A red-fletched arrow lodged at frame edge.
- *Center panel — the body in the field.* Three-quarter shot, white-gi figure against the pale snow field, sword drawn upward, red arrows bristling from his back — the whole stakes readable as silhouette + accents.
- *Right panel — the instrument.* Extreme close-up, the blade running diagonal across the entire panel, hilt top-corner, a sliver of red fletching entering from the edge.

**The grammar rules it encodes (all boardable):**
1. **Content triad = face / body-in-field / instrument-detail.** Not a zoom progression — three *kinds* of information: intent, situation, means.
2. **Value alternation between adjacent panels** (dark ↔ light ↔ lighter) so the gutters read and each panel keys its own field [SS-1's two-value logic applied per panel].
3. **One accent hue repeats in all three panels** (the red arrows/fletching) — the thread that makes three frames one moment [SS-9].
4. **Diagonal continuity across gutters**: the blade's line in one panel implicitly continues into the next — the panels compose as one hidden super-image.
5. Each panel individually obeys the existing staging rules: one rendered subject, silhouette-first, profile-for-glyph where there's action [SS-1, SS-5].

**Deployment map for FIRST LICKS:**
- **Primary (ratified): the Act-3 sever sequence** — as the pre-strike simultaneity beat (replacing coverage cuts before the burst) or as the sever instant itself. Content triad: *the kid's eyes* (headband, locked) / *the full leap arc against the sky* (body-in-field, string and piñata in frame) / *the star* (spinning detail, or the taut string's fibers). **Lock compliance:** no panel contains the dad — the star-targets-string rule applies per panel exactly as it applies per shot; the flight-line diagonal composes toward tree/piñata across the gutters.
- **The rhyme (proposed, cheap, strong): an Act-1 yank triptych in the SAME layout** — *the kid's squeezed-shut eyes* / *the mid-swing body* / *the dad's fist on the string* (his weapon moment — legal here; the hand ban is on the sever frame only). Same format, opposite meaning, one year apart: the party-2 same-composition escalation rule applied to the film's formal language itself [R7's fixed-frame delta]. If adopted, the Act-3 triptych's third panel replacing "his fist on the string" with "her star in flight" IS the movie.
- **Sparingly elsewhere:** one montage skill-payoff moment at most (a petal-pin: eyes / stance / cap striking) — more than that and the device stops being an event [same rationing logic as letterbox, CD-6].
- **NOT the glitch match-cut.** The wordless-reveal gate lives on the CUT carrying the inference (his game → her form, sequential); a side-by-side simultaneity panel would hand the audience the comparison and cheapen the detonation. Flagged, not sanctioned.

**Generation guidance (stills):**
- **Generate each panel as its own image with its own prompt** (portrait crop, ~1:2.4 — e.g. a 640×1536 region), then composite with hard black gutters in the edit (FFmpeg/compositor). Do NOT one-shot the full triptych in a single generation call by default — image models blend panel contents and duplicate the subject across panels; a single-call triptych is a spike to run, not an assumption. (Feasibility note for Flo: three standard_keyframe generations + a $0 composite, not a new route.)
- Per-panel prompts carry: the register clause (unchanged), the panel's single subject, its value field ("dark field, light figure" / inverse), and the shared accent clause repeated verbatim in all three ("a single [accent] element: …") so the thread survives independent generations.
- The diagonal-continuity trick is a composition instruction per panel ("blade/string/flight-line crossing the frame diagonally, entering from lower left"), tuned so the composite lines up — expect one re-roll on the middle panel to make the diagonals meet.
- Bea boards a triptych as ONE storyboard panel with three cells + the pop-order annotation (which panel lands first/second/third, or "all at once").

**Motion guidance (in cost order):**
1. **$0 default — static composite + sequential panel pops in the edit**: panels arrive at ~1.0–2.5s intervals matching the measured reference cadence [V3 10:09–10:18], prior panels held; the whole triptych IS a hold (a ~3–4s beat total), so no generated motion is required at all.
2. **One-panel micro-motion**: Seedance animates exactly ONE panel's clip (the star spinning; a blink) while the other two stay held stills — the one-moving-element discipline [EB-2] applied to the format. Composite in FFmpeg.
3. **Never run motion across the whole composite** — an image-to-video pass on the full triptych will move all three panels at once and warp the gutters; it breaks both the held-panel grammar and the frame geometry. If two panels must move, generate their clips separately and composite.

## Recipe 7 — The geyser over-the-shoulder reveal

1. **Composition**: low horizon sells the geyser's height [CD-5]; the dad is a black foreground mass/occluder (facing the wrong way — the lock), the geyser the single rendered event behind his shoulder [SS-7, SS-1]. His silhouette gets the one accent treatment (koozie, collar) so he reads while unrendered [SS-9].
2. Cut straight from the sever flash to this wide — no intermediate coverage [CG-6's post-action tightening comes later].
3. **Hold it** ⚑ 4–6s as the liquid pours [EB-13]. The geyser is the film's "indulgence" — it must be genuinely maximal to buy the silence that follows [Part 3 §F6]. Oil-spill flow, liquid only (the lock; the reference substitution canon backs liquid-as-aesthetic [R5, V3's wire-viscera confirmation]). **The liquid itself is spec'd in Part 4 §B (Sean-directed, 2026-07-18): a rainbow WATERFALL spraying DOWNWARD** — flat stacked cel bands with scalloped edges, dark source lip with drip-tongues, white foam strands, cloud-pile impact, boil-cycle-on-2s motion at constant speed. Generation and Seedance prompts draw from that spec verbatim.
4. **The decompression insert** [SN-6]: one object, one sound — the severed string-end fluttering down, or the first fat droplets hitting the grass. The shell-casing move. This single foley is the hinge between the burst and the silence.
5. Optional aftermath geography: god's-eye top-down of the party frozen around the spreading pool [V3 11:50 usage; SS-4 — the crowd as a shape around the event].

## Recipe 8 — The long held silence + gags

1. **The master silence**: fixed wide, ⚑ 8–12s licensed (11.1s shipped in the reference [V5 06:54]; the S5 opening caps 24 cuts with ~15s of stillness [EB-13]). Silence begins ON the cut [SN-5] — the geyser's roar dies the frame the wide arrives. ≤3 micro-changes in the frame; blinks and one drifting element keep it alive [EB-1, EB-2, EB-4].
2. **Each gag = one static cell + one foley + a deadpan terminal hold** [MT-1, SN-1, EB-9]: the gag action reads in 1–2s, the *reaction hold* is the punchline (2.5–3s). Flash-flinch (C1): the flash is a 1–2 frame white insert [CG-3's percussion grammar — an edit insert, as the writers' room already spec'd]; everyone's flinch is a single simultaneous two-pose switch [R3], the kid mid-stride unmoved. Ice-sculpture arm (C9): one crack, one wet thud — action + consequence in one cell [MT-1]. Patient zero (C4): close shot, one slow action, the verdict registering as ONE redrawn line on his face [EB-3].
3. **The dad's mute**: the expressionless mask hold [EB-3] — his face carries the loss by duration, not expression; the involuntary respect-flash at the fence is the same setup with one feature redrawn [V6 04:26], then the shake-off two-pose switch.
4. Audience foley = character foley throughout [SN-3]: we hear the drips, the single flash-click, the thud — nothing scored, nothing sweetened (one-song lock).

## Recipe 9 — The walk-off

1. **The poster shot**: the kid in pure profile, flat silhouette against the dawn-warm field, figure at 5–15% of frame height [SS-5, SS-6; V4 04:39's two-value profile]. Locked camera — or the film's one lateral track, tied to his walking body [CD-1], mirroring the cold open's one push (the film's two camera moves bracket it).
2. **The lollipop pluck**: mid-stride, one-pose action reading as a glyph in profile [SS-5]; the arc-and-land is the single-object single-foley insert [SN-6] — the lollipop's tick on the grass is the last diegetic sound before the music.
3. He never looks back (the lock); posture does the transformation — the spine-line from Recipe 2's slump, now straight [SS-8].
4. **The echo rises** as the palette holds warm; no laugh in the exit audio (the lock). Spend the final ⚑ 10–15s on stillness and the walk [EB-13] — the film caps its maximal beat the way the reference caps its opening: with a long quiet figure and nothing else.
5. End card per the lock (the cassette label); a title card on black can carry ~1s of full silence before it [CG-8].

---

# PART 3 — WHAT NOT TO BORROW (+ flagged for Sean)

## Do not borrow (conflicts with locks — keep the lock)

**N1. Primal's permanent letterbox** [V4, every excerpt 00:00–10:06]. Primal runs letterbox as its constant base format — the direct opposite of our per-shot lock. Keep the lock: per-shot deployment is *also* verified Genndy grammar [V1 04:47.5, V3 11:38–13:08], and rationing is what makes the format mean something. Cite SJ, not Primal, for letterbox behavior.

**N2. Primal's music-forward scoring** [V4 02:25–02:31, "music is so important and key"]. Primal scores far more wall-to-wall than our one-song rule permits. The silence patterning we're borrowing (R1) is Samurai Jack's, not Primal's — take Primal's *instrumentation* notes for the song itself [SN-8], not its music density.

**N3. S5's chunky violence substitution** [V6 02:22–02:23]. The S5 opening's robots die in solid black debris + red shards — a *chunky* substitution. Our geyser is locked liquid-only; the classic-era oil-for-blood logic (R5) is the right ancestor, and V3's wire-viscera reading [13:16–13:30] confirms substitution-as-aesthetic. Do not let geyser boards drift toward solid pieces because the S5 reference does.

**N4. Wall-to-wall letterbox switching** [V3 11:38–13:08]. Genndy alternates letterboxed wides with full-bleed close-ups several times a minute through ordinary action. Our lock restricts letterbox to the cold open + peak tension. Keep the lock (tighter = the format stays an event) — but Bea should know the homage source is looser, so a *peak-tension sequence* may legally alternate letterbox/full-bleed within itself rather than holding one matte for the whole sequence.

**N5. Protagonist commentary / explanatory coverage.** The reference's refusal of it is load-bearing [V5 07:28–07:33's mock title card; EB-6's trust-the-audience rule]. Nothing in the turn or the reveal gets an explaining insert, a second look at the photo, or a reaction line. Already our lock (wordless-reveal gate); the videos confirm it from the craft side.

**Confirmed-clean:** nothing in any of the six videos contradicts star-targets-the-string, liquid-only geyser, or climax-never-through-camcorder — no video touches found-footage devices at all, so the camcorder rules stand on the concept doc's own authority.

## Flagged for Sean (the reference argues for a change — tradeoffs listed, nothing applied)

**F1. The hold-length re-spec (the big one — five independent confirmations). ✅ RULED 2026-07-19 (Sean): TWO-BAND ADOPTED** — in-action anticipation stays 2–4s; the designated hero holds (cold-open push, pre-strike standoff, post-geyser silence, final replica wide) get a **6–10s band**. The ⚑ boards in Part 2 are now the rule, not a pending flag; the stopwatch table-read remains the runtime enforcer (montage trims first, the turn never does). Original flag retained below for the record. The locked rule says pre-strike holds run 2–4s past comfort. The measured reference says 2–4s is Genndy's *ordinary shot*, and his designated dread/tension holds run **5–12s**: 6.5s SJ / 8.7s SBT / 9.7s S5 / 9.6s Primal [V1 hold census]; 8.0/6.0/12.0/11.9s bamboo-rain standoff [V3 05:27–06:10]; 10s mask hold + 15s pre-burst approach + 23s fear sequence [V6]; 11.1s dead air [V5 06:54]. **Proposed re-spec:** keep 2–4s for in-action anticipation; give the 3–4 designated hero holds (cold-open push, pre-strike standoff, post-geyser silence, final replica wide) a 6–10s band. **Tradeoff:** ~15–25s of added runtime against the 3:30–4:00 target — those seconds come out of the montage at the stopwatch table-read (the lock already orders it: montage trims first, the turn never does). Part 2 boards to the reference band with ⚑ marks; the stopwatch read is where this gets decided.

**F2. Burst spec should be numeric in the brief.** "Buildup in seconds, the strike in frames" is right but unquantified; the measured spec is **~2.5s total, 15–20 pieces of 1–5 frames (or 6–8 cuts at 0.7–0.9s)** [CG-3]. Recommend writing the numbers into the studio brief's timing non-negotiable so Sam/Bea/the animatic inherit them. Low-risk adoption.

**F3. The three-beat unit as a standing checklist.** *About-to-happen / happens / relax-with-aftermath* [V3 15:02] is a per-action completeness check the brief doesn't currently state. Recommend adopting into the timing bible — it's the rule the Act-1 yank and Act-3 sever recipes are already built on.

**F4. The polarity-inversion strobe (borrow or refuse — a real style call). ✅ RULED 2026-07-19 (Sean): OUT** — the two-borrows discipline holds; the sever's percussion is Recipe 6's 1–2 frame white/palette-color flash [V4 10:06]. (A strobe is edit-side cheap, so the door stays open in the edit if the sever underwhelms — nothing strobe-specific is boarded or generated.) Original flag retained below for the record. Genndy's signature burst intensifier: full-frame value/palette inversion cells strobed at 1–5 frames [V1 14:04, V5 04:56, V6 01:46, V3 12:26]. It would give the sever maximum violence at near-zero animation cost — but it's a *strong* SJ-S5 signature (reads as muzzle-flash lighting), and FIRST LICKS already limits itself to two deliberate cross-register borrows (geyser + gross-up). Adopting a third needs Sean's explicit call; the safer default already in Recipe 6 is the 1–2 frame white flash [V4 10:06], which is percussion without the signature. **Tradeoff:** unmistakable Tartakovsky electricity vs. diluting the "two borrows, each earned" discipline.

**F5. The tiny-window device for the VHS beats** [V5 02:53–03:03]. Footage compressed to a small floating rectangle in black void (10.3s hold) — a focus device that *rhymes* with our 4:3-inset treatment but isn't covered by any lock. If the glitch moment wants one shot where the home movie shrinks to a tiny island in darkness (the world reduced to the tape), this is the tool. Needs Sean's call because it's a new format event beyond the shared VHS treatment spec.

**F6. The indulgence balance** [V5 05:19–05:28]. The essay's thesis: Jack's silence only works because the show indulges maximally in between. FIRST LICKS is quiet nearly wall-to-wall with ONE loud event. Not a rule conflict — a calibration warning: the geyser and the montage's loudest vignettes must be genuinely maximal (scale, liquid volume, color saturation) to pay for the film's silence budget. If the geyser is polite, the silence reads as slow instead of earned.

**F7. Smoothness is the enemy at the Motion phase** [V2 00:53–01:06; V1 11:41]. Not a boards issue — a standing production guard: Seedance's native smoothing fights the pose-held grammar. Poses sharp, transitions may smear [EB-12]. Recommend this line ride into the Motion-phase prompts and Em's Act-3 review criteria when that stage comes.

## Coverage gaps (honest ledger — updated after the second pass)

- **No true montage-vignette timings from Jump Good itself** — MT-1's 0.4–1.0s cells (Clone Wars) plus V13's massed-combat ASL data are the best measured proxies. Verified candidate links for a Jump Good pass are on file if wanted (the official CN clip, 2:03).
- **R1's SJ-ep8 burning-tree ~1:20 hold was neither confirmed nor re-measured**; the number still rests on the text source.
- ~~V6's narration is unheard~~ **CLOSED (2026-07-18):** Whisper-transcribed on the second pass — mined in Part 4 §A. It is performance narration (no stated hold-lengths or process talk), so V6's *visual* timings remain the quantitative source.
- **No foley-level timing from V1/V3/V4** (essay narration masks source audio); the silence math comes from V5 alone.
- **Crowd-wide simultaneous pose-switch (the C1 flash-flinch) still has no found reference** — the search returned nothing usable; the planned 4–5-figure viz test is the cheaper answer.
- Auto-caption garbling in V3 ("Gandy/Candy" = Genndy; "hallasan Whitaker" = Halas & Whitaker's *Timing for Animation*).

---

# PART 4 — THE SECOND PASS (2026-07-18, Sean-directed)

*Seven additional /watch passes run on Sean's picks: the V6 narration capture, two waterfall look-refs for the geyser, three camcorder VHS refs, and four more Tartakovsky sources. Same discipline: cited, nothing silently absorbed. This part is the delta layer — where it refines a Part-1 rule or Part-2 recipe, the pointer is explicit.*

## §A — V6 narration capture (what Genndy's own words add)

Whisper-transcribed on the second pass (near-complete, 00:00–05:45; the two speech-free stretches — 04:33–04:48 and 05:45–end — fall exactly on the two biggest holds the frame pass measured, independently corroborating them). It is beat-by-beat *performance* narration, so intent shows in camera verbs and withholding, not stated theory. No timing contradictions. Extensions:

- **Relabel: the gold calligraphic frames [V6 05:00] are the KILL rendered abstractly**, not a flashback — narration at that beat: "right through his whole body… pulls it out." MT-4's "abstract connective tissue" reading stands, but the device's canonical use is *violence abstracted*, which strengthens its candidacy for the sever instant, not just transitions.
- **The shell-casing insert and the mask hold are ONE designed unit** — "Shells coming out on his face" [~01:54], released by a reload click ("Stops. Click. Let's go." [02:03]). SN-6's decompression insert can play *over* the held face rather than as a separate cut — a composite option for the post-geyser beat.
- **The reveal opens as a pan down the horns** ("down these cool-ass horns to this mysterious samurai" [00:52–01:12]) — SS-3's two-step reveal carries one sanctioned camera move: a descend-the-landmark pan into the held silhouette.
- **"Antic" [03:40]** — the one animation-craft word in the whole narration, used for the staff wind-up: anticipation is the unit he thinks in (CG-7 from the horse's mouth).
- **"Not a word." [05:29]** — Jack's total silence across the sequence is named as design; and the live "Oil. Gush of oil. Sorry." [05:18] confirms R5's substitution-as-aesthetic with a knowing laugh.
- New device logged: a **split-screen insert mid-slow-mo** ("we split screen down in, close on the tire" [~02:34]) — kin to Recipe 6b's panel family.

## §B — The geyser spec (V7 + V8 + Sean's direction)

**Direction locked by Sean 2026-07-18: the geyser reads as a RAINBOW WATERFALL SPRAYING DOWNWARD** — V7 is "pretty much exactly what I had in mind." This supersedes any upward-fountain read of "geyser" in Part 2; Recipe 7's composition (over-the-shoulder, low horizon, liquid-only) stands, with the liquid itself now spec'd:

**Look (stills — gpt-image/NB2, register-adapted):**
- One continuous **sheet/column** pouring down from the severed piñata: hard-edged silhouette, narrow at the source, widening toward impact, gently wavy edges [V7 00:02, 00:10].
- **Rainbow as flat stacked cel bands, not a gradient**: warm-desaturated red-orange at the source → ochre-yellow → olive-green → teal-blue at the base, spectrum stacked top-to-bottom; each band a flat drippy shape with **rounded scalloped edges** — layered spilled paint / oil-slick logic [V7 00:02–00:07].
- **Dark shadow mass at the source lip** (under the piñata), its bottom edge hanging in 3–6 uneven rounded **drip-tongues** — the darkest value sits at the top and pushes the eye down [V7 00:00, 00:13–00:19].
- **Cream-white foam strands**: long tapering vertical streaks with rounded tips running down through the color bands — the lightest value, carrying the vertical read [V7 00:13–00:14].
- Impact swallowed by a **pile of scalloped foam-clouds wider than the column**, plus a few detached teardrop droplets flung sideways; no ripples, no realistic spray [V7 00:13–00:15; V8 00:20–01:58].
- Three-value discipline per hue (dark source / mid bands / light foam); every edge rounded — scallops, lobes, teardrops, never spikes [V8's 3-value scheme].
- **Register guardrails:** neither reference's finish survives — V7's airbrushed pastel gradient and V8's sterile flat vector both fight `primal-sketch-grit`. Transfer **shape + value + cadence only**; desaturate to the register's warm palette; visible ink linework on every liquid edge. V10's "light is a shape" rule applies: the geyser frame follows the SJ white-slash model — one dominant shape, everything else darkened to ground it [V10 07:01].

**Motion (Seedance):**
- **Boil cycle on 2s (≈8–12 drawings)**: the sheet's silhouette holds nearly still; only interior drip-tongues, foam strands, and scalloped bands **travel downward at constant speed** — viscous oil-pour cadence, no acceleration, dreamlike not ballistic [V7 measured at 00:13.2–00:13.9; V8's conveyor-band descent at 01:00].
- **First-eruption beat**: the leading edge descends as elongating rounded finger-tongues, tips first, mass following (≈one-third of fall height per second), then settles into the cycle [V7 00:18–00:19].
- Splash droplets pop in fully formed, vanish after 2–3 frames; foam-clouds boil in place; fixed camera [V8 00:30–01:40].
- Cross-feed from V13: the piñata carries a **damage ledger** before the burst (cracks/seams accumulating across cuts, like arrow-studded armor [V13 342.7–344.5s]); the sever contact itself may render as a **full-frame graphic star-emblem for 1–2 frames** [V13 348–350s]; and the geyser-over-black-crowd-silhouettes contrast model [V13 336.5s] is the wide's value scheme.
- **Re-scope: the Beetle Drone battle (the Episode III oil fight) is NOT a geyser reference** — Sean's review: smoke and explosions, no waterfall/geyser behavior. Retained as a reference for smoke/explosion abstraction and Tartakovsky violence grammar generally.

## §C — The camcorder grammar (V9a/b/c → the cold open + shared VHS treatment)

Sean's direction: **V9a is "very much the camcorder style I was envisioning"** (animated, not live-action); pull aspects from V9b/V9c. One aspect flag up front: V9a is full-frame 16:9 while the locked treatment is 4:3-in-16:9 — **keep the 4:3 lock** (V9b, the artifact-truth reference, is native 4:3 and the pillarbox does story work); steal V9a's *behaviors*, not its aspect or its transition theater.

**The fifteen boardable rules** (each tied to cited observation; full per-video data in the watch notes):
1. **Cut = record-stop, and the timestamp is the cut** — every scene change jumps the OSD clock (V9b: 6:52 PM → 7:35 PM → 12:18 AM in ~20s of runtime; V9a: 9:12 → 10:03 PM); story time lurches, the clock silently confesses it.
2. **One cut = 1–2 frames of garbage + an audio pop** (V9c 01:32; V9b 00:49–00:50). Never full transport screens (STOP/REWIND/EJECT) — that's the app-recreation tell [V9a 00:04, 06:11].
3. **Board one long uncomfortable hold**: the operator plants on one mundane action and outstays it with micro-reframes (V9a's ~11s+ drink-pour hold at 01:41–01:52). The "Happy Birthday" song IS this hold.
4. **Reframe by drift, never by cut; keep the occlusions** — a foreground head/back can eat a third of frame and stay (V9a 01:44–01:46; V9c 00:53).
5. **Whip pan = the drawing dies**: directional streaks + ghost trails, one sub-second legible landing between smears (V9b 00:33–00:40). In ink: dry-brush streaks along the pan vector, one clean drawing per landing.
6. **The OSD survives motion but dies with damage** — the timestamp stays crisp through smears (playback-generated) yet shreds with dropout/tearing, sometimes corrupting single characters (V9b 00:50, 00:31; V9a 01:50, 04:01). **The highest-value authenticity detail in all three refs.**
7. **The operator is a near-mic voice, not a face** — loudest audio object, narrating/interviewing; subjects answer to a point just off-lens (V9a 00:52; V9b 00:08). Exactly the faceless adult.
8. **Introduce the cast by lens-mode**: performers who mug the instant the glass finds them vs obliviouses shot from behind (V9c ~00:20, 01:01; V9b 00:24 vs V9a 00:45). Each character's first frame declares their mode — the cold open's POV inventory, confirmed from life.
9. **Blowouts stay blown**: clip to paper-white, recover on a slow 1–2s ease, never a pop (V9b 00:28).
10. **Low light = two values + crawling streaks**; an on-camera light carves subjects out of absolute black, interrogation-style (V9a 02:42; V9b 00:24).
11. **Timestamp discipline**: one internally consistent, physically plausible format — 12h clock + AM/PM + date, advancing in real time within scenes, date rolling at midnight (V9a 03:11→03:19). Never PM + 24-hour (V9c's giveaway); never indestructible text.
12. **Crowd-crush POV beats**: at peak party, hair/fabric/backs fill 100% of frame for a beat (V9a 03:19–03:29).
13. **Filming a screen in-world gets its own artifact set**: CRT content blows into rainbow chroma/moiré with a tear band (V9b 00:00–00:08) — reserve for the Act-2 tape's TV playback framing.
14. **Hardware limits are story beats**: a battery/tape clock justifies why the cold open ends when it ends ("battery's getting pretty low—" cut to garbage, V9b 00:54; BATTERY LOW corner OSD, V9c 00:41–00:46).
15. **Audio: one hot mono mic** — holder's voice dominant and dry, distant speech thin, music swallows dialogue, cheers/song peaks clip hard (V9a measured −0.3 dB ceiling-riding; V9c 0.0 dB pinned). Mid-song "Happy Birthday" should already distort on the downbeats.

**Shared-VHS-treatment artifact shortlist — REPRODUCE:** bottom-edge head-switching noise band (always on); damage-coupled timestamp corruption (rule 6); 1–2-frame cut garbage + pop; chroma fringe on high-contrast edges only; whip-pan smear + one-frame landings; blowout-slow-recovery; low-light dropout streaks + two-value crush; subtle line jitter on holds; the BATTERY LOW corner state. **SKIP:** full-screen transport UI; interlace combing (invisible at delivery size, fights the linework); constant global grain (the register's ink grit already supplies texture); app-chrome labels ("TBC"); a uniform nostalgic LUT (let color drift per scene); vignette (reserve for the CRT shot); constant autofocus-hunt (one brief focus-breathe is plenty).

## §D — Background craft procedure (V10 → the Art Department)

V10 is an artist's hands-on recreation of **Scott Wills' actual in-house background tutorials** (authored to train the overseas studio [V10 02:00–02:14]) — the look was codified as a teachable recipe, which is precisely what our register spec is. The procedure, register-agnostic:

1. **Layout first** (drawn base before any paint) [02:09–02:14] → 2. **big-shape masses** (thumbnail the value masses before detail) [05:06–05:19] → 3. **texture INSIDE the masses**: the "sponge revelation" — canonical SJ masses are NOT flat up close; they carry dry granular texture behind razor edges [04:27–04:47, 07:19] → 4. **counted accents**: one warm note + one secondary family per scene, everything else in the cast hue [06:01–06:55] → 5. **three-mark detail pass**: suggestion, not rendering (crack-lines, dot clusters, silhouette props) [06:45].

- **The bridge to `primal-sketch-grit`, stated plainly:** primal isn't fighting SJ background craft — it's turning the sponge dial up. The non-negotiables are **value grouping and decisive edges**, not flatness. Group values hard; texture freely inside them.
- **Light is a SHAPE**: the tutorial scene's light shaft is painted as its own flat hard-edged lighter-value shape [02:00] — do the VHS TV-glow, the dawn sunbeam, and the geyser this way (§B cross-ref).
- One-hue-cast-per-scene with a pre-decided ~6–7-mix palette strip [03:29]; two paintings = two times of day = two casts over the same construction [07:19–07:34] — the montage's season swaps, confirmed at craft level.
- **Chroma caveat:** SJ's poster saturation (the S1 Aku footage [06:57–07:01]) must be pulled way down to the register's earthy palette — borrow the structure, not the chroma.
- Bonus staging finds: the doubled-figure smear on the sword draw + the giant single white slash shape filling half the frame [07:01] — both on-register options for the sever frames.

## §E — World rules (V11 → the backyard, the room, party-2)

- **The silence toolkit** [V11 00:16–01:29]: wind through nature, the protagonist's footsteps crossing landscape, and empty-landscape shots with no character — then "complete silence as tension-raiser before a cathartic release of action." The cold open's empty-yard hold, from the source doctrine.
- **The ~6:05 flagged region is the oil-for-blood WORLD rule** [06:07–07:08]: robots exist *so that* full violence is depictable — a constraint converted into a world-population rule, whose targets are then re-weighted as sentient. **This is bootleg maximalism's engine, stated from the source**: pick a class of destroyable object (rentals, piñatas, inflatables), give it a consistent "blood" substitute, then optionally re-weight one (the piñata that stares back — the gross-up shot). Also in that region: the kill registered as an **oil-splat that holds the victim's silhouette on the ground** [06:30] — the candy-burst can persist on the lawn the same way.
- **Landmark + fixture grid** [08:01–08:30]: a location stays readable across scales via one landmark (the temple's red doors) + one repeated fixture (braziers). **The tree is our red doors**; folding tables/string lights are the fixture grid that makes party-1 and party-2 wides read as the same place instantly.
- **The revisit poles** [08:01–08:58 vs 16:31–17:33]: revisit-UNCHANGED = endurance (the temple, same rituals running); revisit-CHANGED = loss (the mossed-over homeland — "the delta between remembered set and present set IS the story beat," no dialogue). **Party-2 sits exactly between and inherits both**: identical compositions (this ritual repeats) with escalated contents (the delta is the story). The tree is the invariant that certifies every other change as real.
- **The restraint doctrine** [19:30–20:37]: SJ is deliberately lore-light; world facts arrive as set dressing and throwaway staging, never exposition — over-explaining "ruins the sense of mystery." One prop = one civilization [15:50–16:25]. For us: the room's props are the entire lore budget; never explain why she trained him. (Friction flag, resolved: the VHS reveal survives this doctrine only as *evidence, not exposition* — which the wordless-reveal gate already enforces.)
- **Tartakovsky's color thesis, verbatim** [21:54–22:05, the video's one direct production quote]: *"The whole show kind of came together from simplicity, and I put it together as like white versus black over red."* Hero value vs antagonist value over an emotional field color — for us: the kid's light shirt vs the piñata/dad mass over the yard's warm field.
- Sky keys: never plain blue; one flat unnatural sky color = one scene's emotional key [frames throughout; blue is *reserved* (otherworldly/night), not banned]. Assign each FIRST LICKS sequence its own sky key.
- **Presence without showing**: glow-silhouettes behind screens (the shoji-screen lantern figures [18:30]) — an option for grandma's presence in the tape or a figure at a window during the montage.
- **Object-as-relic** [10:22–10:53]: the Spartans keep only the shield; a single surviving object + retelling turns an event into myth — the boombox/VHS as the shield.
- Provenance caution: the essayist's intent claims are secondhand except the one direct quote; fine for craft direction, don't cite as production fact in the design bible.

## §F — Cut-grammar refinements (V12 + V13 — numbers the wave-1 rulebook lacked)

**New measured numbers:**
- **Impact/slice flashes are 1–2 frames** [V12 00:16.56 — 2 frames; V13's star-emblem contact frames], distinct from the ~2.5s burst structure. Polarity flashes measured at **single-frame, ~6 frames apart** [V12 00:06–00:07]; the Grievous night-fight strobe runs **~30 flips in 2.67s (~11/sec), and the strobe's colors are the weapon colors** [V13 394–397s] — for us, the sever strobe (if adopted per flag F4) would flash in the star's/string's palette, not arbitrary white.
- **ASL is conditioned on combat type** [V13 measured table]: duels ≈ 2.4s (big readable panels); massed-combat montage ≈ 0.74–1.01s; dread builds run a **~2.3s metronome**. The Part-1 band (1.4–2.4s) is the 1-v-1 figure; FIRST LICKS' sever is a duel-class beat — board at the top of the band.
- **Emotion-scene ASL ≈ 3.5–5s with terminal holds to 9.5s** [V12 measured, n=10 — directional] — the Act-2 turn's tempo now has a number.
- **The anticipation:strike ratio scales to 18:1** at sequence level (46s of 2.3s dread panels : ~2.5s strike, Hypori [V13]) — license to spend nearly the whole Act-3 boarding budget before the throw.

**Rule refinements (wave-1 rules amended, not broken):**
- **The long take is the burst's co-equal opposite mode** [V13 02:03–02:45]: 9.8s/8.6s single-setup locked-wide melee takes, with the craft lint *"no pose is repeated twice"* within a setup. Tartakovsky picks per beat: virtuosity = long take, overwhelming force = burst. A training-payoff vignette could earn one long take; the lint applies to the 30–60-pose thumbnail pass.
- **The flurry/recovery cap (≤1.5s then ≥3.5s) holds for hero exchanges only** — a one-sided "unstoppable" sequence sustains 0.85s ASL for ~26s with recovery only at the end [V13 escort slaughter]. Not our climax's shape (the sever is a hero exchange), but the exception is now on record.
- **"Cut close only after the action resolves" exempts OBJECT inserts**: macro damage receipts (molten seams, arrows-in-plate) intercut mid-flurry; face close-ups still wait [V13 §4]. For us: the string-fibers/star-in-flight macro is legal mid-burst; the kid's face waits for the aftermath.
- **Mid-fight overhead geography check** [V13 02:11–02:22]: an overhead god-shot re-establishing the cleared space *inside* the action — kin to Recipe 2's crowd-shape staging.
- **The intrusion device** [V13 419.6s, 424.4s]: an enemy's position is asserted by a limb entering an empty held frame or a detail shot showing them already there — never a crossing shot. Recipe 2's yank: the dad's hand can simply BE on the string in the insert ("a deliberate break in continuity, masked by timing… never enough to distract" [V13 narrator 06:39]).
- **The grab macro** [V13 599.0s]: a catch rendered as a dedicated 2–4-frame hilt-into-palm insert — the stick-snatch can carry this as a second angle beside the V6 one-pose silhouette.
- **Violence elided into residue** [V12 00:28–00:48]: a massacre staged entirely in aftermath evidence (feet in tinged water, the wiped face, the Loaded-Object insert getting the scene's only sub-2s cut). The Act-1 humiliation's aftermath can work in residue: the dropped stick, the settling streamer, the dad's shadow.
- **The same-composition match-dissolve** [V12 00:39–00:48]: a 9.5s three-stage dissolve on a line-for-line identical eyes-ECU (young → adult → darkening) so seamless the scene detector reads one shot. **The strongest single wave-2 finding for Recipe 4** — an alternative (or complement) to the hard match CUT: hold ONE composition constant (the game-move pose) and dissolve time through it, ~3s per stage, darkening as it lands in the present.
- **Letterbox as memory register** [V12 flashback block letterboxed, present-day full-frame] — S5 assigns letterbox *semantically* to the past. New flag → Part 3 F8.
- **Audio sequence-assignment, Genndy verbatim** [V13 07:52]: "this action sequence is going to be ALL sound effects; this sequence is going to be all music with very low sound effects." Maps cleanly onto the one-song lock: ritual/yank = all SFX; montage = all music (the song); the return = SFX until the geyser, music after. Also [V13 08:29]: designed footsteps + "the less you show, the more you see — less is more" (Hitchcock cited) — the single-foley doctrine from the source.

**New Part-3 items from the second pass:**
- **F8 (flag for Sean): letterbox-as-memory. ✅ RULED 2026-07-19 (Sean): LOOSENED, not fully locked.** Letterbox-as-memory is NOT adopted as a semantic rule (the 4:3 inset owns memory). Cold open + peak tension remain the anchored uses, but the rule is now a **default with latitude**: other scenes may earn per-shot letterbox case-by-case — Bea proposes at boards, Sean gates. Rationing discipline stands (letterbox stays an event, never a base format — N1/N4 unchanged). Original flag: our lock assigned letterbox to cold open + peak tension only; S5 also uses it as a past/memory marker [V12]; the 4:3 inset already marks the VHS material, so adopting F8 would have double-marked memory.
- **Do-not-borrow addition: V9a's transition theater** — full-screen STOP/REWIND/TRACKING screens between scenes read as app recreation, not tape truth [V9a 00:04/02:07/06:11]; the treatment uses 1–2-frame cut garbage instead (§C rule 2).
