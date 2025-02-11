"""
Obsidian2MkDocs module: inline_code

This module handles inline code convertion from Obsidian to MkDocs.

:author: !EEExp3rt
:date: 2025-02-02
"""

from ..parser import ContentType
import re


def convert(lines: list[str], types: list[dict]) -> list[str]:
    """
    Convert inline code from Obsidian to MkDocs.

    :param lines: The content lines from Obsidian.
    :param types: The content types of each line.
    :return: The converted text in MkDocs format.
    """

    def _parse_inline_code(line: str) -> str:
        """
        Parse the inline code.

        :param line: The content line.
        :return: The line after parsing.
        """

        output = ""
        matches = re.search(r'`\{\w+( icon)?( title:".*")?\}.*\S.*`', line)

        if matches:
            left, right = matches.span()
            content = matches.group()
            language = re.search(r'\w+', content).group() # Language.
            content = re.sub(r'\{\w+( icon)?( title:".*")?\}\s*', '#!' + language + ' ', content)
            output = line[:left] + content + line[right:]
        else: # No inline code.
            output = line

        return output

    output = []
    for line, type_ in zip(lines, types):
        output.append(_parse_inline_code(line) if type_.get(ContentType.PLAINTEXT) else line)
    
    return output
