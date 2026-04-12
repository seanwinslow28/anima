# Timing, Spacing, and Physics Primitives

Read this when implementing animation physics, calculating frame positions, or configuring the AnimationClipSpec.

## AnimationClipSpec Schema

The master configuration object for any animation sequence:

```json
{
  "fps": 24,
  "duration_frames": 48,
  "style_profile_id": "golden_age",
  "constraints": {
    "exposure_rate": 2,
    "min_hold_frames": 6,
    "layer_separation": false,
    "static_ratio_target": null
  },
  "character_rig_assumptions": {
    "kinetic_chain_order": ["Hips", "Torso", "Shoulder", "Elbow", "Wrist"],
    "power_center_node": "Chest",
    "layer_separation": false
  },
  "shot_context": {
    "camera_move_velocity": 0,
    "framing": "medium"
  },
  "action_beats": [
    {
      "frame_index": 1,
      "pose_type": "anticipation",
      "duration_frames": 4,
      "vector": "OPPOSITE_TO_TARGET"
    },
    {
      "frame_index": 5,
      "pose_type": "key",
      "duration_frames": 2,
      "smear_flag": true
    },
    {
      "frame_index": 7,
      "pose_type": "overshoot",
      "duration_frames": 3
    },
    {
      "frame_index": 10,
      "pose_type": "moving_hold",
      "duration_frames": 12
    }
  ]
}
```

Key fields:
- `exposure_rate`: 1 = Ones (24fps), 2 = Twos (12fps), 3 = Threes (8fps)
- `power_center_node`: Origin of force. "Chest" for heroes, "Hips" for heavy characters
- `camera_move_velocity`: If >0, force exposure to Ones to prevent background strobing

## Timing Beat Defaults (at 24fps)

| Action Type | Frame Range | Spacing | Use Case |
|-------------|-------------|---------|----------|
| Fast reaction | 2-4 frames | Sharp ease-out | Surprise, impact, shock |
| Normal gesture | 8-12 frames | Cubic ease in/out | Conversation, pointing |
| Heavy effort | 16-24 frames | Extreme ease in/out | Lifting, pushing, fatigue |
| Golden key hold | 6-12 frames | Moving hold (1-2% drift) | Readable attitude pose |
| Readability floor | 3 frames min | N/A | Anything shorter is invisible |

## Easing Primitives

### Ease Curves

| Curve Type | Use Case | Bezier Control Points |
|------------|----------|----------------------|
| Linear | Mechanical motion only (never organic) | [0, 0, 1, 1] |
| Step | Spider-Verse, limited TV, popping | N/A (hold then jump) |
| Cubic bezier (standard) | Most organic motion | [0.4, 0.0, 0.2, 1.0] |
| Gravity (Odd Rule) | Falling objects from rest | Derived from 1:3:5:7 |

### Breakdown Placement Strategies

- **Halves**: Breakdown at geometric center (mechanical)
- **Thirds**: Favor one end for slow-in or slow-out
- **Favors**: "Fourth Down at Half Time" — at 50% time, position is 25% from apex

## Physics Pseudocode

### Gravity Spacing (Odd Rule)

```python
def apply_gravity_spacing(start_pos, frames, unit_dist):
    """Displacement increases by odd numbers: 1, 3, 5, 7..."""
    positions = [start_pos]
    current_y = start_pos
    for t in range(1, frames + 1):
        odd_multiplier = (2 * t) - 1
        displacement = unit_dist * odd_multiplier
        current_y -= displacement
        positions.append(current_y)
    return positions
```

### Anticipation, Action, Settle

```python
def generate_anticipation_beat(start, target, intensity):
    move_vector = target.position - start.position
    # Antic moves OPPOSITE to main action
    antic_pos = start.position - (normalize(move_vector) * intensity * 0.2)

    # Duration heuristic: slower antic, fast action
    antic_time = start.time + 4  # Standard prep (4-8 frames)
    action_time = antic_time + 2  # Fast transit

    return [
        Keyframe(antic_pos, antic_time),      # Anticipation
        Keyframe(target.position, action_time), # Action
    ]
```

### Overshoot and Settle

```python
def apply_overshoot(target, velocity, stiffness):
    overshoot_mag = velocity * (1.0 - stiffness)
    peak_val = target + overshoot_mag

    if stiffness > 0.5:  # Hard accent
        return [Frame(peak_val, t+1), Frame(target, t+3)]
    else:  # Soft accent
        return [Frame(peak_val, t+2), Frame(target, t+6)]
```

### Twinning Detection

```python
def detect_twinning(left_limb_curve, right_limb_curve, timeline):
    for t in timeline:
        if abs(left_limb_curve[t] - right_limb_curve[t]) < 0.05:
            return "FAIL: Twinning detected. Offset right limb by 2 frames."
    return "PASS"
```

### Volume Conservation (Squash/Stretch)

```python
def check_volume(scale_x, scale_y):
    """Volume = Scale_X * Scale_Y should approximate 1.0"""
    volume = scale_x * scale_y
    if abs(volume - 1.0) > 0.1:
        return "FAIL: Volume not conserved"
    return "PASS"

def fix_squash(scale_parallel):
    """Calculate perpendicular scale to conserve volume"""
    return 1.0 / math.sqrt(scale_parallel)
```

## Follow-Through Offset Table

| Joint Pair | Frame Offset | Notes |
|------------|-------------|-------|
| Shoulder -> Elbow | 1-2 frames | Standard kinetic chain |
| Elbow -> Wrist | 1-2 frames | Cumulative with shoulder |
| Wrist -> Fingers | 1-2 frames | Cumulative |
| Head -> Hair tips | 3-5 frames | Soft body, more drag |
| Torso -> Cape/Tail | 4-8 frames | Fluid dynamics, use Straight-Ahead |
| Eyes -> Head turn | -2 to -3 frames | Eyes LEAD (move first) |

## Hold Types

| Type | Variance | Duration | Use Case |
|------|----------|----------|----------|
| Dead hold | 0% | Any | Mechanical objects, freeze frames |
| Moving hold | 1-2% drift | 12+ frames | Living characters in "static" pose |
| Traceback | Loop back toward previous pose | 8-16 frames | Subtle breathing, weight shift |
| Golden key | Moving hold | 6-12 frames | Main attitude pose (must read clearly) |
