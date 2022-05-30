from argparse import ArgumentParser
from configparser import ConfigParser
from re import compile as re_compile
from os.path import abspath as os_path_abspath
from os.path import isabs as os_path_isabs
from os.path import join as os_path_join

class Config(dict):
    __parser__: ArgumentParser
    __configparser__: ConfigParser

    def __init__(self) -> None:
        super(Config, self).__init__()
        self.__parser__ = ArgumentParser(prog='Caduceus')
        self.__parser__.add_argument('-m', '--mode', action='store', nargs='?', type=lambda s: s.split(','),
                                     default=['empty', 'temp', 'dupes', 'badnames', 'samenames', 'flags', 'movable'],
                                     help='comma separated list of modes of operation, available modes: empty, temp, dupes, badnames, samenames, flags, movable. Defaults to all of them')
        self.__parser__.add_argument('target', action='store',
                                     help='target directory')
        self.__parser__.add_argument('directories', action='extend', nargs='+', type=str, default=[],
                                     help='list of directories to compare with')
        self.__parser__.add_argument('-c', '--config', action='store', nargs='?', type=str, default=None,
                                     help='custom config file location')
        self.__parser__.add_argument('-a', '--all', action='store_true',
                                     help='accept all changes')
        self.__configparser__ = ConfigParser()

    def parse(self, main_dir: str) -> None:
        # convert paths to absolute
        self.parse_args()
        self['target'] = os_path_abspath(self['target'])
        self['directories'] = [os_path_abspath(dir) if not os_path_isabs(dir) else dir for dir in self['directories']]
        self.parse_config(main_dir)

    def parse_args(self) -> None:
        # parse command line args
        args = vars(self.__parser__.parse_args())
        self.update(args)

    def parse_config(self, main_dir: str) -> None:
        # get config file name from args
        if self['config'] == None:
            self['config'] = os_path_join(main_dir, 'caduceus.conf')
        self.__configparser__.read(self['config'])

        # expect these tags and invoke these parsing actions on them
        noop = lambda x: x
        list_parser = lambda x: x.split()
        tags = [('DefaultFilePermissions', 'rw-r–-r–-', noop),
                ('IllegalCharacters', [':', ',', '"', ';', '*', '?', '$', '#', '\'', '|', '\\', '"'], list_parser),
                ('IllegalCharacterReplacement', '_', noop),
                ('TemporaryFileExtensions', ['*~', '*.tmp'], list_parser)]
        camel2snake = re_compile('(?!^)([A-Z]+)')

        # if there *is* a valid config file, read it
        if 'Globals' in self.__configparser__.keys():
            for tag in tags:
                if tag[0] in self.__configparser__['Globals'].keys():
                    self[camel2snake.sub(r'_\1', tag[0]).lower()] = tag[2](self.__configparser__['Globals'][tag[0]])
                else:
                    self[camel2snake.sub(r'_\1', tag[0]).lower()] = tag[1]
        # fall back to builtin defaults
        else:
            print(f"Warning: couldn't find config file: {self['config']}. Using defaults...")
            for tag in tags:
                self[camel2snake.sub(r'_\1', tag[0]).lower()] = tag[1]
