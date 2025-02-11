"""
Obsidian2MkDocs module: admonition

This module handles admonitions convertion from Obsidian to MkDocs.

:author: !EEExp3rt
:date: 2025-01-30
"""

from ..parser import ContentType
import re


def convert(lines: list[str], types: list[dict], indents: int = 4) -> list[str]:
    """
    Convert admonitions from Obsidian to MkDocs.

    :param lines: The content lines from Obsidian.
    :param types: The content types of each line.
    :param indents: The number of spaces of one indent. Default is 4.
    :return: The converted text in MkDocs format.
    """

    def _parse_header(line: str, indent_level: int) -> str:
        """
        Parse the header of an admonition.

        :param line: The content line.
        :param indent_level: The indent level of the header.
        :return: The header after parsing.
        """

        header = re.findall(r'\S+', line)
        header_type = re.search(r'\w+', header[indent_level]).group() # Admonition type.
        match(header[indent_level][-1]): # Admonition fold.
            case '+':
                fold = "???+ "
            case '-':
                fold = "??? "
            case _:
                fold = "!!! "
        title = "" if indent_level + 1 == len(header) else ' "' + ' '.join(header[indent_level + 1:]) + '"'
        return indents * (indent_level - 1) * ' ' + fold + header_type + title + "\n"
    
    def _parse_body(line: str, indent_level: int, is_code_block: bool) -> str:
        """
        Parse the body of the admonition.

        This sub function will process the blank line in the admonition.

        :param line: The content line.
        :param indent_level: The indent level of the content line.
        :param is_code_block: Whether this content line belongs to a code block.
        :return: The body after parsing.
        """

        return '\n' \
            if re.match(r'^(> )+$', line) and not is_code_block \
            else (re.sub(r'> ', indents * ' ', line, indent_level) if indent_level > 0 else line)
    
    output = []
    prev = 0 # Previous indent level.

    for index in range(len(lines)):
        indent_level = types[index].get(ContentType.ADMONITION)
        is_code_block = types[index].get(ContentType.CODE_BLOCK)
        output.append(
            _parse_header(lines[index], indent_level) \
            if indent_level > prev \
            else _parse_body(lines[index], indent_level, is_code_block)
        )
        prev = indent_level
    
    return output
