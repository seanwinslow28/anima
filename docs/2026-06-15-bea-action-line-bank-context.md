# Bea build input — the Action-Line Prose Bank (vendored)

> **Build session, read this:** This is a **ready-to-vendor build input** for Bea (the Phase-3b storyboard artist). It carries the **prose-action exemplars** Bea needs for the per-shot `prompt` field — the gap the [voice-integration addendum](2026-06-15-screenwriting-modes-integration-addendum.md) §5 flagged: the shared `sean-screenwriting-voice.md` carries Sam's *dialogue* samples, but Bea writes *prose-action*. Fold the bank below into **`pipeline/agents/prompts/bea-storyboard-context.md`** (NOT into `sean-screenwriting-voice.md` — that file is md5-pinned for Sam; leave it byte-stable). Keep the provenance header. Do **not** distill the exemplars to bullets — the verbatim lines are the load-bearing part.
>
> **Provenance:** vendored verbatim from §2 of `code-brain/.claude/skills/screenwriting-modes/references/2026-06-04-script-mining-report.md` (the script-mining report from Sean's 11 screenplays). Mirrors how [`2026-06-15-sam-bea-screenwriting-voice-context.md`](2026-06-15-sam-bea-screenwriting-voice-context.md) was produced as the Sam voice build-input.

---

## Why Bea needs this (not Sam)

Sam writes dialogue and beat structure; the §8 verbatim samples in the shared voice file are dialogue-heavy and right for him. Bea writes **the per-shot generation prompt** — a prose-action description in the pencil-test register that Flo consumes directly (see the Spark `shots.yaml` `prompt` fields for the target shape). Bea's hard part is making that prose carry Sean's voice into the image, not generic storyboard description. This bank is the few-shot for that job. It pairs with the **visual moves** Bea already inherits from the shared voice file (Room-as-Biography, the Loaded Object, Haptic Visuality, Metaphor-Compression-in-an-empty-frame) — the bank shows the *sentence-level* prose voice; the moves show the *shot-level* strategy.

The **Loaded-Object seam** is where the two meet: when a Sam beat's `intent`/`notes` carry a loaded object (the addendum's Sam→Bea handoff definition), that object *is* Bea's shot — and exemplars 7, 29, 37-shaped lines below are how the prose should read.

---

## Action-Line Prose Bank

*Sean's natural prose voice lives in these. Tagged by what each demonstrates. Vendored verbatim.*

1. **"MAX (31), a permanently stoned trans woman with chicken tenders in her pocket, lifts a large bag of potato skins."** (Gourmet) — character intro: two concretes + one absurd prop, prop lands last.
2. **"LISA, a woman covered in vomit stains and regret, walks over with a SCREAMING baby."** (Gourmet) — zeugma: concrete yoked to abstract in one breath. The signature intro shape.
3. **"Thursday's manager RINALDO (42), a Frenchman with a permanent stick up his ass, barges in and LAUNCHES a menu in Brandon's direction. Brandon casually dodges it."** (Gourmet) — intro + immediate physical behavior; "casually" doing the comedy.
4. **"Brandon takes a burger patty and puts it on a soggy bun with wilted lettuce, a sad tomato, and a limp pickle."** (Gourmet) — rule-of-three adjectives, each sadder; "a sad tomato" is personification at zero cost.
5. **"He vomits in the trash can nearby."** (Gourmet) — buried mid-montage between competent chef beats ("He cracks an egg into a pan with one hand while flipping pancakes with the other. / He vomits in the trash can nearby. / His hand slightly shakes as he slices strawberries.") — the rotten beat hidden in a competence list, never acknowledged.
6. **"No response. He walks over to her, CHUCKLES, and rips a fart in her face. He LAUGHS. She still doesn't respond. His smile slowly fades. She's not breathing."** (Gourmet) — the hardest pivot in the corpus. Lowest comedy to death in five sentences, no signposting. End of Act One.
7. **"Brandon walks in and sees his MOM passed out on the couch with a half-finished glass of wine, an empty wine bottle, and a cigarette cherry still lit in the ashtray. The only light in the room comes from The Food Network across the couch."** (Gourmet) — a room described as a biography. Specific objects carry the sadness; no editorializing.
8. **"A rough crowd. ROCK music blasts. The blue collar and the toothless are settled up at the bar."** (Nothing But A Good Time) — "the blue collar and the toothless": adjectives nominalized into a congregation. Pure prose voice.
9. **"Eric's a well read, decent looking guy, but compared to the other people who inhabit this bar, he's a stud."** (NBAGT) — narrator editorializes with a comparative insult to the whole room.
10. **"The walls are naked, aside from a few pictures above the desk of Hunter S. Thompson, Bukowski, Hemingway, Camus, etc."** (NBAGT) — the gonzo lineage is original equipment.
11. **"A FASHIONABLE WOMAN, late 40's with a gross amount of work done"** / **"A WELL DRESSED MAN, early 50's with swagger"** (NBAGT) — intro economy: one detail, maximally loaded.
12. **"Doilies and Jesus figurines on every table. Multiple cats roam the living room."** (NBAGT) — set description as character study (Mrs. Thompson never needs describing after this).
13. **"Wulfgang's mansion is extravagant, covered in beautiful decor and art. An odd amount of phallic sculptures sprinkled in."** (NBAGT) — elevated register, deflating final fragment. The Hard Cut working inside an action line.
14. **"Eric stands there, in a thong, with a giant dildo in his hand. He looks at the body, then at Nadia."** (NBAGT) — the post-chaos inventory shot: freeze the absurd tableau, list its components flatly.
15. **"GROG (13), a gargantuan man-child with multiple chins and an underbite."** (LOTF) — intro: escalating physical specifics, no judgment word needed.
16. **"FLIP (9), a small girl with an oversized t-shirt and a raspy voice, lets out a WAR CRY, but then trips and falls."** (LOTF) — intro + instant deflation of the intro.
17. **"ROGUE (12) dirt-clumped hair and twitchy eyes, gnawing on the wing of a seagull, in the middle of the room."** (LOTF) — horror-specific physical detail played for comedy.
18. **"ABBY shows the island off like Vanna White."** (LOTF) — pop-culture stage direction: one reference does the whole blocking.
19. **"Zazu lays on it's back with dilated pupils."** (LOTF) — a drugged monkey conveyed in seven words, medical specificity ("dilated pupils") as the joke.
20. **"A boar SQUEALS and runs by with Flip SCREAMING on its back. / Beat. / Grog HUFFS and PUFFS as he waddles in the same direction."** (LOTF) — "Beat." as a written comedy rest; the slow follower as the second punchline.
21. **"A busy office. Close up of office supplies. Phones RING. Copies are made. Coffee drips. Most in their cubicles. Basic office hullabaloo."** (Fetish) — staccato scene-set, then a register-break colloquial summary ("Basic office hullabaloo") that tells you the narrator is a person.
22. **"SHOT OF A FUNNY THING that you would see at a park. Maybe a homeless man pooping."** (Drug Deal) — the narrator talking to himself on the page; draft-casualness as voice.
23. **"SHOT OF: Cocktail weenies. A fly SHAKES it's wings and scrapes it's legs as it crawls all over it."** (New Year's Resolutions) — opening image of the whole sketch: party promise undercut by grotesque macro detail.
24. **"Everyone LAUGHS. Lliam laughs a bit too long. / Everyone, including Father Time, stares until he stops."** (New Year's Resolutions) — social-cringe timing written as blocking.
25. **"The hotel looks like it's standing on its last leg."** + **"Allen stares at two raggedy stray dogs eating a carcass next to a food cart. A sign on the food cart reads 'Scorpion: Ten Baht'."** (Food Traveler) — place established through one terrible sign and one worse tableau.
26. **"Heather takes her finger off of her ear. In her other hand, she holds a torn-out wack-a-mole mallet. She stares at the cashier."** (A.P. Bio) — action-movie gravitas applied to a child in an arcade; the prop does it.
27. **"He's hunched over and takes a bite of his sandwich. A bunch of it falls onto his plate. A tomato falls on the ground. He looks around, picks it up, and puts it back on his sandwich."** (A.P. Bio) — pathetic-character physical comedy in flat declaratives; no adjectives, all verbs.
28. **"Gene's looking up at him with PUPPY DOG EYES. The fish has a BLANK STARE."** (Go Fish, Bob) — parallel-structure button; the second sentence is the joke because it's formatted like the first.
29. **"Gary's crying at the table drinking straight from the bottle. In one hand, a picture of his family. In the other, a picture of his briefcase and cell phone."** (I Quit) — absurd symmetry; a framed photo of a briefcase is the entire satire.
30. **"Closeup of PETEY as the spit slides down his bruised face."** (Petey Possum) — closing image as the thesis. No dialogue needed.

### Cross-cutting observations on the action-line voice

- **Verbs over adjectives** for physical comedy; adjectives reserved for intros, where they come in loaded triples.
- **Flat declaratives around grotesque content** — the sentence never reacts to what it reports.
- **Register breaks** ("Basic office hullabaloo," "Maybe a homeless man pooping") where the narrator's spoken voice punctures screenplay formality. Same instinct as his prose's colloquial closers.
- **"The kids lose their shit"** appears 3× in Petey Possum and once in New Year's ("People in Times Square lose their shit") — a real lexicon item, used as a refrain on the page.

---

## How Bea uses this (the "How this maps to your job" note for `bea-storyboard-context.md`)

- The per-shot `prompt` is prose-action, not dialogue. **Verbs over adjectives.** When a beat is physical comedy, write flat declaratives (exemplars 27, 14); when it's an intro/establish, the loaded-triple is allowed (exemplars 1, 4).
- **The Loaded Object is your shot.** When Sam's beat carries a loaded object in `intent`/`notes`, board *that object*, the way exemplars 7 / 29 / 12 carry the whole story in props. Don't board a held face for an emotional beat — board the object in the frame.
- **Register stays inside the pencil-test medium.** The bank shows the *voice*; the *medium* is fixed: every `prompt` still ends in the pencil-test-register clause block (cream paper, warm graphite line, construction lines, 16:9 fixed camera, "NOT a clean digital/anime/3D render") exactly as the Spark `shots.yaml` prompts do. Voice rides inside that frame; it never replaces it.
- This is the anima loop, not a screenplay: anima is a fixed-camera keyframe loop. Use the *prose voice* and the *object economy*; the *camera-move* vocabulary (pans, push-ins) stays deferred until a Phase-6 motion piece.
