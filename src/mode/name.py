from copy import deepcopy
from os import rename as os_rename
from os.path import join as os_path_join

from src.config import Config
from src.file import File, Flags
from src.prompt import prompt_name

def run_name(target: dict[str, File], dir: dict[str, File], conf: Config) -> tuple[dict[str, File], dict[str, File]]:
    analyze_name_all(target, dir, Flags(conf['illegal_characters']))
    new_target = deepcopy(target)
    for fullname, file in target.items():
        if not file.state_flags[2]:
            continue
        if not prompt_name(fullname):
            continue
        new_target.pop(fullname)
        new_file = solve_name(file, Flags(conf['illegal_characters']), conf['illegal_character_replacement'])
        new_target[os_path_join(new_file.path, new_file.name)] = new_file

    new_dir = deepcopy(dir)
    for fullname, file in dir.items():
        if not file.state_flags[2]:
            continue
        if not prompt_name(fullname):
            continue
        new_dir.pop(fullname)
        new_file = solve_name(file, Flags(conf['illegal_characters']), conf['illegal_character_replacement'])
        new_dir[os_path_join(new_file.path, new_file.name)] = new_file

    return new_target, new_dir


def solve_name(file: File, illegal_chars: list[str], legal_char: str) -> File:
    old_name = file.name
    for ichar in illegal_chars:
        if ichar in file.name:
            file.name = file.name.replace(ichar, legal_char)
            os_rename(os_path_join(file.path, old_name), os_path_join(file.path, file.name))
            file.state_flags[2] = False
    return file


def analyze_name_all(target: dict[str, File], dir: dict[str, File], illegal_chars: list[str]):
    for _, file in target.items():
        analyze_name(file, illegal_chars)

    for _, file in dir.items():
        analyze_name(file, illegal_chars)


def analyze_name(file: File, illegal_chars: list[str]):
         for char in illegal_chars:
            if char in file.name:
                file.state_flags[2] = True
                break
