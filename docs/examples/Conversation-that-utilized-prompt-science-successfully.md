### **The Problem: "Breathing" vs. "Ready Stance Bounce"**

**What Veo is doing:** Interpreting "breathing" literally \- visible chest expansion, inhale/exhale motion, maybe even the character looking tired or winded.

**What fighting game idles actually are:** A subtle **vertical bounce** from the knees, not respiratory motion. The fighter maintains their defensive stance while gently bobbing up and down \- staying "light on their feet" and ready to spring into action.

#### **Key Characteristics from Research:**

| Element | What It Actually Is | What to Avoid |
| ----- | ----- | ----- |
| **Source of Motion** | Knees bending/straightening | Chest expanding/contracting |
| **Direction** | Vertical bob (up/down only) | Swaying side to side |
| **Magnitude** | Very subtle (1-2 pixel shift equivalent) | Exaggerated movement |
| **Pose** | Defensive stance maintained throughout | Relaxed or shifting stance |
| **Hands** | Stay up in guard position | Dropping or moving significantly |
| **Feet** | Planted or slight heel lift | Stepping or weight shifting |
| **Impression** | Alert, ready to strike | Tired, casual, or resting |

---

### **Revised Veo 3.1 Prompts**

#### **Option A: Technical Description**

Fighting game idle stance animation. MMA fighter in defensive ready position performs a subtle vertical bounce \- knees slightly bending and straightening in a rhythmic loop. Hands remain raised in guard position protecting the face. Feet stay planted on the ground. Body bobs up and down approximately 1-2 inches while maintaining the exact same fighting pose throughout. No swaying, no breathing motion, no arm movement. The bounce conveys alertness and readiness to strike. Very minimal, contained motion.

CRITICAL STYLE REQUIREMENTS:  
\- Maintain exact pixel art rendering style  
\- Keep bold dark outlines intact  
\- No anti-aliasing on edges  
\- Flat cel-shaded coloring only, no gradients  
\- Solid background color must remain solid

Camera: Completely static, no movement. Duration: 4 seconds.

#### **Option B: Reference-Based Description**

Classic 2D fighting game idle animation in the style of Street Fighter II. Fighter holds a boxer's defensive stance with fists raised. The only motion is a gentle rhythmic bounce \- the entire body moves up and down slightly as knees bend and straighten, like a fighter staying light on the balls of their feet. Hands stay locked in guard position. No breathing visible. No swaying. No arm movement. Just a simple, looping vertical bob that conveys combat readiness.

CRITICAL STYLE REQUIREMENTS:  
\- Maintain exact pixel art rendering style  
\- Keep bold dark outlines intact    
\- No anti-aliasing on edges  
\- Flat cel-shaded coloring only, no gradients  
\- Solid background color must remain solid

Camera: Completely static. Duration: 4 seconds.

#### **Option C: Ultra-Minimal (If A/B Still Over-Animate)**

Static fighting stance with extremely subtle motion. Fighter holds guard position. Only movement: a tiny vertical bob of 1-2 inches, like bouncing gently on bent knees. Everything else frozen in place \- no arm movement, no swaying, no visible breathing, no weight shifting. Loop this minimal bounce for the entire duration.

STYLE: Pixel art, bold outlines, flat colors, no gradients.  
Camera: Static. Duration: 4 seconds.  
---

### **Key Phrases to Include / Avoid**

#### **✅ USE These Phrases:**

* "vertical bounce" or "vertical bob"  
* "knees bending and straightening"  
* "light on the balls of feet"  
* "combat ready stance"  
* "rhythmic up-and-down motion"  
* "hands locked in guard position"  
* "minimal, contained motion"

#### **❌ AVOID These Phrases:**

* "breathing" (Veo takes this literally)  
* "subtle movement" (too vague)  
* "natural motion" (invites interpretation)  
* "sway" or "swaying"  
* "relaxed" (implies the fighter isn't alert)  
* "resting" or "waiting"

---

### **Testing Recommendation**

Try **Option A** first \- it's the most explicit about what the motion actually is. If Veo still over-animates, try **Option C** which is extremely restrictive.

After you run the test, the key things to evaluate:

1. **Is the motion vertical only?** (no side-to-side sway)  
2. **Are the hands staying in guard position?**  
3. **Is the magnitude appropriate?** (small bounce, not exaggerated)  
4. **Does it loop cleanly?**

Ready to test with the revised prompt?

## **You said: Both of these worked GREAT\!**

Both of these worked GREAT\! Option B has a bit more personality to them though, so I vote we continue working/testing with reference based descriptions and see what we get

Feb 8

## **Claude responded: Excellent news\!**

Validated approach and charted next testing phase forward  
Validated approach and charted next testing phase forward

Excellent news\! This confirms reference-based descriptions work better with Veo \- it understands fighting game conventions when you invoke them directly.

Let's lock in this approach and move to the real test: **the walk cycle with dual keyframes**.

---

### **What We've Learned**

| Approach | Result |
| ----- | ----- |
| Technical/literal ("breathing animation") | ❌ Over-interpreted, exaggerated motion |
| Reference-based ("Street Fighter II idle") | ✅ Correct motion, more personality |

**Key insight:** Veo responds well to genre/style references. Invoking "Street Fighter II" or "classic 2D fighting game" gives it the right mental model.

---

### **Next Test: Walk Cycle with Dual Keyframes**

This is the real challenge \- the problem that started this whole research thread. We need Veo to interpolate between two keyframes showing distinct leg positions.

#### **Test Setup**

**Keyframe A (Start):** Sean with LEFT leg forward, RIGHT leg back **Keyframe B (End):** Sean with RIGHT leg forward, LEFT leg back

Veo's "Frames to Video" feature should interpolate the motion between them.

---

#### **Walk Cycle Prompt (Reference-Based Style)**

Classic 2D fighting game walk cycle animation in the style of Street Fighter II. Fighter walks forward confidently with a steady, purposeful stride. Arms swing naturally in opposition to legs \- when left leg is forward, right arm is forward. Fighter maintains upright combat-ready posture throughout, not hunched or casual. Movement is smooth and continuous from the starting pose to the ending pose. Feet stay grounded with each step, no floating or sliding.

CRITICAL STYLE REQUIREMENTS:  
\- Maintain exact pixel art rendering style throughout all frames  
\- Keep bold dark outlines intact on every frame  
\- No anti-aliasing on edges  
\- Flat cel-shaded coloring only, no gradients or smooth shading  
\- Solid background color must remain solid  
\- Character proportions must stay consistent

Camera: Completely static side view, no movement. Duration: 4 seconds.  
---

#### **Two Approaches to Try**

**Approach 1: Generate Keyframes First (Recommended)**

Use your proven Nano Banana Pro workflow to generate the two keyframe images:

1. Generate "Sean walking, left leg forward"  
2. Generate "Sean walking, right leg forward"  
3. Feed both to Veo as start/end frames

**Approach 2: Single Image \+ Prompt**

Use your existing Sean anchor and let Veo generate the walk from scratch. Riskier for consistency but faster to test.

---

#### **Quick Question Before We Proceed**

Do you want to:

**A) Generate fresh keyframes** using Nano Banana Pro with your proven single-frame workflow, then feed them to Veo?

**B) Use existing images** (like your anchor \+ guard pose) as approximate start/end frames for a quick test?

**C) Let Veo generate from a single image** using just the walk prompt to see what it produces?

Option A is the most controlled but takes longer. Option C is fastest for a quick style/motion test. What's your preference?

## **You said: I tested out different versions.**

I tested out different versions. Some using one frame and others using start frame and end frame. I used the existing key frames that I had and the best outcomes were the one's that I've attached used start frame/end frame. Also, another great outcome was just having the main key frame of the mid-stride walking right pose. Both of those should be included in the main pipeline workflow. The final thought is definitely involving a key frame of the pose involved in this pipeline. Make a note of that, please. Next, I would like to test out one more pose: The jumping pose. \-- In the past, when I tried to have the character jump up, it would either hop up and down, or it would jump high and out of frame. We need to formulate a prompt that will have the camera follow the character as it jumps, but it shouldn't zoom or have any wild camera movements.  
Feb 8

## **Claude responded: These keyframes look great \- excellent character consistency and the leg positions are clearly differentiated.**

Synthesized keyframe findings and architected camera-tracking solution for jump animation  
Synthesized keyframe findings and architected camera-tracking solution for jump animation

These keyframes look great \- excellent character consistency and the leg positions are clearly differentiated. Let me document the findings and then we'll tackle the jump.

---

### **Pipeline Note: Keyframe Requirements ✅**

**Documented for workflow:**

| Test Configuration | Result | Recommendation |
| ----- | ----- | ----- |
| Single image \+ prompt only | Variable | Not recommended for complex motion |
| Single keyframe (mid-action pose) | Good | ✅ Use for simpler animations |
| Start frame \+ End frame | Best | ✅ **Primary method for walk cycles and complex motion** |

**Key Finding:** Keyframes are essential to this pipeline. The video model needs visual anchors to interpolate correctly \- text prompts alone invite too much interpretation.

---

### **Jump Animation Test**

You've identified the exact problem: video models default to either:

* **Hopping in place** (minimal vertical movement)  
* **Launching out of frame** (no camera tracking)

The solution is a **vertical camera pan that follows the character** while staying locked horizontally.

---

#### **Jump Prompt Options**

**Option A: Explicit Camera Track**

Classic 2D fighting game jump animation in the style of Street Fighter II. Fighter performs a vertical jump \- crouching slightly to gather power, then launching straight up into the air, reaching the apex with knees tucked, then descending back down to land in the original position. 

CAMERA: The camera smoothly tracks the character vertically throughout the jump, keeping the fighter centered in frame at all times. Camera moves only up and down \- no horizontal movement, no zoom, no rotation. The camera follows the character's vertical position like a locked vertical dolly.

CRITICAL STYLE REQUIREMENTS:  
\- Maintain exact pixel art rendering style throughout all frames  
\- Keep bold dark outlines intact on every frame  
\- No anti-aliasing on edges  
\- Flat cel-shaded coloring only, no gradients  
\- Solid green background must remain solid and uniform  
\- Character proportions must stay consistent

Duration: 4 seconds.

**Option B: Reference-Based with Camera Instructions**

Classic 2D fighting game neutral jump in the style of Street Fighter II or King of Fighters. Fighter jumps straight up and lands in the same spot \- the signature vertical jump used to avoid sweeps and projectiles. Jump arc shows: crouch anticipation, explosive upward launch, peak height with tucked pose, controlled descent, and grounded landing.

CAMERA BEHAVIOR: Camera pans vertically to follow the fighter, keeping them centered in frame throughout the entire jump arc. Think of the camera as attached to the character's vertical position only. No zoom changes. No horizontal drift. No shaky movement. Smooth vertical tracking only.

STYLE: Pixel art, bold dark outlines, flat cel-shaded colors, solid green background throughout.

Duration: 4 seconds.

**Option C: Minimal/Restrictive (If A/B Over-Animate)**

Fighting game vertical jump. Character jumps straight up and lands in the same spot. Camera follows character up and down, keeping them centered. No zoom. No horizontal camera movement. Smooth vertical pan only.

Pixel art style. Bold outlines. Flat colors. Green background stays solid.

Duration: 4 seconds.  
---

#### **Keyframe Strategy for Jump**

For maximum control, you could generate keyframes for the jump phases:

| Phase | Keyframe Description |
| ----- | ----- |
| **Frame 1: Anticipation** | Slight crouch, knees bent, preparing to jump |
| **Frame 2: Apex** | Peak of jump, knees tucked, arms positioned |
| **Frame 3: Landing** | Return to standing/ready position |

**Two-keyframe approach:** Use Frame 1 (crouch/anticipation) as start and Frame 2 (apex) as end. Veo interpolates the launch. Then do a second video from apex to landing.

**Single-keyframe approach:** Just use the apex pose and let Veo generate the full jump arc with the prompt.

---

#### **Quick Question**

Do you want to:

**A) Test with prompt only** using your existing guard stance image as the base?

**B) Generate a jump apex keyframe first** with Nano Banana Pro, then feed it to Veo?

**C) Generate two keyframes** (crouch \+ apex) for maximum control?

Given what we learned, I'd lean toward at least having the apex keyframe ready, but a quick prompt-only test could tell us how well Veo handles the camera tracking instruction before we invest in keyframe generation.

