"""Persist run configuration, deviations, and block exact-reproduction claims.

JSON serialization and nested-path reporting for unresolved YAML fields are
project assumptions supporting RE §15–§16.

Trace: Spec R-REP; test_exact_run_blocks_unresolved_fields.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping

import yaml

EARTHESND_CONFIG_FILES = (
    "data.yaml",
    "preprocessing.yaml",
    "model.yaml",
    "synthetic_ensemble.yaml",
    "evaluation.yaml",
)

FEATURE_COUNT_CONFLICT_NOTE = (
    "Paper inconsistency: prose references six tabular inputs while seven "
    "vertical features are named (tau_c, ID2, IV2, PI, RSSCV, Tva, CAV). "
    "Runs must record which convention is used as a project assumption (RE §4, §16)."
)


class ExactReproductionBlockedError(RuntimeError):
    """Raised when an exact-reproduction claim is incompatible with null config fields."""


@dataclass(frozen=True, slots=True)
class ExperimentMetadata:
    """Provenance bundle for one EarthESND experiment run."""

    run_id: str
    created_at_utc: str
    exact_reproduction_claim: bool
    configs: Mapping[str, Any]
    deviations: tuple[str, ...]
    project_assumptions: tuple[str, ...]
    unresolved_config_fields: tuple[str, ...]
    target_scales_used: tuple[str, ...]
    feature_count_conflict_note: str = FEATURE_COUNT_CONFLICT_NOTE

    def to_dict(self) -> dict[str, Any]:
        """Serialize metadata for JSON persistence."""
        data = asdict(self)
        for key in (
            "deviations",
            "project_assumptions",
            "unresolved_config_fields",
            "target_scales_used",
        ):
            data[key] = list(data[key])
        return data


def load_earthesnd_config_bundle(config_dir: str | Path) -> dict[str, Any]:
    """Load all EarthESND YAML configs from ``configs/earthesnd/``."""
    base = Path(config_dir)
    if not base.is_dir():
        raise ValueError(f"Config directory does not exist: {base}")
    bundle: dict[str, Any] = {}
    for name in EARTHESND_CONFIG_FILES:
        path = base / name
        if not path.is_file():
            raise ValueError(f"Missing required config file: {path}")
        with path.open("r", encoding="utf-8") as handle:
            payload = yaml.safe_load(handle)
        if not isinstance(payload, dict):
            raise ValueError(f"{name} must contain a mapping at the top level.")
        bundle[name] = payload
    return bundle


def collect_unresolved_config_paths(config: Any, *, prefix: str = "") -> list[str]:
    """Return dotted paths to every ``None`` value in a nested config structure."""
    if config is None:
        return [prefix or "<root>"]
    if isinstance(config, dict):
        paths: list[str] = []
        for key in sorted(config):
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            paths.extend(collect_unresolved_config_paths(config[key], prefix=child_prefix))
        return paths
    if isinstance(config, list):
        paths = []
        for index, item in enumerate(config):
            child_prefix = f"{prefix}[{index}]"
            paths.extend(collect_unresolved_config_paths(item, prefix=child_prefix))
        return paths
    return []


def assert_no_unresolved_settings(
    configs: Mapping[str, Any],
    *,
    exact_reproduction_claim: bool,
) -> None:
    """Block exact-reproduction runs while any required YAML field remains null."""
    if not exact_reproduction_claim:
        return
    unresolved: list[str] = []
    for file_name, payload in sorted(configs.items()):
        for path in collect_unresolved_config_paths(payload):
            unresolved.append(f"{file_name}:{path}")
    if unresolved:
        joined = ", ".join(unresolved)
        raise ExactReproductionBlockedError(
            "Exact paper reproduction cannot be claimed while configuration fields "
            f"remain null (not specified in the paper): {joined}"
        )


def write_deviation_log(metadata: ExperimentMetadata, path: str | Path) -> Path:
    """Persist deviations, assumptions, and unresolved fields as JSON."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if metadata.exact_reproduction_claim and metadata.unresolved_config_fields:
        raise ExactReproductionBlockedError(
            "Cannot write an exact-reproduction deviation log while unresolved "
            "configuration fields remain."
        )
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(metadata.to_dict(), handle, indent=2, sort_keys=True)
        handle.write("\n")
    return output_path


def build_experiment_metadata(
    *,
    run_id: str,
    configs: Mapping[str, Any],
    deviations: tuple[str, ...] = (),
    project_assumptions: tuple[str, ...] = (),
    target_scales_used: tuple[str, ...],
    exact_reproduction_claim: bool = False,
    created_at_utc: str | None = None,
) -> ExperimentMetadata:
    """Construct metadata and apply the exact-reproduction guard when requested."""
    unresolved: list[str] = []
    for file_name, payload in sorted(configs.items()):
        for path in collect_unresolved_config_paths(payload):
            unresolved.append(f"{file_name}:{path}")
    assert_no_unresolved_settings(configs, exact_reproduction_claim=exact_reproduction_claim)
    timestamp = created_at_utc or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return ExperimentMetadata(
        run_id=run_id,
        created_at_utc=timestamp,
        exact_reproduction_claim=exact_reproduction_claim,
        configs=dict(configs),
        deviations=deviations,
        project_assumptions=project_assumptions,
        unresolved_config_fields=tuple(unresolved),
        target_scales_used=target_scales_used,
    )
