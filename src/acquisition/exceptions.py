"""Custom exceptions used by the acquisition framework."""

from __future__ import annotations


class AcquisitionError(Exception):
    """Base class for acquisition-related errors."""


class AcquisitionConfigurationError(AcquisitionError):
    """Raised when acquisition configuration is missing or invalid."""


class AcquisitionRuntimeError(AcquisitionError):
    """Raised when an acquisition operation cannot proceed at runtime."""
