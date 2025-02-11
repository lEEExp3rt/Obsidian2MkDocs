"""
This is the top module for Obsidian2MkDocs.

Obsidian2MkDocs is a helpful tool to convert your Obsidian notes to MkDocs type notes, it uses character replacement to convert Obsidian's syntax to MkDocs's syntax.

You can directly use the `main` function below to use the command-line interface, or you can import the `Obsidian2Mkdocs` class and use the class methods.

:author: !EEExp3rt
:date: 2025-01-30
"""

from .utils import file_manager, logger, statistics, cli
from .converter import convert as convert_1


def main():
    """
    Run Obsidian2MkDocs from the command line. You can directly use this function.
    """

    args = cli.parse()
    o2m = Obsidian2Mkdocs(args['config'])
    o2m.convert(src=args['src'], dest=args['dest'], overwrite=args['overwrite'], debug=args['debug'])


class Obsidian2Mkdocs:
    """
    Main class for Obsidian2MkDocs.

    Use `convert` method to convert your Obsidian note(s) to MkDocs note(s).
    """

    def __init__(self, config_file: str):
        """
        Load configuration file and initialize.

        :param config_file: The configuration file path.
        """

        self.__configs = file_manager.load_config(config_file)
        self.__statistics = statistics.Statistics()

    def convert(self, src: str, dest: str = None, overwrite: bool = False, debug: bool = False) -> None:
        """
        Convert your Obsidian notes to MkDocs notes.

        :param src: The input file or directory path.
        :param dest: The output directory path. If not provided, the output will be written to `output/` in the current working directory.
        :param overwrite: Whether to overwrite the existing files.
        :param debug: Whether to enable debug mode.
        """

        logger.set_level('DEBUG' if debug else 'INFO')
        srcs, dests = file_manager.files_from_to(src, dest or 'output', self.__configs['ignores'])
        for s, d in zip(srcs, dests):
            convert_1(s, d, self.__configs, self.__statistics, overwrite)
        self.__statistics.show()
