# Smear and Multiples Taxonomy

Complete taxonomy of fast-motion synthesis techniques. Read this when choosing a smear type for high-velocity motion (displacement > object width).

## Decision Logic

```
IF displacement > object_width:
    IF action is ballistic (punch, zip, throw):
        USE Elongated Inbetween
    ELIF action is cyclic (wheels, running legs):
        USE Multiples (Ghosting)
    ELIF action is rotation (head whip, spin):
        USE Mini-Smear
    ELIF action is impact (wall slam, landing):
        USE Compression Smear
    ELIF style is Spider-Verse/Comic:
        USE CMYK Offset
    ELIF style is Vintage/Hand-drawn:
        USE Drybrush Smear
    ELIF render is 3D:
        USE Genndy Blur
    ELSE:
        USE Elongated Inbetween (default)
```

All smears last exactly 1 frame. If a smear is held longer, it looks like a mutation.

## Core Smear Types

### Elongated Inbetween (Stretch Mesh)

- **Communicates**: High-velocity transit between two distinct poses
- **Use when**: Action is linear or ballistic (punch, zip, throw)
- **Trigger**: `IF Velocity > Width AND Path == Linear THEN Stretch_Mesh`
- **Parameters**: Duration 1 frame. Stretch along motion axis, compress perpendicular (volume locked)
- **Failure mode**: Held >1 frame (looks mutant). Fix: delete extra frames

### Multiples (Ghosting)

- **Communicates**: Repetitive, cyclic motion or vibration
- **Use when**: Action is cyclic (running legs, spinning wheels, vibrating)
- **Trigger**: `IF Action == Cyclic THEN Instance_Geometry at previous t`
- **Parameters**: 2-6 instances, spacing must be uneven/progressive
- **Failure mode**: Evenly spaced instances cause A-B-A blinking. Fix: randomize spacing
- **Guardrail**: Show only the leading edge outline (approaching side)

### Multiple Limbs

- **Communicates**: Frantic, high-energy activity in localized area
- **Use when**: Character stationary but limbs move fast (fight cloud, scrambling)
- **Trigger**: `IF Limb_Velocity > Threshold AND Root_Velocity ~ 0 THEN Duplicate_Limbs`
- **Parameters**: 3-5 visible limbs per frame
- **Failure mode**: Torso moves too much. Fix: keep power center (torso) static

### Mini-Smear

- **Communicates**: Subtle emphasis on small, fast movement
- **Use when**: Shorter distances, internal features (eyes/mouth) moving fast
- **Trigger**: `IF Displacement < Max_Stretch BUT > Rigid_Limit THEN Deform_Local`
- **Parameters**: Stretch factor 1.1x-1.2x, distort features in motion direction
- **Failure mode**: Used on long distances (looks like glitch). Use elongated mesh instead

### Zip (Zip Turn)

- **Communicates**: Instantaneous exit or entrance
- **Use when**: Character leaves/enters screen in <3 frames
- **Trigger**: `IF Transit_Time < 3 frames THEN Connect Pos_A to Pos_B`
- **Parameters**: 1 Anticipation + 1 Zip + 1 Settle
- **Failure mode**: No anticipation or settle provided. Always include prep and landing

### Smear Take

- **Communicates**: Sudden, violent reaction (shock/surprise)
- **Use when**: Character realizes something abruptly, comedy
- **Trigger**: `IF Emotion == Shock THEN Scale_Head > 2.0 for 1 frame`
- **Parameters**: 1 frame stretch, then settle
- **Failure mode**: Deformation held too long or lacks recoil

## Style-Specific Smears

### Drybrush Smear

- **Communicates**: Atmospheric speed with texture/drag
- **Use when**: Vintage/hand-drawn style, soft edge loose drawings
- **Trigger**: `IF Style == Vintage THEN Apply Alpha_Texture (Scratchy)`
- **Parameters**: Non-linear opacity decay, thick/thin line orchestration
- **Failure mode**: Used on hard-edged/vector styles (looks incongruous)

### Abstract Smear (Graphic)

- **Communicates**: Pure direction/energy, surreal speed
- **Use when**: Action too fast for detail, modern/graphic style
- **Trigger**: `IF Velocity == Extreme THEN Replace Mesh with Solid_Shape`
- **Parameters**: Detail level 0, duration 1 frame, simple color masses
- **Failure mode**: Shape doesn't match character palette/mass

### CMYK Offset (Misprint)

- **Communicates**: Speed/vibration without blur (comic book aesthetic)
- **Use when**: Spider-Verse or comic book style
- **Trigger**: `IF Style == Comic THEN Offset_Color_Channels (C/M/Y)`
- **Parameters**: Offset proportional to velocity vector, hard edges
- **Failure mode**: Standard Gaussian blur applied (ruins the style). Disable motion blur

### Genndy Blur (3D)

- **Communicates**: Tempering standard motion blur with 2D clarity
- **Use when**: 3D animation requiring 2D snappiness
- **Trigger**: `IF Render == 3D THEN Blend Sub_Frames into Current_Frame`
- **Parameters**: 70%+ opacity bias on leading edge to maintain silhouette
- **Failure mode**: Standard motion blur makes pose muddy/transparent

### Speed Lines (2D)

- **Communicates**: Directionality without deforming character
- **Use when**: Anime/action style, character remains on-model
- **Trigger**: `IF Style == Anime THEN Add Line_Particles along vector`
- **Parameters**: High density, variable thickness
- **Failure mode**: Lines cross the face/focal point. Draw on background, not over face

## Specialized Types

### Motion Tube

- **Use when**: Very fast linear moves (Superman flying)
- **Trigger**: `IF Speed == High THEN Deform_Hull to Cylinder`
- **Shape**: Elliptical elongation maintaining volume

### Smear Trail (Geometric)

- **Use when**: Trajectory is narratively important (arrow flight, sword swing)
- **Trigger**: `IF Object_Type == Projectile THEN Extrude_Trailing_Edge`
- **Parameters**: Opacity 100% to 0% over 2-4 frames, jagged/triangular shapes

### Vibrating Multiple

- **Use when**: Character static but shaking (hit by bell, terror)
- **Trigger**: `IF Action == Shaking THEN Instance_Geometry (Offset +/-)`
- **Parameters**: Small offset (<5px), show both leading and trailing outlines
- **Failure mode**: Only one edge shown (looks like drift, not vibration)

### Rolling Shutter (Wide)

- **Use when**: Horizontal dash/entry, character enters laterally extremely fast
- **Trigger**: `IF Entry_Vector == Horizontal THEN Scale_X > 3.0`
- **Parameters**: Duration 1 frame, stretch width significantly more than height

### Dissolve Smear

- **Use when**: Softening harsh 2-frame run cycle flicker
- **Trigger**: `IF Cycle == 2-Drawing THEN Cross_Dissolve 50%`
- **Failure mode**: Looks ghostly. Only use for 2-frame cycles

### Flurry Effect

- **Use when**: Sustained high-intensity conflict (fight clouds)
- **Trigger**: `IF State == Fighting THEN Loop Multiple_Limbs + Dust_FX`
- **Parameters**: Loop length 3-5 distinct frames, mix limbs with impact FX

### Coloring Outside Lines

- **Use when**: Trigger/anime high-intensity moments, raw energy
- **Trigger**: `IF Style == Trigger THEN Expand_Fill_Mask > Line_Mask`
- **Parameters**: High roughness, paint fill extends beyond lineart jaggedly

## Pseudocode: Smear Trigger Logic

```python
def check_for_smear(pose_a, pose_b, object_width):
    displacement = distance(pose_a, pose_b)
    if displacement > object_width:
        if is_linear(pose_a, pose_b):
            return {"type": "ELONGATED_MESH", "duration": 1}
        elif is_cyclic(action):
            return {"type": "MULTIPLES", "count": 3, "spacing": "uneven"}
        else:
            return {"type": "ELONGATED_MESH", "duration": 1}
    return {"generate_smear": False}
```
