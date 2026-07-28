"""Catalog acquisition client for earthquake catalogue retrieval.

The implementation uses ObsPy's FDSN client and is intentionally configured
through YAML so the workflow can target multiple providers without code changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from obspy.clients.fdsn import Client

from src.acquisition.exceptions import AcquisitionConfigurationError, AcquisitionRuntimeError
from src.acquisition.retry_utils import retry_with_backoff
from src.acquisition.validators import validate_config
from src.utils.logging_config import configure_logging, get_logger


@dataclass(slots=True)
class CatalogClient:
    """Configuration-driven catalog client for future retrieval workflows."""

    config: dict[str, Any]

    def __post_init__(self) -> None:
        """Validate configuration on initialization."""
        validate_config(self.config)
        configure_logging()

    def build_query(self) -> dict[str, Any]:
        """Build the event query dictionary from the acquisition configuration."""
        return self.build_retrieval_query("")

    def build_retrieval_query(self, provider: str | None = None) -> dict[str, Any]:
        """Build the event query dictionary and remove provider-specific unsupported parameters."""
        catalog_settings = self.config.get("catalog", {})
        magnitude = self.config.get("magnitude", {})
        query: dict[str, Any] = {
            "starttime": self.config.get("start_time"),
            "endtime": self.config.get("end_time"),
            "minmagnitude": magnitude.get("minimum", 0.0),
            "maxmagnitude": magnitude.get("maximum", 10.0),
            "network": self.config.get("network"),
            "station": self.config.get("station"),
            "channel": self.config.get("channel"),
            "location": self.config.get("location"),
            "limit": int(catalog_settings.get("limit", 10)),
        }

        provider_name = (provider or self.config.get("provider") or "").lower()
        if provider_name in {"usgs", "fdsn", "https://earthquake.usgs.gov", "earthquake.usgs.gov"}:
            for unsupported_param in ("network", "station", "channel", "location"):
                query.pop(unsupported_param, None)

        return {k: v for k, v in query.items() if v not in (None, "")}

    def retrieve_catalog(self) -> dict[str, Any]:
        """Retrieve a sample catalogue using the configured FDSN provider."""
        if not self.config.get("catalog", {}).get("enabled", False):
            raise AcquisitionConfigurationError("Catalog acquisition is disabled in configuration.")

        provider = str(self.config.get("provider", "iris")).lower()
        catalog_settings = self.config.get("catalog", {})
        retry_attempts = int(catalog_settings.get("retry_attempts", 3))
        retry_delay = float(catalog_settings.get("retry_delay", 1.0))
        timeout = int(catalog_settings.get("timeout_seconds", 30))
        client = self._get_client(provider, timeout)
        query = self.build_retrieval_query(provider)
        logger = get_logger(__name__)
        logger.info("catalog_retrieval_start provider=%s query=%s timeout=%s", provider, query, timeout)

        try:
            cat = retry_with_backoff(
                lambda: client.get_events(**query),
                retries=retry_attempts,
                delay=retry_delay,
            )
        except Exception as exc:  # pragma: no cover - network path
            logger.error("catalog_retrieval_failed provider=%s error=%s", provider, exc)
            raise AcquisitionRuntimeError(f"Catalog retrieval failed for provider {provider}: {exc}") from exc

        output_format = str(catalog_settings.get("format", "quakeml")).lower()
        output_dir = Path(catalog_settings.get("output_dir", "data/raw/catalogs"))
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = self._save_catalog(cat, output_dir, output_format)
        logger.info("catalog_retrieval_complete provider=%s events=%s file=%s", provider, len(cat), file_path)

        return {
            "provider": provider,
            "format": output_format,
            "events": len(cat),
            "file_path": str(file_path),
            "status": "retrieved",
        }

    def _get_client(self, provider: str, timeout: int) -> Client:
        """Return an ObsPy FDSN client for the configured provider."""
        providers = {
            "iris": "https://service.iris.edu",
            "usgs": "https://earthquake.usgs.gov",
            "emsc": "EMSC",
            "gfz": "GFZ",
            "fdsn": "https://earthquake.usgs.gov",
        }
        provider_name = providers.get(provider, provider)
        return Client(provider_name, timeout=timeout)

    def _save_catalog(self, catalog: Any, output_dir: Path, output_format: str) -> Path:
        """Save the retrieved catalogue in the requested format."""
        if output_format.lower() == "csv":
            file_path = output_dir / "catalog.csv"
            catalog.write(str(file_path), format="CSV")
        else:
            file_path = output_dir / "catalog.xml"
            catalog.write(str(file_path), format="QUAKEML")
        return file_path
