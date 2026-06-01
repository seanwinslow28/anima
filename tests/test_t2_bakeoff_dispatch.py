# tests/test_t2_bakeoff_dispatch.py
from evals.vision_critic.bakeoff_lib import resolve_runner


def test_resolve_runner_maps_each_config():
    from pipeline.agents.cli_runners import run_antigravity_with_image
    from pipeline.agents.sdk_runners import invoke_sonnet_vision, invoke_opus_vision
    assert resolve_runner("antigravity") is run_antigravity_with_image
    assert resolve_runner("sonnet_vision") is invoke_sonnet_vision
    assert resolve_runner("opus_vision") is invoke_opus_vision
