# Style Profiles and Verification Tests

Read this when adapting animation to a specific historical style or when verifying style compliance.

## Style Profile Registry

### Rubber Hose (1920s)

- **Physics**: No rigid joints. Limbs are flexible tubes (curve deform). Constant bounce synced to musical beat. No holds.
- **FPS**: Sync to audio BPM
- **Interpolation**: Linear (constant speed)
- **Idle state**: ALWAYS_BOUNCE (no static poses)
- **Smear type**: Speed lines only (no blur)
- **Squash/stretch**: High (rubber), no volume lock
- **Line of action**: Curved (hose shape)

**Verification tests**:
- Joint_Angle_Sharpness must be ~0 (smooth curves, not angles)
- Idle_Velocity > 0 always (character never perfectly still)
- Bounce_Frequency matches Audio_BPM
- Z_Axis_Translation ~0 (flat plane only)
- **Drift signal**: Stiff motion, sharp elbows/knees, static poses

### Golden Age (Disney 1930s)

- **Physics**: Volumetric realism. Squash and stretch with volume locked. Cubic easing.
- **FPS**: 24 (Ones) or 12 (Twos). Never 8 (Threes).
- **Interpolation**: Cubic bezier (ease in/out)
- **Idle state**: Moving hold (subtle drift)
- **Smear type**: Drybrush/texture alpha
- **Squash/stretch**: Moderate, volume must be conserved (Scale_X * Scale_Y * Scale_Z ~ 1.0, tolerance 5%)
- **Line of action**: S-curve (flow)

**Verification tests**:
- Volume: Scale_X * Scale_Y * Scale_Z ~ 1.0 at all frames (5% tolerance)
- Framerate: 24fps or 12fps only (no 8fps)
- Arc compliance: End effector path fits bezier curve (no linear paths)
- Cushioning: Non-linear spacing at start/stops
- No twinning: L_Rot != R_Rot (asymmetry enforced)
- Follow-through: Child_Joint_Delay > 0 frames
- **Drift signal**: Floaty motion (linear spacing), shrinking volume, twinning

### Screwball (1940s Tex Avery)

- **Physics**: Extreme exaggeration. Staccato timing (fast move -> hard stop). Zips and violent distortions.
- **FPS**: 24 (Ones) for fast bits
- **Interpolation**: Zip (1-frame transit)
- **Idle state**: Dead stop (hard hold)
- **Smear type**: Elongated mesh (stretch)
- **Squash/stretch**: Extreme (volume can break)

**Verification tests**:
- Transition_Duration for zips must be 1 frame exactly
- Overshoot_Amount > 150% of target
- Anticipation present before every zip
- **Drift signal**: Smooth transitions, gentle easing (too gentle for screwball)

### Modernist/UPA (1950s)

- **Physics**: Planar movement (X/Y only). Asymmetry. Rejects perspective.
- **FPS**: Variable (Ones, Twos, Threes mixed)
- **Interpolation**: Variable, often stepped
- **Smear type**: Abstract shapes
- **Design**: Flat/graphic. Subjective backgrounds reflect mood.

**Verification tests**:
- Z_Translation == 0 (no depth movement)
- Perspective_Change == 0 (flat plane)
- Design is flat shapes, not volumetric
- **Drift signal**: 3D perspective, realistic volume, smooth motion

### Limited TV (Hanna-Barbera 1960s)

- **Physics**: Planned animation. Sound drives visuals. 80% static.
- **FPS**: 12 (Twos) or 8 (Threes)
- **Interpolation**: Step (hold then pop)
- **Idle state**: Static (frozen body, active mouth only)
- **Smear type**: Abstract blur (symbolic)
- **Squash/stretch**: Low (muzzle/mouth only)

**Verification tests**:
- Active_Pixel_Count < 20% of screen area per frame
- Body layer variance == 0 while Mouth layer variance > 0
- Average Pose_Hold > 12 frames (0.5s)
- Unique_Frame_Count / Total_Frames ratio is low (indicates loops)
- Viseme count limited to 7-9 mouth shapes
- Collar/necktie masking between head and body layers
- **Drift signal**: Full animation. Body moves every frame. Fluid inbetweens.

### Anime Traditional

- **Physics**: Dynamic modulation. Switch between framerates based on intensity.
- **FPS**: Variable (Ones for action, Twos/Threes for dialogue)
- **Smear type**: Speed lines (background), not character deformation
- **Special**: "Tome" holds (3-frame impact freeze on negative color)

**Verification tests**:
- Framerate modulates between segments (not constant)
- Speed lines on background layer, not crossing character face
- Impact frames use inverted/high-contrast color
- **Drift signal**: Constant framerate throughout, western-style motion blur

### Spider-Verse Hybrid

- **Physics**: Stepped 3D. Animates on Twos (12fps) to mimic hand-drawn. Motion blur disabled.
- **FPS**: 12 (Twos) forced
- **Interpolation**: Stepped (no splines)
- **Smear type**: CMYK offset (color channel separation)
- **Squash/stretch**: Low (rigid)

**Verification tests**:
- Framerate is 12fps throughout (forced Twos)
- Interpolation is STEPPED, not splined (no smooth curves)
- Motion blur is DISABLED
- Smear uses CMYK offset, not Gaussian blur
- **Drift signal**: Smooth spline interpolation, motion blur enabled

### Genndy 3D (Modern)

- **Physics**: Broken rig 3D. Push 3D models to 2D limits (non-physical deformation).
- **FPS**: 24 (Ones)
- **Interpolation**: Snappy (sharp curves with aggressive ease)
- **Smear type**: Geometry blend (sub-frame compositing, 70% bias to leading edge)
- **Squash/stretch**: Extreme (cartoony, joints can break)

**Verification tests**:
- Transitions are snappy (1-2 frame holds between moves)
- Joint constraints can be broken for extreme poses
- Blur uses geometry blend, not standard motion blur
- Leading edge opacity >= 70% in blurs
- **Drift signal**: Floaty motion, standard motion blur, physically accurate rigs

## Parameter Override Matrix

| Parameter | Rubber Hose | Golden Age | Screwball | Limited TV | Spider-Verse | Genndy 3D |
|-----------|-------------|------------|-----------|------------|--------------|------------|
| Rigidity | 0.0 | 1.0 | 0.5 | 1.0 | 1.0 | 0.0 |
| Idle state | Always bounce | Moving hold | Dead stop | Static | Stepped hold | Moving hold |
| Volume lock | No | Yes (5%) | No | N/A | Yes | No |
| Motion blur | No | Drybrush | Stretch | Abstract | CMYK offset | Geo blend |
| Min hold | 0 (never stop) | 6 frames | 0 (snap) | 12 frames | 6 frames | 3 frames |

## Mode Switch Decision Logic

```
IF style_keyword contains "1920s" or "rubber" or "bendy":
    SET style_profile = RUBBER_HOSE
ELIF style_keyword contains "disney" or "1930s" or "golden":
    SET style_profile = GOLDEN_AGE
ELIF style_keyword contains "tex avery" or "screwball" or "1940s":
    SET style_profile = SCREWBALL
ELIF style_keyword contains "upa" or "modernist" or "1950s" or "graphic":
    SET style_profile = MODERNIST_UPA
ELIF style_keyword contains "tv" or "hanna" or "limited" or "budget":
    SET style_profile = LIMITED_TV
ELIF style_keyword contains "anime" or "japanese":
    SET style_profile = ANIME_TRADITIONAL
ELIF style_keyword contains "spider" or "comic" or "verse":
    SET style_profile = SPIDER_VERSE
ELIF style_keyword contains "genndy" or "tartakovsky" or "primal":
    SET style_profile = GENNDY_3D
ELSE:
    SET style_profile = GOLDEN_AGE  # Default
```
