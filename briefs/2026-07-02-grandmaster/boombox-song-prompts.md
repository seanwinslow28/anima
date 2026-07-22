# FIRST LICKS — The Boombox Song (temp track prompts)

> **STATUS 2026-07-20 — two tracks LOOSE-LOCKED.** Sean generated and picked two
> candidates he's deciding between, both the ~2:00 master arrangement, at
> `runs/2026-07-19-first-licks-artdept/music/` — `first-licks-track-1.mp3` and
> `first-licks-track-2.mp3` (each 120.03s). **Loose lock:** the final pick happens
> by feel during the montage (which track cuts best against the motion frames);
> not committed yet. The derived states (degraded-diegetic / ghost-echo, ffmpeg
> chains below) wait for the single pick. A **lyric-track** option may come in a
> future session (Sean's call). The one-song conceit + the boombox-as-calendar
> device are unchanged.

*Drafted 2026-07-19. This is the pre-Sam/Bea blocker: the montage cuts to this
song, so the temp track must exist and be picked before Bea locks hold
durations. Production model: **one master + derive** (Sean's call, 2026-07-19)
— ElevenLabs Music generates ONLY the full montage arrangement; the
degraded-diegetic and ghost-echo states are derived from the picked keeper via
the ffmpeg chains at the bottom, so all three states are literally the same
recording. Sean generates, Sean picks; nothing here locks until his ear does.*

## The spec (where every prompt line comes from)

- **Genre:** original 70s kung-fu-cinema funk/soul (concept.md §Audio plan).
- **Kit:** raw and small — percussion, bass, distorted elements, **no
  orchestra**; "complex but still very very simple" (addendum SN-8). Take
  Primal's *instrumentation*, not its wall-to-wall density (addendum N2).
- **Voice rules:** instrumental. No lyrics, no lead vocal — the film is
  near-wordless and her laugh is the only voice she gets. Wordless funk
  exclamation stabs ("hah!", "unh!") are a genre marker and are offered as a
  knob on candidate C only; default off.
- **Length:** ~2:00 master. The montage itself likely runs 60–90s; the extra
  gives the edit cutting room and the trims fall on the montage first (F1
  discipline).
- **Structure (all candidates):** cold intro riff (loopable, this is what the
  boombox "starts" with) → main groove → variation/escalation section (the
  vignette ladder) → four-bar breakdown → hard out on a stab. A hard out, not
  a fade — the edit owns the fades, and the derived ghost-echo state needs
  clean material.

## Candidate prompts (generate all, pick one)

**A — the wah-guitar engine** *(the classic; my recommendation to try first)*

> Instrumental 1970s kung-fu-cinema funk, 100 BPM. Small raw band: tight dry
> breakbeat drums, round fingered electric bass riff, wah-wah rhythm guitar,
> one gritty distorted clavinet line. No orchestra, no strings, no synth pads,
> no vocals. Lo-fi analog warmth, slightly overdriven, like a well-worn 45.
> Structure: a four-bar cold intro riff, then the main groove, then an
> escalating variation section with the clavinet pushed harder, a four-bar
> drum-and-bass breakdown, and a hard ending on a single stab. Confident,
> playful, determined — training-montage energy, never epic.

**B — the percussion-forward one** *(closest to Primal's own kit)*

> Instrumental 1970s funk-soul groove for a martial-arts training montage,
> 96 BPM. Dominated by raw percussion: dry breakbeat kit, congas, shaker, a
> struck woodblock; underneath it a deep repetitive bass riff and one
> distorted baritone guitar figure. No orchestra, no horns, no vocals, no
> reverb wash — dry, close, physical. Structure: percussion-only cold intro,
> bass enters, groove builds by adding one element at a time, brief
> percussion-only breakdown, hard stop ending. Sounds hand-made, small room,
> analog tape.

**C — the horn-stab one** *(most "kung-fu cinema"; horns as stabs, not a section)*

> Instrumental 1970s Hong-Kong-cinema funk, 104 BPM. Tight dry drums, driving
> fingered bass, wah guitar, and sparse unison horn stabs used as punctuation
> only — two or three hits per phrase, never a melody line, never a horn
> section pad. No strings, no orchestra, no vocals. Gritty, analog,
> slightly clipped. Structure: cold bass-and-drums intro, main groove with
> horn stabs, escalation with faster stab pattern, breakdown to bass alone,
> hard out on one final horn stab.
>
> *Knob (default off): add "occasional wordless male funk exclamations, mixed
> low" if the takes feel too polite.*

**D — the wildcard: slower, meaner** *(in case A–C all read too happy)*

> Instrumental slow heavy funk, 84 BPM, 1970s revenge-cinema mood played on a
> small raw kit: sparse dry drums with a heavy backbeat, fat overdriven bass,
> a single tremolo guitar line, occasional struck chain or metal percussion.
> No orchestra, no vocals, no epic build. Patient, coiled, deliberate — the
> quiet parts of the song matter as much as the loud. Structure: near-empty
> intro (bass and one drum), groove thickens gradually, one restrained
> escalation, hard stop.

**Generation notes.** Ask for ~2:00. Generate 2–3 takes per candidate you
like — ElevenLabs variance between takes of the same prompt is real and the
pick is your ear's. The keeper lands at
`briefs/2026-07-02-grandmaster/audio/boombox-song-master.{mp3,wav}` (create
`audio/` on first save); name rejected takes `candidates/<letter>-<n>.mp3` if
you want them kept for the record.

## Derived states (run after the keeper is picked — $0, one command each)

**State 1 — degraded-diegetic** (boombox through the camcorder mic; used
inside the home-movie tape and any Act-1/Act-3 diegetic moment):

```bash
ffmpeg -i boombox-song-master.wav -af \
  "aformat=channel_layouts=mono, highpass=f=250, lowpass=f=3400, \
   acompressor=threshold=-18dB:ratio=6:attack=2:release=80, \
   vibrato=f=0.6:d=0.06, \
   volume=6dB, aresample=8000, aresample=44100" \
  boombox-song-diegetic.wav
```

*(Mono, telephone-band EQ, pumping compression, tape wow, a resample crush.
Tune to taste — the goal is "cheap boombox heard by a cheaper mic." The VHS
hiss bed, if wanted, is an edit-stage overlay, not baked in.)*

**State 3 — ghost-echo** (the walk home; "an echo of the training music
slowly rises"):

```bash
ffmpeg -i boombox-song-master.wav -af \
  "lowpass=f=1800, \
   aecho=0.7:0.6:60|180:0.35|0.2, \
   afade=t=in:st=0:d=6, volume=-8dB" \
  boombox-song-ghost.wav
```

*(Lowpassed, doubled echo, long fade-in, sitting well under dialogue-less
foley. The edit decides where it starts rising; this file just needs to feel
like the song remembered rather than played.)*

**Do not** derive until the master is picked — both derivations are one-liners
and re-running them after a future master swap costs nothing.

## What this unblocks

The stopwatch table-read (verification gate 1) and Bea's hold-duration locks
both wait on the picked master. The laugh sourcing stays its own later pass
(concept.md §Audio plan); nothing here touches it.
