"""Configuration loader."""

import json
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Application configuration."""

    DEFAULTS: Dict[str, Any] = {
        "board_size": 15,
        "grid_size": 20,
        "fps": 30,
        "ai": {
            "max_depth": 4,
            "max_candidates": 12,
            "time_limit_ms": 5000,
        },
        "ui": {
            "window_width": 380,
            "window_height": 320,
        },
        "replay": {
            "save_dir": "replays",
        },
    }

    def __init__(self, config_path: Optional[Path] = None) -> None:
        self._config = self.DEFAULTS.copy()
        if config_path and config_path.exists():
            with open(config_path) as f:
                user = json.load(f)
                self._deep_update(self._config, user)

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        val = self._config
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k)
            else:
                return default
        return val if val is not None else default

    @staticmethod
    def _deep_update(base: dict, update: dict) -> None:
        for k, v in update.items():
            if isinstance(v, dict) and k in base:
                Config._deep_update(base[k], v)
            else:
                base[k] = v


def load_config(config_path: Optional[Path] = None) -> Config:
    """Load configuration from file or defaults."""
    return Config(config_path)
