"""Phase 1 tests traced to the EarthESND implementation specification."""

from __future__ import annotations

import json
from dataclasses import asdict

from unittest.mock import mock_open, patch

import pytest

from src.data.manifest import DatasetManifest, ManifestRecord, load_manifest, validate_manifest


def make_record(**overrides: object) -> ManifestRecord:
    values: dict[str, object] = {
        "event_id": "event-001",
        "station_id": "station-001",
        "component_paths": {"NS": "ns.mseed", "EW": "ew.mseed", "UD": "ud.mseed"},
        "p_pick": "2024-01-01T00:00:00Z",
        "sampling_rate_hz": 100.0,
        "station_scaling_provenance": "unresolved-project-assumption",
        "magnitude": 4.2,
        "magnitude_scale": "M_JMA",
        "epicentral_distance_km": 10.0,
        "focal_depth_km": 5.0,
        "hypocentral_distance_km": 11.0,
        "split": "train",
        "is_noto_holdout": False,
        "source_region": "japan",
    }
    values.update(overrides)
    return ManifestRecord(**values)  # type: ignore[arg-type]


def test_manifest_requires_scale_and_split() -> None:
    invalid_scale = make_record(magnitude_scale="")
    invalid_split = make_record(split="")

    with pytest.raises(ValueError, match="magnitude_scale"):
        validate_manifest(DatasetManifest(records=(invalid_scale,)))
    with pytest.raises(ValueError, match="split"):
        validate_manifest(DatasetManifest(records=(invalid_split,)))


def test_manifest_requires_three_named_components() -> None:
    record = make_record(component_paths={"NS": "ns.mseed", "EW": "ew.mseed"})

    with pytest.raises(ValueError, match="NS, EW, and UD"):
        validate_manifest(DatasetManifest(records=(record,)))


def test_manifest_loads_project_assumption_json_format() -> None:
    record = make_record()
    payload = json.dumps({"records": [asdict(record)]})

    with patch("src.data.manifest.Path.open", mock_open(read_data=payload)):
        manifest = load_manifest("manifest.json")

    assert manifest.records == (record,)
