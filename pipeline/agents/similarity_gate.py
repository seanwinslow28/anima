"""anima — Cy's Pass-2.5 pixel-similarity gate.

The visual-fidelity post-mortem (§2.3) named the load-bearing finding: Gemini's
Pass-3 grounds its verdict against the IR.* rule *descriptions* Cy wrote —
prose — not against the source-ref *pixels*. A drifted plate that nominally
satisfies "jaw angular, eyes one eye-width apart" passes, because the wrong
face also has those markers. The prose pass is structurally blind to "looks
like a different character who happens to have those markers."

This module closes that blind spot with a numeric, pixel-grounded similarity
score computed BEFORE the prose pass fires. It does not *fix* drift — it
surfaces it loudly, so the score sits in the persisted per-plate verdict trail
next to Gemini's prose verdict. A plate that Gemini passes but that scores low
on pixels is now visible after the fact.

# The method ladder

Identity similarity is best measured with a learned embedding. Preference order
(post-mortem §5 item 3): DINOv2 (best for identity) > CLIP > a structural
fallback. DINOv2/CLIP need torch + a model download — heavy deps anima does not
require. So the ladder degrades gracefully:

  1. DINOv2 cosine  — if `torch` + `transformers` import.
  2. CLIP cosine    — if `torch` + `open_clip` import.
  3. PIL-perceptual — always available (Pillow only). A color-histogram cosine
     blended with a grayscale structural correlation. Coarse, but it reliably
     catches the SEVERE drift the post-mortem documented — a full-color cartoon
     rendered as monochrome graphite, or a tiny octopus rendered as a chibi
     humanoid — because those collapse the color histogram and gross structure.

To upgrade the gate to DINOv2, `pip install torch transformers` — no code
change; the ladder picks it up.

# Why the threshold is a flag, not a hard block (this commit)

The PIL-perceptual metric is angle-sensitive: a faithful back-of-head plate
compared against a front-facing anchor scores low for legitimate reasons. Hard-
rejecting on it would false-reject correct non-front views. So in this commit
the gate COMPUTES and PERSISTS the score and FLAGS below-threshold plates in
the verdict trail, but does not short-circuit Gemini — both signals get
recorded. Hard-reject-before-Pass-3 becomes safe once the embedding tier
(DINOv2, angle-robust) is the active method; the flag is wired so that promotion
is a threshold/config change, not a rewrite.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

# Below this score the plate is flagged `similarity_below_threshold` in its
# verdict. Deliberately lenient on the coarse PIL metric — it should fire on
# severe palette/structure collapse (the documented drift), not on minor
# angle/pose differences. Tighten when the DINOv2 tier is active.
SIMILARITY_FLAG_THRESHOLD = 0.5

# Working resolution for the PIL-perceptual metric. Small enough to be fast,
# large enough that gross structure survives the downscale.
_PIL_SIZE = 96


@dataclass(frozen=True)
class SimilarityResult:
    """One similarity measurement between a plate and a reference.

    - score: 0.0 (unrelated) .. 1.0 (identical), method-normalized.
    - method: which ladder rung produced it ('dinov2' | 'clip' | 'pil-perceptual').
    - reference: the reference path the plate was scored against.
    """

    score: float
    method: str
    reference: str

    @property
    def below_threshold(self) -> bool:
        return self.score < SIMILARITY_FLAG_THRESHOLD


def compute_similarity(plate_path, reference_path) -> SimilarityResult:
    """Score how much `plate_path` looks like `reference_path`.

    Walks the method ladder top-down, using the first tier whose deps import.
    The PIL-perceptual tier always succeeds, so this never raises for a
    missing-dependency reason.
    """
    plate_path = Path(plate_path)
    reference_path = Path(reference_path)

    score = _dinov2_similarity(plate_path, reference_path)
    if score is not None:
        return SimilarityResult(score, "dinov2", str(reference_path))

    score = _clip_similarity(plate_path, reference_path)
    if score is not None:
        return SimilarityResult(score, "clip", str(reference_path))

    score = _pil_similarity(plate_path, reference_path)
    return SimilarityResult(score, "pil-perceptual", str(reference_path))


# ----- ladder tier 1: DINOv2 -----


def _dinov2_similarity(plate: Path, reference: Path) -> float | None:
    """Cosine of DINOv2 [CLS] embeddings. None if torch/transformers absent."""
    try:
        import torch  # noqa: F401
        from transformers import AutoImageProcessor, AutoModel
    except ImportError:
        return None
    try:
        import torch
        model_id = "facebook/dinov2-small"
        processor = AutoImageProcessor.from_pretrained(model_id)
        model = AutoModel.from_pretrained(model_id)
        model.eval()
        embs = []
        for p in (plate, reference):
            img = Image.open(p).convert("RGB")
            inputs = processor(images=img, return_tensors="pt")
            with torch.no_grad():
                out = model(**inputs)
            embs.append(out.last_hidden_state[:, 0, :].squeeze(0))
        cos = torch.nn.functional.cosine_similarity(embs[0], embs[1], dim=0).item()
        return max(0.0, min(1.0, (cos + 1.0) / 2.0))
    except Exception:
        # A model-download/runtime failure should fall through to the next
        # tier, not crash a Bible bake.
        return None


# ----- ladder tier 2: CLIP -----


def _clip_similarity(plate: Path, reference: Path) -> float | None:
    """Cosine of CLIP image embeddings. None if torch/open_clip absent."""
    try:
        import torch
        import open_clip
    except ImportError:
        return None
    try:
        model, _, preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained="openai"
        )
        model.eval()
        feats = []
        for p in (plate, reference):
            img = preprocess(Image.open(p).convert("RGB")).unsqueeze(0)
            with torch.no_grad():
                f = model.encode_image(img)
            f = f / f.norm(dim=-1, keepdim=True)
            feats.append(f.squeeze(0))
        cos = torch.dot(feats[0], feats[1]).item()
        return max(0.0, min(1.0, (cos + 1.0) / 2.0))
    except Exception:
        return None


# ----- ladder tier 3: PIL-perceptual (always available) -----


def _pil_similarity(plate: Path, reference: Path) -> float:
    """Color-histogram cosine blended with grayscale structural correlation.

    Color is weighted higher than structure: palette is the strongest identity
    signal and is angle-robust (the same character at any angle shares its
    palette), while structure is angle-sensitive. The monochrome-vs-color and
    palette-collapse drift the post-mortem documented live mostly in the color
    term.
    """
    a = Image.open(plate).convert("RGB").resize((_PIL_SIZE, _PIL_SIZE))
    b = Image.open(reference).convert("RGB").resize((_PIL_SIZE, _PIL_SIZE))

    color = _cosine(a.histogram(), b.histogram())

    ga = list(a.convert("L").tobytes())
    gb = list(b.convert("L").tobytes())
    struct01 = (_pearson(ga, gb) + 1.0) / 2.0

    score = 0.6 * color + 0.4 * struct01
    return max(0.0, min(1.0, score))


def _cosine(u: list[float], v: list[float]) -> float:
    dot = sum(a * b for a, b in zip(u, v))
    nu = math.sqrt(sum(a * a for a in u))
    nv = math.sqrt(sum(b * b for b in v))
    if nu == 0.0 or nv == 0.0:
        return 0.0
    return dot / (nu * nv)


def _pearson(u: list[float], v: list[float]) -> float:
    n = len(u)
    if n == 0:
        return 0.0
    mu = sum(u) / n
    mv = sum(v) / n
    cov = sum((a - mu) * (b - mv) for a, b in zip(u, v))
    du = math.sqrt(sum((a - mu) ** 2 for a in u))
    dv = math.sqrt(sum((b - mv) ** 2 for b in v))
    if du == 0.0 or dv == 0.0:
        # At least one image is a flat field — correlation is undefined.
        # If BOTH are flat, structure reduces to whether the luma means match
        # (identical solids correlate; two different solids do not). If only
        # one is flat, there is no shared structure to correlate.
        if du == 0.0 and dv == 0.0:
            return 1.0 if abs(mu - mv) < 1.0 else -1.0
        return 0.0
    return cov / (du * dv)
