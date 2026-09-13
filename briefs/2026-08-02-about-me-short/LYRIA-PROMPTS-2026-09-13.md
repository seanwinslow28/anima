# LYRIA 3.5 PROMPTS — the music cues rewritten for Google's grammar · 2026-09-13

*Companion to `AUDIO-PROMPTS-v1.md` (the ElevenLabs versions of the same four cues, and every SFX). Same sections, same
timecodes (the v8 trim lean, `motion/film-roughcut/FILM-roughcut-v8-trim-lean.mp4`), same rule: the bed is straight,
the picture is the joke. $0 in Higgsfield credits; Lyria 3.5 is $0.08 a generation on the paid tier, Lyria 3 Clip
Preview is ~$0.04 for a 30-second draft. Sources at the foot.*

## 1. Can Lyria "research" the Goofy How-To shorts? No — and here is what to do instead

**Lyria 3.5 does not browse.** It is a single-turn text-to-music model: your prompt (plus up to ten attached images) is
everything it knows about the job. Google's own docs say to reference **genre + era + instrumentation + production
texture**, never a named performer, and the safety layer runs an "artist intent" check that blocks prompts asking for a
particular artist's sound. A title like *Two Weeks Vacation*, a studio name, or the composer's name (Oliver Wallace
scored the Goofy shorts) is at best a weak prior the model may or may not have, and at worst a filter trip. It will not
go and listen.

So the reference has to arrive **already translated into traits** — which is exactly what the shorts sound like once
you write it down:

| What you hear in a 1952 Goofy short | How to say it to Lyria |
|---|---|
| A small studio orchestra, not a symphony | "small 1950s studio orchestra", "light orchestral" |
| Woodwinds carry the tune (clarinet, flute, bassoon), strings pluck under them | name them: clarinet, flute, bassoon, pizzicato strings |
| Muted brass answers; a tuba or plucked bass walks the downbeats | "muted trumpet", "tuba on the downbeats", "walking pizzicato double bass" |
| Brisk, orderly, march-adjacent, always pleasant | "brisk", "orderly", "cheerful and officious", 116–126 BPM, major key |
| Mono optical soundtrack: narrow, warm, a little hiss | "mono, 1950s optical-soundtrack warmth, slight tape hiss" |
| The gag hits are *mickey-moused* — and we do NOT want that in the bed | write it out: "no comedic hits, no mickey-mousing, no stingers" |

**Two levers Lyria has that ElevenLabs does not.** (1) **Image input:** attach the title card (`_LOCKED-M1/01_beat1_S01_title-card.png`)
and one or two frames (the freeze frame, a pit-stop frame) — Google says the model reads mood, palette and setting into the score. That
is the closest thing to "showing it the short": the pencil-test cream paper and the cartoon cast will pull it toward light and period
rather than epic. (2) **Timestamps:** Lyria plans structure before it renders, so one generation can carry the whole cycle-1 bed with the
alarm drops written in at the film's own timecodes (§4).

**If you want to test the naming question anyway, do it as a controlled A/B** ($0.16): the same prompt once with *"in the manner of a 1950s
Disney instructional cartoon short"* and once with only the traits. Keep whichever your ear picks, but expect the traits version to
be the one you can reproduce.

## 2. Lyria's grammar (what Google says works)

The formula, in this order: **genre (with era) → exact instrument names → a numeric BPM → a key → a mood word or two →
structure tags or timestamps.** Then the constraints as plain prose.

- **Exact instruments, not categories.** "Clarinet, pizzicato strings, muted trumpet" steers; "orchestra" defaults to generic.
- **A number for tempo.** "120 BPM" beats "brisk". Add "brisk" as the mood word anyway.
- **A key.** Major for the brochure, a lift for the build (see §3).
- **Structure.** Either bracket tags (`[Intro]` `[Main]` `[Outro]`) or timestamps (`[0:00-0:04] ...`). Timestamps are approximate,
  not frame-locked — the CapCut cut still owns the edges. The Composer mode in AI Studio is the same thing as a form: one section per
  row with timing and intensity.
- **"Instrumental only, no vocals" is prose**, not a switch (there is no negative-prompt field). Say it, and say every other
  exclusion in words too — they are the first thing dropped, so put them at the end where they are last read.
- **Endings are yours to write.** "Ends on a clean hard stop, no ring-out" or "settles to silence without a swell" — otherwise the
  model resolves the way pop songs do.
- **No seed; outputs vary.** Generate two or three of the winner and pick; the prompt is not a recipe you can re-run.
- **Length.** Lyria 3.5 runs up to roughly three minutes and follows a stated duration loosely; ask for the length you want in the
  prompt and cut. Draft in Lyria 3 Clip Preview (fixed 30s) when you are only testing a palette.
- **What gets refused:** named artist sound, copyrighted lyrics. What gets ignored: anything you did not name.

## 3. The four cues, in Lyria's grammar

Keys chosen so the film has a harmonic plan: **F major** for the brochure bed, **G major climbing** for the pit-stop build (one
step up = "we are getting somewhere"), **F major** again for the settle (home). If the ear disagrees, drop the keys; they are the
least load-bearing element.

### M-A · The brochure bed (title → Movement 2) · target 50s, loopable

- **LY-A1 (the lean):**
  > 1950s educational-film library cue, light orchestral, small studio orchestra. Clarinet and flute carrying a tidy cheerful
  > melody, pizzicato strings, brushed snare, a soft tuba on the downbeats, a muted trumpet answering the phrase ends. 120 BPM,
  > key of F major. Mood: pleasant, orderly, officious, like a public-information short about a well-run office. Mono 1950s
  > optical-soundtrack warmth, slight tape hiss, gently compressed. [Intro] four bars of the melody, light. [Main] the full
  > arrangement repeating the tune with small variations, steady, never building. [Outro] returns to the intro figure so it loops.
  > About 50 seconds. Instrumental only, no vocals, no modern drum kit, no synthesizers, no comedic hits, no mickey-mousing,
  > no stingers, no swells, no big finish.

- **LY-A2 (the woodwind version):**
  > Mid-century instructional-short score, chamber-sized. A bassoon and clarinet duet walking a neat little tune over plucked
  > double bass and a light woodblock, a muted trumpet interjecting politely, strings only as soft pizzicato. 112 BPM, key of
  > Bb major. Mood: cheerful, unhurried, orderly. Recorded on a 1950s optical soundtrack: mono, warm, a little hiss. Steady
  > from start to finish, repeats naturally as a loop. About 50 seconds. Instrumental only, no vocals, no synthesizers, no
  > percussion hits, no slapstick stingers, no crescendo.

- **LY-A3 (busier, for Movement 2 only):**
  > 1950s cartoon-short underscore for a bustling montage, light orchestral. Quick pizzicato strings and xylophone runs, a
  > chattering clarinet line, brushed drums with a walking upright bass, muted brass on the offbeats. 132 BPM, key of F major.
  > Mood: bustling, brisk, polite, orderly. Vintage mono recording with tape warmth. [Main] busy and even throughout, no rise
  > and fall. About 35 seconds. Instrumental only, no vocals, no drum fills, no mickey-mousing hits, no synthesizers, no
  > swells, no ending flourish.

Use as in `AUDIO-PROMPTS-v1.md`: A1 or A2 under the title and Movement 1, A3 (or A1 continued) from the GO through the hollow
ship; **cut dead** on the record-scratch frame, no fade.

### M-B · The pit-stop build (delegation → SHIP key) · target 12s

- **LY-B1 (the lean):**
  > 1950s cartoon-short action cue, light orchestral. A fast precise rising figure on xylophone and pizzicato strings, a brisk
  > snare roll underneath, muted trumpet stabbing on each beat, woodwinds climbing in tight sixteenth notes. 144 BPM, key of G
  > major, modulating up a step halfway. Mood: mechanical, delighted, precise, like a well-oiled machine. Vintage mono. [0:00-0:06]
  > the figure begins low and tidy. [0:06-0:11] it climbs and thickens, brass joins. [0:11-0:12] a clean hard stop on the final
  > beat, no ring-out, no cymbal. About 12 seconds. Instrumental only, no vocals, no synthesizers, no crash cymbal, no fade,
  > no reverb tail.

- **LY-B2 (the stopwatch version):**
  > Short accelerating vintage orchestral build, 1950s library style. Woodwinds climbing a scale in sixteenth notes, timpani
  > ticking like a stopwatch, plucked bass, brass entering only in the last four seconds. Starts at 132 BPM and pushes forward,
  > key of G major. Mood: urgent, tidy, cheerful. Warm hissy mono. Ends on a single clean stop. About 12 seconds. Instrumental
  > only, no vocals, no crash cymbal, no reverb tail, no synthesizers.

Use: in on the first point of the delegation (1:16.9), the stop lands on the SHIP press (1:27.9). If it runs long, cut so the
stop is on the key.

### M-C · The settle (SHIP key → cheer → out before the button line) · target 8s

- **LY-C1 (the lean):**
  > Warm brief 1950s orchestral resolution, light orchestral. Strings and a solo clarinet landing on a soft major chord, one
  > gentle glockenspiel note, muted brass warming underneath. 90 BPM, key of F major. Mood: content, modest, resolved. Vintage
  > mono recording. Settles to silence without a swell. About 8 seconds. Instrumental only, no vocals, no build, no cymbal,
  > no big finish, no synthesizers.

- **LY-C2:**
  > A mid-century film cue's happy ending in miniature: a small string section and a harp arpeggio resolving to a held soft
  > chord, a flute holding the top note, then a natural fade. 84 BPM, key of C major. Mood: warm, tidy, small. 1950s mono.
  > About 8 seconds. Instrumental only, no vocals, no crescendo, no drums, no synthesizers.

Use: in on the SHIP press (1:27.9), out by 1:34.5 — before the button line. The one fade the film allows.

### M-D · Optional title sting · 3–4s

- **LY-D1:**
  > A three-second 1950s cartoon title flourish: a quick ascending woodwind and xylophone figure ending on a bright muted-brass
  > chord. 126 BPM, key of F major. Mood: cheerful, vintage. Mono. Ends on the chord, short decay. Instrumental only, no vocals,
  > no synthesizers, no drum hit, no reverb tail.

## 4. The Lyria-only option: one generation for the whole first cycle, alarms written in

Because Lyria plans structure from timestamps, you can ask for the cycle-1 bed as one piece with the two alarm drops
placed at the film's own marks (v8: alarm #1 hits at 0:12.5, alarm #2 at 0:40.0, the record scratch at 0:49.9). The
timestamps will land within a second or so, not on the frame; slip the whole file in CapCut so the first drop sits on
alarm #1, then cut the second edge by hand.

- **LY-FULL (the cycle-1 score):**
  > 1950s educational-film library cue, light orchestral, small studio orchestra: clarinet and flute melody, pizzicato strings,
  > brushed snare, soft tuba downbeats, muted trumpet answers. 120 BPM, key of F major. Mood: pleasant, orderly, officious.
  > Mono 1950s optical-soundtrack warmth, slight tape hiss.
  > [0:00-0:04] a bright four-bar title figure, tidy and confident.
  > [0:04-0:12] the main tune, light and steady under narration, nothing rises.
  > [0:12-0:14] the music drops out completely, two seconds of silence.
  > [0:14-0:39] the tune returns slightly busier: xylophone runs join, walking bass, still polite and even, no build.
  > [0:39-0:41] the music drops out again, silence.
  > [0:41-0:50] the busy tune resumes, then at 0:50 it stops dead mid-phrase, no ring-out.
  > About 50 seconds. Instrumental only, no vocals, no modern drum kit, no synthesizers, no comedic hits, no mickey-mousing, no
  > stingers, no swells, no fade.

If Lyria refuses to leave true silence at the drops (models tend to fill), generate LY-A1 and cut the drops yourself; the
drops are two edits in CapCut either way.

## 5. Working method in AI Studio

1. **Palette first, cheap.** Run LY-A1 and LY-A2 as 30-second Clip Previews. Pick the palette by ear against the title card and
   Movement 1 in the v8 cut, not on its own.
2. **Then the real renders.** The winner ×3 at Lyria 3.5, attaching the title card and the freeze frame as images. Keep the three
   in `audio/Music/` with the prompt text in a sidecar; the losers are still usable as alternates.
3. **B and C last**, each ×2. They are short and the edges are hard, so listen for the stop and the settle, not the tune.
4. **Reject on sight** the same things as the ElevenLabs list: modern kit, synth pads, hall reverb, whistling, ukulele, anything
   with a hum or "la" in it, a comic stinger baked into the bed.
5. **Match the narrator's era in CapCut** the same way the VO gets it: high-pass ~120 Hz, low-pass ~7–8 kHz on the music bus,
   SFX left full-band.

## Sources

- [Generate music with Lyria 3.5 — Gemini API docs](https://ai.google.dev/gemini-api/docs/music-generation) (prompt elements, tags, timestamps, image input, safety filtering, non-determinism, single-turn)
- [Ultimate prompting guide for Lyria 3 Pro — Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-lyria-3-pro) (the formula, "Instrumental.", timestamp syntax, genre/era over artist, verbatim examples)
- [Lyria 3.5 — Google DeepMind](https://deepmind.google/models/lyria/) · [Lyria 3.5 prompts: what changed after the September 2026 API launch](https://roo.beehiiv.com/p/lyria-3-5-prompts) (element order, no seed, no negative-prompt field, Clip Preview for drafts)
- [Lyria 3.5 review — The Rundown](https://www.therundown.ai/tools/lyria-3-5) · [Unite.AI on the Gemini/API launch](https://www.unite.ai/google-brings-lyria-3-5-music-generation-to-the-gemini-app-and-api/) (artist-voice and copyrighted-lyrics blocks, era/instrumentation guidance)
