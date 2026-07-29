"""EarthESND model wrapper, fusion, and configuration tests."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from src.models.dendritic import build_dendritic_readout
from src.models.earthesnd import EarthESNDModel
from src.models.earthesnd_config import (
    DennArchitectureConfig,
    DennWindowSettings,
    build_esn_config,
    load_earthesnd_model_config,
    require_denn_operational_settings,
    require_training_settings,
)
from src.models.esn import ESN, ESNConfig
from src.processing.features import VerticalPWaveFeatures
from src.processing.fusion import concatenate_terminal_state_and_features


def _operational_denn() -> DennArchitectureConfig:
    windows = {
        str(seconds): DennWindowSettings(
            branches=2 if seconds in {2, 3, 6} else 3,
            reported_sparsity={2: 0.1, 3: 0.1, 4: 0.2, 5: 0.1, 6: 0.1}[seconds],
        )
        for seconds in (2, 3, 4, 5, 6)
    }
    return DennArchitectureConfig(
        layer_widths=(64, 1),
        activations=("gelu", "linear"),
        branch_connectivity_method="bernoulli_retained_fraction",
        local_branch_nonlinearity="linear",
        mask_learning=False,
        windows=windows,
    )


def test_fusion_vector_concatenates_terminal_state_and_features() -> None:
    terminal = np.array([1.0, 2.0, 3.0])
    tabular = VerticalPWaveFeatures(
        tau_c=0.1,
        ID2=0.2,
        IV2=0.3,
        PI=0.4,
        RSSCV=0.5,
        Tva=0.6,
        CAV=0.7,
    )
    fused = concatenate_terminal_state_and_features(terminal, tabular)
    assert fused.shape == (10,)
    np.testing.assert_allclose(fused[:3], terminal)
    np.testing.assert_allclose(fused[3:], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])


def test_load_earthesnd_model_config_window_values() -> None:
    config = load_earthesnd_model_config("configs/earthesnd/model.yaml", window_seconds=3)
    assert config.esn_leak_rate == 1.0
    assert config.denn_window.branches == 2
    assert config.training.epochs == 50
    assert config.training.batch_size == 512
    assert config.training.learning_rate == 0.0014


def test_model_yaml_denn_operational_fields_remain_null() -> None:
    config = load_earthesnd_model_config("configs/earthesnd/model.yaml", window_seconds=2)
    with pytest.raises(NotImplementedError):
        require_denn_operational_settings(config.denn)


def test_esn_terminal_state_only() -> None:
    esn_config = ESNConfig(
        reservoir_size=4,
        spectral_radius=0.8,
        input_scaling=0.2,
        sparsity=0.0,
        leak_rate=0.5,
        random_seed=1,
    )
    esn = ESN(esn_config, input_size=9)
    sequence = np.random.default_rng(0).standard_normal((5, 9))
    terminal = esn.terminal_state(sequence)
    states = esn.forward(sequence)
    np.testing.assert_array_equal(terminal, states[-1])


def test_earthesnd_model_predict_returns_scalar() -> None:
    model_config = load_earthesnd_model_config("configs/earthesnd/model.yaml", window_seconds=5)
    operational = _operational_denn()
    model_config = replace(
        model_config,
        denn=operational,
        denn_window=operational.windows["5"],
    )
    esn_config = build_esn_config(
        model_config,
        reservoir_size=8,
        spectral_radius=0.9,
        input_scaling=0.3,
        sparsity=0.1,
        random_seed=2,
    )
    model = EarthESNDModel.from_config(model_config, esn_config, readout_random_seed=3)
    waveform = np.random.default_rng(4).standard_normal((20, 9))
    tabular = np.linspace(0.1, 0.7, 7)
    prediction = model.predict(waveform, tabular)
    assert isinstance(prediction, float)


def test_earthesnd_model_fit_blocks_unresolved_adam_settings() -> None:
    model_config = load_earthesnd_model_config("configs/earthesnd/model.yaml", window_seconds=2)
    operational = _operational_denn()
    model_config = replace(
        model_config,
        denn=operational,
        denn_window=operational.windows["2"],
    )
    esn_config = build_esn_config(
        model_config,
        reservoir_size=6,
        spectral_radius=0.9,
        input_scaling=0.2,
        sparsity=0.1,
        random_seed=1,
    )
    model = EarthESNDModel.from_config(model_config, esn_config, readout_random_seed=2)
    with pytest.raises(NotImplementedError, match="EarthESNDModel.fit is blocked"):
        model.fit(
            np.zeros((2, 10, 9)),
            np.zeros((2, 7)),
            np.zeros(2),
        )


def test_require_training_settings_with_declared_adam() -> None:
    config = load_earthesnd_model_config("configs/earthesnd/model.yaml", window_seconds=4)
    training = replace(
        config.training,
        adam_betas=(0.9, 0.999),
        adam_epsilon=1e-8,
        weight_decay=0.0,
    )
    require_training_settings(training)


def test_earthesnd_from_yaml_with_overrides() -> None:
    model = EarthESNDModel.from_yaml(
        "configs/earthesnd/model.yaml",
        window_seconds=6,
        reservoir_size=5,
        spectral_radius=0.85,
        input_scaling=0.25,
        sparsity=0.05,
        esn_random_seed=10,
        readout_random_seed=11,
        denn_overrides=_operational_denn(),
    )
    waveform = np.random.default_rng(12).standard_normal((12, 9))
    assert isinstance(model.predict(waveform, np.ones(7)), float)
