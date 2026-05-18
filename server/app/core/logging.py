import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """Point the root logger at stdout with a timestamped, human-readable format."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        stream=sys.stdout,
        force=True,  # Replace any handlers uvicorn already installed
    )
