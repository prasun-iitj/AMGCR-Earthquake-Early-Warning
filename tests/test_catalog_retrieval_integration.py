from pathlib import Path

from src.acquisition.catalog_client import CatalogClient
from src.acquisition.config_loader import AcquisitionConfigLoader


def test_integration_catalog_client_with_config_file():
    config_path = Path("configs/acquisition_config.yaml")
    loader = AcquisitionConfigLoader(config_path)
    config = loader.load()
    client = CatalogClient(config)

    assert client.config["catalog"]["enabled"] is True
    assert client.build_query()["limit"] == 10
