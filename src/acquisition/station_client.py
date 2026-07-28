"""Station metadata client interface for future acquisition workflows.

This module provides a placeholder interface for configuration-driven station
metadata retrieval and validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.acquisition.exceptions import AcquisitionConfigurationError
from src.acquisition.validators import validate_config


@dataclass(slots=True)
class StationClient:
    """Configuration-driven station client placeholder."""

    config: dict[str, Any]

    def __post_init__(self) -> None:
        """Validate configuration on initialization."""
        validate_config(self.config)

    def fetch_stations(self) -> dict[str, Any]:
        """Return a placeholder response for future station metadata fetching."""
        if not self.config.get("station", {}).get("enabled", False):
            raise AcquisitionConfigurationError("Station acquisition is disabled in configuration.")
        return {
            "provider": self.config.get("provider", "fdsn"),
            "status": "placeholder",
            "message": "Station metadata download logic will be implemented in a future phase.",
        }
