"""Dendritic neural network (DENN) readout for EarthESND.

Implements the masked branch → local transform → branch aggregation → neuron
activation sequence from RE §6.1, and the applied 64/GELU → 1/linear readout
from RE §6.2.

Trace: Spec R-DENN; test_dendritic_equation, test_readout_shape_and_activation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from src.models.earthesnd_config import DennArchitectureConfig, DennWindowSettings, require_denn_operational_settings

ActivationFn = Callable[[np.ndarray], np.ndarray]
LocalPhiFn = Callable[[np.ndarray], np.ndarray]


def gelu(x: np.ndarray) -> np.ndarray:
    """Paper GELU (RE §6.2)."""
    array = np.asarray(x, dtype=float)
    return 0.5 * array * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (array + 0.044715 * array**3)))


def linear_activation(x: np.ndarray) -> np.ndarray:
    return np.asarray(x, dtype=float)


def sigmoid_activation(x: np.ndarray) -> np.ndarray:
    array = np.asarray(x, dtype=float)
    return 1.0 / (1.0 + np.exp(-array))


def gaussian_phi(x: np.ndarray) -> np.ndarray:
    array = np.asarray(x, dtype=float)
    return np.exp(-(array**2))


def resolve_neuron_activation(name: str) -> ActivationFn:
    activations = {
        "gelu": gelu,
        "linear": linear_activation,
    }
    if name not in activations:
        raise ValueError(f"Unsupported neuron activation {name!r}.")
    return activations[name]


def resolve_local_phi(name: str) -> LocalPhiFn:
    mapping = {
        "linear": linear_activation,
        "sigmoid": sigmoid_activation,
        "gaussian": gaussian_phi,
    }
    if name not in mapping:
        raise ValueError(f"Unsupported local branch nonlinearity {name!r}.")
    return mapping[name]


@dataclass
class DendriticBranch:
    """One dendritic branch with fixed connectivity mask."""

    mask: np.ndarray
    weights: np.ndarray
    bias: float
    local_phi: LocalPhiFn

    def response(self, inputs: np.ndarray) -> float:
        """Compute ``phi_j(sum_m S * W * x + b)`` (RE §6.1)."""
        masked_weights = self.mask * self.weights
        weighted_sum = float(masked_weights @ inputs + self.bias)
        return float(self.local_phi(np.array(weighted_sum)))


@dataclass
class DendriticNeuron:
    """Aggregate ``d`` branch responses with a neuron-level activation."""

    branches: tuple[DendriticBranch, ...]
    neuron_activation: ActivationFn
    bias: float

    def forward(self, inputs: np.ndarray) -> float:
        """Apply branch responses, aggregate, activate, add neuron bias."""
        branch_values = np.array([branch.response(inputs) for branch in self.branches], dtype=float)
        aggregated = float(np.sum(branch_values))
        activated = self.neuron_activation(np.array(aggregated))
        return float(activated + self.bias)


@dataclass
class DendriticLayer:
    """Layer output ``[g_{l,1}, ..., g_{l,n_l}]`` (RE §6.1)."""

    neurons: tuple[DendriticNeuron, ...]

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        vector = np.array([neuron.forward(inputs) for neuron in self.neurons], dtype=float)
        return vector.reshape(-1)


@dataclass
class DendriticReadout:
    """Two-layer 64/GELU → 1/linear DENN readout (RE §6.2)."""

    layers: tuple[DendriticLayer, ...]

    def forward(self, fusion_vector: np.ndarray) -> float:
        """Return scalar magnitude prediction ``y_esn``."""
        vector = np.asarray(fusion_vector, dtype=float).reshape(-1)
        for layer in self.layers:
            vector = layer.forward(vector)
        if vector.shape != (1,):
            raise ValueError("Readout must return a single scalar output.")
        return float(vector[0])


def _create_branch_mask(
    input_dim: int,
    *,
    method: str,
    retained_fraction: float,
    rng: np.random.Generator,
) -> np.ndarray:
    if method != "bernoulli_retained_fraction":
        raise ValueError(
            f"Unsupported branch_connectivity_method {method!r}. "
            "Only 'bernoulli_retained_fraction' is implemented as a project assumption."
        )
    if not 0.0 < retained_fraction <= 1.0:
        raise ValueError("retained_fraction must be in (0, 1].")
    mask = rng.random(input_dim) < retained_fraction
    if not np.any(mask):
        mask[rng.integers(0, input_dim)] = True
    return mask.astype(float)


def _init_layer(
    input_dim: int,
    output_dim: int,
    *,
    branch_count: int,
    neuron_activation: ActivationFn,
    local_phi: LocalPhiFn,
    connectivity_method: str,
    retained_fraction: float,
    rng: np.random.Generator,
) -> DendriticLayer:
    neurons: list[DendriticNeuron] = []
    for _ in range(output_dim):
        branches: list[DendriticBranch] = []
        for _ in range(branch_count):
            mask = _create_branch_mask(
                input_dim,
                method=connectivity_method,
                retained_fraction=retained_fraction,
                rng=rng,
            )
            weights = rng.standard_normal(input_dim)
            bias = float(rng.standard_normal())
            branches.append(
                DendriticBranch(mask=mask, weights=weights, bias=bias, local_phi=local_phi)
            )
        neuron = DendriticNeuron(
            branches=tuple(branches),
            neuron_activation=neuron_activation,
            bias=float(rng.standard_normal()),
        )
        neurons.append(neuron)
    return DendriticLayer(neurons=tuple(neurons))


def build_dendritic_readout(
    input_dim: int,
    denn: DennArchitectureConfig,
    window_settings: DennWindowSettings,
    *,
    random_seed: int | None = None,
) -> DendriticReadout:
    """Construct the paper readout once operational DENN settings are declared."""
    require_denn_operational_settings(denn)
    assert denn.branch_connectivity_method is not None
    assert denn.local_branch_nonlinearity is not None

    if tuple(denn.layer_widths) != (64, 1):
        raise ValueError("Expected denn.layer_widths [64, 1].")
    if tuple(denn.activations) != ("gelu", "linear"):
        raise ValueError("Expected denn.activations [gelu, linear].")

    rng = np.random.default_rng(random_seed)
    local_phi = resolve_local_phi(denn.local_branch_nonlinearity)

    first_layer = _init_layer(
        input_dim,
        denn.layer_widths[0],
        branch_count=window_settings.branches,
        neuron_activation=resolve_neuron_activation(denn.activations[0]),
        local_phi=local_phi,
        connectivity_method=denn.branch_connectivity_method,
        retained_fraction=window_settings.reported_sparsity,
        rng=rng,
    )
    second_layer = _init_layer(
        denn.layer_widths[0],
        denn.layer_widths[1],
        branch_count=1,
        neuron_activation=resolve_neuron_activation(denn.activations[1]),
        local_phi=linear_activation,
        connectivity_method=denn.branch_connectivity_method,
        retained_fraction=window_settings.reported_sparsity,
        rng=rng,
    )
    return DendriticReadout(layers=(first_layer, second_layer))
