
import numpy as np
import pytest

from src.models.esn import ESN, ESNConfig, _create_input_weights, _create_recurrent_weights


def test_esn_config():
    """Tests the ESNConfig dataclass."""
    config = ESNConfig(
        reservoir_size=100,
        spectral_radius=0.9,
        input_scaling=0.5,
        sparsity=0.1,
        leak_rate=0.3,
        random_seed=42,
    )
    assert config.reservoir_size == 100
    assert config.spectral_radius == 0.9
    assert config.input_scaling == 0.5
    assert config.sparsity == 0.1
    assert config.leak_rate == 0.3
    assert config.random_seed == 42


def test_recurrent_weights_reproducibility():
    """Tests that recurrent weight initialization is reproducible."""
    config1 = ESNConfig(
        reservoir_size=100,
        spectral_radius=0.9,
        input_scaling=0.5,
        sparsity=0.1,
        leak_rate=0.3,
        random_seed=42,
    )
    config2 = ESNConfig(
        reservoir_size=100,
        spectral_radius=0.9,
        input_scaling=0.5,
        sparsity=0.1,
        leak_rate=0.3,
        random_seed=42,
    )
    weights1 = _create_recurrent_weights(config1)
    weights2 = _create_recurrent_weights(config2)
    np.testing.assert_array_equal(weights1, weights2)


def test_input_weights_reproducibility():
    """Tests that input weight initialization is reproducible."""
    config1 = ESNConfig(
        reservoir_size=100,
        spectral_radius=0.9,
        input_scaling=0.5,
        sparsity=0.1,
        leak_rate=0.3,
        random_seed=42,
    )
    config2 = ESNConfig(
        reservoir_size=100,
        spectral_radius=0.9,
        input_scaling=0.5,
        sparsity=0.1,
        leak_rate=0.3,
        random_seed=42,
    )
    weights1 = _create_input_weights(config1, input_size=10)
    weights2 = _create_input_weights(config2, input_size=10)
    np.testing.assert_array_equal(weights1, weights2)


def test_recurrent_weights_spectral_radius():
    """Tests that the spectral radius of the recurrent weights is correctly set."""
    config = ESNConfig(
        reservoir_size=100,
        spectral_radius=0.9,
        input_scaling=0.5,
        sparsity=0.1,
        leak_rate=0.3,
        random_seed=42,
    )
    weights = _create_recurrent_weights(config)
    spectral_radius = np.max(np.abs(np.linalg.eigvals(weights)))
    assert np.isclose(spectral_radius, config.spectral_radius)


def test_esn_state_update():
    """Tests the ESN state update equation."""
    config = ESNConfig(
        reservoir_size=2,
        spectral_radius=0.9,
        input_scaling=0.5,
        sparsity=0.0,
        leak_rate=0.3,
        random_seed=42,
    )
    esn = ESN(config, input_size=2)

    # Set weights manually for a predictable outcome
    esn.reservoir.recurrent_weights = np.array([[0.1, 0.2], [0.3, 0.4]])
    esn.reservoir.input_weights = np.array([[0.5, 0.6], [0.7, 0.8]])

    initial_state = np.array([0.1, 0.2])
    input_vector = np.array([0.5, 0.5])

    # Manual calculation
    pre_activation = (
        esn.reservoir.recurrent_weights @ initial_state
        + esn.reservoir.input_weights @ input_vector
    )
    tanh_activation = np.tanh(pre_activation)
    expected_next_state = (
        (1 - config.leak_rate) * initial_state
        + config.leak_rate * tanh_activation
    )

    next_state = esn._update_state(initial_state, input_vector)
    np.testing.assert_allclose(next_state, expected_next_state)


@pytest.mark.parametrize(
    "invalid_params, error_message",
    [
        ({"reservoir_size": 0}, "reservoir_size must be positive."),
        ({"reservoir_size": -1}, "reservoir_size must be positive."),
        ({"spectral_radius": 0}, "spectral_radius must be positive."),
        ({"spectral_radius": -0.9}, "spectral_radius must be positive."),
        ({"input_scaling": -0.1}, "input_scaling must be non-negative."),
        ({"sparsity": -0.1}, "sparsity must be between 0 and 1."),
        ({"sparsity": 1.1}, "sparsity must be between 0 and 1."),
        ({"leak_rate": -0.1}, "leak_rate must be between 0 and 1."),
        ({"leak_rate": 1.1}, "leak_rate must be between 0 and 1."),
    ],
)
def test_esn_config_validation(invalid_params, error_message):
    """Tests that ESNConfig raises ValueError for invalid parameters."""
    params = {
        "reservoir_size": 100,
        "spectral_radius": 0.9,
        "input_scaling": 0.5,
        "sparsity": 0.1,
        "leak_rate": 0.3,
        "random_seed": 42,
    }
    params.update(invalid_params)
    with pytest.raises(ValueError, match=error_message):
        ESNConfig(**params)


def test_forward_input_validation():
    """Tests input validation in the ESN.forward method."""
    config = ESNConfig(
        reservoir_size=10,
        spectral_radius=0.9,
        input_scaling=0.5,
        sparsity=0.1,
        leak_rate=0.3,
        random_seed=42,
    )
    esn = ESN(config, input_size=5)

    with pytest.raises(ValueError, match="input_sequence must be a NumPy ndarray."):
        esn.forward([1, 2, 3])

    with pytest.raises(ValueError, match="input_sequence must be a 2D array."):
        esn.forward(np.array([1, 2, 3]))

    with pytest.raises(ValueError, match="Input feature dimension 3 does not match"):
        esn.forward(np.array([[1, 2, 3]]))