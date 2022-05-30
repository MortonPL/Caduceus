from src.file import Flags
from src.init import init
from src.problemfinder import analyze_flags_all, analyze_movable_all
from src.problemsolver import solve_movable_all, solve_flags_all
from src.mode.empty import run_empty
from src.mode.temp import run_temp
from src.mode.duplicate import run_dupe
from src.mode.name import run_name
from src.mode.samename import run_samename

target_dict, dirs_dict, conf = init()

target_dict, dirs_dict = run_empty(target_dict, dirs_dict)
target_dict, dirs_dict = run_temp(target_dict, dirs_dict, conf)
target_dict, dirs_dict = run_dupe(target_dict, dirs_dict)
target_dict, dirs_dict = run_name(target_dict, dirs_dict, conf)
target_dict, dirs_dict = run_samename(target_dict, dirs_dict)

analyze_movable_all(target_dict, dirs_dict)
target_dict, dirs_dict = solve_movable_all(target_dict, dirs_dict, conf['target'], conf['directories'])

analyze_flags_all(target_dict, dirs_dict, Flags(conf['default_file_permissions']))
target_dict, dirs_dict = solve_flags_all(target_dict, dirs_dict, Flags(conf['default_file_permissions']))
