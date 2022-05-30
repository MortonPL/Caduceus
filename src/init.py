from src.config import Config
from src.creeper import Creeper

def init(main_path: str):
    conf = Config()
    conf.parse(main_path)

    # walk through the target directory
    target_creeper = Creeper()
    target_creeper.creep(conf['target'])

    # walk through other directories
    dirs_creeper = Creeper()
    for dir in conf['directories']:
        dirs_creeper.creep(dir)

    return target_creeper.file_dict, dirs_creeper.file_dict, conf
