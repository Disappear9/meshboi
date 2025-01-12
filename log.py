import logging
from logging.handlers import RotatingFileHandler
import os
import sys


def is_debug():
    return os.getenv("DEBUG", "false").lower() == "true"


# Create a log directory if it doesn't exist
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

log_filename = os.path.join(log_dir, "meshboi.log")

# Create formatters and handlers
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Create and configure handlers
console_handler = logging.StreamHandler(sys.stdout)
file_handler = RotatingFileHandler(
    filename=log_filename,
    maxBytes=5 * 1024 * 1024,  # 5MB per file
    backupCount=5,  # Keep 5 backup files
    encoding="utf-8",
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO if not is_debug() else logging.DEBUG)
# Prevent log propagation to avoid duplicate messages
logger.propagate = False
logger.addHandler(console_handler)
logger.addHandler(file_handler)
