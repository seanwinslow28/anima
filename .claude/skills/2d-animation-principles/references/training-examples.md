# Training Examples

Curated instruction-output pairs demonstrating the Plan, Implement, Verify loop across all 6 modules. Read this for calibration when generating or evaluating animation sequences.

## Module 1: Physics Engine

### Gravity Drop (Heavy Object)

- **Instruction**: "Animate a bowling ball falling from a shelf to the floor."
- **PLAN**: `{"mode": "PHYSICS", "force": "gravity", "fps": 24, "object_mass": "heavy"}`
- **IMPLEMENT**: `{"keys": [1], "spacing_rule": "ODD_RULE (1:3:5:7)", "path": "vertical_linear", "squash_impact": "minimal"}`
- **VERIFY**: Is spacing non-linear? PASS. (Heavy objects: minimal squash on impact)

### Parabolic Jump

- **Instruction**: "Character jumps across a gap. Make the arc feel organic."
- **PLAN**: `{"mode": "ORGANIC", "arc_type": "parabola", "breakdown_placement": "fourth_down_half_time"}`
- **IMPLEMENT**: `{"keys": ["Start", "Apex", "Land"], "breakdown_pos": "Apex_Y - 25%", "breakdown_time": "50%"}`
- **VERIFY**: Is path linear? FAIL. Fix: Apply bezier curve to arc.

### Standard Walk Cycle

- **Instruction**: "Generate a standard bipedal walk cycle."
- **PLAN**: `{"state_machine": "WALK", "tempo": "12_frames_per_step", "cycle": "loop"}`
- **IMPLEMENT**: `{"beats": {"1": "Contact", "4": "Down", "7": "Pass", "10": "Up"}, "loop_point": 25}`
- **VERIFY**: Foot sliding? PASS. Fix: Lock foot x-translation on ground contact.

### Bouncing Ball (Decay)

- **Instruction**: "Rubber ball bounces and stops."
- **PLAN**: `{"physics": "energy_loss", "squash": "impact_only"}`
- **IMPLEMENT**: `{"height_decay": "60%_per_bounce", "timing_decay": "-2fr_per_bounce", "squash": "1_frame_contact"}`
- **VERIFY**: Sticky squash? FAIL. Fix: Limit squash to 1 frame at contact.

## Module 2: Fast-Motion Synthesis

### Super Punch

- **Instruction**: "Character punches forward instantly."
- **PLAN**: `{"action": "ballistic", "velocity": "high", "solution": "ELONGATED_SMEAR"}`
- **IMPLEMENT**: `{"frame_n": "Start", "frame_n+1": "Smear_Mesh(Stretch_Y)", "frame_n+2": "Impact"}`
- **VERIFY**: Smear duration >1? FAIL. Fix: Delete extra frame. Smears are strictly 1 frame.

### Spinning Wheels

- **Instruction**: "Car wheels spinning at high speed."
- **PLAN**: `{"action": "cyclic", "solution": "MULTIPLES", "spacing": "uneven"}`
- **IMPLEMENT**: `{"geometry": "Instance_3x", "visibility": "Leading_Edge_Only", "pattern": "non_ABA"}`
- **VERIFY**: Strobing/Blinking? PASS. (Uneven spacing prevents A-B-A flicker)

### Zip Exit

- **Instruction**: "Character zips off screen to the right."
- **PLAN**: `{"action": "exit", "solution": "MOTION_TUBE", "anticipation": "opposite_dir"}`
- **IMPLEMENT**: `{"seq": ["Antic(Left)", "Zip(Stretch_Right)", "Empty_Frame"], "blur": "geometry_stretch"}`
- **VERIFY**: Gap between A and B? FAIL. Fix: Elongate mesh to cover gap.

## Module 3: TV/Limited Optimization

### Dialogue Scene

- **Instruction**: "Character speaking a long sentence."
- **PLAN**: `{"budget": "TV", "technique": "CEL_STACKING", "ratio": "80/20"}`
- **IMPLEMENT**: `{"layer_1": "Static_Body", "layer_2": "Mouth_Loop", "visemes": "7_standard"}`
- **VERIFY**: Body moving? FAIL. Fix: Freeze body layer. Only mouth updates.

### Reaction Shot (Listening)

- **Instruction**: "Character listens to another person talking."
- **PLAN**: `{"action": "listen", "technique": "MOVING_HOLD", "alive": "true"}`
- **IMPLEMENT**: `{"pose": "static", "drift": "1%_variance", "blink_rate": "every_3s"}`
- **VERIFY**: Dead pixels (zero variance >12 frames)? FAIL. Fix: Add traceback drift.

### Crowd Scene

- **Instruction**: "A crowd of people cheering in background."
- **PLAN**: `{"budget": "low", "technique": "CYCLE_LOOPS", "framerate": "6fps (fours)"}`
- **IMPLEMENT**: `{"assets": ["Cheer_A", "Cheer_B"], "offset": "random_start_times"}`
- **VERIFY**: Unison movement? FAIL. Fix: Offset start frames to prevent synchronized loop.

## Module 4: Style Modes

### Rubber Hose Dance

- **Instruction**: "Character dances in 1920s style."
- **PLAN**: `{"style": "RUBBER_HOSE", "physics": "no_joints", "sync": "musical_beat"}`
- **IMPLEMENT**: `{"limbs": "curved_tubes", "idle": "bounce_loop", "holds": "false"}`
- **VERIFY**: Sharp elbows? FAIL. Fix: Replace joint angles with curve deformers.

### Spider-Verse Swing

- **Instruction**: "Spider-Man swings through city."
- **PLAN**: `{"style": "SPIDER_VERSE", "framerate": "modulated", "blur": "none"}`
- **IMPLEMENT**: `{"fps": "12 (Twos)", "fast_bits": "24 (Ones)", "smear": "CMYK_offset"}`
- **VERIFY**: Smooth spline interpolation? FAIL. Fix: Force stepped curves, no splining.

### Retro Game Idle

- **Instruction**: "16-bit character idle breathing."
- **PLAN**: `{"style": "PIXEL/RETRO", "cycle": "2_frame_bounce", "interp": "none"}`
- **IMPLEMENT**: `{"pose_A": "y=0", "pose_B": "y=-1px", "fps": "4 (6fps)"}`
- **VERIFY**: Sub-pixel movement? FAIL. Fix: Snap to pixel grid.

## Module 5: Acting Engine

### Surprise Take

- **Instruction**: "Character is shocked by a loud noise."
- **PLAN**: `{"emotion": "SURPRISE", "pattern": "Antic -> Take -> Settle", "eyes": "lead"}`
- **IMPLEMENT**: `{"squash": "down (2fr)", "stretch": "up (1fr)", "hold": "open_mouth (12fr)"}`
- **VERIFY**: Symmetric pose? FAIL. Fix: Offset arms by 2 frames.

### Sad Walk

- **Instruction**: "Character walks sadly."
- **PLAN**: `{"emotion": "SAD", "power_center": "hips", "line_of_action": "C_curve_down"}`
- **IMPLEMENT**: `{"speed": "slow (32fr cycle)", "head": "droop", "arms": "minimal_swing"}`
- **VERIFY**: Chest leading? FAIL. Fix: Lead with hips (weight sinks, not lifts).

### Double Take

- **Instruction**: "Character looks, looks away, then looks back fast."
- **PLAN**: `{"pattern": "LOOK_AWAY_LOOK", "timing": "contrast"}`
- **IMPLEMENT**: `{"look_1": "12fr", "away": "4fr", "look_2": "zip (2fr) + settle"}`
- **VERIFY**: Even timing across all three beats? FAIL. Fix: Sharpen contrast (fast second look).

## Module 6: Pipeline Architecture

### X-Sheet Generation

- **Instruction**: "Create exposure sheet for 'Hello World' audio."
- **PLAN**: `{"task": "X_SHEET", "input": "audio_wav", "framerate": "24"}`
- **IMPLEMENT**: `{"phonemes": ["H", "E", "L", "O", "W", "R", "L", "D"], "frames": [2-9]}`
- **VERIFY**: Closed mouth on silence? PASS. Visual accents lead audio by 2 frames.

### Twinning Check (Automated QA)

- **Instruction**: "Run QA on blocking pass."
- **PLAN**: `{"task": "QA_GATE", "filter": "TWINNING"}`
- **IMPLEMENT**: `{"scan_curves": "L_Hand vs R_Hand", "threshold": "Identical keys"}`
- **VERIFY**: Symmetry found? FAIL. Fix: Offset R_Hand by +2 frames.

### Silhouette Check

- **Instruction**: "Verify readability of key poses."
- **PLAN**: `{"task": "QA_STAGING", "method": "BINARY_MASK"}`
- **IMPLEMENT**: `{"render": "Black_White", "measure": "negative_space"}`
- **VERIFY**: Limbs occluded >30%? FAIL. Fix: Move arms to create negative space windows.
