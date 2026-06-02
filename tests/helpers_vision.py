# tests/helpers_vision.py
"""Shared fake CLI/SDK response for vision_critic tests."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class _FakeCLI:
    text: str
    duration_s: float = 1.0
    exit_code: int = 0
    rate_capped: bool = False
    stub_fallback: bool = False
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.rate_capped and self.error is None
