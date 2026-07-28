"""Entry point for the AMGCR Earthquake Research project."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils.logging_config import configure_logging, get_logger


def main() -> None:
    """Run the initial project bootstrap check."""
    configure_logging()
    logger = get_logger(__name__)
    logger.info("AMGCR Earthquake Research initialized")
    logger.info("Project root: %s", ROOT)


if __name__ == "__main__":
    main()
