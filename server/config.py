from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    runs_root: Path


def get_settings() -> Settings:
    return Settings(runs_root=Path(os.environ.get("ANIMA_RUNS_ROOT", "runs")))
