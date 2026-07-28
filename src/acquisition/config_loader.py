"""Configuration loader for acquisition settings.

This module reads YAML files from the configs/ directory and returns a
configuration dictionary that can be validated before any future download.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.acquisition.exceptions import AcquisitionConfigurationError


class AcquisitionConfigLoader:
    """Load acquisition configuration from YAML files."""

    def __init__(self, config_path: str | Path | None = None) -> None:
        """Initialize the loader with an optional config path."""
        self.config_path = Path(config_path or "configs/acquisition_config.yaml")

    def load(self) -> dict[str, Any]:
        """Load and validate the YAML configuration file."""
        if not self.config_path.exists():
            raise AcquisitionConfigurationError(f"Configuration file not found: {self.config_path}")

        with self.config_path.open("r", encoding="utf-8") as handle:
            config = yaml.safe_load(handle) or {}

        if not isinstance(config, dict):
            raise AcquisitionConfigurationError("Configuration file must contain a YAML mapping.")
        return config
