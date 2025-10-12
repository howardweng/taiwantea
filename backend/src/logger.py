"""
Application Logger Configuration

Centralized logging setup for the application
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = "taiwantea") -> logging.Logger:
    """
    Setup and configure application logger

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(detailed_formatter)
    logger.addHandler(console_handler)

    # File handler (logs directory)
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(
        logs_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)

    # Error file handler (separate file for errors)
    error_handler = logging.FileHandler(
        logs_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)

    return logger


# Alias for compatibility
def get_logger(name: str = "taiwantea") -> logging.Logger:
    """
    Get or create a logger instance (alias for setup_logger)

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    return setup_logger(name)


# Create default logger instance
logger = setup_logger()
