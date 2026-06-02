"""--stub must force the credential-free path for BOTH Gemini transports (else a
gemini_api run with --stub would fire live, costed calls)."""
from __future__ import annotations


def test_force_stub_patches_all_three_runners():
    from evals.vision_critic import score
    from pipeline.agents import vision_critic as vc

    orig = (vc.run_antigravity_with_image, vc.run_gemini_api_with_image, vc.invoke_opus_vision)
    try:
        score._force_stub_runners()
        assert vc.run_antigravity_with_image is not orig[0]
        assert vc.run_gemini_api_with_image is not orig[1]   # the new one
        assert vc.invoke_opus_vision is not orig[2]
    finally:
        (vc.run_antigravity_with_image, vc.run_gemini_api_with_image, vc.invoke_opus_vision) = orig
