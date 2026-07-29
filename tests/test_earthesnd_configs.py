"""Configuration-contract tests for the EarthESND Phase 1 foundation."""

from pathlib import Path

import yaml


CONFIG_DIR = Path("configs/earthesnd")


def load_config(name: str) -> dict:
    with (CONFIG_DIR / name).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_data_config_preserves_paper_values_and_unresolved_fields() -> None:
    config = load_config("data.yaml")

    assert config["japan"]["sampling_rate_hz"] == 100
    assert config["japan"]["components"] == ["NS", "EW", "UD"]
    assert config["windows_seconds"] == [2, 3, 4, 5, 6]
    assert config["split"] == {
        "train": 0.70,
        "test": 0.15,
        "validation": 0.15,
        "stratification_bins": "np.arange(3.0, 8.5, 0.5)",
        "random_seed": None,
    }
    assert config["japan"]["magnitude_max"] is None
    assert config["manifest_path"] is None


def test_later_phase_configs_preserve_unspecified_values_as_null() -> None:
    preprocessing = load_config("preprocessing.yaml")
    model = load_config("model.yaml")
    synthetic_ensemble = load_config("synthetic_ensemble.yaml")
    evaluation = load_config("evaluation.yaml")

    assert preprocessing["sta_lta"]["short_window"] is None
    assert model["esn"]["layer_count"] is None
    assert synthetic_ensemble["ensemble"]["aggregation_weights"] is None
    assert evaluation["timing_environment"] is None
