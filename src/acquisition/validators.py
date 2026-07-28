"""Validation helpers for acquisition configuration.

These validators ensure that configuration values are present and well-formed
before any future acquisition workflow is run.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.acquisition.exceptions import AcquisitionConfigurationError


def validate_config(config: dict[str, Any]) -> None:
    """Validate the top-level acquisition configuration dictionary."""
    if not isinstance(config, dict):
        raise AcquisitionConfigurationError("Configuration must be a dictionary.")

    provider = config.get("provider")
    if not isinstance(provider, str) or not provider.strip():
        raise AcquisitionConfigurationError("Provider must be a non-empty string.")

    for key in ("network", "station", "channel"):
        value = config.get(key)
        if not isinstance(value, str) or not value.strip():
            raise AcquisitionConfigurationError(f"{key} must be a non-empty string.")

    location = config.get("location")
    if location is not None and not isinstance(location, str):
        raise AcquisitionConfigurationError("location must be a string.")

    start_time = config.get("start_time")
    end_time = config.get("end_time")
    if not _is_valid_datetime(start_time):
        raise AcquisitionConfigurationError("start_time must be a valid ISO 8601 datetime string.")
    if not _is_valid_datetime(end_time):
        raise AcquisitionConfigurationError("end_time must be a valid ISO 8601 datetime string.")
    if start_time >= end_time:
        raise AcquisitionConfigurationError("start_time must be earlier than end_time.")

    magnitude = config.get("magnitude")
    if not isinstance(magnitude, dict):
        raise AcquisitionConfigurationError("magnitude must be a dictionary.")
    minimum_magnitude = magnitude.get("minimum")
    maximum_magnitude = magnitude.get("maximum")
    if not isinstance(minimum_magnitude, (int, float)) or not isinstance(maximum_magnitude, (int, float)):
        raise AcquisitionConfigurationError("magnitude minimum/maximum must be numeric.")
    if minimum_magnitude > maximum_magnitude:
        raise AcquisitionConfigurationError("magnitude minimum cannot exceed maximum.")

    catalog = config.get("catalog")
    if catalog is None:
        catalog = {}
    elif not isinstance(catalog, dict):
        raise AcquisitionConfigurationError("catalog must be a dictionary.")

    for key in ("enabled", "format", "limit", "output_dir"):
        if key == "enabled":
            value = catalog.get(key)
            if value is not None and not isinstance(value, bool):
                raise AcquisitionConfigurationError("catalog.enabled must be a boolean.")
        elif key == "format":
            value = catalog.get(key)
            if value is not None and not isinstance(value, str):
                raise AcquisitionConfigurationError("catalog.format must be a string.")
        elif key == "output_dir":
            value = catalog.get(key)
            if value is not None and not isinstance(value, str):
                raise AcquisitionConfigurationError("catalog.output_dir must be a string.")
        else:
            value = catalog.get(key)
            if value is not None and not isinstance(value, (int, float)):
                raise AcquisitionConfigurationError("catalog.limit must be numeric.")

    for key in ("retry_attempts", "retry_delay", "timeout_seconds"):
        value = catalog.get(key)
        if value is None:
            continue
        if not isinstance(value, (int, float)):
            raise AcquisitionConfigurationError(f"catalog.{key} must be numeric.")

    output = config.get("output")
    if not isinstance(output, dict):
        raise AcquisitionConfigurationError("output must be a dictionary.")
    for key in ("raw_dir", "processed_dir", "logs_dir"):
        value = output.get(key)
        if not isinstance(value, str) or not value.strip():
            raise AcquisitionConfigurationError(f"output.{key} must be a non-empty string.")


def _is_valid_datetime(value: Any) -> bool:
    """Return True when the given value is a parseable ISO datetime string."""
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        datetime.fromisoformat(value)
    except ValueError:
        return False
    return True
