"""
Obsidian2MkDocs module: code_block

This module handles code block convertion from Obsidian to MkDocs.

:author: !EEExp3rt
:date: 2025-02-02
"""

from ..parser import ContentType
from ..utils.algorithm import merge_intervals
import re


def convert(lines: list[str], types: list[dict], hl_keywords: list[str]) -> list[str]:
    """
    Convert code blocks from Obsidian to MkDocs.

    :param lines: The content lines from Obsidian.
    :param types: The content types of each line.
    :param hl_keywords: The keywords for highlighting.
    :return: The converted text in MkDocs format.
    """

    def _parse_header(line: str) -> str:
        """
        Parse the header of a code block.

        :param line: The content line.
        :return: The header after parsing.
        """

        language = re.search(r'^.*```+\S*', line).group()

        # Title.
        title = ""
        matches = re.search(r'title[:|=]".+"', line) or re.search(r'fold[:|=]".+"', line)
        if matches:
            title = ' title=' + re.search(r'".+"', matches.group()).group()
            line = line.replace(matches.group(), '')
        
        # Highlight lines.
        hl_lines = ""
        for keyword in hl_keywords:
            matches = re.search(rf'{keyword}:\S+', line)
            if matches:
                highlight = matches.group()
                hl_lines += highlight[highlight.index(':') + 1:] + ','
        if hl_lines:
            hl_lines = ' hl_lines="' + merge_intervals(hl_lines[:-1]) + '"'
        
        # Start line.
        linenums = ""
        matches = re.search(r'ln:\S+', line)
        if matches:
            number = matches.group()[3:]
            if number.isdigit():
                linenums = ' linenums="' + number + '"'
            elif number.lower() != 'false':
                linenums = ' linenums="1"'
        
        return language + title + linenums + hl_lines + '\n'
    
    output = []
    prev: bool = None

    cnt = 1
    for index in range(len(lines)):
        is_code_block = types[index].get(ContentType.CODE_BLOCK)
        output.append(_parse_header(lines[index]) if is_code_block and not prev else lines[index])
        prev = is_code_block
        cnt += 1

    return output
