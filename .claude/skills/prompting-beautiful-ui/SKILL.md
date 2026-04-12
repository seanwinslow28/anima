---
name: prompting-beautiful-ui
description: System for generating award-winning, Awwwards-level UI with Claude Code. Covers the spec-driven workflow, anti-generic prompting, signature interaction design, scroll choreography, premium micro-interactions, typography as art, and the full prompting vocabulary that separates "good" from "work of art." Use when creating components, building pages, designing interfaces, or when UI output looks generic.
---

# Prompting for Award-Winning UI

## Purpose

Transform UI requests into specification-driven prompts that produce distinctive, Awwwards-caliber interfaces — not generic "AI slop." This skill covers the full pipeline: creative direction, specification, implementation, and polish. The goal is UI that someone would screenshot and share.

## When to Use

- Creating any new UI component, page, or layout
- UI output looks generic, corporate, or "AI-generated"
- Building interactions that need to feel premium and distinctive
- Wanting to match a specific design aesthetic or award-winning reference
- Adding scroll-driven animations, micro-interactions, or page transitions
- Setting up design systems that prevent generic output

## The Award-Winning Formula

```
Award-Winning = Solid Fundamentals
              + One Signature Interaction
              + Choreographed Motion
              + Performance Obsession
              + Relentless Polish on Every Page
```

The signature interaction is the thing that makes someone screenshot your site. Everything else supports that moment.

---

## Phase 1: Creative Direction (Before Any Code)

Never jump to code. The #1 cause of generic AI output is skipping creative direction.

### Define Visual Identity (5 minutes)

Ask these questions before generating anything:

1. **Personality**: What 3 adjectives describe this UI? (e.g., "precise, luminous, alive")
2. **Reference anchor**: "Like X meets Y" (e.g., "Linear's data density meets Stripe's typography")
3. **Signature moment**: What ONE interaction will be unforgettable?
4. **Typography strategy**: Specific font pairing with weights and roles
5. **Color commitment**: Dominant color with specific hex, accent strategy, tinted neutrals
6. **Motion language**: Spring physics? Scroll-driven? Staggered reveals? Clip-path transitions?

### Prompt Pattern: Creative Brief

```
Before writing any code, act as a creative director for an Awwwards-level site.
Design a creative brief for [feature/page]:

1. Visual identity: 3 personality adjectives
2. Typography: specific font pairing (not Inter) with weights
3. Color: dominant hex + accent hex + neutral strategy (tinted, not pure gray)
4. Layout: unconventional approach (broken grid, editorial, bento, asymmetric)
5. Signature interaction: one bespoke moment unique to this page
6. Motion choreography: entrance sequence, scroll behavior, hover vocabulary
7. Texture: grain, noise, glass, aurora — what material quality?

Reference sites: [paste URLs or "like X meets Y"]
Do not write code yet.
```

---

## Phase 2: Specification

### The Anti-Generic System Prompt

Add this to your CLAUDE.md or project instructions. It explicitly bans the patterns that make AI output recognizable:

```
<frontend_aesthetics>
You tend to converge toward generic outputs. In frontend design, this creates
"AI slop." Make creative, distinctive frontends that could win design awards.

BANNED PATTERNS (never use these):
- Inter/Roboto/Arial as the only font
- Purple/indigo gradients (the unofficial flag of AI-generated UI)
- Cards nested inside cards with uniform padding
- Pure gray text (#666, #888) — use tinted neutrals
- Pure black (#000000) backgrounds — use near-black (#09090B)
- shadow-lg on everything without elevation hierarchy
- Bounce/elastic easing applied indiscriminately
- Big rounded icons centered above every heading
- Symmetric hero sections with even accent distribution
- "transition: all 0.3s ease" as the only animation
- Centered layouts with excessive whitespace
- Everything looking equally important (weak hierarchy)

REQUIRED PATTERNS:
1. Typography with character: choose fonts that match the personality.
   Options: Space Grotesk, Instrument Serif, Bricolage Grotesque, Syne,
   Fraunces, Satoshi, Manrope, DM Sans, GT America, IBM Plex
2. Tinted neutrals: backgrounds and grays pick up a hint of the brand hue
3. Staggered entrance reveals with 40-80ms delay between siblings
4. Layered shadows: shadow + ring-1 ring-white/5 for depth
5. Intentional hierarchy: one element dominates each section
6. Choreographed motion: elements enter in sequence, not simultaneously
7. Texture layer: subtle noise overlay, grain gradient, or glass effect
8. One signature interaction per page that could ONLY exist on this site
</frontend_aesthetics>
```

### Component Specification Template

```markdown
# ROLE
You are building an Awwwards-caliber interface. You value distinctive aesthetics,
choreographed motion, and accessibility. Generic output is failure.

# COMPONENT: [Name]

## Visual Context
- Typography: [e.g., "Space Grotesk 600 headings, JetBrains Mono 400 for data"]
- Spacing: [e.g., "Dense, 8px internal, 16px between sections, 4px grid"]
- Shape: [e.g., "6px buttons, 8px cards, never pill-shaped"]
- Color: [e.g., "Primary #4ADE80, secondary #F97316, surface #09090B"]
- Texture: [e.g., "Subtle noise overlay at 4% opacity, grain gradient on hero"]
- Vibe: [e.g., "Mission control meets terminal, dark mode only"]

## Interaction Design
- Hover: [e.g., "scale(1.02) with spring(damping:20, stiffness:300), shadow elevation lift"]
- Active: [e.g., "scale(0.98), spring(damping:15, stiffness:400), 50ms"]
- Focus-visible: [e.g., "ring-2 ring-primary/50 ring-offset-2 ring-offset-surface"]
- Entrance: [e.g., "fade up from translateY(20px), stagger 50ms between items"]
- Scroll: [e.g., "parallax at 0.5x speed, fade to 0 opacity at 80% scroll"]

## States (all required)
- Default, hover, focus-visible, active, disabled
- Loading: skeleton that matches final layout exactly
- Error: calm diagnostic messaging, no apologetic language
- Empty: illustrated state, not just text

## Anti-Patterns for THIS Component
- [Specific things to avoid based on context]

## Signature Moment
- [The one interaction that makes this component special]

## Performance Rules
- Only animate transform and opacity (GPU-only)
- prefers-reduced-motion: disable all animation
- No layout thrashing, no forced reflow in animation loops

## Reference
[Screenshot, Figma link, or "like [site] meets [site]"]
```

---

## Phase 3: Implementation Techniques

### The Awwwards Toolkit

These are the specific techniques that separate award-winning sites from well-designed ones. Reference the full code patterns in `docs/award-winning-web-patterns.md`.

#### Scroll-Driven Animations
Award-winning sites treat scroll as interaction, not just navigation.

- **CSS `animation-timeline: scroll()`** — GPU-accelerated, no JS needed (Chrome 116+)
- **CSS `animation-timeline: view()`** — elements animate as they enter/exit viewport
- **Lenis smooth scrolling** — near-universal in Awwwards winners (~5KB)
- **GSAP ScrollTrigger** — precision scroll choreography, pin sections, scrub animations

Prompt pattern:
```
Add scroll-driven animations to this page:
- Progress bar at top fills as user scrolls (CSS animation-timeline: scroll())
- Cards fade up and scale from 0.8 as they enter viewport (animation-timeline: view())
- Hero text parallaxes at 0.5x scroll speed
- Use Lenis for smooth scroll (lerp: 0.1, duration: 1.2)
- Wrap all scroll animations in @supports (animation-timeline: scroll())
- prefers-reduced-motion: disable all scroll animation
```

#### Micro-Interactions That Feel Premium
The hover state is where most sites fail the award test.

- **Magnetic buttons** — element follows cursor when nearby, springs back on leave
- **Elastic hover** — `cubic-bezier(0.34, 1.56, 0.64, 1)` overshoots then settles
- **Button press** — translateY(-1px) on hover, translateY(1px) scale(0.98) on active
- **Link underline slide** — scaleX(0) to scaleX(1) with transform-origin flip
- **3D tilt cards** — mouse-tracking perspective rotateX/rotateY with inner parallax layers
- **Spring physics** — use Motion library for damping/stiffness/mass-based movement

Spring physics reference:
| Feel | Damping | Stiffness | Mass | Use Case |
|------|---------|-----------|------|----------|
| Snappy | 30 | 400 | 0.5 | Button press, toggles |
| Smooth | 20 | 300 | 0.5 | Hover feedback, cards |
| Bouncy | 10 | 200 | 0.8 | Playful elements, notifications |
| Heavy | 40 | 150 | 1.2 | Panels, drawers, modals |
| Gentle | 25 | 100 | 0.8 | Ambient floating, background orbs |

#### Typography as Art
Type is the #1 highest-impact change. A single font swap breaks generic instantly.

- **Split-text reveals** — GSAP SplitText (free) for line/word/char mask animations
- **Variable font animation** — animate weight, width, slant via CSS custom properties
- **Text masking** — `background-clip: text` with gradients or video behind text
- **Oversized type as layout** — `clamp(6rem, 15vw, 20rem)` with negative line-height

Font pairing recommendations (context-specific, never default Inter):
| Context | Heading | Body | Mono |
|---------|---------|------|------|
| SaaS / Dashboard | Geist Sans 600 | Geist Sans 400 | Geist Mono |
| Creative / Agency | Instrument Serif 400 | DM Sans 400 | JetBrains Mono |
| Fintech / Trust | IBM Plex Sans 600 | IBM Plex Sans 400 | IBM Plex Mono |
| Edgy / Distinctive | Syne 700 | Space Grotesk 400 | JetBrains Mono |
| Consumer / Friendly | Manrope 700 | Manrope 400 | Fira Code |
| Editorial / Magazine | Fraunces 700 | Satoshi 400 | -- |

#### Layout That Breaks Conventions
Award-winning layouts reject the standard 12-column card grid.

- **Broken grid** — overlapping elements via CSS Grid row/column overlap + z-index
- **Asymmetric splits** — 60/40 or 2fr/1fr content ratios
- **Editorial/magazine** — reading-width center column with full-bleed breakouts
- **Bento grid** — Apple-style mixed-size cards (span-2x2, span-2x1, span-1x2)
- **Horizontal scroll sections** — scroll-snap-type: x mandatory for panel-based storytelling

#### Color and Light
Color creates atmosphere. Flat colors create templates.

- **Aurora/mesh gradients** — animated blurred radial-gradient orbs on dark backgrounds
- **Glassmorphism 2.0** — backdrop-blur + luminous gradient borders via mask-composite
- **OKLCH color manipulation** — perceptually uniform hue shifting, clean gradient interpolation
- **Tinted neutrals** — every gray picks up a hint of the brand hue (never pure #666)
- **Grain texture** — SVG feTurbulence noise overlay at 4-15% opacity via mix-blend-mode

#### Reveal and Entrance Animations
First impressions are choreographed, not simultaneous.

- **Staggered fade-up** — `animation-delay: calc(var(--index) * 0.08s)` per child
- **Clip-path reveals** — inset, diagonal wipe, circle expand from center
- **Image reveal with zoom** — color overlay wipe + scale(1.3) to scale(1) on the image
- **Orchestrated page load** — GSAP timeline: bg -> nav -> hero title -> subtitle -> CTA -> sidebar -> ambient

Choreography rules:
1. Lead with the trigger element
2. Stagger siblings 40-80ms apart
3. Exits run at 70% of entrance duration
4. Movement follows reading direction
5. Related elements share the same easing curve
6. Farther elements take longer to arrive

#### Page Transitions
Route changes are opportunities, not jarring cuts.

- **React ViewTransition** — shared element morphing between routes (React canary)
- **FLIP pattern** — First/Last/Invert/Play for smooth layout animations
- **barba.js** — inter-page transitions with GSAP choreography (~7KB)

#### Cursor and Pointer Effects
Custom cursors signal craft and attention to detail.

- **Dual cursor** — outer ring with spring delay + inner dot that follows instantly
- **Spotlight reveal** — radial-gradient mask follows cursor, reveals hidden content
- **Context-aware scaling** — cursor grows on interactive elements, becomes text cursor on copy

#### Texture and Materiality
Flat surfaces feel like templates. Texture feels like craft.

- **SVG noise overlay** — inline data URI, no network request, 4% opacity
- **Grainy gradients** — feTurbulence + contrast(170%) brightness(1000%) + mix-blend-mode
- **Scanline overlay** — repeating-linear-gradient for CRT/retro aesthetic
- **Dot grid background** — radial-gradient dots at 24px spacing

#### Sound Design (Optional Premium Layer)
Procedural Web Audio API synthesis for key moments — no audio files needed.

- Click: 800Hz -> 600Hz sine, 80ms
- Hover: 1200Hz sine, 40ms, very quiet (0.03 gain)
- Success: ascending triad (C5, E5, G5), 150ms each
- Error: 200Hz -> 150Hz sawtooth, 300ms

Rules: always provide visual equivalent, configurable mute, respect OS settings.

---

## Phase 4: Polish (The Last 10%)

This is where "good" becomes "award-winning." Use `visual-polish-checklist` skill for the full checklist. Key items:

### Shadow Depth System
- Layered: `shadow-md ring-1 ring-black/5` (not just shadow-lg)
- Hover: increase shadow intensity AND add slight scale for physical lift
- Dark mode: shadows are invisible — use lighter surface colors for elevation

### Typography Micro-Details
- Headings: line-height 1.125-1.25, letter-spacing tracking-tight
- Body: line-height 1.5-1.625, letter-spacing normal
- Labels: letter-spacing tracking-wide, uppercase or small-caps
- Weight contrast: 600-800 headings vs 400 body

### Motion Easing Curves
```css
--ease-standard: cubic-bezier(0.2, 0, 0, 1);       /* Most UI transitions */
--ease-emphasized: cubic-bezier(0.05, 0.7, 0.1, 1); /* Entrances, important changes */
--ease-decelerate: cubic-bezier(0, 0, 0, 1);        /* Elements entering screen */
--ease-accelerate: cubic-bezier(0.3, 0, 1, 1);      /* Elements leaving screen */
--ease-elastic: cubic-bezier(0.34, 1.56, 0.64, 1);  /* Playful, attention-grabbing */
--ease-smooth: cubic-bezier(0.33, 1, 0.68, 1);      /* Buttery scroll-linked */
```

### Duration Scale
| Category | Duration | Use Case |
|----------|----------|----------|
| Micro | 100-150ms | Button press, toggle, icon state |
| Small | 200-300ms | Hover states, tooltips, dropdowns |
| Medium | 300-500ms | Panel opens, card transitions |
| Large | 500-800ms | Page transitions, layout shifts |
| Dramatic | 800-1200ms | Hero reveals, first-load sequences |

### Self-Review Checklist
```
After generating any UI, verify:
- [ ] No banned patterns (Inter-only, purple gradients, cards-in-cards, pure gray)
- [ ] Typography uses specified fonts with correct weights
- [ ] Colors use tinted neutrals, not pure gray
- [ ] Shadows are layered (shadow + ring), not just shadow-lg
- [ ] Spacing follows 4px grid consistently
- [ ] All interactive elements have hover + focus-visible + active states
- [ ] Entrance animations are staggered, not simultaneous
- [ ] prefers-reduced-motion disables all animation
- [ ] Only transform and opacity are animated (GPU-only)
- [ ] One element dominates each section (clear hierarchy)
- [ ] The signature interaction is implemented and polished
- [ ] Loading states use skeletons that match final layout
- [ ] Dark mode uses surface lightness for elevation, not shadows
```

---

## Visual Description Vocabulary

Vague adjectives produce generic output. Use specific terms:

| Dimension | Avoid (Generic) | Use (Specific) |
|---|---|---|
| Typography | "Nice fonts", "clean text" | "Instrument Serif headings + DM Sans body", "oversized clamp(6rem,15vw,20rem) hero type" |
| Spacing | "Good spacing" | "4px grid, 8px internal card padding, 32px section gaps" |
| Color | "Dark theme", "bright colors" | "OLED #050505 with oklch tinted warm neutrals, #4ADE80 accent at 70/25/5 ratio" |
| Motion | "Smooth animations" | "Spring(damping:20, stiffness:300) hover, 50ms stagger, expo.out entrance" |
| Layout | "Responsive", "modern" | "Broken grid with overlapping elements, 60/40 asymmetric split" |
| Texture | "Add depth" | "4% SVG noise overlay, grainy gradient on hero, grain + glassmorphism cards" |
| Scroll | "Scroll effects" | "Lenis smooth scroll, view() timeline fade-up on cards, pinned hero with scrub" |
| Style | "Premium", "modern" | Named movement: "Editorial Swiss", "Neobrutalist", "Terminal/CRT", "Glassmorphism 2.0" |

### Named Design Movements (use these in prompts)

- **Editorial / Swiss**: Strong typographic hierarchy, generous whitespace, grid discipline, serif headlines
- **Neobrutalism**: Thick borders, solid offset shadows, bright color blocks, raw typography
- **Glassmorphism 2.0**: Frosted glass + luminous gradient borders + animated aurora backgrounds
- **Terminal / Hacker**: Monospace everything, green-on-dark, scanline overlay, CRT aesthetic
- **Minimal Luxury**: Extreme whitespace, thin serif type, muted tones, subtle animations
- **Data-Dense / Mission Control**: Tight grids, monospace data, colored left-borders, dot-grid backgrounds

---

## Multi-Pass Workflow

High-quality UI is never built in one prompt. Plan for 3-5 passes:

**Pass 1: Layout and Structure**
```
Build the page layout for [feature]. Focus on information hierarchy, grid
structure, and responsive breakpoints. Use placeholder content. Use [broken grid /
bento / editorial / asymmetric] layout — NOT a standard card grid.
Do not worry about visual polish yet.
```

**Pass 2: Typography, Color, and Texture**
```
Apply the design system: [font pairing] headings + body, [primary hex] with
[accent hex] on [surface hex]. Add tinted neutrals (not pure gray). Add subtle
noise texture overlay at 4% opacity. Follow 70/25/5 color ratio.
```

**Pass 3: States and Data**
```
Add all states: hover (spring physics), focus-visible (ring with offset),
active (press feedback), disabled (reduced opacity). Add skeleton loaders
matching final layout. Add empty state with [illustration/icon]. Add error
state with calm diagnostic messaging.
```

**Pass 4: Animation and Signature Interaction**
```
Add choreographed motion:
- Page entrance: staggered fade-up sequence (nav -> title -> body -> CTA -> cards)
- Scroll: [specific scroll behavior from creative brief]
- Signature interaction: [the ONE bespoke moment from creative brief]
- Timing: 50ms stagger between siblings, expo.out easing, 400ms entrance
- prefers-reduced-motion: disable everything
- GPU-only: only animate transform and opacity
```

**Pass 5: Polish**
```
Run the visual polish checklist. Fix: layered shadows, tight heading
line-height, 4px grid consistency, tinted neutrals, focus-visible rings,
skeleton loaders, OKLCH gradient interpolation, dark mode elevation.
Check the signature interaction on mobile. Verify 60fps in DevTools.
```

---

## Copy/Paste Prompt Recipes

### Recipe 1: Break Out of Generic
```
Review this UI for "AI slop" aesthetics. Check for: Inter-only font, purple
gradients, cards-in-cards, uniform shadows, weak hierarchy, bounce easing,
centered symmetric layouts, pure gray text. Replace every instance with a
distinctive alternative using [my design system / these tokens / this aesthetic].
```

### Recipe 2: Add Signature Interaction
```
This page needs ONE signature interaction that makes someone screenshot it.
Design an interaction unique to [this page's content/purpose] that uses
[scroll / cursor / hover / reveal / 3D]. It should feel surprising but
intentional, work on mobile with touch equivalent, respect reduced-motion,
and run at 60fps. Describe the interaction first, then implement it.
```

### Recipe 3: Scroll Choreography
```
Add scroll-driven storytelling to this page:
- Hero: pinned with content scrubbing through on scroll (GSAP ScrollTrigger)
- Section transitions: clip-path reveals as sections enter (CSS view() timeline)
- Cards: staggered fade-up as they cross viewport threshold
- Progress indicator: thin bar at top (CSS scroll() timeline)
- Lenis smooth scroll wrapping the entire page
- Progressive enhancement: @supports check for scroll-timeline
- Fallback: static layout with simple opacity transitions
```

### Recipe 4: Premium Card Component
```
Build a card component that feels premium, not template-grade:
- Subtle 1px border (ring-1 ring-white/6) + layered shadow
- Noise texture overlay at 3% opacity
- 3D tilt on hover: perspective(800px) rotateX/rotateY tracking mouse position
- Inner content at different translateZ depths for parallax within the card
- Spring-based return to flat on mouse leave (damping:20, stiffness:300)
- Entrance: clip-path inset reveal + fade, staggered if in a grid
- prefers-reduced-motion: static card with simple opacity hover
```

### Recipe 5: Typography as Hero
```
Design a hero section where typography IS the design:
- Oversized heading: clamp(4rem, 12vw, 14rem), weight 900, line-height 0.9
- Split-text reveal: GSAP SplitText mask animation, lines stagger 0.08s
- Text masking: gradient or video behind text via background-clip: text
- Let text bleed off-screen intentionally (negative margin)
- Body text overlaps the giant heading with relative positioning
- Variable font weight animation on scroll (200 -> 800 via view() timeline)
```

### Recipe 6: Aurora/Atmospheric Background
```
Add an atmospheric background that feels alive:
- 2-3 blurred gradient orbs (radial-gradient, 300-400px, filter: blur(80px))
- Slow orbital animation (12s infinite, transform only)
- Colors from the design system at 10-15% opacity
- Optional: glassmorphism card on top (backdrop-filter: blur(16px))
- Optional: grain texture overlay (SVG feTurbulence, 4% opacity)
- Performance: only animate transform, use will-change: transform
- prefers-reduced-motion: static gradient, no animation
```

---

## The Good vs. Award-Winning Delta

| Dimension | Good Site | Award-Winning Site |
|-----------|-----------|-------------------|
| **Scroll** | Content appears | Scroll IS the interaction; choreographed to position |
| **Typography** | Clean hierarchy | Type is animated, oversized, masked — it IS the design |
| **Hover** | Color change | Magnetic pull, 3D tilt, parallax within cards, staggered reveals |
| **Loading** | Spinner/skeleton | Orchestrated entrance that builds anticipation |
| **Layout** | Card grid | Broken grids, overlapping elements, editorial compositions |
| **Color** | Consistent palette | Animated gradients, aurora, luminous borders, grain textures |
| **Cursor** | Default | Custom cursor that transforms based on context |
| **Transitions** | Fade | Shared element morphing, FLIP, view transitions |
| **Texture** | Flat surfaces | Noise overlays, grain gradients, glass, layered depth |
| **Mobile** | Responsive | Designed-for-touch with equivalent interaction quality |
| **Uniqueness** | Design system | One signature moment that ONLY this site has |

---

## Library Quick Reference

| Library | Purpose | Size | When to Use |
|---------|---------|------|-------------|
| **GSAP** | Animation orchestration, ScrollTrigger, SplitText | ~30KB | Scroll choreography, split-text, timelines |
| **Motion** | React spring physics, layout animations, gestures | ~35KB | Hover springs, magnetic effects, layout |
| **Lenis** | Smooth scrolling | ~5KB | Almost always (near-universal in winners) |
| **barba.js** | Page transitions | ~7KB | Multi-page route transitions |

Full code patterns for all techniques: see `docs/award-winning-web-patterns.md`

---

## Awwwards Judging Criteria (for context)

| Criterion | Weight | What They Judge |
|-----------|--------|-----------------|
| Design | 40% | Visual hierarchy, typography, color, composition, consistency across ALL pages |
| Usability | 30% | Navigation, load speed, Core Web Vitals, cross-device, accessibility |
| Creativity | 20% | Novel interactions, unexpected layouts, custom experiences |
| Content | 10% | Original media, professional copy, real content |

Threshold: 6.5+ for Honorable Mention. Fewer than 365 SOTDs/year from 15,000+ submissions. Usability failures (not lack of creativity) are the #1 reason sites lose.

---

## Scope Boundaries

- For **post-generation visual review**: use `visual-polish-checklist`
- For **specific micro-interaction code patterns**: use `micro-interaction-patterns`
- For **advanced Tailwind techniques** (gradients, glassmorphism, dark mode): use `tailwind-advanced-patterns`
- For **shadcn/ui component patterns**: use `shadcn-ui-patterns`
- For **UX design rules** (accessibility, touch targets, forms): use `ux-design-guidelines`
- This skill focuses on **creative direction and prompting strategy** that produces distinctive UI
