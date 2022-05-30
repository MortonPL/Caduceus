from os import rename as os_rename
from os.path import join as os_path_join
from os.path import relpath as os_path_relpath
from os.path import commonpath as os_path_commonpath
from copy import deepcopy
from src.file import File




def solve_movable_all(target: dict[str, File], dir: dict[str, File], target_root: str, dir_roots: list[str]) -> tuple[dict[str, File], dict[str, File]]:
    new_target = deepcopy(target)
    for fullname, file in target.items():
        if file.state_flags[6]:
            new_target.pop(fullname)
            new_file = solve_movable(file, target_root, dir_roots)
            new_target[os_path_join(new_file.path, new_file.name)] = new_file

    new_dir = deepcopy(dir)
    for fullname, file in dir.items():
        if file.state_flags[6]:
            new_dir.pop(fullname)
            new_file = solve_movable(file, target_root, dir_roots)
            new_dir[os_path_join(new_file.path, new_file.name)] = new_file

    return new_target, new_dir

def solve_movable(file: File, target_root: str, dir_roots: list[str]) -> File:
    for root in dir_roots:
        d_prefix = os_path_commonpath([root, file.path])
        # if it's in *this* root
        if d_prefix == root:
            named_path = os_path_join(file.path, file.name)
            destination = os_path_join(target_root, os_path_relpath(named_path, root))
            os_rename(named_path, destination)
            file.path = destination
    return file
