# Sean-anchor — character turnaround sheet prompts (2D Disney pencil-test register)

*For Google Flow / Nano Banana 2. Attach `characters/sean-anchor/anchor.png` as the reference (Image 1). Restyled from Sean's proven turnaround prompt: SFII/pixel aesthetic → pencil-test-colored register, anchor identity markers enumerated, 1:7 proportion lock added.*

*2026-06-03 update: the combined body+portrait layout overcrowded and fought the height lock. **Split into two sheets** — one full-body turnaround (carries the 1:7 proportion + views), one head turnaround (carries face/construction/shading + expression variety). This also matches the two-track eval corpus: full-body track for proportion + view-correctness, head track for the style/identity classes.*

---

## Sheet A — Full-body turnaround (the proportion + view source)

Create a professional full-body character model turnaround sheet based strictly on the uploaded reference image (Image 1 — the canonical identity anchor). Use a warm cream animation-paper background with subtle paper grain and faint hole-punch production marks along one edge, and present the sheet as a technical model turnaround while matching the exact visual style of the reference: a 2D Disney-style hand-drawn animation **pencil test** aesthetic — soft graphite pencil linework with light construction lines still visible beneath the final line (NOT bold vector or ink outlines), a light hand-painted color wash and flat marker-style fills over the pencil, gentle cross-hatch and pencil shading rather than hard cel bands, soft top-front lighting, and the loose, confident line quality of a Disney clean-up / color-key drawing.

Match the face, hairstyle, full color palette, and proportions of Image 1 exactly: sandy-blonde tousled hair with a center cowlick at the crown, an angular jawline, light stubble, blue eyes, light skin, and a slim athletic build; navy-blue crew-neck t-shirt, gray slim cuffed jeans, and gray low-top sneakers. Maintain perfect identity consistency across every panel.

Arrange **one horizontal row of five full-body standing views**, evenly spaced and side-by-side, in this order: front view, three-quarter front view (turned slightly toward camera-left), left profile (facing left), right profile (facing right), back view.

Keep the subject in a relaxed A-pose with the arms held slightly away from the body and the hands relaxed, with consistent scale and alignment between views, accurate anatomy, and a clear silhouette. The figure must be drawn at realistic adult proportions of approximately **seven heads tall (a 1:7 head-to-body ratio)** — NOT stylized, chibi, or shortened — and this proportion must be identical across all five views (the same head height and the same seven-head ladder from front, three-quarter, profile, and back). Ensure even spacing, clean panel separation, uniform framing, and a consistent head height and ground line across the entire lineup.

Lighting should be consistent across all panels (the same soft top-front lighting, intensity, and softness), with natural, controlled pencil shading that preserves detail without dramatic mood shifts.

Output a clean, print-ready animation model sheet: graphite line (not flat vector black), keeping the warm cream paper and the full hand-drawn color palette of Image 1. No photographic or 3D rendering, no glossy digital shading, no anime cel-vector look, no pixel art. Do not render any text, labels, captions, panel titles, or watermarks.

*Revert option: if five views crowd, drop the three-quarter and run four (front, left profile, right profile, back) — your originally-proven count.*

---

## Sheet B — Head turnaround (the face / construction / expression source)

Create a professional head-and-shoulders character turnaround sheet based strictly on the uploaded reference image (Image 1 — the canonical identity anchor). Use a warm cream animation-paper background with subtle paper grain and faint hole-punch production marks along one edge, and match the exact visual style of the reference: a 2D Disney-style hand-drawn animation **pencil test** aesthetic — soft graphite pencil linework with light construction lines still visible beneath the final line (NOT bold vector or ink outlines), a light hand-painted color wash and flat marker-style fills over the pencil, gentle cross-hatch and pencil shading rather than hard cel bands, soft top-front lighting, and the loose, confident line quality of a Disney clean-up / color-key drawing.

Match the face, hairstyle, and color palette of Image 1 exactly: sandy-blonde tousled hair with a center cowlick at the crown, an angular jawline, light stubble, blue eyes, light skin, and the navy crew-neck collar. Maintain perfect identity consistency across every panel.

Arrange **one horizontal row of five head-and-shoulders portraits**, evenly spaced and side-by-side, in this order: front, three-quarter front (turned slightly toward camera-left), left profile (facing left), right profile (facing right), back of head. Crop each consistently at mid-chest so the head fills the same proportion of every panel.

Keep a neutral, relaxed expression across all panels, with consistent facial scale, the same head height, and the same eye line across the row. Show the construction of the head clearly — the faint cross-contour and centerline beneath the final drawing — as a clean-up animator would. Lighting should be consistent across all panels (the same soft top-front lighting, intensity, and softness).

Output a clean, print-ready animation model sheet: graphite line (not flat vector black), keeping the warm cream paper and the full hand-drawn color palette of Image 1. No photographic or 3D rendering, no glossy digital shading, no anime cel-vector look, no pixel art. Do not render any text, labels, captions, panel titles, or watermarks.

---

## Notes

- **Proportion lock (Sheet A) is the load-bearing clause** — this sheet is the A4 gold-standard source, and the whole reset exists because proportion drifted to ~1:4–1:5.3 in the old Bible. Eyeball the result against a seven-head ladder before trusting it. If NB2 keeps fighting the ratio, that's the signal we need the SF03 armature-underlay to *force* it rather than ask.
- **Stylus omitted** from both sheets — it's a pose-level prop added per-pose downstream; keeps the back/profile panels clean. Say the word to hold it in the right hand on the front views.
- **Two sheets = the two corpus tracks.** Sheet A feeds proportion + view-correctness fixtures; Sheet B feeds construction-lines + shading-register + palette + expression fixtures. Once both are trusted, they become the reference set the per-pose clean/defect prompts edit against.
