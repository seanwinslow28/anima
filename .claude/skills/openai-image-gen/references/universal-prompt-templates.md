# Universal Prompt Templates — GPT Image 2

> **When to read:** Use these templates when generating any image type via OpenAI GPT Image 2. Each template follows the 7-Layer Prompt Framework from the `image-generator-prompt-science` skill, tuned for GPT Image 2's quirks (silent auto-revision, strong realism bias, excellent text rendering). Copy the template, fill in the bracketed placeholders, and remove layers that don't apply.

---

## How to Use These Templates

1. Pick the template closest to your image type
2. Replace all `[BRACKETED]` placeholders with specifics
3. Drop layers that don't add value (not every image needs all 7)
4. Run through `scripts/generate_image.py` with the appropriate `--aspect-ratio` and `--quality`

### GPT Image 2 defensive-writing reminders (apply to every template)

- **Style anchor in Layer 3 must be explicit and named.** "In the unmistakable style of [ARTIST]" survives auto-revision; "stylized" does not.
- **Repeat the load-bearing constraint** in Layer 7. If the image is hand-drawn, write "NOT digital flat. NOT photorealistic." in Layer 7 even if Layer 3 already said so.
- **Wrap exact text content in quotes** so the model renders it character-accurate.
- **Use `--quality high`** whenever the image carries text or fine line detail.
- **Use `--reference [PATH]`** when a single image carries the aesthetic — routes to `images.edit` with `input_fidelity=high`.

---

## Template 1: Editorial Illustration (Substack header, blog hero)

```
[TASK DECLARATION]
Create an editorial illustration for [PUBLICATION/USE — Substack post header / blog hero / magazine feature].

[CONTEXT FOUNDATION]
This illustrates an essay titled "[POST_TITLE]". The essay's subject is [POST_SUBJECT_ONE_SENTENCE]. Target audience: [AUDIENCE — e.g., AI product managers, design leaders, general readers].

[STYLE DEFINITION]
In the unmistakable style of [ARTIST — Ralph Steadman / Wes Anderson / Saul Steinberg / Maira Kalman], dialed down to a [REGISTER — quiet domestic / chaotic gonzo / minimalist deadpan] register. [MEDIUM — Gestural india-ink linework with watercolor wash splotches and deliberate ink splatter / Flat geometric vector with limited palette / Loose pencil sketch with selective ink wash]. Hand-drawn medium throughout — NOT digital flat, NOT photorealistic.

[COMPOSITIONAL LAYOUT]
[COMPOSITION — Domestic interior framing / Editorial-cover framing / Fish-eye distortion]. [FRAMING — describe specific scene]. Aspect ratio 16:9 for header use. Generous breathing room around the central subject.

[CONSISTENCY CONSTRAINTS]
Single coherent [MEDIUM] throughout. The [TEXTURE — splatter / brushwork / cross-hatching] is deliberate, controlled, never chaotic. The watercolor wash sits BEHIND the ink, not on top of it.

[TECHNICAL UNIFORMITY]
Palette: [PALETTE — e.g., warm sepia, burnt orange, dusty rose, cream wash with deeper umber splatters]. Lighting: [LIGHTING — soft warm interior / harsh fluorescent / nocturnal neon]. Mood: [MOOD — cozy but slightly off-kilter / visceral and chaotic / deadpan absurdist].

[OUTPUT SPECS + NEGATIVES]
High detail in the ink work. NOT photorealistic. NOT digital illustration. Hand-drawn editorial quality, magazine-cover register.
NO text in the image. NO watermark. NO signature. Negative space is a feature, not a bug.
```

**Recommended:** `--aspect-ratio 16:9 --quality high --reference [path-to-style-anchor.png]`

---

## Template 2: Photorealistic Portrait

```
[TASK DECLARATION]
Create a professional photorealistic portrait of [SUBJECT — age, gender, ethnicity, distinguishing features].

[CONTEXT FOUNDATION]
Setting: [ENVIRONMENT — studio, outdoor, office]. Background: [BACKGROUND — blurred bokeh / solid color / environmental]. This is for [PURPOSE — LinkedIn headshot, editorial feature, casting portfolio].

[STYLE DEFINITION]
Photographic style with [CAMERA — 85mm portrait lens, f/2.0 aperture], [FILM STOCK — clean digital / Kodak Portra 400 warmth / black and white silver gelatin], sharp focus on eyes, natural skin texture with visible pores.

[COMPOSITIONAL LAYOUT]
[FRAMING — headshot / bust shot / three-quarter body] with subject positioned [PLACEMENT — center / rule of thirds left]. [GAZE — looking directly at camera / slight off-camera gaze]. [POSE — relaxed shoulders, hands visible/not visible].

[CONSISTENCY CONSTRAINTS]
Maintain natural proportions and realistic anatomy. Skin tones natural and even. If reference provided: keep facial features exactly the same as the reference image.

[TECHNICAL UNIFORMITY]
Lighting: [SETUP — Rembrandt with soft fill / butterfly / three-point softbox / golden hour backlight]. Consistent color temperature. Natural shadows preserving facial detail without harsh edges.

[OUTPUT SPECS + NEGATIVES]
High-resolution, print-ready. Sharp focus on eyes.
No artificial smoothing. No plastic skin. No visible artifacts. No watermarks.
```

**Recommended:** `--aspect-ratio 3:4 --quality high` (add `--reference` for identity locking)

---

## Template 3: Product Photography

```
[TASK DECLARATION]
Create a professional product photograph of [PRODUCT — material, color, size, brand aesthetic].

[CONTEXT FOUNDATION]
Surface: [SURFACE — white seamless / marble tabletop / rustic wood / lifestyle kitchen counter]. This is for [PURPOSE — e-commerce listing / luxury campaign / social media ad].

[STYLE DEFINITION]
Clean commercial photography with [LENS — 50mm macro for small products / 35mm lifestyle], [DEPTH — shallow for hero shots / deep for catalog], [FINISH — matte / glossy / textured].

[COMPOSITIONAL LAYOUT]
[ANGLE — 45-degree hero / flat lay / eye-level / overhead]. Product centered with [NEGATIVE SPACE — generous white space / tight crop]. [PROPS — none / minimal: list them].

[CONSISTENCY CONSTRAINTS]
Product color and material accurate and consistent. Realistic scale relative to any props. No color cast shifting the product's true appearance.

[TECHNICAL UNIFORMITY]
Lighting: [SETUP — soft diffused overhead with fill card / rim light / warm key]. Shadows: [SHADOW — soft natural / hard dramatic / no shadow]. Consistent highlight behavior across reflective surfaces.

[OUTPUT SPECS + NEGATIVES]
Crisp, high-detail, suitable for large-format display. Sharp product edges.
No motion blur. No lens flare. No dust or scratches unless intentional.
```

**Recommended:** `--aspect-ratio 1:1 --quality high`

---

## Template 4: Infographic (text-heavy)

```
[TASK DECLARATION]
Create a [STYLE — clean modern / retro / hand-drawn / corporate] infographic about [TOPIC].

[CONTEXT FOUNDATION]
Format: [ORIENTATION — vertical scrolling / horizontal landscape / square social]. For [PURPOSE — blog, presentation, social, print]. Audience: [AUDIENCE].

[STYLE DEFINITION]
[VISUAL STYLE — flat design with bold colors / editorial illustration / data-driven minimalist] with [COLOR SCHEME — brand colors with hex codes], [TYPOGRAPHY — bold sans-serif headers, clean body text], [ICON STYLE — line / filled / illustrated].

[COMPOSITIONAL LAYOUT]
Structure: [LAYOUT — top-to-bottom flow / three-column comparison / timeline / process flow]. Sections, enumerated explicitly: "Section 1: [exact title]. Section 2: [exact title]. Section 3: [exact title]." Each section clearly separated with [DIVIDERS — colored bars / whitespace / horizontal rules].

[CONSISTENCY CONSTRAINTS]
Consistent icon style, color coding, and typography weight across all sections. Charts use the same color scheme. All text legible at final display size.

[TECHNICAL UNIFORMITY]
[BACKGROUND — white / light gray / dark theme]. Consistent padding and margins. Hierarchy: primary data largest, supporting details smaller.

[OUTPUT SPECS + NEGATIVES]
All text accurate, legible, spelled correctly. Clean vector-like rendering.
No blurry text. No inconsistent icon styles. No cluttered layouts.
```

**Recommended:** `--aspect-ratio 2:3 --quality high` (high is non-negotiable for text)

---

## Template 5: Landscape / Environment

```
[TASK DECLARATION]
Create a [MOOD — serene, dramatic, moody, vibrant] landscape photograph of [SCENE].

[CONTEXT FOUNDATION]
Location: [SPECIFIC SETTING]. Season: [SEASON]. Time of day: [TIME — golden hour, blue hour, midday, twilight]. For [PURPOSE — desktop wallpaper, blog header, fine art print].

[STYLE DEFINITION]
[PHOTOGRAPHIC STYLE — landscape photography / cinematic still / painterly] with [LENS — 16mm ultra-wide / 50mm natural], [FILM LOOK — Fuji Velvia saturation / muted documentary], [RENDERING — sharp throughout / selective focus].

[COMPOSITIONAL LAYOUT]
[COMPOSITION — rule of thirds with horizon on lower third / leading lines to focal point / foreground-mid-background layers]. Focal point: [ELEMENT]. Strong depth with foreground interest.

[CONSISTENCY CONSTRAINTS]
Lighting physically consistent with stated time of day. Cloud shadows align with light direction. Water reflections match sky.

[TECHNICAL UNIFORMITY]
Lighting: [NATURAL LIGHT — warm golden / cool overcast / dramatic storm]. Atmosphere: [EFFECTS — mist, haze, rain, dust in light]. Palette: [PALETTE].

[OUTPUT SPECS + NEGATIVES]
Ultra-high detail, sharp across the frame, print-suitable.
No artificial HDR halos. No oversaturation. No compositing artifacts.
```

**Recommended:** `--aspect-ratio 16:9 --quality medium` (high only for print-bound work)

---

## Template 6: Concept Art

```
[TASK DECLARATION]
Create [CONCEPT TYPE — character / environment / creature / vehicle / weapon] concept art for [PROJECT — fantasy RPG, sci-fi film, children's book, mobile game].

[CONTEXT FOUNDATION]
World: [WORLD — post-apocalyptic desert, underwater kingdom, steampunk Victorian]. Mood: [MOOD — dark, whimsical, epic, intimate]. For [PURPOSE — game pitch, film pre-production, portfolio].

[STYLE DEFINITION]
[ART STYLE — painterly digital / anime / western comic / semi-realistic] with [TECHNIQUE — loose brushwork with defined silhouette / clean line art with flat colors / atmospheric painting], [PALETTE — muted earth tones / neon cyberpunk / warm fantasy], "reminiscent of [ARTIST/FRANCHISE]".

[COMPOSITIONAL LAYOUT]
[VIEWS — single dramatic pose / multiple views / action scene]. [FRAMING — full body with environment / bust / dynamic action]. Focal point: [SUBJECT'S FACE/WEAPON/UNIQUE FEATURE].

[CONSISTENCY CONSTRAINTS]
Design elements internally consistent (armor matches, proportions deliberate). Palette reinforces world identity. Silhouette readable and distinctive.

[TECHNICAL UNIFORMITY]
Lighting: [SETUP — dramatic rim / ambient / warm glow]. Rendering: [FINISH — polished final / rough concept / paintover]. Consistent detail across elements.

[OUTPUT SPECS + NEGATIVES]
Rich detail, strong composition, readable at thumbnail.
No generic designs. No anatomical errors. No conflicting style elements.
```

**Recommended:** `--aspect-ratio 3:4` (character) or `16:9` (environment) `--quality high`

---

## Template 7: UI Mockup

```
[TASK DECLARATION]
Create a high-fidelity UI mockup of [SCREEN — mobile home / web dashboard / settings page / onboarding] for [APP/PRODUCT AND PURPOSE].

[CONTEXT FOUNDATION]
Platform: [iOS / Android / web desktop / responsive]. Device frame: [iPhone 15 Pro / browser window / none]. For [PURPOSE — client presentation, developer handoff, portfolio].

[STYLE DEFINITION]
[DESIGN SYSTEM — Material Design 3 / iOS HIG / custom minimal] with [COLOR SCHEME — primary [hex], secondary [hex]], [TYPOGRAPHY — SF Pro / Inter / system], [CORNER RADIUS — 8px cards, 12px modals, pill buttons].

[COMPOSITIONAL LAYOUT]
[LAYOUT — describe in detail: nav bar with logo + hamburger, hero card with featured content, scrollable grid of 6 items 2 columns, bottom tab bar with 4 icons]. Use realistic placeholder content, NOT lorem ipsum.

[CONSISTENCY CONSTRAINTS]
Follow [DESIGN SYSTEM] spacing conventions. Consistent padding (16px), icon sizes (24px), touch targets (44px minimum). Clear affordances.

[TECHNICAL UNIFORMITY]
Mode: [LIGHT / DARK]. WCAG AA contrast. Consistent elevation/shadow for cards.

[OUTPUT SPECS + NEGATIVES]
Pixel-perfect, production-ready, realistic content. Sharp text rendering.
No lorem ipsum. No inconsistent spacing. No cut-off elements.
```

**Recommended:** `--aspect-ratio 9:16` (mobile) or `16:9` (desktop) `--quality high`

---

## Template 8: Food Photography

```
[TASK DECLARATION]
Create a [STYLE — editorial / rustic / minimalist / overhead flat lay] photograph of [DISH — name with key ingredients visible].

[CONTEXT FOUNDATION]
Setting: [SURFACE — dark wood with linen napkin / marble counter / outdoor picnic / restaurant plating]. Cuisine: [CUISINE — Japanese kaiseki, Italian, Scandinavian, Southern]. For [PURPOSE — cookbook, menu, food blog, Instagram].

[STYLE DEFINITION]
[APPROACH — natural light / dramatic chiaroscuro / bright and airy] with [LENS — 50mm f/1.8 / 35mm context / 90mm macro detail], [COLOR GRADE — warm / cool modern / muted earthy], [TEXTURE — visible steam, glistening sauce, crispy edges].

[COMPOSITIONAL LAYOUT]
[ANGLE — 45-degree hero / overhead flat lay / eye-level]. [ARRANGEMENT — main dish center with negative space, styled with props: [list]]. [GARNISH — fresh herbs, sauce drizzle].

[CONSISTENCY CONSTRAINTS]
Food fresh, appetizing, peak presentation. Colors natural — not oversaturated. Portion realistic.

[TECHNICAL UNIFORMITY]
Lighting: [SETUP — soft natural window light from left / overhead softbox / backlight with diffusion]. DOF: [shallow with sharp focus on key detail / deep for flat lay]. Color temperature: warm enough to be inviting.

[OUTPUT SPECS + NEGATIVES]
Appetizing, editorial-quality. Sharp focus on hero element.
No artificial-looking food. No unappetizing colors. No harsh shadows obscuring the dish.
```

**Recommended:** `--aspect-ratio 1:1 --quality medium`

---

## Template 9: Abstract / Artistic

```
[TASK DECLARATION]
Create an abstract [MEDIUM — digital painting / generative art / mixed media] exploring [THEME — motion, solitude, emergence, chaos and order].

[CONTEXT FOUNDATION]
Emotional register: [MOOD — contemplative, energetic, unsettling, euphoric, meditative]. For [PURPOSE — gallery print, album cover, wallpaper, editorial].

[STYLE DEFINITION]
[APPROACH — geometric abstraction / organic fluid / glitch art / Color Field / data viz art] with [PALETTE — monochromatic blues with red accent / earth tones with metallic gold / neon on black], [TEXTURE — smooth gradients / rough brushwork / digital noise], "inspired by [REFERENCE — Kandinsky, Zaha Hadid, James Turrell]".

[COMPOSITIONAL LAYOUT]
[STRUCTURE — centered focal point radiating outward / asymmetric tension / diagonal flow / grid-based modular]. [NEGATIVE SPACE — generous and integral / minimal edge-to-edge]. Mix of macro and micro elements.

[CONSISTENCY CONSTRAINTS]
Visual language intentional and coherent, NOT random. Palette used consistently. Repeated motifs vary in scale but maintain identity.

[TECHNICAL UNIFORMITY]
Lighting: [TREATMENT — self-luminous / ambient gallery / dramatic directional]. Color transitions: [HANDLING — smooth blending / hard edges / dithered].

[OUTPUT SPECS + NEGATIVES]
Visually striking, gallery-quality. Strong composition at thumbnail and full size.
No cliched fractal spirals. No clipart. No unintentional symmetry flattening the composition.
```

**Recommended:** `--aspect-ratio 1:1` or `16:9` `--quality medium`

---

## Template 10: Social Media Graphic

```
[TASK DECLARATION]
Create a [PLATFORM — Instagram post / Twitter header / LinkedIn banner / YouTube thumbnail] for [BRAND/PURPOSE — product launch, event, quote, data highlight].

[CONTEXT FOUNDATION]
Brand: [IDENTITY — name, industry, vibe]. Audience: [AUDIENCE]. Campaign: [CAMPAIGN].

[STYLE DEFINITION]
[STYLE — bold graphic / photo-based with overlay / illustrated / typography-forward] with [BRAND COLORS — primary [hex], secondary [hex], accent [hex]], [TYPOGRAPHY — bold condensed sans-serif headline, clean body], [GRAPHIC ELEMENTS — geometric shapes, gradients, photo cutouts, icons].

[COMPOSITIONAL LAYOUT]
[LAYOUT — headline dominant (60%) with supporting image / split: image left text right / centered text over full-bleed / collage grid]. Text content: HEADLINE "[exact text]". SUBTEXT "[exact text]". CTA "[exact text]". Logo bottom right, small.

[CONSISTENCY CONSTRAINTS]
Brand guidelines: correct colors, typography hierarchy, logo placement. Text readable against background (overlay if needed). Hierarchy: headline > image > subtext > CTA > logo.

[TECHNICAL UNIFORMITY]
On-brand color throughout. WCAG AA text contrast. Consistent padding from edges. Text aligned to grid.

[OUTPUT SPECS + NEGATIVES]
Text perfectly legible and accurately spelled. Colors matching brand hex exactly.
No blurry text. No off-brand colors. No cramped layouts. No unreadable text over busy backgrounds.
```

**Recommended:** `--aspect-ratio 1:1` (Instagram) or `16:9` (YouTube/LinkedIn) `--quality high`

---

## Prompt Refinement Tips (Model-Specific)

Common issues with GPT Image 2 and their fixes:

| Issue | Cause | Fix |
|---|---|---|
| Output drifts to photorealism when stylized was requested | Auto-revision softens style anchor | Repeat the explicit medium term ("hand-drawn ink and watercolor") twice; add "NOT photorealistic" three times in Layer 7 |
| Text is misspelled or cropped | Too many words or ambiguous placement | Shorten text, wrap in quotes, specify position, use `--quality high` |
| Reference image's style not preserved | Edit endpoint defaulted to low fidelity | Confirm `--reference` was passed (script auto-sets `input_fidelity=high`); reduce reference count to 1 |
| Polished magazine look when "gestural" was requested | Revision smoothed it | Layer 3 lead with "In the unmistakable style of [ARTIST]" + "Hand-drawn at speed by an artist who knows what they're doing — NOT slowly rendered, NOT smooth, NOT polished" |
| Colors off-brand | No explicit color spec | Use hex codes for critical colors throughout the prompt |
| Composition feels random | Layout layer too vague | Enumerate positions ("Element A top-left, B center-right, C bottom"); use "rule of thirds" anchors |
| Too cluttered | Too many elements without hierarchy | Reduce elements; add "clean composition with generous negative space" |
| Wrong aspect ratio in output | Invalid custom size on edit endpoint | Fall back to preset (`1536x1024` / `1024x1536` / `1024x1024`) |
| Content policy block on legitimate editorial work | Default `moderation=auto` too strict | Try `moderation=low` via SDK call directly; rephrase removing trigger words |

### Iterative refinement workflow

Unlike NB2 which excels at conversational editing, GPT Image 2's multi-turn refinement is weaker. Workflow:

1. **First pass:** Run the template filled in, at `--quality medium` to control cost
2. **Review:** Check the output against each layer of the template
3. **Refine the prompt itself** rather than asking for edits:
   - Tighten the load-bearing constraint
   - Add explicit medium negatives ("NOT photorealistic")
   - Adjust the failing voice slot (composition / palette / framing)
4. **Re-run at `--quality medium`** until composition lands
5. **Final pass at `--quality high`** for production output

This approach respects the model's strengths (single-shot fidelity at `high`) and its weaknesses (less predictable multi-turn editing).
