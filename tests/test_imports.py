from src.main import main
from src.utils.logging_config import configure_logging, get_logger


def test_imports_and_logging_configuration():
    logger = get_logger("test")
    configure_logging()
    assert logger.name == "test"
    assert callable(main)
