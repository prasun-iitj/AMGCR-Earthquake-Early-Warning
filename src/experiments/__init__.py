"""Experiment metadata and reproducibility guards.

Trace: RE §15–§16; Spec R-REP.
"""

from src.experiments.run_metadata import (
    ExactReproductionBlockedError,
    ExperimentMetadata,
    assert_no_unresolved_settings,
    collect_unresolved_config_paths,
    load_earthesnd_config_bundle,
    write_deviation_log,
)

__all__ = [
    "ExactReproductionBlockedError",
    "ExperimentMetadata",
    "assert_no_unresolved_settings",
    "collect_unresolved_config_paths",
    "load_earthesnd_config_bundle",
    "write_deviation_log",
]
