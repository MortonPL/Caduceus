from src.config import Config
from src.creeper import Creeper
from src.file import Flags
from src.problemfinder import analyze_flags, analyze_names, analyze_temp, analyze_duplicates, analyze_movables


conf = Config()
conf.parse()

target_creeper = Creeper()
target_creeper.creep(conf['target'])

dirs_creeper = Creeper()
for dir in conf['directories']:
    dirs_creeper.creep(dir)

analyze_flags(target_creeper.file_dict, dirs_creeper.file_dict, Flags(conf['default_file_permissions']))
analyze_names(target_creeper.file_dict, dirs_creeper.file_dict, Flags(conf['illegal_characters']))
analyze_temp(target_creeper.file_dict, dirs_creeper.file_dict, Flags(conf['temporary_file_extensions']))
analyze_duplicates(target_creeper.file_dict, dirs_creeper.file_dict)
analyze_movables(target_creeper.file_dict, dirs_creeper.file_dict)

print(target_creeper.file_dict)
print(dirs_creeper.file_dict)
