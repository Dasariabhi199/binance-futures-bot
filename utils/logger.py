"""
Application logging configuration.

This module creates a centralized logger that writes logs to:
1. Console
2. File (logs/trading.log)

Every module in the application should import
setup_logger() from here.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# -------------------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------------------

LOG_DIRECTORY = "logs"
LOG_FILE_NAME = "trading.log"
LOG_FILE_PATH = os.path.join(LOG_DIRECTORY, LOG_FILE_NAME)

LOGGER_NAME = "TradingBot"

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(filename)s | "
    "%(funcName)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger() -> logging.Logger:
    """
    Configure and return the application logger.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """

    # Create logs directory if it doesn't exist
    os.makedirs(LOG_DIRECTORY, exist_ok=True)

    logger = logging.getLogger(LOGGER_NAME)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    # ---------------- Console Handler ----------------

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # ---------------- File Handler ----------------

    file_handler = RotatingFileHandler(
        filename=LOG_FILE_PATH,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    logger.info("Logger initialized successfully.")

    return logger