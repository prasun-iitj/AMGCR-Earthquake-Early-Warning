"""DENN equation and readout tests. Trace: Spec test_dendritic_equation, test_readout_shape_and_activation."""

from __future__ import annotations

import numpy as np
import pytest

from src.models.dendritic import (
    DendriticBranch,
    DendriticNeuron,
    build_dendritic_readout,
    gelu,
    linear_activation,
)
from src.models.earthesnd_config import DennArchitectureConfig, DennWindowSettings


def _operational_denn() -> DennArchitectureConfig:
    windows = {
        label: DennWindowSettings(branches=2 if label in {"2", "3", "6"} else 3, reported_sparsity=0.1)
        for label in ("2", "3", "4", "5", "6")
    }
    return DennArchitectureConfig(
        layer_widths=(64, 1),
        activations=("gelu", "linear"),
        branch_connectivity_method="bernoulli_retained_fraction",
        local_branch_nonlinearity="linear",
        mask_learning=False,
        windows=windows,
    )


def test_dendritic_equation() -> None:
    """Mask → weighted sum → local phi → aggregate → neuron activation → bias."""
    branch = DendriticBranch(
        mask=np.array([1.0, 0.0]),
        weights=np.array([2.0, 3.0]),
        bias=0.5,
        local_phi=linear_activation,
    )
    assert branch.response(np.array([1.0, 4.0])) == pytest.approx(2.5)

    neuron = DendriticNeuron(
        branches=(branch,),
        neuron_activation=linear_activation,
        bias=1.0,
    )
    assert neuron.forward(np.array([1.0, 4.0])) == pytest.approx(3.5)


def test_readout_shape_and_activation() -> None:
    """64/GELU then 1/linear returns a scalar (RE §6.2)."""
    denn = _operational_denn()
    window = denn.windows["4"]
    readout = build_dendritic_readout(
        input_dim=17,
        denn=denn,
        window_settings=window,
        random_seed=0,
    )
    output = readout.forward(np.linspace(-0.5, 0.5, 17))
    assert isinstance(output, float)


def test_gelu_matches_paper_polynomial_form() -> None:
    value = np.array(1.25)
    expected = 0.5 * value * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (value + 0.044715 * value**3)))
    assert gelu(value) == pytest.approx(float(expected))


def test_build_dendritic_readout_blocks_unresolved_operational_settings() -> None:
    denn = DennArchitectureConfig(
        layer_widths=(64, 1),
        activations=("gelu", "linear"),
        branch_connectivity_method=None,
        local_branch_nonlinearity=None,
        mask_learning=None,
        windows={"2": DennWindowSettings(branches=2, reported_sparsity=0.1)},
    )
    with pytest.raises(NotImplementedError, match="DENN readout construction is blocked"):
        build_dendritic_readout(10, denn, denn.windows["2"])
