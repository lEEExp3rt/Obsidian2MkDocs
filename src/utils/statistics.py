"""
Obsidian2MkDocs module: utils/statistics

This module contains the statistics function.

:author: !EEExp3rt
:date: 2025-02-08
"""

from . import logger


class Statistics:
    """
    Statistics class

    This class provides the statistics function for the conversion process.
    """

    def __init__(self):
        """
        Initialize the statistics counters.
        """

        self.__total: int = 0
        self.__converted: int = 0
        self.__failed: list = []
    
    def converted(self) -> None:
        """
        Increment the converted counter.
        """

        self.__converted += 1
        self.__total += 1
    
    def failed(self, file: str) -> None:
        """
        Increment the failed counter.
        """

        self.__failed.append(file)
        self.__total += 1

    def show(self) -> None:
        """
        Print statistics of the conversion process.
        """
    
        logger.info(f"● Successfully converted {self.__converted} files out of {self.__total} files.")
        if self.__failed:
            logger.warning(f"▼ Failed to convert {len(self.__failed)} files:")
            for fail in self.__failed:
                logger.warning(f"  - {fail}")
