
from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass(frozen=True)
class ESNConfig:
    """Configuration for the Echo State Network.

    This dataclass holds the hyperparameters for the ESN. The parameters are
    derived from the paper, but specific numerical values are often not provided.
    In such cases, they are exposed here to be set by the user.

    Attributes:
        reservoir_size: The number of neurons in the reservoir (N_res).
            Not specified in the paper, must be configured.
        spectral_radius: The desired spectral radius of the recurrent weight
            matrix (rho_target). Paper-specified concept, value not provided.
        input_scaling: The scaling factor for the input weights.
            Not specified in the paper, must be configured.
        sparsity: The fraction of recurrent weights to set to zero.
            Not specified in the paper, must be configured.
        leak_rate: The leak rate (alpha) of the reservoir neurons. The paper
            provides a range and per-window values, but the exact application
            is ambiguous. This is a configurable project assumption.
        random_seed: Seed for the random number generator to ensure
            reproducibility. Not specified in the paper.
    """
    reservoir_size: int
    spectral_radius: float
    input_scaling: float
    sparsity: float
    leak_rate: float
    random_seed: Optional[int] = None

    def __post_init__(self):
        """Validates the ESN configuration."""
        if self.reservoir_size <= 0:
            raise ValueError("reservoir_size must be positive.")
        if self.spectral_radius <= 0:
            raise ValueError("spectral_radius must be positive.")
        if self.input_scaling < 0:
            raise ValueError("input_scaling must be non-negative.")
        if not 0 <= self.sparsity <= 1:
            raise ValueError("sparsity must be between 0 and 1.")
        if not 0 <= self.leak_rate <= 1:
            raise ValueError("leak_rate must be between 0 and 1.")


def _create_recurrent_weights(config: ESNConfig) -> np.ndarray:
    """
    Creates and scales the recurrent weight matrix (W_res).

    The matrix is initialized from a standard normal distribution, made sparse,
    and then scaled to the desired spectral radius as per Eq. 2 in the spec.

    Args:
        config: The ESN configuration.

    Returns:
        The recurrent weight matrix.
    """
    rng = np.random.default_rng(config.random_seed)
    weights = rng.standard_normal(
        (config.reservoir_size, config.reservoir_size)
    )

    # Apply sparsity by creating a boolean mask
    mask = rng.random((config.reservoir_size, config.reservoir_size)) > config.sparsity
    weights *= mask

    # Scale by spectral radius to ensure the echo state property
    current_spectral_radius = np.max(np.abs(np.linalg.eigvals(weights)))
    if current_spectral_radius > 0:
        weights = weights * (config.spectral_radius / current_spectral_radius)

    return weights


def _create_input_weights(config: ESNConfig, input_size: int) -> np.ndarray:
    """
    Creates the input weight matrix (W_in).

    The matrix is initialized from a uniform distribution and scaled.

    Args:
        config: The ESN configuration.
        input_size: The feature dimension of the input signal.

    Returns:
        The input weight matrix.
    """
    rng = np.random.default_rng(config.random_seed)
    weights = rng.uniform(-1, 1, (config.reservoir_size, input_size))
    return weights * config.input_scaling


class Reservoir:
    """
    ESN Reservoir, containing the weight matrices.

    This class encapsulates the fixed random weight matrices of the ESN,
    including the input weights (W_in) and recurrent weights (W_res).

    Attributes:
        config: The ESN configuration.
        input_weights: The input weight matrix.
        recurrent_weights: The recurrent weight matrix.
    """

    def __init__(self, config: ESNConfig, input_size: int):
        self.config = config
        self.input_weights: np.ndarray = _create_input_weights(config, input_size)
        self.recurrent_weights: np.ndarray = _create_recurrent_weights(config)


class ESN:
    """
    Echo State Network model.

    This class implements the core ESN logic, including state initialization
    and the forward pass to generate reservoir states from an input sequence.
    The implementation follows the equations and architecture described in the
    project's reverse-engineering documents.

    Attributes:
        config: The ESN configuration.
        input_size: The feature dimension of the input signal.
        reservoir: The ESN reservoir containing the weight matrices.
        state: The current state of the reservoir, initialized to zeros.
    """

    def __init__(self, config: ESNConfig, input_size: int):
        self.config = config
        self.input_size = input_size
        self.reservoir = Reservoir(config, input_size)
        self.state: np.ndarray = np.zeros(config.reservoir_size)

    def forward(self, input_sequence: np.ndarray) -> np.ndarray:
        """
        Performs a forward pass through the ESN, generating reservoir states.

        Args:
            input_sequence: A 2D numpy array of shape (n_timesteps, n_features).

        Returns:
            A 2D numpy array of shape (n_timesteps, reservoir_size)
            containing the sequence of reservoir states.

        Raises:
            ValueError: If the input_sequence is not a 2D NumPy array or if
                its feature dimension does not match the configured input_size.
        """
        if not isinstance(input_sequence, np.ndarray):
            raise ValueError("input_sequence must be a NumPy ndarray.")
        if input_sequence.ndim != 2:
            raise ValueError("input_sequence must be a 2D array.")
        if input_sequence.shape[1] != self.input_size:
            raise ValueError(
                f"Input feature dimension {input_sequence.shape[1]} does not match "
                f"configured input_size {self.input_size}."
            )

        n_timesteps = input_sequence.shape[0]
        states = np.zeros((n_timesteps, self.config.reservoir_size))

        # Iterate through the time steps of the input sequence
        for t in range(n_timesteps):
            self.state = self._update_state(self.state, input_sequence[t])
            states[t] = self.state

        return states

    def _update_state(self, current_state: np.ndarray, input_vector: np.ndarray) -> np.ndarray:
        """
        Updates the reservoir state according to the ESN state update equation.

        This implementation directly follows Eq. 1 from the reverse-engineering
        specification:
        h_(t+1) = (1 - alpha) * h_t + alpha * tanh(W_in * x_t + W_res * h_t)

        This is a documented project assumption based on the paper's description.

        Args:
            current_state: The reservoir state at time t.
            input_vector: The input vector at time t.

        Returns:
            The updated reservoir state at time t+1.
        """
        pre_activation = (
            self.reservoir.recurrent_weights @ current_state
            + self.reservoir.input_weights @ input_vector
        )
        tanh_activation = np.tanh(pre_activation)

        return (1 - self.config.leak_rate) * current_state + self.config.leak_rate * tanh_activation