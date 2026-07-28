"""Magnitude-stratified split utilities for EarthESND manifests.

The paper specifies bin edges and a 70:15:15 split, but not a random seed,
rounding rule, or output representation. The deterministic shuffle, largest-
remainder allocation, and returned mapping are documented project assumptions.
"""

from __future__ import annotations

from dataclasses import replace
from bisect import bisect_right
from collections.abc import Mapping, Sequence
from math import floor
from random import Random

from src.data.manifest import ManifestRecord


SPLIT_ORDER = ("train", "test", "validation")


def assign_stratified_splits(
    records: Sequence[ManifestRecord],
    bins: Sequence[float],
    proportions: Mapping[str, float],
    seed: int | None,
) -> dict[str, list[ManifestRecord]]:
    """Assign records to paper-specified magnitude strata.

    ``bins`` are ascending inclusive lower boundaries; the final boundary also
    includes its upper endpoint. This boundary convention and largest-remainder
    count allocation are project assumptions, because they are not supplied by
    the paper. ``seed`` is required so a split is reproducible.
    """
    if seed is None:
        raise ValueError("seed is required; the paper does not provide a default seed.")
    _validate_bins(bins)
    _validate_proportions(proportions)

    stratified: dict[int, list[ManifestRecord]] = {}
    for record in records:
        if not isinstance(record, ManifestRecord):
            raise TypeError("records must contain ManifestRecord instances.")
        if record.is_noto_holdout:
            raise ValueError("Noto holdout records must remain separate from stratified assignment.")
        stratum = _stratum_index(record.magnitude, bins)
        stratified.setdefault(stratum, []).append(record)

    rng = Random(seed)
    result: dict[str, list[ManifestRecord]] = {split: [] for split in SPLIT_ORDER}
    for stratum in sorted(stratified):
        members = list(stratified[stratum])
        rng.shuffle(members)
        counts = _allocate_counts(len(members), proportions)
        start = 0
        for split in SPLIT_ORDER:
            end = start + counts[split]
            result[split].extend(replace(record, split=split) for record in members[start:end])
            start = end
    return result


def _validate_bins(bins: Sequence[float]) -> None:
    if len(bins) < 2:
        raise ValueError("At least two magnitude bin boundaries are required.")
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in bins):
        raise TypeError("Magnitude bins must be numeric.")
    if any(current >= following for current, following in zip(bins, bins[1:])):
        raise ValueError("Magnitude bins must be strictly increasing.")


def _validate_proportions(proportions: Mapping[str, float]) -> None:
    if set(proportions) != set(SPLIT_ORDER):
        raise ValueError("proportions must define train, test, and validation.")
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0 for value in proportions.values()):
        raise ValueError("Split proportions must be non-negative numeric values.")
    if abs(sum(proportions.values()) - 1.0) > 1e-12:
        raise ValueError("Split proportions must sum to 1.0.")


def _stratum_index(magnitude: float, bins: Sequence[float]) -> int:
    if magnitude < bins[0] or magnitude > bins[-1]:
        raise ValueError("Record magnitude falls outside configured stratification bins.")
    return bisect_right(bins, magnitude) - 1


def _allocate_counts(total: int, proportions: Mapping[str, float]) -> dict[str, int]:
    raw = {split: total * proportions[split] for split in SPLIT_ORDER}
    counts = {split: floor(raw[split]) for split in SPLIT_ORDER}
    remaining = total - sum(counts.values())
    priorities = sorted(SPLIT_ORDER, key=lambda split: (-(raw[split] - counts[split]), SPLIT_ORDER.index(split)))
    for split in priorities[:remaining]:
        counts[split] += 1
    return counts
