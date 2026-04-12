---
name: visual-polish-checklist
description: Systematic visual quality checklist for reviewing and polishing generated UI. Covers shadow depth, gradient quality, typography refinements, spacing rhythm, border treatments, dark mode correctness, loading states, and self-review techniques. Use when polishing UI, reviewing design quality, fixing generic-looking output, adding loading states, or making dark mode look correct.
---

# Visual Polish Checklist

## Purpose

Systematically review and improve generated UI for visual quality. Use this checklist to identify and fix polish gaps in shadows, gradients, typography, spacing, borders, dark mode, and loading states. Apply after initial code generation to elevate output from functional to premium.

## When to Use

- UI looks "good enough" but not premium
- Reviewing generated components before shipping
- Dark mode looks wrong (flat, low contrast, invisible shadows)
- Loading states are missing or jarring
- Output feels generic and needs distinctive refinement

## Examples

**Example 1: Polish review**
```
User: "This dashboard looks flat and generic, polish it"
Claude: [Uses visual-polish-checklist] Runs the full checklist:
- Adds layered shadows (ring + shadow) for depth
- Switches to OKLCH gradients to fix muddy midpoints
- Tightens heading line-height to 1.25
- Enforces 4px spacing grid
- Adds skeleton loaders for data panels
```

**Example 2: Dark mode fix**
```
User: "Dark mode looks terrible"
Claude: [Uses visual-polish-checklist] Identifies issues:
- Pure black background replaced with gray-900
- Elevation uses lighter surface colors instead of shadows
- Brand accent color adjusted for dark background contrast
- Text meets WCAG AA 4.5:1 ratio
```

## Shadow and Depth

Use layered shadows (shadow + ring) for professional depth:

```html
<button class="
  rounded-md bg-blue-600 px-4 py-2 text-white
  shadow-md ring-2 ring-blue-400 ring-offset-2 ring-offset-white
  transition-all duration-300
  hover:shadow-lg hover:scale-105 hover:bg-blue-500
  focus:outline-none focus:ring-4
">
  Elevated Action
</button>
```

- `ring` alongside `shadow` creates multi-layered depth
- Hover: increase shadow intensity AND add slight scale for physical lift
- Use `ring-offset` for sharp separation between layers

## Gradient Quality

Avoid muddy gradient midpoints caused by standard RGB interpolation.

- Use OKLCH or OKLAB color spaces for perceptually uniform gradients
- Tailwind v4 defaults to OKLCH interpolation
- Use gradients for atmosphere (glassmorphism), not flat replacement

## Typography Refinements

| Element | Property | Value | Why |
|---|---|---|---|
| Body text | line-height | 1.5 (leading-normal) | Readability |
| Headings | line-height | 1.125-1.25 (leading-tight) | Prevents disjointed large text |
| Small/Caps text | letter-spacing | tracking-wide | Improves legibility |
| Large headings | letter-spacing | tracking-tight | Feels cohesive and punchy |
| Hierarchy | Weight contrast | 800 vs 400 | Clear visual distinction |
| Hierarchy | Size jumps | 3x between levels | Strong differentiation |

Limit typography hierarchy to 3 levels: Title, Subtitle, Body.

## Spacing Rhythm

Use the power-of-2 pattern (4, 8, 16, 32, 64px):

```html
<!-- Outer (64px), Section (32px), Internal (8px) -->
<div class="p-16 space-y-8">
  <section class="space-y-2">
    <h2 class="text-3xl font-bold tracking-tight text-gray-900">
      Project Overview
    </h2>
    <p class="text-base leading-relaxed text-gray-600 max-w-prose">
      Description with relaxed line height for readability.
    </p>
  </section>

  <div class="flex gap-4">
    <button class="px-4 py-2 bg-black text-white rounded">Primary</button>
    <button class="px-4 py-2 bg-gray-100 text-gray-900 rounded">
      Secondary
    </button>
  </div>
</div>
```

Group related elements closely (4-8px). Separate sections generously (32-64px).

## Border Treatments

| Type | Layout Impact | Use Case |
|---|---|---|
| border | Affects box model size | Structural edges (cards, inputs) |
| outline | No layout impact | Focus states (prevents layout jank) |
| ring | No layout impact (box-shadow based) | Decorative focus rings, stacking borders |

Modern browsers support `border-radius` on outlines.

## Dark Mode Correctness

1. **No pure black**: Use `gray-900` for backgrounds, not `#000`
2. **Elevation via lightness**: Lighter surfaces = higher elevation (shadows are invisible on dark)
3. **Semantic tokens**: `color.bg.canvas` maps to white (light) and gray-900 (dark)
4. **Contrast adjustment**: Bright brand colors may need desaturation for dark backgrounds
5. **WCAG AA**: Text must meet 4.5:1 contrast ratio in both modes

## Loading States

### Skeleton Screens
Use for primary structural components only. Match final content layout to prevent shifts.

### Staggered Content Reveal
When content loads, stagger the reveal (Text then Image then Button) for a polished entrance.

### Optimistic UI
For micro-interactions (like toggling), update UI immediately before server response. Use a subtle scale animation to mask latency.

**Scope boundaries:**
- For **animation/video project critique** (composition, pacing, color grading), use `creative-director` instead.
- For **prompting strategies** before generating UI, use `prompting-beautiful-ui` instead.
- This skill focuses on **reviewing and polishing already-generated web UI code**.

## Self-Review Checklist

Run this after generating any UI component:

- [ ] Token usage: Are all colors/spacings using tokens, not hardcoded values?
- [ ] Interaction states: Do all interactive elements have hover, focus, and active states?
- [ ] Focus visibility: Is the focus indicator visible and high-contrast (3:1 minimum)?
- [ ] Dark mode depth: Does UI use shadows for depth? Add borders or lightness changes for dark mode
- [ ] Typography: Are line heights relative (unitless) to handle zooming?
- [ ] Spacing: Does spacing follow the 4px grid consistently?
- [ ] Loading: Are skeleton loaders present for async data?
- [ ] Gradients: Are gradient midpoints clean (not muddy)?
- [ ] Borders: Are card edges defined with subtle borders or rings?

## AI-Assisted Review Prompts

Use these prompts to audit generated code:

```
"Extract all colors, fonts, and spacing from this component. Flag any
hardcoded values that deviate from the standard 8pt spacing scale."
```

```
"Review this UI for 'AI slop' aesthetics. Identify generic font choices
or predictable layout patterns and suggest distinct alternatives."
```

```
"Simulate a screen reader traversing this form. Are the focus states
visible and is the tab order logical?"
```

## Success Criteria

- [ ] Shadows use layered approach (shadow + ring), not single shadow
- [ ] Typography uses tight line-height for headings, relaxed for body
- [ ] Spacing follows consistent power-of-2 scale
- [ ] Dark mode uses lightness for elevation, not just shadows
- [ ] All async content has skeleton or loading state
- [ ] Self-review checklist passes on every generated component

## Copy/Paste Ready

```
"Polish this component - run the visual quality checklist"
"Make this look premium, not generic"
"Fix the dark mode - shadows are invisible"
"Add loading states to this data-driven component"
"Review this UI for polish gaps and spacing inconsistencies"
```
