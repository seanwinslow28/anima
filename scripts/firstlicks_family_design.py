#!/usr/bin/env python3
"""FIRST LICKS host family — Art Dept look-test batch (Sean-authorized, gpt-image/Higgsfield).

2026-07-19 Artie session (runs/2026-07-19-first-licks-artdept/artdept-session.md).
Locks: L4 round family · L7 dad = Fieri×Goodman · L9 Brittany = Mini-Fieri candy-bling
· L10 mom = dusty-rose hostess. Dependency map: dad anchor (fresh, style-seeded off the
ratified kid anchor) → Brittany (EDIT of dad — family gene by construction) → mom (EDIT)
→ lineup (COMPOSITE). Run per-preset:

    python scripts/firstlicks_family_design.py dad
    python scripts/firstlicks_family_design.py brittany
    python scripts/firstlicks_family_design.py mom
    python scripts/firstlicks_family_design.py lineup
"""
import sys
from pathlib import Path

from pipeline.agents.nb_pro_runner import invoke_image_edit

RUN = Path("runs/2026-07-19-first-licks-artdept")
STYLE_SEED = Path(
    "runs/2026-07-14-grandmaster-kid-design/Manually-Tinkered-Pass/primal grit/kid-wimpy-anchor.png"
)
DAD = RUN / "dad-y1-anchor.png"
BRITTANY = RUN / "brittany-y1-anchor.png"
MOM = RUN / "mom-anchor.png"

PRIMAL = (
    "Raw hand-drawn register of Genndy Tartakovsky's Primal: visible weight-varying ink "
    "linework, gritty painterly texture, warm earthy desaturated palette."
)
PLATE = (
    "Full-body character design plate: flat even daylight, plain neutral background, "
    "whole figure visible head to feet. "
)

PRESETS = {
    "dad": {
        "sources": [STYLE_SEED],
        "out": DAD,
        "prompt": (
            "COMPLETELY REPLACE THE SUBJECT of the reference image: do NOT depict the boy — "
            "keep ONLY the reference's art-style and rendering treatment. " + PLATE +
            "Depict a hulking ROUND suburban dad in his early forties — a wall of soft heavy "
            "mass, not muscle: big round gut, thick neck, top-heavy bulk on smallish feet; from "
            "a kid's height he blocks the light. Face: doughy round jowly baby-faced cheeks, a "
            "vain smolder, one heavy low brow over small close-set eyes, a groomed horseshoe "
            "mustache, and a feathered dirty-blond 1970s swept hairdo. Outfit: black bowling "
            "shirt with red-orange flame print, khaki cargo shorts, chunky skate shoes, chunky "
            "silver rings, orange-tinted wraparound sunglasses parked BACKWARDS on the back of "
            "his head, a foam beer koozie in one hand. Smug self-appointed master-of-ceremonies "
            "energy; cruelty-from-entitlement in the brow, never cartoon-villain scowling. "
            + PRIMAL + " No text, no watermark."
        ),
    },
    "brittany": {
        "sources": [DAD],
        "out": BRITTANY,
        "prompt": (
            "Image 1 is the art-style AND family-identity reference (her father). Keep the "
            "exact art style and rendering treatment unchanged. " + PLATE +
            "Depict his EIGHT-YEAR-OLD DAUGHTER — unmistakable family resemblance: the same "
            "blond gene (bouncy blonde ringlets), the same small close-set eyes, round "
            "cherub-cute cheeks, a tiny mean chin, big doll eyes with a sly half-lidded smirk. "
            "Round-cute silhouette. Outfit: a custom bubblegum-pink party dress printed with "
            "FLAMES (a kid-party echo of her father's flame shirt), a candy necklace worn like "
            "jewelry, one ring pop worn proudly like a chunky ring, tiny sunglasses parked on "
            "the back of her ringlets exactly like her father's, frilly white socks and shiny "
            "mary-jane shoes. Cute FIRST, sly on the second look — never a scowling brat. "
            "No text, no watermark."
        ),
    },
    "mom": {
        "sources": [BRITTANY, DAD],
        "out": MOM,
        "prompt": (
            "Image 1 (the daughter) and image 2 (the father) are the art-style and "
            "family-identity references. Keep the exact art style and rendering treatment "
            "unchanged. " + PLATE +
            "Depict the MOTHER of this family — the daughter grown up: blonde salon blowout, "
            "the family's close-set eyes, a curated perma-hostess smile that does not reach "
            "them. Outfit: dusty-rose velour athleisure tracksuit, chunky gold hoop earrings, "
            "white wedge sneakers, sunglasses worn ON TOP of her head like a headband. She "
            "holds a store-bought sheet cake, rotating it to its good side. "
            "No text, no watermark."
        ),
    },
    "room": {
        "sources": [
            Path(
                "runs/2026-07-14-grandmaster-kid-design/Manually-Tinkered-Pass/primal grit/scene-wide-no-kids.png"
            )
        ],
        "out": RUN / "grandma-room-wide.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "COMPLETELY REPLACE THE SCENE of the reference image — keep ONLY its art-style "
            "and rendering treatment. One wide 16:9 interior BACKGROUND layout for 2D "
            "animation, seen from the doorway: the small bedroom of a departed grandmother "
            "who secretly loved kung-fu cinema. ANIMATION BACKGROUND DISCIPLINE: the room "
            "reads as a few big grouped value masses with decisive edges; detail is "
            "suggestion, not rendering — a handful of counted accents only; large quiet "
            "areas of wall and floor; the middle of the floor stays OPEN and empty, a clear "
            "light-valued playing space where characters will stand and read in stark value "
            "contrast against the ground. MOVIE-NIGHT GEOMETRY: the small CRT television "
            "with VCR sits against one wall, and facing it across the open floor are the "
            "two seats of their ritual — her worn armchair and the foot of the neatly made "
            "bed side by side, both aimed at the TV. Counted accents (keep to these): two "
            "or three wordless kung-fu movie posters, one shelf of VHS tapes, the old "
            "boombox near the TV, a ring of small Polaroids around the dresser mirror, a "
            "hand-knit blanket on the bed. Dim, curtains drawn, ONE hard-edged shaft of "
            "late light painted as its own flat lighter-value shape falling across the open "
            "floor. No people. Palette drained toward the desaturated end of a warm earthy "
            "range — a room where the color left with her. Quiet, held, reverent. "
            + PRIMAL + " No text, no watermark."
        ),
    },
    "yard": {
        "sources": [
            Path(
                "runs/2026-07-14-grandmaster-kid-design/Manually-Tinkered-Pass/primal grit/scene-wide-no-kids.png"
            )
        ],
        "out": RUN / "yard-master-wide.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "COMPLETELY REPLACE THE SCENE of the reference image — keep ONLY its art-style "
            "and rendering treatment. One wide 16:9 exterior BACKGROUND layout for 2D "
            "animation: a suburban backyard staged for a little girl's birthday party, "
            "dawn, empty, no people. ANIMATION BACKGROUND DISCIPLINE: big grouped value "
            "masses with decisive edges, texture INSIDE the masses only; large quiet lawn "
            "and sky areas; the center foreground lawn stays OPEN as the characters' "
            "playing space; detail as a few counted accents, suggestion not rendering. THE "
            "LANDMARK: one large backyard tree, off-center on a low horizon, a striped "
            "pinata hanging from its branch on a long string — the yard's sacred object. "
            "THE FIXTURE GRID (the repeatable accents that make this yard instantly "
            "recognizable): a row of folding tables with paper tablecloths, a string of "
            "party lights between two poles, a fence line with a gate. Everything looks "
            "expensive but slightly off-brand — bootleg maximalism, maximum spend minimum "
            "taste. Dawn palette: one flat unnatural sky color as the scene's emotional "
            "key (pale ochre, never plain blue), long soft shadows as hard-edged darker "
            "shapes. Quiet, mythic, before the world wakes. "
            + PRIMAL + " No text, no watermark."
        ),
    },
    "lineup": {
        "sources": [DAD, BRITTANY, MOM],
        "out": RUN / "family-lineup.png",
        "prompt": (
            "Images 1-3 are the father, daughter, and mother — keep each character's exact "
            "design, outfit, proportions, and the shared art style unchanged. One wide "
            "full-body lineup plate of the three standing together on a plain neutral "
            "background, flat even daylight: the huge round father in the middle, daughter in "
            "front of him, mother beside — one family, one product line, the resemblance "
            "reading at silhouette scale. No text, no watermark."
        ),
    },
}


def main() -> int:
    which = sys.argv[1]
    spec = PRESETS[which]
    RUN.mkdir(parents=True, exist_ok=True)
    print(f"[{which}] sources={[str(s) for s in spec['sources']]} -> {spec['out']}")
    resp = invoke_image_edit(
        prompt=spec["prompt"],
        reference_images=spec["sources"],
        output_path=spec["out"],
        cache_dir=RUN / ".cache",
        model="gpt-image-2",
        aspect_ratio=spec.get("aspect_ratio"),
        timeout_s=600,
    )
    out = spec["out"]
    print(f"[{which}] ok={getattr(resp, 'ok', None)} exit={getattr(resp, 'exit_code', None)} "
          f"job={getattr(resp, 'job_id', None)} size={out.stat().st_size if out.exists() else 0}")
    return 0 if getattr(resp, "ok", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
