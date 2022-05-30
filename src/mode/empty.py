from copy import deepcopy
from os import remove as os_remove
from os.path import join as os_path_join

from src.config import Config
from src.file import File
from src.prompt import prompt_empty

def run_empty(target: dict[str, File], dir: dict[str, File], conf: Config) -> tuple[dict[str, File], dict[str, File]]:
    new_target = deepcopy(target)
    for fullname, file in target.items():
        if not file.state_flags[0]:
            continue
        if not prompt_empty(fullname):
            continue
        solve_empty(file)
        new_target.pop(fullname)
    target = new_target

    new_dir = deepcopy(dir)
    for fullname, file in dir.items():
        if not file.state_flags[0]:
            continue
        if not prompt_empty(fullname):
            continue
        solve_empty(file)
        new_dir.pop(fullname)
    dir = new_dir

    return new_target, new_dir

def solve_empty(file: File) -> None:
    os_remove(os_path_join(file.path, file.name))
