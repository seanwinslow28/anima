# Pencil Test Timing Map

Read this reference when evaluating timing between keyframes or planning in-between generation strategy for the Pencil Test pipeline.

## Act 1 Transition Analysis

| Transition | Hold | Type | Principle | In-Between Strategy |
|-----------|------|------|-----------|-------------------|
| F01→F06 | 5 frames (0.42s) | Moving hold → action | Eye lead: eyes drop to stylus before head tilts | Subtle drift on hold, then head tilt. 1-2 in-betweens. |
| F06→F10 | 4 frames (0.33s) | Held pose → snap | Fast reaction (2-4 frames). Pop > smooth. | Minimal in-betweens (0-1). Favor the snap. |
| F10→F13 | 3 frames (0.25s) | Anticipation | Acting beat step 2: move opposite before action | Weight shift, elbow leads arm lift. 1 in-between. |
| F13→F18 | 5 frames (0.42s) | Action (ballistic arc) | Drybrush smear, follow-through on wrist/fingers | 2-3 in-betweens with smear at midpoint. Ease out. |
| F18→F31 | 13 frames (1.08s) | Extended hold | Moving hold with composited sprite overlay | 1-2% drift on Sean. Sprite is active layer (80/20 rule). |
| F31→F36 | 5 frames (0.42s) | Acting (nod) | Overlap: head leads, body follows | 1-2 in-betweens. Chin drops first, shoulders lag. |
| F36→F40 | 4 frames (0.33s) | Settle | Return to neutral, ease out into loop | Gradual deceleration. Must match F01 pose exactly. |

## Timing Notes

- **Framerate:** 12fps on Twos (each drawing held for 2 frames at 24fps equivalent)
- **Total duration:** 42 frames = 3.5 seconds per loop
- **Longest hold:** F18 at 13 frames — needs moving hold treatment to avoid "dead" look
- **Shortest hold:** F10 at 3 frames — at the readability floor, works because it's a reaction snap
- **Loop point:** F40 must be identical to F01 (both use A-2 anchor)

## Acting Beat Mapping

The Act 1 hero loop follows the Acting Beat Pattern:

| Beat | Frames | Acting Step | Duration |
|------|--------|-------------|----------|
| Idle | F01-F05 | Settle (from previous loop) | 5 frames |
| Thought | F06-F09 | Eyes on stylus, processing | 4 frames |
| Spark | F10-F12 | Thought → Anticipation transition | 3 frames |
| Anticipation | F13-F17 | Wind-up, body prepares | 5 frames |
| Action | F18-F30 | The gesture + sprite creation | 13 frames |
| Overshoot/Settle | F31-F39 | Sprite lands, nod, return | 9 frames |
| Loop restart | F40-F42 | Return to idle (matches F01) | 3 frames |

## In-Between Budget

Estimated in-between frames needed per transition (Phase 2):

| Transition | In-Betweens | Method | Priority |
|-----------|------------|--------|----------|
| F01→F06 | 2 | Video model (subtle head tilt) | Medium |
| F06→F10 | 0-1 | Manual or skip (snap effect) | Low |
| F10→F13 | 1 | ComfyUI OpenPose (arm position change) | Medium |
| F13→F18 | 2-3 | ComfyUI OpenPose (large motion, smear) | High |
| F18→F31 | 0 (hold) | Moving hold drift only | Low |
| F31→F36 | 1-2 | Video model (subtle nod) | Medium |
| F36→F40 | 1 | Video model (settle to idle) | Medium |

**Total estimated in-betweens:** 7-12 frames
**Total with in-betweens:** ~50-54 frames (up from 42 keyframe holds)
