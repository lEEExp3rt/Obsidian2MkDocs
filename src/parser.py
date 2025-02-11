"""
Obsidian2MkDocs module: parser

This module parses the content types of each line in the Markdown file.

:author: !EEExp3rt
:date: 2025-01-31
"""

from enum import Enum
import re


class ContentType(Enum):
    """
    The content type of one line in the Markdown file.

    Only block-level elements are considered.
    """

    PLAINTEXT = 0
    ADMONITION = 1
    CODE_BLOCK = 2
    FRONTMATTER = 3


def parse_content(lines: list[str]) -> list[dict]:
    """
    Parse the content types in the Markdown file.
    
    :param lines: The content lines of the Markdown file.
    :return: The content types of each line.
    """

    def _preprocess(lines: list[str]) -> int:
        """
        Preprocess and parse the frontmatter.
        
        :param lines: The content lines of the Markdown file.
        :return: The line index of the first line of the body.
        """

        frontmatter = re.compile(r'^---$')
        index = 0

        if frontmatter.match(lines[0]):
            for line in lines[1:]:
                index += 1
                if frontmatter.match(line):
                    break
            index += 1
        
        return index

    def _parse_body(lines: list[str]) -> list[dict]:
        """
        Parse the body content types in the Markdown file.
        
        :param lines: The content lines of the Markdown file.
        :return: The content types of each line.
        """
    
        # Content types regex patterns.
        admonition_header = re.compile(r'^(> )+\[!\w+\][-|+]?')
        admonition_body = re.compile(r'^(> )*>')
        code_block = re.compile(r'^(> )*```+')
    
        output = [] # Output list.
        indent = 0 # Admonition indent level.
        code = 0 # Code block backticks count.
    
        for line in lines:
            isCode = code_block.match(line)
            if code: # Already in a code block.
                if isCode and isCode.group().count('`') == code: # End a code block.
                    code = 0
                else: # Still in a code block.
                    pass
            else: # Not in a code block.
                if isCode: # Start a code block.
                    code = isCode.group().count('`')
                else: # Not in a code block.
                    isAdmonition = admonition_header.match(line)
                    if isAdmonition:
                        indent += 1
                    else:
                        isBody = admonition_body.match(line)
                        indent = min(indent, isBody.group().count('>')) if isBody else 0
            output.append({
                ContentType.ADMONITION: indent,
                ContentType.CODE_BLOCK: code > 0,
                ContentType.PLAINTEXT: True if not (indent or code) else False,
                ContentType.FRONTMATTER: False
            })
        
        return output
    
    if not lines:
        return []

    index = _preprocess(lines)
    return [{
        ContentType.ADMONITION: 0,
        ContentType.CODE_BLOCK: False,
        ContentType.PLAINTEXT: False,
        ContentType.FRONTMATTER: True
    } for _ in range(index)] + _parse_body(lines[index:])
