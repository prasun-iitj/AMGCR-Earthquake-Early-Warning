"""XGBoost / LightGBM / CatBoost tabular ensemble for EarthESND.

Each learner is trained on real training tabular data and on augmented data
(real plus synthetic rows). Tree hyperparameters are not specified in the paper.

Trace: RE §7.2; Spec R-ENS.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, MutableMapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

import numpy as np
import yaml

from src.models.tabular_data import assert_training_split_only


LEARNER_NAMES: tuple[str, ...] = ("xgboost", "lightgbm", "catboost")
TRAINING_SET_NAMES: tuple[str, ...] = ("real", "augmented")
EXPECTED_MODEL_COUNT = 6


class TabularRegressor(Protocol):
    """Minimal learner interface for ensemble members."""

    def fit(self, features: np.ndarray, targets: np.ndarray) -> None: ...

    def predict(self, features: np.ndarray) -> np.ndarray: ...


LearnerFactory = Callable[[str, Mapping[str, Any]], TabularRegressor]


@dataclass(frozen=True, slots=True)
class TabularEnsembleConfig:
    """Configuration contract for the six-model tabular ensemble."""

    learners: tuple[str, ...]
    training_sets: tuple[str, ...]
    expected_model_count: int
    aggregation_weights: Mapping[str, float] | None
    learner_hyperparameters: Mapping[str, Mapping[str, Any]] | None

    def __post_init__(self) -> None:
        if tuple(self.learners) != LEARNER_NAMES:
            raise ValueError(f"learners must be {list(LEARNER_NAMES)}.")
        if tuple(self.training_sets) != TRAINING_SET_NAMES:
            raise ValueError(f"training_sets must be {list(TRAINING_SET_NAMES)}.")
        if self.expected_model_count != EXPECTED_MODEL_COUNT:
            raise ValueError(
                f"expected_model_count must be {EXPECTED_MODEL_COUNT} "
                f"(3 learners × 2 datasets)."
            )


def load_tabular_ensemble_config(path: str | Path) -> TabularEnsembleConfig:
    """Load ensemble settings from ``configs/earthesnd/synthetic_ensemble.yaml``."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if not isinstance(payload, dict) or "ensemble" not in payload:
        raise ValueError("YAML must contain an 'ensemble' mapping.")
    section = payload["ensemble"]
    return TabularEnsembleConfig(
        learners=tuple(section["learners"]),
        training_sets=tuple(section["training_sets"]),
        expected_model_count=int(section["expected_model_count"]),
        aggregation_weights=section.get("aggregation_weights"),
        learner_hyperparameters=section.get("learner_hyperparameters"),
    )


def prediction_key(learner: str, training_set: str) -> str:
    """Return the canonical prediction name for one fitted member."""
    return f"{learner}_{training_set}"


def all_prediction_keys() -> tuple[str, ...]:
    """Ordered keys for the six tree-model outputs."""
    return tuple(
        prediction_key(learner, training_set)
        for learner in LEARNER_NAMES
        for training_set in TRAINING_SET_NAMES
    )


def _require_learner_hyperparameters(config: TabularEnsembleConfig) -> Mapping[str, Mapping[str, Any]]:
    if config.learner_hyperparameters is None:
        raise NotImplementedError(
            "Tabular ensemble training is blocked until learner_hyperparameters "
            "are declared as project assumptions (RE §7.2, §16)."
        )
    missing = [name for name in LEARNER_NAMES if name not in config.learner_hyperparameters]
    if missing:
        raise NotImplementedError(
            "Tabular ensemble training requires hyperparameters for each learner; "
            f"missing: {', '.join(missing)}."
        )
    return config.learner_hyperparameters


def _default_learner_factory(learner: str, hyperparameters: Mapping[str, Any]) -> TabularRegressor:
    if learner == "xgboost":
        import xgboost as xgb

        return xgb.XGBRegressor(**dict(hyperparameters))
    if learner == "lightgbm":
        import lightgbm as lgb

        return lgb.LGBMRegressor(**dict(hyperparameters))
    if learner == "catboost":
        from catboost import CatBoostRegressor

        return CatBoostRegressor(**dict(hyperparameters))
    raise ValueError(f"Unsupported learner {learner!r}.")


class TabularEnsemble:
    """Train six regressors and expose their predictions separately."""

    def __init__(
        self,
        config: TabularEnsembleConfig,
        *,
        learner_factory: LearnerFactory | None = None,
    ) -> None:
        self.config = config
        self._learner_factory = learner_factory or _default_learner_factory
        self._models: MutableMapping[str, TabularRegressor] = {}

    def fit(
        self,
        tab_real: np.ndarray,
        y_real: np.ndarray,
        tab_augmented: np.ndarray,
        y_augmented: np.ndarray,
        *,
        split: str = "train",
    ) -> "TabularEnsemble":
        """Fit all six models on training tabular data only.

        Args:
            tab_real: Real training features ``Tab_act``.
            y_real: Real training targets.
            tab_augmented: Augmented training features ``Tab_aug``.
            y_augmented: Augmented training targets ``y_aug``.
            split: Declared split label (must be ``train``).

        Trace: RE §7.2 — learners trained on real and augmented training sets.
        """
        assert_training_split_only(split)
        hyperparameters = _require_learner_hyperparameters(self.config)

        datasets = {
            "real": (np.asarray(tab_real, dtype=float), np.asarray(y_real, dtype=float)),
            "augmented": (
                np.asarray(tab_augmented, dtype=float),
                np.asarray(y_augmented, dtype=float),
            ),
        }
        for training_set, (features, targets) in datasets.items():
            if features.ndim != 2 or targets.ndim != 1:
                raise ValueError("Features must be 2D and targets 1D.")
            if features.shape[0] != targets.shape[0]:
                raise ValueError("Feature and target row counts must match.")

        self._models.clear()
        for learner in LEARNER_NAMES:
            params = hyperparameters[learner]
            for training_set in TRAINING_SET_NAMES:
                features, targets = datasets[training_set]
                model = self._learner_factory(learner, params)
                model.fit(features, targets)
                self._models[prediction_key(learner, training_set)] = model
        return self

    def predict_six(self, features: np.ndarray) -> dict[str, float]:
        """Return one scalar prediction per ensemble member for a single row.

        Args:
            features: One sample with shape ``(n_features,)`` or ``(1, n_features)``.

        Returns:
            Mapping with exactly six keys (three learners × two training sets).
        """
        if not self._models:
            raise RuntimeError("TabularEnsemble.predict_six called before fit.")

        matrix = np.asarray(features, dtype=float)
        if matrix.ndim == 1:
            matrix = matrix.reshape(1, -1)
        if matrix.shape[0] != 1:
            raise ValueError("predict_six expects a single sample.")

        outputs: dict[str, float] = {}
        for key in all_prediction_keys():
            prediction = self._models[key].predict(matrix)
            outputs[key] = float(np.asarray(prediction).reshape(-1)[0])
        return outputs
