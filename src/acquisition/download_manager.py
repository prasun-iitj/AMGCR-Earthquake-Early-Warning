"""High-level orchestration utility for future acquisition workflows.

The manager coordinates configuration validation and delegates to concrete
clients without performing any actual downloads in Phase 2A.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.acquisition.catalog_client import CatalogClient
from src.acquisition.exceptions import AcquisitionConfigurationError
from src.acquisition.station_client import StationClient
from src.acquisition.validators import validate_config
from src.acquisition.waveform_client import WaveformClient


@dataclass(slots=True)
class DownloadManager:
    """Configuration-driven acquisition manager placeholder."""

    config: dict[str, Any]

    def __post_init__(self) -> None:
        """Validate the acquisition configuration on initialization."""
        validate_config(self.config)

    def preview_plan(self) -> dict[str, Any]:
        """Return a structured preview of the configured acquisition workflow."""
        if not isinstance(self.config, dict):
            raise AcquisitionConfigurationError("Configuration must be a dictionary.")
        return {
            "provider": self.config.get("provider", "fdsn"),
            "network": self.config.get("network"),
            "station": self.config.get("station"),
            "channel": self.config.get("channel"),
            "location": self.config.get("location"),
            "catalog_enabled": self.config.get("catalog", {}).get("enabled", False),
            "waveform_enabled": self.config.get("waveform", {}).get("enabled", False),
            "station_enabled": self.config.get("station", {}).get("enabled", False),
        }

    def get_catalog_client(self) -> CatalogClient:
        """Return a catalog client instance bound to the configuration."""
        return CatalogClient(self.config)

    def get_waveform_client(self) -> WaveformClient:
        """Return a waveform client instance bound to the configuration."""
        return WaveformClient(self.config)

    def get_station_client(self) -> StationClient:
        """Return a station client instance bound to the configuration."""
        return StationClient(self.config)
