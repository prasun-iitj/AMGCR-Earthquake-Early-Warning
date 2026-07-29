"""EarthESND dataset-manifest contracts.

The field names and JSON serialization are project assumptions. They implement
the provenance requirements traced in the implementation specification to
``EARTHESND_REVERSE_ENGINEERING.md`` sections 2, 3, 12, and 15.A.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


VALID_MAGNITUDE_SCALES = frozenset({"M_JMA", "M_w"})
VALID_SPLITS = frozenset({"train", "test", "validation"})
REQUIRED_COMPONENTS = frozenset({"NS", "EW", "UD"})


@dataclass(frozen=True, slots=True)
class ManifestRecord:
    """Provenance and split metadata for one three-component waveform record.

    All fields are required by the project data contract. The paper does not
    prescribe a manifest schema; this dataclass is therefore a project
    assumption, not a claim about the paper's released data files.
    """

    event_id: str
    station_id: str
    component_paths: Mapping[str, str]
    p_pick: str
    sampling_rate_hz: float
    station_scaling_provenance: str
    magnitude: float
    magnitude_scale: str
    epicentral_distance_km: float
    focal_depth_km: float
    hypocentral_distance_km: float
    split: str
    is_noto_holdout: bool
    source_region: str


@dataclass(frozen=True, slots=True)
class DatasetManifest:
    """A collection of validated :class:`ManifestRecord` instances."""

    records: tuple[ManifestRecord, ...]

    @classmethod
    def from_records(cls, records: Iterable[ManifestRecord]) -> "DatasetManifest":
        """Create and validate a manifest from an iterable of records."""
        manifest = cls(records=tuple(records))
        validate_manifest(manifest)
        return manifest


def load_manifest(path: str | Path) -> DatasetManifest:
    """Load a JSON manifest.

    JSON is a project assumption selected to keep Phase 1 dependency-free. The
    paper does not specify a manifest format.
    """
    manifest_path = Path(path)
    with manifest_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
        raise ValueError("Manifest JSON must contain a 'records' list.")

    records = tuple(_record_from_mapping(item) for item in payload["records"])
    return DatasetManifest.from_records(records)


def validate_manifest(manifest: DatasetManifest) -> None:
    """Validate the project-assumption manifest contract.

    Validation deliberately checks only the Phase 1 contract: provenance,
    component identity, target scale, numeric metadata, and split membership.
    It does not infer unavailable paper processing or model choices.
    """
    if not isinstance(manifest, DatasetManifest):
        raise TypeError("manifest must be a DatasetManifest instance.")

    for record in manifest.records:
        if not isinstance(record, ManifestRecord):
            raise TypeError("Manifest records must be ManifestRecord instances.")
        _require_non_empty(record.event_id, "event_id")
        _require_non_empty(record.station_id, "station_id")
        _require_non_empty(record.p_pick, "p_pick")
        _require_non_empty(record.station_scaling_provenance, "station_scaling_provenance")
        _require_non_empty(record.source_region, "source_region")

        if set(record.component_paths) != REQUIRED_COMPONENTS:
            raise ValueError("component_paths must contain exactly NS, EW, and UD entries.")
        for component, component_path in record.component_paths.items():
            _require_non_empty(component, "component path key")
            _require_non_empty(component_path, f"component_paths[{component!r}]")

        _require_positive(record.sampling_rate_hz, "sampling_rate_hz")
        _require_number(record.magnitude, "magnitude")
        _require_non_negative(record.epicentral_distance_km, "epicentral_distance_km")
        _require_non_negative(record.focal_depth_km, "focal_depth_km")
        _require_non_negative(record.hypocentral_distance_km, "hypocentral_distance_km")

        if record.magnitude_scale not in VALID_MAGNITUDE_SCALES:
            raise ValueError(f"magnitude_scale must be one of {sorted(VALID_MAGNITUDE_SCALES)}.")
        if record.split not in VALID_SPLITS:
            raise ValueError(f"split must be one of {sorted(VALID_SPLITS)}.")
        if not isinstance(record.is_noto_holdout, bool):
            raise TypeError("is_noto_holdout must be a boolean.")


def _record_from_mapping(value: Any) -> ManifestRecord:
    if not isinstance(value, dict):
        raise ValueError("Each manifest record must be an object.")
    try:
        return ManifestRecord(**value)
    except TypeError as exc:
        raise ValueError(f"Invalid manifest record fields: {exc}") from exc


def _require_non_empty(value: object, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


def _require_number(value: object, field_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be numeric.")


def _require_positive(value: object, field_name: str) -> None:
    _require_number(value, field_name)
    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")


def _require_non_negative(value: object, field_name: str) -> None:
    _require_number(value, field_name)
    if value < 0:
        raise ValueError(f"{field_name} must be zero or greater.")
