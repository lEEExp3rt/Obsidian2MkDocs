"""
Obsidian2MkDocs module: utils/cli

This module provides the command-line interface.

:author: !EEExp3rt
:date: 2025-02-08
"""

import argparse


def parse() -> dict:
    """
    Parse command-line arguments for Obsidian2MkDocs.

    :return: The parsed arguments as a dictionary.
    """

    parser = argparse.ArgumentParser(description='Obsidian2MkDocs: A helpful tool to convert your Obsidian notes to MkDocs notes.')

    parser.add_argument('src', type=str, help='Source file or directory path')
    parser.add_argument('dest', type=str, nargs='?', help='Destination directory path, default is `output/`')
    parser.add_argument('-c', '--config', type=str, default='configs.yml', help='Configuration file path, default is `configs.yml`')
    parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite existing files')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    return vars(parser.parse_args())
