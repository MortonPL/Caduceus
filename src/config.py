from argparse import ArgumentParser
from configparser import ConfigParser
from re import compile as re_compile

class Config(dict):
    __parser__: ArgumentParser
    __configparser__: ConfigParser

    def __init__(self) -> None:
        super(Config, self).__init__()
        self.__parser__ = ArgumentParser()
        self.__parser__.add_argument('target', action='store',
                                     help='target directory')
        self.__parser__.add_argument('directories', action='extend', nargs='+', type=str, default=[],
                                     help='list of directories to compare with')
        self.__parser__.add_argument('-c', '--config', action='store', nargs='?', type=str, default=None,
                                     help='custom config file location')
        self.__configparser__ = ConfigParser()

    def parse(self) -> None:
        self.parse_args()
        self.parse_config()

    def parse_args(self) -> None:
        # parse command line args
        args = vars(self.__parser__.parse_args())
        self.update(args)

    def parse_config(self) -> None:
        # get config file name from args
        if self['config'] is None:
            self['config'] = 'caduceus.conf'
        self.__configparser__.read(self['config'])

        # expect these tags
        noop = lambda x: x
        list_parser = lambda x: x.split()
        tags = [('DefaultFilePermissions', 'rw-r–-r–-', noop),
                ('IllegalCharacters', [':', '"', ';', '*', '?', '$', '#', '\'', '|', '\\'], list_parser),
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

        # couldn't find the config file or the section
        else:
            print(f"Warning: couldn't find config file: {self['config']}. Using defaults...")
            for tag in tags:
                self[camel2snake.sub(r'_\1', tag[0]).lower()] = tag[1]
