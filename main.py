from src.config import Config
from src.creeper import Creeper
from src.file import Flags
from src.problemfinder import analyze_flags_all, analyze_name_all, analyze_temp_all, analyze_duplicate_all, analyze_movable_all, analyze_samename_all
from src.problemsolver import solve_empty_all, solve_temp_all, solve_dupes_all, solve_name_all, solve_movable_all, solve_samename_all, solve_flags_all


conf = Config()
conf.parse()

target_creeper = Creeper()
target_creeper.creep(conf['target'])

dirs_creeper = Creeper()
for dir in conf['directories']:
    dirs_creeper.creep(dir)

target_dict = target_creeper.file_dict
dirs_dict = dirs_creeper.file_dict

target_dict, dirs_dict = solve_empty_all(target_dict, dirs_dict)

analyze_temp_all(target_dict, dirs_dict, Flags(conf['temporary_file_extensions']))
target_dict, dirs_dict = solve_temp_all(target_dict, dirs_dict)

analyze_duplicate_all(target_dict, dirs_dict)
target_dict, dirs_dict = solve_dupes_all(target_dict, dirs_dict)

analyze_name_all(target_dict, dirs_dict, Flags(conf['illegal_characters']))
target_dict, dirs_dict = solve_name_all(target_dict, dirs_dict, conf['illegal_characters'], conf['illegal_character_replacement'])

analyze_samename_all(target_dict, dirs_dict)

for k, v in target_dict.items():
    print(k, v)
for k, v in dirs_dict.items():
    print(k, v)

target_dict, dirs_dict = solve_samename_all(target_dict, dirs_dict)

analyze_movable_all(target_dict, dirs_dict)
target_dict, dirs_dict = solve_movable_all(target_dict, dirs_dict, conf['target'], conf['directories'])

analyze_flags_all(target_dict, dirs_dict, Flags(conf['default_file_permissions']))
target_dict, dirs_dict = solve_flags_all(target_dict, dirs_dict, Flags(conf['default_file_permissions']))
