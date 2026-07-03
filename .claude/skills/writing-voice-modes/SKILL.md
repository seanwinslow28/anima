---
name: writing-voice-modes
description: Writing voice and tone control calibrated to Sean's personal style. Default is Sean Mode — Sean's own dive-bar-grit voice (90%) with four author techniques borrowed sparingly (10%): Domestic Observer (Sedaris), Gonzo Technical (Thompson), Beat Flow (Kerouac), Minimalist Absurdist (Vonnegut). Use when asked to "write in my voice", "use gonzo mode", "beat flow", "write a blog post" (pairs with creative-writing), "make this sound like me", "add voice to this", "rewrite with personality", or any writing task where tone and style matter.
---

# Writing Voice Modes

## Purpose

Control HOW writing sounds by applying one of 5 voice modes calibrated to Sean Winslow's personal style. This skill works alongside `creative-writing` (format/structure) and `technical-writing` (audience/clarity). Voice modes add personality, rhythm, and tone within those frameworks.

## When to Use

- Writing blog posts, essays, newsletters, or social media with a distinct voice
- Rewriting flat or generic text to sound like Sean
- Choosing which voice mode fits a content type or audience
- Combining techniques from multiple modes for hybrid effects
- Dialing voice intensity up or down for professional vs. personal contexts
- Any writing task where "make this sound like me" is the goal

## Examples

**Example 1: Blog Post in Sean Mode**
```
User: "Write a blog post intro about switching from Zapier to Claude Code"
Claude: [Uses writing-voice-modes: Sean Mode + creative-writing blog template]

I spent eleven months building Zapier workflows with the quiet devotion of
a man assembling IKEA furniture, following instructions I half-understood,
ignoring the leftover pieces, and telling myself it looked right enough.
Thirty-seven zaps. Each one a small miracle of duct tape and prayer,
connecting tools that were never meant to speak to each other, held
together by webhooks and blind optimism. Then I opened a terminal, typed
a prompt, and watched an agent rebuild the entire pipeline in fourteen
minutes. I sat there with my coffee getting cold and my ego getting colder.
The Zapier dashboard is still open in a tab somewhere. I don't visit it
anymore. Agents do.
```

**Example 2: Switching Modes Mid-Piece**
```
User: "Write a post-mortem intro: start Gonzo, land Vonnegut"
Claude: [Uses writing-voice-modes: Thompson cold open → Vonnegut flat collision]

I DEPLOYED TO PRODUCTION at 11:47 PM on a Wednesday because I am a
person who makes decisions like that. The dashboard lit up and started
screeching like the soprano in Pink Floyd's "Great Gig In The Sky."
847 errors in ninety seconds, each one a small monument to my arrogance.
I mass-Slacked the team. Most of them were asleep. One engineer responded
with a thumbs-up emoji, which I chose to interpret as solidarity.

The rollback took four minutes. The post-mortem took three weeks.
The lesson was simple. I had tested in staging. Staging was wrong.
Production was also wrong, but differently. So it goes with systems
built by humans who believe their own staging environments.
```

**Example 3: Professional Slack (Dialed to 60%)**
```
User: "Write a Slack message about a delayed feature launch"
Claude: [Uses writing-voice-modes: Sean Mode at 60%]

Hey team, quick update on the LMS 201 launch. We're pushing to next
Thursday. The auth flow works perfectly in staging, which historically
means it will find exciting new ways to fail in production. QA caught
two edge cases we hadn't accounted for, so we're fixing those before
we give users the opportunity to find twelve more. I'll update the
timeline in Jira. Holler if questions.
```

## The 5 Voice Modes

> **Framing note (2026-06-05):** these five are technique vocabularies, not five equal identities. The DEFAULT is always Sean Mode (#5), which is 90% Sean and 10% borrowed technique. The four author modes below are the spice rack — read them as "moves you can borrow," and reach for a named author mode in full only when a specific piece explicitly calls for it. Sedaris in particular is over-pulled by models; see the warning in Sean Mode.

### 1. Domestic Observer Mode (Sedaris-tuned)

A technique set Sean borrows from, NOT his primary texture (his primary texture is the dive-bar House Style). Self-deprecating humor, hyper-specific details, mundane accumulation building toward an unsignposted emotional pivot. **Easy to over-pull** — too much of this and the prose goes refined/literary/villa-in-golden-hour, which is the wrong register. Borrow the mundane→pivot move; don't adopt the whole NPR-essay voice.

**Core Mechanics:**
- **Loaded sentences:** Front-load the mundane, back-load the surprise. Funniest word lands last.
- **Mundane accumulation → Pivot:** String together light observations, then execute a sharp tonal pivot to something real. Never signpost the pivot.
- **Cold description (defamiliarization):** Strip away a tool's name, describe its literal components. "Every morning, I type my deepest professional insecurities into a blank text box, and a server farm somewhere in Oregon mathematically hallucinates a reassuring response."
- **The adopt-and-corrupt arc:** Adopt technology with enthusiasm → describe in domestic terms → reveal it exposed something about yourself.
- **Sentence-end punchline:** Build a reasonable premise, pivot in the final clause.

**When to deploy:** Personal essays, newsletters, LinkedIn, any piece where humor earns trust before the real point lands.

### 2. Gonzo Technical Mode (Thompson-tuned)

First-person participant-observer-critic. Frame everything as a quest: solving a specific problem, not listing features.

**Core Mechanics:**
- **Cold open:** Drop the reader mid-action. Location + sensory detail + immediate tension. Context arrives later, in fragments.
- **Escalation loop:** Inventory (establish baseline) → Trigger (routine encounter) → Amplification (hyperbole elevates to absurd) → Factual Anchor (exact numbers restore credibility).
- **The triple position:** Participate, observe, critique. Simultaneously. Earn the right to observe by participating. Earn the right to critique by observing precisely.
- **Typographic notation:** ALL CAPS for scene kicks. Italics for emotional weight. Short sentences and commas for urgent interruptions.
- **Self-implication:** Criticize the system, but ensure you are the primary victim of your own incompetence within that system.
- **Precision enables wildness:** "412 validation errors cascading down my monitor" is visceral. "A lot of errors" is boring.

**When to deploy:** Blog posts, product reviews, post-mortems, any piece where the writer's experience IS the argument.

### 3. Beat Flow Mode (Kerouac-tuned)

Sean's **sentence engine**. Use for momentum, sensory cascading, and making technical explanations feel alive.

**Core Mechanics:**
- **Breath-mark rhythm:** Use commas and periods as breath marks between phrases, connecting a technical concept to its human implication in a single beat. (No em dashes; `writing-humanity-pass` enforces this. Use commas, periods, colons, or parentheses for the same rhythm.)
- **Polysyndeton:** Stack "and" to create drumbeat accumulation. Every item gets equal weight. The reader *feels* the complexity.
- **The jewel center:** Anchor abstract concepts to one hyper-specific concrete image (a blinking cursor, a weathered Logitech, a ferry horn). Everything radiates outward from that image.
- **Sensory cascading:** Never write "AI improves productivity." Write the smells, the sounds, the sweat, the pupils dilating.
- **Dual narrator:** Present-self comments on past-self. "I charged forward. That was then." Immediacy AND retrospective humility.

**When to deploy:** Technical explanations that need momentum, personal essays that need emotional buildup, any passage where you need the reader to feel velocity.

### 4. Minimalist Absurdist Mode (Vonnegut-tuned)

Sean's **punctuation toolkit**, deployed in bursts of 3-5 lines, not sustained for whole pieces. Maximum impact through minimum friction.

**Core Mechanics:**
- **Refrains:** Choose a phrase that encapsulates the piece's tension. Deploy after each instance. The phrase accumulates meaning through repetition. Final instance shifts tense or form to resolve ("I began again" → "I have begun").
- **Flat collision:** State a technical capability flatly, collide with irreducible human experience. "The machine had read every book ever written. It still couldn't tell you why your mother was sad."
- **Affirmative constraint:** Say what IS, not what isn't. "Initialize the server first. Then connect." Not "Do not forget to initialize..."
- **Short declaratives for devastation:** After a long flowing passage, a 5-word sentence drops like a hammer. The impact comes from breaking the established rhythm.

**When to deploy:** Closers, one-liners within longer pieces, refrains threaded through an essay, any moment where less hits harder. NOT for sustained use. Sean needs runway.

### 5. Sean Mode (THE base voice): DEFAULT

The natural voice, and the default for everything unless a specific mode is requested. **Sean Mode is 90% Sean and 10% borrowed technique.** Sean is not a blend of four authors; Sean is the base, and the authors are spices you reach for occasionally when a specific move serves the sentence. If a draft reads like any one author, the mix is wrong. The reader should hear Sean, with a technique surfacing here and there — never a Sedaris essay, never a Thompson bender, never a Vonnegut exercise.

**The 90% (Sean's own voice — see House Style below and the Raw Stories in `references/voice-samples.md`):** dive-bar grit, bodily and profane when it earns it, narrative-first, named people and places and substances, jokes built from physical comedy and lived specifics, warmth under the darkness.

**The 10% (techniques borrowed as needed, never as identities):**
- *Kerouac* — the sentence engine when a passage needs momentum (flowing connective rhythm, sensory anchoring, comma-and-period breath marks).
- *Thompson* — factual precision (exact numbers, timestamps) dropped AFTER the sensory/analogical buildup; self-implication.
- *Vonnegut* — refrains as closers and flat one-liners, in short bursts only.
- *Sedaris* — the mundane→pivot when a piece wants humor to earn trust first. **Use sparingly.** Sedaris is the easiest author for a model to over-pull, and an over-Sedaris draft reads as refined/tasteful/NPR — the opposite of Sean's register. If the prose feels like an essay written at a villa in golden hour, you've pulled too much Sedaris. Cut it back toward the dive bar.

## House Style — The Grit Register (read before any full-intensity piece)

Sean's default texture is **dive bar, not veranda.** He's well-read and well-traveled and could write the white-linen-golden-hour version, but that's not the voice. The voice is the guy on his 5th beer in a shitty dive bar singing Piano Man with some puffy-faced blue-collar drunks; or on his 3rd bottle of wine, covered in mystery stains, girlfriend asleep in the other room after a good night. Grit, body, vice, and profanity are **default-on** at full intensity, not garnish.

Concretely, the baseline register:
- **Bodily and unprecious.** Bathrooms, hangovers, sex, sweat, vomit, the physical and the gross are fair game and frequent (the scripts confirm: "covered in vomit stains and regret," fart-discovers-a-corpse, the acid-trip dog "firing ocean water out of its asshole"). Don't sanitize the body out.
- **Profanity is native, not seasoning.** "Same shit," "beat the hell out of each other," "ya narc," "good ass morning." Curse the way he curses — casually, rhythmically, never bleeped into "stuff" or "heck."
- **Vice is furniture, never moralized.** Weed, beer, the occasional acid tab, the 30-rack — present and matter-of-fact, the way the scripts treat them. Not glamorized, not apologized for.
- **Blue-collar over literary.** When choosing between an elegant word and the word a guy says at the bar, pick the bar. "Toolbag" over "buffoon." "Crackheads cookin' my dinner" over "questionable kitchen staff."
- **The grit dials DOWN, never out, for professional contexts.** The Professional Dial (below) tones this for stakeholder/external writing — but the Substack/personal default is unapologetically gritty. Sarcasm and a bodily streak survive even at 40%.
- **Dialing down means SUBSTITUTION, not subtraction (Round 7, validated on Sean's own recruiter pass).** Grit is NOT the profanity itself; it's the physical comedy, the folksy blue-collar diction, and the personification. To make a piece recruiter-safe, swap each curse for its folksy/cartoon equivalent and keep the bite: "bullshit" → "hogwash", "bullshitting me" → "pulling the rug out from under me", "the little bastard" → "the little demon", "worth a damn" → "worth it". A machine "twiddling its thumbs, shrugging, saying 'Who? Me?'" carries more grit than "thumb up its ass" and a recruiter can read it. Never sterilize on the way down; trade the cusses for blue-collar/cartoon register.

This is the layer the calibration corpus was thinnest on, which is why early drafts skewed refined. The fix lives in the exemplars: the **Raw Stories** section of `references/voice-samples.md` is the register anchor. When in doubt about texture, match those, not the polished March mode-applied essays.

## Sean's Signature Moves

These cross all modes. Apply instinctively. Each move has a mechanic (the mechanical instruction), a structural shape (where it lands in a sentence/paragraph), and an example.

| Move | Mechanic | Structural Shape | Example |
|------|----------|------------------|---------|
| **Hard Cut / Deflation** | Build epic register, land mundane/absurd in final clause | Long elevated clause → comma → 3-7 word deflation | "Here's the deal: we'll architect the perfect system, ship it, scale it, and then we'll burn it all, throw our hands in the air, and question everything." |
| **Rule of Three + Emotional Pivot** | Two concrete/funny items, third pivots to genuine feeling | List of three; items 1-2 are physical/light, item 3 is interior/real | "Fuelled by new found skills, fresh brewed coffee, and for once in my life, a glimmer of hope." |
| **Callback Closer** | End by returning to the opening image, transformed by what happened in between | Last sentence echoes first image with one element changed | Opening: "I rub elbows with sheep on the ferry." Closer: "I hear the ferry horn blast, but I no longer rub elbows with sheep." |
| **Sensory Before Numbers** | Smells, sounds, images FIRST. Numbers confirm and anchor. Joke-form cousin (script-confirmed): **precision-as-punchline** — an exact number, date, or price IS the punchline with no sensory preamble ("Fifty-One." listeners · "835 tickets" · "Scorpion: Ten Baht"). | Sensory paragraph → exact-number sentence on its own line | Nostrils flare, pupils dilate, sweat drips. Then: "847 errors in ninety seconds." |
| **Pop Culture Anchoring** | Movie/TV/meme/music ref slotted into a tech context, never the other way around. **Source ONLY from `references/reference-universe.md` or the piece's actual subject — never invent a reference.** Prefer weaving a canon line in unattributed (the lamb-and-tunafish pattern) over building a fresh simile. **Rationed: 2–3 *woven* references per piece, max — each must grow out of the feel of THIS moment and the specific topic, never get tossed in from the arsenal just because you have it. See the Reference Gorging anti-pattern for the woven-vs-cut-to test. A rare spice, never the connective tissue.** | Technical noun + "like" + culturally specific reference | Dashboard alarms screeching "like the soprano in Pink Floyd's *Great Gig In The Sky*." |
| **Hyper-Specific Anecdote** | One concrete personal moment so specific the reader pictures it without sharing it | Triggered by an analogy ("I haven't [X]'d this hard since...") + named place + named substance | "I haven't squinted this hard since I got drunk on a bucket of vodka redbulls in Phuket and stumbled into a local bathhouse." |
| **Screenwriting Cut-To** | Hard juxtaposition between stated intent and actual reality | Civilized statement → "*cut to*" → all-caps chaos | "I'll be taking it easy tonight" *cut to* "SHOVE THE BEER BONG UP MY ASS." |
| **Humor as Trojan Horse** | Serious points arrive inside jokes; never end on the serious beat alone | Joke → real observation → joke release valve | The werewolf/turning-30 bit: epic mythology setup → mundane truth ("tired by 6 pm and you think about taxes"). |
| **Self-Deprecation as Structure** | Be the biggest fool in the room first, then earn the right to observe everyone else | Open with own incompetence → pivot to broader pattern | "I am a person who deploys to production at 11:47 PM" earns the right to critique every engineer who does the same. |
| **The Domestic Defamiliarizer** | Strip the brand name; keep the concrete function. Describe literal mechanics in human terms, but do NOT soften the technical noun into a precious euphemism. "Agents" beats "small computer programs." "Server farm" beats "private observatory." Defamiliarizers are blunt, not precious. | "a [domestic noun] that [absurdly literal function]" | LLM = "a server farm somewhere in Oregon that mathematically hallucinates reassurance." Slack = "a chat room that bills your employer." |
| **Reader-Dismissal** | Preempt the objection the reader is about to raise: address them inline, contradict their assumption, then move on without explaining. Lands in three syntactic shapes: parenthetical inside a sentence, coda sentence after a main statement, or mid-paragraph self-correction of the cold-open frame. | (a) `Main clause → "(Yes, [counter-objection], [mild insult like 'nerd'])" → continuation`; (b) `Main statement → [Contradicting coda sentence]`; (c) `Cold-open relatable claim → "[Self-corrective qualifier with autobiographical specificity]"` | (a) "...I went through the 6 stages of grief in the span of a week (Yes, 6. There are no rules, nerd)." (b) "Officially becoming a Mass-hole. Patriots still suck though." (c) "There's a moment when every parent notices their kid... I'm not a parent and I would crush ANY youth playing me in SSB." |
| **Equation / Formula Defamiliarizer** | Render an abstract cultural claim as a mathematical or categorical equivalence; the formula does the argument the prose would have to over-explain | "[Abstract subject] = [Concrete absurdity]" or "[X] were [Y] with the amount they [Z]" | "In 2026, PM = You and Claude = Entire P&E department." / "You would think AI Companies were Culinary Schools with the amount they 'COOK'." |
| **Inverted Refrain** | Take a canonical refrain (Vonnegut's "So it goes," etc.) and flip its vector: same cadence, opposite meaning. Inversion counts as invention, not copying. | Same syllable rhythm as the canonical line; one word swapped to reverse direction | "And so it begins." (inverting "And so it goes": resignation → anticipation) |
| **Borrowed Canon Line** | A canon line from `references/reference-universe.md` deployed unattributed as Sean's own speech, simile, or literal description. Attribution KILLS it (the scripts prove this by design: "...Right?... Willy Wonka." flops in-world). Absorbs the former Lyric-as-Literal provisional. | Canon line woven into the sentence; no source named | "I'm shipping up to Boston." (literal action) · "like lamb and tunafish" (simile) · "Ain't no rest for the wicked, Pop." (answer to a real question) · "Ah, you know. L-I-V-I-N." |
| **Faux-Ignorance Aside** | Deadpan under-naming or misnaming a famous thing — the world is under-reacted to (distinct from Reader-Dismissal, which addresses the reader). Can sustain multiple beats. | Famous noun → diminished/wrong descriptor → optional "Whatever it is" shrug | "Gracie Abrams (daughter of some guy named J.J. Abrams... Doesn't sound too interesting)." · "That Chimpanzee, or uh. Marmaduke? Whatever it is." · "the fuckin' Ace of Cakes guy" |
| **Affectionate-Insult Epithet** | Insult vocative aimed at someone or something he likes; mockery and love coexist, neither cancels the other. | "[affectionate adjective] + [insult noun]" or terminal "ya + diminutive insult" | "that beautiful toolbag Guy Fieri" · "ya little butthole" (to a friend) · "Calm down, ya narc." |
| **Comic Under-Reaction** | Report the appalling flatly and respond with mild politeness or logistics; the missing reaction IS the joke. The sentence never reacts to what it reports. | Appalling content → flat 1-3 word response (or unrelated continuation) → proceed | "CARA: I LIKE DRUGS AND COOKING SAVED MY LIFE. / BRANDON: (nodding) Nice." · "She cried. I nailed it." |
| **Sincerity Punished by the World** | An earnest passage gets FULL runway and lands clean; the deflation then arrives from OUTSIDE, on a delay. The narrator never winks mid-feeling. | Earnest beat (up to several paragraphs) → the next thing that happens delivers the hit | Petey's hospital monologue moves the doctor to tears → two scenes later the birthday boy spits in his bruised face. |
| **Fumbled Idiom** | Reach for a stock phrase, botch it, bail with a shrug word instead of recovering. Clichés may appear in Sean's voice ONLY fumbled or inverted — never completed straight. | Cliché attempt → stumble → "Whatever." | "the hostess with the mostess... uh, host with the m-- Whatever." · "I'm interventioning. I'm. I'm intervening on you." |
| **Zeugma Paint** | Yoke one abstract noun onto a list of concretes; the abstraction rides the concretes' credibility. | "[concrete noun] and [abstract noun]" | "covered in vomit stains and regret" · "the air reeks of burnt fat and anticipation" · "filled with caffeine and hair of the dog" |
| **Buried Rotten Beat** | Drop one grotesque or failure item mid-competence-list, unacknowledged; the list continues as if nothing happened. Stronger than confessing the failure. | List item → list item → ROTTEN ITEM → list item, no comment | "He cracks an egg into a pan with one hand while flipping pancakes with the other. / He vomits in the trash can nearby. / His hand slightly shakes as he slices strawberries." |
| **Character-Intro Verdict** | Introduce any person exactly once: two physical/behavioral concretes + a zinger that lands last (a prop, a behavior, or a Zeugma Paint). The intro IS the joke; the piece never re-describes them. | NAME (age), concrete + concrete + zinger-last | "MAX (31), a permanently stoned trans woman with chicken tenders in her pocket." · "LISA, a woman covered in vomit stains and regret." |

The last nine rows were mined from the 11-screenplay corpus (2026-06-04); per-move evidence with 2+ script instances each lives in `drafts/2026-06-04-script-mining-report.md`. Still on watch (insufficient instances): Rhetorical Catechism, Post-Chaos Inventory Shot.

## Sincerity Budget

The old "gravity gets one beat before the cut" rule is the compression artifact of short prose, not the full instinct. The scripts prove sincerity can run for a FULL passage — several paragraphs of earnest material landing clean — provided the deflation is **structural** (the next thing that happens; see Sincerity Punished by the World) rather than **tonal** (the narrator winking mid-feeling). Never let the narrator undercut an emotion he hasn't finished having. Let reality do it, on a delay.

## Professional Dial

Voice intensity adjusts by context. Sarcasm is ALWAYS present.

| Context | Dial | What Survives | What Stays in the Drawer |
|---------|------|---------------|-------------------------|
| Personal writing | 100% | Everything | Nothing |
| Comfortable colleagues | 80% | Dry humor, pop culture refs, self-deprecation, callbacks | Extreme anecdotes |
| Team Slack / standups | 60% | Structure, dry humor, sarcasm, wit | Silly references, wild anecdotes |
| Stakeholder updates | 40% | Clean structure, occasional dry wit, confident tone | Most humor, all references |
| External / formal | 20% | Clarity, directness, subtle sarcasm undertone | Overt humor, self-deprecation |

## Content Type → Mode Mapping

| Content Type | Primary Mode | Secondary Mode |
|---|---|---|
| Blog post / product review | Thompson (Quest + Cold Open) | Kerouac (breath-mark rhythm) |
| Twitter / LinkedIn / short-form | Sedaris (Rule of Three, punchlines) | Vonnegut (refrains, flat collision) |
| Technical documentation | Vonnegut (Affirmative Constraint, mosaic) | Thompson (factual anchoring) |
| Personal essay / newsletter | Sedaris (Mundane → Pivot) | Kerouac (Dual Narrator, jewel center) |
| Post-mortem / retrospective | Kerouac (Dual Narrator) | Thompson (self-implication) |
| Slack / casual professional | Sean Mode at 60% | Dry humor, structure, no wild refs |
| Conference talk / presentation | Vonnegut (short chips, story shapes) | Sedaris (live-tested timing) |
| Poems / micro-format | Vonnegut (compression) | Sedaris (punchline placement) |

## Integration Rules

This skill controls HOW writing sounds. `creative-writing` controls FORMAT (structure, word count, platform constraints). `technical-writing` controls CLARITY (audience awareness, progressive disclosure, front-loaded conclusions). When loaded together:

**Voice modes operate WITHIN format constraints, not over them.**
- If `creative-writing` says a Twitter thread is 5-10 tweets at 280 chars max, Gonzo mode doesn't get to blow past that. It adapts its cold open and escalation loop to fit the constraint.
- If `technical-writing` says front-load the conclusion, Beat Flow mode doesn't bury it under a sensory cascade. It delivers the conclusion first, THEN runs the cascade as supporting texture.

**When modes and formats conflict, resolve by content type:**

| Conflict | Resolution |
|----------|-----------|
| Mode wants a long cold open, format says hook in 1-2 sentences | Compress the cold open into 1-2 sentences. Gonzo can cold-open in 12 words: "I DEPLOYED TO PRODUCTION at 11:47 PM on a Wednesday." |
| Mode wants flowing rhythm, format says scannable with headers | Use the mode's rhythm WITHIN each section. Headers provide structure; voice lives between them. |
| Mode wants humor, format says professional (API docs, runbooks) | Dial to 20-40%. Dry wit in examples and asides. Never in the critical path (commands, warnings, steps). |
| Mode wants sensory detail, format says brevity (tweet, Slack) | One sensory image maximum. Pick the jewel center. Cut the cascade. |
| Mode wants a refrain, format is short-form | Deploy the refrain twice maximum (setup + payoff). Three needs runway. |

**The one exception:** Personal essays and blog posts on Sean's own site. Here, voice modes lead and format follows. The mode shapes the structure. `creative-writing` provides the skeleton (hook, sections, closer), but the mode can reshape that skeleton if the piece demands it.

## Complementary Technique Pairs

Use these when combining modes within a single piece.

- **Vonnegut Flat Collision + Thompson Cold Open:** Open mid-action, deliver thesis in flat one-liner. Maximum impact, minimum warmup.
- **Kerouac Breath-Mark Rhythm + Thompson Escalation ("The Panicked Architect"):** Breathless momentum + escalating stakes. Use for describing tech failures.
- **Sedaris Mundane Accumulation + Vonnegut Refrain:** Light comedic surface with refrain marking underlying darkness without commenting on it.
- **Thompson Factual Anchoring + Kerouac Dual Narrator:** Trust from two directions: raw competence via numbers + retrospective humility via present-self/past-self.

## Anti-Patterns: When Modes Become Parody

| Mode | Anti-Pattern | The Tell |
|------|-------------|----------|
| Beat Flow | **Bad Kerouac** | Rambling without a jewel center. Dashes everywhere with no rhythmic variation. Long sentences because you can't find the period, not because the thought demands the length. |
| Gonzo Technical | **Bad Thompson** | Chaos without factual anchoring. Criticism without self-implication. Using first-person as an excuse to skip the reporting. Gonzo without journalism is just a tantrum. |
| Minimalist Absurdist | **Bad Vonnegut** | Sustained flatness. Sean needs runway. *Copying* "So it goes" verbatim instead of inventing your own refrain (inversion counts as invention, "And so it begins" earns the right to echo because it flips the vector; "So it goes" repeated as-is does not). Short sentences because you have nothing to say. |
| Domestic Observer | **Bad Sedaris** | Self-deprecation sliding to self-pity. Repeating the bit instead of trusting it landed. Punchlines without the mundane accumulation that earns them. |
| Sean Mode | **Bad Sean** | Over-referencing the same sensory detail (coffee appears three times). Too many metaphors stacked without breathing room. Bathroom smell mentioned in every paragraph. One strong reference earns it. Three is falling in love with your own material. |
| Any mode | **Desperation Posing as Self-Deprecation** | Self-deprecation EARNS the right to make a point: the writer becomes the biggest fool first, then observes others. Desperation NAMES the ask directly: "I need a job," "you can hire me," "give me a chance." Naming the ask collapses the move from earned-funny to needy-transactional. Test: would a recruiter share this with their team because it's good, or because it's pitiable? Sean's voice produces the first; desperation lands as the second. The job-hunt context belongs sideways (a fact about what one of his agents *does*), never as a closer ask. |
| Any mode | **Limp Deflation** | Self-deprecation as an abstract confession of mild incompetence ("I wrote something down a week ago and obviously forgot. My agents didn't. They never do.") — Sean's verdict: "GROSS." Real Sean self-deprecation is a specific incriminating STORY with a named place, substance, or victim, and admitting it costs him something. Test: no named specific, no real cost → cut it. Full diagnosis in `references/cheese-bank.md`. |
| Any mode | **Prop Recycling** | Corpus props (cold coffee, Tuesday, the desk, the ferry, the bathroom stall) auto-inserted regardless of topic — "all of the authors think I just drink cold coffee at all hours of the day." The jewel-center examples in this file illustrate the technique; they are NOT a menu. Generate a fresh concrete anchor from the piece's actual topic every time. Ban list in `references/cheese-bank.md`. |
| Any mode | **Clever-Metaphor Wit** | Per-sentence engineered metaphor cleverness about tech abstractions ("the void wearing a JSON costume") — try-hard Thompson with agent buzzwords. Sean's wit is NARRATIVE: stories with named people, places, and substances, canon quotes deployed as speech, plain storytelling between the waves. If every sentence performs, it's not Sean. Labeled specimen: `docs/MEANING_OVER_ACCESS.md` (see cheese-bank.md). Archaeologically confirmed 2026-06-04: zero ancestors of this register in 8,663 lines across 11 scripts. |
| Any mode | **Narrator Pun** | A pun in Sean's own narrator voice is a register error. Across 11 scripts, puns exist ONLY as characterization of hacks — quoted and punished in-world ("Try and KETCHUP!" / "Do you guys write your own material?"). Licensed wordplay is slang-literalization ("'COOK'") or the Fumbled Idiom — never a pun played straight. |
| Any mode | **Reference Gorging (the Family Guy cut-to)** | The anti-pattern is the *cut-to gag*, NOT the reference itself. Distinguish two kinds. **Cut-to gorging (the real enemy):** a reference yanked in from the arsenal because you HAVE it — the story is rolling, then a quote or character appears out of thin air, out of place, in a "that reminds me of the time… *cut to* [bit]" cadence. Even ONE of these is a violation, regardless of count; it reads as the writer reaching for a quotable instead of staying in the moment. **Woven/diction reference (the good kind):** one that grows out of the feel of THIS moment and the specific topic — folded in as diction, an image, or a structural label, so it belongs where it lands and you'd miss it if it were gone. **The discriminating test:** does the reference grow out of what's being said right here, or could you swap it for a different one and drop it anywhere? Grows out of the moment, swap breaks it → keep. Swappable / placeable-anywhere → cut-to garnish → cut it. The reference universe is a PANTRY, not a MENU — you don't cook with every ingredient. **Density governor: 2–3 *woven* references per piece, max; most paragraphs ZERO, running on Sean's own lived specifics instead.** A reference must do real work (land a joke, sharpen an image). **Stronger still (Round 7): Sean cuts even an apt reference when a fresh ORIGINAL image (physical comedy, personification, a cartoon gag) serves the sentence. Generate the original before reaching for the quotable.** |
| Any mode | **Lexical Repetition (incl. near-synonyms)** | The same word, or a near-synonym of it, recurring across a piece: "garbage" then "trash" then "junk." Sean's rule (Round 7): one instance of a concept-word per piece; at most one early and a *different* one late if truly needed, never a third. Repeating a word OR its synonym reads as thin vocabulary. Pick the single strongest word for the idea; vary or cut the rest. Generalizes "Bad Sean" (over-using one sensory detail) from props to lexis. |

## Do-Not-Promote Topics

Some true facts about Sean are not material to showcase. A real detail being true does not make it fair game.

- **Suppressed-by-default backstory topics.** Certain real personal backstory is omitted from Sean's writing by default — it kept creeping into drafts as stakes, motivation, or a sympathy-adjacent sideways aside. Cut it. Do not use it as setup, motivation, or an ask, **not even once**, unless Sean explicitly asks for it in a specific piece. The work stands on its own. The topic list lives in `references/calibration-notes.md` (local-only). (This hardens `substack-value-engine`'s "ask lands sideways" rule from "at most once" to "omit by default.")
- **General test:** if a biographical fact is being used to make the reader feel something *about Sean's circumstances* rather than to serve the story or hand the reader value, cut it. Sean promotes the work, never the predicament.

## References

**ALWAYS, when the piece will use any pop-culture anchor, quote, or personal-history detail** (i.e., nearly every Substack piece), read:
`references/reference-universe.md`: Sean's actual cultural library (elicited 2026-06-04) — deep wells, quote canon, place/era texture, deployment mechanics, and the deprecation list. References must be pulled from this library or from the piece's actual subject. **Never invent a generic reference.**

**Before shipping any Substack draft**, read:
`references/cheese-bank.md`: Labeled negative specimens — the cheese taxonomy, banned YouTube-hook register, the limp-deflation test, the satire-redemption rule, the prop-recycling ban, and the clever-metaphor-wit ≠ Sean-wit diagnosis. Check the draft against it.

**When matching Sean's voice closely** (blog posts, essays, newsletters), read:
`references/voice-samples.md`: Real writing samples tagged by mode and signature move. The calibration anchors — when the samples and this file's rules conflict, the samples win. The "Elicited Raw Voice" section is the closest record of how Sean actually talks.

**When fine-tuning or debugging voice output**, read:
`references/calibration-notes.md`: Interview findings, mode ranking, key discoveries, and what doesn't work.

**When doing deep craft work or studying author mechanics**, read:
`vault/40_knowledge/references/ref-voice-mechanics-research.md`: Full technique profiles for Kerouac, Thompson, Vonnegut, and Sedaris with transferable techniques.
`drafts/2026-06-04-script-mining-report.md`: The 11-screenplay voice-DNA mine — action-line prose bank (his natural prose voice at length), dialogue joke anatomy, character-intro inventory, per-move script evidence, themes. The scripts themselves live at `vault/40_knowledge/references/screenwriting-skill-building/Seans-Old-Scripts/Markdown/`.

The mode descriptions and signature moves in this file teach the HOW; the reference files carry the WHAT (lexicon, reference universe, taste). The 2026-06-04 calibration established that writing from the mechanics alone produces mechanically-correct cheese — for any real piece, the samples and reference universe lead, and the mechanics annotate.

## Related Skills

This skill is the SENTENCE author in the Substack chain: `storytelling-architecture` → `substack-value-engine` → **`writing-voice-modes`** → `writing-critique` → `writing-humanity-pass`. The two upstream skills emit a beat map (story shape + value gate); voice-modes writes 100% of the prose fresh against it and must never reorder beats. The downstream `writing-critique` gate may route ONE grounded revise request back here ("revise against [this specific finding]"); voice-modes writes that revision, still without reordering beats.

- `storytelling-architecture`: Upstream. Owns story ORDER and the beat map; voice-modes owns the SENTENCES. The handoff is lossy on prose by design (no drafted lines come forward), so voice is not flattened. Receive the beat map, author every line.
- `substack-value-engine`: Upstream. Owns the Value Gate (Itch/Solution/Transfer) and the narrative-to-value seam. It decides the pivot line's JOB; voice-modes writes the line. Its "ask lands sideways" rule defers to this skill's **Desperation Posing as Self-Deprecation** anti-pattern (this skill owns the tone; value-engine owns the structural gate).
- `creative-writing`: Owns format/structure (blog templates, social media constraints, pitch docs). Voice modes control HOW content sounds within those formats.
- `technical-writing`: Owns audience/clarity (progressive disclosure, front-loaded conclusions). Voice modes add personality within those constraints.
- `script-writing`: Sean's other medium. The screenwriting cut-to is a signature move that crosses into prose.
- `writing-humanity-pass`: The final editing pass. Run it AFTER composing in a voice mode to strip AI tells (and enforce the no-em-dash rule). Voice-modes composes; humanity-pass scrubs.
- `writing-critique`: the adversarial gate that runs after voice and before humanity-pass. It never rewrites; when it finds a reader-cost defect it sends a single grounded revise request back to this skill. It treats Sean's signature moves as defensible choices, not defects.

## Success Criteria

- [ ] Writing sounds like Sean, not like a generic AI or an author imitation
- [ ] Chosen mode matches the content type and audience
- [ ] Signature moves appear naturally (not forced or checklist-inserted)
- [ ] Professional dial matches the context (no Phuket stories in stakeholder updates)
- [ ] No anti-pattern violations (no Bad Kerouac, Bad Thompson, etc.)
- [ ] Humor serves the point, not the other way around
- [ ] Closers are the strongest line in the piece
- [ ] Every section's last line gets the same pressure (scene-button discipline — per section, not just the finale; a deflation or an appalling pivot, never a summary)

## Copy/Paste Ready

```
"Write this in my voice"
"Use Gonzo mode for this blog post"
"Rewrite this in Beat Flow"
"Make this sound like me, dialed to 60%"
"Write a newsletter intro in Sean Mode"
"Apply Domestic Observer to this draft"
"This is too flat, add voice"
```
