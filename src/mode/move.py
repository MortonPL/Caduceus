from os import rename as os_rename
from os.path import join as os_path_join
from os.path import relpath as os_path_relpath
from os.path import commonpath as os_path_commonpath
from os.path import dirname as os_path_dirname
from copy import deepcopy

from src.config import Config
from src.file import File
from src.prompt import prompt_move

def run_move(target: dict[str, File], dir: dict[str, File], conf: Config) -> tuple[dict[str, File], dict[str, File]]:
    target_root = conf['target']
    dir_roots = conf['directories']
    analyze_movable_all(target, dir)
    new_target = deepcopy(target)
    for fullname, file in target.items():
        if not file.state_flags[6]:
            continue
        destination = solve_movable_1(fullname, target_root, dir_roots)
        if not prompt_move(fullname, destination):
            continue
        new_target.pop(fullname)
        new_file = solve_movable_2(file, fullname, destination)
        new_target[os_path_join(new_file.path, new_file.name)] = new_file

    new_dir = deepcopy(dir)
    for fullname, file in dir.items():
        if not file.state_flags[6]:
            continue
        destination = solve_movable_1(fullname, target_root, dir_roots)
        if not prompt_move(fullname, destination):
            continue
        new_dir.pop(fullname)
        new_file = solve_movable_2(file, fullname, destination)
        new_dir[os_path_join(new_file.path, new_file.name)] = new_file

    return new_target, new_dir

def solve_movable_1(fullname: str, target_root: str, dir_roots: list[str]) -> str:
    for root in dir_roots:
        d_prefix = os_path_commonpath([root, fullname])
        # if it's in *this* root
        if d_prefix == root:
            return os_path_join(target_root, os_path_relpath(fullname, root))
    return ''

def solve_movable_2(file: File, fullname: str, destination: str) -> File:
    os_rename(fullname, destination)
    file.path = os_path_dirname(destination)
    return file

def analyze_movable_all(target: dict[str, File], dir: dict[str, File]):
    for _, dfile in dir.items():
        for _, tfile in target.items():
            if dfile.name == tfile.name:
                break
            dfile.state_flags[6] = True
