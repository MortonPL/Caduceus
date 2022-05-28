from src.config import Config
from src.creeper import Creeper
from src.file import Flags
from src.problemfinder import analyze_flags_all, analyze_name_all, analyze_temp_all, analyze_duplicate_all, analyze_movable_all, analyze_samename_all


conf = Config()
conf.parse()

target_creeper = Creeper()
target_creeper.creep(conf['target'])

dirs_creeper = Creeper()
for dir in conf['directories']:
    dirs_creeper.creep(dir)

analyze_flags_all(target_creeper.file_dict, dirs_creeper.file_dict, Flags(conf['default_file_permissions']))
analyze_name_all(target_creeper.file_dict, dirs_creeper.file_dict, Flags(conf['illegal_characters']))
analyze_temp_all(target_creeper.file_dict, dirs_creeper.file_dict, Flags(conf['temporary_file_extensions']))
analyze_duplicate_all(target_creeper.file_dict, dirs_creeper.file_dict)
analyze_samename_all(target_creeper.file_dict, dirs_creeper.file_dict)
analyze_movable_all(target_creeper.file_dict, dirs_creeper.file_dict)

for k, v in target_creeper.file_dict.items():
    print(k, v)

for k, v in dirs_creeper.file_dict.items():
    print(k, v)
