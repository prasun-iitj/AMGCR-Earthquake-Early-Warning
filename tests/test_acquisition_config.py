from pathlib import Path

import pytest

from src.acquisition.config_loader import AcquisitionConfigLoader
from src.acquisition.exceptions import AcquisitionConfigurationError
from src.acquisition.validators import validate_config


def test_config_loader_reads_default_config():
    loader = AcquisitionConfigLoader(Path("configs/acquisition_config.yaml"))
    config = loader.load()

    assert config["provider"] == "fdsn"
    assert config["network"] == "IU"
    assert config["station"] == "ANMO"


def test_validator_accepts_valid_config():
    config = {
        "provider": "fdsn",
        "network": "IU",
        "station": "ANMO",
        "channel": "BHZ",
        "location": "",
        "start_time": "2024-01-01T00:00:00",
        "end_time": "2024-01-02T00:00:00",
        "magnitude": {"minimum": 4.0, "maximum": 6.0},
        "output": {"raw_dir": "data/raw", "processed_dir": "data/processed", "logs_dir": "logs"},
    }

    validate_config(config)


def test_validator_rejects_invalid_time_range():
    config = {
        "provider": "fdsn",
        "network": "IU",
        "station": "ANMO",
        "channel": "BHZ",
        "location": "",
        "start_time": "2024-01-02T00:00:00",
        "end_time": "2024-01-01T00:00:00",
        "magnitude": {"minimum": 4.0, "maximum": 6.0},
        "output": {"raw_dir": "data/raw", "processed_dir": "data/processed", "logs_dir": "logs"},
    }

    with pytest.raises(AcquisitionConfigurationError):
        validate_config(config)
