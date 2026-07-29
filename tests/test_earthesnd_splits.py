"""Tests for paper-traceable Phase 1 stratified split utilities."""

from __future__ import annotations

import pytest

from src.data.manifest import ManifestRecord
from src.data.splits import assign_stratified_splits


def make_record(index: int, magnitude: float, *, noto: bool = False) -> ManifestRecord:
    return ManifestRecord(
        event_id=f"event-{index}",
        station_id=f"station-{index}",
        component_paths={"NS": "ns.mseed", "EW": "ew.mseed", "UD": "ud.mseed"},
        p_pick="2024-01-01T00:00:00Z",
        sampling_rate_hz=100.0,
        station_scaling_provenance="unresolved-project-assumption",
        magnitude=magnitude,
        magnitude_scale="M_JMA",
        epicentral_distance_km=10.0,
        focal_depth_km=5.0,
        hypocentral_distance_km=11.0,
        split="train",
        is_noto_holdout=noto,
        source_region="japan",
    )


def test_stratification_uses_reported_bins_and_proportions() -> None:
    records = [make_record(index, 3.1 if index < 10 else 4.1) for index in range(20)]
    result = assign_stratified_splits(
        records,
        bins=[3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0],
        proportions={"train": 0.70, "test": 0.15, "validation": 0.15},
        seed=42,
    )

    assert {name: len(items) for name, items in result.items()} == {"train": 14, "test": 4, "validation": 2}
    assert {record.split for record in result["train"]} == {"train"}
    assert {record.split for record in result["test"]} == {"test"}
    assert {record.split for record in result["validation"]} == {"validation"}


def test_stratification_requires_seed() -> None:
    with pytest.raises(ValueError, match="seed is required"):
        assign_stratified_splits(
            [make_record(1, 4.0)],
            bins=[3.0, 3.5, 4.0, 4.5],
            proportions={"train": 0.70, "test": 0.15, "validation": 0.15},
            seed=None,
        )


def test_noto_holdout_is_not_reassigned() -> None:
    with pytest.raises(ValueError, match="Noto holdout"):
        assign_stratified_splits(
            [make_record(1, 4.0, noto=True)],
            bins=[3.0, 3.5, 4.0, 4.5],
            proportions={"train": 0.70, "test": 0.15, "validation": 0.15},
            seed=1,
        )
