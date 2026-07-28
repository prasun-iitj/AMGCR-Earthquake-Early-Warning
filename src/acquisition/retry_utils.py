"""Retry helpers for transient acquisition failures.

The helpers are intentionally simple and designed for future use around
network-bound catalogue retrieval.
"""

from __future__ import annotations

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def retry_with_backoff(func: Callable[[], T], retries: int = 3, delay: float = 1.0) -> T:
    """Retry a callable a handful of times with exponential backoff."""
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            return func()
        except Exception as exc:  # pragma: no cover - network path
            last_error = exc
            if attempt == retries - 1:
                raise
            time.sleep(delay * (attempt + 1))
    if last_error is not None:
        raise last_error
    raise RuntimeError("Retry logic failed without an error")
