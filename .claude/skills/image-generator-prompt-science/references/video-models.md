# Video Generation Models (Veo, Kling, etc.)

## Key Principle: Less Detail = Better Motion

Video models interpolate motion between concepts. Unlike image models where specificity improves output, **video models produce better results with compressed, action-focused prompts** that describe WHAT happens without micromanaging HOW each body part moves.

Over-detailed prompts over-constrain the generation — the model tries to hit every specified movement and overcomplicates the result. Shorter prompts that lay out the action beats let the model fill in the blanks with more natural, fluid motion.

```
❌ OVER-CONSTRAINED (too much detail for video models):
"His head tilts ~15 degrees downward. Eyes drop to the stylus. After a brief pause 
of 2-3 frames, his head snaps back up quickly over 3-4 frames of fast motion. His 
eyebrows lift, eyes widen slightly by a fraction, and his half-smile broadens showing 
a hint of teeth. Subtle secondary motion: hair bounces slightly on the head snap."

✅ ACTION-FOCUSED (let the model interpolate):
"He glances down at his stylus, then snaps his head up with an idea — eyebrows 
lift, smile widens."
```

## Prompt Structure for Video Models

The 7-Layer framework compresses to 3 layers for video:

### 1. Medium + Style (one sentence)
What kind of visual are we looking at?
```
"Animate a hand-drawn pencil test character on cream animation paper."
```

### 2. Action Arc (the bulk of the prompt)
Describe the sequence of ACTIONS, not body mechanics. Use plain verbs.
```
"He raises his arm and sweeps the stylus in an arc. Pencil-sketch lines trail 
behind and transform into a small sprite character that bounces once and lands 
on his shoulder. He looks at it with a satisfied smirk and nods."
```

### 3. Style Guardrails + Negatives (one sentence)
What to preserve, what to prevent.
```
"Hand-drawn graphite pencil on cream paper style throughout. No camera movement, 
no style changes."
```

## Start Frame / End Frame Prompting

Models like Kling 3.0 that accept start and end frame images use a specific reference format:

### Kling Format
Kling expects `@Image1` (start) and `@Image2` (end) references woven into the prompt:

```
Take @Image1 as the start frame, Take @Image2 as the end frame. [Style sentence]. 
[Action arc describing what happens FROM @Image1's pose TO @Image2's pose]. 
[Style guardrails + negatives].
```

**Tip:** Reference @Image1 and @Image2 at moments in the action where the model should match the provided frame — e.g., "starting from the pose in @Image1" and "settling into the pose shown in @Image2."

### Veo Format
Veo 3.1 accepts start/end frames as image inputs alongside the prompt. The prompt itself doesn't need `@Image` references — just describe the action arc and let the model handle interpolation.

## What NOT To Include

| Skip this | Why |
|-----------|-----|
| Frame-by-frame body mechanics | Over-constrains interpolation |
| Specific degree measurements ("15-degree tilt") | Model can't parse precise angles in motion |
| Frame counts or timing ("over 3-4 frames") | Model controls its own timing |
| Secondary motion details ("hair bounces") | Model handles physics-based follow-through naturally |
| Animation jargon ("squash and stretch", "ease in") | Plain action verbs work better |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Stiff, unnatural motion | Prompt is too detailed — remove body mechanics, keep actions |
| Style drifts mid-video | Add style negatives: "No 3D rendering, no digital painting, no camera movement" |
| Character changes appearance | Add one consistency line: "Same character, same clothing throughout" |
| Action too complex/muddled | Reduce to fewer, clearer beats — max 3-4 actions |
| Model ignores start/end frames | Make sure prompt describes a path FROM start TO end, not an independent narrative |
