"""Phase 5 synthetic generation, tabular ensemble, and aggregation tests.

Trace: Spec test_synthetic_count, test_six_ensemble_predictions,
test_aggregation_requires_weights; RE §7.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pytest

from src.models.aggregation import aggregate_predictions
from src.models.denn_ctgan import DennCtgan, DennCtganConfig
from src.models.tabular_data import build_augmented_tabular
from src.models.tabular_ensemble import (
    EXPECTED_MODEL_COUNT,
    TabularEnsemble,
    TabularEnsembleConfig,
    all_prediction_keys,
    load_tabular_ensemble_config,
)


@dataclass
class _RecordingLearner:
    """Minimal regressor that stores training-set size for leakage checks."""

    training_rows: int = 0

    def fit(self, features: np.ndarray, targets: np.ndarray) -> None:
        self.training_rows = int(features.shape[0])

    def predict(self, features: np.ndarray) -> np.ndarray:
        return np.full(features.shape[0], 4.5, dtype=float)


def _learner_factory(_learner: str, _params: dict) -> _RecordingLearner:
    return _RecordingLearner()


def _resolved_ctgan_config() -> DennCtganConfig:
    return DennCtganConfig(
        model="denn_ctgan",
        synthetic_record_count=10_000,
        input="vertical_component_tabular_features_and_training_target",
        generator_architecture={"layers": "project_assumption"},
        discriminator_architecture={"layers": "project_assumption"},
        training_hyperparameters={"epochs": 1},
        t_sne_parameters=None,
    )


def _ensemble_config_with_hyperparameters() -> TabularEnsembleConfig:
    params = {"n_estimators": 1, "max_depth": 1}
    return TabularEnsembleConfig(
        learners=("xgboost", "lightgbm", "catboost"),
        training_sets=("real", "augmented"),
        expected_model_count=EXPECTED_MODEL_COUNT,
        aggregation_weights=None,
        learner_hyperparameters={
            "xgboost": params,
            "lightgbm": params,
            "catboost": params,
        },
    )


def test_synthetic_count() -> None:
    """Requests exactly 10,000 synthetic rows. Trace: RE §7.1."""
    config = _resolved_ctgan_config()
    assert config.synthetic_record_count == 10_000

    generator = DennCtgan(config)
    with pytest.raises(ValueError, match="exactly 10,000"):
        generator.sample(n_samples=9_999)


def test_denn_ctgan_fit_blocks_unresolved_architecture() -> None:
    config = DennCtganConfig(
        model="denn_ctgan",
        synthetic_record_count=10_000,
        input="vertical_component_tabular_features_and_training_target",
        generator_architecture=None,
        discriminator_architecture=None,
        training_hyperparameters=None,
        t_sne_parameters=None,
    )
    model = DennCtgan(config)
    tab = np.zeros((5, 7))
    y = np.zeros(5)
    with pytest.raises(NotImplementedError, match="DENN-CTGAN training is blocked"):
        model.fit(tab, y)


def test_denn_ctgan_fit_rejects_non_training_split() -> None:
    model = DennCtgan(_resolved_ctgan_config())
    tab = np.zeros((3, 7))
    y = np.zeros(3)
    with pytest.raises(ValueError, match="training data only"):
        model.fit(tab, y, split="test")
    with pytest.raises(ValueError, match="training data only"):
        model.fit(tab, y, record_splits=["train", "validation"])


def test_six_ensemble_predictions() -> None:
    """Three learners times two datasets equals six outputs. Trace: RE §7.2."""
    config = _ensemble_config_with_hyperparameters()
    ensemble = TabularEnsemble(config, learner_factory=_learner_factory)

    tab_real = np.random.default_rng(0).standard_normal((20, 7))
    y_real = np.linspace(3.0, 5.0, 20)
    tab_syn = np.random.default_rng(1).standard_normal((10, 7))
    y_syn = np.linspace(3.2, 4.8, 10)
    tab_aug, y_aug = build_augmented_tabular(tab_syn, y_syn, tab_real, y_real)

    ensemble.fit(tab_real, y_real, tab_aug, y_aug)
    predictions = ensemble.predict_six(tab_real[0])

    assert len(predictions) == EXPECTED_MODEL_COUNT
    assert set(predictions) == set(all_prediction_keys())


def test_tabular_ensemble_fit_rejects_non_training_split() -> None:
    config = _ensemble_config_with_hyperparameters()
    ensemble = TabularEnsemble(config, learner_factory=_learner_factory)
    features = np.zeros((4, 7))
    targets = np.zeros(4)
    with pytest.raises(ValueError, match="training data only"):
        ensemble.fit(features, targets, features, targets, split="validation")


def test_aggregation_requires_weights() -> None:
    """No implicit equal-weight aggregation. Trace: RE §7.2, §16."""
    predictions = {
        "y_esn": 4.0,
        **{key: 3.5 for key in all_prediction_keys()},
    }
    with pytest.raises(ValueError, match="declared explicitly"):
        aggregate_predictions(predictions, None)

    with pytest.raises(ValueError, match="non-empty"):
        aggregate_predictions(predictions, {})

    partial_weights = {key: 0.1 for key in list(predictions)[:3]}
    with pytest.raises(ValueError, match="match prediction keys"):
        aggregate_predictions(predictions, partial_weights)


def test_aggregation_with_declared_weights() -> None:
    predictions = {"y_esn": 2.0, "xgboost_real": 4.0}
    weights = {"y_esn": 0.25, "xgboost_real": 0.75}
    result = aggregate_predictions(predictions, weights)
    assert result == pytest.approx(3.5)


def test_synthetic_ensemble_yaml_contract() -> None:
    ensemble_config = load_tabular_ensemble_config("configs/earthesnd/synthetic_ensemble.yaml")
    assert ensemble_config.expected_model_count == 6
    assert ensemble_config.aggregation_weights is None
    assert ensemble_config.learner_hyperparameters is None
