#!/usr/bin/env python3
"""Register A/B style-swap: cartoon-pushed Primal vs samurai-jack-s5 (Sean-authorized).

Pure style transfer — keeps subjects/faces/composition, changes ONLY the render — so
Sean can judge the register on any source. Settles 'too photoreal' + the piece register.

    python scripts/grandma_register_test.py primal_cartoon <source.png>
    python scripts/grandma_register_test.py jack <source.png>
    # default source = the young-warrior reveal
"""
import sys
from pathlib import Path

from pipeline.agents.nb_pro_runner import invoke_image_edit
from pipeline.registers import get_register

RUN = Path("runs/2026-07-14-grandmaster-kid-design")
JACK = get_register("samurai-jack-s5")

KEEP = (
    "Re-render this exact image — keep the SAME subjects, faces, identities, poses, "
    "expressions, and composition, and keep the faded old-photo border. Change ONLY the "
    "rendering STYLE. "
)
CARTOON = (
    "It must read as a STYLIZED 2D HAND-DRAWN ANIMATED CARTOON — a frame from an animated "
    "film. NOT photorealistic, NOT a rendered 3D image, NOT a real photograph, NOT a "
    "realistic painting. Simplified stylized cartoon features, confident cartoon linework, "
    "flat cartoon shading, clearly a drawing. "
)
ETHNIC = "Keep the people ethnically ambiguous / mixed — not specifically East Asian. "

PRESETS = {
    "primal_cartoon": (
        KEEP + CARTOON + "Keep raw hand-inked Primal grit (visible ink line, gritty "
        "texture, warm earthy desaturated palette) but push it fully into animated-cartoon "
        "territory — cartoon, not realism. " + ETHNIC + "No text, no watermark."
    ),
    "jack": (
        KEEP + "New style — a flat cinematic 2D poster-art cartoon register: "
        + JACK.style_token + " " + JACK.preserve + " " + CARTOON + ETHNIC
        + "No text, no watermark."
    ),
}


def main() -> int:
    which = sys.argv[1]
    src = Path(sys.argv[2]) if len(sys.argv) > 2 else RUN / "grandma-young-warrior.png"
    tag = src.stem
    out = RUN / f"register-{which}--{tag}.png"
    print(f"[{which}] {src} -> {out}")
    resp = invoke_image_edit(
        prompt=PRESETS[which],
        reference_images=[src],
        output_path=out,
        cache_dir=RUN / ".cache",
        model="gpt-image-2",
        aspect_ratio=None,
        timeout_s=600,
    )
    print(f"[{which}] ok={getattr(resp, 'ok', None)} job={getattr(resp, 'job_id', None)} "
          f"size={out.stat().st_size if out.exists() else 0}")
    return 0 if getattr(resp, "ok", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
