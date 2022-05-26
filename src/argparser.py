from argparse import ArgumentParser
from typing import Any

class ArgParser:
    __parser__: ArgumentParser

    def __init__(self) -> None:
        self.__parser__ = ArgumentParser()
        self.__parser__.add_argument('target', action='store', help='target directory')
        self.__parser__.add_argument('directories', action='extend', nargs='+', type=str, default=[], help='list of directories to compare with')

    def parse(self) -> dict[str, Any]:
        return vars(self.__parser__.parse_args())
