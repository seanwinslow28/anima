# 16BitFit Dual-Aesthetic Style Reference

16BitFit uses two distinct visual languages that create a dramatic contrast when transitioning between modes.

---

## DMG Mode (4-Color Game Boy Aesthetic)

### Sacred Palette
| Role | Hex | Usage |
|------|-----|-------|
| Lightest | `#9BBC0F` | Backgrounds, inverse text |
| Light | `#8BAC0F` | Highlights, buttons, CTAs |
| Dark | `#306230` | Borders, secondary text, shadows |
| Darkest | `#0F380F` | Primary text, outlines, deep shadows |

### DMG Mode Style Cluster
```
(Game Boy DMG monochrome aesthetic using strict 4-color palette: 
#9BBC0F lightest, #8BAC0F light, #306230 dark, #0F380F darkest. 
Flat colors with optional dithering for texture transitions. 
No gradients, no anti-aliasing, no blur effects, crisp pixel edges)
```

### DMG Mode Rules
- **Palette:** ONLY these 4 colors, no exceptions
- **Shading:** Flat colors + dithering patterns only
- **Edges:** Crisp, no anti-aliasing
- **Effects:** No gradients, no blur, no glow
- **Animation:** 12-24 FPS for retro feel
- **Orientation:** Portrait (9:16)

### DMG Mode Assets
- User Avatars (5 archetypes × 5 evolution stages)
- Home Screen UI (buttons, progress bars, meters)
- Onboarding UI (welcome, archetype cards, profile setup)
- Workout UI (timer, rep counter, exercise display)
- Settings/Profile (menus, toggles, icons)

### DMG Mode Prompt Template
```
Create a [ASSET TYPE] for a Game Boy DMG-style fitness app interface.
Use ONLY the 4-color DMG palette: #9BBC0F (lightest/background), 
#8BAC0F (light/highlights), #306230 (dark/borders), #0F380F (darkest/text).
[SPECIFIC ASSET DESCRIPTION]. Portrait orientation. Flat pixel art with 
optional dithering for shading transitions. Crisp pixel edges.
No gradients. No anti-aliasing. No blur. No colors outside the 4-color palette.
```

---

## Battle Mode (Full-Color Arcade Fighter Aesthetic)

### Style References
- Street Fighter II
- Capcom arcade fighters (CPS-2 era)
- SNK Neo Geo titles

### Battle Mode Style Cluster
```
(Street Fighter II arcade aesthetic with bold #272929 dark outlines (2-3px), 
3-4 tone cel shading showing form and bone structure, top-front lighting, 
16-bit pixel rendering, full-color palette, dynamic poses)
```

### Champion Sprite Specifications
| Attribute | Value |
|-----------|-------|
| Canvas Size | 128×128 pixels |
| Character Height | ~100-110 pixels |
| Outline Color | #272929 (bold, 2-3px) |
| Shading | 3-4 tones per color area |
| Light Source | Upper-front |
| Background | Transparent or white |

### Boss Sprite Specifications
| Attribute | Value |
|-----------|-------|
| Canvas Size | 256×256 pixels |
| Outline Color | #272929 (bold) |
| Shading | 3-4 tones, unique palettes per boss |
| Style | Larger, more menacing presence |

### Battle Mode Rules
- **Palette:** Full-color, character-specific palettes
- **Outlines:** Bold #272929 dark outlines (2-3px)
- **Shading:** 3-4 tone cel shading per color region
- **Lighting:** Consistent top-front lighting
- **Orientation:** Landscape (16:9)
- **Renderer:** Phaser 3 (game engine sprites)

### Battle Mode Assets
- Champion Sprites (6 characters × 15 animation states)
- Champion Select Portraits (64×64 headshots)
- Boss Sprites (6 bosses × 9 animation states)
- Battle UI (health bars, timer, combo counter, "READY!", "FIGHT!", "K.O.!")
- Battle Backgrounds (parallax layers: Far, Mid, Near, Floor)

### Battle Mode Prompt Template
```
Create a [ASSET TYPE] for a Street Fighter II-style fighting game.
Full-color 16-bit pixel art with bold #272929 dark outlines (2-3px).
[SPECIFIC ASSET DESCRIPTION]. Use 3-4 tone cel shading per color area
with top-front lighting. [DIMENSIONS]. Dynamic [POSE/STATE].
Transparent background. Crisp pixel edges with defined outlines.
No anti-aliasing on sprite edges.
```

---

## Champion Color Palettes

| Champion | Skin | Hair | Eyes | Primary | Secondary |
|----------|------|------|------|---------|-----------|
| Sean (MMA) | #F5D6C6 | #C2A769 | #4682B4 | #F2F0EF tank | #2323FF pants |
| Mary (Kickboxing) | #F5D6C6 | #6D4C41 | #654321 | #FF7BAC top | #7E57C2 shorts |
| Marcus (Boxing) | #8D5524 | #212121 | #4A4A4A | #545454 tank | #FFD700 gloves |
| Aria (Capoeira) | #C68642 | #4B3621 | #06402B | #9A2257 top | #5577AA pants |
| Kenji (Aikido) | #FFDBAC | #212121 | #4A4A4A | #B0BEC5 top | #424242 pants |
| Zara (Powerlifter) | #CBB59D | #3B2F2F | #654321 | #545454 tank | #212121 pants |

---

## Boss Color Palettes

| Boss | Theme | Key Colors |
|------|-------|------------|
| Training Dummy | Tutorial | Wood #8B5A2B, Padding #A9A9A9, Joints #696969 |
| Procrastination Phantom | Ghostly | Mist #B3E5FC, Gi #ECEFF1, Aura #80DEEA |
| Sloth Demon | Lethargy | Fur #8D6E63, Eyes #FFCC80, Armor #90A4AE |
| Gym Bully | Intimidation | Tank #545454, Sunglasses #C0C0C0 |
| Stress Titan | Overstrain | Armor #263238, Conduits #FFC107, Eyes #FF5722 |
| Ultimate Slump | Burnout | Body #8D6E63, Clothes #545454 |

---

## Transition Video Context

The **Battle Mode Transition** is the dramatic moment where DMG Mode "explodes" into full-color:
1. DMG screen showing avatar in 4-color palette
2. Screen pixelates/shatters from center
3. Colorful pixels burst revealing arcade fighters
4. Full-color Battle Mode UI with "READY!" text

This is a **key brand moment** — the visual payoff for completing a workout.

---

## Post-Processing Requirements

### DMG Mode
- **Mandatory:** Server-side color quantization to enforce strict 4-color palette
- AI models tend to "color bleed" even when instructed — quantization is non-negotiable

### Battle Mode
- **Recommended:** Edge cleanup for consistent outline weights
- **Optional:** Palette verification against character color specs
