from pathlib import Path
from unittest.mock import patch

import pytest

from src.acquisition.catalog_client import CatalogClient
from src.acquisition.exceptions import AcquisitionConfigurationError


def test_catalog_client_builds_query_from_config():
    config = {
        "provider": "iris",
        "network": "IU",
        "station": "ANMO",
        "channel": "BHZ",
        "location": "",
        "start_time": "2024-01-01T00:00:00",
        "end_time": "2024-01-02T00:00:00",
        "magnitude": {"minimum": 5.0, "maximum": 7.0},
        "catalog": {"enabled": True, "format": "quakeml", "limit": 3, "output_dir": "data/raw/catalogs"},
        "output": {"raw_dir": "data/raw", "processed_dir": "data/processed", "logs_dir": "logs"},
    }

    client = CatalogClient(config)
    query = client.build_query()

    assert query["starttime"] == "2024-01-01T00:00:00"
    assert query["endtime"] == "2024-01-02T00:00:00"
    assert query["minmagnitude"] == 5.0
    assert query["limit"] == 3
    assert query["network"] == "IU"


def test_catalog_client_requires_enabled_catalog():
    config = {
        "provider": "iris",
        "network": "IU",
        "station": "ANMO",
        "channel": "BHZ",
        "location": "",
        "start_time": "2024-01-01T00:00:00",
        "end_time": "2024-01-02T00:00:00",
        "magnitude": {"minimum": 5.0, "maximum": 7.0},
        "catalog": {"enabled": False, "format": "quakeml", "limit": 3, "output_dir": "data/raw/catalogs"},
        "output": {"raw_dir": "data/raw", "processed_dir": "data/processed", "logs_dir": "logs"},
    }

    client = CatalogClient(config)
    with pytest.raises(AcquisitionConfigurationError):
        client.retrieve_catalog()


def test_catalog_client_resolves_fdsn_alias_to_working_provider():
    config = {
        "provider": "fdsn",
        "network": "IU",
        "station": "ANMO",
        "channel": "BHZ",
        "location": "",
        "start_time": "2024-01-01T00:00:00",
        "end_time": "2024-01-02T00:00:00",
        "magnitude": {"minimum": 5.0, "maximum": 7.0},
        "catalog": {"enabled": True, "format": "quakeml", "limit": 3, "output_dir": "data/raw/catalogs"},
        "output": {"raw_dir": "data/raw", "processed_dir": "data/processed", "logs_dir": "logs"},
    }

    client = CatalogClient(config)

    with patch("src.acquisition.catalog_client.Client") as mock_client:
        client._get_client("fdsn", 30)

    mock_client.assert_called_once_with("https://earthquake.usgs.gov", timeout=30)


def test_catalog_client_removes_unsupported_query_parameters_for_usgs():
    config = {
        "provider": "fdsn",
        "network": "IU",
        "station": "ANMO",
        "channel": "BHZ",
        "location": "",
        "start_time": "2024-01-01T00:00:00",
        "end_time": "2024-01-02T00:00:00",
        "magnitude": {"minimum": 5.0, "maximum": 7.0},
        "catalog": {"enabled": True, "format": "quakeml", "limit": 3, "output_dir": "data/raw/catalogs"},
        "output": {"raw_dir": "data/raw", "processed_dir": "data/processed", "logs_dir": "logs"},
    }

    client = CatalogClient(config)
    query = client.build_retrieval_query("https://earthquake.usgs.gov")

    assert "network" not in query
    assert "station" not in query
    assert "channel" not in query
    assert "location" not in query
    assert query["minmagnitude"] == 5.0
    assert query["limit"] == 3
