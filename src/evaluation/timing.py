"""Training-time measurement helpers.

Hardware, repetitions, and timing methodology are not specified in the
paper (RE §9, §11). Callers must supply environment metadata explicitly.

Trace: Spec R-EVAL; RE §9, §11.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrainingTimingResult:
    """Seconds elapsed for one training epoch plus caller-declared environment."""

    seconds_per_epoch: float
    timing_environment: tuple[tuple[str, str], ...]


def measure_training_seconds_per_epoch(
    train_one_epoch: Callable[[], None],
    *,
    timing_environment: Mapping[str, str] | None,
) -> TrainingTimingResult:
    """Measure wall-clock seconds for a single epoch callback.

    Args:
        train_one_epoch: Callable that runs exactly one training epoch.
        timing_environment: Non-empty mapping describing hardware, software, or
            other timing context. Must not be omitted because the paper does
            not specify timing methodology.

    Raises:
        ValueError: If ``timing_environment`` is missing or empty.
    """
    if timing_environment is None or not timing_environment:
        raise ValueError(
            "timing_environment must be supplied explicitly; "
            "timing hardware and methodology are not specified in the paper (RE §11)."
        )
    normalized = tuple(
        (str(key), str(value))
        for key, value in sorted(timing_environment.items(), key=lambda item: item[0])
    )
    start = time.perf_counter()
    train_one_epoch()
    elapsed = time.perf_counter() - start
    if elapsed < 0.0:
        raise RuntimeError("Measured elapsed time must be non-negative.")
    return TrainingTimingResult(seconds_per_epoch=float(elapsed), timing_environment=normalized)
