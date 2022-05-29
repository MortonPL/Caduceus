from copy import deepcopy
from fnmatch import filter as fnmatch_filter
from os import remove as os_remove
from os.path import join as os_path_join

from src.config import Config
from src.file import File, Flags
from src.prompt import prompt_temp

def run_temp(target: dict[str, File], dir: dict[str, File], conf: Config) -> tuple[dict[str, File], dict[str, File]]:
    analyze_temp_all(target, dir, Flags(conf['temporary_file_extensions']))

    new_target = deepcopy(target)
    for fullname, file in target.items():
        if not file.state_flags[1]:
            continue
        if not prompt_temp(fullname):
            continue
        solve_temp(file)
        new_target.pop(fullname)
    target = new_target

    new_dir = deepcopy(dir)
    for fullname, file in dir.items():
        if not file.state_flags[1]:
            continue
        if not prompt_temp(fullname):
            continue
        solve_temp(file)
        new_dir.pop(fullname)
    dir = new_dir

    return new_target, new_dir


def solve_temp(file: File) -> None:
    os_remove(os_path_join(file.path, file.name))


def analyze_temp_all(target: dict[str, File], dir: dict[str, File], patterns: list[str]):
    for _, file in target.items():
        analyze_temp(file, patterns)
    for _, file in dir.items():
        analyze_temp(file, patterns)


def analyze_temp(file: File, patterns: list[str]):
    for string in patterns:
        if fnmatch_filter([file.name], string):
            file.state_flags[1] = True
            break
