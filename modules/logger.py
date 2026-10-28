
import logging
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Log directory and file
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "simulator.log"

# Create logs directory automatically
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ],
)

logger = logging.getLogger("OSResourceSimulator")


def log_info(message):
    """Log normal information."""
    logger.info(message)


def log_warning(message):
    """Log warning messages."""
    logger.warning(message)


def log_error(message):
    """Log error messages."""
    logger.error(message)


def log_exception(message):
    """Log an exception with traceback."""
    logger.exception(message)
