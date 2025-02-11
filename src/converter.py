"""
Obsidian2MkDocs module: converter

This module wraps the conversion process of Obsidian notes to MkDocs notes.

:author: !EEExp3rt
:date: 2025-02-07
"""

from .utils import file_manager, logger, statistics
from .parser import parse_content
from .frontmatters import frontmatter
from .admonitions import admonition
from .codes import code_block, inline_code


def convert(src: str, dest: str, configs: dict, statistics: statistics.Statistics ,overwrite: bool = False) -> None:
    """
    Convert 1 file from Obsidian to MkDocs.

    If the file is a Markdown file, it will be converted while other files will be copied.

    :param src: The input file path.
    :param dest: The output file path.
    :param configs: The configuration dictionary.
    :param statistics: The statistics object.
    :param overwrite: Whether to overwrite the existing file. Default is False.
    """

    def __convert() -> bool:
        """
        Convert 1 Obsidian note to MkDocs note.

        :return: True if the conversion is successful, False otherwise.
        """

        lines = file_manager.read_input(src)
        # Start parsing.
        types = parse_content(lines)
        header, body, types = frontmatter.process(lines, types, configs['frontmatter'])
        body = admonition.convert(body, types, configs['indent'])
        body = code_block.convert(body, types, configs['code_block']['highlight_keywords'])
        body = inline_code.convert(body, types)
        # End parsing.
        return file_manager.write_output(dest, header + body, overwrite)

    if file_manager.check_file(src):
        if __convert():
            logger.debug(f"√ Converted {src} to {dest}")
            statistics.converted()
        else:
            statistics.failed(src)
    else:
        if file_manager.copy_file(src, dest, overwrite):
            logger.debug(f"√ Copied {src} to {dest}")
            statistics.converted()
        else:
            statistics.failed(src)
