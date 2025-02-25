"""
Obsidian2MkDocs module: frontmatter

This module processes the frontmatter of the markdown files.

:author: !EEExp3rt
:date: 2025-02-09
"""

from ..parser import ContentType
import yaml


def process(lines: list[str], types: list[dict], conditions: list[str] = None) -> tuple[list[str], list[str], list[dict]]:
    """
    Process the frontmatter of the markdown files.

    :param lines: The content lines from Obsidian.
    :param types: The content types of each line.
    :param conditions: The conditions to select items in the frontmatter. Default is None.
    :return: The processed frontmatter, body and types.
    """

    def _split() -> tuple[list[str], list[str], list[dict]]:
        """
        Split the content into header and body.

        :return : The tuple of the header, body and types.
        """

        index = 0
        while index < len(types) and types[index][ContentType.FRONTMATTER]:
            index += 1
        return lines[:index], lines[index:], types[index:]
    
    def _filter(header: list[str]) -> list[str]:
        """
        Filter the header content.

        :param header: The header content.
        :return: The filtered header content.
        """

        data = yaml.safe_load("".join(header[1:-1]))
        if data is None:
            return []
        output = {}
        for key in data.keys():
            if key in conditions:
                output[key] = data[key]
        return ['---\n'] + yaml.safe_dump(output, allow_unicode=True, sort_keys=True).splitlines(True) + ['---\n'] if output else []

    if not lines:
        return [], [], []
    
    header, body, types = _split()
    header = _filter(header)
    return header, body, types
