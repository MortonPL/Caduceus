from src.config import Config
from src.creeper import Creeper

def init():
    conf = Config()
    conf.parse()

    target_creeper = Creeper()
    target_creeper.creep(conf['target'])

    dirs_creeper = Creeper()
    for dir in conf['directories']:
        dirs_creeper.creep(dir)

    return target_creeper.file_dict, dirs_creeper.file_dict, conf
