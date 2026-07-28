"""Waveform acquisition client interface for future seismic data downloads.

The client is intentionally configuration-driven and never performs network
access unless the caller enables an explicit future implementation path.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.acquisition.exceptions import AcquisitionConfigurationError
from src.acquisition.validators import validate_config


@dataclass(slots=True)
class WaveformClient:
    """Configuration-driven waveform client placeholder."""

    config: dict[str, Any]

    def __post_init__(self) -> None:
        """Validate configuration on initialization."""
        validate_config(self.config)

    def fetch_waveforms(self) -> dict[str, Any]:
        """Return a placeholder response for future waveform fetching."""
        if not self.config.get("waveform", {}).get("enabled", False):
            raise AcquisitionConfigurationError("Waveform acquisition is disabled in configuration.")
        return {
            "provider": self.config.get("provider", "fdsn"),
            "status": "placeholder",
            "message": "Waveform download logic will be implemented in a future phase.",
        }
