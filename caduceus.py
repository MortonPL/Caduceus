from src.init import init
from src.problemfinder import analyze_movable_all
from src.problemsolver import solve_movable_all
from src.mode.duplicate import run_dupe
from src.mode.empty import run_empty
from src.mode.flag import run_flag
from src.mode.name import run_name
from src.mode.samename import run_samename
from src.mode.temp import run_temp

target_dict, dirs_dict, conf = init()

target_dict, dirs_dict = run_empty(target_dict, dirs_dict)
target_dict, dirs_dict = run_temp(target_dict, dirs_dict, conf)
target_dict, dirs_dict = run_dupe(target_dict, dirs_dict)
target_dict, dirs_dict = run_name(target_dict, dirs_dict, conf)
target_dict, dirs_dict = run_samename(target_dict, dirs_dict)
target_dict, dirs_dict = run_flag(target_dict, dirs_dict, conf)

analyze_movable_all(target_dict, dirs_dict)
target_dict, dirs_dict = solve_movable_all(target_dict, dirs_dict, conf['target'], conf['directories'])
