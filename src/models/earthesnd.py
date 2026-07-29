"""EarthESND ESN + DENN magnitude predictor (``y_esn`` path).

Coordinates fixed-random ESN terminal-state extraction, fusion with tabular
features, and the dendritic readout. Full Adam training is blocked until
omitted optimizer hyperparameters are declared.

Trace: RE §1, §4–§6, §8; Spec R-ESN, R-DENN, R-TRAIN.
"""

from __future__ import annotations

from dataclasses import replace

import numpy as np

from src.models.dendritic import DendriticReadout, build_dendritic_readout
from src.models.earthesnd_config import (
    DennArchitectureConfig,
    EarthESNDModelConfig,
    TrainingConfig,
    build_esn_config,
    load_earthesnd_model_config,
    require_denn_operational_settings,
    require_training_settings,
)
from src.models.esn import ESN, ESNConfig
from src.processing.features import VerticalPWaveFeatures
from src.processing.fusion import concatenate_terminal_state_and_features


class EarthESNDModel:
    """ESN terminal state fused with tabular features and read out by DENN."""

    def __init__(
        self,
        esn: ESN,
        readout: DendriticReadout,
        model_config: EarthESNDModelConfig,
    ) -> None:
        self.esn = esn
        self.readout = readout
        self.model_config = model_config

    @classmethod
    def from_config(
        cls,
        model_config: EarthESNDModelConfig,
        esn_config: ESNConfig,
        *,
        readout_random_seed: int | None = None,
    ) -> "EarthESNDModel":
        """Build model components from resolved ESN settings and declared DENN ops."""
        require_denn_operational_settings(model_config.denn)
        if esn_config.leak_rate != model_config.esn_leak_rate:
            raise ValueError(
                "ESN leak_rate must match the selected window reported leak "
                f"({model_config.esn_leak_rate})."
            )
        esn = ESN(esn_config, input_size=model_config.channel_count)
        fusion_input_dim = esn_config.reservoir_size + 7
        readout = build_dendritic_readout(
            fusion_input_dim,
            model_config.denn,
            model_config.denn_window,
            random_seed=readout_random_seed,
        )
        return cls(esn=esn, readout=readout, model_config=model_config)

    @classmethod
    def from_yaml(
        cls,
        path: str,
        *,
        window_seconds: int,
        reservoir_size: int,
        spectral_radius: float,
        input_scaling: float,
        sparsity: float,
        esn_random_seed: int | None,
        readout_random_seed: int | None = None,
        denn_overrides: DennArchitectureConfig | None = None,
    ) -> "EarthESNDModel":
        """Load ``model.yaml`` and construct the model for one window."""
        model_config = load_earthesnd_model_config(path, window_seconds=window_seconds)
        if denn_overrides is not None:
            model_config = replace(model_config, denn=denn_overrides)
        esn_config = build_esn_config(
            model_config,
            reservoir_size=reservoir_size,
            spectral_radius=spectral_radius,
            input_scaling=input_scaling,
            sparsity=sparsity,
            random_seed=esn_random_seed,
        )
        return cls.from_config(
            model_config,
            esn_config,
            readout_random_seed=readout_random_seed,
        )

    def predict(
        self,
        waveform_tensor: np.ndarray,
        tabular_features: VerticalPWaveFeatures | np.ndarray,
    ) -> float:
        """Predict ``y_esn`` for one ``(T, 9)`` window and tabular feature vector."""
        terminal_state = self._terminal_state(waveform_tensor)
        fusion_vector = concatenate_terminal_state_and_features(terminal_state, tabular_features)
        return self.readout.forward(fusion_vector)

    def fit(
        self,
        waveform_tensors: np.ndarray,
        tabular_features: np.ndarray,
        targets: np.ndarray,
        training: TrainingConfig | None = None,
    ) -> "EarthESNDModel":
        """Train the DENN readout under the paper MSE/Adam schedule.

        ESN recurrent and input weights remain fixed (RE §5.2). Optimizer details
        omitted from the paper must be supplied via ``training`` or
        ``model_config.training``.
        """
        schedule = training or self.model_config.training
        require_training_settings(schedule)
        raise NotImplementedError(
            "Differentiable DENN training with Adam is not implemented yet; "
            "forward inference via predict() is available once DENN operational "
            "settings are declared."
        )

    def _terminal_state(self, waveform_tensor: np.ndarray) -> np.ndarray:
        """Return ``h_T`` only (no intermediate-state concatenation)."""
        states = self.esn.forward(waveform_tensor)
        return states[-1]
