"""Load and validate EarthESND model configuration from YAML.

Trace: Spec ``configs/earthesnd/model.yaml``; RE §5–§8, §16.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

from src.models.esn import ESNConfig


VALID_WINDOW_LABELS = frozenset({"2", "3", "4", "5", "6"})
VALID_TARGET_SCALES = frozenset({"M_JMA", "M_w"})


@dataclass(frozen=True, slots=True)
class DennWindowSettings:
    """Per-window DENN branch count and reported connectivity sparsity ``nu``."""

    branches: int
    reported_sparsity: float


@dataclass(frozen=True, slots=True)
class DennArchitectureConfig:
    """Paper-declared DENN readout structure with operational fields unresolved."""

    layer_widths: tuple[int, ...]
    activations: tuple[str, ...]
    branch_connectivity_method: str | None
    local_branch_nonlinearity: str | None
    mask_learning: bool | None
    windows: Mapping[str, DennWindowSettings]


@dataclass(frozen=True, slots=True)
class TrainingConfig:
    """Reported training schedule from the paper."""

    loss: str
    optimizer: str
    epochs: int
    batch_size: int
    learning_rate: float
    adam_betas: tuple[float, float] | None
    adam_epsilon: float | None
    weight_decay: float | None


@dataclass(frozen=True, slots=True)
class EarthESNDModelConfig:
    """Resolved model contract for one P-wave window experiment."""

    channel_count: int
    target_scale: str
    window_label: str
    esn_leak_rate: float
    denn: DennArchitectureConfig
    denn_window: DennWindowSettings
    training: TrainingConfig


def load_model_yaml(path: str | Path) -> Mapping[str, Any]:
    """Load raw ``model.yaml`` contents."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if not isinstance(payload, dict):
        raise ValueError("model.yaml must contain a mapping at the top level.")
    return payload


def _parse_denn_windows(raw: Mapping[str, Any]) -> dict[str, DennWindowSettings]:
    windows: dict[str, DennWindowSettings] = {}
    for label, values in raw.items():
        windows[str(label)] = DennWindowSettings(
            branches=int(values["branches"]),
            reported_sparsity=float(values["reported_sparsity"]),
        )
    return windows


def parse_denn_architecture(section: Mapping[str, Any]) -> DennArchitectureConfig:
    """Parse the ``denn`` block from ``model.yaml``."""
    mask_learning = section.get("mask_learning")
    if mask_learning is not None and not isinstance(mask_learning, bool):
        raise ValueError("denn.mask_learning must be a boolean when set.")
    return DennArchitectureConfig(
        layer_widths=tuple(int(width) for width in section["layer_widths"]),
        activations=tuple(str(name) for name in section["activations"]),
        branch_connectivity_method=section.get("branch_connectivity_method"),
        local_branch_nonlinearity=section.get("local_branch_nonlinearity"),
        mask_learning=mask_learning,
        windows=_parse_denn_windows(section["windows"]),
    )


def parse_training_for_window(section: Mapping[str, Any], window_label: str) -> TrainingConfig:
    """Parse shared training settings plus the per-window learning rate."""
    window_rates = section["windows"]
    if window_label not in window_rates:
        raise ValueError(f"training.windows missing key {window_label!r}.")
    betas = section.get("adam_betas")
    parsed_betas: tuple[float, float] | None
    if betas is None:
        parsed_betas = None
    else:
        parsed_betas = (float(betas[0]), float(betas[1]))
    return TrainingConfig(
        loss=str(section["loss"]),
        optimizer=str(section["optimizer"]),
        epochs=int(section["epochs"]),
        batch_size=int(section["batch_size"]),
        learning_rate=float(window_rates[window_label]["learning_rate"]),
        adam_betas=parsed_betas,
        adam_epsilon=section.get("adam_epsilon"),
        weight_decay=section.get("weight_decay"),
    )


def load_earthesnd_model_config(
    path: str | Path,
    *,
    window_seconds: int,
) -> EarthESNDModelConfig:
    """Load :class:`EarthESNDModelConfig` for one window (2–6 s)."""
    payload = load_model_yaml(path)
    window_label = str(window_seconds)
    if window_label not in VALID_WINDOW_LABELS:
        raise ValueError(f"window_seconds must be one of {sorted(VALID_WINDOW_LABELS)}.")

    target_scale = str(payload["target_scale"])
    if target_scale not in VALID_TARGET_SCALES:
        raise ValueError(f"Unsupported target_scale {target_scale!r}.")

    esn_windows = payload["esn"]["windows"]
    if window_label not in esn_windows:
        raise ValueError(f"esn.windows missing key {window_label!r}.")

    denn = parse_denn_architecture(payload["denn"])
    if window_label not in denn.windows:
        raise ValueError(f"denn.windows missing key {window_label!r}.")

    if tuple(denn.layer_widths) != (64, 1):
        raise ValueError("Paper readout requires denn.layer_widths [64, 1].")
    if tuple(denn.activations) != ("gelu", "linear"):
        raise ValueError("Paper readout requires denn.activations [gelu, linear].")

    return EarthESNDModelConfig(
        channel_count=int(payload["inputs"]["channel_count"]),
        target_scale=target_scale,
        window_label=window_label,
        esn_leak_rate=float(esn_windows[window_label]["reported_leak"]),
        denn=denn,
        denn_window=denn.windows[window_label],
        training=parse_training_for_window(payload["training"], window_label),
    )


def build_esn_config(
    model_config: EarthESNDModelConfig,
    *,
    reservoir_size: int,
    spectral_radius: float,
    input_scaling: float,
    sparsity: float,
    random_seed: int | None,
) -> ESNConfig:
    """Build :class:`ESNConfig` using paper leak for the selected window.

    Reservoir size, spectral radius, input scaling, and sparsity are not
    specified in the paper and must be supplied explicitly by the caller.
    """
    return ESNConfig(
        reservoir_size=reservoir_size,
        spectral_radius=spectral_radius,
        input_scaling=input_scaling,
        sparsity=sparsity,
        leak_rate=model_config.esn_leak_rate,
        random_seed=random_seed,
    )


def require_denn_operational_settings(denn: DennArchitectureConfig) -> None:
    """Fail closed until DENN mask and local-nonlinearity choices are declared."""
    missing: list[str] = []
    if denn.branch_connectivity_method is None:
        missing.append("branch_connectivity_method")
    if denn.local_branch_nonlinearity is None:
        missing.append("local_branch_nonlinearity")
    if denn.mask_learning is None:
        missing.append("mask_learning")
    if missing:
        raise NotImplementedError(
            "DENN readout construction is blocked until the following settings "
            f"are declared as project assumptions: {', '.join(missing)} "
            "(RE §6.1, §16)."
        )
    if denn.mask_learning:
        raise NotImplementedError(
            "Learnable DENN connectivity masks are not specified in the paper "
            "(RE §6.1, §16)."
        )


def require_training_settings(training: TrainingConfig) -> None:
    """Fail closed until Adam details omitted from the paper are declared."""
    missing: list[str] = []
    if training.optimizer != "adam":
        raise ValueError("Only optimizer 'adam' is traced to the paper schedule.")
    if training.loss != "mse":
        raise ValueError("Only loss 'mse' is traced to the paper schedule.")
    if training.adam_betas is None:
        missing.append("adam_betas")
    if training.adam_epsilon is None:
        missing.append("adam_epsilon")
    if training.weight_decay is None:
        missing.append("weight_decay")
    if missing:
        raise NotImplementedError(
            "EarthESNDModel.fit is blocked until training settings are declared "
            f"as project assumptions: {', '.join(missing)} (RE §8, §16)."
        )
