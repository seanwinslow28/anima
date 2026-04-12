# Procreate Sprite Extraction Guide

**Purpose:** Extract the seated sprite asset with a transparent background for compositing in the animation pipeline. This is the manual prerequisite before Claude Code can run the compositing script.

**Time estimate:** 15-20 minutes
**Output:** 1 RGBA PNG file with clean transparency

---

## What You're Producing

| Asset | Source File | What to Extract | Output Path |
|-------|------------|-----------------|-------------|
| Seated sprite | `candidates/sprite/seated_sprite_01.png` | The full sprite character (seated pose, S-2 label) | `candidates/sprite/sprite_seated_alpha.png` |

**Why only one asset:** F28 already has the sprite baked in and we keep that keyframe as-is. We only composite the sprite onto the new Sean-only in-between frames (mid-flight) and the fade frames (F38-F39). At 12fps, the flight frames are on screen for ~0.17s each — the seated pose reads fine for a sprite in rapid motion. No bounce-pose extraction needed.

---

## Recommended Method: Mask Trick (Lineart Extraction)

This is the best technique for pencil-on-paper because it uses luminosity to separate dark lines from the light paper — preserving soft pencil edges that automatic selection would clip.

### Extraction 1: Seated Sprite (easier — start here)

The seated sprite (`seated_sprite_01.png`) is a clean, large drawing on cream paper. This is the easier extraction to practice the technique on.

**Step 1 — Import and crop**
1. Create a new canvas in Procreate at **1376x768** (the pipeline's frame resolution). This ensures the sprite will be at the correct scale relative to the animation frames.
2. Import `candidates/sprite/seated_sprite_01.png` (Actions > Add > Insert a Photo)
3. The sprite image is 896x1200 (portrait). You'll need to scale it down significantly — the sprite on Sean's shoulder in F31 is roughly **80px tall**. Pinch to scale the sprite to approximately that size. Position it in the center of the canvas for now.
4. Flatten the import to a single layer if needed.

**Step 2 — Increase contrast**
1. Tap Adjustments (magic wand icon) > **Curves**
2. Pull the **highlights** (top-right of the curve) up toward pure white — this pushes the cream paper toward white
3. Pull the **shadows** (bottom-left of the curve) down toward pure black — this darkens the pencil lines
4. Goal: maximize the difference between paper and linework without losing pencil texture detail. The paper should be near-white, the lines should be dark gray to black.
5. Tap the canvas to apply.

**Step 3 — The mask trick**
1. Open the Layers panel. Tap on the sprite layer to open the layer menu.
2. Tap **Copy** (this copies the layer contents to the clipboard).
3. Tap the same layer again and tap **Mask**. A white mask appears above the layer.
4. Tap the **Mask** thumbnail to select it (it should be highlighted).
5. Three-finger swipe down on the canvas > select **Paste**. This pastes the sprite image into the mask.
6. With the mask still selected, tap Adjustments > **Invert**. Now the mask uses luminosity: dark lines = visible, light paper = transparent.
7. Pinch the mask and the layer together to **Merge** them (or tap the layer > Merge Down / Flatten with Mask).

**Step 4 — Clean up**
1. You should now see the sprite's pencil lines on a checkerboard (transparent) background.
2. Zoom in and check the edges. You may see faint paper-colored fringe around the outer edges.
3. Use the **Eraser tool** with a soft brush at low opacity (20-30%) to gently clean up any remaining fringe. Work around the silhouette edge only — don't erase into the sprite's body.
4. Check the "S-2 IDLE SEATED" production label and the hole-punch marks — erase these too (they're paper elements, not part of the sprite).
5. Erase the ledge/line the sprite is sitting on unless you want it as part of the asset.

**Step 5 — Export**
1. Make sure the **background layer is hidden** (tap the checkmark next to the Background Color layer to hide it). You should see a checkerboard behind the sprite.
2. Actions (wrench) > Share > **PNG**
3. Save as `sprite_seated_alpha.png`
4. Transfer to your Mac and place at: `runs/run_2026-04-04_174805/candidates/sprite/sprite_seated_alpha.png`

---

## Quality Checklist Before Leaving Procreate

Verify:

- [ ] **Transparent background** — checkerboard visible, no cream/white background remaining
- [ ] **Clean edges** — no paper-colored halo around the silhouette
- [ ] **Pencil texture preserved** — lines still have graphite quality, not over-processed to solid black
- [ ] **No stray elements** — production labels, hole-punch marks, Sean's body parts, pencil trails all removed
- [ ] **Correct file format** — PNG (not JPEG, not PSD)
- [ ] **Reasonable file size** — should be under 500KB each

---

## Tips and Gotchas

1. **Start with the seated sprite.** It's larger, cleaner, and on its own sheet — much easier to extract. Get comfortable with the mask trick on this one first.

2. **The Curves step is critical.** If you skip the contrast increase, the mask trick will leave heavy paper-colored fringe because the cream and pencil tones are too close in luminosity. Push the highlights hard.

3. **Don't over-clean.** Some paper grain showing through the pencil lines is desirable — it helps the sprite blend with the paper-textured animation frames. If the sprite looks like crisp digital vector art, you've over-processed.

4. **If the mask trick doesn't work well** on the bounce sprite (because it's so small), fall back to **Freehand Selection**:
   - Selection tool > Freehand mode
   - Trace around the sprite outline
   - Add 1-2px feather (tap Feather at the bottom of the selection bar)
   - Copy, paste to new layer, hide/delete original
   - Clean edges with eraser

5. **Canvas size matters.** Export at the size you extracted at — the compositing script handles all resizing. Don't upscale in Procreate.

6. **Save a .procreate file too** (in addition to the PNG export). If we need to re-extract with different settings, you won't have to redo the manual cleanup.

---

## YouTube Search Terms

Search these exact phrases to find video walkthroughs of the techniques used above:

| Search Term | What It Covers |
|-------------|---------------|
| `Procreate mask trick lineart transparent background` | The core extraction technique (Steps 2-3) |
| `Procreate separate lineart from paper background` | Alternative approaches to the same problem |
| `Procreate extract scanned drawing transparent PNG` | End-to-end workflow for scanned pencil art |
| `Procreate curves contrast pencil sketch` | The contrast prep step specifically |
| `Procreate remove background keep linework` | General background removal preserving lines |

**Recommended channels:** Bardot Brush, Art with Flo, Brad Colbow, RetroSupply Co — all have Procreate deep-dive tutorials.

---

## Reference Links

- [Procreate Official: Crop and Remove Background](https://help.procreate.com/articles/JCLHGT-crop-and-remove-background)
- [Procreate Handbook: Masks](https://help.procreate.com/procreate/handbook/layers/layers-mask)
- [RetroSupply: How to Draw Using Masks in Procreate](https://www.retrosupply.co/blogs/tutorials/masks-and-channels-in-procreate)
- [Procreate Forum: Scanned lineart to transparent](https://folio.procreate.com/discussions/5/17/18925)
- [Procreate Forum: Separate linework from background](https://folio.procreate.com/discussions/5/17/28121)
- [Homeostasis Lab: Mastering Line Art Extraction in Procreate](https://www.homeostasislab.com/mastering-line-art-extraction-in-procreate/)
- [21 Draw: How to Remove Background in Procreate](https://www.21-draw.com/how-to-remove-background-in-procreate/)
- [Artsydee: 3 Easy Methods to Remove Background](https://www.artsydee.com/how-to-remove-background-in-procreate/)

---

## After Extraction

Once the PNG is in place at:
- `runs/run_2026-04-04_174805/candidates/sprite/sprite_seated_alpha.png`

Tell Claude Code: **"Sprite asset is extracted and ready. Execute Phase 4 compositing plan."**

Claude Code will then run Steps 1-4 from `docs/phase4-compositing-plan.md` autonomously.
