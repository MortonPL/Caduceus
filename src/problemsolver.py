from os import chmod as os_chmod
from os import remove as os_remove
from os import rename as os_rename
from os.path import join as os_path_join
from os.path import relpath as os_path_relpath
from os.path import commonpath as os_path_commonpath
from copy import deepcopy
import stat
from src.file import File, Flags

CODES = [stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR,
         stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
         stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH]


def solve_name_all(target: dict[str, File], dir: dict[str, File], illegal_chars: list[str], legal_char: str) -> tuple[dict[str, File], dict[str, File]]:
    new_target = deepcopy(target)
    for fullname, file in target.items():
        if file.state_flags[2]:
            new_target.pop(fullname)
            new_file = solve_name(file, illegal_chars, legal_char)
            new_target[os_path_join(new_file.path, new_file.name)] = new_file

    new_dir = deepcopy(dir)
    for fullname, file in dir.items():
        if file.state_flags[2]:
            new_dir.pop(fullname)
            new_file = solve_name(file, illegal_chars, legal_char)
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


def solve_samename_all(target: dict[str, File], dir: dict[str, File]) -> tuple[dict[str, File], dict[str, File]]:
    new_target = deepcopy(target)
    for fullname, file in target.items():
        if file.state_flags[5]:
            solve_samename(file)
            new_target.pop(fullname)
    target = new_target

    new_dir = deepcopy(dir)
    for fullname, file in dir.items():
        if file.state_flags[5]:
            solve_samename(file)
            new_dir.pop(fullname)
    dir = new_dir

    return new_target, new_dir

def solve_samename(file: File) -> None:
    os_remove(os_path_join(file.path, file.name))

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


def solve_flags_all(target: dict[int, File], dir: dict[int, File], desired_flags: Flags) -> tuple[dict[int, File], dict[int, File]]:
    for _, file in target.items():
        if file.state_flags[3]:
            solve_flags(file, desired_flags)

    for _, file in dir.items():
        if file.state_flags[3]:
            solve_flags(file, desired_flags)

    return target, dir

def solve_flags(file: File, desired_flags: Flags) -> None:
    flags = 0

    for flag, code in zip(desired_flags, CODES):
        if flag is None:
            continue
        if flag:
            flags |= code
        else:
            flags &= ~code
    os_chmod(os_path_join(file.path, file.name), flags)
    file.state_flags[3] = False
