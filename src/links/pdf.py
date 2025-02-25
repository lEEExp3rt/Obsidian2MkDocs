"""
Obsidian2MkDocs module: pdf

This module converts the embedded PDFs in Obsidian to HTML which can be used in MkDocs.

In Obsidian, PDF embeddings are represented as a link to the PDF file. This module converts the link to an HTML embed
tag which can be used in MkDocs.

:author: !EEExp3rt
:date: 2025-02-24
"""

from ..parser import ContentType
import re


def convert(lines: list[str], types: list[dict], height: int = 800) -> list[str]:
    """
    Convert PDF embeddings from Obsidian to MkDocs.

    :param lines: The content lines from Obsidian.
    :param types: The content types of each line.
    :param height: The height of the PDF viewer. Default is 800 px.
    :return: The converted text in MkDocs format.
    """

    def __replace(line: str) -> str:
        """
        Replace the PDF embedding in link format to HTML embed tag.

        :param line: The content line to be converted.
        :return: The converted content.
        """

        filename = re.search(r'\(([^)]+\.pdf)\)', line).group(0)[1:-1]
        html = f'<object data="../{filename}" type="application/pdf" width="100%" height="{height}px">' \
            f'<embed src="../{filename}" type="application/pdf" width="100%" height="{height}px"/></object>'
        return LINK.sub(html, line)

    LINK = re.compile(r'!\[([^\]]*)\]\(([^)]+\.pdf)\)')
    output = []
    for line_, type_ in zip(lines, types):
        is_pdf = LINK.search(line_)
        output.append(__replace(line_) if type_.get(ContentType.PLAINTEXT) and is_pdf else line_)
    return output
