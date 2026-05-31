# Plate — expressions/neutral.png

- kind: plate_verdict
- outcome: human_gate_required
- decided by: cy
- date: 2026-05-29
- pil-perceptual similarity: 1.0
- evidence: rich

## Rationale

The plate 'expressions/neutral.png' is identical to the canonical anchor reference 'anchor.png', which is a high-resolution sketch drawn in the pencil-test-colored register on textured cream paper. Because the cited identity rules define a strict 'pixel-art-8bit' register, the plate completely fails to honor them: (1) 'IR.claude-mascot.palette.four-indexed-color-vocabulary' is violated: the plate features 8,987 unique colors (pencil shading and paper texture) and contains 0 primary orange (#E89B6B), 0 cream highlight (#F4DDB8), and 0 deep brown (#5C3A24) pixels within tolerance. (2) 'IR.claude-mascot.style.integer-pixel-grid-no-subpixel' is violated: contours are sketchy lines rather than integer grid runs. (3) 'IR.claude-mascot.face.eye-deep-brown-dot-cluster' and 'IR.claude-mascot.face.mouth-line-deep-brown-single-stroke' are violated: the eyes and mouth are sketchy pencil marks, not deep brown pixel clusters or a single clean stroke. (4) 'IR.claude-mascot.face.expression-vocabulary-three-only' is technically honored because 'neutral' is one of the three authored expressions in the vocabulary.

_(source: plate_verdicts.jsonl)_

## Cites criteria

- `IR.claude-mascot.palette.four-indexed-color-vocabulary`
- `IR.claude-mascot.style.integer-pixel-grid-no-subpixel`
- `IR.claude-mascot.face.eye-deep-brown-dot-cluster`
- `IR.claude-mascot.face.mouth-line-deep-brown-single-stroke`
- `IR.claude-mascot.face.expression-vocabulary-three-only`

## Provenance

- `runs/2026-05-29-cy-claude-mascot-production/plate_verdicts.jsonl#L6`
