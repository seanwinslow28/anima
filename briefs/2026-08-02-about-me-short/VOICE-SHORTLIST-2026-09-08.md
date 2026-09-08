# VOICE SHORTLIST — ElevenLabs voices for the "How To" narrator, via Voice Changer · 2026-09-08

*Companion to `VO-SCRIPT-v1.md` (the lines, the delivery notes, the take list) and `AUDIO-PROMPTS-v1.md` (music + SFX).
$0. Research from ElevenLabs' own library pages and Voice Changer docs (sources at the foot); nothing here has been
auditioned by ear yet. That audition is the protocol in §4, and it doubles as the scratch-narration gate the brief asks for.*

## 1. The one fact that decides everything

**Voice Changer keeps your performance and swaps only the timbre.** ElevenLabs' own guide says it preserves "the tone
and delivery of the original voice" — pacing, emphasis, emotion, *and accent*. Record American, pick a Mid-Atlantic
voice, and you get an American accent in that voice's throat. Which means:

- **The 1952-serene read has to already be in your recording.** The composure, the unhurried pace, the never-acknowledging
  flatness, the breath before "…is a step back" — the changer will not add any of it, and it will faithfully transmit any
  wink you leave in. `VO-SCRIPT-v1.md`'s delivery notes are for *you*, not for the model.
- **The shortlist below is a shortlist of throats, not of performances.** What you are choosing is: how deep, how old,
  how much chest, how much vintage-announcer polish. John McLeish's Goofy narration was a dignified, erudite, deadpan
  baritone — the joke was that he read the instructions as if they were true. So the target timbre is: **deep,
  resonant, measured, dignified, a little older than you, with the smooth "announcer" quality of a man who has read
  a lot of pamphlets aloud.** Not dramatic. Not gravelly. Not British.
- **Nothing on this list carries the 1952 optical-soundtrack grain.** That is a CapCut EQ pass after the render
  (§5), the same treatment the music prompts ask for, so the narrator and the score live in one era.

## 2. The shortlist

All from the public Voice Library unless marked *default*. IDs are for the library search box (paste the ID) or the API.
Ranked by fit to the target timbre. **Lean: A and B, auditioned against each other; C is the tie-break.**

| # | Voice | ID | What it is | Why it fits | Watch for |
|---|---|---|---|---|---|
| **A** | **The Golden Age Announcer** | `awuP1IX9V7hxeGp0B3cF` | Male, 40s, slight transatlantic. "Deep baritone… rich, theatrical quality of a 1940s radio announcer… measured, dramatic pace" | The closest single match to McLeish in the library: the announcer-baritone with the period polish already in the timbre | "Theatrical/dramatic" — a newsreel-bombast risk. Under Voice Changer the drama comes from *your* read, so the risk is small; if the render still sounds like it is selling war bonds, drop to B |
| **B** | **The Golden Age Radio Host** | `nDetGehLv9T8RrbPvtvW` | Male, 50s, Mid-Atlantic. "Warm, authoritative… deep, resonant… smooth, buttery timbre" | The warmer, older, less bombastic twin of A — "buttery" is the serene half of the brief. Likely the better fit for the step-back line and the button | May be *too* warm on cycle 1, where the narrator should sound like a pamphlet, not a friend. Audition the "Step four" line specifically |
| **C** | **The Master Demonstrator** | `8FhiNDf0kdTIIpJdPdzg` | Male, 50s, American. "Authoritative… deep, resonant bass tones with a deliberate, measured pace" — from the library's *Demonstrator* (instructional) shelf | Literally the how-to-narrator archetype: deliberate, bass, measured. The most "instructional" of the three | Recorded clean and modern — no vintage character in the timbre at all, so the era has to come entirely from your read + the §5 EQ. The safest and the least flavoured |
| D | Knox Dark — Serious, Deep, and Steady | `dPah2VEoifKnZT37774q` | Male, middle-aged. "Deep voice of a middle aged man, serious in read… slow, methodical and particular" | The deadpan option: if A/B feel too pleased with themselves, this is the straight man | Can read as grim rather than serene; "Dark" is in the name for a reason |
| E | Older Joe — Calm Authoritative Narrator | *(search by name)* | Male, senior, British RP. "Polished and professional… news articles, audiobooks" | An older, polished baritone; since the changer keeps *your* accent, the RP does not transfer — only the age and polish do | A wildcard. The training accent can still colour vowels slightly |
| F | David Castlemore — Newsreader | `XjLkpWUlnhS8i7gGz3lZ` | Male, middle-aged American. "Clear and crisp… in the style of broadcast news presenters" | The broadcast crispness, if the period voices sound too costume-y | Modern; the least "1952" of the set |

**Defaults worth a pass (Bill, Brian, George, Daniel, Roger, Clyde).** ElevenLabs' own descriptions: Bill "friendly and
comforting", Brian "resonant and comforting, middle-aged", George "warm resonance", Daniel "strong British… professional
broadcasts". They are easy to reach and fine to audition — **but every Default voice expires on 31 December 2026** per
ElevenLabs' help centre, so a narrator built on one cannot be re-rendered next year. Use them to calibrate, not to ship.

**Not this:** *John Facenda* on the Iconic marketplace ("The Voice of God") — the grandeur is the opposite of brochure-
serene, and it is a licensed voice with its own terms. The 1950s *Game Show Host* on the Retro shelf is the wrong energy
(bright, nasal, exclamatory). Nothing gravelly, nothing "storyteller-grandpa", nothing British-by-accent — the accent is
yours anyway.

## 3. Voice Changer settings for a serene read

Model: **Eleven English v2** (the speech-to-speech model, `eleven_english_sts_v2`) for an English-only source; the
Multilingual v2 your screenshot shows also works but has nothing to add here.

| Control | Set | Why |
|---|---|---|
| Stability | **65–75** | Serene = stable. The published sweet spot for tutorial/corporate reads is 65–75; storytelling drops to 40–55 and that is where the model starts adding expression you do not want. Push toward 75 for cycle 1, ease toward 60 for the step-back line if it comes out stiff |
| Similarity | **70–75** | Above ~80 the model over-enunciates into an artificial "news anchor" clip; below ~65 the target throat thins out |
| Style exaggeration | **0** | The style is in your read. Any value here invites the wink |
| Remove background noise | on only if your room is noisy | It can also scrub the breath before "…is a step back"; try the button line with it off |

Source recording: consistent distance, no clipping, no room echo. ElevenLabs bills the changer at 1,000 characters per
minute of audio; a 45-second full read is trivial, so audition freely. 5-minute / 50 MB cap per file — irrelevant here.

## 4. The audition — and it IS the scratch-narration gate

The brief's non-negotiable (*"no full production spend before a blind-judged 30-second scratch narration passes; the
narrator fallback named in writing"*) was never performed; GAPS-2026-09-07 names an ElevenLabs stock 1950s voice as the
fallback. This audition satisfies the gate and picks the throat in one sitting:

1. **Record once, dry, your own voice**, the three registers in one take (~35s): the title + "Step one" (the pamphlet),
   "Step four: change only what needs changing" (the driest gap line), the step-back line with its held breath, and the
   button line — Take B from the take list, read through "quiet morning" so the alarm has a word to cut.
2. **Run that one recording through A, B, C, D** (and a default or two if you like) at the §3 settings. Do not
   re-record between candidates; the whole point is the same performance in different throats.
3. **Lay each under the v8 rough cut** (`motion/film-roughcut/FILM-roughcut-v8-trim-lean.mp4`) at the timecodes in
   `VO-SCRIPT-v1.md`, export four 45-second clips, label them 1–4, and **do not tell the judge which is which** — or
   which one is your own un-changed voice. Include the un-changed take as a fifth clip.
4. **The judge is anyone who has not read a page of this project.** One question: *"Which narrator sounds like he
   believes the instructions?"* A second, only after: *"Did any of them sound like a guy with a mic?"* (the brief's
   failure phrase). If your own voice wins, the changer is unnecessary and that is the best outcome; if a stock voice
   wins, it is the fallback made real.
5. **Record the result** in `GAPS-2026-09-07.md` (item 1) and `POST-CHECKLIST.md`.

## 5. The 1952 treatment in CapCut (after the render, whichever voice wins)

High-pass ~120 Hz (take the modern chest out), low-pass ~7–8 kHz (optical-track bandwidth), light compression, a
touch of hiss or a "vintage radio" preset at low mix — matched to the music, which is prompted the same way. Do this
on the VO track, never on the SFX: the alarms and the record scratch stay full-band so they cut through the era.

## Sources

- ElevenLabs Voice Library — [Retro](https://elevenlabs.io/voice-library/retro) · [Old Time Radio](https://elevenlabs.io/voice-library/old-time-radio) ·
  [Demonstrator](https://elevenlabs.io/voice-library/demonstrator) · [Old Male](https://elevenlabs.io/voice-library/old-male) ·
  [Professional Narrator](https://elevenlabs.io/voice-library/professional-narrator-voices) · [Documentary Narrator](https://elevenlabs.io/voice-library/documentary-narrator-voices)
- [Voice Changer product guide](https://elevenlabs.io/docs/eleven-creative/playground/voice-changer) (models, what is preserved, limits, pricing) ·
  [Old-time-radio voice changer page](https://elevenlabs.io/voice-changer/old-time-radio)
- [Default voices — expiry notice](https://elevenlabs.io/docs/product/voices/default-voices) · [Knox Dark](https://json2video.com/ai-voices/elevenlabs/voices/dPah2VEoifKnZT37774q/)
- Settings ranges: [ElevenLabs best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices) · [Voice Changer guide 2026](https://elevenlabsmagazine.com/elevenlabs-voice-changer-guide-2026/) · [NeuraPulse settings](https://neuraplus-ai.github.io/blog/best-settings-for-elevenlabs-ai-voice-quality-improvement-2026.html)
- The target: [John McLeish — Wikipedia](https://en.wikipedia.org/wiki/John_McLeish_(voice_actor)) · [D23](https://d23.com/a-to-z/mcleish-john/)
