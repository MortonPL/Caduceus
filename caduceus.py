from src.init import init
from src.mode.duplicate import run_dupe
from src.mode.empty import run_empty
from src.mode.flag import run_flag
from src.mode.move import run_move
from src.mode.name import run_name
from src.mode.samename import run_samename
from src.mode.temp import run_temp
import src.prompt


target_dict, dirs_dict, conf = init()
if conf['all']:
    src.prompt.CACHE = [2]*7
for mode in conf['mode']:
    if mode == 'empty':
        target_dict, dirs_dict = run_empty(target_dict, dirs_dict, conf)
    elif mode == 'temp':
        target_dict, dirs_dict = run_temp(target_dict, dirs_dict, conf)
    elif mode == 'dupes':
        target_dict, dirs_dict = run_dupe(target_dict, dirs_dict, conf)
    elif mode == 'badnames':
        target_dict, dirs_dict = run_name(target_dict, dirs_dict, conf)
    elif mode == 'samenames':
        target_dict, dirs_dict = run_samename(target_dict, dirs_dict, conf)
    elif mode == 'flags':
        target_dict, dirs_dict = run_flag(target_dict, dirs_dict, conf)
    elif mode == 'movable':
        target_dict, dirs_dict = run_move(target_dict, dirs_dict, conf)
