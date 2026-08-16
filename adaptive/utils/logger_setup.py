"""
utils/logger_setup.py
=====================
Centralised Loguru configuration.

Import `get_logger` once per module:

    from utils.logger_setup import get_logger
    logger = get_logger(__name__)
"""

import sys
from loguru import logger

_configured = False   # guard against double-initialisation


def setup_logging(
    log_file: str = "student_system.log",
    console_level: str = "DEBUG",
    file_level: str = "DEBUG",
) -> None:
    """
    Configure Loguru handlers.
    Safe to call multiple times — only runs once.
    """
    global _configured
    if _configured:
        return

    # Remove the default Loguru handler
    logger.remove()

    # ── Coloured console output ──────────────────────────────────────────────
    logger.add(
        sys.stderr,
        format=(
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan> - "
            "<level>{message}</level>"
        ),
        level=console_level,
        colorize=True,
    )

    # ── Rotating file log ────────────────────────────────────────────────────
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level=file_level,
        rotation="1 MB",    # rotate when file reaches 1 MB
        retention="7 days", # keep logs for 7 days
        diagnose=False,     # hide variable values in tracebacks (privacy)
        enqueue=True,       # thread-safe writes
    )

    _configured = True
    logger.debug("Loguru logging initialised.")


def get_logger(name: str = "student_system"):
    """
    Return the shared Loguru logger, binding `name` for context.
    Call setup_logging() first (main.py does this automatically).
    """
    return logger.bind(name=name)