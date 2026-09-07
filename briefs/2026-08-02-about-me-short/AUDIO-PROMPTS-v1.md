# AUDIO PROMPTS v1 — music and SFX for ElevenLabs · HOW TO SOLVE A PROBLEM

*2026-09-07. Companion to `VO-SCRIPT-v1.md` and the SFX list in `POST-CHECKLIST.md`. Every cue below is written for
ElevenLabs' Sound Effects and Music generators; durations are sized to the v8 trim lean (`motion/film-roughcut/
FILM-roughcut-v8-trim-lean.mp4`) with a little tail so the CapCut trim has room. Generate 2–4 of each, pick by ear
against the cut, keep the losers in `post/audio/_rejected/` with the prompt that made them. $0 in Higgsfield credits.*

## How to run these

**Sound Effects.** One cue per generation. Set the duration to the cut window + ~0.5s tail. Where the tool has a
"prompt influence" slider: high for literal, single-event cues (a key click, a bell, a cannon), lower for textures and
beds (room tone, paper flutter) so it improvises grain. Tick **loop** only where the row says so. Nothing in this film
has words: if a generation produces a voice, a syllable or gibberish, throw it away (the sighs and the cheer are the two
cues that tempt it; the prompts say "no words" and mean it). Every prompt starts with the sound and ends with what it
is *not*, because the negative is the part these models drop first.

**Music.** Instrumental only. One cue per section, not one cue for the film: the film has a hard silence in the middle
(the record scratch to the replay) and the cut points are the sections' edges. Generate each section 2–3 times with the
prompt variants, and audition against the picture, not on its own; a cue that sounds good alone and wrong under Grok
missing the dartboard is wrong. If the generator takes a structure hint, use the one given; if it does not, cut the
structure in CapCut.

Music never plays under: the swivel, the turn back, the question, the replay, the button line, the black.

---

## MUSIC

### M-A · The brochure bed (title → Movement 2, under the wrong-builds) · ~40–45s, loopable

The film's main cue. 1950s educational-short library music: pleasant, brisk, slightly officious, the sound of a pamphlet
that believes in itself. It must NOT be funny on its own; the picture is funny, the music is straight. It sits under the
narrator, so mid-range light (no strings swelling in the vocal band) and no melodic hooks that fight the words.

- **M-A1 (the lean):** "Instrumental. 1950s educational film library cue, light orchestral: pizzicato strings, clarinet and
  flute carrying a cheerful, orderly melody, brushed snare, a soft tuba on the downbeats, bright and brisk at about 120 BPM.
  Mono-era warmth, slight tape hiss, gently compressed. Pleasant and officious, like a public-information short about
  workplace tidiness. Loops cleanly. No vocals, no modern drums, no synths, no comedic sound effects, no swells."
- **M-A2 (the woodwind version):** "Instrumental. Mid-century instructional-short score: a bassoon and clarinet duet
  walking a tidy little tune over plucked double bass and a light woodblock, a muted trumpet answering now and then, major
  key, moderate tempo, cheerful and unhurried, recorded on an old optical soundtrack with a little warmth and hiss. Repeats
  in a loop. No vocals, no synthesizers, no percussion hits, no slapstick stingers."
- **M-A3 (the busier one, for Movement 2 only):** "Instrumental. 1950s cartoon-short underscore for a busy montage:
  quick pizzicato strings and xylophone runs, a chattering clarinet line, brushed drums with a walking bass, upbeat and
  bustling but still polite and orderly, about 132 BPM, vintage mono recording. No vocals, no drum fills, no
  mickey-mousing hits, no synths, no swells or big finishes."

Use: M-A1 or M-A2 under the title and Movement 1 (0:00–0:14); either continue it or cross to M-A3 at the GO (0:16.7)
and hold under the four builds and the hollow ship. **Cut the music dead** on the record-scratch frame (0:49.9 in v8);
do not fade it. Whether it survives the two alarms is your ear: the classic move is the music *drops* on alarm #1's hit
and comes back a bar later, and drops again on alarm #2 and does not return.

### M-B · The pit-stop build (the delegation → the SHIP key) · ~12s

The film's one flourish. The same 1950s band, now playing a fast, precise, F1-tidy figure: rising, mechanical, delighted.
Ends on a clean stop as the SHIP key is pressed.

- **M-B1 (the lean):** "Instrumental. 1950s cartoon-short action cue, 12 seconds: a fast, precise, rising figure on
  xylophone and pizzicato strings with a brisk snare roll underneath and a muted trumpet stabbing on each beat, building
  in quick steps, mechanical and cheerful like a well-oiled machine, then a clean hard stop on the final beat, no ring-out.
  Vintage mono. No vocals, no synths, no cymbal crash at the end, no fade."
- **M-B2:** "Instrumental. A short accelerating vintage orchestral build, about 12 seconds: woodwinds climbing a scale
  in tight sixteenth notes, timpani ticking like a stopwatch, brass entering in the last four seconds, tempo pushing
  forward, ending on a single clean stop. 1950s library recording, warm and hissy. No vocals, no crash cymbal, no reverb
  tail, no synths."
- **M-B3 (the drier one):** "Instrumental. 12 seconds of quick, tidy 1950s-style pit-crew music: a fast woodblock and
  snare pattern, a clipped clarinet riff that repeats four times each a step higher, plucked bass, brisk and mechanical,
  stops dead on the last beat. Mono, vintage. No vocals, no synth, no hits or stingers, no ending flourish."

Use: from the first point of the delegation (1:16.9 in v8) to the SHIP key press (1:27.9); the stop lands on the press.
If the generation runs long, cut so the stop is on the key.

### M-C · The settle (the SHIP key → the cheer → out before the button line) · ~8s

The exhale. Warm, resolved, small. It must be **gone before the narrator's last line begins** (1:34.7 in v8) so the
third alarm is the only sound that cuts him.

- **M-C1 (the lean):** "Instrumental. A warm, brief 1950s orchestral resolution, 8 seconds: strings and a solo clarinet
  landing on a soft major chord, a gentle glockenspiel note, light and content, then settling to silence without a
  swell. Vintage mono recording. No vocals, no build, no cymbal, no big finish, no synths."
- **M-C2:** "Instrumental. 8 seconds of a mid-century film cue's happy ending in miniature: a small string section
  and a harp arpeggio resolving to a held soft chord, muted brass warming underneath, then fading naturally. Warm,
  modest, tidy. No vocals, no crescendo, no synths, no drums."

Use: in on the SHIP press (1:27.9), hold under the colorize and the cheer, **out by 1:34.5**. If it wants to end on its
own, let it; if not, a 0.5s fade is the one fade the film allows.

### M-D · Optional title sting · 3–4s

Only if the title card feels naked without it. A three-note vintage "here we go" figure. Try once; if it makes the card
feel like a TV show, drop it.

- **M-D1:** "Instrumental. A 3-second 1950s cartoon title flourish: a quick ascending woodwind and xylophone figure ending
  on a bright brass chord, cheerful, vintage mono. No vocals, no synths, no drum hit, no reverb tail."

### What to reject on sight

Anything with a modern drum kit, synth pads, reverb halls, a whistled melody (too cute), a ukulele (too YouTube), a
melody that has words in it somewhere, or a comic stinger built into the bed. The bed is straight; the picture is the joke.

---

## SOUND EFFECTS

Numbering follows the 24-cue list in `POST-CHECKLIST.md`. Durations are the v8 window plus a tail. "Loop" = tick the
loop option. Where a cue has a **transient that is the edit point** (the alarms, the record scratch, the key presses), it
says so: put the transient on the cut frame and let the tail run.

### The alarm family (cues 1, 9, 23) — generate these first; they are the film's spine

Three alarms, escalating, the same sound getting bigger. Generate #1 in several flavours, pick one, then generate #2 and
#3 as the *same description* with the additions below, so they are recognisably one alarm.

- **A1 · ALARM #1 (beat 3, 2.6s window; transient on the CRT snap-on):**
  - "An old CRT television clicking on with a soft electric thunk and a faint high whine, followed immediately by a
    small office alarm: a repeating two-tone electronic klaxon, mid-sized, urgent but not painful, about 2 seconds,
    slightly muffled as if from a wall-mounted TV speaker. No voices, no music, no sirens."
  - "A vintage cartoon problem alarm: a brassy 'awooga'-style klaxon repeating three times, cartoonish and springy, with
    a tiny red-light buzz underneath, 2.5 seconds, mono, a little tinny. No voices, no music."
  - "A tabletop alarm bell hammering fast for two seconds, tinny and insistent, with a short electronic beep pattern
    layered on top, heard through a small TV speaker. No speech, no music."
- **A2 · ALARM #2 (beat 10, 3.8s window):** the chosen A1 prompt + " — louder, closer, with more bass, a second lower
  klaxon tone added underneath, a crackle of speaker distortion, and the rattle of a wall shelf and a loose cable
  shaking with it, 3.5 seconds." (If the generator supports it, feed the chosen A1 as reference audio.)
- **A3 · ALARM #3, the sting (beat 20; the transient is the cut on the narrator's word):** the A2 prompt + " — starting
  with a sharp white-flash electric crack at the very first frame, the loudest of the three, the shelf rattling hard, a
  cable swinging and tapping the wall, 2 seconds, then cut dead to silence (no tail, no reverb)."
  - Also generate the **crack alone**: "A single sharp electric crack, like a CRT flashing white with a power surge, 0.3
    seconds, dry, no tail." Lay it on the flash frame under whichever alarm wins; it is what cuts the word.

### Movement 1

- **2 · the push-in whoosh (beat 3, under the zoom, ~1s):** "A soft, short air whoosh, like a camera rushing toward a
  television, 0.8 seconds, low and airy, no impact at the end." Alt: "A quick cartoon zip-in swish, light, 0.6 seconds,
  no impact, no ring."
- **Room tone (under everything, loop, ~10s):** "Quiet office room tone: a fridge hum, a faint server fan, an old CRT's
  high whine barely audible, a coffee machine ticking as it cools. Steady, no events, no voices. Loops." (Two takes:
  one with the CRT whine, one without — the whine should exist only while the TV is on.)

### Movement 2

- **3 · the GO (beat 4, ~1s):** "An office chair swivelling quickly on its base, a short squeak and a wheel clack, then
  two crisp finger snaps in a row, dry, close. No voice." Alt: "A quick chair spin with a springy cartoon creak, then a
  single sharp finger-flick snap. No voice, no music."
- **4 · Claude, the paper storm (beat 5, 4s, loop):** "Furious pencil scribbling on paper at high speed, pages being
  flipped and flung into the air, a flutter of many sheets falling, a stack of paper thumping as more lands on it,
  continuous, cartoonish energy. No voices, no music." Alt: "Rapid pencil-on-paper writing, paper rustling and whooshing
  as sheets fly, small springy boings as a plush toy bounces up and down, 4 seconds, looping. No voices."
- **5 · Codex, the screen and the code flood (beat 6, 4.2s):** "A heavy thump on a metal server rack, then a mechanical
  arm swinging a monitor out with a clank and a click, then extremely fast keyboard typing, hundreds of keys a second,
  building to a bright electronic zip as a screen floods with text, ending on a soft flash tone. No voices, no music."
  Alt: "A server tower being hit, a screen popping out on an arm with a metallic sproing, then cartoon hammer-typing on a
  keyboard at impossible speed, a rising electronic data-stream whir, 4 seconds. No voices."
- **6 · Gemini, the whirlwind (beat 7, 4s):** "A cartoon tornado spin: a fast whirling whoosh with a rising, wobbling
  pitch, paper sheets slapping onto a wall rapidly one after another, a wet sticky-tape rip on each, the spin stopping
  dead then starting again, 4 seconds. No voices, no music." Alt: "A Tasmanian-devil-style spinning whirlwind whoosh,
  cyclical and fast, with dozens of quick paper slaps and tape peels, two spins with a hard stop between, 4 seconds."
- **7 · Grok, the wall (beat 8, 4.4s):** "A sledgehammer being hoisted with a grunt-free swing whoosh, a heavy smash
  into a plaster wall, bricks and plaster crumbling and raining down, a big hollow object being dragged across a floor
  through rubble, one soft pat on metal. Cartoonish but weighty. No voices, no music." Alt: "A cartoon wall demolition:
  a big hammer swing whoosh, a crunching plaster impact with debris scatter, a dust hiss, a heavy drag of something
  metal through gravel, one hollow tap. 4.5 seconds. No voices."
- **8 · the hollow ship (beat 9, 3.8s; transient on the key slam):** "A single heavy keyboard key slammed hard, then a
  weak, sputtering party-cannon misfire: a small pop, a fizzle, a few streamers flopping out, then a metal cannon
  tipping and falling off a tripod with a clatter and a roll, and a brass bell giving one dull, muffled, hollow clank
  instead of a ring. No voices, no music, no cheering." Alt: "A hard key slam, a deflated confetti-cannon pfft with a
  paper flutter, a tripod toppling with a clang, and a sad, damped bell thud. 3.5 seconds, cartoonish."
  - **The bell, hollow, alone (for layering):** "A single brass desk bell struck once but muffled by a hand, a dead
    hollow clunk with no ring, 0.5 seconds." Generate its **earned** twin now too (cue 19): "A single brass bell struck
    cleanly, bright and full, ringing out for 2 seconds, close, vintage, no reverb hall."

### The hinge (beats 10.5–13)

- **10 · Sean notices (beat 10.5):** room tone only. If anything: "A faint fabric rustle of two fists shaking, then a
  small sharp intake of breath, no voice, 1 second." Try it; it may be too much.
- **11 · the chaos bed → the record scratch (beat 11, bed 4.8s then the scratch; the scratch's transient is the freeze
  frame):**
  - Bed: "A chaotic room: paper storms, hammering, a tornado whoosh, fast typing, rubble, all layered thin and distant
    like it is happening across a large room, 5 seconds, continuous. No voices, no music."
  - Scratch: "A vinyl record scratch: the needle dragged hard across a record, a sharp zip, then absolute silence, 0.8
    seconds, dry, no tail." Alt: "A classic cartoon record-scratch stop, short and harsh, then dead silence, 0.6 seconds."
  - **The silence after it is a designed hole:** nothing but the quietest room tone (no CRT whine, no fridge) until the
    keys in 13.2.
- **12 · the swivel (beat 12):** "A single slow office-chair swivel, a long low creak and a quiet wheel roll, 2 seconds,
  then stillness. No voice." Nothing else on this beat. **No breath is recorded**: the shoulders are the breath.
- **13 · the turn back (beat 13.1):** the same swivel prompt with "in the opposite direction, slightly quicker."
- **14 · the keys, the typewriter, the send (beats 13.2–13.3, ~6s total):**
  - Keys: "Slow, deliberate single presses on a mechanical keyboard: one, a pause, three more, one heavier Enter key,
    close and dry, 2 seconds. No voice."
  - Typewriter (the question typing itself, 3.2s): "A manual typewriter typing steadily at a measured pace, each key a
    distinct clack, four short lines with a soft carriage return between them, 3.5 seconds, close, vintage. No bell,
    no voice." Alt: "Gentle typewriter clacks at a calm rhythm, four lines, a quiet return after each, ending with one
    slightly firmer key, 3.5 seconds."
  - Send: "A single soft digital send chime, one low-to-high two-note blip, 0.5 seconds, small and polite."
- **15 · the replay (beat 14, 6s, loop):** "An old CRT television humming with a faint high whine, and a computer mouse
  sliding on a desk in slow circles, the small rolling scrape of a mouse moving and pausing, three circles, never a
  click. 6 seconds, loops. No voices, no music." Alt: "A screen-recording playback: soft CRT hum, a cursor's mouse
  movement as gentle desk scuffs in loops, a tiny hover blip now and then, no click ever, loops."

### The exhale and the fix

- **16 · the four sighs (beat 15, ~1.2s each) — no words, no vowels that sound like words:**
  - Claude: "A small plush creature's sigh of relief: a soft cartoon exhale like air leaving a cushion, a gentle
    squeak at the end, 1 second. No words, no speech."
  - Codex: "A big held breath released in a whoosh, like a balloon deflating with a soft rubbery flutter, 1.2 seconds.
    No words."
  - Gemini: "A light, bubbly cartoon exhale with a little sparkle glissando and a tiny hop-land thump, 1 second. No
    words, no speech."
  - Grok: "A gravelly little creature exhaling in relief, a brow-wipe swish, a small satisfied grunt with no words, 1.2
    seconds. No speech."
- **17 · the delegation (beat 16):** room tone; optional "four quick soft pointing swishes, a hand cutting the air, 0.3
  seconds each" to lay on each point.
- **18 · the pit stop (beat 16.5, four cues, each ≤1.2s, each snap on its cut):**
  - Claude: "One fast pencil stroke on paper, then a sheet of paper snapped up and held with a crisp flick, 0.8 seconds."
  - Codex: "A single sharp mechanical key tap, then a small springy hop and a soft landing thump, 0.9 seconds."
  - Gemini: "A sketch snatched with a quick paper whip, a flourish swish, slapped onto a wall with one firm smack and a
    tape peel, a tiny corner nudge, 1 second."
  - Grok: "A hammer hoisted with a short whoosh and smashed into a big wooden button, wood splintering into three
    pieces, a puff of dust, a small hop-land and two hand-dusting claps, 1.2 seconds, cartoonish. No voice."
  - **Under all four, optional:** "An F1 pit-stop pneumatic wheel-gun rattle, four quick bursts, 4 seconds, distant."
    (Try it once; if it reads as a car, cut it.)
- **19 · the SHIP key + the earned bell (beat 17, 2s; transient on the press):** "A single clean, satisfying mechanical
  key press, deep and solid, one click, dry, 0.3 seconds." Then the earned bell from cue 8 on the same frame, if ruled.
- **20 · the colorize (beat 18, 3.2s):** "A soft rising electric tone travelling upward, like a current climbing a cable,
  warm and gentle, 1.5 seconds, ending in a small bright bloom and a quick cartoon 'thumbs-up' snap. No voices, no
  music." Alt: "A gentle magical fill-up sound, a smooth glissando up with a warm glow at the top, then one crisp
  snap, 2 seconds. No voices."
- **21 · the cheer (beat 18.5, 2.6s) — the hardest one; it must not contain words:**
  - "A small cartoon crowd of five creatures cheering wordlessly: whoops, a squeak, a happy trill, a gravelly whoop, an
    excited yelp, plus an office chair spinning and a springy hop, 2.5 seconds. No words, no language, no laughter
    track, no applause."
  - Alt: "Five joyful non-verbal cartoon exclamations layered together, high and low, with a chair spin creak and a
    small confetti-free jump landing, 2.5 seconds. No speech, no words."
  - If every generation smuggles words in, build it from the four sigh voices plus one "Sean" whoop: "A single wordless
    man's happy whoop, short, 0.5 seconds, no words."
- **22 · the button hold (beat 19):** the quiet room tone (the CRT whine on, since the USER is on screen). Nothing else.
- **23 · the sting:** A3 above (the crack on the flash frame; the alarm; the shelf rattle; the cable tap).
- **24 · the black:** silence. Do not generate anything. No tail, no music, no hum.

### Alt-textures worth one generation each (for the CapCut bin)

- "Paper flutter, a single sheet falling and settling, 1 second." (a universal glue)
- "A soft cartoon spring boing, small, 0.4 seconds." (Claude's bounces in beats 2 and 5)
- "A dart thrown and thudding into plaster next to a dartboard, 0.6 seconds." (beat 2, Grok's miss)
- "A coffee mug lifted and set down on a wooden desk, one gulp-free clink, 0.8 seconds." (beat 2, Sean; no gulp: he never opens his mouth on screen)
- "A CRT power-on click and high whine rising, 0.5 seconds." (before each alarm)
- "A short white-noise burst like a CRT flashing, 0.2 seconds." (the two post opacity flashes)

---

## Mix notes for CapCut, in five lines

1. VO on its own track, centred, about 6 dB above everything; music under the narrator sits at −18 to −22 dB relative.
2. The three alarms are the loudest things in the film and each is louder than the last; nothing else may peak above alarm #2.
3. The silence after the record scratch is real: kill every bed, leave only the quietest room tone.
4. The transient rule: alarm crack on the flash frame, record scratch on the freeze frame, key press on the press frame, pit-stop snaps on their cuts.
5. The black is silent. If the export tool adds a fade, remove it.
