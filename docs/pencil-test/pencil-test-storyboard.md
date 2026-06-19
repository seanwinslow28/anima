# Pencil Test — Sean Winslow
## Production Storyboard v1.0

**Format:** 2D pencil test animation on vintage production paper
**Style reference:** A-1 (generic) and A-2 (Sean) character sketches
**Background:** P-32A production paper with blue grid lines
**Frame rate:** 12 fps (ones) or 24 fps (twos) — classic pencil test timing
**Deliverables:** Act 1 hero loop (GIF/WebM) + Act 2 full piece (MP4)

---

## Act 1 — The Hero Loop (3-5 seconds)

Self-contained loop for the portfolio hero section. Ships independently.

### Beat 1: The Spark (frames 1-12, ~1 second)

**Action:** Sean stands in the A-2 pose, holding his stylus. He glances down at the stylus in his hand, then looks up — eyebrows raise slightly, eyes widen just a fraction. The half-smile broadens. He's had an idea.

**Key poses:**
1. **F1 — Idle hold:** A-2 pose exactly as generated. Stylus in right hand, weight on back leg. This is also the loop return frame.
2. **F6 — Glance down:** Head tilts ~15° downward. Eyes drop to stylus. Slight shoulder dip — the "contemplating" pose.
3. **F10 — The spark:** Head snaps up (fast action — 2-3 frames). Eyebrows lift. Eyes brighten. Mouth shifts from closed half-smile to open half-smile showing a hint of teeth. Left shoulder rises slightly — anticipation.

**Animation notes:**
- Held frames on F1 (hold 2-3 frames before movement starts) to give the loop a breathing point
- The head snap from F6→F10 should be fast (3-4 frames) — this is the "idea" beat and should feel energetic
- Subtle secondary motion: hair bounces slightly on the head snap
- Keep the body mostly still — this beat is all in the face and head

**Reference:** Classic Disney "take" — the moment of recognition. Not a full-body take, just a head/eyebrow version. Think Milt Kahl subtlety, not Tex Avery exaggeration.

---

### Beat 2: The Draw (frames 13-30, ~1.5 seconds)

**Action:** Sean raises his stylus arm and draws a quick gesture in the air. A trail of pencil-sketch lines follows the stylus tip. The lines swirl and resolve into a tiny pixel sprite (16BitFit style) that bounces once.

**Key poses:**
4. **F13 — Wind up:** Right arm lifts, elbow leads. Stylus tip moves to roughly head height. Body leans slightly into the gesture — weight shifts forward.
5. **F18 — Mid-gesture:** Arm sweeps right in a confident arc. Pencil lines trail behind the stylus tip — sketchy, loose, overlapping. The lines should feel like real pencil marks on the production paper.
6. **F24 — Lines resolve:** The trailing pencil marks cluster and transform into a small pixel sprite. The sprite should be recognizable as a 16BitFit character — 32x32 aesthetic, idle animation pose. The style shift from pencil to pixel should feel magical but natural.
7. **F28 — Sprite bounces:** The sprite does one small bounce (squash and stretch) as it "comes alive." Arc trajectory — up slightly, then down to land.

**Animation notes:**
- The pencil trail effect: 4-6 loose pencil strokes that follow the stylus with slight delay (like a ribbon trail). They converge into the sprite shape. Use decreasing opacity as lines age.
- The sprite is a separate animated element composited over the character animation. It has its own mini idle loop (2-3 pixel frames cycling).
- The style transition moment (pencil marks → pixel sprite) is the hero moment of Act 1. Spend extra time on this — the marks should feel like they're being "drawn into existence."
- Sean's face tracks the stylus tip, then tracks the sprite once it appears.

**Technical note:** The sprite overlay can be pre-rendered separately and composited in After Effects/Premiere. This means the character animation and the sprite animation are independent production tracks.

---

### Beat 3: The Nod (frames 31-42, ~1 second)

**Action:** The sprite lands on Sean's left shoulder. Sean glances at it, does a small satisfied nod, then turns back to his starting position. The sprite fades as we approach the loop point.

**Key poses:**
8. **F31 — Sprite lands:** Sean's head turns left to look at the sprite on his shoulder. Slight smirk — he's pleased with what he made.
9. **F36 — The nod:** Small, definitive downward nod. Not big — just a single chin-drop that says "yeah, that's good." This is the emotional payoff of the loop.
10. **F40 — Return:** Head and body ease back to the A-2 starting pose. The sprite fades (3-frame dissolve). Weight shifts back to the starting leg.

**Animation notes:**
- The nod is the signature gesture. It should feel natural and confident — a craftsman acknowledging his work, not a celebration.
- Sprite fade timing: starts fading at F38, fully gone by F41. This sells the "page flip" feeling — like the animator lifted the page.
- F42 must match F1 exactly for seamless looping. The last 2 frames ease into the idle pose.
- Hold F42 for 2-3 frames before the loop restarts (this gives the eye a rest and makes the loop feel less mechanical).

**Loop mechanics:** The fade-out of the sprite + return to idle creates a natural "page turn" moment that makes the loop restart feel intentional rather than jarring.

---

## Act 2 — The Extension (15-25 seconds)

Act 1 becomes the opening. New footage adds after the loop point.

### Beat 4: Sprite Walks the Zones (frames 43-96, ~4.5 seconds)

**Action:** Instead of fading, the sprite hops off Sean's shoulder and starts walking to the right. As it walks, the ground beneath it transforms — the production paper texture shifts through three visual zones.

**Zone transitions:**
- **F43-58 — Pencil zone:** The sprite walks across raw pencil-sketch ground. Small hand-drawn elements emerge in the background: rough character sketches, gesture drawings, storyboard thumbnails. These look like pages from an animator's sketchbook.
- **F59-74 — Pixel zone:** The ground texture shifts to pixel art. 8-bit terrain tiles appear. Small game UI elements pop up: a health bar, an XP counter, a tiny inventory grid. The sprite looks right at home here.
- **F75-96 — Wireframe zone:** The ground becomes a clean grid. Wireframe UI elements sketch themselves into existence: a Kanban board with cards, a data dashboard outline, a clean navigation bar.

**Animation notes:**
- The zone transitions should be GRADUAL, not hard cuts. The textures blend at the boundaries — pencil marks slowly become pixel blocks, pixel blocks slowly become wireframe lines.
- Background elements appear with a "being drawn" effect — lines extending from nothing, as if an invisible hand is sketching them in real-time.
- The sprite walks with its native pixel animation loop — it doesn't change style. It's the constant while the world changes around it.
- Sean stays visible at frame left during this beat, watching the sprite go. He starts walking at the end of this beat (F90ish), following the trail.

---

### Beat 5: Sean Follows + AI Companion Cameo (frames 97-168, ~6 seconds)

**Action:** Sean walks right through the zones, interacting with elements in each. In the wireframe zone, the AI companion character assembles itself from the wireframe lines and collaborates with Sean.

**Zone interactions:**
- **F97-114 — Through pencil zone:** Sean walks past the sketches. He casually flips through a floating storyboard thumbnail — a callback to his animation roots. Quick gesture, doesn't stop.
- **F115-134 — Through pixel zone:** Sean pauses briefly. The 16BitFit health bar and XP counter react to his presence — the health bar fills, XP ticks up. He gives it a knowing look (he built this) and keeps walking.
- **F135-168 — Wireframe zone + AI companion:**

**AI Companion entrance (F140-155):**
The companion assembles from the wireframe grid lines. The lines lift off the ground and fold together into a simple geometric character — round head, two dots for eyes, minimal but expressive. The assembly takes 10-12 frames and should feel like origami or paper folding.

The companion floats (doesn't walk — it hovers with a gentle bob). It has a subtle pulsing glow animation — a slow, rhythmic opacity shift that contrasts with Sean's organic pencil-test movement. Two different animation philosophies sharing one frame.

**Collaboration moment (F155-168):**
The companion gestures toward the Kanban board. A new card materializes. The companion slides it toward Sean. Sean catches it, reads it (brief pause), then places it on the board himself. A small collaborative nod between them — Sean to the companion. The companion does its own version of a nod (a small downward bob of its round form).

**Character design notes for the AI companion:**
- Simple geometric form: circle head (~20% of Sean's head size), two expressive dot eyes, maybe a subtle curved line for a mouth when "smiling"
- Drawn in the wireframe zone's visual language: clean thin lines, no pencil texture, geometric precision
- But with WARMTH: the lines aren't cold or sterile. They have slight thickness variation like they were drawn with care. The eyes have genuine expression.
- Color: pencil gray like everything else in the pencil test, but its pulsing idle animation uses slightly lighter/darker values — it "breathes" differently than the rest of the drawing
- It should feel like a natural part of this world, not an intruder. It belongs in the wireframe zone because that's where building happens.

---

### Beat 6: The Survey (frames 169-210, ~3.5 seconds)

**Action:** Sean reaches the right edge of the full composition. He turns around to look back at everything — all three zones visible across the wide frame. The companion floats nearby. Sean reaches up and rearranges one of the floating elements (moves a Kanban card, or re-positions a storyboard thumbnail). Then holds the stylus up in a final pose.

**Key poses:**
11. **F169 — The turn:** Sean pivots to face left (toward the camera/viewer). Full body visible. The three zones stretch out behind him like a timeline.
12. **F180 — The rearrange:** He reaches up to one of the floating UI elements and slides it to a new position. This is the PM gesture — organizing, prioritizing, shaping.
13. **F195 — The hold:** Sean settles into a confident standing pose. Stylus held up, not quite a salute — more like a painter stepping back from the canvas. The companion hovers at his shoulder height, slightly behind.
14. **F205-210 — Freeze:** Hold this pose. Classic pencil test "hold frame" — the drawing stays still but the paper grain and pencil texture give it life.

**Animation notes:**
- The turn should be fluid — not a snap. 8-10 frames for a natural pivot.
- When he looks back at the full frame, his expression should show quiet satisfaction. Not arrogance. The energy of someone who's built something real and knows there's more to build.
- The companion's position in the final hold: slightly behind and above Sean's right shoulder. Not front and center — it's a partner, not the protagonist.
- The freeze at the end is important. Real pencil tests hold on key poses. The stillness makes the next beat (the title card) feel like a reveal.

---

### Beat 7: The Page Turn (frames 211-250, ~3.3 seconds)

**Action:** Title card fades in on the production paper. Then the page "lifts" off the peg bar — revealing the clean portfolio site beneath.

**F211-230 — Title card:**
Hand-drawn pencil lettering fades in below Sean's figure: "Sean Winslow" in a confident, slightly rough lettering style. Below it, smaller: "Creative Technologist" in the same hand. No fancy fonts — this is pencil on paper.

**F231-250 — The page lift:**
The bottom of the frame shows the production paper peg bar (the three hole punches from the P-32A background). The entire animation frame — paper, drawing, everything — lifts upward as if someone is pulling the page off the pegs. Beneath it: a clean, minimal version of the same composition. This is the transition into the actual portfolio site content below the hero section.

**Animation notes:**
- The title lettering should appear stroke by stroke, like it's being written in real-time. Not a fade-in — a draw-on effect.
- The page lift is a perspective transform — the bottom lifts first, the top follows, creating a slight curl. Think of peeling a sticky note off a desk.
- The "clean version underneath" doesn't need to be fully designed yet — even a simple white/cream background with your name in clean typography works as a transition frame. The actual portfolio site takes over from here.
- Audio note (if adding sound later): a soft paper-peeling sound effect during the lift would sell it beautifully.

---

## Production Pipeline

### Phase 1: Act 1 Keyframes (generate with Nano Banana Pro)
1. Generate 4 key poses using A-2 as anchor: idle, glance-down, spark, gesture, nod, return
2. Upload all poses + A-2 as references to maintain consistency across frames
3. Refinement passes on any poses that drift from the A-2 likeness/style

### Phase 2: Act 1 In-Betweens (ComfyUI + ControlNet)
1. Set up OpenPose ControlNet with key poses as anchors
2. Generate in-between frames with pose interpolation
3. Clean up in Procreate — fix any consistency breaks, add pencil texture details
4. The pencil trail effect (Beat 2) is a separate layer — hand-draw in Procreate or generate

### Phase 3: Sprite Element
1. Pull existing 16BitFit idle sprite or generate new one
2. Create the "pencil marks → sprite" transformation sequence (5-6 transition frames)
3. Export as separate layer with transparency

### Phase 4: Act 1 Compositing
1. Layer character animation over P-32A background in After Effects or Premiere Pro
2. Composite sprite overlay
3. Add pencil trail effect
4. Export seamless loop as high-quality GIF/WebM for hero section
5. **Ship to portfolio**

### Phase 5: Act 2 Zone Backgrounds (can run in parallel with Phase 2-4)
1. Generate three zone backgrounds with Nano Banana Pro:
   - Pencil zone: sketchy animation reference sheets
   - Pixel zone: 16BitFit game terrain with UI elements
   - Wireframe zone: clean grid with UI wireframes
2. Create transition textures between zones

### Phase 6: AI Companion Character Design
1. Design the companion character: simple geometric form, expressive
2. Generate key poses: assembly from wireframe, idle hover, card gesture, nod
3. Create the pulsing idle loop (subtle, rhythmic — contrasts organic movement)

### Phase 7: Act 2 Character Animation
1. Generate new key poses for Sean walking through zones
2. Zone interaction poses (flipping thumbnail, looking at health bar, receiving card)
3. Final survey pose and hold
4. In-between generation via ComfyUI

### Phase 8: Act 2 Compositing + Sound
1. Full composite with all zones, characters, and effects
2. Title card draw-on effect
3. Page lift transition
4. Optional: sound design (pencil scratches, subtle paper sounds, soft ambient)
5. Export full piece for festival submission

---

## Technical Specs

| Attribute | Act 1 (Loop) | Act 2 (Full) |
|-----------|-------------|-------------|
| Duration | 3.5 sec | 18-22 sec |
| Frame rate | 12 fps on twos | 12 fps on twos |
| Total frames | ~42 drawn | ~250 drawn |
| Key poses | 10 | 14 + companion poses |
| Resolution | 1920x1080 | 1920x1080 |
| Export format | WebM/GIF (loop) | MP4 (H.264) |
| Color | Graphite gray + pixel sprite color | Same + zone-specific palettes |
| Aspect ratio | 16:9 | 16:9 |

---

## Festival Submission Notes

The extended version (Act 2) is eligible for:
- AI film festivals (the human-AI collaboration narrative is the whole point)
- Animation festivals (pencil test format demonstrates traditional knowledge)
- Short film festivals (under 30 seconds, narrative arc complete)

The meta-narrative — an animator animating himself creating his own portfolio, with an AI companion appearing to help — is inherently about the state of creative technology in 2026. That's a festival-ready concept.
