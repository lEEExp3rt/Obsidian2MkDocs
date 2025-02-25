"""
Obsidian2MkDocs module: anchor

This module processes the links to heading anchor in the markdown files.

The link to a heading anchor will be converted with the following features:

- Keep case sensitive
- Keep the Unicode characters and not percent-encoded
- Omits spaces and the special characters except the separator

:author: !EEExp3rt
:date: 2025-02-16
"""

from ..parser import ContentType
import re


def convert(lines: list[str], types: list[dict], seperator: str = None) -> list[str]:
    """
    Convert the links to heading anchors from Obsidian to MkDocs.

    :param lines: The content lines from Obsidian.
    :param types: The content types of each line.
    :param seperator: The seperator of the link.
    :return: The converted text in MkDocs format.
    """

    return NotImplementedError
