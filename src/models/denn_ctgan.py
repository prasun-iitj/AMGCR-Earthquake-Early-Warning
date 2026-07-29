"""DENN-CTGAN synthetic tabular generation (paper-declared, detail-blocked).

The paper specifies DENN-based CTGAN on vertical tabular features plus the
training magnitude target, producing 10,000 synthetic rows. Generator,
discriminator, and training hyperparameters are not specified in the main PDF.

Trace: RE §7.1, §16; Spec R-SYN.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import yaml

from src.models.tabular_data import assert_all_training_splits, assert_training_split_only


@dataclass(frozen=True, slots=True)
class DennCtganConfig:
    """Configuration contract for DENN-CTGAN."""

    model: str
    synthetic_record_count: int
    input: str
    generator_architecture: Mapping[str, Any] | None
    discriminator_architecture: Mapping[str, Any] | None
    training_hyperparameters: Mapping[str, Any] | None
    t_sne_parameters: Mapping[str, Any] | None

    def __post_init__(self) -> None:
        if self.model != "denn_ctgan":
            raise ValueError("model must be 'denn_ctgan' for this implementation.")
        if self.synthetic_record_count != 10_000:
            raise ValueError(
                "synthetic_record_count must be 10,000 per the paper; "
                f"got {self.synthetic_record_count}."
            )


def load_denn_ctgan_config(path: str | Path) -> DennCtganConfig:
    """Load DENN-CTGAN settings from ``configs/earthesnd/synthetic_ensemble.yaml``."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if not isinstance(payload, dict) or "synthetic" not in payload:
        raise ValueError("YAML must contain a 'synthetic' mapping.")
    return denn_ctgan_config_from_mapping(payload["synthetic"])


def denn_ctgan_config_from_mapping(payload: Mapping[str, Any]) -> DennCtganConfig:
    """Parse a synthetic-section mapping into :class:`DennCtganConfig`."""
    return DennCtganConfig(
        model=str(payload["model"]),
        synthetic_record_count=int(payload["synthetic_record_count"]),
        input=str(payload["input"]),
        generator_architecture=payload.get("generator_architecture"),
        discriminator_architecture=payload.get("discriminator_architecture"),
        training_hyperparameters=payload.get("training_hyperparameters"),
        t_sne_parameters=payload.get("t_sne_parameters"),
    )


def _require_resolved_training_config(config: DennCtganConfig) -> None:
    missing: list[str] = []
    if config.generator_architecture is None:
        missing.append("generator_architecture")
    if config.discriminator_architecture is None:
        missing.append("discriminator_architecture")
    if config.training_hyperparameters is None:
        missing.append("training_hyperparameters")
    if missing:
        raise NotImplementedError(
            "DENN-CTGAN training is blocked until the following settings are "
            f"resolved as project assumptions: {', '.join(missing)}. "
            "They are not specified in the paper (RE §7.1, §16)."
        )


class DennCtgan:
    """DENN-CTGAN wrapper with train-only fit and fixed 10,000-row sampling."""

    def __init__(self, config: DennCtganConfig) -> None:
        self.config = config
        self._is_fitted = False

    def fit(
        self,
        tab_act: np.ndarray,
        y_act: np.ndarray,
        *,
        split: str = "train",
        record_splits: list[str] | None = None,
    ) -> "DennCtgan":
        """Fit on real training tabular features and targets only.

        Args:
            tab_act: Training feature matrix ``Tab_act``.
            y_act: Training targets ``y_act``.
            split: Declared dataset split for the passed rows (must be ``train``).
            record_splits: Optional per-row split labels; every value must be
                ``train`` when supplied.

        Trace: RE §7.1 — synthetic generation uses training data only.
        """
        assert_training_split_only(split)
        if record_splits is not None:
            assert_all_training_splits(record_splits)

        tab_act = np.asarray(tab_act, dtype=float)
        y_act = np.asarray(y_act, dtype=float)
        if tab_act.ndim != 2:
            raise ValueError("tab_act must be a two-dimensional array.")
        if y_act.ndim != 1 or tab_act.shape[0] != y_act.shape[0]:
            raise ValueError("tab_act row count must match y_act length.")

        _require_resolved_training_config(self.config)
        # Unreachable until CTGAN architecture/training settings are approved.
        self._is_fitted = True
        return self

    def sample(
        self,
        n_samples: int | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Generate synthetic tabular rows ``{Tab_syn | y_syn}``.

        Args:
            n_samples: Row count. When omitted, uses ``synthetic_record_count``
                (10,000). Any other value is rejected.

        Returns:
            ``(Tab_syn, y_syn)`` arrays.

        Raises:
            ValueError: If ``n_samples`` differs from the configured paper count.
            NotImplementedError: While GAN architecture/training remain unresolved.
        """
        requested = self.config.synthetic_record_count if n_samples is None else n_samples
        if requested != 10_000:
            raise ValueError(
                "DENN-CTGAN must request exactly 10,000 synthetic records; "
                f"got {requested}."
            )
        if not self._is_fitted:
            raise RuntimeError("DennCtgan.sample called before fit.")
        _require_resolved_training_config(self.config)
        raise AssertionError("unreachable after _require_resolved_training_config")

    def visualize_tsne(
        self,
        tab_real: np.ndarray,
        tab_syn: np.ndarray,
    ) -> None:
        """Visualize real versus synthetic tabular data (paper t-SNE diagnostic).

        Trace: RE §7.1.
        """
        if self.config.t_sne_parameters is None:
            raise NotImplementedError(
                "t-SNE visualization is blocked until t_sne_parameters are "
                "declared as a project assumption (RE §7.1, §16)."
            )
        raise NotImplementedError(
            "t-SNE plotting is not implemented; parameters are declared but "
            "visualization backend is unresolved."
        )
