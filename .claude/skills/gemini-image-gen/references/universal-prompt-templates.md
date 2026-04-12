# Universal Prompt Templates

> **When to read:** Use these templates when generating any image type. Each template follows the 7-Layer Prompt Framework from the `image-generator-prompt-science` skill, optimized for Nano Banana 2 (`gemini-3.1-flash-image-preview`). Copy the template, fill in the bracketed placeholders, and remove any layers that don't apply to your specific request.

---

## How to Use These Templates

1. Pick the template closest to your image type
2. Replace all `[BRACKETED]` placeholders with specifics
3. Remove layers that don't add value for your particular request (not every image needs all 7 layers)
4. Run the optimized prompt through `scripts/generate_image.py`

---

## Template 1: Photorealistic Portrait

```
[TASK DECLARATION]
Create a professional photorealistic portrait of [SUBJECT DESCRIPTION — age, gender, ethnicity, distinguishing features].

[CONTEXT FOUNDATION]
Setting: [ENVIRONMENT — studio, outdoor, office, etc.]. Background: [BACKGROUND TREATMENT — blurred bokeh, solid color, environmental]. This is for [PURPOSE — LinkedIn headshot, editorial feature, casting portfolio].

[STYLE DEFINITION]
Photographic style with ([CAMERA — 85mm portrait lens, f/2.0 aperture], [FILM STOCK OR DIGITAL LOOK — clean digital, Kodak Portra 400 warmth], [RENDERING — sharp focus on eyes, natural skin texture with visible pores]).

[COMPOSITIONAL LAYOUT]
[FRAMING — headshot / bust / three-quarter body] with subject positioned at [RULE OF THIRDS PLACEMENT — left third, center, right third]. [GAZE — looking directly at camera / slight off-camera gaze]. [POSE — relaxed shoulders, slight head tilt, hands visible/not visible].

[CONSISTENCY CONSTRAINTS]
Maintain natural proportions and realistic anatomy. Skin tones must be natural and even. If using a reference image: keep facial features exactly the same as the reference.

[TECHNICAL UNIFORMITY]
Lighting: [SETUP — Rembrandt lighting with soft fill / butterfly lighting / three-point setup / golden hour backlight]. Consistent color temperature throughout. Natural, controlled shadows that preserve facial detail without harsh edges.

[OUTPUT SPECS + NEGATIVES]
High-resolution, print-ready quality. Sharp focus on eyes and face.
No artificial smoothing. No plastic skin. No visible artifacts. No watermarks.
```

**Recommended aspect ratio:** `3:4` (portrait) or `4:5` (social media portrait)

---

## Template 2: Product Photography

```
[TASK DECLARATION]
Create a professional product photograph of [PRODUCT DESCRIPTION — material, color, size, brand aesthetic].

[CONTEXT FOUNDATION]
Surface: [SURFACE — white seamless backdrop, marble tabletop, rustic wood, lifestyle kitchen counter]. This is for [PURPOSE — e-commerce listing, luxury brand campaign, social media ad, packaging insert].

[STYLE DEFINITION]
Clean commercial photography with ([LENS — 50mm macro for small products / 35mm for lifestyle], [DEPTH OF FIELD — shallow for hero shots / deep for catalog], [FINISH — matte, glossy, textured]).

[COMPOSITIONAL LAYOUT]
[ANGLE — 45-degree hero angle / flat lay / eye-level / slight overhead]. Product centered with [NEGATIVE SPACE — generous white space on all sides / tight crop]. [PROPS — none / minimal lifestyle props: [list them]].

[CONSISTENCY CONSTRAINTS]
Product color and material must be accurate and consistent. Maintain realistic scale relative to any props. No color cast that shifts the product's true appearance.

[TECHNICAL UNIFORMITY]
Lighting: [SETUP — soft diffused overhead with fill card / rim light for edge definition / warm key light for lifestyle feel]. Shadows: [SHADOW STYLE — soft, natural / hard, dramatic / no shadow (floating)]. Consistent highlight behavior across all reflective surfaces.

[OUTPUT SPECS + NEGATIVES]
Crisp, high-detail output suitable for large-format display. Sharp product edges.
No motion blur. No lens flare. No dust or scratches unless intentionally aged.
```

**Recommended aspect ratio:** `1:1` (e-commerce) or `4:3` (catalog)

---

## Template 3: Landscape / Environment

```
[TASK DECLARATION]
Create a [MOOD — serene, dramatic, moody, vibrant] landscape photograph of [SCENE — mountain range at sunset, misty forest at dawn, urban skyline at night, coastal cliffs].

[CONTEXT FOUNDATION]
Location: [SPECIFIC SETTING — Pacific Northwest old-growth forest, Icelandic volcanic highlands, Tokyo neon district at 2am]. Season: [SEASON]. Time of day: [TIME — golden hour, blue hour, midday, twilight]. This is for [PURPOSE — desktop wallpaper, travel blog header, fine art print].

[STYLE DEFINITION]
[PHOTOGRAPHIC STYLE — landscape photography / cinematic still / painterly rendering] with ([LENS — 16mm ultra-wide for dramatic perspective / 50mm for natural], [FILM LOOK — Fuji Velvia saturation / muted documentary], [RENDERING — sharp throughout / selective focus on foreground]).

[COMPOSITIONAL LAYOUT]
[COMPOSITION — rule of thirds with horizon on lower third / leading lines converging to focal point / foreground-midground-background layers]. Focal point: [ELEMENT — lone tree, mountain peak, reflection in water]. [DEPTH — strong depth with foreground interest].

[CONSISTENCY CONSTRAINTS]
Lighting must be physically consistent with the stated time of day. Cloud shadows should align with light direction. Water reflections must match the sky and surrounding elements accurately.

[TECHNICAL UNIFORMITY]
Lighting: [NATURAL LIGHT — warm golden hour glow / cool overcast diffusion / dramatic storm light breaking through clouds]. Atmosphere: [ATMOSPHERIC EFFECTS — morning mist, haze, rain, dust particles in light]. Color palette: [PALETTE — warm earth tones, cool blues and greens, high-contrast complementary].

[OUTPUT SPECS + NEGATIVES]
Ultra-high detail, sharp across the full frame, suitable for large print.
No artificial HDR halos. No oversaturation. No visible compositing artifacts.
```

**Recommended aspect ratio:** `16:9` (widescreen) or `3:2` (classic landscape)

---

## Template 4: Infographic

```
[TASK DECLARATION]
Create a [STYLE — clean modern / retro vintage / hand-drawn / corporate] infographic about [TOPIC].

[CONTEXT FOUNDATION]
Format: [ORIENTATION — vertical scrolling / horizontal landscape / square social post]. This is for [PURPOSE — blog post, internal presentation, social media, print handout]. Target audience: [AUDIENCE — general public, technical team, executives].

[STYLE DEFINITION]
[VISUAL STYLE — flat design with bold colors / editorial illustration / data-driven minimalist] with ([COLOR SCHEME — brand colors [hex codes] / complementary palette / monochromatic], [TYPOGRAPHY STYLE — bold sans-serif headers with clean body text / handwritten feel], [ICON STYLE — line icons / filled icons / illustrated]).

[COMPOSITIONAL LAYOUT]
Structure: [LAYOUT — top-to-bottom flow with distinct sections / three-column comparison / timeline / process flow]. Sections: [ENUMERATE — "Section 1: [title]. Section 2: [title]. Section 3: [title]."]. Each section clearly separated with [DIVIDERS — colored bars, whitespace, horizontal rules].

[CONSISTENCY CONSTRAINTS]
Consistent icon style, color coding, and typography weight across all sections. Data visualizations (charts, graphs) must use the same color scheme. All text must be legible at the final display size.

[TECHNICAL UNIFORMITY]
Color: [BACKGROUND — white / light gray / dark theme]. Consistent padding and margins between sections. Hierarchy: primary data in largest type, supporting details smaller. All text rendered sharply.

[OUTPUT SPECS + NEGATIVES]
All text must be accurate, legible, and spelled correctly. Clean vector-like rendering.
No blurry text. No inconsistent icon styles. No cluttered layouts.
```

**Recommended aspect ratio:** `9:16` (vertical) or `2:3` (tall portrait)

---

## Template 5: UI Mockup

```
[TASK DECLARATION]
Create a high-fidelity UI mockup of [SCREEN TYPE — mobile app home screen, web dashboard, settings page, onboarding flow] for [APP/PRODUCT NAME AND PURPOSE].

[CONTEXT FOUNDATION]
Platform: [PLATFORM — iOS, Android, web desktop, responsive]. Device frame: [FRAME — iPhone 15 Pro, none, browser window]. This is for [PURPOSE — client presentation, developer handoff, portfolio piece].

[STYLE DEFINITION]
[DESIGN SYSTEM — Material Design 3 / iOS Human Interface / custom minimal] with ([COLOR SCHEME — primary [hex], secondary [hex], neutral [hex]], [TYPOGRAPHY — SF Pro for iOS / Inter for web / system font], [CORNER RADIUS — 8px cards, 12px modals, pill buttons]).

[COMPOSITIONAL LAYOUT]
Screen layout: [DESCRIBE — top navigation bar with logo and hamburger menu, hero card with featured content, scrollable grid of 6 items in 2 columns, bottom tab bar with 4 icons]. [CONTENT — use realistic placeholder content, not lorem ipsum].

[CONSISTENCY CONSTRAINTS]
Follow [DESIGN SYSTEM] spacing and sizing conventions. Consistent padding (16px), consistent icon sizes (24px), consistent touch targets (44px minimum). All interactive elements must have clear affordances.

[TECHNICAL UNIFORMITY]
Light/dark mode: [MODE]. Colors must meet WCAG AA contrast ratios. Consistent elevation/shadow treatment for cards and overlays.

[OUTPUT SPECS + NEGATIVES]
Pixel-perfect, production-ready mockup with realistic content. Sharp text rendering.
No lorem ipsum. No inconsistent spacing. No cut-off elements.
```

**Recommended aspect ratio:** `9:16` (mobile) or `16:9` (desktop/web)

---

## Template 6: Concept Art

```
[TASK DECLARATION]
Create [CONCEPT TYPE — character concept art / environment concept / creature design / vehicle design / weapon design] for [PROJECT CONTEXT — fantasy RPG, sci-fi film, children's book, mobile game].

[CONTEXT FOUNDATION]
World/setting: [WORLD — post-apocalyptic desert, underwater kingdom, steampunk Victorian London, enchanted forest]. Mood: [MOOD — dark and foreboding, whimsical and colorful, epic and grand, intimate and mysterious]. This is for [PURPOSE — game pitch, film pre-production, illustration portfolio].

[STYLE DEFINITION]
[ART STYLE — painterly digital art / anime / western comic / semi-realistic] with ([TECHNIQUE — loose brushwork with defined silhouette / clean line art with flat colors / atmospheric painting], [PALETTE — muted earth tones / neon cyberpunk / warm fantasy golds and greens], [INFLUENCE — "reminiscent of [ARTIST/FRANCHISE]"]).

[COMPOSITIONAL LAYOUT]
[VIEWS — single dramatic pose / multiple views (front, side, detail callouts) / action scene]. [FRAMING — full body with environmental context / bust portrait / dynamic action angle]. [FOCAL POINT — the subject's face/weapon/unique feature].

[CONSISTENCY CONSTRAINTS]
Design elements must be internally consistent (armor pieces match, proportions are deliberate). Color palette should reinforce the world's visual identity. Silhouette must be readable and distinctive.

[TECHNICAL UNIFORMITY]
Lighting: [SETUP — dramatic rim light / ambient environmental / warm campfire glow]. Rendering: [FINISH — polished final / rough concept sketch / paintover]. Consistent level of detail across all elements.

[OUTPUT SPECS + NEGATIVES]
Rich detail, strong composition, clear character/object read at thumbnail size.
No generic designs. No anatomical errors. No conflicting style elements.
```

**Recommended aspect ratio:** `3:4` (character) or `16:9` (environment)

---

## Template 7: Architectural Visualization

```
[TASK DECLARATION]
Create a [VISUALIZATION TYPE — exterior rendering / interior rendering / aerial view / cross-section] of [BUILDING/SPACE — modern residential home, coworking office, restaurant interior, urban plaza].

[CONTEXT FOUNDATION]
Style: [ARCHITECTURAL STYLE — modern minimalist, mid-century modern, industrial loft, Scandinavian, brutalist]. Location context: [SETTING — suburban lot with mature trees, downtown corner, waterfront, hillside]. Time of day: [TIME — bright midday, golden hour, blue twilight, night with interior glow]. This is for [PURPOSE — client presentation, real estate listing, architectural portfolio].

[STYLE DEFINITION]
[RENDERING APPROACH — photorealistic architectural visualization / watercolor sketch / technical line drawing] with ([MATERIALS — warm oak flooring, white plaster walls, floor-to-ceiling glass, exposed concrete], [FURNITURE STYLE — Eames and Noguchi mid-century / contemporary Italian / Scandinavian minimal], [LANDSCAPE — native plantings, manicured lawn, gravel paths]).

[COMPOSITIONAL LAYOUT]
[CAMERA — wide-angle interior from entry looking toward main living area / exterior street-level perspective / bird's eye at 45 degrees]. [FOCAL POINT — the main design feature: double-height window, cantilevered staircase, central courtyard]. Human figures for scale: [YES/NO — if yes, 1-2 people in natural activity].

[CONSISTENCY CONSTRAINTS]
Materials must appear realistic and consistent (same wood grain, same concrete finish throughout). Scale must be architecturally accurate. Furniture and fixtures must be proportionally correct.

[TECHNICAL UNIFORMITY]
Lighting: [SETUP — natural light streaming through windows with soft bounce / artificial warm-white interior lighting / mixed natural + accent lighting]. Shadows: architecturally accurate based on sun position. Reflections: realistic on glass and polished surfaces.

[OUTPUT SPECS + NEGATIVES]
High-resolution, presentation-quality rendering. Architecturally accurate proportions.
No distorted perspectives. No floating objects. No impossible lighting.
```

**Recommended aspect ratio:** `16:9` (presentation) or `3:2` (portfolio)

---

## Template 8: Food Photography

```
[TASK DECLARATION]
Create a [FOOD PHOTOGRAPHY STYLE — editorial, rustic, minimalist, overhead flat lay] photograph of [DISH — specific dish name with key ingredients visible].

[CONTEXT FOUNDATION]
Setting: [SURFACE AND ENVIRONMENT — dark wood table with linen napkin, marble counter, outdoor picnic, restaurant plating]. Cuisine context: [CUISINE — Japanese kaiseki, Italian trattoria, modern Scandinavian, Southern comfort]. This is for [PURPOSE — cookbook, restaurant menu, food blog, Instagram post].

[STYLE DEFINITION]
[PHOTOGRAPHIC APPROACH — natural light food photography / dramatic chiaroscuro / bright and airy] with ([LENS — 50mm f/1.8 for shallow depth / 35mm for context / 90mm macro for details], [COLOR GRADE — warm and inviting / cool and modern / earthy and muted], [TEXTURE EMPHASIS — visible steam, glistening sauce, crispy edges, melting cheese]).

[COMPOSITIONAL LAYOUT]
[ANGLE — 45-degree hero angle / directly overhead flat lay / eye-level for tall dishes like burgers and drinks]. [ARRANGEMENT — main dish center with negative space / styled with props: [list utensils, napkin, ingredients, drinks]]. [GARNISH — fresh herbs, sauce drizzle, scattered crumbs for texture].

[CONSISTENCY CONSTRAINTS]
Food must look fresh, appetizing, and at peak presentation. Colors must be natural — not oversaturated. Portion size must look generous but realistic.

[TECHNICAL UNIFORMITY]
Lighting: [SETUP — soft natural window light from the left / overhead softbox / backlight with diffusion for steam/glow]. Depth of field: [DOF — shallow with sharp focus on key detail / deep for flat lay showing everything]. Color temperature: warm enough to be inviting, not so warm it looks unnatural.

[OUTPUT SPECS + NEGATIVES]
Appetizing, editorial-quality food photography. Sharp focus on the hero element.
No artificial-looking food. No unappetizing colors. No harsh shadows obscuring the dish.
```

**Recommended aspect ratio:** `1:1` (Instagram) or `4:5` (social portrait)

---

## Template 9: Abstract / Artistic

```
[TASK DECLARATION]
Create an abstract [MEDIUM — digital painting / generative art / mixed media / sculptural rendering] exploring the concept of [THEME — motion, solitude, emergence, chaos and order, interconnection].

[CONTEXT FOUNDATION]
Emotional register: [MOOD — contemplative, energetic, unsettling, euphoric, meditative]. This is for [PURPOSE — gallery print, album cover, wallpaper, editorial illustration, brand identity].

[STYLE DEFINITION]
[ARTISTIC APPROACH — geometric abstraction / organic fluid forms / glitch art / Color Field painting / data visualization art] with ([COLOR PALETTE — monochromatic blues with a single red accent / full spectrum / earth tones with metallic gold / neon on black], [TEXTURE — smooth gradients / rough brushwork / digital noise / crystalline], [INFLUENCE — "inspired by [REFERENCE — Kandinsky, Zaha Hadid, James Turrell, generative algorithms]"]).

[COMPOSITIONAL LAYOUT]
[STRUCTURE — centered focal point radiating outward / asymmetric tension between two masses / flowing movement from lower left to upper right / grid-based modular pattern]. [NEGATIVE SPACE — generous, integral to the composition / minimal, filled edge-to-edge]. [SCALE VARIATION — mix of macro and micro elements].

[CONSISTENCY CONSTRAINTS]
The visual language must feel intentional and coherent — not random. Color palette must be used consistently. Repeated motifs should vary in scale but maintain recognizable identity.

[TECHNICAL UNIFORMITY]
Lighting: [TREATMENT — self-luminous elements / ambient gallery lighting / dramatic directional]. Color transitions: [HANDLING — smooth blending / hard edges / dithered]. Overall harmony between all compositional elements.

[OUTPUT SPECS + NEGATIVES]
Visually striking, gallery-quality resolution. Strong composition at both thumbnail and full size.
No cliched fractal spirals. No clipart. No unintentional symmetry that flattens the composition.
```

**Recommended aspect ratio:** `1:1` (print) or `16:9` (widescreen display)

---

## Template 10: Social Media Graphic

```
[TASK DECLARATION]
Create a [PLATFORM — Instagram post / Twitter/X header / LinkedIn banner / YouTube thumbnail / Facebook ad] graphic for [BRAND/PURPOSE — product launch, event announcement, motivational quote, data highlight, behind-the-scenes].

[CONTEXT FOUNDATION]
Brand: [BRAND IDENTITY — name, industry, vibe (playful/corporate/edgy/luxury)]. Target audience: [AUDIENCE — tech professionals, fitness enthusiasts, Gen Z consumers, B2B decision-makers]. Campaign: [CAMPAIGN — product launch, seasonal promotion, thought leadership, hiring].

[STYLE DEFINITION]
[VISUAL STYLE — bold and graphic / photo-based with overlay / illustrated / minimalist typography-forward] with ([BRAND COLORS — primary [hex], secondary [hex], accent [hex]], [TYPOGRAPHY STYLE — bold condensed sans-serif headline, clean body text], [GRAPHIC ELEMENTS — geometric shapes, gradients, photo cutouts, icons]).

[COMPOSITIONAL LAYOUT]
[LAYOUT — headline dominant (60% of frame) with supporting image / split layout: image left, text right / centered text over full-bleed photo / collage grid]. Text content: [HEADLINE — "exact text here"]. [SUBTEXT — "supporting text here"]. [CTA — "Call to action text"]. Logo: [POSITION — bottom right corner, small].

[CONSISTENCY CONSTRAINTS]
Must follow brand guidelines: correct colors, typography hierarchy, logo placement. Text must be readable against background (use contrast overlay if needed). Visual hierarchy: headline > image > subtext > CTA > logo.

[TECHNICAL UNIFORMITY]
Color: on-brand throughout. Text contrast: WCAG AA minimum against background. Consistent padding from edges (minimum [SAFE ZONE]px). All text elements aligned to a grid.

[OUTPUT SPECS + NEGATIVES]
Text must be perfectly legible and accurately spelled. Colors must match brand hex values exactly.
No blurry text. No off-brand colors. No cramped layouts. No unreadable text over busy backgrounds.
```

**Recommended aspect ratio:** `1:1` (Instagram/Facebook) or `16:9` (YouTube/LinkedIn/Twitter)

---

## Prompt Refinement Tips (Model-Specific)

Common issues and fixes when using these templates with Nano Banana 2:

| Issue | Cause | Fix |
|-------|-------|-----|
| Image looks too photorealistic | NB2's realism bias | Add "stylized illustration" or "Not photorealistic" |
| Text is misspelled | Too many words or ambiguous placement | Shorten text, use quotes, specify position explicitly |
| Wrong style/mood | Too vague | Add a known reference anchor ("in the style of...") |
| Composition feels random | Layout layer too vague | Enumerate positions: "Element A at top-left, B at center-right" |
| Character looks different from reference | Weak identity constraint | Repeat "exactly the same as the reference" 3+ times |
| Colors are off | No explicit color specification | Use hex codes for critical colors |
| Too busy / cluttered | Too many elements without hierarchy | Reduce elements, add "clean composition with generous negative space" |
| Flat / boring lighting | Default flat lighting | Specify exact lighting setup with direction and quality |
| Aspect ratio doesn't match use case | Wrong ratio selected | Refer to the aspect ratio guide in SKILL.md |
| Output resolution too low | Default 1K | Add `--aspect-ratio` flag and specify image_size in API config |

### Iterative Refinement Workflow

1. **First pass:** Run the template with all placeholders filled
2. **Review:** Check the output against each layer of the template
3. **Refine:** Don't regenerate — instead, describe specific changes:
   - "Make the lighting warmer"
   - "Move the subject slightly to the left"
   - "Change the background to a deeper blue"
4. **Polish:** Final pass for details: "Sharpen the text", "Add more contrast to the shadows"

This iterative approach leverages NB2's conversational editing strength and saves API costs.
