from src.file import Flags
from src.init import init
from src.problemfinder import analyze_flags_all, analyze_name_all, analyze_movable_all, analyze_samename_all
from src.problemsolver import solve_name_all, solve_movable_all, solve_samename_all, solve_flags_all
from src.mode.empty import run_empty
from src.mode.temp import run_temp
from src.mode.duplicate import run_dupes

target_dict, dirs_dict, conf = init()

target_dict, dirs_dict = run_empty(target_dict, dirs_dict)
target_dict, dirs_dict = run_temp(target_dict, dirs_dict, conf)
target_dict, dirs_dict = run_dupes(target_dict, dirs_dict)

analyze_name_all(target_dict, dirs_dict, Flags(conf['illegal_characters']))
target_dict, dirs_dict = solve_name_all(target_dict, dirs_dict, conf['illegal_characters'], conf['illegal_character_replacement'])

analyze_samename_all(target_dict, dirs_dict)

target_dict, dirs_dict = solve_samename_all(target_dict, dirs_dict)

analyze_movable_all(target_dict, dirs_dict)
target_dict, dirs_dict = solve_movable_all(target_dict, dirs_dict, conf['target'], conf['directories'])

analyze_flags_all(target_dict, dirs_dict, Flags(conf['default_file_permissions']))
target_dict, dirs_dict = solve_flags_all(target_dict, dirs_dict, Flags(conf['default_file_permissions']))
