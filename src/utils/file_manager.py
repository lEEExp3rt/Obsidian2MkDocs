"""
Obsidian2MkDocs module: utils/files_manager

This module contains some file management functions.

:author: !EEExp3rt
:date: 2025-02-01
"""

from . import logger
from pathspec import GitIgnoreSpec
import os, shutil
import yaml


@logger.error_check
def load_config(config_file: str) -> dict:
    """
    Load the YAML configuration file.

    :param config_file: The configuration file path.
    :return: The configuration dictionary.
    :raises FileNotFoundError: If the configuration file is not found.
    :raises KeyError: If the configuration file is not complete.
    """

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file {os.path.abspath(config_file)} not exists!!!")

    with open(config_file, 'r') as f:
        configs = yaml.safe_load(f)
    if 'indent' not in configs:
        raise KeyError(f"Missing 'indent' in configuration file {config_file}!!!")
    if 'frontmatter' not in configs:
        raise KeyError(f"Missing 'frontmatter' in configuration file {config_file}!!!")
    if 'code_block' not in configs:
        raise KeyError(f"Missing 'code_block' in configuration file {config_file}!!!")
    if 'highlight_keywords' not in configs['code_block']:
        raise KeyError(f"Missing 'code_block.highlight_keywords' in configuration file {config_file}!!!")
    if 'pdf' not in configs:
        raise KeyError(f"Missing 'pdf' in configuration file {config_file}!!!")
    if 'height' not in configs['pdf']:
        raise KeyError(f"Missing 'pdf.height' in configuration file {config_file}!!!")
    if 'ignores' not in configs:
        raise KeyError(f"Missing 'ignores' in configuration file {config_file}!!!")
    return configs

def read_input(input_file: str) -> list[str]:
    """
    Read the input Obsidian notes file and return the content as a list of strings.

    :param input_file: The input file path.
    :return: The content of the input file as a list of strings.
    """

    with open(input_file, 'r') as f:
        return f.readlines()

def write_output(output_file: str, content: list[str], overwrite: bool = False) -> bool:
    """
    Write the converted content to the output file.

    :param output_file: The output file path.
    :param content: The content to write to the output file.
    :param overwrite: Whether to overwrite the output file if it already exists. Default is False.
    :return: True if the output is written successfully, False otherwise.
    """

    directory = os.path.dirname(output_file)
    if os.path.exists(output_file) and not overwrite:
        return False

    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    with open(output_file, 'w') as f:
        f.writelines(content)
    return True

@logger.error_check
def files_from_to(src: str, dest: str, filters: list[str] = None) -> tuple[list[str], list[str]]:
    """
    List all files in `src` and their destination paths in `dest`.

    :param src: The source file or directory path.
    :param dest: The destination directory path.
    :param filters: Path filter to ignore some files. Default is None. The same as `.gitignore` file.
    :return: A tuple of the source and destination files list.
    :raises FileNotFoundError: If the source path is not found or invalid.
    """

    def __filter_paths(paths: list[str]) -> list[str]:
        """
        Filter the paths based on the filters.

        :param paths: The paths to check.
        :return: The filtered paths.
        """

        if not filters:
            return paths

        spec = GitIgnoreSpec.from_lines(filters)
        output = []
        for path in paths:
            if spec.match_file(path):
                logger.debug(f"Ignoring {path}")
            else:
                output.append(path)

        return output

    def __list_files(path: str) -> list[str]:
        """
        List all files in the path.
    
        Make sure the path exists and is valid.
    
        :param path: The directory path.
        :return: A list of all files in the path.
        """

        filelist = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                filelist.append(item)
            elif os.path.isdir(item_path):
                filelist.extend(os.path.join(item, f) for f in __list_files(item_path))
        return filelist

    src_ = os.path.abspath(src)
    dest_ = os.path.abspath(dest)

    if os.path.isfile(src):
        return [src_], [os.path.join(dest_, os.path.basename(src))]

    if os.path.isdir(src):
        items = __filter_paths(__list_files(src))
        return [os.path.join(src_, item) for item in items], [os.path.join(dest_, item) for item in items]

    raise FileNotFoundError(f"Invalid source path: {src}!!!")

def check_file(path: str) -> bool:
    """
    Check if the file is a Markdown file.

    :param path: The file path.
    :return: True if the file is a Markdown file, False otherwise.
    """

    return os.path.splitext(path)[1] == '.md'


def copy_file(src: str, dest: str, overwrite: bool = False) -> bool:
    """
    Copy non-Markdown file from `src` to `dest`.

    :param src: The source file path.
    :param dest: The destination file path.
    :param overwrite: Whether to overwrite the destination file if it already exists. Default is False.
    :return: True if the file is copied successfully, False otherwise.
    """

    if os.path.exists(dest) and not overwrite:
        return False

    directory = os.path.dirname(dest)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    shutil.copy2(src, dest)
    return True
