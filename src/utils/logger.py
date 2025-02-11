"""
Obsidian2MkDocs module: utils/logger

This module contains some logging functions.

:author: !EEExp3rt
:date: 2025-02-06
"""

from multiprocessing import Value
from colorlog import ColoredFormatter
import logging, functools


logger = logging.getLogger("Obsidian2MkDocs")
handler = logging.StreamHandler()
formatter = ColoredFormatter(
    "%(log_color)s[%(name)s] %(message)s",
    datefmt="%Y-%m-%d~%H:%M:%S",
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

def error_check(func):
    """
    Decorator to detect exceptions and log them.

    :param func: The function to decorate.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError or KeyError or ValueError as e:
            logger.error(e)
            exit(1)
        except Exception as e:
            raise e

    return wrapper

def warning(msg: str) -> None:
    """
    Log a warning message.

    :param msg: The message to log.
    """

    logger.warning(msg)

def info(msg: str) -> None:
    """
    Log an info message.

    :param msg: The message to log.
    """

    logger.info(msg)

def debug(msg: str) -> None:
    """
    Log a debug message.

    :param msg: The message to log.
    """

    logger.debug(msg)

@error_check
def set_level(level: str) -> None:
    """
    Set the logging level.

    :param level: The logging level.
    :raises ValueError: If the logging level is unknown.
    """

    if level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif level == 'INFO':
        logger.setLevel(logging.INFO)
    elif level == 'WARNING':
        logger.setLevel(logging.WARNING)
    elif level == 'ERROR':
        logger.setLevel(logging.ERROR)
    elif level == 'CRITICAL':
        logger.setLevel(logging.CRITICAL)
    else:
        raise ValueError(f"Unknown logging level {level}!!!")
